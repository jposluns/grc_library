"""Working-tree release floor for the Corpus-Management pack (stdlib only)."""
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
    # references let pack-root or noncanonical references escape (3b81 QA r2 and r3, codex), and a
    # README can be a generation source (QA r4, claude), so neither decides the scope.
    return {rel for rel in snapshot.files if "__pycache__" not in PurePosixPath(rel).parts}


def _engine_path(rel):
    # Every Python file in the pack is engine code, wherever it sits (3b81 QA r1).
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


def _accepted_sets(tree, label):
    # One union per module, so renaming a key-set variable is not a removal; private (underscore)
    # scopes are skipped, so a local helper's `keys` is not an accepted-key declaration.
    keys = set()

    def visit(node, scope):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                return
            scope = (*scope, node.name)
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    name = target.id.lower()
                    if name == "keys" or name.endswith("_keys"):
                        identity = ".".join((*scope, target.id))
                        if node.value is None:
                            raise ValueError(f"{label}: accepted-key declaration {identity} has no value")
                        keys.update(_literal_set(node.value, f"{label}: {identity}"))
        for child in ast.iter_child_nodes(node):
            visit(child, scope)

    visit(tree, ())
    return {"module": keys} if keys else {}


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


def _api(raw, label):
    if raw is None:
        return {}, {}, {}
    try:
        tree = ast.parse(raw, filename=label)
    except (SyntaxError, ValueError) as exc:
        raise ValueError(f"{label}: invalid Python: {exc}") from exc
    symbols = {}
    config = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                if node.name in symbols:
                    raise ValueError(f"{label}: ambiguous public definition {node.name}")
                is_class = isinstance(node, ast.ClassDef)
                parameters = _class_parameters(node) if is_class else _parameters(node)
                symbols[node.name] = ("class" if is_class else "function", parameters)
                if node.name == "configure" and not is_class:
                    config["configure"] = _configure_fields(node, label)
    return symbols, config, _accepted_sets(tree, label)


def _set_changes(left, right, label, emit):
    for item in sorted(left - right):
        emit(3, f"{label}: removed {item}")
    for item in sorted(right - left):
        emit(2, f"{label}: added {item}")


def _engine_changes(left, right, label, emit):
    old, old_config, old_sets = _api(left, label)
    new, new_config, new_sets = _api(right, label)
    _set_changes(set(old), set(new), f"{label}: public symbol", emit)
    for name in sorted(old.keys() & new.keys()):
        if old[name][0] != new[name][0]:
            emit(3, f"{label}: public symbol kind changed {name}")
        _set_changes(old[name][1], new[name][1], f"{label}: {name} parameter", emit)
    for before, after, kind in (
        (old_config, new_config, "configure input"),
        (old_sets, new_sets, "accepted-key set"),
    ):
        for name in sorted(before.keys() | after.keys()):
            _set_changes(before.get(name, set()), after.get(name, set()),
                         f"{label}: {kind} {name}", emit)


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
            # An equal or backward row would waive every later unbumped change (3b81 QA r1).
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
    except (OSError, ValueError, UnicodeError, subprocess.SubprocessError) as exc:
        print(f"ERROR: release-delta input: {exc}")
        return 2
    for line in lines:
        print(line)
    return status
