#!/usr/bin/env python3
"""One-way narrative authority-boundary - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A; narrative-family):
the PURE scan (the link/fence regexes + _fence_marker/_closes + _resolves_into_narrative
+ check_file + check_taxonomy) is the source of record here in the pack, moved verbatim
from the grc gate. The narrative root and its two derived mention regexes are supplied
by the adopter via configure(ref), so the engine's LOGIC is narrative-root-agnostic (its
finding-message text and internal docstrings carry the configured root name literally, a
byte-identity residue of the verbatim transfer); the grc
wrapper (tools/lint-narrative-authority-boundary.py) supplies them + the corpus scan
scope (iter_markdown_files), configures the engine, and keeps the self-test, main,
module-global shims (check_file / check_taxonomy), and the exit codes.
"""

from __future__ import annotations

import re
from pathlib import Path  # noqa: F401  # used in the check-function annotations (get_type_hints fidelity)

try:
    from aiqt_corpus import parse_metadata_block, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_narrative_authority_boundary: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# --- Narrative root + its derived mention regexes: populated by configure(ref). ---
# Placeholders until an adopter calls configure(); the grc wrapper does so at import.
NARRATIVE_ROOT = ""
FIELD_MENTION_RE = None
TAXONOMY_MENTION_RE = None
# Placeholder so the check-function signatures' `root: Path = REPO_ROOT` default binds
# at import (byte-identical to the original signatures); the shim ALWAYS passes root
# explicitly, so this default value is never used in a call.
REPO_ROOT = None


def configure(ref) -> None:
    """Populate the narrative root and its two derived mention regexes from the adopter.
    _resolves_into_narrative / check_file / check_taxonomy resolve these as module
    globals; call once before check_file()/check_taxonomy()."""
    global NARRATIVE_ROOT, FIELD_MENTION_RE, TAXONOMY_MENTION_RE
    NARRATIVE_ROOT = ref.narrative_root
    FIELD_MENTION_RE = ref.field_mention_re
    TAXONOMY_MENTION_RE = ref.taxonomy_mention_re


# Match markdown links ``[text](target)``; external schemes skipped.
# Same patterns as gates 3 and 53.
# Link destination in ``](dest)``, ``](dest "title")``, or ``](<dest>)`` form:
# capture the destination token (up to whitespace, ")", or ">") without
# requiring the closing ")", so a titled or angle-bracket link cannot fail open.
LINK_RE = re.compile(r"\]\(\s*<?([^\s)>]+)")
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|ftp:|#)")

# Reference-style link DEFINITION: ``[label]: dest`` at line start (optionally
# ``<dest>``). A corpus doc that references executive/ via a ref-def (``[brief][n]``
# in the body, ``[n]: ../executive/brief-x.md`` below) renders as a corpus-to-narrative
# link but is NOT an inline ``](dest)`` match, so LINK_RE alone fails open. The
# line-start ``[label]:`` shape cannot collide with an inline ``[text](url)`` (``](``
# not ``]:``) or a body reference ``[text][label]``, so there is no double-count.
# 0-3 leading spaces only (4+ is an indented code block, not a link def), an
# optional blockquote prefix (a blockquoted ref-def still renders a link), then
# the label. Marker-aware fence tracking (below) excludes fenced ref-defs.
REF_DEF_RE = re.compile(r"^ {0,3}(?:>[ \t]?)*\[[^\]]+\]:\s*<?([^\s>]+)")

# Marker-aware fence parser (CommonMark): a fenced block closes only on the same
# marker char and a run length >= the opener, no info string; the shared
# ``is_fence_line`` toggle is marker-blind, so a ``` inside a ~~~ example would
# wrongly flip the scan and mis-read fenced content (a ref-def inside a fenced
# block is not a rendered link). Local to gate 87, mirroring gate 86.
_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


def _fence_marker(line: str):
    m = _FENCE_RE.match(line)
    if not m:
        return None
    run = m.group(1)
    return run[0], len(run), m.group(2).strip()


def _closes(marker, opener) -> bool:
    return (marker is not None and marker[0] == opener[0]
            and marker[1] >= opener[1] and not marker[2])


def _resolves_into_narrative(source: Path, target: str, root: Path) -> bool:
    """True iff ``target`` (a link in ``source``) resolves into the ROOT
    ``executive/`` tree of ``root``. Root-anchored: a nested ``executive``
    directory elsewhere does not count."""
    target_no_anchor = target.split("#", 1)[0]
    if not target_no_anchor:
        return False  # pure-anchor link
    resolved = (source.parent / target_no_anchor).resolve()
    try:
        rel = resolved.relative_to(root.resolve())
    except ValueError:
        return False  # outside the repo: not the narrative tree
    return len(rel.parts) >= 1 and rel.parts[0] == NARRATIVE_ROOT


def check_file(path: Path, root: Path = REPO_ROOT) -> list[tuple[int, str]]:
    """(lineno, message) findings for one corpus document."""
    text = read_text_safe(path)
    if text is None:
        # Fail LOUD, not open: an unreadable corpus file cannot be cleared of
        # executive/ references (the 1.3a fail-loud lesson).
        return [(0, "not readable / not utf-8 (cannot be cleared of executive/ references; fail loud)")]
    findings: list[tuple[int, str]] = []

    # FIELD check: any metadata field value referencing executive/.
    block = parse_metadata_block(text)
    for field, value in block.fields.items():
        if FIELD_MENTION_RE.search(value):
            lineno = block.raw_lines[field][0]
            findings.append(
                (lineno,
                 f"metadata field {field!r} references executive/ (the authority "
                 f"boundary is one-way: no corpus field may reference the "
                 f"narrative tree, Related Documents included)")
            )

    # LINK check: any markdown link resolving into the root executive/ tree.
    open_fence = None  # marker-aware: (char, run-length); ``` inside ~~~ is content
    for lineno, raw in enumerate(text.splitlines(), 1):
        marker = _fence_marker(raw)
        if open_fence is not None:
            if _closes(marker, open_fence):
                open_fence = None
            continue
        if marker is not None:
            open_fence = (marker[0], marker[1])
            continue
        for m in LINK_RE.finditer(raw):
            target = m.group(1)
            if EXTERNAL.match(target):
                continue
            if _resolves_into_narrative(path, target, root):
                findings.append(
                    (lineno,
                     f"corpus-to-narrative link {target!r} (derive any "
                     f"corpus-explained-by-narrative view at render time from the "
                     f"narrative registry; never write it into corpus source)")
                )
        rd = REF_DEF_RE.match(raw)
        if rd:
            target = rd.group(1)
            if not EXTERNAL.match(target) and _resolves_into_narrative(path, target, root):
                findings.append(
                    (lineno,
                     f"corpus-to-narrative link {target!r} via reference definition "
                     f"(derive any corpus-explained-by-narrative view at render time "
                     f"from the narrative registry; never write it into corpus source)")
                )
    return findings


def check_taxonomy(root: Path = REPO_ROOT) -> list[tuple[int, str]]:
    """Defence-in-depth: no executive/ path may appear in taxonomy.yml."""
    tax = root / "taxonomy.yml"
    if not tax.is_file():
        return []
    text = read_text_safe(tax)
    if text is None:
        return [(0, "taxonomy.yml not readable / not utf-8 (cannot be checked for executive/ targets; fail loud)")]
    findings: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if TAXONOMY_MENTION_RE.search(line):
            findings.append(
                (lineno,
                 "taxonomy.yml carries an executive/ target (taxonomy.yml is "
                 "corpus-only by construction; the generator must reject "
                 "executive/ targets and no narrative row is ever added)")
            )
    return findings

