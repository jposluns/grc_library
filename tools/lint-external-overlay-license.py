#!/usr/bin/env python3
"""External-overlay licence audit for rules and registered addyosmani skills.

Rules live under .claude/rules/external/<source>/; addyosmani skills live
under .claude/skills/addyosmani-<name>/. Every declared location must exist
and carry its expected LICENSE. Unknown rule sources and unknown addyosmani
skill directories fail. All markdown in those locations is checked for the
project licence claim, as is rule-source PROVENANCE.txt (required beside LICENSE).
Skill locations also require SKILL.md and PROVENANCE.md.
Registered skills require name/description-only frontmatter and bodies free of
active Claude interpolation tokens, using JavaScript whitespace boundaries.
Skill bytes must be strict UTF-8 without CR, NUL or interpolation sentinels.
Unrelated skills are outside this gate. Exit codes: 0 pass, 1 findings, 2 error.
"""

from __future__ import annotations

import re
import stat
import sys
from typing import NamedTuple

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import REPO_ROOT  # noqa: E402  # grc-config/store, stays local
from external_overlay import (  # noqa: E402
    ADDYOSMANI_SKILLS, InputError, directory_entries, path_stat, read_utf8, walk_files,
)


EXTERNAL_OVERLAY_DIR = REPO_ROOT / ".claude" / "rules" / "external"

# Map of (external source subdir name) -> (expected licence identifier).
# The expected identifier is matched against the LICENSE file's first
# non-empty line, case-insensitive prefix match. Adding a new external
# source requires adding an entry here.
EXPECTED_LICENSE: dict[str, str] = {
    "kariedo": "MIT",
    "tikitribe": "MIT",
}

# Project licence claim that external markdown and rule provenance MUST NOT contain
# in their metadata block.
PROJECT_LICENCE_CLAIM = "**License:** CC BY-SA 4.0"

# Mapping from the LICENSE-file first-line prefix to the canonical
# identifier used in EXPECTED_LICENSE.
LICENSE_PREFIX_TO_IDENT: dict[str, str] = {
    "MIT License": "MIT",
    "Apache License": "Apache 2.0",
    "BSD ": "BSD",
    "BSD-": "BSD",
    "GNU GENERAL PUBLIC LICENSE": "GPL",
    "Mozilla Public License": "MPL",
    "ISC License": "ISC",
    "Creative Commons CC0": "CC0",
    "Creative Commons Attribution": "CC BY",
    "The Unlicense": "Unlicense",
}


class Finding(NamedTuple):
    kind: str
    location: str
    detail: str


def identify_license(text: str) -> str | None:
    """Return the canonical identifier of a LICENSE file's text, or None
    if no known prefix matches the file's first non-empty line."""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        for prefix, ident in LICENSE_PREFIX_TO_IDENT.items():
            if stripped.lower().startswith(prefix.lower()):
                return ident
        return None
    return None


def check_tree(root, expected_licenses, prefix="") -> list[Finding]:
    findings: list[Finding] = []
    relative_root = root.relative_to(REPO_ROOT).as_posix()

    declared_sources = set(expected_licenses.keys())
    present_sources: set[str] = set()
    try:
        info = path_stat(root, missing_ok=True)
        if info is not None and stat.S_ISDIR(info.st_mode):
            for entry in directory_entries(root):
                if entry.name.startswith(".") or not entry.name.startswith(prefix):
                    continue
                if stat.S_ISDIR(path_stat(entry).st_mode):
                    present_sources.add(entry.name)
    except InputError as exc:
        return [Finding("inaccessible-overlay", exc.path.relative_to(REPO_ROOT).as_posix(),
                        str(exc))]

    # Check 1: every present source declares an expected licence.
    for source in sorted(present_sources - declared_sources):
        findings.append(
            Finding(
                kind="undeclared-source",
                location=f"{relative_root}/{source}/",
                detail=(
                    f"present in the external overlay but no expected licence "
                    f"declared in EXPECTED_LICENSE. Add the source to the "
                    f"map in tools/lint-external-overlay-license.py."
                ),
            )
        )

    # Check 1b: every declared source is actually present (catches stale map entries).
    for source in sorted(declared_sources - present_sources):
        findings.append(
            Finding(
                kind="stale-declaration",
                location=f"{relative_root}/{source}/",
                detail=(
                    f"declared in EXPECTED_LICENSE but no directory present. "
                    f"Remove the source from the map in "
                    f"tools/lint-external-overlay-license.py."
                ),
            )
        )

    # Check 2: each present, declared source has a LICENSE file matching expected.
    for source in sorted(present_sources & declared_sources):
        if not prefix:
            provenance = root / source / "PROVENANCE.txt"
            try:
                info = path_stat(provenance, missing_ok=True)
                if info is None or not stat.S_ISREG(info.st_mode):
                    findings.append(Finding(
                        "missing-rule-provenance", provenance.relative_to(REPO_ROOT).as_posix(),
                        "Declared external rule source requires PROVENANCE.txt beside LICENSE.",
                    ))
            except InputError as exc:
                findings.append(Finding("inaccessible-overlay",
                                        provenance.relative_to(REPO_ROOT).as_posix(), str(exc)))
        expected = expected_licenses[source]
        license_path = root / source / "LICENSE"
        try:
            info = path_stat(license_path, missing_ok=True)
        except InputError as exc:
            findings.append(Finding("unreadable-license-file",
                                    license_path.relative_to(REPO_ROOT).as_posix(), str(exc)))
            continue
        if info is None or not stat.S_ISREG(info.st_mode):
            findings.append(
                Finding(
                    kind="missing-license-file",
                    location=f"{relative_root}/{source}/LICENSE",
                    detail=(
                        f"expected to exist (source's licence is {expected}) "
                        f"but the file is absent or unreadable."
                    ),
                )
            )
            continue
        try:
            text = read_utf8(license_path)
        except InputError as exc:
            findings.append(
                Finding(
                    kind="unreadable-license-file",
                    location=f"{relative_root}/{source}/LICENSE",
                    detail=f"LICENSE file is not readable as UTF-8 text: {exc}",
                )
            )
            continue
        actual = identify_license(text)
        if actual is None:
            findings.append(
                Finding(
                    kind="unrecognized-license",
                    location=f"{relative_root}/{source}/LICENSE",
                    detail=(
                        f"LICENSE first non-empty line did not match any known "
                        f"prefix in LICENSE_PREFIX_TO_IDENT. Expected: {expected}. "
                        f"Either update the LICENSE to a recognized form or add "
                        f"a new prefix to LICENSE_PREFIX_TO_IDENT."
                    ),
                )
            )
            continue
        if actual != expected:
            findings.append(
                Finding(
                    kind="license-mismatch",
                    location=f"{relative_root}/{source}/LICENSE",
                    detail=(
                        f"LICENSE file identifies as {actual}, but EXPECTED_LICENSE "
                        f"declares {expected}. Either the LICENSE was changed "
                        f"upstream (update EXPECTED_LICENSE) or the file is wrong."
                    ),
                )
            )

    # Check 3: audit markdown and non-rule provenance for the project licence claim.
    for source in sorted(present_sources):
        try:
            for md_file in walk_files(root / source):
                if not (md_file.name.endswith(".md") or md_file.name == "PROVENANCE.txt"):
                    continue
                rel = md_file.relative_to(REPO_ROOT).as_posix()
                try:
                    text = read_utf8(md_file)
                except InputError as exc:
                    kind = ("unreadable-skill" if prefix == "addyosmani-"
                            and source in declared_sources
                            and md_file == root / source / "SKILL.md"
                            else "unreadable-provenance-file" if md_file.name == "PROVENANCE.txt"
                            else "unreadable-markdown-file")
                    findings.append(Finding(kind, rel, str(exc)))
                    continue
                if PROJECT_LICENCE_CLAIM in text:
                    findings.append(
                        Finding(
                            kind="external-file-claims-project-licence",
                            location=rel,
                            detail=(
                                f"contains the literal string '{PROJECT_LICENCE_CLAIM}' "
                                f"but is an external file. External files retain their "
                                f"source project's licence (per the overlay's "
                                f"directory-level LICENSE file)."
                            ),
                        )
                    )
        except InputError as exc:
            findings.append(Finding("inaccessible-overlay",
                                    exc.path.relative_to(REPO_ROOT).as_posix(), str(exc)))

    return findings


# Claude Code 2.1.287, /usr/bin/claude: jTe, CDt, Vne, _4n and Y1n.
# Keep the current name/description-only header: an `arguments` declaration
# enables arbitrary named $tokens and needs a fresh interpolation audit.
SKILL_HEADER_RE = re.compile(
    r"\A---\nname: [^\n]+\ndescription: [^\n]+\n---(?:\n|\Z)"
)
ARGUMENT_ESCAPE_RE = re.compile(r"(?<!\\)\\\$(?=[0-9]|ARGUMENTS)")
# ECMAScript WhiteSpace + LineTerminator (RegExp \s), not Python's \s:
# includes U+FEFF; excludes U+001C..U+001F and U+0085.
JS_WHITESPACE = (
    r"\u0009-\u000d\u0020\u00a0\u1680\u2000-\u200a"
    r"\u2028\u2029\u202f\u205f\u3000\ufeff"
)
# Claude Code 2.1.287: ZVo calls Ms, whose jk regex is
# /^---\s*\n([\s\S]*?)---\s*\n?/. The first closing triple dash wins,
# even inside a header value; trailing JS whitespace is consumed as well.
# The strict header above already excludes the leading BOM that Ms strips.
CLAUDE_FRONTMATTER_RE = re.compile(
    rf"\A---[{JS_WHITESPACE}]*\n([\s\S]*?)---[{JS_WHITESPACE}]*\n?"
)
SKILL_TOKEN_RE = re.compile(
    r"\$ARGUMENTS(?:\[[0-9]+\])?|\$[0-9]+(?![A-Za-z0-9_])"
    r"|\$\{CLAUDE_(?:SKILL_DIR|PROJECT_DIR|SESSION_ID|EFFORT|PLUGIN_ROOT|PLUGIN_DATA)\}"
    r"|\$\{user_config\.[^}]+\}"
    # Conservatively refuse command markers, including incomplete commands.
    rf"|```!|(?<![^{JS_WHITESPACE}])!`"
)


def check_skill_body(path) -> list[Finding]:
    location = path.relative_to(REPO_ROOT).as_posix()
    # Claude reads the original UTF-8 bytes. Universal-newline translation can
    # invent frontmatter and hide live tokens, so never use read_text_safe here.
    try:
        text = read_utf8(path)
    except InputError as exc:
        return [Finding(
            "unreadable-skill", location,
            str(exc),
        )]
    # Fail before parsing or masking, even when the file contains no tokens.
    # jTe in Claude Code 2.1.287 replaces literal U+FFFE/U+FFFF with U+FFFD;
    # refuse these reserved interpolation sentinels rather than model a rewrite.
    for character, label in (("\r", "CR (including CRLF)"), ("\0", "NUL"),
                             ("\ufffe", "U+FFFE"), ("\uffff", "U+FFFF")):
        if character in text:
            return [Finding(
                "unsupported-skill-bytes", location,
                f"Cannot audit skill body containing {label}; use UTF-8 text "
                "with LF line endings and no NUL or interpolation sentinels.",
            )]
    header = SKILL_HEADER_RE.match(text)
    if header is None:
        return [Finding(
            "unsupported-skill-frontmatter", location,
            "Expected the name/description-only overlay header; changes require "
            "an interpolation audit, including named arguments.",
        )]
    runtime_header = CLAUDE_FRONTMATTER_RE.match(text)
    assert runtime_header is not None  # Guaranteed by SKILL_HEADER_RE above.
    body_start = runtime_header.end()
    # A single backslash not preceded by another backslash protects argument
    # placeholders. This masking does not exempt ${CLAUDE_*} or command markers.
    body = ARGUMENT_ESCAPE_RE.sub("\uffff", text[body_start:])
    findings = []
    first_line = text[:body_start].count("\n") + 1
    for token in SKILL_TOKEN_RE.finditer(body):
        lineno = first_line + body.count("\n", 0, token.start())
        findings.append(Finding(
            "skill-interpolation-token", f"{location}:{lineno}",
            f"{token.group()!r} may interpolate at invocation; escape an argument "
            "placeholder or rewrite the example and record the divergence.",
        ))
    return findings


def check() -> list[Finding]:
    skills_root = REPO_ROOT / ".claude" / "skills"
    findings = check_tree(EXTERNAL_OVERLAY_DIR, EXPECTED_LICENSE)
    findings.extend(check_tree(
        skills_root,
        dict.fromkeys(ADDYOSMANI_SKILLS, "MIT"),
        "addyosmani-",
    ))
    for name in ADDYOSMANI_SKILLS:
        for filename in ("SKILL.md", "PROVENANCE.md"):
            path = skills_root / name / filename
            location = path.relative_to(REPO_ROOT).as_posix()
            try:
                info = path_stat(path, missing_ok=True)
            except InputError as exc:
                findings.append(Finding("inaccessible-overlay", location, str(exc)))
                continue
            if info is None or not stat.S_ISREG(info.st_mode):
                findings.append(Finding(
                    "missing-skill-companion", location,
                    "Declared external skill requires SKILL.md and PROVENANCE.md.",
                ))
            elif filename == "SKILL.md":
                findings.extend(check_skill_body(path))
    # Licence and body checks can encounter the same unreadable SKILL.md.
    return list(dict.fromkeys(findings))


def main(argv: list[str]) -> int:
    findings = check()
    if not findings:
        print(
            f"OK: external overlay licence consistency confirmed "
            f"({len(EXPECTED_LICENSE) + len(ADDYOSMANI_SKILLS)} declared "
            f"location(s); all LICENSE files "
            f"present and matching expected; rule provenance present; no audited file claims "
            f"the project licence; skill bodies have no active interpolation)."
        )
        return 0

    for finding in findings:
        print(f"=== {finding.kind} ===")
        print(f"  {finding.location}: {finding.detail}")
    print(
        f"\nFAIL: {len(findings)} external-overlay licence finding(s). "
        f"Resolve by updating EXPECTED_LICENSE, restoring the LICENSE file, "
        f"removing the incorrect project-licence claim, or fixing skill interpolation.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    # 3b50b2g: this tool takes no argument; an unknown or surplus one
    # used to be ignored with exit 0, so it is refused (exit 2) before the check runs.
    import os as _os
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from lint_common import strict_flags as _strict_flags
    _strict_flags(sys.argv[1:], ())
    sys.exit(main(sys.argv))
