#!/usr/bin/env python3
"""Enumeration-parity check (grc gate): pack-owned engine (source of record).

Verify that a canonical two-category enumeration (a set of NAME tokens and a set
of PREFIX tokens, defined in a single source of truth) is faithfully re-enumerated
across every surface that restates it. The check has four categories:

- Cross-config set checks: a companion config's token set must either equal the
  canonical set exactly (``mode="equal"``, reporting both missing and extra) or be
  a subset of it (``mode="extra_only"``, reporting only tokens not in the canonical
  set). The wrapper supplies the two sets already computed; the engine only diffs.
- Name-cell surfaces: every canonical NAME token must appear, in the surface's
  anchored region, as a bounded markdown table cell ``| name |`` or a plain list
  item ``- name`` (``name_is_cell``), robust against a coincidental prose mention.
- Prefix-substring surfaces: every canonical PREFIX token must appear as a
  substring within the surface's anchored region (prefixes are distinctive).
- An anchor that cannot be located on its surface is itself a hard parity failure
  (the enumeration the check keys on is gone).

Engine/wrapper split (Group-A content-generic lane, Pattern A): this engine carries
the PURE check (``name_is_cell``, ``doctype_region``, ``collect_findings``) plus the
generic cell/item regex. It is repository-root-free (the wrapper reads the surface
files and passes their text) and carries NO project schema and NO project
vocabulary: the canonical sets, the companion-config sets, the per-surface region
anchors, and every finding-message TEMPLATE are supplied by the wrapper. The engine
emits no literal finding text of its own; it fills each wrapper-supplied template's
``{tokens}`` slot with ``str(sorted(...))`` and appends the wrapper's pre-formed
anchor-absent message verbatim, so no project schema word is ever hard-coded in an
engine message.

``collect_findings`` returns the ordered list of failure strings (empty when parity
holds); the wrapper owns the FAIL header, the per-line printing, and the summary /
OK reporting.
"""

from __future__ import annotations

import re


def name_is_cell(text: str, name: str) -> bool:
    """True if `name` appears as a bounded markdown table cell `| name |` or a
    plain list item `- name`. Both forms are robust against a coincidental
    prose mention of a common name token (Guide, Standard, Plan, ...)."""
    if re.search(r"\|\s*" + re.escape(name) + r"\s*\|", text):
        return True
    if re.search(r"^-\s+" + re.escape(name) + r"\s*$", text, re.M):
        return True
    return False


def doctype_region(text: str, anchor: tuple) -> str | None:
    """Extract a surface's enumeration region. Returns None if the anchor is absent
    (a hard parity failure: the region the check keys on is gone). For a `heading`
    anchor, the block runs from the heading line to the next heading of the same or
    shallower level. For a `phrase` anchor (a heading-less list), the single line
    containing the phrase."""
    kind, value = anchor
    if kind == "heading":
        level = len(value) - len(value.lstrip("#"))
        out: list[str] = []
        capturing = False
        for ln in text.splitlines():
            if ln.strip() == value:
                capturing = True
                continue
            if capturing:
                stripped = ln.lstrip("#")
                depth = len(ln) - len(stripped)
                if ln.startswith("#") and 1 <= depth <= level and ln[depth:depth + 1] == " ":
                    break
                out.append(ln)
        return "\n".join(out) if capturing else None
    if kind == "phrase":
        for ln in text.splitlines():
            if value in ln:
                return ln
        return None
    return None


def collect_findings(
    *,
    canonical_names: set,
    canonical_prefixes: set,
    set_checks: list[dict],
    name_surfaces: list[dict],
    prefix_surfaces: list[dict],
) -> list[str]:
    """Run the four parity categories and return the ordered failure strings.

    Each ``set_checks`` entry: ``actual`` (set), ``canonical`` (set), ``mode``
    (``"equal"`` -> report both directions, ``"extra_only"`` -> report only
    ``actual - canonical``), and the message template(s) whose ``{tokens}`` slot is
    filled with ``str(sorted(diff))``: ``missing_template`` (equal mode) and
    ``extra_template``.

    Each surface entry: ``text`` (surface content), ``anchor`` (region anchor),
    ``anchor_absent_msg`` (pre-formed string, appended verbatim when the anchor is
    absent), and ``omit_template`` (its ``{tokens}`` slot filled with the sorted
    absent list). Name surfaces test cell/item presence against ``canonical_names``;
    prefix surfaces test substring presence against ``canonical_prefixes``.
    """
    failures: list[str] = []

    for chk in set_checks:
        actual = chk["actual"]
        canonical = chk["canonical"]
        missing = canonical - actual
        extra = actual - canonical
        if chk["mode"] == "equal":
            if missing:
                failures.append(chk["missing_template"].replace("{tokens}", str(sorted(missing))))
            if extra:
                failures.append(chk["extra_template"].replace("{tokens}", str(sorted(extra))))
        elif chk["mode"] == "extra_only":
            if extra:
                failures.append(chk["extra_template"].replace("{tokens}", str(sorted(extra))))

    for surf in name_surfaces:
        region = doctype_region(surf["text"], surf["anchor"])
        if region is None:
            failures.append(surf["anchor_absent_msg"])
            continue
        absent = sorted(n for n in canonical_names if not name_is_cell(region, n))
        if absent:
            failures.append(surf["omit_template"].replace("{tokens}", str(absent)))

    for surf in prefix_surfaces:
        region = doctype_region(surf["text"], surf["anchor"])
        if region is None:
            failures.append(surf["anchor_absent_msg"])
            continue
        absent = sorted(p for p in canonical_prefixes if p not in region)
        if absent:
            failures.append(surf["omit_template"].replace("{tokens}", str(absent)))

    return failures
