#!/usr/bin/env python3
"""Partial-rewrite tension-marker scan over TODO and ledger blocks (the GR-P3 aid).

The GR-P3 failure class (three occurrences, #563/#564/#565): a scope-adding fix
or rewrite touches PART of a TODO bullet or ledger row while hedges or stale
status framings survive elsewhere in the SAME block ("upstream-CONFIRMED" in
the clause just edited, "NEEDS-UPSTREAM" surviving three clauses later). The
containing block reads self-contradictory, and no gate sees it: the surfaces
are gate-exempt free prose.

This aid re-lints the rewritten line whenever a diff partially rewrites a
block (on these surfaces a block is normally one long physical line, so the
line usually IS the whole block; a status token on an unchanged sibling line
of a multi-line block is outside the scan): for each TODO bullet, ledger
table row, bold-led paragraph, or plain paragraph line that a commit range
MODIFIES (an added line sharing a pairing
key with a removed counterpart in the same file, a rewrite rather than a pure
addition or deletion; keys are the bold lead token, the first two table cells,
and a normalized prefix, matched on ANY so an edit inside one key region still
pairs), it scans the block's NEW text for a status-claim token co-occurring
with a hedge token, and prints every pair hit as an untruncated full line for
judgment.

KNOWN RECALL LIMIT: pairing is line-local, so a rewrite that changes a block's
OPENING words and has no stable bold lead or table cells (a DONE-entry body
whose leading count is the edit, "Seven stale ..." to "Eleven stale ...")
matches no key and escapes. A best-effort trigger is the aid's design point;
treat a clean run as "nothing detected", never "nothing rewritten".

WHY AN AID AND NOT A GATE (the build-time census, 2026-07-02): every candidate
status+hedge pair has legitimate hits on the live surfaces. A census over
TODO.md and the then-six working ledgers found 91 block-level pair coincidences,
essentially all honest narrative (a retro row narrating "shipped X; pending Y",
the handoff's soft-spots block mixing CONFIRMED with awaiting, and bullets that
QUOTE the marker vocabulary, this aid's own backlog bullet among them). The
bookkeeping-gate family's precision-first bar (a standing gate ships only with
a zero-false-positive census, the D5 precedent) is therefore unreachable for
this class; the mechanizable half is the TRIGGER (a partial rewrite) and the
CANDIDATE list (the pairs), with the contradiction judgment staying human. The
aid prints candidates and always exits 0 on findings-for-judgment; it exits
non-zero only for usage or git errors, or to refuse a collapsed range (base and
head resolving to the same commit: CANNOT-EVALUATE, exit 2).

Usage:
    python3 tools/tension-scan.py origin/main          # blocks rewritten since base
    python3 tools/tension-scan.py origin/main HEAD

The close-out convention: run it before pushing any PR that edits TODO or a
ledger row in place; read each printed block END TO END (the splice-seam
lesson) and fix real contradictions, leaving honest narrative alone.

Exit codes:
    0 : scan ran (with or without candidate pairs; the judgment is the reader's)
    2 : usage or git error (including a work tree top level git reports that
        is not this script's own repository, REPO_ROOT: another directory, or
        a relative or empty one; a git directory other than REPO_ROOT's own,
        as GIT_DIR naming another repository gives; GIT_COMMON_DIR,
        GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_DIRECTORIES,
        GIT_GRAFT_FILE or GIT_SHALLOW_FILE in the environment, or
        GIT_WORK_TREE or GIT_INDEX_FILE pointing away from REPO_ROOT; a
        REPO_ROOT that is not a work tree registered with the git directory
        git reads, as a .git file naming another checkout's gives, or a
        relocated objects directory or a git-new-workdir checkout (objects,
        refs or reftable that are symbolic links); and a separate git
        directory that sets no core.worktree, as git init or git clone
        --separate-git-dir leaves one: in that checkout run
        git config core.worktree "$PWD"), or CANNOT-EVALUATE: base and head
        resolve to the same commit (an empty range), so nothing was scanned

Known residuals (3b564): git failing to run at all (OSError) on the one
top-level read degrades to a placeholder and skips the top-level comparison
(the git-directory checks still run). The scan runs git from the current
directory, so it also refuses (fail-closed) where git's top level is not this
copy's REPO_ROOT although nothing is misread: the main checkout's copy run
from inside a linked worktree or a submodule, and this copy run from a
subdirectory while GIT_DIR is exported (git then takes the current directory
as the top level). The scan is run by hand (the close-out convention above)
and should be run from the repository's top level. What the git-directory
checks do not cover is disclosed in lint_common.require_own_git_dir.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
from lint_common import REPO_ROOT, require_own_git_dir, resolve_base_ref, resolve_working  # noqa: E402

# The surfaces whose blocks the GR-P3 class lives in: the backlog and the
# working ledgers whose rows are rewritten in place. The `.working/`
# paths resolve from the operational store when present.
SCANNED_FILES = (
    "TODO.md",
    "TODO-REFERENCE.md",
    ".working/pending-decisions.md",
    ".working/session-handoff.md",
    ".working/DONE.md",
    ".working/improvement-log.md",
    ".working/validate-pr/history.md",
)

_WORKING_TARGETS = tuple(f for f in SCANNED_FILES if f.startswith(".working/"))
_PUBLIC_TARGETS = tuple(f for f in SCANNED_FILES if not f.startswith(".working/"))


def git_diffable_targets() -> tuple[list[str], list[str]]:
    """(files, skipped): the scanned surfaces `git diff` on the public repo can
    see, plus the `.working/` surfaces it cannot. A public target always
    qualifies; a `.working/` target qualifies only while it resolves in-repo
    (pre-migration). Once it resolves into the operational store or private-sibling fallback, the public
    `git diff` cannot reach it, so it is skipped with an honest note (the
    private ledgers' block-tension scan becomes a private-repo concern)."""
    files = list(_PUBLIC_TARGETS)
    skipped: list[str] = []
    for rel in _WORKING_TARGETS:
        resolved = resolve_working(rel[len(".working/"):], repo_root=REPO_ROOT)
        if resolved is not None:
            try:
                files.append(str(resolved.relative_to(REPO_ROOT)))
                continue
            except ValueError:
                # Resolved OUTSIDE the public repo (operational store or private sibling):
                # the public git diff cannot reach it. Report the PHYSICAL resolved location,
                # not the logical .working/ key (the store has no working/ subdir).
                skipped.append(str(resolved))
                continue
        skipped.append(rel)
    return files, skipped

# Status-claim tokens: the block asserts a settled state.
STATUS_RE = re.compile(
    r"upstream-CONFIRMED|\bCONFIRMED\b|\bCLOSED\b|\bRESOLVED\b|\bACTIONED\b|\bSHIPPED\b|\b[Ss]hipped\b"
)

# Hedge tokens: the block still carries an unsettled framing.
HEDGE_RE = re.compile(
    r"NEEDS-UPSTREAM|\bTBD\b|\bpending\b|\blikely\b|\bawaiting\b|\bnot yet\b|\bdeferred\b"
)

# A block line: a markdown bullet, a table data row, a bold-led paragraph
# (the pending-decisions "**Status:** ..." shape), or a plain paragraph line
# (the DONE-entry body shape, this aid's own motivating record-drift case),
# including digit-initial paragraphs ("72-hour ..."). Headings, fences, and
# other markup-led lines are excluded; the pairing requirement (a shared key
# on both diff sides of the same file) is what keeps the wide net from
# pairing unrelated prose.
BLOCK_RE = re.compile(r"^\s*(?:- |\| |\*\*|[A-Za-z0-9])")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)


def block_keys(line: str) -> set[str]:
    """Candidate identities for pairing a rewritten block's old and new versions.

    A block pairs when ANY key matches across the diff sides, because each
    single key fails some real rewrite shape: the bold lead token (the
    '- **(GR-5, ...)**' and '**Status:** ...' shapes) is stable when the
    body is rewritten but changes when the lead itself carries the edited
    status word; the normalized prefix is stable in that case but changes
    when the block's opening value is the edit (a '**Status:** 2 pending'
    to '0 pending' rewrite). Table rows key on their first two cells.
    """
    stripped = line.strip()
    keys: set[str] = set()
    if stripped.startswith("|"):
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        keys.add("cells:" + "|".join(cells[:2]).lower())
    m = re.match(r"(?:-\s+)?\*\*(.+?)\*\*", stripped)
    if m:
        keys.add("lead:" + m.group(1).lower())
    keys.add("prefix:" + re.sub(r"\W+", " ", stripped)[:24].lower())
    return keys


def main(argv: list[str]) -> int:
    if len(argv) < 2 or len(argv) > 3 or any(a.startswith("-") for a in argv[1:]):  # 3b50b2f: only the documented forms are accepted; anything else is a usage error (exit 2)
        print("usage: tension-scan.py <base-ref> [head-ref]", file=sys.stderr)
        return 2
    base, head = argv[1], (argv[2] if len(argv) > 2 else "HEAD")
    # A short name such as origin/main is read from <git-dir>/origin/main
    # before refs/remotes, so it is resolved unambiguously first (3b620
    # round 8).
    base, refusal = resolve_base_ref(base, REPO_ROOT, from_cwd=True)
    if refusal:
        print(f"tension-scan: {refusal}; nothing was scanned.", file=sys.stderr)
        return 2
    scanned, skipped = git_diffable_targets()
    if skipped:
        print("tension-scan: NOTE: skipping surfaces not visible to the public "
              "git diff (resolved into the operational store or private sibling): "
              + ", ".join(skipped), file=sys.stderr)
    try:
        merge_base = git("merge-base", base, head).strip()
        head_sha = git("rev-parse", "--verify", f"{head}^{{commit}}").strip()
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"tension-scan: git failed: {exc}", file=sys.stderr)
        return 2
    try:
        # The refusal's repo= field and the comparison below: git failing to
        # run at all (OSError) degrades to a placeholder as D12's _toplevel
        # does, so the scan keeps its real result instead of a traceback
        # (3b540 round 8). The top level is read as bytes and decoded with
        # os.fsdecode, so a path that is not valid UTF-8 still reaches the
        # comparison instead of the placeholder (3b564). git refusing to
        # print one (no work tree, as with GIT_DIR naming a bare repository)
        # still refuses with exit 2 (3b540 round 9).
        toplevel = os.fsdecode(subprocess.check_output(["git", "rev-parse", "--show-toplevel"])).strip()
    except OSError:
        toplevel = "(no work tree)"
    except subprocess.CalledProcessError as exc:
        print(f"tension-scan: git failed: {exc}", file=sys.stderr)
        return 2
    else:
        if not toplevel:
            # git older than 2.25 printed nothing and exited 0 outside a work tree
            # instead of refusing, so an empty top level is the same missing work
            # tree and refuses the same way on any git (3b559).
            print("tension-scan: git rev-parse --show-toplevel printed an empty top "
                  "level (no work tree); nothing was scanned.", file=sys.stderr)
            return 2
        # The scanned surfaces resolve against REPO_ROOT while git runs from
        # the current directory, so the top level git reports must be
        # REPO_ROOT itself (not another clone, nor GIT_DIR naming a bare
        # clone plus GIT_WORK_TREE naming another directory). Path resolves
        # a relative top level against the current directory, so it must
        # also be absolute, as git always prints it (3b564). The placeholder
        # above skips this check (3b540 round 8).
        top = Path(toplevel)
        if not (top.is_absolute() and top.resolve() == REPO_ROOT.resolve()):
            print(
                f"tension-scan: git reports the work tree top level {toplevel!r}, "
                f"not this script's repository {REPO_ROOT}; run the copy of this "
                f"script inside the tree under test.",
                file=sys.stderr,
            )
            return 2
    # A top level of REPO_ROOT does not show that git reads REPO_ROOT's
    # repository (GIT_DIR naming another one still reports it), so compare
    # the git directories too, as D9 does (3b564).
    refusal = require_own_git_dir(REPO_ROOT, from_cwd=True)
    if refusal:
        print(f"tension-scan: {refusal}; nothing was scanned.", file=sys.stderr)
        return 2
    # A collapsed range would read as the clean "0 rewritten block(s)" summary;
    # refuse it instead (same wrong-repository signature the delta gates refuse,
    # orchestrator mistake 300).
    if merge_base == head_sha:
        print(
            f"tension-scan: CANNOT-EVALUATE: base {base} and head {head} resolve to "
            f"the same commit (repo={toplevel} base={merge_base} head={head_sha}); "
            f"the range is empty, so nothing was scanned.",
            file=sys.stderr,
        )
        return 2
    try:
        diff = git("diff", merge_base, head, "--", *scanned)
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"tension-scan: git failed: {exc}", file=sys.stderr)
        return 2

    # Duplicate keys within a file collapse (set semantics), so two rewritten
    # blocks sharing a key count once; acceptable for an aid whose output is
    # candidates-for-judgment, not a tally.
    removed_keys: set[str] = set()
    added: list[tuple[str, str, set[str]]] = []
    current_file = "?"
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue
        if line.startswith("+++ "):
            current_file = "?"  # deleted-file half; do not attribute to the prior file
            continue
        if line.startswith("-") and not line.startswith("---") and BLOCK_RE.match(line[1:]):
            removed_keys.update(f"{current_file}\x00{k}" for k in block_keys(line[1:]))
        elif line.startswith("+") and not line.startswith("+++") and BLOCK_RE.match(line[1:]):
            added.append((current_file, line[1:], block_keys(line[1:])))

    candidates = 0
    rewrites = 0
    for fname, new_line, keys in added:
        if not any(f"{fname}\x00{k}" in removed_keys for k in keys):
            continue  # pure addition, not a rewrite
        rewrites += 1
        st = STATUS_RE.search(new_line)
        hg = HEDGE_RE.search(new_line)
        if st and hg:
            candidates += 1
            print(f"[JUDGE] {fname}: status '{st.group(0)}' with hedge '{hg.group(0)}' in the rewritten block:")
            print(f"        {new_line.strip()}")

    print(
        f"\ntension-scan: {rewrites} rewritten block(s) since {merge_base[:8]}, "
        f"{candidates} carrying a status+hedge pair to judge."
    )
    if candidates:
        print(
            "tension-scan: read each flagged block END TO END; fix a real "
            "contradiction, leave honest narrative alone (the judgment is not "
            "mechanizable; see the docstring's census)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
