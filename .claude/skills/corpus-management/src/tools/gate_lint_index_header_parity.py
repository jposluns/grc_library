#!/usr/bin/env python3
"""Index-header parity check (grc gate): pack-owned engine (source of record).

Verify that a corpus's document-index register mirrors, per active document, that
document's own metadata Owner and Review Frequency (the go-forward source of
truth). For every active-index row the check resolves the row's Repository-Path
link to the document, reads its metadata header, and compares:

- Review Frequency: the index cell's BASE cadence token set (every recognized
  cadence except the ``EVENT`` trigger marker) must equal the header's base
  cadence token set. ``EVENT`` is a trigger modifier, so "Annual and upon
  material change" agrees with index "Annual". A per-document allow-list of
  legitimate multi-cadence shapes is honoured; a purely-event-driven side agrees
  only with another purely-event-driven side; a base-vs-event-only shape
  mismatch, and an unrecognizable cadence on either side, are findings
  (fail-closed, per the guard-inputs discipline).
- Owner: the index Owner-Role cell vs the header Owner value (``.strip()`` then
  byte equality). Under ``strict_owner`` a mismatch is a finding; otherwise it is
  a ``WARNING:``-prefixed advisory the wrapper reports without failing.
- Title (third comparator, OFF unless ``col_title`` is supplied): the index Title
  cell vs the header title field (``.strip()`` then byte equality), ratcheted
  against a caller-supplied baseline of exact (index title, header title, class,
  rationale) pairs keyed by document path. An empty title on either side, a NEW
  difference, a pinned pair that CHANGED, and a stale entry whose titles now agree
  are findings; an unchanged pinned pair passes, and one whose class is in
  ``title_worklist_classes`` is returned as a ``DRIFT:``-prefixed work item.

Engine/wrapper split (Group-A content-generic lane, Pattern A): this engine
carries the PURE check (``cadence_tokens``, ``find_index_table``, ``check_row``,
``collect_findings``) plus the GENERIC review-cadence recognizer vocabulary
(``CADENCE_PHRASES`` / ``CADENCE_EVENT_RE``) and the code-span-link regex. It is
repository-root-free (``collect_findings`` takes ``repo_root``) and carries no
project register schema: the index relative path, the 8-column header schema, the
column indices, the metadata field names, the per-document base-cadence
allow-list, and the title field, baseline and class names are supplied by the
wrapper. The linked-document read stays in the engine (an ``OSError`` or a
``UnicodeError`` there is a per-row finding, not an environmental exit), while the
register-missing / register-unreadable environmental error paths stay in the
wrapper (Pattern-A precedent: standards-currency, gate 6).

``collect_findings`` returns ``(findings, warnings, rows_checked, title_worklist)``,
or ``None`` when the index table's header row is not found (the wrapper turns that
into the environmental exit). ``title_worklist`` is empty unless the title
comparator is enabled.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import (
        METADATA_FIELD_RE, METADATA_HEAD_LINES, parse_metadata_block, split_row, is_separator_row,
    )
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_index_header_parity: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# Code-span-link shape (identical to the structure engine, gate 4): [`display`](target).
LINK_TARGET_RE = re.compile(r"\[`([^`]+)`\]\(([^)]+)\)")

# Generic review-cadence recognizer: longest-phrase-first, case-insensitive,
# CONSUMING, and leading-word-boundary anchored (each phrase is blanked before
# shorter phrases are tried). Word-boundary anchoring stops a naive substring
# collision ("triannual" matching "annual", "bimonthly" matching "monthly"); the
# leading \b with no trailing anchor still lets "annual" match "annually".
# Ordered list of (phrase, token); scanned in this order. This is a
# domain-neutral cadence lexicon (an adopter may override it via the
# cadence_phrases / cadence_event_re parameters); the retention engine keeps its
# generic period lexicon in the engine the same way.
CADENCE_PHRASES = [
    ("6 to 12 months", "SIX_TO_TWELVE"),
    ("semi-annual", "SEMIANNUAL"),
    ("semi annual", "SEMIANNUAL"),
    ("bi-annual", "SEMIANNUAL"),
    ("bi-annually", "SEMIANNUAL"),
    ("biannual", "SEMIANNUAL"),
    ("6 months", "SEMIANNUAL"),
    ("biennial", "BIENNIAL"),
    ("24 months", "BIENNIAL"),
    ("annual", "ANNUAL"),  # leading-boundary match also covers "annually"
    ("yearly", "ANNUAL"),
    ("12 months", "ANNUAL"),
    ("quarterly", "QUARTERLY"),
    ("3 months", "QUARTERLY"),
    ("monthly", "MONTHLY"),
    ("weekly", "WEEKLY"),
    ("daily", "DAILY"),
    ("continuous", "CONTINUOUS"),
]
# Event-driven / on-demand cadence, matched after the fixed phrases. Hyphen and
# space variants are both accepted ("as needed" / "as-needed").
CADENCE_EVENT_RE = re.compile(
    r"upon|as[ -]required|as[ -]needed|following|on material change|"
    r"at every material change|event[ -]driven|updated",
    re.IGNORECASE,
)


def cadence_tokens(
    value: str,
    cadence_phrases: list[tuple[str, str]] = CADENCE_PHRASES,
    cadence_event_re: re.Pattern = CADENCE_EVENT_RE,
) -> set[str]:
    """Tokenize a cadence string (longest-phrase-first, word-boundary, consuming)."""
    work = value.lower()
    tokens: set[str] = set()
    for phrase, token in cadence_phrases:
        pat = re.compile(r"\b" + re.escape(phrase))
        if pat.search(work):
            tokens.add(token)
            work = pat.sub(" ", work)
    if cadence_event_re.search(work):
        tokens.add("EVENT")
    return tokens


def find_index_table(
    lines: list[str], header_cells: list[str]
) -> tuple[int, list[tuple[int, str]]] | None:
    """Return (start_lineno, data_rows) for the active index table, or None.

    ``start_lineno`` is 1-based, the line of the header row. ``data_rows`` is a
    list of (lineno, raw_line) for each data row (separator excluded). A blank
    line WITHIN the table is tolerated (skipped, not treated as the table's end),
    so an accidental blank row cannot silently truncate the scan; the table ends
    only at the first non-blank line that is not a pipe row.
    """
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        if split_row(line) == header_cells:
            data: list[tuple[int, str]] = []
            for j in range(i + 1, len(lines)):
                row = lines[j]
                if not row.strip():
                    continue  # tolerate a blank line inside the table
                if not row.lstrip().startswith("|"):
                    break  # first non-blank prose/heading line ends the table
                cells = split_row(row)
                if is_separator_row(cells):
                    continue
                data.append((j + 1, row))
            return (i + 1, data)
    return None


def check_row(
    cells: list[str],
    header_fields: dict[str, str],
    strict_owner: bool,
    *,
    col_path: int,
    col_owner: int,
    col_freq: int,
    owner_field: str,
    freq_field: str,
    base_cadence_allowlist: dict[str, tuple[frozenset[str], frozenset[str], str]],
    link_target_re: re.Pattern = LINK_TARGET_RE,
    cadence_phrases: list[tuple[str, str]] = CADENCE_PHRASES,
    cadence_event_re: re.Pattern = CADENCE_EVENT_RE,
    col_title: int | None = None,
    title_field: str | None = None,
    title_baseline: dict[str, tuple[str, str, str, str]] | None = None,
    title_worklist_classes: frozenset[str] = frozenset(),
) -> list[str]:
    """Return per-row findings (owner/cadence, plus title when ``col_title`` is set).

    Warnings are prefixed 'WARNING:' and title work items 'DRIFT:'. Without
    ``col_title`` the result is exactly the owner/cadence result.
    """
    findings: list[str] = []

    # Review Frequency: exact base-cadence-set agreement (EVENT is a trigger
    # modifier, not a base cadence).
    idx_freq = cells[col_freq]
    hdr_freq = header_fields.get(freq_field, "")
    idx_tok = cadence_tokens(idx_freq, cadence_phrases, cadence_event_re)
    hdr_tok = cadence_tokens(hdr_freq, cadence_phrases, cadence_event_re)
    if not idx_tok and not hdr_tok:
        findings.append(
            f"no recognized cadence token in index cell ({idx_freq!r}) or header ({hdr_freq!r})"
        )
    elif not idx_tok:
        findings.append(f"no recognized cadence token in index cell ({idx_freq!r})")
    elif not hdr_tok:
        findings.append(f"no recognized cadence token in header {freq_field} ({hdr_freq!r})")
    else:
        idx_base = idx_tok - {"EVENT"}
        hdr_base = hdr_tok - {"EVENT"}
        if idx_base and hdr_base:
            path_match = link_target_re.search(cells[col_path])
            document_path = path_match.group(1) if path_match else ""
            exception = base_cadence_allowlist.get(document_path)
            exception_matches = False
            if exception is not None:
                allowed_idx, allowed_hdr, _rationale = exception
                exception_matches = idx_base == allowed_idx and hdr_base == allowed_hdr
            if idx_base != hdr_base and not exception_matches:
                findings.append(
                    f"base cadence set mismatch (index {sorted(idx_base)} vs header {sorted(hdr_base)}); "
                    "exact base-set equality is required unless this document's expected "
                    "multi-cadence shape is allow-listed"
                )
        elif not idx_base and not hdr_base:
            pass  # both purely event-driven; EVENT-on-both agrees
        else:
            findings.append(
                f"cadence shape mismatch (index {sorted(idx_tok)} vs header {sorted(hdr_tok)}): "
                "one side names a base cadence and the other is event-only"
            )

    # Owner Role: strict equality; gated by strict_owner.
    idx_owner = cells[col_owner].strip()
    hdr_owner = header_fields.get(owner_field, "").strip()
    if idx_owner != hdr_owner:
        msg = f"owner mismatch (index {idx_owner!r} vs header {hdr_owner!r})"
        findings.append(msg if strict_owner else f"WARNING:{msg}")

    # Title: strict equality, ratcheted against the exact pinned pairs.
    if col_title is not None:
        idx_title = cells[col_title].strip()
        hdr_title = header_fields.get(title_field, "").strip()
        path_match = link_target_re.search(cells[col_path])
        display = path_match.group(1) if path_match else ""
        entry = (title_baseline or {}).get(display)
        if not idx_title or not hdr_title:
            if not idx_title:
                findings.append("empty index title")
            if not hdr_title:
                findings.append(f"empty header {title_field}")
        elif idx_title == hdr_title:
            if entry is not None:
                findings.append(f"stale title-baseline entry for {display}: titles now agree; remove the entry")
        elif entry is None:
            findings.append(f"NEW index-vs-header title diff for {display} "
                            f"(index {idx_title!r} vs header {hdr_title!r})")
        elif (idx_title, hdr_title) != entry[:2]:
            findings.append(f"title diff for {display} changed since it was baselined "
                            f"(index {idx_title!r} vs header {hdr_title!r}; pinned {entry[:2]!r})")
        elif entry[2] in title_worklist_classes:
            findings.append(f"DRIFT:{display}: index {idx_title!r} vs header {hdr_title!r}")

    return findings


def collect_findings(
    index_text: str,
    repo_root: Path,
    *,
    index_rel: str,
    header_cells: list[str],
    num_cols: int,
    col_path: int,
    col_owner: int,
    col_freq: int,
    owner_field: str,
    freq_field: str,
    strict_owner: bool,
    base_cadence_allowlist: dict[str, tuple[frozenset[str], frozenset[str], str]] | None = None,
    cadence_phrases: list[tuple[str, str]] = CADENCE_PHRASES,
    cadence_event_re: re.Pattern = CADENCE_EVENT_RE,
    link_target_re: re.Pattern = LINK_TARGET_RE,
    col_title: int | None = None,
    title_field: str | None = None,
    title_baseline: dict[str, tuple[str, str, str, str]] | None = None,
    title_classes: frozenset[str] = frozenset(),
    title_worklist_classes: frozenset[str] = frozenset(),
    title_baseline_partial: bool = False,
) -> tuple[list[str], list[str], int, list[str]] | None:
    """Return (findings, warnings, rows_checked, title_worklist), or None if the table header is not found.

    All per-row finding/warning/work-item strings are fully qualified with the
    ``index_rel:lineno`` prefix, so the wrapper prints them verbatim. The linked
    documents are resolved relative to the directory that contains the index
    register (``(repo_root / index_rel).parent``) and read here; a read or decode
    error is a per-row finding, matching the original.

    The title comparator runs only when ``col_title`` is supplied (with
    ``title_field``). Baseline entries must be four non-empty strings with a class
    in ``title_classes`` and titles that differ after stripping; a malformed entry
    is a finding. A linked document must carry exactly one ``title_field`` line in
    its metadata head. A baseline path that matched no readable row is a finding,
    or a warning when ``title_baseline_partial`` is set (a partial fixture tree);
    those two messages carry no line prefix. Every row that does not reach the
    title comparison yields a finding, so a clean run compared every row's title.
    """
    allowlist = base_cadence_allowlist or {}
    lines = index_text.splitlines()
    table = find_index_table(lines, header_cells)
    if table is None:
        return None
    _start, data_rows = table

    findings: list[str] = []
    warnings: list[str] = []
    worklist: list[str] = []
    link_base = (repo_root / index_rel).parent

    title_on = col_title is not None
    valid_baseline: dict[str, tuple[str, str, str, str]] = {}
    if title_on:
        for path, entry in (title_baseline or {}).items():
            if (not isinstance(path, str) or not path.strip()
                    or not isinstance(entry, tuple) or len(entry) != 4
                    or not all(isinstance(v, str) and v.strip() for v in entry)):
                findings.append(f"{index_rel}: malformed title-baseline entry for {path!r}: expected four non-empty strings")
                continue
            if entry[2] not in title_classes or entry[0].strip() == entry[1].strip():
                findings.append(f"{index_rel}: malformed title-baseline entry for {path}: unknown class or identical titles")
                continue
            valid_baseline[path] = entry
    seen_paths: set[str] = set()
    titles_checked = 0

    for lineno, raw in data_rows:
        cells = split_row(raw)
        if len(cells) != num_cols:
            findings.append(f"{index_rel}:{lineno}: malformed row: {len(cells)} cells, expected {num_cols}")
            continue
        m = link_target_re.search(cells[col_path])
        if not m:
            findings.append(f"{index_rel}:{lineno}: {header_cells[col_path]} cell has no parseable code-span link: {cells[col_path]!r}")
            continue
        display, target = m.group(1), m.group(2)
        resolved = (link_base / target).resolve()
        # Defence in depth: display path (repo-root-relative) must agree with target.
        expected = (repo_root / display).resolve()
        if resolved != expected:
            findings.append(f"{index_rel}:{lineno}: display path {display!r} disagrees with link target {target!r}")
            continue
        if not resolved.exists():
            findings.append(f"{index_rel}:{lineno}: linked document does not exist: {display}")
            continue
        try:
            doc_text = resolved.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            findings.append(f"{index_rel}:{lineno}: cannot read linked document {display}: {exc}")
            continue
        seen_paths.add(display)
        block = parse_metadata_block(doc_text)
        if owner_field not in block.fields:
            findings.append(f"{index_rel}:{lineno}: linked document {display} header has no {owner_field} field")
            continue
        if freq_field not in block.fields:
            findings.append(f"{index_rel}:{lineno}: linked document {display} header has no {freq_field} field")
            continue
        row_col_title = None
        if title_on:
            title_lines = [
                line for line in doc_text.splitlines()[:METADATA_HEAD_LINES]
                if (m_field := METADATA_FIELD_RE.match(line)) and m_field.group(1) == title_field
            ]
            if not title_lines:
                findings.append(f"{index_rel}:{lineno}: linked document {display} header has no {title_field} field")
            elif len(title_lines) != 1:
                findings.append(f"{index_rel}:{lineno}: linked document {display} has duplicate {title_field} fields")
            else:
                row_col_title = col_title
                titles_checked += 1
        for f in check_row(
            cells, block.fields, strict_owner,
            col_path=col_path, col_owner=col_owner, col_freq=col_freq,
            owner_field=owner_field, freq_field=freq_field,
            base_cadence_allowlist=allowlist,
            link_target_re=link_target_re,
            cadence_phrases=cadence_phrases, cadence_event_re=cadence_event_re,
            col_title=row_col_title, title_field=title_field,
            title_baseline=valid_baseline, title_worklist_classes=title_worklist_classes,
        ):
            if f.startswith("WARNING:"):
                warnings.append(f"{index_rel}:{lineno}: {f[len('WARNING:'):]}")
            elif f.startswith("DRIFT:"):
                worklist.append(f"{index_rel}:{lineno}: {f[len('DRIFT:'):]}")
            else:
                findings.append(f"{index_rel}:{lineno}: {f}")

    if title_on:
        for path in sorted(set(valid_baseline) - seen_paths):
            message = (f"title-baseline entry for {path} matched no resolvable "
                       "active-index row; reconcile or prune the entry")
            (warnings if title_baseline_partial else findings).append(message)
        if not titles_checked:
            findings.append(f"{index_rel}: zero title cells checked")

    return findings, warnings, len(data_rows), worklist
