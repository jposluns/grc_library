#!/usr/bin/env python3
"""Shared control-code parsing for the two advisory matrix aids
(audit-matrix-semantic-fit.py and audit-stranded-matrix-code.py).

Both aids parse CSA CCM / AICM control codes out of the compliance matrix and
related tables; they had drifted into two different CSA regexes. This module is
the single canonical source, so the two aids share one CSA shape.

Behaviour note (P-1.62 I10): the canonical CSA core below is
audit-stranded-matrix-code's shape (first char a letter; a (?<![\\w&]) lookbehind).
It was chosen over audit-matrix-semantic-fit's prior [A-Z&]{2,4}-[0-9]{2} because
it is strictly more principled (it rejects an ampersand-leading pseudo-code such
as "&DSP-05" that the \\b-anchored form could emit) while producing IDENTICAL
results on the live corpus: verified 0 divergences over 3186 semantic-fit cells
and 4528 matrix cells, and both aids' self-tests stay green. The two forms differ
only on inputs that do not occur in the corpus (a 5-char prefix, or an ampersand
adjacent to a code); all real CCM/AICM prefixes are 3 characters.
"""
from __future__ import annotations

import re
import unicodedata

# Canonical CSA CCM / AICM control-code CORE (no anchors): a 2-5 char prefix whose first character
# is a letter and remainder letters or ampersand (so A&A / I&S match), a hyphen, two ASCII digits.
# Shared by CSA_CODE_RE and by the CSA branch of CODE_RE, so both aids parse one canonical CSA
# shape. A code's own digits are [0-9], not \d: \d matches any Unicode decimal digit, so a
# document showing Arabic-Indic digits would read as carrying the ASCII code (3b117). A GUARD that
# rejects a match must not be narrowed the same way, since narrowing a rejecting guard makes it
# reject less; every code branch uses the closed guard _ASCII_END instead (3b118, below).
_NON_ASCII = r"[^\x00-\x7f]"
# Non-ASCII characters that END a token rather than continue it (3b118 QA r3): dashes, opening and
# closing brackets, and initial and final quotes (Unicode categories Pd, Ps, Pe, Pi, Pf), from
# Python's Unicode tables at import.
_END_CATEGORIES = ("Pd", "Ps", "Pe", "Pi", "Pf")
_TOKEN_END_PUNCT = "[" + "".join(re.escape(chr(c)) for c in range(0x80, 0x110000)
                                 if unicodedata.category(chr(c)) in _END_CATEGORIES) + "]"
# Non-ASCII whitespace also ends a token unless a digit, a dot or another non-ASCII character
# follows it.
_WIDE_SPACE = r"[^\S\x00-\x7f]"
_WIDE_SPACE_END = _WIDE_SPACE + r"+(?:$|(?![0-9.])[\x00-\x7f]|" + _TOKEN_END_PUNCT + ")"
# The closed guard (3b118): after a code's ASCII digit-and-dot run, a non-ASCII character stops the
# read unless it is one of the token-ending characters above.
_ASCII_END = r"(?![0-9.]*(?!" + _TOKEN_END_PUNCT + "|" + _WIDE_SPACE_END + ")" + _NON_ASCII + ")"
CSA_CODE_CORE = r"[A-Z][A-Z&]{1,4}-[0-9]{2}" + _ASCII_END

# Standalone CSA matcher (was audit-stranded-matrix-code._CSA_CODE; identical on ASCII input,
# digits narrowed to ASCII by 3b117):
# a capturing group so .findall() yields the code; a (?<![\w&]) lookbehind and a
# trailing \b so a code embedded in a word, or preceded by '&', does not match.
CSA_CODE_RE = re.compile(r"(?<![\w&])(" + CSA_CODE_CORE + r")\b")

# A contiguous CSA range: "IAM-01 to 15", "LOG-01 through LOG-14", "A&A-01 to A&A-06"
# (was audit-stranded-matrix-code._CSA_RANGE; identical on ASCII input, digits narrowed
# to ASCII by 3b117).
CSA_RANGE_RE = re.compile(
    r"(?<![\w&])([A-Z][A-Z&]{1,4})-([0-9]{1,2})" + _ASCII_END + r"\s*(?:to|through)\s*"
    r"(?:([A-Z][A-Z&]{1,4})-)?([0-9]{1,2})" + _ASCII_END + r"\b"
)

# Multi-framework code token (was audit-matrix-semantic-fit.CODE_RE): the CSA core
# above, a NIST CSF 2.0 category (GV.OC, ...), a COBIT 2019 objective/practice
# (APO12, DSS05.03), or an ISO/IEC 27001:2022 Annex A control (A.5.1, A.7.10,
# A.8.34). The CSA branch is CSA_CODE_CORE, so both aids share one canonical CSA
# shape. Verified identical (set AND order) to the prior CODE_RE on the live corpus.
# Every CSA, COBIT and ISO code branch (CSA code, both CSA range endpoints, COBIT, ISO; NIST CSF
# categories carry no digits and are unguarded) uses _ASCII_END (3b118 QA r1-r3): after the code's
# ASCII digit-and-dot run, the read continues only into ASCII, the end of the text, a token-ending
# mark (a dash, bracket or quote) or non-ASCII whitespace not followed by a digit or dot. Any
# other non-ASCII character (a digit of any kind, a letter or mark, a format character, a non-
# ASCII dot or other punctuation) means the token continues in a form this parser does not read,
# so the code is not taken from it. ASCII behaviour is unchanged, and no live corpus document has
# a CSA, COBIT or ISO code followed by a non-ASCII character (measured 2026-09-27), so live output
# is unchanged too.

CODE_RE = re.compile(
    r"\b(?:" + CSA_CODE_CORE + r"|(?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2}"
    r"|(?:EDM|APO|BAI|DSS|MEA)" + _ASCII_END + r"[0-9]{2}(?:\.[0-9]{2})?"
    r"|A\.[5-8]\.[0-9]{1,2}(?!\.?[0-9])" + _ASCII_END + r")\b"
)


def expand_codes(text: str) -> set[str]:
    """Every CSA CCM/AICM control code in ``text``, contiguous ranges expanded.

    Was audit-stranded-matrix-code._expand_codes; identical behaviour on ASCII input (3b117). A
    cross-family range ("IAM-01 to LOG-05") is not a real range and is ignored; a
    range is bounded to <100 codes as a sanity guard.
    """
    codes: set[str] = set(CSA_CODE_RE.findall(text))
    for prefix, start, end_prefix, end in CSA_RANGE_RE.findall(text):
        if end_prefix and end_prefix != prefix:  # cross-family range: not a real range
            continue
        s, e = int(start), int(end)
        if s <= e and e - s < 100:  # sane bound
            for n in range(s, e + 1):
                codes.add(f"{prefix}-{n:02d}")
    return codes


def _self_test() -> int:
    """Inline unit tests, incl. equivalence assertions against each original form."""
    import unittest

    class MatrixCodeParseTests(unittest.TestCase):
        # --- CODE_RE: multi-framework ---
        def test_code_re_csa(self):
            self.assertEqual(CODE_RE.findall("DSP-16 and A&A-02"), ["DSP-16", "A&A-02"])

        def test_code_re_csf_cobit_iso(self):
            self.assertEqual(CODE_RE.findall("GV.OC"), ["GV.OC"])
            self.assertEqual(CODE_RE.findall("APO12 DSS05.03"), ["APO12", "DSS05.03"])
            self.assertEqual(CODE_RE.findall("A.5.1 A.7.10 A.8.34"),
                             ["A.5.1", "A.7.10", "A.8.34"])

        # --- CSA_CODE_RE incl. ampersand family ---
        def test_csa_code_ampersand(self):
            self.assertEqual(CSA_CODE_RE.findall("I&S-04 near A&A-02"),
                             ["I&S-04", "A&A-02"])

        def test_csa_code_rejects_ampersand_leading(self):
            # The improvement over the prior [A-Z&]{2,4} form: no '&DSP-05'.
            self.assertEqual(CSA_CODE_RE.findall("word&DSP-05"), [])

        # --- ranges ---
        def test_range_expansion(self):
            self.assertEqual(expand_codes("IAM-01 to 15"),
                             {f"IAM-{n:02d}" for n in range(1, 16)})

        def test_range_cross_family_rejected(self):
            # A cross-family "range" expands neither side as a block; only the two
            # literal endpoints (via CSA_CODE_RE) are present.
            self.assertEqual(expand_codes("IAM-01 to LOG-05"), {"IAM-01", "LOG-05"})

        def test_range_sane_bound(self):
            # A 2-digit range is at most 01..99 (99 codes), always under the <100
            # guard, so it expands in full; AAA-50 and AAA-99 are both present.
            expanded = expand_codes("AAA-01 to 99")
            self.assertIn("AAA-50", expanded)
            self.assertIn("AAA-99", expanded)
            self.assertEqual(len(expanded), 99)

        def test_ascii_digits_only(self):
            # 3b117: Unicode digits are not code digits (\d would accept Arabic-Indic digits).
            self.assertEqual(expand_codes("STA-\u0660\u0662"), set())
            self.assertEqual(expand_codes("STA-01 to \u0660\u0663"), {"STA-01"})
            self.assertEqual(CODE_RE.findall("APO\u0661\u0662 A.5.\u0661 DSP-\u0661\u0666"), [])
            self.assertEqual(CODE_RE.findall("APO12 A.5.1 DSP-16"), ["APO12", "A.5.1", "DSP-16"])
            # every changed site, and the guards that must stay Unicode-wide (3b117 QA r1)
            self.assertEqual(expand_codes("STA-\u0660\u0661 to 03"), set())
            self.assertEqual(CODE_RE.findall("A.5.1.\u0662 A.5.1.\uff12 A.5.1.2"), [])
            self.assertEqual(CODE_RE.findall("DSS05.\u0660\u0663 APO12.\u0661\u0662"), [])
            # a guard right after the prefix sees every ASCII digit and dot, so a mixed practice or
            # a trailing non-ASCII sub-part cannot backtrack to the ASCII objective (3b117 QA r2)
            for s in ("DSS05.0\u0663", "APO12.0\uff12", "DSS05.03.\u0661",
                      "STA-APO15.1\u0663", "DSS05\u0663"):
                self.assertEqual(CODE_RE.findall(s), [], s)
            self.assertEqual(CODE_RE.findall("DSS05.03.1"), ["DSS05.03"])

        def test_guards_closed_on_the_ascii_side(self):
            # 3b118: any non-ASCII character right after a guarded code's ASCII token stops the
            # read: non-decimal digits, no-break spaces before a digit or a dot, format characters,
            # non-ASCII dots and separators, a supplementary-plane digit, and non-digit numerics.
            for s in ("DSS05.0\u00b3", "A.5.1.\u00b2", "APO12\u2460", "A.5.1\u00b9",
                      "DSS05.\u00a0\u0663", "A.5.1.\u3000\u00b2", "A.5.1\u00a0\u0662",
                      "DSS05\u00a0.\u00b3", "A.5.1\u00a0.\u00b2", "DSS05.\u200b3", "A.5.1\uff0e2",
                      "DSS05.0\U0001f100", "A.5.1\u2028.2", "APO12\u2160",
                      "A.5.1..\u00b2", "A.5.1...\u0663", "A.5.1\u0301", "DSS05\u0301",
                      "DSP-16\u200b7", "DSP-16\u0301"):
                self.assertEqual(CODE_RE.findall(s), [], ascii(s))
            # ASCII behaviour is unchanged: ASCII space still ends a token.
            # the range END is guarded too
            self.assertEqual(expand_codes("STA-01 to 03\u0301"), {"STA-01"})
            self.assertEqual(expand_codes("STA-01 to STA-03\u0301"), {"STA-01"})
            # token-ending punctuation and whitespace do not stop a read (3b118 QA r3)
            en_dash = chr(0x2013)  # built, not written, so the prose dash lint stays meaningful
            quoted = "DSP-16\u2019s \u201cDSS05.03\u201d A.5.1" + en_dash + "A.5.3"
            self.assertEqual(CODE_RE.findall(quoted),
                             ["DSP-16", "DSS05.03", "A.5.1", "A.5.3"])
            self.assertEqual(expand_codes("STA-01\u00a0"), {"STA-01"})
            self.assertEqual(CODE_RE.findall("(APO12) [A.5.1]"), ["APO12", "A.5.1"])
            # DEL is ASCII, so it does not stop a read
            self.assertEqual(CODE_RE.findall("A.5.1\x7f DSP-16\x7f"), ["A.5.1", "DSP-16"])
            self.assertEqual(expand_codes("STA-01\u200b to 03"), set())
            # a no-break space before "to" ends the start code's token; the range reads as on main
            self.assertEqual(expand_codes("STA-01\u00a0to 03"), {"STA-01", "STA-02", "STA-03"})
            self.assertEqual(expand_codes("STA-01 to 03"), {"STA-01", "STA-02", "STA-03"})
            self.assertEqual(CODE_RE.findall("DSS05. 3 A.5.1 2 A.5.1.a"),
                             ["DSS05", "A.5.1", "A.5.1"])
            self.assertEqual(CODE_RE.findall("DSS05.03 DSS05.3"), ["DSS05.03", "DSS05"])

        # --- EQUIVALENCE against each original form (the critical tests) ---
        def test_equiv_semantic_fit_CODE_RE(self):
            prior = re.compile(
                r"\b(?:[A-Z&]{2,4}-[0-9]{2}|(?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2}"
                r"|(?:EDM|APO|BAI|DSS|MEA)\d{2}(?:\.\d{2})?"
                r"|A\.[5-8]\.\d{1,2}(?!\d|\.\d))\b")
            for cell in ["DSP-16, DSP-02", "A&A-02 I&S-04", "GV.OC PR.AA",
                         "APO12 DSS05.03 BAI09", "A.5.1 A.8.34", "TVM-07, TVM-06",
                         "N/A", "", "IAM-01 to 15"]:
                self.assertEqual(CODE_RE.findall(cell), prior.findall(cell), cell)

        def test_equiv_stranded_expand(self):
            prior_code = re.compile(r"(?<![\w&])([A-Z][A-Z&]{1,4}-\d{2})\b")
            prior_range = re.compile(
                r"(?<![\w&])([A-Z][A-Z&]{1,4})-(\d{1,2})\s*(?:to|through)\s*"
                r"(?:([A-Z][A-Z&]{1,4})-)?(\d{1,2})\b")

            def prior_expand(text):
                codes = set(prior_code.findall(text))
                for p, s, ep, e in prior_range.findall(text):
                    if ep and ep != p:
                        continue
                    si, ei = int(s), int(e)
                    if si <= ei and ei - si < 100:
                        for n in range(si, ei + 1):
                            codes.add(f"{p}-{n:02d}")
                return codes

            for cell in ["STA-02", "A&A-02", "GRC-01 to GRC-03", "IAM-01 through 14",
                         "word&DSP-05", "N/A", "", "LOG-03, SEF-01"]:
                self.assertEqual(expand_codes(cell), prior_expand(cell), cell)

    suite = unittest.TestLoader().loadTestsFromTestCase(MatrixCodeParseTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    import sys
    sys.exit(_self_test())
