#!/usr/bin/env python3
"""Standards-currency audit: project policy and register parser.

The pack engine owns citation extraction, comparison and reporting.
This wrapper owns the canonical-register schema, roots, exclusions and CLI.

PR1 defaults to report mode. Only the unchanged legacy Markdown stale
check blocks in that mode. New findings are advisory. Explicit enforce
mode supports migration fixtures; no gate invocation enables it in PR1.

3b75: a superseded edition cited as history passes only through a reviewed row
of the TOML data file `.project-governance/register-historical-citation-exceptions.toml`;
everything else keeps blocking. The Markdown page of the same name is a generated view,
never parsed for policy; this gate refuses a page whose generated table differs from the
data (tools/build-historical-citation-exceptions.py regenerates it).

Exit: 0 no blocking findings; 1 blocking findings, a malformed or empty
canonical register, malformed historical register data, or a historical
register page out of step with its data; 2 missing/unreadable intended inputs.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import AUDITED_DOMAIN_DIRS, require_dir  # noqa: E402  # grc-config/store, stays local
import historical_citation_register as HCR  # noqa: E402  # 3b75: the register data and page sync

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
    ".project-governance/register-historical-citation-exceptions.md",
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

# 3b75: the sanctioned historical-context form. A superseded edition cited
# as HISTORY ("the 2019 edition of ISO/IEC 27701 extended ISO/IEC
# 27001:2013") passes only through a reviewed row of the register data file:
# one path, one verbatim whole sentence, one registered superseded citation,
# a reason and upstream evidence. The two wording screens are this project's
# policy vocabulary; they refuse a present-tense claim at parse time, and the
# engine refuses a fragment of a longer sentence at scan time. An absent
# register sanctions nothing, so every stale citation keeps blocking.
HISTORICAL_REGISTER_REL = HCR.PAGE_REL  # the generated view (never parsed for policy)
HISTORICAL_DATA_REL = HCR.DATA_REL  # the rows gate 6 reads
HISTORICAL_REGISTER = REPO_ROOT / HISTORICAL_REGISTER_REL
HISTORICAL_DATA = REPO_ROOT / HISTORICAL_DATA_REL
HISTORICAL_CUE = re.compile(
    r"\b(?:superseded|replaced|withdrawn|revised|previous(?:ly)?"
    r"|former(?:ly)?|prior|earlier|original(?:ly)?|historical(?:ly)?"
    r"|until|then-current|(?:19|20)\d\d edition"
    r"|edition of (?:19|20)\d\d)\b",
    re.I,
)
PRESENT_TENSE = re.compile(
    r"\b(?:is|are|remains?|requires?|mandates?|specif(?:y|ies)|states?"
    r"|defines?|prescribes?|governs?|applies|apply|extends|covers"
    r"|includes|provides|must|shall|should|current(?:ly)?|today|now"
    # 3b75 QA r1 (claude): common present-tense verbs and "still". The screen is a vocabulary
    # heuristic on the declared text only; review of each row is the control.
    r"|still|sets|follows?|lists|contains|has|have|needs|establishes|supports|uses?"
    r"|relies|rely|anchors?|underpins?|forms?|serves?|drives?"
    r"|maps?|aligns?|underlies|implements?"
    # 3b75 QA r7 (claude): further verbs common in compliance writing.
    r"|conforms?|complies|continues?|retains?|references?|cites?|adopts?|operates?|keeps?)\b",
    re.I,
)

EXEMPT_REASONS = {
    "CHANGELOG.md": "Append-only change history.",
    "TODO.md": "Explicit defect/backlog documentation.",
    "TODO-REFERENCE.md": "Explicit defect/backlog documentation.",
    "governance/register-canonical-citations.md": "Authority parsed separately.",
    ".project-governance/register-historical-citation-exceptions.md": (
        "The generated view of the historical-citation exception data; the gate reads the .toml, and checks this page only for sync."
    ),
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
                    superseded=[] if row[4] in {"", "-", "\u2014"} else [
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


def parse_historical_exceptions(text, entries):
    """3b75: load and validate the historical-context exception DATA file (TOML).

    The rows live in a TOML data file (historical_citation_register.load applies the structural
    checks: strict TOML, exact keys, exact types, single-line printable ASCII strings); this
    function applies the policy checks to each row. The Markdown register page is a generated
    view and is never parsed for policy (maintainer ruling 2026-09-26, after ten QA rounds of
    Markdown shapes that rendered differently from what a parser read)."""
    engine, out, seen = _engine(), [], set()
    today = datetime.now(timezone.utc).date()
    try:
        rows = HCR.load(text)
    except HCR.RegisterDataError as exc:
        raise RegisterError(str(exc)) from None
    for n, row in enumerate(rows, 1):
        xid, path, citation, sentence = row["id"], row["path"], row["citation"], row["sentence"]
        reason, upstream, verified = row["reason"], row["upstream"], row["verified"]
        where = f"historical register data: exception {n}: {xid}"
        if not re.fullmatch(r"HCE-\d{3}", xid) or xid in seen:
            raise RegisterError(f"{where}: needs a unique HCE-NNN id")
        seen.add(xid)
        if (path, sentence, citation) in seen:
            # Two rows would sanction the one occurrence twice (3b75 QA r7, claude).
            raise RegisterError(f"{where}: repeats another row's path, sentence and citation")
        seen.add((path, sentence, citation))
        parts = path.split("/")
        if (
            not re.fullmatch(r"[A-Za-z0-9._/-]+\.md", path)
            or any(part in {"", ".", ".."} for part in parts)
        ):
            raise RegisterError(f"{where}: path must be a canonical repo .md path")
        occ = [
            o for o in engine.discover(citation, ".md")
            if o["channel"] == "grammar"
        ]
        if (
            len(occ) != 1
            or occ[0]["span"] != [[1, 1], [1, len(citation)]]
            or [k for k, _ in engine.resolve(
                occ[0], entries, BARE_EXCEPTIONS
            )] != ["STALE"]
        ):
            raise RegisterError(
                f"{where}: citation {citation!r} is not exactly "
                "one registered superseded edition"
            )
        if sentence.count(citation) != 1:
            raise RegisterError(
                f"{where}: sentence must contain the citation verbatim exactly once"
            )
        if not engine.SENTENCE_TEXT.fullmatch(sentence):
            raise RegisterError(
                f"{where}: sentence must be plain text (letters, digits, spaces and . , ; : ' \" "
                "( ) / % -) ending in . ! or ?; no markup, escapes or character references"
            )
        tense = PRESENT_TENSE.search(sentence)
        if tense:
            raise RegisterError(
                f"{where}: present-tense wording {tense[0]!r}; "
                "a current-tense claim cannot be sanctioned"
            )
        if not HISTORICAL_CUE.search(sentence):
            raise RegisterError(
                f"{where}: sentence carries no historical-context cue"
            )
        if len(reason) < 10 or reason.lower() in {"-", "tbd", "n/a"}:
            raise RegisterError(f"{where}: reason required")
        if not re.fullmatch(r"https://[^\s|<>`\\]+", upstream):
            raise RegisterError(
                f"{where}: upstream evidence URL required"
            )
        if verified > today:
            raise RegisterError(
                f"{where}: verified must be a date on or before today (UTC)"
            )
        out.append(dict(
            id=xid, path=path, citation=citation, sentence=sentence,
            reason=reason, identity=occ[0]["identity"],
            edition=engine.edition_key(occ[0]["version"]),
        ))
    return out


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
        # 3b50b1: existence is checked BEFORE the exclusion filter, so a missing explicit path
        # under an excluded prefix is refused rather than silently dropped.
        if not path.exists():
            raise OSError(f"missing/unreadable intended input: {path}")
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
        candidate = root / value
        if candidate.is_symlink() and candidate.is_dir():
            raise OSError(
                f"directory symlink in scan scope: {candidate}"
            )
        path = within(candidate)
        if not explicit and not path.exists():
            # Sparse --root fixtures need not create every default root.
            continue
        visit(path)
    return sorted(selected)


def main(argv=None):
    global REPO_ROOT, CANONICAL_REGISTER, HISTORICAL_REGISTER, HISTORICAL_DATA

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths", nargs="+", default=None)
    parser.add_argument("--root", type=str)
    parser.add_argument(
        "--coverage-mode", choices=("report", "enforce"), default="report"
    )
    parser.add_argument(
        "--format", choices=("text", "json"), default="text"
    )
    args = parser.parse_args(argv)
    if args.root is not None:  # 3b50b2d1: a missing, empty or non-directory --root is refused
        args.root = require_dir(args.root, "--root")
    if args.paths is not None and any(not p.strip() for p in args.paths):
        # 3b50b2d1: an empty --paths entry resolved to the tree root, so the run fell back to a
        # whole-tree scan while reporting an explicit scope.
        print("ERROR: --paths: an empty path entry is refused.", file=sys.stderr)
        return 2

    REPO_ROOT = (
        args.root.resolve() if args.root
        else Path(__file__).resolve().parent.parent
    )
    CANONICAL_REGISTER = (
        REPO_ROOT / "governance/register-canonical-citations.md"
    )
    HISTORICAL_REGISTER = REPO_ROOT / HISTORICAL_REGISTER_REL
    HISTORICAL_DATA = REPO_ROOT / HISTORICAL_DATA_REL
    try:
        entries = parse_canonical_register()
        # Read directly: only a missing file counts as absent, so a permission or other I/O
        # error reaches the exit-2 handler instead of reading as "no register" (3b75 QA, codex:
        # Path.exists() swallows OSError on Python 3.14).
        def _read(path):
            try:
                return path.read_bytes().decode("utf-8")
            except FileNotFoundError:
                return None
        data_text, page = _read(HISTORICAL_DATA), _read(HISTORICAL_REGISTER)
        historical = (
            parse_historical_exceptions(data_text, entries) if data_text is not None else []
        )
        # The page's generated table must match the data (3b75 redesign). With no data file, a
        # page that exists must show the empty table; with a data file, the page must exist.
        if data_text is not None or page is not None:
            rows = HCR.load(data_text) if data_text is not None else []
            problem = HCR.sync_problem(page, rows)
            if problem:
                raise RegisterError(problem)
        paths = (
            args.paths if args.paths is not None
            else [*DEFAULT_PATHS, HTML_ROOT]
        )
        files = iter_files(paths, explicit=args.paths is not None)
        scanned = {f.relative_to(REPO_ROOT).as_posix() for f in files}
        orphans = [h["id"] for h in historical if h["path"] not in scanned]
        if args.paths is None and orphans:
            # A default run scans every sanctioned path; a row naming an
            # unscanned path is stale policy, never a silent pass.
            raise RegisterError(
                "historical exception(s) outside the scan scope: "
                + ", ".join(orphans)
            )
        report = _engine().coverage_report(
            files,
            entries,
            repo_root=REPO_ROOT,
            mode=args.coverage_mode,
            bare_exceptions=BARE_EXCEPTIONS,
            historical_exceptions=historical,
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
