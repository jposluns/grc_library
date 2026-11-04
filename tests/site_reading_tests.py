#!/usr/bin/env python3
"""List, and run, the regression-suite test classes that read a site-only path.

The pre-push guard's site-only fast path (tools/pre-push-guard.sh) skips the
full linter regression suite (gate 36) and runs, instead, the test classes this
module finds reading a path the fast path admits: anything under ``.web/`` or
``.baseline/``, or the root ``CHANGELOG.md``, ``README.md`` or ``NOTICE.md``.
``tests/test_web_draft.py`` runs whole on the fast path, so it is not scanned.
This file is a helper, not a test module: gate 36 discovers only
``tests/test_*.py``.

The detector reads each other top-level ``tests/test_*.py`` file as a Python
syntax tree, so the quoting of a string never matters. A top-level class is
selected when it is a ``unittest.TestCase`` subclass (by its base chain in the
file) and its code (methods, class attributes, decorators and bases) does one of:

* joins a repository-root path with an admitted path. A root is ``REPO_ROOT``
  (a bare name or any ``x.REPO_ROOT`` attribute), a name or ``self``/``cls``
  attribute assigned from one in the same module, class or function, or
  ``__file__`` taken up two directories (``Path(__file__).resolve().parent.parent``,
  ``.parents[1]``, ``os.path.dirname`` twice). A join is ``/``, ``joinpath``,
  ``os.path.join``, ``Path(root, ...)``, ``+``, ``%``, ``str.format`` or an
  f-string;
* passes an admitted path, as a string argument, to a path sink: a function or
  method whose own root join takes that parameter, a function passing its
  parameter on to a sink, or ``run_linter``, ``load_linter_module``,
  ``spec_from_file_location``, ``SourceFileLoader`` or ``runpy.run_path`` (the
  first two join the path to ``REPO_ROOT``; the others resolve it against the
  working directory, which is the repository root when the suite runs), so
  loading a module under ``.web/`` is a read;
* names a module-level function, class or assigned name that does either,
  or has such a base class (matched as a whole word in its source, so a
  mention in a string also counts; that errs towards running more).

A join is decided on its normalized path when every component is a string
constant and it does not climb above the root. Otherwise a join with an
admitted name as any known component is a read; one whose first component is
known and not admitted (``REPO_ROOT / "tools" / name``) is not; and one whose
first component is not a constant and not a parameter (``REPO_ROOT / rel``
with ``rel`` a local or an attribute), or that climbs above the root, is a read
when any string constant in the same top-level class or function, read as a
path from the root, names an admitted path (a later component of a ``/`` chain
does not count).

Not detected (each still runs in CI before merge, as the whole suite does): a
read through a path built some other way (a subprocess given a relative path
with ``cwd`` at the root, a linter run at its default root over a tree that
includes an admitted path, a root obtained through a function call, a
non-constant component that climbs back out of a known first directory), and a
read in a module-level statement that no class names.

Usage (the guard runs both from the repository root):
  python3 -B tests/site_reading_tests.py --list         # one tests.<module>.<Class> per line
  python3 -B tests/site_reading_tests.py --run ID...    # run those classes with unittest

Exit codes: 0 when --list lists at least one id, or when every test --run ran
passes; 1 when a test --run ran fails or errors; 2 for a usage error, a test
file that cannot be read or parsed, or no class selected.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import ast
import os
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SITE_DIRS = frozenset({".web", ".baseline"})
SITE_FILES = frozenset({"CHANGELOG.md", "README.md", "NOTICE.md"})
# Calls that resolve a relative path argument against the repository root here.
LOADERS = frozenset({"run_linter", "load_linter_module", "spec_from_file_location",
                     "SourceFileLoader", "run_path"})
# Calls whose single argument keeps the path it was given.
PASS_THROUGH = frozenset({"Path", "PurePath", "PosixPath", "str", "fspath", "abspath",
                          "realpath", "normpath"})
ROOT_NAME = "REPO_ROOT"
# Modules the fast path runs whole, so they are not scanned.
RUN_WHOLE = frozenset({"test_web_draft"})
TEST_ID = re.compile(r"tests\.test_\w+\.[A-Za-z_]\w*", re.ASCII)


def _call_name(node):
    func = node.func
    if isinstance(func, ast.Attribute):
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return None


def _file_parents(node):
    """How many directories above ``__file__`` the expression names, or None."""
    if isinstance(node, ast.Name):
        return 0 if node.id == "__file__" else None
    if isinstance(node, ast.Attribute):
        if node.attr == "parent":
            inner = _file_parents(node.value)
            return None if inner is None else inner + 1
        return None
    if isinstance(node, ast.Subscript):
        if (isinstance(node.value, ast.Attribute) and node.value.attr == "parents"
                and isinstance(node.slice, ast.Constant) and type(node.slice.value) is int):
            inner = _file_parents(node.value.value)
            return None if inner is None else inner + node.slice.value + 1
        return None
    if isinstance(node, ast.Call):
        name = _call_name(node)
        if isinstance(node.func, ast.Attribute) and name in ("resolve", "absolute"):
            return _file_parents(node.func.value)
        if len(node.args) == 1 and name in PASS_THROUGH:
            return _file_parents(node.args[0])
        if len(node.args) == 1 and name == "dirname":
            inner = _file_parents(node.args[0])
            return None if inner is None else inner + 1
    return None


def _is_root(node, aliases):
    """True when the expression names the repository root (tests/ is one level down)."""
    if isinstance(node, ast.Name):
        return node.id == ROOT_NAME or node.id in aliases
    if isinstance(node, ast.Attribute):
        if node.attr == ROOT_NAME:
            return True
        # self.x and cls.x: an attribute bound in a method, or a class attribute.
        if (isinstance(node.value, ast.Name) and node.value.id in ("self", "cls")
                and ("." + node.attr in aliases or node.attr in aliases)):
            return True
    if isinstance(node, ast.Call):
        name = _call_name(node)
        if isinstance(node.func, ast.Attribute) and name in ("resolve", "absolute"):
            return _is_root(node.func.value, aliases)
        if len(node.args) == 1 and name in PASS_THROUGH and _is_root(node.args[0], aliases):
            return True
    return _file_parents(node) == 2


def _text(node):
    """The value of a string constant, else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _components(text):
    return text.replace("\\", "/").split("/")


def decide(pieces):
    """Classify the path pieces joined after a root: "site", "other" or "unknown".

    Each piece is a string or None (not a constant). With every piece known and
    no climb above the root, the first component of the normalized path
    decides. Otherwise any known component that is an admitted name makes it
    "site"; failing that, a known first component (before the first unknown
    piece or climb above the root) makes it "other", and anything else is
    "unknown".
    """
    stack = []
    known = True
    first = None
    seen = []
    for piece in pieces:
        if piece is None:
            known = False
            continue
        for part in _components(piece):
            seen.append(part)
            if not known or part in ("", "."):
                continue
            if part == "..":
                if stack:
                    stack.pop()
                else:
                    known = False
            else:
                stack.append(part)
                first = first or part
    if known:
        if stack and (stack[0] in SITE_DIRS or (len(stack) == 1 and stack[0] in SITE_FILES)):
            return "site"
        return "other"
    if any(part in SITE_DIRS or part in SITE_FILES for part in seen):
        return "site"
    return "other" if first is not None else "unknown"


def _joined(node, aliases):
    """The piece nodes (or template strings) an expression joins after a root, or None."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        operands = []
        left = node
        while isinstance(left, ast.BinOp) and isinstance(left.op, ast.Div):
            operands.append(left.right)
            left = left.left
        return list(reversed(operands)) if _is_root(left, aliases) else None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return [node.right] if _is_root(node.left, aliases) else None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
        template = _text(node.left)
        first = node.right
        if isinstance(first, ast.Tuple):
            first = first.elts[0] if first.elts else None
        if template is not None and template.startswith("%s") and first is not None \
                and _is_root(first, aliases):
            return [template[2:]]
        return None
    if isinstance(node, ast.JoinedStr):
        values = node.values
        if values and isinstance(values[0], ast.FormattedValue) \
                and _is_root(values[0].value, aliases):
            return list(values[1:])
        return None
    if isinstance(node, ast.Call):
        name = _call_name(node)
        if isinstance(node.func, ast.Attribute) and name == "joinpath" \
                and _is_root(node.func.value, aliases):
            return list(node.args)
        if isinstance(node.func, ast.Attribute) and name == "format" \
                and node.args and _is_root(node.args[0], aliases):
            template = _text(node.func.value)
            for opener in ("{}", "{0}"):
                if template is not None and template.startswith(opener):
                    return [template[len(opener):]]
            return None
        if name in ("join", "Path", "PurePath", "PosixPath") and len(node.args) > 1 \
                and _is_root(node.args[0], aliases):
            return list(node.args[1:])
    return None


def _piece_text(piece):
    if isinstance(piece, str):
        return piece
    if isinstance(piece, ast.FormattedValue):
        return None
    return _text(piece)


def _assigned(body):
    """(target, value) for each simple assignment directly in a statement list.

    A target is a name, or ".attr" for a self/cls attribute.
    """
    for stmt in body:
        if isinstance(stmt, ast.Assign):
            targets, value = stmt.targets, stmt.value
        elif isinstance(stmt, ast.AnnAssign) and stmt.value is not None:
            targets, value = [stmt.target], stmt.value
        else:
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                yield target.id, value
            elif (isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name)
                    and target.value.id in ("self", "cls")):
                yield "." + target.attr, value


def _statements(body):
    """Every statement in a list, nested blocks included, not nested functions or classes."""
    stack = list(body)
    while stack:
        stmt = stack.pop()
        yield stmt
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        for field in ("body", "orelse", "finalbody", "handlers", "cases"):
            stack.extend(getattr(stmt, field, None) or [])


def _aliases(body, inherited):
    """``inherited`` plus the names a statement list binds to the repository root."""
    aliases = set(inherited)
    pairs = list(_assigned(body))
    changed = True
    while changed:
        changed = False
        for target, value in pairs:
            if target not in aliases and _is_root(value, aliases):
                aliases.add(target)
                changed = True
    return frozenset(aliases)


def _params(func):
    args = func.args
    names = [a.arg for a in args.posonlyargs + args.args + args.kwonlyargs]
    names += [a.arg for a in (args.vararg, args.kwarg) if a is not None]
    return frozenset(names)


def _mentions_site(node):
    """True when any string constant under ``node``, read as a path from the
    repository root, names an admitted path (``.web``, ``.web/x``, ``README.md``).

    A constant in a later place of a ``/`` chain (the ``"README.md"`` of
    ``x / "tests" / "README.md"``) is a path below another component, not one
    from the root, so it does not count.
    """
    nodes = list(ast.walk(node))
    inner = {id(child.right) for child in nodes
             if isinstance(child, ast.BinOp) and isinstance(child.op, ast.Div)
             and isinstance(child.left, ast.BinOp) and isinstance(child.left.op, ast.Div)}
    return any(decide([text]) == "site" for child in nodes
               if id(child) not in inner and (text := _text(child)) is not None)


def _class_aliases(cls, aliases):
    """The root names inside a class: its own assignments, and self/cls
    attributes bound to the root in any of its methods."""
    body = list(cls.body)
    for stmt in cls.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body.extend(inner for inner in _statements(stmt.body)
                        if any(target.startswith(".") for target, _ in _assigned([inner])))
    return _aliases(body, aliases)


class _Scan:
    """One unit (a function, a method or another class or module statement):
    does it read an admitted path, and which path sinks does it define."""

    def __init__(self, sinks):
        self.sinks = sinks
        self.direct = False
        self.uncertain = False
        self.new_sinks = set()

    def unit(self, node, aliases):
        self._walk(node, aliases, None)

    def _walk(self, node, aliases, func):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            inner = _aliases(list(_statements(node.body)), aliases)
            for child in ast.iter_child_nodes(node):
                self._walk(child, inner, node)
            return
        if isinstance(node, ast.ClassDef):
            inner = _class_aliases(node, aliases)
            for child in ast.iter_child_nodes(node):
                self._walk(child, inner, None)
            return
        self._check(node, aliases, func)
        for child in ast.iter_child_nodes(node):
            self._walk(child, aliases, func)

    def _check(self, node, aliases, func):
        if not isinstance(node, (ast.BinOp, ast.JoinedStr, ast.Call)):
            return
        params = _params(func) if func is not None else frozenset()
        pieces = _joined(node, aliases)
        if pieces is not None:
            verdict = decide([_piece_text(piece) for piece in pieces])
            if verdict == "site":
                self.direct = True
            elif verdict == "unknown":
                unknown = [piece for piece in pieces if _piece_text(piece) is None]
                if unknown and all(isinstance(piece, ast.Name) and piece.id in params
                                   for piece in unknown):
                    self.new_sinks.add(func.name)
                else:
                    self.uncertain = True
        if isinstance(node, ast.Call):
            name = _call_name(node)
            if name in LOADERS or name in self.sinks:
                values = list(node.args) + [kw.value for kw in node.keywords]
                for value in values:
                    text = _text(value)
                    if text is not None and decide([text]) == "site":
                        self.direct = True
                    if isinstance(value, ast.Name) and value.id in params:
                        self.new_sinks.add(func.name)


def _base_names(cls):
    for base in cls.bases:
        if isinstance(base, ast.Name):
            yield base.id
        elif isinstance(base, ast.Attribute):
            yield base.attr


def selected_classes(source, filename="<test module>"):
    """(flagged, test_cases) for one test module's source.

    ``flagged`` is every top-level class that reads an admitted path by the rules
    in the module docstring; ``test_cases`` is the subset that are
    unittest.TestCase subclasses by their base chain in this source. Raises
    SyntaxError when the source does not parse.
    """
    tree = ast.parse(source, filename=filename)
    lines = source.splitlines()

    def text_of(node):
        first = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
        return "\n".join(lines[first - 1:node.end_lineno])

    def words(names):
        names = sorted(n for n in names if n)
        return re.compile(r"\b(?:%s)\b" % "|".join(map(re.escape, names))) if names else None

    module_aliases = _aliases(tree.body, frozenset())
    roots = words({ROOT_NAME, "__file__"} | set(module_aliases))
    entries = []
    units = []
    for stmt in tree.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            key = stmt.name
        else:
            names = [target for target, _ in _assigned([stmt]) if not target.startswith(".")]
            if not names:
                continue
            key = names[0]
        text = text_of(stmt)
        entries.append((key, stmt, text))
        if isinstance(stmt, ast.ClassDef):
            # A class with no root word binds no root name of its own. Its own
            # root names (self.repo is the word "repo") also mark its units.
            scope = _class_aliases(stmt, module_aliases) if roots.search(text) else module_aliases
            own = words({alias.lstrip(".") for alias in scope - module_aliases})
            parts = stmt.decorator_list + stmt.bases + [kw.value for kw in stmt.keywords] + stmt.body
            units.extend((key, part, scope, text_of(part), own) for part in parts)
        else:
            units.append((key, stmt, module_aliases, text, None))

    # A unit none of these words appears in has no root join and no sink call,
    # so it is not scanned; units naming a newly found sink are scanned again.
    sinks = set()
    direct = set()
    uncertain = set()
    trigger = words({ROOT_NAME, "__file__"} | set(module_aliases) | LOADERS)
    first_pass = True
    while trigger is not None:
        found = set()
        for key, node, scope, text, own in units:
            if not (trigger.search(text) or (first_pass and own and own.search(text))):
                continue
            scan = _Scan(frozenset(sinks))
            scan.unit(node, scope)
            found |= scan.new_sinks
            if scan.direct:
                direct.add(key)
            if scan.uncertain:
                uncertain.add(key)
        found -= sinks | LOADERS
        sinks |= found
        trigger = words(found)
        first_pass = False
    statements = {key: stmt for key, stmt, _ in entries}
    reading = direct | {key for key in uncertain if _mentions_site(statements[key])}
    classes = {key: stmt for key, stmt in statements.items() if isinstance(stmt, ast.ClassDef)}
    while True:
        pattern = words(reading)
        grown = {key for key, stmt, text in entries
                 if key not in reading and pattern is not None and pattern.search(text)}
        if not grown:
            break
        reading |= grown

    def is_test_case(name, seen=()):
        cls = classes.get(name)
        if cls is None or name in seen:
            return False
        return any(base == "TestCase" or is_test_case(base, seen + (name,))
                   for base in _base_names(cls))

    flagged = sorted(name for name in reading if name in classes)
    return flagged, [name for name in flagged if is_test_case(name)]


def site_reading_test_ids(repo_root=REPO_ROOT):
    """``tests.<module>.<Class>`` for every selected class, module by module."""
    ids = []
    for path in sorted((repo_root / "tests").glob("test_*.py")):
        if path.stem in RUN_WHOLE:
            continue
        _flagged, test_cases = selected_classes(path.read_text(encoding="utf-8"), str(path))
        ids.extend(f"tests.{path.stem}.{name}" for name in test_cases)
    return ids


def main(argv):
    if argv[1:2] == ["--run"] and len(argv) > 2:
        ids = argv[2:]
        if not all(TEST_ID.fullmatch(test_id) for test_id in ids):
            print("site_reading_tests.py: --run takes tests.<module>.<Class> ids only",
                  file=sys.stderr)
            return 2
        # The script's own directory (tests/) heads sys.path; the ids import
        # through the tests package, and run from the repository root, as
        # gate 36 imports and runs them.
        sys.path.insert(0, str(REPO_ROOT))
        os.chdir(REPO_ROOT)
        program = unittest.main(module=None, argv=["unittest", *ids], exit=False)
        return 0 if program.result.wasSuccessful() else 1
    if argv[1:] != ["--list"]:
        print("usage: site_reading_tests.py --list | --run ID...", file=sys.stderr)
        return 2
    try:
        ids = site_reading_test_ids()
    except (OSError, UnicodeError, SyntaxError, ValueError) as exc:
        print(f"site_reading_tests.py: cannot scan the test files: {exc}", file=sys.stderr)
        return 2
    if not ids:
        print("site_reading_tests.py: no test class reads an admitted path", file=sys.stderr)
        return 2
    print("\n".join(ids))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
