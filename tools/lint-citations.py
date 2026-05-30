#!/usr/bin/env python3
"""Lint framework citations against a curated denylist of hallucinated or stale strings.

This linter exists because the broader text linters cannot detect plausible-looking
but incorrect framework version numbers. The denylist below is hand-curated based on
verified primary sources (ISACA, CSA, NIST, etc.).

Usage:
    python3 tools/lint-citations.py
    python3 tools/lint-citations.py --paths governance ai

Exit codes:
    0   no findings
    1   one or more findings present

Maintenance:
    Add new patterns to DENYLIST when a hallucinated or stale framework string is
    discovered. Add files to PATH_EXEMPTIONS where the literal string must appear
    (e.g. CHANGELOG entries documenting the historical defect).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Each entry: (string-to-find, why-it-is-wrong, suggested-replacement).
# Use plain string matching; if regex is needed, switch to a different field.
DENYLIST: list[tuple[str, str, str]] = [
    (
        "COBIT 2025",
        "Hallucinated framework version. ISACA's current COBIT version is COBIT 2019.",
        "COBIT 2019",
    ),
    (
        "CSA CCM v5",
        "Hallucinated framework version. CSA's current Cloud Controls Matrix version is v4.1.",
        "CSA CCM v4.1",
    ),
    (
        "CCM v5",
        "Hallucinated framework version. CSA's current Cloud Controls Matrix version is v4.1.",
        "CCM v4.1",
    ),
    (
        "NIST AI RMF 1.1",
        "Hallucinated NIST AI RMF version. NIST AI RMF was published as version 1.0; the GenAI Profile is NIST AI 600-1.",
        "NIST AI RMF 1.0 (with AI 600-1 Generative AI Profile)",
    ),
    (
        "AI RMF 1.1",
        "Hallucinated NIST AI RMF version (bare form). NIST AI RMF was published as version 1.0; the GenAI Profile is NIST AI 600-1.",
        "NIST AI RMF 1.0 (with AI 600-1 Generative AI Profile)",
    ),
    (
        "Draft 2026 ISO 37301",
        "Unverified speculative reference. No such revision is published by ISO.",
        "(remove the reference or replace with current ISO 37301:2021)",
    ),
    (
        "IT Operations Documentation Framework",
        "Phantom dependency. No such framework exists in the library; documents previously referencing it now point to operations/framework-it-service-management.md or governance/standard-records-retention-and-destruction.md.",
        "operations/framework-it-service-management.md (or governance/standard-records-retention-and-destruction.md)",
    ),
    (
        "CCM GRM",
        "Stale v3 CCM domain code. v4.1 uses GRC (Governance, Risk, Compliance).",
        "CCM GRC",
    ),
    (
        "CCM EKM",
        "Stale v3 CCM domain code. v4.1 uses CEK (Cryptography, Encryption, Key Management).",
        "CCM CEK",
    ),
    (
        "CCM END",
        "Stale CCM domain code. v4.1 uses UEM (Universal Endpoint Management).",
        "CCM UEM",
    ),
    (
        "CCM TIM",
        "Non-existent CCM domain code. Threat intelligence is part of TVM (Threat and Vulnerability Management) in v4.1.",
        "CCM TVM",
    ),
]

# Paths exempted from each pattern. CHANGELOG is the canonical exemption: historical
# entries record what was committed at the time, including the defects that were later
# corrected. Add as a relative posix path.
PATH_EXEMPTIONS: dict[str, set[str]] = {
    # COBIT 2025 is exempt in documents that legitimately discuss the
    # hallucination warning: CHANGELOG (phase history), this linter (rule
    # definition), canonical-citations register (the warning's source of
    # truth), Q4 worklist (verification campaign), and the Audit Programme
    # Specification (which uses the exemption as a worked example in §8.3).
    "COBIT 2025": {"CHANGELOG.md", "tools/lint-citations.py", "governance/register-canonical-citations.md", "governance/worklist-citation-verification-batch-q4-canonical-citations.md", "governance/specification-audit-programme.md"},
    "CSA CCM v5": {"CHANGELOG.md", "tools/lint-citations.py", "governance/register-canonical-citations.md"},
    "CCM v5": {"CHANGELOG.md", "tools/lint-citations.py", "governance/register-canonical-citations.md"},
    "NIST AI RMF 1.1": {"CHANGELOG.md", "tools/lint-citations.py", "governance/register-canonical-citations.md"},
    "AI RMF 1.1": {"CHANGELOG.md", "tools/lint-citations.py", "governance/register-canonical-citations.md"},
    "Draft 2026 ISO 37301": {"CHANGELOG.md", "tools/lint-citations.py", "governance/register-canonical-citations.md"},
    "IT Operations Documentation Framework": {"CHANGELOG.md", "tools/lint-citations.py", "governance/register-canonical-citations.md"},
    "CCM GRM": {"CHANGELOG.md", "tools/lint-citations.py", "governance/register-canonical-citations.md"},
    "CCM EKM": {"CHANGELOG.md", "tools/lint-citations.py", "governance/register-canonical-citations.md"},
    "CCM END": {"CHANGELOG.md", "tools/lint-citations.py", "governance/register-canonical-citations.md"},
    "CCM TIM": {"CHANGELOG.md", "tools/lint-citations.py", "governance/register-canonical-citations.md"},
}

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
    "ai",
    "architecture",
    "compliance",
    "dev-security",
    "governance",
    "operations",
    "privacy",
    "resilience",
    "risk",
    "sectors",
    "security",
    "supply-chain",
]


def iter_markdown_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = REPO_ROOT / p
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            for f in path.rglob("*.md"):
                files.append(f)
    return sorted(set(files))


def check_file(path: Path) -> list[tuple[str, int, str, str, str]]:
    """Return list of (term, lineno, line, why, suggested_replacement) findings."""
    relative = path.relative_to(REPO_ROOT).as_posix()
    findings: list[tuple[str, int, str, str, str]] = []

    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            for term, why, suggested in DENYLIST:
                if relative in PATH_EXEMPTIONS.get(term, set()):
                    continue
                if term in line:
                    findings.append((term, lineno, line.strip(), why, suggested))

    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Lint framework citations against a denylist.")
    parser.add_argument("--paths", nargs="*", default=DEFAULT_PATHS,
                        help="Paths to scan (files or directories).")
    args = parser.parse_args(argv[1:])

    files = iter_markdown_files(args.paths)
    grouped: dict[str, list[tuple[str, int, str, str, str]]] = {}
    total = 0

    for f in files:
        rel = f.relative_to(REPO_ROOT).as_posix()
        findings = check_file(f)
        if findings:
            grouped[rel] = findings
            total += len(findings)

    if not grouped:
        print("OK: no citation findings.")
        return 0

    for rel, findings in sorted(grouped.items()):
        print(f"=== {rel} ===")
        for term, lineno, line, why, suggested in findings:
            print(f"  L{lineno} [{term}] -> {suggested}")
            print(f"     {why}")
            print(f"     line: {line[:140]}")

    print(f"\nFAIL: {total} citation finding(s) across {len(grouped)} file(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
