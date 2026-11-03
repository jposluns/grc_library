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
        # The rows are drawn from the non-root documents alone, so the label
        # counts that pool, never the whole-library total.
        self.assertIn(f"All documents, {len(domain_docs)}</p>", search)

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

    def test_search_has_one_row_per_draft_document_page(self):
        doc_pages = {rel for rel in self.draft_html
                     if rel.startswith("draft/documents/")}
        self.assertTrue(doc_pages)
        self.assertEqual(
            len(self._search_rows()), len(doc_pages),
            "the search list carries one row per draft document page")

    def test_every_search_row_links_an_existing_draft_document_page(self):
        doc_pages = {rel for rel in self.draft_html
                     if rel.startswith("draft/documents/")}
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


if __name__ == "__main__":
    unittest.main()
