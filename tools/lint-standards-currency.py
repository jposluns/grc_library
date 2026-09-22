#!/usr/bin/env python3
"""Standards-currency audit: project policy and register parser.

The pack engine owns citation extraction, comparison and reporting.
This wrapper owns the canonical-register schema, roots, exclusions and CLI.

PR1 defaults to report mode. Only the unchanged legacy Markdown stale
check blocks in that mode. New findings are advisory. Explicit enforce
mode supports migration fixtures; no gate invocation enables it in PR1.

Exit: 0 no blocking findings; 1 blocking findings or malformed/empty
register; 2 missing/unreadable intended inputs.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import AUDITED_DOMAIN_DIRS  # noqa: E402  # grc-config/store, stays local

REPO_ROOT = Path(__file__).resolve().parent.parent
PACK_TOOLS = REPO_ROOT / ".corpus-management" / "tools"
CANONICAL_REGISTER = REPO_ROOT / "governance" / "register-canonical-citations.md"

# Files exempt from the linter (typically CHANGELOG-style records and
# discussions of the defect itself).
EXEMPT_FILES = {
    "CHANGELOG.md",
    "TODO.md",
    "TODO-REFERENCE.md",
    "governance/register-canonical-citations.md",
}

EXEMPT_DIRECTORY_PREFIXES = (
    "tools/",
    "docs/",
)

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    "CONTRIBUTING.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    # Domain run splatted from lint_common (scan-scope parity gate
    # forbids hardcoding the run).
    *AUDITED_DOMAIN_DIRS,
    "guardrails",
]


STANDARD_HEADER = [
    "Standard ID", "Current version", "Publication date",
    "Topic", "Superseded versions",
]
EVIDENCE_HEADER = ["Upstream check location", "Last verified (UTC)"]
PROJECT_HEADER = [
    "Project", "Current version", "Registration date", "Topic",
    "License", "Status notes", *EVIDENCE_HEADER,
]
HTML_ROOT = ".web/templates"

# No evidence-backed bare-publication or series exceptions approved in PR1.
BARE_EXCEPTIONS = {}

EXEMPT_REASONS = {
    "CHANGELOG.md": "Append-only change history.",
    "TODO.md": "Explicit defect/backlog documentation.",
    "TODO-REFERENCE.md": "Explicit defect/backlog documentation.",
    "governance/register-canonical-citations.md": "Authority parsed separately.",
    "tools/": "Implementation and fixtures.",
    "docs/": "Existing explicit meta-document exemption.",
}


class RegisterError(ValueError):
    pass


def parse_register_text(text):
    lines = text.splitlines()
    entries, seen, section, i = [], {}, "(legacy fixture)", 0

    def cells(raw, line):
        raw = raw.strip()
        if not (raw.startswith("|") and raw.endswith("|")):
            raise RegisterError(
                f"register:{line}: {section}: table row needs outer pipes"
            )
        return [
            c.strip() for c in re.split(r"(?<!\\)\|", raw[1:-1])
        ]

    while i < len(lines):
        raw = lines[i]
        if raw.startswith("## "):
            section = raw[3:].strip()
        if "|" not in raw:
            i += 1
            continue

        # Every table in this authority must have a known schema.
        # A misspelled header cannot silently discard a section.
        header = cells(raw, i + 1)
        tooling = section == "AI security tooling references"
        expected = PROJECT_HEADER if tooling else (
            STANDARD_HEADER if len(header) == 5
            else STANDARD_HEADER + EVIDENCE_HEADER
        )
        if header != expected:
            raise RegisterError(
                f"register:{i + 1}: {section}: malformed header; "
                f"expected {expected!r}, got {header!r}"
            )
        if i + 1 >= len(lines):
            raise RegisterError(f"register:{i + 1}: missing separator")
        sep = cells(lines[i + 1], i + 2)
        if len(sep) != len(header) or not all(
            re.fullmatch(r":?-{3,}:?", c) for c in sep
        ):
            raise RegisterError(
                f"register:{i + 2}: {section}: malformed separator"
            )

        i += 2
        while (
            i < len(lines)
            and lines[i].strip()
            and not lines[i].startswith("#")
        ):
            row = cells(lines[i], i + 1)
            if len(row) != len(header):
                raise RegisterError(
                    f"register:{i + 1}: {section}: "
                    f"expected {len(header)} cells, got {len(row)}"
                )
            if not row[0] or not row[1]:
                raise RegisterError(
                    f"register:{i + 1}: identifier/current version required"
                )
            if not tooling:
                key = _engine().identity_key(row[0])
                if key in seen:
                    raise RegisterError(
                        f"register:{i + 1}: duplicate canonical identity "
                        f"{row[0]!r}; first at {seen[key]}"
                    )
                seen[key] = i + 1
                entries.append(dict(
                    id=row[0],
                    current=row[1],
                    superseded=[] if row[4] in {"", "-", "—"} else [
                        v.strip() for v in row[4].split(",") if v.strip()
                    ],
                    superseded_raw=row[4],
                    section=section,
                    source_line=i + 1,
                    identity_key=key,
                    upstream=row[5] if len(row) == 7 else "",
                    verified=row[6] if len(row) == 7 else "",
                    cells=row,
                ))
            i += 1

    if not entries:
        raise RegisterError("canonical citations register parsed no entries")
    return entries


def parse_canonical_register():
    return parse_register_text(
        CANONICAL_REGISTER.read_text(encoding="utf-8")
    )


def _engine():
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_standards_currency
    return gate_lint_standards_currency


def iter_files(paths, *, explicit=True):
    # Preserve this wrapper API for the scan-scope regression ALLOW map.
    # The shared Markdown helper remains unchanged and Markdown-only.
    from lint_common import is_default_exempt_root, is_adopter_exempt

    root = REPO_ROOT.resolve()
    selected = set()

    def within(path):
        resolved = path.resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            raise OSError(f"out-of-root scan path: {path}") from None
        return resolved

    def excluded(path):
        rel = path.relative_to(root).as_posix()
        return (
            rel in EXEMPT_FILES
            or any(rel.startswith(p) for p in EXEMPT_DIRECTORY_PREFIXES)
            or rel == ".web/dist"
            or rel.startswith(".web/dist/")
            or rel == ".web/templates-v2"
            or rel.startswith(".web/templates-v2/")
            or rel == ".web/templates-v3"
            or rel.startswith(".web/templates-v3/")
            or is_default_exempt_root(path, repo_root=root)
            or is_adopter_exempt(path, repo_root=root)
        )

    def visit(path):
        path = within(path)
        if excluded(path):
            return
        if path.is_dir():
            # scandir surfaces unreadable-directory errors that a glob may
            # silently omit. Resolve every descendant before accepting it.
            import os
            with os.scandir(path) as children:
                for child in sorted(children, key=lambda c: c.name):
                    if child.is_symlink() and child.is_dir():
                        raise OSError(
                            f"directory symlink in scan scope: {child.path}"
                        )
                    visit(Path(child.path))
        elif path.is_file():
            rel = path.relative_to(root).as_posix()
            if path.suffix == ".md" or (
                path.suffix == ".html"
                and rel.startswith(HTML_ROOT + "/")
            ):
                selected.add(path)
        else:
            raise OSError(f"missing/unreadable intended input: {path}")

    for value in paths:
        path = within(root / value)
        if not explicit and not path.exists():
            # Sparse --root fixtures need not create every default root.
            continue
        visit(path)
    return sorted(selected)


def main(argv=None):
    global REPO_ROOT, CANONICAL_REGISTER

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths", nargs="+", default=None)
    parser.add_argument("--root", type=Path)
    parser.add_argument(
        "--coverage-mode", choices=("report", "enforce"), default="report"
    )
    parser.add_argument(
        "--format", choices=("text", "json"), default="text"
    )
    args = parser.parse_args(argv)

    REPO_ROOT = (
        args.root.resolve() if args.root
        else Path(__file__).resolve().parent.parent
    )
    CANONICAL_REGISTER = (
        REPO_ROOT / "governance/register-canonical-citations.md"
    )
    try:
        entries = parse_canonical_register()
        paths = (
            args.paths if args.paths is not None
            else [*DEFAULT_PATHS, HTML_ROOT]
        )
        files = iter_files(paths, explicit=args.paths is not None)
        report = _engine().coverage_report(
            files,
            entries,
            repo_root=REPO_ROOT,
            mode=args.coverage_mode,
            bare_exceptions=BARE_EXCEPTIONS,
        )
        report["scope"] = dict(
            paths=paths,
            explicit=args.paths is not None,
            exclusions=EXEMPT_REASONS,
            omitted=[
                ".web/templates-v2/", ".web/templates-v3/", ".web/dist/",
            ],
            residual=(
                "Regulations, Acts, soft law, tooling, unrecognized prose; "
                "legacy stale checks retained."
            ),
        )
        _engine().print_coverage(
            report, as_json=args.format == "json"
        )
        return report["exit"]
    except RegisterError as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1
    except (OSError, UnicodeError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
