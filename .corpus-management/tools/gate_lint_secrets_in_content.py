#!/usr/bin/env python3
"""Secret-content audit (grc gate): pack-owned engine (source of record).

Scan content for high-confidence secret patterns (cloud keys, provider tokens,
PEM private-key blocks, realistic JWTs). Each pattern requires enough structural
detail to avoid catching documentation prose; the match is redacted to its first
twelve characters in the finding so the linter output never echoes a full value.
Lines inside fenced code blocks are skipped (the shared fence-aware scan), and at
most one finding is reported per line.

Engine/wrapper split (SHARED/SAFETY lane PR-37, Pattern A): this engine carries the
detection vocabulary (``SECRET_PATTERNS``) and the pure ``scan``; the project
wrapper (``tools/lint-secrets-in-content.py``) supplies the grc scan scope (the
scanned-suffix set and the exempt-file set, which includes THIS engine because it
documents the secret formats by design) and the grouped reporting in ``main``, and
keeps a thin module-global ``scan`` shim delegating here so the scan-scope
regression test (which patches ``mod.scan`` and runs ``main``) observes the original
signature and behaviour. The engine's ``scan`` is scope-free and repository-root-free.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_secrets_in_content: cannot import the AIQT generic core (aiqt_corpus); "
        f"the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )


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
