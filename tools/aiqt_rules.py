"""Pinned AIQT rendering and validation. Offline, exact bytes, fail closed."""
import hashlib
import json
import re
import tomllib
from pathlib import Path

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
    return b"---\n" + header.encode() + b[4:] if scopes else b

def compatibility(root, legacy):
    parts = []
    for path in legacy:
        text = (root / path).read_text()
        if MARKER not in text:
            continue
        if text.count(MARKER) != 1:
            raise ValueError("duplicate overlay marker: " + path)
        tail = text.split(MARKER, 1)[1].strip()
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

def validate(root):
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
    legacy = data["legacy_details"]
    actual_legacy = sorted(p.relative_to(root).as_posix()
                          for p in (root / ".claude/references/governance").glob("*.md"))
    expected_legacy = sorted(".claude/references/governance/" + p.name
                            for p in (root / "guardrails/governance").glob("*.md"))
    if legacy != expected_legacy or actual_legacy != legacy or len(legacy) != 15:
        raise ValueError("legacy inventory mismatch")
    if (root / TARGET).read_bytes() != compatibility(root, legacy):
        raise ValueError("generated compatibility drift")
    return owned
