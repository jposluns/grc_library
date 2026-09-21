#!/usr/bin/env python3
"""Preflight aid: predict the per-document Version/Date co-bump (D4) for the commit you are about to make.

D4 (``check-date-cobump-on-pr.py``) compares each bumped document's ``Date`` with the UTC committer date
of the PR-range commit that touched it -- which is only known AFTER committing. This aid runs BEFORE the
commit and PREDICTS that check for a commit made now: for every document whose ``Version`` differs from the
base, it flags a ``Date`` that is missing, malformed, or not today's UTC date, and prints the exact metadata
line to use. It is block-and-print (no auto-fix, no staging) and strictly read-only.

It predicts ``git commit``, which commits the INDEX, so it inspects the STAGED (index) content -- the exact
bytes that will be committed -- via ``git show``. That is deliberate: reading the working tree instead would
mispredict whenever the index and working tree diverge (a staged bump whose Date fix was not re-staged, a
``git rm --cached`` copy left on disk, a clean/smudge filter or working-tree-encoding), and would run those
filters as a side effect. The index blob is already the converted, about-to-be-committed content, so this aid
and D4 always agree on what they inspect. Run it after ``git add`` and before ``git commit``.

It is NOT a push gate: a document correctly dated in an earlier branch commit stays valid tomorrow, so
predicting "today" must never fail a push. D4 remains the authority after committing; this aid only saves a
round-trip (and a UTC-rollover surprise) by catching a stale Date before the commit.

Exit codes: 0 clear; 1 one or more predicted findings; 2 inspection/scope error (unreadable Git state, a
missing base, an in-progress merge or unmerged index, or a non-UTF-8 tracked filename).

Reuses ``check-date-cobump-on-pr.py`` (D4) for the exemption set and ``aiqt_corpus`` for the Version/Date
field extraction, so this aid and the D4 gate never drift on what they inspect.

Scope boundaries (two documented residues, D-220 round-10; D4 remains the post-commit authority):
- STAGED scope: this aid predicts the co-bump status of the STAGED changes you are about to commit. A
  pre-existing stale Version/Date bump introduced by an EARLIER commit already in the PR range is NOT
  re-audited here; D4 catches it over the whole ``merge-base..HEAD`` range at push (and it would have
  been caught when that earlier commit was made). A "clear" from this aid is therefore scoped to the
  staged changes, which is what its output states.
- Index MTIME: reading git's index can refresh ``.git/sharedindex.*`` timestamps under the split-index
  feature (``core.splitIndex``). That is git's own read-side behaviour and mutates no tracked content
  or state; the aid's read-only contract is that it never changes tracked content, refs, objects, or
  the working tree, not that it never lets git touch an index mtime.
- FILENAME NEWLINES: a filename containing a raw CR or LF byte is enumerated through git's text-mode
  helper, which applies universal-newline translation, so such a name can be mis-identified. Both this
  aid and D4 share that helper and behave identically; a CR/LF in a filename is pathological input the
  corpus never produces, and D4 remains the post-commit authority.
- GITLINK CONVERSION: if a versioned ``.md`` is converted to a git submodule (gitlink) in the staged
  change, the aid skips the non-blob entry while D4 renders the referenced commit and reports the lost
  Version field. The aid does not model this (a documentation file becoming a submodule is nonsensical
  and never occurs in the corpus); D4 remains the authority.
- INVALID GIT CONFIG: under an INVALID git configuration value (e.g. ``log.showSignature=<not-a-bool>``)
  git commands fail and D4 can treat the failure as absent content. Predicting D4 exactly under a broken
  git configuration is outside the aid's contract; the misconfiguration is the operator's to fix.
- PARTIAL CLONE + D4: in a partial clone (a promisor remote) with a base blob unavailable, the aid
  correctly scope-errors (2) while D4 may treat the unavailable blob as absent and clear (0). This is
  the SAFE direction (the aid is stricter); D4 runs in a full clone in CI, where the blob is present.
- INTERPRETER-STARTUP .pyc: ``from __future__ import annotations`` MUST be the module's first statement
  (a language rule), so it executes before ``sys.dont_write_bytecode = True`` and, on a cold cache with
  a writable bytecode target, git-independent interpreter startup may write ``__future__``'s ``.pyc``.
  This is the interpreter caching its own stdlib module, not the aid writing tracked content.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # set FIRST, before any other import, so no .pyc cache is written

import argparse  # noqa: E402
import datetime  # noqa: E402
import importlib.util as _ilu  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402
# Never trigger a partial-clone lazy fetch (which writes pack files): the aid must stay read-only.
# This is a plain boolean env git reads directly, so setting it here overrides any inherited value
# (unlike a config override, which an inherited GIT_CONFIG_PARAMETERS could defeat).
os.environ["GIT_NO_LAZY_FETCH"] = "1"
# Remove GIT_CONFIG so the aid's `git config` promisor query inspects the SAME configuration hierarchy
# (repo/global/system) that git's other commands use. An inherited GIT_CONFIG=<file> redirects only
# the config-READ to that single file, which would hide the repo's `remote.*.promisor` and defeat
# partial-clone detection (making an unavailable base blob look merely absent). GIT_CONFIG_GLOBAL/
# SYSTEM do not hide the repo-local promisor, so only GIT_CONFIG is removed.
os.environ.pop("GIT_CONFIG", None)
# Disable every file-writing git trace/logging vector. Setting each to "0" DISABLES it, which
# (unlike deleting the var) also overrides a GLOBAL/SYSTEM ``trace2.*target`` CONFIG that a late
# command-line ``-c`` cannot prevent, because git initialises trace2 before applying ``-c``. An
# inherited ``GIT_TRACE2_EVENT=<path>`` (or a global config target) otherwise makes a git subprocess
# WRITE a trace file, breaking this aid's strict read-only contract. Covers the known GIT_TRACE* set
# plus any other inherited GIT_TRACE* var.
_GIT_TRACE_VARS = (
    "GIT_TRACE", "GIT_TRACE2", "GIT_TRACE2_EVENT", "GIT_TRACE2_PERF",
    "GIT_TRACE_PACKET", "GIT_TRACE_PERFORMANCE", "GIT_TRACE_SETUP",
    "GIT_TRACE_CURL", "GIT_TRACE_CURL_NO_DATA", "GIT_TRACE_REFS",
    "GIT_TRACE_FSMONITOR", "GIT_TRACE_PACK_ACCESS", "GIT_TRACE_SHALLOW",
)
for _tv in set(_GIT_TRACE_VARS) | {_k for _k in os.environ if _k.startswith("GIT_TRACE")}:
    os.environ[_tv] = "0"
# B4: never crash on output encoding (e.g. PYTHONIOENCODING=ascii with a non-ASCII path in a
# finding): escape unencodable characters rather than raising UnicodeEncodeError mid-print.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="backslashreplace")
    except (AttributeError, ValueError):  # pragma: no cover - non-reconfigurable stream
        pass
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
    from aiqt_corpus import (  # noqa: E402  # generic core (behaviour-identical to lint_common)
        git as _raw_git,
        head_version,
        parse_iso_date,
        parse_metadata_block,
    )
except (ImportError, RuntimeError, OSError, ValueError, SyntaxError, EOFError) as _boot_exc:
    # A bad AIQT_PACK_ROOT (e.g. an unresolvable ~user) or a missing pack dependency must be a clean
    # scope error, not a traceback: the bootstrap runs at import, outside main()'s ScopeError handler.
    print(f"ERROR: cannot initialise the AIQT pack ({_boot_exc}); no prediction made.", file=sys.stderr)
    raise SystemExit(2)


def git(*args: str) -> str:
    """Every git invocation this aid makes carries the highest-precedence ``-c
    core.fsmonitor=false`` so a configured fsmonitor hook (which can write files) never runs. A
    command-line ``-c`` outranks GIT_CONFIG_* and GIT_CONFIG_PARAMETERS, unlike an environment
    override, which an inherited GIT_CONFIG_PARAMETERS can defeat. The aid must stay read-only."""
    try:
        return _raw_git(
            "-c", "core.fsmonitor=false",
            # Defence in depth against the config-based trace2 vector (the env vars are scrubbed
            # above): an empty target disables the file writer git would otherwise open.
            "-c", "trace2.eventtarget=",
            "-c", "trace2.perftarget=",
            "-c", "trace2.normaltarget=",
            *args,
        )
    except OSError as exc:  # git binary missing / not launchable (e.g. restricted PATH)
        raise ScopeError(f"cannot launch git ({exc})") from exc


def git_show(ref: str, path: str) -> str | None:
    """``git show ref:path`` content (fsmonitor disabled), or None if the blob is ABSENT. An
    UNDECODABLE blob raises UnicodeDecodeError, which the caller turns into a scope error."""
    try:
        return git("cat-file", "blob", f"{ref}:{path}")
    except subprocess.CalledProcessError:
        return None  # absent, or a non-blob (e.g. a .md gitlink): cat-file blob errors -> skip


def index_blob(path: str) -> str | None:
    """Stage-0 index content of ``path`` -- exactly what ``git commit`` will record -- or None if the
    path is not in the index. Uses the EXPLICIT ``:0:<path>`` form so a filename beginning with a
    stage prefix (e.g. ``0:review.md``) is not misparsed as ``:<stage>:<path>`` and silently skipped.
    An UNDECODABLE blob raises UnicodeDecodeError, which the caller turns into a scope error."""
    try:
        return git("cat-file", "blob", f":0:{path}")
    except subprocess.CalledProcessError:
        return None  # not in the index, or a non-blob (gitlink): cat-file blob errors -> skip

# D4 owns the exemption set (EXEMPT_FILES / EXEMPT_PREFIXES / the .md-only rule); reuse its
# ``is_exempt`` verbatim so this aid never inspects a file D4 would skip. The filename is
# hyphenated, so load it via importlib (the same pattern preflight-changelog.py uses for D7).
try:
    _d4_spec = _ilu.spec_from_file_location(
        "_date_cobump_d4", Path(__file__).resolve().parent / "check-date-cobump-on-pr.py"
    )
    _d4 = _ilu.module_from_spec(_d4_spec)
    _d4_spec.loader.exec_module(_d4)
    is_exempt = _d4.is_exempt
except (ImportError, OSError, AttributeError, SyntaxError, ValueError, EOFError) as _d4_exc:
    # The D4 module or one of its dependencies is missing / unloadable (e.g. an unstaged deletion of
    # check-date-cobump-on-pr.py or lint_common.py): a clean scope error, not a traceback. This load
    # runs at import, before main()'s ScopeError handler, so it exits here directly.
    print(f"ERROR: cannot load the D4 gate module ({_d4_exc}); no prediction made.", file=sys.stderr)
    raise SystemExit(2)


class ScopeError(Exception):
    """An inspection or scope problem that should exit 2 (not a content finding)."""


def _today_utc() -> datetime.date:
    # PREFLIGHT_VD_TODAY (an ISO YYYY-MM-DD) overrides "now" for deterministic tests and
    # reproducible reruns; a non-conforming value (fromisoformat also accepts basic forms
    # like 20260920) falls back to the real UTC date.
    override = os.environ.get("PREFLIGHT_VD_TODAY")
    if override and re.fullmatch(r"\d{4}-\d{2}-\d{2}", override):
        try:
            return datetime.date.fromisoformat(override)
        except ValueError:
            pass
    return datetime.datetime.now(datetime.timezone.utc).date()


def _special_state() -> str | None:
    """A short reason if the repository is in a state where the prospective commit cannot be
    reliably predicted (so the aid returns a scope error rather than guess), else None. An
    in-progress MERGE has extra parents that move the base D4 later compares against; unmerged
    (conflicted) index entries cannot be committed yet and have no readable stage-0 blob. A
    RESOLVED cherry-pick / rebase / revert is fine and is deliberately NOT rejected here."""
    if os.environ.get("GIT_COMMITTER_DATE") and not os.environ.get("PREFLIGHT_VD_TODAY"):
        # GIT_COMMITTER_DATE overrides the committer date D4 compares against, so the aid's wall-clock
        # "today" would mispredict; without a way to know the prospective committer date reliably, decline.
        return "GIT_COMMITTER_DATE overrides the commit date; cannot predict reliably (D4 is authoritative)"
    try:
        git("rev-parse", "--verify", "--quiet", "MERGE_HEAD^{commit}")
        return "a merge is in progress (MERGE_HEAD present)"
    except subprocess.CalledProcessError:
        pass
    try:
        if git("ls-files", "--unmerged").strip():
            return "the index has unmerged (conflicted) entries"
    except subprocess.CalledProcessError:
        pass
    except UnicodeDecodeError:
        return "the index has a non-UTF-8 unmerged entry"
    # A partial clone (a promisor remote) may not hold the base commit's blobs; with lazy fetch
    # disabled (read-only), those reads would fail and be misread as absent files. Decline.
    try:
        promisors = git("config", "--get-regexp", r"^remote\..*\.promisor$")
    except subprocess.CalledProcessError:
        promisors = ""  # no promisor remote -> not a partial clone
    except UnicodeDecodeError:
        # An accented / non-UTF-8 remote name under an ASCII locale makes the config output
        # undecodable; we cannot tell whether a promisor remote is present, so decline (scope error).
        return "a remote name is non-UTF-8; cannot read partial-clone config reliably"
    for _line in promisors.splitlines():
        _key = _line.split(None, 1)[0] if _line.strip() else ""
        if not _key:
            continue
        try:
            # Let git normalise the boolean itself, so 1 / yes / on / True / 2 / a bare key all
            # count as true exactly as git reads them (a literal ``endswith("true")`` missed these).
            _norm = git("config", "--type=bool", "--get", _key)
        except (subprocess.CalledProcessError, UnicodeDecodeError):
            return "cannot normalise a partial-clone config value; declining"
        if _norm.strip() == "true":
            return "this is a partial clone; base objects may be unavailable without a fetch"
    return None


def _resolve_base(base_arg: str | None) -> str:
    """Resolve the base for comparison, or raise ScopeError. To match the D4 gate this predicts
    (which ranges over ``merge-base(base, HEAD)..HEAD``), the comparison base is the MERGE-BASE of
    the requested ref and HEAD, so an independently-advanced upstream (e.g. origin/main ahead of
    the branch point) cannot hide a co-bump. When HEAD is unborn or shares no ancestor with the ref,
    D4 rejects the range, so the aid scope-errors (exit 2) and defers to D4 rather than diverge."""
    ref = base_arg or os.environ.get("BASE_REF") or "origin/main"
    try:
        commit = git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").strip()
    except subprocess.CalledProcessError as exc:
        raise ScopeError(
            f"cannot resolve base ref '{ref}'. Pass --base <ref> or set BASE_REF. ({exc})"
        ) from exc
    try:
        merge_base = git("merge-base", commit, "HEAD").strip()
    except subprocess.CalledProcessError as exc:
        # B4: no common ancestor (or unborn HEAD). D4 rejects such a range (exit 2), so the aid makes
        # no prediction and defers to D4 post-commit rather than diverging by comparing against the ref.
        raise ScopeError(
            f"'{ref}' shares no common ancestor with HEAD (or HEAD is unborn); D4 rejects such a "
            f"range, so no prediction is made. ({exc})"
        ) from exc
    return merge_base or commit


def _date_field(content: str | None) -> tuple[datetime.date | None, str | None]:
    """(parsed Date, problem) for a document's metadata Date. problem is one of
    None / 'missing' / 'malformed'."""
    if content is None:
        return None, "missing"
    raw = parse_metadata_block(content).fields.get("Date")
    if raw is None:
        return None, "missing"
    parsed = parse_iso_date(raw)
    if parsed is None:
        return None, "malformed"
    return parsed, None


def _staged_paths() -> list[str]:
    """Non-exempt .md paths STAGED for the prospective commit -- the index differs from HEAD, i.e.
    exactly the files ``git commit`` would record NOW (not the whole PR delta vs the base, which
    would spuriously re-flag documents correctly bumped in earlier branch commits). The Version
    event is still judged against the merge-base in ``find_findings``, so a body-only edit of an
    earlier bump is still caught. Compares stored blobs (no working-tree read, no clean/smudge
    filter run). ``-c diff.autoRefreshIndex=false`` keeps the .git/index stat cache unwritten
    (the git wrapper already disables fsmonitor); ``--no-relative`` keeps paths repo-root-relative.
    Both this aid and D4 enumerate with ``-z`` (NUL-delimited, never quoted), so every filename --
    non-ASCII, or ASCII containing a quote/backslash/control char -- is enumerated identically and
    the two stay in exact parity regardless of ``core.quotePath``. A filename that is not valid
    UTF-8 raises UnicodeDecodeError here and becomes a scope error (below)."""
    args = ["-c", "diff.autoRefreshIndex=false", "diff", "--cached",
            "--name-only", "-z", "--no-renames", "--no-relative"]
    try:
        out = git(*args)
    except subprocess.CalledProcessError as exc:
        raise ScopeError(f"git {' '.join(args)} failed: {exc}") from exc
    except UnicodeDecodeError as exc:
        # a tracked filename is not valid UTF-8; the aid cannot enumerate reliably. D4
        # (running after the commit) remains the authority.
        raise ScopeError(f"a tracked filename is not valid UTF-8; cannot inspect ({exc})") from exc
    return [p for p in out.split("\0") if p and not is_exempt(p)]


def find_findings(base: str, today: datetime.date, paths: list[str]) -> list[str]:
    """One human-readable finding per document whose Version changed vs the base (in the index)
    but whose staged Date is not today's UTC date (missing, malformed, or a different day)."""
    findings: list[str] = []
    for path in paths:
        # git_show returns None only when the blob is ABSENT (an add has no base; a staged delete
        # has no index blob) -> those are out of D4's co-bump scope and skipped. An UNDECODABLE
        # blob is an inspection failure, not an absence: it must scope-error, never silently clear
        # a staged stale bump (codex R5 P2).
        try:
            base_content = git_show(base, path)
            index_content = index_blob(path)  # the stage-0 index blob = what git commit records
        except UnicodeDecodeError as exc:
            raise ScopeError(f"a staged or base blob for '{path}' is not valid UTF-8; cannot inspect ({exc})") from exc
        if base_content is None or index_content is None:
            continue
        base_version = head_version(base_content)
        index_version = head_version(index_content)
        if base_version == index_version:
            continue  # no Version event -> D4 will not fire; Date may legitimately be unchanged
        date, problem = _date_field(index_content)
        if problem is None and date == today:
            continue  # correctly co-bumped for a commit made today
        observed = "missing" if problem == "missing" else (
            "malformed" if problem == "malformed" else date.isoformat()
        )
        findings.append(
            f"FAIL {path} [index]: Version {base_version} -> {index_version}; "
            f"Date {observed}; expected {today.isoformat()} UTC.\n"
            f"  Set the metadata Date line to (preserve the existing line-break style):\n"
            f"  **Date:** {today.isoformat()}\\\n"
            f"  then re-stage the file (git add) and re-run."
        )
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Predict the D4 Version/Date co-bump for the commit you are about to make (it inspects "
            "the staged/index content). Block-and-print; never a push gate (D4 is authoritative "
            "after committing). Run after `git add`, before `git commit`."
        )
    )
    parser.add_argument("--base", help="base ref (default: $BASE_REF or origin/main)")
    parser.add_argument(
        "--staged",
        action="store_true",
        help="accepted for compatibility; the aid always inspects the staged (index) content",
    )
    args = parser.parse_args(argv)

    try:
        state = _special_state()
        if state is not None:
            raise ScopeError(
                f"{state}; the prospective commit cannot be reliably predicted. "
                "Resolve it; D4 checks the co-bump after the commit."
            )
        base = _resolve_base(args.base)
        today = _today_utc()
        paths = _staged_paths()
        findings = find_findings(base, today, paths)
    except ScopeError as exc:
        print(f"preflight-version-date: SCOPE ERROR: {exc}", file=sys.stderr)
        return 2

    if not findings:
        print(
            "OK: every staged document with a Version change is dated "
            f"{today.isoformat()} (UTC) for a commit made today."
        )
        return 0
    print(
        f"preflight-version-date: {len(findings)} staged document(s) would fail the D4 "
        "Version/Date co-bump for a commit made today:\n"
    )
    for f in findings:
        print(f)
        print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
