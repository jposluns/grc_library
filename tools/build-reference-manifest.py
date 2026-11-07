#!/usr/bin/env python3
"""Generate the public reference-acquisition manifest (1.19.7 (closing PR #1007)).

The manifest [`docs/reference-acquisition-manifest.md`] is a PUBLIC BIBLIOGRAPHY of the
corpus's citation-source reference base: for each trusted-bucket entry in
`grc_library_ref/catalogue.yml` (standards / frameworks / legislation / programs) it lists
the title, version/edition, bucket, upstream URL, and acquisition class (free|licensed),
with the held source TEXT stripped. An adopter's `/adopt` uses it to bootstrap a `.ref`:
FREE sources are web-fetched, LICENSED sources are listed for manual acquisition.

**Copyright guardrail:** this reads ONLY catalogue bibliographic metadata (`title`,
`origin`/`body`/`jurisdiction`, `checked_edition`, `upstream_url`, `bucket`, `acquisition`);
it NEVER reads the held `--full-text` files nor the catalogue `notes`/`extract` fields, and
never reproduces source prose. The manifest is a bibliography, never the texts.

**Sibling-independence:** this is an ORCHESTRATOR/maintainer tool. It locates the real
`grc_library_ref` sibling via `lint_common.resolve_sibling("ref", strict=True)`. With that
sibling absent, regenerating NO-OPS (exit 0) in every context, for an adopter's portable clone.
`--check` with it absent never reports a success it did not earn (3b796). It keeps the explicit
static-ship no-op (exit 0, saying it did not check) only when all of these hold: no
repository-redirecting variable is set (GIT_DIR, GIT_WORK_TREE, or one of
`lint_common._GIT_REDIRECT_VARIABLES`), whatever it names, so an adopter whose git exports GIT_DIR
to a linked worktree's hooks sees exit 4 too; `lint_common.require_own_git_dir` confirms git reads
this checkout's own repository; `git remote get-url origin` exits 0, prints nothing on stderr and
prints exactly one line, the value and one LF, with no other LF or CR in it; that value is an
`https://`, `http://` or `ssh://` URL or a `user@host:owner/repo` form whose path is exactly
`owner/repo` (an optional `.git` or trailing slash aside) and is not the maintainer's
`jposluns/grc_library` on any host; and `tools/detect-env.py` `probe_identity`, the identity source
`tools/ref-holds.py` `_operator_is_adopter` reads, run in a separate, isolated process, gives the
same value as not the maintainer repository. A clone whose origin is the maintainer repository on
`github.com` exits 4 (cannot evaluate) with one line naming the missing sibling, and so does every
other context (a local-path, `file://`, `git://`, userless `host:path` or otherwise unplaced
origin, an SSH host alias or other host serving `jposluns/grc_library`, no readable `origin`, a
garbled read, a detector process whose result fails a check, or a detector that disagrees), which
is never read as adopter; there the line also gives the cause, in fixed wording that may carry a
redirect variable's name, git's exit code, the detector process's exit status, signal number or
time limit, or an exception's type name, and never any part of the origin, of a refusal, of a
command line or of the detector process's output: the redirect variable set (its name only);
`require_own_git_dir` not confirming that git reads this checkout's own repository, through the
layout or the environment (that category only, for every refusal: its refusal text is withheld,
because it can carry paths taken from the environment, and `_repository_redirect` says how to
print it); the origin read's validation failure (with git's exit code when it is not 0); an origin
in no form the check places; the maintainer repository (`MAINTAINER_ORIGIN_OWNER_REPO` in
`tools/detect-env.py`) on a host other than `github.com`; the check the detector process's result
failed, or the detector disagreeing; or, for an unexpected exception in this tool's own process,
the part that failed (the repository check or the origin read, running the detector process, or
placing the origin with what the detector gave) and the exception's type name, read without
running code the exception's class or metaclass defines (a fixed text when it cannot be read).
Trust boundary (3b796 round 8): the detector runs in a separate process (`sys.executable -I`
running a fixed program that loads this tool's own `tools/detect-env.py` by path and prints its
maintainer owner/repo, origin and maintainer flag as one JSON object), under a time limit, with
stdin from the null device, no inherited `GIT_` variable and the checkout as its working
directory, so its exceptions, class definitions and process-state changes cannot reach this tool.
What this tool trusts is the child's validated output only: exit status 0, nothing on stderr,
valid UTF-8, and exactly one line holding one JSON object with exactly the expected keys and value
types, in the form the program writes; any other result (a timeout, a signal, a non-zero exit,
malformed or extra output) is undecidable, and none of the child's output is printed. The child
is ended on every path (3b796 round 9): this tool reads both pipes itself, without
`Popen.communicate`, and on POSIX sees the child exit without reaping it (`os.waitid` with
`WNOWAIT`), so after a normal finish, the time limit, an interrupt or any other exception it kills
the child's whole process group while the child's pid still pins that group id (a descendant still
running in the group after a normal finish included, so nothing the detector starts there outlives
the check), then closes the pipes and reaps the child. Each cleanup step (the group kill, the
child kill, each pipe close and the reap) runs even when an earlier one raises, and the first
exception (an interrupt before any other) goes on once the reap has been attempted (3b796 round
11); an exception already on its way from starting or waiting for the child counts as the first,
so an interrupt while waiting stays an interrupt whatever a cleanup step then raises, the group
kill passes over only a group that is already gone (ESRCH) and records any other failure, and
when neither kill returned the reap waits at most a fixed second (3b796 round 12). SIGCHLD is
held at its default disposition around all of this tool's subprocess work on this path, from
before the repository check's first git read, through the origin read, until the detector child
is reaped, and the caller's disposition is put back after, on every path (3b796
rounds 10 and 11): with SIGCHLD ignored the kernel reaps each child itself, so Python's subprocess
reports a git read's exit status as 0 whatever git exited with, the detector's exit could not be
seen without reaping it, and its pid would no longer pin its group id. Off the main thread, or
where the disposition cannot be read or set, nothing is run, not even the repository check, and
the line gives that fixed cause; when setting it raises, the caller's disposition is still put
back, and the cause stays the fixed one unless putting it back raises too, which gives the
could-not-be-put-back cause instead (3b796 round 12). A platform without SIGCHLD has nothing to
hold. Placing the origin and the agreement check run in this process on those plain values. An
exception in this tool's own parts, a SystemExit included, gives that line too; only
KeyboardInterrupt passes through.
Residuals: a detector that prints valid but wrong values is trusted (equivalent to editing the
checkout's own code; the child runs as the same user, so the process boundary is not a sandbox,
and detector code acting outside its own process is that same edit); the child's resources are not
limited beyond the time limit; a descendant that leaves the child's process group is not stopped;
an interrupt that lands inside `subprocess.Popen` after the fork and before the child is bound can
leave the child running; on the thread fallback, an interrupt inside `Thread.start` after the
thread has begun leaves that running reader unrecorded, and its pipe is then closed under it; any
interrupt that lands during the cleanup, the first one included (after a normal finish, the time
limit or another exception as much as after an earlier interrupt), can cut short the step it lands
in, so it can leave the child or its group running, a pipe open or the child unreaped, though the
later steps still run; a reap that fails (an interrupt or another exception inside
`Popen.wait`, or, when both kills raised, its one-second limit passing) leaves the child
unreaped, a zombie or, if both kills also failed, still running, with its pid and process group
id pinned until this process exits or something reaps it, and SIGCHLD is put back after that
failed reap all the same, and the line gives the could-not-be-run cause with the exception's type
name (an interrupt passes through); an interrupt that lands at the instant the caller's SIGCHLD
disposition is put back leaves SIGCHLD at its default, and so does a failure to put it back,
which gives its own fixed cause naming the exception's type, also when setting it had raised
first; the hold is process-wide, so a child another thread of the caller ends during it is not
reaped automatically, and a git read or child another thread starts then sees SIGCHLD at its
default; for in-process embedding only (the command line is a fresh process, where only the
default and ignored dispositions survive the exec and both are read exactly, as
tools/preflight-changelog.py states for its own hold): `signal.getsignal` gives Python's own
record, so a SIGCHLD handler that native code installs after interpreter startup, outside the
signal module, reads as that stale record and is put back as it, replacing the native
handler (one installed before startup reads as unreadable, and nothing is run); on POSIX
without `os.waitid` and `WNOWAIT` the child is reaped once both pipes close, so a descendant left
in its group without the pipes is not stopped after a normal finish; and on a platform without
process groups only the child itself is killed, and a pipe a surviving descendant holds stays open
until the tool exits (the tests run the POSIX path with `os.waitid`, and the thread fallback only
where a test forces it on POSIX).
Control characters, U+2028 and U+2029 in the displayed sibling path are written as escapes, so
the diagnostic stays one line whatever its parent directory is named. Known residual: git
configuration that both reads share (the repository's own config, the global files under HOME and
XDG_CONFIG_HOME, and the system file), such as a `url.<base>.insteadOf` rewrite or a
`remote.origin.url`, changes what `git remote get-url` prints in this tool and in the detector
process alike, so a maintainer clone whose printed origin becomes a fork URL that way still takes
the no-op, as do the layouts `require_own_git_dir` lists as its own residuals. Configuration this
tool's `GIT_` variables supply (`GIT_CONFIG_COUNT` and its `GIT_CONFIG_KEY_<n>` and
`GIT_CONFIG_VALUE_<n>` pairs, `GIT_CONFIG_PARAMETERS` from `git -c`, `GIT_CONFIG_GLOBAL`,
`GIT_CONFIG_SYSTEM`, `GIT_CONFIG_NOSYSTEM`, and a `safe.directory` supplied that way) reaches this
tool's read only, since the detector process gets no `GIT_` variable: a difference it makes to the
origin either read gives makes the two reads disagree, and `--check` exits 4 with the
disagreement cause. A sibling that is
present but unusable (not a directory, a dangling link, or one that cannot be examined) is not
absent: it fails with exit 2 naming it, as does a `catalogue.yml` in it that cannot be examined,
is not a regular file, cannot be read or is not valid UTF-8 (3b677). A `catalogue.yml` genuinely
absent from a usable sibling exits 2 as not found. The probes use `os.lstat`/`os.stat`, so the
verdict is the same on Python 3.11 and 3.12+. It is NEVER a CI gate, and
`check-portability.sh`, which runs the regenerate path, stays green. The maintainer-side
`_ref`-required loud gate lives at `/orch` (detect-env `ref_availability`); `--check` only refuses
to pass without having checked. The committed manifest ships statically, so an adopter gets it
without any sibling.

Usage:
  python3 tools/build-reference-manifest.py            # regenerate the committed manifest
  python3 tools/build-reference-manifest.py --check    # drift check (exit 1 if out of date, 4 if
                                                       # it cannot be evaluated)

`--check` is an orchestrator/maintainer drift check (it reads `_ref`), NOT a CI gate; run it
at `_ref`-update / resume, folded into the resync-`_ref` discipline.
"""
import json
import os
import re
import selectors
import signal
import subprocess
import sys
import threading
import time
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_common  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "docs" / "reference-acquisition-manifest.md"
TRUSTED = ("standards", "frameworks", "legislation", "programs")
# Generator schema version: bump on a change to the manifest's SHAPE (columns,
# header), recorded in CHANGELOG.md. Not the library CalVer, and not the row
# contents (which advance with the reference base). The manifest is exempt from
# the date/version-staleness gates (like docs/portal.md), so this stays stable
# across content regens; the Date below is the reference base's own max currency.
SCHEMA_VERSION = "1.0.0"
FALLBACK_DATE = "2026-07-17"
BUCKET_LABEL = {
    "standards": "Standards",
    "frameworks": "Frameworks",
    "legislation": "Legislation",
    "programs": "Programs",
}


# The YAML 1.1 double-quoted escape set (the one yaml.safe_load implements), plus the three
# hex forms; \x, \u and \U carry 2, 4 and 8 hex digits (P-TODO 3b63).
_DQ_ESCAPES = {"0": "\0", "a": "\a", "b": "\b", "t": "\t", "\t": "\t", "n": "\n",
               "v": "\v", "f": "\f", "r": "\r", "e": "\x1b", " ": " ", '"': '"',
               "/": "/", "\\": "\\", "N": "\x85", "_": "\xa0", "L": "\u2028",
               "P": "\u2029"}
_DQ_HEX = {"x": 2, "u": 4, "U": 8}


def _unescape_double(s: str) -> str:
    """Unescape a YAML double-quoted scalar's backslash escapes: the named escapes and the
    \\x, \\u and \\U hex forms, matching yaml.safe_load for every escape YAML defines.
    Malformed input never raises: an escape YAML does not define, a hex escape with too few or
    non-hex digits or a code point beyond U+10FFFF, and a lone trailing backslash all keep their
    characters literally (yaml.safe_load would raise instead). The catalogue is machine-generated
    and carries none of these."""
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            c = s[i + 1]
            width = _DQ_HEX.get(c)
            digits = s[i + 2:i + 2 + width] if width else ""
            if width and len(digits) == width and all(ch in "0123456789abcdefABCDEF"
                                                      for ch in digits):
                code = int(digits, 16)
                if code <= 0x10FFFF:  # beyond Unicode is malformed: fall through, keep the char
                    out.append(chr(code))
                    i += 2 + width
                    continue
            out.append(_DQ_ESCAPES.get(c, c))
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def _scalar(v: str):
    """Parse a catalogue scalar value: strip a matched surrounding quote pair
    (unescaping YAML escapes per quote style), map bare booleans, else return the
    raw string; a bare null/~ is None and a bare decimal integer an int, as yaml.safe_load gives.
    That is the parity contract: the scalar shapes the catalogue uses (double- and single-quoted
    strings, true/false, null/~, decimal integers) parse as yaml.safe_load parses them. Other YAML
    1.1 forms (hex or octal integers, floats, yes/no/on/off, timestamps) stay literal strings, so
    render() prints exactly what the catalogue author wrote.
    (The audit toolchain is stdlib-only, so this hand-parses the catalogue rather than importing
    PyYAML.)"""
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] == '"':
        return _unescape_double(v[1:-1])
    if len(v) >= 2 and v[0] == v[-1] == "'":
        return v[1:-1].replace("''", "'")  # YAML single-quote escape
    if v == "true":
        return True
    if v == "false":
        return False
    # A bare null or ~ is YAML's null (yaml.safe_load gives None); a bare decimal integer is an
    # int. Without this, an unquoted null reached render() as the literal text "null" (3b63).
    if v in ("null", "~", "Null", "NULL", ""):
        return None
    if re.fullmatch(r"[-+]?(0|[1-9][0-9]*)", v):
        return int(v)
    return v


def _parse_catalogue(text: str) -> dict:
    """Minimal stdlib parser for grc_library_ref/catalogue.yml.

    The catalogue is machine-generated with a fixed, regular shape: top-level
    bucket keys at column 0 (`standards:`), list entries beneath them
    (`  - key: value`), and entry fields (`    key: value`). Values are quoted
    strings, booleans, nulls (None), decimal integers, or other bare scalars kept as text; the one list field (`topics`) is stored
    verbatim and never read. Returns `{bucket: [entry_dict, ...]}`, matching the
    dict shape `render()`/`_max_date()` consume. This avoids a non-stdlib PyYAML
    dependency in the stdlib-only audit toolchain (no tool imports `yaml`)."""
    catalogue: dict = {}
    bucket = None
    entry = None
    # Split on the three ASCII line-break forms only. str.splitlines also splits on U+2028,
    # U+2029, U+0085 and other separators, which would truncate a value that carries one
    # (P-TODO 3b63). A raw one inside a quoted value is kept verbatim here, where
    # yaml.safe_load would fold it into a space; the catalogue carries none.
    for raw in re.split(r"\r\n|\r|\n", text):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*$", raw)  # top-level bucket opener
        if m:
            bucket = m.group(1)
            catalogue.setdefault(bucket, [])
            entry = None
            continue
        if bucket is None:  # pre-bucket top-level metadata scalars: skip
            continue
        m = re.match(r"^  - ([A-Za-z_][\w-]*):\s?(.*)$", raw)  # entry start
        if m:
            entry = {m.group(1): _scalar(m.group(2))}
            catalogue[bucket].append(entry)
            continue
        m = re.match(r"^    ([A-Za-z_][\w-]*):\s?(.*)$", raw)  # entry field
        if m and entry is not None:
            entry[m.group(1)] = _scalar(m.group(2))
    return catalogue


def _text(v) -> str:
    """A parsed catalogue value as display text: None (a YAML null) is empty, anything else is
    str(v), so an int 0 stays "0" rather than vanishing through an `or ""` (P-TODO 3b63)."""
    return "" if v is None else str(v)


def _cell(v) -> str:
    """Escape a value for a markdown table cell (pipes; collapse line breaks, including a bare
    carriage return, which would otherwise split the row for any reader)."""
    return _text(v).replace("|", "\\|").replace("\r\n", " ").replace("\r", " ").replace("\n", " ").strip()


def _issuer(bucket: str, e: dict) -> str:
    if bucket == "programs":
        return _cell(e.get("body", ""))
    if bucket == "legislation":
        return _cell(e.get("jurisdiction", ""))
    return _cell(e.get("origin", ""))


def _max_date(catalogue: dict) -> str:
    """Deterministic manifest Date: the max last_updated across trusted entries
    (the reference base's own currency), else FALLBACK_DATE. Not today() (which
    would break --check)."""
    dates = []
    for bucket in TRUSTED:
        for e in catalogue.get(bucket, []):
            for key in ("last_updated", "last_checked"):
                v = _text(e.get(key))
                if len(v) == 10 and v[4] == "-" and v[7] == "-":
                    dates.append(v)
    return max(dates) if dates else FALLBACK_DATE


def render(catalogue: dict) -> str:
    fields = [
        ("Document Title", "Reference-Acquisition Manifest"),
        ("Document Type", "Guide"),
        ("Version", SCHEMA_VERSION),
        ("Date", _max_date(catalogue)),
        ("Owner", "Governance Library Maintainer"),
        ("Approving Authority", "Governance Library Maintainer"),
        ("Related Documents", "[`README.md`](../README.md), "
         "[`docs/portal.md`](portal.md)"),
        ("Classification", "Public"),
        ("Category", "Documentation"),
        ("Review Frequency", "Regenerated from grc_library_ref/catalogue.yml on any "
         "reference-base change; maintainer-side, not a CI gate"),
        ("Repository Path", "[`docs/reference-acquisition-manifest.md`]"
         "(reference-acquisition-manifest.md)"),
        ("Confidentiality", "Public"),
        ("License", "CC BY-SA 4.0"),
    ]
    lines = [
        "<!--",
        "Auto-generated by tools/build-reference-manifest.py from "
        "grc_library_ref/catalogue.yml.",
        "Do not edit by hand. Regenerate with "
        "`python3 tools/build-reference-manifest.py`.",
        "-->",
        "",
        "# Reference-acquisition manifest",
        "",
    ]
    for i, (name, value) in enumerate(fields):
        suffix = "\\" if i < len(fields) - 1 else ""
        lines.append(f"**{name}:** {value}{suffix}")
    lines += [
        "",
        "---",
        "",
        "## Overview",
        "",
        "**Purpose.** A public bibliography of the citation-source reference base the GRC",
        "Library corpus draws on: the trusted, citation-grade sources (standards, frameworks,",
        "legislation, programs) the corpus cites as ground truth. It lists bibliographic",
        "metadata only, title, version, issuer, upstream URL, and acquisition class, so a fork",
        "adopting the library can acquire the sources it needs. It carries NO source text.",
        "",
        "**How `/adopt` uses it.** When a fork runs `/adopt`, the FREE-class sources are",
        "web-fetched into the adopter's reference sibling; the LICENSED-class sources are listed",
        "for manual acquisition (the adopter obtains them under their own licence). `/adopt`",
        "never redistributes licensed content.",
        "",
        "**Trust and scope.** Only the four citation-grade trusted buckets are listed; untrusted",
        "publications, recommendation-tier books, and scaffolding templates are excluded. The",
        "acquisition class is the source of truth held in `grc_library_ref`'s catalogue: FREE =",
        "freely and legally downloadable from the issuer; LICENSED = purchase, membership, or",
        "paywall required. A blank upstream URL means the catalogue does not yet record one.",
        "",
        "**Generated file, do not hand-edit.** Produced by `tools/build-reference-manifest.py`",
        "from `grc_library_ref/catalogue.yml`; regenerate on any reference-base change (the",
        "generator is maintainer-side, never a CI gate, so the public repo stays clonable",
        "without the private reference sibling).",
        "",
    ]
    total = 0
    free_total = 0
    for bucket in TRUSTED:
        entries = sorted(catalogue.get(bucket, []), key=lambda e: _text(e.get("title")).lower())
        if not entries:
            continue
        free = sum(1 for e in entries if e.get("acquisition") == "free")
        lines += [
            f"## {BUCKET_LABEL[bucket]} ({len(entries)}: {free} free, {len(entries) - free} licensed)",
            "",
            "| Title | Version / edition | Issuer | Upstream URL | Acquisition |",
            "| --- | --- | --- | --- | --- |",
        ]
        for e in entries:
            title = _cell(e.get("title"))
            version = _cell(e.get("checked_edition"))
            issuer = _issuer(bucket, e)
            url = _cell(e.get("upstream_url"))
            acq = _cell(e.get("acquisition", "")).upper()
            lines.append(f"| {title} | {version} | {issuer} | {url} | {acq} |")
            total += 1
            if e.get("acquisition") == "free":
                free_total += 1
        lines.append("")
    lines += [
        f"**Total: {total} sources ({free_total} free, {total - free_total} licensed).**",
        "",
    ]
    return "\n".join(lines) + "\n"


# 3b796: --check with no sibling outside a positively placed adopter clone. Distinct from 1
# (DRIFT), 2 (an unusable sibling or catalogue, or a bad flag) and 3 (an internal error).
EXIT_CANNOT_EVALUATE = 4


# Variables that point git at another repository's git directory, work tree, common directory,
# objects or history (3b796 round 2). Any of them set makes the origin read undecidable, whatever
# it names: the read then need not be this checkout's own origin.
_REDIRECT_VARIABLES = ("GIT_DIR", "GIT_WORK_TREE") + tuple(lint_common._GIT_REDIRECT_VARIABLES)

# The origin forms the decision can place: an https, http or ssh URL, and the user@host:path form,
# each with a path of exactly owner/repo. Anything else (a local path, file:// or git://, a
# userless host:path, a nested path, characters outside these sets) is not placed.
_HOST = r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?"
_SEGMENT = r"[A-Za-z0-9_-][A-Za-z0-9_.-]*"
_PLACED_ORIGINS = (
    re.compile(rf"(?:https?|ssh)://(?:[^@/\s:]+(?::[^@/\s]*)?@)?(?P<host>{_HOST})(?::[0-9]+)?"
               rf"/(?P<owner>{_SEGMENT})/(?P<repo>{_SEGMENT})/?", re.IGNORECASE),
    re.compile(rf"[A-Za-z0-9_.-]+@(?P<host>{_HOST}):(?P<owner>{_SEGMENT})/(?P<repo>{_SEGMENT})/?"),
)


def _origin_read_fault(returncode: int, stdout: bytes, stderr: bytes) -> "str | None":
    """PURE: why ``_origin_from_read`` refuses a raw read, as one short line, else None."""
    if returncode != 0:
        return f"git remote get-url origin exited {returncode}"
    if stderr:
        return "git remote get-url origin wrote to stderr"
    value = stdout[:-1] if stdout.endswith(b"\n") else None
    if not value or b"\n" in value or b"\r" in value:
        return "git remote get-url origin did not print exactly one line with no other LF or CR"
    try:
        value.decode("utf-8")
    except UnicodeDecodeError:
        return "git remote get-url origin printed a value that is not valid UTF-8"
    return None


def _origin_from_read(returncode: int, stdout: bytes, stderr: bytes) -> "str | None":
    """PURE validation of a raw ``git remote get-url origin`` read, before anything strips it: the
    origin value when git exited 0, printed nothing on stderr and printed exactly one line (the value
    and one LF) with no other LF or CR and valid UTF-8, else None. tools/detect-env.py joins stdout
    and stderr, translates CR to LF and strips only the ends of the result, so a leading or trailing
    line break or CR is gone from its value while an internal one and any trace text stay in it;
    this raw read rejects all of them."""
    if _origin_read_fault(returncode, stdout, stderr) is not None:
        return None
    return stdout[:-1].decode("utf-8")


def _origin_parts(origin: str) -> "tuple[str, str] | None":
    """PURE: (host, owner/repo) for an origin in a placed form, an optional ``.git`` dropped from
    the repository name, else None (a form the check does not place)."""
    for form in _PLACED_ORIGINS:
        m = form.fullmatch(origin)
        if m:
            break
    else:
        return None
    repo = m.group("repo")
    if repo.lower().endswith(".git"):
        repo = repo[:-4]
    if not repo:
        return None
    return m.group("host"), f"{m.group('owner')}/{repo}"


def _place_origin(origin: str, maintainer: str) -> "str | None":
    """PURE: "maintainer" for ``maintainer`` (owner/repo) on github.com, "adopter" for a placed form
    naming another owner/repo, else None (not placed). ``maintainer`` on any other host is not
    placed: an SSH host alias or a mirror serving the maintainer repository is not an adopter."""
    parts = _origin_parts(origin)
    if parts is None:
        return None
    host, owner_repo = parts
    if owner_repo.lower() != maintainer.lower():
        return "adopter"
    return "maintainer" if host.lower() == "github.com" else None


def _unplaced_reason(origin: str) -> str:
    """PURE: why ``_place_origin`` left ``origin`` unplaced, as fixed text with no part of the
    origin in it: a placed form can only be left unplaced by the host rule (the maintainer
    repository on a host other than github.com); anything else is not a form the check places."""
    if _origin_parts(origin) is not None:
        return ("the origin names the maintainer repository (MAINTAINER_ORIGIN_OWNER_REPO in "
                "tools/detect-env.py) on a host other than github.com, which the check does not "
                "place")
    return "the origin is not a form the check places as an adopter or maintainer clone"


def _context_from_identity(identity: dict, origin: "str | None", maintainer: str) -> str:
    """PURE decision: "maintainer", "adopter" or "undecidable", from a tools/detect-env.py
    ``probe_identity`` result, the origin ``_origin_from_read`` validated (None when it refused the
    read) and the maintainer owner/repo. Only a positively placed origin the detector read
    identically, with its maintainer flag agreeing, decides; everything else is "undecidable". The
    adopter arm is a strict subset of tools/ref-holds.py ``_identity_is_adopter`` (a non-empty string
    origin with the flag exactly False): probe_identity classifies a failed origin read as
    ``adopter``, so its ``classification`` is not read here."""
    url = identity.get("origin_url")
    flag = identity.get("origin_is_maintainer_repo")
    if origin is None or not isinstance(url, str) or url != origin:
        return "undecidable"
    placed = _place_origin(origin, maintainer)
    if placed == "maintainer" and flag is True:
        return "maintainer"
    if placed == "adopter" and flag is False:
        return "adopter"
    return "undecidable"


_LAYOUT_REFUSED = ("lint_common.require_own_git_dir did not confirm that git reads this checkout's "
                   "own repository (layout or environment)")


def _repository_redirect() -> "str | None":
    """Why the origin read may not be this checkout's own, as one line, else None: a set redirect
    variable (its name only), or ``_LAYOUT_REFUSED`` whenever ``lint_common.require_own_git_dir``
    refuses, one category for every refusal (it did not confirm that git reads this checkout's own
    repository, through the layout or the environment): the layout giving git another
    repository's git directory, an environment variable such as GIT_INDEX_FILE pointing git away
    from it, a directory that is not a repository, or a git command that fails. No part of that
    refusal's text goes into the line: it can carry absolute paths taken
    from the environment (the index GIT_INDEX_FILE names, for one) and command lines, so it is
    withheld, not cut. An operator reaches the detail by running, from the checkout's top level
    in the same environment, ``python3 -c "import pathlib, sys; sys.path.insert(0, 'tools');
    import lint_common; print(lint_common.require_own_git_dir(pathlib.Path.cwd()))"``, which
    prints the refusal in full (None when there is none); the delta gates that call it, such as
    tools/check-stranded-control-code-on-pr.py, print it too."""
    name = next((n for n in _REDIRECT_VARIABLES if n in os.environ), None)
    if name is not None:
        return f"the repository-redirecting variable {name} is set"
    # require_own_git_dir's git reads write their own errors (and any trace) to file descriptor 2;
    # only its verdict is used here, so stderr is silenced around it to keep the one-line message.
    sys.stderr.flush()
    saved = os.dup(2)
    try:
        with open(os.devnull, "wb") as null:
            os.dup2(null.fileno(), 2)
        refusal = lint_common.require_own_git_dir(REPO_ROOT)
    finally:
        os.dup2(saved, 2)
        os.close(saved)
    return None if refusal is None else _LAYOUT_REFUSED


def _read_origin() -> "tuple[int, bytes, bytes]":
    """The raw origin read, as bytes, with nothing stripped or translated."""
    p = subprocess.run(["git", "-C", str(REPO_ROOT), "remote", "get-url", "origin"],
                       capture_output=True, stdin=subprocess.DEVNULL, timeout=10)
    return p.returncode, p.stdout, p.stderr


_UNREADABLE_TYPE_NAME = "an exception whose type name could not be read"


def _type_name(exc: BaseException) -> str:
    """``exc``'s type name for the diagnostic, read without running code that the exception's class
    or metaclass defines (3b796 round 7). ``type(exc).__name__`` goes through the metaclass, whose
    ``__name__`` (a property, say) can raise, a SystemExit included, inside an ``except`` body,
    where no clause of that ``try`` catches it. ``type`` with one argument and type's own
    ``__name__`` descriptor run no such code, and ``str.__str__`` turns a str subclass stored as the
    name into an exact str, so the f-string that formats it and ``_one_line``, which escapes it with
    the rest of the cause, run none either. Any exception all the same, KeyboardInterrupt aside,
    gives ``_UNREADABLE_TYPE_NAME``. Since round 8 the exceptions named here come from this tool's
    own process only, never from the detector; the name is still escaped, not trusted."""
    try:
        return str.__str__(type.__dict__["__name__"].__get__(type(exc)))
    except KeyboardInterrupt:
        raise
    except BaseException:  # noqa: BLE001 (deliberate: reading the name never ends --check)
        return _UNREADABLE_TYPE_NAME


# 3b796 round 8: tools/detect-env.py runs in a separate process, never in this one. This fixed
# program is all the child runs besides the detector itself: it loads the detector by the path
# given as its one argument, as tools/ref-holds.py ``_operator_is_adopter`` loads it (the file is
# hyphenated), and prints the three values the decision needs as one JSON object on one line.
# The detector's --json profile is not used: it carries no maintainer owner/repo, and it probes gh
# and the network.
_DETECTOR_PROGRAM = (
    "import importlib.util, json, sys\n"
    "spec = importlib.util.spec_from_file_location('detect_env', sys.argv[1])\n"
    "mod = importlib.util.module_from_spec(spec)\n"
    "spec.loader.exec_module(mod)\n"
    "identity = mod.probe_identity(mod.probe_siblings())\n"
    "sys.stdout.buffer.write((json.dumps({\n"
    "    'maintainer_owner_repo': mod.MAINTAINER_ORIGIN_OWNER_REPO,\n"
    "    'origin_url': identity['origin_url'],\n"
    "    'origin_is_maintainer_repo': identity['origin_is_maintainer_repo'],\n"
    "}, sort_keys=True) + '\\n').encode('ascii'))\n"
    "sys.stdout.buffer.flush()\n"
)
# 3b796 round 9: the line goes out as ASCII bytes through sys.stdout.buffer, below the text
# layer, so a platform whose text stdout translates newlines cannot add a CR to it (json.dumps
# escapes every non-ASCII character, so the encoding cannot fail).
# The keys the child must print, each with the exact types its value may have.
_DETECTOR_VALUE_TYPES = {
    "maintainer_owner_repo": (str,),
    "origin_url": (str, type(None)),
    "origin_is_maintainer_repo": (bool,),
}
# Seconds the child may take. The detector's own git reads have a 10-second limit each, and it
# makes at most three on this path (the origin and one per present sibling).
_DETECTOR_TIMEOUT = 60
# Seconds between looks for the child's exit once both of its pipes have closed.
_DETECTOR_POLL = 0.01
# Seconds _stop_detector waits for a reader thread (platforms other than POSIX) to end once the
# child is killed; a pipe whose reader is still running then is left open, not closed under it.
_DETECTOR_READER_GRACE = 1
# 3b796 round 12 (claude N3): seconds _stop_detector's reap waits when neither kill returned (each
# raised, an interrupt included), so a child no kill reached cannot block the cleanup; it is then
# left unreaped, a residual the module docstring lists.
_DETECTOR_UNKILLED_REAP = 1
# 3b796 round 9: whether this platform can see that the child has exited without reaping it
# (os.waitid with WEXITED, WNOHANG and WNOWAIT leaves it a zombie). Its pid, and with it its
# process group id, then stays pinned until _stop_detector has killed the group.
_WAITS_WITHOUT_REAPING = os.name == "posix" and all(
    hasattr(os, name) for name in ("waitid", "P_PID", "WEXITED", "WNOHANG", "WNOWAIT"))
# 3b796 round 10: the fixed causes when SIGCHLD cannot be held at its default disposition for the
# check's subprocess work, so nothing is run (see _operator_context; round 11 widened the hold
# from the detector to every git read and child on this path, and these causes are unchanged).
_SIGCHLD_OFF_MAIN_THREAD = ("SIGCHLD cannot be held at its default disposition off the main "
                            "thread, so tools/detect-env.py was not run")
_SIGCHLD_UNREADABLE = ("the SIGCHLD disposition could not be read, so tools/detect-env.py was "
                       "not run")
_SIGCHLD_UNSETTABLE = ("SIGCHLD could not be set to its default disposition, so "
                       "tools/detect-env.py was not run")
# 3b796 round 11: the fixed cause, before the exception's type name, when the caller's SIGCHLD
# disposition could not be put back after the hold.
_SIGCHLD_NOT_RESTORED = "the caller's SIGCHLD disposition could not be put back"


def _detector_exited(child: subprocess.Popen) -> bool:
    """Whether the detector child has exited, seen without reaping it (``WNOWAIT``)."""
    info = os.waitid(os.P_PID, child.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
    return info is not None and info.si_pid == child.pid


def _collect_detector(child: subprocess.Popen, timeout: float,
                      readers: list) -> "tuple[bytes, bytes] | None":
    """Read the detector child's stdout and stderr to their ends and wait for the child to exit,
    within ``timeout`` seconds, without ``Popen.communicate`` (3b796 round 9); return (stdout,
    stderr), or None when the time limit passes first. Both pipes must reach their ends and the
    child must exit: output still held open by a descendant keeps the read going until the time
    limit. On POSIX one selector reads both pipes, and where ``_WAITS_WITHOUT_REAPING`` holds the
    exit is seen without reaping the child, so the child is still unreaped, its group id pinned,
    when ``_stop_detector`` runs on every path; elsewhere on POSIX the child is reaped here, but
    only after both pipes have closed. On other platforms two reader threads, each added to
    ``readers`` with its pipe for ``_stop_detector``, read the pipes, and the child is reaped here
    after both end."""
    deadline = time.monotonic() + timeout
    if os.name != "posix":
        return _collect_with_threads(child, deadline, readers)
    out_fd, err_fd = child.stdout.fileno(), child.stderr.fileno()
    chunks: "dict[int, list[bytes]]" = {out_fd: [], err_fd: []}
    with selectors.DefaultSelector() as selector:
        for fd in chunks:
            selector.register(fd, selectors.EVENT_READ)
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return None
            for key, _events in selector.select(remaining):
                data = os.read(key.fd, 65536)
                if data:
                    chunks[key.fd].append(data)
                else:
                    selector.unregister(key.fd)
    if _WAITS_WITHOUT_REAPING:
        while not _detector_exited(child):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return None
            time.sleep(min(remaining, _DETECTOR_POLL))
    else:
        try:
            child.wait(max(deadline - time.monotonic(), 0))
        except subprocess.TimeoutExpired:
            return None
    return b"".join(chunks[out_fd]), b"".join(chunks[err_fd])


def _collect_with_threads(child: subprocess.Popen, deadline: float,
                          readers: list) -> "tuple[bytes, bytes] | None":
    """``_collect_detector`` on a platform other than POSIX, whose pipes a selector cannot wait
    on: one reader thread per pipe, then the child is reaped (there is no process group to pin).
    A reader is added to ``readers`` only once it has started (3b796 round 10), so a reader whose
    start raised is never joined, and its pipe, which no thread reads, is closed (an interrupt
    inside ``start`` after the thread has begun is the one case where a running reader goes
    unrecorded, and its pipe is then closed under it)."""
    chunks: "dict[str, bytes]" = {}

    def drain(name: str, pipe) -> None:
        chunks[name] = pipe.read()
    for name, pipe in (("stdout", child.stdout), ("stderr", child.stderr)):
        reader = threading.Thread(target=drain, args=(name, pipe), daemon=True)
        reader.start()
        readers.append((pipe, reader))
    for _pipe, reader in readers:
        reader.join(max(deadline - time.monotonic(), 0))
        if reader.is_alive():
            return None
    try:
        child.wait(max(deadline - time.monotonic(), 0))
    except subprocess.TimeoutExpired:
        return None
    return chunks["stdout"], chunks["stderr"]


def _stop_detector(child: subprocess.Popen, readers: list,
                   in_flight: "BaseException | None" = None) -> None:
    """End the detector child on every path, a normal finish included, then reap it (3b796 round
    9). While the child is unreaped (its returncode is None), its pid pins its process group id
    (``start_new_session`` made it the leader of its own group), so the kill cannot reach another
    group: the group is killed first, with every process left in it (a descendant still running
    after a normal finish included), and then the child itself, so a group kill that fails (or a
    platform with no process groups) still ends it. Then the pipes are closed unread, so a
    descendant that left the group and holds them cannot block the reap, and the child is reaped.
    A child ``_collect_detector`` has already reaped (only where ``_WAITS_WITHOUT_REAPING`` does
    not hold, after both pipes closed) no longer pins a group id, so no kill is sent to it. A pipe
    whose reader thread has not been seen to end within ``_DETECTOR_READER_GRACE`` seconds of the
    kill is left open rather than closed under the thread reading it: each pipe with a reader
    counts as held until its reader is seen to end (3b796 round 10). Since 3b796 round 11 every
    step is independent: the group kill, the child kill, each reader's join, each pipe close and
    the reap run in that order, each even when an earlier one raised, and once the reap has been
    attempted the first exception goes on (the first KeyboardInterrupt, when one was raised, so an
    interrupt is never replaced by a later failure). Since round 12 ``in_flight``, the exception
    already on its way from starting or waiting for the child (None when there is none), counts as
    the first, so an interrupt while waiting goes on whatever a cleanup step then raises (claude
    W1, codex W1); the group kill passes over only a group that is already gone (ESRCH), and any
    other failure of it is recorded like the other steps' (codex W2); and when neither kill
    returned (each raised), the reap waits at most ``_DETECTOR_UNKILLED_REAP`` seconds, so a child
    no kill reached cannot block the cleanup, and is left unreaped, still running, once that
    passes (claude N3). A step that raises does only what it did before raising: a reap that fails
    leaves the child unreaped (a residual the module docstring lists), and the caller restores
    SIGCHLD only after this returns or raises."""
    held = {id(pipe) for pipe, _reader in readers}
    steps = []
    killed = []
    kills_sent = child.returncode is None
    if kills_sent:
        killpg = getattr(os, "killpg", None)

        def kill_group() -> None:
            try:
                killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                return
            killed.append("group")

        def kill_child() -> None:
            # Popen.kill polls first, which can reap the child; the group kill has been sent by
            # then.
            child.kill()
            killed.append("child")
        if killpg is not None:
            steps.append(kill_group)
        steps.append(kill_child)

    def join(pipe, reader) -> None:
        reader.join(_DETECTOR_READER_GRACE)
        if not reader.is_alive():
            held.discard(id(pipe))

    def close(pipe) -> None:
        if pipe is not None and id(pipe) not in held:
            pipe.close()
    steps += [lambda pipe=pipe, reader=reader: join(pipe, reader) for pipe, reader in readers]
    steps += [lambda pipe=pipe: close(pipe) for pipe in (child.stdout, child.stderr)]

    def reap() -> None:
        if kills_sent and not killed:
            child.wait(_DETECTOR_UNKILLED_REAP)
        else:
            child.wait()
    steps.append(reap)
    raised = []
    for step in steps:
        try:
            step()
        except BaseException as exc:  # noqa: BLE001 (deliberate: every later step still runs)
            raised.append(exc)
    if raised:
        first = raised if in_flight is None else [in_flight, *raised]
        raise next((exc for exc in first if isinstance(exc, KeyboardInterrupt)), first[0])


def _detector_fault(returncode: int, stdout: bytes, stderr: bytes) -> "str | None":
    """PURE: which check the detector child's result fails, as fixed text that carries no part of
    its output, else None. In order: exit status 0 (a negative status is the signal that ended it),
    nothing on stderr, stdout valid UTF-8, exactly one line ending in one LF with no other LF or CR,
    that line valid JSON, a JSON object, with exactly the keys of ``_DETECTOR_VALUE_TYPES``, each
    value of one of its exact types, and the line exactly as ``_DETECTOR_PROGRAM`` writes those
    values (so no added whitespace, repeated key or other key order). Nothing on stderr is
    tolerated: the program and the detector's git reads, which capture git's output, write none,
    so any stderr text means something ran that the decision did not expect."""
    if returncode < 0:
        return f"tools/detect-env.py was ended by signal {-returncode}"
    if returncode != 0:
        return f"tools/detect-env.py exited {returncode}"
    if stderr:
        return "tools/detect-env.py wrote to stderr"
    try:
        text = stdout.decode("utf-8")
    except UnicodeDecodeError:
        return "tools/detect-env.py printed output that is not valid UTF-8"
    line = text[:-1] if text.endswith("\n") else None
    if not line or "\n" in line or "\r" in line:
        return "tools/detect-env.py did not print exactly one line"
    try:
        values = json.loads(line)
    except (ValueError, RecursionError):
        return "tools/detect-env.py printed a line that is not valid JSON"
    if type(values) is not dict:
        return "tools/detect-env.py printed JSON that is not an object"
    if set(values) != set(_DETECTOR_VALUE_TYPES):
        return "tools/detect-env.py printed a JSON object without exactly the expected keys"
    if any(type(values[key]) not in types for key, types in _DETECTOR_VALUE_TYPES.items()):
        return "tools/detect-env.py printed a value of the wrong type"
    if json.dumps(values, sort_keys=True) != line:
        return "tools/detect-env.py printed the JSON object in a form the program does not write"
    return None


def _detector_values() -> "tuple[dict | None, str | None]":
    """Run tools/detect-env.py in a separate, isolated process and return (values, None) for a
    result that passes every ``_detector_fault`` check, else (None, the failed check). The child is
    ``sys.executable -I`` (isolated mode: no PYTHON* variables, no script or current directory on
    its path) running ``_DETECTOR_PROGRAM`` with this tool's own tools/detect-env.py as its one
    argument, the checkout as its working directory, stdin from the null device, this process's
    environment without any variable whose name begins with GIT_ (git still finds the same PATH
    and HOME as this tool's own origin read), and a new session, so its process group can be
    killed whole. Its stdout and stderr are captured as bytes by ``_collect_detector`` and never
    printed. A run that takes longer than ``_DETECTOR_TIMEOUT`` seconds (read when the child
    starts, so a test can shorten it) is a failed check. Whatever happens, ``_stop_detector`` then
    kills the child's process group, closes the pipes and reaps the child (3b796 round 9).
    The caller, ``_operator_context``, holds SIGCHLD at its default disposition around this whole
    call, so the child is reaped before the caller's disposition is put back (3b796 round 11;
    round 10 held it here, around the detector only)."""
    timeout = _DETECTOR_TIMEOUT
    detector = Path(__file__).resolve().parent / "detect-env.py"
    env = {name: value for name, value in os.environ.items()
           if not name.upper().startswith("GIT_")}
    child = None
    readers: list = []
    in_flight = None
    try:
        child = subprocess.Popen([sys.executable, "-I", "-c", _DETECTOR_PROGRAM, str(detector)],
                                 cwd=str(REPO_ROOT), env=env, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 start_new_session=True)
        output = _collect_detector(child, timeout, readers)
    except BaseException as exc:
        # 3b796 round 12 (claude W1, codex W1): recorded and re-raised unchanged, so the cleanup
        # below counts it as the first exception and a cleanup step that then fails cannot
        # replace it (an interrupt while waiting stays an interrupt).
        in_flight = exc
        raise
    finally:
        # 3b796 round 9: every path ends the child here, a normal finish, the time limit, an
        # interrupt and any other exception alike. _collect_detector never reaps the child where
        # _WAITS_WITHOUT_REAPING holds, so its pid still pins its process group id while
        # _stop_detector kills the group, closes the pipes and reaps it, even when the child has
        # already exited and a descendant in its group still holds the pipes. The Popen call is
        # inside this try, so an interrupt once child is bound still ends the child; one that
        # lands inside Popen itself, after the fork and before child is bound, leaves it running,
        # and any interrupt that lands during this cleanup can cut short the step it lands in
        # (residuals the module docstring lists). Round 11: _operator_context puts the caller's
        # SIGCHLD disposition back only after this, so only after the reap was attempted.
        if child is not None:
            _stop_detector(child, readers, in_flight)
    if output is None:
        return None, f"tools/detect-env.py did not finish within {timeout} seconds"
    stdout, stderr = output
    fault = _detector_fault(child.returncode, stdout, stderr)
    if fault is not None:
        return None, fault
    return json.loads(stdout.decode("utf-8")), None


def _operator_context() -> "tuple[str, str | None]":
    """The operator context and, when it is "undecidable", why, as one line (else None): refused
    redirects first, then this tool's own raw origin read, then tools/detect-env.py, run by
    ``_detector_values`` in a separate, isolated process, whose maintainer owner/repo places that
    origin and which must read the same origin. Trust boundary (3b796 round 8): nothing the
    detector raises, defines or changes in its own process (an exception of any class, a class
    with any MRO or metaclass, a SystemExit, os._exit, atexit handlers, a signal that ends it,
    changed builtins) can reach this process; the tool reads only the child's exit status and
    output, prints none of that output, and trusts only output that passes every
    ``_detector_fault`` check. Any other
    result (a timeout, a signal, a non-zero exit, stderr text, output that is not exactly the one
    expected JSON object) is "undecidable" with a fixed cause naming the check that failed, and so
    is SIGCHLD that cannot be held at its default disposition for this function's subprocess work
    (off the main thread, or a disposition that cannot be read or set; 3b796 round 10), with
    nothing run, and a caller's disposition that cannot be put back after (3b796 round 11). The
    hold covers every git read and child here, the repository check's, the origin read's and the
    detector's, so each sees its child's real exit status (3b796 round 11: under an inherited
    ignored SIGCHLD, Python's subprocess reports a git exit as 0). Placing the origin and the
    agreement check then run here, on those validated plain
    values only. This tool's own parts (the repository check and the origin read; starting the child and
    waiting for it; placing the origin) keep their handlers: any exception there, a SystemExit
    included, is "undecidable" with the part that failed and the type name ``_type_name`` reads,
    and only KeyboardInterrupt passes through (an interrupt while waiting kills the child's
    process group and reaps the child first, and still goes on when a cleanup step then fails;
    3b796 round 12). Residuals: a detector that prints valid but wrong
    values is trusted, as an edit to the checkout's own code would be (the child runs as the same
    user, so the process boundary is not a sandbox: detector code acting outside its own process,
    by signalling this one or writing files, is that same edit); the child's resources are not
    limited beyond the time limit (its output is read in full, and a descendant it leaves running
    is stopped only inside its process group, on every path where ``_WAITS_WITHOUT_REAPING``
    holds); and the cleanup, interrupt and SIGCHLD residuals the module docstring lists. Git
    configuration both reads share (the repository's config, the HOME and XDG global files, the
    system file) changes both reads alike, so a rewrite there that turns a maintainer origin into
    a fork URL still takes the no-op; configuration this process's ``GIT_`` variables supply
    (``GIT_CONFIG_COUNT`` and its pairs, ``GIT_CONFIG_PARAMETERS`` from ``git -c``,
    ``GIT_CONFIG_GLOBAL``, ``GIT_CONFIG_SYSTEM``, ``GIT_CONFIG_NOSYSTEM``, and ``safe.directory``
    supplied that way) reaches only this tool's read, so a difference it makes to the origin
    makes the two reads disagree: "undecidable", exit 4. Only reached by --check on the
    absent-sibling branch."""
    sigchld = getattr(signal, "SIGCHLD", None)
    if sigchld is None:
        return _context_under_hold()
    # 3b796 rounds 10 and 11, as tools/preflight-changelog.py holds it for its runner: the
    # refusals come before any child runs, the repository check's git reads included.
    if threading.current_thread() is not threading.main_thread():
        return "undecidable", _SIGCHLD_OFF_MAIN_THREAD
    try:
        inherited = signal.getsignal(sigchld)
    except KeyboardInterrupt:
        raise
    except BaseException:  # noqa: BLE001 (deliberate: never ends --check without the line)
        inherited = None
    if inherited is None:
        return "undecidable", _SIGCHLD_UNREADABLE
    # The caller's disposition is recorded BEFORE the swap and the restore below is armed from
    # the swap attempt on, even when the swap raises (round 11, codex W1: a swap that raises may
    # have changed it all the same, and putting back a disposition that was never swapped changes
    # nothing). No return inside this try, so the restore's outcome can still decide the result.
    not_restored = None
    try:
        try:
            signal.signal(sigchld, signal.SIG_DFL)
        except KeyboardInterrupt:
            raise
        except BaseException:  # noqa: BLE001 (deliberate: never ends --check without the line)
            result = ("undecidable", _SIGCHLD_UNSETTABLE)
        else:
            # Returns or raises only after _detector_values has attempted the reap.
            result = _context_under_hold()
    finally:
        try:
            signal.signal(sigchld, inherited)
        except KeyboardInterrupt:
            raise
        except BaseException as exc:  # noqa: BLE001 (deliberate: never ends --check without the
            # line; an exception already on its way, an interrupt included, still goes on)
            not_restored = _type_name(exc)
    # Round 12 (claude N1): a restore that fails gives its own cause on every path, after a swap
    # that raised as well, since SIGCHLD may then be left at its default.
    if not_restored is not None:
        return "undecidable", f"{_SIGCHLD_NOT_RESTORED} ({not_restored})"
    return result


def _context_under_hold() -> "tuple[str, str | None]":
    """``_operator_context``'s work once SIGCHLD is held at its default disposition (3b796 round
    11): the repository check, the origin read, the detector, then placing the origin."""
    try:
        redirect = _repository_redirect()
        if redirect is not None:
            return "undecidable", redirect
        read = _read_origin()
        fault = _origin_read_fault(*read)
        if fault is not None:
            return "undecidable", f"the origin read failed validation ({fault})"
        origin = _origin_from_read(*read)
    except KeyboardInterrupt:
        raise
    except BaseException as exc:  # noqa: BLE001 (deliberate: a failure, a SystemExit included, is
        # never an adopter and never ends --check without the line)
        return "undecidable", ("the repository check or the origin read failed "
                               f"({_type_name(exc)})")
    try:
        values, fault = _detector_values()
    except KeyboardInterrupt:
        raise
    except BaseException as exc:  # noqa: BLE001 (deliberate: this tool failing to start or wait
        # for the child, a SystemExit included, is never an adopter and never ends --check
        # without the line)
        return "undecidable", f"tools/detect-env.py could not be run ({_type_name(exc)})"
    if fault is not None:
        return "undecidable", fault
    maintainer = values["maintainer_owner_repo"]
    identity = {"origin_url": values["origin_url"],
                "origin_is_maintainer_repo": values["origin_is_maintainer_repo"]}
    try:
        if _place_origin(origin, maintainer) is None:
            return "undecidable", _unplaced_reason(origin)
        context = _context_from_identity(identity, origin, maintainer)
    except KeyboardInterrupt:
        raise
    except BaseException as exc:  # noqa: BLE001 (deliberate: a failure, a SystemExit included, is
        # never an adopter and never ends --check without the line)
        # The inputs are the validated origin and the detector's validated plain values, so only
        # this tool's own code can raise here.
        return "undecidable", ("the origin could not be placed with what tools/detect-env.py gave "
                               f"({_type_name(exc)})")
    if context == "undecidable":
        return context, "tools/detect-env.py did not read the same origin and maintainer flag"
    return context, None


def _one_line(text: str) -> str:
    """PURE: ``text`` for display with each control character (Unicode category Cc: LF, CR, NEL and
    every other separator str.splitlines splits on except U+2028 and U+2029) and U+2028 and U+2029
    written as its repr escape (``\\n``, ``\\r``, ``\\x85``, ``\\u2028``), and every other character
    kept, so a value carrying a line break cannot split the one-line diagnostic. The display is not
    reversible, by choice: a backslash is not escaped, so an escaped control character and the same
    literal backslash sequence in a name (an LF and a backslash followed by n) display the same,
    and format characters (Unicode category Cf, such as U+202E and U+200B) pass through unchanged.
    Neither can split the line, which is all the display has to keep, and leaving backslashes
    alone keeps each backslash in a Windows path single rather than doubling it."""
    return "".join(repr(c)[1:-1] if unicodedata.category(c) in ("Cc", "Zl", "Zp") else c
                   for c in text)


def _check_without_sibling() -> int:
    """--check with the sibling absent (3b796): adopter no-op, else cannot evaluate."""
    context, reason = _operator_context()
    if context == "adopter":
        print("build-reference-manifest --check: grc_library_ref not present; no-op, did not check "
              "for drift (adopter clone: the committed manifest ships statically for adopters).")
        return 0
    missing = _one_line(str(lint_common.REPO_ROOT.parent / "grc_library_ref"))
    where = "a clone whose origin is the maintainer repository" if context == "maintainer" else (
        f"a context the origin check cannot decide ({_one_line(reason or 'no reason given')}), "
        f"which is not taken as an adopter clone")
    print(f"build-reference-manifest --check: CANNOT EVALUATE, the grc_library_ref sibling is "
          f"missing (expected at {missing}) in {where}; nothing was checked.", file=sys.stderr)
    return EXIT_CANNOT_EVALUATE


def main() -> int:
    # 3b50b2a: parse strictly first, so a mistyped --check can never fall through to the WRITE
    # below (and is refused even in an adopter clone, before the no-op branch).
    check = "--check" in lint_common.strict_flags(sys.argv[1:], ("--check",))
    try:
        # Strict (3b74): only an ABSENT sibling takes the no-op; a present but unusable one refuses.
        ref = lint_common.resolve_sibling("ref", strict=True)
    except lint_common.InaccessiblePath as exc:
        print(f"build-reference-manifest: the grc_library_ref sibling is present but unusable "
              f"({exc}); refusing the no-op an absent sibling takes.", file=sys.stderr)
        return 2
    if ref is None:
        if check:
            return _check_without_sibling()
        # Regenerate with no reference sibling: no-op (exit 0); the committed manifest is used
        # as-is. (Maintainer-side absence is caught loud at /orch, and by --check above.)
        note = ("build-reference-manifest: grc_library_ref not present; "
                "no-op (the committed manifest ships statically for adopters).")
        print(note)
        return 0
    catalogue_path = ref / "catalogue.yml"
    # 3b677: strict_kind, not Path.is_file, which reads a catalogue in an unsearchable sibling
    # as absent (3.12+) or raises PermissionError (3.11). Only ENOENT is "not found".
    try:
        kind = lint_common.strict_kind(catalogue_path)
        if kind == "file":
            text = catalogue_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"build-reference-manifest: the grc_library_ref sibling is present but unusable "
              f"(cannot read {exc.filename or catalogue_path}: {exc.strerror}).", file=sys.stderr)
        return 2
    except UnicodeDecodeError as exc:
        # 3b677: a catalogue that is not valid UTF-8 exits 2 naming it, not exit 3 with a traceback.
        print(f"build-reference-manifest: the grc_library_ref sibling is present but unusable "
              f"(cannot decode {catalogue_path} as UTF-8: {exc.reason} at byte {exc.start}).",
              file=sys.stderr)
        return 2
    if kind is None:
        print(f"build-reference-manifest: {catalogue_path} not found", file=sys.stderr)
        return 2
    if kind != "file":
        print(f"build-reference-manifest: the grc_library_ref sibling is present but unusable "
              f"({catalogue_path} is present but is not a regular file).", file=sys.stderr)
        return 2
    catalogue = _parse_catalogue(text)
    rendered = render(catalogue)
    if check:
        current = MANIFEST.read_text(encoding="utf-8") if MANIFEST.exists() else ""
        if current != rendered:
            print("build-reference-manifest --check: DRIFT, the committed manifest is out of "
                  "date with grc_library_ref's catalogue. Run "
                  "`python3 tools/build-reference-manifest.py` and commit.", file=sys.stderr)
            return 1
        print("build-reference-manifest --check: OK (manifest in sync with the reference base).")
        return 0
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(rendered, encoding="utf-8")
    print(f"build-reference-manifest: wrote {MANIFEST} ({rendered.count(chr(10))} lines).")
    return 0


if __name__ == "__main__":
    # Exit codes: 0 in sync, written, no sibling when regenerating, or no sibling on --check in a
    # positively placed adopter clone (which says it did not check; see the docstring for the
    # rule and its residual); 1 --check DRIFT only; 2 catalogue missing, a present but unusable
    # sibling or catalogue (including one not valid UTF-8), or a bad flag; 3 an unexpected internal
    # error; 4 --check cannot evaluate (no sibling in a clone whose origin is the maintainer
    # repository, or in any context that cannot be decided, 3b796). Python's own uncaught-exception
    # exit is 1, the same as DRIFT, so an unexpected error is mapped to 3 to keep 1 meaning drift
    # (P-TODO 3b62: the pre-push guard reports drift from this code and must not misreport a crash
    # as drift).
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 (deliberate: any unexpected failure becomes exit 3)
        import traceback
        traceback.print_exc()
        print(f"build-reference-manifest: internal error ({type(exc).__name__}); exit 3",
              file=sys.stderr)
        sys.exit(3)
