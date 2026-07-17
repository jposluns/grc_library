#!/usr/bin/env python3
"""Sibling-repo stub-guard audit (gate 70).

Guards the in-repo sibling-repo placeholder directories introduced in TODO
section 1.19.3: ``.ref``, ``.scratch``, ``.private``. Each stands in for a
sibling repository (``grc_library_ref`` / ``grc_library_scratch`` /
``grc_library_private``) when that sibling is absent (an adopter clone), so a
fork that clones only this public repo resolves real-sibling then in-repo
placeholder then a clean no-op.

A placeholder must stay a PLACEHOLDER: it must never accumulate real reference
text, worker-exchange payload, or private operational state that would then ship
to adopters in the public repo. This gate enforces that each placeholder dir:

1. EXISTS (it is a committed placeholder; absence is a defect or tampering).
2. contains EXACTLY one entry, ``README.md`` (no other file or subdirectory).
3. whose ``README.md`` carries the ``<!-- SIBLING-PLACEHOLDER: <name> -->``
   marker on its first line (``<name>`` = ``ref`` / ``scratch`` / ``private``).
4. whose ``README.md`` is bounded to at most ``MAX_README_LINES`` lines, so the
   stub cannot grow into a payload while still carrying the marker.

The gate scans ONLY the in-repo ``.ref`` / ``.scratch`` / ``.private`` dirs; it
never reaches the real sibling repositories (which live outside this repo and
are never scanned). It ships in the public repo and is active on an adopter's
clone-and-run.

Exit codes: 0 = all placeholders are well-formed stubs; 1 = at least one
placeholder violates a rule.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# The placeholder directory name -> its SIBLING-PLACEHOLDER marker token.
PLACEHOLDERS: dict[str, str] = {
    ".ref": "ref",
    ".scratch": "scratch",
    ".private": "private",
}

MARKER_TEMPLATE = "<!-- SIBLING-PLACEHOLDER: {name} -->"
MAX_README_LINES = 25


def check_placeholder(dir_path: Path, marker_token: str) -> list[str]:
    """Return a list of violation messages for one placeholder dir (empty = OK).

    ``dir_path`` is the actual directory to inspect (``REPO_ROOT / <name>`` in
    normal use; a temp directory in tests). Its basename is used in messages.
    """
    findings: list[str] = []
    dir_name = dir_path.name

    if not dir_path.is_dir():
        findings.append(
            f"{dir_name}/: placeholder directory is missing (it is a committed "
            f"stub and must exist)."
        )
        return findings

    entries = sorted(p.name for p in dir_path.iterdir())
    if entries != ["README.md"]:
        extra = [e for e in entries if e != "README.md"]
        if extra:
            findings.append(
                f"{dir_name}/: must contain ONLY README.md; found also: "
                f"{', '.join(extra)}. A placeholder must never carry payload."
            )
        if "README.md" not in entries:
            findings.append(f"{dir_name}/: missing README.md stub.")
            return findings

    readme = dir_path / "README.md"
    try:
        text = readme.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover - unexpected I/O error
        findings.append(f"{dir_name}/README.md: cannot read ({exc}).")
        return findings

    lines = text.splitlines()
    expected_marker = MARKER_TEMPLATE.format(name=marker_token)
    if not lines or lines[0].strip() != expected_marker:
        findings.append(
            f"{dir_name}/README.md: first line must be the marker "
            f"'{expected_marker}'."
        )
    if len(lines) > MAX_README_LINES:
        findings.append(
            f"{dir_name}/README.md: {len(lines)} lines exceeds the "
            f"{MAX_README_LINES}-line placeholder cap (payload creep)."
        )

    return findings


def main(argv: list[str] | None = None) -> int:
    all_findings: list[str] = []
    for dir_name, marker_token in PLACEHOLDERS.items():
        all_findings.extend(check_placeholder(REPO_ROOT / dir_name, marker_token))

    for message in all_findings:
        print(f"FAIL: {message}", file=sys.stderr)

    if all_findings:
        return 1

    print(
        f"OK: {len(PLACEHOLDERS)} sibling-repo placeholder(s) "
        f"(.ref, .scratch, .private) are well-formed stubs."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
