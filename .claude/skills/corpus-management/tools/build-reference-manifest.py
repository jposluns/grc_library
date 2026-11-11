#!/usr/bin/env python3
"""Generate the public reference-acquisition manifest.

The manifest [`.claude/skills/corpus-management/registers/reference-acquisition-manifest.md`] is a PUBLIC BIBLIOGRAPHY of the
corpus's citation-source reference base: for each trusted-bucket entry in
`grc_library_ref/catalogue.yml` (standards / frameworks / legislation / programs) it lists
the title, version/edition, bucket, upstream URL, and acquisition class (free|licensed),
with the held source TEXT stripped. An adopter's `/adopt` uses it to bootstrap a `.ref`:
FREE sources are web-fetched, LICENSED sources are listed for manual acquisition. The
catalogue's internal acquisition-provenance notes in `checked_edition` are written in public
wording (`PUBLIC_WORDING`), so the public file names no internal role.

**Copyright guardrail:** this reads ONLY catalogue bibliographic metadata (`title`,
`origin`/`body`/`jurisdiction`, `checked_edition`, `upstream_url`, `bucket`, `acquisition`);
it NEVER reads the held `--full-text` files nor the catalogue `notes`/`extract` fields, and
never reproduces source prose. The manifest is a bibliography, never the texts.

**Sibling-independence:** this is a maintainer tool. It locates the real
`grc_library_ref` sibling via `lint_common.resolve_sibling("ref", strict=True)`. With that
sibling absent, regenerating NO-OPS (exit 0) in every context, for an adopter's portable clone.
`--check` with it absent never reports a success it did not earn. It keeps the explicit
static-ship no-op (exit 0, saying it did not check) only in a positively placed adopter clone,
decided from repository-local evidence alone (no separate identity probe is run, and the
maintainer repository is declared in this tool as `MAINTAINER_ORIGIN_OWNER_REPO`), when all of
these hold: no repository-redirecting variable is set (GIT_DIR, GIT_WORK_TREE, or one of
`lint_common._GIT_REDIRECT_VARIABLES`), whatever it names, so an adopter whose git exports GIT_DIR
to a linked worktree's hooks sees exit 4 too; `lint_common.require_own_git_dir` confirms git reads
this checkout's own repository; `git remote get-url origin` exits 0, prints nothing on stderr and
prints exactly one line, the value and one LF, with no other LF or CR in it; a second read of the
origin, run with every `GIT_` variable removed from its environment, passes the same validation
and gives the identical value; and that value is an `https://`, `http://` or `ssh://` URL or a
`user@host:owner/repo` form whose path is exactly `owner/repo` (an optional `.git` or trailing
slash aside) and is not the maintainer's `jposluns/grc_library` on any host. `adopt-preflight-guard.py`
classifies through the same `_operator_context`. The degrade path: a clone whose origin is the
maintainer repository on `github.com` exits 4 (cannot evaluate) with one line naming the missing
sibling, and so does every context the check cannot decide (a local-path, `file://`, `git://`,
userless `host:path` or otherwise unplaced origin, an SSH host alias or other host serving
`jposluns/grc_library`, no readable `origin`, a garbled read, or two reads that disagree), which
is never read as adopter; there the line also gives the cause, in fixed wording that may carry a
redirect variable's name, git's exit code or an exception's type name, and never any part of the
origin, of a refusal or of a command line: the redirect variable set (its name only);
`require_own_git_dir` not confirming that git reads this checkout's own repository, through the
layout or the environment (that category only, for every refusal: its refusal text is withheld,
because it can carry paths taken from the environment, and `_repository_redirect` says how to
print it); either origin read's validation failure (with git's exit code when it is not 0); an
origin in no form the check places; the maintainer repository on a host other than `github.com`;
the two reads disagreeing; or, for an unexpected exception in this tool's own process, the part
that failed (the repository check or the origin reads, or placing the origin) and the exception's
type name, read without running code the exception's class or metaclass defines (a fixed text
when it cannot be read).
SIGCHLD is held at its default disposition around all of this tool's subprocess work on this path,
from before the repository check's first git read until the second origin read has finished, and
the caller's disposition is put back after, on every path: with SIGCHLD ignored the kernel reaps
each child itself, so Python's subprocess reports a git read's exit status as 0 whatever git
exited with. Off the main thread, or where the disposition cannot be read or set, nothing is run,
not even the repository check, and the line gives that fixed cause; when setting it raises, the
caller's disposition is still put back, and the cause stays the fixed one unless putting it back
raises too, which gives the could-not-be-put-back cause instead. A platform without SIGCHLD has
nothing to hold. Placing the origin and the agreement check run in this process on the two
validated values. An exception in this tool's own parts, a SystemExit included, gives that line
too; only KeyboardInterrupt passes through.
Residuals: an interrupt that lands at the instant the caller's SIGCHLD disposition is put back
leaves SIGCHLD at its default, and so does a failure to put it back, which gives its own fixed
cause naming the exception's type, also when setting it had raised first; the hold is
process-wide, so a child another thread of the caller ends during it is not reaped automatically,
and a git read or child another thread starts then sees SIGCHLD at its default; for in-process
embedding only (the command line is a fresh process, where only the default and ignored
dispositions survive the exec and both are read exactly, as
.claude/skills/corpus-management/tools/preflight-changelog.py states for its own hold):
`signal.getsignal` gives Python's own record, so a SIGCHLD handler that native code installs
after interpreter startup, outside the signal module, reads as that stale record and is put back
as it, replacing the native handler (one installed before startup reads as unreadable, and
nothing is run).
Control characters, U+2028 and U+2029 in the displayed sibling path are written as escapes, so
the diagnostic stays one line whatever its parent directory is named. Known residual: git
configuration that both reads share (the repository's own config, the global files under HOME and
XDG_CONFIG_HOME, and the system file), such as a `url.<base>.insteadOf` rewrite or a
`remote.origin.url`, changes what `git remote get-url` prints in both reads alike, so a maintainer
clone whose printed origin becomes a fork URL that way still takes the no-op, as do the layouts
`require_own_git_dir` lists as its own residuals. Configuration this tool's `GIT_` variables
supply (`GIT_CONFIG_COUNT` and its `GIT_CONFIG_KEY_<n>` and `GIT_CONFIG_VALUE_<n>` pairs,
`GIT_CONFIG_PARAMETERS` from `git -c`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`,
`GIT_CONFIG_NOSYSTEM`, and a `safe.directory` supplied that way) reaches the first read only, since
the second read gets no `GIT_` variable: a difference it makes to the origin makes the two reads
disagree, and `--check` exits 4 with the disagreement cause. A sibling that is
present but unusable (not a directory, a dangling link, or one that cannot be examined) is not
absent: it fails with exit 2 naming it, as does a `catalogue.yml` in it that cannot be examined,
is not a regular file, cannot be read or is not valid UTF-8. A `catalogue.yml` genuinely
absent from a usable sibling exits 2 as not found. The probes use `os.lstat`/`os.stat`, so the
verdict is the same on Python 3.11 and 3.12+. It is NEVER a CI gate, and
`check-portability.sh`, which runs the regenerate path, stays green. `--check` only refuses to
pass without having checked. The committed manifest ships statically, so an adopter gets it
without any sibling.

Usage:
  python3 .claude/skills/corpus-management/tools/build-reference-manifest.py            # regenerate the committed manifest
  python3 .claude/skills/corpus-management/tools/build-reference-manifest.py --check    # drift check (exit 1 if out of date, 4 if
                                                       # it cannot be evaluated)

`--check` is an orchestrator/maintainer drift check (it reads `_ref`), NOT a CI gate; run it
at `_ref`-update / resume, folded into the resync-`_ref` discipline.
"""
import os
import re
import signal
import subprocess
import sys
import threading
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_common  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[4]
MANIFEST = (REPO_ROOT / ".claude" / "skills" / "corpus-management" / "registers"
            / "reference-acquisition-manifest.md")
TRUSTED = ("standards", "frameworks", "legislation", "programs")
# Generator schema version: bump on a change to what this generator writes (the manifest's
# SHAPE, columns or header, or the PUBLIC_WORDING it applies), recorded in
# .working/CHANGELOG.md. Not the library CalVer, and not the row contents (which advance
# with the reference base). The manifest is exempt from the date/version-staleness gates
# (like governance/portal.md), so this stays stable across content regens; the Date below
# is the reference base's own max currency. 1.0.1: PUBLIC_WORDING added.
SCHEMA_VERSION = "1.0.1"
FALLBACK_DATE = "2026-07-17"
BUCKET_LABEL = {
    "standards": "Standards",
    "frameworks": "Frameworks",
    "legislation": "Legislation",
    "programs": "Programs",
}
# The public wording for the catalogue's internal acquisition-provenance notes, applied in this
# order to each Version / edition cell (`checked_edition`, the only rendered field that carries
# them; titles that name workers as data subjects are left alone). Exact literal pairs, each
# taken from a committed manifest row; a provenance phrase not listed here is written as the
# catalogue has it.
PUBLIC_WORDING = (
    ("worker-acquired", "acquired"),
    (" worker acquisition", " acquisition"),
    (", upstream not re-fetched by the orchestrator this cycle",
     "; upstream not re-fetched this cycle"),
    ("orchestrator-confirmed", "confirmed"),
    ("Orchestrator re-fetch blocked", "A re-fetch attempt was blocked"),
)


# The YAML 1.1 double-quoted escape set (the one yaml.safe_load implements), plus the three
# hex forms; \x, \u and \U carry 2, 4 and 8 hex digits.
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
    # int. Without this, an unquoted null reached render() as the literal text "null".
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
    # U+2029, U+0085 and other separators, which would truncate a value that carries one. A raw
    # one inside a quoted value is kept verbatim here, where yaml.safe_load would fold it into a
    # space; the catalogue carries none.
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
    str(v), so an int 0 stays "0" rather than vanishing through an `or ""`."""
    return "" if v is None else str(v)


def _cell(v) -> str:
    """Escape a value for a markdown table cell (pipes; collapse line breaks, including a bare
    carriage return, which would otherwise split the row for any reader)."""
    return _text(v).replace("|", "\\|").replace("\r\n", " ").replace("\r", " ").replace("\n", " ").strip()


def _public(text: str) -> str:
    """``text`` with each PUBLIC_WORDING pair applied, in order."""
    for internal, public in PUBLIC_WORDING:
        text = text.replace(internal, public)
    return text


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
        ("Related Documents", "[`README.md`](../../../../README.md), "
         "[`governance/portal.md`](../../../../governance/portal.md)"),
        ("Classification", "Public"),
        ("Category", "Documentation"),
        ("Review Frequency", "Regenerated from grc_library_ref/catalogue.yml on any "
         "reference-base change; maintainer-side, not a CI gate"),
        ("Repository Path", "[`.claude/skills/corpus-management/registers/reference-acquisition-manifest.md`]"
         "(reference-acquisition-manifest.md)"),
        ("Confidentiality", "Public"),
        ("License", "CC BY-SA 4.0"),
    ]
    lines = [
        "<!--",
        "Auto-generated by .claude/skills/corpus-management/tools/build-reference-manifest.py from "
        "grc_library_ref/catalogue.yml.",
        "Do not edit by hand. Regenerate with "
        "`python3 .claude/skills/corpus-management/tools/build-reference-manifest.py`.",
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
        "**Generated file, do not hand-edit.** Produced by `.claude/skills/corpus-management/tools/build-reference-manifest.py`",
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
            version = _public(_cell(e.get("checked_edition")))
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


# --check with no sibling outside a positively placed adopter clone. Distinct from 1 (DRIFT),
# 2 (an unusable sibling or catalogue, or a bad flag) and 3 (an internal error).
EXIT_CANNOT_EVALUATE = 4


# Variables that point git at another repository's git directory, work tree, common directory,
# objects or history. Any of them set makes the origin read undecidable, whatever it names: the
# read then need not be this checkout's own origin.
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
    and one LF) with no other LF or CR and valid UTF-8, else None. Nothing is stripped or
    translated first, so a leading or trailing line break or CR, an internal one and any trace
    text all refuse the read."""
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
                "build-reference-manifest.py) on a host other than github.com, which the check "
                "does not place")
    return "the origin is not a form the check places as an adopter or maintainer clone"


def _context_from_reads(origin: "str | None", plain: "str | None", maintainer: str) -> str:
    """PURE decision: "maintainer", "adopter" or "undecidable", from the origin
    ``_origin_from_read`` validated in this tool's own read, the origin it validated in the second
    read made with no ``GIT_`` variable (each None when the read was refused) and the maintainer
    owner/repo. Only a positively placed origin that both reads gave identically decides;
    everything else is "undecidable"."""
    if origin is None or plain is None or plain != origin:
        return "undecidable"
    placed = _place_origin(origin, maintainer)
    return placed if placed in ("maintainer", "adopter") else "undecidable"


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
    in the same environment, ``python3 -c "import pathlib, sys; sys.path.insert(0, '.claude/skills/corpus-management/tools');
    import lint_common; print(lint_common.require_own_git_dir(pathlib.Path.cwd()))"``, which
    prints the refusal in full (None when there is none); the delta gates that call it, such as
    .claude/skills/corpus-management/tools/check-stranded-control-code-on-pr.py, print it too."""
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
    or metaclass defines. ``type(exc).__name__`` goes through the metaclass, whose
    ``__name__`` (a property, say) can raise, a SystemExit included, inside an ``except`` body,
    where no clause of that ``try`` catches it. ``type`` with one argument and type's own
    ``__name__`` descriptor run no such code, and ``str.__str__`` turns a str subclass stored as the
    name into an exact str, so the f-string that formats it and ``_one_line``, which escapes it with
    the rest of the cause, run none either. Any exception all the same, KeyboardInterrupt aside,
    gives ``_UNREADABLE_TYPE_NAME``. The exceptions named here come from this tool's own process
    only; the name is still escaped, not trusted."""
    try:
        return str.__str__(type.__dict__["__name__"].__get__(type(exc)))
    except KeyboardInterrupt:
        raise
    except BaseException:  # noqa: BLE001 (deliberate: reading the name never ends --check)
        return _UNREADABLE_TYPE_NAME


# The maintainer repository, declared in this shipped tool; no separate identity probe ships.
# .claude/skills/corpus-management/tools/install-git-hooks.sh and
# .claude/skills/corpus-management/tools/pre-push-hook.py name the same owner/repo.
MAINTAINER_ORIGIN_OWNER_REPO = "jposluns/grc_library"
# The fixed causes when SIGCHLD cannot be held at its default disposition for the check's
# subprocess work, so nothing is run (see _operator_context; the hold covers every git read on
# this path).
_SIGCHLD_OFF_MAIN_THREAD = ("SIGCHLD cannot be held at its default disposition off the main "
                            "thread, so the origin was not read")
_SIGCHLD_UNREADABLE = "the SIGCHLD disposition could not be read, so the origin was not read"
_SIGCHLD_UNSETTABLE = ("SIGCHLD could not be set to its default disposition, so the origin was "
                       "not read")
# The fixed cause, before the exception's type name, when the caller's SIGCHLD disposition could
# not be put back after the hold.
_SIGCHLD_NOT_RESTORED = "the caller's SIGCHLD disposition could not be put back"


def _read_origin_plain() -> "tuple[int, bytes, bytes]":
    """The second raw origin read: the same command as ``_read_origin``, run with every
    variable whose name begins with GIT_ removed from its environment, so configuration those
    variables supply reaches only the first read. Nothing is stripped or translated."""
    env = {name: value for name, value in os.environ.items()
           if not name.upper().startswith("GIT_")}
    p = subprocess.run(["git", "-C", str(REPO_ROOT), "remote", "get-url", "origin"],
                       capture_output=True, stdin=subprocess.DEVNULL, env=env, timeout=10)
    return p.returncode, p.stdout, p.stderr


def _operator_context() -> "tuple[str, str | None]":
    """The operator context and, when it is "undecidable", why, as one line (else None), from
    repository-local evidence only: refused redirects first, then this tool's own raw origin read,
    then a second read with no ``GIT_`` variable that must give the same value, placed against
    ``MAINTAINER_ORIGIN_OWNER_REPO``. SIGCHLD that cannot be held at its default disposition for
    this function's subprocess work (off the main thread, or a disposition that cannot be read or
    set) is "undecidable" with nothing run, and so is a caller's disposition that cannot be put
    back after. The hold covers every git read here, the repository check's and both origin reads,
    so each sees git's real exit status (under an inherited ignored SIGCHLD, Python's subprocess
    reports a git exit as 0). Placing the origin and the agreement check then run on the validated
    values only. Any exception in this tool's parts (the repository check and the origin reads;
    placing the origin), a SystemExit included, is "undecidable" with the part that failed and the
    type name ``_type_name`` reads, and only KeyboardInterrupt passes through. Residuals: git
    configuration both reads share (the repository's config, the HOME and XDG global files, the
    system file) changes both reads alike, so a rewrite there that turns a maintainer origin into
    a fork URL still takes the no-op; configuration this process's ``GIT_`` variables supply
    (``GIT_CONFIG_COUNT`` and its pairs, ``GIT_CONFIG_PARAMETERS`` from ``git -c``,
    ``GIT_CONFIG_GLOBAL``, ``GIT_CONFIG_SYSTEM``, ``GIT_CONFIG_NOSYSTEM``, and ``safe.directory``
    supplied that way) reaches only the first read, so a difference it makes to the origin makes
    the two reads disagree: "undecidable", exit 4; and the SIGCHLD residuals the module docstring
    lists. Reached by --check on the absent-sibling branch, and by adopt-preflight-guard.py."""
    sigchld = getattr(signal, "SIGCHLD", None)
    if sigchld is None:
        return _context_under_hold()
    # As .claude/skills/corpus-management/tools/preflight-changelog.py holds it for its runner, the
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
    # the swap attempt on, even when the swap raises (a swap that raises may have changed it all
    # the same, and putting back a disposition that was never swapped changes nothing). No return
    # inside this try, so the restore's outcome can still decide the result.
    not_restored = None
    try:
        try:
            signal.signal(sigchld, signal.SIG_DFL)
        except KeyboardInterrupt:
            raise
        except BaseException:  # noqa: BLE001 (deliberate: never ends --check without the line)
            result = ("undecidable", _SIGCHLD_UNSETTABLE)
        else:
            # Returns or raises only after both origin reads have finished.
            result = _context_under_hold()
    finally:
        try:
            signal.signal(sigchld, inherited)
        except KeyboardInterrupt:
            raise
        except BaseException as exc:  # noqa: BLE001 (deliberate: never ends --check without the
            # line; an exception already on its way, an interrupt included, still goes on)
            not_restored = _type_name(exc)
    # A restore that fails gives its own cause on every path, after a swap that raised as well,
    # since SIGCHLD may then be left at its default.
    if not_restored is not None:
        return "undecidable", f"{_SIGCHLD_NOT_RESTORED} ({not_restored})"
    return result


def _context_under_hold() -> "tuple[str, str | None]":
    """``_operator_context``'s work once SIGCHLD is held at its default disposition: the
    repository check, the two origin reads, then placing the origin."""
    try:
        redirect = _repository_redirect()
        if redirect is not None:
            return "undecidable", redirect
        read = _read_origin()
        fault = _origin_read_fault(*read)
        if fault is not None:
            return "undecidable", f"the origin read failed validation ({fault})"
        origin = _origin_from_read(*read)
        plain_read = _read_origin_plain()
        fault = _origin_read_fault(*plain_read)
        if fault is not None:
            return "undecidable", ("the origin read without GIT_ variables failed validation "
                                   f"({fault})")
        plain = _origin_from_read(*plain_read)
    except KeyboardInterrupt:
        raise
    except BaseException as exc:  # noqa: BLE001 (deliberate: a failure, a SystemExit included, is
        # never an adopter and never ends --check without the line)
        return "undecidable", ("the repository check or the origin reads failed "
                               f"({_type_name(exc)})")
    try:
        if _place_origin(origin, MAINTAINER_ORIGIN_OWNER_REPO) is None:
            return "undecidable", _unplaced_reason(origin)
        context = _context_from_reads(origin, plain, MAINTAINER_ORIGIN_OWNER_REPO)
    except KeyboardInterrupt:
        raise
    except BaseException as exc:  # noqa: BLE001 (deliberate: a failure, a SystemExit included, is
        # never an adopter and never ends --check without the line)
        return "undecidable", f"the origin could not be placed ({_type_name(exc)})"
    if context == "undecidable":
        return context, "the two origin reads did not give the same value"
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
    """--check with the sibling absent: adopter no-op, else cannot evaluate."""
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
    # Parse strictly first, so a mistyped --check can never fall through to the WRITE below (and
    # is refused even in an adopter clone, before the no-op branch).
    check = "--check" in lint_common.strict_flags(sys.argv[1:], ("--check",))
    try:
        # Strict: only an ABSENT sibling takes the no-op; a present but unusable one refuses.
        ref = lint_common.resolve_sibling("ref", strict=True)
    except lint_common.InaccessiblePath as exc:
        print(f"build-reference-manifest: the grc_library_ref sibling is present but unusable "
              f"({exc}); refusing the no-op an absent sibling takes.", file=sys.stderr)
        return 2
    if ref is None:
        if check:
            return _check_without_sibling()
        # Regenerate with no reference sibling: no-op (exit 0); the committed manifest is used
        # as-is. (Maintainer-side absence is caught loudly in the maintainer's own workflow, and
        # by --check above.)
        note = ("build-reference-manifest: grc_library_ref not present; "
                "no-op (the committed manifest ships statically for adopters).")
        print(note)
        return 0
    catalogue_path = ref / "catalogue.yml"
    # Uses strict_kind, not Path.is_file, which reads a catalogue in an unsearchable sibling
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
        # A catalogue that is not valid UTF-8 exits 2 naming it, not exit 3 with a traceback.
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
                  "`python3 .claude/skills/corpus-management/tools/build-reference-manifest.py` and commit.", file=sys.stderr)
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
    # repository, or in any context that cannot be decided). Python's own uncaught-exception exit
    # is 1, the same as DRIFT, so an unexpected error is mapped to 3 to keep 1 meaning drift (the
    # pre-push guard reports drift from this code and must not misreport a crash as drift).
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
