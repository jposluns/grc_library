#!/usr/bin/env python3
"""recover-codex-verdict.py - recover a stranded codex worker verdict from its log.

When a codex exec-dispatch worker COMPLETES a review but its delivery file never
lands in the tray (the codex-cli 0.146.1 multi_agent collab-wait strand, diagnosed
2026-08-08 in the private third-party-issues register: the collab "wait" tool call
is rejected with timeout_ms below the router's 10000 ms floor and the worker loops
until its turn budget is exhausted before the delivery step), the finished verdict
is stranded in the worker's wrapper log. This tool recovers the final verdict
block from that log and writes a recovery delivery into the tray, under a
RECOVERED-FROM-LOG banner. It is the defence-in-depth backstop queued by that
diagnosis; the primary fix (disabling the multi_agent features at dispatch) lives
in the host wrapper.

EXTRACTION INTEGRITY: the tool NEVER writes a recovery whose text could be wrong
or partial; ambiguity REFUSES. The codex exec transcript repeats the final agent
message twice (as the last `codex` block and again after the tokens-used trailer),
and that redundancy is the integrity check: when a trailer exists, the tail after
it must agree (whitespace-trimmed) with the FULL region between the last preceding
`codex` marker and the trailer; there is no single-copy trailer-only mode. A
candidate that quotes transcript structure is TAINTED and refuses, and an empty
tail after the trailer refuses rather than falling back to an earlier block. A log
with no `codex` marker line anywhere is not a recoverable codex transcript at all.

GUARD-INPUT RESIDUE (stated per validate-inference-before-action, "Guard inputs"):
a recovery proves the log CONTAINED a terminal verdict block, never that the
review ran to a semantically complete delivery. The recovery file is a LOWER-TRUST
artefact: the orchestrator re-verifies every positive finding at source, exactly
as it would for a normal delivery.

Host constants (the wrapper log dir and the delivery tray dir) are OPERATIONAL
data: the private CONFIG is read at import (like exec-dispatch), over neutral
placeholders, and the exit-2 placeholder guard fires before any LOG or TRAY
filesystem access, so an un-configured run fails loud rather than leaking a real
layout (the exec-dispatch disclosure pattern, PR #1457).

Modes:
  <id-substring>            recover the single matching codex log's final verdict
  <id-substring> --dry-run  print what would be written; write nothing
  <id-substring> --force    recover even when the tray already holds an anchored
                            delivery match for the worker (see Refusals)
  --scan                    list codex logs holding a verdict but no matching
                            delivery in the tray (recovery candidates); no writes.
                            Bounded to the last 72 hours by default (the strand
                            class surfaces within hours; unbounded, months of
                            consumed logs drown the signal); --all lifts the bound
  --self-test               run the synthetic-fixture unit tests

Refusals (ignorance refuses, never a silent wrong or partial recovery):
  * an id substring matching MORE than one codex log refuses and lists matches
  * a log with NO bare `codex` marker line anywhere refuses: it is not a
    recoverable codex transcript (this exits non-zero with a clear message)
  * extraction refuses on ambiguity: a TAINTED candidate (the verdict quotes
    transcript structure), an empty or disagreeing pre-trailer comparison
    copy, or an empty tail after the tokens-used trailer
  * a tray already holding an anchored delivery match for the worker refuses,
    listing the matching filename(s); --force recovers anyway (a same-worker
    different-order tray file can legitimately trip the guard)
  * an unconfigured placeholder path exits 2 before any log or tray access
  * an already-existing recovery file is never overwritten (atomic hard-link
    publish; no check-then-write window)

Stdlib-only (project convention). PROJECT-ONLY operational machinery, in the same
class as exec-dispatch.py / manage-workers.py / collect-deliveries.py.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path

# --- host constants (project-only; loaded from the private config) -----------------
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT.parent / "grc_library_private" / "worker-accounts.json"


def _wrapper_cfg() -> dict:
    try:
        w = json.loads(DEFAULT_CONFIG.read_text(encoding="utf-8")).get("wrapper", {})
        return w if isinstance(w, dict) else {}
    except Exception:
        return {}


_W = _wrapper_cfg()
# The wrappers redirect each worker's full stdout/stderr to a dated per-worker log
# under the wrapper LOGDIR (same key exec-dispatch reads).
WORKER_LOG_DIR = Path(_W.get("log_dir", "/nonexistent/worker-logs"))
# The exec-dispatch delivery tray the codex sandbox is allowed to write into.
# NEW config key: `wrapper.tray_dir` (proposed by this tool; add to the private config).
TRAY_DIR = Path(_W.get("tray_dir", "/nonexistent/worker-tray"))
del _W

BANNER_MARK = "RECOVERED-FROM-LOG"

# Lines that begin a labelled item in a codex exec transcript. Marker lines are
# matched AFTER .strip(), everywhere (label recognition, block boundaries, and
# the taint check), so an indented marker behaves like a flush-left one.
_MARKERS = {"codex", "exec", "user", "thinking", "tokens used"}
_COUNT_RE = re.compile(r"^[\d,]+$")

_NO_BLOCK_REASON = "no agent-message block; not a recoverable codex transcript"


# --- pure log analysis ---------------------------------------------------------------
def _last_trailer_indices(lines: list[str]) -> tuple[int, int] | None:
    """PURE. (tokens-used index, count index) of the LAST well-formed trailer.

    Well-formed = a line whose stripped text is `tokens used` whose next
    non-empty line is a bare token count (whitespace around the count line is
    tolerated). A `tokens used` line with no count after it is NOT a trailer;
    the scan keeps looking earlier.
    """
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() != "tokens used":
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and _COUNT_RE.match(lines[j].strip()):
            return (i, j)
    return None


# Terminal-verdict discriminator for FALLBACK-ONLY extraction (NO trailer): a
# recoverable final block must look terminal, not intermediate. The project's
# delivery convention ends with END OF DELIVERY; QA verdicts carry a verdict
# word or a SHIP/HOLD token. An ordinary mid-run codex message carries none, so
# requiring one keeps a truncated log's last intermediate message out of the
# tray (refuse-on-ambiguity, the tool's integrity contract).
_TERMINAL_RE = re.compile(r"END OF DELIVERY|\bverdicts?\b|\bSHIP\b|\bHOLD\b",
                          re.IGNORECASE)


def _taint(text: str) -> str | None:
    """PURE. Why a candidate quotes transcript structure, or None when clean.

    Any bare marker line (matched after .strip()) taints. A well-formed trailer
    pair necessarily starts with a bare `tokens used` marker line, so the marker
    check subsumes the pair check.
    """
    for ln in text.splitlines():
        if ln.strip() in _MARKERS:
            return f"contains a bare '{ln.strip()}' marker line"
    return None


def extract_final_verdict(text: str) -> tuple[str | None, str]:
    """PURE. (verdict, mode) on success; (None, reason) on refusal.

    INTEGRITY CONTRACT: never return text that could be wrong or partial;
    ambiguity refuses. A transcript with NO bare `codex` marker line anywhere
    refuses outright: it is not a recoverable codex transcript. When a
    well-formed tokens-used trailer exists, the primary candidate P is the
    stripped tail after the trailer's count line (the codex exec transcript
    repeats the final agent message there), and the comparison copy C is the
    FULL stripped region from after the LAST bare `codex` marker line that
    precedes the trailer's `tokens used` line, up to that `tokens used` line
    (never truncated at intervening marker lines). P and C must BOTH be
    non-empty and equal after whitespace trimming (a trimmed equality, not a
    byte-exact one); an empty C or a disagreement refuses. A tainted P (a
    bare marker line, which subsumes an embedded trailer pair) refuses, and an
    empty tail after the trailer refuses rather than falling back to an
    earlier block. When NO well-formed trailer exists (a truncated log), the
    LAST bare `codex` block runs to end-of-log and any bare marker line in
    that region refuses. Success modes are exactly `trailer+fallback-agree`
    and `fallback-only` (fallback-only marks a truncated log).
    """
    lines = text.splitlines()
    codex_idx = [i for i, ln in enumerate(lines) if ln.strip() == "codex"]
    if not codex_idx:
        return (None, _NO_BLOCK_REASON)
    trailer = _last_trailer_indices(lines)
    if trailer is not None:
        tu, cnt = trailer
        primary = "\n".join(lines[cnt + 1:]).strip()
        if not primary:
            return (None, "empty tail after the tokens-used trailer; refusing "
                          "(never falling back to an earlier block)")
        taint = _taint(primary)
        if taint:
            return (None, f"trailer tail is tainted: it {taint}; the verdict "
                          "quotes transcript structure, extraction unreliable")
        prior = [i for i in codex_idx if i < tu]
        if not prior:
            return (None, "no codex agent-message block precedes the tokens-used "
                          "trailer; the duplicated-final-message integrity check "
                          "cannot run, refusing")
        compare = "\n".join(lines[prior[-1] + 1:tu]).strip()
        if not compare:
            return (None, "empty comparison copy between the last codex marker "
                          "and the tokens-used trailer; the duplicated-final-"
                          "message integrity check cannot run, refusing")
        if primary != compare:
            return (None, "primary/fallback disagree: the trailer tail and the "
                          "full pre-trailer codex region differ (whitespace-"
                          "trimmed comparison); refusing a possibly wrong or "
                          "partial recovery")
        return (primary, "trailer+fallback-agree")
    start = codex_idx[-1] + 1
    region = "\n".join(lines[start:]).strip()
    if not region:
        return (None, "empty final codex block and no tokens-used trailer; "
                      "nothing recoverable")
    taint = _taint(region)
    if taint:
        return (None, f"fallback codex block is tainted: it {taint}; with no "
                      "tokens-used trailer the extraction cannot be disambiguated")
    if not _TERMINAL_RE.search(region):
        return (None, "fallback codex block carries no terminal-verdict marker "
                      "(no END OF DELIVERY / verdict / SHIP / HOLD token); a "
                      "truncated log can end on an ordinary intermediate "
                      "message, so an unmarked block refuses rather than "
                      "publishing a possibly partial recovery")
    return (region, "fallback-only")


def tray_references(text: str, tray_dir: Path) -> list[str]:
    """PURE. Tray filenames the transcript mentions, order-preserving and unique.

    RESIDUE: a mention proves the worker INTENDED (or attempted) a tray write, not
    that the write succeeded; existence in the tray is the separate ground truth
    the caller checks. Slash runs are tolerated because apply-patch diffs render
    the tray path with a doubled slash.
    """
    pat = re.compile(re.escape(str(tray_dir)).replace("/", "/+") + r"/+([A-Za-z0-9._-]+\.md)")
    seen: list[str] = []
    for m in pat.finditer(text):
        if m.group(1) not in seen:
            seen.append(m.group(1))
    return seen


def worker_id_from_log(name: str) -> str | None:
    """PURE. Parse the worker id from a wrapper log filename.

    The wrappers name logs `<date>_<time>_<family>_<account>_<worker-id>.log`
    (see exec-dispatch's log-glob note). RESIDUE: an account name containing an
    underscore would shift the split; the observed account charset does not, and a
    mis-split only degrades the recovery FILENAME, never the recovered content.
    """
    stem = name[:-len(".log")] if name.endswith(".log") else name
    parts = stem.split("_")
    if len(parts) >= 5:
        return "_".join(parts[4:])
    return None


def resolve_matches(matches: list) -> tuple[str, list]:
    """PURE. Refuse-on-ambiguity: ('none'|'ambiguous'|'ok', matches)."""
    if not matches:
        return ("none", [])
    if len(matches) > 1:
        return ("ambiguous", matches)
    return ("ok", matches)


def recovery_name(referenced_missing: list[str], worker_id: str | None, log_name: str) -> str:
    """PURE. RECOVERED-<original-expected-name-or-id>.md."""
    if referenced_missing:
        return "RECOVERED-" + referenced_missing[0]
    base = worker_id or Path(log_name).stem
    return "RECOVERED-" + base + ".md"


def compose_recovery(verdict: str, log_name: str, worker_id: str | None,
                     referenced: list[str], now_utc: str, mode: str) -> str:
    """PURE. The recovery body: banner + extraction mode + residue + verdict.

    The mode is one of exactly `trailer+fallback-agree` (rendered as-is) and
    `fallback-only` (rendered as the truncated-log wording below).
    """
    extraction = ("trailer missing (truncated log): fallback extraction of a "
                  "terminal-marked block"
                  if mode == "fallback-only" else mode)
    head = [
        f"# {BANNER_MARK}: stranded codex verdict recovery",
        "",
        f"- source log: {log_name}",
        f"- worker id: {worker_id or 'unknown (unparsed log name)'}",
        f"- recovered: {now_utc} UTC by tools/recover-codex-verdict.py",
        f"- extraction: {extraction}",
        f"- tray file(s) the log references: {', '.join(referenced) if referenced else 'none found'}",
        "",
        "RESIDUE (guard-inputs discipline): this recovery proves the worker LOG",
        "contained a terminal verdict block; it does NOT prove the review ran to a",
        "semantically complete delivery. Treat this as a LOWER-TRUST artefact: the",
        "orchestrator re-verifies every positive finding at source before acting,",
        "and a clean verdict here is corroborated, never trusted on recovery alone.",
        "",
        "---",
        "",
    ]
    return "\n".join(head) + verdict.rstrip() + "\n"


def config_ok(*paths: Path) -> bool:
    """PURE. False when any host path is still the fail-loud placeholder."""
    return not any(str(p).startswith("/nonexistent/") for p in paths)


# --- filesystem shell ------------------------------------------------------------------
def within_window(mtime: float, now: float, hours: float | None) -> bool:
    """PURE. None means unbounded; else the log's mtime falls inside the window."""
    if hours is None:
        return True
    return (now - mtime) <= hours * 3600.0


def matching_logs(log_dir: Path, needle: str) -> list[Path]:
    return sorted(p for p in log_dir.glob("*_codex_*.log") if needle in p.name)


def delivery_matches(tray_dir: Path, refs: list[str], worker_id: str | None) -> list[str]:
    """Tray filenames evidencing this worker's result already landed.

    ANCHORED matching only, never a bare substring scan: an exact match on a
    referenced filename (or its RECOVERED- twin), or a worker-id anchor of one
    of the three forms `<worker-id>__*`, `RECOVERED-<worker-id>.md`, or
    `RECOVERED-<worker-id>__*` (collect-deliveries names tray files
    `<worker-id>__<order-id>.md`; recoveries prefix RECOVERED-). RESIDUE:
    anchored matching can false-negative on hand-renamed deliveries; the log's
    tray references stay the primary evidence.
    """
    if not tray_dir.is_dir():
        return []
    hits: list[str] = []
    for r in refs:
        for cand in (r, "RECOVERED-" + r):
            if (tray_dir / cand).exists() and cand not in hits:
                hits.append(cand)
    if worker_id:
        for f in sorted(tray_dir.glob("*.md")):
            n = f.name
            if ((n.startswith(worker_id + "__")
                 or n == "RECOVERED-" + worker_id + ".md"
                 or n.startswith("RECOVERED-" + worker_id + "__"))
                    and n not in hits):
                hits.append(n)
    return hits


def delivered_already(tray_dir: Path, refs: list[str], worker_id: str | None) -> bool:
    """Boolean form of delivery_matches (same check; see its docstring)."""
    return bool(delivery_matches(tray_dir, refs, worker_id))


def write_recovery(dest: Path, content: str, dry_run: bool) -> bool:
    """Write via a pid-suffixed temp name (`<dest-name>.part.<pid>`, unique per
    process so two concurrent recoveries never collide on the temp file), then
    publish with os.link(tmp, dest) + tmp unlink (the #1171 delivery-completeness
    pattern, hardened): the hard link itself raises FileExistsError when dest
    exists, atomically, with no exists()-then-rename window. Never overwrites.
    Returns True when written."""
    if dry_run:
        return False
    tmp = dest.with_name(dest.name + ".part." + str(os.getpid()))
    tmp.write_text(content, encoding="utf-8")
    try:
        os.link(tmp, dest)
    finally:
        tmp.unlink(missing_ok=True)
    return True


def do_scan(log_dir: Path, tray_dir: Path, since_hours: float | None) -> int:
    """List logs whose order has a terminal verdict but no matching delivery."""
    import time as _time
    now = _time.time()
    candidates = []
    skipped_old = 0
    for p in sorted(log_dir.glob("*_codex_*.log")):
        if not within_window(p.stat().st_mtime, now, since_hours):
            skipped_old += 1
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print(f"  UNREADABLE: {p.name} ({e})")
            continue
        verdict, mode = extract_final_verdict(text)
        if verdict is None:
            if mode != _NO_BLOCK_REASON:
                print(f"  EXTRACTION REFUSED: {p.name} ({mode})")
            continue
        refs = tray_references(text, tray_dir)
        wid = worker_id_from_log(p.name)
        if not delivered_already(tray_dir, refs, wid):
            candidates.append((p.name, wid, refs))
    bound = ("unbounded" if since_hours is None
             else f"last {since_hours:g} hours; {skipped_old} older log(s) outside the "
                  "window, --all lifts the bound")
    if not candidates:
        print(f"scan ({bound}): no recovery candidates (every in-window verdict-bearing "
              "codex log has a matching delivery in the tray)")
        return 0
    print(f"scan ({bound}): {len(candidates)} recovery candidate(s), newest last:")
    for name, wid, refs in candidates:
        want = ", ".join(refs) if refs else "no tray reference in log"
        print(f"  {name}\n    worker id: {wid or 'unparsed'}; expected delivery: {want}")
    print("scan wrote nothing; recover one with: recover-codex-verdict.py <id-substring>")
    return 0


def do_recover(needle: str, log_dir: Path, tray_dir: Path, dry_run: bool,
               force: bool = False) -> int:
    status, matches = resolve_matches(matching_logs(log_dir, needle))
    if status == "none":
        print(f"ERROR: no codex worker log matches '{needle}' under the configured log dir")
        return 1
    if status == "ambiguous":
        print(f"REFUSED: '{needle}' matches {len(matches)} logs; disambiguate to exactly one:")
        for p in matches:
            print(f"  {p.name}")
        return 1
    log = matches[0]
    text = log.read_text(encoding="utf-8", errors="replace")
    verdict, mode = extract_final_verdict(text)
    if verdict is None:
        print(f"REFUSED: cannot recover from {log.name}: {mode}")
        return 1
    refs = tray_references(text, tray_dir)
    wid = worker_id_from_log(log.name)
    hits = delivery_matches(tray_dir, refs, wid)
    if hits and not force:
        print("REFUSED: the tray already holds a matching delivery for this worker:")
        for h in hits:
            print(f"  {h}")
        print("use --force to recover anyway (a same-worker different-order tray "
              "file can legitimately trip this guard)")
        return 1
    missing = [r for r in refs if not (tray_dir / r).exists()]
    now_utc = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
    content = compose_recovery(verdict, log.name, wid, refs, now_utc, mode)
    dest = tray_dir / recovery_name(missing, wid, log.name)
    if dry_run:
        print(f"DRY-RUN: would write {dest} ({len(content)} chars); content follows\n")
        print(content)
        return 0
    try:
        write_recovery(dest, content, dry_run=False)
    except FileExistsError:
        print(f"REFUSED: {dest} already exists; not overwriting a prior recovery")
        return 1
    print(f"recovered verdict from {log.name}\n  -> {dest}")
    print("REMINDER: lower-trust artefact; re-verify positive findings at source.")
    return 0


# --- self-test (synthetic fixtures only; they mirror NO real worker, account, ---------
# --- order, or host layout) ------------------------------------------------------------
def self_test() -> int:
    import contextlib
    import io
    import tempfile

    failures, total = [], [0]

    def check(name, got, want):
        total[0] += 1
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}: {name}" + ("" if ok else f" -> {got!r}, expected {want!r}"))
        if not ok:
            failures.append(name)

    # SYNTHETIC transcript in the healthy duplicated shape: the final message
    # appears as the last codex block AND again after the tokens-used trailer.
    syn_dup = "\n".join([
        "Reading additional input from stdin...",
        "Synthetic Codex vX.Y.Z",
        "--------",
        "user",
        "synthetic brief (SYNTHETIC FIXTURE)",
        "exec",
        "/bin/sh -lc 'true' in /tmp/syn",
        " succeeded in 1ms:",
        "codex",
        "Intermediate synthetic note.",
        "codex",
        "# Verdict: SYNTHETIC-PASS",
        "Final synthetic verdict body.",
        "tokens used",
        "12,345",
        "# Verdict: SYNTHETIC-PASS",
        "Final synthetic verdict body.",
    ])
    check("duplicated final message agrees (trailer+fallback-agree)",
          extract_final_verdict(syn_dup),
          ("# Verdict: SYNTHETIC-PASS\nFinal synthetic verdict body.",
           "trailer+fallback-agree"))

    # SYNTHETIC healthy duplicated transcript with a multi-paragraph verdict:
    # the FULL-WIDTH comparison copy spans the internal blank line intact.
    syn_dup_blank = "\n".join([
        "user",
        "synthetic brief (SYNTHETIC FIXTURE)",
        "codex",
        "Paragraph one of the synthetic verdict.",
        "",
        "Paragraph two of the synthetic verdict.",
        "tokens used",
        "7",
        "Paragraph one of the synthetic verdict.",
        "",
        "Paragraph two of the synthetic verdict.",
    ])
    check("healthy multi-paragraph duplicate agrees (full-width comparison)",
          extract_final_verdict(syn_dup_blank),
          ("Paragraph one of the synthetic verdict.\n\n"
           "Paragraph two of the synthetic verdict.",
           "trailer+fallback-agree"))

    # SYNTHETIC transcript whose trailer tail DIFFERS from the pre-trailer codex
    # region: under the integrity contract this refuses (never a partial pick).
    syn_mismatch = "\n".join([
        "user",
        "synthetic brief (SYNTHETIC FIXTURE)",
        "codex",
        "Older synthetic verdict, must NOT win.",
        "tokens used",
        "12,345",
        "# Verdict: SYNTHETIC-PASS",
        "Final synthetic verdict body.",
    ])
    got = extract_final_verdict(syn_mismatch)
    check("primary/fallback disagreement refuses",
          (got[0], "disagree" in got[1]), (None, True))

    # ROUND-2 PROBE D (SYNTHETIC): the duplicate copy opens with a quoted
    # well-formed trailer pair, so the trailer anchor lands on the quoted pair
    # and the clean-looking residual tail disagrees with the FULL pre-trailer
    # region; the full-width comparison refuses instead of returning "V".
    syn_probe_d = "\n".join([
        "user",
        "synthetic brief (SYNTHETIC FIXTURE)",
        "codex",
        "tokens used",
        "1,234",
        "V",
        "tokens used",
        "1,234",
        "tokens used",
        "1,234",
        "V",
    ])
    got = extract_final_verdict(syn_probe_d)
    check("probe D: quoted trailer pair at the verdict head refuses (full-width)",
          (got[0], "disagree" in got[1]), (None, True))

    # ROUND-2 PROBE E (SYNTHETIC): a byte-symmetric trailer sandwich with no
    # codex marker anywhere is not a recoverable codex transcript.
    check("probe E: byte-symmetric log with no codex marker refuses",
          extract_final_verdict("X\ntokens used\n1\nX"),
          (None, _NO_BLOCK_REASON))

    # SYNTHETIC transcript with NO trailer: the LAST codex block wins (fallback-only).
    syn_multi = "\n".join([
        "user",
        "synthetic brief",
        "codex",
        "First synthetic block, must NOT win.",
        "exec",
        "/bin/sh -lc 'true'",
        "codex",
        "# Verdict: SYNTHETIC-HOLD",
        "Last synthetic block wins.",
    ])
    check("last codex block wins without a trailer (fallback-only)",
          extract_final_verdict(syn_multi),
          ("# Verdict: SYNTHETIC-HOLD\nLast synthetic block wins.", "fallback-only"))

    check("single codex block WITH a terminal marker extracts (fallback-only)",
          extract_final_verdict("user\nbrief\ncodex\nonly block verdict: HOLD"),
          ("only block verdict: HOLD", "fallback-only"))
    got_intermediate = extract_final_verdict(
        "user\nbrief\ncodex\nIntermediate note, not terminal.")
    check("an unmarked intermediate final block refuses (terminal grammar)",
          (got_intermediate[0], got_intermediate[1].startswith(
              "fallback codex block carries no terminal-verdict marker")),
          (None, True))
    check("exec-only log refuses (no agent-message block anywhere)",
          extract_final_verdict("user\nbrief\nexec\n/bin/sh -lc 'true'"),
          (None, _NO_BLOCK_REASON))

    # CONTRACT (retired trailer-only mode): a well-formed trailer with NO codex
    # marker anywhere now refuses instead of returning a trailer-only verdict.
    check("trailer without any codex marker refuses (trailer-only retired)",
          extract_final_verdict("tokens used\n   1,234   \nsolo verdict tail"),
          (None, _NO_BLOCK_REASON))

    # Whitespace around the count line is still tolerated when the duplicated
    # copies agree.
    check("whitespace-padded count line accepted (trailer+fallback-agree)",
          extract_final_verdict("codex\nsolo verdict tail\ntokens used\n   1,234   \nsolo verdict tail"),
          ("solo verdict tail", "trailer+fallback-agree"))

    # An empty comparison copy (codex marker immediately followed by the
    # trailer) refuses: the duplicated-final-message check cannot run.
    got = extract_final_verdict("codex\ntokens used\n5\nV")
    check("empty comparison copy refuses",
          (got[0], "comparison copy" in got[1]), (None, True))

    # CONTRACT CHANGE: an empty tail after a well-formed trailer REFUSES,
    # never falling back to an earlier block.
    got = extract_final_verdict("codex\nfallback body\ntokens used\n99\n")
    check("empty trailer tail refuses (no fallback to an earlier block)",
          (got[0], "empty tail" in got[1]), (None, True))

    # SYNTHETIC tainted tail: the verdict body quotes an embedded
    # "tokens used"+count pair; the anchor lands on the quoted pair and the
    # residual tail still quotes a bare marker, so extraction refuses as tainted.
    syn_taint_tail = "\n".join([
        "codex",
        "duplicate copy (SYNTHETIC FIXTURE)",
        "tokens used",
        "77",
        "# Verdict quoting transcript structure (SYNTHETIC FIXTURE)",
        "tokens used",
        "1,234",
        "codex",
        "a quoted agent line.",
    ])
    got = extract_final_verdict(syn_taint_tail)
    check("tainted trailer tail refuses (embedded tokens-used pair in the verdict)",
          (got[0], "tainted" in got[1]), (None, True))

    # SYNTHETIC tainted fallback: no well-formed trailer anywhere (truncated log)
    # and the last codex block quotes a bare "tokens used" marker line.
    syn_taint_fb = "\n".join([
        "user",
        "synthetic brief",
        "codex",
        "# Verdict quoting structure (SYNTHETIC FIXTURE)",
        "tokens used",
        "not a count so no trailer",
    ])
    got = extract_final_verdict(syn_taint_fb)
    check("tainted fallback refuses (quoted marker, no trailer)",
          (got[0], "tainted" in got[1]), (None, True))

    check("indented codex label recognized (markers matched after strip)",
          extract_final_verdict("user\nbrief\n  codex  \nonly block verdict: HOLD"),
          ("only block verdict: HOLD", "fallback-only"))
    got = extract_final_verdict("codex\nbody line\n  exec  \nignored")
    check("indented marker taints a fallback-only block (strip matching)",
          (got[0], "tainted" in got[1]), (None, True))

    tray = Path("/syn/tray")  # SYNTHETIC path, never touched
    syn_refs = ("exec\ncat /syn/tray/syn-delivery.md\n"
                "diff --git a//syn/tray/syn-delivery.md b//syn/tray/syn-delivery.md\n")
    check("tray references found once through single and doubled slashes",
          tray_references(syn_refs, tray), ["syn-delivery.md"])

    check("worker id parsed from synthetic log name",
          worker_id_from_log("2026-01-01_000000_codex_synacct_codex-synacct-20260101T000000Z-0000.log"),
          "codex-synacct-20260101T000000Z-0000")
    check("unparseable log name yields None", worker_id_from_log("odd.log"), None)

    check("zero matches refuse", resolve_matches([]), ("none", []))
    check("two matches refuse (no newest-wins guess)",
          resolve_matches(["a", "b"])[0], "ambiguous")
    check("one match proceeds", resolve_matches(["a"])[0], "ok")

    check("recovery name prefers the missing referenced filename",
          recovery_name(["syn-delivery.md"], "wid-x", "log.log"),
          "RECOVERED-syn-delivery.md")
    check("recovery name falls back to the worker id",
          recovery_name([], "wid-x", "log.log"), "RECOVERED-wid-x.md")

    body = compose_recovery("V", "syn.log", "wid-x", [], "2026-01-01 00:00",
                            "trailer+fallback-agree")
    check("banner mark present", BANNER_MARK in body, True)
    check("residue statement present", "does NOT prove" in body, True)
    check("verdict carried", body.rstrip().endswith("V"), True)
    check("extraction mode recorded in the banner",
          "- extraction: trailer+fallback-agree" in body, True)
    body_fb = compose_recovery("V", "syn.log", None, [], "2026-01-01 00:00", "fallback-only")
    check("fallback-only banner marks the truncated-log extraction",
          "trailer missing (truncated log): fallback extraction" in body_fb, True)

    # Anchored delivered_already (SYNTHETIC tray contents; no real worker mirrored).
    with tempfile.TemporaryDirectory() as td:
        syn_tray = Path(td)
        (syn_tray / "zz-widX__o1.md").write_text("x", encoding="utf-8")
        check("substring near-miss is NOT a delivery match",
              delivered_already(syn_tray, [], "widX"), False)
        (syn_tray / "widX__o1.md").write_text("x", encoding="utf-8")
        check("anchored <worker-id>__ delivery detected",
              delivered_already(syn_tray, [], "widX"), True)
        (syn_tray / "RECOVERED-widY.md").write_text("x", encoding="utf-8")
        check("anchored RECOVERED-<worker-id>.md detected",
              delivered_already(syn_tray, [], "widY"), True)
        (syn_tray / "RECOVERED-widZ__extra.md").write_text("x", encoding="utf-8")
        check("anchored RECOVERED-<worker-id>__ detected",
              delivered_already(syn_tray, [], "widZ"), True)
        (syn_tray / "syn-ref.md").write_text("x", encoding="utf-8")
        check("existing referenced tray file counts as delivered",
              delivered_already(syn_tray, ["syn-ref.md"], None), True)

    # do_recover delivered-already guard + --force (SYNTHETIC log/tray fixtures).
    with tempfile.TemporaryDirectory() as td:
        logd = Path(td) / "logs"
        trayd = Path(td) / "tray"
        logd.mkdir()
        trayd.mkdir()
        (logd / "2026-01-01_000000_codex_synacct_wid-syn-1.log").write_text("\n".join([
            "user",
            "synthetic brief (SYNTHETIC FIXTURE)",
            "codex",
            "# Verdict: SYNTHETIC-PASS (recover test)",
            "tokens used",
            "12",
            "# Verdict: SYNTHETIC-PASS (recover test)",
        ]), encoding="utf-8")
        (trayd / "wid-syn-1__syn-order.md").write_text("prior delivery", encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = do_recover("wid-syn-1", logd, trayd, dry_run=False, force=False)
        check("do_recover refuses on an anchored existing delivery", rc, 1)
        check("refusal names the matching tray file",
              "wid-syn-1__syn-order.md" in buf.getvalue(), True)
        check("refusal wrote nothing",
              (trayd / "RECOVERED-wid-syn-1.md").exists(), False)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = do_recover("wid-syn-1", logd, trayd, dry_run=False, force=True)
        check("--force overrides the delivered-already guard", rc, 0)
        check("forced recovery landed",
              (trayd / "RECOVERED-wid-syn-1.md").exists(), True)
        check("recovery banner carries the extraction mode",
              "trailer+fallback-agree" in (trayd / "RECOVERED-wid-syn-1.md").read_text(encoding="utf-8"),
              True)

    with tempfile.TemporaryDirectory() as td:
        dest = Path(td) / "RECOVERED-syn.md"
        check("dry-run writes nothing", write_recovery(dest, "x", dry_run=True), False)
        check("dry-run left no file", dest.exists(), False)
        check("real write lands", write_recovery(dest, "x", dry_run=False), True)
        check("real write left no pid-suffixed temp residue",
              list(Path(td).glob("RECOVERED-syn.md.part.*")), [])
        outcome = "no exception"
        try:
            write_recovery(dest, "y", dry_run=False)
        except FileExistsError:
            outcome = "FileExistsError"
        check("overwrite refused (atomic link path)", outcome, "FileExistsError")
        check("refused overwrite left no pid-suffixed temp residue",
              list(Path(td).glob("RECOVERED-syn.md.part.*")), [])
        check("refused overwrite preserved the original content",
              dest.read_text(encoding="utf-8"), "x")

    check("window: inside passes", within_window(1000.0, 1000.0 + 71 * 3600, 72.0), True)
    check("window: outside refused", within_window(1000.0, 1000.0 + 73 * 3600, 72.0), False)
    check("window: None is unbounded", within_window(0.0, 9e12, None), True)

    check("placeholder config fails loud",
          config_ok(Path("/nonexistent/worker-logs"), Path("/tmp")), False)
    check("configured paths pass", config_ok(Path("/tmp"), Path("/tmp")), True)

    print(f"self-test: {total[0] - len(failures)}/{total[0]} passed")
    return 1 if failures else 0


# --- CLI ---------------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("needle", nargs="?",
                    help="worker-or-order-id substring selecting exactly ONE codex log")
    ap.add_argument("--scan", action="store_true",
                    help="list verdict-bearing logs with no matching tray delivery; no writes")
    ap.add_argument("--since-hours", type=float, default=72.0,
                    help="scan window in hours (default 72); ignored outside --scan")
    ap.add_argument("--all", action="store_true",
                    help="lift the scan window (scan every log)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would be written; write nothing")
    ap.add_argument("--force", action="store_true",
                    help="recover anyway; a same-worker different-order tray file "
                         "can legitimately trip the guard")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not config_ok(WORKER_LOG_DIR, TRAY_DIR):
        print("ERROR: wrapper log/tray dirs are unconfigured placeholders; set "
              "`wrapper.log_dir` and `wrapper.tray_dir` in the private account config "
              "(fail-loud by design, never a silent guess)")
        return 2
    if args.scan:
        return do_scan(WORKER_LOG_DIR, TRAY_DIR, None if args.all else args.since_hours)
    if not args.needle:
        ap.error("an id substring is required unless --scan or --self-test is given")
    return do_recover(args.needle, WORKER_LOG_DIR, TRAY_DIR, args.dry_run, args.force)


if __name__ == "__main__":
    sys.exit(main())
