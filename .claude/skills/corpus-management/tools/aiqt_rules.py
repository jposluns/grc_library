"""Pinned AIQT rendering and validation. Offline, exact bytes, fail closed.

The project vendors a subset of the AIQT project's release (https://aiqt.ai)
under ``.claude/aiqt/``: the rule set rendered for Claude Code, the generic
corpus core ``tools/aiqt_corpus.py``, the upstream LICENSE and NOTICE, and the
upstream release manifest (``.aiqt/manifest.toml``) with its release root
record (``.aiqt/release/root.txt``).

The pin IDENTITY is the upstream release root digest: the SHA-256 of the exact
bytes of the vendored manifest, which is also the single line of the vendored
root record. ``PIN.toml`` names that digest; the commit it also names is
provenance only, because commit ids do not carry over when the upstream
project moves to a new repository, and nothing verifies against it.

``validate()`` verifies, in order: the pin record's shape; the release root
(the pin, the root record, and the recomputed manifest digest must agree);
every vendored file's byte count and SHA-256 against its manifest row, with no
missing, extra, symlinked, or special entry (a fail-closed, non-following
traversal that propagates listing errors; the vendor root, the rendered
directories, and every path component below the root are also checked without
following links); the pin schema-version and the manifest format-version
against the supported values; the rendered copies under
``.claude/rules/aiqt/`` and ``.claude/rules/security/``, byte-identical to
their vendored sources except for the declared paths-scope insertion; and the
generated AIQT index block in ``.claude/CLAUDE.md``. Any failure raises
``ValueError``. An unreadable input is a failure, never a pass. Every
comparison is of exact bytes, so a checkout with ``git core.autocrlf=true``
fails by design.

``--write`` regenerates the rendered rules and the index block from the
vendored copy after verifying it; ``--check`` reports drift without writing.
``--write`` replaces a read-only target: the inode is always replaced,
timestamps are not preserved, and owner, group, ACLs and extended attributes
are not carried. There is no fsync. A write killed before the rename can leave
a temporary ``.<name>.<random>`` file beside the target.
"""
import argparse
import hashlib
import json
import os
import re
import stat
import tempfile
import tomllib
from pathlib import Path

CLI_DESCRIPTION = "Pinned AIQT rendering and validation. Offline, exact bytes, fail closed."

VENDOR_REL = ".claude/aiqt"
PIN_NAME = "PIN.toml"
MANIFEST_REL = ".aiqt/manifest.toml"
ROOT_RECORD_REL = ".aiqt/release/root.txt"
CLAUDE_MD_REL = ".claude/CLAUDE.md"
INDEX_BEGIN = "<!-- AIQT-RULES-BEGIN -->"
INDEX_END = "<!-- AIQT-RULES-END -->"

# Upstream manifest paths mapped to their vendored location under .claude/aiqt/.
# Everything the upstream manifest lists under .claude/rules/ is vendored at
# rules/<rest>; these fixed files are vendored at their own upstream paths.
UPSTREAM_RULES_PREFIX = ".claude/rules/"
VENDORED_RULES_DIR = "rules"
FIXED_VENDORED = {"tools/aiqt_corpus.py", "LICENSE", "NOTICE"}
RENDER_SUBDIRS = ("aiqt", "security")

# Supported schema declarations (RBQ8-schema-versions): the pin record and the
# vendored upstream manifest must declare exactly these versions.
PIN_SCHEMA_VERSION = 1
MANIFEST_FORMAT_VERSION = 1

GLOBS = ["**/*.py", "**/*.sh", "**/*.js", "**/*.ts", "**/*.tsx", "**/*.jsx",
         "**/*.html", "**/*.yml", "**/*.yaml", "**/*.json", "**/*.toml",
         "security/**", "dev-security/**", "ai/**", "architecture/**"]
SCOPED = {"SECI-federated-identity-flow.md", "SECI-ssrf-prevention.md",
          "SECI-symlink-resolution.md"}

_ROOT_DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}")
_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_COMMIT_RE = re.compile(r"[0-9a-fA-F]{7,40}")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def repo_root_default():
    """The repository root: this file lives at
    .claude/skills/corpus-management/tools/aiqt_rules.py, four levels down."""
    return Path(__file__).resolve().parents[4]


def _read_bytes(path, what):
    """Fail-closed byte read: a symlink, any non-regular input (FIFO, socket,
    device), or an unreadable file is a ValueError. The type is checked with a
    non-following lstat BEFORE the file is opened, the open itself is
    non-following and non-blocking, and the descriptor's type is re-checked,
    so a special file swapped into place can neither redirect the read nor
    block it (RBQ11-metadata-fifo-hang)."""
    path = Path(path)
    try:
        mode = os.lstat(path).st_mode
    except OSError as exc:
        raise ValueError("unreadable {}: {} ({})".format(what, path, exc)) from exc
    if stat.S_ISLNK(mode):
        raise ValueError("refusing symlinked {}: {}".format(what, path))
    if not stat.S_ISREG(mode):
        raise ValueError("refusing non-regular {} (not opened): {}".format(what, path))
    flags = (os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
             | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_BINARY", 0))
    fd = -1
    try:
        fd = os.open(path, flags)
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError("refusing non-regular {}: {}".format(what, path))
        with os.fdopen(fd, "rb") as stream:
            fd = -1
            return stream.read()
    except OSError as exc:
        raise ValueError("unreadable {}: {} ({})".format(what, path, exc)) from exc
    finally:
        if fd >= 0:
            os.close(fd)


def _is_printable_ascii(s):
    return bool(s) and all(0x21 <= ord(ch) <= 0x7E for ch in s)


def _assert_no_symlink_components(root, rel):
    """Refuse a symlinked path component: every component from ``root`` down
    to ``root/rel`` is checked with a non-following lstat, so the vendored or
    rendered tree cannot be redirected through a symlinked parent."""
    current = Path(root)
    for part in Path(rel).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("refusing symlinked path component: {}".format(current))


def _walk_regular_files(base, what):
    """Fail-closed, non-following traversal of ``base``. Returns every entry
    that is a regular file or a symlink (a symlink then surfaces in the
    inventory comparison and is refused on read). A listing error propagates
    as ValueError (an unlistable directory is a failure, never a pass), and an
    entry that is neither a regular file, a directory, nor a symlink (a FIFO,
    socket, or device) is refused outright."""
    found = []
    stack = [Path(base)]
    while stack:
        directory = stack.pop()
        try:
            entries = list(os.scandir(directory))
        except OSError as exc:
            raise ValueError("unlistable {} directory: {} ({})".format(
                what, directory, exc)) from exc
        for entry in entries:
            try:
                mode = entry.stat(follow_symlinks=False).st_mode
            except OSError as exc:
                raise ValueError("unreadable {} entry: {} ({})".format(
                    what, entry.path, exc)) from exc
            if stat.S_ISLNK(mode) or stat.S_ISREG(mode):
                found.append(Path(entry.path))
            elif stat.S_ISDIR(mode):
                stack.append(Path(entry.path))
            else:
                raise ValueError(
                    "refusing special {} entry (neither a regular file nor a "
                    "directory): {}".format(what, entry.path))
    return found


def load_pin(root):
    """Read and schema-validate .claude/aiqt/PIN.toml. Returns the parsed pin.
    A missing, unreadable, unparseable or ill-shaped pin raises ValueError."""
    return _load_pin_file(Path(root) / VENDOR_REL / PIN_NAME)


def _load_pin_file(path):
    """Read and schema-validate one pin record. Returns the parsed pin.
    A missing, unreadable, unparseable or ill-shaped pin raises ValueError."""
    if not path.is_file():
        raise ValueError("pin record not found at {}".format(path))
    raw = _read_bytes(path, "pin record")
    try:
        pin = tomllib.loads(raw.decode("utf-8"))
    except Exception as exc:  # deliberate choke-point: ANY parse failure is a tamper signal
        raise ValueError("pin record is unreadable: {}: {}".format(type(exc).__name__, exc)) from exc
    source = pin.get("source")
    if not isinstance(source, dict):
        raise ValueError("pin record is malformed: [source] must be a table")
    problems = []
    schema = pin.get("schema-version")
    # Exact int TYPE, not value equality: bool(True) and float(1.0) both == 1
    # (RBQ11-float-schema-versions).
    if type(schema) is not int or schema != PIN_SCHEMA_VERSION:
        problems.append("schema-version must be the integer {} (found {!r})"
                        .format(PIN_SCHEMA_VERSION, schema))
    for key in ("project", "url", "release-version"):
        val = source.get(key)
        if not isinstance(val, str) or not val.strip():
            problems.append("[source] {} must be a non-empty string".format(key))
    release_root = source.get("release-root")
    if not isinstance(release_root, str) or not _ROOT_DIGEST_RE.fullmatch(release_root):
        problems.append("[source] release-root must be 'sha256:' followed by 64 lowercase hex characters")
    commit = source.get("commit")
    if not isinstance(commit, str) or not _COMMIT_RE.fullmatch(commit):
        problems.append("[source] commit must be a string of 7 to 40 hexadecimal characters")
    if problems:
        raise ValueError("pin record is malformed: " + "; ".join(problems))
    return pin


def _manifest_rows(manifest):
    """The validated path -> (bytes, sha256) inventory from a parsed manifest."""
    fmt = manifest.get("format-version")
    # Exact int TYPE, not value equality: bool(True) and float(1.0) both == 1
    # (RBQ11-float-schema-versions).
    if type(fmt) is not int or fmt != MANIFEST_FORMAT_VERSION:
        raise ValueError("vendored manifest format-version must be the integer {} "
                         "(found {!r})".format(MANIFEST_FORMAT_VERSION, fmt))
    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("vendored manifest has no [[sources]] rows")
    rows = {}
    for entry in sources:
        if not isinstance(entry, dict):
            raise ValueError("vendored manifest row is not a table")
        path, nbytes, digest = entry.get("path"), entry.get("bytes"), entry.get("sha256")
        if (not isinstance(path, str) or not _is_printable_ascii(path)
                or isinstance(nbytes, bool) or not isinstance(nbytes, int) or nbytes < 0
                or not isinstance(digest, str) or not _SHA256_RE.fullmatch(digest)):
            raise ValueError("vendored manifest row for {!r} is malformed".format(path))
        if path in rows:
            raise ValueError("vendored manifest lists {} twice".format(path))
        rows[path] = (nbytes, digest)
    return rows


def vendored_inventory(manifest):
    """Map each vendored file's path under .claude/aiqt/ to its manifest row.
    The vendored set is derived from the manifest, never hand-listed: every
    manifest row under .claude/rules/ plus the fixed corpus-core and licence
    files. A fixed file absent from the manifest is a ValueError."""
    rows = _manifest_rows(manifest)
    inventory = {}
    for path, row in rows.items():
        if path.startswith(UPSTREAM_RULES_PREFIX):
            local = VENDORED_RULES_DIR + "/" + path[len(UPSTREAM_RULES_PREFIX):]
            inventory[local] = row
    for path in sorted(FIXED_VENDORED):
        if path not in rows:
            raise ValueError("vendored manifest carries no row for {}".format(path))
        inventory[path] = rows[path]
    return inventory


def verify_vendored(root):
    """Verify the whole vendored copy under <root>/.claude/aiqt against the
    release root and manifest. Returns (pin, inventory). The vendor root and
    every path component below ``root`` are checked without following links;
    any mismatch, missing, extra, symlinked or special file, unlistable
    directory, or unreadable input raises ValueError (fail closed)."""
    root = Path(root)
    _assert_no_symlink_components(root, VENDOR_REL)
    return verify_vendor_dir(root / VENDOR_REL)


def verify_vendor_dir(vendor):
    """Verify one vendored copy, laid out like .claude/aiqt/, against its own
    pin record, manifest, and root record. Returns (pin, inventory). The
    vendor root is checked without following links; any mismatch, missing,
    extra, symlinked or special file, unlistable directory, or unreadable
    input raises ValueError (fail closed). The aiqt_bootstrap shim calls this
    to verify a selected copy BEFORE exposing or importing any of its code."""
    vendor = Path(vendor)
    if vendor.is_symlink():
        raise ValueError("refusing symlinked vendor root: {}".format(vendor))
    if not vendor.is_dir():
        raise ValueError("vendor root is not a directory: {}".format(vendor))
    pin = _load_pin_file(vendor / PIN_NAME)
    raw = _read_bytes(vendor / MANIFEST_REL, "vendored manifest")
    digest = sha(raw)
    pinned = pin["source"]["release-root"].removeprefix("sha256:")
    if digest != pinned:
        raise ValueError("release root mismatch: vendored manifest digest {} does not match "
                         "the pinned release root {}".format(digest, pinned))
    record = _read_bytes(vendor / ROOT_RECORD_REL, "vendored root record")
    # Exact bytes (RBQ11-root-record-whitespace): the record must equal
    # b"sha256:" + digest + b"\n"; any whitespace variation is drift.
    if record != ("sha256:" + digest + "\n").encode("ascii"):
        raise ValueError("vendored root record {!r} disagrees with the manifest digest: the "
                         "record must be exactly b'sha256:{}\\n'"
                         .format(record[:100], digest))
    try:
        manifest = tomllib.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise ValueError("vendored manifest is unreadable: {}: {}"
                         .format(type(exc).__name__, exc)) from exc
    inventory = vendored_inventory(manifest)
    expected = set(inventory) | {PIN_NAME, MANIFEST_REL, ROOT_RECORD_REL}
    actual = {p.relative_to(vendor).as_posix()
              for p in _walk_regular_files(vendor, "vendored")}
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise ValueError("vendored copy does not match the pin: missing {}; extra {}"
                         .format(missing or "none", extra or "none"))
    for rel in sorted(inventory):
        nbytes, filedigest = inventory[rel]
        data = _read_bytes(vendor / rel, "vendored file")
        if len(data) != nbytes or sha(data) != filedigest:
            raise ValueError("vendored drift: {}/{} does not match its manifest row"
                             .format(VENDOR_REL, rel))
    return pin, inventory


def inventory(root):
    """Compatibility surface for consumers that enumerate the pinned files:
    the VERIFIED vendored inventory as {"files": [{"path", "bytes", "sha256"},
    ...]} with paths relative to the repository root, sorted by path."""
    _, inv = verify_vendored(Path(root))
    return {"files": [{"path": VENDOR_REL + "/" + rel, "bytes": nb, "sha256": hx}
                      for rel, (nb, hx) in sorted(inv.items())]}


def render(b, scopes):
    """The rendered bytes for a vendored rule: the source bytes, with the
    declared paths scopes inserted into the frontmatter for a scoped rule."""
    if not scopes:
        return b
    if not b.startswith(b"---\n") or b"\npaths:" in b:
        raise ValueError("upstream frontmatter is not eligible for paths insertion")
    header = "paths:\n" + "".join("  - " + json.dumps(g) + "\n" for g in scopes)
    notice = "# Modified by GRC: paths added\n"
    return b"---\n" + (notice + header).encode() + b[4:]


def expected_rules(inventory):
    """The rendered-rule plan: (vendored source rel, rendered target rel, scopes)."""
    plan = []
    for rel in sorted(inventory):
        parts = rel.split("/")
        if len(parts) == 3 and parts[0] == VENDORED_RULES_DIR and parts[1] in RENDER_SUBDIRS:
            scopes = GLOBS if parts[2] in SCOPED else []
            plan.append((VENDOR_REL + "/" + rel, ".claude/rules/" + parts[1] + "/" + parts[2], scopes))
    if not plan:
        raise ValueError("the vendored manifest yields no rules to render")
    return plan


def index_block(plan):
    """The generated AIQT index block body carried by .claude/CLAUDE.md: one
    line per rendered subdirectory listing every rule, in sorted order."""
    lines = []
    for sub in RENDER_SUBDIRS:
        names = sorted(t.split("/")[-1] for _, t, _ in plan
                       if t.startswith(".claude/rules/" + sub + "/"))
        lines.append("- {}: {}".format(sub, "; ".join("[`{}/{}`]".format(sub, n) for n in names)))
    return "\n".join(lines) + "\n"


def _split_claude_md(root):
    """The CLAUDE.md text split at the index markers: (head, current, tail).
    Missing or duplicated markers raise ValueError."""
    path = root / CLAUDE_MD_REL
    text = _read_bytes(path, "CLAUDE.md").decode("utf-8")
    if text.count(INDEX_BEGIN) != 1 or text.count(INDEX_END) != 1:
        raise ValueError("{} must carry exactly one AIQT index block".format(CLAUDE_MD_REL))
    head, rest = text.split(INDEX_BEGIN + "\n", 1)
    current, tail = rest.split(INDEX_END, 1)
    return head, current, tail


def validate(root):
    """Full snapshot validation; returns the set of rendered rule paths the
    pin owns. Raises ValueError on any drift (fail closed)."""
    root = Path(root).resolve()
    pin, inventory = verify_vendored(root)
    plan = expected_rules(inventory)
    owned = set()
    for source_rel, target_rel, scopes in plan:
        target = root / target_rel
        generated = render(_read_bytes(root / source_rel, "vendored rule"), scopes)
        if target.is_symlink() or not target.is_file() or target.read_bytes() != generated:
            raise ValueError("rendered AIQT drift: " + target_rel)
        owned.add(target_rel)
    for sub in RENDER_SUBDIRS:
        _assert_no_symlink_components(root, ".claude/rules/" + sub)
        rendered_dir = root / ".claude/rules" / sub
        actual = {p.relative_to(root).as_posix()
                  for p in _walk_regular_files(rendered_dir, "rendered")}
        if actual != {t for _, t, _ in plan if t.startswith(".claude/rules/" + sub + "/")}:
            raise ValueError("unexpected file set under .claude/rules/" + sub)
    _, current, _ = _split_claude_md(root)
    if current != index_block(plan):
        raise ValueError("stale AIQT index block in " + CLAUDE_MD_REL)
    return owned


def atomic_write(target, content):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix="." + target.name + ".",
                                         delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        temporary.chmod(target.stat().st_mode & 0o777 if target.exists() else 0o644)
        temporary.replace(target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_rendered(root):
    """Regenerate every rendered rule and the CLAUDE.md index block from the
    verified vendored copy. Removes nothing: a stray rendered file is reported
    by validate() and by the sync gate, never silently deleted here."""
    root = Path(root).resolve()
    _, inventory = verify_vendored(root)
    plan = expected_rules(inventory)
    for source_rel, target_rel, scopes in plan:
        target = root / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(target, render(_read_bytes(root / source_rel, "vendored rule"), scopes))
    head, _, tail = _split_claude_md(root)
    text = head + INDEX_BEGIN + "\n" + index_block(plan) + INDEX_END + tail
    atomic_write(root / CLAUDE_MD_REL, text.encode("utf-8"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=CLI_DESCRIPTION)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true",
                      help="Regenerate the rendered rules and the CLAUDE.md index block.")
    mode.add_argument("--check", action="store_true",
                      help="Validate the vendored copy, the rendered rules, and the index block.")
    args = parser.parse_args(argv)
    root = repo_root_default()
    try:
        if args.write:
            write_rendered(root)
        else:
            validate(root)
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
        print(str(exc))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
