#!/usr/bin/env python3
"""handoff-snapshot.py: emit the mechanical facts a session handoff needs.

Read-only aggregator (roadmap track B "close-out efficiency tooling"; shipped in PR #1240).
The wind-down pastes a VERIFIED block from this tool instead of hand-deriving each
number, which is the recurring source of stale handoff figures. This tool is
read-only in its reporting path; only `--self-test` writes, and then only to a
temporary directory.

Sources of truth (each the canonical one, so the emitted number cannot drift from it):
  - Library Version / README Version : the README.md metadata block.
  - Gate count                       : `run_gate ` lines in tools/run_all_audits.sh
                                       (the canonical runtime inventory per CLAUDE.md).
  - Pack rules                       : guardrails/governance/*.md
  - Pack skills                      : guardrails/skills/*/SKILL.md
  - Commands                         : .claude/commands/*.md
  - HEAD                             : git rev-parse --short HEAD (green-at requires
                                       the pre-push guard to confirm; this tool only
                                       reports the sha, it does not run the guard).
  - Session metrics (optional)       : the operational store's
                                       degradation-watch-log.md, if present (adopter
                                       clones have none; the section is then omitted).

Usage:
  python3 tools/handoff-snapshot.py            # print the snapshot block
  python3 tools/handoff-snapshot.py --self-test # parser self-test against a fixture

Exit codes: 0 on success (and on a passing self-test); 1 only on a self-test failure.
The reporting path always exits 0, so this tool is advisory and never blocks a run.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import resolve_working, resolve_working_for_write  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]  # tools/ -> repo root


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def library_version(root: Path) -> str | None:
    m = re.search(r"^\*\*Library Version:\*\*\s*([0-9][0-9.]*)", _read(root / "README.md"), re.M)
    return m.group(1) if m else None


def readme_version(root: Path) -> str | None:
    m = re.search(r"^\*\*README Version:\*\*\s*([0-9][0-9.]*)", _read(root / "README.md"), re.M)
    return m.group(1) if m else None


def gate_count(root: Path) -> int:
    return len(re.findall(r"^run_gate ", _read(root / "tools" / "run_all_audits.sh"), re.M))


def rule_count(root: Path) -> int:
    d = root / "guardrails" / "governance"
    return len(list(d.glob("*.md"))) if d.is_dir() else 0


def skill_count(root: Path) -> int:
    d = root / "guardrails" / "skills"
    return len(list(d.glob("*/SKILL.md"))) if d.is_dir() else 0


def command_count(root: Path) -> int:
    d = root / ".claude" / "commands"
    return len(list(d.glob("*.md"))) if d.is_dir() else 0


def head_sha(root: Path) -> str | None:
    try:
        r = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        return r.stdout.strip() or None
    except (subprocess.CalledProcessError, OSError):
        return None


_TS = re.compile(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z)")


def _parse_ts(ts):
    """Parse a degradation-log ISO stamp (minute-only OR full-seconds) to an aware datetime;
    None if unparseable. Used for NEWEST-selection so a same-minute mix does not lexicographically
    mis-sort (`15:30Z` must not out-sort `15:30:45Z`)."""
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ"):
        try:
            return datetime.strptime(ts, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


# --- session-start matcher (KEEP IN LOCKSTEP with .claude/hooks/surface-session-facts.py) ---
# A row is a session-start entry when the TYPE TOKEN `session-start` heads the row (after
# optional bullet/heading/table markers and an optional leading ISO), NOT when the substring
# appears inside another row's prose note (a compaction/considered DECOY). Two cases:
# ISO-before-token (table iso-first, bullet iso-first, bold-iso) and token-first (bare, bullet,
# ###, table token-first, reversed inline). `(?![\w-])` rejects `session-start-<suffix>`.
# Reality-validated against the live degradation log: 87/87 real rows, 0 decoys.
_SS_RE_B = re.compile(r"^[\s\-#>|]*(?:\*\*)?" + _TS.pattern + r"(?:\*\*)?\s*\|?\s*session-start(?![\w-])")
_SS_RE_A = re.compile(r"^[\s\-#>|]*session-start(?![\w-])[:\s|]")
# NOTE: this matcher is deliberately LINE-ANCHORED (session-start must HEAD its row after optional
# markers). That anchoring IS the decoy-exclusion mechanism: a session-start mentioned inside another
# row's note (a compaction/considered decoy, INCLUDING a quoted `| session-start <iso>`) sits on a line
# that starts with the OTHER row's structure, so it never matches. ASSUMPTION: one record per physical
# line. A record concatenated onto another row's line (a write that dropped the trailing newline) is a
# DATA defect to correct in the log, NOT to parse here: matching it mid-line reintroduces the
# prose-decoy ambiguity (codex #1759 iter-2 proved a mid-line Case-C leaks quoted-pipe decoys).


def _session_start_stamps(text: str) -> list:
    """Every session-start row's ISO stamp, TYPE-token-keyed (excludes prose/decoy mentions)."""
    out = []
    for ln in text.splitlines():
        m = _SS_RE_B.match(ln)
        if m:
            out.append(m.group(1))
            continue
        if _SS_RE_A.match(ln):
            m2 = _TS.search(ln)
            if m2:
                out.append(m2.group(1))
    return out


def session_metrics(root: Path, now: datetime | None = None):
    """Best-effort: latest session-start timestamp + elapsed, from the operational store's log.

    Returns None if the log is absent (the adopter case). Returns a dict
    with `start` None if the log holds no parseable session-start timestamp.
    """
    log = resolve_working("degradation-watch-log.md", repo_root=root)
    if log is None or not log.is_file():
        return None
    text = _read(log)
    starts = _session_start_stamps(text)
    _EPOCH0 = datetime.min.replace(tzinfo=timezone.utc)
    start = max(starts, key=lambda t: _parse_ts(t) or _EPOCH0) if starts else None
    elapsed = None
    if start:
        now = now or datetime.now(timezone.utc)
        dt = _parse_ts(start)
        if dt is not None:
            secs = int((now - dt).total_seconds())
            if secs >= 0:
                elapsed = f"{secs // 3600}h{(secs % 3600) // 60}m"
    compactions = len(re.findall(r"\|\s*compaction\s*\|", text))
    return {"start": start, "elapsed": elapsed, "compaction_rows": compactions}


def snapshot(root: Path) -> str:
    lib = library_version(root)
    rme = readme_version(root)
    lines = [
        "## Mechanical snapshot (generated by `tools/handoff-snapshot.py`; verify before pasting)",
        "",
        f"- **Library Version:** {lib or 'UNKNOWN'}",
        f"- **README Version:** {rme or 'UNKNOWN'}",
        f"- **Gates:** {gate_count(root)} (run_gate count in `tools/run_all_audits.sh`)",
        f"- **Pack rules:** {rule_count(root)} / **skills:** {skill_count(root)} / **commands:** {command_count(root)}",
        f"- **HEAD:** `{head_sha(root) or 'UNKNOWN'}` (run the pre-push guard to confirm green-at this sha)",
    ]
    sm = session_metrics(root)
    if sm is not None:
        start = sm["start"] or "UNKNOWN"
        elapsed = sm["elapsed"] or "?"
        lines.append(
            f"- **Session:** start {start}, elapsed {elapsed}, "
            f"{sm['compaction_rows']} stamped compaction row(s) in the working log "
            "(count the rows at/after this session-start for the per-session figure)"
        )
    return "\n".join(lines) + "\n"


def _self_test() -> int:
    """Build a throwaway fixture repo and assert every parser reads it correctly."""
    failures = []
    _prev_store = os.environ.get("GRC_STORE")
    with tempfile.TemporaryDirectory() as td:
        # hermetic: point the store at the tempdir so resolve_working_for_write NEVER
        # touches the ambient operational store (GRC_STORE is absolute, repo_root-independent).
        os.environ["GRC_STORE"] = str(Path(td) / "store")
        root = Path(td) / "grc_library"
        root.mkdir()
        (root / "tools").mkdir()
        (root / "guardrails" / "governance").mkdir(parents=True)
        (root / "guardrails" / "skills" / "alpha").mkdir(parents=True)
        (root / "guardrails" / "skills" / "beta").mkdir(parents=True)
        (root / ".claude" / "commands").mkdir(parents=True)

        (root / "README.md").write_text(
            "# X\n\n**Library Version:** 2026.07.729 (CalVer)\n"
            "**README Version:** 1.10.91 (semantic)\n", encoding="utf-8")
        # 3 run_gate lines + a decoy that must NOT count
        (root / "tools" / "run_all_audits.sh").write_text(
            '#!/bin/bash\nrun_gate() {\n  : ; }\n'
            'run_gate "A" python3 tools/a.py\n'
            'run_gate "B" python3 tools/b.py\n'
            '  # run_gate in a comment must not count\n'
            'run_gate "C" python3 tools/c.py\n', encoding="utf-8")
        for n in ("one", "two", "three"):
            (root / "guardrails" / "governance" / f"{n}.md").write_text("r", encoding="utf-8")
        (root / "guardrails" / "skills" / "alpha" / "SKILL.md").write_text("s", encoding="utf-8")
        (root / "guardrails" / "skills" / "beta" / "SKILL.md").write_text("s", encoding="utf-8")
        (root / "guardrails" / "skills" / "beta" / "NOT-a-skill.md").write_text("x", encoding="utf-8")
        for n in ("resume", "validate", "retro", "fitness"):
            (root / ".claude" / "commands" / f"{n}.md").write_text("c", encoding="utf-8")

        checks = [
            ("library_version", library_version(root), "2026.07.729"),
            ("readme_version", readme_version(root), "1.10.91"),
            ("gate_count (3, decoy comment excluded)", gate_count(root), 3),
            ("rule_count", rule_count(root), 3),
            ("skill_count (SKILL.md only)", skill_count(root), 2),
            ("command_count", command_count(root), 4),
        ]
        for name, got, want in checks:
            if got != want:
                failures.append(f"  {name}: got {got!r}, want {want!r}")

        # session_metrics: absent log -> None
        if session_metrics(root) is not None:
            failures.append("  session_metrics: expected None when the log is absent")

        # session_metrics: present log -> parse latest start + fixed-clock elapsed
        dw = resolve_working_for_write("degradation-watch-log.md", repo_root=root)
        dw.parent.mkdir(parents=True, exist_ok=True)
        dw.write_text(
            "| 2026-07-29T10:00:00Z | session-start | earlier full-seconds |\n"
            "- session-start 2026-07-29T12:00:00Z (prose full-seconds)\n"
            "| session-start | 2026-07-29T11:00Z | table token-first |\n"
            "- **2026-07-29T14:00Z** session-start: bold-iso |\n"
            "| 2026-07-29T15:30Z | session-start | minute-only |\n"
            "| 2026-07-29T15:30:45Z | session-start | SAME-MINUTE full-seconds, the TRUE latest (lexicographic sort would wrongly pick 15:30Z) |\n"
            "session-start-continuation 2026-07-29T16:45Z (suffix decoy, must not match)\n"
            "| 2026-07-29T17:00:00Z | compaction | DECOY note mentions session-start 2026-07-29T17:00:00Z (newer; must be excluded) |\n"
            "| 2026-07-29T13:00:00Z | compaction | C1 |\n", encoding="utf-8")
        now = datetime(2026, 7, 29, 18, 0, 0, tzinfo=timezone.utc)
        sm = session_metrics(root, now=now)
        if not sm or sm["start"] != "2026-07-29T15:30:45Z":
            failures.append(f"  session_metrics.start (minutes-only latest): got {sm}")
        elif sm["elapsed"] != "2h29m":
            failures.append(f"  session_metrics.elapsed (same-minute mixed): got {sm['elapsed']!r}, want '2h29m'")
        elif sm["compaction_rows"] != 2:
            failures.append(f"  session_metrics.compaction_rows: got {sm['compaction_rows']}")
        # matcher recall + decoy exclusion (guard-input reality fixture): every layout recalled,
        # the newer compaction-note decoy and the session-start-<suffix> row both excluded.
        _mf = (
            "| session-start | 2026-07-29T11:00Z | token-first |\n"
            "session-start | 2026-07-29T12:00:00Z | reversed |\n"
            "- 2026-07-29T14:00:00Z  session-start: iso-first\n"
            "### session-start 2026-07-29T17:00Z\n"
            "- session-start: 2026-07-29T18:30:45Z\n"
            "| 2026-07-29T09:30:00Z | considered | quote: | session-start 2026-12-31T23:59:59Z | end (pipe-prose decoy) |\n"
            "| 2026-07-29T23:59:59Z | compaction | DECOY session-start 2026-07-29T23:59:59Z |\n"
            "session-start-continuation 2026-07-29T22:00Z\n")
        _st = _session_start_stamps(_mf)
        for _real in ("2026-07-29T11:00Z", "2026-07-29T12:00:00Z", "2026-07-29T14:00:00Z",
                      "2026-07-29T17:00Z", "2026-07-29T18:30:45Z"):
            if _real not in _st:
                failures.append(f"  _session_start_stamps recall gap: {_real} missing")
        if "2026-12-31T23:59:59Z" in _st:
            failures.append("  _session_start_stamps: pipe-prose decoy iso leaked (line-anchored must exclude)")
        if "2026-07-29T09:30:00Z" in _st:
            failures.append("  _session_start_stamps: decoy host considered-row iso leaked")
        if "2026-07-29T23:59:59Z" in _st:
            failures.append("  _session_start_stamps: compaction-note DECOY leaked")
        if "2026-07-29T22:00Z" in _st:
            failures.append("  _session_start_stamps: session-start-<suffix> leaked")
        if _st and max(_st) != "2026-07-29T18:30:45Z":
            failures.append(f"  _session_start_stamps newest: got {max(_st)}")

    if _prev_store is None:
        os.environ.pop("GRC_STORE", None)
    else:
        os.environ["GRC_STORE"] = _prev_store
    if failures:
        print("handoff-snapshot self-test: FAILED")
        print("\n".join(failures))
        return 1
    print("handoff-snapshot self-test: OK, 6 parsers + session-metrics (absent + present) verified.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit mechanical handoff-snapshot facts (read-only).")
    ap.add_argument("--self-test", action="store_true", help="run the parser self-test and exit")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    sys.stdout.write(snapshot(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
