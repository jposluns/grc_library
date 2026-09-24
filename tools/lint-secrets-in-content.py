#!/usr/bin/env python3
"""Detect accidentally-committed secrets in library content.

An openly-published (CC BY-SA 4.0) library leaking real credentials would be a serious
failure. This linter scans markdown content for high-confidence secret
patterns. The pattern families currently implemented (SECRET_PATTERNS):

  - AWS access key IDs (AKIA / AGPA / AIDA / AROA / AIPA / ANPA / ANVA /
    ASIA prefix + 16 chars).
  - GitHub tokens: classic personal (ghp_), OAuth (gho_), user-to-server
    (ghu_), server-to-server (ghs_), and refresh (ghr_).
  - GitLab personal access tokens (glpat- prefix).
  - Slack tokens (xoxb / xoxa / xoxp / xoxr / xoxs).
  - Stripe live keys (sk_live_ and rk_live_ restricted variants).
  - SendGrid API keys (SG.<22>.<43> pattern).
  - Google API keys (AIza prefix + 35 chars).
  - Private-key PEM headers (RSA, DSA, EC, OPENSSH, PGP).
  - JWT-shaped strings with plausibly long header / payload / signature.

The regex set is informed by ClawGuard's published sanitizer-engine
patterns (recorded in [`governance/register-ai-security-tooling-landscape.md`](register-ai-security-tooling-landscape.md))
and the detect-secrets project's default rules. No entropy-based check
is implemented; every pattern requires a structural prefix to avoid
prose-text false positives.

The linter is deliberately conservative: each pattern requires enough
structural detail to avoid false positives on library prose discussing
secret formats. The dev-security standards and the AI security standard
discuss secrets at length; they exempt themselves only where they
contain documentation-format examples.

Usage:
    python3 tools/lint-secrets-in-content.py
    python3 tools/lint-secrets-in-content.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more suspected secret patterns present
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import guard_explicit_paths_cwd, REPO_ROOT, iter_targets  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]

SCAN_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".toml", ".txt"}

# Files exempt because they document secret formats by design.
EXEMPT_FILES = {
    "lint-secrets-in-content.py",
    # guardrails/core/secrets.md is the canonical "never hardcode secrets"
    # rule file; it documents the patterns to forbid by showing them in
    # code-block examples.
    "secrets.md",
    # Linter regression tests deliberately embed pattern-shaped strings
    # in fixture content. The test file is itself the canonical place
    # those patterns appear as test inputs.
    "test_linters.py",
    # The gate-mutation probe's variant library deliberately embeds
    # pattern-shaped payloads (an AWS documentation-format example key,
    # dash characters) as the defect strings the probe seeds into a
    # disposable repo copy to test each gate's detection width. Same
    # rationale as test_linters.py: the fixture is the canonical place
    # those patterns appear as probe inputs.
    "gate-mutation-variants.json",
    # The pack-owned engine (gate_lint_secrets_in_content.py) now holds the
    # SECRET_PATTERNS, so it documents the secret formats by design exactly as
    # this wrapper did before the PR-37 transfer; exempt it for the same reason.
    "gate_lint_secrets_in_content.py",
}


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_secrets_in_content  # the pack-owned engine (source of record)
    return gate_lint_secrets_in_content


def scan(path: Path) -> list[tuple[int, str, str]]:
    """Thin shim delegating to the pack engine's pure check.

    Kept in the wrapper as a module-global because the scan-scope regression
    test patches ``mod.scan`` and runs ``main``; the SECRET_PATTERNS and the
    check live in the pack engine (gate_lint_secrets_in_content.py).
    """
    return _engine().scan(path)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect accidentally-committed secrets in library content."
    )
    parser.add_argument("paths", nargs="*", default=None)
    args = parser.parse_args(argv[1:])
    # 3b48: explicit paths are refused when missing or outside this tree, else normalized.
    args.paths = guard_explicit_paths_cwd(args.paths, repo_root=REPO_ROOT) if args.paths else DEFAULT_PATHS
    targets = iter_targets(
        args.paths,
        suffixes=SCAN_SUFFIXES,
        exclude_default_roots=False,  # Preserve source-tree safety coverage.
        exempt_files=EXEMPT_FILES,
    )
    grouped: dict[Path, list[tuple[int, str, str]]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: no suspected secret patterns (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for lineno, label, redacted in findings:
            print(f"  L{lineno} [secret-pattern] {label}: {redacted}")
        total += len(findings)
    print(f"\nFAIL: {total} suspected secret(s) across {len(grouped)} file(s).")
    print(
        "Possible accidentally-committed secrets detected. Investigate each "
        "finding: if a real secret was committed, rotate it immediately and "
        "purge from git history. If the match is documentation prose, change "
        "the example value to one that does not match the secret pattern."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
