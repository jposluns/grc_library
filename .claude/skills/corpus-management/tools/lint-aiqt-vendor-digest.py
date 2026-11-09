#!/usr/bin/env python3
"""Verify the vendored AIQT copy against its pin (digest gate).

The Corpus-Management umbrella vendors a subset of the AIQT project's release
(https://aiqt.ai) under ``.claude/aiqt/``: the rendered rule set, the generic
corpus core ``tools/aiqt_corpus.py`` (imported through
``.claude/skills/corpus-management/tools/aiqt_bootstrap.py``), the upstream
LICENSE and NOTICE, and the upstream release manifest with its release root
record. Because the copy is CONSUMED from AIQT, not authored here, it is held
to a committed pin rather than to this project's own authoring gates.

The pin identity is the upstream RELEASE ROOT digest: the SHA-256 of the exact
bytes of the vendored ``.aiqt/manifest.toml``, which is also the single line
of ``.aiqt/release/root.txt``. ``.claude/aiqt/PIN.toml`` records that digest;
this gate recomputes it, requires the pin, the root record and the manifest to
agree, and then checks every vendored file's byte count and SHA-256 against
its manifest row, with no missing, extra, or symlinked entry. The commit the
pin also records is PROVENANCE ONLY: the gate shape-checks and echoes it but
verifies nothing against it, because commit ids do not carry over when the
upstream project moves to a new repository.

A mismatch means the vendored bytes and the committed pin disagree (this gate
checks byte equality and does not determine which side changed); re-vendor
from the pinned release and re-pin, or correct the pin, never hand-edit the
vendored copy.

All output is ASCII-safe (non-ASCII in any message is backslash-escaped), so
no stdout encoding can turn a clean rc=1 into an uncaught UnicodeEncodeError.

Stdlib-only. Exit 0 = pin holds; exit 1 = malformed pin / mismatch / missing
pin or file; exit 2 = refused surplus argument.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aiqt_rules  # noqa: E402  single source of truth for the pin verification

# The repository root: this file lives at
# .claude/skills/corpus-management/tools/, four levels down.
REPO_ROOT = Path(__file__).resolve().parents[4]
VENDOR = REPO_ROOT / ".claude" / "aiqt"
PIN = VENDOR / "PIN.toml"


def _emit(text: str) -> None:
    """ASCII-safe output choke-point: NEVER raise UnicodeEncodeError, whatever
    the stdout encoding or the non-ASCII content a parse error echoes."""
    sys.stdout.write(text.encode("ascii", "backslashreplace").decode("ascii") + "\n")


def _fail(msg: str) -> int:
    _emit(f"FAIL: {msg}")
    return 1


def check(root: Path | None = None) -> int:
    """Run the digest gate against ``root`` (default: this checkout).
    The call completing without an exception is part of the contract: any
    verification problem is a clean rc=1, never a traceback."""
    base = Path(root) if root is not None else REPO_ROOT
    try:
        pin, inventory = aiqt_rules.verify_vendored(base)
    except ValueError as exc:
        return _fail(str(exc))
    except Exception as exc:  # noqa: BLE001 - deliberate: the pin and the vendored copy are
        # trusted committed state, so ANY residual failure (OS error, decode error, recursion
        # on pathological input) is a corruption/tamper signal to report cleanly, never to
        # crash on. This one choke-point keeps the whole gate crash-safe by shape.
        return _fail(f"vendored AIQT verification is unreadable: {type(exc).__name__}: {exc}")
    source = pin["source"]
    _emit(
        f"OK: {len(inventory)} vendored AIQT files match the release root "
        f"{source['release-root'][:19]}... (release {source['release-version']}; "
        f"source {source['project']} at {source['url']}; provenance commit {source['commit']})."
    )
    return 0


if __name__ == "__main__":
    # This tool takes no argument; an unknown or surplus one is refused
    # (exit 2) before the check runs.
    from lint_common import strict_flags as _strict_flags
    _strict_flags(sys.argv[1:], ())
    sys.exit(check())
