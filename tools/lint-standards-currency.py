#!/usr/bin/env python3
"""Standards-currency audit: project policy and register parser.

The pack engine owns citation extraction, comparison and reporting.
This wrapper owns the canonical-register schema, roots, exclusions and CLI.

PR1 defaults to report mode. Exactly two kinds of finding block in that mode:
those of the unchanged legacy Markdown stale check and a historical exception
row that does not bind (INVALID_EXCEPTION, which blocks in every mode; 3b75
below). Every other finding is advisory. A run also exits non-zero on errors
that are not findings: an UNPINNED ratchet failure below, and the register,
input and ratchet-base errors. Explicit enforce mode supports migration
fixtures; no gate invocation enables it in PR1. Every exit status, and every
condition that produces it, is listed once, under "Exit codes" at the end.

3b75: a superseded edition cited as history passes only through a reviewed row
of the TOML data file `.project-governance/register-historical-citation-exceptions.toml`;
everything else keeps blocking. The Markdown page of the same name is a generated view,
never parsed for policy; this gate refuses a page whose generated table differs from the
data (tools/build-historical-citation-exceptions.py regenerates it).

P-3.213 ratchet (maintainer ruling 2026-10-27, option A): a default-scope run
compares each standard's UNPINNED count with the checked-in baseline
`tools/standards-currency-unpinned-baseline.json` (source, keyed by register
Standard ID), which may only fall. A count above its baseline fails and names
the standard and both counts. A baseline above its count also fails, so the
recorded value is lowered in the PR that pins the citations; slack left in the
baseline would let a later change add that many new unpinned citations
unnoticed. A missing, unreadable or malformed baseline fails (statuses under
Exit codes).

The baseline itself ratchets (P-3.213 round 2): the same run reads the baseline
as it stood at a base revision and fails when an entry is above its base value,
or when an entry has no base entry although the base register already lists
that standard (a standard registered at the base had no unpinned citation there,
so a new entry is a rise). An entry with no base entry is allowed only for a
standard whose register row is new in the same change, compared by identity
key, so a renamed Standard ID is not new, and (P-3.213 round 4) only up to that
standard's UNPINNED count at the base, measured as the bootstrap measures it
below, so adding the row cannot raise the count. Conversely a register row whose
standard has a base entry cannot be removed in the change, which would move
its citations to the unratcheted UNREGISTERED count.

One function, ratchet_base, selects the base revision (P-3.213 round 3). Every
ref it uses (HEAD and refs/remotes/origin/main) is resolved exactly, by its full
name, and only the resolved object id is passed to later git calls, so a branch
or tag whose name imitates a ref cannot stand in for it (round 4). A run is a
GitHub Actions run only when GITHUB_ACTIONS is exactly the string "true" and
GITHUB_EVENT_PATH names a readable file holding a JSON object; when GITHUB_ACTIONS is
exactly "true" and the event file is unset, missing, unreadable or not a JSON object,
the run fails closed (round 4), and a run with any other GITHUB_ACTIONS value, or none,
is local. In a pull_request run the base is HEAD^1 of the checked-out
merge commit, read from git, and the payload's pull_request.base.sha must be that
commit or an ancestor of it (the base branch may have moved after the event;
round 4). In a push run the base is the payload's "before", which must be a
proper ancestor of HEAD. A schedule or workflow_dispatch run (the nightly sweep,
through tools/run_all_audits.sh), and every local run (tools/run_all_audits.sh,
pre-commit, a direct run), takes the one merge base of HEAD and
refs/remotes/origin/main. A base that cannot be determined or read fails closed,
with an "UNPINNED ratchet base" message except for the few causes Exit codes lists
under main's OSError and UnicodeError handler (each cause under Exit codes); so does a
base with no baseline file, except the one bootstrap. The one bootstrap
case is a base that predates the ratchet: no baseline file there, and the base's
copy of this wrapper exists and does not name RATCHET_MARKER; a base with no
baseline file and no copy of this wrapper fails closed. Such a run says so on a NOTE
line and holds the seed to the live counts and to each standard's UNPINNED count
at the base, computed with the same predicate and the head register from the
base tree read through git, never the working tree, so seeding cannot raise a
count. A base with this wrapper's ratchet but no baseline file fails closed, so
deleting or moving the file cannot reopen the bootstrap; a base that has the
file is always compared as above.

Every git call the ratchet makes (the work-tree and shallow checks, the refs, the base
and the parent, the commit and ancestry checks, and the tree and blob reads) goes
through one helper, _git, so git cannot substitute an object or a parent for the ones
the object ids name (round 5). Its environment is an allowlist built from nothing
(rebase revision): of the inherited variables only HOME, which git needs to find its
global configuration, is passed on (_GIT_ENV_INHERITED), and every other one is absent,
so no GIT_ variable can point git at another repository or substitute an object
(GIT_DIR, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY, GIT_REPLACE_REF_BASE and GIT_GRAFT_FILE
among them) and no LD_PRELOAD or LD_LIBRARY_PATH reaches git. To that it adds only
GIT_NO_REPLACE_OBJECTS=1 (no replace ref substitutes an object), GIT_GRAFT_FILE=/dev/null
(the repository's info/grafts, which git still honours, is not read),
GIT_CONFIG_NOSYSTEM=1 (the system configuration is not read), LC_ALL=C and the fixed
PATH below. Every call also passes
-c core.commitGraph=false, so the commit-graph file cannot substitute a commit's
parents. The helper runs git by absolute path (round 6): git is resolved once with
shutil.which on the fixed GIT_SEARCH_PATH (/usr/local/bin:/usr/bin:/bin), never the
inherited PATH, and the child's PATH is set to that same value, so a substitute git
earlier on the caller's PATH is not run; no git there fails closed naming the
searched path. A shallow file is not harmless: it can hide a commit's parents and so move
the merge base to an older commit. Before any base is computed the ratchet asks
git, through the helper (rev-parse --is-shallow-repository), and a shallow
repository fails closed with a message that the base cannot be computed in a shallow
clone and that full history must be fetched. A failing call's message shows git's
stderr without its advisory hint lines ("hint: ..." and a bare "hint:", with or
without a trailing space), so a deprecation hint cannot hide the real error.

Disclosed residuals, in this order: a local process that controls the environment
(GITHUB_ACTIONS, HOME and the global git configuration it locates, the variables the
Python interpreter reads, or any other), the git executable on GIT_SEARCH_PATH, or the
event payload (a GITHUB_EVENT_PATH file of its choosing) is not defended against,
because with HEAD these choose the base and what git reports of it; CI is the defended
path. A local caller can move or recreate refs/remotes/origin/main; edits to this
wrapper, the workflows (.github/workflows/quality.yml, nightly-sweep.yml), the runner
(tools/run_all_audits.sh) or the pre-commit invocation can change or remove the
gate, and review of such a change is the control; and the base count (of the
bootstrap and of a new register row's entry) uses the head register, so a
register edit in the same change can change which citations count.

An explicit --paths run scans a subset, so it skips the ratchet. A text run that
completes the scan (one whose status is the scan's: 0, or 1 for a blocking finding
or a "FAIL:" ratchet line) prints a NOTE line of the UNPINNED and UNREGISTERED
totals as the last line before the closing verdict line, which
tools/run_all_audits.sh shows on a pass through the runner-echo marker. A run that
stops earlier prints none: --help, a usage error, a refused --root or --paths, and
every other error status under Exit codes. A --format json run prints no NOTE line
and carries the totals in its report's inventories instead.

Exit codes. This is the one authoritative list of gate 6's exit statuses (P-3.213):
the standards-currency rule, the audit programme specification, the pack README and
the engine docstring point here (the rule and the README also name classes of exit),
so a change to an exit path updates this list and no other. Each condition names the
function it comes from. main() returns each status through the handler named, except
the argparse and lint_common.require_dir statuses, which leave main as SystemExit raised
inside it. Each listed condition is pinned by a test that asserts its status (tests/
test_linters.py, StandardsCurrencyTests and the CLI refusal tests, and tests/
test_standards_currency_coverage.py).

0  --help (argparse prints this docstring). Otherwise a run with no blocking finding
   (coverage_report's exit is 0), no "FAIL:" ratchet line and no error below; advisory
   findings and NOTE lines never change the status.

1  Blocking findings, coverage_report's status (engine):
   - a finding of the legacy Markdown stale check (check_text), in every mode;
   - an INVALID_EXCEPTION (a historical exception row that does not bind), in every mode;
   - with --coverage-mode enforce only, any other STALE, UNREGISTERED, NONCANONICAL_ID or
     UNPINNED finding.
   A "FAIL:" ratchet line (a default-scope run only; main sets report["exit"] to 1):
   - unpinned_ratchet_lines: a standard's UNPINNED count above its baseline entry (0 when
     it has none), or below it;
   - base_ratchet_lines: an entry above its base value; a new entry for a standard the
     base register already lists; a new register row's entry above that standard's
     UNPINNED count at the base; a register row removed while the base baseline records
     its entry; in the bootstrap, a seed entry above its count at the base.
   A RegisterError (main's RegisterError handler):
   - parse_register_text: a malformed or empty canonical register in the tree (a table
     row without outer pipes, an unknown header, a bad separator, a wrong cell count, an
     empty identifier or current version, a repeated identity, no entries);
   - parse_unpinned_baseline: a malformed baseline in the tree (not JSON, a repeated key,
     NaN or Infinity, no "unpinned" object, an unknown top-level key, a "_comment" that is
     not a string, a key that is not a register Standard ID, a count that is not an
     integer of at least 1);
   - parse_historical_exceptions, through historical_citation_register.load: malformed
     historical-citation exception data, or a row that fails a policy check;
   - main, through historical_citation_register.sync_problem: a register page missing
     while the data exists, or a page (with no data, one that exists) that fails the page
     checks: a generated table that differs from the data (the empty table when there is
     no data), missing or misordered sentinels, a line ending other than LF, or content
     outside the table that sync_problem refuses;
   - main: on a default run, a historical exception row naming a path outside the scan
     scope.
   Any exception main does not catch (a defect, a failed engine import, or git output of
   an unexpected shape, such as an ls-tree record base_unpinned_counts cannot split into
   three fields) ends in a Python traceback, status 1.

2  argparse (parse_args, SystemExit): a command-line usage error (an unknown option,
   --paths with no value, a --coverage-mode or --format value outside its choices).
   lint_common.require_dir (SystemExit): a --root that is empty, unreadable or
   unresolvable, or not a directory as given.
   main: an empty --paths entry.
   main's OSError and UnicodeError handler, with an "ERROR:" message and no "UNPINNED
   ratchet base" prefix, even where the cause is in the ratchet base:
   - parse_canonical_register: the canonical register missing, unreadable or not UTF-8;
   - main: the baseline in the tree missing, unreadable or not UTF-8 (a default-scope run
     only);
   - main (_read): the historical data or page unreadable for any reason but absence, or
     not UTF-8;
   - iter_files: an out-of-root scan path (within, a symlink whose target is outside the
     root included); a missing explicit path, checked before the exclusion filter; a
     directory symlink in the scan scope, as a scan root or a descendant; an entry that is
     neither a file nor a directory; an unreadable directory (os.scandir);
   - coverage_report (engine): a scanned file that is unreadable or not UTF-8;
   - ratchet_base, base_unpinned_counts: git output that is not ASCII where an object id
     or listing is read;
   - base_unpinned_counts (the bootstrap, or a new register row's entry): an OSError
     creating the temporary directory the base scope is copied into
     (tempfile.TemporaryDirectory), resolving it, or removing it afterwards; these steps
     lie outside the try block that turns a scan failure into a RatchetBaseError.
   main's RatchetBaseError handler, with an "UNPINNED ratchet base" message (a
   default-scope run only):
   - _git_executable: no git on GIT_SEARCH_PATH;
   - _git: a git call that does not run, times out (GIT_TIMEOUT) or exits non-zero;
   - _ref, _commit: a missing ref (HEAD or refs/remotes/origin/main), or a revision that
     is not a commit in the clone;
   - ratchet_base: a --root that is not the top of a git work tree; a shallow repository;
     in a pull_request run, a HEAD without exactly two parents, or a base.sha that is
     neither HEAD^1 nor an ancestor of it; in a push run, a "before" that is not a proper
     ancestor of HEAD; an Actions event other than pull_request, push, schedule and
     workflow_dispatch; zero or several merge bases of HEAD and refs/remotes/origin/main;
   - _actions_event: GITHUB_ACTIONS exactly "true" with GITHUB_EVENT_PATH unset or empty,
     or naming a file that is missing, unreadable, not UTF-8 JSON, has a repeated key, or
     is not a JSON object;
   - _payload_sha: a payload with no value at the key the event needs, or a value that is
     not a full object id (or is all zeros);
   - _blob_at: a base path that holds a tree or gitlink, or a blob that is not UTF-8;
   - base_ratchet_lines: a base with no baseline file whose copy of this wrapper is
     missing or already names RATCHET_MARKER (only a copy without the marker is the
     bootstrap); a base with a baseline file but no canonical register; a malformed or
     empty base register or a malformed base baseline (parse_register_text and
     parse_unpinned_baseline, the same checks that exit 1 in the tree);
   - base_unpinned_counts (the bootstrap, or a new register row's entry): a path in the
     base tree that is not canonical, a blob git cat-file does not return, or a base scope
     that cannot be scanned (any OSError, UnicodeError or ValueError, iter_files's
     refusals above included).

The script exits with sys.exit(main()). This list does not cover statuses the wrapper
does not choose: a SystemExit that argparse or lint_common.require_dir raises for a
condition not listed above (their codes are theirs); a broken or closed stdout (a write
that fails inside main reaches the OSError handler above, and a failed flush at
interpreter exit makes Python exit 120); a signal (SIGINT, SIGTERM and others end the
run with the signal's status or through Python's KeyboardInterrupt; Python ignores
SIGPIPE, so a broken pipe is the stdout case above); and
interpreter-level failures (an interpreter that cannot start, an import this module makes
before main runs, memory exhaustion).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from datetime import date, datetime, timezone
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import AUDITED_DOMAIN_DIRS, require_dir  # noqa: E402  # grc-config/store, stays local
import historical_citation_register as HCR  # noqa: E402  # 3b75: the register data and page sync

REPO_ROOT = Path(__file__).resolve().parent.parent
PACK_TOOLS = REPO_ROOT / ".corpus-management" / "tools"
CANONICAL_REGISTER = REPO_ROOT / "governance" / "register-canonical-citations.md"

# Files exempt from the linter (typically CHANGELOG-style records and
# discussions of the defect itself).
EXEMPT_FILES = {
    "CHANGELOG.md",
    "TODO.md",
    "TODO-REFERENCE.md",
    "governance/register-canonical-citations.md",
    ".project-governance/register-historical-citation-exceptions.md",
}

EXEMPT_DIRECTORY_PREFIXES = (
    "tools/",
    "docs/",
)

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    "CONTRIBUTING.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    # Domain run splatted from lint_common (scan-scope parity gate
    # forbids hardcoding the run).
    *AUDITED_DOMAIN_DIRS,
    # A scan root, not an exemption (3b418): #1367 added it so the default
    # run keeps checking the standards the guardrails/ pack cites after the
    # pack left dev-security/ for the root.
    "guardrails",
]


STANDARD_HEADER = [
    "Standard ID", "Current version", "Publication date",
    "Topic", "Superseded versions",
]
EVIDENCE_HEADER = ["Upstream check location", "Last verified (UTC)"]
PROJECT_HEADER = [
    "Project", "Current version", "Registration date", "Topic",
    "License", "Status notes", *EVIDENCE_HEADER,
]
HTML_ROOT = ".web/templates"

# No evidence-backed bare-publication or series exceptions approved in PR1.
BARE_EXCEPTIONS = {}

# P-3.213: the per-standard UNPINNED baseline, a checked-in source file that may only fall.
UNPINNED_BASELINE_REL = "tools/standards-currency-unpinned-baseline.json"
UNPINNED_BASELINE = REPO_ROOT / UNPINNED_BASELINE_REL
# Test seam only: the coverage-fixture tests in tests/test_standards_currency_coverage.py
# patch this to False because their in-memory trees hold no baseline. No CLI flag reaches it.
UNPINNED_RATCHET = True

# P-3.213 round 2: the baseline is also compared with its copy at a base revision.
# A base whose copy of this wrapper (at its fixed path) does not contain RATCHET_MARKER
# predates the ratchet, and only such a base with no baseline file is the bootstrap.
RATCHET_WRAPPER_REL = "tools/lint-standards-currency.py"
RATCHET_MARKER = "UNPINNED_BASELINE_REL"
CANONICAL_REGISTER_REL = "governance/register-canonical-citations.md"
# Round 3: fully qualified. Round 4: resolved exactly (_ref), so a branch or tag whose
# name is origin/main or refs/remotes/origin/main cannot stand in for it.
MAIN_REF = "refs/remotes/origin/main"
GIT_TIMEOUT = 60
# Round 6: git is found by shutil.which on this fixed PATH, never the inherited one, so a
# substitute git earlier on the caller's PATH is not run; the child's PATH is set to it too.
GIT_SEARCH_PATH = "/usr/local/bin:/usr/bin:/bin"
_GIT_EXECUTABLE = None  # resolved once, by _git_executable
# Round 6: advisory lines git prints on stderr (with GIT_GRAFT_FILE set, git 2.53 prints a
# deprecation hint); a failing call's message leaves them out so the real error shows.
# Rebase revision (D21): a bare "hint:" line, with or without a trailing space, is one too.
_GIT_HINT_PREFIX = "hint: "
_GIT_HINT_BARE = "hint:"
# Rebase revision (D21): the environment of every git call is built from nothing. These are
# the only inherited variables passed on, because git needs them to run: HOME locates the
# global configuration (where a CI checkout records safe.directory for the work tree). Every
# other inherited variable, LD_PRELOAD, LD_LIBRARY_PATH and every GIT_ variable among them
# (a pre-commit hook's GIT_DIR or GIT_INDEX_FILE, GIT_WORK_TREE, GIT_OBJECT_DIRECTORY,
# GIT_REPLACE_REF_BASE, GIT_GRAFT_FILE and the rest), is absent.
_GIT_ENV_INHERITED = ("HOME",)
# Round 5: fixed values every git call gets, whatever the caller exported; PATH is
# GIT_SEARCH_PATH (round 6) and LC_ALL is fixed (rebase revision) so git's messages are
# untranslated and its hint lines are recognised.
_GIT_ENV = {
    # No replace ref, under refs/replace/ or any other base, substitutes an object.
    "GIT_NO_REPLACE_OBJECTS": "1",
    # The repository's info/grafts, which git 2.53 still honours (GIT_NO_REPLACE_OBJECTS
    # does not stop it), is not read; an empty graft file grafts nothing.
    "GIT_GRAFT_FILE": os.devnull,
    # The system configuration file is not read.
    "GIT_CONFIG_NOSYSTEM": "1",
    "LC_ALL": "C",
    "PATH": GIT_SEARCH_PATH,
}
# Passed to every git call, so the commit-graph file cannot substitute a commit's parents.
_GIT_CONFIG = ("-c", "core.commitGraph=false")
_SHA = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")


class RatchetBaseError(Exception):
    """The ratchet base revision is undeterminable, or its register or baseline unreadable."""

# tools/run_all_audits.sh hides a passing gate's output, but shows this gate's
# WARN and NOTE lines when the output has this exact line followed by a space
# and the token run_gate passed in RUNNER_ECHO_TOKEN_ENV (the gate 72 opt-in;
# run_gate holds the same string). With the variable unset or empty (a direct
# run, the pre-commit hook, the quality.yml gate step) the line is not printed.
RUNNER_ECHO_MARKER = (
    "runner-echo: tools/run_all_audits.sh shows this gate's advisory lines on a pass"
)
RUNNER_ECHO_TOKEN_ENV = "GRC_RUNNER_ECHO_TOKEN"

# 3b75: the sanctioned historical-context form. A superseded edition cited
# as HISTORY ("the 2019 edition of ISO/IEC 27701 extended ISO/IEC
# 27001:2013") passes only through a reviewed row of the register data file:
# one path, one verbatim whole sentence, one registered superseded citation,
# a reason and upstream evidence. The two wording screens are this project's
# policy vocabulary; they refuse a present-tense claim at parse time, and the
# engine refuses a fragment of a longer sentence at scan time. An absent
# register sanctions nothing, so every stale citation keeps blocking.
HISTORICAL_REGISTER_REL = HCR.PAGE_REL  # the generated view (never parsed for policy)
HISTORICAL_DATA_REL = HCR.DATA_REL  # the rows gate 6 reads
HISTORICAL_REGISTER = REPO_ROOT / HISTORICAL_REGISTER_REL
HISTORICAL_DATA = REPO_ROOT / HISTORICAL_DATA_REL
HISTORICAL_CUE = re.compile(
    r"\b(?:superseded|replaced|withdrawn|revised|previous(?:ly)?"
    r"|former(?:ly)?|prior|earlier|original(?:ly)?|historical(?:ly)?"
    r"|until|then-current|(?:19|20)\d\d edition"
    r"|edition of (?:19|20)\d\d)\b",
    re.I,
)
PRESENT_TENSE = re.compile(
    r"\b(?:is|are|remains?|requires?|mandates?|specif(?:y|ies)|states?"
    r"|defines?|prescribes?|governs?|applies|apply|extends|covers"
    r"|includes|provides|must|shall|should|current(?:ly)?|today|now"
    # 3b75 QA r1 (claude): common present-tense verbs and "still". The screen is a vocabulary
    # heuristic on the declared text only; review of each row is the control.
    r"|still|sets|follows?|lists|contains|has|have|needs|establishes|supports|uses?"
    r"|relies|rely|anchors?|underpins?|forms?|serves?|drives?"
    r"|maps?|aligns?|underlies|implements?"
    # 3b75 QA r7 (claude): further verbs common in compliance writing.
    r"|conforms?|complies|continues?|retains?|references?|cites?|adopts?|operates?|keeps?)\b",
    re.I,
)

EXEMPT_REASONS = {
    "CHANGELOG.md": "Append-only change history.",
    "TODO.md": "Explicit defect/backlog documentation.",
    "TODO-REFERENCE.md": "Explicit defect/backlog documentation.",
    "governance/register-canonical-citations.md": "Authority parsed separately.",
    ".project-governance/register-historical-citation-exceptions.md": (
        "The generated view of the historical-citation exception data; the gate reads the .toml, and checks this page only for sync."
    ),
    "tools/": "Implementation and fixtures.",
    "docs/": "Existing explicit meta-document exemption.",
}


class RegisterError(ValueError):
    pass


def parse_register_text(text):
    lines = text.splitlines()
    entries, seen, section, i = [], {}, "(legacy fixture)", 0

    def cells(raw, line):
        raw = raw.strip()
        if not (raw.startswith("|") and raw.endswith("|")):
            raise RegisterError(
                f"register:{line}: {section}: table row needs outer pipes"
            )
        return [
            c.strip() for c in re.split(r"(?<!\\)\|", raw[1:-1])
        ]

    while i < len(lines):
        raw = lines[i]
        if raw.startswith("## "):
            section = raw[3:].strip()
        if "|" not in raw:
            i += 1
            continue

        # Every table in this authority must have a known schema.
        # A misspelled header cannot silently discard a section.
        header = cells(raw, i + 1)
        tooling = section == "AI security tooling references"
        expected = PROJECT_HEADER if tooling else (
            STANDARD_HEADER if len(header) == 5
            else STANDARD_HEADER + EVIDENCE_HEADER
        )
        if header != expected:
            raise RegisterError(
                f"register:{i + 1}: {section}: malformed header; "
                f"expected {expected!r}, got {header!r}"
            )
        if i + 1 >= len(lines):
            raise RegisterError(f"register:{i + 1}: missing separator")
        sep = cells(lines[i + 1], i + 2)
        if len(sep) != len(header) or not all(
            re.fullmatch(r":?-{3,}:?", c) for c in sep
        ):
            raise RegisterError(
                f"register:{i + 2}: {section}: malformed separator"
            )

        i += 2
        while (
            i < len(lines)
            and lines[i].strip()
            and not lines[i].startswith("#")
        ):
            row = cells(lines[i], i + 1)
            if len(row) != len(header):
                raise RegisterError(
                    f"register:{i + 1}: {section}: "
                    f"expected {len(header)} cells, got {len(row)}"
                )
            if not row[0] or not row[1]:
                raise RegisterError(
                    f"register:{i + 1}: identifier/current version required"
                )
            if not tooling:
                key = _engine().identity_key(row[0])
                if key in seen:
                    raise RegisterError(
                        f"register:{i + 1}: duplicate canonical identity "
                        f"{row[0]!r}; first at {seen[key]}"
                    )
                seen[key] = i + 1
                entries.append(dict(
                    id=row[0],
                    current=row[1],
                    superseded=[] if row[4] in {"", "-", "\u2014"} else [
                        v.strip() for v in row[4].split(",") if v.strip()
                    ],
                    superseded_raw=row[4],
                    section=section,
                    source_line=i + 1,
                    identity_key=key,
                    upstream=row[5] if len(row) == 7 else "",
                    verified=row[6] if len(row) == 7 else "",
                    cells=row,
                ))
            i += 1

    if not entries:
        raise RegisterError("canonical citations register parsed no entries")
    return entries


_HOST = re.compile(r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z](?:[a-z0-9-]*[a-z0-9])?")


def _https_evidence_url(url: str) -> bool:
    """True for an https URL naming a real-looking host; "https://#" names none (3b75 r5, codex)."""
    if not re.fullmatch(r"https://[^\s|<>`\\]+", url):
        return False
    try:
        parts = urllib.parse.urlsplit(url)
        host, port = parts.hostname, parts.port
    except ValueError:
        return False
    # No credentials on a public page, and a port, when present, is a real one (r6, claude).
    if parts.username is not None or parts.password is not None:
        return False
    if parts.netloc.endswith(":") or port == 0:
        return False
    return parts.scheme == "https" and bool(host) and bool(_HOST.fullmatch(host))


def parse_historical_exceptions(text, entries):
    """3b75: load and validate the historical-context exception DATA file (TOML).

    The rows live in a TOML data file (historical_citation_register.load applies the structural
    checks: strict TOML, exact keys, exact types, single-line printable ASCII strings); this
    function applies the policy checks to each row. The Markdown register page is a generated
    view and is never parsed for policy (maintainer ruling 2026-09-26, after ten QA rounds of
    Markdown shapes that rendered differently from what a parser read)."""
    engine, out, seen = _engine(), [], set()
    today = datetime.now(timezone.utc).date()
    try:
        rows = HCR.load(text)
    except HCR.RegisterDataError as exc:
        raise RegisterError(str(exc)) from None
    for n, row in enumerate(rows, 1):
        xid, path, citation, sentence = row["id"], row["path"], row["citation"], row["sentence"]
        reason, upstream, verified = row["reason"], row["upstream"], row["verified"]
        where = f"historical register data: exception {n}: {xid}"
        if not re.fullmatch(r"HCE-\d{3}", xid) or xid in seen:
            raise RegisterError(f"{where}: needs a unique HCE-NNN id")
        seen.add(xid)
        if (path, sentence, citation) in seen:
            # Two rows would sanction the one occurrence twice (3b75 QA r7, claude).
            raise RegisterError(f"{where}: repeats another row's path, sentence and citation")
        seen.add((path, sentence, citation))
        parts = path.split("/")
        if (
            not re.fullmatch(r"[A-Za-z0-9._/-]+\.md", path)
            or any(part in {"", ".", ".."} for part in parts)
        ):
            raise RegisterError(f"{where}: path must be a canonical repo .md path")
        occ = [
            o for o in engine.discover(citation, ".md")
            if o["channel"] == "grammar"
        ]
        if (
            len(occ) != 1
            or occ[0]["span"] != [[1, 1], [1, len(citation)]]
            or [k for k, _ in engine.resolve(
                occ[0], entries, BARE_EXCEPTIONS
            )] != ["STALE"]
        ):
            raise RegisterError(
                f"{where}: citation {citation!r} is not exactly "
                "one registered superseded edition"
            )
        if sentence.count(citation) != 1:
            raise RegisterError(
                f"{where}: sentence must contain the citation verbatim exactly once"
            )
        if not engine.SENTENCE_TEXT.fullmatch(sentence):
            raise RegisterError(
                f"{where}: sentence must be plain text (letters, digits, spaces and . , ; : ' \" "
                "( ) / % -) ending in . ! or ?; no markup, escapes or character references"
            )
        tense = PRESENT_TENSE.search(sentence)
        if tense:
            raise RegisterError(
                f"{where}: present-tense wording {tense[0]!r}; "
                "a current-tense claim cannot be sanctioned"
            )
        if not HISTORICAL_CUE.search(sentence):
            raise RegisterError(
                f"{where}: sentence carries no historical-context cue"
            )
        if len(reason) < 10 or reason.lower() in {"-", "tbd", "n/a"}:
            raise RegisterError(f"{where}: reason required")
        if not _https_evidence_url(upstream):
            raise RegisterError(
                f"{where}: upstream evidence URL required"
            )
        if verified > today:
            raise RegisterError(
                f"{where}: verified must be a date on or before today (UTC)"
            )
        out.append(dict(
            id=xid, path=path, citation=citation, sentence=sentence,
            reason=reason, identity=occ[0]["identity"],
            edition=engine.edition_key(occ[0]["version"]),
        ))
    return out


def parse_canonical_register():
    return parse_register_text(
        CANONICAL_REGISTER.read_text(encoding="utf-8")
    )


def parse_unpinned_baseline(text, entries):
    """P-3.213: the UNPINNED baseline, as {identity key: count}.

    Strict: a JSON object with an "unpinned" object and an optional "_comment"
    string, nothing else; no repeated key at any level; each key exactly a
    register Standard ID; each count an integer of at least 1 (a standard whose
    count reaches 0 leaves the file). Anything else raises RegisterError."""
    where = f"UNPINNED baseline {UNPINNED_BASELINE_REL}"

    def pairs(items):
        seen = {}
        for key, value in items:
            if key in seen:
                raise RegisterError(f"{where}: repeated key {key!r}")
            seen[key] = value
        return seen

    def constant(name):
        raise RegisterError(f"{where}: {name} is not a count")

    try:
        data = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except ValueError as exc:
        raise RegisterError(f"{where}: not valid JSON: {exc}") from None
    if not isinstance(data, dict) or not isinstance(data.get("unpinned"), dict):
        raise RegisterError(f"{where}: needs an \"unpinned\" object")
    extra = sorted(set(data) - {"unpinned", "_comment"})
    if extra:
        raise RegisterError(f"{where}: unknown key(s) {extra!r}")
    if not isinstance(data.get("_comment", ""), str):
        raise RegisterError(f"{where}: \"_comment\" must be a string")
    ids = {e["id"]: e["identity_key"] for e in entries}
    baseline = {}
    for standard, count in data["unpinned"].items():
        if standard not in ids:
            raise RegisterError(
                f"{where}: {standard!r} is not a Standard ID in the canonical register"
            )
        if type(count) is not int or count < 1:
            raise RegisterError(
                f"{where}: {standard!r} count {count!r} must be an integer of at least 1 "
                "(remove the entry when the count reaches 0)"
            )
        baseline[ids[standard]] = count
    return baseline


def unpinned_ratchet_lines(report, entries, baseline):
    """The FAIL lines of the P-3.213 UNPINNED ratchet (none when every count equals its baseline)."""
    engine = _engine()
    names = {e["identity_key"]: e["id"] for e in entries}
    over, under = engine.ratchet(engine.identity_counts(report, "UNPINNED"), baseline)
    lines = []
    for key, live, recorded in over:
        lines.append(
            f"FAIL: UNPINNED ratchet: {names.get(key, key)} has {live} unpinned citation(s), "
            f"above its baseline of {recorded} in {UNPINNED_BASELINE_REL}. Pin the edition "
            "(the register's Standard ID plus Current version) on the new citations; "
            "the baseline may only fall."
        )
    for key, live, recorded in under:
        action = (
            f"set its entry to {live}" if live else "remove its entry"
        )
        lines.append(
            f"FAIL: UNPINNED ratchet: {names.get(key, key)} has {live} unpinned citation(s), "
            f"below its baseline of {recorded}; lower the baseline: in "
            f"{UNPINNED_BASELINE_REL}, {action} in this change."
        )
    return lines


def _git_env():
    """The environment of every git call, built from nothing (rebase revision): the
    _GIT_ENV_INHERITED variables this process has, then _GIT_ENV (round 5), whose PATH is
    GIT_SEARCH_PATH (round 6). No other inherited variable is passed."""
    env = {k: os.environ[k] for k in _GIT_ENV_INHERITED if k in os.environ}
    env.update(_GIT_ENV)
    return env


def _git_hint(line):
    """True for an advisory line of git's stderr: "hint: ..." or a bare "hint:", with or
    without a trailing space (rebase revision)."""
    return line.startswith(_GIT_HINT_PREFIX) or line.rstrip(" ") == _GIT_HINT_BARE


def _git_executable():
    """The absolute path of git on GIT_SEARCH_PATH, resolved once (round 6); none there raises
    RatchetBaseError naming the searched path."""
    global _GIT_EXECUTABLE
    if _GIT_EXECUTABLE is None:
        found = shutil.which("git", path=GIT_SEARCH_PATH)
        if found is None:
            raise RatchetBaseError(f"no git executable found on {GIT_SEARCH_PATH}")
        _GIT_EXECUTABLE = os.path.abspath(found)
    return _GIT_EXECUTABLE


def _git(*args, stdin=None):
    """stdout bytes of ``<git> -C REPO_ROOT -c core.commitGraph=false <args>`` under
    _git_env(), where <git> is _git_executable()'s absolute path; any failure raises
    RatchetBaseError. Every git call the ratchet makes goes through here."""
    git = _git_executable()
    try:
        proc = subprocess.run(
            [git, "-C", str(REPO_ROOT), *_GIT_CONFIG, *args], capture_output=True,
            env=_git_env(), timeout=GIT_TIMEOUT, input=stdin,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RatchetBaseError(f"git {' '.join(args)} did not run: {exc}") from None
    if proc.returncode:
        stderr = proc.stderr.decode("utf-8", "replace")
        detail = "\n".join(
            line for line in stderr.splitlines() if not _git_hint(line)
        ).strip() or stderr.strip()
        raise RatchetBaseError(
            f"git {' '.join(args)} exited {proc.returncode}: {detail or '(no message)'}"
        )
    return proc.stdout


def _commit(rev, what):
    try:
        out = _git("rev-parse", "--verify", f"{rev}^{{commit}}")
    except RatchetBaseError as exc:
        raise RatchetBaseError(f"{what} {rev} is not a commit in this clone: {exc}") from None
    sha = out.decode("ascii", "replace").strip()
    if not _SHA.fullmatch(sha):
        raise RatchetBaseError(f"{what} {rev!r} resolved to {sha!r}, not a commit")
    return sha


def _ref(name):
    """The object id of the ref with exactly this full name (HEAD or refs/...), peeled to a
    commit. Round 4: git's ref-name lookup tries several prefixes, so a tag or branch whose
    name imitates the ref could stand in for a missing one; show-ref --verify does not."""
    try:
        out = _git("show-ref", "--verify", "--hash", name)
    except RatchetBaseError as exc:
        raise RatchetBaseError(f"the ref {name} does not exist in this clone: {exc}") from None
    sha = out.decode("ascii", "replace").strip()
    if not _SHA.fullmatch(sha):
        raise RatchetBaseError(f"the ref {name} resolved to {sha!r}, not an object id")
    return _commit(sha, f"the ref {name}")


def _actions_event(environ):
    """(event name, payload object) when GITHUB_ACTIONS is exactly "true", else None (a local run).
    Round 4: an Actions run whose GITHUB_EVENT_PATH is unset, missing, unreadable or not a
    JSON object raises RatchetBaseError; it never falls back to the local base."""
    if environ.get("GITHUB_ACTIONS") != "true":
        return None
    path = environ.get("GITHUB_EVENT_PATH", "")
    if not path:
        raise RatchetBaseError(
            "GITHUB_ACTIONS is true but GITHUB_EVENT_PATH is unset or empty, so the event "
            "payload cannot be read"
        )

    def pairs(items):
        seen = {}
        for key, value in items:
            if key in seen:
                raise ValueError(f"repeated key {key!r}")
            seen[key] = value
        return seen

    try:
        with open(path, "rb") as fh:
            payload = json.loads(fh.read().decode("utf-8"), object_pairs_hook=pairs)
    except (OSError, ValueError) as exc:
        raise RatchetBaseError(
            f"GITHUB_ACTIONS is true but the event payload at GITHUB_EVENT_PATH={path!r} is "
            f"unreadable ({exc.__class__.__name__}: {exc})"
        ) from None
    if not isinstance(payload, dict):
        raise RatchetBaseError(
            f"GITHUB_ACTIONS is true but the event payload at GITHUB_EVENT_PATH={path!r} is "
            f"not a JSON object"
        )
    return environ.get("GITHUB_EVENT_NAME", ""), payload


def _payload_sha(event, payload, *keys):
    """The commit the event payload names under ``keys``; any failure raises."""
    sha = payload
    try:
        for key in keys:
            sha = sha[key]
    except (KeyError, TypeError) as exc:
        raise RatchetBaseError(
            f"the {event} event payload names no {'.'.join(keys)} "
            f"({exc.__class__.__name__}: {exc})"
        ) from None
    if not isinstance(sha, str) or not _SHA.fullmatch(sha) or not sha.strip("0"):
        raise RatchetBaseError(
            f"the {event} event payload's {'.'.join(keys)} {sha!r} is not a commit"
        )
    return sha


def ratchet_base(environ=None):
    """(base commit, how it was chosen) for the baseline's own ratchet; the one place the
    base is selected (P-3.213 round 3).

    A run is a GitHub Actions run only when GITHUB_ACTIONS is exactly "true" and its event
    file is a readable JSON object; with GITHUB_ACTIONS exactly "true" and any other event
    file it raises. A pull_request run's base is HEAD^1 of the merge commit
    the checkout holds, read from git, and the payload's pull_request.base.sha must be that
    commit or an ancestor of it. A push run's base is the payload's "before", which must be
    a proper ancestor of HEAD. A schedule or workflow_dispatch run, and every local run,
    takes the one merge base of HEAD and MAIN_REF. Refs are resolved exactly (_ref) and
    only object ids reach later git calls. A REPO_ROOT that is not the top of a work tree, a
    shallow repository (round 6), any other Actions event, an unreadable payload, a missing
    ref or an unresolvable base raises RatchetBaseError; never falls back to the tree
    itself."""
    environ = os.environ if environ is None else environ
    try:
        top = Path(_git("rev-parse", "--show-toplevel").decode("utf-8").strip()).resolve()
    except (RatchetBaseError, UnicodeDecodeError) as exc:
        top = f"no work tree: {exc}"
    if top != REPO_ROOT.resolve():
        raise RatchetBaseError(
            f"{REPO_ROOT} is not the top level of a git work tree (git reports {top}), "
            "so no base revision can be read"
        )
    # Round 6: a shallow file can hide a parent and move the merge base to an older commit,
    # so no base is computed in a shallow clone.
    shallow = _git("rev-parse", "--is-shallow-repository").decode("ascii", "replace").strip()
    if shallow != "false":
        raise RatchetBaseError(
            f"git reports the repository as shallow ({shallow!r}), and the base cannot be "
            "computed in a shallow clone; fetch full history (git fetch --unshallow) and re-run"
        )
    actions = _actions_event(environ)
    event = actions[0] if actions else None
    head = _ref("HEAD")
    if event == "pull_request":
        claimed = _commit(_payload_sha(event, actions[1], "pull_request", "base", "sha"),
                          "the pull_request payload's base.sha")
        parents = _git("rev-list", "--parents", "-n", "1", head).decode("ascii").split()
        if len(parents) != 3:
            raise RatchetBaseError(
                f"HEAD has {len(parents) - 1} parent(s), so it is not the merge commit a "
                "pull_request run checks out and HEAD^1 is not the pull request base"
            )
        base = _commit(parents[1], "HEAD^1")
        # Round 4: the base branch may move after the event, so base.sha need only be HEAD^1
        # or an ancestor of it.
        if claimed != base and claimed not in _git(
            "merge-base", "--all", claimed, base
        ).decode("ascii").split():
            raise RatchetBaseError(
                f"the pull_request payload's base.sha {claimed} is neither HEAD^1 {base}, the "
                "first parent of the checked-out merge commit, nor an ancestor of it"
            )
        return base, "first parent of the pull request merge commit"
    if event == "push":
        before = _commit(_payload_sha(event, actions[1], "before"), "the push payload's before")
        if before == head or before not in _git(
            "merge-base", "--all", before, head
        ).decode("ascii").split():
            raise RatchetBaseError(
                f"the push payload's before {before} is not a proper ancestor of HEAD {head}"
            )
        return before, "previous tip of the pushed branch"
    if event is not None and event not in ("schedule", "workflow_dispatch"):
        raise RatchetBaseError(
            f"GitHub Actions event {event!r} has no base revision rule (pull_request, push, "
            "schedule and workflow_dispatch have one)"
        )
    main = _ref(MAIN_REF)
    merge_bases = _git("merge-base", "--all", main, head).decode("ascii").split()
    if len(merge_bases) != 1:
        raise RatchetBaseError(
            f"{MAIN_REF} and HEAD have {len(merge_bases)} merge bases, not one"
        )
    return _commit(merge_bases[0], "merge base"), f"merge base with {MAIN_REF}"


def _blob_at(rev, rel):
    """Text of ``rev:rel``, or None when the tree of ``rev`` has no entry there. Anything
    else (a tree or gitlink at that path, a git failure, bytes that are not UTF-8) raises."""
    listing = _git("ls-tree", "-z", "--full-tree", rev, "--", f":(literal){rel}")
    if not listing:
        return None
    fields = listing.split(b"\t", 1)[0].split()
    if len(fields) != 3 or fields[1] != b"blob":
        raise RatchetBaseError(f"{rel} at {rev} is not a file")
    try:
        return _git("cat-file", "blob", fields[2].decode("ascii")).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RatchetBaseError(f"{rel} at {rev} is not UTF-8: {exc}") from None


def base_unpinned_counts(rev, entries):
    """P-3.213 round 3: each standard's UNPINNED count at ``rev``, by identity key. The default
    scope's .md and .html files (and symlinks) are read from rev's tree through git, never the
    working tree, into a temporary directory and scanned with the same predicate and the head
    register, so a standard whose row is new in the change counts its citations already at
    rev (the cap on a bootstrap seed and, from round 4, on a new row's entry). Historical exceptions sanction only superseded editions, never an UNPINNED one, so
    none are applied. Any failure raises RatchetBaseError."""
    roots = [*DEFAULT_PATHS, HTML_ROOT]
    listing = _git("ls-tree", "-r", "-z", "--full-tree", rev, "--",
                   *(f":(literal){p}" for p in roots))
    blobs, links = [], []
    for record in filter(None, listing.split(b"\0")):
        meta, _, raw = record.partition(b"\t")
        mode, kind, sha = meta.decode("ascii").split()
        rel = raw.decode("utf-8", "surrogateescape")
        if any(part in {"", ".", ".."} for part in rel.split("/")):
            raise RatchetBaseError(f"{rel!r} at {rev} is not a canonical path")
        if kind == "blob" and mode == "120000":
            links.append((rel, sha))
        elif kind == "blob" and rel.endswith((".md", ".html")):
            blobs.append((rel, sha))
    wanted, link_paths = blobs + links, {rel for rel, _ in links}
    out = _git("cat-file", "--batch", stdin="".join(f"{sha}\n" for _, sha in wanted).encode())
    contents, at = [], 0
    for rel, sha in wanted:
        try:
            end = out.index(b"\n", at)
            header = out[at:end].split()
            if len(header) != 3 or header[:2] != [sha.encode("ascii"), b"blob"]:
                raise ValueError("unexpected header")
            size = int(header[2])
        except ValueError:
            raise RatchetBaseError(
                f"git cat-file did not return the blob of {rel} at {rev}"
            ) from None
        contents.append(out[end + 1:end + 1 + size])
        at = end + 2 + size
    with tempfile.TemporaryDirectory(prefix="gate6-base-") as tmp:
        root = Path(tmp).resolve()
        try:
            for (rel, _sha), data in zip(wanted, contents):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                if rel in link_paths:
                    os.symlink(os.fsdecode(data), target)
                else:
                    target.write_bytes(data)
            files = iter_files(roots, explicit=False, root=root)
            report = _engine().coverage_report(
                files, entries, repo_root=root, bare_exceptions=BARE_EXCEPTIONS,
                historical_exceptions=[],
            )
        except (OSError, UnicodeError, ValueError) as exc:
            raise RatchetBaseError(f"the default scope at {rev} cannot be scanned: {exc}") from None
    return _engine().identity_counts(report, "UNPINNED")


def base_ratchet_lines(entries, baseline, environ=None):
    """P-3.213 round 2: (FAIL or NOTE lines, base record) comparing the tree's baseline
    with the baseline at the base revision. Raises RatchetBaseError when the base is
    undeterminable or its register or baseline cannot be read (fail closed)."""
    base, how = ratchet_base(environ)
    where = f"the base revision {base[:12]} ({how})"
    record = dict(revision=base, chosen_by=how, bootstrap=False)
    text = _blob_at(base, UNPINNED_BASELINE_REL)
    if text is None:
        wrapper = _blob_at(base, RATCHET_WRAPPER_REL)
        if wrapper is None or RATCHET_MARKER in wrapper:
            raise RatchetBaseError(
                f"{where} has no {UNPINNED_BASELINE_REL}, but "
                + ("no " + RATCHET_WRAPPER_REL if wrapper is None
                   else f"its {RATCHET_WRAPPER_REL} already holds the ratchet")
                + ", so the baseline cannot be compared and this is not the bootstrap"
            )
        record["bootstrap"] = True
        # Round 3: the seed is also held to each standard's count at the base, so the
        # seeding change cannot raise a count.
        at_base = base_unpinned_counts(base, entries)
        names = {e["identity_key"]: e["id"] for e in entries}
        lines = [
            f"NOTE: UNPINNED ratchet: {where} predates the ratchet (no baseline there), so "
            "this change seeds the baseline, held to the live counts and to each "
            "standard's UNPINNED count at the base."
        ]
        for key, count in sorted(baseline.items()):
            if count > at_base.get(key, 0):
                lines.append(
                    f"FAIL: UNPINNED ratchet: the seed entry for {names.get(key, key)} is "
                    f"{count}, above its {at_base.get(key, 0)} unpinned citation(s) at "
                    f"{where}; seeding may not raise a count. Pin the edition on the new "
                    "citations instead."
                )
        return lines, record
    register = _blob_at(base, CANONICAL_REGISTER_REL)
    if register is None:
        raise RatchetBaseError(f"{where} has no {CANONICAL_REGISTER_REL}")
    try:
        base_entries = parse_register_text(register)
        recorded = parse_unpinned_baseline(text, base_entries)
    except RegisterError as exc:
        raise RatchetBaseError(f"{where}: {exc}") from None
    registered = {e["identity_key"] for e in base_entries}
    names = {e["identity_key"]: e["id"] for e in entries}
    lines, at_base = [], None
    for key, count in sorted(baseline.items()):
        if key in recorded:
            if count > recorded[key]:
                lines.append(
                    f"FAIL: UNPINNED ratchet: the baseline entry for {names.get(key, key)} "
                    f"rose from {recorded[key]} at {where} to {count}; the baseline may only "
                    "fall. Pin the edition on the new citations instead."
                )
        elif key in registered:
            lines.append(
                f"FAIL: UNPINNED ratchet: {names.get(key, key)} has a baseline entry of "
                f"{count} but none at {where}, whose register already lists it; a new "
                "entry is allowed only with the standard's new register row in the same "
                "change."
            )
        else:
            # Round 4: the new row's entry is capped as a bootstrap seed is, at the
            # standard's UNPINNED count at the base under the head register.
            if at_base is None:
                at_base = base_unpinned_counts(base, entries)
            if count > at_base.get(key, 0):
                lines.append(
                    f"FAIL: UNPINNED ratchet: the new baseline entry for {names.get(key, key)} "
                    f"is {count}, above its {at_base.get(key, 0)} unpinned citation(s) at "
                    f"{where}; a new register row may not raise a count. Pin the edition on "
                    "the new citations instead."
                )
    # Removing a register row with its entry would move the citations to the unratcheted
    # UNREGISTERED count, so a row can leave only once its entry has fallen to 0.
    current = {e["identity_key"] for e in entries}
    for key, count in sorted(recorded.items()):
        if key not in current:
            name = next(e["id"] for e in base_entries if e["identity_key"] == key)
            lines.append(
                f"FAIL: UNPINNED ratchet: the register row for {name} is removed while "
                f"{where} records {count} unpinned citation(s) of it; pin or remove those "
                "citations, and its entry, in a change that keeps the row."
            )
    return lines, record


def _engine():
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_standards_currency
    return gate_lint_standards_currency


def iter_files(paths, *, explicit=True, root=None):
    # Preserve this wrapper API for the scan-scope regression ALLOW map.
    # The shared Markdown helper remains unchanged and Markdown-only.
    # root (P-3.213 round 3) is the base revision's scope copy; None is REPO_ROOT.
    from lint_common import is_default_exempt_root, is_adopter_exempt

    root = (REPO_ROOT if root is None else root).resolve()
    selected = set()

    def within(path):
        resolved = path.resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            raise OSError(f"out-of-root scan path: {path}") from None
        return resolved

    def excluded(path):
        rel = path.relative_to(root).as_posix()
        return (
            rel in EXEMPT_FILES
            or any(rel.startswith(p) for p in EXEMPT_DIRECTORY_PREFIXES)
            or rel == ".web/dist"
            or rel.startswith(".web/dist/")
            or rel == ".web/templates-v2"
            or rel.startswith(".web/templates-v2/")
            or rel == ".web/templates-v3"
            or rel.startswith(".web/templates-v3/")
            or is_default_exempt_root(path, repo_root=root)
            or is_adopter_exempt(path, repo_root=root)
        )

    def visit(path):
        path = within(path)
        # 3b50b1: existence is checked BEFORE the exclusion filter, so a missing explicit path
        # under an excluded prefix is refused rather than silently dropped.
        if not path.exists():
            raise OSError(f"missing/unreadable intended input: {path}")
        if excluded(path):
            return
        if path.is_dir():
            # scandir surfaces unreadable-directory errors that a glob may
            # silently omit. Resolve every descendant before accepting it.
            import os
            with os.scandir(path) as children:
                for child in sorted(children, key=lambda c: c.name):
                    if child.is_symlink() and child.is_dir():
                        raise OSError(
                            f"directory symlink in scan scope: {child.path}"
                        )
                    visit(Path(child.path))
        elif path.is_file():
            rel = path.relative_to(root).as_posix()
            if path.suffix == ".md" or (
                path.suffix == ".html"
                and rel.startswith(HTML_ROOT + "/")
            ):
                selected.add(path)
        else:
            raise OSError(f"missing/unreadable intended input: {path}")

    for value in paths:
        candidate = root / value
        if candidate.is_symlink() and candidate.is_dir():
            raise OSError(
                f"directory symlink in scan scope: {candidate}"
            )
        path = within(candidate)
        if not explicit and not path.exists():
            # Sparse --root fixtures need not create every default root.
            continue
        visit(path)
    return sorted(selected)


def main(argv=None):
    global REPO_ROOT, CANONICAL_REGISTER, HISTORICAL_REGISTER, HISTORICAL_DATA
    global UNPINNED_BASELINE

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths", nargs="+", default=None)
    parser.add_argument("--root", type=str)
    parser.add_argument(
        "--coverage-mode", choices=("report", "enforce"), default="report"
    )
    parser.add_argument(
        "--format", choices=("text", "json"), default="text"
    )
    args = parser.parse_args(argv)
    if args.root is not None:  # 3b50b2d1: a missing, empty or non-directory --root is refused
        args.root = require_dir(args.root, "--root")
    if args.paths is not None and any(not p.strip() for p in args.paths):
        # 3b50b2d1: an empty --paths entry resolved to the tree root, so the run fell back to a
        # whole-tree scan while reporting an explicit scope.
        print("ERROR: --paths: an empty path entry is refused.", file=sys.stderr)
        return 2

    REPO_ROOT = (
        args.root.resolve() if args.root
        else Path(__file__).resolve().parent.parent
    )
    CANONICAL_REGISTER = (
        REPO_ROOT / "governance/register-canonical-citations.md"
    )
    HISTORICAL_REGISTER = REPO_ROOT / HISTORICAL_REGISTER_REL
    HISTORICAL_DATA = REPO_ROOT / HISTORICAL_DATA_REL
    UNPINNED_BASELINE = REPO_ROOT / UNPINNED_BASELINE_REL
    try:
        entries = parse_canonical_register()
        # The ratchet compares default-scope counts, so only a default-scope run reads the
        # baseline; it is read before the scan so a missing one fails closed at once.
        ratchet = args.paths is None and UNPINNED_RATCHET
        baseline = parse_unpinned_baseline(
            UNPINNED_BASELINE.read_bytes().decode("utf-8"), entries
        ) if ratchet else None
        # The baseline may only fall relative to the base revision (P-3.213 round 2).
        base_lines, base_record = (
            base_ratchet_lines(entries, baseline) if ratchet else ([], None)
        )
        # Read directly: only a missing file counts as absent, so a permission or other I/O
        # error reaches the exit-2 handler instead of reading as "no register" (3b75 QA, codex:
        # Path.exists() swallows OSError on Python 3.14).
        def _read(path):
            try:
                return path.read_bytes().decode("utf-8")
            except FileNotFoundError:
                return None
        data_text, page = _read(HISTORICAL_DATA), _read(HISTORICAL_REGISTER)
        historical = (
            parse_historical_exceptions(data_text, entries) if data_text is not None else []
        )
        # The page's generated table must match the data (3b75 redesign). With no data file, a
        # page that exists must show the empty table; with a data file, the page must exist.
        if data_text is not None or page is not None:
            rows = HCR.load(data_text) if data_text is not None else []
            problem = HCR.sync_problem(page, rows)
            if problem:
                raise RegisterError(problem)
        paths = (
            args.paths if args.paths is not None
            else [*DEFAULT_PATHS, HTML_ROOT]
        )
        files = iter_files(paths, explicit=args.paths is not None)
        scanned = {f.relative_to(REPO_ROOT).as_posix() for f in files}
        orphans = [h["id"] for h in historical if h["path"] not in scanned]
        if args.paths is None and orphans:
            # A default run scans every sanctioned path; a row naming an
            # unscanned path is stale policy, never a silent pass.
            raise RegisterError(
                "historical exception(s) outside the scan scope: "
                + ", ".join(orphans)
            )
        report = _engine().coverage_report(
            files,
            entries,
            repo_root=REPO_ROOT,
            mode=args.coverage_mode,
            bare_exceptions=BARE_EXCEPTIONS,
            historical_exceptions=historical,
        )
        report["scope"] = dict(
            paths=paths,
            explicit=args.paths is not None,
            exclusions=EXEMPT_REASONS,
            omitted=[
                ".web/templates-v2/", ".web/templates-v3/", ".web/dist/",
            ],
            residual=(
                "Regulations, Acts, soft law, tooling, unrecognized prose; "
                "legacy stale checks retained."
            ),
        )
        trailer = []
        if ratchet:
            trailer = base_lines + unpinned_ratchet_lines(report, entries, baseline)
            report["unpinned_ratchet"] = list(trailer)
            report["unpinned_ratchet_base"] = base_record
            if any(line.startswith("FAIL:") for line in trailer):
                report["exit"] = 1
        token = os.environ.get(RUNNER_ECHO_TOKEN_ENV, "")
        if token and args.format == "text":
            print(RUNNER_ECHO_MARKER + " " + token)
        # The summary line the runner shows on a pass; it never changes the exit status.
        trailer.append(
            "NOTE: standards-currency counts: " + _engine().count_summary(report)
        )
        _engine().print_coverage(
            report, as_json=args.format == "json", trailer=trailer
        )
        return report["exit"]
    except RatchetBaseError as exc:
        print("ERROR: UNPINNED ratchet base:", exc, file=sys.stderr)
        return 2
    except RegisterError as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1
    except (OSError, UnicodeError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
