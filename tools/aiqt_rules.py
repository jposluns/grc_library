"""Pinned AIQT rendering and validation. Offline, exact bytes, fail closed.

OVERLAY_DIGESTS pins the SHA-256 of the raw UTF-8 bytes that follow the first
PROJECT-OVERLAY marker in each retained legacy file, read without newline
translation and before any strip or rewrite. To change a retained overlay, edit
the legacy tail, recompute
hashlib.sha256(text.split(MARKER, 1)[1].encode()).hexdigest(), update the
constant in the same commit, run python3 tools/aiqt_rules.py --write, and
re-run gate 37.

validate() resolves its root first, so a relative or symlink-reached root is
accepted. A changed retained tail fails before the generated target is compared,
normally as "retained overlay drift: <path>" (a second or missing marker, or
invalid encoding, fails with its own message). --write and --check do not run
full snapshot validation; tools/lint-claude-rules-sync.py does.

--write replaces a read-only target. The inode is always replaced and
timestamps are not preserved. The umask is not applied to a newly created
target. There is no fsync. Owner, group, ACLs and extended attributes are not
carried. Setuid, setgid and sticky bits are dropped.
The path check and the write are separate steps. A FIFO in place of any input
file blocks the read. A write killed before the rename can leave a temporary
file named .governance-compatibility.md.<random> in .claude/rules/, which then
counts toward the startup size check until it is removed (a complete leftover
fails that check at the present headroom).
"""
import argparse
import hashlib
import json
import re
import tempfile
import tomllib
from pathlib import Path

CLI_DESCRIPTION = "Pinned AIQT rendering and validation. Offline, exact bytes, fail closed."

PIN = "a3ff734ca855e4363f340eca52fbd87272c51854"
SNAPSHOT_DIGEST = "237838f77661a58a38a694cc0d95429c9390864dd8b0efffe8b73c693916c86d"
GLOBS = ["**/*.py", "**/*.sh", "**/*.js", "**/*.ts", "**/*.tsx", "**/*.jsx",
         "**/*.html", "**/*.yml", "**/*.yaml", "**/*.json", "**/*.toml",
         "security/**", "dev-security/**", "ai/**", "architecture/**"]
SCOPED = {"SECI-federated-identity-flow.md", "SECI-ssrf-prevention.md",
          "SECI-symlink-resolution.md"}
MARKER = "<!-- PROJECT-OVERLAY: not part of the distributable pack -->"
SOURCE = ".claude/references/governance-compatibility.md"
TARGET = ".claude/rules/governance-compatibility.md"
MANIFEST = "vendor/aiqt/RULES.json"
OVERLAY_DIGESTS: dict[str, str] = {
    ".claude/references/governance/action-before-explanation-of-inaction.md":
        "7cb3bbce65996a4ce92370fa2aec5d7eb6aecfa090d28144ee7148a7bca0a4aa",
    ".claude/references/governance/ai-assistant-workflow-disciplines.md":
        "28228e2fe18fd10e774a9c2c38ed169bab27b349afa1bc76873cac6f59342c11",
    ".claude/references/governance/artefact-and-branch-discipline.md":
        "3a5f8301bebf5f2ec25971588acdfd0488e51f292e30bb0ab8e1058dffca9168",
    ".claude/references/governance/change-tracking.md":
        "22a467ea46473a353d8ac9ad9f3b24d8b565fd1e7c8c898d59a27cd5eba9b67b",
    ".claude/references/governance/clarify-before-acting.md":
        "ba680bc2e68e2b3c734704348ccac1f4676f1fbb4a8eaf6d5ba6194b8cbf6d31",
    ".claude/references/governance/decision-classification-before-enacting.md":
        "3b355a91e04f73365f8c0f15a972a136d2a8db475af2730f30d203c4c5e90a3c",
    ".claude/references/governance/evidence-grounded-completion.md":
        "5db4ca63758b5f43febd8be919606fb5f63916b09d69d46406a0ce9993c83022",
    ".claude/references/governance/gate-discipline.md":
        "711ec266ff36cdbc77559554cfbf226384eddc542a8213962998533d7694cf53",
    ".claude/references/governance/high-assurance-verification.md":
        "2fc01d5864c5b0525532741b04127c75a26f88f75381f6d2844db8d7da308215",
    ".claude/references/governance/project-integrity.md":
        "744c0349e9f06d7352ba6324343c37be948273deb734a3d5388ec9c02331b695",
    ".claude/references/governance/session-lifecycle.md":
        "b607303fda1ef924f80adf2735e2260386e48b9566e21cb83f818df22170f079",
    ".claude/references/governance/surface-counterproductive-instructions.md":
        "b78c4a56be6ba6d9cf2cb7a19efd0cc8d67a0e8ec0090a40f4865acd83ae985e",
    ".claude/references/governance/trust-recovery-escalation.md":
        "6185a585a0c3efccd16c4b07fc94424f985afb12b7d03e82fc5506a1bd726958",
    ".claude/references/governance/validate-inference-before-action.md":
        "c56c352abcdcb19dc264328f54b187010630c0b5b7a23b32946f905f085cf9ac",
}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def unique(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise ValueError("duplicate key: " + k)
        result[k] = v
    return result

def render(b, scopes):
    if not b.startswith(b"---\n") or b"\npaths:" in b:
        raise ValueError("upstream frontmatter is not eligible for paths insertion")
    header = "paths:\n" + "".join("  - " + json.dumps(g) + "\n" for g in scopes)
    notice = "# Modified by GRC: paths added\n"
    return b"---\n" + (notice + header).encode() + b[4:] if scopes else b

def overlays(root, legacy):
    parts = []
    paths = []
    for path in legacy:
        text = (root / path).read_bytes().decode("utf-8")
        count = text.count(MARKER)
        if path not in OVERLAY_DIGESTS:
            if count:
                raise ValueError("unexpected overlay: " + path)
            continue
        if count > 1:
            raise ValueError("duplicate overlay marker: " + path)
        if not count:
            raise ValueError("missing overlay: " + path)
        raw = text.partition(MARKER)[2]
        paths.append(path)
        if sha(raw.encode()) != OVERLAY_DIGESTS[path]:
            raise ValueError("retained overlay drift: " + path)
        tail = raw.strip()
        tail = tail.replace("## Project overlay (grc_library wiring and lineage; local copy only)",
                            "## " + Path(path).name)
        tail = tail.replace("(../../hooks/", "(../hooks/")
        tail = tail.replace("(../../../tools/", "(../../tools/")
        tail = tail.replace("grc_library_private/.working/worker-brief-template.md",
                            "/opt/grc/private/worker-brief-template.md")
        tail = re.sub(r"- Guardrails authoring instantiation.*?(?=\n- Gate-37)",
                      "- Maintainer D2 (2026-10-02): upstream owns the pinned AIQT bytes; "
                      "GRC owns compatibility and legacy publication procedures. "
                      "Portable AIQT changes require upstream review and an explicit re-pin.",
                      tail, flags=re.S)
        parts.append(tail)
    if len(parts) != 14:
        raise ValueError("expected fourteen retained overlays")
    if len(set(paths)) != len(paths) or set(paths) != set(OVERLAY_DIGESTS):
        raise ValueError("retained overlay inventory mismatch")
    return parts

def compatibility(root, legacy):
    parts = overlays(root, legacy)
    return ((root / SOURCE).read_text() + "\n" + "\n\n".join(parts) + "\n").encode()

def inventory(root):
    data = json.loads((root / MANIFEST).read_text(), object_pairs_hook=unique)
    metadata = dict(schema_version=1, repo="jposluns/guardrails", commit=PIN,
                    license="Apache-2.0", owner="upstream", upstream_tree=".claude/rules",
                    upstream_files=133, upstream_bytes=149344,
                    compatibility_source=SOURCE, compatibility_target=TARGET)
    if (not isinstance(data, dict) or set(data) != set(metadata) | {"files", "rules", "legacy_details"}
            or any(type(data[k]) is not type(v) or data[k] != v for k, v in metadata.items())):
        raise ValueError("invalid manifest metadata")
    pin = tomllib.loads((root / "vendor/aiqt/PIN.toml").read_text())
    if pin["source"]["commit"] != data["commit"]:
        raise ValueError("PIN.toml / RULES.json disagreement")
    files = data["files"]
    # This aggregate anchors the complete upstream inventory, not just self-reported hashes.
    if sha(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()) != SNAPSHOT_DIGEST:
        raise ValueError("snapshot inventory differs from pin")
    return data

def legacy_inventory(root, data):
    legacy = data["legacy_details"]
    actual_legacy = sorted(p.relative_to(root).as_posix()
                          for p in (root / ".claude/references/governance").glob("*.md"))
    expected_legacy = sorted(".claude/references/governance/" + p.name
                            for p in (root / "guardrails/governance").glob("*.md"))
    if legacy != expected_legacy or actual_legacy != legacy or len(legacy) != 15:
        raise ValueError("legacy inventory mismatch")
    return legacy

def validate(root):
    root = Path(root).resolve()
    data = inventory(root)
    files = data["files"]
    expected = {r["path"] for r in files}
    actual = {p.relative_to(root).as_posix()
              for p in (root / "guardrails/aiqt-rules").rglob("*") if p.is_file()}
    if len(files) != 135 or actual != expected:
        raise ValueError("missing/extra snapshot file")
    for r in files:
        p = root / r["path"]
        b = p.read_bytes()
        if p.is_symlink() or len(b) != r["bytes"] or sha(b) != r["sha256"]:
            raise ValueError("snapshot drift: " + r["path"])
    expected_rules = []
    for r in files:
        rel = r["path"].removeprefix("guardrails/aiqt-rules/")
        if not rel.startswith(("aiqt/", "security/")):
            continue
        expected_rules.append(dict(source=r["path"], target=".claude/rules/" + rel,
            upstream=".claude/rules/" + rel, bytes=r["bytes"], sha256=r["sha256"],
            paths=GLOBS if Path(rel).name in SCOPED else []))
    if data["rules"] != expected_rules or len(expected_rules) != 132:
        raise ValueError("invalid rule inventory or scope declarations")
    owned = {TARGET}
    for r in expected_rules:
        p = root / r["target"]
        if p.is_symlink() or p.read_bytes() != render((root / r["source"]).read_bytes(), r["paths"]):
            raise ValueError("local AIQT drift: " + r["target"])
        owned.add(r["target"])
    legacy = legacy_inventory(root, data)
    overlays(root, legacy)
    target = compatibility_target(root)
    if target.read_bytes() != compatibility(root, legacy):
        raise ValueError("generated compatibility drift")
    return owned

def compatibility_target(root):
    target = root / TARGET
    if (target.is_symlink() or target.parent.is_symlink() or target.resolve() != target
            or (target.exists() and (not target.is_file() or target.stat().st_nlink != 1))):
        raise ValueError("refusing non-regular compatibility target")
    return target

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

def main(argv=None):
    parser = argparse.ArgumentParser(description=CLI_DESCRIPTION)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true",
                      help="Write the compatibility target without full snapshot validation.")
    mode.add_argument("--check", action="store_true",
                      help="Check the compatibility target without full snapshot validation.")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    try:
        data = inventory(root)
        legacy = legacy_inventory(root, data)
        target = compatibility_target(root)
        generated = compatibility(root, legacy)
        if args.write:
            atomic_write(target, generated)
        elif target.read_bytes() != generated:
            print("generated compatibility drift")
            return 1
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
        print(str(exc))
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
