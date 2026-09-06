#!/usr/bin/env python3
"""Verify the vendored AIQT generic-core module against its pin (digest gate).

The Corpus-Management umbrella vendors a MINIMAL subset of the AIQT guardrails pack
-- ``vendor/aiqt/tools/aiqt_corpus.py`` -- which grc's corpus tools import through
``tools/aiqt_bootstrap.py``. Because it is CONSUMED from AIQT (not authored here),
it is held to a committed digest pin rather than to grc's own authoring gates:
``vendor/aiqt/PIN.toml`` records the pack repo + commit (provenance) and the module's
sha256 + byte count (from the pack's ``.aiqt/manifest.toml``), and this gate ``--check``s
that the vendored file still matches. A mismatch means the vendored bytes and the committed
pin disagree (this gate checks byte equality and does not determine which side changed);
re-vendor from the pinned pack commit and re-pin, or correct the pin, never hand-edit the
vendored file.

The whole pin is schema-validated before any digest work, so a malformed pin (a scalar
or list where a table is expected, a non-printable-ASCII path or repo, a sha256 that is not
exactly 64 lowercase hex, a negative or over-large byte count, a short or non-hex commit)
fails with a clean exit 1 and a named problem list, never an uncaught exception. (A
pathologically large vendored file ON DISK is resource exhaustion, not a malformed pin, and
is out of scope: the vendored file is trusted in-repo state.) The [source] provenance requirement is SYNTACTIC only: the gate shape-checks
and reports the recorded repo and 40-hex commit; it does NOT confirm they exist upstream
or that the pinned digest corresponds to that commit's content. Those checks belong to
the re-vendoring step, not to this gate.

All output is ASCII-safe (non-ASCII in any message is backslash-escaped), so no stdout encoding
(e.g. a strict-ASCII CI locale) can turn a clean rc=1 into an uncaught UnicodeEncodeError.

Stdlib-only. Exit 0 = pin holds; exit 1 = malformed pin / mismatch / missing pin or file.
"""

from __future__ import annotations

import hashlib
import re
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VENDOR = REPO_ROOT / "vendor" / "aiqt"
PIN = VENDOR / "PIN.toml"

# A git commit id: exactly 40 hexadecimal characters, either case (fullmatch-anchored).
_COMMIT_RE = re.compile(r"[0-9a-fA-F]{40}")
_SHA256_RE = re.compile(r"[0-9a-f]{64}")  # lowercase: matches hashlib hexdigest exactly
# A source module's byte count is bounded far below this; a larger or negative value is
# malformed. Rejecting it at schema keeps the mismatch message's int->decimal formatting
# away from Python's 4300-digit int-string-conversion ValueError (any hex/oct/bin literal).
_MAX_MODULE_BYTES = 1 << 30  # 1 GiB


def _is_printable_ascii(s: str) -> bool:
    """True iff every char is a printable ASCII graphic (0x21-0x7E): no space, no control
    (C0/C1/DEL), no Unicode format/bidi/zero-width (Cf), and no separator (Zl/Zp/Zs). A vendor
    repo slug and a relative module path are printable-ASCII by construction, so this positive
    charset both forecloses display-line corruption (Trojan-Source bidi, CVE-2021-42574) AND
    guarantees the echoed OK/provenance line is encodable on any stdout (no UnicodeEncodeError)."""
    return bool(s) and all(0x21 <= ord(ch) <= 0x7E for ch in s)


def _rel(p: Path) -> str:
    """Path relative to the repo root when possible, else the path itself.
    Keeps the error path from crashing if VENDOR is ever relocated or monkeypatched."""
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def _emit(text: str) -> None:
    """ASCII-safe output choke-point: NEVER raise UnicodeEncodeError, regardless of the stdout
    encoding (e.g. a strict-ASCII CI locale) or of non-ASCII interpolated into a message (e.g. a
    tomllib parse error that echoes a non-ASCII key). Non-ASCII becomes a backslash escape. This is
    belt-and-suspenders with the printable-ASCII field schema: a bad FIELD still fails with a named
    problem, and any residual non-ASCII in an error string is rendered safely rather than crashing."""
    sys.stdout.write(text.encode("ascii", "backslashreplace").decode("ascii") + "\n")


def _fail(msg: str) -> int:
    _emit(f"FAIL: {msg}")
    return 1


def _pin_schema_problems(pin: dict) -> list[str]:
    """Type-check every field the gate reads; empty list = well-shaped.

    Collects ALL problems rather than stopping at the first, so one run reports a
    wholly malformed pin completely. Purely syntactic: a well-shaped [source] is
    RECORDED provenance; this function does not establish that the repo or commit
    exist upstream, or that the pinned digest corresponds to that commit.
    """
    problems: list[str] = []

    module = pin.get("module")
    if not isinstance(module, dict):
        problems.append("[module] must be a table carrying path, sha256, and bytes")
    else:
        rel = module.get("path")
        if not isinstance(rel, str) or not rel:
            problems.append("[module] path must be a non-empty string")
        elif not _is_printable_ascii(rel):
            problems.append("[module] path must be printable ASCII (no spaces, control, or bidi/format characters)")
        sha = module.get("sha256")
        if not isinstance(sha, str) or not _SHA256_RE.fullmatch(sha):
            problems.append("[module] sha256 must be a string of exactly 64 lowercase hexadecimal characters")
        nbytes = module.get("bytes")
        if isinstance(nbytes, bool) or not isinstance(nbytes, int):
            # bool is an int subclass in Python, so `bytes = true` needs the explicit test
            problems.append("[module] bytes must be an integer")
        elif nbytes < 0 or nbytes > _MAX_MODULE_BYTES:
            problems.append(f"[module] bytes must be an integer between 0 and {_MAX_MODULE_BYTES}")

    source = pin.get("source")
    if not isinstance(source, dict):
        problems.append("[source] must be a table carrying repo and commit (recorded provenance)")
    else:
        repo = source.get("repo")
        if not isinstance(repo, str) or not repo:
            problems.append("[source] repo must be a non-empty string")
        elif not _is_printable_ascii(repo):
            problems.append("[source] repo must be printable ASCII (no spaces, control, or bidi/format characters)")
        commit = source.get("commit")
        if not isinstance(commit, str) or not _COMMIT_RE.fullmatch(commit):
            problems.append("[source] commit must be a string of exactly 40 hexadecimal characters")

    return problems


def check() -> int:
    if not PIN.is_file():
        return _fail(f"vendor pin not found at {_rel(PIN)}")
    try:
        pin = tomllib.loads(PIN.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - deliberate: the pin is trusted committed state, so ANY
        # read/parse failure (OS error, decode error, TOML syntax, an over-long int-string ValueError,
        # a RecursionError on pathological nesting, etc.) is a corruption/tamper signal to report
        # cleanly, never to crash on. This one choke-point makes the whole gate crash-safe by shape.
        return _fail(f"vendor pin {_rel(PIN)} is unreadable: {type(exc).__name__}: {exc}")

    # Schema first: every later step (the VENDOR/rel join, the mismatch message's
    # commit, the OK line's repo@commit) reads these fields, so type-proving the
    # whole pin here makes the rest of the gate crash-safe by construction.
    problems = _pin_schema_problems(pin)
    if problems:
        return _fail(f"vendor pin {_rel(PIN)} is malformed: {'; '.join(problems)}")

    rel = pin["module"]["path"]
    want_sha = pin["module"]["sha256"]
    want_bytes = pin["module"]["bytes"]
    src_repo = pin["source"]["repo"]
    src_commit = pin["source"]["commit"]

    target = VENDOR / rel
    try:
        contained = target.resolve().is_relative_to(VENDOR.resolve())
    except (OSError, RuntimeError, ValueError):
        contained = False  # cannot establish containment (unresolvable/NUL/loop) -> refuse rather than proceed
    if not contained:
        return _fail(f"PIN.toml [module] path {rel!r} escapes the vendor root {_rel(VENDOR)}")

    if not target.is_file():
        return _fail(f"vendored module missing at {_rel(target)}")

    try:
        data = target.read_bytes()
    except OSError as exc:
        return _fail(f"vendored module {_rel(target)} is unreadable: {exc}")
    got_sha = hashlib.sha256(data).hexdigest()
    got_bytes = len(data)

    mismatches = []
    if got_bytes != want_bytes:
        mismatches.append(f"byte count {got_bytes} != pinned {want_bytes}")
    if got_sha != want_sha:
        mismatches.append(f"sha256 {got_sha} != pinned {want_sha}")
    if mismatches:
        return _fail(
            f"vendored {rel} does not match PIN.toml ({'; '.join(mismatches)}). "
            "The vendored bytes and the committed pin disagree (this gate checks byte "
            "equality and does not determine which side changed); re-vendor from the "
            f"pinned pack commit ({src_commit}) and re-pin, or correct the pin."
        )

    _emit(
        f"OK: vendored {rel} matches PIN.toml "
        f"(sha256 {got_sha[:12]}..., {got_bytes} bytes; pin records source "
        f"{src_repo}@{src_commit[:12]})."
    )
    return 0


if __name__ == "__main__":
    sys.exit(check())
