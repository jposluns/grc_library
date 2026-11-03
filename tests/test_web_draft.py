#!/usr/bin/env python3
"""The /draft tree (PR 2b): the grclibrary.ai rebuild on the shared family
site template (baseline 1.6.0).

What is locked here, each test failing without its feature:

1. Frozen root: the draft variant adds pages only under ``draft/`` and changes
   no other output byte, except the one sanctioned ``_headers`` appendix (the
   ``/draft/*`` block); the discovery files never mention the draft.
2. Page hygiene: every draft page is noindex with a self-canonical under
   /draft/, carries the baseline head order and the favicon and touch-icon
   links, resolves every internal reference inside the draft tree or its
   copied assets, and marks every external link as opening in a new tab.
3. The top bar is exactly Browse, Domains, Types, Search, GitHub (GitHub
   last); the landing page's About line carries Disclosure, Licence, Privacy,
   Security; no other draft page links the Disclosure or Licence pages, and
   the approved value paragraph keeps its words with no link.
4. The draft refusal guard rejects an en or em dash (literal or
   entity-encoded), inline style or script, an ``on*`` attribute, and "what
   this is" framing, and is draft-scoped (the live trees keep their inline
   partials).
5. Every count shown on the draft equals a value recomputed from
   ``taxonomy.yml``.
6. The baseline asset copy matches ``.web/baseline/`` byte for byte and every
   file's SHA-256 matches ``.baseline/pin.toml``; a tampered byte, a missing
   pinned file, an unpinned extra and a key outside the tree each fail the
   build. Gate 110 passes on the vendored tree, the pinned scripts are the
   release's whole script set (spec section 8), ``matrix.js`` loads exactly
   on a page with a matrix (proved on fixtures too), every ``.sticky`` table
   sits in a bounded scroll box (spec section 7.31), and the licence page
   names the pin's version, which no template types (spec section 11). The
   served stylesheet carries the 1.5.1 rule that content with the hidden
   attribute is never displayed (spec section 10), and the served template
   notice names no template version or script count the pin contradicts. The
   disclosure page's data-handling claim matches the scripts the pages load,
   including the query search.js writes into the page address and who
   receives or can read that address, and its evidence links every script
   the rendered draft pages load.
7. ``_headers`` is PR 1's ``/*`` rule byte for byte plus exactly the decided
   ``/draft/*`` block (the spec section 9 CSP, the ``!`` detach line and
   ``X-Robots-Tag: noindex``), with no zone-owned header name.
8. Every taxonomy type has exactly one draft type page carrying its
   TYPE_SCOPE line and every document of the type, with area and purpose;
   the Browse "By type" entries link those pages; the page's prose about its
   rows holds for every row and every row's rendered document page.
9. The documents index (design A PR A3), named All Documents: one row per
   non-root taxonomy path in title order, each carrying the search page's
   data-search text, wired the way search.js expects; area and type chips
   link the domain pages and the design A type routes, each type chip
   counting the corpus list its type page shows; the root specifications
   open on GitHub under the one area label the type pages give them; every
   document page's Next and the Browse page lead to the index; the index
   and Browse prose about the list holds for the rendered rows.
10. The executive layer (design D items D1 and D3, section 4.1 branch 2):
   every narrative registry page renders at
   ``/draft/decisions/<subtype>/<slug>/`` on the baseline shell; each of the
   six ``/draft/decide/<subtype-plural>/`` indexes lists exactly the pages of
   its narrative type; each domain page's leadership section matches the
   registry join; every count these pages show equals the registry's; every
   page of the three types carries the layer's authority qualifier whole;
   and a narrative type with no subtype index fails the build.
11. The executive path hub and the concern topic pages (design D sections 4.1
   branches 1 and 3, and 5): ``/draft/decide/`` groups every concern under the
   three board questions with two generated counts per row and carries the
   subtype-index and By domain branches; each ``/draft/decide/<concern>/``
   page's leadership list equals its registry join, its governing documents
   equal the union of its pages' corpus_sources joined to the taxonomy (plus a
   declared-gap concern's corpus-only material), its frameworks are the plain-
   text union of those documents' mappings, and its Go deeper chips are the
   derived domains; a concern with no mapped page renders its declared-gap
   block, never hidden; the authority qualifier stays visible on the hub and
   every concern page; each subtype index links up to the hub; and an unknown
   mapped path or an unmapped registry page fails the build.
12. The page prose rule on the hub and the concern pages (round 2): every
   sentence that describes what a page or list holds is checked against the
   rendered pages, including the declared-gap page: the hub lead claims only
   what is curated and what is generated, the qualifier, leadership intro and
   evidence-shelf intro each take the form true for their page, and no lede
   leans on a multi-concern page. A repeated concern slug, a group outside
   the board questions, a root-domain corpus source, corpus-only material on
   a concern with mapped pages, and a registry page with no corpus_sources
   each fail the build.
13. Round 3: the hub qualifier's opening sentence names the pages the path
   leads to; the evidence-shelf sentences agree in number with the rendered
   shelf (and the frameworks intro is count-neutral); a concern with neither
   mapped pages nor corpus-only material fails the build.
14. The crosswalk (design C 3.7 Version A): every main-table instrument has a
   column on /draft/crosswalk/ and an instrument page, every cell's document
   count link resolves to its instrument page at its domain anchor, each
   preset view renders only its own columns, and every crosswalk page carries
   the matrices' own caveats in the "What this mapping is" block.
15. Crosswalk round 2: no register-internal text reaches an instrument
   page's register-fed regions (the lead and the Canonical citation record),
   the Browse and landing pages link the crosswalk, the preset list sits in
   the right-hand rail only, the reverse matrix parser refuses interrupted
   tables and unreadable links, every instrument's reverse paths are
   validated at build, the trade programmes point at the combined CTPAT
   section, and the preset views keep their All link.
16. Crosswalk round 3: the reverse matrix parser refuses a second instrument
   table under a repeated heading and a document path written as plain text
   in a matrix cell, and an instrument lead cuts the register Topic only at
   a sentence-ending period (pinned as literal leads).
17. The Browse adventure (design D sections 3 and 4.2 to 4.5): the By need
   cards land on the five need pages (the mockup's anchor, search and
   example-document targets are retired); Browse carries the executive path
   block (the decide hub plus the six subtype indexes with registry
   counts); the Browse Scope sentence's qualified form is checked against
   every rendered document page; on every need page each branch link in the
   main column resolves to a rendered page and is never a bare anchor or a
   fragment; the govern artefact links open their draft document pages
   wherever one renders (gap G1) and its landing list equals its sources;
   the comply instrument rows equal the
   crosswalk model with recomputed counts; the solutions event rows follow
   the curated table, its scenario index equals the registry and its
   builders rows their domains; and the policies type and subject rows
   equal the taxonomy's counts.
18. Adopter documents (site a9): every top-level ``docs/*.md`` renders a draft
   document page titled from its own metadata block, and the generated search
   and browse listings carry every one of them.
19. Adopter round 2, re-based onto this branch (the search page is just a
   search, so the chips PR 9 adjusted are gone): the adopter metadata reader
   takes only the LEADING block (a fenced example never reads as the
   document, and no file, README.md included, is skipped silently) and
   validates the full 13-field model loudly; related documents resolve by
   link target, not link text; a lede drops a leading bold run-in label; and
   every descriptive sentence on the Browse adopter and By type sections and
   in the search prompt is true for the rendered pool it covers, checked
   against the rendered pages.
20. Adopter round 3: the Browse type counts state their corpus scope and the
   search prompt counts its own pool, the corpus documents and the adopter
   documents apart, and the stated scopes account for every difference
   between the two pools on the rendered pages; the adopter prose says
   documents, not guides, and the Browse intro is a full sentence, singular
   for one file; a repeated metadata field, a Related Documents entry the
   parser cannot keep, and an invalid Version each fail the build; the
   maturity scorecard fails on a version it cannot class instead of
   publishing an Unknown class.
21. Adopter round 4: the docs/ area is labelled Adopter documents wherever it
   renders (row label, section label and heading, anchor), and no paragraph,
   heading or label on Browse or search calls every adopter document a
   guide; the site Version rule judges every version as the corpus metadata
   gate and the maturity heuristic do (a leading zero is accepted, ASCII
   digits only); a root document whose type is not Specification fails the
   draft build; and a Related Documents target that is not a tracked file
   inside the repository (an absolute URL, a path outside the repository, a
   missing or untracked file, or a tracked path whose file is absent or
   resolves elsewhere, a symlink) fails the build.
22. Integration fixes: each concern-page framework name whose exact spelling
   the committed crosswalk alias map carries links its rendered instrument
   page and any other name stays plain text, as the page's sentence says;
   the Related Documents check's file-presence and resolution clauses are
   exercised on fixtures; and the target variable inside that check does not
   shadow the parse loop's own file variable.
23. Browse adventure round 2: the By need card lines are the directed copy;
   the comply instruments intro gives the crosswalk table's instrument count
   and names its Also in the corpus instruments, as the rendered crosswalk
   shows them; the govern and comply annex sentences give the whole annex
   page's count and claim only overlays the rendered annex page includes;
   the govern Lands intro counts its types from the landing table and names
   the concern page by what it asks; and each fail-loud guard of the need
   pages (an artefact not in the repository, a solutions event naming an
   unknown narrative, an unknown govern landing type or concern, and an
   unknown comply gaps register or outcome map) raises on a patched table.
24. Integration round 2: no plain-text framework name on a rendered concern
   page names a crosswalk instrument (outside the listed namesakes and
   derived texts), every linked name names the instrument it links, and a
   name joining several instruments links each; each type page lists the
   adopter documents of its type in a counted block whose sentence holds
   for every row, so it and the policies sentence hold for every document
   of the type, while the documents index's type chips still count the
   corpus list; the Browse and govern sentences about All Documents say
   corpus document and Browse points to the adopter list; the comply annex
   sentence names jurisdiction and sector overlays; a compound alias that
   does not rejoin, also sits in the alias map, or names no instrument,
   and an adopter document whose type has no type page, each fail the
   build; and the generator's content-boundary docstring names each extra
   read the draft makes and calls the adopter pages adopter document pages.
25. Baseline 1.6.0 (spec sections 4, 6.1, 7.33 and 10): the pin and the
   served copies carry the 1.6.0 files (``scheme.js`` new, ``baseline.css``
   and ``palettes.css`` changed) and the pinned, never served palette gate
   ``.baseline/check_palette.py``; every draft page carries the light and
   dark switch as the last child of ``header.mast``, after ``nav.nav``, with
   the ``hidden`` attribute, and loads ``scheme.js`` in ``<head>`` before the
   stylesheets with ``data-cfasync="false"`` before ``src`` and no ``defer``
   or ``async``; the served dark ``--bg`` for grclibrary is the released
   value in both dark forms; the disclosure page names what the switch
   stores; and the build runs the palette gate on the served
   ``palettes.css``, failing on a doctored palette and on an unpinned,
   altered or symlinked gate, and running a private copy of the hashed gate
   bytes.
26. Integration round 3: every count beside a type page link on comply,
   govern, solutions, policies and Browse matches the rendered type page in
   the scope its sentence states (the page's total, or its corpus list); a
   compound framework string's part naming a text that is no crosswalk
   instrument renders as plain text, a linked span names only its own
   instrument, and a compound none of whose parts names an instrument
   fails the build; each instrument's citations include the documents
   reached only through a compound part, as do the comply counts; the
   comply count sentence and meta line claim only what the alias map
   counts; and the alias map comment scopes its clause rule to the concern
   pages.
"""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import re
import shutil
import tempfile
import unittest
from html import unescape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# The draft CSP, copied from baseline 1.6.0 SPECIFICATION.md section 9
# (unchanged since 1.3.1), the shared policy for draft pages; build.py must
# carry it byte for byte.
SPEC_SECTION_9_CSP = (
    "default-src 'none'; script-src 'self' 'unsafe-inline'"
    " https://ajax.cloudflare.com https://static.cloudflareinsights.com;"
    " connect-src 'self' https://cloudflareinsights.com; style-src 'self';"
    " font-src 'self'; img-src 'self'; base-uri 'none'; form-action 'none';"
    " frame-ancestors 'none'"
)

# Baseline 1.6.0 SPECIFICATION.md section 7.33, in the full form every 1.6.0
# reference page carries: the light and dark switch, the last child of
# header.mast after nav.nav, hidden until scheme.js shows it.
SCHEME_SWITCH = (
    '<button class="scheme" type="button" data-scheme-toggle '
    'aria-pressed="false" hidden><svg class="moon" viewBox="0 0 24 24" '
    'width="24" height="24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
    'aria-hidden="true" focusable="false"><path d="M20.5 14.2A8.5 8.5 0 0 1 '
    '9.8 3.5a8.5 8.5 0 1 0 10.7 10.7z"/></svg><svg class="sun" '
    'viewBox="0 0 24 24" width="24" height="24" fill="none" '
    'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
    'stroke-linejoin="round" aria-hidden="true" focusable="false"><circle '
    'cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2'
    'M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 '
    '6.9l1.6-1.6"/></svg><span class="vh">Dark mode</span></button>'
)
# Section 5 and 7.33: in <head>, before the stylesheets, data-cfasync before
# src, no defer or async.
SCHEME_SCRIPT_TAG = (
    '<script data-cfasync="false" src="/draft/assets/baseline/scheme.js">'
    "</script>"
)
# The baseline 1.6.0 SHA256SUMS digests of the files 1.6.0 adds to the copy
# set or changes (CHANGELOG 1.6.0); every other pinned file is unchanged
# from 1.5.1.
RELEASE_1_6_0_DIGESTS = {
    ".web/baseline/scheme.js":
        "39d035d986f53c987cbe92516b9a5fd499af5c7fcdda701ea896c63c45ef1634",
    ".web/baseline/baseline.css":
        "654f9b349acf97860dae417e2bd3cc3de1fe51a2c7b1d7f88d0971efc83bceae",
    ".web/baseline/palettes.css":
        "f1d77366c5bfdae3e7c35420f755cf6a7cbe2a0c8eca081e062635202769cb17",
    ".baseline/check_palette.py":
        "d7a9994997ef721e8e7ba3809b18df3f0e9e3c803bd6fcddb3c8125171e21bfc",
}
# Section 6.1: grclibrary's dark --bg in 1.6.0 (#1f1718 in 1.5.1).
RELEASED_DARK_BG = "#110814"
_DARK_BLOCKS = (
    '.site-grclibrary:not([data-scheme="light"]) {',
    '[data-scheme="dark"].site-grclibrary {',
)


def _dark_token(css, token):
    """The value of ``--<token>`` in each of grclibrary's 2 dark blocks."""
    values = []
    for opener in _DARK_BLOCKS:
        start = css.index(opener) + len(opener)
        block = css[start:css.index("}", start)]
        found = re.findall(r"--" + re.escape(token) + r":\s*([^;]+);", block)
        values.append(found[0].strip() if len(found) == 1 else None)
    return values


def _doctor_dark_token(css, token, value, openers=_DARK_BLOCKS):
    """``css`` with grclibrary's ``--<token>`` set to ``value`` in the named
    dark blocks only."""
    for opener in openers:
        start = css.index(opener) + len(opener)
        end = css.index("}", start)
        block, count = re.subn(r"(--" + re.escape(token) + r":\s*)[^;]+;",
                               r"\g<1>" + value + ";", css[start:end])
        assert count == 1, (opener, token)
        css = css[:start] + block + css[end:]
    return css


_ANCHOR_RE = re.compile(r"<a\s[^>]*>", re.S)
_HREF_RE = re.compile(r'href="([^"]*)"')
_SRC_RE = re.compile(r'src="([^"]*)"')
_EXTERNAL_A_RE = re.compile(r'<a\s[^>]*href="https?://[^"]*"[^>]*>.*?</a>', re.S)
_NAV_RE = re.compile(r'<nav class="nav" aria-label="Site">(.*?)</nav>', re.S)
_NAV_LINK_RE = re.compile(r"<a\s[^>]*>([^<]*)")
_RAIL_RE = re.compile(r'<nav class="rail"[^>]*>.*?</nav>', re.S)
_ID_RE = re.compile(r'\bid="([^"]+)"')
_ROW_HREF_RE = re.compile(r'<li><a href="([^"]*)">')

# The six subtype index routes the reconciled design fixes
# (RECONCILED.md: /draft/decide/<subtype-plural>/, design D section 4.1).
SUBTYPE_SLUGS = {
    "briefs", "scenarios", "journeys", "outcome-maps", "question-sets",
    "choices",
}


def _reading_room_href(page):
    """The draft reading-room URL of one registry page, derived here from
    the registry route rather than through build.py's helpers."""
    return "/draft/decisions/" + page["route"][len("executive/"):] + "/"


_MATRIX_RE = re.compile(r"<table\b[^>]*\sdata-matrix\b")
_TABLE_CLASS_RE = re.compile(r'<table\b[^>]*\sclass="([^"]*)"[^>]*>')
_WRAPPER_TAIL_RE = re.compile(r'<div\b[^>]*\sclass="([^"]*)"[^>]*>\s*$')


def _unbounded_sticky_tables(html):
    """Every ``table.sticky`` whose wrapper is not ``.tablewrap.bounded``.

    Baseline 1.5.0 SPECIFICATION.md section 7.31: a sticky header sticks
    only to its nearest scroll container, so a sticky table's markup is
    ``<div class="tablewrap bounded" tabindex="0"><table class="sticky">``.
    """
    found = []
    for match in _TABLE_CLASS_RE.finditer(html):
        if "sticky" not in match.group(1).split():
            continue
        wrapper = _WRAPPER_TAIL_RE.search(html[max(0, match.start() - 400):
                                               match.start()])
        classes = set(wrapper.group(1).split()) if wrapper else set()
        if not {"tablewrap", "bounded"} <= classes:
            found.append(match.group(0))
    return found


def _matrix_script_faults(html):
    """Every way one page breaks the matrix.js loading rule.

    Baseline 1.5.0 SPECIFICATION.md section 7.30 allows 1 matrix per page,
    and section 8 makes each script opt-in per page, so ``matrix.js`` loads
    exactly on a page whose table carries ``data-matrix``.
    """
    faults = []
    matrices = len(_MATRIX_RE.findall(html))
    if matrices > 1:
        faults.append(f"{matrices} matrices (1 per page, spec 7.30)")
    loads = "/assets/baseline/matrix.js" in html
    if matrices and not loads:
        faults.append("a data-matrix table without matrix.js")
    if loads and not matrices:
        faults.append("matrix.js without a data-matrix table")
    return faults

# The owner-approved "What it gives you" paragraph (landing page), compared
# whole after whitespace normalization, with only the computed document total
# substituted (round-1 WARN: a one-phrase check let "confers no certification"
# flip to "confers certification").
APPROVED_VALUE_PARAGRAPH = (
    "Starting a governance, risk, or compliance programme means writing "
    "dozens of documents before the first control is reviewed. GRC Library "
    "gives you {total} documents that already fit together, each with its "
    "owner, approver, and classification, and mapped to the frameworks an "
    "auditor will ask about. They are free to adopt and adapt under "
    "CC BY-SA 4.0. They are organization-neutral templates: you adapt them "
    "with your own names and details and approve them; adopting them confers "
    "no certification, and legal advice is outside the library."
)

# The executive layer's authority qualifier as each of its three draft page
# types carries it (design D sections 2 and 5 item 7), compared whole (round-1
# WARN: removing any clause passed every test). The subtype index makes the
# promise per page, as executive/README.md line 7 does (round-1 NOTE: it had
# said every claim resolves to the corpus).
NARRATIVE_QUALIFIER = (
    '<p class="lead">A leadership page from the library\'s executive layer: '
    "it explains the position in plain language, and the corpus documents it "
    "cites remain the governing texts.</p>"
)
SUBTYPE_QUALIFIER = (
    '<div class="callout"><p>The leadership pages linked here are explanatory '
    "and advisory; they establish no requirement and prove nothing about your "
    "organization. Every page resolves to the authoritative corpus documents "
    "that do govern.</p></div>"
)
LEADERSHIP_QUALIFIER = (
    '<h2 id="leadership">Leadership pages for this area</h2>\n'
    "<p>Pages from the executive layer that tag this area. They explain and "
    "advise; the documents above govern.</p>"
)


def _load_build():
    spec = importlib.util.spec_from_file_location(
        "web_build_draft_mod", REPO_ROOT / ".web" / "build.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_module(rel, name):
    """Load a repository tool by path (a hyphenated name cannot import)."""
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _page_rel_for(url_path):
    """Map a /draft/... URL path to its dist-relative output path."""
    path = url_path.split("#", 1)[0]
    rel = path.lstrip("/")
    if rel.endswith("/"):
        return rel + "index.html"
    return rel


class DraftSiteRenderTests(unittest.TestCase):
    """Tests over one shared full-site render (the heavy fixture)."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()
        cls.figures = cls.mod.compute_figures()
        cls.site_pages = cls.mod.render_site(cls.figures)
        cls.draft_all = {
            rel: content for rel, content in cls.site_pages
            if rel.startswith("draft/")
        }
        cls.draft_html = {
            rel: content for rel, content in cls.draft_all.items()
            if rel.endswith(".html")
        }
        cls.by_rel = {}
        for rel, content in cls.site_pages:
            cls.by_rel.setdefault(rel, []).append(content)

    # -- 1. frozen root ----------------------------------------------------

    def test_root_byte_identical_without_draft_except_headers_block(self):
        mod = self.mod
        original = mod.VARIANTS
        try:
            mod.VARIANTS = tuple(v for v in original if not v.draft_rules)
            without = mod.render_site(self.figures)
        finally:
            mod.VARIANTS = original
        kept = [(rel, c) for rel, c in self.site_pages
                if not rel.startswith("draft/")]
        self.assertEqual([rel for rel, _ in without], [rel for rel, _ in kept])
        for (rel_a, content_a), (_, content_b) in zip(without, kept):
            if rel_a == "_headers":
                self.assertEqual(
                    content_a + mod.DRAFT_HEADERS_BLOCK, content_b,
                    "_headers must be the draft-free file plus the block",
                )
            else:
                self.assertEqual(
                    content_a, content_b,
                    f"{rel_a} changed by the draft variant",
                )

    def test_every_draft_output_lives_under_draft_prefix(self):
        draft_variant = next(v for v in self.mod.VARIANTS if v.draft_rules)
        rendered = self.mod.render_variant(self.figures, draft_variant)
        self.assertTrue(rendered)
        expected = {
            self.mod.output_rel_for(draft_variant, rel) for rel, _ in rendered
        }
        self.assertEqual(expected, set(self.draft_all))
        for rel in expected:
            self.assertTrue(rel.startswith("draft/"), rel)

    def test_discovery_files_never_mention_the_draft(self):
        for name in ("robots.txt", "sitemap.xml", "llms.txt"):
            self.assertEqual(len(self.by_rel[name]), 1)
            self.assertNotIn("draft", self.by_rel[name][0],
                             f"{name} must not mention the draft")

    def test_no_live_page_links_the_draft(self):
        for rel, content in self.site_pages:
            if rel.startswith("draft/") or not rel.endswith(".html"):
                continue
            self.assertNotIn("/draft", content,
                             f"live page {rel} must not link the draft")

    def test_draft_page_set_is_complete(self):
        self.assertIn("draft/index.html", self.draft_html)
        self.assertIn("draft/browse/index.html", self.draft_html)
        self.assertIn("draft/search/index.html", self.draft_html)
        self.assertIn("draft/documents/index.html", self.draft_html)
        self.assertIn("draft/disclosure/index.html", self.draft_html)
        self.assertIn("draft/license/index.html", self.draft_html)
        self.assertIn("draft/404.html", self.draft_html)
        self.assertNotIn("draft/license.html", self.draft_all,
                         "no license.html file may shadow license/ (spec 7.16)")
        for dp in self.figures["domain_pages"]:
            self.assertIn(f"draft/{dp['domain']}/index.html", self.draft_html)
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8")
        )
        for doc in full:
            rel = "draft/" + self.mod._doc_route_rel(doc["path"])
            if doc.get("domain") == self.mod.ROOT_DOMAIN:
                self.assertNotIn(rel, self.draft_html,
                                 "root specs have no draft document page")
            else:
                self.assertIn(rel, self.draft_html)

    # -- 2. page hygiene ---------------------------------------------------

    def test_pages_noindex_and_self_canonical(self):
        for rel, html in self.draft_html.items():
            self.assertIn('<meta name="robots" content="noindex,nofollow">',
                          html, rel)
            canonical = re.findall(
                r'<link rel="canonical" href="([^"]*)">', html
            )
            self.assertEqual(len(canonical), 1, rel)
            self.assertTrue(
                canonical[0].startswith("https://grclibrary.ai/draft/"),
                f"{rel}: {canonical[0]}",
            )

    def test_pages_pass_the_refusal_rules(self):
        for rel, html in self.draft_html.items():
            # The guard ran at render time; re-assert the properties here so a
            # weakened guard cannot pass silently.
            self.assertNotIn("–", html, rel)
            self.assertNotIn("—", html, rel)
            # Round-3 WARN: an exact spelling list missed valid entity forms,
            # so assert with the guard's own decoding: nothing on the page may
            # decode to a dash, whatever its spelling.
            decoded = unescape(html)
            self.assertNotIn("\u2013", decoded, rel)
            self.assertNotIn("\u2014", decoded, rel)
            self.assertNotRegex(html, r"<style\b", rel)
            self.assertNotRegex(html, r"<script\b(?![^>]*\bsrc=)", rel)
            self.assertNotRegex(html, r"\sstyle\s*=", rel)
            self.assertNotRegex(html, r"\son[a-z]+\s*=", rel)
            self.assertNotIn("{{", html, rel)

    def test_head_order_icons_and_scripts(self):
        for rel, html in self.draft_html.items():
            fonts = html.find("/assets/baseline/fonts.css")
            palettes = html.find("/assets/baseline/palettes.css")
            baseline = html.find("/assets/baseline/baseline.css")
            self.assertTrue(0 < fonts < palettes < baseline,
                            f"{rel}: stylesheet order must be fonts, "
                            "palettes, baseline")
            self.assertIn(
                '<link rel="icon" href="/draft/assets/baseline/logos/'
                'grclibrary-favicon.svg" type="image/svg+xml">', html, rel)
            self.assertIn(
                '<link rel="apple-touch-icon" href="/draft/assets/baseline/'
                'logos/grclibrary-touch.png">', html, rel)
            self.assertIn(
                '<script src="/draft/assets/baseline/copy.js" defer></script>',
                html, rel)
            self.assertNotIn("application/ld+json", html,
                             f"{rel}: no JSON-LD on a noindex draft")
            self.assertNotIn("site.css", html,
                             f"{rel}: the draft loads no site.css")

    def test_rail_pages_load_rail_js_and_carry_no_static_mark(self):
        for rel, html in self.draft_html.items():
            rails = _RAIL_RE.findall(html)
            has_anchor_rail = any('href="#' in rail for rail in rails)
            for rail in rails:
                self.assertNotIn("aria-current", rail,
                                 f"{rel}: no static aria-current on rail links")
            loads_rail_js = "/assets/baseline/rail.js" in html
            self.assertEqual(
                has_anchor_rail, loads_rail_js,
                f"{rel}: rail.js loads exactly on pages whose rail lists "
                "in-page sections",
            )

    def test_matrix_js_loads_exactly_on_matrix_pages(self):
        """Baseline 1.5.0 adds matrix.js (spec 7.30, 1 matrix per page), and
        each script is opt-in per page (spec section 8), so adopting the
        release switches it on nowhere: it loads exactly on a page whose
        table carries ``data-matrix``. No draft page has a matrix yet, so
        MatrixScriptFixtureTests proves the rule on pages that do."""
        for rel, html in self.draft_html.items():
            self.assertEqual(
                _matrix_script_faults(html), [],
                f"{rel}: matrix.js loads exactly on a page with a matrix",
            )

    def test_sticky_tables_sit_in_a_bounded_scroll_box(self):
        """Baseline 1.5.0 defect fix (spec 7.31): a ``.sticky`` table's
        wrapper is ``.tablewrap.bounded``, so its header stays at the top of
        a scroll box bounded to the viewport instead of leaving the screen
        with the page."""
        for rel, html in self.draft_html.items():
            self.assertEqual(
                _unbounded_sticky_tables(html), [],
                f"{rel}: every table.sticky sits in a .tablewrap.bounded",
            )

    def test_document_pages_use_the_logo_only_rail_and_a_body_outline(self):
        """PR 2c (maintainer 2026-11-03 12:16Z): the template allows two
        rails only, so a document page carries the logo-only rail and never
        a nav rail; the source document's outline is a plain list
        under an Outline heading in the page body, and rail.js stays off
        document pages."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8")
        )
        pages_with_sections = 0
        for doc in full:
            if doc.get("domain") == self.mod.ROOT_DOMAIN:
                continue
            rel = "draft/" + self.mod._doc_route_rel(doc["path"])
            html = self.draft_html[rel]
            self.assertNotIn(
                '<nav class="rail"', html,
                f"{rel}: a document page carries no nav rail (spec 7.6 "
                "allows the logo-only rail here)")
            self.assertIn(
                '<div class="rail"><img class="rail-logo"', html,
                f"{rel}: a document page carries the logo-only rail")
            self.assertNotIn(
                "/assets/baseline/rail.js", html,
                f"{rel}: rail.js stays off document pages")
            outline = re.search(
                r'<h2>Outline</h2>\s*<ul>(.*?)</ul>', html, re.S)
            self.assertIsNone(
                re.search(r'<h2>Outline</h2>\s*<ol class="num">', html),
                f'{rel}: the outline is a plain <ul>, not an '
                '<ol class="num">')
            if doc.get("sections"):
                pages_with_sections += 1
                self.assertIsNotNone(
                    outline,
                    f"{rel}: the outline list appears in the page body")
                self.assertNotIn(
                    "<a", outline.group(1),
                    f"{rel}: outline items are plain text, not links")
                body = html.split('<main id="main-content">', 1)[1]
                self.assertIn(
                    "<h2>Outline</h2>", body,
                    f"{rel}: the Outline heading sits in the page body")
                for section in doc["sections"]:
                    expected = self.mod._esc(re.sub(
                        r"\*\*([^*]+)\*\*", r"\1", section.replace("`", "")))
                    self.assertIn(
                        f"<li>{expected}</li>", outline.group(1),
                        f"{rel}: outline lists the heading {section!r}")
            else:
                self.assertIsNone(
                    outline,
                    f"{rel}: no outline on a document without sections")
        self.assertTrue(pages_with_sections,
                        "at least one document page shows an outline")

    def test_internal_references_resolve_inside_the_draft(self):
        rendered = set(self.draft_all)
        ids_by_rel = {
            rel: set(_ID_RE.findall(html))
            for rel, html in self.draft_html.items()
        }
        for rel, html in self.draft_html.items():
            refs = _HREF_RE.findall(html) + _SRC_RE.findall(html)
            for ref in refs:
                if ref.startswith(("https://", "http://")):
                    continue
                path, hash_sign, fragment = ref.partition("#")
                if path:
                    self.assertTrue(path.startswith("/draft/"),
                                    f"{rel}: internal reference escapes the "
                                    f"draft: {ref}")
                    target = _page_rel_for(path)
                    self.assertIn(target, rendered,
                                  f"{rel}: unresolved reference {ref}")
                else:
                    # A fragment-only reference targets the page it is on.
                    target = rel
                if hash_sign:
                    # Every fragment, same-page included, must name an id in
                    # the destination HTML (round-1 WARN: a broken Browse
                    # section id survived the old fragment-stripping check).
                    self.assertTrue(fragment, f"{rel}: empty fragment {ref}")
                    self.assertIn(target, ids_by_rel,
                                  f"{rel}: fragment on a non-page target {ref}")
                    self.assertIn(fragment, ids_by_rel[target],
                                  f"{rel}: fragment {ref} names no id in "
                                  f"{target}")

    def test_external_links_open_in_a_new_tab_with_the_hint(self):
        for rel, html in self.draft_html.items():
            for anchor in _EXTERNAL_A_RE.findall(html):
                head = anchor.split(">", 1)[0]
                self.assertIn('target="_blank"', head, f"{rel}: {head}")
                self.assertIn('rel="noopener noreferrer"', head,
                              f"{rel}: {head}")
                self.assertIn("(opens in a new tab)", anchor,
                              f"{rel}: external link without the hidden hint")

    # -- 3. top bar and About line ------------------------------------------

    def test_top_bar_is_browse_domains_types_search_github(self):
        for rel, html in self.draft_html.items():
            nav = _NAV_RE.search(html)
            self.assertIsNotNone(nav, rel)
            labels = [t.strip() for t in _NAV_LINK_RE.findall(nav.group(1))]
            self.assertEqual(labels,
                             ["Browse", "Domains", "Types", "Search", "GitHub"],
                             f"{rel}: the bar must be Browse, Domains, Types, "
                             "Search, then GitHub last")
            self.assertNotIn("Disclosure", nav.group(1), rel)
            self.assertNotIn("Licence", nav.group(1), rel)
            hrefs = _HREF_RE.findall(nav.group(1))
            self.assertEqual(hrefs[:4], [
                "/draft/browse/", "/draft/browse/#domains",
                "/draft/browse/#types", "/draft/search/",
            ], rel)
            self.assertTrue(hrefs[4].startswith("https://github.com/"), rel)

    def test_current_page_marker(self):
        browse_nav = _NAV_RE.search(
            self.draft_html["draft/browse/index.html"]).group(1)
        self.assertIn('href="/draft/browse/" aria-current="page"', browse_nav)
        search_nav = _NAV_RE.search(
            self.draft_html["draft/search/index.html"]).group(1)
        self.assertIn('href="/draft/search/" aria-current="page"', search_nav)
        home_nav = _NAV_RE.search(self.draft_html["draft/index.html"]).group(1)
        self.assertNotIn("aria-current", home_nav,
                         "the landing page is not in the bar")

    def test_about_line_and_value_paragraph(self):
        landing = self.draft_html["draft/index.html"]
        about = re.search(
            r'<p class="lbl">About this project</p><div><p class="about">'
            r"(.*?)</p></div>", landing, re.S)
        self.assertIsNotNone(about, "the About line (spec 7.24) is required")
        hrefs = _HREF_RE.findall(about.group(1))
        self.assertEqual(hrefs, [
            "/draft/disclosure/", "/draft/license/",
            "https://posluns.ca/privacy/", "https://posluns.ca/security/",
        ], "the About line links in order")
        self.assertEqual(about.group(1).count("(opens in a new tab)"), 2,
                         "Privacy and Security carry the new-tab hint")
        self.assertEqual(about.group(1).count('class="dot"'), 3)
        value = re.search(r'<p class="value">(.*?)</p>', landing, re.S)
        self.assertIsNotNone(value)
        expected = APPROVED_VALUE_PARAGRAPH.format(
            total=self.figures["total"]
        )
        self.assertEqual(" ".join(value.group(1).split()), expected,
                         "the complete approved value paragraph stays, word "
                         "for word, with only the computed total substituted")
        self.assertNotIn("<a", value.group(1),
                         "the value paragraph keeps no licence link "
                         "(maintainer 2026-11-03 02:19Z)")

    def test_only_the_landing_page_links_disclosure_and_licence(self):
        allowed = {
            "draft/index.html", "draft/disclosure/index.html",
            "draft/license/index.html",
        }
        for rel, html in self.draft_html.items():
            if rel in allowed:
                continue
            self.assertNotIn("/draft/disclosure/", html, rel)
            self.assertNotIn("/draft/license/", html, rel)

    # -- licence and disclosure copy -----------------------------------------

    def test_licence_summary_keeps_qualifiers_and_carveouts(self):
        """Round-1 ERROR: the summary dropped LICENSE source qualifiers, and
        the carve-out list missed the vendored AIQT corpus-tool subset that
        NOTICE.md records."""
        page = self.draft_html["draft/license/index.html"]
        self.assertIn(
            "and, if the licensor asks, you must remove any of the "
            "attribution information above to the extent reasonably "
            "practicable (3(a)(3))", page,
            "the 3(a)(3) summary keeps the clause's 'to the extent "
            "reasonably practicable' qualifier")
        self.assertIn(
            "the material is offered as is, without warranties of any kind, "
            "to the extent possible and unless the licensor separately "
            "undertakes otherwise, and where the law allows such a "
            "disclaimer (section 5(a))", page,
            "the 5(a) summary keeps the clause's qualifiers and carries the "
            "closing limit that the disclaimer may not apply where the law "
            "does not allow it (round-4 NOTE)")
        self.assertIn(
            "and, to the extent possible and where the law allows such a "
            "limit, the licensor is not liable for losses arising out of the "
            "licence or the use of the material (5(b))", page,
            "the 5(b) summary keeps the clause's 'to the extent possible' "
            "qualifier, covers losses arising out of the licence as well as "
            "use of the material (round-2 NOTE), and carries the closing "
            "limit that the limitation may not apply where the law does not "
            "allow it (round-3 NOTE)")
        self.assertIn(
            "keep, where the licensor supplied them,", page,
            "the 3(a)(1)(A) summary keeps the 'if it is supplied by the "
            "Licensor' qualifier")
        self.assertIn(
            "the vendored AIQT corpus-tool subset", page,
            "the carve-out list names the vendored AIQT corpus-tool subset "
            "NOTICE.md records under vendor/aiqt/")

    def test_disclosure_data_handling_claim_matches_the_scripts(self):
        """Round-1 NOTE (a published privacy statement): from baseline 1.5.0
        search.js writes the query into the page address (spec 7.29), so the
        Entry 6 claim says so, and each part of the claim is checked against
        the rendered pages and the scripts they load."""
        page = self.draft_html["draft/disclosure/index.html"]
        claim = re.search(
            r'<h2 id="d-6">[^<]*</h2>\s*<p><strong>Claim:</strong>(.*?)</p>',
            page, re.S)
        self.assertIsNotNone(claim, "Entry 6 carries a claim")
        claim = " ".join(claim.group(1).split())
        self.assertIn("make no network requests and use no cookies.", claim)
        # Baseline 1.6.0 (spec sections 7.33 and 8): scheme.js keeps the
        # reader's choice in localStorage, so "use no browser storage" would
        # be false; the claim says what it stores, under which key, and when.
        self.assertNotIn("no cookies or browser storage", claim)
        self.assertIn(
            "The light and dark switch is the one script that uses browser "
            "storage: when the reader presses the switch, it saves the chosen "
            "scheme, the word light or dark, in the browser's local storage "
            'under the key "scheme", so later pages open in that scheme. It '
            "stores nothing else, and nothing until the switch is pressed.",
            claim)
        # Round-2 WARN: the claim names who receives the address. The host
        # receives it on a reload and with later requests to the site; what
        # the beacon sends or stores is not settled by any source in the
        # repository, so the claim says it "can read" the address and stops.
        self.assertIn(
            "The search form filters a list already on the page and does not "
            "submit the query. As the reader types, the search script writes "
            "the query into the page address (?q=), so the query can appear "
            "in the browser history. This site's host, Cloudflare, receives "
            "that address, query included, when the reader reloads the page "
            "and with later requests from the page to this site. Scripts the "
            "page runs, including the Cloudflare Web Analytics beacon, can "
            "read the page address.", claim)
        self.assertNotIn("store nothing", claim,
                         "the address holds the query, so the claim may not "
                         "say the scripts store nothing")
        limitation = re.search(
            r'<h2 id="d-6">.*?<p><strong>Limitation:</strong>(.*?)</p>',
            page, re.S)
        self.assertIsNotNone(limitation, "Entry 6 carries a limitation")
        self.assertIn("the Web Analytics beacon", limitation.group(1),
                      "the beacon the claim names is the one the limitation "
                      "says the host keeps")

        loaded = set()
        for html in self.draft_html.values():
            # Any attribute order: scheme.js carries data-cfasync before src.
            loaded.update(re.findall(
                r'<script\b[^>]*\ssrc="/draft/assets/baseline/([^"]+)"',
                html))
        self.assertIn("scheme.js", loaded)
        sources = {
            name: self.draft_all[f"draft/assets/baseline/{name}"].decode(
                "utf-8")
            for name in loaded
        }
        # "make no network requests and use no cookies"; "the one script
        # that uses browser storage"
        for name, js in sorted(sources.items()):
            for api in ("fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket",
                        "EventSource", "sessionStorage", "indexedDB",
                        "document.cookie", "caches."):
                self.assertNotIn(api, js, f"{name} uses {api}")
            if name != "scheme.js":
                self.assertNotIn("localStorage", js, f"{name} uses storage")
        # "saves ... the word light or dark ... under the key "scheme"":
        # one key, one write, inside the click handler, of "light" or "dark".
        scheme = sources["scheme.js"]
        self.assertIn('var KEY = "scheme";', scheme)
        self.assertEqual(
            re.findall(r"localStorage\.(\w+)\(([^,)]*)", scheme),
            [("getItem", "KEY"), ("setItem", "KEY")],
            "scheme.js reads and writes the one key and nothing else")
        self.assertEqual(re.findall(r"(?<!function )\bwrite\((\w+)\)", scheme),
                         ["next"],
                         "the one write call stores the scheme a press picks")
        self.assertIn('var next = isDark() ? "light" : "dark";', scheme)
        click = scheme[scheme.index('addEventListener("click"'):]
        self.assertIn("write(next);", click[:click.index("});")],
                      "the write happens inside the click handler only")
        # "the search script writes the query into the page address (?q=)":
        # it is the only loaded script that writes the address, and it
        # writes ?q= and no facet key (no draft page has a facet group).
        self.assertEqual(
            sorted(n for n, js in sources.items() if "replaceState" in js),
            ["search.js"],
            "exactly the search script writes the page address")
        self.assertIn('p.set("q", input.value)', sources["search.js"])
        # "filters a list already on the page and does not submit the query"
        search_pages = [rel for rel, html in self.draft_html.items()
                        if "/assets/baseline/search.js" in html]
        self.assertTrue(search_pages, "a draft page carries the search form")
        for rel in search_pages:
            html = self.draft_html[rel]
            self.assertNotIn("data-filter-group", html,
                             f"{rel}: a facet would write its own key too")
            form = re.search(r"<form\b[^>]*\sdata-search\b[^>]*>(.*?)</form>",
                             html, re.S)
            self.assertIsNotNone(form, f"{rel}: the search form")
            self.assertNotRegex(form.group(0), r"<form\b[^>]*\saction=",
                                f"{rel}: the form names no submit target")
            self.assertNotRegex(form.group(1), r"<input\b[^>]*\sname=",
                                f"{rel}: the query field has no name, so a "
                                "submit never carries the query")
            self.assertRegex(
                html, r"<ul\b[^>]*\sdata-search-scope\b[^>]*>\s*<li\b",
                f"{rel}: the list the form filters is already on the page")

    def test_disclosure_evidence_lists_every_loaded_script(self):
        """Round-2 NOTE: Entry 6's evidence for "its own scripts" listed
        copy.js and search.js but not rail.js, which the draft pages load.
        The evidence links exactly the scripts the rendered draft pages load,
        each to its vendored source, and every script is a baseline asset."""
        loaded = set()
        for rel, html in self.draft_html.items():
            for src in re.findall(r'<script\b[^>]*\ssrc="([^"]*)"', html):
                self.assertTrue(
                    src.startswith("/draft/assets/baseline/"),
                    f"{rel}: {src} is not a baseline asset")
                loaded.add(src.rsplit("/", 1)[1])
        self.assertIn("rail.js", loaded)
        page = self.draft_html["draft/disclosure/index.html"]
        evidence = re.search(
            r'<h2 id="d-6">.*?<p><strong>Evidence:</strong>(.*?)</p>',
            page, re.S)
        self.assertIsNotNone(evidence, "Entry 6 carries evidence")
        base = self.mod.GITHUB_BLOB_BASE + ".web/baseline/"
        listed = re.findall(
            r'<a href="' + re.escape(base) + r'([^"/]+\.js)"[^>]*>([^<]*)<',
            evidence.group(1))
        self.assertEqual(sorted(href for href, _ in listed), sorted(loaded),
                         "the evidence links every loaded script, no other")
        for href, text in listed:
            self.assertEqual(text, href, "each link names its script")

    # -- pinned version named in prose ---------------------------------------

    def test_prose_names_the_pinned_baseline_version(self):
        """Round-3 finding: nothing checked that prose naming the pinned
        template version agrees with ``.baseline/pin.toml``, so build.py
        comments kept saying "baseline 1.3.1" after the bump to 1.4.1. Every
        "baseline <version>" that names the current template (NOTICE.md's
        baseline entry, the rendered licence page and the build.py comments)
        must carry the pin.toml version; a historical mention such as
        "unchanged since 1.3.1" stays allowed because it does not use the
        "baseline <version>" form."""
        pin_text = (REPO_ROOT / ".baseline" / "pin.toml").read_text(
            encoding="utf-8")
        pin = re.search(r'^version\s*=\s*"(\d+\.\d+\.\d+)"', pin_text, re.M)
        self.assertIsNotNone(pin, ".baseline/pin.toml carries a version key")
        version = pin.group(1)
        named = re.compile(r"baseline (\d+\.\d+\.\d+)")

        notice = (REPO_ROOT / "NOTICE.md").read_text(encoding="utf-8")
        entries = [p for p in notice.split("\n\n")
                   if p.startswith("Site template:")]
        self.assertEqual(
            len(entries), 1, "NOTICE.md keeps exactly one baseline entry")
        self.assertEqual(
            named.findall(entries[0]), [version],
            "NOTICE.md's baseline entry names exactly the pinned version")

        page = self.draft_html["draft/license/index.html"]
        self.assertEqual(
            set(named.findall(page)), {version},
            "the rendered licence page names exactly the pinned version")
        # Round-1 NOTE (spec section 11): the version on the page is rendered
        # from the pin, so no draft template may type one.
        for path in sorted((REPO_ROOT / ".web" / "templates-draft").rglob(
                "*.html")):
            self.assertEqual(
                named.findall(path.read_text(encoding="utf-8")), [],
                f"{path.relative_to(REPO_ROOT)}: a template names the baseline "
                "version as {{BASELINE_VERSION}}, never typed")

        source = (REPO_ROOT / ".web" / "build.py").read_text(encoding="utf-8")
        # Rejoin wrapped comment lines so "baseline\n# 1.4.1" is one phrase.
        found = set(named.findall(source.replace("\n# ", " ")))
        self.assertEqual(
            found, {version},
            "every build.py comment that names the current template carries "
            "the pinned version, and no other baseline version is named as "
            "current")

    # -- 5. counts ----------------------------------------------------------

    def test_counts_match_a_recount_of_the_taxonomy(self):
        text = self.mod.TAXONOMY.read_text(encoding="utf-8")
        docs = self.mod.parse_taxonomy(text)
        total = len(docs)
        domain_docs = [d for d in docs
                       if d["domain"] != self.mod.ROOT_DOMAIN]
        domains = {}
        types = {}
        for d in docs:
            types[d["type"]] = types.get(d["type"], 0) + 1
        for d in domain_docs:
            domains[d["domain"]] = domains.get(d["domain"], 0) + 1
        root_count = total - len(domain_docs)
        browse = self.draft_html["draft/browse/index.html"]
        # The meta sentence separates the in-domain documents from the root
        # library specifications (round-1 WARN: "360 documents in 12 domains"
        # overcounted; 2 of the 360 live in no domain).
        self.assertIn(
            f'<p class="meta">{total} documents: {len(domain_docs)} across '
            f'{len(domains)} domains plus {root_count} library '
            f'specifications, in {len(types)} types, one connected corpus. ',
            browse)
        self.assertIn(
            f'<div class="fig"><span class="num">{total}</span>'
            '<span class="cap">documents</span></div>', browse)
        self.assertIn(
            f'<div class="fig"><span class="num">{len(domains)}</span>'
            '<span class="cap">domains</span></div>', browse)
        self.assertIn(
            f'<div class="fig"><span class="num">{len(types)}</span>'
            '<span class="cap">document types</span></div>', browse)
        for domain, count in domains.items():
            page = self.draft_html[f"draft/{domain}/index.html"]
            noun = "document" if count == 1 else "documents"
            self.assertIn(f'<p class="meta">{count} {noun}. ', page)
            self.assertIn(f'<span class="n">{count}</span>', browse)
        landing = self.draft_html["draft/index.html"]
        self.assertIn(f">{domains['governance']} documents</span>", landing)
        self.assertIn(
            f"{len(domain_docs)} documents across {len(domains)} domains "
            f"plus {root_count} library specifications", landing,
            "the Browse tile separates in-domain documents from the root "
            "library specifications")
        search = self.draft_html["draft/search/index.html"]
        # The rows are drawn from the non-root corpus documents plus the
        # docs/ adopter documents (site a9), so the row count and the prompt
        # count that pool, the two parts apart, and never claim the whole
        # library.
        adopter_count = len(self._adopter_doc_paths())
        pool = len(domain_docs) + adopter_count
        self.assertEqual(search.count("data-search="), pool)
        self.assertIn(
            f'<p class="meta" id="search-prompt">Search the {pool} '
            f"documents listed below, the {len(domain_docs)} corpus "
            f"documents across the {len(domains)} domains and the "
            f"{adopter_count} adopter documents under docs/, by ", search)
        self.assertNotIn(f"Search all {pool}", search)
        # The documents index counts its own rows: the non-root documents and
        # their areas, plus the root specifications, in the types of all of
        # them (the set the type pages count).
        index = self.draft_html["draft/documents/index.html"]
        self.assertIn(
            f'<p class="meta">{len(domain_docs)} documents across '
            f'{len(domains)} areas, ', index)
        self.assertIn(
            f"plus {root_count} library specifications read on GitHub, in "
            f"{len(types)} types. ", index)
        self.assertIn(f"Documents, {len(domain_docs)}</p>", index)

    # -- 5b. search coverage (round-1 defect: the page carried only the 36
    # most recently dated rows, so most queries matched nothing) --------------

    _SEARCH_ROW_RE = re.compile(r'<li data-search="([^"]*)"><a href="([^"]*)">')

    def _search_rows(self):
        search = self.draft_html["draft/search/index.html"]
        scope = re.search(
            r"<ul[^>]* data-search-scope>(.*?)</ul>", search, re.S
        )
        self.assertIsNotNone(
            scope, "search page has no [data-search-scope] list"
        )
        return self._SEARCH_ROW_RE.findall(scope.group(1))

    def _doc_pages(self):
        """The draft document pages (the documents index, the one fixed page
        under documents/, is not a document page)."""
        return {rel for rel in self.draft_html
                if rel.startswith("draft/documents/")
                and rel != "draft/documents/index.html"}

    def test_search_has_one_row_per_draft_document_page(self):
        doc_pages = self._doc_pages()
        self.assertTrue(doc_pages)
        self.assertEqual(
            len(self._search_rows()), len(doc_pages),
            "the search list carries one row per draft document page")

    def test_every_search_row_links_an_existing_draft_document_page(self):
        doc_pages = self._doc_pages()
        linked = set()
        for _, href in self._search_rows():
            self.assertTrue(href.startswith("/draft/documents/"), href)
            target = _page_rel_for(href)
            self.assertIn(target, self.draft_html,
                          f"search row links a missing page: {href}")
            linked.add(target)
        self.assertEqual(
            linked, doc_pages,
            "the rows link every draft document page, each exactly once")

    def test_known_terms_match_the_expected_documents(self):
        """Replays search.js's matching (every whitespace-split query term is
        a substring of the row's decoded data-search text) for terms a reader
        would type, including documents the old 36-row page missed."""
        rows = [(unescape(hay).lower(), href)
                for hay, href in self._search_rows()]

        def hits(query):
            terms = query.lower().split()
            return {href for hay, href in rows
                    if all(t in hay for t in terms)}

        cases = (
            # Title terms; dated 2026-10-27, outside the old 36-row window.
            ("exception risk acceptance",
             "/draft/documents/governance/"
             "policy-exception-and-risk-acceptance-management/"),
            # Title term on one of the oldest documents (2026-07-02).
            ("ctpat",
             "/draft/documents/compliance/logistics/"
             "register-ctpat-united-states-msc-controls/"),
            # A mapped framework name reaches the same governance policy.
            ("iso 31000",
             "/draft/documents/governance/"
             "policy-exception-and-risk-acceptance-management/"),
            # Review round 1 WARN: two of the page's own example searches,
            # each matching its document only through purpose words after the
            # first 200 characters ("retention" first appears at offset 294 of
            # this purpose, "incident" at offset 419 of the next); a truncated
            # purpose lost both.
            ("retention",
             "/draft/documents/operations/"
             "procedure-media-handling-and-transport/"),
            ("incident response",
             "/draft/documents/operations/"
             "procedure-security-monitoring-and-alert-management/"),
        )
        for query, expected in cases:
            with self.subTest(query=query):
                self.assertIn(expected, hits(query))

    # -- 5c. adopter documents (site a9, maintainer decision 2026-11-03
    # 14:59Z: every docs/ adopter document gets a draft document page and
    # appears in the generated search and browse listings, each read from the
    # file's own metadata block because docs/ sits outside taxonomy.yml per
    # specification-master-project.md section 4) ------------------------------

    _TITLE_FIELD_RE = re.compile(
        r"^\*\*Document Title:\*\*\s*(.*?)\s*\\?$", re.M)

    def _adopter_doc_paths(self):
        # Every top-level docs/*.md, README.md not excepted (round-2 note 2:
        # the build no longer skips one silently; docs/ carries none today,
        # and a future one must carry the metadata block like any other).
        paths = sorted(
            f"docs/{p.name}" for p in (REPO_ROOT / "docs").glob("*.md")
        )
        self.assertTrue(paths, "docs/ holds no adopter documents")
        return paths

    def test_every_adopter_doc_has_a_draft_document_page(self):
        for rel_md in self._adopter_doc_paths():
            rel = "draft/" + self.mod._doc_route_rel(rel_md)
            self.assertIn(rel, self.draft_html,
                          f"{rel_md} has no draft document page")
            title = self._TITLE_FIELD_RE.search(
                (REPO_ROOT / rel_md).read_text(encoding="utf-8"))
            self.assertIsNotNone(title, f"{rel_md} carries no Document Title")
            self.assertIn(f"<h1>{self.mod._esc(title.group(1))}</h1>",
                          self.draft_html[rel],
                          f"{rel_md}: the page heading is the document title")

    def test_search_lists_every_adopter_doc(self):
        hrefs = {href for _, href in self._search_rows()}
        for rel_md in self._adopter_doc_paths():
            self.assertIn(f"/draft/documents/{rel_md[:-3]}/", hrefs,
                          f"{rel_md} has no search row")

    def test_browse_lists_every_adopter_doc(self):
        browse = self.draft_html["draft/browse/index.html"]
        for rel_md in self._adopter_doc_paths():
            self.assertIn(f'href="/draft/documents/{rel_md[:-3]}/"', browse,
                          f"{rel_md} is not listed on the browse page")

    # -- 5d. adopter page prose: every descriptive sentence true for every
    # item it covers, checked against the rendered pages ----------------------

    def test_browse_adopter_intro_is_true_for_every_item(self):
        """Round-2 fix 3: the adopter section intro named only some of the
        listed documents and called them all 'how to adopt the library'. The
        sentence now derives its count from the generated list and claims
        only what every item satisfies (each is read from its own record)."""
        browse = self.draft_html["draft/browse/index.html"]
        guides = re.search(
            r'<h2 id="adopter-documents">.*?<ul class="plan described">\n'
            r'(.*?)\n</ul>', browse, re.S)
        self.assertIsNotNone(guides, "no adopter list after the adopter h2")
        rows = guides.group(1).count("<li>")
        self.assertEqual(rows, len(self._adopter_doc_paths()),
                         "the adopter list carries one row per docs/ file")
        self.assertIn(
            f"<p>The {rows} adopter documents under docs/ are listed here. "
            "Each entry is read from the leading metadata block of its file, "
            "so the list follows the repository at every build.</p>", browse,
            "the intro states the generated count and only universal claims")
        self.assertNotIn("How to adopt the library", browse)

    def test_browse_adopter_intro_is_a_sentence_singular_for_one(self):
        """Round-3 note 4: the intro opened with a fragment ('The 12
        adopter documents under docs/.'), would read 'The 1 adopter
        documents' for one file, and 'its own record' did not say it meant
        the metadata block. Rendered from the browse values for one and for
        two real adopter records."""
        docs = self.mod.parse_adopter_docs()
        self.assertGreaterEqual(len(docs), 2)
        one = self.mod.draft_browse_values(self.figures, docs[:1])
        self.assertEqual(
            one["GUIDE_INTRO"],
            "The 1 adopter document under docs/ is listed here. Its entry is "
            "read from the leading metadata block of its file, so the list "
            "follows the repository at every build.")
        two = self.mod.draft_browse_values(self.figures, docs[:2])
        self.assertEqual(
            two["GUIDE_INTRO"],
            "The 2 adopter documents under docs/ are listed here. Each entry "
            "is read from the leading metadata block of its file, so the list "
            "follows the repository at every build.")
        for values in (one, two):
            self.assertNotIn("adopter documents under docs/.",
                             values["GUIDE_INTRO"])
            self.assertNotIn("own record", values["GUIDE_INTRO"])

    _TYPE_PLAN_RE = re.compile(
        r'<li><a href="[^"]*">([^<]+)</a><span class="n">(\d+)</span></li>')

    def test_browse_type_counts_state_their_scope(self):
        """Round-3 WARN 1, re-based onto this branch (the search page is just
        a search, so its type chips are gone): the Browse type counts cover
        the whole corpus, the library specifications included, while the
        search list adds the adopter documents and leaves out the library
        specifications. The scope sentence states both claims, each checked
        against the rendered pages, type section and search rows alike."""
        browse = self.draft_html["draft/browse/index.html"]
        section = re.search(
            r'<h2 id="types">By type</h2>\n<p>([^<]*)</p>\n'
            r'<div class="wide"><ul class="plan three">\n(.*?)\n</ul>',
            browse, re.S)
        self.assertIsNotNone(section, "no By type scope line on Browse")
        browse_counts = {unescape(t): int(c) for t, c in
                         self._TYPE_PLAN_RE.findall(section.group(2))}
        self.assertTrue(browse_counts)
        docs = self.mod.parse_taxonomy(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        root = [d for d in docs if d["domain"] == self.mod.ROOT_DOMAIN]
        adopter = self.mod.parse_adopter_docs()
        # The stated scope: the whole corpus, the library specifications
        # included, the adopter documents not.
        self.assertEqual(sum(browse_counts.values()), len(docs))
        self.assertEqual(
            unescape(section.group(1)),
            f"Each count covers the {len(docs)} corpus documents, the "
            f"{len(root)} library specifications included; the "
            f"{len(adopter)} adopter documents listed below are not counted "
            "here. The search page's list adds the adopter documents and "
            "leaves out the library specifications.")
        # The sentence's second claim, on the rendered search rows: the pool
        # is the corpus documents without the root specifications, plus
        # every adopter document.
        hrefs = {href for _, href in self._search_rows()}
        self.assertEqual(len(hrefs), len(docs) - len(root) + len(adopter))
        for g in adopter:
            self.assertIn(f"/draft/documents/{g['path'][:-3]}/", hrefs)
        for d in root:
            self.assertNotIn(f"/draft/documents/{d['path'][:-3]}/", hrefs)

    _ROW_META_RE = re.compile(
        r'<li data-search="[^"]*"><a href="[^"]*">.*?</a>'
        r'<span class="n">([^,<]+), ([^<]+)</span>')

    # The page's own words: paragraphs (label paragraphs included), headings,
    # and row labels. A quoted corpus purpose inside a row's data-search
    # attribute, and a document title, are not page prose.
    _LABEL_TEXT_RES = (
        re.compile(r"<p[^>]*>(.*?)</p>", re.S),
        re.compile(r"<h[1-6][^>]*>(.*?)</h[1-6]>", re.S),
        re.compile(r'<span class="n">(.*?)</span>', re.S),
    )

    def _label_texts(self, html):
        texts = []
        for pattern in self._LABEL_TEXT_RES:
            for chunk in pattern.findall(html):
                texts.append(" ".join(
                    unescape(re.sub(r"<[^>]+>", " ", chunk)).split()))
        self.assertTrue(texts)
        return texts

    def test_no_page_prose_calls_every_adopter_document_a_guide(self):
        """Round-3 note 3 and round-4 WARN 1: the docs/ area holds guides,
        templates and a register, so while any adopter document is not a
        Guide, no paragraph, heading or label on Browse or search may call
        the area's documents adopter guides. Checked on the rendered
        pages."""
        types = {d["type"] for d in self.mod.parse_adopter_docs()}
        self.assertNotEqual(types, {"Guide"},
                            "the docs/ area is not all guides today")
        for rel in ("draft/search/index.html", "draft/browse/index.html"):
            for text in self._label_texts(self.draft_html[rel]):
                self.assertNotIn(
                    "adopter guides", text.lower(),
                    f"{rel}: '{text}' (adopter document types are "
                    f"{sorted(types)})")

    def test_adopter_area_is_labelled_adopter_documents_everywhere(self):
        """Round-4 WARN 1, re-based (no chips on this branch's search page):
        the docs/ area is labelled Adopter documents on the Browse section
        label, heading and anchor and on every docs/ search row's area
        label. Checked on the rendered pages."""
        adopter = self.mod.parse_adopter_docs()
        browse = self.draft_html["draft/browse/index.html"]
        search = self.draft_html["draft/search/index.html"]
        self.assertIn(
            '<p class="lbl sec">Adopter documents</p>\n'
            '<h2 id="adopter-documents">Adopter documents</h2>', browse)
        labels = [unescape(area) for _, area in
                  self._ROW_META_RE.findall(search)]
        self.assertEqual(labels.count("Adopter documents"), len(adopter),
                         "every docs/ row carries the area label")
        # The old anchor is gone, and nothing links it.
        for rel, html in self.draft_html.items():
            self.assertNotIn("#guides", html, rel)
            self.assertNotIn('id="guides"', html, rel)

    def test_no_draft_page_links_a_docs_area_page(self):
        """Round-2 check 6 (agy F1): adopter documents carry the docs area
        and no /draft/docs/ page is generated, so no page may reference
        one (the Browse adopter section at /draft/browse/#adopter-documents
        is the area's listing instead)."""
        for rel, html in self.draft_html.items():
            self.assertNotIn('"/draft/docs/', html, rel)

    _LEAD_RE = re.compile(r'<p class="lead">(.*?)</p>', re.S)

    def _doc_lead(self, rel_md):
        rel = "draft/" + self.mod._doc_route_rel(rel_md)
        m = self._LEAD_RE.search(self.draft_html[rel])
        self.assertIsNotNone(m, f"{rel} has no lede")
        return unescape(m.group(1))

    def test_generated_portal_and_scorecard_ledes_are_true_here(self):
        """Round-2 fix 4: the generated ledes said 'Each section lists' and
        'per the heuristic below', describing content these pages do not
        show; the generator wording is now true wherever it is shown."""
        portal = self._doc_lead("docs/portal.md")
        self.assertTrue(
            portal.startswith("The adopter portal is a navigation aid"),
            portal)
        for phrase in ("This page", "Each section lists", "below"):
            self.assertNotIn(phrase, portal)
        scorecard = self._doc_lead("docs/maturity-scorecard.md")
        self.assertTrue(
            scorecard.startswith("The maturity scorecard classifies"),
            scorecard)
        for phrase in ("This scorecard", "below"):
            self.assertNotIn(phrase, scorecard)
        self.assertIn("recorded in the scorecard", scorecard)

    def test_scorecard_names_every_class_it_can_publish(self):
        """Round-3 note 6: the scorecard lede names three classes while the
        generator also published an Unknown class (its summary read
        'Unknown: 0'). A version it cannot class now fails the build, and the
        classes the lede names are exactly the classes the committed
        scorecard and its draft page publish."""
        portal = _load_module("tools/build-portal.py",
                              "portal_build_draft_mod")
        doc = {"path": "governance/fixture.md", "title": "Fixture",
               "type": "Policy", "version": "1.0", "date": "2026-11-03"}
        with self.assertRaises(SystemExit) as caught:
            portal.build_scorecard([doc])
        self.assertIn("governance/fixture.md", str(caught.exception))
        lede = self._doc_lead("docs/maturity-scorecard.md")
        named = re.search(r"classifies each active artefact as (.*?)\.",
                          lede)
        self.assertIsNotNone(named, lede)
        lede_classes = re.split(r", or |, ", named.group(1))
        text = (REPO_ROOT / "docs" / "maturity-scorecard.md").read_text(
            encoding="utf-8")
        summary = re.search(r"^_Summary as of last regeneration: (.*)\._$",
                            text, re.M)
        self.assertIsNotNone(summary)
        summary_classes = [part.split(":")[0] for part in
                           summary.group(1).split(", ")]
        self.assertEqual(lede_classes, summary_classes)
        self.assertEqual(lede_classes, ["Mature", "Baseline", "Draft"])
        self.assertNotIn("Unknown", text)

    def test_lede_drops_a_leading_bold_run_in_label(self):
        """Round-2 note 1: the manifest's lede opened 'Purpose. A public
        bibliography...', the flattened run-in label kept as prose."""
        lead = self._doc_lead("docs/reference-acquisition-manifest.md")
        self.assertTrue(lead.startswith("A public bibliography"), lead)

    def test_worked_example_page_is_titled_from_its_own_block(self):
        """Round-2 error 1 companion: docs/worked-example.md carries a whole
        fenced example document; the page must read the file's own leading
        block, never the fenced one."""
        rel = "draft/" + self.mod._doc_route_rel("docs/worked-example.md")
        self.assertIn(
            "<h1>Worked Example: Converting a Draft into a CC BY-SA 4.0 "
            "Artefact</h1>", self.draft_html[rel])

    # -- 5e. search is just a search (maintainer 2026-11-03 14:29Z: "there's
    # too much going on ... search should just give you a search") -----------

    def test_search_page_has_no_chip_rows_or_recently_updated_block(self):
        search = self.draft_html["draft/search/index.html"]
        main = search.split('<main id="main-content">', 1)[1]
        main = main.split("</main>", 1)[0]
        self.assertNotIn('class="chips"', main,
                         "the type and area chip rows belong to Browse")
        for phrase in ("By type", "By area", "Recently updated",
                       "most recently dated"):
            self.assertNotIn(phrase, main, f"search page still says {phrase!r}")
        self.assertNotIn("<h2", main,
                         "no section blocks under the search heading")
        lists = re.findall(r"<ul\b[^>]*>", main)
        self.assertEqual(len(lists), 1,
                         "the one list on the page is the search scope")
        self.assertIn("data-search-scope", lists[0])

    def test_search_input_is_labelled_and_described_by_the_prompt(self):
        search = self.draft_html["draft/search/index.html"]
        self.assertIn('<label class="lbl" for="q">Search the library</label>',
                      search)
        self.assertIn('aria-describedby="search-prompt"', search)
        self.assertEqual(search.count('id="search-prompt"'), 1)
        self.assertIn("data-search-status></p></form>", search,
                      "the status line stays empty for search.js to fill")

    def test_search_landmark_live_status_and_list_name_are_exposed(self):
        """Review round 2 WARN: removing the search landmark, the status
        line's live-region roles, or the list's accessible name passed every
        test. The list is named for what it holds on this page, not "All
        documents" or "Documents", the names of the separate full index."""
        search = self.draft_html["draft/search/index.html"]
        forms = re.findall(r"<form\b([^>]*)>", search)
        self.assertEqual(len(forms), 1, "the page has one form")
        self.assertIn('role="search"', forms[0],
                      "the form is the page's search landmark")
        self.assertIn("data-search", forms[0])
        status = re.findall(r"<p\b([^>]*)\bdata-search-status>", search)
        self.assertEqual(len(status), 1, "one status line for search.js")
        self.assertIn('role="status"', status[0])
        self.assertIn('aria-live="polite"', status[0])
        scope = re.findall(r"<ul\b([^>]*)\bdata-search-scope>", search)
        self.assertEqual(len(scope), 1)
        name = re.search(r'\baria-label="([^"]*)"', scope[0])
        self.assertIsNotNone(name, "the result list has an accessible name")
        self.assertEqual(name.group(1), "Search results")

    def test_search_prompt_describes_every_row_it_counts(self):
        """The rendered prompt, checked against the rendered rows: its counts
        are the rows, the two pools they come from (the corpus documents and
        the docs/ adopter documents, site a9) and the corpus rows' domains, a
        field it states plainly is carried by every row, and a purpose only
        some rows state is qualified with the count of rows that do.
        Frameworks carry no count and are qualified in words (review round 2
        WARN: "by framework for the 240 that map to one" counted a row whose
        taxonomy frameworks list holds only prose fragments). The groupings
        counted are the corpus domains, as on Browse (review round 2 NOTE);
        the docs/ area is no domain, so the stated field is the row's
        area."""
        search = self.draft_html["draft/search/index.html"]
        prompt = re.search(
            r'<p class="meta" id="search-prompt">([^<]*)</p>', search)
        self.assertIsNotNone(prompt)
        prompt = unescape(prompt.group(1))
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8")
        )
        by_href = {self.mod._doc_page_url("/draft", d["path"]): d
                   for d in full + self.mod.parse_adopter_docs()}
        hrefs = [href for _, href in self._search_rows()]
        docs = [by_href[href] for href in hrefs]
        corpus = [d for d in docs
                  if d.get("domain") != self.mod.ADOPTER_DOCS_AREA]
        adopter = [d for d in docs
                   if d.get("domain") == self.mod.ADOPTER_DOCS_AREA]
        self.assertTrue(adopter, "the pool carries the adopter documents")
        scope = re.search(r"<ul[^>]* data-search-scope>(.*?)</ul>",
                          search, re.S).group(1)
        rows = re.findall(
            r'<li data-search="[^"]*"><a href="[^"]*">([^<]+)</a>'
            r'<span class="n">([^<,]+), ([^<]+)</span>', scope)
        self.assertEqual(len(rows), len(hrefs),
                         "every row shows a title, a type and an area")
        domains = {d["domain"] for d in corpus}
        with_purpose = sum(1 for d in docs
                           if (d.get("purpose") or "").strip())
        head = re.match(
            r"Search the (\d+) documents listed below, the (\d+) corpus "
            r"documents across the (\d+) domains and the (\d+) adopter "
            r"documents under docs/, by title, type, ", prompt)
        self.assertIsNotNone(head, prompt)
        self.assertEqual(int(head.group(1)), len(rows))
        self.assertEqual(int(head.group(2)), len(corpus))
        self.assertEqual(int(head.group(3)), len(domains))
        self.assertEqual(int(head.group(4)), len(adopter))
        self.assertIn(
            f'<div class="fig"><span class="num">{head.group(3)}</span>'
            '<span class="cap">domains</span></div>',
            self.draft_html["draft/browse/index.html"],
            "the prompt's domains are the ones Browse counts")
        self.assertNotRegex(prompt, r"\ball\b",
                            "the rows are not the whole library")
        # The row areas the stated field covers: every corpus domain label
        # plus the adopter area label, each counted truthfully by pool.
        areas = {area for _, _, area in rows}
        self.assertIn("Adopter documents", areas)
        self.assertEqual(
            len(areas - {"Adopter documents"}), len(domains),
            "the corpus rows' areas are their domains, one label each")
        purpose = re.search(r"by purpose for the (\d+) that states? one",
                            prompt)
        counts = [len(rows), len(corpus), len(domains), len(adopter)]
        if with_purpose == len(rows):
            self.assertIsNone(purpose)
            self.assertRegex(prompt, r"\barea, (and )?purpose\b")
        else:
            self.assertIsNotNone(purpose, "purpose is qualified")
            self.assertEqual(int(purpose.group(1)), with_purpose)
            self.assertNotRegex(prompt, r"\barea, (and )?purpose\b")
            counts.append(with_purpose)
        self.assertEqual([int(n) for n in re.findall(r"\d+", prompt)],
                         counts, "the prompt counts no frameworks")
        self.assertNotRegex(prompt, r"frameworks? (each|every)\b")
        if any(d.get("frameworks") for d in docs):
            self.assertIn(
                "by the frameworks a document maps to, where it has any.",
                prompt)
        else:
            self.assertNotIn("framework", prompt)

    def test_search_rows_carry_the_full_data_search_text(self):
        """Each draft document appears once, the docs/ adopter documents
        included (site a9), and its data-search text is the PR 2d haystack:
        title, type, area label and slug, full purpose, and framework names,
        lower-cased with whitespace collapsed."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8")
        )
        expected = {}
        for d in full + self.mod.parse_adopter_docs():
            if d.get("domain") == self.mod.ROOT_DOMAIN:
                continue
            href = self.mod._doc_page_url("/draft", d["path"])
            expected[href] = " ".join(" ".join(
                [d.get("title", ""), d.get("type", ""),
                 self.mod.draft_domain_label(d.get("domain", "")),
                 d.get("domain", ""), d.get("purpose", "") or ""]
                + d.get("frameworks", [])
            ).lower().split())
        rows = self._search_rows()
        hrefs = [href for _, href in rows]
        self.assertEqual(len(hrefs), len(set(hrefs)),
                         "no document is listed twice")
        self.assertEqual(set(hrefs), set(expected))
        for hay, href in rows:
            with self.subTest(href=href):
                self.assertEqual(unescape(hay), expected[href])

    def test_search_prompt_count_is_generated_from_the_rows(self):
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8")
        )
        domain_docs = [d for d in full
                       if d.get("domain") != self.mod.ROOT_DOMAIN]
        one = [d for d in domain_docs if d["domain"] == "governance"][:3]
        two = one[:2] + [next(d for d in domain_docs
                              if d["domain"] == "privacy")]

        # A frameworks list is empty (0), names a framework (1), or holds only
        # extraction fragments (2), the shape of the round 2 WARN's row; the
        # prompt never counts either kind, so both read the same.
        framework_lists = ([], ["ISO 31000:2018"],
                           ["Normative weight.", "Distributed traceability."])

        def shaped(docs, purposes, frameworks):
            return [dict(d, purpose="A purpose." if p else "",
                         frameworks=framework_lists[f])
                    for d, p, f in zip(docs, purposes, frameworks)]

        cases = (
            (shaped(one[:1], [1], [1]),
             "Search the 1 document across the 1 domain by title, type, "
             "domain, and purpose, and by the frameworks a document maps to, "
             "where it has any."),
            (shaped(two, [1, 1, 1], [1, 1, 2]),
             "Search the 3 documents across the 2 domains by title, type, "
             "domain, and purpose, and by the frameworks a document maps to, "
             "where it has any."),
            (shaped(one, [1, 1, 1], [0, 0, 0]),
             "Search the 3 documents across the 1 domain by title, type, "
             "domain, and purpose."),
            (shaped(one, [1, 1, 1], [2, 0, 0]),
             "Search the 3 documents across the 1 domain by title, type, "
             "domain, and purpose, and by the frameworks a document maps to, "
             "where it has any."),
            (shaped(two, [1, 0, 1], [1, 2, 0]),
             "Search the 3 documents across the 2 domains by title, type, and "
             "domain, by purpose for the 2 that state one, and by the "
             "frameworks a document maps to, where it has any."),
            (shaped(two, [0, 1, 0], [0, 0, 0]),
             "Search the 3 documents across the 2 domains by title, type, and "
             "domain, and by purpose for the 1 that states one."),
        )
        for subset, prompt in cases:
            with self.subTest(prompt=prompt):
                values = self.mod.draft_search_values(subset, [])
                self.assertEqual(values["SEARCH_PROMPT"], prompt)
                self.assertEqual(
                    values["SEARCH_ROWS"].count("<li data-search="),
                    len(subset))
        # With adopter documents in the pool (site a9) the prompt counts the
        # two pools apart, singular for one, and the field is the row's area.
        fixture_guide = {
            "path": "docs/fixture.md", "domain": "docs", "type": "Guide",
            "title": "Fixture Guide", "date": "2026-11-03",
            "purpose": "A purpose.", "frameworks": [],
        }
        values = self.mod.draft_search_values(
            shaped(one[:1], [1], [1]), [fixture_guide])
        self.assertEqual(
            values["SEARCH_PROMPT"],
            "Search the 2 documents listed below, the 1 corpus document "
            "across the 1 domain and the 1 adopter document under docs/, by "
            "title, type, area, and purpose, and by the frameworks a "
            "document maps to, where it has any.")
        self.assertEqual(
            values["SEARCH_ROWS"].count("<li data-search="), 2)
        adopter = self.mod.parse_adopter_docs()
        values = self.mod.draft_search_values(domain_docs, adopter)
        self.assertEqual(values["SEARCH_ROWS"].count("<li data-search="),
                         len(domain_docs) + len(adopter))
        self.assertTrue(values["SEARCH_PROMPT"].startswith(
            f"Search the {len(domain_docs) + len(adopter)} documents listed "
            f"below, the {len(domain_docs)} corpus documents across the "))
        template = (REPO_ROOT / ".web" / "templates-draft"
                    / "search.html").read_text(encoding="utf-8")
        self.assertIn(">{{SEARCH_PROMPT}}</p>", template,
                      "the prompt is the generated value, never typed copy")

    # -- 9. the documents index (design A PR A3) ------------------------------

    _INDEX_REL = "draft/documents/index.html"
    _CHIP_RE = re.compile(
        r'<li><a href="([^"]*)">([^<]*)<span class="n">(\d+)</span></a></li>')

    def _full_taxonomy(self):
        return self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))

    def _index_scope(self):
        index = self.draft_html[self._INDEX_REL]
        scopes = re.findall(
            r"<ul[^>]* data-search-scope>(.*?)</ul>", index, re.S)
        self.assertEqual(len(scopes), 1,
                         "the index carries exactly one [data-search-scope]")
        return scopes[0]

    def _index_rows(self):
        return self._SEARCH_ROW_RE.findall(self._index_scope())

    def _index_block(self, label):
        index = self.draft_html[self._INDEX_REL]
        block = re.search(
            rf'<p class="lbl blk">{label}</p>\s*<ul[^>]*>(.*?)</ul>',
            index, re.S)
        self.assertIsNotNone(block, f"the index has no {label} list")
        return block.group(1)

    def test_documents_index_has_one_row_per_non_root_taxonomy_path(self):
        expected = [
            self.mod._doc_page_url("/draft", d["path"])
            for d in self._full_taxonomy()
            if d.get("domain") != self.mod.ROOT_DOMAIN
        ]
        self.assertTrue(expected)
        hrefs = [href for _, href in self._index_rows()]
        self.assertEqual(len(hrefs), len(expected),
                         "one index row per non-root taxonomy path")
        self.assertEqual(len(set(hrefs)), len(hrefs),
                         "no document is listed twice")
        self.assertEqual(set(hrefs), set(expected),
                         "the rows link exactly the non-root taxonomy paths")
        for href in hrefs:
            self.assertIn(_page_rel_for(href), self.draft_html,
                          f"index row links a missing page: {href}")

    def test_documents_index_rows_run_in_title_order(self):
        """Design B 4.3: rows are emitted A to Z by title, path breaking a
        tie, and filtering never reorders them."""
        docs = sorted(
            (d for d in self._full_taxonomy()
             if d.get("domain") != self.mod.ROOT_DOMAIN),
            key=lambda d: (d.get("title", "").lower(), d["path"]))
        self.assertEqual(
            [href for _, href in self._index_rows()],
            [self.mod._doc_page_url("/draft", d["path"]) for d in docs])

    def test_documents_index_prose_is_true_for_every_row(self):
        """The page prose rule, on the index: the meta line says every listed
        document has its own page and the list runs A to Z, generated from
        the library; the list heading names the documents its list holds,
        read off the rendered heading (round-2 review: "Every document" sat
        over a list that leaves out the library specifications)."""
        index = self.draft_html[self._INDEX_REL]
        meta = re.search(r'<p class="meta">(.*?)</p>', index, re.S)
        self.assertIsNotNone(meta)
        text = " ".join(meta.group(1).split())
        self.assertIn(" areas, each with its own page, listed by title from "
                      "A to Z, plus ", text)
        self.assertIn(
            "The list is generated from the library at build time, so a "
            "document added or removed appears or drops out on the next "
            "build.", text)
        heading = re.search(
            r"<h2>Every document(?P<scope> in a corpus area)?, A to Z</h2>",
            index)
        self.assertIsNotNone(heading, "the list heading is not recognized")
        listed = sorted(
            (d for d in self._full_taxonomy()
             if heading.group("scope") is None
             or d.get("domain") != self.mod.ROOT_DOMAIN),
            key=lambda d: (d.get("title", "").lower(), d["path"]))
        hrefs = [href for _, href in self._index_rows()]
        self.assertEqual(
            hrefs,
            [self.mod._doc_page_url("/draft", d["path"]) for d in listed],
            "the list holds, A to Z, exactly the documents its heading names")
        for href in hrefs:
            self.assertIn(_page_rel_for(href), self.draft_html,
                          f"{href}: a listed document has its own page")

    def test_documents_index_rows_carry_the_search_text(self):
        """Each row's data-search text holds the title, type, area, the
        full purpose and every framework name (the PR 2d row shape), so the
        search.js text filter matches what the page says it matches."""
        index = self.draft_html[self._INDEX_REL]
        self.assertIn(
            "<p>With script, typing narrows the list to the documents whose "
            "title, type, area, purpose, or framework names match every word; "
            "without it, the whole list stays as it is.</p>", index)
        hay_by_href = {href: unescape(hay)
                       for hay, href in self._index_rows()}

        def collapsed(text):
            return " ".join(text.lower().split())

        for d in self._full_taxonomy():
            if d.get("domain") == self.mod.ROOT_DOMAIN:
                continue
            href = self.mod._doc_page_url("/draft", d["path"])
            hay = hay_by_href[href]
            parts = [d.get("title", ""), d.get("type", ""),
                     self.mod.draft_domain_label(d.get("domain", "")),
                     d.get("purpose", "") or ""] + d.get("frameworks", [])
            for part in parts:
                if part:
                    self.assertIn(collapsed(part), hay,
                                  f"{href}: data-search lacks {part[:60]!r}")
        index_rows = {href: hay for hay, href in self._index_rows()}
        search_rows = {href: hay for hay, href in self._search_rows()}
        self.assertEqual(
            index_rows,
            {href: search_rows[href] for href in index_rows
             if href in search_rows},
            "an index row and its search page row carry the same text")
        # The search page's extra rows are exactly the docs/ adopter
        # documents (site a9); the index stays the corpus index its prose
        # describes.
        self.assertEqual(
            set(search_rows) - set(index_rows),
            {self.mod._doc_page_url("/draft", g["path"])
             for g in self.mod.parse_adopter_docs()})

    def test_documents_index_wires_the_filter_scope_search_js_expects(self):
        """search.js takes the first [data-search] element as its form, the
        input[type=search] and [data-search-status] inside it, and every li
        of the first [data-search-scope] as a row."""
        index = self.draft_html[self._INDEX_REL]
        self.assertIn(
            '<script src="/draft/assets/baseline/search.js" defer></script>',
            index, "the index loads the baseline search.js")
        first = re.search(r"<([a-z]+)\b[^>]*\sdata-search(?=[\s>=])", index)
        self.assertIsNotNone(first)
        self.assertEqual(first.group(1), "form",
                         "the first [data-search] element is the form")
        form = re.search(r"<form\b[^>]*\sdata-search>(.*?)</form>", index,
                         re.S)
        self.assertIsNotNone(form)
        self.assertRegex(form.group(1), r'<input id="q" type="search"')
        self.assertRegex(form.group(1), r'<label[^>]* for="q">')
        self.assertRegex(
            form.group(1), r'role="status"[^>]*\sdata-search-status')
        self.assertEqual(index.count("data-search-scope"), 1)
        scope = self._index_scope()
        items = re.findall(r"<li\b[^>]*>", scope)
        self.assertTrue(items)
        for item in items:
            self.assertIn("data-search=", item,
                          "every li in the scope is a filterable row")
        self.assertEqual(index.count('<li data-search="'), len(items),
                         "no row carries data-search outside the scope")
        self.assertLess(index.find("data-search>"),
                        index.find("data-search-scope"),
                        "the filter form sits above the list")

    def test_documents_index_chips_link_domain_and_type_pages(self):
        """The chips are plain links (design B 4.5): areas to the domain
        pages, each counting the area's rows, and types to the design A
        routes types/<slug>/, each counting every document of the type, root
        specifications included, as its type page does (round-1 ERROR: the
        Specification chip counted 3 of the 5)."""
        domains = {}
        types = {}
        for d in self._full_taxonomy():
            types[d["type"]] = types.get(d["type"], 0) + 1
            if d.get("domain") == self.mod.ROOT_DOMAIN:
                continue
            domains[d["domain"]] = domains.get(d["domain"], 0) + 1
        areas = self._CHIP_RE.findall(self._index_block("By area"))
        self.assertEqual(
            {href: int(n) for href, _, n in areas},
            {f"/draft/{dom}/": n for dom, n in domains.items()})
        for href, label, _ in areas:
            self.assertEqual(
                label, self.mod._esc(self.mod.draft_domain_label(
                    href.split("/")[2])))
        type_chips = self._CHIP_RE.findall(self._index_block("By type"))
        self.assertEqual(
            {href: (label, int(n)) for href, label, n in type_chips},
            {f"/draft/types/{self.mod.type_slug(t)}/": (t, n)
             for t, n in types.items()})

    def test_documents_index_type_chips_count_what_their_type_pages_list(self):
        """Each type chip's count equals the corpus rows its type page lists
        and the corpus count the page states, and every type page has a
        chip. Integration round 2: a type page also lists the type's adopter
        documents, which All Documents does not carry, in their own counted
        block, so the page's total is the chip's count plus that block's and
        the page states the corpus count apart."""
        type_chips = self._CHIP_RE.findall(self._index_block("By type"))
        type_pages = {rel for rel in self.draft_html
                      if rel.startswith("draft/types/")}
        self.assertEqual({_page_rel_for(href) for href, _, _ in type_chips},
                         type_pages, "one chip per type page")
        adopter_label = re.escape(self.mod._esc(
            self.mod.draft_domain_label(self.mod.ADOPTER_DOCS_AREA)))
        for href, label, n in type_chips:
            with self.subTest(type=label):
                page = self.draft_html[_page_rel_for(href)]
                scope = re.search(
                    r'<ul class="plan one described">(.*?)</ul>', page, re.S)
                self.assertIsNotNone(scope, "the type page has no list")
                self.assertEqual(
                    int(n), len(self._TYPE_ROW_RE.findall(scope.group(1))),
                    "the chip counts the rows its type page lists")
                adopter = re.search(
                    rf'<p class="lbl blk">{adopter_label}, (\d+)</p>', page)
                if adopter:
                    self.assertIn(f": {n} in the corpus and "
                                  f"{adopter.group(1)} adopter ", page,
                                  "the page states the chip's corpus count")
                    shown = int(n) + int(adopter.group(1))
                else:
                    shown = int(n)
                self.assertIn(f"Documents, {shown}</p>", page)

    def test_documents_index_counts_a_type_only_root_documents_hold(self):
        """Every type in today's corpus has a non-root document, so the live
        render cannot tell the two counts apart; a fixture can. A type held
        only by root specifications still has a type page, so it gets a chip
        and counts among the index's types."""
        root = self.mod.ROOT_DOMAIN
        values = self.mod.draft_documents_values([
            {"path": "governance/policy-a.md", "domain": "governance",
             "type": "Policy", "title": "A"},
            {"path": "specification-b.md", "domain": root,
             "type": "Specification", "title": "B"},
        ])
        self.assertEqual(values["INDEX_TYPE_COUNT"], "2")
        self.assertIn('/types/specification/">Specification'
                      '<span class="n">1</span>', values["INDEX_TYPE_CHIPS"])

    def test_documents_index_is_named_all_documents(self):
        """Maintainer decision: the index is All Documents, in its title,
        label and heading, and in the Next label of every document page."""
        index = self.draft_html[self._INDEX_REL]
        self.assertIn("<title>All Documents | GRCLibrary.ai</title>", index)
        self.assertIn('<p class="lbl first">All Documents</p>', index)
        self.assertIn("<h1>All Documents</h1>", index)
        for rel in self._doc_pages():
            self.assertIn(
                '<p class="lbl">Next</p><a class="start" '
                'href="/draft/documents/">All Documents <span',
                self.draft_html[rel], rel)

    def test_browse_links_all_documents_outside_the_top_bar(self):
        """The Browse body links the index by name, and its sentence about
        the index holds on the rendered index: every library document is
        linked there (its page, or its GitHub source for a library
        specification), and the filter covers exactly the documents across
        the domains (round-2 review: "the whole library in one list you can
        filter" left out the library specifications, which sit outside the
        filtered list). Integration round 2 NOTE: All Documents carries the
        corpus, not the docs/ adopter documents, so the sentence says every
        corpus document and points to the Browse list that carries every
        adopter document."""
        browse = self.draft_html["draft/browse/index.html"]
        main = browse.split('<main id="main-content">', 1)[1]
        self.assertIn('<a href="/draft/documents/">All Documents</a>', main,
                      "the Browse page body links the index by name")
        self.assertNotIn("/draft/documents/", _NAV_RE.search(browse).group(1),
                         "the top bar is unchanged in this PR")
        label = self.mod._esc(
            self.mod.draft_domain_label(self.mod.ADOPTER_DOCS_AREA))
        self.assertIn(
            "<p>To see every corpus document on one page, open "
            '<a href="/draft/documents/">All Documents</a>; its filter covers '
            "the documents across the domains. The adopter documents, outside "
            "the corpus, are listed further down this page, under "
            f"{label}.</p>", main)
        self.assertNotIn("every document in the library", main)
        after = main.split("open <a href=\"/draft/documents/\">", 1)[1]
        section = re.search(
            rf'<h2 id="adopter-documents">{re.escape(label)}</h2>\s*'
            r'<p>[^<]*</p>\s*<div class="wide"><ul class="plan described">'
            r"(.*?)</ul>", after, re.S)
        self.assertIsNotNone(section, "the adopter list sits further down")
        self.assertEqual(
            sorted(_HREF_RE.findall(section.group(1))),
            sorted(self.mod._doc_page_url("/draft", g["path"])
                   for g in self.mod.parse_adopter_docs()),
            "the list under the label carries every adopter document")
        self._assert_index_links_every_corpus_document()

    def test_govern_names_all_documents_by_its_corpus_scope(self):
        """Integration round 2 NOTE: govern said All Documents shows every
        library document, but it omits the docs/ adopter documents; the
        sentence says every corpus document, checked on the rendered
        index."""
        govern = self.draft_html["draft/govern/index.html"]
        self.assertIn(
            '<a href="/draft/documents/">All Documents</a> to see every '
            "corpus document on one page;", govern)
        self.assertNotIn("every library document", govern)
        self._assert_index_links_every_corpus_document()

    def _assert_index_links_every_corpus_document(self):
        """Every taxonomy document is linked on All Documents (its page, or
        its GitHub source for a library specification), and the filter rows
        are exactly the documents across the domains."""
        index = self.draft_html[self._INDEX_REL]
        linked = {unescape(href) for href in _HREF_RE.findall(
            index.split('<main id="main-content">', 1)[1])}
        domain_hrefs = set()
        for d in self._full_taxonomy():
            if d.get("domain") == self.mod.ROOT_DOMAIN:
                href = self.mod.GITHUB_BLOB_BASE + d["path"]
            else:
                href = self.mod._doc_page_url("/draft", d["path"])
                domain_hrefs.add(href)
            self.assertIn(href, linked,
                          f"{d['path']}: not on the All Documents page")
        self.assertEqual({href for _, href in self._index_rows()},
                         domain_hrefs,
                         "the filter covers the documents across the domains")

    def test_root_specifications_carry_one_area_label(self):
        """A root specification sits in no corpus area; the index and the
        type pages give it the same area label, in the same slot."""
        label = self.mod.draft_domain_label(self.mod.ROOT_DOMAIN)
        self.assertNotIn(
            label,
            {self.mod.draft_domain_label(dom) for dom in self.mod.DOMAIN_SCOPE},
            "the root label names no corpus area")
        roots = [d for d in self._full_taxonomy()
                 if d.get("domain") == self.mod.ROOT_DOMAIN]
        self.assertTrue(roots)
        block = self._index_block("Library specifications")
        self.assertEqual(
            sorted(re.findall(r'<span class="n">([^<]*)</span>', block)),
            sorted(self.mod._esc(f"{d['type'].lower()}, {label}")
                   for d in roots),
            "an index root row reads type, area like every other row")
        for d in roots:
            page = self.draft_html[self._type_rel(d["type"])]
            areas = {href: area for href, _, area, _
                     in self._TYPE_ROW_RE.findall(page)}
            self.assertEqual(
                areas[self.mod.GITHUB_BLOB_BASE + d["path"]],
                self.mod._esc(label), d["path"])

    def test_documents_index_links_root_specifications_to_github(self):
        roots = [d for d in self._full_taxonomy()
                 if d.get("domain") == self.mod.ROOT_DOMAIN]
        self.assertTrue(roots)
        block = self._index_block("Library specifications")
        self.assertEqual(
            sorted(_HREF_RE.findall(block)),
            sorted(self.mod._esc(self.mod.GITHUB_BLOB_BASE + d["path"])
                   for d in roots),
            "each root specification opens its GitHub source")
        self.assertEqual(block.count("(opens in a new tab)"), len(roots))
        scope = self._index_scope()
        for d in roots:
            self.assertNotIn(self.mod.GITHUB_BLOB_BASE + d["path"], scope,
                             "root specifications stay out of the filter rows")

    def test_document_pages_next_leads_to_the_documents_index(self):
        """Design A NOTE-1: a document page's Next is the documents index,
        not the search page."""
        for rel in self._doc_pages():
            nxt = re.search(
                r'<div class="next"><p class="lbl">Next</p>'
                r'<a class="start" href="([^"]*)">', self.draft_html[rel])
            self.assertIsNotNone(nxt, rel)
            self.assertEqual(nxt.group(1), "/draft/documents/", rel)

    # -- 10. the executive layer ----------------------------------------------

    def test_every_narrative_registry_page_renders_on_the_draft(self):
        narratives = self.figures["narratives"]
        self.assertTrue(narratives)
        rendered = {rel for rel in self.draft_html
                    if rel.startswith("draft/decisions/")}
        expected = {_page_rel_for(_reading_room_href(p)) for p in narratives}
        self.assertEqual(rendered, expected,
                         "exactly one draft reading-room page per registry "
                         "narrative page")
        for page in narratives:
            rel = _page_rel_for(_reading_room_href(page))
            html = self.draft_html[rel]
            with self.subTest(page=page["path"]):
                self.assertIn(
                    f'<p class="lbl first">{self.mod._esc(page["narrative_type"])}'
                    f'</p>\n<h1>{self.mod._esc(page["title"])}</h1>', html)
                self.assertIn('<section class="narr">', html,
                              "the body comes from the constrained renderer")
                rail = _RAIL_RE.search(html)
                self.assertIsNotNone(rail, f"{rel}: the sections rail")
                self.assertIn('href="#', rail.group(0))
                self.assertIn(
                    f'href="{self.mod.GITHUB_BLOB_BASE}{page["path"]}"', html,
                    f"{rel}: links its Markdown source")
                chips = re.search(r'<ul class="chips">(.*?)</ul>', html, re.S)
                self.assertIsNotNone(chips, f"{rel}: domain chips")
                self.assertEqual(
                    _HREF_RE.findall(chips.group(1)),
                    [f"/draft/{d}/" for d in page["domains"]],
                    f"{rel}: the chips are the registry's domain tags")

    def test_every_subtype_index_lists_exactly_its_pages(self):
        narratives = self.figures["narratives"]
        rendered = {rel for rel in self.draft_html
                    if rel.startswith("draft/decide/")}
        expected = {"draft/decide/index.html"}
        expected |= {f"draft/decide/{s}/index.html" for s in SUBTYPE_SLUGS}
        expected |= {f"draft/decide/{c['slug']}/index.html"
                     for c in self.mod.DRAFT_CONCERNS}
        self.assertEqual(
            rendered, expected,
            "exactly the hub, the six reconciled subtype index routes and "
            "the concern topic pages render under decide/")
        counts = {}
        for p in narratives:
            counts[p["narrative_type"]] = counts.get(p["narrative_type"], 0) + 1
        listed = set()
        for narrative_type, (slug, label, question) in (
                self.mod.DRAFT_NARRATIVE_SUBTYPES.items()):
            html = self.draft_html[f"draft/decide/{slug}/index.html"]
            block = re.search(
                r'<h2 id="pages">.*?<ul class="plan one described">(.*?)</ul>',
                html, re.S)
            self.assertIsNotNone(block, f"{slug}: the pages list")
            hrefs = _ROW_HREF_RE.findall(block.group(1))
            expected = [_reading_room_href(p) for p in narratives
                        if p["narrative_type"] == narrative_type]
            with self.subTest(subtype=slug):
                self.assertEqual(len(hrefs), len(set(hrefs)), "no repeated row")
                self.assertEqual(set(hrefs), set(expected),
                                 "one row per registry page of the type, "
                                 "and no other")
                self.assertIn(f"{label}, {len(expected)}</p>", html,
                              "the generated count")
                # Round-1 WARN: the meta line's count and the sibling counts
                # had no test, so an off-by-one at either passed.
                noun = "page" if len(expected) == 1 else "pages"
                self.assertIn(
                    f'<p class="meta">{len(expected)} {noun}. '
                    f"{self.mod._esc(question)}</p>", html,
                    "the meta line's generated count")
                kinds = re.search(
                    r'<h2 id="kinds">.*?<ul class="plan">(.*?)</ul>',
                    html, re.S)
                self.assertIsNotNone(kinds, f"{slug}: the other kinds list")
                self.assertEqual(
                    dict(re.findall(
                        r'<li><a href="([^"]*)">[^<]*</a>'
                        r'<span class="n">([^<]*)</span></li>',
                        kinds.group(1))),
                    {f"/draft/decide/{other_slug}/":
                         str(counts.get(other, 0))
                     for other, (other_slug, _, _) in (
                         self.mod.DRAFT_NARRATIVE_SUBTYPES.items())
                     if other != narrative_type},
                    "each other kind carries its registry count")
            listed.update(hrefs)
        self.assertEqual(listed, {_reading_room_href(p) for p in narratives},
                         "the six indexes together list every registry page")

    def test_every_domain_leadership_section_matches_the_registry_join(self):
        narratives = self.figures["narratives"]
        for dp in self.figures["domain_pages"]:
            domain = dp["domain"]
            joined = sorted(
                (p for p in narratives if domain in p["domains"]),
                key=lambda p: (p["narrative_type"], p["title"].lower(),
                               p["path"]),
            )
            html = self.draft_html[f"draft/{domain}/index.html"]
            with self.subTest(domain=domain):
                self.assertIn(
                    f'<li><a href="#leadership">Leadership, {len(joined)}'
                    "</a></li>", _RAIL_RE.search(html).group(0),
                    "the rail lists the section with its generated count")
                # Round-1 WARN: the section label's count had no test.
                self.assertIn(
                    f'<p class="lbl sec">Leadership, {len(joined)}</p>\n'
                    '<h2 id="leadership">', html,
                    "the section label carries the generated count")
                if not joined:
                    self.assertIn("a declared coverage gap, not a hidden one",
                                  html.split('<h2 id="leadership">', 1)[1])
                    continue
                section = re.search(
                    r'<h2 id="leadership">.*?<ul class="plan one">(.*?)</ul>',
                    html, re.S)
                self.assertIsNotNone(section, f"{domain}: leadership section")
                self.assertEqual(
                    _ROW_HREF_RE.findall(section.group(1)),
                    [_reading_room_href(p) for p in joined],
                    "the rows are the registry join, in order")

    def test_every_executive_page_carries_the_authority_qualifier(self):
        """Round-1 WARN: removing any clause of the layer's authority
        qualifier passed every test. Every reading-room page, every subtype
        index and every domain page's leadership section carries it whole."""
        for page in self.figures["narratives"]:
            rel = _page_rel_for(_reading_room_href(page))
            with self.subTest(page=rel):
                self.assertIn(NARRATIVE_QUALIFIER, self.draft_html[rel])
        for slug in sorted(SUBTYPE_SLUGS):
            rel = f"draft/decide/{slug}/index.html"
            with self.subTest(page=rel):
                self.assertIn(SUBTYPE_QUALIFIER, self.draft_html[rel])
        for dp in self.figures["domain_pages"]:
            rel = f"draft/{dp['domain']}/index.html"
            with self.subTest(page=rel):
                self.assertIn(LEADERSHIP_QUALIFIER, self.draft_html[rel])

    # -- 11. the executive path hub and the concern topic pages --------------

    # The layer's authority qualifier (carried from templates-v2/decisions.html
    # via the subtype indexes), required visible on the hub and every concern
    # page: the pages explain; the corpus governs. Round-2 (page prose rule):
    # the hub links no leadership page itself, so it names the pages the path
    # leads to; a declared-gap concern page links none, so it carries the
    # gap form instead of claiming linked pages.
    QUALIFIER_SENTENCE = (
        "The leadership pages linked here are explanatory and advisory; they "
        "establish no requirement and prove nothing about your organization. "
        "Every claim in them resolves to the governing reference documents in "
        "the corpus, and it is those documents that govern."
    )
    # Round-3 WARN: the hub's opening sentence also said "a page here".
    HUB_QUALIFIER_SENTENCE = (
        "Adopting a page this path leads to decides nothing for you. The "
        "leadership pages this path leads to are explanatory and advisory; "
        "they establish no requirement and prove nothing about your "
        "organization. Every claim in them resolves to the governing reference "
        "documents in the corpus, and it is those documents that govern."
    )
    # Round-3 NOTE: the shelf sentences agree in number with the shelf, so
    # each is pinned in both forms, keyed by whether the shelf holds exactly
    # one document.
    GAP_QUALIFIER = {
        True: (
            '<div class="callout"><p>No leadership page is linked here yet. '
            "The document below is a governing reference document in the "
            "corpus, and it is that document that governs.</p></div>"
        ),
        False: (
            '<div class="callout"><p>No leadership page is linked here yet. '
            "The documents below are governing reference documents in the "
            "corpus, and it is those documents that govern.</p></div>"
        ),
    }
    GAP_MATERIAL = {
        True: "The governing document below is the corpus material that "
              "supports the concern today.</p></div>",
        False: "The governing documents below are the corpus material that "
               "supports the concern today.</p></div>",
    }
    # Round-2 ERROR 1: the hub lead claimed every list was generated, while
    # the concern groups are the curated DRAFT_CONCERNS table.
    HUB_LEAD = (
        '<p class="lead">Start from the concern you own, the kind of page you '
        "need, or the domain you oversee. The concerns, their board-question "
        "groups and the kinds of page are curated in the site generator; the "
        "counts beside them and the domain list are generated at build time. "
        "A newly published leadership page fails the build until it is mapped "
        "to a concern, so every published leadership page appears on at least "
        "one concern page.</p>"
    )
    # Round-2 ERROR 3 and WARN 2: the leadership and evidence-shelf intros,
    # each in the form true for its case.
    LEADERSHIP_INTRO = (
        "<p>Pages from the executive layer mapped to this concern, generated "
        "from the narrative registry. They explain and advise; the documents "
        "below govern.</p>"
    )
    DOCS_INTRO_PAGES = {
        True: (
            "<p>The evidence shelf: the corpus document the pages above "
            "resolve to, joined to the library's registries at build time. "
            "This is the document that governs, and the evidence to ask for "
            "starts here.</p>"
        ),
        False: (
            "<p>The evidence shelf: the corpus documents the pages above "
            "resolve to, joined to the library's registries at build time. "
            "These are the documents that govern, and the evidence to ask for "
            "starts here.</p>"
        ),
    }
    DOCS_INTRO_GAP = {
        True: (
            "<p>The evidence shelf: with no leadership page to resolve from, "
            "this is the corpus document chosen for this concern, checked "
            "against the taxonomy at build time. This is the document that "
            "governs, and the evidence to ask for starts here.</p>"
        ),
        False: (
            "<p>The evidence shelf: with no leadership page to resolve from, "
            "these are the corpus documents chosen for this concern, each "
            "checked against the taxonomy at build time. These are the "
            "documents that govern, and the evidence to ask for starts "
            "here.</p>"
        ),
    }
    # The frameworks intro is count-neutral: it sits over a shelf of any
    # size. The crosswalk ships on this branch, so the intro says which
    # names link and which stay plain text (WARN fix: the old sentence said
    # the crosswalk page was not built yet; integration round 2: a name
    # citing an instrument by a clause links too, and a compound links each;
    # integration round 3: a compound's part naming another text is plain).
    FRAMEWORKS_INTRO = (
        "<p>The external frameworks the shelf above maps, from the corpus "
        "registry. A name that cites a crosswalk instrument, whole or by a "
        "clause, links its instrument page; in a name joining several texts, "
        "each part that names a crosswalk instrument links its page and any "
        "other part is plain text; any other name is shown as plain "
        "text.</p>"
    )

    def _concern_joins(self):
        """The concern joins recomputed here from the registries (not through
        build.py's join helper), keyed by slug: (concern, mapped pages in the
        registry-join order, governing documents in type-rank order)."""
        by_path = {p["path"]: p for p in self.figures["narratives"]}
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        docs_by_path = {d["path"]: d for d in full}
        joins = {}
        for concern in self.mod.DRAFT_CONCERNS:
            pages = sorted(
                (by_path[p] for p in concern["pages"]),
                key=lambda p: (p["narrative_type"], p["title"].lower(),
                               p["path"]))
            doc_paths = sorted({s for p in pages for s in p["sources"]}
                               | set(concern["corpus"]))
            docs = sorted(
                (docs_by_path[dp] for dp in doc_paths),
                key=lambda d: (
                    self.mod.TYPE_RANK.get(d.get("type"),
                                           len(self.mod.TYPE_ORDER)),
                    d.get("title", "").lower(), d["path"]))
            joins[concern["slug"]] = (concern, pages, docs)
        return joins

    @staticmethod
    def _concern_counts_text(pages, docs):
        pages_noun = ("leadership page" if len(pages) == 1
                      else "leadership pages")
        docs_noun = ("governing document" if len(docs) == 1
                     else "governing documents")
        return f"{len(pages)} {pages_noun}, {len(docs)} {docs_noun}"

    def test_decide_hub_groups_every_concern_with_generated_counts(self):
        hub = self.draft_html["draft/decide/index.html"]
        joins = self._concern_joins()
        hrefs = []
        for group_slug, board_question in self.mod.DRAFT_DECIDE_GROUPS:
            section = re.search(
                rf'<h2 id="g-{group_slug}">(.*?)</h2>\n'
                r'<div class="wide"><ul class="plan described">(.*?)</ul>',
                hub, re.S)
            self.assertIsNotNone(section, group_slug)
            self.assertEqual(section.group(1),
                             self.mod._esc(board_question),
                             "the group heading is the board question")
            hrefs += _ROW_HREF_RE.findall(section.group(2))
        self.assertEqual(
            hrefs,
            [f"/draft/decide/{c['slug']}/" for c in self.mod.DRAFT_CONCERNS],
            "the three groups together list every concern exactly once, in "
            "table order")
        for concern, pages, docs in joins.values():
            counts = self._concern_counts_text(pages, docs)
            if not pages:
                counts = "declared gap: " + counts
            row = (f'<li><a href="/draft/decide/{concern["slug"]}/">'
                   f'{self.mod._esc(concern["question"])}</a>'
                   f'<span class="n">{counts}</span>'
                   f'<small>{self.mod._esc(concern["label"])}</small></li>')
            self.assertIn(row, hub, concern["slug"])

    def test_decide_hub_kinds_branch_lists_the_six_indexes(self):
        hub = self.draft_html["draft/decide/index.html"]
        block = re.search(
            r'<h2 id="kinds">.*?<ul class="plan described">(.*?)</ul>',
            hub, re.S)
        self.assertIsNotNone(block)
        hrefs = _ROW_HREF_RE.findall(block.group(1))
        self.assertEqual(set(hrefs),
                         {f"/draft/decide/{s}/" for s in SUBTYPE_SLUGS},
                         "one row per subtype index")
        for narrative_type, (slug, label, _) in (
                self.mod.DRAFT_NARRATIVE_SUBTYPES.items()):
            count = sum(1 for p in self.figures["narratives"]
                        if p["narrative_type"] == narrative_type)
            self.assertIn(
                f'<li><a href="/draft/decide/{slug}/">{label}</a>'
                f'<span class="n">{count}</span>', block.group(1),
                f"{slug}: the generated count")

    def test_decide_hub_domain_branch_is_the_browse_list_unchanged(self):
        hub = self.draft_html["draft/decide/index.html"]
        browse = self.draft_html["draft/browse/index.html"]
        hub_block = re.search(
            r'<h2 id="domains">.*?<ul class="plan described">(.*?)</ul>',
            hub, re.S)
        browse_block = re.search(
            r'<h2 id="domains">.*?<ul class="plan described">(.*?)</ul>',
            browse, re.S)
        self.assertIsNotNone(hub_block)
        self.assertIsNotNone(browse_block)
        self.assertEqual(hub_block.group(1), browse_block.group(1),
                         "branch 3 is the Browse By domain list, unchanged")

    def test_concern_leadership_equals_the_registry_join(self):
        for slug, (concern, pages, _) in self._concern_joins().items():
            html = self.draft_html[f"draft/decide/{slug}/index.html"]
            with self.subTest(concern=slug):
                if not pages:
                    continue  # the declared-gap test below covers this shape
                section = re.search(
                    r'<h2 id="leadership">.*?<ul class="plan one">(.*?)</ul>',
                    html, re.S)
                self.assertIsNotNone(section, f"{slug}: leadership list")
                self.assertEqual(
                    _ROW_HREF_RE.findall(section.group(1)),
                    [_reading_room_href(p) for p in pages],
                    "the rows are the registry join, in order")
                for page in pages:
                    self.assertIn(
                        f'<span class="n">'
                        f'{self.mod._esc(page["narrative_type"].lower())}'
                        f"</span>", section.group(1),
                        f"{slug}: each row carries its type label")

    def test_concern_documents_equal_the_source_union_joined_to_taxonomy(self):
        for slug, (concern, _, docs) in self._concern_joins().items():
            html = self.draft_html[f"draft/decide/{slug}/index.html"]
            section = re.search(
                r'<h2 id="documents">.*?<ul class="plan one">(.*?)</ul>',
                html, re.S)
            with self.subTest(concern=slug):
                self.assertIsNotNone(section, f"{slug}: documents list")
                hrefs = _ROW_HREF_RE.findall(section.group(1))
                self.assertEqual(len(hrefs), len(set(hrefs)),
                                 "no repeated document row")
                self.assertEqual(
                    hrefs,
                    [f"/draft/documents/{d['path'][:-3]}/" for d in docs],
                    "the rows are the deduplicated corpus-source union, "
                    "joined to the taxonomy, in type-rank order")
                for d in docs:
                    self.assertIn(
                        f'<span class="n">'
                        f'{self.mod._esc(d["type"].lower())}, '
                        f'{self.mod._esc(self.mod.draft_domain_label(d["domain"]))}'
                        f"</span>", section.group(1),
                        f"{slug}: each row carries the taxonomy type and "
                        "domain")

    def test_concern_frameworks_are_the_union_linked_where_aliased(self):
        """WARN fix: the crosswalk ships on this branch, so each framework
        name whose exact spelling the committed alias map carries links its
        crosswalk instrument page (a rendered page), a compound the parts
        map carries links each part to its own page (integration round 2),
        and any other name stays plain text, exactly as the page's own
        sentence says; checked
        on every rendered concern page. Both forms must occur today, so a
        regression in either direction fails."""
        linked_any = plain_any = False
        for slug, (concern, _, docs) in self._concern_joins().items():
            html = self.draft_html[f"draft/decide/{slug}/index.html"]
            block = re.search(
                r'<h2 id="frameworks">(.*?)<p class="lbl sec">Go deeper</p>',
                html, re.S)
            expected = sorted({f for d in docs
                               for f in d.get("frameworks", [])})
            with self.subTest(concern=slug):
                self.assertIsNotNone(block, f"{slug}: frameworks block")
                if not expected:
                    self.assertIn("a declared gap, not a hidden one",
                                  block.group(1))
                    continue
                chips = re.search(r'<ul class="chips">(.*?)</ul>',
                                  block.group(1), re.S)
                self.assertIsNotNone(chips, f"{slug}: framework chips")
                items = re.findall(r"<li>(.*?)</li>", chips.group(1))
                self.assertEqual(len(items), len(expected),
                                 "one chip per union framework name")
                for item, name in zip(items, expected):
                    key = self.mod.CROSSWALK_ALIASES.get(name)
                    parts = self.mod.CROSSWALK_ALIAS_PARTS.get(name)
                    if parts:
                        self.assertEqual(
                            item,
                            " / ".join(
                                f'<a href="/draft/crosswalk/{k}/">'
                                f"{self.mod._esc(part)}</a>"
                                if k is not None else self.mod._esc(part)
                                for part, k in parts),
                            f"{slug}: a compound name links each instrument "
                            "part to its own page and leaves any other part "
                            "plain")
                        for _, k in parts:
                            if k is not None:
                                self.assertIn(
                                    f"draft/crosswalk/{k}/index.html",
                                    self.draft_html, slug)
                        linked_any = True
                    elif key:
                        self.assertEqual(
                            item,
                            f'<a href="/draft/crosswalk/{key}/">'
                            f"{self.mod._esc(name)}</a>",
                            f"{slug}: an aliased name links its instrument "
                            "page")
                        self.assertIn(f"draft/crosswalk/{key}/index.html",
                                      self.draft_html,
                                      f"{slug}: the linked page renders")
                        linked_any = True
                    else:
                        self.assertEqual(
                            item, self.mod._esc(name),
                            f"{slug}: a name outside the alias map stays "
                            "plain text")
                        plain_any = True
        self.assertTrue(linked_any,
                        "a concern page links an instrument page today")
        self.assertTrue(plain_any,
                        "a concern page keeps an unaliased name plain today")

    def test_concern_domain_chips_are_the_derived_domains(self):
        for slug, (concern, pages, docs) in self._concern_joins().items():
            html = self.draft_html[f"draft/decide/{slug}/index.html"]
            chips = re.search(
                r'<h2 id="domains">.*?<ul class="chips">(.*?)</ul>',
                html, re.S)
            if pages:
                expected = sorted({d for p in pages for d in p["domains"]})
            else:
                expected = sorted({d["domain"] for d in docs})
            with self.subTest(concern=slug):
                self.assertIsNotNone(chips, f"{slug}: domain chips")
                self.assertEqual(
                    _HREF_RE.findall(chips.group(1)),
                    [f"/draft/{d}/" for d in expected],
                    "the Go deeper chips are the derived domains")

    def test_declared_gap_concern_renders_its_gap_block(self):
        gaps = [c for c in self.mod.DRAFT_CONCERNS if not c["pages"]]
        self.assertTrue(gaps, "the concern set carries a declared gap today "
                              "(programme-maturity, design D item G2)")
        for concern in gaps:
            html = self.draft_html[f"draft/decide/{concern['slug']}/index.html"]
            with self.subTest(concern=concern["slug"]):
                gap_block = html.split('<h2 id="leadership">', 1)[1] \
                                .split('<h2 id="documents">', 1)[0]
                self.assertIn("Declared coverage gap: no leadership page is "
                              "published for this concern yet", gap_block)
                self.assertNotIn("<ul", gap_block,
                                 "the gap is stated, never padded with rows")
                self.assertTrue(concern["corpus"],
                                "a gap concern still shows corpus-only "
                                "material")
                for path in concern["corpus"]:
                    self.assertIn(f'/draft/documents/{path[:-3]}/', html,
                                  "the corpus-only material still renders")

    def test_qualifier_visible_on_hub_and_every_concern_page(self):
        hub = self.draft_html["draft/decide/index.html"]
        self.assertIn(self.HUB_QUALIFIER_SENTENCE, hub,
                      "the hub's authority qualifier stays visible")
        self.assertNotIn("Adopting a page here", hub,
                         "the hub holds no leadership page to adopt")
        self.assertIsNone(
            re.search(r'<a href="/draft/decisions/', hub),
            "the hub links no leadership page itself, so its qualifier "
            "names the pages the path leads to")
        for slug, (concern, _, docs) in self._concern_joins().items():
            rel = f"draft/decide/{slug}/index.html"
            html = self.draft_html[rel]
            with self.subTest(page=rel):
                if concern["pages"]:
                    self.assertIn(self.QUALIFIER_SENTENCE, html,
                                  "the authority qualifier stays visible")
                    self.assertIn('href="/draft/decisions/', html,
                                  "the qualifier's linked pages exist")
                else:
                    self.assertIn(self.GAP_QUALIFIER[len(docs) == 1], html,
                                  "the gap page's qualifier stays visible")
                    self.assertNotIn("The leadership pages linked here", html)
                    self.assertNotIn('href="/draft/decisions/', html,
                                     "the gap page links no leadership page")

    def test_decide_hub_lead_claims_only_what_is_true(self):
        """Round-2 ERROR 1: the lead's claims checked against the render:
        the concern groups are the curated table (not a registry list), and
        every registry page is linked from at least one concern page."""
        hub = self.draft_html["draft/decide/index.html"]
        self.assertIn(self.HUB_LEAD, hub)
        self.assertNotIn("Every list here is generated", hub)
        linked = set()
        for concern in self.mod.DRAFT_CONCERNS:
            html = self.draft_html[f"draft/decide/{concern['slug']}/index.html"]
            linked.update(h for h in _HREF_RE.findall(html)
                          if h.startswith("/draft/decisions/"))
        for page in self.figures["narratives"]:
            with self.subTest(page=page["path"]):
                self.assertIn(_reading_room_href(page), linked,
                              "every published leadership page appears on "
                              "at least one concern page")

    def test_concern_intros_are_true_for_the_page_they_sit_on(self):
        """Round-2 ERROR 3 and WARN 2: the leadership intro renders only where
        a leadership list does, and the evidence-shelf intro says where its
        documents come from in both cases, checked on every concern page,
        including the declared-gap page."""
        joins = self._concern_joins()
        seen_gap = False
        for slug, (concern, pages, docs) in joins.items():
            html = self.draft_html[f"draft/decide/{slug}/index.html"]
            leadership = html.split('<h2 id="leadership">', 1)[1] \
                             .split('<p class="lbl sec">Documents</p>', 1)[0]
            with self.subTest(concern=slug):
                one_doc = len(docs) == 1
                if pages:
                    self.assertIn(self.LEADERSHIP_INTRO, leadership)
                    self.assertIn('<ul class="plan one">', leadership,
                                  "the intro sits above a leadership list")
                    self.assertIn(self.DOCS_INTRO_PAGES[one_doc], html)
                    self.assertNotIn(self.DOCS_INTRO_GAP[one_doc], html)
                    self.assertEqual(
                        {d["path"] for d in docs},
                        {s for p in pages for s in p["sources"]},
                        "the shelf is exactly what the pages above resolve "
                        "to, as its intro says")
                else:
                    seen_gap = True
                    self.assertNotIn("Pages from the executive layer", html)
                    self.assertNotIn("the pages above resolve to", html)
                    self.assertIn(self.DOCS_INTRO_GAP[one_doc], html)
                    self.assertEqual(
                        {d["path"] for d in docs}, set(concern["corpus"]),
                        "the gap shelf is exactly the concern's own corpus "
                        "list, as its intro says")
        self.assertTrue(seen_gap, "the declared-gap page is covered")

    def test_shelf_sentences_agree_in_number_with_the_rendered_shelf(self):
        """Round-3 NOTE: the gap page's shelf sentences were plural over a
        shelf of one document. On every concern page the evidence-shelf intro,
        and on a declared-gap page also the qualifier and the gap block's
        closing sentence, take the form for the number of rows the rendered
        shelf holds, never the other; the frameworks intro is count-neutral."""
        seen_gap = False
        for concern in self.mod.DRAFT_CONCERNS:
            html = self.draft_html[f"draft/decide/{concern['slug']}/index.html"]
            shelf = html.split('<h2 id="documents">', 1)[1] \
                        .split('<p class="lbl sec">Frameworks</p>', 1)[0]
            one_doc = len(_ROW_HREF_RE.findall(shelf)) == 1
            with self.subTest(concern=concern["slug"]):
                self.assertIn(self.FRAMEWORKS_INTRO, html)
                intros = (self.DOCS_INTRO_PAGES if concern["pages"]
                          else self.DOCS_INTRO_GAP)
                self.assertIn(intros[one_doc], shelf)
                self.assertNotIn(intros[not one_doc], html)
                if concern["pages"]:
                    continue
                seen_gap = True
                self.assertIn(self.GAP_QUALIFIER[one_doc], html)
                self.assertNotIn(self.GAP_QUALIFIER[not one_doc], html)
                self.assertIn(self.GAP_MATERIAL[one_doc], html)
                self.assertNotIn(self.GAP_MATERIAL[not one_doc], html)
        self.assertTrue(seen_gap, "the declared-gap page is covered")

    def test_concern_ledes_stand_on_a_single_concern_page(self):
        """Round-2 WARN 4: the ai-systems lede was v2 copy from a page listing
        every concern ("among the concerns on this page"). Each rendered lede
        equals its curated lede and contains none of the listed page-level
        phrases ("on this page", "this page", "among the ten", "concerns
        here"); the ai-systems lede's claim of other concerns on the decide
        hub holds on the rendered hub, which lists ai-systems and at least one
        other concern."""
        hub = self.draft_html["draft/decide/index.html"]
        hub_concerns = re.findall(r'<li><a href="/draft/decide/([^/"]+)/">',
                                  hub)
        subtype_slugs = {s for s, _, _ in
                         self.mod.DRAFT_NARRATIVE_SUBTYPES.values()}
        hub_concerns = [s for s in hub_concerns if s not in subtype_slugs]
        for concern in self.mod.DRAFT_CONCERNS:
            html = self.draft_html[f"draft/decide/{concern['slug']}/index.html"]
            lede = re.search(r'<p class="lead">(.*?)</p>', html, re.S)
            with self.subTest(concern=concern["slug"]):
                self.assertIsNotNone(lede)
                self.assertEqual(lede.group(1), self.mod._esc(concern["lede"]))
                for phrase in ("on this page", "this page", "among the ten",
                               "concerns here"):
                    self.assertNotIn(phrase, lede.group(1))
        ai = self.draft_html["draft/decide/ai-systems/index.html"]
        self.assertIn(
            '<p class="lead">AI is one leadership concern among the others on '
            "the decide hub: governed like the rest, which is precisely the "
            "point.", ai)
        self.assertIn("ai-systems", hub_concerns)
        self.assertGreater(len(set(hub_concerns) - {"ai-systems"}), 0,
                           "the decide hub carries other concerns")

    def test_each_subtype_index_links_up_to_the_hub(self):
        for slug in SUBTYPE_SLUGS:
            self.assertIn(
                'href="/draft/decide/"',
                self.draft_html[f"draft/decide/{slug}/index.html"],
                f"{slug}: the subtype index links up to the decide hub")

    # -- 14. the crosswalk (design C 3.7 Version A) --------------------------

    _XW_COL_RE = re.compile(r'<th scope="col" data-col="([a-z0-9-]+)"')
    _XW_COUNT_LINK_RE = re.compile(
        r'<a href="(/draft/crosswalk/([a-z0-9-]+)/#([a-z-]+))">'
        r"(\d+) documents?</a>"
    )

    def test_crosswalk_every_main_table_instrument_has_a_column_and_a_page(self):
        main = self.draft_html["draft/crosswalk/index.html"]
        expected = [i.key for i in self.mod.CROSSWALK_INSTRUMENTS
                    if i.main_table]
        self.assertEqual(
            self._XW_COL_RE.findall(main), expected,
            "the main table carries one column per main-table instrument, "
            "in the configured group order")
        for inst in self.mod.CROSSWALK_INSTRUMENTS:
            self.assertIn(
                f"draft/crosswalk/{inst.key}/index.html", self.draft_html,
                f"instrument '{inst.key}' has no generated page")

    def test_crosswalk_cell_count_links_resolve(self):
        main = self.draft_html["draft/crosswalk/index.html"]
        links = self._XW_COUNT_LINK_RE.findall(main)
        self.assertTrue(links, "the main table carries document count links")
        # Independent recount: rebuild the model and compare each link's count
        # with the matrix-derived document list it lands on.
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8")
        )
        xw = self.mod.build_crosswalk(full)
        linked = set()
        for href, key, domain, count in links:
            linked.add((key, domain))
            target = _page_rel_for(href)
            self.assertIn(target, self.draft_html,
                          f"count link targets a missing page: {href}")
            self.assertIn(f'id="{domain}"', self.draft_html[target],
                          f"count link anchor names no id: {href}")
            entry = xw["instruments"][key]["by_domain"].get(domain)
            self.assertIsNotNone(entry, f"count link with no matrix cell: {href}")
            self.assertEqual(int(count), len(entry["docs"]),
                             f"count disagrees with a recount: {href}")
        expected = {
            (i.key, domain)
            for i in self.mod.CROSSWALK_INSTRUMENTS if i.main_table
            for domain in xw["instruments"][i.key]["by_domain"]
        }
        self.assertEqual(
            linked, expected,
            "the main table carries exactly one resolving count link per "
            "non-empty domain-by-instrument cell (the AICPA TSC column is "
            "all N/A until the matrix populates it)")

    def test_crosswalk_presets_render_only_their_columns(self):
        for preset in self.mod.CROSSWALK_PRESETS:
            rel = f"draft/crosswalk/view/{preset.slug}/index.html"
            self.assertIn(rel, self.draft_html,
                          f"preset '{preset.slug}' has no generated view page")
            page = self.draft_html[rel]
            self.assertEqual(
                self._XW_COL_RE.findall(page), list(preset.columns),
                f"the '{preset.slug}' view renders exactly its own columns")
            # Round-2 item 9: a bare href check also matched the Next block's
            # link, so a removed All link passed; pin the list item itself.
            self.assertIn(
                '<li><a href="/draft/crosswalk/">All</a></li>', page,
                f"the '{preset.slug}' view keeps the All link in the views "
                "list")
        main = self.draft_html["draft/crosswalk/index.html"]
        self.assertIn(
            '<li><a href="/draft/crosswalk/" aria-current="page">All</a></li>',
            main, "the full crosswalk marks All as the current view")

    def test_crosswalk_caveat_block_present(self):
        pages = ["draft/crosswalk/index.html"]
        pages += [f"draft/crosswalk/view/{p.slug}/index.html"
                  for p in self.mod.CROSSWALK_PRESETS]
        pages += [f"draft/crosswalk/{i.key}/index.html"
                  for i in self.mod.CROSSWALK_INSTRUMENTS]
        # The matrices' own caveats (design C 3.6), carried nearly verbatim.
        fragments = (
            "citations are indicative, not exhaustive",
            "certification, attestation, or legal opinion",
            "no mapping has been made yet and does not assert that no "
            "criterion applies",
            "coverage is partial",
            "referenced for navigation only",
            "not an official mapping, certification claim, legal opinion",
        )
        for rel in pages:
            html = self.draft_html[rel]
            self.assertIn('<h2 id="caveats">What this mapping is</h2>', html,
                          rel)
            for fragment in fragments:
                self.assertIn(fragment, html,
                              f"{rel}: caveat block misses {fragment!r}")

    _XWI_LEAD_RE = re.compile(r'<p class="lead">.*?</p>', re.S)
    _XWI_RECORD_RE = re.compile(r'<dl class="record side">.*?</dl>', re.S)

    def test_crosswalk_instrument_pages_free_of_register_internal_text(self):
        """Round-2 item 1: the instrument lead piped the whole register Topic
        cell, so /draft/crosswalk/cobit/ showed the register's internal
        "Note: COBIT 2025 is not a published version..." remark and its lint
        tool reference. Pages show the descriptive name alone, and no
        register-internal text in a register-fed region: the lead and the
        Canonical citation record, the only regions built from register
        cells. Round 2b narrows the scan to those regions (never the whole
        page) because the reverse matrix's own threat-area rows legitimately
        carry such words: "LLM07:2026 Misinformation (including
        hallucination)" on the OWASP LLM Top 10 page quotes the library's
        reverse matrix row, not the register."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8")
        )
        xw = self.mod.build_crosswalk(full)
        for inst in self.mod.CROSSWALK_INSTRUMENTS:
            rel = f"draft/crosswalk/{inst.key}/index.html"
            html = self.draft_html[rel]
            lead = self._XWI_LEAD_RE.search(html)
            self.assertIsNotNone(lead, f"{rel}: no lead paragraph")
            record = self._XWI_RECORD_RE.search(html)
            data = xw["instruments"][inst.key]
            if data["register"] is not None:
                self.assertIsNotNone(
                    record, f"{rel}: no Canonical citation record")
            register_fed = lead.group(0) + (
                record.group(0) if record else "")
            for fragment in ("Note:", "lint-", "hallucination",
                             "is not a published version"):
                self.assertNotIn(
                    fragment, register_fed,
                    f"{rel}: register-internal text {fragment!r} in a "
                    "register-fed region")
        # Round 3 item 3: the expected leads are literal strings, never
        # recomputed with _xw_topic_name (a shared bug would pass itself).
        # Each pin drops a different register remainder: a semicolon tail,
        # a parenthetical currency remark, a parenthetical scope, an
        # abbreviation, and a parenthetical list plus a semicolon tail.
        pinned = {
            "iso-iec-27001":
                "Information security management systems: requirements",
            "nist-ai-rmf": "AI Risk Management Framework",
            "dora": "Digital Operational Resilience Act",
            "basc": "Business Alliance for Secure Commerce control and "
                    "security management system norm",
            "aicpa-tsc": "Trust Services Criteria for SOC 2 examinations",
        }
        for key, name in pinned.items():
            rel = f"draft/crosswalk/{key}/index.html"
            display = xw["instruments"][key]["display"]
            expected = self.mod._esc(
                f"Where the corpus maps to {display}: {name}.")
            self.assertIn(
                expected, self._XWI_LEAD_RE.search(self.draft_html[rel])
                .group(0),
                f"{rel}: the lead carries the descriptive name alone")
        cobit = self.draft_html["draft/crosswalk/cobit/index.html"]
        self.assertIn(
            "Control Objectives for Information and Related Technologies",
            cobit, "the COBIT page keeps the descriptive name")
        self.assertNotIn("COBIT 2025", cobit,
                         "the register note's unpublished version never "
                         "reaches the page")

    def test_browse_and_landing_link_the_crosswalk(self):
        """Round-2 item 2: no page outside /draft/crosswalk/ linked the
        crosswalk. The Browse page and the landing page link it (the top bar
        awaits a maintainer decision and stays unchanged)."""
        count = len([i for i in self.mod.CROSSWALK_INSTRUMENTS
                     if i.main_table])
        landing = self.draft_html["draft/index.html"]
        self.assertIn('href="/draft/crosswalk/"', landing,
                      "the landing page links the crosswalk")
        self.assertIn(f'<span class="n">{count} instruments</span>', landing,
                      "the landing tile's instrument count is computed")
        browse = self.draft_html["draft/browse/index.html"]
        self.assertIn('href="/draft/crosswalk/"', browse,
                      "the Browse page links the crosswalk")
        self.assertIn(
            f"against {count} standards, laws, frameworks, and programmes",
            browse, "the Browse sentence's instrument count is computed")

    _XW_RAIL_RE = re.compile(r'<div class="rail">(.*?)</div>', re.S)

    def test_crosswalk_preset_list_sits_in_the_rail(self):
        """Round-2 item 3 (maintainer direction, 15:09Z): the preset list is
        a vertical list in the page's existing right-hand rail, one side
        only; the table takes the main column. The links stay plain links to
        the preset views. Round 2b: the one-side rule holds for anchors, by
        role, because a preset view's required self-canonical (a head
        <link>, page hygiene test) names its own /draft/crosswalk/view/ URL
        and is no preset link."""
        pages = ["draft/crosswalk/index.html"]
        pages += [f"draft/crosswalk/view/{p.slug}/index.html"
                  for p in self.mod.CROSSWALK_PRESETS]
        for rel in pages:
            html = self.draft_html[rel]
            rail = self._XW_RAIL_RE.search(html)
            self.assertIsNotNone(rail, f"{rel}: no rail column")
            self.assertIn('href="/draft/crosswalk/"', rail.group(1),
                          f"{rel}: the All link sits in the rail")
            for preset in self.mod.CROSSWALK_PRESETS:
                self.assertIn(
                    f'href="/draft/crosswalk/view/{preset.slug}/"',
                    rail.group(1),
                    f"{rel}: the '{preset.slug}' link sits in the rail")
            outside = html.replace(rail.group(0), "")
            for anchor in _ANCHOR_RE.findall(outside):
                for href in _HREF_RE.findall(anchor):
                    self.assertFalse(
                        href.startswith("/draft/crosswalk/view/"),
                        f"{rel}: preset link {href} lives in the rail only "
                        "(one side)")
            self.assertNotIn("<table", rail.group(1),
                             f"{rel}: the table takes the main column")

    def test_trade_programme_pages_point_at_the_combined_reverse_section(self):
        """Round-2 item 5 (agy F2): the combined trade section's rows all
        carry CTPAT MSC domain area labels (none is BASC-labelled), so its
        table renders once, on the CTPAT page, and every programme the
        section names points there. The pointer sentence is checked against
        the parsed section, so it stays true of the source data."""
        mod = self.mod
        heading = "CTPAT MSC and BASC v6 (trade and supply-chain security)"
        sections = mod.parse_reverse_matrix(
            mod.CROSSWALK_REVERSE_MATRIX.read_text(encoding="utf-8"))
        self.assertIn(heading, sections)
        rows = sections[heading]["rows"]
        self.assertEqual(sections[heading]["area_label"], "CTPAT MSC domain")
        self.assertFalse([r for r in rows if r["area"].startswith("BASC")],
                         "no row is BASC-labelled, so no filter split")
        blob = heading + " " + " ".join(r["area"] for r in rows)
        pointers = {i.key: i for i in mod.CROSSWALK_INSTRUMENTS
                    if i.reverse_pointer}
        self.assertEqual(set(pointers), {"basc", "pip", "wco-safe", "aeo"})
        tokens = {"basc": "BASC", "pip": "PIP", "wco-safe": "WCO SAFE",
                  "aeo": "AEO"}
        ctpat = self.draft_html["draft/crosswalk/ctpat/index.html"]
        self.assertIn('id="control-areas"', ctpat)
        self.assertIn("Procedural and cargo security", ctpat)
        for key, inst in pointers.items():
            self.assertEqual(inst.reverse_pointer, "ctpat")
            self.assertIn(
                tokens[key], blob,
                f"the combined section names {tokens[key]}, which keeps the "
                "pointer sentence true")
            page = self.draft_html[f"draft/crosswalk/{key}/index.html"]
            self.assertIn('href="/draft/crosswalk/ctpat/#control-areas"',
                          page, f"{key}: no pointer link to the section")
            self.assertIn("names this programme in its combined section",
                          page, key)
            self.assertIn(mod._esc(heading), page, key)
            self.assertNotIn(
                'id="control-areas"', page,
                f"{key}: the combined table renders once, on the CTPAT page")

    def test_aicpa_tsc_taxonomy_spellings_all_aliased(self):
        """Round-2 item 7 (agy F4): no alias maps to aicpa-tsc because no
        taxonomy frameworks string names the AICPA TSC at all (verified: 0
        matches for AICPA, TSC, TSP, or Trust Services across the 758
        distinct strings), so none was added; an alias would be invented
        data. This canary fails the moment a TSC spelling appears in the
        taxonomy without an alias."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8")
        )
        pat = re.compile(r"\bAICPA\b|\bTSC\b|\bTSP\b|Trust Services")
        names = {f for d in full for f in d.get("frameworks", [])}
        unaliased = sorted(
            n for n in names
            if pat.search(n)
            and self.mod.CROSSWALK_ALIASES.get(n) != "aicpa-tsc")
        self.assertEqual(
            unaliased, [],
            "every AICPA TSC spelling in the taxonomy must alias to "
            "aicpa-tsc")

    # -- 6. asset copy ------------------------------------------------------

    def test_asset_copy_matches_the_pinned_tree(self):
        import tomllib
        pin = tomllib.loads(
            (REPO_ROOT / ".baseline" / "pin.toml").read_text(encoding="utf-8")
        )
        prefix = ".web/baseline/"
        # Baseline 1.6.0 section 4 items 2 and 3: the palette gate is pinned
        # beside the copies and never served.
        served = {key: digest for key, digest in pin["files"].items()
                  if key != self.mod.PALETTE_GATE_KEY}
        self.assertEqual(set(pin["files"]) - set(served),
                         {".baseline/check_palette.py"})
        for key, digest in served.items():
            self.assertTrue(key.startswith(prefix), key)
            rel = key[len(prefix):]
            out_rel = f"draft/assets/baseline/{rel}"
            self.assertIn(out_rel, self.draft_all, out_rel)
            data = self.draft_all[out_rel]
            self.assertIsInstance(data, bytes, out_rel)
            self.assertEqual(hashlib.sha256(data).hexdigest(), digest, out_rel)
            self.assertEqual(
                data, (REPO_ROOT / ".web" / "baseline" / rel).read_bytes(),
                f"{out_rel} must equal the vendored file byte for byte",
            )
        copied = {rel for rel in self.draft_all
                  if rel.startswith("draft/assets/baseline/")}
        self.assertEqual(len(copied), len(served),
                         "exactly the pinned files are copied")
        self.assertEqual(
            [rel for rel, _ in self.site_pages
             if rel.endswith("check_palette.py")], [],
            "the palette gate is never served")

    def test_pinned_scripts_are_the_release_script_set(self):
        """Baseline 1.6.0 SPECIFICATION.md section 8: "The 6 scripts are the
        whole set", and section 4 step 2 copies each of them, matrix.js and
        scheme.js included; the pin and the draft asset copy carry exactly
        that set."""
        import tomllib
        pin = tomllib.loads(
            (REPO_ROOT / ".baseline" / "pin.toml").read_text(encoding="utf-8")
        )
        prefix = ".web/baseline/"
        scripts = {key[len(prefix):] for key in pin["files"]
                   if key.startswith(prefix) and key.endswith(".js")}
        self.assertEqual(
            scripts,
            {"copy.js", "select.js", "search.js", "rail.js", "matrix.js",
             "scheme.js"},
            "the pin carries the release's whole script set")
        for name in sorted(scripts):
            self.assertIn(f"draft/assets/baseline/{name}", self.draft_all,
                          f"{name} is copied into the draft asset tree")

    def test_hidden_content_is_never_displayed(self):
        """Baseline 1.5.1 SPECIFICATION.md section 10 (every site moves to
        1.5.1): from 1.0.0 to 1.5.0 ``.doc section, .doc article { display:
        contents; }`` overrode the browser's own ``[hidden]`` rule, so the
        release adds 1 global rule that outranks any component's display
        rule. The stylesheet the draft serves carries it, so what search.js,
        select.js, matrix.js or copy.js hides stays off screen."""
        css = self.draft_all["draft/assets/baseline/baseline.css"].decode(
            "utf-8")
        self.assertEqual(
            re.findall(r"^\[hidden\] \{ display: none !important; \}$", css,
                       re.M),
            ["[hidden] { display: none !important; }"],
            "the served baseline.css carries the 1.5.1 global [hidden] rule")

    def test_served_template_notice_matches_the_pin(self):
        """Baseline 1.5.1 rewrote the template's NOTICE.md on grclibrary.ai's
        report: it said "Baseline 1.0.0" and "the 3 scripts" while the
        package had 5 scripts. The copy the draft serves under
        assets/baseline/ names no template version other than the pinned
        one and no script count other than the pinned script set's."""
        import tomllib
        pin = tomllib.loads(
            (REPO_ROOT / ".baseline" / "pin.toml").read_text(encoding="utf-8")
        )
        notice = self.draft_all["draft/assets/baseline/NOTICE.md"].decode(
            "utf-8")
        self.assertLessEqual(
            set(re.findall(r"\bbaseline (\d+\.\d+\.\d+)", notice, re.I)),
            {pin["version"]},
            "the served template notice names no other baseline version")
        scripts = sum(1 for key in pin["files"] if key.endswith(".js"))
        self.assertLessEqual(
            {int(n) for n in re.findall(r"\b(\d+) scripts\b", notice)},
            {scripts},
            "the served template notice counts no other number of scripts")

    # -- 25. baseline 1.6.0: switch, scheme.js, dark palette, palette gate --

    def test_pin_and_copies_are_baseline_1_6_0(self):
        """The 1.6.0 move (CHANGELOG 1.6.0): the pin names 1.6.0, and the
        files 1.6.0 adds or changes carry the release's digests in the pin,
        in the repository and, for the served ones, in the draft copy; the
        module docstring and the CSP comment name the pinned version."""
        import tomllib
        pin = tomllib.loads(
            (REPO_ROOT / ".baseline" / "pin.toml").read_text(encoding="utf-8")
        )
        self.assertEqual(pin["version"], "1.6.0")
        for key, digest in RELEASE_1_6_0_DIGESTS.items():
            self.assertEqual(pin["files"].get(key), digest, f"{key} pin")
            self.assertEqual(
                hashlib.sha256((REPO_ROOT / key).read_bytes()).hexdigest(),
                digest, f"{key} copy")
            if key.startswith(".web/baseline/"):
                out_rel = "draft/assets/baseline/" + key[len(".web/baseline/"):]
                self.assertEqual(
                    hashlib.sha256(self.draft_all[out_rel]).hexdigest(),
                    digest, out_rel)
        named = re.compile(r"baseline (\d+\.\d+\.\d+)")
        self.assertEqual(named.findall(" ".join(__doc__.split()[:20])),
                         [pin["version"]],
                         "the module docstring names the pinned version")
        source = Path(__file__).read_text(encoding="utf-8")
        csp_comment = re.search(r"^# The draft CSP, copied from (.*)$",
                                source, re.M)
        self.assertEqual(named.findall(csp_comment.group(1)),
                         [pin["version"]],
                         "the CSP comment names the pinned version")

    def test_scheme_switch_ends_the_top_bar_on_every_page(self):
        """Spec 7.33: on every page, the 404 page included, the switch is
        the last child of header.mast, right after nav.nav, and carries the
        hidden attribute in the markup (without script it is never shown)."""
        self.assertIn("draft/404.html", self.draft_html)
        for rel, html in self.draft_html.items():
            masts = re.findall(r'<header class="mast">(.*?)</header>', html,
                               re.S)
            self.assertEqual(len(masts), 1, f"{rel}: one top bar")
            self.assertTrue(
                masts[0].endswith("</nav>" + SCHEME_SWITCH),
                f"{rel}: the switch follows nav.nav as the last child of "
                "header.mast")
            self.assertEqual(masts[0].count('<nav class="nav"'), 1, rel)
            self.assertEqual(html.count("data-scheme-toggle"), 1,
                             f"{rel}: exactly one switch")
            self.assertRegex(
                html, r'<button class="scheme"[^>]*\shidden>',
                f"{rel}: the switch carries the hidden attribute")

    def test_scheme_script_in_head_before_the_stylesheets(self):
        """Spec sections 5 and 7.33: scheme.js loads in <head>, before the
        stylesheets, with data-cfasync="false" before src and no defer or
        async, so a stored scheme applies before the first paint."""
        for rel, html in self.draft_html.items():
            head = html[:html.index("</head>")]
            tags = re.findall(r"<script\b[^>]*/scheme\.js\"[^>]*>", html)
            self.assertEqual(len(tags), 1, f"{rel}: scheme.js loads once")
            self.assertNotRegex(tags[0], r"\b(?:defer|async)\b",
                                f"{rel}: no defer or async on scheme.js")
            self.assertLess(tags[0].index("data-cfasync"),
                            tags[0].index(" src="),
                            f"{rel}: data-cfasync comes before src")
            at = head.find(SCHEME_SCRIPT_TAG)
            self.assertGreater(at, 0, f"{rel}: the exact tag sits in <head>")
            sheet = head.find('<link rel="stylesheet"')
            self.assertGreater(sheet, at,
                               f"{rel}: scheme.js precedes every stylesheet")

    def test_served_dark_bg_is_the_released_value(self):
        """Spec 6.1: grclibrary's dark --bg in 1.6.0 is #110814 (1.5.1 had
        #1f1718); the served palettes.css carries it in both dark forms."""
        css = self.draft_all["draft/assets/baseline/palettes.css"].decode(
            "utf-8")
        self.assertEqual(_dark_token(css, "bg"),
                         [RELEASED_DARK_BG, RELEASED_DARK_BG])

    def test_draft_build_runs_the_palette_gate(self):
        """Spec section 4 item 3: the palette gate runs in the draft build,
        so a palettes.css that fails it fails the build (and --check, which
        renders the same tree)."""
        mod = self.mod
        root = Path(tempfile.mkdtemp(prefix="draft-palette-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        doctored = root / "palettes.css"
        doctored.write_text(_doctor_dark_token(
            mod.PALETTE_CSS.read_text(encoding="utf-8"), "text-muted",
            "#2a2a2a"), encoding="utf-8")
        draft_variant = next(v for v in mod.VARIANTS if v.draft_rules)
        original = mod.PALETTE_CSS
        try:
            mod.PALETTE_CSS = doctored
            with self.assertRaisesRegex(mod.BuildError, r"^palette gate: "):
                mod.render_variant(self.figures, draft_variant)
        finally:
            mod.PALETTE_CSS = original

    # -- 7. _headers --------------------------------------------------------

    def test_headers_block_exact(self):
        content = self.by_rel["_headers"][0]
        self.assertEqual(len(self.by_rel["_headers"]), 1)
        self.assertEqual(self.mod.DRAFT_CSP, SPEC_SECTION_9_CSP,
                         "the draft CSP is the spec section 9 string")
        block = (
            "/draft/*\n"
            "  ! Content-Security-Policy\n"
            f"  Content-Security-Policy: {SPEC_SECTION_9_CSP}\n"
            "  X-Robots-Tag: noindex\n"
        )
        self.assertEqual(self.mod.DRAFT_HEADERS_BLOCK, block)
        self.assertTrue(content.endswith(block))
        self.assertEqual(content.count("/draft/*"), 1)
        self.assertEqual(content.count(SPEC_SECTION_9_CSP), 1)
        self.assertEqual(content, self.mod.HEADERS_FILE + block,
                         "the live /* rule stays byte for byte above the block")
        for name in ("X-Content-Type-Options", "Referrer-Policy",
                     "Strict-Transport-Security"):
            self.assertNotIn(name, content,
                             f"{name} is zone-owned and never set here")

    # -- 8. type pages (design A, PR A2: the draft had no type landing, and
    # its type links circled between Browse and Search) -----------------------

    _TYPE_ROW_RE = re.compile(
        r'<li><a href="([^"]*)"[^>]*>(.*?)</a><span class="n">([^<]*)</span>'
        r'<small>(.*?)</small></li>', re.S)

    def _type_rel(self, type_name):
        return f"draft/types/{self.mod.type_slug(type_name)}/index.html"

    def test_every_taxonomy_type_has_exactly_one_draft_type_page(self):
        docs = self.mod.parse_taxonomy(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        types = {d["type"] for d in docs}
        self.assertTrue(types)
        expected = {self._type_rel(t) for t in types}
        self.assertEqual(len(expected), len(types),
                         "two taxonomy types share one type slug")
        rendered = [rel for rel in self.draft_all
                    if rel.startswith("draft/types/")]
        self.assertEqual(len(rendered), len(set(rendered)))
        self.assertEqual(set(rendered), expected,
                         "one draft type page per taxonomy type, no other")
        for type_name in types:
            page = self.draft_html[self._type_rel(type_name)]
            self.assertIn(
                f"<h1>{self.mod._esc(self.mod.draft_type_plural(type_name))}"
                "</h1>", page, type_name)
            self.assertIn(
                self.mod._esc(self.mod.TYPE_SCOPE[type_name]), page,
                f"{type_name}: the page carries its TYPE_SCOPE line")

    def test_every_document_appears_on_its_type_page(self):
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        by_type = {}
        for doc in full:
            by_type.setdefault(doc["type"], []).append(doc)
        for type_name, docs in by_type.items():
            with self.subTest(type=type_name):
                page = self.draft_html[self._type_rel(type_name)]
                scope = re.search(
                    r'<ul class="plan one described">(.*?)</ul>', page, re.S)
                self.assertIsNotNone(scope, "the type page has no list")
                found = self._TYPE_ROW_RE.findall(scope.group(1))
                self.assertEqual(len(found), len(docs),
                                 "one row per document of the type")
                rows = {href: (title, area, purpose)
                        for href, title, area, purpose in found}
                # The type's adopter documents are listed apart (integration
                # round 2), and the meta and the section label count both.
                n_adopter = sum(1 for g in self.mod.parse_adopter_docs()
                                if g["type"] == type_name)
                total = len(docs) + n_adopter
                noun = "document" if total == 1 else "documents"
                if n_adopter:
                    self.assertIn(
                        f'<p class="meta">{total} {noun}: {len(docs)} in the '
                        f"corpus and {n_adopter} adopter ", page)
                else:
                    self.assertIn(f'<p class="meta">{total} {noun}. ', page)
                self.assertIn(f"Documents, {total}</p>", page)
                for doc in docs:
                    area = self.mod._esc(
                        self.mod.draft_domain_label(doc["domain"]))
                    if doc["domain"] == self.mod.ROOT_DOMAIN:
                        href = self.mod.GITHUB_BLOB_BASE + doc["path"]
                    else:
                        href = self.mod._doc_page_url("/draft", doc["path"])
                    self.assertIn(href, rows, f"{doc['path']} has no row")
                    title, shown_area, purpose = rows[href]
                    self.assertTrue(
                        title.startswith(self.mod._esc(doc["title"])),
                        doc["path"])
                    self.assertEqual(shown_area, area, doc["path"])
                    self.assertEqual(
                        purpose,
                        self.mod._esc(self.mod.draft_doc_purpose(doc)),
                        f"{doc['path']}: the row carries the purpose")

    # Each part of a document page the type page prose can name, found on
    # the rendered page, with the taxonomy field that decides whether the
    # page has it (None: every document page has it).
    _DOC_PAGE_PARTS = {
        "record": (re.compile(r'<dl class="record side">\s*<dt>'), None),
        "outline": (re.compile(r"<h2>Outline</h2>"), "sections"),
        "frameworks": (re.compile(r"<h2>Frameworks it maps to</h2>"),
                       "frameworks"),
        "related documents": (re.compile(r"<h2>Related documents</h2>"),
                              "related_documents"),
    }
    _HOLDS_RE = re.compile(
        r"which holds the (.*?)(?: and, where the document has them, its "
        r"(.*?))?;")
    _NO_PURPOSE_LINE = (
        "a document that states no purpose gets a line naming its type and "
        "area")

    @staticmethod
    def _named_parts(clause):
        """'outline, frameworks, and related documents' -> the three names."""
        return [p for p in re.split(r",\s*(?:and\s+)?|\s+and\s+", clause or "")
                if p]

    def test_type_page_prose_is_true_for_every_row(self):
        """Round-1 NOTE: the type page said a document page holds every
        row's record and outline, but a root specification row opens its
        GitHub source and has no page. Round-2 WARN: it said every document
        page holds frameworks, but that section renders only for a document
        that has frameworks. The prose is read off each rendered type page
        and checked against every row and every row's rendered document
        page: a part named outside "where the document has them" is on every
        page, a part named inside it is on a page exactly when the document
        has it, and a row shows a generated purpose line only where the
        prose says so."""
        root_label = self.mod._esc(
            self.mod.draft_domain_label(self.mod.ROOT_DOMAIN))
        docs = {}
        for d in self._full_taxonomy():
            if d["domain"] == self.mod.ROOT_DOMAIN:
                docs[self.mod.GITHUB_BLOB_BASE + d["path"]] = d
            else:
                docs[self.mod._doc_page_url("/draft", d["path"])] = d
        for tp in self.figures["type_pages"]:
            with self.subTest(type=tp["type"]):
                page = self.draft_html[self._type_rel(tp["type"])]
                prose = re.search(
                    r"<h2>Every document of this type</h2>\s*<p>(.*?)</p>",
                    page, re.S)
                self.assertIsNotNone(prose)
                text = " ".join(prose.group(1).split())
                self.assertTrue(
                    text.startswith("Each with its area and its purpose"),
                    text)
                self.assertIn(
                    "A title in a corpus area opens the document's page, "
                    "which holds the ", text)
                self.assertIn(
                    "; a title in the "
                    f"{root_label} area is a library specification with no "
                    "page and opens its source on GitHub. The full text of "
                    "every document is read on GitHub.", text)
                holds = self._HOLDS_RE.search(text)
                self.assertIsNotNone(holds, text)
                always = self._named_parts(holds.group(1))
                where = self._named_parts(holds.group(2))
                self.assertEqual(
                    sorted(always + where), sorted(self._DOC_PAGE_PARTS),
                    "the prose names each part of a document page once")
                # The corpus list this prose introduces; the adopter list
                # after it carries its own sentence, checked by the adopter
                # type-page test (integration round 2).
                corpus_list = re.search(
                    r'<ul class="plan one described">(.*?)</ul>', page, re.S)
                rows = self._TYPE_ROW_RE.findall(corpus_list.group(1))
                self.assertTrue(rows)
                for href, _, area, purpose in rows:
                    doc = docs[unescape(href)]
                    if doc.get("purpose"):
                        self.assertEqual(
                            purpose, self.mod._esc(doc["purpose"]), href)
                    else:
                        self.assertIn(
                            self._NO_PURPOSE_LINE, text,
                            f"{href} states no purpose, and the prose "
                            "promises every row its purpose")
                        self.assertIn(
                            self.mod._esc(doc["type"].lower()), purpose, href)
                        self.assertIn(area, purpose, href)
                    if area == root_label:
                        self.assertTrue(
                            href.startswith(self.mod.GITHUB_BLOB_BASE), href)
                        continue
                    self.assertIn(_page_rel_for(href), self.draft_html,
                                  f"{href}: a corpus row opens its page")
                    doc_page = self.draft_html[_page_rel_for(href)]
                    self.assertIn(
                        'href="' + self.mod._esc(
                            self.mod.GITHUB_BLOB_BASE + doc["path"])
                        + '" target="_blank" rel="noopener noreferrer">'
                        "Read the full text on GitHub", doc_page, href)
                    for name in always:
                        found, _ = self._DOC_PAGE_PARTS[name]
                        self.assertRegex(
                            doc_page, found,
                            f"{href}: the prose says every document page "
                            f"holds the {name}")
                    for name in where:
                        found, field = self._DOC_PAGE_PARTS[name]
                        self.assertEqual(
                            bool(found.search(doc_page)),
                            field is None or bool(doc.get(field)),
                            f"{href}: the page holds the {name} exactly "
                            "where the document has it")

    def test_browse_by_type_links_the_type_pages(self):
        browse = self.draft_html["draft/browse/index.html"]
        # The scope sentence (site a9) sits between the heading and the
        # list; its content is pinned by the type-scope test.
        section = re.search(
            r'<h2 id="types">By type</h2>\s*<p>[^<]*</p>\s*<div class="wide">'
            r'<ul class="plan three">(.*?)</ul>', browse, re.S)
        self.assertIsNotNone(section, "Browse has no By type list")
        hrefs = _HREF_RE.findall(section.group(1))
        self.assertEqual(
            hrefs,
            ["/draft/types/" + self.mod.type_slug(t) + "/"
             for t, _ in self.figures["types"]],
            "every By type entry links its own type page, never the search "
            "page or a Browse anchor")

    # -- 17. the Browse adventure (design D sections 3 and 4.2 to 4.5) -------

    _NEED_SLUGS = ("decide", "govern", "comply", "solutions", "policies")

    # The Browse Scope sentence in the qualified form that is true for every
    # rendered document page (the unqualified form claimed an outline,
    # frameworks and related documents every page does not have).
    BROWSE_SCOPE_SENTENCE = (
        "A document page holds the record and, where the document has them, "
        "its outline, frameworks, and related documents; the full text is "
        "read on GitHub."
    )

    def test_browse_by_need_links_the_five_need_pages(self):
        """Design D section 3 (maintainer 14:39Z): the By need cards keep
        the approved copy but land on the five need pages; the mockup's
        placeholder targets (two Browse anchors, the search page and one
        example document) are retired."""
        browse = self.draft_html["draft/browse/index.html"]
        block = re.search(
            r'<h2 id="need">By need</h2>\s*<div class="wide">'
            r"<ol class=\"entries\">(.*?)</ol>", browse, re.S)
        self.assertIsNotNone(block, "Browse has no By need list")
        entries = re.findall(
            r'<li><a href="([^"]*)"><span class="t">([^<]*)</span>'
            r'<span class="n">([^<]*)</span>', block.group(1))
        self.assertEqual(
            entries,
            [(f"/draft/{tag}/", self.mod._esc(title), self.mod._esc(tag))
             for title, tag, _, _ in self.mod.DRAFT_NEEDS],
            "each By need card lands on its need page, approved copy intact")
        for href, _, _ in entries:
            self.assertIn(_page_rel_for(href), self.draft_html,
                          f"{href}: the need page is rendered")
        for retired in ('href="/draft/browse/#domains"',
                        'href="/draft/search/"',
                        "/draft/documents/governance/"):
            self.assertNotIn(retired, block.group(1),
                             "a mockup placeholder target survives")

    def test_browse_executive_path_block(self):
        """Design D section 3: Browse carries the executive path, the
        decide hub plus one chip per narrative kind, every count generated
        from the registry, and every concern a rendered topic page."""
        browse = self.draft_html["draft/browse/index.html"]
        self.assertIn(
            '<a href="/draft/decide/">Make a decision</a> is its hub: '
            f"{len(self.mod.DRAFT_CONCERNS)} leadership concerns, each a "
            f"topic page, and {len(self.figures['narratives'])} leadership "
            f"pages in {len(self.mod.DRAFT_NARRATIVE_SUBTYPES)} kinds",
            browse, "the executive path sentence carries generated counts")
        for concern in self.mod.DRAFT_CONCERNS:
            self.assertIn(f"draft/decide/{concern['slug']}/index.html",
                          self.draft_html,
                          "each a topic page holds for every concern")
        block = re.search(
            r'<h2 id="executive">.*?<ul class="plan three">(.*?)</ul>',
            browse, re.S)
        self.assertIsNotNone(block, "Browse has no executive path list")
        hrefs = _ROW_HREF_RE.findall(block.group(1))
        self.assertEqual(set(hrefs),
                         {f"/draft/decide/{s}/" for s in SUBTYPE_SLUGS},
                         "one chip per subtype index")
        for narrative_type, (slug, label, _) in (
                self.mod.DRAFT_NARRATIVE_SUBTYPES.items()):
            count = sum(1 for p in self.figures["narratives"]
                        if p["narrative_type"] == narrative_type)
            self.assertIn(
                f'<li><a href="/draft/decide/{slug}/">{label}</a>'
                f'<span class="n">{count}</span></li>', block.group(1),
                f"{slug}: the registry count")

    def test_browse_scope_sentence_true_of_every_document_page(self):
        """The page prose rule on the pre-existing Browse Scope sentence:
        the qualified form is on the page, the unqualified form is gone,
        and the claim is checked against every rendered document page: the
        record on every page, and the outline, frameworks and related
        documents exactly where the taxonomy carries them."""
        browse = self.draft_html["draft/browse/index.html"]
        self.assertIn(self.BROWSE_SCOPE_SENTENCE, browse)
        self.assertNotIn(
            "A document page holds the record, outline, frameworks, and "
            "related documents", browse,
            "the unqualified form claims sections only some pages have")
        for d in self._full_taxonomy():
            if d.get("domain") == self.mod.ROOT_DOMAIN:
                continue
            rel = "draft/" + self.mod._doc_route_rel(d["path"])
            page = self.draft_html[rel]
            with self.subTest(doc=d["path"]):
                for name, (found, field) in self._DOC_PAGE_PARTS.items():
                    if field is None:
                        self.assertRegex(
                            page, found,
                            f"{rel}: every document page holds the {name}")
                    else:
                        self.assertEqual(
                            bool(found.search(page)), bool(d.get(field)),
                            f"{rel}: the page holds the {name} exactly "
                            "where the document has it")

    def test_need_page_branches_resolve_and_are_never_bare_anchors(self):
        """On every need page, every link in the main column (the rail's
        on-page contents aside) lands on a rendered page, never on a bare
        anchor or another page's fragment; an external link keeps the
        draft's new-tab form (checked suite-wide by the hygiene test)."""
        for need in self._NEED_SLUGS:
            html = self.draft_html[f"draft/{need}/index.html"]
            main = html.split('<main id="main-content">', 1)[1] \
                       .split("</main>", 1)[0]
            main = _RAIL_RE.sub("", main)
            hrefs = _HREF_RE.findall(main)
            self.assertTrue(hrefs, need)
            for href in hrefs:
                with self.subTest(page=need, href=href):
                    self.assertFalse(
                        href.startswith("#"),
                        "a branch lands on a page, never a bare anchor")
                    if href.startswith(("https://", "http://")):
                        continue
                    self.assertNotIn(
                        "#", href,
                        "a branch lands on a page, not a fragment")
                    self.assertTrue(href.startswith("/draft/"), href)
                    self.assertIn(_page_rel_for(href), self.draft_html,
                                  f"unresolved branch {href}")

    def test_govern_artefact_links_open_their_draft_pages(self):
        """Design D gap G1, round 2 note 8: a govern-path artefact links its
        draft document page wherever one renders, a taxonomy document's or
        (since site a9) a docs/ adopter document's, and opens its GitHub
        source in the draft's external-link form only where neither carries
        it; every docs/ artefact now has an on-site page, and each artefact
        file exists in the repository."""
        html = self.draft_html["draft/govern/index.html"]
        by_path = {d["path"]: d for d in self._full_taxonomy()}
        by_path.update({g["path"]: g for g in self.mod.parse_adopter_docs()})
        for key, (path, label) in self.mod.DRAFT_GOVERN_ARTEFACTS.items():
            with self.subTest(artefact=path):
                self.assertTrue((REPO_ROOT / path).is_file(), path)
                doc = by_path.get(path)
                if path.startswith("docs/"):
                    self.assertIsNotNone(
                        doc, f"{key}: every docs/ artefact is an adopter "
                        "document with a draft page")
                if doc is not None and doc["domain"] != self.mod.ROOT_DOMAIN:
                    href = self.mod._doc_page_url("/draft", path)
                    self.assertIn(
                        f'<a href="{href}">{self.mod._esc(label)}</a>', html,
                        key)
                    self.assertIn(_page_rel_for(href), self.draft_html,
                                  f"{key}: the draft page renders")
                    self.assertNotIn(self.mod.GITHUB_BLOB_BASE + path, html,
                                     f"{key}: no GitHub fallback beside an "
                                     "on-site page")
                else:
                    self.assertIn(
                        f'<a href="{self.mod.GITHUB_BLOB_BASE + path}" '
                        'target="_blank" rel="noopener noreferrer">'
                        f"{self.mod._esc(label)}"
                        '<span class="vh"> (opens in a new tab)</span></a>',
                        html, key)
        self.assertIn('<a href="/draft/comply/">Meet an obligation</a>',
                      html, "situation four routes to the comply path")

    def test_govern_landing_list_equals_its_sources(self):
        """The govern landing rows are the configured domains, types and
        concern, each count recomputed from the figures and the concern
        join."""
        html = self.draft_html["draft/govern/index.html"]
        block = re.search(
            r'<h2 id="lands">.*?<ul class="plan described">(.*?)</ul>',
            html, re.S)
        self.assertIsNotNone(block, "govern has no landing list")
        self.assertEqual(
            _ROW_HREF_RE.findall(block.group(1)),
            [f"/draft/{d}/" for d in self.mod.DRAFT_GOVERN_LANDING_DOMAINS]
            + [f"/draft/types/{self.mod.type_slug(t)}/"
               for t in self.mod.DRAFT_GOVERN_LANDING_TYPES]
            + [f"/draft/decide/{self.mod.DRAFT_GOVERN_CONCERN}/"],
            "the landing rows, in table order")
        domain_counts = dict(self.figures["domains"])
        for domain in self.mod.DRAFT_GOVERN_LANDING_DOMAINS:
            self.assertIn(
                f'<li><a href="/draft/{domain}/">'
                f"{self.mod._esc(self.mod.draft_domain_label(domain))}</a>"
                f'<span class="n">{domain_counts[domain]}</span>',
                block.group(1), domain)
        type_counts = dict(self.figures["types"])
        for type_name in self.mod.DRAFT_GOVERN_LANDING_TYPES:
            self.assertIn(
                f'<a href="/draft/types/{self.mod.type_slug(type_name)}/">'
                f"{self.mod.draft_type_plural(type_name)}</a>"
                f'<span class="n">{type_counts[type_name]}</span>',
                block.group(1), type_name)
        concern, pages, docs = self._concern_joins()[
            self.mod.DRAFT_GOVERN_CONCERN]
        self.assertIn(
            f'<li><a href="/draft/decide/{concern["slug"]}/">'
            f'{self.mod._esc(concern["question"])}</a>'
            f'<span class="n">{self._concern_counts_text(pages, docs)}</span>',
            block.group(1), "the concern row carries the join's counts")

    def test_comply_instrument_rows_equal_the_crosswalk(self):
        """The comply instrument index is generated from the crosswalk
        model: one row per configured instrument, in table order, each
        landing on its instrument page with the recomputed count of
        documents the matrices map to it or whose framework alignment
        names it in an aliased form; the meta line's union count matches;
        and the not-listed
        branch lands on the matrix type page, the coverage-gaps register's
        document page and the regulatory-obligations outcome map."""
        html = self.draft_html["draft/comply/index.html"]
        block = re.search(
            r'<h2 id="instruments">.*?<ul class="plan described">(.*?)</ul>',
            html, re.S)
        self.assertIsNotNone(block, "comply has no instrument list")
        rows = re.findall(
            r'<li><a href="([^"]*)">([^<]*)</a><span class="n">([^<]*)'
            r"</span><small>([^<]*)</small></li>", block.group(1))
        self.assertEqual(
            [r[0] for r in rows],
            [f"/draft/crosswalk/{inst.key}/"
             for inst in self.mod.CROSSWALK_INSTRUMENTS],
            "one row per configured instrument, in table order")
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        xw = self.mod.build_crosswalk(full)
        union = set()
        for inst, (_, name, count_text, group) in zip(
                self.mod.CROSSWALK_INSTRUMENTS, rows):
            data = xw["instruments"][inst.key]
            paths = {path for entry in data["by_domain"].values()
                     for path, _ in entry["docs"]}
            paths |= {d["path"] for d in data["citations"]}
            union |= paths
            noun = "document" if len(paths) == 1 else "documents"
            with self.subTest(instrument=inst.key):
                self.assertEqual(name, self.mod._esc(data["display"]))
                self.assertEqual(count_text, f"{len(paths)} {noun}",
                                 "the count is the mapped-or-citing union")
                self.assertEqual(group, self.mod._esc(inst.group))
        self.assertIn(
            f"{len(rows)} instruments; {len(union)} library documents count "
            "toward at least one of them.", html,
            "the meta line's counts are recomputed")
        matrix = next(tp for tp in self.figures["type_pages"]
                      if tp["type"] == "Matrix")
        self.assertIn(
            f'<a href="/draft/types/matrix/">matrix documents</a>, '
            f'{matrix["count"]} in the corpus, on one page', html)
        self.assertIn(
            self.mod._doc_page_url(
                "/draft", self.mod.DRAFT_COMPLY_GAPS_REGISTER), html,
            "the coverage-gaps register's document page")
        outcome = next(p for p in self.figures["narratives"]
                       if p["path"] == self.mod.DRAFT_COMPLY_OUTCOME_MAP)
        self.assertIn(_reading_room_href(outcome), html,
                      "the regulatory-obligations outcome map")
        self.assertIn("they do not certify compliance", html,
                      "the carried no-certification caution")
        self.assertIn("never hidden", html, "the declared-gaps stance")

    def test_solutions_rows_follow_their_sources(self):
        """The solutions event rows follow the curated table (main link the
        leadership page or the resolving concern, counts from the registry
        and the concern join, Go deeper links the configured concern and
        domains); the scenario index equals the registry's Scenario pages;
        the builders rows are the configured domains with their counts."""
        html = self.draft_html["draft/solutions/index.html"]
        joins = self._concern_joins()
        by_path = {p["path"]: p for p in self.figures["narratives"]}
        block = re.search(
            r'<h2 id="events">.*?<ul class="plan one described">(.*?)</ul>',
            html, re.S)
        self.assertIsNotNone(block, "solutions has no event list")
        expected_hrefs = []
        for label, lede, page_path, concern_slug, domains in (
                self.mod.DRAFT_SOLUTION_EVENTS):
            if page_path is not None:
                expected_hrefs.append(_reading_room_href(by_path[page_path]))
            else:
                expected_hrefs.append(f"/draft/decide/{concern_slug}/")
        self.assertEqual(_ROW_HREF_RE.findall(block.group(1)),
                         expected_hrefs, "one row per event, in table order")
        for label, lede, page_path, concern_slug, domains in (
                self.mod.DRAFT_SOLUTION_EVENTS):
            concern, pages, docs = joins[concern_slug]
            with self.subTest(event=label):
                if page_path is not None:
                    page = by_path[page_path]
                    noun = ("governing document"
                            if len(page["sources"]) == 1
                            else "governing documents")
                    self.assertIn(
                        f'<span class="n">'
                        f'{self.mod._esc(page["narrative_type"].lower())}, '
                        f'{len(page["sources"])} {noun}</span>',
                        block.group(1),
                        "the row's count is the page's source count")
                    self.assertIn(f'<a href="/draft/decide/{concern_slug}/">',
                                  block.group(1),
                                  "Go deeper names the resolving concern")
                else:
                    self.assertIn(
                        f'<span class="n">'
                        f"{self._concern_counts_text(pages, docs)}</span>",
                        block.group(1),
                        "the row's counts are the concern join's")
                for domain in domains:
                    self.assertIn(f'<a href="/draft/{domain}/">',
                                  block.group(1),
                                  f"Go deeper names the {domain} domain")
        scenarios = sorted(
            (p for p in self.figures["narratives"]
             if p["narrative_type"] == "Scenario"),
            key=lambda p: (p["title"].lower(), p["path"]))
        self.assertTrue(scenarios)
        scen = re.search(
            r'<h2 id="rehearse">.*?<ul class="plan one described">(.*?)'
            r"</ul>", html, re.S)
        self.assertIsNotNone(scen, "solutions has no scenario index")
        self.assertEqual(
            _ROW_HREF_RE.findall(scen.group(1)),
            [_reading_room_href(p) for p in scenarios],
            "the scenario index equals the registry, in title order")
        self.assertIn(f"Scenarios, {len(scenarios)}</p>", html)
        builders = re.search(
            r'<h2 id="builders">.*?<ul class="plan described">(.*?)</ul>',
            html, re.S)
        self.assertIsNotNone(builders, "solutions has no builders list")
        domain_counts = dict(self.figures["domains"])
        self.assertEqual(
            _ROW_HREF_RE.findall(builders.group(1)),
            [f"/draft/{d}/"
             for d in self.mod.DRAFT_SOLUTION_BUILDER_DOMAINS])
        for domain in self.mod.DRAFT_SOLUTION_BUILDER_DOMAINS:
            self.assertIn(
                f'<li><a href="/draft/{domain}/">'
                f"{self.mod._esc(self.mod.draft_domain_label(domain))}</a>"
                f'<span class="n">{domain_counts[domain]}</span>',
                builders.group(1), domain)

    def test_policies_rows_equal_the_taxonomy(self):
        """The policies start rows are the policy and template type pages
        with the taxonomy's counts; the subject rows are exactly the
        domains with at least one policy or template, each count recounted
        from the type pages' own document lists, so the page's derived
        sentence stays true; the adapt block links the standard type page
        and the NOTICE file."""
        html = self.draft_html["draft/policies/index.html"]
        types = {tp["type"]: tp for tp in self.figures["type_pages"]}
        start = re.search(
            r'<h2 id="start">.*?<ul class="plan described">(.*?)</ul>',
            html, re.S)
        self.assertIsNotNone(start, "policies has no start list")
        self.assertEqual(_ROW_HREF_RE.findall(start.group(1)),
                         ["/draft/types/policy/", "/draft/types/template/"])
        for type_name in ("Policy", "Template"):
            tp = types[type_name]
            self.assertIn(
                f'<li><a href="/draft/types/{tp["slug"]}/">'
                f"{self.mod.draft_type_plural(type_name)}</a>"
                f'<span class="n">{tp["count"]}</span>', start.group(1),
                type_name)
        per_domain = {}
        for type_name in ("Policy", "Template"):
            for d in types[type_name]["docs"]:
                if d["domain"] != self.mod.ROOT_DOMAIN:
                    per_domain[d["domain"]] = \
                        per_domain.get(d["domain"], 0) + 1
        expected = sorted(per_domain.items(),
                          key=lambda kv: (-kv[1], kv[0]))
        subjects = re.search(
            r'<h2 id="subjects">.*?<ul class="plan described">(.*?)</ul>',
            html, re.S)
        self.assertIsNotNone(subjects, "policies has no subject list")
        self.assertEqual(_ROW_HREF_RE.findall(subjects.group(1)),
                         [f"/draft/{domain}/" for domain, _ in expected],
                         "exactly the domains with a policy or template")
        for domain, count in expected:
            self.assertGreater(count, 0, domain)
            self.assertIn(
                f'<li><a href="/draft/{domain}/">'
                f"{self.mod._esc(self.mod.draft_domain_label(domain))}</a>"
                f'<span class="n">{count}</span>', subjects.group(1), domain)
        self.assertIn(
            f"{types['Policy']['count']} policies and "
            f"{types['Template']['count']} templates in the corpus, across "
            f"{len(expected)} subjects.", html,
            "the meta counts are the type pages' corpus counts")
        self.assertIn('<a href="/draft/types/standard/">standards</a>', html)
        self.assertIn(
            self.mod.GITHUB_BLOB_BASE + "NOTICE.md", html,
            "the licence paragraph links the NOTICE file")

    # -- 23. Browse adventure round 2 (site a8 review round 1) --------------

    # The By need card lines as rendered, in card order: the Find a solution
    # and Write a policy lines are the maintainer's 2026-11-03 17:55Z copy,
    # the other three the approved mockup copy, unchanged.
    NEED_CARD_LINES = (
        "What the board should ask: decision briefs, oversight questions, "
        "and the evidence to expect back.",
        "Stand up a programme, run it, or assess its maturity, with "
        "charters, policies, and registers ready to adapt.",
        "Choose a framework, see the mappings and the gaps, and assemble the "
        "evidence an audit will ask for.",
        "Start from a problem or a lifecycle event and follow it to the "
        "leadership pages and documents that resolve it.",
        "Choose a policy or template, by type or by subject, and adapt it to "
        "your organization.",
    )

    @staticmethod
    def _series(items):
        items = list(items)
        if len(items) <= 2:
            return " and ".join(items)
        return ", ".join(items[:-1]) + ", and " + items[-1]

    def test_browse_need_card_lines_are_the_directed_copy(self):
        """Maintainer directive 2026-11-03 17:55Z: two By need card lines
        change exactly as directed and the other three stay as approved,
        checked on the rendered Browse cards."""
        browse = self.draft_html["draft/browse/index.html"]
        block = re.search(
            r'<h2 id="need">By need</h2>\s*<div class="wide">'
            r"<ol class=\"entries\">(.*?)</ol>", browse, re.S)
        self.assertIsNotNone(block, "Browse has no By need list")
        self.assertEqual(
            tuple(unescape(line) for line in re.findall(
                r'<span class="d">([^<]*)</span>', block.group(1))),
            self.NEED_CARD_LINES, "the card lines, in card order")

    def test_comply_crosswalk_sentence_matches_the_crosswalk_page(self):
        """Round 2 error 1: the comply instruments intro states how many of
        its rows the crosswalk table holds and names the instruments the
        crosswalk lists under Also in the corpus, checked against the
        rendered crosswalk page's columns and Also chips; the old claim
        that the crosswalk shows the same instruments is gone."""
        comply = self.draft_html["draft/comply/index.html"]
        xw = self.draft_html["draft/crosswalk/index.html"]
        table = re.search(r"<thead><tr>(.*?)</tr></thead>", xw, re.S)
        self.assertIsNotNone(table, "the crosswalk has no table head")
        columns = re.findall(r'<th scope="col" data-col="', table.group(1))
        also = re.search(r'<h2 id="also">Also in the corpus</h2>\s*<p>.*?'
                         r'</p>\s*<ul class="chips">(.*?)</ul>', xw, re.S)
        self.assertIsNotNone(also, "the crosswalk has no Also index")
        also_names = re.findall(r'<li><a href="[^"]*">([^<]*)</a></li>',
                                also.group(1))
        self.assertTrue(columns)
        self.assertTrue(also_names, "the committed model lists Also pages")
        block = re.search(
            r'<h2 id="instruments">.*?<ul class="plan described">(.*?)</ul>',
            comply, re.S)
        self.assertEqual(len(_ROW_HREF_RE.findall(block.group(1))),
                         len(columns) + len(also_names),
                         "comply lists every table column and Also page")
        self.assertIn(
            'The <a href="/draft/crosswalk/">crosswalk</a> shows '
            f"{len(columns)} of them as one table, domain by domain, and "
            f"lists {self._series(also_names)} under Also in the corpus.</p>",
            comply)
        self.assertNotIn("shows the same instruments", comply)

    def test_annex_sentences_are_true_of_the_annex_page(self):
        """Round 2 error 2 and warn 3: the govern and comply annex sentences
        give the whole annex page's count and claim only that it includes
        jurisdiction (govern) and jurisdiction and sector (comply) overlays,
        checked against the rendered annex type page: it lists the counted
        documents, among them at least one under a jurisdictions/ path and
        one under a compliance sector directory."""
        annex = next(tp for tp in self.figures["type_pages"]
                     if tp["type"] == "Annex")
        page = self.draft_html[f"draft/types/{annex['slug']}/index.html"]
        listed = [d for d in annex["docs"]
                  if d["domain"] != self.mod.ROOT_DOMAIN
                  and f'href="{self.mod._doc_page_url("/draft", d["path"])}"'
                  in page]
        self.assertEqual(len(listed), annex["count"],
                         "the annex page lists every counted annex")
        self.assertTrue(
            any("/jurisdictions/" in d["path"] for d in listed),
            "the annex page includes jurisdiction overlays")
        self.assertTrue(
            any(d["path"].startswith("compliance/")
                and d["path"].count("/") == 2 for d in listed),
            "the annex page includes sector overlays")
        link = f'<a href="/draft/types/{annex["slug"]}/">annex overlays</a>'
        govern = self.draft_html["draft/govern/index.html"]
        self.assertIn(
            "per entity layer on what applies from the "
            f"{link}, {annex['count']} in the corpus, including those for "
            "specific jurisdictions.</li>", govern)
        self.assertNotIn("jurisdiction-specific obligations", govern)
        # Integration round 2 NOTE: "those for your jurisdiction or sector"
        # assumed every reader has an annex; the sentence names the overlay
        # kinds the page includes instead.
        comply = self.draft_html["draft/comply/index.html"]
        self.assertIn(
            f"plus the {link}, {annex['count']} in the corpus, including "
            "jurisdiction and sector overlays, and keep", comply)
        self.assertNotIn("annex overlays</a> for your jurisdiction", comply)
        self.assertNotIn("for your jurisdiction or sector", comply)

    def test_govern_lands_sentence_is_true_of_the_rows(self):
        """Round 2 notes 5 and 6: the Lands intro counts its document types
        from the landing table, one clause per type, and calls the concern
        row the page that asks where the programme stands (the
        programme-maturity page scores nothing), checked against the
        rendered landing rows."""
        html = self.draft_html["draft/govern/index.html"]
        block = re.search(
            r'<h2 id="lands">.*?<ul class="plan described">(.*?)</ul>',
            html, re.S)
        self.assertIsNotNone(block, "govern has no landing list")
        type_rows = re.findall(
            r'<li><a href="/draft/types/[^"]*/">([^<]*)</a>', block.group(1))
        roles = self.mod.DRAFT_GOVERN_LANDING_TYPES
        self.assertEqual(
            type_rows,
            [self.mod.draft_type_plural(t) for t in roles],
            "one landing row per type the sentence counts")
        sentence = (
            f"The work rests on {len(type_rows)} document types: "
            + self._series(f"{plural.lower()} {role}"
                           for plural, role in zip(type_rows,
                                                   roles.values()))
            + ". The rows below are the areas and document types that run a "
            "programme, and the concern page that asks where the programme "
            "stands;")
        self.assertIn(sentence, html)
        concern = re.search(
            r'<li><a href="/draft/decide/'
            f'{self.mod.DRAFT_GOVERN_CONCERN}/">([^<]*)</a>', block.group(1))
        self.assertIsNotNone(concern, "the concern row")
        self.assertIn("programme stand", unescape(concern.group(1)),
                      "the concern row asks where the programme stands")
        self.assertNotIn("Three document types", html)
        self.assertNotIn("scores it", html)

    # -- 24. integration round 2 (batch 2 review at e9b50226f) --------------

    # What "names a crosswalk instrument" means to the concern-page check:
    # per configured instrument, its key names and common short forms.
    INSTRUMENT_NAME_RES = {
        "iso-iec-27001": r"\b27001\b",
        "iso-iec-42001": r"\b42001\b",
        "nist-csf": r"\bCSF\b|Cybersecurity Framework",
        "nist-sp-800-53": r"\b800-53(?![0-9A-Za-z])",
        "nist-ai-rmf": r"\bAI RMF\b|\bAI 100-1\b",
        "csa-ccm": r"\bCCM\b|Cloud Controls Matrix",
        "csa-aicm": r"\bAICM\b|AI Controls Matrix",
        "owasp-llm-top-10": r"\bLLM Top 10\b",
        "mitre-atlas": r"\bATLAS\b",
        "eu-ai-act": r"\bAI Act\b|\b2024/1689\b",
        "gdpr": r"\bGDPR\b|\b2016/679\b|General Data Protection Regulation",
        "dora": r"\bDORA\b|\b2022/2554\b|Digital Operational Resilience Act",
        "nis-2": r"\bNIS ?2\b|\b2022/2555\b",
        "ctpat": r"\bC-?TPAT\b",
        "pip": r"\bPIP\b|Partners in Protection",
        "basc": r"\bBASC\b",
        "wco-safe": r"\bWCO SAFE\b|\bSAFE Framework\b",
        "aeo": r"\bAEO\b|Authori[sz]ed Economic Operator",
        "aicpa-tsc": r"\bAICPA\b|\bTSC\b|Trust Services Criteria",
        "cobit": r"\bCOBIT\b",
        "pipeda": r"\bPIPEDA\b|Personal Information Protection and "
                  r"Electronic Documents Act",
        "quebec-law-25": r"\bLaw 25\b|\bBill 64\b",
    }
    # Plain-text names the matcher hits that name a different text than the
    # instrument: a namesake, or guidance, a profile, or a regulation made
    # under the instrument. Each stays unaliased, by design.
    NOT_INSTRUMENT_NAMES = {
        "Accelerate (DORA research)":
            "DORA here is DevOps Research and Assessment",
        "DORA accelerate metrics":
            "DORA here is DevOps Research and Assessment",
        "DORA RTS (EU) 2025/301":
            "a delegated regulation (RTS) made under DORA",
        "DORA RTS (EU) 2025/532":
            "a delegated regulation (RTS) made under DORA",
        "Commission Delegated Regulation (EU) 2025/301 of 23 October 2024 "
        "Article 5 (time limits for DORA major-incident reports)":
            "a delegated regulation (RTS) made under DORA",
        "NIS 2 Implementing Regulation (EU) 2024/2690":
            "an implementing regulation made under NIS 2",
        "EDPB Guidelines 07/2020 on the concepts of controller and processor "
        "in the GDPR, Version 2.1 (adopted 7 July 2021)":
            "EDPB guidance on the GDPR",
        "NIST AI RMF Generative AI Profile (NIST AI 600-1)":
            "NIST AI 600-1, a separate profile publication",
        "NIST IR 8374 Rev. 1 (Ransomware Risk Management: A Cybersecurity "
        "Framework 2.0 Community Profile, June 2026)":
            "NIST IR 8374, a separate community profile publication",
        "PIPEDA Breach of Security Safeguards Regulations (successor Bill "
        "C-36/PPCDA proposed, not in force)":
            "regulations made under PIPEDA",
        "BASC International Norm Implementation Guide V6-2022 (Version 06, "
        "effective 2022-03-02)":
            "the implementation guide to the BASC norm",
    }
    # Separate texts that name no crosswalk instrument but sit beside one in
    # a taxonomy string (integration round 3 WARN: each linked whole to the
    # instrument page); a linked span may not name any of them.
    SEPARATE_TEXT_RES = {
        "ISO/IEC 27002": r"\b27002\b",
        "Data Protection Act 2018": r"\bData Protection Act\b",
    }

    def test_no_plain_concern_framework_name_names_an_instrument(self):
        """Integration round 2 ERROR: the concern-page sentence says a name
        the crosswalk carries as an instrument links its page, but only
        exact alias spellings linked, so compliance-assurance showed NIST
        Cybersecurity Framework 2.0 as plain text beside a linked NIST CSF
        2.0. On every rendered concern page: no plain-text part of a
        framework chip names a crosswalk instrument unless it is listed in
        NOT_INSTRUMENT_NAMES with its reason, and every linked name names
        the instrument whose page it links. Integration round 3: a linked
        span may not include text naming another text, so each of its
        " / "-joined pieces names the linked instrument, and no piece names
        another configured instrument or a SEPARATE_TEXT_RES text.

        Matcher coverage limits: it matches the INSTRUMENT_NAME_RES key
        names and short forms only, case-sensitively, so a name citing an
        instrument by a form not listed there (an amending act's number
        alone, such as Regulation (EU) 2026/1744 for the EU AI Act; a
        translated or lower-case title; another short form) is not caught;
        it judges each chip's text, not what the name means, so the
        namesakes and derived texts it does hit are excluded by exact
        string in NOT_INSTRUMENT_NAMES, and a new spelling of one of those
        fails until it is listed or aliased; inside a linked span it finds
        another text only where a " / " separates it or where it matches
        an instrument matcher or SEPARATE_TEXT_RES, so a separate text
        joined some other way and named in no listed form is not caught;
        and it reads only the concern
        pages' framework chips, not document pages, the crosswalk or any
        other list of framework names."""
        self.assertEqual(set(self.INSTRUMENT_NAME_RES),
                         set(self.mod.CROSSWALK_BY_KEY),
                         "one matcher entry per configured instrument")
        aliased = (set(self.mod.CROSSWALK_ALIASES)
                   | set(self.mod.CROSSWALK_ALIAS_PARTS))
        self.assertFalse(set(self.NOT_INSTRUMENT_NAMES) & aliased,
                         "an excluded name is not aliased")
        matchers = {key: re.compile(pattern)
                    for key, pattern in self.INSTRUMENT_NAME_RES.items()}
        separate = {name: re.compile(pattern)
                    for name, pattern in self.SEPARATE_TEXT_RES.items()}
        plain_hits, wrong_links, chips_read = [], [], 0
        for slug in self._concern_joins():
            html = self.draft_html[f"draft/decide/{slug}/index.html"]
            block = re.search(
                r'<h2 id="frameworks">.*?<ul class="chips">(.*?)</ul>',
                html, re.S)
            if block is None:
                continue
            for item in re.findall(r"<li>(.*?)</li>", block.group(1)):
                chips_read += 1
                plain = " ".join(unescape(
                    re.sub(r"<a\s[^>]*>.*?</a>", " ", item)).split())
                named = sorted(key for key, m in matchers.items()
                               if m.search(plain))
                if named and plain not in self.NOT_INSTRUMENT_NAMES:
                    plain_hits.append(f"{slug}: {plain!r} names {named}")
                for key, text in re.findall(
                        r'<a href="/draft/crosswalk/([^"/]+)/">(.*?)</a>',
                        item):
                    self.assertIn(f"draft/crosswalk/{key}/index.html",
                                  self.draft_html, f"{slug}: {key}")
                    for piece in unescape(text).split(" / "):
                        others = sorted(
                            [k for k, m in matchers.items()
                             if k != key and m.search(piece)]
                            + [n for n, m in separate.items()
                               if m.search(piece)])
                        if not matchers[key].search(piece) or others:
                            wrong_links.append(
                                f"{slug}: {text!r} links {key}, but its part "
                                f"{piece!r} names {others or 'another text'}")
        self.assertGreater(chips_read, 0, "no concern framework chip read")
        self.assertEqual(plain_hits, [],
                         "a plain-text name names a crosswalk instrument")
        self.assertEqual(wrong_links, [],
                         "a linked name does not name its instrument")
        page = self.draft_html["draft/decide/compliance-assurance/index.html"]
        self.assertIn('<a href="/draft/crosswalk/nist-csf/">NIST Cybersecurity '
                      "Framework 2.0</a>", page)

    def test_type_pages_list_their_adopter_documents(self):
        """Integration round 2 WARN: the type page said every document of
        the type while the docs/ adopter documents of the type (Template,
        Guide, Register) were on no type page. Each type page lists every
        adopter document of its type after the corpus list, under the
        adopter area label with its generated count, and the block's
        sentence holds for every row and every row's rendered page: the
        count and scope it states, the record on every page, the outline
        and related documents exactly where the document has them, and no
        frameworks section (the sentence names none, as no adopter
        document maps one); the page's opening prose holds too (each row's
        area and purpose, the full text read on GitHub). A type with no
        adopter document has no block, and every adopter document is on
        exactly one type page."""
        adopter = self.mod.parse_adopter_docs()
        self.assertTrue(adopter)
        label = self.mod._esc(
            self.mod.draft_domain_label(self.mod.ADOPTER_DOCS_AREA))
        by_href = {self.mod._doc_page_url("/draft", g["path"]): g
                   for g in adopter}
        block_re = re.compile(
            rf'<p class="lbl blk">{re.escape(label)}, (\d+)</p>\n<p>(.*?)</p>'
            r'\n<div class="wide"><ul class="plan one described">\n(.*?)\n'
            r"</ul></div>", re.S)
        listed = []
        for tp in self.figures["type_pages"]:
            with self.subTest(type=tp["type"]):
                page = self.draft_html[self._type_rel(tp["type"])]
                mine = [g for g in adopter if g["type"] == tp["type"]]
                block = block_re.search(page)
                if not mine:
                    self.assertIsNone(block, "no adopter block without one")
                    continue
                self.assertIsNotNone(block, "the type page lists its adopter "
                                     "documents")
                n = len(mine)
                self.assertEqual(int(block.group(1)), n)
                noun = "document" if n == 1 else "documents"
                each = "Its title opens" if n == 1 else "Each title opens"
                self.assertEqual(
                    block.group(2),
                    f"The {n} adopter {noun} of this type, under docs/ and "
                    "outside the corpus taxonomy; "
                    f"{'its entry is' if n == 1 else 'each entry is'} read "
                    "from the leading metadata block of its file at build "
                    f"time. {each} the document's page, which holds the "
                    "record and, where the document has them, its outline "
                    "and related documents.")
                self.assertLess(page.index("Every document of this type"),
                                block.start(), "the block sits under the "
                                "heading that says every document")
                rows = self._TYPE_ROW_RE.findall(block.group(3))
                self.assertEqual(
                    sorted(unescape(href) for href, _, _, _ in rows),
                    sorted(self.mod._doc_page_url("/draft", g["path"])
                           for g in mine))
                for href, title, area, purpose in rows:
                    g = by_href[unescape(href)]
                    listed.append(g["path"])
                    self.assertEqual(title, self.mod._esc(g["title"]))
                    self.assertEqual(area, label, href)
                    self.assertEqual(
                        purpose, self.mod._esc(self.mod.draft_doc_purpose(g)),
                        f"{href}: the row carries its purpose")
                    doc_page = self.draft_html[_page_rel_for(unescape(href))]
                    record, _ = self._DOC_PAGE_PARTS["record"]
                    self.assertRegex(doc_page, record, href)
                    for name, field in (("outline", "sections"),
                                        ("related documents",
                                         "related_documents")):
                        found, _ = self._DOC_PAGE_PARTS[name]
                        self.assertEqual(bool(found.search(doc_page)),
                                         bool(g.get(field)), f"{href}: {name}")
                    found, _ = self._DOC_PAGE_PARTS["frameworks"]
                    self.assertIsNone(found.search(doc_page), href)
                    self.assertIn(
                        'href="' + self.mod._esc(
                            self.mod.GITHUB_BLOB_BASE + g["path"])
                        + '" target="_blank" rel="noopener noreferrer">'
                        "Read the full text on GitHub", doc_page, href)
        self.assertEqual(sorted(listed), sorted(g["path"] for g in adopter),
                         "every adopter document is on exactly one type page")

    def test_policies_start_sentence_is_true_of_the_type_pages(self):
        """Integration round 2 WARN: policies said each row opens a type page
        listing every document of the type, which left out the adopter
        documents. Checked against each start row's rendered type page: it
        links every corpus document and every adopter document of the type,
        the row's count is the page's corpus list, and the adopter
        documents come after the corpus list on a page that has any."""
        html = self.draft_html["draft/policies/index.html"]
        self.assertIn(
            "<p>Each row opens a type page listing every document of the "
            "type, with its area and purpose: the corpus documents, then the "
            "adopter documents of the type under docs/, where it has any. The "
            "count beside a row is the type's corpus documents, generated "
            "from the taxonomy at build time.</p>", html)
        start = re.search(
            r'<h2 id="start">.*?<ul class="plan described">(.*?)</ul>',
            html, re.S)
        rows = re.findall(r'<li><a href="([^"]*)">[^<]*</a>'
                          r'<span class="n">(\d+)</span>', start.group(1))
        self.assertTrue(rows)
        slugs = {tp["slug"]: tp["type"] for tp in self.figures["type_pages"]}
        full = self._full_taxonomy()
        adopter = self.mod.parse_adopter_docs()
        for href, n in rows:
            type_name = slugs[href.split("/")[3]]
            with self.subTest(type=type_name):
                page = self.draft_html[_page_rel_for(href)]
                main = page.split('<main id="main-content">', 1)[1]
                linked = [unescape(h) for h in _HREF_RE.findall(main)]
                corpus = [d for d in full if d["type"] == type_name]
                for d in corpus:
                    self.assertIn(
                        self.mod.GITHUB_BLOB_BASE + d["path"]
                        if d["domain"] == self.mod.ROOT_DOMAIN
                        else self.mod._doc_page_url("/draft", d["path"]),
                        linked, d["path"])
                corpus_list = re.search(
                    r'<ul class="plan one described">(.*?)</ul>', main, re.S)
                self.assertEqual(
                    int(n), len(self._TYPE_ROW_RE.findall(
                        corpus_list.group(1))),
                    "the row counts the type's corpus documents")
                self.assertEqual(int(n), len(corpus))
                for g in adopter:
                    if g["type"] != type_name:
                        continue
                    href_g = self.mod._doc_page_url("/draft", g["path"])
                    self.assertIn(href_g, linked, g["path"])
                    self.assertGreater(main.index(f'href="{href_g}"'),
                                       corpus_list.end(),
                                       "adopter documents follow the corpus")

    # -- 26. integration round 3 (review of integration round 2) ------------

    # A type page link on a need page or Browse, the prose up to the next
    # tag after it, and the row count beside it where it is a list row.
    _TYPE_LINK_RE = re.compile(
        r'<a href="/draft/types/([^"/]+)/">[^<]*</a>([^<]*)'
        r'(?:<span class="n">(\d+)</span>)?')
    # Per page with type rows: the sentence stating that each row count is
    # the type's corpus documents.
    TYPE_ROW_SCOPES = {
        "browse": "corpus documents, the ",
        "govern": "the count beside an area or a type is its corpus "
                  "documents",
        "policies": "The count beside a row is the type's corpus documents",
    }

    def test_type_page_counts_state_their_scope(self):
        """Integration round 3 WARN: comply said "the registers that carry
        the evidence, 39 documents" while the Register type page lists 40
        (39 in the corpus and 1 adopter document). On comply, govern,
        solutions, policies and Browse, every count beside a type page link
        is checked against that rendered type page: a prose count reading
        "N documents" is the page's total, one reading "N in the corpus" is
        its corpus list, and a list row's count is its corpus list on a
        page whose sentence says so. At least one linked type page lists
        adopter documents, so the two scopes differ somewhere checked."""
        checked, differ = 0, False
        for name in ("comply", "govern", "solutions", "policies", "browse"):
            html = self.draft_html[f"draft/{name}/index.html"]
            main = html.split('<main id="main-content">', 1)[1]
            main = main.split("</main>", 1)[0]
            for slug, prose, row in self._TYPE_LINK_RE.findall(main):
                page = self.draft_html[f"draft/types/{slug}/index.html"]
                total = int(re.search(r'<p class="meta">(\d+) documents?\b',
                                      page).group(1))
                corpus_list = re.search(
                    r'<ul class="plan one described">(.*?)</ul>', page, re.S)
                corpus = len(self._TYPE_ROW_RE.findall(corpus_list.group(1)))
                differ = differ or total != corpus
                with self.subTest(page=name, type=slug):
                    if row:
                        checked += 1
                        self.assertEqual(int(row), corpus,
                                         "a row counts the corpus list")
                        self.assertIn(self.TYPE_ROW_SCOPES.get(name, "\0"),
                                      main, "the page says rows count the "
                                      "corpus documents")
                        continue
                    found = re.match(
                        r"[^0-9]*?(\d+) (in the corpus|documents?)\b", prose)
                    if found is None:
                        continue
                    checked += 1
                    n, scope = int(found.group(1)), found.group(2)
                    if scope == "in the corpus":
                        self.assertEqual(n, corpus, "the corpus list")
                    else:
                        self.assertEqual(n, total, "the type page's total")
        self.assertGreater(checked, 0, "no type page count read")
        self.assertTrue(differ, "no linked type page lists adopter documents")
        register = next(tp for tp in self.figures["type_pages"]
                        if tp["type"] == "Register")
        self.assertIn(
            f'<a href="/draft/types/{register["slug"]}/">registers</a> that '
            f"carry the evidence, {register['count']} in the corpus.</p>",
            self.draft_html["draft/comply/index.html"])

    def _citation_hrefs(self, key):
        page = self.draft_html[f"draft/crosswalk/{key}/index.html"]
        self.assertIn('<h2 id="citations">', page, key)
        block = re.search(
            r'<h2 id="citations">[^<]*</h2>\n<p>[^<]*</p>\n'
            r'<div class="wide"><ul class="plan one">\n(.*?)\n</ul>',
            page, re.S)
        return set(_ROW_HREF_RE.findall(block.group(1))) if block else set()

    def test_compound_parts_count_toward_their_instruments(self):
        """Integration round 3 WARN: the compound split raises crosswalk
        citations and comply counts, but exact-alias counting failed no
        test. Each instrument's rendered citation list is exactly the
        non-root documents naming it through an exact alias or a compound
        part, recomputed here from the taxonomy, and its comply count is
        that list plus its matrix mappings; the documents reached only
        through a compound part are on their pages, among them the CSA CCM
        v4.1 / AICM v1.1 document on the csa-aicm page, for each
        instrument the split serves."""
        full = [d for d in self._full_taxonomy()
                if d["domain"] != self.mod.ROOT_DOMAIN]
        aliases = self.mod.CROSSWALK_ALIASES
        parts = self.mod.CROSSWALK_ALIAS_PARTS
        cited = {key: set() for key in self.mod.CROSSWALK_BY_KEY}
        only_part = {key: set() for key in self.mod.CROSSWALK_BY_KEY}
        for d in full:
            href = self.mod._doc_page_url("/draft", d["path"])
            names = d.get("frameworks", [])
            exact = {aliases[n] for n in names if n in aliases}
            for key in exact:
                cited[key].add(href)
            for n in names:
                for _, key in parts.get(n, ()):
                    if key is None:
                        continue
                    cited[key].add(href)
                    if key not in exact:
                        only_part[key].add(href)
        comply = self.draft_html["draft/comply/index.html"]
        xw = self.mod.build_crosswalk(self._full_taxonomy())
        for key in self.mod.CROSSWALK_BY_KEY:
            with self.subTest(instrument=key):
                self.assertEqual(self._citation_hrefs(key), cited[key],
                                 "the citations are the aliased documents")
                mapped = {self.mod._doc_page_url("/draft", path)
                          for entry in xw["instruments"][key]["by_domain"]
                          .values() for path, _ in entry["docs"]}
                n = len(mapped | cited[key])
                self.assertIn(
                    f'<li><a href="/draft/crosswalk/{key}/">'
                    f'{self.mod._esc(xw["instruments"][key]["display"])}</a>'
                    f'<span class="n">{n} '
                    f'{"document" if n == 1 else "documents"}</span>', comply,
                    "the comply count includes the compound-only documents")
        self.assertLessEqual(
            {"csa-aicm", "ctpat", "pip", "basc", "pipeda", "quebec-law-25"},
            {key for key, hrefs in only_part.items() if hrefs},
            "the instruments the split serves each gain a document")
        aicm = [d for d in full
                if "CSA CCM v4.1 / AICM v1.1" in d.get("frameworks", [])
                and not any(aliases.get(n) == "csa-aicm"
                            for n in d["frameworks"])]
        self.assertTrue(aicm, "a document names AICM only in the compound")
        for d in aicm:
            self.assertIn(self.mod._doc_page_url("/draft", d["path"]),
                          self._citation_hrefs("csa-aicm"), d["path"])

    def test_compound_parts_naming_other_texts_render_plain(self):
        """Integration round 3 WARN: "UK GDPR / Data Protection Act 2018"
        linked whole to the GDPR page and "ISO/IEC 27001:2022 / ISO/IEC
        27002:2022" whole to the 27001 page. On the rendered concern pages
        the instrument part links and the other part is plain text; neither
        string sits in the exact alias map, and the plain parts count toward
        no instrument."""
        parts = self.mod.CROSSWALK_ALIAS_PARTS
        expected = {
            "UK GDPR / Data Protection Act 2018":
                '<li><a href="/draft/crosswalk/gdpr/">UK GDPR</a> / '
                "Data Protection Act 2018</li>",
            "ISO/IEC 27001:2022 / ISO/IEC 27002:2022":
                '<li><a href="/draft/crosswalk/iso-iec-27001/">ISO/IEC '
                "27001:2022</a> / ISO/IEC 27002:2022</li>",
        }
        for name, chip in expected.items():
            with self.subTest(name=name):
                self.assertNotIn(name, self.mod.CROSSWALK_ALIASES)
                self.assertIn(None, [key for _, key in parts[name]])
                pages = [slug for slug in self._concern_joins()
                         if chip in self.draft_html[
                             f"draft/decide/{slug}/index.html"]]
                self.assertTrue(pages, "a concern page shows the chip")
                self.assertEqual(
                    self.mod.crosswalk_alias_keys(name),
                    tuple(key for _, key in parts[name] if key is not None))

    def test_comply_count_sentence_states_the_alias_scope(self):
        """Integration round 3 WARN: comply said each count is the
        documents the matrices map to the instrument or whose framework
        alignment names it, while taxonomy strings naming an instrument in
        an unaliased form count toward none. The rendered sentence scopes
        the count to forms the alias map recognizes, as the instrument
        pages' citation sentence does, and the meta line claims only the
        counted union; an unaliased string naming an instrument exists, so
        the qualifier is needed."""
        comply = self.draft_html["draft/comply/index.html"]
        self.assertIn(
            "A row opens the instrument's crosswalk page; the count beside it "
            "is the library documents the matrices map to it or whose "
            "framework alignment names it in a form the site's alias map "
            "recognizes, so a document naming it only in another form is not "
            "counted.", comply)
        self.assertNotIn("framework alignment names it. The", comply)
        self.assertNotIn("map to or cite at least one of them", comply)
        names = {n for d in self._full_taxonomy()
                 for n in d.get("frameworks", [])}
        cobit = re.compile(self.INSTRUMENT_NAME_RES["cobit"])
        unaliased = sorted(n for n in names if cobit.search(n)
                           and not self.mod.crosswalk_alias_keys(n))
        self.assertIn("COBIT 2019 DSS05", unaliased)
        page = self.draft_html["draft/crosswalk/cobit/index.html"]
        self.assertIn("through the committed alias map.</p>", page)

    def test_alias_comment_scopes_the_clause_rule_to_concern_pages(self):
        """Integration round 3 NOTE: the comment above CROSSWALK_ALIASES
        said every spelling citing an instrument by a clause is aliased;
        that holds for the concern pages' names only, and the comment
        says so."""
        source = (REPO_ROOT / ".web" / "build.py").read_text(encoding="utf-8")
        comment = source[:source.index("\nCROSSWALK_ALIASES = {")]
        comment = " ".join(
            line.lstrip("# ") for line in
            comment[comment.rindex("\n\n"):].splitlines())
        self.assertIn("A spelling on a concern page that cites an instrument",
                      comment)
        self.assertIn("an unaliased spelling counts toward no instrument",
                      comment)
        self.assertNotIn("A spelling that cites an instrument", comment)


class DraftAdventureGuardTests(unittest.TestCase):
    """23: each fail-loud guard of the Browse adventure's need pages raises
    on a curated table patched with a bogus value (round 2 warn 4)."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()
        cls.figures = cls.mod.compute_figures()
        full = cls.mod.parse_taxonomy_full(
            cls.mod.TAXONOMY.read_text(encoding="utf-8"))
        cls.docs_by_path = {d["path"]: d for d in full}
        cls.pages_by_path = {
            **cls.docs_by_path,
            **{g["path"]: g for g in cls.mod.parse_adopter_docs()},
        }
        cls.concerns = cls.mod.draft_concern_join(
            cls.figures, cls.docs_by_path)
        cls.xw = cls.mod.build_crosswalk(full)

    def _raises(self, name, value, pattern, call):
        mod = self.mod
        original = getattr(mod, name)
        try:
            setattr(mod, name, value)
            with self.assertRaisesRegex(mod.BuildError, pattern):
                call()
        finally:
            setattr(mod, name, original)

    def _govern(self):
        return self.mod.draft_govern_values(
            self.figures, self.pages_by_path, self.concerns)

    def _comply(self):
        return self.mod.draft_comply_values(
            self.figures, self.docs_by_path, self.xw)

    def test_the_committed_tables_render(self):
        self._govern()
        self._comply()
        self.mod.draft_solutions_values(self.figures, self.concerns)

    def test_an_artefact_not_in_the_repository_fails(self):
        path = "docs/portal-not-in-the-repository.md"
        self._raises(
            "DRAFT_GOVERN_ARTEFACTS",
            {**self.mod.DRAFT_GOVERN_ARTEFACTS,
             "GOV_ART_PORTAL": (path, "adopter portal")},
            re.escape(f"adventure artefact {path} is not in the repository"),
            self._govern)

    def test_a_solutions_event_naming_an_unknown_narrative_fails(self):
        path = "executive/journeys/journey-not-in-the-registry.md"
        events = list(self.mod.DRAFT_SOLUTION_EVENTS)
        label, lede, _, concern, domains = events[0]
        events[0] = (label, lede, path, concern, domains)
        self._raises(
            "DRAFT_SOLUTION_EVENTS", tuple(events),
            re.escape(f"names {path} which the narrative registry does not "
                      "carry"),
            lambda: self.mod.draft_solutions_values(
                self.figures, self.concerns))

    def test_a_govern_landing_type_the_taxonomy_lacks_fails(self):
        self._raises(
            "DRAFT_GOVERN_LANDING_TYPES",
            {**self.mod.DRAFT_GOVERN_LANDING_TYPES, "Almanac": "stage it"},
            "names document type 'Almanac' which the taxonomy does not carry",
            self._govern)

    def test_a_govern_concern_outside_the_concerns_fails(self):
        self._raises(
            "DRAFT_GOVERN_CONCERN", "not-a-concern",
            "names concern 'not-a-concern' which DRAFT_CONCERNS does not "
            "carry",
            self._govern)

    def test_a_comply_gaps_register_not_in_the_taxonomy_fails(self):
        path = "governance/register-not-in-the-taxonomy.md"
        self._raises(
            "DRAFT_COMPLY_GAPS_REGISTER", path,
            re.escape(f"comply names {path} which is not in the taxonomy"),
            self._comply)

    def test_a_comply_outcome_map_not_in_the_registry_fails(self):
        path = "executive/outcome-maps/outcome-map-not-in-the-registry.md"
        self._raises(
            "DRAFT_COMPLY_OUTCOME_MAP", path,
            re.escape(f"comply names {path} which the narrative registry "
                      "does not carry"),
            self._comply)


class DraftIntegrationRound2GuardTests(unittest.TestCase):
    """24 and 26: a compound crosswalk alias whose parts do not rejoin to its
    string, that also sits in CROSSWALK_ALIASES, whose part names no
    configured instrument, or none of whose parts names an instrument (26),
    and an adopter document whose type has no type
    page, each fail the build; and the generator's content-boundary
    docstring names each extra read the draft makes and calls the adopter
    pages adopter document pages."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()
        cls.full = cls.mod.parse_taxonomy_full(
            cls.mod.TAXONOMY.read_text(encoding="utf-8"))

    def _crosswalk_with_parts(self, parts):
        original = self.mod.CROSSWALK_ALIAS_PARTS
        try:
            self.mod.CROSSWALK_ALIAS_PARTS = parts
            self.mod.build_crosswalk(self.full)
        finally:
            self.mod.CROSSWALK_ALIAS_PARTS = original

    def test_the_committed_parts_build(self):
        self.assertTrue(self.mod.CROSSWALK_ALIAS_PARTS)
        self._crosswalk_with_parts(self.mod.CROSSWALK_ALIAS_PARTS)

    def test_parts_that_do_not_rejoin_fail(self):
        with self.assertRaisesRegex(self.mod.BuildError, "do not rejoin"):
            self._crosswalk_with_parts(
                {"PIPEDA / Quebec Law 25": (("PIPEDA", "pipeda"),
                                            ("Law 25", "quebec-law-25"))})

    def test_a_compound_also_in_the_alias_map_fails(self):
        with self.assertRaisesRegex(self.mod.BuildError, "in both"):
            self._crosswalk_with_parts(
                {"GDPR / UK GDPR": (("GDPR", "gdpr"), ("UK GDPR", "gdpr"))})

    def test_a_part_naming_no_instrument_fails(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "naming no configured instrument"):
            self._crosswalk_with_parts(
                {"PIPEDA / Quebec Law 25": (("PIPEDA", "pipeda"),
                                            ("Quebec Law 25", "law-25"))})

    def test_a_compound_with_no_instrument_part_fails(self):
        """Integration round 3: a part may be plain text (key None), but a
        compound none of whose parts names an instrument links nothing and
        belongs in neither map."""
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "names a crosswalk instrument"):
            self._crosswalk_with_parts(
                {"PIPEDA / Quebec Law 25": (("PIPEDA", None),
                                            ("Quebec Law 25", None))})

    def test_an_adopter_type_with_no_type_page_fails(self):
        figures = self.mod.compute_figures()
        adopter_types = {g["type"] for g in self.mod.parse_adopter_docs()}
        self.assertTrue(adopter_types)
        dropped = sorted(adopter_types)[0]
        patched = dict(figures, type_pages=[
            tp for tp in figures["type_pages"] if tp["type"] != dropped])
        draft = next(v for v in self.mod.VARIANTS if v.draft_rules)
        with self.assertRaisesRegex(self.mod.BuildError,
                                    f"type '{dropped}', which has no type "
                                    "page"):
            self.mod.render_draft_variant(patched, draft)

    def test_content_boundary_names_each_extra_read_of_the_draft(self):
        """Integration round 2 NOTE: the boundary said adopter-guide pages
        while the docs/ area holds templates, guides and a register. Like
        the version-rule docstring test, this holds the docstring to the
        code: each file or tree the draft reads beyond the live trees'
        allow-list (its template tree, the baseline runtime files and pin,
        the crosswalk's two matrices and the citations register, and the
        docs/ adopter documents), each path taken from the generator's own
        configuration where it carries one, is named in the CONTENT BOUNDARY
        paragraph, as are its two file checks that read no content."""
        mod = self.mod
        doc = mod.__doc__
        boundary = " ".join(doc[doc.index("CONTENT BOUNDARY"):
                                doc.index("QUALITATIVE, NOT COUNTED")].split())

        def rel(path):
            return path.relative_to(mod.REPO_ROOT).as_posix()

        draft = next(v for v in mod.VARIANTS if v.draft_rules)
        reads = [
            rel(mod.template_dir_for(draft)) + "/",
            rel(mod.WEB_DIR / "baseline") + "/",
            # read_baseline_pin's default path (the pin gate 110 checks).
            ".baseline/pin.toml",
            rel(mod.CROSSWALK_COMPLIANCE_MATRIX),
            rel(mod.CROSSWALK_REVERSE_MATRIX),
            rel(mod.CITATIONS_REGISTER),
            rel(mod.ADOPTER_DOCS_DIR) + "/*.md",
        ]
        for path in reads:
            self.assertIn(f"``{path}``", boundary, path)
        self.assertIn("the adopter Related Documents check's one "
                      "``git ls-files`` call returns tracked paths", boundary)
        self.assertIn("the Browse adventure's artefact links check only that "
                      "each named file exists", boundary)
        self.assertIn("the draft's adopter document pages and listings",
                      boundary)
        self.assertNotIn("adopter-guide pages", boundary)


class DraftRefusalGuardTests(unittest.TestCase):
    """4: the draft-scoped refusal guard, class by class."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()

    def test_each_refusal_class_raises(self):
        cases = {
            "an en dash": "<p>a – b</p>",
            "an em dash": "<p>a — b</p>",
            "an inline style element": "<style>p { color: red; }</style>",
            "an inline script element": "<script>alert(1)</script>",
            "a style attribute": '<p style="color: red">x</p>',
            "an on* event attribute": '<p onclick="x()">x</p>',
            '"what this is"': "<p>What this is and is not.</p>",
        }
        for what, snippet in cases.items():
            with self.subTest(what=what):
                with self.assertRaisesRegex(self.mod.BuildError, "refusal"):
                    self.mod.refuse_draft_page("draft/x.html", snippet)

    def test_each_entity_encoded_dash_spelling_raises(self):
        """Round-2 WARN: an entity-encoded dash would render as a dash and
        pass the literal-character scan. Round-3 WARN: an exact spelling list
        missed valid forms with no trailing semicolon, with leading zeros, and
        the Windows-1252 code points; the guard decodes the page, so every
        spelling that decodes to a dash must be refused."""
        spellings = (
            # round 2: named entities and plain numeric references (the hex
            # forms in either case of the x)
            "&ndash;", "&mdash;", "&#8211;", "&#8212;",
            "&#x2013;", "&#X2013;", "&#x2014;", "&#X2014;",
            # round 3: no trailing semicolon
            "&#8211", "&#8212", "&#x2013", "&#x2014",
            # round 3: leading zeros
            "&#08211;", "&#08212;", "&#x02013;", "&#x02014;",
            # round 3: Windows-1252 code points, decimal and hex
            "&#150;", "&#151;", "&#x96;", "&#X96;", "&#x97;", "&#X97;",
        )
        for spelling in spellings:
            with self.subTest(spelling=spelling):
                with self.assertRaisesRegex(self.mod.BuildError, "refusal"):
                    self.mod.refuse_draft_page(
                        "draft/x.html", f"<p>a {spelling} b</p>")

    def test_clean_page_and_external_script_pass(self):
        self.mod.refuse_draft_page(
            "draft/x.html",
            '<p>Clean.</p><script src="/draft/assets/baseline/copy.js" '
            "defer></script>",
        )

    def test_text_that_only_shows_a_dash_spelling_passes(self):
        """Round-3 WARN companion: an escaped ampersand form decodes to the
        spelling itself, not to a dash, so prose that discusses a spelling is
        not refused. Round-4 NOTE: a named reference with no trailing
        semicolon is one HTML5 does not decode (&ndash and &mdash are not in
        the legacy no-semicolon list), so it stays text and is accepted."""
        self.mod.refuse_draft_page(
            "draft/x.html",
            "<p>Write &amp;ndash; or &amp;#8211; here, or the undecoded "
            "&ndash and &mdash forms.</p>")

    def test_guard_is_wired_into_the_draft_render(self):
        mod = self.mod
        figures = mod.compute_figures()
        with tempfile.TemporaryDirectory() as tmp:
            doctored = Path(tmp) / "templates-draft"
            shutil.copytree(REPO_ROOT / ".web" / "templates-draft", doctored)
            page = doctored / "404.html"
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    "That page is not here.",
                    "That page — is not here.",
                ),
                encoding="utf-8",
            )
            variant = mod.Variant(
                "draft-fixture", str(doctored), "draft/", indexable=False,
                document_routes=True, pages=mod.DRAFT_PAGES, draft_rules=True,
            )
            with self.assertRaisesRegex(mod.BuildError, "em dash"):
                mod.render_variant(figures, variant)

    def test_guard_is_scoped_to_the_draft(self):
        mod = self.mod
        figures = mod.compute_figures()
        v1 = mod.VARIANTS[0]
        pages = dict(mod.render_variant(figures, v1))
        self.assertIn("<style", pages["index.html"],
                      "the live tree keeps its inline style partial, so the "
                      "guard must stay draft-scoped")


class DraftNarrativeShellTests(unittest.TestCase):
    """10: the draft reading room's build-time contracts, on fixtures."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()

    def test_unknown_narrative_type_fails_the_build(self):
        mod = self.mod
        with self.assertRaisesRegex(mod.BuildError, "DRAFT_NARRATIVE_SUBTYPES"):
            mod.draft_narrative_subtype("Board Memo")
        figures = dict(mod.compute_figures())
        figures["narratives"] = [dict(p) for p in figures["narratives"]]
        figures["narratives"][0]["narrative_type"] = "Board Memo"
        draft = next(v for v in mod.VARIANTS if v.draft_rules)
        with self.assertRaisesRegex(mod.BuildError, "DRAFT_NARRATIVE_SUBTYPES"):
            mod.render_variant(figures, draft)

    def test_reserved_ids_cover_the_draft_narrative_template(self):
        """A body heading slugging to a shell id raises (the RR guard), so
        the reservation must be exactly the template's own ids plus the
        renderer's narr-intro."""
        tmpl = (REPO_ROOT / ".web" / "templates-draft" / "narrative.html"
                ).read_text(encoding="utf-8")
        reserved = self.mod.NARRATIVE_SHELL_IDS["templates-draft"]
        self.assertEqual(set(_ID_RE.findall(tmpl)) | {"narr-intro"}, reserved)

    def test_body_adapter_gives_sections_a_box_and_links_the_hint(self):
        mod = self.mod
        body = ("# T\n\n---\n\nIntro.\n\n## First part\n\nSee the "
                "[policy](../../README.md).\n\n**End of Document**\n")
        html, _ = mod.render_narrative_body(
            body, "executive/briefs/x.md",
            mod.NARRATIVE_SHELL_IDS["templates-draft"])
        adapted = mod.draft_narrative_body(html, "executive/briefs/x.md")
        self.assertNotRegex(adapted, r"<section[^>]*\bid=")
        self.assertIn('<div id="first-part">', adapted)
        self.assertIn('<div id="narr-intro">', adapted)
        self.assertIn(
            f'<a href="{mod.GITHUB_BLOB_BASE}README.md" target="_blank" '
            'rel="noopener noreferrer">policy<span class="vh"> (opens in a '
            "new tab)</span></a>", adapted)
        with self.assertRaisesRegex(mod.BuildError, "renderer change"):
            mod.draft_narrative_body(
                html.replace('class="narr" id=', 'class="narr x" id=', 1),
                "executive/briefs/x.md")
        with self.assertRaisesRegex(mod.BuildError, "renderer change"):
            mod.draft_narrative_body(
                html.replace('rel="noopener"', 'rel="external"', 1),
                "executive/briefs/x.md")


class DraftConcernMappingTests(unittest.TestCase):
    """11: the concern mapping's loud build checks, on doctored inputs, so the
    mapping stays mechanical rather than silently stale (design D section 5)."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()
        cls.figures = cls.mod.compute_figures()
        full = cls.mod.parse_taxonomy_full(
            cls.mod.TAXONOMY.read_text(encoding="utf-8"))
        cls.docs_by_path = {d["path"]: d for d in full}

    def test_the_committed_mapping_joins_cleanly(self):
        joined = self.mod.draft_concern_join(self.figures, self.docs_by_path)
        self.assertEqual([c["slug"] for c in joined],
                         [c["slug"] for c in self.mod.DRAFT_CONCERNS])

    def test_a_mapped_path_missing_from_the_registry_fails(self):
        mod = self.mod
        original = mod.DRAFT_CONCERNS
        doctored = [dict(c) for c in original]
        doctored[0]["pages"] = tuple(doctored[0]["pages"]) + (
            "executive/briefs/brief-not-in-the-registry.md",)
        try:
            mod.DRAFT_CONCERNS = tuple(doctored)
            with self.assertRaisesRegex(mod.BuildError,
                                        "maps a page not in"):
                mod.draft_concern_join(self.figures, self.docs_by_path)
        finally:
            mod.DRAFT_CONCERNS = original

    def test_a_registry_page_mapped_to_no_concern_fails(self):
        figures = dict(self.figures)
        extra = dict(figures["narratives"][0])
        extra["path"] = "executive/briefs/brief-new-and-unmapped.md"
        figures["narratives"] = list(figures["narratives"]) + [extra]
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "mapped to no concern"):
            self.mod.draft_concern_join(figures, self.docs_by_path)

    def test_a_gap_corpus_path_missing_from_the_taxonomy_fails(self):
        mod = self.mod
        original = mod.DRAFT_CONCERNS
        doctored = [dict(c) for c in original]
        for concern in doctored:
            if not concern["pages"]:
                concern["corpus"] = tuple(concern["corpus"]) + (
                    "governance/guideline-not-in-the-taxonomy.md",)
        try:
            mod.DRAFT_CONCERNS = tuple(doctored)
            with self.assertRaisesRegex(mod.BuildError,
                                        "corpus source not in"):
                mod.draft_concern_join(self.figures, self.docs_by_path)
        finally:
            mod.DRAFT_CONCERNS = original

    def test_a_concern_slug_colliding_with_a_subtype_route_fails(self):
        mod = self.mod
        original = mod.DRAFT_CONCERNS
        doctored = [dict(c) for c in original]
        doctored[0]["slug"] = "briefs"
        try:
            mod.DRAFT_CONCERNS = tuple(doctored)
            with self.assertRaisesRegex(mod.BuildError,
                                        "collide with a decide/ subtype"):
                mod.draft_concern_join(self.figures, self.docs_by_path)
        finally:
            mod.DRAFT_CONCERNS = original

    # Round-2 NOTE 5: each remaining loud check gets its negative test.

    def test_a_repeated_concern_slug_fails(self):
        mod = self.mod
        original = mod.DRAFT_CONCERNS
        doctored = [dict(c) for c in original]
        doctored[1]["slug"] = doctored[0]["slug"]
        try:
            mod.DRAFT_CONCERNS = tuple(doctored)
            with self.assertRaisesRegex(mod.BuildError,
                                        "repeated concern slug"):
                mod.draft_concern_join(self.figures, self.docs_by_path)
        finally:
            mod.DRAFT_CONCERNS = original

    def test_a_concern_group_outside_the_decide_groups_fails(self):
        mod = self.mod
        original = mod.DRAFT_CONCERNS
        doctored = [dict(c) for c in original]
        doctored[0]["group"] = "not-a-board-question"
        try:
            mod.DRAFT_CONCERNS = tuple(doctored)
            with self.assertRaisesRegex(mod.BuildError,
                                        "group outside DRAFT_DECIDE_GROUPS"):
                mod.draft_concern_join(self.figures, self.docs_by_path)
        finally:
            mod.DRAFT_CONCERNS = original

    def test_a_corpus_source_in_the_root_domain_fails(self):
        mod = self.mod
        root_paths = sorted(p for p, d in self.docs_by_path.items()
                            if d.get("domain") == mod.ROOT_DOMAIN)
        self.assertTrue(root_paths, "the taxonomy carries root documents")
        original = mod.DRAFT_CONCERNS
        doctored = [dict(c) for c in original]
        for concern in doctored:
            if not concern["pages"]:
                concern["corpus"] = tuple(concern["corpus"]) + (
                    root_paths[0],)
        try:
            mod.DRAFT_CONCERNS = tuple(doctored)
            with self.assertRaisesRegex(mod.BuildError,
                                        "corpus source in the root domain"):
                mod.draft_concern_join(self.figures, self.docs_by_path)
        finally:
            mod.DRAFT_CONCERNS = original

    def test_corpus_material_on_a_concern_with_pages_fails(self):
        """Round-2: the evidence-shelf intro says a mapped concern's documents
        are the ones its pages resolve to, so a curated corpus entry beside
        mapped pages fails the build rather than falsify the intro."""
        mod = self.mod
        original = mod.DRAFT_CONCERNS
        doctored = [dict(c) for c in original]
        mapped = next(c for c in doctored if c["pages"])
        mapped["corpus"] = (mod.DRAFT_EXAMPLE_DOC,)
        try:
            mod.DRAFT_CONCERNS = tuple(doctored)
            with self.assertRaisesRegex(mod.BuildError,
                                        "has mapped pages and corpus-only"):
                mod.draft_concern_join(self.figures, self.docs_by_path)
        finally:
            mod.DRAFT_CONCERNS = original

    def test_a_gap_concern_with_no_corpus_material_fails(self):
        """Round-3 NOTE: a concern with no mapped page and no corpus-only
        material would render the gap intros over an empty shelf, so it fails
        the build."""
        mod = self.mod
        original = mod.DRAFT_CONCERNS
        doctored = [dict(c) for c in original]
        gap = next(c for c in doctored if not c["pages"])
        gap["corpus"] = ()
        try:
            mod.DRAFT_CONCERNS = tuple(doctored)
            with self.assertRaisesRegex(mod.BuildError,
                                        "no mapped page and no corpus-only"):
                mod.draft_concern_join(self.figures, self.docs_by_path)
        finally:
            mod.DRAFT_CONCERNS = original

    def test_gap_shelf_sentences_take_the_form_for_the_shelf_count(self):
        """Round-3 NOTE: the committed gap shelf holds one document, so the
        rendered pages exercise only one form; both forms are checked here on
        the page values for a one-document and a two-document gap shelf."""
        joined = self.mod.draft_concern_join(self.figures, self.docs_by_path)
        gap = next(c for c in joined if not c["mapped_pages"])
        other = next(d for p, d in sorted(self.docs_by_path.items())
                     if d.get("domain") != self.mod.ROOT_DOMAIN
                     and p != gap["docs"][0]["path"])
        render = DraftSiteRenderTests
        for docs in ([gap["docs"][0]], [gap["docs"][0], other]):
            one_doc = len(docs) == 1
            values = self.mod.draft_concern_values({**gap, "docs": docs})
            with self.subTest(shelf=len(docs)):
                self.assertEqual(
                    f'<div class="callout"><p>{values["CONCERN_NOTE"]}'
                    "</p></div>", render.GAP_QUALIFIER[one_doc])
                self.assertTrue(values["CONCERN_LEADERSHIP"].endswith(
                    render.GAP_MATERIAL[one_doc]))
                self.assertEqual(f'<p>{values["CONCERN_DOCS_INTRO"]}</p>',
                                 render.DOCS_INTRO_GAP[one_doc])

    def test_mapped_shelf_intro_takes_the_form_for_the_shelf_count(self):
        """Round-3 NOTE: every committed mapped shelf holds several documents,
        so the one-document form of its intro is checked here on the page
        values."""
        joined = self.mod.draft_concern_join(self.figures, self.docs_by_path)
        mapped = next(c for c in joined if c["mapped_pages"])
        for docs in (mapped["docs"][:1], mapped["docs"][:2]):
            values = self.mod.draft_concern_values({**mapped, "docs": docs})
            with self.subTest(shelf=len(docs)):
                self.assertEqual(
                    f'<p>{values["CONCERN_DOCS_INTRO"]}</p>',
                    DraftSiteRenderTests.DOCS_INTRO_PAGES[len(docs) == 1])

    def test_a_registry_page_with_no_corpus_sources_fails(self):
        mod = self.mod
        lines = mod.NARRATIVE_REGISTRY.read_text(
            encoding="utf-8").splitlines(keepends=True)
        start = next(i for i, line in enumerate(lines)
                     if line.rstrip() == "  corpus_sources:")
        end = start + 1
        while lines[end].startswith("    - "):
            end += 1
        self.assertGreater(end, start + 1, "the fixture drops real entries")
        original = mod.NARRATIVE_REGISTRY
        with tempfile.TemporaryDirectory() as tmp:
            doctored = Path(tmp) / "narrative.yml"
            doctored.write_text("".join(lines[:start + 1] + lines[end:]),
                                encoding="utf-8")
            try:
                mod.NARRATIVE_REGISTRY = doctored
                with self.assertRaisesRegex(mod.BuildError,
                                            "with no corpus_sources"):
                    mod.load_narratives()
            finally:
                mod.NARRATIVE_REGISTRY = original


class DraftCrosswalkParserTests(unittest.TestCase):
    """Round-2 fixes 4, 6 and 8: the reverse matrix parser refuses an
    interrupted table and an unreadable link instead of dropping rows
    silently, and every instrument's reverse paths are validated at build.
    Round 3 items 1 to 3: a repeated heading and a plain-text path raise, and
    the register Topic name cuts only at a sentence-ending period."""

    _RM_HEAD = (
        "## X instrument\n\n"
        "| Area | Library documents | Alignment type |\n"
        "| --- | --- | --- |\n"
    )
    _RM_ROW = "| A.1 | [`x/a.md`](../x/a.md) | Industry practice |\n"

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()

    def test_blank_line_inside_a_reverse_table_raises(self):
        """agy F1: a blank line inside a section's table set the parser state
        to outside and silently dropped the rest of that table."""
        text = (self._RM_HEAD + self._RM_ROW + "\n"
                + "| A.2 | [`x/b.md`](../x/b.md) | Industry practice |\n")
        with self.assertRaisesRegex(self.mod.BuildError, "interrupted"):
            self.mod.parse_reverse_matrix(text)

    def test_stray_table_line_after_a_reverse_table_raises(self):
        text = (self._RM_HEAD + self._RM_ROW
                + "\nSome prose after the table.\n\n| stray | row | here |\n")
        with self.assertRaisesRegex(self.mod.BuildError, "interrupted"):
            self.mod.parse_reverse_matrix(text)

    def test_non_instrument_table_stays_tolerated(self):
        text = ("## Purpose\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n\n"
                + self._RM_HEAD + self._RM_ROW)
        sections = self.mod.parse_reverse_matrix(text)
        self.assertEqual(list(sections), ["X instrument"])
        self.assertEqual(sections["X instrument"]["rows"][0]["paths"],
                         ["x/a.md"])

    def test_reverse_cell_accepts_backticked_and_bare_links(self):
        """agy F5: the backtick-only pattern silently dropped a bare markdown
        link in a multi-link cell."""
        text = (self._RM_HEAD
                + "| A.1 | [`x/a.md`](../x/a.md), [x/b.md](../x/b.md) | "
                "Industry practice |\n")
        sections = self.mod.parse_reverse_matrix(text)
        self.assertEqual(sections["X instrument"]["rows"][0]["paths"],
                         ["x/a.md", "x/b.md"])

    def test_reverse_cell_with_unreadable_link_raises(self):
        cases = (
            # an unbalanced backtick in the link text
            "[`x/a.md`](../x/a.md), [`x/b.md](../x/b.md)",
            # an empty link text
            "[`x/a.md`](../x/a.md), [](../x/b.md)",
        )
        for cell in cases:
            with self.subTest(cell=cell):
                text = (self._RM_HEAD
                        + f"| A.1 | {cell} | Industry practice |\n")
                with self.assertRaisesRegex(self.mod.BuildError,
                                            "cannot read"):
                    self.mod.parse_reverse_matrix(text)

    def test_repeated_reverse_heading_raises(self):
        """Round 3 item 1: two sections under one heading made the second
        table overwrite the first silently (only its rows survived)."""
        text = (self._RM_HEAD + self._RM_ROW + "\n"
                + self._RM_HEAD
                + "| A.2 | [`x/b.md`](../x/b.md) | Industry practice |\n")
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "duplicate reverse matrix table"):
            self.mod.parse_reverse_matrix(text)

    def test_plain_text_path_in_a_matrix_cell_raises(self):
        """Round 3 item 2: a document path written as plain text beside the
        links was dropped silently."""
        cases = (
            "[`x/a.md`](../x/a.md), `x/b.md`",
            "[`x/a.md`](../x/a.md), x/b.md",
            "x/b.md",
        )
        for cell in cases:
            with self.subTest(cell=cell):
                text = (self._RM_HEAD
                        + f"| A.1 | {cell} | Industry practice |\n")
                with self.assertRaisesRegex(self.mod.BuildError,
                                            "outside its document links"):
                    self.mod.parse_reverse_matrix(text)

    def test_matrix_cell_separators_stay_accepted(self):
        text = (self._RM_HEAD
                + "| A.1 | [`x/a.md`](../x/a.md) ; [`x/b.md`](../x/b.md) ,"
                " [`x/c.md`](../x/c.md) | Industry practice |\n")
        sections = self.mod.parse_reverse_matrix(text)
        self.assertEqual(sections["X instrument"]["rows"][0]["paths"],
                         ["x/a.md", "x/b.md", "x/c.md"])

    def test_topic_name_cuts_only_at_a_sentence_end(self):
        """Round 3 item 3: any top-level period cut the name, so "Privacy
        Framework 1.0 for ..." became "Privacy Framework 1". Expected names
        are literal strings."""
        cases = {
            "Privacy Framework 1.0 for managing privacy risk":
                "Privacy Framework 1.0 for managing privacy risk",
            "Secure Software Development Framework v1.1. Superseded later":
                "Secure Software Development Framework v1.1",
            "Cloud Controls Matrix v4.1.":
                "Cloud Controls Matrix v4.1",
            "AI regulation (EU) 2024/1689. Amended 2026":
                "AI regulation 2024/1689",
            "Requirements 2.0; Amd 1:2024 (Climate action changes)":
                "Requirements 2.0",
            "A name (v2.0. a remark) with a tail":
                "A name with a tail",
        }
        for topic, name in cases.items():
            with self.subTest(topic=topic):
                self.assertEqual(self.mod._xw_topic_name(topic), name)

    def test_reverse_paths_validated_for_every_instrument(self):
        """agy F3: paths were validated only for instruments without a
        compliance column; a stale path in, say, the ISO/IEC 27001 section
        (which has one) surfaced as a KeyError at render. Every reverse
        row's paths fail the build loudly."""
        mod = _load_build()
        real = mod.CROSSWALK_REVERSE_MATRIX.read_text(encoding="utf-8")
        marker = "| A.5.7 Threat intelligence"
        self.assertIn(marker, real)
        doctored = real.replace(
            marker,
            "| A.0 Fixture | [`governance/no-such-document.md`]"
            "(no-such-document.md) | Industry practice |\n" + marker, 1)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "reverse.md"
            path.write_text(doctored, encoding="utf-8")
            mod.CROSSWALK_REVERSE_MATRIX = path
            full = mod.parse_taxonomy_full(
                mod.TAXONOMY.read_text(encoding="utf-8")
            )
            with self.assertRaisesRegex(mod.BuildError,
                                        "no-such-document"):
                mod.build_crosswalk(full)


class BaselineAssetCopyFixtureTests(unittest.TestCase):
    """6: build-time pin verification failure classes, on fixtures."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()

    def _fixture(self):
        root = Path(tempfile.mkdtemp(prefix="draft-assets-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        baseline = root / "baseline"
        (baseline / "fonts").mkdir(parents=True)
        files = {
            "baseline.css": b"body { color: green; }\n",
            "fonts/sample-LICENSE.txt": b"SIL OFL 1.1 sample\n",
        }
        for rel, data in files.items():
            (baseline / rel).write_bytes(data)
        pin = root / "pin.toml"
        lines = ['version = "1.5.0"', "", "[files]"]
        lines += [
            f'".web/baseline/{rel}" = "{hashlib.sha256(data).hexdigest()}"'
            for rel, data in sorted(files.items())
        ]
        pin.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return baseline, pin

    def test_clean_fixture_loads(self):
        baseline, pin = self._fixture()
        assets = dict(self.mod.load_baseline_assets(baseline, pin))
        self.assertEqual(sorted(assets),
                         ["baseline.css", "fonts/sample-LICENSE.txt"])

    def test_licence_page_version_comes_from_the_pin(self):
        """Round-1 NOTE (spec section 11: no hard-coded versions): the
        licence page names the version the pin carries, so a bump needs no
        template edit."""
        _, pin = self._fixture()
        pin.write_text(
            pin.read_text(encoding="utf-8").replace(
                'version = "1.5.0"', 'version = "9.8.7"'
            ),
            encoding="utf-8",
        )
        self.assertEqual(
            self.mod.draft_license_values(pin)["BASELINE_VERSION"], "9.8.7")

    def test_tampered_byte_fails(self):
        baseline, pin = self._fixture()
        target = baseline / "baseline.css"
        data = bytearray(target.read_bytes())
        data[0] ^= 0x01
        target.write_bytes(bytes(data))
        with self.assertRaisesRegex(self.mod.BuildError, "SHA-256"):
            self.mod.load_baseline_assets(baseline, pin)

    def test_missing_pinned_file_fails(self):
        baseline, pin = self._fixture()
        (baseline / "baseline.css").unlink()
        with self.assertRaisesRegex(self.mod.BuildError, "missing"):
            self.mod.load_baseline_assets(baseline, pin)

    def test_unpinned_extra_file_fails(self):
        baseline, pin = self._fixture()
        (baseline / "extra.js").write_bytes(b"alert(1)\n")
        with self.assertRaisesRegex(self.mod.BuildError, "unpinned"):
            self.mod.load_baseline_assets(baseline, pin)

    def test_pin_key_outside_tree_fails(self):
        baseline, pin = self._fixture()
        pin.write_text(
            pin.read_text(encoding="utf-8").replace(
                '".web/baseline/baseline.css"', '"docs/outside.md"'
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(self.mod.BuildError, "outside"):
            self.mod.load_baseline_assets(baseline, pin)

    def test_missing_pin_fails(self):
        baseline, pin = self._fixture()
        pin.unlink()
        with self.assertRaisesRegex(self.mod.BuildError, "pin file not found"):
            self.mod.load_baseline_assets(baseline, pin)

    def test_pin_errors_name_the_pin_for_both_readers(self):
        """Round-2 NOTE: read_baseline_pin serves the asset copy and the
        licence page, so its errors carry a neutral "baseline pin:" prefix,
        not "draft asset copy:", whichever reader hit them."""
        cases = {
            "missing": lambda pin: pin.unlink(),
            "malformed": lambda pin: pin.write_text(
                "version = \n", encoding="utf-8"),
            "no version": lambda pin: pin.write_text(
                pin.read_text(encoding="utf-8").replace(
                    'version = "1.5.0"', ""),
                encoding="utf-8"),
        }
        for what, spoil in cases.items():
            for reader in ("assets", "licence"):
                with self.subTest(what=what, reader=reader):
                    baseline, pin = self._fixture()
                    spoil(pin)
                    with self.assertRaisesRegex(
                            self.mod.BuildError, r"^baseline pin: "):
                        if reader == "assets":
                            self.mod.load_baseline_assets(baseline, pin)
                        else:
                            self.mod.draft_license_values(pin)


class DraftLoadedScriptsTests(unittest.TestCase):
    """6: the disclosure's script list is generated from the rendered pages,
    on fixtures, so a script from outside the baseline fails the build
    instead of dropping out of the list."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()

    def test_names_every_baseline_script_once_sorted(self):
        pages = [
            '<script src="/draft/assets/baseline/rail.js" defer></script>'
            '<script src="/draft/assets/baseline/copy.js" defer></script>',
            '<script src="/draft/assets/baseline/copy.js" defer></script>',
        ]
        self.assertEqual(
            self.mod.draft_loaded_scripts(pages, "/draft/assets/baseline/"),
            ["copy.js", "rail.js"])

    def test_script_outside_the_baseline_fails(self):
        for src in ("/elsewhere/x.js", "/draft/assets/other.js",
                    "/draft/assets/baseline/nested/x.js"):
            with self.subTest(src=src):
                with self.assertRaisesRegex(self.mod.BuildError,
                                            "not a baseline asset"):
                    self.mod.draft_loaded_scripts(
                        [f'<script src="{src}" defer></script>'],
                        "/draft/assets/baseline/")


class BaselinePinGateTests(unittest.TestCase):
    """6: gate 110 on the vendored tree, outside the shared render, so a pin
    or copy fault fails this test by name."""

    def test_gate_110_passes_on_the_vendored_tree(self):
        """The baseline-pin integrity audit (gate 110, named in
        .github/workflows/quality.yml) agrees with the vendored tree and
        reports the pin.toml version."""
        import contextlib
        import io
        import tomllib
        version = tomllib.loads(
            (REPO_ROOT / ".baseline" / "pin.toml").read_text(encoding="utf-8")
        )["version"]
        spec = importlib.util.spec_from_file_location(
            "lint_baseline_pin_mod", REPO_ROOT / "tools" / "lint-baseline-pin.py"
        )
        gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gate)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = gate.main(["lint-baseline-pin.py", "--root", str(REPO_ROOT)])
        self.assertEqual(code, 0, out.getvalue())
        self.assertIn(f"(baseline {version}).", out.getvalue())


class PaletteGateFixtureTests(unittest.TestCase):
    """25: the palette gate (spec section 4 items 2 and 3) as the build runs
    it, on fixtures: the released palette passes, and a doctored palette, an
    override in only 1 of a scheme's 2 forms, an altered gate, a symlinked
    gate and a pin without the gate each fail; what runs is a private copy
    of the hashed bytes, never the gate path."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()

    def _root(self):
        root = Path(tempfile.mkdtemp(prefix="draft-palette-gate-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        return root

    def _palettes(self, css):
        path = self._root() / "palettes.css"
        path.write_text(css, encoding="utf-8")
        return path

    def _released(self):
        return self.mod.PALETTE_CSS.read_text(encoding="utf-8")

    def test_released_palette_passes(self):
        self.assertIsNone(self.mod.run_palette_gate())

    def test_low_contrast_dark_text_fails(self):
        bad = self._palettes(_doctor_dark_token(
            self._released(), "text-muted", "#2a2a2a"))
        with self.assertRaisesRegex(self.mod.BuildError,
                                    r"text-muted .*FAIL.*RESULT: fail"):
            self.mod.run_palette_gate(bad)

    def test_override_in_one_dark_form_only_fails(self):
        bad = self._palettes(_doctor_dark_token(
            self._released(), "bg", "#000000", openers=_DARK_BLOCKS[1:]))
        with self.assertRaisesRegex(self.mod.BuildError,
                                    r"FAIL grclibrary / dark: --bg"):
            self.mod.run_palette_gate(bad)

    def test_altered_gate_is_not_run(self):
        gate = self._root() / "check_palette.py"
        gate.write_bytes(
            (REPO_ROOT / self.mod.PALETTE_GATE_KEY).read_bytes()
            + b"\nraise SystemExit(0)\n")
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "does not match its pinned SHA-256"):
            self.mod.run_palette_gate(gate=gate)

    def test_symlinked_gate_is_not_run(self):
        """Round 2 NOTE 3: a symbolic link to the pinned gate bytes is
        refused by lstat, never followed (is_file followed it)."""
        gate = self._root() / "check_palette.py"
        gate.symlink_to(REPO_ROOT / self.mod.PALETTE_GATE_KEY)
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "is not a regular file"):
            self.mod.run_palette_gate(gate=gate)

    def test_gate_runs_a_private_copy_of_the_hashed_bytes(self):
        """Round 2 NOTE 3: the build runs a temporary copy of exactly the
        bytes it hashed, removed afterwards, never the gate path. The
        fixture gate, pinned by a fixture pin, reports the path it ran
        from."""
        root = self._root()
        gate = root / "check_palette.py"
        gate.write_bytes(b"import sys\nprint('ERROR ran ' + __file__)\n"
                         b"sys.exit(1)\n")
        pin = root / "pin.toml"
        pin.write_text(
            'version = "9.9.9"\n\n[files]\n'
            f'"{self.mod.PALETTE_GATE_KEY}" = '
            f'"{hashlib.sha256(gate.read_bytes()).hexdigest()}"\n',
            encoding="utf-8")
        with self.assertRaisesRegex(self.mod.BuildError,
                                    r"ERROR ran (\S+)") as caught:
            self.mod.run_palette_gate(gate=gate, pin_path=pin)
        ran = Path(re.search(r"ERROR ran (\S+)",
                             str(caught.exception)).group(1))
        self.assertNotEqual(ran.resolve(), gate.resolve(),
                            "the gate path itself ran, not the hashed copy")
        self.assertEqual(ran.name, gate.name)
        self.assertFalse(ran.exists(), "the private copy was not removed")

    def test_pin_without_the_gate_fails(self):
        pin = self._root() / "pin.toml"
        pin.write_text(
            "\n".join(
                line for line in (REPO_ROOT / ".baseline" / "pin.toml")
                .read_text(encoding="utf-8").splitlines()
                if not line.startswith(f'"{self.mod.PALETTE_GATE_KEY}"'))
            + "\n", encoding="utf-8")
        with self.assertRaisesRegex(self.mod.BuildError, "has no pin entry"):
            self.mod.run_palette_gate(pin_path=pin)

    def test_asset_copy_skips_only_the_gate_key(self):
        """The gate's pin key is the one key outside .web/baseline/ the asset
        copy accepts, and it is never copied (served)."""
        assets = dict(self.mod.load_baseline_assets())
        self.assertNotIn("check_palette.py", {Path(r).name for r in assets})
        self.assertIn("scheme.js", assets)


class StickyTableBoundFixtureTests(unittest.TestCase):
    """6: the spec 7.31 check finds an unbounded sticky table, on fixtures,
    so the render test above cannot pass by matching nothing."""

    def test_unbounded_sticky_table_is_found(self):
        html = ('<div class="tablewrap" tabindex="0"><table class="sticky">'
                '<caption class="vh">x</caption></table></div>')
        self.assertEqual(len(_unbounded_sticky_tables(html)), 1)

    def test_bounded_sticky_and_plain_tables_pass(self):
        html = (
            '<div class="tablewrap bounded" tabindex="0">'
            '<table class="matrix sticky sticky-col" data-matrix></table></div>'
            '<div class="tablewrap" tabindex="0"><table class="fixed"></table>'
            "</div>"
        )
        self.assertEqual(_unbounded_sticky_tables(html), [])


class MatrixScriptFixtureTests(unittest.TestCase):
    """6: the matrix.js loading rule (spec 7.30 and section 8), on fixtures,
    so the render test above cannot pass while no draft page has a matrix
    (round-1 ERROR: False equalled False on every page)."""

    SCRIPT = '<script src="/draft/assets/baseline/matrix.js" defer></script>'
    MATRIX = ('<div class="tablewrap bounded" tabindex="0">'
              '<table class="matrix sticky sticky-col" data-matrix></table>'
              "</div>")
    PLAIN = ('<div class="tablewrap" tabindex="0"><table class="fixed">'
             "</table></div>")

    def test_matrix_page_loads_matrix_js(self):
        self.assertEqual(_matrix_script_faults(self.SCRIPT + self.MATRIX), [])

    def test_page_without_a_matrix_omits_matrix_js(self):
        self.assertEqual(_matrix_script_faults(self.PLAIN), [])

    def test_matrix_without_matrix_js_is_found(self):
        self.assertEqual(_matrix_script_faults(self.MATRIX),
                         ["a data-matrix table without matrix.js"])

    def test_matrix_js_without_a_matrix_is_found(self):
        self.assertEqual(_matrix_script_faults(self.SCRIPT + self.PLAIN),
                         ["matrix.js without a data-matrix table"])

    def test_second_matrix_is_found(self):
        self.assertEqual(
            _matrix_script_faults(self.SCRIPT + self.MATRIX + self.MATRIX),
            ["2 matrices (1 per page, spec 7.30)"])


class AdopterDocsFixtureTests(unittest.TestCase):
    """18 and 21: the docs/ metadata reader's loud failure classes, on
    fixtures (round-2 fixes 1, 2, 7 and 8: only the leading block is read,
    the full 13-field model is validated, related documents resolve by link
    target, and nothing, README.md included, is skipped silently).
    parse_adopter_docs reads ADOPTER_DOCS_DIR; each test points it at a
    doctored tree and restores it."""

    FIELDS = (
        ("Document Title", "Fixture Guide"),
        ("Document Type", "Guide"),
        ("Version", "1.0.0"),
        ("Date", "2026-11-03"),
        ("Owner", "Governance Library Maintainer"),
        ("Approving Authority", "Governance Library Maintainer"),
        ("Related Documents", "[`docs/adopter-guide.md`](adopter-guide.md)"),
        ("Classification", "Public"),
        ("Category", "Documentation"),
        ("Review Frequency", "Annual"),
        ("Repository Path", "[`docs/fixture.md`](fixture.md)"),
        ("Confidentiality", "Public"),
        ("License", "CC BY-SA 4.0"),
    )

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()

    def _block(self, overrides=None, drop=(), extra=()):
        fields = [(n, v) for n, v in self.FIELDS if n not in drop]
        if overrides:
            fields = [(n, overrides.get(n, v)) for n, v in fields]
        fields += list(extra)
        lines = []
        for i, (name, value) in enumerate(fields):
            suffix = "\\" if i < len(fields) - 1 else ""
            lines.append(f"**{name}:** {value}{suffix}")
        return "\n".join(lines)

    def _doc(self, overrides=None, drop=(), extra=()):
        return (
            "# Fixture guide\n\n" + self._block(overrides, drop, extra)
            + "\n\n---\n\n## Overview\n\nA fixture paragraph.\n"
        )

    def _parse(self, files):
        root = Path(tempfile.mkdtemp(prefix="adopter-docs-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        for name, text in files.items():
            (root / name).write_text(text, encoding="utf-8")
        original = self.mod.ADOPTER_DOCS_DIR
        self.mod.ADOPTER_DOCS_DIR = root
        try:
            return self.mod.parse_adopter_docs()
        finally:
            self.mod.ADOPTER_DOCS_DIR = original

    def test_clean_fixture_parses(self):
        records = self._parse({"fixture.md": self._doc()})
        self.assertEqual([r["title"] for r in records], ["Fixture Guide"])
        self.assertEqual(records[0]["purpose"], "A fixture paragraph.")
        self.assertEqual(records[0]["related_documents"],
                         ["docs/adopter-guide.md"])

    def test_fenced_example_block_never_reads_as_the_document(self):
        """Round-2 ERROR 1: with a guide's real block removed, the old
        scanner read the fenced example's block as the document instead of
        failing; only the leading block may count."""
        body = (
            "# Fixture guide\n\nIntro prose, no metadata block.\n\n"
            "```markdown\n# Example\n\n" + self._block() + "\n```\n\n"
            "## Overview\n\nA fixture paragraph.\n"
        )
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "no leading metadata block"):
            self._parse({"fixture.md": body})

    def test_a_file_without_a_block_fails(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "no leading metadata block"):
            self._parse({"fixture.md": "# Fixture guide\n\nProse only.\n"})

    def test_a_blank_line_mid_block_fails_loudly(self):
        """Round-2 ERROR 2: a blank line mid-block dropped every later
        field silently (the first four satisfied the old check)."""
        lines = self._block().splitlines()
        lines.insert(4, "")
        doc = "# Fixture guide\n\n" + "\n".join(lines) + "\n\n---\n"
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "missing metadata field"):
            self._parse({"fixture.md": doc})

    def test_a_missing_license_fails(self):
        """Round-2 ERROR 2: a missing License rendered an empty licence."""
        with self.assertRaisesRegex(self.mod.BuildError, "License"):
            self._parse({"fixture.md": self._doc(drop=("License",))})

    def test_an_unknown_field_name_fails(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "unknown metadata field"):
            self._parse(
                {"fixture.md": self._doc(extra=(("Colour", "Blue"),))})

    def test_an_invalid_date_fails(self):
        for bad in ("2026-13-40", "26-10-26", "2026/10/26"):
            with self.subTest(date=bad):
                with self.assertRaisesRegex(self.mod.BuildError,
                                            "invalid Date"):
                    self._parse({"fixture.md": self._doc({"Date": bad})})

    def test_an_invalid_version_fails(self):
        # The last is a non-ASCII digit: the site rule takes ASCII digits
        # only (round-3 note 7).
        for bad in ("v1.2.3", "1.2", "1.2.3-rc1", "1.0.١"):
            with self.subTest(version=bad):
                with self.assertRaisesRegex(self.mod.BuildError,
                                            "invalid Version"):
                    self._parse(
                        {"fixture.md": self._doc({"Version": bad})})

    def test_version_rule_agrees_with_the_corpus_rule(self):
        """Round-4 WARN 2: the round-3 site rule refused a leading zero
        ('01.0.0') that the corpus metadata gate, which covers docs/, and
        the maturity heuristic both accept, so one file could pass
        lint-metadata and fail the site build. Every version string below,
        leading zeros included, is judged the same by all three."""
        gate = _load_module(
            ".corpus-management/tools/gate_lint_metadata.py",
            "gate_lint_metadata_draft_mod")
        portal = _load_module("tools/build-portal.py",
                              "portal_version_draft_mod")
        versions = ("01.0.0", "1.00.0", "1.0.01", "00.0.0", "0.0.1",
                    "1.0.0", "10.20.30", "3.0.11", "v1.2.3", "1.2",
                    "1.2.3-rc1", "1.2.3.4", "1..0")
        for version in versions:
            with self.subTest(version=version):
                gate_ok = bool(gate.VERSION_RE.match(version))
                try:
                    portal.classify_maturity(
                        {"path": "docs/fixture.md", "version": version})
                    portal_ok = True
                except SystemExit:
                    portal_ok = False
                try:
                    self._parse(
                        {"fixture.md": self._doc({"Version": version})})
                    site_ok = True
                except self.mod.BuildError as e:
                    self.assertIn("invalid Version", str(e))
                    site_ok = False
                self.assertEqual(site_ok, gate_ok, "site and corpus gate")
                self.assertEqual(portal_ok, gate_ok,
                                 "maturity heuristic and corpus gate")
        self.assertTrue(gate.VERSION_RE.match("01.0.0"),
                        "the corpus rule accepts a leading zero")

    def test_module_docstring_agrees_with_the_version_rule(self):
        """NOTE fix: PR 9's round-3 docstring item said a Version with a
        leading zero fails the build, which round 4 reversed (item 21: a
        leading zero is accepted). The docstring must never claim a leading
        zero fails while the rule accepts one: every docstring sentence
        naming a leading zero must be an accepted-form sentence."""
        self.assertIsNotNone(self.mod._ADOPTER_VERSION_RE.match("01.0.0"),
                             "the site rule accepts a leading zero")
        mentions = [s for s in re.split(r"(?<=[.;])\s+", __doc__)
                    if "leading zero" in s]
        self.assertTrue(mentions, "the docstring states the rule")
        for sentence in mentions:
            self.assertIn("accepted", sentence, sentence)
            self.assertNotIn("fail", sentence, sentence)

    def test_a_repeated_field_name_fails(self):
        """Round-3 WARN 2: a second Version line overwrote the first
        silently, so the page showed whichever came last."""
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "repeats metadata field 'Version'"):
            self._parse(
                {"fixture.md": self._doc(extra=(("Version", "9.9.9"),))})

    def test_a_related_entry_the_parser_cannot_keep_fails(self):
        """Round-3 note 5: a Related Documents link without backticked text,
        or whose target is not a .md file, was dropped silently, and so was
        an entry that is not a link at all."""
        cases = (
            ("[adopter guide](adopter-guide.md)", "cannot keep"),
            ("[`docs/adopter-guide.md`](adopter-guide.md#modes)",
             "cannot keep"),
            ("[`LICENSE`](../LICENSE)", "cannot keep"),
            ("[`docs/adopter-guide.md`](adopter-guide.md), "
             "governance/register-glossary.md", "not a link"),
        )
        for value, message in cases:
            with self.subTest(value=value):
                with self.assertRaisesRegex(self.mod.BuildError, message):
                    self._parse({"fixture.md": self._doc(
                        {"Related Documents": value})})

    def test_a_related_target_that_is_not_a_tracked_repo_file_fails(self):
        """Round-4 note 4: a backticked link over a .md target was kept
        whatever the target named, so an absolute URL, a path outside the
        repository, and a missing file each rendered as a broken link."""
        cases = (
            ("an absolute URL",
             "[`docs/portal.md`](https://github.com/jposluns/grc_library/"
             "blob/main/docs/portal.md)"),
            ("a path outside the repository",
             "[`outside.md`](../../outside.md)"),
            ("an absolute filesystem path", "[`outside.md`](/outside.md)"),
            ("a missing file",
             "[`docs/no-such-file.md`](no-such-file.md)"),
        )
        for what, value in cases:
            with self.subTest(what=what):
                with self.assertRaisesRegex(
                        self.mod.BuildError,
                        "not a tracked file inside the repository"):
                    self._parse({"fixture.md": self._doc(
                        {"Related Documents": value})})

    def test_an_untracked_related_target_fails(self):
        """Round-4 note 4 companion: a file on disk that git does not track
        is not published, so its link would break too. The tracked set is
        git's answer; here it is narrowed to leave out the fixture's real,
        present target (docs/adopter-guide.md)."""
        self.assertTrue((REPO_ROOT / "docs" / "adopter-guide.md").is_file())
        original = self.mod._tracked_repo_files
        self.mod._tracked_repo_files = lambda: {"docs/portal.md"}
        try:
            with self.assertRaisesRegex(
                    self.mod.BuildError,
                    "not a tracked file inside the repository"):
                self._parse({"fixture.md": self._doc()})
        finally:
            self.mod._tracked_repo_files = original

    def _doctored_repo_root(self):
        """A doctored repository root for the two target-resolution tests
        (NOTE fix: the check's is_file() and resolve() clauses had no test),
        restored after the test."""
        repo = Path(tempfile.mkdtemp(prefix="adopter-repo-"))
        self.addCleanup(shutil.rmtree, repo, ignore_errors=True)
        (repo / "docs").mkdir()
        original_root = self.mod.REPO_ROOT

        def restore():
            self.mod.REPO_ROOT = original_root

        self.addCleanup(restore)
        self.mod.REPO_ROOT = repo
        return repo

    def test_a_tracked_target_with_no_file_on_disk_fails(self):
        """NOTE fix: tracked-set membership alone is not enough; the
        is_file() clause must refuse a tracked path whose file is absent
        from the work tree (a stale or doctored tracked set)."""
        self._doctored_repo_root()
        original = self.mod._tracked_repo_files
        self.mod._tracked_repo_files = lambda: {"docs/ghost.md"}
        try:
            with self.assertRaisesRegex(
                    self.mod.BuildError,
                    "not a tracked file inside the repository"):
                self._parse({"fixture.md": self._doc(
                    {"Related Documents": "[`docs/ghost.md`](ghost.md)"})})
        finally:
            self.mod._tracked_repo_files = original

    def test_a_tracked_symlink_target_fails(self):
        """NOTE fix: a tracked symlink passes the membership and is_file()
        clauses (is_file follows links), so the resolve() clause must refuse
        it; a symlinked target would publish a link to a page the build
        never renders under that path."""
        repo = self._doctored_repo_root()
        real = repo / "elsewhere.md"
        real.write_text("# elsewhere\n", encoding="utf-8")
        (repo / "docs" / "alias.md").symlink_to(real)
        self.assertTrue((repo / "docs" / "alias.md").is_file(),
                        "the symlink passes the file-presence clause")
        original = self.mod._tracked_repo_files
        self.mod._tracked_repo_files = lambda: {"docs/alias.md"}
        try:
            with self.assertRaisesRegex(
                    self.mod.BuildError,
                    "not a tracked file inside the repository"):
                self._parse({"fixture.md": self._doc(
                    {"Related Documents": "[`docs/alias.md`](alias.md)"})})
        finally:
            self.mod._tracked_repo_files = original

    def test_related_target_variable_does_not_shadow_the_parse_loop(self):
        """NOTE fix: inside parse_adopter_docs the Related Documents target
        path was assigned to ``path``, the parse loop's own variable (the
        docs/ file under parse), so any later use of ``path`` in the loop
        body would silently mean the last related target instead of the
        file. The inner name is target_path."""
        source = inspect.getsource(self.mod.parse_adopter_docs)
        self.assertIn("target_path = REPO_ROOT / target", source)
        self.assertNotRegex(source, r"(?<![\w])path = REPO_ROOT",
                            "the loop variable 'path' is never reassigned")

    def test_an_unknown_document_type_fails(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "DRAFT_TYPE_PLURALS"):
            self._parse(
                {"fixture.md": self._doc({"Document Type": "Essay"})})

    def test_an_empty_directory_fails(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "no adopter documents"):
            self._parse({})

    def test_a_missing_directory_fails(self):
        root = Path(tempfile.mkdtemp(prefix="adopter-gone-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        original = self.mod.ADOPTER_DOCS_DIR
        self.mod.ADOPTER_DOCS_DIR = root / "absent"
        try:
            with self.assertRaisesRegex(self.mod.BuildError, "not found"):
                self.mod.parse_adopter_docs()
        finally:
            self.mod.ADOPTER_DOCS_DIR = original

    def test_a_readme_is_not_silently_skipped(self):
        """Round-2 note 2: a docs/README.md was skipped silently; it must
        carry the block like any other docs/ file or fail the build."""
        with self.assertRaisesRegex(self.mod.BuildError, "docs/README.md"):
            self._parse({
                "fixture.md": self._doc(),
                "README.md": "# docs\n\nAn index, no block.\n",
            })

    def test_related_documents_resolve_by_target_not_text(self):
        """Round-2 fix 7 (agy F5): the old parser kept the link TEXT, so a
        descriptive text lost its link; the target, normalized from docs/,
        names the file."""
        doc = self._doc({"Related Documents":
                         "[`the adopter guide`](adopter-guide.md), "
                         "[`the glossary`](../governance/register-glossary.md)"})
        records = self._parse({"fixture.md": doc})
        self.assertEqual(records[0]["related_documents"],
                         ["docs/adopter-guide.md",
                          "governance/register-glossary.md"])

    def test_a_leading_bold_run_in_label_is_stripped(self):
        """Round-2 note 1: a lede opened 'Purpose. A public bibliography...'
        with the run-in label flattened into the prose."""
        body = ("# Fixture guide\n\n" + self._block()
                + "\n\n---\n\n## Overview\n\n"
                + "**Purpose.** A fixture bibliography.\n")
        records = self._parse({"fixture.md": body})
        self.assertEqual(records[0]["purpose"], "A fixture bibliography.")


class DraftRootTypeTests(unittest.TestCase):
    """Round-4 note 3: Browse ('plus N library specifications') and the
    documents index call every root document a library specification, so a
    root document of another type must fail the draft build.
    render_draft_variant reads TAXONOMY; the test points it at a doctored
    copy and restores it."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()

    def test_a_root_document_that_is_not_a_specification_fails(self):
        mod = self.mod
        figures = mod.compute_figures()
        text = mod.TAXONOMY.read_text(encoding="utf-8")
        doctored_text, n = re.subn(
            r'(- path: "([^"]*)"\n  domain: "root"\n  type: )"Specification"',
            r'\1"Guide"', text, count=1)
        self.assertEqual(n, 1, "no root Specification block in taxonomy.yml")
        path = re.search(r'- path: "([^"]*)"\n  domain: "root"\n  type: '
                         r'"Guide"', doctored_text).group(1)
        root = Path(tempfile.mkdtemp(prefix="draft-taxonomy-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        doctored = root / "taxonomy.yml"
        doctored.write_text(doctored_text, encoding="utf-8")
        draft = next(v for v in mod.VARIANTS if v.draft_rules)
        original = mod.TAXONOMY
        mod.TAXONOMY = doctored
        try:
            with self.assertRaisesRegex(
                    mod.BuildError,
                    re.escape(f"root document {path} has type 'Guide', "
                              "not Specification")):
                mod.render_variant(figures, draft)
        finally:
            mod.TAXONOMY = original


class DraftTemplateTypedCountTests(unittest.TestCase):
    """Round-2 fix 1: no draft template may type a count. Every number a page
    shows is computed at build time (owner decision), so a digit may appear in
    a template source only inside one of the listed exceptions."""

    # The exceptions, each a regex blanked from the source before the digit
    # scan; any digit that survives is a typed count and fails the test.
    EXCEPTIONS = (
        # The light and dark switch's two inline SVG glyphs, the moon and the
        # sun, exactly as the switch renders them (SCHEME_SWITCH, baseline
        # 1.6.0 section 7.33, copied from the reference pages): drawing sizes
        # and coordinates, not counts. Any other inline SVG is scanned. First,
        # so the class blanking below cannot break the literal match.
        *(re.escape(glyph) for glyph in re.findall(
            r'<svg class="(?:moon|sun)" .*?</svg>', SCHEME_SWITCH)),
        # A {{PLACEHOLDER}}: the computed values.
        r"\{\{[A-Z0-9_]+\}\}",
        # A URL in an href or src attribute.
        r'(?:href|src)="[^"]*"',
        # Structural id and class attribute values (anchor ids like d-1 and
        # the shared footer's slice-6 grid classes are positions, not counts).
        r'(?:id|class)="[^"]*"',
        # A tabindex value (the crosswalk's keyboard-focusable .tablewrap
        # scroll region): a focus position, not a count.
        r'tabindex="[^"]*"',
        # HTML heading tag names (h1, h2).
        r"</?h[1-6]\b",
        # The charset and viewport meta attribute values.
        r'(?:charset|content)="[^"]*"',
        # A licence version string: CC BY-SA 4.0, CC0 1.0, OFL 1.1 (the
        # template version is {{BASELINE_VERSION}}, from the pin).
        r"\d+(?:\.\d+)+",
        r"\bCC0\b",
        # A licence clause reference: 2(a)(1), 3(a)(1)(A), section 5.
        r"\b\d+(?:\([A-Za-z0-9]+\))+",
        r"\b[Ss]ection \d+\b",
        # The licence's own cure period, quoted from LICENSE section 6(b)(1).
        r"\b30 days\b",
        # The search page's example query names a standard edition.
        r"\bISO 27001\b",
        # The error page names its HTTP status.
        r"\b404\b",
        # The disclosure page's ordinal entry labels (positions, not counts).
        r"\bEntry \d+\b",
        # The shared family footer's fixed site-list label: the baseline
        # owns that wording, outside this site's copy.
        r'aria-label="The 6 project sites"',
    )

    def _typed_number(self, text):
        """The first digit run left once every exception is blanked."""
        for pattern in self.EXCEPTIONS:
            text = re.sub(pattern, " ", text)
        return re.search(r"\d+", text), text

    def test_only_the_switch_glyphs_are_exempt(self):
        """Round 2 NOTE 5: the SVG exception blanks the switch's own moon
        and sun glyphs and nothing else, so a typed count inside any other
        inline SVG still fails the scan."""
        glyphs = re.findall(r'<svg class="(?:moon|sun)" .*?</svg>',
                            SCHEME_SWITCH)
        self.assertEqual(len(glyphs), 2, "the switch's two glyphs")
        match, _ = self._typed_number(SCHEME_SWITCH)
        self.assertIsNone(match, "a switch glyph is not exempt")
        for svg in ('<svg class="badge"><text>358 documents</text></svg>',
                    '<svg class="moon"><text>358 documents</text></svg>'):
            match, _ = self._typed_number(svg)
            self.assertIsNotNone(match, f"an inline SVG is exempt: {svg}")
            self.assertEqual(match.group(0), "358")

    def test_no_typed_count_in_any_draft_template(self):
        template_root = REPO_ROOT / ".web" / "templates-draft"
        sources = sorted(template_root.rglob("*.html"))
        self.assertTrue(sources, "no draft template sources found")
        for path in sources:
            match, text = self._typed_number(
                path.read_text(encoding="utf-8"))
            if match:
                start = max(0, match.start() - 60)
                context = text[start:match.end() + 60].replace("\n", " ")
                self.fail(
                    f"{path.relative_to(REPO_ROOT)}: typed number "
                    f"{match.group(0)!r} outside the listed exceptions "
                    f"(counts are computed at build time, never typed): "
                    f"...{context}..."
                )


class DraftTestSectionNumberTests(unittest.TestCase):
    """Round-1 NOTE: two test sections both said 8. Each numbered section
    comment carries its own number from the module docstring's list. Round 2
    WARN 2: a class docstring's leading section number ("25: ...") names a
    docstring item too, and the item whose words it uses."""

    # Words too common to tie a docstring to one item.
    COMMON = frozenset(
        "a an and as at by each every for from has in is it its no not of on "
        "or so that the their to was where which while with".split())

    def test_section_comments_follow_the_module_docstring(self):
        items = re.findall(r"^(\d+)\. ", __doc__, re.M)
        source = Path(__file__).read_text(encoding="utf-8")
        sections = re.findall(r"^    # -- (\d+)\. ", source, re.M)
        self.assertTrue(sections, "no numbered section comments found")
        self.assertEqual(len(sections), len(set(sections)),
                         f"two sections share a number: {sections}")
        self.assertLessEqual(set(sections), set(items),
                             "a section number names no docstring item")

    def _phrases(self, text):
        """Adjacent pairs of uncommon words, possessives dropped."""
        words = re.findall(r"[a-z0-9][a-z0-9.-]*[a-z0-9]|[a-z]",
                           text.lower().replace("'s", ""))
        return {(a, b) for a, b in zip(words, words[1:])
                if a not in self.COMMON and b not in self.COMMON}

    def test_docstring_numbers_follow_the_module_docstring(self):
        """A class docstring's number names a docstring item, and when the
        docstring shares a two-word phrase with exactly one item, its own
        item is among those (the palette gate class said 24 while only item
        25 names the palette gate)."""
        items = dict(re.findall(r"^(\d+)\. (.*?)(?=^\d+\. |\Z)", __doc__,
                                re.M | re.S))
        phrases = {number: self._phrases(text)
                   for number, text in items.items()}
        numbered = 0
        for name, obj in sorted(globals().items()):
            if not inspect.isclass(obj) or obj.__module__ != __name__:
                continue
            doc = inspect.cleandoc(obj.__doc__ or "")
            match = re.match(r"(\d+): ", doc)
            if not match:
                continue
            numbered += 1
            number = match.group(1)
            self.assertIn(number, items,
                          f"{name}: docstring number {number} names no "
                          "docstring item")
            owners = set()
            for pair in self._phrases(doc[match.end():]):
                holders = [owner for owner, held in phrases.items()
                           if pair in held]
                if len(holders) == 1:
                    owners.update(holders)
            if owners:
                self.assertIn(number, owners,
                              f"{name}: docstring says {number} but its "
                              f"phrases belong to item(s) {sorted(owners)}")
        self.assertTrue(numbered, "no numbered class docstrings found")


if __name__ == "__main__":
    unittest.main()
