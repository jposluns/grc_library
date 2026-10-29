#!/usr/bin/env python3
"""CHANGELOG-hygiene first-commit pre-flight aid (TODO P4.14).

A gating helper run BEFORE the first commit of any PR that edits the
CHANGELOG, as:

    python3 tools/preflight-changelog.py && git commit ...

It exits non-zero (so the ``&&`` chain will not fire) when the working-tree
additions to the root [`CHANGELOG.md`] or the maintainer-grade detailed
mirror contain any of:

  - a gate-2 spelling finding (ise, isation, or yse), found by gate 2's own
    matcher (the engine's ``spelling_matches``: the same language profile,
    http(s) URL-token mask and official-quote masks), or
  - an em-dash or en-dash in prose (the no-dash convention: delta gate D3
    enforces this PR-time on the root file, and gate 51 enforces it on the
    ``.working/`` mirror, but NEITHER fires on the first local commit), or
  - a path-shaped backtick code span that is not wrapped in a markdown link
    (the link-coverage convention that ``lint-changelog-link-coverage.py``
    enforces post-commit on the root file), or
  - a relative markdown-link whose in-repo target does not resolve to an
    existing file (3.34 (closing PR #1084)): unlike the two checks above, this one has NO
    authoritative gate behind it, because the detailed mirror lives under
    ``.working/`` (gate-exempt) so the corpus broken-link gate never scans it,
    a dangling link there is otherwise ungated. Cross-repo / out-of-repo
    targets (a sibling repo, an ``inbox/`` worker-provenance path), external
    ``http(s)``/``mailto:``/anchor targets, and code-span-illustrative links
    are excluded; resolution is relative to the source file's own directory.

  - a root ``CHANGELOG.md`` compact entry whose summary exceeds the D7 length
    ceiling (100 words total, or a single sentence over 45 words); this reuses
    ``check-changelog-length-on-pr.py`` (the D7 delta-gate authority) so the two
    never drift, catching an over-long entry at authoring rather than at the guard.

In addition to the added-line checks above, a FULL-MIRROR link-resolution pass
(3.34 (closing PR #1084) remaining half) scans EVERY in-repo relative markdown link in the
whole detailed mirror (not only added lines), reusing the identical resolution
and exclusion rules, and fails on any dangling target with its line number. This
catches a link that went dangling by a later move of its TARGET, which the
added-line pass (source line unchanged) cannot see. It runs unconditionally, on the
mirror ``resolve_working`` finds first and (3b399 round 8) on every other external
mirror whose diff added a line (3b399 round 9), each read from its own file, since
lines added to a ``.working/`` mirror get no per-line link check.

This is a developer AID, not a new audit gate. The authoritative gates
(D3, gate 51, the link-coverage gate) remain and run in CI and
``run_all_audits.sh`` / ``run-pr-time-checks.sh``; this aid only moves their
diagnosis earlier, to before the first commit, closing the recurring
commit-then-amend loop (improvement-log #341/#347/#349/#355). Run it in an
``&&`` chain: a ``;`` join commits whatever its exit status. Where
``tools/install-git-hooks.sh`` has installed the git-native pre-commit
hook, ``check-changelog-preflight-commit.py`` also runs it (``--staged``)
inside every commit that stages ``CHANGELOG.md`` and refuses on failure.

The check is scoped to the lines a PR ADDS (``git diff`` against HEAD), so
historical entries that predate the conventions never false-alarm. Dash
detection strips inline code spans first (a regex character class or a
quoted format literal may legitimately contain a dash), matching gate 51.

Known limitation: because the aid scans the added diff-lines in isolation,
it does NOT track fenced (```` ``` ````) code-block state the way the
authoritative link-coverage gate does (that gate skips path-shaped spans
inside fenced blocks). A path-shaped span added inside a fenced block in a
CHANGELOG entry would therefore make this aid exit 1 (over-block) where the
gate exits 0. The divergence fails safe (it over-blocks the author's own
commit; it never lets a defect through) and is latent (CHANGELOG entries do
not currently use fenced blocks), so full fenced-block tracking is left
unimplemented; if a CHANGELOG entry ever needs a fenced path-span, run the
commit without the aid and rely on the authoritative gate.

Usage:
    python3 tools/preflight-changelog.py            # working tree vs HEAD
    python3 tools/preflight-changelog.py --staged   # staged diff only

Exit codes:
    0   no spelling, dash, unlinked-reference, dangling-link, or D7-over-length issue in the added CHANGELOG lines
    1   one or more issues (do not commit until fixed)
    2   git invocation error: a ``git diff`` that fails (an unborn HEAD, or a directory that is not
        a repository, including the operational store or the private sibling, whenever its
        directory exists) exits 2
        instead of reporting 0 added lines and passing (fail closed, 3b141 QA r1); or the gate-2
        language-engine child did not deliver a valid result (a load failure, an engine
        API violation, a crash, a timeout, exit 0 without the marked result line, or
        malformed output), reported as one fixed ERROR line rather than a traceback.
        Loading is checked even without added lines (3b201). KeyboardInterrupt raised
        in THIS process (a real Ctrl-C) propagates; one raised by engine code is an
        engine fault in the child, exit 2. A D7 length checker
        (check-changelog-length-on-pr.py) that fails to load, or that lacks
        entries_in_added_line, evaluate, DEFAULT_WORD_MAX or DEFAULT_SENTENCE_MAX,
        is also exit 2, reported as one fixed ERROR line rather than a traceback (3b236).
        So is a diff the parser cannot read exactly: a hunk whose lines do not match its
        header's line counts, or an added line that is not valid UTF-8 (3b236 round 2), or a
        CHANGELOG.md or mirror that the diff shows as a symbolic link or a submodule (3b399
        round 4). So is a run where git selects a work tree other than this repository's
        root, or a repository other than the one found there (``GIT_WORK_TREE``,
        ``core.worktree`` or ``GIT_DIR`` naming elsewhere, 3b399 round 4). So is (3b399
        rounds 5 and 6): a CHANGELOG.md or mirror, or a directory above one of them, that is a
        symbolic link or a gitlink in the index or a symbolic link in the work tree; such a
        path that cannot be examined (an ``OSError`` other than its absence, such as a parent
        directory that cannot be searched); an external mirror whose repository's selected work
        tree does not hold the mirror's directory; an external mirror present in its work tree
        whose repository holds it in neither its index nor its HEAD tree (an untracked mirror,
        or a ``core.worktree`` naming a directory above the store, which makes git read every
        path under another prefix); and a failed ``git rev-parse``, ``ls-files`` or ``ls-tree``
        that these checks run (a bare repository or none, for example), named as that command.
        The external mirrors are the operational store's (``changelog-details/...`` at the
        store root) and the private sibling's (``.working/changelog-details/...`` in
        ``grc_library_private``); each is diffed when its repository's index holds it or its
        work-tree file exists (3b399 round 7), so a store directory that is not a repository,
        or a ``grc_library_private`` directory that is not one or that git cannot enter, exits
        2 too, and a failed git query there names that directory (3b399 round 8). The index
        is asked for the mirror at its expected path only (3b399 round 9): as git names it
        from the store or sibling directory, or, when that directory holds its repository's
        ``.git`` and git reads it under a prefix, at the top of the index, so a repository
        whose ``core.worktree`` names a directory above it still exits 2 as untracked when its
        mirror file is deleted, and a tracked copy at any other path (an archived copy, for
        example) is ignored. So does (3b399 round 9) a detailed mirror that the full-mirror
        scan cannot read or decode, named as that file. So does (3b399 round 7) an operational store
        path that may exist but that this account cannot examine, search or read, or that is
        not a directory, named as the store, and (3b399 round 8) such a
        ``grc_library_private`` path, named as the private sibling: a committing account
        without access to either is therefore refused (exit 2) whenever the aid runs, in the
        commit hook too, rather than having that mirror skipped. An unknown command-line
        argument is argparse's usage error, also exit 2.

Engine isolation (3b201, /validate-pr round 5): every language-engine interaction
(loading lint-language.py, engine API validation, compile_language,
spelling_matches) runs in a separate child process (``sys.executable -I`` on
tools/preflight_language_runner.py), never in this process. The parent sends the
added lines as JSON on the child's stdin. It accepts a result ONLY as exit status
0 plus exactly one JSON line on the child's stdout, carrying this run's nonce and
one list of [kind, word] string pairs per input line. Anything else is the one
fixed engine error, exit 2: a nonzero or signalled exit, a timeout (default 60
seconds, GRC_PREFLIGHT_ENGINE_TIMEOUT accepts finite values up to 300 seconds),
no output, extra output, a wrong nonce, or a schema violation. Cleanup scope,
exactly (round 8, W2): on every completion path (a delivered result, a nonzero
exit, a timeout, an exception) not cut short by an interrupt, the parent kills
ONLY the child's own process group, whose id it verified against the child's
pid, while the child is still unreaped, and only then reaps it, so the
unreaped pid pins the group id through the kill. On a delivered result or a
nonzero exit it first reads the child's stdout to EOF and waits for the exit
WITHOUT reaping (os.waitid with WNOWAIT); on a timeout or an exception the
child has not been reaped either (it may still be running or may have exited
as a waitable zombie), so its pid still pins the group id at the kill. The parent holds the DEFAULT SIGCHLD disposition from before
the spawn until after that reap and then restores the caller's, interrupt
paths included: the restore is armed before the disposition changes, so an
interrupt delivered before or during the swap either finds the disposition
unchanged or finds the restore armed (round 10); an interrupt at the instant
of the restore itself, or before the group kill, is a disclosed residual
(3b259, below). A caller-inherited SIGCHLD=SIG_IGN would
otherwise make the kernel reap the runner automatically, unpinning its pid
and refusing a healthy run (round 9, W1). The SUPPORTED invocations are the
command line and the commit hook, each a fresh process, where only SIG_DFL
and SIG_IGN can survive the exec boundary and both are saved and restored
exactly. Disclosed residuals for IN-PROCESS EMBEDDING only (follow-up 3b259),
with behaviour unchanged for the supported invocations: a native SIGCHLD
handler installed after interpreter startup outside the signal module reads
as the stale startup snapshot, so the restore replaces the handler with that
snapshot (one installed before startup reads as unsaveable, None, and is left
alone); and a
spelling check run outside the main thread cannot swap the disposition at
all, so under a caller-set SIGCHLD=SIG_IGN it refuses a healthy run as the
fixed engine error (fail closed, availability only, never a wrong verdict)
and leaves the caller's disposition untouched. An interrupt delivered at the
instant of the restore can leave SIG_DFL in a process that is exiting
(residual, stated, 3b259). Residuals, stated: a descendant that moves itself
to a new process group, or to a new session, leaves that group and escapes
the kill; and this process reaps only the child itself, so zombie reaping of descendants
depends on the parent's reaper, and under a non-reaping reaper a killed or
surviving descendant can persist as a zombie. An engine that forks a helper
WITHOUT exec leaves the child's saved result descriptor open in the helper, so
the parent never sees end-of-output and the run is refused at the timeout:
fail closed, availability only, never a wrong verdict (residual, stated).
Results over 8 MiB are refused before parsing, though the parent reads and
buffers the child's whole stdout before the cap is applied (residual, stated).
Child stderr (engine tracebacks and prints included)
goes directly to DEVNULL; only strict ASCII result bytes are decoded, inside the
same fault boundary as JSON parsing and schema validation, and no engine
diagnostic is printed. The runner consumes stdin and duplicates the result
channel before any engine code runs, redirects the engine-visible stdout into the
discarded stderr, and seals a computed result with os._exit(0), so engine output
cannot reach the result channel and a fault delivered during child teardown
cannot alter a result the real matcher already produced. Before any matcher
result is read, and again immediately before sealing, the runner refuses (exit
72, no result line) while any thread registered with the threading module,
other than its own main thread, is alive, and takes an immutable snapshot of
the validated results only after
that check, so a matcher that handed its work to a still-running registered
thread cannot seal an unfinished result (round 8, E1). Residual, stated: a
thread started below the threading module (_thread.start_new_thread) is
invisible to that check, and a result deferred through a signal handler runs
no thread at all; both are a disclosed residual (follow-up 3b253). Before sealing, the
runner collects pending garbage and refuses (exit 71, no result line) unless
both fault hooks are still its own and no fault was recorded, so an engine that
restores the interpreter's default hooks cannot mask a fault (see the runner's
docstring for the replace-and-restore residual). Residual, stated: the
child runs the same-tree engine with this process's credentials, so an engine
that DELIBERATELY forges a well-formed marked result line is outside this
boundary's threat model, which covers faults, not malice. The timeout override is
read from this process's environment, which the caller already controls.
"""

from __future__ import annotations

import argparse
import errno
import json
import math
import os
import re
import secrets
import selectors
import signal
import stat
import subprocess
import sys
import time
from pathlib import Path

_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from aiqt_corpus import CODE_SPAN_RE  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import (  # noqa: E402  # grc-config/store, stays local
    REPO_ROOT, _SIBLING_REPO_DIRS, InaccessiblePath, _store_dir, _strict_is_dir, resolve_working)
# The added-line diff, its parser and the repository-selection and link checks are shared with
# the D3 and D7 delta gates (3b399); the parser and the foreign environment keep their earlier
# private names here.
from changelog_diff import (  # noqa: E402
    ChangelogDiffUnreadable, GitQueryFailed, GitSelectsAnotherTree, _git_query, added_line_diff,
    check_git_selects_root, foreign_repo_env as _foreign_repo_env, git_selection,
    parse_added_lines as _parse_added_lines, refuse_links)

# D7 length check reuse (P-1.4): import the authoritative per-PR length checker so the
# 100-word / 45-word-sentence ceiling on a root-CHANGELOG compact entry is caught at
# authoring (this aid) rather than only at the pre-push guard. The module name is
# hyphenated, so load it via importlib; reusing its entry reader + evaluate keeps the two in
# lock-step (no duplicated length logic to drift). It loads on first use, inside main()'s
# fail-closed boundary, so a load failure is one named error (exit 2), not a traceback (3b236).
import importlib.util as _ilu  # noqa: E402
_d7 = None

_D7_ERROR = (
    "ERROR: the D7 length checker could not be loaded from "
    "check-changelog-length-on-pr.py."
)


class D7CheckerUnavailable(RuntimeError):
    """The D7 length checker failed to load; main() reports the fixed error and exits 2."""


_D7_NAMES = ("entries_in_added_line", "evaluate", "DEFAULT_WORD_MAX", "DEFAULT_SENTENCE_MAX")


def _load_d7():
    """The loaded D7 length-checker module. Any failure while loading it, or a loaded module
    without one of the names d7_length_findings() reads (_D7_NAMES), raises
    D7CheckerUnavailable; a KeyboardInterrupt propagates."""
    global _d7
    if _d7 is None:
        try:
            spec = _ilu.spec_from_file_location(
                '_changelog_len_d7',
                Path(__file__).resolve().parent / 'check-changelog-length-on-pr.py')
            module = _ilu.module_from_spec(spec)
            spec.loader.exec_module(module)
            if not all(hasattr(module, name) for name in _D7_NAMES):
                raise D7CheckerUnavailable()
        except KeyboardInterrupt:
            raise
        except BaseException:
            raise D7CheckerUnavailable() from None
        _d7 = module
    return _d7


# Gate 2's project entry point: the isolated child loads it, and through it the
# pack engine and the language profile, exactly as the gate does.
_LANGUAGE_GATE = Path(_TOOLS_DIR) / "lint-language.py"
_LANGUAGE_RUNNER = Path(_TOOLS_DIR) / "preflight_language_runner.py"


_LANGUAGE_ERROR = (
    "ERROR: the gate-2 language engine could not be loaded "
    "or used through lint-language.py."
)

# The engine child is killed after this many seconds (the hang fail-closed bound);
# GRC_PREFLIGHT_ENGINE_TIMEOUT accepts finite seconds in (0, 300]; otherwise
# the default applies. The result cap bounds decoding and JSON parsing.
_ENGINE_TIMEOUT_DEFAULT = 60.0
_ENGINE_TIMEOUT_MAX = 300.0
_ENGINE_STDOUT_MAX = 8 * 1024 * 1024
_ENGINE_TIMEOUT_ENV = "GRC_PREFLIGHT_ENGINE_TIMEOUT"


class LanguageEngineUnavailable(RuntimeError):
    """An engine interaction failed; main() reports the fixed error and exits 2."""


def _engine_timeout() -> float:
    """Seconds before the engine child is killed. The env override is for tests
    and operations; an absent, malformed, non-finite, non-positive or
    over-maximum value keeps the default (the bound never becomes unbounded,
    and never exceeds 300 seconds)."""
    try:
        value = float(os.environ.get(_ENGINE_TIMEOUT_ENV, ""))
    except ValueError:
        return _ENGINE_TIMEOUT_DEFAULT
    return (value if math.isfinite(value) and 0 < value <= _ENGINE_TIMEOUT_MAX
            else _ENGINE_TIMEOUT_DEFAULT)


def _exchange_with_runner(child, request, deadline):
    """Write ``request`` to the runner's stdin and read its stdout to EOF,
    WITHOUT waiting on or reaping the runner: ``Popen.communicate`` reaps the
    runner when it completes, which would free the runner's pid before the
    group kill in :func:`spelling_findings` (round 8, W2). Raises
    LanguageEngineUnavailable once ``deadline`` (``time.monotonic``) passes;
    the caller's ``finally`` then kills the still-unreaped runner's group
    before reaping it."""
    stdin_fd, stdout_fd = child.stdin.fileno(), child.stdout.fileno()
    os.set_blocking(stdin_fd, False)
    os.set_blocking(stdout_fd, False)
    pending = request
    chunks = []
    with selectors.DefaultSelector() as poller:
        poller.register(stdin_fd, selectors.EVENT_WRITE)
        poller.register(stdout_fd, selectors.EVENT_READ)
        while poller.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise LanguageEngineUnavailable()
            for key, _ in poller.select(remaining):
                if key.fd == stdin_fd:
                    try:
                        pending = pending[os.write(stdin_fd, pending):]
                    except BrokenPipeError:
                        # The runner is gone or closed stdin; drain its stdout.
                        pending = b""
                    except BlockingIOError:
                        continue
                    if not pending:
                        poller.unregister(stdin_fd)
                        child.stdin.close()
                else:
                    data = os.read(stdout_fd, 65536)
                    if data:
                        chunks.append(data)
                    else:
                        poller.unregister(stdout_fd)
    return b"".join(chunks)


def _wait_runner_exit_unreaped(child, deadline):
    """Block until the runner has exited WITHOUT reaping it (``os.waitid``
    with ``os.WEXITED | os.WNOWAIT``): the exited runner stays waitable, so
    its pid, and with it the recorded process-group id, remain pinned until
    the group kill in :func:`spelling_findings` (round 8, W2). Polls with
    ``os.WNOHANG`` so a runner that closed its stdout but never exits still
    hits ``deadline`` and is refused (fail closed) instead of blocking this
    process forever."""
    while os.waitid(os.P_PID, child.pid,
                    os.WEXITED | os.WNOWAIT | os.WNOHANG) is None:
        if time.monotonic() >= deadline:
            raise LanguageEngineUnavailable()
        time.sleep(0.005)


def _validated_matches(stdout, nonce, expected):
    """The child's per-input-line [kind, word] match lists, or None unless
    ``stdout`` is EXACTLY one newline-terminated JSON object carrying this run's
    nonce and a schema-valid findings list (one list of two-string pairs per
    input line). Nothing else the child produced is inspected."""
    if stdout.count("\n") != 1 or not stdout.endswith("\n"):
        return None
    try:
        result = json.loads(stdout)
    except ValueError:
        return None
    if not (isinstance(result, dict) and set(result) == {"nonce", "findings"}
            and result["nonce"] == nonce):
        return None
    findings = result["findings"]
    if not (isinstance(findings, list) and len(findings) == expected):
        return None
    for matches in findings:
        if not isinstance(matches, list):
            return None
        for pair in matches:
            if not (isinstance(pair, list) and len(pair) == 2
                    and all(isinstance(item, str) for item in pair)):
                return None
    return findings


def spelling_findings(lines):
    """Check added lines with gate 2's own spelling matcher, in an isolated child.

    The child (the module docstring and tools/preflight_language_runner.py) loads
    lint-language.py, validates the engine API, compiles the language and runs
    the engine's ``spelling_matches`` on every added line, so gate 2's
    vocabulary, patterns and masks apply: the http(s) URL-token mask
    (``mask_urls``: only the URL itself, so link text, prose separated from
    the URL by whitespace or a delimiter, and prose glued to it past the token
    end are still checked, and a URL wrapped across lines stays checked) and
    then the allowed verbatim-quote spans. Additions are checked in
    isolation, including inline code as in gate 2. Fenced additions may
    over-report, like the existing preflight link check. A run with zero added
    lines still loads and validates the engine (the no-added-lines loading
    contract). Raises LanguageEngineUnavailable unless the child exits 0 with a
    valid marked result (fail closed)."""
    try:
        nonce = secrets.token_hex(16)
        request = json.dumps({"nonce": nonce, "texts": [text for _, text in lines]})
        # A caller that inherited SIGCHLD=SIG_IGN makes the kernel reap this
        # process's children automatically: the runner would be reaped the
        # moment it exited, the WNOWAIT wait below would raise
        # ChildProcessError, and a HEALTHY run would be refused as the engine
        # error (round 9, W1). Hold the DEFAULT disposition for the runner's
        # whole lifetime and put the caller's back only after the runner is
        # reaped, so the unreaped pid keeps pinning the group id on every
        # path. saved_sigchld is recorded BEFORE the swap, inside the
        # protecting try, so an interrupt delivered before or during the swap
        # either finds the disposition unchanged or finds the restore below
        # armed (round 10; an interrupt at the restore instant itself is a
        # disclosed residual, 3b259); re-arming an unswapped disposition is a harmless no-op. A
        # disposition this module reads as unsaveable (None: a non-Python
        # handler from before interpreter startup) or cannot swap (not the
        # main thread) is left alone: a real handler does not make the kernel
        # auto-reap. Residual, in-process embedding only: a native handler
        # installed AFTER startup outside the signal module reads as the
        # stale startup snapshot, which the restore puts back (see the module
        # docstring; one installed with SA_NOCLDWAIT is indistinguishable
        # here too).
        saved_sigchld = None
        try:
            inherited = signal.getsignal(signal.SIGCHLD)
            if inherited is not None:
                saved_sigchld = inherited
                try:
                    signal.signal(signal.SIGCHLD, signal.SIG_DFL)
                except ValueError:
                    saved_sigchld = None  # not the main thread: no swap
            with subprocess.Popen(
                    [sys.executable, "-I", str(_LANGUAGE_RUNNER), str(_LANGUAGE_GATE)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL, start_new_session=True) as child:
                # start_new_session put the runner alone in a NEW process group
                # whose id is the runner's own pid. That pid stays pinned to the
                # runner (running, then an unreaped zombie) until the child.wait()
                # in the finally below, and the group kill runs BEFORE that reap
                # on every path an interrupt does not cut short (3b259), so the kill can never target a recycled id or a
                # group that is not the runner's own (round 8, W2).
                pgid = os.getpgid(child.pid)
                if pgid != child.pid:
                    # Unreachable (start_new_session completes before Popen
                    # returns), but fail closed IMMEDIATELY if it ever fires: kill
                    # the runner ITSELF, reap it, and refuse. Never signal a group
                    # this process has not verified as the runner's own, and never
                    # block on a runner still holding its stdin open (round 8, W2).
                    child.kill()
                    child.wait()
                    raise LanguageEngineUnavailable()
                try:
                    deadline = time.monotonic() + _engine_timeout()
                    stdout = _exchange_with_runner(
                        child, request.encode("ascii"), deadline)
                    _wait_runner_exit_unreaped(child, deadline)
                finally:
                    # Every completion path not cut short by an interrupt (a
                    # delivered result, a nonzero exit, a timeout, an exception;
                    # 3b259) kills engine descendants left in the
                    # runner's own group, then reaps the runner. The runner is
                    # still unreaped here, running or a waitable zombie, so its
                    # pid pins the group id through the kill. Residuals, stated:
                    # a descendant that moved itself to a new process group or a
                    # new session escapes this kill, and this process reaps only
                    # the runner, so descendant zombie reaping depends on the
                    # parent's reaper.
                    try:
                        os.killpg(pgid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    child.wait()
        finally:
            # The caller's SIGCHLD disposition returns only AFTER the runner
            # is reaped, on every path, interrupt paths included (rounds
            # 9-10), except an interrupt at the instant of this restore
            # (disclosed residual, 3b259). ValueError here means a non-main-thread caller whose
            # disposition was never swapped: nothing to put back.
            if saved_sigchld is not None:
                try:
                    signal.signal(signal.SIGCHLD, saved_sigchld)
                except ValueError:
                    pass  # not the main thread: nothing was swapped
        if child.returncode != 0 or len(stdout) > _ENGINE_STDOUT_MAX:
            raise LanguageEngineUnavailable()
        matches = _validated_matches(stdout.decode("ascii"), nonce, len(lines))
        if matches is None:
            raise LanguageEngineUnavailable()
        return [(path, f"gate 2 spelling [{kind}]: {word}", text.strip())
                for (path, text), found in zip(lines, matches)
                for kind, word in found]
    except KeyboardInterrupt:
        # Only the parent's own interrupt propagates, never a child's exception.
        raise
    except BaseException:
        # Parsing and schema validation belong to the same fault boundary:
        # a spawn failure, a timeout (the group is killed above), undecodable
        # or over-cap result bytes, and a decoder resource fault all become
        # the one fixed engine error.
        raise LanguageEngineUnavailable() from None


def d7_length_findings(lines):
    """The D7 length-ceiling findings for the ROOT ``CHANGELOG.md`` compact entries in
    ``lines`` (a list of ``(path, added_text)``), reusing ``check-changelog-length-on-pr``'s
    entries_in_added_line + evaluate so this aid and the D7 delta gate never drift (P-1.4). An
    entry is read at the start of an added line and after any ``str.splitlines()`` boundary
    inside it (CR, U+2028, U+0085 and the rest), as D7 reads it (3b399). Only the root file
    is length-gated; the detailed mirror is out of the D7 gate's scope."""
    d7 = _load_d7()
    entries = []
    for path, text in lines:
        if path == "CHANGELOG.md":
            entries.extend(d7.entries_in_added_line(text))
    return [
        ("CHANGELOG.md", f"D7 length ceiling exceeded ({offence})", "")
        for offence in d7.evaluate(entries, d7.DEFAULT_WORD_MAX, d7.DEFAULT_SENTENCE_MAX)
    ]


CHANGELOG_FILES = (
    "CHANGELOG.md",
    ".working/changelog-details/CHANGELOG-detailed.md",
)

EM_DASH = "\u2014"
EN_DASH = "\u2013"

# Inline code-span stripper: a run of N backticks, the shortest content, then
# a closing run of N backticks (the standard CommonMark code-span shape). Same
# approach as gate 51 (lint-working-prose-hygiene.py), so a dash that is
# legitimately inside a code span (a regex character class, a quoted format
# literal) is treated as content, not prose.
#
# DELIBERATE two-parser seam (GR-11): this file carries TWO code-span parsers
# because each mirrors a DIFFERENT authoritative gate. This regex mirrors gate
# 51's any-length span stripper (the dash check); the manual single-backtick
# walk in unlinked_refs_in_line() mirrors lint-changelog-link-coverage.py's
# per-line walk byte-for-byte (the link check). Unifying them would break
# parity with one gate or the other; keep each in step with ITS gate.

# --- File-reference recognition, mirrored from lint-changelog-link-coverage.py ---
# Kept in step with that gate (the authoritative post-commit check); this aid
# only surfaces the same class earlier. If the gate's logic changes, update
# this block to match.
FILE_EXTENSIONS = (
    ".md",
    ".py",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".cff",
    ".toml",
    ".html",
    ".css",
    ".js",
)
TOP_LEVEL_FILES = {
    "README.md",
    "CHANGELOG.md",
    "NOTICE.md",
    "LICENSE",
    "CITATION.cff",
    "AUTHORS.md",
    "TODO.md",
    "TODO-REFERENCE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "taxonomy.yml",
    ".pre-commit-config.yaml",
    "specification-ingestion.md",
    "specification-master-project.md",
}


def looks_like_file_reference(text: str) -> bool:
    if "/" in text and text.endswith(FILE_EXTENSIONS):
        return True
    if text in TOP_LEVEL_FILES:
        return True
    if "/" not in text and text.endswith(FILE_EXTENSIONS):
        base = text[: text.rindex(".")]
        if base and re.match(r"^\.?[A-Za-z0-9][A-Za-z0-9_\-.]*$", base):
            return True
    return False


def unlinked_refs_in_line(line: str) -> list[str]:
    """Return path-shaped backtick spans on a line that are NOT wrapped in a
    markdown link. Mirrors the per-line walk in lint-changelog-link-coverage.py."""
    findings: list[str] = []
    i = 0
    while i < len(line):
        # Skip an already-linked reference: [`...`](...)
        if line[i] == "[" and i + 1 < len(line) and line[i + 1] == "`":
            close = line.find("](", i + 2)
            if close != -1:
                paren_close = line.find(")", close + 2)
                if paren_close != -1:
                    i = paren_close + 1
                    continue
        if line[i] != "`":
            i += 1
            continue
        end = line.find("`", i + 1)
        if end == -1:
            break
        inner = line[i + 1 : end]
        if looks_like_file_reference(inner):
            findings.append(inner)
        i = end + 1
    return findings


# --- Markdown-link target resolution (3.34 (closing PR #1084)) ---
# The detailed mirror lives under `.working/` (gate-exempt), so the corpus
# broken-link gate does not scan it; a dangling relative link there is otherwise
# ungated. This check verifies that each IN-REPO relative markdown-link target
# an added line introduces resolves to an existing file. Excluded (by
# construction, consistent with the worker-provenance plain-text convention):
# external `http(s)`/`mailto:`/anchor targets;
# cross-repo / out-of-repo targets (a sibling repo such as `grc_library_ref` /
# `grc_library_scratch`, or an `inbox/` worker-provenance path, or any target
# that resolves outside this repo); and links inside a code span (an
# illustrative ``[text](url)``). Resolution is relative to the SOURCE file's
# own directory, so the same check serves both CHANGELOG files.
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CROSS_REPO_MARKERS = ("grc_library_ref", "grc_library_scratch", "/inbox/")


def unresolved_link_targets(
    source_rel_path: str,
    line: str,
    root: Path = REPO_ROOT,
    *,
    source_path: Path | None = None,
) -> list[str]:
    """Return in-repo relative markdown-link targets on ``line`` that do NOT
    resolve to an existing file (see the block comment above for exclusions).
    ``root`` is the repository root (default ``REPO_ROOT``); it is a parameter so
    the full-mirror scan (3.34 (closing PR #1084)) can reuse this identical resolution against
    a test root without a divergent reimplementation. ``source_path`` is the
    PHYSICAL on-disk location of the source file when it differs from its logical
    ``root``/``source_rel_path`` location (the post-.working-move case: the mirror
    is read from the operational store or private-sibling fallback). Link CLASSIFICATION stays logical against
    the public ``root``; link EXISTENCE follows the physical working tree for a
    target that stays inside logical ``.working/``, and the public ``root`` for a
    target that leaves ``.working/`` into the public corpus."""
    findings: list[str] = []
    stripped = CODE_SPAN_RE.sub("", line)  # drop code-span-illustrative links
    public_root = root.resolve()
    logical_source = public_root / source_rel_path
    physical_source = source_path or logical_source
    logical_working = public_root / ".working"
    for match in MD_LINK_RE.finditer(stripped):
        base = match.group(1).split("#", 1)[0].strip()
        if not base or base.startswith(("http://", "https://", "mailto:")):
            continue
        if any(marker in base for marker in CROSS_REPO_MARKERS):
            continue
        try:
            logical_path = Path(os.path.normpath(str(logical_source.parent / base)))
        except (OSError, RuntimeError, ValueError):
            findings.append(base)
            continue
        try:
            working_rel = logical_source.relative_to(logical_working)
            logical_rel = logical_path.relative_to(logical_working)
        except ValueError:
            working_rel = None
        if working_rel is not None:
            if Path(base).is_absolute():
                findings.append(base)  # a mirror link must not name logical .working absolutely
                continue
            if (not working_rel.parts or not physical_source.is_absolute()
                    or len(physical_source.parents) < len(working_rel.parts)):
                findings.append(base)  # the physical store root cannot be established
                continue
            # The link stayed inside logical .working: follow the selected
            # physical working tree (a private-only mirror included).
            try:
                store_root = physical_source.parents[len(working_rel.parts) - 1].resolve()
                physical_source.resolve().relative_to(store_root)
                resolved = (store_root / logical_rel).resolve()
                resolved.relative_to(store_root)
            except (ValueError, OSError, RuntimeError):
                findings.append(base)
                continue
        else:
            try:
                resolved = (logical_source.parent / base).resolve()
                resolved.relative_to(public_root)
            except ValueError:
                if "\0" in base or logical_path.is_relative_to(logical_working):
                    findings.append(base)
                continue  # resolved outside this repo: treated as cross-repo
            except (OSError, RuntimeError):
                findings.append(base)
                continue
            # A public symlink may enter .working even when the authored path did not.
            try:
                resolved.relative_to(logical_working)
            except ValueError:
                pass
            else:
                try:
                    logical_path.relative_to(logical_working)
                except ValueError:
                    findings.append(base)
                    continue
        try:
            exists = resolved.exists()
        except (OSError, RuntimeError, ValueError):
            exists = False
        if not exists:
            findings.append(base)
    return findings


# --- Full-mirror link-resolution scan (3.34 (closing PR #1084) remaining half) ---
# The added-line check above catches a NEW dangling link before commit, but a
# link that went dangling by a later move of its TARGET (the source line
# unchanged) is invisible to it. This full-mirror pass scans EVERY in-repo
# relative markdown link in the whole detailed mirror, reusing the identical
# resolution + exclusion rules of unresolved_link_targets line-by-line. It runs
# unconditionally (the mirror is currently clean at 0 dangling of 142 links, so
# default-on adds no noise; the tradeoff is that it re-reads the whole mirror
# each run, negligible for a single file). Known limitation inherited from the
# per-line resolver: a link inside a FENCED code block is not skipped (the
# resolver only strips single-backtick code spans); there are 0 fenced-block
# links in the mirror today, so no false positive arises. If a future
# fenced-block illustrative link appears, add ```-fence tracking here.
DETAILED_MIRROR_REL = ".working/changelog-details/CHANGELOG-detailed.md"


def unresolved_links_in_mirror(root: Path | None = None, *,
                               mirror: Path | None = None) -> list[tuple[int, str, str]]:
    """Every in-repo relative markdown-link target in the WHOLE detailed mirror
    that does NOT resolve. Returns ``(line_no, target, line_text)`` per dangling
    link. Reuses ``unresolved_link_targets`` (same rules). ``root=None`` (the
    default) resolves the mirror via ``resolve_working`` (operational store first,
    then private sibling, then in-repo); an explicit ``root`` preserves the temp-fixture behaviour. Link
    targets resolve against ``REPO_ROOT`` in the default case, since the mirror's
    references are authored relative to the public corpus. ``mirror`` names the
    physical mirror file to read instead, resolved as in the default case (3b399 round
    8: ``main()`` scans each external mirror whose diff added a line, not only
    ``resolve_working``'s first hit). Returns [] if absent; a file that cannot be read or
    decoded raises ``OSError`` or ``UnicodeDecodeError`` (``main()`` exits 2, 3b399 round 9)."""
    if mirror is not None:
        if not mirror.is_file():
            return []
        resolution_root = REPO_ROOT
    elif root is None:
        mirror = resolve_working(
            DETAILED_MIRROR_REL[len(".working/"):], repo_root=REPO_ROOT)
        if mirror is None or not mirror.is_file():
            return []
        resolution_root = REPO_ROOT
    else:
        mirror = root / DETAILED_MIRROR_REL
        if not mirror.is_file():
            return []
        resolution_root = root
    findings: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(
        mirror.read_text(encoding="utf-8").splitlines(), start=1
    ):
        for target in unresolved_link_targets(
                DETAILED_MIRROR_REL, line, root=resolution_root,
                source_path=mirror):
            findings.append((lineno, target, line.strip()))
    return findings


def _refuse_linked_paths(repo: Path, paths: tuple[str, ...],
                         env: dict[str, str] | None = None) -> None:
    """Raise ``ChangelogDiffUnreadable`` (``main()`` exits 2) when one of ``paths``, files named
    from ``repo``, or a directory above one of them under ``repo``, is a symbolic link or a
    gitlink in the index (``changelog_diff.refuse_links``, run with ``env``) or a symbolic link
    in the work tree (3b399 round 5). git prints nothing for a path beyond a symbolic link, so
    a mirror under a symlinked ``.working`` passed with "0 added"; and the diff shows a link's
    mode only when the link changes, so a CHANGELOG.md already linked at HEAD passed too. The
    work tree is checked in both modes, since the link targets and the full-mirror scan read
    it. An absent path (``FileNotFoundError`` or ``NotADirectoryError``) is not a link; any other
    failure to stat a path, such as a parent directory that cannot be searched, raises
    ``OSError`` (3b399 round 6: ``Path.is_symlink()`` returned False there), and a git failure
    raises ``GitQueryFailed``."""
    names = sorted({"/".join(rel.split("/")[:depth])
                    for rel in paths for depth in range(1, rel.count("/") + 2)})
    refuse_links(names, cwd=repo, env=env)
    for name in names:
        try:
            mode = os.lstat(repo / name).st_mode
        except (FileNotFoundError, NotADirectoryError):
            continue
        if stat.S_ISLNK(mode):
            raise ChangelogDiffUnreadable(
                f"{name} has mode 120000 in the work tree, a symbolic link, not a regular file or "
                "directory, so the diff does not show the lines of the file it leads to")


def _check_mirror_work_tree(private_root: Path, env: dict[str, str]) -> None:
    """Raise ``GitSelectsAnotherTree`` (``main()`` exits 2) unless the work tree that git selects
    for the external mirror's repository, run in ``private_root`` with ``env`` (no local
    variable of the public repository), holds ``private_root`` (3b399 round 5). The mirror's
    repository's own ``core.worktree`` naming an empty sibling made the working-tree diff read
    that directory, so a mirror addition passed with "0 added". ``private_root`` may be a
    subdirectory of that work tree (the private sibling's ``.working``). A bare repository, or
    none, raises ``GitQueryFailed``."""
    top, _ = git_selection(private_root, env)
    if not private_root.resolve().is_relative_to(top.resolve()):
        raise GitSelectsAnotherTree(
            f"git selects the work tree {top} for the mirror's repository, which does not hold "
            f"{private_root}")


def _check_mirror_tracked(private_root: Path, rel: str, env: dict[str, str]) -> None:
    """Raise ``ChangelogDiffUnreadable`` (``main()`` exits 2) unless ``rel``, named from
    ``private_root``, is in the index or the HEAD tree of the repository that git selects there
    with ``env`` (3b399 round 6). git reads a pathspec relative to ``private_root``'s place in the
    work tree, so a store whose own ``core.worktree`` names its parent made every path read as
    ``<store>/<rel>``, which matched no entry, and a staged mirror addition passed with "0
    added"; an untracked mirror passed the same way. The HEAD tree is read only when the index
    has no entry. A git failure (an unborn HEAD included) raises ``GitQueryFailed``."""
    for args in (["ls-files", "-z", "--", rel],
                 ["ls-tree", "-z", "--name-only", "HEAD", "--", rel]):
        if rel.encode("utf-8") in _git_query(args, cwd=private_root, env=env).split(b"\0"):
            return
    raise ChangelogDiffUnreadable(
        f"{rel} is in neither the index nor the HEAD tree of the repository that git selects in "
        f"{private_root} (an untracked mirror, or a core.worktree naming a directory above it), "
        "so its diff would show no line")


def _mirror_in_index(private_root: Path, rel: str, env: dict[str, str]) -> bool:
    """True when the index of the repository that git selects in ``private_root`` with ``env``
    tracks or stages the mirror at its expected path (3b399 round 7): ``rel`` named from
    ``private_root`` (git's prefix there, then ``rel``), or, when ``private_root`` holds its
    repository's ``.git`` and git reads it under a prefix, ``rel`` named from the top of the
    index. Round 7 asked only for the first, so a repository whose ``core.worktree`` names a
    directory above it read every path under a wrong prefix, found no entry, and with the mirror
    file deleted was skipped ("OK: 0 added") before :func:`_check_mirror_tracked` could refuse
    it. Round 8 asked for ``**/<rel>`` at any depth, so a tracked copy elsewhere (the private
    sibling's archived ``archive/.../.working/changelog-details/CHANGELOG-detailed.md``) made the
    tracked check refuse every run; a copy at any other path is now ignored (3b399 round 9). The
    names are read with ``--full-name``. A git failure (no repository, for example) raises
    ``GitQueryFailed``, and a ``.git`` that cannot be examined raises ``OSError``."""
    prefix = _git_query(["rev-parse", "--show-prefix"], cwd=private_root,
                        env=env).decode("utf-8", errors="surrogateescape").rstrip("\n")
    expected = {prefix + rel}
    if prefix:
        try:
            os.lstat(private_root / ".git")
        except (FileNotFoundError, NotADirectoryError):
            pass
        else:
            expected.add(rel)
    names = _git_query(["ls-files", "--full-name", "-z", "--",
                        *(f":(top,literal){name}" for name in sorted(expected))],
                       cwd=private_root, env=env).decode("utf-8", errors="surrogateescape")
    return any(name in expected for name in names.split("\0"))


class StoreInaccessible(RuntimeError):
    """The operational store may exist but this account cannot examine, search or read it; main()
    prints the message and exits 2 (3b399 round 7)."""


class SiblingInaccessible(RuntimeError):
    """The private sibling ``grc_library_private`` may exist but this account cannot examine,
    search or read it, or it is not a directory; main() prints the message and exits 2 (3b399
    round 8)."""


def _inaccessible_reason(exc: InaccessiblePath) -> str:
    """Why a strict lookup refused a path, without claiming it exists (3b399 round 8, N1): only
    ENOTDIR and a store directory that is "present but not searchable" say what is there; ENOENT
    (a missing or dangling component, which lint_common's message names, 3b677 r7) says only that
    it cannot be used; any other error (a parent this account cannot search, for example) leaves
    the path's existence unknown."""
    if exc.errno == errno.ENOTDIR:
        return f"is not a directory, or a path above it is not one ({exc.strerror})"
    if exc.errno == errno.ENOENT:
        return f"cannot be used ({exc.strerror})"
    if (exc.strerror or "").startswith("present but not searchable"):
        return f"exists but this account cannot search it ({exc.strerror})"
    return f"may exist but this account cannot examine it ({exc.strerror})"


def _operational_store(root: Path) -> Path | None:
    """The operational store for ``root`` (``lint_common._store_dir`` in its strict mode), or None
    when there is none. A store path that may exist but cannot be examined (a parent this account
    cannot search) or is not a directory, or a store directory this account cannot search or
    read, raises :class:`StoreInaccessible` (3b399 round 7): the default lookup read such a store
    as absent, so a staged store-mirror addition passed with "OK: 0 added"."""
    try:
        store = _store_dir(root, strict=True)
    except InaccessiblePath as exc:
        raise StoreInaccessible(
            f"the operational store {exc.filename} {_inaccessible_reason(exc)}, so its CHANGELOG "
            "mirror cannot be checked") from None
    if store is not None and not os.access(store, os.R_OK | os.X_OK,
                                           effective_ids=os.access in os.supports_effective_ids):
        raise StoreInaccessible(
            f"the operational store {store} exists but this account cannot search or read it, so "
            "its CHANGELOG mirror cannot be checked")
    return store


def _private_sibling(root: Path) -> Path | None:
    """The private sibling ``<root's parent>/grc_library_private``, or None when no entry is there
    (``lint_common._strict_is_dir``, as ``resolve_sibling(strict=True)`` probes it). A sibling
    path that may exist but cannot be examined (a symbolic link into a directory this account
    cannot search, for example) or is not a directory, or a sibling directory this account
    cannot search or read, raises :class:`SiblingInaccessible` (3b399 round 8): round 7's
    ``Path.is_dir()`` read a sibling linked into a directory this account cannot search as
    absent on Python 3.14, so a staged sibling-mirror addition passed with "OK: 0 added"."""
    sibling = root.parent / _SIBLING_REPO_DIRS["private"]
    try:
        if not _strict_is_dir(sibling):
            return None
    except InaccessiblePath as exc:
        raise SiblingInaccessible(
            f"the private sibling {exc.filename} {_inaccessible_reason(exc)}, so its CHANGELOG "
            "mirror cannot be checked") from None
    if not os.access(sibling, os.R_OK | os.X_OK,
                     effective_ids=os.access in os.supports_effective_ids):
        raise SiblingInaccessible(
            f"the private sibling {sibling} exists but this account cannot search or read it, so "
            "its CHANGELOG mirror cannot be checked")
    return sibling


def _added_lines_from_repo(
    repo: Path, paths: tuple[str, ...], staged: bool, env: dict[str, str] | None = None
) -> list[tuple[str, str]]:
    """(file, added-line-text) for every added CHANGELOG line in ONE repo's diff, run with ``env``:
    None inherits this process's environment, right for the public repository, where a pre-commit
    hook's GIT_INDEX_FILE names the index being committed; a mirror in another repository passes
    :func:`_foreign_repo_env`.

    The diff is ``changelog_diff.added_line_diff`` (shared with the D3 and D7 delta gates, 3b399),
    whose docstring lists the settings its flags override: an external diff driver, a
    ``textconv`` filter, a ``-diff`` attribute, colour and the ``+++ b/`` prefix each left no
    ``+`` line, so the aid reported 0 added lines and passed (3b141 QA r1). It also pins the
    context (3b236 round 2), since a blank context line printed as an empty line ended the round
    1 hunk early and lost the added lines in the rest of that hunk. It also pins the file
    pairing (3b399 round 3): a new CHANGELOG.md that git paired as a rename or copy of the
    in-repo detailed mirror showed no added line. git runs in ``repo``, so the pathspecs name
    files at that root whatever this process's working directory, provided git selects that
    root as its work tree (:func:`added_lines` checks it for the public repository). The
    runner also drops the pathspec-reading variables (3b399 round 4). Its parser,
    ``changelog_diff.parse_added_lines``, reads each hunk by its header's line counts, and a diff it
    cannot read exactly raises ``ChangelogDiffUnreadable`` (``main()`` exits 2) rather than
    yielding fewer added lines.

    A git failure raises ``CalledProcessError`` carrying git's ``stderr``, and ``main()`` exits 2:
    an unread diff is not zero added lines. This replaces the 3.190 fail-open, which returned []
    for any git failure (a sibling that is not a git repository included), so a failed diff
    printed "OK: 0 added CHANGELOG line(s)" and exited 0."""
    revs = ["--cached", "HEAD"] if staged else ["HEAD"]
    return _parse_added_lines(added_line_diff(revs, paths, cwd=repo, env=env))


def added_lines(staged: bool, root: Path = REPO_ROOT,
                diffed: list[tuple[str, Path]] | None = None) -> list[tuple[str, str]]:
    """Added CHANGELOG lines across the public repo AND the (post-move) private
    detailed mirror. The public root CHANGELOG.md (and, pre-move, the in-repo
    mirror) come from this repo's diff; a mirror in the operational store or the private sibling gets its OWN
    repository-local ``git diff`` so private additions still receive the dash and
    unlinked-path checks. That diff runs without this repository's local git
    variables (:func:`_foreign_repo_env`), so ``--staged`` reads THAT repository's
    index. The ``staged`` choice is applied separately in each repository,
    preserving staged-only versus full-working-tree semantics. The public diff
    runs only when git selects ``root`` (``changelog_diff.check_git_selects_root``),
    and the mirror's only when its repository's work tree holds the mirror
    (:func:`_check_mirror_work_tree`) and that repository tracks the mirror at its
    expected path (:func:`_check_mirror_tracked`); each diff's paths are first checked
    for links (:func:`_refuse_linked_paths`). The in-repo mirror is always in the public
    diff (3b399 round 5): it was added only when ``is_file()`` found it in the work tree,
    so a staged mirror gitlink or dangling symlink, or a staged mirror whose
    working-tree file was deleted, passed with "0 added". For the same reason each
    external mirror is chosen by its repository's index, not by its working-tree file
    (3b399 round 7): the operational store's mirror (``<store>/changelog-details/...``,
    found by :func:`_operational_store`) and the private sibling's
    (``grc_library_private/.working/changelog-details/...``, whenever that directory
    exists) are EACH diffed when ``git ls-files`` there holds the mirror, or its
    working-tree file exists. Round 6 diffed the store alone whenever it existed, so a
    staged sibling-mirror addition was never read once the store's mirror file was
    gone, and without a store the sibling was found by its working-tree file, so a
    staged sibling addition whose file was then deleted passed with "0 added".

    3b399 round 8: the sibling is found strictly (:func:`_private_sibling`), as the store
    is; a ``GitQueryFailed`` in an external repository names that repository's directory;
    and each external mirror diffed is appended to ``diffed``, when given, as its added
    lines' file name and its physical file, for ``main()``'s full-mirror link scan. 3b399
    round 9: the index is asked for the mirror at its expected path only
    (:func:`_mirror_in_index`), so a tracked copy elsewhere is ignored, and a mirror is
    appended to ``diffed`` only when its diff added a line."""
    check_git_selects_root(root, cwd=root)
    public_paths = ("CHANGELOG.md", DETAILED_MIRROR_REL)
    _refuse_linked_paths(root, public_paths)
    results = _added_lines_from_repo(root, public_paths, staged)
    external = []
    store = _operational_store(root.resolve())
    if store is not None:
        # The operational store (Option C): files live at its root, with no .working/ prefix.
        external.append((store, DETAILED_MIRROR_REL[len(".working/"):]))
    sibling = _private_sibling(root.resolve())
    if sibling is not None:
        # The private sibling's repository, at its root: the mirror is under its .working/.
        external.append((sibling, DETAILED_MIRROR_REL))
    if not external:
        return results
    env = _foreign_repo_env()
    for private_root, rel in external:
        try:
            _check_mirror_work_tree(private_root, env)
            if not (_mirror_in_index(private_root, rel, env)
                    or os.path.lexists(private_root / rel)):
                continue
            _check_mirror_tracked(private_root, rel, env)
            _refuse_linked_paths(private_root, (rel,), env)
        except GitQueryFailed as exc:
            raise GitQueryFailed(f"{exc} (in {private_root})") from None
        added = _added_lines_from_repo(private_root, (rel,), staged, env=env)
        results.extend(added)
        if diffed is not None and added:
            # 3b399 round 9 (claude W1 3B399-R8-SIBLING-FULLSCAN-STALE): only a mirror whose diff
            # added a line is scanned in full, so a stale link already committed there does not
            # refuse a run that adds nothing to it.
            diffed.append((rel, private_root / rel))
    return results


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Pre-commit aid: fail when added CHANGELOG lines carry an em/en "
            "dash in prose, a gate-2 spelling, an unlinked path-shaped reference, a dangling "
            "in-repo markdown-link target, or a root entry over the D7 length ceiling."
        )
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help=("Check only the staged diff's added lines (default: full working tree vs HEAD); "
              "link targets and the full-mirror scan still read the working tree."),
    )
    args = parser.parse_args(argv[1:])

    try:
        _load_d7()
    except D7CheckerUnavailable:
        print(_D7_ERROR, file=sys.stderr)
        return 2
    diffed: list[tuple[str, Path]] = []
    try:
        lines = added_lines(args.staged, diffed=diffed)
    except subprocess.CalledProcessError as exc:
        # Fail closed (3b141 QA r1): a failed diff is not zero added lines.
        detail = (exc.stderr or "").strip()
        print(f"ERROR: git diff failed: {exc}" + (f"\n{detail}" if detail else ""), file=sys.stderr)
        return 2
    except (OSError, ChangelogDiffUnreadable) as exc:
        print(f"ERROR: the CHANGELOG diff could not be read: {exc}", file=sys.stderr)
        return 2
    except (GitQueryFailed, StoreInaccessible, SiblingInaccessible) as exc:
        # 3b399 round 5 (N3): a rev-parse, ls-files or ls-tree failure is named as such; round 7:
        # so is a store this account cannot examine, search or read; round 8: and such a sibling.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except GitSelectsAnotherTree as exc:
        print(f"ERROR: {exc}; unset GIT_DIR, GIT_WORK_TREE or core.worktree and rerun.",
              file=sys.stderr)
        return 2
    try:
        spelling = spelling_findings(lines)
    except LanguageEngineUnavailable:
        # The isolated child delivered no valid marked result; fail closed.
        print(_LANGUAGE_ERROR, file=sys.stderr)
        return 2

    findings: list[tuple[str, str, str]] = []
    for path, text in lines:
        stripped = CODE_SPAN_RE.sub("", text)
        if EM_DASH in stripped or EN_DASH in stripped:
            findings.append((path, "em/en dash in prose", text.strip()))
        for ref in unlinked_refs_in_line(text):
            findings.append((path, f"unlinked file reference `{ref}`", text.strip()))
        # Resolution on the ROOT changelog only: the detailed mirror is covered
        # in full by the full-mirror pass below (which also catches a link that
        # went dangling by a later move of its target), so resolving the mirror
        # here too would double-report a newly-added mirror dangling link.
        if path != DETAILED_MIRROR_REL:
            for tgt in unresolved_link_targets(path, text):
                findings.append(
                    (path, f"dangling markdown-link target `{tgt}`", text.strip())
                )

    # 3b399 round 9 (claude N3 3B399-R8-SCAN-TRACEBACK): a mirror the scans below cannot read
    # (a file this account may not open) or decode is one ERROR line and exit 2, not a traceback.
    scanning: Path | None = None
    try:
        first = resolve_working(DETAILED_MIRROR_REL[len(".working/"):], repo_root=REPO_ROOT)
        scanning = first
        # Full-mirror scan (3.34 (closing PR #1084) remaining half): catch a link that went
        # dangling by a later move of its target, which the added-line pass misses.
        for lineno, tgt, evidence in unresolved_links_in_mirror():
            findings.append(
                (
                    DETAILED_MIRROR_REL[len(".working/"):],
                    f"dangling markdown-link target `{tgt}` (full-mirror scan, line {lineno})",
                    evidence,
                )
            )
        # 3b399 round 8 (codex 3B399-SIBLING-LINK-SKIPPED, claude W2): that scan reads only the
        # mirror resolve_working finds first, the store's whenever it exists, so a dangling link
        # added to the private sibling's mirror went unchecked. Every other external mirror whose
        # diff added a line (round 9) is scanned too, from its own file.
        for label, mirror in diffed:
            if mirror == first:
                continue
            scanning = mirror
            for lineno, tgt, evidence in unresolved_links_in_mirror(mirror=mirror):
                findings.append(
                    (label,
                     f"dangling markdown-link target `{tgt}` (full-mirror scan of {mirror}, "
                     f"line {lineno})",
                     evidence))
    except (OSError, UnicodeDecodeError) as exc:
        print("ERROR: the full-mirror scan could not read the CHANGELOG mirror"
              + (f" {scanning}" if scanning is not None else "") + f": {exc}", file=sys.stderr)
        return 2

    findings.extend(spelling)
    findings.extend(d7_length_findings(lines))

    if not findings:
        scope = "staged" if args.staged else "working-tree"
        print(
            f"OK: {len(lines)} added CHANGELOG line(s) ({scope}) are spelling-clean and dash-free, "
            f"every path-shaped reference is a markdown link, every in-repo link "
            f"target resolves, and no root entry exceeds the D7 length ceiling."
        )
        return 0

    for path, issue, evidence in findings:
        # Only append the evidence line when there is evidence: the D7 length findings
        # carry no line-evidence (the offence string already names the PR and the count),
        # so a blank indented line would otherwise print (claude vpr1325 cosmetic note).
        msg = f"FAIL {path}: {issue}" + (f"\n    {evidence}" if evidence else "")
        print(msg, file=sys.stderr)
    print(
        f"\n{len(findings)} CHANGELOG-hygiene issue(s) in the added lines. Fix "
        f"before committing: fix gate-2 spellings, remove em/en dashes from prose (use commas, "
        f"colons, or parentheses), wrap path-shaped references as "
        f"[`path`](path), fix any dangling in-repo link target (or exclude "
        f"a cross-repo / illustrative link), and shorten any root entry over the "
        f"D7 length ceiling (100 words total, or a single sentence over 45 words). "
        f"This aid mirrors gate 2 spelling, delta gate D3, the D7 length check, gate 51, the "
        f"link-coverage gate, and the detailed-mirror link-resolution check "
        f"(3.34 (closing PR #1084)), surfaced before the first commit.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
