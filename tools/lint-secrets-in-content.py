#!/usr/bin/env python3
"""Detect accidentally-committed secrets in library content.

A CC0 public-domain library leaking real credentials would be a serious
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

The regex set is informed by ClawGuard's published sanitiser-engine
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
import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT, iter_non_code_lines, iter_targets, read_text_safe

DEFAULT_PATHS = [str(REPO_ROOT)]

SCAN_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".toml", ".txt"}

# Files exempt because they document secret formats by design.
EXEMPT_FILES = {
    "lint-secrets-in-content.py",
    # claude-rules/core/secrets.md is the canonical "never hardcode secrets"
    # rule file; it documents the patterns to forbid by showing them in
    # code-block examples.
    "secrets.md",
    # Linter regression tests deliberately embed pattern-shaped strings
    # in fixture content. The test file is itself the canonical place
    # those patterns appear as test inputs.
    "test_linters.py",
}

# High-confidence secret patterns. Each regex requires enough structural
# detail to avoid catching documentation prose. Patterns are
# case-sensitive unless noted.
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "AWS Access Key ID",
        # Real AWS keys are exactly 20 chars: prefix + 16 base32.
        # The prefix is one of: AKIA, AGPA, AIDA, AROA, AIPA, ANPA, ANVA, ASIA, A3T (followed by another letter).
        # We require the FULL 20-char structure to avoid catching the word "AIDA" alone.
        re.compile(r"\b(?:AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}\b"),
    ),
    (
        "GitHub personal access token",
        # ghp_ followed by 36+ alphanumeric chars.
        re.compile(r"\bghp_[A-Za-z0-9]{36,}\b"),
    ),
    (
        "GitHub OAuth token",
        re.compile(r"\bgho_[A-Za-z0-9]{36,}\b"),
    ),
    (
        "GitHub user-to-server token",
        re.compile(r"\bghu_[A-Za-z0-9]{36,}\b"),
    ),
    (
        "GitHub server-to-server token",
        re.compile(r"\bghs_[A-Za-z0-9]{36,}\b"),
    ),
    (
        "GitHub refresh token",
        re.compile(r"\bghr_[A-Za-z0-9]{36,}\b"),
    ),
    (
        "GitLab personal access token",
        re.compile(r"\bglpat-[A-Za-z0-9_\-]{20,}\b"),
    ),
    (
        "Slack token",
        re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}-[A-Za-z0-9\-]{10,}-[A-Za-z0-9\-]{20,}\b"),
    ),
    (
        "Stripe live secret key",
        re.compile(r"\bsk_live_[A-Za-z0-9]{24,}\b"),
    ),
    (
        "Stripe restricted live key",
        re.compile(r"\brk_live_[A-Za-z0-9]{24,}\b"),
    ),
    (
        "SendGrid API key",
        re.compile(r"\bSG\.[A-Za-z0-9_\-]{22}\.[A-Za-z0-9_\-]{43}\b"),
    ),
    (
        "Google API key",
        re.compile(r"\bAIza[A-Za-z0-9_\-]{35}\b"),
    ),
    (
        # Matches any PEM private-key header regardless of algorithm:
        # the algorithm prefix (RSA / DSA / EC / OPENSSH / ENCRYPTED /
        # PGP / future types) varies, but the invariant "PRIVATE KEY"
        # token is what makes the block a secret. Anchoring on that
        # token (with an open-ended uppercase prefix and the optional
        # PGP " BLOCK" suffix) future-proofs against new key types
        # without matching the non-secret PEM blocks that share the
        # same envelope (CERTIFICATE, PUBLIC KEY, DH PARAMETERS).
        # Per RFC 7468, PEM labels are uppercase.
        "Private key block (PEM, any algorithm)",
        re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----"),
    ),
    (
        "JWT (3-part Base64URL with realistic payload)",
        # Header.Payload.Signature: each Base64URL segment at least 16 chars,
        # payload at least 60 chars to filter prose mentions of "JWT".
        re.compile(r"\beyJ[A-Za-z0-9_\-]{16,}\.eyJ[A-Za-z0-9_\-]{60,}\.[A-Za-z0-9_\-]{16,}\b"),
    ),
]


def scan(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in iter_non_code_lines(text):
        for label, pattern in SECRET_PATTERNS:
            m = pattern.search(line)
            if m:
                # Show only first 12 characters of the matched secret to
                # avoid echoing the full value in linter output.
                excerpt = m.group(0)
                redacted = excerpt[:12] + "..." if len(excerpt) > 12 else excerpt
                findings.append((lineno, label, redacted))
                break  # one finding per line
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect accidentally-committed secrets in library content."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(
        args.paths,
        suffixes=SCAN_SUFFIXES,
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
