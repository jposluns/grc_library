#!/usr/bin/env python3
"""Delivery-pipeline reconciliation: worker deliveries in the scratch inbox
versus the live backlog, so a "backlog applied / cleared" claim rests on the
record instead of memory.

WHY THIS EXISTS. Worker deliveries land in the SIBLING repository
``grc_library_scratch`` under ``inbox/<worker-id>/<work-unit>/`` and are applied
to this corpus one at a time under validate-then-apply. Nothing mechanical asked
"which delivered work-units map to a still-OPEN backlog item (unapplied) versus a
CLOSED one (applied)?", so the orchestrator's spoken pipeline status was
unverifiable. This tool answers that question from the record. It is the
mechanical form of the ``## Multi-session orchestration`` start-side
worker-collision check and the anti-recurrence backstop for the
delivery-status-claim discipline in ``.claude/CLAUDE.md``: any "applied / done /
backlog-clear / blocked" assertion must quote THIS tool's same-turn output, and a
per-item blocking reason is recorded per item (never generalized).

It is ADVISORY, NOT a gate. It is orchestrator-side (neither repo's CI can see the
other), so it is not wired into ``quality.yml`` / ``run_all_audits.sh`` /
``.pre-commit-config.yaml`` (wiring it would be a decorative gate, gate-discipline
rule, because the scratch checkout is not guaranteed present in every
environment). It always exits 0. When the scratch checkout is absent it says so
and exits 0 (an advisory tool must not manufacture a clean result from missing
input).

WHAT IT CLASSIFIES. For every ``inbox/<worker-id>/<work-unit>/`` directory it
extracts the backlog reference token(s) it declares (section numbers ``N.M`` and
coded ids ``FR-N`` / ``SR-N`` / ``GR-N`` from the MANIFEST text and the directory
name), then classifies against the live ``TODO.md`` open-item set:

  - PENDING   : a token matches a still-OPEN TODO item (heading section number,
                ``### SR-N`` id, or an ``(FR-N ...)`` id in a section heading).
                This is the "delivered but not yet applied / not yet closed"
                set, the one a "backlog applied" claim must reckon with.
  - APPLIED   : every extracted token maps only to items no longer open (closed
                and rotated to DONE), so the delivery has been consumed.
  - UNMAPPED  : no backlog token could be extracted; reported for manual triage
                rather than guessed (the tool never invents a status).

Each PENDING/APPLIED verdict also carries a CONFIDENCE flag (TODO §3.61). A verdict
that rests ONLY on a section-number token (``N.M``) with no stable coded id (FR/SR/GR-N)
is marked LOW-CONFIDENCE: a section number can be renumbered/recycled to a DIFFERENT
current item than the delivery intended (the 2026-07-16 gr-gap ``3.15``->MITRE-ATLAS and
etsi ``3.16``->CHANGELOG mis-maps), so such a map is flagged for manual verification
against the live TODO heading rather than trusted. A coded-id match is high-confidence.

A PENDING or UNMAPPED delivery is NOT proof of un-applied work by itself (a
research-only scoping delivery legitimately leaves its item open pending a
maintainer-scheduled build), and a per-item disposition still lives in the scratch
``research/COVERAGE.md`` verdicts; this tool surfaces the set to reconcile, it
does not adjudicate each. It never claims "applied" for a PENDING/UNMAPPED row.

Known cosmetic limit: a directory batch-label that happens to read like a coded id
(e.g. ``gr345`` for a GR-P3/4/5 batch) can synthesize a display-only token
(``GR-345``) that maps to no real backlog id. This never affects the bucket
(classification uses the manifest's real section/coded tokens); it is display noise
only, and is left rather than tightened because the same hyphen-less pattern
legitimately matches real ids like ``sr3`` -> ``SR-3``.

USAGE
  python3 tools/audit-delivery-status.py [--scratch PATH]
      Full reconciliation: every inbox delivery grouped PENDING / APPLIED /
      UNMAPPED, headlining the PENDING + UNMAPPED review set with a count.
  python3 tools/audit-delivery-status.py --item <ref> [--scratch PATH]
      Start-side worker-collision check for one backlog item (a section number
      like ``3.13`` or a coded id like ``FR-60`` / ``SR-3``): prints DELIVERED at
      each matching inbox path (apply-work) for an open item, or a build-work
      clear. The clear is CONSERVATIVE: it is only a clean "BUILD-work" when no
      UNMAPPED delivery exists (an UNMAPPED delivery, manifest without a header
      backlog id, is invisible to token matching, so clearing while one exists
      could repeat the TODO-3.13 false-clear); otherwise it refuses to clear and
      points at the full report's UNMAPPED bucket. Run and PASTE this before
      building any backlog item.
  python3 tools/audit-delivery-status.py --self-test
      Inline parser self-test.

The scratch checkout is located by ``--scratch``, else ``GRC_SCRATCH_PATH``, else
the sibling directory ``../grc_library_scratch`` relative to this repository root.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# A section number qualified by TODO / § (e.g. "TODO 3.13", "TODO section 2.2",
# "TODO §5.1", "grc_library TODO §5.9", or a bare "§5.9"); the optional "P" is the
# positional-token form. Requiring the TODO/§ qualifier avoids matching version
# numbers or other dotted figures in a manifest.
SECTION_TOKEN_RE = re.compile(
    r'(?:TODO\s+(?:section\s+)?|§)\s*P?(\d+\.\d+)', re.I)
# Coded backlog ids, tolerant of the hyphen-less directory-name form ("fr-60",
# "sr3"); the trailing boundary stops "GR-P2" (a P-suffixed id, out of scope here)
# from matching as "GR" + nothing.
CODED_TOKEN_RE = re.compile(r'\b(FR|SR|GR)-?(\d+)\b', re.I)

# Live open-item anchors in TODO.md.
OPEN_SECTION_RE = re.compile(r'^### (\d+\.\d+)\b', re.M)
OPEN_SR_RE = re.compile(r'^### (SR-\d+)\b', re.M)
OPEN_FR_IN_HEADING_RE = re.compile(r'^### \d+\.\d+[^\n(]*\((FR-\d+)', re.M)


def find_scratch(cli_path):
    """Resolve the scratch checkout, or None. An EXPLICITLY named path
    (--scratch / GRC_SCRATCH_PATH) that does not resolve is reported and NOT
    silently replaced by the sibling default (an explicit wrong path is a
    mistake to surface, not to paper over)."""
    for label, cand in (("--scratch", cli_path),
                        ("GRC_SCRATCH_PATH", os.environ.get("GRC_SCRATCH_PATH"))):
        if cand:
            if Path(cand).is_dir() and (Path(cand) / "inbox").is_dir():
                return Path(cand)
            print(f"advisory: {label}={cand} is not a scratch checkout with an "
                  "inbox/ tree; nothing to report.")
            sys.exit(0)
    default = REPO_ROOT.parent / "grc_library_scratch"
    if default.is_dir() and (default / "inbox").is_dir():
        return default
    return None


def open_refs():
    """The set of live OPEN backlog tokens in TODO.md: section numbers, SR ids,
    and FR ids named in section headings. Tokens are upper-cased for matching."""
    todo = (REPO_ROOT / "TODO.md").read_text(errors="replace")
    refs = set(OPEN_SECTION_RE.findall(todo))
    refs |= {s.upper() for s in OPEN_SR_RE.findall(todo)}
    refs |= {f.upper() for f in OPEN_FR_IN_HEADING_RE.findall(todo)}
    return refs


def _header_region(manifest_text, dirname):
    """The delivery's OWN-item declaration region: the directory name, the first
    ``# `` title line, and any ``**Work-unit:**`` / ``**Backlog item:**`` line.
    Restricting to these avoids a false match on a sibling id cross-referenced in
    the manifest BODY (e.g. a cumulative claims-ledger note "fr-59, fr-60, ...")."""
    region = [dirname]
    for ln in manifest_text.splitlines():
        if (ln.lstrip().startswith("# ")
                or "**Work-unit:**" in ln or "**Backlog item:**" in ln):
            region.append(ln)
    return "\n".join(region)


def delivery_tokens(manifest_text, dirname):
    """Backlog reference tokens a delivery declares for its OWN item (from its
    header region and directory name): section numbers ``N.M`` and coded ids
    ``XX-N`` (upper)."""
    blob = _header_region(manifest_text, dirname)
    tokens = set(SECTION_TOKEN_RE.findall(blob))
    for kind, num in CODED_TOKEN_RE.findall(blob):
        tokens.add(f"{kind.upper()}-{num}")
    return tokens


def deliveries(scratch):
    """Yield (worker_id, work_unit, rel_path, tokens) for each inbox delivery
    directory (a work-unit dir holding a MANIFEST.md)."""
    inbox = scratch / "inbox"
    for manifest in sorted(inbox.glob("*/*/MANIFEST.md")):
        d = manifest.parent
        text = manifest.read_text(errors="replace")
        rel = d.relative_to(scratch).as_posix()
        yield d.parent.name, d.name, rel, delivery_tokens(text, d.name)


def _is_coded(token):
    """True if the token is a STABLE coded backlog id (FR-N / SR-N / GR-N), which is
    never recycled, as opposed to a section number (N.M), which CAN be renumbered/
    recycled to a different item (TODO §3.61)."""
    return bool(CODED_TOKEN_RE.fullmatch(token.replace(" ", "")))


def classify(tokens, live_open):
    """Returns (bucket, low_confidence). PENDING if any token maps to an open item;
    UNMAPPED if no token; else APPLIED (every token maps only to closed items).

    `low_confidence` is True when the classification rests ONLY on a recyclable
    section-number token (N.M) with no stable coded id (FR/SR/GR-N) confirming it: a
    renumbered/recycled section token can map to a DIFFERENT current item than the
    delivery intended (the 2026-07-16 gr-gap `3.15`->MITRE-ATLAS and etsi `3.16`
    ->CHANGELOG mis-maps), so such a map is flagged for manual verification against the
    current heading rather than trusted (TODO §3.61). A coded-id match is always
    high-confidence."""
    if not tokens:
        return ("UNMAPPED", False)
    coded = {t for t in tokens if _is_coded(t)}
    if tokens & live_open:
        matched_via_coded = bool((tokens & live_open) & coded)
        return ("PENDING", not matched_via_coded)
    # APPLIED (no token maps to an open item). Low-confidence when it rests only on
    # section tokens: a recycled section number could belong to an open item under its
    # NEW meaning, so an all-section APPLIED verdict is not fully trustworthy either.
    return ("APPLIED", not coded)


def run_report(scratch):
    live = open_refs()
    buckets = {"PENDING": [], "APPLIED": [], "UNMAPPED": []}
    low_conf_count = 0
    for _worker, _unit, rel, tokens in deliveries(scratch):
        bucket, low_conf = classify(tokens, live)
        shown = ", ".join(sorted(tokens)) if tokens else "(no backlog token found)"
        if low_conf:
            low_conf_count += 1
            shown += " [LOW-CONFIDENCE: section-token only, no stable coded id; a " \
                     "renumbered/recycled section number may map to the wrong current " \
                     "item, verify against the live TODO heading]"
        buckets[bucket].append((rel, shown))

    total = sum(len(v) for v in buckets.values())
    print(f"delivery-pipeline reconciliation: {total} inbox delivery(ies); "
          f"{len(buckets['PENDING'])} PENDING (map to an open TODO item), "
          f"{len(buckets['APPLIED'])} APPLIED (map only to closed items), "
          f"{len(buckets['UNMAPPED'])} UNMAPPED (no token; triage manually)"
          + (f"; {low_conf_count} LOW-CONFIDENCE (section-token-only map, verify)"
             if low_conf_count else "") + ".")
    for name in ("PENDING", "UNMAPPED", "APPLIED"):
        rows = buckets[name]
        if not rows:
            continue
        print(f"\n{name} ({len(rows)}):")
        for rel, shown in rows:
            print(f"  - {rel}  [{shown}]")
    review = len(buckets["PENDING"]) + len(buckets["UNMAPPED"])
    if review:
        print(f"\nreview set: {review} delivery(ies) map to an open or unknown "
              "backlog item. A 'backlog applied / cleared' claim must reconcile "
              "each (applied / needs-authoring / genuinely gated / "
              "maintainer-schedule-gated); do NOT generalize one blocking reason "
              "across items.")
    else:
        print("\nall inbox deliveries map to closed backlog items.")


def run_item(scratch, ref):
    """Start-side worker-collision check for one backlog item. Distinguishes an
    OPEN target (the start-side use case: build-vs-apply) from a target that is
    not a current open TODO item (already closed/applied, or a stale id), so a
    delivery for a closed item is not mis-labelled fresh apply-work."""
    ref_u = ref.upper()
    # Normalize a coded ref like "fr-60" / "sr3" to the token form "FR-60".
    m = CODED_TOKEN_RE.fullmatch(ref_u.replace(" ", ""))
    norm = f"{m.group(1)}-{m.group(2)}" if m else ref_u
    is_open = norm in open_refs() or ref in open_refs()
    matches = []
    unmapped = []
    for _w, _u, rel, tokens in deliveries(scratch):
        if norm in tokens or ref in tokens:
            matches.append(rel)
        elif not tokens:
            unmapped.append(rel)
    if matches and is_open:
        print(f"DELIVERED for {ref} (an OPEN backlog item): APPLY-work "
              "(validate-then-apply on the delivery), NOT a from-scratch build. "
              "Delivery path(s):")
        for rel in matches:
            print(f"  - {rel}")
        return
    if matches:
        print(f"DELIVERED for {ref}, but {ref} is NOT a current open TODO item "
              "(already closed/applied, or a stale id): the delivery is already "
              "consumed, not fresh apply-work; confirm before acting. Path(s):")
        for rel in matches:
            print(f"  - {rel}")
        return
    # No token-matched delivery. A "build-work" clear is only SAFE when no
    # UNMAPPED delivery could hide this item: an UNMAPPED delivery (manifest with
    # no header backlog id, e.g. dora/nis2) is invisible to token matching, so
    # clearing to build-work while any exists would repeat the false-clear that
    # caused the TODO 3.13 collision. Refuse to clear; point at the full report.
    if unmapped:
        print(f"no TOKEN-matched delivery for {ref}, BUT {len(unmapped)} inbox "
              "delivery(ies) are UNMAPPED (manifests declaring no backlog id in "
              "the header), so this is NOT a clean build-clear. Run "
              "`python3 tools/audit-delivery-status.py` and scan the UNMAPPED "
              "bucket for this item's work before building. UNMAPPED path(s):")
        for rel in unmapped:
            print(f"  - {rel}")
    elif is_open:
        print(f"no delivery found for {ref} (an open backlog item) and no UNMAPPED "
              "deliveries: BUILD-work (no worker collision). (Also confirm "
              "claims-ledger.md and research/COVERAGE.md before building.)")
    else:
        print(f"no delivery found for {ref}, and {ref} is not a current open "
              "TODO item: check the id (it may be closed, stale, or mistyped).")


def self_test():
    import unittest

    class Parsers(unittest.TestCase):
        def test_section_tokens(self):
            self.assertEqual(
                sorted(SECTION_TOKEN_RE.findall(
                    "grc_library TODO 3.13 (positional-backlog-token lint)")),
                ["3.13"])
            self.assertEqual(
                sorted(SECTION_TOKEN_RE.findall(
                    "TODO section 2.2; FR-60 HIPAA")),
                ["2.2"])
            self.assertEqual(
                sorted(SECTION_TOKEN_RE.findall("grc_library TODO §5.1 / §5.9")),
                ["5.1", "5.9"])

        def test_coded_tokens(self):
            # Own-item tokens come from the header region (title / Work-unit /
            # Backlog-item line) plus the directory name.
            self.assertEqual(
                delivery_tokens(
                    "- **Work-unit:** fr-60-hipaa (TODO section 2.2; FR-60 HIPAA)",
                    "fr-60-hipaa-deepening"),
                {"2.2", "FR-60"})
            self.assertEqual(
                delivery_tokens("**Backlog item:** grc_library TODO 3.13",
                                "positional-token-lint-313"),
                {"3.13"})
            self.assertEqual(
                delivery_tokens("no header markers", "sr3-ref-binary-scan-build"),
                {"SR-3"})

        def test_body_cross_reference_excluded(self):
            # A sibling id in the BODY (a cumulative claims-ledger note) must NOT
            # be attributed to this delivery (the fr-15/fr-99 false-match bug).
            text = ("- **Work-unit:** fr-15-maturity-ladder (TODO section 2.5)\n"
                    "- claims-ledger cumulative for the session "
                    "(fr-59, fr-60, fr-99)\n")
            tokens = delivery_tokens(text, "fr-15-maturity-ladder-methodology")
            self.assertEqual(tokens, {"2.5", "FR-15"})
            self.assertNotIn("FR-60", tokens)

        def test_classify(self):
            live = {"2.2", "FR-60", "3.13", "SR-1"}
            # classify returns (bucket, low_confidence); a stable coded id (FR/SR/GR-N)
            # confirming the match is high-confidence, a section-token-only map is low.
            self.assertEqual(classify({"2.2", "FR-60"}, live), ("PENDING", False))
            self.assertEqual(classify({"2.4", "FR-99"}, live), ("APPLIED", False))
            self.assertEqual(classify(set(), live), ("UNMAPPED", False))
            # section-token-only PENDING -> low-confidence (the token could be recycled):
            self.assertEqual(classify({"3.13"}, live), ("PENDING", True))
            self.assertEqual(classify({"2.2"}, live), ("PENDING", True))
            # section-token-only APPLIED -> low-confidence (a renumbered token might now
            # belong to an open item under its NEW meaning):
            self.assertEqual(classify({"2.4"}, live), ("APPLIED", True))
            # a coded id maps APPLIED with high confidence even alongside a section token:
            self.assertEqual(classify({"2.4", "GR-99"}, live), ("APPLIED", False))

        def test_open_ref_regexes(self):
            todo = ("### 2.2 HIPAA operational deepening (FR-60, H, L)\n"
                    "### SR-1 last_checked currency mechanism is inert (item 26)\n"
                    "### 5.1 AI jurisdiction annexes (FR-62, M, S)\n")
            self.assertEqual(set(OPEN_SECTION_RE.findall(todo)), {"2.2", "5.1"})
            self.assertEqual(set(OPEN_SR_RE.findall(todo)), {"SR-1"})
            self.assertEqual(set(OPEN_FR_IN_HEADING_RE.findall(todo)),
                             {"FR-60", "FR-62"})

    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(
        unittest.defaultTestLoader.loadTestsFromTestCase(Parsers))
    return 0 if result.wasSuccessful() else 1


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scratch", help="path to the grc_library_scratch checkout")
    ap.add_argument("--item", help="start-side collision check for one backlog "
                    "item (e.g. 3.13, FR-60, SR-3)")
    ap.add_argument("--self-test", action="store_true",
                    help="run the inline parser self-test and exit")
    args = ap.parse_args(argv[1:])

    if args.self_test:
        return self_test()

    scratch = find_scratch(args.scratch)
    if scratch is None:
        print("advisory: no scratch checkout found (no --scratch or "
              "GRC_SCRATCH_PATH given, and no sibling grc_library_scratch "
              "directory with an inbox/ tree); nothing to report.")
        return 0

    if args.item:
        run_item(scratch, args.item)
    else:
        run_report(scratch)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
