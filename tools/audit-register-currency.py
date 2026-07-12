#!/usr/bin/env python3
"""Advisory cross-repo currency-drift report for the canonical-citations register
(shipped PR #817; delivery spec: grc_library_scratch
``inbox/worker-20260709-fable/currency-ledger-sync/sync-tool-spec.md``).

WHAT THIS IS (and is NOT). This is an orchestrator dev-AID, not an audit gate.
It reports drift between the ``grc_library_ref`` currency ledger (the
``catalogue.yml`` per-item currency fields, the source of truth for held
editions and last-checked dates) and this repo's consumer surface, the
register [`governance/register-canonical-citations.md`]. Neither repository's
CI can see the other, so no CI gate can check cross-repo currency; the check is
orchestrator-side by design (the same pattern as
``tools/audit-brief-freshness.py`` and ``tools/audit-delivery-status.py``).

It is named ``audit-*`` (not ``lint-*``) so the gate machinery (the four-surface
parity gate, the regression suite gate) does NOT auto-discover it, and it is NOT
wired into ``run_all_audits.sh`` / ``quality.yml`` / ``.pre-commit-config.yaml``.
It exits 0 by default: its findings are reconciliation candidates for the
orchestrator, never workflow failures. Making it a blocking gate would be a
decorative gate (gate-discipline rule) because the ``grc_library_ref`` checkout
is not guaranteed present in every environment; when the ledger is absent the
tool says so and exits 0 (an advisory tool must not manufacture a failure out of
its own optional input). A ``--strict`` flag exits non-zero when the two
substantive checks (register-behind, version-disagreement) fire, for a
deliberate local orchestrator run that wants a non-zero signal; it is never
wired into CI. Its self-test lives behind ``--self-test`` (inline unittest on
the parsers and the normalization) rather than in ``tests/`` so the regression
runner does not adopt it as a gated test.

The ledger is the superset (everything held); the register is a citation-scoped
subset. The tool reports on the intersection (register rows whose designation
matches a held ledger item) and lists non-intersecting register rows as
informational (expected: the corpus cites sources that are not held), never as
errors.

Checks (all advisory):
  1. Register behind on verification: the register's ``Last verified`` date is
     older than the ledger item's ``last_checked``.
  2. Version disagreement: the register's ``Current version`` does not agree
     with the ledger item's ``checked_edition``.
  3. Upstream URL mismatch (informational): the register's ``Upstream check
     location`` differs from the ledger ``upstream_url``.
  4. Ledger item held-stale (informational): the ledger ``checked_edition``
     itself signals a superseded/held-stale state, so the register should not
     inherit it.
  5. Unmatched register rows (informational): register rows with no held
     ledger counterpart.

Usage:
  python3 tools/audit-register-currency.py [--ledger PATH] [--register PATH]
                                           [--strict] [--self-test]

The ledger is located by ``--ledger``, else the ``GRC_REF_PATH`` environment
variable (pointing at the ``grc_library_ref`` root or the catalogue directly),
else the sibling ``../grc_library_ref/catalogue.yml`` relative to this repo root.

Exit codes:
    0   advisory report produced (or ledger absent, skip note), default mode
    0   default mode always, regardless of findings
    2   --strict mode AND check 1 or 2 fired
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTER = REPO_ROOT / "governance" / "register-canonical-citations.md"

# A held-stale signal in a ledger checked_edition free-text value.
HELD_STALE_RE = re.compile(
    r"\b(supersed|superseded|stale|withdrawn|replaced by|obsolet)", re.IGNORECASE
)
# A trailing edition year on a designation, ":2022" or " 2022" or "-2022".
EDITION_TAIL_RE = re.compile(r"[:\-\s]\(?(19|20)\d{2}[a-z]?\)?$")
# A trailing parenthetical clause, "(Web Application Security Risks)".
PAREN_TAIL_RE = re.compile(r"\s*\([^()]*\)\s*$")
DATE_RE = re.compile(r"(19|20)\d{2}-\d{2}-\d{2}")


def normalize_designation(text: str) -> str:
    """Reduce a Standard ID or a catalogue title to a comparable designation stem.

    Takes the part before the first comma (the catalogue title puts the
    designation first, then a descriptive clause), strips a trailing edition
    year, uppercases, and collapses whitespace. Register Standard IDs are
    already stems; this is idempotent on them.
    """
    stem = text.split(",", 1)[0].strip()
    # Strip a trailing parenthetical and a trailing edition year, repeatedly, so
    # "OWASP Top 10:2025 (Web Application Security Risks)" reduces to "OWASP Top 10"
    # (the paren guards the year from the end-anchor) and "ISO/IEC 27001:2022"
    # reduces to "ISO/IEC 27001".
    prev = None
    while prev != stem:
        prev = stem
        stem = PAREN_TAIL_RE.sub("", stem).strip()
        stem = EDITION_TAIL_RE.sub("", stem).strip()
    stem = re.sub(r"\s+", " ", stem).upper()
    return stem


def parse_ledger(text: str) -> list[dict]:
    """Parse the generated catalogue.yml (2-space-indent, ``  - title:`` items)
    into a list of item dicts, without PyYAML (stdlib-only toolchain).

    Each item starts at a ``  - title:`` line; its fields are the following
    ``    key: value`` lines until the next item or a top-level bucket header.
    Only the fields the currency check needs are extracted.
    """
    items: list[dict] = []
    cur: dict | None = None
    field_re = re.compile(r"^    ([a-z_]+):\s*(.*)$")
    title_re = re.compile(r"^  - title:\s*(.*)$")
    bucket_re = re.compile(r"^[a-z_]+:\s*$")
    for raw in text.splitlines():
        m = title_re.match(raw)
        if m:
            if cur is not None:
                items.append(cur)
            cur = {"title": _unquote(m.group(1))}
            continue
        if bucket_re.match(raw):
            # top-level bucket header ends the current item
            if cur is not None:
                items.append(cur)
                cur = None
            continue
        if cur is not None:
            fm = field_re.match(raw)
            if fm:
                cur[fm.group(1)] = _unquote(fm.group(2))
    if cur is not None:
        items.append(cur)
    return items


def _unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        return v[1:-1]
    return v


def parse_register(text: str) -> list[dict]:
    """Parse the register table rows into dicts keyed by the seven columns.

    Only rows with the expected seven pipe-delimited cells are taken; the header
    and the GFM delimiter row are skipped.
    """
    rows: list[dict] = []
    cols = [
        "standard_id", "current_version", "publication_date", "topic",
        "superseded", "upstream", "last_verified",
    ]
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 7:
            continue
        if cells[0] in ("Standard ID", "") or set(cells[0]) <= set("-: "):
            continue  # header or delimiter
        rows.append(dict(zip(cols, cells)))
    return rows


def _date_in(s: str) -> str | None:
    m = DATE_RE.search(s or "")
    return m.group(0) if m else None


_REV_RE = re.compile(r"\brev\.?\s*(\d+)", re.IGNORECASE)
_YEAR_RE = re.compile(r"\b(?:19|20)\d{2}[a-z]?\b")


def _edition_token(s: str) -> str | None:
    """Extract a comparable edition token from a version/edition free-text cell.

    Prefers a 4-digit year (the dominant edition form); falls back to a
    ``Rev N`` token. Returns None when neither is present, so the version-
    disagreement check only fires on a clear token-vs-token difference.
    """
    if not s:
        return None
    m = _YEAR_RE.search(s)
    if m:
        return m.group(0).lower()
    r = _REV_RE.search(s)
    if r:
        return "rev" + r.group(1)
    return None


def build_report(ledger_items: list[dict], reg_rows: list[dict]) -> dict:
    """Run the five checks; return a structured findings dict."""
    # Index ledger items by normalized designation. Keep the full list too so a
    # register stem can be matched as a word-boundary prefix of a longer ledger
    # title (register "WCO SAFE" vs ledger "WCO SAFE Framework").
    by_key: dict[str, dict] = {}
    keyed: list[tuple[str, dict]] = []
    for it in ledger_items:
        key = normalize_designation(it.get("title", ""))
        if not key:
            continue
        keyed.append((key, it))
        if key not in by_key:
            by_key[key] = it

    def match(reg_key: str) -> dict | None:
        exact = by_key.get(reg_key)
        if exact is not None:
            return exact
        # Word-boundary prefix: the register stem is the leading designation of a
        # longer ledger title. The trailing space guards against "ISO 27001"
        # spuriously matching "ISO 27001-1". Among several prefix matches (a
        # designation with a base edition, a draft, and a variant all share the
        # stem), prefer the SHORTEST ledger key, which is the base standard
        # rather than a verbose draft/overlay title.
        prefix = reg_key + " "
        cands = [(lk, it) for lk, it in keyed if lk.startswith(prefix)]
        if not cands:
            return None
        return min(cands, key=lambda t: len(t[0]))[1]

    behind, version, url, held_stale, unmatched = [], [], [], [], []
    matched = 0
    for row in reg_rows:
        key = normalize_designation(row["standard_id"])
        item = match(key)
        if item is None:
            unmatched.append(row["standard_id"])
            continue
        matched += 1
        # 1. register behind on verification
        rv, lc = _date_in(row["last_verified"]), _date_in(item.get("last_checked", ""))
        if rv and lc and rv < lc:
            behind.append((row["standard_id"], rv, lc))
        # 2. version disagreement, compared on an extracted edition token (a
        # year or a "Rev N"), so free-text differences ("2025" vs "2025
        # (launched 2 December 2025)") do not false-flag. Only a clear
        # token-vs-token disagreement is surfaced.
        ce = item.get("checked_edition", "")
        cv = row["current_version"]
        tv, te = _edition_token(cv), _edition_token(ce)
        if tv and te and tv != te:
            version.append((row["standard_id"], cv, ce))
        # 3. upstream URL mismatch
        ru, lu = row["upstream"], item.get("upstream_url", "")
        if ru and lu and ru != lu:
            url.append((row["standard_id"], ru, lu))
        # 4. ledger held-stale
        if HELD_STALE_RE.search(ce):
            held_stale.append((row["standard_id"], ce))
    return {
        "matched": matched, "behind": behind, "version": version,
        "url": url, "held_stale": held_stale, "unmatched": unmatched,
    }


def print_report(rep: dict) -> None:
    print("Register-currency drift report (advisory; grc_library_ref ledger vs "
          "governance/register-canonical-citations.md)")
    print(f"  matched register rows: {rep['matched']}; "
          f"unmatched (not held, informational): {len(rep['unmatched'])}")
    print("")

    def group(name, items, fmt):
        print(f"[{name}] {len(items)} finding(s)")
        for it in items:
            print(f"  - {fmt(it)}")
        print("")

    group("1 register-behind-on-verification (advisory)", rep["behind"],
          lambda t: f"{t[0]}: register verified {t[1]}, ledger checked {t[2]} "
                    f"(refresh the register row from the ledger)")
    group("2 version-disagreement (advisory)", rep["version"],
          lambda t: f"{t[0]}: register '{t[1]}' vs ledger checked_edition '{t[2]}' "
                    f"(reconcile toward the more recently verified side)")
    group("3 upstream-url-mismatch (informational)", rep["url"],
          lambda t: f"{t[0]}: register '{t[1]}' vs ledger '{t[2]}'")
    group("4 ledger-held-stale (informational)", rep["held_stale"],
          lambda t: f"{t[0]}: ledger checked_edition signals stale: '{t[1]}'")
    print(f"[5 unmatched-register-rows (informational, not held)] "
          f"{len(rep['unmatched'])} row(s)")
    for sid in rep["unmatched"]:
        print(f"  - {sid}")


def resolve_ledger(arg: str | None) -> Path | None:
    if arg:
        p = Path(arg)
    elif os.environ.get("GRC_REF_PATH"):
        p = Path(os.environ["GRC_REF_PATH"])
    else:
        p = REPO_ROOT.parent / "grc_library_ref" / "catalogue.yml"
    if p.is_dir():
        p = p / "catalogue.yml"
    return p if p.is_file() else None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Advisory register-currency drift report.")
    ap.add_argument("--ledger", help="path to grc_library_ref catalogue.yml (or its dir)")
    ap.add_argument("--register", default=str(DEFAULT_REGISTER),
                    help="path to the canonical-citations register")
    ap.add_argument("--strict", action="store_true",
                    help="exit 2 if check 1 or 2 fires (never wired into CI)")
    ap.add_argument("--self-test", action="store_true", help="run inline unit tests")
    args = ap.parse_args(argv)

    if args.self_test:
        return _run_self_test()

    ledger = resolve_ledger(args.ledger)
    if ledger is None:
        print("SKIP: grc_library_ref catalogue.yml not found "
              "(pass --ledger, set GRC_REF_PATH, or check out the sibling repo). "
              "Advisory tool; exiting 0.")
        return 0
    reg_path = Path(args.register)
    if not reg_path.is_file():
        print(f"SKIP: register not found at {reg_path}. Advisory tool; exiting 0.")
        return 0

    rep = build_report(parse_ledger(ledger.read_text(encoding="utf-8")),
                       parse_register(reg_path.read_text(encoding="utf-8")))
    print_report(rep)
    if args.strict and (rep["behind"] or rep["version"]):
        return 2
    return 0


# ----------------------------------------------------------------------
# Inline self-test (not in tests/, so the regression runner does not adopt it).
# ----------------------------------------------------------------------
class _SelfTest(unittest.TestCase):
    LEDGER = (
        "standards:\n"
        '  - title: "ISO/IEC 27001:2022, Information security management systems"\n'
        "    origin: \"ISO\"\n"
        '    last_checked: "2026-07-10"\n'
        '    checked_edition: "2022"\n'
        '    upstream_url: "https://www.iso.org/standard/27001"\n'
        '  - title: "WCO SAFE Framework"\n'
        '    last_checked: "2026-07-01"\n'
        '    checked_edition: "2021 (superseded by the 2025 edition)"\n'
        "legislation:\n"
        '  - title: "Some Act"\n'
        '    last_checked: "2026-07-05"\n'
    )
    REGISTER = (
        "| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
        "| ISO/IEC 27001 | 2022 | 2022-10 | ISMS | 2013 | https://www.iso.org/standard/27001 | verified 2026-07-09 |\n"
        "| WCO SAFE | 2021 | 2021 | Trade security | | https://wcoomd.org | verified 2026-07-01 |\n"
        "| NIST SP 800-53 | Rev. 5 | 2020 | Controls | | https://csrc.nist.gov | verified 2026-07-08 |\n"
    )

    def test_normalize(self):
        self.assertEqual(normalize_designation("ISO/IEC 27001:2022, Information security"),
                         "ISO/IEC 27001")
        self.assertEqual(normalize_designation("ISO/IEC 27001"), "ISO/IEC 27001")
        self.assertEqual(normalize_designation("NIST SP 800-53 Rev. 5"),
                         "NIST SP 800-53 REV. 5")
        # A designation with a mid-string edition year followed by a trailing
        # parenthetical (the OWASP Top 10 flagship shape) reduces to the stem,
        # so it matches the register's "OWASP Top 10" exactly (not the longer
        # "OWASP Top 10 Proactive Controls" sibling).
        self.assertEqual(
            normalize_designation("OWASP Top 10:2025 (Web Application Security Risks)"),
            "OWASP TOP 10")

    def test_parse_ledger(self):
        items = parse_ledger(self.LEDGER)
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0]["checked_edition"], "2022")
        self.assertEqual(items[2]["title"], "Some Act")

    def test_parse_register(self):
        rows = parse_register(self.REGISTER)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["standard_id"], "ISO/IEC 27001")
        self.assertEqual(rows[0]["current_version"], "2022")

    def test_report(self):
        rep = build_report(parse_ledger(self.LEDGER), parse_register(self.REGISTER))
        self.assertEqual(rep["matched"], 2)  # ISO 27001 + WCO SAFE (prefix); NIST unmatched
        self.assertIn("NIST SP 800-53", rep["unmatched"])
        # ISO 27001: register verified 2026-07-09 < ledger checked 2026-07-10 -> behind
        self.assertTrue(any(t[0] == "ISO/IEC 27001" for t in rep["behind"]))
        # WCO SAFE: checked_edition signals superseded -> held_stale
        self.assertTrue(any(t[0] == "WCO SAFE" for t in rep["held_stale"]))

    def test_edition_token(self):
        self.assertEqual(_edition_token("2022"), "2022")
        self.assertEqual(_edition_token("2025 (launched 2 December 2025)"), "2025")
        self.assertEqual(_edition_token("Rev. 5"), "rev5")
        self.assertIsNone(_edition_token("National AI Plan"))
        # same-year cells do not disagree (the Australia false-positive class)
        self.assertEqual(_edition_token("2025 (launched 2 December 2025)"),
                         _edition_token("National AI Plan 2025"))

    def test_shortest_prefix_match(self):
        # "NIST SP 800-53" prefix-matches a verbose draft AND the base Rev 5;
        # the shorter (base) key must win.
        led = ('standards:\n'
               '  - title: "NIST SP 800-53 Control Overlays for Securing AI Systems (COSAiS), draft"\n'
               '    checked_edition: "draft concept paper"\n'
               '  - title: "NIST SP 800-53 Rev 5"\n'
               '    checked_edition: "Rev 5"\n')
        reg = ("| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |\n"
               "| --- | --- | --- | --- | --- | --- | --- |\n"
               "| NIST SP 800-53 | Rev. 5 | 2020 | Controls | | u | verified 2026-07-08 |\n")
        rep = build_report(parse_ledger(led), parse_register(reg))
        self.assertEqual(rep["matched"], 1)
        # Matched to Rev 5 (shorter), so no version disagreement (rev5 == rev5).
        self.assertEqual(rep["version"], [])

    def test_strict_exit(self):
        # A ledger/register that produces a version disagreement -> strict exit 2.
        led = ('standards:\n  - title: "X Standard"\n    checked_edition: "2025"\n')
        reg = ("| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |\n"
               "| --- | --- | --- | --- | --- | --- | --- |\n"
               "| X Standard | 2019 | 2019 | t | | u | verified 2026-01-01 |\n")
        rep = build_report(parse_ledger(led), parse_register(reg))
        self.assertTrue(rep["version"])


def _run_self_test() -> int:
    suite = unittest.TestLoader().loadTestsFromTestCase(_SelfTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
