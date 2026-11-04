#!/usr/bin/env python3
"""The /draft tree (PR 2b): the grclibrary.ai rebuild on the shared family
site template (baseline 1.7.0).

What is locked here, each test failing without its feature:

1. Frozen root: the draft variant adds pages only under ``draft/`` and changes
   no other output byte, except the one sanctioned ``_headers`` appendix (the
   ``/draft/*`` block); the discovery files never mention the draft.
2. Page hygiene: every draft page is noindex with a self-canonical under
   /draft/, carries the baseline head order and the favicon and touch-icon
   links, resolves every internal reference inside the draft tree or its
   copied assets, and marks every external link as opening in a new tab.
3. The top bar is exactly Browse, All Documents, Decisions, Crosswalk,
   Search, GitHub (GitHub last; maintainer decision 2026-11-03 23:27Z), each
   link opening its own rendered page, never an anchor; each page marks the
   link of the section its route belongs to, and pages outside every section
   mark none; the landing page's About line carries Disclosure, Licence,
   Privacy, Security; no other draft page links the Disclosure or Licence
   pages, and the approved value paragraph keeps its words with no link.
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
   data-search text, wired the way search.js expects; type and area are
   search.js facet groups (item 27), each type chip counting the
   corpus-area rows its type page shows; the root specifications open on
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
   one side rail only (the left rail from item 29), the reverse matrix
   parser refuses interrupted
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
   corpus list's corpus-area rows; the Browse and govern sentences about All Documents say
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
27. Search results mode and All Documents facets (site f1, baseline 1.5.1
   spec 7.29, unchanged at 1.6.0; maintainer 2026-11-03: search is just a
   search, and All Documents carries the filters, type among them): the
   search scope runs in results mode with a generated status prompt, every
   row's first link is the title search.js ranks by, and no sentence on the
   page says the rows are listed below; every document page's framework chip links the search
   page's ?q= address for its name, which finds that document; All
   Documents carries a type and an area chip group whose counts are each
   chip's documents in the whole list, whose chips link their own facet
   addresses, and whose filter paragraph holds for every chip and row; each
   type page links its type's facet address with a count true for its rows;
   and the disclosure's data-handling claim names every key search.js
   writes. Each check replays search.js 1.5.1 (unchanged at 1.6.0) on the
   rendered rows. No test replays 1.7.0's count(); the rows it shows in
   each state, and the count it gives a chip that is not chosen (the rows
   holding that chip's value, every other group's choice and the words
   typed), were read from its source to match what the 1.5.1 replay gives,
   and the pinned 1.7.0 search.js digest (item 39) locks that file, so a
   changed search.js fails there.
28. Site f1 round 2, each sentence replayed on the rendered pages: the All
   Documents filter paragraph says a chip's count is its documents in the
   whole list and the status line gives how many show, true in every
   combined state (every type by every area, and each type page's filter
   address), where a chip can show fewer than its count; the search page
   says a ?q= address with words shows results on load; the search status
   prompt and results sentence name the fields a row matches on, never the
   whole document; a type page that lists one All Documents row drops the
   narrowing clause; and Browse calls All Documents every corpus document,
   which the adopter documents it leaves out are not.
29. Crosswalk left rail and matrix presets (site f2, baseline 1.5.1 sections
   7.30 to 7.32, unchanged at 1.6.0): the crosswalk page and its preset views are left-rail pages
   with no right rail (the instrument pages keep the logo-only rail); the
   side list names every instrument under its group, the Also in the corpus
   instruments included; the matrix.js presets are All plus the topic views
   (item 30), each a link to its static view; the row-header column
   carries no data-col and sits outside every preset; the table is the
   page's one matrix in a bounded scroll box and shows every column without
   script; the sentences about the table and the views hold for every column
   and view they cover; the generator refuses groups and instruments that
   disagree; and the disclosure names the view the matrix script writes into
   the page address.
30. Crosswalk topic views (site f2 round 2, maintainer decision 2026-11-03
   18:53Z: the views stay by topic): the presets equal design C 3.7's topic
   views, pinned as literals; each renders at /draft/crosswalk/view/<topic>/
   with its topic's columns and, where it has any, its related instrument
   pages, and no other view route renders; the rail's Views list is All plus
   the topics; the Views sentence's clauses on topics spanning groups,
   columns shared between topics, and related pages hold on the rendered
   pages; and the generator refuses a topic with no column, an unknown or
   page-only instrument as a column, an unknown related instrument, and a
   column in no topic.
31. Crosswalk round 3 (site f2): the Views sentence tells All, which opens
   the full table, from the topic views; the sentences about the side list
   say the group lists, not the Views list, hold the instruments; the
   disclosure's ?view= clause matches what matrix.js writes and removes;
   headers and cells take the spec 7.30 markup (name over organization tag,
   single-word identifiers in code type, a count link with a visually hidden
   noun) and no phrase-length label sits in a matrix cell; a view's column
   split counts its own columns, and the crosswalk page scopes every count to
   the full table while each caption count equals the rendered columns; a
   static view's columns follow the full table's order; a bad topic fails
   the build, not the import; the generator refuses a duplicate topic slug,
   the slug all, a column repeated in a topic, and a column header with no
   organization tag; and a view's lead says All opens every instrument
   column.
32. Crosswalk round 4 (site f2): the table sentences name the columns whose
   cells show a code, the columns that record phrase-length labels only,
   and the columns with no mapping, each checked against every rendered
   column of every table page; a header's name is its display without the
   leading organization; and an empty cell holds only a visually hidden
   "no documents" while "and more" is visually hidden, so a cell shows its
   codes and count link alone.
33. Batch 3 integration (site f1 and f2 onto batch 2): a type page's All
   Documents sentence names the area chips only where its rows span areas
   and the text filter alone where they sit in one, and counts its rows
   against the page's whole total, adopter documents included; the
   crosswalk opening sentence says what every column is, true for a column
   no domain maps; a one-column group names its column directly; a space
   separates the hidden "and more" from the count; the disclosure
   names every script's address and storage behaviour together; and the
   docstring-number guard reads a lead naming several items.
34. Batch 3 round 2: on a type page with adopter documents, the All
   Documents sentence names its scope as a part of this page's documents,
   never "these" just after the adopter block; the AICPA TSC caveat says
   what the reader sees, an empty cell for the matrix's N/A, renders only
   on a page whose table has that column, and holds for every such cell;
   and a plain space separates the codes from the count link in every
   cell, capped or not.
35. Batch 3 round 3: the AICPA TSC caveat names the documents the matrix
   lists for a domain, checked against the matrix rows and each domain's
   document count; the AICPA TSC instrument page carries its own caveat,
   its N/A rows counted from the matrix, and no other page carries it; the
   disclosure page carries the owner's "Your browser" paragraph before the
   Security label, and every sentence on it about cookies or storage
   agrees with that paragraph and with scheme.js; and the pin, NOTICE.md
   and the version comments name the pinned baseline version (then 1.6.1,
   whose pinned files were the 1.6.0 files byte for byte; item 38 moves
   them on).
36. Batch 3 round 5: view pages say the AICPA TSC column is being populated
   on the same parsed status as the AICPA TSC instrument page, so they agree
   with the matrix sentence present and removed; and a one-row column with
   no N/A gets its single-row form.
37. Batch 3 round 6: the AICPA TSC status is read from the compliance
   matrix's reading-guide paragraph alone, the first paragraph after its
   framework column key table, which must be exactly one of two pinned
   forms, with the status sentence or with exactly that sentence removed;
   any other text in that paragraph, or the paragraph or key table missing,
   fails the build, and wording elsewhere in the matrix is not read, so an
   unrelated "populated" there passes; and no compliance matrix column can
   have 0 rows.
38. Batch 3 follow-up: the compliance matrix's "How to use this matrix"
   section is pinned whole, from its heading to the --- that ends it, in
   its two forms, so the status sentence moved or reworded anywhere in that
   section (the intro paragraph, a paragraph of its own above the key list
   or after the reading-guide paragraph, a key table row, old or new) fails
   the build; the exact status sentence anywhere else in the matrix (the
   document header, after the section's ---, Notes, the end of the file)
   fails the build too, while a reworded status outside the section is not
   refused, so the build passes without the caveat; and the 404 page lead
   names each top bar link, in the bar's order, by its exact label, or,
   for a label listed in _404_LEAD_FORMS, by that fixed form only.
39. Baseline 1.7.0 (CHANGELOG 1.7.0; spec sections 6.1, 7.24 and 7.29): the
   pin names 1.7.0, and the 5 files 1.7.0 changes (baseline.css,
   palettes.css, search.js, matrix.js and the palette gate) carry the
   release's digests in the pin, in the repository and, for the served
   ones, in the draft copy; the served palettes.css gives grclibrary the 13
   matrix tokens in all 4 of its light and dark forms, and the build's
   palette gate fails on a palette without them or with a heat step text
   cannot be read on; the landing page's About line has exactly one
   ordinary space after each dot span and none before it; and All Documents
   has two facet groups again, type and area (?type=, ?area=), each opted
   in to unavailable chips (data-filter-empty="disable") with the served
   counts kept (no data-filter-count="live"), so the filter paragraph's
   unavailable-chip sentence holds in every combined state, replayed on
   the rendered rows.
"""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import re
import shutil
import tempfile
import unittest
import urllib.parse
from collections import Counter
from html import unescape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# The draft CSP, copied from baseline 1.7.0 SPECIFICATION.md section 9
# (unchanged since 1.3.1), the shared policy for draft pages; build.py must
# carry it byte for byte.
SPEC_SECTION_9_CSP = (
    "default-src 'none'; script-src 'self' 'unsafe-inline'"
    " https://ajax.cloudflare.com https://static.cloudflareinsights.com;"
    " connect-src 'self' https://cloudflareinsights.com; style-src 'self';"
    " font-src 'self'; img-src 'self'; base-uri 'none'; form-action 'none';"
    " frame-ancestors 'none'"
)

# Baseline 1.7.0 SPECIFICATION.md section 7.33, in the full form every 1.7.0
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
# The baseline 1.7.0 SHA256SUMS digests of the files 1.7.0 changes
# (CHANGELOG 1.7.0: baseline.css, palettes.css, search.js, matrix.js and
# tools/check_palette.py), and of scheme.js, which 1.6.0 added and 1.7.0
# leaves unchanged; every other pinned file is unchanged from 1.6.1.
RELEASE_1_7_0_DIGESTS = {
    ".web/baseline/scheme.js":
        "39d035d986f53c987cbe92516b9a5fd499af5c7fcdda701ea896c63c45ef1634",
    ".web/baseline/baseline.css":
        "8a902e09bc770744e4f1a15066a0c5ef33095d829a5dc59486a502c567dac777",
    ".web/baseline/palettes.css":
        "cf4bed49e0c3c16fcc8272acbf8263753e2f392db6dcdac96313540b0da220f2",
    ".web/baseline/search.js":
        "ff39a504d988c51510be466b2ad7e5eb2edf8299eead35b4070a20ac768359bb",
    ".web/baseline/matrix.js":
        "f8b2d53a4bd5ad25bae8974668c3e0b71f32298bc3b2f96913c2455a0739d87e",
    ".baseline/check_palette.py":
        "cae71e9a43e87c5687bc50dc75784e83b3a5b643a4e9a07298294b9d270971a4",
}
# Section 6.1: grclibrary's dark --bg in 1.6.0 (#1f1718 in 1.5.1), unchanged
# in 1.7.0, which adds tokens and changes no existing value.
RELEASED_DARK_BG = "#110814"
_DARK_BLOCKS = (
    '.site-grclibrary:not([data-scheme="light"]) {',
    '[data-scheme="dark"].site-grclibrary {',
)
# The light forms: the bare site class (the first rule in the file that
# opens with it) and the forced light scheme.
_LIGHT_BLOCKS = (
    '\n.site-grclibrary {',
    '[data-scheme="light"].site-grclibrary {',
)
# Section 6.1 from 1.7.0: the 13 matrix tokens every site and scheme carries,
# which the palette gate checks.
MATRIX_TOKENS = (
    ["row-tint", "row-hover"] + [f"heat-{i}" for i in range(5)]
    + [f"grp-{i}" for i in range(1, 7)]
)


def _dark_token(css, token, openers=_DARK_BLOCKS):
    """The value of ``--<token>`` in each of grclibrary's 2 dark blocks (or
    the named blocks), None where a block sets it other than once."""
    values = []
    for opener in openers:
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


def _drop_token(css, token, openers=_DARK_BLOCKS + _LIGHT_BLOCKS):
    """``css`` with grclibrary's ``--<token>`` removed from the named
    blocks (by default all 4 of its light and dark forms)."""
    for opener in openers:
        start = css.index(opener) + len(opener)
        end = css.index("}", start)
        block, count = re.subn(r"\n\s*--" + re.escape(token) + r":[^;]+;",
                               "", css[start:end])
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
    """Map a /draft/... URL path to its dist-relative output path (a query
    string, such as a search or facet address, names no other page)."""
    path = url_path.split("#", 1)[0].split("?", 1)[0]
    rel = path.lstrip("/")
    if rel.endswith("/"):
        return rel + "index.html"
    return rel


def _address_params(href):
    """The decoded query parameters of a rendered href, as URLSearchParams
    reads them ('+' is a space), one value per key."""
    query = urllib.parse.urlsplit(unescape(href)).query
    pairs = urllib.parse.parse_qsl(query, keep_blank_values=True)
    params = dict(pairs)
    assert len(params) == len(pairs), f"{href}: a repeated parameter"
    return params


def _replay_search_js(rows, query="", active=None, results=False,
                      rank=False):
    """The rows baseline 1.5.1 search.js shows, in display order (spec 7.29,
    its run()): a row shows when every whitespace-split term is a substring
    of its lowercased data-search text and every active facet value is among
    its group tokens; in results mode nothing shows with no query and no
    active facet; with ranking, rows whose title holds every term come
    first, page order kept within each group. Each row is a dict with
    ``hay``, ``title``, ``href`` and ``tokens`` (group to token list)."""
    terms = query.lower().split()
    active = {g: v for g, v in (active or {}).items() if v}
    if results and not terms and not active:
        return []
    first, rest = [], []
    for row in rows:
        if not all(t in row["hay"] for t in terms):
            continue
        if not all(v in row["tokens"].get(g, []) for g, v in active.items()):
            continue
        titled = rank and terms and all(t in row["title"] for t in terms)
        (first if titled else rest).append(row)
    return first + rest


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
        table carries ``data-matrix``: the crosswalk page from site f2
        (section 29 below), and MatrixScriptFixtureTests proves the rule on
        fixtures too."""
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

    # The maintainer's bar (2026-11-03 23:27Z), in order, before GitHub.
    _TOP_BAR = [
        ("Browse", "/draft/browse/"),
        ("All Documents", "/draft/documents/"),
        ("Decisions", "/draft/decide/"),
        ("Crosswalk", "/draft/crosswalk/"),
        ("Search", "/draft/search/"),
    ]

    def test_top_bar_is_six_links_each_to_its_own_page(self):
        """Maintainer decision 2026-11-03 23:27Z: every draft page carries
        exactly Browse, All Documents, Decisions, Crosswalk, Search, then the
        unchanged GitHub link; no link is an in-page anchor, no two open the
        same page, and every internal target renders."""
        for rel, html in self.draft_html.items():
            nav = _NAV_RE.search(html)
            self.assertIsNotNone(nav, rel)
            labels = [t.strip() for t in _NAV_LINK_RE.findall(nav.group(1))]
            hrefs = _HREF_RE.findall(nav.group(1))
            self.assertEqual(
                list(zip(labels, hrefs)),
                self._TOP_BAR + [
                    ("GitHub", "https://github.com/jposluns/grc_library")],
                f"{rel}: the bar must be Browse, All Documents, Decisions, "
                "Crosswalk, Search, then GitHub last")
            self.assertNotIn("Disclosure", nav.group(1), rel)
            self.assertNotIn("Licence", nav.group(1), rel)
            for href in hrefs:
                self.assertNotIn("#", href, f"{rel}: {href} is an anchor")
            internal = [_page_rel_for(h) for h in hrefs
                        if h.startswith("/")]
            self.assertEqual(len(set(internal)), len(internal),
                             f"{rel}: two bar links open the same page")
        for _, href in self._TOP_BAR:
            self.assertIn(_page_rel_for(href), self.draft_html,
                          f"{href}: the bar's target page is rendered")

    def _top_bar_section(self, rel):
        """The bar link a draft page belongs under, from its route alone: the
        need, domain and type pages under Browse, every document page under
        All Documents, the decide hub, concern, subtype index and
        reading-room pages under Decisions, the crosswalk views and
        instrument pages under Crosswalk; None for a page in no section."""
        route = rel[len("draft/"):]
        first = route.split("/", 1)[0]
        domains = {dp["domain"] for dp in self.figures["domain_pages"]}
        if first in {"browse", "govern", "comply", "solutions", "policies",
                     "types"} | domains:
            return "/draft/browse/"
        if first in ("decide", "decisions"):
            return "/draft/decide/"
        if first in ("documents", "crosswalk", "search"):
            return f"/draft/{first}/"
        self.assertIn(route, ("index.html", "404.html",
                              "disclosure/index.html", "license/index.html"),
                      f"{rel}: a page the section map does not place")
        return None

    def test_top_bar_marks_the_section_of_every_page(self):
        """Each page marks exactly the bar link of its section (the bar
        page itself and the pages under it), and the landing, disclosure,
        licence and 404 pages mark none."""
        sections = Counter()
        for rel, html in self.draft_html.items():
            nav = _NAV_RE.search(html).group(1)
            current = re.findall(r'<a href="([^"]*)" aria-current="page">',
                                 nav)
            own = self._top_bar_section(rel)
            self.assertEqual(current, [own] if own else [], rel)
            self.assertEqual(nav.count("aria-current"), len(current), rel)
            sections[own] += 1
        self.assertEqual(set(sections), {h for _, h in self._TOP_BAR} | {None},
                         "every bar section, and no section, has pages")

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

    def test_about_line_has_one_space_after_each_dot_and_none_before(self):
        """Spec 7.24 from 1.7.0 (required on every site): one ordinary space
        after each dot span and none before it, so the line breaks only
        after a dot and a dot never starts a line. Until 1.6.1 the links and
        dots touched, so the line could not break and overflowed at 300 to
        360 px. Each dot is read off the rendered landing page with what
        touches it on either side."""
        landing = self.draft_html["draft/index.html"]
        about = re.search(r'<p class="about">(.*?)</p>', landing, re.S)
        self.assertIsNotNone(about, "the About line (spec 7.24) is required")
        dot = '<span class="dot" aria-hidden="true">&middot;</span>'
        parts = about.group(1).split(dot)
        self.assertEqual(len(parts), 4, "3 dots between the 4 links")
        for before, after in zip(parts, parts[1:]):
            with self.subTest(after=after[:40]):
                self.assertTrue(before.endswith("</a>"),
                                "no space or other text before the dot")
                self.assertTrue(after.startswith(" <a "),
                                "one ordinary space after the dot")
                self.assertFalse(after.startswith("  "))
        self.assertFalse(parts[0][:1].isspace())
        self.assertTrue(parts[-1].endswith("</a>"))

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

    # Entry 6's claim, sentence by sentence, as the one paragraph held it
    # before the maintainer's 2026-11-04 split; the split moves sentence
    # boundaries into separate paragraphs and changes no wording. One
    # sentence was later reworded for baseline 1.7.0 (round-2 NOTE): the
    # search script sentence says its "never" covers only what the script
    # writes.
    _D6_CLAIM_SENTENCES = (
        "This is a static site.",
        "Its own scripts are same-origin files that make no network requests "
        "and use no cookies.",
        "The light and dark switch is the one script that uses browser "
        "storage: when the reader presses the switch, it saves the chosen "
        "scheme, the word light or dark, in the browser's local storage "
        'under the key "scheme", so later pages open in that scheme.',
        "It stores nothing else, and nothing until the switch is pressed.",
        "The search form filters a list already on the page and does not "
        "submit the query.",
        "As the reader types, the search script writes the query into the "
        "page address (?q=), and on All Documents it writes the type and "
        "area the reader picks there too (?type=, ?area=), so the query and "
        "those choices can appear in the browser history; the script itself "
        "never writes the type or area of a chip marked unavailable, though "
        "a chip's link opened in a new tab or window carries it, as any link "
        "does.",
        "When the reader chooses a crosswalk topic view, the matrix script "
        "writes the view's short identifier (for example, privacy) into the "
        "page address (?view=) the same way, and removes it from the address "
        "when the reader chooses All.",
        "This site's host, Cloudflare, receives that address, query, choices "
        "and view included, when the reader reloads the page and with later "
        "requests from the page to this site.",
        "Scripts the page runs, including the Cloudflare Web Analytics "
        "beacon, can read the page address.",
    )

    def _disclosure_claim_parts(self, page):
        """Entry 6's claim paragraphs in order, whitespace collapsed: the
        "Claim:" paragraph (lead dropped) and the unlabelled paragraphs that
        follow it, up to the Limitation paragraph."""
        block = re.search(
            r'<h2 id="d-6">[^<]*</h2>\s*<p><strong>Claim:</strong>(.*?)'
            r'<p><strong>Limitation:</strong>', page, re.S)
        self.assertIsNotNone(block, "Entry 6 carries a claim, then a "
                             "limitation")
        body = "<p>" + block.group(1)
        self.assertRegex(body, r"(?s)\A(?:<p>(?:(?!<p\b|</p>).)*</p>\s*)+\Z",
                         "only plain paragraphs sit between the claim's lead "
                         "and the limitation")
        return [" ".join(p.split())
                for p in re.findall(r"<p>(.*?)</p>", body, re.S)]

    def test_disclosure_data_handling_claim_keeps_every_sentence(self):
        """Maintainer 2026-11-04 03:07Z: Entry 6's claim was one paragraph of
        about 1,270 characters, hard to read, so it is split into short
        paragraphs by subject. The split adds, drops and rewords nothing,
        and one sentence, the search script's, was later reworded for
        baseline 1.7.0: the claim's paragraphs, read in order and split at
        sentence ends, are the old claim's sentences with that one reworded,
        so each paragraph holds whole sentences, and each sentence appears
        on the rendered page exactly once."""
        page = self.draft_html["draft/disclosure/index.html"]
        parts = self._disclosure_claim_parts(page)
        # Four paragraphs by subject, each opening on its own sentence.
        self.assertEqual(len(parts), 4, "the claim is four paragraphs")
        for part, first in zip(parts, [self._D6_CLAIM_SENTENCES[i]
                                       for i in (0, 2, 4, 7)]):
            self.assertTrue(part.startswith(first), first)
        self.assertEqual(
            [s for p in parts for s in re.split(r"(?<=\.)\s+(?=[A-Z])", p)],
            list(self._D6_CLAIM_SENTENCES))
        text = unescape(" ".join(re.sub(r"<[^>]+>", " ", page).split()))
        for sentence in self._D6_CLAIM_SENTENCES:
            self.assertEqual(text.count(sentence), 1, sentence)

    def test_disclosure_data_handling_claim_matches_the_scripts(self):
        """Round-1 NOTE (a published privacy statement): from baseline 1.5.0
        search.js writes the query into the page address (spec 7.29), so the
        Entry 6 claim says so, and each part of the claim is checked against
        the rendered pages and the scripts they load."""
        page = self.draft_html["draft/disclosure/index.html"]
        # The claim runs over several paragraphs (maintainer 2026-11-04
        # split); joined, they read as the one paragraph did.
        claim = " ".join(self._disclosure_claim_parts(page))
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
            "the query into the page address (?q=), and on All Documents it "
            "writes the type and area the reader picks there too (?type=, "
            "?area=), so the query and those choices can appear in the "
            "browser history; the script itself never writes the type or "
            "area of a chip marked unavailable, though a chip's link opened "
            "in a new tab or window carries it, as any link does. When the "
            "reader chooses a crosswalk topic "
            "view, the matrix script writes the view's short identifier (for "
            "example, privacy) into the page address (?view=) the same way, "
            "and removes it from the address when the reader chooses All. "
            "This site's host, Cloudflare, receives that address, query, "
            "choices and view included, when the reader reloads the page and "
            "with later requests from the page to this site. Scripts the page "
            "runs, including the Cloudflare Web Analytics beacon, can read the "
            "page address.", claim)
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
        # "the search script writes the query into the page address (?q=),
        # and on All Documents ... the type and area (?type=, ?area=)" and
        # the matrix script's ?view= clause (checked against matrix.js in
        # section 31): they are the only loaded scripts that write the
        # address; search.js writes ?q= and one key per facet group, the
        # only facet groups on the draft being All Documents' type and area,
        # and matrix.js writes ?view= and loads on the crosswalk page alone
        # (site f2), so "when the reader chooses a crosswalk topic view"
        # covers it.
        self.assertEqual(
            sorted(n for n, js in sources.items() if "replaceState" in js),
            ["matrix.js", "search.js"],
            "exactly the search and matrix scripts write the page address")
        self.assertIn('p.set("q", input.value)', sources["search.js"])
        self.assertIn("p.set(g.name, g.value)", sources["search.js"])
        groups = {
            rel: re.findall(r'\sdata-filter-group="([^"]*)"', html)
            for rel, html in self.draft_html.items()
            if "data-filter-group" in html
        }
        self.assertEqual(groups,
                         {"draft/documents/index.html": ["type", "area"]},
                         "the claim names every facet key a page writes")
        # "the script itself never writes the type or area of a chip marked
        # unavailable": search.js 1.7.0 refuses such a chip and returns
        # before the click handler writes the address.
        click = sources["search.js"][
            sources["search.js"].index('c.addEventListener("click"'):]
        self.assertLess(click.index('=== "true") {'),
                        click.index("write();"))
        # matrix.js 1.7.0 writes { view: id } for a topic preset and deletes
        # view for All; ?cols= only where column toggles exist, and the
        # crosswalk has none (section 31 reads the exact call).
        self.assertIn('{ view: k.length && id ? id : "" }',
                      sources["matrix.js"])
        self.assertNotIn("data-col-toggles",
                         self.draft_html["draft/crosswalk/index.html"])
        self.assertEqual(
            sorted(rel for rel, html in self.draft_html.items()
                   if "/assets/baseline/matrix.js" in html),
            ["draft/crosswalk/index.html"],
            "the matrix script loads on the crosswalk page alone")
        # Batch 3 integration: the claim names every script's address and
        # storage behaviour together, so a script that writes the address
        # or keeps storage and goes unnamed fails here.
        named = {"scheme.js": 'under the key "scheme"',
                 "search.js": "(?q=)", "matrix.js": "(?view=)"}
        self.assertEqual(
            sorted(n for n, js in sources.items()
                   if "replaceState" in js or "localStorage" in js),
            sorted(named), "the scripts with address or storage behaviour")
        for name, phrase in sorted(named.items()):
            self.assertIn(phrase, claim, f"the claim names what {name} does")
        keys = ", ".join(f"?{g}=" for g in groups["draft/documents/index.html"])
        self.assertIn(f"({keys})", claim,
                      "the claim names every facet key search.js writes")
        # "filters a list already on the page and does not submit the query"
        search_pages = [rel for rel, html in self.draft_html.items()
                        if "/assets/baseline/search.js" in html]
        self.assertTrue(search_pages, "a draft page carries the search form")
        for rel in search_pages:
            html = self.draft_html[rel]
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
            f"documents, the {len(domain_docs)} corpus "
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
            r"Search the (\d+) documents, the (\d+) corpus "
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
            "Search the 2 documents, the 1 corpus document "
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
            f"Search the {len(domain_docs) + len(adopter)} documents, the "
            f"{len(domain_docs)} corpus documents across the "))
        self.assertEqual(
            values["SEARCH_STATUS_PROMPT"],
            f"Type one or more words to search the "
            f"{len(domain_docs) + len(adopter)} documents; "
            f"{self.SEARCH_MATCH_FIELDS}.")
        template = (REPO_ROOT / ".web" / "templates-draft"
                    / "search.html").read_text(encoding="utf-8")
        self.assertIn(">{{SEARCH_PROMPT}}</p>", template,
                      "the prompt is the generated value, never typed copy")
        self.assertIn('data-search-prompt="{{SEARCH_STATUS_PROMPT}}"',
                      template, "the status prompt is generated too")

    # -- 5f. results mode (baseline 1.5.1 spec 7.29; maintainer 2026-11-03:
    # search is just a search) -----------------------------------------------

    _SEARCH_TITLED_ROW_RE = re.compile(
        r'<li data-search="([^"]*)"><a href="([^"]*)">([^<]*)</a>')
    # The search page's sentence on how results mode behaves, compared whole;
    # each claim in it is checked on the rendered page.
    SEARCH_RESULTS_PROSE = (
        "<p>With script, the results stay empty until you type, or open a "
        "search address with words in ?q=; then a document shows when every "
        "word is in its title, type, area, or, where it has them, its "
        "purpose or framework names, and those whose title holds every word "
        "come first. The page address keeps your words (?q=), so a search "
        "can be linked. Without script, the whole list stays below.</p>"
    )
    # What a search matches, as the status prompt and the results sentence
    # both say it: the fields of a row's data-search text, not the document's
    # full text (round-1 NOTE).
    SEARCH_MATCH_FIELDS = (
        "a document shows when every word is in its title, type, area, or, "
        "where it has them, its purpose or framework names"
    )

    def _search_replay_rows(self):
        """The search page's rows as search.js reads them, its title being
        the first link's text (the page sets no data-title)."""
        search = self.draft_html["draft/search/index.html"]
        scope = re.search(r"<ul[^>]* data-search-scope>(.*?)</ul>", search,
                          re.S).group(1)
        return [
            {"hay": unescape(hay).lower(), "href": href,
             "title": unescape(title).lower(), "tokens": {}}
            for hay, href, title in self._SEARCH_TITLED_ROW_RE.findall(scope)
        ]

    def test_search_scope_runs_in_results_mode_with_a_generated_prompt(self):
        """The search list is search.js's results mode (data-search-mode=
        "results" on the scope), so an empty query shows no row and the
        status shows the scope's data-search-prompt, generated from the rows
        and saying how to search: its count is the rows, and its "a document
        shows when every word is in" its fields is replayed on them. The
        status line stays empty in the markup for search.js to fill."""
        search = self.draft_html["draft/search/index.html"]
        scopes = re.findall(r"<ul\b([^>]*)\bdata-search-scope>", search)
        self.assertEqual(len(scopes), 1)
        attrs = dict(re.findall(r'\s(data-search-[a-z]+)="([^"]*)"',
                                scopes[0]))
        self.assertEqual(attrs.get("data-search-mode"), "results",
                         "the scope runs in results mode")
        rows = self._search_replay_rows()
        self.assertEqual(len(rows), len(self._search_rows()))
        self.assertEqual(
            unescape(attrs.get("data-search-prompt", "")),
            f"Type one or more words to search the {len(rows)} documents; "
            f"{self.SEARCH_MATCH_FIELDS}.")
        self.assertIn("data-search-status></p></form>", search)
        self.assertEqual(_replay_search_js(rows, "", results=True), [],
                         "an empty query shows no row")
        for query in ("retention", "incident response"):
            with self.subTest(query=query):
                shown = _replay_search_js(rows, query, results=True,
                                          rank=True)
                self.assertTrue(shown)
                self.assertLess(len(shown), len(rows))
                for row in shown:
                    for word in query.split():
                        self.assertIn(word, row["hay"], row["href"])

    def test_search_rows_rank_by_the_title_search_js_reads(self):
        """Title ranking, on in results mode, reads a row's data-title or
        else its first link's text, so every row's first link is exactly
        its document's title and no row sets data-title. Replayed for one of
        the page's own example searches: the rows whose title holds every
        word lead, and rows matching only elsewhere follow."""
        search = self.draft_html["draft/search/index.html"]
        self.assertNotIn("data-title", search)
        by_href = {self.mod._doc_page_url("/draft", d["path"]): d
                   for d in self._full_taxonomy()
                   + self.mod.parse_adopter_docs()}
        rows = self._search_replay_rows()
        for row in rows:
            doc = by_href[row["href"]]
            self.assertEqual(row["title"],
                             doc.get("title", doc["path"]).lower(), row["href"])
        shown = _replay_search_js(rows, "incident response", results=True,
                                  rank=True)
        titled = [r for r in shown
                  if "incident" in r["title"] and "response" in r["title"]]
        self.assertTrue(titled)
        self.assertGreater(len(shown), len(titled))
        self.assertEqual(shown[:len(titled)], titled,
                         "titles holding every word come first")

    def test_search_page_prose_is_true_in_results_mode(self):
        """The page prose rule in results mode: no sentence on the page says
        the rows are listed below (with script none shows before a query);
        the behaviour sentence is read off the rendered page and each claim
        checked there: results mode and its title ranking on the scope, the
        ?q= write-back in the loaded search.js, and the whole list in the
        markup with no row hidden, so without script it stays below."""
        search = self.draft_html["draft/search/index.html"]
        main = search.split('<main id="main-content">', 1)[1]
        for text in self._label_texts(main):
            self.assertNotIn("listed below", text)
        self.assertIn(self.SEARCH_RESULTS_PROSE, main)
        self.assertRegex(main, r'<ul\b[^>]*\sdata-search-mode="results"')
        js = self.draft_all["draft/assets/baseline/search.js"].decode("utf-8")
        self.assertIn('p.set("q", input.value)', js)
        self.assertIn('params.get("q")', js)
        self.assertIn('var rank = results ||', js,
                      "title ranking is on in results mode")
        scope = re.search(r"<ul[^>]* data-search-scope>(.*?)</ul>", search,
                          re.S).group(1)
        self.assertNotRegex(scope, r"<li\b[^>]*\shidden\b")
        self.assertEqual(len(self._search_replay_rows()),
                         len(re.findall(r"<li\b", scope)))
        self.assertLess(main.find(self.SEARCH_RESULTS_PROSE),
                        main.find("data-search-scope"),
                        "the list the sentence calls below is below it")

    def test_search_address_with_words_shows_results_on_load(self):
        """Round-1 WARN: "the results stay empty until you type" was false
        for a /draft/search/?q=<words> address, which the framework chips
        open. The sentence now names that address, and each part is checked:
        search.js reads ?q= into the input before its first run(), so every
        rendered chip address (replayed with its words) shows results on
        load, while an address with no words (?q=) stays empty."""
        search = self.draft_html["draft/search/index.html"]
        self.assertIn(self.SEARCH_RESULTS_PROSE, search)
        js = self.draft_all["draft/assets/baseline/search.js"].decode("utf-8")
        load = js.find('if (input && params.has("q")) '
                       '{ input.value = params.get("q"); }')
        self.assertGreaterEqual(load, 0, "search.js reads ?q= on load")
        self.assertLess(load, js.rfind("  run();\n})();"),
                        "the first run() comes after the ?q= read")
        rows = self._search_replay_rows()
        queries = set()
        for rel in self._doc_pages():
            section = self._DOC_FW_RE.search(self.draft_html[rel])
            if section:
                queries.update(
                    _address_params(href)["q"]
                    for href, _ in self._FW_CHIP_RE.findall(section.group(1)))
        self.assertTrue(queries, "some page opens a search address")
        for query in sorted(queries):
            with self.subTest(q=query):
                self.assertTrue(query.split(), "the address carries words")
                self.assertTrue(
                    _replay_search_js(rows, query, results=True, rank=True),
                    "the address shows results on load")
        self.assertEqual(_replay_search_js(rows, "", results=True), [],
                         "an address with no words stays empty")

    def test_search_prose_names_only_the_fields_a_row_matches(self):
        """Round-1 NOTE: "a document shows when it holds every word" claimed
        the whole document, but a row matches on its data-search text alone.
        The status prompt and the results sentence each name those fields
        (SEARCH_MATCH_FIELDS), qualifying purpose and frameworks "where it
        has them"; every row's text is exactly those fields (rebuilt here
        from the taxonomy and the adopter metadata), and some row's owner, a
        field the document holds, has a word its row cannot match, so the
        unscoped wording was false."""
        search = self.draft_html["draft/search/index.html"]
        prompt = unescape(re.search(r'\sdata-search-prompt="([^"]*)"',
                                    search).group(1))
        self.assertIn(self.SEARCH_MATCH_FIELDS, prompt)
        self.assertIn(self.SEARCH_MATCH_FIELDS, self.SEARCH_RESULTS_PROSE)
        self.assertIn(self.SEARCH_RESULTS_PROSE, search)
        for text in (prompt, self.SEARCH_RESULTS_PROSE):
            self.assertNotIn("holds every word.", text)
        by_href = {self.mod._doc_page_url("/draft", d["path"]): d
                   for d in self._full_taxonomy()
                   + self.mod.parse_adopter_docs()}
        rows = self._search_replay_rows()
        unmatched_owner = 0
        for row in rows:
            d = by_href[row["href"]]
            fields = " ".join(" ".join(
                [d.get("title", ""), d.get("type", ""),
                 self.mod.draft_domain_label(d.get("domain", "")),
                 d.get("domain", ""), d.get("purpose", "") or ""]
                + d.get("frameworks", [])).lower().split())
            self.assertEqual(row["hay"], fields, row["href"])
            if any(w not in row["hay"]
                   for w in (d.get("owner") or "").lower().split()):
                unmatched_owner += 1
        self.assertTrue(unmatched_owner,
                        "a document holds words its row cannot match")

    _DOC_FW_RE = re.compile(
        r'<h2>Frameworks it maps to</h2>\n<ul class="chips">(.*?)</ul>', re.S)
    _FW_CHIP_RE = re.compile(r'<li><a href="([^"]*)">([^<]*)</a></li>')

    def test_document_framework_chips_open_their_search(self):
        """Design B 5.5 (a bare search link lost the framework the reader
        clicked): every framework chip on a document page links the search
        page's ?q= address for its own name, the address search.js reads on
        load, and the search it opens, replayed on the rendered search rows,
        finds the document the chip sits on."""
        rows = self._search_replay_rows()
        chips = 0
        for rel in sorted(self._doc_pages()):
            section = self._DOC_FW_RE.search(self.draft_html[rel])
            if not section:
                continue
            own = "/" + rel[:-len("index.html")]
            for href, name in self._FW_CHIP_RE.findall(section.group(1)):
                chips += 1
                self.assertEqual(_page_rel_for(unescape(href)),
                                 "draft/search/index.html", f"{rel}: {href}")
                self.assertEqual(_address_params(href), {"q": unescape(name)},
                                 f"{rel}: {href}")
                hits = {r["href"] for r in _replay_search_js(
                    rows, unescape(name), results=True, rank=True)}
                self.assertIn(own, hits,
                              f"{rel}: ?q={unescape(name)!r} misses its page")
        self.assertTrue(chips, "some document page carries framework chips")

    # -- 9. the documents index (design A PR A3) ------------------------------

    _INDEX_REL = "draft/documents/index.html"
    _FACET_CHIP_RE = re.compile(
        r'<li><a href="([^"]*)" data-filter="([^"]*)">([^<]*)'
        r'<span class="n">(\d+)</span></a></li>')
    _INDEX_ROW_RE = re.compile(
        r'<li data-search="([^"]*)" data-type="([^"]*)" data-area="([^"]*)">'
        r'<a href="([^"]*)">([^<]*)</a>')
    # The filter paragraph on All Documents, compared whole; each claim in
    # it is checked on the rendered page by the facet prose test.
    INDEX_FILTER_PROSE = (
        "<p>With script, a type chip keeps the documents of its type and an "
        "area chip the documents of its area, and typing keeps the documents "
        "whose title, type, area, purpose, or framework names match every "
        "word; a type, an area and words combine. A second click on a chosen "
        "chip, or a click on All, clears that chip's group and leaves the "
        "other choices as they are. Each chip's count is the number of "
        "documents of its type or area in the whole list, All counting the "
        "whole list, and stays the same whatever else is chosen; the status "
        "line under the text filter gives how many documents show. A type or "
        "area chip that would show no documents with the other group's "
        "choice and the words typed is marked unavailable, with a dashed "
        "border: choosing it on the page (a plain click, Enter or Space) "
        "leaves the list and the page address as they are, and the status "
        "line says that it would show no documents, until the next change. "
        "Opening a chip's link in a new tab or window goes to the address it "
        "links, as any link does: the whole list for All, and the list "
        "filtered to that chip's type or area alone for any other chip. All "
        "and a chosen chip are never unavailable. "
        "The page address keeps the choice (?type=, ?area=, ?q=), so a "
        "filtered list can be linked. Without script, the whole list stays "
        "as it is.</p>"
    )

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
        return [(hay, href) for hay, _, _, href, _
                in self._INDEX_ROW_RE.findall(self._index_scope())]

    def _index_replay_rows(self):
        """The index rows as search.js reads them, for _replay_search_js."""
        return [
            {"hay": unescape(hay).lower(), "href": href,
             "title": unescape(title).lower(),
             "tokens": {"type": unescape(t).lower().split(),
                        "area": unescape(a).lower().split()}}
            for hay, t, a, href, title
            in self._INDEX_ROW_RE.findall(self._index_scope())
        ]

    def _facet_group(self, group):
        """(aria-label, chip markup) of one All Documents chip group (its
        other attributes are checked by
        test_documents_index_facet_groups_disable_empty_chips)."""
        block = re.search(
            rf'<ul class="chips" data-filter-group="{group}"[^>]* '
            r'aria-label="([^"]*)">(.*?)</ul>',
            self.draft_html[self._INDEX_REL], re.S)
        self.assertIsNotNone(block, f"the index has no {group} chip group")
        return block.group(1), block.group(2)

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
            "typing keeps the documents whose title, type, area, purpose, or "
            "framework names match every word;", index)
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

    def test_documents_index_facet_groups_filter_type_and_area(self):
        """Spec 7.29 facets (maintainer 2026-11-03: All Documents carries the
        filters, and type is a filter of it, not a separate heading): a type
        group and an area group, each a [data-filter-group] of links carrying
        data-filter, the All chip first; every row carries its taxonomy type
        slug as data-type and its area slug as data-area; each chip's count
        equals the rows carrying its token, All counts every row, and every
        row token has a chip; each chip links its own facet address on the
        index (?type=, ?area=), which search.js reads on load and which is
        the plain link without script; and search.js on a chip (replayed)
        shows exactly the chip's count."""
        docs = {self.mod._doc_page_url("/draft", d["path"]): d
                for d in self._full_taxonomy()
                if d.get("domain") != self.mod.ROOT_DOMAIN}
        rows = self._index_replay_rows()
        self.assertEqual(len(rows), len(docs), "every row carries the tokens")
        for row in rows:
            d = docs[row["href"]]
            self.assertEqual(row["tokens"]["type"],
                             [self.mod.type_slug(d["type"])], row["href"])
            self.assertEqual(row["tokens"]["area"], [d["domain"]], row["href"])
        labels = {
            "type": {self.mod.type_slug(d["type"]): d["type"]
                     for d in docs.values()},
            "area": {d["domain"]: self.mod.draft_domain_label(d["domain"])
                     for d in docs.values()},
        }
        for group in ("type", "area"):
            with self.subTest(group=group):
                aria, block = self._facet_group(group)
                self.assertEqual(aria, f"Filter by {group}")
                chips = self._FACET_CHIP_RE.findall(block)
                self.assertEqual(len(chips), block.count("<li>"),
                                 "every item in the group is a facet chip")
                self.assertEqual(chips[0], ("/draft/documents/", "", "All",
                                            str(len(rows))),
                                 "the All chip leads and counts every row")
                tokens = Counter(row["tokens"][group][0] for row in rows)
                self.assertEqual({v: int(n) for _, v, _, n in chips[1:]},
                                 dict(tokens),
                                 "one chip per row token, counting its rows")
                for href, value, label, n in chips[1:]:
                    self.assertEqual(_address_params(href), {group: value})
                    self.assertEqual(_page_rel_for(href), self._INDEX_REL)
                    self.assertEqual(unescape(label), labels[group][value])
                    self.assertEqual(
                        len(_replay_search_js(rows, active={group: value})),
                        int(n), f"{group}={value}")

    def test_documents_index_facets_combine_with_each_other_and_the_text(self):
        """The two groups and the text filter combine (spec 7.29: a row shows
        when every active facet's value is among its tokens and it matches
        the query). Replayed on the rendered rows for the largest type and
        area: the pair keeps exactly the rows carrying both tokens, and a
        word from one of those titles narrows that further, never widening
        it."""
        rows = self._index_replay_rows()
        self.assertEqual(len(rows), self._index_scope().count("<li "),
                         "every row carries a type and an area token")
        self.assertTrue(rows)
        types = Counter(row["tokens"]["type"][0] for row in rows)
        areas = Counter(row["tokens"]["area"][0] for row in rows)
        pair = {"type": types.most_common(1)[0][0],
                "area": areas.most_common(1)[0][0]}
        both = _replay_search_js(rows, active=pair)
        self.assertEqual(
            [row["href"] for row in both],
            [row["href"] for row in rows
             if pair["type"] in row["tokens"]["type"]
             and pair["area"] in row["tokens"]["area"]])
        self.assertTrue(both)
        self.assertLess(len(both), types[pair["type"]])
        word = max(both[0]["title"].split(), key=len)
        narrowed = _replay_search_js(rows, word, active=pair)
        self.assertIn(both[0], narrowed)
        self.assertLessEqual(len(narrowed), len(both))

    def test_documents_index_filter_prose_is_true_for_every_chip_and_row(self):
        """The page prose rule on the filter paragraph, read off the rendered
        page with each claim checked there: a type chip keeps the documents
        of its type and an area chip those of its area (each chip replayed,
        every kept row's taxonomy type or area checked); the address keeps
        ?type=, ?area= and ?q= (the page's facet groups are exactly type and
        area, and its form holds the q input search.js writes). The count,
        All and status claims are replayed in every combined state by
        test_documents_index_counts_hold_in_every_combined_state, and the
        typing clause against every row's data-search text by
        test_documents_index_rows_carry_the_search_text."""
        index = self.draft_html[self._INDEX_REL]
        self.assertIn(self.INDEX_FILTER_PROSE, index)
        docs = {self.mod._doc_page_url("/draft", d["path"]): d
                for d in self._full_taxonomy()
                if d.get("domain") != self.mod.ROOT_DOMAIN}
        rows = self._index_replay_rows()
        field = {"type": lambda d: self.mod.type_slug(d["type"]),
                 "area": lambda d: d["domain"]}
        for group in ("type", "area"):
            _, block = self._facet_group(group)
            for _, value, label, n in self._FACET_CHIP_RE.findall(block):
                if not value:
                    continue
                with self.subTest(group=group, chip=label):
                    kept = _replay_search_js(rows, active={group: value})
                    self.assertEqual(
                        [r["href"] for r in kept],
                        [href for href in (r["href"] for r in rows)
                         if field[group](docs[href]) == value],
                        "the chip keeps exactly its documents")
        self.assertEqual(
            re.findall(r'\sdata-filter-group="([^"]*)"', index),
            ["type", "area"], "the address keys the prose names")
        self.assertRegex(
            index, r'<form class="search" role="search" data-search>'
                   r'<label class="lbl" for="q">[^<]*</label>'
                   r'<input id="q" type="search"')
        self.assertLess(index.find("data-filter-group"),
                        index.find("data-search-scope"),
                        "the chips sit above the list they filter")

    def test_documents_index_counts_hold_in_every_combined_state(self):
        """Round-1 ERROR: "Each chip's count is the number of documents in
        this list that it keeps, and All keeps the whole list" was false once
        filters combine (with ?type=policy&area=ai the Policy and AI chips
        kept their whole-list counts while one row showed). The paragraph's
        count, All and status claims are replayed in every combined state,
        every type value (All included) by every area value (All included),
        and each type page's filter address as search.js loads it: every
        chip's count is its documents in the whole list and All's the whole
        list; search.js writes no text but the status line, so no count
        changes with the state; a click on All, or a second click on the
        chosen chip, clears only that chip's group; and the status line,
        under the text filter, gives how many rows show. Some state shows a
        chip fewer rows than its count, so the old wording was false."""
        index = self.draft_html[self._INDEX_REL]
        self.assertIn(self.INDEX_FILTER_PROSE, index)
        rows = self._index_replay_rows()
        chips = {}
        for group in ("type", "area"):
            found = self._FACET_CHIP_RE.findall(self._facet_group(group)[1])
            chips[group] = {value: int(n) for _, value, _, n in found}
            for value, n in chips[group].items():
                self.assertEqual(
                    n, sum(1 for r in rows
                           if not value or value in r["tokens"][group]),
                    f"{group}={value}: its documents in the whole list")
        self.assertEqual(chips["type"][""], len(rows), "All is the list")
        self.assertEqual(chips["area"][""], len(rows), "All is the list")
        js = self.draft_all["draft/assets/baseline/search.js"].decode("utf-8")
        # From 1.7.0 search.js also writes a chip's .n (el), only in a group
        # with data-filter-count="live", which neither group carries, and
        # the text of the hidden note it creates once (note); so the counts
        # stay as served.
        self.assertEqual(set(re.findall(r"(\w+)\.textContent\s*=", js)),
                         {"status", "el", "note"},
                         "only the status line's text changes here")
        self.assertIn('        if (g.live) {\n'
                      '          var el = c.querySelector(".n");', js)
        self.assertIn('live: el.getAttribute("data-filter-count") === "live"',
                      js)
        self.assertNotIn("data-filter-count", index)
        self.assertIn('status.textContent = "Showing " + shown + " of " + '
                      'total + " documents.";', js)
        self.assertRegex(index, r'<input id="q" type="search"[^>]*>'
                                r'<p class="status" role="status"[^>]*'
                                r'\sdata-search-status></p></form>')
        # Each type page's filter address, as search.js loads it: a value
        # is set only when a chip of its group carries it.
        loaded = set()
        for tp in self.figures["type_pages"]:
            for href in re.findall(r'<a href="([^"]*/documents/\?[^"]*)">',
                                   self.draft_html[self._type_rel(tp["type"])]):
                params = _address_params(href)
                self.assertEqual(set(params), {"type"}, href)
                self.assertIn(params["type"], chips["type"], href)
                loaded.add(params["type"])
        self.assertTrue(loaded, "type pages link their filter address")
        states = [{"type": t, "area": a}
                  for t in chips["type"] for a in chips["area"]]
        self.assertLessEqual({(t, "") for t in loaded},
                             {(s["type"], s["area"]) for s in states})
        fewer = 0
        for state in states:
            with self.subTest(**state):
                # The status line's number is the rows shown, those carrying
                # every chosen token, recounted here.
                shown = _replay_search_js(rows, active=state)
                self.assertEqual(
                    shown, [r for r in rows
                            if all(not v or v in r["tokens"][g]
                                   for g, v in state.items())])
                for group, other in (("type", "area"), ("area", "type")):
                    cleared = _replay_search_js(
                        rows, active={group: "", other: state[other]})
                    self.assertEqual(
                        len(cleared), chips[other][state[other]],
                        "clearing a group leaves the other as it is")
                    for value, n in chips[group].items():
                        kept = _replay_search_js(
                            rows, active={group: value, other: state[other]})
                        if len(kept) < n:
                            fewer += 1
        self.assertTrue(fewer, "a chip can show fewer rows than its count")

    def test_documents_index_facet_groups_disable_empty_chips(self):
        """Spec 7.29 from 1.7.0 (CHANGELOG 1.7.0: grclibrary.ai's request
        for chips that show when a choice would give no results; site round
        b170-r1: two groups again, each marking such a chip): All Documents has
        exactly the type and area groups, each a ul.chips opted in with
        data-filter-empty="disable" and labelled for screen readers, each
        holding its own All chip, so no All chip sits outside a group; no
        group opts in to live counts, because the filter paragraph says the
        counts stay the same; and no other draft page has a facet group."""
        index = self.draft_html[self._INDEX_REL]
        for group in ("type", "area"):
            with self.subTest(group=group):
                self.assertEqual(
                    index.count(f'data-filter-group="{group}"'), 1)
                self.assertIn(
                    f'<ul class="chips" data-filter-group="{group}" '
                    'data-filter-empty="disable" '
                    f'aria-label="Filter by {group}">', index)
                chips = self._FACET_CHIP_RE.findall(
                    self._facet_group(group)[1])
                self.assertEqual([v for _, v, _, _ in chips].count(""), 1,
                                 "the group holds its own All chip")
        self.assertEqual(
            re.findall(r'\sdata-filter-group="([^"]*)"', index),
            ["type", "area"])
        self.assertEqual(index.count('data-filter-empty="disable"'), 2)
        self.assertEqual(index.count(' data-filter=""'), 2,
                         "no All chip outside the two groups")
        self.assertNotIn("data-filter-count", index)
        self.assertIn("and stays the same whatever else is chosen",
                      self.INDEX_FILTER_PROSE)
        self.assertEqual(
            sorted(rel for rel, html in self.draft_html.items()
                   if "data-filter-group" in html), [self._INDEX_REL])
        js = self.draft_all["draft/assets/baseline/search.js"].decode("utf-8")
        self.assertIn('empty: el.getAttribute("data-filter-empty") === '
                      '"disable"', js)

    def test_documents_index_unavailable_chip_sentence_holds(self):
        """The filter paragraph's unavailable-chip sentences, each checked:
        search.js 1.7.0 (spec 7.29) marks a chip unavailable when its
        would-show count is 0, counted with the words typed and every other
        group's choice, never for All or the chosen chip ("var off = ...");
        activating one returns before any choice, row or address change and
        writes the refusal to the status line; and baseline.css draws it
        with a dashed border. Replayed on the rendered rows in every
        combined state (every type value by every area value, All
        included): the chips the sentence covers exist on this page."""
        index = self.draft_html[self._INDEX_REL]
        self.assertIn(self.INDEX_FILTER_PROSE, index)
        js = self.draft_all["draft/assets/baseline/search.js"].decode("utf-8")
        self.assertIn('var off = g.empty && v !== "" && v !== g.value && '
                      'n === 0;', js)
        # "with the other group's choice and the words typed": a row that
        # misses a word counts nowhere; one that misses only another
        # group's choice counts toward that group alone.
        self.assertIn('if (!terms.every(function (t) { return '
                      'r.hay.indexOf(t) >= 0; })) { return false; }', js)
        self.assertIn('var n = v ? tally[g.name].v[v] || 0 : '
                      'tally[g.name].all;', js)
        click = js[js.index('c.addEventListener("click"'):]
        refused = click.index('if (c.getAttribute("aria-disabled") === '
                              '"true") {')
        self.assertLess(refused, click.index("g.value ="),
                        "the refusal returns before the choice changes")
        # "choosing it on the page (a plain click, Enter or Space)": Space
        # clicks the chip, and a modified or non-primary click returns before
        # the refusal, so the browser opens the chip's link as any link.
        self.assertIn('if (e.key === " " || e.key === "Spacebar") { '
                      'e.preventDefault(); c.click(); }', js)
        self.assertLess(click.index('if (e.metaKey || e.ctrlKey || '
                                    'e.shiftKey || e.altKey || e.button !== '
                                    '0) { return; }'), refused)
        self.assertIn('status.textContent = labelOf(c) + " would show no '
                      'documents with the current choices.";',
                      click[refused:click.index("g.value =")])
        css = self.draft_all["draft/assets/baseline/baseline.css"].decode(
            "utf-8")
        self.assertIn('.chips a[aria-disabled="true"], .chips '
                      'button[aria-disabled="true"] { border-style: dashed;',
                      css)
        rows = self._index_replay_rows()
        chips = {group: [v for _, v, _, _ in self._FACET_CHIP_RE.findall(
                     self._facet_group(group)[1])]
                 for group in ("type", "area")}
        unavailable = 0
        for t in chips["type"]:
            for a in chips["area"]:
                state = {"type": t, "area": a}
                for group, values in chips.items():
                    for value in values:
                        if value in ("", state[group]):
                            continue  # All and the chosen chip: never off
                        # The would-show count of spec 7.29: the rows
                        # holding every other group's choice and this
                        # chip's value (no words typed here).
                        unavailable += not _replay_search_js(
                            rows, active={**state, group: value})
        self.assertTrue(unavailable,
                        "some state has a chip the sentence covers")

    def test_documents_index_type_chips_count_what_their_type_pages_list(self):
        """Each type chip's count equals the corpus-area rows its type page
        lists, the rows its filter keeps, and every type page with such a
        row has a chip (site f1: a chip counts the rows it filters, so a
        library specification, which has a type page row and no All
        Documents row, stays out of it). Integration round 2: a type page
        also lists the type's adopter documents, which All Documents does
        not carry, in their own counted block, so the page's total is its
        corpus list plus that block's and the page states the corpus count
        apart."""
        _, block = self._facet_group("type")
        type_chips = [(href, value, label, n) for href, value, label, n
                      in self._FACET_CHIP_RE.findall(block) if value]
        with_rows = set()
        adopter_label = re.escape(self.mod._esc(
            self.mod.draft_domain_label(self.mod.ADOPTER_DOCS_AREA)))
        for tp in self.figures["type_pages"]:
            page = self.draft_html[self._type_rel(tp["type"])]
            scope = re.search(
                r'<ul class="plan one described">(.*?)</ul>', page, re.S)
            self.assertIsNotNone(scope, "the type page has no list")
            corpus = self._TYPE_ROW_RE.findall(scope.group(1))
            in_area = [href for href, _, _, _ in corpus
                       if not href.startswith(self.mod.GITHUB_BLOB_BASE)]
            if in_area:
                with_rows.add(tp["slug"])
            adopter = re.search(
                rf'<p class="lbl blk">{adopter_label}, (\d+)</p>', page)
            with self.subTest(type=tp["type"]):
                if adopter:
                    self.assertIn(f": {len(corpus)} in the corpus and "
                                  f"{adopter.group(1)} adopter ", page,
                                  "the page states its corpus count apart")
                    shown = len(corpus) + int(adopter.group(1))
                else:
                    shown = len(corpus)
                self.assertIn(f"Documents, {shown}</p>", page)
            for _, value, label, n in type_chips:
                if value != tp["slug"]:
                    continue
                with self.subTest(chip=label):
                    self.assertEqual(int(n), len(in_area),
                                     "the chip counts the type page's "
                                     "corpus-area rows")
        self.assertEqual({value for _, value, _, _ in type_chips}, with_rows,
                         "one chip per type page with a corpus-area row")

    def test_documents_index_counts_a_type_only_root_documents_hold(self):
        """Every type in today's corpus has a non-root document, so the live
        render cannot tell the counts apart; a fixture can. A type held only
        by root specifications still counts among the page's types (the
        meta line counts every document on the page), but no filtered row
        carries it, so its group has no chip: a chip whose count is the rows
        it keeps would read 0 (round-1 ERROR on this page: a count that
        differed from what the chip's landing showed)."""
        root = self.mod.ROOT_DOMAIN
        values = self.mod.draft_documents_values([
            {"path": "governance/policy-a.md", "domain": "governance",
             "type": "Policy", "title": "A"},
            {"path": "specification-b.md", "domain": root,
             "type": "Specification", "title": "B"},
        ])
        self.assertEqual(values["INDEX_TYPE_COUNT"], "2")
        self.assertNotIn("specification", values["INDEX_TYPE_CHIPS"].lower())
        self.assertEqual(
            values["INDEX_TYPE_CHIPS"],
            '<li><a href="{{BASE}}/documents/" data-filter="">All'
            '<span class="n">1</span></a></li>\n'
            '<li><a href="{{BASE}}/documents/?type=policy" '
            'data-filter="policy">Policy<span class="n">1</span></a></li>')
        self.assertIn('data-type="policy" data-area="governance"',
                      values["INDEX_ROWS"])

    def test_documents_index_refuses_a_facet_value_no_chip_can_match(self):
        """search.js splits a row's tokens on whitespace and compares them
        in lowercase, so an area slug that is not one lowercase token would
        publish a chip that keeps nothing; the build refuses it instead."""
        with self.assertRaises(self.mod.BuildError) as caught:
            self.mod.draft_documents_values([
                {"path": "Bad Area/policy-a.md", "domain": "Bad Area",
                 "type": "Policy", "title": "A"},
            ])
        self.assertIn("'Bad Area'", str(caught.exception))

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
        filtered list). Integration round 2 NOTE (and f1 round-1 NOTE): All
        Documents carries the corpus, not the docs/ adopter documents, which
        have pages but no row on the index, so the sentence says every
        corpus document and points to the Browse list that carries every
        adopter document. Site f1: the sentence names the index's filters,
        by type, by area and by words."""
        browse = self.draft_html["draft/browse/index.html"]
        main = browse.split('<main id="main-content">', 1)[1]
        self.assertIn('<a href="/draft/documents/">All Documents</a>', main,
                      "the Browse page body links the index by name")
        label = self.mod._esc(
            self.mod.draft_domain_label(self.mod.ADOPTER_DOCS_AREA))
        self.assertIn(
            "<p>To see every corpus document on one page, open "
            '<a href="/draft/documents/">All Documents</a>; its filters, by '
            "type, by area and by words, cover the documents across the "
            "domains. The adopter documents, outside the corpus, are listed "
            f"further down this page, under {label}.</p>", main)
        self.assertNotIn("every document in the library", main)
        index = self.draft_html[self._INDEX_REL]
        # "its filters, by type, by area and by words": the index's two
        # facet groups and its text filter, all over the one filtered list.
        self.assertEqual(
            re.findall(r'\sdata-filter-group="([^"]*)"', index),
            ["type", "area"])
        self.assertEqual(index.count("<form "), 1)
        self.assertEqual(index.count("data-search-scope"), 1)
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
        are exactly the documents across the domains; the docs/ adopter
        documents have pages and no link there."""
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
        adopter = {self.mod._doc_page_url("/draft", d["path"])
                   for d in self.mod.parse_adopter_docs()}
        self.assertTrue(adopter, "the library holds adopter documents")
        for href in sorted(adopter):
            self.assertIn(_page_rel_for(href), self.draft_html, href)
        self.assertEqual(adopter & linked, set(),
                         "the adopter documents are no corpus document of "
                         "All Documents, so the sentence names the corpus")
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
        "groups and the kinds of page are curated in the site generator; "
        "their counts and the domain list are generated at build time. "
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
                r'<div class="wide"><ul class="plan described one">(.*?)</ul>',
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
            mark = "" if pages else '<span class="n">declared gap</span>'
            row = (f'<li><a href="/draft/decide/{concern["slug"]}/">'
                   f'{self.mod._esc(concern["question"])}</a>{mark}'
                   f'<small>{self.mod._esc(concern["label"])}. '
                   f'{self._concern_counts_text(pages, docs)}.</small></li>')
            self.assertIn(row, hub, concern["slug"])

    # Item 3b788: .plan li .n is nowrap in a minmax(0, 1fr) auto grid, so a
    # long count takes the row and the title column shrinks to nothing. At
    # 320 px a row is 254 px wide and a .n character 7.9 px (headless Chrome,
    # JetBrains Mono at 0.82rem); 25 characters (197 px) leave the title
    # about 40 px beside the 1rem gap, the room the widest count on these
    # pages, "specification, Governance" on documents/, leaves today. The
    # crosswalk instrument pages' identifier lists (up to 140 characters,
    # basc 1152 px wide at 320 px) now sit in the <small> line too, so the
    # crosswalk and leadership pages are held to the same limit.
    _N_MAX_CHARS = 25

    def test_no_plan_count_outgrows_a_320px_row(self):
        rels = [rel for rel in self.draft_html
                if rel in {f"draft/{page}/index.html" for page in (
                    "decide", "browse", "policies", "comply", "govern",
                    "solutions", "documents")}
                or rel.startswith(("draft/types/", "draft/decide/",
                                   "draft/crosswalk/", "draft/decisions/"))]
        self.assertGreater(len(rels), 7, "the pages under test rendered")
        self.assertTrue(
            any(rel.startswith("draft/crosswalk/") for rel in rels)
            and any(rel.startswith("draft/decisions/") for rel in rels),
            "the crosswalk and leadership pages are under test")
        for rel in rels:
            html = self.draft_html[rel]
            for count in re.findall(r'<span class="n">(.*?)</span>', html,
                                    re.S):
                text = unescape(re.sub(r"<[^>]+>", "", count))
                with self.subTest(page=rel, count=text):
                    self.assertLessEqual(
                        len(text), self._N_MAX_CHARS,
                        "a nowrap .n count this long squeezes the row's "
                        "title column to nothing at 320 px; carry it in the "
                        "row's <small> line")

    def test_every_draft_table_scrolls_inside_a_tablewrap(self):
        """Item 3b788: a table outside the baseline's .tablewrap widens the
        page when its columns outgrow it (the outcome maps' nowrap uppercase
        headers made the page 522 px wide at 320 px); inside it, the table
        scrolls in its own box. Every table on every draft page opens its
        .tablewrap, the leadership pages' body tables among them."""
        wrapped = re.compile(r'<div class="tablewrap[^"]*"[^>]*>\s*<table\b')
        narrative = 0
        for rel, html in self.draft_html.items():
            tables = html.count("<table")
            with self.subTest(page=rel):
                self.assertEqual(len(wrapped.findall(html)), tables,
                                 "a table outside .tablewrap can widen the "
                                 "page at 320 px")
            if tables and rel.startswith("draft/decisions/"):
                narrative += 1
        self.assertGreaterEqual(narrative, 3,
                                "the outcome maps' tables are under test")

    # Item 3b788: a register address with no break opportunity widened its
    # instrument page (nist-sp-800-53's 50 characters ran 325 px from a
    # 16 px inset, 341 px wide at 320 px; headless Chrome, the record's
    # 0.95rem Public Sans, about 6.5 px a character). The record has about
    # 273 px at 320 px, so a run of 36 characters (about 234 px) fits.
    _ADDRESS_RUN_MAX_CHARS = 36

    def test_register_addresses_wrap_inside_a_320px_record(self):
        xw = self.mod.build_crosswalk(self._full_taxonomy())
        checked = 0
        for key, data in xw["instruments"].items():
            row = data["register"]
            if row is None or row["upstream"] == "-":
                continue
            page = self.draft_html[f"draft/crosswalk/{key}/index.html"]
            link = re.search(
                r'<dt>Upstream check location</dt><dd><a href="([^"]*)"'
                r'[^>]*>(.*?)<span class="vh">', page, re.S)
            with self.subTest(instrument=key):
                self.assertIsNotNone(link, "the record links the address")
                href, text = link.groups()
                self.assertEqual(unescape(href), row["upstream"])
                self.assertEqual(unescape(text.replace("<wbr>", "")),
                                 row["upstream"],
                                 "the link text reads as the address")
                self.assertEqual(text.count("<wbr>"),
                                 len(re.findall("/(?!/)", row["upstream"])),
                                 "a break opportunity after each slash")
                # A hyphen before a letter is a break opportunity too; one
                # before a digit is not ("p-39.1" stays whole).
                for run in re.split(r"<wbr>|(?<=-)(?=[A-Za-z])", text):
                    self.assertLessEqual(
                        len(unescape(run)), self._ADDRESS_RUN_MAX_CHARS,
                        f"{run!r} cannot wrap inside the record at 320 px")
            checked += 1
        self.assertGreater(checked, 0, "the register addresses rendered")

    def test_no_path_link_text_outruns_a_320px_column(self):
        """Item 3b788: the same holds for every link whose text is an address
        or a corpus path (a slash, no space) on every draft page, such as a
        related document's source row ("compliance/healthcare/README.md" in a
        191 px title column took two document pages to 323 px at 320 px)."""
        link_re = re.compile(r"<a\b[^>]*>(.*?)</a>", re.S)
        sources = 0
        for rel, html in self.draft_html.items():
            for body in link_re.findall(html):
                text = re.sub(r'<span class="vh">.*?</span>', "", body)
                plain = unescape(text.replace("<wbr>", ""))
                if ("<" in text.replace("<wbr>", "") or "/" not in plain
                        or " " in plain):
                    continue
                sources += rel.startswith("draft/documents/")
                for run in re.split(r"<wbr>|(?<=-)(?=[A-Za-z])", text):
                    with self.subTest(page=rel, text=plain):
                        self.assertLessEqual(
                            len(unescape(run)), self._ADDRESS_RUN_MAX_CHARS,
                            f"{run!r} cannot wrap at 320 px")
        self.assertGreater(sources, 0,
                           "the document pages' source rows are under test")

    def test_every_path_link_text_breaks_after_each_slash(self):
        """Item 3b788 round 2: a run under the limit above can still outrun a
        narrower column ("compliance/healthcare/README.md", 31 characters, in
        a 191 px source row took two document pages to 323 px at 320 px), so
        every link whose text is the address or corpus path it opens (a
        register address on a crosswalk page, a source row on a document
        page) carries a <wbr> after each slash but the first of a "//"."""
        link_re = re.compile(r'<a\b[^>]*?\bhref="([^"]*)"[^>]*>(.*?)</a>',
                             re.S)
        found = {"draft/crosswalk/": 0, "draft/documents/": 0}
        for rel, html in self.draft_html.items():
            for href, body in link_re.findall(html):
                text = re.sub(r'<span class="vh">.*?</span>', "", body)
                plain = unescape(text.replace("<wbr>", ""))
                if "/" not in plain or unescape(href) not in (
                        plain, self.mod.GITHUB_BLOB_BASE + plain):
                    continue
                with self.subTest(page=rel, text=plain):
                    self.assertIsNone(
                        re.search("/(?!/|<wbr>)", text),
                        "a slash with no <wbr> after it leaves the path no "
                        "break there")
                for prefix in found:
                    found[prefix] += rel.startswith(prefix)
        for prefix, count in found.items():
            self.assertGreater(count, 0,
                               f"the path links on {prefix} pages are under "
                               "test")

    # Item 3b788 lows round 1: each title word of 15 to 17 letters with its
    # width in px set alone in the h1 at 320 px in the dark scheme, the wider
    # one (headless Chrome 156, the 2.2rem Newsreader 300, 0.01em tracking).
    _MEASURED_TITLE_WORDS = {
        "Trustworthiness": 238.9,
        "Responsibilities": 231.1,
        "Pseudonymization": 275.2,
        "Interrelationship": 247.7,
    }

    def _assert_heading_pieces_measured(self, titles):
        """Each run of more than 14 letters the document h1 of one of
        ``titles`` renders, split at the soft hyphens _draft_breakable_title
        inserts, is one of _MEASURED_TITLE_WORDS, and each of those renders.
        A title word of 18 or more letters renders as its pieces, so they
        are what must fit, and a longer piece is unmeasured too."""
        pieces = {p for t in titles
                  for part in unescape(
                      self.mod._draft_breakable_title(t)).split("\u00ad")
                  for p in re.findall(r"[^\W\d_]+", part)}
        self.assertEqual(
            {p for p in pieces if len(p) > 14},
            set(self._MEASURED_TITLE_WORDS),
            "an h1 piece of more than 14 letters not measured to fit the "
            "288 px h1 box at 320 px; measure it in light and dark, then "
            "list it")

    def test_document_heading_words_can_break_at_320px(self):
        """Item 3b788 round 2: "Telecommunications" (18 letters) ran 19 px
        past its 288 px h1 box at 320 px in the dark scheme and widened its
        page to 323 px. No draft h1 holds a run of more than
        DRAFT_TITLE_RUN_MAX letters without a soft hyphen; a document
        heading reads as the title once they are removed, and the page's
        <title> keeps the plain title.

        Item 3b788 lows round 1 item 4: with the limit at 14 letters,
        "Trustworthiness", "Responsibilities" and "Interrelationship" broke
        where the whole word fits on the next line. Measured in the 288 px
        h1 box at 320 px, light and dark, every title word of up to 17
        letters fits with at least 12 px to spare, so the limit is 17; a
        title word of 15 to 17 letters must be one of those measured
        (_MEASURED_TITLE_WORDS), since a new one, unlike a word of 14
        letters or fewer, could be too wide."""
        self.assertEqual(self.mod.DRAFT_TITLE_RUN_MAX, 17)
        long_run = re.compile(
            rf"[^\W\d_]{{{self.mod.DRAFT_TITLE_RUN_MAX + 1},}}")
        self.assertEqual(
            self.mod._draft_breakable_title(
                "Telecommunications & Trustworthiness"),
            "Telecommu&shy;nications &amp; Trustworthiness")
        self._assert_heading_pieces_measured(
            d.get("title", "") for d in self._full_taxonomy())
        for word, width in self._MEASURED_TITLE_WORDS.items():
            with self.subTest(word=word):
                self.assertLessEqual(width + 12, 288)
        hyphenated = []
        for rel, html in self.draft_html.items():
            h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", html, re.S)
            if h1 is None:
                continue
            heading = h1.group(1)
            with self.subTest(page=rel):
                self.assertIsNone(
                    long_run.search(unescape(heading)),
                    "a word too long for the h1 at 320 px has no soft hyphen")
                if rel.startswith("draft/documents/") and rel != (
                        "draft/documents/index.html"):
                    title = re.search(r"<title>(.*?) \| GRCLibrary\.ai</title>",
                                      html).group(1)
                    self.assertEqual(heading.replace("&shy;", ""), title,
                                     "the heading reads as the title")
                    self.assertNotIn("&shy;", title)
            if "&shy;" in heading:
                hyphenated.append(rel)
        self.assertIn("draft/documents/compliance/telecommunications/"
                      "annex-telecommunications-sector-requirements/"
                      "index.html", hyphenated)

    def test_heading_guard_measures_the_pieces_a_long_word_renders(self):
        """Item 3b788: the guard above measures the pieces an h1 renders, not
        whole title words. A synthetic 22-letter word breaks into
        "Overstrengthsst" (15 letters, unmeasured) and "rengths"; a guard
        over whole words of 15 to 17 letters never saw that piece."""
        word = "Overstrengthsstrengths"
        self.assertEqual(self.mod._draft_breakable_title(word),
                         "Overstrengthsst&shy;rengths")
        titles = [d.get("title", "") for d in self._full_taxonomy()]
        with self.assertRaises(AssertionError):
            self._assert_heading_pieces_measured(titles + [word])

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
        # In the page body: the top bar's Decisions link is on every page.
        for slug in SUBTYPE_SLUGS:
            self.assertIn(
                'href="/draft/decide/"',
                self.draft_html[f"draft/decide/{slug}/index.html"].split(
                    '<main id="main-content">', 1)[1],
                f"{slug}: the subtype index links up to the decide hub")

    # -- 14. the crosswalk (design C 3.7 Version A) --------------------------

    _XW_COL_RE = re.compile(r'<th scope="col" data-col="([a-z0-9-]+)"')
    _XW_COUNT_LINK_RE = re.compile(
        r'<a href="(/draft/crosswalk/([a-z0-9-]+)/#([a-z-]+))">'
        r'(\d+)<span class="vh"> documents?</span></a>'
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
        for preset in self.mod.CROSSWALK_TOPICS:
            rel = f"draft/crosswalk/view/{preset.slug}/index.html"
            self.assertIn(rel, self.draft_html,
                          f"preset '{preset.slug}' has no generated view page")
            page = self.draft_html[rel]
            self.assertEqual(
                sorted(self._XW_COL_RE.findall(page)), sorted(preset.columns),
                f"the '{preset.slug}' view renders exactly its own columns")
            # Round-2 item 9: a bare href check also matched the Next block's
            # link, so a removed All link passed; pin the list item itself.
            self.assertIn(
                '<li><a href="/draft/crosswalk/">All</a></li>', page,
                f"the '{preset.slug}' view keeps the All link in the views "
                "list")
        main = self.draft_html["draft/crosswalk/index.html"]
        self.assertIn(
            '<li><a href="/draft/crosswalk/" aria-current="page" '
            'data-preset="" data-preset-id="all">All</a></li>',
            main, "the full crosswalk marks All as the current view, and All "
            "is its matrix.js preset showing every column")

    def test_crosswalk_caveat_block_present(self):
        pages = ["draft/crosswalk/index.html"]
        pages += [f"draft/crosswalk/view/{p.slug}/index.html"
                  for p in self.mod.CROSSWALK_TOPICS]
        pages += [f"draft/crosswalk/{i.key}/index.html"
                  for i in self.mod.CROSSWALK_INSTRUMENTS]
        # The matrices' own caveats (design C 3.6), carried nearly verbatim;
        # the AICPA TSC caveat renders only where the table has that column
        # (test_crosswalk_tsc_caveat_only_where_the_table_has_the_column).
        fragments = (
            "citations are indicative, not exhaustive",
            "certification, attestation, or legal opinion",
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
        crosswalk. The Browse page and the landing page link it in their
        page bodies, apart from the top bar's Crosswalk link."""
        count = len([i for i in self.mod.CROSSWALK_INSTRUMENTS
                     if i.main_table])
        landing = self.draft_html["draft/index.html"].split(
            '<main id="main-content">', 1)[1]
        self.assertIn('href="/draft/crosswalk/"', landing,
                      "the landing page links the crosswalk")
        self.assertIn(f'<span class="n">{count} instruments</span>', landing,
                      "the landing tile's instrument count is computed")
        browse = self.draft_html["draft/browse/index.html"].split(
            '<main id="main-content">', 1)[1]
        self.assertIn('href="/draft/crosswalk/"', browse,
                      "the Browse page links the crosswalk")
        self.assertIn(
            f"against {count} standards, laws, frameworks, and programmes",
            browse, "the Browse sentence's instrument count is computed")

    _XW_RAIL_RE = re.compile(r'<div class="lrail">(.*?)</div>', re.S)

    def test_crosswalk_preset_list_sits_in_the_rail(self):
        """Round-2 item 3 (maintainer direction, 15:09Z): the preset list is
        a vertical list in one side rail; the table takes the main column.
        The links stay links to the preset views. Round 2b: the one-side
        rule holds for anchors, by role, because a preset view's required
        self-canonical (a head <link>, page hygiene test) names its own
        /draft/crosswalk/view/ URL and is no preset link. Site f2: the rail
        is the left-rail page's side list (spec 7.32), the right rail having
        stood in for it until the template carried one."""
        pages = ["draft/crosswalk/index.html"]
        pages += [f"draft/crosswalk/view/{p.slug}/index.html"
                  for p in self.mod.CROSSWALK_TOPICS]
        for rel in pages:
            html = self.draft_html[rel]
            rail = self._XW_RAIL_RE.search(html)
            self.assertIsNotNone(rail, f"{rel}: no side list")
            self.assertIn('href="/draft/crosswalk/"', rail.group(1),
                          f"{rel}: the All link sits in the rail")
            for preset in self.mod.CROSSWALK_TOPICS:
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

    # -- 29. crosswalk left rail and matrix presets (site f2) ---------------

    _XW_RAIL_BLOCK_RE = re.compile(
        r'<p class="lbl">([^<]*)</p><ul>(.*?)</ul>', re.S)
    _XW_RAIL_LINK_RE = re.compile(
        r'<li><a href="([^"]*)"([^>]*)>([^<]*)</a></li>')
    _XW_PRESET_RE = re.compile(
        r'<a href="([^"]*)"[^>]*\sdata-preset="([^"]*)" '
        r'data-preset-id="([^"]*)">([^<]*)</a>')
    _XW_ROW_RE = re.compile(r"<tr>(.*?)</tr>", re.S)
    _XW_CELL_RE = re.compile(r"<(th|td)\b([^>]*)>(.*?)</\1>", re.S)
    _XW_DATA_COL_RE = re.compile(r'\sdata-col="([^"]*)"')
    _XW_ALSO = "Also in the corpus"

    def _xw_table_pages(self):
        return ["draft/crosswalk/index.html"] + [
            f"draft/crosswalk/view/{p.slug}/index.html"
            for p in self.mod.CROSSWALK_TOPICS]

    def _xw_main_order(self, columns):
        """A view's columns as the full table orders them (round 3 item 7:
        matrix.js hides columns and never reorders them)."""
        return [i.key for i in self.mod.CROSSWALK_INSTRUMENTS
                if i.main_table and i.key in columns]

    def _xw_groups(self):
        """The page's instrument groups, rebuilt here from the instrument
        table: every column group in order, then the Also in the corpus
        instruments, each with its instruments in configured order."""
        groups = list(self.mod.CROSSWALK_GROUPS) + [self._XW_ALSO]
        return [(g, [i.key for i in self.mod.CROSSWALK_INSTRUMENTS
                     if i.group == g]) for g in groups]

    def _xw_table(self, html):
        match = re.search(
            r'<div class="tablewrap bounded" tabindex="0">\s*'
            r'(<table class="matrix sticky sticky-col"[^>]*>.*?</table>)',
            html, re.S)
        self.assertIsNotNone(
            match, "the table sits in a bounded scroll box (spec 7.31) in "
            "the matrix markup (spec 7.30)")
        return match.group(1)

    def test_crosswalk_pages_are_left_rail_pages_with_no_right_rail(self):
        """Maintainer directive 2026-11-03 15:06Z and 15:09Z: the crosswalk
        option list sits in ONE side rail on the LEFT and the page carries no
        right rail. Spec 7.32 markup and order: the kicker, the h1, then the
        side list (logo once, above a labelled nav list), then the page's
        blocks; rail.js stays off (a left-rail page has no nav.rail). The
        preset views are the crosswalk page shown without script, so they
        take the same layout. Decision: the instrument pages keep the
        standard document grid with the logo-only rail (spec 7.6 and 7.5),
        since they carry no option list and the directive names the
        crosswalk page; this pins that they did not change."""
        for rel in self._xw_table_pages():
            html = self.draft_html[rel]
            main = html[html.index("<main"):html.index("</main>")]
            self.assertEqual(main.count('<div class="doc left-rail">'), 1,
                             f"{rel}: one left-rail page grid")
            self.assertNotIn('<div class="doc">', main,
                             f"{rel}: not the standard document grid")
            self.assertNotRegex(main, r'class="rail["\s]',
                                f"{rel}: no right rail, nav or logo-only")
            self.assertNotIn("/assets/baseline/rail.js", html,
                             f"{rel}: rail.js has nothing to mark here")
            self.assertEqual(main.count('<div class="lrail">'), 1, rel)
            self.assertEqual(main.count('class="rail-logo"'), 1,
                             f"{rel}: the logo appears once")
            self.assertRegex(
                main,
                r'<div class="doc left-rail"><p class="lbl first">Crosswalk'
                r'</p>\s*<h1>[^<]+</h1>\s*<div class="lrail"><img '
                r'class="rail-logo" [^>]*><nav aria-label="[^"]+">\s*'
                r'<p class="lbl">Views</p><ul>',
                f"{rel}: kicker, h1, then the side list (spec 7.32)")
        for inst in self.mod.CROSSWALK_INSTRUMENTS:
            rel = f"draft/crosswalk/{inst.key}/index.html"
            html = self.draft_html[rel]
            self.assertIn('<div class="doc"><p class="lbl first">', html, rel)
            self.assertIn('<div class="rail"><img class="rail-logo"', html,
                          f"{rel}: the instrument page keeps its logo-only "
                          "rail")
            self.assertNotIn("left-rail", html, rel)

    def test_crosswalk_side_list_names_every_instrument_by_group(self):
        """Directive item 1: the side list holds every crosswalk instrument,
        generated and grouped as the page groups them, the Also in the corpus
        instruments included, each linking its rendered instrument page
        under its display name."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        xw = self.mod.build_crosswalk(full)
        expected = [
            (g, [(f"/draft/crosswalk/{k}/", "",
                  self.mod._esc(xw["instruments"][k]["display"]))
                 for k in keys])
            for g, keys in self._xw_groups() if keys]
        self.assertTrue(dict(expected).get(self._XW_ALSO),
                        "the Also in the corpus instruments are listed")
        for rel in self._xw_table_pages():
            rail = self._XW_RAIL_RE.search(self.draft_html[rel]).group(1)
            blocks = self._XW_RAIL_BLOCK_RE.findall(rail)
            self.assertEqual(blocks[0][0], "Views", rel)
            got = [(unescape(label), self._XW_RAIL_LINK_RE.findall(body))
                   for label, body in blocks[1:]]
            self.assertEqual(got, expected,
                             f"{rel}: the side list equals the instrument "
                             "list, group by group")
            hrefs = [h for _, links in got for h, _, _ in links]
            self.assertEqual(
                sorted(hrefs),
                sorted(f"/draft/crosswalk/{i.key}/"
                       for i in self.mod.CROSSWALK_INSTRUMENTS),
                f"{rel}: every instrument exactly once")
            for href in hrefs:
                self.assertIn(_page_rel_for(href), self.draft_html, href)

    # The topic views of design C 3.7 as the 8c3d83756 build carried them
    # (slug, label, columns, related instrument pages), pinned as literals so
    # a preset model regenerated from anything else fails here (round 2,
    # maintainer decision 2026-11-03 18:53Z: the views stay by topic).
    _XW_TOPICS = (
        ("security", "Security",
         ("iso-iec-27001", "nist-csf", "nist-sp-800-53", "csa-ccm",
          "aicpa-tsc"), ()),
        ("ai", "AI",
         ("iso-iec-42001", "nist-ai-rmf", "csa-aicm", "eu-ai-act",
          "owasp-llm-top-10", "mitre-atlas"), ()),
        ("privacy", "Privacy and data protection",
         ("gdpr", "eu-ai-act", "nis-2"), ("pipeda", "quebec-law-25")),
        ("resilience", "Resilience and financial services",
         ("dora", "nis-2", "csa-ccm"), ()),
        ("trade", "Trade and customs",
         ("ctpat", "pip", "basc", "wco-safe", "aeo"), ()),
        ("canada", "Canada", ("pip",), ("pipeda", "quebec-law-25")),
    )
    _XW_RELATED_RE = re.compile(
        r'<p class="lbl blk">Related instrument pages</p>'
        r'<ul class="chips">(.*?)</ul>', re.S)

    def test_crosswalk_presets_equal_the_topics(self):
        """Round 2 item 1: the matrix.js presets (spec 7.30) are All plus
        the topic views of design C 3.7, each holding exactly its topic's
        columns, in topic order; every column sits in at least one topic,
        the Also in the corpus instruments in none. Each preset lives in the
        side list and is a link to a page that resolves without script and
        renders that preset's columns; a static view carries no preset and
        no matrix, so no script acts there."""
        main = self.draft_html["draft/crosswalk/index.html"]
        expected = [("/draft/crosswalk/", "", "all", "All")] + [
            (f"/draft/crosswalk/view/{slug}/", " ".join(columns), slug,
             self.mod._esc(label))
            for slug, label, columns, _ in self._XW_TOPICS]
        presets = self._XW_PRESET_RE.findall(main)
        self.assertEqual(presets, expected,
                         "the presets are All plus the topic views")
        rail = self._XW_RAIL_RE.search(main).group(1)
        self.assertEqual(rail.count("data-preset="), len(expected))
        self.assertEqual(main.count("data-preset="), len(expected),
                         "every preset sits in the side list")
        columns = self._XW_COL_RE.findall(main)
        in_presets = [k for _, keys, _, _ in presets for k in keys.split()]
        self.assertEqual(sorted(set(in_presets)), sorted(columns),
                         "every column sits in at least one topic preset, "
                         "and no preset names a column the table has not")
        also = dict(self._xw_groups())[self._XW_ALSO]
        self.assertFalse(set(also) & set(in_presets),
                         "an instrument with no column is in no preset")
        for href, keys, slug, _ in presets[1:]:
            rel = _page_rel_for(href)
            self.assertIn(rel, self.draft_html,
                          f"preset '{slug}' links a page that resolves")
            view = self.draft_html[rel]
            self.assertEqual(self._XW_COL_RE.findall(view),
                             self._xw_main_order(keys.split()),
                             f"the '{slug}' view renders its preset's columns")
            self.assertNotIn("data-preset=", view, rel)
            self.assertNotRegex(view, r"\sdata-matrix\b", rel)

    def test_crosswalk_topic_view_routes_render(self):
        """Round 2 item 1: each topic view renders at its old route
        /draft/crosswalk/view/<topic>/ under its topic heading with a
        non-empty column set equal to its topic's, and links its related
        instrument pages beneath the table where it has any (each resolving);
        no other view route renders, so no instrument-group view survives."""
        rendered = sorted(
            rel for rel in self.draft_html
            if rel.startswith("draft/crosswalk/view/"))
        self.assertEqual(
            rendered,
            sorted(f"draft/crosswalk/view/{slug}/index.html"
                   for slug, _, _, _ in self._XW_TOPICS),
            "the view routes are exactly the topic routes")
        for slug, label, columns, related in self._XW_TOPICS:
            rel = f"draft/crosswalk/view/{slug}/index.html"
            html = self.draft_html[rel]
            self.assertIn(
                f"<h1>Crosswalk: {self.mod._esc(label)}</h1>", html, rel)
            self.assertTrue(columns, f"{slug}: a topic has a column")
            self.assertEqual(
                self._XW_COL_RE.findall(self._xw_table(html)),
                self._xw_main_order(columns), f"{rel}: the topic's columns")
            block = self._XW_RELATED_RE.search(html)
            if not related:
                self.assertIsNone(block, f"{rel}: no related pages block")
                continue
            self.assertIsNotNone(block, f"{rel}: the related pages block")
            hrefs = _HREF_RE.findall(block.group(1))
            self.assertEqual(
                hrefs, [f"/draft/crosswalk/{key}/" for key in related], rel)
            for href in hrefs:
                self.assertIn(_page_rel_for(href), self.draft_html, href)
        self.assertIsNone(
            self._XW_RELATED_RE.search(
                self.draft_html["draft/crosswalk/index.html"]),
            "the full crosswalk's side list already names every instrument")

    def test_crosswalk_rail_views_equal_the_topics(self):
        """Round 2 item 1: on the crosswalk page and on every view, the side
        list's Views block holds All then the topic views in topic order,
        each linking its route under its topic label, and the page's own
        view is the one marked current."""
        pages = [("draft/crosswalk/index.html", "/draft/crosswalk/")] + [
            (f"draft/crosswalk/view/{slug}/index.html",
             f"/draft/crosswalk/view/{slug}/")
            for slug, _, _, _ in self._XW_TOPICS]
        expected = [("/draft/crosswalk/", "All")] + [
            (f"/draft/crosswalk/view/{slug}/", self.mod._esc(label))
            for slug, label, _, _ in self._XW_TOPICS]
        for rel, own in pages:
            rail = self._XW_RAIL_RE.search(self.draft_html[rel]).group(1)
            label, body = self._XW_RAIL_BLOCK_RE.findall(rail)[0]
            self.assertEqual(label, "Views", rel)
            links = self._XW_RAIL_LINK_RE.findall(body)
            self.assertEqual([(href, text) for href, _, text in links],
                             expected, f"{rel}: Views is All plus the topics")
            current = [href for href, attrs, _ in links
                       if 'aria-current="page"' in attrs]
            self.assertEqual(current, [own], f"{rel}: its own view is current")

    def test_crosswalk_row_header_column_sits_outside_every_preset(self):
        """Directive item 2 and spec 7.30: the row-header column carries no
        data-col, so no preset names it and matrix.js never hides it; every
        other header and cell carries its column's key; the crosswalk table
        is the page's one matrix, in its bounded scroll box (spec 7.31),
        with the status line above it; and without script the full table
        reads (no cell is hidden in the markup)."""
        main = self.draft_html["draft/crosswalk/index.html"]
        preset_keys = {k for _, keys, _, _ in self._XW_PRESET_RE.findall(main)
                       for k in keys.split()}
        for rel in self._xw_table_pages():
            html = self.draft_html[rel]
            table = self._xw_table(html)
            columns = self._XW_COL_RE.findall(table)
            self.assertNotRegex(table, r"\shidden\b",
                                f"{rel}: every column shows without script")
            self.assertIn('<caption class="vh">', table, rel)
            rows = self._XW_ROW_RE.findall(table)
            self.assertTrue(len(rows) > 1, rel)
            for index, row in enumerate(rows):
                cells = self._XW_CELL_RE.findall(row)
                tag, attrs, _ = cells[0]
                self.assertEqual(
                    (tag, attrs), ("th", ' scope="col"' if index == 0
                                   else ' scope="row"'),
                    f"{rel}: the row-header column carries no data-col")
                keys = [self._XW_DATA_COL_RE.search(a) for _, a, _ in
                        cells[1:]]
                self.assertTrue(all(keys), f"{rel}: every other cell has a "
                                "data-col key")
                self.assertEqual([k.group(1) for k in keys], columns, rel)
                if rel == "draft/crosswalk/index.html":
                    self.assertTrue(
                        {k.group(1) for k in keys} <= preset_keys,
                        "every keyed cell belongs to a preset")
        self.assertRegex(
            main, r'<p class="matrix-status" role="status" '
            r'aria-live="polite" data-matrix-status></p>\s*<div class="wide">'
            r'<div class="tablewrap bounded" tabindex="0">\s*<table '
            r'class="matrix sticky sticky-col" data-matrix>',
            "the status line sits above the page's one matrix")

    def test_crosswalk_table_sentences_hold_for_every_column(self):
        """Directive item 3 and the page prose rule: the sentences about the
        table are generated from the columns each page renders and checked
        against its rendered cells. A cell with no count link is empty on
        screen (round 4 item 3) and has no mapping in the model; a
        count-link cell lands on its instrument page at its domain;
        identifiers show only in the columns the compliance alignment matrix
        carries (wherever the model has any), and the other columns' cells
        carry the count alone. Round 4 item 1 checks which columns the
        sentences name."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        xw = self.mod.build_crosswalk(full)
        by_key = {i.key: i for i in self.mod.CROSSWALK_INSTRUMENTS}
        for rel in self._xw_table_pages():
            html = self.draft_html[rel]
            intro = self._xw_intro(html)
            columns = self._XW_COL_RE.findall(html)
            comp = [k for k in columns if by_key[k].compliance_column]
            self.assertIn(
                "A cell with a recorded mapping carries a generated document "
                "count that opens the instrument page at that domain, and a "
                "cell with none is left empty.", intro, rel)
            table = self._xw_table(html)
            for row in self._XW_ROW_RE.findall(table)[1:]:
                cells = self._XW_CELL_RE.findall(row)
                domain = re.search(r'href="/draft/([a-z-]+)/"',
                                   cells[0][2]).group(1)
                for (_, attrs, body), key in zip(cells[1:], columns):
                    entry = xw["instruments"][key]["by_domain"].get(domain)
                    where = f"{rel}: {key} x {domain}"
                    if body == self._XW_NO_DOCS:
                        self.assertIsNone(entry, where)
                        continue
                    self.assertIsNotNone(entry, where)
                    self.assertIn(
                        f'<a href="/draft/crosswalk/{key}/#{domain}">', body,
                        where)
                    shows_ids = "<code>" in body
                    single = [i for i in entry["ids"] if " " not in i]
                    if key in comp:
                        self.assertEqual(shows_ids, bool(single), where)
                    else:
                        self.assertFalse(shows_ids, f"{where}: count alone")
                    if key not in comp:
                        continue
                    # "the instrument page lists every identifier and label
                    # in full": each identifier the model records for the
                    # domain shows on the instrument page under its anchor.
                    page = self.draft_html[f"draft/crosswalk/{key}/index.html"]
                    section = re.search(
                        rf'<h3 id="{domain}">.*?</ul>', page, re.S).group(0)
                    for ident in entry["ids"]:
                        self.assertIn(self.mod._esc(ident), section, where)

    def test_crosswalk_views_sentences_hold_for_every_view(self):
        """The page prose rule on the Views sentences, checked against the
        rendered pages: the number of topic views equals the presets in the
        side list; "every column is in at least one topic" holds for the
        rendered presets; "the Domain column shows in every view" holds
        because the row-header column is outside every preset (test above);
        the clause that a topic can take columns from more than one group
        appears exactly when a rendered topic's columns sit under more than
        one group in the rendered side list, the clause that a column can
        sit in more than one topic exactly when a rendered column does, and
        the related pages clause exactly when a rendered view links related
        pages (qualified, since only some do); each Also in the corpus
        instrument the sentence counts has a rendered page and no column;
        and a view page's sentence names only what its side list holds (the
        other views, All among them, and every instrument)."""
        main = self.draft_html["draft/crosswalk/index.html"]
        presets = self._XW_PRESET_RE.findall(main)
        also = dict(self._xw_groups())[self._XW_ALSO]
        para = re.search(r"<p>(Each of the (\d+) topic views in the Views "
                         r"list .*?)</p>", main, re.S)
        self.assertIsNotNone(para, "the Views sentence on the crosswalk")
        text = para.group(1)
        self.assertEqual(int(para.group(2)), len(presets) - 1,
                         "the topic view count equals the rendered presets")
        self.assertIn(
            "shows the columns for one topic, and All shows every column; "
            "every column is in at least one topic, and the Domain column "
            "shows in every view.", text)
        columns = self._XW_COL_RE.findall(main)
        topic_keys = [keys.split() for _, keys, _, _ in presets[1:]]
        self.assertEqual({k for keys in topic_keys for k in keys},
                         set(columns), "every column is in a topic")
        rail = self._XW_RAIL_RE.search(main).group(1)
        group_of = {}
        for label, body in self._XW_RAIL_BLOCK_RE.findall(rail)[1:]:
            for href, _, _ in self._XW_RAIL_LINK_RE.findall(body):
                group_of[href.split("/")[-2]] = label
        spans = any(len({group_of[k] for k in keys}) > 1
                    for keys in topic_keys)
        flat = [k for keys in topic_keys for k in keys]
        shared = any(flat.count(k) > 1 for k in flat)
        related = any(
            self._XW_RELATED_RE.search(self.draft_html[_page_rel_for(href)])
            for href, _, _, _ in presets[1:])
        self.assertTrue(spans and shared and related,
                        "the corpus exercises every clause today")
        self.assertEqual(
            "A topic can take columns from more than one instrument group"
            in text, spans, "the spanning clause holds on the rendered pages")
        self.assertEqual(
            "a column can sit in more than one topic" in text.lower(), shared,
            "the shared column clause holds on the rendered pages")
        self.assertEqual(
            "which also links the topic's related instrument pages where it "
            "has any" in unescape(text), related,
            "the related pages clause holds on the rendered pages")
        self.assertIn("Without script every column shows here, All is a link "
                      "to this full table, and each topic view is a link to a "
                      "page with that topic's columns only", unescape(text))
        tail = re.search(
            r"Below the Views list, the group lists name every instrument "
            r"under its group, each linking its instrument page; the (\d+) "
            r"under Also in the corpus (?:has|have) a page and no column "
            r"until a matrix carries (?:it|them)\.$", text)
        self.assertIsNotNone(tail, text)
        self.assertEqual(int(tail.group(1)), len(also))
        for key in also:
            self.assertIn(f"draft/crosswalk/{key}/index.html", self.draft_html)
            self.assertNotIn(key, columns, f"{key} has no column")
        for preset in self.mod.CROSSWALK_TOPICS:
            view = self.draft_html[
                f"draft/crosswalk/view/{preset.slug}/index.html"]
            self.assertIn(
                "<p>The Views list opens the other views, All among them, "
                "and the group lists below it name every instrument under "
                "its group, each linking its instrument page.</p>", view,
                preset.slug)
            hrefs = set(_HREF_RE.findall(
                self._XW_RAIL_RE.search(view).group(1)))
            for other in self.mod.CROSSWALK_TOPICS:
                if other.slug != preset.slug:
                    self.assertIn(f"/draft/crosswalk/view/{other.slug}/",
                                  hrefs, preset.slug)
            self.assertIn("/draft/crosswalk/", hrefs, preset.slug)
            self.assertTrue(
                {f"/draft/crosswalk/{i.key}/"
                 for i in self.mod.CROSSWALK_INSTRUMENTS} <= hrefs,
                f"{preset.slug}: every instrument")

    # -- 31. crosswalk round 3 (site f2) ------------------------------------

    _XW_HEAD_RE = re.compile(
        r'<th scope="col" data-col="([a-z0-9-]+)">([^<]+)'
        r'<span class="org">([^<]+)</span></th>')
    _XW_COUNT_CELL_RE = re.compile(
        r"^(?:<code>[^<\s]+</code>(?:, <code>[^<\s]+</code>)*"
        r'(?:<span class="vh">, and more</span>)? )?'
        r'<a href="/draft/crosswalk/([a-z0-9-]+)/#([a-z-]+)">(\d+)'
        r'<span class="vh"> (documents?)</span></a>$')
    _XW_CAPTION_RE = re.compile(r'<caption class="vh">([^<]*)</caption>')

    def _xw_main_keys(self):
        return [i.key for i in self.mod.CROSSWALK_INSTRUMENTS if i.main_table]

    def _xw_views_text(self):
        main = self.draft_html["draft/crosswalk/index.html"]
        para = re.search(r"<p>(Each of the \d+ topic views in the Views "
                         r"list .*?)</p>", main, re.S)
        self.assertIsNotNone(para, "the Views sentence on the crosswalk")
        return unescape(" ".join(para.group(1).split()))

    def test_crosswalk_views_sentence_tells_all_from_the_topic_views(self):
        """Round 3 item 1 (ERROR): without script All opens the full table,
        and only a topic view opens a page with its topic's columns only.
        The sentence says so, checked against the side list's links and the
        pages they open: All is the crosswalk page itself, which renders
        every main-table column, and each topic link opens a page with
        exactly its preset's columns, fewer than the full table."""
        text = self._xw_views_text()
        self.assertIn(
            "Without script every column shows here, All is a link to this "
            "full table, and each topic view is a link to a page with that "
            "topic's columns only", text)
        self.assertNotIn("each view is a link to a page with that topic's "
                         "columns only", text, "All is no topic page")
        main = self.draft_html["draft/crosswalk/index.html"]
        self.assertIn('<link rel="canonical" '
                      'href="https://grclibrary.ai/draft/crosswalk/">', main)
        main_keys = self._xw_main_keys()
        self.assertEqual(self._XW_COL_RE.findall(main), main_keys,
                         "this page is the full table")
        presets = self._XW_PRESET_RE.findall(main)
        self.assertEqual(presets[0][:2], ("/draft/crosswalk/", ""),
                         "All links this full table")
        self.assertEqual(presets[0][3], "All")
        for href, keys, slug, _ in presets[1:]:
            view = self.draft_html[_page_rel_for(href)]
            shown = self._XW_COL_RE.findall(view)
            self.assertEqual(sorted(shown), sorted(keys.split()), slug)
            self.assertLess(len(shown), len(main_keys),
                            f"{slug}: a topic page holds its columns only")

    def test_crosswalk_side_list_sentences_name_the_lists_that_hold(self):
        """Round 3 item 2 (ERROR): the Views list holds only All and the
        topic views; the instruments sit in the group lists below it. On the
        crosswalk page and every view, no sentence says the Views list (or
        "the same list") names the instruments, a sentence says the group
        lists do, and the rendered side list bears both out."""
        instruments = {f"/draft/crosswalk/{i.key}/"
                       for i in self.mod.CROSSWALK_INSTRUMENTS}
        for rel in self._xw_table_pages():
            html = self.draft_html[rel]
            rail = self._XW_RAIL_RE.search(html).group(1)
            blocks = self._XW_RAIL_BLOCK_RE.findall(rail)
            self.assertEqual(blocks[0][0], "Views", rel)
            views = [h for h, _, _ in
                     self._XW_RAIL_LINK_RE.findall(blocks[0][1])]
            self.assertTrue(all(h == "/draft/crosswalk/"
                                or h.startswith("/draft/crosswalk/view/")
                                for h in views),
                            f"{rel}: the Views list holds All and the topic "
                            "views only")
            self.assertFalse(set(views) & instruments, rel)
            grouped = {h for _, body in blocks[1:]
                       for h, _, _ in self._XW_RAIL_LINK_RE.findall(body)}
            self.assertEqual(grouped, instruments,
                             f"{rel}: the group lists hold every instrument")
            main = html[html.index("<main"):html.index("</main>")]
            prose = unescape(" ".join(
                re.sub(r"<[^>]+>", " ", main.replace(rail, "")).split()))
            self.assertNotRegex(prose,
                                r"Views list[^.]*\bnames every instrument",
                                rel)
            self.assertNotIn("The same list names every instrument", prose,
                             rel)
            self.assertRegex(prose, r"the group lists (?:below it )?name "
                             r"every instrument under its group", rel)

    def test_disclosure_view_claim_matches_matrix_js(self):
        """Round 3 item 3 (WARN): the disclosure's ?view= clause says what
        matrix.js does, read from the served script and the rendered presets:
        on a topic view the script writes the chosen preset's data-preset-id
        (a short identifier, not the view's name), and on All, whose
        data-preset is empty, it removes the parameter. The example the
        clause gives is a topic preset's id on the rendered crosswalk."""
        page = self.draft_html["draft/disclosure/index.html"]
        claim = " ".join(self._disclosure_claim_parts(page))
        clause = re.search(
            r"When the reader chooses a crosswalk topic view, the matrix "
            r"script writes the view's short identifier \(for example, "
            r"([a-z0-9-]+)\) into the page address \(\?view=\) the same way, "
            r"and removes it from the address when the reader chooses All\.",
            claim)
        self.assertIsNotNone(clause, claim)
        main = self.draft_html["draft/crosswalk/index.html"]
        presets = {pid: (keys, unescape(label)) for _, keys, pid, label
                   in self._XW_PRESET_RE.findall(main)}
        example = clause.group(1)
        self.assertIn(example, presets, "the example is a rendered preset id")
        keys, label = presets[example]
        self.assertTrue(keys, "the example is a topic view with columns")
        self.assertNotEqual(label, example,
                            "the address takes the id, not the view's name")
        self.assertEqual([k for k, lbl in presets.values() if lbl == "All"],
                         [""], "All carries no column keys")
        js = self.draft_all["draft/assets/baseline/matrix.js"].decode("utf-8")
        # keys(p) reads data-preset, so All's k is empty; a preset with keys
        # writes its data-preset-id as ?view=, and All deletes the parameter
        # (writeAddress sets a key with a value and deletes an empty one).
        # From 1.7.0 the same call also clears ?cols= on a page with column
        # toggles; the crosswalk has none, so it writes ?view= alone, and
        # ?cols= is written only from the toggles (showSet).
        self.assertIn('return (p.getAttribute("data-preset") || "")', js)
        self.assertIn("var k = keys(p);", js)
        self.assertIn('var id = p.getAttribute("data-preset-id");', js)
        self.assertIn('writeAddress(toggles.length ? { view: k.length && id '
                      '? id : "", cols: "" } : { view: k.length && id ? id '
                      ': "" });', js)
        self.assertIn('if (set[k]) { s.set(k, set[k]); } else { '
                      's.delete(k); }', js)
        self.assertIn('var toggles = slice(document.querySelectorAll('
                      '"[data-col-toggles] button[data-col]"));', js)
        self.assertNotIn("data-col-toggles", main)

    def test_crosswalk_headers_and_cells_follow_spec_7_30(self):
        """Round 3 item 4 (WARN): spec 7.30 markup. A header is the name over
        its organization tag (the display name without the tag it opens
        with); a mapped cell holds its single-word identifiers in code type
        and a count link whose noun is visually hidden, the count equal to a
        recount; a phrase-length label never sits in a matrix cell, so a
        column with no single-word identifiers shows the count link alone."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        xw = self.mod.build_crosswalk(full)
        labels_seen = 0
        stripped = 0
        for rel in self._xw_table_pages():
            table = self._xw_table(self.draft_html[rel])
            self.assertNotIn('<span class="n">', table, rel)
            columns = self._XW_COL_RE.findall(table)
            heads = self._XW_HEAD_RE.findall(table)
            self.assertEqual([k for k, _, _ in heads], columns,
                             f"{rel}: every header takes the spec markup")
            for key, name, org in heads:
                # Round 4 item 2: the name is the display with the leading
                # organization and space removed whenever it opens with them,
                # else the whole display; the tag is the instrument's org.
                display = xw["instruments"][key]["display"]
                tag = self.mod.CROSSWALK_BY_KEY[key].org
                self.assertEqual(unescape(org), tag, f"{rel}: {key} tag")
                expected = display
                if display.startswith(tag + " "):
                    expected = display[len(tag) + 1:]
                    stripped += 1
                self.assertEqual(unescape(name), expected,
                                 f"{rel}: {key} header")
            for row in self._XW_ROW_RE.findall(table)[1:]:
                cells = self._XW_CELL_RE.findall(row)
                domain = re.search(r'href="/draft/([a-z-]+)/"',
                                   cells[0][2]).group(1)
                for (_, _, body), key in zip(cells[1:], columns):
                    where = f"{rel}: {key} x {domain}"
                    if body == self._XW_NO_DOCS:
                        continue
                    entry = xw["instruments"][key]["by_domain"][domain]
                    cell = self._XW_COUNT_CELL_RE.match(body)
                    self.assertIsNotNone(cell, f"{where}: {body}")
                    self.assertEqual(cell.group(1, 2), (key, domain), where)
                    count = int(cell.group(3))
                    self.assertEqual(count, len(entry["docs"]), where)
                    self.assertEqual(cell.group(4), "document" if count == 1
                                     else "documents", where)
                    codes = [unescape(c) for c in
                             re.findall(r"<code>([^<]*)</code>", body)]
                    self.assertTrue(set(codes) <= set(entry["ids"]), where)
                    for ident in entry["ids"]:
                        if len(ident.split()) > 1:
                            labels_seen += 1
                            self.assertNotIn(self.mod._esc(ident), body,
                                             f"{where}: a phrase-length label")
        self.assertTrue(labels_seen, "the corpus has phrase-length labels "
                        "today, so the label rule bites")
        self.assertTrue(stripped, "a display opens with its organization "
                        "today, so the prefix rule bites")

    def test_crosswalk_counts_name_their_scope(self):
        """Round 3 items 5 and 6 (WARN): matrix.js hides columns on the
        crosswalk page, so every count there names the full table (caption,
        label, meta, and the intro's column split); a static view's columns
        never change, so its split counts the columns here. Wherever a
        caption states a number, it equals the rendered data-col headers."""
        split_views = 0
        for rel in self._xw_table_pages():
            html = self.draft_html[rel]
            columns = self._XW_COL_RE.findall(self._xw_table(html))
            caption = self._XW_CAPTION_RE.search(html).group(1)
            for number in re.findall(r"\d+", caption):
                self.assertEqual(int(number), len(columns),
                                 f"{rel}: caption {caption!r}")
            intro = self._xw_intro(html)
            # Every column count in the sentences names its scope (round 4
            # names the columns, and keeps each count scoped), and so does
            # every column a sentence names alone (batch 3: "the PIP column
            # here"); the opening sentence's "a column of the compliance
            # alignment matrix" is the matrix's column, no column here.
            where = (" of the full table" if rel == "draft/crosswalk/index.html"
                     else " here")
            scopes = re.findall(r"(?:\b\d+ columns|(?<!\ba) column)\b"
                                r"( of the full table| here)?", intro)
            self.assertEqual(set(scopes), {where} if scopes else set(),
                             f"{rel}: every column count names its scope")
            if rel != "draft/crosswalk/index.html":
                if len(scopes) > 1:
                    split_views += 1
                continue
            n = len(self._xw_main_keys())
            self.assertEqual(len(columns), n)
            self.assertEqual(
                caption, f"Corpus domains by instruments, {n} in the full "
                "table")
            self.assertIn(f'<p class="lbl sec">The full table, {n} '
                          "instruments</p>", html)
            self.assertRegex(html, rf'<p class="meta">{n} instruments across '
                             r"\d+ domains in the full table, ")
            self.assertRegex(intro, r"In the \d+ columns of the full table "
                             r"for ")
        self.assertTrue(split_views, "a view splits its columns today")

    def test_crosswalk_view_columns_follow_the_full_table_order(self):
        """Round 3 item 7 (NOTE): matrix.js hides columns and never reorders
        them, so each static view lists its columns in the full table's
        order and agrees with the scripted view; at least one topic names
        its columns in another order, so the rule bites."""
        order = self._XW_COL_RE.findall(
            self.draft_html["draft/crosswalk/index.html"])
        reordered = False
        for topic in self.mod.CROSSWALK_TOPICS:
            shown = self._XW_COL_RE.findall(self.draft_html[
                f"draft/crosswalk/view/{topic.slug}/index.html"])
            self.assertEqual(shown, [k for k in order if k in topic.columns],
                             topic.slug)
            reordered = reordered or shown != list(topic.columns)
        self.assertTrue(reordered)

    def test_crosswalk_view_lead_says_all_opens_every_instrument_column(self):
        """Round 3 item 10 (NOTE): the Also in the corpus instruments have no
        column, so All opens every instrument column, not every instrument;
        each view's lead says so, and its All link opens a page rendering
        every main-table column."""
        also = dict(self._xw_groups())[self._XW_ALSO]
        self.assertTrue(also, "an instrument with no column exists")
        for topic in self.mod.CROSSWALK_TOPICS:
            html = self.draft_html[
                f"draft/crosswalk/view/{topic.slug}/index.html"]
            lead = re.search(r'<p class="lead">(.*?)</p>', html, re.S)
            self.assertTrue(lead.group(1).endswith(
                "The All link opens every instrument column."), topic.slug)
            rail = self._XW_RAIL_RE.search(html).group(1)
            self.assertIn('<li><a href="/draft/crosswalk/">All</a></li>', rail)
        self.assertEqual(
            self._XW_COL_RE.findall(
                self.draft_html["draft/crosswalk/index.html"]),
            self._xw_main_keys())

    # -- 32. crosswalk round 4 (site f2) ------------------------------------

    _XW_NO_DOCS = '<span class="vh">no documents</span>'
    _XW_MORE = '<span class="vh">, and more</span>'
    _XW_VH_RE = re.compile(r'<span class="vh">[^<]*</span>')
    _XW_VISIBLE_CELL_RE = re.compile(
        r"^(?:<code>[^<]+</code>(?:, <code>[^<]+</code>)* )?"
        r'<a href="/draft/crosswalk/[a-z0-9-]+/#[a-z-]+">\d+</a>$')

    def _xw_intro(self, html):
        intro = re.search(
            r'<h2 id="table">Domains by instruments</h2>\s*<p>(.*?)</p>',
            html, re.S)
        self.assertIsNotNone(intro, "the table sentences")
        return unescape(" ".join(intro.group(1).split()))

    def _xw_cells(self, html):
        """(column key, domain, cell body) for every data cell rendered."""
        table = self._xw_table(html)
        columns = self._XW_COL_RE.findall(table)
        for row in self._XW_ROW_RE.findall(table)[1:]:
            cells = self._XW_CELL_RE.findall(row)
            domain = re.search(r'href="/draft/([a-z-]+)/"',
                               cells[0][2]).group(1)
            for (_, _, body), key in zip(cells[1:], columns):
                yield key, domain, body

    @staticmethod
    def _xw_split_names(text):
        return re.split(r", and |, | and ", text)

    def test_crosswalk_sentences_name_the_columns_that_show_codes(self):
        """Round 4 item 1 (WARN): the identifier clause is generated from
        the columns that render a code, and checked against every rendered
        column of every table page. The columns a sentence names as showing
        codes are exactly those with a code in some rendered cell, and no
        cell shows more codes than the stated cap; the columns it names as
        recording phrase-length labels only show a count and no code, and
        their instrument page lists each label under its domain; the
        columns it names as having no mapping show no count; the remaining
        columns take their cells from the reverse crosswalk, show no code,
        and their instrument page carries its control areas. Every rendered
        column falls in exactly one class, and a page with no code column
        (the Trade view today) says nothing about code type."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        xw = self.mod.build_crosswalk(full)
        cap = self.mod.CROSSWALK_CELL_ID_CAP
        seen = {"codes": 0, "labels": 0, "unmapped": 0, "rest": 0,
                "no codes": 0, "single": 0}
        for rel in self._xw_table_pages():
            html = self.draft_html[rel]
            intro = self._xw_intro(html)
            columns = self._XW_COL_RE.findall(html)
            rail = self._XW_RAIL_RE.search(html).group(1)
            key_of = {unescape(name): href.split("/")[-2]
                      for href, _, name in self._XW_RAIL_LINK_RE.findall(rail)
                      if href.count("/") == 4}
            has_code = dict.fromkeys(columns, False)
            has_count = dict.fromkeys(columns, False)
            for key, domain, body in self._xw_cells(html):
                shown = body.count("<code>")
                self.assertLessEqual(shown, cap, f"{rel}: {key} x {domain}")
                has_code[key] = has_code[key] or bool(shown)
                has_count[key] = has_count[key] or "<a href=" in body
            codes = [k for k in columns if has_code[k]]
            unmapped = [k for k in columns if not has_count[k]]
            comp = [k for k in columns
                    if self.mod.CROSSWALK_BY_KEY[k].compliance_column]
            labels = [k for k in comp if has_count[k] and not has_code[k]]
            rest = [k for k in columns
                    if k not in codes + labels + unmapped]
            self.assertTrue(set(codes) <= set(comp), rel)
            where = (" of the full table"
                     if rel == "draft/crosswalk/index.html" else " here")

            def named(pattern, keys, label):
                match = re.search(pattern, intro)
                if not keys:
                    self.assertIsNone(match, f"{rel}: no {label} clause")
                    return None
                self.assertIsNotNone(match, f"{rel}: {label} in {intro}")
                # Batch 3 (f2 note): a one-column group names its column
                # directly ("the PIP column here"), never "the 1 column
                # here for PIP"; a larger group gives its count and names.
                if match.group(1) is None:
                    self.assertEqual(len(keys), 1, f"{rel}: {label} count")
                    names = [match.group(3)]
                    seen["single"] += 1
                else:
                    self.assertEqual(int(match.group(1)), len(keys),
                                     f"{rel}: {label} count")
                    self.assertGreater(len(keys), 1, f"{rel}: {label}")
                    names = self._xw_split_names(match.group(2))
                self.assertEqual([key_of.get(n) for n in names], keys,
                                 f"{rel}: {label} names {names}")
                seen[label] += 1
                return match

            # A names group never runs on into the next sentence.
            names = r"((?:(?!In the |No domain ).)+?)"
            cols = (rf"the (?:(\d+) columns{where} for {names}|"
                    rf"{names} column{where})")
            self.assertNotRegex(intro, r"\bthe 1 columns?\b", rel)
            match = named(
                rf"In {cols}, a cell also "
                r"shows, in code type, up to (\d+) of the single-word "
                r"identifiers "
                r"that the compliance alignment matrix records for its "
                r"domain, where it records any, and the instrument page lists "
                r"every identifier and label in full\.", codes, "codes")
            if match:
                self.assertEqual(int(match.group(4)), cap, rel)
            else:
                self.assertNotIn("code type", intro, rel)
                seen["no codes"] += 1
            named(
                rf"In {cols}, the compliance "
                r"alignment matrix records only phrase-length labels, so a "
                r"cell shows the count alone and the instrument page lists "
                r"the labels in full\.", labels, "labels")
            named(
                rf"No domain has a recorded mapping in {cols}, so every cell "
                r"there is empty\.",
                unmapped, "unmapped")
            tail = (r"cells from the documents the reverse framework control "
                    r"crosswalk cites, with the count alone, and the "
                    r"instrument page lists the control areas that crosswalk "
                    r"maps\.")
            if rest and len(rest) == len(columns):
                self.assertIn(f"Every column{where} takes its ",
                              intro, rel)
                self.assertRegex(intro, tail, rel)
                seen["rest"] += 1
            elif rest:
                split = re.search(
                    rf"The remaining (?:(\d+) columns{where} take their|"
                    rf"{names} column{where} takes its) {tail}", intro)
                self.assertIsNotNone(split, f"{rel}: {intro}")
                if split.group(1) is None:
                    self.assertEqual([key_of.get(split.group(2))], rest, rel)
                else:
                    self.assertEqual(int(split.group(1)), len(rest), rel)
                    self.assertGreater(len(rest), 1, rel)
                seen["rest"] += 1
            else:
                self.assertNotRegex(intro, tail, rel)
            for key in labels:
                page = self.draft_html[f"draft/crosswalk/{key}/index.html"]
                for domain, entry in xw["instruments"][key][
                        "by_domain"].items():
                    section = re.search(rf'<h3 id="{domain}">.*?</ul>',
                                        page, re.S).group(0)
                    for label in entry["ids"]:
                        self.assertGreater(len(label.split()), 1,
                                           f"{key}: phrase-length only")
                        self.assertIn(self.mod._esc(label), section, key)
            for key in rest:
                self.assertFalse(has_code[key], f"{rel}: {key} count alone")
                page = self.draft_html[f"draft/crosswalk/{key}/index.html"]
                self.assertRegex(
                    page, re.compile(
                        r'<h2 id="control-areas">.*?<tbody>\s*<tr><td>', re.S),
                    f"{key}: the instrument page lists control areas")
        self.assertTrue(all(seen.values()),
                        f"the corpus exercises every clause today: {seen}")

    def test_crosswalk_cells_show_only_codes_and_the_count_link(self):
        """Round 4 item 3 (NOTE, spec 7.30): an empty cell holds only a
        visually hidden "no documents", as the reference page marks it, and
        "and more" past the cap is visually hidden, so no cell shows n/a or
        "and more"; with the hidden text removed a mapped cell is its codes
        and the count link alone. "And more" is present exactly when the
        cell's single-word identifiers exceed the cap, which then shows the
        cap's number of codes. The sentence that a cell with none is left
        empty holds for every rendered cell."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        xw = self.mod.build_crosswalk(full)
        cap = self.mod.CROSSWALK_CELL_ID_CAP
        empty = capped = 0
        for rel in self._xw_table_pages():
            html = self.draft_html[rel]
            self.assertIn("and a cell with none is left empty.",
                          self._xw_intro(html), rel)
            for key, domain, body in self._xw_cells(html):
                where = f"{rel}: {key} x {domain}"
                entry = xw["instruments"][key]["by_domain"].get(domain)
                visible = self._XW_VH_RE.sub("", body)
                text = unescape(re.sub(r"<[^>]+>", "", visible))
                self.assertNotIn("n/a", text.lower(), where)
                self.assertNotIn("and more", text, where)
                if entry is None:
                    self.assertEqual(body, self._XW_NO_DOCS, where)
                    self.assertEqual(text, "", where)
                    empty += 1
                    continue
                self.assertRegex(visible, self._XW_VISIBLE_CELL_RE, where)
                short = [i for i in entry["ids"] if len(i.split()) == 1]
                more = len(short) > cap
                self.assertEqual(body.count(self._XW_MORE), int(more), where)
                if more:
                    self.assertEqual(body.count("<code>"), cap, where)
                    self.assertLess(body.index(self._XW_MORE),
                                    body.index("<a href="),
                                    f"{where}: before the count link")
                    capped += 1
        self.assertTrue(empty and capped,
                        "the corpus has empty and capped cells today")

    # -- 33. batch 3 integration (site f1 and f2 onto batch 2) -------------

    _XW_OPENING = (
        "Rows are the corpus domains and columns are instruments the "
        "alignment matrices carry, each as a column of the compliance "
        "alignment matrix or in a section of the reverse framework control "
        "crosswalk."
    )

    def test_type_filter_sentence_names_only_the_filters_that_narrow(self):
        """Batch 3 (f1 note, published text): a type page whose All
        Documents rows all sit in one area (Guides, Principles, SOPs and
        Specifications today) said the area chips narrow them, but with the
        type chosen every row carries that one area, so no area chip keeps
        fewer of them; the sentence names the text filter alone there and
        the area chips only where the rows span areas. Replayed on the
        rendered rows in each type's filter state: some area chip keeps a
        nonempty part of the rows exactly when the sentence names the area
        chips, and some word from a kept title keeps a nonempty part of them
        wherever the sentence names the text filter."""
        rows = self._index_replay_rows()
        _, block = self._facet_group("area")
        areas = [v for _, v, _, _ in self._FACET_CHIP_RE.findall(block) if v]
        seen = {"one area": 0, "areas": 0}
        for tp in self.figures["type_pages"]:
            found = self._TYPE_FILTER_RE.findall(
                self.draft_html[self._type_rel(tp["type"])])
            if not found:
                continue
            narrow = found[0][3]
            state = {"type": tp["slug"]}
            kept = _replay_search_js(rows, active=state)
            if len(kept) == 1:
                continue
            with self.subTest(type=tp["type"]):
                by_area = any(
                    0 < len(_replay_search_js(
                        rows, active={**state, "area": a})) < len(kept)
                    for a in areas)
                if by_area:
                    self.assertEqual(narrow, ", and the area chips holding "
                                     "any of them, and its text filter, "
                                     "narrow them further")
                    seen["areas"] += 1
                else:
                    self.assertEqual(len({r["tokens"]["area"][0]
                                          for r in kept}), 1)
                    self.assertEqual(narrow, ", and its text filter narrows "
                                     "them further")
                    seen["one area"] += 1
                words = {w for r in kept for w in r["title"].split()}
                self.assertTrue(any(
                    0 < len(_replay_search_js(rows, w, active=state))
                    < len(kept) for w in words),
                    "a word narrows the rows, as the sentence says")
        self.assertTrue(all(seen.values()),
                        f"the corpus exercises both forms today: {seen}")

    def test_type_filter_sentence_area_chips_are_available_at_the_type(self):
        """Adoption round-2 NOTE: from baseline 1.7.0 an area chip that would
        show no documents at ?type=<slug> is unavailable there, so "its area
        chips ... narrow them further" was false of every such chip. The
        sentence names "the area chips holding any of
        them". No test replays 1.7.0's count(); read from its source, it
        makes a chip that is not chosen available when some row holds both
        the type and the chip's area, and those rows are replayed with
        search.js 1.5.1 in each type's filter state: at least one area chip
        is available on every page using that wording, and each available
        one keeps fewer of the rows than the type does."""
        rows = self._index_replay_rows()
        _, block = self._facet_group("area")
        areas = [v for _, v, _, _ in self._FACET_CHIP_RE.findall(block) if v]
        named = 0
        for tp in self.figures["type_pages"]:
            found = self._TYPE_FILTER_RE.findall(
                self.draft_html[self._type_rel(tp["type"])])
            if not found or not found[0][3].startswith(
                    ", and the area chips holding any of them"):
                continue
            named += 1
            state = {"type": tp["slug"]}
            kept = _replay_search_js(rows, active=state)
            with self.subTest(type=tp["type"]):
                available = [
                    len(_replay_search_js(rows, active={**state, "area": a}))
                    for a in areas]
                available = [n for n in available if n]
                self.assertTrue(available, "an area chip is available")
                for n in available:
                    self.assertLess(n, len(kept), "the chip narrows the rows")
        self.assertTrue(named, "a type page names the area chips today")

    def test_crosswalk_opening_sentence_holds_for_every_column(self):
        """Batch 3 (f2 note, published text): "columns are instruments the
        alignment matrices map" was false for AICPA TSC, which no domain
        maps, on the full table and the Security view. The opening sentence
        now says what every column is, checked on every table page: each
        rendered column's instrument is a column of the compliance alignment
        matrix's pinned header or has a section in the parsed reverse
        framework control crosswalk, and a page with a column no domain maps
        (no count link in any of its cells) never says the matrices map its
        columns."""
        reverse = self.mod.parse_reverse_matrix(
            self.mod.CROSSWALK_REVERSE_MATRIX.read_text(encoding="utf-8"))
        unmapped_pages = []
        for rel in self._xw_table_pages():
            html = self.draft_html[rel]
            intro = self._xw_intro(html)
            self.assertTrue(intro.startswith(self._XW_OPENING + " "),
                            f"{rel}: {intro}")
            mapped = dict.fromkeys(self._XW_COL_RE.findall(html), False)
            for key, _, body in self._xw_cells(html):
                mapped[key] = mapped[key] or "<a href=" in body
            for key in mapped:
                inst = self.mod.CROSSWALK_BY_KEY[key]
                self.assertTrue(
                    inst.compliance_column
                    in self.mod.CROSSWALK_COMPLIANCE_COLUMNS
                    or inst.reverse_section in reverse,
                    f"{rel}: {key} is in neither matrix")
            if not all(mapped.values()):
                unmapped_pages.append(rel)
                self.assertNotIn("instruments the alignment matrices map",
                                 intro, rel)
        self.assertIn("draft/crosswalk/index.html", unmapped_pages)
        self.assertIn("draft/crosswalk/view/security/index.html",
                      unmapped_pages,
                      "the Security view carries the column no domain maps")

    def test_crosswalk_one_column_groups_name_their_column(self):
        """Batch 3 (f2 note): a one-column group read "the 1 column here for
        PIP"; the sentence names the column directly ("the PIP column
        here"). On every table page no sentence counts one column, and each
        column a sentence names alone is one of the page's rendered columns
        under its display name; some page names one today."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        xw = self.mod.build_crosswalk(full)
        named = 0
        for rel in self._xw_table_pages():
            html = self.draft_html[rel]
            intro = self._xw_intro(html)
            self.assertNotRegex(intro, r"(?<![\w.])1 columns?\b", rel)
            where = (" of the full table"
                     if rel == "draft/crosswalk/index.html" else " here")
            displays = {xw["instruments"][k]["display"]
                        for k in self._XW_COL_RE.findall(html)}
            for name in re.findall(
                    r"(?:\bIn the |\bmapping in the |\bThe remaining )"
                    rf"((?:(?!\. ).)+?) column{re.escape(where)}\b", intro):
                self.assertIn(name, displays, f"{rel}: {name}")
                named += 1
        self.assertTrue(named, "some page names a one-column group today")

    def test_crosswalk_hidden_tail_never_runs_into_the_count(self):
        """Batch 3 (f2 note): the visually hidden ", and more" ran into the
        count link's text, so read aloud a cell said "more22"; a space
        follows the hidden span (batch 3 round 2: a plain space outside it,
        test_crosswalk_codes_and_count_link_are_spaced_in_every_cell). On
        every capped cell of every table page
        the cell's text, hidden text included, ends ", and more N
        document(s)", a space before the count."""
        capped = 0
        for rel in self._xw_table_pages():
            for key, domain, body in self._xw_cells(self.draft_html[rel]):
                text = unescape(re.sub(r"<[^>]+>", "", body))
                if "and more" not in text:
                    continue
                capped += 1
                self.assertRegex(text, r", and more \d+ documents?$",
                                 f"{rel}: {key} x {domain}")
        self.assertTrue(capped, "the corpus has capped cells today")

    # -- 34. batch 3 round 2 ------------------------------------------------

    _TYPE_ADOPTER_LBL_RE = re.compile(
        r'<p class="lbl blk">([^<]*), (\d+)</p>\s*<p>[^<]*</p>\s*'
        r'<div class="wide"><ul class="plan one described">(.*?)</ul>', re.S)

    def test_type_filter_sentence_names_its_scope_after_the_adopter_block(self):
        """Batch 3 round 2 WARN (published text): on a type page with
        adopter documents the All Documents sentence came straight after the
        adopter block and said "the 3 of these in a corpus area", so "these"
        read as the adopter documents. Read off every rendered type page
        with an adopter block: the sentence follows the block, never says
        "these", and names its part of the page's whole, the corpus-area
        rows out of the page's own document count, which is the corpus list
        and the adopter list together."""
        label = self.mod.draft_domain_label(self.mod.ADOPTER_DOCS_AREA)
        seen = 0
        for tp in self.figures["type_pages"]:
            page = self.draft_html[self._type_rel(tp["type"])]
            block = self._TYPE_ADOPTER_LBL_RE.search(page)
            if block is None or unescape(block.group(1)) != label:
                continue
            found = self._TYPE_FILTER_RE.search(page)
            if found is None:
                continue
            with self.subTest(type=tp["type"]):
                seen += 1
                held = found.group(3)
                in_index = [href for href, _, _, _
                            in self._type_corpus_rows(page)
                            if not href.startswith(self.mod.GITHUB_BLOB_BASE)]
                adopters = self._TYPE_ROW_RE.findall(block.group(3))
                total = int(re.search(r'<p class="lbl sec">Documents, '
                                      r'(\d+)</p>', page).group(1))
                self.assertEqual(int(block.group(2)), len(adopters))
                self.assertEqual(total, len(self._type_corpus_rows(page))
                                 + len(adopters))
                self.assertLess(block.end(), found.start(),
                                "the sentence follows the adopter block")
                self.assertNotIn("these", held)
                part = ("one" if len(in_index) == 1 else str(len(in_index)))
                verb = "sits" if len(in_index) == 1 else "sit"
                self.assertEqual(
                    held, f"the {part} of this page's {total} documents that "
                    f"{verb} in a corpus area")
        self.assertTrue(seen, "a type page with adopter documents and an All "
                        "Documents sentence exists today")

    _XW_CAVEATS_RE = re.compile(
        r'<h2 id="caveats">What this mapping is</h2>\s*<div class="callout">'
        r"(.*?)</div>", re.S)
    _XW_TSC_CAVEAT = (
        "Its AICPA TSC 2017 column is being populated domain by domain: "
        "until a document's Trust Services Criteria mapping has been "
        "assessed, its N/A in that column records that no mapping has been "
        "made yet and does not assert that no criterion applies. The table "
        "here leaves an AICPA TSC cell empty where every document the matrix "
        "lists for the domain has N/A in that column."
    )

    def _xw_all_pages(self):
        return self._xw_table_pages() + [
            f"draft/crosswalk/{i.key}/index.html"
            for i in self.mod.CROSSWALK_INSTRUMENTS]

    def test_crosswalk_tsc_caveat_only_where_the_table_has_the_column(self):
        """Batch 3 round 2 NOTE (published text): the caveat "In the AICPA
        TSC column, an N/A records ..." sat on all 29 crosswalk pages,
        though since f2 no cell shows N/A and most of those pages have no
        such column. On every crosswalk page the caveat renders exactly
        when the page's table has the AICPA TSC column, and the old N/A
        wording renders nowhere; the Trade view and the instrument pages,
        whose tables have no such column, carry the other caveats only, the
        AICPA TSC instrument page apart, which carries its own caveat (batch
        3 round 3 item 2,
        test_crosswalk_tsc_instrument_page_carries_its_own_caveat)."""
        tsc = [i.key for i in self.mod.CROSSWALK_INSTRUMENTS
               if i.compliance_column == "AICPA TSC 2017"]
        self.assertEqual(len(tsc), 1, "one AICPA TSC column")
        own = f"draft/crosswalk/{tsc[0]}/index.html"
        with_col = without = 0
        for rel in self._xw_all_pages():
            html = self.draft_html[rel]
            caveats = self._XW_CAVEATS_RE.search(html)
            self.assertIsNotNone(caveats, rel)
            text = unescape(" ".join(
                re.sub(r"<[^>]+>", "", caveats.group(1)).split()))
            self.assertNotIn("an N/A records", text, rel)
            has_col = tsc[0] in self._XW_COL_RE.findall(html)
            self.assertEqual(self._XW_TSC_CAVEAT in text, has_col, rel)
            self.assertEqual("AICPA" in text, has_col or rel == own, rel)
            with_col += has_col
            without += not has_col
        self.assertTrue(with_col and without, "pages of both kinds today")

    def test_crosswalk_tsc_caveat_holds_for_every_tsc_cell(self):
        """Batch 3 round 2 NOTE: the caveat describes what the reader sees,
        so it is checked against the rendered cells and its source. On every
        page carrying it, each AICPA TSC cell is empty (only the visually
        hidden "no documents") exactly where every document of its domain
        has N/A in the compliance alignment matrix's AICPA TSC 2017 column;
        no cell shows N/A; and the matrix itself states that the column is
        populated domain by domain and that its N/A records no mapping
        made yet."""
        source = self.mod.CROSSWALK_COMPLIANCE_MATRIX.read_text(
            encoding="utf-8")
        flat = " ".join(source.split())
        self.assertIn("The AICPA TSC 2017 column is being populated domain by "
                      "domain", flat)
        self.assertIn('its "N/A" in that column records that no mapping has '
                      "been made yet and does not assert that no criterion "
                      "applies", flat)
        _, rows = self.mod.parse_compliance_matrix(source)
        tsc = [i.key for i in self.mod.CROSSWALK_INSTRUMENTS
               if i.compliance_column == "AICPA TSC 2017"][0]
        cells = 0
        for rel in self._xw_table_pages():
            html = self.draft_html[rel]
            if self._XW_TSC_CAVEAT not in unescape(" ".join(html.split())):
                continue
            for key, domain, body in self._xw_cells(html):
                if key != tsc:
                    continue
                cells += 1
                all_na = all(r["cells"]["AICPA TSC 2017"] == "N/A"
                             for r in rows[domain])
                self.assertEqual(body == self._XW_NO_DOCS, all_na,
                                 f"{rel}: {domain}")
                self.assertNotIn("N/A", body, f"{rel}: {domain}")
        self.assertTrue(cells, "some page carries the caveat and the column")

    def test_crosswalk_codes_and_count_link_are_spaced_in_every_cell(self):
        """Batch 3 round 2 NOTE (accessibility): in a cell under the cap the
        last code sat directly against the count link, so read aloud it ran
        into the count ("A.622"). In every cell that shows a code, capped or
        not, on every table page, a plain space outside any visually hidden
        span sits directly before the count link, and the cell's text,
        hidden text included, has a space before the count."""
        capped = uncapped = 0
        for rel in self._xw_table_pages():
            for key, domain, body in self._xw_cells(self.draft_html[rel]):
                if "<code>" not in body:
                    continue
                where = f"{rel}: {key} x {domain}"
                self.assertRegex(body, r'(?:</code>|</span>) <a href=', where)
                text = unescape(re.sub(r"<[^>]+>", "", body))
                self.assertRegex(text, r"\S \d+ documents?$", where)
                if self._XW_MORE in body:
                    capped += 1
                else:
                    uncapped += 1
        self.assertTrue(capped and uncapped,
                        "the corpus has capped and uncapped code cells today")

    # -- 35. batch 3 round 3 ------------------------------------------------

    def _xw_caveat_text(self, html):
        caveats = self._XW_CAVEATS_RE.search(html)
        self.assertIsNotNone(caveats, "the What this mapping is block")
        return unescape(" ".join(
            re.sub(r"<[^>]+>", "", caveats.group(1)).split()))

    def test_crosswalk_tsc_caveat_names_the_rows_the_matrix_lists(self):
        """Batch 3 round 3 item 1 (WARN, published text): the caveat said a
        cell is empty "where every document of the domain has N/A", but a
        cell is empty where every row the compliance alignment matrix lists
        for the domain is N/A, and the matrix lists only some of most
        domains' documents (ai 45 of 65). Checked against the matrix rows
        and each domain's document count: every row of a domain section is
        a document of that domain, some domain has documents the matrix does
        not list (so the unscoped wording is false today), each AICPA TSC
        cell is empty exactly where every listed row is N/A, and every page
        whose table has the column says "every document the matrix lists
        for the domain" and never "every document of the domain"."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        domain_of = {d["path"]: d.get("domain") for d in full}
        counts = Counter(domain_of.values())
        domains, rows = self.mod.parse_compliance_matrix(
            self.mod.CROSSWALK_COMPLIANCE_MATRIX.read_text(encoding="utf-8"))
        unlisted = []
        for domain in domains:
            paths = {r["path"] for r in rows[domain]}
            for path in sorted(paths):
                self.assertEqual(domain_of.get(path), domain,
                                 f"{domain} section lists {path}")
            self.assertLessEqual(len(paths), counts[domain], domain)
            if len(paths) < counts[domain]:
                unlisted.append(domain)
        self.assertTrue(unlisted, "the matrix leaves out documents of some "
                        "domain today, so the scope must be stated")
        tsc = [i.key for i in self.mod.CROSSWALK_INSTRUMENTS
               if i.compliance_column == "AICPA TSC 2017"][0]
        pages = cells = 0
        for rel in self._xw_table_pages():
            html = self.draft_html[rel]
            if tsc not in self._XW_COL_RE.findall(html):
                continue
            pages += 1
            text = self._xw_caveat_text(html)
            self.assertIn(
                "The table here leaves an AICPA TSC cell empty where every "
                "document the matrix lists for the domain has N/A in that "
                "column.", text, rel)
            self.assertNotIn("every document of the domain", text, rel)
            for key, domain, body in self._xw_cells(html):
                if key != tsc:
                    continue
                cells += 1
                all_na = all(r["cells"]["AICPA TSC 2017"] == "N/A"
                             for r in rows[domain])
                self.assertEqual(body == self._XW_NO_DOCS, all_na,
                                 f"{rel}: {domain}")
        self.assertTrue(pages and cells, "some page has the column today")

    def test_crosswalk_tsc_instrument_page_carries_its_own_caveat(self):
        """Batch 3 round 3 item 2 (WARN, published text): round 2 moved the
        AICPA TSC caveat to the tables with that column, so the AICPA TSC
        instrument page lost its only word that the column is being
        populated. That page's compliance alignment matrix caveat says so and
        how many of the column's rows are N/A today, recounted here from the
        matrix; no other crosswalk page, view or instrument page, carries
        that sentence; and the generator words it from the counts, so a
        partly filled column and a filled one each get a sentence true for
        them.

        Batch 3 round 4 item 1 (WARN, published text): the sentence keeps the
        matrix's condition, that an N/A records no mapping yet only until the
        row's mapping has been assessed, and says the column is being
        populated only while the matrix's own text says so, never because
        some N/A remains. Once the matrix drops that sentence (every row
        assessed), an N/A there means no direct mapping, as in every other
        column, and the page says nothing of its own about it."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        source = self.mod.CROSSWALK_COMPLIANCE_MATRIX.read_text(
            encoding="utf-8")
        domains, rows = self.mod.parse_compliance_matrix(source)
        column = [r["cells"]["AICPA TSC 2017"]
                  for domain in domains for r in rows[domain]]
        na = sum(cell == "N/A" for cell in column)
        self.assertEqual(na, len(column), "every row is N/A today")
        populated = (
            "Its AICPA TSC 2017 column is being populated domain by domain: ")
        condition = (
            " N/A in that column today; until a row's Trust Services Criteria "
            "mapping has been assessed, its N/A in that column records that "
            "no mapping has been made yet and does not assert that no "
            "criterion applies."
        )
        sentence = (
            f"{populated}every one of its {len(column)} rows is{condition}")
        tsc = [i for i in self.mod.CROSSWALK_INSTRUMENTS
               if i.compliance_column == "AICPA TSC 2017"][0]
        own = f"draft/crosswalk/{tsc.key}/index.html"
        for rel in self._xw_all_pages():
            text = self._xw_caveat_text(self.draft_html[rel])
            self.assertEqual(sentence in text, rel == own, rel)
            self.assertEqual("in that column today" in text, rel == own, rel)
        # The sentence sits in the paragraph attributed to the compliance
        # alignment matrix, whose "Its" it continues.
        title = next(d["title"] for d in full
                     if d["path"] == self.mod.CROSSWALK_COMPLIANCE_MATRIX_PATH)
        para = re.search(
            r"<p>From the <a [^>]*>([^<]*)</a>: citations are indicative"
            r"(.*?)</p>", self.draft_html[own], re.S)
        self.assertIsNotNone(para, "the compliance alignment matrix caveat")
        self.assertEqual(unescape(para.group(1)), title)
        self.assertIn(sentence, unescape(" ".join(para.group(2).split())))

        xw = self.mod.build_crosswalk(full)
        data = xw["instruments"][tsc.key]
        self.assertEqual((data["column_rows"], data["column_na"]),
                         (len(column), na))
        # "Being populated" comes from the matrix's text: the matrix says so
        # today, and without its sentence it does not, whatever the counts.
        self.assertTrue(data["column_populating"])
        self.assertTrue(self.mod.parse_compliance_tsc_status(source))
        self.assertIn(" " + self.mod.CROSSWALK_TSC_POPULATING, source)
        self.assertFalse(self.mod.parse_compliance_tsc_status(
            source.replace(" " + self.mod.CROSSWALK_TSC_POPULATING, "")))
        with self.assertRaises(self.mod.BuildError):
            self.mod.parse_compliance_tsc_status(source.replace(
                self.mod.CROSSWALK_TSC_POPULATING,
                "The AICPA TSC 2017 column has been assessed."))
        self.assertFalse(any(
            other["column_populating"] for key, other in
            xw["instruments"].items() if key != tsc.key))
        rows_n = len(column)
        cases = (
            # The matrix says the column is being populated: all N/A,
            # partly filled (one N/A and several), and no N/A left.
            (True, rows_n, f"{populated}every one of its {rows_n} rows is"
             f"{condition}"),
            (True, rows_n - 1, f"{populated}{rows_n - 1} of its {rows_n} rows "
             f"are{condition}"),
            (True, 1, f"{populated}1 of its {rows_n} rows is{condition}"),
            (True, 0, f"{populated}none of its {rows_n} rows is{condition}"),
            # Every row assessed, so the matrix no longer says so: N/A
            # means no direct mapping, and the page claims neither.
            (False, rows_n, None),
            (False, rows_n - 1, None),
            (False, 0, None),
        )
        for populating, left, expected in cases:
            data["column_populating"] = populating
            data["column_na"] = left
            text = unescape(" ".join(re.sub(
                r"<[^>]+>", "",
                self.mod.render_crosswalk_caveats(xw, inst=tsc)).split()))
            case = f"populating {populating}, {left} N/A"
            if expected:
                self.assertIn(expected, text, case)
                self.assertEqual(text.count("AICPA"), 1, case)
            else:
                self.assertNotIn("AICPA", text, case)
                self.assertNotIn("being populated", text, case)
                self.assertNotIn("no mapping has been made yet", text, case)

    _YOUR_BROWSER = (
        '<p class="lbl blk">Your browser</p>\n'
        "<p>If you use the light and dark switch, your choice is kept in "
        "your browser's local storage under the name scheme, so the site "
        "opens in that scheme next time. It is not sent to this site, and "
        "nothing is stored until you press the switch.</p>\n"
        '<p class="lbl blk">Security</p>'
    )

    def test_disclosure_your_browser_paragraph_and_storage_claims_agree(self):
        """Batch 3 round 3 item 3 (template owner notice, owner-approved
        2026-11-03 21:25Z; baseline 1.6.1 SPECIFICATION.md section 7.20 and
        reference/disclosure.html): the "Your browser" paragraph sits under
        its label, word for word as the reference page shows it, after the
        entries and directly before the Security label. Every sentence on
        the page about cookies or storage is pinned, and they agree with it
        and with scheme.js: each names the storage key scheme.js uses, each
        says nothing is stored before the switch is pressed, no sentence
        says the site stores nothing in the browser (spec 7.20: inaccurate
        from 1.6.0), and scheme.js sets no cookie and makes no request, so
        the choice is not sent to this site."""
        page = self.draft_html["draft/disclosure/index.html"]
        self.assertEqual(page.count(self._YOUR_BROWSER), 1)
        self.assertEqual(page.count("Your browser"), 1)
        at = page.index(self._YOUR_BROWSER)
        entry = page.index('<h2 id="d-6">')
        self.assertLess(page.index("<p><strong>Evidence:</strong>", entry), at,
                        "the paragraph follows the last entry")
        self.assertEqual(re.findall(r'<h2 id="(d-\d+)">', page[at:]), [],
                         "no entry follows the paragraph")

        main = page[page.index("<main"):page.index("</main>")]
        paragraphs = [unescape(" ".join(re.sub(r"<[^>]+>", "", p).split()))
                      for p in re.findall(r"<p\b[^>]*>(.*?)</p>", main, re.S)]
        text = " ".join(paragraphs)
        sentences = [s for p in paragraphs
                     for s in re.split(r"(?<=\.)\s+(?=[A-Z])", p)
                     if re.search(r"\bstor|\bcookie", s, re.I)]
        self.assertEqual(sentences, [
            "Its own scripts are same-origin files that make no network "
            "requests and use no cookies.",
            "The light and dark switch is the one script that uses browser "
            "storage: when the reader presses the switch, it saves the chosen "
            "scheme, the word light or dark, in the browser's local storage "
            'under the key "scheme", so later pages open in that scheme.',
            "It stores nothing else, and nothing until the switch is pressed.",
            "If you use the light and dark switch, your choice is kept in "
            "your browser's local storage under the name scheme, so the site "
            "opens in that scheme next time.",
            "It is not sent to this site, and nothing is stored until you "
            "press the switch.",
        ])
        scheme = self.draft_all["draft/assets/baseline/scheme.js"].decode(
            "utf-8")
        key = re.search(r'var KEY = "(\w+)";', scheme).group(1)
        self.assertEqual(
            re.findall(r'under the (?:key|name) "?([\w-]+)"?', text),
            [key, key], "both statements name the key scheme.js uses")
        self.assertIn("nothing until the switch is pressed", text)
        self.assertIn("nothing is stored until you press the switch", text)
        for claim in (r"\bno (?:browser|local) storage\b",
                      r"\bstores? nothing\b(?! else)",
                      r"\bnothing is stored\b(?! until)",
                      r"\buses? no (?:browser )?storage\b"):
            self.assertNotRegex(text, claim, "the site stores the scheme")
        for api in ("document.cookie", "fetch(", "XMLHttpRequest",
                    "sendBeacon", "WebSocket", "EventSource"):
            self.assertNotIn(api, scheme, f"scheme.js uses {api}")

    # -- 36. batch 3 round 5 ------------------------------------------------

    @staticmethod
    def _xw_text(html):
        return unescape(" ".join(re.sub(r"<[^>]+>", "", html).split()))

    def test_crosswalk_tsc_view_caveat_follows_the_matrix_status(self):
        """Batch 3 round 5 item 2 (NOTE, published text): a view page whose
        table has the AICPA TSC column said the column "is being populated
        domain by domain" whatever the matrix said, while the instrument page
        followed the matrix. The view sentence renders on the same parsed
        status: on the rendered pages today (the matrix carries its sentence)
        and on a crosswalk built from the matrix with that sentence removed,
        a view page and the AICPA TSC instrument page each say "being
        populated" and "no mapping has been made yet" exactly when the matrix
        does, and the view page keeps the sentence on its empty cells."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        source = self.mod.CROSSWALK_COMPLIANCE_MATRIX.read_text(
            encoding="utf-8")
        pinned = self.mod.CROSSWALK_TSC_POPULATING
        self.assertIn(" " + pinned, source)
        tsc = [i for i in self.mod.CROSSWALK_INSTRUMENTS
               if i.compliance_column == "AICPA TSC 2017"][0]
        table = (
            "The table here leaves an AICPA TSC cell empty where every "
            "document the matrix lists for the domain has N/A in that column."
        )
        xw = self.mod.build_crosswalk(full)
        # The generator's view caveat is what the rendered pages carry.
        pages = 0
        keys = None
        for rel in self._xw_table_pages():
            html = self.draft_html[rel]
            cols = [k for k in self._XW_COL_RE.findall(html)
                    if k in self.mod.CROSSWALK_BY_KEY]
            if tsc.key not in cols:
                continue
            pages += 1
            keys = cols
            self.assertEqual(
                self._xw_caveat_text(html),
                self._xw_text(self.mod.render_crosswalk_caveats(xw, cols)),
                rel)
        self.assertTrue(pages, "some page has the column today")
        with tempfile.TemporaryDirectory() as tmp:
            doctored = Path(tmp) / "matrix.md"
            doctored.write_text(source.replace(" " + pinned, ""),
                                encoding="utf-8")
            saved = self.mod.CROSSWALK_COMPLIANCE_MATRIX
            self.mod.CROSSWALK_COMPLIANCE_MATRIX = doctored
            try:
                bare = self.mod.build_crosswalk(full)
            finally:
                self.mod.CROSSWALK_COMPLIANCE_MATRIX = saved
        for populating, model in ((True, xw), (False, bare)):
            self.assertEqual(
                model["instruments"][tsc.key]["column_populating"], populating)
            view = self._xw_text(self.mod.render_crosswalk_caveats(
                model, keys))
            own = self._xw_text(self.mod.render_crosswalk_caveats(
                model, inst=tsc))
            for phrase in ("being populated", "no mapping has been made yet"):
                case = f"populating {populating}: {phrase}"
                self.assertEqual(phrase in view, populating, case)
                self.assertEqual(phrase in own, populating, case)
            self.assertIn(table, view, f"populating {populating}")
        for rel in self._xw_table_pages():
            text = self._xw_caveat_text(self.draft_html[rel])
            self.assertEqual("being populated" in text,
                             self._XW_TSC_CAVEAT in text, rel)

    def test_crosswalk_tsc_instrument_caveat_one_row_forms(self):
        """Batch 3 round 5 item 3 (NOTE, published text): a one-row column
        with no N/A read "none of its 1 rows is". The single-row form, as
        the all-N/A branch has, renders for a one-row column in both states
        of that row, and the plural forms stay for several rows."""
        full = self.mod.parse_taxonomy_full(
            self.mod.TAXONOMY.read_text(encoding="utf-8"))
        tsc = [i for i in self.mod.CROSSWALK_INSTRUMENTS
               if i.compliance_column == "AICPA TSC 2017"][0]
        xw = self.mod.build_crosswalk(full)
        data = xw["instruments"][tsc.key]
        data["column_populating"] = True
        cases = (
            (1, 0, "its one row is not N/A in that column today;"),
            (1, 1, "its one row is N/A in that column today;"),
            (2, 0, "none of its 2 rows is N/A in that column today;"),
            (2, 2, "every one of its 2 rows is N/A in that column today;"),
        )
        for rows, na, expected in cases:
            data["column_rows"], data["column_na"] = rows, na
            text = self._xw_text(self.mod.render_crosswalk_caveats(
                xw, inst=tsc))
            case = f"{na} of {rows} N/A"
            self.assertIn(expected, text, case)
            self.assertNotIn("of its 1 rows", text, case)
            self.assertNotIn("its 1 rows", text, case)

    # -- 37. batch 3 round 6 ------------------------------------------------

    def test_crosswalk_tsc_status_is_an_exact_pin_of_the_reading_guide(self):
        """Batch 3 round 6 item 1 (WARN, design fix): rounds 4 and 5 read the
        AICPA TSC 2017 column's status by matching phrases, and each review
        found a rewording that slipped through. The status is read from the
        matrix's reading-guide paragraph alone, the first paragraph after the
        framework column key table, and that paragraph must be exactly one
        of two forms: with CROSSWALK_TSC_POPULATING (being populated) or
        with exactly that sentence removed (not). On the matrix, each form
        parses with its status, and each of these fails the build with a
        message naming the paragraph and both forms: a reworded status
        sentence, the sentence moved within the paragraph, an extra sentence
        in either form, another sentence of the paragraph reworded, the
        paragraph reflowed onto two lines or missing, and the key table
        missing or repeated.

        Batch 3 round 6 item 2 (NOTE): no phrase is matched any more, so an
        unrelated "populated" elsewhere in the matrix ("Every CTPAT cell is
        populated for logistics rows.") leaves the build passing with the
        paragraph's status.

        Batch 3 follow-up items 1 to 3 (WARN): the paragraph was read only up
        to its first blank line, so the status sentence moved into a
        paragraph of its own after it (probe A04), or replaced by a reworded
        one there (probe A05), passed with the status False.

        Batch 3 follow-up round 2 item 1 (WARN): round 1 still passed with
        the status False when the sentence moved before the key table or
        into another key row. The whole "How to use this matrix" section is
        pinned in its two forms, and every refusal names the matrix file.
        Refused in the section: either probe, nothing after the paragraph,
        no blank line between the key table and the paragraph, and the
        sentence moved into the intro paragraph, into a paragraph of its own
        above the key list (also reworded), into the AICPA TSC 2017 key row
        or another key row, or into a new key row, or that row missing, or
        the section heading reworded or repeated.
        Refused outside it: the exact sentence after the section's ---, in
        Notes (also reflowed over two lines), in the document header, at the
        end of the file, and as a second copy beside the current one. Not
        refused, a disclosed limit: a reworded status after the section's
        --- or in Notes passes with the status False."""
        source = self.mod.CROSSWALK_COMPLIANCE_MATRIX.read_text(
            encoding="utf-8")
        guide = self.mod.CROSSWALK_TSC_READING_GUIDE
        pinned = self.mod.CROSSWALK_TSC_POPULATING
        current = f"{guide} {pinned}"
        self.assertEqual(source.count(f"\n\n{current}\n\n"), 1)
        bare = source.replace(current, guide)
        notes = "## Notes\n\n"
        self.assertEqual(source.count(notes), 1)
        ctpat = "Every CTPAT cell is populated for logistics rows."
        reworded = ("The AICPA TSC 2017 mappings are being filled in domain "
                    "by domain.")
        divider = "---\n\n## Notes"
        self.assertEqual(source.count(divider), 1)
        accepted = (
            ("current paragraph", source, True),
            ("sentence removed", bare, False),
            ("CTPAT populated, current",
             source.replace(notes, f"{notes}{ctpat}\n\n"), True),
            ("CTPAT populated, sentence removed",
             bare.replace(notes, f"{notes}{ctpat}\n\n"), False),
            ("CTPAT populated at the end", f"{source}\n{ctpat}\n", True),
            # Disclosed limit, not a requirement: a reworded status outside
            # the pinned section is not read.
            ("reworded status after the section's ---",
             bare.replace(divider, f"---\n\n{reworded}\n\n## Notes"), False),
            ("reworded status in Notes",
             bare.replace(notes, f"{notes}{reworded}\n\n"), False),
        )
        for case, text, status in accepted:
            with self.subTest(case=case):
                self.assertIs(self.mod.parse_compliance_tsc_status(text),
                              status)

        first, rest = guide.split(". ", 1)
        key = "| Column | Framework | Reference Basis |"
        self.assertEqual(source.count(key), 1)
        refused = (
            ("mappings being filled in", current.replace(
                pinned, "The AICPA TSC 2017 mappings are being filled in "
                "domain by domain.")),
            ("2017 dropped", current.replace(
                "AICPA TSC 2017 column", "AICPA TSC column")),
            ("sentence moved first", f"{pinned} {guide}"),
            ("sentence moved second", f"{first}. {pinned} {rest}"),
            ("extra sentence, current",
             f"{current} The AICPA TSC column is being populated."),
            ("extra sentence, sentence removed", f"{guide} {ctpat}"),
            ("another sentence reworded",
             current.replace("Read across a row", "Read along a row")),
            ("reflowed", current.replace(f" {pinned}", f"\n{pinned}")),
            ("missing", None),
            ("key table header changed", key),
            ("key table repeated", key),
            ("A04, sentence moved into a paragraph of its own",
             f"{guide}\n\n{pinned}"),
            ("A05, reworded sentence in a paragraph of its own",
             f"{guide}\n\n{reworded}"),
            ("nothing after the paragraph", None),
            ("no blank line under the key table", None),
        )
        path = self.mod.CROSSWALK_COMPLIANCE_MATRIX_PATH
        for case, para in refused:
            with self.subTest(case=case):
                if case == "missing":
                    text = source.replace(f"{current}\n\n", "")
                elif case == "key table header changed":
                    text = source.replace(
                        key, "| Column | Framework | Basis |")
                elif case == "key table repeated":
                    text = f"{source}\n{key}\n| --- | --- | --- |\n"
                elif case == "nothing after the paragraph":
                    text = source[:source.index(current) + len(current)] + "\n"
                elif case == "no blank line under the key table":
                    text = source.replace(f"\n\n{current}\n\n",
                                          f"\n{current}\n\n")
                else:
                    text = source.replace(current, para)
                self.assertNotEqual(text, source)
                with self.assertRaises(self.mod.BuildError) as raised:
                    self.mod.parse_compliance_tsc_status(text)
                message = str(raised.exception)
                self.assertIn(path, message)
                self.assertIn("reading-guide paragraph", message)
                self.assertIn(f"form 1: {current} form 2: {guide}", message)

        opening = self.mod.CROSSWALK_TSC_SECTION_OPENING.split("\n")
        row = [line for line in opening
               if line.startswith("| AICPA TSC 2017 |")]
        self.assertEqual(len(row), 1, "the key table's AICPA TSC 2017 row")
        row = row[0]
        ctpat_row = "| CTPAT | C-TPAT | Section headings |"
        intro = "section references that the document materially supports."
        key_list = "**Framework column keys:**"
        header = "**License:** CC BY-SA 4.0\n"
        for anchor in (f"{row}\n", ctpat_row, intro, key_list, header):
            self.assertEqual(source.count(anchor), 1, anchor)
        heading = f"{self.mod.CROSSWALK_TSC_SECTION_HEADING}\n"
        self.assertEqual(source.count(heading), 1)
        reflowed = pinned.replace("; until ", ";\nuntil ")
        self.assertNotEqual(reflowed, pinned)
        in_section = "where the pin has"
        outside = "outside the reading-guide paragraph"
        moved = (
            ("kept, the section heading reworded",
             source.replace(heading, "## How to read this matrix\n"),
             "headings instead of one"),
            ("kept, the section heading repeated", f"{source}\n{heading}",
             "headings instead of one"),
            ("into the intro paragraph",
             bare.replace(intro, f"{intro} {pinned}"), in_section),
            ("into its own paragraph above the key list",
             bare.replace(key_list, f"{pinned}\n\n{key_list}"), in_section),
            ("reworded, its own paragraph above the key list",
             bare.replace(key_list, f"{reworded}\n\n{key_list}"), in_section),
            ("into the AICPA TSC key row",
             bare.replace(row, f"{row[:-2]} {pinned} |"), in_section),
            ("into another key row",
             bare.replace(ctpat_row, f"{ctpat_row[:-2]}; {pinned} |"),
             in_section),
            ("as a new key row",
             bare.replace(f"{row}\n", f"{row}\n| AICPA TSC 2017 status | "
                          f"{pinned} | Matrix status |\n"), in_section),
            ("kept, the AICPA TSC key row removed",
             source.replace(f"{row}\n", ""), in_section),
            ("after the section's ---",
             bare.replace(divider, f"---\n\n{pinned}\n\n## Notes"), outside),
            ("into Notes", bare.replace(notes, f"{notes}{pinned}\n\n"),
             outside),
            ("into Notes, reflowed",
             bare.replace(notes, f"{notes}{reflowed}\n\n"), outside),
            ("into the document header",
             bare.replace(header, f"{header}\n{pinned}\n"), outside),
            ("at the end of the file", f"{bare}\n{pinned}\n", outside),
            ("a second copy in Notes",
             source.replace(notes, f"{notes}{pinned}\n\n"), outside),
        )
        for case, text, check in moved:
            with self.subTest(case=f"status sentence {case}"):
                self.assertNotEqual(text, source)
                with self.assertRaises(self.mod.BuildError) as raised:
                    self.mod.parse_compliance_tsc_status(text)
                message = str(raised.exception)
                self.assertIn(path, message)
                self.assertIn(check, message)

    def test_crosswalk_compliance_matrix_refuses_an_empty_column(self):
        """Batch 3 round 6 item 3 (observation): with 0 rows the AICPA TSC
        instrument caveat would read "none of its 0 rows is N/A". No column
        can have 0 rows: the parse fails on a matrix missing a domain's
        section and on a domain section with no rows, and every row has a
        cell in every column (build_crosswalk counts each one), so the
        caveat is never worded for 0 rows."""
        source = self.mod.CROSSWALK_COMPLIANCE_MATRIX.read_text(
            encoding="utf-8")
        domains, rows = self.mod.parse_compliance_matrix(source)
        self.assertEqual(sorted(domains), sorted(self.mod.DOMAIN_SCOPE))
        lines = source.splitlines()
        row_lines = [line for line in lines
                     if line.startswith("| ") and "[`" in line]
        self.assertEqual(len(row_lines),
                         sum(len(rows[domain]) for domain in domains))
        emptied = "\n".join(line for line in lines if line not in row_lines)
        with self.assertRaisesRegex(self.mod.BuildError, "zero rows"):
            self.mod.parse_compliance_matrix(emptied)
        heading = "## Governance domain\n"
        self.assertEqual(source.count(heading), 1)
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "missing domain section"):
            self.mod.parse_compliance_matrix(source.replace(heading, ""))

    # -- 38. batch 3 follow-up ----------------------------------------------

    # The 404 lead's fixed form for each top bar link it does not name by its
    # exact label (batch 3 follow-up round 2 item 2); every other lead item
    # must equal its bar label.
    _404_LEAD_FORMS = {
        "Crosswalk": "the crosswalk",
        "Search": "the search page",
        "GitHub": "the GitHub repository",
    }

    def _404_lead_problems(self, bar, page):
        """What keeps the 404 lead from naming the bar's links, in order."""
        nav = re.findall(r'<nav class="nav"[^>]*>(.*?)</nav>', bar, re.S)
        if len(nav) != 1:
            return [f"the top bar has {len(nav)} site navs"]
        labels = [re.sub(r'<span class="vh">.*?</span>', "", link).strip()
                  for link in re.findall(r"<a [^>]*>(.*?)</a>", nav[0], re.S)]
        lead = re.findall(r'<p class="lead">(.*?)</p>', page, re.S)
        if not labels or len(lead) != 1:
            return [f"{len(labels)} bar links, {len(lead)} 404 leads"]
        listed = re.fullmatch(r"(.*) are linked from the bar above\.",
                              lead[0])
        if listed is None:
            return [f"lead {lead[0]!r}"]
        items = re.split(r", (?:and )?", listed.group(1))
        if len(items) != len(labels):
            return [f"lead items {items} for bar links {labels}"]
        return [f"lead item {item!r} for bar link {label!r}"
                for item, label in zip(items, labels)
                if item != self._404_LEAD_FORMS.get(label, label)]

    def test_404_lead_names_every_top_bar_link(self):
        """Batch 3 follow-up item 4: the 404 page's lead lists the links of
        the top bar, one item per bar link in the bar's order, so renaming,
        adding or removing a bar link without updating the lead fails.

        Batch 3 follow-up round 2 item 2 (NOTE): round 1 matched each label
        as a case-insensitive word in its item, so renaming the bar's All
        Documents to Documents passed. Each item names its bar link by its
        exact label, or, for a label listed in _404_LEAD_FORMS, by that fixed
        form only.
        Flip samples, each failing: that rename, a lead item reworded ("the
        crosswalks"), and a bar link renamed while the lead keeps its old
        fixed form (Search to Site search)."""
        root = REPO_ROOT / ".web" / "templates-draft"
        bar = (root / "partials" / "topbar.html").read_text(encoding="utf-8")
        page = (root / "404.html").read_text(encoding="utf-8")
        self.assertEqual(self._404_lead_problems(bar, page), [])
        flips = (
            ("bar All Documents renamed Documents",
             bar.replace(">All Documents</a>", ">Documents</a>"), page),
            ("lead item reworded",
             bar, page.replace("the crosswalk,", "the crosswalks,")),
            ("bar Search renamed Site search",
             bar.replace(">Search</a>", ">Site search</a>"), page),
        )
        for case, flip_bar, flip_page in flips:
            with self.subTest(case=case):
                self.assertNotEqual((flip_bar, flip_page), (bar, page))
                self.assertTrue(self._404_lead_problems(flip_bar, flip_page))

    def test_crosswalk_section_pin_message_names_the_pin_to_update(self):
        """Batch 3 follow-up round 3 item 1: round 2's section pin failure
        message said only that the section must read exactly the pin, which
        points an author who fixed a typo in the matrix toward reverting it.

        Batch 3 follow-up round 4 item 1: round 3 named one constant to
        update, chosen by similarity or line position, which for a reworded
        status sentence named CROSSWALK_TSC_READING_GUIDE (updating it passes
        with the status False and drops the caveat) and on a layout line
        named a constant that cannot make the section pass. The message
        gives the line, the text found there and the pinned text, in the
        populating form at the reading-guide line when that line is the
        reading guide with more text after it, then one fixed sentence for
        every mismatch: update the pinned text in .web/build.py, the four
        constants named, the blank lines and the closing --- fixed in
        parse_compliance_tsc_status, and a changed status sentence goes in
        CROSSWALK_TSC_POPULATING, never folded into
        CROSSWALK_TSC_READING_GUIDE. Samples: a typo fixed in the status
        sentence, the status sentence reworded, the bare reading guide and
        the intro paragraph edited, the status sentence reflowed onto a line
        of its own, and the blank line after the reading guide removed.

        Batch 3 follow-up round 5 item 1: round 4 forbade folding a status
        sentence only into CROSSWALK_TSC_READING_GUIDE, so one moved into a
        paragraph of its own before the bare reading guide (P5) or onto the
        end of the intro paragraph (P6) passed once that pin was updated,
        with the status False. The status rule is independent of
        destination: a status sentence, changed or moved, belongs only in
        CROSSWALK_TSC_POPULATING at the end of the reading-guide line, never
        in CROSSWALK_TSC_SECTION_HEADING, CROSSWALK_TSC_SECTION_OPENING or
        CROSSWALK_TSC_READING_GUIDE. Round 5 item 2: the blank lines named
        as fixed in parse_compliance_tsc_status are those between the
        heading, the opening, the reading-guide paragraph and the closing
        ---. Samples added: P5 and P6.

        Batch 3 follow-up round 6 item 1: round 5 gave the instruction and
        the status rule only in the line mismatch error, so a status
        sentence moved into the section heading (P9) took the heading count
        error without them, and passed once CROSSWALK_TSC_SECTION_HEADING
        was updated, with the status False. Every section error carries
        both. Sample added: P9.

        Item 3b788 lows round 1 item 1: no sample reached the heading count
        error with two headings or the missing closing --- error, so either
        could lose the instruction and the rule unseen. Samples added: the
        section heading repeated at the end of the file, and every --- rule
        written as ***."""
        source = self.mod.CROSSWALK_COMPLIANCE_MATRIX.read_text(
            encoding="utf-8")
        guide = self.mod.CROSSWALK_TSC_READING_GUIDE
        pinned = self.mod.CROSSWALK_TSC_POPULATING
        current = f"{guide} {pinned}"
        self.assertEqual(source.count(f"\n\n{current}\n\n"), 1)
        bare = source.replace(current, guide)
        intro = [line for line
                 in self.mod.CROSSWALK_TSC_SECTION_OPENING.split("\n")
                 if line.startswith("This matrix maps GRC library")]
        self.assertEqual(len(intro), 1, "the intro paragraph")
        intro = intro[0]
        fixed = (
            "if the edit is intended, update the pinned text in "
            ".web/build.py (CROSSWALK_TSC_SECTION_HEADING, "
            "CROSSWALK_TSC_SECTION_OPENING, CROSSWALK_TSC_READING_GUIDE, "
            "CROSSWALK_TSC_POPULATING; the blank lines between the heading, the opening, "
            "the reading-guide paragraph and the closing --- are fixed in "
            "parse_compliance_tsc_status); "
        )
        rule = (
            "a status sentence, changed or moved, belongs only in "
            "CROSSWALK_TSC_POPULATING at the end of the reading-guide line, "
            "never in CROSSWALK_TSC_SECTION_HEADING, "
            "CROSSWALK_TSC_SECTION_OPENING or CROSSWALK_TSC_READING_GUIDE, "
            "because the section without it records the AICPA TSC 2017 "
            "column as no longer being populated; "
        )
        fixed += rule
        moved = "The AICPA TSC 2017 column is still being filled in."
        reworded = source.replace(current, f"{guide} {moved}")
        # P5 and P6: the status reworded and moved out of the reading-guide
        # line, which passes with the status False once its pin is updated.
        placed = (
            ("P5 status as its own paragraph before the bare reading guide",
             source.replace(f"\n\n{current}\n\n",
                            f"\n\n{moved}\n\n{guide}\n\n"),
             guide),
            ("P6 status appended to the intro paragraph",
             bare.replace(intro, f"{intro} {moved}"), intro),
        )
        cases = (
            ("typo fixed in the status sentence",
             source.replace(pinned, pinned.replace("domain by domain",
                                                   "domain-by-domain")),
             current),
            ("status sentence reworded", reworded, current),
            ("bare reading guide edited",
             bare.replace(guide, guide.replace("Read across a row",
                                               "Read across each row")),
             guide),
            ("intro paragraph edited",
             source.replace(intro, intro.replace("ten compliance",
                                                 "eleven compliance")),
             intro),
            ("status sentence reflowed onto its own line",
             source.replace(current, f"{guide}\n{pinned}"), ""),
            ("blank line after the reading guide removed",
             source.replace(f"\n\n{current}\n\n", f"\n\n{current}\n"), ""),
            *placed,
        )
        for case, text, shown in cases:
            with self.subTest(case=case):
                self.assertNotEqual(text, source)
                with self.assertRaises(self.mod.BuildError) as raised:
                    self.mod.parse_compliance_tsc_status(text)
                message = str(raised.exception)
                self.assertIn(".web/build.py", message)
                self.assertIn(f"where the pin has {shown!r}; {fixed}",
                              message)
        # P9: the status moved into the heading, which takes the heading
        # count error and passes with the status False once its pin is
        # updated.
        heading = f"{self.mod.CROSSWALK_TSC_SECTION_HEADING}\n"
        self.assertEqual(source.count(heading), 1)
        headed = ("P9 status in the section heading",
                  bare.replace(heading, f"{heading[:-1]} ({moved})\n"))
        # The heading count and closing --- errors, which no line mismatch
        # reaches: P9 (no heading), the heading repeated (two) and no ---
        # left after the heading.
        structural = (
            (*headed, f"0 {heading[:-1]!r} headings instead of one"),
            ("section heading repeated at the end of the file",
             f"{source}\n{heading}",
             f"2 {heading[:-1]!r} headings instead of one"),
            ("every --- rule written as ***",
             source.replace("\n---\n", "\n***\n"),
             f"no --- after {heading[:-1]!r} ends its section"),
        )
        for case, text, error in structural:
            with self.subTest(case=case):
                self.assertNotEqual(text, source)
                with self.assertRaises(self.mod.BuildError) as raised:
                    self.mod.parse_compliance_tsc_status(text)
                self.assertIn(f"{error}; {fixed}", str(raised.exception))
        for case, text in (("status sentence reworded", reworded),
                           *((case, text) for case, text, _ in placed),
                           headed):
            with self.subTest(case=f"destination-independent rule: {case}"):
                with self.assertRaises(self.mod.BuildError) as raised:
                    self.mod.parse_compliance_tsc_status(text)
                self.assertIn(rule, str(raised.exception))

    # -- 6. asset copy ------------------------------------------------------

    def test_asset_copy_matches_the_pinned_tree(self):
        import tomllib
        pin = tomllib.loads(
            (REPO_ROOT / ".baseline" / "pin.toml").read_text(encoding="utf-8")
        )
        prefix = ".web/baseline/"
        # Baseline 1.7.0 section 4 items 2 and 3: the palette gate is pinned
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
        """Baseline 1.7.0 SPECIFICATION.md section 8: "The 6 scripts are the
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

    def test_pin_and_copies_are_baseline_1_7_0(self):
        """The 1.7.0 move (CHANGELOG 1.7.0: every site moves to 1.7.0):
        the pin names 1.7.0, and the files 1.7.0 changes, with scheme.js
        from 1.6.0, carry the release's SHA256SUMS digests in the pin, in the
        repository and, for the served ones, in the draft copy; the module
        docstring and the CSP comment name the pinned version."""
        import tomllib
        pin = tomllib.loads(
            (REPO_ROOT / ".baseline" / "pin.toml").read_text(encoding="utf-8")
        )
        self.assertEqual(pin["version"], "1.7.0")
        for key, digest in RELEASE_1_7_0_DIGESTS.items():
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

    def test_served_palette_carries_the_matrix_tokens(self):
        """Spec 6.1 from 1.7.0: the 13 matrix tokens are palette tokens on
        every site and scheme, and the palette gate checks them. The site has
        no site-palette.css, so the served palettes.css alone must give
        grclibrary each token once, as a hex value, in both forms of each
        scheme, the 2 forms agreeing."""
        css = self.draft_all["draft/assets/baseline/palettes.css"].decode(
            "utf-8")
        self.assertEqual(len(MATRIX_TOKENS), 13)
        for token in MATRIX_TOKENS:
            for openers in (_LIGHT_BLOCKS, _DARK_BLOCKS):
                with self.subTest(token=token, block=openers[1]):
                    values = _dark_token(css, token, openers)
                    self.assertEqual(len(set(values)), 1, values)
                    self.assertRegex(values[0] or "", r"^#[0-9a-f]{6}$")
        self.assertEqual(
            [rel for rel in self.draft_all if rel.endswith("site-palette.css")],
            [], "the site serves no site-palette.css")

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

    _TYPE_FILTER_RE = re.compile(
        r'<p>With script, <a href="([^"]*)">All Documents, filtered to '
        r'([^<]*)</a>, lists (.*?)(, and the area chips holding any of them, '
        r'and its text filter, narrow them further|, and its text filter '
        r'narrows them further)?\.</p>')

    def _type_corpus_rows(self, page):
        """The rows of a type page's corpus list (its first list; the
        adopter documents follow in a block of their own)."""
        scope = re.search(r'<ul class="plan one described">(.*?)</ul>', page,
                          re.S)
        self.assertIsNotNone(scope, "the type page has no list")
        return self._TYPE_ROW_RE.findall(scope.group(1))

    def test_type_pages_link_their_all_documents_type_filter(self):
        """Each type page links its type's facet address on All Documents
        (?type=<slug>), the landing that adds the area chips and the text
        filter to the type; the value names a chip in the index's type
        group, so search.js sets it on load. The sentence is read off each
        rendered page: the documents it says that filter lists are exactly
        the type page's corpus-area rows and the rows the filter keeps
        (replayed), and it says "these N documents" only when the page
        lists no library specification and no adopter document (batch 3:
        the adopter block batch 2 added sits on the same page). A type with
        no row on All Documents gets no link. Round-1 NOTE: with one such
        row the sentence names one document and drops the clause saying the
        area chips and the text filter narrow "them" further; with more it
        keeps a narrowing clause (test_type_filter_sentence_names_only_the_
        filters_that_narrow checks which)."""
        rows = self._index_replay_rows()
        _, block = self._facet_group("type")
        chip_values = {v for _, v, _, _ in self._FACET_CHIP_RE.findall(block)}
        qualified = 0
        single = 0
        for tp in self.figures["type_pages"]:
            with self.subTest(type=tp["type"]):
                page = self.draft_html[self._type_rel(tp["type"])]
                in_index = [href for href, _, _, _
                            in self._type_corpus_rows(page)
                            if not href.startswith(self.mod.GITHUB_BLOB_BASE)]
                total = int(re.search(r'<p class="lbl sec">Documents, '
                                      r'(\d+)</p>', page).group(1))
                found = self._TYPE_FILTER_RE.findall(page)
                if not in_index:
                    self.assertEqual(found, [])
                    continue
                self.assertEqual(len(found), 1, "one filter link per page")
                href, plural, held, narrow = found[0]
                if len(in_index) == 1:
                    single += 1
                    self.assertEqual(narrow, "", "one row: nothing to narrow")
                else:
                    self.assertTrue(narrow, "the chips narrow these rows")
                self.assertEqual(_address_params(href), {"type": tp["slug"]})
                self.assertEqual(_page_rel_for(href), self._INDEX_REL)
                self.assertIn(tp["slug"], chip_values)
                self.assertEqual(unescape(plural),
                                 self.mod.draft_type_plural(tp["type"]))
                kept = _replay_search_js(rows, active={"type": tp["slug"]})
                self.assertEqual(sorted(r["href"] for r in kept),
                                 sorted(in_index))
                if len(in_index) == total:
                    expected = ("this document" if len(in_index) == 1
                                else f"these {len(in_index)} documents")
                else:
                    qualified += 1
                    expected = (f"the one of this page's {total} documents "
                                "that sits in a corpus area"
                                if len(in_index) == 1 else
                                f"the {len(in_index)} of this page's {total} "
                                "documents that sit in a corpus area")
                self.assertEqual(held, expected)
        self.assertTrue(qualified, "a type with library specifications "
                        "exercises the qualified form")
        self.assertTrue(single, "a type with one row exercises the singular")

    def test_type_filter_sentence_for_one_of_several_documents(self):
        """No type in today's corpus pairs one corpus-area document with a
        library specification, so a fixture exercises that form: the
        sentence names "the one of this page's 2 documents that sits in a
        corpus area" and drops the narrowing clause, as it does for a page
        of one document."""
        root = self.mod.ROOT_DOMAIN
        tp = {"type": "Specification", "slug": "specification", "count": 2,
              "scope": "A scope", "docs": [
                  {"path": "governance/specification-a.md",
                   "domain": "governance", "title": "A",
                   "type": "Specification"},
                  {"path": "specification-b.md", "domain": root,
                   "title": "B", "type": "Specification"}]}
        values = self.mod.draft_type_values(tp, {}, "/next/", "Next")
        self.assertEqual(
            values["TYPE_FILTER_SECTION"],
            '<p>With script, <a href="{{BASE}}/documents/?type=specification">'
            "All Documents, filtered to "
            f"{self.mod.draft_type_plural('Specification')}</a>, lists the "
            "one of this page's 2 documents that sits in a corpus area.</p>")

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
        mark = "" if pages else '<span class="n">declared gap</span>'
        self.assertIn(
            f'<li><a href="/draft/decide/{concern["slug"]}/">'
            f'{self.mod._esc(concern["question"])}</a>{mark}'
            f'<small>{self.mod._esc(concern["label"])}. '
            f'{self._concern_counts_text(pages, docs)}.</small></li>',
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
                        f'{self.mod._esc(page["narrative_type"].lower())}'
                        f'</span><small>{self.mod._esc(lede)} '
                        f'{len(page["sources"])} {noun}.',
                        block.group(1),
                        "the row's count is the page's source count")
                    self.assertIn(f'<a href="/draft/decide/{concern_slug}/">',
                                  block.group(1),
                                  "Go deeper names the resolving concern")
                else:
                    mark = ("" if pages
                            else '<span class="n">declared gap</span>')
                    self.assertIn(
                        f'{self.mod._esc(concern["question"])}</a>{mark}'
                        f'<small>{self.mod._esc(lede)} '
                        f"{self._concern_counts_text(pages, docs)}.",
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
        rendered crosswalk page's columns and Also list; the old claim
        that the crosswalk shows the same instruments is gone. Site f2: the
        Also in the corpus instruments are a group list in the crosswalk's
        left-rail side list, no longer chips under the table."""
        comply = self.draft_html["draft/comply/index.html"]
        xw = self.draft_html["draft/crosswalk/index.html"]
        table = re.search(r"<thead><tr>(.*?)</tr></thead>", xw, re.S)
        self.assertIsNotNone(table, "the crosswalk has no table head")
        columns = re.findall(r'<th scope="col" data-col="', table.group(1))
        rail = re.search(r'<div class="lrail">(.*?)</div>', xw, re.S)
        self.assertIsNotNone(rail, "the crosswalk has no side list")
        also = re.search(r'<p class="lbl">Also in the corpus</p><ul>(.*?)'
                         r'</ul>', rail.group(1), re.S)
        self.assertIsNotNone(also, "the crosswalk has no Also list")
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

    def test_palette_without_a_matrix_token_fails(self):
        """CHANGELOG 1.7.0: the 13 matrix tokens join the palette tokens and
        "a palette without them fails"; each, removed from all 4 of
        grclibrary's forms, fails the build's gate as not set."""
        for token in MATRIX_TOKENS:
            with self.subTest(token=token):
                bad = self._palettes(_drop_token(self._released(), token))
                with self.assertRaisesRegex(
                        self.mod.BuildError,
                        rf"FAIL grclibrary / light: --{token} is not set"):
                    self.mod.run_palette_gate(bad)

    def test_heat_step_text_cannot_be_read_on_fails(self):
        """1.7.0 checks the text on each heat step at 4.5:1: a dark --heat-4
        as light as the dark --text fails the build's gate."""
        bad = self._palettes(_doctor_dark_token(
            self._released(), "heat-4", "#e9e9e9"))
        with self.assertRaisesRegex(self.mod.BuildError,
                                    r"text on heat-4 .*FAIL"):
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
    """6: the matrix.js loading rule (spec section 7.30 and section 8), on
    fixtures, so the render test above cannot pass while no draft page has a
    matrix (round-1 ERROR: False equalled False on every page)."""

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


class CrosswalkPresetGroupTests(unittest.TestCase):
    """29 to 31: the presets are the topic views, and the generator refuses
    every way the topics, the groups and the instruments could disagree, so
    a column can never fall out of every topic, a topic can never show
    nothing or a column the table has not, and an instrument can never fall
    out of the side list silently."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_build()

    def _with(self, key, **changes):
        return tuple(i._replace(**changes) if i.key == key else i
                     for i in self.mod.CROSSWALK_INSTRUMENTS)

    def _topic(self, slug, **changes):
        return tuple(t._replace(**changes) if t.slug == slug else t
                     for t in self.mod.CROSSWALK_TOPICS)

    def test_presets_are_the_topics(self):
        presets = self.mod.crosswalk_presets()
        self.assertEqual(
            [(p.slug, p.label, p.columns, p.related) for p in presets],
            list(DraftSiteRenderTests._XW_TOPICS))
        self.assertEqual(presets, self.mod.CROSSWALK_TOPICS)

    def test_topic_with_no_column_raises(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "topic 'canada' has no column"):
            self.mod.crosswalk_presets(topics=self._topic("canada",
                                                          columns=()))

    def test_unknown_instrument_in_a_topic_raises(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "names instrument 'soc-2', which is no "
                                    "crosswalk instrument"):
            self.mod.crosswalk_presets(topics=self._topic(
                "security", columns=("iso-iec-27001", "soc-2")))

    def test_page_only_instrument_as_a_topic_column_raises(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "names 'pipeda' as a column, but it has "
                                    "no main-table column"):
            self.mod.crosswalk_presets(topics=self._topic(
                "canada", columns=("pip", "pipeda")))

    def test_unknown_related_instrument_raises(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "relates instrument 'lgpd', which is no "
                                    "crosswalk instrument"):
            self.mod.crosswalk_presets(topics=self._topic(
                "privacy", related=("pipeda", "lgpd")))

    def test_column_in_no_topic_raises(self):
        topics = self._topic("security", columns=(
            "iso-iec-27001", "nist-csf", "nist-sp-800-53", "csa-ccm"))
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "'aicpa-tsc' has a main-table column in "
                                    "no topic"):
            self.mod.crosswalk_presets(topics=topics)

    def test_instrument_outside_every_group_raises(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "which is no crosswalk group"):
            self.mod.crosswalk_presets(self._with("gdpr", group="Privacy"))

    def test_column_instrument_in_the_also_group_raises(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "belongs to a column group"):
            self.mod.crosswalk_presets(
                self._with("gdpr", group="Also in the corpus"))

    def test_page_only_instrument_in_a_column_group_raises(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "belongs to 'Also in the corpus'"):
            self.mod.crosswalk_presets(
                self._with("cobit", group="Laws and regulations"))

    # 31: round 3 items 8 and 9, and the spec 7.30 header's organization tag.

    def test_duplicate_topic_slug_raises(self):
        topics = self.mod.CROSSWALK_TOPICS + (
            self.mod.CROSSWALK_TOPICS[0]._replace(label="Security again"),)
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "duplicate topic slug 'security'"):
            self.mod.crosswalk_presets(topics=topics)

    def test_topic_slug_all_raises(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "topic slug 'all' is the All view's "
                                    "preset id"):
            self.mod.crosswalk_presets(topics=tuple(
                t._replace(slug="all") if t.slug == "canada" else t
                for t in self.mod.CROSSWALK_TOPICS))

    def test_column_repeated_within_a_topic_raises(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "topic 'trade' names column 'pip' more "
                                    "than once"):
            self.mod.crosswalk_presets(topics=self._topic("trade", columns=(
                "ctpat", "pip", "basc", "wco-safe", "aeo", "pip")))

    def test_main_table_instrument_with_no_org_raises(self):
        with self.assertRaisesRegex(self.mod.BuildError,
                                    "main-table instrument 'gdpr' has no "
                                    "organization tag"):
            self.mod.crosswalk_presets(self._with("gdpr", org=None))

    def test_bad_topic_fails_the_build_not_the_import(self):
        """Round 3 item 8: the presets are validated in build_crosswalk, not
        at import, so a bad topic reports as a generator failure (main
        catches the BuildError the render raises) and an importer of the
        module does not break. The module is loaded from its own source with
        one topic emptied: the load succeeds and the build refuses."""
        path = REPO_ROOT / ".web" / "build.py"
        source = path.read_text(encoding="utf-8")
        good = ('CrosswalkPreset("canada", "Canada",\n'
                '                    ("pip",), ("pipeda", "quebec-law-25")),')
        self.assertEqual(source.count(good), 1, "the fixture finds its topic")
        bad = source.replace(good, good.replace('("pip",)', "()"))
        namespace = {"__name__": "web_build_bad_topic",
                     "__file__": str(path)}
        exec(compile(bad, str(path), "exec"), namespace)
        self.assertNotIn("CROSSWALK_PRESETS", namespace,
                         "no preset table is built at import")
        full = namespace["parse_taxonomy_full"](
            namespace["TAXONOMY"].read_text(encoding="utf-8"))
        with self.assertRaisesRegex(namespace["BuildError"],
                                    "topic 'canada' has no column"):
            namespace["build_crosswalk"](full)


class AdopterDocsFixtureTests(unittest.TestCase):
    """18, 19 and 21: the docs/ metadata reader's loud failure classes, on
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
                    "1.2.3-rc1", "1.2.3.400", "1..0")
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
        # 1.6.1 section 7.33, copied from the reference pages): drawing sizes
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

    # A class docstring's leading numbers: "25: ", "18 and 21: ", "29 to 31: "
    # or "4, 5 and 6: " (batch 3 note: "N and M:" was skipped unchecked).
    _LEAD_RE = re.compile(r"(\d+(?:(?:, | and | to )\d+)*): ")

    @classmethod
    def _lead_numbers(cls, doc):
        """The item numbers a docstring's lead names, a range expanded, or
        None when it has no numbered lead."""
        match = cls._LEAD_RE.match(doc)
        if not match:
            return None, None
        numbers = []
        for part in re.split(r", | and ", match.group(1)):
            low, _, high = part.partition(" to ")
            numbers += [str(n) for n in range(int(low), int(high or low) + 1)]
        return numbers, match.end()

    def _docstring_number_faults(self, classes):
        """Every fault in the classes' numbered docstrings: a number that
        names no module docstring item, and a docstring whose two-word
        phrases, held by exactly one item each, belong to items none of its
        numbers names."""
        items = dict(re.findall(r"^(\d+)\. (.*?)(?=^\d+\. |\Z)", __doc__,
                                re.M | re.S))
        phrases = {number: self._phrases(text)
                   for number, text in items.items()}
        faults = []
        numbered = 0
        for name, obj in classes:
            doc = inspect.cleandoc(obj.__doc__ or "")
            numbers, end = self._lead_numbers(doc)
            if numbers is None:
                continue
            numbered += 1
            for number in numbers:
                if number not in items:
                    faults.append(f"{name}: docstring number {number} names "
                                  "no docstring item")
            owners = set()
            for pair in self._phrases(doc[end:]):
                holders = [owner for owner, held in phrases.items()
                           if pair in held]
                if len(holders) == 1:
                    owners.update(holders)
            if owners and not owners & set(numbers):
                faults.append(f"{name}: docstring says {', '.join(numbers)} "
                              f"but its phrases belong to item(s) "
                              f"{sorted(owners)}")
        return numbered, faults

    def test_docstring_numbers_follow_the_module_docstring(self):
        """A class docstring's numbers name docstring items, and when the
        docstring shares a two-word phrase with exactly one item, one of its
        own items is among those (the palette gate class said 24 while only
        item 25 names the palette gate). A lead naming several items ("18
        and 21: ", "29 to 31: ") is checked number by number."""
        classes = [(name, obj) for name, obj in sorted(globals().items())
                   if inspect.isclass(obj) and obj.__module__ == __name__]
        numbered, faults = self._docstring_number_faults(classes)
        self.assertTrue(numbered, "no numbered class docstrings found")
        self.assertEqual(faults, [])
        multi = [name for name, obj in classes
                 if len(self._lead_numbers(
                     inspect.cleandoc(obj.__doc__ or ""))[0] or ()) > 1]
        self.assertTrue(multi, "a class docstring names several items today")

    def test_docstring_guard_parses_a_lead_naming_several_items(self):
        """Batch 3 (batch 2 note): the guard read only a "N: " lead, so a
        docstring opening "N and M: " was skipped and a number in it naming
        no item passed. On fixtures: each number of an "and" lead and of a
        "to" range must name an item, and a lead whose numbers all name
        items passes."""
        items = re.findall(r"^(\d+)\. ", __doc__, re.M)
        top = max(int(n) for n in items)
        good = type("Good", (), {"__doc__": f"1 and {top}: fixture."})
        bad_and = type("BadAnd", (), {"__doc__": f"1 and {top + 1}: fixture."})
        bad_range = type("BadRange", (),
                         {"__doc__": f"{top - 1} to {top + 1}: fixture."})
        self.assertEqual(self._lead_numbers("18 and 21: x")[0], ["18", "21"])
        self.assertEqual(self._lead_numbers("29 to 31: x")[0],
                         ["29", "30", "31"])
        self.assertEqual(self._lead_numbers("4, 5 and 6: x")[0],
                         ["4", "5", "6"])
        _, faults = self._docstring_number_faults([("Good", good)])
        self.assertEqual(faults, [])
        _, faults = self._docstring_number_faults(
            [("BadAnd", bad_and), ("BadRange", bad_range)])
        self.assertEqual(
            faults,
            [f"BadAnd: docstring number {top + 1} names no docstring item",
             f"BadRange: docstring number {top + 1} names no docstring item"])


if __name__ == "__main__":
    unittest.main()
