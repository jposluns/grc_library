"""Release-delta fixtures use temporary git repositories and no third-party code."""
from __future__ import annotations

import ast
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tokenize
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / "src" / "tools"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DELTA = _load("pack_release_delta")
COMPILER = _load("corpus_mgmt_compiler")
MANIFEST = """schema_version = 1
[pack]
version = "1.2.3"
state = "active"
[registers]
clauses = "core/clauses.toml"
id_history = "core/id-history.toml"
ownership = "core/ownership.toml"
gates = "core/gates.toml"
profiles = "core/profiles.toml"
hooks = "core/hooks.toml"
[generation]
ruleset = "gensrc.toml"
[reference_registers]
defaults_root = "defaults"
[release]
waivers = "core/release-waivers.toml"
"""
ENGINE = """KNOWN_KEYS = {"first", "second"}

class Widget:
    def __init__(self, left, right):
        self.left = left

def public(left, right, *, enabled=True):
    gate_keys = {"id", "title"}
    return left

def configure(ref, *, debug=False):
    value = ref.first
    other = getattr(ref, "second", None)
    return value

def _private():
    return 1
"""
REGISTERS = {
    "clauses": ('clauses', 'id', 'alpha',
                'title = "Alpha"\nsource = "core/policies/note.md"\n'),
    "id-history": ('events', 'id', 'alpha', 'event = "created"\n'),
    "ownership": ('owned_targets', 'rule', 'alpha', 'target = "out.md"\nkind = "file"\n'),
    "gates": ('gates', 'id', 'lint-alpha', 'title = "Alpha"\nsource = "tools/engine.py"\n'),
    "profiles": ('profiles', 'id', 'words', 'target = "defaults/words.toml"\ntitle = "Words"\n'),
    "hooks": ('hooks', 'id', 'check-alpha', 'title = "Alpha"\n'),
}


class _Repo:
    def __init__(self, root, version="1.2.3"):
        self.root = root
        # The pack root the compiler reads by default (no --pack-root).
        self.pack = root / COMPILER.PACK_DIR
        # Drop every inherited GIT_* variable (a caller's GIT_INDEX_FILE or
        # GIT_DIR would redirect this fixture's git commands outside its
        # temporary directory), as .claude/skills/corpus-management/tests/test_linters.py's
        # fixture_git_environment() does.
        self.env = {k: v for k, v in os.environ.items()
                    if not k.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Release Test")
        self.git("config", "user.email", "release@example.invalid")
        self.write("core/manifest.toml", MANIFEST.replace("1.2.3", version))
        for name, (collection, field, identity, extra) in REGISTERS.items():
            self.write(f"core/{name}.toml",
                       f'schema_version = 1\n[[{collection}]]\n'
                       f'{field} = "{identity}"\n{extra}')
        self.write("defaults/words.toml", 'schema_version = 1\n[words]\nterms = ["alpha"]\n')
        self.write("gensrc.toml", 'schema_version = 1\nsources = ["core/policies/note.md"]\n')
        self.write("core/policies/note.md", "Pack policy.\n")
        self.write("core/rules/alpha.md", "A clause.\n")
        self.write("tools/engine.py", ENGINE)
        self.write("README.md", "Pack readme.\n")
        self.checkpoint()

    def git(self, *args):
        result = subprocess.run(
            ["git", "-C", str(self.root), *args],
            env=self.env, text=True, capture_output=True, check=True,
        )
        return result.stdout.strip()

    def checkpoint(self):
        self.git("add", ".")
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        self.base = self.git("rev-parse", "HEAD")
        self.git("update-ref", "refs/remotes/origin/main", self.base)

    def write(self, rel, text):
        path = self.pack / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def read(self, rel):
        return (self.pack / rel).read_text(encoding="utf-8")

    def replace(self, rel, old, new):
        text = self.read(rel)
        if old not in text:
            raise AssertionError(f"{rel}: missing replacement {old!r}")
        self.write(rel, text.replace(old, new))

    def remove(self, rel):
        (self.pack / rel).unlink()

    def version(self, value):
        data = DELTA.tomllib.loads(self.read("core/manifest.toml"))
        self.replace("core/manifest.toml", f'version = "{data["pack"]["version"]}"',
                     f'version = "{value}"')

    def waiver(self, required="MINOR", before="1.2.3", after="1.2.4"):
        self.write("core/release-waivers.toml", f"""schema_version = 1
[[waiver]]
from = "{before}"
to = "{after}"
required = "{required}"
reason = "Approved fixture re-baseline."
approved_by = "maintainer"
approved = 2026-09-26
decision_ref = "fixture decision"
""")


# The module-level binding forms the documentation sends readers to the release-level table
# (_RELEASE_CASES) for, and the two subjects whose level differs: a key-named name, whose
# declarations hold accepted keys, and a counted public name. _binding_form_pairs() derives
# every change between them (a binding added, removed or renamed, and a name moved from one
# form to another) as (change, base source, head source).
_BINDING_FORMS = (
    ("an assignment", "{name} = {value}\n"),
    ("an assignment expression", "_value = ({name} := {value})\n"),
    ("an annotation without a value", "{name}: int\n"),
    ("an import alias", "from os import sep as {name}\n"),
    ("a binding only inside a top-level if", "if True:\n    {name} = {value}\n"),
    ("a lambda body", "_value = lambda: ({name} := {value})\n"),
)
_BINDING_SUBJECTS = (
    ("*_keys name", "profile_keys", "other_keys", "{'a'}"),
    ("counted public name", "LIMIT", "BOUND", "3"),
)


def _binding_form_pairs():
    pairs = []
    for subject, name, other, value in _BINDING_SUBJECTS:
        sources = [(form, text.format(name=name, value=value), text.format(name=other, value=value))
                   for form, text in _BINDING_FORMS]
        for form, source, renamed in sources:
            pairs.append((f"{subject} bound by {form} added", "", source))
            pairs.append((f"{subject} bound by {form} removed", source, ""))
            pairs.append((f"{subject} bound by {form} renamed", source, renamed))
        for form, source, _renamed in sources:
            for other_form, other_source, _other_renamed in sources:
                if other_form != form:
                    pairs.append((f"{subject} moved from {form} to {other_form}", source,
                                  other_source))
    return pairs


def _string_values(node):
    # Every string an expression of the walker can evaluate to: a constant, either branch of a
    # conditional expression, or a concatenation of two such strings. A name or call gives none.
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return {node.value}
    if isinstance(node, ast.IfExp):
        return _string_values(node.body) | _string_values(node.orelse)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return {left + right for left in _string_values(node.left)
                for right in _string_values(node.right)}
    return set()


def _isinstance_types(test):
    # The ast class names of an isinstance(x, ast.T) or isinstance(x, (ast.T, ...)) test,
    # negated or not.
    if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
        return _isinstance_types(test.operand)
    if (isinstance(test, ast.Call) and isinstance(test.func, ast.Name)
            and test.func.id == "isinstance" and len(test.args) == 2):
        kinds = test.args[1]
        return tuple(kind.attr for kind in (kinds.elts if isinstance(kinds, ast.Tuple) else [kinds])
                     if isinstance(kind, ast.Attribute))
    return ()


def _walker_requirements():
    # Reads the walker (the visit function inside _accepted_sets) from the module source, so a
    # construct added to the walker is required here without being typed by hand. Returns:
    # the constructs refused for a key-owning name that is not key-named (every string passed
    # to body_bound, and every named construct the loop over named sends to body_bound); the
    # constructs refused for a key-named name only (every string passed to unread, and the
    # named constructs of the branch the loop sends to unread instead); for each node type of
    # a named branch, the constructs that branch names; and for each (statement types, target
    # type) the unpacking check reads, the construct it names.
    module = ast.parse((TOOLS / "pack_release_delta.py").read_text(encoding="utf-8"))
    walker = next(node for node in module.body
                  if isinstance(node, ast.FunctionDef) and node.name == "_accepted_sets")
    visit = next(node for node in walker.body
                 if isinstance(node, ast.FunctionDef) and node.name == "visit")

    def calls(tree, function):
        return [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name) and node.func.id == function]

    def chain(variable):
        # The longest if/elif chain whose branches each assign variable, as (types, value).
        found = []
        for node in ast.walk(visit):
            branches = []
            while (isinstance(node, ast.If) and node.body and isinstance(node.body[0], ast.Assign)
                   and [target.id for target in node.body[0].targets
                        if isinstance(target, ast.Name)] == [variable]):
                branches.append((_isinstance_types(node.test), node.body[0].value))
                node = node.orelse[0] if len(node.orelse) == 1 else None
            if len(branches) > len(found):
                found = branches
        return found

    def loop(variable):
        return next(node for node in ast.walk(visit) if isinstance(node, ast.For)
                    and isinstance(node.iter, ast.Name) and node.iter.id == variable)

    over_refused, key_named_only = set(), set()
    for call in calls(visit, "body_bound"):
        over_refused |= _string_values(call.args[2])
    for call in calls(visit, "unread"):
        key_named_only |= _string_values(call.args[1])
    named_loop = loop("named")
    suffix = {value for call in calls(named_loop, "body_bound")
              if isinstance(call.args[2], ast.BinOp)
              for value in _string_values(call.args[2].right)}
    routed = [node for node in ast.walk(named_loop) if isinstance(node, ast.If)
              and isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not)
              and calls(ast.Module(body=node.body, type_ignores=[]), "body_bound")]
    assert len(suffix) == 1 and len(routed) == 1, (suffix, routed)
    suffix = suffix.pop()
    key_named_types = set(_isinstance_types(routed[0].test))
    nodes = {}
    named = chain("named")
    assert named
    for types, value in named:
        elements = (value.elts if isinstance(value, ast.List)
                    else [value.elt] if isinstance(value, ast.ListComp) else [])
        constructs = {text + suffix for element in elements if isinstance(element, ast.Tuple)
                      for text in _string_values(element.elts[1])}
        (key_named_only if key_named_types & set(types) else over_refused).update(constructs)
        for type_name in types:
            nodes.setdefault(type_name, set()).update(constructs)
    unpacking_loop = loop("unpacking")
    test = next(node.test for node in ast.walk(unpacking_loop) if isinstance(node, ast.If))
    construct = {value for call in calls(unpacking_loop, "body_bound")
                 for value in _string_values(call.args[2])}
    assert len(construct) == 1, construct
    construct = construct.pop()
    targets = {}
    unpacking = chain("unpacking")
    assert unpacking
    for types, value in unpacking:
        if isinstance(value, ast.List) and not value.elts:
            continue
        # Each statement type of a branch is required apart (a for and an async for, a with and
        # an async with), with each target type apart, so one form never stands for another.
        for type_name in types:
            for target_type in _isinstance_types(test):
                targets[((type_name,), target_type)] = construct
    # A named branch that names each target of its statement apart through a conditional
    # expression on the target's type (a del names a plain name as one construct and a name
    # inside a tuple or list target as another) is required for each target type the grammar
    # allows for that statement, with the construct the expression gives that type. A branch
    # for a node that a statement holds in its handlers (an except name) is required for each
    # statement type that has handlers (a try and a try with except* clauses) apart.
    statement_forms = {"Delete": "del {}"}
    shapes = {"Name": "a", "Tuple": "(a, b)", "List": "[a, b]", "Starred": "*a"}
    handler_statements = sorted(
        name for name in dir(ast) if isinstance(getattr(ast, name), type)
        and issubclass(getattr(ast, name), ast.stmt) and "handlers" in getattr(ast, name)._fields)
    for types, value in named:
        if (isinstance(value, ast.ListComp) and isinstance(value.elt, ast.Tuple)
                and isinstance(value.elt.elts[1], ast.IfExp)
                and any(isinstance(generator.iter, ast.Attribute)
                        and generator.iter.attr == "targets" for generator in value.generators)):
            choice = value.elt.elts[1]
            tested = set(_isinstance_types(choice.test))
            assert tested, ast.unparse(choice)
            for type_name in types:
                for target_type, shape in shapes.items():
                    try:
                        tree = ast.parse(statement_forms[type_name].format(shape))
                    except SyntaxError:
                        continue
                    if not any(isinstance(target, getattr(ast, target_type))
                               for top in tree.body for target in _statement_targets(top)):
                        continue
                    texts = _string_values(choice.body if target_type in tested
                                           else choice.orelse)
                    assert len(texts) == 1, texts
                    targets[((type_name,), target_type)] = texts.pop() + suffix
        for type_name in [name for name in types
                          if issubclass(getattr(ast, name), ast.excepthandler)]:
            assert len(nodes[type_name]) == 1, nodes[type_name]
            for statement in handler_statements:
                targets[((statement,), type_name)] = next(iter(nodes[type_name]))
    assert over_refused and key_named_only and nodes and targets
    return over_refused, key_named_only, nodes, targets


def _event_requirements():
    # Reads _binding_events (the walker of a top-level statement) and every function inside it
    # that passes a construct to add or target from the module source, so a construct added
    # there is required here without being typed by hand. Each string expression is evaluated
    # to every (text, conditions) it can take, a condition being the source of an if test or
    # conditional expression test with its truth value, and a name read through its
    # assignments in the same function (or, for a parameter, through every call that passes
    # it); texts whose conditions contradict each other are dropped. Returns a map from
    # (statement type, target type) to the constructs a refusing row must name: for a call in
    # a branch of the statement function, each statement type of that branch apart (with the
    # isinstance conditions decided for that type), and for a call to target each target type
    # apart (Name, Tuple, List and Starred; an unpacking target adds the unpacking suffix and is
    # read as unread), with None as the statement type for a call outside the statement
    # function and None as the target type for a call to add. A construct whose kind is
    # "certain" is a release the check reads, so it is not required; an add whose name is None
    # marks a node type the check does not know, so it is not required either. A target type
    # the grammar does not allow for a statement (ast.parse refuses the form) is not required.
    module = ast.parse((TOOLS / "pack_release_delta.py").read_text(encoding="utf-8"))
    walker = next(node for node in module.body
                  if isinstance(node, ast.FunctionDef) and node.name == "_binding_events")
    functions = {node.name: node for node in walker.body if isinstance(node, ast.FunctionDef)}
    owner = {}
    for function in (*functions.values(), walker):
        for node in ast.walk(function):
            owner.setdefault(id(node), function)

    def conditions(function):
        # Each node of the function with the conditions of the if statements around it.
        found = {}

        def walk(body, held):
            for node in body:
                if isinstance(node, ast.If):
                    key = test_key(node.test, function)
                    walk(node.body, held | {(key, True)})
                    walk(node.orelse, held | {(key, False)})
                else:
                    for field in ("body", "orelse", "finalbody", "handlers"):
                        inner = getattr(node, field, None)
                        if isinstance(inner, list) and inner:
                            walk(inner, held)
                for part in ast.walk(node):
                    found.setdefault(id(part), held)
        walk(function.body, frozenset())
        return found

    def consistent(items):
        return not any((key, not truth) in items for key, truth in items)

    def test_key(test, function):
        # A name assigned once in the function to an expression stands for that expression.
        if isinstance(test, ast.Name):
            values = [node.value for node in ast.walk(function) if isinstance(node, ast.Assign)
                      and [t.id for t in node.targets if isinstance(t, ast.Name)] == [test.id]]
            if len(values) == 1:
                return ast.unparse(values[0])
        return ast.unparse(test)

    guards = {}
    for function in (*functions.values(), walker):
        for key, value in conditions(function).items():
            if owner.get(key) is function:
                guards[key] = value

    def callers(function_name, index, keyword):
        found = []
        for node in ast.walk(walker):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == function_name):
                if len(node.args) > index:
                    found.append(node.args[index])
                found.extend(k.value for k in node.keywords if k.arg == keyword)
        return found

    def values(node, function, seen=frozenset()):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return {(node.value, frozenset())}
        if isinstance(node, ast.IfExp):
            key = test_key(node.test, function)
            return ({(text, held | {(key, True)}) for text, held in values(node.body, function, seen)
                     if consistent(held | {(key, True)})}
                    | {(text, held | {(key, False)}) for text, held in values(node.orelse, function, seen)
                       if consistent(held | {(key, False)})})
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return {(left + right, a | b) for left, a in values(node.left, function, seen)
                    for right, b in values(node.right, function, seen) if consistent(a | b)}
        if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
            found = set()
            for operand in node.values:
                found |= {(text, held) for text, held in values(operand, function, seen) if text}
            return found
        if isinstance(node, ast.JoinedStr):
            found = {("", frozenset())}
            for part in node.values:
                part = part.value if isinstance(part, ast.FormattedValue) else part
                found = {(left + right, a | b) for left, a in found
                         for right, b in values(part, function, seen) if consistent(a | b)}
            return found
        if isinstance(node, ast.Name) and (function.name, node.id) not in seen:
            seen = seen | {(function.name, node.id)}
            found = set()
            for scope in (function, walker):
                assigns = [part for part in ast.walk(scope) if isinstance(part, ast.Assign)
                           and owner.get(id(part)) is scope
                           and [t.id for t in part.targets if isinstance(t, ast.Name)] == [node.id]]
                for part in assigns:
                    found |= {(text, held_ | guards.get(id(part), frozenset()))
                              for text, held_ in values(part.value, scope, seen)
                              if consistent(held_ | guards.get(id(part), frozenset()))}
                if assigns:
                    return found
                parameters = [arg.arg for arg in scope.args.args] if scope is not walker else []
                if node.id in parameters:
                    index = parameters.index(node.id)
                    for argument in callers(scope.name, index, node.id):
                        found |= {(text, a | {(node.id, bool(text))}) for text, a
                                  in values(argument, owner.get(id(argument), walker), seen)
                                  if consistent(a | {(node.id, bool(text))})}
                    return found
            return found
        return set()

    statement = functions["statement"]
    branches = []
    node = next(part for part in statement.body if isinstance(part, ast.If))
    while isinstance(node, ast.If):
        branches.append((_isinstance_types(node.test), node))
        node = node.orelse[0] if len(node.orelse) == 1 else None

    def branch_of(call):
        for types, branch in branches:
            if any(part is call for body in branch.body for part in ast.walk(body)):
                return types
        return (None,)

    def decided(held, type_name):
        # Drop texts whose isinstance conditions contradict the statement type.
        if type_name is None:
            return True
        kind = getattr(ast, type_name)
        for key, truth in held:
            test = ast.parse(key, mode="eval").body
            types = _isinstance_types(test)
            if types and isinstance(test, ast.Call) and test.args[0].id == "child":
                if issubclass(kind, tuple(getattr(ast, name) for name in types)) != truth:
                    return False
        return True

    forms = {"Assign": "{} = x", "AugAssign": "{} += x", "AnnAssign": "{}: int = x",
             "Delete": "del {}", "For": "for {} in x: pass",
             "AsyncFor": "async for {} in x: pass", "With": "with x as {}: pass",
             "AsyncWith": "async with x as {}: pass", "TypeAlias": "type {} = int"}
    shapes = {"Name": "a", "Tuple": "(a, b)", "List": "[a, b]", "Starred": "*a"}

    def allowed(type_name, target_type):
        try:
            tree = ast.parse(forms[type_name].format(shapes[target_type]))
        except SyntaxError:
            return False
        return any(isinstance(node, getattr(ast, target_type))
                   for top in tree.body for node in _statement_targets(top) + [getattr(top, "name", None)]
                   if node is not None)

    required = {}
    for function in functions.values():
        for call in ast.walk(function):
            if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                    and call.func.id in ("add", "target") and owner.get(id(call)) is function):
                continue
            if call.func.id == "add" and isinstance(call.args[0], ast.Constant) and call.args[0].value is None:
                continue
            if function.name == "target":
                # target passes its own construct, kind and suffix on unchanged; the calls
                # that give them are read where they are made.
                continue
            context = guards.get(id(call), frozenset())
            pairs = [(text, a | context) for text, a in values(call.args[1], function)
                     if consistent(a | context)]
            assert pairs, ast.unparse(call)
            kinds = values(call.args[2], function)
            types = branch_of(call) if function is statement else (None,)
            if call.func.id == "add":
                target_types = (None,)
            else:
                target_types = ("Name", "Tuple", "List", "Starred")
                suffixes = (values(call.args[4], function) if len(call.args) > 4
                            else values(ast.Name(id="unpacked"), walker))
            for type_name in types:
                for target_type in target_types:
                    if target_type and type_name and not allowed(type_name, target_type):
                        continue
                    for text, a in pairs:
                        if not decided(a, type_name):
                            continue
                        if target_type in (None, "Name"):
                            options = [(text, kind, a | b) for kind, b in kinds
                                       if consistent(a | b) and kind != "certain"]
                        else:
                            options = [((text + suffix if suffix and not text.endswith(suffix)
                                         else text), "unread", a | b)
                                       for suffix, b in suffixes if consistent(a | b)]
                        for construct, _kind, _held in options:
                            required.setdefault((type_name, target_type), set()).add(construct)
    assert required
    return required


def _refusal_names(message, construct):
    # Whether a refusal message names the construct as the place it refuses (the unread
    # refusal), as the form a release takes (the uncertain refusal) or as the uncertain release
    # of a key-named name that owns no declarations.
    return (f"is bound or deleted by {construct}, a place" in message
            or f": {construct}); the check" in message
            or f"is bound or deleted by {construct}, which the check reads as an uncertain"
               " release" in message)


# Constructs _binding_events names for a node ast.parse never builds, so no source can make a
# row for them: every stored or deleted ast.Name the parser builds is an assignment, for, with
# or del target (read by target) or a comprehension target (read by comprehension_target), never
# a name inside another expression. The walker keeps the branch so a hand-built tree still fails
# closed. test_binding_event_pairs_have_rows checks that each one is still derived, so a renamed
# construct cannot hide behind this list.
_PARSER_UNREACHABLE = frozenset({"a name stored or deleted in an expression"})


def _refused_name(message):
    # The name a refusal refuses, taken from where the message gives it: "<name>, a key-owning
    # name, is bound or deleted by" (the unread refusal; a name in a def or class body is given
    # with its scope, which is dropped), "the release of <name>, which owns accepted keys"
    # (the uncertain refusal) or "<name>, a key-named name that owns no accepted-key
    # declarations, is bound or deleted by" (the uncertain release of such a name). None for
    # any other message, which then names no name.
    found = re.search(r": (?:([A-Za-z_][\w.]*), a key-owning name, is bound or deleted by"
                      r"|the release of ([A-Za-z_][\w.]*), which owns accepted keys"
                      r"|([A-Za-z_][\w.]*), a key-named name that owns no accepted-key"
                      r" declarations, is bound or deleted by)", message)
    if not found:
        return None
    return (found.group(1) or found.group(2) or found.group(3)).rsplit(".", 1)[-1]


def _target_binds(target):
    # The names a target itself binds or deletes: an ast.Name in store or delete context, reached
    # only through tuple, list and starred elements. A name read inside a subscript, attribute
    # or call within the target, or bound by an assignment expression there, is not bound by
    # the target, so it never counts here.
    if isinstance(target, ast.Name):
        return {target.id} if isinstance(target.ctx, (ast.Store, ast.Del)) else set()
    if isinstance(target, (ast.Tuple, ast.List)):
        return set().union(*(_target_binds(element) for element in target.elts))
    if isinstance(target, ast.Starred):
        return _target_binds(target.value)
    return set()


def _holds(head, message, statement_type, target_type):
    # Whether the head holds a node of the statement type whose target of the target type (or,
    # for a target type of None, the node itself) binds or deletes the name the refusal names
    # (_refused_name), not merely some word that appears in the message.
    refused = _refused_name(message)
    named = {refused} if refused else set()
    for node in ast.walk(ast.parse(head)):
        if statement_type is not None and not isinstance(node, getattr(ast, statement_type)):
            continue
        if target_type is None:
            # A try statement binds its except names through its handlers.
            bound = set().union(*(_bound_by(part) for part in (node, *getattr(node, "handlers", ()))))
            if statement_type is None or bound & named:
                return True
            continue
        for target in [*_statement_targets(node), getattr(node, "name", None)]:
            if isinstance(target, getattr(ast, target_type)) and _target_binds(target) & named:
                return True
    return False


def _event_pairs_without_rows(requirements, refusals):
    # Each required (statement type, target type) pair and construct that no exit 2 row
    # covers: a row covers one when its head alone is refused with a message naming the
    # construct and the head holds a node of that statement type whose target of that type
    # binds or deletes the refused name (_holds).
    missing = []
    for (statement_type, target_type), constructs in sorted(
            requirements.items(), key=lambda item: (str(item[0][0]), str(item[0][1]))):
        for construct in sorted(constructs - _PARSER_UNREACHABLE):
            if not any(_refusal_names(message, construct)
                       and _holds(head, message, statement_type, target_type)
                       for _change, _place, _base, head, message in refusals):
                missing.append(f"{statement_type} / {target_type}: {construct}")
    return missing


def _table_refusals():
    # Every exit 2 row of the release-level table with the message its head alone raises
    # through _api (an empty message when the head is accepted alone).
    found = []
    for change, place, base, head, outcome in DELTA._RELEASE_CASES:
        if outcome != "exit 2":
            continue
        try:
            DELTA._api((ENGINE + "\n" + head).encode("utf-8"), "tools/engine.py")
        except ValueError as exc:
            message = str(exc)
        else:
            message = ""
        found.append((change, place, base, head, message))
    return found


_LEVEL = re.compile(r"(?<![A-Za-z])(PATCH|MINOR|MAJOR)(?![A-Za-z])|exit(s|ed)? \(?2(?![0-9])")
_GIVES_LEVEL = re.compile(r"(needs?|requires?|must have|gives?|counts?( only)? as|is|are)"
                          r"( at least)?( an?)? (PATCH|MINOR|MAJOR)"
                          r"|\((PATCH|MINOR|MAJOR|exit 2)")
_ENGINE_WORDS = re.compile(r"\b(names?|key|declarations?|def|class|function|assignment|import"
                           r"|del|parameters?|bindings?|module|engine|construct)\b")


def _sentences(text):
    return re.split(r"(?<=\.)\s+(?=[A-Z`*])", " ".join(text.split()))


# Text in src/README.md that states the exit status of another tool, not a release level:
# the compiler's stray scan (its --check and generation exits) and the gate 6 wrapper's
# classes of exit. Each must occur exactly once, and only that text is set aside.
_OTHER_EXIT_STATUSES = ("fail `--check` (exit 1) and generation (exit 2)",
                        "malformed data at the base exit 2")
# Text in the skill body that states the compiler's exit status when its surfaces disagree,
# not a release level; it too must occur exactly once, and only that text is set aside.
_SKILL_OTHER_EXIT_STATUSES = ("The compiler fail-closes (exit 2) on any disagreement among the"
                              " three surfaces.",)


def _comment_blocks(source):
    # Each run of comments on consecutive lines of a Python source, as (first line, text).
    blocks = []
    last = None
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type != tokenize.COMMENT:
            continue
        line = token.start[0]
        text = token.string[1:].strip()
        if blocks and last == line - 1:
            blocks[-1] = (blocks[-1][0], blocks[-1][1] + "\n" + text)
        else:
            blocks.append((line, text))
        last = line
    return blocks


def _docstrings(source):
    # The module docstring and every def and class docstring of a Python source.
    found = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None:
                found.append((getattr(node, "name", "module"), doc))
    return found


def _level_statements(module_source=None, readme=None, skill=None):
    # Release-level statements that are not where they belong. All of src/README.md (its
    # release history included), the skill body (src/core/skill/SKILL.md, the source of the
    # generated SKILL.md) and every comment and docstring of pack_release_delta.py
    # may give a level only in a pointer sentence, one that names the specification's
    # gate 99 rules and gives no construct a level; README text that states another tool's
    # exit status (_OTHER_EXIT_STATUSES) is set aside. In the specification's gate 99
    # paragraph, a sentence that gives a level for an engine construct names the rows of
    # _RELEASE_CASES, or the test, that exercise it, and does not say that the construct
    # counts as a level.
    if module_source is None:
        module_source = (TOOLS / "pack_release_delta.py").read_text(encoding="utf-8")
    if readme is None:
        readme = (TOOLS.parent / "README.md").read_text(encoding="utf-8")
    if skill is None:
        skill = (TOOLS.parent / "core" / "skill" / "SKILL.md").read_text(encoding="utf-8")
    spec = (TOOLS.parents[1] / "specs" / "specification-audit-programme.md"
            ).read_text(encoding="utf-8")
    paragraph = [line for line in spec.splitlines()
                 if line.startswith("Gate 99 runs ") and "--release-delta" in line]
    found = []
    # README is read paragraph by paragraph, and each heading and list item on its own, so a
    # sentence never runs across a heading or into the next release history entry.
    blocks = [" ".join(block.split()) for block in re.split(r"\n\s*\n|\n(?=#|- )", readme)]
    for other in _OTHER_EXIT_STATUSES:
        count = sum(block.count(other) for block in blocks)
        if count != 1:
            found.append(f"README: {count} occurrence(s) of {other!r}")
        blocks = [block.replace(other, "") for block in blocks]
    texts = [("README", block) for block in blocks if block]
    # The skill body is read the same way, block by block.
    skill_blocks = [" ".join(block.split()) for block in re.split(r"\n\s*\n|\n(?=#|- )", skill)]
    for other in _SKILL_OTHER_EXIT_STATUSES:
        count = sum(block.count(other) for block in skill_blocks)
        if count != 1:
            found.append(f"SKILL.md: {count} occurrence(s) of {other!r}")
        skill_blocks = [block.replace(other, "") for block in skill_blocks]
    texts += [("SKILL.md", block) for block in skill_blocks if block.strip()]
    texts += [(f"pack_release_delta.py comment at line {line}", block)
              for line, block in _comment_blocks(module_source)]
    texts += [(f"pack_release_delta.py docstring of {name}", doc)
              for name, doc in _docstrings(module_source)]
    for name, text in texts:
        for sentence in _sentences(text):
            if not _LEVEL.search(sentence):
                continue
            pointer = "specification-audit-programme.md" in sentence and "gate 99" in sentence
            if not pointer or _GIVES_LEVEL.search(sentence):
                found.append(f"{name}: {sentence[:160]}")
    if len(paragraph) != 1:
        found.append(f"specification: {len(paragraph)} gate 99 release-delta paragraph(s)")
    for sentence in _sentences("\n".join(paragraph)):
        if not _LEVEL.search(sentence) or not _ENGINE_WORDS.search(sentence):
            continue
        cited = "_RELEASE_CASES" in sentence or re.search(r"`test_\w+`", sentence)
        if not cited or re.search(r"counts?( only)? as (PATCH|MINOR|MAJOR)", sentence):
            found.append(f"specification: {sentence[:160]}")
    return found


_RULE_TITLE = "Accepted-key declaration and removal rules"
# Phrases of the accepted-key rule text. Each must be in the module docstring's rule section
# and in neither src/README.md nor the specification, so a restatement added there fails.
_RULE_MARKERS = ("only these places", "compared in five views", "binds a lambda local",
                 "must be bound exactly once", "a key-owning name is a name that owns",
                 "deliberate over-refusal for every construct above")


def _rule_section(module_source=None):
    # The rule section of the module docstring of pack_release_delta.py, read with
    # ast.get_docstring, as one line of text: everything after its titled heading, or ""
    # when the docstring holds no such heading.
    if module_source is None:
        module_source = (TOOLS / "pack_release_delta.py").read_text(encoding="utf-8")
    doc = ast.get_docstring(ast.parse(module_source), clean=False) or ""
    heading = _RULE_TITLE + "\n" + "=" * len(_RULE_TITLE) + "\n"
    if heading not in doc:
        return ""
    return " ".join(doc.partition(heading)[2].split())


def _accepted_key_rule_problems(readme=None, spec=None):
    # The module docstring of pack_release_delta.py, read with ast.get_docstring, holds the
    # accepted-key rule in one titled section; src/README.md and the specification each point
    # to that section by name and hold none of its phrases.
    source = (TOOLS / "pack_release_delta.py").read_text(encoding="utf-8")
    doc = ast.get_docstring(ast.parse(source), clean=False) or ""
    if readme is None:
        readme = (TOOLS.parent / "README.md").read_text(encoding="utf-8")
    if spec is None:
        spec = (TOOLS.parents[1] / "specs" / "specification-audit-programme.md"
                ).read_text(encoding="utf-8")
    found = []
    heading = _RULE_TITLE + "\n" + "=" * len(_RULE_TITLE) + "\n"
    if doc.count(heading) != 1:
        found.append(f"module docstring: {doc.count(heading)} section(s) titled {_RULE_TITLE!r}")
    section = " ".join(doc.partition(heading)[2].split()).lower()
    for marker in _RULE_MARKERS:
        if marker not in section:
            found.append(f"module docstring: the rule section lacks {marker!r}")
    documents = (("README", readme, "`tools/pack_release_delta.py`"),
                 ("specification", spec,
                  "`.claude/skills/corpus-management/src/tools/pack_release_delta.py`"))
    for name, text, path in documents:
        flat = " ".join(text.split())
        pointer = f'module docstring of {path}, section "{_RULE_TITLE}"'
        if flat.count(pointer) != 1:
            found.append(f"{name}: {flat.count(pointer)} pointer(s) to the rule section")
        for marker in _RULE_MARKERS:
            if marker in flat.lower():
                found.append(f"{name}: restates the accepted-key rule ({marker!r})")
    return found


def _bound_by(node):
    # The names a node itself binds or deletes: its own name (a def, class, except handler,
    # match capture, star capture or mapping rest), the names of an import alias, a global or
    # nonlocal statement or a type statement, and the stored or deleted ast.Name nodes of its
    # targets.
    names = set()
    for field in ("name", "rest", "asname"):
        value = getattr(node, field, None)
        if isinstance(value, str):
            names.add(value)
        elif isinstance(value, ast.Name):
            names.add(value.id)
    if isinstance(node, ast.alias) and node.asname is None:
        names.add(node.name.split(".")[0])
    names.update(getattr(node, "names", ()) if isinstance(node, (ast.Global, ast.Nonlocal))
                 else ())
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        for alias in node.names:
            names |= _bound_by(alias)
    for target in [*getattr(node, "targets", ()), getattr(node, "target", None),
                   *(item.optional_vars for item in getattr(node, "items", ()))]:
        if isinstance(target, ast.AST):
            names.update(sub.id for sub in ast.walk(target) if isinstance(sub, ast.Name)
                         and isinstance(sub.ctx, (ast.Store, ast.Del)))
    return names


def _statement_targets(node):
    # The targets of an assignment, for, async for, with or async with statement.
    return [*getattr(node, "targets", ()), getattr(node, "target", None),
            *(item.optional_vars for item in getattr(node, "items", ()))]


class ReleaseDeltaTests(unittest.TestCase):
    @contextlib.contextmanager
    def repo(self, version="1.2.3"):
        with tempfile.TemporaryDirectory(prefix="release-delta-") as directory:
            yield _Repo(Path(directory), version)

    def result(self, repo, base=None):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = DELTA.check(repo.root, repo.pack, base)
        return code, output.getvalue()

    def expect(self, repo, floor, code=1, claimed="NONE", base=None):
        actual, output = self.result(repo, base)
        self.assertEqual(actual, code, output)
        self.assertIn(f"FLOOR: {floor}", output)
        self.assertIn(f"CLAIMED: {claimed}", output)
        return output

    def test_no_change_and_explicit_base(self):
        with self.repo() as repo:
            self.expect(repo, "NONE", 0)
            self.expect(repo, "NONE", 0, base=repo.base)

    def test_pycache_is_the_only_exclusion(self):
        # The scope is every pack file except __pycache__, so no reference form and no README
        # (which a tree or block rule can consume) escapes it.
        with self.repo() as repo:
            repo.write("tools/__pycache__/engine.cpython-314.pyc", "bytes")
            self.expect(repo, "NONE", 0)
            repo.write("notes/README.md", "Changed.\n")
            self.assertIn("notes/README.md", self.expect(repo, "PATCH"))
            repo.write("notes/unreferenced.toml", "not even valid TOML")
            self.assertIn("notes/unreferenced.toml", self.expect(repo, "PATCH"))
            repo.write("notes/helper.py", "def run():\n    return 1\n")
            self.assertIn("notes/helper.py", self.expect(repo, "MINOR"))

    def test_patch_surfaces_need_a_bump(self):
        cases = [
            ("core/manifest.toml", 'state = "active"', 'state = "ready"'),
            ("core/policies/note.md", "Pack policy.", "Corrected policy."),
            ("gensrc.toml", "schema_version = 1", "# comment\nschema_version = 1"),
            ("core/clauses.toml", 'title = "Alpha"', 'title = "Corrected"'),
            ("core/gates.toml", 'title = "Alpha"', 'title = "Corrected"'),
            ("core/id-history.toml", 'event = "created"', 'event = "retired"'),
            ("core/ownership.toml", 'target = "out.md"', 'target = "other.md"'),
            ("core/hooks.toml", 'title = "Alpha"', 'title = "Corrected"'),
            ("tools/engine.py", "return 1", "return 2"),
        ]
        for path, old, new in cases:
            with self.subTest(path=path), self.repo() as repo:
                repo.replace(path, old, new)
                output = self.expect(repo, "PATCH")
                if path in ("core/clauses.toml", "core/gates.toml", "core/hooks.toml"):
                    self.assertIn("register value changed", output)
                repo.version("1.2.4")
                self.expect(repo, "PATCH", 0, "PATCH")

    def test_all_register_ids_added_removed_and_renamed(self):
        for name, (collection, field, identity, extra) in REGISTERS.items():
            for action, floor in (("add", "MINOR"), ("remove", "MAJOR"), ("rename", "MAJOR")):
                with self.subTest(register=name, action=action), self.repo() as repo:
                    path = f"core/{name}.toml"
                    if action == "add":
                        repo.write(path, repo.read(path) +
                                   f'\n[[{collection}]]\n{field} = "another"\n{extra}')
                    elif action == "remove":
                        repo.write(path, f"schema_version = 1\n{collection} = []\n")
                    else:
                        repo.replace(path, f'{field} = "{identity}"', f'{field} = "renamed"')
                    self.expect(repo, floor)

    def test_history_multiple_events_keep_one_identity(self):
        with self.repo() as repo:
            path = "core/id-history.toml"
            repo.write(path, repo.read(path) + '\n[[events]]\nid = "alpha"\nevent = "retired"\n')
            self.expect(repo, "PATCH")

    def test_table_keyed_register_and_manifest_union(self):
        with self.repo() as repo:
            repo.replace("core/manifest.toml", "[generation]",
                         'custom = "core/custom.toml"\n[generation]')
            repo.write("core/custom.toml", 'schema_version = 1\n[items.alpha]\nvalue = 1\n')
            repo.checkpoint()
            repo.replace("core/custom.toml", "[items.alpha]", "[items.beta]")
            self.expect(repo, "MAJOR")
        with self.repo() as repo:
            repo.replace("core/manifest.toml", 'hooks = "core/hooks.toml"\n', "")
            self.expect(repo, "MAJOR")
        with self.repo() as repo:
            repo.replace("core/manifest.toml", "[generation]",
                         'custom = "core/custom.toml"\n[generation]')
            repo.write("core/custom.toml", 'schema_version = 1\n[items.alpha]\nvalue = 1\n')
            self.expect(repo, "MINOR")

    def test_register_ambiguity_duplicate_and_missing_file(self):
        cases = [
            ("core/gates.toml", 'schema_version = 1\n[[gates]]\nname = "unknown"\n'),
            ("core/gates.toml", 'schema_version = 1\n[gates.alpha]\nid = "different"\n'),
            ("core/gates.toml", 'schema_version = 1\n[unexpected]\nvalue = 1\n'),
            ("core/gates.toml", 'schema_version = 1\n[[gates]]\nid = "x"\n[[gates]]\nid = "x"\n'),
        ]
        for path, content in cases:
            with self.subTest(content=content), self.repo() as repo:
                repo.write(path, content)
                self.assertEqual(self.result(repo)[0], 2)
        with self.repo() as repo:
            repo.remove("core/gates.toml")
            self.assertEqual(self.result(repo)[0], 2)

    def test_schema_versions(self):
        paths = ["core/manifest.toml", "defaults/words.toml"]
        paths += [f"core/{name}.toml" for name in REGISTERS]
        for path in paths:
            with self.subTest(path=path), self.repo() as repo:
                repo.replace(path, "schema_version = 1", "schema_version = 2")
                self.expect(repo, "MAJOR")

    def test_clause_add_remove_change(self):
        for action, floor in (("add", "MINOR"), ("remove", "MAJOR"), ("edit", "PATCH")):
            with self.subTest(action=action), self.repo() as repo:
                if action == "add":
                    repo.write("core/rules/new.md", "New clause.\n")
                elif action == "remove":
                    repo.remove("core/rules/alpha.md")
                else:
                    repo.write("core/rules/alpha.md", "Changed clause.\n")
                output = self.expect(repo, floor)
                if action == "edit":
                    self.assertIn("strengthening vs clarifying is not machine-decidable", output)

    def test_refactors_engine_scope_and_waiver_path(self):
        # Renaming a key-set variable or adding a private helper that assigns `keys` is not a
        # configuration change; an engine outside tools/ is classified; the manifest's declared
        # waiver path must be the supported one. Any edit to tools/engine.py is at least
        # PATCH, so the first case also requires that no accepted-key set line is emitted
        # and gives one private helper a literal key set (flips: key each declaration by
        # its own name instead of the module union, or read private scopes, even when a
        # non-literal value there is ignored; either adds an accepted-key line, MINOR or
        # MAJOR, or fails the read).
        with self.repo() as repo:
            repo.replace("tools/engine.py", "    gate_keys = ", "    allowed_gate_keys = ")
            repo.replace("tools/engine.py", "def _private():", "def _helper(d):\n    keys = sorted(d)\n    return keys\n\n"
                         "def _defaults():\n    keys = {\"internal\"}\n    return keys\n\ndef _private():")
            output = self.expect(repo, "PATCH")
            self.assertNotIn("accepted-key set", output)
        with self.repo() as repo:
            repo.write("engines/language.py", "def run():\n    return 1\n")
            repo.checkpoint()
            repo.replace("engines/language.py", "def run():", "def _run():")
            self.assertIn("removed run", self.expect(repo, "MAJOR"))
        with self.repo() as repo:
            repo.replace("tools/engine.py", "KNOWN_KEYS = {\"first\", \"second\"}", "KNOWN_KEYS = {\"first\"}")
            self.assertIn("removed second", self.expect(repo, "MAJOR"))
        with self.repo() as repo:
            repo.replace("core/manifest.toml", 'waivers = "core/release-waivers.toml"', 'waivers = "core/other.toml"')
            code, output = self.result(repo)
            self.assertEqual(code, 2, output)
            self.assertIn("[release].waivers must be", output)

    def test_policy_file_change_reported_as_pack_surface_patch(self):
        # A change to a pack file under core/policies is reported PATCH, with a pack
        # surface line naming the file by its pack-relative path.
        with self.repo() as repo:
            repo.replace("core/policies/note.md", "Pack policy.", "Changed policy.")
            output = self.expect(repo, "PATCH")
            self.assertIn("core/policies/note.md: pack surface changed", output)

    def test_engine_public_api_and_configuration(self):
        cases = [
            ("def public(", "def _public(", "MAJOR"),
            ("def _private(", "def added(", "MINOR"),
            ("public(left, right,", "public(left,", "MAJOR"),
            ("public(left, right,", "public(left, right, third,", "MINOR"),
            ("class Widget:", "class _Widget:", "MAJOR"),
            ("class Widget:", "class Extra:\n    pass\n\nclass Widget:", "MINOR"),
            ("__init__(self, left, right)", "__init__(self, left)", "MAJOR"),
            ("__init__(self, left, right)", "__init__(self, left, right, extra)", "MINOR"),
            ('{"first", "second"}', '{"first"}', "MAJOR"),
            ('{"first", "second"}', '{"first", "second", "third"}', "MINOR"),
            ('{"id", "title"}', '{"id"}', "MAJOR"),
            ('{"id", "title"}', '{"id", "title", "source"}', "MINOR"),
            ("configure(ref, *, debug=False)", "configure(ref)", "MAJOR"),
            ("configure(ref, *, debug=False)", "configure(ref, *, debug=False, flag=False)", "MINOR"),
            ("value = ref.first", "value = None", "MAJOR"),
            ("value = ref.first", "value = ref.first\n    extra = ref.third", "MINOR"),
            ('getattr(ref, "second", None)', "None", "MAJOR"),
        ]
        for old, new, floor in cases:
            with self.subTest(change=new), self.repo() as repo:
                repo.replace("tools/engine.py", old, new)
                self.expect(repo, floor)
        for old, new, floor in (
            ('ref["first"]', "None", "MAJOR"),
            ('ref["first"]', 'ref["first"] + ref.get("second", "")', "MINOR"),
        ):
            with self.subTest(change=new), self.repo() as repo:
                repo.write("tools/engine.py", 'def configure(ref):\n    return ref["first"]\n')
                repo.checkpoint()
                repo.replace("tools/engine.py", old, new)
                self.expect(repo, floor)

    def test_new_and_removed_engine_files(self):
        with self.repo() as repo:
            repo.write("tools/new.py", "def new():\n    return None\n")
            self.expect(repo, "MINOR")
        with self.repo() as repo:
            repo.remove("tools/engine.py")
            self.expect(repo, "MAJOR")
        with self.repo() as repo:
            repo.write("tools/private.py", "def _helper():\n    pass\n")
            self.expect(repo, "PATCH")

    def test_engine_input_errors(self):
        for content in ("def broken(", 'ACCEPTED_KEYS = compute_keys()\n'):
            with self.subTest(content=content), self.repo() as repo:
                repo.write("tools/engine.py", content)
                self.assertEqual(self.result(repo)[0], 2)

    def test_engine_public_module_assignments(self):
        # A public name bound by a top-level assignment is public surface: adding one needs a
        # MINOR; removing it (a top-level del included), renaming it to a private name or
        # changing its kind is breaking, and a kind change is reported without parameter
        # changes; any two bindings of one public name by def, class or assignment, at least
        # one of them a def or class, with no top-level del of that name between them, fail
        # closed, and a top-level del lets a later def, class or assignment bind the name
        # again. A private name, a binding inside a function or class, an annotation without a
        # value, an import alias, __all__ and a changed value stay PATCH (residuals the _api
        # docstring lists), but replacing a counted name with one of those unseen bindings
        # reads as a removal.
        added = [
            ("LIMIT = 3", "MINOR", ["added LIMIT"]),
            ('import re\nTOKEN_RE = re.compile("x")', "MINOR", ["added TOKEN_RE"]),
            ("LIMIT: int = 3", "MINOR", ["added LIMIT"]),
            ("LEFT, (RIGHT, *REST) = 1, (2, 3)", "MINOR",
             ["added LEFT", "added RIGHT", "added REST"]),
            ("[LEFT, RIGHT] = 1, 2", "MINOR", ["added LEFT", "added RIGHT"]),
            ("FIRST = SECOND = 1", "MINOR", ["added FIRST", "added SECOND"]),
            ("_LIMIT = 3", "PATCH", []),
            ("LIMIT: int", "PATCH", []),
            ("from re import compile as COMPILE", "PATCH", []),
            ('__all__ = ["public"]', "PATCH", []),
        ]
        for lines, floor, reports in added:
            with self.subTest(added=lines), self.repo() as repo:
                repo.replace("tools/engine.py", "class Widget:", f"{lines}\n\nclass Widget:")
                output = self.expect(repo, floor)
                for report in reports:
                    self.assertIn(report, output)
        for old, new in (
            ("    return left", "    limit = 3\n    return left"),
            ("class Widget:\n", "class Widget:\n    LIMIT = 3\n\n"),
        ):
            with self.subTest(local=new), self.repo() as repo:
                repo.replace("tools/engine.py", old, new)
                self.expect(repo, "PATCH")
        for new, floor, report in (
            ("", "MAJOR", "removed LIMIT"),
            ("_LIMIT = 3\n", "MAJOR", "removed LIMIT"),
            ("LIMIT = 4\n", "PATCH", None),
            ("def LIMIT():\n    return 3\n", "MAJOR", "public symbol kind changed LIMIT"),
            ("def LIMIT(first, second):\n    return first\n", "MAJOR",
             "public symbol kind changed LIMIT"),
            ("LIMIT = 3\ndel LIMIT\n", "MAJOR", "removed LIMIT"),
            ("LIMIT = 3\ndel LIMIT\nLIMIT = 4\n", "PATCH", None),
            ("LIMIT = 3\nif LIMIT:\n    del LIMIT\n", "PATCH", None),
            ("LIMIT: int\n", "MAJOR", "removed LIMIT"),
            ("from os import sep as LIMIT\n", "MAJOR", "removed LIMIT"),
        ):
            with self.subTest(base="LIMIT = 3", head=new), self.repo() as repo:
                repo.replace("tools/engine.py", "class Widget:", "LIMIT = 3\n\nclass Widget:")
                repo.checkpoint()
                repo.replace("tools/engine.py", "LIMIT = 3\n", new)
                output = self.expect(repo, floor)
                if report:
                    self.assertIn(report, output)
                self.assertNotIn("LIMIT parameter", output)
        with self.subTest(base="def LIMIT(first, second)", head="LIMIT = 3"), self.repo() as repo:
            function = "def LIMIT(first, second):\n    return first\n"
            repo.replace("tools/engine.py", "class Widget:", f"{function}\nclass Widget:")
            repo.checkpoint()
            repo.replace("tools/engine.py", function, "LIMIT = 3\n")
            output = self.expect(repo, "MAJOR")
            self.assertIn("public symbol kind changed LIMIT", output)
            self.assertNotIn("LIMIT parameter", output)
        with self.subTest(deleted="public"), self.repo() as repo:
            repo.write("tools/engine.py", repo.read("tools/engine.py") + "\ndel public\n")
            self.assertIn("removed public", self.expect(repo, "MAJOR"))
        with self.subTest(ambiguous="run"), self.repo() as repo:
            repo.write("tools/engine.py",
                       repo.read("tools/engine.py") + "\ndef run():\n    return 1\n\nrun = 1\n")
            code, output = self.result(repo)
            self.assertEqual(code, 2, output)
            self.assertIn("ambiguous public definition run", output)
        with self.subTest(ambiguous="run", deleted_after="run"), self.repo() as repo:
            # The def clashes with the assignment before it, so the check fails closed there
            # and never reaches the del after both bindings.
            repo.write("tools/engine.py", repo.read("tools/engine.py")
                       + "\nrun = 1\n\ndef run():\n    return 1\n\ndel run\n")
            code, output = self.result(repo)
            self.assertEqual(code, 2, output)
            self.assertIn("ambiguous public definition run", output)
        for lines in (
            "def run():\n    return 1\n\ndel other\n\ndef run():\n    return 2\n",
            "def run():\n    return 1\n\ndel other\nrun = 1\n",
            "run = 1\ndel other\n\ndef run():\n    return 1\n",
        ):
            # A del of a different name between two bindings ends neither of them, so they stay
            # ambiguous and fail closed.
            with self.subTest(ambiguous="run", deleted_between="other", head=lines), \
                    self.repo() as repo:
                repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + lines)
                code, output = self.result(repo)
                self.assertEqual(code, 2, output)
                self.assertIn("ambiguous public definition run", output)
        for base, head, floor, report in (
            ("LIMIT = 3\n", "LIMIT = 3\ndel LIMIT\n\ndef LIMIT():\n    return 3\n", "MAJOR",
             "public symbol kind changed LIMIT"),
            ("def run(first):\n    return first\n",
             "def run(first):\n    return first\n\ndel run\n\ndef run(first, second):\n"
             "    return first\n", "MINOR", "run parameter: added second"),
            ("def run(first):\n    return first\n",
             "def run(first):\n    return first\n\ndel run\nrun = 1\n", "MAJOR",
             "public symbol kind changed run"),
            ("class Gadget:\n    pass\n",
             "class Gadget:\n    pass\n\ndel Gadget\n\nclass Gadget:\n    pass\n", "PATCH",
             None),
        ):
            # A top-level del ends a binding, so a later def, class or assignment binds the
            # name again instead of failing closed as ambiguous.
            with self.subTest(base=base, head=head), self.repo() as repo:
                repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + base)
                repo.checkpoint()
                repo.replace("tools/engine.py", base, head)
                output = self.expect(repo, floor)
                if report:
                    self.assertIn(report, output)
        with self.subTest(renamed="KNOWN_KEYS"), self.repo() as repo:
            repo.replace("tools/engine.py", "KNOWN_KEYS = ", "ALLOWED_KEYS = ")
            self.assertIn("removed KNOWN_KEYS", self.expect(repo, "MAJOR"))

    def test_deleted_configure_drops_its_inputs(self):
        # A top-level del of configure drops its configure inputs with the name, so they are
        # reported as removed instead of staying in the compared configuration, and a configure
        # bound again by a later def is compared by that def's own inputs.
        restored = ("del configure\n\ndef configure(ref, *, debug=False):\n"
                    "    return ref.first, getattr(ref, \"second\", None)\n")
        for head, floor, reports in (
            ("del configure\n", "MAJOR",
             ["public symbol: removed configure",
              "configure input configure: removed ref.first",
              "configure input configure: removed ref.second",
              "configure input configure: removed keyword debug"]),
            ("del configure\nconfigure = None\n", "MAJOR",
             ["public symbol kind changed configure",
              "configure input configure: removed ref.first"]),
            (restored, "PATCH", []),
        ):
            with self.subTest(head=head), self.repo() as repo:
                repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + head)
                output = self.expect(repo, floor)
                for report in reports:
                    self.assertIn(report, output)
                if not reports:
                    self.assertNotIn("configure input", output)

    def test_deleted_binding_drops_its_accepted_keys(self):
        # A top-level del of a public def, or of a module-level key set, drops the accepted keys
        # declared in the deleted binding, so a del followed by a later binding of the name
        # cannot hide a removed key: the later binding counts only its own declarations. A del
        # of a class owner fails closed instead, since every class owner (a class bound by a
        # top-level statement) is shared (test_class_body_hand_off_fails_closed).
        load_a = "def load():\n    profile_keys = {'a'}\n"
        load_b = "def load():\n    profile_keys = {'b'}\n"
        set_a = "profile_keys = {'a'}\n"
        for base, head, floor, reports in (
            (load_a, load_a + "\ndel load\n\n" + load_b, "MAJOR",
             ["accepted-key set module: removed a", "accepted-key set module: added b"]),
            (load_a, load_a + "\ndel load\n", "MAJOR",
             ["public symbol: removed load", "accepted-key set module: removed a"]),
            (set_a, set_a + "del profile_keys\nprofile_keys = {'b'}\n", "MAJOR",
             ["accepted-key set module: removed a", "accepted-key set module: added b"]),
            (set_a, set_a + "del profile_keys\n", "MAJOR",
             ["public symbol: removed profile_keys", "accepted-key set module: removed a"]),
            (load_a, load_a + "\ndel load\n\n" + load_a, "PATCH", []),
            (load_a, load_a + "\ndel other\n", "PATCH", []),
        ):
            with self.subTest(base=base, head=head), self.repo() as repo:
                repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + base)
                repo.checkpoint()
                repo.replace("tools/engine.py", base, head)
                output = self.expect(repo, floor)
                for report in reports:
                    self.assertIn(report, output)
                if not reports:
                    self.assertNotIn("accepted-key set", output)

    def assert_release_fails_closed(self, repo, name):
        code, output = self.result(repo)
        self.assertEqual(code, 2, output)
        self.assertIn(
            f"ERROR: release-delta input: tools/engine.py: accepted keys of {name} may still be"
            " reachable after its release; the check cannot decide the floor", output)
        self.assertNotIn("FLOOR:", output)

    def test_referenced_key_owner_release_fails_closed(self):
        # A top-level statement that deletes or
        # rebinds a name owning accepted-key declarations fails closed (exit 2) when the module
        # refers to that name anywhere (a load in any scope and at any position, before or after
        # the release, in a function or class body, a container, a tuple or a default value) or
        # has a star import, since the keys may still be reachable after the release. The cases
        # cover alias, tuple, container, parameter and rebinding inputs, and each fails closed.
        base = "def load():\n    profile_keys = {'a'}\n"
        empty = "def load():\n    profile_keys = set()\n"
        tail = "del load\ndef load():\n    pass\n"
        cases = [(base, base + added + tail, "load") for added in (
            "loader = load\n",
            "class _C:\n    load += ()\n",
            "_loader = load\n",
            "_loader: object = load\n",
            "_loader = load\n_loader = None\n",
            "loader = load\nloader = None\n",
            "def _other():\n    pass\n_l = load\n_l = _other\n",
            "_loader = load\ndef _loader():\n    pass\n",
            "_loader = load\nimport os as _loader\n",
            "_loader = load\nfor _loader in ():\n    pass\n",
            "_loader = load\nwith open(__file__) as _loader:\n    pass\n",
            "_loader = load\ndel _loader\n",
            "_loader = load\nif load:\n    _loader = None\n",
            "_loader = load\ndef _reset():\n    global _loader\n    _loader = None\n",
            "_loader = load\nfrom os import *\n",
            "_first = _second = load\n_first = None\n",
            "_loader = load\n_loader = _loader\n",
            "loader, keeper = load\n",
            "loader, keeper = load, None\n",
            "[loader, keeper] = load\n",
            "_loader = load\ndef f(_loader):\n    pass\n",
            "_loader = load\ndef f():\n    _loader = 1\n",
            "def _r():\n    global load\n    load = None\n_r()\n_loader = load\n",
            "if True:\n    load = None\n_loader = load\n",
            "def f(load):\n    return load\n",
            "def f():\n    load = 1\n    return load\n",
            "HANDLERS = [load]\n",
            "def _get():\n    return load\n",
            "def _f(handler=load):\n    pass\n",
            "class _Holder:\n    handler = load\n",
            "from os import *\n",
        )]
        cases += [
            (base, base + tail + "def _get():\n    return load\n", "load"),
            (base, base + "del load\n_loader = load\n", "load"),
            (base + "loader = load\ndel load\n", "def _other():\n    pass\nloader = _other\n",
             "load"),
            (base + "HANDLERS = {'x': load}\nfor load in ():\n    pass\n",
             empty + "HANDLERS = {'x': load}\nfor load in ():\n    pass\n", "load"),
            (base + "HANDLERS = {'x': load}\nwith open(__file__) as load:\n    pass\n",
             empty + "HANDLERS = {'x': load}\nwith open(__file__) as load:\n    pass\n", "load"),
            (base + "HANDLERS = {'x': load}\nfrom os import path as load\n",
             empty + "HANDLERS = {'x': load}\nfrom os import path as load\n", "load"),
            (base + "_a, _b = load, None\nfrom os import path as load\n",
             empty + "_a, _b = load, None\nfrom os import path as load\n", "load"),
            ("profile_keys = {'a'}\n",
             "profile_keys = {'a'}\nACCEPTED = profile_keys\nprofile_keys = {'b'}\n",
             "profile_keys"),
        ]
        for old, new, name in cases:
            with self.subTest(base=old, head=new), self.repo() as repo:
                repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + old)
                repo.checkpoint()
                repo.replace("tools/engine.py", old, new)
                self.assert_release_fails_closed(repo, name)

    def test_unreferenced_key_owner_release_drops_keys(self):
        # A release of a key-owning name the module never refers to drops its declarations, so a
        # del and redefinition reports the removed key; a parameter or local of the same name in
        # a function is not a reference unless the module loads the name, and a referenced name
        # that owns no accepted keys is released without failing closed.
        base = "def load():\n    profile_keys = {'a'}\n"
        empty = "def load():\n    profile_keys = set()\n"
        tail = "del load\ndef load():\n    pass\n"
        keep = "def keep():\n    profile_keys = {'a'}\n"
        removed = "accepted-key set module: removed a"
        for old, new, floor, reports in (
            (base, base + tail, "MAJOR", [removed]),
            (base, empty, "MAJOR", [removed]),
            (base, base + "del load\ndef load():\n    profile_keys = {'b'}\n", "MAJOR",
             [removed, "accepted-key set module: added b"]),
            (base + keep, base + keep + "del load\ndef load():\n    profile_keys = {'b'}\n",
             "MINOR", ["accepted-key set module: added b"]),
            (base, base + "def f(load):\n    pass\n" + tail, "MAJOR",
             [removed, "public symbol: added f"]),
            (base, base + "def f():\n    load = 1\n" + tail, "MAJOR",
             [removed, "public symbol: added f"]),
            (base, base + "def _plain():\n    pass\n_ref = _plain\ndel _plain\n", "PATCH", []),
        ):
            with self.subTest(base=old, head=new), self.repo() as repo:
                repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + old)
                repo.checkpoint()
                repo.replace("tools/engine.py", old, new)
                output = self.expect(repo, floor)
                for report in reports:
                    self.assertIn(report, output)
                if removed not in reports:
                    self.assertNotIn("accepted-key set module: removed", output)
                if not reports:
                    self.assertNotIn("accepted-key set", output)
        with self.subTest(unchanged=base), self.repo() as repo:
            repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + base)
            repo.checkpoint()
            output = self.expect(repo, "NONE", code=0)
            self.assertNotIn("accepted-key set", output)

    def test_top_level_rebinding_releases_accepted_keys(self):
        # A top-level statement that binds a key-set name, or the def holding a key set, again
        # (an assignment, an import or a with target) releases that name with certainty, so the
        # keys of the earlier binding are no longer counted.
        load_a = "def load():\n    profile_keys = {'a'}\n"
        for base, added, reports in (
            ("profile_keys = {'a'}\n", "profile_keys = {'b'}\n", ["removed a", "added b"]),
            (load_a, "from os import path as load\n", ["removed a"]),
            (load_a, "with open(__file__) as load:\n    pass\n", ["removed a"]),
        ):
            with self.subTest(base=base, added=added), self.repo() as repo:
                repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + base)
                repo.checkpoint()
                repo.replace("tools/engine.py", base, base + added)
                output = self.expect(repo, "MAJOR")
                for report in reports:
                    self.assertIn(f"accepted-key set module: {report}", output)

    def assert_release_uncertain(self, repo, name, reason):
        code, output = self.result(repo)
        self.assertEqual(code, 2, output)
        self.assertIn(
            f"ERROR: release-delta input: tools/engine.py: the release of {name}, which owns"
            " accepted keys, cannot be read as certain (", output)
        self.assertIn(reason, output)
        self.assertIn("the check cannot decide the floor", output)
        self.assertNotIn("FLOOR:", output)

    def release_case(self, base, expected, name):
        # The base appends base to the engine and is committed; the head removes key b from
        # every {'a', 'b'} in it and claims a PATCH (1.2.3 to 1.2.4).
        with self.repo() as repo:
            repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + base)
            repo.checkpoint()
            repo.replace("tools/engine.py", "{'a', 'b'}", "{'a'}")
            repo.version("1.2.4")
            if expected == "PATCH":
                output = self.expect(repo, "PATCH", 0, "PATCH")
                self.assertNotIn("accepted-key set", output)
            elif expected == "MAJOR":
                output = self.expect(repo, "MAJOR", 1, "PATCH")
                self.assertIn("accepted-key set module: removed b", output)
            elif expected == "reachable":
                self.assert_release_fails_closed(repo, name)
            elif expected == "invalid":
                # A source whose tree does not compile fails closed (exit 2).
                code, output = self.result(repo)
                self.assertEqual(code, 2, output)
                self.assertIn("ERROR: release-delta input: tools/engine.py: invalid Python: ",
                              output)
                self.assertNotIn("FLOOR:", output)
            elif expected == "no value":
                # A key-named annotation without a value binds nothing; it is refused as a
                # declaration without a value.
                code, output = self.result(repo)
                self.assertEqual(code, 2, output)
                self.assertIn(f"accepted-key declaration {name} has no value", output)
            else:
                # "declaration": the walker reads the binding as a declaration, which for a
                # name that owns keys is an uncertain release; the refusal names an assignment
                # expression outside every header (no header follows the construct).
                self.assert_release_uncertain(repo, name, {
                    "uncertain": "the statement may not bind or delete it",
                    "declaration": "the statement may not bind or delete it, or binds it only"
                                   " in a form not read as a certain release: an assignment"
                                   " expression); the check",
                    "shared": "also bound the same object to another target or handed it",
                    "global": "a global statement names it",
                }[expected])

    def test_release_regressions_and_controls(self):
        # A key set bound to two names by one chained assignment keeps the other name after a
        # del, and an empty for loop binds nothing, so neither release is certain; the
        # controls keep their verdicts, and a name that is neither keys nor *_keys is not a key
        # set.
        load = "def load():\n    profile_keys = {'a', 'b'}\n    return profile_keys\n"
        for label, base, expected, name in (
            ("chained assignment then del",
             "profile_keys = ACCEPTED = {'a', 'b'}\ndel profile_keys\n", "shared",
             "profile_keys"),
            ("empty for loop rebinding a def that owns keys",
             load + "for load in ():\n    pass\n", "uncertain", "load"),
            ("chained assignment kept",
             "profile_keys = ACCEPTED = {'a', 'b'}\n", "MAJOR", None),
            ("def that owns keys kept", load, "MAJOR", None),
            ("set bound to a name neither keys nor *_keys", "ACCEPTED = {'a', 'b'}\n",
             "PATCH", None),
            ("walrus in a return annotation",
             "profile_keys = {'a', 'b'}\ndef f() -> (profile_keys := {'b'}):\n    pass\n",
             "uncertain", "profile_keys"),
            ("walrus in an argument annotation",
             "profile_keys = {'a', 'b'}\ndef f(x: (profile_keys := {'b'})):\n    pass\n",
             "uncertain", "profile_keys"),
        ):
            with self.subTest(case=label):
                self.release_case(base, expected, name)

    def test_release_certainty_enumeration(self):
        # One case per form in Python's ast grammar that binds or deletes a module name, or
        # that looks like it does: a certain release of an unreferenced key set drops its keys
        # (PATCH), a release the check cannot read as certain fails closed, a release of a
        # referenced name fails closed as reachable, and a binding in another scope keeps the
        # keys (MAJOR). The owner is a private module-level key set, so _api reports no symbol.
        own = "_profile_keys = {'a', 'b'}\n"
        name = "_profile_keys"
        cases = [
            # Statements whose binding or deletion is certain at top level.
            ("Assign", "_profile_keys = set()\n", "PATCH"),
            ("AnnAssign with value", "_profile_keys: set = set()\n", "PATCH"),
            ("FunctionDef", "def _profile_keys():\n    pass\n", "PATCH"),
            ("AsyncFunctionDef", "async def _profile_keys():\n    pass\n", "PATCH"),
            ("ClassDef", "class _profile_keys:\n    pass\n", "PATCH"),
            ("Import", "import os as _profile_keys\n", "PATCH"),
            ("ImportFrom", "from os import sep as _profile_keys\n", "PATCH"),
            ("With target", "with open(__file__) as _profile_keys:\n    pass\n", "PATCH"),
            # An async with outside an async function does not compile, and the walker reads
            # its target as unread, never as a certain release, so it fails closed (exit 2)
            # before the compile step.
            ("AsyncWith target", "async with open(__file__) as _profile_keys:\n    pass\n",
             "uncertain"),
            ("Delete", "del _profile_keys\n", "PATCH"),
            ("AugAssign (reads the name)", "_profile_keys |= set()\n", "reachable"),
            ("ImportFrom of the name", "from os import _profile_keys\n", "reachable"),
            ("star ImportFrom", "from os import *\ndel _profile_keys\n", "reachable"),
            # Releases the check cannot read as certain, a name inside a tuple, list or starred
            # target among them (the check does not take such a target apart).
            ("Assign tuple target", "_profile_keys, _other = None, None\n", "uncertain"),
            ("Assign starred target", "*_profile_keys, = ()\n", "uncertain"),
            ("For target", "for _profile_keys in ():\n    pass\n", "uncertain"),
            ("AsyncFor target", "async for _profile_keys in ():\n    pass\n", "uncertain"),
            ("For body", "for _x in ():\n    del _profile_keys\n", "uncertain"),
            ("For else", "for _x in ():\n    pass\nelse:\n    del _profile_keys\n",
             "uncertain"),
            ("While body", "while False:\n    _profile_keys = set()\n", "uncertain"),
            ("While else", "while False:\n    pass\nelse:\n    del _profile_keys\n",
             "uncertain"),
            ("If body", "if False:\n    del _profile_keys\n", "uncertain"),
            ("If else", "if False:\n    pass\nelse:\n    _profile_keys = set()\n",
             "uncertain"),
            ("With body", "with open(__file__):\n    del _profile_keys\n", "uncertain"),
            ("AsyncWith body", "async with open(__file__):\n    del _profile_keys\n",
             "uncertain"),
            ("Try body", "try:\n    del _profile_keys\nexcept OSError:\n    pass\n",
             "uncertain"),
            ("Try handler body", "try:\n    pass\nexcept OSError:\n    del _profile_keys\n",
             "uncertain"),
            ("ExceptHandler name", "try:\n    pass\nexcept OSError as _profile_keys:\n    pass\n",
             "uncertain"),
            ("Try else", "try:\n    pass\nexcept OSError:\n    pass\nelse:\n"
             "    del _profile_keys\n", "uncertain"),
            ("Try finally", "try:\n    pass\nfinally:\n    del _profile_keys\n", "uncertain"),
            ("TryStar handler name",
             "try:\n    pass\nexcept* OSError as _profile_keys:\n    pass\n", "uncertain"),
            ("TryStar handler body",
             "try:\n    pass\nexcept* OSError:\n    del _profile_keys\n", "uncertain"),
            ("MatchAs capture", "match 1:\n    case _profile_keys:\n        pass\n",
             "uncertain"),
            ("MatchStar capture", "match []:\n    case [*_profile_keys]:\n        pass\n",
             "uncertain"),
            ("MatchMapping rest", "match {}:\n    case {**_profile_keys}:\n        pass\n",
             "uncertain"),
            ("Match case body", "match 1:\n    case 1:\n        del _profile_keys\n",
             "uncertain"),
            ("Import in a compound statement", "if False:\n    import os as _profile_keys\n",
             "uncertain"),
            ("FunctionDef in a compound statement",
             "if False:\n    def _profile_keys():\n        pass\n", "uncertain"),
            ("ClassDef in a compound statement",
             "if False:\n    class _profile_keys:\n        pass\n", "uncertain"),
            ("TypeAlias", "type _profile_keys = int\n", "uncertain"),
            # An assignment expression outside every header is read as a declaration, an
            # uncertain release of a name that owns keys.
            ("NamedExpr statement", "(_profile_keys := None)\n", "declaration"),
            ("NamedExpr in a module comprehension", "_xs = [(_profile_keys := _x) for _x in ()]\n",
             "declaration"),
            ("NamedExpr in a default value", "def _f(a=(_profile_keys := None)):\n    pass\n",
             "uncertain"),
            ("NamedExpr in a decorator",
             "@(_profile_keys := staticmethod)\ndef _f():\n    pass\n", "uncertain"),
            ("NamedExpr in a class base", "class _C((_profile_keys := object)):\n    pass\n",
             "uncertain"),
            ("NamedExpr in a class keyword",
             "class _C(metaclass=(_profile_keys := type)):\n    pass\n", "uncertain"),
            ("NamedExpr in an argument annotation",
             "def _f(a: (_profile_keys := None)):\n    pass\n", "uncertain"),
            ("NamedExpr in a return annotation",
             "def _f() -> (_profile_keys := None):\n    pass\n", "uncertain"),
            ("NamedExpr in a def type parameter bound",
             "def _f[T: (_profile_keys := int)]():\n    pass\n", "uncertain"),
            ("NamedExpr in a def type parameter default",
             "def _f[T = (_profile_keys := int)]():\n    pass\n", "uncertain"),
            ("NamedExpr in a class type parameter bound",
             "class _C[T: (_profile_keys := int)]:\n    pass\n", "uncertain"),
            ("Global in a def body", "def _reset():\n    global _profile_keys\n"
             "    _profile_keys = None\n", "global"),
            ("Global in a class body", "class _C:\n    global _profile_keys\n"
             "    del _profile_keys\n", "global"),
            ("Global at module level", "global _profile_keys\n", "global"),
            # Bindings of another scope, or no binding: the module key set stays counted.
            ("AnnAssign without value", "_profile_keys: object\n", "no value"),
            ("def local", "def _f():\n    _profile_keys = None\n", "MAJOR"),
            ("def parameter", "def _f(_profile_keys):\n    pass\n", "MAJOR"),
            ("def type parameter", "def _f[_profile_keys]():\n    pass\n", "MAJOR"),
            ("class body binding", "class _C:\n    _profile_keys = None\n", "MAJOR"),
            ("lambda parameter", "_f = lambda _profile_keys: None\n", "MAJOR"),
            ("NamedExpr in a lambda", "_f = lambda: (_profile_keys := set())\n", "MAJOR"),
            ("comprehension target", "_xs = [_y for _profile_keys in () for _y in ()]\n",
             "MAJOR"),
            ("Nonlocal in a nested def", "def _f():\n    _profile_keys = None\n"
             "    def _g():\n        nonlocal _profile_keys\n        _profile_keys = 1\n",
             "MAJOR"),
            ("del of an attribute", "import os as _os\ndel _os._profile_keys\n", "MAJOR"),
        ]
        for form, release, expected in cases:
            with self.subTest(form=form):
                self.release_case(own + release, expected, name)

    def test_unread_binding_places_fail_closed(self):
        # The check reads only a fixed set of places that bind or delete a module name (a
        # certain release, a declaration or an uncertain release); every other place that binds
        # or deletes a key-owning name (a name owning accepted keys, or named keys or *_keys)
        # fails closed with exit 2 and a message naming the module, the name and the construct.
        # The cases cover each place that is not read, each known unread input among them; an
        # uncertain release of a key-named name that owns no declarations, which fails closed
        # with its own message naming the construct; a with target after the first item and an
        # async with target
        # inside a compound statement, for a plain name and an unpacking target; and an owner
        # that is not key-named bound or deleted in a public def or class body. Each head
        # removes key b and claims a PATCH. The controls after them bind such an owner in a
        # public def or class body in a way that is not refused (the removal is reported,
        # MAJOR), and a class owner, which a process-wide __build_class__ hook can hand off,
        # fails closed as shared.
        own = "_profile_keys = {'a', 'b'}\n"
        keep = "_x = {'a', 'b'}\n"
        tuple_form = " (inside a tuple, list or starred target)"
        # A def that owns declarations but is not key-named is a key-owning name too.
        loader = "def load():\n    profile_keys = {'a', 'b'}\n"
        in_body = " in a def or class body"
        cases = [
            # A key-owning name inside a tuple, list or starred target.
            ("tuple-target declaration", "profile_keys, other = {'a', 'b'}, {'c'}\n",
             "profile_keys", "an assignment" + tuple_form),
            ("tuple-target declaration then del",
             "profile_keys, other = {'a', 'b'}, {'c'}\ndel profile_keys\n", "profile_keys",
             "an assignment" + tuple_form),
            ("list-target declaration", "[profile_keys, other] = {'a', 'b'}, {'c'}\n",
             "profile_keys", "an assignment" + tuple_form),
            ("starred-target declaration", "*profile_keys, = ({'a', 'b'},)\n", "profile_keys",
             "an assignment" + tuple_form + ", a place"),
            ("starred target inside a list", "[*profile_keys] = ({'a', 'b'},)\n",
             "profile_keys", "an assignment" + tuple_form + ", a place"),
            ("nested tuple target", "_x, (profile_keys, _y) = 1, ({'a', 'b'}, 2)\n",
             "profile_keys", "an assignment" + tuple_form + ", a place"),
            ("owner rebound in a tuple target", own + "_profile_keys, _other = None, None\n",
             "_profile_keys", "an assignment" + tuple_form),
            ("for tuple target", keep + "for profile_keys, _y in ():\n    pass\n",
             "profile_keys", "a for target" + tuple_form),
            ("del of a tuple", own + "del (_profile_keys,)\n", "_profile_keys",
             "a del" + tuple_form),
            # A with target a context manager can skip. A top-level async with does not
            # compile, so its target after the first item fails closed with the async with
            # reason, not the after-the-first-item reason.
            ("with target after a suppressing item", "import contextlib\n" + own
             + "with contextlib.suppress(OSError), open('/nonexistent/release-probe')"
             " as _profile_keys:\n    pass\n", "_profile_keys",
             "a with target after the first item"),
            ("async with target after the first item, outside an async def",
             "import contextlib\n" + own
             + "async with contextlib.suppress(OSError), f() as _profile_keys:\n    pass\n",
             "_profile_keys", "an async with target outside an async def"),
            ("with tuple target", "import contextlib\n" + own
             + "with contextlib.suppress(TypeError) as (_profile_keys, _other):\n    pass\n",
             "_profile_keys", "a with target" + tuple_form),
            ("with tuple target after a suppressing item", "import contextlib\n" + own
             + "with contextlib.suppress(OSError), open(__file__) as (_profile_keys, _y):\n"
             "    pass\n", "_profile_keys", "a with target after the first item"),
            # An assignment expression in a header.
            ("walrus in a type statement value",
             "profile_keys = {'a', 'b'}\ntype T = (profile_keys := {'b'})\n", "profile_keys",
             "an assignment expression in a type statement"),
            ("walrus in a type statement type parameter bound",
             "profile_keys = {'a', 'b'}\ntype T[X: (profile_keys := {'b'})] = int\n",
             "profile_keys", "an assignment expression in a type statement"),
            ("walrus declaring a key set in a type statement",
             "type _T = (profile_keys := {'a', 'b'})\n", "profile_keys",
             "an assignment expression in a type statement"),
            ("walrus in an underscore def default",
             "def _f(a=(profile_keys := {'a', 'b'})):\n    pass\n", "profile_keys",
             "an assignment expression in a def header"),
            ("walrus in a public def default, then del",
             "def f(a=(profile_keys := {'a', 'b'})):\n    pass\ndel f\n", "profile_keys",
             "an assignment expression in a def header"),
            ("walrus in a def decorator",
             "@(profile_keys := {'a', 'b'}).copy\ndef _f():\n    pass\n", "profile_keys",
             "an assignment expression in a def header"),
            ("walrus in a def argument annotation",
             "def _f(a: (profile_keys := {'a', 'b'})):\n    pass\n", "profile_keys",
             "an assignment expression in a def header"),
            ("walrus in a def return annotation",
             "def _f() -> (profile_keys := {'a', 'b'}):\n    pass\n", "profile_keys",
             "an assignment expression in a def header"),
            ("walrus in a def type parameter bound",
             "def _f[T: (profile_keys := {'a', 'b'})]():\n    pass\n", "profile_keys",
             "an assignment expression in a def header"),
            ("walrus in a def type parameter default",
             "def _f[T = (profile_keys := {'a', 'b'})]():\n    pass\n", "profile_keys",
             "an assignment expression in a def header"),
            ("walrus in an underscore class base",
             "class _C((profile_keys := {'a', 'b'}).__class__):\n    pass\n", "profile_keys",
             "an assignment expression in a class header"),
            ("walrus in a class keyword",
             "class _C(metaclass=(profile_keys := {'a', 'b'})):\n    pass\n", "profile_keys",
             "an assignment expression in a class header"),
            ("walrus in a class decorator",
             "@(profile_keys := {'a', 'b'}).copy\nclass _C:\n    pass\n", "profile_keys",
             "an assignment expression in a class header"),
            ("walrus in a class type parameter bound",
             "class _C[T: (profile_keys := {'a', 'b'})]:\n    pass\n", "profile_keys",
             "an assignment expression in a class header"),
            ("walrus in a lambda default",
             "_f = lambda a=(profile_keys := {'a', 'b'}): a\n", "profile_keys",
             "an assignment expression in a lambda header"),
            ("walrus in an annotation", "_y: (profile_keys := {'a', 'b'}) = 1\n",
             "profile_keys", "an assignment expression in an annotation"),
            # A global statement naming a key-named name.
            ("global in a def body", "def _f():\n    global profile_keys\n"
             "    profile_keys = {'a', 'b'}\n", "profile_keys", "a global statement"),
            # An uncertain release of a key-named name that owns no declarations.
            ("for target", "for profile_keys in ({'a', 'b'},):\n    pass\n", "profile_keys",
             "a for target, which the check reads as an uncertain release"),
            ("async for target", "async for profile_keys in ({'a', 'b'},):\n    pass\n",
             "profile_keys", "an async for target, which the check reads as an uncertain"
             " release"),
            ("except name", keep + "try:\n    pass\nexcept OSError as profile_keys:\n    pass\n",
             "profile_keys", "an except name"),
            ("except-star name",
             keep + "try:\n    pass\nexcept* OSError as profile_keys:\n    pass\n",
             "profile_keys", "an except name"),
            ("match capture", "match {'a', 'b'}:\n    case profile_keys:\n        pass\n",
             "profile_keys", "a match capture"),
            ("match star", keep + "match []:\n    case [*profile_keys]:\n        pass\n",
             "profile_keys", "a match capture"),
            ("match mapping rest", keep + "match {}:\n    case {**profile_keys}:\n        pass\n",
             "profile_keys", "a match mapping rest"),
            ("type statement name", keep + "type profile_keys = int\n", "profile_keys",
             "a type statement"),
            ("def in a compound statement",
             "if True:\n    def profile_keys():\n        return {'a', 'b'}\n", "profile_keys",
             "a def inside a compound statement"),
            ("async def in a compound statement",
             "if True:\n    async def profile_keys():\n        return {'a', 'b'}\n",
             "profile_keys", "an async def inside a compound statement"),
            ("class in a compound statement",
             keep + "if True:\n    class profile_keys:\n        pass\n", "profile_keys",
             "a class inside a compound statement"),
            ("import in a compound statement",
             keep + "if True:\n    import os as profile_keys\n", "profile_keys",
             "an import inside a compound statement"),
            ("del in a compound statement", keep + "if False:\n    del profile_keys\n",
             "profile_keys", "a del inside a compound statement"),
            ("augmented assignment in a compound statement",
             keep + "if False:\n    profile_keys |= set()\n", "profile_keys",
             "an augmented assignment inside a compound statement"),
            ("with target in a compound statement",
             keep + "if True:\n    with open(__file__) as profile_keys:\n        pass\n",
             "profile_keys", "a with target inside a compound statement"),
            # A with target after the first item, and every async with target, keeps its
            # reason inside a compound statement, for a plain name and an unpacking target.
            ("with target after the first item in a compound statement",
             keep + "if True:\n    with open(__file__), open(__file__) as profile_keys:\n"
             "        pass\n", "profile_keys", "a with target after the first item"),
            ("with tuple target after the first item in a compound statement",
             own + "while False:\n    with open(__file__), open(__file__) as"
             " (_profile_keys, _y):\n        pass\n", "_profile_keys",
             "a with target after the first item"),
            ("async with target in a compound statement",
             keep + "if True:\n    async with f() as profile_keys:\n        pass\n",
             "profile_keys", "an async with target outside an async def"),
            ("async with tuple target in a compound statement",
             own + "if True:\n    async with f() as (_profile_keys, _y):\n        pass\n",
             "_profile_keys", "an async with target outside an async def"),
            ("for target in a compound statement",
             keep + "if True:\n    for profile_keys in ():\n        pass\n", "profile_keys",
             "a for target inside a compound statement, which the check reads as an"
             " uncertain release"),
            ("async for target in a compound statement",
             keep + "if True:\n    async for profile_keys in f():\n        pass\n",
             "profile_keys", "an async for target inside a compound statement, which the"
             " check reads as an uncertain release"),
            ("for tuple target in a compound statement",
             keep + "while False:\n    for profile_keys, _y in ():\n        pass\n",
             "profile_keys", "a for target inside a compound statement" + tuple_form),
            # A key-owning name that is not key-named (a def owning declarations), bound or
            # deleted in a public def or class body, before or after its declarations.
            ("owner that is not key-named deleted in a public def",
             loader + "def g():\n    del load\n", "g.load", "a del" + in_body),
            ("owner that is not key-named deleted in a public def before the owner",
             "def g():\n    del load\n" + loader, "g.load", "a del" + in_body),
            ("owner that is not key-named rebound by a for target in a public def",
             loader + "def g():\n    for load in ():\n        pass\n", "g.load",
             "a for target" + in_body),
            ("owner that is not key-named rebound by a for target in a class body",
             loader + "class C:\n    for load in ():\n        pass\n", "C.load",
             "a for target" + in_body),
            ("owner that is not key-named rebound by an augmented assignment",
             loader + "def g():\n    load += 1\n", "g.load",
             "an augmented assignment" + in_body),
            ("owner that is not key-named rebound by a nested def",
             loader + "def g():\n    def load():\n        pass\n", "g.load",
             "a def" + in_body),
            ("owner that is not key-named in a tuple target in a public def",
             loader + "def g():\n    load, other = 1, 2\n", "g.load",
             "a name inside a tuple, list or starred target" + in_body),
            # Refusing these is a deliberate over-refusal: in a public def or class body
            # each binds a local or a class attribute, which cannot rebind the module name
            # without a global statement (refused separately).
            ("owner that is not key-named rebound by a method",
             loader + "class C:\n    def load(self):\n        pass\n", "C.load",
             "a def" + in_body),
            ("owner that is not key-named rebound by a nested class",
             loader + "def g():\n    class load:\n        pass\n", "g.load",
             "a class" + in_body),
            ("owner that is not key-named rebound by an import in a public def",
             loader + "def g():\n    import os as load\n", "g.load", "an import" + in_body),
            ("owner that is not key-named rebound by an except name in a public def",
             loader + "def g():\n    try:\n        pass\n    except OSError as load:\n"
             "        pass\n", "g.load", "an except name" + in_body),
        ]
        for form, base, name, construct in cases:
            with self.subTest(form=form), self.repo() as repo:
                repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + base)
                repo.checkpoint()
                repo.replace("tools/engine.py", "{'a', 'b'}", "{'a'}")
                repo.version("1.2.4")
                code, output = self.result(repo)
                self.assertEqual(code, 2, output)
                self.assertIn("ERROR: release-delta input: tools/engine.py: ", output)
                self.assertIn(name, output)
                self.assertIn(construct, output)
                self.assertNotIn(tuple_form + tuple_form, output)
                self.assertIn("the check cannot decide the floor", output)
                self.assertNotIn("FLOOR:", output)
        # A plain assignment, an annotated assignment, an assignment expression or a
        # parameter binding an owner that is not key-named in a public def or class body is
        # not refused, so the removal of key b is reported (MAJOR, exit 1).
        for form, body in (
            ("plain assignment in a public def", "def g():\n    load = 1\n"),
            ("annotated assignment in a public def", "def g():\n    load: int = 1\n"),
            ("assignment expression in a public def", "def g():\n    (load := 1)\n"),
            ("parameter of a public def", "def g(load):\n    pass\n"),
            ("plain assignment in a class body", "class C:\n    load = 1\n"),
            ("annotated assignment in a class body", "class C:\n    load: int = 1\n"),
        ):
            with self.subTest(form=form):
                self.release_case(loader + body, "MAJOR", None)
        # A class statement calls builtins.__build_class__, which any code in the process can
        # replace, so a class owner is shared and its release fails closed.
        with self.subTest(form="process-wide __build_class__ hook"):
            self.release_case(
                "import builtins\n_HOLD = []\n_build = builtins.__build_class__\n"
                "def _hook(*args, **kwargs):\n    made = _build(*args, **kwargs)\n"
                "    _HOLD.append(made)\n    return made\nbuiltins.__build_class__ = _hook\n"
                "class Loader:\n    def load(self):\n        profile_keys = {'a', 'b'}\n"
                "        return profile_keys\nbuiltins.__build_class__ = _build\ndel Loader\n",
                "shared", "Loader")

    def test_read_binding_places_keep_their_verdicts(self):
        # The places the check reads keep their verdicts: a certain release drops the keys
        # (PATCH), a binding that is no release keeps them (MAJOR), and a declaration counts.
        own = "_profile_keys = {'a', 'b'}\n"
        for form, base, expected in (
            ("plain removal", "profile_keys = {'a', 'b'}\n", "MAJOR"),
            ("declaration in a compound statement", "if True:\n    profile_keys = {'a', 'b'}\n",
             "MAJOR"),
            ("walrus declaration outside a header", "ACCEPTED = (profile_keys := {'a', 'b'})\n",
             "MAJOR"),
            ("walrus declaration in a module comprehension",
             "_xs = [(profile_keys := {'a', 'b'}) for _y in ()]\n", "MAJOR"),
            ("first with item target", "import contextlib\n" + own
             + "with open(__file__) as _profile_keys, contextlib.suppress(OSError):\n"
             "    pass\n", "PATCH"),
            ("single with item target", own + "with open(__file__) as _profile_keys:\n    pass\n",
             "PATCH"),
            ("import", own + "import os as _profile_keys\n", "PATCH"),
            ("del", own + "del _profile_keys\n", "PATCH"),
            ("undecorated def, certain release",
             "def load():\n    profile_keys = {'a', 'b'}\n\ndel load\n", "PATCH"),
            ("tuple target of names that own no keys", own + "_a, *_b = 1, 2\n", "MAJOR"),
            ("walrus of another name in a def header", own
             + "def _f(a=(_y := 1)):\n    pass\n", "MAJOR"),
            # A top-level |= on a key-named name that owns no declaration is a certain
            # release and no declaration, so its keys are not accepted keys (PATCH).
            ("top-level augmented assignment on a key-named name without a declaration",
             "profile_keys |= {'a', 'b'}\n", "PATCH"),
        ):
            with self.subTest(form=form):
                self.release_case(base, expected, None)

    # One module per Python 3 construct that binds, deletes or scopes a name, each binding a
    # key-named name through it; the walker reads it by Python's scoping rules (the accepted
    # keys it reports) or fails closed (a ValueError, which check() turns into exit 2). A
    # construct that counts a name in the wrong scope gives neither and fails the test.
    SCOPE_CASES = [
        ("module assignment", "profile_keys = {'k'}\n", {"k"}),
        ("module del", "profile_keys = {'k'}\ndel profile_keys\n", set()),
        ("def body", "def f():\n    profile_keys = {'k'}\n", {"k"}),
        ("def then del", "def f():\n    profile_keys = {'k'}\ndel f\n", set()),
        ("private def body", "def _f():\n    profile_keys = {'k'}\n", set()),
        ("def default walrus", "def f(x=(profile_keys := {'k'})):\n    pass\n", "exit2"),
        ("def in if", "if True:\n    def f():\n        profile_keys = {'k'}\n", {"k"}),
        ("async def in if", "if True:\n    async def f():\n        profile_keys = {'k'}\n",
         {"k"}),
        ("def in if, deleted in the same statement",
         "if True:\n    def f():\n        profile_keys = {'k'}\n    del f\n", "exit2"),
        ("async def body", "async def f():\n    profile_keys = {'k'}\n", {"k"}),
        ("async def in try, deleted in finally",
         "try:\n    async def f():\n        profile_keys = {'k'}\nfinally:\n    del f\n",
         "exit2"),
        ("class body", "class C:\n    profile_keys = {'k'}\n", {"k"}),
        ("class then del", "class C:\n    profile_keys = {'k'}\ndel C\n", "exit2"),
        ("class in try, deleted in finally",
         "try:\n    class C:\n        profile_keys = {'k'}\nfinally:\n    del C\n", "exit2"),
        ("class body walrus", "class C:\n    (profile_keys := {'k'})\n", {"k"}),
        ("lambda body walrus", "_probe = lambda: (profile_keys := {'k'})\n", set()),
        ("lambda body walrus, lambda deleted",
         "_probe = lambda: (profile_keys := {'k'})\ndel _probe\n", set()),
        ("lambda body walrus beside a module key set",
         "profile_keys = {'k'}\n_probe = lambda: (profile_keys := {'j'})\n", {"k"}),
        ("lambda in a public def", "def f():\n    g = lambda: (profile_keys := {'k'})\n",
         {"k"}),
        ("lambda default walrus", "f = lambda x=(profile_keys := {'k'}): x\n", "exit2"),
        # A lambda default nested in a module-level lambda body runs in that lambda's scope,
        # so its assignment expression binds a lambda local: no declaration and no refusal.
        ("lambda default walrus in a module-level lambda body",
         "profile_keys = {'k'}\nX = lambda: (lambda y=(profile_keys := {'z'}): y)\n", {"k"}),
        ("comprehension in a lambda body",
         "f = lambda: [(profile_keys := {'k'}) for _ in ()]\n", set()),
        ("list comprehension target", "[0 for profile_keys in [{'k'}]]\n", set()),
        ("set comprehension target", "{0 for profile_keys in [{'k'}]}\n", set()),
        ("dict comprehension target", "{0: 0 for profile_keys in [{'k'}]}\n", set()),
        ("generator expression target", "(0 for profile_keys in [{'k'}])\n", set()),
        ("list comprehension walrus", "[(profile_keys := {'k'}) for _ in ()]\n", {"k"}),
        ("set comprehension walrus", "{(profile_keys := {'k'}) for _ in ()}\n", {"k"}),
        ("dict comprehension walrus", "{0: (profile_keys := {'k'}) for _ in ()}\n", {"k"}),
        ("generator expression walrus", "((profile_keys := {'k'}) for _ in ())\n", {"k"}),
        ("generator expression walrus releasing an owner",
         "profile_keys = {'k'}\n((profile_keys := 1) for _ in ())\n", "exit2"),
        ("comprehension target subscript walrus in a def default",
         "profile_keys = {'k'}\ndef f(x=[0 for d[(profile_keys := {'j'})] in ()]):\n"
         "    pass\n", "exit2"),
        # An assignment expression directly in a comprehension target does not compile
        # ("comprehension inner loop cannot rebind assignment expression target"), so at module
        # level only _surface's compile step refuses it, after the walker. A lambda there
        # compiles, and its body is a scope of its own, where an assignment expression binds a
        # lambda local, no declaration; at module level the walker reads only the lambda's
        # defaults and skips its body (neither _accepted_sets nor _binding_events reaches it),
        # so this case finds no keys.
        ("comprehension target subscript lambda walrus at module",
         "[0 for d[lambda: (profile_keys := {'k'})] in ()]\n", set()),
        ("comprehension tuple target", "profile_keys = {'k'}\n[0 for (profile_keys, _y) in ()]\n",
         {"k"}),
        ("type statement name", "profile_keys = {'k'}\ntype profile_keys = int\n", "exit2"),
        ("type statement value walrus", "type T = (profile_keys := {'k'})\n", "exit2"),
        ("def type parameter", "profile_keys = {'k'}\ndef f[profile_keys]():\n    pass\n",
         {"k"}),
        ("class type parameter", "profile_keys = {'k'}\nclass C[profile_keys]:\n    pass\n",
         {"k"}),
        ("type statement type parameter", "profile_keys = {'k'}\ntype T[profile_keys] = int\n",
         {"k"}),
        ("type parameter bound walrus", "def f[T: (profile_keys := {'k'})]():\n    pass\n",
         "exit2"),
        # A lambda in a def or class header is a scope of its own: a walrus in its body binds a
        # lambda local, so the def or class does not own it.
        ("def default lambda walrus",
         "def f(x=lambda: (profile_keys := {'k'})):\n    pass\n", set()),
        ("def type parameter bound lambda walrus",
         "def f[T: (lambda: (profile_keys := {'k'}))]():\n    pass\n", set()),
        ("def type parameter default lambda walrus",
         "def f[T = (lambda: (profile_keys := {'k'}))]():\n    pass\n", set()),
        ("def decorator lambda walrus",
         "@(lambda g: (profile_keys := {'k'}) and g)\ndef f():\n    pass\n", set()),
        ("class keyword lambda walrus",
         "class C(x=lambda: (profile_keys := {'k'})):\n    pass\n", set()),
        # A nested def's header runs in the body around it, so its walrus is owned there.
        ("nested def default walrus",
         "def f():\n    def g(x=(profile_keys := {'k'})):\n        pass\n", {"k"}),
        ("def header walrus rebinding the def name",
         "def f(x=(f := 1)):\n    profile_keys = {'k'}\n", "exit2"),
        ("walrus at module", "(profile_keys := {'k'})\n", {"k"}),
        ("walrus in a def", "def f():\n    (profile_keys := {'k'})\n", {"k"}),
        ("two walruses in one statement",
         "print((profile_keys := {'k'}), (profile_keys := {'j'}))\n", "exit2"),
        ("rebound in one compound statement",
         "if True:\n    profile_keys = {'k'}\n    profile_keys = {'j'}\n", "exit2"),
        ("global in a def", "def f():\n    global profile_keys\n    profile_keys = {'k'}\n",
         "exit2"),
        ("global at module", "profile_keys = {'k'}\nglobal profile_keys\n", "exit2"),
        ("nonlocal", "def f():\n    profile_keys = {'k'}\n    def g():\n"
         "        nonlocal profile_keys\n        profile_keys = {'j'}\n", "exit2"),
        ("del in a compound statement", "profile_keys = {'k'}\nif True:\n    del profile_keys\n",
         "exit2"),
        ("del in a def", "profile_keys = {'k'}\ndef f():\n    del profile_keys\n", "exit2"),
        ("del of a tuple", "profile_keys = {'k'}\ndel (profile_keys,)\n", "exit2"),
        ("import", "profile_keys = {'k'}\nimport profile_keys\n", set()),
        ("import as", "profile_keys = {'k'}\nimport os as profile_keys\n", set()),
        ("dotted import", "profile_keys = {'k'}\nimport profile_keys.sub\n", set()),
        ("from-import as", "profile_keys = {'k'}\nfrom os import sep as profile_keys\n", set()),
        ("star import after a declaration", "profile_keys = {'k'}\nfrom os import *\n", "exit2"),
        ("star import in a compound statement",
         "profile_keys = {'k'}\nif True:\n    from os import *\n", "exit2"),
        ("star import after a declaration in the same statement",
         "try:\n    profile_keys = {'k'}\n    from os import *\nexcept ImportError:\n    pass\n",
         "exit2"),
        ("star import before a declaration in the same statement",
         "if True:\n    from os import *\n    profile_keys = {'k'}\n", "exit2"),
        ("import in a def", "profile_keys = {'k'}\ndef f():\n    import os as profile_keys\n",
         "exit2"),
        ("import in a compound statement",
         "profile_keys = {'k'}\nif True:\n    import os as profile_keys\n", "exit2"),
        ("for target", "for profile_keys in ({'k'},):\n    pass\n", "exit2"),
        ("for target releasing an owner",
         "profile_keys = {'k'}\nfor profile_keys in ():\n    pass\n", "exit2"),
        ("for target in a def", "def f():\n    for profile_keys in ():\n        pass\n",
         "exit2"),
        ("async for target", "profile_keys = {'k'}\nasync for profile_keys in ():\n    pass\n",
         "exit2"),
        ("with target", "profile_keys = {'k'}\nwith open(__file__) as profile_keys:\n    pass\n",
         set()),
        ("with target after the first item", "profile_keys = {'k'}\n"
         "with open(__file__), open(__file__) as profile_keys:\n    pass\n", "exit2"),
        # An async with outside an async function does not compile, and the walker reads its
        # target as unread.
        ("async with target",
         "profile_keys = {'k'}\nasync with open(__file__) as profile_keys:\n    pass\n", "exit2"),
        ("with target in a def",
         "def f():\n    with open(__file__) as profile_keys:\n        pass\n", "exit2"),
        ("except name",
         "profile_keys = {'k'}\ntry:\n    pass\nexcept OSError as profile_keys:\n    pass\n",
         "exit2"),
        ("except-star name",
         "profile_keys = {'k'}\ntry:\n    pass\nexcept* OSError as profile_keys:\n    pass\n",
         "exit2"),
        ("except name in a def", "def f():\n    try:\n        pass\n"
         "    except OSError as profile_keys:\n        pass\n", "exit2"),
        ("match capture", "profile_keys = {'k'}\nmatch 1:\n    case profile_keys:\n        pass\n",
         "exit2"),
        ("match star",
         "profile_keys = {'k'}\nmatch []:\n    case [*profile_keys]:\n        pass\n", "exit2"),
        ("match mapping rest",
         "profile_keys = {'k'}\nmatch {}:\n    case {**profile_keys}:\n        pass\n", "exit2"),
        ("match as pattern",
         "profile_keys = {'k'}\nmatch []:\n    case [1] as profile_keys:\n        pass\n",
         "exit2"),
        ("match class pattern capture",
         "profile_keys = {'k'}\nmatch 1:\n    case int(profile_keys):\n        pass\n", "exit2"),
        ("match capture in a def",
         "def f():\n    match 1:\n        case profile_keys:\n            pass\n", "exit2"),
        ("annotated name with a value", "profile_keys: set = {'k'}\n", {"k"}),
        ("annotated name without a value", "profile_keys = {'k'}\nprofile_keys: set\n", "exit2"),
        ("annotated name without a value in a def", "def f():\n    profile_keys: set\n",
         "exit2"),
        ("augmented assignment", "profile_keys = {'k'}\nprofile_keys |= {'j'}\n", "exit2"),
        ("expression nested too deeply", "LIMIT = " + " + ".join(["1"] * 3000) + "\n", "exit2"),
        ("expression too complex to parse", "LIMIT = " + "-" * 60000 + "1\n", "exit2"),
    ]

    def test_async_with_target_outside_an_async_def_is_never_certain(self):
        # An async with compiles only in an async def body, so a module-level one does not
        # compile and _surface's compile step refuses it after the walker. The walker itself
        # must still never read its target as a certain release, and every target of one, at
        # top level or inside a compound statement, a plain name or a name inside an unpacking
        # target, is refused for not compiling rather than for its position, its depth or its
        # unpacking: these cases call _binding_events and _accepted_sets on the parsed tree,
        # without the compile step.
        outside = "an async with target outside an async def, which does not compile"
        cases = [
            ("first item, owner", "_profile_keys = {'a', 'b'}\n"
             "async with open(__file__) as _profile_keys:\n    pass\n", outside),
            ("first item, key-named name that owns nothing",
             "async with open(__file__) as profile_keys:\n    pass\n", outside),
            ("second item of an async with, owner", "_profile_keys = {'a', 'b'}\n"
             "async with open(__file__) as _x, open(__file__) as _profile_keys:\n    pass\n",
             outside),
            ("tuple target, owner", "_profile_keys = {'a', 'b'}\n"
             "async with open(__file__) as (_profile_keys, _y):\n    pass\n", outside),
            ("tuple target, key-named name that owns nothing",
             "async with open(__file__) as (profile_keys, y):\n    pass\n", outside),
            ("starred target inside a list, owner", "_profile_keys = {'a', 'b'}\n"
             "async with open(__file__) as [*_profile_keys]:\n    pass\n", outside),
            ("nested tuple target of a second item, owner", "_profile_keys = {'a', 'b'}\n"
             "async with open(__file__) as _x, open(__file__) as (_y, (_profile_keys, _z)):\n"
             "    pass\n", outside),
            ("inside a compound statement, owner", "_profile_keys = {'a', 'b'}\n"
             "if True:\n    async with open(__file__) as _profile_keys:\n        pass\n",
             outside),
            ("inside a compound statement, key-named name that owns nothing",
             "if True:\n    async with open(__file__) as profile_keys:\n        pass\n",
             outside),
            ("tuple target inside a compound statement, owner", "_profile_keys = {'a', 'b'}\n"
             "while False:\n    async with open(__file__) as (_profile_keys, _y):\n"
             "        pass\n", outside),
            ("second item inside a compound statement, owner", "_profile_keys = {'a', 'b'}\n"
             "try:\n    async with open(__file__) as _x, open(__file__) as _profile_keys:\n"
             "        pass\nfinally:\n    pass\n", outside),
            ("nested tuple target of a second item inside a compound statement, owner",
             "_profile_keys = {'a', 'b'}\nfor _i in ():\n"
             "    async with open(__file__) as _x, open(__file__) as (_y, (_profile_keys, _z)):\n"
             "        pass\n", outside),
        ]
        for form, source, reason in cases:
            with self.subTest(form=form):
                tree = ast.parse(source)
                events = [(construct, kind) for node in tree.body
                          for _, construct, kind in DELTA._binding_events(node)
                          if construct.startswith("an async with target")]
                self.assertTrue(events)
                self.assertEqual({construct for construct, _ in events}, {reason})
                self.assertNotIn("certain", [kind for _, kind in events])
                with self.assertRaises(ValueError) as caught:
                    DELTA._accepted_sets(tree, "tools/engine.py")
                self.assertIn(reason, str(caught.exception))

    def test_async_with_second_item_gets_the_async_reason(self):
        # _binding_events checks for a top-level async with before the second-item rule, for
        # every item: the second-item reason describes an earlier context manager skipping a
        # later target of a statement that runs, and a top-level async with does not compile, so
        # no context manager in it ever runs and not compiling is the reason that applies.
        source = ("_profile_keys = {'a', 'b'}\n"
                  "async with open(__file__) as _x, open(__file__) as _profile_keys:\n    pass\n")
        tree = ast.parse(source)
        reason = "an async with target outside an async def, which does not compile"
        self.assertEqual(DELTA._binding_events(tree.body[1]),
                         [("_x", reason, "unread"), ("_profile_keys", reason, "unread")])
        with self.assertRaises(ValueError) as caught:
            DELTA._accepted_sets(tree, "tools/engine.py")
        self.assertIn(reason, str(caught.exception))
        self.assertNotIn("after the first item", str(caught.exception))

    def test_with_target_after_the_first_item_is_never_certain(self):
        # An earlier context manager of a with statement can skip binding a later item's
        # target, so the walker never reads that target as a certain release. The reason
        # depends on the item's position only: a plain name and every name an unpacking target
        # holds get it, at top level and inside a compound statement, without the unpacking
        # suffix. Only the kind can differ: for a plain-name target it follows the depth
        # (unread at top level, uncertain inside a compound statement), and every name inside an
        # unpacking target is unread at any depth. These cases use a with statement, which
        # compiles at module level, so they reach the second-item rule and not the async with
        # refusal.
        reason = "a with target after the first item, which an earlier context manager can skip"
        first = ("_x", "a with target", "certain")
        nested = ("_x", "a with target inside a compound statement", "uncertain")
        cases = [
            ("second item, owner", "_profile_keys = {'a', 'b'}\n"
             "with open(__file__) as _x, open(__file__) as _profile_keys:\n    pass\n",
             [first, ("_profile_keys", reason, "unread")]),
            ("second item, key-named name that owns nothing",
             "with open(__file__) as _x, open(__file__) as profile_keys:\n    pass\n",
             [first, ("profile_keys", reason, "unread")]),
            ("tuple target of a second item, owner", "_profile_keys = {'a', 'b'}\n"
             "with open(__file__) as _x, open(__file__) as (_profile_keys, _y):\n    pass\n",
             [first, ("_profile_keys", reason, "unread"), ("_y", reason, "unread")]),
            ("starred target of a second item, key-named name that owns nothing",
             "with open(__file__) as _x, open(__file__) as [_y, *profile_keys]:\n    pass\n",
             [first, ("_y", reason, "unread"), ("profile_keys", reason, "unread")]),
            ("second item inside a compound statement, owner", "_profile_keys = {'a', 'b'}\n"
             "if True:\n    with open(__file__) as _x, open(__file__) as _profile_keys:\n"
             "        pass\n",
             [nested, ("_profile_keys", reason, "uncertain")]),
            ("second item inside a compound statement, key-named name that owns nothing",
             "while False:\n    with open(__file__) as _x, open(__file__) as profile_keys:\n"
             "        pass\n",
             [nested, ("profile_keys", reason, "uncertain")]),
            ("tuple target of a second item inside a compound statement, owner",
             "_profile_keys = {'a', 'b'}\ntry:\n"
             "    with open(__file__) as _x, open(__file__) as (_y, (_profile_keys, _z)):\n"
             "        pass\nfinally:\n    pass\n",
             [nested, ("_y", reason, "unread"), ("_profile_keys", reason, "unread"),
              ("_z", reason, "unread")]),
        ]
        for form, source, events in cases:
            with self.subTest(form=form):
                tree = ast.parse(source)
                compile(tree, "tools/engine.py", "exec")
                self.assertEqual(DELTA._binding_events(tree.body[-1]), events)
                with self.assertRaises(ValueError) as caught:
                    DELTA._accepted_sets(tree, "tools/engine.py")
                self.assertIn(reason, str(caught.exception))
                self.assertNotIn("inside a tuple", str(caught.exception))

    def test_scoping_constructs_handled_or_fail_closed(self):
        for form, source, expected in self.SCOPE_CASES:
            with self.subTest(form=form):
                try:
                    found = DELTA._api(source.encode("utf-8"), "tools/engine.py")[2]
                except ValueError as exc:
                    self.assertEqual(expected, "exit2", str(exc))
                    self.assertIn("tools/engine.py: ", str(exc))
                    continue
                self.assertEqual(found.get("module", set()), expected)

    def patch_claim_case(self, base, head):
        # The base appends base to the engine and is committed; the head replaces it with head
        # and claims a PATCH (1.2.3 to 1.2.4).
        with self.repo() as repo:
            repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + base)
            repo.checkpoint()
            repo.replace("tools/engine.py", base, head)
            repo.version("1.2.4")
            return self.result(repo)

    def test_scoping_regressions_through_check(self):
        # A walrus in a lambda body binds a lambda local, so the key set is gone (MAJOR).
        code, output = self.patch_claim_case(
            "_known_keys = {'a', 'b'}\n",
            "_probe = lambda: (_known_keys := {'a', 'b'})\ndel _probe\n")
        self.assertEqual(code, 1, output)
        self.assertIn("accepted-key set module: removed a", output)
        self.assertIn("accepted-key set module: removed b", output)
        load = "def load():\n    profile_keys = {'a', 'b'}\n"
        for form, head, message in (
            ("def declared and deleted in one if statement",
             "def load():\n    profile_keys = {'a'}\nif True:\n    def helper():\n"
             "        old_keys = {'b'}\n    del helper\n",
             "the release of helper, which owns accepted keys, cannot be read as certain"),
            ("class declared in try and deleted in finally",
             "def load():\n    profile_keys = {'a'}\ntry:\n    class Holder:\n"
             "        extra_keys = {'b'}\nfinally:\n    del Holder\n",
             "the release of Holder, which owns accepted keys, cannot be read as certain"),
            ("walrus in a comprehension target in a def default",
             "def load():\n    profile_keys = {'a'}\n"
             "def f(x=[0 for d[(profile_keys := {'b'})] in ()]):\n    pass\n",
             "an assignment expression in a def header"),
            ("star import after a declaration", load + "from os import *\n",
             "a star import after a declaration of"),
            ("expression nested too deeply",
             load + "LIMIT = " + " + ".join(["1"] * 3000) + "\n",
             "nested too deeply for the check to read"),
        ):
            with self.subTest(form=form):
                code, output = self.patch_claim_case(load, head)
                self.assertEqual(code, 2, output)
                self.assertIn("ERROR: release-delta input: tools/engine.py: ", output)
                self.assertIn(message, output)
                self.assertNotIn("FLOOR:", output)

    def test_header_scope_regressions_through_check(self):
        # A lambda in a def header is a scope of its own, so a walrus in its body binds a lambda
        # local and the def does not own it: the key set loses b (MAJOR, exit 1).
        for form, base, head in (
            ("type parameter bound",
             "_known_keys = {'a', 'b'}\ndef f[T: int]():\n    pass\n",
             "_known_keys = {'a'}\ndef f[T: (lambda: (_known_keys := {'b'}))]():\n    pass\n"),
            ("type parameter default",
             "_known_keys = {'a', 'b'}\ndef f[T = int]():\n    pass\n",
             "_known_keys = {'a'}\ndef f[T = (lambda: (_known_keys := {'b'}))]():\n    pass\n"),
            ("argument default",
             "_known_keys = {'a', 'b'}\ndef f(x=None):\n    pass\n",
             "_known_keys = {'a'}\ndef f(x=lambda: (_known_keys := {'b'})):\n    pass\n"),
        ):
            with self.subTest(form=form):
                code, output = self.patch_claim_case(base, head)
                self.assertEqual(code, 1, output)
                self.assertIn("FLOOR: MAJOR", output)
                self.assertIn("accepted-key set module: removed b", output)
        # The same lambda holds the only declaration of b in the base and the head drops it: the
        # lambda body is a lambda scope that no def owns, so b was never an accepted key (PATCH,
        # exit 0). Reading the header in the def's own scope would make b a key of f (MAJOR).
        with self.subTest(form="header lambda key removed"):
            code, output = self.patch_claim_case(
                "_known_keys = {'a'}\ndef f(x=lambda: (_known_keys := {'b'})):\n    pass\n",
                "_known_keys = {'a'}\ndef f(x=None):\n    pass\n")
            self.assertEqual(code, 0, output)
            self.assertIn("FLOOR: PATCH", output)
            self.assertNotIn("accepted-key set", output)
        # A star import in the statement that makes a declaration fails closed (exit 2), in a
        # module with no earlier declaration.
        with self.subTest(form="star import in the declaring statement"), self.repo() as repo:
            repo.write("tools/engine.py",
                       "try:\n    profile_keys = {'a', 'b'}\nexcept ImportError:\n    pass\n")
            repo.checkpoint()
            repo.write("tools/engine.py", "try:\n    profile_keys = {'a', 'b'}\n"
                       "    from os import *\nexcept ImportError:\n    pass\n")
            repo.version("1.2.4")
            code, output = self.result(repo)
            self.assertEqual(code, 2, output)
            self.assertIn("ERROR: release-delta input: tools/engine.py: ", output)
            self.assertIn("a star import after a declaration of profile_keys", output)
            self.assertNotIn("FLOOR:", output)
        # A module too complex for ast.parse (MemoryError) fails closed (exit 2).
        with self.subTest(form="expression too complex to parse"):
            load = "def load():\n    profile_keys = {'a', 'b'}\n"
            code, output = self.patch_claim_case(load, load + "LIMIT = " + "-" * 60000 + "1\n")
            self.assertEqual(code, 2, output)
            self.assertIn("ERROR: release-delta input: tools/engine.py: ", output)
            self.assertIn("too complex for the check to parse", output)
            self.assertNotIn("FLOOR:", output)

    def test_value_less_key_named_annotation_reach_through_check(self):
        # An annotated assignment without a value to a key-named name binds nothing, and the
        # walker refuses it (exit 2) everywhere it reads statements: inside a top-level
        # compound statement, in a public class body and in a def nested in a compound
        # statement. A private def body, and a public def inside a private class, are not read,
        # so the same annotation there is no input error and the PATCH claim stands (exit 0).
        # Each base holds the same statement without the annotation.
        for form, base, head in (
            ("top-level if",
             "if True:\n    pass\n",
             "if True:\n    profile_keys: set\n"),
            ("public class body",
             "class Holder:\n    pass\n",
             "class Holder:\n    profile_keys: set\n"),
            ("def inside a compound statement",
             "while False:\n    def load():\n        pass\n",
             "while False:\n    def load():\n        profile_keys: set\n"),
        ):
            with self.subTest(form=form):
                code, output = self.patch_claim_case(base, head)
                self.assertEqual(code, 2, output)
                self.assertIn("ERROR: release-delta input: tools/engine.py: ", output)
                self.assertIn("profile_keys has no value", output)
                self.assertNotIn("FLOOR:", output)
        for form, base, head in (
            ("private def body",
             "def _load():\n    pass\n",
             "def _load():\n    profile_keys: set\n"),
            ("public def inside a private class",
             "class _Holder:\n    def load(self):\n        pass\n",
             "class _Holder:\n    def load(self):\n        profile_keys: set\n"),
        ):
            with self.subTest(form=form):
                code, output = self.patch_claim_case(base, head)
                self.assertEqual(code, 0, output)
                self.assertIn("FLOOR: PATCH", output)
                self.assertNotIn("has no value", output)
                self.assertNotIn("accepted-key set", output)

    def test_private_nested_header_read_in_enclosing_scope(self):
        # A header of a private (underscore) def or class nested in a public def or class runs
        # in the scope around it, so an assignment expression there is a declaration of the
        # outermost public def or class; only the private body is skipped. Without a del of the
        # owner the removed key gives MAJOR; with one, the shared declaration fails closed.
        walrus = "(profile_keys := {'a', 'b'})"
        compiled = [
            ("def default", "pub", f"def pub():\n    def _h(x={walrus}):\n        pass\n"),
            ("def keyword-only default", "pub",
             f"def pub():\n    def _h(*, x={walrus}):\n        pass\n"),
            ("def decorator", "pub", f"def pub():\n    @{walrus}.copy\n    def _h():\n        pass\n"),
            ("async def default", "pub",
             f"def pub():\n    async def _h(x={walrus}):\n        pass\n"),
            ("class base", "pub", f"def pub():\n    class _C({walrus}.__class__):\n        pass\n"),
            ("class keyword", "pub", f"def pub():\n    class _C(x={walrus}):\n        pass\n"),
            ("class decorator", "pub",
             f"def pub():\n    @{walrus}.copy\n    class _C:\n        pass\n"),
            ("method default", "Pub", f"class Pub:\n    def _m(self, x={walrus}):\n        pass\n"),
            ("class base in a class", "Outer",
             f"class Outer:\n    class _Inner({walrus}.__class__):\n        pass\n"),
            ("lambda in a private def default", "pub",
             f"def pub():\n    def _h(x=lambda: {walrus}):\n        pass\n"),
        ]
        for form, owner, base in compiled:
            for tail, expected in (("", "MAJOR"), (f"del {owner}\n", "shared")):
                with self.subTest(form=form, released=bool(tail)):
                    self.release_case(base + tail, expected, owner)
        # Python refuses an assignment expression in an annotation or a type parameter, so these
        # headers fail closed (exit 2) through the compile; with the owner deleted, the release
        # of the owner of a shared declaration fails closed first.
        refused = [
            ("def argument annotation", "pub",
             f"def pub():\n    def _h(x: {walrus}):\n        pass\n"),
            ("def return annotation", "pub",
             f"def pub():\n    def _h() -> {walrus}:\n        pass\n"),
            ("def type parameter bound", "pub",
             f"def pub():\n    def _h[T: {walrus}]():\n        pass\n"),
            ("def type parameter default", "pub",
             f"def pub():\n    def _h[T = {walrus}]():\n        pass\n"),
            ("class type parameter bound", "pub",
             f"def pub():\n    class _C[T: {walrus}]:\n        pass\n"),
        ]
        for form, owner, base in refused:
            for tail in ("", f"del {owner}\n"):
                with self.subTest(form=form, released=bool(tail)), self.repo() as repo:
                    repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + base + tail)
                    repo.version("1.2.4")
                    code, output = self.result(repo)
                    self.assertEqual(code, 2, output)
                    if tail:
                        self.assertIn(f"ERROR: release-delta input: tools/engine.py: the release"
                                      f" of {owner}, which owns accepted keys, cannot be read as"
                                      " certain", output)
                    else:
                        self.assertIn("ERROR: release-delta input: tools/engine.py: invalid"
                                      " Python: ", output)
                        self.assertIn("named expression cannot be used within", output)
                    self.assertNotIn("FLOOR:", output)

    def test_lambda_local_declaration_never_hides_a_removal(self):
        # An assignment expression in a lambda body inside a public def or a class comprehension
        # binds a lambda local; it is still read as a declaration, but it never hides the
        # removal of a key an assignment held, in the base, the head or both (MAJOR, exit 1).
        known = "_known_keys = {'a', 'b'}\n"
        lambdas = [
            ("lambda in a lambda in a public def",
             "def f():\n    g = lambda: (lambda: (profile_keys := {'b'}))\n"),
            ("lambda in a public def", "def f():\n    g = lambda: (profile_keys := {'b'})\n"),
            ("lambda in a class comprehension",
             "class C:\n    values = [(lambda: (profile_keys := {'b'})) for x in ()]\n"),
        ]
        for form, extra in lambdas:
            for side, base, head in (
                    ("in base and head", known + extra, known.replace("'a', 'b'", "'a'") + extra),
                    ("in head only", known, known.replace("'a', 'b'", "'a'") + extra)):
                with self.subTest(form=form, side=side):
                    code, output = self.patch_claim_case(base, head)
                    self.assertEqual(code, 1, output)
                    self.assertIn("FLOOR: MAJOR", output)
                    self.assertIn("accepted-key set module: removed b", output)
            # A key removed from the lambda-local declaration itself is still a removal.
            with self.subTest(form=form, side="lambda key removed"):
                base = "_known_keys = {'a'}\n" + extra.replace("{'b'}", "{'a', 'b'}")
                code, output = self.patch_claim_case(base, "_known_keys = {'a'}\n" + extra.replace(
                    "{'b'}", "{'a'}"))
                self.assertEqual(code, 1, output)
                self.assertIn("accepted-key set module: removed b", output)
            # A key removed from an assignment expression in a private def default is a
            # removal too: with the lambda-local declaration holding it in the head, only
            # the view outside lambda bodies, which reads that default and leaves the
            # lambda body out, reports it, so the case fails without that view.
            held = "def k():\n    def _h(x=(profile_keys := {'a', 'b'})):\n        pass\n"
            for side, base, head in (
                    ("private default walrus, lambda in base and head", held + extra,
                     held.replace("'a', 'b'", "'a'") + extra),
                    ("private default walrus, lambda in head only", held,
                     held.replace("'a', 'b'", "'a'") + extra)):
                with self.subTest(form=form, side=side):
                    code, output = self.patch_claim_case(base, head)
                    self.assertEqual(code, 1, output)
                    self.assertIn("FLOOR: MAJOR", output)
                    self.assertIn("accepted-key set module: removed b", output)

    def test_lambda_local_declaration_never_hides_a_walrus_removal(self):
        # A lambda-local declaration in a public def never hides the removal of a key from an
        # assignment expression outside every lambda body, in the def body or in a private
        # header: the view outside lambda bodies (_KEY_VIEWS) reports it (MAJOR, exit 1).
        unused = "    unused = lambda: (profile_keys := {'b'})\n"
        walrus_return = "def f():\n    return (profile_keys := {'a', 'b'})\n"
        for form, base, head in (
            ("unused lambda beside a walrus return", walrus_return,
             "def f():\n" + unused + "    return (profile_keys := {'a'})\n"),
            ("nested lambda beside a walrus return", walrus_return,
             "def f():\n    unused = lambda: (lambda: (profile_keys := {'b'}))\n"
             "    return (profile_keys := {'a'})\n"),
            ("unused lambda beside a walrus in a private def default",
             "def f():\n    def _h(x=(profile_keys := {'a', 'b'})):\n        pass\n",
             "def f():\n" + unused + "    def _h(x=(profile_keys := {'a'})):\n        pass\n"),
        ):
            with self.subTest(form=form):
                code, output = self.patch_claim_case(base, head)
                self.assertEqual(code, 1, output)
                self.assertIn("FLOOR: MAJOR", output)
                self.assertIn("accepted-key set module: removed b", output)
        # A lambda added beside an unchanged walrus removes nothing (PATCH, exit 0).
        with self.subTest(form="lambda added beside an unchanged walrus"):
            code, output = self.patch_claim_case(
                walrus_return, "def f():\n" + unused + "    return (profile_keys := {'a', 'b'})\n")
            self.assertEqual(code, 0, output)
            self.assertIn("FLOOR: PATCH", output)
            self.assertNotIn("accepted-key set", output)

    def test_moving_a_key_between_an_assignment_and_an_assignment_expression(self):
        # An assignment and an assignment expression in a public def that hold the same keys
        # differ only in the assignments-only view (_KEY_VIEWS), so moving a key between them
        # is reported only through that view.
        walrus_return = "def f():\n    return (profile_keys := {'a', 'b'})\n"
        # Moving a declaration from an assignment to an assignment expression is a removal in
        # the assignments-only view (MAJOR, exit 1), although the walrus holds the same keys.
        with self.subTest(form="assignment moved to a walrus"):
            code, output = self.patch_claim_case(
                "def f():\n    profile_keys = {'a', 'b'}\n", walrus_return)
            self.assertEqual(code, 1, output)
            self.assertIn("FLOOR: MAJOR", output)
            self.assertIn("accepted-key set module: removed a", output)
            self.assertIn("accepted-key set module: removed b", output)
        # The reverse move is an addition in that view (MINOR, exit 1).
        with self.subTest(form="walrus moved to an assignment"):
            code, output = self.patch_claim_case(
                walrus_return, "def f():\n    profile_keys = {'a', 'b'}\n")
            self.assertEqual(code, 1, output)
            self.assertIn("FLOOR: MINOR", output)
            self.assertIn("accepted-key set module: added a", output)
            self.assertNotIn("removed", output)

    def test_release_level_table(self):
        # Every row of the release-level table (_RELEASE_CASES) runs through check() with a
        # PATCH claim (1.2.3 to 1.2.4) and gives the outcome the row states. A refused base
        # stops the check before it reads the head, so each exit 2 head also runs alone
        # against the accepted engine module, each refused base runs alone against it, and the
        # head of an "exit 2, base refused" row must be accepted when it runs alone.
        codes = {"PATCH": 0, "MINOR": 1, "MAJOR": 1, "exit 2": 2, "exit 2, base refused": 2}
        self.assertTrue(DELTA._RELEASE_CASES)

        def run(base, head):
            with self.repo() as repo:
                repo.write("tools/engine.py", ENGINE + "\n" + base)
                repo.checkpoint()
                repo.write("tools/engine.py", ENGINE + "\n" + head)
                repo.version("1.2.4")
                return self.result(repo)

        def refused(code, output):
            self.assertEqual(code, 2, output)
            self.assertIn("ERROR: release-delta input: tools/engine.py: ", output)
            self.assertNotIn("FLOOR:", output)

        def base_refused(base):
            try:
                DELTA._api((ENGINE + "\n" + base).encode("utf-8"), "tools/engine.py")
            except ValueError:
                return True
            return False

        for change, place, base, head, outcome in DELTA._RELEASE_CASES:
            with self.subTest(change=change, place=place):
                code, output = run(base, head)
                self.assertEqual(code, codes[outcome], output)
                if outcome.startswith("exit 2"):
                    refused(code, output)
                else:
                    self.assertIn(f"FLOOR: {outcome}\n", output)
                    self.assertIn("CLAIMED: PATCH", output)
                    self.assertFalse(base_refused(base), base)
                if outcome == "exit 2":
                    # The head is refused on its own, whatever the base.
                    with self.subTest(side="head alone"):
                        refused(*run("", head))
                    if base_refused(base):
                        with self.subTest(side="base alone"):
                            refused(*run(base, ""))
                elif outcome == "exit 2, base refused":
                    self.assertTrue(base_refused(base), base)
                    with self.subTest(side="base alone"):
                        refused(*run(base, ""))
                    with self.subTest(side="head alone"):
                        code, output = run("", head)
                        self.assertNotEqual(code, 2, output)
                        self.assertIn("FLOOR: ", output)

    def test_unpacking_del_in_a_body_names_its_form(self):
        # A del of a name inside a tuple or list target in a public def body names that form,
        # as the top-level reading does; a del of the plain name keeps its own message.
        owner = "def load():\n    profile_keys = {'a'}\n"
        for target, construct in (
            ("(load,)", "a del (inside a tuple, list or starred target) in a def or class body"),
            ("[load]", "a del (inside a tuple, list or starred target) in a def or class body"),
            ("load", "a del in a def or class body"),
        ):
            with self.subTest(target=target):
                with self.assertRaises(ValueError) as caught:
                    DELTA._api((owner + f"def f():\n    del {target}\n").encode("utf-8"),
                               "tools/engine.py")
                self.assertIn(f"f.load, a key-owning name, is bound or deleted by {construct},",
                              str(caught.exception))

    def test_uncertain_release_of_a_key_named_name_names_its_cause(self):
        # A key-named name that owns no declarations, bound or deleted by a construct the
        # check reads as an uncertain release, fails closed (exit 2) with a message that names
        # the construct and says the check reads it as an uncertain release, not as a place
        # it does not read. A place the check does not read keeps its own message.
        expected = ("tools/engine.py: profile_keys, a key-named name that owns no accepted-key"
                    " declarations, is bound or deleted by {}, which the check reads as an"
                    " uncertain release, not as a declaration or a certain release; the check"
                    " cannot decide the floor")
        for form, source, construct in (
            ("top-level for target", "for profile_keys in ():\n    pass\n", "a for target"),
            ("for target inside a compound statement",
             "if True:\n    for profile_keys in ():\n        pass\n",
             "a for target inside a compound statement"),
            ("except name", "try:\n    pass\nexcept OSError as profile_keys:\n    pass\n",
             "an except name"),
            ("match capture", "match 1:\n    case profile_keys:\n        pass\n",
             "a match capture"),
            ("type statement", "type profile_keys = int\n", "a type statement"),
            ("del inside a compound statement", "if False:\n    del profile_keys\n",
             "a del inside a compound statement"),
        ):
            with self.subTest(form=form):
                with self.assertRaises(ValueError) as caught:
                    DELTA._api(source.encode("utf-8"), "tools/engine.py")
                self.assertEqual(str(caught.exception), expected.format(construct))
        with self.subTest(form="place the check does not read"):
            with self.assertRaises(ValueError) as caught:
                DELTA._api(b"for profile_keys, _y in ():\n    pass\n", "tools/engine.py")
            self.assertEqual(str(caught.exception),
                             "tools/engine.py: profile_keys, a key-owning name, is bound or"
                             " deleted by a for target (inside a tuple, list or starred target),"
                             " a place the check does not read; the check cannot decide the"
                             " floor")
        with self.subTest(form="exit 2 through the check"), self.repo() as repo:
            repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n"
                       + "for profile_keys in ({'a', 'b'},):\n    pass\n")
            repo.checkpoint()
            repo.replace("tools/engine.py", "{'a', 'b'}", "{'a'}")
            repo.version("1.2.4")
            code, output = self.result(repo)
            self.assertEqual(code, 2, output)
            self.assertIn(expected.format("a for target"), output)
            self.assertNotIn("a place the check does not read", output)
            self.assertNotIn("FLOOR:", output)

    def test_over_refusal_sentence_names_every_body_construct(self):
        # The sentence on the deliberate over-refusal for a name that is not key-named is
        # read from the rule section of the module docstring, the one text of the accepted-key
        # rule: it names the key-owning name that is not key-named in a public def or class
        # body and points to the release-level table, and the table has an exit 2 row, which
        # test_release_level_table runs through the check, for every construct that fails
        # closed for such a name in a public def or class body. The _api docstring, the module
        # comments, src/README.md and the specification each point to that section by name
        # and do not restate the sentence.
        opening = "For a name that is not key-named this is a deliberate over-refusal"
        sentences = [sentence for sentence in _sentences(_rule_section())
                     if opening in sentence]
        self.assertEqual(len(sentences), 1, sentences)
        self.assertIn("_RELEASE_CASES", sentences[0])
        self.assertIn("for a key-owning name that is not key-named in a public def or class"
                      " body", sentences[0])
        source = (TOOLS / "pack_release_delta.py").read_text(encoding="utf-8")
        texts = {
            "_api": DELTA._api.__doc__,
            "module comment": "\n".join(line.strip()[1:] for line in source.splitlines()
                                        if line.strip().startswith("#")),
            "README": (TOOLS.parent / "README.md").read_text(encoding="utf-8"),
            "specification": (TOOLS.parents[1] / "specs" / "specification-audit-programme.md"
                              ).read_text(encoding="utf-8"),
        }
        for name, text in texts.items():
            with self.subTest(text=name):
                doc = " ".join(text.split())
                self.assertIn(f'section "{_RULE_TITLE}"', doc)
                self.assertNotIn(opening, doc)
        rows = [change for change, place, base, _head, outcome in DELTA._RELEASE_CASES
                if outcome == "exit 2" and base == DELTA._OWNER
                and change.startswith("key-owning name ")
                and place in ("a public def body", "a public async def body", "a public class body")]
        for construct in ("a nested def", "a nested async def", "a nested class",
                          "a def (a method", "a for target", "an async for target",
                          "a with target", "an async with target", "an except name",
                          "a match capture", "an import", "a del", "an augmented assignment",
                          "a type statement", "a tuple target", "a starred target"):
            with self.subTest(construct=construct):
                self.assertTrue(any(construct in change for change in rows), construct)
        # The constructs refused for such a name are also taken from the walker's own code
        # (_walker_requirements), so a construct added there without a row fails here: each
        # must be named by the refusal of the head of an exit 2 row whose base is the
        # key-owning owner that is not key-named, in a public def, async def or class body.
        over_refused = _walker_requirements()[0]
        refusals = [(change, message) for change, place, base, _head, message
                    in _table_refusals()
                    if base == DELTA._OWNER and change.startswith("key-owning name ")
                    and place in ("a public def body", "a public async def body",
                                  "a public class body")]
        for construct in sorted(over_refused):
            with self.subTest(derived=construct):
                self.assertTrue(any(f"is bound or deleted by {construct}, a place" in message
                                    for _change, message in refusals), construct)

    def test_release_level_table_is_complete(self):
        # The table holds a row for every pair the documentation sends readers to it for, and
        # the pairs are derived, not listed by hand: each construct the walker names when a
        # public def or class body binds or deletes a name at a place the check does not read
        # (read from the module by _walker_requirements), each node type and each unpacking
        # (statement, target) form that produces such a construct, and each module-level
        # change between binding forms (_binding_form_pairs). A refusal row covers a construct
        # when its head alone is refused with a message naming it; a binding-form pair is
        # covered by a row with that base and head. test_release_level_table runs each row.
        over_refused, key_named_only, nodes, targets = _walker_requirements()
        refusals = _table_refusals()

        def heads(construct, owner_only):
            return [ast.parse(head) for _change, _place, base, head, message in refusals
                    if f"is bound or deleted by {construct}, a place" in message
                    and (not owner_only or base == DELTA._OWNER)]

        missing = []
        for construct in sorted(over_refused):
            if not heads(construct, True):
                missing.append(f"refused for a key-owning name that is not key-named: {construct}")
        for construct in sorted(key_named_only):
            if not heads(construct, False):
                missing.append(f"refused for a key-named name: {construct}")
        for type_name, constructs in sorted(nodes.items()):
            kind = getattr(ast, type_name)
            if not any(isinstance(node, kind) for construct in constructs
                       for tree in heads(construct, False) for node in ast.walk(tree)):
                missing.append(f"a {type_name} node refused as "
                               + " or ".join(sorted(constructs)))
        for (statement_types, target_type), construct in sorted(targets.items()):
            statements = tuple(getattr(ast, name) for name in statement_types)
            if not any(isinstance(node, statements)
                       and any(isinstance(target, getattr(ast, target_type))
                               for target in [*_statement_targets(node),
                                              *getattr(node, "handlers", ())])
                       for tree in heads(construct, True) for node in ast.walk(tree)):
                missing.append(f"a {target_type} target of a {' or '.join(statement_types)}"
                               f" refused as {construct}")
        rows = {(base, head) for _change, _place, base, head, _outcome in DELTA._RELEASE_CASES}
        for change, base, head in _binding_form_pairs():
            if (base, head) not in rows:
                missing.append(f"{change}: {base!r} to {head!r}")
        self.assertFalse(missing, f"{len(missing)} pair(s) without a row:\n" + "\n".join(missing))

    def test_binding_event_pairs_have_rows(self):
        # Every construct _binding_events and the functions inside it pass to add or target
        # (read from the module by _event_requirements, not typed here) has an exit 2 row
        # whose head alone is refused with a message naming it, for each statement type and
        # each target type apart: the head holds a node of that statement type whose target of
        # that type binds or deletes the refused name, so the row exercises that form.
        requirements = _event_requirements()
        refusals = _table_refusals()
        derived = set().union(*requirements.values())
        for construct in sorted(_PARSER_UNREACHABLE):
            with self.subTest(unreachable=construct):
                self.assertIn(construct, derived)
        missing = _event_pairs_without_rows(requirements, refusals)
        self.assertFalse(missing, f"{len(missing)} pair(s) without a refusing row:\n"
                         + "\n".join(missing))

    def test_binding_pair_guard_matches_the_refused_name_to_the_target(self):
        # A row covers a (statement, target) pair only when the target of that type binds or
        # deletes the name the refusal names, never another name that happens to appear in
        # the message (the article "a" of "a key-owning name", for example). Each refusing
        # row whose head binds a name inside a list target of an assignment is rewritten to a
        # tuple target, and an unrelated list-target assignment of another name is appended
        # to its head; no row then covers an assignment with a list target, so the guard must
        # report that pair, while the unchanged table leaves it covered.
        requirements = _event_requirements()
        self.assertIn(("Assign", "List"), requirements)
        refusals = _table_refusals()
        self.assertFalse([pair for pair in _event_pairs_without_rows(requirements, refusals)
                          if pair.startswith("Assign / List: ")])
        rewritten = []
        changed = 0
        for change, place, base, head, message in refusals:
            tree = ast.parse(head)
            found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for index, target in enumerate(node.targets):
                        if isinstance(target, ast.List):
                            node.targets[index] = ast.Tuple(elts=target.elts, ctx=ast.Store())
                            found = True
            if found:
                changed += 1
                head = ast.unparse(tree) + "\n[a] = [0]\n"
                self.assertIn("a", _bound_by(ast.parse(head).body[-1]))
                try:
                    DELTA._api((ENGINE + "\n" + head).encode("utf-8"), "tools/engine.py")
                except ValueError as exc:
                    message = str(exc)
                else:
                    message = ""
            rewritten.append((change, place, base, head, message))
        self.assertTrue(changed)
        missing = _event_pairs_without_rows(requirements, rewritten)
        self.assertTrue([pair for pair in missing if pair.startswith("Assign / List: ")],
                        missing)

    def test_binding_pair_guard_ignores_names_the_target_does_not_bind(self):
        # A target binds only the stored or deleted names reached through its tuple, list and
        # starred elements; a name read inside a subscript, attribute or call within the target
        # (or bound by an assignment expression there) is not bound by that target. Here the
        # tuple target is what the check refuses, and the list target either reads the refused
        # name or binds it through an assignment expression inside a subscript, never as one
        # of its own elements, so the row covers the tuple pair and never the list pair.
        construct = "an assignment (inside a tuple, list or starred target)"
        requirements = _event_requirements()
        self.assertIn(construct, requirements[("Assign", "List")])
        self.assertIn(construct, requirements[("Assign", "Tuple")])
        for reader in ("_sink[_profile_keys]", "_sink[_profile_keys].field",
                       "_sink[call(_profile_keys)]", "_sink[(_profile_keys := 1)]"):
            head = f"(_profile_keys,) = (None,)\n[{reader}] = [0]\n"
            with self.subTest(head=head):
                with self.assertRaises(ValueError) as caught:
                    DELTA._api((ENGINE + "\n" + head).encode("utf-8"), "tools/engine.py")
                message = str(caught.exception)
                self.assertEqual(_refused_name(message), "_profile_keys")
                self.assertTrue(_refusal_names(message, construct), message)
                self.assertTrue(_holds(head, message, "Assign", "Tuple"))
                self.assertFalse(_holds(head, message, "Assign", "List"))
                missing = _event_pairs_without_rows(
                    {("Assign", "List"): {construct}}, [("read", "module", "", head, message)])
                self.assertEqual(missing, [f"Assign / List: {construct}"])

    def test_release_levels_outside_the_table_are_pointers(self):
        # README, the specification and the _api docstring state no release level (PATCH,
        # MINOR, MAJOR or exit 2) for a construct whose level the release-level table holds,
        # except in a pointer sentence: one that names _RELEASE_CASES and does not itself say
        # that the construct counts as a level. A sentence is matched by the construct phrases
        # below, each of which has rows in the table.
        constructs = ("inline set", "later add", "later `add`", "|=", "__all__", "import alias",
                      "alias by import", "alias made by import", "walrus", "globals()",
                      "annotation without a value", "breaking-shaped", "unseen binding",
                      "other place that binds or deletes")
        level = re.compile(r"(?<![A-Za-z])(PATCH|MINOR|MAJOR)(?![A-Za-z])|exit \(?2")
        predicate = re.compile(r"counts?( only)? as (PATCH|MINOR|MAJOR)")
        texts = {
            "_api": DELTA._api.__doc__,
            "README": (TOOLS.parent / "README.md").read_text(encoding="utf-8"),
            "specification": (TOOLS.parents[1] / "specs" / "specification-audit-programme.md"
                              ).read_text(encoding="utf-8"),
        }
        found = []
        for name, text in texts.items():
            for sentence in re.split(r"(?<=\.)\s+(?=[A-Z`*])", " ".join(text.split())):
                if not level.search(sentence) or not any(c in sentence for c in constructs):
                    continue
                if "_RELEASE_CASES" not in sentence or predicate.search(sentence):
                    found.append(f"{name}: {sentence[:160]}")
        self.assertFalse(found, f"{len(found)} level statement(s) outside a pointer:\n"
                         + "\n".join(found))

    def test_level_guard_reads_comments_docstrings_and_release_history(self):
        # A level sentence in any comment or docstring of pack_release_delta.py, anywhere in
        # src/README.md (its release history included), or anywhere in the skill body
        # (src/core/skill/SKILL.md) is found; a release history entry that only points to the
        # specification's gate 99 rules is not. The rule section of the module docstring
        # gives no level, and a level planted in it is found.
        source = (TOOLS / "pack_release_delta.py").read_text(encoding="utf-8")
        section = _rule_section(source)
        self.assertIn("What the check does not see.", section)
        self.assertFalse([s for s in _sentences(section) if _LEVEL.search(s)])
        readme = (TOOLS.parent / "README.md").read_text(encoding="utf-8")
        skill = (TOOLS.parent / "core" / "skill" / "SKILL.md").read_text(encoding="utf-8")
        tooling = "## Tooling\n"
        planted = "Adding a public def needs a MINOR."
        history = "## Release history\n"
        check_doc = '"""Print the release-delta report; return 0, 1 or 2 without writing files.'
        plants = {
            "module comment": {"module_source": source.replace(
                "\n_OWNER = ", "\n# " + planted + "\n_OWNER = ", 1)},
            "docstring": {"module_source": source.replace(
                check_doc, check_doc + " " + planted, 1)},
            "rule section": {"module_source": source.replace(
                "What the check does not see.",
                planted + " What the check does not see.", 1)},
            "release history": {"readme": readme.replace(
                history, history + "- **9.9.9:** " + planted + "\n", 1)},
            "skill body": {"skill": skill.replace(
                tooling, tooling + "\n" + planted + "\n", 1)},
        }
        self.assertFalse(_level_statements(module_source=source, readme=readme, skill=skill))
        for name, texts in plants.items():
            with self.subTest(name):
                self.assertNotEqual((texts.get("module_source", source),
                                     texts.get("readme", readme), texts.get("skill", skill)),
                                    (source, readme, skill))
                found = _level_statements(**texts)
                self.assertTrue(any(planted in finding for finding in found), found)
        self.assertIn(planted, _rule_section(plants["rule section"]["module_source"]))
        pointer = ("- **9.9.9:** the PATCH, MINOR or MAJOR level of each change is stated in "
                   "`specs/specification-audit-programme.md`, section 6, gate 99.\n")
        self.assertFalse(_level_statements(readme=readme.replace(history, history + pointer, 1)))

    def test_release_levels_are_stated_once_in_the_specification(self):
        # The specification states each general release-level rule (PATCH, MINOR, MAJOR or an
        # exit 2 refusal for a kind of change) once, pointing to the table rows that exercise
        # it. src/README.md (its release history included), the skill body
        # (src/core/skill/SKILL.md) and every comment and docstring
        # of pack_release_delta.py state no level outside a pointer sentence to the
        # specification, whatever construct a sentence
        # names, and the specification gives no engine construct a level without naming its
        # rows of the release-level table (or the test that runs a case too large for it).
        found = _level_statements()
        self.assertFalse(found, f"{len(found)} release-level statement(s) out of place:\n"
                         + "\n".join(found))
        # Each general rule's own rows exist in the table and the specification names them.
        spec = " ".join((TOOLS.parents[1] / "specs" / "specification-audit-programme.md"
                         ).read_text(encoding="utf-8").split())
        changes = {change for change, *_rest in DELTA._RELEASE_CASES}
        for change in ("public name added", "public def added", "public class added",
                       "public def removed", "public def renamed to a private name",
                       "public name changed from a def to a class",
                       "public name changed from an assignment to a def",
                       "parameter removed", "parameter added",
                       "counted public name deleted by a top-level del",
                       "counted public name deleted by a top-level del and bound again by an"
                       " assignment",
                       "counted public name deleted by a top-level del and bound again by a def",
                       "public name bound by a def and by an assignment",
                       "key-owning name released while the module refers to it",
                       "key-owning name bound twice in one statement",
                       "key-owning declaration shared by a chained assignment, then released",
                       "star import added", "changed value, key removed",
                       "walrus to a *_keys name, key added to its value"):
            with self.subTest(change=change):
                self.assertIn(change, changes)
                self.assertIn(f'"{change}"', spec)
        # The accepted-key rules those key rows exercise are read from the rule section of
        # the module docstring, which gives no level itself; the specification points to it.
        section = _rule_section()
        self.assertTrue(section)
        self.assertFalse([s for s in _sentences(section) if _LEVEL.search(s)])
        self.assertIn(f'section "{_RULE_TITLE}"', spec)
        for change, rule in (
                ("changed value, key removed", "a key is reported removed"),
                ("walrus to a *_keys name, key added to its value",
                 "and added when some view holds it"),
                ("*_keys name bound by an assignment renamed",
                 "renaming a key-set variable is not a removal of an accepted key"),
                ("key-owning name released while the module refers to it",
                 "when the module refers to that name anywhere"),
                ("key-owning name bound twice in one statement",
                 "must be bound exactly once in the statement that makes them"),
                ("key-owning declaration shared by a chained assignment, then released",
                 "as a chained assignment does"),
                ("star import added", "a star import, at any depth"),
                ("keys of a released name removed later through a reference the check does"
                 " not see", "a later removal of those keys is not reported")):
            with self.subTest(rule=change):
                self.assertIn(change, changes)
                self.assertIn(rule, section.lower())

    def test_accepted_key_rule_is_stated_once_in_the_module_docstring(self):
        # The accepted-key rule is read from the module docstring, not typed here: its titled
        # section holds the rule phrases, and src/README.md and the specification point to the
        # section by name and restate none of it. A missing pointer or an added restatement in
        # either document is found.
        found = _accepted_key_rule_problems()
        self.assertFalse(found, f"{len(found)} problem(s) with the one rule text:\n"
                         + "\n".join(found))
        readme = (TOOLS.parent / "README.md").read_text(encoding="utf-8")
        spec = (TOOLS.parents[1] / "specs" / "specification-audit-programme.md"
                ).read_text(encoding="utf-8")
        title = f'section "{_RULE_TITLE}"'
        planted = "\nOnly these places that bind or delete a module name are read.\n"
        for name, texts in (("README pointer", {"readme": readme.replace(title, "", 1)}),
                            ("spec pointer", {"spec": spec.replace(title, "", 1)}),
                            ("README restatement", {"readme": readme + planted}),
                            ("spec restatement", {"spec": spec + planted})):
            with self.subTest(name):
                self.assertTrue(_accepted_key_rule_problems(**texts))

    def test_over_refusal_sentence_names_the_key_named_only_exception(self):
        # The rule section of the module docstring calls the refusal of a name that is not
        # key-named a deliberate over-refusal for every construct it lists, and the _api
        # docstring points to that section. The walker refuses a nonlocal statement
        # in a def or class body for a key-named name only and accepts one naming any other
        # name, so the sentence must name that exception rather than claim a refusal the code
        # does not make.
        self.assertIn("a nonlocal statement in a def or class body", _walker_requirements()[1])
        sentences = [sentence for sentence in _sentences(_rule_section())
                     if "deliberate over-refusal for every construct above" in sentence]
        self.assertEqual(len(sentences), 1, sentences)
        api = " ".join(DELTA._api.__doc__.split())
        self.assertIn(f'section "{_RULE_TITLE}"', api)
        self.assertNotIn("deliberate over-refusal for every construct above", api)
        self.assertIn("except a nonlocal statement, which is refused only for a key-named name",
                      sentences[0])

    def test_derived_body_constructs_have_class_body_rows(self):
        # A class body runs at class creation, not when a def is called, so each construct the
        # walker refuses in a public def or class body for a key-owning name that is not
        # key-named needs its own exit 2 row in a public class body, whose head alone is
        # refused with a message naming that construct.
        refusals = [message for change, place, base, _head, message in _table_refusals()
                    if base == DELTA._OWNER and place == "a public class body"]
        missing = [construct for construct in sorted(_walker_requirements()[0])
                   if not any(f"is bound or deleted by {construct}, a place" in message
                              for message in refusals)]
        self.assertFalse(missing, f"{len(missing)} construct(s) without a class body row:\n"
                         + "\n".join(missing))

    def test_refused_node_binds_the_refused_name(self):
        # For each node type of a named branch of the walker, some exit 2 row's head holds a
        # node of that type that itself binds or deletes the name the refusal names, so the
        # row exercises that node and not another binding of the name in the same head.
        _over, _key_named, nodes, _targets = _walker_requirements()
        refusals = _table_refusals()
        missing = []
        for type_name, constructs in sorted(nodes.items()):
            kind = getattr(ast, type_name)
            covered = False
            for _change, _place, _base, head, message in refusals:
                if not any(f"is bound or deleted by {construct}, a place" in message
                           for construct in constructs):
                    continue
                refused = re.search(r"([A-Za-z_][\w.]*), a key", message)
                if not refused:
                    continue
                name = refused.group(1).rsplit(".", 1)[-1]
                for node in ast.walk(ast.parse(head)):
                    if isinstance(node, kind) and name in _bound_by(node):
                        covered = True
            if not covered:
                missing.append(f"a {type_name} node binding the refused name, refused as "
                               + " or ".join(sorted(constructs)))
        self.assertFalse(missing, f"{len(missing)} node type(s) without a row:\n"
                         + "\n".join(missing))

    def test_unpacked_key_named_target_in_a_body_fails_closed(self):
        # A key-named name inside a tuple, list or starred target of an assignment, for or with
        # in a public def or class body is a place the check does not read, so it fails closed
        # (exit 2), in the base or the head, as it does in a top-level statement.
        for form, owner, body in (
            ("tuple", "def f():\n", "    profile_keys, x = {'a', 'b'}, 1\n"),
            ("parenthesized tuple", "def f():\n", "    (profile_keys, x) = {'a', 'b'}, 1\n"),
            ("list", "def f():\n", "    [profile_keys, x] = [{'a', 'b'}, 1]\n"),
            ("starred", "def f():\n", "    *profile_keys, = [{'a', 'b'}]\n"),
            ("nested tuple", "def f():\n", "    x, (y, profile_keys) = 1, (2, {'a', 'b'})\n"),
            ("inside an if", "def f():\n", "    if f:\n        profile_keys, x = {'a', 'b'}, 1\n"),
            ("for tuple", "def f():\n", "    for profile_keys, x in ():\n        pass\n"),
            ("async for tuple", "async def f():\n",
             "    async for profile_keys, x in f():\n        pass\n"),
            ("with tuple", "def f():\n", "    with f() as (profile_keys, x):\n        pass\n"),
            ("class body tuple", "class C:\n", "    profile_keys, x = {'a', 'b'}, 1\n"),
            ("method tuple", "class C:\n",
             "    def m(self):\n        profile_keys, x = {'a', 'b'}, 1\n"),
        ):
            for side in ("head", "base"):
                with self.subTest(form=form, side=side):
                    plain = owner + "    pass\n"
                    unpacked = owner + body
                    if side == "head":
                        code, output = self.patch_claim_case(plain, unpacked)
                    else:
                        # The head differs from the base, so the check reads both sides.
                        code, output = self.patch_claim_case(
                            unpacked, unpacked.replace("{'a', 'b'}", "{'a'}") + "# changed\n")
                    self.assertEqual(code, 2, output)
                    self.assertIn("ERROR: release-delta input: tools/engine.py: ", output)
                    self.assertIn("profile_keys, a key-owning name, is bound or deleted by a name"
                                  " inside a tuple, list or starred target", output)
                    self.assertNotIn("FLOOR:", output)
        # A comprehension target binds a name of the comprehension's own scope, and a private
        # body is skipped, so neither is refused (PATCH, exit 0).
        for form, head in (
            ("comprehension target", "def f():\n    return [x for profile_keys, x in ()]\n"),
            ("private def body",
             "def f():\n    pass\ndef _g():\n    profile_keys, x = {'a', 'b'}, 1\n"),
        ):
            with self.subTest(form=form):
                code, output = self.patch_claim_case("def f():\n    pass\n", head)
                self.assertEqual(code, 0, output)
                self.assertIn("FLOOR: PATCH", output)

    def test_plain_key_named_target_in_a_body_fails_closed(self):
        # In a public def or class body, outside every private body, a key-named plain name
        # that a for, async for, with or async with target, an except name, a match capture or
        # an import binds is a place the check does not read, so it fails closed (exit 2), in
        # the base or the head, as a tuple target there does.
        for form, owner, body, construct in (
            ("for", "def f():\n",
             "    for profile_keys in ({'a', 'b'},):\n        return profile_keys\n",
             "a for target"),
            ("async for", "async def f():\n",
             "    async for profile_keys in f():\n        pass\n", "an async for target"),
            ("with", "def f():\n", "    with f() as profile_keys:\n        pass\n",
             "a with target"),
            ("with second item", "def f():\n",
             "    with f() as x, f() as profile_keys:\n        pass\n", "a with target"),
            ("async with", "async def f():\n",
             "    async with f() as profile_keys:\n        pass\n", "an async with target"),
            ("except name", "def f():\n",
             "    try:\n        pass\n    except E as profile_keys:\n        pass\n",
             "an except name"),
            ("except star name", "def f():\n",
             "    try:\n        pass\n    except* E as profile_keys:\n        pass\n",
             "an except name"),
            ("match capture", "def f(x):\n",
             "    match x:\n        case profile_keys:\n            pass\n", "a match capture"),
            ("match as", "def f(x):\n",
             "    match x:\n        case [1] as profile_keys:\n            pass\n",
             "a match capture"),
            ("match star", "def f(x):\n",
             "    match x:\n        case [*profile_keys]:\n            pass\n",
             "a match capture"),
            ("match mapping rest", "def f(x):\n",
             "    match x:\n        case {**profile_keys}:\n            pass\n",
             "a match mapping rest"),
            ("import", "def f():\n", "    import profile_keys\n", "an import"),
            ("import as", "def f():\n", "    import os as profile_keys\n", "an import"),
            ("from import", "def f():\n", "    from os import profile_keys\n", "an import"),
            ("from import as", "def f():\n", "    from os import path as profile_keys\n",
             "an import"),
            ("inside an if", "def f():\n",
             "    if f:\n        for profile_keys in ():\n            pass\n", "a for target"),
            ("nested public def", "def f():\n",
             "    def g():\n        import profile_keys\n", "an import"),
            ("class body for", "class C:\n", "    for profile_keys in ():\n        pass\n",
             "a for target"),
            ("method with", "class C:\n",
             "    def m(self):\n        with f() as profile_keys:\n            pass\n",
             "a with target"),
        ):
            for side in ("head", "base"):
                with self.subTest(form=form, side=side):
                    plain = owner + "    pass\n"
                    bound = owner + body
                    if side == "head":
                        code, output = self.patch_claim_case(plain, bound)
                    else:
                        # The head differs from the base, so the check reads both sides.
                        code, output = self.patch_claim_case(
                            bound, bound.replace("{'a', 'b'}", "{'a'}") + "# changed\n")
                    self.assertEqual(code, 2, output)
                    self.assertIn("ERROR: release-delta input: tools/engine.py: ", output)
                    self.assertIn("profile_keys, a key-owning name, is bound or deleted by "
                                  + construct + " in a def or class body, a place the check"
                                  " does not read", output)
                    self.assertNotIn("FLOOR:", output)
        # A comprehension target binds a name of the comprehension's own scope, and a private
        # body is skipped, so neither is refused (PATCH, exit 0).
        private_body = (
            "    for profile_keys in ():\n        pass\n"
            "    async for profile_keys in f():\n        pass\n"
            "    with f() as profile_keys:\n        pass\n"
            "    async with f() as profile_keys:\n        pass\n"
            "    try:\n        pass\n    except E as profile_keys:\n        pass\n"
            "    match x:\n        case [*profile_keys]:\n            pass\n"
            "        case {**profile_keys}:\n            pass\n"
            "        case profile_keys:\n            pass\n"
            "    import profile_keys\n    from os import path as profile_keys\n")
        for form, head in (
            ("private def body", "def f():\n    pass\nasync def _g(x):\n" + private_body),
            ("private def body nested in a public def",
             "def f():\n    async def _g(x):\n"
             + private_body.replace("\n    ", "\n        ").replace("    for", "        for", 1)),
            ("private method body", "class C:\n    async def _m(self, x):\n"
             + private_body.replace("\n    ", "\n        ").replace("    for", "        for", 1)),
            ("comprehension target", "def f():\n    return [x for profile_keys in ()]\n"),
            ("async comprehension target",
             "async def f():\n    return [x async for profile_keys in f()]\n"),
        ):
            with self.subTest(form=form):
                # The base binds the same public owner, so only the private body or the
                # comprehension is new.
                code, output = self.patch_claim_case(head.split("\n")[0] + "\n    pass\n", head)
                self.assertEqual(code, 0, output)
                self.assertIn("FLOOR: PATCH", output)

    def test_public_body_binding_forms_fail_closed(self):
        # In a public def or class body, outside every private body, a key-owning name that a
        # del deletes, or that an augmented assignment, a type statement or a nested def, async
        # def or class (a private one included) binds, is a place the check does not read, and
        # so is a key-named nonlocal statement anywhere inside a public def or class body, a
        # private body nested in it included; each fails closed (exit 2), in the base or the
        # head.
        declared = "    profile_keys = {'a', 'b'}\n"
        for form, owner, body, name, construct in (
            ("del", "def f():\n", declared + "    del profile_keys\n", "profile_keys", "a del"),
            ("del then rebind", "def f():\n",
             declared + "    del profile_keys\n    profile_keys = {'a'}\n", "profile_keys",
             "a del"),
            ("del of a tuple", "def f():\n", declared + "    del (x, profile_keys)\n",
             "profile_keys", "a del (inside a tuple, list or starred target)"),
            ("augmented assignment", "def f():\n", declared + "    profile_keys |= {'c'}\n",
             "profile_keys", "an augmented assignment"),
            ("augmented assignment alone", "def f():\n", "    profile_keys |= {'a', 'b'}\n",
             "profile_keys", "an augmented assignment"),
            ("type statement", "def f():\n", "    type profile_keys = int\n", "profile_keys",
             "a type statement"),
            ("nested def", "def f():\n", "    def profile_keys():\n        return {'a', 'b'}\n",
             "profile_keys", "a def"),
            ("nested async def", "def f():\n",
             "    async def profile_keys():\n        return {'a', 'b'}\n", "profile_keys",
             "an async def"),
            ("nested class", "def f():\n", "    class profile_keys:\n        pass\n",
             "profile_keys", "a class"),
            ("nested private def", "def f():\n",
             "    def _profile_keys():\n        return {'a', 'b'}\n", "_profile_keys", "a def"),
            ("method named keys", "class C:\n", "    def keys(self):\n        return {'a', 'b'}\n",
             "C.keys", "a def"),
            ("nonlocal from a nested private body", "def f():\n",
             declared + "    def _g():\n        nonlocal profile_keys\n        del profile_keys\n",
             "profile_keys", "a nonlocal statement"),
            ("nonlocal from a private method of a nested private class", "def f():\n",
             declared + "    class _C:\n        def _m(self):\n            nonlocal profile_keys\n"
             "            profile_keys = set()\n", "profile_keys", "a nonlocal statement"),
            ("nonlocal from a nested public def", "def f():\n",
             declared + "    def g():\n        nonlocal profile_keys\n"
             "        profile_keys = {'a', 'b'}\n", "profile_keys", "a nonlocal statement"),
            ("inside an if", "def f():\n", declared + "    if f:\n        del profile_keys\n",
             "profile_keys", "a del"),
            ("class body del", "class C:\n", "    profile_keys = {'a', 'b'}\n    del profile_keys\n",
             "profile_keys", "a del"),
            ("class body augmented assignment", "class C:\n",
             "    profile_keys = {'a', 'b'}\n    profile_keys |= {'c'}\n", "profile_keys",
             "an augmented assignment"),
        ):
            for side in ("head", "base"):
                with self.subTest(form=form, side=side):
                    plain = owner + "    pass\n"
                    bound = owner + body
                    if side == "head":
                        code, output = self.patch_claim_case(plain, bound)
                    else:
                        # The head differs from the base, so the check reads both sides.
                        code, output = self.patch_claim_case(
                            bound, bound.replace("{'a', 'b'}", "{'a'}") + "# changed\n")
                    self.assertEqual(code, 2, output)
                    self.assertIn("ERROR: release-delta input: tools/engine.py: ", output)
                    self.assertIn(name + ", a key-owning name, is bound or deleted by "
                                  + construct + " in a def or class body, a place the check"
                                  " does not read", output)
                    self.assertNotIn("FLOOR:", output)
        # A private body is skipped (a nonlocal statement in it is refused only when the private
        # body is nested in a public def or class body), a comprehension target binds a name of
        # the comprehension's own scope, and an attribute or subscript target binds no name, so
        # none of these is refused (PATCH, exit 0).
        forms = (
            "    profile_keys = {'a', 'b'}\n"
            "    del profile_keys\n"
            "    profile_keys |= {'c'}\n"
            "    type profile_keys = int\n"
            "    def profile_keys():\n        pass\n"
            "    async def keys():\n        pass\n"
            "    class profile_keys:\n        pass\n")
        nonlocal_form = "    def _h():\n        nonlocal profile_keys\n        del profile_keys\n"

        def nested(text):
            return "".join("    " + line + "\n" for line in text.splitlines())

        for form, head in (
            ("top-level private def body", "def f():\n    pass\ndef _g():\n" + forms + nonlocal_form),
            ("private def nested in a public def", "def f():\n    def _g():\n" + nested(forms)),
            ("private method of a public class", "class C:\n    def _m(self):\n" + nested(forms)),
            ("comprehension target", "def f():\n    return [profile_keys for profile_keys in ()]\n"),
            ("comprehension target in a class body",
             "class C:\n    x = [profile_keys for profile_keys in ()]\n"),
            ("attribute and subscript targets",
             "def f(self, d):\n    self.profile_keys |= {'c'}\n    del self.profile_keys\n"
             "    d['profile_keys'] += 1\n    del d['profile_keys']\n"),
            ("nonlocal of a name that is not key-named",
             "def f():\n    x = 1\n    def _g():\n        nonlocal x\n        del x\n"),
        ):
            with self.subTest(form=form):
                # The base binds the same public owner, so only the private body, the
                # comprehension or the target is new.
                code, output = self.patch_claim_case(head.split("\n")[0] + "\n    pass\n", head)
                self.assertEqual(code, 0, output)
                self.assertIn("FLOOR: PATCH", output)

    def test_lambda_and_private_header_together_never_hide_a_removal(self):
        # A lambda-local declaration beside a private header declaration in a public def never
        # hides the removal of a key from an assignment expression outside both: the view
        # outside private headers and lambda bodies (_KEY_VIEWS) reports it (MAJOR, exit 1).
        helpers = ("    def _h(x=(private_keys := {'b'})):\n        pass\n"
                   "    unused = lambda: (lambda_keys := {'b'})\n")
        walrus_return = "def f():\n    return (profile_keys := {'a', 'b'})\n"
        narrowed = "    return (profile_keys := {'a'})\n"
        for form, base, head in (
            ("both helpers in base and head",
             "def f():\n" + helpers + "    return (profile_keys := {'a', 'b'})\n",
             "def f():\n" + helpers + narrowed),
            ("both helpers added in the head", walrus_return, "def f():\n" + helpers + narrowed),
            ("private class header beside a lambda",
             "def f():\n    class _C(metaclass=(private_keys := {'b'})):\n        pass\n"
             "    unused = lambda: (lambda_keys := {'b'})\n"
             "    return (profile_keys := {'a', 'b'})\n",
             "def f():\n    class _C(metaclass=(private_keys := {'b'})):\n        pass\n"
             "    unused = lambda: (lambda_keys := {'b'})\n" + narrowed),
        ):
            with self.subTest(form=form):
                code, output = self.patch_claim_case(base, head)
                self.assertEqual(code, 1, output)
                self.assertIn("FLOOR: MAJOR", output)
                self.assertIn("accepted-key set module: removed b", output)
        # Both helpers added beside an unchanged walrus remove nothing (PATCH, exit 0).
        with self.subTest(form="helpers added beside an unchanged walrus"):
            code, output = self.patch_claim_case(
                walrus_return,
                "def f():\n" + helpers + "    return (profile_keys := {'a', 'b'})\n")
            self.assertEqual(code, 0, output)
            self.assertIn("FLOOR: PATCH", output)
            self.assertNotIn("accepted-key set", output)

    def test_source_that_does_not_compile_fails_closed(self):
        # A module whose tree parses but does not compile (an assignment expression in a
        # comprehension directly in a class body, or in a comprehension iterable) fails closed
        # (exit 2) in the head and in the base.
        good = "class Pub:\n    gate_keys = {'a', 'b'}\n"
        for form, bad, message in (
                ("walrus in a class-body comprehension",
                 "class Pub:\n    gate_keys = {'a'}\n    y = [(_known_keys := {'b'}) for _ in ()]\n",
                 "assignment expression within a comprehension cannot be used in a class body"),
                ("walrus in a class-body comprehension iterable",
                 "class Pub:\n    gate_keys = {'a'}\n    y = [z for z in (_known_keys := {'b'})]\n",
                 "assignment expression cannot be used in a comprehension iterable expression")):
            for side, base, head in (("head", good, bad), ("base", bad, good)):
                with self.subTest(form=form, side=side):
                    code, output = self.patch_claim_case(base, head)
                    self.assertEqual(code, 2, output)
                    self.assertIn("ERROR: release-delta input: tools/engine.py: invalid Python: ",
                                  output)
                    self.assertIn(message, output)
                    self.assertNotIn("FLOOR:", output)

    def test_unknown_node_fails_closed(self):
        # A node type the check does not know, as a statement, inside an expression or as a
        # match pattern, in a module with a key-owning name, fails closed (exit 2) through
        # check().
        class UnknownStatement(DELTA.ast.stmt):
            _fields = ()

        class UnknownExpression(DELTA.ast.expr):
            _fields = ()

        class UnknownPattern(DELTA.ast.pattern):
            _fields = ()

        parse = DELTA.ast.parse

        def statement(tree):
            tree.body.append(UnknownStatement())

        def expression(tree):
            tree.body.append(DELTA.ast.Expr(value=UnknownExpression()))

        def pattern(tree):
            tree.body.append(DELTA.ast.Match(
                subject=DELTA.ast.Constant(value=1),
                cases=[DELTA.ast.match_case(pattern=UnknownPattern(), guard=None,
                                            body=[DELTA.ast.Pass()])]))

        for form, graft, construct in (
                ("statement", statement, "a UnknownStatement statement"),
                ("expression", expression, "a UnknownExpression node"),
                ("pattern", pattern, "a UnknownPattern pattern")):
            def grafted(source, filename="<unknown>", *args, **kwargs):
                tree = parse(source, filename, *args, **kwargs)
                if str(filename).endswith("engine.py"):
                    graft(tree)
                return tree

            with self.subTest(form=form), self.repo() as repo:
                repo.replace("tools/engine.py", "return 1", "return 2")
                repo.version("1.2.4")
                with patch.object(DELTA.ast, "parse", grafted):
                    code, output = self.result(repo)
                self.assertEqual(code, 2, output)
                self.assertIn("ERROR: release-delta input: tools/engine.py: every key-owning name",
                              output)
                self.assertIn(construct + ", which the check does not know", output)
                self.assertNotIn("FLOOR:", output)

        # The same node types inside a public def body (public) and a public class body
        # (Widget) fail closed the same way, before the compile step, which would refuse these
        # synthetic nodes for another reason.
        class Body:
            def __init__(self, nodes):
                self.body = nodes

        for where, owner in (("def body", "public"), ("class body", "Widget")):
            for form, graft, construct in (
                    ("statement", statement, "a UnknownStatement statement"),
                    ("expression", expression, "a UnknownExpression node"),
                    ("pattern", pattern, "a UnknownPattern pattern")):
                def grafted(source, filename="<unknown>", *args, **kwargs):
                    tree = parse(source, filename, *args, **kwargs)
                    if str(filename).endswith("engine.py"):
                        graft(Body(next(node for node in tree.body
                                        if getattr(node, "name", None) == owner).body))
                    return tree

                with self.subTest(form=form, where=where), self.repo() as repo:
                    repo.replace("tools/engine.py", "return 1", "return 2")
                    repo.version("1.2.4")
                    with patch.object(DELTA.ast, "parse", grafted):
                        code, output = self.result(repo)
                    self.assertEqual(code, 2, output)
                    self.assertIn("ERROR: release-delta input: tools/engine.py: every key-owning"
                                  " name", output)
                    self.assertIn(construct + " in a def or class body, which the check does"
                                  " not know", output)
                    self.assertNotIn("invalid Python", output)
                    self.assertNotIn("FLOOR:", output)

    def test_shared_key_set_release_fails_closed(self):
        # A release of a key-owning name fails closed when the declaring statement bound the
        # same object to another target or handed it to other code, since no ast.Name load of
        # the released name then shows that the keys stay reachable.
        cases = [
            ("chained Assign, reversed", "ACCEPTED = profile_keys = {'a', 'b'}\n"
             "del profile_keys\n", "shared", "profile_keys"),
            ("chained Assign to a subscript", "_HOLD = {}\nprofile_keys = _HOLD['k'] = {'a', 'b'}\n"
             "del profile_keys\n", "shared", "profile_keys"),
            ("chained Assign to a tuple target bound from one value",
             "profile_keys = (ACCEPTED, *REST) = {'a', 'b'}\ndel profile_keys\n", "shared",
             "profile_keys"),
            ("chained Assign then a certain rebinding",
             "profile_keys = ACCEPTED = {'a', 'b'}\nprofile_keys = {'c'}\n", "shared",
             "profile_keys"),
            ("NamedExpr bound to another name",
             "ACCEPTED = (profile_keys := {'a', 'b'})\ndel profile_keys\n", "shared",
             "profile_keys"),
            ("NamedExpr without a release", "ACCEPTED = (profile_keys := {'a', 'b'})\n",
             "MAJOR", None),
            ("decorated def", "def _register(f):\n    return f\n\n@_register\ndef load():\n"
             "    profile_keys = {'a', 'b'}\n\ndel load\n", "shared", "load"),
            ("class with a base", "class Loader(object):\n    def load(self):\n"
             "        profile_keys = {'a', 'b'}\n\ndel Loader\n", "shared", "Loader"),
            ("decorated method", "class Loader:\n    @staticmethod\n    def load():\n"
             "        profile_keys = {'a', 'b'}\n\ndel Loader\n", "shared", "Loader"),
            ("declaration in a class body", "class Loader:\n    profile_keys = {'a', 'b'}\n\n"
             "del Loader\n", "shared", "Loader"),
            ("class with a keyword", "class Loader(metaclass=type):\n    def load(self):\n"
             "        profile_keys = {'a', 'b'}\n\ndel Loader\n", "shared", "Loader"),
            ("decorated class", "def _register(c):\n    return c\n\n@_register\nclass Loader:\n"
             "    def load(self):\n        profile_keys = {'a', 'b'}\n\ndel Loader\n", "shared",
             "Loader"),
            ("nested class with a base", "class Loader:\n    class Inner(object):\n        pass\n\n"
             "    def load(self):\n        profile_keys = {'a', 'b'}\n\ndel Loader\n", "shared",
             "Loader"),
            ("nested class with a keyword", "class Loader:\n    class Inner(metaclass=type):\n"
             "        pass\n\n    def load(self):\n        profile_keys = {'a', 'b'}\n\n"
             "del Loader\n", "shared", "Loader"),
            ("decorated nested class", "def _register(c):\n    return c\n\nclass Loader:\n"
             "    @_register\n    class Inner:\n        pass\n\n    def load(self):\n"
             "        profile_keys = {'a', 'b'}\n\ndel Loader\n", "shared", "Loader"),
            ("undecorated def, certain release", "def load():\n    profile_keys = {'a', 'b'}\n\n"
             "del load\n", "PATCH", None),
            ("plain key set, certain release", "profile_keys = {'a', 'b'}\ndel profile_keys\n",
             "PATCH", None),
            ("AnnAssign then a later Assign alias",
             "profile_keys: frozenset = frozenset({'a', 'b'})\nACCEPTED = profile_keys\n"
             "del profile_keys\n", "reachable", "profile_keys"),
            ("with item bound to it", "import contextlib\n"
             "profile_keys = {'a', 'b'}\nwith contextlib.nullcontext(profile_keys) as ACCEPTED:\n"
             "    pass\ndel profile_keys\n", "reachable", "profile_keys"),
            ("from-import bound to it", "profile_keys = {'a', 'b'}\n"
             "from engine import profile_keys as ACCEPTED\ndel profile_keys\n", "reachable",
             "profile_keys"),
        ]
        for form, base, expected, name in cases:
            with self.subTest(form=form):
                self.release_case(base, expected, name)

    def test_class_body_hand_off_fails_closed(self):
        # A class owner is shared, so its release fails closed: a class statement calls
        # builtins.__build_class__, which any code in the process can replace, and a class body
        # statement can hand the method or the class to other code, so a del of the class does
        # not show that its keys are gone. A class body of literal statements and plain defs
        # is shared too, a deliberate over-refusal. Each form sits beside a control without the
        # del, which reports the removed key.
        method = ("    def load(self):\n        profile_keys = {'a', 'b'}\n"
                  "        return profile_keys\n")
        mark = "def _mark():\n    return int\n"
        forms = [
            ("call appending the method", "_HOLD = []\n", "    _HOLD.append(load)\n"),
            ("descriptor with __set_name__",
             "_HOLD = []\nclass _Grab:\n    def __set_name__(self, owner, name):\n"
             "        _HOLD.append(owner)\n_GRAB = _Grab()\n", "    hook = _GRAB\n"),
            ("global set to the method", "KEEP = None\n", "    global KEEP\n    KEEP = load\n"),
            ("default that appends the method", "_HOLD = []\n",
             "    def other(self, _=_HOLD.append(load)):\n        return None\n"),
            ("call appending vars()", "_HOLD = []\n", "    _HOLD.append(vars())\n"),
            ("name load", "", "    hook = len\n"),
            ("assignment of a call", "", "    limit = len('abc')\n"),
            ("nonlocal statement", "", "    nonlocal limit\n"),
            ("nested class without a base", "", "    class Inner:\n        pass\n"),
            ("argument annotation that is a call", mark,
             "    def other(self, value: _mark()):\n        return None\n"),
            ("return annotation that is a call", mark,
             "    def other(self) -> _mark():\n        return None\n"),
            ("annotated assignment with a call annotation", mark, "    limit: _mark() = 3\n"),
            ("method with a type parameter", "",
             "    def other[T](self, value: T):\n        return value\n"),
        ]
        for form, before, body in forms:
            # A nonlocal statement in a module-level class body does not compile, so without
            # the del it fails closed (exit 2); with the del, the shared release fails first.
            for tail, expected in (("del Loader\n", "shared"),
                                   ("", "invalid" if form == "nonlocal statement" else "MAJOR")):
                with self.subTest(form=form, released=bool(tail)):
                    self.release_case(before + "class Loader:\n" + method + body + tail,
                                      expected, "Loader")
        with self.subTest(form="class with a type parameter"):
            self.release_case("class Loader[T]:\n" + method + "del Loader\n", "shared", "Loader")
        quiet = ('    \"\"\"Loader.\"\"\"\n    pass\n    LIMIT = 3\n'
                 '    NAMES = ("x", -1, {"k": [1.0, None]})\n    FIRST = SECOND = ()\n'
                 '    count: int = 0\n    label: "str"\n'
                 '    def other(self, flag=False, *rest, size: int = -1, **extra) -> None:\n'
                 '        return None\n'
                 '    async def later(self, name: "str" = None):\n        return None\n')
        for tail, expected in (("del Loader\n", "shared"), ("", "MAJOR")):
            with self.subTest(form="literal statements and plain defs", released=bool(tail)):
                self.release_case("class Loader:\n" + method + quiet + tail, expected, "Loader")

    def test_accepted_keys_belong_to_outermost_owner(self):
        # A key set in a nested def or in a method belongs to the outermost public def or class
        # around it, so a top-level del of an outer def drops it; a del of an outer class fails
        # closed, since every class owner (a class bound by a top-level statement) is shared.
        for outer, base, rebound in (
            ("load",
             "def load():\n    def inner():\n        profile_keys = {'a'}\n    return inner\n",
             "def load():\n    def inner():\n        profile_keys = {'b'}\n    return inner\n"),
            ("Loader",
             "class Loader:\n    def load(self):\n        profile_keys = {'a'}\n",
             "class Loader:\n    def load(self):\n        profile_keys = {'b'}\n"),
        ):
            head = base + f"\ndel {outer}\n\n" + rebound
            with self.subTest(base=base, head=head), self.repo() as repo:
                repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + base)
                repo.checkpoint()
                repo.replace("tools/engine.py", base, head)
                if outer == "Loader":
                    self.assert_release_uncertain(repo, outer, "handed it to other code")
                    continue
                output = self.expect(repo, "MAJOR")
                self.assertIn("accepted-key set module: removed a", output)
                self.assertIn("accepted-key set module: added b", output)

    def test_accepted_keys_compared_as_module_union(self):
        # Accepted keys are one union per module: a key dropped from a deleted and rebound def is
        # not reported removed while another remaining declaration in the module still holds it.
        base = ("def load():\n    profile_keys = {'a'}\n\n"
                "def keep():\n    profile_keys = {'a'}\n")
        head = base + "\ndel load\n\ndef load():\n    profile_keys = {'b'}\n"
        with self.subTest(base=base, head=head), self.repo() as repo:
            repo.write("tools/engine.py", repo.read("tools/engine.py") + "\n" + base)
            repo.checkpoint()
            repo.replace("tools/engine.py", base, head)
            output = self.expect(repo, "MINOR")
            self.assertIn("accepted-key set module: added b", output)
            self.assertNotIn("accepted-key set module: removed", output)

    def test_profile_values_and_keys(self):
        cases = [
            ("defaults/words.toml", 'terms = ["alpha"]', 'terms = ["beta"]', "MINOR"),
            ("defaults/words.toml", 'terms = ["alpha"]', "", "MAJOR"),
            ("defaults/words.toml", 'terms = ["alpha"]', 'terms = ["alpha"]\nextra = []', "MINOR"),
            ("core/profiles.toml", 'title = "Words"', 'title = "Corrected"', "MINOR"),
            ("core/profiles.toml", 'title = "Words"', "", "MAJOR"),
            ("core/profiles.toml", 'title = "Words"', 'title = "Words"\nnote = "Extra"', "MINOR"),
        ]
        for path, old, new, floor in cases:
            with self.subTest(change=new), self.repo() as repo:
                repo.replace(path, old, new)
                self.expect(repo, floor)

    def test_zero_major_breaking_and_stable_major(self):
        for version, code, claimed in (
            ("0.6.1", 1, "PATCH"), ("0.7.0", 0, "MINOR"), ("1.0.0", 0, "MAJOR"),
        ):
            with self.subTest(version=version), self.repo("0.6.0") as repo:
                repo.replace("tools/engine.py", "def public(", "def _public(")
                repo.version(version)
                output = self.expect(repo, "MAJOR", code, claimed)
                self.assertIn("BREAKING", output)
        with self.repo() as repo:
            repo.replace("tools/engine.py", "def public(", "def _public(")
            repo.version("1.3.0")
            self.expect(repo, "MAJOR", 1, "MINOR")
            repo.version("2.0.0")
            self.expect(repo, "MAJOR", 0, "MAJOR")

    def test_version_decrease_and_strict_versions(self):
        with self.repo() as repo:
            repo.version("1.2.2")
            output = self.expect(repo, "PATCH", 1, "DECREASE")
            self.assertIn("version decreased", output)
        # A waiver row that does not move the version up is refused outright: an equal or
        # backward row would waive every later unbumped change.
        for after in ("1.2.3", "1.2.2"):
            with self.subTest(after=after), self.repo() as repo:
                repo.replace("tools/engine.py", "return 1", "return 2")
                repo.waiver("PATCH", after=after)
                code, output = self.result(repo)
                self.assertEqual(code, 2, output)
                self.assertIn("to must be greater than from", output)
        for value in ("1.2", "01.2.3", "1.2.3-rc1", "1.2.3+build"):
            with self.subTest(value=value), self.repo() as repo:
                repo.version(value)
                self.assertEqual(self.result(repo)[0], 2)

    def test_matching_waiver_and_rebaseline(self):
        for before, after in (("1.2.3", "1.2.4"), ("0.6.0", "0.6.80")):
            with self.subTest(before=before), self.repo(before) as repo:
                repo.write("tools/new.py", "def check():\n    pass\n")
                repo.version(after)
                repo.waiver(before=before, after=after)
                self.assertIn("WAIVED", self.expect(repo, "MINOR", 0, "PATCH"))

    def test_mismatching_waivers(self):
        for options in (
            {"before": "1.2.2"}, {"after": "1.2.5"}, {"required": "PATCH"},
        ):
            with self.subTest(options=options), self.repo() as repo:
                repo.write("core/rules/new.md", "New.\n")
                repo.version("1.2.4")
                repo.waiver(**options)
                self.assertNotIn("WAIVED", self.expect(repo, "MINOR", 1, "PATCH"))

    def test_malformed_waivers_fail_closed(self):
        cases = [
            ("schema_version = 1", "schema_version = true"),
            ("schema_version = 1", "schema_version = 2"),
            ('from = "1.2.3"', 'from = "1.2"'),
            ('to = "1.2.4"', "to = 12"),
            ('required = "MINOR"', 'required = "NONE"'),
            ('reason = "Approved fixture re-baseline."', 'reason = ""'),
            ('approved_by = "maintainer"', 'approved_by = "reviewer"'),
            ("approved = 2026-09-26", 'approved = "2026-09-26"'),
            ("approved = 2026-09-26", "approved = 2026-09-26T00:00:00Z"),
            ('decision_ref = "fixture decision"', 'decision_ref = " "'),
            ('decision_ref = "fixture decision"', ""),
            ('decision_ref = "fixture decision"', 'decision_ref = "fixture decision"\nextra = 1'),
            ("schema_version = 1", "schema_version = 1\nextra = 1"),
            ("[[waiver]]", "[waiver]"),
        ]
        for old, new in cases:
            with self.subTest(change=new), self.repo() as repo:
                repo.waiver()
                repo.replace("core/release-waivers.toml", old, new)
                self.assertEqual(self.result(repo)[0], 2)

    def test_unresolvable_base(self):
        with self.repo() as repo:
            code, output = self.result(repo, "no-such-ref")
            self.assertEqual(code, 2)
            self.assertIn("cannot resolve release base", output)
            repo.git("update-ref", "-d", "refs/remotes/origin/main")
            code, output = self.result(repo)
            self.assertEqual(code, 2)
            self.assertIn("origin/main", output)
            self.expect(repo, "NONE", 0, base=repo.base)

    def test_head_is_disk_not_index_or_commit(self):
        with self.repo() as repo:
            repo.replace("core/rules/alpha.md", "A clause.", "Staged clause.")
            repo.git("add", ".")
            repo.write("core/rules/alpha.md", "A clause.\n")
            self.expect(repo, "NONE", 0)
            repo.write("core/rules/alpha.md", "Unstaged clause.\n")
            self.expect(repo, "PATCH")
        with self.repo() as repo:
            repo.write("core/rules/new.md", "Committed on branch.\n")
            repo.git("add", ".")
            repo.git("-c", "commit.gpgsign=false", "commit", "-qm", "branch")
            self.expect(repo, "MINOR")

    def test_mode_only_change(self):
        with self.repo() as repo:
            path = repo.pack / "tools/engine.py"
            path.chmod(path.stat().st_mode | 0o100)
            self.expect(repo, "PATCH")

    def test_compiler_modes_are_read_only_and_combine_failures(self):
        with self.repo() as repo:
            args = ["--root", str(repo.root), "--release-delta", "--base", repo.base]
            with patch.dict(sys.modules, {"pack_release_delta": DELTA}), \
                    patch.object(COMPILER, "_ensure_aiqt", return_value=None) as aiqt, \
                    patch.object(COMPILER, "load_and_validate", return_value=([], [])), \
                    patch.object(COMPILER, "run_check", return_value=[]) as drift, \
                    patch.object(COMPILER, "plan_generate", side_effect=AssertionError("write")), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(COMPILER.main(args), 0)
                aiqt.assert_not_called()
                self.assertEqual(COMPILER.main(args + ["--check"]), 0)
                repo.write("core/rules/new.md", "New.\n")
                self.assertEqual(COMPILER.main(args + ["--check"]), 1)
                drift.return_value = ["fixture drift"]
                repo.version("1.3.0")
                self.assertEqual(COMPILER.main(args + ["--check"]), 1)
                drift.return_value = []
                self.assertEqual(COMPILER.main(args + ["--check"]), 0)
                repo.write("core/release-waivers.toml", "invalid TOML")
                self.assertEqual(COMPILER.main(args + ["--check"]), 2)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            COMPILER.main(["--base", "HEAD", "--check"])
        self.assertEqual(error.exception.code, 2)

    def test_fixture_git_ignores_ambient_git_index_file(self):
        # In the earlier repository, an inherited GIT_INDEX_FILE made the
        # fixture's `git add` write an index outside its temporary
        # directory. The fixture environment drops every GIT_* variable.
        with tempfile.TemporaryDirectory(prefix="release-delta-") as directory:
            ambient = Path(directory) / "ambient-index"
            with patch.dict(os.environ, {"GIT_INDEX_FILE": str(ambient)}):
                with self.repo() as repo:
                    self.assertNotIn("GIT_INDEX_FILE", repo.env)
                    self.expect(repo, "NONE", 0)
            self.assertFalse(
                ambient.exists(),
                "the fixture's git commands wrote to the ambient "
                "GIT_INDEX_FILE instead of the fixture repository")


if __name__ == "__main__":
    unittest.main()
