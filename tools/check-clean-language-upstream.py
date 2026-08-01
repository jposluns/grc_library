#!/usr/bin/env python3
"""Clean-Language skill upstream-drift check (P-1.13): report when the vendored
`.claude/skills/clean-language/` skill has diverged from its upstream at
github.com/jposluns/ai-language, so a maintainer-invisible upstream update is surfaced.

The skill is Jeff Posluns's, vendored into this repo (see the skill's PROVENANCE.md). Upstream
advances without a heads-up, so a MONTHLY time-bounded follow-up in TODO.md runs this at /resume.
It compares each vendored file's git blob SHA (``git hash-object``) against the upstream blob SHA
(``gh api ... contents ... --jq .sha``); a mismatch is DRIFT, meaning re-fetch and re-vendor.

ADVISORY (not a gate): it REPORTS drift for the maintainer to action, and exits 0 on both in-sync
and drift so it never blocks; exit 2 only if the local skill dir or ``gh`` is unavailable (so a
network / auth problem is loud, not silently read as in-sync). GitHub has no egress issue here.

Usage:
    python3 tools/check-clean-language-upstream.py            # check drift, report
    python3 tools/check-clean-language-upstream.py --self-test

Exit codes: 0 checked (in-sync OR drift, both reported); 2 the local skill dir is missing or ``gh``
failed (an unverifiable state, surfaced loud rather than assumed in-sync).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".claude" / "skills" / "clean-language"
UPSTREAM = "repos/jposluns/ai-language/contents/clean-language"
# The vendored files, relative to the skill dir (also the upstream path suffix).
FILES = (
    "SKILL.md",
    "references/examples.md",
    "references/context-modes.md",
    "references/qa-checklist.md",
    "references/anti-patterns.md",
    "agents/openai.yaml",
)


def classify(local_shas: dict[str, str | None], upstream_shas: dict[str, str | None]) -> list[str]:
    """PURE: return the list of files that DRIFT (local != upstream, or either side missing).
    A missing file on either side is drift (it must be re-vendored / investigated), never silently
    treated as in-sync."""
    drift = []
    for f in local_shas:
        loc, up = local_shas.get(f), upstream_shas.get(f)
        if loc is None or up is None or loc != up:
            drift.append(f)
    return drift


def _local_sha(rel: str) -> str | None:
    p = SKILL_DIR / rel
    if not p.is_file():
        return None
    try:
        return subprocess.check_output(["git", "hash-object", str(p)], text=True).strip()
    except (subprocess.CalledProcessError, OSError):
        return None


def _upstream_sha(rel: str) -> str | None:
    try:
        out = subprocess.check_output(
            ["gh", "api", f"{UPSTREAM}/{rel}", "--jq", ".sha"], text=True).strip()
        return out or None
    except (subprocess.CalledProcessError, OSError):
        return None


def _self_test() -> int:
    checks = []
    # in-sync: identical shas -> no drift
    checks.append(("in-sync-no-drift", classify({"a": "x", "b": "y"}, {"a": "x", "b": "y"}) == []))
    # changed sha -> drift
    checks.append(("changed-sha-drift", classify({"a": "x"}, {"a": "z"}) == ["a"]))
    # missing upstream -> drift (not silently in-sync)
    checks.append(("missing-upstream-drift", classify({"a": "x"}, {"a": None}) == ["a"]))
    # missing local -> drift
    checks.append(("missing-local-drift", classify({"a": None}, {"a": "x"}) == ["a"]))
    # mixed
    checks.append(("mixed", classify({"a": "x", "b": "y"}, {"a": "x", "b": "z"}) == ["b"]))
    bad = [n for n, ok in checks if not ok]
    if bad:
        print(f"check-clean-language-upstream self-test: FAIL {bad}")
        return 1
    print(f"check-clean-language-upstream self-test: OK ({len(checks)} checks)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return _self_test()
    if not SKILL_DIR.is_dir():
        print(f"ERROR: vendored skill dir not found at {SKILL_DIR} (nothing to check).", file=sys.stderr)
        return 2
    local = {f: _local_sha(f) for f in FILES}
    upstream = {f: _upstream_sha(f) for f in FILES}
    if all(v is None for v in upstream.values()):
        print("ERROR: could not read ANY upstream blob SHA via `gh api` (auth / network / repo "
              "moved?). Cannot verify drift; not assuming in-sync.", file=sys.stderr)
        return 2
    drift = classify(local, upstream)
    if not drift:
        print(f"OK: all {len(FILES)} vendored clean-language file(s) are IN SYNC with upstream "
              f"jposluns/ai-language.")
        return 0
    print(f"DRIFT: {len(drift)} vendored clean-language file(s) differ from upstream "
          f"jposluns/ai-language; re-fetch and re-vendor them:")
    for f in drift:
        print(f"  {f}: local={ (local[f] or 'MISSING')[:8] } upstream={ (upstream[f] or 'MISSING')[:8] }")
    print("Re-vendor: `gh api repos/jposluns/ai-language/contents/clean-language/<file> --jq .content "
          "| base64 -d > .claude/skills/clean-language/<file>`, then commit + update PROVENANCE.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
