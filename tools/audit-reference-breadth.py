#!/usr/bin/env python3
"""Reference-breadth worklist: how the corpus uses the held reference base, both
directions, exhaustively.

WHAT THIS IS (and is NOT). This is an orchestrator dev-AID feeding the
/reference-audit skill (TODO 2.14), not an audit gate. It exits 0 after
printing its report (2 only on internal or usage error; a truncated-pipe consumer
such as ``| head`` terminates it via SIGPIPE, as normal for a command-line tool);
CI cannot host it because
the ground truth lives in the sibling private reference repo. Its output is a
recall-oriented WORKLIST for the semantic judge, never a defect list: a lexical
matcher deliberately over-collects, and every classification below is a candidate
for adjudication.

Directions and modes:

- FULL (default): exhaustive both ways. Every in-scope reference item is classified
  by corpus usage (WELL-CITED / THIN / UNCITED / NO-KEY), and every corpus document
  gets a candidate list of topic-matching items it does not cite.
- --docs P [P ...]: the per-touch mode. For the named corpus documents only, emit
  the candidate set, filtered (when the doc-state file has a row for the document)
  to reference items ADDED or UPDATED in the reference repo since the recorded SHA,
  plus any topic match the document has never been audited against. --update-state
  rewrites the state rows for the named documents to the reference repo's current
  HEAD (intended to be committed with the PR's QA batch).
- --ref-since SHA (or --ref-items SUBSTR ...): the new-ingest direction. For the
  reference items changed since SHA (or matching the substrings), list the corpus
  documents that topically match and do not cite them.

Trust tiers (maintainer decisions, 2026-07-08): standards, frameworks, legislation,
and programs are AUTHORITATIVE (citation-grade suggestions); templates are
TEMPLATE-tier (template-content improvement suggestions, not citation authorities);
books are RECOMMENDATION-tier only (never authoritative; a book-sourced suggestion
must be corroborated against a trusted source before anything normative rests on
it); publications are EXCLUDED unless --include-publications (screen-first tier,
pending the publications-assessment process).

Honest limits: citation detection derives lexical keys from catalogue titles
(NIST / ISO / FIPS identifier shapes, parenthesized acronyms, curated aliases in
``reference-breadth-aliases.json``); items with no derivable key are reported as
NO-KEY for alias curation rather than silently guessed. Topic matching maps corpus
domain directories and text keywords onto the reference base's controlled topic
vocabulary; it is a recall heuristic. The judge decides; this tool narrows.

Usage:
    python3 tools/audit-reference-breadth.py [--ref-base PATH]
    python3 tools/audit-reference-breadth.py --docs privacy/policy-privacy.md --update-state
    python3 tools/audit-reference-breadth.py --ref-since <sha>
    python3 tools/audit-reference-breadth.py --ref-items "ATT&CK" "27701"

Stdlib-only Python 3.11. The catalogue parser is keyed to the GENERATED
catalogue.yml format (do-not-hand-edit header, 2-space item indent, 4-space
fields, inline topic lists); a format change fails loudly, never silently.
"""

from __future__ import annotations

import argparse
import json
import re
import signal
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REF_BASE = REPO_ROOT.parent / "grc_library_ref"
DEFAULT_ALIASES = Path(__file__).resolve().parent / "reference-breadth-aliases.json"
DEFAULT_STATE = REPO_ROOT / ".working" / "reference-audit" / "doc-state.md"

AUTHORITATIVE_BUCKETS = ("standards", "frameworks", "legislation", "programs")
TIER_BY_BUCKET = {
    "standards": "authoritative",
    "frameworks": "authoritative",
    "legislation": "authoritative",
    "programs": "authoritative",
    "templates": "template",
    "books": "recommendation",
    "publications": "screen-first",
}
EXCLUDED_BUCKETS_DEFAULT = ("publications",)

CORPUS_DIRS = (
    "ai", "architecture", "compliance", "dev-security", "governance",
    "operations", "privacy", "resilience", "risk", "security", "supply-chain",
)
# The scan set is INCLUDE-based: the citable corpus surface only. Registers
# (.project-governance/), working state (.working/), the CHANGELOG/TODO, and
# generated artefacts (docs/portal.md, docs/maturity-scorecard.md) are excluded
# so a mention there neither counts as corpus usage nor draws candidates.
INCLUDE_ROOT_FILES = (
    "README.md", "specification-master-project.md", "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
)
EXCLUDE_FILES = ("docs/portal.md", "docs/maturity-scorecard.md")

# Corpus domain directory -> reference topic vocabulary (recall heuristic; the
# vocabulary is grc_library_ref/topics.md's controlled set).
DIR_TOPICS = {
    "ai": {"ai", "ai-security", "risk-management"},
    "architecture": {"cybersecurity", "cloud-security", "governance"},
    "compliance": {"controls-frameworks", "law", "governance", "privacy"},
    "dev-security": {"appsec", "cybersecurity", "ai-security"},
    "governance": {"governance", "risk-management", "controls-frameworks"},
    "operations": {"cybersecurity", "resilience", "incident-response"},
    "privacy": {"privacy", "law"},
    "resilience": {"resilience", "incident-response", "risk-management"},
    "risk": {"risk-management", "governance"},
    "security": {"cybersecurity", "controls-frameworks", "incident-response",
                 "cloud-security"},
    "supply-chain": {"cybersecurity", "risk-management", "controls-frameworks",
                     "supply-chain-security"},
}
# Topic -> body-text keyword signals (adds topics beyond the directory default).
# Every tag in the reference base's 21-tag controlled vocabulary (topics.md) is
# reachable through DIR_TOPICS or a keyword row here; an unreachable tag would
# silently zero out its items' candidate matching.
TOPIC_KEYWORDS = {
    "ai": ("artificial intelligence", " llm", "machine learning"),
    "ai-security": ("prompt injection", "model poisoning", "adversarial"),
    "agentic-ai": ("agentic", "ai agent"),
    "privacy": ("personal data", "data subject", "privacy"),
    "law": ("regulation", "directive", "statute", "jurisdiction"),
    "cloud-security": ("cloud", "iaas", "saas"),
    "incident-response": ("incident response", "breach notification"),
    "resilience": ("business continuity", "disaster recovery", "resilience"),
    "appsec": ("secure development", "application security", "owasp"),
    "risk-management": ("risk assessment", "risk register", "risk treatment"),
    "controls-frameworks": ("control", "framework alignment"),
    "governance": ("governance", "accountability", "policy"),
    "cybersecurity": ("security",),
    "identity": ("identity and access", "access management", "authentication",
                 "workload identity"),
    "threat-intelligence": ("threat intelligence", "threat actor", "att&ck",
                            "indicators of compromise"),
    "offensive-security": ("penetration test", "red team",
                           "adversary emulation"),
    "vulnerability-management": ("vulnerability management", "attack surface",
                                 "cvss"),
    "threat-modeling": ("threat model",),
    "zero-trust": ("zero trust",),
    "supply-chain-security": ("supply chain", "supplier", "third-party"),
    "data-governance": ("data governance", "data sharing", "data act"),
}

ISO_TITLE_RE = re.compile(
    r"\b(?:ISO|IEC)(?:/IEC)?(?:/IEEE)?\s*(?:TR|TS|PAS)?\s*(\d{4,5})(?:-(\d+))?")
NIST_ID_RE = re.compile(
    r"\b(SP\s?\d{3,4}(?:-\d+[A-Za-z]?)?|AI\s?\d{3}-\d+e?\d*|FIPS\s?\d{2,3}(?:-\d)?|"
    r"IR\s?\d{4}[A-Za-z]?|CSWP\s?\d+)"
)
EU_NUM_RE = re.compile(r"\b(\d{4}/\d{2,4})\b")
CFR_RE = re.compile(r"\b(\d{1,2}\s?CFR\s?Part\s?\d{2,3})\b")
ETSI_EN_RE = re.compile(r"\bEN\s?(\d{3}\s?\d{3})\b")
IEEE_STD_RE = re.compile(r"\bIEEE\s+Std\s+(\d{3,4}(?:\.\d+)?)\b")
PAREN_ACRONYM_RE = re.compile(r"\(([A-Z][A-Za-z0-9&\- ]{1,40})\)")
CAPS_RUN_RE = re.compile(r"\b([A-Z][A-Z0-9&\.\-]{2,}(?:\s+[A-Z][A-Z0-9&\.\-]{1,})*)\b")


@dataclass
class RefItem:
    bucket: str
    title: str
    path: str = ""
    original: str = ""
    topics: set[str] = field(default_factory=set)
    tier: str = ""
    keys: list[str] = field(default_factory=list)
    cited_by: dict[str, int] = field(default_factory=dict)

    @property
    def ident(self) -> str:
        return f"{self.bucket}:{self.title}"


def parse_catalogue(ref_base: Path) -> list[RefItem]:
    """Line-based parser keyed to the generated catalogue.yml format."""
    cat = ref_base / "catalogue.yml"
    if not cat.is_file():
        raise RuntimeError(f"catalogue not found: {cat}")
    items: list[RefItem] = []
    bucket = None
    cur: RefItem | None = None
    bucket_re = re.compile(r"^([a-z_]+):\s*$")
    item_re = re.compile(r'^  - title:\s*"(.*)"\s*$')
    field_re = re.compile(r'^    ([a-z_]+):\s*(.*?)\s*$')
    for raw in cat.read_text(encoding="utf-8", errors="replace").splitlines():
        if raw.startswith("#") or not raw.strip():
            continue
        m = bucket_re.match(raw)
        if m:
            bucket = m.group(1)
            continue
        m = item_re.match(raw)
        if m:
            if bucket is None:
                raise RuntimeError("catalogue format drift: item before bucket")
            cur = RefItem(bucket=bucket, title=m.group(1),
                          tier=TIER_BY_BUCKET.get(bucket, "unknown"))
            items.append(cur)
            continue
        m = field_re.match(raw)
        if m and cur is not None:
            key, val = m.group(1), m.group(2)
            if key == "path":
                cur.path = val.strip('"')
            elif key == "original":
                cur.original = val.strip('"')
            elif key == "topics":
                cur.topics = set(re.findall(r'"([^"]+)"', val))
    if not items:
        raise RuntimeError("catalogue format drift: zero items parsed")
    return items


def derive_keys(item: RefItem, aliases: dict[str, list[str]]) -> list[str]:
    keys: list[str] = list(aliases.get(item.title, []))
    t = item.title
    m = ISO_TITLE_RE.search(t)
    if m:
        keys.append(m.group(1) + (f"-{m.group(2)}" if m.group(2) else ""))
    for nid in NIST_ID_RE.findall(t):
        nid = re.sub(r"\s+", " ", nid)
        # "SP 800-53" cites as the bare series-number "800-53"; "SP 1270" as-is.
        keys.append(re.sub(r"^SP\s?", "", nid) if re.match(r"SP\s?\d{3}-", nid)
                    else nid)
    if item.bucket == "legislation":
        keys.extend(EU_NUM_RE.findall(t))
        keys.extend(CFR_RE.findall(t))
    if item.bucket == "standards":
        keys.extend(ETSI_EN_RE.findall(t))
        keys.extend(IEEE_STD_RE.findall(t))
    for ac in PAREN_ACRONYM_RE.findall(t):
        ac = ac.strip()
        if 2 <= len(ac) <= 12 and " " not in ac:
            keys.append(ac)
    if item.bucket in ("frameworks", "programs", "legislation") and not keys:
        run = CAPS_RUN_RE.search(t)
        if run and len(run.group(1)) >= 3 and "." not in run.group(1):
            keys.append(run.group(1))
    # Dedupe, drop too-generic keys.
    out, seen = [], set()
    for k in keys:
        k = k.strip()
        if len(k) < 3 or k.lower() in {"the", "and", "for"}:
            continue
        if k.lower() not in seen:
            seen.add(k.lower())
            out.append(k)
    return out


def tracked_corpus_md(root: Path) -> list[str]:
    out = subprocess.run(["git", "-C", str(root), "ls-files", "*.md"],
                         capture_output=True, text=True, check=True)
    files = []
    for rel in out.stdout.splitlines():
        if not rel or rel in EXCLUDE_FILES:
            continue
        top = rel.split("/", 1)[0]
        if top in CORPUS_DIRS or rel.startswith("docs/") \
                or rel in INCLUDE_ROOT_FILES:
            files.append(rel)
    return files


def key_regex(key: str) -> re.Pattern:
    # Separator-tolerant bare-token match: "27001" must not match "270010".
    esc = re.escape(key).replace(r"\ ", r"[\s ]?")
    return re.compile(r"(?<![\w-])" + esc + r"(?![\w])", re.IGNORECASE)


def doc_topics(rel: str, text: str) -> set[str]:
    top = rel.split("/")[0]
    topics = set(DIR_TOPICS.get(top, set()))
    low = text.lower()
    for topic, kws in TOPIC_KEYWORDS.items():
        if any(kw in low for kw in kws):
            topics.add(topic)
    return topics


def load_state(path: Path) -> dict[str, str]:
    state: dict[str, str] = {}
    if not path.is_file():
        return state
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^\|\s*`?([^|`]+?)`?\s*\|\s*([0-9a-f]{7,40})\s*\|", ln)
        if m and "/" in m.group(1):
            state[m.group(1).strip()] = m.group(2)
    return state


def write_state(path: Path, state: dict[str, str], ref_head: str,
                docs: list[str], today: str) -> None:
    for d in docs:
        state[d] = ref_head
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Reference-audit per-document state",
        "",
        "Maps each corpus document to the grc_library_ref commit at its last",
        "per-document reference audit (the /reference-audit --docs mode's delta",
        "anchor). Live surface: non-dated, stays in-repo under the current-week",
        "sweep model. Rewritten by tools/audit-reference-breadth.py --update-state;",
        "commit the refresh with the touching PR's QA batch.",
        "",
        "| Document | Ref SHA at last audit | Updated (UTC) |",
        "| --- | --- | --- |",
    ]
    for doc in sorted(state):
        lines.append(f"| `{doc}` | {state[doc]} | {today} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def ref_changed_paths(ref_base: Path, since: str) -> set[str]:
    out = subprocess.run(["git", "-C", str(ref_base), "diff", "--name-only",
                          f"{since}..HEAD"], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"ref diff failed for {since}: {out.stderr.strip()}")
    return {ln for ln in out.stdout.splitlines() if ln}


def item_touched(item: RefItem, changed: set[str]) -> bool:
    return any(p and any(c == p or c.startswith(p) for c in changed)
               for p in (item.path, item.original))


def main(argv: list[str] | None = None) -> int:
    # A truncated pipe consumer (for example ``| head``) should terminate this
    # dev-aid cleanly via SIGPIPE rather than raise a BrokenPipeError traceback;
    # restore the default disposition so a broken pipe is a clean exit.
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ref-base", type=Path, default=DEFAULT_REF_BASE)
    ap.add_argument("--aliases", type=Path, default=DEFAULT_ALIASES)
    ap.add_argument("--state", type=Path, default=DEFAULT_STATE)
    ap.add_argument("--docs", nargs="+", default=None,
                    help="Per-touch mode: corpus documents to assess.")
    ap.add_argument("--update-state", action="store_true",
                    help="With --docs: record ref HEAD for the named documents.")
    ap.add_argument("--ref-since", default=None,
                    help="New-ingest mode: reference items changed since this SHA.")
    ap.add_argument("--ref-items", nargs="+", default=None,
                    help="New-ingest mode: reference items whose title matches.")
    ap.add_argument("--include-publications", action="store_true")
    ap.add_argument("--max-candidates-per-doc", type=int, default=10)
    args = ap.parse_args(argv)

    # Adopter graceful-degradation (TODO 3.91): with no reachable reference base (the
    # DEFAULT ref-base, not an explicit --ref-base override, and no grc_library_ref
    # sibling holding a catalogue), no-op exit 0 rather than crash, so a bare adopter
    # clone runs this maintainer-only advisory green. An EXPLICIT --ref-base that is bad
    # still falls through to parse_catalogue's error (typo guard). For the maintainer, a
    # missing _ref is caught loud at /resume (the §1.19.7 loud gate), not silently here.
    if args.ref_base == DEFAULT_REF_BASE and not (args.ref_base / "catalogue.yml").is_file():
        print("audit-reference-breadth: grc_library_ref not present; no-op "
              "(reference-breadth is a maintainer-only advisory, nothing to report).")
        return 0

    try:
        ref_base = args.ref_base.resolve()
        items = parse_catalogue(ref_base)
        aliases = (json.loads(args.aliases.read_text(encoding="utf-8"))
                   if args.aliases.is_file() else {})
        excluded = () if args.include_publications else EXCLUDED_BUCKETS_DEFAULT
        items = [i for i in items if i.bucket not in excluded]
        for it in items:
            it.keys = derive_keys(it, aliases)
        corpus = tracked_corpus_md(REPO_ROOT)
        ref_head = subprocess.run(
            ["git", "-C", str(ref_base), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()
    except (RuntimeError, OSError, subprocess.CalledProcessError,
            json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    # Scan corpus once: per-doc text, topics, and per-item citation hits.
    doc_text: dict[str, str] = {}
    doc_topic: dict[str, set[str]] = {}
    keyed = [(it, [key_regex(k) for k in it.keys]) for it in items if it.keys]
    for rel in corpus:
        try:
            text = (REPO_ROOT / rel).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        doc_text[rel] = text
        doc_topic[rel] = doc_topics(rel, text)
        for it, regs in keyed:
            n = sum(len(r.findall(text)) for r in regs)
            if n:
                it.cited_by[rel] = n

    def classify(it: RefItem) -> str:
        if not it.keys:
            return "NO-KEY"
        if not it.cited_by:
            return "UNCITED"
        return "THIN" if len(it.cited_by) <= 2 else "WELL-CITED"

    def candidates_for(rel: str, pool: list[RefItem]) -> list[RefItem]:
        topics = doc_topic.get(rel, set())
        cands = [it for it in pool
                 if it.topics & topics and rel not in it.cited_by]
        # Strongest topical overlap first, so a capped display stays useful.
        cands.sort(key=lambda it: (-len(it.topics & topics), it.title))
        return cands

    today = subprocess.run(["date", "-u", "+%Y-%m-%d"], capture_output=True,
                           text=True).stdout.strip()
    print(f"# Reference-breadth worklist (corpus {REPO_ROOT.name}, "
          f"ref {ref_base.name} at {ref_head}, {today})\n")
    counts = {"WELL-CITED": 0, "THIN": 0, "UNCITED": 0, "NO-KEY": 0}
    for it in items:
        counts[classify(it)] += 1
    print(f"In-scope reference items: {len(items)} "
          f"({', '.join(f'{b} {sum(1 for i in items if i.bucket == b)}' for b in sorted({i.bucket for i in items}))}); "
          f"excluded buckets: {', '.join(excluded) or 'none'}. Corpus documents "
          f"scanned: {len(corpus)}. Classification: "
          f"{counts['WELL-CITED']} well-cited, {counts['THIN']} thin, "
          f"{counts['UNCITED']} uncited, {counts['NO-KEY']} no-key (no "
          f"derivable citation key: curate an alias, or expected for books, "
          f"which are engaged by topic rather than cited by identifier).\n")
    print("Recall-oriented worklist, NOT a defect list; the semantic judge "
          "adjudicates every row. Tier semantics: authoritative buckets support "
          "citation-grade suggestions; template tier supports template-content "
          "improvements; recommendation tier (books) is never authoritative and "
          "requires corroboration before anything normative.\n")

    if args.docs:
        state = load_state(args.state)
        assessed: list[str] = []
        for rel in args.docs:
            if rel not in doc_text:
                print(f"## {rel}\n\nNOT FOUND in scanned corpus set (domain "
                      f"dirs, docs/, and the root citable documents only); "
                      f"check the path.\n")
                continue
            assessed.append(rel)
            pool = items
            anchor = state.get(rel)
            note = "never audited: all topic matches are candidates"
            if anchor:
                try:
                    changed = ref_changed_paths(ref_base, anchor)
                except RuntimeError as exc:
                    changed, note = None, f"state SHA unusable ({exc}); full set"
                if changed is not None:
                    pool = [it for it in items if item_touched(it, changed)]
                    note = (f"delta since ref {anchor}: {len(pool)} item(s) "
                            f"added/updated")
            cands = candidates_for(rel, pool)
            print(f"## Per-touch candidates: {rel}\n\n({note}; topics "
                  f"{sorted(doc_topic[rel])}; {len(cands)} candidate(s))\n")
            for it in cands:
                print(f"- [{it.tier}] {it.title} (`{it.path or it.original}`; "
                      f"topics {sorted(it.topics)})")
            print()
        if args.update_state:
            if assessed:
                write_state(args.state, state, ref_head, assessed, today)
            print(f"State updated for {len(assessed)} assessed document(s) "
                  f"(of {len(args.docs)} named) at ref {ref_head}: "
                  f"{args.state}")
        return 0

    if args.ref_since or args.ref_items:
        if args.ref_since:
            try:
                changed = ref_changed_paths(ref_base, args.ref_since)
            except RuntimeError as exc:
                print(f"ERROR: {exc}", file=sys.stderr)
                return 2
            sel = [it for it in items if item_touched(it, changed)]
            print(f"## New-ingest direction: {len(sel)} item(s) changed since "
                  f"{args.ref_since}\n")
        else:
            subs = [s.lower() for s in args.ref_items]
            sel = [it for it in items if any(s in it.title.lower() for s in subs)]
            print(f"## New-ingest direction: {len(sel)} item(s) matching "
                  f"{args.ref_items}\n")
        for it in sel:
            matches = [(len(it.topics & doc_topic.get(rel, set())), rel)
                       for rel in corpus
                       if it.topics & doc_topic.get(rel, set())
                       and rel not in it.cited_by]
            matches.sort(key=lambda m: (-m[0], m[1]))
            print(f"### [{it.tier}] {it.title}\n\nKeys: {it.keys or 'NO-KEY'}; "
                  f"cited by {len(it.cited_by)} doc(s); {len(matches)} "
                  f"topic-matching uncited doc(s), strongest overlap first:")
            for ov, rel in matches[:args.max_candidates_per_doc]:
                print(f"- {rel} (topic overlap {ov})")
            if len(matches) > args.max_candidates_per_doc:
                print(f"- ... plus {len(matches) - args.max_candidates_per_doc} "
                      f"more (capped for display, count is complete)")
            print()
        return 0

    # FULL mode: exhaustive item table, then per-doc candidate summary.
    print("## Per-item usage (exhaustive)\n")
    print("| Item | Bucket | Tier | Keys | Cited by | Class |")
    print("| --- | --- | --- | --- | --- | --- |")
    for it in sorted(items, key=lambda i: (i.bucket, i.title)):
        cited = f"{len(it.cited_by)} doc(s)"
        keys = "; ".join(it.keys) if it.keys else "NO-KEY"
        print(f"| {it.title} | {it.bucket} | {it.tier} | {keys} | {cited} | "
              f"{classify(it)} |")
    print("\n## Per-document enhancement candidates (capped display; counts "
          "complete)\n")
    for rel in sorted(corpus):
        cands = candidates_for(rel, items)
        if not cands:
            continue
        shown = cands[:args.max_candidates_per_doc]
        extra = len(cands) - len(shown)
        names = "; ".join(f"[{c.tier}] {c.title}" for c in shown)
        tail = f" ... plus {extra} more" if extra > 0 else ""
        print(f"- {rel} ({len(cands)}): {names}{tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
