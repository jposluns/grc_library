#!/usr/bin/env python3
"""Verify a PR that asserts it closes a TODO item also rotates it to DONE (delta gate D5).

This is the PR-time, closure-assertion half of the TODO/DONE rotation
bookkeeping-parity gate family. Its static companion is the corpus gate
"Backlog marked-done audit" (gate 57, `lint-todo-marked-done.py`), which flags
an item self-marked done IN PLACE. This check covers the case gate 57 cannot
see: a PR that CLOSES a TODO item (its commit message or CHANGELOG says so) but never edits
`.working/TODO.md` at all, so there is nothing self-marked for the static gate
to catch. That failure mode occurred in the earlier repository: the PR that
built gate 56 asserted a "closing TODO §" closure but omitted the rotation, and
the omission surfaced only in the post-merge sweep.

The rule (change-tracking PR-finalization protocol): when a PR closes a TODO
item, the item's index row is deleted from `.working/TODO.md` in THIS diff, and
the per-item detail block rotates in the private sibling and the DONE ledger in
the operational store (both cross-repo, outside the public diff). Since the
working-state move to the private sibling on 2026-07-29, the DONE ledger has
been outside the public diff (it later moved to the operational store), so this
gate enforces only the public index rotation (`.working/TODO.md` present on a
closure) surface: if a line ADDED to the root CHANGELOG, or a line of a commit
message in the PR range, asserts a TODO-item closure, or a commit message in the
range carries a ``Closes-Backlog: <id>`` trailer, the PR's changed-file set must
include `.working/TODO.md` (index row); the detail block rotates in the private
sibling, outside the public diff.

What it reads. Under the weekly-only public changelog rule, ``.working/CHANGELOG.md``
carries weekly summaries only and delta check D1 refuses a per-change line there, so
an ordinary PR adds no changelog line for this gate to read. D5 therefore reads three
sources, all from the local repository (no store and no network, so CI and the
pre-push run read the same thing): the lines the PR adds to ``.working/CHANGELOG.md``
(so a weekly-summary PR stays covered); every line of every commit message in the PR
range (merge-base to head), matched against the same closure forms; and the
structured trailer

    Closes-Backlog: <id>

one backlog id per trailer line, the id in the backlog index's own form (such as
``2.25.3``, ``P-1.2`` or ``TF-4``; ``lint_common.TODO_ID_RE``). Every
``Closes-Backlog:`` line counts as a closure assertion, even when its value is not one
id in that form (fail-closed; the failure message then says so).

Trigger (broadened 2026-06-30 to three forms, 2026-07-02 to six, 2026-07-03 to
seven, 2026-07-06 to eight, and 2026-08-01 to nine, each chosen to stay
false-positive-free; see ``CLOSURE_PATTERNS``): an added CHANGELOG line or a
commit-message line matching any of (1) the canonical section form ``clos(e|es|ed|ing) [the] TODO
§`` (e.g. "closing TODO §N.M"); (2) the coded-id major-closure marker, a
two-to-four-letter uppercase id then uppercase CLOSED (e.g. "FR-N CLOSED",
"GR-N CLOSED"; widened from the FR-only form, and note the wider id class
brushes the NIST-style control-id families, an accepted collision surface
bounded by the scan of added CHANGELOG lines and range commit messages only and
the standalone uppercase-CLOSED flag); (3) the explicit backlog-item form ``clos(e|es|ed|ing)
the <...> (backlog item | TODO item | directive | bullet(s))`` (e.g. "closes
the maintainer-directed ... validation directive", the prose-named shape;
"bullet(s)" and the decimal-dot tolerance added 2026-07-03 after a mirror
line's "Closes the ... bullets" in the earlier repository evaded the noun set
AND the intervening "section-N.M" token's dots blocked the clause run); (4) the
section-name closure form ``section-N.M <...> clos(ed|ure)`` (e.g. "the
section-N.M remainder closed"); (5) the item-number closure form ``item(s) N
[and M ...] closed`` (e.g. "items N and M closed"); or (6) the
rotation-assertion form ``rotated to [the] DONE [ledger]`` (a line claiming the
rotation happened must be accompanied by the rotation surfaces in the diff; the
short "rotated to DONE" variant added 2026-07-03, with a not-negation guard so
"NOT rotated to DONE" narration stays exempt, the two negation lines the
earlier repository's census surfaced; widened again 2026-07-06 with a
markdown-linked DONE target ``rotated to [`.working/DONE.md`](...)``, a shape
the literal missed); (7) the space-separated TODO-section closure form ``TODO
section N.M <...> clos(ed|ure)`` (case-insensitive, forward-only window; e.g.
"TODO section N.M is CLOSED", a lead line in the earlier repository that evaded
forms 1, 4, and 6; the ``TODO `` anchor keeps it out of the bare-"section" FP
space the earlier repository's census rejected); or (8) the bare TODO-section
closure form ``TODO N.M <...> clos(ed|ure)`` (a decimal section token with NO
"section" word and NO `§`, case-insensitive, forward-only; e.g. "TODO N.M ...
closed", a lead line in the earlier repository that evaded forms 1 and 7; added
2026-07-06, when that repository's full-history census found 16 hits, all
genuine, 0 negation FPs); or (9) the verb-first bare TODO-section closure form
``clos(e|es|ed|ing) [the] TODO N.M`` (the clos-FIRST word order, the mirror of
forms 7 and 8 and the decimal analogue of form 1; e.g. "Closes TODO N.M"; added
2026-08-01 after the eight prior forms were found to pass this phrasing
vacuously; the earlier repository's full-history census found 29 matches, 28
same-PR closures plus one re-added prior closure line (a prior PR's closure
entry re-touched in a later PR's commit and masked by that PR's own rotation,
the re-add class every form shares), 0 genuine past-narration FPs; the rare
quoting-a-prior-PR case uses the TodoRotation: opt-out, as form 1 does). Forms
4 to 6 were added 2026-07-02 after a pre-push verifier in the earlier
repository showed that a PR's section-and-item closure phrasings passed the
gate vacuously. It does NOT match incidental mentions ("closing the #N
finding", "TODO §N.M updated", "per FR-N"), and it deliberately does NOT match
bare lowercase ``Closes FR-N``: that form matched ~95 of the earlier
repository's historical CHANGELOG lines including past-closure narration ("PR
#N closed FR-N", "PRs #N-#M closing FR-N/..."), which would false-fail a
standing PR-time gate; the close-out-checklist convention and the static
marked-done gate cover that residual. The 2026-06-30 broadening was driven by a
miss in the earlier repository (a prose-named "OT post-ingestion validation"
item closed without rotation, invisible to the old ``TODO §``-only trigger).

Opt-out / exemption: any commit in the PR range carrying a

    TodoRotation: <one-line-reason>

trailer satisfies the gate. This covers (a) a CHANGELOG entry or commit message that
NARRATES a past closure (e.g. quoting "closing TODO §X" while describing a prior PR), which
would otherwise false-trigger, and (b) the session-closing handoff-PR case (the
shared handoff-exemption logic of the bookkeeping-parity gate family). The
trailer is a one-line ``Key: reason`` commit trailer read from any commit in the PR range.

Coverage kept across the weekly-only changelog. At main d7387bf3 D5 read its nine
closure forms and its opt-out against the lines a PR added to the CHANGELOG; an
ordinary PR now adds none, so each case is caught on a commit message of the PR range
(no changelog line added) and, for a weekly-summary PR, on an added summary line. The
cases are tested in TodoRotationOnPrDeltaTests (tests/test_linters.py). Switching off
closure reading from commit messages (the TodoRotation: trailer still read) is expected
to fail every case there whose closure, the Closes-Backlog: trailer included, is stated
only in a commit message, and no case whose closure is an added changelog line; that set
is held once as FAIL_WITHOUT_COMMIT_MESSAGE_READING in that class, where a test derives
it by running the cases with that reading off and asserts the two are equal. No case is
left uncovered. What the move changes is stated under Known residuals.

Usage:
    # In CI (uses GITHUB_BASE_REF):
    python3 .claude/skills/corpus-management/tools/check-todo-rotation-on-pr.py

    # Locally, comparing HEAD to a specific base:
    python3 .claude/skills/corpus-management/tools/check-todo-rotation-on-pr.py origin/main
    python3 .claude/skills/corpus-management/tools/check-todo-rotation-on-pr.py origin/main HEAD

Exit codes:
    0 : no closure assertion in the added CHANGELOG lines or in the commit messages of
        the PR range, OR .working/TODO.md is in the diff (the public index rotated), OR
        an opt-out trailer is present.
    1 : a closure is asserted but .working/TODO.md is missing from the diff (the public
        index row was not rotated).
    2 : invocation or environment error (cannot determine base/head, git failure,
        a work tree top level git reports that is not this script's own
        repository, REPO_ROOT: another directory, or a relative or empty one,
        a git directory other than REPO_ROOT's own, as GIT_DIR naming
        another repository gives, GIT_COMMON_DIR, GIT_OBJECT_DIRECTORY,
        GIT_ALTERNATE_OBJECT_DIRECTORIES, GIT_GRAFT_FILE or GIT_SHALLOW_FILE
        in the environment, or GIT_WORK_TREE or GIT_INDEX_FILE pointing away
        from REPO_ROOT, a REPO_ROOT that is not a work tree registered with
        the git directory git reads, as a .git file naming another
        checkout's gives, or a relocated objects directory or a
        git-new-workdir checkout (objects, refs or reftable that are
        symbolic links), or a separate git directory that sets no
        core.worktree, as git init or git clone --separate-git-dir leaves
        one: in that checkout run git config core.worktree "$PWD"), or
        CANNOT-EVALUATE: base and head resolve to the same commit, or the
        range changes no file (an empty diff), so nothing was evaluated.

Known residuals: the nine closure forms were census-tested against changelog history,
not commit-message history, so a commit message that narrates a past closure in one of
those forms fails until a TodoRotation: trailer opts out; a closure stated only in a
pull request's title or description, never in a commit message or an added changelog
line, is not read (a squash merge's message is written after this gate runs). Git
failing to run at all (OSError) on the one
top-level read degrades to a placeholder and skips the top-level comparison
(the git-directory checks still run). D5 runs git from the current
directory, so it also refuses (fail-closed) where git's top level is not this
copy's REPO_ROOT although nothing is misread: the main checkout's copy run
from inside a linked worktree or a submodule, and this copy run from a
subdirectory while GIT_DIR is exported (git then takes the current directory
as the top level). The runner, CI and git hooks all run it from the top level.
What the git-directory checks do not cover is disclosed in
lint_common.require_own_git_dir.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import REPO_ROOT, TODO_ID_RE, require_own_git_dir, resolve_base_ref  # noqa: E402

CHANGELOG_PATHS = (".working/CHANGELOG.md",)
TODO_PATH = ".working/TODO.md"
# 2026-08 migration: the per-item detail file (TODO-REFERENCE.md) moved to the private
# sibling, so a PUBLIC closure only rotates the .working/TODO.md INDEX row; the detail block and the
# DONE ledger rotate privately (cross-repo, invisible to the public diff). Retained for the
# docstring/reference; the check now requires only .working/TODO.md.

# The DONE ledger (.working/DONE.md) moved to the private sibling on 2026-07-29
# and now lives in the operational store, so it is a cross-repo surface invisible to a public
# PR diff. This gate therefore requires the PUBLIC rotation surface: the .working/TODO.md index-row
# edit (the per-item detail block rotates in the private sibling, cross-repo, outside this diff).
# (The closure-assertion scan reads the lines a PR adds to the root .working/CHANGELOG.md and
# the commit messages of the PR range; the detailed mirror is private.)


# Closure-assertion phrasings, broadened 2026-06-30 beyond the original `TODO §`
# form to also catch the prose-named and FR-N closures a miss in the earlier
# repository exposed, again 2026-07-02 (forms 4 to 6, after section-and-item
# phrasings passed vacuously), again 2026-07-03 (form 7, after another miss in
# the earlier repository), and again 2026-07-06 (form 8 and the form-6
# markdown-link widening), while staying false-positive-free. The nine forms
# below were chosen empirically: tested against the earlier repository's entire
# CHANGELOG history (root + detailed mirror, ~14k lines), each matched only
# genuine current-PR closures with ZERO past-closure-narration false positives. A
# bare lowercase `Closes FR-N` is deliberately NOT matched: it matched ~95 lines
# including past-closure narration ("PR #N closed FR-N", "PRs #N-#M closing
# FR-N/..."), exactly the standing-gate false-fire the original narrow design
# avoided; the close-out-checklist convention covers that residual. A generalized
# "clos... the section" form was census-tested in the earlier repository for the
# 2026-07-02 widening and REJECTED on two historical false positives there; the
# shipped section form requires the hyphenated `section-N.M` token instead.
CLOSURE_PATTERNS = (
    # (1) the canonical section form: a closure verb, optional "the", then "TODO §".
    re.compile(r"\bclos(?:e|es|ed|ing)\b\s+(?:the\s+)?TODO\s+§", re.IGNORECASE),
    # (2) the distinctive major-closure marker "FR-N CLOSED", widened from the
    # FR-only form to any two-to-four-letter uppercase coded id (FR/GR/SR and
    # future families): GR-coded items in the earlier repository showed a coded
    # closure the FR-only pattern was blind to. Uppercase CLOSED stays the
    # deliberate this-PR-closure flag; case-sensitive so lowercase "closed FR-N"
    # / "GR-N closed" narration does not match. Empirically FP-free: in the
    # earlier repository's whole CHANGELOG history the widened form matched
    # exactly the same four genuine FR-N CLOSED instances the old one did.
    re.compile(r"\b[A-Z]{2,4}-\d+\s+CLOSED\b"),
    # (3) the prose-named / explicit backlog-item form: a closure verb, "the", then
    # (within one clause) "backlog item" / "TODO item" / "directive". This catches
    # "closes the maintainer-directed ... validation directive" (the prose-named
    # miss in the earlier repository) and "closes the ... backlog item". The
    # tempered run forbids a SECOND "the": a second "the" signals a new noun phrase
    # or a prepositional object ("closing the gap per the maintainer directive"),
    # where the trailing item/directive word is NOT the closure's direct object, so
    # it is excluded as a false positive. The run admits a dot ONLY between digits
    # (a decimal / section token such as "section-1.2" or "§5.3") while a
    # sentence-ending period still terminates the clause: the earlier repository's
    # 2026-07-03 census showed the plain [^.\n] run could never match a closure
    # whose intervening text carries a section number (two genuine historical
    # closures were invisible). "bullet(s)" joins the noun set (the mirror-line
    # evasion); the widened form's census of that repository found three new hits,
    # all true positives, zero false positives.
    re.compile(
        r"\bclos(?:e|es|ed|ing)\b\s+the\s+(?:(?!\bthe\b)(?:[^.\n]|(?<=\d)\.(?=\d))){0,70}?\b(?:backlog item|TODO item|directive|bullets?)\b",
        re.IGNORECASE,
    ),
    # (4) the section-name closure form: a hyphenated `section-N.M` token then
    # (within one clause) a closed/closure word. The hyphenated token is the FP
    # guard: the generalized "clos... the section" form was census-tested in the
    # earlier repository and rejected on two historical false positives there.
    # Case-sensitive, matching the censused form.
    re.compile(r"\bsection-\d+\.\d+(?:[^.\n]){0,80}?\bclos(?:ed|ure)\b"),
    # (5) the item-number closure form: "item(s) N [and M ...] closed", the
    # multi-item shape ("items N and M closed"). The character class between
    # the numbers and "closed" admits only digits, punctuation, and
    # whitespace, so narration like "items 4-7 remain deferred, not closed"
    # cannot match. Case-sensitive, matching the censused form.
    re.compile(r"\bitems?\s+\d[\d.,\s\-]*(?:and\s+[\d.,\s\-]+)*closed\b"),
    # (6) the rotation-assertion form: a line claiming the rotation itself
    # happened. If the claim is true the gate passes trivially (both surfaces
    # are in the diff); a line NARRATING a past PR's rotation is covered
    # by the TodoRotation: opt-out trailer, the same escape hatch as
    # form 1. Widened 2026-07-03 with the short "rotated to DONE" variant
    # (22 census hits in the earlier repository: 20 genuine same-PR
    # rotation assertions, 2 negations); the fixed-width not-lookbehind
    # excludes the negation narration ("is NOT rotated to DONE") the census
    # surfaced. Widened again 2026-07-06 with a markdown-linked DONE target
    # (``[`.working/DONE.md`](...)``), the "rotated to [linked path]" shape
    # that defeated the literal; the earlier repository's full-history
    # census found 64 genuine linked rotation assertions and 0 bug-matches,
    # and the not-negation guard still fronts the whole clause.
    re.compile(r"(?<![Nn][Oo][Tt] )\brotated to (?:the DONE ledger|DONE\b|\[`?[^\]]*DONE)"),
    # (7) the space-separated TODO-section closure form: the literal token "TODO
    # section N.M" then (within one clause, forward-only) a closed/closure word.
    # Added 2026-07-03 after a root lead line in the earlier repository (`"TODO
    # section N.M is CLOSED and rotated to [a linked path]"`) matched none of the
    # six forms: form 1 wants a `§`, form 4 wants the hyphenated `section-N.M`,
    # and the rotation clause's markdown link defeated form 6's literal "rotated
    # to DONE". The `TODO ` anchor is the FP guard that the generalized
    # bare-"section" form, which the earlier repository's census rejected,
    # lacked: that repository's full-history census found exactly 4 hits (the
    # root lead lines of two PRs plus two mirror lines of the second; the first
    # PR's mirror carried no such token), all genuine same-PR closures, 0 false
    # positives; the forward-only window correctly excludes past-closure
    # narration where the closure word PRECEDES the token ("the closed TODO
    # section N.M reworded"). Case-insensitive so the emphatic "is CLOSED"
    # matches; the clause run admits a dot only between digits, as in form 3.
    re.compile(
        r"\bTODO section \d+\.\d+(?:[^.\n]|(?<=\d)\.(?=\d)){0,80}?\bclos(?:ed|ure)\b",
        re.IGNORECASE,
    ),
    # (8) the bare TODO-section closure form: the literal token "TODO N.M" (a
    # decimal section number, NO "section" word and NO `§`) then (within one
    # clause, forward-only) a closed/closure word. Added 2026-07-06 after a
    # lead line's "TODO N.M ... closed" phrasing in the earlier repository
    # matched none of forms 1-7 (form 1 wants `§`, form 7 wants the "section"
    # word). The `TODO ` anchor plus the decimal token is the FP guard, and
    # the forward-only window (closure word AFTER the token) excludes
    # past-closure narration; the earlier repository's full-history census
    # found 16 hits, all genuine same-PR closures, 0 negation false positives.
    # The clause run admits a dot only between digits (as in forms 3 and 7);
    # case-insensitive for "is CLOSED".
    re.compile(
        r"\bTODO \d+\.\d+(?:[^.\n]|(?<=\d)\.(?=\d)){0,80}?\bclos(?:ed|ure)\b",
        re.IGNORECASE,
    ),
    # (9) the verb-first bare TODO-section closure form: a closure verb, optional
    # "the", then the literal token "TODO N.M" (a decimal section number, NO "section"
    # word and NO `§`). This is the clos-FIRST word order (e.g. "Closes TODO N.M"),
    # the mirror of forms 7/8 (which are token-first) and the exact decimal analogue
    # of form 1 ("clos... TODO §"). Added 2026-08-01 after the eight prior forms were
    # found to pass "Closes TODO N.M" phrasing VACUOUSLY (form 1 wants `§`; forms 7/8
    # want the TODO token to PRECEDE the closure verb). The earlier repository's
    # full-history census: 29 matches, 28 same-PR closures ("Closes/closed/closing
    # [the] TODO N.M") plus one re-added prior closure line (a prior PR's closure
    # entry re-touched in a later PR's commit, masked by that PR's own rotation, the
    # re-add class EVERY closure form shares and the TodoRotation: opt-out covers), 0
    # genuine past-narration or incidental false positives (the earlier repository's
    # CHANGELOG never wrote "PR #N closed TODO N.M" narration in this contiguous form;
    # its past-closure narration used the FR-id shape instead). Like form 1, the rare
    # quoting-a-prior-PR case is handled by the TodoRotation: opt-out trailer.
    # Case-insensitive for "Closes"/"CLOSES".
    re.compile(r"\bclos(?:e|es|ed|ing)\b\s+(?:the\s+)?TODO\s+\d+\.\d+", re.IGNORECASE),
)

TRAILER_PATTERN = re.compile(
    r"^\s*TodoRotation:\s*(\S.*?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# The structured closure trailer: one backlog id per trailer line. Any value counts as a
# closure assertion (fail-closed); TODO_ID_RE only words the failure message.
CLOSES_BACKLOG_PATTERN = re.compile(
    r"^[ \t]*Closes-Backlog:[ \t]*(.*?)[ \t]*$",
    re.IGNORECASE | re.MULTILINE,
)


def asserts_todo_closure(added_lines: list[str]) -> str | None:
    """Return the first added line that asserts a TODO-item closure, or None.

    Pure helper (no git), unit-tested directly: this is the false-positive-
    critical part of the gate.
    """
    for line in added_lines:
        if any(pat.search(line) for pat in CLOSURE_PATTERNS):
            return line
    return None


def commit_message_closure(messages: list[tuple[str, str]]) -> tuple[str, str] | None:
    """Return ``(sha, line)`` for the first commit message that asserts a TODO-item closure.

    ``messages`` holds ``(sha, full message)`` pairs of the PR range. A message asserts a
    closure when it carries a ``Closes-Backlog:`` trailer line or when any of its lines
    matches ``CLOSURE_PATTERNS``. Pure helper (no git), unit-tested directly.
    """
    for sha, body in messages:
        trailer = CLOSES_BACKLOG_PATTERN.search(body)
        if trailer:
            return sha, trailer.group(0).strip()
        line = asserts_todo_closure(body.splitlines())
        if line is not None:
            return sha, line
    return None


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def added_changelog_lines(merge_base: str, head: str) -> list[str]:
    """The '+' lines (added content, not '+++' headers) of the CHANGELOG diff."""
    try:
        diff = git("diff", merge_base, head, "--", *CHANGELOG_PATHS)
    except subprocess.CalledProcessError:
        return []
    out: list[str] = []
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            out.append(line[1:])
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check that a PR asserting a TODO-item closure also rotates the "
            "item (touches the .working/TODO.md index row; the detail rotates privately)."
        ),
    )
    parser.add_argument("base", nargs="?", help="Base ref (default: origin/$GITHUB_BASE_REF in CI).")
    parser.add_argument("head", nargs="?", default="HEAD", help="Head ref (default: HEAD).")
    args = parser.parse_args(argv[1:])

    base = args.base
    if not base:
        github_base = os.environ.get("GITHUB_BASE_REF")
        if not github_base:
            print(
                "ERROR: base ref not provided and GITHUB_BASE_REF is unset. "
                "Pass a base ref as the first positional argument when running "
                "locally (e.g. origin/main).",
                file=sys.stderr,
            )
            return 2
        base = f"refs/remotes/origin/{github_base}"
    head = args.head
    # A short name such as origin/main is read from <git-dir>/origin/main
    # before refs/remotes, so it is resolved unambiguously first, and the
    # default above is fully qualified.
    base, refusal = resolve_base_ref(base, REPO_ROOT, from_cwd=True)
    if refusal:
        print(f"ERROR: {refusal}.", file=sys.stderr)
        return 2

    try:
        merge_base = git("merge-base", base, head)
    except subprocess.CalledProcessError as exc:
        print(
            f"ERROR: could not determine merge-base of {base}..{head}: {exc}. "
            f"In GitHub Actions, ensure that actions/checkout uses fetch-depth: 0.",
            file=sys.stderr,
        )
        return 2
    except OSError as exc:
        # git that cannot be started at all (not on PATH, or not executable)
        # exited 1, D5's own missing-rotation FAIL code, with a traceback; it
        # refuses instead, naming the error, as D13 does.
        print(f"ERROR: git could not be run to find the merge base (base={base}, head={head}): "
              f"{exc}", file=sys.stderr)
        return 2
    except UnicodeDecodeError as exc:
        # Defence in depth: git() captures only standard output and
        # merge-base prints object names, so no known input reaches this; if
        # git's output ever fails to decode, refuse, naming the error, as D13 does.
        print(f"ERROR: git's output could not be decoded finding the merge base "
              f"(base={base}, head={head}): {exc}", file=sys.stderr)
        return 2

    # D5 keeps its own resolution flow (see lint_common's hoist note), so it
    # carries its own copy of the collapsed-range refusal: a base and head
    # resolving to the same commit is how a run from the wrong repository (a
    # main clone while the change lives in a worktree) looks, and it must
    # never read as a clean pass.
    try:
        head_sha = git("rev-parse", "--verify", f"{head}^{{commit}}")
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: could not resolve {head} to a commit: {exc}", file=sys.stderr)
        return 2
    try:
        # The refusals' repo= field and the comparison below: git failing to
        # run at all (OSError) degrades to a placeholder as D12's _toplevel
        # does, so the gate keeps its real verdict instead of a traceback.
        # The top level is read as bytes and decoded with os.fsdecode, so a
        # path that is not valid UTF-8 still reaches the comparison instead
        # of the placeholder. git refusing to print one (no work tree, as
        # with GIT_DIR naming a bare repository) still refuses with exit 2.
        toplevel = os.fsdecode(subprocess.check_output(["git", "rev-parse", "--show-toplevel"])).strip()
    except OSError:
        toplevel = "(no work tree)"
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: could not read the work tree top level: {exc}", file=sys.stderr)
        return 2
    else:
        if not toplevel:
            # git older than 2.25 printed nothing and exited 0 outside a work tree
            # instead of refusing, so an empty top level is the same missing work
            # tree and refuses the same way on any git.
            print("ERROR: could not read the work tree top level: git rev-parse "
                  "--show-toplevel printed an empty top level (no work tree).", file=sys.stderr)
            return 2
        # A top level other than this script's own REPO_ROOT means git is
        # reading another repository (GIT_DIR naming a bare clone plus
        # GIT_WORK_TREE naming another directory, or a run of this copy from
        # inside a different clone); refuse it, as D9 does. Path resolves a
        # relative top level against the current directory, so it must also
        # be absolute, as git always prints it. The placeholder above
        # skips this check.
        top = Path(toplevel)
        if not (top.is_absolute() and top.resolve() == REPO_ROOT.resolve()):
            print(
                f"ERROR: git reports the work tree top level {toplevel!r}, not this "
                f"script's repository {REPO_ROOT}; run the copy of this script inside "
                f"the tree under test.",
                file=sys.stderr,
            )
            return 2
    # A top level of REPO_ROOT does not show that git reads REPO_ROOT's
    # repository (GIT_DIR naming another one, with the current directory or
    # GIT_WORK_TREE as the top level, still reports it), so compare the git
    # directories too, as D9 does.
    refusal = require_own_git_dir(REPO_ROOT, from_cwd=True)
    if refusal:
        print(f"ERROR: {refusal}.", file=sys.stderr)
        return 2
    if merge_base == head_sha:
        print(
            f"CANNOT-EVALUATE: base {base} and head {head} resolve to the same "
            f"commit (repo={toplevel} base={merge_base} head={head_sha}); the "
            f"named range is empty, so nothing was evaluated. If the change "
            f"lives in a worktree, run from that worktree, or pass a "
            f"base..head range that selects the change.",
            file=sys.stderr,
        )
        return 2

    try:
        changed = [ln for ln in git("diff", "--name-only", merge_base, head).splitlines() if ln]
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    if not changed:
        print(
            f"CANNOT-EVALUATE: refs were named but no files changed in the range "
            f"(repo={toplevel} base={merge_base} head={head} -> {head_sha}); "
            f"nothing was evaluated.",
            file=sys.stderr,
        )
        return 2

    # The commit messages of the PR range are read on every run: since the weekly-only
    # public changelog they are where an ordinary PR states a closure, and they carry the
    # opt-out trailer. Only the local repository is read (no store, no network).
    try:
        commit_shas = git("log", "--format=%H", f"{merge_base}..{head}").splitlines()
        messages = [(sha, git("log", "-1", "--format=%B", sha)) for sha in commit_shas]
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git log failed: {exc}", file=sys.stderr)
        return 2
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: the commit messages of {merge_base}..{head} could not be read: {exc}",
              file=sys.stderr)
        return 2

    closure_line = asserts_todo_closure(added_changelog_lines(merge_base, head))
    source = "an added CHANGELOG line"
    if closure_line is None:
        found = commit_message_closure(messages)
        if found is not None:
            source = f"the message of commit {found[0][:8]}"
            closure_line = found[1]
    if closure_line is None:
        print("OK: no TODO-item closure asserted in the added CHANGELOG lines or in the "
              "commit messages of the PR range.")
        return 0

    # 2026-08 migration: the per-item DETAIL (TODO-REFERENCE.md) is PRIVATE now,
    # so a public closure touches only the .working/TODO.md INDEX row; the detail block
    # rotates in the private sibling and the DONE ledger in the operational store
    # (cross-repo, not in this diff).
    missing_rotation = [p for p in (TODO_PATH,) if p not in changed]
    if not missing_rotation:
        print(
            f"OK: {source} asserts a TODO-item closure and {TODO_PATH} is in the diff "
            f"(the public index row rotated); the item's detail block rotates in the private "
            f"sibling and the DONE ledger in the operational store (cross-repo, not in the public diff)."
        )
        return 0

    # Closure asserted but a rotation surface is missing: check the opt-out trailer.
    for sha, body in messages:
        match = TRAILER_PATTERN.search(body)
        if match:
            print(
                f"OK: commit {sha[:8]} carries opt-out trailer: "
                f"'TodoRotation: {match.group(1)}'."
            )
            return 0

    print(
        f"FAIL: {source} asserts a TODO-item closure but the diff "
        f"does not rotate the public index: {' and '.join(missing_rotation)} not in the diff. "
        f"A closure deletes the item's index row from {TODO_PATH} (the detail block rotates "
        f"in the private sibling).",
        file=sys.stderr,
    )
    print(f"  asserting line: {closure_line.strip()[:160]}", file=sys.stderr)
    trailer = CLOSES_BACKLOG_PATTERN.fullmatch(closure_line.strip())
    if trailer and not TODO_ID_RE.match(trailer.group(1)):
        print("  (its value is not one backlog id in the index's form; it still counts as "
              "a closure assertion)", file=sys.stderr)
    print("", file=sys.stderr)
    print(
        "When a PR closes a TODO item, delete its index row from .working/TODO.md (the "
        "change-tracking rotation discipline; the per-item detail block lands in the private "
        "sibling and the paired DONE ledger row in the operational store, cross-repo and not "
        "in the public diff). If "
        "the line merely narrates a past closure, add a 'TodoRotation: <reason>' "
        "trailer to any commit to opt out.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
