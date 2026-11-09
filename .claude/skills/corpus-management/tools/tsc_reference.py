"""AICPA 2017 Trust Services Criteria (TSP Section 100) criterion-identifier reference.

A citation index of the criterion IDENTIFIERS only (no criterion text, no points of
focus): the AICPA text is copyrighted and held in grc_library_ref for reference, not
redistributed. Imported by ``lint-matrix-control-codes.py`` (the central matrix's
"AICPA TSC 2017" column, gate 49) and ``verify-reference-modules.py`` (the parity aid).

Provenance: transcribed from the held copy
``frameworks/AICPA/AICPA-TSP-100-2017-Trust-Services-Criteria-revised-POF-2022-clean--full-text.md``
in grc_library_ref (2017 criteria with the March 2020 updates); each series comment
names the extract line where each criterion begins. The 2022 revision updated the
points of focus, not the criteria (the held AICPA SOC 2 guide, AAG-SOP22E, states that the
points-of-focus revisions do not alter the 2017 criteria), so the identifiers are
unchanged by it. The privacy
group headings P1.0 to P8.0 name groups of criteria and are NOT criteria.

61 criteria: CC 33 (common criteria, common to all five categories), A 3
(Availability), C 2 (Confidentiality), PI 5 (Processing Integrity), P 18 (Privacy).
"""

from __future__ import annotations

TSC_EDITION = "2017"

TSC_CATEGORIES: dict[str, str] = {
    "CC": "Common criteria (common to all five categories)",
    "A": "Availability",
    "C": "Confidentiality",
    "PI": "Processing Integrity",
    "P": "Privacy",
}

TSC_CRITERIA: frozenset[str] = frozenset((
    "CC1.1", "CC1.2", "CC1.3", "CC1.4", "CC1.5",             # 474, 520, 565, 622, 684
    "CC2.1", "CC2.2", "CC2.3",                                # 732, 763, 858
    "CC3.1", "CC3.2", "CC3.3", "CC3.4",                       # 962, 1071, 1144, 1194
    "CC4.1", "CC4.2",                                         # 1246, 1307
    "CC5.1", "CC5.2", "CC5.3",                                # 1335, 1379, 1420
    "CC6.1", "CC6.2", "CC6.3", "CC6.4",                       # 1463, 1532, 1565, 1601
    "CC6.5", "CC6.6", "CC6.7", "CC6.8",                       # 1627, 1650, 1687, 1718
    "CC7.1", "CC7.2", "CC7.3", "CC7.4", "CC7.5",             # 1761, 1804, 1842, 1892, 1984
    "CC8.1",                                                  # 2028
    "CC9.1", "CC9.2",                                         # 2135, 2166
    "A1.1", "A1.2", "A1.3",                                   # 2262, 2295, 2361
    "C1.1", "C1.2",                                           # 2386, 2408
    "PI1.1", "PI1.2", "PI1.3", "PI1.4", "PI1.5",             # 2438, 2502, 2526, 2563, 2593
    "P1.1",                                                   # 2633
    "P2.1",                                                   # 2686
    "P3.1", "P3.2",                                           # 2744, 2776
    "P4.1", "P4.2", "P4.3",                                   # 2805, 2823, 2844
    "P5.1", "P5.2",                                           # 2878, 2918
    "P6.1", "P6.2", "P6.3", "P6.4", "P6.5", "P6.6", "P6.7",   # 2953, 2994, 3011, 3029, 3060, 3085, 3107
    "P7.1",                                                   # 3139
    "P8.1",                                                   # 3161
))

# Privacy group headings (2631, 2684, 2742, 2803, 2876, 2951, 3137, 3159): not criteria.
TSC_GROUP_HEADINGS: frozenset[str] = frozenset(f"P{n}.0" for n in range(1, 9))


def is_valid_tsc_criterion(tok: str) -> bool:
    """True iff ``tok`` is one of the 61 2017 Trust Services Criteria identifiers."""
    return tok in TSC_CRITERIA


def is_tsc_group_heading(tok: str) -> bool:
    """True iff ``tok`` is a privacy group heading (P1.0 to P8.0), which is not a criterion."""
    return tok in TSC_GROUP_HEADINGS
