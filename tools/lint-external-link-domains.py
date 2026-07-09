#!/usr/bin/env python3
"""Validate external URLs against an allow-list of trusted publisher domains.

A library linking to an unexpected domain is a supply-chain attack vector
for adopters. This linter scans all external http(s) URLs in library
content and validates their domains against an allow-list mirroring the
citation-verification publisher allow-list plus accepted reference and
tooling domains.

The allow-list is intentionally broad to accommodate legitimate library
references (publishers, standards bodies, OWASP/NIST/MITRE, common
open-source hosting). New external domains require explicit addition.

Usage:
    python3 tools/lint-external-link-domains.py

Exit codes:
    0   no findings
    1   one or more external URLs to non-allow-listed domains
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT, iter_targets, iter_non_code_lines, read_text_safe

DEFAULT_PATHS = [str(REPO_ROOT)]

SCAN_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".toml", ".txt", ".cff"}

EXEMPT_FILES = {
    "lint-external-link-domains.py",
    # Linter regression tests deliberately embed non-allowlisted
    # example URLs as test inputs.
    "test_linters.py",
}

URL_RE = re.compile(r"https?://([a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})(?::\d+)?(?:/[^\s)\]]*)?")

# Allow-listed domains and parent-domain suffixes. A URL matches if its
# host is in this set or is a subdomain of any entry.
ALLOW_LIST = {
    # Standards publishers
    "iso.org", "iec.ch", "nist.gov", "csrc.nist.gov", "nvlpubs.nist.gov",
    "ieee.org", "standards.ieee.org",
    "ashrae.org", "nfpa.org", "cencenelec.eu", "cen.eu", "cenelec.eu",
    "ietf.org", "rfc-editor.org", "datatracker.ietf.org",
    "w3.org", "oasis-open.org",
    # OWASP / Cloud Security Alliance / ISACA / MITRE
    "owasp.org", "cloudsecurityalliance.org", "isaca.org",
    "attack.mitre.org", "cve.mitre.org", "cwe.mitre.org", "atlas.mitre.org",
    # FedRAMP / US Federal
    "fedramp.gov", "federalregister.gov", "congress.gov", "whitehouse.gov",
    "cisa.gov", "tsa.gov", "dhs.gov", "hhs.gov", "ftc.gov", "sec.gov", "nist.gov",
    # EU / UK / Canada / Other jurisdictions
    "eur-lex.europa.eu", "digital-strategy.ec.europa.eu", "enisa.europa.eu",
    "europa.eu",
    "legislation.gov.uk", "ico.org.uk", "ncsc.gov.uk", "gov.uk",
    "laws-lois.justice.gc.ca", "gazette.gc.ca", "priv.gc.ca", "cyber.gc.ca", "canada.ca",
    "legisquebec.gouv.qc.ca",
    "wcoomd.org", "icao.int", "imo.org", "bis.org", "nerc.com",
    "aicpa.org", "aicpa-cima.com",
    "gov.br", "planalto.gov.br", "pdpc.gov.sg", "oaic.gov.au",
    "admin.ch", "edoeb.admin.ch", "npc.gov.cn", "sdaia.gov.sa",
    # Internet Archive (third-party anchor)
    "web.archive.org",
    # OSS hosting
    "github.com", "raw.githubusercontent.com", "huggingface.co", "pypi.org",
    "gitlab.com",
    # Citation / DOI / ORCID
    "doi.org", "orcid.org", "arxiv.org",
    # AI/ML safety bodies
    "aisi.org.uk", "inspect.aisi.org.uk", "mlcommons.org", "avidml.org",
    # OWASP GenAI subdomain
    "genai.owasp.org",
    # Adopted references mentioned in library content
    "keepachangelog.com", "semver.org", "spdx.org", "calver.org",
    "creativecommons.org",
    # Library maintainer documentation
    "claude.ai",
    # Anthropic Claude Code official documentation domain
    "code.claude.com",
    # Common Linux Foundation domains
    "linuxfoundation.org", "openssf.org", "slsa.dev", "cncf.io",
    # AI runtime / observability project canonical homes
    "promptfoo.dev",
    # Schema.org and JSON schema
    "schema.org", "json-schema.org",
    # SANS / CIS
    "sans.org", "cisecurity.org",
    # Library maintainer profile
    "linkedin.com",
    # Google Secure AI Framework
    "saif.google",
    # Anthropic Claude documentation
    "anthropic.com",
    # Commercial AI security vendors referenced in the tooling landscape register
    "lakera.ai", "promptarmor.com", "hiddenlayer.com",
    "calypsoai.com", "mindgard.ai", "splx.ai",
    # (Phase 23.63 removed checkpoint.com and zscaler.com from the
    # "other commercial security vendors that may be referenced"
    # block — neither was cited in any document and the library is
    # vendor-neutral; if a future citation needs one, re-add via PR
    # with justification.)
    # Additional publisher canonical domains (Q4 worklist coverage)
    "oag.ca.gov",  # California Attorney General
    "dodcio.defense.gov",  # US DoD CIO
    "parl.ca",  # Canadian Parliament
    "fedlex.admin.ch",  # Swiss federal legislation
    "harmbench.org",  # HarmBench official site
    "owaspsamm.org",  # OWASP SAMM official site
    "wbasco.org",  # WBASCO (Western Business Alliance Security Council)
    "cbp.gov",  # US Customs and Border Protection
    "pcisecuritystandards.org",  # PCI Security Standards Council
    "oecd.ai", "oecd.org",  # OECD
    "wto.org",  # World Trade Organization
    # Canonical-citations register Upstream check location URLs (register v1.5.7)
    "govinfo.gov",  # US Government Publishing Office (public laws: HITECH, SOX)
    "ilga.gov",  # Illinois General Assembly (BIPA)
    "leg.colorado.gov",  # Colorado General Assembly (Colorado AI Act / SB 24-205 / SB 26-189)
    "cac.gov.cn",  # Cyberspace Administration of China (cross-border data provisions)
    "legislation.gov.au",  # Australian Federal Register of Legislation (Privacy Act)
    "pdp.gov.my",  # Malaysia Personal Data Protection Department (PDPA)
    "linddun.org",  # LINDDUN privacy threat-modelling (KU Leuven imec-DistriNet)
    "ukgovernmentbeis.github.io",  # UK AISI inspect_evals catalogue (GitHub Pages)
    # Canonical-citations register Upstream check location URLs (register v1.5.17, TODO 1.5 currency sweep)
    "ecfr.gov",  # US Electronic Code of Federal Regulations (CMMC 32 CFR 170 / 48 CFR DFARS acquisition rule)
    "pib.gov.in",  # India Press Information Bureau (DPDP Rules 2025 notification)
}


def is_allowed(host: str) -> bool:
    h = host.lower().rstrip(".")
    if h in ALLOW_LIST:
        return True
    # Subdomain match: any parent suffix in the allow-list.
    parts = h.split(".")
    for i in range(len(parts)):
        suffix = ".".join(parts[i:])
        if suffix in ALLOW_LIST:
            return True
    return False


def scan(path: Path) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in iter_non_code_lines(text):
        for m in URL_RE.finditer(line):
            host = m.group(1)
            if is_allowed(host):
                continue
            findings.append((lineno, host))
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate external URLs against the publisher allow-list."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(
        args.paths,
        suffixes=SCAN_SUFFIXES,
        exempt_files=EXEMPT_FILES,
    )
    grouped: dict[Path, list[tuple[int, str]]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: all external URLs are on the allow-list (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        # Deduplicate per file
        seen_hosts = set()
        for lineno, host in findings:
            if host in seen_hosts:
                continue
            seen_hosts.add(host)
            print(f"  L{lineno} [external-link-domain] {host}")
            total += 1
    print(f"\nFAIL: {total} non-allow-listed domain(s) across {len(grouped)} file(s).")
    print(
        "External URLs must point to allow-listed domains. If the reference "
        "is legitimate, add the domain to ALLOW_LIST in lint-external-link-"
        "domains.py and update the citation-verification specification "
        "publisher allow-list (§7) where appropriate."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
