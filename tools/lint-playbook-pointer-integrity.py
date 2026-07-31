#!/usr/bin/env python3
"""Playbook-pointer-integrity audit (gate 80).

The activity-scoped rule loader (roadmap C part 2) relocates per-activity
prose out of the always-loaded core (``.claude/CLAUDE.md``) into
``references/<playbook>.md`` files read at their activity boundary "like a
skill", leaving a lean inline core plus a pointer. Convention alone does not
stop a catastrophic mistake: a section titled for one activity can carry a
BURIED always-on clause (a directive that must stay in force OUTSIDE that
activity), and moving the section moves the clause out of the core with it.

This gate is that invariant's enforcer. It reads ``references/PLAYBOOK-MANIFEST.yml``
(one entry per relocated section: its ``references/<playbook>.md`` target, the
triggering activity boundary, the RETAINED always-on clause anchors kept inline,
and the RELOCATED anchors) and asserts, against ``.claude/CLAUDE.md``:

  (a) Bidirectional pointer parity. Every manifest playbook has a live inline
      ``references/<file>.md`` pointer in the core (no ORPHAN playbook), and
      every inline ``references/*.md`` pointer resolves to an existing file
      (no DANGLING pointer).
  (b) Activity-playbooks INDEX completeness. Once the ``## Activity playbooks``
      INDEX section exists in the core, every manifest playbook is listed in it
      exactly once. DEGRADATION: while that section is ABSENT (Stage 1, current
      tree), the check emits an informational NOTE and is skipped, so the gate
      passes with only the seed manifest. The INDEX check EXPECTS each playbook
      listed by a link whose target contains ``references/<file>.md``, counted
      by that path, exactly once, between the ``## Activity playbooks`` heading
      and the next ``## `` heading.
  (c) Retained-clause presence (THE INVARIANT ENFORCER). Every manifest RETAINED
      clause anchor still appears, as a substring, inline in ``.claude/CLAUDE.md``.
      A missing anchor is the exact signature of an always-on clause moved out
      with its section -> RED gate.
  (d) Duplication carve-out. Inline+playbook duplication of a retained clause is
      deliberate defence-in-depth and is NEVER a finding: this gate implements no
      dedupe check, and a retained anchor that ALSO appears in the playbook file
      is expected, not flagged.
  (e) OPTIONAL relocated-anchor presence (pointer-rot guard). Each RELOCATED
      anchor appears in its playbook FILE, so the pointer target demonstrably
      still contains the moved material. Isolated in ``_check_relocated`` and easy
      to drop if it proves brittle; it is additive to (a)-(d), never a substitute.

Exit codes:
  0  clean.
  1  one or more integrity findings.
  2  environment error (a required input is missing or the manifest is unparseable).

FP-safety is paramount (a gate that cries wolf gets bypassed):
  * It reads named files by explicit path, never the exempt-dir walker.
  * A ``references/`` file that exists but is NOT in the manifest is NOT flagged
    (a non-playbook reference doc is legitimate; only manifest<->pointer and
    manifest<->clause relationships are enforced).
  * The bare directory token ``references/`` (as in prose like "(NOT `.claude/`
    or `references/`)") is not a pointer: the pointer pattern requires a
    ``<name>.md`` tail.
  * Anchor matching is plain substring containment over the WHOLE core text
    (fence state irrelevant: a retained directive is present or it is not),
    which has no regex-escaping or windowing failure mode.

``--root`` overrides the repository root the two inputs are read from (the
regression fixtures point it at a synthetic tree). ``--self-test`` builds
synthetic positive/negative trees in a tempdir and verifies detection, then
exits 0 only if every self-test assertion holds.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import REPO_ROOT  # noqa: E402

CLAUDE_REL = ".claude/CLAUDE.md"
MANIFEST_REL = "references/PLAYBOOK-MANIFEST.yml"
INDEX_HEADING = "## Activity playbooks"

# An inline pointer to a playbook: `references/<name>.md`. Requires the `.md`
# tail so the bare directory token `references/` is never a pointer.
POINTER_RE = re.compile(r"references/([A-Za-z0-9._-]+\.md)")


class ManifestError(Exception):
    """A required input is missing or the manifest cannot be parsed (exit 2)."""


# --- Manifest parsing (quoted-value, indentation-based; the taxonomy.yml idiom) ---

def _yaml_value(line: str, key: str) -> str:
    m = re.search(rf'{re.escape(key)}:\s*"((?:[^"\\]|\\.)*)"', line)
    if not m:
        return ""
    return m.group(1).replace('\\"', '"').replace("\\\\", "\\")


def _yaml_list_value(line: str) -> str:
    m = re.search(r'-\s+"((?:[^"\\]|\\.)*)"', line)
    if not m:
        return ""
    return m.group(1).replace('\\"', '"').replace("\\\\", "\\")


def parse_manifest(text: str) -> list[dict]:
    """Parse the manifest into a list of entry dicts.

    Block boundary: a column-0 ``- playbook:`` line. 2-space scalars become
    string values; the two list sections (``retained_anchors``,
    ``relocated_anchors``) collect their 4-space ``- "value"`` items.
    """
    entries: list[dict] = []
    cur: dict | None = None
    listkey: str | None = None
    for raw in text.splitlines():
        if raw.startswith("- playbook:"):
            if cur is not None:
                entries.append(cur)
            cur = {"retained_anchors": [], "relocated_anchors": []}
            listkey = None
            cur["playbook"] = _yaml_value(raw, "playbook")
        elif cur is not None and raw.startswith("  "):
            stripped = raw.strip()
            if stripped in ("retained_anchors:", "relocated_anchors:"):
                listkey = stripped[:-1]  # drop trailing ':'
            elif raw.startswith("    - ") and listkey:
                val = _yaml_list_value(raw)
                if not val:
                    # gF2 (fail-loud, not fail-open): a malformed/unquoted list
                    # item would silently parse to "" and be skipped by the
                    # checks, leaving the declared always-on clause UNENFORCED
                    # while the gate stayed green. For a sensitive-tier invariant
                    # enforcer that silent-drop is the dangerous direction, so a
                    # non-parseable anchor is a loud environment error, never a
                    # skip. (An entry with NO list items is still allowed: a
                    # relocated section may legitimately carry no always-on
                    # residue.)
                    raise ManifestError(
                        f"malformed {listkey} item in {MANIFEST_REL} (must be a "
                        f'non-empty quoted "value"): {raw.strip()!r}'
                    )
                cur[listkey].append(val)
            elif ": " in stripped and not stripped.startswith("-"):
                key, _, _v = stripped.partition(":")
                cur[key.strip()] = _yaml_value(raw, key.strip())
                listkey = None
    if cur is not None:
        entries.append(cur)
    return entries


# --- The four checks (plus optional (e)) ---

def _check_pointers(entries: list[dict], claude_text: str, root: Path) -> list[str]:
    """(a) bidirectional pointer parity."""
    findings: list[str] = []
    inline = {m.group(1) for m in POINTER_RE.finditer(claude_text)}
    # forward: every manifest playbook has an inline pointer.
    for e in entries:
        base = e["playbook"].split("/")[-1]
        if base not in inline:
            findings.append(
                f"[pointer] ORPHAN playbook: manifest lists {e['playbook']!r} but "
                f"{CLAUDE_REL} has no inline `references/{base}` pointer to it"
            )
    # reverse: every MANIFEST playbook target file exists. gF1: we deliberately
    # do NOT require every incidental `references/<x>.md` MENTION in the core to
    # resolve. A prose mention, a fenced example, an external URL, or a
    # forward-reference to a not-yet-created Stage-2 playbook is legitimate and
    # must not cry wolf (a gate that cries wolf gets bypassed). The gate's scope
    # is MANIFEST/playbook integrity, not link-checking the core: gate 3 does not
    # scan the exempt .claude/ tree, so a stray broken references/ link there is
    # out of scope here by design. A manifest entry pointing at a deleted or
    # renamed file is the dangling case that matters, and it is caught here.
    for e in entries:
        if not (root / e["playbook"]).is_file():
            findings.append(
                f"[pointer] DANGLING playbook target: manifest lists "
                f"{e['playbook']!r} but that file does not exist"
            )
    return findings


def _index_section(claude_text: str) -> str | None:
    """Return the text of the `## Activity playbooks` INDEX section, or None if absent."""
    lines = claude_text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith(INDEX_HEADING):
            start = i + 1
            break
    if start is None:
        return None
    body: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def _check_index(entries: list[dict], claude_text: str) -> tuple[list[str], list[str]]:
    """(b) INDEX completeness, degrading to a NOTE while the section is absent.

    Returns (findings, notes).
    """
    section = _index_section(claude_text)
    if section is None:
        return [], [
            f"[index] NOTE: `{INDEX_HEADING}` INDEX section not present in "
            f"{CLAUDE_REL}; INDEX completeness check skipped (Stage-1 degradation)."
        ]
    findings: list[str] = []
    for e in entries:
        n = section.count(e["playbook"])
        if n == 0:
            findings.append(
                f"[index] MISSING: playbook {e['playbook']!r} is not listed in the "
                f"`{INDEX_HEADING}` INDEX"
            )
        elif n > 1:
            findings.append(
                f"[index] DUPLICATE: playbook {e['playbook']!r} is listed {n} times "
                f"in the `{INDEX_HEADING}` INDEX (must be exactly once)"
            )
    return findings, []


def _check_retained(entries: list[dict], claude_text: str) -> list[str]:
    """(c) retained-clause presence -- the invariant enforcer."""
    findings: list[str] = []
    for e in entries:
        for anchor in e["retained_anchors"]:
            if anchor and anchor not in claude_text:
                findings.append(
                    f"[retained] MOVED-OUT always-on clause: the retained anchor "
                    f"{anchor!r} for playbook {e['playbook']!r} no longer appears "
                    f"inline in {CLAUDE_REL}. An always-on directive was relocated "
                    f"with its section. Restore the clause to the inline core."
                )
    return findings


def _check_relocated(entries: list[dict], root: Path) -> list[str]:
    """(e) OPTIONAL pointer-rot guard: each relocated anchor is in its playbook file."""
    findings: list[str] = []
    for e in entries:
        if not e["relocated_anchors"]:
            continue
        pb = root / e["playbook"]
        if not pb.is_file():
            # A dangling target is already reported by (a); do not double-report.
            continue
        pb_text = pb.read_text(encoding="utf-8")
        for anchor in e["relocated_anchors"]:
            if anchor and anchor not in pb_text:
                findings.append(
                    f"[relocated] POINTER ROT: relocated anchor {anchor!r} is not "
                    f"present in its playbook {e['playbook']!r} (the moved material "
                    f"is missing from the pointer target)"
                )
    return findings


def run_checks(root: Path) -> tuple[list[str], list[str]]:
    """Run all checks against ``root``. Returns (findings, notes).

    Raises ManifestError (exit 2) when a required input is missing/unparseable.
    """
    claude_path = root / CLAUDE_REL
    manifest_path = root / MANIFEST_REL
    if not claude_path.is_file():
        raise ManifestError(f"required file not found: {CLAUDE_REL}")
    if not manifest_path.is_file():
        raise ManifestError(f"required file not found: {MANIFEST_REL}")
    claude_text = claude_path.read_text(encoding="utf-8")
    entries = parse_manifest(manifest_path.read_text(encoding="utf-8"))
    if not entries:
        raise ManifestError(f"no playbook entries parsed from {MANIFEST_REL}")
    for e in entries:
        if not e.get("playbook"):
            raise ManifestError(
                f"a manifest entry has no `playbook:` value in {MANIFEST_REL}"
            )

    findings: list[str] = []
    notes: list[str] = []
    findings += _check_pointers(entries, claude_text, root)
    idx_f, idx_n = _check_index(entries, claude_text)
    findings += idx_f
    notes += idx_n
    findings += _check_retained(entries, claude_text)
    findings += _check_relocated(entries, root)
    return findings, notes


# --- Self-test (synthetic trees; provable standalone) ---

def _write_tree(root: Path, claude: str, manifest: str, playbook: str = "detail\n") -> None:
    (root / ".claude").mkdir(parents=True, exist_ok=True)
    (root / "references").mkdir(parents=True, exist_ok=True)
    (root / CLAUDE_REL).write_text(claude, encoding="utf-8")
    (root / MANIFEST_REL).write_text(manifest, encoding="utf-8")
    (root / "references" / "pr-lifecycle.md").write_text(playbook, encoding="utf-8")


_MANIFEST = (
    '- playbook: "references/pr-lifecycle.md"\n'
    '  activity: "PR close-out"\n'
    '  retained_anchors:\n'
    '    - "Feature branch only, never"\n'
    '  relocated_anchors:\n'
    '    - "DISPATCHED ORDER"\n'
)
_CLEAN_CLAUDE = (
    "# CLAUDE.md\n\n## PR workflow\n"
    "See [`references/pr-lifecycle.md`](../references/pr-lifecycle.md).\n"
    "Feature branch only, never `main`.\n"
)
_PLAYBOOK = "# pr-lifecycle\n\nA DISPATCHED ORDER IS WORK ORDERED.\n"


def self_test() -> int:
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        # NEGATIVE: clean tree passes.
        _write_tree(root, _CLEAN_CLAUDE, _MANIFEST, _PLAYBOOK)
        f, _ = run_checks(root)
        if f:
            failures += 1
            print(f"SELF-TEST FAIL (clean should pass): {f}")
        # POSITIVE: retained anchor removed from the core -> a finding.
        _write_tree(
            root,
            _CLEAN_CLAUDE.replace("Feature branch only, never `main`.\n", ""),
            _MANIFEST,
            _PLAYBOOK,
        )
        f, _ = run_checks(root)
        if not any("[retained]" in x for x in f):
            failures += 1
            print(f"SELF-TEST FAIL (removed retained anchor should flag): {f}")
        # POSITIVE: dangling pointer (manifest target file absent) -> a finding.
        (root / "references" / "pr-lifecycle.md").unlink()
        f, _ = run_checks(root)
        if not any("DANGLING" in x or "ORPHAN" in x for x in f):
            failures += 1
            print(f"SELF-TEST FAIL (missing playbook file should flag): {f}")
    if failures:
        print(f"SELF-TEST: {failures} failure(s).")
        return 1
    print("SELF-TEST: all assertions held.")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(REPO_ROOT),
                    help="repository root the two inputs are read from")
    ap.add_argument("--self-test", action="store_true",
                    help="run synthetic positive/negative self-tests and exit")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return self_test()

    try:
        findings, notes = run_checks(Path(args.root))
    except ManifestError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for note in notes:
        print(note)
    if findings:
        print("FAIL: playbook-pointer-integrity finding(s):")
        for f in findings:
            print(f"  - {f}")
        print(
            "\nThe activity-scoped rule loader requires: every manifest playbook is "
            "pointed to and resolves; each RETAINED always-on clause is still inline; "
            "and (once it exists) the `## Activity playbooks` INDEX lists each playbook "
            "once. Restore the missing clause/pointer or fix the manifest."
        )
        return 1
    print(
        "OK: playbook-pointer integrity confirmed "
        "(pointers parity, retained clauses inline, relocated anchors present)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
