"""Put the AIQT pack's ``tools/`` on ``sys.path`` so a corpus tool can
``from aiqt_corpus import ...`` for the generic file/text/date/git/metadata
helpers. This is the SINGLE shim for the Corpus-Management Phase-2 re-point
(guardrails-confirmed mechanism, 2026-09-05): the pack is vendored and
digest-verified, not pip-installed, so the tools it publishes are reached by
adding its ``tools/`` directory to the path ONCE, here, rather than by 80-odd
per-tool path inserts.

Only the corpus tools that import the generic ``aiqt_corpus`` helpers import
this module; a tool that needs only grc-local config/store helpers keeps
importing ``lint_common`` and does not touch this shim.

Discovery order (first hit wins), all keyed on the pack's ``.aiqt`` root marker
so no host path is hardcoded:

1. ``GRC_AIQT_PACK`` env var (explicit override; its ``tools/aiqt_corpus.py``
   must exist), for a non-default layout or a test harness.
2. A ``.aiqt`` marker walked UP from this file, for a pack vendored inside or
   above the consuming repo.
3. A sibling directory of the repo root carrying a ``.aiqt`` marker AND
   ``tools/aiqt_corpus.py`` -- grc's dogfood, where the standalone ``guardrails``
   pack sits beside ``grc_library``.

It fails LOUD (``ImportError`` naming the fix) when the pack cannot be found,
so a broken setup surfaces here rather than as a downstream
``No module named aiqt_corpus``. The discovery lives ONLY in this file: when
guardrails finalizes the pack-root discovery convention, this shim changes and
the re-pointed tools do not (their ``from aiqt_corpus import ...`` line is
stable, exactly the point of a single shim).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

__all__ = ["ensure_on_path", "find_pack_tools"]

_inserted_path: str | None = None


def _has_module(pack_root: Path) -> bool:
    return (pack_root / ".aiqt").exists() and (pack_root / "tools" / "aiqt_corpus.py").is_file()


def find_pack_tools() -> Path | None:
    """Return the AIQT pack's ``tools/`` directory, or ``None`` if not found."""
    # 1. explicit override
    env = os.environ.get("GRC_AIQT_PACK")
    if env:
        root = Path(env).expanduser()
        if _has_module(root):
            return root / "tools"

    here = Path(__file__).resolve()

    # 2. a .aiqt marker walked UP from this file (vendored/in-tree pack)
    for parent in here.parents:
        if _has_module(parent):
            return parent / "tools"

    # 3. a sibling of the repo root carrying the marker + the module
    #    (this file lives at <repo>/tools/aiqt_bootstrap.py, so parents[1] == repo root)
    repo_root = here.parents[1]
    parent_dir = repo_root.parent
    try:
        siblings = sorted(parent_dir.iterdir())
    except OSError:
        siblings = []
    for sib in siblings:
        try:
            if sib.is_dir() and _has_module(sib):
                return sib / "tools"
        except OSError:
            # an unreadable neighbour (a restricted account dir) is skipped, not fatal
            continue
    return None


def ensure_on_path() -> Path:
    """Idempotently insert the AIQT pack's ``tools/`` on ``sys.path``; return it.

    Raises ``ImportError`` (with the fix) if the pack cannot be located.
    """
    global _inserted_path
    tools = find_pack_tools()
    if tools is None:
        raise ImportError(
            "AIQT pack not found: looked for a `.aiqt` marker + tools/aiqt_corpus.py "
            "via GRC_AIQT_PACK, a walk-up from this file, and repo siblings. "
            "Set GRC_AIQT_PACK to the pack root (the dir containing `.aiqt`), or place "
            "the pack beside this repo."
        )
    p = str(tools)
    if p not in sys.path:
        sys.path.insert(0, p)
    _inserted_path = p
    return tools


# Module-level side effect: discovery runs on import, so a consumer's
# `import aiqt_bootstrap` is enough before `from aiqt_corpus import ...`.
ensure_on_path()
