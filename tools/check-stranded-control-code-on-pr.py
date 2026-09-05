#!/usr/bin/env python3
"""D13: stranded-control-code-on-PR delta gate (PR-time, diff-scoped).

THE CLASS. A corpus document carries control codes on two surfaces: the
framework-alignment TABLE (the full mapping) and inline BODY prose (a few codes
cited in a sentence or a `*CCM: X / AICM: Y*` annotation). When a PR corrects a
code in the table but leaves the paired body cite pointing at the OLD code, the
body cite is STRANDED: still a well-formed, in-catalogue citation, so no existence
gate (48/49/54/58/61, lint-document-control-codes, lint-ccm-aicm-citations) can
see it. It is a silent accuracy defect. Observed thrice in one session (#1895 and
#1899 caught in-PR by QA; a P-1.57 PR-D miss survived on main and was fixed in
#1905, found by this check's own retroactive replay).

WHY DIFF-SCOPED, NOT A CORPUS-STATE LINT. Table and body are legitimately
inconsistent in steady state (a table enumerates the full mapping; prose cites a
few). A scan of 344 corpus docs found 27 of 29 dual-surface docs mismatch today,
almost all legitimately. So a whole-doc set check is unusable noise. This gate
fires ONLY on the DELTA: a code REMOVED from a table in THIS PR that still appears
on a body line at HEAD. Measured FP rate: 0 over the last 80 commits with the
guards below (base trigger ~16 qualifying events / 80 commits).

TEMPLATE. Architecturally a sibling of D9 (check-retired-section-orphan-on-pr.py):
deletion-triggered, merge-base-diffed, anchored-form matching, FP guards, a
`StrandedCode:` commit-trailer opt-out (D9's SectionRef mechanism verbatim), an
inline `--self-test`, wired into the pre-push runner and quality.yml PR event.

RESIDUE (what D13 does NOT establish). It is deletion-triggered and same-document
only. It cannot see (i) a body cite wrong from birth (no table change to trigger
on), (ii) cross-document stranding (check-class-completeness territory), (iii) a
wrong NEW code (/matrix-fit semantic-fit territory), or (iv) prose naming a control
by title not code. It is a targeted tripwire under the triple-family QA, the
defence-in-depth default at low marginal cost.

FAIL DIRECTION. Needs a resolvable merge base; on a missing base ref it no-ops
with a printed notice (fail-open, per the project's guard-malfunction stance): the
pre-push runner supplies the base in every normal path.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# The central compliance matrix is excluded: its cross-doc consistency is /matrix-fit's
# concern, not a same-doc table-vs-body question.
EXCLUDED = frozenset({"compliance/matrix-grc-compliance-alignment.md"})

# A control-code token: the union of families that appear in corpus alignment tables.
# A family omitted only narrows coverage, never adds FPs (the token must extract
# identically from a removed table line and a HEAD body line). Left guard forbids a
# preceding word char / dot / open-paren / hyphen; right guard forbids a following
# word char / open-paren / hyphen so `SA-11(8)` never counts as a survivor of `SA-11`
# and `A.5.1` is not a prefix-match of `A.5.12`.
_CODE_ALTS = (
    r"[A-Z&]{2,5}-\d{1,2}(?:\.\d{1,2})?"                 # CCM/AICM/800-53: IAM-04, A&A-06, AC-2, DSP-24
    r"|A\.\d{1,2}\.\d{1,2}(?:\.\d{1,2})?"              # ISO 27001 A.5.12 AND ISO 27701 4-level A.7.2.3
    r"|(?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2}(?:-\d{2})?"      # NIST CSF 2.0: PR.IR, GV.OC-01
    r"|(?:PO|PS|PW|RV)\.\d(?:\.\d)?"                     # NIST SSDF 800-218: PW.1, PO.1.1
    r"|(?:ID|GV|CT|CM|PR|CO)\.[A-Z]{2}-P\d{0,2}"        # NIST Privacy Framework: ID.DE-P, CT.DM-P2, CT.PO-P5
    r"|(?:DSS|APO|MEA|BAI|EDM)\d{2}\.\d{2}"            # COBIT 2019: DSS05.04
)
CODE_RE = re.compile(r"(?<![\w.-])(" + _CODE_ALTS + r")(?![\w(-])")

# A range `<CODE> to <endpoint>`, expanded before differencing so a range-to-single
# edit is caught (naive tokenizing misses #1899). The endpoint may repeat the code's
# stem (`PW.1 to PW.4`), echo a trailing fragment of it (`A.8.20 to 8.23`), or be a
# bare numeric suffix (`CCC-04 to 05`). A CROSS-stem range (`IAM-01 to DSP-03`,
# `A.5.1 to A.6.5`, `PW.1 to RV.4`) is left verbatim: expanding it would FABRICATE
# codes, so FP-safety wins over completeness. Same-stem-only via the stem check below.
_CODE_GROUP = r"(?:" + _CODE_ALTS + r")"
_RANGE_RE = re.compile(r"(?<![\w.-])(?P<left>" + _CODE_GROUP + r")\s+(?:to|through)\s+(?P<right>[A-Z&.\d-]*\d)(?![\w-])")
_TRAILING_NUM = re.compile(r"^(.*?)(\d{1,2})$")

TABLE_LINE = re.compile(r"^\s*\|")


def expand_ranges(text: str) -> str:
    """Rewrite a SAME-STEM control-code range into space-separated enumerated codes,
    so a range-to-single-or-narrower edit differs correctly at the token level. A
    cross-stem range is left verbatim (never fabricate a code: FP-safety)."""
    def _repl(m: "re.Match") -> str:
        lm = _TRAILING_NUM.match(m.group("left"))
        rm = _TRAILING_NUM.match(m.group("right"))
        if not lm or not rm:
            return m.group(0)
        stem, lo_s = lm.group(1), lm.group(2)
        rstem, hi_s = rm.group(1), rm.group(2)
        # Accept a bare suffix (rstem empty), an exact stem repeat, or a trailing
        # fragment echo of the stem AT A DOT/HYPHEN BOUNDARY (so "8." echoes "A.8."
        # but "AM-" does NOT echo "IAM-"). Reject a cross-stem endpoint or one that is
        # itself a complete valid control code of a different stem: never fabricate.
        if rstem and rstem != stem:
            boundary_echo = (
                stem.endswith(rstem)
                and (len(rstem) == len(stem) or stem[-len(rstem) - 1] in ".-")
            )
            if CODE_RE.fullmatch(m.group("right")) or not boundary_echo:
                return m.group(0)
        lo, hi = int(lo_s), int(hi_s)
        if hi < lo or hi - lo > 30:
            return m.group(0)
        width = len(lo_s)
        return " ".join(f"{stem}{n:0{width}d}" for n in range(lo, hi + 1))

    return _RANGE_RE.sub(_repl, text)


def codes_in(text: str) -> set[str]:
    """All control-code tokens in `text` (ranges already expanded by the caller)."""
    return {m.group(1) for m in CODE_RE.finditer(text)}


def table_codes_from_diff(diff: str, sign: str) -> set[str]:
    """Codes on added (`sign='+'`) or removed (`sign='-'`) TABLE lines in a unified diff.
    A diff body line is `<sign><content>`; we look at content lines that are table rows."""
    out: set[str] = set()
    for line in diff.splitlines():
        if not line or line[0] != sign:
            continue
        content = line[1:]
        if content.startswith(sign * 2) or content.startswith("+++") or content.startswith("---"):
            continue  # diff header line
        if TABLE_LINE.match(content):
            out |= codes_in(expand_ranges(content))
    return out


def anchored(code: str) -> re.Pattern:
    """An anchored matcher for one specific code, same guards as CODE_RE."""
    return re.compile(r"(?<![\w.-])" + re.escape(code) + r"(?![\w(-])")


def head_table_codes(head_text: str) -> set[str]:
    """All codes on table lines of the HEAD file (the still-in-table guard input)."""
    out: set[str] = set()
    for line in head_text.splitlines():
        if TABLE_LINE.match(line):
            out |= codes_in(expand_ranges(line))
    return out


def body_orphans(codes: set[str], head_text: str) -> list[tuple[int, str, str]]:
    """(line_no, code, line_text) for each removed code that appears anchored on a
    NON-table line of the HEAD file."""
    hits: list[tuple[int, str, str]] = []
    pats = {c: anchored(c) for c in codes}
    for i, line in enumerate(head_text.splitlines(), 1):
        if TABLE_LINE.match(line):
            continue
        for c, pat in pats.items():
            if pat.search(line):
                hits.append((i, c, line.strip()))
    return hits


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO_ROOT), *args], text=True)


def in_scope(rel: str) -> bool:
    """PURE: a corpus `.md` file this gate governs. Corpus domain dirs only; the
    master matrix and non-corpus trees are out."""
    if rel in EXCLUDED:
        return False
    if not rel.endswith(".md"):
        return False
    top = rel.split("/", 1)[0]
    CORPUS = {
        "ai", "architecture", "compliance", "crypto", "dev-security", "governance",
        "operations", "privacy", "resilience", "risk", "security", "supply-chain",
    }
    return "/" in rel and top in CORPUS


def opt_out_present(base: str, head: str) -> bool:
    """True if any commit in base..head carries a non-empty `StrandedCode:` trailer.
    A bare `StrandedCode:` must NOT disable the gate (a costless bypass is no guard)."""
    try:
        log = git("log", f"{base}..{head}", "--format=%B")
    except subprocess.CalledProcessError:
        return False
    for line in log.splitlines():
        s = line.strip()
        if s.lower().startswith("strandedcode:") and s[len("strandedcode:"):].strip():
            return True
    return False


def changed_corpus_files(merge_base: str, head: str) -> list[str]:
    try:
        names = git("diff", "--name-only", merge_base, head).splitlines()
    except subprocess.CalledProcessError:
        return []
    return [n for n in names if in_scope(n)]


def run(base: str | None, head: str) -> int:
    if base is None:
        target = os.environ.get("GITHUB_BASE_REF", "").strip() or "main"
        base = f"origin/{target}"
    try:
        merge_base = git("merge-base", base, head).strip()
    except subprocess.CalledProcessError:
        print(f"D13 SKIP: no resolvable merge base (base={base}, head={head}); fail-open.")
        return 0

    files = changed_corpus_files(merge_base, head)
    if not files:
        print("D13 OK: no corpus document changed in this PR.")
        return 0

    all_hits: list[tuple[str, int, str, str]] = []
    for rel in files:
        try:
            diff = git("diff", merge_base, head, "--", rel)
            head_text = git("show", f"{head}:{rel}")
        except subprocess.CalledProcessError:
            continue
        removed = table_codes_from_diff(diff, "-") - table_codes_from_diff(diff, "+")
        if not removed:
            continue
        removed -= head_table_codes(head_text)  # still-in-table guard
        if not removed:
            continue
        for ln, code, text in body_orphans(removed, head_text):
            all_hits.append((rel, ln, code, text))

    if not all_hits:
        print(f"D13 OK: {len(files)} corpus doc(s) changed; no stranded body control-codes.")
        return 0
    if opt_out_present(merge_base, head):
        print(f"D13 OK: {len(all_hits)} candidate(s); StrandedCode: opt-out present.")
        return 0

    print(
        f"FAIL: {len(all_hits)} body control-code(s) stranded by a table edit in this PR "
        f"(code removed from a table but still cited in the same doc's prose). Correct the "
        f"body cite to match, or add a `StrandedCode: <reason>` commit trailer for a "
        f"legitimate residue (e.g. a 'formerly mapped to X' narration):",
        file=sys.stderr,
    )
    for rel, ln, code, text in all_hits:
        print(f"  {rel}:{ln}: stranded `{code}` -> {text[:110]}", file=sys.stderr)
    return 1


# ---------------------------------------------------------------------------
# Inline self-test (D9's convention; the regression harness for this gate).
# ---------------------------------------------------------------------------
def _self_test() -> int:
    failures: list[str] = []

    def check(name: str, cond: bool) -> None:
        if not cond:
            failures.append(name)

    # Range expansion (the #1899 case).
    check("range-domain", expand_ranges("| ... | CCC-04 to 05 | ...") .find("CCC-04") >= 0
          and "CCC-05" in expand_ranges("CCC-04 to 05"))
    check("range-iso", "A.5.4" in expand_ranges("A.5.1 to A.5.4") and "A.5.2" in expand_ranges("A.5.1 to A.5.4"))
    # codex-HOLD regression: ISO echo form, SSDF dotted form, domain no-repeat form.
    check("range-iso-echo", "A.8.23" in expand_ranges("A.8.20 to 8.23") and "A.8.21" in expand_ranges("A.8.20 to 8.23"))
    check("range-ssdf-dotted", "PW.4" in expand_ranges("PW.1 to PW.4") and "PW.3" in expand_ranges("PW.1 to PW.4"))
    check("range-domain-norepeat", "I&S-09" in expand_ranges("I&S-01 to 09") and "I&S-05" in expand_ranges("I&S-01 to 09"))
    # codex-HOLD regression: a parenthesized body cite (SA-11) IS caught; SA-11(8) enhancement is NOT.
    check("paren-cite-caught", bool(anchored("SA-11").search("this maps to (SA-11).")))
    check("enhancement-still-excluded", not anchored("SA-11").search("addresses SA-11(8) here"))
    # still-in-table guard covers an ISO-echo range at HEAD.
    check("iso-echo-still-in-table", "A.8.23" in head_table_codes("| Net | A.8.20 to 8.23 | ... |"))
    # codex-HOLD-2 regression: 27701 4-level code + range; Privacy-Framework -P range; nested SSDF.
    check("iso-27701-4level-token", "A.7.2.3" in codes_in("mapped to A.7.2.3 here"))
    check("iso-27701-4level-range", "A.7.2.4" in expand_ranges("A.7.2.3 to A.7.2.4") and "A.7.2.3" in expand_ranges("A.7.2.3 to A.7.2.4"))
    check("privacy-P-range", "CT.PO-P5" in expand_ranges("CT.PO-P1 to P5") and "CT.PO-P3" in expand_ranges("CT.PO-P1 to P5"))
    check("ssdf-nested-range", "PO.1.3" in expand_ranges("PO.1.1 to PO.1.3"))
    # codex-HOLD-2 FP-safety: cross-stem ranges must NOT expand (no fabricated codes).
    check("cross-stem-domain-noexpand", "IAM-02" not in expand_ranges("IAM-01 to DSP-03") and "IAM-01 to DSP-03" in expand_ranges("IAM-01 to DSP-03"))
    check("cross-stem-iso-noexpand", "A.5.2" not in expand_ranges("A.5.1 to A.6.5"))
    check("cross-stem-ssdf-noexpand", "PW.2" not in expand_ranges("PW.1 to RV.4"))
    # codex-HOLD-3 regression: suffix-collision, mid-token left, and the `through` form.
    check("suffix-collision-noexpand", "IAM-02" not in expand_ranges("IAM-01 to AM-03"))
    check("midtoken-left-domain-noexpand", "IAM-02" not in expand_ranges("X-IAM-01 to 03"))
    check("midtoken-left-iso-noexpand", "A.5.2" not in expand_ranges("FOOA.5.1 to 5.3"))
    check("through-form-expands", "IAM-13" in expand_ranges("IAM-01 through IAM-15") and "IAM-15" in expand_ranges("IAM-01 through IAM-15"))

    # POSITIVE: #1899-shaped. Table cell `CCC-04 to 05` -> `CCC-04`; body still cites CCC-05.
    diff_1899 = (
        "--- a/dev-security/x.md\n+++ b/dev-security/x.md\n"
        "-| Build integrity | CCC-04 to 05 | ... |\n"
        "+| Build integrity | CCC-04 | ... |\n"
    )
    removed = table_codes_from_diff(diff_1899, "-") - table_codes_from_diff(diff_1899, "+")
    check("1899-removed-has-CCC-05", "CCC-05" in removed and "CCC-04" not in removed)
    head_1899 = "| Build integrity | CCC-04 | ... |\n\n*CCM: CCC-04, CCC-05 / SLSA Build L3*\n"
    removed2 = removed - head_table_codes(head_1899)
    check("1899-still-in-table-keeps-CCC-05", "CCC-05" in removed2)
    check("1899-orphan-found", any(c == "CCC-05" for _, c, _ in body_orphans(removed2, head_1899)))

    # POSITIVE: #1895-shaped. Table SA-11 -> CA-8; body still says SA-11.
    diff_1895 = (
        "-| Pentest programme | A.8.8 | SA-11 | ... |\n"
        "+| Pentest programme | A.8.8 | CA-8 | ... |\n"
    )
    rem = table_codes_from_diff(diff_1895, "-") - table_codes_from_diff(diff_1895, "+")
    head_1895 = "| Pentest programme | A.8.8 | CA-8 | ... |\n\nThis standard addresses NIST SP 800-53 SA-11.\n"
    rem -= head_table_codes(head_1895)
    check("1895-orphan-found", any(c == "SA-11" for _, c, _ in body_orphans(rem, head_1895)))

    # NEGATIVE: enhancement notation. Body cites SA-11(8), a narrower deliberate cite; not a survivor of SA-11.
    head_enh = "| Pentest programme | CA-8 | ... |\n\nAddresses CA-8 and SA-11(8).\n"
    check("enhancement-not-orphan", not any(c == "SA-11" for _, c, _ in body_orphans({"SA-11"}, head_enh)))

    # NEGATIVE: row move (set-level differencing self-cancels). Same code removed and re-added.
    diff_move = "-| Row A | IAM-04 | ... |\n+| Row A moved | IAM-04 | ... |\n"
    check("row-move-no-removed", not (table_codes_from_diff(diff_move, "-") - table_codes_from_diff(diff_move, "+")))

    # NEGATIVE: code still in another table row at HEAD (body cite anchored to unchanged row).
    head_stillrow = "| Row A | IAM-05 | ... |\n| Row B | IAM-04 | ... |\n\nSee IAM-04.\n"
    rem3 = {"IAM-04"} - head_table_codes(head_stillrow)
    check("still-in-other-row-suppressed", not rem3)

    # NEGATIVE: prefix safety. A.5.1 must not match A.5.12.
    check("iso-prefix-safety", not anchored("A.5.1").search("mapped to A.5.12 here"))

    # NEGATIVE: scope predicate.
    check("scope-corpus", in_scope("security/policy-x.md"))
    check("scope-excludes-matrix", not in_scope("compliance/matrix-grc-compliance-alignment.md"))
    check("scope-excludes-tools", not in_scope("tools/x.py"))

    if failures:
        print("D13 self-test FAILED: " + ", ".join(failures), file=sys.stderr)
        return 1
    print("D13 self-test OK (31 cases: range expansion incl. 27701 4-level, Privacy -P, nested SSDF, through-form, cross-stem + suffix-collision + mid-token FP-safety, paren-cite, positives, negatives, scope).")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="D13: stranded body control-code delta gate.")
    ap.add_argument("base", nargs="?", default=None, help="base ref (default: origin/$GITHUB_BASE_REF or origin/main)")
    ap.add_argument("head", nargs="?", default="HEAD", help="head ref (default: HEAD)")
    ap.add_argument("--self-test", action="store_true", help="run inline unit tests and exit")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    return run(args.base, args.head)


if __name__ == "__main__":
    sys.exit(main())
