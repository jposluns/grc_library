#!/usr/bin/env python3
"""Document Date staleness audit.

For every Markdown file under corpus scope that carries a canonical
``**Date:**`` metadata field, compare the Date value to the file's
most-recent git commit date (committer date). Fail when the metadata
Date is more than ``--max-lag-days`` behind the commit date, OR when
the Date is more than ``--max-future-days`` AHEAD of the current UTC
date (a "last updated" Date cannot be in the future; the future-date
check compares to today, not the commit date, so a working-tree Date
freshly bumped to today is never a false positive).

This audit catches a class of defect that no other gate catches: a
file's content was edited in a commit, but the per-document ``Date``
metadata field was not refreshed to reflect the edit date. The
ingestion specification requires every substantive content change to
update both ``Version`` and ``Date``; existing audits enforce version
monotonicity (gate 13) and library-level version-date consistency
(gate 29), but neither compares the per-document ``Date`` to the
file's git commit date. The S.4 PR (library version ``2026.06.21``,
shipped 2026-06-19) demonstrated the gap: five governance documents
were substantively edited but their per-document ``Date`` and
``Version`` fields stayed at their pre-edit values. The gap was
caught later by inspection and remediated in the ``2026.06.23``
backfill PR. This linter closes the gap so a future omission
mechanically blocks the merge.

How the audit decides what is in scope:

  1. The set of paths the linter scans is the same default-paths set
     the metadata audit uses (corpus directories plus the repo-root
     meta files). Override via positional arguments.
  2. Inside each scanned file, the linter looks for a metadata Date
     field of the form ``**Date:** YYYY-MM-DD`` (trailing ``\\`` line
     break tolerated) via the shared metadata parser in
     ``lint_common``. Files without a Date field are skipped (and the
     skip count is reported); a file whose Date field is PRESENT but
     malformed (a trailing annotation, a non-ISO value) is a FINDING,
     not a skip, so a formatting slip cannot silently exempt a file
     from the staleness check (the guardrail review's GR-3 fail-loud
     migration, wave 1).
  3. The file's most-recent commit date is obtained via
     ``git log -1 --follow --format=%cI -- <path>`` (committer date,
     ISO-8601 with timezone). Files with no git history (untracked
     or staged-only) are skipped — the audit cannot reason about
     them.
  4. Generated markdown files (the portal page and the maturity
     scorecard) are exempt because their ``Date`` is set by the
     generator at regeneration time; their freshness is policed by
     the generator-output drift gates (33 and 34).

Tolerance and grandfathering:

  The ``--max-lag-days`` flag (default 1) sets the maximum number of
  whole days the metadata Date may lag behind the commit date. The
  default of 1 day handles trailing-edge timezone differences (a
  commit at 23:59 in one timezone is at 00:59 the next day in
  another); a metadata Date that lags by 2 or more days reflects a
  real omission.

  The ``--baseline-date`` flag (default ``2026-06-19``) is the
  inception date of this audit. Files whose most-recent git commit
  predates the baseline are skipped: their staleness reflects
  historical drift accumulated before the audit existed, not a
  defect introduced under the discipline this audit enforces. The
  initial-corpus run before this audit was wired identified 233
  files with stale Dates; rather than block CI on the historical
  backlog, the audit grandfathers it. A maintainer who runs a
  full-corpus refresh in the future can shift the baseline forward
  by editing the default in this file (the change-tracking
  discipline requires the baseline shift to be recorded in the
  CHANGELOG).

  Files committed at or after the baseline are subject to the full
  ``--max-lag-days`` check. The S.4 backfill PR (library version
  ``2026.06.23``, shipped 2026-06-19) is the inflection point: every
  PR landing after it is expected to bump the per-document Date on
  every substantive content change, and this audit catches the
  omission.

The ``--root`` flag overrides the repository root used both for
resolving default scan paths and for running ``git log``. Used by
the regression test suite to point at a synthetic minimal source
set with engineered staleness so the linter's detection logic can
be exercised without touching the real corpus.

Stdlib-only Python 3.11. Subprocess invocations always use the
argument-list form (no ``shell=True``); inputs are file paths
resolved from the configured scan paths, not from external input.

Exit codes:

    0   every in-scope file's metadata Date is within
        ``--max-lag-days`` of its most-recent commit date and no more
        than ``--max-future-days`` ahead of today (UTC), or no
        in-scope files were found / had Date metadata (bootstrap
        pass).
    1   one or more findings: a stale Date (lags the commit date), a
        future-dated Date (ahead of today), or a malformed Date value.
    2   internal error (a subprocess failed unexpectedly).
"""

from __future__ import annotations

import argparse
import datetime
import subprocess
import sys
from pathlib import Path

from lint_common import (
    AUDITED_DOMAIN_DIRS,
    DEFAULT_EXEMPT_DIRS,
    iter_markdown_targets,
    parse_iso_date,
    parse_metadata_block,
    read_text_safe,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

# Inception date of this audit. Files whose most-recent commit predates
# this date are grandfathered: their stale Dates accumulated before the
# audit existed and are not within scope for the discipline this audit
# enforces. See module docstring for the rationale.
DEFAULT_BASELINE_DATE = datetime.date(2026, 6, 19)

# Default scan set: same shape as the metadata audit's default paths,
# without the per-linter exempt lists that the metadata audit applies
# to the ``.claude/`` rules pack and the dev-security claude-rules
# subdirectory (the corpus linters skip those via DEFAULT_EXEMPT_DIRS
# and via dev-security exempt prefixes; this linter relies on the
# DEFAULT_EXEMPT_DIRS skip for .claude/ and additionally exempts
# the dev-security/claude-rules/ tree below).
# Meta files plus ``docs`` (the generated-artefact directory, a
# per-linter extra not in the shared domain set) plus the canonical
# audited domain directories. The domain run is splatted from
# ``AUDITED_DOMAIN_DIRS`` (the single source of truth in
# ``lint_common``) rather than hardcoded, so a future top-level
# audited directory propagates here automatically; the
# directory-scan-scope parity gate enforces this.
DEFAULT_SCAN_PATHS: tuple[str, ...] = (
    "README.md",
    "NOTICE.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "AUTHORS.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "docs",
    *AUDITED_DOMAIN_DIRS,
)

# Generated markdown files: the Date is set by the generator at
# regeneration time, not by hand. Generator-output drift gates (32
# and 33) police their consistency with the source metadata. This
# linter would otherwise false-positive on them at every commit that
# updates the source-of-truth metadata but happens to leave the
# generated output's Date older.
EXEMPT_FILES: frozenset[str] = frozenset(
    {
        "docs/portal.md",
        "docs/maturity-scorecard.md",
    }
)

# Pack-rule and skill directories carry their own format conventions
# (the dev-security/claude-rules/ tree uses YAML frontmatter for
# skills; the rule pack documents use a leaner metadata convention
# than the corpus's 13-field block). They are not in scope for this
# linter.
EXEMPT_DIR_PREFIXES: tuple[str, ...] = (
    "dev-security/claude-rules/",
)

# Date parsing is delegated to the shared metadata parser
# (lint_common.parse_metadata_block + parse_iso_date), which strips
# the optional trailing backslash (hard-line-break marker) and windows
# the scan to the metadata head lines. This retired the private
# line-end-anchored DATE_RE whose non-match silently skipped a file
# with an annotated Date value (GR-3 wave 1).


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit that every corpus markdown file with a metadata Date "
            "field has a Date no more than --max-lag-days behind its "
            "most-recent git commit date."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help=(
            "Override the repository root used both for resolving "
            "scan paths and for running `git log`. Defaults to the "
            "repository root derived from this file's location."
        ),
    )
    parser.add_argument(
        "--max-lag-days",
        type=int,
        default=1,
        help=(
            "Maximum whole-day lag tolerated between the metadata "
            "Date and the file's most-recent commit date. Default 1."
        ),
    )
    parser.add_argument(
        "--max-future-days",
        type=int,
        default=0,
        help=(
            "Maximum whole days the metadata Date may LEAD the current "
            "UTC date. Default 0: a Date after today is a finding (a "
            "document cannot have been updated in the future). Compared "
            "to today, not to the commit date, so a freshly-bumped "
            "working-tree Date is never a false positive."
        ),
    )
    parser.add_argument(
        "--baseline-date",
        type=datetime.date.fromisoformat,
        default=DEFAULT_BASELINE_DATE,
        help=(
            "Files whose most-recent commit predates this date are "
            "grandfathered (skipped). Default %s."
            % DEFAULT_BASELINE_DATE.isoformat()
        ),
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=list(DEFAULT_SCAN_PATHS),
        help=(
            "Paths to scan (relative to --root). Defaults to the "
            "standard corpus directory and repo-root meta file set."
        ),
    )
    return parser.parse_args(argv)


def get_metadata_date(text: str) -> tuple[datetime.date | None, str | None]:
    """Return ``(date, malformed_value)`` for a file's metadata Date field.

    Three outcomes:

      - ``(date, None)``: a well-formed ``**Date:** YYYY-MM-DD`` field.
      - ``(None, None)``: no Date field in the metadata head window;
        the caller skips the file (legitimately date-free).
      - ``(None, raw_value)``: a Date field is PRESENT but its value is
        not exactly an ISO date (trailing annotation, malformed value).
        The caller reports a finding; silently skipping here was the
        fail-open the GR-3 migration closed.
    """
    block = parse_metadata_block(text)
    if "Date" not in block.fields:
        return None, None
    value = block.fields["Date"]
    parsed = parse_iso_date(value)
    if parsed is None:
        return None, value
    return parsed, None


def get_file_commit_date(
    file_path: Path,
    *,
    repo_root: Path,
) -> datetime.date | None:
    """Return the date of the file's most-recent commit, or None.

    Uses ``git log -1 --follow --format=%cI`` so rename history is
    followed. The committer date (``%cI``) is preferred over the
    author date because committer time reflects when the commit was
    actually made, which is what the ingestion-spec contract is
    about. The result is converted to UTC before extracting the
    date portion to give a stable comparison frame regardless of
    the maintainer's local timezone.

    Returns None when:
      - the file has no commit history (untracked / staged-only);
      - the file is outside the git repo;
      - git itself is not available.
    """
    rel = file_path.relative_to(repo_root) if file_path.is_absolute() else file_path
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "-1",
                "--follow",
                "--format=%cI",
                "--",
                str(rel),
            ],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        # git binary not found.
        return None
    if result.returncode != 0:
        return None
    stamp = result.stdout.strip()
    if not stamp:
        return None
    try:
        dt = datetime.datetime.fromisoformat(stamp)
    except ValueError:
        return None
    return dt.astimezone(datetime.timezone.utc).date()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root: Path = args.root.resolve()
    max_lag_days: int = args.max_lag_days
    max_future_days: int = args.max_future_days
    baseline_date: datetime.date = args.baseline_date
    # "Today" for the future-date check is the current UTC date, matching the
    # project's UTC date convention. Compared to the metadata Date directly
    # (never to the commit date), so a working-tree Date freshly bumped to
    # today is not flagged even when the file's last commit is older.
    today_utc: datetime.date = datetime.datetime.now(datetime.timezone.utc).date()

    # Resolve scan paths against --root.
    scan_paths = [root / p for p in args.paths]
    files = iter_markdown_targets(
        scan_paths,
        exempt_dirs=DEFAULT_EXEMPT_DIRS,
    )

    findings: list[tuple[str, datetime.date, datetime.date, int]] = []
    future_findings: list[tuple[str, datetime.date, int]] = []
    malformed: list[tuple[str, str]] = []
    scanned = 0
    skipped_no_date = 0
    skipped_no_history = 0

    for f in files:
        try:
            rel = f.relative_to(root).as_posix()
        except ValueError:
            # Outside root; defensive skip.
            continue
        if rel in EXEMPT_FILES:
            continue
        if any(rel.startswith(pfx) for pfx in EXEMPT_DIR_PREFIXES):
            continue
        text = read_text_safe(f)
        if text is None:
            continue
        metadata_date, malformed_value = get_metadata_date(text)
        if malformed_value is not None:
            # Present-but-malformed Date: a finding, never a skip
            # (fail-loud per GR-3; a silent skip here exempted the
            # file from the staleness check on a formatting slip).
            malformed.append((rel, malformed_value))
            continue
        if metadata_date is None:
            skipped_no_date += 1
            continue
        # Future-dated Date check (R8a): a Date after today (UTC) is impossible
        # for a "last updated" field. Compared to today, not the commit date,
        # and evaluated before the baseline grandfather skip so a future Date on
        # an old-commit file is still caught.
        future_lead = (metadata_date - today_utc).days
        if future_lead > max_future_days:
            future_findings.append((rel, metadata_date, future_lead))
        commit_date = get_file_commit_date(f, repo_root=root)
        if commit_date is None:
            skipped_no_history += 1
            continue
        if commit_date < baseline_date:
            # Grandfathered: the file's most-recent commit predates
            # the audit's inception date; its staleness, if any, is
            # historical drift outside this audit's scope.
            continue
        scanned += 1
        lag = (commit_date - metadata_date).days
        if lag > max_lag_days:
            findings.append((rel, metadata_date, commit_date, lag))

    if malformed:
        malformed.sort()
        print(
            f"FAIL: {len(malformed)} document(s) carry a PRESENT but "
            f"malformed metadata Date field (the value must be exactly "
            f"YYYY-MM-DD, optional trailing backslash); a malformed "
            f"Date is a finding, not a skip."
        )
        for rel, value in malformed:
            print(f"  {rel} | **Date:** {value!r}")
        print(
            "\nRemediation: restore the canonical `**Date:** "
            "YYYY-MM-DD` shape (move any annotation out of the "
            "metadata value)."
        )
        return 1

    if scanned == 0 and not future_findings:
        print(
            f"OK: no files with both a metadata Date and a git "
            f"commit history were found under {len(scan_paths)} "
            f"scan path(s); nothing to verify."
        )
        return 0

    if not findings and not future_findings:
        print(
            f"OK: {scanned} file(s) checked; "
            f"all metadata Dates are within {max_lag_days} day(s) "
            f"of the file's most-recent commit date and none is dated "
            f"after today (UTC). "
            f"Skipped: {skipped_no_date} with no Date field, "
            f"{skipped_no_history} with no git history."
        )
        return 0

    # One or both finding classes are non-empty; report each present class.
    if future_findings:
        future_findings.sort(key=lambda row: (-row[2], row[0]))
        print(
            f"FAIL: {len(future_findings)} document(s) carry a metadata "
            f"Date AFTER the current UTC date ({today_utc.isoformat()}); a "
            f"'last updated' Date cannot be in the future."
        )
        print(
            "Each entry shows: file | metadata Date | days ahead of today."
        )
        for rel, mdate, lead in future_findings:
            print(f"  {rel} | {mdate.isoformat()} | +{lead}")
        print(
            "\nRemediation: correct the `**Date:**` to the date the "
            "document was actually last updated (today, in UTC, if the "
            "change is current)."
        )
        if findings:
            print()

    if findings:
        findings.sort(key=lambda row: (-row[3], row[0]))
        print(
            f"FAIL: {len(findings)} document(s) carry a metadata Date "
            f"that lags the file's most-recent commit date by more than "
            f"{max_lag_days} day(s)."
        )
        print(
            "Each entry shows: file | metadata Date | most-recent commit "
            "date (UTC) | lag (days)."
        )
        for rel, mdate, cdate, lag in findings:
            print(f"  {rel} | {mdate.isoformat()} | {cdate.isoformat()} | {lag}")
        print(
            "\nRemediation: bump the document's `**Date:**` metadata "
            "to the current date (and its `**Version:**` per the "
            "ingestion specification's disposition rules) in the same "
            "commit that changed the document's content."
        )
    return 1


if __name__ == "__main__":
    sys.exit(main())
