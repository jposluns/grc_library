#!/usr/bin/env python3
"""Static-site generator for the grclibrary.ai public site: the landing, about, pack, and per-domain pages (TODO section 2.4).

WHAT THIS IS. A stdlib-only generator that renders the public site (the landing page,
the about page, the governance-pack page, and one page per corpus domain) from the
LIVE corpus at build time.
There is one source of truth (the corpus); the site is a projection of it. Every
corpus figure on the pages is recomputed here
from ``taxonomy.yml`` (the canonical machine-readable taxonomy, kept in sync with
the corpus by the taxonomy-drift gate) and the library version from ``README.md``.
Nothing is hardcoded; the preview HTML that seeded the templates carried a
point-in-time snapshot that this generator overwrites.

CONTENT BOUNDARY (why this is safe to publish). The generator reads EXACTLY an
explicit allow-list: ``taxonomy.yml``, ``README.md``, each corpus domain's own
``<domain>/README.md`` (for the per-domain page intro), and the page templates
and shared partials under ``.web/templates/``. It never walks the repository and
never reads ``.working/``, ``.claude/``, ``tools/``, ``tests/``, ``.github/``, or
the private sibling repositories. Its only output is the rendered site under
``.web/dist/`` (``index.html``, ``about/index.html``, ``pack/index.html``, and one
``<domain>/index.html`` per corpus domain). So the published surface is those
pages and nothing else; a repo file cannot leak onto the public site through this
generator. The about page's content is static template prose (the maintainer bio
and the acknowledged contributors), not corpus-derived. Each domain page draws
only its intro (the domain README's ``## Purpose`` paragraph, public corpus
content) and its document list (title / type / path from ``taxonomy.yml``, each
linking out to the document's GitHub blob), so the allow-list additions are the
eleven domain READMEs and nothing else.

QUALITATIVE, NOT COUNTED. The automated gating system is described qualitatively
on the page ("comprehensive, continuously-improving", "Continuous"), never as a
gate count: the suite grows continuously and a hardcoded number would understate
it and go stale. This generator therefore computes NO gate count.

OUTPUT IS EPHEMERAL. The rendered ``.web/dist/`` tree is a build artefact, not
committed (it is git-ignored). Only this generator and the templates are committed.

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
TEMPLATES_DIR = WEB_DIR / "templates"
PARTIALS_DIR = TEMPLATES_DIR / "partials"
TAXONOMY = REPO_ROOT / "taxonomy.yml"
README = REPO_ROOT / "README.md"
DEFAULT_OUT = WEB_DIR / "dist"

# Shared chrome injected into every page from a single source, so the pages
# cannot drift. Placeholder name -> partial filename under PARTIALS_DIR. A
# partial may itself carry figure placeholders (CALVER in the topbar,
# DOC_TOTAL / DOMAIN_COUNT in the footer), resolved in render_page()'s 2nd pass.
PARTIALS = {
    "HEAD_STYLE": "head-style.html",
    "TOPBAR": "topbar.html",
    "FOOTER": "footer.html",
    "SCRIPT": "script.html",
}

# The site's pages: (template filename under TEMPLATES_DIR, output path relative
# to the out directory).
PAGES = [
    ("landing.html", "index.html"),
    ("about.html", "about/index.html"),
    ("pack.html", "pack/index.html"),
]

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

# Reading-progression rank for the per-domain document list on each domain page
# (maintainer-directed 2026-07-15, "source + type-priority ordering"): a domain's
# documents read most-foundational-first (govern -> define -> do -> reference), then
# alphabetically by title within a type, instead of alphabetically by type string.
# This MUST stay in sync with ``TYPE_ORDER`` in ``tools/build-taxonomy.py`` (the
# source-side rank that orders taxonomy.yml the same way); the value is replicated
# here rather than imported because this site generator is deliberately standalone
# (stdlib-only, isolated from ``tools/``). A type not listed sorts last (rank = len).
TYPE_ORDER = (
    "Principle", "Charter", "Policy", "Framework", "Standard", "Specification",
    "Procedure", "SOP", "Guide", "Guideline", "Plan", "Roadmap",
    "Matrix", "Register", "Checklist", "Template", "Annex",
)
TYPE_RANK = {t: i for i, t in enumerate(TYPE_ORDER)}

_DOC_RE = re.compile(r'^- path:\s*"(.*)"\s*$')
_DOMAIN_RE = re.compile(r'^  domain:\s*"(.*)"\s*$')
_TYPE_RE = re.compile(r'^  type:\s*"(.*)"\s*$')
_TITLE_RE = re.compile(r'^  title:\s*"(.*)"\s*$')
_CALVER_RE = re.compile(r"^\*\*Library Version:\*\*\s+([0-9]{4}\.[0-9]{2}\.[0-9]+)", re.M)
_PLACEHOLDER_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")

# Per-domain pages link each document out to its source on GitHub (the corpus
# lives there; the site does not recreate rendered document content), and carry a
# canonical URL for SEO. Both are the public repository / site, no secret.
GITHUB_BLOB_BASE = "https://github.com/jposluns/grc_library/blob/main/"
SITE_BASE = "https://grclibrary.ai"


class BuildError(Exception):
    """A corpus-coupling breakage the generator-health check must surface."""


def parse_taxonomy(text):
    """Return a list of {'path','domain','type','title'} dicts from taxonomy.yml.

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
            cur = {"path": m.group(1), "domain": None, "type": None, "title": None}
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
                continue
            mtitle = _TITLE_RE.match(line)
            if mtitle:
                cur["title"] = mtitle.group(1)
    return docs


def read_domain_purpose(domain):
    """Return the ``## Purpose`` intro of ``<domain>/README.md`` as clean plain
    text. Normally that is the section's first paragraph. When the first
    paragraph is a list lead-in (it ends with a colon, the dev-security case),
    the following list items' lead-in sentences are folded in so the page never
    renders a dangling colon. Markdown links, bold, and code spans are flattened.
    Every corpus domain README follows the section model and carries a Purpose
    section; a missing file or missing section is a coupling breakage the
    generator-health check must surface."""
    p = REPO_ROOT / domain / "README.md"
    if not p.is_file():
        raise BuildError(f"domain README not found at {p}")
    # Collect the section's lines (stripped), stopping at the next heading / rule.
    lines = []
    in_purpose = False
    for line in p.read_text(encoding="utf-8").splitlines():
        if not in_purpose:
            if re.match(r"^##\s+Purpose\s*$", line):
                in_purpose = True
            continue
        if line.strip().startswith("## ") or line.strip() == "---":
            break
        lines.append(line.strip())

    i = 0
    while i < len(lines) and not lines[i]:
        i += 1
    para = []
    while i < len(lines) and lines[i]:
        para.append(lines[i])
        i += 1
    if not para:
        raise BuildError(f"{domain}/README.md has no '## Purpose' paragraph")
    intro = " ".join(para)

    if intro.endswith(":"):
        # Fold the following list items' first sentences into the lead-in.
        items = []
        cur = None
        while i < len(lines):
            m = re.match(r"^(?:\d+\.|[-*])\s+(.*)$", lines[i])
            if m:
                if cur is not None:
                    items.append(cur)
                cur = m.group(1)
            elif lines[i] == "":
                pass
            elif cur is not None:
                cur += " " + lines[i]
            else:
                break
            i += 1
        if cur is not None:
            items.append(cur)
        leads = []
        for it in items:
            it = it.replace("**", "").replace("`", "")
            first = re.split(r"(?<=\.)\s", it, maxsplit=1)[0].rstrip(".")
            leads.append(first)
        if leads:
            intro = intro.rstrip(":").rstrip() + ": " + "; ".join(leads) + "."

    return _MD_LINK_RE.sub(r"\1", intro).replace("**", "").replace("`", "")


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

    # Per-domain page data: the domain's document list (title / type / path from
    # the taxonomy, sorted by reading-progression type rank then title) plus its
    # README Purpose intro.
    domain_pages = []
    for domain, count in domains:
        ddocs = [d for d in docs if d["domain"] == domain]
        untitled = [d["path"] for d in ddocs if not d["title"]]
        if untitled:
            raise BuildError(
                f"{len(untitled)} taxonomy entr(y/ies) in domain '{domain}' "
                f"missing a title (schema change?); first: {untitled[0]}"
            )
        ddocs = sorted(ddocs, key=lambda d: (TYPE_RANK.get(d["type"], len(TYPE_ORDER)), d["title"]))
        domain_pages.append(
            {
                "domain": domain,
                "scope": DOMAIN_SCOPE[domain],
                "purpose": read_domain_purpose(domain),
                "docs": ddocs,
                "count": count,
            }
        )

    return {
        "total": total,
        "root_count": root_count,
        "domain_docs": domain_docs,
        "domain_count": domain_count,
        "largest": largest,
        "domains": domains,
        "types": types,
        "calver": calver,
        "domain_pages": domain_pages,
    }


def _esc(s):
    """Minimal HTML escaping for interpolated corpus-derived strings. Escapes the
    double-quote too, so the same helper is safe in an attribute context (a URL
    or value interpolated into ``href="..."`` / ``content="..."``), not only in a
    text node."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_domain_rows(figures):
    rows = []
    largest = figures["largest"]
    for idx, (domain, count) in enumerate(figures["domains"], start=1):
        pct = round(count / largest * 100)
        scope = _esc(DOMAIN_SCOPE[domain])
        rows.append(
            f'            <tr><td class="rg-idx tnum">{idx:02d}</td>'
            f'<td class="rg-name"><a href="/{_esc(domain)}/">{_esc(domain)}</a></td>'
            f'<td class="rg-scope">{scope}</td>'
            f'<td class="rg-count"><span class="bar-wrap">'
            f'<span class="bar" style="width:{pct}%"></span>'
            f'<span class="n">{count}</span></span></td></tr>'
        )
    return "\n".join(rows)


def render_sidenav_domains(figures):
    """The landing-page contents-sidebar domain links (one per domain, register
    order), each to its on-site domain page. Rendered as indented sub-links
    (``class="sub"``) nested under the "By domain" section link, so the nav is a
    two-level quick-nav rather than a separate flat Domains group (TODO 2.16)."""
    return "\n".join(
        f'      <a class="sub" href="/{_esc(domain)}/">{_esc(domain)}</a>'
        for domain, _ in figures["domains"]
    )


def render_type_chips(figures):
    chips = []
    for type_name, count in figures["types"]:
        chips.append(
            f'          <span class="type-chip"><span class="tn">{count}</span>'
            f'<span class="tk">{_esc(type_name)}</span></span>'
        )
    return "\n".join(chips)


def load_partials():
    """Read the shared-chrome partials once. Trailing newlines are stripped so a
    partial drops cleanly onto its own placeholder line."""
    partials = {}
    for key, fname in PARTIALS.items():
        p = PARTIALS_DIR / fname
        if not p.is_file():
            raise BuildError(f"partial not found at {p}")
        partials[key] = p.read_text(encoding="utf-8").rstrip("\n")
    return partials


def render_domain_doc_rows(dp):
    """One list row per document in the domain: a type tag and the document
    title rendered as the link to its source on GitHub, opening in a new tab
    (the corpus lives on GitHub; the site does not recreate rendered document
    content). There is no separate GitHub link, the title is the link."""
    rows = []
    for d in dp["docs"]:
        url = GITHUB_BLOB_BASE + d["path"]
        rows.append(
            f'          <li class="doc-row">'
            f'<span class="doc-type">{_esc(d["type"])}</span>'
            f'<a class="doc-title" href="{_esc(url)}" target="_blank" rel="noopener">'
            f'{_esc(d["title"])}<span class="ext">&#8599;</span></a>'
            f"</li>"
        )
    return "\n".join(rows)


def domain_page_values(dp):
    """The per-page values for one domain page (merged on top of the shared
    values in render_page). SEO/attribute values are built from controlled
    strings (the domain name, the curated scope, the count), never from the
    README prose, so no quote-escaping is needed in the attribute context."""
    name = dp["domain"]
    return {
        "DOMAIN_NAME": _esc(name),
        "DOMAIN_SCOPE_TEXT": _esc(dp["scope"]),
        "DOMAIN_PURPOSE": _esc(dp["purpose"]),
        "DOMAIN_DOC_COUNT": str(dp["count"]),
        "DOMAIN_DOC_ROWS": render_domain_doc_rows(dp),
        "DOMAIN_TITLE": f"{_esc(name)} domain: GRC Library",
        "DOMAIN_SEO_DESC": _esc(
            f"{dp['scope']}. {dp['count']} governance documents in the {name} "
            "domain of the open, CC BY-SA 4.0 GRC Library."
        ),
        "DOMAIN_CANONICAL": f"{SITE_BASE}/{name}/",
    }


def figure_values(figures):
    """The corpus-derived values interpolated into every page."""
    return {
        "CALVER": figures["calver"],
        "DOC_TOTAL": str(figures["total"]),
        "DOMAIN_COUNT": str(figures["domain_count"]),
        "DOMAIN_DOC_TOTAL": str(figures["domain_docs"]),
        "ROOT_COUNT": str(figures["root_count"]),
        "DOMAIN_ROWS": render_domain_rows(figures),
        "TYPE_CHIPS": render_type_chips(figures),
        "SIDENAV_DOMAINS": render_sidenav_domains(figures),
    }


def render_page(template_name, figures, partials, extra=None):
    """Render one page: inject the shared partials, then the corpus figures.

    Two substitution passes, because the partials carry figure placeholders of
    their own (CALVER in the topbar; DOC_TOTAL / DOMAIN_COUNT in the footer). The
    first pass drops the partial text (with its ``{{CALVER}}`` etc. still literal)
    into the page and resolves any figures written directly in the page body; the
    second resolves the figures that arrived via a partial. Returns
    ``(html, used_keys)``."""
    template_path = TEMPLATES_DIR / template_name
    if not template_path.is_file():
        raise BuildError(f"template not found at {template_path}")
    template = template_path.read_text(encoding="utf-8")

    values = {**partials, **figure_values(figures)}
    if extra:
        values.update(extra)
    used = set()

    def sub(match):
        key = match.group(1)
        if key not in values:
            raise BuildError(
                f"template {template_name} has an unknown placeholder {{{{{key}}}}}"
            )
        used.add(key)
        return values[key]

    rendered = _PLACEHOLDER_RE.sub(sub, template)   # pass 1: partials + inline figures
    rendered = _PLACEHOLDER_RE.sub(sub, rendered)   # pass 2: figures arriving via partials

    # No placeholder tokens may survive rendering.
    leftover = _PLACEHOLDER_RE.findall(rendered)
    if leftover:
        raise BuildError(
            f"unrendered placeholder(s) remain in {template_name}: "
            f"{', '.join(sorted(set(leftover)))}"
        )
    return rendered, used


def render_site(figures):
    """Render every page. Returns a list of ``(out_rel, html)``. Enforces that
    every computed value is used by at least one page: a value used by no page is
    a dead computation (or a dropped placeholder), which is a build error."""
    partials = load_partials()
    all_values = set(PARTIALS) | set(figure_values(figures))
    pages = []
    used_across = set()
    for template_name, out_rel in PAGES:
        html, used = render_page(template_name, figures, partials)
        pages.append((out_rel, html))
        used_across |= used

    # One page per corpus domain, from the shared domain template plus that
    # domain's per-page values. The dead-value check below covers the global
    # values (used by the fixed pages); each domain page's own leftover check in
    # render_page guarantees its DOMAIN_* placeholders all resolved.
    for dp in figures["domain_pages"]:
        html, _ = render_page(
            "domain.html", figures, partials, extra=domain_page_values(dp)
        )
        pages.append((f"{dp['domain']}/index.html", html))

    unused = sorted(all_values - used_across)
    if unused:
        raise BuildError(
            "value(s) used by no page (dead computation or a dropped placeholder): "
            f"{', '.join('{{' + k + '}}' for k in unused)}"
        )
    return pages


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Render the grclibrary.ai public site (landing, about, pack, and per-domain pages) from the live corpus.",
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
        # Rendering is part of the health check: it proves every page template
        # still matches the generator's partial and placeholder set.
        pages = render_site(figures)
    except BuildError as e:
        print(f"web-generator FAIL: {e}", file=sys.stderr)
        return 1

    summary = (
        f"web-generator: {figures['total']} documents "
        f"({figures['domain_docs']} across {figures['domain_count']} domains "
        f"+ {figures['root_count']} root), {len(figures['types'])} document types, "
        f"library {figures['calver']}; {len(pages)} pages "
        f"({', '.join(rel for rel, _ in pages)})."
    )

    if args.check:
        print(f"web-generator --check OK: corpus parses and every page renders. {summary}")
        return 0

    out_dir = Path(args.out).resolve() if args.out else DEFAULT_OUT
    written = []
    for out_rel, html in pages:
        out_file = out_dir / out_rel
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html, encoding="utf-8")
        written.append(out_rel)
    print(
        f"web-generator OK: wrote {len(written)} page(s) to {out_dir} "
        f"({', '.join(written)}). {summary}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
