"""Working-tree release floor for the Corpus-Management pack (stdlib only).

Accepted-key declaration and removal rules
==========================================

This section is the one authoritative text of the rules by which the check reads accepted keys:
what counts as a declaration, the views in which keys are compared, what is reported removed or
added, which places are read as releases, and which places are not read and fail closed.
src/README.md, specs/specification-audit-programme.md (section 6, gate 99), the _api
docstring and the comment of _accepted_sets point to this section by name and do not
restate it. The release level each change reported here needs, and
the exit status of a refusal, are stated in specification-audit-programme.md, section 6, gate
99, whose rules point to the rows of _RELEASE_CASES that exercise them.

An accepted-key declaration is a literal assignment, an annotated assignment with a value or an
assignment expression whose target is a name equal to keys or ending in _keys (for example
KNOWN_RULE_KEYS, REGEX_TABLE_KEYS, gate_keys and profile_keys), read at module level and in
public defs and classes, outside every private (underscore) def or class body; the header of a
private def or class is read in the scope around it. A non-literal declaration in those scopes
is an input error (ValueError). Outside every def, class and lambda body, an assignment
expression in a header (a def or class header, a lambda default, a type statement or an
annotation) fails closed and one in a lambda body is a lambda local, no declaration; inside a
public def or class body every assignment expression is a declaration, one in the header of a
nested private def or class or in a lambda body included. Each declaration is held by the
top-level name whose binding holds it: the outermost public def or class around it, or else the
key-set name itself.

Accepted keys are compared in views, each the union per module of that view's declarations that
remain after each top-level statement, so renaming a key-set variable is not a removal of an
accepted key (renaming a public key set bound at module level still removes a public name). A
top-level del of a public name is a certain release: unless one of the refusal conditions
below applies, it drops, with its symbol, the accepted keys declared in the deleted binding.
A top-level assignment, augmented assignment, annotated assignment with a
value, def, async def, class, import other than a star import, name target of the first item of
a with statement or del releases with certainty only a name it binds or deletes directly, and a
declaration that no name holds any more is dropped, so a del or a rebinding followed by a later
binding of the name cannot hide a removed key. When a release of a name that owns declarations
is refused because the module refers to the name or has a star import, the error names the
module and the name and states that the accepted keys of that name may still be reachable after
its release; when it is refused because the release is not certain, a declaration is shared or
a global statement names it, the error states that the release cannot be read as certain.

A key-owning name is a name that owns accepted-key declarations or is named keys or *_keys, and
only these places binding or deleting a module name are read: a certain release (a name target
of a top-level assignment, augmented assignment, annotated assignment with a value or del, a
top-level def, async def or class name, a name a top-level import other than a star import
binds, and a name target of the first item of a top-level with, never of an async with), which
drops the declarations the name owned; a declaration (a name target of an assignment or
annotated assignment with a value inside a compound statement, or an assignment expression
outside every header (a def or class header, a lambda default, a type statement's value or type
parameter, or an annotation) and outside every lambda body); and an uncertain release (a for or
async for target, an except name, a match capture, a type statement's name, and a def, async
def, class, import, del, augmented assignment, with or async with target inside a compound
statement). A declaration place that binds a name that owns declarations (an assignment inside
a compound statement, or an assignment expression) is read as an uncertain release of that
name, not only as a declaration, and fails closed (the release is not certain, one of the
refusal conditions below) when no place in the same statement is a certain release of the
name. Every other place that binds or deletes a key-owning name fails closed (ValueError
naming the module, the name and the construct; its outcome is the matching row of
_RELEASE_CASES): a name inside a tuple, list or starred target (of an assignment, for, with or
del in a top-level statement, a del of a tuple included, a deliberate over-refusal, or of an
assignment, for, async for, with or async with in a public def or class body, outside every
private body); in a public def or class body, outside every private body, a plain name that a
for, async for, with or async with target, an except name, a match capture or an import binds;
in a public def or class body, outside every private body, a name that a del deletes, or that
an augmented assignment, a type statement or a nested def, async def or class (a private one
included) binds; a nonlocal statement naming a key-named name anywhere inside a public def or
class body, a private body nested in it included (a deliberate over-refusal for one that names
a local of a private body around it); a with target after the first item of a top-level with
statement, which an earlier context manager can skip (inside a compound statement every with
target is read as an uncertain release), or a with target that unpacks; a name target of a
top-level async with statement, which compiles only in an async def body (the walker itself
never reads it as a certain release, and _surface's compile step then refuses the module too; a
target after the first item gets this reason too, not the after-the-first-item one, since a
statement that does not compile never runs a context manager that could skip it; a with target
after the first item and every async with target keep their reason inside a compound statement
and for every name an unpacking target holds); an assignment expression in a header (a
decorator, default, annotation, base, keyword or type parameter of a def or class, a lambda
default, a type statement's value or type parameter, or an annotation); a global statement
anywhere in the module; and a node type (a statement, an expression or a match pattern) the
check does not know, at top level or in a public def or class body, when the module has a
key-owning name. A name bound or deleted at such a place in a public def or class body
fails closed when it is key-named or owns declarations anywhere in the module, before or after
that place. For a name that is not key-named this is a deliberate over-refusal for every
construct above except a nonlocal statement, which is refused only for a key-named name (one
naming any other name is not refused), and an assignment expression in a header of a def or
class nested in the body, which is not refused for such a name (only a key-named target there
is read, as a declaration); exactly these refuse such a name there, outside every private body:
a name inside a tuple, list or starred target of an assignment, for, async for, with or async
with; a plain for, async for, with (at any item) or async with target; an except name (of
except or except*); a match capture, star pattern or mapping rest; an import or from-import; a
del, of the plain name or inside a tuple or list; an augmented assignment; a type statement;
and a nested def, async def or class (a global statement naming such a name is refused
separately, below, and a node type the check does not know is refused whatever it binds); the
constructs it covers are the refusing rows of _RELEASE_CASES for a key-owning name that is not
key-named in a public def or class body: such a binding in a public def or class body binds a
local or a class attribute and cannot rebind the module name without a global statement, which
is refused separately. A plain or annotated assignment whose target is the name itself (not
inside a tuple, list or starred target), an assignment expression or a parameter binding such a
name in a public def or class body is not refused. A key-named name that owns no declarations
fails closed the same way at an uncertain release, with its own message, which names the
construct and says the check reads it as an uncertain release, not as a declaration or a
certain release. The level of a key accepted in another way (an inline set in an expression, a
later add, or a |= on a name, one on a keys or *_keys name in a public def or class body or
inside a compound statement included) is the matching row of _RELEASE_CASES. A release of a
name that owns declarations fails closed (ValueError naming the module and the name) when the
module refers to that name anywhere (an ast.Name load of it, the target of an augmented
assignment, which reads it, or a from-import of it, in any scope and at any position, before or
after the release, including inside a function or class body, a container, a tuple or a default
value; a load of a same-named local or parameter counts too, a deliberate over-refusal), when
the module has a star import, when the release is not a certain release, when a declaration the
name owns is shared (its statement also bound the same object to another target, as a chained
assignment does; it is an assignment expression; the owning def has a decorator; the owner is a
class, a class bound by a top-level statement (directly or inside a compound statement), since
a class statement calls builtins.__build_class__, which any code in the process can replace, a
deliberate over-refusal for a class nothing hooks; or it sits directly in a class body), or
when a global statement anywhere in the module names it (a def or class body that declares it
global can bind or delete it when that body runs; a module-level global statement, which binds
nothing by itself, is refused too, a deliberate over-refusal). A certain release of a
key-owning name with none of these drops its keys. A class or def nested in a def or class body
owns nothing: its declarations belong to the outermost def or class around it and are shared as
that one's are, or when they sit directly in a class body, since the outermost def's body, with
every class or decorated def nested in it, runs only when the def is called, through a load of
its name (refused), its decorator (shared) or a reference the check does not see. A lambda body
at module level is a scope of its own that no public def or class owns, so an assignment
expression in it binds a lambda local and is no declaration; the lambda's defaults run in the
module scope and are read as a header. A header of a def or class (a decorator, default,
annotation, type parameter, base or keyword) runs in the scope around it, so it is read with
that scope's owner, never as part of the def or class: an assignment expression in a header of
a top-level statement fails closed (above), a lambda body in such a header is a lambda scope
that holds no declaration, and an assignment expression in a header of a def or class, public
or private (underscore), nested in a public def or class is a declaration that the outermost
public def or class around it owns; only a private body is skipped. Inside a public def or
class body, outside every private def or class body, every assignment, annotated assignment
with a value and assignment expression whose target is keys or a *_keys name is a declaration
of the outermost public def or class, one in a lambda body included. An annotated assignment
without a value whose target is keys or a *_keys name fails closed (ValueError naming the
module and the declaration) everywhere the walker reads statements, that is outside every
private def or class body: at top level, at any depth in a compound statement and in a public
def or class body. It binds nothing, so the refusal, at top level too, is a deliberate
over-refusal. Accepted keys are compared in five views (_KEY_VIEWS): every declaration; only
assignments and annotated assignments; every declaration outside a header of a private def or
class nested in a public def or class; every declaration outside every lambda body; and every
declaration outside both such headers and every lambda body. A key is reported removed or added
when any view removes or adds it, so neither an assignment expression, a lambda local
declaration nor a private header hides a removal, alone or together (a lambda local declaration
beside a private header included); the level of moving a key between an assignment and an
assignment expression, or into or out of a lambda body, is a row of _RELEASE_CASES. A module
whose parsed tree does not compile (for example an assignment expression in a comprehension
directly in a class body) fails closed (ValueError). Each name that owns declarations must be
bound exactly once in the statement that makes them, by the binding that holds them: a second
binding or a deletion of that name in the same statement fails closed (ValueError naming the
module and the name), a deliberate over-refusal that includes an assignment expression in a def
header that rebinds the def's own name. A star import, at any depth, in a top-level statement
that makes a declaration or comes after one that made a declaration fails closed, a deliberate
over-refusal for a star import that would not rebind the owning name or that runs before the
declaration in the same statement. A module nested too deeply for the recursive reading (a deep
expression), or too complex for ast.parse (a MemoryError or RecursionError), fails closed: _api
raises ValueError. Accepted keys are not compared per binding: each view is the union of its
declarations that remain after each top-level statement, so a key is reported removed when some
view held it before and no remaining declaration in that view holds it, and added when some
view holds it and no declaration in that view held it before.

What the check does not see. A reference to a key-owning name that is none of an ast.Name
load, an augmented-assignment target or a from-import in the module is not seen: an attribute
of the module object, globals(), getattr, exec or a string, another module, or a process-wide
hook that sees the module namespace or every object (a tracing, profiling or monitoring
function, an audit hook, builtins.__import__, which an import statement passes the module
namespace, the gc module, or a C-level dictionary or function watcher). A certain release of
the name drops its accepted keys although such a reference may still reach them, and a later
removal of those keys is not reported; the outcome of that edit is the matching row of
_RELEASE_CASES. Also not seen: a key removed from one declaration while another remaining
declaration still holds it in every view that held it; and the value that a top-level import
or the name target of the first item of a top-level with binds to a key-set name, which is
not an accepted-key declaration (the binding itself is seen: it is a certain release, so it
drops the declarations the name owned, and a key that no remaining declaration holds is
reported removed).
"""
from __future__ import annotations

import ast
import datetime
import os
import re
import subprocess
import tomllib
from pathlib import Path, PurePosixPath

_LEVELS = ("NONE", "PATCH", "MINOR", "MAJOR")
_VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
_MANIFEST = "core/manifest.toml"
_WAIVERS = "core/release-waivers.toml"
_WAIVER_FIELDS = {
    "from", "to", "required", "reason", "approved_by", "approved", "decision_ref",
}


def _git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"git {' '.join(args)}: {detail or 'command failed'}")
    return result.stdout


def _version(value, label):
    if not isinstance(value, str) or not _VERSION.fullmatch(value):
        raise ValueError(f"{label}: expected strict x.y.z version, got {value!r}")
    return tuple(int(part) for part in value.split("."))


def _relative(value, label):
    if (not isinstance(value, str) or not value or "\\" in value
            or PurePosixPath(value).is_absolute()
            or ".." in PurePosixPath(value).parts
            or PurePosixPath(value).as_posix() != value or value == "."):
        raise ValueError(f"{label}: invalid pack-relative path {value!r}")
    return value


class _Snapshot:
    def __init__(self, root, pack_root, revision=None):
        self.root = root
        self.pack_root = pack_root
        self.revision = revision
        self.prefix = pack_root.relative_to(root).as_posix() + "/"
        self.files = {}
        self.cache = {}
        self.modes = {}
        if revision:
            raw = _git(root, "ls-tree", "-r", "-z", revision, "--", self.prefix)
            for entry in raw.split(b"\0"):
                if entry:
                    metadata, path = entry.split(b"\t", 1)
                    mode, kind, _ = metadata.split()
                    rel = path.decode("utf-8")[len(self.prefix):]
                    self.files[rel] = mode in (b"100644", b"100755")
                    self.modes[rel] = mode.decode("ascii")
        else:
            def onerror(error):
                raise error

            for parent, dirs, names in os.walk(pack_root, onerror=onerror):
                for name in list(dirs):
                    path = Path(parent) / name
                    if path.is_symlink():
                        self.files[path.relative_to(pack_root).as_posix()] = False
                        dirs.remove(name)
                for name in names:
                    path = Path(parent) / name
                    rel = path.relative_to(pack_root).as_posix()
                    self.files[rel] = path.is_file() and not path.is_symlink()
                    if self.files[rel]:
                        self.modes[rel] = "100755" if path.stat().st_mode & 0o100 else "100644"

    def read(self, rel):
        if rel not in self.files:
            return None
        if not self.files[rel]:
            raise ValueError(f"{rel}: release inputs must be regular files")
        if rel not in self.cache:
            if self.revision:
                data = _git(self.root, "show", f"{self.revision}:{self.prefix}{rel}")
            else:
                path = self.pack_root / rel
                if not path.resolve().is_relative_to(self.pack_root):
                    raise ValueError(f"{rel}: path escapes the pack")
                data = path.read_bytes()
            self.cache[rel] = data
        return self.cache[rel]

    def toml(self, rel):
        raw = self.read(rel)
        if raw is None:
            raise ValueError(f"{rel}: missing declared file")
        try:
            return tomllib.loads(raw.decode("utf-8"))
        except (UnicodeError, tomllib.TOMLDecodeError) as exc:
            raise ValueError(f"{rel}: invalid TOML: {exc}") from exc


def _schema(data, label):
    value = data.get("schema_version")
    if type(value) is not int or value < 1:
        raise ValueError(f"{label}: schema_version must be a positive integer")
    return value


def _registers(snapshot, manifest):
    declarations = manifest.get("registers")
    if not isinstance(declarations, dict):
        raise ValueError(f"{_MANIFEST}: [registers] must be a table")
    result = {}
    for name, rel in declarations.items():
        _relative(rel, f"[registers].{name}")
        if not rel.endswith(".toml"):
            raise ValueError(f"[registers].{name}: expected a TOML path")
        data = snapshot.toml(rel)
        _schema(data, rel)
        result[name] = (rel, data)
    return result


def _scope(snapshot):
    # Every file in the pack is a release surface except __pycache__. Following manifest
    # references let pack-root or noncanonical references escape, and a README can be a
    # generation source, so neither decides the scope.
    return {rel for rel in snapshot.files if "__pycache__" not in PurePosixPath(rel).parts}


def _engine_path(rel):
    # Every Python file in the pack is engine code, wherever it sits.
    path = PurePosixPath(rel)
    return path.suffix == ".py" and "__pycache__" not in path.parts


def _clause_path(rel):
    path = PurePosixPath(rel)
    return path.parent == PurePosixPath("core/rules") and path.suffix == ".md"


def _entities(data, name, label):
    if not data:
        return {}
    layouts = {
        "clauses": "clauses", "id_history": "events", "ownership": "owned_targets",
        "gates": "gates", "profiles": "profiles", "hooks": "hooks",
    }
    collections = [key for key, value in data.items() if isinstance(value, (dict, list))]
    expected = layouts.get(name)
    if (len(collections) != 1 or expected is not None and collections != [expected]):
        raise ValueError(f"{label}: ambiguous register identity layout; expected "
                         f"{expected or 'one table-keyed or id-field collection'}")
    result = {}
    for collection, rows in data.items():
        if collection == "schema_version":
            continue
        field = "rule" if name == "ownership" and collection == "owned_targets" else "id"
        if isinstance(rows, dict):
            for identity, row in rows.items():
                if isinstance(row, dict) and "id" in row and row["id"] != identity:
                    raise ValueError(f"{label}: ambiguous table key/id at {collection}.{identity}")
                result[(collection, identity)] = [row]
        elif isinstance(rows, list):
            for row in rows:
                if (not isinstance(row, dict) or not isinstance(row.get(field), str)
                        or not row[field].strip()):
                    raise ValueError(
                        f"{label}: ambiguous identity in {collection}; expected {field!r}"
                    )
                identity = (collection, row[field])
                if identity in result and not (name == "id_history" and collection == "events"):
                    raise ValueError(f"{label}: duplicate identity {identity!r}")
                result.setdefault(identity, []).append(row)
    return result


def _same(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_same(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(_same(a, b) for a, b in zip(left, right))
    return left == right


def _profile_changes(left, right, label, emit):
    if isinstance(left, dict) and isinstance(right, dict):
        for field in sorted(left.keys() - right.keys()):
            emit(3, f"{label}: profile key removed {field}")
        for field in sorted(right.keys() - left.keys()):
            emit(2, f"{label}: profile key added {field}")
        for field in sorted(left.keys() & right.keys()):
            _profile_changes(left[field], right[field], f"{label}.{field}", emit)
    elif not _same(left, right):
        if isinstance(left, dict):
            for field in sorted(left):
                emit(3, f"{label}: profile key removed {field}")
        if isinstance(right, dict):
            for field in sorted(right):
                emit(2, f"{label}: profile key added {field}")
        emit(2, f"{label}: profile value changed (default correction)")


def _profiles(snapshot, registers):
    result = {}
    if "profiles" not in registers:
        return result
    rel, data = registers["profiles"]
    for identity, rows in _entities(data, "profiles", rel).items():
        row = rows[0]
        if not isinstance(row, dict) or "target" not in row:
            raise ValueError(f"{rel}: profile {identity!r} needs a target")
        target = _relative(row["target"], f"{rel}: profile target")
        if not target.endswith(".toml"):
            raise ValueError(f"{rel}: profile target must be TOML")
        document = snapshot.toml(target)
        _schema(document, target)
        result[identity] = (target, document)
    return result


def _parameters(node):
    args = node.args
    result = {arg.arg for arg in args.posonlyargs + args.args + args.kwonlyargs}
    if args.vararg:
        result.add("*" + args.vararg.arg)
    if args.kwarg:
        result.add("**" + args.kwarg.arg)
    return result


def _class_parameters(node):
    result = set()
    for child in node.body:
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if child.name in ("__init__", "__new__"):
                result.update(_parameters(child) - {"self", "cls"})
    if any(
        isinstance(decorator, ast.Name) and decorator.id == "dataclass"
        or isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name)
        and decorator.func.id == "dataclass"
        for decorator in node.decorator_list
    ):
        result.update(
            child.target.id for child in node.body
            if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name)
        )
    return result


def _literal_set(node, label):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id in ("set", "frozenset") and not node.keywords:
            if not node.args:
                return set()
            if len(node.args) == 1:
                return _literal_set(node.args[0], label)
    try:
        value = ast.literal_eval(node)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{label}: accepted-key declaration is not a literal string set") from exc
    if not isinstance(value, (set, frozenset, tuple, list, dict)):
        raise ValueError(f"{label}: accepted-key declaration is not a string collection")
    if not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label}: accepted keys must be strings")
    return set(value)


def _key_named(name):
    lowered = name.lower()
    return lowered == "keys" or lowered.endswith("_keys")


def _accepted_sets(tree, label):
    # The rules by which this reads accepted keys (what counts as a declaration, the views in
    # which keys are compared, what is reported removed or added, the places read as
    # releases, the places that are not read and fail closed, and what the check does not
    # see) are stated once, in the module docstring, section "Accepted-key declaration and
    # removal rules"; this comment does not restate them.
    declarations = []
    loaded = {node.id for node in ast.walk(tree)
              if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)}
    loaded |= {node.target.id for node in ast.walk(tree)
               if isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name)}
    loaded |= {alias.name for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
               for alias in node.names}
    star = any(isinstance(node, ast.ImportFrom) and any(alias.name == "*" for alias in node.names)
               for node in ast.walk(tree))
    deferred = {name for node in ast.walk(tree) if isinstance(node, ast.Global)
                for name in node.names}
    key_named = any(isinstance(node, ast.Name) and _key_named(node.id) for node in ast.walk(tree))

    def visit(node, scope, shared, in_class, place):
        if scope and not isinstance(node, _BODY_NODES):
            # A node type the check does not know, in a public def or class body, can bind or
            # delete a name in a way none of the branches below reads, so it fails closed when
            # the module has a key-owning name, as one in a top-level statement does.
            kind = ("statement" if isinstance(node, ast.stmt)
                    else "pattern" if isinstance(node, ast.pattern) else "node")
            unknown_in_bodies.append(f"a {type(node).__name__} {kind} in a def or class body,"
                                     " which the check does not know")
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            # A header (a decorator, default, annotation, return annotation, type parameter,
            # base or keyword) runs in the scope around the def or class, so it is read with
            # that scope's owner, for a private (underscore) def or class too; only the body
            # belongs to the def or class, and a private body is skipped. A lambda in a header
            # of a top-level statement is then read as a lambda at module level.
            private = node.name.startswith("_")
            if scope:
                # A nested def or class binds its name in the public def or class body
                # around it, a place the check does not read, so a key-owning one fails
                # closed, a private (underscore) one included (body_bound).
                body_bound(scope, node.name,
                           ("a class" if isinstance(node, ast.ClassDef)
                            else "an async def" if isinstance(node, ast.AsyncFunctionDef)
                            else "a def") + " in a def or class body")
            body = {id(child) for child in node.body}
            for child in ast.iter_child_nodes(node):
                if id(child) not in body:
                    visit(child, scope, shared, in_class,
                          place | {"private header"} if private else place)
            if private:
                if scope:
                    # A nonlocal statement in a private body nested in a public def or
                    # class body can rebind or delete a name of that body when the private
                    # body runs, so a key-named one fails closed, a deliberate over-refusal
                    # for one that names a local of a private body around it.
                    for part in ast.walk(node):
                        if isinstance(part, ast.Nonlocal):
                            for name in part.names:
                                if _key_named(name):
                                    raise unread(".".join((*scope, name)),
                                                 "a nonlocal statement in a def or class"
                                                 " body")
                return
            inner = (*scope, node.name)
            # Only the outermost def or class owns declarations, so a nested one keeps its
            # sharing (in_class still marks a declaration directly in a class body shared).
            for child in node.body:
                visit(child, inner, shared if scope else _hands_off(node),
                      isinstance(node, ast.ClassDef), place)
            return
        elif isinstance(node, ast.Lambda):
            # A lambda body is a function scope of its own; its defaults run in the scope
            # around it and are read there.
            visit(node.args, scope, shared, in_class, place)
            if scope:
                # In a public def or class, an assignment expression in the body binds a
                # lambda local; it is read as a declaration of the outermost public def or
                # class, marked so that the view outside every lambda body leaves it out and
                # it never hides a removal (_KEY_VIEWS).
                visit(node.body, scope, shared, False, place | {"lambda"})
            # At module level no public def or class owns the body, so an assignment
            # expression in it binds a lambda local and is no declaration.
            return
        if scope:
            # In a public def or class body a key-owning name inside a tuple, list or starred
            # target of an assignment, for, async for, with or async with is a place the check
            # does not read, so it fails closed (body_bound), as _binding_events makes it fail
            # closed in a top-level statement; so does a key-owning plain name that a for, async
            # for, with or async with target, an except name, a match capture or an import binds
            # there, a key-owning name that a del deletes or that an augmented assignment or a
            # type statement binds there (a nested def or class name is refused above), and a
            # key-named name that a nonlocal statement names there.
            if isinstance(node, ast.Assign):
                unpacking = node.targets
            elif isinstance(node, (ast.For, ast.AsyncFor)):
                unpacking = [node.target]
            elif isinstance(node, (ast.With, ast.AsyncWith)):
                unpacking = [item.optional_vars for item in node.items]
            else:
                unpacking = []
            for target in unpacking:
                if isinstance(target, (ast.Tuple, ast.List, ast.Starred)):
                    for name in _bound_names(target):
                        body_bound(scope, name, "a name inside a tuple, list or starred"
                                                " target in a def or class body")
            if isinstance(node, (ast.For, ast.AsyncFor)):
                named = [(node.target, "an async for target" if isinstance(node, ast.AsyncFor)
                          else "a for target")]
            elif isinstance(node, (ast.With, ast.AsyncWith)):
                named = [(item.optional_vars, "an async with target"
                          if isinstance(node, ast.AsyncWith) else "a with target")
                         for item in node.items]
            elif isinstance(node, ast.ExceptHandler):
                named = [(node.name, "an except name")]
            elif isinstance(node, (ast.MatchAs, ast.MatchStar)):
                named = [(node.name, "a match capture")]
            elif isinstance(node, ast.MatchMapping):
                named = [(node.rest, "a match mapping rest")]
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                named = [(alias.asname or alias.name.split(".")[0], "an import")
                         for alias in node.names if alias.name != "*"]
            elif isinstance(node, ast.Delete):
                named = [(name, "a del" if isinstance(target, ast.Name)
                          else "a del (inside a tuple, list or starred target)")
                         for target in node.targets for name in _bound_names(target)]
            elif isinstance(node, ast.AugAssign):
                named = [(node.target, "an augmented assignment")]
            elif isinstance(node, ast.TypeAlias):
                named = [(node.name, "a type statement")]
            elif isinstance(node, ast.Nonlocal):
                named = [(name, "a nonlocal statement") for name in node.names]
            else:
                named = []
            for bound, construct in named:
                if isinstance(bound, ast.Name):
                    bound = bound.id
                if not isinstance(bound, str):
                    continue
                if not isinstance(node, ast.Nonlocal):
                    body_bound(scope, bound, construct + " in a def or class body")
                elif _key_named(bound):
                    raise unread(".".join((*scope, bound)), construct + " in a def or class body")
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    if _key_named(target.id):
                        identity = ".".join((*scope, target.id))
                        if node.value is None:
                            raise ValueError(f"{label}: accepted-key declaration {identity} has no value")
                        owner = scope[0] if scope else target.id
                        declarations.append(
                            (owner, _literal_set(node.value, f"{label}: {identity}"),
                             shared or in_class or len(targets) > 1
                             or isinstance(node, ast.NamedExpr),
                             place | {"walrus"} if isinstance(node, ast.NamedExpr) else place))
        for child in ast.iter_child_nodes(node):
            visit(child, scope, shared, in_class, place)

    def uncertain(name, reason):
        return ValueError(
            f"{label}: the release of {name}, which owns accepted keys, cannot be read as"
            f" certain ({reason}); the check cannot decide the floor")

    # The refusal for a place in a def or class body that the check does not read, for a
    # global statement naming a key-named name that owns no declarations (one naming a name
    # that owns declarations is refused through uncertain() instead, below), for a node type
    # (a statement, an expression or a match pattern) the check does not know, at top level
    # or in a public def or class body, and for a top-level unread place that binds or
    # deletes a key-named name owning no declarations (_other_keys, _o = None, None, for
    # example). A top-level unread place (a name inside a tuple, list or starred target, or
    # an async with target, for example) that binds or deletes a name owning declarations is
    # refused through uncertain() instead (below), which names the construct. An uncertain
    # release of a key-named name that owns no declarations fails closed through
    # unowned_uncertain() instead (below).
    def unread(name, construct):
        return ValueError(
            f"{label}: {name}, a key-owning name, is bound or deleted by {construct}, a place"
            " the check does not read; the check cannot decide the floor")

    # The refusal for an uncertain release (a place the check reads as a release that may or
    # may not happen) of a key-named name that owns no declarations: the check reads the
    # construct, but neither as a declaration nor as a certain release, so it names the
    # construct and that reading rather than a place the check does not read.
    def unowned_uncertain(name, construct):
        return ValueError(
            f"{label}: {name}, a key-named name that owns no accepted-key declarations, is bound"
            f" or deleted by {construct}, which the check reads as an uncertain release, not as a"
            " declaration or a certain release; the check cannot decide the floor")

    def body_bound(scope, name, construct):
        # A name bound or deleted at a place in a public def or class body that the check
        # does not read: a key-named one fails closed at once, and any other one fails closed
        # once the module is read if it owns declarations anywhere in the module, before or
        # after that place.
        if _key_named(name):
            raise unread(".".join((*scope, name)), construct)
        bound_in_bodies.append((name, ".".join((*scope, name)), construct))

    bound_in_bodies = []
    unknown_in_bodies = []
    owned = set()
    star_owner = None
    for node in tree.body:
        events = _binding_events(node)
        owners = {entry[0] for entry in declarations}
        certain = {name for name, _, kind in events if kind == "certain"}
        for name, construct, kind in events:
            if name is None and (owners or key_named):
                raise unread("every key-owning name", construct)
        names = sorted({name for name, _, _ in events
                        if name is not None and (name in owners or _key_named(name))})
        for name in names:
            mine = [(construct, kind) for other, construct, kind in events if other == name]
            if name in owners:
                if star or name in loaded:
                    raise ValueError(
                        f"{label}: accepted keys of {name} may still be reachable after its"
                        " release; the check cannot decide the floor")
                odd = [construct for construct, kind in mine if kind == "unread"]
                if odd or name not in certain:
                    odd += [construct for construct, kind in mine if kind != "certain"]
                    raise uncertain(name, "the statement may not bind or delete it, or binds it"
                                          " only in a form not read as a certain release: "
                                          + odd[0])
                if any(entry[2] for entry in declarations if entry[0] == name):
                    raise uncertain(name, "a declaration it owns also bound the same object to"
                                          " another target or handed it to other code")
            else:
                # A key-named name that owns no declarations: a place not read and an uncertain
                # release both fail closed; the first of them in the statement gives the
                # message, the unread one or the uncertain-release one, each naming its kind.
                odd = [(construct, kind) for construct, kind in mine
                       if kind in ("unread", "uncertain")]
                if odd:
                    construct, kind = odd[0]
                    raise (unread if kind == "unread" else unowned_uncertain)(name, construct)
        declarations[:] = [entry for entry in declarations if entry[0] not in certain]
        before = len(declarations)
        visit(node, (), False, False, frozenset())
        for name in sorted({entry[0] for entry in declarations[before:]}):
            # The statement that makes these declarations must bind the owning name once, by
            # the binding that holds them; a second binding or deletion of the name in the same
            # statement can release them before the statement ends.
            mine = [(construct, kind) for other, construct, kind in events if other == name]
            if len(mine) > 1 or mine and not (
                    mine[0][1] in ("certain", "declaration")
                    or mine[0][0] in ("a def inside a compound statement",
                                      "an async def inside a compound statement",
                                      "a class inside a compound statement")):
                raise uncertain(name, "the statement that makes its declarations also binds or"
                                      " deletes it: " + mine[-1][0])
        made = {entry[0] for entry in declarations[before:]}
        if star_owner is None and (owners or made) and any(
                isinstance(child, ast.ImportFrom) and any(alias.name == "*" for alias in child.names)
                for child in ast.walk(node)):
            # A star import can rebind any module name: one in a statement after a declaration,
            # or in the statement that makes it (even where it runs first), is refused.
            star_owner = sorted(owners | made)[0]
        owned |= {entry[0] for entry in declarations}
    if unknown_in_bodies and (owned or key_named):
        raise unread("every key-owning name", unknown_in_bodies[0])
    if star_owner is not None:
        raise ValueError(
            f"{label}: a star import after a declaration of {star_owner}, which owns accepted"
            " keys, or in the statement that makes it, can rebind any module name; the check"
            " cannot decide the floor")
    for name, identity, construct in bound_in_bodies:
        if name in owned:
            raise unread(identity, construct)
    for name in sorted(deferred):
        if name in owned:
            raise uncertain(name, "a global statement names it: a function or class body that"
                                  " declares it global can bind or delete it when that body"
                                  " runs, and a module-level global statement is refused too")
        if _key_named(name):
            raise unread(name, "a global statement, which lets a function or class body bind or"
                               " delete it")
    keys = set().union(*(found for _, found, _, _ in declarations))
    if not keys:
        return {}
    # Each view is one reading of the module's accepted keys (_KEY_VIEWS); _engine_changes
    # reports a key removed or added when any view removes or adds it.
    return {
        "module": keys,
        "module, assignments only": set().union(
            *(found for _, found, _, place in declarations if "walrus" not in place)),
        "module, outside private headers": set().union(
            *(found for _, found, _, place in declarations if "private header" not in place)),
        "module, outside lambda bodies": set().union(
            *(found for _, found, _, place in declarations if "lambda" not in place)),
        "module, outside private headers and lambda bodies": set().union(
            *(found for _, found, _, place in declarations
              if not place & {"private header", "lambda"})),
    }


def _configure_fields(node, label):
    args = node.args
    parameters = {arg.arg for arg in args.posonlyargs + args.args + args.kwonlyargs}
    if args.kwarg:
        parameters.add(args.kwarg.arg)
    result = {"keyword " + arg.arg for arg in args.args + args.kwonlyargs}

    def parameter(value):
        return isinstance(value, ast.Name) and value.id in parameters

    def literal(value):
        if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
            raise ValueError(f"{label}: dynamic configure key cannot be classified")
        return value.value

    for child in ast.walk(node):
        if isinstance(child, ast.Attribute) and parameter(child.value):
            if child.attr not in ("get", "pop", "setdefault", "keys", "items", "values"):
                result.add(f"{child.value.id}.{child.attr}")
        elif isinstance(child, ast.Subscript) and parameter(child.value):
            result.add(f"{child.value.id}[{literal(child.slice)!r}]")
        elif isinstance(child, ast.Call):
            if (isinstance(child.func, ast.Name)
                    and child.func.id in ("getattr", "hasattr")
                    and len(child.args) >= 2 and parameter(child.args[0])):
                result.add(f"{child.args[0].id}.{literal(child.args[1])}")
            elif (isinstance(child.func, ast.Attribute)
                    and parameter(child.func.value)
                    and child.func.attr in ("get", "pop", "setdefault") and child.args):
                result.add(f"{child.func.value.id}[{literal(child.args[0])!r}]")
    return result


def _bound_names(target):
    # The module names an assignment target binds: a name, or the names inside a tuple, list or
    # starred target. An attribute or subscript target binds no module name.
    if isinstance(target, ast.Name):
        yield target.id
    elif isinstance(target, (ast.Tuple, ast.List)):
        for element in target.elts:
            yield from _bound_names(element)
    elif isinstance(target, ast.Starred):
        yield from _bound_names(target.value)


_COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
_SIMPLE = (ast.Pass, ast.Break, ast.Continue, ast.Global, ast.Nonlocal)
# Every expression node type of the ast grammar that binds or deletes no name by itself, so
# its children are read in place. The parts that bind are read by name in _binding_events.
_EXPRESSIONS = (
    ast.Attribute, ast.Await, ast.BinOp, ast.BoolOp, ast.Call, ast.Compare, ast.Constant,
    ast.Dict, ast.FormattedValue, ast.IfExp, ast.Interpolation, ast.JoinedStr, ast.List,
    ast.Set, ast.Slice, ast.Starred, ast.Subscript, ast.TemplateStr, ast.Tuple, ast.UnaryOp,
    ast.Yield, ast.YieldFrom, ast.keyword, ast.expr_context, ast.boolop, ast.operator,
    ast.unaryop, ast.cmpop,
)
# Every match pattern node type of the ast grammar; _binding_events reads each one's captures
# and expressions, and any other pattern type is a node the check does not know.
_PATTERNS = (
    ast.MatchAs, ast.MatchClass, ast.MatchMapping, ast.MatchOr, ast.MatchSequence,
    ast.MatchSingleton, ast.MatchStar, ast.MatchValue,
)
# Every node type of the ast grammar that _accepted_sets reads in a public def or class body:
# each statement, expression and match pattern, and the parts that hold them. Any other node
# type there is a node the check does not know.
_BODY_NODES = (
    ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Return, ast.Delete, ast.Assign,
    ast.TypeAlias, ast.AugAssign, ast.AnnAssign, ast.For, ast.AsyncFor, ast.While, ast.If,
    ast.With, ast.AsyncWith, ast.Match, ast.Raise, ast.Try, ast.TryStar, ast.Assert,
    ast.Import, ast.ImportFrom, ast.Expr, *_SIMPLE, *_EXPRESSIONS, *_PATTERNS,
    *_COMPREHENSIONS, ast.Name, ast.NamedExpr, ast.Lambda, ast.TypeVar, ast.ParamSpec,
    ast.TypeVarTuple, ast.arguments, ast.arg, ast.alias, ast.withitem, ast.match_case,
    ast.ExceptHandler, ast.comprehension,
)


def _binding_events(node):
    # Every place a top-level statement can bind or delete a module name when it runs, at any
    # depth outside nested function, class and lambda bodies and comprehension targets (which
    # bind names of their own scope; a global statement there is read module-wide by
    # _accepted_sets), as (name, construct, kind) events. kind is "certain" (a certain release),
    # "declaration" (a place _accepted_sets reads as a declaration of a key-named name and an
    # uncertain release), "uncertain" (an uncertain release) or "unread" (a place the check does
    # not read). A name of None marks a node type (a statement, an expression or a match
    # pattern) the check does not know. Every expression of
    # a def or class header outside its body is read (a decorator, a default value, an argument
    # or return annotation, a type parameter's bound or default, a class base or keyword), as
    # are a lambda's defaults, an annotation and, for a type statement, its value and each type
    # parameter's bound (a TypeVar has one) and default; a type parameter's own name binds in
    # the type statement's own scope and is not read;
    # an assignment expression in any of these headers is unread (the walker reads the ast;
    # _surface then compiles the tree, so a header assignment expression that Python rejects,
    # such as one in an annotation, also fails closed through that compile). The first iterable of a
    # comprehension runs in module scope, and an assignment expression in a comprehension
    # binds in the scope around it. A comprehension target that is not a name (a subscript or
    # attribute, alone or inside a tuple, list or starred target) is read as an expression of
    # the same header. An annotation without a value binds nothing (one whose target is keys
    # or a *_keys name fails closed in _accepted_sets;
    # specification-audit-programme.md, section 6, gate 99, states the outcome).
    events = []
    unpacked = " (inside a tuple, list or starred target)"

    def add(name, construct, kind):
        events.append((name, construct, kind))

    def target(child, construct, kind, header, suffix=unpacked):
        if isinstance(child, ast.Name):
            add(child.id, construct, kind)
        elif isinstance(child, (ast.Tuple, ast.List, ast.Starred)):
            # The suffix is added once, however deeply the target nests. ast.parse also
            # accepts a starred target with no tuple or list around it as the whole target of
            # an assignment, for or with (only compile refuses it), so a starred target adds
            # the suffix itself when nothing around it did; every name inside is read as
            # unread either way, so the check fails closed before _surface's compile step
            # (specification-audit-programme.md, section 6, gate 99, states the outcome). An
            # empty suffix keeps the construct as given for every name the target holds.
            if suffix and not construct.endswith(suffix):
                construct += suffix
            for element in (child.value,) if isinstance(child, ast.Starred) else child.elts:
                target(element, construct, "unread", header, suffix)
        else:
            expression(child, header)

    def arguments(args, header):
        for arg in (*args.posonlyargs, *args.args, args.vararg, *args.kwonlyargs, args.kwarg):
            if arg is not None and arg.annotation is not None:
                expression(arg.annotation, header)
        for value in (*args.defaults, *args.kw_defaults):
            if value is not None:
                expression(value, header)

    def expression(child, header):
        if isinstance(child, ast.Name):
            if not isinstance(child.ctx, ast.Load):
                add(child.id, "a name stored or deleted in an expression", "unread")
        elif isinstance(child, ast.NamedExpr):
            if header:
                add(child.target.id, f"an assignment expression in {header}", "unread")
            else:
                add(child.target.id, "an assignment expression", "declaration")
            expression(child.value, header)
        elif isinstance(child, ast.Lambda):
            arguments(child.args, header or "a lambda header")
        elif isinstance(child, _COMPREHENSIONS):
            for generator in child.generators:
                comprehension_target(generator.target, header)
                expression(generator.iter, header)
                for condition in generator.ifs:
                    expression(condition, header)
            for part in ("elt", "key", "value"):
                if getattr(child, part, None) is not None:
                    expression(getattr(child, part), header)
        elif isinstance(child, (ast.TypeVar, ast.ParamSpec, ast.TypeVarTuple)):
            for part in (getattr(child, "bound", None), child.default_value):
                if part is not None:
                    expression(part, header)
        elif isinstance(child, _EXPRESSIONS):
            for part in ast.iter_child_nodes(child):
                expression(part, header)
        else:
            add(None, f"a {type(child).__name__} node, which the check does not know", "unread")

    def comprehension_target(child, header):
        # A name target binds a name of the comprehension's own scope; every other part of a
        # target is an expression, where an assignment expression binds in the scope around it.
        if isinstance(child, (ast.Tuple, ast.List)):
            for element in child.elts:
                comprehension_target(element, header)
        elif isinstance(child, ast.Starred):
            comprehension_target(child.value, header)
        elif not isinstance(child, ast.Name):
            expression(child, header)

    def pattern(child):
        if not isinstance(child, _PATTERNS):
            add(None, f"a {type(child).__name__} pattern, which the check does not know",
                "unread")
            return
        if isinstance(child, (ast.MatchAs, ast.MatchStar)) and child.name:
            add(child.name, "a match capture", "uncertain")
        if isinstance(child, ast.MatchMapping) and child.rest:
            add(child.rest, "a match mapping rest", "uncertain")
        for part in ast.iter_child_nodes(child):
            if isinstance(part, ast.pattern):
                pattern(part)
            else:
                expression(part, "")

    def statement(child, top):
        inner = "" if top else " inside a compound statement"
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            is_class = isinstance(child, ast.ClassDef)
            add(child.name, ("a class" if is_class
                             else "an async def" if isinstance(child, ast.AsyncFunctionDef)
                             else "a def") + inner,
                "certain" if top else "uncertain")
            header = "a class header" if is_class else "a def header"
            for part in (*child.decorator_list, *child.type_params):
                expression(part, header)
            if is_class:
                for part in (*child.bases, *child.keywords):
                    expression(part, header)
            else:
                arguments(child.args, header)
                if child.returns is not None:
                    expression(child.returns, header)
        elif isinstance(child, ast.Assign):
            for part in child.targets:
                target(part, "an assignment" + inner, "certain" if top else "declaration", "")
            expression(child.value, "")
        elif isinstance(child, ast.AugAssign):
            target(child.target, "an augmented assignment" + inner,
                   "certain" if top else "uncertain", "")
            expression(child.value, "")
        elif isinstance(child, ast.AnnAssign):
            expression(child.annotation, "an annotation")
            if child.value is None:
                if not isinstance(child.target, ast.Name):
                    expression(child.target, "")
            else:
                target(child.target, "an annotated assignment" + inner,
                       "certain" if top else "declaration", "")
                expression(child.value, "")
        elif isinstance(child, ast.Delete):
            for part in child.targets:
                target(part, "a del" + inner, "certain" if top else "uncertain", "")
        elif isinstance(child, (ast.Import, ast.ImportFrom)):
            for alias in child.names:
                if alias.name != "*":
                    add(alias.asname or alias.name.split(".")[0], "an import" + inner,
                        "certain" if top else "uncertain")
        elif isinstance(child, (ast.For, ast.AsyncFor)):
            target(child.target, ("an async for target" if isinstance(child, ast.AsyncFor)
                                  else "a for target") + inner, "uncertain", "")
            expression(child.iter, "")
            for part in (*child.body, *child.orelse):
                statement(part, False)
        elif isinstance(child, (ast.While, ast.If)):
            expression(child.test, "")
            for part in (*child.body, *child.orelse):
                statement(part, False)
        elif isinstance(child, (ast.With, ast.AsyncWith)):
            is_async = isinstance(child, ast.AsyncWith)
            construct = "an async with target" if is_async else "a with target"
            for index, item in enumerate(child.items):
                expression(item.context_expr, "")
                if item.optional_vars is None:
                    continue
                # For an async with item and a with item after the first (the two branches below
                # that set a reason, not the else branch for the first item of a plain with),
                # the reason depends on the construct and the item's position only, never
                # on the target's form or on whether the statement is top-level: a plain name
                # and every name an unpacking target holds get the same reason at any depth
                # (the empty suffix keeps it unchanged for each name). Only the kind can
                # differ: for a plain-name target it follows the depth (unread at top level,
                # uncertain inside a compound statement), and target() reads every name inside
                # an unpacking target as unread at any depth.
                if is_async:
                    # An async with compiles only in an async def body, which this walker
                    # never enters, so one at any depth here never compiles and its target is
                    # never read as a certain release (_surface's compile step refuses the
                    # module too, after the walker). This check comes first for every item:
                    # the second-item reason describes an earlier context manager skipping a
                    # later target of a statement that runs, and the unpacking suffix
                    # describes how a statement that runs binds, but this one never runs.
                    reason = construct + " outside an async def, which does not compile"
                elif index:
                    reason = construct + (" after the first item, which an earlier context"
                                          " manager can skip")
                else:
                    target(item.optional_vars, construct + inner,
                           "certain" if top else "uncertain", "")
                    continue
                target(item.optional_vars, reason, "unread" if top else "uncertain", "", "")
            for part in child.body:
                statement(part, False)
        elif isinstance(child, ast.Match):
            expression(child.subject, "")
            for case in child.cases:
                pattern(case.pattern)
                if case.guard is not None:
                    expression(case.guard, "")
                for part in case.body:
                    statement(part, False)
        elif isinstance(child, (ast.Try, ast.TryStar)):
            for part in child.body:
                statement(part, False)
            for handler in child.handlers:
                if handler.type is not None:
                    expression(handler.type, "")
                if handler.name:
                    add(handler.name, "an except name", "uncertain")
                for part in handler.body:
                    statement(part, False)
            for part in (*child.orelse, *child.finalbody):
                statement(part, False)
        elif isinstance(child, ast.TypeAlias):
            target(child.name, "a type statement", "uncertain", "")
            for part in (*child.type_params, child.value):
                expression(part, "a type statement")
        elif isinstance(child, (ast.Expr, ast.Return, ast.Raise, ast.Assert)):
            for part in ast.iter_child_nodes(child):
                expression(part, "")
        elif not isinstance(child, _SIMPLE):
            add(None, f"a {type(child).__name__} statement, which the check does not know",
                "unread")

    statement(node, True)
    return events


def _hands_off(node):
    # Whether running a top-level def or class statement can pass the object it binds, or an
    # object its body makes, to other code without an ast.Name load of the bound name. A def
    # hands off when it has a decorator. A class always hands off: the class statement calls
    # builtins.__build_class__ with the class body, and any code in the process can replace
    # that function, so the class and its methods can be kept by a hook the module never
    # names (a deliberate over-refusal for a class nothing hooks).
    if isinstance(node, ast.ClassDef):
        return True
    return bool(node.decorator_list)


def _api(raw, label):
    """Return a module's public surface: (symbols, configure inputs, accepted-key sets).

    symbols maps each public name bound by a top-level statement to (kind, parameters):
    a def or async def ("function"), a class ("class"), or an assignment ("assignment",
    no parameters). An assignment counts when the name has no leading underscore and a
    top-level plain Assign binds it directly or inside a tuple, list or starred target, or a
    top-level AnnAssign with a value binds it directly (an annotated assignment has one
    target and cannot unpack). Rebinding a name by assignment is one entry. Any two bindings
    of one public name by def, class or assignment, at least one of them a def or class, with
    no top-level del of that name between them, are ambiguous and fail closed. A top-level
    del of a name drops what was recorded for it (its symbol; for configure, its
    configure inputs; what it drops of accepted keys is stated in the module docstring's
    section "Accepted-key declaration and removal rules")
    and lets a later def, class or assignment bind the name again. A top-level
    del of a counted name is a removal unless a later top-level def, class or assignment
    binds the name again; a name bound again is compared as its last binding (its kind,
    parameters and configure inputs against the base). The rules by which _accepted_sets
    reads accepted keys, and what it does not see, are stated once, in the module
    docstring, section "Accepted-key declaration and removal rules"; this docstring does
    not restate them. The release level each kind of change needs, and the exit status
    of a refusal, are stated once, in the specification
    (specs/specification-audit-programme.md, section 6, gate 99), whose rules point to the
    rows of _RELEASE_CASES that exercise them.

    Not seen; the level each such edit needs is the matching row of _RELEASE_CASES (an
    accepted-key declaration made in one of these places, such as an assignment expression
    or an assignment inside a block, is still read by the module docstring's rule section): the value of an assignment (a changed
    constant or pattern keeps its name and kind); a name made public or private by __all__
    (the list is not read); a re-export or alias by import (import and from-import bindings
    are not read); a binding or del only inside a top-level if, try, with, for, while or
    match block; a binding by augmented assignment, by a walrus expression, by a type
    statement, by an annotation without a value (one whose target is keys or a *_keys name
    is refused, as the module docstring's rule section states), or through globals(); attributes of a
    class or instance; and each accepted-key case the module docstring's rule section
    lists as not seen. Replacing a counted
    name with one of
    these unseen bindings (LIMIT = 3
    becoming LIMIT: int, or from os import sep as LIMIT) drops the name from the surface; the
    level it needs is the matching row of _RELEASE_CASES.
    """
    if raw is None:
        return {}, {}, {}
    try:
        return _surface(raw, label)
    except RecursionError as exc:
        raise ValueError(f"{label}: nested too deeply for the check to read ({exc}); the check"
                         " cannot decide the floor") from exc


def _surface(raw, label):
    # _api's reading of a module that is not None; a RecursionError here is an input error.
    try:
        tree = ast.parse(raw, filename=label)
    except (SyntaxError, ValueError) as exc:
        raise ValueError(f"{label}: invalid Python: {exc}") from exc
    except (MemoryError, RecursionError) as exc:
        # The parser gives up on a module too complex for it (a very deep expression) with a
        # MemoryError or RecursionError: an input the check cannot read, so it fails closed.
        raise ValueError(f"{label}: too complex for the check to parse ({exc}); the check"
                         " cannot decide the floor") from exc
    symbols = {}
    config = {}
    defined = set()
    assigned = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                if node.name in defined or node.name in assigned:
                    raise ValueError(f"{label}: ambiguous public definition {node.name}")
                defined.add(node.name)
                is_class = isinstance(node, ast.ClassDef)
                parameters = _class_parameters(node) if is_class else _parameters(node)
                symbols[node.name] = ("class" if is_class else "function", parameters)
                if node.name == "configure" and not is_class:
                    config["configure"] = _configure_fields(node, label)
        elif isinstance(node, ast.Assign) or (
                isinstance(node, ast.AnnAssign) and node.value is not None):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                for name in _bound_names(target):
                    if not name.startswith("_"):
                        if name in defined:
                            raise ValueError(f"{label}: ambiguous public definition {name}")
                        assigned.add(name)
                        symbols[name] = ("assignment", set())
        elif isinstance(node, ast.Delete):
            # A top-level del unbinds the name until a later top-level def, class or assignment
            # binds it again, so a binding after the del does not clash with one before it, and
            # drops everything recorded for the name: a deleted configure's inputs go with it
            # (_accepted_sets drops the deleted binding's accepted keys the same way).
            for target in node.targets:
                for name in _bound_names(target):
                    symbols.pop(name, None)
                    config.pop(name, None)
                    defined.discard(name)
                    assigned.discard(name)
    sets = _accepted_sets(tree, label)
    try:
        # A tree that parses can still be refused by the compiler (for example an assignment
        # expression in a comprehension directly in a class body), and the walker would read
        # declarations that cannot exist; such a module fails closed. dont_inherit keeps this
        # module's future flags out of the compile.
        compile(tree, label, "exec", dont_inherit=True)
    except (SyntaxError, ValueError, TypeError) as exc:
        raise ValueError(f"{label}: invalid Python: {exc}; the check cannot decide the floor") from exc
    except MemoryError as exc:
        raise ValueError(f"{label}: too complex for the check to compile ({exc}); the check"
                         " cannot decide the floor") from exc
    return symbols, config, sets


def _set_changes(left, right, label, emit):
    for item in sorted(left - right):
        emit(3, f"{label}: removed {item}")
    for item in sorted(right - left):
        emit(2, f"{label}: added {item}")


# The views of a module's accepted keys that _engine_changes compares: every declaration;
# only the declarations that are assignments or annotated assignments (an assignment
# expression, such as one binding a lambda local in a public def or class, never hides the
# removal of a key an assignment held); every declaration outside a header of a private def
# or class nested in a public def or class; every declaration outside every lambda body
# (a lambda local declaration never hides the removal of a key an assignment expression
# outside every lambda body held); and every declaration outside both such headers and every
# lambda body (a lambda local declaration beside a private header never hides it either).
# Every declaration in a private header or a lambda body is an assignment expression, so
# these views exclude every combination of the three markers.
_KEY_VIEWS = ("module", "module, assignments only", "module, outside private headers",
              "module, outside lambda bodies", "module, outside private headers and lambda bodies")

# The release-level table: the one statement of the level each listed change needs. Each row
# is (the change, where it sits, the base source, the head source, the outcome); the sources
# are appended to an engine module, and the outcome is a release level or one of two refusal
# outcomes, a refused head or a refused base with an accepted head;
# specification-audit-programme.md, section 6, gate 99, states what each outcome means.
# test_release_level_table in tests/test_cm_release_delta.py
# runs every row through check() with the lowest bump claimed and asserts its outcome. A
# refused base stops the check before it reads the head, so the test also runs each refused
# head alone against an accepted base and each refused base alone against an accepted head,
# and requires the head of a refused-base row to be accepted.
_OWNER = "def load():\n    profile_keys = {'a'}\n"
_RELEASE_CASES = (
    ("walrus to a *_keys name, key removed from its value", "a module-level lambda body",
     "value = lambda: (profile_keys := {'a', 'b'})\n",
     "value = lambda: (profile_keys := {'a'})\n", "PATCH"),
    ("walrus to a *_keys name, key removed from its value", "a private def body",
     "def _f():\n    value = (profile_keys := {'a', 'b'})\n",
     "def _f():\n    value = (profile_keys := {'a'})\n", "PATCH"),
    ("walrus to a *_keys name, key removed from its value", "a module-level lambda default",
     "value = lambda x=(profile_keys := {'a', 'b'}): x\n",
     "value = lambda x=(profile_keys := {'a'}): x\n", "exit 2"),
    ("walrus to a *_keys name, key removed from its value", "a top-level def header",
     "def f(x=(profile_keys := {'a', 'b'})):\n    pass\n",
     "def f(x=(profile_keys := {'a'})):\n    pass\n", "exit 2"),
    ("walrus to a *_keys name, key removed from its value", "a top-level plain assignment",
     "value = (profile_keys := {'a', 'b'})\n", "value = (profile_keys := {'a'})\n", "MAJOR"),
    ("walrus to a *_keys name, key added to its value", "a top-level plain assignment",
     "value = (profile_keys := {'a'})\n", "value = (profile_keys := {'a', 'b'})\n", "MINOR"),
    ("walrus to a keys name, key removed from its value", "a top-level plain assignment",
     "value = (keys := {'a', 'b'})\n", "value = (keys := {'a'})\n", "MAJOR"),
    ("walrus to a *_keys name, key removed from its value", "a public def body",
     "def f():\n    value = (profile_keys := {'a', 'b'})\n",
     "def f():\n    value = (profile_keys := {'a'})\n", "MAJOR"),
    ("walrus to a *_keys name, key removed from its value", "a lambda body in a public def body",
     "def f():\n    value = lambda: (profile_keys := {'a', 'b'})\n",
     "def f():\n    value = lambda: (profile_keys := {'a'})\n", "MAJOR"),
    ("walrus to a *_keys name moved into a lambda body", "a public def body",
     "def f():\n    value = (profile_keys := {'a', 'b'})\n",
     "def f():\n    value = lambda: (profile_keys := {'a', 'b'})\n", "MAJOR"),
    ("walrus to a *_keys name moved out of a lambda body", "a public def body",
     "def f():\n    value = lambda: (profile_keys := {'a', 'b'})\n",
     "def f():\n    value = (profile_keys := {'a', 'b'})\n", "MINOR"),
    ("*_keys assignment moved to a walrus", "a public def body",
     "def f():\n    profile_keys = {'a', 'b'}\n",
     "def f():\n    return (profile_keys := {'a', 'b'})\n", "MAJOR"),
    ("*_keys walrus moved to an assignment", "a public def body",
     "def f():\n    return (profile_keys := {'a', 'b'})\n",
     "def f():\n    profile_keys = {'a', 'b'}\n", "MINOR"),
    ("changed constant value", "a top-level plain assignment to a public name",
     "LIMIT = 3\n", "LIMIT = 4\n", "PATCH"),
    ("changed value, key removed", "a top-level plain assignment to a *_keys name",
     "profile_keys = {'a', 'b'}\n", "profile_keys = {'a'}\n", "MAJOR"),
    ("changed value, key removed", "a *_keys assignment in a private def body",
     "def _f():\n    profile_keys = {'a', 'b'}\n", "def _f():\n    profile_keys = {'a'}\n",
     "PATCH"),
    ("public name added", "a top-level plain assignment", "", "LIMIT = 3\n", "MINOR"),
    ("import alias added", "a top-level from-import", "",
     "from re import compile as COMPILE\n", "PATCH"),
    ("__all__ added", "a top-level plain assignment", "", "__all__ = ['public']\n", "PATCH"),
    ("counted public name replaced by an import alias", "a top-level from-import",
     "LIMIT = 3\n", "from os import sep as LIMIT\n", "MAJOR"),
    ("*_keys name replaced by an unreferenced import alias", "a top-level from-import",
     "profile_keys = {'a', 'b'}\n", "from os import sep as profile_keys\n", "MAJOR"),
    ("binding of a name that is not key-named added", "a public def body",
     "def f():\n    return 1\n", "def f():\n    limit = 3\n    return 1\n", "PATCH"),
    ("binding of a name that is not key-named added", "a private def body",
     "def _f():\n    return 1\n", "def _f():\n    limit = 3\n    return 1\n", "PATCH"),
    ("key-owning name bound by a for target", "a public def body", _OWNER,
     _OWNER + "def f():\n    for load in ():\n        pass\n", "exit 2"),
    ("key-owning name bound by a with target", "a public def body", _OWNER,
     _OWNER + "def f():\n    with open(__file__) as load:\n        pass\n", "exit 2"),
    ("key-owning name bound by an augmented assignment", "a public def body", _OWNER,
     _OWNER + "def f():\n    load += 1\n", "exit 2"),
    ("key-owning name bound by a type statement", "a public def body", _OWNER,
     _OWNER + "def f():\n    type load = int\n", "exit 2"),
    ("key-owning name bound by a match capture", "a public def body", _OWNER,
     _OWNER + "def f(x):\n    match x:\n        case load:\n            pass\n", "exit 2"),
    ("key-owning name deleted by a del of a tuple", "a public def body", _OWNER,
     _OWNER + "def f():\n    del (load,)\n", "exit 2"),
    ("key-owning name deleted by a del of a list", "a public def body", _OWNER,
     _OWNER + "def f():\n    del [load]\n", "exit 2"),
    ("key-owning name bound by a nested def", "a public def body", _OWNER,
     _OWNER + "def f():\n    def load():\n        pass\n", "exit 2"),
    ("key-owning name bound by a plain assignment", "a public def body",
     _OWNER + "def f():\n    return 1\n", _OWNER + "def f():\n    load = 1\n", "PATCH"),
    ("key-named name that owns no declarations bound by a for target", "a top-level for",
     "", "for profile_keys in ():\n    pass\n", "exit 2"),
    ("global statement naming a *_keys name", "a public def body",
     "profile_keys = {'a', 'b'}\n",
     "profile_keys = {'a', 'b'}\ndef f():\n    global profile_keys\n", "exit 2"),
    ("walrus to a *_keys name added", "a module-level lambda default",
     "value = lambda x=None: x\n", "value = lambda x=(profile_keys := {'a'}): x\n", "exit 2"),
    ("walrus to a *_keys name removed", "a module-level lambda default",
     "value = lambda x=(profile_keys := {'a'}): x\n", "value = lambda x=None: x\n",
     "exit 2, base refused"),
    ("walrus to a *_keys name added", "a top-level def header",
     "def f(x=None):\n    pass\n", "def f(x=(profile_keys := {'a'})):\n    pass\n", "exit 2"),
    ("walrus to a *_keys name removed", "a top-level def header",
     "def f(x=(profile_keys := {'a'})):\n    pass\n", "def f(x=None):\n    pass\n",
     "exit 2, base refused"),
    ("walrus to a *_keys name, key removed from its value",
     "a header of a private def nested in a public def body",
     "def f():\n    def _h(x=(profile_keys := {'a', 'b'})):\n        pass\n",
     "def f():\n    def _h(x=(profile_keys := {'a'})):\n        pass\n", "MAJOR"),
    ("walrus to a *_keys name, key removed from its value", "a public class body",
     "class C:\n    value = (profile_keys := {'a', 'b'})\n",
     "class C:\n    value = (profile_keys := {'a'})\n", "MAJOR"),
    ("changed value, key removed", "a *_keys assignment in a public class body",
     "class C:\n    profile_keys = {'a', 'b'}\n", "class C:\n    profile_keys = {'a'}\n",
     "MAJOR"),
    ("changed value, key removed", "a *_keys assignment in a private class body",
     "class _C:\n    profile_keys = {'a', 'b'}\n", "class _C:\n    profile_keys = {'a'}\n",
     "PATCH"),
    ("binding of a name that is not key-named added", "a public class body",
     "class C:\n    pass\n", "class C:\n    limit = 3\n", "PATCH"),
    ("key-owning name bound by a plain assignment", "a public class body",
     _OWNER + "class C:\n    pass\n", _OWNER + "class C:\n    load = 1\n", "PATCH"),
    ("key-owning name bound by a def (a method named like it)", "a public class body", _OWNER,
     _OWNER + "class C:\n    def load(self):\n        pass\n", "exit 2"),
    ("key-owning name bound by a for target", "a public class body", _OWNER,
     _OWNER + "class C:\n    for load in ():\n        pass\n", "exit 2"),
    ("key-owning name bound by an except name", "a public def body", _OWNER,
     _OWNER + "def f():\n    try:\n        pass\n    except Exception as load:\n        pass\n",
     "exit 2"),
    ("key-owning name bound by an except name (of an except* clause)", "a public def body",
     _OWNER,
     _OWNER + "def f():\n    try:\n        pass\n    except* Exception as load:\n        pass\n",
     "exit 2"),
    ("key-owning name bound by an except name (of an except* clause)", "a public class body",
     _OWNER,
     _OWNER + "class C:\n    try:\n        pass\n    except* Exception as load:\n        pass\n",
     "exit 2"),
    ("key-owning name bound by an import", "a public def body", _OWNER,
     _OWNER + "def f():\n    import os as load\n", "exit 2"),
    ("key-owning name bound by a from-import", "a public def body", _OWNER,
     _OWNER + "def f():\n    from os import sep as load\n", "exit 2"),
    ("key-owning name bound by an async for target", "a public async def body", _OWNER,
     _OWNER + "async def f():\n    async for load in g():\n        pass\n", "exit 2"),
    ("key-owning name bound by an async with target", "a public async def body", _OWNER,
     _OWNER + "async def f():\n    async with g() as load:\n        pass\n", "exit 2"),
    ("key-owning name deleted by a del of the plain name", "a public def body", _OWNER,
     _OWNER + "def f():\n    del load\n", "exit 2"),
    ("key-owning name bound by a starred target", "a public def body", _OWNER,
     _OWNER + "def f():\n    *load, = ()\n", "exit 2"),
    ("key-owning name bound by a tuple target", "a public def body", _OWNER,
     _OWNER + "def f():\n    load, other = 1, 2\n", "exit 2"),
    ("key-owning name bound by a nested class", "a public def body", _OWNER,
     _OWNER + "def f():\n    class load:\n        pass\n", "exit 2"),
    ("key-owning name bound by a nested async def", "a public def body", _OWNER,
     _OWNER + "def f():\n    async def load():\n        pass\n", "exit 2"),
    ("key-owning name bound by an annotated assignment", "a public def body",
     _OWNER + "def f():\n    return 1\n", _OWNER + "def f():\n    load: int = 1\n", "PATCH"),
    ("key-owning name bound by an assignment expression", "a public def body",
     _OWNER + "def f():\n    return 1\n", _OWNER + "def f():\n    return (load := 1)\n",
     "PATCH"),
    ("augmented assignment (|=) to a *_keys name", "a public def body",
     "def f():\n    profile_keys = {'a'}\n",
     "def f():\n    profile_keys = {'a'}\n    profile_keys |= {'b'}\n", "exit 2"),
    ("*_keys name bound in a tuple target", "a top-level assignment",
     "", "profile_keys, other = {'a'}, 1\n", "exit 2"),
    ("*_keys name deleted by a del of a tuple", "a top-level del",
     "profile_keys = {'k'}\n", "profile_keys = {'k'}\ndel (profile_keys,)\n", "exit 2"),
    ("star import added", "a top-level from-import after a key-owning declaration",
     "", "from os import *\n", "exit 2"),
    ('*_keys name bound by an assignment added', 'module level',
     '',
     "profile_keys = {'a'}\n", 'MINOR'),
    ('*_keys name bound by an assignment removed', 'module level',
     "profile_keys = {'a'}\n",
     '', 'MAJOR'),
    ('*_keys name bound by an assignment renamed', 'module level',
     "profile_keys = {'a'}\n",
     "other_keys = {'a'}\n", 'MAJOR'),
    ('*_keys name bound by an assignment expression added', 'module level',
     '',
     "_value = (profile_keys := {'a'})\n", 'MINOR'),
    ('*_keys name bound by an assignment expression removed', 'module level',
     "_value = (profile_keys := {'a'})\n",
     '', 'MAJOR'),
    ('*_keys name bound by an assignment expression renamed', 'module level',
     "_value = (profile_keys := {'a'})\n",
     "_value = (other_keys := {'a'})\n", 'PATCH'),
    ('*_keys name bound by an annotation without a value added', 'module level',
     '',
     'profile_keys: int\n', 'exit 2'),
    ('*_keys name bound by an annotation without a value removed', 'module level',
     'profile_keys: int\n',
     '', 'exit 2, base refused'),
    ('*_keys name bound by an annotation without a value renamed', 'module level',
     'profile_keys: int\n',
     'other_keys: int\n', 'exit 2'),
    ('*_keys name bound by an import alias added', 'module level',
     '',
     'from os import sep as profile_keys\n', 'PATCH'),
    ('*_keys name bound by an import alias removed', 'module level',
     'from os import sep as profile_keys\n',
     '', 'PATCH'),
    ('*_keys name bound by an import alias renamed', 'module level',
     'from os import sep as profile_keys\n',
     'from os import sep as other_keys\n', 'PATCH'),
    ('*_keys name bound by a binding only inside a top-level if added', 'module level',
     '',
     "if True:\n    profile_keys = {'a'}\n", 'MINOR'),
    ('*_keys name bound by a binding only inside a top-level if removed', 'module level',
     "if True:\n    profile_keys = {'a'}\n",
     '', 'MAJOR'),
    ('*_keys name bound by a binding only inside a top-level if renamed', 'module level',
     "if True:\n    profile_keys = {'a'}\n",
     "if True:\n    other_keys = {'a'}\n", 'PATCH'),
    ('*_keys name bound by a lambda body added', 'module level',
     '',
     "_value = lambda: (profile_keys := {'a'})\n", 'PATCH'),
    ('*_keys name bound by a lambda body removed', 'module level',
     "_value = lambda: (profile_keys := {'a'})\n",
     '', 'PATCH'),
    ('*_keys name bound by a lambda body renamed', 'module level',
     "_value = lambda: (profile_keys := {'a'})\n",
     "_value = lambda: (other_keys := {'a'})\n", 'PATCH'),
    ('*_keys name moved from an assignment to an assignment expression', 'module level',
     "profile_keys = {'a'}\n",
     "_value = (profile_keys := {'a'})\n", 'MAJOR'),
    ('*_keys name moved from an assignment to an annotation without a value', 'module level',
     "profile_keys = {'a'}\n",
     'profile_keys: int\n', 'exit 2'),
    ('*_keys name moved from an assignment to an import alias', 'module level',
     "profile_keys = {'a'}\n",
     'from os import sep as profile_keys\n', 'MAJOR'),
    ('*_keys name moved from an assignment to a binding only inside a top-level if', 'module level',
     "profile_keys = {'a'}\n",
     "if True:\n    profile_keys = {'a'}\n", 'MAJOR'),
    ('*_keys name moved from an assignment to a lambda body', 'module level',
     "profile_keys = {'a'}\n",
     "_value = lambda: (profile_keys := {'a'})\n", 'MAJOR'),
    ('*_keys name moved from an assignment expression to an assignment', 'module level',
     "_value = (profile_keys := {'a'})\n",
     "profile_keys = {'a'}\n", 'MINOR'),
    ('*_keys name moved from an assignment expression to an annotation without a value', 'module level',
     "_value = (profile_keys := {'a'})\n",
     'profile_keys: int\n', 'exit 2'),
    ('*_keys name moved from an assignment expression to an import alias', 'module level',
     "_value = (profile_keys := {'a'})\n",
     'from os import sep as profile_keys\n', 'MAJOR'),
    ('*_keys name moved from an assignment expression to a binding only inside a top-level if', 'module level',
     "_value = (profile_keys := {'a'})\n",
     "if True:\n    profile_keys = {'a'}\n", 'MINOR'),
    ('*_keys name moved from an assignment expression to a lambda body', 'module level',
     "_value = (profile_keys := {'a'})\n",
     "_value = lambda: (profile_keys := {'a'})\n", 'MAJOR'),
    ('*_keys name moved from an annotation without a value to an assignment', 'module level',
     'profile_keys: int\n',
     "profile_keys = {'a'}\n", 'exit 2, base refused'),
    ('*_keys name moved from an annotation without a value to an assignment expression', 'module level',
     'profile_keys: int\n',
     "_value = (profile_keys := {'a'})\n", 'exit 2, base refused'),
    ('*_keys name moved from an annotation without a value to an import alias', 'module level',
     'profile_keys: int\n',
     'from os import sep as profile_keys\n', 'exit 2, base refused'),
    ('*_keys name moved from an annotation without a value to a binding only inside a top-level if', 'module level',
     'profile_keys: int\n',
     "if True:\n    profile_keys = {'a'}\n", 'exit 2, base refused'),
    ('*_keys name moved from an annotation without a value to a lambda body', 'module level',
     'profile_keys: int\n',
     "_value = lambda: (profile_keys := {'a'})\n", 'exit 2, base refused'),
    ('*_keys name moved from an import alias to an assignment', 'module level',
     'from os import sep as profile_keys\n',
     "profile_keys = {'a'}\n", 'MINOR'),
    ('*_keys name moved from an import alias to an assignment expression', 'module level',
     'from os import sep as profile_keys\n',
     "_value = (profile_keys := {'a'})\n", 'MINOR'),
    ('*_keys name moved from an import alias to an annotation without a value', 'module level',
     'from os import sep as profile_keys\n',
     'profile_keys: int\n', 'exit 2'),
    ('*_keys name moved from an import alias to a binding only inside a top-level if', 'module level',
     'from os import sep as profile_keys\n',
     "if True:\n    profile_keys = {'a'}\n", 'MINOR'),
    ('*_keys name moved from an import alias to a lambda body', 'module level',
     'from os import sep as profile_keys\n',
     "_value = lambda: (profile_keys := {'a'})\n", 'PATCH'),
    ('*_keys name moved from a binding only inside a top-level if to an assignment', 'module level',
     "if True:\n    profile_keys = {'a'}\n",
     "profile_keys = {'a'}\n", 'MINOR'),
    ('*_keys name moved from a binding only inside a top-level if to an assignment expression', 'module level',
     "if True:\n    profile_keys = {'a'}\n",
     "_value = (profile_keys := {'a'})\n", 'MAJOR'),
    ('*_keys name moved from a binding only inside a top-level if to an annotation without a value', 'module level',
     "if True:\n    profile_keys = {'a'}\n",
     'profile_keys: int\n', 'exit 2'),
    ('*_keys name moved from a binding only inside a top-level if to an import alias', 'module level',
     "if True:\n    profile_keys = {'a'}\n",
     'from os import sep as profile_keys\n', 'MAJOR'),
    ('*_keys name moved from a binding only inside a top-level if to a lambda body', 'module level',
     "if True:\n    profile_keys = {'a'}\n",
     "_value = lambda: (profile_keys := {'a'})\n", 'MAJOR'),
    ('*_keys name moved from a lambda body to an assignment', 'module level',
     "_value = lambda: (profile_keys := {'a'})\n",
     "profile_keys = {'a'}\n", 'MINOR'),
    ('*_keys name moved from a lambda body to an assignment expression', 'module level',
     "_value = lambda: (profile_keys := {'a'})\n",
     "_value = (profile_keys := {'a'})\n", 'MINOR'),
    ('*_keys name moved from a lambda body to an annotation without a value', 'module level',
     "_value = lambda: (profile_keys := {'a'})\n",
     'profile_keys: int\n', 'exit 2'),
    ('*_keys name moved from a lambda body to an import alias', 'module level',
     "_value = lambda: (profile_keys := {'a'})\n",
     'from os import sep as profile_keys\n', 'PATCH'),
    ('*_keys name moved from a lambda body to a binding only inside a top-level if', 'module level',
     "_value = lambda: (profile_keys := {'a'})\n",
     "if True:\n    profile_keys = {'a'}\n", 'MINOR'),
    ('counted public name bound by an assignment removed', 'module level',
     'LIMIT = 3\n',
     '', 'MAJOR'),
    ('counted public name bound by an assignment renamed', 'module level',
     'LIMIT = 3\n',
     'BOUND = 3\n', 'MAJOR'),
    ('counted public name bound by an assignment expression added', 'module level',
     '',
     '_value = (LIMIT := 3)\n', 'PATCH'),
    ('counted public name bound by an assignment expression removed', 'module level',
     '_value = (LIMIT := 3)\n',
     '', 'PATCH'),
    ('counted public name bound by an assignment expression renamed', 'module level',
     '_value = (LIMIT := 3)\n',
     '_value = (BOUND := 3)\n', 'PATCH'),
    ('counted public name bound by an annotation without a value added', 'module level',
     '',
     'LIMIT: int\n', 'PATCH'),
    ('counted public name bound by an annotation without a value removed', 'module level',
     'LIMIT: int\n',
     '', 'PATCH'),
    ('counted public name bound by an annotation without a value renamed', 'module level',
     'LIMIT: int\n',
     'BOUND: int\n', 'PATCH'),
    ('counted public name bound by an import alias added', 'module level',
     '',
     'from os import sep as LIMIT\n', 'PATCH'),
    ('counted public name bound by an import alias removed', 'module level',
     'from os import sep as LIMIT\n',
     '', 'PATCH'),
    ('counted public name bound by an import alias renamed', 'module level',
     'from os import sep as LIMIT\n',
     'from os import sep as BOUND\n', 'PATCH'),
    ('counted public name bound by a binding only inside a top-level if added', 'module level',
     '',
     'if True:\n    LIMIT = 3\n', 'PATCH'),
    ('counted public name bound by a binding only inside a top-level if removed', 'module level',
     'if True:\n    LIMIT = 3\n',
     '', 'PATCH'),
    ('counted public name bound by a binding only inside a top-level if renamed', 'module level',
     'if True:\n    LIMIT = 3\n',
     'if True:\n    BOUND = 3\n', 'PATCH'),
    ('counted public name bound by a lambda body added', 'module level',
     '',
     '_value = lambda: (LIMIT := 3)\n', 'PATCH'),
    ('counted public name bound by a lambda body removed', 'module level',
     '_value = lambda: (LIMIT := 3)\n',
     '', 'PATCH'),
    ('counted public name bound by a lambda body renamed', 'module level',
     '_value = lambda: (LIMIT := 3)\n',
     '_value = lambda: (BOUND := 3)\n', 'PATCH'),
    ('counted public name moved from an assignment to an assignment expression', 'module level',
     'LIMIT = 3\n',
     '_value = (LIMIT := 3)\n', 'MAJOR'),
    ('counted public name moved from an assignment to an annotation without a value', 'module level',
     'LIMIT = 3\n',
     'LIMIT: int\n', 'MAJOR'),
    ('counted public name moved from an assignment to a binding only inside a top-level if', 'module level',
     'LIMIT = 3\n',
     'if True:\n    LIMIT = 3\n', 'MAJOR'),
    ('counted public name moved from an assignment to a lambda body', 'module level',
     'LIMIT = 3\n',
     '_value = lambda: (LIMIT := 3)\n', 'MAJOR'),
    ('counted public name moved from an assignment expression to an assignment', 'module level',
     '_value = (LIMIT := 3)\n',
     'LIMIT = 3\n', 'MINOR'),
    ('counted public name moved from an assignment expression to an annotation without a value', 'module level',
     '_value = (LIMIT := 3)\n',
     'LIMIT: int\n', 'PATCH'),
    ('counted public name moved from an assignment expression to an import alias', 'module level',
     '_value = (LIMIT := 3)\n',
     'from os import sep as LIMIT\n', 'PATCH'),
    ('counted public name moved from an assignment expression to a binding only inside a top-level if', 'module level',
     '_value = (LIMIT := 3)\n',
     'if True:\n    LIMIT = 3\n', 'PATCH'),
    ('counted public name moved from an assignment expression to a lambda body', 'module level',
     '_value = (LIMIT := 3)\n',
     '_value = lambda: (LIMIT := 3)\n', 'PATCH'),
    ('counted public name moved from an annotation without a value to an assignment', 'module level',
     'LIMIT: int\n',
     'LIMIT = 3\n', 'MINOR'),
    ('counted public name moved from an annotation without a value to an assignment expression', 'module level',
     'LIMIT: int\n',
     '_value = (LIMIT := 3)\n', 'PATCH'),
    ('counted public name moved from an annotation without a value to an import alias', 'module level',
     'LIMIT: int\n',
     'from os import sep as LIMIT\n', 'PATCH'),
    ('counted public name moved from an annotation without a value to a binding only inside a top-level if', 'module level',
     'LIMIT: int\n',
     'if True:\n    LIMIT = 3\n', 'PATCH'),
    ('counted public name moved from an annotation without a value to a lambda body', 'module level',
     'LIMIT: int\n',
     '_value = lambda: (LIMIT := 3)\n', 'PATCH'),
    ('counted public name moved from an import alias to an assignment', 'module level',
     'from os import sep as LIMIT\n',
     'LIMIT = 3\n', 'MINOR'),
    ('counted public name moved from an import alias to an assignment expression', 'module level',
     'from os import sep as LIMIT\n',
     '_value = (LIMIT := 3)\n', 'PATCH'),
    ('counted public name moved from an import alias to an annotation without a value', 'module level',
     'from os import sep as LIMIT\n',
     'LIMIT: int\n', 'PATCH'),
    ('counted public name moved from an import alias to a binding only inside a top-level if', 'module level',
     'from os import sep as LIMIT\n',
     'if True:\n    LIMIT = 3\n', 'PATCH'),
    ('counted public name moved from an import alias to a lambda body', 'module level',
     'from os import sep as LIMIT\n',
     '_value = lambda: (LIMIT := 3)\n', 'PATCH'),
    ('counted public name moved from a binding only inside a top-level if to an assignment', 'module level',
     'if True:\n    LIMIT = 3\n',
     'LIMIT = 3\n', 'MINOR'),
    ('counted public name moved from a binding only inside a top-level if to an assignment expression', 'module level',
     'if True:\n    LIMIT = 3\n',
     '_value = (LIMIT := 3)\n', 'PATCH'),
    ('counted public name moved from a binding only inside a top-level if to an annotation without a value', 'module level',
     'if True:\n    LIMIT = 3\n',
     'LIMIT: int\n', 'PATCH'),
    ('counted public name moved from a binding only inside a top-level if to an import alias', 'module level',
     'if True:\n    LIMIT = 3\n',
     'from os import sep as LIMIT\n', 'PATCH'),
    ('counted public name moved from a binding only inside a top-level if to a lambda body', 'module level',
     'if True:\n    LIMIT = 3\n',
     '_value = lambda: (LIMIT := 3)\n', 'PATCH'),
    ('counted public name moved from a lambda body to an assignment', 'module level',
     '_value = lambda: (LIMIT := 3)\n',
     'LIMIT = 3\n', 'MINOR'),
    ('counted public name moved from a lambda body to an assignment expression', 'module level',
     '_value = lambda: (LIMIT := 3)\n',
     '_value = (LIMIT := 3)\n', 'PATCH'),
    ('counted public name moved from a lambda body to an annotation without a value', 'module level',
     '_value = lambda: (LIMIT := 3)\n',
     'LIMIT: int\n', 'PATCH'),
    ('counted public name moved from a lambda body to an import alias', 'module level',
     '_value = lambda: (LIMIT := 3)\n',
     'from os import sep as LIMIT\n', 'PATCH'),
    ('counted public name moved from a lambda body to a binding only inside a top-level if', 'module level',
     '_value = lambda: (LIMIT := 3)\n',
     'if True:\n    LIMIT = 3\n', 'PATCH'),
    ('key-owning name bound by a match mapping rest', 'a public def body',
     _OWNER,
     _OWNER + 'def f(x):\n    match x:\n        case {**load}:\n            pass\n', 'exit 2'),
    ('key-owning name bound by a match star capture', 'a public def body',
     _OWNER,
     _OWNER + 'def f(x):\n    match x:\n        case [*load]:\n            pass\n', 'exit 2'),
    ('key-owning name bound by a list target', 'a public def body',
     _OWNER,
     _OWNER + 'def f():\n    [load, other] = 1, 2\n', 'exit 2'),
    ('key-owning name bound by a starred target with no tuple or list around it (parsed, not compiled)', 'a public def body',
     _OWNER,
     _OWNER + 'def f():\n    *load = ()\n', 'exit 2'),
    ('key-owning name bound by an unpacking for target (a tuple)', 'a public def body',
     _OWNER,
     _OWNER + 'def f():\n    for load, other in ():\n        pass\n', 'exit 2'),
    ('key-owning name bound by an unpacking for target (a list)', 'a public def body',
     _OWNER,
     _OWNER + 'def f():\n    for [load, other] in ():\n        pass\n', 'exit 2'),
    ('key-owning name bound by a starred for target with no tuple or list around it (parsed, not compiled)', 'a public def body',
     _OWNER,
     _OWNER + 'def f():\n    for *load in ():\n        pass\n', 'exit 2'),
    ('key-owning name bound by an unpacking with target (a tuple)', 'a public def body',
     _OWNER,
     _OWNER + 'def f():\n    with open(__file__) as (load, other):\n        pass\n', 'exit 2'),
    ('key-owning name bound by an unpacking with target (a list)', 'a public def body',
     _OWNER,
     _OWNER + 'def f():\n    with open(__file__) as [load, other]:\n        pass\n', 'exit 2'),
    ('key-owning name bound by a starred with target with no tuple or list around it (parsed, not compiled)', 'a public def body',
     _OWNER,
     _OWNER + 'def f():\n    with open(__file__) as *load:\n        pass\n', 'exit 2'),
    ('nonlocal statement naming a *_keys name', 'a public def nested in a public def body',
     '',
     "def f():\n    profile_keys = {'a'}\n    def g():\n        nonlocal profile_keys\n", 'exit 2'),
    ('walrus to a *_keys name added to an ordinary value', 'a top-level plain assignment',
     'value = 3\n',
     "value = (profile_keys := {'z'})\n", 'MINOR'),
    ('walrus to a *_keys name removed from an ordinary value', 'a top-level plain assignment',
     "value = (profile_keys := {'z'})\n",
     'value = 3\n', 'MAJOR'),
    ('import alias removed', 'a top-level from-import',
     'from re import compile as COMPILE\n',
     '', 'PATCH'),
    ('import alias renamed', 'a top-level from-import',
     'from re import compile as COMPILE\n',
     'from re import compile as PATTERN\n', 'PATCH'),
    ('key added to an inline set in an expression', 'a public def body',
     "def tool():\n    return 'a' in {'a'}\n",
     "def tool():\n    return 'a' in {'a', 'b'}\n", 'PATCH'),
    ('key accepted by a later add', 'a top-level expression statement',
     '',
     "KNOWN_KEYS.add('third')\n", 'PATCH'),
    ('key accepted by a |= on a name that owns no accepted-key declaration', 'a top-level augmented assignment',
     '_names = set()\n',
     "_names = set()\n_names |= {'a'}\n", 'PATCH'),
    ('augmented assignment (|=) to a *_keys name', 'a top-level if',
     '',
     "if True:\n    profile_keys |= {'a'}\n", 'exit 2'),
    ('augmented assignment (|=) to a *_keys name', 'a public class body',
     "class Tool:\n    profile_keys = {'a'}\n",
     "class Tool:\n    profile_keys = {'a'}\n    profile_keys |= {'b'}\n", 'exit 2'),
    ('public method of a public class removed', 'a public class body',
     'class Tool:\n    def run(self):\n        pass\n',
     'class Tool:\n    pass\n', 'PATCH'),
    ('class attribute value changed', 'a public class body',
     'class Tool:\n    size = 1\n',
     'class Tool:\n    size = 2\n', 'PATCH'),
    ('instance attribute value changed', 'a public def body in a public class body',
     'class Tool:\n    def run(self):\n        self.size = 1\n',
     'class Tool:\n    def run(self):\n        self.size = 2\n', 'PATCH'),
    ('parameters reordered', 'a public top-level def',
     'def tool(a, b):\n    pass\n',
     'def tool(b, a):\n    pass\n', 'PATCH'),
    ('parameter default removed', 'a public top-level def',
     'def tool(a=1):\n    pass\n',
     'def tool(a):\n    pass\n', 'PATCH'),
    ('__all__ removed', 'a top-level plain assignment',
     "__all__ = ['public']\n",
     '', 'PATCH'),
    ('counted public name bound by an augmented assignment added', 'a top-level augmented assignment',
     '',
     'LIMIT += 1\n', 'PATCH'),
    ('counted public name bound by a type statement added', 'a top-level type statement',
     '',
     'type LIMIT = int\n', 'PATCH'),
    ('counted public name bound through globals() added', 'a top-level expression',
     '',
     "globals()['LIMIT'] = 3\n", 'PATCH'),
    ('counted public name bound only inside a top-level try added', 'a top-level try',
     '',
     'try:\n    LIMIT = 3\nexcept E:\n    pass\n', 'PATCH'),
    ('counted public name bound only inside a top-level with added', 'a top-level with',
     '',
     'with f():\n    LIMIT = 3\n', 'PATCH'),
    ('counted public name bound only inside a top-level for added', 'a top-level for',
     '',
     'for _x in ():\n    LIMIT = 3\n', 'PATCH'),
    ('counted public name bound only inside a top-level while added', 'a top-level while',
     '',
     'while False:\n    LIMIT = 3\n', 'PATCH'),
    ('counted public name bound only inside a top-level match added', 'a top-level match',
     '',
     'match 1:\n    case _:\n        LIMIT = 3\n', 'PATCH'),
    ('counted public name deleted only inside a top-level if', 'a top-level if',
     'LIMIT = 3\n',
     'LIMIT = 3\nif False:\n    del LIMIT\n', 'PATCH'),
    ('key removed from one declaration while another remaining declaration holds it', 'two top-level plain assignments',
     "a_keys = {'a'}\nb_keys = {'a', 'b'}\n",
     "a_keys = {'a'}\nb_keys = {'b'}\n", 'PATCH'),
    ('key-set name bound by a top-level import added', 'a top-level from-import',
     '',
     'from os import sep as other_keys\n', 'PATCH'),
    ('*_keys name with keys replaced by a top-level import', 'a top-level from-import',
     "profile_keys = {'a'}\n",
     'from os import sep as profile_keys\n', 'MAJOR'),
    ('*_keys name with keys replaced by the first top-level with target', 'a top-level with',
     "profile_keys = {'a'}\n",
     'with f() as profile_keys:\n    pass\n', 'MAJOR'),
    ('keys of a released name removed later through a reference the check does not see', 'top-level statements',
     "profile_keys = {'a'}\n_held = globals()['profile_keys']\nprofile_keys = {'b'}\n",
     "profile_keys = {'a'}\n_held = globals()['profile_keys']\nprofile_keys = {'b'}\n_held.discard('a')\n", 'PATCH'),
    ('key-owning name bound by a nested class', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    class load:\n        pass\n', 'exit 2'),
    ('key-owning name deleted by a del of a tuple', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    del (load,)\n', 'exit 2'),
    ('key-owning name deleted by a del', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    del load\n', 'exit 2'),
    ('key-owning name bound by an annotated assignment inside a compound statement', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    profile_keys: set = {'b'}\n", 'exit 2'),
    ('key-owning name bound by an assignment, a list target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\n[profile_keys, _x] = [{'b'}, 1]\n", 'exit 2'),
    ('key-owning name bound by an assignment inside a compound statement, a list target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    [profile_keys, _x] = [{'b'}, 1]\n", 'exit 2'),
    ('key-owning name bound by an assignment inside a compound statement', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    profile_keys = [{'b'}, 1]\n", 'exit 2'),
    ('key-owning name bound by an assignment, a starred target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\n*profile_keys = [{'b'}, 1]\n", 'exit 2'),
    ('key-owning name bound by an assignment inside a compound statement, a starred target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    *profile_keys = [{'b'}, 1]\n", 'exit 2'),
    ('key-owning name bound by an assignment inside a compound statement, a tuple target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    (profile_keys, _x) = [{'b'}, 1]\n", 'exit 2'),
    ('key-owning name bound by an async for target, a list target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nasync for [profile_keys, _x] in []:\n    pass\n", 'exit 2'),
    ('key-owning name bound by an async for target inside a compound statement, a list target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    async for [profile_keys, _x] in []:\n        pass\n", 'exit 2'),
    ('key-owning name bound by an async for target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nasync for profile_keys in []:\n    pass\n", 'exit 2'),
    ('key-owning name bound by an async for target inside a compound statement', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    async for profile_keys in []:\n        pass\n", 'exit 2'),
    ('key-owning name bound by an async for target, a starred target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nasync for *profile_keys in []:\n    pass\n", 'exit 2'),
    ('key-owning name bound by an async for target inside a compound statement, a starred target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    async for *profile_keys in []:\n        pass\n", 'exit 2'),
    ('key-owning name bound by an async for target, a tuple target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nasync for (profile_keys, _x) in []:\n    pass\n", 'exit 2'),
    ('key-owning name bound by an async for target inside a compound statement, a tuple target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    async for (profile_keys, _x) in []:\n        pass\n", 'exit 2'),
    ('key-owning name bound by an async def inside a compound statement', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    async def profile_keys():\n        pass\n", 'exit 2'),
    ('key-owning name bound by an async with target outside an async def, which does not compile, a list target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nasync with open('a') as [profile_keys, _x]:\n    pass\n", 'exit 2'),
    ('key-owning name bound by an async with target outside an async def, which does not compile', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nasync with open('a') as profile_keys:\n    pass\n", 'exit 2'),
    ('key-owning name bound by an async with target outside an async def, which does not compile, a starred target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nasync with open('a') as *profile_keys:\n    pass\n", 'exit 2'),
    ('key-owning name bound by an async with target outside an async def, which does not compile, a tuple target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nasync with open('a') as (profile_keys, _x):\n    pass\n", 'exit 2'),
    ('key-owning name bound by a class inside a compound statement', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    class profile_keys:\n        pass\n", 'exit 2'),
    ('key-owning name deleted by a del, a list target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\ndel [profile_keys, _x]\n", 'exit 2'),
    ('key-owning name deleted by a del inside a compound statement, a list target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    del [profile_keys, _x]\n", 'exit 2'),
    ('key-owning name deleted by a del inside a compound statement', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    del profile_keys\n", 'exit 2'),
    ('key-owning name deleted by a del inside a compound statement, a tuple target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    del (profile_keys, _x)\n", 'exit 2'),
    ('key-owning name bound by a for target, a list target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nfor [profile_keys, _x] in []:\n    pass\n", 'exit 2'),
    ('key-owning name bound by a for target inside a compound statement, a list target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    for [profile_keys, _x] in []:\n        pass\n", 'exit 2'),
    ('key-owning name bound by a for target inside a compound statement', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    for profile_keys in []:\n        pass\n", 'exit 2'),
    ('key-owning name bound by a for target, a starred target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nfor *profile_keys in []:\n    pass\n", 'exit 2'),
    ('key-owning name bound by a for target inside a compound statement, a starred target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    for *profile_keys in []:\n        pass\n", 'exit 2'),
    ('key-owning name bound by a for target, a tuple target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nfor (profile_keys, _x) in []:\n    pass\n", 'exit 2'),
    ('key-owning name bound by a for target inside a compound statement, a tuple target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    for (profile_keys, _x) in []:\n        pass\n", 'exit 2'),
    ('key-owning name bound by a def inside a compound statement', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    def profile_keys():\n        pass\n", 'exit 2'),
    ('key-owning name bound by an import inside a compound statement (a plain import)', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    import os as profile_keys\n", 'exit 2'),
    ('key-owning name bound by an import inside a compound statement (a from-import)', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    from os import sep as profile_keys\n", 'exit 2'),
    ('key-owning name bound by a match capture', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nmatch []:\n    case profile_keys:\n        pass\n", 'exit 2'),
    ('key-owning name bound by a match mapping rest', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nmatch {}:\n    case {**profile_keys}:\n        pass\n", 'exit 2'),
    ('key-owning name bound by an assignment expression', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\n_v = (profile_keys := {'b'})\n", 'exit 2'),
    ('key-owning name bound by an assignment expression in a class header', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nclass _C((profile_keys := object)):\n    pass\n", 'exit 2'),
    ('key-owning name bound by an assignment expression in a type statement', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\ntype _T = (profile_keys := int)\n", 'exit 2'),
    ('key-owning name bound by an assignment expression in an annotation', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\n_v: (profile_keys := int) = 1\n", 'exit 2'),
    ('key-owning name bound by an except name (of an except clause)', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\ntry:\n    pass\nexcept OSError as profile_keys:\n    pass\n", 'exit 2'),
    ('key-owning name bound by an except name (of an except* clause)', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\ntry:\n    pass\nexcept* OSError as profile_keys:\n    pass\n", 'exit 2'),
    ('key-owning name bound by a type statement', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\ntype profile_keys = int\n", 'exit 2'),
    ('key-owning name bound by a with target, a list target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nwith open('a') as [profile_keys, _x]:\n    pass\n", 'exit 2'),
    ('key-owning name bound by a with target after the first item, which an earlier context manager can skip, a list target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nwith open('a') as _a, open('b') as [profile_keys, _x]:\n    pass\n", 'exit 2'),
    ('key-owning name bound by a with target inside a compound statement, a list target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    with open('a') as [profile_keys, _x]:\n        pass\n", 'exit 2'),
    ('key-owning name bound by a with target inside a compound statement', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    with open('a') as profile_keys:\n        pass\n", 'exit 2'),
    ('key-owning name bound by a with target, a starred target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nwith open('a') as *profile_keys:\n    pass\n", 'exit 2'),
    ('key-owning name bound by a with target after the first item, which an earlier context manager can skip, a starred target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nwith open('a') as _a, open('b') as *profile_keys:\n    pass\n", 'exit 2'),
    ('key-owning name bound by a with target inside a compound statement, a starred target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    with open('a') as *profile_keys:\n        pass\n", 'exit 2'),
    ('key-owning name bound by a with target, a tuple target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nwith open('a') as (profile_keys, _x):\n    pass\n", 'exit 2'),
    ('key-owning name bound by a with target after the first item, which an earlier context manager can skip, a tuple target', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nwith open('a') as _a, open('b') as (profile_keys, _x):\n    pass\n", 'exit 2'),
    ('key-owning name bound by a with target inside a compound statement, a tuple target', 'a compound statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nif True:\n    with open('a') as (profile_keys, _x):\n        pass\n", 'exit 2'),
    ('key-owning name bound by a with target after the first item, which an earlier context manager can skip', 'a top-level statement',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\nwith open('a') as _a, open('b') as profile_keys:\n    pass\n", 'exit 2'),
    ('key-owning name bound by an async for target, a list target', 'a public async def body',
     _OWNER,
     _OWNER + 'async def f():\n    async for [load, _x] in []:\n        pass\n', 'exit 2'),
    ('key-owning name bound by an async for target, a starred target', 'a public async def body',
     _OWNER,
     _OWNER + 'async def f():\n    async for *load in []:\n        pass\n', 'exit 2'),
    ('key-owning name bound by an async for target, a tuple target', 'a public async def body',
     _OWNER,
     _OWNER + 'async def f():\n    async for (load, _x) in []:\n        pass\n', 'exit 2'),
    ('key-owning name bound by an async with target, a list target', 'a public async def body',
     _OWNER,
     _OWNER + "async def f():\n    async with open('a') as [load, _x]:\n        pass\n", 'exit 2'),
    ('key-owning name bound by an async with target, a starred target', 'a public async def body',
     _OWNER,
     _OWNER + "async def f():\n    async with open('a') as *load:\n        pass\n", 'exit 2'),
    ('key-owning name bound by an async with target, a tuple target', 'a public async def body',
     _OWNER,
     _OWNER + "async def f():\n    async with open('a') as (load, _x):\n        pass\n", 'exit 2'),
    ('key-owning name bound by a match capture', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    match 1:\n        case load:\n            pass\n', 'exit 2'),
    ('key-owning name bound by a match mapping rest', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    match {}:\n        case {**load}:\n            pass\n', 'exit 2'),
    ('key-owning name bound by a tuple target', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    load, x = 1, 2\n', 'exit 2'),
    ('key-owning name bound by a type statement', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    type load = int\n', 'exit 2'),
    ('key-owning name bound by a with target', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    with f() as load:\n        pass\n', 'exit 2'),
    ('key-owning name bound by a nested async def', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    async def load(self):\n        pass\n', 'exit 2'),
    ('key-owning name bound by an async for target', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    async for load in f():\n        pass\n', 'exit 2'),
    ('key-owning name bound by an async with target', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    async with f() as load:\n        pass\n', 'exit 2'),
    ('key-owning name bound by an augmented assignment', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    load += 1\n', 'exit 2'),
    ('key-owning name bound by an except name', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    try:\n        pass\n    except E as load:\n        pass\n', 'exit 2'),
    ('key-owning name bound by an import', 'a public class body',
     _OWNER,
     _OWNER + 'class C:\n    import load\n', 'exit 2'),
    # Public surface: a counted name added, removed, renamed to a private name, changed in
    # kind or deleted by a top-level del (and bound again), a parameter added or removed,
    # and the refusals for an ambiguous public name and for a key-owning name whose release
    # cannot be read as certain.
    ('counted public name deleted by a top-level del', 'a top-level del',
     'LIMIT = 3\n', 'LIMIT = 3\ndel LIMIT\n', 'MAJOR'),
    ('counted public name deleted by a top-level del and bound again by an assignment',
     'a top-level del', 'LIMIT = 3\n', 'LIMIT = 3\ndel LIMIT\nLIMIT = 4\n', 'PATCH'),
    ('counted public name deleted by a top-level del and bound again by a def',
     'a top-level del', 'LIMIT = 3\n', 'LIMIT = 3\ndel LIMIT\ndef LIMIT():\n    pass\n',
     'MAJOR'),
    ('public def added', 'a public top-level def', '', 'def tool():\n    pass\n', 'MINOR'),
    ('public class added', 'a public top-level class', '', 'class Tool:\n    pass\n',
     'MINOR'),
    ('public def removed', 'a public top-level def', 'def tool():\n    pass\n', '', 'MAJOR'),
    ('public def renamed to a private name', 'a public top-level def',
     'def tool():\n    pass\n', 'def _tool():\n    pass\n', 'MAJOR'),
    ('public name changed from a def to a class', 'a public top-level def',
     'def tool():\n    pass\n', 'class tool:\n    pass\n', 'MAJOR'),
    ('public name changed from an assignment to a def', 'a top-level plain assignment',
     'LIMIT = 3\n', 'def LIMIT():\n    pass\n', 'MAJOR'),
    ('parameter removed', 'a public top-level def',
     'def tool(a, b):\n    pass\n', 'def tool(a):\n    pass\n', 'MAJOR'),
    ('parameter added', 'a public top-level def',
     'def tool(a):\n    pass\n', 'def tool(a, b=None):\n    pass\n', 'MINOR'),
    ('public name bound by a def and by an assignment', 'top-level statements',
     '', 'def tool():\n    pass\ntool = 1\n', 'exit 2'),
    ('key-owning name released while the module refers to it', 'top-level statements',
     "profile_keys = {'a'}\n",
     "profile_keys = {'a'}\n_held = profile_keys\nprofile_keys = {'b'}\n", 'exit 2'),
    ('key-owning name bound twice in one statement', 'a top-level chained assignment',
     '', "profile_keys = profile_keys = {'a'}\n", 'exit 2'),
    ('key-owning declaration shared by a chained assignment, then released',
     'a top-level chained assignment', '',
     "profile_keys = other = {'a'}\nprofile_keys = {'b'}\n", 'exit 2'),
)


def _engine_changes(left, right, label, emit):
    old, old_config, old_sets = _api(left, label)
    new, new_config, new_sets = _api(right, label)
    _set_changes(set(old), set(new), f"{label}: public symbol", emit)
    for name in sorted(old.keys() & new.keys()):
        if old[name][0] != new[name][0]:
            # Report the kind change alone: one kind's parameters are not removals or additions
            # of the other's (an assignment has none).
            emit(3, f"{label}: public symbol kind changed {name}")
        else:
            _set_changes(old[name][1], new[name][1], f"{label}: {name} parameter", emit)
    for name in sorted(old_config.keys() | new_config.keys()):
        _set_changes(old_config.get(name, set()), new_config.get(name, set()),
                     f"{label}: configure input {name}", emit)
    # A key is removed (or added) when any view of the accepted keys removes (or adds) it, so
    # a declaration read in only one view never hides a removal another view reports.
    removed = set().union(*(old_sets.get(view, set()) - new_sets.get(view, set())
                            for view in _KEY_VIEWS))
    added = set().union(*(new_sets.get(view, set()) - old_sets.get(view, set())
                          for view in _KEY_VIEWS))
    for item in sorted(removed):
        emit(3, f"{label}: accepted-key set module: removed {item}")
    for item in sorted(added):
        emit(2, f"{label}: accepted-key set module: added {item}")


def _waivers(snapshot):
    if snapshot.read(_WAIVERS) is None:
        return []
    data = snapshot.toml(_WAIVERS)
    if set(data) != {"schema_version", "waiver"} or type(data["schema_version"]) is not int:
        raise ValueError(f"{_WAIVERS}: expected exactly schema_version and waiver")
    if data["schema_version"] != 1 or not isinstance(data["waiver"], list):
        raise ValueError(f"{_WAIVERS}: expected schema_version = 1 and [[waiver]] rows")
    for index, row in enumerate(data["waiver"]):
        label = f"{_WAIVERS}: waiver[{index}]"
        if not isinstance(row, dict) or set(row) != _WAIVER_FIELDS:
            raise ValueError(f"{label}: expected exactly {', '.join(sorted(_WAIVER_FIELDS))}")
        _version(row["from"], f"{label}.from")
        _version(row["to"], f"{label}.to")
        if type(row["required"]) is not str or row["required"] not in _LEVELS[1:]:
            raise ValueError(f"{label}: required must be PATCH, MINOR or MAJOR")
        for field in ("reason", "decision_ref"):
            if type(row[field]) is not str or not row[field].strip():
                raise ValueError(f"{label}: {field} must be a non-empty string")
        if row["approved_by"] != "maintainer":
            raise ValueError(f"{label}: approved_by must be maintainer")
        if type(row["approved"]) is not datetime.date:
            raise ValueError(f"{label}: approved must be a TOML date")
        if _version(row["to"], f"{label}.to") <= _version(row["from"], f"{label}.from"):
            # An equal or backward row would waive every later unbumped change.
            raise ValueError(f"{label}: to must be greater than from")
    return data["waiver"]


def _evaluate(root, pack_root, base):
    root = Path(root).resolve()
    pack_root = Path(pack_root).resolve()
    top = Path(_git(root, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if root != top or pack_root == root or not pack_root.is_relative_to(root):
        raise ValueError("root must be the git top level and pack-root must be inside it")
    try:
        if base is None:
            revision = _git(root, "merge-base", "HEAD", "origin/main").decode().strip()
        else:
            revision = _git(
                root, "rev-parse", "--verify", "--end-of-options", f"{base}^{{commit}}",
            ).decode().strip()
    except ValueError as exc:
        raise ValueError(f"cannot resolve release base {base or 'merge-base HEAD origin/main'}: {exc}") from exc
    snapshots = [_Snapshot(root, pack_root, revision), _Snapshot(root, pack_root)]
    manifests = [snapshot.toml(_MANIFEST) for snapshot in snapshots]
    for data in manifests:
        _schema(data, _MANIFEST)
    versions = []
    for data in manifests:
        pack = data.get("pack")
        if not isinstance(pack, dict):
            raise ValueError(f"{_MANIFEST}: missing [pack]")
        versions.append(_version(pack.get("version"), "[pack].version"))
    before_version, after_version = versions
    registers = [_registers(s, m) for s, m in zip(snapshots, manifests)]
    profiles = [_profiles(s, r) for s, r in zip(snapshots, registers)]
    for data in manifests:
        declared = data.get("release", {}).get("waivers", _WAIVERS) if isinstance(data.get("release", {}), dict) else None
        if declared != _WAIVERS:
            raise ValueError(f"{_MANIFEST}: [release].waivers must be {_WAIVERS!r}")
    _waivers(snapshots[0])
    waivers = _waivers(snapshots[1])
    changes = []

    def emit(level, message):
        changes.append((level, message))

    if manifests[0]["schema_version"] != manifests[1]["schema_version"]:
        emit(3, f"{_MANIFEST}: schema_version changed")
    for name in sorted(registers[0].keys() | registers[1].keys()):
        old_rel, old = registers[0].get(name, ("", {}))
        new_rel, new = registers[1].get(name, ("", {}))
        label = new_rel or old_rel
        if old and new and old["schema_version"] != new["schema_version"]:
            emit(3, f"{label}: schema_version changed")
        old_ids = _entities(old, name, old_rel)
        new_ids = _entities(new, name, new_rel)
        _set_changes(set(old_ids), set(new_ids), f"{label}: register identity", emit)
        for identity in sorted(old_ids.keys() & new_ids.keys()):
            if name == "profiles":
                _profile_changes(old_ids[identity][0], new_ids[identity][0],
                                 f"{label}: {identity!r}", emit)
            elif not _same(old_ids[identity], new_ids[identity]):
                emit(1, f"{label}: register value changed {identity!r}")
        if name == "profiles":
            old_extra = {k: v for k, v in old.items() if not isinstance(v, (dict, list))}
            new_extra = {k: v for k, v in new.items() if not isinstance(v, (dict, list))}
            old_extra.pop("schema_version", None)
            new_extra.pop("schema_version", None)
            _profile_changes(old_extra, new_extra, label, emit)
    for identity in sorted(profiles[0].keys() & profiles[1].keys()):
        old_rel, old = profiles[0][identity]
        new_rel, new = profiles[1][identity]
        if old["schema_version"] != new["schema_version"]:
            emit(3, f"{new_rel}: schema_version changed")
        _profile_changes(
            {k: v for k, v in old.items() if k != "schema_version"},
            {k: v for k, v in new.items() if k != "schema_version"},
            new_rel, emit,
        )
    scope = _scope(snapshots[0]) | _scope(snapshots[1])
    for rel in sorted(scope):
        old, new = (snapshot.read(rel) for snapshot in snapshots)
        if old == new and snapshots[0].modes.get(rel) == snapshots[1].modes.get(rel):
            continue
        emit(1, f"{rel}: pack surface changed")
        if _clause_path(rel):
            if new is None:
                emit(3, f"{rel}: clause source removed")
            elif old is None:
                emit(2, f"{rel}: clause source added")
            else:
                emit(1, f"{rel}: clause changed; strengthening vs clarifying is not machine-decidable")
        if _engine_path(rel):
            _engine_changes(old, new, rel, emit)
    floor = max((level for level, _ in changes), default=0)
    claimed = next(
        (3 - index for index, (old, new) in enumerate(zip(before_version, after_version))
         if old != new), 0,
    )
    breaking = floor == 3 and before_version[0] == 0
    effective = 2 if breaking else floor
    decreased = after_version < before_version
    if decreased:
        outcome, status = "FAIL (version decreased)", 1
    elif any(
        row["from"] == manifests[0]["pack"]["version"]
        and row["to"] == manifests[1]["pack"]["version"]
        and row["required"] == _LEVELS[floor]
        for row in waivers
    ):
        outcome, status = "WAIVED (maintainer-approved release waiver)", 0
    elif claimed >= effective:
        outcome, status = "PASS", 0
    else:
        outcome, status = "FAIL (claimed bump does not meet required floor)", 1
    lines = [f"{_LEVELS[level]} {message}" for level, message in changes]
    lines.extend([
        f"FLOOR: {_LEVELS[floor]}" + (" (BREAKING; 0.x requires MINOR)" if breaking else ""),
        "CLAIMED: " + ("DECREASE" if decreased else _LEVELS[claimed])
        + f" ({manifests[0]['pack']['version']} -> {manifests[1]['pack']['version']})",
        outcome,
    ])
    return status, lines


def check(root, pack_root, base=None):
    """Print the release-delta report; return 0, 1 or 2 without writing files."""
    try:
        status, lines = _evaluate(root, pack_root, base)
    except (OSError, ValueError, UnicodeError, RecursionError,
            subprocess.SubprocessError) as exc:
        print(f"ERROR: release-delta input: {exc}")
        return 2
    for line in lines:
        print(line)
    return status
