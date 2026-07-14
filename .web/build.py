#!/usr/bin/env python3
"""Static-site generator for the grclibrary.ai public landing page (TODO section 2.4).

WHAT THIS IS. A stdlib-only generator that renders the public landing page from
the LIVE corpus at build time. There is one source of truth (the corpus); the
site is a projection of it. Every corpus figure on the page is recomputed here
from ``taxonomy.yml`` (the canonical machine-readable taxonomy, kept in sync with
the corpus by the taxonomy-drift gate) and the library version from ``README.md``.
Nothing is hardcoded; the preview HTML that seeded the template carried a
point-in-time snapshot that this generator overwrites.

CONTENT BOUNDARY (why this is safe to publish). The generator reads EXACTLY three
inputs, an explicit allow-list: ``taxonomy.yml``, ``README.md``, and the page
template under ``.web/templates/``. It never walks the repository and never reads
``.working/``, ``.claude/``, ``tools/``, ``tests/``, ``.github/``, or the private
sibling repositories. Its only output is the rendered landing page under
``.web/dist/``. So the published surface is the landing page and nothing else; a
repo file cannot leak onto the public site through this generator.

QUALITATIVE, NOT COUNTED. The automated gating system is described qualitatively
on the page ("comprehensive, continuously-improving", "Continuous"), never as a
gate count: the suite grows continuously and a hardcoded number would understate
it and go stale. This generator therefore computes NO gate count.

OUTPUT IS EPHEMERAL. The rendered ``.web/dist/`` tree is a build artefact, not
committed (it is git-ignored). Only this generator and the template are committed.

USAGE
  python3 .web/build.py            render the site into .web/dist/
  python3 .web/build.py --check    parse-and-compute only, write nothing; exit
                                   non-zero if the corpus it depends on cannot be
                                   parsed (a renamed field, a moved file, a
                                   taxonomy schema change). This is the
                                   generator-health check wired into CI; it is a
                                   coupling-breakage detector, NOT a corpus gate.
  python3 .web/build.py --out DIR  render into DIR instead of .web/dist/
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WEB_DIR = REPO_ROOT / ".web"
TEMPLATE = WEB_DIR / "templates" / "landing.html"
TAXONOMY = REPO_ROOT / "taxonomy.yml"
README = REPO_ROOT / "README.md"
DEFAULT_OUT = WEB_DIR / "dist"

# The eleven corpus domains, with the one-line scope description shown in the
# section-04 register. Curated prose (a scope sentence is not derivable from
# metadata); the COUNTS beside them are always recomputed from the taxonomy.
# A domain present in the taxonomy but missing here is a build error (the
# generator-health check surfaces it), so a new domain cannot be published with
# a blank scope.
DOMAIN_SCOPE = {
    "privacy": "Data protection, privacy engineering, and multi-jurisdiction obligations",
    "ai": "AI governance, assurance, and lifecycle risk controls",
    "security": "Information-security controls, architecture, and operations",
    "governance": "Charters, policies, registers, and the programme operating model",
    "compliance": "Regulatory mapping, control frameworks, and sector audit readiness",
    "operations": "Operational security, monitoring, and IT service management",
    "resilience": "Business continuity, disaster recovery, and incident response",
    "supply-chain": "Third-party, vendor, and supply-chain security management",
    "dev-security": "Secure development lifecycle, CI/CD, and pipeline controls",
    "risk": "Risk methodology, assessment, and treatment",
    "architecture": "Reference architectures and secure-design control patterns",
}

# The taxonomy marks the root-level specification documents with this domain.
ROOT_DOMAIN = "root"

_DOC_RE = re.compile(r'^- path:\s*"(.*)"\s*$')
_DOMAIN_RE = re.compile(r'^  domain:\s*"(.*)"\s*$')
_TYPE_RE = re.compile(r'^  type:\s*"(.*)"\s*$')
_CALVER_RE = re.compile(r"^\*\*Library Version:\*\*\s+([0-9]{4}\.[0-9]{2}\.[0-9]+)", re.M)
_PLACEHOLDER_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


class BuildError(Exception):
    """A corpus-coupling breakage the generator-health check must surface."""


def parse_taxonomy(text):
    """Return a list of {'path','domain','type'} dicts from taxonomy.yml.

    Deliberately a tiny structural parser (the corpus toolchain is stdlib-only,
    no YAML library) tolerant only of the regular one-document-per-block shape
    the generator ``build-taxonomy.py`` emits. A schema change breaks it loudly,
    which is exactly what the generator-health check exists to catch.
    """
    docs = []
    cur = None
    in_docs = False
    for line in text.splitlines():
        if line.rstrip() == "documents:":
            in_docs = True
            continue
        if not in_docs:
            continue
        m = _DOC_RE.match(line)
        if m:
            cur = {"path": m.group(1), "domain": None, "type": None}
            docs.append(cur)
            continue
        if cur is not None:
            md = _DOMAIN_RE.match(line)
            if md:
                cur["domain"] = md.group(1)
                continue
            mt = _TYPE_RE.match(line)
            if mt:
                cur["type"] = mt.group(1)
    return docs


def compute_figures():
    """Read the allow-listed inputs and compute every dynamic value the page
    carries. Raises BuildError on any coupling breakage."""
    if not TAXONOMY.is_file():
        raise BuildError(f"taxonomy not found at {TAXONOMY}")
    if not README.is_file():
        raise BuildError(f"README not found at {README}")

    docs = parse_taxonomy(TAXONOMY.read_text(encoding="utf-8"))
    if not docs:
        raise BuildError(
            "taxonomy parsed to zero documents (schema change or empty list?)"
        )
    missing = [d["path"] for d in docs if not d["domain"] or not d["type"]]
    if missing:
        raise BuildError(
            f"{len(missing)} taxonomy entr(y/ies) missing a domain or type "
            f"(schema change?); first: {missing[0]}"
        )

    total = len(docs)
    by_domain = Counter(d["domain"] for d in docs)
    by_type = Counter(d["type"] for d in docs)

    root_count = by_domain.pop(ROOT_DOMAIN, 0)
    if not by_domain:
        raise BuildError("no non-root domains found in the taxonomy")

    # Every taxonomy domain must have a curated scope line, or the page would
    # publish a blank scope. Surface it as a build error.
    unknown = sorted(set(by_domain) - set(DOMAIN_SCOPE))
    if unknown:
        raise BuildError(
            "taxonomy domain(s) with no scope description in DOMAIN_SCOPE: "
            f"{', '.join(unknown)} (add a scope line to .web/build.py)"
        )

    m = _CALVER_RE.search(README.read_text(encoding="utf-8"))
    if not m:
        raise BuildError("could not read '**Library Version:**' CalVer from README.md")
    calver = m.group(1)

    domain_docs = sum(by_domain.values())
    domain_count = len(by_domain)
    largest = max(by_domain.values())

    # Domains sorted by count descending, then name ascending for a stable order.
    domains = sorted(by_domain.items(), key=lambda kv: (-kv[1], kv[0]))
    # Types sorted by count descending, then name ascending.
    types = sorted(by_type.items(), key=lambda kv: (-kv[1], kv[0]))

    return {
        "total": total,
        "root_count": root_count,
        "domain_docs": domain_docs,
        "domain_count": domain_count,
        "largest": largest,
        "domains": domains,
        "types": types,
        "calver": calver,
    }


def _esc(s):
    """Minimal HTML-text escaping for interpolated corpus-derived strings."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render_domain_rows(figures):
    rows = []
    largest = figures["largest"]
    for idx, (domain, count) in enumerate(figures["domains"], start=1):
        pct = round(count / largest * 100)
        scope = _esc(DOMAIN_SCOPE[domain])
        rows.append(
            f'            <tr><td class="rg-idx tnum">{idx:02d}</td>'
            f'<td class="rg-name">{_esc(domain)}</td>'
            f'<td class="rg-scope">{scope}</td>'
            f'<td class="rg-count"><span class="bar-wrap">'
            f'<span class="bar" style="width:{pct}%"></span>'
            f'<span class="n">{count}</span></span></td></tr>'
        )
    return "\n".join(rows)


def render_type_chips(figures):
    chips = []
    for type_name, count in figures["types"]:
        chips.append(
            f'          <span class="type-chip"><span class="tn">{count}</span>'
            f'<span class="tk">{_esc(type_name)}</span></span>'
        )
    return "\n".join(chips)


def render(figures):
    if not TEMPLATE.is_file():
        raise BuildError(f"template not found at {TEMPLATE}")
    template = TEMPLATE.read_text(encoding="utf-8")

    values = {
        "CALVER": figures["calver"],
        "DOC_TOTAL": str(figures["total"]),
        "DOMAIN_COUNT": str(figures["domain_count"]),
        "DOMAIN_DOC_TOTAL": str(figures["domain_docs"]),
        "ROOT_COUNT": str(figures["root_count"]),
        "DOMAIN_ROWS": render_domain_rows(figures),
        "TYPE_CHIPS": render_type_chips(figures),
    }

    used = set()

    def sub(match):
        key = match.group(1)
        if key not in values:
            raise BuildError(f"template has an unknown placeholder {{{{{key}}}}}")
        used.add(key)
        return values[key]

    rendered = _PLACEHOLDER_RE.sub(sub, template)

    unused = sorted(set(values) - used)
    if unused:
        raise BuildError(
            "template is missing expected placeholder(s): "
            f"{', '.join('{{' + k + '}}' for k in unused)}"
        )
    # No placeholder tokens may survive rendering.
    leftover = _PLACEHOLDER_RE.findall(rendered)
    if leftover:
        raise BuildError(f"unrendered placeholder(s) remain: {', '.join(sorted(set(leftover)))}")
    return rendered


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Render the grclibrary.ai landing page from the live corpus.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="parse-and-compute only; write nothing; non-zero exit on a "
        "corpus-coupling breakage (the CI generator-health check).",
    )
    ap.add_argument(
        "--out",
        default=None,
        help=f"output directory (default: {DEFAULT_OUT.relative_to(REPO_ROOT)})",
    )
    args = ap.parse_args(argv)

    try:
        figures = compute_figures()
        # Rendering is part of the health check: it proves the template still
        # matches the generator's placeholder set.
        html = render(figures)
    except BuildError as e:
        print(f"web-generator FAIL: {e}", file=sys.stderr)
        return 1

    summary = (
        f"web-generator: {figures['total']} documents "
        f"({figures['domain_docs']} across {figures['domain_count']} domains "
        f"+ {figures['root_count']} root), {len(figures['types'])} document types, "
        f"library {figures['calver']}."
    )

    if args.check:
        print(f"web-generator --check OK: corpus parses and the template renders. {summary}")
        return 0

    out_dir = Path(args.out).resolve() if args.out else DEFAULT_OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.html"
    out_file.write_text(html, encoding="utf-8")
    print(f"web-generator OK: wrote {out_file}. {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
