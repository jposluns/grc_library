#!/usr/bin/env python3
"""Clean-Language skill upstream-drift check (P-1.13): report when the vendored
`.claude/skills/clean-language/` skill has diverged from its upstream at
github.com/jposluns/ai-language, so a maintainer-invisible upstream update is surfaced.

The skill is Jeff Posluns's, vendored into this repo (see the skill's PROVENANCE.md). Upstream
advances without a heads-up, so a MONTHLY time-bounded follow-up in TODO.md runs this at /resume.
It compares each vendored file's git blob SHA (``git hash-object``) against the upstream blob SHA
(``gh api ... contents ... --jq .sha``); a mismatch is DRIFT, meaning re-fetch and re-vendor.

The tracked set is EVERY vendored file, keyed by its LOCAL path with its correct UPSTREAM path
(they differ: the skill content lives under upstream ``clean-language/``, but ``LICENSE`` and
``NOTICE.md`` are upstream REPO-ROOT files, and the icon assets live under ``clean-language/assets/``).
The two binary icon assets and the legal files (LICENSE / NOTICE) are tracked too, so an upstream
attribution or licence change does not go silent (defence in depth, codex vpr1328 findings 2 and 3).

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
UPSTREAM_BASE = "repos/jposluns/ai-language/contents"
# Every vendored file: LOCAL path (relative to the skill dir) -> UPSTREAM contents path.
# The upstream paths differ by file: skill content is under ``clean-language/``, the icon assets
# under ``clean-language/assets/``, but LICENSE and NOTICE.md are upstream REPO-ROOT files.
FILES = {
    "SKILL.md": "clean-language/SKILL.md",
    "references/examples.md": "clean-language/references/examples.md",
    "references/context-modes.md": "clean-language/references/context-modes.md",
    "references/qa-checklist.md": "clean-language/references/qa-checklist.md",
    "references/anti-patterns.md": "clean-language/references/anti-patterns.md",
    "agents/openai.yaml": "clean-language/agents/openai.yaml",
    "assets/CL_icon.svg": "clean-language/assets/CL_icon.svg",
    "assets/CL_icon.png": "clean-language/assets/CL_icon.png",
    "LICENSE": "LICENSE",
    "NOTICE.md": "NOTICE.md",
}


def classify(local_shas: dict[str, str | None], upstream_shas: dict[str, str | None]) -> list[str]:
    """PURE: return the sorted list of files that DRIFT (local != upstream, or either side
    missing). A file missing on EITHER side is drift, whether it is present-with-value-None or
    ABSENT as a key: the union of both key sets is iterated so an upstream-only or local-only file
    is never silently treated as in-sync (codex vpr1328 finding 1: iterating only local keys missed
    a file present upstream but absent locally)."""
    drift = []
    for f in set(local_shas) | set(upstream_shas):
        loc, up = local_shas.get(f), upstream_shas.get(f)
        if loc is None or up is None or loc != up:
            drift.append(f)
    return sorted(drift)


def _local_sha(rel: str) -> str | None:
    p = SKILL_DIR / rel
    if not p.is_file():
        return None
    try:
        return subprocess.check_output(["git", "hash-object", str(p)], text=True).strip()
    except (subprocess.CalledProcessError, OSError):
        return None


def _upstream_sha(upstream_path: str) -> str | None:
    try:
        out = subprocess.check_output(
            ["gh", "api", f"{UPSTREAM_BASE}/{upstream_path}", "--jq", ".sha"], text=True).strip()
        return out or None
    except (subprocess.CalledProcessError, OSError):
        return None


def _self_test() -> int:
    checks = []
    # in-sync: identical shas -> no drift
    checks.append(("in-sync-no-drift", classify({"a": "x", "b": "y"}, {"a": "x", "b": "y"}) == []))
    # changed sha -> drift
    checks.append(("changed-sha-drift", classify({"a": "x"}, {"a": "z"}) == ["a"]))
    # missing upstream (present-None) -> drift (not silently in-sync)
    checks.append(("missing-upstream-none-drift", classify({"a": "x"}, {"a": None}) == ["a"]))
    # missing local (present-None) -> drift
    checks.append(("missing-local-none-drift", classify({"a": None}, {"a": "x"}) == ["a"]))
    # ABSENT KEY upstream-only (local key entirely missing) -> drift (finding 1)
    checks.append(("absent-local-key-drift", classify({}, {"a": "x"}) == ["a"]))
    # ABSENT KEY local-only (upstream key entirely missing) -> drift (finding 1)
    checks.append(("absent-upstream-key-drift", classify({"a": "x"}, {}) == ["a"]))
    # mixed, one changed one same -> only the changed one, sorted
    checks.append(("mixed", classify({"a": "x", "b": "y"}, {"a": "x", "b": "z"}) == ["b"]))
    # union with disjoint keys -> both drift, sorted
    checks.append(("disjoint-union", classify({"a": "x"}, {"b": "y"}) == ["a", "b"]))
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
    local = {rel: _local_sha(rel) for rel in FILES}
    upstream = {rel: _upstream_sha(FILES[rel]) for rel in FILES}
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
        print(f"  {f} (upstream {FILES[f]}): "
              f"local={ (local.get(f) or 'MISSING')[:8] } upstream={ (upstream.get(f) or 'MISSING')[:8] }")
    print("Re-vendor each: `gh api repos/jposluns/ai-language/contents/<upstream-path> --jq .content "
          "| base64 -d > .claude/skills/clean-language/<local-path>`, then commit + update PROVENANCE.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
