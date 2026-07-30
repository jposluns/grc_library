#!/usr/bin/env python3
"""Advisory token-spend report: orchestrator spend beside worker spend, per session.

WHY THIS EXISTS. The credit-offload metrics ledger recorded, per offloaded order, the worker's
own best-effort estimate of the tokens it spent, and called that figure "orchestrator credits
conserved". It never recorded what the orchestrator ACTUALLY spent, so the ledger could show a
running total of credits saved with no denominator: saved against what? The maintainer asked for
the pairing (2026-07-25) and the honest answer was that only half of it was being tracked.

WHAT MAKES THE PAIRING WORTH HAVING, and the thing the "credits conserved" framing gets wrong.
An orchestrator turn does not cost its output tokens. It costs its output PLUS a re-read of the
whole conversation context, which on a long session is orders of magnitude larger. Measured on
one real session: 1.35M output tokens against 800M cache-read tokens, a ratio near 600 to 1. So
a worker order that the worker estimates at 8k tokens did not save the orchestrator 8k; it saved
8k of generation plus however many context re-reads the orchestrator would have needed to do that
work inline. The ledger's conserved figure is therefore a FLOOR, not an estimate, and this tool
reports the orchestrator's own context-multiplier so the floor can be read against something.

TWO SOURCES, TWO EVIDENCE QUALITIES, KEPT SEPARATE ON PURPOSE.

  ORCHESTRATOR spend is INSTRUMENTED. It comes from the session transcript, which records a
  `usage` block per assistant message: input, output, cache-creation and cache-read tokens. This
  is a measurement, not an estimate.

  WORKER spend is SELF-REPORTED. A worker cannot read an exact in-session count either, so its
  order brief asks it to state an approximate spend and this tool parses that statement. It is an
  estimate, and the report labels it as one every time. Do not add the two columns into a single
  "total" and present it as measured: that would launder an estimate into an instrumented figure,
  which is the kind of quiet precision-inflation this project treats as a defect.

Advisory only: every reporting path exits 0. Only `--self-test` can exit non-zero. Cross-repo and
environment-dependent by nature (the transcript lives under the harness's own state directory and
the deliveries live in the file-drop root), so an absent source is reported as absent rather than
counted as zero, the same no-op-loudly shape as `audit-delivery-status.py`.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

# The harness's per-project transcript directory. Derived from the repo path the way the harness
# derives it (absolute path, separators to hyphens), never hardcoded, so this follows a checkout
# that moves on disk (the repo-root-relocation row of the change-impact surface map).
TRANSCRIPT_HOME = Path.home() / ".claude" / "projects"
FILEDROP_DEFAULT = Path("/home/grc/grc_working")
DELIVERY_TRAY_REL = "inbox/deliveries"

# A worker's self-reported spend. Deliberately several phrasings: the figure is prose in a
# delivery, not a field, so the brief's wording drifts and a single pattern would silently read
# zero for a delivery that did report one. Matches "8,400", "8400", "~8.4k", "8.4K".
# What may sit between a spend phrase and its number, and nothing else. The gap is a CONNECTOR, not
# free prose: whitespace, punctuation, and this small ALLOWLIST of joining words. Any OTHER
# alphabetic word means the number is not attributable to the phrase (it belongs to an adjacent
# clause, as in "Token spend: withheld. Budget 8,000 tokens"), so the parser REFUSES and reads
# UNKNOWN. An allowlist on purpose: it fails CLOSED on withheld / declined / unavailable and on any
# future synonym, where the earlier negation BLOCKLIST could only reject the words it enumerated.
# The #1176 sweep fed exactly that withheld string and the blocklist returned 8000.
GAP_CONNECTORS = frozenset({
    "of", "was", "is", "at", "about", "approx", "approximately",
    "roughly", "around", "some", "total", "equals",
})
# One ALPHABETIC run in the gap. Digits and punctuation are not words here: a digit in the gap would
# have been captured as the number itself, and punctuation ("~", "=", ":", "-") is always allowed.
GAP_WORD = re.compile(r"[a-z]+", re.I)

# Word multipliers, so "8.4 thousand tokens" is 8400 rather than 8.
WORD_MULT = {"thousand": 1_000, "k": 1_000, "million": 1_000_000, "m": 1_000_000}

# A spend statement. The window between the phrase and the number is DELIBERATELY SHORT (20 chars,
# was 40) and its contents are vetted by gap_is_connector: the earlier form accepted the first
# number within 40 non-digits, so an unrelated budget figure later in the sentence became the spend.
# re.S (DOTALL) lets the gap cross a newline, so a "## Token spend" heading with the figure on the
# next line is attributed instead of read as UNKNOWN. That is safe only because the allowlist rejects
# prose: a newline then connector content is a spend, a newline then a sentence is not.
SPEND_PATTERNS = (
    re.compile(r"token[s]?\s+spend\b(.{0,20}?)([0-9][0-9,\.]*)\s*([kKmM]|thousand|million)?", re.I | re.S),
    re.compile(r"token[s]?\s+(?:spent|used)\b(.{0,20}?)([0-9][0-9,\.]*)\s*([kKmM]|thousand|million)?",
               re.I | re.S),
    re.compile(r"(?:spent|used|approximately|approx\.?|about|~)(.{0,12}?)([0-9][0-9,\.]*)"
               r"\s*([kKmM]|thousand|million)?\s*tokens", re.I | re.S),
)


def parse_spend(token_text: str):
    """PURE. A worker's reported spend as an int, or None when it cannot be read.

    Returns None rather than 0 for an unparseable figure. The distinction is load-bearing: 0 means
    "reported nothing spent", None means "we could not read what it reported", and collapsing the
    second into the first would make a parsing gap look like a free order.
    """
    s = (token_text or "").strip().replace(",", "")
    if not s:
        return None
    mult = 1
    if s[-1] in "kK":
        mult, s = 1_000, s[:-1]
    elif s[-1] in "mM":
        mult, s = 1_000_000, s[:-1]
    try:
        value = float(s)
    except ValueError:
        return None
    if value < 0:
        return None
    return int(value * mult)


def gap_is_connector(gap: str) -> bool:
    """PURE. True when the phrase-to-number gap holds only connectors, so the number is the spend.

    Whitespace and punctuation are free; the only ALPHABETIC content allowed is a connector word.
    Any other word means the number belongs to a different clause and the caller must refuse it. An
    unrecognized word fails closed, which is the behaviour the tool wants for withheld / declined /
    unavailable and for words no one has enumerated yet.
    """
    return all(word.lower() in GAP_CONNECTORS for word in GAP_WORD.findall(gap))


def find_reported_spend(text: str):
    """PURE. The first readable self-reported spend in a delivery, or None.

    FIRST match, not largest: a delivery's own "Token spend" section is what the brief asks for, and
    picking the largest number would happily pick up an unrelated corpus figure the delivery quotes.

    REFUSES unless the number is attributable to the spend phrase. The gap between the phrase and the
    number may hold only connectors (see gap_is_connector); any other word means the number belongs
    to a neighbouring clause and reading it would fabricate a figure. The #1176 sweep fed
    "Token spend: withheld. Budget 8,000 tokens" and the earlier negation blocklist, which knew only
    an enumerated set of refusal words, returned 8000. An invented figure entering a report read as
    evidence is worse than None, and the tool's premise is that an unreadable figure is UNKNOWN
    rather than zero or a guess, so the parser holds to that too.
    """
    for pattern in SPEND_PATTERNS:
        for m in pattern.finditer(text or ""):
            gap, digits, word = m.group(1) or "", m.group(2), (m.group(3) or "")
            if not gap_is_connector(gap):
                continue  # a non-connector word in the gap: the number is not this phrase's spend
            # Multiply BEFORE truncating to int. Truncating first turned "8.4 thousand" into
            # 8 * 1000 = 8000 and "3.1k" into 3000, silently losing the fractional part that the
            # multiplier exists to scale.
            try:
                raw = float(digits.replace(",", ""))
            except ValueError:
                continue
            if raw < 0:
                continue
            mult = WORD_MULT.get(word.lower().strip(), 1) if word else 1
            return int(raw * mult)
    return None


def transcript_dir_for(repo_root: Path) -> Path:
    """The harness transcript directory for a repo path. Observer.

    The harness names it after the absolute repo path with BOTH path separators and underscores
    replaced by hyphens, so `/home/grc/grc_library` becomes `-home-grc-grc-library`. Getting only
    the separators produced `-home-grc-grc_library`, which does not exist; the tool reported the
    transcript as ABSENT rather than counting zero, which is how the mistake surfaced instead of
    shipping as a silent "0 tokens spent".
    """
    return TRANSCRIPT_HOME / str(repo_root.resolve()).replace("/", "-").replace("_", "-")


def sum_usage(transcript: Path) -> dict:
    """Total the per-message usage blocks in one session transcript. Observer.

    Tolerates a partially-written or corrupt line rather than aborting: a transcript is appended to
    live by the running session, so the last line can be half-flushed at read time, and refusing to
    report anything because of one torn line would be the wrong trade for an advisory tool. The
    count of unreadable lines is reported so the tolerance is visible rather than silent.
    """
    totals = {"turns": 0, "input": 0, "output": 0, "cache_write": 0, "cache_read": 0, "unreadable": 0}
    try:
        handle = transcript.open(encoding="utf-8", errors="replace")
    except OSError:
        return totals
    with handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except (ValueError, TypeError):
                totals["unreadable"] += 1
                continue
            usage = (record.get("message") or {}).get("usage") if isinstance(record, dict) else None
            if not isinstance(usage, dict):
                continue
            totals["turns"] += 1
            totals["input"] += usage.get("input_tokens") or 0
            totals["output"] += usage.get("output_tokens") or 0
            totals["cache_write"] += usage.get("cache_creation_input_tokens") or 0
            totals["cache_read"] += usage.get("cache_read_input_tokens") or 0
    return totals


def context_multiplier(totals: dict):
    """PURE. Cache-read tokens per output token, or None when output is zero.

    This is the number that makes the offload case concrete: it is roughly how many context tokens
    the orchestrator re-reads for each token it generates. A worker starts from a small context, so
    the same work done by a worker skips this multiplier entirely.
    """
    if not totals.get("output"):
        return None
    return (totals.get("cache_read") or 0) / totals["output"]


def collect_worker_spend(filedrop_root: Path):
    """Per-delivery self-reported spend from the delivery tray. Observer.

    Returns (rows, unreadable_count) where each row is (worker_id, order_id, spend_or_None). The
    tray filename is `<worker-id>__<order-id>.md`, so attribution needs no file read.
    """
    rows, unreadable = [], 0
    tray = filedrop_root / DELIVERY_TRAY_REL
    if not tray.is_dir():
        return rows, unreadable
    for path in sorted(tray.glob("*__*.md")):
        worker, _, order = path.stem.partition("__")
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            unreadable += 1
            continue
        rows.append((worker, order, find_reported_spend(text)))
    return rows, unreadable


def fmt(value) -> str:
    return "not reported" if value is None else f"{value:,}"


def report(repo_root: Path, filedrop_root: Path, session: str | None, oneline: bool) -> int:
    tdir = transcript_dir_for(repo_root)
    transcripts = []
    if tdir.is_dir():
        transcripts = sorted(tdir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if session:
        transcripts = [p for p in transcripts if session in p.stem]

    orch = sum_usage(transcripts[0]) if transcripts else None
    rows, unreadable = collect_worker_spend(filedrop_root)
    reported = [s for _, _, s in rows if s is not None]

    if oneline:
        if orch is None:
            print(f"tokens: orchestrator transcript not found under {tdir}; "
                  f"workers {len(reported)}/{len(rows)} reporting ~{sum(reported):,} (self-reported)")
            return 0
        mult = context_multiplier(orch)
        mult_text = f", {mult:.0f}x context" if mult is not None else ""
        print(f"tokens: orchestrator {orch['output']:,} out / {orch['cache_read']:,} cache-read"
              f"{mult_text} | workers ~{sum(reported):,} est. over {len(reported)} delivery(ies)")
        return 0

    print("token-spend report (advisory)")
    print()
    if orch is None:
        print(f"  ORCHESTRATOR: no transcript found under {tdir}")
        print("    Reported as absent rather than zero. The transcript lives in the harness's own")
        print("    state directory, so a different machine or harness legitimately has none here.")
    else:
        print(f"  ORCHESTRATOR (INSTRUMENTED, from {transcripts[0].name})")
        print(f"    assistant turns:      {orch['turns']:>14,}")
        print(f"    output (generated):   {orch['output']:>14,}")
        print(f"    input (uncached):     {orch['input']:>14,}")
        print(f"    cache writes:         {orch['cache_write']:>14,}")
        print(f"    cache reads:          {orch['cache_read']:>14,}")
        mult = context_multiplier(orch)
        if mult is not None:
            print(f"    context multiplier:   {mult:>13.0f}x  (cache-read tokens per output token)")
            print("      Each turn re-reads the whole conversation. This is why an offloaded order")
            print("      saves MORE than the worker's own reported spend: the worker never pays it.")
        if orch["unreadable"]:
            print(f"    unreadable lines:     {orch['unreadable']:>14,}  (live-append tear, tolerated)")
    print()
    if not rows:
        print(f"  WORKERS: no deliveries in {filedrop_root / DELIVERY_TRAY_REL}")
    else:
        print(f"  WORKERS (SELF-REPORTED ESTIMATES, {len(reported)} of {len(rows)} deliveries)")
        by_worker: dict[str, list] = {}
        for worker, _order, spend in rows:
            by_worker.setdefault(worker, []).append(spend)
        for worker in sorted(by_worker):
            spends = [s for s in by_worker[worker] if s is not None]
            print(f"    {worker:<34} {len(by_worker[worker]):>2} delivery(ies), "
                  f"~{sum(spends):,} est." if spends
                  else f"    {worker:<34} {len(by_worker[worker]):>2} delivery(ies), none reported")
        print(f"    {'TOTAL':<34} ~{sum(reported):,} est.")
        if len(reported) < len(rows):
            print(f"    {len(rows) - len(reported)} delivery(ies) reported no readable figure; counted")
            print("      as unknown, NOT as zero, so a parsing gap cannot read as a free order.")
        if unreadable:
            print(f"    {unreadable} delivery file(s) unreadable")
    print()
    print("  The two columns are NOT summed. One is measured, the other is a worker's estimate;")
    print("  adding them would present an estimate with instrumented precision.")
    return 0


def self_test() -> int:
    failures = []
    total = 0

    def check(name, got, want):
        nonlocal total
        total += 1
        if got != want:
            failures.append(name)
            print(f"  FAIL: {name} -> {got!r}, expected {want!r}")
        else:
            print(f"  PASS: {name}")

    for name, text, want in (
        ("a plain figure parses", "8400", 8400),
        ("thousands separators are stripped", "8,400", 8400),
        ("a k suffix multiplies", "8.4k", 8400),
        ("an uppercase K multiplies", "12K", 12000),
        ("an m suffix multiplies", "1.2M", 1200000),
        ("an unparseable figure is None, NOT zero", "several", None),
        ("an empty figure is None", "", None),
        ("a negative figure is rejected", "-5", None),
    ):
        check(f"parse_spend: {name}", parse_spend(text), want)

    for name, text, want in (
        ("the brief's own phrasing is found",
         "## Token spend\nApproximate token spend: 8,400.", 8400),
        ("an inline sentence is found", "This used about 5,900 tokens in total.", 5900),
        ("the tokens-spent phrasing is found", "Tokens spent: 3.1k", 3100),
        ("a delivery reporting nothing yields None",
         "# Delivery\nSome findings and no spend statement.", None),
        ("the FIRST readable figure wins, not the largest",
         "Token spend: 2,000. The corpus cites 900,000 elsewhere.", 2000),
    ):
        check(f"find_reported_spend: {name}", find_reported_spend(text), want)

    check("transcript_dir_for: underscores hyphenate too, not only separators",
          transcript_dir_for(Path("/home/grc/grc_library")).name, "-home-grc-grc-library")
    # The #1175 sweep's own cases, kept verbatim as reality fixtures. The first two are the defect:
    # the earlier parser turned a NEGATED spend statement into a real figure by grabbing an unrelated
    # budget number later in the sentence, which is worse than returning None because an invented
    # figure enters a report read as evidence.
    for name, text, want in (
        ("a negated statement yields None, not the budget figure",
         "Token spend: not reported; the task budget is 8,000 tokens.", None),
        ("a 'none' statement yields None, not the allowed budget",
         "Tokens spent: none, although the allowed budget was 8,000 tokens.", None),
        ("a spelled-out figure is unreadable, so None", "Approximate token spend: eight thousand tokens.",
         None),
        ("a word multiplier scales BEFORE truncation", "Token spend: 8.4 thousand tokens.", 8400),
        ("a fractional k scales before truncation", "Tokens spent: 3.1k", 3100),
        ("an uppercase M scales", "Token spend: 1.2M", 1200000),
    ):
        check(f"find_reported_spend: {name}", find_reported_spend(text), want)

    # The #1176 sweep (W1 + W2), kept verbatim as reality fixtures.
    # W1: a figure in a "## Token spend" SECTION was read UNKNOWN because the gap pattern had no
    # DOTALL (measured ~14 of 36 tray deliveries); re.S now lets a newline in the gap through, which
    # is safe because gap_is_connector allows only connector content there.
    # W2: the negation BLOCKLIST let non-enumerated refusals (withheld / declined / unavailable)
    # through and fabricated an adjacent budget number; the connector ALLOWLIST fails closed on all
    # of them and on any future synonym. The two COMPACT forms are the true guard (the old blocklist
    # returned 8000 on them); the "..., but the budget was ..." forms push the number past the
    # 20-char window and return None under both old and new code, so they document intent only.
    for name, text, want in (
        ("a section-format figure across a newline is found", "## Token spend\n8,400 tokens", 8400),
        ("a withheld statement yields None, not the budget figure",
         "Token spend: withheld, but the budget was 8,000 tokens.", None),
        ("a declined statement yields None, not the budget figure",
         "Token spend: declined, but the budget was 8,000 tokens.", None),
        ("an unavailable statement yields None, not the budget figure",
         "Token spend: unavailable, but the budget was 8,000 tokens.", None),
        ("a compact withheld + adjacent budget yields None, not the budget",
         "Token spend: withheld. Budget 8,000 tokens.", None),
        ("a compact declined + adjacent budget yields None, not the budget",
         "Token spend: declined. Budget 8,000 tokens.", None),
        ("the #1175 not-reported case still yields None under the allowlist",
         "Token spend: not reported; the task budget is 8,000 tokens.", None),
        ("a plain attributed figure still parses", "Token spend: 8,400", 8400),
        ("a connector-word gap ('about') still parses", "spent about 5,900 tokens", 5900),
    ):
        check(f"find_reported_spend: {name}", find_reported_spend(text), want)

    check("context_multiplier: zero output yields None, not a division error",
          context_multiplier({"output": 0, "cache_read": 100}), None)
    check("context_multiplier: the ratio is cache-read over output",
          context_multiplier({"output": 100, "cache_read": 60000}), 600.0)
    check("context_multiplier: absent cache reads count as zero, not an error",
          context_multiplier({"output": 100}), 0.0)

    # The transcript reader must tolerate a torn line (live append) and COUNT it, and must ignore a
    # record with no usage block rather than counting it as a turn.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        t = Path(td) / "s.jsonl"
        t.write_text(
            json.dumps({"message": {"usage": {"input_tokens": 5, "output_tokens": 7,
                                              "cache_read_input_tokens": 11,
                                              "cache_creation_input_tokens": 13}}}) + "\n"
            + json.dumps({"message": {"role": "user"}}) + "\n"
            + '{"message": {"usage": {"output_tok\n'
            + json.dumps({"message": {"usage": {"output_tokens": 3}}}) + "\n",
            encoding="utf-8")
        got = sum_usage(t)
        check("sum_usage: only usage-bearing records count as turns", got["turns"], 2)
        check("sum_usage: output totals across records", got["output"], 10)
        check("sum_usage: a torn line is counted, not silently dropped", got["unreadable"], 1)
        check("sum_usage: cache reads total", got["cache_read"], 11)
        check("sum_usage: a missing transcript yields zeros, not an exception",
              sum_usage(Path(td) / "nope.jsonl")["turns"], 0)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        tray = root / DELIVERY_TRAY_REL
        tray.mkdir(parents=True)
        (tray / "opus-a__order-1.md").write_text("Token spend: 1,000.", encoding="utf-8")
        (tray / "opus-a__order-2.md").write_text("no figure here", encoding="utf-8")
        (tray / "codex-b__order-3.md").write_text("Approximate token spend: 2k", encoding="utf-8")
        (tray / "README.md").write_text("not a delivery", encoding="utf-8")
        rows, bad = collect_worker_spend(root)
        check("collect_worker_spend: only <worker>__<order>.md files count", len(rows), 3)
        check("collect_worker_spend: attribution comes from the filename",
              sorted({w for w, _, _ in rows}), ["codex-b", "opus-a"])
        check("collect_worker_spend: an unreported figure stays None, not zero",
              [s for _, _, s in rows].count(None), 1)
        check("collect_worker_spend: reported figures survive parsing",
              sorted(s for _, _, s in rows if s is not None), [1000, 2000])
        check("collect_worker_spend: an absent tray is empty, not an error",
              collect_worker_spend(Path(td) / "nothing")[0], [])
        check("collect_worker_spend: unreadable count starts at zero", bad, 0)

    print()
    print(f"self-test: {total - len(failures)}/{total} passed")
    return 1 if failures else 0


def main(argv) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=os.environ.get("GRC_REPO", str(Path(__file__).resolve().parents[1])),
                    help="repo root whose transcript directory to read")
    ap.add_argument("--filedrop-root", default=os.environ.get("GRC_WORKING", str(FILEDROP_DEFAULT)),
                    help="file-drop exchange root holding the delivery tray")
    ap.add_argument("--session", help="substring of a session id; defaults to the most recent")
    ap.add_argument("--oneline", action="store_true", help="one-line form for a statusline")
    ap.add_argument("--self-test", action="store_true", help="run the fixture set")
    a = ap.parse_args(argv[1:])
    if a.self_test:
        return self_test()
    return report(Path(a.repo), Path(a.filedrop_root), a.session, a.oneline)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
