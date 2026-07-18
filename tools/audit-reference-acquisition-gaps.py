#!/usr/bin/env python3
"""Reference-acquisition gap worklist: standards the corpus CITES but the
reference base does NOT hold.

WHAT THIS IS (and is NOT). An orchestrator dev-AID feeding the not-held-source
direction of the /reference-audit cadence (#718, closing the reference-audit spec item
(d)), not an audit gate. It always exits 0 after printing its report (2 only on
internal or usage error); CI cannot host it because the ground truth lives in the
sibling private reference repo. Its companion `tools/audit-reference-breadth.py`
answers the HELD -> corpus direction (does the corpus use what we hold); this tool
answers the CITED -> not-held direction (does the corpus cite a source we do not
hold, so it is an acquisition candidate for the ref-base acquisition queue and the
maintainer source-drop list).

It is deliberately the tractable half of the not-held-source problem (#718). The
untractable half ("what authoritative sources exist upstream that we neither cite
nor hold") a tool cannot know and stays judge-led and ad-hoc in the skill. This
tool measures the KNOWN gap: the corpus's own canonical citations register
(`governance/register-canonical-citations.md`, the single source of truth for what
the corpus cites) diffed against the reference catalogue's held items. An entry the
corpus cites by name/number but no held item matches is a candidate to ACQUIRE (or
to confirm is deliberately reference-only, not full-text-held).

Honest limits: this is a recall-oriented WORKLIST, never a defect list. A
"not-held" candidate is a prompt for the maintainer to decide acquire-vs-skip, not
an error: many cited standards are legitimately cited-not-held (the corpus cites the
control identifier; the full text is not needed in the base). Matching is lexical
(the same ISO/NIST/EU identifier-shape keys `audit-reference-breadth.py` derives,
plus soft-law name matching); a near-miss can mis-classify, so the judge confirms
each row against the ref index before it enters the acquisition queue. The known
residual false-positive class is an acronym the register cites versus its
spelled-out held title where the numeric bridge and the topic expansion both miss
(e.g. "OWASP LLM Top 10" where the held title reads "Large Language Model"); these
over-report as not-held and the judge clears them. The complementary risk, a
promiscuous topic-token match wrongly marking an unheld source held, is bounded by
requiring at least two significant topic tokens to co-occur in one held title.

Usage:
    python3 tools/audit-reference-acquisition-gaps.py [--ref-base PATH]
    python3 tools/audit-reference-acquisition-gaps.py --section "NIST publications"

Stdlib-only Python 3.11. The register parser is keyed to the canonical register's
table format (Standard ID in column 1, `## ` section family headers); a format
change fails loudly, never silently.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REF_BASE = REPO_ROOT.parent / "grc_library_ref"
DEFAULT_ALIASES = Path(__file__).resolve().parent / "reference-breadth-aliases.json"
CANONICAL_REGISTER = REPO_ROOT / "governance" / "register-canonical-citations.md"

# Identifier-shape key derivation, shared in spirit with
# audit-reference-breadth.py (kept local so this tool is standalone; the shapes
# are the same, so a register "ISO/IEC 27001" and a catalogue
# "ISO/IEC 27001:2022 ..." both derive the key "27001").
ISO_RE = re.compile(r"\b(?:ISO|IEC)(?:/IEC)?(?:/IEEE)?\s*(?:TR|TS|PAS)?\s*(\d{4,5})(?:-(\d+))?")
NIST_RE = re.compile(
    r"\b(SP\s?\d{3,4}(?:-\d+[A-Za-z]?)?|AI\s?\d{3}(?:-\d+[a-z]?\d*)?|FIPS\s?\d{2,3}(?:-\d)?|"
    r"IR\s?\d{4}[A-Za-z]?|CSWP\s?\d+)")
EU_NUM_RE = re.compile(r"\b(\d{4}/\d{2,4})\b")
CFR_RE = re.compile(r"\b(\d{1,2}\s?CFR\s?(?:Part\s?)?\d{2,3})\b")
ETSI_RE = re.compile(r"\bEN\s?(\d{3}\s?\d{3})\b")
IEEE_RE = re.compile(r"\bIEEE\s+(?:Std\s+)?(\d{3,4}(?:\.\d+)?)\b")


def derive_keys(text: str) -> list[str]:
    keys: list[str] = []
    m = ISO_RE.search(text)
    if m:
        keys.append(m.group(1) + (f"-{m.group(2)}" if m.group(2) else ""))
    for nid in NIST_RE.findall(text):
        nid = re.sub(r"\s+", " ", nid)
        keys.append(re.sub(r"^SP\s?", "", nid) if re.match(r"SP\s?\d{3}-", nid) else nid)
    keys.extend(EU_NUM_RE.findall(text))
    keys.extend(CFR_RE.findall(text))
    keys.extend(ETSI_RE.findall(text))
    keys.extend(IEEE_RE.findall(text))
    # Normalize whitespace inside keys and dedupe.
    out, seen = [], set()
    for k in keys:
        k = re.sub(r"\s+", " ", k).strip()
        if len(k) >= 3 and k.lower() not in seen:
            seen.add(k.lower())
            out.append(k)
    return out


# Register families that catalogue SOFTWARE tools or running programmes rather
# than acquirable reference DOCUMENTS. Cited for awareness; not "held" as texts
# (the ref base itself skips tools, e.g. Threat Dragon: "tool, not citable text").
# Excluded from the acquisition worklist by default; --include-tooling overrides.
TOOLING_SECTIONS = frozenset({
    "AI security tooling references",
    "AI safety evaluation programmes",
})
SKIP_SECTIONS = frozenset({"Purpose", "Conventions", "Maintenance", "(preamble)"})
SEP_RE = re.compile(r"^\|[\s\-:|]+\|\s*$")


def parse_register(path: Path, include_tooling: bool) -> list[tuple[str, str, str, str]]:
    """Return (section, standard_id, topic_or_desc) per register data row.

    Only rows AFTER a table's separator line are data (this skips each family's
    column-header row, whose first cell varies: "Standard ID", "Project", ...).
    """
    if not path.is_file():
        raise RuntimeError(f"canonical register not found: {path}")
    rows: list[tuple[str, str, str]] = []
    section = "(preamble)"
    in_body = False
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        h = re.match(r"^##\s+(.*)$", raw)
        if h:
            section = h.group(1).strip()
            in_body = False
            continue
        if section in SKIP_SECTIONS:
            continue
        if not include_tooling and section in TOOLING_SECTIONS:
            continue
        if SEP_RE.match(raw):
            in_body = True
            continue
        if not (in_body and raw.startswith("|")):
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if not cells or not cells[0]:
            continue
        sid = cells[0]
        topic = cells[3] if len(cells) > 3 else (cells[1] if len(cells) > 1 else "")
        # Keep the whole row's text so key derivation and name matching can use
        # the version and topic columns (they carry the bridge: EU rows list
        # "Regulation 2024/1689" in the version column, and the Topic column
        # spells out an acronym, e.g. "Cloud Controls Matrix" for "CSA CCM").
        rows.append((section, sid, topic, " ".join(cells)))
    if not rows:
        raise RuntimeError("register format drift: zero rows parsed")
    return rows


def parse_catalogue_titles(ref_base: Path) -> list[str]:
    cat = ref_base / "catalogue.yml"
    if not cat.is_file():
        raise RuntimeError(f"catalogue not found: {cat}")
    titles = re.findall(r'^  - title:\s*"(.*)"\s*$',
                        cat.read_text(encoding="utf-8", errors="replace"), re.M)
    if not titles:
        raise RuntimeError("catalogue format drift: zero titles parsed")
    return titles


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ref-base", type=Path, default=DEFAULT_REF_BASE)
    ap.add_argument("--aliases", type=Path, default=DEFAULT_ALIASES)
    ap.add_argument("--section", default=None,
                    help="Restrict to one register family (## header text).")
    ap.add_argument("--include-tooling", action="store_true",
                    help="Include the software-tool / programme families (excluded by default).")
    args = ap.parse_args(argv)

    # Adopter graceful-degradation (TODO 3.91): default ref-base (no --ref-base
    # override) with no grc_library_ref catalogue -> no-op exit 0, so a bare adopter
    # clone runs this maintainer-only advisory green rather than crashing. An explicit
    # --ref-base that is bad still errors below (typo guard).
    if args.ref_base == DEFAULT_REF_BASE and not (args.ref_base / "catalogue.yml").is_file():
        print("audit-reference-acquisition-gaps: grc_library_ref not present; no-op "
              "(reference-acquisition-gap is a maintainer-only advisory, nothing to report).")
        return 0

    try:
        rows = parse_register(CANONICAL_REGISTER, args.include_tooling)
        titles = parse_catalogue_titles(args.ref_base.resolve())
        aliases = (json.loads(args.aliases.read_text(encoding="utf-8"))
                   if args.aliases.is_file() else {})
        today = subprocess.run(["date", "-u", "+%Y-%m-%d"], capture_output=True,
                               text=True).stdout.strip()
    except (RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    # Held-key index: every key derivable from any catalogue title, plus the
    # lowercased alias values (so a soft-law or name-only held item matches).
    held_keys: set[str] = set()
    for t in titles:
        held_keys.update(k.lower() for k in derive_keys(t))
    for vals in aliases.values():
        held_keys.update(v.lower() for v in vals)

    # Alphanumeric-only, no-space, lowercase normalization applied IDENTICALLY to
    # both the register id and the held titles, so punctuation differences
    # ("ATT&CK" vs "att ck") do not cause a spurious miss.
    def squash(s: str) -> str:
        return re.sub(r"[^a-z0-9]", "", s.lower())
    held_titles_sq = [squash(t) for t in titles]
    held_alias_sq = {squash(v) for vals in aliases.values() for v in vals}

    # Held-title token index for expansion matching (the register Topic spells
    # out an acronym; require its significant tokens to co-occur in one title).
    STOP = {"the", "and", "for", "of", "in", "on", "a", "an", "to", "with",
            "management", "system", "systems", "requirements", "guidelines"}
    held_title_tokensets = [set(re.findall(r"[a-z0-9]{3,}", t.lower())) for t in titles]

    def is_held(sid: str, topic: str, rowtext: str) -> bool:
        # 1. Numeric identifier anywhere in the row (col1 acronym rarely has one,
        #    but the version column does for EU regs, and the topic can too).
        keys = derive_keys(rowtext)
        if keys and any(k.lower() in held_keys for k in keys):
            return True
        # 2. Acronym / name substring under identical squash, or a held alias.
        name = re.sub(r"\s+v?\d+(\.\d+)*\s*$", "", sid)  # drop trailing version
        sq = squash(name)
        if len(sq) >= 5 and (sq in held_alias_sq or any(sq in ht for ht in held_titles_sq)):
            return True
        # 3. Topic-expansion token subset (e.g. "Cloud Controls Matrix" for the
        #    "CSA CCM" acronym): the topic's significant tokens all co-occur in
        #    one held title. Requires >= 2 significant tokens so a one-word topic
        #    cannot match promiscuously.
        toks = {w for w in re.findall(r"[a-z0-9]{3,}", topic.lower()) if w not in STOP}
        if len(toks) >= 2 and any(toks <= ts for ts in held_title_tokensets):
            return True
        return False

    gaps: dict[str, list[tuple[str, str]]] = {}
    total = held = 0
    for section, sid, topic, rowtext in rows:
        if args.section and section != args.section:
            continue
        total += 1
        if is_held(sid, topic, rowtext):
            held += 1
        else:
            gaps.setdefault(section, []).append((sid, topic))

    print(f"# Reference-acquisition gap worklist (corpus register vs "
          f"{args.ref_base.name}, {today})\n")
    print(f"Register entries examined: {total}; matched to a held reference item: "
          f"{held}; NOT held (acquisition candidates): {total - held}.\n")
    print("Recall-oriented worklist, NOT a defect list. A not-held row is a prompt "
          "to decide acquire-vs-skip (many cited standards are legitimately "
          "cited-not-held: the corpus cites the identifier, the full text is not "
          "needed in the base). The judge confirms each row against the ref index "
          "before it enters the acquisition queue.\n")
    if not gaps:
        print("No acquisition candidates in scope: every examined register entry "
              "matched a held reference item.")
        return 0
    for section in sorted(gaps):
        print(f"## {section} ({len(gaps[section])} not-held)\n")
        for sid, topic in gaps[section]:
            print(f"- {sid}" + (f" -- {topic}" if topic else ""))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
