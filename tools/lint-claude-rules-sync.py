#!/usr/bin/env python3
"""Claude-rules local-copy sync audit.

The project consumes a subset of the ``dev-security/claude-rules/``
pack as session-start context by keeping copies under ``.claude/rules/``.
Those copies are supposed to track their pack source: the pack file is
the source of truth, and the local copy is what a Claude Code session
actually loads. When the pack source is edited but the local copy is
not (or vice versa), the session loads stale guidance and nothing
catches it, because both ``.claude/`` and ``dev-security/claude-rules/``
are on the corpus linters' exemption list.

This audit closes that gap. For each declared (local copy, pack source)
pair it compares the two files' *bodies* and fails on any divergence.

Three intentional, by-design differences are stripped before comparison
(they are local-only adaptations, not drift):

  1. A leading YAML frontmatter block (``---`` ... ``---``). The
     path-scoped local copies (``python.md``, ``input-validation.md``,
     ``cicd-gates.md``) carry a ``paths:`` frontmatter that scopes the
     rule to this repository's relevant files via Claude Code's
     path-scoped-rules feature. The pack source is generic and carries
     no such block.
  2. A leading HTML provenance comment (``<!-- Source: ... -->``) and
     surrounding blank lines. The local copies note where they were
     copied from; the pack source does not.
  3. A trailing PROJECT-OVERLAY block in the local copy: everything
     from the first line matching ``OVERLAY_MARKER`` to end-of-file.
     The overlay carries this project's wiring and lineage (the
     project-specific content the distributable pack deliberately does
     not carry); it is local-only and never synced. Two failure modes
     guard the mechanism: the marker appearing anywhere in a MAPPED pack
     source fails the audit (the overlay must never leak into the
     distributable; only sources in the mirror map are scanned), and the marker appearing more than once in a
     local copy fails it (one trailing block only).

After stripping those, the remaining body must be identical (trailing
newline differences are normalized away). A governance local copy with
no overlay block and no preamble is compared effectively whole-file.

Completeness check: every markdown file under ``.claude/rules/`` other
than the local-only ``external/`` overlay (third-party rule sets that
have no pack source) must appear in the mapping below. A new local
mirror that is not mapped fails the audit, rather than going silently
unchecked. This is the property that prevents the drift class from
recurring one level up: forgetting to map a new mirror is loud, not
silent.

The ``--root`` argument overrides the repository root used to resolve
both halves of every pair. Used by the regression test suite to point
at a synthetic minimal source set with engineered drift so the linter's
detection logic can be exercised.

Stdlib-only Python 3.11.

Exit codes:

    0   every mapped local copy's body matches its pack source, and
        every local rule file is covered by the mapping.
    1   one or more findings (body drift, or an unmapped local file).
    2   internal error (a declared source or local file is missing).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lint_common import read_text_safe

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directory holding the project-local rule copies.
LOCAL_RULES_DIR_REL = ".claude/rules"

# Local-only overlay: third-party rule sets with no pack source. These
# are not mirrored and are excluded from the completeness check.
LOCAL_ONLY_SUBDIR = "external"

# Marker opening the trailing project-overlay block a LOCAL copy may
# carry (project wiring and lineage; local-only, never synced). Exactly
# this line, alone on its line. It must never appear in a pack source.
OVERLAY_MARKER = "<!-- PROJECT-OVERLAY: not part of the distributable pack -->"

# Mapping of project-local copy -> pack source of truth. Both paths are
# relative to the repository root. Every markdown file under
# ``.claude/rules/`` (except the ``external/`` overlay) must appear as a
# key here; the completeness check enforces that.
MIRROR_MAP: dict[str, str] = {
    ".claude/rules/secrets.md": "dev-security/claude-rules/core/secrets.md",
    ".claude/rules/input-validation.md": "dev-security/claude-rules/core/input-validation.md",
    ".claude/rules/python.md": "dev-security/claude-rules/languages/python.md",
    ".claude/rules/cicd-gates.md": "dev-security/claude-rules/pipeline/cicd-gates.md",
    ".claude/rules/governance/gate-discipline.md": "dev-security/claude-rules/governance/gate-discipline.md",
    ".claude/rules/governance/change-tracking.md": "dev-security/claude-rules/governance/change-tracking.md",
    ".claude/rules/governance/evidence-grounded-completion.md": "dev-security/claude-rules/governance/evidence-grounded-completion.md",
    ".claude/rules/governance/clarify-before-acting.md": "dev-security/claude-rules/governance/clarify-before-acting.md",
    ".claude/rules/governance/artefact-and-branch-discipline.md": "dev-security/claude-rules/governance/artefact-and-branch-discipline.md",
    ".claude/rules/governance/action-before-explanation-of-inaction.md": "dev-security/claude-rules/governance/action-before-explanation-of-inaction.md",
    ".claude/rules/governance/validate-inference-before-action.md": "dev-security/claude-rules/governance/validate-inference-before-action.md",
    ".claude/rules/governance/ai-assistant-workflow-disciplines.md": "dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md",
    ".claude/rules/governance/trust-recovery-escalation.md": "dev-security/claude-rules/governance/trust-recovery-escalation.md",
    ".claude/rules/governance/project-integrity.md": "dev-security/claude-rules/governance/project-integrity.md",
    ".claude/rules/governance/surface-counterproductive-instructions.md": "dev-security/claude-rules/governance/surface-counterproductive-instructions.md",
    ".claude/rules/governance/high-assurance-verification.md": "dev-security/claude-rules/governance/high-assurance-verification.md",
    ".claude/rules/governance/session-lifecycle.md": "dev-security/claude-rules/governance/session-lifecycle.md",
    ".claude/rules/governance/decision-classification-before-enacting.md": "dev-security/claude-rules/governance/decision-classification-before-enacting.md",
}


def strip_preamble(text: str) -> str:
    """Return ``text`` with a leading frontmatter block and provenance
    comment removed, and trailing newlines normalized.

    Removes, in order:
      1. A leading YAML frontmatter block delimited by ``---`` lines.
      2. Any leading blank lines and HTML comment blocks (``<!-- -->``,
         possibly multi-line).

    The result is the rule body, comparable across a local copy (which
    may carry the above local-only additions) and its pack source
    (which does not).
    """
    lines = text.splitlines()
    i = 0
    # 1. Skip a leading YAML frontmatter block.
    if i < len(lines) and lines[i].strip() == "---":
        i += 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        if i < len(lines):  # consume the closing delimiter
            i += 1
    # 2. Skip leading blank lines and HTML comment blocks.
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped == "":
            i += 1
        elif stripped.startswith("<!--"):
            # Skip until the line that closes the comment.
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            if i < len(lines):
                i += 1
        else:
            break
    return "\n".join(lines[i:]).rstrip("\n")


def split_overlay(text: str) -> tuple[str, int]:
    """Return ``(text_without_overlay, marker_count)``.

    The overlay is the trailing block from the first line equal to
    ``OVERLAY_MARKER`` (ignoring surrounding whitespace) to end-of-file,
    plus immediately preceding blank lines. ``marker_count`` is the
    total number of marker lines seen, so the caller can fail a copy
    carrying more than one.
    """
    lines = text.splitlines()
    marker_count = sum(1 for ln in lines if ln.strip() == OVERLAY_MARKER)
    if marker_count == 0:
        return text, 0
    cut = next(i for i, ln in enumerate(lines) if ln.strip() == OVERLAY_MARKER)
    while cut > 0 and lines[cut - 1].strip() == "":
        cut -= 1
    return "\n".join(lines[:cut]), marker_count


def find_local_rule_files(root: Path) -> list[Path]:
    """Return all markdown files under ``.claude/rules/`` except the
    local-only ``external/`` overlay."""
    local_dir = root / LOCAL_RULES_DIR_REL
    if not local_dir.is_dir():
        return []
    out: list[Path] = []
    for f in sorted(local_dir.rglob("*.md")):
        rel_parts = f.relative_to(local_dir).parts
        if rel_parts and rel_parts[0] == LOCAL_ONLY_SUBDIR:
            continue
        out.append(f)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit that every project-local .claude/rules copy's body "
            "matches its dev-security/claude-rules pack source, and that "
            "every local rule file is covered by the sync mapping."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help=(
            "Override the repository root used to resolve both halves of "
            "every mapped pair. Defaults to the repository root derived "
            "from this file's location."
        ),
    )
    args = parser.parse_args(argv)
    root: Path = args.root.resolve()

    findings: list[str] = []

    # --- Body-sync check for every mapped pair. ---
    for local_rel, source_rel in sorted(MIRROR_MAP.items()):
        local_path = root / local_rel
        source_path = root / source_rel
        if not local_path.is_file():
            print(
                f"ERROR: mapped local copy does not exist: {local_rel}",
                file=sys.stderr,
            )
            return 2
        if not source_path.is_file():
            print(
                f"ERROR: mapped pack source does not exist: {source_rel} "
                f"(referenced by {local_rel})",
                file=sys.stderr,
            )
            return 2
        local_text = read_text_safe(local_path)
        source_text = read_text_safe(source_path)
        if local_text is None or source_text is None:
            print(
                f"ERROR: could not read one of {local_rel} / {source_rel} "
                f"as UTF-8 text",
                file=sys.stderr,
            )
            return 2
        if any(ln.strip() == OVERLAY_MARKER for ln in source_text.splitlines()):
            findings.append(
                f"overlay leak: pack source {source_rel} contains the "
                f"PROJECT-OVERLAY marker. The overlay block is a "
                f".claude/rules/ local-copy mechanism only; remove it "
                f"from the distributable pack file."
            )
            continue
        local_text, marker_count = split_overlay(local_text)
        if marker_count > 1:
            findings.append(
                f"duplicate overlay marker: {local_rel} carries the "
                f"PROJECT-OVERLAY marker {marker_count} times; a local "
                f"copy may carry at most one trailing overlay block."
            )
            continue
        if strip_preamble(local_text) != strip_preamble(source_text):
            findings.append(
                f"body drift: {local_rel} diverges from its pack source "
                f"{source_rel}. Re-sync the local copy from the source "
                f"(preserving the local copy's frontmatter / provenance "
                f"comment, if any)."
            )

    # --- Completeness check: every local rule file must be mapped. ---
    for local_path in find_local_rule_files(root):
        rel = local_path.relative_to(root).as_posix()
        if rel not in MIRROR_MAP:
            findings.append(
                f"unmapped local rule file: {rel}. Add it to MIRROR_MAP "
                f"in tools/lint-claude-rules-sync.py with its pack source, "
                f"so its sync with the source is audited (or move it under "
                f".claude/rules/{LOCAL_ONLY_SUBDIR}/ if it is a local-only "
                f"overlay with no pack source)."
            )

    if not findings:
        print(
            f"OK: {len(MIRROR_MAP)} local rule copies are in sync with "
            f"their pack sources; every local rule file is mapped."
        )
        return 0

    print("FAIL: claude-rules sync findings:")
    for f in findings:
        print(f"  [claude-rules-sync] {f}")
    print(
        f"\n{len(findings)} finding(s). The .claude/rules/ copies are "
        f"loaded as session context and must track their "
        f"dev-security/claude-rules/ pack sources."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
