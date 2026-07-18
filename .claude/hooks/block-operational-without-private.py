#!/usr/bin/env python3
"""PreToolUse Edit/Write hook: fail loud when the maintainer orchestrator lacks _private.

Shipped 2026-07-18 (TODO section 1.19.8 layered assurance, maintainer-directed). The concern:
an AI "trying to be helpful" ignores grc_library_private being inaccessible, or skips it and
reconstructs its content from memory, instead of using it or failing loud. grc_library_private
holds the maintainer orchestrator's operational state (the CLAUDE.md delegation directive points
to its INDEX), so for the maintainer a missing _private is a broken setup to FIX (clone it),
never to silently work around.

This hook is the MECHANICAL core of the layered assurance (the others: detect-env's
private_availability decision + the /resume HALT, and the read-evidence discipline). It fires on
the operational-work tools (Edit, Write) and BLOCKS them (exit 2, reason on stderr) ONLY when
BOTH are confirmed: (a) the operator is the maintainer (origin remote is jposluns/grc_library),
and (b) grc_library_private is genuinely absent (no readable, non-empty sibling directory). Read
and Bash are deliberately NOT gated, so the session can still clone _private and investigate.

Design (fail-open on uncertainty, fail-loud on the real condition):
  - _private present  -> ALLOW (fast path; the common case).
  - _private absent + maintainer origin CONFIRMED -> BLOCK (loud clone/fix message).
  - _private absent + adopter/indeterminate origin -> ALLOW (an adopter legitimately has no
    _private; blocking would brick a legitimate adopter session).
  - any parse/read error, or origin cannot be positively confirmed as maintainer -> ALLOW.
    Blocking requires POSITIVE confirmation of BOTH conditions; the safe direction on any
    uncertainty is allow (a false block bricks the session; a false allow only misses the
    guard, which the detect-env HALT + read-evidence discipline still cover). A hook bug must
    never be worse than the mistake it prevents.

Exit protocol (Claude Code hooks): exit 0 allows; exit 2 blocks and feeds stderr to the model.
Like the sibling hooks, this does not fire in a child session whose CLAUDE_PROJECT_DIR is unset
(documented harness limitation); the detect-env HALT + the discipline are the primary controls.

Self-test: python3 .claude/hooks/block-operational-without-private.py --self-test
"""

import json
import os
import re
import sys
from pathlib import Path

MAINTAINER_ORIGIN = "jposluns/grc_library"
# Match the origin remote url in .git/config, tolerating https and ssh forms and an
# optional .git suffix. We confirm MAINTAINER only on a positive match; anything else
# (fork, missing, unparseable) is treated as non-maintainer -> allow.
ORIGIN_BLOCK_RE = re.compile(r'\[remote "origin"\][^\[]*', re.DOTALL)
URL_RE = re.compile(r"url\s*=\s*(\S+)")


def _origin_is_maintainer(project_dir: str) -> bool:
    """True only if the origin remote positively points at the maintainer repo."""
    cfg = Path(project_dir) / ".git" / "config"
    try:
        text = cfg.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    block = ORIGIN_BLOCK_RE.search(text)
    if not block:
        return False
    m = URL_RE.search(block.group(0))
    if not m:
        return False
    url = m.group(1)
    # normalize: strip trailing .git
    norm = url[:-4] if url.endswith(".git") else url
    # Match ONLY on a boundary (exact, or preceded by "/" or ":") so a pathological
    # fork owner literally ending in "jposluns" (e.g. evil-jposluns/grc_library) is NOT
    # misread as the maintainer and wrongly blocked. A bare endswith would over-match.
    return (
        norm == MAINTAINER_ORIGIN
        or f"/{MAINTAINER_ORIGIN}" in norm
        or f":{MAINTAINER_ORIGIN}" in norm
    )


def _private_present(project_dir: str) -> bool:
    """True if a readable, non-empty grc_library_private sibling exists."""
    sib = Path(project_dir).parent / "grc_library_private"
    try:
        return sib.is_dir() and any(sib.iterdir())
    except OSError:
        # cannot stat -> treat as indeterminate; caller's default is allow, but we
        # only reach the maintainer-origin check when this returns False, so return
        # True here to fail-open (do not block on a stat error).
        return True


def decide(project_dir: str) -> tuple[bool, str]:
    """Return (block, reason). Block only on confirmed maintainer + confirmed _private-absent."""
    if _private_present(project_dir):
        return False, ""
    if not _origin_is_maintainer(project_dir):
        return False, ""  # adopter / indeterminate: allow (fail-open)
    return True, (
        "Edit/Write BLOCKED: this is the maintainer orchestrator (origin is "
        f"{MAINTAINER_ORIGIN}) but grc_library_private is NOT accessible. _private holds "
        "the operational state the CLAUDE.md delegation directive points to; it is a "
        "REQUIRED dependency, not optional. Do NOT proceed with operational edits and do "
        "NOT reconstruct _private content from memory. FIX FIRST: clone it "
        "(git clone https://github.com/jposluns/grc_library_private.git ../grc_library_private) "
        "or grant sibling access (--add-dir ../grc_library_private), then continue. Read and "
        "Bash are still available so you can do exactly that. (If you are genuinely an adopter, "
        "this hook would not have fired; if origin was misdetected, resolve it and retry.)"
    )


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # fail-open
    workspace = payload.get("workspace") or {}
    project_dir = (
        workspace.get("project_dir")
        or os.environ.get("CLAUDE_PROJECT_DIR")
        or "/home/jposluns/grc_library"
    )
    try:
        block, reason = decide(project_dir)
    except Exception:
        return 0  # fail-open on any unexpected error
    if block:
        print(reason, file=sys.stderr)
        return 2
    return 0


def _self_test() -> int:
    import tempfile
    import subprocess
    import unittest

    def make_repo(tmp, origin_url, with_private):
        repo = Path(tmp) / "grc_library"
        repo.mkdir()
        gitdir = repo / ".git"
        gitdir.mkdir()
        (gitdir / "config").write_text(
            f'[remote "origin"]\n\turl = {origin_url}\n\tfetch = +refs/heads/*\n'
        )
        if with_private:
            priv = Path(tmp) / "grc_library_private"
            priv.mkdir()
            (priv / "INDEX.md").write_text("x")
        return str(repo)

    class T(unittest.TestCase):
        def test_maintainer_no_private_blocks(self):
            with tempfile.TemporaryDirectory() as tmp:
                rd = make_repo(tmp, "https://github.com/jposluns/grc_library.git", False)
                self.assertTrue(decide(rd)[0])

        def test_maintainer_ssh_no_private_blocks(self):
            with tempfile.TemporaryDirectory() as tmp:
                rd = make_repo(tmp, "git@github.com:jposluns/grc_library.git", False)
                self.assertTrue(decide(rd)[0])

        def test_maintainer_with_private_allows(self):
            with tempfile.TemporaryDirectory() as tmp:
                rd = make_repo(tmp, "https://github.com/jposluns/grc_library.git", True)
                self.assertFalse(decide(rd)[0])

        def test_adopter_no_private_allows(self):
            with tempfile.TemporaryDirectory() as tmp:
                rd = make_repo(tmp, "https://github.com/somefork/grc_library.git", False)
                self.assertFalse(decide(rd)[0])

        def test_lookalike_owner_no_private_allows(self):
            # a fork owner ending in "jposluns" must NOT be misread as the maintainer
            with tempfile.TemporaryDirectory() as tmp:
                rd = make_repo(tmp, "https://github.com/evil-jposluns/grc_library.git", False)
                self.assertFalse(decide(rd)[0])

        def test_no_git_config_allows(self):
            with tempfile.TemporaryDirectory() as tmp:
                repo = Path(tmp) / "grc_library"
                repo.mkdir()
                self.assertFalse(decide(str(repo))[0])

        def test_empty_private_dir_blocks_for_maintainer(self):
            with tempfile.TemporaryDirectory() as tmp:
                rd = make_repo(tmp, "https://github.com/jposluns/grc_library.git", False)
                (Path(tmp) / "grc_library_private").mkdir()  # empty
                self.assertTrue(decide(rd)[0])

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
