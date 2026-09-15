#!/usr/bin/env python3
"""External-link-domain audit (grc gate): pack-owned engine (source of record).

Scan external http(s) URLs and validate each URL's host against a caller-supplied
allow-list of trusted publisher domains (a host matches if it is in the allow-list
or is a subdomain of an allow-listed parent). A URL whose host is not allow-listed
is a finding: an unexpected external domain in published content is a supply-chain
vector for adopters. Lines inside fenced code blocks are skipped (the shared
fence-aware scan).

Engine/wrapper split (SHARED/SAFETY lane PR-40, Pattern A): this engine carries the
URL regex (``URL_RE``), the host matcher (``is_allowed``), and the pure ``scan``; the
project wrapper (``tools/lint-external-link-domains.py``) supplies the grc scan scope
(the scanned-suffix set and the exempt-file set) and the grc publisher allow-list, and
keeps a thin module-global ``scan`` shim delegating here so the scan-scope regression
test (which patches ``mod.scan`` and runs ``main``) observes the original signature and
behaviour. ``scan`` and ``is_allowed`` take ``allow_list`` as a keyword so the engine
carries no grc-specific allow-list; the wrapper supplies it. The engine is scope-free
and repository-root-free.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_external_link_domains: cannot import the AIQT generic core (aiqt_corpus); "
        f"the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )


URL_RE = re.compile(r"https?://([a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})(?::\d+)?(?:/[^\s)\]]*)?")


def is_allowed(host: str, *, allow_list) -> bool:
    h = host.lower().rstrip(".")
    if h in allow_list:
        return True
    # Subdomain match: any parent suffix in the allow-list.
    parts = h.split(".")
    for i in range(len(parts)):
        suffix = ".".join(parts[i:])
        if suffix in allow_list:
            return True
    return False


def scan(path: Path, *, allow_list) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in iter_non_code_lines(text):
        for m in URL_RE.finditer(line):
            host = m.group(1)
            if is_allowed(host, allow_list=allow_list):
                continue
            findings.append((lineno, host))
    return findings
