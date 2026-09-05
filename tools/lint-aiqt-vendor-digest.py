#!/usr/bin/env python3
"""Verify the vendored AIQT generic-core module against its pin (digest gate).

The Corpus-Management umbrella vendors a MINIMAL subset of the AIQT guardrails pack
-- ``vendor/aiqt/tools/aiqt_corpus.py`` -- which grc's corpus tools import through
``tools/aiqt_bootstrap.py``. Because it is CONSUMED from AIQT (not authored here),
its integrity is guaranteed by a digest pin rather than by grc's own authoring gates:
``vendor/aiqt/PIN.toml`` records the pack commit and the module's sha256 + byte count
(from the pack's ``.aiqt/manifest.toml``), and this gate ``--check``s that the vendored
file still matches. A mismatch means the vendored copy drifted or was tampered with;
re-vendor from the pinned pack commit and re-pin, never hand-edit the vendored file.

Stdlib-only. Exit 0 = pin holds; exit 1 = mismatch / missing pin or file.
"""

from __future__ import annotations

import hashlib
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VENDOR = REPO_ROOT / "vendor" / "aiqt"
PIN = VENDOR / "PIN.toml"


def _fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def check() -> int:
    if not PIN.is_file():
        return _fail(f"vendor pin not found at {PIN.relative_to(REPO_ROOT)}")
    try:
        pin = tomllib.loads(PIN.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return _fail(f"vendor pin {PIN.relative_to(REPO_ROOT)} is unreadable: {exc}")

    module = pin.get("module", {})
    rel = module.get("path")
    want_sha = module.get("sha256")
    want_bytes = module.get("bytes")
    if not rel or not want_sha or want_bytes is None:
        return _fail("PIN.toml [module] must set path, sha256, and bytes")

    target = VENDOR / rel
    if not target.is_file():
        return _fail(f"vendored module missing at {target.relative_to(REPO_ROOT)}")

    data = target.read_bytes()
    got_sha = hashlib.sha256(data).hexdigest()
    got_bytes = len(data)

    problems = []
    if got_bytes != want_bytes:
        problems.append(f"byte count {got_bytes} != pinned {want_bytes}")
    if got_sha != want_sha:
        problems.append(f"sha256 {got_sha} != pinned {want_sha}")
    if problems:
        return _fail(
            f"vendored {rel} does not match PIN.toml ({'; '.join(problems)}). "
            "The vendored AIQT core drifted or was hand-edited; re-vendor from the "
            f"pinned pack commit ({pin.get('source', {}).get('commit', '?')}) and re-pin."
        )

    src = pin.get("source", {})
    print(
        f"OK: vendored {rel} matches PIN.toml "
        f"(sha256 {got_sha[:12]}..., {got_bytes} bytes; pinned to {src.get('repo', '?')}"
        f"@{str(src.get('commit', '?'))[:12]})."
    )
    return 0


if __name__ == "__main__":
    sys.exit(check())
