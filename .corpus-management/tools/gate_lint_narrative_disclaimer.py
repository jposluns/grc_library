#!/usr/bin/env python3
"""Executive-narrative authority-disclaimer presence - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(disclaimer_finding, check_file) is the source of record here in the pack, moved
verbatim from the grc gate. The required disclaimer text is supplied by the adopter
via configure(ref), so the engine carries no project content; the grc wrapper
(tools/lint-narrative-disclaimer.py) supplies the disclaimer + the narrative scan
scope (discover), configures the engine, and keeps the self-test, main, shims, and
the exit codes.
"""

from __future__ import annotations

from pathlib import Path  # noqa: F401  # used in check_file's annotation (get_type_hints fidelity)

try:
    from aiqt_corpus import METADATA_FIELD_RE, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_narrative_disclaimer: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# --- Required disclaimer text: populated by configure(ref). ---
# Placeholder until an adopter calls configure(); the grc wrapper does so at import.
DISCLAIMER = ""


def configure(disclaimer) -> None:
    """Populate the required verbatim disclaimer text from the adopter. disclaimer_finding
    resolves it as a module global; call once before disclaimer_finding()/check_file()."""
    global DISCLAIMER
    DISCLAIMER = disclaimer


def disclaimer_finding(text: str, rel: str) -> str | None:
    """Return a finding string if the page lacks the verbatim disclaimer in the
    required position, else None. PURE (operates on the page text)."""
    lines = text.splitlines()

    # Locate the leading metadata block's closing `---` separator. The metadata
    # block is the CONTIGUOUS leading run of metadata-field lines (matching
    # METADATA_FIELD_RE, so a `**bold body**` paragraph is NOT a field: it lacks
    # the `Name:**` label), optionally preceded by a `# Title` and blank lines,
    # ending at the first `---` after that run. Body text therefore cannot FORGE
    # the anchor: a `**bold**` paragraph plus a later `---` is not a metadata block.
    seen_field = False
    close_idx: int | None = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if METADATA_FIELD_RE.match(line):
            seen_field = True
            continue
        if not seen_field:
            # Before any field: tolerate a leading `# Title` and blank lines; any
            # other non-field content means there is no leading metadata block.
            if not stripped or stripped.startswith("#"):
                continue
            break
        # After the field run: tolerate blank lines up to the closing `---`.
        if not stripped:
            continue
        if stripped == "---":
            close_idx = i
            break
        # A non-field, non-blank, non-`---` line ends the run without a separator.
        break

    if close_idx is None:
        return (
            f"{rel}: could not locate the metadata block's closing '---' separator, "
            f"so the authority disclaimer's required position cannot be confirmed "
            f"(the disclaimer must be the first body content after that separator)"
        )

    # The FIRST non-blank line after the closing `---` must be the verbatim
    # disclaimer. Fences are NOT skipped: a fenced block is body content, so a
    # fence appearing before the disclaimer means the disclaimer is not the first
    # body content. The comparison uses rstrip only (never lstrip), so a leading-
    # indented line (a Markdown indented CODE block, not a rendered blockquote) is
    # not accepted as the disclaimer.
    for line in lines[close_idx + 1:]:
        if not line.strip():
            continue
        if line.rstrip() == DISCLAIMER:
            return None
        if line.lstrip().startswith("#"):
            return (
                f"{rel}: the first body content after the metadata block is a section "
                f"heading, not the authority disclaimer; the verbatim disclaimer must "
                f"appear before the first section heading"
            )
        return (
            f"{rel}: the first body content after the metadata block is not the "
            f"verbatim authority disclaimer (found: {line.strip()[:60]!r}...); the "
            f"disclaimer text is fixed by the specification and must appear verbatim "
            f"at column 0, as the first body content"
        )

    return (
        f"{rel}: no body content after the metadata block; the verbatim authority "
        f"disclaimer is required as the first body content"
    )


def check_file(path: Path, rel: str) -> list[str]:
    text = read_text_safe(path)
    if text is None:
        return [
            f"{rel}: not readable / not utf-8 (a page whose disclaimer cannot be read "
            f"cannot be cleared of the requirement; fail loud, not open)"
        ]
    finding = disclaimer_finding(text, rel)
    return [finding] if finding else []

