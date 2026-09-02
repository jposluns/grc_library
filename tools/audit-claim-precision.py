#!/usr/bin/env python3
"""Advisory citation-precision worklist for normative-attribution claims (the
S3 instrument, the closed 2026-06-22-review backlog item; design decided
2026-07-03, matrix-fit pattern; catches the FR-120 class).

WHAT THIS IS (and is NOT). This is an orchestrator dev-AID, not an audit
gate. The existence gates (48/49/54/58/61 and the citation family) confirm a
cited source or control code EXISTS and is well-formed; none of them checks
CLAIM PRECISION: whether the source actually contains the supporting
language a sentence attributes to it. The motivating incident (FR-120, PR
#294): a policy attributed a fixed "180-day baseline" to NIST SP 800-53 CA-6
and ISO/IEC 27001 Clause 9.2, and neither source prescribes a fixed
interval. That class is semantic, so it is not mechanically gate-checkable
(the same conclusion the matrix-fit design reached for control-code fit);
the durable instrument is a cadenced judging skill fed by this
RECALL-ORIENTED TRIAGE tool. This tool does NOT judge a claim right or
wrong; it hands the semantic judge (the `/claim-fit` skill, PR B of this
build, and the human reading its output) a worklist, tiered by risk:

  TIER A (judge every one): value-attribution claims, a specific value
    (N days/hours/months/years) tied to a named normative source in the
    same clause, in either order ("retained ... 7 years ... under ISO/IEC
    42001"; "GDPR Article 33(1) requires ... 72 hours"). A wrong Tier-A
    claim is a factual misattribution, the exact FR-120 shape. The corpus
    population was small before the I2 recall-widening (census 2026-07-04,
    post the adoption-pass fixes: 8 Tier-A rows); the current count is below.
  TIER B (sample on cadence): soft-alignment claims ("aligns with /
    consistent with / in accordance with / compliance with / conforms
    to / as required by / as defined in / per" plus a
    named source) with no specific value. These assert alignment, not
    specific language; the census counts 53 Tier-A + 163 Tier-B rows (2026-09-02, post the I2 recall-widening, its over-match fixes, and the non-corpus-tree exclusions guardrails/ references/ .project-governance/), so the
    skill samples them rather than judging each per run.

Ground truth for the judge is the held source text in the SIBLING
grc_library_ref reference repo (buckets at its root); this tool reports,
best-effort, whether each named source FAMILY appears held (token search of
the grc_library_ref indexes), because a claim against an un-held source
cannot be judged and routes to the maintainer's source-acquisition queue instead.
The grc_library_ref checkout is optional input (as in
audit-brief-freshness.py): absent checkout means held-state reads
"unknown", never a failure.

It is named ``audit-*`` (not ``lint-*``) so the gate machinery (the
four-surface parity gate 35, the regression suite gate 36) does NOT
auto-discover it, and it is NOT wired into ``run_all_audits.sh`` /
``quality.yml`` / ``.pre-commit-config.yaml``. It always exits 0: its
output is a worklist, and a lexical extractor is deliberately
recall-oriented (a miss is worse than a spurious row the judge dismisses in
seconds). CI additionally CANNOT host this check because the ground truth
lives in the sibling private repo CI cannot see. Its self-test lives behind
``--self-test`` (inline unittest on the extractors) rather than in
``tests/`` so the gate-36 regression runner does not adopt it.

Usage:
  python3 tools/audit-claim-precision.py [--ref-base PATH] [--tier {A,B,all}]
  python3 tools/audit-claim-precision.py --self-test
"""

import argparse
import os
import re
import sys
import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories and files never scanned: working state, assistant config,
# generated artefacts (edit the source, not the artefact), and the
# CHANGELOG (it quotes claims historically; it does not assert them).
EXCLUDE_DIRS = {".git", ".working", ".claude", "node_modules", "__pycache__",
                "tests", "tools",
                # Non-corpus trees: the pack (skill/rule EXAMPLE claims), the playbooks,
                # and the project-governance working store are not corpus documents.
                "guardrails", "references", ".project-governance", ".web"}
EXCLUDE_FILES = {"CHANGELOG.md", "TODO.md", "TODO-REFERENCE.md",
                 str(Path("docs") / "portal.md"),
                 str(Path("docs") / "maturity-scorecard.md"),
                 # A pure document-index register: its review-cadence column ("6 to 12
                 # months") pairs with an adjacent frameworks-list column, a cross-cell
                 # value+source that is NOT an attribution claim (P-1.62 I2 QA, #1922).
                 str(Path("governance") / "register-document-index-and-classification.md")}

SOURCE = (
    r'(?:ISO(?:/IEC)?\s?(?:TS\s|TR\s)?[0-9]{4,5}(?:-[0-9]+)?(?::[0-9]{4})?'
    r'|ISO/IEC\s?27001(?::2022)?'
    r'|NIST\s(?:SP\s)?[0-9]{3}-[0-9A-Za-z]+(?:\sRev\.?\s?[0-9])?'
    r'|NIST\sCSF(?:\s2\.0)?'
    r'|CSA\s(?:CCM|AICM|CAIQ)(?:\sv?[0-9.]+)?'
    r'|COBIT(?:\s2019)?'
    r'|GDPR(?:\sArticle\s[0-9]+(?:\([0-9]+\))?)?'
    r'|EU\sAI\sAct(?:\sAnnex\s[IVX]+|\sArticle\s[0-9]+(?:\([0-9]+\))?)?'
    r'|PCI\sDSS(?:\sv?[0-9.]+)?'
    r'|SOC\s?2'
    r'|HIPAA(?:\sSecurity\sRule|\sPrivacy\sRule)?'
    r'|\b(?:DORA|NIS2|CPRA|CCPA|LGPD|PIPEDA|POPIA|APPI)\b'
    r'|\bPIPL\b(?:\sArticle\s[0-9]+)?'
    r'|\bFIPS\s?[0-9]{3}(?:-[0-9])?'
    r'|(?:NIST\s)?\bAI\sRMF\b'
    r'|\bSSAE\b\s?(?:No\.?\s?)?[0-9]+'
    r'|\bCIS\b(?:\s(?:Controls?|Critical(?:\sSecurity\sControls?)?|CSC|Benchmarks?)|\sv?[0-9][0-9.]*)'
    r'|\bFedRAMP\b'
    r'|ISO\s?[0-9]{4,5}(?::[0-9]{4})?'
    r')'
)
VALUE = (
    r'(?:'
    r'[0-9]+(?:\.[0-9]+)?[- ]'
    r'(?:calendar[- ]day|business[- ]day|working[- ]day|day|hour|minute|week|month|year)s?'
    r'|[0-9]+[- ](?:character|attempt|failed[- ]attempt|bit|round)s?\b'
    r'|[0-9]+(?:\.[0-9]+)?\s?(?:%|per\s?cent|percent)'
    r')'
)
ATTRIB = (r'\b(?:per|under|as\srequired\sby|as\sdefined\sin|'
          r'in\saccordance\swith|compliance\swith|consistent\swith|'
          r'align(?:s|ed)?\swith|conforms?\sto|pursuant\sto|according\sto)')
NORMVERB = r'(?:requires?|prescribes?|mandates?|sets?|specifies|stipulates?)'

# Same clause: no sentence-ending period between the parts (a period
# followed by whitespace; decimal points and "e.g." survive imperfectly,
# recall over precision).
CLAUSE = r'[^.|]{0,90}'

TIER_A_VALUE_FIRST = re.compile(
    VALUE + CLAUSE + ATTRIB + r'\s(?:the\s)?' + SOURCE, re.IGNORECASE)
TIER_A_SOURCE_FIRST = re.compile(
    SOURCE + CLAUSE + NORMVERB + CLAUSE + VALUE, re.IGNORECASE)
# The FR-120 shape: an ATTRIB leads into a source-first attribution with no
# normative verb ("Under GDPR Article 33(1), notification ... within 72 hours").
TIER_A_ATTRIB_FIRST = re.compile(
    ATTRIB + r'\s(?:the\s)?' + SOURCE + CLAUSE + VALUE, re.IGNORECASE)
TIER_B = re.compile(ATTRIB + r'\s(?:the\s)?' + SOURCE, re.IGNORECASE)

# Held-state token per source family, searched in the grc_library_ref indexes.
FAMILY_TOKENS = {
    "ISO": "ISO", "NIST": "NIST", "CSA": "CCM", "COBIT": "COBIT",
    "GDPR": "GDPR", "EU AI Act": "AI Act", "PCI": "PCI", "SOC": "SOC",
    "HIPAA": "HIPAA", "DORA": "DORA", "NIS2": "NIS2", "CPRA": "CCPA",
    "CCPA": "CCPA", "LGPD": "LGPD", "PIPEDA": "PIPEDA", "POPIA": "POPIA",
    "APPI": "APPI",
    "PIPL": "PIPL", "FIPS": "FIPS", "AI RMF": "AI RMF",
    "SSAE": "SSAE", "CIS": "CIS", "FedRAMP": "FedRAMP",
}


def find_ref_base(cli_path):
    for label, cand in (("--ref-base", cli_path),
                        ("GRC_REF_PATH", os.environ.get("GRC_REF_PATH"))):
        if cand:
            if (Path(cand) / "catalogue.yml").exists():
                return Path(cand)
            print(f"advisory: {label}={cand} has no catalogue.yml; held-state "
                  "will read unknown.")
            return None
    default = REPO_ROOT.parent / "grc_library_ref"
    return default if (default / "catalogue.yml").exists() else None


def corpus_files(docs=None):
    """Yield (rel, path) for corpus markdown. If `docs` is given (an iterable of
    repo-relative path strings), yield ONLY those files that exist and pass the
    exclusions, so a per-batch cadence can scope the worklist to the batch's docs."""
    want = None
    if docs is not None:
        want = {str(Path(d)) for d in docs}
    for p in sorted(REPO_ROOT.rglob("*.md")):
        rel = p.relative_to(REPO_ROOT)
        if rel.parts and rel.parts[0] in EXCLUDE_DIRS:
            continue
        if str(rel) in EXCLUDE_FILES or rel.name == "CHANGELOG.md":
            continue
        if want is not None and str(rel) not in want:
            continue
        yield rel, p


def extract_claims(text):
    """Return (tier, line_no, line, source) tuples for one file's text."""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        m = (TIER_A_VALUE_FIRST.search(line)
             or TIER_A_ATTRIB_FIRST.search(line)
             or TIER_A_SOURCE_FIRST.search(line))
        if m:
            out.append(("A", i, line.strip(), m.group(0)))
            continue
        # Cross-cell table row: CLAUSE excludes '|', so a value cell and a source
        # cell in DIFFERENT cells of one row are invisible to the patterns above.
        # A KPI/SLA table is a primary /claim-fit batch trigger, so surface the row.
        stripped = line.lstrip()
        if stripped.startswith("|") and stripped.count("|") >= 2:
            cells = [c.strip() for c in line.split("|")]
            if any(re.search(VALUE, c, re.IGNORECASE) for c in cells):
                sm = next((re.search(SOURCE, c, re.IGNORECASE)
                           for c in cells if re.search(SOURCE, c, re.IGNORECASE)), None)
                if sm:
                    out.append(("A", i, line.strip(), sm.group(0)))
                    continue
        b = TIER_B.search(line)
        if b:
            out.append(("B", i, line.strip(), b.group(0)))
    return out


def family_of(match_text):
    up = match_text.upper()
    for fam in ("EU AI ACT", "AI RMF", "NIST", "CSA", "COBIT", "GDPR", "PCI",
                "SOC", "HIPAA", "DORA", "NIS2", "CPRA", "CCPA", "LGPD", "PIPEDA",
                "POPIA", "APPI", "PIPL", "FIPS", "SSAE", "FEDRAMP", "CIS", "ISO"):
        if fam in up:
            if fam == "EU AI ACT":
                return "EU AI Act"
            if fam == "AI RMF":
                return "AI RMF"
            if fam == "FEDRAMP":
                return "FedRAMP"
            return fam
    return "other"


def _norm_claim(text):
    """Normalize a claim line for anchoring: lowercase, collapse whitespace, strip.
    Survives reflow/whitespace edits; a genuine reword changes the anchor (accepted
    residue, per the claim-fit SKILL step-3 note)."""
    return re.sub(r"\s+", " ", text.strip().lower())


def claim_anchor(text, length=12):
    """Stable short content anchor for a claim line (D1/D2). sha256 hex, truncated;
    line-drift-immune (NOT a line number), matching the sweep-preflight-scanner precedent."""
    return hashlib.sha256(_norm_claim(text).encode("utf-8")).hexdigest()[:length]


def source_key(src):
    """The normalized SOURCE identifier component of a row key (D3): drop the leading
    ATTRIB verb so 'per ISO/IEC 27001' and 'in accordance with ISO/IEC 27001' key the
    same source. Falls back to the whole match if no bare SOURCE is found."""
    m = re.search(SOURCE, src, re.IGNORECASE)
    return re.sub(r"\s+", " ", (m.group(0) if m else src).strip().lower())


def domain_of(rel):
    """Document domain = corpus top-level dir (D4)."""
    parts = Path(rel).parts
    return parts[0] if parts else "(root)"


def row_key(path, src, anchor):
    """Row identity for the coverage sweep: path + cited source + claim anchor."""
    return f"{path}|{source_key(src)}|{anchor}"


def build_tier_b_census(docs=None):
    """Live Tier-B census as a deterministic, key-deduped list of row dicts.
    Global (no --docs) for the coverage sweep; `docs` is accepted only for testing."""
    rows = []
    for rel, p in corpus_files(docs):
        for tier, ln, line, src in extract_claims(p.read_text(errors="replace")):
            if tier != "B":
                continue
            anchor = claim_anchor(line)
            rows.append({
                "key": row_key(str(rel), src, anchor),
                "path": str(rel), "source": src,
                "family": family_of(src), "domain": domain_of(rel),
                "anchor": anchor, "line_hint": ln,
            })
    seen = {}                       # D7: collapse identical claim lines by key, keep first
    for r in rows:
        seen.setdefault(r["key"], r)
    return sorted(seen.values(), key=lambda r: r["key"])


def load_sweep_records(path):
    """Parse the JSONL sweep ledger into a list of dicts (empty if absent)."""
    import json as _json
    out = []
    if path and Path(path).exists():
        for ln in Path(path).read_text(errors="replace").splitlines():
            ln = ln.strip()
            if ln:
                out.append(_json.loads(ln))
    return out


def current_cycle_state(records):
    """Return (cycle, judged_keys:set, runs_in_cycle:int, per_stratum_judged:dict).
    Cycle advances on each cycle-reset; judged/rotation counts are scoped to the
    CURRENT cycle only, so a reset restarts sampling on the refreshed census."""
    from collections import Counter
    cycle = 1
    for rec in records:
        if rec.get("kind") == "cycle-reset":
            cycle = max(cycle, int(rec["cycle"]) + 1)
    judged, runs, strat = set(), 0, Counter()
    for rec in records:
        if rec.get("kind") != "coverage-sweep" or rec.get("cycle") != cycle:
            continue
        runs += 1
        for s in rec.get("sampled", []):
            judged.add(s["key"])
            strat[(s["family"], s["domain"])] += 1
    return cycle, judged, runs, dict(strat)


def stratified_draw(census, judged, per_stratum_judged, n):
    """Draw the next <=n un-judged rows, stratified by (family,domain) with rotation.
    Deterministic: no seed/date/random. Returns (drawn_rows, unjudged_total).

    Rotation (D6): strata are ordered least-judged-this-cycle first (then canonical
    tuple), so under-sampled strata surface each run -> every stratum is reached over
    the cadence. Within a run we round-robin one row per stratum (spread, not cluster).
    Within a stratum, rows are taken in ascending-anchor order (without replacement)."""
    from collections import defaultdict
    unjudged = [r for r in census if r["key"] not in judged]
    buckets = defaultdict(list)
    for r in unjudged:
        buckets[(r["family"], r["domain"])].append(r)
    for k in buckets:
        buckets[k].sort(key=lambda r: r["anchor"])
    order = sorted(buckets.keys(),
                   key=lambda s: (per_stratum_judged.get(s, 0), s))
    drawn, cursor, progressed = [], {k: 0 for k in order}, True
    while len(drawn) < n and progressed:
        progressed = False
        for stratum in order:
            if len(drawn) >= n:
                break
            i = cursor[stratum]
            if i < len(buckets[stratum]):
                drawn.append(buckets[stratum][i])
                cursor[stratum] = i + 1
                progressed = True
    return drawn, len(unjudged)


def run_sample(n, record_path, date=None, as_json=False, _census=None, _records=None):
    """Tier-B coverage-sweep mode: emit the next stratified un-judged N and the JSONL
    record line(s) to append. `_census`/`_records` are test injection seams."""
    import json as _json
    records = _records if _records is not None else load_sweep_records(record_path)
    cycle, judged, runs, strat = current_cycle_state(records)
    census = _census if _census is not None else build_tier_b_census()
    census_keys = {r["key"] for r in census}
    stale = judged - census_keys        # judged rows no longer in the live census
    drawn, unjudged_total = stratified_draw(census, judged, strat, n)
    remaining_after = unjudged_total - len(drawn)
    run_no = runs + 1

    sweep_rec = None
    if drawn:
        sweep_rec = {"kind": "coverage-sweep", "cycle": cycle, "run": run_no,
                     "date": date, "census_size": len(census),
                     "n_requested": n, "n_drawn": len(drawn),
                     "remaining_after": remaining_after,
                     "sampled": [{"key": r["key"], "path": r["path"],
                                  "source": r["source"], "family": r["family"],
                                  "domain": r["domain"], "anchor": r["anchor"],
                                  "line_hint": r["line_hint"]} for r in drawn]}
    reset_rec = None
    if remaining_after == 0:             # this run completes the cycle (or already done)
        reset_rec = {"kind": "cycle-reset", "cycle": cycle, "date": date,
                     "reason": ("census exhausted; sampling restarts on the refreshed "
                                f"census as cycle {cycle + 1}")}

    if as_json:
        print(_json.dumps({
            "mode": "coverage-sweep", "cycle": cycle, "run": run_no,
            "census_size": len(census), "unjudged_before": unjudged_total,
            "n_requested": n, "n_drawn": len(drawn),
            "remaining_after": remaining_after, "cycle_complete": remaining_after == 0,
            "stale_judged_keys": sorted(stale),
            "record_path": (str(record_path) if record_path else None),
            "append_records": [r for r in (sweep_rec, reset_rec) if r],
        }, indent=2))
        return 0

    print(f"claim-fit Tier-B coverage sweep: cycle {cycle}, run {run_no} "
          f"(census {len(census)}, un-judged before {unjudged_total}, drawing "
          f"{len(drawn)} of {n}; {remaining_after} left after)")
    if record_path is None:
        print("  note: no sweep-ledger path resolved (public/adopter clone); cold start "
              "assumed. Pass --sweeps-record PATH to persist without-replacement state.")
    if stale:
        print(f"  note: {len(stale)} previously-judged key(s) no longer in the live "
              f"census (rename/reword); manual reconciliation, per SKILL residue.")
    for r in drawn:
        print(f"  [{r['family']} x {r['domain']}] {r['path']}:{r['line_hint']} "
              f"({r['anchor']})  {r['source']}")
    if remaining_after == 0:
        print(f"  CYCLE {cycle} COMPLETE -> append the cycle-reset record; next run "
              f"starts cycle {cycle + 1} on the refreshed census.")
    print("\n  append the following line(s) to the sweep ledger AFTER judging "
          "(the without-replacement basis):")
    for r in (sweep_rec, reset_rec):
        if r:
            print("    " + _json.dumps(r))
    return 0


def held_families(ref_base):
    if ref_base is None:
        return None
    idx = ""
    for name in ("INDEX.md", "catalogue.yml"):
        p = ref_base / name
        if p.exists():
            idx += p.read_text(errors="replace")
    held = set()
    for fam, token in FAMILY_TOKENS.items():
        if token.lower() in idx.lower():
            held.add(fam)
    return held


def run_report(tier_filter, ref_base, docs=None, as_json=False):
    held = held_families(ref_base)
    all_rows = []
    for rel, p in corpus_files(docs):
        for tier, ln, line, src in extract_claims(p.read_text(errors="replace")):
            all_rows.append((tier, rel, ln, line, src))
    a = [r for r in all_rows if r[0] == "A"]
    b = [r for r in all_rows if r[0] == "B"]
    if as_json:
        import json as _json
        def _row(r):
            fam = family_of(r[4])
            return {"tier": r[0], "path": str(r[1]), "line": r[2], "text": r[3],
                    "source": r[4], "family": fam,
                    "held": (None if held is None else (fam in held))}
        rows = all_rows if tier_filter == "all" else [r for r in all_rows if r[0] == tier_filter]
        print(_json.dumps({"census": {"tier_a": len(a), "tier_b": len(b)},
                           "tier_filter": tier_filter,
                           "scoped_docs": (sorted(str(Path(d)) for d in docs) if docs is not None else None),
                           "rows": [_row(r) for r in rows]}, indent=2))
        return
    print(f"claim-precision worklist: {len(a)} Tier-A value-attribution "
          f"claim(s), {len(b)} Tier-B soft-alignment claim(s) "
          f"(recall-oriented; rows are judge-candidates, not defects)"
          + (f"; showing tier {tier_filter} only" if tier_filter != "all" else ""))
    rows = all_rows if tier_filter == "all" else [
        r for r in all_rows if r[0] == tier_filter]
    if held is None:
        print("held-state: UNKNOWN (no grc_library_ref checkout with a "
              "catalogue.yml found; every source routes to the judge as unconfirmed)")
    for tier, rel, ln, line, src in rows:
        fam = family_of(src)
        state = ("held?" if held is None
                 else ("held" if fam in held else "NOT-HELD"))
        show = line if len(line) <= 200 else line[:197] + "..."
        print(f"  [{tier}] {rel}:{ln} [{fam}:{state}] {show}")
    if tier_filter == "all" and b:
        print(f"\ncadence note: judge every Tier-A row; sample Tier B "
              f"(population {len(b)}) per the /claim-fit skill's cadence.")


def self_test():
    import unittest

    class Extractors(unittest.TestCase):
        def test_tier_a_value_first(self):
            line = ("These logs are retained ... for a minimum of 7 years, "
                    "consistent with AI-system audit-log retention under "
                    "ISO/IEC 42001 and EU AI Act Annex IV")
            got = extract_claims(line)
            self.assertEqual(len(got), 1)
            self.assertEqual(got[0][0], "A")

        def test_tier_a_source_first(self):
            line = ("GDPR Article 33(1) requires notification to the "
                    "supervisory authority within 72 hours of awareness.")
            got = extract_claims(line)
            self.assertEqual(got[0][0], "A")

        def test_tier_b(self):
            line = "The control set is aligned with NIST CSF 2.0 functions."
            got = extract_claims(line)
            self.assertEqual(got[0][0], "B")

        def test_plain_prose_no_claim(self):
            line = ("The register lists retention periods for each system "
                    "class and is reviewed quarterly.")
            self.assertEqual(extract_claims(line), [])

        def test_value_without_source_not_tier_a(self):
            line = "Backups are retained for 30 days in the primary region."
            self.assertEqual(extract_claims(line), [])

        def test_guardrails_pack_is_excluded(self):
            # The pack (guardrails/) carries skill/rule EXAMPLE claims (e.g. the claim-fit
            # 7-year example), which are illustrations, NOT corpus normative-attribution
            # claims, so corpus_files must not scan them.
            for d in ("guardrails", "references", ".project-governance", ".web"):
                self.assertIn(d, EXCLUDE_DIRS)
            paths = [str(rel) for rel, _ in corpus_files()]
            self.assertFalse(
                any(p.split("/", 1)[0] in ("guardrails", "references", ".project-governance", ".web")
                    for p in paths),
                "non-corpus trees must be excluded from the corpus scan")

        def test_docs_scope_filters_corpus(self):
            # --docs scoping: corpus_files(docs=[X]) yields only X (a real corpus doc).
            target = "governance/register-data-retention-schedule.md"
            got = [str(rel) for rel, _ in corpus_files(docs=[target])]
            self.assertEqual(got, [target])
            self.assertEqual([str(rel) for rel, _ in corpus_files(docs=["nope/none.md"])], [])

        def test_json_output_is_valid_and_scoped(self):
            import io, contextlib, json as _json
            target = "governance/register-data-retention-schedule.md"
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                run_report("all", None, docs=[target], as_json=True)
            d = _json.loads(buf.getvalue())
            self.assertEqual(d["scoped_docs"], [target])
            self.assertIn("census", d)
            self.assertTrue(all(r["path"] == target for r in d["rows"]))

        def test_family_mapping(self):
            self.assertEqual(family_of("under ISO/IEC 42001"), "ISO")
            self.assertEqual(family_of("per GDPR Article 33(2)"), "GDPR")
            self.assertEqual(family_of("EU AI Act Annex IV"), "EU AI Act")

        # --- I2 recall-widening (2026-09-02): each new shape + an over-match guard ---
        def test_tier_a_attrib_first_fr120(self):
            line = "Under GDPR Article 33(1), notification is due within 72 hours of awareness."
            self.assertEqual(extract_claims(line)[0][0], "A")

        def test_tier_a_minute_and_week_values(self):
            self.assertEqual(extract_claims(
                "Sessions time out after 15 minutes, as required by PCI DSS.")[0][0], "A")
            self.assertEqual(extract_claims(
                "Scans run every 2 weeks in accordance with ISO/IEC 27001.")[0][0], "A")

        def test_tier_a_count_value(self):
            self.assertEqual(extract_claims(
                "Passwords are a minimum of 12 characters, as required by PCI DSS.")[0][0], "A")

        def test_tier_a_cross_cell_table_row(self):
            self.assertEqual(extract_claims(
                "| Regulator notification | 72 hours | GDPR Article 33(1) |")[0][0], "A")

        def test_new_sources_recognized_not_invisible(self):
            # PIPL / FIPS / NIST AI RMF were NO-MATCH before I2; now at least Tier-B.
            for line in ("Requests are handled under PIPL Article 45.",
                         "Keys use AES in accordance with FIPS 140-3.",
                         "The programme aligns with the NIST AI RMF."):
                self.assertTrue(extract_claims(line), f"source not recognized: {line}")

        def test_cis_substring_does_not_false_match(self):
            # \bCIS\b must NOT match the "cis" inside "precise" (over-match guard).
            self.assertEqual(extract_claims(
                "This requires a precise 30 day review of the register."), [])

        def test_new_family_mapping(self):
            self.assertEqual(family_of("under PIPL Article 45"), "PIPL")
            self.assertEqual(family_of("aligns with the NIST AI RMF"), "AI RMF")
            self.assertEqual(family_of("per FedRAMP"), "FedRAMP")

        # --- I2 QA (#1922) over-match fixes: count/source boundary + junk-column guards ---
        def test_count_value_needs_trailing_boundary(self):
            # 'character' must not match inside 'characteristic' (a header cell), nor
            # 'attempt' in 'attempted', 'bit' in 'bitmap', 'round' in 'roundup'.
            self.assertEqual(extract_claims(
                "| AIQT facet | NIST AI RMF 1.0 characteristic | ISO/IEC 42001 |"), [])
            self.assertNotEqual(
                (extract_claims("Lockout after 5 attempted logins per NIST SP 800-63")
                 or [("", 0, "", "")])[0][0], "A")

        def test_legacy_short_source_word_boundary(self):
            # \bAPPI\b must not match the 'appi' inside 'mapping'.
            self.assertEqual(extract_claims(
                "| MITRE ATT&CK mapping documented | 100% of rules | retire |"), [])

        def test_cis_requires_qualifier_not_url_slug(self):
            # \bCIS\b with no Controls/version qualifier (e.g. a URL slug '...-cis')
            # must not match; a real 'CIS Controls v8' claim still does.
            self.assertEqual(extract_claims(
                "| ANPD | 3-business-day | comunicado-de-incidente-de-seguranca-cis |"), [])
            self.assertEqual(extract_claims(
                "per CIS Controls v8, patch within 14 days")[0][0], "A")
            # CIS Benchmark(s) / CSC are the corpus's most common CIS forms -> recognized
            self.assertTrue(extract_claims(
                "Baselines are aligned with CIS Benchmark recommendations."))
            self.assertTrue(extract_claims("consistent with CIS CSC controls"))

        def test_pure_index_register_excluded(self):
            # The document-index/classification register is in EXCLUDE_FILES: its
            # review-cadence-vs-frameworks columns are not attribution claims.
            self.assertIn(
                str(Path("governance") / "register-document-index-and-classification.md"),
                EXCLUDE_FILES)

        # --- P-1.64 Tier-B coverage-sweep mode ---
        def _mk(self, fam, dom, i):
            path = f"{dom}/doc{i}.md"
            src = f"per {fam}"
            return {"key": f"{path}|{fam.lower()}|{i:012d}", "path": path,
                    "source": src, "family": fam, "domain": dom,
                    "anchor": f"{i:012d}", "line_hint": i}

        def test_anchor_stable_and_whitespace_immune(self):
            self.assertEqual(claim_anchor("aligns with  NIST CSF 2.0"),
                             claim_anchor("aligns with NIST CSF 2.0 "))
            self.assertEqual(len(claim_anchor("x")), 12)

        def test_source_key_drops_attrib_verb(self):
            self.assertEqual(source_key("per ISO/IEC 27001"),
                             source_key("in accordance with ISO/IEC 27001"))

        def test_sample_cold_start_stratified(self):
            census = [self._mk("ISO", "ai", i) for i in range(6)] + \
                     [self._mk("GDPR", "privacy", 100 + i) for i in range(6)]
            drawn, rem = stratified_draw(census, set(), {}, 4)
            self.assertEqual(len(drawn), 4)
            self.assertEqual(rem, 12)
            self.assertEqual(len({d["family"] for d in drawn}), 2)  # spread, not cluster

        def test_sample_without_replacement(self):
            census = [self._mk("ISO", "ai", i) for i in range(6)]
            d1, _ = stratified_draw(census, set(), {}, 3)
            judged = {r["key"] for r in d1}
            d2, _ = stratified_draw(census, judged, {("ISO", "ai"): 3}, 3)
            self.assertFalse({r["key"] for r in d2} & judged)

        def test_sample_terminal_min_n_remaining(self):
            census = [self._mk("ISO", "ai", i) for i in range(2)]
            drawn, rem = stratified_draw(census, set(), {}, 10)
            self.assertEqual(len(drawn), 2)         # min(N, remaining)
            self.assertEqual(rem, 2)

        def test_sample_rotation_across_runs_covers_all_strata(self):
            # 4 strata, N=2: run1 hits 2 strata, run2 (given run1 counts) hits the other 2.
            strata = [("ISO", "ai"), ("GDPR", "privacy"),
                      ("NIST", "security"), ("CSA", "compliance")]
            census = [self._mk(f, d, k * 10 + j)
                      for k, (f, d) in enumerate(strata) for j in range(2)]
            d1, _ = stratified_draw(census, set(), {}, 2)
            j1 = {r["key"] for r in d1}
            s1 = {(r["family"], r["domain"]) for r in d1}
            counts = {}
            for r in d1:
                counts[(r["family"], r["domain"])] = counts.get((r["family"], r["domain"]), 0) + 1
            d2, _ = stratified_draw(census, j1, counts, 2)
            s2 = {(r["family"], r["domain"]) for r in d2}
            self.assertEqual(s1 | s2, set(strata))   # every stratum reached over the cadence

        def test_cycle_state_and_reset(self):
            recs = [{"kind": "coverage-sweep", "cycle": 1, "run": 1,
                     "sampled": [{"key": "k1", "family": "ISO", "domain": "ai"}]}]
            cyc, judged, runs, strat = current_cycle_state(recs)
            self.assertEqual((cyc, runs), (1, 1))
            self.assertEqual(judged, {"k1"})
            recs.append({"kind": "cycle-reset", "cycle": 1})
            cyc2, judged2, runs2, _ = current_cycle_state(recs)
            self.assertEqual(cyc2, 2)          # cycle advanced
            self.assertEqual((judged2, runs2), (set(), 0))  # judged/rotation reset

        def test_sample_determinism(self):
            census = [self._mk("ISO", "ai", i) for i in range(5)] + \
                     [self._mk("GDPR", "privacy", 100 + i) for i in range(5)]
            a, _ = stratified_draw(census, set(), {}, 4)
            b, _ = stratified_draw(census, set(), {}, 4)
            self.assertEqual([r["key"] for r in a], [r["key"] for r in b])

        def test_sample_emits_reset_record_when_exhausted(self):
            import io, contextlib, json as _json
            census = [self._mk("ISO", "ai", i) for i in range(2)]
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                run_sample(10, None, as_json=True, _census=census, _records=[])
            out = _json.loads(buf.getvalue())
            self.assertTrue(out["cycle_complete"])
            kinds = {r["kind"] for r in out["append_records"]}
            self.assertEqual(kinds, {"coverage-sweep", "cycle-reset"})

    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(
        unittest.defaultTestLoader.loadTestsFromTestCase(Extractors))
    return 0 if result.wasSuccessful() else 1


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ref-base", help="path to the grc_library_ref checkout")
    ap.add_argument("--tier", choices=["A", "B", "all"], default="all")
    ap.add_argument("--docs", nargs="+", metavar="PATH",
                    help="scope to these repo-relative doc path(s) (the per-batch cadence)")
    ap.add_argument("--json", action="store_true", dest="as_json",
                    help="emit the worklist as JSON (for a dispatch brief or a run-over-run diff)")
    ap.add_argument("--self-test", action="store_true",
                    help="run the inline extractor self-test and exit")
    ap.add_argument("--sample", "--unjudged", action="store_true", dest="sample",
                    help="Tier-B coverage-sweep mode: emit the next stratified, "
                         "without-replacement, un-judged N (P-1.64)")
    ap.add_argument("--n", type=int, default=10, metavar="N",
                    help="coverage-sweep sample size (default 10)")
    ap.add_argument("--sweeps-record", metavar="PATH",
                    help="JSONL sweep-ledger path (default: resolve_working "
                         "claim-fit/tierb-coverage-sweeps.jsonl)")
    ap.add_argument("--date", help="date stamp written into the emitted record "
                                   "(metadata only; NOT used in the draw)")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return self_test()
    if args.sample:
        if args.docs:
            ap.error("--sample is the GLOBAL Tier-B coverage sweep; it does not take "
                     "--docs (a scoped run does not advance the coverage cycle).")
        if args.n <= 0:
            ap.error("--n must be a positive integer (the coverage sweep draws the "
                     "next N un-judged rows; N<=0 would never advance the cadence).")
        record_path = args.sweeps_record
        if record_path is None:
            try:                       # lazy: keep the default path off the module top
                import lint_common
                # Resolve the WORKING DIR (which exists) then name the ledger file, so a
                # cold start (ledger not yet created) still gets a writable first-use path;
                # resolve_working() is existence-only and returns None for a missing file.
                base = lint_common.resolve_working_dir()
                record_path = (str(Path(base) / "claim-fit" /
                                   "tierb-coverage-sweeps.jsonl") if base else None)
            except Exception:
                record_path = None
        return run_sample(args.n, record_path, date=args.date, as_json=args.as_json)
    run_report(args.tier, find_ref_base(args.ref_base), docs=args.docs,
               as_json=args.as_json)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
