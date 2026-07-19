#!/usr/bin/env python3
"""Sibling-repo stub-guard audit (gate 70), guard-if-present-as-stub.

The three sibling repositories (``grc_library_ref`` / ``grc_library_scratch`` /
``grc_library_private``) are SEPARATE repositories that live beside this one at
origin; they are NOT shipped inside the public repo. The maintainer runs the
real siblings beside this clone; an adopter chooses how to run (their own
siblings, or the in-repo ``.<name>`` placeholder stub that the ``/adopt`` flow
creates on request, or nothing). So the in-repo ``.ref`` / ``.scratch`` /
``.private`` directories are NOT committed to this repo by default, and their
absence is the normal state, not a defect.

This gate is therefore GUARD-IF-PRESENT-AS-STUB. For each of the three slots:

1. ABSENT -> OK (no finding). The maintainer repo has no stubs, and an adopter
   who did not opt into the in-repo placeholder model has none either.
2. PRESENT AND DECLARED A STUB (a ``README.md`` whose first line is the
   ``<!-- SIBLING-PLACEHOLDER: <name> -->`` marker for THIS slot) -> the gate
   enforces the stub shape: exactly one entry ``README.md`` (no other file or
   subdirectory) bounded to ``MAX_README_LINES`` lines, so an adopter-created
   stub can never grow into reference / worker-exchange / private-operational
   payload while still calling itself a placeholder.
3. PRESENT BUT NOT A DECLARED STUB (no ``README.md``, or a ``README.md`` without
   the marker on its first line) -> the gate does NOT apply and returns no
   finding. This is the ``/adopt`` "functional directory" case: an adopter who
   materializes a real sibling checkout (or their own content) at ``.<name>`` is
   subject to different guards or none; a stub-shape gate is not their concern.

The gate scans ONLY the in-repo ``.ref`` / ``.scratch`` / ``.private`` slots; it
never reaches the real sibling repositories (which live outside this repo and
are never scanned). It ships in the public repo and is active on an adopter's
clone-and-run, where it is really a POST-ADOPTION payload-creep guard for an
adopter who chose the in-repo stub model; in the maintainer repo (all three
absent) it passes trivially.

Exit codes: 0 = every present-and-declared stub is well-formed (and absent slots
are fine); 1 = at least one declared stub carries payload or exceeds the cap.
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
    """Return a list of violation messages for one placeholder slot (empty = OK).

    Guard-if-present-as-stub (see the module docstring): an ABSENT slot is OK; a
    slot PRESENT AND DECLARED A STUB (a ``README.md`` whose first line is this
    slot's ``SIBLING-PLACEHOLDER`` marker) must be a well-formed, payload-free
    stub; a slot PRESENT BUT NOT a declared stub (no ``README.md``, or one
    without the marker, an adopter's functional directory) is out of this gate's
    scope and yields no finding.

    ``dir_path`` is the actual directory to inspect (``REPO_ROOT / <name>`` in
    normal use; a temp directory in tests). Its basename is used in messages.
    """
    findings: list[str] = []
    dir_name = dir_path.name

    # 1. Absent slot: fine. The dirs are not shipped in the public repo; the
    #    maintainer runs the real siblings, and an adopter opts into the in-repo
    #    stub only via /adopt.
    if not dir_path.is_dir():
        return findings

    # Is this a DECLARED stub? (a README.md whose first line is THIS slot's marker)
    readme = dir_path / "README.md"
    expected_marker = MARKER_TEMPLATE.format(name=marker_token)
    declared_stub = False
    if readme.is_file():
        try:
            first_lines = readme.read_text(encoding="utf-8").splitlines()[:1]
        except OSError:  # pragma: no cover - unexpected I/O error
            first_lines = []
        if first_lines and first_lines[0].strip() == expected_marker:
            declared_stub = True

    # 3. Present but NOT a declared stub (a functional sibling checkout, or the
    #    adopter's own content): out of scope, different guards or none apply.
    if not declared_stub:
        return findings

    # 2. A declared stub: enforce the stub shape so it cannot grow into payload.
    entries = sorted(p.name for p in dir_path.iterdir())
    if entries != ["README.md"]:
        extra = [e for e in entries if e != "README.md"]
        if extra:
            findings.append(
                f"{dir_name}/: a declared placeholder stub must contain ONLY "
                f"README.md; found also: {', '.join(extra)}. A stub must never "
                f"carry payload."
            )

    try:
        lines = readme.read_text(encoding="utf-8").splitlines()
    except OSError as exc:  # pragma: no cover - unexpected I/O error
        findings.append(f"{dir_name}/README.md: cannot read ({exc}).")
        return findings
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
        f"OK: {len(PLACEHOLDERS)} sibling-repo placeholder slot(s) "
        f"(.ref, .scratch, .private) checked; each is absent, a functional "
        f"directory (out of scope), or a well-formed stub."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
