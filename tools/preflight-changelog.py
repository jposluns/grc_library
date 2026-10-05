#!/usr/bin/env python3
"""CHANGELOG-hygiene first-commit pre-flight aid (TODO P4.14).

A gating helper run BEFORE the first commit of any PR that edits the
CHANGELOG, as:

    python3 tools/preflight-changelog.py && git commit ...

It exits non-zero (so the ``&&`` chain will not fire) when the working-tree
additions to the root [`CHANGELOG.md`] or the maintainer-grade detailed
mirror contain any of:

  - a gate-2 spelling finding (ise, isation, or yse), found by gate 2's own
    matcher (the engine's ``spelling_matches``: the same language profile and
    official-quote masks), or
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
added-line pass (source line unchanged) cannot see. It runs unconditionally.

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
        a repository, an operational store or private sibling holding the mirror included) exits 2
        instead of reporting 0 added lines and passing (fail closed, 3b141 QA r1); or the gate-2
        language-engine child did not deliver a valid result (a load failure, an engine
        API violation, a crash, a timeout, exit 0 without the marked result line, or
        malformed output), reported as one fixed ERROR line rather than a traceback.
        Loading is checked even without added lines (3b201). KeyboardInterrupt raised
        in THIS process (a real Ctrl-C) propagates; one raised by engine code is an
        engine fault in the child, exit 2.

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
exit, a timeout, an exception) the parent reads the child's stdout to EOF,
waits for the child's exit WITHOUT reaping it (os.waitid with WNOWAIT), kills
ONLY the child's own process group, whose id it verified against the child's
pid, and only then reaps the child, so the unreaped pid pins the group id
through the kill. The parent holds the DEFAULT SIGCHLD disposition from before
the spawn until after that reap and then restores the caller's: a
caller-inherited SIGCHLD=SIG_IGN would otherwise make the kernel reap the
runner automatically, unpinning its pid and refusing a healthy run (round 9,
W1). A disposition the signal module cannot save (a non-Python handler), or a
spelling check run outside the main thread, leaves the inherited disposition
in place (residual, stated). Residuals, stated: a descendant that moves itself to a new
process group, or to a new session, leaves that group and escapes the kill;
and this process reaps only the child itself, so zombie reaping of descendants
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
72, no result line) while any thread registered with the threading module is
alive, and takes an immutable snapshot of the validated results only after
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
import json
import math
import os
import re
import secrets
import selectors
import signal
import subprocess
import sys
import time
from pathlib import Path

_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from aiqt_corpus import CODE_SPAN_RE  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import REPO_ROOT, resolve_working  # noqa: E402  # grc-config/store, stays local

# D7 length check reuse (P-1.4): import the authoritative per-PR length checker so the
# 100-word / 45-word-sentence ceiling on a root-CHANGELOG compact entry is caught at
# authoring (this aid) rather than only at the pre-push guard. The module name is
# hyphenated, so load it via importlib; reusing its ENTRY_RE + evaluate keeps the two in
# lock-step (no duplicated length logic to drift).
import importlib.util as _ilu  # noqa: E402
_d7_spec = _ilu.spec_from_file_location(
    '_changelog_len_d7', Path(__file__).resolve().parent / 'check-changelog-length-on-pr.py')
_d7 = _ilu.module_from_spec(_d7_spec)
_d7_spec.loader.exec_module(_d7)


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
    vocabulary, patterns and quote masks apply. Additions are checked in
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
        # path. A disposition this module cannot save (a non-Python handler)
        # or cannot swap (not the main thread) is left alone: a real handler
        # does not make the kernel auto-reap (residual: one installed with
        # SA_NOCLDWAIT outside the signal module is indistinguishable here).
        saved_sigchld = signal.getsignal(signal.SIGCHLD)
        if saved_sigchld is not None:
            try:
                signal.signal(signal.SIGCHLD, signal.SIG_DFL)
            except ValueError:
                saved_sigchld = None  # not the main thread: no swap, no restore
        try:
            with subprocess.Popen(
                    [sys.executable, "-I", str(_LANGUAGE_RUNNER), str(_LANGUAGE_GATE)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL, start_new_session=True) as child:
                # start_new_session put the runner alone in a NEW process group
                # whose id is the runner's own pid. That pid stays pinned to the
                # runner (running, then an unreaped zombie) until the child.wait()
                # in the finally below, and the group kill runs BEFORE that reap
                # on every path, so the kill can never target a recycled id or a
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
                    # EVERY completion path (a delivered result, a nonzero exit, a
                    # timeout, an exception) kills engine descendants left in the
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
            # is reaped, on every path (round 9, W1).
            if saved_sigchld is not None:
                signal.signal(signal.SIGCHLD, saved_sigchld)
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
    ENTRY_RE + evaluate so this aid and the D7 delta gate never drift (P-1.4). Only the root
    file is length-gated; the detailed mirror is out of the D7 gate's scope."""
    entries = []
    for path, text in lines:
        if path == "CHANGELOG.md":
            m = _d7.ENTRY_RE.match(text)
            if m:
                entries.append((m.group(1), m.group(2)))
    return [
        ("CHANGELOG.md", f"D7 length ceiling exceeded ({offence})", "")
        for offence in _d7.evaluate(entries, _d7.DEFAULT_WORD_MAX, _d7.DEFAULT_SENTENCE_MAX)
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
    is read from the private sibling). Link CLASSIFICATION stays logical against
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
        logical_target = (logical_source.parent / base).resolve()
        try:
            logical_target.relative_to(public_root)
        except ValueError:
            continue  # resolves outside this repo: treated as cross-repo
        try:
            logical_target.relative_to(logical_working)
        except ValueError:
            # The link left logical .working but stayed in the public repo:
            # resolve existence against the public corpus.
            resolved = logical_target
        else:
            # The link stayed inside logical .working: follow the selected
            # physical working tree (a private-only mirror included).
            resolved = (physical_source.parent / base).resolve()
        if not resolved.exists():
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


def unresolved_links_in_mirror(root: Path | None = None) -> list[tuple[int, str, str]]:
    """Every in-repo relative markdown-link target in the WHOLE detailed mirror
    that does NOT resolve. Returns ``(line_no, target, line_text)`` per dangling
    link. Reuses ``unresolved_link_targets`` (same rules). ``root=None`` (the
    default) resolves the mirror via ``resolve_working`` (private sibling then
    in-repo); an explicit ``root`` preserves the temp-fixture behaviour. Link
    targets resolve against ``REPO_ROOT`` in the default case, since the mirror's
    references are authored relative to the public corpus. Returns [] if absent."""
    if root is None:
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


def _foreign_repo_env() -> dict[str, str]:
    """This process's environment for a ``git diff`` in ANOTHER repository (the operational store or
    the private sibling holding the mirror): every variable that ``git rev-parse --local-env-vars``
    names as local to one repository is dropped (GIT_INDEX_FILE, GIT_DIR, GIT_WORK_TREE,
    GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_DIRECTORIES, GIT_COMMON_DIR, GIT_CONFIG_PARAMETERS
    and the rest; git drops the same list before it enters a submodule), and every other variable
    is kept. A pre-commit hook inherits them for the PUBLIC repository (``git commit -a`` names its
    temporary index in GIT_INDEX_FILE), and the mirror's ``git diff --cached`` read that index
    through them: it found no staged mirror addition, so a commit the standalone aid refuses passed
    (3b141 QA r2). A failure to list them raises ``CalledProcessError``, and ``main()`` exits 2."""
    local = set(subprocess.run(["git", "rev-parse", "--local-env-vars"], capture_output=True,
                               text=True, check=True).stdout.split())
    return {k: v for k, v in os.environ.items() if k not in local}


def _added_lines_from_repo(
    repo: Path, paths: tuple[str, ...], staged: bool, env: dict[str, str] | None = None
) -> list[tuple[str, str]]:
    """(file, added-line-text) for every added CHANGELOG line in ONE repo's diff, run with ``env``:
    None inherits this process's environment, right for the public repository, where a pre-commit
    hook's GIT_INDEX_FILE names the index being committed; a mirror in another repository passes
    :func:`_foreign_repo_env`.

    The flags override every setting that would reshape what the parser below reads (3b141 QA
    r1): an external diff driver (``diff.external``, ``GIT_EXTERNAL_DIFF``, the ``command`` of a
    ``diff=<driver>`` attribute), a ``textconv`` filter, a ``-diff`` or ``binary`` attribute (it
    prints "Binary files ... differ"), colour (``color.diff``, ``color.ui``), and the ``+++ b/``
    prefix (``diff.noprefix``, ``diff.mnemonicPrefix``, ``diff.dstPrefix``). Each leaves no
    ``+++ b/`` header or ``+`` line, so the aid reported 0 added lines and passed. Not pinned: the
    source prefix (only the ``---`` line carries it, and the parser skips that line), and
    ``diff.relative`` (it changes a path, never whether a ``+`` line is read).

    A git failure raises ``CalledProcessError`` carrying git's ``stderr``, and ``main()`` exits 2:
    an unread diff is not zero added lines. This replaces the 3.190 fail-open, which returned []
    for any git failure (a sibling that is not a git repository included), so a failed diff
    printed "OK: 0 added CHANGELOG line(s)" and exited 0."""
    cmd = ["git", "diff", "--no-ext-diff", "--no-textconv", "--text", "--no-color",
           "--dst-prefix=b/", "--unified=0"]
    if staged:
        cmd.append("--cached")
    cmd += ["HEAD", "--", *paths]
    out = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True,
                         check=True, env=env).stdout
    results: list[tuple[str, str]] = []
    current: str | None = None
    for line in out.splitlines():
        if line.startswith("+++ b/"):
            current = line[len("+++ b/") :]
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+") and current is not None:
            results.append((current, line[1:]))
    return results


def added_lines(staged: bool, root: Path = REPO_ROOT) -> list[tuple[str, str]]:
    """Added CHANGELOG lines across the public repo AND the (post-move) private
    detailed mirror. The public root CHANGELOG.md (and, pre-move, the in-repo
    mirror) come from this repo's diff; a private-sibling mirror gets its OWN
    repository-local ``git diff`` so private additions still receive the dash and
    unlinked-path checks. That diff runs without this repository's local git
    variables (:func:`_foreign_repo_env`), so ``--staged`` reads THAT repository's
    index. The ``staged`` choice is applied separately in each repository,
    preserving staged-only versus full-working-tree semantics."""
    public_paths = ["CHANGELOG.md"]
    if (root / DETAILED_MIRROR_REL).is_file():
        public_paths.append(DETAILED_MIRROR_REL)
    results = _added_lines_from_repo(root, tuple(public_paths), staged)
    mirror = resolve_working(
        DETAILED_MIRROR_REL[len(".working/"):], repo_root=root
    )
    if mirror is None or not mirror.is_file():
        return results
    try:
        mirror.relative_to(root.resolve())
    except ValueError:
        # The mirror lives outside this repo (the operational store, Option C, or a
        # private sibling). resolve_working already located it; derive its OWN repo
        # root from the stripped mirror-relative path's depth (store layout is
        # changelog-details/<file> -> root is parents[1]) and diff it there with the
        # stripped rel path, so the store (no .working/ prefix) and any sibling layout
        # both resolve correctly. Fixes the prior parents[2]+".working/"-rel mismatch
        # that silently no-op'd the store mirror's added-line checks.
        stripped_rel = DETAILED_MIRROR_REL[len(".working/"):]
        private_root = mirror.parents[stripped_rel.count("/")]
        results.extend(
            _added_lines_from_repo(private_root, (stripped_rel,), staged,
                                   env=_foreign_repo_env())
        )
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
        lines = added_lines(args.staged)
    except subprocess.CalledProcessError as exc:
        # Fail closed (3b141 QA r1): a failed diff is not zero added lines.
        detail = (exc.stderr or "").strip()
        print(f"ERROR: git diff failed: {exc}" + (f"\n{detail}" if detail else ""), file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: the CHANGELOG diff could not be read: {exc}", file=sys.stderr)
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
