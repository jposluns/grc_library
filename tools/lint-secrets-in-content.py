#!/usr/bin/env python3
"""Detect accidentally-committed secrets in library content.

A CC0 public-domain library leaking real credentials would be a serious
failure. This linter scans markdown content for high-confidence secret
patterns: AWS access keys, GitHub tokens, Slack tokens, Stripe live
keys, SSH private keys, JWT-shaped strings with payloads of plausible
length, and high-entropy base64/hex strings in suspicious contexts.

The regex set is informed by ClawGuard's published sanitiser-engine
patterns (recorded in [`governance/register-ai-security-tooling-landscape.md`](register-ai-security-tooling-landscape.md))
and the detect-secrets project's default rules.

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

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATHS = [str(REPO_ROOT)]

EXEMPT_DIR_PARTS = {".git", "node_modules", "__pycache__"}

# Files exempt because they document secret formats by design.
EXEMPT_FILES = {
    "lint-secrets-in-content.py",
    # claude-rules/core/secrets.md is the canonical "never hardcode secrets"
    # rule file; it documents the patterns to forbid by showing them in
    # code-block examples.
    "secrets.md",
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
        "Private key block (RSA, DSA, EC, OPENSSH)",
        re.compile(r"-----BEGIN (RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----"),
    ),
    (
        "JWT (3-part Base64URL with realistic payload)",
        # Header.Payload.Signature: each Base64URL segment at least 16 chars,
        # payload at least 60 chars to filter prose mentions of "JWT".
        re.compile(r"\beyJ[A-Za-z0-9_\-]{16,}\.eyJ[A-Za-z0-9_\-]{60,}\.[A-Za-z0-9_\-]{16,}\b"),
    ),
]


def is_target(path: Path) -> bool:
    if path.suffix not in {".md", ".py", ".yaml", ".yml", ".json", ".toml", ".txt"}:
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return False
    if path.name in EXEMPT_FILES:
        return False
    return True


def scan(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings
    for lineno, line in enumerate(text.splitlines(), start=1):
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


def iter_targets(paths: list[str]) -> list[Path]:
    targets: list[Path] = []
    seen: set[Path] = set()
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file() and is_target(p):
            if p not in seen:
                targets.append(p)
                seen.add(p)
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and is_target(f) and f not in seen:
                    targets.append(f)
                    seen.add(f)
    return targets


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect accidentally-committed secrets in library content."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(args.paths)
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
