#!/usr/bin/env python3
"""Static-site generator for the grclibrary.ai public site: the landing, about, pack, per-domain, and per-type pages, plus the non-indexable staging trees (/v2 executive routes; the /v3 need-based path routes, the /v3 on-site document pages, one per domain document, root specs excepted, the /v3 client-side search, and the /v3 executive reading room).

WHAT THIS IS. A stdlib-only generator that renders the public site (the landing page,
the about page, the governance-pack page, one page per corpus domain, and one listing
page per document type) from the LIVE corpus at build time.
There is one source of truth (the corpus); the site is a projection of it. Every
corpus figure on the pages is recomputed here
from ``taxonomy.yml`` (the canonical machine-readable taxonomy, kept in sync with
the corpus by the taxonomy-drift gate), the library version from ``README.md``,
and, on the v2 and v3 staging domain pages, the published leadership-page listing from
``narrative.yml`` (the generated executive-narrative registry).
Nothing is hardcoded; the preview HTML that seeded the templates carried a
point-in-time snapshot that this generator overwrites.

CONTENT BOUNDARY (why this is safe to publish). The generator reads EXACTLY an
explicit allow-list: ``taxonomy.yml``, ``narrative.yml`` (the committed generated
narrative registry, joined at render time into each v2 and v3 staging domain
page's leadership-page list), ``README.md``, each corpus domain's own
``<domain>/README.md`` (for the per-domain page intro), and the page templates and
shared partials under each variant's template tree (``.web/templates/`` and the
non-indexable ``.web/templates-v2/`` and ``.web/templates-v3/`` staging copies). It never walks the repository and
never reads ``.working/``, ``.claude/``, ``tools/``, ``tests/``, ``.github/``, or
the private sibling repositories. (Under ``--check`` it additionally reads the
committed ``.web/corpus-link-manifest.md`` and self-scans this generator source for
the safeguard checks; neither feeds published content.) By default its rendered output is the site under
``.web/dist/`` (``--out DIR`` redirects it) (``index.html``, ``about/index.html``, ``pack/index.html``,
``for-ai/index.html``, one ``<domain>/index.html`` per corpus domain, one
``types/<slug>/index.html`` per document type, and the three generated files
``robots.txt``, ``sitemap.xml``, and ``llms.txt``); it also writes the committed ``.web/corpus-link-manifest.md`` (a generated artefact outside the ephemeral ``dist/`` tree). So the
published surface is those root pages and files, plus the non-indexable staging
variants' trees under ``.web/dist/v2/`` and ``.web/dist/v3/`` (both noindex); v2 additionally carries the
executive-shell routes declared in ``V2_EXTRA_PAGES`` (decisions, start, trust,
coverage, library, how-its-built), v3 additionally carries the need-based path
routes declared in ``V3_EXTRA_PAGES`` (decide, govern, comply, solutions,
policies, plus the client-side search page), while v2 AND v3 both carry the executive reading room (one on-site page
per registry-listed narrative page: ALL 18 published narrative pages across the
six narrative types render at ``decisions/<subtype>/<slug>/``, each from the
page's Markdown source by the constrained stdlib renderer below; v2's discovery
rows and hand-curated decisions page link to these on-site routes, and on v3 the
Decide and Solutions pages link them on-site and every narrative is reachable
from its domain page); a repo file cannot
leak onto the public site through this generator: the reading room reads ONLY
registry-listed sources admitted by the renderer-confinement validator
(``narrative_source_file``: a normalized repo-relative regular file under
``executive/`` only, git-tracked; absolute paths, parent-directory traversal,
symlinks, duplicates, and untracked sources are all rejected loudly; the
tracked-path authority is one ``git ls-files`` call returning paths, never content). The about page and the For-AI
page are static template prose (the maintainer bio and acknowledged contributors;
and, for For-AI, descriptive guidance plus a resource index whose links point at
public corpus artefacts on GitHub), not corpus-derived. ``robots.txt`` welcomes
AI/search crawlers, ``sitemap.xml`` lists the indexable root variant's rendered pages, and ``llms.txt`` is
a curated Markdown map of public corpus artefacts. Each domain page draws its
intro (the domain README's ``## Purpose`` paragraph, public corpus content) and
its document list (title / type / path from ``taxonomy.yml``, each linking to its
on-site document page on v3, or the document's GitHub blob on the frozen v1/v2
trees and for root specifications); the v2 and v3 staging domain pages additionally list the
published leadership (executive-narrative) pages that touch the area, joined at
render time from ``narrative.yml``. The allow-list additions are the eleven
domain READMEs, ``narrative.yml``, and, for the v2 and v3 reading rooms, the
registry-listed ``executive/`` narrative sources (each admitted only through the
renderer-confinement validator above).

QUALITATIVE, NOT COUNTED. The automated gating system is described qualitatively
on the page ("comprehensive, continuously-improving", "Continuous"), never as a
gate count: the suite grows continuously and a hardcoded number would understate
it and go stale. This generator therefore computes NO gate count.

OUTPUT IS EPHEMERAL. The rendered ``.web/dist/`` tree is a build artefact, not
committed (it is git-ignored). The generator, the templates, and the generated ``.web/corpus-link-manifest.md`` are committed (the manifest is a generated artefact like ``taxonomy.yml``, refreshed on every normal build).

USAGE
  python3 .web/build.py            render the site into .web/dist/
  python3 .web/build.py --check    parse-and-compute only, write nothing; exit
                                   non-zero if the corpus it depends on cannot be
                                   parsed (a renamed field, a moved file, a
                                   taxonomy schema change). This is the
                                   generator-health check wired into CI; it is a
                                   coupling-breakage detector, NOT a corpus gate. It ALSO fails on a stale committed ``corpus-link-manifest.md``, a hardcoded CalVer literal in a template, or a root-relative href that skips the ``{{BASE}}`` token.
  python3 .web/build.py --out DIR  render into DIR instead of .web/dist/
"""

from __future__ import annotations

import argparse
import posixpath
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
WEB_DIR = REPO_ROOT / ".web"
TAXONOMY = REPO_ROOT / "taxonomy.yml"
# The committed generated narrative registry (like taxonomy.yml, a generated
# artefact regenerated by its own tool and gated for drift): the machine-readable
# inventory of the published executive narrative pages. The two registries join
# only at render time (specification-executive-narrative.md), here into the
# per-domain leadership-page listing the v2 and v3 domain templates consume.
NARRATIVE_REGISTRY = REPO_ROOT / "narrative.yml"
README = REPO_ROOT / "README.md"
DEFAULT_OUT = WEB_DIR / "dist"
# The committed web-to-corpus link manifest (a generated artefact like
# taxonomy.yml / docs/portal.md, NOT part of the ephemeral dist/ tree): every
# corpus/GitHub target the indexable root variant's pages link, with its website location and link text.
# Gate 75 (tools/lint-web-corpus-links.py) resolves its targets against the repo.
CORPUS_LINK_MANIFEST = WEB_DIR / "corpus-link-manifest.md"


class Variant(NamedTuple):
    """One independently rendered public-site tree."""

    name: str
    template_source_dir: str
    url_prefix: str
    indexable: bool = False
    # Extra (template, out_rel) pages this variant renders on TOP of the shared
    # PAGES set. A non-indexable staging variant uses this to carry routes the
    # frozen root does not yet have, without touching PAGES (which is shared, so
    # a root render stays byte-for-byte unchanged). Empty for the root variant.
    extra_pages: tuple = ()
    # Whether this variant renders the executive reading room (the on-site
    # narrative routes generated from the registry). VARIANT-SCOPED by this
    # table flag, so the frozen root's page loop is untouched (the
    # byte-identical-root mechanism for the new route class): the root variant
    # keeps the default False and renders exactly the page set it always has.
    narrative_routes: bool = False
    # Whether this variant renders the on-site document (L2) pages, one per
    # corpus document from the enriched taxonomy. VARIANT-SCOPED like
    # narrative_routes so the frozen root/v2 trees are untouched.
    document_routes: bool = False


# Executive routes that exist ONLY on the non-indexable /v2 staging tree (wave 1
# of the executive-site rework). These render in addition to PAGES for v2 alone,
# so the frozen root (v1) is unaffected and stays byte-identical to its baseline.
# They inherit the noindex + self-canonical + /v2/-prefixed treatment every v2
# page gets. Discovery files (robots/sitemap/llms.txt) are emitted for the
# indexable variant only, so these routes stay out of them automatically.
V2_EXTRA_PAGES = (
    ("decisions.html", "decisions/index.html"),
    ("start.html", "start/index.html"),
    ("trust.html", "trust/index.html"),
    ("coverage.html", "coverage/index.html"),
    ("library.html", "library/index.html"),
    ("how-its-built.html", "how-its-built/index.html"),
)

# The five need-based path routes (plus the client-side search page) that exist ONLY
# on the non-indexable /v3 staging tree (PR-B of the ground-up redesign). The
# landing's path cards and the v3 topnav link these routes; each opens on one
# plain question and routes to content that already renders in v3 (the
# per-domain and per-type pages) or to the corpus on GitHub. They render in
# addition to PAGES for v3 alone, so v1 and v2 are unaffected and stay
# byte-identical to their baselines. They inherit the noindex + self-canonical
# + /v3/-prefixed treatment every v3 page gets, and stay out of the discovery
# files (robots/sitemap/llms.txt), which are emitted for the indexable variant
# only.
V3_EXTRA_PAGES = (
    ("decide.html", "decide/index.html"),
    ("govern.html", "govern/index.html"),
    ("comply.html", "comply/index.html"),
    ("solutions.html", "solutions/index.html"),
    ("policies.html", "policies/index.html"),
    ("search.html", "search/index.html"),
)

# The site variant table: one indexable root variant (v1) plus any non-indexable
# staging variants (v2 and v3). New staging variants belong in this table, so
# the template source, URL prefix, and indexability policy stay coupled.
VARIANTS = (
    Variant("v1", "templates", "", indexable=True),
    Variant("v2", "templates-v2", "v2/", indexable=False, extra_pages=V2_EXTRA_PAGES,
            narrative_routes=True),
    Variant("v3", "templates-v3", "v3/", indexable=False,
            extra_pages=V3_EXTRA_PAGES, document_routes=True, narrative_routes=True),
)

# Shared chrome injected into every page from a single source, so the pages
# cannot drift. Placeholder name -> partial filename under a variant's template
# tree. A partial may itself carry figure placeholders (CALVER in the topbar,
# DOC_TOTAL / DOMAIN_COUNT in the footer), resolved in render_page()'s 2nd pass.
PARTIALS = {
    "HEAD_STYLE": "head-style.html",
    "TOPBAR": "topbar.html",
    "FOOTER": "footer.html",
    "SCRIPT": "script.html",
}

# The site's pages: (template filename under a variant's template tree, output
# path relative to that variant's output directory).
PAGES = [
    ("landing.html", "index.html"),
    ("about.html", "about/index.html"),
    ("pack.html", "pack/index.html"),
    ("for-ai.html", "for-ai/index.html"),
]

# AI and search crawlers explicitly welcomed in robots.txt (documenting intent;
# a trailing wildcard group allows everyone, but naming the known AI/training
# crawlers records that this openly-licensed corpus welcomes them and overrides
# any restrictive platform-managed default). Order is alphabetical.
AI_CRAWLER_USER_AGENTS = (
    "AI2Bot", "Amazonbot", "anthropic-ai", "Applebot", "Applebot-Extended",
    "Bytespider", "CCBot", "ChatGPT-User", "Claude-User", "Claude-Web",
    "ClaudeBot", "cohere-ai", "Diffbot", "DuckAssistBot", "FacebookBot",
    "Google-Extended", "GPTBot", "Meta-ExternalAgent", "OAI-SearchBot",
    "PerplexityBot", "Perplexity-User", "Timpibot", "YouBot",
)

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

# One-line description per document TYPE, shown as the intro on each per-type
# listing page (the /types/<slug>/ pages the "By document type" chips link to).
# A type present in the taxonomy but missing here is a build error (mirrors the
# DOMAIN_SCOPE completeness check). Descriptions of the pairs the ingestion spec
# distinguishes (Procedure/SOP, Plan/Roadmap, Guideline/Guide, Template) follow
# specification-ingestion.md "Type selection guidance"; the rest describe how the
# corpus uses the type.
TYPE_SCOPE = {
    "Standard": "Normative control requirements that policies delegate to and audits test against",
    "Procedure": "Multi-actor, cross-functional workflows that coordinate several roles",
    "Annex": "Jurisdiction- and sector-specific overlays that extend a parent document",
    "Register": "Living inventories of record: assets, risks, controls, and decisions",
    "Template": "Reusable blank skeletons meant to be copied into working instances",
    "Framework": "Organizing structures that arrange controls, functions, and lifecycles",
    "Policy": "Governing intent and mandatory direction the rest of the corpus implements",
    "Guideline": "Advisory interpretation of a policy or standard requirement",
    "Plan": "Event-triggered or schedule-bound coordination such as incident or recovery",
    "Matrix": "Cross-walks that map controls and citations across frameworks",
    "Specification": "The library's own meta-documents defining how the corpus is built",
    "Charter": "Mandates that establish a function's authority, scope, and accountability",
    "Guide": "Technical reference material organized for adoption and implementation",
    "SOP": "Single-actor or narrow-team step sequences for one repeatable task",
    "Checklist": "Point-in-time verification lists for a defined activity",
    "Principle": "Foundational commitments that anchor the corpus's design choices",
    "Roadmap": "Multi-phase forward strategy tied to milestones and dependencies",
}


def type_slug(type_name):
    """URL slug for a document type (e.g. 'Standard' -> 'standard', 'SOP' -> 'sop').
    Lowercase, non-alphanumeric runs collapsed to a hyphen, so a future multi-word
    type stays a clean single path segment."""
    return re.sub(r"[^a-z0-9]+", "-", type_name.lower()).strip("-")


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
# Narrative-registry (narrative.yml) line shapes. The registry is generated by
# tools/build-narrative-registry.py in a regular one-page-per-block shape, like
# taxonomy.yml; the parser below is deliberately structural and loud on change.
_NARR_PATH_RE = re.compile(r'^- path:\s*"(.*)"\s*$')
_NARR_TITLE_RE = re.compile(r'^  title:\s*"(.*)"\s*$')
_NARR_TYPE_RE = re.compile(r'^  narrative_type:\s*"(.*)"\s*$')
_NARR_FIELD_RE = re.compile(r'^  [a-z_]+:')
_NARR_LIST_ITEM_RE = re.compile(r'^    - "(.*)"\s*$')
_NARR_ROUTE_RE = re.compile(r'^- route:\s*"(.*)"\s*$')
_CALVER_RE = re.compile(r"^\*\*Library Version:\*\*\s+([0-9]{4}\.[0-9]{2}\.[0-9]+)", re.M)
_PLACEHOLDER_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
_CANONICAL_TAG_RE = re.compile(r'<link rel="canonical" href="[^"]*">')
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
# Matches a root-relative href (quoted or unquoted) on a single line. The optional
# quote also catches the unquoted form (an href attribute assigned a bare site-root
# path), not only the quoted variants; the match is case-insensitive. A newline-split
# attribute is a known residual the line-by-line scan does not cover. The pattern is
# built in two pieces so this source line is not itself a false positive when the
# check scans the generator source below.
_ROOT_HREF_RE = re.compile(r'(?i)href' + r'\s*=\s*["\']?/')

# On the frozen v1/v2 trees, per-domain pages link each document out to its
# GitHub source; on v3 they link corpus documents to their on-site pages (PR-C),
# while root specifications, which have no on-site page, still open on GitHub.
# Pages carry a canonical URL for SEO. Both are the public repository / site, no secret.
GITHUB_BLOB_BASE = "https://github.com/jposluns/grc_library/blob/main/"
RAW_GITHUB_BASE = "https://raw.githubusercontent.com/jposluns/grc_library/main/"

# The curated corpus artefacts linked from the llms.txt map (repo-relative path,
# label). The manifest's llms.txt rows are re-derived from this list. NOTE: this
# is a PARALLEL list to the corpus links render_llms_txt emits inline, not a
# consumed single source (render_llms_txt hardcodes its own link lines with their
# trailing descriptions); keep the two in sync by hand until a test or refactor
# binds them (TODO 3.75 follow-up). By contrast, the manifest's domain-page and
# type-page rows ARE drift-proof: they re-derive from the same `figures` the pages
# render from. The repo-root and on-site (SITE_BASE) links in llms.txt are NOT
# corpus-path targets and are deliberately excluded.
CURATED_CORPUS_LINKS = [
    ("taxonomy.yml", "taxonomy.yml"),
    ("docs/portal.md", "Adopter portal"),
    ("compliance/matrix-grc-compliance-alignment.md", "Compliance matrix"),
    ("ai/README.md", "AI domain index"),
    ("ai/policy-ai-compliance.md", "AI compliance policy"),
    ("guardrails/README.md", "Governance rule-pack"),
    ("governance/register-canonical-citations.md", "Canonical citations register"),
    ("docs/decision-tree.md", "Decision tree"),
    ("docs/adopter-guide.md", "Adopter guide"),
    ("docs/maturity-scorecard.md", "Maturity scorecard"),
]
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


def load_narratives():
    """Return a list of narrative-page dicts from the committed generated
    narrative registry ``narrative.yml``: ``{'path','title','narrative_type',
    'route','domains'}``, where ``domains`` holds the ``domain:<name>`` facets of
    the page's ``derived_tags`` and ``route`` is the page's slug from the
    registry's ``listing:`` block.

    Like ``parse_taxonomy``, a tiny structural line parser (stdlib-only, no YAML
    library) tolerant only of the regular shape ``build-narrative-registry.py``
    emits. A missing registry, a zero-page parse, or a page missing a required
    field is a coupling breakage surfaced loudly as a BuildError, exactly the
    generator-health check's job."""
    if not NARRATIVE_REGISTRY.is_file():
        raise BuildError(f"narrative registry not found at {NARRATIVE_REGISTRY}")
    pages = []
    routes = {}  # page path -> route slug, from the listing: block
    section = None  # None | "pages" | "listing"
    cur = None
    cur_list = None  # "tags" while inside a derived_tags: block
    cur_route = None
    for line in NARRATIVE_REGISTRY.read_text(encoding="utf-8").splitlines():
        if line.rstrip() == "pages:":
            section, cur, cur_list = "pages", None, None
            continue
        if line.rstrip() == "listing:":
            section, cur, cur_list = "listing", None, None
            continue
        if section == "pages":
            m = _NARR_PATH_RE.match(line)
            if m:
                cur = {
                    "path": m.group(1), "title": None, "narrative_type": None,
                    "route": None, "domains": [],
                }
                pages.append(cur)
                cur_list = None
                continue
            if cur is None:
                continue
            mt = _NARR_TITLE_RE.match(line)
            if mt:
                cur["title"] = mt.group(1)
                cur_list = None
                continue
            mty = _NARR_TYPE_RE.match(line)
            if mty:
                cur["narrative_type"] = mty.group(1)
                cur_list = None
                continue
            if line.rstrip() == "  derived_tags:":
                cur_list = "tags"
                continue
            if _NARR_FIELD_RE.match(line):
                # Any other per-page field (corpus_sources:, version:, ...) ends
                # a derived_tags block; their own nested "- ..." items are then
                # ignored below because cur_list is no longer "tags".
                cur_list = None
                continue
            if cur_list == "tags":
                mtag = _NARR_LIST_ITEM_RE.match(line)
                if mtag and mtag.group(1).startswith("domain:"):
                    cur["domains"].append(mtag.group(1)[len("domain:"):])
                continue
        elif section == "listing":
            mr = _NARR_ROUTE_RE.match(line)
            if mr:
                cur_route = mr.group(1)
                continue
            mp = _NARR_TITLE_RE.match(line)  # listing "  title:" lines; ignored
            if mp:
                continue
            mpath = re.match(r'^  path:\s*"(.*)"\s*$', line)
            if mpath and cur_route is not None:
                routes[mpath.group(1)] = cur_route
                cur_route = None
    if not pages:
        raise BuildError(
            "narrative registry parsed to zero pages (schema change or empty registry?)"
        )
    missing = [p["path"] for p in pages if not p["title"] or not p["narrative_type"]]
    if missing:
        raise BuildError(
            f"{len(missing)} narrative registry page(s) missing a title or "
            f"narrative_type (schema change?); first: {missing[0]}"
        )
    braced = [
        p["path"] for p in pages
        if any(c in p["title"] or c in p["path"] for c in "{}")
    ]
    if braced:
        raise BuildError(
            f"{len(braced)} narrative registry page(s) with a brace in the "
            "title or path: a brace would survive as a template token in "
            "NARRATIVE_H1, the discovery-row title, or the source-URL href "
            f"(all _esc-only, not brace-escaped); first: {braced[0]}"
        )
    no_domains = [p["path"] for p in pages if not p["domains"]]
    if no_domains:
        raise BuildError(
            f"{len(no_domains)} narrative registry page(s) with no domain: derived "
            f"tag, so they would silently drop off every domain listing (emit-shape "
            f"drift or an untagged page?); first: {no_domains[0]}"
        )
    for page in pages:
        page["route"] = routes.get(page["path"])
    unrouted = [p["path"] for p in pages if not p["route"]]
    if unrouted:
        raise BuildError(
            f"{len(unrouted)} narrative registry page(s) with no listing: route "
            f"(schema change?); first: {unrouted[0]}"
        )
    return pages


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

    # The narrative registry joins the domain pages at render time. HEALTH
    # CHECK: every domain: derived tag must name a real DOMAIN_SCOPE domain, or
    # a page would silently drop off every domain listing (the same
    # loud-on-unknown philosophy as the DOMAIN_SCOPE completeness check above).
    narratives = load_narratives()
    unknown_narrative_domains = sorted(
        {d for page in narratives for d in page["domains"]} - set(DOMAIN_SCOPE)
    )
    if unknown_narrative_domains:
        raise BuildError(
            "narrative registry domain tag(s) naming no DOMAIN_SCOPE domain: "
            f"{', '.join(unknown_narrative_domains)} (registry drift or a renamed domain?)"
        )

    domain_docs = sum(by_domain.values())
    domain_count = len(by_domain)
    largest = max(by_domain.values())

    # Domains sorted by count descending, then name ascending for a stable order.
    domains = sorted(by_domain.items(), key=lambda kv: (-kv[1], kv[0]))
    # Types sorted by count descending, then name ascending.
    types = sorted(by_type.items(), key=lambda kv: (-kv[1], kv[0]))

    # Per-domain page data: the domain's document list (title / type / path from
    # the taxonomy, sorted by reading-progression type rank then title) plus its
    # README Purpose intro. The v2 and v3 domain pages additionally show the
    # render-time join of the published leadership (narrative) pages that touch
    # this domain.
    domain_pages = []
    for domain, count in domains:
        ddocs = [d for d in docs if d["domain"] == domain]
        untitled = [d["path"] for d in ddocs if not d["title"]]
        if untitled:
            raise BuildError(
                f"{len(untitled)} taxonomy entr(y/ies) in domain '{domain}' "
                f"missing a title (schema change?); first: {untitled[0]}"
            )
        # Secondary key mirrors tools/build-taxonomy.py: case-insensitive title then
        # repo-relative path tiebreaker, so the on-site domain-page order matches the
        # canonical taxonomy.yml / portal.md order (a case-sensitive title key here made
        # e.g. "eIDAS ..." sort to the end of its type; Sweep 105 finding A-1).
        ddocs = sorted(
            ddocs,
            key=lambda d: (TYPE_RANK.get(d["type"], len(TYPE_ORDER)), d["title"].lower(), d["path"]),
        )
        # The render-time registry join: the published leadership (narrative)
        # pages whose derived domain tags include this domain, sorted by
        # narrative_type then title then path for a stable, deterministic list.
        ndocs = sorted(
            [page for page in narratives if domain in page["domains"]],
            key=lambda page: (page["narrative_type"], page["title"].lower(), page["path"]),
        )
        domain_pages.append(
            {
                "domain": domain,
                "scope": DOMAIN_SCOPE[domain],
                "purpose": read_domain_purpose(domain),
                "docs": ddocs,
                "count": count,
                "narratives": ndocs,
            }
        )

    # Per-type page data: each type's document list across ALL domains (including
    # the root specification docs, which are in by_type though popped from
    # by_domain), sorted by domain then title, plus its curated one-line scope. A
    # taxonomy type with no TYPE_SCOPE entry is a build error.
    unknown_types = sorted(set(by_type) - set(TYPE_SCOPE))
    if unknown_types:
        raise BuildError(
            "document type(s) in the taxonomy with no TYPE_SCOPE description: "
            + ", ".join(unknown_types)
        )
    type_pages = []
    for type_name, count in types:
        tdocs = sorted(
            [d for d in docs if d["type"] == type_name],
            key=lambda d: (d["domain"], d["title"].lower(), d["path"]),
        )
        if len(tdocs) != count:
            raise BuildError(
                f"type '{type_name}' count mismatch: {count} vs {len(tdocs)} docs"
            )
        type_pages.append(
            {
                "type": type_name,
                "slug": type_slug(type_name),
                "scope": TYPE_SCOPE[type_name],
                "docs": tdocs,
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
        "type_pages": type_pages,
        "narratives": narratives,
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
            f'<td class="rg-name"><a href="{{{{BASE}}}}/{_esc(domain)}/">{_esc(domain)}</a></td>'
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
    two-level quick-nav rather than a separate flat Domains group (#941)."""
    return "\n".join(
        f'      <a class="sub" href="{{{{BASE}}}}/{_esc(domain)}/">{_esc(domain)}</a>'
        for domain, _ in figures["domains"]
    )


def render_type_chips(figures):
    """The "By document type" chips on the landing #register section, each a link
    to that type's per-type listing page (/types/<slug>/)."""
    chips = []
    for type_name, count in figures["types"]:
        slug = type_slug(type_name)
        chips.append(
            f'          <a class="type-chip" href="{{{{BASE}}}}/types/{slug}/">'
            f'<span class="tn">{count}</span>'
            f'<span class="tk">{_esc(type_name)}</span></a>'
        )
    return "\n".join(chips)


def template_dir_for(variant):
    """Return the template tree selected by one variant-table row."""
    return WEB_DIR / variant.template_source_dir


def load_partials(template_dir):
    """Read the shared-chrome partials once. Trailing newlines are stripped so a
    partial drops cleanly onto its own placeholder line."""
    partials = {}
    for key, fname in PARTIALS.items():
        p = template_dir / "partials" / fname
        if not p.is_file():
            raise BuildError(f"partial not found at {p}")
        partials[key] = p.read_text(encoding="utf-8").rstrip("\n")
    return partials


def render_domain_doc_rows(dp, variant):
    """One list row per document in the domain: a type tag and the document
    title as a link. On a variant with on-site document pages (v3) the title
    links to the document's own L2 page; otherwise it links to the source on
    GitHub in a new tab (the frozen root/v2 behaviour, kept byte-identical)."""
    rows = []
    for d in dp["docs"]:
        if variant.document_routes and d["domain"] != ROOT_DOMAIN:
            url = _doc_page_url("{{BASE}}", d["path"])
            link = (f'<a class="doc-title" href="{_esc(url)}">'
                    f'{_esc(d["title"])}</a>')
        else:
            url = GITHUB_BLOB_BASE + d["path"]
            link = (f'<a class="doc-title" href="{_esc(url)}" target="_blank" '
                    f'rel="noopener">{_esc(d["title"])}<span class="ext">&#8599;</span></a>')
        rows.append(
            f'          <li class="doc-row">'
            f'<span class="doc-type">{_esc(d["type"])}</span>'
            f'{link}</li>'
        )
    return "\n".join(rows)


def narrative_source_blob_url(page):
    """ONE narrative page's raw Markdown source on GitHub (the blob URL). The
    reading-room pages' "Read the source on GitHub" link uses THIS helper
    directly, so it keeps pointing at the source even after wave-2 PR-2b flips
    ``narrative_page_url`` below from the blob to the on-site route."""
    return GITHUB_BLOB_BASE + page["path"]


def narrative_page_url(page):
    """The link target for ONE narrative-page row: the page's ON-SITE
    reading-room route (wave-2 PR-2b's blob-to-on-site flip; every narrative
    row URL is emitted through this single helper). The route is derived
    from the SAME mapping the render loop writes (``narrative_out_rel``), so
    a row can never point at a route the reading room does not render, and
    it is emitted site-relative behind the BASE token (resolved in
    render_page's second substitution pass, the staging-template convention for
    internal links), so the link stays correct under the variant's URL
    prefix. The generated rows render in the v2 and v3 domain templates (the value is
    inert in v1), so the flip does not touch the frozen root. The
    "Read the source on GitHub" link inside the reading-room page keeps
    using ``narrative_source_blob_url`` directly."""
    out_rel = narrative_out_rel(page)
    return "{{BASE}}/" + out_rel[: -len("index.html")]


def render_domain_narrative_rows(dp):
    """One list row per published leadership (narrative) page that touches this
    domain, in the shape ``render_domain_doc_rows`` emits, with the page's
    narrative_type as the type tag and the title as the link to the page's
    ON-SITE reading-room route (via ``narrative_page_url``). Unlike the corpus
    doc rows on the frozen v1/v2 trees (external GitHub links, new-tab,
    external-arrow), these are INTERNAL links, so they open in place and carry no external arrow.
    When NO page touches the domain, the single row is the declared-gap
    statement in the shell's declared-gap voice (a gap is declared, never
    hidden), so the template needs no branch; today every domain has at least
    three pages, so the branch is future-proofing, not current output."""
    if not dp["narratives"]:
        return (
            '          <li class="doc-row">'
            '<span class="doc-type">Declared gap</span>'
            '<span class="doc-title">No leadership pages touch this area yet: '
            "a declared coverage gap, not a hidden one.</span>"
            "</li>"
        )
    rows = []
    for page in dp["narratives"]:
        url = narrative_page_url(page)
        rows.append(
            f'          <li class="doc-row">'
            f'<span class="doc-type">{_esc(page["narrative_type"])}</span>'
            f'<a class="doc-title" href="{_esc(url)}">'
            f'{_esc(page["title"])}</a>'
            f"</li>"
        )
    return "\n".join(rows)


def domain_page_values(dp, variant):
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
        "DOMAIN_DOC_ROWS": render_domain_doc_rows(dp, variant),
        # The leadership-page (narrative registry) join, consumed by the v2
        # and v3 domain templates. Per-page extra= values are inert in a template
        # that does not reference them (the unknown-placeholder error fires only
        # on placeholders a template contains), so the untouched v1 template's
        # output stays byte-identical. The count is COMPUTED, never typed.
        "DOMAIN_NARRATIVE_COUNT": str(len(dp["narratives"])),
        "DOMAIN_NARRATIVE_ROWS": render_domain_narrative_rows(dp),
        "DOMAIN_TITLE": f"{_esc(name)} domain: GRC Library",
        "DOMAIN_SEO_DESC": _esc(
            f"{dp['scope']}. {dp['count']} governance documents in the {name} "
            "domain of the open, CC BY-SA 4.0 GRC Library."
        ),
        "DOMAIN_CANONICAL": _site_url_for(variant, f"{name}/index.html"),
    }


def render_type_doc_rows(tp, variant):
    """One list row per document of this type: a small tag showing the document's
    DOMAIN and the document title as a link. On a variant with on-site document
    pages (v3) a non-root document links to its own L2 page; otherwise (and for
    root-level specs, which have no L2 page) it links to the source on GitHub."""
    rows = []
    for d in tp["docs"]:
        # Root-level specs (domain "root") only ever surface on a type page; show
        # a reader-friendly "library" tag rather than the internal "root".
        dom = "library" if d["domain"] == ROOT_DOMAIN else d["domain"]
        if variant.document_routes and d["domain"] != ROOT_DOMAIN:
            url = _doc_page_url("{{BASE}}", d["path"])
            link = (f'<a class="doc-title" href="{_esc(url)}">'
                    f'{_esc(d["title"])}</a>')
        else:
            url = GITHUB_BLOB_BASE + d["path"]
            link = (f'<a class="doc-title" href="{_esc(url)}" target="_blank" '
                    f'rel="noopener">{_esc(d["title"])}<span class="ext">&#8599;</span></a>')
        rows.append(
            f'          <li class="doc-row">'
            f'<span class="doc-type">{_esc(dom)}</span>'
            f'{link}</li>'
        )
    return "\n".join(rows)


def type_page_values(tp, variant):
    """The per-page values for one per-type listing page (merged on top of the
    shared values in render_page). All are built from controlled strings (the type
    name, curated scope, count), never from document prose."""
    name = tp["type"]
    return {
        "TYPE_NAME": _esc(name),
        "TYPE_SCOPE_TEXT": _esc(tp["scope"]),
        "TYPE_DOC_COUNT": str(tp["count"]),
        "TYPE_DOC_ROWS": render_type_doc_rows(tp, variant),
        "TYPE_TITLE": f"{_esc(name)} documents: GRC Library",
        "TYPE_SEO_DESC": _esc(
            f"{tp['scope']}. {tp['count']} {name}-type documents in the open, "
            "CC BY-SA 4.0 GRC Library."
        ),
        "TYPE_CANONICAL": _site_url_for(variant, f"types/{tp['slug']}/index.html"),
    }


# ---------------------------------------------------------------------------
# The executive reading room (wave-2 PR-2a; extended to /v3 in PR #1638): registry-listed narrative
# pages rendered ON-SITE by a constrained, stdlib-only Markdown renderer,
# under the narrative spec's renderer-confinement contract
# (specification-executive-narrative.md, the reserved website-track gate).
# ---------------------------------------------------------------------------

# Narrative types that render on-site. Wave-2 PR-2b scope: EVERY published
# narrative type (PR-2a shipped the Executive Briefs alone). The render loop
# additionally requires every registry narrative_type to appear in this tuple
# (a loud BuildError otherwise), so a future NEW type cannot silently skip
# on-site rendering by falling through the type filter.
NARRATIVE_ROUTE_TYPES = (
    "Executive Brief",
    "Journey",
    "Scenario",
    "Oversight Question Set",
    "Decision Narrative",
    "Outcome Map",
)

# On-site route prefix for the reading room (wave-2 decision Q2: one exec
# vocabulary on-site, /decisions/<subtype>/<slug>/; this deliberately diverges
# from the registry's executive/... route slugs, a recorded promotion-time
# note in the wave-2 decision record).
NARRATIVE_ROUTE_PREFIX = "decisions/"

# The section ids each reading-room TEMPLATE uses for its own shell sections,
# reserved so a narrative-body heading slugging to one raises loudly rather than
# emitting a duplicate id (RR guard, PR #1638). Keyed by template dir because the
# v2 and v3 reading-room templates use different shells; ``narr-intro`` is the
# renderer's own intro-section id and is always present.
NARRATIVE_SHELL_IDS = {
    "templates-v2": {"narr-intro", "depth", "source"},
    "templates-v3": {"narr-intro", "contents", "source", "go-deeper"},
}


def narrative_shell_ids_for(variant):
    """The reserved shell-id set for ``variant``'s reading-room template; raises
    if a narrative variant has no registered set (so a future template cannot
    silently fall back to the wrong reservation)."""
    ids = NARRATIVE_SHELL_IDS.get(variant.template_source_dir)
    if ids is None:
        raise BuildError(
            f"no narrative shell-id reservation for {variant.template_source_dir!r}; "
            "add its template's shell ids to NARRATIVE_SHELL_IDS"
        )
    return ids


# The narrative-source Markdown shapes the constrained renderer accepts. The
# supported set is EXACTLY the construct set surveyed across all 18 published
# narrative pages (2026-08-18): '## ' and '### ' section headings, flush-left
# paragraph prose, flat '- ' unordered and 'N. ' ordered lists, single-line
# '> ' blockquotes, uniform-separator GFM tables ('|'-led and '|'-terminated
# rows, a '---' separator row, no alignment colons), **bold**, `inline code`,
# and corpus-relative [label](path.md) links. Anything else is a loud
# BuildError, so a future narrative using an unsupported construct FAILS the
# build rather than rendering wrong: that includes setext heading underlines,
# spaced thematic breaks, malformed or ragged or colon-aligned tables, fenced
# code, raw HTML tags and blocks, HTML entities, closing-hash ATX headings
# ('## Text ##'), backslash escapes, tab-separated list markers ('N.<tab>'),
# and any block construct nested behind a '> ', '- ', or 'N. ' container
# marker or inside a table cell (container content is inline-only), each
# rejected explicitly. A literal
# ``{`` in prose is escaped to ``&#123;`` so no ``{{NAME}}`` placeholder
# pattern can survive into the rendered page (render_page's second
# substitution pass re-scans the whole document).
_NARR_ROUTE_SEGMENT_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_NARR_MD_LINK_RE = re.compile(r"\[([^\[\]]+)\]\(([^()\s]+)\)")
# Bold: the interior must open AND close against non-space content (mirroring
# _NARR_MD_EM_RE), so a CommonMark-invalid space-flanked closing delimiter
# ('**a **') is NOT paired here. An overlapping run like '**a **b** c**' would
# otherwise be silently re-partitioned by greedy left-to-right pairing into
# '<strong>a </strong>b<strong> c</strong>' (the middle word NOT bold, the
# opposite of the CommonMark parse); with the non-space-flanking interior the
# stray '**' survives to _esc_narrative_text and raises loudly instead.
_NARR_MD_BOLD_RE = re.compile(r"\*\*([^*\s](?:[^*]*[^*\s])?)\*\*")
# Single-star emphasis, processed AFTER bold extraction on the bold-free
# segments: the span must open and close against non-space content (so a
# spaced '3 * 4' star is never emphasis and still raises via the residual-star
# check downstream). PR-2b SURVEY NOTE: this construct was found in the
# published corpus (oversight-questions-ai-inventory-risk.md leads each
# question item with an italic span) but was NOT in the build order's
# anticipated construct list; it is supported deliberately and loudly-guarded
# (an unbalanced or malformed star still raises), never rendered silently.
_NARR_MD_EM_RE = re.compile(r"\*([^*\s](?:[^*]*[^*\s])?)\*")
_NARR_MD_UNDERSCORE_EM_RE = re.compile(r"(?<![A-Za-z0-9])_[^_\s][^_]*_(?![A-Za-z0-9])")
_NARR_MD_AUTOLINK_RE = re.compile(r"<[a-z][a-z0-9+.-]*:")
_NARR_MD_SCHEME_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
_NARR_MD_HR_RE = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")
_NARR_MD_SETEXT_UNDERLINE_RE = re.compile(r"^(=+|-{2})[ \t]*$")
_NARR_MD_SPACED_BREAK_RE = re.compile(r"^([-*_=])(?:[ \t]+\1)+[ \t]*$")
_NARR_MD_RAW_HTML_RE = re.compile(r"<[A-Za-z/!?]")
_NARR_MD_ENTITY_RE = re.compile(r"&(?:#\d+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);")
_NARR_MD_OTHER_LIST_RE = re.compile(r"^(\d+[.)]|[*+])\s")
# Ordered-list marker: 1 to 9 ASCII digits (the CommonMark bound). A longer
# run ('0000000001. ') is NOT a list marker and falls through to the
# _NARR_MD_OTHER_LIST_RE reject, so it cannot silently become an <ol> via an
# unbounded \d+ where int('0000000001') == 1.
_NARR_MD_OL_ITEM_RE = re.compile(r"^([0-9]{1,9})\. ")
# A GFM separator-row cell: three-or-more hyphens (the surveyed uniform '---'
# form), with the colon-alignment forms admitted here ONLY so a colon-bearing
# ':---:' separator is detected as separator-shaped and then rejected
# explicitly downstream. A one- or two-hyphen cell ('-', '--') is NOT
# separator-shaped, so the table model's "second row must be the separator"
# check raises rather than silently accepting an un-surveyed separator width.
_NARR_MD_TABLE_SEP_CELL_RE = re.compile(r":?-{3,}:?")
_NARR_TERMINATOR = "**End of Document**"


def _tracked_executive_paths():
    """The set of git-tracked repo-relative paths under ``executive/`` (paths
    only, never file content), the authority for the renderer-confinement
    "untracked source" rejection: trackedness is a property only git can
    answer, so the check asks git rather than inferring it from the file
    existing on disk. Fails LOUD (BuildError) when git is unavailable or the
    repo is not a work tree: the confinement refuses on ignorance rather than
    permitting, and rendering narrative sources without the tracked set is
    exactly the unverified state it must not proceed on (the narrative
    spec's renderer-confinement contract rejects untracked sources; the
    registry lists PATHS, not provenance, so an untracked file at a
    registry-listed path is only caught here (a content-modified tracked
    file stays listed and is not detected). A git-less build is an
    unsupported deploy and fails loud rather than weakening provenance.
    The ONE in-git-environment failure the call is hardened against is the
    container dubious-ownership refusal: ``-c safe.directory=<REPO_ROOT>``
    trusts THIS repository for this one invocation only (no global config
    change), so a differently-owned checkout in CI still answers; a
    genuinely absent or erroring git still raises."""
    try:
        proc = subprocess.run(
            [
                "git", "-c", f"safe.directory={REPO_ROOT}",
                "-C", str(REPO_ROOT), "ls-files", "-z", "--", "executive",
            ],
            capture_output=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError) as e:
        raise BuildError(
            "renderer confinement cannot establish the git-tracked executive/ "
            f"source set (git ls-files failed: {e}); refusing to render "
            "narrative sources without the trackedness authority"
        )
    tracked = {s for s in proc.stdout.decode("utf-8").split("\0") if s}
    if not tracked:
        raise BuildError(
            "git ls-files returned no tracked executive/ paths (not a git "
            "work tree, or the executive/ tree is missing?); refusing to "
            "render narrative sources"
        )
    return tracked


def narrative_source_file(rel_path, tracked, seen, root=None):
    """Admit ONE registry-listed narrative source path under the
    renderer-confinement contract and return its absolute path. The contract
    (specification-executive-narrative.md, website-track gate): the path is
    normalized, repository-relative, a regular file, resolved under
    ``executive/`` only; an absolute path, a parent-directory traversal, a
    symlink, a duplicate, or an untracked source is REJECTED with a loud
    BuildError. ``tracked`` is the git-tracked path set (from
    ``_tracked_executive_paths``), ``seen`` the mutable set of
    already-admitted paths (duplicate rejection; this call adds the admitted
    path), and ``root`` overrides the repo root for tests. Pure decision
    logic over supplied facts behind the thin git observer, so tests can
    drive every rejection with constructed roots and tracked sets."""
    root = REPO_ROOT if root is None else root
    if (not rel_path or rel_path.startswith(("/", "\\"))
            or re.match(r"^[A-Za-z]:", rel_path)):
        raise BuildError(f"narrative source path is absolute or empty: {rel_path!r}")
    if posixpath.normpath(rel_path) != rel_path or any(
        seg in ("", ".", "..") for seg in rel_path.split("/")
    ):
        raise BuildError(
            "narrative source path is not a normalized repo-relative path "
            f"(parent-directory traversal?): {rel_path!r}"
        )
    if not rel_path.startswith("executive/"):
        raise BuildError(f"narrative source outside executive/: {rel_path!r}")
    if rel_path in seen:
        raise BuildError(f"duplicate narrative source: {rel_path!r}")
    if rel_path not in tracked:
        raise BuildError(f"narrative source is not a git-tracked file: {rel_path!r}")
    path = root / rel_path
    if path.is_symlink() or path.resolve() != root.resolve() / rel_path:
        raise BuildError(f"narrative source resolves through a symlink: {rel_path!r}")
    if not path.is_file():
        raise BuildError(f"narrative source is not a regular file: {rel_path!r}")
    seen.add(rel_path)
    return path


def _narrative_body_lines(text, source_rel):
    """Return the BODY lines of one narrative source: everything after the
    first ``---`` metadata terminator, with the trailing corpus
    ``**End of Document**`` terminator required and dropped (the page chrome
    supplies the title and the closing sections, so neither the H1, the
    metadata block, nor the terminator is rendered). Loud on document-model
    drift: a missing leading H1, a missing metadata terminator, or a missing
    document terminator each raise BuildError."""
    lines = text.splitlines()
    first_content = next((ln for ln in lines if ln.strip()), "")
    if not first_content.startswith("# "):
        raise BuildError(f"{source_rel}: narrative source has no leading '# ' title line")
    for i, ln in enumerate(lines):
        if ln.strip() == "---":
            body = lines[i + 1:]
            break
    else:
        raise BuildError(f"{source_rel}: no '---' metadata terminator found")
    non_blank = [j for j, ln in enumerate(body) if ln.strip()]
    if not non_blank or body[non_blank[-1]].strip() != _NARR_TERMINATOR:
        raise BuildError(
            f"{source_rel}: body does not end with the '{_NARR_TERMINATOR}' "
            "terminator (document-model drift?)"
        )
    return body[: non_blank[-1]]


def _reject_nested_block(content, source_rel, container):
    """Reject a nested BLOCK construct hiding behind a container marker
    (E1, QA round 2): a blockquote's, list item's (unordered or ordered),
    or table cell's INNER content flows only through the inline renderer,
    so a block construct after the marker or inside the cell ('> ###
    heading', '- - nested list', '1. > quote', '| ### x |', '- ---',
    '>  indented', '> ```', '> <div>') would otherwise render silently as
    prose. The inner content is re-classified with the SAME line
    classifier and must come back a plain paragraph; any other
    classification, and any rejection the classifier itself raises, is a
    loud BuildError, so container content is inline-only by construction."""
    try:
        kind = _classify_narrative_line(content, source_rel)
    except BuildError as e:
        raise BuildError(
            f"{source_rel}: nested block construct in a {container} "
            f"unsupported (container content must be inline-only): "
            f"{content[:60]!r} ({e})"
        ) from e
    if kind != "p":
        raise BuildError(
            f"{source_rel}: nested block construct in a {container} "
            f"unsupported (container content must be inline-only): "
            f"{content[:60]!r}"
        )


def _classify_narrative_line(line, source_rel):
    """Classify ONE flush-left body line as h2 / h3 / quote / li / ol / tr /
    p, raising a loud BuildError on every construct outside the supported set
    (any other heading level, closing-hash ATX headings, star/plus or
    paren-marker lists, tab-separated list markers, pipes outside a
    well-formed '|'-led and '|'-terminated table row, fenced or indented
    code, horizontal rules, setext heading underlines, spaced thematic
    breaks, raw HTML tags and blocks, malformed markers, and any block
    construct nested behind a blockquote or list marker). Every rejection
    here fires BEFORE the paragraph fallback, so none of these shapes can
    silently render as prose."""
    if line != line.lstrip():
        raise BuildError(
            f"{source_rel}: indented line unsupported by the constrained "
            f"renderer: {line[:60]!r}"
        )
    # A pipe classifies the line as a table row ONLY in the exact surveyed
    # GFM shape: '|'-led AND '|'-terminated. Any other pipe placement (the
    # pipe-less header row 'A | B', the pipe-less separator '--- | ---', an
    # unterminated '| a | b') is still rejected here, never a paragraph;
    # the row grouping in _narrative_blocks then enforces the header /
    # separator / data-row table model on the classified rows.
    if "|" in line:
        if line.startswith("|") and line.endswith("|") and len(line) > 1:
            return "tr"
        raise BuildError(
            f"{source_rel}: a pipe is only supported inside a '|'-led and "
            f"'|'-terminated table row: {line[:60]!r}"
        )
    if line.startswith("#"):
        # A CommonMark CLOSING-hash sequence (a trailing '#' run alone or
        # preceded by whitespace, '## Text ##' / '## Text #' / '## ###')
        # would leak the hashes into the rendered heading text; the
        # supported forms are '## Text' / '### Text' with NO trailing
        # hashes. A hash attached to content ('## C#') is content, not a
        # closing sequence, and stays supported.
        for marker, kind in (("## ", "h2"), ("### ", "h3")):
            if line.startswith(marker) and line[len(marker):].strip():
                if re.search(r"(?:^|[ \t])#+$", line[len(marker):].strip()):
                    raise BuildError(
                        f"{source_rel}: closing-hash ATX headings unsupported "
                        f"(the supported form is '{marker}Text' with no "
                        f"trailing hashes): {line[:60]!r}"
                    )
                return kind
        raise BuildError(
            f"{source_rel}: only '## ' and '### ' section headings are "
            f"supported in the body: {line[:60]!r}"
        )
    if line.startswith(">"):
        if line.startswith("> ") and line[2:].strip():
            _reject_nested_block(line[2:], source_rel, "blockquote")
            return "quote"
        raise BuildError(f"{source_rel}: malformed blockquote line: {line[:60]!r}")
    # Setext underlines ('===' under an H1 candidate, '--' under an H2
    # candidate; a bare '---' body line already hits the HR rejection below)
    # and SPACED thematic breaks ('- - -', '* * *', '= = ='), both of which
    # would otherwise fall through to the paragraph or list branches and
    # render silently wrong.
    if _NARR_MD_SETEXT_UNDERLINE_RE.match(line):
        raise BuildError(
            f"{source_rel}: setext heading underlines unsupported: {line[:60]!r}"
        )
    if _NARR_MD_SPACED_BREAK_RE.match(line):
        raise BuildError(
            f"{source_rel}: spaced thematic breaks unsupported: {line[:60]!r}"
        )
    if _NARR_MD_HR_RE.match(line):
        raise BuildError(f"{source_rel}: horizontal rules unsupported: {line[:60]!r}")
    if line == "-" or (line.startswith("- ") and not line[2:].strip()):
        raise BuildError(f"{source_rel}: empty list item: {line[:60]!r}")
    if line.startswith("- "):
        _reject_nested_block(line[2:], source_rel, "list item")
        return "li"
    if line[:1] == "-" and len(line) >= 2 and line[1] in "\t\v\f\r":
        raise BuildError(
            f"{source_rel}: unsupported whitespace after the '-' list marker "
            f"(use '- ' with a single space): {line[:60]!r}"
        )
    # Ordered lists: the surveyed 'N. item' shape only (dot marker, ONE
    # space, inline-only content). The empty-item and tab/odd-whitespace
    # marker forms are rejected explicitly BEFORE the paragraph fallback,
    # so 'N.<tab>item' can never silently render as prose (the ul marker's
    # tab discipline, applied to the ordered marker too); 'N)' and star/plus
    # markers stay rejected below.
    if re.match(r"^\d+\.$", line):
        raise BuildError(f"{source_rel}: empty list item: {line[:60]!r}")
    m = _NARR_MD_OL_ITEM_RE.match(line)
    if m:
        if not line[m.end():].strip():
            raise BuildError(f"{source_rel}: empty list item: {line[:60]!r}")
        _reject_nested_block(line[m.end():], source_rel, "ordered-list item")
        return "ol"
    if re.match(r"^\d+\.[\t\v\f\r]", line):
        raise BuildError(
            f"{source_rel}: unsupported whitespace after the 'N.' ordered-list "
            f"marker (use 'N. ' with a single space): {line[:60]!r}"
        )
    if _NARR_MD_OTHER_LIST_RE.match(line):
        raise BuildError(
            f"{source_rel}: only flat '- ' unordered and 'N. ' ordered lists "
            f"are supported: {line[:60]!r}"
        )
    if line.startswith(("```", "~~~")):
        raise BuildError(f"{source_rel}: fenced code unsupported: {line[:60]!r}")
    # A raw HTML tag or block opener at line start ('<div>', '</div>',
    # '<!-- -->', '<!DOCTYPE', '<?'): rejected here as a block-level
    # construct; the inline escaper independently rejects the same shape
    # mid-paragraph. A lone '<' in prose (a spaced comparison sign) does not
    # match and still escapes cleanly downstream.
    if _NARR_MD_RAW_HTML_RE.match(line):
        raise BuildError(
            f"{source_rel}: raw HTML unsupported by the constrained "
            f"renderer: {line[:60]!r}"
        )
    return "p"


def _narrative_blocks(body_lines, source_rel):
    """Group body lines into (kind, contents) blocks: h2, h3, and quote
    blocks are single-line; consecutive plain lines join into one paragraph;
    consecutive '- ' lines join into one unordered list, consecutive 'N. '
    lines into one ordered list, and consecutive '|...|' rows into one
    table. Markdown's lazy continuations (a plain line directly under a
    list item, a quote, or a table) and multi-line blockquotes are
    AMBIGUOUS in a constrained renderer and none are used by the published
    pages, so they raise rather than guessing. Ordered-list items must be
    numbered sequentially from 1 (this renderer emits ``<ol>``, whose
    displayed numbering IS 1..n, so any other source numbering would
    silently diverge from a standard renderer)."""
    blocks = []
    cur_kind = None
    for raw in body_lines:
        if not raw.strip():
            cur_kind = None
            continue
        if raw.rstrip("\r\n").endswith("\\") or raw.endswith("  "):
            raise BuildError(f"{source_rel}: hard line breaks unsupported: {raw[:60]!r}")
        line = raw.rstrip()
        kind = _classify_narrative_line(line, source_rel)
        if cur_kind in ("li", "ol") and kind == "p":
            raise BuildError(
                f"{source_rel}: lazy list-item continuation unsupported: {line[:60]!r}"
            )
        if cur_kind == "quote" and kind in ("p", "quote"):
            raise BuildError(
                f"{source_rel}: multi-line blockquotes unsupported: {line[:60]!r}"
            )
        # In GFM a pipe-less line directly under a table's rows is ABSORBED
        # into the table as one more row; this renderer would instead start
        # a new paragraph, a silent divergence, so the shape raises.
        if cur_kind == "tr" and kind == "p":
            raise BuildError(
                f"{source_rel}: a table must be followed by a blank line, "
                f"not directly by prose (GFM would absorb the line into the "
                f"table): {line[:60]!r}"
            )
        # The mirror direction: a table row directly UNDER prose, a quote, or a
        # list item is not a new table in GFM (a table cannot interrupt a
        # paragraph; under a quote or list item it is a lazy continuation of
        # that container). This renderer would start a new table block, a
        # silent divergence, so a table must be PRECEDED by a blank line too.
        if kind == "tr" and cur_kind in ("p", "quote", "li", "ol"):
            raise BuildError(
                f"{source_rel}: a table must be preceded by a blank line, not "
                f"directly by prose, a quote, or a list item (GFM would not "
                f"start a new table there): {line[:60]!r}"
            )
        if kind == "ol":
            # The classifier admitted the 'N. ' marker, so the match holds.
            m = _NARR_MD_OL_ITEM_RE.match(line)
            expected = len(blocks[-1][1]) + 1 if cur_kind == "ol" else 1
            if int(m.group(1)) != expected:
                raise BuildError(
                    f"{source_rel}: ordered-list items must be numbered "
                    f"sequentially from 1 (expected {expected}; <ol> renders "
                    f"1..n, so other numbering would silently diverge): "
                    f"{line[:60]!r}"
                )
            item = line[m.end():]
            if cur_kind == "ol":
                blocks[-1][1].append(item)
            else:
                blocks.append((kind, [item]))
        elif kind == "p" and cur_kind == "p":
            blocks[-1][1].append(line)
        elif kind == "li" and cur_kind == "li":
            blocks[-1][1].append(line[2:])
        elif kind == "tr" and cur_kind == "tr":
            blocks[-1][1].append(line)
        else:
            if kind == "h2":
                content = line[3:]
            elif kind == "h3":
                content = line[4:]
            elif kind in ("quote", "li"):
                content = line[2:]
            else:
                content = line
            blocks.append((kind, [content]))
        cur_kind = kind
    return blocks


def _esc_narrative_text(text, source_rel):
    """HTML-escape ONE plain-text segment (links and bold already extracted),
    loud on any residual markup: unbalanced bold, code spans, stray link
    brackets, star emphasis, strikethrough, underscore emphasis, backslash
    escapes, autolink/raw-HTML scheme text, raw HTML tags, and HTML
    entities all raise. Literal ``<``, ``>``, ``&``, and ``{`` in prose are ESCAPED
    (never passed through as HTML). The ``{`` escape (to ``&#123;``) exists
    because render_page's SECOND substitution pass re-scans the whole
    document, narrative body included, so an unescaped ``{{SCRIPT}}``
    literal in prose would expand into the site's live script partial on
    that pass. Escaping ``{`` alone breaks the pattern (the placeholder
    regex requires a literal ``{{`` opener), so ``}`` needs no escaping;
    the escape is scoped to narrative TEXT only and never touches the
    template's own placeholders. A lone ``<`` in genuine prose (``1 < 2``)
    still escapes cleanly: the raw-HTML rejection fires only on ``<``
    immediately followed by a tag-shaped character (a letter, ``/``, ``!``,
    or ``?``), never on a spaced comparison sign. HTML entities
    (``&amp;``, ``&#123;``) are rejected rather than passed through: the
    escaper would double-escape them into visibly wrong text, so the loud
    failure replaces a silent mis-render."""
    for marker, name in (
        ("**", "unbalanced bold"),
        ("`", "code spans"),
        ("[", "unsupported or malformed link syntax"),
        ("]", "unsupported or malformed link syntax"),
        ("*", "star emphasis"),
        ("~~", "strikethrough"),
    ):
        if marker in text:
            raise BuildError(
                f"{source_rel}: {name} unsupported by the constrained "
                f"renderer: {text[:60]!r}"
            )
    # A backslash before ASCII punctuation is a Markdown escape ('\#', '\>',
    # '\-'): a standard renderer drops the backslash, this one would print
    # it, a silent divergence, so it is rejected. A backslash before an
    # alphanumeric ('C:\Users') is NOT a Markdown escape and stays plain
    # escaped prose.
    if re.search(r"\\[!-/:-@\[-`{-~]", text):
        raise BuildError(
            f"{source_rel}: backslash escapes unsupported by the constrained "
            f"renderer: {text[:60]!r}"
        )
    if _NARR_MD_UNDERSCORE_EM_RE.search(text):
        raise BuildError(f"{source_rel}: underscore emphasis unsupported: {text[:60]!r}")
    if _NARR_MD_AUTOLINK_RE.search(text):
        raise BuildError(
            f"{source_rel}: autolink or raw-HTML scheme text unsupported: {text[:60]!r}"
        )
    if _NARR_MD_RAW_HTML_RE.search(text):
        raise BuildError(
            f"{source_rel}: raw HTML tags unsupported by the constrained "
            f"renderer: {text[:60]!r}"
        )
    if _NARR_MD_ENTITY_RE.search(text):
        raise BuildError(
            f"{source_rel}: HTML entities unsupported (write the literal "
            f"character; prose is escaped at render time): {text[:60]!r}"
        )
    return _esc(text).replace("{", "&#123;")


def _render_narrative_em(text, source_rel):
    """Render ``*emphasis*`` spans in one BOLD-FREE, LINK-FREE segment,
    escaping everything else. Runs after the bold and link extractions, so a
    ``**`` still present here is an unbalanced bold marker and raises before
    it could be misread as two emphasis delimiters; a star that opens or
    closes against whitespace (``3 * 4``) never matches and raises via the
    segment escaper's residual-star check."""
    if "**" in text:
        raise BuildError(
            f"{source_rel}: unbalanced bold unsupported by the constrained "
            f"renderer: {text[:60]!r}"
        )
    parts = []
    pos = 0
    for m in _NARR_MD_EM_RE.finditer(text):
        parts.append(_esc_narrative_text(text[pos:m.start()], source_rel))
        parts.append("<em>" + _esc_narrative_text(m.group(1), source_rel) + "</em>")
        pos = m.end()
    parts.append(_esc_narrative_text(text[pos:], source_rel))
    return "".join(parts)


def _narrative_link_url(target, source_rel):
    """Convert ONE corpus-relative link target to its GitHub blob URL (the
    convention for corpus-relative links inside a narrative body). Only a plain relative path that
    resolves to an existing repo file is supported: scheme/protocol links,
    absolute paths, fragments and queries, and targets that escape the
    repository all raise."""
    if _NARR_MD_SCHEME_RE.match(target) or target.startswith("//"):
        raise BuildError(
            f"{source_rel}: only corpus-relative link targets are supported: {target!r}"
        )
    if target.startswith("/"):
        raise BuildError(f"{source_rel}: absolute link target unsupported: {target!r}")
    if "#" in target or "?" in target:
        raise BuildError(
            f"{source_rel}: link fragments and queries unsupported: {target!r}"
        )
    # A brace in the target would survive into the rendered ``href`` (the URL
    # is escaped by ``_esc``, which does NOT replace ``{``) and be re-expanded
    # as a ``{{NAME}}`` template token on render_page's second substitution
    # pass, injecting a live site partial inside the attribute. No corpus path
    # contains a brace, so reject it loudly rather than relying on the
    # defence-in-depth href escape below.
    if "{" in target or "}" in target:
        raise BuildError(
            f"{source_rel}: brace in a link target unsupported (would survive "
            f"as a template token in the href): {target!r}"
        )
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source_rel), target))
    if resolved.split("/", 1)[0] == "..":
        raise BuildError(f"{source_rel}: link target escapes the repository: {target!r}")
    if not (REPO_ROOT / resolved).is_file():
        raise BuildError(
            f"{source_rel}: link target does not resolve to a repo file: "
            f"{target!r} -> {resolved}"
        )
    return GITHUB_BLOB_BASE + resolved


def _render_narrative_links(text, source_rel):
    """Render one code-free, bold-free text segment's link constructs:
    corpus-relative links (to their GitHub blob URLs, opening in a new tab). The between-link segments carry ``*emphasis*`` rendering,
    but a link LABEL is plain text through ``_esc_narrative_text`` (so a star,
    bracket, or other inline marker in a label raises rather than silently
    rendering an un-surveyed nesting such as emphasis-inside-a-label); every
    other inline construct raises via the segment escaper. The ``href`` is
    ``{``-escaped as defence-in-depth on top of the brace reject in
    ``_narrative_link_url`` (a brace in a URL would otherwise re-expand as a
    ``{{NAME}}`` template token on render_page's second pass)."""
    parts = []
    pos = 0
    for m in _NARR_MD_LINK_RE.finditer(text):
        parts.append(_render_narrative_em(text[pos:m.start()], source_rel))
        url = _narrative_link_url(m.group(2), source_rel)
        parts.append(
            f'<a href="{_esc(url).replace("{", "&#123;")}" '
            'target="_blank" rel="noopener">'
            + _esc_narrative_text(m.group(1), source_rel) + "</a>"
        )
        pos = m.end()
    parts.append(_render_narrative_em(text[pos:], source_rel))
    return "".join(parts)


def _render_narrative_bold(text, source_rel):
    """Render one code-free segment's ``**bold**`` spans. Bold is extracted
    BEFORE links (PR-2b: the published corpus nests links INSIDE bold spans,
    '**... the [MCP server register](...)**'; the reverse nesting, bold
    inside a link label, appears nowhere in the corpus and now raises via
    the leftover-bracket check rather than rendering), so both the bold
    inner and the between-bold segments flow through the link renderer."""
    parts = []
    pos = 0
    for m in _NARR_MD_BOLD_RE.finditer(text):
        parts.append(_render_narrative_links(text[pos:m.start()], source_rel))
        parts.append(
            "<strong>" + _render_narrative_links(m.group(1), source_rel) + "</strong>"
        )
        pos = m.end()
    parts.append(_render_narrative_links(text[pos:], source_rel))
    return "".join(parts)


def _render_narrative_inline(text, source_rel):
    """Render one text unit's inline constructs: `code` spans first (as in
    CommonMark, code binds tighter than links and emphasis), then bold, links,
    and emphasis on the segments between the spans (in that outer-to-inner
    order: the corpus nests links inside bold and emphasis inside neither). A
    code span's inner text is LITERAL: markup-shaped characters (``*``, ``[``,
    ``**``, backticks are the span delimiter) stay as text rather than
    rendering or raising, per CommonMark, but the content is still HTML-escaped
    (``<``/``>``/``&``/``"``) and the ``{``->``&#123;`` placeholder-injection
    guard applies, so a ``<script>`` or ``{{NAME}}`` inside a span renders
    inert. CommonMark's single-space strip is applied (one leading and one
    trailing space removed when the content both begins and ends with a space
    and is not all spaces). An unbalanced or all-space/empty span raises
    loudly."""
    if "![" in text:
        raise BuildError(f"{source_rel}: images unsupported: {text[:60]!r}")
    if "`" not in text:
        return _render_narrative_bold(text, source_rel)
    segments = text.split("`")
    if len(segments) % 2 == 0:
        raise BuildError(
            f"{source_rel}: unbalanced code span (odd number of backticks): "
            f"{text[:60]!r}"
        )
    parts = []
    for i, segment in enumerate(segments):
        if i % 2:
            if not segment.strip():
                raise BuildError(f"{source_rel}: empty code span: {text[:60]!r}")
            # CommonMark code-span normalization: strip ONE leading and ONE
            # trailing space when the content both begins and ends with a space
            # (the all-space case is excluded above).
            inner = segment
            if len(inner) >= 2 and inner[0] == " " and inner[-1] == " ":
                inner = inner[1:-1]
            parts.append("<code>" + _esc(inner).replace("{", "&#123;") + "</code>")
        else:
            parts.append(_render_narrative_bold(segment, source_rel))
    return "".join(parts)


def _split_narrative_table_cells(line, source_rel):
    """Split ONE classified '|'-led and '|'-terminated table row into its
    stripped cells. A backslash anywhere in the row raises: GFM's ``\\|``
    escape denotes a LITERAL pipe, which this split cannot represent, so
    the escaped form (and every other backslash use, rejected downstream
    anyway) must not silently shift a cell boundary. An empty cell is
    document-model drift and raises too."""
    if "\\" in line:
        raise BuildError(
            f"{source_rel}: backslash in a table row unsupported (an escaped "
            f"pipe cannot be represented): {line[:60]!r}"
        )
    cells = [cell.strip() for cell in line[1:-1].split("|")]
    if any(not cell for cell in cells):
        raise BuildError(f"{source_rel}: empty table cell: {line[:60]!r}")
    return cells


def _render_narrative_table(row_lines, source_rel):
    """Render ONE grouped run of table rows as a GFM table: a header row, a
    UNIFORM '---' separator row (no alignment colons anywhere in the corpus;
    a colon-bearing separator is out of scope and raises), then data rows.
    The table model is enforced loudly: a missing or misplaced separator, a
    separator-shaped data or header row, a ragged row (any row's cell count
    differing from the header's), or a table with no data rows is
    document-model drift and raises. Every cell is inline-only (re-classified
    via ``_reject_nested_block``) and renders through the same inline
    renderer as prose, so cell text carries the full escaping discipline."""
    rows = [_split_narrative_table_cells(line, source_rel) for line in row_lines]

    def separator_shaped(cells):
        return all(_NARR_MD_TABLE_SEP_CELL_RE.fullmatch(cell) for cell in cells)

    if len(rows) < 3:
        raise BuildError(
            f"{source_rel}: a table needs a header row, a '---' separator "
            f"row, and at least one data row: {row_lines[0][:60]!r}"
        )
    header, separator, data = rows[0], rows[1], rows[2:]
    if not separator_shaped(separator):
        raise BuildError(
            f"{source_rel}: the second table row must be the '---' separator "
            f"row: {row_lines[1][:60]!r}"
        )
    if any(":" in cell for cell in separator):
        raise BuildError(
            f"{source_rel}: column-alignment colons in a table separator "
            f"unsupported (the corpus separator shape is uniform '---'): "
            f"{row_lines[1][:60]!r}"
        )
    for i, row in enumerate(rows):
        if i != 1 and separator_shaped(row):
            raise BuildError(
                f"{source_rel}: separator-shaped table row outside the "
                f"separator position: {row_lines[i][:60]!r}"
            )
        if len(row) != len(header):
            raise BuildError(
                f"{source_rel}: ragged table (row {i + 1} has {len(row)} "
                f"cell(s), the header has {len(header)}): {row_lines[i][:60]!r}"
            )

    def render_cells(cells, tag):
        rendered = []
        for cell in cells:
            _reject_nested_block(cell, source_rel, "table cell")
            rendered.append(
                f"<{tag}>" + _render_narrative_inline(cell, source_rel) + f"</{tag}>"
            )
        return "<tr>" + "".join(rendered) + "</tr>"

    body_rows = "\n".join("          " + render_cells(row, "td") for row in data)
    return (
        "      <table>\n"
        "        <thead>\n"
        "          " + render_cells(header, "th") + "\n"
        "        </thead>\n"
        "        <tbody>\n"
        + body_rows + "\n"
        "        </tbody>\n"
        "      </table>"
    )


def _narrative_heading_slug(text, seen_slugs, source_rel):
    """Anchor slug for one '## ' or '### ' heading (one shared page-wide slug
    set, so an h2/h3 anchor collision raises); loud on an empty, duplicate,
    or template-reserved slug (the reading-room template's own section ids, passed
    in per-variant by the caller as ``seen_slugs``)."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if not slug:
        raise BuildError(f"{source_rel}: heading yields an empty anchor: {text!r}")
    if slug in seen_slugs:
        raise BuildError(
            f"{source_rel}: duplicate or template-reserved section anchor: {slug!r}"
        )
    seen_slugs.add(slug)
    return slug


def render_narrative_body(text, source_rel, reserved_shell_ids=None):
    """Constrained Markdown-to-HTML for ONE narrative page body. Returns
    ``(sections_html, toc)`` where ``toc`` is ``[(anchor, heading), ...]``
    for the page's table-of-contents nav.

    The supported set is EXACTLY the construct set surveyed across the 18
    published narrative pages: '## ' headings (each opening a numbered
    exec-shell section, the section number COMPUTED), '### ' sub-headings
    (anchored within their section; the ToC lists the '## '
    sections alone), flush-left paragraphs, flat '- ' unordered and 'N. '
    ordered lists, single-line '> ' blockquotes, uniform-separator GFM
    tables, **bold**, `inline code`, and corpus-relative links (converted
    to GitHub blob URLs). Any unsupported construct raises a loud
    BuildError so a future narrative fails the build rather than rendering
    wrong; all body text is HTML-escaped with no raw-HTML passthrough, and a
    literal ``{`` in body prose escapes to ``&#123;`` so no ``{{NAME}}``
    placeholder pattern survives into render_page's second substitution pass
    (in a section HEADING a literal brace is instead rejected loudly, since a
    heading is plain text reused in slugs, the ToC, and attributes).
    Blocks before the first heading (the authority disclaimer) render in an
    unnumbered intro section."""
    blocks = _narrative_blocks(_narrative_body_lines(text, source_rel), source_rel)
    # The shell ids the TEMPLATE reserves (passed per-variant; defaults to the
    # v2 set for the direct-call test surface), so a body heading slugging to one
    # raises rather than emitting a duplicate id (RR guard, PR #1638).
    if reserved_shell_ids is None:
        reserved_shell_ids = NARRATIVE_SHELL_IDS["templates-v2"]
    seen_slugs = set(reserved_shell_ids)
    toc = []
    sections = []
    cur = {"anchor": "narr-intro", "head": None, "blocks": []}
    for kind, content in blocks:
        if kind == "h2":
            head_text = content[0]
            if (
                "{" in head_text
                or "}" in head_text
                or _render_narrative_inline(head_text, source_rel) != _esc(head_text)
            ):
                # A literal '{' differs after the inline pass ('{'->'&#123;')
                # but a lone '}' is identical on both sides, so both braces are
                # rejected EXPLICITLY here rather than relying on the escape
                # asymmetry (F2, round-2 QA).
                raise BuildError(
                    f"{source_rel}: inline markup or a literal brace in a "
                    f"section heading unsupported (a heading is plain text, "
                    f"and a brace is template-reserved and rejected here "
                    f"rather than escaped as it is in body prose): "
                    f"{head_text[:60]!r}"
                )
            if cur["head"] is not None or cur["blocks"]:
                sections.append(cur)
            slug = _narrative_heading_slug(head_text, seen_slugs, source_rel)
            toc.append((slug, head_text))
            cur = {"anchor": slug, "head": head_text, "blocks": []}
        elif kind == "h3":
            # The H2 treatment inside the current section: inline-only text,
            # a page-unique anchor from the shared slug set (so an h2/h3
            # collision raises), heading text through the narrative escaper.
            # Deliberately NOT in the ToC: the sidenav lists the numbered
            # '## ' sections alone.
            head_text = content[0]
            if (
                "{" in head_text
                or "}" in head_text
                or _render_narrative_inline(head_text, source_rel) != _esc(head_text)
            ):
                # A literal '{' differs after the inline pass ('{'->'&#123;')
                # but a lone '}' is identical on both sides, so both braces are
                # rejected EXPLICITLY here rather than relying on the escape
                # asymmetry (F2, round-2 QA).
                raise BuildError(
                    f"{source_rel}: inline markup or a literal brace in a "
                    f"section heading unsupported (a heading is plain text, "
                    f"and a brace is template-reserved and rejected here "
                    f"rather than escaped as it is in body prose): "
                    f"{head_text[:60]!r}"
                )
            slug = _narrative_heading_slug(head_text, seen_slugs, source_rel)
            cur["blocks"].append(
                f'      <h3 id="{slug}">'
                + _esc_narrative_text(head_text, source_rel) + "</h3>"
            )
        elif kind == "p":
            cur["blocks"].append(
                "      <p>" + _render_narrative_inline(" ".join(content), source_rel) + "</p>"
            )
        elif kind == "quote":
            cur["blocks"].append(
                "      <blockquote><p>"
                + _render_narrative_inline(content[0], source_rel)
                + "</p></blockquote>"
            )
        elif kind == "tr":
            cur["blocks"].append(_render_narrative_table(content, source_rel))
        else:  # li / ol
            tag = "ul" if kind == "li" else "ol"
            items = "\n".join(
                "        <li>" + _render_narrative_inline(item, source_rel) + "</li>"
                for item in content
            )
            cur["blocks"].append(f"      <{tag}>\n" + items + f"\n      </{tag}>")
    if cur["head"] is not None or cur["blocks"]:
        sections.append(cur)
    if not toc:
        raise BuildError(f"{source_rel}: body has no '## ' sections (document-model drift?)")
    out = []
    number = 0
    for sec in sections:
        head_html = ""
        if sec["head"] is not None:
            number += 1
            head_html = (
                f'      <div class="sec-head"><span class="sec-num">&sect;{number:02d}</span>'
                f"<h2>{_esc(sec['head'])}</h2></div>\n"
            )
        out.append(
            f'  <section class="narr" id="{sec["anchor"]}">\n'
            '    <div class="wrap">\n'
            + head_html + "\n".join(sec["blocks"]) + "\n"
            "    </div>\n"
            "  </section>"
        )
    return "\n\n".join(out), toc


def narrative_out_rel(page):
    """Map ONE narrative page's registry route to its on-site output path:
    ``decisions/<subtype>/<slug>/index.html`` (wave-2 decision Q2, one exec
    vocabulary on-site; the registry's route slugs keep their ``executive/``
    prefix, a recorded divergence). The route drives a filesystem write, so
    a shape outside ``executive/<subtype>/<slug>`` in the plain slug charset
    raises rather than being written."""
    route = page["route"]
    prefix = "executive/"
    if not route.startswith(prefix):
        raise BuildError(f"narrative route without the executive/ prefix: {route!r}")
    tail = route[len(prefix):]
    segments = tail.split("/")
    if len(segments) != 2 or not all(_NARR_ROUTE_SEGMENT_RE.match(s) for s in segments):
        raise BuildError(f"narrative route is not executive/<subtype>/<slug>: {route!r}")
    return f"{NARRATIVE_ROUTE_PREFIX}{tail}/index.html"


def render_narrative_domain_chips(page):
    """The domain-page chips for ONE narrative: exactly the domains the registry
    tags it with (``page['domains']``), each linking to its on-site domain page.
    Replaces the fixed rail so the "go deeper" links match THIS narrative and its
    copy is accurate (PR #1638; RR-1). All 18 narratives carry domain tags."""
    return "\n".join(
        f'        <a href="{{{{BASE}}}}/{_esc(d)}/">{_esc(d)}</a>'
        for d in page.get("domains", [])
    )


def narrative_page_values(page, variant, out_rel, body_html, toc):
    """The per-page values for one reading-room page (merged on top of the
    shared values in render_page, riding the same ``extra=`` path as the
    domain and type pages, so they are inert everywhere else). SEO/attribute
    values are built from registry strings (title, narrative_type), all
    escaped; the body arrives pre-rendered by the constrained renderer."""
    title = page["title"]
    sidenav = "\n".join(
        f'      <a href="#{anchor}">{_esc(heading)}</a>' for anchor, heading in toc
    )
    return {
        "NARRATIVE_TYPE": _esc(page["narrative_type"]),
        "NARRATIVE_H1": _esc(title),
        "NARRATIVE_BODY": body_html,
        "NARRATIVE_SIDENAV": sidenav,
        "NARRATIVE_DOMAINS": render_narrative_domain_chips(page),
        # Brace-escaped as defence-in-depth (F1, round-2 QA): the registry
        # path is already brace-rejected in load_narratives, but the source
        # URL flows into an href, so mirror the in-body href treatment so a
        # brace could never survive into render_page's second pass here either.
        "NARRATIVE_SOURCE_URL": _esc(narrative_source_blob_url(page)).replace("{", "&#123;"),
        "NARRATIVE_TITLE": f"{_esc(title)}: GRC Library",
        "NARRATIVE_SEO_DESC": _esc(
            f"{page['narrative_type']}: {title}. A leadership page of the open, "
            "CC BY-SA 4.0 GRC Library; every claim resolves to the governing "
            "corpus documents."
        ),
        "NARRATIVE_CANONICAL": _site_url_for(variant, out_rel),
    }


def figure_values(figures, variant):
    """The corpus-derived values interpolated into every page."""
    return {
        "CALVER": figures["calver"],
        "DOC_TOTAL": str(figures["total"]),
        "DOMAIN_COUNT": str(figures["domain_count"]),
        "DOMAIN_DOC_TOTAL": str(figures["domain_docs"]),
        "ROOT_COUNT": str(figures["root_count"]),
        "BASE": site_prefix_for(variant),
        "DOMAIN_ROWS": render_domain_rows(figures),
        "TYPE_CHIPS": render_type_chips(figures),
        "SIDENAV_DOMAINS": render_sidenav_domains(figures),
    }


def render_page(template_name, figures, variant, template_dir, partials, extra=None, out_rel=None):
    """Render one page: inject the shared partials, then the corpus figures.

    Two substitution passes, because the partials carry figure placeholders of
    their own (CALVER in the topbar; DOC_TOTAL / DOMAIN_COUNT in the footer). The
    first pass drops the partial text (with its ``{{CALVER}}`` etc. still literal)
    into the page and resolves any figures written directly in the page body; the
    second resolves the figures that arrived via a partial. Returns
    ``(html, used_keys)``."""
    template_path = template_dir / template_name
    if not template_path.is_file():
        raise BuildError(f"template not found at {template_path}")
    template = template_path.read_text(encoding="utf-8")

    values = {**partials, **figure_values(figures, variant)}
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
    if not variant.indexable:
        if out_rel is None:
            raise BuildError(f"non-indexable variant page {template_name} has no output path")
        metadata = (
            '<meta name="robots" content="noindex,nofollow">\n'
            f'<link rel="canonical" href="{_site_url_for(variant, out_rel)}">'
        )
        if _CANONICAL_TAG_RE.search(rendered):
            rendered = _CANONICAL_TAG_RE.sub(metadata, rendered)
        else:
            rendered = rendered.replace("</head>", f"{metadata}\n</head>", 1)
    return rendered, used


def render_robots_txt():
    """robots.txt welcoming AI and search crawlers. This corpus is CC BY-SA 4.0
    and intended to be widely read, cited, and learned from (including as AI
    training data), so the file names the known AI/training crawlers explicitly
    with ``Allow: /`` and then allows everyone via a trailing wildcard group while disallowing the ``/v2``
    staging tree,
    and advertises the sitemap. It is deliberately permissive and replaces any
    platform-managed default that would restrict AI crawlers."""
    lines = [
        "# grclibrary.ai",
        "# This is an open, CC BY-SA 4.0 governance, risk, and compliance corpus,",
        "# intended to be widely read, cited, and learned from, including as",
        "# training data for AI systems. All crawlers are welcome on every public path (the /v2 staging tree is disallowed).",
        "",
    ]
    for ua in AI_CRAWLER_USER_AGENTS:
        lines += [f"User-agent: {ua}", "Allow: /", "Disallow: /v2/", ""]
    lines += [
        "User-agent: *", "Allow: /", "Disallow: /v2/", "",
        f"Sitemap: {SITE_BASE}/sitemap.xml", "",
    ]
    return "\n".join(lines)


def site_prefix_for(variant):
    """Return one variant's slash-led site URL prefix for HTML and canonicals."""
    prefix = variant.url_prefix.strip("/")
    return f"/{prefix}" if prefix else ""


def _site_url_for(variant, out_rel):
    """Map one variant's rendered page path to its canonical site URL."""
    prefix = site_prefix_for(variant)
    if out_rel == "index.html":
        return f"{SITE_BASE}{prefix}/"
    if out_rel.endswith("/index.html"):
        return f"{SITE_BASE}{prefix}/{out_rel[: -len('index.html')]}"
    return f"{SITE_BASE}{prefix}/{out_rel}"


def _site_path_for(variant, out_rel):
    """Map one variant's rendered page path to its site-relative URL path."""
    prefix = site_prefix_for(variant)
    if out_rel == "index.html":
        return f"{prefix}/"
    if out_rel.endswith("/index.html"):
        return f"{prefix}/{out_rel[: -len('index.html')]}"
    return f"{prefix}/{out_rel}"


def output_rel_for(variant, out_rel):
    """Map one variant's site-relative output to its dist-relative path."""
    prefix = variant.url_prefix.strip("/")
    return f"{prefix}/{out_rel}" if prefix else out_rel


def render_sitemap(variant, html_page_rels):
    """sitemap.xml listing every rendered page of the sole indexable root variant as a directory-style URL,
    built from the HTML page set so a newly-added page is listed automatically."""
    locs = "\n".join(
        f"  <url><loc>{_site_url_for(variant, rel)}</loc></url>" for rel in html_page_rels
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{locs}\n"
        "</urlset>\n"
    )


def render_llms_txt(figures, variant):
    """llms.txt (the llmstxt.org convention): a curated Markdown map of the site
    and corpus for LLMs. Descriptive register only (a link list with short
    notes). Corpus artefacts link to GitHub (the source material); site pages
    link to grclibrary.ai. All links resolve to real, verified artefacts."""
    gh = GITHUB_BLOB_BASE
    repo = "https://github.com/jposluns/grc_library"
    return f"""# GRC Library

> An openly-licensed (CC BY-SA 4.0) corpus of organization-neutral governance,
> risk, and compliance documentation in Markdown, spanning {figures['domain_count']} domains including a
> self-contained AI-governance sub-corpus. Descriptive reference material; not legal advice.

## Core
- [GitHub repository]({repo}): the raw Markdown corpus, the source material.
- [taxonomy.yml]({gh}taxonomy.yml): machine-readable inventory of every document.
- [Adopter portal]({gh}docs/portal.md): audience-keyed navigation front door.
- [Compliance matrix]({gh}compliance/matrix-grc-compliance-alignment.md): control-to-framework mappings.
- [For AI]({_site_url_for(variant, "for-ai/index.html")}): how AI systems can learn from the corpus, plus a resource index.

## AI governance
- [AI domain index]({gh}ai/README.md): the AI governance, risk, security, and documentation sub-corpus.
- [AI compliance policy]({gh}ai/policy-ai-compliance.md): risk-tier classification and obligations.
- [Governance rule-pack]({gh}guardrails/README.md): the disciplines an AI assistant follows when contributing to the corpus.

## Optional
- [Canonical citations register]({gh}governance/register-canonical-citations.md): the corpus's verified external-standard citations.
- [Decision tree]({gh}docs/decision-tree.md), [Adopter guide]({gh}docs/adopter-guide.md), [Maturity scorecard]({gh}docs/maturity-scorecard.md).
"""


# A corpus link written directly into a static page template, as opposed to one
# the taxonomy emits. `render_static_template_links` scans for these so the
# manifest (and therefore gate 75) reaches them; before that scan existed, 48
# distinct targets were linked by the site and covered by no gate, including
# every governance-rule and skill link on the pack page (Sweep 120 F2).
TEMPLATE_CORPUS_LINK_RE = re.compile(
    re.escape(GITHUB_BLOB_BASE) + r'([^"#?\s]+)'
)


def render_static_template_links(variant):
    """Yield ``(target, location, link_text)`` for every corpus link hardcoded in
    a static page template.

    Only the templates in PAGES are scanned: `domain.html` and `type.html` render
    from the taxonomy (already covered above) and the shared partials carry no
    corpus links, so PAGES is the complete set of static-link sources for the indexable
    root manifest. A staging variant's extra_pages templates carry their own hardcoded
    corpus links, intentionally excluded from the committed root manifest (verified at
    authoring time, folded in at promotion). The link
    text is the anchor's own text when it can be read, else the target's basename,
    since a template anchor's text is prose rather than a document title."""
    template_dir = template_dir_for(variant)
    for template_name, out_rel in PAGES:
        path = template_dir / template_name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        location = _site_path_for(variant, out_rel)
        for match in TEMPLATE_CORPUS_LINK_RE.finditer(text):
            target = match.group(1)
            anchor = re.match(
                r'[^>]*>(?P<text>[^<]{1,120})</a>', text[match.end():]
            )
            label = (anchor.group("text").strip() if anchor
                     else target.rsplit("/", 1)[-1])
            yield target, location, label


def render_corpus_link_manifest(figures, variant):
    """The committed web-to-corpus link manifest: one row per corpus/GitHub
    target the indexable root variant's pages link (its repo-relative path, its
    website location, and its link text). A non-indexable staging variant may carry
    extra routes (variant.extra_pages) that link further corpus targets; those
    staging-only links are verified at authoring time but are not enumerated in
    this root manifest, and enter it when a staging tree is promoted to root. Re-derived from the SAME sources the pages emit from, so the
    manifest cannot drift from the emitted links: the taxonomy docs behind the
    per-domain pages (render_domain_doc_rows) and the per-type pages
    (render_type_doc_rows), the curated llms.txt corpus links
    (CURATED_CORPUS_LINKS), and the corpus links hardcoded in the static page
    templates (render_static_template_links). The repo-root and on-site links are
    not corpus-path targets and are excluded, matching the gate's scope."""
    rows = {}  # (target, location) -> link_text, dedup-safe and deterministic
    for dp in figures["domain_pages"]:
        for d in dp["docs"]:
            rows[(d["path"], _site_path_for(variant, f"{dp['domain']}/index.html"))] = d["title"]
    for tp in figures["type_pages"]:
        for d in tp["docs"]:
            rows[(d["path"], _site_path_for(variant, f"types/{tp['slug']}/index.html"))] = d["title"]
    for path, label in CURATED_CORPUS_LINKS:
        rows[(path, "llms.txt")] = label
    for target, location, label in render_static_template_links(variant):
        rows[(target, location)] = label
    lines = [
        "# Web-to-corpus link manifest",
        "",
        "Generated by `.web/build.py`; do not edit by hand. Every corpus/GitHub "
        "target the indexable root variant's pages link, with its website location and link text: the "
        "taxonomy-derived domain and type pages, the curated `llms.txt` map, and "
        "the corpus links hardcoded in the static page templates. Gate 75 "
        "(`tools/lint-web-corpus-links.py`) resolves each target against the repo. "
        "Non-indexable staging variants (v2 and v3) may carry extra routes that "
        "link further corpus targets; those staging-only links are verified at "
        "authoring time, are not enumerated here, and enter this manifest when a "
        "staging tree is promoted to root.",
        "",
        "| Corpus target | Website location | Link text |",
        "| --- | --- | --- |",
    ]
    for (target, location), link_text in sorted(rows.items()):
        lines.append(f"| {target} | {location} | {link_text} |")
    return "\n".join(lines) + "\n"


def indexable_variant():
    """Return the sole indexable root variant, rejecting an incomplete promotion."""
    indexable = [variant for variant in VARIANTS if variant.indexable]
    if len(indexable) != 1 or indexable[0].url_prefix != "":
        raise BuildError(
            "variant table must contain exactly one indexable variant with an empty prefix"
        )
    return indexable[0]



# ---------------------------------------------------------------------------
# On-site document pages (v3 wave PR-C): one L2 page per corpus document,
# surfacing the 13-field metadata + purpose + section outline + frameworks +
# related documents that the corpus already carries (before PR-C every document
# dead-ended at a raw GitHub .md). Data comes ENTIRELY from the enriched
# taxonomy.yml (tools/build-taxonomy.py emits purpose/sections/frameworks/
# confidentiality alongside the existing per-doc fields), so the generator
# still never walks the repository. Variant-scoped by Variant.document_routes
# so the frozen root/v2 trees are untouched.
# ---------------------------------------------------------------------------

_TAXO_SCALAR_RE = re.compile(r'^  ([a-z_]+): "(.*)"$')
_TAXO_LISTKEY_RE = re.compile(r'^  ([a-z_]+):$')
_TAXO_LISTITEM_RE = re.compile(r'^    - "(.*)"$')


def _taxo_unescape(v):
    """Reverse tools/build-taxonomy.py yaml_escape (double-quoted, backslash +
    quote escaped)."""
    return v.replace('\\"', '"').replace("\\\\", "\\")


def parse_taxonomy_full(text):
    """Return a list of full per-document dicts from taxonomy.yml, including the
    scalar fields plus the ``sections``/``frameworks``/``related_documents``
    lists. Companion to the deliberately-tiny parse_taxonomy (which reads only
    path/domain/type/title for the domain/type pages); this reader is used only
    for the on-site document pages and tolerates exactly the one-doc-per-block
    shape the generator emits."""
    docs = []
    cur = None
    cur_list = None
    in_docs = False
    for line in text.splitlines():
        if line.rstrip() == "documents:":
            in_docs = True
            continue
        if not in_docs:
            continue
        m = _DOC_RE.match(line)
        if m:
            cur = {"path": m.group(1), "sections": [], "frameworks": [],
                   "related_documents": []}
            docs.append(cur)
            cur_list = None
            continue
        if cur is None:
            continue
        ms = _TAXO_SCALAR_RE.match(line)
        if ms:
            cur[ms.group(1)] = _taxo_unescape(ms.group(2))
            cur_list = None
            continue
        mk = _TAXO_LISTKEY_RE.match(line)
        if mk:
            cur_list = mk.group(1)
            cur.setdefault(cur_list, [])
            continue
        mi = _TAXO_LISTITEM_RE.match(line)
        if mi and cur_list is not None:
            cur[cur_list].append(_taxo_unescape(mi.group(1)))
    return docs


def _doc_route_rel(path):
    """The on-site route for a corpus document page: documents/<path-no-.md>/."""
    return "documents/" + path[:-3] + "/index.html" if path.endswith(".md") \
        else "documents/" + path + "/index.html"


def _doc_page_url(base, path):
    """The {{BASE}}-relative link to a document's on-site page."""
    stem = path[:-3] if path.endswith(".md") else path
    return f"{base}/documents/{stem}/"


# The metadata fields shown in the L2 spec strip, in display order (label, key).
_SPEC_STRIP_FIELDS = (
    ("Type", "type"),
    ("Version", "version"),
    ("Date", "date"),
    ("Owner", "owner"),
    ("Approving authority", "approving_authority"),
    ("Classification", "classification"),
    ("Confidentiality", "confidentiality"),
    ("Category", "category"),
    ("Review frequency", "review_frequency"),
    ("License", "license"),
)


def _render_meta_strip(doc):
    cells = []
    for label, key in _SPEC_STRIP_FIELDS:
        val = doc.get(key, "")
        if not val:
            continue
        cells.append(
            f'        <div class="spec"><dt>{_esc(label)}</dt>'
            f'<dd>{_esc(val)}</dd></div>'
        )
    return "\n".join(cells)


def _render_section_outline(doc):
    secs = doc.get("sections", [])
    if not secs:
        return '        <li class="muted">No section outline.</li>'
    # Flatten inline Markdown (code spans, bold) in a heading for clean display;
    # the taxonomy keeps the exact heading, the outline shows plain text.
    def _plain(s):
        s = s.replace("`", "")
        s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
        return s
    return "\n".join(f'        <li>{_esc(_plain(s))}</li>' for s in secs)


def _render_frameworks(doc):
    fws = doc.get("frameworks", [])
    if not fws:
        return ('        <span class="chip-muted">'
                'No external-framework alignment table.</span>')
    return "\n".join(f'        <span class="type-chip">{_esc(f)}</span>'
                     for f in fws)


def _render_related_docs(doc, docs_by_path, base):
    rels = doc.get("related_documents", [])
    if not rels:
        return ('        <li class="doc-row"><span class="doc-type">None listed</span>'
                '<span class="doc-title">This document lists no related documents.</span></li>')
    rows = []
    for rp in rels:
        rd = docs_by_path.get(rp)
        if rd and rd.get("domain") != ROOT_DOMAIN:
            # on-site link to the related document's own L2 page
            url = _doc_page_url(base, rp)
            rows.append(
                f'        <li class="doc-row">'
                f'<span class="doc-type">{_esc(rd.get("type",""))}</span>'
                f'<a class="doc-title" href="{_esc(url)}">'
                f'{_esc(rd.get("title", rp))}</a></li>'
            )
        else:
            # related target not an on-site domain document: link to source
            url = GITHUB_BLOB_BASE + rp
            title = rd.get("title", rp) if rd else rp
            rows.append(
                f'        <li class="doc-row">'
                f'<span class="doc-type">source</span>'
                f'<a class="doc-title" href="{_esc(url)}" target="_blank" rel="noopener">'
                f'{_esc(title)}<span class="ext">&#8599;</span></a></li>'
            )
    return "\n".join(rows)


def document_page_values(doc, docs_by_path, variant):
    """Per-page values for one on-site document (L2) page, all built from the
    enriched taxonomy (never from live document prose): the escaper covers the
    attribute context, so the purpose is safe in the meta-description too."""
    base = "{{BASE}}"
    path = doc["path"]
    domain = doc.get("domain", "")
    doc_type = doc.get("type", "")
    title = doc.get("title", path)
    purpose = doc.get("purpose", "")
    if not purpose:
        # Graceful lede for the few structurally-atypical docs with no
        # purpose paragraph in source (keeps the lede + meta non-empty).
        purpose = f"A {doc_type.lower()} in the {domain} area of the GRC Library."
    return {
        "DOC_TITLE": _esc(title),
        "DOC_TYPE": _esc(doc_type),
        "DOC_TYPE_SLUG": type_slug(doc_type),
        "DOC_AREA": _esc(domain),
        "DOC_AREA_SLUG": _esc(domain),
        "DOC_PURPOSE": _esc(purpose),
        "META_STRIP": _render_meta_strip(doc),
        "SECTION_OUTLINE": _render_section_outline(doc),
        "FRAMEWORKS": _render_frameworks(doc),
        "RELATED_DOCS": _render_related_docs(doc, docs_by_path, base),
        "GITHUB_URL": _esc(GITHUB_BLOB_BASE + path),
        "RAW_MD_URL": _esc(RAW_GITHUB_BASE + path),
    }


def render_search_index(variant):
    """A compact JSON index for the client-side /v3 search: one entry per corpus
    DOMAIN document (title, type, area, a truncated purpose, frameworks, and its
    on-site URL), built from the enriched taxonomy (the generator still never
    walks the repository). Emitted only for a variant with document_routes.
    Reading-room narrative pages are NOT indexed here: they are corpus documents
    by neither count nor category (the gate-86 boundary), and are reached from
    their domain pages and the Decide path instead."""
    import json
    base = variant.url_prefix.rstrip("/")
    prefix = f"/{base}" if base else ""
    full = parse_taxonomy_full(TAXONOMY.read_text(encoding="utf-8"))
    entries = []
    for d in full:
        if d.get("domain") == ROOT_DOMAIN:
            continue
        stem = d["path"][:-3] if d["path"].endswith(".md") else d["path"]
        entries.append({
            "t": d.get("title", ""),
            "y": d.get("type", ""),
            "a": d.get("domain", ""),
            "p": (d.get("purpose", "") or "")[:200],
            "f": d.get("frameworks", []),
            "u": f"{prefix}/documents/{stem}/",
        })
    return json.dumps(entries, ensure_ascii=False, separators=(",", ":"))


def render_variant(figures, variant):
    """Render one variant's HTML template tree and return relative outputs."""
    template_dir = template_dir_for(variant)
    partials = load_partials(template_dir)
    all_values = set(PARTIALS) | set(figure_values(figures, variant))
    pages = []
    used_across = set()
    for template_name, out_rel in tuple(PAGES) + tuple(variant.extra_pages):
        html, used = render_page(
            template_name, figures, variant, template_dir, partials, out_rel=out_rel
        )
        pages.append((out_rel, html))
        used_across |= used

    # One page per corpus domain, from the shared domain template plus that
    # domain's per-page values. The dead-value check below covers the global
    # values (used by the fixed pages); each domain page's own leftover check in
    # render_page guarantees its DOMAIN_* placeholders all resolved.
    for dp in figures["domain_pages"]:
        html, _ = render_page(
            "domain.html", figures, variant, template_dir, partials,
            extra=domain_page_values(dp, variant), out_rel=f"{dp['domain']}/index.html"
        )
        pages.append((f"{dp['domain']}/index.html", html))

    # One page per document type, from the shared type template plus that type's
    # per-page values. Like the domain pages, each page's own leftover check in
    # render_page guarantees its TYPE_* placeholders all resolved. The "By document
    # type" chips on the landing page link here (/types/<slug>/).
    for tp in figures["type_pages"]:
        html, _ = render_page(
            "type.html", figures, variant, template_dir, partials,
            extra=type_page_values(tp, variant), out_rel=f"types/{tp['slug']}/index.html"
        )
        pages.append((f"types/{tp['slug']}/index.html", html))

    # On-site document (L2) pages: one per corpus DOMAIN document, built from
    # the enriched taxonomy (never from live prose), VARIANT-SCOPED by
    # document_routes so the frozen root/v2 trees are untouched. Root-level
    # specs are excluded (they have no domain page to anchor their area link).
    # Each page's own leftover check in render_page guarantees its DOC_*
    # placeholders all resolved.
    if variant.document_routes:
        full_docs = parse_taxonomy_full(TAXONOMY.read_text(encoding="utf-8"))
        docs_by_path = {d["path"]: d for d in full_docs}
        for d in full_docs:
            if d.get("domain") == ROOT_DOMAIN:
                continue
            out_rel = _doc_route_rel(d["path"])
            html, _ = render_page(
                "document.html", figures, variant, template_dir, partials,
                extra=document_page_values(d, docs_by_path, variant),
                out_rel=out_rel,
            )
            pages.append((out_rel, html))
        pages.append(("search-index.json", render_search_index(variant)))

    # The executive reading room (wave-2 PR-2a; extended to /v3 in PR #1638):
    # one on-site page per
    # registry-listed narrative page of a routed type, VARIANT-SCOPED by the
    # variant-table flag so the frozen root's page loops above are untouched
    # (the byte-identical-root mechanism for this new route class). Sources
    # are read ONLY after the renderer-confinement validator admits them
    # (registry-listed, normalized, git-tracked, under executive/ only), so
    # this loop extends the generator's read allow-list to the registry-listed
    # executive/ pages without the generator ever walking the repository.
    if variant.narrative_routes:
        # Every registry type must be a routed type: a future NEW narrative
        # type would otherwise fall through the filter below and silently
        # skip on-site rendering (PR-2b widened the tuple to all six
        # published types; this check keeps the widening honest).
        unrouted = sorted(
            {p["narrative_type"] for p in figures["narratives"]}
            - set(NARRATIVE_ROUTE_TYPES)
        )
        if unrouted:
            raise BuildError(
                "narrative registry type(s) with no on-site route (add to "
                f"NARRATIVE_ROUTE_TYPES): {', '.join(unrouted)}"
            )
        tracked = _tracked_executive_paths()
        seen_sources = set()
        seen_out_rels = {out_rel for out_rel, _ in pages}
        for page in figures["narratives"]:
            if page["narrative_type"] not in NARRATIVE_ROUTE_TYPES:
                continue
            source = narrative_source_file(page["path"], tracked, seen_sources)
            out_rel = narrative_out_rel(page)
            if out_rel in seen_out_rels:
                raise BuildError(
                    f"narrative route collides with an existing page: {out_rel}"
                )
            seen_out_rels.add(out_rel)
            body_html, toc = render_narrative_body(
                source.read_text(encoding="utf-8"), page["path"],
                narrative_shell_ids_for(variant),
            )
            html, _ = render_page(
                "narrative.html", figures, variant, template_dir, partials,
                extra=narrative_page_values(page, variant, out_rel, body_html, toc),
                out_rel=out_rel,
            )
            pages.append((out_rel, html))

    unused = sorted(all_values - used_across)
    if unused:
        raise BuildError(
            "value(s) used by no page (dead computation or a dropped placeholder): "
            f"{', '.join('{{' + k + '}}' for k in unused)}"
        )

    return pages


def render_site(figures):
    """Render every variant tree and return ``(dist-relative path, content)``.

    Each table row renders its own template tree. The indexable root tree
    alone emits crawler and discovery files, so a non-indexable staging tree
    cannot publish a competing root.
    """
    indexable_variant()
    pages = []
    for variant in VARIANTS:
        variant_pages = render_variant(figures, variant)
        pages.extend(
            (output_rel_for(variant, out_rel), html)
            for out_rel, html in variant_pages
        )
        if variant.indexable:
            html_page_rels = [out_rel for out_rel, _ in variant_pages]
            pages.append((output_rel_for(variant, "robots.txt"), render_robots_txt()))
            pages.append((
                output_rel_for(variant, "sitemap.xml"),
                render_sitemap(variant, html_page_rels),
            ))
            pages.append((
                output_rel_for(variant, "llms.txt"), render_llms_txt(figures, variant),
            ))
    return pages


# Conservative literal-figure detector (P-1.25.26 / S2). The CalVer (YYYY.MM.NNN)
# is the most distinctive corpus figure (it changes every PR), so a hardcoded
# CalVer literal in a template is an unambiguous regression from the {{CALVER}}
# token. Bare counts are deliberately NOT flagged (too false-positive-prone for a
# conservative check). This detector is CalVer-only; displayed corpus counts
# (documents, domains, types) are token-driven but are NOT covered here or by the
# manifest-drift check (the manifest carries link targets, not counts), so a
# hardcoded count literal is a separate, currently-unguarded class.
_CALVER_LITERAL_RE = re.compile(r"\b20\d\d\.\d\d\.\d+\b")


def hardcoded_calver_literals():
    """Return ["<relpath>:<lineno>", ...] for hardcoded CalVer literals in templates (empty = clean)."""
    hits = []
    for variant in VARIANTS:
        for tpl in sorted(template_dir_for(variant).rglob("*.html")):
            for lineno, line in enumerate(tpl.read_text(encoding="utf-8").splitlines(), 1):
                if _CALVER_LITERAL_RE.search(line):
                    hits.append(f"{tpl.relative_to(REPO_ROOT)}:{lineno}")
    return hits


def bare_root_relative_hrefs():
    """Return source locations of root-relative hrefs missing the BASE token.

    Templates and the generator's emitted-link expressions are both scanned:
    either source can otherwise reintroduce a link that escapes a prefixed site
    variant. A BASE-prefixed value begins with the token rather than a slash and
    therefore cannot match _ROOT_HREF_RE.
    """
    hits = []
    sources = [
        *(
            tpl for variant in VARIANTS
            for tpl in sorted(template_dir_for(variant).rglob("*.html"))
        ),
        Path(__file__),
    ]
    for source in sources:
        for lineno, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            if _ROOT_HREF_RE.search(line):
                hits.append(f"{source.relative_to(REPO_ROOT)}:{lineno}")
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Render the grclibrary.ai public site (landing, about, pack, per-domain, and per-type pages, plus the non-indexable staging trees: the /v2 executive routes (decisions/start/trust/coverage/library/how-its-built), the /v3 need-based path routes, on-site document pages, and client-side search, and the decisions/<subtype>/<slug>/ executive reading-room pages, one per registry narrative page, rendered on-site for both /v2 and /v3) from the live corpus.",
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
        manifest_text = render_corpus_link_manifest(figures, indexable_variant())
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
        # The committed corpus-link manifest is a generated artefact (like
        # taxonomy.yml / docs/portal.md): --check fails on drift between the
        # committed copy and a fresh build, the same way the taxonomy/portal
        # drift is gated.
        committed = (
            CORPUS_LINK_MANIFEST.read_text(encoding="utf-8")
            if CORPUS_LINK_MANIFEST.exists()
            else None
        )
        if committed != manifest_text:
            reason = "missing" if committed is None else "stale"
            print(
                f"web-generator --check FAIL: {CORPUS_LINK_MANIFEST.relative_to(REPO_ROOT)} "
                f"is {reason}; regenerate with `python3 .web/build.py`.",
                file=sys.stderr,
            )
            return 1
        # Conservative literal-figure detector (P-1.25.26 / S2): corpus figures
        # must come from generator tokens, never be hardcoded in a template.
        literal_hits = hardcoded_calver_literals()
        if literal_hits:
            token = "{{" + "CALVER" + "}}"
            print(
                f"web-generator --check FAIL: hardcoded CalVer literal(s) in "
                f"template(s) (use the {token} token, never a literal): "
                f"{', '.join(literal_hits)}.",
                file=sys.stderr,
            )
            return 1
        root_href_hits = bare_root_relative_hrefs()
        if root_href_hits:
            token = "{{" + "BASE" + "}}"
            print(
                f"web-generator --check FAIL: root-relative href(s) missing "
                f"the {token} prefix: {', '.join(root_href_hits)}.",
                file=sys.stderr,
            )
            return 1
        print(f"web-generator --check OK: corpus parses and every page renders. {summary}")
        return 0

    out_dir = Path(args.out).resolve() if args.out else DEFAULT_OUT
    written = []
    for out_rel, html in pages:
        out_file = out_dir / out_rel
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html, encoding="utf-8")
        written.append(out_rel)
    # The corpus-link manifest is a COMMITTED artefact (not part of the ephemeral
    # dist/ tree), so it is always written to its tracked path, independent of
    # --out, and committed in the same PR as any corpus/link change (paired surface).
    CORPUS_LINK_MANIFEST.write_text(manifest_text, encoding="utf-8")
    written.append(str(CORPUS_LINK_MANIFEST.relative_to(REPO_ROOT)))
    print(
        f"web-generator OK: wrote {len(written)} page(s) to {out_dir} "
        f"({', '.join(written)}). {summary}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
