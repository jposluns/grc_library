#!/usr/bin/env python3
"""Backlog actionability enumeration across BOTH backlog lists, so a "queue
exhausted / all blocked / hold" claim cannot be made without confronting every
open item on either list (anti-false-completeness layer 1).

WHY THIS EXISTS. A completeness claim ("everything left is blocked, so I am
stopping") was made from a PARTIAL review and was wrong: actionable items
remained. Nothing mechanical forced the claimant to confront EVERY backlog item
first. This tool does: it enumerates every open item in the PUBLIC ``TODO.md``
AND the PRIVATE ``grc_library_private/P-TODO.md`` and, per item, reports whether
it is BLOCKED.

THE AUTHORITATIVE BLOCKER SIGNAL IS THE TAG, NOT PROSE. An item is counted
BLOCKED only if it carries a ``[BLOCKED:<reason>]`` tag. That tag is a
maintainer-GRANTED status: the assistant never self-applies it (a PreToolUse
hook rejects a ``[BLOCKED]`` written without a matching maintainer approval
record), it proposes a block in ``.working/pending-decisions.md`` and only an
approved block becomes a tag. So "all blocked" is assertable only when EVERY
open item on BOTH lists literally carries an approved ``[BLOCKED:...]`` tag,
which is essentially never. Until the maintainer approves blocks, every item
reads ACTIONABLE, which is the honest state.

PROSE SIGNAL IS ADVISORY ONLY. The closed keyword set below (``egress-gated``,
``DEFERRED``, ``maintainer-decision`` ...) no longer decides blocked-vs-actionable;
it is surfaced as an ADVISORY "this item's prose mentions a blocker; propose a
``[BLOCKED]`` tag for it?" hint. An item with a prose signal but no approved tag
is still ACTIONABLE (the safe direction: it forces a disposition, it does not
hide a blocker behind an unapproved self-assessment).

It is ADVISORY, NOT a gate: it always exits 0, is not wired into
``quality.yml`` / ``run_all_audits.sh`` / ``.pre-commit-config.yaml``, and is
portable-clone-tolerant (a missing list is a no-op for that list; an adopter with
no private sibling simply audits the public list). Regression coverage:
``BacklogActionabilityTests`` in ``tests/test_linters.py``.

USAGE
  python3 tools/audit-backlog-actionability.py
      Enumerate every open item on both lists; print the full table, the summary
      counts, and the ACTIONABLE list.
  python3 tools/audit-backlog-actionability.py --actionable-only
      Print only the summary and the ACTIONABLE list.
  python3 tools/audit-backlog-actionability.py --todo PATH --ptodo PATH
      Override either list path (testing / non-default layout).

Stdlib-only (gate 71). Python 3.11.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TODO_PATH = REPO_ROOT / "TODO.md"
# The private backlog lives in the maintainer's private sibling; adopters have no
# such sibling and simply audit the public list (resolve_sibling no-op).
PTODO_PATH = REPO_ROOT.parent / "grc_library_private" / "P-TODO.md"
DONE_PATH = REPO_ROOT.parent / "grc_library_private" / ".working" / "DONE.md"
NEXTPRS_PATH = REPO_ROOT.parent / "grc_library_private" / ".working" / "next-prs.txt"

# An open backlog item heading: ``### <id> <title>`` where <id> is a section
# number (``N.M`` / ``N.M.K``, optional trailing letter), a private ``P-n.m`` id,
# or a coded id (``SR-1`` / ``RB-R6`` / ``GR-GAP-1``). ``## `` section headers are
# NOT items.
ITEM_HEADING_RE = re.compile(
    r"^### (?P<id>P-\d+(?:\.\d+){1,2}[a-z]?"
    r"|\d+(?:\.\d+){1,2}[a-z]?"
    r"|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\b[ \t]*(?P<title>.*)$"
)

# The AUTHORITATIVE blocker signal: a ``[BLOCKED:<reason>]`` tag (maintainer-granted).
BLOCKED_TAG_RE = re.compile(r"\[BLOCKED:[^\]]*\]")

# ADVISORY prose-signal set (closed). Detected only to SUGGEST proposing a block;
# it never counts an item blocked. Kept deliberately narrow to avoid false hints.
PROSE_SIGNAL_TOKENS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"egress[- ]gated|egress[- ]blocked", re.I), "egress"),
    (re.compile(r"source[- ]gated|source[- ]not[- ]held|pending held source"
                r"|pending maintainer source|blocked on .{0,30}ingest", re.I),
     "source"),
    (re.compile(r"maintainer[- ](decision|decided|gated|collaborative|"
                r"sign[- ]off|owned)", re.I), "maintainer-decision"),
    (re.compile(r"\bNOT automated\b|explicitly NOT automated"), "maintainer-decision"),
    (re.compile(r"\bDEFERRED\b|\bdeferred\b"), "deferred"),
    (re.compile(r"\bIN PROGRESS\b"), "in-progress"),
    (re.compile(r"fresh[- ]session|fresh[- ]context|attended[- ]preferred"
                r"|attended/fresh|fresh session", re.I), "fresh-session"),
    (re.compile(r"\(standing\)|,\s*standing\)|standing (?:tracker|watch)"
                r"|stays open by design", re.I), "standing"),
]


def parse_items(text: str, source: str) -> list[tuple[str, str, str, str, str]]:
    """Return ``(id, title, block_text, source, umbrella)`` for every open ``### `` item.

    A block runs from its item heading to the next item heading, the next ``## ``
    section header, or end of file, so a signal is detected only within the item's
    own text. ``source`` labels which list the item came from (``public`` /
    ``private``)."""
    lines = text.splitlines()
    items: list[tuple[str, str, str, str, str]] = []
    cur: tuple[str, str] | None = None
    body: list[str] = []
    umbrella = ""  # the most-recent ``## `` section header (the item's umbrella)

    def flush() -> None:
        if cur is not None:
            items.append((cur[0], cur[1].strip(), "\n".join(body), source, umbrella))

    for line in lines:
        m = ITEM_HEADING_RE.match(line)
        if m:
            flush()
            cur = (m.group("id"), m.group("title"))
            body = [line]
        elif line.startswith("## "):
            flush()
            cur = None
            body = []
            umbrella = line[3:].strip()
        elif cur is not None:
            body.append(line)
    flush()
    return items


def is_blocked(block_text: str) -> bool:
    """True iff the item's HEADING carries an (approved) ``[BLOCKED:...]`` tag.

    Scans ONLY the heading (first line of the block): per the design the tag lives
    on the item heading, so a ``[BLOCKED:...]`` appearing in an item's BODY prose
    (e.g. an item describing the blocked-tag feature) must NOT false-match as
    blocked, which is the unsafe direction (it would hide an actionable item)."""
    heading = block_text.splitlines()[0] if block_text else ""
    return bool(BLOCKED_TAG_RE.search(heading))


def prose_signals(block_text: str) -> list[str]:
    """Sorted distinct ADVISORY prose blocker-signals (never authoritative)."""
    return sorted({cls for pat, cls in PROSE_SIGNAL_TOKENS if pat.search(block_text)})


def build_report(public_text: str,
                 private_text: str | None = None) -> tuple[list, int, int]:
    """Return (rows, blocked_count, actionable_count). Each row is
    ``(id, title, source, blocked_bool, prose_list)``."""
    items = parse_items(public_text, "public")
    if private_text is not None:
        items += parse_items(private_text, "private")
    rows = []
    blocked = 0
    for item_id, title, block, source, _umbrella in items:
        b = is_blocked(block)
        rows.append((item_id, title, source, b, prose_signals(block)))
        if b:
            blocked += 1
    return rows, blocked, len(rows) - blocked



# ---- --pipeline mode (maintainer-directed 2026-08-06): the scannable roadmap view ----

# A bulleted SUB-ITEM under an umbrella heading: ``- **<id>** <desc>``.
BULLET_ITEM_RE = re.compile(r"^\s*[-*] \*\*(?P<id>P-\d+(?:\.\d+){1,2}[a-z]?"
                            r"|\d+(?:\.\d+){1,2}[a-z]?"
                            r"|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\*\*[ \t]*(?P<title>.*)$")

# An INLINE formal-id mention in umbrella wave-prose (NOT a ``- **id**`` bullet):
# e.g. ``_Wave 2_: **P-1.25.12** 4 more briefs; **P-1.25.13** 3 scenarios``. The description
# runs to the next ``;`` or ``**`` (P-1.30 bug b: inline wave items were omitted from the view).
INLINE_ID_RE = re.compile(
    r"\*\*(?P<id>P-\d+(?:\.\d+){1,2}[a-z]?"
    r"|\d+(?:\.\d+){1,2}[a-z]?"
    r"|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\*\*[ \t]*(?P<title>(?:[^;*]|\*(?!\*))*)")


def _is_descendant(child_id: str, parent_id: str) -> bool:
    """True if ``child_id`` is a proper dotted descendant of ``parent_id`` (e.g.
    ``P-1.25.12`` under ``P-1.25``). Umbrella children share the umbrella id prefix per
    the multi-phase-series numbering convention."""
    return child_id.startswith(parent_id + ".")

# A DONE.md entry heading. Accepts a SINGLE PR (``### PR #1425: ... (2026-08-06)``) or a
# COMPOUND heading (``### PR #1425 + #1426: ... (date)``); the ``extra`` group captures the
# ``+ #NNNN`` repeats so a compound entry is not silently skipped (P-1.30 bug a).
DONE_ENTRY_RE = re.compile(
    r"^### PR #(?P<pr>\d+)(?P<extra>(?:\s*\+\s*#\d+)*):\s*(?P<title>.*?)\s*\((?P<date>\d{4}-\d\d-\d\d)\)\s*$")

# Priority-ordered (first match wins) TYPE heuristic. Rough by design: the /pipeline
# command refines a wrong guess. Keyword -> one-word type.
_TYPE_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("website", (".web", "site route", "site render", "homepage", "re-hero",
                 "role page", "role (", "maturity", "local search", "adjacency",
                 "guided discovery", "portal", "relationship view")),
    ("rule", ("pack rule", "change-tracking extension", "trust-recovery extension",
              "conformance contract", "oversight and autonomy", "discipline (")),
    ("validation", ("validat", "/fitness", "fitness", "reference-increment")),
    ("ops", ("runbook", "changelog", "roll-up", "rollup", "scale wave", "ops ")),
    ("content", ("brief", "scenario", "journey", "exemplar", "story",
                 "narrative page", "outcome map", "control journey")),
    ("gate", ("new gate", "staleness gate", "audit gate", "freshness gate")),  # specific gate phrases
    ("tool", ("lint", "scanner", "guard", ".py", "hook", "tool", "generator")),
    ("gate", ("gate ",)),   # P-1.30 bug d + QA finding 6: generic "gate N" fallback AFTER the tool
                            # rule, so a tool item that also mentions "gate" (e.g. "add gate-count
                            # consistency linter", "... evidence gates ...") stays tool; a pure
                            # "gate 87" item (no tool indicator) still types gate.
    ("rule", (" rule", "extension")),  # last-resort rule catch (after specifics)
]


def infer_type(text: str) -> str:
    low = text.lower()
    for typ, kws in _TYPE_RULES:
        if any(k in low for k in kws):
            return typ
    return "item"


def trunc_words(title: str, n: int = 10) -> str:
    """First ``n`` words of the title, stripped of a leading bold/label run."""
    title = re.sub(r"\*\*[^*]*\*\*", lambda m: m.group(0).strip("*"), title).strip()
    words = title.split()
    return " ".join(words[:n]) + (" ..." if len(words) > n else "")


def parse_done(done_text: str, limit: int = 5) -> list[tuple[int, str]]:
    """The ``limit`` most-recent completed items from DONE.md, most-recent first.
    Ordered by completion DATE (the ledger date), tie-broken by highest PR number, NOT by
    PR number alone (P-1.30 bug a: merge order and completion-ledger order can diverge). A
    compound ``### PR #A + #B`` heading counts as ONE entry, represented by its highest PR.
    Returns ``(pr_number, title)``."""
    entries: list[tuple[str, int, str]] = []   # (date, representative_pr, title)
    for line in done_text.splitlines():
        m = DONE_ENTRY_RE.match(line)
        if m:
            prs = [int(m.group("pr"))]
            if m.group("extra"):
                prs += [int(x) for x in re.findall(r"#(\d+)", m.group("extra"))]
            entries.append((m.group("date"), max(prs), m.group("title").strip()))
    # ISO dates sort lexically == chronologically; reverse => most-recent first,
    # tie-broken by PR number descending.
    entries.sort(key=lambda e: (e[0], e[1]), reverse=True)
    return [(pr, title) for _date, pr, title in entries[:limit]]


def _short_id(title: str) -> str:
    """Leading backlog-id-like token in a title, else empty."""
    m = re.match(r"(P-\d+(?:\.\d+){0,2}[a-z]?|\d+(?:\.\d+){1,2}[a-z]?"
                 r"|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\b", title.strip())
    return m.group(1) if m else ""


def render_pipeline(public_text: str, private_text: str | None,
                    done_text: str | None, umbrella_filter: str | None,
                    limit: int = 20) -> str:
    """Render the pipeline view: the 5 most-recent done at top (``[x]`` + PR####),
    then the current umbrella's open items up to ``limit``, filling from subsequent
    umbrellas (file/priority order) when the current one has fewer than ``limit``."""
    items = parse_items(public_text, "public")
    if private_text is not None:
        items += parse_items(private_text, "private")

    # Build LEAF items. A ``### `` block that contains ``- **<id>**`` bullets is an
    # umbrella whose bullets are the leaves (umbrella = the ### heading id + title);
    # a ``### `` block with no bullets is itself a leaf (umbrella = its ## parent).
    open_items: list[tuple[str, str, str, str, str]] = []
    for item_id, title, block, source, umb in items:
        if is_blocked(block):
            continue  # a [BLOCKED:] parent heading excludes itself AND its bullet leaves
        head_umb = f"{item_id} {title}".strip()
        # An umbrella's CHILDREN are the formal ids in its block that are dotted DESCENDANTS
        # of the umbrella id, written either as ``- **id**`` bullets OR inline in wave prose
        # (``**id** ...``); the inline form was previously dropped (P-1.30 bug b). A bullet in
        # the block whose id is NOT a descendant (a sibling item authored inside the block) is
        # promoted to its OWN leaf item rather than mis-attributed as this umbrella's child.
        children: list[tuple[str, str, str]] = []     # (id, title, line) descendant children
        foreign: list[tuple[str, str, str]] = []      # non-descendant bullets, promoted
        seen: set[str] = set()                        # every id claimed (child / foreign / blocked)
        had_bullets = False                           # did the block carry ANY child/item bullet
        lines = block.splitlines()
        # Pass 1 -- bullets are AUTHORITATIVE, collected first so an inline mention never
        # shadows a bullet of the same id (QA finding 1); a repeated or blocked bullet id is
        # claimed in `seen` so it is neither duplicated (finding 5) nor resurrected inline.
        for line in lines:
            bm = BULLET_ITEM_RE.match(line)
            if not bm:
                continue
            had_bullets = True
            bid = bm.group("id")
            if bid in seen:
                continue
            seen.add(bid)
            if BLOCKED_TAG_RE.search(line):
                continue                              # a granted-blocked bullet is not emitted
            (children if _is_descendant(bid, item_id) else foreign).append(
                (bid, bm.group("title"), line))
        # Pass 2 -- inline wave-prose ids (non-bullet lines only, descendants, not blocked).
        for line in lines:
            if BULLET_ITEM_RE.match(line):
                continue
            for im in INLINE_ID_RE.finditer(line):
                iid = im.group("id")
                if iid in seen or not _is_descendant(iid, item_id):
                    continue
                if BLOCKED_TAG_RE.search(im.group(0)):   # inline [BLOCKED] item excluded (finding 3)
                    seen.add(iid)
                    continue
                idesc = im.group("title").strip()
                # context = the child's OWN desc (the shared wave line mixes sibling items and
                # track keywords, which would mis-type an inline child).
                children.append((iid, idesc, idesc)); seen.add(iid)
        if children or foreign:
            for bid, btitle, bline in children:
                open_items.append((bid, btitle, bline, source, head_umb))
            for bid, btitle, bline in foreign:
                open_items.append((bid, btitle, bline, source, umb or ""))
        elif not had_bullets:
            # a genuine bulletless leaf is the item itself; if the block HAD bullets that were
            # ALL blocked, emit nothing (do not resurrect the parent as open -- QA finding 4).
            open_items.append((item_id, title, block, source, umb or title))

    out: list[str] = []
    # R20-GAP-1: degradation must be LOUD, not silent -- a maintainer view missing the
    # private backlog or the DONE ledger is INCOMPLETE and must say so at the top.
    missing = []
    if private_text is None:
        missing.append("private backlog (P-TODO.md)")
    if not done_text:
        missing.append("DONE ledger (recent-done section)")
    if missing:
        out.append("!!! INCOMPLETE PIPELINE VIEW: missing " + " + ".join(missing)
                   + " -- upcoming private items and/or done-marking are NOT shown !!!")
        out.append("")
    # 1. recent-done header
    if done_text:
        for pr, title in parse_done(done_text, 5):
            sid = _short_id(title) or f"#{pr}"
            out.append(f"{sid} [x] PR{pr} {infer_type(title)} - {trunc_words(title)}")
        out.append("")

    # 2. current umbrella up to limit, then fill from subsequent umbrellas
    umbrellas: list[str] = []
    for _i, _t, _b, _s, umb in open_items:
        if umb not in umbrellas:
            umbrellas.append(umb)
    if umbrella_filter:
        start = next((u for u in umbrellas if umbrella_filter.lower() in u.lower()), None)
        if start is None:
            # a non-matching filter must SIGNAL, not silently render the default view
            out.append(f"(no umbrella matched {umbrella_filter!r}; showing default order)")
            out.append("")
        order = umbrellas[umbrellas.index(start):] if start else umbrellas
    else:
        order = umbrellas  # first umbrella (highest-priority open item) leads

    shown = 0
    for ui, umb in enumerate(order):
        if shown >= limit:
            break
        grp = [it for it in open_items if it[4] == umb]
        if ui > 0:
            out.append("")  # blank line between umbrellas
        for item_id, title, _b, _s, _u in grp:
            if shown >= limit:
                break
            out.append(f"{item_id} [ ] {infer_type(title + ' ' + _b)} - {trunc_words(title)}")
            shown += 1
    return "\n".join(out)


def _self_test() -> int:
    failures: list[str] = []

    def check(name: str, cond: bool) -> None:
        if not cond:
            failures.append(name)

    # infer_type
    check("type-website", infer_type("first live /executive/ site render") == "website")
    check("type-rule", infer_type("new ai-supply-chain-provenance pack rule") == "rule")
    check("type-content", infer_type("author three scenario pages") == "content")
    check("type-validation", infer_type("full validation pass") == "validation")
    check("type-tool", infer_type("shared multi-line link scanner (lint_common)") == "tool")
    check("type-gate", infer_type("wire the new authority-boundary gate 87") == "gate")  # P-1.30 bug d
    check("type-gate-plural-stays-tool", infer_type("lint-executive-metadata.py + section/evidence gates") == "tool")

    # trunc_words: <=10 words, ellipsis when longer
    tw = trunc_words("one two three four five six seven eight nine ten eleven twelve")
    check("trunc-10-plus-ellipsis", tw.split(" ...")[0].split() == ["one","two","three","four","five","six","seven","eight","nine","ten"] and tw.endswith("..."))
    check("trunc-short-no-ellipsis", trunc_words("short title here") == "short title here")

    # parse_done: highest PR first, limit honoured
    done = "### PR #1420: item A (2026-08-05)\n\n### PR #1429: item B (2026-08-06)\n\n### PR #1425: item C (2026-08-05)\n"
    d = parse_done(done, 2)
    check("done-order-and-limit", d == [(1429, "item B"), (1425, "item C")])

    # render_pipeline: 5 done at top, then umbrella-grouped open items, blank between umbrellas
    pub = ("## Umbrella One\n\n### 1.1 First website render task here\n\n### 1.2 Second content brief task here\n\n"
           "## Umbrella Two\n\n### 2.1 A blocked one [BLOCKED:x] should not show\n\n### 2.2 A tool lint task here\n")
    r = render_pipeline(pub, None, "### PR #1429: recent done thing (2026-08-06)\n", None, limit=20)
    lines = r.splitlines()
    check("render-done-header", any(l.startswith("#1429 [x] PR1429 ") for l in lines))
    check("render-has-1.1", any(l.startswith("1.1 [ ] ") for l in lines))
    check("render-1.2-content", any(l.startswith("1.2 [ ] ") for l in lines))
    check("render-excludes-blocked", not any("2.1 [ ]" in l for l in lines))
    check("render-includes-2.2", any(l.startswith("2.2 [ ] ") for l in lines))
    # blank line between the two umbrellas (a "" line exists between 1.x and 2.x groups)
    check("render-blank-between-umbrellas", "" in lines[lines.index(next(l for l in lines if l.startswith("1.1"))):])

    # umbrella filter scopes to the matching umbrella first
    r2 = render_pipeline(pub, None, None, "Two", limit=20)
    r2_lines = [l for l in r2.splitlines() if l and not l.startswith("!!!")]
    check("filter-starts-at-two", r2_lines[0].startswith("2.2 [ ] "))

    # R20 fixes: blocked-parent leaf exclusion + loud banner on missing state
    rb = render_pipeline("## U\n\n### 9.9 Parent [BLOCKED:granted]\n- **9.9.1** child\n\n### 8.8 Open one\n", None, None, None)
    check("blocked-parent-leaf-excluded", "9.9.1" not in rb and any("8.8 [ ]" in l for l in rb.splitlines()))
    check("loud-banner-on-missing-state", any(l.startswith("!!! INCOMPLETE PIPELINE VIEW") for l in rb.splitlines()))

    # P-1.30 bug a: compound DONE headings counted (not skipped) and ordered by DATE, not PR.
    done2 = ("### PR #1500: newer low-pr (2026-08-07)\n\n"
             "### PR #1600: older high-pr (2026-08-01)\n\n"
             "### PR #1425 + #1426: compound entry (2026-08-06)\n")
    d2 = parse_done(done2, 3)
    check("done-date-order-not-pr",
          d2 == [(1500, "newer low-pr"), (1426, "compound entry"), (1600, "older high-pr")])
    check("done-compound-counted", any(pr == 1426 for pr, _ in d2))

    # P-1.30 bug b: inline wave-prose child ids are enumerated, and a non-descendant bullet
    # authored inside an umbrella block is PROMOTED to its own item, not mis-attributed.
    pub2 = ("## U3\n\n### P-9.1 Umbrella heading here\n"
            "- **P-9.9** sibling item authored inside the block\n"
            "- **P-9.1.1** real bullet child here\n"
            "_Wave X:_ **P-9.1.2** inline child two; **P-9.1.3** inline child three\n")
    r3l = render_pipeline(pub2, None, None, None, limit=20).splitlines()
    check("inline-child-enumerated",
          any(l.startswith("P-9.1.2 [ ] ") for l in r3l) and any(l.startswith("P-9.1.3 [ ] ") for l in r3l))
    check("bullet-child-enumerated", any(l.startswith("P-9.1.1 [ ] ") for l in r3l))
    check("foreign-bullet-promoted", any(l.startswith("P-9.9 [ ] ") for l in r3l))
    _ic = next(i for i, l in enumerate(r3l) if l.startswith("P-9.1.1"))
    _if = next(i for i, l in enumerate(r3l) if l.startswith("P-9.9"))
    check("foreign-bullet-separate-group", "" in r3l[min(_ic, _if):max(_ic, _if)])
    # an inline content child must type from its own desc, not the shared wave line
    pub3 = ("## U4\n\n### P-8.1 Umbrella here\n"
            "Track A (content): **P-8.1.1** author four briefs; Track B (website): **P-8.1.2** homepage re-hero\n")
    r4l = render_pipeline(pub3, None, None, None, limit=20).splitlines()
    check("inline-child-typed-from-own-desc",
          any(l.startswith("P-8.1.1 [ ] content ") for l in r4l)
          and any(l.startswith("P-8.1.2 [ ] website ") for l in r4l))

    # P-1.30 QA finding 1: a bullet is authoritative; an inline mention of the same id
    # (even earlier in the text) never shadows it -- the bullet's desc wins, one row only.
    pub5 = ("## U5\n\n### P-5.1 Umbrella\n"
            "_Wave:_ **P-5.1.1** inline shadow desc\n"
            "- **P-5.1.1** authoritative bullet desc here\n")
    r5l = [l for l in render_pipeline(pub5, None, None, None, limit=20).splitlines() if l.startswith("P-5.1.1")]
    check("bullet-wins-over-inline", len(r5l) == 1 and "authoritative bullet desc" in r5l[0])

    # finding 2: an inline desc with markdown emphasis is not truncated at the lone '*'.
    pub6 = ("## U6\n\n### P-6.1 Umbrella\nTrack: **P-6.1.1** author *four* briefs here\n")
    r6l = render_pipeline(pub6, None, None, None, limit=20).splitlines()
    check("inline-emphasis-not-truncated", any("briefs here" in l for l in r6l if l.startswith("P-6.1.1")))

    # finding 3: an inline child carrying a granted [BLOCKED] tag is excluded, like a bullet.
    pub7 = ("## U7\n\n### P-7.1 Umbrella\nWave: **P-7.1.1** ok child; **P-7.1.2** blocked [BLOCKED:granted] one\n")
    r7l = render_pipeline(pub7, None, None, None, limit=20).splitlines()
    check("inline-blocked-excluded",
          any(l.startswith("P-7.1.1 [ ] ") for l in r7l) and not any(l.startswith("P-7.1.2 ") for l in r7l))

    # finding 4: when every child bullet is blocked, neither the children NOR the parent emit.
    pub8 = ("## U8\n\n### P-8.9 Umbrella parent\n- **P-8.9.1** child [BLOCKED:granted]\n- **P-8.9.2** child2 [BLOCKED:granted]\n")
    r8l = render_pipeline(pub8, None, None, None, limit=20).splitlines()
    check("all-blocked-children-no-parent-resurrect",
          not any(l.startswith("P-8.9 ") for l in r8l) and not any(l.startswith("P-8.9.1") for l in r8l))

    # finding 5: a repeated foreign (non-descendant) bullet is deduplicated to one row.
    pub9 = ("## U9\n\n### P-9.5 Umbrella\n- **P-4.1** foreign sibling\n- **P-4.1** foreign sibling dup\n- **P-9.5.1** real child\n")
    r9l = [l for l in render_pipeline(pub9, None, None, None, limit=20).splitlines() if l.startswith("P-4.1 ")]
    check("foreign-bullet-deduped", len(r9l) == 1)

    if failures:
        for f in failures:
            print(f"  SELF-TEST FAIL: {f}")
        print(f"self-test: {len(failures)} case(s) failed.")
        return 1
    print("self-test: all pipeline cases passed (type inference incl. gate, 10-word truncation, "
          "recent-done date-ordering + compound headings, umbrella grouping, inline-wave children, "
          "foreign-bullet promotion, blocked exclusion, umbrella filter).")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--actionable-only", action="store_true",
                    help="print only the summary and the ACTIONABLE list")
    ap.add_argument("--pipeline", action="store_true",
                    help="render the scannable roadmap pipeline view")
    ap.add_argument("--umbrella", default=None,
                    help="--pipeline: scope to the umbrella whose header matches this substring")
    ap.add_argument("--self-test", action="store_true", help="run internal self-test")
    ap.add_argument("--todo", default=str(TODO_PATH), help="public TODO.md path")
    ap.add_argument("--ptodo", default=str(PTODO_PATH),
                    help="private P-TODO.md path (no-op if absent)")
    args = ap.parse_args(argv)

    if args.self_test:
        return _self_test()

    todo = Path(args.todo)
    if not todo.is_file():
        print(f"advisory: TODO.md not found at {todo} (portable clone); no-op.")
        return 0
    public_text = todo.read_text(encoding="utf-8", errors="replace")

    ptodo = Path(args.ptodo)
    private_text = ptodo.read_text(encoding="utf-8", errors="replace") \
        if ptodo.is_file() else None
    private_note = "" if private_text is not None \
        else f" (private list {ptodo} absent; public-only)"

    if args.pipeline:
        done = Path(DONE_PATH)
        done_text = done.read_text(encoding="utf-8", errors="replace") if done.is_file() else None
        print(render_pipeline(public_text, private_text, done_text, args.umbrella))
        return 0

    rows, blocked, actionable = build_report(public_text, private_text)

    def trunc(t: str, w: int = 52) -> str:
        t = t.strip()
        return t if len(t) <= w else t[: w - 3] + "..."

    if not args.actionable_only:
        print(f"Backlog actionability enumeration (both lists){private_note}:")
        print(f"{'id':<10} {'list':<8} {'BLOCKED?':<9} {'prose-signal':<20} title")
        print("-" * 100)
        for item_id, title, source, b, sig in rows:
            bl = "BLOCKED" if b else "-"
            ps = ",".join(sig) if sig else ""
            print(f"{item_id:<10} {source:<8} {bl:<9} {ps:<20} {trunc(title)}")

    print(f"\n{len(rows)} open item(s) across both lists; {blocked} BLOCKED "
          f"(approved [BLOCKED:] tag); {actionable} ACTIONABLE.")
    print("An item is BLOCKED only via a maintainer-approved [BLOCKED:<reason>] "
          "tag. 'all blocked' is assertable only when EVERY item carries one.")

    # Advisory: items whose PROSE mentions a blocker but that carry no approved tag
    # are ACTIONABLE and are candidates to PROPOSE for a [BLOCKED] tag (never self-tag).
    propose = [(i, t, sig) for i, t, s, b, sig in rows if sig and not b]
    if propose:
        print(f"\nPROSE-SIGNAL, NO APPROVED TAG ({len(propose)}) "
              f"-- ACTIONABLE now; propose a [BLOCKED] tag via pending-decisions.md:")
        for item_id, title, sig in propose:
            print(f"  - {item_id}  [{','.join(sig)}]  {trunc(title)}")

    actionable_rows = [(i, t, s) for i, t, s, b, sig in rows if not b]
    if actionable_rows:
        print(f"\nACTIONABLE ({len(actionable_rows)}):")
        for item_id, title, source in actionable_rows:
            print(f"  - {item_id}  ({source})  {trunc(title)}")
    else:
        print("\n(no actionable items: every open item on both lists carries an "
              "approved [BLOCKED:] tag. Verify each before any all-blocked claim.)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
