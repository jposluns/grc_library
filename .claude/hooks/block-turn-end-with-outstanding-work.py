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
<root>/stop-hook-detail/turn-end.<first 12 characters of session_id>.log (each entry's header
carries the whole session_id), where <root> is the fixed per-account detail log root
<home>/.local/state/grc (_open_detail_root), the same root stop-guard-unattended.py uses,
through helpers identical in both hooks. <home> is the password-database home of the effective
uid (_detail_home); neither HOME nor XDG_STATE_HOME is read, so a session's environment cannot
move the log (tests replace it through _DETAIL_HOME). The log is never written into the
operator's store (GRC_STORE, else <repo-parent>/private), and detail logs already in
<store>/stop-hook-detail are neither moved nor deleted. The detail log never uses
lint_common.resolve_working, whose transitional fallback can name a `.working` directory inside
a git checkout. The text returned
to the harness is then three short lines (summarize()), each at most _MAX_LINE_CHARS
characters: what blocked, with the branch count and at most the first _SHOWN_ITEMS branches
(each escaped with _printable, then cut to _MAX_ITEM_CHARS); WHY; and the one action that
clears it, which names the held-branches record path and the one-shot escape (touch of
ESCAPE_FILE) when they fit, so the reader learns the remedy without opening the log (as
stop-guard-unattended.py keeps its escape on the console, #2496): both, else the escape alone,
else the held path alone, each with the log path ending the action line or, failing that, the
WHY line; when neither path fits, the action names only the log path (the log holds both). A
held or escape path that is unset or has any non-printable character stays in the log only.
PATH BUDGET: the log path adds 43 characters to the root path (with a 12-character session
prefix), so the short form fits a root path of at most 79 characters (60 with the longer
wording; a shorter one still when the held path or the escape is shown), that is a home of at
most 62 characters (the root adds 17); a longer root path, or a log path with any non-printable
character (a newline, a carriage return, a terminal escape or a Unicode space separator other
than the ASCII space, tested with _printable), falls back as below. A root inside this checkout,
or inside any git working tree or bare repository (a `.git` entry in the root or any ancestor up
to the filesystem root, lexically or after resolving symlinks, or `git rev-parse
--is-inside-work-tree` exiting 0, as it does in a working tree and inside a bare repository, run
with every inherited GIT_* variable removed in the deepest level of the root's path that
exists), is refused before anything is created. The root is opened
without following a symlink anywhere on its path ("/" first, then each component relative to the
one before, with O_NOFOLLOW), and each open directory is checked with fstat: every directory
above the home owned by root or this uid with no group or other write bit, unless root-owned and
sticky; the home, .local and .local/state owned by this uid with no group or other write bit;
grc owned by this uid with no group or other access. Missing directories from .local down are
created with mode 0700; nothing is created at or above the home, and no existing directory is
changed. A `.git` entry in grc or in the subdirectory is refused, and the git working tree check
runs again after the walk, whether or not a directory was created, immediately before the root
is returned for the write, so a `.git` planted meanwhile at a level that already existed is
refused too. The subdirectory must be owned by this uid with no group or other access; the file
must be regular, mode 0600, owned by this uid and singly linked; and after the write the
advertised path must still name the written file (lstat st_dev and st_ino against the
descriptor's fstat). The resolution, checks, open and write run in a daemon thread joined for at
most _DETAIL_TIMEOUT_S seconds, and the git working tree checks get only the time left, so a
stalled filesystem cannot delay the refusal. If the log cannot be written (no usable session_id
in the Stop payload, no password-database entry or an unusable home, a root inside this checkout,
a git working tree or a bare repository, a symlink, a wrong owner or mode, a timeout, or any
open, check or write failure), or the log path cannot be shown on one console line, the console
fallback is returned
instead: the BLOCKED and WHY lines, one NOTE line naming the failure (_note_line: the cause's
type and reason and, for an OSError naming one path, that path; when the line would exceed
_MAX_LINE_CHARS, only the path is shortened (_shorten_path), to the room the form, the state,
the reason and the quoting around the path (the ": '" before it and the "'" after it) leave of
_MAX_LINE_CHARS, so the entry it names, such as a .git, is shown only when that room holds its
name, and the path can shrink to the elision mark alone; when even the mark does not fit, and
for any other cause whose line is too long, the whole line is cut to _MAX_LINE_CHARS ending in
the mark (_clamp), which drops the end of the line, then the path, then the end of the reason),
then the branch list cut at the first _FALLBACK_ITEMS branches (the pre-2026-11-04 console cap)
with one line counting the rest, the held-branches path and the one-shot escape. Every branch
item the fallback shows is escaped with _printable, and so is every item of the last-resort form
(the full detail with the NOTE after it, used when the fallback cannot be rendered), so a
newline or terminal escape in a git error text cannot start a console line on any path; the
detail log keeps the raw text. The held-branches path and the one-shot escape path are escaped
with _printable wherever decide() renders them (the fallback, the last-resort form and the
detail log alike), and so is the escape path in main()'s cannot-format refusal and every path
the hook-helper-isolation refusal names, so a newline or terminal escape in a path cannot start
a console line either. This fails open to visibility, never to silence: the count is always
shown, and when the log was written the full list is there. RESIDUE: when the log was not
written, branches past the first _FALLBACK_ITEMS are named nowhere, as before 2026-11-04. Exit
status, the escape and stop_hook_active handling are unchanged. RESIDUE: a home kept in a git
working tree or a bare repository refuses every log (visibly, through the NOTE), with no second
location; a bare repository is not seen when git's configuration sets safe.bareRepository to
explicit; a `.git`
planted above grc, or in grc itself, between the last git working tree check and the file open
is not seen (only this uid or root can plant one there); the log is appended to without
rotation; two sessions
whose ids share their first 12 characters share one log file (each entry names its session); a
write that times out may still complete later in the abandoned thread, and the process exit can
still wait on a syscall the kernel does not let a fatal signal interrupt.
"""

from __future__ import annotations

import datetime as _dt
import errno
import json
import os
import pwd
import re as _re
import stat
import subprocess
import sys
import time
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
        # A launch path holding a newline or a terminal escape is shown escaped: every
        # character that is neither printable nor a space separator (this runs before
        # _printable is defined, and keeps the rule the repository's other hooks use).
        import unicodedata
        why = "".join(char if char.isprintable() or unicodedata.category(char) == "Zs"
                      else ascii(char)[1:-1] for char in why)
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
# _clamp's per-line byte bound, shared with stop-guard-unattended.py, whose fallback needs
# it to fit PIPE_BUF: any valid 160-character UTF-8 line fits, so only a line holding lone
# surrogates is cut further.
_MAX_LINE_BYTES = 640
_DETAIL_SUBDIR = "stop-hook-detail"
_DETAIL_NAME = "turn-end"
_SESSION_PREFIX_CHARS = 12
_DETAIL_TIMEOUT_S = 2.0
_SESSION_ID = _re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}", _re.ASCII)


# The detail log root, <home>/.local/state/grc, under the password-database home of the effective
# uid (_detail_home). No environment variable moves it; tests set _DETAIL_HOME (None: the lookup).
_DETAIL_ROOT_PARTS = (".local", "state", "grc")
_DETAIL_HOME = None
# The mark _shorten_path puts where it drops part of a path a NOTE line names, and _clamp
# puts at the end of a line it cuts.
_ELISION = "..."
# Set to 1 to let a self-test real detail log write skip, with the reason, on a host whose
# temporary directory cannot provide a fixture home that meets the root's rule; unset, it fails.
# tests/test_linters.py applies the same rule with the same variable.
_UNSAFE_TMP_SKIP_ENV = "GRC_ALLOW_UNSAFE_TMP_SKIP"


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


def _printable(value):
    """``value`` as text with every character that is not printable shown as its ascii()
    escape: a control character, and a Unicode space separator (category Zs) other than the
    ASCII space, among others. Used for console lines and the detail log in both Stop hooks."""
    return "".join(ch if ch.isprintable() else ascii(ch)[1:-1] for ch in str(value))


def _shell_word(text) -> str:
    """``text`` as ONE shell word that names the path ``text`` and prints on one line, for a
    command a refusal tells the reader to run (escaping a shell-quoted word would change the
    path the command names): shlex.quote when every character is printable or a space
    separator, else a bash ANSI-C quoted $'...' word in which a backslash or a single quote is
    backslash-escaped and every other character outside that rule is an escape bash reads
    back in any locale: below 0x80 the ascii() escape _printable shows, such as \\n or
    \\x1b; from 0x80 up, a surrogate-escaped byte included, \\xHH for each byte os.fsencode
    gives: the path's own bytes in this process's filesystem encoding, which bash rebuilds in
    any locale (a \\uHHHH escape stayed literal outside a UTF-8 locale, round 4, claude W1;
    UTF-8 bytes named another path when the hook ran in a non-UTF-8 locale, round 5, claude
    N3). A character that encoding cannot hold keeps its UTF-8 bytes. A relative
    path starting with "-" is written "./" first, so touch, cd, git -C or python3 cannot
    read it as an option (round 4, codex W2)."""
    import shlex
    import unicodedata
    text = str(text)
    if text.startswith("-"):
        text = "./" + text

    def plain(char):
        return char.isprintable() or unicodedata.category(char) == "Zs"

    if all(plain(char) for char in text):
        return shlex.quote(text)
    out = []
    for char in text:
        code = ord(char)
        if char in "\\'":
            out.append("\\" + char)
        elif plain(char):
            out.append(char)
        elif code < 0x80:
            out.append(ascii(char)[1:-1])  # \n, \r, \t or \xHH: the escape _printable shows
        else:
            try:
                data = os.fsencode(char)  # a surrogate-escaped byte gives that byte back
            except UnicodeEncodeError:
                data = char.encode("utf-8", "surrogatepass")
            out.append("".join("\\x%02x" % byte for byte in data))
    return "$'" + "".join(out) + "'"


def _branch_display(ref: bytes) -> str:
    """A branch ref shown without its refs/heads/ prefix: a byte that is not UTF-8 and every
    character that is neither printable nor a Unicode space separator are escaped, so a space
    separator a branch name holds is shown as it is (_printable, by contrast, escapes it)."""
    import unicodedata
    text = ref.removeprefix(b"refs/heads/").decode("utf-8", errors="backslashreplace")
    return "".join(char if char.isprintable() or unicodedata.category(char) == "Zs"
                   else ascii(char)[1:-1] for char in text)


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
    console fallback (_route_refusal) passes ``shown``, which keeps that many branches, each
    escaped with _printable (the detail log form keeps the raw text), and counts the rest on
    one line, and ``note``, placed before the list. The held-branches path and the one-shot
    escape path are escaped with _printable on every form."""
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
        if shown is None:
            lines += ["    - %s (+%s)" % (n, a) for n, a in listed]
        else:
            lines += ["    - " + _printable("%s (+%s)" % (n, a)) for n, a in listed]
        if len(listed) < len(branches):
            lines.append("    ... and %d more, not shown here" % (len(branches) - len(listed)))
        lines.append("    Held-branches record path:")
        # Show the ACTUAL resolved held-branches path (resolve_working -> local store), never a
        # hardcoded sibling path, so the remediation the guard prints follows the store migration.
        lines.append("      %s" % (_printable(str(HELD_FILE)) if HELD_FILE is not None
                                   else "the held-branches file (resolved via lint_common.resolve_working)"))
    lines += [
        "",
        "CONSIDER INSTEAD: merge the branch(es) above, or record the hold with its reason in the "
        "held-branches file. For a genuine block (CI, a maintainer decision, an external wait), record that blocker, then run:",
        # One shell word naming the escape path itself (_shell_word), so the command, copied, touches it.
        f"      touch {_shell_word(ESCAPE_FILE)}     # honoured once, then deleted",
    ]
    return "\n".join(lines)


def _clamp(line, limit=_MAX_LINE_CHARS):
    """``line`` as one console line of at most ``limit`` characters (``limit`` at least
    len(_ELISION)) and _MAX_LINE_BYTES encoded bytes: whole when it fits both, else cut to fit
    them, ending in _ELISION."""
    if len(line) <= limit and len(line.encode("utf-8", "backslashreplace")) <= _MAX_LINE_BYTES:
        return line
    line = line[:limit - len(_ELISION)]
    while len((line + _ELISION).encode("utf-8", "backslashreplace")) > _MAX_LINE_BYTES:
        line = line[:-1]
    return line + _ELISION


def _console_path(path) -> str | None:
    """``path`` as console text for the short form, or None when it is unset or holds any
    non-printable character: the short form then leaves that path to the detail log (which
    escapes it) rather than show an escaped path that a reader could take for the literal one."""
    if path is None:
        return None
    text = str(path)
    return text if _printable(text) == text else None


def summarize(branches: list, log_path: str) -> str:
    """The three console lines, each at most _MAX_LINE_CHARS: what blocked (the count, then at
    most the first _SHOWN_ITEMS branches, each escaped with _printable and then cut to
    _MAX_ITEM_CHARS, so a newline or terminal escape in a git error text cannot break the
    three-line form), WHY, and the one action that clears it, with the detail log path.
    The action names the held-branches record path (HELD_FILE) and the one-shot escape
    (ESCAPE_FILE, as one shell word, with its condition "once, after recording it") when they
    fit, so the remedy is on the console (as stop-guard-unattended.py
    keeps its escape there, #2496): first both, then the escape alone, then the held path
    alone. Each wording is tried with the log path ending the action line, then with the log
    path ending the WHY line; when none fits, the action names only the log path, which holds
    both. A held or escape path that is unset or has any non-printable character is left to
    the log. The count precedes the list so a cut line keeps it. A log path with any
    non-printable character, or one that cannot fit whole, raises before its length is used,
    and the caller then shows the fallback. PATH BUDGET: with the shortest wording the log
    path may be at most 122 characters, so the store path at most 79 (see CONSOLE AND DETAIL
    LOG); every wording that names the held path or the escape needs a shorter log path."""
    if _printable(log_path) != log_path:
        raise ValueError("detail log path has a non-printable character")
    shown = [_clamp(_printable("%s (+%s)" % (name, ahead)), _MAX_ITEM_CHARS)
             for name, ahead in branches[:_SHOWN_ITEMS]]
    if len(branches) > _SHOWN_ITEMS:
        head = "%d branch(es) outstanding or not verifiable; first %d: " % (len(branches), len(shown))
    else:
        head = "%d branch(es) outstanding or not verifiable: " % len(branches)
    held, escape = _console_path(HELD_FILE), _console_path(ESCAPE_FILE)
    # The escape is honoured once (decide()'s "# honoured once, then deleted"), as stop-guard's
    # "(once, after recording the blocker)" says; the path is one shell word (_shell_word), so a
    # path with a space or a quote is still the path the copied command touches.
    escape = None if escape is None else _shell_word(escape)
    remedies = []
    if held is not None and escape is not None:
        remedies.append("merge, or hold in " + held + "; genuine block (once, after recording "
                        "it): touch " + escape)
    if escape is not None:
        remedies.append("merge or hold; genuine block (once, after recording it): touch " + escape)
    if held is not None:
        remedies.append("merge, or hold in " + held)
    why = "WHY: a turn-end yield strands unmerged work ahead of main for the next session."
    candidates = []
    for remedy in remedies:
        candidates.append((why, "CONSIDER INSTEAD: " + remedy + "; log: " + log_path))
        for logged_why in ("WHY: a turn-end yield strands unmerged work ahead of main; "
                           "detail log: " + log_path,
                           "WHY: a turn-end yield strands unmerged work; log: " + log_path):
            candidates.append((logged_why, "CONSIDER INSTEAD: " + remedy))
    candidates += [(why, "CONSIDER INSTEAD: merge or hold each branch; detail log: " + log_path),
                   (why, "CONSIDER INSTEAD: merge or hold; log: " + log_path)]
    for why_line, action in candidates:
        if len(why_line) <= _MAX_LINE_CHARS and len(action) <= _MAX_LINE_CHARS:
            break
    else:
        raise ValueError("detail log path does not fit one console line")
    return "\n".join([
        _clamp("BLOCKED (turn-end-outstanding-work): " + head + ", ".join(shown)),
        why_line,
        action,
    ])


def _append_private(top, directory, name, text):
    """Append ``text`` to ``directory/_DETAIL_SUBDIR/name``, where ``top`` is the descriptor
    _open_detail_root returned for ``directory`` (the caller closes it), without following a
    symlink at the subdirectory or the file. The subdirectory must be owned by this uid with no
    group or other access and hold no `.git` entry; the file must be a singly linked regular
    file owned by this uid, mode 0600; after the write the returned path must still name the
    written file (same st_dev and st_ino). Any failure raises; the caller then fails open."""
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    try:
        os.mkdir(_DETAIL_SUBDIR, 0o700, dir_fd=top)
    except FileExistsError:
        pass
    sub = os.open(_DETAIL_SUBDIR, flags, dir_fd=top)
    try:
        info = os.fstat(sub)
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.geteuid()
                or info.st_mode & 0o077):
            raise PermissionError(errno.EPERM, "detail log directory is not private", _DETAIL_SUBDIR)
        try:
            os.stat(".git", dir_fd=sub, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise PermissionError(errno.EPERM, "detail log directory holds a .git entry",
                                  os.path.join(os.fspath(directory), _DETAIL_SUBDIR, ".git"))
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
        data = text.encode("utf-8", "backslashreplace")
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


def _git_tree_marker(directory, timeout):
    """What places ``directory`` inside a git working tree or a bare repository, or None: the
    first `.git` entry (of any type) in it or an ancestor up to the filesystem root, on the
    lexical path and on the resolved path, then `git rev-parse --is-inside-work-tree` exiting 0
    with every inherited GIT_* variable removed (so neither GIT_DIR nor a ceiling changes
    discovery), bounded by ``timeout``. git runs in the deepest of ``directory`` and its
    ancestors that exists (lexically), so a directory not yet created is checked where it
    would be created; inside a bare repository git prints "false" and still exits 0, so a bare
    repository is found before anything is created in it, unless git's own configuration sets
    safe.bareRepository to explicit (git then refuses the repository and exits nonzero). A
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
    while root != root.parent and not os.path.lexists(root):
        root = root.parent
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env["LC_ALL"] = "C"
    try:
        result = subprocess.run(['git', '-C', str(root), 'rev-parse', '--is-inside-work-tree'],
                                stdin=subprocess.DEVNULL, capture_output=True, env=env,
                                timeout=max(timeout, 0.01), check=False)
    except FileNotFoundError:
        return None
    return "git rev-parse" if result.returncode == 0 else None


def _refuse_git_tree(root, timeout):
    """Raise PermissionError when ``root`` is inside a git working tree or a bare repository
    (_git_tree_marker, within ``timeout`` seconds); the reason says "git working tree" for
    both. The error's path is the `.git` entry found, so a NOTE line that must shorten it still
    ends with that entry; when only git rev-parse placed the root in a repository, as for a
    bare repository, the path is the root and the reason says so."""
    marker = _git_tree_marker(root, timeout)
    if marker is None:
        return
    if marker == "git rev-parse":
        raise PermissionError(errno.EPERM, "detail log root is inside a git working tree "
                              "(git rev-parse)", root)
    raise PermissionError(errno.EPERM, "detail log root is inside a git working tree", marker)


def _shorten_path(path, room):
    """``path`` in at most max(``room``, len(_ELISION)) characters: whole when it fits; else its
    middle components replaced by _ELISION, keeping as many of its last components as fit (the
    last names the offending entry, such as a .git) and its first component when that fits
    too, as in "/var/.../home/.git". Only a last component longer than ``room`` allows is
    itself cut, from the left, behind _ELISION; with ``room`` at most len(_ELISION), only
    _ELISION is left."""
    if len(path) <= room:
        return path
    parts = path.split("/")
    lead = 2 if parts[0] == "" else 1
    head = "/".join(parts[:lead])
    for keep in range(len(parts) - lead, 0, -1):
        tail = "/".join(parts[-keep:])
        for shown in (head + "/" + _ELISION + "/" + tail, _ELISION + "/" + tail):
            if len(shown) <= room:
                return shown
    last = parts[-1]
    return _ELISION + last[len(last) - max(room - len(_ELISION), 0):]


def _note_line(form, state, cause):
    """``form``, a NOTE line with %s for the log state and then the cause, filled with
    ``state`` and ``cause`` (an exception, or text already naming one), at most
    _MAX_LINE_CHARS characters. Only the cause is escaped with _printable; ``form`` and
    ``state`` are fixed internal strings and go in as given. The cause is the text itself, or
    the exception's type and its reason text. For an OSError that names one path (a filename
    and no filename2), the reason is "<type>: [Errno N] <strerror>" and the path follows it in
    single quotes, as "<reason>: '<path>'", the reason and the path each escaped on its own
    before the path is shortened. The path gets the room the form, the state, the reason and
    that quoting (the ": '" before the path and the "'" after it) leave of _MAX_LINE_CHARS:
    _shorten_path cuts the path only when it is longer than that room, so the reason stays
    whole and the path keeps as many of its last components as fit (the last names the
    offending entry, such as a .git, only when the room holds its name). Every line then goes
    through _clamp, which cuts a line longer than _MAX_LINE_CHARS to end in _ELISION: an
    OSError line when that room is shorter than both _ELISION and the path, and any other
    cause's line when its text is too long. The end of the form goes first, then the path, if
    any, then the end of the reason, so the reason is kept whole only when it ends within the
    first _MAX_LINE_CHARS - len(_ELISION) characters of the line."""
    if not isinstance(cause, BaseException):
        return _clamp(form % (state, _printable(str(cause))))
    name = type(cause).__name__
    named = cause.filename if isinstance(cause, OSError) else None
    if named is None or cause.filename2 is not None:
        return _clamp(form % (state, _printable("%s: %s" % (name, cause))))
    try:
        path = os.fsdecode(named)
    except TypeError:
        path = str(named)
    reason = _printable("%s: [Errno %s] %s" % (name, cause.errno, cause.strerror))
    path = _printable(path)
    room = _MAX_LINE_CHARS - len(form % (state, "%s: ''" % reason))
    return _clamp(form % (state, "%s: '%s'" % (reason, _shorten_path(path, room))))


def _detail_home():
    """The home of this process's effective uid in the password database (pwd.getpwuid), or
    _DETAIL_HOME when a test sets it. HOME and XDG_STATE_HOME are never read, so a session's
    environment cannot move the detail log. Raises KeyError when the uid has no entry, and
    PermissionError unless the home is an absolute, normalized path below the filesystem root."""
    home = _DETAIL_HOME
    if home is None:
        home = pwd.getpwuid(os.geteuid()).pw_dir
    home = os.fspath(home)
    if (not os.path.isabs(home) or os.path.normpath(home) != home or home.startswith("//")
            or home == "/"):
        raise PermissionError(errno.EPERM, "home directory is not an absolute normalized path "
                              "below the filesystem root", home)
    return home


def _open_detail_root(checkout, timeout):
    """Open the detail log root, <home>/.local/state/grc (_detail_home, _DETAIL_ROOT_PARTS), and
    return (its directory descriptor, its path); the caller closes the descriptor. A root
    inside ``checkout``, or inside any git working tree or bare repository (_git_tree_marker,
    whose git leg runs in the deepest existing level of the root's path, within ``timeout``
    seconds), is refused before anything is created. "/" is opened and then each component
    relative to the one before with O_NOFOLLOW, so a symlink anywhere on the path is refused,
    and every open directory is checked with fstat, never by path: each directory above the
    home must be owned by root or this uid with no group or other write bit, unless it is
    root-owned and sticky; the home, .local and .local/state must be owned by this uid with no
    group or other write bit; grc must be owned by this uid with no group or other access.
    Missing directories from .local down are created with mode 0700, and one that already
    exists is trusted only through the fstat of the descriptor then opened; nothing is created
    at or above the home, and no existing directory is changed. A `.git` entry in grc is
    refused, and the git working tree check (_refuse_git_tree) runs again after the walk,
    whether or not this call created a directory, immediately before the root is returned for
    the write. A failed open or mkdir names the whole path it reached. Any failure raises; the
    caller then fails open."""
    started = time.monotonic()
    home = _detail_home()
    root = os.path.join(home, *_DETAIL_ROOT_PARTS)
    if Path(root).resolve().is_relative_to(Path(checkout).resolve()):
        raise PermissionError(errno.EPERM, "detail log root resolves inside this checkout", root)
    _refuse_git_tree(root, timeout - (time.monotonic() - started))
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    euid = os.geteuid()
    writable = stat.S_IWGRP | stat.S_IWOTH

    def descend(parent, name, path):
        # On failure the caller still holds ``parent`` and closes it.
        try:
            child = os.open(name, flags, dir_fd=parent)
        except OSError as exc:
            if exc.errno in (errno.ELOOP, errno.ENOTDIR):
                raise PermissionError(errno.EPERM, "symlink or non-directory in detail log root "
                                      "path", path) from exc
            raise OSError(exc.errno, exc.strerror, path) from exc
        os.close(parent)
        return child

    path = "/"
    fd = os.open(path, flags)
    try:
        for name in [part for part in home.split("/") if part]:
            info = os.fstat(fd)
            if not (info.st_uid in (0, euid) and not info.st_mode & writable
                    or info.st_uid == 0 and info.st_mode & stat.S_ISVTX):
                raise PermissionError(errno.EPERM, "directory above the home is not owned by "
                                      "root or this uid, or others can write it", path)
            path = os.path.join(path, name)
            fd = descend(fd, name, path)
        for name in ("",) + _DETAIL_ROOT_PARTS:
            if name:
                path = os.path.join(path, name)
                try:
                    os.mkdir(name, 0o700, dir_fd=fd)
                except FileExistsError:
                    pass
                except OSError as exc:
                    raise OSError(exc.errno, exc.strerror, path) from exc
                fd = descend(fd, name, path)
            info = os.fstat(fd)
            private = name == _DETAIL_ROOT_PARTS[-1]
            if (not stat.S_ISDIR(info.st_mode) or info.st_uid != euid
                    or info.st_mode & (0o077 if private else writable)):
                raise PermissionError(errno.EPERM, "detail log root path component must be owned "
                                      "by this uid with no group or other %s"
                                      % ("access" if private else "write bit"), path)
        try:
            os.stat(".git", dir_fd=fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise PermissionError(errno.EPERM, "detail log root holds a .git entry",
                                  os.path.join(root, ".git"))
        # Again whether or not a directory was created, immediately before the write, so a
        # .git planted at a level that already existed, after the first check, is refused too.
        _refuse_git_tree(root, timeout - (time.monotonic() - started))
    except BaseException:
        os.close(fd)
        raise
    return fd, root


def _write_detail_log(detail: str, payload, timeout=_DETAIL_TIMEOUT_S) -> str:
    """Append the full refusal detail to this session's log under the detail log root
    (_open_detail_root, its git working tree checks within ``timeout`` seconds) and return its
    path, or raise. The operator's store is never written."""
    started = time.monotonic()
    session = payload.get("session_id") if isinstance(payload, dict) else None
    if not isinstance(session, str) or not _SESSION_ID.fullmatch(session):
        raise ValueError("no usable session_id in the Stop payload")
    top, directory = _open_detail_root(REPO, timeout - (time.monotonic() - started))
    try:
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        name = "%s.%s.log" % (_DETAIL_NAME, session[:_SESSION_PREFIX_CHARS])
        return _append_private(top, directory, name,
                               "=== %s turn-end-outstanding-work session %s ===\n%s\n\n"
                               % (stamp, session, detail))
    finally:
        os.close(top)


def _bounded_write(detail: str, payload) -> str:
    """_write_detail_log in a daemon thread joined for at most _DETAIL_TIMEOUT_S seconds, so a
    stalled filesystem cannot delay the refusal. The write gets the time left from the start of
    this call, so its git working tree checks stay within the same bound; a timeout raises and
    the caller fails open."""
    import threading
    box = {}
    started = time.monotonic()

    def work():
        try:
            box["path"] = _write_detail_log(detail, payload,
                                            _DETAIL_TIMEOUT_S - (time.monotonic() - started))
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
    rest counted (fail open to visibility, never to silence); the NOTE names the failure
    (_note_line, which keeps its reason whole only when the line has room for it). Should that
    rendering fail, or lack the NOTE, the full detail is shown with the NOTE after it
    (_last_resort)."""
    state = "not written"
    try:
        path = _bounded_write(detail, payload)
        state = "written but not summarized"
        return summarize(branches, path)
    except Exception as exc:
        form = "NOTE: detail log %s (%s); detail shown here."
        try:
            note = _note_line(form, state, exc)
        except Exception:
            note = _clamp(form % (state, type(exc).__name__))
        try:
            shown = decide(False, False, branches, shown=_FALLBACK_ITEMS, note=note)
        except Exception:
            shown = None
        if not isinstance(shown, str) or note not in shown:
            return _last_resort(detail, branches, note)
        return shown


def _last_resort(detail: str, branches: list, note: str) -> str:
    """The full detail with ``note`` after it, every branch item escaped with _printable so a
    raw newline inside an item cannot start a console line. When the escaped items cannot be
    rendered, the whole detail is escaped onto one line instead (visible, never silent)."""
    try:
        safe = decide(False, False, [(_printable(str(n)), _printable(str(a))) for n, a in branches])
    except Exception:
        safe = None
    if not isinstance(safe, str):
        safe = _printable(detail)
    return safe + "\n" + note


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
                       "one-shot escape: touch " + _shell_word(ESCAPE_FILE))
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


# The check tests/test_linters.py (StopHookDetailRootTests._unsafe_above) applies to TMPDIR before
# a real detail log write, the same source (a test compares them), used by the self-test's own
# real writes, so the self-test fails or skips for exactly the reason the suite gives.
def _unsafe_above(path):
    """Why a directory above `path` ("/" first) is a symlink, cannot be opened for reading by
    this uid, or fails the root's rule for directories above the home (owned by root or this
    uid with no group or other write bit, or root-owned and sticky), or None."""
    import stat
    euid = os.geteuid()
    for directory in reversed(Path(path).parents):
        info = os.lstat(directory)
        if stat.S_ISLNK(info.st_mode):
            return "%s is a symlink" % directory
        if not os.access(directory, os.R_OK | os.X_OK):
            return ("%s cannot be opened for reading by uid %d (the hook opens every "
                    "directory on the path)" % (directory, euid))
        if not (info.st_uid in (0, euid) and not info.st_mode & 0o022
                or info.st_uid == 0 and info.st_mode & stat.S_ISVTX):
            return ("%s has owner uid %d and mode %04o (the rule needs root or uid %d as owner "
                    "with no group or other write bit, or a root-owned sticky directory)"
                    % (directory, info.st_uid, stat.S_IMODE(info.st_mode), euid))
    return None


def _escape_pinned(cases):
    """``cases`` with ESCAPE_FILE pinned to the path GRC_DROP_ROOT=/w gives, restored afterwards
    (a case may still patch its own). This hook reads GRC_DROP_ROOT only when it loads, so
    without the pin a value inherited from the environment that runs the self-test would reach
    decide()'s escape line."""
    def pinned() -> int:
        from unittest import mock
        with mock.patch.dict(globals(), ESCAPE_FILE=Path("/w/.allow-stop")):
            return cases()
    return pinned


@_escape_pinned
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

    # Console form: three lines, the count and at most the first _SHOWN_ITEMS branches. Fixed
    # held and escape paths, so the result never depends on where this checkout lives.
    many = [("b%d" % n, "1") for n in range(5)]
    with mock.patch.object(module, "HELD_FILE", Path("/h/held-branches.txt")), \
            mock.patch.object(module, "ESCAPE_FILE", Path("/w/.allow-stop")):
        short = summarize(many, "/store/x.log")
        wide = summarize(many, "/" + "s" * 90 + "/x.log")
    if (len(short.splitlines()) != 3 or "5 branch(es)" not in short or "b2 (+1)" not in short
            or "b3" in short or "first 3: " not in short or not short.endswith("/store/x.log")
            or max(map(len, short.splitlines())) > _MAX_LINE_CHARS):
        bad += 1
        print("FAIL summarize did not cap the console list at three")

    # The remedy is on the console when it fits: the held-branches path and the one-shot escape
    # with the log path; a longer log path moves to the WHY line; a held path with a newline is
    # left to the log and the escape stays.
    with mock.patch.object(module, "HELD_FILE", Path("/h/held\nx.txt")), \
            mock.patch.object(module, "ESCAPE_FILE", Path("/w/.allow-stop")):
        odd_held = summarize(many, "/store/x.log")
    if (short.splitlines()[2] != "CONSIDER INSTEAD: merge, or hold in /h/held-branches.txt; "
            "genuine block (once, after recording it): touch /w/.allow-stop; log: /store/x.log"
            or wide.splitlines()[1] != "WHY: a turn-end yield strands unmerged work; log: /"
            + "s" * 90 + "/x.log"
            or wide.splitlines()[2] != "CONSIDER INSTEAD: merge, or hold in /h/held-branches.txt; "
            "genuine block (once, after recording it): touch /w/.allow-stop"
            or odd_held.splitlines()[2] != "CONSIDER INSTEAD: merge or hold; genuine block (once, "
            "after recording it): touch /w/.allow-stop; log: /store/x.log"
            or "held" in odd_held):
        bad += 1
        print("FAIL summarize did not put the held path and the escape on the console")

    # No usable session_id: the refusal stays visible with the NOTE before the list, and
    # nothing is written: the fixture home is never created.
    import tempfile
    detail = decide(False, False, many)
    with tempfile.TemporaryDirectory() as parent:
        absent = os.path.join(parent, "home")
        with mock.patch.object(module, "_DETAIL_HOME", absent):
            routed = _route_refusal(detail, many, {})
        wrote = os.path.lexists(absent)
    if ("NOTE: detail log not written" not in routed or wrote
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

    # A usable session and a fixture home (_DETAIL_HOME): the detail is appended to a 0600 log
    # under <home>/.local/state/grc and three lines return. The second form keeps the store
    # (GRC_STORE) inside a git working tree: the log still lands under the clean home and the
    # store stays empty. A form fails, with the reason, when a directory above its fixture home
    # fails the check tests/test_linters.py applies (_unsafe_above: a symlink, a directory this
    # uid cannot open for reading, or one outside the detail log root's owner and mode rule), so
    # the self-test exits 1, or is skipped with that reason when _UNSAFE_TMP_SKIP_ENV is set to 1.
    skipped = []

    def fixture_home(parent):
        home = os.path.join(parent, "home")
        os.mkdir(home, 0o700)
        os.chmod(home, 0o700)
        why = _unsafe_above(home)
        return (home, None) if why is None else (None, _printable(why))

    for form in ("clean store", "store inside a git working tree"):
        with tempfile.TemporaryDirectory() as parent:
            home, unsafe = fixture_home(parent)
            if home is None:
                if os.environ.get(_UNSAFE_TMP_SKIP_ENV) == "1":
                    skipped.append(form)
                    print("SKIP detail log write (%s): this host cannot provide a safe temporary "
                          "home root: %s (%s=1)" % (form, unsafe, _UNSAFE_TMP_SKIP_ENV))
                else:
                    bad += 1
                    print("FAIL detail log write (%s): this host cannot provide a safe temporary "
                          "home root: %s; set %s=1 to skip instead"
                          % (form, unsafe, _UNSAFE_TMP_SKIP_ENV))
                continue
            store = os.path.join(parent, "outer", "private")
            os.makedirs(store)
            if form != "clean store":
                os.mkdir(os.path.join(parent, "outer", ".git"))
            with mock.patch.object(module, "_DETAIL_HOME", home), \
                    mock.patch.dict(os.environ, {"GRC_STORE": store}):
                routed = _route_refusal(detail, many, {"session_id": "self-test-1"})
            log = Path(home, *_DETAIL_ROOT_PARTS, _DETAIL_SUBDIR, "turn-end.self-test-1.log")
            logged = log.read_text(encoding="utf-8") if log.is_file() else ""
            mode = stat.S_IMODE(os.lstat(log).st_mode) if log.is_file() else None
            untouched = os.listdir(store) == []
        try:
            expected = summarize(many, str(log))
        except ValueError:
            expected = None  # a TMPDIR beyond the PATH BUDGET: the fallback is the right answer
        shown_ok = (routed == expected if expected is not None
                    else "NOTE: detail log written but not summarized" in routed)
        if not shown_ok or "b4 (+1)" not in logged or mode != 0o600 or not untouched:
            bad += 1
            print("FAIL detail log was not written privately with the short console form (%s)"
                  % form)

    # A short fixed directory, so this case never depends on TMPDIR: a 79-character root
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
        print("FAIL the documented root-path budget does not hold")

    # A log path with a newline, a carriage return or an escape is never advertised raw.
    for odd in ("\n", "\r", "\x1b"):
        try:
            summarize(many, "/store" + odd + "x.log")
        except ValueError:
            continue
        bad += 1
        print("FAIL summarize advertised a log path with %r" % odd)

    # Round 5: a newline or an ESC in a git error text never reaches the console raw on the
    # fallback or on the last-resort form; the detail (the log's text) keeps it raw.
    odd = [("claude/a", "unverified: fatal: bad\nref"), ("claude/b\x1b[2J", "1")]
    raw = decide(False, False, odd)
    real_decide = decide

    def no_fallback(*args, **kwargs):
        if kwargs.get("shown") is not None:
            raise ValueError("fallback unavailable")
        return real_decide(*args, **kwargs)

    for label, patch in (("fallback", real_decide), ("last-resort", no_fallback)):
        with mock.patch.object(module, "decide", patch):
            routed = _route_refusal(raw, odd, {})
        if ("\x1b" in routed or "bad\nref" in routed or "bad\\nref" not in routed
                or "claude/b\\x1b[2J (+1)" not in routed or "bad\nref" not in raw):
            bad += 1
            print("FAIL the %s form showed a raw newline or ESC in an item" % label)

    total = len(SELF_TEST) + 16 - len(skipped)
    print(str(total - bad) + "/" + str(total) + " decision cases pass"
          + (" (%d skipped)" % len(skipped) if skipped else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
