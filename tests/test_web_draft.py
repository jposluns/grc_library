#!/usr/bin/env python3
"""The /draft tree (PR 2b): the grclibrary.ai rebuild on the shared family
site template (baseline 1.4.1).

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
   build.
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
   counting what its type page lists; the root specifications open on
   GitHub under the one area label the type pages give them; every document
   page's Next and the Browse page lead to the index; the index and Browse
   prose about the list holds for the rendered rows.
10. The executive layer (design D items D1 and D3, section 4.1 branch 2):
   every narrative registry page renders at
   ``/draft/decisions/<subtype>/<slug>/`` on the baseline shell; each of the
   six ``/draft/decide/<subtype-plural>/`` indexes lists exactly the pages of
   its narrative type; each domain page's leadership section matches the
   registry join; every count these pages show equals the registry's; every
   page of the three types carries the layer's authority qualifier whole;
   and a narrative type with no subtype index fails the build.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
import shutil
import tempfile
import unittest
from html import unescape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# The draft CSP, copied from baseline 1.4.1 SPECIFICATION.md section 9
# (unchanged since 1.3.1), the shared policy for draft pages; build.py must
# carry it byte for byte.
SPEC_SECTION_9_CSP = (
    "default-src 'none'; script-src 'self' 'unsafe-inline'"
    " https://ajax.cloudflare.com https://static.cloudflareinsights.com;"
    " connect-src 'self' https://cloudflareinsights.com; style-src 'self';"
    " font-src 'self'; img-src 'self'; base-uri 'none'; form-action 'none';"
    " frame-ancestors 'none'"
)

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
        self.assertEqual(search.count("data-search="), len(domain_docs))
        # The rows are drawn from the non-root documents alone, so the prompt
        # counts that pool, names it, and never claims the whole library; it
        # calls the groupings domains, as Browse does (review round 2 NOTE).
        self.assertIn(
            f'<p class="meta" id="search-prompt">Search the {len(domain_docs)} '
            f"documents across the {len(domains)} domains by ", search)
        self.assertNotIn(f"Search all {len(domain_docs)}", search)
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

    # -- 5c. search is just a search (maintainer 2026-11-03 14:29Z: "there's
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
        are the rows and their domains, a field it states plainly is carried
        by every row, and a purpose only some rows state is qualified with the
        count of rows that do. Frameworks carry no count and are qualified in
        words (review round 2 WARN: "by framework for the 240 that map to one"
        counted a row whose taxonomy frameworks list holds only prose
        fragments), and the groupings are domains, as on Browse (review round
        2 NOTE: "areas" was a second name)."""
        search = self.draft_html["draft/search/index.html"]
        prompt = re.search(
            r'<p class="meta" id="search-prompt">([^<]*)</p>', search)
        self.assertIsNotNone(prompt)
        prompt = unescape(prompt.group(1))
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8")
        )
        by_href = {self.mod._doc_page_url("/draft", d["path"]): d
                   for d in full}
        hrefs = [href for _, href in self._search_rows()]
        docs = [by_href[href] for href in hrefs]
        scope = re.search(r"<ul[^>]* data-search-scope>(.*?)</ul>",
                          search, re.S).group(1)
        rows = re.findall(
            r'<li data-search="[^"]*"><a href="[^"]*">([^<]+)</a>'
            r'<span class="n">([^<,]+), ([^<]+)</span>', scope)
        self.assertEqual(len(rows), len(hrefs),
                         "every row shows a title, a type and a domain")
        domains = {domain for _, _, domain in rows}
        with_purpose = sum(1 for d in docs
                           if (d.get("purpose") or "").strip())
        head = re.match(
            r"Search the (\d+) (documents?) across the (\d+) (domains?) "
            r"by title, type, ", prompt)
        self.assertIsNotNone(head, prompt)
        self.assertEqual(int(head.group(1)), len(rows))
        self.assertEqual(int(head.group(3)), len(domains))
        self.assertIn(
            f'<div class="fig"><span class="num">{head.group(3)}</span>'
            '<span class="cap">domains</span></div>',
            self.draft_html["draft/browse/index.html"],
            "the prompt's domains are the ones Browse counts")
        self.assertNotRegex(prompt, r"\bareas?\b",
                            "Browse calls them domains")
        self.assertNotRegex(prompt, r"\ball\b",
                            "the rows are not the whole library")
        purpose = re.search(r"by purpose for the (\d+) that states? one",
                            prompt)
        counts = [len(rows), len(domains)]
        if with_purpose == len(rows):
            self.assertIsNone(purpose)
            self.assertRegex(prompt, r"\bdomain, (and )?purpose\b")
        else:
            self.assertIsNotNone(purpose, "purpose is qualified")
            self.assertEqual(int(purpose.group(1)), with_purpose)
            self.assertNotRegex(prompt, r"\bdomain, (and )?purpose\b")
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
        """Each draft document appears once, and its data-search text is the
        PR 2d haystack: title, type, area label and slug, full purpose, and
        framework names, lower-cased with whitespace collapsed."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8")
        )
        expected = {}
        for d in full:
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
                values = self.mod.draft_search_values(subset)
                self.assertEqual(values["SEARCH_PROMPT"], prompt)
                self.assertEqual(
                    values["SEARCH_ROWS"].count("<li data-search="),
                    len(subset))
        values = self.mod.draft_search_values(domain_docs)
        self.assertEqual(values["SEARCH_ROWS"].count("<li data-search="),
                         len(domain_docs))
        self.assertTrue(values["SEARCH_PROMPT"].startswith(
            f"Search the {len(domain_docs)} documents across the "))
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
        self.assertEqual(
            {href: hay for hay, href in self._index_rows()},
            {href: hay for hay, href in self._search_rows()},
            "an index row and its search page row carry the same text")

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
        """Each type chip's count equals the rows and the count its type
        page shows, and every type page has a chip."""
        type_chips = self._CHIP_RE.findall(self._index_block("By type"))
        type_pages = {rel for rel in self.draft_html
                      if rel.startswith("draft/types/")}
        self.assertEqual({_page_rel_for(href) for href, _, _ in type_chips},
                         type_pages, "one chip per type page")
        for href, label, n in type_chips:
            with self.subTest(type=label):
                page = self.draft_html[_page_rel_for(href)]
                scope = re.search(
                    r'<ul class="plan one described">(.*?)</ul>', page, re.S)
                self.assertIsNotNone(scope, "the type page has no list")
                self.assertEqual(
                    int(n), len(self._TYPE_ROW_RE.findall(scope.group(1))),
                    "the chip counts the rows its type page lists")
                self.assertIn(f"Documents, {n}</p>", page)

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
        filtered list)."""
        browse = self.draft_html["draft/browse/index.html"]
        main = browse.split('<main id="main-content">', 1)[1]
        self.assertIn('<a href="/draft/documents/">All Documents</a>', main,
                      "the Browse page body links the index by name")
        self.assertNotIn("/draft/documents/", _NAV_RE.search(browse).group(1),
                         "the top bar is unchanged in this PR")
        self.assertIn(
            "<p>To see every document in the library on one page, open "
            '<a href="/draft/documents/">All Documents</a>; its filter covers '
            "the documents across the domains.</p>", main)
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
        self.assertEqual(
            rendered, {f"draft/decide/{s}/index.html" for s in SUBTYPE_SLUGS},
            "exactly the six reconciled subtype index routes render")
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

    # -- 6. asset copy ------------------------------------------------------

    def test_asset_copy_matches_the_pinned_tree(self):
        import tomllib
        pin = tomllib.loads(
            (REPO_ROOT / ".baseline" / "pin.toml").read_text(encoding="utf-8")
        )
        prefix = ".web/baseline/"
        for key, digest in pin["files"].items():
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
        self.assertEqual(len(copied), len(pin["files"]),
                         "exactly the pinned files are copied")

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
                noun = "document" if len(docs) == 1 else "documents"
                self.assertIn(f'<p class="meta">{len(docs)} {noun}. ', page)
                self.assertIn(f"Documents, {len(docs)}</p>", page)
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
                rows = self._TYPE_ROW_RE.findall(page)
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
        section = re.search(
            r'<h2 id="types">By type</h2>\s*<div class="wide">'
            r'<ul class="plan three">(.*?)</ul>', browse, re.S)
        self.assertIsNotNone(section, "Browse has no By type list")
        hrefs = _HREF_RE.findall(section.group(1))
        self.assertEqual(
            hrefs,
            ["/draft/types/" + self.mod.type_slug(t) + "/"
             for t, _ in self.figures["types"]],
            "every By type entry links its own type page, never the search "
            "page or a Browse anchor")


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
        lines = ['version = "1.4.1"', "", "[files]"]
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


class DraftTemplateTypedCountTests(unittest.TestCase):
    """Round-2 fix 1: no draft template may type a count. Every number a page
    shows is computed at build time (owner decision), so a digit may appear in
    a template source only inside one of the listed exceptions."""

    # The exceptions, each a regex blanked from the source before the digit
    # scan; any digit that survives is a typed count and fails the test.
    EXCEPTIONS = (
        # A {{PLACEHOLDER}}: the computed values.
        r"\{\{[A-Z0-9_]+\}\}",
        # A URL in an href or src attribute.
        r'(?:href|src)="[^"]*"',
        # Structural id and class attribute values (anchor ids like d-1 and
        # the shared footer's slice-6 grid classes are positions, not counts).
        r'(?:id|class)="[^"]*"',
        # HTML heading tag names (h1, h2).
        r"</?h[1-6]\b",
        # The charset and viewport meta attribute values.
        r'(?:charset|content)="[^"]*"',
        # A version string: CC BY-SA 4.0, CC0 1.0, OFL 1.1, baseline 1.4.1.
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
        # The shared family footer's fixed site-list label: baseline 1.4.1
        # owns that wording, outside this site's copy.
        r'aria-label="The 6 project sites"',
    )

    def test_no_typed_count_in_any_draft_template(self):
        template_root = REPO_ROOT / ".web" / "templates-draft"
        sources = sorted(template_root.rglob("*.html"))
        self.assertTrue(sources, "no draft template sources found")
        for path in sources:
            text = path.read_text(encoding="utf-8")
            for pattern in self.EXCEPTIONS:
                text = re.sub(pattern, " ", text)
            match = re.search(r"\d+", text)
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
    comment carries its own number from the module docstring's list."""

    def test_section_comments_follow_the_module_docstring(self):
        items = re.findall(r"^(\d+)\. ", __doc__, re.M)
        source = Path(__file__).read_text(encoding="utf-8")
        sections = re.findall(r"^    # -- (\d+)\. ", source, re.M)
        self.assertTrue(sections, "no numbered section comments found")
        self.assertEqual(len(sections), len(set(sections)),
                         f"two sections share a number: {sections}")
        self.assertLessEqual(set(sections), set(items),
                             "a section number names no docstring item")


if __name__ == "__main__":
    unittest.main()
