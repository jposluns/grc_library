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

GUARD-INPUT RESIDUE (stated per validate-inference-before-action, "Guard inputs"):
a recovery proves the log CONTAINED a terminal verdict block, never that the
review ran to a semantically complete delivery. The recovery file is a LOWER-TRUST
artifact: the orchestrator re-verifies every positive finding at source, exactly
as it would for a normal delivery.

Host constants (the wrapper log dir and the delivery tray dir) are OPERATIONAL
data: they load from the private account config's `wrapper` block, over neutral
placeholders that make any un-configured use fail loud rather than leak a real
layout (the exec-dispatch disclosure pattern, PR #1457).

Modes:
  <id-substring>            recover the single matching codex log's final verdict
  <id-substring> --dry-run  print what would be written; write nothing
  --scan                    list codex logs holding a verdict but no matching
                            delivery in the tray (recovery candidates); no writes.
                            Bounded to the last 72 hours by default (the strand
                            class surfaces within hours; unbounded, months of
                            consumed logs drown the signal); --all lifts the bound
  --self-test               run the synthetic-fixture unit tests

Refusals (ignorance refuses, never a silent empty recovery):
  * an id substring matching MORE than one codex log refuses and lists matches
  * a log with NO terminal verdict block exits non-zero with a clear message
  * an unconfigured placeholder path exits 2 before touching the filesystem
  * an already-existing recovery file is never overwritten

Stdlib-only (project convention). PROJECT-ONLY operational machinery, in the same
class as exec-dispatch.py / manage-workers.py / collect-deliveries.py.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
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

# Lines that begin a labelled item in a codex exec transcript. The extractor treats
# any of these, alone on a line, as the boundary of a `codex` (agent-message) block.
_MARKERS = {"codex", "exec", "user", "thinking", "tokens used"}
_COUNT_RE = re.compile(r"^[\d,]+$")


# --- pure log analysis ---------------------------------------------------------------
def extract_final_verdict(text: str) -> str | None:
    """PURE. Return the final verdict block of a codex exec transcript, or None.

    Primary anchor: the LAST `tokens used` marker line whose next non-empty line is
    a token count; the final agent message is everything after the count line (the
    codex exec transcript repeats the final message there at end of run). Fallback:
    the LAST `codex` block (content up to the next labelled marker or EOF), because
    a log truncated before the tokens-used trailer can still hold the finished
    verdict as its last agent message. The LAST block wins in both cases.
    """
    lines = text.splitlines()
    # Primary: the tokens-used trailer.
    for i in range(len(lines) - 1, -1, -1):
        if lines[i] == "tokens used":
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and _COUNT_RE.match(lines[j].strip()):
                tail = "\n".join(lines[j + 1:]).strip()
                if tail:
                    return tail
            break
    # Fallback: the last `codex` block.
    start = None
    for i in range(len(lines) - 1, -1, -1):
        if lines[i] == "codex":
            start = i + 1
            break
    if start is None:
        return None
    body: list[str] = []
    for ln in lines[start:]:
        if ln in _MARKERS:
            break
        body.append(ln)
    block = "\n".join(body).strip()
    return block or None


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
                     referenced: list[str], now_utc: str) -> str:
    """PURE. The recovery delivery body: banner + residue statement + verdict."""
    head = [
        f"# {BANNER_MARK}: stranded codex verdict recovery",
        "",
        f"- source log: {log_name}",
        f"- worker id: {worker_id or 'unknown (unparsed log name)'}",
        f"- recovered: {now_utc} UTC by tools/recover-codex-verdict.py",
        f"- tray file(s) the log references: {', '.join(referenced) if referenced else 'none found'}",
        "",
        "RESIDUE (guard-inputs discipline): this recovery proves the worker LOG",
        "contained a terminal verdict block; it does NOT prove the review ran to a",
        "semantically complete delivery. Treat this as a LOWER-TRUST artifact: the",
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


def delivered_already(tray_dir: Path, refs: list[str], worker_id: str | None) -> bool:
    """Is there evidence in the tray that this worker's result already landed?

    True when a referenced tray file exists, when its RECOVERED- twin exists, or
    when any tray filename carries the worker id (collect-deliveries names tray
    files `<worker-id>__<order-id>.md`, and a prior recovery names them
    `RECOVERED-<worker-id>.md`, so both are covered by the id scan).
    """
    if not tray_dir.is_dir():
        return False
    for r in refs:
        if (tray_dir / r).exists() or (tray_dir / ("RECOVERED-" + r)).exists():
            return True
    if worker_id:
        for f in tray_dir.glob("*.md"):
            if worker_id in f.name:
                return True
    return False


def write_recovery(dest: Path, content: str, dry_run: bool) -> bool:
    """Write via a temp name + atomic rename (the #1171 delivery-completeness
    pattern), refusing to overwrite. Returns True when a file was written."""
    if dry_run:
        return False
    if dest.exists():
        raise FileExistsError(str(dest))
    tmp = dest.with_suffix(dest.suffix + ".part")
    tmp.write_text(content, encoding="utf-8")
    tmp.rename(dest)
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
        verdict = extract_final_verdict(text)
        if not verdict:
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


def do_recover(needle: str, log_dir: Path, tray_dir: Path, dry_run: bool) -> int:
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
    verdict = extract_final_verdict(text)
    if not verdict:
        print(f"ERROR: no terminal verdict block found in {log.name} (no tokens-used "
              "trailer and no agent-message block); nothing recoverable, refusing a "
              "silent empty recovery")
        return 1
    refs = tray_references(text, tray_dir)
    wid = worker_id_from_log(log.name)
    missing = [r for r in refs if not (tray_dir / r).exists()]
    if refs and not missing:
        print(f"NOTHING TO RECOVER: every tray file the log references already exists "
              f"({', '.join(refs)}); the delivery landed")
        return 1
    now_utc = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
    content = compose_recovery(verdict, log.name, wid, refs, now_utc)
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
    print("REMINDER: lower-trust artifact; re-verify positive findings at source.")
    return 0


# --- self-test (synthetic fixtures only; they mirror NO real worker, account, ---------
# --- order, or host layout) ------------------------------------------------------------
def self_test() -> int:
    import tempfile

    failures, total = [], [0]

    def check(name, got, want):
        total[0] += 1
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}: {name}" + ("" if ok else f" -> {got!r}, expected {want!r}"))
        if not ok:
            failures.append(name)

    # SYNTHETIC transcript with a tokens-used trailer and TWO earlier codex blocks:
    # the trailer-anchored final message must win over both.
    syn_full = "\n".join([
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
        "Older synthetic verdict, must NOT win.",
        "tokens used",
        "12,345",
        "# Verdict: SYNTHETIC-PASS",
        "Final synthetic verdict body.",
    ])
    check("tokens-used trailer anchors the final verdict",
          extract_final_verdict(syn_full),
          "# Verdict: SYNTHETIC-PASS\nFinal synthetic verdict body.")

    # SYNTHETIC transcript with NO trailer: the LAST codex block wins.
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
    check("last codex block wins without a trailer",
          extract_final_verdict(syn_multi),
          "# Verdict: SYNTHETIC-HOLD\nLast synthetic block wins.")

    check("single codex block extracts",
          extract_final_verdict("user\nbrief\ncodex\nonly block"),
          "only block")
    check("no verdict block returns None (ignorance refuses upstream)",
          extract_final_verdict("user\nbrief\nexec\n/bin/sh -lc 'true'"), None)
    check("empty trailer tail falls back to last codex block",
          extract_final_verdict("codex\nfallback body\ntokens used\n99\n"),
          "fallback body")

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

    body = compose_recovery("V", "syn.log", "wid-x", [], "2026-01-01 00:00")
    check("banner mark present", BANNER_MARK in body, True)
    check("residue statement present", "does NOT prove" in body, True)
    check("verdict carried", body.rstrip().endswith("V"), True)

    with tempfile.TemporaryDirectory() as td:
        dest = Path(td) / "RECOVERED-syn.md"
        check("dry-run writes nothing", write_recovery(dest, "x", dry_run=True), False)
        check("dry-run left no file", dest.exists(), False)
        check("real write lands", write_recovery(dest, "x", dry_run=False), True)
        try:
            write_recovery(dest, "y", dry_run=False)
            check("overwrite refused", "no exception", "FileExistsError")
        except FileExistsError:
            check("overwrite refused", "FileExistsError", "FileExistsError")

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
    return do_recover(args.needle, WORKER_LOG_DIR, TRAY_DIR, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
