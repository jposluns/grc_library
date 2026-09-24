#!/usr/bin/env python3
"""Symmetric narrative-boundary - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A; narrative-family):
the PURE symmetric scan (the fence helpers + parse_metadata_run + scan_outside_file
+ check_inside_page) is the source of record here in the pack, moved verbatim from
the grc gate. The narrative document type, the path-scoped entry-point exemption, the
8-field extension set, the allowed corpus document-type set, and the two line-anchored
markers are supplied by the adopter via configure(ref), so the engine's LOGIC is
project-agnostic (its finding-message text carries the configured type/field names
literally, a byte-identity residue of the verbatim transfer). The grc wrapper
(tools/lint-narrative-boundary.py) supplies them + the repository scan scope (discover),
configures the engine, and keeps the self-test, main, module-global shims
(scan_outside_file / check_inside_page), and the exit codes.
"""

from __future__ import annotations

import re
from pathlib import Path  # noqa: F401  # used in the check-function annotations (get_type_hints fidelity)

try:
    from aiqt_corpus import METADATA_FIELD_RE, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_narrative_boundary: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# --- Narrative markers + type/field sets: populated by configure(ref). ---
# Placeholders until an adopter calls configure(); the grc wrapper does so at import.
NARRATIVE_DOCUMENT_TYPE = ""
ENTRY_POINT = ""
EXTENSION_FIELDS: tuple[str, ...] = ()
CORPUS_DOCUMENT_TYPES: frozenset[str] = frozenset()
NARRATIVE_TYPE_LINE_RE = None
EXTENSION_FIELD_LINE_RE = None


def configure(ref) -> None:
    """Populate the narrative document type, the entry-point exemption, the extension
    field set, the corpus document-type set, and the two line-anchored marker regexes
    from the adopter. parse_metadata_run / scan_outside_file / check_inside_page resolve
    these as module globals; call once before scan_outside_file()/check_inside_page()."""
    global NARRATIVE_DOCUMENT_TYPE, ENTRY_POINT, EXTENSION_FIELDS, CORPUS_DOCUMENT_TYPES
    global NARRATIVE_TYPE_LINE_RE, EXTENSION_FIELD_LINE_RE
    NARRATIVE_DOCUMENT_TYPE = ref.narrative_document_type
    ENTRY_POINT = ref.entry_point
    EXTENSION_FIELDS = ref.extension_fields
    CORPUS_DOCUMENT_TYPES = ref.corpus_document_types
    NARRATIVE_TYPE_LINE_RE = ref.narrative_type_line_re
    EXTENSION_FIELD_LINE_RE = ref.extension_field_line_re


# Marker-aware fence parser: a fenced block closes only on a line using the SAME
# marker char and a run length >= the opener, with no info string. It is a local
# approximation of CommonMark, not a full parser (any leading indentation is
# accepted, a backtick info string may contain a backtick, and container blocks are
# not modelled); a file that ends inside an open fence is reported (3b54b), so the
# residue that remains silent is a fence boundary or extent the model gets wrong while
# its scan still closes before the end of the file: a line mis-recognized as an opener
# followed by a later closer, or a fence that CommonMark ends at the edge of its list
# or blockquote container but this model carries on to a later fence line.
_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


def _fence_marker(line: str) -> tuple[str, int, str] | None:
    """(char, run-length, info-string) for a fence delimiter line, else None."""
    m = _FENCE_RE.match(line)
    if not m:
        return None
    run = m.group(1)
    return run[0], len(run), m.group(2).strip()


def _closes(marker: "tuple[str, int, str] | None", opener: "tuple[str, int]") -> bool:
    """True iff ``marker`` closes a block opened by ``opener`` (same char, length
    >= opener, no info string)."""
    return (marker is not None and marker[0] == opener[0]
            and marker[1] >= opener[1] and not marker[2])


def parse_metadata_run(text: str) -> dict[str, str]:
    """First-occurrence field values of the leading metadata run (the block
    ending at the first ``---`` or blank line after at least one field)."""
    fields: dict[str, str] = {}
    seen = False
    open_fence: "tuple[str, int] | None" = None
    for line in text.splitlines():
        # Fence-aware (marker-type-tracking): a fenced example block is not the
        # metadata run. A block closes only on the same marker char and length; a
        # mismatched fence inside it (``` inside a ~~~ block) is content.
        marker = _fence_marker(line)
        if open_fence is not None:
            if _closes(marker, open_fence):
                open_fence = None
            continue
        if marker is not None:
            open_fence = (marker[0], marker[1])
            continue
        stripped = line.strip()
        if seen and (stripped.startswith("---") or not stripped):
            break
        m = METADATA_FIELD_RE.match(line)
        if m:
            name, value = m.group(1).strip(), m.group(2).strip()
            if value.endswith("\\"):
                value = value[:-1].rstrip()
            fields.setdefault(name, value)
            seen = True
    return fields


def scan_outside_file(path: Path, rel: str) -> list[str]:
    """The OUTSIDE side: reject narrative type / extension fields anywhere.

    Fence-aware and line-anchored (see module docstring). Applied to every
    ``.md`` outside the root ``executive/`` tree, README paths included."""
    text = read_text_safe(path)
    if text is None:
        return [f"{rel}: not readable / not utf-8 (a file outside executive/ that cannot be "
                f"read cannot be cleared of narrative markers; fail loud, not open)"]
    findings: list[str] = []
    open_fence: "tuple[str, int] | None" = None
    open_line = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        marker = _fence_marker(line)
        if open_fence is not None:
            # inside a fenced block: closes only on the same marker char and a
            # length >= the opener with no info string; a mismatched fence
            # (``` inside a ~~~ block) is content, not a close.
            if _closes(marker, open_fence):
                open_fence = None
            continue
        if marker is not None:
            open_fence = (marker[0], marker[1])
            open_line = lineno
            continue
        if NARRATIVE_TYPE_LINE_RE.match(line):
            findings.append(
                f"{rel}:L{lineno}: narrative document type {NARRATIVE_DOCUMENT_TYPE!r} "
                f"outside executive/ (a narrative page outside executive/ is a defect; "
                f"move the page, never retype it)"
            )
        m = EXTENSION_FIELD_LINE_RE.match(line)
        if m:
            findings.append(
                f"{rel}:L{lineno}: narrative-extension field {m.group(1)!r} outside "
                f"executive/ (extension fields are narrative-only; this closes the "
                f"retyped-leak escape of the corpus metadata gate)"
            )
    if open_fence is not None:
        # 3b54b: fail loud rather than silently skipping the rest of the file.
        findings.append(
            f"{rel}:L{open_line}: the file ends inside the fence opened here (per this gate's "
            f"marker-aware scan), so every line after it went unscanned for narrative markers; "
            f"close the fence"
        )
    return findings


def check_inside_page(path: Path, rel: str) -> list[str]:
    """The INSIDE side: require the narrative type and the full extension
    block; reject corpus document types. Applied to every ``.md`` under the
    root ``executive/`` tree except the path-scoped ``executive/README.md``."""
    text = read_text_safe(path)
    if text is None:
        return [f"{rel}: not readable / not utf-8"]
    findings: list[str] = []
    meta = parse_metadata_run(text)
    dtype = meta.get("Document Type")
    if dtype in CORPUS_DOCUMENT_TYPES:
        findings.append(
            f"{rel}: corpus document type {dtype!r} inside executive/ (executive/ is "
            f"not a corpus domain; a corpus document may never live here)"
        )
    elif dtype != NARRATIVE_DOCUMENT_TYPE:
        findings.append(
            f"{rel}: every page under executive/ must carry Document Type "
            f"{NARRATIVE_DOCUMENT_TYPE!r}, got {dtype!r} (only the entry point "
            f"{ENTRY_POINT} is exempt, path-scoped)"
        )
    for fld in EXTENSION_FIELDS:
        if fld not in meta:
            findings.append(
                f"{rel}: missing narrative-extension field {fld!r} (every narrative "
                f"page carries the full 8-field extension block)"
            )
    return findings
