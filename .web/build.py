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
committed ``.web/corpus-link-manifest.md``, self-scans this generator source for
the safeguard checks, and, for the hand-written edition check, reads
``governance/register-canonical-citations.md`` through gate D15's resolver
(``tools/check-alignment-register-on-pr.py`` and its alias and exclusion files);
none of these feeds published content.) By default its rendered output is the site under
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
per registry-listed narrative page: ALL 34 published narrative pages across the
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
render time from ``narrative.yml``. The allow-list additions are the twelve
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
                                   coupling-breakage detector, NOT a corpus gate. It ALSO fails on a stale committed ``corpus-link-manifest.md``, a hardcoded CalVer literal in a template, a root-relative href that skips the ``{{BASE}}`` token, or a hand-written standard edition that differs from the citations register (``stale_standard_editions``: the landing and v2 coverage "biblio-col" lists and the OWASP and EU AI Act entries of the For-AI pages; each listed name is resolved by gate D15's resolver, a register Standard ID or curated alias, and its edition must equal the row's Current version, must not be among the row's Superseded versions, and must not be marked ended by the Current version (after the year of a statute named by its year only the row's enumerated notes, the register's own text with its dates, numbers and amending Act name variable, may follow (``STATUTE_NOTE_FORMS``), and an EU instrument citation may end only with a short name enumerated for its row or the row's own Standard ID (``EU_INSTRUMENT_SHORT_NAMES``), so any other text after the edition fails and the failure says to update the allowlist if the register text changed legitimately); a name that resolves to no row but carries an edition, or whose topic carries an EU instrument number, reads as an edition or date, or is not descriptive (a numeric character or a word not in ``TOPIC_WORDS``), or that carries no edition and is not enumerated in ``UNRESOLVED_LIST_NAMES`` (which a For-AI name cannot use), also fails, as does a list item the check cannot parse (any text but whitespace after an item's ``</li>`` and before the next item or the list's close included, a For-AI item's text between its name and description spans, which must be one of the forms in ``FOR_AI_INTER_SPAN_FORMS``, a For-AI item whose description span does not run to its ``</li>``, whitespace aside, and the description of a For-AI item, which must be one enumerated in ``FOR_AI_DESCRIPTIONS`` for the row of every part of its name, split on " / " and " and ", that names one (resolved, mapped in ``FOR_AI_NAME_ROWS``, or named by a leading part); the OWASP entries are chosen by the row any part of the name resolves to, not by its literal prefix, with one fallback by spelling: a For-AI name that, NFKC-normalised with format characters removed and case-folded, contains "owasp" anywhere is compared too, so one that does not resolve fails, and every part of a compared compound name has its edition compared), a For-AI jurisdiction label whose instrument text is none of its forms in ``FOR_AI_LABEL_INSTRUMENTS``, or any other For-AI name enumerated in ``FOR_AI_NAME_TEXTS`` whose text is none of its forms there, or a form of either list after a name it is not enumerated for, a compared OWASP name enumerated in ``FOR_AI_OWASP_TEXTS`` whose text is a form of the OWASP branch in ``FOR_AI_INTER_SPAN_FORMS`` but none of its own forms there (text that is no form of the branch fails as unparsed, above), a For-AI name, part or piece not compared as an OWASP entry that names no row and is not enumerated in ``FOR_AI_UNCHECKED_NAMES``, an "id" list item outside every list read, a For-AI source without exactly one EU AI Act entry or on which a name of ``FOR_AI_LABEL_INSTRUMENTS`` or ``FOR_AI_NAME_TEXTS`` (case and spacing ignored), of ``FOR_AI_UNCHECKED_NAMES`` (matched exactly) or of ``FOR_AI_OWASP_TEXTS`` (case and spacing ignored, any trailing edition removed) is not the whole name of exactly one item or on which an item named by a name of ``FOR_AI_OWASP_TEXTS`` adds or drops a trailing edition (adding or dropping one needs a list update) or on which a name of ``FOR_AI_OWASP_TEXTS`` that names one item is not the only item, part or piece naming its register row in any spelling, or a configured source with no list read; names without an edition are out of scope, and so are the other For-AI editions (ISO/IEC 42001:2023, ISO/IEC 23894:2023, ISO/IEC 42005:2025, ISO 31000:2018, ISO/IEC 27001:2022 and the rest), which this check does not compare).
  python3 .web/build.py --out DIR  render into DIR instead of .web/dist/
"""

from __future__ import annotations

import argparse
import datetime
import importlib.util
import posixpath
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from html import unescape as html_unescape
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
    # Only templates that consume DOMAIN_RAIL_LENSES opt into its validation.
    domain_rail: bool = False


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
            narrative_routes=True, domain_rail=True),
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

# The twelve corpus domains, with the one-line scope description shown in the
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
    "crypto": "Crypto-asset and blockchain governance: classification, custody, and platform risk",
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


# The v2 domain page's closing three-lens "Go deeper" rail. Every other v2 page
# carries this block verbatim in its template; the domain template instead
# renders it from this table (via the DOMAIN_RAIL_LENSES value below) so the
# lens entry that IS the current domain page demotes to a non-link current-page
# marker instead of linking to itself (3b152 N4: 8 of the rail's 10 entries are
# domain pages, so the verbatim block self-linked on 8 of the domain pages).
# Each entry is (domain slug or None, BASE-relative path or None, label); the
# labels are template-authored HTML, already entity-escaped. A domain entry
# carries its slug and no path (the renderer derives its href from the slug, so
# the link destination cannot diverge from the validated slug); a None slug
# marks a non-domain page that can never be the current domain page, and only
# such an entry carries a hand-typed path.
V2_DOMAIN_RAIL_LENSES = (
    ("Security &amp; risk (CISO)", (
        ("security", None, "Security controls &amp; operations"),
        ("risk", None, "Risk methodology &amp; registers"),
        ("resilience", None, "Continuity, recovery &amp; incidents"),
    )),
    ("Compliance &amp; evidence", (
        ("compliance", None, "Regulatory mapping &amp; audit readiness"),
        ("privacy", None, "Privacy &amp; data-protection obligations"),
        ("governance", None, "Charters, policies &amp; registers"),
    )),
    ("Technology", (
        (None, "how-its-built/", "How the library is built &amp; gated"),
        ("architecture", None, "Reference architectures"),
        ("dev-security", None, "Secure development &amp; pipelines"),
        (None, "for-ai/", "For AI systems"),
    )),
)


def render_domain_rail_lenses(current_domain, generated_domains):
    """The three-lens rail for one v2 domain page: the shared lens block, except
    that the entry naming the current domain renders as a non-link current-page
    marker (aria-current, styled in the template) rather than a self-link. Fail
    closed on table drift (3b152 round-1 QA): a rail slug that names no
    GENERATED domain page (a renamed domain, or a domain whose last document
    was removed, including one whose stale DOMAIN_SCOPE key remains) is a loud
    build error, so neither case can leave the demotion silently dead or the
    rail linking to a page that is not built; and a domain entry's href is
    derived from its slug (an entry carrying both a slug and a hand-typed path,
    or neither, is a loud build error), so the link destination cannot diverge
    from the validated slug."""
    malformed = sorted(
        label for _, entries in V2_DOMAIN_RAIL_LENSES
        for slug, path, label in entries if (slug is None) == (path is None)
    )
    if malformed:
        raise BuildError(
            "V2_DOMAIN_RAIL_LENSES entr(y/ies) must carry exactly one of a "
            "domain slug (href derived from it) or a hand-typed path: "
            + ", ".join(malformed)
        )
    unknown = sorted({slug for _, entries in V2_DOMAIN_RAIL_LENSES
                      for slug, _, _ in entries if slug is not None}
                     - set(generated_domains))
    if unknown:
        raise BuildError(
            "V2_DOMAIN_RAIL_LENSES slug(s) name no generated domain page "
            "(a renamed domain, or every document in it removed?): "
            + ", ".join(unknown)
        )
    lenses = []
    for heading, entries in V2_DOMAIN_RAIL_LENSES:
        lines = ['        <div class="lens">', f"          <h3>{heading}</h3>"]
        for slug, path, label in entries:
            if slug == current_domain:
                lines.append(
                    f'          <span class="lens-here" aria-current="page">{label}</span>'
                )
            else:
                href_path = f"{slug}/" if slug is not None else path
                lines.append(
                    f'          <a href="{{{{BASE}}}}/{href_path}">{label}</a>'
                )
        lines.append("        </div>")
        lenses.append("\n".join(lines))
    return "\n".join(lenses)


def domain_page_values(dp, variant, generated_domains):
    """The per-page values for one domain page (merged on top of the shared
    values in render_page). SEO/attribute values are built from controlled
    strings (the domain name, the curated scope, the count), never from the
    README prose, so no quote-escaping is needed in the attribute context.
    ``generated_domains`` is the set of domain slugs that actually get pages
    this build, the fail-closed ground truth for the rail renderer."""
    name = dp["domain"]
    return {
        "DOMAIN_NAME": _esc(name),
        "DOMAIN_SCOPE_TEXT": _esc(dp["scope"]),
        "DOMAIN_PURPOSE": _esc(dp["purpose"]),
        "DOMAIN_DOC_COUNT": str(dp["count"]),
        # The documents lede's noun is COMPUTED with the count (3b152 round-1
        # QA, the same grammar class as the leadership lede below): exactly one
        # document reads "reference document". A domain page exists only for a
        # domain with at least one document, so zero never renders here. Like
        # the narrative tokens this is inert on templates that omit the token,
        # so v1 and v3 output stays byte-identical.
        "DOMAIN_DOC_NOUN": (
            "reference document" if dp["count"] == 1 else "reference documents"
        ),
        "DOMAIN_DOC_ROWS": render_domain_doc_rows(dp, variant),
        # The leadership-page (narrative registry) join, consumed by the v2
        # and v3 domain templates. Per-page extra= values are inert in a template
        # that does not reference them (the unknown-placeholder error fires only
        # on placeholders a template contains), so the untouched v1 template's
        # output stays byte-identical. The count is COMPUTED, never typed.
        "DOMAIN_NARRATIVE_COUNT": str(len(dp["narratives"])),
        # The lede's noun-verb agreement is COMPUTED with the count (3b152 N2):
        # exactly one page reads "page draws"; zero keeps the plural ("0 ...
        # pages draw"), consistent with the declared-gap row beneath it. Like
        # the rows/count values this is inert on templates that omit the token.
        "DOMAIN_NARRATIVE_PAGES_DRAW": (
            "page draws" if len(dp["narratives"]) == 1 else "pages draw"
        ),
        "DOMAIN_NARRATIVE_ROWS": render_domain_narrative_rows(dp),
        # Only rail variants get the key, so a template that uses the rail on a
        # variant without the flag fails the unknown-placeholder check instead of
        # rendering an empty rail (3b152 round-3 claude N1).
        **({"DOMAIN_RAIL_LENSES": render_domain_rail_lenses(name, generated_domains)}
           if variant.domain_rail else {}),
        "DOMAIN_TITLE": f"{_esc(name)} domain: GRC Library",
        "DOMAIN_SEO_DESC": _esc(
            f"{dp['scope']}. {dp['count']} governance documents in the {name} "
            "domain of the open, CC BY-SA 4.0 GRC Library."
        ),
        # Only v2 consumes this agreed description; keep the legacy token.
        "DOMAIN_SEO_DESC_AGREED": _esc(
            f"{dp['scope']}. {dp['count']} governance "
            f"{'document' if dp['count'] == 1 else 'documents'} in the {name} "
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
        # The type lede's noun is COMPUTED with the count (3b152 round-1 QA,
        # the same grammar class as the domain ledes; the live corpus has
        # one-document types, Checklist and Roadmap): exactly one document
        # reads "reference document". Inert on templates that omit the token,
        # so v1 and v3 output stays byte-identical.
        "TYPE_DOC_NOUN": (
            "reference document" if tp["count"] == 1 else "reference documents"
        ),
        "TYPE_DOC_ROWS": render_type_doc_rows(tp, variant),
        "TYPE_TITLE": f"{_esc(name)} documents: GRC Library",
        "TYPE_SEO_DESC": _esc(
            f"{tp['scope']}. {tp['count']} {name}-type documents in the open, "
            "CC BY-SA 4.0 GRC Library."
        ),
        # Only v2 consumes this agreed description; keep the legacy token.
        "TYPE_SEO_DESC_AGREED": _esc(
            f"{tp['scope']}. {tp['count']} {name}-type "
            f"{'document' if tp['count'] == 1 else 'documents'} in the open, "
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
    copy is accurate (PR #1638; RR-1). All 34 narratives carry domain tags."""
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
    generated_domains = set(d["domain"] for d in figures["domain_pages"])
    for dp in figures["domain_pages"]:
        html, _ = render_page(
            "domain.html", figures, variant, template_dir, partials,
            extra=domain_page_values(dp, variant, generated_domains),
            out_rel=f"{dp['domain']}/index.html"
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


# Hand-written standard editions (3b380). Most site figures are generated, but a few
# lists name standards by hand, and their editions drifted behind the citations
# register until PR #2846 corrected them. The register is the authority; this check
# compares the hand-written editions with it and does not generate the lists.
CITATIONS_REGISTER = REPO_ROOT / "governance" / "register-canonical-citations.md"
# Gate D15's checker, whose resolver (Standard ID or curated alias, from
# tools/alignment-register-aliases.json) is reused rather than re-implemented.
D15_CHECKER = REPO_ROOT / "tools" / "check-alignment-register-on-pr.py"
# (template path under .web/, list kind). "biblio" reads every <li> inside each <div>
# whose class list contains "biblio-col" (whatever its other attributes or classes),
# up to that div's own closing tag (nested divs are counted), each an "id" span and a
# "topic" span; "for-ai" reads every <li> of the For-AI resource index and checks its
# OWASP entries and its one EU AI Act entry. Items are told apart by their offset in
# the source, not their line, so two items on one line are both read. These fail the
# check: an <li> of a list read that the item pattern cannot parse ("unparsed"); a
# source with no list read; an <li> anywhere in the source with an "id" span anywhere
# inside it (as its first child or nested, say in an <a>) that is not among the items
# read ("incomplete"); and a For-AI source without exactly one EU AI Act entry
# ("incomplete"). So a markup change to an <li> with an "id" span, to a "biblio-col"
# div or to the EU AI Act entry fails rather than silently dropping the entry.
EDITION_LIST_SOURCES = (
    ("templates/landing.html", "biblio"),
    ("templates-v2/coverage.html", "biblio"),
    ("templates/for-ai.html", "for-ai"),
    ("templates-v2/for-ai.html", "for-ai"),
    ("templates-v3/for-ai.html", "for-ai"),
)
_BIBLIO_ITEM_RE = re.compile(
    r'<li><span class="id">(?P<name>[^<]*)</span><span class="topic">(?P<topic>[^<]*)</span></li>'
)
# A <div> open tag whose class attribute contains the token "biblio-col", any <div>
# open or close tag (to find that div's own close), an <li> item up to its close (or
# the next <li> or the end of the column), and, for the completeness check, a span
# with the class token "id" anywhere inside such an item. Tag and attribute names are
# matched in any case ("<LI>", "CLASS"), and a class value may be quoted or unquoted
# (class=id); an item found this way that the strict item pattern cannot parse fails as
# unparsed or incomplete, so the wider match only widens what fails.
_BIBLIO_COL_RE = re.compile(
    r"""<div\b[^>]*\bclass\s*=\s*(?:["'](?:[^"']*\s)?biblio-col(?:\s[^"']*)?["']|biblio-col(?=[\s/>]))[^>]*>""",
    re.I,
)
_DIV_TAG_RE = re.compile(r"<(/?)div\b[^>]*>", re.I)
_LI_RE = re.compile(r"<li\b.*?(?:</li>|(?=<li\b)|\Z)", re.S | re.I)
# The text after an item's </li>, up to the next <li>, the list's close (</ul> or
# </ol>) or the end of the list read. Only whitespace is accepted there; any other
# text ("</li> (withdrawn)") fails the item as unparsed.
_LI_GAP_RE = re.compile(r".*?(?=<li\b|</[uo]l\s*>|\Z)", re.S | re.I)
_ID_SPAN_RE = re.compile(
    r"""<span\b[^>]*\bclass\s*=\s*(?:["'](?:[^"']*\s)?id(?:\s[^"']*)?["']|id(?=[\s/>]))""", re.I
)
# The For-AI resource index runs from its heading to the next section heading.
_FOR_AI_INDEX_RE = re.compile(r"<h2>Resource index\b")
_FOR_AI_ITEM_RE = re.compile(
    r'<li><span class="(?:fa-inst|row-name)">(?P<name>[^<]*)</span>(?P<rest>.*?)'
    r'<span class="(?:fa-cov|row-desc)">'
)
# The For-AI pages name the EU AI Act as "European Union, AI Act (Regulation ...)",
# split across the name span on v3; the parenthetical is its edition.
_FOR_AI_EU_AI_ACT_RE = re.compile(
    r"^European Union, AI Act \((?P<edition>Regulation (?:[^()]|\([^()]*\))*)\)"
)
FOR_AI_EU_AI_ACT_ID = "EU AI Act"
# An item that names the EU AI Act in some other shape; it fails as unparsed.
_FOR_AI_EU_AI_ACT_LOOSE_RE = re.compile(r"\b(?:European Union|EU)\b.*\bAI Act\b")
# The external-link marker the templates write after a link's text (``_plain`` drops
# it, and only it): at 5c1e2b6a the v2 coverage page carries it 60 times (57 in its
# bibliography list; PR #2848 added one in its prose) and the landing page and the
# three For-AI pages none. Any other span with the class "ext"
# ("<span class="ext"> (repealed)</span>") is read as text.
EXT_LINK_MARKER = '<span class="ext">&#8599;</span>'
# A For-AI item's description span runs to the end of the item; whitespace may stand
# between its </span> and the </li>. An item whose description span does not run to its
# close this way fails as unparsed, whatever its name.
_FOR_AI_DESC_RE = re.compile(r"(?P<desc>.*)</span>\s*</li>", re.S)
# The descriptions (the "fa-cov" or "row-desc" span, as text: ``_plain``, so a link is
# its anchor text) a For-AI item may carry, keyed by the register Standard ID of each
# row its name names (``_for_ai_name_rows``; the EU AI Act entry under
# ``FOR_AI_EU_AI_ACT_ID``), enumerated from the three For-AI templates at d6b7c37a
# (93 of the 105 items, naming 37 rows, one description per row, 27 distinct
# descriptions). A compound name ("A / B", "A and B") names the row of each of its
# parts, so the description must be enumerated for every such row. The description of
# an item that names a row is one of that row's, or the item fails as unparsed ("This
# 2026 edition is withdrawn."), whatever words it uses; an item that names no row keeps
# its description unchecked (at d6b7c37a the 12 items "NIST AI 100-2e2025", "NIST AI
# 100-4", "Model Cards" and "Datasheets for Datasets", three per name, which have no
# register row), and only a name enumerated in ``FOR_AI_UNCHECKED_NAMES`` may name no
# row (a part of a compared OWASP name that names no row fails as unresolved, as
# ``UNRESOLVED_LIST_NAMES`` applies to bibliography lists only: "OWASP MCP Top 10 /
# IEC 62443"). If a template's text changed legitimately, update this allowlist.
FOR_AI_DESCRIPTIONS = {
    FOR_AI_EU_AI_ACT_ID: frozenset({
        "Documented in the EU AI annex (which also reflects the in-force Digital Omnibus on AI, "
        "Regulation (EU) 2026/1744).",
    }),
    "ISO 31000": frozenset({"Engaged across the risk domain and the cross-framework matrix."}),
    "ISO/IEC 23894": frozenset({"Documented in the AI model-risk framework."}),
    "ISO/IEC 42001": frozenset({"Documented in the AI governance and risk framework."}),
    "ISO/IEC 42005": frozenset({"Documented in the AI system impact-assessment procedure."}),
    "MITRE ATLAS": frozenset({
        "Engaged in the adversarial-test reference and the AI security tooling landscape.",
    }),
    "NIST AI 600-1": frozenset({"Documented in the AI compliance policy."}),
    "NIST AI RMF": frozenset({"Documented in the AI governance and risk framework."}),
    "NIST CSF": frozenset({
        "NIST CSF 2.0 is mapped in the compliance matrix; selected NIST SP 800-53 Rev. 5 control "
        "families are mapped in the reverse framework-control crosswalk.",
    }),
    "NIST SP 800-218A": frozenset({"Documented in the AI and agentic development-security standard."}),
    "OWASP GenAI Red Teaming Guide": frozenset({
        "Documented in the AI and agentic development-security standard.",
    }),
    "OWASP LLM Top 10": frozenset({"Documented in the AI security and risk standard."}),
    "OWASP MCP Top 10": frozenset({
        "Documented in the AI and agentic development-security standard.",
    }),
    # Named by a leading part of the name (``_named_prefix``): "CSA AI Controls Matrix
    # (AICM)", "CSA Cloud Controls Matrix (CCM)", "ISO/IEC 5259 series".
    "CSA AICM": frozenset({"Mapped in the compliance matrix."}),
    "CSA CCM": frozenset({"Mapped in the compliance matrix."}),
    "ISO/IEC 5259": frozenset({"Documented in the AI data-quality and readiness standard."}),
    # The parts of "ISO/IEC 27001:2022 and 27002:2022".
    "ISO/IEC 27001": frozenset({
        "Both are documented in the information-security policy; ISO/IEC 27001:2022 is mapped in "
        "the compliance matrix.",
    }),
    "ISO/IEC 27002": frozenset({
        "Both are documented in the information-security policy; ISO/IEC 27001:2022 is mapped in "
        "the compliance matrix.",
    }),
    # The parts of "ISO/IEC 27701:2025 and the GDPR (Regulation (EU) 2016/679)".
    "ISO/IEC 27701": frozenset({
        "ISO/IEC 27701:2025 is documented in the privacy programme charter and the privacy and data "
        "governance policy; the GDPR is documented in the EU privacy annex.",
    }),
    "EU GDPR": frozenset({
        "ISO/IEC 27701:2025 is documented in the privacy programme charter and the privacy and data "
        "governance policy; the GDPR is documented in the EU privacy annex.",
    }),
    # The rows of ``FOR_AI_NAME_ROWS``.
    "OECD AI Principles": frozenset({"Cited in the canonical citations register."}),
    "Colorado AI Act": frozenset({"Documented in the Colorado AI annex."}),
    "NYC Local Law 144 (AEDT)": frozenset({"Documented in the NYC AI annex."}),
    "US CCPA Regulations 2026": frozenset({"Documented in the California ADMT annex."}),
    "Canada TBS Directive on Automated Decision-Making": frozenset({"Documented in the Canada AI annex."}),
    "Australia Privacy Act": frozenset({"Documented in the Australia AI annex."}),
    "Australia Voluntary AI Safety Standard": frozenset({"Documented in the Australia AI annex."}),
    "Singapore Model AI Governance Framework for Generative AI": frozenset({
        "Documented in the Singapore AI annex.",
    }),
    "Malaysia AIGE": frozenset({"Documented in the Malaysia AI annex."}),
    "UK AI regulation white paper": frozenset({"Documented in the United Kingdom AI annex."}),
    "UK AI regulation government response": frozenset({"Documented in the United Kingdom AI annex."}),
    "South Korea AI Basic Act": frozenset({"Documented in the South Korea AI annex."}),
    "Illinois HB 3773": frozenset({"Documented in the Illinois AI annex."}),
    "Texas TRAIGA": frozenset({"Documented in the Texas AI annex."}),
    "US OMB M-25-21": frozenset({"Documented in the US federal AI annex."}),
    "US OMB M-25-22": frozenset({"Documented in the US federal AI annex."}),
    "US OMB M-26-04": frozenset({"Documented in the US federal AI annex."}),
}
# For-AI names worded unlike any register Standard ID or curated alias, mapped to the
# Standard IDs of the rows they name, so their descriptions are checked. A name (or a
# part of a compound name) is matched as the resolver matches one (``identity_key``:
# case and spacing ignored), and only for the description check: no edition is read
# from these names. A jurisdiction label names the rows of the instruments its item
# lists between the name and description spans (``FOR_AI_INTER_SPAN_FORMS``), as on the
# three For-AI templates at d6b7c37a: "United States, Colorado, AI Act (SB24-205) and
# its automated-decision-making re-enactment (SB26-189)." names the Colorado AI Act
# row, and "Australia, Privacy Act automated-decision transparency amendments
# (commencing 2026) and the Voluntary AI Safety Standard." names two rows; the label
# must be the whole name and its item must list that instrument text, one of its forms
# in ``FOR_AI_LABEL_INSTRUMENTS``. A mapped
# Standard ID that is no register row stops the check (``BuildError``); if the register
# renames a row, update this mapping. These are not curated aliases, so gate D15 does
# not read them.
FOR_AI_NAME_ROWS = {
    "OECD Recommendation on AI": ("OECD AI Principles",),
    # The second part of "ISO/IEC 27701:2025 and the GDPR (Regulation (EU) 2016/679)".
    "the GDPR (Regulation (EU) 2016/679)": ("EU GDPR",),
    "United States, Colorado": ("Colorado AI Act",),
    "United States, New York City": ("NYC Local Law 144 (AEDT)",),
    "United States, California": ("US CCPA Regulations 2026",),
    "Canada": ("Canada TBS Directive on Automated Decision-Making",),
    "Australia": ("Australia Privacy Act", "Australia Voluntary AI Safety Standard"),
    "Singapore": ("Singapore Model AI Governance Framework for Generative AI",),
    "Malaysia": ("Malaysia AIGE",),
    "United Kingdom": ("UK AI regulation white paper", "UK AI regulation government response"),
    "South Korea": ("South Korea AI Basic Act",),
    "United States, Illinois": ("Illinois HB 3773",),
    "United States, Texas": ("Texas TRAIGA",),
    "United States, federal": ("US OMB M-25-21", "US OMB M-25-22", "US OMB M-26-04"),
}
# The instrument text each jurisdiction label of ``FOR_AI_NAME_ROWS`` lists between its
# name and description spans (as text: ``_plain``), the one form that names the label's
# mapped rows, enumerated from the three For-AI templates at d6b7c37a (12 labels, one
# form each, the same on all three pages; every form is also in
# ``FOR_AI_INTER_SPAN_FORMS``). A label is matched as the whole name, as
# ``FOR_AI_NAME_ROWS`` matches it (``identity_key``), and maps to its rows only as the
# whole name, not as a part of a compound name. A label whose text is none of its forms
# (the empty text included), or a label's form after any other name ("United States,
# Texas" with Colorado's instrument text, "Canada" with Colorado's), fails as a
# mismatched instrument, whatever its description. Each label names exactly one item on
# every For-AI page, matched as the whole name; a page where a label names no item or
# more than one fails as incomplete, naming the page and the label. If a template's text
# changed legitimately, update this allowlist.
FOR_AI_LABEL_INSTRUMENTS = {
    "United States, Colorado": frozenset({
        ", AI Act (SB24-205) and its automated-decision-making re-enactment (SB26-189).",
    }),
    "United States, New York City": frozenset({
        ", Local Law 144 on automated employment decision tools.",
    }),
    "United States, California": frozenset({
        ", CCPA regulations on automated decision-making technology (11 CCR Article 11, "
        "sections 7200 to 7222).",
    }),
    "Canada": frozenset({
        ", Treasury Board Directive on Automated Decision-Making (in force) and provincial and "
        "sectoral instruments.",
    }),
    "Australia": frozenset({
        ", Privacy Act automated-decision transparency amendments (commencing 2026) and the "
        "Voluntary AI Safety Standard.",
    }),
    "Singapore": frozenset({
        ", Model AI Governance Framework for Generative AI (advisory, not legislation).",
    }),
    "Malaysia": frozenset({
        ", National Guidelines on AI Governance and Ethics (MOSTI, 2024; voluntary, seven "
        "principles).",
    }),
    "United Kingdom": frozenset({
        ", pro-innovation AI regulation framework (CP 815 white paper, 2023, and CP 1019 "
        "government response, 2024; non-statutory, five principles applied by existing "
        "regulators).",
    }),
    "South Korea": frozenset({
        ", Framework Act on AI (AI Basic Act, Law No. 20676, in force 22 January 2026).",
    }),
    "United States, Illinois": frozenset({
        ", AI in employment (HB 3773 / Public Act 103-0804), effective 1 January 2026.",
    }),
    "United States, Texas": frozenset({
        ", Responsible Artificial Intelligence Governance Act (TRAIGA, HB 149), effective "
        "1 January 2026.",
    }),
    "United States, federal": frozenset({
        ", OMB memoranda M-25-21 (agency use of AI), M-25-22 (AI acquisition), and M-26-04 "
        "(Unbiased AI Principles for procured LLMs), binding on federal agencies and reaching "
        "vendors through contract terms.",
    }),
}
# The text each For-AI name on the "" branch (``_for_ai_branch``) that is not a
# jurisdiction label lists between its name and description spans (as text: ``_plain``),
# enumerated from the three For-AI templates at 703abaf4 (19 names, one form each, the
# same on all three pages; the two CSA names share "."). A name is matched as a label is
# (``identity_key``: case and spacing ignored). A name whose text is none of its forms
# (the empty text included: "NIST Cybersecurity Framework 2.0" without " and NIST SP
# 800-53 Rev. 5."), or a form enumerated here or in ``FOR_AI_LABEL_INSTRUMENTS`` after a
# name it is not enumerated for ("ISO 31000:2018" with ", AI management system.",
# "ISO/IEC 42001:2023" with "(OECD/LEGAL/0449).", a renamed item), fails as a
# mismatched instrument, whatever its description; only the empty text may follow a name
# enumerated in neither. Each name here names exactly one item on every For-AI page,
# matched as a label is; a page where it names no item or more than one (the item
# removed, doubled, replaced by a copy of another, or renamed with its text emptied)
# fails as incomplete, naming the page and the name. If a template's text changed
# legitimately, update this allowlist.
FOR_AI_NAME_TEXTS = {
    "ISO/IEC 42001:2023": frozenset({", AI management system."}),
    "ISO/IEC 23894:2023": frozenset({", AI risk-management guidance."}),
    "ISO/IEC 42005:2025": frozenset({", AI system impact assessment."}),
    "NIST AI 100-1": frozenset({", AI Risk Management Framework 1.0."}),
    "NIST AI 600-1": frozenset({", Generative AI Profile."}),
    "NIST AI 100-2e2025": frozenset({", Adversarial Machine Learning taxonomy."}),
    "NIST AI 100-4": frozenset({", Reducing Risks Posed by Synthetic Content."}),
    "NIST SP 800-218A": frozenset({", Secure Software Development for Generative AI."}),
    "MITRE ATLAS": frozenset({", adversarial threat landscape for AI systems."}),
    "OECD Recommendation on AI": frozenset({"(OECD/LEGAL/0449)."}),
    "ISO/IEC 5259 series": frozenset({", data quality for analytics and machine learning."}),
    "Model Cards": frozenset({", from the 2019 research paper that introduced the practice."}),
    "Datasheets for Datasets": frozenset({", from the 2018 research paper that introduced it."}),
    "ISO 31000:2018": frozenset({", risk management."}),
    "ISO/IEC 27001:2022 and 27002:2022": frozenset({", information-security management and controls."}),
    "ISO/IEC 27701:2025 and the GDPR (Regulation (EU) 2016/679)": frozenset({
        ", privacy management and data protection.",
    }),
    "NIST Cybersecurity Framework 2.0": frozenset({"and NIST SP 800-53 Rev. 5."}),
    "CSA AI Controls Matrix (AICM)": frozenset({"."}),
    "CSA Cloud Controls Matrix (CCM)": frozenset({"."}),
}
# Every name whose text is enumerated: the jurisdiction labels and the other names.
FOR_AI_ITEM_TEXTS = {**FOR_AI_LABEL_INSTRUMENTS, **FOR_AI_NAME_TEXTS}
# The For-AI names compared as OWASP entries (``_for_ai_branch``), each with the text it
# lists between its name and description spans (as text: ``_plain``), enumerated from
# the three For-AI templates at d60f7774 (3 names, one form each, "." after every name
# on all three pages). A name is matched with case and spacing ignored (``identity_key``)
# and with any trailing edition removed, whether or not one was present
# (``_for_ai_owasp_key``): the edition comparison checks its value against the register,
# so "OWASP Top 10 for LLM Applications 2025" is this list's first name with a stale
# edition (a mismatch), and "OWASP Top 10 for LLM Applications" is that name with its
# edition dropped. An item named by a name here carries a trailing edition exactly when
# that name does; an item that drops or adds one ("OWASP Top 10 for LLM Applications",
# "OWASP GenAI Red Teaming Guide 1.0") fails as incomplete, naming the page and the
# item, so adding or dropping an edition needs a list update. Text that is none of the
# "OWASP" branch's forms (``FOR_AI_INTER_SPAN_FORMS``) fails the item as unparsed; a name
# here whose text is a form of that branch but none of its own (the empty text
# included) fails as a mismatched instrument, whatever its description; the shared "."
# may follow any other compared name, which fails if it does not resolve. Each name here
# names exactly one item on every For-AI page; a page where it names no item or more
# than one (the item removed, doubled, with or without an edition, replaced by a copy of
# another OWASP item, or renamed) fails as incomplete, naming the page and the name, and
# so does a page where another item, part of a compound name or piece of one names the
# register row of a name here in any spelling (counted over ``_for_ai_branch``'s keys: a
# copy named by the row's Standard ID, "OWASP LLM Top 10 2026", or "OWASP MCP Top 10 /
# OWASP GenAI Red Teaming Guide" beside both items). If a template's text changed
# legitimately, update this allowlist.
FOR_AI_OWASP_TEXTS = {
    "OWASP Top 10 for LLM Applications 2026": frozenset({"."}),
    "OWASP MCP Top 10": frozenset({"."}),
    "OWASP GenAI Red Teaming Guide": frozenset({"."}),
}
# The text a For-AI item may carry between its name span and its description span
# (for the EU AI Act entry, after its citation), as text (``_plain``), enumerated per
# branch from the three For-AI templates at 5c1e2b6a (105 items, 31 distinct forms):
# "OWASP" for an item compared as an OWASP entry (``_for_ai_branch``; 9 items, all
# ".", the form of each name in ``FOR_AI_OWASP_TEXTS``, which this branch is built
# from), the EU AI Act entry (3 items), and "" for every other item (93 items, 30
# forms, each enumerated for its name in ``FOR_AI_ITEM_TEXTS``, which this branch is
# built from). The empty text is accepted on every branch by the branch check; a name of
# ``FOR_AI_OWASP_TEXTS`` or ``FOR_AI_ITEM_TEXTS`` still needs one of its own forms. Any
# text that is none of its branch's forms fails the item as unparsed ("</span>
# (repealed).", "</span> 2024 edition (withdrawn)."), whatever words it uses; if a
# template's text changed legitimately, update this allowlist (on the "" branch,
# ``FOR_AI_NAME_TEXTS`` or ``FOR_AI_LABEL_INSTRUMENTS``; on the "OWASP" branch,
# ``FOR_AI_OWASP_TEXTS``).
FOR_AI_INTER_SPAN_FORMS = {
    "OWASP": frozenset({""}).union(*FOR_AI_OWASP_TEXTS.values()),
    FOR_AI_EU_AI_ACT_ID: frozenset({"", ", in force and phasing in."}),
    "": frozenset({""}).union(*FOR_AI_ITEM_TEXTS.values()),
}
# The For-AI names, or parts of names, that may name no register row, so their
# descriptions are not checked, enumerated from the three For-AI templates at d6b7c37a
# (12 items, three per name). A name is matched exactly as written. Any other name, part
# or piece of an item that is not compared as an OWASP entry and names no row
# (``_for_ai_name_rows``) fails as unchecked ("United States, Texas (TRAIGA)", "Model
# Card"), whatever words it uses; add a register row or curated alias for it or map it
# in ``FOR_AI_NAME_ROWS``, or, if it legitimately names no row, add it here. Each name
# here is the whole name of exactly one item on every For-AI page, matched exactly; a
# page where it names no item or more than one ("Model Cards" given to a second item)
# fails as incomplete, naming the page and the name. A name also in
# ``FOR_AI_NAME_TEXTS`` is counted both ways and fails once if either count is not one.
FOR_AI_UNCHECKED_NAMES = frozenset({
    "NIST AI 100-2e2025", "NIST AI 100-4", "Model Cards", "Datasheets for Datasets",
})
# A For-AI name, or a part of one split on " / ", that names no row whole is split
# again on " and " ("ISO/IEC 27001:2022 and 27002:2022"). A later part that begins with
# a digit takes the designator before the first part's number (``_SHARED_PREFIX_RE``,
# "ISO/IEC "), so "27002:2022" is read as "ISO/IEC 27002:2022".
_COMPOUND_AND_SPLIT_RE = re.compile(r"\s+and\s+")
_SHARED_PREFIX_RE = re.compile(r"\D*?\s(?=\d)")
# The For-AI entries compared are those of the register rows whose Standard ID begins
# with this word and a space (the OWASP rows), chosen by the row the name resolves to.
FOR_AI_COMPARED_ID_PREFIX = "OWASP "
# A For-AI name whose text, after NFKC normalisation with format characters (Unicode
# category Cf, such as a zero-width space) removed and case folding, contains this
# anywhere (as a word or inside one: "OWASP's", "OWASP-Top", a fullwidth "OWASP") is
# compared as an OWASP entry too, so one that does not resolve fails.
FOR_AI_COMPARED_WORD = "owasp"
# A compound name ("UK GDPR / DPA 2018") is split into its parts here, as gate D15
# splits a cell.
_COMPOUND_NAME_SPLIT_RE = re.compile(r"\s+/\s+")
# A trailing token is an edition only in one of these shapes: a dotted version, a v- or
# Rev.-prefixed number, or a year. Any other trailing number is part of the name
# ("IEC 62443", "EU eIDAS 2").
_EDITION_SHAPE_RE = re.compile(
    r"(?:v|Rev\.?\s*)?\d+(?:\.\d+)+|(?:v|Rev\.?\s*)\d+|(?:19|20)\d\d", re.I
)
# A token in an edition shape at word boundaries anywhere in a name: a name that resolves
# to no row and holds one carries an edition ("OWASP Top Ten (2025) (repealed)",
# "FooStandard 2.0 (withdrawn)"), however the text after it reads.
_EDITION_TOKEN_IN_NAME_RE = re.compile(rf"(?<!\w)(?:{_EDITION_SHAPE_RE.pattern})(?!\w)", re.I)
# Editions are compared by their numbers ("v1.1" and "1.1", "(2026)" and "2026",
# "Regulation (EU) 2024/1689" and "Regulation 2024/1689" are equal).
_EDITION_NUMBER_RE = re.compile(r"\d+(?:[./]\d+)*")
_YEAR_RE = re.compile(r"(?:19|20)\d\d")
# The register rows of statutes the site names by their enactment year ("Australia
# Privacy Act 1988", "India DPDPA 2023"), with the notes their Current version may carry
# after the year. Only for these rows may a listed year match a Current version that
# continues past the year (``edition_matches``); every other row, including a bare-year
# edition (ISO, COBIT, OWASP), is compared by its numbers alone.
#
# The notes are enumerated, not patterned: each form is the register's own text with
# only its variable parts as slots (``_STATUTE_SLOTS``: a date, a year, an Act number,
# a G.S.R. number, an amending Act name from ``STATUTE_AMENDING_ACTS``). The text
# after the year is split at each ";" outside parentheses; its first part must equal one
# of the row's "opening" forms, and each later part, after one space, one of its
# "clauses" forms, each form at most once. Anything else fails closed, and the failure
# says to update this allowlist when the register text changed legitimately.
# Sources, governance/register-canonical-citations.md as of 2026-10-18:
# * Australia Privacy Act (Current version): "1988, as amended by the Privacy and Other
#   Legislation Amendment Act 2024 (Cth) No. 128, 2024 (Royal Assent 10 December 2024);
#   the automated-decision transparency obligation (Australian Privacy Principles 1.7
#   to 1.9, Schedule 1 Part 15) commences 10 December 2026".
# * India DPDPA (Current version): "2023 (Act enacted 2023-08-11); Act brought into force
#   by G.S.R. 843(E) of 13 November 2025 on a staged schedule under s. 1(2) (...; core
#   substantive regime and the Board's principal inquiry-and-penalty functions at 18
#   months, around 13 May 2027); Digital Personal Data Protection Rules 2025 (G.S.R.
#   846(E)) notified the same day commence on a matching rule 1(2)-(4) schedule". The
#   short Rules clause "Rules 2025 commence 2025-11-13" is not the register's text and
#   fails.
STATUTE_NOTE_FORMS = {
    "Australia Privacy Act": {
        "opening": (
            ", as amended by {amending_act} (Cth) No. {number}, {year} (Royal Assent {date})",
        ),
        "clauses": (
            "the automated-decision transparency obligation (Australian Privacy Principles 1.7 "
            "to 1.9, Schedule 1 Part 15) commences {date}",
        ),
    },
    "India DPDPA": {
        "opening": (
            " (Act enacted {iso_date})",
        ),
        "clauses": (
            "Act brought into force by G.S.R. {gsr} of {date} on a staged schedule under s. 1(2) "
            "(definitions and Board establishment immediate; consent-manager registration s. 6(9) "
            "at 12 months; core substantive regime and the Board's principal inquiry-and-penalty "
            "functions at 18 months, around {date})",
            "Digital Personal Data Protection Rules {year} (G.S.R. {gsr}) notified the same day "
            "commence on a matching rule 1(2)-(4) schedule",
        ),
    },
}
STATUTE_YEAR_ROWS = frozenset(STATUTE_NOTE_FORMS)
# The amending Act names the {amending_act} slot takes, enumerated from the register
# (the Australia Privacy Act row as of 2026-10-18). Any other name fails, so no wording
# of ending, displacement or succession can enter through the slot ("the Privacy Repeal
# Amendment Act 2026"); if the register names a new amending Act legitimately, add it here.
STATUTE_AMENDING_ACTS = frozenset({"the Privacy and Other Legislation Amendment Act 2024"})
# The variable parts of the forms, matched as ASCII (a digit slot takes no other
# script's digits).
_STATUTE_SLOTS = {
    "amending_act": "|".join(re.escape(name) for name in sorted(STATUTE_AMENDING_ACTS)),
    "number": r"\d{1,4}",
    "year": r"(?:19|20)\d\d",
    "date": r"\d{1,2} (?:January|February|March|April|May|June|July|August|September|October"
            r"|November|December) (?:19|20)\d\d",
    "iso_date": r"(?:19|20)\d\d-\d\d-\d\d",
    "gsr": r"\d{1,4}\(E\)",
}


def _statute_form_re(form):
    parts = re.split(r"\{(\w+)\}", form)
    return re.compile("".join(
        re.escape(part) if i % 2 == 0 else f"(?:{_STATUTE_SLOTS[part]})" for i, part in enumerate(parts)
    ), re.ASCII)


_STATUTE_NOTE_RES = {
    row: {kind: tuple(_statute_form_re(f) for f in forms[kind]) for kind in ("opening", "clauses")}
    for row, forms in STATUTE_NOTE_FORMS.items()
}
# Succession wording that no statute note may carry, even inside a slot (an amending Act
# named "the Successor Amendment Act 2026", "the Privacy Act Sunset Amendment Act 2026",
# "the Privacy Abrogation Amendment Act 2026").
_SUCCESSION_RE = re.compile(
    r"\b(?:successor|succeed\w*|replac\w*|abolish\w*|end(?:s|ed|ing)?|terminat\w*|sunset\w*"
    r"|abrogat\w*)\b",
    re.I,
)
# Wording that marks an edition ended: the passive or state forms ("superseded",
# "succeeded by", "repealed", "withdrawn", "deprecated", "obsolete", "retired",
# "cancelled", "annulled", "retracted", "sunset", "expired in 2026", "in force until 2026-06-30",
# "valid until", "applies until", "no longer in force", "no longer current"). The active
# forms by which a row says it displaces something older ("supersedes", "cancels and
# supersedes", "replaces", "repeals") are deliberately not matched here: the TSA
# directive and TBS policy rows use them of their predecessors.
_EDITION_ENDED_RE = re.compile(
    r"\b(?:supersed(?:ed|ure)|succeeded by|repeal(?:ed)?|replaced|withdrawn|withdrew|revoked"
    r"|rescinded|laps(?:ed|es)|expir(?:ed|es|y)|ceas(?:ed|es)|deprecated|obsolete|retired"
    r"|cancell?ed|annulled|retracted|sunset(?:s|ted|ting)?"
    r"|no longer (?:in force|in effect|applies|current)"
    r"|(?:in force|in effect|valid|applies) until)\b",
    re.I,
)
# A general row (neither a year-named statute nor an EU instrument citation) is compared
# only when its Current version is the edition token alone (``_GENERAL_EDITION_TOKEN_RE``:
# "2025", "v1.1", "2.2.0", "Rev. 5", "v2026.07", matched as ASCII) or one of the row's
# enumerated shapes below, the register's own text with the edition as the {edition} slot
# and only a year open beyond it ({year}). Any other Current version fails closed ("2025
# (revocation)", "2025 (EOL)", "2025 (archived)", a "sunset" spelt with another script's
# letters), and the failure says to update this allowlist when the register text changed
# legitimately. ``_EDITION_ENDED_RE`` still applies as a second check.
# Sources, governance/register-canonical-citations.md at e3ca4a72 (Current version):
# * OECD AI Principles: "2019 Recommendation as updated 2024".
# * OECD Privacy Guidelines: "2013 (revised)".
# * WCO SAFE Framework: "2025 edition".
# * ASHRAE 135: "2020 (with subsequent addenda)".
# Every other general row's Current version is the token alone or prose that carries no
# single edition (a date, a designator, "continuous", "Version 2.1", "Edition 12"); those
# rows fail closed if the site ever lists an edition for them.
GENERAL_CURRENT_FORMS = {
    "OECD AI Principles": ("{edition} Recommendation as updated {year}",),
    "OECD Privacy Guidelines": ("{edition} (revised)",),
    "WCO SAFE Framework": ("{edition} edition",),
    "ASHRAE 135": ("{edition} (with subsequent addenda)",),
}
_GENERAL_EDITION_TOKEN_RE = re.compile(_EDITION_SHAPE_RE.pattern, re.I | re.ASCII)
_GENERAL_SLOTS = {"edition": f"(?i:{_GENERAL_EDITION_TOKEN_RE.pattern})", "year": _STATUTE_SLOTS["year"]}
_GENERAL_CURRENT_RES = {
    row: tuple(
        re.compile("".join(
            re.escape(part) if i % 2 == 0 else f"(?:{_GENERAL_SLOTS[part]})"
            for i, part in enumerate(re.split(r"\{(\w+)\}", form))
        ), re.ASCII)
        for form in forms
    )
    for row, forms in GENERAL_CURRENT_FORMS.items()
}
# The active forms. A statute note or an instrument citation never displaces anything,
# so in those allowlisted texts these words fail too ("the Privacy Act 2026 replaces it").
_EDITION_DISPLACING_RE = re.compile(r"\b(?:supersedes|succeeds|replaces|repeals|cancels)\b", re.I)
# The clause a marking is said of runs between these boundaries around it.
_CLAUSE_BOUNDARY_RE = re.compile(r"[;,()]|\.\s")
# The register rows the site names after their amending instrument: "EU eIDAS 2", topic
# "Regulation (EU) 2024/1183", is the row "Regulation 910/2014 as amended by Regulation
# 2024/1183 (eIDAS 2)". For these rows a listed edition that is one instrument number
# matches when it is the last instrument the Current version says amended the base act,
# so a later amendment recorded in the register fails the site's citation.
AMENDMENT_NAMED_ROWS = frozenset({"EU eIDAS"})
# An EU instrument citation is read whole against an allowlist (``instrument_edition``):
# a base instrument ("Regulation 2024/1689", "Directive (EU) 2022/2555"); then
# optionally an amendment list, either ",? as amended by" followed by instrument numbers
# joined by "," or "and", each with or without "Regulation", "Directive" or "(EU)"
# ("Regulation 2024/1183 and (EU) 2027/55"), the list ending at the first ";" or "("
# that is not an "(EU)" or "(EC)" marker, or the same list in parentheses ("(as amended
# by Regulation (EU) 2023/2869)", the EU MiCA row); then optionally one short-name
# parenthetical that is one of the row's enumerated short names
# (``instrument_short_names``). Any other text makes the citation unreadable.
_BASE_INSTRUMENT_RE = re.compile(
    r"(?P<kind>Regulation|Directive)\s+(?:\((?:EU|EC)\)\s+)?(?P<num>\d{1,4}/\d{1,4})(?![\w/])"
)
_AMENDMENT_ITEM_RE = re.compile(
    r"(?:(?P<kind>Regulation|Directive)\s+)?(?:\((?:EU|EC)\)\s+)?(?P<num>\d{1,4}/\d{1,4})"
)
_AMENDED_BY_RE = re.compile(r",?\s+as amended by\s+")
_PAREN_AMENDED_BY_RE = re.compile(r"\s+\(as amended by\s+")
_AMENDMENT_LIST_END_RE = re.compile(r";|\((?!(?:EU|EC)\))")
_AMENDMENT_SEPARATOR_RE = re.compile(r"\s*,\s*|\s+and\s+")
_SHORT_NAME_RE = re.compile(r"\s*\((?P<name>[^()]*)\)\s*")
# Any EU instrument number, in any surrounding text. A listed edition that carries one
# is read only as an instrument citation (``edition_matches`` fails closed otherwise).
# Deliberately wider than gate D15's EU_NUMBER: no instrument word, marker or case.
_INSTRUMENT_NUMBER_RE = re.compile(r"\d{1,4}/\d{1,4}")
# The short names a row's citation may end with, enumerated from the register
# (governance/register-canonical-citations.md as of 2026-10-18): EU eIDAS, "Regulation
# 910/2014 as amended by Regulation 2024/1183 (eIDAS 2)"; EU AI Act, "Regulation
# 2024/1689 as amended by Regulation (EU) 2026/1744 (Digital Omnibus)". Every row may
# also carry its own register Standard ID, with or without its leading "EU " ("(EU
# MiCA)", "(MiCA)"). Any other parenthetical ("(No Longer Valid)", "(Until)", "(Not
# Current)") fails; if the register text changed legitimately, update this allowlist.
EU_INSTRUMENT_SHORT_NAMES = {
    "EU eIDAS": frozenset({"eIDAS 2"}),
    "EU AI Act": frozenset({"Digital Omnibus"}),
}
# The words of a descriptive topic, enumerated from the topics of the landing and v2
# coverage bibliography lists as of 2026-10-18 (50 distinct descriptive topics; the
# edition, date and EU instrument citation topics and the statute amendment topic "as
# amended 2024" keep their own rules). A topic is split at each single space after its
# HTML entities are decoded (``_plain``), and every word, parenthesised words and the
# symbols "&" and "/" included, must be one of these, ignoring the case of ASCII letters
# only (so no letter of another script folds onto a listed word). Any other word or
# character fails as unreadable ("Web application risks (archived)", "(EOL)", a
# "repealed" spelt with a Cyrillic letter, a digit, a double space). None of these words
# states that an edition ended; if a new topic is legitimate, add its words here, never
# one that does.
TOPIC_WORDS = frozenset({
    "&", "(ot)", "(ssdf)", "/", "act", "adversarial", "adversary", "ai", "app", "application",
    "architecture", "assessment", "assurance", "authentication", "banking", "business",
    "california", "card", "cloud", "clouds", "compliance", "consumer", "continuity", "controls",
    "cybersecurity", "dados", "data", "de", "development", "digital", "federal", "for",
    "framework", "generative", "geral", "governance", "health", "identity", "impact", "in",
    "incident", "industrial", "information", "it", "law", "lei", "llm", "management", "matrix",
    "maturity", "media", "ml", "modeling", "of", "on", "operational", "ot", "payment",
    "personal", "pii", "privacy", "profile", "protection", "prote\u00e7\u00e3o", "public",
    "quality", "regulation", "response", "revised", "risk", "risks", "sanitization",
    "sarbanes-oxley", "secure", "security", "series", "service", "software", "supply-chain",
    "system", "systems", "tactics", "taxonomy", "techniques", "technology", "threat",
    "threat-modeling", "threats", "to", "trust", "uk", "verification", "web", "zero",
})
# The names a bibliography list may carry that resolve to no register row and hold no
# edition, enumerated from the lists read as of 2026-10-18: "IEC 62443" on the landing
# and v2 coverage lists. A name is matched exactly as written. Any other name that
# resolves to no row and holds no edition fails as unresolved ("IEC 62443 (withdrawn)",
# "IEC 62443 superseded"), whatever words it uses; add a register row or curated alias
# for it, or, if it legitimately names no row, add it here. This list does not apply to
# the For-AI pages: there every part of a compared OWASP name must name a row, so
# "OWASP MCP Top 10 / IEC 62443" fails as unresolved.
UNRESOLVED_LIST_NAMES = frozenset({"IEC 62443"})


class EditionEntry(NamedTuple):
    """One hand-written entry the edition check read, with its outcome."""

    source: str
    line: int
    name: str
    edition: str
    row: str
    current: str
    # "match", "mismatch", "unresolved", "unreadable", "no edition", "unparsed",
    # "mismatched instrument", "unchecked" or "incomplete"
    status: str


def _edition_source_text(rel):
    return (WEB_DIR / rel).read_text(encoding="utf-8")


def _load_edition_resolver():
    """Gate D15's module and its resolver over the citations register."""
    tools = str(REPO_ROOT / "tools")
    if tools not in sys.path:
        sys.path.insert(0, tools)
    try:
        spec = importlib.util.spec_from_file_location("d15_for_web_editions", D15_CHECKER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        resolver = module.build_resolver(CITATIONS_REGISTER.read_text(encoding="utf-8"))
    except (ImportError, OSError, ValueError) as e:
        raise BuildError(f"cannot load the D15 citation resolver: {e}") from e
    return module, resolver


def _plain(fragment):
    """Template HTML as text: the external-link marker (``EXT_LINK_MARKER``, exactly as
    written) and tags dropped, entities decoded. The text of any other "ext" span is kept."""
    fragment = fragment.replace(EXT_LINK_MARKER, "")
    return html_unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def _biblio_columns(text):
    """(start, end) offsets of the content of each "biblio-col" div, ending at that div's
    own closing tag (nested divs counted), or at the end of the text if it never closes."""
    cols = []
    for m in _BIBLIO_COL_RE.finditer(text):
        if cols and m.start() < cols[-1][1]:
            continue  # a column nested in a column is read with its parent
        depth, end = 0, len(text)
        for tag in _DIV_TAG_RE.finditer(text, m.start()):
            depth += -1 if tag[1] else 1
            if depth == 0:
                end = tag.start()
                break
        cols.append((m.end(), end))
    return cols


def _for_ai_row(d15, resolver, name):
    """The identity key of the register row a For-AI item's name resolves to: the name
    as written, or the name without a trailing edition in an edition shape (D15's
    ``VERSION_TAIL``, as ``standard_edition_entries`` splits one off); None when neither
    resolves. The resolver ignores case and spacing, so "Owasp Top 10 for LLM
    Applications 2025", or the name with a no-break or double space, resolves."""
    key = resolver.named_row(name)
    if key:
        return key
    m = d15.VERSION_TAIL.search(name)
    tail = m[0].strip(" :,()") if m and m.start() > 0 else ""
    return resolver.named_row(name[:m.start()].strip()) if _EDITION_SHAPE_RE.fullmatch(tail) else None


def _for_ai_label(d15, name):
    """The jurisdiction label of ``FOR_AI_LABEL_INSTRUMENTS`` that ``name`` is (matched
    by ``identity_key``, as ``FOR_AI_NAME_ROWS`` matches it), or None."""
    key = d15.identity_key(name)
    return next((label for label in FOR_AI_LABEL_INSTRUMENTS if d15.identity_key(label) == key), None)


def _for_ai_text_name(d15, name):
    """The name of ``FOR_AI_ITEM_TEXTS`` (a jurisdiction label or a name of
    ``FOR_AI_NAME_TEXTS``) that ``name`` is (matched by ``identity_key``), or None."""
    key = d15.identity_key(name)
    return next((listed for listed in FOR_AI_ITEM_TEXTS if d15.identity_key(listed) == key), None)


def _for_ai_owasp_key(d15, name):
    """(key, edition) for a compared For-AI name: the identity key of ``name`` without a
    trailing edition in an edition shape (D15's ``VERSION_TAIL``, as ``_for_ai_row``
    splits one off), and whether it carried one."""
    m = d15.VERSION_TAIL.search(name)
    tail = m[0].strip(" :,()") if m and m.start() > 0 else ""
    if _EDITION_SHAPE_RE.fullmatch(tail):
        return d15.identity_key(name[:m.start()].strip()), True
    return d15.identity_key(name), False


def _for_ai_owasp_name(d15, name):
    """The name of ``FOR_AI_OWASP_TEXTS`` that ``name`` is (matched by the key of
    ``_for_ai_owasp_key``: case and spacing ignored, any trailing edition removed,
    whether or not either carried one), or None."""
    key = _for_ai_owasp_key(d15, name)[0]
    return next((listed for listed in FOR_AI_OWASP_TEXTS if _for_ai_owasp_key(d15, listed)[0] == key), None)


def _for_ai_mapped_rows(d15, resolver, name, whole=True):
    """The identity keys of the rows ``FOR_AI_NAME_ROWS`` maps ``name`` to (matched by
    ``identity_key``), or an empty list; a jurisdiction label (``FOR_AI_LABEL_INSTRUMENTS``)
    maps only when ``whole``, the item's whole name. Raises BuildError when a mapped
    Standard ID is no register row."""
    key = d15.identity_key(name)
    for listed, row_ids in FOR_AI_NAME_ROWS.items():
        if d15.identity_key(listed) != key or (not whole and listed in FOR_AI_LABEL_INSTRUMENTS):
            continue
        missing = [r for r in row_ids if not resolver.register.has_id(r)]
        if missing:
            raise BuildError(f"FOR_AI_NAME_ROWS maps {listed!r} to {', '.join(map(repr, missing))}, "
                             f"which is no Standard ID in {CITATIONS_REGISTER.relative_to(REPO_ROOT)} "
                             f"(update the mapping in .web/build.py)")
        return [d15.identity_key(r) for r in row_ids]
    return []


def _for_ai_named_pieces(d15, resolver, part, whole=True):
    """(piece, keys) per piece of one part of a For-AI name (split on " / "), ``keys``
    the identity keys of the rows the piece names, for its description check, or [None]
    for a piece that names none: the row the part resolves to (``_for_ai_row``), else
    the rows ``FOR_AI_NAME_ROWS`` maps it to (a jurisdiction label only when ``whole``,
    the part being the item's whole name), else, for a part joined with " and "
    (``_COMPOUND_AND_SPLIT_RE``), those of each piece, a later piece that begins with a
    digit taking the first piece's designator ("ISO/IEC 27001:2022 and 27002:2022" names
    ISO/IEC 27001 and ISO/IEC 27002) and a piece never mapping as a jurisdiction label,
    else the row a leading part of it names (``_named_prefix``: "CSA Cloud Controls
    Matrix (CCM)", "ISO/IEC 5259 series", "ISO/IEC 42001:2023 (withdrawn)")."""
    key = _for_ai_row(d15, resolver, part)
    if key:
        return [(part, [key])]
    mapped = _for_ai_mapped_rows(d15, resolver, part, whole)
    if mapped:
        return [(part, mapped)]
    pieces = _COMPOUND_AND_SPLIT_RE.split(part)
    if len(pieces) == 1:
        return [(part, [_named_prefix(resolver, part)])]
    shared = _SHARED_PREFIX_RE.match(pieces[0])
    out = []
    for piece in pieces:
        if shared and piece[:1].isdigit():
            piece = shared[0] + piece
        key = _for_ai_row(d15, resolver, piece)
        out.append((piece, [key] if key else _for_ai_mapped_rows(d15, resolver, piece, False)
                    or [_named_prefix(resolver, piece)]))
    return out


def _for_ai_name_rows(d15, resolver, part, whole=True):
    """The identity keys of the rows one part of a For-AI name (split on " / ") names,
    for its description check, None for a piece that names none
    (``_for_ai_named_pieces``)."""
    return [key for _, keys in _for_ai_named_pieces(d15, resolver, part, whole) for key in keys]


def _for_ai_unchecked(d15, resolver, name):
    """The parts and pieces of a For-AI name (split on " / " and " and ", as
    ``_for_ai_named_pieces`` splits them) that name no row and are not enumerated in
    ``FOR_AI_UNCHECKED_NAMES``, in order."""
    parts = _COMPOUND_NAME_SPLIT_RE.split(name)
    return [piece for part in parts for piece, keys in _for_ai_named_pieces(d15, resolver, part, len(parts) == 1)
            if keys == [None] and piece not in FOR_AI_UNCHECKED_NAMES]


def _for_ai_branch(d15, resolver, name):
    """(branch, keys) for a For-AI item that is not the EU AI Act entry. The name is
    split on " / " (``_COMPOUND_NAME_SPLIT_RE``) and ``keys`` holds, part by part, the
    rows that part names (``_for_ai_name_rows``; a jurisdiction label names its rows
    only as the whole name), None for a part or piece that names none. The branch is
    "OWASP", the item compared, when any of those rows (one a
    leading part of a part names included: "Owasp Top 10 for LLM Applications 2026
    (withdrawn)") has a Standard ID beginning ``FOR_AI_COMPARED_ID_PREFIX`` ("ISO/IEC
    42001 / OWASP MCP Top 10" included), or when the name contains
    ``FOR_AI_COMPARED_WORD`` once NFKC-normalised, stripped of format characters and
    case-folded ("The OWASP Top 10 for LLM Applications 2025", "OW<zero-width
    space>ASP MCP Top 10", which then fail as unresolved); "" otherwise."""
    parts = _COMPOUND_NAME_SPLIT_RE.split(name)
    keys = [key for part in parts for key in _for_ai_name_rows(d15, resolver, part, len(parts) == 1)]
    owasp = False
    for key in keys:
        if key:
            row = next(e for e in resolver.register.entries if e["identity_key"] == key)
            owasp = owasp or row["id"].startswith(FOR_AI_COMPARED_ID_PREFIX)
    folded = "".join(ch for ch in unicodedata.normalize("NFKC", name)
                     if unicodedata.category(ch) != "Cf").casefold()
    return ("OWASP" if owasp or FOR_AI_COMPARED_WORD in folded else ""), keys


def _hand_written_entries(rel, kind, text, d15_resolver=None):
    """(line, name, edition, problem) per entry of one hand-written list; edition may be
    empty and problem is "" for an entry read. Items are tracked by their offset in the
    source, so two items on one line are two items. An <li> of a list read that its item
    pattern cannot parse gives problem "unparsed" with the item's text as the name, and
    so does an item followed, after its </li>, by anything but whitespace before the
    next <li> or the list's close (``_LI_GAP_RE``; the name is the item's text with that
    text), and a For-AI item whose text between its name and description spans is none
    of the forms enumerated for its branch (``FOR_AI_INTER_SPAN_FORMS``), with that text
    as the edition, and so does a For-AI item whose description span does not run to its
    close (``_FOR_AI_DESC_RE``), with the item's text as the name; a For-AI item a part
    of whose name names a row (``_for_ai_name_rows``, or the EU AI Act entry) and whose
    description is none of those enumerated for that row (``FOR_AI_DESCRIPTIONS``) gives
    problem "unparsed description", once per such row, with the row's Standard ID as the
    name and the description as the edition, and its entry is still read so its editions
    are compared (the description of an item whose name names no row is not checked);
    a For-AI item on the "" branch named by a name of ``FOR_AI_ITEM_TEXTS``
    (``_for_ai_text_name``: a jurisdiction label or a name of ``FOR_AI_NAME_TEXTS``) whose
    text between the spans is none of that name's forms, or whose text is a form
    enumerated there only for other names, gives problem "mismatched instrument", with
    the item's name and that text as the edition, and so does a For-AI item compared as
    an OWASP entry named by a name of ``FOR_AI_OWASP_TEXTS`` (``_for_ai_owasp_name``)
    whose text between the spans is none of that name's forms (on either branch, only
    text that is a form of the branch reaches this check: any other text gives
    "unparsed", as above); a For-AI item not compared as an OWASP entry gives problem
    "unchecked" for each part or piece of its name that names no row and is not
    enumerated in ``FOR_AI_UNCHECKED_NAMES`` (``_for_ai_unchecked``), with that part as
    the name; an <li> with an "id" span anywhere inside it that is not among the items
    of the lists read gives "incomplete"; a For-AI source without exactly one EU AI Act
    entry gives one "incomplete" entry with line 0, and so does, once per name, a For-AI
    source on which a name of ``FOR_AI_ITEM_TEXTS`` (matched as ``_for_ai_text_name``
    matches it), of ``FOR_AI_UNCHECKED_NAMES`` (matched exactly) or of
    ``FOR_AI_OWASP_TEXTS`` (matched as ``_for_ai_owasp_name`` matches it) is not the
    whole name of exactly one item, and so does, once per name, a For-AI source on which
    a name of ``FOR_AI_OWASP_TEXTS`` that is the whole name of exactly one item is not
    the only item, part or piece naming its register row (``_for_ai_row``; counted over
    ``_for_ai_branch``'s keys), and so does, once per item, a For-AI item named by a
    name of ``FOR_AI_OWASP_TEXTS`` that carries a trailing edition
    (``_for_ai_owasp_key``) where that name has none, or none where it has one; a source
    with no list read gives one "unparsed" entry with line 0 and an empty name.
    ``d15_resolver`` is ``_load_edition_resolver()``'s result, loaded when not given."""
    if kind == "for-ai":
        d15, resolver = d15_resolver or _load_edition_resolver()
        ids = {e["identity_key"]: e["id"] for e in resolver.register.entries}
    entries, seen, eu_entries = [], set(), 0  # entries are (offset or None, name, edition, problem)
    if kind == "biblio":
        lists = _biblio_columns(text)
    else:
        lists = []
        for heading in _FOR_AI_INDEX_RE.finditer(text):
            end = text.find("<h2", heading.end())
            lists.append((heading.end(), len(text) if end < 0 else end))
    for start, end in lists:
        for li in _LI_RE.finditer(text, start, end):
            pos = li.start()
            seen.add(pos)
            gap = _LI_GAP_RE.match(text, li.end(), end)[0]
            if gap.strip():
                # Text after the item's </li> is read with it and fails it.
                entries.append((pos, _plain(li[0] + gap), "", "unparsed"))
                if kind == "for-ai" and _FOR_AI_EU_AI_ACT_LOOSE_RE.search(_plain(li[0])):
                    eu_entries += 1
                continue
            if kind == "biblio":
                item = re.sub(r"</?a\b[^>]*>", "", li[0].replace(EXT_LINK_MARKER, "")).strip()
                m = _BIBLIO_ITEM_RE.fullmatch(item)
                if m:
                    entries.append((pos, _plain(m["name"]), _plain(m["topic"]), ""))
                else:
                    entries.append((pos, _plain(li[0]), "", "unparsed"))
                continue
            m = _FOR_AI_ITEM_RE.match(li[0])
            if not m:
                entries.append((pos, _plain(li[0]), "", "unparsed"))
                continue
            name = _plain(m["name"])
            full = _plain(m["name"] + m["rest"])
            eu = _FOR_AI_EU_AI_ACT_RE.match(full)
            if eu:
                eu_entries += 1
                (branch, keys), between = (FOR_AI_EU_AI_ACT_ID, ()), full[eu.end():].strip()
            elif _FOR_AI_EU_AI_ACT_LOOSE_RE.search(full):
                eu_entries += 1
                entries.append((pos, full, "", "unparsed"))
                continue
            else:
                (branch, keys), between = _for_ai_branch(d15, resolver, name), _plain(m["rest"])
            tail = _FOR_AI_DESC_RE.fullmatch(li[0], m.end())
            if not tail:
                # The description span does not run to the item's close.
                entries.append((pos, _plain(li[0]), "", "unparsed"))
                continue
            # The rows the item names: the EU AI Act, or the rows its name's parts name.
            row_ids = [FOR_AI_EU_AI_ACT_ID] if eu else list(dict.fromkeys(ids[k] for k in keys if k))
            desc = _plain(tail["desc"])
            undescribed = [r for r in row_ids if desc not in FOR_AI_DESCRIPTIONS.get(r, ())]
            if between not in FOR_AI_INTER_SPAN_FORMS[branch]:
                # The text between the spans is none of the forms enumerated for the branch.
                entries.append((pos, full, between, "unparsed"))
                continue
            if branch == "":
                # A name enumerated in FOR_AI_ITEM_TEXTS (a jurisdiction label included)
                # lists one of its own forms, and a form enumerated for a name follows no
                # other name.
                listed = _for_ai_text_name(d15, name)
                owners = [n for n, forms in FOR_AI_ITEM_TEXTS.items() if between in forms]
                if (listed and between not in FOR_AI_ITEM_TEXTS[listed]) or (owners and listed not in owners):
                    entries.append((pos, name, between, "mismatched instrument"))
            if branch == "":
                # A name, part or piece that names no row is enumerated, or it fails.
                entries.extend((pos, piece, "", "unchecked") for piece in _for_ai_unchecked(d15, resolver, name))
            if branch == "OWASP":
                # A name enumerated in FOR_AI_OWASP_TEXTS lists one of its own forms.
                owasp = _for_ai_owasp_name(d15, name)
                if owasp and between not in FOR_AI_OWASP_TEXTS[owasp]:
                    entries.append((pos, name, between, "mismatched instrument"))
            # A description none of those enumerated for a row the item names fails; the
            # item's editions are still compared.
            entries.extend((pos, row_id, desc, "unparsed description") for row_id in undescribed)
            if eu:
                entries.append((pos, FOR_AI_EU_AI_ACT_ID, eu["edition"], ""))
            elif branch == "OWASP":
                entries.append((pos, name, "", ""))
    if not lists or not entries:
        entries.append((None, "", "", "unparsed"))
    else:
        # Completeness: every <li> in the source with an "id" span anywhere inside it is
        # an item of a list read (matched by offset, not by line).
        for li in _LI_RE.finditer(text):
            if li.start() not in seen and _ID_SPAN_RE.search(li[0]):
                entries.append((li.start(), _plain(li[0]), "", "incomplete"))
        if kind == "for-ai" and eu_entries != 1:
            entries.append((None, f"expected exactly one EU AI Act entry in the resource index, "
                            f"found {eu_entries}", "", "incomplete"))
        if kind == "for-ai":
            # Each name of FOR_AI_ITEM_TEXTS (a jurisdiction label or a name of
            # FOR_AI_NAME_TEXTS, matched as ``_for_ai_text_name`` matches it), each name
            # of FOR_AI_UNCHECKED_NAMES (matched exactly) and each name of
            # FOR_AI_OWASP_TEXTS (matched as ``_for_ai_owasp_name`` matches it) is the whole
            # name of exactly one item whose name span is read, whether or not the item
            # passes; a name in both of the first two is counted exactly when that count is
            # not one. An item named by a name of FOR_AI_OWASP_TEXTS carries a trailing
            # edition exactly when that name does. Each name of FOR_AI_OWASP_TEXTS that
            # names one item is also the only item, part or piece naming its register row
            # (``_for_ai_branch``'s keys: "OWASP LLM Top 10 2026", or a compound part).
            named, exact, owasp_named, owasp_edition, rows = Counter(), Counter(), Counter(), [], Counter()
            for start, end in lists:
                for li in _LI_RE.finditer(text, start, end):
                    m = _FOR_AI_ITEM_RE.match(li[0])
                    if m:
                        name = _plain(m["name"])
                        named[_for_ai_text_name(d15, name) or name] += 1
                        exact[name] += 1
                        owasp = _for_ai_owasp_name(d15, name)
                        owasp_named[owasp] += 1
                        if owasp and _for_ai_owasp_key(d15, name)[1] != _for_ai_owasp_key(d15, owasp)[1]:
                            owasp_edition.append((name, owasp))
                        rows.update(key for key in _for_ai_branch(d15, resolver, name)[1] if key)
            found = {name: named[name] for name in FOR_AI_ITEM_TEXTS}
            for name in sorted(FOR_AI_UNCHECKED_NAMES):
                if exact[name] != 1 or name not in found:
                    found[name] = exact[name]
            found.update((name, owasp_named[name]) for name in FOR_AI_OWASP_TEXTS)
            for name, count in found.items():
                if count != 1:
                    lists_for = " and ".join(n for n, listed in (
                        ("FOR_AI_LABEL_INSTRUMENTS", FOR_AI_LABEL_INSTRUMENTS),
                        ("FOR_AI_NAME_TEXTS", FOR_AI_NAME_TEXTS),
                        ("FOR_AI_UNCHECKED_NAMES", FOR_AI_UNCHECKED_NAMES),
                        ("FOR_AI_OWASP_TEXTS", FOR_AI_OWASP_TEXTS)) if name in listed)
                    entries.append((None, f"expected exactly one item named {name!r} in the resource "
                                    f"index, found {count} (each name of FOR_AI_LABEL_INSTRUMENTS and "
                                    f"FOR_AI_NAME_TEXTS, case and spacing ignored, and each name of "
                                    f"FOR_AI_UNCHECKED_NAMES, matched exactly, in .web/build.py names one "
                                    f"item on every For-AI page, and so does each name of "
                                    f"FOR_AI_OWASP_TEXTS, case and spacing ignored and any trailing edition "
                                    f"removed; correct the template, or if the list changed legitimately, "
                                    f"update {lists_for})", "", "incomplete"))
            for name in FOR_AI_OWASP_TEXTS:
                key = _for_ai_row(d15, resolver, name)
                if key and owasp_named[name] == 1 and rows[key] != 1:
                    entries.append((None, f"expected exactly one item, part or piece naming the register row "
                                    f"{ids[key]!r} of {name!r} in the resource index, found {rows[key]} (each "
                                    f"name of FOR_AI_OWASP_TEXTS in .web/build.py names one item on every For-AI "
                                    f"page, and no other item, part of a compound name or piece of one names its "
                                    f"register row, in any spelling; the row may be named once, so the template "
                                    f"should drop the duplicate or compound part)", "", "incomplete"))
            for name, owasp in owasp_edition:
                entries.append((None, f"item {name!r} in the resource index is the name {owasp!r} with its "
                                f"trailing edition {'dropped' if _for_ai_owasp_key(d15, owasp)[1] else 'added'} "
                                f"(an item named by a name of FOR_AI_OWASP_TEXTS in .web/build.py carries a "
                                f"trailing edition exactly when that name does, the edition's value left to "
                                f"the comparison; correct the template, or if the edition was added or "
                                f"dropped legitimately, update FOR_AI_OWASP_TEXTS)", "", "incomplete"))
    return [(0 if pos is None else text.count("\n", 0, pos) + 1, name, edition, problem)
            for pos, name, edition, problem in entries]


def _topic_edition(topic, d15):
    """The topic span read as an edition, when it is one: it carries an EU instrument
    number ("Regulation (EU) 2016/679"), or every comma item is a date or edition
    ("2019, updated 2024"), read ignoring the case of ASCII letters only ("UPDATED 2025-01"
    as "updated 2025-01") and with ASCII digits. Descriptive topics give an empty string."""
    if d15.eu_numbers(topic):
        return topic
    fixed = re.compile(d15.FIXED_ITEM.pattern, re.I | re.ASCII)
    items = [i.strip() for i in topic.split(",")]
    if topic and all(fixed.fullmatch(i) for i in items):
        return topic
    return ""


def _topic_words_listed(topic):
    """Whether every word of ``topic``, split at each single space, is in ``TOPIC_WORDS``,
    ignoring the case of ASCII letters only. An empty topic has no words and passes."""
    if not topic:
        return True
    return all("".join(ch.lower() if ch.isascii() else ch for ch in word) in TOPIC_WORDS
               for word in topic.split(" "))


def _topic_unreadable(topic, row):
    """Whether a topic that ``_topic_edition`` did not read as an edition fails rather
    than counting as descriptive: the topic holds any numeric character (in any script:
    "2019, updated 2024 (repealed)", an EU number written with a division slash or
    "Regulation (EU) 2016-679"), or a word not in ``TOPIC_WORDS`` ("Web application risks
    (archived)", "Top 10 web application risks"), or the row's Current version is an EU
    instrument citation (``instrument_parts``), whose topic must be that citation
    ("General Data Protection Regulation (repealed)" on EU GDPR). The descriptive topics
    of the current entries ("Zero Trust Architecture") do none of these."""
    return (_topic_not_descriptive(topic)
            or instrument_parts(row["current"], row["id"]) is not None)


def _topic_not_descriptive(topic):
    """Whether ``topic`` holds any numeric character (in any script) or a word not in
    ``TOPIC_WORDS``: the topic rules that need no register row."""
    return any(ch.isnumeric() for ch in topic) or not _topic_words_listed(topic)


def _topic_date_re(d15):
    """The dates the same-year rule reads, enumerated: "YYYY", "YYYY-MM", "YYYY-MM-DD",
    "Month YYYY", "D Month YYYY" and "Month D YYYY" ("June 1 2025"; a month as D15's
    ``MONTH`` spells it), each optionally after one of D15's date words ("updated") and
    one space, ASCII digits only and ASCII letters in any case."""
    return re.compile(
        r"(?:(?:adopted|updated|effective|published|revised) )?"
        r"(?:(?P<year>\d{4})(?:-(?P<month>\d{2})(?:-(?P<day>\d{2}))?)?"
        rf"|(?:(?P<mday>\d{{1,2}}) )?(?P<mname>{d15.MONTH}) (?P<myear>\d{{4}})"
        rf"|(?P<dname>{d15.MONTH}) (?P<dday>\d{{1,2}}) (?P<dyear>\d{{4}}))",
        re.I | re.ASCII,
    )


def _topic_dates_in_year(topic, year, d15):
    """Whether ``year`` is a year edition and every comma item of ``topic`` is a date the
    same-year rule reads (``_topic_date_re``: "2025-01", "updated 2025-05-01", "UPDATED
    2025-01", "1 June 2025", "June 1 2025") that is a calendar date ("2025-13-99",
    "2025-02-30", "31 June 2025" and "June 31 2025" are not) in ``year``."""
    if not _YEAR_RE.fullmatch(year):
        return False
    date_re = _topic_date_re(d15)
    months = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
    for item in (i.strip() for i in topic.split(",")):
        m = date_re.fullmatch(item)
        if not m:
            return False
        if m["year"]:
            y, month, day = int(m["year"]), int(m["month"] or 1), int(m["day"] or 1)
        elif m["mname"]:
            y, month = int(m["myear"]), months.index(m["mname"][:3].lower()) + 1
            day = int(m["mday"] or 1)
        else:
            y, month = int(m["dyear"]), months.index(m["dname"][:3].lower()) + 1
            day = int(m["dday"])
        try:
            datetime.date(y, month, day)
        except ValueError:
            return False
        if str(y) != year:
            return False
    return True


def _stripped_topic_unreadable(topic, edition, row, d15):
    """Whether the topic of a name that resolves only once its trailing edition
    ``edition`` is split off ("OWASP Top 10 (2025)", also as a part of a compound name)
    fails: a topic read as an edition (``_topic_edition``) whose numbers differ from that
    edition ("2021 edition") unless the edition is a year and the topic dates in that year
    (``_topic_dates_in_year``: "2025-01"), or any other topic that is unreadable
    (``_topic_unreadable``: "2.0 (withdrawn)", "Top 10 web application risks", "Web
    application risks (repealed)", a word not in ``TOPIC_WORDS``). An empty topic, a
    descriptive one ("Web application risks"), one that repeats the edition ("2025
    edition") and a year-named statute's amendment topic (``statute_topic_recognised``:
    "as amended 2024") pass."""
    if not topic:
        return False
    read = _topic_edition(topic, d15)
    if read:
        return _numbers(read) != _numbers(edition) and not _topic_dates_in_year(read, edition, d15)
    if statute_topic_recognised(row["id"], edition, topic, row["current"]):
        return False
    return _topic_unreadable(topic, row)


def _named_prefix(resolver, name):
    """The register row named by the longest leading part of ``name`` that ends at a
    non-space character before a non-word character and resolves
    (``Resolver.named_row``), or None. A name that does not resolve whole but begins
    with a row's name ("OWASP Top 10 (2025) (repealed)", "General Data Protection
    Regulation (repealed)", "ICAO Annex 17 (Chicago Convention) Edition 11", the row's
    name ending in ")") names that row with text the check cannot read."""
    for m in reversed(list(re.finditer(r"\S(?=\W)", name))):
        key = resolver.named_row(name[:m.end()].strip())
        if key:
            return key
    return None


def _numbers(text):
    return _EDITION_NUMBER_RE.findall(text)


def edition_superseded(listed, superseded):
    """Whether the listed edition is one of the row's Superseded versions: an item with
    the same numbers, as written or without a trailing parenthetical ("2025" is the item
    "2025 (v2.0)"). A draft item ("draft 2024") is a different edition from the
    published one and is not compared."""
    nums = _numbers(listed)
    for item in superseded or ():
        if not nums or re.search(r"\bdraft\b", item, re.I):
            continue
        core = re.sub(r"\s*\([^()]*\)\s*$", "", item)
        if nums in (_numbers(item), _numbers(core)):
            return True
    return False


def edition_ended(listed, current, superseded=()):
    """Whether the Current version marks the listed edition ended (``_EDITION_ENDED_RE``:
    superseded, succeeded by, repealed, replaced, withdrawn, revoked, rescinded, lapsed,
    expired, ceased, deprecated, obsolete, retired, cancelled, annulled, retracted, no
    longer in force or current, in force, valid or applies until).

    Each marking is tied to its subject within its clause, the text between the clause
    boundaries around it (";", ",", "(", ")" or a sentence end). Its subject is the
    nearest number before it in the clause. A marking ends the listed edition unless
    that subject is a number of one of the row's Superseded versions that is not a
    number of the listed edition ("2026 (the 2025 edition was withdrawn)" when 2025 is
    superseded), and even then it ends the listed edition when the rest of its clause
    names a number of the listed edition other than after "by" ("2025 withdrawn along
    with 2026"; but "Directive 1999/93/EC repealed by Regulation 910/2014" is said of
    the directive). So an older number in an earlier clause, or earlier in the same
    clause before a nearer number, does not excuse a later marking. A row that only
    says it supersedes, replaces or repeals something older uses an active form the
    pattern does not match."""
    own = set(_numbers(listed))
    older = {n for item in superseded or () for n in _numbers(item)} - own
    for m in _EDITION_ENDED_RE.finditer(current):
        before = [b.end() for b in _CLAUSE_BOUNDARY_RE.finditer(current, 0, m.start())]
        after = _CLAUSE_BOUNDARY_RE.search(current, m.end())
        head = current[before[-1] if before else 0:m.start()]
        tail = current[m.end():after.start() if after else len(current)]
        subject = (_numbers(head) or [None])[-1]
        if subject not in older:
            return True
        if not re.match(r"\s*by\b", tail, re.I) and own & set(_numbers(tail)):
            return True
    return False


def _clauses(text):
    """The text split at each ";" outside parentheses."""
    out, depth, start = [], 0, 0
    for i, ch in enumerate(text):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(depth - 1, 0)
        elif ch == ";" and not depth:
            out.append(text[start:i])
            start = i + 1
    return out + [text[start:]]


def statute_note_recognised(row, note):
    """Whether ``note``, the text after the listed year in the Current version of the
    statute row ``row``, is empty or one of that row's enumerated notes
    (``STATUTE_NOTE_FORMS``): its first ";"-separated part equals one of the row's
    opening forms and each later part, after one space, one of its clause forms, each
    form used at most once, the forms' slots taking only their variable parts (a date,
    a year, an Act or G.S.R. number, an amending Act name in ``STATUTE_AMENDING_ACTS``).
    Every other text fails ("; the successor Privacy Law 2026 commences and ends the
    1988 Act", "; Act No. 5 of 2026 commences", "; Bill 2026 commences", "; replacing
    ..."), and so does a note that fills a slot with ending, displacing or succession
    wording ("the Successor Amendment Act 2026", "the Repeal Amendment Act 2026")."""
    if not note:
        return True
    forms = _STATUTE_NOTE_RES.get(row)
    if forms is None:
        return False
    if _EDITION_ENDED_RE.search(note) or _EDITION_DISPLACING_RE.search(note) or _SUCCESSION_RE.search(note):
        return False
    opening, *continuation = _clauses(note)
    if not any(f.fullmatch(opening) for f in forms["opening"]):
        return False
    used = set()
    for clause in continuation:
        if not clause.startswith(" "):
            return False
        hit = next((i for i, f in enumerate(forms["clauses"]) if f.fullmatch(clause[1:])), None)
        if hit is None or hit in used:
            return False
        used.add(hit)
    return True


# The one topic a year-named statute listed with its year may carry: "as amended {year}"
# ("Australia Privacy Act 1988", topic "as amended 2024"), the year matched as ASCII.
_STATUTE_TOPIC_RE = re.compile(r"as amended (?P<year>(?:19|20)\d\d)", re.ASCII)


def statute_topic_recognised(row, edition, topic, current):
    """Whether ``topic`` is the amendment topic of the statute row ``row``
    (``STATUTE_YEAR_ROWS``) listed with the year ``edition``: "as amended {year}", where
    the Current version is that year followed by ", as amended by" an amending Act of
    ``STATUTE_AMENDING_ACTS`` whose name ends with the topic's year. So "as amended 2026"
    against the register's 2024 Act, "as amended 2024 (repealed)", and the topic on any
    other row (India DPDPA, whose Current version names no amending Act) fail."""
    m = _STATUTE_TOPIC_RE.fullmatch(topic)
    if not m or row not in STATUTE_YEAR_ROWS or not _YEAR_RE.fullmatch(edition):
        return False
    if not current.startswith(edition):
        return False
    opening = _clauses(current[len(edition):])[0]
    return any(opening.startswith(f", as amended by {act} ") and act.endswith(f" {m['year']}")
               for act in STATUTE_AMENDING_ACTS)


def instrument_short_names(row):
    """The short names a citation of the register row ``row`` may end with in
    parentheses: the row's enumerated names (``EU_INSTRUMENT_SHORT_NAMES``) and its own
    Standard ID, with or without a leading "EU ". No row, no short name."""
    names = set(EU_INSTRUMENT_SHORT_NAMES.get(row, ()))
    if row:
        names.add(row)
        if row.startswith("EU "):
            names.add(row[3:])
    return names


def instrument_edition(text, row=""):
    """The instrument numbers of an EU instrument citation, the base act's first and then
    each amendment's in order ("2024/1689", "2026/1744"; leading zeros dropped), when the
    whole text is one citation of the register row ``row`` in the allowlisted shape (see
    ``_BASE_INSTRUMENT_RE``); None for any other text. Amendment numbers are collected
    only up to the first ";" or "(" after "as amended by" (an "(EU)" marker excepted),
    or inside one "(as amended by ...)" parenthetical, and what follows must be nothing
    or one parenthetical that is one of the row's short names
    (``instrument_short_names``), so "...(eIDAS 2); valid until 2030", "... (No Longer
    Valid)" and "...(Digital Omnibus) (Until)" are not citations."""
    parts = instrument_parts(text, row)
    return None if parts is None else [num for _, num in parts]


def instrument_parts(text, row=""):
    """``instrument_edition`` with each number's instrument kind: (kind, number) pairs,
    kind "Regulation", "Directive" or "" where the citation names none (an amendment
    written "(EU) 2026/1744"); None for any text that is not a citation."""
    def key(m):
        a, b = m["num"].split("/")
        return (m["kind"] or "", f"{int(a)}/{int(b)}")

    def amendments(listed):
        out = []
        for item in _AMENDMENT_SEPARATOR_RE.split(listed.strip()):
            m = _AMENDMENT_ITEM_RE.fullmatch(item)
            if not m:
                return None
            out.append(key(m))
        return out

    text = text.strip()
    base = _BASE_INSTRUMENT_RE.match(text)
    if not base:
        return None
    nums, rest = [key(base)], text[base.end():]
    amended = _AMENDED_BY_RE.match(rest)
    paren = _PAREN_AMENDED_BY_RE.match(rest)
    if amended:
        stop = _AMENDMENT_LIST_END_RE.search(rest, amended.end())
        end = stop.start() if stop else len(rest)
        listed, rest = rest[amended.end():end], rest[end:]
    elif paren:
        depth, end = 1, None
        for i in range(paren.end(), len(rest)):
            depth += {"(": 1, ")": -1}.get(rest[i], 0)
            if depth == 0:
                end = i
                break
        if end is None:
            return None
        listed, rest = rest[paren.end():end], rest[end + 1:]
    else:
        listed = None
    if listed is not None:
        more = amendments(listed)
        if more is None:
            return None
        nums += more
    if rest.strip():
        short = _SHORT_NAME_RE.fullmatch(rest)
        if not short or short["name"] not in instrument_short_names(row):
            return None
    return nums


def edition_matches(listed, current, row="", superseded=()):
    """Whether a listed edition equals the Current version of the register row ``row``,
    whose Superseded versions are ``superseded``.

    A listed edition that is one of the Superseded versions (``edition_superseded``)
    never matches. Otherwise one of three rules applies, by the listed edition and row:

    * An EU instrument citation ("Regulation (EU) 2016/679", "Regulation (EU)
      2024/1689, as amended by (EU) 2026/1744", the topic editions of the EU rows,
      the EU AI Act among them) matches only when the Current version is wholly an
      instrument citation of the row too (``instrument_edition``, an allowlist:
      "Regulation 2024/1689 as amended by Regulation (EU) 2026/1744 (Digital Omnibus)",
      "Regulation 2023/1114 (as amended by Regulation (EU) 2023/2869)") with the same
      instrument numbers in the same order. A row named after its amending
      instrument (``AMENDMENT_NAMED_ROWS``: "EU eIDAS 2") also matches a listed edition
      that is one instrument number ("Regulation (EU) 2024/1183") when that is the last
      amendment number of the Current version, in any form ("Regulation 2027/55", "(EU)
      2027/55", "2027/55"). Any text the citation allowlist does not accept ("...
      (eIDAS 2); valid until 2030", "... (repealed)", a short name not enumerated for
      the row) matches nothing. Neither does a listed edition that carries any EU
      instrument number (``_INSTRUMENT_NUMBER_RE``) but that the allowlist cannot read,
      however it begins ("Regulation (EU) 2016/679 (repealed)", "(EU) 2016/679
      (repealed)", "regulation (EU) 2016/679 (repealed)", "Repealed Regulation (EU)
      2016/679", "Regulation (EU) No 2016/679 (repealed)"): it is not compared by its
      numbers.
    * A statute named by its enactment year (``STATUTE_YEAR_ROWS``: "Australia Privacy
      Act 1988", "India DPDPA 2023") matches a Current version that is that year alone
      or that year followed by one of the row's enumerated notes
      (``statute_note_recognised`` over ``STATUTE_NOTE_FORMS``: the register's own
      amendment, commencement and Rules clauses, with only their dates, years, numbers
      and amending Act name variable). Any other continuation ("1988 Act", "1988, as
      amended", "1988, as amended; the Privacy Act 2026 replaces it", "1988
      (repealed)") does not match.
    * Any other edition, including a bare-year edition of any other row (ISO, COBIT,
      OWASP), matches when the Current version is one the check reads for a general
      row (``general_current_recognised``: the edition token alone or one of the row's
      ``GENERAL_CURRENT_FORMS``), its numbers equal the Current version's, and the
      Current version does not mark it ended (``edition_ended``: "2025 (superseded)",
      "2.2.0 (withdrawn)", "2022 (deprecated)"). So "2025 (revocation)", "2025 (EOL)"
      or "2025 (archived)" matches nothing, whatever word it uses.

    Where both citations name the instrument kind of a number (Regulation or
    Directive), the kinds must be equal too ("Directive (EU) 2016/679" does not match
    "Regulation 2016/679").
    """
    if edition_superseded(listed, superseded):
        return False
    own = instrument_parts(listed, row)
    if own is not None:
        cited = instrument_parts(current, row)
        if cited is None:
            return False
        if len(own) == len(cited) and all(_same_instrument(a, b) for a, b in zip(own, cited)):
            return True
        return (row in AMENDMENT_NAMED_ROWS and len(own) == 1 and len(cited) > 1
                and _same_instrument(own[0], cited[-1]))
    if _INSTRUMENT_NUMBER_RE.search(listed):
        return False
    if row in STATUTE_YEAR_ROWS and _YEAR_RE.fullmatch(listed) and current.startswith(listed):
        return statute_note_recognised(row, current[len(listed):])
    return (general_current_recognised(row, current) and _numbers(listed) == _numbers(current)
            and not edition_ended(listed, current, superseded))


def _same_instrument(a, b):
    """Two (kind, number) pairs name the same instrument: equal numbers, and equal kinds
    where both name one."""
    return a[1] == b[1] and (not a[0] or not b[0] or a[0] == b[0])


def general_current_recognised(row, current):
    """Whether ``current``, the Current version of the general register row ``row``, is
    one the check reads: the edition token alone (``_GENERAL_EDITION_TOKEN_RE``) or one
    of the row's enumerated shapes (``GENERAL_CURRENT_FORMS``). Anything else fails
    closed, whatever words it uses."""
    return bool(_GENERAL_EDITION_TOKEN_RE.fullmatch(current)
                or any(f.fullmatch(current) for f in _GENERAL_CURRENT_RES.get(row, ())))


def standard_edition_entries(texts=None):
    """Every entry of the hand-written standard lists, resolved against the register.

    A compound name ("UK GDPR / DPA 2018") is split on " / " as gate D15 splits a
    cell, and each part is resolved with D15's resolver (``Resolver.named_row``: a
    register Standard ID or a curated alias). A part that resolves as written names
    no edition; otherwise a trailing edition in an edition shape (D15's
    ``VERSION_TAIL``: "v1.1", "2.2.0", ":2024", "(2026)", "Rev. 5", "2019") is split
    off and the rest resolved. On a "biblio" list, a one-part name that resolves
    without an edition takes its edition from the topic span when the topic is one
    ("EU AI Act", "Regulation (EU) 2024/1689, as amended by (EU) 2026/1744"). For a
    name that does not resolve and holds no edition, the biblio topic takes the same
    rules: an EU instrument number there ("Directive (EU) 2022/2555"), or a topic read as
    an edition or date (``_topic_edition``: "2009 edition"), is an edition that names no
    row, so the entry fails rather than passing with a number nobody compared, and a
    topic holding a numeric character or a word not in ``TOPIC_WORDS``
    (``_topic_not_descriptive``: "Industrial / OT security series (withdrawn)") is
    unreadable. A part of a compound
    name takes no edition from the topic, so a topic that is one or holds one fails.
    A name, or a part of a compound name, that resolves only once its trailing edition
    is split off keeps that edition, and its topic is checked against it
    (``_stripped_topic_unreadable``). Outcomes:

    * ``match``: the name resolves, its edition is not among the row's Superseded
      versions, and it equals the row's Current version under the rule for its kind
      (``edition_matches``: an instrument citation or a statute note read against an
      allowlist, any other edition by its numbers and not marked ended).
    * ``mismatch``: the name resolves and its edition differs, is superseded, is
      marked ended, or meets a Current version the allowlist rejects (a failure).
    * ``unresolved``: the name resolves to no row and carries an edition, in the name
      (a trailing edition, or a token in an edition shape at word boundaries anywhere:
      "OWASP Top Ten (2025) (repealed)", "FooStandard 2.0 (withdrawn)"; "IEC 62443"
      holds none) or in the topic, as an EU instrument number or a topic read as an
      edition or date ("IEC 62443", topic "2009 edition"), or it carries no edition and
      is not one of the names enumerated in ``UNRESOLVED_LIST_NAMES``, which a For-AI
      name cannot use ("IEC 62443 (withdrawn)", "IEC 62443 superseded", and "IEC
      62443" as a part of the For-AI name "OWASP MCP Top 10 / IEC 62443"; the edition
      field is empty) (a failure).
    * ``unreadable``: the name does not resolve whole but a leading part of it does
      (``_named_prefix``: "OWASP Top 10 (2025) (repealed)"), or a one-part biblio name
      resolves and its topic is no edition the check reads yet holds a numeric
      character or a word not in ``TOPIC_WORDS`` or belongs to an EU instrument row
      (``_topic_unreadable``: "OWASP Top 10", topic "Web application risks
      (repealed)"), or a part of a compound name resolves and the topic is an edition
      the check reads (ambiguous between the parts) or is unreadable in that sense, or a
      name or part resolves once its trailing edition is split off, that edition matches
      (else the entry is a ``mismatch``), and its topic is an edition with other numbers
      ("OWASP Top 10 (2025)", topic "2021 edition"; a date in the name's year passes) or
      unreadable in that sense ("Web application risks (archived)"), or a name
      that does not resolve holds a numeric character outside ASCII ("OWASP Top Ten
      (2025) (repealed)" with fullwidth digits; the row is then the one a leading part
      names, or none), or a biblio name that does not resolve and holds no edition has
      a topic that is no edition the check reads yet is not descriptive ("IEC 62443",
      topic "Industrial / OT security series, 2018 edition (superseded)"; no row); the
      edition field holds the unreadable text (a failure).
    * ``unparsed``: an <li> of a list read that its item pattern cannot parse, an <li>
      followed after its </li> by anything but whitespace before the next <li> or the
      list's close ("</li> (withdrawn)"; the name holds the item's text with that text),
      a For-AI item whose text between its name and description spans is none of the
      forms enumerated for it (``FOR_AI_INTER_SPAN_FORMS``; the edition field holds that
      text), a For-AI item whose description span does not run to its close, whitespace
      aside ("</span> (withdrawn)</li>"), a For-AI item a part of whose name names a row
      (``_for_ai_name_rows``: split on " / " and " and ", resolved, mapped by
      ``FOR_AI_NAME_ROWS`` or named by a leading part; or the EU AI Act entry) whose
      description is none of those enumerated for that row (``FOR_AI_DESCRIPTIONS``; one
      entry per such row, the name and row fields hold the row's Standard ID and the
      edition field the description; an item whose name names no row keeps its
      description unchecked), or a source with no list read (a failure).
    * ``mismatched instrument``: a For-AI item named by a jurisdiction label or a name
      of ``FOR_AI_NAME_TEXTS`` whose text between its name and description spans is none
      of the forms enumerated for that name in ``FOR_AI_LABEL_INSTRUMENTS`` or
      ``FOR_AI_NAME_TEXTS`` ("United States, Texas" with Colorado's instrument text,
      "NIST Cybersecurity Framework 2.0" with none), or whose text is a form enumerated
      only for other names ("Canada" with Colorado's, "ISO 31000:2018" with ", AI
      management system.", a renamed item with its old text), or a compared OWASP name
      of ``FOR_AI_OWASP_TEXTS`` whose text is none of its forms there ("OWASP MCP Top
      10" with none); the edition field holds that text (a failure). Only text that is
      a form of the item's branch in ``FOR_AI_INTER_SPAN_FORMS`` reaches this check; any
      other text is ``unparsed``.
    * ``unchecked``: a part or piece of the name of a For-AI item not compared as an
      OWASP entry that names no row (``_for_ai_named_pieces``) and is not enumerated in
      ``FOR_AI_UNCHECKED_NAMES`` ("United States, Texas (TRAIGA)"), so its description
      would go unchecked; the name field holds that part (a failure).
    * ``incomplete``: an <li> with an "id" span that is not among the entries read,
      a For-AI source without exactly one EU AI Act entry, or a For-AI source on which a
      name of ``FOR_AI_LABEL_INSTRUMENTS`` or ``FOR_AI_NAME_TEXTS`` (case and spacing
      ignored), of ``FOR_AI_UNCHECKED_NAMES`` (matched exactly) or of
      ``FOR_AI_OWASP_TEXTS`` (case and spacing ignored, any trailing edition removed) is
      not the whole name of exactly one item (removed, renamed, doubled or replaced by a
      copy of another item; one entry per name), or on which a name of
      ``FOR_AI_OWASP_TEXTS`` that names one item shares its register row with another
      item, part of a compound name or piece of one (``_for_ai_branch``: "OWASP LLM Top
      10 2026", "OWASP MCP Top 10 / OWASP GenAI Red Teaming Guide"; one entry per name),
      or on which an item named by a name of ``FOR_AI_OWASP_TEXTS`` carries a trailing
      edition where that name has none, or none where it has one ("OWASP GenAI Red
      Teaming Guide 1.0", "OWASP Top 10 for LLM Applications"; one entry per item) (a
      failure).
    * ``no edition``: the entry names no edition, so there is nothing to compare.
      These are out of scope. On 2026-10-18 they were: LINDDUN, STRIDE, IEC 62443,
      NIST AI 600-1 and NIST SP 800-207 on both lists; MITRE ATLAS, MITRE ATT&CK and
      NIST SP 800-218 on the landing list (the coverage list gives their editions);
      UK GDPR, DPA 2018, US CCPA, CPRA, Brazil LGPD, Canada PIPEDA, Singapore PDPA,
      China PIPL, Switzerland nFADP, US HIPAA, US SOX and Basel III on both lists;
      OWASP MCP Top 10 and OWASP GenAI Red Teaming Guide on the For-AI pages. EU NIS2
      and EU eIDAS 2 resolve through curated aliases and are compared.

    On the For-AI pages only the OWASP entries and the EU AI Act entry are compared.
    A For-AI name is split on " / " like any compound name, and an OWASP entry is
    chosen by resolution (``_for_ai_branch``: the row any part, that part without its
    trailing edition, or a leading part of it names has a Standard ID beginning "OWASP
    ", so "Owasp Top 10 for LLM Applications 2025", the name with a no-break or double
    space, or "ISO/IEC 42001 / OWASP MCP Top 10" is compared), with one fallback by
    spelling: a name that, NFKC-normalised, stripped of format characters (a zero-width
    space) and case-folded, contains "owasp" anywhere ("The OWASP Top 10 for LLM
    Applications 2025", "OWASP's Top 10", "OWASP-Top 10", a fullwidth "OWASP",
    "Withdrawn OWASP Top 10") is compared too, so one that does not resolve fails as
    unresolved (or as unreadable when a leading part names a row). Every part of a
    compared compound name has its edition compared, and the description is checked
    against the row of every part that names one. The other
    For-AI editions (ISO/IEC 42001:2023, ISO/IEC 23894:2023, ISO/IEC 42005:2025, ISO
    31000:2018, ISO/IEC 27001:2022 and the rest) are out of scope of this check,
    although every <li> of the resource index must still parse and the description of
    every item whose name names a row must be enumerated (``FOR_AI_DESCRIPTIONS``; a
    name worded unlike its row is mapped in ``FOR_AI_NAME_ROWS``), the text between the
    spans of a name enumerated in ``FOR_AI_LABEL_INSTRUMENTS`` (a jurisdiction label) or
    ``FOR_AI_NAME_TEXTS`` must be its own form and follow no other name, a name that
    names no row must be enumerated in ``FOR_AI_UNCHECKED_NAMES``, and each name of
    ``FOR_AI_LABEL_INSTRUMENTS``, ``FOR_AI_NAME_TEXTS`` (both with case and spacing
    ignored) and ``FOR_AI_UNCHECKED_NAMES`` (matched exactly) must name exactly one item
    per page. So must each compared OWASP name of ``FOR_AI_OWASP_TEXTS`` (case and
    spacing ignored, any trailing edition removed), which must also be the only item,
    part or piece naming its register row in any spelling, whose item must carry a
    trailing edition exactly when the name does (its value left to the comparison) and
    whose text between the spans, once a form of the "OWASP" branch, must be one of its
    forms there.

    ``texts`` maps a source path to replacement text (for tests); other sources are
    read from the template tree.
    """
    d15, resolver = _load_edition_resolver()
    texts = texts or {}
    rows = {e["identity_key"]: e for e in resolver.register.entries}
    out = []
    for rel, kind in EDITION_LIST_SOURCES:
        text = texts[rel] if rel in texts else _edition_source_text(rel)
        for lineno, listed, extra, problem in _hand_written_entries(rel, kind, text, (d15, resolver)):
            if problem == "unparsed description":
                # The name field holds the Standard ID of the row the item names.
                out.append(EditionEntry(f".web/{rel}", lineno, listed, extra, listed, "", "unparsed"))
                continue
            if problem:
                out.append(EditionEntry(f".web/{rel}", lineno, listed, extra, "", "", problem))
                continue
            parts = _COMPOUND_NAME_SPLIT_RE.split(listed)
            for name in parts:
                key, edition, unreadable, stray_topic = resolver.named_row(name), "", "", ""
                if key and kind == "for-ai":
                    edition = extra
                elif key and len(parts) == 1:
                    edition = _topic_edition(extra, d15)
                    if not edition and _topic_unreadable(extra, rows[key]):
                        unreadable = extra
                elif key:
                    # A compound name's topic names no edition: one the check reads is
                    # ambiguous between the parts, and an unreadable one fails as well.
                    if _topic_edition(extra, d15) or _topic_unreadable(extra, rows[key]):
                        unreadable = extra
                elif not key:
                    m = d15.VERSION_TAIL.search(name)
                    tail = m[0].strip(" :,()") if m and m.start() > 0 else ""
                    if any(ch.isnumeric() and not ch.isascii() for ch in name):
                        # Digits in another script are read in no edition shape.
                        key, unreadable = _named_prefix(resolver, name), name
                    elif _EDITION_SHAPE_RE.fullmatch(tail):
                        key, edition = resolver.named_row(name[:m.start()].strip()), tail
                        if key and _stripped_topic_unreadable(extra, edition, rows[key], d15):
                            stray_topic = extra
                    elif _named_prefix(resolver, name):
                        key, unreadable = _named_prefix(resolver, name), name
                    elif kind == "biblio" and d15.eu_numbers(extra):
                        edition = extra
                    elif _EDITION_TOKEN_IN_NAME_RE.search(name):
                        edition = _EDITION_TOKEN_IN_NAME_RE.search(name)[0]
                    elif kind == "biblio" and _topic_edition(extra, d15):
                        # A topic read as an edition or date is an edition that names no row.
                        edition = extra
                    elif kind == "biblio" and _topic_not_descriptive(extra):
                        unreadable = extra
                row = rows.get(key)
                if unreadable:
                    status, edition = "unreadable", unreadable
                elif not edition and row is None and (kind != "biblio" or name not in UNRESOLVED_LIST_NAMES):
                    # A name that names no row and holds no edition is enumerated, on a
                    # bibliography list only: every part of a compared For-AI name names a row.
                    status = "unresolved"
                elif not edition:
                    status = "no edition"
                elif row is None:
                    status = "unresolved"
                elif not edition_matches(edition, row["current"], row["id"], row["superseded"]):
                    status = "mismatch"
                elif stray_topic:
                    # The name's edition matches; its topic still fails.
                    status, edition = "unreadable", stray_topic
                else:
                    status = "match"
                out.append(EditionEntry(
                    f".web/{rel}", lineno, name, edition,
                    row["id"] if row else "", row["current"] if row else "", status,
                ))
    return out


def _allowlist_rejection(edition, current, row):
    """The note added to a mismatch that an allowlist caused: the text after a statute's
    year is none of its ``STATUTE_NOTE_FORMS``, or the Current version is no instrument
    citation the check reads (an unlisted short name among the causes), or the listed
    edition carries an EU instrument number but is no instrument citation the check
    reads. "" otherwise."""
    if (row in STATUTE_YEAR_ROWS and _YEAR_RE.fullmatch(edition) and current.startswith(edition)
            and not statute_note_recognised(row, current[len(edition):])):
        return (" (the text after the year is none of the row's enumerated notes in "
                "STATUTE_NOTE_FORMS, or names an amending Act not in STATUTE_AMENDING_ACTS; if "
                "the register text changed legitimately, update that allowlist in .web/build.py)")
    if _INSTRUMENT_NUMBER_RE.search(edition) and instrument_edition(edition, row) is None:
        return (" (the listed edition carries an EU instrument number but is not an EU instrument "
                "citation the check reads; write it as \"Regulation (EU) N/N\" or \"Directive (EU) "
                "N/N\", optionally \"as amended by\" further numbers, with at most one short-name "
                "parenthetical that is listed for the row in EU_INSTRUMENT_SHORT_NAMES; if a new "
                "short name is legitimate, add it to that allowlist in .web/build.py)")
    if instrument_edition(edition, row) is not None and instrument_edition(current, row) is None:
        return (" (the Current version is not an EU instrument citation the check reads; a "
                "short-name parenthetical must be listed for the row in EU_INSTRUMENT_SHORT_NAMES; "
                "if the register text changed legitimately, update that allowlist in .web/build.py)")
    if (not _INSTRUMENT_NUMBER_RE.search(edition) and instrument_edition(edition, row) is None
            and not (row in STATUTE_YEAR_ROWS and _YEAR_RE.fullmatch(edition))
            and not general_current_recognised(row, current)):
        return (" (the Current version is neither the edition token alone nor one of the row's "
                "shapes in GENERAL_CURRENT_FORMS; if the register text changed legitimately, "
                "update that allowlist in .web/build.py)")
    return ""


def stale_standard_editions(texts=None):
    """Failure lines for hand-written editions that differ from the register (empty = clean)."""
    for_ai_sources = {f".web/{rel}" for rel, kind in EDITION_LIST_SOURCES if kind == "for-ai"}
    hits = []
    for e in standard_edition_entries(texts):
        if e.status == "mismatch":
            hits.append(
                f"{e.source}:{e.line}: {e.name!r} lists edition {e.edition!r} but the register "
                f"row {e.row!r} has Current version {e.current!r}"
                + _allowlist_rejection(e.edition, e.current, e.row)
            )
        elif e.status == "unreadable" and not e.row and not any(
                ch.isnumeric() and not ch.isascii() for ch in e.name):
            hits.append(
                f"{e.source}:{e.line}: {e.name!r} names no register row and its topic "
                f"{e.edition!r} is neither an edition the check reads nor descriptive (every "
                f"word of a descriptive topic, parenthesised words included, must be listed in "
                f"TOPIC_WORDS in .web/build.py, and it holds no numeric character; correct the "
                f"template, add the words of a legitimate topic to TOPIC_WORDS (never one "
                f"stating that an edition ended), or add the row or a curated alias)"
            )
        elif e.status == "unreadable" and not e.row:
            hits.append(
                f"{e.source}:{e.line}: {e.name!r} names no register row and holds a numeric "
                f"character outside ASCII, which the check cannot read (write any number in "
                f"the name with ASCII digits, and add the row or a curated alias)"
            )
        elif e.status == "unreadable":
            hits.append(
                f"{e.source}:{e.line}: {e.name!r} names the register row {e.row!r} but its listed "
                f"text {e.edition!r} is not that name with an edition the check reads (accepted: "
                f"the name alone, the name with a trailing edition in an edition shape, or on a "
                f"bibliography list an EU instrument citation, date or edition as the topic of a "
                f"name that is not compound; the topic of a name with a trailing edition is "
                f"empty, descriptive, that same edition (for a year edition, dates in that "
                f"year), or for a year-named statute \"as amended\" and the year of the "
                f"register's amending Act; a compound "
                f"name with an EU instrument part needs an empty topic; every word of a "
                f"descriptive topic, parenthesised words included, must be listed in "
                f"TOPIC_WORDS in .web/build.py, so a descriptive number in a topic must be "
                f"spelled out and listed; correct the template, add the words of a legitimate "
                f"topic to TOPIC_WORDS (never one stating that an edition ended), or add a "
                f"curated alias if it names another row)"
            )
        elif e.status == "unresolved" and not e.edition and e.source in for_ai_sources:
            hits.append(
                f"{e.source}:{e.line}: {e.name!r} names no register row and is not among the "
                f"names enumerated for a compared For-AI name, of which there are none "
                f"(UNRESOLVED_LIST_NAMES in .web/build.py applies to bibliography lists only, so "
                f"every part of a compared OWASP name must name a row; correct the template, or "
                f"add a register row or a curated alias for it)"
            )
        elif e.status == "unresolved" and not e.edition:
            hits.append(
                f"{e.source}:{e.line}: {e.name!r} names no register row and is not among the "
                f"names enumerated in UNRESOLVED_LIST_NAMES in .web/build.py (add a register row "
                f"or a curated alias for it, or, if it legitimately names no row, add the name "
                f"to UNRESOLVED_LIST_NAMES)"
            )
        elif e.status == "unresolved":
            hits.append(
                f"{e.source}:{e.line}: {e.name!r} carries edition {e.edition!r} but names no "
                f"register row (add the row or a curated alias)"
            )
        elif e.status == "mismatched instrument":
            hits.append(
                f"{e.source}:{e.line}: list item {e.name!r} lists the instrument text {e.edition!r}, "
                f"which is not the one enumerated for its name in FOR_AI_LABEL_INSTRUMENTS or "
                f"FOR_AI_NAME_TEXTS, or for a compared OWASP name in FOR_AI_OWASP_TEXTS (a "
                f"jurisdiction label must list one of its own forms, which name its mapped rows, "
                f"any other name enumerated there must list one of its own, and a form enumerated "
                f"for a name follows no other name, except that a form of FOR_AI_OWASP_TEXTS may "
                f"follow any compared OWASP name; correct the template, or if its text changed "
                f"legitimately, update those allowlists in .web/build.py)"
            )
        elif e.status == "unchecked":
            hits.append(
                f"{e.source}:{e.line}: {e.name!r} names no register row, so its item's "
                f"description is not checked, and is not among the names enumerated in "
                f"FOR_AI_UNCHECKED_NAMES in .web/build.py (correct the template, add a register "
                f"row or curated alias for it or map it in FOR_AI_NAME_ROWS, or, if it "
                f"legitimately names no row, add the name to FOR_AI_UNCHECKED_NAMES)"
            )
        elif e.status == "unparsed" and e.line and e.row:
            hits.append(
                f"{e.source}:{e.line}: list item for the register row {e.row!r} cannot be parsed: "
                f"its description {e.edition!r} is none of the descriptions enumerated for that "
                f"row in FOR_AI_DESCRIPTIONS (correct the template, or if its text changed "
                f"legitimately, update that allowlist in .web/build.py)"
            )
        elif e.status == "unparsed" and e.line and e.edition:
            hits.append(
                f"{e.source}:{e.line}: list item {e.name!r} cannot be parsed: the text between its "
                f"name and description spans, {e.edition!r}, is none of the forms enumerated for "
                f"it in FOR_AI_INTER_SPAN_FORMS (correct the template, or if its text changed "
                f"legitimately, update that allowlist in .web/build.py)"
            )
        elif e.status == "unparsed" and e.line:
            hits.append(
                f"{e.source}:{e.line}: list item {e.name!r} cannot be parsed (the markup the "
                f"edition check reads changed; update the check or the template)"
            )
        elif e.status == "unparsed":
            hits.append(f"{e.source}: no hand-written standard list found to check")
        elif e.status == "incomplete" and e.line:
            hits.append(
                f"{e.source}:{e.line}: list item {e.name!r} is not among the entries the edition "
                f"check read (it lies outside every list read; update the check or the template)"
            )
        elif e.status == "incomplete":
            hits.append(f"{e.source}: {e.name}")
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
        # Hand-written standard editions (3b380) must match the citations register.
        try:
            edition_hits = stale_standard_editions()
        except BuildError as e:
            print(f"web-generator --check FAIL: {e}", file=sys.stderr)
            return 1
        if edition_hits:
            print(
                "web-generator --check FAIL: hand-written standard edition(s) differ from "
                "governance/register-canonical-citations.md (correct the template, or the "
                "register if upstream moved): " + "; ".join(edition_hits) + ".",
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
