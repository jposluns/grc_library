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
    population is small (census 2026-07-04, post the adoption-pass fixes:
    8 rows).
  TIER B (sample on cadence): soft-alignment claims ("aligns with /
    consistent with / in accordance with / compliance with / conforms
    to / as required by / as defined in / per" plus a
    named source) with no specific value. These assert alignment, not
    specific language; the census counts 119 rows (2026-07-04), so the
    skill samples them rather than judging each per run.

Ground truth for the judge is the held source text in the SIBLING
grc_library_scratch repo's ``ref/`` base; this tool reports, best-effort,
whether each named source FAMILY appears held (token search of the scratch
indexes), because a claim against an un-held source cannot be judged and
routes to the maintainer's source-drop queue instead. The scratch checkout
is optional input (as in audit-brief-freshness.py): absent checkout means
held-state reads "unknown", never a failure.

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
  python3 tools/audit-claim-precision.py [--scratch PATH] [--tier {A,B,all}]
  python3 tools/audit-claim-precision.py --self-test
"""

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories and files never scanned: working state, assistant config,
# generated artefacts (edit the source, not the artefact), and the
# CHANGELOG (it quotes claims historically; it does not assert them).
EXCLUDE_DIRS = {".git", ".working", ".claude", "node_modules", "__pycache__",
                "tests", "tools"}
EXCLUDE_FILES = {"CHANGELOG.md", "TODO.md",
                 str(Path("docs") / "portal.md"),
                 str(Path("docs") / "maturity-scorecard.md")}

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
    r'|DORA|NIS2|CPRA|CCPA|LGPD|PIPEDA|POPIA|APPI'
    r'|ISO\s?[0-9]{4,5}(?::[0-9]{4})?'
    r')'
)
VALUE = (
    r'[0-9]+(?:\.[0-9]+)?[- ]'
    r'(?:calendar[- ]day|business[- ]day|working[- ]day|day|hour|month|year)s?'
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
TIER_B = re.compile(ATTRIB + r'\s(?:the\s)?' + SOURCE, re.IGNORECASE)

# Held-state token per source family, searched in the scratch indexes.
FAMILY_TOKENS = {
    "ISO": "ISO", "NIST": "NIST", "CSA": "CCM", "COBIT": "COBIT",
    "GDPR": "GDPR", "EU AI Act": "AI Act", "PCI": "PCI", "SOC": "SOC",
    "HIPAA": "HIPAA", "DORA": "DORA", "NIS2": "NIS2", "CPRA": "CCPA",
    "CCPA": "CCPA", "LGPD": "LGPD", "PIPEDA": "PIPEDA", "POPIA": "POPIA",
    "APPI": "APPI",
}


def find_scratch(cli_path):
    for label, cand in (("--scratch", cli_path),
                        ("GRC_SCRATCH_PATH", os.environ.get("GRC_SCRATCH_PATH"))):
        if cand:
            if (Path(cand) / "ref").is_dir():
                return Path(cand)
            print(f"advisory: {label}={cand} has no ref/ tree; held-state "
                  "will read unknown.")
            return None
    default = REPO_ROOT.parent / "grc_library_scratch"
    return default if (default / "ref").is_dir() else None


def corpus_files():
    for p in sorted(REPO_ROOT.rglob("*.md")):
        rel = p.relative_to(REPO_ROOT)
        if rel.parts and rel.parts[0] in EXCLUDE_DIRS:
            continue
        if str(rel) in EXCLUDE_FILES or rel.name == "CHANGELOG.md":
            continue
        yield rel, p


def extract_claims(text):
    """Return (tier, line_no, line, source) tuples for one file's text."""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        a1 = TIER_A_VALUE_FIRST.search(line)
        a2 = TIER_A_SOURCE_FIRST.search(line)
        if a1 or a2:
            m = a1 or a2
            out.append(("A", i, line.strip(), m.group(0)))
            continue
        b = TIER_B.search(line)
        if b:
            out.append(("B", i, line.strip(), b.group(0)))
    return out


def family_of(match_text):
    up = match_text.upper()
    for fam in ("EU AI ACT", "NIST", "CSA", "COBIT", "GDPR", "PCI", "SOC",
                "HIPAA", "DORA", "NIS2", "CPRA", "CCPA", "LGPD", "PIPEDA",
                "POPIA", "APPI", "ISO"):
        if fam in up:
            return "EU AI Act" if fam == "EU AI ACT" else fam
    return "other"


def held_families(scratch):
    if scratch is None:
        return None
    idx = ""
    for name in ("ref/INDEX.md", "ref/catalogue.yml"):
        p = scratch / name
        if p.exists():
            idx += p.read_text(errors="replace")
    held = set()
    for fam, token in FAMILY_TOKENS.items():
        if token.lower() in idx.lower():
            held.add(fam)
    return held


def run_report(tier_filter, scratch):
    held = held_families(scratch)
    all_rows = []
    for rel, p in corpus_files():
        for tier, ln, line, src in extract_claims(p.read_text(errors="replace")):
            all_rows.append((tier, rel, ln, line, src))
    a = [r for r in all_rows if r[0] == "A"]
    b = [r for r in all_rows if r[0] == "B"]
    print(f"claim-precision worklist: {len(a)} Tier-A value-attribution "
          f"claim(s), {len(b)} Tier-B soft-alignment claim(s) "
          f"(recall-oriented; rows are judge-candidates, not defects)"
          + (f"; showing tier {tier_filter} only" if tier_filter != "all" else ""))
    rows = all_rows if tier_filter == "all" else [
        r for r in all_rows if r[0] == tier_filter]
    if held is None:
        print("held-state: UNKNOWN (no scratch checkout with a ref/ tree "
              "found; every source routes to the judge as unconfirmed)")
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

        def test_family_mapping(self):
            self.assertEqual(family_of("under ISO/IEC 42001"), "ISO")
            self.assertEqual(family_of("per GDPR Article 33(2)"), "GDPR")
            self.assertEqual(family_of("EU AI Act Annex IV"), "EU AI Act")

    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(
        unittest.defaultTestLoader.loadTestsFromTestCase(Extractors))
    return 0 if result.wasSuccessful() else 1


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scratch", help="path to the grc_library_scratch checkout")
    ap.add_argument("--tier", choices=["A", "B", "all"], default="all")
    ap.add_argument("--self-test", action="store_true",
                    help="run the inline extractor self-test and exit")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return self_test()
    run_report(args.tier, find_scratch(args.scratch))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
