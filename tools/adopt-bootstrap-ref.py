#!/usr/bin/env python3
"""Adopter `.ref` bootstrap planner (TODO section 1.19.7 part c).

WHAT IT DOES. Reads the committed public reference-acquisition manifest
(`docs/reference-acquisition-manifest.md`, itself generated from grc_library_ref's
trusted-bucket catalogue by `tools/build-reference-manifest.py`) and emits a
CATEGORIZED ACQUISITION PLAN a fork adopter uses to build their OWN external
`grc_library_ref` reference base:

  - **auto-fetchable**  : acquisition FREE *and* an upstream URL is recorded, so the
                          `/adopt`-running assistant can WebFetch it directly.
  - **free-manual**     : acquisition FREE but no upstream URL recorded yet, so the
                          adopter locates and downloads it manually.
  - **licensed-manual** : acquisition LICENSED, so the adopter acquires it under the
                          issuer's licence (purchase / membership / paywall).

WHY A PLANNER, NOT A FETCHER. This tool NEVER fetches, downloads, or writes anything:
it only READS the committed public manifest (bibliographic metadata: title, issuer,
version, upstream URL, acquisition class) and prints a plan. The actual fetching is the
`/adopt` assistant's job (WebFetch of the auto-fetchable list INTO the adopter's EXTERNAL
`grc_library_ref` sibling), governed by two guardrails the skill enforces: never fetch
into an in-repo `.ref` STUB (a payload-bearing declared stub hard-fails the stub-guard gate;
a functional in-repo `.ref` is the adopter's own real sibling, out of the gate's scope), and
never redistribute licensed content (only FREE sources are auto-fetched; LICENSED items
are listed for the adopter to acquire lawfully). Keeping the tool network-free and
write-free keeps it stdlib-only and side-effect-free, and keeps the copyright boundary
in the assistant + skill layer where the human is in the loop.

ADOPTER-PORTABLE. It reads ONLY the in-repo committed manifest, so it needs NO sibling
repositories and runs green on a bare adopter clone (the sibling-independence invariant).
It is NOT an audit gate and is NOT wired into run_all_audits; it is an on-demand planner
the `/adopt` skill invokes.

Exit codes: 0 = plan emitted (or a clean empty manifest); 2 = the manifest is missing or
unparseable (a broken clone).
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "docs" / "reference-acquisition-manifest.md"
BUCKET_HEADING = re.compile(r"^##\s+(Standards|Frameworks|Legislation|Programs)\b")
# A manifest table row: | title | version | issuer | url | ACQUISITION |
# The acquisition cell (FREE / LICENSED) anchors a genuine data row, so header and
# separator rows (which have no such cell) are skipped without a position heuristic.
ROW = re.compile(
    r"^\|(?P<title>[^|]*)\|(?P<version>[^|]*)\|(?P<issuer>[^|]*)\|"
    r"(?P<url>[^|]*)\|\s*(?P<acq>FREE|LICENSED)\s*\|\s*$"
)


def parse_manifest(text: str) -> list[dict]:
    """Return [{bucket, title, version, issuer, url, acquisition}, ...] from the
    manifest's per-bucket tables. Keyed on the FREE/LICENSED acquisition cell, so
    only genuine data rows are captured (header/separator rows carry no such cell)."""
    entries: list[dict] = []
    bucket = None
    for raw in text.splitlines():
        h = BUCKET_HEADING.match(raw)
        if h:
            bucket = h.group(1)
            continue
        m = ROW.match(raw)
        if m:
            entries.append({
                "bucket": bucket or "",
                "title": m.group("title").strip(),
                "version": m.group("version").strip(),
                "issuer": m.group("issuer").strip(),
                "url": m.group("url").strip(),
                "acquisition": m.group("acq").strip().lower(),
            })
    return entries


def categorize(entries: list[dict]) -> dict:
    """Split entries into the three acquisition classes the adopter acts on."""
    plan: dict = {"auto_fetchable": [], "free_manual": [], "licensed_manual": []}
    for e in entries:
        if e["acquisition"] == "free" and e["url"]:
            plan["auto_fetchable"].append(e)
        elif e["acquisition"] == "free":
            plan["free_manual"].append(e)
        else:
            plan["licensed_manual"].append(e)
    return plan


_GUARDRAIL = (
    "GUARDRAILS (the /adopt skill enforces these): fetch the AUTO-FETCHABLE sources into "
    "your EXTERNAL grc_library_ref sibling ONLY, NEVER into an in-repo .ref STUB (a "
    "payload-bearing declared stub hard-fails the stub-guard gate); NEVER redistribute LICENSED content, acquire "
    "each licensed item lawfully under its issuer's terms."
)


def _render_text(plan: dict) -> str:
    out: list[str] = []
    total = sum(len(v) for v in plan.values())
    out.append("Adopter grc_library_ref bootstrap plan")
    out.append("=" * 39)
    out.append(f"{total} trusted-bucket source(s): "
               f"{len(plan['auto_fetchable'])} auto-fetchable (FREE + URL), "
               f"{len(plan['free_manual'])} free-manual (FREE, no URL recorded), "
               f"{len(plan['licensed_manual'])} licensed-manual.")
    out.append("")
    out.append(_GUARDRAIL)
    labels = [
        ("auto_fetchable", "AUTO-FETCHABLE (FREE + upstream URL): WebFetch into the external sibling"),
        ("free_manual", "FREE-MANUAL (no URL recorded yet): locate + download manually"),
        ("licensed_manual", "LICENSED-MANUAL: acquire lawfully under the issuer's terms"),
    ]
    for key, label in labels:
        rows = plan[key]
        out.append("")
        out.append(f"## {label} ({len(rows)})")
        for e in rows:
            suffix = f"  <{e['url']}>" if e["url"] else ""
            out.append(f"  - [{e['bucket']}] {e['title']} ({e['issuer']}){suffix}")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Adopter grc_library_ref bootstrap planner "
                                             "(reads the committed manifest; never fetches).")
    ap.add_argument("--json", action="store_true",
                    help="emit the categorized plan as JSON (for the /adopt assistant to drive).")
    ap.add_argument("--manifest", default=str(MANIFEST),
                    help="manifest path (default: the committed docs/ manifest).")
    args = ap.parse_args(argv)

    path = Path(args.manifest)
    if not path.is_file():
        print(f"adopt-bootstrap-ref: manifest not found at {path} (broken clone?).",
              file=sys.stderr)
        return 2
    entries = parse_manifest(path.read_text(encoding="utf-8"))
    plan = categorize(entries)
    if args.json:
        print(json.dumps({"guardrails": _GUARDRAIL, "counts": {k: len(v) for k, v in plan.items()},
                          "plan": plan}, indent=2))
    else:
        print(_render_text(plan), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
