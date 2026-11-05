#!/usr/bin/env python3
"""Retained GRC procedure: .claude/references/governance/evidence-grounded-completion.md;
AIQT baseline: .claude/rules/aiqt/10-ACCUR-evidence-grounded-completion.md.

Stop hook: refuse a turn-end while the session is holding outstanding work.

Shipped 2026-08-07 after the orchestrator ended a turn on a stated intention ("continuing with X",
"next I will do X") EIGHT times in one session, each after an explicit maintainer correction, one
of them in capitals, while every mechanical guard in the same session held without exception. That
asymmetry is the whole argument for this hook: prose correctives failed repeatedly against the same
reflex, and mechanism did not fail once. The discipline it backstops is the section "A stated
intention is a claim, and an unkept one is a false statement" in
guardrails/governance/evidence-grounded-completion.md.

REVISED 2026-08-07, same day, after a dual-family review of the FIRST version returned seven errors
against it. Four were fatal and all four are fixed here: it never read its Stop payload, so it could
not see stop_hook_active and had no terminating condition; its escape hatch was an environment
variable the actor cannot set into this process, which is the appearance of an escape rather than
one; and the held-branch list was a hardcoded set whose "must cite a decision record" was an
unenforced comment.

WHAT IT IS, stated narrowly because a cross-family verifier caught the first version claiming more
than it can see. This is a LOCAL-BRANCH SENTINEL, not a general
outstanding-work detector. It is blind to a still-running dispatched worker, to an unfinished task list, to uncommitted
working-tree changes, and to a detached commit. Those are
real outstanding work and this hook will let you yield on all of them; the discipline, not the
guard, covers them.

WHAT IT BLOCKS. A turn-end while a branch is ahead of main whose tree `git diff --quiet` reports as differing (a tree-identical branch, e.g. squash-merged-but-undeleted, is exempt; a diff-command error also leaves it reportable) and is not on the recorded held list.

WHAT IT DOES NOT BLOCK, by construction:
  * a continuation that is already under way (stop_hook_active), so it blocks at most once and
    cannot loop the session;
  * anything at all, if the escape file exists and is successfully consumed (see below);
  * anything at all, if an error reaches main()'s outer exception handler (see GIT FAILURES BLOCK); a LOCAL
    recovery path (git checks, the resolver import, a failed escape-unlink) can instead block;
  * anything at all, inside a dispatched worker session: a worker's fan-out cannot discharge any of
    this guard's remedies, so the check is skipped there (#1695).

ESCAPE, and it is reachable. Create the file named by ESCAPE_FILE from any shell:
``touch "${GRC_DROP_ROOT:-<repo-parent>/grc_working}/.allow-stop"`` (default ``<repo-parent>/grc_working/.allow-stop`` when GRC_DROP_ROOT is unset). The hook honours it ONCE and deletes it, so an escape
cannot silently become the standing state. It is reachable from a Bash tool call, which the previous
environment-variable form was not: a Stop hook inherits the harness's environment, never the
environment of a tool call.

GIT FAILURES BLOCK: enumeration failures, malformed listing records, unreadable
ref files, rev-list failures and diff failures/timeouts produce blocking diagnostics.
A repository without main or refused by safe.directory also blocks.
LIMIT: a ref directory git cannot read (for example permission-denied
refs/heads/sub/) is invisible to git, which exits 0 with no stderr; this hook
cannot see branches inside that directory.
Per-branch failures name the branch and do not discard other branches. Listing
failures name the enumeration because no trustworthy branch list is available.
Non-UTF-8 names are kept as bytes for git and escaped for display. Inherited
GIT_TRACE* variables are removed and configured trace2 targets are disabled.
Git runs with LC_ALL=C and without LANGUAGE or LC_MESSAGES so diagnostics
match the untranslated prefixes below. Stderr lines starting with "fatal:", "error:",
"warning: ignoring broken ref " or "warning: ignoring ref with broken name "
block. Other stderr (including other warnings, hints and trace2 lines) is ignored;
stdout must still be clean. A nonzero exit blocks, except diff exit 1 with empty
stdout and no blocking diagnostic, which means the branch tree differs.
HELD-INPUT FAILURES BLOCK: on the normal strict-resolution path, a held file
whose initial lstat raises FileNotFoundError reads as absent, with no holds
and no diagnostic. ENOTDIR, a dangling link and every other resolution,
stat, read or decode failure use no holds and add one diagnostic while
retaining the branch scan. Only in the fallback resolver (when lint_common
cannot be loaded) and the post-resolution stat in held_branches() do ENOENT
and ENOTDIR read as absent, with no holds and no diagnostic.
A malformed hold line is skipped as no hold without a diagnostic.
The one-shot escape and stop_hook_active still take precedence. Other errors
reaching main()'s outer handler retain its existing fail-open behavior.

GUARD-INPUT RESIDUE, stated at the point of use per validate-inference-before-action:
  * "a branch is ahead of main" is NOT "a branch is meant to merge". A deliberately-held branch
    needs a file entry with a YYYY-MM-DD-shaped date token comparing lexically at or after today; the
    reason and any decision-record citation are the instructed convention the hook does not verify (it
    checks only that token). The list is a file
    rather than a constant so holds are recorded, not baked in.
  * the hook sees files and refs. It cannot see whether the actor intends to continue, which is the
    thing it is really trying to constrain; it can only make yielding-with-work-outstanding require
    a deliberate act.

CONSOLE AND DETAIL LOG (maintainer-directed 2026-11-04: refusal detail belongs on the backend, not
the operator view). This changes only how a refusal is worded and routed, never whether the hook
refuses. decide() renders the FULL detail: every outstanding or unverifiable branch, the resolved
held-branches path and the one-shot escape. main() appends that detail to a per-session log,
<store>/stop-hook-detail/turn-end.<first 12 characters of session_id>.log (each entry's header
carries the whole session_id), where <store> is _DETAIL_STORE: GRC_STORE (a relative value is
resolved against this checkout's root), else <repo-parent>/private, the same store resolution
as stop-guard-unattended.py. The detail log never uses lint_common.resolve_working, whose
transitional fallback can name a `.working` directory inside a git checkout. The text returned
to the harness is then three short lines (summarize()), each at most _MAX_LINE_CHARS
characters: what blocked, with the branch count and at most the first _SHOWN_ITEMS branches
(each escaped with _printable, then cut to _MAX_ITEM_CHARS); WHY; and the one action that
clears it, followed by the log
path. PATH BUDGET: the log path adds 43 characters to the store path (with a 12-character
session prefix), so the short form fits a store path of at most 79 characters (60 with the
longer wording); a longer store path, or a log path with any non-printable character (a
newline, a carriage return or a terminal escape, tested with the same rule _branch_display
uses), falls back as below. A store inside this checkout, or inside any git working tree (a
`.git` entry in the store directory or any ancestor up to the filesystem root, lexically or
after resolving symlinks, or `git rev-parse --is-inside-work-tree` succeeding there with every
inherited GIT_* variable removed), is refused before anything is created. The log is created
without following symlinks (the store directory, the subdirectory and the file are opened with
O_NOFOLLOW); the subdirectory must be owned by this uid with no group or other write bit; the
file must be regular, mode 0600, owned by this uid and singly linked; and after the write the
advertised path must still name the written file (lstat st_dev and st_ino against the
descriptor's fstat). The resolution, checks, open and write run in a daemon thread joined for
at most _DETAIL_TIMEOUT_S seconds, so a stalled filesystem cannot delay the refusal. If the log
cannot be written (no usable session_id in the Stop payload, no store, a store inside this
checkout or a git working tree, a timeout, or any open, check or write failure), or the log
path cannot be shown on one console line, the console fallback is returned instead: the
BLOCKED and WHY lines, one NOTE line naming the failure, then the branch list cut at the first
_FALLBACK_ITEMS branches (the pre-2026-11-04 console cap) with one line counting the rest, the
held-branches path and the one-shot escape. This fails open to visibility, never to silence:
the count is always shown, and when the log was written the full list is there. RESIDUE: when
the log was not written, branches past the first _FALLBACK_ITEMS are named nowhere, as before
2026-11-04. Exit status, the escape and stop_hook_active handling are unchanged. RESIDUE:
ancestors above the store directory are not checked for symlinks; the log is appended to
without rotation; two sessions whose ids share their first 12 characters share one log file
(each entry names its session); a write that times out may still complete later in the
abandoned thread, and the process exit can still wait on a syscall the kernel does not let a
fatal signal interrupt.
"""

from __future__ import annotations

import datetime as _dt
import errno
import json
import os
import re as _re
import stat
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

def _load_sibling(name, _cache={}):
    """Execute a reviewed repository helper's .py SOURCE BYTES and return the module.

    SECI-config-is-executable-trust-gate: the settings.json launcher runs `python3 -I`,
    this function never touches sys.path and never uses import machinery for the
    helper, so nothing planted beside a hook (a stdlib-named decoy module, a
    __pycache__/*.pyc) can execute, and no bytecode cache is ever read or written.
    Containment is decided on the path AS LAUNCHED, before any symlink resolution:
    os.path.abspath(__file__) (unresolved) must sit at <root>/.claude/hooks/<hook>.py,
    and every component from that root down to the hook and down to the helper (the
    root itself, .claude, .claude/hooks, tools, the hook file and the helper file)
    must not be a symlink; only then are real paths compared, requiring the hook's and
    the helper's real locations to sit at exactly their expected places under the real
    repository root (ancestors ABOVE the root may be symlinks: both sides of each
    comparison resolve them identically). Any violation is REFUSED fail-closed: exit 2
    with a clear message, raised as SystemExit so the hooks' fail-open
    `except Exception` guards cannot swallow it. A MISSING helper is different: the
    plain OSError propagates to the caller, which takes this hook's documented
    missing-helper behaviour, never a sys.modules fallback.

    TEST-ONLY SEAM: when this hook is loaded AS A MODULE by the in-repo test harness
    (__name__ != "__main__"), a helper already present in sys.modules is reused, which
    preserves the patch-the-helper-then-load-the-hook test contract. A production launch
    is always a direct execution (__name__ == "__main__"), and neither the environment
    nor any file in the tree can change that, so a production load NEVER consults a
    pre-existing sys.modules entry: it always re-executes the reviewed source and
    overwrites the entry (dependencies included: todo_index_rows reads lint_common from
    the entry this loader has just written).
    """
    import os.path
    import sys
    if name in _cache:
        return _cache[name]
    if __name__ != "__main__" and name in sys.modules:
        _cache[name] = sys.modules[name]
        return _cache[name]

    def _refuse(why):
        print("BLOCKED (hook-helper-isolation): " + why + "; refusing to execute "
              "anything but the reviewed helper sources.", file=sys.stderr)
        sys.exit(2)

    hook_path = os.path.abspath(__file__)  # the path AS LAUNCHED, symlinks unresolved
    hooks_dir = os.path.dirname(hook_path)
    claude_dir = os.path.dirname(hooks_dir)
    root = os.path.dirname(claude_dir)
    if os.path.basename(hooks_dir) != "hooks" or os.path.basename(claude_dir) != ".claude":
        _refuse("this hook's launch path " + hook_path + " is not under "
                "<repo-root>/.claude/hooks, so no repository root can anchor helper "
                "containment")
    parts = (".claude", "hooks") if name.startswith("_") else ("tools",)
    helper_dir = os.path.join(root, *parts)
    helper_path = os.path.join(helper_dir, name + ".py")
    for p in (root, claude_dir, hooks_dir, hook_path, helper_dir, helper_path):
        if os.path.islink(p):
            _refuse(p + " is a symlink on the path as launched (containment is "
                    "decided before any symlink resolution)")
    real_root = os.path.realpath(root)
    if os.path.realpath(hook_path) != os.path.join(real_root, ".claude", "hooks",
                                                   os.path.basename(hook_path)):
        _refuse("this hook's real location " + os.path.realpath(hook_path)
                + " does not sit at its launch-path place under the real repository "
                "root " + real_root)
    if os.path.realpath(helper_path) != os.path.join(real_root, *parts, name + ".py"):
        _refuse("helper " + helper_path + " does not resolve to its expected place "
                "under the real repository root " + real_root)
    for dep in {"todo_index_rows": ("lint_common",)}.get(name, ()):
        _load_sibling(dep)
    with open(helper_path, "rb") as fh:
        source = fh.read()
    module = type(sys)(name)
    module.__file__ = helper_path
    exec(compile(source, helper_path, "exec", dont_inherit=True), module.__dict__)
    sys.modules[name] = module
    _cache[name] = module
    return module


try:
    is_worker_session = _load_sibling("_hookutil").is_worker_session
except Exception:                                  # pragma: no cover - fail OPEN on import trouble
    def is_worker_session() -> bool:               # noqa: D103
        return True

REPO = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
ESCAPE_FILE = Path((os.environ.get("GRC_DROP_ROOT") or (Path(__file__).resolve().parents[3] / "grc_working"))) / ".allow-stop"
# Held branches live in a FILE with a reason per line, not a constant in this file: a hardcoded set
# goes stale the day it is written, and a comment saying "cite a decision record" enforces nothing.
# The file is resolved via the store-aware resolver (local operational store preferred, the
# grc_library_private/.working sibling a transitional fallback), never a hardcoded sibling-store path,
# so this guard follows the migration of the working store to local. Fail-safe: a resolver-load
# failure leaves _resolve_working None and _working_file falls back to the in-repo .working/ path.
try:
    _resolve_working = _load_sibling("lint_common").resolve_working
except Exception:  # pragma: no cover - fail-safe: never let a helper-load failure break the hook
    _resolve_working = None


def _working_file(rel_below, root):
    """`.working/<rel_below>` resolved via lint_common (local store preferred), or None."""
    if _resolve_working is not None:
        return _resolve_working(rel_below, repo_root=root, strict=True)
    cand = root / ".working" / rel_below
    try:
        os.stat(cand)
    except OSError as exc:
        if exc.errno in (errno.ENOENT, errno.ENOTDIR):
            return None
        raise
    return cand


# Save resolution failures until AFTER the continuation/worker/escape checks.
# Raising here would bypass main() entirely and make the escape unreachable.
_HELD_FILE_ERROR = None
try:
    HELD_FILE = _working_file("held-branches.txt", REPO)
except Exception as exc:
    HELD_FILE = None
    _HELD_FILE_ERROR = exc
GIT_TIMEOUT = 20
_EXPIRY = _re.compile(r"\d{4}-\d{2}-\d{2}", _re.ASCII)
# Console refusal shape (see CONSOLE AND DETAIL LOG in the module docstring). _MAX_LINE_CHARS is
# stop-guard-unattended.py's existing per-line clamp, mirrored here so both Stop hooks agree.
_SHOWN_ITEMS = 3
_FALLBACK_ITEMS = 8
_MAX_ITEM_CHARS = 48
_MAX_LINE_CHARS = 160
_DETAIL_SUBDIR = "stop-hook-detail"
_DETAIL_NAME = "turn-end"
_SESSION_PREFIX_CHARS = 12
_DETAIL_TIMEOUT_S = 2.0
_SESSION_ID = _re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}", _re.ASCII)


def _detail_store():
    """The detail log's store directory, resolved as stop-guard-unattended.py resolves its own:
    GRC_STORE (relative to this checkout's root when relative), else <repo-parent>/private."""
    root = Path(__file__).resolve().parents[2]
    value = os.environ.get("GRC_STORE")
    if not value:
        return root.parent / "private"
    return Path(value) if os.path.isabs(value) else Path(os.path.normpath(root / value))


try:
    _DETAIL_STORE = _detail_store()
except Exception:  # pragma: no cover - no store: the refusal falls back to the console
    _DETAIL_STORE = None


def _git_environment() -> dict:
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_TRACE") and key not in {"LANGUAGE", "LC_MESSAGES"}}
    env["LC_ALL"] = "C"
    # Trace2 starts before git applies -c settings; override its early config too.
    env.update(GIT_TRACE2="0", GIT_TRACE2_PERF="0", GIT_TRACE2_EVENT="0")
    return env


def _git_result(*args: str | bytes) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-c", "core.warnAmbiguousRefs=false",
         "-c", "trace2.normalTarget=", "-c", "trace2.perfTarget=",
         "-c", "trace2.eventTarget=", "-C", str(REPO), *args],
        capture_output=True, env=_git_environment(), timeout=GIT_TIMEOUT, check=False,
    )


def _blocking_stderr(stderr: bytes) -> bool:
    return any(line.startswith((b"fatal:", b"error:",
                                b"warning: ignoring broken ref ",
                                b"warning: ignoring ref with broken name "))
               for line in stderr.split(b"\n"))


def _printable(text: str) -> str:
    """Escape every character that is neither printable nor a space separator."""
    return "".join(char if char.isprintable() or unicodedata.category(char) == "Zs"
                   else ascii(char)[1:-1] for char in text)


def _branch_display(ref: bytes) -> str:
    return _printable(ref.removeprefix(b"refs/heads/").decode("utf-8", errors="backslashreplace"))


def _git_display(output: bytes) -> str:
    return output.decode("utf-8", errors="backslashreplace").rstrip("\r\n")


def _git(*args: str | bytes) -> bytes:
    result = _git_result(*args)
    result.check_returncode()
    if _blocking_stderr(result.stderr):
        raise ValueError("git diagnostic: " + _git_display(result.stderr))
    return result.stdout


def held_branches() -> dict:
    """Map branch -> reason for each UNEXPIRED hold. Absent file means nothing is held.

    Line format: ``<branch>  # <YYYY-MM-DD expiry>  <reason>``. The expiry is required and is
    checked, because a cross-family verifier pointed out that an exemption keyed on a mutable
    branch name alone exempts every later commit under that name, forever, with nothing forcing
    anyone to revisit it. An expired or malformed hold is simply NOT a hold: the branch reappears
    in the guard's output, which is the prompt to renew it deliberately or let it go.

    RESIDUE, at the predicate: this validates that a hold was recorded and has not lapsed. It does
    NOT pin the approved tip, so work added to a held branch after the hold was granted is covered
    by it. Pinning the tip is the stronger form and is deliberately not built yet; a branch is held
    for weeks and would need its hold rewritten on every commit.
    """
    held = {}
    if HELD_FILE is None:
        return held
    try:
        os.stat(HELD_FILE)
    except OSError as exc:
        if exc.errno in (errno.ENOENT, errno.ENOTDIR):
            return held
        raise
    today = _dt.date.today().isoformat()
    for line in HELD_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, _, rest = line.partition("#")
        rest = rest.strip()
        parts = rest.split(None, 1)
        if not parts or not _EXPIRY.fullmatch(parts[0]):
            continue                      # no parsable expiry: not a hold
        if parts[0] < today:
            continue                      # lapsed: the branch is visible again, deliberately
        held[name.strip()] = parts[1] if len(parts) > 1 else "no reason recorded"
    return held


def unmerged_branches() -> list:
    # RESIDUE, at the predicate: "ahead of main" is NOT "not merged". This project squash-merges,
    # so a branch whose work is fully on main keeps its own distinct commits forever and stays
    # ahead until it is deleted. A cross-family verifier proved this with a synthetic squash probe:
    # rev-list said one commit ahead while the trees were identical. Counting alone would make the
    # guard block permanently on every merged-but-undeleted branch, which is the shape that gets a
    # guard switched off. So a branch is reported only when it is ahead AND its tree differs from
    # main. Remaining residue: patch-equivalent-but-not-tree-equal work (a merged change plus an
    # unrelated later edit) still reads as unmerged, which errs toward blocking, and a stale local
    # main reads every branch as unmerged, which errs the same way.
    out = []
    try:
        if _HELD_FILE_ERROR is not None:
            raise _HELD_FILE_ERROR
        held = held_branches()
    except Exception as exc:
        # No partial holds survive an untrusted input. Keep scanning so ALL
        # outstanding branches remain visible, alongside exactly one input error.
        held = {}
        path = HELD_FILE if HELD_FILE is not None else "held-branches.txt (resolution)"
        out.append((str(path), "unverified: " + type(exc).__name__ + ": " + str(exc)))
    try:
        listing = _git("for-each-ref", "--format=%(refname)", "refs/heads")
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        return out + [("branch enumeration", "unverified: " + str(exc))]
    if b"refs/heads/main" not in listing.split(b"\n"):
        out.append(("main", "unverified: missing refs/heads/main"))
    for ref in listing.split(b"\n"):
        if not ref:
            continue
        if (not ref.startswith(b"refs/heads/") or ref == b"refs/heads/"
                or any(byte <= 32 or byte == 127 for byte in ref)):
            out.append((_branch_display(ref), "unverified: malformed branch listing"))
            continue
        name = ref[len(b"refs/heads/"):].decode("utf-8", errors="surrogateescape")
        if name == "main" or name in held:
            continue
        display = _branch_display(ref)
        try:
            ahead = _git("rev-list", "--count", b"refs/heads/main.." + ref)
            if not _re.fullmatch(rb"[0-9]+\n?", ahead):
                raise ValueError("invalid rev-list count: " + _git_display(ahead))
            ahead = ahead.strip()
            if int(ahead) == 0:
                continue
            result = _git_result("diff", "--quiet", b"refs/heads/main", ref, "--")
            if result.stdout or _blocking_stderr(result.stderr):
                raise ValueError("git diff diagnostic: stdout: " + _git_display(result.stdout)
                                 + "; stderr: " + _git_display(result.stderr))
            if result.returncode == 0:
                continue          # tree-identical: the work landed
            if result.returncode != 1:
                raise ValueError("git diff exit %s: %s" %
                                 (result.returncode, _git_display(result.stderr)))
        except (OSError, subprocess.SubprocessError, ValueError) as exc:
            out.append((display, "unverified: " + str(exc)))
            continue
        out.append((display, ahead.decode("ascii")))
    return out




def decide(stop_hook_active: bool, escape: bool, branches: list,
           shown: int | None = None, note: str | None = None) -> str | None:
    """Pure decision, so it is testable without a repository. Returns the FULL detail (every
    branch); main() routes it to the detail log and shows summarize() on the console. The
    console fallback (_route_refusal) passes ``shown``, which keeps that many branches and
    counts the rest on one line, and ``note``, placed before the list."""
    if stop_hook_active or escape:
        return None
    if not branches:
        return None
    lines = ["BLOCKED (turn-end-outstanding-work): a turn-end yield while unmerged work is outstanding.",
             "WHY: an unmerged branch ahead of main is real outstanding work; yielding here strands it "
             "for the next session to untangle.", ""]
    if note is not None:
        lines.append(note)
    if branches:
        listed = branches if shown is None else branches[:shown]
        lines.append("  Branches outstanding or not verifiable (%d):" % len(branches))
        lines += ["    - %s (+%s)" % (n, a) for n, a in listed]
        if len(listed) < len(branches):
            lines.append("    ... and %d more, not shown here" % (len(branches) - len(listed)))
        lines.append("    Held-branches record path:")
        # Show the ACTUAL resolved held-branches path (resolve_working -> local store), never a
        # hardcoded sibling path, so the remediation the guard prints follows the store migration.
        lines.append("      %s" % (HELD_FILE if HELD_FILE is not None
                                   else "the held-branches file (resolved via lint_common.resolve_working)"))
    lines += [
        "",
        "CONSIDER INSTEAD: merge the branch(es) above, or record the hold with its reason in the "
        "held-branches file. For a genuine block (CI, a maintainer decision, an external wait), record that blocker, then run:",
        f"      touch {ESCAPE_FILE}     # honoured once, then deleted",
    ]
    return "\n".join(lines)


def _clamp(line: str, limit: int = _MAX_LINE_CHARS) -> str:
    """One console line cut to ``limit`` characters, marked with "..." when cut."""
    return line if len(line) <= limit else line[:limit - 3] + "..."


def summarize(branches: list, log_path: str) -> str:
    """The three console lines, each at most _MAX_LINE_CHARS: what blocked (the count, then at
    most the first _SHOWN_ITEMS branches, each escaped with _printable and then cut to
    _MAX_ITEM_CHARS, so a newline or terminal escape in a git error text cannot break the
    three-line form), WHY, and the one action that clears it followed by the detail log path.
    The count precedes the list so a cut line keeps it. A log path with any non-printable
    character, or one that cannot fit whole, raises before its length is used, and the caller
    then shows the fallback. PATH BUDGET: with the shorter wording the log path may be at most
    122 characters, so the store path at most 79 (see CONSOLE AND DETAIL LOG)."""
    if _printable(log_path) != log_path:
        raise ValueError("detail log path has a non-printable character")
    shown = [_clamp(_printable("%s (+%s)" % (name, ahead)), _MAX_ITEM_CHARS)
             for name, ahead in branches[:_SHOWN_ITEMS]]
    if len(branches) > _SHOWN_ITEMS:
        head = "%d branch(es) outstanding or not verifiable; first %d: " % (len(branches), len(shown))
    else:
        head = "%d branch(es) outstanding or not verifiable: " % len(branches)
    for form in ("CONSIDER INSTEAD: merge or hold each branch; detail log: %s",
                 "CONSIDER INSTEAD: merge or hold; log: %s"):
        action = form % log_path
        if len(action) <= _MAX_LINE_CHARS:
            break
    else:
        raise ValueError("detail log path does not fit one console line")
    return "\n".join([
        _clamp("BLOCKED (turn-end-outstanding-work): " + head + ", ".join(shown)),
        _clamp("WHY: a turn-end yield strands unmerged work ahead of main for the next session."),
        action,
    ])


def _git_tree_marker(directory) -> str | None:
    """What places ``directory`` inside a git working tree, or None: the first `.git` entry (of
    any type) in it or an ancestor up to the filesystem root, on the lexical path and on the
    resolved path, then `git rev-parse --is-inside-work-tree` exiting 0 there with every
    inherited GIT_* variable removed (so neither GIT_DIR nor a ceiling changes discovery). A
    missing git binary leaves the `.git` walk as the check; any other failure raises."""
    lexical = Path(os.path.abspath(directory))
    for start in (lexical, lexical.resolve()):
        for candidate in (start, *start.parents):
            try:
                os.lstat(candidate / ".git")
            except (FileNotFoundError, NotADirectoryError):
                continue
            return str(candidate / ".git")
    root = lexical
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env["LC_ALL"] = "C"
    try:
        result = subprocess.run(['git', '-C', str(root), 'rev-parse', '--is-inside-work-tree'],
                                stdin=subprocess.DEVNULL, capture_output=True, env=env,
                                timeout=_DETAIL_TIMEOUT_S, check=False)
    except FileNotFoundError:
        return None
    return "git rev-parse" if result.returncode == 0 else None


def _detail_dir():
    """The store directory holding the detail log subdirectory: _DETAIL_STORE (GRC_STORE, else
    <repo-parent>/private). None when no store resolves; raises when the store is inside this
    checkout or inside any git working tree (detail never lands in a git tree)."""
    if _DETAIL_STORE is None:
        return None
    found = Path(os.path.abspath(_DETAIL_STORE))
    if found.resolve().is_relative_to(Path(REPO).resolve()):
        raise PermissionError(errno.EPERM, "store resolves inside this checkout", str(found))
    marker = _git_tree_marker(found)
    if marker is not None:
        raise PermissionError(errno.EPERM, "store is inside a git working tree (%s)" % marker,
                              str(found))
    return found


def _append_private(directory, name: str, text: str) -> str:
    """Append ``text`` to ``directory/_DETAIL_SUBDIR/name`` without following a symlink at the
    directory, the subdirectory or the file. The subdirectory must be owned by this uid with no
    group or other write bit; the file must be a singly linked regular file owned by this uid,
    mode 0600; after the write the returned path must still name the written file (same st_dev
    and st_ino). Any failure raises; the caller then fails open to the console."""
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    top = os.open(directory, flags)
    try:
        try:
            os.mkdir(_DETAIL_SUBDIR, 0o700, dir_fd=top)
        except FileExistsError:
            pass
        sub = os.open(_DETAIL_SUBDIR, flags, dir_fd=top)
    finally:
        os.close(top)
    try:
        info = os.fstat(sub)
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.geteuid()
                or info.st_mode & (stat.S_IWGRP | stat.S_IWOTH)):
            raise PermissionError(errno.EPERM, "detail log directory is not private", _DETAIL_SUBDIR)
        fd = os.open(name, os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW
                     | os.O_NONBLOCK | os.O_CLOEXEC, 0o600, dir_fd=sub)
    finally:
        os.close(sub)
    path = os.path.join(os.fspath(directory), _DETAIL_SUBDIR, name)
    try:
        info = os.fstat(fd)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid()
                or info.st_nlink != 1):
            raise PermissionError(errno.EPERM, "detail log is not a private regular file", name)
        os.fchmod(fd, 0o600)
        data = text.encode("utf-8", errors="backslashreplace")
        while data:
            written = os.write(fd, data)
            if written <= 0:
                raise OSError(errno.EIO, "short write to detail log", name)
            data = data[written:]
        named = os.lstat(path)
        if (named.st_dev, named.st_ino) != (info.st_dev, info.st_ino):
            raise PermissionError(errno.EPERM, "detail log path was replaced during the write", name)
    finally:
        os.close(fd)
    return path


def _write_detail_log(detail: str, payload) -> str:
    """Append the full refusal detail to this session's log and return its path, or raise."""
    session = payload.get("session_id") if isinstance(payload, dict) else None
    if not isinstance(session, str) or not _SESSION_ID.fullmatch(session):
        raise ValueError("no usable session_id in the Stop payload")
    directory = _detail_dir()
    if directory is None:
        raise FileNotFoundError(errno.ENOENT, "no private store directory resolved for the detail log")
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    name = "%s.%s.log" % (_DETAIL_NAME, session[:_SESSION_PREFIX_CHARS])
    return _append_private(directory, name, "=== %s turn-end-outstanding-work session %s ===\n%s\n\n"
                           % (stamp, session, detail))


def _bounded_write(detail: str, payload) -> str:
    """_write_detail_log in a daemon thread joined for at most _DETAIL_TIMEOUT_S seconds, so a
    stalled filesystem cannot delay the refusal; a timeout raises and the caller fails open."""
    import threading
    box = {}

    def work():
        try:
            box["path"] = _write_detail_log(detail, payload)
        except Exception as exc:
            box["error"] = exc

    worker = threading.Thread(target=work, name="stop-hook-detail-log", daemon=True)
    worker.start()
    worker.join(_DETAIL_TIMEOUT_S)
    if worker.is_alive():
        raise TimeoutError(errno.ETIMEDOUT, "detail log write exceeded %gs" % _DETAIL_TIMEOUT_S)
    if "error" in box:
        raise box["error"]
    return box["path"]


def _route_refusal(detail: str, branches: list, payload) -> str:
    """Short console form after a successful log write; otherwise the console fallback: the
    refusal with one NOTE line before the branch list, which is cut at _FALLBACK_ITEMS with the
    rest counted (fail open to visibility, never to silence). Should that rendering fail, or
    lack the NOTE, the full detail is shown with the NOTE after it."""
    state = "not written"
    try:
        path = _bounded_write(detail, payload)
        state = "written but not summarized"
        return summarize(branches, path)
    except Exception as exc:
        try:
            why = _printable("%s: %s" % (type(exc).__name__, exc))
        except Exception:
            why = type(exc).__name__
        note = _clamp("NOTE: detail log %s (%s); detail shown here." % (state, why))
        try:
            shown = decide(False, False, branches, shown=_FALLBACK_ITEMS, note=note)
        except Exception:
            shown = None
        if not isinstance(shown, str) or note not in shown:
            return detail + "\n" + note
        return shown


def _fail_open() -> int:
    """Allow the stop, consuming a present one-shot escape first so a malformed or
    non-object Stop payload cannot leave the ``.allow-stop`` sentinel behind to
    authorize a LATER stop (one-shot parity with block-idle-stop, which consumes at
    top). Fails open regardless of whether the sentinel was present or the unlink
    succeeded, because a malformed payload gives no readable loop-termination signal."""
    try:
        ESCAPE_FILE.unlink()
    except OSError:
        pass
    return 0


def main() -> int:
    try:
        payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except Exception:
        return _fail_open()                   # unparseable payload: consume escape, then fail open
    if not isinstance(payload, dict):
        return _fail_open()                   # non-object payload: consume escape, then fail open
    try:
        if payload.get("stop_hook_active"):
            return 0
        if is_worker_session():
            # A dispatched worker cannot discharge ANY of this guard's remedies: it cannot
            # merge the orchestrator's branch (merging is orchestrator-only work), it cannot
            # write the `_private` held-branches record, and it cannot create the escape file,
            # all three sitting outside a worker's writable root. So the guard could only wedge
            # a worker at the end of an order it had already completed. The branch it names is
            # the ORCHESTRATOR's outstanding work, and the orchestrator's own turn-end is where
            # that gets enforced. Observed 2026-08-20: a /validate-pr worker delivered its full
            # verdict, then spent its remaining turns unable to satisfy or escape this guard.
            return 0
        if ESCAPE_FILE.exists():
            try:
                ESCAPE_FILE.unlink()          # one-shot: CONSUME before granting
            except OSError:
                pass                          # a failed unlink must NOT grant the stop (else the
                                              # sentinel persists = the permanent standing state the
                                              # docstring rules out); fall through to block instead
            else:
                return 0                      # granted ONLY after a successful consume
        branches = unmerged_branches()
        try:
            message = decide(False, False, branches)
        except Exception:
            if not branches:
                return 0
            # The scan established a block; a rendering error must not erase it.
            # Escape handling above remains independent of this fallback.
            message = ("BLOCKED (turn-end-outstanding-work): cannot format outstanding work; "
                       "one-shot escape: touch " + str(ESCAPE_FILE))
        else:
            if message:
                # Wording and routing only: the full detail goes to the session log and the
                # console gets three lines, or the full detail when the log cannot be written.
                message = _route_refusal(message, branches, payload)
        if message:
            try:
                print(message, file=sys.stderr)
            except UnicodeError:
                print(message.encode("ascii", errors="backslashreplace").decode("ascii"),
                      file=sys.stderr)
            return 2
    except Exception:
        return 0                              # fail open, deliberately
    return 0


SELF_TEST = [
    ("clean tree allows",            (False, False, []),           False),
    ("continuation never blocks",    (True,  False, [("b", "1")]), False),
    ("escape file never blocks",     (False, True,  [("b", "1")]), False),
    ("one unmerged branch blocks",   (False, False, [("b", "1")]), True),
]


def self_test() -> int:
    import io
    from unittest import mock

    bad = 0
    for name, args, should_block in SELF_TEST:
        got = decide(*args) is not None
        if got != should_block:
            bad += 1
            print("FAIL " + name + ": want " + ("BLOCK" if should_block else "allow")
                  + ", got " + ("BLOCK" if got else "allow"))

    # Worker scoping lives in main(), not the pure branch decision. Assert that a
    # positively identified worker returns before it probes either the escape or branches.
    module = sys.modules[__name__]
    worker_escape = mock.Mock()
    with mock.patch.dict(
        os.environ, {"CLAUDE_CONFIG_DIR": "/run/orch/orch-worker.Ab3xZ9"}
    ), mock.patch.object(
        sys, "stdin", io.StringIO("{}")
    ), mock.patch.object(
        module, "ESCAPE_FILE", worker_escape
    ), mock.patch.object(
        module, "unmerged_branches"
    ) as branch_scan:
        worker_rc = main()
    if worker_rc != 0 or worker_escape.exists.called or branch_scan.called:
        bad += 1
        print("FAIL worker session allows before escape/branch probes")

    # A normal orchestrator path must retain the current branch-blocking contract.
    orchestrator_escape = mock.Mock()
    orchestrator_escape.exists.return_value = False
    with mock.patch.dict(
        os.environ, {"CLAUDE_CONFIG_DIR": "/opt/orch-accounts/test/orchestrator"}
    ), mock.patch.object(
        sys, "stdin", io.StringIO("{}")
    ), mock.patch.object(
        sys, "stderr", io.StringIO()
    ), mock.patch.object(
        module, "ESCAPE_FILE", orchestrator_escape
    ), mock.patch.object(
        module, "unmerged_branches", return_value=[("b", "1")]
    ) as branch_scan:
        orchestrator_rc = main()
    if orchestrator_rc != 2 or branch_scan.call_count != 1:
        bad += 1
        print("FAIL orchestrator session did not retain branch block")

    # A malformed/unparseable Stop payload must fail OPEN (rc 0), even with branches
    # present, so a harness or environment error never blocks turn-end (the fail-open
    # design; parity with block-idle-stop-with-actionable-backlog.py). Also asserts the
    # parse-error path short-circuits BEFORE the branch scan.
    malformed_escape = mock.Mock()
    malformed_escape.exists.return_value = True   # sentinel present: must be consumed on the fail-open path
    with mock.patch.dict(
        os.environ, {"CLAUDE_CONFIG_DIR": "/opt/orch-accounts/test/orchestrator"}
    ), mock.patch.object(
        sys, "stdin", io.StringIO("{not valid json")
    ), mock.patch.object(
        sys, "stderr", io.StringIO()
    ), mock.patch.object(
        module, "ESCAPE_FILE", malformed_escape
    ), mock.patch.object(
        module, "unmerged_branches", return_value=[("b", "1")]
    ) as malformed_branch_scan:
        malformed_rc = main()
    if malformed_rc != 0 or malformed_branch_scan.called or not malformed_escape.unlink.called:
        bad += 1
        print("FAIL malformed payload did not fail open + consume the escape")

    # And a malformed payload with NO sentinel present + an unmerged branch must STILL
    # fail open (rc 0) WITHOUT scanning branches - the case the F1 fix repairs (the
    # pre-fix code fell through to a branch-block return 2). Distinct from the
    # present-sentinel case above, which the pre-fix code also allowed via the escape.
    absent_escape = mock.Mock()
    absent_escape.exists.return_value = False
    absent_escape.unlink.side_effect = FileNotFoundError   # no sentinel on disk
    with mock.patch.dict(
        os.environ, {"CLAUDE_CONFIG_DIR": "/opt/orch-accounts/test/orchestrator"}
    ), mock.patch.object(
        sys, "stdin", io.StringIO("{not valid json")
    ), mock.patch.object(
        sys, "stderr", io.StringIO()
    ), mock.patch.object(
        module, "ESCAPE_FILE", absent_escape
    ), mock.patch.object(
        module, "unmerged_branches", return_value=[("b", "1")]
    ) as absent_branch_scan:
        absent_rc = main()
    if absent_rc != 0 or absent_branch_scan.called:
        bad += 1
        print("FAIL malformed payload with no sentinel did not fail open")

    # Console form: three lines, the count and at most the first _SHOWN_ITEMS branches.
    many = [("b%d" % n, "1") for n in range(5)]
    short = summarize(many, "/store/x.log")
    if (len(short.splitlines()) != 3 or "5 branch(es)" not in short or "b2 (+1)" not in short
            or "b3" in short or "first 3: " not in short or not short.endswith("/store/x.log")
            or max(map(len, short.splitlines())) > _MAX_LINE_CHARS):
        bad += 1
        print("FAIL summarize did not cap the console list at three")

    # No usable session_id: the refusal stays visible with the NOTE before the list, and
    # nothing is written.
    detail = decide(False, False, many)
    with mock.patch.object(module, "_detail_dir") as no_dir:
        routed = _route_refusal(detail, many, {})
    if ("NOTE: detail log not written" not in routed or no_dir.called
            or not routed.startswith("BLOCKED (turn-end-outstanding-work): ")
            or routed.index("NOTE:") > routed.index("Branches outstanding")
            or "b4 (+1)" not in routed or "more, not shown" in routed):
        bad += 1
        print("FAIL missing session_id did not fail open to the visible refusal")

    # The fallback list stops at _FALLBACK_ITEMS branches and counts the rest.
    lots = [("b%d" % n, "1") for n in range(_FALLBACK_ITEMS + 4)]
    routed = _route_refusal(decide(False, False, lots), lots, {})
    if ("b%d (+1)" % (_FALLBACK_ITEMS - 1) not in routed or "b%d (+1)" % _FALLBACK_ITEMS in routed
            or "... and 4 more, not shown here" not in routed):
        bad += 1
        print("FAIL the console fallback did not cap the branch list")

    # A usable session and store: the detail is appended to a 0600 log and three lines return.
    import tempfile
    with tempfile.TemporaryDirectory() as store, mock.patch.object(
        module, "_detail_dir", return_value=Path(store)
    ):
        routed = _route_refusal(detail, many, {"session_id": "self-test-1"})
        log = Path(store) / _DETAIL_SUBDIR / "turn-end.self-test-1.log"
        logged = log.read_text(encoding="utf-8") if log.is_file() else ""
        mode = stat.S_IMODE(os.lstat(log).st_mode) if log.is_file() else None
    try:
        expected = summarize(many, str(log))
    except ValueError:
        expected = None  # a TMPDIR beyond the PATH BUDGET: the fallback is the right answer
    shown_ok = (routed == expected if expected is not None
                else "NOTE: detail log written but not summarized" in routed)
    if not shown_ok or "b4 (+1)" not in logged or mode != 0o600:
        bad += 1
        print("FAIL detail log was not written privately with the short console form")

    # A short fixed directory, so this case never depends on TMPDIR: a 79-character store
    # path fits the shorter wording exactly, and one more character does not.
    fixed = "/" + "s" * 78 + "/" + _DETAIL_SUBDIR + "/turn-end.0123456789ab.log"
    try:
        fits = summarize(many, fixed).endswith("; log: " + fixed)
    except ValueError:
        fits = False
    try:
        summarize(many, "/s" + fixed)
        overflow = False
    except ValueError:
        overflow = True
    if not fits or not overflow:
        bad += 1
        print("FAIL the documented store-path budget does not hold")

    # A log path with a newline, a carriage return or an escape is never advertised raw.
    for odd in ("\n", "\r", "\x1b"):
        try:
            summarize(many, "/store" + odd + "x.log")
        except ValueError:
            continue
        bad += 1
        print("FAIL summarize advertised a log path with %r" % odd)

    total = len(SELF_TEST) + 12
    print(str(total - bad) + "/" + str(total) + " decision cases pass")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
