#!/usr/bin/env python3
"""Static-site generator for the grclibrary.ai public site: the promoted baseline-template tree (the PR 2b rebuild, flipped to the site root at the draft-site promotion): the fixed pages, per-domain, per-type and per-document pages, the Browse adventure's need pages, the decide hub and concern pages, the executive reading room, and the crosswalk views and instrument pages.

WHAT THIS IS. A stdlib-only generator that renders the public site from the
LIVE corpus at build time.
There is one source of truth (the corpus); the site is a projection of it. Every
corpus figure on the pages is recomputed here
from ``taxonomy.yml`` (the canonical machine-readable taxonomy, kept in sync with
the corpus by the taxonomy-drift gate) and, on the domain pages and the
executive routes, the published leadership-page listing from
``narrative.yml`` (the generated executive-narrative registry).
Nothing is hardcoded; the preview HTML that seeded the templates carried a
point-in-time snapshot that this generator overwrites.

CONTENT BOUNDARY (why this is safe to publish). The generator reads EXACTLY an
explicit allow-list: ``taxonomy.yml``, ``narrative.yml`` (the committed generated
narrative registry, joined at render time into each domain
page's leadership-page list), ``README.md``, each corpus domain's own
``<domain>/README.md`` (for the per-domain page intro), and the page templates and
shared partials under the variant's template tree. It never walks the repository and
never reads ``.working/``, ``.claude/``, ``tools/``, ``tests/``, ``.github/``, or
the private sibling repositories. (Under ``--check`` it additionally reads the
committed ``.web/corpus-link-manifest.md``, self-scans this generator source for
the safeguard checks, and, for the hand-written edition check, reads
``governance/register-canonical-citations.md`` through gate D15's resolver
(``tools/check-alignment-register-on-pr.py`` and its alias and exclusion files);
none of these feeds published content.) By default its rendered output is the site under
``.web/dist/`` (``--out DIR`` redirects it): the fixed pages of ``DRAFT_PAGES``
(the landing, Browse, Search, All Documents, the crosswalk, the need pages, the
Contributors and For-AI pages, the disclosure and licence pages), one
``<domain>/index.html`` per corpus domain, one
``types/<slug>/index.html`` per document type, one document page per non-root
corpus document under ``documents/``, the executive layer (the decide hub,
concern and subtype pages, and the reading room at
``decisions/<subtype>/<slug>/``: ALL 34 published narrative pages across the
six narrative types, each from the
page's Markdown source by the constrained stdlib renderer below), the error page ``404.html``
(noindex, excluded from the sitemap; Cloudflare Pages serves
it with status 404 for any missing path), and the generated files
``robots.txt``, ``sitemap.xml``, ``llms.txt``, ``_headers`` (the Pages security
headers, ``HEADERS_FILE``), ``_redirects`` (the Pages redirect rules,
``REDIRECTS_FILE``: the pre-promotion /draft/ splat and the retired /about/
and /pack/ addresses), and ``.well-known/security.txt`` (RFC 9116,
``SECURITY_TXT``); it also writes the committed ``.web/corpus-link-manifest.md`` (a generated artefact outside the ephemeral ``dist/`` tree). So the
published surface is those pages and files; a repo file cannot
leak onto the public site through this generator: the reading room reads ONLY
registry-listed sources admitted by the renderer-confinement validator
(``narrative_source_file``: a normalized repo-relative regular file under
``executive/`` only, git-tracked; absolute paths, parent-directory traversal,
symlinks, duplicates, and untracked sources are all rejected loudly; the
tracked-path authority is one ``git ls-files`` call returning paths, never content). The Contributors page and the For-AI
page are static template prose (the acknowledged contributors;
and, for For-AI, descriptive guidance plus a resource index whose links point at
public corpus artefacts on GitHub), not corpus-derived. ``robots.txt`` welcomes
AI/search crawlers, ``sitemap.xml`` lists the indexable root variant's rendered pages, and ``llms.txt`` is
a curated Markdown map of public corpus artefacts. Each domain page draws its
intro (the domain README's ``## Purpose`` paragraph, public corpus content), its
document list (title / type / path from ``taxonomy.yml``, each linking to its
on-site document page, root specifications to their GitHub blobs), and the
published leadership (executive-narrative) pages that touch the area, joined at
render time from ``narrative.yml``. The allow-list additions are the twelve
domain READMEs, ``narrative.yml``, and, for the reading room, the
registry-listed ``executive/`` narrative sources (each admitted only through the
renderer-confinement validator above). Beyond that allow-list the tree
reads its own template tree ``.web/templates-draft/``; the pinned baseline
runtime files under ``.web/baseline/`` and their pin ``.baseline/pin.toml``
(PR 2b), each copied file verified by SHA-256 at build time, and runs the
pinned palette gate ``.baseline/check_palette.py`` (verified by SHA-256 against
the same pin, never served) on the served ``palettes.css``; for the crosswalk
(PR 5) and the comply page built on its model, the compliance alignment
matrix, the reverse framework-control crosswalk, and the canonical citations
register (``compliance/matrix-grc-compliance-alignment.md``,
``governance/matrix-reverse-framework-control-crosswalk.md``,
``governance/register-canonical-citations.md``), each parsed structurally and
loud on schema change; and (site a9, maintainer decision 2026-11-03) the
top-level ``docs/*.md`` adopter documents, each read for its own canonical
metadata block, purpose paragraph, and section outline. Its draft-only file
checks read no file content: the adopter Related Documents check's one
``git ls-files`` call returns tracked paths and its targets are checked for
presence and resolution only, and the Browse adventure's artefact links check
only that each named file exists. docs/ is adopter documentation outside
``taxonomy.yml`` (specification-master-project.md section 4 keeps it outside
the canonical governance-artefact regime), so the draft's adopter document pages
and listings are generated from those records at build time and a docs/ file
added or removed on GitHub appears on or leaves the draft at the next build.
The /draft tree also renders the reading room at ``decisions/<subtype>/<slug>/``
(the same registry-listed sources through the same confinement validator), one
generated ``decide/<subtype-plural>/`` index per narrative type, the
leadership-page list on each draft domain page, the decide hub at ``decide/``,
and one concern topic page per ``DRAFT_CONCERNS`` entry at
``decide/<concern>/``, each assembled at build time from ``narrative.yml`` and
``taxonomy.yml``, plus the Browse adventure's need pages at ``govern/``,
``comply/``, ``solutions/`` and ``policies/`` (design D sections 4.2 to 4.5),
whose counts, lists and link targets come from the same registries and the
crosswalk model.

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
                                   coupling-breakage detector, NOT a corpus gate. It ALSO fails on a stale committed ``corpus-link-manifest.md``, a hardcoded CalVer literal in a template, a root-relative href that skips the ``{{BASE}}`` token, or a hand-written standard edition that differs from the citations register (``stale_standard_editions``: the OWASP and EU AI Act entries of the For-AI page; each listed name is resolved by gate D15's resolver, a register Standard ID or curated alias, and its edition must equal the row's Current version, must not be among the row's Superseded versions, and must not be marked ended by the Current version (after the year of a statute named by its year only the row's enumerated notes, the register's own text with its dates, numbers and amending Act name variable, may follow (``STATUTE_NOTE_FORMS``), and an EU instrument citation may end only with a short name enumerated for its row or the row's own Standard ID (``EU_INSTRUMENT_SHORT_NAMES``), so any other text after the edition fails and the failure says to update the allowlist if the register text changed legitimately); a name that resolves to no row but carries an edition, or whose topic carries an EU instrument number, reads as an edition or date, or is not descriptive (a numeric character or a word not in ``TOPIC_WORDS``), or that carries no edition and is not enumerated in ``UNRESOLVED_LIST_NAMES`` (which a For-AI name cannot use), also fails, as does a list item the check cannot parse (any text but whitespace after an item's ``</li>`` and before the next item or the list's close included, a For-AI item's text between its name and description spans, which must be one of the forms in ``FOR_AI_INTER_SPAN_FORMS``, a For-AI item whose description span does not run to its ``</li>``, whitespace aside, and the description of a For-AI item, which must be one enumerated in ``FOR_AI_DESCRIPTIONS`` for the row of every part of its name, split on " / " and " and ", that names one (resolved, mapped in ``FOR_AI_NAME_ROWS``, or named by a leading part); the OWASP entries are chosen by the row any part of the name resolves to, not by its literal prefix, with one fallback by spelling: a For-AI name that, NFKC-normalised with format characters removed and case-folded, contains "owasp" anywhere is compared too, so one that does not resolve fails, and every part of a compared compound name has its edition compared), a For-AI jurisdiction label whose instrument text is none of its forms in ``FOR_AI_LABEL_INSTRUMENTS``, or any other For-AI name enumerated in ``FOR_AI_NAME_TEXTS`` whose text is none of its forms there, or a form of either list after a name it is not enumerated for, a compared OWASP name enumerated in ``FOR_AI_OWASP_TEXTS`` whose text is a form of the OWASP branch in ``FOR_AI_INTER_SPAN_FORMS`` but none of its own forms there (text that is no form of the branch fails as unparsed, above), a For-AI name, part or piece not compared as an OWASP entry that names no row and is not enumerated in ``FOR_AI_UNCHECKED_NAMES``, an "id" list item outside every list read, a For-AI source without exactly one EU AI Act entry or on which a name of ``FOR_AI_LABEL_INSTRUMENTS`` or ``FOR_AI_NAME_TEXTS`` (case and spacing ignored), of ``FOR_AI_UNCHECKED_NAMES`` (matched exactly) or of ``FOR_AI_OWASP_TEXTS`` (case and spacing ignored, any trailing edition removed) is not the whole name of exactly one item or on which an item named by a name of ``FOR_AI_OWASP_TEXTS`` adds or drops a trailing edition (adding or dropping one needs a list update) or on which a name of ``FOR_AI_OWASP_TEXTS`` that names one item is not the only item, part or piece naming its register row in any spelling, or a configured source with no list read; names without an edition are out of scope, and so are the other For-AI editions (ISO/IEC 42001:2023, ISO/IEC 23894:2023, ISO/IEC 42005:2025, ISO 31000:2018, ISO/IEC 27001:2022 and the rest), which this check does not compare).
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
import urllib.parse
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
    # Whether this variant renders the executive reading room (the on-site
    # narrative routes generated from the registry).
    narrative_routes: bool = False
    # Whether this variant renders the on-site document (L2) pages, one per
    # corpus document from the enriched taxonomy.
    document_routes: bool = False
    # The variant's own fixed page set (DRAFT_PAGES for the promoted tree).
    pages: tuple = None
    # Baseline-template draft rules (PR 2b, promoted to the root at the
    # draft-site promotion): the tree renders through render_draft_variant
    # (its own templates, partials and figure values), copies the pinned
    # baseline assets under <prefix>assets/baseline/ with SHA-256
    # verification against .baseline/pin.toml, and every rendered page must
    # pass the draft refusal guard (no inline style or script, no on*
    # attribute, no en or em dash, no "what this is" framing).
    draft_rules: bool = False


# The fixed pages of the promoted tree (the PR 2b baseline-template rebuild,
# flipped to the site root at the draft-site promotion): (template under
# .web/templates-draft/, output path at the dist root). The per-domain,
# per-type and per-document routes come from the same machinery the fixed
# pages cannot carry (one page per corpus domain; one per document type; one
# per non-root corpus document), inside render_draft_variant. The 404 page is
# excluded from sitemap.xml in render_site; Cloudflare Pages serves /404.html
# with status 404 for any missing path.
DRAFT_PAGES = (
    ("landing.html", "index.html"),
    ("browse.html", "browse/index.html"),
    ("search.html", "search/index.html"),
    ("documents.html", "documents/index.html"),
    ("crosswalk.html", "crosswalk/index.html"),
    ("govern.html", "govern/index.html"),
    ("comply.html", "comply/index.html"),
    ("solutions.html", "solutions/index.html"),
    ("policies.html", "policies/index.html"),
    ("contributors.html", "contributors/index.html"),
    ("for-ai.html", "for-ai/index.html"),
    ("disclosure.html", "disclosure/index.html"),
    ("license.html", "license/index.html"),
    ("404.html", "404.html"),
)

# The site variant table: exactly one indexable root variant (the promoted
# baseline-template tree; the old root and the v2/v3 staging trees are removed
# at the draft-site promotion, maintainer decision 2026-11-04). A future
# staging variant belongs in this table, so the template source, URL prefix,
# and indexability policy stay coupled.
VARIANTS = (
    Variant("draft", "templates-draft", "", indexable=True,
            document_routes=True, narrative_routes=True, pages=DRAFT_PAGES,
            draft_rules=True),
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

# The licence sentence closing every generated page description: CC BY-SA 4.0
# covers the library's own text only, matching each document's License field,
# and quoted third-party material keeps its own terms under NOTICE.md (3b550).
LICENCE_SEO_SUFFIX = (
    "Its own text is under CC BY-SA 4.0; quoted third-party material keeps "
    "its own terms (see NOTICE.md)."
)

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

# The shared-baseline CSP, copied byte for byte from the shared policy in
# baseline 1.7.0 SPECIFICATION.md section 9 (unchanged since 1.3.1; section 9
# states that the light and dark switch of 1.6.0 needs no CSP change): the
# same policy on every family site, and on every page here since the
# promotion executed the recorded owner decision that ``/*`` takes this
# policy when the baseline-template tree becomes the root (the old live
# CSP's ``style-src 'unsafe-inline'`` widening left with the old tree's
# inline styles). The 3 Cloudflare hosts are in
# tools/lint-external-link-domains.py ALLOW_LIST.
DRAFT_CSP = (
    "default-src 'none'; script-src 'self' 'unsafe-inline'"
    " https://ajax.cloudflare.com https://static.cloudflareinsights.com;"
    " connect-src 'self' https://cloudflareinsights.com; style-src 'self';"
    " font-src 'self'; img-src 'self'; base-uri 'none'; form-action 'none';"
    " frame-ancestors 'none'"
)

# The security headers Cloudflare Pages applies from the dist-root ``_headers``
# file: one ``/*`` rule carrying the spec section 9 CSP (the recorded
# at-promotion owner decision, executed at the draft-site promotion). The
# zone keeps sending X-Content-Type-Options, Referrer-Policy,
# Access-Control-Allow-Origin and Strict-Transport-Security automatically,
# so none of those is repeated here.
HEADERS_FILE = (
    "/*\n"
    f"  Content-Security-Policy: {DRAFT_CSP}\n"
    "  X-Frame-Options: DENY\n"
    "  Permissions-Policy: accelerometer=(), autoplay=(), bluetooth=(),"
    " browsing-topics=(), camera=(), display-capture=(), fullscreen=(),"
    " geolocation=(), gyroscope=(), hid=(), magnetometer=(), microphone=(),"
    " midi=(), payment=(), serial=(), usb=()\n"
    "  Cross-Origin-Opener-Policy: same-origin\n"
)

# The ``_redirects`` rules Cloudflare Pages applies from the dist root,
# emitted at the draft-site promotion (maintainer decisions 2026-11-04):
# every pre-promotion /draft/ address maps to its promoted root address
# through the splat (the promoted tree is the draft tree with the prefix
# stripped, so every target exists by construction); the old About page's
# contributor content moved to /contributors/; the old rule-pack page's
# subject is now the AIQT project. Round-2 fix 7: the splat covers only
# paths under /draft/, and Pages matches rules literally, so the slashless
# and explicit index.html spellings of each redirected address carry their
# own rules (/draft itself lands on the promoted root).
REDIRECTS_FILE = (
    "/draft/* /:splat 301\n"
    "/draft / 301\n"
    "/about/ /contributors/ 301\n"
    "/about /contributors/ 301\n"
    "/about/index.html /contributors/ 301\n"
    "/pack/ https://aiqt.ai/ 301\n"
    "/pack https://aiqt.ai/ 301\n"
    "/pack/index.html https://aiqt.ai/ 301\n"
)

# RFC 9116 security.txt, served at /.well-known/security.txt by the indexable
# root variant alone. Exact decided fields; the zone-level security.txt
# feature is switched off after deploy so this committed file is the one
# served.
SECURITY_TXT = (
    "Contact: mailto:jeff@posluns.ca\n"
    "Expires: 2030-10-31T00:00:00Z\n"
    "Encryption: https://posluns.ca/security/pgp-key.txt\n"
    "Policy: https://posluns.ca/security/\n"
    "Preferred-Languages: en, fr\n"
    "Canonical: https://grclibrary.ai/.well-known/security.txt\n"
)


# The prefixed staging block appended to the ``/*`` rule only while a
# draft-rules variant renders under a non-empty URL prefix: ``!`` detaches
# the root CSP, the spec section 9 CSP replaces it, and X-Robots-Tag keeps a
# staging tree out of search alongside each page's noindex meta. The block
# left the emitted ``_headers`` with the /draft/ prefix at promotion (the
# promoted tree has the empty prefix, so no page renders under /draft/).
# Never add X-Content-Type-Options, Referrer-Policy or
# Strict-Transport-Security here: the zone sends them automatically.
DRAFT_HEADERS_BLOCK = (
    "/draft/*\n"
    "  ! Content-Security-Policy\n"
    f"  Content-Security-Policy: {DRAFT_CSP}\n"
    "  X-Robots-Tag: noindex\n"
)


def render_headers_file():
    """The dist-root ``_headers`` content: the ``/*`` rule byte for byte, with
    the ``/draft/*`` block appended only while the variant table carries a
    draft-rules tree under a non-empty prefix (the block left with the prefix
    at promotion)."""
    if any(variant.draft_rules and variant.url_prefix for variant in VARIANTS):
        return HEADERS_FILE + DRAFT_HEADERS_BLOCK
    return HEADERS_FILE


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
    'route','domains','sources'}``, where ``domains`` holds the
    ``domain:<name>`` facets of the page's ``derived_tags``, ``sources`` holds
    the page's ``corpus_sources`` (the governing corpus documents the page
    resolves to), and ``route`` is the page's slug from the registry's
    ``listing:`` block.

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
                    "route": None, "domains": [], "sources": [],
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
            if line.rstrip() == "  corpus_sources:":
                cur_list = "sources"
                continue
            if _NARR_FIELD_RE.match(line):
                # Any other per-page field (external_sources:, version:, ...)
                # ends a derived_tags or corpus_sources block; their own nested
                # "- ..." items are then ignored below because cur_list is no
                # longer "tags" or "sources".
                cur_list = None
                continue
            if cur_list == "tags":
                mtag = _NARR_LIST_ITEM_RE.match(line)
                if mtag and mtag.group(1).startswith("domain:"):
                    cur["domains"].append(mtag.group(1)[len("domain:"):])
                continue
            if cur_list == "sources":
                msrc = _NARR_LIST_ITEM_RE.match(line)
                if msrc:
                    cur["sources"].append(msrc.group(1))
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
    no_sources = [p["path"] for p in pages if not p["sources"]]
    if no_sources:
        raise BuildError(
            f"{len(no_sources)} narrative registry page(s) with no corpus_sources "
            f"entry, so the concern pages' governing-documents join would silently "
            f"shrink (emit-shape drift? every published page resolves to the "
            f"corpus); first: {no_sources[0]}"
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
# emitting a duplicate id (RR guard, PR #1638). Keyed by template dir so a
# future second shell carries its own reservation; ``narr-intro`` is the
# renderer's own intro-section id and is always present.
NARRATIVE_SHELL_IDS = {
    # The shell's ids are every id its narrative.html carries (the
    # skip-link target, two heading anchors and the copy status line).
    "templates-draft": {
        "narr-intro", "main-content", "source", "domains", "copy-status",
    },
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
    # draft set for the direct-call test surface), so a body heading slugging to
    # one raises rather than emitting a duplicate id (RR guard, PR #1638).
    if reserved_shell_ids is None:
        reserved_shell_ids = NARRATIVE_SHELL_IDS["templates-draft"]
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


def narrative_route_bodies(figures, variant, seen_out_rels):
    """Yield ``(page, out_rel, body_html, toc)`` for every registry-listed
    narrative page of a routed type: the reading-room loop shared by the live
    staging trees (render_variant) and the /draft tree (render_draft_variant),
    so both read the same confined sources through the same renderer. Sources
    are read ONLY after the renderer-confinement validator admits them
    (registry-listed, normalized, git-tracked, under executive/ only), so this
    loop extends the generator's read allow-list to the registry-listed
    executive/ pages without the generator ever walking the repository.
    ``seen_out_rels`` holds the variant's already-rendered paths; a narrative
    route colliding with one raises."""
    # Every registry type must be a routed type: a future NEW narrative
    # type would otherwise fall through the filter below and silently
    # skip on-site rendering (PR-2b widened the tuple to all six
    # published types; this check keeps the widening honest). The
    # subtype-index table joins the union (round-2 fix 5): a type with a
    # DRAFT_NARRATIVE_SUBTYPES entry but no route would publish an index
    # whose pages the reading room never renders.
    unrouted = sorted(
        ({p["narrative_type"] for p in figures["narratives"]}
         | set(DRAFT_NARRATIVE_SUBTYPES))
        - set(NARRATIVE_ROUTE_TYPES)
    )
    if unrouted:
        raise BuildError(
            "narrative type(s) with no on-site route (in the registry or "
            "DRAFT_NARRATIVE_SUBTYPES; add to "
            f"NARRATIVE_ROUTE_TYPES): {', '.join(unrouted)}"
        )
    tracked = _tracked_executive_paths()
    seen_sources = set()
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
        yield page, out_rel, body_html, toc


def figure_values(figures, variant):
    """The corpus-derived values interpolated into every page: counts only,
    every one recomputed (decision: no count is ever typed into a
    template)."""
    return {
        "BASE": site_prefix_for(variant),
        "DOC_TOTAL": str(figures["total"]),
        "DOMAIN_COUNT": str(figures["domain_count"]),
        "DOMAIN_DOC_COUNT": str(figures["domain_docs"]),
        "ROOT_COUNT": str(figures["root_count"]),
        "TYPE_COUNT": str(len(figures["types"])),
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
    elif variant.draft_rules and out_rel != "404.html":
        # Promoted draft-rules pages carry an injected self-canonical: the
        # templates carry no canonical tag of their own (pre-promotion the
        # noindex injection above was the sole canonical source, so without
        # this branch the promoted pages would ship with none). The 404 page
        # is excluded, matching its sitemap exclusion; it carries a static
        # noindex meta in its template.
        if out_rel is None:
            raise BuildError(f"indexable variant page {template_name} has no output path")
        metadata = f'<link rel="canonical" href="{_site_url_for(variant, out_rel)}">'
        if _CANONICAL_TAG_RE.search(rendered):
            rendered = _CANONICAL_TAG_RE.sub(metadata, rendered)
        else:
            rendered = rendered.replace("</head>", f"{metadata}\n</head>", 1)
    return rendered, used


def render_robots_txt():
    """robots.txt welcoming AI and search crawlers. This corpus's original
    content is CC BY-SA 4.0 (quotations keep their own licences; see NOTICE.md)
    and it is intended to be widely read, cited, and learned from (including as AI
    training data), so the file names the known AI/training crawlers explicitly
    with ``Allow: /`` and then allows everyone via a trailing wildcard group,
    and advertises the sitemap. It is deliberately permissive and replaces any
    platform-managed default that would restrict AI crawlers."""
    lines = [
        "# grclibrary.ai",
        "# This is an open governance, risk, and compliance corpus, its original",
        "# content under CC BY-SA 4.0 (vendored third-party material and quotations",
        "# keep their own licences; see NOTICE.md in the source repository),",
        "# intended to be widely read, cited, and learned from, including as",
        "# training data for AI systems. All crawlers are welcome on every public path.",
        "",
    ]
    for ua in AI_CRAWLER_USER_AGENTS:
        lines += [f"User-agent: {ua}", "Allow: /", ""]
    lines += [
        "User-agent: *", "Allow: /", "",
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

> An openly-licensed corpus of organization-neutral governance,
> risk, and compliance documentation in Markdown, spanning {figures['domain_count']} domains including a
> self-contained AI-governance sub-corpus. Its original content is under CC BY-SA 4.0;
> vendored third-party material and quotations keep their own licences (see NOTICE.md).
> Descriptive reference material; not legal advice.

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


# A corpus link emitted into a page (hardcoded in a template, or generated
# from the taxonomy, the narrative registry or the crosswalk model).
# `render_corpus_link_manifest` scans the RENDERED pages for these so the
# manifest (and therefore gate 75) reaches every one; before that scan
# existed, 48 distinct targets were linked by the site and covered by no gate
# (Sweep 120 F2), and the promotion-era pages (document pages linking their
# own sources, the documents index's root-spec links, the licence and For-AI
# pages) would otherwise each need their own enumeration. The regex finds the
# blob base alone; the target after it is read by `_link_target`, the ONE
# extraction the uncounted-link check shares (round-3 fix 2).
TEMPLATE_CORPUS_LINK_RE = re.compile(re.escape(GITHUB_BLOB_BASE))

_ANCHOR_TEXT_RE_TEMPLATE = r'[^>]*>(?P<text>[^<]{1,120})</a>'

# The one link-target extraction (round-3 fix 2), shared by the manifest scan
# and the uncounted-link check so both end a link at the same characters: a
# target runs to the first double or single quote, fragment, query,
# whitespace, angle bracket or backslash. A closing parenthesis with no
# opener earlier in the target ends it too (the Markdown `[text](url)` and
# prose-parenthesis delimiters), while balanced parentheses stay inside, so a
# counted corpus path whose name carries parentheses is read whole by BOTH
# scans instead of splitting into a counted row and an uncounted link.
_LINK_TARGET_RUN_RE = re.compile(r"[^\"'#?\s<>\\]*")


def _link_target(text):
    """The link target at the start of ``text``, per the shared extraction."""
    run = _LINK_TARGET_RUN_RE.match(text).group(0)
    depth = 0
    for index, char in enumerate(run):
        if char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                return run[:index]
            depth -= 1
    return run


# Every spelling of a link to this repository (github.com and the raw host),
# however deep, as it appears in an emitted output (an HTML attribute, a
# Markdown link, or plain text): the https, http, protocol-relative // and
# bare www. forms, with the host, owner and repository matched
# case-insensitively, and a boundary required after the repository name so
# grc_library_ref (or any other grc_library-prefixed sibling) is never read
# as this repository. The regex ends at the repository name; the link's tail
# is read by `_link_target`, the same extraction the manifest scan uses.
# Used by the round-2 fix 3 coverage check: a repository link the manifest
# scan does not count (a raw, tree or other form, a non-canonical spelling,
# or a blob link in an output the scan does not read) would bypass gate 75's
# resolution, so emitting one fails the build.
REPO_LINK_RE = re.compile(
    r"(?:(?:https?:)?//(?:www\.)?|www\.)"
    r"(?:github\.com|raw\.githubusercontent\.com)"
    r"/jposluns/grc_library(?![\w-])",
    re.IGNORECASE,
)

# The bare repository root is not a corpus-path target and is deliberately
# excluded from the manifest (the llms.txt map and the topbar link it).
GITHUB_REPO_ROOT = "https://github.com/jposluns/grc_library"


def _staging_prefixes():
    """The dist-relative path prefixes of every non-indexable variant, for
    excluding staging outputs from the indexable-root manifest scan."""
    return tuple(
        v.url_prefix.strip("/") + "/"
        for v in VARIANTS
        if not v.indexable and v.url_prefix.strip("/")
    )


def _uncounted_repo_links(pages, counted_targets):
    """Repository links in ANY emitted output (HTML or not) that the manifest
    scan does not count, as ``[(dist-relative path, link), ...]``: a raw-host
    link, a tree or commit form, a non-canonical spelling (http, protocol-
    relative, www. or a case variant), a blob link to a target no counted row
    carries, or the blob base itself with no target. Each link's tail is read
    by ``_link_target``, the manifest scan's own extraction, so the two scans
    end every link at the same characters (round-3 fix 2). The bare
    repository root (with or without a trailing slash) stays excluded,
    matching the manifest's declared scope."""
    uncounted = []
    for rel, content in pages:
        text = (content.decode("utf-8", "replace")
                if isinstance(content, bytes) else content)
        for match in REPO_LINK_RE.finditer(text):
            link = match.group(0) + _link_target(text[match.end():])
            if link in (GITHUB_REPO_ROOT, GITHUB_REPO_ROOT + "/"):
                continue
            if link.startswith(GITHUB_BLOB_BASE):
                target = link[len(GITHUB_BLOB_BASE):]
                if target and target in counted_targets:
                    continue
            uncounted.append((rel, link))
    return uncounted


def render_corpus_link_manifest(figures, variant, pages):
    """The committed web-to-corpus link manifest: one row per corpus/GitHub
    target the indexable root variant's pages link (its repo-relative path,
    its website location, and its link text). Re-derived by scanning the
    RENDERED HTML pages of the indexable root variant alone (a staging
    tree's outputs are out of the manifest's declared scope) plus the
    curated llms.txt corpus links (CURATED_CORPUS_LINKS), so the manifest
    cannot drift from the emitted links, whatever machinery emitted them.
    The link text is the anchor's own text when it can be read, else the
    target's basename. The repo-root and on-site links are not corpus-path
    targets and are excluded, matching the gate's scope. ``pages`` is the
    render_site output (dist-relative path, content). Round-2 fix 3: any
    repository link in any emitted output that this scan does not count (a
    raw, tree or other form) is a BuildError, so no emitted link can bypass
    gate 75."""
    rows = {}  # (target, location) -> link_text, dedup-safe and deterministic
    for path, label in CURATED_CORPUS_LINKS:
        rows[(path, "llms.txt")] = label
    staging = _staging_prefixes()
    for rel, content in pages:
        if not rel.endswith(".html") or not isinstance(content, str):
            continue
        if staging and rel.startswith(staging):
            continue
        location = _site_path_for(variant, rel)
        for match in TEMPLATE_CORPUS_LINK_RE.finditer(content):
            target = _link_target(content[match.end():])
            if not target:
                continue  # the bare blob base links no corpus target
            end = match.end() + len(target)
            anchor = re.match(_ANCHOR_TEXT_RE_TEMPLATE, content[end:])
            label = (anchor.group("text").strip() if anchor
                     else target.rsplit("/", 1)[-1])
            rows[(target, location)] = label
    uncounted = _uncounted_repo_links(
        pages, {target for target, _ in rows}
    )
    if uncounted:
        listed = "; ".join(f"{rel}: {link}" for rel, link in uncounted[:20])
        raise BuildError(
            "repository link(s) the corpus-link manifest scan does not count "
            "(use the blob form the scan reads, or link the repository root): "
            + listed
        )
    lines = [
        "# Web-to-corpus link manifest",
        "",
        "Generated by `.web/build.py`; do not edit by hand. Every corpus/GitHub "
        "target the indexable root variant's pages link, with its website "
        "location and link text, scanned from the rendered pages themselves "
        "(so a hardcoded template link, a taxonomy-derived link and a "
        "registry-derived link all land here the same way), plus the curated "
        "`llms.txt` map. Gate 75 (`tools/lint-web-corpus-links.py`) resolves "
        "each target against the repo.",
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


# ---------------------------------------------------------------------------
# The /draft tree (PR 2b): the grclibrary.ai rebuild on the shared family site
# template (baseline 1.7.0, pinned under .web/baseline/ by PR 2a). The tree is
# VARIANT-SCOPED by Variant.draft_rules, renders from its own templates under
# .web/templates-draft/, and is self-contained: every internal link and asset
# is {{BASE}}-prefixed and the pinned baseline runtime files are copied to
# draft/assets/baseline/ at build time, each byte verified against
# .baseline/pin.toml (the same pin gate 110 checks). This section's reads
# extend the generator's allow-list by exactly .web/baseline/**,
# .baseline/pin.toml and the pinned palette gate .baseline/check_palette.py,
# which every draft build runs (spec section 4 item 3). Every rendered draft
# page must pass the draft refusal guard below (spec section 12 generator
# rule).
# ---------------------------------------------------------------------------

# Display label per corpus domain slug (the slug is the URL and the registry
# key; the label is the page wording, per the owner-approved mockups). The
# root specifications live in no corpus domain; their one area label is
# "Library", shown the same way on the type pages and the documents index. The
# docs/ area holds guides, templates and a register, so it is labelled by what
# every file in it is, an adopter document (site a9 round-4 WARN 1).
_DRAFT_DOMAIN_LABEL_OVERRIDES = {
    "ai": "AI", ROOT_DOMAIN: "Library", "docs": "Adopter documents",
}


def draft_domain_label(domain):
    """'governance' -> 'Governance', 'supply-chain' -> 'Supply chain',
    'root' -> 'Library'."""
    return _DRAFT_DOMAIN_LABEL_OVERRIDES.get(
        domain, domain.replace("-", " ").capitalize()
    )


# Section heading per document type on a draft domain page (the mockup uses
# plural headings). A taxonomy type with no entry is a build error, so a new
# type cannot publish a blank or misspelled heading.
DRAFT_TYPE_PLURALS = {
    "Standard": "Standards", "Procedure": "Procedures", "Annex": "Annexes",
    "Register": "Registers", "Template": "Templates", "Framework": "Frameworks",
    "Policy": "Policies", "Guideline": "Guidelines", "Plan": "Plans",
    "Matrix": "Matrices", "Specification": "Specifications",
    "Charter": "Charters", "Guide": "Guides", "SOP": "SOPs",
    "Checklist": "Checklists", "Principle": "Principles", "Roadmap": "Roadmaps",
}


def draft_type_plural(type_name):
    try:
        return DRAFT_TYPE_PLURALS[type_name]
    except KeyError:
        raise BuildError(
            f"draft: document type '{type_name}' has no plural heading in "
            "DRAFT_TYPE_PLURALS (add one to .web/build.py)"
        ) from None


# The adopter-document layer (site a9, maintainer decision 2026-11-03 14:59Z):
# every top-level docs/*.md adopter document gets a draft document page and a
# row in the draft's generated listings, like a corpus document. docs/ is
# adopter documentation OUTSIDE the corpus registries
# (specification-master-project.md section 4: not subject to the canonical
# governance-artefact regime, so taxonomy.yml cannot carry it), so the draft
# tree reads each file's own 13-field metadata block at build time instead.
# Every docs/ file carries the block (the generated portal, maturity scorecard
# and reference-acquisition manifest emit theirs from their generators), so a
# new adopter document appears on the next build with no generator edit, and a
# file without the leading block, missing any of the 13 fields, carrying an
# unknown or repeated field name, with an invalid Date or Version, or with a
# Related Documents entry the parser cannot keep or whose target is not a
# tracked file inside the repository fails the build loudly.
ADOPTER_DOCS_DIR = REPO_ROOT / "docs"
ADOPTER_DOCS_AREA = "docs"

_ADOPTER_FIELD_RE = re.compile(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$")
# Any Markdown link in a Related Documents value; the kept form is a
# backticked text over a .md target (round-3 note 5: every other link was
# dropped silently, so each one now fails the build).
_ADOPTER_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
_ADOPTER_LINK_TEXT_RE = re.compile(r"^`[^`]+`$")

# The 13 canonical metadata fields (tools/lint-metadata.py's model), every one
# required on every adopter document; any other field name is unknown and
# fails the build (the same loud-on-unknown stance as the corpus types).
ADOPTER_REQUIRED_FIELDS = (
    "Document Title", "Document Type", "Version", "Date", "Owner",
    "Approving Authority", "Related Documents", "Classification", "Category",
    "Review Frequency", "Repository Path", "Confidentiality", "License",
)

# The corpus's own version rule (MAJOR.MINOR.PATCH), the one the metadata
# gate applies to docs/ (the VERSION_RE of the engine behind gate
# lint-metadata, tools/lint-metadata.py) and the maturity heuristic reads
# (tools/build-portal.py classify_maturity), restricted to ASCII digits
# (round-4 WARN 2: the round-3 no-leading-zero rule refused versions the
# corpus gate accepts). A leading zero is accepted, as there. Then the ISO
# calendar-date form.
_ADOPTER_VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
_ADOPTER_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# A bold run-in label opening a paragraph ("**Purpose.** A public
# bibliography..."): a short bold span ending in a period or colon, stripped
# from a lede so the page lede starts with the prose, not the label.
_ADOPTER_RUNIN_RE = re.compile(r"^\*\*[^*]{1,40}?[.:]\*\*\s+")


def _tracked_repo_files():
    """The set of git-tracked repo-relative paths (paths only, never file
    content), the authority for the adopter Related Documents check: every
    kept target must be a tracked file inside the repository (round-4 note
    4). Fails LOUD when git cannot answer, like _tracked_executive_paths,
    with the same one-invocation safe.directory trust."""
    try:
        proc = subprocess.run(
            [
                "git", "-c", f"safe.directory={REPO_ROOT}",
                "-C", str(REPO_ROOT), "ls-files", "-z",
            ],
            capture_output=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError) as e:
        raise BuildError(
            "cannot establish the git-tracked file set for the adopter "
            f"Related Documents check (git ls-files failed: {e})"
        )
    tracked = {s for s in proc.stdout.decode("utf-8").split("\0") if s}
    if not tracked:
        raise BuildError(
            "git ls-files returned no tracked paths (not a git work tree?); "
            "refusing to keep adopter Related Documents targets unchecked"
        )
    return tracked


def _adopter_fence_line(line):
    """A code-fence marker line (backtick or tilde, indented under four
    columns), mirroring the taxonomy generator's shared fence predicate so a
    heading inside a fenced example (docs/worked-example.md carries a whole
    example document in a fence) never reads as structure."""
    stripped = line.lstrip(" ")
    if len(line) - len(stripped) >= 4:
        return False
    return stripped.startswith("```") or stripped.startswith("~~~")


def _adopter_flatten(text):
    """Reduce inline Markdown in a one-paragraph string to display-ready prose
    (mirrors the taxonomy generator's flattener for corpus purposes). A
    leading bold run-in label is dropped, not flattened: it labels the
    paragraph in source, and a lede that kept it would open "Purpose. A
    public bibliography..." (round-2 note 1)."""
    text = _ADOPTER_RUNIN_RE.sub("", text)
    text = re.sub(r"\[`?([^\]`]+)`?\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    text = text.replace("`", "")
    return re.sub(r"\s{2,}", " ", text).strip()


def _adopter_metadata(text, rel):
    """The LEADING ``**Field:** value`` block, hard-break backslashes stripped
    (mirrors the taxonomy generator's metadata reader). Only lines before the
    first code fence, horizontal rule, or section heading are read, so a
    fenced example document (docs/worked-example.md carries a whole one) can
    never read as the file's own block (round-2 error 1), and a file with no
    leading block fails the build loudly instead of rendering something
    else."""
    fields = {}
    seen = False
    for line in text.splitlines():
        s = line.strip()
        if _adopter_fence_line(line) or s.startswith("---") \
                or s.startswith("## "):
            break
        if not s and seen:
            break
        m = _ADOPTER_FIELD_RE.match(line)
        if m:
            name, value = m.groups()
            value = value.strip()
            if value.endswith("\\"):
                value = value[:-1].rstrip()
            # A repeated field name would overwrite the first value silently
            # (round-3 WARN 2), so the page could show either; refuse it.
            name = name.strip()
            if name in fields:
                raise BuildError(
                    f"adopter doc {rel} repeats metadata field '{name}' "
                    "(each field appears once in the leading block)"
                )
            fields[name] = value
            seen = True
    if not fields:
        raise BuildError(
            f"adopter doc {rel} has no leading metadata block (the "
            "**Field:** block before the first code fence, rule, or section)"
        )
    return fields


def _adopter_first_paragraph(lines):
    """First real prose paragraph, skipping sub-headings, stopping at the next
    top-level section or a horizontal rule."""
    para = []
    for nxt in lines:
        st = nxt.strip()
        if st == "---" or re.match(r"^##\s", nxt):
            break
        if re.match(r"^#{3,}\s", nxt):
            if para:
                break
            continue
        if not st:
            if para:
                break
            continue
        para.append(st)
    return " ".join(para)


def _adopter_purpose(text):
    """The document's lede: the first paragraph under a ``## Purpose`` or
    ``## Overview`` heading outside any code fence, else the intro paragraph
    between the metadata block and the first section (the worked examples
    carry no Overview heading). Empty string only if neither is present."""
    lines = text.splitlines()
    in_fence = False
    for i, ln in enumerate(lines):
        if _adopter_fence_line(ln):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.match(r"^##\s+(?:\d+\.\s+)?(?:Purpose|Overview)\b",
                    ln.strip(), re.I):
            return _adopter_flatten(_adopter_first_paragraph(lines[i + 1:]))
    started = False
    para = []
    for ln in lines:
        st = ln.strip()
        if st.startswith("## "):
            break
        if st.startswith("# "):
            continue
        if re.match(r"^\*\*[^*]+:\*\*", ln):
            started = True
            continue
        if st == "---" or re.match(r"^#{3,}\s", ln):
            continue
        if not st:
            if para:
                break
            continue
        if started:
            para.append(st)
        elif para:
            break
    return _adopter_flatten(" ".join(para)) if para else ""


def _adopter_sections(text):
    """The ordered ``## `` headings outside code fences (the page outline)."""
    out = []
    in_fence = False
    for ln in text.splitlines():
        if _adopter_fence_line(ln):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^##\s+(.+?)\s*$", ln)
        if m:
            out.append(m.group(1).strip())
    return out


def parse_adopter_docs():
    """One record per top-level ``docs/*.md`` adopter document (README.md
    included: docs/ carries none, and one added later must carry the block or
    the build fails loudly rather than skipping the file silently), read from
    the file's own LEADING metadata block (see the ADOPTER_DOCS_DIR note
    above), shaped like a parse_taxonomy_full entry so the draft document
    machinery renders it unchanged. Sorted by title then path for a stable,
    deterministic order. BuildError on a missing directory, no documents, a
    file without the block, a missing, unknown or repeated metadata field, an
    invalid Date or Version, a Related Documents entry that is not a
    backticked link to a .md target or whose target is not a tracked file
    inside the repository, or a document type outside
    DRAFT_TYPE_PLURALS (the same loud-on-unknown stance as the corpus type
    machinery). The fixture tests
    point ADOPTER_DOCS_DIR at doctored trees; a build always reads docs/."""
    if not ADOPTER_DOCS_DIR.is_dir():
        raise BuildError(
            f"adopter docs directory not found at {ADOPTER_DOCS_DIR}"
        )
    records = []
    tracked = None
    for path in sorted(ADOPTER_DOCS_DIR.glob("*.md")):
        rel = f"docs/{path.name}"
        text = path.read_text(encoding="utf-8")
        meta = _adopter_metadata(text, rel)
        unknown = sorted(set(meta) - set(ADOPTER_REQUIRED_FIELDS))
        if unknown:
            raise BuildError(
                f"adopter doc {rel} has unknown metadata field(s): "
                + ", ".join(unknown)
            )
        missing = [f for f in ADOPTER_REQUIRED_FIELDS if not meta.get(f)]
        if missing:
            raise BuildError(
                f"adopter doc {rel} is missing metadata field(s): "
                + ", ".join(missing)
            )
        try:
            if not _ADOPTER_DATE_RE.match(meta["Date"]):
                raise ValueError(meta["Date"])
            datetime.date.fromisoformat(meta["Date"])
        except ValueError:
            raise BuildError(
                f"adopter doc {rel} has an invalid Date '{meta['Date']}' "
                "(an ISO calendar date, yyyy-mm-dd, is required)"
            ) from None
        if not _ADOPTER_VERSION_RE.match(meta["Version"]):
            raise BuildError(
                f"adopter doc {rel} has an invalid Version "
                f"'{meta['Version']}' (the corpus's MAJOR.MINOR.PATCH form "
                "is required)"
            )
        doc_type = meta["Document Type"]
        if doc_type not in DRAFT_TYPE_PLURALS:
            raise BuildError(
                f"adopter doc {rel} has document type '{doc_type}' outside "
                "DRAFT_TYPE_PLURALS (add one to .web/build.py)"
            )
        # The link TARGET names the related file (round-2 fix 7: the link
        # text is display prose and nothing holds it to the repo path);
        # normalize it relative to docs/, where these links resolve from.
        # A link without backticked text or a .md target, and any entry
        # that is not a link at all, fails the build instead of dropping
        # from the page silently (round-3 note 5). A kept target must be a
        # tracked file inside the repository: an absolute URL, a path
        # outside the repository, and a missing file each rendered as a
        # broken link (round-4 note 4).
        related = []
        value = meta["Related Documents"]
        for m in _ADOPTER_LINK_RE.finditer(value):
            label, href = m.groups()
            if not _ADOPTER_LINK_TEXT_RE.match(label) \
                    or not href.endswith(".md"):
                raise BuildError(
                    f"adopter doc {rel} has a Related Documents link the "
                    f"parser cannot keep: {m.group(0)} (the form is "
                    "[`path`](target.md))"
                )
            target = posixpath.normpath(
                posixpath.join(ADOPTER_DOCS_AREA, href)
            )
            if tracked is None:
                tracked = _tracked_repo_files()
            target_path = REPO_ROOT / target
            if target not in tracked or not target_path.is_file() \
                    or target_path.resolve() != REPO_ROOT.resolve() / target:
                raise BuildError(
                    f"adopter doc {rel} has a Related Documents target "
                    f"that is not a tracked file inside the repository: "
                    f"{m.group(0)} (resolves to '{target}')"
                )
            related.append(target)
        leftover = _ADOPTER_LINK_RE.sub("", value).replace(",", "").strip()
        if leftover:
            raise BuildError(
                f"adopter doc {rel} has Related Documents text that is not a "
                f"link: '{leftover}' (each entry is [`path`](target.md))"
            )
        records.append({
            "path": rel,
            "domain": ADOPTER_DOCS_AREA,
            "type": doc_type,
            "title": meta["Document Title"],
            "version": meta["Version"],
            "date": meta["Date"],
            "owner": meta["Owner"],
            "approving_authority": meta["Approving Authority"],
            "classification": meta["Classification"],
            "category": meta["Category"],
            "review_frequency": meta["Review Frequency"],
            "license": meta["License"],
            "confidentiality": meta["Confidentiality"],
            "purpose": _adopter_purpose(text),
            "sections": _adopter_sections(text),
            "frameworks": [],
            "related_documents": related,
        })
    if not records:
        raise BuildError(f"no adopter documents found under {ADOPTER_DOCS_DIR}")
    records.sort(key=lambda r: (r["title"].lower(), r["path"]))
    return records


# The generated subtype index pages, one per narrative type, at
# decide/<slug>/ (design D section 4.1 branch 2): (route slug, plural
# heading, the reader's question the subtype answers). Mirrors
# DRAFT_TYPE_PLURALS: a registry narrative_type with no entry is a build
# error, so a new narrative type cannot publish without its index.
DRAFT_NARRATIVE_SUBTYPES = {
    "Executive Brief": (
        "briefs", "Executive briefs",
        "What should we require before we approve this?"),
    "Scenario": (
        "scenarios", "Scenarios",
        "What does the bad day look like, and would we cope?"),
    "Journey": (
        "journeys", "Journeys",
        "How does one thing move through governance end to end?"),
    "Outcome Map": (
        "outcome-maps", "Outcome maps",
        "How would we know, with evidence, that the outcome holds?"),
    "Oversight Question Set": (
        "question-sets", "Oversight question sets",
        "What should we ask, and what evidence should come back?"),
    "Decision Narrative": (
        "choices", "Decision narratives",
        "What are the options on a genuine choice, and the trade-offs?"),
}


def draft_narrative_subtype(narrative_type):
    try:
        return DRAFT_NARRATIVE_SUBTYPES[narrative_type]
    except KeyError:
        raise BuildError(
            f"draft: narrative type '{narrative_type}' has no subtype index "
            "in DRAFT_NARRATIVE_SUBTYPES (add one to .web/build.py)"
        ) from None


def _draft_subtype_url(narrative_type):
    slug, _, _ = draft_narrative_subtype(narrative_type)
    return "{{BASE}}/decide/" + slug + "/"


# The decide hub's three board-question groups (design D section 4.1 branch 1,
# carried from templates-v3/decide.html): (section anchor slug, the question).
DRAFT_DECIDE_GROUPS = (
    ("withstand", "Can we withstand what hits us?"),
    ("prove", "Can we prove we are in control?"),
    ("run-well", "Are we running and funding it well?"),
)

# The 14 leadership concerns (design D section 5): v2's set, the ten of
# executive/README.md plus the four templates-v2/decisions.html added. The
# curated prose is limited to the label, the question-led title and the
# two-sentence exposure lede, each carried from templates-v2/decisions.html and
# re-edited to the draft rules; the four concerns v3's decide page never
# carried are grouped here under the same three board questions. The concern
# set and its grouping are this curated table; the rows, counts and documents
# under each concern are generated at build time from narrative.yml and
# taxonomy.yml. ``pages`` maps the concern to registry paths; the loud checks
# in draft_concern_join keep the mapping mechanical rather than silently
# stale. ``corpus`` is the corpus-only material of a declared-gap concern (the
# templates-v2/decisions.html stance: a gap is declared, never hidden and
# never padded), taxonomy paths validated at build time, allowed only on a
# concern with no mapped page and required there, so the documents shelf's
# intro stays true and the shelf is never empty. A
# lede is read on its own concern page, never beside the other concerns, so
# it must not lean on v2's or v3's multi-concern page.
DRAFT_CONCERNS = (
    {
        "slug": "resilience",
        "group": "withstand",
        "label": "Cybersecurity and operational resilience",
        "question": "Could we take the hit and keep operating?",
        "lede": (
            "Preventing every incident is not a plausible plan; withstanding "
            "one is. The exposure leadership owns is the gap between the "
            "controls that exist on paper and the organization's tested "
            "ability to absorb an identity-provider compromise, a compromised "
            "release-signing key, or the loss of a critical service, and keep "
            "operating."
        ),
        "pages": (
            "executive/briefs/brief-ai-resilience-continuity.md",
            "executive/scenarios/scenario-identity-provider-compromise.md",
            "executive/scenarios/scenario-release-signing-key-compromise.md",
            "executive/outcome-maps/outcome-map-continuity-recovery-readiness.md",
        ),
        "corpus": (),
    },
    {
        "slug": "data-privacy",
        "group": "withstand",
        "label": "Data, privacy and the information lifecycle",
        "question": "Do we control our information from creation to destruction?",
        "lede": (
            "Information the organization cannot classify, locate, or "
            "provably destroy is a liability with no expiry date. "
            "Cross-border movement and changing legal boundaries turn quiet "
            "data flows into board-level exposure without any system changing "
            "at all."
        ),
        "pages": (
            "executive/briefs/brief-ai-data-governance.md",
            "executive/scenarios/scenario-jurisdictional-data-redesign.md",
            "executive/journeys/journey-record-retention-destruction.md",
            "executive/oversight-question-sets/oversight-questions-privacy-data-protection.md",
        ),
        "corpus": (),
    },
    {
        "slug": "supplier-cloud",
        "group": "withstand",
        "label": "Supplier and cloud dependency",
        "question": "How exposed are we through the parties we depend on?",
        "lede": (
            "Most organizations now run on other people's infrastructure, "
            "software, and models. The exposure is concentration you have not "
            "measured, exits you have not rehearsed, and assurance you have "
            "taken on a supplier's word, discovered, typically, on the day a "
            "critical supplier fails."
        ),
        "pages": (
            "executive/briefs/brief-ai-supply-chain-oversight.md",
            "executive/scenarios/scenario-critical-supplier-outage.md",
            "executive/decision-narratives/decision-cloud-concentration-exit.md",
        ),
        "corpus": (),
    },
    {
        "slug": "ai-systems",
        "group": "withstand",
        "label": "AI and autonomous systems",
        "question": "What is AI doing on our behalf, and who approved it?",
        "lede": (
            "AI is one leadership concern among the others on the decide "
            "hub: governed like the rest, which is precisely the point. The "
            "questions are "
            "the familiar governance questions asked of a new class of "
            "system: what is deployed, on whose approval, under whose "
            "oversight, with what authority, and what happens when it acts "
            "beyond it."
        ),
        "pages": (
            "executive/briefs/brief-ai-production-approval.md",
            "executive/briefs/brief-ai-incident-response-readiness.md",
            "executive/journeys/journey-ai-idea-to-retirement.md",
            "executive/scenarios/scenario-ai-agent-exceeds-authority.md",
            "executive/oversight-question-sets/oversight-questions-ai-inventory-risk.md",
            "executive/decision-narratives/decision-human-review-oversight.md",
        ),
        "corpus": (),
    },
    {
        "slug": "accountability",
        "group": "prove",
        "label": "Accountability and decision rights",
        "question": "Who owns this decision, and where is that written?",
        "lede": (
            "A decision with no named owner still gets made: by a supplier's "
            "default, an engineer's judgement call, or nobody, until an "
            "incident assigns it in hindsight. The governing body remains "
            "accountable either way."
        ),
        "pages": (
            "executive/briefs/brief-ai-production-approval.md",
            "executive/decision-narratives/decision-human-review-oversight.md",
            "executive/decision-narratives/decision-cloud-concentration-exit.md",
        ),
        "corpus": (),
    },
    {
        "slug": "compliance-assurance",
        "group": "prove",
        "label": "Compliance and assurance",
        "question": "Can we show, with evidence, that our controls operate?",
        "lede": (
            "\"We have a policy\" is an assertion; what an auditor, a "
            "regulator, or a court asks for is evidence that the control the "
            "policy requires actually operated, on the days it mattered. The "
            "exposure is the distance between the two."
        ),
        "pages": (
            "executive/outcome-maps/outcome-map-control-effectiveness.md",
            "executive/outcome-maps/outcome-map-regulatory-obligations-coverage.md",
            "executive/outcome-maps/outcome-map-continuity-recovery-readiness.md",
            "executive/journeys/journey-privileged-access-assurance.md",
        ),
        "corpus": (),
    },
    {
        "slug": "risk-acceptance",
        "group": "prove",
        "label": "Risk acceptance and exceptions",
        "question": "Which risks have we knowingly accepted, and who signed?",
        "lede": (
            "Every organization accepts risk; the question is whether it does "
            "so on purpose. Silent exceptions (the control that was waived "
            "and never revisited) surface in the post-incident review, "
            "attached to no name and no expiry date."
        ),
        "pages": (
            "executive/briefs/brief-ai-production-approval.md",
            "executive/scenarios/scenario-risk-appetite-breach.md",
        ),
        "corpus": (),
    },
    {
        "slug": "crypto-asset-governance",
        "group": "prove",
        "label": "Crypto-asset governance",
        "question": (
            "Do we govern our crypto-asset and blockchain activity before it "
            "starts?"
        ),
        "lede": (
            "Crypto-asset activity concentrates several exposures at once: "
            "assets that can be irreversibly lost if keys are mishandled, and "
            "stable-value tokens whose holders rely on a backing the "
            "organization must actually hold. It also brings disclosures that "
            "carry legal liability, and third-party providers and "
            "smart-contract code the organization does not fully control."
        ),
        "pages": (
            "executive/briefs/brief-crypto-asset-governance-oversight.md",
            "executive/oversight-question-sets/oversight-questions-crypto-asset-governance.md",
            "executive/scenarios/scenario-crypto-custody-key-compromise.md",
        ),
        "corpus": (),
    },
    {
        "slug": "enterprise-risk-governance",
        "group": "prove",
        "label": "Enterprise risk governance",
        "question": (
            "Do we know our enterprise risk is actually governed, not just "
            "listed?"
        ),
        "lede": (
            "A risk register is not the same as governed risk. The governing "
            "body needs to see that risks are measured on one consistent "
            "scale, weighed against an appetite it set, escalated when a "
            "tolerance is breached, decided through a governed acceptance "
            "rather than absorbed silently, and reported on a cadence, with "
            "assurance mapped to the risks that matter most."
        ),
        "pages": (
            "executive/briefs/brief-enterprise-risk-governance-oversight.md",
            "executive/oversight-question-sets/oversight-questions-enterprise-risk-appetite.md",
            "executive/scenarios/scenario-risk-appetite-breach.md",
        ),
        "corpus": (),
    },
    {
        "slug": "architecture-debt",
        "group": "run-well",
        "label": "Enterprise architecture and technology debt",
        "question": "What is our accumulated technology debt costing us?",
        "lede": (
            "Deferred modernization compounds quietly: each postponement is "
            "individually rational and collectively a balance-sheet exposure "
            "no one owns. Leadership finds out what the debt cost when a "
            "change that should take weeks takes quarters, or when the "
            "unsupported component fails."
        ),
        "pages": (
            "executive/oversight-question-sets/oversight-questions-architecture-technology-debt.md",
        ),
        "corpus": (),
    },
    {
        "slug": "workforce",
        "group": "run-well",
        "label": "Workforce, conduct and the operating model",
        "question": (
            "Do the people running the controls have the mandate to run them?"
        ),
        "lede": (
            "Controls are run by people: screened, trained, empowered people, "
            "or not. The exposure is an operating model where responsibility "
            "is assigned to roles that lack the authority, the headcount, or "
            "the reporting line to act on it."
        ),
        "pages": (
            "executive/briefs/brief-workforce-conduct-oversight.md",
        ),
        "corpus": (),
    },
    {
        "slug": "it-operations-governance",
        "group": "run-well",
        "label": "IT operations governance",
        "question": (
            "Do we know our IT operations run under a controlled governance "
            "model?"
        ),
        "lede": (
            "Most technology risk is realized in daily operations: an "
            "unauthorized change breaks production, an unknown asset goes "
            "unpatched, a service degrades below what the business was "
            "promised. The governing body's question is not whether "
            "operations run, but whether it can require, and see in evidence, "
            "that changes are authorized, the estate is known, "
            "vulnerabilities are managed, production is secured, service "
            "levels are managed, and operational state is measured."
        ),
        "pages": (
            "executive/briefs/brief-it-operations-governance-oversight.md",
            "executive/oversight-question-sets/oversight-questions-it-operations-governance.md",
            "executive/scenarios/scenario-unauthorized-production-change-outage.md",
        ),
        "corpus": (),
    },
    {
        "slug": "secure-development-governance",
        "group": "run-well",
        "label": "Secure-development governance",
        "question": (
            "Do we build our software under a controlled secure-development "
            "model?"
        ),
        "lede": (
            "Software is where an organization builds its own risk: insecure "
            "code, an insecure delivery pipeline, defects merged without "
            "review, and unvetted open-source or AI-suggested dependencies "
            "all enter through development. The governing body's question is "
            "not whether software ships, but whether it can require, and see "
            "in evidence, that software is designed, coded, reviewed, tested, "
            "and its dependencies vetted under a controlled model."
        ),
        "pages": (
            "executive/briefs/brief-secure-development-governance-oversight.md",
            "executive/oversight-question-sets/oversight-questions-secure-development-governance.md",
            "executive/scenarios/scenario-ai-suggested-malicious-dependency.md",
        ),
        "corpus": (),
    },
    {
        "slug": "programme-maturity",
        "group": "run-well",
        "label": "Programme establishment and maturity",
        "question": (
            "Where does our programme stand, and what would better look like?"
        ),
        "lede": (
            "A governance programme is itself something to govern: it has a "
            "current state, a target state, and a path between them that "
            "someone must own. Without an honest maturity picture, investment "
            "goes where the last incident pointed."
        ),
        "pages": (),
        "corpus": (
            "governance/guideline-minimum-viable-governance-structure.md",
        ),
    },
)


def draft_concern_join(figures, docs_by_path):
    """Resolve DRAFT_CONCERNS against the registries: per concern, the mapped
    registry pages (the leadership list, the v2/v3 domain-page join order),
    the union of those pages' corpus_sources joined to the taxonomy (the
    governing-documents shelf; a declared-gap concern contributes its
    corpus-only material), the frameworks those documents touch, and the
    domains behind it. Loud checks make the mapping mechanical rather than
    silently stale: a duplicate or subtype-colliding slug, an unknown group, a
    mapped path missing from narrative.yml, corpus-only material on a concern
    that has mapped pages (the shelf intro says its documents are the ones
    the pages resolve to), a concern with neither mapped pages nor corpus-only
    material (its gap intros would sit over an empty shelf), a corpus path
    missing from taxonomy.yml (or in the root domain, which has no draft
    document page), and a registry page mapped to no concern each fail the
    build, so
    publishing a new narrative page fails the draft build until its one-line
    mapping is added."""
    slugs = [concern["slug"] for concern in DRAFT_CONCERNS]
    repeated = sorted({s for s in slugs if slugs.count(s) > 1})
    if repeated:
        raise BuildError(
            "draft: repeated concern slug(s) in DRAFT_CONCERNS: "
            + ", ".join(repeated)
        )
    subtype_slugs = {slug for slug, _, _ in DRAFT_NARRATIVE_SUBTYPES.values()}
    clashes = sorted(set(slugs) & subtype_slugs)
    if clashes:
        raise BuildError(
            "draft: concern slug(s) collide with a decide/ subtype index "
            "route: " + ", ".join(clashes)
        )
    group_slugs = {slug for slug, _ in DRAFT_DECIDE_GROUPS}
    by_path = {p["path"]: p for p in figures["narratives"]}
    mapped = set()
    joined = []
    for concern in DRAFT_CONCERNS:
        slug = concern["slug"]
        if concern["group"] not in group_slugs:
            raise BuildError(
                f"draft: concern '{slug}' names a group outside "
                f"DRAFT_DECIDE_GROUPS: {concern['group']}"
            )
        if concern["pages"] and concern["corpus"]:
            raise BuildError(
                f"draft: concern '{slug}' has mapped pages and corpus-only "
                "material; corpus is for a declared-gap concern only (map a "
                "page whose corpus_sources carry the document instead)"
            )
        if not concern["pages"] and not concern["corpus"]:
            raise BuildError(
                f"draft: concern '{slug}' has no mapped page and no "
                "corpus-only material; a declared-gap concern lists the "
                "corpus documents that support it, so its evidence shelf is "
                "never empty"
            )
        pages = []
        for path in concern["pages"]:
            page = by_path.get(path)
            if page is None:
                raise BuildError(
                    f"draft: concern '{slug}' maps a page not in "
                    f"narrative.yml: {path}"
                )
            pages.append(page)
            mapped.add(path)
        pages.sort(
            key=lambda p: (p["narrative_type"], p["title"].lower(), p["path"])
        )
        doc_paths = sorted(
            {s for p in pages for s in p["sources"]} | set(concern["corpus"])
        )
        docs = []
        for doc_path in doc_paths:
            doc = docs_by_path.get(doc_path)
            if doc is None:
                raise BuildError(
                    f"draft: concern '{slug}': corpus source not in "
                    f"taxonomy.yml: {doc_path}"
                )
            if doc.get("domain") == ROOT_DOMAIN:
                raise BuildError(
                    f"draft: concern '{slug}': corpus source in the root "
                    f"domain, which has no draft document page: {doc_path}"
                )
            docs.append(doc)
        docs.sort(key=lambda d: (
            TYPE_RANK.get(d.get("type"), len(TYPE_ORDER)),
            d.get("title", "").lower(), d["path"],
        ))
        frameworks = sorted({f for d in docs for f in d.get("frameworks", [])})
        if pages:
            domains = sorted({d for p in pages for d in p["domains"]})
        else:
            # A declared-gap concern derives its Go deeper chips from its
            # corpus-only material instead (blocks 3 to 5 where derivable).
            domains = sorted({d.get("domain") for d in docs})
        joined.append({
            **concern,
            "mapped_pages": pages,
            "docs": docs,
            "frameworks": frameworks,
            "domains": domains,
        })
    unmapped = sorted(set(by_path) - mapped)
    if unmapped:
        raise BuildError(
            "draft: narrative registry page(s) mapped to no concern (add a "
            "one-line mapping to DRAFT_CONCERNS): " + ", ".join(unmapped)
        )
    return joined


# The owner-approved example document (the mockup's "Open a document" tile and
# the last domain page's Next). Validated against the taxonomy on every draft
# render, so a rename fails the build instead of publishing a dead link.
DRAFT_EXAMPLE_DOC = "governance/policy-exception-and-risk-acceptance-management.md"
# The landing tile's example domain (the mockup's "Open a domain: Governance").
DRAFT_EXAMPLE_DOMAIN = "governance"

# The browse page's "By need" entries (approved mockup copy, with the Find a
# solution and Write a policy lines changed by maintainer directive
# 2026-11-03 17:55Z; the mockup's placeholder targets, two Browse anchors,
# the search page and one example document, are retired for the five need
# pages of the Browse adventure, design D section 3). (title, tag, href,
# line).
DRAFT_NEEDS = (
    ("Make a decision", "decide", "{{BASE}}/decide/",
     "What the board should ask: decision briefs, oversight questions, and "
     "the evidence to expect back."),
    ("Govern a programme", "govern", "{{BASE}}/govern/",
     "Stand up a programme, run it, or assess its maturity, with charters, "
     "policies, and registers ready to adapt."),
    ("Meet an obligation", "comply", "{{BASE}}/comply/",
     "Choose a framework, see the mappings and the gaps, and assemble the "
     "evidence an audit will ask for."),
    ("Find a solution", "solutions", "{{BASE}}/solutions/",
     "Start from a problem or a lifecycle event and follow it to the "
     "leadership pages and documents that resolve it."),
    ("Write a policy", "policies", "{{BASE}}/policies/",
     "Choose a policy or template, by type or by subject, and adapt it to "
     "your organization."),
)

# ---------------------------------------------------------------------------
# The Browse adventure's need pages (design D sections 4.2 to 4.5): govern/,
# comply/, solutions/ and policies/, one question per page, every branch
# landing on a generated page (domain, type and concern pages, the crosswalk
# and its instrument pages, the reading room), carried from
# templates-v2/start.html and the templates-v3 need pages and re-edited to
# the draft rules. The curated prose lives in the templates; every count,
# list and link target below is generated or validated at build time.

# The govern path's staged-step artefacts, template placeholder -> (repo
# path, link label). The adopter docs/ documents are outside taxonomy.yml
# (design D gap G1) but render draft document pages since site a9, so each
# link resolves to the artefact's draft document page where the taxonomy or
# the adopter documents carry it, else to its GitHub source, and a path
# missing from the repository fails the build instead of publishing a dead
# link.
DRAFT_GOVERN_ARTEFACTS = {
    "GOV_ART_MVGS": (
        "governance/guideline-minimum-viable-governance-structure.md",
        "minimum viable governance structure guideline"),
    "GOV_ART_QUICKSTART": (
        "docs/template-quickstart.md", "quickstart template"),
    "GOV_ART_ROADMAP": (
        "docs/template-startup-roadmap.md", "startup roadmap template"),
    "GOV_ART_ADOPTER_GUIDE": ("docs/adopter-guide.md", "adopter guide"),
    "GOV_ART_DECISION_TREE": (
        "docs/decision-tree.md", "applicability decision tree"),
    "GOV_ART_PORTAL": ("docs/portal.md", "adopter portal"),
    "GOV_ART_SELF_ASSESSMENT": (
        "docs/template-maturity-self-assessment.md",
        "maturity self-assessment template"),
    "GOV_ART_MULTI_ENTITY": (
        "docs/adopter-guide-multi-entity.md", "multi-entity adopter guide"),
    "GOV_ART_COMPLIANCE_MATRIX": (
        "compliance/matrix-grc-compliance-alignment.md",
        "compliance alignment matrix"),
    "GOV_ART_REVERSE_MATRIX": (
        "governance/matrix-reverse-framework-control-crosswalk.md",
        "reverse framework-control crosswalk"),
    "GOV_ART_CITATIONS_REGISTER": (
        "governance/register-canonical-citations.md",
        "canonical citations register"),
}

# Where the govern path lands (design D section 4.2): the two programme
# areas, the document types that stand a programme up, and the
# programme-maturity concern page appended in draft_govern_values. Each type
# maps to what its documents do for the programme, the clause the Lands
# sentence carries, so the sentence's type count and clauses come from this
# one table.
DRAFT_GOVERN_LANDING_DOMAINS = ("governance", "compliance")
DRAFT_GOVERN_LANDING_TYPES = {
    "Roadmap": "stage it",
    "Charter": "establish the authority to do it",
    "Plan": "coordinate the events it must survive",
}
DRAFT_GOVERN_CONCERN = "programme-maturity"

# The solutions path's lifecycle events (design D section 4.4, routings
# carried from templates-v3/solutions.html): (label, lede, main narrative
# path or None, resolving concern slug, extra domain links). A narrative
# path outside the registry, a concern slug outside DRAFT_CONCERNS or a
# domain outside the taxonomy fails the build.
DRAFT_SOLUTION_EVENTS = (
    ("Secure privileged access",
     "Admin accounts, service accounts, and the people who can change "
     "everything.",
     "executive/journeys/journey-privileged-access-assurance.md",
     "compliance-assurance", ("security",)),
    ("Respond to an incident",
     "Detection, coordination, communication, and recovery.",
     None, "resilience", ("resilience", "security", "operations")),
    ("Govern an AI system end to end",
     "Intake, approval, oversight, incidents, and retirement, governed like "
     "any other system.",
     "executive/journeys/journey-ai-idea-to-retirement.md",
     "ai-systems", ()),
    ("Manage a supplier",
     "Onboarding, ongoing monitoring, concentration, and exit.",
     None, "supplier-cloud", ()),
    ("Retain and destroy records",
     "Classification, retention, cross-border movement, and provable "
     "destruction.",
     "executive/journeys/journey-record-retention-destruction.md",
     "data-privacy", ()),
)

# The solutions path's builders block (carried from
# templates-v3/solutions.html): the domains that carry the technology side.
DRAFT_SOLUTION_BUILDER_DOMAINS = ("architecture", "dev-security", "operations")

# The comply path's not-listed branch (design D section 4.3 branch 2): the
# coverage-gaps register and the regulatory-obligations outcome map, each
# validated against its registry at build time.
DRAFT_COMPLY_GAPS_REGISTER = "governance/register-coverage-gaps.md"
DRAFT_COMPLY_OUTCOME_MAP = (
    "executive/outcome-maps/outcome-map-regulatory-obligations-coverage.md"
)


# The draft document record's field order and wording (Canadian spelling for
# the licence label; values come from the enriched taxonomy).
DRAFT_RECORD_FIELDS = (
    ("Type", "type"), ("Version", "version"), ("Date", "date"),
    ("Owner", "owner"), ("Approving authority", "approving_authority"),
    ("Classification", "classification"),
    ("Confidentiality", "confidentiality"), ("Category", "category"),
    ("Review frequency", "review_frequency"), ("Licence", "license"),
)

_DRAFT_NEW_TAB = '<span class="vh"> (opens in a new tab)</span>'


def _draft_wrapping_path(text):
    """Escaped ``text`` with a <wbr> after each slash (after the pair in
    "//"), so a web address or corpus path shown as link text can wrap where
    the browser finds no other break; unbroken, one widened its page past
    320 px (item 3b788). The text still reads, and copies, the same."""
    return re.sub("/(?!/)", "/<wbr>", _esc(text))


# A document h1 word longer than this many letters gets a soft hyphen, so the
# heading can break it; a shorter one moves whole to the next line. At 320 px
# the h1 box is 288 px (the narrow layout's 2.2rem Newsreader 300). Of the 125
# distinct title words of 10 or more letters measured there (headless Chrome,
# light and dark), every one of 17 letters or fewer fits with at least 12 px
# to spare, the widest "Pseudonymization" (16 letters, 275.2 px in the dark
# scheme), while "Telecommunications" (18 letters, 307.4 px in dark) runs
# 19 px past the box and widened its page to 323 px (item 3b788). At the
# widest rate measured, "Management"'s 19.6 px a letter, only 14 letters
# (274 px) fit, so the test holds each h1 piece of more than 14 letters, a
# whole word or a piece of a split one, to the ones measured (item 3b788 lows
# round 1).
DRAFT_TITLE_RUN_MAX = 17
_DRAFT_TITLE_RUN_RE = re.compile(rf"[^\W\d_]{{{DRAFT_TITLE_RUN_MAX + 1},}}")
_DRAFT_VOWELS = frozenset("aeiouyAEIOUY")
_DRAFT_DIGRAPHS = frozenset({"ch", "ck", "gh", "ph", "qu", "sh", "th", "wh"})


def _draft_soft_hyphenated(word):
    """``word`` with a U+00AD soft hyphen at the syllable break nearest its
    middle (before a consonant a vowel follows, never inside a digraph:
    "Telecommu-nications"), again in either half while it is longer than
    DRAFT_TITLE_RUN_MAX letters."""
    if len(word) <= DRAFT_TITLE_RUN_MAX:
        return word
    breaks = [
        i for i in range(2, len(word) - 2)
        if word[i] not in _DRAFT_VOWELS and word[i + 1] in _DRAFT_VOWELS
        and (word[i - 1] in _DRAFT_VOWELS
             or word[i - 1:i + 1].lower() not in _DRAFT_DIGRAPHS)
    ]
    mid = len(word) // 2
    at = min(breaks, key=lambda i: abs(i - mid), default=mid)
    return (_draft_soft_hyphenated(word[:at]) + "\u00ad"
            + _draft_soft_hyphenated(word[at:]))


def _draft_breakable_title(title):
    """Escaped ``title`` for a document h1, with &shy; in each word longer
    than DRAFT_TITLE_RUN_MAX letters. The heading reads the same and shows a
    hyphen only where it breaks; the page's <title> keeps the plain text."""
    return _esc(_DRAFT_TITLE_RUN_RE.sub(
        lambda m: _draft_soft_hyphenated(m.group(0)), title
    )).replace("\u00ad", "&shy;")


# The constrained narrative renderer's shapes the draft shell adapts (the
# renderer itself is shared with v2 and v3 and stays unchanged). The baseline
# lays a .doc section out with display: contents, which gives the section no
# box, so its id moves to the inner block (an anchor or rail.js target needs
# a box) and the inner block drops the .wrap class the draft page already
# supplies. A body link to the source on GitHub gains the draft's external
# link form: noreferrer and the hidden new-tab hint.
_DRAFT_NARR_SECTION_RE = re.compile(
    r'<section class="narr" id="([^"]+)">\n    <div class="wrap">'
)
_DRAFT_NARR_LINK_RE = re.compile(
    r'(<a href="[^"]*") target="_blank" rel="noopener">([^<]*)</a>'
)
# A body table sits in the baseline's .tablewrap, so a table wider than the
# page scrolls inside that box and not the page: the outcome maps' nowrap
# uppercase headers made the page 522 px wide at 320 px (item 3b788).
_DRAFT_NARR_TABLE_RE = re.compile(r"<table>(.*?)</table>", re.S)

# ---------------------------------------------------------------------------
# The /draft/crosswalk/ pages (design C section 3.7 Version A, upgraded to
# 3.8; on baseline 1.7.0, whose matrix.js arrived in 1.5.0, spec 7.30 to 7.32
# keep their 1.5.1 contract for a page without the opt-in column toggles,
# column highlight and pinned-column cap that 1.7.0 adds, none of which these
# pages use): one domain-by-instrument table,
# one page per instrument, and static preset views, all re-parsed on every
# build from the
# two alignment matrices, the canonical citations register, and taxonomy.yml,
# structural and loud on schema change exactly like parse_taxonomy. The
# crosswalk page is a left-rail page (spec 7.32) whose side list carries the
# matrix.js column presets (spec 7.30), one per topic view of design C 3.7
# (maintainer decision 2026-11-03 18:53Z: the views stay by topic), and every
# instrument by group; each preset is a link to its static view page, so the
# views still resolve without script.

CROSSWALK_COMPLIANCE_MATRIX = (
    REPO_ROOT / "compliance" / "matrix-grc-compliance-alignment.md"
)
CROSSWALK_REVERSE_MATRIX = (
    REPO_ROOT / "governance" / "matrix-reverse-framework-control-crosswalk.md"
)
# The forward matrix carries the "not an official mapping" caveat the page
# repeats (design C 3.6); its on-site document page is linked from the block.
CROSSWALK_FORWARD_MATRIX_PATH = "governance/matrix-cross-framework-alignment.md"
CROSSWALK_COMPLIANCE_MATRIX_PATH = "compliance/matrix-grc-compliance-alignment.md"
CROSSWALK_REVERSE_MATRIX_PATH = (
    "governance/matrix-reverse-framework-control-crosswalk.md"
)

# The compliance matrix's ten framework columns, in its own header order. A
# renamed, added, or removed column is a schema change the parser must refuse
# loudly, so the expected header is pinned here.
CROSSWALK_COMPLIANCE_COLUMNS = (
    "CSA CCM v4.1", "CSA AICM v1.1", "ISO/IEC 27001:2022", "NIST CSF 2.0",
    "CTPAT", "PIP", "BASC v6", "WCO SAFE", "AEO/AEO-S", "AICPA TSC 2017",
)

# The compliance matrix's own statement that its AICPA TSC 2017 column is
# still being populated, with the condition on that column's N/A (batch 3
# round 4 item 1). The AICPA TSC instrument page says the column is being
# populated only while the matrix carries this sentence, so it is pinned here.
# It may stand only in the reading-guide paragraph: anywhere else in the
# matrix it fails the build (batch 3 follow-up round 2 item 1). A reworded
# status outside the "How to use this matrix" section is not read and does
# not fail the build.
CROSSWALK_TSC_POPULATING = (
    "The AICPA TSC 2017 column is being populated domain by domain; until a "
    "row's Trust Services Criteria mapping has been assessed, its \"N/A\" in "
    "that column records that no mapping has been made yet and does not "
    "assert that no criterion applies."
)

# The compliance matrix's reading-guide paragraph without that sentence (batch
# 3 round 6 item 1). The paragraph is pinned whole: it reads exactly this
# (the column is not being populated) or this, a space, and
# CROSSWALK_TSC_POPULATING (it is), and any other text fails the build, so no
# rewording of the status can pass as either form. It is found by position,
# the last paragraph of the "How to use this matrix" section pinned below,
# never by its own words.
CROSSWALK_TSC_READING_GUIDE = (
    "Read across a row to identify which frameworks a given document "
    "supports. Read down a column to identify which GRC library documents "
    "map or align to a framework's requirements; a mapping does not "
    "establish that those documents satisfy the framework. A cell containing "
    "\"N/A\" indicates no direct mapping; the document may still provide "
    "contextual support. \"N/A\" is used in particular for the customs and "
    "trade-security columns (CTPAT, PIP, BASC, WCO SAFE, AEO/AEO-S) on "
    "documents whose subject is not customs or trade security."
)

# The header of the compliance matrix's framework column key table; the
# matrix carries exactly one table with this header.
CROSSWALK_COMPLIANCE_KEY_HEADER = ("Column", "Framework", "Reference Basis")

# The compliance matrix's "How to use this matrix" section, pinned whole from
# its heading to the --- that ends it (batch 3 follow-up round 2 item 1): the
# heading, a blank line, CROSSWALK_TSC_SECTION_OPENING (the intro and
# representative-citation paragraphs and the framework column key list), a
# blank line, the reading-guide paragraph in one of its two forms, a blank
# line and ---. Any other text in the section fails the build, so the status
# sentence moved or reworded into the intro paragraph, a paragraph of its
# own, or a key table row, old or new, cannot drop the caveat. Editing this
# section of the matrix means editing this pin with it.
CROSSWALK_TSC_SECTION_HEADING = "## How to use this matrix"
CROSSWALK_TSC_SECTION_OPENING = "\n".join((
    "This matrix maps GRC library documents to the control domains and "
    "section references of ten compliance, security, assurance, and "
    "AI-control frameworks. Each row represents one GRC library document. "
    "Each framework column lists the control identifiers, domains, or "
    "section references that the document materially supports.",
    "",
    "**Citations are indicative, not exhaustive (representative-citation "
    "convention).** The identifiers in each framework column are a "
    "REPRESENTATIVE selection that best characterizes how the document "
    "aligns to that framework; they are not an exhaustive reproduction of, "
    "and need not appear verbatim in, the referenced document. A document "
    "commonly expresses its own control coverage at a different granularity "
    "or as a different subset (or carries no same-framework identifiers of "
    "its own at all), so a control named here may be an indicative example "
    "of the domain's applicability rather than a code the document itself "
    "cites. Consequently, an advisory stranded-code scan that compares a "
    "cell against the referenced document's own codes may list a cited "
    "identifier as a \"candidate\"; under this convention that is expected "
    "and is not, by itself, a defect. A cited identifier is still expected "
    "to be a real control of its framework and to materially fit the row's "
    "subject: literal absence from the referenced document is permitted by "
    "this convention, but a fabricated (non-existent) code or a genuine "
    "wrong-fit is not, and the corpus's citation-validity and periodic "
    "semantic-fit checks address those separately (to the extent each "
    "framework column is covered). Where a citation uses a control-family "
    "RANGE (for example a domain's NN-01 through NN-14), the range expresses "
    "broad family coverage and does not assert that every member "
    "individually applies to the row; narrower direct citations elsewhere "
    "identify the strongest specific mappings. A family range is split or "
    "enumerated, however, to exclude any member whose source specification "
    "imposes a cloud provider's duty to its service customers or tenants "
    "where the citing document is internal in scope.",
    "",
    "**Framework column keys:**",
    "",
    "| Column | Framework | Reference Basis |",
    "| --- | --- | --- |",
    "| CSA CCM v4.1 | Cloud Security Alliance Cloud Controls Matrix v4.1 | "
    "Control domain identifiers (e.g., IAM, SEF, DSP) |",
    "| CSA AICM v1.1 | Cloud Security Alliance AI Controls Matrix v1.1, the "
    "AI-focused extension of CCM v4.1 | AI-specific control identifiers only "
    "(the AICM-only delta: the MDS Model Security domain plus the "
    "AI-specific AIS, GRC, DSP, HRS, IAM, LOG, and TVM controls). CCM-base "
    "controls remain in the CSA CCM v4.1 column; this column carries the "
    "AI-specific additions, so it is N/A for documents with no AI dimension |",
    "| ISO/IEC 27001:2022 | ISO/IEC 27001:2022 | Annex A control numbers and "
    "§4 to §10 clauses; ISO/IEC 27002:2022 is the supporting implementation "
    "guidance for the Annex A controls, not a separate column |",
    "| NIST CSF 2.0 | NIST Cybersecurity Framework 2.0 | Category "
    "identifiers (e.g., GV.SC, ID.RA, DE.AE) within the six Core Functions "
    "(GV, ID, PR, DE, RS, RC) |",
    "| CTPAT | C-TPAT | Section headings |",
    "| PIP | Partners in Protection (Canada Border Services Agency) | "
    "Programme requirement areas |",
    "| BASC v6 | BASC (Business Alliance for Secure Commerce): the Norm "
    "V6-2022 (CSMS, §4 to §9.4) and the applicable Security Standard "
    "6.0.2/6.0.3 (§1 to §5) | Clause references; each cell names the "
    "instrument (Norm or Security Standard) so the clause resolves |",
    "| WCO SAFE | WCO SAFE Framework of Standards | Pillar and standard "
    "references |",
    "| AEO/AEO-S | UK HMRC Authorized Economic Operator (Security and "
    "Safety) | Requirement area headings |",
    "| AICPA TSC 2017 | AICPA 2017 Trust Services Criteria (TSP Section "
    "100), the criteria used to evaluate controls in a SOC 2 examination; "
    "the 2022 revision updated the points of focus, not the criteria | "
    "Criterion identifiers only: CC1.1 to CC9.2 (common criteria), A1.1 to "
    "A1.3 (Availability), C1.1 to C1.2 (Confidentiality), PI1.1 to PI1.5 "
    "(Processing Integrity), and P1.1 to P8.1 (Privacy); never a category "
    "name or a privacy group heading such as P1.0 |",
))

# Representative identifiers shown per cell before "and more" (design C 3.3
# caps a cell at roughly six).
CROSSWALK_CELL_ID_CAP = 6

# --check warning threshold (design C 3.5): a taxonomy framework string cited
# by at least this many documents with no alias is surfaced, so a new
# instrument shows up instead of silently vanishing from the crosswalk.
CROSSWALK_ALIAS_WARN_MIN = 10


class Instrument(NamedTuple):
    """One crosswalk instrument: a main-table column and/or an instrument page."""

    key: str                 # URL slug under crosswalk/
    label: str               # short display label (the column header base)
    group: str               # instrument-group band (design C 3.2)
    register_id: str | None  # Standard ID in the citations register; None for
                             # the two programmes the register carries no row
                             # for (PIP and AEO/AEO-S), whose naming source is
                             # the compliance matrix's own column key
    version_join: str | None  # how label + register Current version compose
                             # the display name: "colon", "space", "paren", or
                             # None (a long legal version shows on the
                             # instrument page only)
    compliance_column: str | None  # compliance-matrix column, or None
    reverse_section: str | None    # reverse-matrix section heading, or None
    reverse_filter: tuple | None   # None (all rows) or ("include"|"exclude",
                                   # <area-label prefix>) for the combined
                                   # OWASP LLM Top 10 / MITRE ATLAS section
    main_table: bool         # a column of the main table (19 instruments);
                             # False lists the page under "Also in the corpus"
    reverse_pointer: str | None = None  # key of the instrument whose page
                             # renders the combined reverse matrix section
                             # that names this programme (the CTPAT MSC and
                             # BASC v6 section carries no per-programme rows
                             # to split, so the sibling pages point at it)
    org: str | None = None   # the organization tag under a main-table column
                             # header (spec 7.30: Name<span class="org">);
                             # a display name that opens with it drops it


_XW_G_STANDARDS = "Standards and management systems"
_XW_G_FRAMEWORKS = "Frameworks and control catalogues"
_XW_G_LAWS = "Laws and regulations"
_XW_G_TRADE = "Sector and trade programmes"
_XW_G_AUDIT = "Audit and attestation"
_XW_G_ALSO = "Also in the corpus"

CROSSWALK_GROUPS = (
    _XW_G_STANDARDS, _XW_G_FRAMEWORKS, _XW_G_LAWS, _XW_G_TRADE, _XW_G_AUDIT,
)

# The 19 main-table instruments (the union of the compliance matrix's ten
# columns and the reverse matrix's fifteen scope instruments, design C 3.2),
# plus the register-and-taxonomy-only instrument pages the "Also in the
# corpus" group lists and the topic views link (design C 3.4: COBIT; 3.7:
# the Canadian privacy instruments). Every register_id must resolve in the
# register and every main-table instrument must appear in at least one
# matrix; both are build errors (design C 3.5).
CROSSWALK_INSTRUMENTS = (
    Instrument("iso-iec-27001", "ISO/IEC 27001", _XW_G_STANDARDS,
               "ISO/IEC 27001", "colon", "ISO/IEC 27001:2022",
               "ISO/IEC 27001:2022 Annex A", None, True, org="ISO/IEC"),
    Instrument("iso-iec-42001", "ISO/IEC 42001", _XW_G_STANDARDS,
               "ISO/IEC 42001", "colon", None,
               "ISO/IEC 42001:2023 (AI management systems)", None, True,
               org="ISO/IEC"),
    Instrument("nist-csf", "NIST CSF", _XW_G_FRAMEWORKS,
               "NIST CSF", "space", "NIST CSF 2.0", "NIST CSF 2.0", None, True,
               org="NIST"),
    Instrument("nist-sp-800-53", "NIST SP 800-53", _XW_G_FRAMEWORKS,
               "NIST SP 800-53", "space", None,
               "NIST SP 800-53 Rev. 5 (selected families)", None, True,
               org="NIST"),
    Instrument("nist-ai-rmf", "NIST AI RMF", _XW_G_FRAMEWORKS,
               "NIST AI RMF", "space", None,
               "NIST AI RMF 1.0 (Govern, Map, Measure, Manage)", None, True,
               org="NIST"),
    Instrument("csa-ccm", "CSA CCM", _XW_G_FRAMEWORKS,
               "CSA CCM", "space", "CSA CCM v4.1",
               "CSA CCM v4.1 (selected domains)", None, True, org="CSA"),
    Instrument("csa-aicm", "CSA AICM", _XW_G_FRAMEWORKS,
               "CSA AICM", "space", "CSA AICM v1.1", None, None, True,
               org="CSA"),
    Instrument("owasp-llm-top-10", "OWASP LLM Top 10", _XW_G_FRAMEWORKS,
               "OWASP LLM Top 10", "paren", None,
               "OWASP LLM Top 10 (2026) and MITRE ATLAS",
               ("exclude", "MITRE ATLAS"), True, org="OWASP"),
    Instrument("mitre-atlas", "MITRE ATLAS", _XW_G_FRAMEWORKS,
               "MITRE ATLAS", "space", None,
               "OWASP LLM Top 10 (2026) and MITRE ATLAS",
               ("include", "MITRE ATLAS"), True, org="MITRE"),
    Instrument("eu-ai-act", "EU AI Act", _XW_G_LAWS,
               "EU AI Act", None, None, "EU AI Act", None, True, org="EU"),
    Instrument("gdpr", "GDPR", _XW_G_LAWS,
               "EU GDPR", None, None, "GDPR (and UK GDPR by analogue)",
               None, True, org="EU"),
    Instrument("dora", "DORA", _XW_G_LAWS,
               "EU DORA", None, None, "DORA (Digital Operational Resilience Act)",
               None, True, org="EU"),
    Instrument("nis-2", "NIS 2", _XW_G_LAWS,
               "EU NIS 2 Directive", None, None, "NIS 2 Directive", None, True,
               org="EU"),
    # The trade programmes' organization tags are their authorities as the
    # supply-chain programme alignment matrix's programme summary names them
    # (AEO/AEO-S as the compliance matrix's column key does: UK HMRC).
    Instrument("ctpat", "CTPAT", _XW_G_TRADE,
               "CTPAT MSC", "paren", "CTPAT",
               "CTPAT MSC and BASC v6 (trade and supply-chain security)",
               None, True, org="CBP"),
    Instrument("pip", "PIP", _XW_G_TRADE,
               None, None, "PIP", None, None, True,
               reverse_pointer="ctpat", org="CBSA"),
    Instrument("basc", "BASC", _XW_G_TRADE,
               "BASC International Norm V6-2022 (Control and Security "
               "Management System, CSMS)", "paren", "BASC v6", None, None, True,
               reverse_pointer="ctpat", org="WBO"),
    Instrument("wco-safe", "WCO SAFE", _XW_G_TRADE,
               "WCO SAFE Framework", "paren", "WCO SAFE", None, None, True,
               reverse_pointer="ctpat", org="WCO"),
    Instrument("aeo", "AEO/AEO-S", _XW_G_TRADE,
               None, None, "AEO/AEO-S", None, None, True,
               reverse_pointer="ctpat", org="HMRC"),
    Instrument("aicpa-tsc", "AICPA TSC", _XW_G_AUDIT,
               "AICPA TSP Section 100", None, "AICPA TSC 2017", None, None, True,
               org="AICPA"),
    # Register-and-taxonomy-only instrument pages (no matrix backing, so no
    # main-table column until a matrix carries them, design C 3.2 and 3.4).
    Instrument("cobit", "COBIT", _XW_G_ALSO,
               "COBIT", "space", None, None, None, False),
    Instrument("pipeda", "PIPEDA", _XW_G_ALSO,
               "Canada PIPEDA", None, None, None, None, False),
    Instrument("quebec-law-25", "Quebec Law 25", _XW_G_ALSO,
               "Quebec Law 25", None, None, None, None, False),
)

CROSSWALK_BY_KEY = {inst.key: inst for inst in CROSSWALK_INSTRUMENTS}

# The committed alias map (design C 3.5, the one new data artefact): exact
# taxonomy framework strings -> instrument key. The taxonomy extraction is
# unnormalized free text, so only exact spellings are aliased; high-frequency
# strings with no alias surface as a --check warning rather than silently
# vanishing. An alias naming no configured instrument, or an instrument whose
# register_id resolves to no register row, is a build error. A spelling on a
# concern page that cites an instrument by one of its clauses, articles or
# control identifiers names that instrument and is aliased too (integration
# round 2 ERROR: the concern pages showed such names as plain text beside a
# linked short form); elsewhere in the taxonomy such spellings are not all
# aliased yet (for example "COBIT 2019 DSS05"), and an unaliased spelling
# counts toward no instrument. Guidance, a profile, or a regulation made
# under an instrument is a separate text and is not aliased.
CROSSWALK_ALIASES = {
    "ISO/IEC 27001:2022": "iso-iec-27001",
    "ISO/IEC 27001:2022 Annex A.5.24 to A.5.28": "iso-iec-27001",
    "ISO/IEC 42001:2023": "iso-iec-42001",
    "ISO/IEC 42001:2023 A.8.4 (Communication of incidents)": "iso-iec-42001",
    "ISO/IEC 42001:2023 §7.5.3": "iso-iec-42001",
    "NIST CSF 2.0": "nist-csf",
    "NIST Cybersecurity Framework 2.0": "nist-csf",
    "NIST SP 800-53 Rev. 5": "nist-sp-800-53",
    "NIST SP 800-53 Rev. 5 CA": "nist-sp-800-53",
    "NIST AI RMF 1.0": "nist-ai-rmf",
    "NIST AI RMF 1.0 (2023)": "nist-ai-rmf",
    "NIST AI RMF 1.0 (NIST AI 100-1)": "nist-ai-rmf",
    "NIST AI RMF 1.0 MANAGE 4.3": "nist-ai-rmf",
    "NIST AI 100-1 (AI RMF 1.0)": "nist-ai-rmf",
    "CSA CCM v4.1": "csa-ccm",
    "CSA CCM v4.1.0": "csa-ccm",
    "CSA CCM": "csa-ccm",
    "CSA CCM v4.1 DSP-02": "csa-ccm",
    "CSA CCM v4.1 DSP-09": "csa-ccm",
    "CSA CCM v4.1 DSP-10": "csa-ccm",
    "CSA CCM v4.1 DSP-16": "csa-ccm",
    "CSA CCM v4.1 Data Security and Privacy Lifecycle Management (DSP) "
    "domain": "csa-ccm",
    "CSA CCM v4.1 SEF-03, SEF-07, SEF-08, SEF-09": "csa-ccm",
    "CSA CCM v4.1 SEF-06": "csa-ccm",
    "CSA CCM v4.1 SEF-08, SEF-03": "csa-ccm",
    "CSA Cloud Controls Matrix": "csa-ccm",
    "CSA Cloud Controls Matrix v4.1": "csa-ccm",
    "CSA AICM v1.1": "csa-aicm",
    "CSA AICM v1.1.0": "csa-aicm",
    "CSA AICM": "csa-aicm",
    "OWASP LLM Top 10": "owasp-llm-top-10",
    "OWASP LLM Top 10 (2026)": "owasp-llm-top-10",
    "MITRE ATLAS": "mitre-atlas",
    "MITRE ATLAS (2026.07)": "mitre-atlas",
    "EU AI Act": "eu-ai-act",
    "EU AI Act (2024)": "eu-ai-act",
    "EU AI Act (Regulation (EU) 2024/1689)": "eu-ai-act",
    "EU AI Act (Regulation (EU) 2024/1689 as amended by Regulation (EU) "
    "2026/1744)": "eu-ai-act",
    "EU AI Act Annex IV": "eu-ai-act",
    "GDPR": "gdpr",
    "EU GDPR": "gdpr",
    "EU GDPR (Regulation (EU) 2016/679)": "gdpr",
    "GDPR (EU)": "gdpr",
    "GDPR (2018)": "gdpr",
    "UK GDPR": "gdpr",
    "GDPR / UK GDPR": "gdpr",
    "GDPR (EU) / UK GDPR": "gdpr",
    "GDPR (Regulation (EU) 2016/679)": "gdpr",
    "GDPR Art. 34(3)(a)": "gdpr",
    "GDPR Article 35": "gdpr",
    "GDPR Articles 33 to 34": "gdpr",
    "GDPR Arts. 33 to 34 (Art. 33(1) notification to the supervisory "
    "authority; Art. 34(1) communication to the data subject)": "gdpr",
    "UK GDPR (consolidated text retrieved 29 September 2026)": "gdpr",
    "UK GDPR Articles 33 to 34 (consolidated text retrieved 29 September "
    "2026)": "gdpr",
    "UK GDPR Arts. 33 to 34": "gdpr",
    "DORA": "dora",
    "DORA (Regulation (EU) 2022/2554, 14 December 2022)": "dora",
    "DORA Articles 17 and 19": "dora",
    "NIS 2": "nis-2",
    "NIS 2 Article 23": "nis-2",
    "NIS2": "nis-2",
    "EU NIS 2": "nis-2",
    "EU NIS 2 Directive": "nis-2",
    "EU NIS 2 Directive (Directive (EU) 2022/2555)": "nis-2",
    "NIS 2 Directive": "nis-2",
    "CTPAT": "ctpat",
    "CTPAT Minimum Security Criteria": "ctpat",
    "Canada PIP": "pip",
    "BASC v6 (2022)": "basc",
    "BASC International Norm V6-2022": "basc",
    "BASC International Standard v6": "basc",
    "BASC International Security Standard 6.0.2/6.0.3": "basc",
    "BASC International Security Standard 6.0.2/6.0.3 (2022)": "basc",
    "WCO SAFE Framework": "wco-safe",
    "WCO SAFE Framework (2025 edition)": "wco-safe",
    "AEO-S (UK)": "aeo",
    "AEO-S IT Control Requirements": "aeo",
    "COBIT 2019": "cobit",
    "COBIT 2019 APO14.09, DSS01": "cobit",
    "COBIT 2019 MEA01": "cobit",
    "PIPEDA": "pipeda",
    "Canada PIPEDA": "pipeda",
    "PIPEDA (Canada)": "pipeda",
    "PIPEDA (Canada Personal Information Protection and Electronic "
    "Documents Act)": "pipeda",
    "Quebec Law 25": "quebec-law-25",
    "Quebec Law 25 (S.Q. 2021, c. 25)": "quebec-law-25",
    "Quebec Law 25 (CQLR c. P-39.1) sections 3.3 and 12.1 (private "
    "sector)": "quebec-law-25",
    "Quebec CQLR c. P-39.1, as amended by Law 25 (consolidated text updated "
    "to 1 April 2026)": "quebec-law-25",
}

# Exact taxonomy framework strings that join several texts with " / ": each
# part, in order, with the instrument it names, or None for a part naming a
# text that is no crosswalk instrument (integration round 3 WARN: the Data
# Protection Act 2018 and ISO/IEC 27002 linked whole to the UK GDPR and
# ISO/IEC 27001 pages). The parts rejoined with " / " must give the string
# back, every key must name a configured instrument, at least one part must
# name one, and no string may also sit in CROSSWALK_ALIASES (build errors),
# so a chip links each instrument it names and nothing it does not.
CROSSWALK_ALIAS_PARTS = {
    "CSA CCM v4.1 / AICM v1.1": (
        ("CSA CCM v4.1", "csa-ccm"), ("AICM v1.1", "csa-aicm")),
    "CTPAT / PIP / BASC": (
        ("CTPAT", "ctpat"), ("PIP", "pip"), ("BASC", "basc")),
    "ISO/IEC 27001:2022 / ISO/IEC 27002:2022": (
        ("ISO/IEC 27001:2022", "iso-iec-27001"), ("ISO/IEC 27002:2022", None)),
    "PIPEDA / Quebec Law 25": (
        ("PIPEDA", "pipeda"), ("Quebec Law 25", "quebec-law-25")),
    "UK GDPR / Data Protection Act 2018": (
        ("UK GDPR", "gdpr"), ("Data Protection Act 2018", None)),
}


def crosswalk_alias_keys(name):
    """The instrument keys one exact taxonomy framework string names through
    the committed alias maps, in order; empty for a string neither carries.
    A compound's plain-text parts (key None) name no instrument."""
    if name in CROSSWALK_ALIASES:
        return (CROSSWALK_ALIASES[name],)
    return tuple(key for _, key in CROSSWALK_ALIAS_PARTS.get(name, ())
                 if key is not None)


class CrosswalkPreset(NamedTuple):
    """One topic view (design C 3.7): a matrix.js preset on the crosswalk
    page (spec 7.30) and its static view at crosswalk/view/<slug>/, the page
    the preset link resolves to without script (design C 3.8)."""

    slug: str
    label: str
    columns: tuple    # instrument keys whose columns the view renders
    related: tuple    # instrument-page keys linked beneath the view's table


# The topic views of design C 3.7 (maintainer decision 2026-11-03 18:53Z:
# the views stay by topic). A topic may take columns from several instrument
# groups, and one column may sit in several topics.
CROSSWALK_TOPICS = (
    CrosswalkPreset("security", "Security",
                    ("iso-iec-27001", "nist-csf", "nist-sp-800-53", "csa-ccm",
                     "aicpa-tsc"), ()),
    CrosswalkPreset("ai", "AI",
                    ("iso-iec-42001", "nist-ai-rmf", "csa-aicm", "eu-ai-act",
                     "owasp-llm-top-10", "mitre-atlas"), ()),
    CrosswalkPreset("privacy", "Privacy and data protection",
                    ("gdpr", "eu-ai-act", "nis-2"),
                    ("pipeda", "quebec-law-25")),
    CrosswalkPreset("resilience", "Resilience and financial services",
                    ("dora", "nis-2", "csa-ccm"), ()),
    CrosswalkPreset("trade", "Trade and customs",
                    ("ctpat", "pip", "basc", "wco-safe", "aeo"), ()),
    CrosswalkPreset("canada", "Canada",
                    ("pip",), ("pipeda", "quebec-law-25")),
)


# The groups the crosswalk's side list shows, in page order: every column
# group, then the instruments with a page and no column.
CROSSWALK_RAIL_GROUPS = CROSSWALK_GROUPS + (_XW_G_ALSO,)

# The All preset's id (spec 7.30 data-preset-id); a topic taking it would
# make ?view=all name two views, so crosswalk_presets refuses it.
CROSSWALK_ALL_ID = "all"


def crosswalk_presets(instruments=None, topics=None):
    """The column presets: the topic views, validated against the
    instruments and their side-list groups. Loud when they disagree: an
    instrument outside every side-list group would vanish from the side list,
    a main-table instrument under "Also in the corpus" (or a page-only one
    under a column group) would be listed as what it is not, a topic naming
    an unknown instrument or a page-only one as a column would render a
    column the table has not, a topic with no column would be a view showing
    nothing, a related key naming no instrument page would be a dead link,
    and a main-table instrument in no topic would be reachable only through
    All. A main-table instrument with no organization tag would render a
    column header short of its spec 7.30 markup; a repeated topic slug would
    give two views one route and one preset id, a topic slug "all" would
    take the All preset's id, and a column repeated within a topic would
    render twice in its view. Called from build_crosswalk, never at import,
    so a refusal reports as a generator failure and an importer of this
    module does not break."""
    instruments = CROSSWALK_INSTRUMENTS if instruments is None else instruments
    topics = CROSSWALK_TOPICS if topics is None else topics
    for inst in instruments:
        if inst.group not in CROSSWALK_RAIL_GROUPS:
            raise BuildError(
                f"crosswalk: instrument '{inst.key}' names group "
                f"'{inst.group}', which is no crosswalk group"
            )
        if inst.main_table != (inst.group in CROSSWALK_GROUPS):
            raise BuildError(
                f"crosswalk: instrument '{inst.key}' in group '{inst.group}' "
                + ("has a main-table column, so it belongs to a column group"
                   if inst.main_table else
                   "has no main-table column, so it belongs to "
                   f"'{_XW_G_ALSO}'")
            )
        if inst.main_table and not inst.org:
            raise BuildError(
                f"crosswalk: main-table instrument '{inst.key}' has no "
                "organization tag for its column header"
            )
    by_key = {inst.key: inst for inst in instruments}
    slugs = set()
    for topic in topics:
        if topic.slug == CROSSWALK_ALL_ID:
            raise BuildError(
                f"crosswalk: topic slug '{topic.slug}' is the All view's "
                "preset id"
            )
        if topic.slug in slugs:
            raise BuildError(
                f"crosswalk: duplicate topic slug '{topic.slug}', so two "
                "views would share one route and one preset id"
            )
        slugs.add(topic.slug)
        if not topic.columns:
            raise BuildError(
                f"crosswalk: topic '{topic.slug}' has no column, so its view "
                "would show nothing"
            )
        for key in topic.columns:
            if topic.columns.count(key) > 1:
                raise BuildError(
                    f"crosswalk: topic '{topic.slug}' names column '{key}' "
                    "more than once"
                )
            if key not in by_key:
                raise BuildError(
                    f"crosswalk: topic '{topic.slug}' names instrument "
                    f"'{key}', which is no crosswalk instrument"
                )
            if not by_key[key].main_table:
                raise BuildError(
                    f"crosswalk: topic '{topic.slug}' names '{key}' as a "
                    "column, but it has no main-table column"
                )
        for key in topic.related:
            if key not in by_key:
                raise BuildError(
                    f"crosswalk: topic '{topic.slug}' relates instrument "
                    f"'{key}', which is no crosswalk instrument"
                )
    covered = {key for topic in topics for key in topic.columns}
    for inst in instruments:
        if inst.main_table and inst.key not in covered:
            raise BuildError(
                f"crosswalk: instrument '{inst.key}' has a main-table column "
                "in no topic, so only All would show it"
            )
    return tuple(topics)


# The draft refusal guard (spec section 12: a generator refuses to write a
# page that contains an en or em dash (literal or entity-encoded), an inline
# style or script, an on* attribute, or "what this is" framing). Scoped to
# draft pages because the live v1/v2/v3 partials deliberately carry an inline
# <style> and <script>.
_DRAFT_REFUSALS = (
    ("an en dash", re.compile("–")),
    ("an em dash", re.compile("—")),
    ("an inline style element", re.compile(r"<style\b", re.I)),
    ("an inline script element", re.compile(r"<script\b(?![^>]*\bsrc=)", re.I)),
    ("a style attribute", re.compile(r"\sstyle\s*=", re.I)),
    ("an on* event attribute", re.compile(r"\son[a-z]+\s*=", re.I)),
    ('"what this is" framing', re.compile(r"what this is", re.I)),
)


def refuse_draft_page(out_rel, html):
    """Raise BuildError when a rendered draft page breaks a refusal rule."""
    for what, pattern in _DRAFT_REFUSALS:
        if pattern.search(html):
            raise BuildError(f"draft refusal guard: {out_rel} contains {what}")
    # Round-3 WARN: an exact spelling list missed valid entity forms (no
    # trailing semicolon, leading zeros, the Windows-1252 code points), each
    # of which a browser decodes to a dash. Decode once and scan for the
    # literal characters instead, so every spelling that renders as a dash is
    # refused, while text that only shows a spelling (an escaped ampersand
    # form such as "&amp;ndash;") still passes.
    decoded = html_unescape(html)
    if "\u2013" in decoded:
        raise BuildError(
            f"draft refusal guard: {out_rel} contains an encoded en dash"
        )
    if "\u2014" in decoded:
        raise BuildError(
            f"draft refusal guard: {out_rel} contains an encoded em dash"
        )


def read_baseline_pin(pin_path=None):
    """Read ``.baseline/pin.toml`` (stdlib ``tomllib``) and return
    ``(version, files)``. BuildError on a missing or malformed pin, so the
    asset copy and the licence page's template version (spec section 11:
    grclibrary.ai templates carry no hard-coded versions) both come from the
    one checked pin. The parameter exists for the test fixtures."""
    import tomllib
    pin_path = (
        Path(pin_path) if pin_path is not None
        else REPO_ROOT / ".baseline" / "pin.toml"
    )
    if not pin_path.is_file():
        raise BuildError(f"baseline pin: pin file not found at {pin_path}")
    try:
        pin = tomllib.loads(pin_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise BuildError(f"baseline pin: malformed pin {pin_path}: {exc}")
    version = pin.get("version")
    files = pin.get("files")
    if not isinstance(version, str) or not version \
            or not isinstance(files, dict) or not files:
        raise BuildError(
            f"baseline pin: {pin_path} needs a version string and a "
            "non-empty [files] table"
        )
    return version, files


def load_baseline_assets(baseline_dir=None, pin_path=None):
    """Read every pinned baseline runtime file as bytes for the draft asset
    copy, verifying each against ``.baseline/pin.toml`` (read_baseline_pin).

    Returns ``[(rel-under-assets/baseline/, bytes), ...]``. BuildError on a
    missing or malformed pin, a pin key outside ``.web/baseline/``, a pinned
    file missing, a SHA-256 mismatch, or an unpinned file present, so a
    tampered or drifted copy can never deploy. The parameters exist for the
    test fixtures; a build always uses the repository paths."""
    import hashlib
    baseline_dir = (
        Path(baseline_dir) if baseline_dir is not None else WEB_DIR / "baseline"
    )
    pin_path = (
        Path(pin_path) if pin_path is not None
        else REPO_ROOT / ".baseline" / "pin.toml"
    )
    _, files = read_baseline_pin(pin_path)
    prefix = ".web/baseline/"
    assets = []
    pinned = set()
    for key in sorted(files):
        digest = files[key]
        if key == PALETTE_GATE_KEY:
            # Pinned beside the copies but never served; run_palette_gate
            # verifies and runs it.
            continue
        if not key.startswith(prefix) or not isinstance(digest, str):
            raise BuildError(
                f"draft asset copy: pin entry outside {prefix} or with a "
                f"non-string digest: {key}"
            )
        rel = key[len(prefix):]
        pinned.add(rel)
        source = baseline_dir / rel
        if not source.is_file():
            raise BuildError(
                f"draft asset copy: pinned file missing from {baseline_dir}: {rel}"
            )
        data = source.read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise BuildError(
                f"draft asset copy: {rel} does not match its pinned SHA-256 "
                f"in {pin_path}"
            )
        assets.append((rel, data))
    on_disk = {
        p.relative_to(baseline_dir).as_posix()
        for p in baseline_dir.rglob("*") if p.is_file()
    }
    unpinned = sorted(on_disk - pinned)
    if unpinned:
        raise BuildError(
            f"draft asset copy: unpinned file(s) under {baseline_dir}: "
            + ", ".join(unpinned)
        )
    return assets


# The palette gate (baseline 1.7.0 SPECIFICATION.md section 4 items 2 and 3):
# the package's tools/check_palette.py, copied to .baseline/check_palette.py
# and pinned in .baseline/pin.toml beside the served copies, never served.
# Every draft build runs it on the served palettes.css (the pin-verified
# source of draft/assets/baseline/palettes.css) for this site, so a palette
# that misses a contrast threshold fails the build, --check included (CI and
# the pre-push guard run --check). The site has no site-palette.css (the
# owner has asked for none), so the gate runs without --site-palette.
PALETTE_GATE_KEY = ".baseline/check_palette.py"
PALETTE_SITE = "grclibrary"
PALETTE_CSS = WEB_DIR / "baseline" / "palettes.css"


def run_palette_gate(palettes=None, gate=None, pin_path=None):
    """Verify the palette gate against the pin, then run it on ``palettes``
    (default ``PALETTE_CSS``). BuildError when the pin has no entry for the
    gate, the gate is missing, is not a regular file by ``lstat`` (a symbolic
    link is refused, never followed) or differs from its pinned SHA-256, or
    the gate exits non-zero (a failing pairing, or input it cannot read).
    What runs is a private temporary copy of exactly the bytes that were
    hashed, removed afterwards, so the gate path cannot change between the
    hash and the run. The parameters exist for the test fixtures; a build
    always uses the repository paths."""
    import hashlib
    import stat
    import tempfile
    palettes = Path(palettes) if palettes is not None else PALETTE_CSS
    gate = Path(gate) if gate is not None else REPO_ROOT / PALETTE_GATE_KEY
    _, files = read_baseline_pin(pin_path)
    digest = files.get(PALETTE_GATE_KEY)
    if not isinstance(digest, str):
        raise BuildError(
            f"palette gate: {PALETTE_GATE_KEY} has no pin entry in "
            f"{pin_path or '.baseline/pin.toml'} (spec section 4 item 3 "
            "pins it)"
        )
    try:
        mode = gate.lstat().st_mode
    except FileNotFoundError:
        raise BuildError(f"palette gate: {gate} is missing") from None
    if not stat.S_ISREG(mode):
        raise BuildError(
            f"palette gate: {gate} is not a regular file (a symbolic link "
            "or other entry, refused by lstat), so it is not run"
        )
    data = gate.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise BuildError(
            f"palette gate: {gate} does not match its pinned SHA-256, so it "
            "is not run"
        )
    with tempfile.TemporaryDirectory(prefix="palette-gate-") as private:
        copy = Path(private) / gate.name
        copy.write_bytes(data)
        try:
            result = subprocess.run(
                [sys.executable, "-I", str(copy), "--site", PALETTE_SITE,
                 "--palettes", str(palettes)],
                capture_output=True, text=True, timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired) as e:
            raise BuildError(
                f"palette gate: could not run {gate}: {e}") from None
    if result.returncode != 0:
        # The scheme headers, every failing row or check, and the verdict.
        failures = [
            " ".join(line.split()) for line in result.stdout.splitlines()
            if "FAIL" in line or line.startswith(("==", "ERROR", "RESULT"))
        ]
        raise BuildError(
            f"palette gate: {PALETTE_GATE_KEY} --site {PALETTE_SITE} "
            f"--palettes {palettes} exited {result.returncode}: "
            + "; ".join(failures or [result.stderr.strip()])
        )


def _draft_nav(current=None):
    """The topbar partial's per-page current-page markers. Each bar link
    opens its own page (maintainer decision 2026-11-03 23:27Z), and a page
    marks the link of the section it belongs to: the need, domain and type
    pages under Browse, every document page under All Documents, the decide
    hub, concern, subtype index and reading-room pages under Decisions, and
    the crosswalk views and instrument pages under Crosswalk. The landing,
    disclosure, licence and 404 pages belong to no bar section."""
    return {
        "NAV_BROWSE": ' aria-current="page"' if current == "browse" else "",
        "NAV_DOCUMENTS":
            ' aria-current="page"' if current == "documents" else "",
        "NAV_DECISIONS":
            ' aria-current="page"' if current == "decisions" else "",
        "NAV_CROSSWALK":
            ' aria-current="page"' if current == "crosswalk" else "",
        "NAV_SEARCH": ' aria-current="page"' if current == "search" else "",
    }


def _draft_domain_page(figures, domain):
    for dp in figures["domain_pages"]:
        if dp["domain"] == domain:
            return dp
    raise BuildError(
        f"draft: domain '{domain}' has no generated domain page "
        "(renamed in the taxonomy?)"
    )


def _draft_type_entry(figures, type_name):
    for tp in figures["type_pages"]:
        if tp["type"] == type_name:
            return tp
    raise BuildError(
        f"draft: the adventure names document type '{type_name}' which the "
        "taxonomy does not carry (renamed?)"
    )


def _draft_concern_entry(concerns, slug):
    for concern in concerns:
        if concern["slug"] == slug:
            return concern
    raise BuildError(
        f"draft: the adventure names concern '{slug}' which DRAFT_CONCERNS "
        "does not carry (renamed?)"
    )


def _draft_doc_or_source_link(docs_by_path, path, label):
    """A link to one repository artefact: its draft document page where the
    given page lookup carries it outside the root domain (the taxonomy
    documents, plus the docs/ adopter documents when the caller passes the
    merged lookup render_draft_variant builds), else its GitHub source in
    the draft's external-link form (design D gap G1: the adopter docs/
    artefacts are outside taxonomy.yml). Either way the file must exist in
    the repository, so a renamed artefact fails the build instead of
    publishing a dead link."""
    doc = docs_by_path.get(path)
    if doc is not None and doc.get("domain") != ROOT_DOMAIN:
        return (
            f'<a href="{_esc(_doc_page_url("{{BASE}}", path))}">'
            f"{_esc(label)}</a>"
        )
    if not (REPO_ROOT / path).is_file():
        raise BuildError(
            f"draft: adventure artefact {path} is not in the repository "
            "(renamed or removed?)"
        )
    return (
        f'<a href="{_esc(GITHUB_BLOB_BASE + path)}" target="_blank" '
        f'rel="noopener noreferrer">{_esc(label)}{_DRAFT_NEW_TAB}</a>'
    )


def _draft_series(items):
    """A prose series with the serial comma: "a", "a and b", "a, b, and c"."""
    items = list(items)
    if len(items) <= 2:
        return " and ".join(items)
    return ", ".join(items[:-1]) + ", and " + items[-1]


def draft_landing_values(figures):
    gov = _draft_domain_page(figures, DRAFT_EXAMPLE_DOMAIN)
    return {
        **_draft_nav(),
        "GOV_COUNT": str(gov["count"]),
        "NEED_COUNT": str(len(DRAFT_NEEDS)),
        "XW_INSTRUMENT_COUNT": str(
            len([i for i in CROSSWALK_INSTRUMENTS if i.main_table])
        ),
        "EXAMPLE_DOC_URL": _doc_page_url("{{BASE}}", DRAFT_EXAMPLE_DOC),
    }


def draft_browse_values(figures, adopter_docs):
    needs = "\n".join(
        f'<li><a href="{href}"><span class="t">{_esc(title)}</span>'
        f'<span class="n">{_esc(tag)}</span>'
        f'<span class="d">{_esc(line)}</span></a></li>'
        for title, tag, href, line in DRAFT_NEEDS
    )
    domains = "\n".join(
        f'<li><a href="{{{{BASE}}}}/{_esc(domain)}/">'
        f'{_esc(draft_domain_label(domain))}</a>'
        f'<span class="n">{count}</span>'
        f'<small>{_esc(DOMAIN_SCOPE[domain])}</small></li>'
        for domain, count in figures["domains"]
    )
    types = "\n".join(
        f'<li><a href="{{{{BASE}}}}/types/{type_slug(type_name)}/">'
        f'{_esc(type_name)}</a>'
        f'<span class="n">{count}</span></li>'
        for type_name, count in figures["types"]
    )
    guides = "\n".join(
        f'<li><a href="{_esc(_doc_page_url("{{BASE}}", g["path"]))}">'
        f'{_esc(g["title"])}</a>'
        f'<span class="n">{_esc(g["type"].lower())}</span>'
        f'<small>{_esc(g["date"])}</small></li>'
        for g in adopter_docs
    )
    # The type counts here are corpus counts while the search page's list
    # carries the adopter documents too (site a9 round-3 WARN 1), so this
    # line states each scope from the same figures and both pools read true
    # where shown and where they lead.
    total, root = figures["total"], figures["root_count"]
    n_guides = len(adopter_docs)
    type_scope = (
        f"Each count covers the {total} corpus "
        f"{'document' if total == 1 else 'documents'}, the {root} library "
        f"{'specification' if root == 1 else 'specifications'} included; "
        f"the {n_guides} adopter "
        f"{'document' if n_guides == 1 else 'documents'} listed below "
        f"{'is' if n_guides == 1 else 'are'} not counted here. The "
        "search page's list adds the adopter documents and leaves out the "
        "library specifications."
    )
    # A full sentence, singular for one file, naming the metadata block each
    # entry is read from (round-3 note 4).
    if n_guides == 1:
        guide_intro = (
            f"The {n_guides} adopter document under docs/ is listed here. Its "
            "entry is read from the leading metadata block of its file, so "
            "the list follows the repository at every build."
        )
    else:
        guide_intro = (
            f"The {n_guides} adopter documents under docs/ are listed here. "
            "Each entry is read from the leading metadata block of its file, "
            "so the list follows the repository at every build."
        )
    first_domain, _ = figures["domains"][0]
    # The executive path block (design D section 3): the hub link plus one
    # chip per narrative kind, each count generated from the registry, the
    # decide hub's kinds branch in Browse form.
    exec_kinds = "\n".join(
        f'<li><a href="{_draft_subtype_url(narrative_type)}">{_esc(label)}</a>'
        f'<span class="n">'
        f'{sum(1 for p in figures["narratives"] if p["narrative_type"] == narrative_type)}'
        f"</span></li>"
        for narrative_type, (_, label, _) in DRAFT_NARRATIVE_SUBTYPES.items()
    )
    return {
        **_draft_nav("browse"),
        "NEED_ENTRIES": needs,
        "EXEC_CONCERN_COUNT": str(len(DRAFT_CONCERNS)),
        "EXEC_PAGE_COUNT": str(len(figures["narratives"])),
        "EXEC_KIND_COUNT": str(len(DRAFT_NARRATIVE_SUBTYPES)),
        "EXEC_KINDS": exec_kinds,
        "DOMAIN_PLAN": domains,
        "TYPE_SCOPE_LINE": type_scope,
        "TYPE_PLAN": types,
        "GUIDE_PLAN": guides,
        "GUIDE_INTRO": guide_intro,
        "ADOPTER_AREA_LABEL": _esc(draft_domain_label(ADOPTER_DOCS_AREA)),
        "XW_INSTRUMENT_COUNT": str(
            len([i for i in CROSSWALK_INSTRUMENTS if i.main_table])
        ),
        "NEXT_DOMAIN_URL": "{{BASE}}/" + first_domain + "/",
        "NEXT_DOMAIN_LABEL": _esc(draft_domain_label(first_domain)),
    }


# A facet value search.js can match (spec 7.29): a row's data-<group> is a
# space-separated token list compared in lowercase, so a value is one
# lowercase token; anything else would silently match nothing.
_DRAFT_FACET_VALUE_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def _draft_facet_value(value):
    if not _DRAFT_FACET_VALUE_RE.match(value):
        raise BuildError(
            f"draft: facet value {value!r} is not one lowercase token "
            "(letters, digits, hyphens), so no chip could match it"
        )
    return value


def _draft_facet_chips(group, counts, label_of, total):
    """One All Documents chip group (spec 7.29): the All chip, then one chip
    per value in label order, each counting the rows that carry its token.
    Every chip is a plain link to its facet address on the index, which
    search.js reads on load (?<group>=<value>)."""
    chips = [
        f'<li><a href="{{{{BASE}}}}/documents/" data-filter="">All'
        f'<span class="n">{total}</span></a></li>'
    ]
    for value in sorted(counts, key=lambda v: (label_of(v).lower(), v)):
        value = _draft_facet_value(value)
        chips.append(
            f'<li><a href="{{{{BASE}}}}/documents/?{group}={_esc(value)}" '
            f'data-filter="{_esc(value)}">{_esc(label_of(value))}'
            f'<span class="n">{counts[value]}</span></a></li>'
        )
    return "\n".join(chips)


def _draft_search_url(query):
    """The search page's address with ``query`` in ?q=, which search.js
    reads on load (spec 7.29), so a link can open a search already run."""
    return "{{BASE}}/search/?" + urllib.parse.urlencode({"q": query})


def _draft_search_row(d, facets=False):
    """One document row for a search.js scope (the search page and the
    documents index): the title links the on-site page, the annotation names
    the type and area, the small line carries the date. With ``facets`` the
    row also carries the All Documents facet tokens (spec 7.29: data-<group>
    per chip group), its type slug and its area slug."""
    label = draft_domain_label(d.get("domain", ""))
    # Every corpus document gets a row, and its data-search text carries the
    # title, type, area, the full purpose, and the framework names, with
    # whitespace collapsed, so a query matches everything the page says it
    # matches (round-1 defects: a 36-row cap left most queries empty, and a
    # 200-character purpose cut lost matches for the page's own examples).
    haystack = " ".join(" ".join(
        [d.get("title", ""), d.get("type", ""), label,
         d.get("domain", ""), d.get("purpose", "") or ""]
        + d.get("frameworks", [])
    ).lower().split())
    tokens = ""
    if facets:
        doc_type = _draft_facet_value(type_slug(d.get("type", "")))
        area = _draft_facet_value(d.get("domain", ""))
        tokens = f' data-type="{_esc(doc_type)}" data-area="{_esc(area)}"'
    return (
        f'<li data-search="{_esc(haystack)}"{tokens}>'
        f'<a href="{_esc(_doc_page_url("{{BASE}}", d["path"]))}">'
        f'{_esc(d.get("title", d["path"]))}</a>'
        f'<span class="n">{_esc(d.get("type", "").lower())}, {_esc(label)}</span>'
        f'<small>{_esc(d.get("date", ""))}</small></li>'
    )


def draft_search_values(full_docs, adopter_docs):
    # The search page is just a search (maintainer, 2026-11-03 14:29Z): the
    # type and area chips and the "Recently updated" framing duplicated
    # Browse and are gone; the full list stays as search.js's scope and as
    # the page's content without script. Every corpus domain document and
    # every docs/ adopter document gets a row (site a9), one dated pool. The
    # scope runs in results mode (spec 7.29): with script no row shows until
    # the reader types, so no sentence may say the rows are listed below,
    # and the status prompt, generated from the same rows, says how to
    # search.
    pool = sorted(
        [d for d in full_docs if d.get("domain") != ROOT_DOMAIN]
        + list(adopter_docs),
        key=lambda d: (d.get("title", "").lower(), d["path"]),
    )
    pool.sort(key=lambda d: d.get("date", ""), reverse=True)
    rows = [_draft_search_row(d) for d in pool]
    # The prompt names its pool (the library also holds the root
    # specifications, which have no row) and states a field plainly only when
    # every row carries it; a purpose only some rows state is qualified with
    # the generated count of rows that do. Frameworks are never counted: a
    # raw taxonomy frameworks list can hold extraction fragments rather than
    # frameworks (review round 2 WARN), so the clause is qualified in words
    # and stays true however that data stands. Browse calls the groupings
    # domains, so the prompt does too (review round 2 NOTE); with the adopter
    # documents in the pool (site a9) the docs/ area is no domain, so the
    # prompt counts the two pools apart and the field is the row's area.
    n_adopter = len(adopter_docs)
    noun = "document" if len(rows) == 1 else "documents"
    domains = len({d.get("domain", "") for d in pool
                   if d.get("domain") != ADOPTER_DOCS_AREA})
    domain_noun = "domain" if domains == 1 else "domains"
    with_purpose = sum(1 for d in pool if (d.get("purpose") or "").strip())
    fields = ["title", "type", "area" if n_adopter else "domain"]
    clauses = []
    if with_purpose == len(rows):
        fields.append("purpose")
    elif with_purpose:
        verb = "states" if with_purpose == 1 else "state"
        clauses.append(f"by purpose for the {with_purpose} that {verb} one")
    if any(d.get("frameworks") for d in pool):
        clauses.append("by the frameworks a document maps to, where it has any")
    clauses.insert(0, "by " + ", ".join(fields[:-1]) + ", and " + fields[-1])
    if len(clauses) > 1:
        clauses[-1] = "and " + clauses[-1]
    if n_adopter:
        corpus_rows = len(rows) - n_adopter
        corpus_noun = "document" if corpus_rows == 1 else "documents"
        adopter_noun = "document" if n_adopter == 1 else "documents"
        head = (
            f"Search the {len(rows)} {noun}, the {corpus_rows} "
            f"corpus {corpus_noun} across the {domains} {domain_noun} and "
            f"the {n_adopter} adopter {adopter_noun} under docs/, "
        )
    else:
        head = f"Search the {len(rows)} {noun} across the {domains} {domain_noun} "
    return {
        **_draft_nav("search"),
        "SEARCH_PROMPT": head + ", ".join(clauses) + ".",
        # The status prompt names the fields a row's data-search text holds,
        # never the whole document (round-1 NOTE: "it holds every word" read
        # as full text, which only GitHub searches); purpose and frameworks
        # are qualified, as the prompt above qualifies them.
        "SEARCH_STATUS_PROMPT": (
            f"Type one or more words to search the {len(rows)} {noun}; a "
            "document shows when every word is in its title, type, area, "
            "or, where it has them, its purpose or framework names."
        ),
        "SEARCH_ROWS": "\n".join(rows),
    }


def draft_documents_values(full_docs):
    """The full document index (design A PR A3, design B section 4 without a
    template change): every non-root corpus document, one row each in title
    order, filtered on the page by the baseline search.js. Type and area are
    search.js facet groups (spec 7.29; maintainer 2026-11-03: All Documents
    carries the filters, and type is a filter of it, not a separate
    heading), each chip's count recounted from the rows it filters and each
    chip a plain link to its facet address. From baseline 1.7.0 both groups
    carry data-filter-empty="disable" in the template, so search.js marks a
    chip that would show no rows unavailable; the served counts stay, as the
    page's filter paragraph says. The root specifications, which have no
    on-site page, open on GitHub and stay out of the filtered rows."""
    domain_docs = sorted(
        (d for d in full_docs if d.get("domain") != ROOT_DOMAIN),
        key=lambda d: (d.get("title", "").lower(), d["path"]),
    )
    root_docs = sorted(
        (d for d in full_docs if d.get("domain") == ROOT_DOMAIN),
        key=lambda d: (d.get("title", "").lower(), d["path"]),
    )
    by_domain = Counter(d.get("domain", "") for d in domain_docs)
    # The meta line's type count covers every document on the page, root
    # specifications included, as the type pages do.
    by_type = Counter(d.get("type", "") for d in full_docs)
    # A chip filters the rows below, so its count is recounted from those
    # rows alone (round-1 ERROR on this page: a chip that linked a type page
    # counted other documents than its landing showed); the chip links its
    # own facet address, never a page with a different count.
    type_names = {type_slug(d.get("type", "")): d.get("type", "")
                  for d in domain_docs}
    row_types = Counter(type_slug(d.get("type", "")) for d in domain_docs)
    # Each group reads its own row tokens (data-type, data-area), so a type
    # slug equal to an area slug matches only in its own group and needs no
    # guard.
    type_chips = _draft_facet_chips(
        "type", row_types, lambda slug: type_names[slug], len(domain_docs))
    area_chips = _draft_facet_chips(
        "area", by_domain, draft_domain_label, len(domain_docs))
    root_rows = "\n".join(
        f'<li><a href="{_esc(GITHUB_BLOB_BASE + d["path"])}"'
        ' target="_blank" rel="noopener noreferrer">'
        f'{_esc(d.get("title", d["path"]))}{_DRAFT_NEW_TAB}</a>'
        f'<span class="n">{_esc(d.get("type", "").lower())}, '
        f'{_esc(draft_domain_label(ROOT_DOMAIN))}</span>'
        f'<small>{_esc(d.get("date", ""))}</small></li>'
        for d in root_docs
    )
    rows = [_draft_search_row(d, facets=True) for d in domain_docs]
    return {
        **_draft_nav("documents"),
        "INDEX_AREA_CHIPS": area_chips,
        "INDEX_TYPE_CHIPS": type_chips,
        "INDEX_ROOT_ROWS": root_rows,
        "INDEX_ROWS": "\n".join(rows),
        "INDEX_COUNT": str(len(rows)),
        "INDEX_AREA_COUNT": str(len(by_domain)),
        "INDEX_TYPE_COUNT": str(len(by_type)),
        "INDEX_ROOT_COUNT": str(len(root_docs)),
    }


def draft_domain_values(dp, docs_by_path, next_url, next_label,
                        leadership=False):
    label = draft_domain_label(dp["domain"])
    by_type = {}
    for d in dp["docs"]:
        by_type.setdefault(d["type"], []).append(d)
    ordered = [t for t in TYPE_ORDER if t in by_type]
    ordered += sorted(t for t in by_type if t not in TYPE_RANK)
    rail_items = "\n".join(
        f'<li><a href="#t-{type_slug(t)}">{_esc(t)}, {len(by_type[t])}</a></li>'
        for t in ordered
    )
    sections = []
    for t in ordered:
        rows = []
        for d in by_type[t]:
            version = docs_by_path.get(d["path"], {}).get("version", "")
            tail = f'<span class="n">v{_esc(version)}</span>' if version else ""
            rows.append(
                f'<li><a href="{_esc(_doc_page_url("{{BASE}}", d["path"]))}">'
                f'{_esc(d["title"])}</a>{tail}</li>'
            )
        sections.append(
            f'<p class="lbl sec">{_esc(t)}, {len(by_type[t])}</p>\n'
            f'<h2 id="t-{type_slug(t)}">{_esc(draft_type_plural(t))}</h2>\n'
            f'<div class="wide"><ul class="plan">\n' + "\n".join(rows)
            + "\n</ul></div>"
        )
    if leadership:
        # The registry join the v2 and v3 domain pages already compute
        # (dp["narratives"]: every narrative page whose domain tags include
        # this domain), each row linking the page's on-site reading room.
        count = len(dp["narratives"])
        rail_items += f'\n<li><a href="#leadership">Leadership, {count}</a></li>'
        rows = [
            f'<li><a href="{_esc(narrative_page_url(page))}">'
            f'{_esc(page["title"])}</a>'
            f'<span class="n">{_esc(page["narrative_type"].lower())}</span></li>'
            for page in dp["narratives"]
        ]
        if rows:
            listing = (
                '<div class="wide"><ul class="plan one">\n' + "\n".join(rows)
                + "\n</ul></div>"
            )
        else:
            listing = (
                "<p>No leadership page tags this area yet: a declared "
                "coverage gap, not a hidden one.</p>"
            )
        sections.append(
            f'<p class="lbl sec">Leadership, {count}</p>\n'
            '<h2 id="leadership">Leadership pages for this area</h2>\n'
            "<p>Pages from the executive layer that tag this area. They "
            "explain and advise; the documents above govern.</p>\n" + listing
        )
    noun = "document" if dp["count"] == 1 else "documents"
    return {
        **_draft_nav("browse"),
        "DOMAIN_LABEL": _esc(label),
        "DOMAIN_META": f"{dp['count']} {noun}. {_esc(dp['scope'])}.",
        "DOMAIN_LEAD": _esc(dp["purpose"]),
        "DOMAIN_RAIL_ITEMS": rail_items,
        "DOMAIN_SECTIONS": "\n".join(sections),
        "NEXT_URL": next_url,
        "NEXT_LABEL": next_label,
    }


_DRAFT_SCRIPT_SRC_RE = re.compile(r'<script\b[^>]*\ssrc="([^"]*)"', re.I)


def draft_loaded_scripts(htmls, prefix):
    """Every script the rendered draft pages load, as sorted file names
    under ``prefix`` (the draft's ``assets/baseline/``). BuildError on a
    script from anywhere else, so the disclosure's evidence list can never
    leave one out."""
    names = set()
    for html in htmls:
        for src in _DRAFT_SCRIPT_SRC_RE.findall(html):
            name = src[len(prefix):] if src.startswith(prefix) else ""
            if not name or "/" in name:
                raise BuildError(
                    f"draft: script {src} is not a baseline asset under "
                    f"{prefix}, so the disclosure cannot list it"
                )
            names.add(name)
    return sorted(names)


def draft_disclosure_values(scripts):
    """Entry 6's evidence links every runtime script the draft pages load,
    generated from the rendered pages (round-2 NOTE: a typed list left out
    rail.js)."""
    links = " ".join(
        f'<a href="{_esc(GITHUB_BLOB_BASE + ".web/baseline/" + name)}"'
        ' target="_blank" rel="noopener noreferrer">'
        f'{_esc(name)}{_DRAFT_NEW_TAB}</a>'
        for name in scripts
    )
    return {
        **_draft_nav(),
        "SCRIPT_EVIDENCE": links,
    }


def draft_license_values(pin_path=None):
    """The licence page names the shared template's version from the pin,
    never typed in the template (spec section 11)."""
    version, _ = read_baseline_pin(pin_path)
    return {
        **_draft_nav(),
        "BASELINE_VERSION": _esc(version),
    }


def draft_doc_purpose(doc):
    """A document's taxonomy purpose, or a generated line when it has none
    (shared by the document page lead and the type page rows)."""
    purpose = doc.get("purpose", "")
    if not purpose:
        purpose = (
            f"A {doc.get('type', '').lower()} in the "
            f"{draft_domain_label(doc.get('domain', ''))} area of the GRC Library."
        )
    return purpose


def draft_type_values(tp, docs_by_path, next_url, next_label, adopter_docs=()):
    # One row per document of the type, in the shared type-page order (area,
    # then title), each with its area and purpose. Root-level specifications
    # have no draft document page, so they link their GitHub source, as the
    # related-documents list does; their area label is the documents index's.
    # The docs/ adopter documents of the type follow in their own labelled
    # list (integration round 2 WARN: the page said every document of the
    # type while listing only the corpus ones); the corpus list stays apart,
    # so the index's type chip still counts its corpus-area rows (site f1:
    # a chip counts the rows it filters, which no library specification is).
    rows = []
    for d in tp["docs"]:
        doc = docs_by_path.get(d["path"], d)
        area = draft_domain_label(d["domain"])
        if d["domain"] == ROOT_DOMAIN:
            link = (
                f'<a href="{_esc(GITHUB_BLOB_BASE + d["path"])}"'
                ' target="_blank" rel="noopener noreferrer">'
                f'{_esc(d["title"])}{_DRAFT_NEW_TAB}</a>'
            )
        else:
            link = (
                f'<a href="{_esc(_doc_page_url("{{BASE}}", d["path"]))}">'
                f'{_esc(d["title"])}</a>'
            )
        rows.append(
            f'<li>{link}<span class="n">{_esc(area)}</span>'
            f'<small>{_esc(draft_doc_purpose(doc))}</small></li>'
        )
    adopter_rows = [
        f'<li><a href="{_esc(_doc_page_url("{{BASE}}", g["path"]))}">'
        f'{_esc(g["title"])}</a>'
        f'<span class="n">{_esc(draft_domain_label(g["domain"]))}</span>'
        f'<small>{_esc(draft_doc_purpose(g))}</small></li>'
        for g in adopter_docs
    ]
    total = len(rows) + len(adopter_rows)
    noun = "document" if total == 1 else "documents"
    meta = f"{total} {noun}"
    adopter_block = ""
    if adopter_rows:
        n = len(adopter_rows)
        meta += (
            f": {len(rows)} in the corpus and {n} adopter "
            f"{'document' if n == 1 else 'documents'} under docs/"
        )
        if n == 1:
            intro = (
                f"The {n} adopter document of this type, under docs/ and "
                "outside the corpus taxonomy; its entry is read from the "
                "leading metadata block of its file at build time. Its title "
                "opens the document's page, which holds the record and, where "
                "the document has them, its outline and related documents."
            )
        else:
            intro = (
                f"The {n} adopter documents of this type, under docs/ and "
                "outside the corpus taxonomy; each entry is read from the "
                "leading metadata block of its file at build time. Each title "
                "opens the document's page, which holds the record and, where "
                "the document has them, its outline and related documents."
            )
        adopter_block = (
            f'<p class="lbl blk">'
            f"{_esc(draft_domain_label(ADOPTER_DOCS_AREA))}, {n}</p>\n"
            f"<p>{intro}</p>\n"
            '<div class="wide"><ul class="plan one described">\n'
            + "\n".join(adopter_rows) + "\n</ul></div>"
        )
    # The type's facet address on All Documents, where the type has a row
    # there: that list adds the area chips and the text filter to the type.
    # Its rows are the corpus-area documents only, so the sentence counts
    # them from this page's own lists and says so when the library
    # specifications or the adopter documents this page also lists stay out.
    # The sentence follows the adopter block, so a part names its whole as
    # the page's documents, never "these" (batch 3 round 2 WARN: "these"
    # read as the adopter documents just above it).
    in_index = [d for d in tp["docs"] if d["domain"] != ROOT_DOMAIN]
    filter_section = ""
    if in_index:
        if len(in_index) == total:
            held = ("this document" if len(in_index) == 1
                    else f"these {len(in_index)} documents")
        elif len(in_index) == 1:
            held = (f"the one of this page's {total} documents that sits "
                    "in a corpus area")
        else:
            held = (f"the {len(in_index)} of this page's {total} documents "
                    "that sit in a corpus area")
        # One document leaves the area chips and the text filter nothing to
        # narrow, so the clause saying they narrow "them" goes (round-1
        # NOTE: Checklists and Roadmaps each list one document); rows that
        # all sit in one area leave the area chips nothing to narrow, so only
        # the text filter is named (integration note: Guides, Principles,
        # SOPs and Specifications each sit in one area). From baseline 1.7.0
        # an area chip holding none of the type's rows is unavailable there,
        # which narrows nothing either, so the clause names only the area
        # chips holding them (adoption round-2 NOTE).
        if len(in_index) == 1:
            narrow = ""
        elif len({d["domain"] for d in in_index}) == 1:
            narrow = ", and its text filter narrows them further"
        else:
            narrow = (", and the area chips holding any of them, and its text "
                      "filter, narrow them further")
        filter_section = (
            f'<p>With script, <a href="{{{{BASE}}}}/documents/?type='
            f'{_esc(_draft_facet_value(tp["slug"]))}">All Documents, filtered '
            f'to {_esc(draft_type_plural(tp["type"]))}</a>, lists '
            f"{held}{narrow}.</p>"
        )
    return {
        **_draft_nav("browse"),
        "TYPE_HEADING": _esc(draft_type_plural(tp["type"])),
        "TYPE_META": f"{meta}. {_esc(tp['scope'])}.",
        "TYPE_FILTER_SECTION": filter_section,
        "TYPE_ROWS": "\n".join(rows),
        "TYPE_ROW_COUNT": str(total),
        "TYPE_ADOPTER_BLOCK": adopter_block,
        "NEXT_URL": next_url,
        "NEXT_LABEL": next_label,
    }


def draft_document_values(doc, docs_by_path):
    doc_type = doc.get("type", "")
    title = doc.get("title", doc["path"])
    purpose = draft_doc_purpose(doc)
    logo = (
        f'<img class="rail-logo" src="{{{{BASE}}}}/assets/baseline/logos/'
        f'grclibrary.svg" alt="Books on a shelf with a seal">'
    )
    # Spec 7.6 allows two rails only, so a document page takes the logo-only
    # rail; the source document's outline is body content, a plain list
    # under its own heading (maintainer, 2026-11-03 12:16Z).
    rail = f'<div class="rail">{logo}</div>'
    outline_section = ""
    sections = doc.get("sections", [])
    if sections:
        items = "\n".join(
            "<li>"
            + _esc(re.sub(r"\*\*([^*]+)\*\*", r"\1", s.replace("`", "")))
            + "</li>"
            for s in sections
        )
        outline_section = f'<h2>Outline</h2>\n<ul>\n{items}\n</ul>'
    record = "\n".join(
        f"<dt>{_esc(field)}</dt><dd>{_esc(doc[key])}</dd>"
        for field, key in DRAFT_RECORD_FIELDS if doc.get(key)
    )
    frameworks_section = ""
    if doc.get("frameworks"):
        # Each chip opens the search already run for its framework name (the
        # ?q= address search.js reads on load, spec 7.29; design B 5.5: a
        # bare search link lost the framework the reader clicked).
        chips = "".join(
            f'<li><a href="{_esc(_draft_search_url(f))}">{_esc(f)}</a></li>'
            for f in doc["frameworks"]
        )
        frameworks_section = (
            f'<h2>Frameworks it maps to</h2>\n<ul class="chips">{chips}</ul>'
        )
    related_section = ""
    if doc.get("related_documents"):
        rows = []
        for rp in doc["related_documents"]:
            rd = docs_by_path.get(rp)
            if rd and rd.get("domain") != ROOT_DOMAIN:
                rows.append(
                    f'<li><a href="{_esc(_doc_page_url("{{BASE}}", rp))}">'
                    f'{_esc(rd.get("title", rp))}</a>'
                    f'<span class="n">{_esc(rd.get("domain", ""))}</span></li>'
                )
            else:
                rtitle = rd.get("title", rp) if rd else rp
                rows.append(
                    f'<li><a href="{_esc(GITHUB_BLOB_BASE + rp)}"'
                    ' target="_blank" rel="noopener noreferrer">'
                    f'{_draft_wrapping_path(rtitle)}{_DRAFT_NEW_TAB}</a>'
                    '<span class="n">source</span></li>'
                )
        related_section = (
            '<h2>Related documents</h2>\n<ul class="plan one">\n'
            + "\n".join(rows) + "\n</ul>"
        )
    return {
        **_draft_nav("documents"),
        "DOC_TITLE": _esc(title),
        "DOC_HEADING": _draft_breakable_title(title),
        "DOC_TYPE": _esc(doc_type),
        "DOC_RAIL": rail,
        "DOC_OUTLINE_SECTION": outline_section,
        "DOC_LEAD": _esc(purpose),
        "DOC_RECORD": record,
        "DOC_GITHUB_URL": _esc(GITHUB_BLOB_BASE + doc["path"]),
        "DOC_FRAMEWORKS_SECTION": frameworks_section,
        "DOC_RELATED_SECTION": related_section,
    }


def draft_narrative_body(body_html, source_rel):
    """Adapt one render_narrative_body result to the draft shell (see
    _DRAFT_NARR_SECTION_RE). Each rewrite must account for every section,
    every link and every table in the body, so a renderer shape change raises
    here rather than shipping a section with no box, a link with no new-tab
    hint or a table that widens the page."""
    body, moved = _DRAFT_NARR_SECTION_RE.subn(
        lambda m: f'<section class="narr">\n    <div id="{m.group(1)}">',
        body_html,
    )
    if moved != body_html.count("<section "):
        raise BuildError(
            f"draft: {source_rel}: a narrative section outside the shape the "
            "draft shell adapts (renderer change?)"
        )
    body, marked = _DRAFT_NARR_LINK_RE.subn(
        lambda m: (f'{m.group(1)} target="_blank" rel="noopener noreferrer">'
                   f"{m.group(2)}{_DRAFT_NEW_TAB}</a>"),
        body,
    )
    if marked != body_html.count("<a "):
        raise BuildError(
            f"draft: {source_rel}: a narrative link outside the shape the "
            "draft shell adapts (renderer change?)"
        )
    body, wrapped = _DRAFT_NARR_TABLE_RE.subn(
        r'<div class="tablewrap" tabindex="0"><table>\1</table></div>', body
    )
    if wrapped != body_html.count("<table"):
        raise BuildError(
            f"draft: {source_rel}: a narrative table outside the shape the "
            "draft shell adapts (renderer change?)"
        )
    return body


def draft_narrative_values(page, body_html, toc):
    _, label, _ = draft_narrative_subtype(page["narrative_type"])
    rail_items = "\n".join(
        f'<li><a href="#{anchor}">{_esc(heading)}</a></li>'
        for anchor, heading in toc
    )
    chips = "".join(
        f'<li><a href="{{{{BASE}}}}/{_esc(d)}/">'
        f"{_esc(draft_domain_label(d))}</a></li>"
        for d in page["domains"]
    )
    return {
        **_draft_nav("decisions"),
        "NARRATIVE_TYPE": _esc(page["narrative_type"]),
        "NARRATIVE_H1": _esc(page["title"]),
        "NARRATIVE_RAIL_ITEMS": rail_items,
        "NARRATIVE_BODY": draft_narrative_body(body_html, page["path"]),
        # Brace-escaped as on v2 and v3 (narrative_page_values).
        "NARRATIVE_SOURCE_URL": _esc(narrative_source_blob_url(page)).replace("{", "&#123;"),
        "NARRATIVE_DOMAIN_CHIPS": chips,
        "NARRATIVE_INDEX_URL": _draft_subtype_url(page["narrative_type"]),
        "NARRATIVE_INDEX_LABEL": _esc(label.lower()),
    }


def draft_subtype_values(figures, narrative_type):
    """One generated subtype index: every registry narrative page of
    ``narrative_type``, title order, each row its title (to the on-site
    reading room) and the domains it tags; then the other subtype indexes
    with their counts. An empty subtype is a declared gap, never hidden."""
    _, label, question = draft_narrative_subtype(narrative_type)
    members = sorted(
        (p for p in figures["narratives"] if p["narrative_type"] == narrative_type),
        key=lambda p: (p["title"].lower(), p["path"]),
    )
    rows = []
    for page in members:
        domains = ", ".join(
            f'<a href="{{{{BASE}}}}/{_esc(d)}/">{_esc(draft_domain_label(d))}</a>'
            for d in page["domains"]
        )
        rows.append(
            f'<li><a href="{_esc(narrative_page_url(page))}">'
            f'{_esc(page["title"])}</a><small>{domains}</small></li>'
        )
    if not rows:
        rows.append(
            "<li>No page of this kind is published yet: a declared coverage "
            "gap, not a hidden one.</li>"
        )
    siblings = "\n".join(
        f'<li><a href="{_draft_subtype_url(other)}">{_esc(other_label)}</a>'
        f'<span class="n">'
        f'{sum(1 for p in figures["narratives"] if p["narrative_type"] == other)}'
        f"</span></li>"
        for other, (_, other_label, _) in DRAFT_NARRATIVE_SUBTYPES.items()
        if other != narrative_type
    )
    noun = "page" if len(members) == 1 else "pages"
    return {
        **_draft_nav("decisions"),
        "SUBTYPE_LABEL": _esc(label),
        "SUBTYPE_META": f"{len(members)} {noun}. {_esc(question)}",
        "SUBTYPE_COUNT": str(len(members)),
        "SUBTYPE_ROWS": "\n".join(rows),
        "SUBTYPE_SIBLINGS": siblings,
    }


def _concern_counts(concern):
    """One concern's two generated counts as display text: the leadership
    pages mapped to it and the governing documents its shelf resolves to."""
    pages = len(concern["mapped_pages"])
    docs = len(concern["docs"])
    pages_noun = "leadership page" if pages == 1 else "leadership pages"
    docs_noun = "governing document" if docs == 1 else "governing documents"
    return f"{pages} {pages_noun}, {docs} {docs_noun}"


def _concern_gap_mark(concern):
    """A concern row's .n slot: the short declared-gap mark (never hidden)
    where no leadership page maps to the concern, else nothing. The row's
    counts sit in its <small> line instead: .plan li .n is nowrap in a
    minmax(0, 1fr) auto grid, so a full count there took the row at 320 px
    and shrank the question column to nothing (item 3b788)."""
    if concern["mapped_pages"]:
        return ""
    return '<span class="n">declared gap</span>'


def draft_decide_values(figures, concerns):
    """The decide hub at decide/ (design D section 4.1): branch 1 the concern
    rows grouped under the three board questions, each row carrying the
    question-led title, a declared-gap mark (never hidden) where a concern
    has no leadership page, and the two generated counts in its wrapping
    <small> line; branch 2 the six subtype indexes with their counts; branch
    3 the Browse By domain list, unchanged."""
    group_sections = []
    rail_items = []
    for group_slug, board_question in DRAFT_DECIDE_GROUPS:
        members = [c for c in concerns if c["group"] == group_slug]
        rows = []
        for concern in members:
            rows.append(
                f'<li><a href="{{{{BASE}}}}/decide/{_esc(concern["slug"])}/">'
                f'{_esc(concern["question"])}</a>'
                f'{_concern_gap_mark(concern)}'
                f'<small>{_esc(concern["label"])}. '
                f'{_concern_counts(concern)}.</small></li>'
            )
        group_sections.append(
            f'<p class="lbl sec">Concerns, {len(members)}</p>\n'
            f'<h2 id="g-{group_slug}">{_esc(board_question)}</h2>\n'
            '<div class="wide"><ul class="plan described one">\n'
            + "\n".join(rows) + "\n</ul></div>"
        )
        rail_items.append(
            f'<li><a href="#g-{group_slug}">{_esc(board_question)}</a></li>'
        )
    rail_items.append('<li><a href="#kinds">The kind of page</a></li>')
    rail_items.append('<li><a href="#domains">The domain you oversee</a></li>')
    kinds = "\n".join(
        f'<li><a href="{_draft_subtype_url(narrative_type)}">{_esc(label)}</a>'
        f'<span class="n">'
        f'{sum(1 for p in figures["narratives"] if p["narrative_type"] == narrative_type)}'
        f"</span><small>{_esc(question)}</small></li>"
        for narrative_type, (_, label, question)
        in DRAFT_NARRATIVE_SUBTYPES.items()
    )
    # Branch 3 is the Browse By domain list, unchanged (draft_browse_values
    # keeps its own copy so Browse stays untouched by this hub).
    domains = "\n".join(
        f'<li><a href="{{{{BASE}}}}/{_esc(domain)}/">'
        f'{_esc(draft_domain_label(domain))}</a>'
        f'<span class="n">{count}</span>'
        f'<small>{_esc(DOMAIN_SCOPE[domain])}</small></li>'
        for domain, count in figures["domains"]
    )
    return {
        **_draft_nav("decisions"),
        "DECIDE_META": (
            f"{len(concerns)} concerns under {len(DRAFT_DECIDE_GROUPS)} board "
            f"questions, {len(figures['narratives'])} leadership pages, "
            f"{figures['domain_count']} domains."
        ),
        "DECIDE_RAIL_ITEMS": "\n".join(rail_items),
        "DECIDE_GROUPS": "\n".join(group_sections),
        "DECIDE_KINDS": kinds,
        "DECIDE_DOMAINS": domains,
    }


def draft_concern_values(concern):
    """One concern topic page at decide/<slug>/ (design D section 5): the
    curated title, lede and group; then the generated blocks, the leadership
    pages mapped to the concern (or the declared-gap block, never hidden), the
    governing-documents shelf, the frameworks touched (each name linking its
    crosswalk instrument page where the alias map carries one, else plain
    text), and the Go deeper domain chips."""
    board_question = dict(DRAFT_DECIDE_GROUPS)[concern["group"]]
    pages = concern["mapped_pages"]
    docs = concern["docs"]
    rail_items = [
        f'<li><a href="#leadership">Leadership pages, {len(pages)}</a></li>',
        f'<li><a href="#documents">Governing documents, {len(docs)}</a></li>',
        f'<li><a href="#frameworks">Frameworks, '
        f'{len(concern["frameworks"])}</a></li>',
        '<li><a href="#domains">Go deeper</a></li>',
    ]
    # The sentences that describe what this page links are chosen by whether
    # the concern has mapped pages, so each stays true on a declared-gap page
    # (round-1 review: three intros claimed leadership pages a gap page lacks),
    # and the shelf sentences agree in number with the shelf (round-3: a
    # one-document gap shelf read as plural).
    one_doc = len(docs) == 1
    if one_doc:
        shelf_close = (
            "This is the document that governs, and the evidence to ask for "
            "starts here."
        )
    else:
        shelf_close = (
            "These are the documents that govern, and the evidence to ask for "
            "starts here."
        )
    if pages:
        note = (
            "Adopting a page here decides nothing for you. The leadership "
            "pages linked here are explanatory and advisory; they establish no "
            "requirement and prove nothing about your organization. Every "
            "claim in them resolves to the governing reference documents in "
            "the corpus, and it is those documents that govern."
        )
        rows = [
            f'<li><a href="{_esc(narrative_page_url(page))}">'
            f'{_esc(page["title"])}</a>'
            f'<span class="n">{_esc(page["narrative_type"].lower())}</span></li>'
            for page in pages
        ]
        leadership = (
            "<p>Pages from the executive layer mapped to this concern, "
            "generated from the narrative registry. They explain and advise; "
            "the documents below govern.</p>\n"
            '<div class="wide"><ul class="plan one">\n' + "\n".join(rows)
            + "\n</ul></div>"
        )
        docs_intro = (
            "The evidence shelf: the corpus "
            + ("document" if one_doc else "documents")
            + " the pages above resolve to, joined to the library's registries "
            "at build time. " + shelf_close
        )
    else:
        if one_doc:
            shelf_note = (
                "The document below is a governing reference document in the "
                "corpus, and it is that document that governs."
            )
            shelf_material = "The governing document below is"
            shelf_intro = (
                "The evidence shelf: with no leadership page to resolve from, "
                "this is the corpus document chosen for this concern, checked "
                "against the taxonomy at build time."
            )
        else:
            shelf_note = (
                "The documents below are governing reference documents in the "
                "corpus, and it is those documents that govern."
            )
            shelf_material = "The governing documents below are"
            shelf_intro = (
                "The evidence shelf: with no leadership page to resolve from, "
                "these are the corpus documents chosen for this concern, each "
                "checked against the taxonomy at build time."
            )
        note = "No leadership page is linked here yet. " + shelf_note
        leadership = (
            '<div class="callout"><p>Declared coverage gap: no leadership '
            "page is published for this concern yet. A gap is declared, never "
            "hidden, and never padded; coverage is measured by concerns with "
            f"published pages, not by page count. {shelf_material} the corpus "
            "material that supports the concern today.</p></div>"
        )
        docs_intro = shelf_intro + " " + shelf_close
    doc_rows = "\n".join(
        f'<li><a href="{_esc(_doc_page_url("{{BASE}}", d["path"]))}">'
        f'{_esc(d.get("title", d["path"]))}</a>'
        f'<span class="n">{_esc(d.get("type", "").lower())}, '
        f'{_esc(draft_domain_label(d.get("domain", "")))}</span></li>'
        for d in docs
    )
    if concern["frameworks"]:
        # Each name whose exact spelling the committed alias map carries
        # links its crosswalk instrument page (the crosswalk ships on this
        # branch), a name joining several texts links each part that names
        # an instrument to its own page and shows any other part as plain
        # text, and a name outside both maps stays plain text, never a
        # guessed link (fix for the concern-page WARN: the page said the
        # crosswalk was not built yet).
        chips = []
        for f in concern["frameworks"]:
            key = CROSSWALK_ALIASES.get(f)
            if key:
                chips.append(
                    f'<li><a href="{{{{BASE}}}}/crosswalk/{key}/">'
                    f"{_esc(f)}</a></li>"
                )
            elif f in CROSSWALK_ALIAS_PARTS:
                chips.append("<li>" + " / ".join(
                    f'<a href="{{{{BASE}}}}/crosswalk/{part_key}/">'
                    f"{_esc(part)}</a>" if part_key is not None
                    else _esc(part)
                    for part, part_key in CROSSWALK_ALIAS_PARTS[f]
                ) + "</li>")
            else:
                chips.append(f"<li>{_esc(f)}</li>")
        frameworks = '<ul class="chips">' + "".join(chips) + "</ul>"
    else:
        frameworks = (
            "<p>No governing document on this shelf carries an external "
            "framework mapping yet: a declared gap, not a hidden one.</p>"
        )
    domain_chips = "".join(
        f'<li><a href="{{{{BASE}}}}/{_esc(d)}/">'
        f"{_esc(draft_domain_label(d))}</a></li>"
        for d in concern["domains"]
    )
    return {
        **_draft_nav("decisions"),
        "CONCERN_LABEL": _esc(concern["label"]),
        "CONCERN_TITLE": _esc(concern["question"]),
        "CONCERN_META": f"{_concern_counts(concern)}. {_esc(board_question)}",
        "CONCERN_LEDE": _esc(concern["lede"]),
        "CONCERN_RAIL_ITEMS": "\n".join(rail_items),
        "CONCERN_NOTE": note,
        "CONCERN_LEADERSHIP": leadership,
        "CONCERN_DOCS_INTRO": docs_intro,
        "CONCERN_DOCS": doc_rows,
        "CONCERN_FRAMEWORKS": frameworks,
        "CONCERN_DOMAIN_CHIPS": domain_chips,
    }


def draft_govern_values(figures, docs_by_path, concerns):
    """The govern need page at govern/ (design D section 4.2): the four
    starting situations carried from templates-v2/start.html via
    templates-v3/govern.html as curated template prose, their artefact links
    resolved by _draft_doc_or_source_link over the merged page lookup (a
    docs/ adopter document links its draft document page, gap G1), and the
    generated landing list: the two programme domains, the document types
    that stand a programme up (counted, with their clauses, from
    DRAFT_GOVERN_LANDING_TYPES), and the programme-maturity concern page."""
    maturity = _draft_concern_entry(concerns, DRAFT_GOVERN_CONCERN)
    lands = []
    for domain in DRAFT_GOVERN_LANDING_DOMAINS:
        dp = _draft_domain_page(figures, domain)
        lands.append(
            f'<li><a href="{{{{BASE}}}}/{_esc(domain)}/">'
            f'{_esc(draft_domain_label(domain))}</a>'
            f'<span class="n">{dp["count"]}</span>'
            f'<small>{_esc(DOMAIN_SCOPE[domain])}</small></li>'
        )
    for type_name in DRAFT_GOVERN_LANDING_TYPES:
        tp = _draft_type_entry(figures, type_name)
        lands.append(
            f'<li><a href="{{{{BASE}}}}/types/{tp["slug"]}/">'
            f'{_esc(draft_type_plural(type_name))}</a>'
            f'<span class="n">{tp["count"]}</span>'
            f'<small>{_esc(TYPE_SCOPE[type_name])}</small></li>'
        )
    lands.append(
        f'<li><a href="{{{{BASE}}}}/decide/{_esc(maturity["slug"])}/">'
        f'{_esc(maturity["question"])}</a>'
        f'{_concern_gap_mark(maturity)}'
        f'<small>{_esc(maturity["label"])}. '
        f'{_concern_counts(maturity)}.</small></li>'
    )
    gov = _draft_domain_page(figures, DRAFT_GOVERN_LANDING_DOMAINS[0])
    comp = _draft_domain_page(figures, DRAFT_GOVERN_LANDING_DOMAINS[1])
    counts = {
        type_name: _draft_type_entry(figures, type_name)["count"]
        for type_name in tuple(DRAFT_GOVERN_LANDING_TYPES) + ("Annex",)
    }
    n_types = len(DRAFT_GOVERN_LANDING_TYPES)
    types_sentence = (
        f"The work rests on {n_types} document "
        + ("type" if n_types == 1 else "types") + ": "
        + _draft_series(
            f"{draft_type_plural(type_name).lower()} {role}"
            for type_name, role in DRAFT_GOVERN_LANDING_TYPES.items()
        ) + "."
    )
    return {
        **_draft_nav("browse"),
        **{
            key: _draft_doc_or_source_link(docs_by_path, path, label)
            for key, (path, label) in DRAFT_GOVERN_ARTEFACTS.items()
        },
        "GOVERN_META": (
            f"{gov['count']} governance and {comp['count']} compliance "
            "documents; "
            + ", ".join(
                f"{counts[type_name]} "
                + (draft_type_plural(type_name).lower()
                   if counts[type_name] != 1 else type_name.lower())
                for type_name in DRAFT_GOVERN_LANDING_TYPES
            ) + "."
        ),
        "GOVERN_LANDS": "\n".join(lands),
        "GOV_TYPES_SENTENCE": _esc(types_sentence),
        "GOV_DOMAIN_COUNT": str(gov["count"]),
        "GOV_ANNEX_COUNT": str(counts["Annex"]),
        "GOV_MATURITY_URL": "{{BASE}}/decide/" + maturity["slug"] + "/",
        "GOV_MATURITY_QUESTION": _esc(maturity["question"]),
    }


def draft_comply_values(figures, docs_by_path, xw):
    """The comply need page at comply/ (design D section 4.3): the
    instrument index generated from the crosswalk model, one row per
    configured instrument (CROSSWALK_INSTRUMENTS, main-table and "Also in
    the corpus" alike), each row landing on its instrument page with the
    generated count of library documents the matrices map to it or whose
    framework alignment names it in a form the committed alias maps carry
    (integration round 3 WARN: a name in any other form is not counted, and
    the page says so); the sentence saying how the crosswalk
    shows them, generated from the same main_table split the crosswalk table
    and its "Also in the corpus" index use; the not-listed branch; and the
    work-backwards method carried from templates-v3/comply.html onto
    generated links."""
    rows = []
    mapped_union = set()
    for inst in CROSSWALK_INSTRUMENTS:
        data = xw["instruments"][inst.key]
        paths = {path for entry in data["by_domain"].values()
                 for path, _ in entry["docs"]}
        paths |= {d["path"] for d in data["citations"]}
        mapped_union |= paths
        rows.append(
            f'<li><a href="{{{{BASE}}}}/crosswalk/{inst.key}/">'
            f'{_esc(data["display"])}</a>'
            f'<span class="n">{len(paths)} {_xw_doc_noun(len(paths))}</span>'
            f'<small>{_esc(inst.group)}</small></li>'
        )
    main_keys = [i.key for i in CROSSWALK_INSTRUMENTS if i.main_table]
    extra_keys = [i.key for i in CROSSWALK_INSTRUMENTS if not i.main_table]
    if extra_keys:
        xw_scope = (
            f"shows {len(main_keys)} of them as one table, domain by domain, "
            "and lists "
            + _draft_series(_esc(xw["instruments"][key]["display"])
                            for key in extra_keys)
            + f" under {_esc(_XW_G_ALSO)}."
        )
    else:
        xw_scope = "shows all of them as one table, domain by domain."
    if DRAFT_COMPLY_GAPS_REGISTER not in docs_by_path:
        raise BuildError(
            f"draft: comply names {DRAFT_COMPLY_GAPS_REGISTER} which is not "
            "in the taxonomy (renamed or removed?)"
        )
    gaps = docs_by_path[DRAFT_COMPLY_GAPS_REGISTER]
    outcome = next(
        (p for p in figures["narratives"]
         if p["path"] == DRAFT_COMPLY_OUTCOME_MAP), None)
    if outcome is None:
        raise BuildError(
            f"draft: comply names {DRAFT_COMPLY_OUTCOME_MAP} which the "
            "narrative registry does not carry (renamed or removed?)"
        )
    return {
        **_draft_nav("browse"),
        "COMPLY_META": (
            f"{len(rows)} instruments; {len(mapped_union)} library documents "
            "count toward at least one of them."
        ),
        "COMPLY_ROW_COUNT": str(len(rows)),
        "COMPLY_INSTRUMENTS": "\n".join(rows),
        "COMPLY_XW_SCOPE": xw_scope,
        "COMPLY_MATRIX_COUNT": str(_draft_type_entry(figures, "Matrix")["count"]),
        "COMPLY_ANNEX_COUNT": str(_draft_type_entry(figures, "Annex")["count"]),
        "COMPLY_REGISTER_COUNT": str(
            _draft_type_entry(figures, "Register")["count"]
        ),
        "COMPLY_GAPS_LINK": _draft_doc_or_source_link(
            docs_by_path, DRAFT_COMPLY_GAPS_REGISTER,
            gaps.get("title", DRAFT_COMPLY_GAPS_REGISTER)),
        "COMPLY_OUTCOME_LINK": (
            f'<a href="{_esc(narrative_page_url(outcome))}">'
            f'{_esc(outcome["title"])}</a>'
        ),
        "COMPLY_ART_COMPLIANCE_MATRIX": _draft_doc_or_source_link(
            docs_by_path, CROSSWALK_COMPLIANCE_MATRIX_PATH,
            "compliance alignment matrix"),
        "COMPLY_ART_FORWARD_MATRIX": _draft_doc_or_source_link(
            docs_by_path, CROSSWALK_FORWARD_MATRIX_PATH,
            "cross-framework alignment matrix"),
        "COMPLY_ART_REVERSE_MATRIX": _draft_doc_or_source_link(
            docs_by_path, CROSSWALK_REVERSE_MATRIX_PATH,
            "reverse framework-control crosswalk"),
        "COMPLY_ART_CITATIONS_REGISTER": _draft_doc_or_source_link(
            docs_by_path, "governance/register-canonical-citations.md",
            "canonical citations register"),
    }


def draft_solutions_values(figures, concerns):
    """The solutions need page at solutions/ (design D section 4.4): one row
    per curated lifecycle event, its main link the event's leadership page
    (or, where none walks it, its resolving concern page) with a generated
    count, and its Go deeper links the concern and domain pages behind it;
    then the generated index of every Scenario page (the hand-picked v3
    list drifted), and the builders block as domain rows."""
    by_path = {p["path"]: p for p in figures["narratives"]}
    event_rows = []
    for label, lede, page_path, concern_slug, domains in DRAFT_SOLUTION_EVENTS:
        concern = _draft_concern_entry(concerns, concern_slug)
        concern_link = (
            f'<a href="{{{{BASE}}}}/decide/{_esc(concern["slug"])}/">'
            f'{_esc(concern["question"])}</a>'
        )
        deeper = []
        if page_path is not None:
            page = by_path.get(page_path)
            if page is None:
                raise BuildError(
                    f"draft: solutions event '{label}' names {page_path} "
                    "which the narrative registry does not carry (renamed "
                    "or removed?)"
                )
            noun = ("governing document" if len(page["sources"]) == 1
                    else "governing documents")
            # The count sits in the wrapping <small> line, the .n slot
            # keeps only the page kind (item 3b788, as on the concern rows).
            main = (
                f'<a href="{_esc(narrative_page_url(page))}">'
                f'{_esc(page["title"])}</a>'
                f'<span class="n">{_esc(page["narrative_type"].lower())}</span>'
            )
            counts = f'{len(page["sources"])} {noun}'
            deeper.append(concern_link)
        else:
            main = f'{concern_link}{_concern_gap_mark(concern)}'
            counts = _concern_counts(concern)
        for domain in domains:
            dp = _draft_domain_page(figures, domain)
            deeper.append(
                f'<a href="{{{{BASE}}}}/{_esc(domain)}/">'
                f'{_esc(draft_domain_label(domain))}</a>'
            )
        tail = ""
        if deeper:
            tail = " Go deeper: " + "; ".join(deeper) + "."
        event_rows.append(
            f"<li>{main}<small>{_esc(lede)} {counts}.{tail}</small></li>"
        )
    scenarios = sorted(
        (p for p in figures["narratives"]
         if p["narrative_type"] == "Scenario"),
        key=lambda p: (p["title"].lower(), p["path"]),
    )
    # The decide/scenarios/ index's row shape, duplicated here so the
    # solutions page carries the whole generated list itself (design D 4.4:
    # a new scenario appears with no edit).
    scenario_rows = []
    for page in scenarios:
        domains = ", ".join(
            f'<a href="{{{{BASE}}}}/{_esc(d)}/">{_esc(draft_domain_label(d))}</a>'
            for d in page["domains"]
        )
        scenario_rows.append(
            f'<li><a href="{_esc(narrative_page_url(page))}">'
            f'{_esc(page["title"])}</a><small>{domains}</small></li>'
        )
    if not scenario_rows:
        scenario_rows.append(
            "<li>No scenario is published yet: a declared coverage gap, not "
            "a hidden one.</li>"
        )
    builders = []
    for domain in DRAFT_SOLUTION_BUILDER_DOMAINS:
        dp = _draft_domain_page(figures, domain)
        builders.append(
            f'<li><a href="{{{{BASE}}}}/{_esc(domain)}/">'
            f'{_esc(draft_domain_label(domain))}</a>'
            f'<span class="n">{dp["count"]}</span>'
            f'<small>{_esc(DOMAIN_SCOPE[domain])}</small></li>'
        )
    return {
        **_draft_nav("browse"),
        "SOL_META": (
            f"{len(DRAFT_SOLUTION_EVENTS)} lifecycle events, "
            f"{len(scenarios)} scenarios to rehearse, "
            f"{len(DRAFT_SOLUTION_BUILDER_DOMAINS)} domains for builders."
        ),
        "SOL_EVENT_COUNT": str(len(DRAFT_SOLUTION_EVENTS)),
        "SOL_EVENTS": "\n".join(event_rows),
        "SOL_SCENARIO_COUNT": str(len(scenarios)),
        "SOL_SCENARIOS": "\n".join(scenario_rows),
        "SOL_BUILDERS": "\n".join(builders),
    }


def draft_policies_values(figures):
    """The policies need page at policies/ (design D section 4.5): the
    policy and template type pages as the start rows, then the subject
    rows, one per domain with at least one policy or template, each count
    recounted from the type pages' own document lists."""
    start_rows = []
    per_domain = Counter()
    for type_name in ("Policy", "Template"):
        tp = _draft_type_entry(figures, type_name)
        start_rows.append(
            f'<li><a href="{{{{BASE}}}}/types/{tp["slug"]}/">'
            f'{_esc(draft_type_plural(type_name))}</a>'
            f'<span class="n">{tp["count"]}</span>'
            f'<small>{_esc(TYPE_SCOPE[type_name])}</small></li>'
        )
        for d in tp["docs"]:
            if d["domain"] != ROOT_DOMAIN:
                per_domain[d["domain"]] += 1
    subjects = sorted(per_domain.items(), key=lambda kv: (-kv[1], kv[0]))
    subject_rows = [
        f'<li><a href="{{{{BASE}}}}/{_esc(domain)}/">'
        f'{_esc(draft_domain_label(domain))}</a>'
        f'<span class="n">{count}</span>'
        f'<small>{_esc(DOMAIN_SCOPE[domain])}</small></li>'
        for domain, count in subjects
    ]
    policy_count = _draft_type_entry(figures, "Policy")["count"]
    template_count = _draft_type_entry(figures, "Template")["count"]
    return {
        **_draft_nav("browse"),
        "POL_META": (
            f"{policy_count} policies and {template_count} templates in the "
            f"corpus, across {len(subjects)} subjects."
        ),
        "POL_TYPES": "\n".join(start_rows),
        "POL_SUBJECT_COUNT": str(len(subjects)),
        "POL_SUBJECTS": "\n".join(subject_rows),
    }


def _xw_table_cells(line):
    """Split one markdown table line into stripped cell strings."""
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _xw_is_separator(cells):
    return all(set(c) <= {"-", ":", " "} and c for c in cells)


_XW_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_XW_MD_LINK_RE = re.compile(r"\[`?([^`\]]*)`?\]\([^)]*\)")
_XW_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# A register Topic cell may end in a register-internal "Note: ..." remark
# (maintenance prose, sometimes naming lint tooling); no page shows it.
_XW_TOPIC_NOTE_RE = re.compile(r"\.?\s*\bNote:.*\Z")


def _xw_plain(text):
    """Flatten a register or matrix cell for display: markdown links become
    their text, HTML comments drop, whitespace collapses."""
    text = _XW_COMMENT_RE.sub("", text)
    text = _XW_MD_LINK_RE.sub(r"\1", text)
    return " ".join(text.split())


def _xw_doc_paths(cell, where):
    """Document paths from a matrix cell's markdown links, backticked or
    bare. A link whose text does not read as one document path, link
    syntax outside the pattern, or anything but separators (commas,
    semicolons, whitespace) left once the links are removed (a path written
    as plain text) is a BuildError, never a silent drop."""
    paths = []
    for text in _XW_LINK_RE.findall(cell):
        path = text.strip()
        if len(path) >= 2 and path.startswith("`") and path.endswith("`"):
            path = path[1:-1].strip()
        if not path or "`" in path:
            raise BuildError(
                f"crosswalk: {where} holds a link the parser cannot read "
                f"as a document path: {text!r}"
            )
        paths.append(path)
    rest = _XW_LINK_RE.sub("", cell)
    if "](" in rest:
        raise BuildError(
            f"crosswalk: {where} holds link syntax the parser cannot "
            f"read: {cell!r}"
        )
    if rest.replace(",", " ").replace(";", " ").strip():
        raise BuildError(
            f"crosswalk: {where} holds text outside its document links "
            f"(a path written as plain text?): {cell!r}"
        )
    return paths


def _xw_topic_name(topic):
    """The descriptive name alone from a register Topic cell: the text
    before the first top-level semicolon or sentence-ending period (one
    followed by whitespace or the end, so a version such as "1.0" never
    cuts), with parentheticals dropped (currency remarks and expansions stay
    on the register record, never in a page lead)."""
    out = []
    depth = 0
    for i, ch in enumerate(topic):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif depth == 0:
            if ch == ";" or (ch == "." and not topic[i + 1:i + 2].strip()):
                break
            out.append(ch)
    return " ".join("".join(out).split())


def parse_citations_register(text):
    """Standard ID -> row dict from governance/register-canonical-citations.md.

    Structural and loud, like parse_taxonomy: only rows under the register's
    exact seven-column header are read; a malformed row, a duplicate Standard
    ID, or a zero-row parse is a BuildError (schema change)."""
    expected = ["Standard ID", "Current version", "Publication date", "Topic",
                "Superseded versions", "Upstream check location",
                "Last verified (UTC)"]
    rows = {}
    state = "outside"  # outside -> header -> rows
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            state = "outside"
            continue
        cells = _xw_table_cells(line)
        if cells == expected:
            state = "header"
            continue
        if state == "header":
            if not _xw_is_separator(cells):
                raise BuildError(
                    "crosswalk: citations register header not followed by a "
                    "separator row (schema change?)"
                )
            state = "rows"
            continue
        if state != "rows":
            continue
        if len(cells) != len(expected):
            raise BuildError(
                "crosswalk: citations register row with "
                f"{len(cells)} cell(s) instead of {len(expected)}: "
                f"{cells[0] if cells else line!r}"
            )
        standard_id = cells[0]
        if standard_id in rows:
            raise BuildError(
                f"crosswalk: duplicate Standard ID in the citations register: "
                f"{standard_id}"
            )
        rows[standard_id] = {
            "id": standard_id,
            "version": cells[1],
            "date": cells[2],
            # Register-internal notes never reach a page (round-2 fix 1).
            "topic": _XW_TOPIC_NOTE_RE.sub("", _xw_plain(cells[3])),
            "upstream": cells[5],
            "verified": cells[6],
        }
    if not rows:
        raise BuildError(
            "crosswalk: citations register parsed to zero rows (schema change?)"
        )
    return rows


def parse_compliance_matrix(text):
    """The compliance alignment matrix, domain section by domain section.

    Returns ``(domains, rows_by_domain)`` where ``domains`` is the matrix's own
    section order (slugs) and ``rows_by_domain[slug]`` is a list of
    ``{'path','title','cells'}`` dicts, ``cells`` keyed by
    CROSSWALK_COMPLIANCE_COLUMNS. Loud on schema change: a section header that
    is not exactly the pinned column set, a row with the wrong cell count or an
    unparsable path, a domain outside DOMAIN_SCOPE, or a missing domain all
    raise BuildError."""
    expected_header = ["Domain", "Document Title", "Path"] + list(
        CROSSWALK_COMPLIANCE_COLUMNS
    )
    domains = []
    rows_by_domain = {}
    domain = None
    state = "outside"
    for line in text.splitlines():
        m = re.match(r"^## (.+) domain\s*$", line)
        if m:
            slug = m.group(1).strip().lower().replace(" ", "-")
            if slug not in DOMAIN_SCOPE:
                raise BuildError(
                    f"crosswalk: compliance matrix section '{m.group(1)}' "
                    "names no DOMAIN_SCOPE domain (renamed domain or schema "
                    "change?)"
                )
            if slug in rows_by_domain:
                raise BuildError(
                    f"crosswalk: duplicate compliance matrix section for "
                    f"domain '{slug}'"
                )
            domain = slug
            domains.append(slug)
            rows_by_domain[slug] = []
            state = "outside"
            continue
        if line.startswith("## "):
            domain = None
            state = "outside"
            continue
        if domain is None or not line.strip().startswith("|"):
            state = "outside"
            continue
        cells = _xw_table_cells(line)
        if cells == expected_header:
            state = "header"
            continue
        if state == "header":
            if not _xw_is_separator(cells):
                raise BuildError(
                    f"crosswalk: compliance matrix '{domain}' header not "
                    "followed by a separator row (schema change?)"
                )
            state = "rows"
            continue
        if state != "rows":
            raise BuildError(
                f"crosswalk: compliance matrix table in '{domain}' does not "
                "open with the pinned column header (schema change?)"
            )
        if len(cells) != len(expected_header):
            raise BuildError(
                f"crosswalk: compliance matrix row in '{domain}' with "
                f"{len(cells)} cell(s) instead of {len(expected_header)}"
            )
        paths = _xw_doc_paths(
            cells[2], f"compliance matrix row in '{domain}'"
        )
        if len(paths) != 1:
            raise BuildError(
                f"crosswalk: compliance matrix row in '{domain}' must cite "
                f"exactly one document path: {cells[2]!r}"
            )
        rows_by_domain[domain].append({
            "path": paths[0],
            "title": cells[1],
            "cells": dict(zip(CROSSWALK_COMPLIANCE_COLUMNS, cells[3:])),
        })
    missing = sorted(set(DOMAIN_SCOPE) - set(rows_by_domain))
    if missing:
        raise BuildError(
            "crosswalk: compliance matrix is missing domain section(s): "
            + ", ".join(missing)
        )
    empty = sorted(d for d, rows in rows_by_domain.items() if not rows)
    if empty:
        raise BuildError(
            "crosswalk: compliance matrix domain section(s) with zero rows: "
            + ", ".join(empty)
        )
    return domains, rows_by_domain


def parse_compliance_tsc_status(text):
    """Whether the compliance alignment matrix says its AICPA TSC 2017 column
    is being populated (batch 3 round 4 item 1), read from its reading-guide
    paragraph alone (batch 3 round 6 item 1), the last paragraph of its "How
    to use this matrix" section. That section, from its heading to the ---
    that ends it, is pinned whole (batch 3 follow-up round 2 item 1): it must
    read exactly CROSSWALK_TSC_SECTION_HEADING, CROSSWALK_TSC_SECTION_OPENING
    and the reading-guide paragraph, each followed by a blank line, then ---,
    with the paragraph in one of two forms: CROSSWALK_TSC_READING_GUIDE, a
    space and CROSSWALK_TSC_POPULATING (True), or CROSSWALK_TSC_READING_GUIDE
    alone (False).

    Each of these is a BuildError naming the matrix file: any other text in
    that section, so the status sentence moved or reworded into the intro
    paragraph, into a paragraph of its own anywhere in the section, or into
    a key table row, old or new; the heading missing or repeated, or no ---
    after it; a second framework column key table anywhere in the matrix;
    and CROSSWALK_TSC_POPULATING anywhere outside the section (the document
    header, after the section's closing ---, Notes, a domain table, the end
    of the file), compared with each run of whitespace as one space, so a
    copy reflowed over several lines counts too.

    Not refused: a reworded status sentence outside the section (any text
    other than CROSSWALK_TSC_POPULATING up to whitespace). Telling one from
    an unrelated sentence would take phrase matching, which rounds 4 and 5
    showed misses rewordings and fails the build on an unrelated "populated"
    (batch 3 round 6 item 2), so outside the section the matrix is read for
    that one sentence alone and the status comes from the section."""
    forms = {
        f"{CROSSWALK_TSC_READING_GUIDE} {CROSSWALK_TSC_POPULATING}": True,
        CROSSWALK_TSC_READING_GUIDE: False,
    }
    populating, bare = forms
    accepted = (
        "its \"How to use this matrix\" section, from its heading to the --- "
        "that ends it, must read exactly CROSSWALK_TSC_SECTION_HEADING, "
        "CROSSWALK_TSC_SECTION_OPENING and its reading-guide paragraph, each "
        "followed by a blank line, then ---, with the reading-guide paragraph "
        "in one of two forms, CROSSWALK_TSC_READING_GUIDE followed by a space "
        "and CROSSWALK_TSC_POPULATING (the AICPA TSC 2017 column is being "
        "populated) or CROSSWALK_TSC_READING_GUIDE alone (it is not): "
        f"form 1: {populating} form 2: {bare}"
    )
    # The instruction is one fixed sentence (batch 3 follow-up round 4
    # item 1): naming one constant by similarity or line position named
    # the reading guide for a reworded status sentence, so updating it
    # passed with the status False, and on a layout line named a
    # constant that cannot make the section pass. The status rule names
    # every other pinned constant (batch 3 follow-up round 5 item 1): a
    # status sentence moved into the opening or a paragraph of its own
    # passes once that constant is updated, with the status False. Every
    # section error carries both (batch 3 follow-up round 6 item 1): a
    # status sentence moved into the heading takes the heading count
    # error, and passes once the heading is updated, with the status False.
    update = (
        "if the edit is intended, update the pinned text in .web/build.py "
        "(CROSSWALK_TSC_SECTION_HEADING, CROSSWALK_TSC_SECTION_OPENING, "
        "CROSSWALK_TSC_READING_GUIDE, CROSSWALK_TSC_POPULATING; the blank "
        "lines between the heading, the opening, the reading-guide "
        "paragraph and the closing --- are fixed in "
        "parse_compliance_tsc_status); a status sentence, changed or moved, "
        "belongs only in CROSSWALK_TSC_POPULATING at the end of the "
        "reading-guide line, never in CROSSWALK_TSC_SECTION_HEADING, "
        "CROSSWALK_TSC_SECTION_OPENING or CROSSWALK_TSC_READING_GUIDE, "
        "because the section without it records the AICPA TSC 2017 column "
        "as no longer being populated; "
    )
    where = f"crosswalk: {CROSSWALK_COMPLIANCE_MATRIX_PATH}:"
    lines = text.splitlines()
    heads = [i for i, line in enumerate(lines)
             if line == CROSSWALK_TSC_SECTION_HEADING]
    if len(heads) != 1:
        raise BuildError(
            f"{where} {len(heads)} {CROSSWALK_TSC_SECTION_HEADING!r} headings "
            f"instead of one; {update}{accepted}"
        )
    start = heads[0]
    end = next((i for i in range(start, len(lines)) if lines[i] == "---"),
               None)
    if end is None:
        raise BuildError(
            f"{where} no --- after {CROSSWALK_TSC_SECTION_HEADING!r} ends "
            f"its section; {update}{accepted}"
        )
    found = lines[start:end + 1]
    pinned = {
        status: [CROSSWALK_TSC_SECTION_HEADING, "",
                 *CROSSWALK_TSC_SECTION_OPENING.split("\n"), "",
                 paragraph, "", "---"]
        for paragraph, status in forms.items()
    }
    status = next((s for s, want in pinned.items() if found == want), None)
    if status is None:
        # The first line off the pin, the reading-guide line in either form.
        # Both lists end at their only line that is exactly ---, so they
        # differ before either ends.
        want = pinned[False]
        at = next(n for n, (got, line) in enumerate(zip(found, want))
                  if got != line and not (line == bare and got == populating))
        # At the reading-guide line the pin is shown in the populating form
        # when the found line is the reading guide with more text after it.
        expected = want[at]
        if (at == len(want) - 3 and found[at].startswith(bare)
                and found[at] != bare):
            expected = populating
        raise BuildError(
            f"{where} line {start + at + 1} reads {found[at]!r} where the "
            f"pin has {expected!r}; {update}{accepted}"
        )
    keys = [i for i, line in enumerate(lines)
            if line.strip().startswith("|")
            and tuple(_xw_table_cells(line)) == CROSSWALK_COMPLIANCE_KEY_HEADER]
    if len(keys) != 1:
        raise BuildError(
            f"{where} {len(keys)} framework column key tables (header "
            f"{' | '.join(CROSSWALK_COMPLIANCE_KEY_HEADER)}) instead of one; "
            f"{accepted}"
        )
    outside = (" ".join(text.split()).count(CROSSWALK_TSC_POPULATING)
               - int(status))
    if outside:
        raise BuildError(
            f"{where} CROSSWALK_TSC_POPULATING stands {outside} time(s) "
            "outside the reading-guide paragraph (each run of whitespace "
            "read as one space); it may stand only there, as form 1; "
            f"{accepted}"
        )
    return status


def parse_reverse_matrix(text):
    """The reverse framework control crosswalk, section by section.

    Returns ``{heading: {'area_label', 'rows'}}`` where each row is
    ``{'area','paths','alignment'}``. Only sections holding a three-column
    table whose second and third headers are exactly "Library documents" and
    "Alignment type" are instrument sections; a malformed row, a row citing
    no document, a second instrument table under a heading already read (a
    repeated section heading), or an interrupted table (a blank line inside
    it, or any stray table line after it closes) is a BuildError."""
    sections = {}
    heading = None
    current = None
    state = "outside"
    for line in text.splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
            current = None
            state = "outside"
            continue
        if heading is None or not line.strip().startswith("|"):
            state = "outside"
            continue
        cells = _xw_table_cells(line)
        if state == "outside" and current is not None:
            # Round-2 fix 4: inside an instrument section, a table line
            # after the table closed (a blank line inside the table, a
            # second table, or a stray row) must never be dropped silently.
            raise BuildError(
                f"crosswalk: reverse matrix table under '{heading}' is "
                "interrupted or carries an unexpected table line"
            )
        if (state == "outside" and len(cells) == 3
                and cells[1] == "Library documents"
                and cells[2] == "Alignment type"):
            if heading in sections:
                raise BuildError(
                    f"crosswalk: duplicate reverse matrix table under "
                    f"'{heading}'"
                )
            current = {"area_label": cells[0], "rows": []}
            sections[heading] = current
            state = "header"
            continue
        if state == "header":
            if not _xw_is_separator(cells):
                raise BuildError(
                    f"crosswalk: reverse matrix '{heading}' header not "
                    "followed by a separator row (schema change?)"
                )
            state = "rows"
            continue
        if state != "rows":
            continue
        if len(cells) != 3:
            raise BuildError(
                f"crosswalk: reverse matrix row under '{heading}' with "
                f"{len(cells)} cell(s) instead of 3"
            )
        paths = _xw_doc_paths(
            cells[1], f"reverse matrix row under '{heading}'"
        )
        if not paths:
            raise BuildError(
                f"crosswalk: reverse matrix row under '{heading}' cites no "
                f"parsable document path: {cells[0]!r}"
            )
        current["rows"].append({
            "area": cells[0],
            "paths": paths,
            "alignment": cells[2],
        })
    if not sections:
        raise BuildError(
            "crosswalk: reverse matrix parsed to zero instrument sections "
            "(schema change?)"
        )
    empty = sorted(h for h, s in sections.items() if not s["rows"])
    if empty:
        raise BuildError(
            "crosswalk: reverse matrix section(s) with zero rows: "
            + ", ".join(empty)
        )
    return sections


def _xw_split_identifiers(cell):
    """Split a compliance matrix cell into identifiers on top-level commas and
    semicolons (a separator inside parentheses, as in "Pillar II
    (Customs-to-Business; Standard 6)", does not split)."""
    parts = []
    depth = 0
    cur = []
    for ch in cell:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch in ",;" and depth == 0:
            part = "".join(cur).strip()
            if part:
                parts.append(part)
            cur = []
        else:
            cur.append(ch)
    part = "".join(cur).strip()
    if part:
        parts.append(part)
    return parts


def _xw_reverse_rows(inst, reverse_sections):
    """The reverse matrix rows feeding one instrument (the combined OWASP LLM
    Top 10 / MITRE ATLAS section splits by area-label prefix)."""
    if not inst.reverse_section:
        return []
    section = reverse_sections[inst.reverse_section]
    rows = section["rows"]
    if inst.reverse_filter:
        mode, prefix = inst.reverse_filter
        keep = (lambda a: a.startswith(prefix)) if mode == "include" \
            else (lambda a: not a.startswith(prefix))
        rows = [r for r in rows if keep(r["area"])]
    return rows


def build_crosswalk(full_docs):
    """Parse every crosswalk input and assemble the page model. Loud on every
    coupling breakage design C 3.5 names: an instrument register_id missing
    from the register, a main-table instrument absent from both matrices, an
    alias naming no configured instrument, a cited path missing from the
    taxonomy, and any schema change in a parsed source. The column presets
    are validated here too (crosswalk_presets), so a bad topic or instrument
    fails the build rather than the module import."""
    presets = crosswalk_presets()
    register = parse_citations_register(
        CITATIONS_REGISTER.read_text(encoding="utf-8")
    )
    comp_text = CROSSWALK_COMPLIANCE_MATRIX.read_text(encoding="utf-8")
    domains, comp_rows = parse_compliance_matrix(comp_text)
    tsc_populating = parse_compliance_tsc_status(comp_text)
    reverse_sections = parse_reverse_matrix(
        CROSSWALK_REVERSE_MATRIX.read_text(encoding="utf-8")
    )
    docs_by_path = {d["path"]: d for d in full_docs}

    bad_aliases = sorted(
        {key for key in CROSSWALK_ALIASES.values() if key not in CROSSWALK_BY_KEY}
        | {key for parts in CROSSWALK_ALIAS_PARTS.values() for _, key in parts
           if key is not None and key not in CROSSWALK_BY_KEY}
    )
    if bad_aliases:
        raise BuildError(
            "crosswalk: alias target(s) naming no configured instrument: "
            + ", ".join(bad_aliases)
        )
    for name, parts in CROSSWALK_ALIAS_PARTS.items():
        if name in CROSSWALK_ALIASES:
            raise BuildError(
                f"crosswalk: '{name}' is in both CROSSWALK_ALIASES and "
                "CROSSWALK_ALIAS_PARTS"
            )
        if " / ".join(part for part, _ in parts) != name:
            raise BuildError(
                f"crosswalk: the CROSSWALK_ALIAS_PARTS parts of '{name}' do "
                "not rejoin with ' / ' to the string"
            )
        if all(key is None for _, key in parts):
            raise BuildError(
                f"crosswalk: no CROSSWALK_ALIAS_PARTS part of '{name}' names "
                "a crosswalk instrument"
            )
    for anchor_path in (CROSSWALK_FORWARD_MATRIX_PATH,
                        CROSSWALK_COMPLIANCE_MATRIX_PATH,
                        CROSSWALK_REVERSE_MATRIX_PATH):
        if anchor_path not in docs_by_path:
            raise BuildError(
                f"crosswalk: matrix document {anchor_path} is not in the "
                "taxonomy (renamed or removed?)"
            )

    for domain in domains:
        for r in comp_rows[domain]:
            if r["path"] not in docs_by_path:
                raise BuildError(
                    f"crosswalk: compliance matrix cites {r['path']} which "
                    "is not in the taxonomy (renamed or removed?)"
                )
    # Every reverse matrix row's paths, for every instrument (round-2 fix 6:
    # instruments with a compliance column render reverse rows too, so a
    # stale path must fail the build here, never a KeyError at render).
    for heading, section in reverse_sections.items():
        for r in section["rows"]:
            for path in r["paths"]:
                if path not in docs_by_path:
                    raise BuildError(
                        f"crosswalk: reverse matrix row under '{heading}' "
                        f"cites {path} which is not in the taxonomy "
                        "(renamed or removed?)"
                    )

    # Taxonomy citations per instrument, through the committed alias map.
    citations = {inst.key: [] for inst in CROSSWALK_INSTRUMENTS}
    for d in full_docs:
        if d.get("domain") == ROOT_DOMAIN:
            continue
        keys = {key for f in d.get("frameworks", [])
                for key in crosswalk_alias_keys(f)}
        for key in keys:
            citations[key].append(d)
    for key in citations:
        citations[key].sort(key=lambda d: (d.get("title", "").lower(), d["path"]))

    instruments = {}
    for inst in CROSSWALK_INSTRUMENTS:
        row = None
        if inst.register_id is not None:
            row = register.get(inst.register_id)
            if row is None:
                raise BuildError(
                    f"crosswalk: instrument '{inst.key}' names Standard ID "
                    f"'{inst.register_id}' which the citations register does "
                    "not carry"
                )
        if inst.main_table and not inst.compliance_column \
                and not inst.reverse_section:
            raise BuildError(
                f"crosswalk: main-table instrument '{inst.key}' is absent "
                "from both matrices (no compliance column and no reverse "
                "section)"
            )
        if inst.reverse_section and inst.reverse_section not in reverse_sections:
            raise BuildError(
                f"crosswalk: instrument '{inst.key}' names reverse matrix "
                f"section '{inst.reverse_section}' which the matrix does not "
                "carry (renamed section or schema change?)"
            )
        if inst.compliance_column \
                and inst.compliance_column not in CROSSWALK_COMPLIANCE_COLUMNS:
            raise BuildError(
                f"crosswalk: instrument '{inst.key}' names compliance column "
                f"'{inst.compliance_column}' outside the pinned column set"
            )
        if inst.reverse_pointer is not None:
            target = CROSSWALK_BY_KEY.get(inst.reverse_pointer)
            if target is None or not target.reverse_section:
                raise BuildError(
                    f"crosswalk: instrument '{inst.key}' points its reverse "
                    f"coverage at '{inst.reverse_pointer}' which is no "
                    "configured instrument with a reverse matrix section"
                )
            if inst.reverse_section:
                raise BuildError(
                    f"crosswalk: instrument '{inst.key}' has both a reverse "
                    "matrix section and a reverse pointer"
                )
        if inst.version_join is not None and row is not None:
            version = row["version"]
            if inst.version_join == "colon":
                display = f"{inst.label}:{version}"
            elif inst.version_join == "paren":
                display = f"{inst.label} ({version})"
            else:
                display = f"{inst.label} {version}"
        else:
            display = inst.label

        # Per-domain cell data: identifiers and document lists, from the
        # compliance matrix column when one exists, else from the reverse
        # matrix's cited documents grouped by their path's domain.
        by_domain = {}
        # The compliance matrix column's rows and how many are N/A, so a
        # caveat about the column's N/A is generated from the matrix (batch 3
        # round 3 item 2).
        column_rows = column_na = 0
        if inst.compliance_column:
            for domain in domains:
                ids = []
                docs = []
                for r in comp_rows[domain]:
                    cell = r["cells"][inst.compliance_column]
                    if not cell:
                        raise BuildError(
                            f"crosswalk: empty compliance matrix cell for "
                            f"{r['path']} / {inst.compliance_column}"
                        )
                    column_rows += 1
                    if cell == "N/A":
                        column_na += 1
                        continue
                    for ident in _xw_split_identifiers(cell):
                        if ident not in ids:
                            ids.append(ident)
                    docs.append((r["path"], _xw_split_identifiers(cell)))
                if docs:
                    by_domain[domain] = {"ids": ids, "docs": docs}
        else:
            for r in _xw_reverse_rows(inst, reverse_sections):
                for path in r["paths"]:
                    domain = docs_by_path[path].get("domain", "")
                    entry = by_domain.setdefault(domain, {"ids": [], "docs": []})
                    if path not in [p for p, _ in entry["docs"]]:
                        entry["docs"].append((path, []))
        instruments[inst.key] = {
            "inst": inst,
            "display": display,
            "register": row,
            "by_domain": by_domain,
            "column_rows": column_rows,
            "column_na": column_na,
            "column_populating": (
                tsc_populating
                and inst.compliance_column == "AICPA TSC 2017"
            ),
            "reverse_rows": _xw_reverse_rows(inst, reverse_sections),
            "reverse_area_label": (
                reverse_sections[inst.reverse_section]["area_label"]
                if inst.reverse_section else None
            ),
            "citations": citations[inst.key],
        }

    return {
        "domains": domains,
        "instruments": instruments,
        "docs_by_path": docs_by_path,
        "presets": presets,
    }


def crosswalk_alias_warnings():
    """High-frequency taxonomy framework strings with no crosswalk alias
    (design C 3.5): surfaced by --check so a new instrument shows up instead
    of silently vanishing from the crosswalk. Advisory, never a failure."""
    full_docs = parse_taxonomy_full(TAXONOMY.read_text(encoding="utf-8"))
    counts = Counter(
        f for d in full_docs for f in d.get("frameworks", [])
    )
    return sorted(
        ((n, name) for name, n in counts.items()
         if n >= CROSSWALK_ALIAS_WARN_MIN and not crosswalk_alias_keys(name)),
        key=lambda item: (-item[0], item[1]),
    )


def _xw_doc_noun(count):
    return "document" if count == 1 else "documents"


def _xw_short_ids(ids):
    """The identifiers a matrix cell shows in code type (spec 7.30: cells
    hold short identifiers): the single-word ones. A phrase-length label (a
    trade programme's requirement area, a BASC clause named with its
    instrument) cannot sit in a nowrap matrix cell, so it stays on the
    instrument page, which lists every identifier and label in full."""
    return [ident for ident in ids if len(ident.split()) == 1]


def _xw_column_name(data):
    """A column header's name: the display name without the organization
    tag it opens with, since the tag shows beneath it (spec 7.30)."""
    display, org = data["display"], data["inst"].org
    if display.startswith(org + " "):
        return display[len(org) + 1:]
    return display


def render_crosswalk_table(xw, keys, matrix):
    """The domain-by-instrument table (design C 3.3) for the given instrument
    columns, in the spec 7.30 matrix markup: every instrument th and td
    carries its data-col key and the row-header column carries none, so
    matrix.js never hides it; a header is the name over its organization
    tag, and a cell holds its single-word identifiers in code type and a
    count link whose noun is visually hidden. Past the cap, "and more" is
    visually hidden too, and an empty cell holds only a visually hidden
    "no documents", as the reference page marks one, so the identifiers and
    the count link are a cell's only visible content. ``matrix`` marks the
    table data-matrix (the one matrix on the crosswalk page); a static
    view's table is the same markup without it, so no script acts there.
    No colgroup: a fixed column width would outlive the column matrix.js
    hides."""
    head = ['<th scope="col">Domain</th>']
    for key in keys:
        data = xw["instruments"][key]
        head.append(
            f'<th scope="col" data-col="{key}">'
            f'{_esc(_xw_column_name(data))}'
            f'<span class="org">{_esc(data["inst"].org)}</span></th>'
        )
    body = []
    for domain in xw["domains"]:
        cells = [
            f'<th scope="row"><a href="{{{{BASE}}}}/{_esc(domain)}/">'
            f'{_esc(draft_domain_label(domain))}</a></th>'
        ]
        for key in keys:
            data = xw["instruments"][key]
            entry = data["by_domain"].get(domain)
            if not entry:
                cells.append(
                    f'<td data-col="{key}"><span class="vh">no documents'
                    "</span></td>"
                )
                continue
            count = len(entry["docs"])
            link = (
                f'<a href="{{{{BASE}}}}/crosswalk/{key}/#{_esc(domain)}">'
                f'{count}<span class="vh"> {_xw_doc_noun(count)}</span></a>'
            )
            ids = _xw_short_ids(entry["ids"])
            if ids:
                shown = ids[:CROSSWALK_CELL_ID_CAP]
                # A plain space, outside the hidden tail, separates the codes
                # from the count link in every cell, capped or not, so read
                # aloud the last code or "and more" never runs into the
                # count's number ("A.622", "more22"; batch 3 round 2 NOTE).
                tail = (
                    '<span class="vh">, and more</span>'
                    if len(ids) > CROSSWALK_CELL_ID_CAP else ""
                )
                codes = ", ".join(f"<code>{_esc(i)}</code>" for i in shown)
                cells.append(f'<td data-col="{key}">{codes}{tail} {link}</td>')
            else:
                cells.append(f'<td data-col="{key}">{link}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    marker = " data-matrix" if matrix else ""
    noun = "instrument" if len(keys) == 1 else "instruments"
    # matrix.js hides columns on the crosswalk page, so its caption scopes
    # the count to the full table; a static view's columns never change.
    caption = (
        f"Corpus domains by instruments, {len(keys)} in the full table"
        if matrix else f"Corpus domains by {len(keys)} {noun}"
    )
    return (
        f'<table class="matrix sticky sticky-col"{marker}>\n'
        f'<caption class="vh">{caption}</caption>\n'
        "<thead><tr>" + "".join(head) + "</tr></thead>\n"
        "<tbody>\n" + "\n".join(body) + "\n</tbody>\n</table>"
    )


def _xw_names(xw, keys):
    """The columns' display names as a running-text list."""
    names = [_esc(xw["instruments"][k]["display"]) for k in keys]
    if len(names) < 3:
        return " and ".join(names)
    return ", ".join(names[:-1]) + ", and " + names[-1]


def _xw_table_intro(xw, keys, matrix):
    """The sentences under the table heading, derived from what the page's
    columns render, so each holds for every column it covers: the columns
    whose cells show a code are the compliance alignment matrix columns
    with a single-word identifier in some domain (_xw_short_ids), and they
    are named; the other matrix columns record phrase-length labels only and
    show the count alone; a column with no recorded mapping in any domain is
    empty throughout; and the remaining columns take their cells from the
    documents the reverse framework control crosswalk cites, with the count
    alone. On the crosswalk page (``matrix``) matrix.js hides columns, so
    the counts name the full table; a static view's counts name the columns
    here. The opening sentence says what every column is: an instrument the
    matrices carry, as a compliance alignment matrix column or in a reverse
    framework control crosswalk section (build_crosswalk refuses a
    main-table instrument with neither), not one they map, since a column
    can have no recorded mapping in any domain (AICPA TSC today). A
    one-column group is named directly ("the PIP column here"), never
    counted."""
    where = "of the full table" if matrix else "here"

    def columns(group):
        if len(group) == 1:
            return f"the {_xw_names(xw, group)} column {where}"
        return f"the {len(group)} columns {where} for {_xw_names(xw, group)}"

    data = xw["instruments"]
    unmapped = [k for k in keys if not data[k]["by_domain"]]
    comp = [k for k in keys if CROSSWALK_BY_KEY[k].compliance_column
            and k not in unmapped]
    codes = [k for k in comp
             if any(_xw_short_ids(e["ids"])
                    for e in data[k]["by_domain"].values())]
    labels = [k for k in comp if k not in codes]
    rest = [k for k in keys if k not in comp and k not in unmapped]
    parts = [
        "Rows are the corpus domains and columns are instruments the "
        "alignment matrices carry, each as a column of the compliance "
        "alignment matrix or in a section of the reverse framework control "
        "crosswalk. A cell with a recorded mapping carries a generated "
        "document count that opens the instrument page at that domain, and "
        "a cell with none is left empty."
    ]
    if codes:
        parts.append(
            f"In {columns(codes)}, a cell also shows, in code type, up to "
            f"{CROSSWALK_CELL_ID_CAP} of the single-word identifiers that the "
            "compliance alignment matrix records for its domain, where it "
            "records any, and the instrument page lists every identifier and "
            "label in full."
        )
    if labels:
        parts.append(
            f"In {columns(labels)}, the compliance alignment matrix records "
            "only phrase-length labels, so a cell shows the count alone and "
            "the instrument page lists the labels in full."
        )
    if unmapped:
        parts.append(
            f"No domain has a recorded mapping in {columns(unmapped)}, so "
            "every cell there is empty."
        )
    if rest:
        cites = (
            "cells from the documents the reverse framework control "
            "crosswalk cites, with the count alone, and the instrument page "
            "lists the control areas that crosswalk maps."
        )
        if len(rest) == len(keys):
            parts.append(f"Every column {where} takes its {cites}")
        elif len(rest) == 1:
            parts.append(
                f"The remaining {_xw_names(xw, rest)} column {where} takes "
                f"its {cites}")
        else:
            parts.append(
                f"The remaining {len(rest)} columns {where} take their {cites}")
    return " ".join(parts)


def _xw_matrix_link(xw, path):
    doc = xw["docs_by_path"][path]
    return (
        f'<a href="{_esc(_doc_page_url("{{BASE}}", path))}">'
        f'{_esc(doc.get("title", path))}</a>'
    )


def render_crosswalk_caveats(xw, keys=(), inst=None):
    """The "What this mapping is" block (design C 3.6): the matrices' own
    caveats, carried nearly verbatim, each attributed to its on-site source.
    The AICPA TSC caveat describes what the reader sees, an empty cell here
    for the matrix's N/A, so it renders only where the page's table has that
    column (``keys``, the table's columns; an instrument page has none)
    (batch 3 round 2 NOTE: since f2 no cell shows N/A, and the caveat sat on
    pages with no such column). A cell is empty where every row the matrix
    lists for its domain is N/A, and the matrix lists only some of a
    domain's documents, so the sentence names those rows (batch 3 round 3
    item 1). The AICPA TSC instrument page (``inst``) carries its own
    caveat, its N/A rows counted from the matrix, so it stays true as the
    column is filled (batch 3 round 3 item 2). It says the column is being
    populated, and keeps the matrix's condition on each N/A, only while the
    matrix itself says so (``column_populating``); once the matrix drops that
    sentence, an N/A there means no direct mapping, as in every other column,
    and no caveat of its own renders (batch 3 round 4 item 1). A view page
    says the column is being populated on the same parsed status, so view
    and instrument pages agree in every state (batch 3 round 5 item 2)."""
    tsc = ""
    col = next((k for k in keys
                if CROSSWALK_BY_KEY[k].compliance_column == "AICPA TSC 2017"),
               None)
    if col is not None:
        if xw["instruments"][col]["column_populating"]:
            tsc = (
                " Its AICPA TSC 2017 column is being populated domain by "
                "domain: until a document's Trust Services Criteria mapping "
                "has been assessed, its N/A in that column records that no "
                "mapping has been made yet and does not assert that no "
                "criterion applies."
            )
        tsc += (
            " The table here leaves an AICPA TSC cell empty where every "
            "document the matrix lists for the domain has N/A in that column."
        )
    elif inst is not None and inst.compliance_column == "AICPA TSC 2017":
        data = xw["instruments"][inst.key]
        rows, na = data["column_rows"], data["column_na"]
        if na and na == rows:
            held = (
                "its one row is" if rows == 1 else
                f"every one of its {rows} rows is"
            )
        elif na:
            held = f"{na} of its {rows} rows {'is' if na == 1 else 'are'}"
        else:
            held = (
                "its one row is not" if rows == 1 else
                f"none of its {rows} rows is"
            )
        if data["column_populating"]:
            tsc = (
                " Its AICPA TSC 2017 column is being populated domain by "
                f"domain: {held} N/A in that column today; until a row's "
                "Trust Services Criteria mapping has been assessed, its N/A "
                "in that column records that no mapping has been made yet "
                "and does not assert that no criterion applies."
            )
    return "\n".join((
        "<p>From the " + _xw_matrix_link(xw, CROSSWALK_COMPLIANCE_MATRIX_PATH)
        + ": citations are indicative, not exhaustive (the "
        "representative-citation convention), and no entry constitutes a "
        f"certification, attestation, or legal opinion.{tsc}</p>",
        "<p>From the " + _xw_matrix_link(xw, CROSSWALK_REVERSE_MATRIX_PATH)
        + ": coverage is partial, and external control identifiers and "
        "clause numbers are referenced for navigation only; the library does "
        "not reproduce third-party control text.</p>",
        "<p>From the " + _xw_matrix_link(xw, CROSSWALK_FORWARD_MATRIX_PATH)
        + ": the alignment is not an official mapping, certification claim, "
        "legal opinion, or reproduction of third-party framework "
        "content.</p>",
    ))


def render_crosswalk_rail(xw, current=None, matrix=False):
    """The crosswalk side list (spec 7.32; maintainer direction 2026-11-03
    15:06Z and 15:09Z: one side rail, on the left, which the right rail
    stood in for until the template carried it): the Views list, All plus
    one preset per topic view, then every instrument under its group,
    the "Also in the corpus" instruments included, each linking its page.
    On the crosswalk page (``matrix``) each view carries its matrix.js
    preset keys and id (spec 7.30); every view stays a link to the page that
    shows it without script, and the current page's view is marked."""

    def view(href, keys, slug, label, here):
        attrs = ' aria-current="page"' if here else ""
        if matrix:
            attrs += f' data-preset="{" ".join(keys)}" data-preset-id="{slug}"'
        return f'<li><a href="{href}"{attrs}>{_esc(label)}</a></li>'

    views = [view("{{BASE}}/crosswalk/", (), CROSSWALK_ALL_ID, "All",
                  current is None)]
    for preset in xw["presets"]:
        views.append(view(
            f"{{{{BASE}}}}/crosswalk/view/{preset.slug}/", preset.columns,
            preset.slug, preset.label, current == preset.slug,
        ))
    parts = ['<p class="lbl">Views</p><ul>\n' + "\n".join(views) + "\n</ul>"]
    for group in CROSSWALK_RAIL_GROUPS:
        keys = [i.key for i in CROSSWALK_INSTRUMENTS if i.group == group]
        if not keys:
            continue
        parts.append(
            f'<p class="lbl">{_esc(group)}</p><ul>\n'
            + "\n".join(
                f'<li><a href="{{{{BASE}}}}/crosswalk/{key}/">'
                f'{_esc(xw["instruments"][key]["display"])}</a></li>'
                for key in keys
            )
            + "\n</ul>"
        )
    return "\n".join(parts)


def _xw_views_intro(xw, preset):
    """The sentences about the side list, true for every item they cover and
    derived from the topics: each preset is one topic's columns
    (crosswalk_presets, which also puts every column in a topic), All opens
    the full table and each topic view a page of its columns, the row-header
    column carries no data-col, the clauses on topics spanning groups and
    columns shared between topics appear only while some topic does so, the
    Views list holds only All and the topic views while the group lists
    below it hold the instruments, and every instrument outside the column
    groups is an "Also in the corpus" page with no column."""
    if preset is not None:
        return (
            "The Views list opens the other views, All among them, and the "
            "group lists below it name every instrument under its group, "
            "each linking its instrument page."
        )
    presets = xw["presets"]
    group_of = {i.key: i.group for i in CROSSWALK_INSTRUMENTS}
    spans = [p for p in presets
             if len({group_of[k] for k in p.columns}) > 1]
    seen = [k for p in presets for k in p.columns]
    shared = sorted({k for k in seen if seen.count(k) > 1})
    related = [p for p in presets if p.related]
    text = (
        f"Each of the {len(presets)} topic views in the Views list "
        "shows the columns for one topic, and All shows every column; every "
        "column is in at least one topic, and the Domain column shows in "
        "every view."
    )
    if spans and shared:
        text += (
            " A topic can take columns from more than one instrument group, "
            "and a column can sit in more than one topic."
        )
    elif spans:
        text += (
            " A topic can take columns from more than one instrument group."
        )
    elif shared:
        text += " A column can sit in more than one topic."
    text += (
        " Without script every column shows here, All is a link to this full "
        "table, and each topic view is a link to a page with that topic's "
        "columns only"
    )
    text += (
        ", which also links the topic's related instrument pages where it "
        "has any." if related else "."
    )
    also = [i for i in CROSSWALK_INSTRUMENTS if i.group == _XW_G_ALSO]
    text += (
        " Below the Views list, the group lists name every instrument under "
        "its group, each linking its instrument page"
    )
    if len(also) == 1:
        text += (
            f"; the 1 under {_XW_G_ALSO} has a page and no column until a "
            "matrix carries it."
        )
    elif also:
        text += (
            f"; the {len(also)} under {_XW_G_ALSO} have a page and no column "
            "until a matrix carries them."
        )
    else:
        text += "."
    return text


def draft_crosswalk_values(xw, preset=None):
    """Per-page values for the crosswalk table page: the full table when
    ``preset`` is None, as the page's one matrix with matrix.js and its
    status line (spec 7.30), else that preset's columns only, the static view
    its preset link opens without script (design C 3.7)."""
    main_keys = [i.key for i in CROSSWALK_INSTRUMENTS if i.main_table]
    if preset is None:
        keys = main_keys
        title = "Crosswalk"
        heading = "The crosswalk"
        meta = (
            f"{len(main_keys)} instruments across {len(xw['domains'])} "
            "domains in the full table, every cell generated from the corpus "
            "alignment matrices at build time."
        )
        label = f"The full table, {len(keys)} instruments"
        lead = (
            "Where the corpus maps to the standards, laws, frameworks, and "
            "programmes it cites. Every row, column, cell, and count is "
            "generated from the compliance alignment matrix, the reverse "
            "framework control crosswalk, the canonical citations register, "
            "and the taxonomy."
        )
        below = ""
        next_url = "{{BASE}}/browse/"
        next_label = "Browse by need, domain, or type"
    else:
        # The view's columns in the full table's order, so the static page
        # and the scripted view (matrix.js hides, never reorders) agree.
        keys = [k for k in main_keys if k in preset.columns]
        title = f"Crosswalk: {preset.label}"
        heading = f"Crosswalk: {preset.label}"
        meta = (
            f"A topic view showing {len(keys)} of the crosswalk's "
            f"{len(main_keys)} instrument columns."
        )
        lead = (
            f"The {preset.label} view of the crosswalk: the same generated "
            "table, restricted to its columns. The All link opens every "
            "instrument column."
        )
        label = (f"This view, {len(keys)} "
                 f"{'instrument' if len(keys) == 1 else 'instruments'}")
        below = ""
        if preset.related:
            below = (
                '<p class="lbl blk">Related instrument pages</p>'
                '<ul class="chips">' + "".join(
                    f'<li><a href="{{{{BASE}}}}/crosswalk/{key}/">'
                    f'{_esc(xw["instruments"][key]["display"])}</a></li>'
                    for key in preset.related
                ) + "</ul>"
            )
        next_url = "{{BASE}}/crosswalk/"
        next_label = "Open the full crosswalk"
    matrix = preset is None
    return {
        **_draft_nav("crosswalk"),
        "XW_TITLE": _esc(title),
        "XW_HEADING": _esc(heading),
        "XW_META": meta,
        "XW_LEAD": lead,
        "XW_SCRIPT": (
            '<script src="{{BASE}}/assets/baseline/matrix.js" defer></script>'
            if matrix else ""
        ),
        "XW_RAIL": render_crosswalk_rail(
            xw, preset.slug if preset else None, matrix),
        "XW_TABLE_CAPTION": label,
        "XW_TABLE_INTRO": _xw_table_intro(xw, keys, matrix),
        "XW_VIEWS_INTRO": _xw_views_intro(xw, preset),
        "XW_STATUS": (
            '<p class="matrix-status" role="status" aria-live="polite" '
            "data-matrix-status></p>" if matrix else ""
        ),
        "XW_TABLE": render_crosswalk_table(xw, keys, matrix),
        "XW_BELOW": below,
        "XW_CAVEATS": render_crosswalk_caveats(xw, keys),
        "XW_NEXT_URL": next_url,
        "XW_NEXT_LABEL": next_label,
    }


def _xw_register_block(inst, row):
    """The instrument page's register record (design C 3.4): the canonical
    citation row, staleness visible; or, for the two programmes the register
    carries no row for, the compliance matrix's own column key naming."""
    if row is None:
        return (
            "<p>The canonical citations register carries no row for this "
            "programme; its name and scope come from the compliance "
            "alignment matrix's own column key.</p>"
        )
    if row["upstream"] == "-":
        upstream = "none recorded"
    else:
        upstream = (
            f'<a href="{_esc(row["upstream"])}" target="_blank" '
            'rel="noopener noreferrer">'
            f'{_draft_wrapping_path(row["upstream"])}{_DRAFT_NEW_TAB}</a>'
        )
    fields = (
        ("Standard ID", _esc(row["id"])),
        ("Current version", _esc(row["version"])),
        ("Publication date", _esc(row["date"])),
        ("Topic", _esc(row["topic"])),
        ("Upstream check location", upstream),
        ("Last verified (UTC)", _esc(row["verified"])),
    )
    rows = "\n".join(
        f"<dt>{label}</dt><dd>{value}</dd>" for label, value in fields
    )
    return f'<dl class="record side">\n{rows}\n</dl>'


def draft_crosswalk_instrument_values(xw, inst):
    """Per-page values for one instrument page at crosswalk/<slug>/ (design C
    3.4): register record, reverse matrix section, per-domain coverage (the
    main table's anchor targets), and the taxonomy citation list."""
    data = xw["instruments"][inst.key]
    docs_by_path = xw["docs_by_path"]
    sections = []

    rows = data["reverse_rows"]
    if rows:
        body = []
        for r in rows:
            links = ", ".join(
                _xw_matrix_link(xw, p) for p in r["paths"]
            )
            body.append(
                f"<tr><td>{_esc(r['area'])}</td><td>{links}</td>"
                f"<td>{_esc(r['alignment'])}</td></tr>"
            )
        sections.append(
            f'<p class="lbl sec">Mapped control areas, {len(rows)}</p>\n'
            '<h2 id="control-areas">Control areas from the reverse '
            "crosswalk</h2>\n"
            "<p>From the "
            + _xw_matrix_link(xw, CROSSWALK_REVERSE_MATRIX_PATH)
            + ", which answers: given a control identifier or family, which "
            "documents address it.</p>\n"
            '<div class="wide"><div class="tablewrap" tabindex="0">'
            '<table class="fixed">'
            '<colgroup><col class="w30"><col class="w50"><col class="w20">'
            "</colgroup>"
            f'<thead><tr><th scope="col">{_esc(data["reverse_area_label"])}'
            '</th><th scope="col">Library documents</th>'
            '<th scope="col">Alignment type</th></tr></thead>\n<tbody>\n'
            + "\n".join(body) + "\n</tbody></table></div></div>"
        )

    if inst.reverse_pointer:
        # The combined trade section's rows all carry CTPAT MSC domain area
        # labels, so the table renders once, on the pointer target's page;
        # the programmes the section names point there (round-2 fix 5).
        target = xw["instruments"][inst.reverse_pointer]
        sections.append(
            '<p class="lbl sec">Reverse crosswalk</p>\n'
            '<h2 id="reverse-crosswalk">Control areas from the reverse '
            "crosswalk</h2>\n"
            "<p>The "
            + _xw_matrix_link(xw, CROSSWALK_REVERSE_MATRIX_PATH)
            + " names this programme in its combined section &quot;"
            + _esc(target["inst"].reverse_section)
            + "&quot;; its control-area table is rendered on the "
            f'<a href="{{{{BASE}}}}/crosswalk/{inst.reverse_pointer}/'
            '#control-areas">'
            f'{_esc(target["display"])}</a> instrument page.</p>'
        )

    by_domain = data["by_domain"]
    if by_domain:
        source_path = (
            CROSSWALK_COMPLIANCE_MATRIX_PATH if inst.compliance_column
            else CROSSWALK_REVERSE_MATRIX_PATH
        )
        parts = [
            f'<p class="lbl sec">Coverage, {len(by_domain)} '
            f'{"domain" if len(by_domain) == 1 else "domains"}</p>',
            '<h2 id="by-domain">Coverage by domain</h2>',
            "<p>From the " + _xw_matrix_link(xw, source_path)
            + "; the main crosswalk table's document counts land here.</p>",
        ]
        for domain in xw["domains"]:
            entry = by_domain.get(domain)
            if not entry:
                continue
            items = []
            for path, ids in entry["docs"]:
                doc = docs_by_path[path]
                # The identifiers sit in the row's wrapping <small> line:
                # .plan li .n is nowrap in a minmax(0, 1fr) auto grid, so a
                # list of up to 140 characters there widened the page past
                # 320, 360 and 390 px (item 3b788, as on the concern rows).
                tail = (
                    f'<small>{_esc(", ".join(ids))}</small>'
                    if ids else
                    f'<span class="n">{_esc(doc.get("type", "").lower())}</span>'
                )
                items.append(
                    f'<li><a href="{_esc(_doc_page_url("{{BASE}}", path))}">'
                    f'{_esc(doc.get("title", path))}</a>{tail}</li>'
                )
            parts.append(
                f'<h3 id="{_esc(domain)}">'
                f'{_esc(draft_domain_label(domain))}, {len(items)} '
                f"{_xw_doc_noun(len(items))}</h3>\n"
                '<div class="wide"><ul class="plan one">\n'
                + "\n".join(items) + "\n</ul></div>"
            )
        sections.append("\n".join(parts))

    cited = data["citations"]
    if cited:
        items = "\n".join(
            f'<li><a href="{_esc(_doc_page_url("{{BASE}}", d["path"]))}">'
            f'{_esc(d.get("title", d["path"]))}</a>'
            f'<span class="n">{_esc(draft_domain_label(d.get("domain", "")))}'
            "</span></li>"
            for d in cited
        )
        sections.append(
            f'<p class="lbl sec">Corpus citations, {len(cited)}</p>\n'
            '<h2 id="citations">Documents naming it in their framework '
            "alignment</h2>\n"
            "<p>Generated from each document's framework alignment list in "
            "the taxonomy, through the committed alias map.</p>\n"
            '<div class="wide"><ul class="plan one">\n'
            + items + "\n</ul></div>"
        )
    else:
        sections.append(
            '<h2 id="citations">Documents naming it in their framework '
            "alignment</h2>\n"
            "<p>No document's framework alignment list names this instrument "
            "under the committed aliases.</p>"
        )

    row = data["register"]
    if row is not None:
        # The lead carries the instrument's descriptive name alone; the full
        # Topic cell stays on the register record (round-2 fix 1).
        lead_tail = _xw_topic_name(row["topic"]) or row["topic"]
    else:
        lead_tail = (
            "a trade-security programme the compliance alignment matrix "
            "maps column by column"
        )
    return {
        **_draft_nav("crosswalk"),
        "XWI_TITLE": _esc(f"{data['display']} crosswalk"),
        "XWI_HEADING": _esc(data["display"]),
        "XWI_META": _esc(inst.group) + ".",
        "XWI_LEAD": _esc(
            f"Where the corpus maps to {data['display']}: {lead_tail}."
        ),
        "XWI_REGISTER": _xw_register_block(inst, row),
        "XWI_SECTIONS": "\n".join(sections),
        "XW_CAVEATS": render_crosswalk_caveats(xw, inst=inst),
    }


def render_draft_variant(figures, variant):
    """Render the whole /draft tree: the fixed pages, one page per corpus
    domain, one page per document type, one page per non-root corpus
    document, one page per docs/ adopter document (site a9), with
    narrative_routes the narrative subtype indexes and the
    reading room, and the pin-verified
    baseline asset copy (bytes), whose palettes.css must pass the pinned
    palette gate. Every HTML page passes the refusal guard, and
    the draft figure values get the same dead-value check as the live trees."""
    template_dir = template_dir_for(variant)
    partials = load_partials(template_dir)
    full_docs = parse_taxonomy_full(TAXONOMY.read_text(encoding="utf-8"))
    docs_by_path = {d["path"]: d for d in full_docs}
    if DRAFT_EXAMPLE_DOC not in docs_by_path:
        raise BuildError(
            f"draft: example document {DRAFT_EXAMPLE_DOC} is not in the "
            "taxonomy (renamed or removed?)"
        )
    # Browse and the documents index call every root document a library
    # specification ("plus N library specifications"), so a root document of
    # any other type fails the build instead of publishing a false sentence
    # (site a9 round-4 note 3).
    for d in full_docs:
        if d.get("domain") == ROOT_DOMAIN \
                and d.get("type") != "Specification":
            raise BuildError(
                f"draft: root document {d['path']} has type "
                f"'{d.get('type', '')}', not Specification (the browse page "
                "and the documents index call every root document a library "
                "specification)"
            )
    # The docs/ adopter documents (site a9): rendered and listed beside the
    # corpus documents, each from its own metadata record. The merged lookup
    # lets a Related Documents entry or a govern artefact link naming a docs/
    # file resolve to its on-site page instead of a GitHub fallback link.
    adopter_docs = parse_adopter_docs()
    # Each adopter document is listed on its type's page, so an adopter type
    # no taxonomy document carries (no type page) fails the build instead of
    # leaving the document on no type page.
    page_types = {tp["type"] for tp in figures["type_pages"]}
    for g in adopter_docs:
        if g["type"] not in page_types:
            raise BuildError(
                f"draft: adopter doc {g['path']} has document type "
                f"'{g['type']}', which has no type page (no taxonomy "
                "document carries it)"
            )
    pages_by_path = {**docs_by_path,
                     **{g["path"]: g for g in adopter_docs}}
    crosswalk = build_crosswalk(full_docs)
    # The adventure's need pages, the decide hub and the Browse executive
    # block share one validated concern join and one subtype table, resolved
    # before the fixed pages render so every branch target is checked first.
    for narrative_type in sorted(
        {p["narrative_type"] for p in figures["narratives"]}
    ):
        draft_narrative_subtype(narrative_type)
    concerns = draft_concern_join(figures, docs_by_path)
    pages = []
    used = set()

    def emit(template_name, out_rel, extra):
        html, used_keys = render_page(
            template_name, figures, variant, template_dir, partials,
            extra=extra, out_rel=out_rel,
        )
        refuse_draft_page(out_rel, html)
        pages.append((out_rel, html))
        used.update(used_keys)

    fixed_extras = {
        "landing.html": lambda: draft_landing_values(figures),
        "browse.html": lambda: draft_browse_values(figures, adopter_docs),
        "search.html": lambda: draft_search_values(full_docs, adopter_docs),
        "documents.html": lambda: draft_documents_values(full_docs),
        "crosswalk.html": lambda: draft_crosswalk_values(crosswalk),
        "govern.html": lambda: draft_govern_values(
            figures, pages_by_path, concerns),
        "comply.html": lambda: draft_comply_values(
            figures, docs_by_path, crosswalk),
        "solutions.html": lambda: draft_solutions_values(figures, concerns),
        "policies.html": lambda: draft_policies_values(figures),
        # Static template prose carried over from the old root at promotion
        # (maintainer decisions 2026-11-04): the Contributors page and the
        # For-AI page. Neither belongs to a top-bar section.
        "contributors.html": _draft_nav,
        "for-ai.html": _draft_nav,
        # Rendered after every other page (below), so its evidence lists
        # the scripts the draft actually loads.
        "disclosure.html": None,
        "license.html": draft_license_values,
        "404.html": _draft_nav,
    }
    disclosure_at = None
    for template_name, out_rel in variant.pages or ():
        if template_name not in fixed_extras:
            raise BuildError(
                f"draft: no extras builder for fixed page {template_name}"
            )
        if fixed_extras[template_name] is None:
            disclosure_at = (len(pages), template_name, out_rel)
            continue
        emit(template_name, out_rel, fixed_extras[template_name]())

    domain_seq = figures["domain_pages"]
    for idx, dp in enumerate(domain_seq):
        if idx + 1 < len(domain_seq):
            nxt = domain_seq[idx + 1]["domain"]
            next_url = "{{BASE}}/" + nxt + "/"
            next_label = "Open a domain: " + _esc(draft_domain_label(nxt))
        else:
            next_url = _doc_page_url("{{BASE}}", DRAFT_EXAMPLE_DOC)
            next_label = "Open a document: " + _esc(
                docs_by_path[DRAFT_EXAMPLE_DOC].get("title", DRAFT_EXAMPLE_DOC)
            )
        emit(
            "domain.html", f"{dp['domain']}/index.html",
            draft_domain_values(dp, docs_by_path, next_url, next_label,
                                leadership=variant.narrative_routes),
        )

    # One page per document type (/types/<slug>/, the route the other
    # variants' type pages use), chained by Next like the domain pages; the
    # Browse "By type" entries link here, and each page links its type's
    # facet address on All Documents.
    type_seq = figures["type_pages"]
    for idx, tp in enumerate(type_seq):
        if idx + 1 < len(type_seq):
            nxt = type_seq[idx + 1]
            next_url = "{{BASE}}/types/" + nxt["slug"] + "/"
            next_label = "Open a type: " + _esc(draft_type_plural(nxt["type"]))
        else:
            next_url = "{{BASE}}/browse/"
            next_label = "Browse by need, domain, or type"
        emit(
            "type.html", f"types/{tp['slug']}/index.html",
            draft_type_values(tp, docs_by_path, next_url, next_label,
                              [g for g in adopter_docs
                               if g["type"] == tp["type"]]),
        )

    for d in full_docs:
        if d.get("domain") == ROOT_DOMAIN:
            continue
        emit(
            "document.html", _doc_route_rel(d["path"]),
            draft_document_values(d, pages_by_path),
        )

    for g in adopter_docs:
        emit(
            "document.html", _doc_route_rel(g["path"]),
            draft_document_values(g, pages_by_path),
        )

    # The executive layer (design D items D1 and D3, sections 4.1 and 5),
    # VARIANT-SCOPED by narrative_routes like the live staging trees: the
    # decide hub at decide/, one concern topic page per DRAFT_CONCERNS entry
    # at decide/<concern>/, one generated index per narrative type at
    # decide/<slug>/, then the reading room at decisions/<subtype>/<slug>/ on
    # the baseline shell, each page under the refusal guard like every other
    # draft page.
    if variant.narrative_routes:
        emit(
            "decide.html", "decide/index.html",
            draft_decide_values(figures, concerns),
        )
        for concern in concerns:
            emit(
                "concern.html", f"decide/{concern['slug']}/index.html",
                draft_concern_values(concern),
            )
        for narrative_type, (slug, _, _) in DRAFT_NARRATIVE_SUBTYPES.items():
            emit(
                "subtype.html", f"decide/{slug}/index.html",
                draft_subtype_values(figures, narrative_type),
            )
        seen_out_rels = {out_rel for out_rel, _ in pages}
        for page, out_rel, body_html, toc in narrative_route_bodies(
            figures, variant, seen_out_rels
        ):
            emit(
                "narrative.html", out_rel,
                draft_narrative_values(page, body_html, toc),
            )

    # The crosswalk preset views and instrument pages (design C 3.4 and 3.7):
    # one static page per preset (one per topic view), each the same
    # generated table restricted to its columns and the page its matrix.js
    # preset link opens without script, and one page per configured
    # instrument.
    for preset in crosswalk["presets"]:
        emit(
            "crosswalk.html", f"crosswalk/view/{preset.slug}/index.html",
            draft_crosswalk_values(crosswalk, preset),
        )
    for inst in CROSSWALK_INSTRUMENTS:
        emit(
            "crosswalk-instrument.html", f"crosswalk/{inst.key}/index.html",
            draft_crosswalk_instrument_values(crosswalk, inst),
        )

    if disclosure_at is not None:
        # The scripts a page loads come from its head, never from the
        # evidence list, so one draft render of the disclosure page tells
        # what it loads itself; the page then keeps its place in the order.
        slot, template_name, out_rel = disclosure_at
        prefix = site_prefix_for(variant) + "/assets/baseline/"
        own, _ = render_page(
            template_name, figures, variant, template_dir, partials,
            extra=draft_disclosure_values([]), out_rel=out_rel,
        )
        scripts = draft_loaded_scripts(
            [html for _, html in pages] + [own], prefix,
        )
        emit(template_name, out_rel, draft_disclosure_values(scripts))
        pages.insert(slot, pages.pop())

    unused = sorted(
        (set(PARTIALS) | set(figure_values(figures, variant))) - used
    )
    if unused:
        raise BuildError(
            "draft value(s) used by no page (dead computation or a dropped "
            "placeholder): " + ", ".join("{{" + k + "}}" for k in unused)
        )

    assets = load_baseline_assets()
    # The palette gate runs after the pin check, so it judges the bytes the
    # draft serves (spec section 4 item 3: mandatory on every site).
    run_palette_gate()
    for rel, data in assets:
        pages.append((f"assets/baseline/{rel}", data))
    return pages


def render_variant(figures, variant):
    """Render one variant's HTML template tree and return relative outputs.

    Every variant in the promoted table renders through render_draft_variant
    (the plain-template machinery left with the old root and the v2/v3
    staging trees at the draft-site promotion); a non-draft-rules row is a
    table error, surfaced loudly here."""
    if variant.draft_rules:
        return render_draft_variant(figures, variant)
    raise BuildError(
        f"variant {variant.name} has no renderer: the plain-template "
        "machinery was removed at the draft-site promotion (every variant "
        "must set draft_rules)"
    )


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
            # Only rendered .html pages belong in the sitemap: the variant's
            # output also carries the copied baseline assets (fonts, CSS, JS,
            # logos, licence texts), which are not pages (round-2 fix 1), and
            # the error page is served for missing paths and must never be
            # crawled, so it stays out of the sitemap's page list.
            html_page_rels = [
                out_rel for out_rel, _ in variant_pages
                if out_rel.endswith(".html") and out_rel != "404.html"
            ]
            pages.append((output_rel_for(variant, "robots.txt"), render_robots_txt()))
            pages.append((
                output_rel_for(variant, "sitemap.xml"),
                render_sitemap(variant, html_page_rels),
            ))
            pages.append((
                output_rel_for(variant, "llms.txt"), render_llms_txt(figures, variant),
            ))
            # The Pages header and redirect rules and the RFC 9116
            # security.txt, emitted once each, at the output root alone (the
            # sole indexable variant has the empty prefix, so none lands
            # under a staging tree).
            pages.append((output_rel_for(variant, "_headers"), render_headers_file()))
            pages.append((output_rel_for(variant, "_redirects"), REDIRECTS_FILE))
            pages.append((
                output_rel_for(variant, ".well-known/security.txt"), SECURITY_TXT,
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
    ("templates-draft/for-ai.html", "for-ai"),
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
    # The international AI-governance rows the For-AI pages name by their Standard IDs
    # (backlog 2.25.2), each credited to the register as the OECD entry is.
    "UNESCO Recommendation on the Ethics of AI": frozenset({"Cited in the canonical citations register."}),
    "G7 Hiroshima Process International Code of Conduct": frozenset({
        "Cited in the canonical citations register.",
    }),
    "Council of Europe Framework Convention on AI": frozenset({"Cited in the canonical citations register."}),
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
    # Added by backlog 2.25.2 (the names of three register rows, so not unchecked).
    "UNESCO Recommendation on the Ethics of AI": frozenset({"(adopted 23 November 2021)."}),
    "G7 Hiroshima Process International Code of Conduct": frozenset({"(30 October 2023)."}),
    "Council of Europe Framework Convention on AI": frozenset({"(CETS No. 225)."}),
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
    """Template HTML as text: the external-link markers (``EXT_LINK_MARKER``
    and the draft new-tab hint ``_DRAFT_NEW_TAB``, each exactly as written)
    and tags dropped, entities decoded. The text of any other "ext" or "vh"
    span is kept."""
    fragment = fragment.replace(EXT_LINK_MARKER, "")
    fragment = fragment.replace(_DRAFT_NEW_TAB, "")
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
        description="Render the grclibrary.ai public site (the promoted baseline-template tree: the fixed pages, per-domain, per-type and per-document pages, the decide hub and concern pages, the decisions/<subtype>/<slug>/ executive reading-room pages, and the crosswalk views and instrument pages) from the live corpus.",
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
        manifest_text = render_corpus_link_manifest(
            figures, indexable_variant(), pages
        )
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
        # Advisory crosswalk coverage list (design C 3.5): a high-frequency
        # taxonomy framework string with no alias surfaces here so a new
        # instrument shows up instead of silently vanishing from the
        # crosswalk. A warning, never a failure.
        for count, name in crosswalk_alias_warnings():
            print(
                f"web-generator --check WARN: taxonomy framework string "
                f"'{name}' ({count} documents) has no crosswalk alias (add "
                "one to CROSSWALK_ALIASES in .web/build.py if it is an "
                "instrument the crosswalk should carry).",
                file=sys.stderr,
            )
        print(f"web-generator --check OK: corpus parses and every page renders. {summary}")
        return 0

    out_dir = Path(args.out).resolve() if args.out else DEFAULT_OUT
    written = []
    for out_rel, html in pages:
        out_file = out_dir / out_rel
        out_file.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(html, bytes):
            # The draft tree's baseline asset copy (fonts and PNGs included)
            # is byte content; pin-verified in load_baseline_assets.
            out_file.write_bytes(html)
        else:
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
