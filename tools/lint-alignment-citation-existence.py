#!/usr/bin/env python3
"""Fabricated alignment-citation existence audit - grc wrapper over the pack engine.

Flag a citation to a NIST Privacy Framework, OWASP ASVS or MITRE CWE identifier that exists
in no held edition of its framework's catalogue (a fabricated code). ASVS requirement and
section identifiers are checked only in ASVS context (see the engine); CWE identifiers
everywhere. Report-only by default; --strict
makes it a blocking gate.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan (the PF
identifier/range regexes, _check_pf, check_file) is the source of record in the pack
engine (.corpus-management/tools/gate_lint_alignment_citation_existence.py); it is
catalogue-free and takes the framework catalogue via configure(ref). This wrapper
imports the alignment_citation_reference registry, derives the valid-identifier union
and the framework name, configures the engine, and keeps EXEMPT_SUFFIXES, a
module-global check_file shim, main, and the exit codes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # own dir on sys.path (programmatic-load safe)
import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path (engine imports aiqt_corpus)
from lint_common import guard_explicit_paths_cwd, REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local
from alignment_citation_reference import REGISTRY, PF_ALL_EDITIONS_VALID, ASVS, CWE  # noqa: E402  # grc factual registry

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

# Markdown files where a code-shaped string is historical description / an example, not
# a live citation. (The walker is iter_markdown_targets, so only .md files reach here;
# the registry and this lint are .py and are never scanned.)
EXEMPT_SUFFIXES = (
    "CHANGELOG.md",
    "governance/specification-audit-programme.md",        # gate-description prose uses example codes
    "governance/specification-citation-verification.md",  # ditto
)


# The PF 1.0 edition entry supplies the framework name and counts; validation uses the union below.
_PF = REGISTRY["nist-privacy-framework-1.0"]
# Validate against the UNION of every held Privacy Framework edition (1.0 + 1.1 IPD), so a
# legitimate 1.1-only code is not false-flagged; only a code absent from ALL editions is fabricated.
_PF_ALL = PF_ALL_EDITIONS_VALID
_PF_NAME = _PF["name"]  # edition-agnostic; validated vs the union of held editions


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_alignment_citation_existence  # the pack-owned engine (source of record)
    return gate_lint_alignment_citation_existence


# Configure the engine ONCE with the grc framework catalogue (validated vs the union
# of every held Privacy Framework edition).
import types  # noqa: E402
_engine().configure(types.SimpleNamespace(
    pf_all=_PF_ALL, pf_name=_PF_NAME,
    asvs_req=ASVS["requirements"], asvs_sec=ASVS["sections"], asvs_name=ASVS["name"],
    asvs_edition=ASVS["edition"],
    cwe_all=CWE["all"], cwe_name=CWE["name"],
))


def check_file(path: Path, rel: str) -> list[str]:
    """Thin shim delegating to the pack engine's pure scan (engine already configured);
    kept module-global so the scan-scope regression meta-test can call it."""
    return _engine().check_file(path, rel)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Fabricated alignment-citation existence audit.")
    ap.add_argument("paths", nargs="*", default=None,
                    help="files or directories to scan (default: the whole repository)")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on any fabricated code (blocking-gate mode); default is report-only (exit 0)")
    args = ap.parse_args(argv[1:])
    # 3b48: explicit paths are refused when missing or outside this tree, else normalized.
    args.paths = guard_explicit_paths_cwd(args.paths, repo_root=REPO_ROOT) if args.paths else [str(REPO_ROOT)]
    findings: list[str] = []
    for path in iter_markdown_targets(args.paths or [str(REPO_ROOT)]):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel.endswith(EXEMPT_SUFFIXES):
            continue
        findings.extend(check_file(path, rel))
    if findings:
        label = "FAIL" if args.strict else "REPORT"
        print(f"{label}: fabricated alignment citation(s) found ({len(set(findings))}):")
        for f in sorted(set(findings)):
            print(f"  - {f}")
        print(f"\nEach cites an identifier absent from every held edition of its framework's catalogue. "
              f"Correct to an existing identifier that fits the row.")
        return 1 if args.strict else 0
    print(f"OK: all alignment citations exist in a held edition of their framework "
          f"(coverage: {_PF_NAME}, 1.0 core + 1.1 IPD, validated as a union; {ASVS['name']} "
          f"requirements and sections in ASVS context; {CWE['name']} weaknesses).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
