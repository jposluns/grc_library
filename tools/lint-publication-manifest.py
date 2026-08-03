#!/usr/bin/env python3
"""Validate the AIQT Guardrails publication manifest against the live pack tree.

The manifest ``tools/publication-manifest.json`` classifies every file under
``guardrails/`` for the one-way publication of the portable core: each file is
CORE (publishes), ADAPTER-INPUT (a coding-agent adapter-generator source),
GRC-ONLY (stays in grc_library), or EXCLUDED, with a disclosure status
(PUBLIC / SANITIZE / WITHHELD). Origin: TODO 1.26.5, a dual-family (Opus-5 +
Codex) classification reconciled and Fable-confirmed, maintainer GO 2026-08-03.

This gate is the machine-validation the manifest exists to earn: it fails when

  * a ``guardrails/`` file has no manifest entry (an unclassified file could be
    published or withheld by accident), or
  * a manifest entry names a path that is not on disk (a stale entry), or
  * an entry carries a bucket or disclosure value outside the allowed set.

It is stdlib-only and fails closed (any discrepancy is a non-zero exit), so a
file added to the pack without a classification decision blocks the build.

The decision is a pure function (``evaluate``) over a tree set and a manifest
mapping, so both the observer (``pack_files``) and the decision are testable in
isolation.

Usage:
    python3 tools/lint-publication-manifest.py
    python3 tools/lint-publication-manifest.py --check   (alias; same behaviour)

Exit codes:
    0   manifest and tree are in sync and every value is valid
    1   one or more discrepancies present
    2   the manifest file is missing or unparseable
"""
from __future__ import annotations

import argparse
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK_DIR = os.path.join(REPO_ROOT, "guardrails")
MANIFEST = os.path.join(REPO_ROOT, "tools", "publication-manifest.json")

BUCKETS = {"CORE", "ADAPTER-INPUT", "GRC-ONLY", "EXCLUDED"}
DISCLOSURES = {"PUBLIC", "SANITIZE", "WITHHELD"}


def pack_files(pack_dir: str = PACK_DIR) -> set:
    """Every file under the pack dir, path relative to it (the observer)."""
    found = set()
    for dirpath, _dirs, names in os.walk(pack_dir):
        for name in names:
            full = os.path.join(dirpath, name)
            found.add(os.path.relpath(full, pack_dir))
    return found


def evaluate(tree: set, entries: dict) -> dict:
    """Pure decision: given the pack tree and the manifest 'files' mapping,
    return the four finding lists. No filesystem access."""
    classified = set(entries)
    return {
        "unclassified": sorted(tree - classified),
        "orphans": sorted(classified - tree),
        "bad_bucket": sorted(p for p, v in entries.items() if v.get("bucket") not in BUCKETS),
        "bad_disclosure": sorted(p for p, v in entries.items() if v.get("disclosure") not in DISCLOSURES),
    }


def main(argv: list) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the manifest (default behaviour; flag accepted for CI symmetry)",
    )
    parser.parse_args(argv[1:])

    if not os.path.isfile(MANIFEST):
        print(f"ERROR: manifest not found: {MANIFEST}")
        return 2
    try:
        with open(MANIFEST, encoding="utf-8") as handle:
            entries = json.load(handle)["files"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"ERROR: manifest unparseable or missing 'files' key: {exc}")
        return 2

    result = evaluate(pack_files(), entries)
    findings = 0
    labels = {
        "unclassified": ("UNCLASSIFIED", "pack files with no manifest entry", "guardrails/{}"),
        "orphans": ("ORPHAN", "manifest entries whose path is not on disk", "{}"),
        "bad_bucket": ("BAD BUCKET", f"value not in {sorted(BUCKETS)}", "{}"),
        "bad_disclosure": ("BAD DISCLOSURE", f"value not in {sorted(DISCLOSURES)}", "{}"),
    }
    for key, (tag, desc, fmt) in labels.items():
        hits = result[key]
        if hits:
            findings += len(hits)
            print(f"{tag} ({len(hits)}): {desc}:")
            for p in hits:
                print(f"    {fmt.format(p)}")

    if findings:
        print(f"\nFAIL: {findings} publication-manifest discrepancy(ies).")
        return 1
    print(f"OK: {len(entries)} pack files classified, manifest in sync with guardrails/.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
