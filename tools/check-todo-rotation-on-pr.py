#!/usr/bin/env python3
"""Verify a PR that asserts it closes a TODO item also rotates it to DONE (delta gate D5).

This is the PR-time, CHANGELOG-asserts-closure half of the §4.10 TODO/DONE
rotation bookkeeping-parity gate family. Its static companion is the corpus
gate "Backlog marked-done audit" (gate 57, `lint-todo-marked-done.py`), which
flags an item self-marked done IN PLACE. This check covers the case gate 57
cannot see: a PR that CLOSES a TODO item (its CHANGELOG says so) but never
edits `TODO.md` at all, so there is nothing self-marked for the static gate to
catch. That is the #466 failure mode (it built gate 56 "closing TODO §4.5 S4"
but omitted the rotation; the omission surfaced only in the post-merge sweep).

The rule (change-tracking PR-finalization protocol): when a PR closes a TODO
item, the item is deleted from `TODO.md` and an entry is added to
`.working/DONE.md` in the SAME diff. This gate enforces that mechanically at PR
time: if any line ADDED to the CHANGELOG (root or detailed mirror) asserts a
TODO-item closure, the PR's changed-file set must include BOTH `TODO.md` and
`.working/DONE.md`.

Trigger (broadened 2026-06-30 to three forms, 2026-07-02 to six, and
2026-07-03 to seven, each chosen to stay false-positive-free; see
``CLOSURE_PATTERNS``): an added CHANGELOG line matching
any of (1) the canonical section form ``clos(e|es|ed|ing) [the] TODO §`` (e.g.
"closing TODO §4.5 S4"); (2) the coded-id major-closure marker, a
two-to-four-letter uppercase id then uppercase CLOSED (e.g. "FR-58 CLOSED",
"GR-13 CLOSED"; widened from the FR-only form by GR-13, and note the wider id
class brushes the NIST-style control-id families, an accepted collision
surface bounded by the added-CHANGELOG-lines-only scan and the standalone
uppercase-CLOSED flag); (3) the explicit backlog-item form
``clos(e|es|ed|ing) the <...> (backlog item | TODO item | directive | bullet(s))``
(e.g. "closes the maintainer-directed ... validation directive", the #495
prose-named shape; "bullet(s)" and the decimal-dot tolerance added 2026-07-03
after the #592 mirror's "Closes the ... bullets" evaded the noun set AND the
intervening "section-3.14" token's dots blocked the clause run); (4) the section-name closure form ``section-N.M <...> clos(ed|ure)``
(e.g. "the section-3.14 remainder closed"); (5) the item-number closure form
``item(s) N [and M ...] closed`` (e.g. "items 11 and 12 closed"); or (6) the
rotation-assertion form ``rotated to [the] DONE [ledger]`` (a line claiming
the rotation happened must be accompanied by the rotation surfaces in the
diff; the short "rotated to DONE" variant added 2026-07-03, with a
not-negation guard so "NOT rotated to DONE" narration stays exempt, the two
historical negation lines the census surfaced); or (7) the space-separated
TODO-section closure form ``TODO section N.M <...> clos(ed|ure)``
(case-insensitive, forward-only window; e.g. "TODO section 1.1 is CLOSED",
the #607 lead that evaded forms 1, 4, and 6; the ``TODO `` anchor keeps it
out of the census-rejected bare-"section" FP space).
Forms 4 to 6 were added 2026-07-02 after the #563 pre-push verifier showed
that #567's section-and-item closure phrasings passed the gate vacuously.
It does NOT match incidental mentions ("closing the #466 finding",
"TODO §4.10 updated", "per FR-154"), and it deliberately does NOT match bare
lowercase ``Closes FR-N``: that form matched ~95 historical CHANGELOG lines
including past-closure narration ("PR #143 closed FR-9", "PRs #221-#228 closing
FR-33/82/..."), which would false-fail a standing PR-time gate; the
close-out-checklist convention and the static marked-done gate cover that
residual. The 2026-06-30 broadening was driven by the #495 miss (a prose-named
"OT post-ingestion validation" item closed without rotation, invisible to the
old ``TODO §``-only trigger).

Opt-out / exemption: any commit in the PR range carrying a

    TodoRotation: <one-line-reason>

trailer satisfies the gate. This covers (a) a CHANGELOG entry that NARRATES a
past closure (e.g. quoting "closing TODO §X" while describing a prior PR), which
would otherwise false-trigger, and (b) the session-closing handoff-PR case (the
shared handoff-exemption logic of the bookkeeping-parity gate family). The
trailer is the same proven shape as the ``Changelog:`` opt-out of delta gate D1.

Usage:
    # In CI (uses GITHUB_BASE_REF):
    python3 tools/check-todo-rotation-on-pr.py

    # Locally, comparing HEAD to a specific base:
    python3 tools/check-todo-rotation-on-pr.py origin/main
    python3 tools/check-todo-rotation-on-pr.py origin/main HEAD

Exit codes:
    0 : no closure assertion in the added CHANGELOG lines, OR both TODO.md and
        DONE.md are in the diff, OR an opt-out trailer is present, OR empty diff.
    1 : a closure is asserted but TODO.md and/or .working/DONE.md is missing.
    2 : invocation or environment error (cannot determine base/head, git failure).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

CHANGELOG_PATHS = ("CHANGELOG.md", ".working/changelog-details/CHANGELOG-detailed.md")
TODO_PATH = "TODO.md"
DONE_PATH = ".working/DONE.md"

# Closure-assertion phrasings, broadened 2026-06-30 (the rotation-prevention
# backlog item, since closed) beyond the original `TODO §` form to also catch the
# prose-named and FR-N closures the #495 miss exposed, again 2026-07-02
# (forms 4 to 6, the #563 verifier's tooling note after #567's section-and-item
# phrasings passed vacuously), and again 2026-07-03 (form 7, the #607 miss),
# while staying false-positive-free. The seven forms
# below were chosen empirically: tested
# against the entire CHANGELOG history (root + detailed mirror, ~14k lines),
# each matched only genuine current-PR closures with ZERO past-closure-narration
# false positives. A bare lowercase `Closes FR-N` was deliberately NOT added: it
# matched ~95 lines including past-closure narration ("PR #143 closed FR-9",
# "PRs #221-#228 closing FR-33/82/..."), exactly the standing-gate false-fire the
# original narrow design avoided; the close-out-checklist convention covers that
# residual (maintainer decision 2026-06-30). A generalized "clos... the
# section" form was census-tested for the 2026-07-02 widening and REJECTED on
# two historical false positives; the shipped section form requires the
# hyphenated `section-N.M` token instead.
CLOSURE_PATTERNS = (
    # (1) the canonical section form: a closure verb, optional "the", then "TODO §".
    re.compile(r"\bclos(?:e|es|ed|ing)\b\s+(?:the\s+)?TODO\s+§", re.IGNORECASE),
    # (2) the distinctive major-closure marker "FR-N CLOSED", widened (GR-13)
    # from the FR-only form to any two-to-four-letter uppercase coded id
    # (FR/GR/SR and future families): the guardrail-intake GR items showed a
    # coded closure the FR-only pattern was blind to. Uppercase CLOSED stays
    # the deliberate this-PR-closure flag; case-sensitive so lowercase
    # "closed FR-N" / "GR-2 closed" narration does not match. Empirically
    # FP-free against the whole CHANGELOG history (the widened form matches
    # exactly the same four genuine FR-N CLOSED instances the old one did).
    re.compile(r"\b[A-Z]{2,4}-\d+\s+CLOSED\b"),
    # (3) the prose-named / explicit backlog-item form: a closure verb, "the",
    # then (within one clause) "backlog item" / "TODO item" / "directive". This
    # catches "closes the maintainer-directed ... validation directive" (the #495
    # prose-named miss) and "closes the ... backlog item".
    # The tempered run forbids a SECOND "the": a second "the" signals a new noun
    # phrase or a prepositional object ("closing the gap per the maintainer
    # directive"), where the trailing item/directive word is NOT the closure's
    # direct object, so it is excluded as a false positive. The run admits a
    # dot ONLY between digits (a decimal / section token such as "section-3.14"
    # or "\u00a75.3") while a sentence-ending period still terminates the clause:
    # the 2026-07-03 census showed the plain [^.\n] run could never match a
    # closure whose intervening text carries a section number (two genuine
    # historical closures were invisible). "bullet(s)" joins the noun set (the
    # #592 mirror evasion); the widened form's census found three new hits,
    # all true positives, zero false positives.
    re.compile(
        r"\bclos(?:e|es|ed|ing)\b\s+the\s+(?:(?!\bthe\b)(?:[^.\n]|(?<=\d)\.(?=\d))){0,70}?\b(?:backlog item|TODO item|directive|bullets?)\b",
        re.IGNORECASE,
    ),
    # (4) the section-name closure form: a hyphenated `section-N.M` token then
    # (within one clause) a closed/closure word. The hyphenated token is the
    # FP guard: the generalized "clos... the section" form was census-tested
    # and rejected on two historical false positives. Case-sensitive, matching
    # the censused form.
    re.compile(r"\bsection-\d+\.\d+(?:[^.\n]){0,80}?\bclos(?:ed|ure)\b"),
    # (5) the item-number closure form: "item(s) N [and M ...] closed", the
    # multi-item shape #567 used ("items 11 and 12 closed"). The character
    # class between the numbers and "closed" admits only digits, punctuation,
    # and whitespace, so narration like "items 4-7 remain deferred, not
    # closed" cannot match. Case-sensitive, matching the censused form.
    re.compile(r"\bitems?\s+\d[\d.,\s\-]*(?:and\s+[\d.,\s\-]+)*closed\b"),
    # (6) the rotation-assertion form: a line claiming the rotation itself
    # happened. If the claim is true the gate passes trivially (both surfaces
    # are in the diff); a line NARRATING a past PR's rotation is covered by
    # the TodoRotation: opt-out trailer, the same escape hatch as form 1.
    # Widened 2026-07-03 with the short "rotated to DONE" variant (22 census
    # hits: 20 genuine same-PR rotation assertions, 2 negations); the
    # fixed-width not-lookbehind excludes the negation narration ("is NOT
    # rotated to DONE") the census surfaced.
    re.compile(r"(?<![Nn][Oo][Tt] )\brotated to (?:the DONE ledger|DONE)\b"),
    # (7) the space-separated TODO-section closure form: the literal token
    # "TODO section N.M" then (within one clause, forward-only) a
    # closed/closure word. Added 2026-07-03 after #607's root lead ("TODO
    # section 1.1 is CLOSED and rotated to [a linked path]") matched none of
    # the six forms: form 1 wants a `§`, form 4 wants the hyphenated
    # `section-N.M`, and the rotation clause's markdown link defeated form 6's
    # literal "rotated to DONE". The `TODO ` anchor is the FP guard that the
    # census-rejected generalized bare-"section" form lacked: the full-history
    # census found exactly 4 hits (the #593 and #607 root leads plus two #607
    # mirror lines; the #593 mirror carries no such token), all
    # genuine same-PR closures, 0 false positives; the forward-only window
    # correctly excludes past-closure narration where the closure word
    # PRECEDES the token ("the closed TODO section 3.14 reworded", #594).
    # Case-insensitive so the emphatic "is CLOSED" matches; the clause run
    # admits a dot only between digits, as in form 3.
    re.compile(
        r"\bTODO section \d+\.\d+(?:[^.\n]|(?<=\d)\.(?=\d)){0,80}?\bclos(?:ed|ure)\b",
        re.IGNORECASE,
    ),
)

TRAILER_PATTERN = re.compile(
    r"^\s*TodoRotation:\s*(\S.*?)\s*$",
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
            "item (touches TODO.md and .working/DONE.md)."
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
        base = f"origin/{github_base}"
    head = args.head

    try:
        merge_base = git("merge-base", base, head)
    except subprocess.CalledProcessError as exc:
        print(
            f"ERROR: could not determine merge-base of {base}..{head}: {exc}. "
            f"In GitHub Actions, ensure that actions/checkout uses fetch-depth: 0.",
            file=sys.stderr,
        )
        return 2

    try:
        changed = [ln for ln in git("diff", "--name-only", merge_base, head).splitlines() if ln]
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    if not changed:
        print(f"OK: no files changed between {merge_base[:8]} and {head}.")
        return 0

    closure_line = asserts_todo_closure(added_changelog_lines(merge_base, head))
    if closure_line is None:
        print("OK: no TODO-item closure asserted in the added CHANGELOG lines.")
        return 0

    if TODO_PATH in changed and DONE_PATH in changed:
        print(
            f"OK: CHANGELOG asserts a TODO-item closure and the diff rotates it "
            f"(both {TODO_PATH} and {DONE_PATH} are in the diff)."
        )
        return 0

    # Closure asserted but a rotation surface is missing: check the opt-out trailer.
    try:
        commit_shas = git("log", "--format=%H", f"{merge_base}..{head}").splitlines()
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git log failed: {exc}", file=sys.stderr)
        return 2
    for sha in commit_shas:
        match = TRAILER_PATTERN.search(git("log", "-1", "--format=%B", sha))
        if match:
            print(
                f"OK: commit {sha[:8]} carries opt-out trailer: "
                f"'TodoRotation: {match.group(1)}'."
            )
            return 0

    missing = [p for p in (TODO_PATH, DONE_PATH) if p not in changed]
    print(
        f"FAIL: an added CHANGELOG line asserts a TODO-item closure but the diff "
        f"does not rotate it: {', '.join(missing)} not in the diff.",
        file=sys.stderr,
    )
    print(f"  asserting line: {closure_line.strip()[:160]}", file=sys.stderr)
    print("", file=sys.stderr)
    print(
        "When a PR closes a TODO item, delete it from TODO.md and add a row to "
        ".working/DONE.md in the same diff (the change-tracking rotation discipline). "
        "If the CHANGELOG line merely narrates a past closure, add a "
        "'TodoRotation: <reason>' trailer to any commit to opt out.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
