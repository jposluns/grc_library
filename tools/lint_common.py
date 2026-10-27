"""Shared helpers for the audit-programme linters in ``tools/``.

This module exposes functions that 11+ linters previously copied
verbatim: the repository root constant, the default-exempt-directory
set, the markdown-target eligibility check, the directory-walking
target iterator, the UTF-8-safe text reader, and the
fenced-code-block-aware line iterator.

The module is deliberately minimal. It does not encapsulate per-linter
exemption lists, per-linter regex patterns, or per-linter scan logic;
each linter retains its own rule set, and the helpers expose hooks for
linters to pass their own exempt-file / exempt-directory sets.

Stdlib-only Python 3.11. No third-party dependencies.

Scope notes:

- ``REPO_ROOT`` is computed from this file's location: the parent of
  ``tools/`` is the repository root. Linters that import this constant
  inherit the same value.
- ``DEFAULT_EXEMPT_DIRS`` mirrors the set 13+ linters already defined
  inline (``.git``, ``node_modules``, ``__pycache__``, ``.claude``,
  ``.working``), the top-level ``references`` operational-prose dir (added
  in #1249), plus the three in-repo sibling-repo placeholder
  directories (``.ref``, ``.scratch``, ``.private``; closing PR
  #994, whose stub-only invariant the sibling-repo stub-guard gate
  enforces). Linters that need further exempt directories beyond this
  shared default pass them via the ``exempt_dirs`` argument.
- ``resolve_sibling`` / ``sibling_placeholder_present`` locate a real
  sibling repository (``grc_library_ref`` / ``grc_library_scratch`` /
  ``grc_library_private``) by short name, returning ``None`` when it is
  absent. Sibling-reaching ADVISORY tools route their default lookup
  through these so a portable clone with no sibling degrades to an
  advisory no-op (exit 0) rather than an error (1.19.2 (closing PR #996)).
- ``iter_markdown_targets`` and ``is_markdown_target`` deliberately
  accept ``Iterable[str]`` for ``exempt_files`` so callers can pass a
  ``set``, ``frozenset``, or ``list`` interchangeably.
- ``iter_non_code_lines`` yields ``(lineno, line)`` skipping any line
  inside a fenced code block (lines bounded by fence lines: ``` ``` ```
  or ``~~~`` after at most three spaces of indent). The fence-start and
  fence-end lines are also skipped.
- ``print_degraded`` prints the ``DEGRADED:`` line of a gate that skips a
  check because the private store is absent, plus a GitHub Actions warning
  annotation when ``GITHUB_ACTIONS`` is ``true`` (3b635).
"""

from __future__ import annotations

import datetime
import errno
import json
import os
import re
import stat as _stat
import subprocess
import sys
from collections.abc import Iterable, Iterator
from pathlib import Path, PureWindowsPath
from typing import NamedTuple

# Repository root: the parent of ``tools/``.
REPO_ROOT: Path = Path(__file__).resolve().parent.parent

# Default directory parts that every linter skips when walking the
# repository. Frozen so callers cannot mutate the shared default.
# ``.claude`` holds this project's Claude Code AI-assistant config
# (project CLAUDE.md and draggable rule files copied from the
# guardrails/ pack); like that pack directory, its
# contents are AI-context artefacts, not governed corpus documents,
# so the corpus linters skip it.
# ``.working`` held maintainer working state (per-run records from
# /validate, /fitness, and other maintainer-invoked activities): frozen-state
# archives the corpus linters skip. It has moved out of this public repository
# into the operational store, with the private sibling's ``.working/`` retained
# as a transitional fallback; the exempt-dir
# entry is retained so an in-repo ``.working`` (a maintainer mid-migration state,
# or an adopter's own) is still skipped if present.
DEFAULT_EXEMPT_DIRS: frozenset[str] = frozenset(
    {
        ".git",
        "node_modules",
        "__pycache__",
        ".claude",
        ".working",
        # references/ holds operational REFERENCE prose relocated from the
        # gate-exempt .claude/CLAUDE.md (3.139.1 (closing PR #1249), roadmap C phase 1): the
        # per-turn-loaded governance detail read at the PR-close-out boundary.
        # It is operational machinery, not corpus content, so it is exempt like
        # .claude/ (the prose was exempt in its prior home; this preserves that).
        # NOTE (dual-family verify, PR #1249): "references" is a GENERIC dir name
        # matched by bare component (is_target checks `part in exempt_dirs`), so a
        # future nested `references/` under a SCANNED tree would be silently exempt.
        # No such collision today (only top-level ./references; skill references/
        # subdirs live under already-exempt .claude/). Top-level-anchoring is a
        # queued morning-review item; a reviewer adding a nested references/ must
        # weigh this.
        "references",
        # In-repo sibling-repo placeholder slots (1.22.2 (closing PR #1047)): OPTIONAL
        # stand-ins for the grc_library_ref / grc_library_scratch / grc_library_private
        # siblings. They are NOT shipped by default (the maintainer runs the real
        # siblings; an adopter opts into an in-repo stub via /adopt), so these are
        # normally absent. Kept exempt so that IF an adopter materializes one (as a
        # README-only stub, which the stub-guard gate lint-sibling-placeholders.py
        # keeps payload-free, or as a functional checkout), the content gates skip it.
        ".ref",
        ".scratch",
        ".private",
    }
)

# Root-relative source trees excluded from corpus content selection.
# Safety callers can retain these trees with exclude_default_roots=False.
DEFAULT_EXEMPT_ROOTS: frozenset[str] = frozenset({".corpus-management"})


def is_default_exempt_root(
    path: str | Path, *, repo_root: Path | None = None,
) -> bool:
    """Match descendants of a default exempt root, including missing files.

    Relative paths are repository-relative. Outside paths and nested or
    similarly named directories do not acquire this exemption. None uses
    the current REPO_ROOT; it does not disable the policy.
    """
    root = (REPO_ROOT if repo_root is None else Path(repo_root)).resolve()
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        rel = candidate.resolve().relative_to(root)
    except (ValueError, OSError):
        return False
    return len(rel.parts) > 1 and rel.parts[0] in DEFAULT_EXEMPT_ROOTS


# Root-relative test scratch tree (3b653): ``tests/tmp`` holds the regression
# suite's transient per-run fixtures (gitignored; created and removed while a
# sweep may be running), never corpus. The skip is OPT-IN (``skip_test_scratch``
# on :func:`iter_targets`), set only by gates 48, 61, 73 and 79, which crashed on
# a fixture the suite deleted mid-walk; every other caller, including the secrets
# and PII gates that keep source-tree coverage, still walks ``tests/tmp``. With
# the opt-in, a directory walk from outside it prunes the tree, so it is never
# entered (:func:`_walk_files_pruned`). Root-anchored like
# the default exempt roots (a nested ``tests/tmp`` elsewhere is still walked), and
# an explicit argument naming a file or directory inside it is still scanned, so
# the suite's own fixtures stay reachable. A symlink outside the tree whose target
# is inside it is still listed; those gates refuse it by name if it is gone when
# read (:func:`scan_listed`).
TEST_SCRATCH_ROOT: tuple[str, ...] = ("tests", "tmp")


def _test_scratch_dir(repo_root: Path | None = None) -> Path:
    """Resolved ``tests/tmp`` under ``repo_root`` (default :data:`REPO_ROOT`)."""
    return (REPO_ROOT if repo_root is None else Path(repo_root)).resolve().joinpath(*TEST_SCRATCH_ROOT)


def _walk_files_pruned(top: Path, prune: Path) -> Iterator[Path]:
    """Every non-directory entry under ``top``, never entering ``prune`` (3b653).

    The same non-directory entries as ``top.rglob("*")`` (directory symlinks are
    not followed), except that ``prune`` is dropped from the walk before it is
    read: nothing under it is listed, and a scratch directory removed mid-walk is
    never opened. A directory that vanishes elsewhere is skipped, as
    :func:`os.walk` ignores ``scandir`` errors by default.
    """
    for dirpath, dirnames, filenames in os.walk(top):
        base = Path(dirpath)
        dirnames[:] = [d for d in dirnames if base / d != prune]
        for name in filenames:
            yield base / name


def scan_listed(scan, path: Path, vanished: list[Path]) -> list:
    """Run ``scan()`` for the listed file ``path``; record ``path`` if it vanished.

    A file the discovery walk listed can be removed before the gate reads it (a
    concurrent run deleting its scratch). That is neither a finding nor a pass:
    the file is appended to ``vanished`` and ``[]`` returned, so the caller ends
    with :func:`refuse_vanished` (fail closed, naming the file) instead of a
    FileNotFoundError traceback or a silent skip. Any other FileNotFoundError
    (a different file) still raises.
    """
    try:
        return scan()
    except FileNotFoundError as exc:
        if exc.filename is None or Path(exc.filename) != path:
            raise
        vanished.append(path)
        return []


def refuse_vanished(vanished: Iterable[Path], *, repo_root: Path | None = None) -> int:
    """Name each listed file that was gone when read, on stderr; return exit code 2.

    The scan did not read these files, so the gate cannot pass; it refuses as an
    environment error (2), distinct from findings (1). Rerun when the tree is quiet.
    """
    root = (REPO_ROOT if repo_root is None else Path(repo_root)).resolve()
    for path in vanished:
        try:
            shown = path.resolve().relative_to(root).as_posix()
        except (ValueError, OSError):
            shown = path.as_posix()
        print(f"ERROR: {shown}: listed for scanning but gone when read (removed "
              f"mid-scan); the scan is incomplete, refusing to pass. Rerun when "
              f"nothing is creating or deleting files in the tree.", file=sys.stderr)
    return 2


# The executive narrative layer (P-1.25, root ``executive/``) is OUTSIDE the
# corpus document model but INSIDE the repository safety gates. Corpus-MODEL
# gates that walk the repo root exclude it via the root-anchored
# ``is_narrative_root`` helper (NOT by unioning this component set, which would
# over-match a nested directory merely named ``executive``); safety and
# reference-integrity gates deliberately do NOT exclude it. Never fold this into
# ``DEFAULT_EXEMPT_DIRS`` itself: that would silently remove the narrative
# tree from the secrets/PII/link-safety gates too. The authoritative per-gate
# classification is ``tools/gate-scope-manifest.json`` (regression-checked).
NARRATIVE_DIRS: frozenset[str] = frozenset({"executive"})


def is_narrative_root(path: "str | Path") -> bool:
    """Root-anchored narrative-layer test: True iff ``path`` lies under the
    repository-root ``executive/`` tree. Unlike a bare path-component check, a
    NESTED directory merely named ``executive`` (e.g. ``governance/executive/``)
    is NOT matched, so corpus-model gates keep scanning it. This is the sound
    mechanism for the P-1.25 scan-root split; ``NARRATIVE_DIRS`` names the root
    for reference but must never be unioned into a component-wise exemption."""
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate
    try:
        rel = candidate.resolve().relative_to(REPO_ROOT.resolve())
    except (ValueError, OSError):
        return False
    return len(rel.parts) >= 1 and rel.parts[0] == "executive"


# --- Historical-surface classification (hoisted from residual-scan.py, #1250) ---
# Shared by residual-scan.py and the D9 retired-section-orphan gate so the two
# cannot drift on what counts as a LIVE surface (defence in depth). A hit is
# LEDGER (append-only history) or FROZEN-RECORD (dated per-run archive) or LIVE;
# only LIVE hits are actionable, the others are legitimate historical narration.

# Dated per-run archive: any .working/<activity>/<YYYY-...> file, any year.
FROZEN_RECORD_RE = re.compile(r"^\.working/[^/]+/\d{4}-")

# Per-activity append-only history tables.
LEDGER_RE = re.compile(r"^\.working/[^/]+/history\.md$")

# Top-level append-only ledgers. Logical `.working/` names also
# classify the operational store records resolved outside this checkout.
LEDGER_PATHS = (
    "CHANGELOG.md",
    ".working/changelog-details/CHANGELOG-detailed.md",
    ".working/DONE.md",
    ".working/improvement-log.md",
)


def classify(rel: str) -> str:
    """Classify a repo-relative path as LEDGER / FROZEN-RECORD / LIVE."""
    if LEDGER_RE.match(rel) or rel in LEDGER_PATHS:
        return "LEDGER"
    if FROZEN_RECORD_RE.match(rel):
        return "FROZEN-RECORD"
    return "LIVE"


# Sibling-repo short name -> the real sibling checkout's directory name.
# The three siblings of the public ``grc_library`` repo. See PR #996
# (operational-state privatization + adopter-clone portability).
_SIBLING_REPO_DIRS: dict[str, str] = {
    "ref": "grc_library_ref",
    # RETIRED 2026-09-23 (maintainer-directed); its last data reader, audit-brief-freshness.py, was
    # retired 2026-09-24. Kept because audit-cross-repo-references.py classifies grc_library_scratch
    # pointers through resolve_sibling and sibling_placeholder_present, which raise on an unknown
    # name; deleting it breaks that audit on every retired-sibling pointer. Never clone/sync it.
    "scratch": "grc_library_scratch",
    "private": "grc_library_private",
}


class InaccessiblePath(OSError):
    """A path that is, or may be, present but cannot be examined: a parent without search
    permission (EACCES), a symlink loop (ELOOP), a non-directory parent (ENOTDIR), an entry that
    cannot be followed (a dangling link, a link into a locked directory), or an entry of the wrong
    kind. The strict lookups raise it rather than read such a path as absent (3b74)."""


def strict_kind(path) -> "str | None":
    """``"dir"``, ``"file"`` or ``"other"`` for ``path``; ``None`` only when it is genuinely ABSENT.

    ABSENT means ``lstat`` reports ENOENT (no entry for the path or for a parent). Any other failure
    raises :class:`InaccessiblePath`. The probe calls ``os.lstat``/``os.stat`` directly, so the
    verdict is the same on Python 3.11, whose pathlib ``exists()``/``is_file()``/``is_dir()`` raise
    PermissionError on EACCES, and on 3.12+, whose versions return False and so read an unreadable
    path as absent. It does not test read permission on a directory's contents.
    """
    p = os.fspath(path)
    try:
        os.lstat(p)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise InaccessiblePath(exc.errno, exc.strerror, p) from exc
    except ValueError as exc:  # an embedded NUL byte
        raise InaccessiblePath(errno.EINVAL, str(exc), p) from exc
    try:
        st = os.stat(p)
    except OSError as exc:
        # lstat found an entry that stat cannot follow: present but unusable, never absent.
        raise InaccessiblePath(exc.errno, exc.strerror, p) from exc
    if _stat.S_ISDIR(st.st_mode):
        return "dir"
    return "file" if _stat.S_ISREG(st.st_mode) else "other"


def _strict_is_dir(path) -> bool:
    """True for a directory, False when ABSENT; :class:`InaccessiblePath` for anything else."""
    kind = strict_kind(path)
    if kind is None:
        return False
    if kind != "dir":
        raise InaccessiblePath(errno.ENOTDIR, "present but not a directory", os.fspath(path))
    return True


def sibling_placeholder_present(name: str) -> bool:
    """Return True if an in-repo ``.<name>`` placeholder directory is present.

    ``name`` is a short sibling name (``ref`` / ``scratch`` / ``private``). The
    in-repo ``.<name>`` slot is NOT shipped by default (the maintainer runs the
    real siblings; an adopter may create an in-repo stub via ``/adopt``), so this
    is normally False. When True (an adopter opted into the in-repo stub model), a
    ``None`` from :func:`resolve_sibling` is the EXPECTED portable-clone state (an
    advisory tool no-ops), not a broken checkout. Raises ``ValueError`` on an
    unknown name.
    """
    if name not in _SIBLING_REPO_DIRS:
        raise ValueError(
            f"unknown sibling name {name!r}; expected one of "
            f"{sorted(_SIBLING_REPO_DIRS)}"
        )
    return (REPO_ROOT / f".{name}").is_dir()


def resolve_sibling(name: str, *, strict: bool = False) -> Path | None:
    """Locate a real sibling repository by short name, or return ``None``.

    ``name`` is ``ref`` / ``scratch`` / ``private``. Returns the REAL sibling
    checkout directory (``../grc_library_<full-name>`` relative to this repo's
    root) when it exists, else ``None``. The in-repo ``.<name>`` placeholder is
    deliberately NOT treated as a real sibling (it is a stub with no payload);
    use :func:`sibling_placeholder_present` to tell an expected portable-clone
    ``None`` (placeholder present) from a genuinely broken one.

    An advisory tool routes its DEFAULT sibling lookup through this helper and
    no-ops (exits 0) on ``None``; an EXPLICITLY named path (a ``--flag`` or
    environment variable) stays the caller's own concern, since an explicit
    wrong path is surfaced rather than papered over. Raises ``ValueError`` on
    an unknown name.

    ``strict=True`` (3b74) separates ABSENT from INACCESSIBLE: ``None`` only when no entry exists
    at the sibling path; an entry that cannot be examined, or is not a directory (a file, a dangling
    or looping symlink), raises :class:`InaccessiblePath` so the caller refuses (exit 2) instead of
    taking the absent-sibling no-op. The default is unchanged.
    """
    if name not in _SIBLING_REPO_DIRS:
        raise ValueError(
            f"unknown sibling name {name!r}; expected one of "
            f"{sorted(_SIBLING_REPO_DIRS)}"
        )
    candidate = REPO_ROOT.parent / _SIBLING_REPO_DIRS[name]
    if strict:
        return candidate if _strict_is_dir(candidate) else None
    return candidate if candidate.is_dir() else None


# The maintainer working-state subtree (`.working/`) moved out of the public repo
# into the operational store (`$GRC_STORE` or `<repo-parent>/private`; privacy:
# it carried account identifiers and operational records adopters never need).
# `resolve_working` is the single access point: it prefers that store, then the
# transitional private sibling's `.working/` tree, then the in-repo
# `.working/` (so migration states still work), and returns None when none is
# present (public CI / adopter clone -> the reader no-ops,
# exactly like an advisory sibling tool). See the migration plan in grc_library_private.
WORKING_SUBDIR = ".working"


# The fleet-standard operational store (adopt-with-overlay migration, 2026-08-23; decision (a)):
# `/opt/<project>/private` (wire-orch's `@STORE@`). Files live at the store ROOT (NO `.working`
# subdir), unlike the transitional `grc_library_private/.working/` location. It is PREFERRED over
# both the private sibling's `.working/` and the in-repo `.working/`, so a seeded store wins while an
# absent one falls through untouched (fallback-safe during the migration). Env `GRC_STORE` overrides
# the default `<repo-parent>/private`.
def _store_root(root: "Path") -> "Path":
    import os
    env = os.environ.get("GRC_STORE")
    if env:
        p = Path(env)
        # A relative GRC_STORE is resolved against the repo root (not the process CWD),
        # so the override's meaning does not shift with the caller's working directory.
        return p if p.is_absolute() else (root / p).resolve()
    return root.parent / "private"


def private_store_roots(root: "Path | None" = None) -> "list[Path]":
    """The recognized PRIVATE maintainer-store roots a private-required file may live under.

    Both the fleet-standard operational store (``/opt/<project>/private`` or ``$GRC_STORE``)
    and the private sibling (``grc_library_private``) are private (maintainer-owned, not a public
    or adopter checkout), so a private-required write guarded as "must be under a private store"
    accepts EITHER. Returns only the roots that actually exist, resolved. Order: store first, then
    the sibling. Used by the private-write accountability guards (e.g.
    audit-reference-breadth --update-state) so they accept the store as a valid private location
    (adopt-with-overlay migration, option B, 2026-08-23)."""
    r = (root or REPO_ROOT).resolve()
    roots = []
    store = _store_dir(r)
    if store is not None:
        roots.append(store.resolve())
    private = r.parent / _SIBLING_REPO_DIRS["private"]
    if private.is_dir():
        roots.append(private.resolve())
    return roots


def _store_dir(root: "Path", *, strict: bool = False) -> "Path | None":
    """The USABLE operational store for ``root``: :func:`_store_root` when it exists AND
    resolves OUTSIDE the public repo. A store that resolves INSIDE the repo (e.g. a relative
    ``GRC_STORE=private`` -> ``<repo>/private``) is REJECTED (returns None), preserving the
    invariant the old hardcoded ``grc_library_private`` guard held: private maintainer content
    is never written into the public checkout. Callers then fall back to the private sibling /
    in-repo ``.working/`` (reads) or refuse (private writes).

    ``strict=True`` (3b74) keeps both fallbacks (an ABSENT store and an in-repo store return None)
    but raises :class:`InaccessiblePath` for a store path that cannot be examined or is not a
    directory, which the default reads as absent. Both modes also catch the RuntimeError that
    Python 3.11's ``resolve()`` raises on a relative ``GRC_STORE`` symlink loop (it escaped as a
    traceback, since ``_store_root`` ran outside the ``try``)."""
    try:
        if strict:
            # Probe the configured store AS GIVEN (a relative GRC_STORE joined to the root, not yet
            # resolved) BEFORE _store_root resolves it, so a relative and an absolute spelling of
            # the same path get the same verdict and no "missing/.." or dangling link is normalized
            # away first. Only a store that is a real directory is resolved.
            env = os.environ.get("GRC_STORE")
            given = (Path(env) if Path(env).is_absolute() else root / env) if env else root.parent / "private"
            if not _strict_is_dir(given):
                return None
            store = _store_root(root)
            present = True
        else:
            store = _store_root(root)
            present = store.is_dir()
        if present and not store.resolve().is_relative_to(root.resolve()):
            return store
    except InaccessiblePath:
        raise
    except (OSError, RuntimeError) as exc:
        if strict:
            raise InaccessiblePath(getattr(exc, "errno", None) or errno.ELOOP,
                                   getattr(exc, "strerror", None) or str(exc),
                                   os.environ.get("GRC_STORE") or str(root.parent / "private")) from exc
        return None
    return None


def resolve_working(relpath: str, *, repo_root: Path | None = None, strict: bool = False) -> Path | None:
    """Locate a `.working/`-tree file, preferring the operational store (`$GRC_STORE` or `<repo-parent>/private`); the private sibling `grc_library_private/.working/` is a transitional fallback.

    `relpath` is POSIX-relative to the `.working/` root (e.g.
    ``"validate-pr/history.md"``). Resolution order:
      1. ``<store>/<relpath>`` where ``<store>`` is ``$GRC_STORE`` or ``<repo-parent>/private``
         (the fleet-standard operational store, adopt-with-overlay migration 2026-08-23),
         if the store dir is present AND the file exists there (NO ``.working`` subdir at the store);
      2. ``grc_library_private/.working/<relpath>`` (the transitional location), if present there;
      3. ``<repo>/.working/<relpath>`` (the pre-migration in-repo location), if present;
      4. ``None`` -- none is available (public CI / adopter clone). A reader that
         routes through this helper then no-ops, the graceful-degradation contract the
         `.working/`-reading gates adopt when their input leaves the public repo.

    ``repo_root`` overrides the repository root used to locate both the private sibling
    (``<repo_root>/../grc_library_private``) and the in-repo fallback. It defaults to
    :data:`REPO_ROOT`, so an existing caller (the 9 rewired gates) is unchanged. Consumers
    outside ``tools/`` (a hook that knows its ``CLAUDE_PROJECT_DIR``, a tool with its own
    root) pass their own root rather than relying on this module's constant.

    An EXPLICIT path passed to a tool (a ``--flag``) stays the caller's concern, as with
    :func:`resolve_sibling`; this helper governs only the DEFAULT `.working/` lookup.

    ``strict=True`` (3b74) raises :class:`InaccessiblePath` where the default falls through: a
    location that cannot be examined (an unsearchable parent, a symlink loop, a non-directory where
    a directory belongs). An ABSENT location still falls through, so a public or adopter clone still
    gets None. The default is unchanged.
    """
    root = (repo_root or REPO_ROOT).resolve()
    if strict:
        def present(p: Path) -> bool:
            return strict_kind(p) is not None
        is_dir = _strict_is_dir
    else:
        def present(p: Path) -> bool:
            return p.exists()

        def is_dir(p: Path) -> bool:
            return p.is_dir()
    store = _store_dir(root, strict=strict)
    if store is not None:
        cand = store / relpath
        if present(cand):
            return cand
    private = root.parent / _SIBLING_REPO_DIRS["private"]
    if is_dir(private):
        cand = private / WORKING_SUBDIR / relpath
        if present(cand):
            return cand
    local = root / WORKING_SUBDIR / relpath
    if present(local):
        return local
    return None


def resolve_working_dir(*, repo_root: Path | None = None, strict: bool = False) -> Path | None:
    """The `.working/` DIRECTORY (store preferred, then private sibling, then in-repo), or None.

    The directory analogue of :func:`resolve_working` for consumers that WALK the
    `.working/` tree (the residual scan, the cross-repo-reference audit) rather than
    open one named file. ``"."`` denotes the `.working/` root itself: pathlib drops a
    trailing ``.``, so the candidate is the directory and ``Path.exists()`` is true for it.
    ``strict`` is passed through to :func:`resolve_working`.
    """
    return resolve_working(".", repo_root=repo_root, strict=strict)


def resolve_working_for_write(relpath: str, *, repo_root: Path | None = None) -> Path:
    """A `.working/`-tree file path to WRITE, choosing a destination even when absent.

    Unlike :func:`resolve_working` (existence-based, ``None`` when neither location holds
    the file), a WRITER needs a destination regardless: the existing resolved file if one
    is present, else alongside the CURRENT `.working/` tree (:func:`resolve_working_dir`:
    the operational store when it exists, else the private sibling's ``.working/``, else the in-repo tree), else
    the private sibling's ``.working/<relpath>`` as the eventual home when no `.working/`
    tree exists anywhere (or the in-repo path when no private sibling repo is present). The
    caller creates the parent directory as needed. Never ``None``.

    RESIDUE (migration): a NEW file lands in the current `.working/` tree that
    resolve_working_dir selects (the operational store, else the private sibling, else
    in-repo), whereas an EXISTING file stays wherever it already lives (existing wins). So
    while a migration INTO the selected tree is incomplete, an existing file still in the
    old tree and a new file in the selected tree split across the two; they unify only once
    every existing file has also been copied into the selected tree. The deletion step's
    no-leftover-in-the-old-tree QA is the control. A partial copy splits.
    """
    root = (repo_root or REPO_ROOT).resolve()
    existing = resolve_working(relpath, repo_root=root)
    if existing is not None:
        return existing
    # Write alongside the CURRENT `.working/` tree so a NEW file lands where its
    # siblings already live (its relative links to them then resolve). During the
    # in-repo -> private migration that is the in-repo tree until the content move
    # completes, and the private tree after: exactly what resolve_working_dir tracks.
    current = resolve_working_dir(repo_root=root)
    if current is not None:
        return current / relpath
    # No `.working/` tree exists anywhere yet (fresh checkout): prefer the private
    # sibling as the eventual home when that repo is present, else the in-repo path.
    private = root.parent / _SIBLING_REPO_DIRS["private"]
    if private.is_dir():
        return private / WORKING_SUBDIR / relpath
    return root / WORKING_SUBDIR / relpath


def resolve_working_for_write_private(relpath: str, *, repo_root: Path | None = None) -> Path | None:
    """A private-REQUIRED `.working/`-tree write destination for MAINTAINER-only records.

    The writer-contract counterpart to :func:`resolve_working_for_write` for records that
    must NEVER be left in a public / adopter checkout (a worker-prompt log, the
    reference-audit state): the account-identifier and operational content the migration
    exists to keep private. Resolution:
      1. the already-resolved existing file (:func:`resolve_working`), if present; else
      2. the store (``$GRC_STORE`` / ``<repo-parent>/private``) when it exists, else the
         ``grc_library_private/.working/<relpath>`` sibling when present (both are private); else
      3. ``None`` -- so the caller REFUSES the write rather than recreating a public
         ``<repo>/.working/`` tree.

    This is the codex-I-4/I-5 fix: post-PR2b-3 (public ``.working/`` deleted), a maintainer
    tool in a clone WITHOUT ``_private`` would otherwise fall back to the public path and
    silently recreate the frozen public tree. Returning ``None`` makes the caller fail
    loud instead. Adopter/public tools that legitimately keep an in-repo ``.working/``
    use :func:`resolve_working_for_write` (never-None) rather than this helper.
    The caller creates the parent directory as needed.
    """
    root = (repo_root or REPO_ROOT).resolve()
    existing = resolve_working(relpath, repo_root=root)
    if existing is not None:
        return existing
    # Prefer the fleet-standard store (a private maintainer location) for a NEW
    # private-required record, so it unifies with the rest of the operational state
    # (adopt-with-overlay migration, option B). Fall back to the private sibling, else None.
    store = _store_dir(root)
    if store is not None:
        return store / relpath
    private = root.parent / _SIBLING_REPO_DIRS["private"]
    if private.is_dir():
        return private / WORKING_SUBDIR / relpath
    return None


def _workflow_escape(text: str, *, prop: bool = False) -> str:
    """Escape ``text`` for a GitHub Actions workflow command: message data, or a property value
    when ``prop`` (which also escapes ``:`` and ``,``)."""
    text = text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    return text.replace(":", "%3A").replace(",", "%2C") if prop else text


def print_degraded(gate: str, text: str) -> None:
    """Print the 3b635 store-degraded notice: ``DEGRADED: <text>`` on stdout, always.

    ``gate`` names the gate (``"gate 43"``, ``"delta gate D14"``). When the environment variable
    ``GITHUB_ACTIONS`` is ``"true"`` it also prints a warning annotation,
    ``::warning title=<gate> degraded::DEGRADED: <text>``, so the skip shows on the run summary
    rather than only inside a collapsed green step. Every gate that skips a check because the
    private store is absent calls this, so the line and the annotation have one implementation.
    """
    line = f"DEGRADED: {text}"
    print(line)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::warning title={_workflow_escape(gate + ' degraded', prop=True)}::"
              f"{_workflow_escape(line)}")


# Canonical list of audited-not-exempt top-level directories: the
# twelve domain directories plus ``.project-governance``. This is the
# single source of truth for the "explicit allow-list" content linters
# (the ones that enumerate scan roots rather than walking the
# repository root and subtracting ``DEFAULT_EXEMPT_DIRS``). Each such
# linter splats ``AUDITED_DOMAIN_DIRS`` into its scan-root list rather
# than hardcoding the directory run inline, so that adding a future
# top-level audited directory propagates to every content linter from
# one place. The directory-scan-scope parity gate
# (``tools/lint-scan-scope-parity.py``) enforces that no content
# linter hardcodes this run; the governance contract is in
# ``governance/specification-project-governance-separation.md`` section 7.4.
#
# ``docs`` is deliberately NOT in this set: it holds generated
# artefacts (``docs/portal.md``, ``docs/maturity-scorecard.md``) and is
# a per-linter extra that only the date/version-currency linters add,
# not a corpus domain. Each linter keeps its own meta-file entries
# (``README.md``, ``NOTICE.md``, the root specifications, etc.) and any
# extra directories alongside the splatted ``AUDITED_DOMAIN_DIRS``.
#
# The ordering matches the historical scan-root ordering across the
# linters (``.project-governance`` after ``governance``), so the
# refactor that introduces the splat is a no-op on the resulting file
# list.
AUDITED_DOMAIN_DIRS: tuple[str, ...] = (
    "ai",
    "architecture",
    "compliance",
    "crypto",
    "dev-security",
    "governance",
    ".project-governance",
    "operations",
    "privacy",
    "resilience",
    "risk",
    "security",
    "supply-chain",
)


# Default suffix set for markdown-only linters.
MARKDOWN_SUFFIXES: frozenset[str] = frozenset({".md"})


# --- Adopter overlay-exemption config (3.183, maintainer-decided 2026-09-12) ---
# An adopter forks the corpus and keeps organization-specific values (real names,
# internal system names, credentials) in a private-overlay directory the content gates
# (INCLUDING the PII/secrets/placeholder scanners) must not scan. Rather than source-edit
# DEFAULT_EXEMPT_DIRS (a change that conflicts on every upstream pull), the adopter names
# their overlay directory in the committed, non-source ``adopter-config.json`` at the repo
# root:  {"extra_exempt_dirs": ["my-org-overlay"]}
#
# Matching is TOP-LEVEL-ANCHORED (via ``is_adopter_exempt``, mirroring
# ``is_default_exempt_root``): an accepted name exempts ONLY ``<name>/`` directly under the
# repository root, NEVER a nested directory or file of that name elsewhere. That is what
# makes the HARD FLOOR sufficient: because a match can only be a top-level directory, the
# floor need only reject the SHIPPED top-level directories (derived mechanically below from
# the canonical constants, so it cannot silently drift as the tree grows). A rejected entry
# is SKIPPED with a loud stderr warning (fail-SAFE toward MORE scanning: the gate still
# scans it), never silently applied.
ADOPTER_CONFIG_FILENAME = "adopter-config.json"
# Shipped top-level directories an adopter exempt entry may NEVER name (exempting one would
# blind a gate over shipped content). Derived from the canonical constants so a NEW shipped
# top-level directory is covered automatically once it joins one of them; the completeness
# test (test_adopter_extra_exempt_dirs_floor) fails if a live top-level dir escapes this set.
PROTECTED_EXEMPT_NAMES: frozenset[str] = (
    frozenset(AUDITED_DOMAIN_DIRS)          # the 12 domains + .project-governance
    | DEFAULT_EXEMPT_DIRS                    # .git, node_modules, references, .ref, ...
    | NARRATIVE_DIRS                         # executive/
    | DEFAULT_EXEMPT_ROOTS                   # .corpus-management/
    | frozenset({"tools", "guardrails", "docs", "tests", ".github", ".web", "vendor"})
    | frozenset({"", ".", "/"})             # repo-root markers
)


def _load_adopter_extra_exempt_dirs(repo_root: "Path | None" = None) -> "frozenset[str]":
    """Validated adopter-declared extra exempt directory NAMES from ``adopter-config.json``.

    Absent or malformed config -> empty set (never an error: the shipped repo carries an
    empty list, and an adopter's typo must not break linting). A protected or malformed
    entry is SKIPPED with a stderr warning (fail-safe toward scanning). Names are matched
    TOP-LEVEL-ANCHORED by ``is_adopter_exempt``, so a bare single component is required.
    """
    root = REPO_ROOT if repo_root is None else Path(repo_root)
    cfg = root / ADOPTER_CONFIG_FILENAME
    if not cfg.exists():
        return frozenset()
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        print(f"WARNING ({ADOPTER_CONFIG_FILENAME}): unreadable/invalid JSON ({exc}); "
              "no adopter exempt directories applied.", file=sys.stderr)
        return frozenset()
    entries = data.get("extra_exempt_dirs", []) if isinstance(data, dict) else []
    if not isinstance(entries, list):
        print(f"WARNING ({ADOPTER_CONFIG_FILENAME}): 'extra_exempt_dirs' is not a list; "
              "no adopter exempt directories applied.", file=sys.stderr)
        return frozenset()
    accepted: set[str] = set()
    for raw in entries:
        if not isinstance(raw, str):
            print(f"WARNING ({ADOPTER_CONFIG_FILENAME}): non-string exempt entry {raw!r} "
                  "skipped.", file=sys.stderr)
            continue
        name = raw.strip()
        if (not name or "/" in name or "\\" in name or ".." in name
                or Path(name).is_absolute() or name in PROTECTED_EXEMPT_NAMES):
            print(f"WARNING ({ADOPTER_CONFIG_FILENAME}): exempt entry {raw!r} is a "
                  "protected or malformed name (a shipped corpus/tooling directory, an "
                  "absolute or multi-segment path, or empty); SKIPPED, so gates still "
                  "scan it. An adopter exempt entry must be your own top-level overlay "
                  "directory's bare name.", file=sys.stderr)
            continue
        accepted.add(name)
    return frozenset(accepted)


ADOPTER_EXTRA_EXEMPT_DIRS: frozenset[str] = _load_adopter_extra_exempt_dirs()


def is_adopter_exempt(path: "str | Path", *, repo_root: "Path | None" = None) -> bool:
    """True iff ``path`` lies directly under a repo-root adopter-exempt overlay directory.

    TOP-LEVEL-ANCHORED (like ``is_default_exempt_root``): only ``<name>/...`` where ``name``
    is a validated ``adopter-config.json`` entry AND ``name`` is the FIRST repo-relative
    path component matches. A nested directory or file merely named the same elsewhere is
    NOT matched, so an adopter entry can never blind a gate over shipped nested content.
    Applies unconditionally (independent of ``exclude_default_roots``), so even the
    safety gates (PII/secrets/placeholder) that retain the default exempt roots still skip
    the adopter's overlay, which is the point.
    """
    if not ADOPTER_EXTRA_EXEMPT_DIRS:
        return False
    root = (REPO_ROOT if repo_root is None else Path(repo_root)).resolve()
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        resolved = candidate.resolve()
        rel = resolved.relative_to(root)
    except (ValueError, OSError):
        return False
    if not (len(rel.parts) >= 1 and rel.parts[0] in ADOPTER_EXTRA_EXEMPT_DIRS):
        return False
    # The config semantic is an overlay DIRECTORY name, so the matched top-level component
    # must be a directory: this stops a top-level FILE whose name collides with an entry
    # (e.g. a shipped README.md) from being exempted, which would blind a gate over shipped
    # content. A path IS exempt when its first component names an adopter overlay directory.
    return (root / rel.parts[0]).is_dir()



def is_target(
    path: Path,
    *,
    suffixes: Iterable[str] = MARKDOWN_SUFFIXES,
    exempt_dirs: Iterable[str] = DEFAULT_EXEMPT_DIRS,
    exempt_files: Iterable[str] = (),
    repo_root: Path | None = None,
    exclude_default_roots: bool = True,
) -> bool:
    """Return True if ``path`` is a file the linter should scan.

    A path is a target when:
      - its suffix is in ``suffixes``;
      - none of its directory parts appears in ``exempt_dirs``;
      - it is outside the default exempt roots unless explicitly retained;
      - its filename (``path.name``) is not in ``exempt_files``.

    The caller passes its own suffix and exempt sets. The defaults are
    the common markdown-linter set: scan only ``.md``
    (``MARKDOWN_SUFFIXES``) and skip the ``DEFAULT_EXEMPT_DIRS`` set (``.git``,
    ``node_modules``, ``__pycache__``, ``.claude``, ``.working``, ``references``,
    ``.ref``, ``.scratch``, ``.private``), with no per-file exemptions.

    Implementation note: if the same exempt sets are checked many times
    (e.g., during a recursive walk), prefer to pass pre-constructed
    ``set`` / ``frozenset`` values so the conversion happens once
    rather than per call. ``iter_targets`` does this internally.
    """
    suffixes_set = suffixes if isinstance(suffixes, (set, frozenset)) else set(suffixes)
    exempt_dirs_set = exempt_dirs if isinstance(exempt_dirs, (set, frozenset)) else set(exempt_dirs)
    exempt_files_set = exempt_files if isinstance(exempt_files, (set, frozenset)) else set(exempt_files)
    if path.suffix not in suffixes_set:
        return False
    # Adopter overlay-exemption (3.183): TOP-LEVEL-ANCHORED, applies to EVERY is_target
    # caller including the safety gates, and independent of exclude_default_roots.
    if is_adopter_exempt(path, repo_root=repo_root):
        return False
    if any(part in exempt_dirs_set for part in path.parts):
        return False
    if exclude_default_roots and is_default_exempt_root(path, repo_root=repo_root):
        return False
    if path.name in exempt_files_set:
        return False
    return True


def is_markdown_target(
    path: Path,
    *,
    exempt_dirs: Iterable[str] = DEFAULT_EXEMPT_DIRS,
    exempt_files: Iterable[str] = (),
    repo_root: Path | None = None,
    exclude_default_roots: bool = True,
) -> bool:
    """Return True if ``path`` is a markdown file the linter should scan.

    Convenience wrapper around :func:`is_target` with the markdown suffix
    set. Root policy arguments are forwarded unchanged.
    """
    return is_target(
        path,
        suffixes=MARKDOWN_SUFFIXES,
        exempt_dirs=exempt_dirs,
        exempt_files=exempt_files,
        repo_root=repo_root,
        exclude_default_roots=exclude_default_roots,
    )


def iter_targets(
    paths: Iterable[str | Path],
    *,
    suffixes: Iterable[str] = MARKDOWN_SUFFIXES,
    exempt_dirs: Iterable[str] = DEFAULT_EXEMPT_DIRS,
    exempt_files: Iterable[str] = (),
    repo_root: Path | None = None,
    exclude_default_roots: bool = True,
    skip_test_scratch: bool = False,
) -> list[Path]:
    """Return deduplicated, ordered list of targets matching ``suffixes``.

    For each entry in ``paths``:
      - if it is a file and matches :func:`is_target`, include it;
      - if it is a directory, walk it recursively and include every
        file whose suffix is in ``suffixes`` and that passes
        :func:`is_target`; with ``skip_test_scratch`` (default off),
        prune the ``tests/tmp`` scratch tree (:data:`TEST_SCRATCH_ROOT`)
        from the walk, never entering it, unless the directory is inside it.

    Paths are resolved before deduplication. Order across the input is
    preserved. Relative input paths retain their current-working-directory
    interpretation; repo_root controls only the exemption boundary.
    """
    targets: list[Path] = []
    seen: set[Path] = set()
    suffixes_set = set(suffixes)
    exempt_dirs_set = set(exempt_dirs)
    exempt_files_set = set(exempt_files)

    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file():
            if is_target(
                p,
                suffixes=suffixes_set,
                exempt_dirs=exempt_dirs_set,
                exempt_files=exempt_files_set,
                repo_root=repo_root,
                exclude_default_roots=exclude_default_roots,
            ):
                if p not in seen:
                    targets.append(p)
                    seen.add(p)
        elif p.is_dir():
            # 3b653: opt-in skip of tests/tmp scratch unless the walk starts inside it;
            # the walk prunes it, so it never lists or enters that tree.
            scratch = _test_scratch_dir(repo_root) if skip_test_scratch else None
            if scratch is not None and not p.is_relative_to(scratch):
                walk: Iterable[Path] = _walk_files_pruned(p, scratch)
            else:
                walk = p.rglob("*")
            for f in walk:
                if not f.is_file():
                    continue
                if is_target(
                    f,
                    suffixes=suffixes_set,
                    exempt_dirs=exempt_dirs_set,
                    exempt_files=exempt_files_set,
                    repo_root=repo_root,
                    exclude_default_roots=exclude_default_roots,
                ):
                    if f not in seen:
                        targets.append(f)
                        seen.add(f)
    return targets


def iter_markdown_targets(
    paths: Iterable[str | Path],
    *,
    exempt_dirs: Iterable[str] = DEFAULT_EXEMPT_DIRS,
    exempt_files: Iterable[str] = (),
    repo_root: Path | None = None,
    exclude_default_roots: bool = True,
    skip_test_scratch: bool = False,
) -> list[Path]:
    """Return deduplicated, ordered list of markdown targets under ``paths``.

    Convenience wrapper around :func:`iter_targets` with the markdown
    suffix set. Retained for callers that scan only ``.md``.
    """
    return iter_targets(
        paths,
        suffixes=MARKDOWN_SUFFIXES,
        exempt_dirs=exempt_dirs,
        exempt_files=exempt_files,
        repo_root=repo_root,
        exclude_default_roots=exclude_default_roots,
        skip_test_scratch=skip_test_scratch,
    )


def check_explicit_paths(
    paths: Iterable[str],
    *,
    repo_root: Path | None = None,
    allow_outside: bool = False,
) -> list[str]:
    """Refusal messages for explicit linter arguments that would be mis-targeted or skipped.

    A content linter given explicit paths is a control only if it scans what the caller
    named. :func:`iter_scan_roots_markdown` resolves each entry against ``repo_root``
    (never the current directory) and silently drops an entry that does not exist, so
    three inputs used to pass without scanning the intended file (P-TODO 3b21):

    * a path that does not exist (a typo, or a file in another worktree), which scanned
      nothing and exited 0;
    * a RELATIVE path given while the current directory is not ``repo_root`` itself
      (outside the tree, or a subdirectory of it), which scanned the file at that path
      under ``repo_root``, not the file the caller was looking at;
    * an absolute path outside ``repo_root`` (``allow_outside=False``), which a linter
      whose vocabulary and repo-relative reporting belong to its own tree cannot scan
      soundly (``lint-language`` raised a ValueError traceback). Run the target tree's
      own ``tools/`` copy instead.

    Returns one message per refused argument; an empty list means none of the three
    shapes above applies, NOT that every argument will be scanned. Residue, stated: an
    existing path can still yield no scan through the linter's own documented
    exemptions or file-type filter (for example ``.corpus-management/``, a generated
    ``docs/`` artefact, or a non-``.md`` file), and a DIRECTORY argument's descendants
    are walked without a per-file containment check (no symlinks exist in the corpus).
    Use :func:`guard_explicit_paths` in a wrapper: it refuses and normalizes.
    """
    root = (repo_root if repo_root is not None else REPO_ROOT).resolve()
    cwd = Path.cwd().resolve()
    errors: list[str] = []
    for p in paths:
        if not str(p).strip():
            # 3b50b2a: an empty entry resolves to the tree root, so the linter would scan the
            # whole tree as an EXPLICIT path, bypassing its default exemptions.
            errors.append(f"{p!r}: an empty path argument is refused (it would resolve to the tree "
                          f"root and scan everything as an explicit path).")
            continue
        given = Path(p)
        if not given.is_absolute() and cwd != root:
            errors.append(
                f"{p}: relative path given from {cwd}, which is not this linter's tree root "
                f"{root}; it would resolve against {root}, not the current directory. Pass an "
                f"absolute path, run from {root}, or run the linter copy in the tree you are "
                f"working in."
            )
            continue
        target = root / given
        resolved = target.resolve()
        if not allow_outside and resolved != root and root not in resolved.parents:
            errors.append(
                f"{p}: outside this linter's tree ({root}); run the tools/ copy in the "
                f"tree that holds the file."
            )
            continue
        if not target.exists():
            errors.append(f"{p}: does not exist (resolved to {target}); nothing would be scanned.")
    return errors


def positional_args(argv: Iterable[str], known_flags: Iterable[str] = ("--self-test",)) -> list[str]:
    """Positional (path) arguments from a hand-parsed argv, refusing what would be dropped (3b50a).

    Several linters filtered argv with ``not a.startswith("-")``, which silently discarded an
    unknown option AND a dash-prefixed filename even after ``--``, so ``-- -missing.md`` scanned
    the defaults and exited 0. Every token after a ``--`` separator is positional; before it, a
    dash token must be one of ``known_flags`` or the call prints an error and raises
    ``SystemExit(2)``. Pass the result to the explicit-path guard.
    """
    argv = list(argv)
    tail: list[str] = []
    if "--" in argv:
        i = argv.index("--")
        argv, tail = argv[:i], argv[i + 1:]
    known = set(known_flags)
    repeated = sorted({a for a in argv if a in known and argv.count(a) > 1})
    if repeated:
        for a in repeated:
            print(f"ERROR: {a}: given more than once (use -- before a path that looks like an "
                  f"option).", file=sys.stderr)
        raise SystemExit(2)
    unknown = [a for a in argv if a.startswith("-") and a not in known]
    if unknown:
        for a in unknown:
            print(f"ERROR: {a}: unknown option (use -- before a path that begins with '-').",
                  file=sys.stderr)
        raise SystemExit(2)
    return [a for a in argv if not a.startswith("-")] + tail


def strict_flags(argv: Iterable[str], allowed: Iterable[str]) -> set[str]:
    """The flags of a tool that takes flags only, refusing anything else (3b50b2a).

    Several build and check tools tested ``"--check" in argv`` and ran their DEFAULT branch for
    any other input, so a mistyped ``--chck`` silently regenerated a committed artefact instead of
    checking it, and exited 0. Every token must be one of ``allowed``, given at most once; an
    unknown flag, a positional argument, a ``--`` separator, or a repeated flag prints an error and
    raises ``SystemExit(2)`` BEFORE the tool does anything. Returns the set of flags given.
    """
    argv = list(argv)
    known = set(allowed)
    errors: list[str] = []
    for a in argv:
        if a not in known:
            kind = "unknown option" if a.startswith("-") else "unexpected argument"
            errors.append(f"{a!r}: {kind} (allowed: {', '.join(sorted(known)) or 'none'}).")
    for a in sorted({a for a in argv if a in known and argv.count(a) > 1}):
        errors.append(f"{a}: given more than once.")
    if errors:
        for msg in errors:
            print(f"ERROR: {msg}", file=sys.stderr)
        raise SystemExit(2)
    return set(argv)


def flag_before_separator(argv: Iterable[str], flag: str) -> bool:
    """True when ``flag`` appears before any ``--`` separator (a token after ``--`` is a path).

    Call it only AFTER :func:`positional_args` has validated the same argv, so a flag test can
    never pre-empt the explicit-path refusal (3b50a round 2: ``-- --self-test missing.md`` ran the
    self-test and skipped the refusal)."""
    argv = list(argv)
    return flag in (argv[:argv.index("--")] if "--" in argv else argv)


def self_test_requested(argv: Iterable[str], paths: Iterable[str]) -> bool:
    """True when ``--self-test`` was given before any ``--``; refuses (exit 2) when paths were also
    given, since a self-test would ignore them and they would escape the explicit-path guard
    (3b50a round 3: ``--self-test -- missing.md`` exited 0)."""
    if not flag_before_separator(argv, "--self-test"):
        return False
    paths = list(paths)
    if paths:
        print(f"ERROR: --self-test takes no paths (given: {' '.join(paths)}); run the self-test "
              f"and the path scan separately.", file=sys.stderr)
        raise SystemExit(2)
    return True


def require_dir(path, flag: str) -> Path:
    """An explicit directory argument, resolved, or a refusal (stderr, SystemExit(2)) when it is not
    an existing directory (3b50b1: several --root overrides scanned nothing and exited 0).

    The path is checked AS GIVEN before it is resolved (3b74): the kernel follows each component in
    turn, so ``missing/../real`` and ``file/../real`` do not exist, but ``resolve()`` normalizes
    them lexically into ``real`` and a root nobody named would be scanned."""
    if not str(path).strip():
        # An empty value (--flag= or --flag "") would resolve to the current directory and pass.
        print(f"ERROR: {flag} needs a directory argument (an empty value is refused).", file=sys.stderr)
        raise SystemExit(2)
    try:
        given = Path(path)
        # Probe the path AS GIVEN (the kernel walks it component by component), then resolve.
        is_dir = given.is_dir()
        p = given.resolve()
    except (OSError, RuntimeError, ValueError) as exc:
        # Python 3.11's is_dir() raises on EACCES where newer versions return False, and its
        # resolve() raises RuntimeError on a symlink loop; ValueError is an embedded NUL byte.
        print(f"ERROR: {flag} {path}: unreadable or unresolvable ({exc}); nothing would be checked.",
              file=sys.stderr)
        raise SystemExit(2)
    if not is_dir:
        print(f"ERROR: {flag} {path}: not a directory as given (checked before any '..' is "
              f"normalized); nothing would be checked.", file=sys.stderr)
        raise SystemExit(2)
    return p


def require_git_worktree_at(root: Path) -> str | None:
    """A refusal message when ``root`` is not inside a git work tree, else None."""
    import subprocess

    try:
        inside = subprocess.run(["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
                                capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, OSError) as exc:
        return f"{root} is not inside a git work tree ({exc}); nothing can be checked."
    if inside != "true":
        return f"{root} is not inside a git work tree (git reports {inside!r}); nothing can be checked."
    return None


def guard_explicit_paths(
    paths: Iterable[str],
    *,
    repo_root: Path | None = None,
    allow_outside: bool = False,
) -> list[str]:
    """Refuse unsound explicit linter arguments (exit 2), else return them normalized.

    Prints each :func:`check_explicit_paths` message to stderr and raises
    ``SystemExit(2)`` when any argument is refused. Otherwise returns each argument
    resolved: repo-relative when it lies inside ``repo_root`` (so a spelling such as
    ``/abs/../abs/tree/file.md`` or ``tools/../README.md`` reaches the scanner in the
    form its repo-relative reporting expects), and absolute when it lies outside
    (only possible with ``allow_outside=True``). Call it only on user-given paths,
    never on a linter's default scan roots.
    """
    root = (repo_root if repo_root is not None else REPO_ROOT).resolve()
    paths = list(paths)
    refused = check_explicit_paths(paths, repo_root=root, allow_outside=allow_outside)
    if refused:
        for msg in refused:
            print(f"ERROR: {msg}", file=sys.stderr)
        raise SystemExit(2)
    out: list[str] = []
    for p in paths:
        resolved = (root / p).resolve()
        if resolved == root or root in resolved.parents:
            rel = resolved.relative_to(root)
            out.append(str(rel) if rel.parts else ".")
        else:
            out.append(str(resolved))
    return out



def guard_explicit_paths_cwd(
    paths: Iterable[str],
    *,
    repo_root: Path | None = None,
    allow_outside: bool = False,
    base: Path | None = None,
) -> list[str]:
    """Explicit-path guard for the :func:`iter_targets` family (3b48): refuse or normalize.

    :func:`iter_targets` resolves a relative entry against the CURRENT DIRECTORY (the
    conventional CLI meaning, kept here) and silently drops an entry that is neither a
    file nor a directory, so a missing explicit path used to scan nothing and exit 0.
    This guard resolves each user-given entry against ``base`` (default: the current
    directory; a linter whose documented contract is ``--root``-relative passes its live
    root) and refuses, with messages on stderr and ``SystemExit(2)``:

    * an entry that does not exist, since nothing would be scanned;
    * with ``allow_outside=False``, an entry that resolves outside ``repo_root``, since a
      linter whose checks read this tree's registers, glossary, inventory or git history,
      or whose reporting is repo-relative, cannot scan another tree soundly (run the
      ``tools/`` copy in the tree that holds the file).

    Returns the entries resolved to ABSOLUTE paths (``..`` and ``//`` spellings
    normalized), which the cwd-resolving walkers consume unchanged. Call it only on
    user-given paths, never on a linter's default or computed scan list. Residue, stated:
    an existing entry can still yield no scan through the linter's own exemptions or
    file-type filter, and a directory's descendants are walked without a per-file
    containment check (no symlinks exist in the corpus).
    """
    root = (repo_root if repo_root is not None else REPO_ROOT).resolve()
    anchor = (base if base is not None else Path.cwd()).resolve()
    errors: list[str] = []
    out: list[str] = []
    for p in paths:
        if not str(p).strip():
            # 3b50b2a: an empty entry resolves to the anchor directory and scans all of it.
            errors.append(f"{p!r}: an empty path argument is refused (it would resolve to "
                          f"{anchor} and scan everything there as an explicit path).")
            continue
        resolved = (anchor / Path(p)).resolve()
        if not allow_outside and resolved != root and root not in resolved.parents:
            errors.append(
                f"{p}: outside this linter's tree ({root}); run the tools/ copy in the "
                f"tree that holds the file."
            )
        elif not resolved.exists():
            errors.append(f"{p}: does not exist (resolved to {resolved}); nothing would be scanned.")
        else:
            out.append(str(resolved))
    if errors:
        for msg in errors:
            print(f"ERROR: {msg}", file=sys.stderr)
        raise SystemExit(2)
    return out

def iter_scan_roots_markdown(
    paths: Iterable[str],
    *,
    repo_root: Path | None = None,
) -> list[Path]:
    """Sorted, deduplicated ``.md`` files under explicit repo-relative scan roots.

    The allow-list walker shared by the explicit-scan-root content linters:
    they enumerate their scan roots (typically ``AUDITED_DOMAIN_DIRS`` plus
    root meta files) and subtract per-linter exempt files/prefixes at the
    call site, rather than walking the repository root and subtracting
    ``DEFAULT_EXEMPT_DIRS`` the way :func:`iter_markdown_targets` callers
    do. A dozen linters previously carried this loop verbatim.

    Each entry is taken relative to ``repo_root``: a ``.md`` FILE entry is
    included as-is; a DIRECTORY entry contributes every ``.md`` beneath it
    recursively. The default root exemption AND the adopter overlay-exemption (3.183) are
    subtracted. No other component exemptions are applied, so explicitly listed
    operational roots remain in scope.
    Otherwise, no exempt-directory subtraction happens here
    (an allow-list linter's scan roots ARE its scope) and paths are not
    resolved (matching the historical walkers, so reported paths and
    ordering are unchanged). ``repo_root`` defaults to :data:`REPO_ROOT`;
    a linter whose ``--root`` flag rebinds its module-level root passes
    its own current value explicitly.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    files: set[Path] = set()
    for p in paths:
        path = root / p
        if path.is_file() and path.suffix == ".md":
            files.add(path)
        elif path.is_dir():
            files.update(path.rglob("*.md"))
    return sorted(
        f for f in files
        if not is_default_exempt_root(f, repo_root=root)
        and not is_adopter_exempt(f, repo_root=root)  # 3.183: honor the adopter overlay here too
    )


def read_text_safe(path: Path) -> str | None:
    """Read ``path`` as UTF-8 text; return ``None`` on a decode error.

    Linters that scan a heterogeneous file tree should skip files that
    are not valid UTF-8 (binary files mis-named with ``.md``, lock
    files, etc.) rather than aborting the entire run. The contract is:
    successful return is a string; ``None`` signals "skip this file".

    Filesystem errors (FileNotFoundError, PermissionError) are not
    caught: those represent a real environmental problem the caller
    should surface.
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


class MetadataBlock:
    """Parsed document-metadata fields from a file's head window.

    Attributes:
        fields: field name to value, with a single trailing backslash
            (the metadata hard-line-break marker) stripped from the
            value and surrounding whitespace trimmed.
        raw_lines: field name to ``(lineno, raw line)`` for callers
            that need to point a finding at the exact source line.

    A field that appears more than once inside the window keeps its
    FIRST occurrence (matching the first-match semantics of the
    per-linter parsers this helper replaces).
    """

    __slots__ = ("fields", "raw_lines")

    def __init__(self) -> None:
        self.fields: dict[str, str] = {}
        self.raw_lines: dict[str, tuple[int, str]] = {}


# The generic metadata field shape shared by every corpus document:
# ``**Field:** value`` with an optional trailing backslash. This is the
# same pattern lint-metadata.py and build-taxonomy.py use; centralized
# here so parsers stop drifting apart (guardrail review GR-3).
METADATA_FIELD_RE = re.compile(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$")

# How many leading lines of a document constitute the metadata head
# window. Matches the long-standing window in the version-bump and
# co-bump gates; a ``**Field:**``-shaped line deeper in the body (for
# example a documented placeholder in a how-to section) is body prose,
# not metadata.
METADATA_HEAD_LINES = 30


def parse_metadata_block(text: str, *, head_lines: int = METADATA_HEAD_LINES) -> MetadataBlock:
    """Parse ``**Field:** value`` metadata lines from a file's head window.

    Scans the first ``head_lines`` lines of ``text`` for the corpus
    metadata-field shape and returns a :class:`MetadataBlock`. Values
    have the optional trailing backslash (hard-line-break marker)
    stripped, so ``**Date:** 2026-07-01\\`` yields ``"2026-07-01"``.

    The parser is deliberately TOLERANT at this layer: it captures
    whatever value text follows the field marker (including trailing
    annotations such as ``**Date:** 2026-07-01 (draft)``). Per-field
    validity is the CALLER's judgement, so a gate can fail loud on a
    present-but-malformed value instead of silently skipping the file
    (the gate-31 silent fail-open this helper was introduced to close);
    use a validator such as :func:`parse_iso_date` on the captured
    value and treat ``None``-on-present-field as a finding.
    """
    block = MetadataBlock()
    for lineno, line in enumerate(text.splitlines()[:head_lines], start=1):
        match = METADATA_FIELD_RE.match(line)
        if not match:
            continue
        field = match.group(1)
        if field in block.fields:
            continue
        value = match.group(2)
        if value.endswith("\\"):
            value = value[:-1].rstrip()
        block.fields[field] = value
        block.raw_lines[field] = (lineno, line)
    return block


def parse_iso_date(value: str) -> datetime.date | None:
    """Return ``value`` as a date if it is EXACTLY ``YYYY-MM-DD``, else ``None``.

    The whole captured value must be the ISO date: a trailing
    annotation (``2026-07-01 (draft)``) returns ``None`` so the caller
    can distinguish a malformed-but-present field (a finding, under
    fail-loud semantics) from an absent one (a legitimate skip).
    """
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


def head_version(text: str | None, *, head_lines: int = METADATA_HEAD_LINES) -> str | None:
    """Return the head-window ``Version`` or ``Library Version`` value, or ``None``.

    The Version-window trio's shared extraction (GR-3 wave 2: gate 40
    plus the D2 and D4 delta checks retired their identical private
    regex for this helper). Reads via :func:`parse_metadata_block`, so
    the corpus in-scope rule the trio shares is centralized here:

    - The ``Version`` field wins, then ``Library Version`` (the README's
      CalVer line); ``README Version`` is a DISTINCT field and never
      matches, exactly as the retired private regex behaved.
    - An EMPTY value is treated as absent (``None``), preserving the
      trio's scope rule that only a non-empty version value brings a
      file into scope.
    - Line-initial fields only: the retired regex tolerated leading
      whitespace before ``**Version:**``; this helper narrows to the
      canonical line-initial shape (the documented wave-2 narrowing;
      no corpus file carries an indented metadata field).
    - Three further edge-case divergences from the retired regex, each
      confirmed corpus-neutral at migration time (zero live instances):
      a no-separator value (``**Version:**1.0``) now parses (the old
      regex required whitespace before the value); precedence between
      ``Version`` and ``Library Version`` is by field name rather than
      by position in the window; and an empty first ``Version`` line no
      longer falls through to a later non-empty ``Version`` line in the
      same window.
    """
    if text is None:
        return None
    fields = parse_metadata_block(text, head_lines=head_lines).fields
    value = fields.get("Version") or fields.get("Library Version")
    return value or None


def add_months(d: datetime.date, months: int) -> datetime.date:
    """Return ``d`` advanced by ``months`` calendar months.

    Handles month-end roll-forward: 31 January + 1 month yields 28/29
    February. Stdlib-only; avoids a dateutil dependency. Hoisted from the
    two freshness linters (citation-verification and tooling-provenance),
    which carried identical copies of this calendar-aware arithmetic
    (Phase 23.65 parity; 1.26.1 Family-F hoist).
    """
    total_month_index = d.month - 1 + months
    new_year = d.year + total_month_index // 12
    new_month = total_month_index % 12 + 1
    # Clamp day to last day of the new month.
    if new_month == 12:
        next_month_first = datetime.date(new_year + 1, 1, 1)
    else:
        next_month_first = datetime.date(new_year, new_month + 1, 1)
    last_day_of_new_month = (next_month_first.toordinal() - 1)
    last_day_of_new_month_date = datetime.date.fromordinal(last_day_of_new_month)
    new_day = min(d.day, last_day_of_new_month_date.day)
    return datetime.date(new_year, new_month, new_day)


def dynamic_floor(present: Iterable[int], floor: int) -> int:
    """``max(floor, oldest surviving entry)``, or ``floor`` when none survive.

    The shared kernel of the two dynamic windowing floors (the
    bookkeeping-parity Check-6 ``effective_floor``, which Check 1 also used until
    3b206, and the changelog-mirror-header-parity ``effective_cutoff``): registers whose
    aged rows are swept to the private archive scope their comparisons to
    ``max(<fixed inception constant>, min(<surviving entries>))``, so a
    swept-out entry is correctly out of scope rather than flagged. Each
    gate keeps its own inception constant and row-extraction; this is only
    the arithmetic they must not drift on.
    """
    entries = list(present)
    return max(floor, min(entries)) if entries else floor


# --- Store-scope ceiling (maintainer option B, 2026-09-30 17:07Z; simplified 21:03Z) ---
# A declaration or a clean-base scope (maintainer "Allow clean-base", 2026-10-22 01:29Z) enables
# deferral. A declaration is the single new singular root header whose PR is absent from
# the merge-base root headers and from origin/main's root headers and merge subjects. No other
# ref is consulted. Historical edits, roll-ups, a merged PR's header and example headers do not
# declare an own PR. Read origin/main locally, without fetching or API calls. Readers retain
# raw lines; uncertainty widens evaluation. The invariant: a missing or wrong record for a
# merged PR, or for the branch's own PR once declared, is never deferred, and ambiguity fails
# closed (no deferral). A clean-base scope has no new header-like line against the merge-base,
# a parseable root ceiling, and no root delimiters. Historical header-like lines already
# in the merge-base (including milestones) do not invalidate it. It uses the same readable
# origin/main evidence, protects merged PRs, and declares no own PR, so the own PR is unknown
# and cannot be protected: a trailer-only PR (D1 `Changelog:` trailer, no root header) has its
# own mirror and history entries deferred like any other open PR's until it merges, when
# origin/main's merge subject protects it. A branch that adds its root header declares and
# leaves clean-base, so its own entries are evaluated again.
#
# ONE shared, case-insensitive PR-identity grammar reads every identity (root and mirror header
# cells and register rows alike) and, from the same matched text, every range, so identity and
# range extraction cannot disagree (round-7 R7-01: a lowercase `pr` range was a certain identity
# with no range spans). `\w` is Unicode-aware, so a digit run running into a Unicode letter
# (`1309\u00e9`) is no PR number; a hyphen continues an identity only into `#` or a digit:
# `1309-REVERTED` is no identity, while `#10-#x` keeps `#10` with an uncertain tail. A `-`
# connector between two numbers is a range.
_STORE_PR_NUM = r"#?\d+(?!\w|\.\d|-(?!#|\d))"
_STORE_PR_LABEL = r"(?:PRs?\s+)?"
_STORE_PR_IDENTITY = (
    _STORE_PR_LABEL + _STORE_PR_NUM
    + r"(?:(?:\s*(?:[,&]|\band\b|-))+\s*" + _STORE_PR_LABEL + _STORE_PR_NUM + r")*"
)
STORE_PR_IDENTITY_RE = re.compile("^" + _STORE_PR_IDENTITY, re.IGNORECASE)
# The same grammar, unanchored, for the over-read (ceiling and protection) side: every identity
# run that opens on `#`.
_STORE_PR_RUN_RE = re.compile(r"(?=#)" + _STORE_PR_IDENTITY, re.IGNORECASE)
# In text the grammar matched, digits are only PR numbers and `-` is only a range connector.
_STORE_PR_PART_RE = re.compile(r"\d+|-")
# The three root and mirror header forms. Their dates and version cells are exact; their `PR`
# labels are case-insensitive like the grammar; the PR cell itself is read by the grammar.
# The legacy form has no closing delimiter, so its cell runs to the end of the line, and any PR
# identity in the tail after the identity makes it ambiguous: a `#N` token, or a run of the
# shared grammar, labelled or bare, in any case, or with its label glued on (`/ PR 2665`,
# `pr 2665`, `PRs 2665`, `/ 2665`, `PR2665`; round-8 R8-01). A compact or weekly cell is
# certain only when nothing but a `(N PRs)` count follows the identity.
CHANGELOG_HEADER_PRS_RE = re.compile(
    r"^(?:##[ \t]+\d{4}-\d{2}-\d{2},[^\n]*?\b(?i:PRs?)[ \t]+(?P<a>#\d[^\n]*)"
    r"|\*\*\d{4}-\d{2}-\d{2} \| [0-9.]+ \| (?i:PRs?) (?P<b>#\d[^*\n]*)\*\*"
    r"|\*\*Week of \d{4}-\d{2}-\d{2} \((?i:PRs?) (?P<c>#\d[^)\n]*)\)\*\*)"
)
_HEADER_PR_TOKEN_RE = re.compile(r"#(\d+)(?!\d|\.\d)")
# The legacy tail probe: the shared grammar, unanchored, opening after no word character or
# right after a glued `PR` or `PRs` label.
_HEADER_TAIL_IDENTITY_RE = re.compile(
    r"(?:(?<!\w)|(?<=PR)|(?<=PRs))" + _STORE_PR_IDENTITY, re.IGNORECASE
)
_HEADER_PR_COUNT_RE = re.compile(r"\(\d+ PRs?\)", re.IGNORECASE)
STORE_SCOPE_BASE_REF = "origin/main"
CHANGELOG_ENTRY_BOUNDARY_RE = re.compile(
    r"^(?:##[ \t]+\d{4}-\d{2}-\d{2},|\*\*\d{4}-\d{2}-\d{2} \| |\*\*Week of \d{4}-\d{2}-\d{2}\b)"
)
# A line shaped like an entry header that the boundary grammar does not read: a markdown
# heading naming a date or a `#N` token, or a bold lead-in opening on a date, `Week`, `PR` or
# `MILESTONE` (a compact header with other separators, `### 2026-09-30 PR #N`). Body
# subsection headings (`### Added`) name neither and stay body lines.
_HEADER_LIKE_RE = re.compile(
    r"^[ \t]{0,3}(?:#{1,6}\s+[^\n]*?(?:\d{4}-\d{2}-\d{2}|#\d)"
    r"|(?:\*\*|__)[ \t]*(?:\d{4}-\d{2}-\d{2}|Week\b|PRs?\b|MILESTONE\b))",
    re.IGNORECASE,
)
# Fenced-block and HTML-comment delimiters. Nothing is masked by them: they only make the
# surrounding structure uncertain, which disables deferral from the delimiter line to the end
# of the scanned text, and declaration when the delimiter line is at or above the candidate
# header.
STORE_EXAMPLE_DELIMITERS = (chr(96) * 3, "~~~", "<!--", "-->")
# Merged-PR evidence in origin/main's commit subjects: the squash-merge `(#N)` suffix and the
# merge-commit `Merge pull request #N` form. Over-reading only protects more PRs.
_MERGED_SUBJECT_PR_RE = re.compile(r"\(#(\d+)\)|^Merge pull request #(\d+)\b", re.MULTILINE)


class StorePRs(list):
    """A parsed identity with optional inclusive ranges and uncertainty."""

    def __init__(self, values: Iterable[int], *, certain: bool = True,
                 spans: tuple[tuple[int, int], ...] = ()) -> None:
        super().__init__(values)
        self.certain = certain
        self.spans = spans


def _identity_parts(identity: str) -> tuple[list[int], tuple[tuple[int, int], ...]]:
    """The PR numbers in order, and the inclusive ranges, of text the shared grammar matched."""
    values: list[int] = []
    spans: list[tuple[int, int]] = []
    dash = False
    for part in _STORE_PR_PART_RE.findall(identity):
        if part == "-":
            dash = True
            continue
        number = int(part)
        if dash and values:
            spans.append((min(values[-1], number), max(values[-1], number)))
        values.append(number)
        dash = False
    return values, tuple(spans)


def changelog_entry_boundary(line: str) -> bool:
    """Recognize entry boundaries even when their PR cells cannot be parsed."""
    return bool(CHANGELOG_ENTRY_BOUNDARY_RE.match(line))


def changelog_header_like(line: str) -> bool:
    """A recognized boundary, or a header-shaped line the boundary grammar cannot read."""
    return changelog_entry_boundary(line) or bool(_HEADER_LIKE_RE.match(line))


def store_example_delimiter(line: str) -> bool:
    """True for a line carrying a fence or HTML-comment delimiter anywhere."""
    return any(token in line for token in STORE_EXAMPLE_DELIMITERS)


def _header_identity(line: str) -> tuple[str, StorePRs]:
    """The raw PR cell of a recognized header form, and its identity under the shared grammar."""
    match = CHANGELOG_HEADER_PRS_RE.match(line)
    if not match:
        return "", StorePRs([], certain=False)
    cell = match.group("a") or match.group("b") or match.group("c") or ""
    identity = STORE_PR_IDENTITY_RE.match(cell)
    if identity is None:
        return cell, StorePRs([], certain=False)
    values, spans = _identity_parts(identity.group(0))
    tail = cell[identity.end():]
    if match.group("a") is not None:
        certain = not (_HEADER_PR_TOKEN_RE.search(tail) or _HEADER_TAIL_IDENTITY_RE.search(tail))
    else:
        certain = not _HEADER_PR_COUNT_RE.sub("", tail).strip()
    return cell, StorePRs(values, certain=certain, spans=spans)


def changelog_header_prs(line: str) -> list[int]:
    """Read complete identities; unknown or ambiguous cells remain evaluated.

    Ranges return endpoints here. Deferral separately checks their interiors
    against protected root/main ranges, without expanding large ranges.
    """
    _cell, prs = _header_identity(line)
    return list(prs) if prs.certain else []


def _header_over_read(line: str) -> tuple[list[int], tuple[tuple[int, int], ...]]:
    """The ceiling and protection side: every grammar run in the cell, plus every `#N` token.

    Over-reading only raises the ceiling and protects more PRs, so an ambiguous
    or unparsed cell still counts everything it names.
    """
    cell, _prs = _header_identity(line)
    values: list[int] = []
    spans: list[tuple[int, int]] = []
    for run in _STORE_PR_RUN_RE.finditer(cell):
        run_values, run_spans = _identity_parts(run.group(0))
        values.extend(run_values)
        spans.extend(run_spans)
    values.extend(int(n) for n in _HEADER_PR_TOKEN_RE.findall(cell))
    return values, tuple(spans)


def _ceiling_header_prs(line: str) -> list[int]:
    """Over-read ambiguous headers only on the protection/ceiling side."""
    return _header_over_read(line)[0]


def _header_ranges(line: str) -> tuple[tuple[int, int], ...]:
    """Inclusive PR coverage, represented as intervals to avoid expansion."""
    values, spans = _header_over_read(line)
    return tuple((n, n) for n in values) + spans


def _changelog_ranges(text: str) -> tuple[tuple[int, int], ...]:
    return tuple(span for line in text.splitlines() for span in _header_ranges(line))


def _contains_pr(spans: Iterable[tuple[int, int]], pr: int) -> bool:
    return any(lo <= pr <= hi for lo, hi in spans)


def store_pr_ceiling(changelog_text: str | None) -> int | None:
    """Highest raw header PR; example headers count and summary tails do not."""
    prs = [pr for line in (changelog_text or "").splitlines()
           for pr in _ceiling_header_prs(line)]
    return max(prs) if prs else None


def _store_git_text(args: list[str], repo_root: Path | str | None) -> str | None:
    root = Path(repo_root) if repo_root is not None else REPO_ROOT
    try:
        result = subprocess.run(["git", "-C", str(root), *args],
                                capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, OSError):
        return None
    return result.stdout


def merge_base_changelog(repo_root: Path | str | None = None) -> str | None:
    """Fail closed if either the merge-base or its root changelog is unreadable."""
    base = _store_git_text(["merge-base", "HEAD", STORE_SCOPE_BASE_REF], repo_root)
    if not base or not base.strip():
        return None
    return _store_git_text(["show", f"{base.strip()}:CHANGELOG.md"], repo_root)


def main_changelog(repo_root: Path | str | None = None) -> str | None:
    """Offline merged-PR evidence from the remote-tracking ref's root file."""
    return _store_git_text(["show", f"{STORE_SCOPE_BASE_REF}:CHANGELOG.md"], repo_root)


def main_merged_prs(repo_root: Path | str | None = None) -> tuple[tuple[int, int], ...] | None:
    """Offline merged-PR evidence from origin/main's commit subjects.

    A merged PR need not have a root header (D1 accepts a `Changelog:` trailer),
    so header absence alone never proves that a PR is open.
    """
    log = _store_git_text(["log", "--format=%s", STORE_SCOPE_BASE_REF, "--"], repo_root)
    if log is None:
        return None
    prs = {int(a or b) for a, b in _MERGED_SUBJECT_PR_RE.findall(log)}
    return tuple((pr, pr) for pr in sorted(prs))


def own_pr_declaration(changelog_text: str, base_changelog_text: str,
                       main_changelog_text: str = "",
                       merged_prs: Iterable[tuple[int, int]] = ()) -> tuple[int | None, str]:
    """The declared own PR, or None with the reason no PR is declared.

    The declaration is the single new (against the merge-base) singular root
    header naming a PR absent from the merge-base root headers, from
    origin/main's root headers and from origin/main's merge subjects
    (``merged_prs``), range interiors included. Historical corrections,
    roll-ups and a merged PR's header (a squash-merged or merge-committed
    parent's entry on a branch not yet rebased) therefore never declare. A new
    header-shaped line that does not parse, a second new identity, a combined
    identity, or a fence or comment delimiter at or above the candidate is
    ambiguous and fails closed, so a fenced or commented example header can
    never declare. No other ref is read: an open PR's header carried onto a
    stacked branch that has no own entry yet is indistinguishable offline from
    an own entry and declares; every deferral note names the declared PR.
    """
    base_lines = {line.strip() for line in base_changelog_text.splitlines()
                  if changelog_header_like(line)}
    known = (_changelog_ranges(base_changelog_text) + _changelog_ranges(main_changelog_text)
             + tuple(merged_prs))
    first_delimiter: int | None = None
    candidates: list[tuple[int, list[int]]] = []
    for lineno, line in enumerate(changelog_text.splitlines(), 1):
        if first_delimiter is None and store_example_delimiter(line):
            first_delimiter = lineno
        if not changelog_header_like(line) or line.strip() in base_lines:
            continue
        prs = changelog_header_prs(line) if changelog_entry_boundary(line) else []
        if not prs:
            return None, f"new root header at line {lineno} has no parseable PR identity"
        if all(_contains_pr(known, pr) for pr in prs):
            continue
        candidates.append((lineno, prs))
    if not candidates:
        return None, ("no new root header names a PR absent from the merge-base headers and "
                      "from origin/main's headers and merge subjects")
    if len(candidates) > 1:
        lines = ", ".join(str(lineno) for lineno, _ in candidates)
        return None, (f"new root headers at lines {lines} name PRs absent from the merge-base "
                      "and origin/main, so one own PR cannot be identified")
    lineno, prs = candidates[0]
    if len(set(prs)) != 1:
        return None, f"the new root header at line {lineno} names more than one PR"
    if first_delimiter is not None and first_delimiter <= lineno:
        return None, (f"a fence or comment delimiter at root line {first_delimiter} is at or "
                      f"above the candidate header at line {lineno}")
    return prs[0], ""


def declared_own_pr(changelog_text: str, base_changelog_text: str,
                    main_changelog_text: str = "",
                    merged_prs: Iterable[tuple[int, int]] = ()) -> int | None:
    """The declared own PR (see own_pr_declaration), or None."""
    return own_pr_declaration(changelog_text, base_changelog_text, main_changelog_text,
                              merged_prs)[0]


class StoreScope(NamedTuple):
    """Declaration, numeric ceiling, and offline protected PR coverage.

    ``store_scope`` declares an own PR only when the merge-base changelog and
    both origin/main readers are readable. The same evidence enables a
    clean-base scope with no own PR when no new header-like line exists against
    the merge-base; root delimiters disallow that scope. Historical milestone
    lines already present in the merge-base do not invalidate it.
    Both scopes set ``open_rule`` and protect all ``merged_prs`` evidence. A
    clean-base scope has ``own_pr`` None, so an undeclared (trailer-only) own
    PR's entries defer until it merges. A scope built
    without ``open_rule`` keeps only the ceiling rule.
    """

    root_max: int | None
    own_pr: int | None
    ceiling: int | None
    note: str | None
    branch_prs: tuple[tuple[int, int], ...] = ()
    merged_prs: tuple[tuple[int, int], ...] = ()
    open_rule: bool = False


def store_scope(changelog_text: str | None, *, repo_root: Path | str | None = None) -> StoreScope:
    text = changelog_text or ""
    root_max = store_pr_ceiling(text)
    branch_prs = _changelog_ranges(text)
    base = merge_base_changelog(repo_root)
    if base is None:
        return StoreScope(root_max, None, None,
                          "store scope fail-closed: the merge-base changelog with origin/main "
                          "is unreadable; every store entry is evaluated.", branch_prs)
    main = main_changelog(repo_root)
    merged = main_merged_prs(repo_root)
    if main is None or merged is None:
        return StoreScope(root_max, None, None,
                          "store scope fail-closed: origin/main evidence (CHANGELOG.md headers "
                          "or merge subjects) is unreadable, so no own PR can be declared; every "
                          "store entry is evaluated.", branch_prs)
    own, why = own_pr_declaration(text, base, main, merged)
    if own is None:
        # Clean-base: nothing new against the merge-base, so the own PR (if any) is unknown and
        # its entries defer like another open PR's until merged; merged PRs stay protected.
        base_headers = {line.strip() for line in base.splitlines()
                        if changelog_header_like(line)}
        clean_base = changelog_text is not None and root_max is not None and not any(
            store_example_delimiter(line)
            or (changelog_header_like(line) and line.strip() not in base_headers)
            for line in text.splitlines()
        )
        if clean_base:
            return StoreScope(
                root_max, None, root_max,
                "store scope: clean-base (no new root header against the merge-base; "
                "origin/main headers and merge subjects readable); other open PRs may "
                "defer. Offline origin/main may be stale until fetched.",
                branch_prs, _changelog_ranges(main) + merged, True)
        return StoreScope(root_max, None, None,
                          f"store scope: no own-PR declaration ({why}); every store entry "
                          "is evaluated.", branch_prs)
    return StoreScope(root_max, own, max(own, root_max or own), None, branch_prs,
                      _changelog_ranges(main) + merged, True)


_STORE_ROW_TAIL_RE = re.compile(
    r"\s*(?:(?:iteration|addendum)(?:\s+\(/retro\))?|\(/retro\))\s*", re.IGNORECASE
)


def store_row_prs(cell: str) -> StorePRs:
    """Read a leading combined identity; uncertain tails cannot defer a row.

    Prose PR mentions do not become row keys. They make deferral uncertain,
    so an unfamiliar or truncated identity still reaches row-integrity checks.
    Values and ranges come from the one grammar match, so they cannot disagree.
    """
    match = STORE_PR_IDENTITY_RE.match(cell)
    if match is None:
        return StorePRs([], certain=False)
    tail = cell[match.end():]
    certain = not tail.strip() or bool(_STORE_ROW_TAIL_RE.fullmatch(tail))
    values, spans = _identity_parts(match.group(0))
    return StorePRs(sorted(set(values)), certain=certain, spans=spans)


def store_history_prs(cell: str, keys: Iterable[int]) -> StorePRs:
    """History-row keys carrying the identity metadata deferral needs.

    The register's own token reader supplies the keys. Deferral is certain
    only when the complete leading identity names exactly those keys, and
    its ranges protect their interiors, as for retro rows.
    """
    values = sorted(set(keys))
    identity = store_row_prs(cell)
    return StorePRs(values, certain=identity.certain and list(identity) == values,
                    spans=identity.spans)


def store_deferral_reason(prs: Iterable[int], ceiling: int | StoreScope | None) -> str | None:
    """Explain a whole-entry deferral, or return None to require evaluation."""
    if not getattr(prs, "certain", True):
        return None
    named = list(prs)
    scope = ceiling if isinstance(ceiling, StoreScope) else None
    limit = scope.ceiling if scope is not None else ceiling
    if limit is None or not named:
        return None
    spans = tuple((n, n) for n in named) + getattr(prs, "spans", ())
    if scope is not None:
        protected = scope.branch_prs + scope.merged_prs
        if scope.own_pr is not None:
            protected += ((scope.own_pr, scope.own_pr),)
        if any(a <= d and c <= b for a, b in spans for c, d in protected):
            return None
    if min(named) > limit:
        return f"every named PR exceeds store-scope ceiling #{limit}"
    if scope is not None and scope.open_rule:
        return ("every named PR is another open PR, absent from branch and origin/main "
                "root headers and from origin/main merge subjects")
    return None


def store_deferral_note(prs: Iterable[int], scope: StoreScope, source: str, lineno: int) -> str:
    """One note per deferred entry, with its location, keys and reason."""
    reason = store_deferral_reason(prs, scope)
    keys = ", ".join(f"#{pr}" for pr in sorted(set(prs)))
    basis = (f"declared own PR #{scope.own_pr}" if scope.own_pr is not None
             else "clean-base scope (no declared own PR)")
    return (f"note: {source}:{lineno}: deferred {keys}: {reason}; "
            f"{basis}, ceiling #{scope.ceiling}.")


def store_deferral_flags(lines: Iterable[str], ceiling: int | StoreScope | None) -> list[tuple[bool, list[int]]]:
    """Raw per-line flags; uncertainty and example delimiters add evaluation.

    Ceiling deferral remains confined to the initial run of deferrable entries.
    The open-PR rule also reaches entries below the own entry, including
    entries whose PRs exceed the ceiling. An unknown boundary, a header-shaped
    line the grammar cannot read, or a fence/comment delimiter disables
    deferral for the remainder of the mirror, so an example cannot reopen it
    or hide a later marker, and an unrecognized header is never swallowed
    into the deferred entry above it. Nothing is stripped: example headers,
    rows and markers are still audited. Literal delimiters can therefore
    conservatively reduce deferral. Plain unmarked header lookalikes remain
    indistinguishable from real entries, including inside the own entry.
    """
    flags: list[tuple[bool, list[int]]] = []
    prs: list[int] = []
    numeric_run = True
    uncertain = False
    deferred = False
    for line in lines:
        if store_example_delimiter(line):
            uncertain = True
        if changelog_header_like(line):
            parsed = changelog_header_prs(line) if changelog_entry_boundary(line) else []
            prs = StorePRs(parsed, spans=_header_ranges(line) if parsed else ())
            if not parsed:
                uncertain = True
            reason = store_deferral_reason(prs, ceiling)
            if reason is None:
                numeric_run = False
            limit = ceiling.ceiling if isinstance(ceiling, StoreScope) else ceiling
            numeric = bool(parsed and limit is not None and min(parsed) > limit)
            open_rule = isinstance(ceiling, StoreScope) and ceiling.open_rule
            deferred = bool(reason and (numeric_run or not numeric or open_rule))
        if uncertain:
            deferred = False
        flags.append((deferred, prs))
    return flags


def above_store_ceiling(prs: Iterable[int], ceiling: int | StoreScope | None) -> bool:
    """Compatibility name for the shared ceiling-or-other-open-PR decision."""
    return store_deferral_reason(prs, ceiling) is not None


def split_row(line: str) -> list[str]:
    """Return the stripped cells of a markdown table row (bounding pipes dropped)."""
    parts = line.split("|")
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [c.strip() for c in parts]


def is_separator_row(cells: list[str]) -> bool:
    """True for a ``|---|---|`` style separator row (or an empty pipe line).

    ``cells`` is a :func:`split_row` result. An EMPTY cell list is not a
    separator (returns False). One caller (the matrix control-code gate)
    deliberately keeps its own empty-is-separator variant; the other
    table-scanning framework gates share this definition.
    """
    return bool(cells) and set("".join(cells)) <= set("-: ")


# Inline code spans. Two shapes are in live use and they are NOT
# interchangeable, so both are named here:
#
# - ``CODE_SPAN_RE`` is the multi-backtick-aware form: a run of N
#   backticks, content, a closing run of N backticks (the CommonMark
#   code-span shape, so ``...`` spans with embedded single backticks
#   are handled).
# - ``SIMPLE_CODE_SPAN_RE`` is the single-backtick form several gates
#   deliberately use (their corpora only carry single-backtick spans,
#   and the simpler pattern cannot pair two fence-like runs).
#
# What a gate does WITH a matched span (drop it, blank it
# length-preserving, mask it with a placeholder) is per-gate semantics
# and stays at the call site; only the span grammar is shared.
CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1")
SIMPLE_CODE_SPAN_RE = re.compile(r"`[^`]*`")


def strip_code_spans(line: str) -> str:
    """Return ``line`` with multi-backtick-aware inline code spans removed."""
    return CODE_SPAN_RE.sub("", line)


def is_fence_line(line: str) -> bool:
    """True if ``line`` is a fenced-code-block delimiter.

    A fence starts with three backticks (``` ``` ```) OR three tildes
    (``~~~``), preceded by zero to three ASCII spaces (the CommonMark fence
    indent limit). Four or more leading spaces are not a fence: under
    CommonMark such a line is indented code, or a paragraph continuation, so
    it neither opens nor closes a block (3b83). Tabs advance indentation to a
    multiple of four columns, so a tab before the marker also makes the line
    ineligible. This is the same rule as the AIQT generic core's
    ``aiqt_corpus.is_fence_line`` (guardrails PR #324). Container blocks are
    not modelled: a fence nested in a list item four or more columns in,
    after a block-quote ``>``, or opened on the list-marker line itself
    (``- `` then a marker) is not recognized, and a fence CommonMark closes
    where its container ends stays open to this model until the next
    recognized fence line. Both fence characters
    count so that a stray CommonMark-valid ``~~~`` fence cannot silently
    suppress scanning of everything after it (the GR-4 tilde-blindness class).

    This is the SHARED fence predicate the corpus linters use for their
    in-code-block skip loops, so a fence toggle is recognized consistently
    across gates. It replaces the per-linter private ``startswith("```")``
    checks, six of which were tilde-blind before the r5 GR-4 consolidation
    (3.10 (closing PR #937)). A toggle is a toggle: this predicate does not pair fences by
    character or match fence widths, consistent with :func:`iter_non_code_lines`.
    """
    return re.match(r" {0,3}(?:`{3}|~{3})", line) is not None


def iter_non_code_lines(text: str) -> Iterator[tuple[int, str]]:
    """Yield ``(lineno, line)`` for each line outside a fenced code block.

    ``lineno`` is 1-indexed.

    Fence detection (deliberately simple):

      - A fence is a line starting with zero to three ASCII spaces
        followed by three backticks (``` ``` ```) OR three tildes
        (``~~~``), as :func:`is_fence_line` decides. The library
        convention is backtick fences and no document currently uses
        tilde fences, but a stray CommonMark-valid ``~~~`` fence would
        otherwise silently suppress scanning of everything after it,
        so both fence characters toggle (added with the guardrail
        review's GR-4).
      - Up to three spaces of indentation before the fence are
        tolerated, the CommonMark limit. Four or more indentation
        columns, including a tab, are not a fence and do not toggle,
        so an indented backtick pair cannot hide the lines between
        it from a fence-aware gate (3b83).
      - Fence parsing is a state toggle per fence character: every
        fence line flips ``in_code``. A line containing ``\\`\\`\\``
        inside an inline code block on its own (which is unusual but
        possible) would erroneously toggle the state. The linters that
        use this helper do not encounter this in practice. Backtick
        and tilde fences are tracked with ONE toggle, not paired by
        character (a toggle is a toggle; mixed-character fence pairs
        are not a corpus shape).

    Edge cases:

      - File starts with a fence: the fence line is consumed; lines
        until the next fence are skipped; yielding resumes after the
        close.
      - Unterminated fence: every line after the unclosed fence is
        skipped. The function does not warn about unbalanced fences.
      - Nested or re-opened fences: each fence line toggles state, so
        ``` ``` ... ``` ... ``` ... ``` ``` ``` toggles include/exclude
        in pairs.

    The function does not attempt to recognize matching fence widths
    (CommonMark requires the closing fence to be at least as wide as
    the opening fence); a toggle is a toggle.
    """
    in_code = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if is_fence_line(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        yield lineno, line


# ---------------------------------------------------------------------------
# Cross-file section-reference shared constants (gates 62 and 65).
#
# The two cross-file reference linters (lint-cross-file-section-refs.py,
# the numbers phase, and lint-cross-file-section-names.py, the names
# phase) share these extraction constants. They were duplicated
# copy-with-comment until the 2026-07-04 guardrail-review G-4 hoist;
# this single definition is now the source of truth for both, so a
# sentinel or window change cannot drift between the phases.

# Cross-file section references: a section-number citation in prose.
CROSS_REF_PATTERNS = [
    re.compile(r"§\s?(\d+(?:\.\d+){0,3})"),
    re.compile(r"\bSection\s+(\d+(?:\.\d+){0,3})\b"),
]

# A markdown link to another .md file (the reference's binding target).
CROSS_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")

# The explicit binding sentence: section numbers on the line cite the
# named external standard, not a corpus document.
CROSS_BINDING_SENTINEL = "Section numbers below refer to that standard."

# A line naming an external standard: its section numbers cite that
# standard, not a corpus document.
CROSS_EXTERNAL_CONTEXT_RE = re.compile(
    r"\b(?:ISO(?:/IEC)?|IEC|NIST|OWASP|GDPR|BASC|CSA|CCM|AICM|COBIT|CTPAT|PIP|"
    r"HIPAA|PIPEDA|DORA|MiCA|SOX|Clause|Article|Annex|SP\s?800|SP\s?600|CSF|SSDF|ASVS)\b"
)

# Maximum distance (characters) between a reference and its naming link
# for the adjacent-link class.
CROSS_ADJACENCY_WINDOW = 40


# ---------------------------------------------------------------------------
# PR-delta git-range helpers (1.26.1 Family-A hoist).
#
# The PR-time delta checks D1-D4 and D7 each carried a verbatim copy of the
# same ~40 lines: a ``git`` subprocess wrapper, the positional-base fallback
# to ``origin/$GITHUB_BASE_REF``, and merge-base resolution with a shared
# error message. This is the single definition. The delta checks whose
# range resolution deliberately differs (D5's own git plus merge-base flow,
# D9's argless
# origin/main default) keep their own resolution flow.


def git(*args: str, raw: bool = False) -> str | bytes:
    """Run ``git <args>``; return stdout with only trailing newlines removed.

    Uses ``.rstrip(chr(10))`` NOT ``.strip()``: a ``-z`` caller gets NUL-delimited
    output whose paths may begin or end with whitespace, and stripping the whole
    string corrupts the first path leading whitespace; removing only trailing
    newlines still drops the trailing newline that non-``-z`` callers and
    ``resolve_pr_range`` rely on. ``raw=True`` returns stdout as bytes, neither
    decoded nor stripped, for output that need not be UTF-8 (tree entry names).
    Raises on non-zero exit."""
    out = subprocess.check_output(["git", *args], text=not raw)
    return out if raw else out.rstrip("\n")


def tree_entry_type(ref: str, path: str, *, repo: str | os.PathLike | None = None) -> str | None:
    """Object type of the tree entry at ``ref:path`` (``"blob"``, ``"tree"``, or ``"commit"``
    for a gitlink), or ``None`` when every tree on the way is readable and no entry is at
    ``path`` (a name not found, or a component before the last that is not a tree).

    Walks ``git ls-tree --full-tree -z`` from the root tree of ``ref``, one path component at a
    time, so it reads only the objects ``ref^{tree}`` peels through and the trees on the way,
    never the entry's own object, and passes no pathspec, so no pathspec magic applies to
    ``path``: a missing or corrupt blob still has a type here. ``--full-tree`` lists every
    entry wherever the caller runs; without it git lists only the part of each tree under the
    current directory, and from a subdirectory an existing entry read as absent. Entry names
    are compared as bytes with ``os.fsencode(path)``, the bytes git receives for
    ``ref:path``, so a sibling name that is not UTF-8 is never decoded. Absence is therefore
    established, never inferred from a failed read (3b551); a bad ref or an unreadable tree
    raises ``CalledProcessError``. Runs through ``git`` above, so the hook import graph gains
    no new subprocess call."""
    prefix = () if repo is None else ("-C", str(repo))
    tree = f"{ref}^{{tree}}"
    parts = os.fsencode(path).split(b"/")
    for depth, name in enumerate(parts):
        for record in git(*prefix, "ls-tree", "--full-tree", "-z", tree, raw=True).split(b"\0"):
            meta, _, entry = record.partition(b"\t")
            if record and entry == name:
                _mode, kind, oid = meta.decode("ascii").split()
                break
        else:
            return None
        if depth == len(parts) - 1:
            return kind
        if kind != "tree":
            return None
        tree = oid
    return None


def git_show(ref: str, path: str) -> str | None:
    """Return file content at ``ref:path`` or ``None`` if the file is absent.

    A failed read is ``None`` only when ``tree_entry_type`` establishes that ``ref`` holds no
    blob at ``path``: the path is absent, a gitlink, or a tree whose own object git cannot read.
    An intact tree is not a failed read: git prints its listing, and that is returned. Any other
    failure (a bad ref, an unreadable tree on the way to ``path``, a missing or corrupt blob)
    raises ``CalledProcessError``, so a git failure can never make a file read as added or
    deleted. The trailing ``--`` makes git read ``ref:path`` only as an object name: without it
    an absent path holding a glob character is taken as a pathspec and reads as ``''``. stderr
    is discarded, not decoded: git's message names the path, and a name that is not UTF-8
    would raise before the absence check (3b551)."""
    try:
        return subprocess.check_output(
            ["git", "show", f"{ref}:{path}", "--"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        if tree_entry_type(ref, path) != "blob":
            return None
        raise


# git ls-tree accepts only the top and literal pathspec magic, so an inherited
# GIT_GLOB_PATHSPECS or GIT_ICASE_PATHSPECS makes it exit 128, and
# GIT_LITERAL_PATHSPECS or GIT_NOGLOB_PATHSPECS would read the :(literal)
# prefix git_tree_entry adds as part of the name; it runs without all four.
_TREE_ENTRY_DROPPED_ENV = (
    "GIT_GLOB_PATHSPECS", "GIT_ICASE_PATHSPECS", "GIT_LITERAL_PATHSPECS", "GIT_NOGLOB_PATHSPECS",
)


def git_tree_entry(rev: str, path: str) -> tuple[str, str] | None:
    """``(type, object id)`` of the entry the tree of ``rev`` lists at
    ``path``, or ``None`` when it lists none: git's own answer that the path
    does not exist at that revision (``git ls-tree`` exits 0 and prints
    nothing). --full-tree reads ``path`` from the repository top level, as
    ``rev:path`` does, and the :(literal) prefix keeps a name that begins
    with pathspec magic literal. Any other outcome is a failure, not that
    answer, and raises for the caller to refuse on (3b577 round 5): a
    nonzero exit (``rev`` or a tree on the path unreadable) as
    CalledProcessError, git not running at all as OSError, and a listing
    that is not an ls-tree entry as ValueError."""
    env = {k: v for k, v in os.environ.items() if k not in _TREE_ENTRY_DROPPED_ENV}
    listing = subprocess.check_output(
        ["git", "ls-tree", "-z", "--full-tree", rev, "--", f":(literal){path}"],
        stderr=subprocess.DEVNULL, env=env,
    )
    if not listing:
        return None
    fields = listing.split(b"\t", 1)[0].split()
    if len(fields) != 3:
        raise ValueError(f"git ls-tree {rev} -- {path} printed {listing[:80]!r}, not an entry")
    return fields[1].decode("ascii", "replace"), fields[2].decode("ascii", "replace")


def git_show_strict(ref: str, path: str) -> str | None:
    """File content at ``ref:path``, or ``None`` only when git_tree_entry
    finds no entry there (the path does not exist at that revision) or an
    entry that is not a blob (a gitlink or a tree), which holds no file
    content: ``git show`` exits 128 on a gitlink whose commit the repository
    does not hold and prints a held commit's log or a tree's listing, so
    neither is read (3b577 round 6), as D4's blob_at reads them. As in
    git_show (3b551), a failure is never read as absence (3b577 round 5):
    the listing's own failures, and a
    listed blob whose ``git show`` read exits nonzero, raise
    CalledProcessError; git not running at all raises OSError, and content
    the locale codec cannot decode UnicodeDecodeError."""
    entry = git_tree_entry(ref, path)
    if entry is None or entry[0] != "blob":
        return None
    return subprocess.check_output(
        ["git", "show", f"{ref}:{path}"],
        text=True,
        stderr=subprocess.DEVNULL,
    )


class PrRangeError(Exception):
    """A PR base/head range could not be resolved.

    ``str(exc)`` is the exact operator-facing message the delta checks print
    to stderr before returning exit code 2; the wording predates the hoist
    and is shared verbatim by the refactored checks.
    """


def pr_range_resolution(head: str) -> tuple[str, str]:
    """``(head commit SHA, repository top-level)`` the range resolves to, in
    the repository git selects from the current directory. A ref that no
    longer resolves is echoed back verbatim and a missing work tree is
    reported as such, so a refusal message can still be composed. The top
    level is diagnostic only: git failing to run at all (OSError) or printing
    a top level the locale codec cannot decode (UnicodeDecodeError, a path
    that is not valid UTF-8) degrades it the same way, as D12's _toplevel
    does, so resolve_pr_range, which runs this on every call, keeps the
    gate's real verdict instead of escaping as a traceback (3b540 round 8).
    The head SHA is not: resolve_pr_range compares it with the merge base to
    detect a collapsed range, so its read degrades on a CalledProcessError
    only. Any other failure there leaves the SHA unread, and the echoed ref
    name would then read a collapsed range as a real one (3b540 round 9), so
    such a failure -- git failing to run at all (OSError), say -- raises
    PrRangeError instead, the refusal every resolve_pr_range caller already
    catches (exit 2 in the strict gates, D15's fail-open NOTE): never a
    fallback to the ref name and never a traceback (3b577).
    empty_pr_range_message runs this a second time, outside that handler,
    once the changed set is already empty; there the head SHA is diagnostic
    only, so it catches the PrRangeError and degrades the SHA to a
    placeholder instead (3b577 round 3)."""
    try:
        head_sha = git("rev-parse", "--verify", f"{head}^{{commit}}")
    except subprocess.CalledProcessError:
        head_sha = head
    except Exception as exc:  # noqa: BLE001 - any other failure leaves the head SHA unread
        raise PrRangeError(
            f"CANNOT-EVALUATE: git rev-parse --verify {head}^{{commit}} failed "
            f"({exc.__class__.__name__}: {exc}); without the head SHA a "
            f"collapsed range cannot be told from a real one, so nothing was "
            f"evaluated. Fix the git installation or repository state and "
            f"re-run."
        ) from exc
    try:
        toplevel = git("rev-parse", "--show-toplevel")
    except (subprocess.CalledProcessError, OSError, UnicodeDecodeError):
        toplevel = "(no work tree)"
    return head_sha, toplevel


def empty_pr_range_message(merge_base: str, head: str) -> str:
    """The CANNOT-EVALUATE message for a resolvable base..head whose changed
    set is empty. A named range that selects nothing is indistinguishable from
    a gate run against the wrong repository (a main clone whose HEAD is the
    branch point while the change lives in a worktree printed a false clean,
    orchestrator mistake 300), so the delta gates refuse it instead of
    reporting a clean pass.

    The callers run this outside their resolve_pr_range handler, after the
    range is already found empty, so the head SHA and top level here are
    diagnostic only: a head-SHA read that fails this second time (the
    PrRangeError pr_range_resolution raises) degrades to a placeholder, and
    the top level degrades as pr_range_resolution's own read does, so the
    refusal is still composed and never escapes as a traceback (3b577
    round 3)."""
    try:
        head_sha, toplevel = pr_range_resolution(head)
    except PrRangeError:
        head_sha = "(head SHA unread)"
        try:
            toplevel = git("rev-parse", "--show-toplevel")
        except (subprocess.CalledProcessError, OSError, UnicodeDecodeError):
            toplevel = "(no work tree)"
    return (
        f"CANNOT-EVALUATE: refs were named but no files changed in the range "
        f"(repo={toplevel} base={merge_base} head={head} -> {head_sha}); "
        f"nothing was evaluated. If the change lives in a worktree, run from "
        f"that worktree, or pass a base..head range that selects the change."
    )


def resolve_pr_range(base: str | None, head: str = "HEAD") -> tuple[str, str]:
    """Resolve the ``(merge_base, head)`` pair a PR-delta check diffs across.

    ``base`` is the check's optional positional base ref; when empty it
    falls back to ``origin/$GITHUB_BASE_REF`` (the GitHub Actions PR base).
    Raises :class:`PrRangeError` when neither is available, when
    ``git merge-base`` fails (typically a shallow checkout in CI), cannot
    run at all (OSError) or prints a merge base the locale codec cannot
    decode (UnicodeDecodeError; 3b577 round 4), when base and head have
    more than one merge base, or when
    base and head resolve to the same commit: a collapsed range evaluates
    nothing, and the main-clone-vs-worktree misrun it signals must surface
    as a refusal, never as a clean pass (orchestrator mistake 300).

    A criss-cross history gives base and head more than one merge base, and
    ``git merge-base`` without --all prints only one of them, so a gate
    diffing against that one alone judges a change the others would show
    differently. Every caller diffs against a single merge base, so the
    merge bases are read with --all and more than one refuses (3b577 round
    5), as does a run that prints none; D12, whose floor comparison can be
    made against each merge base in turn, reads them itself.
    """
    if not base:
        github_base = os.environ.get("GITHUB_BASE_REF")
        if not github_base:
            raise PrRangeError(
                "ERROR: base ref not provided and GITHUB_BASE_REF is unset. "
                "Pass a base ref as the first positional argument when running "
                "locally (e.g. origin/main)."
            )
        base = f"origin/{github_base}"

    try:
        merge_bases = git("merge-base", "--all", base, head).split()
    except subprocess.CalledProcessError as exc:
        raise PrRangeError(
            f"ERROR: could not determine merge-base of {base}..{head}: {exc}. "
            f"In GitHub Actions, ensure that actions/checkout uses fetch-depth: 0."
        ) from exc
    except (OSError, UnicodeDecodeError) as exc:
        # git not running at all, or a merge base that cannot be decoded,
        # leaves the range unresolved: the same refusal every caller already
        # catches, never a traceback (3b577 round 4).
        raise PrRangeError(
            f"CANNOT-EVALUATE: git merge-base --all {base} {head} failed "
            f"({exc.__class__.__name__}: {exc}); the range is undetermined, so "
            f"nothing was evaluated. Fix the git installation or repository "
            f"state and re-run."
        ) from exc
    if not merge_bases:
        raise PrRangeError(
            f"CANNOT-EVALUATE: git merge-base --all {base} {head} printed no "
            f"merge base; the range is undetermined, so nothing was evaluated. "
            f"Fix the git installation or repository state and re-run."
        )
    if len(merge_bases) > 1:
        raise PrRangeError(
            f"CANNOT-EVALUATE: {base} and {head} have {len(merge_bases)} merge "
            f"bases ({', '.join(merge_bases)}), a criss-cross history; this "
            f"gate diffs the head against one merge base, and any one of them "
            f"alone can hide the change against another, so nothing was "
            f"evaluated. Merge {base} into the branch (its tip is then the only "
            f"merge base), or rebase the branch onto {base}, and re-run."
        )
    merge_base = merge_bases[0]
    head_sha, toplevel = pr_range_resolution(head)
    if merge_base == head_sha:
        raise PrRangeError(
            f"CANNOT-EVALUATE: base {base} and head {head} resolve to the same "
            f"commit (repo={toplevel} base={merge_base} head={head_sha}); the "
            f"named range is empty, so nothing was evaluated. If the change "
            f"lives in a worktree, run from that worktree, or pass a "
            f"base..head range that selects the change."
        )
    return merge_base, head


def _existing_realpath(path: bytes) -> bytes | None:
    """realpath of ``path`` where it exists as spelled, else None (3b564 round
    6). Python's realpath tidies a trailing slash on a file and a path through
    a missing component (``missing/..``), and realpath(1) builds differ on a
    file followed by ``/.`` or ``/..``, so here the kernel must resolve the
    spelling first, as tools/git-hooks/pre-push's existing_realpath requires
    with test -e (round 7)."""
    try:
        os.stat(path)
    except OSError:
        return None
    return os.path.realpath(path)


# git's repository-local variables (git rev-parse --local-env-vars) that move
# the common directory, the object store or the history git reads, and that
# git 2.53 exported to no pre-push or commit hook, so any value refuses (3b564
# round 7). tools/git-hooks/pre-push refuses the same names.
_GIT_REDIRECT_VARIABLES = ("GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY",
                           "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_GRAFT_FILE",
                           "GIT_SHALLOW_FILE")


def require_own_git_dir(repo_root: Path, *, from_cwd: bool = False) -> str | None:
    """A refusal message when git, under the inherited environment, reads a
    repository other than ``repo_root``'s own, else None (3b564).

    A gate that checks the work tree top level against ``repo_root`` still
    printed a clean verdict over another repository's history wherever that
    top level came out as ``repo_root`` while GIT_DIR named the other
    repository: GIT_DIR alone (git then takes the current directory, or
    ``-C repo_root``, as the top level), GIT_DIR plus GIT_WORK_TREE naming
    ``repo_root``, a GIT_DIR whose own core.worktree names it, and the GIT_DIR
    git exports to the hooks of a linked worktree, which reached the main
    checkout's copy of a gate run there. This compares ``git rev-parse
    --absolute-git-dir`` read the way the gate runs git (``-C repo_root``, or
    the current directory with ``from_cwd``, as D5 and tension-scan run it)
    with the value ``repo_root`` gives with GIT_DIR and GIT_WORK_TREE removed,
    the comparison tools/git-hooks/pre-push makes. Both are canonicalized with
    realpath and compared as bytes, so no path needs to decode. Either read
    failing to run or exiting non-zero is a refusal too: the repository
    cannot be confirmed. So is either read printing anything but an absolute
    path, checked before realpath, which resolves a relative one against the
    current directory: git rev-parse echoes an option it does not know and
    exits 0, so a git without --absolute-git-dir would print the flag itself
    for both reads, and a shim git doing that made the two compare equal
    (3b564 round 3). Last, ``repo_root`` must be a work tree registered with
    the git directory git reads, the check tools/git-hooks/pre-push makes,
    ported here: a .git in ``repo_root`` that is a symbolic link refuses, and
    so do objects or refs in the common directory (``git rev-parse
    --path-format=absolute --git-common-dir``, read the way the gate runs git,
    and absolute) that are symbolic links; a .git directory must be that git
    directory and its own common directory; a .git file must be the one that
    git directory's gitdir file names, with the git directory in its common
    directory's worktrees directory (a linked worktree) or, where the git
    directory has no gitdir file and is not its parent's .git (a separate git
    directory, as a submodule's is), its own config file must give a
    core.worktree that resolves to ``repo_root`` and it must be its own common
    directory, so a separate git directory that sets no core.worktree, as git
    init or git clone --separate-git-dir leaves one, refuses with that fix. A
    main-tree alias whose .git file names another checkout's git directory
    gave both reads that directory while git took the alias as the top level,
    so it passed the comparison above and the gates' top-level check (r3
    review W1); so did an alias whose .git directory, or the git directory its
    .git file names, has a commondir file naming another checkout's git
    directory, or objects and refs that are symbolic links into it, since git
    then reports the alias's own git directory but reads that checkout's
    objects and refs (r5 review W1). Objects, refs or reftable that are
    symbolic links refuse wherever they point, so a repository whose own
    objects directory was moved and linked back (a relocated objects
    directory) and a git-new-workdir checkout, which links another
    checkout's objects, refs and hooks, refuse too, and the message names
    both (r6 review N2); reftable is checked because a reftable repository
    keeps its refs there, not in refs (r6 review N3). Paths a .git file, a
    gitdir file or core.worktree spells are compared canonically, as pre-push
    compares them: each must exist as spelled (_existing_realpath), so a
    trailing slash on a file, a path through a missing component and a file
    followed by /. or /.. refuse, here and in pre-push, whichever realpath(1)
    build it runs (round 7; r6 review W1 and N4: uutils realpath 0.10.0
    resolves the last two, and pre-push passed them).

    git's repository-local variables (``git rev-parse --local-env-vars``)
    that move what git reads refuse too (round 7). GIT_COMMON_DIR,
    GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_DIRECTORIES, GIT_GRAFT_FILE and
    GIT_SHALLOW_FILE (_GIT_REDIRECT_VARIABLES) refuse by name, whatever their
    value, before any read: git 2.53 exported none of them to a pre-push or
    commit hook in any layout tried (a checkout, a subdirectory, a linked
    worktree, a separate git directory, a submodule, git -C, --git-dir,
    --work-tree, -c and --no-replace-objects), so none is a value git chose,
    and with GIT_OBJECT_DIRECTORY naming another repository's objects this
    passed, as pre-push did, while git wrote objects there (r6 review E1). The
    three git does export refuse only where they point away from
    ``repo_root``: GIT_DIR (exported to the hooks of a linked worktree, a
    submodule or a separate git directory) through the git-directory
    comparison above; GIT_WORK_TREE (passed on from git --work-tree or the
    caller) where ``git rev-parse --show-toplevel``, read the way the gate
    runs git, is not ``repo_root``; and GIT_INDEX_FILE (exported to commit
    hooks, naming index, index.lock or next-index-<pid>.lock in the git
    directory git runs in) where the index ``git rev-parse
    --path-format=absolute --git-path index`` gives is not directly in the
    git directory git reads. The other seven moved nothing git reads when
    set to values naming another repository (git 2.53): GIT_CONFIG affects
    only git config, which is given --file here; GIT_CONFIG_PARAMETERS and
    GIT_CONFIG_COUNT add runtime configuration, as git -c does, and
    core.worktree is read from the git directory's own config file;
    GIT_NO_REPLACE_OBJECTS and GIT_REPLACE_REF_BASE choose replace refs
    within the repository; GIT_PREFIX names the caller's subdirectory; and
    GIT_IMPLICIT_WORK_TREE=0 changed no read.

    Known residuals, each passing here as it passes pre-push: a common
    directory whose objects, refs and reftable are its own directories but
    that takes another checkout's objects or refs from deeper inside them (a
    symbolic link at refs/heads, a loose ref or a pack), through a
    packed-refs file that is a symbolic or hard link, or through
    objects/info/alternates; and a .git directory that is a bind mount of
    another checkout's, which realpath does not reveal."""
    redirect = next((name for name in _GIT_REDIRECT_VARIABLES if name in os.environ), None)
    if redirect:
        return (f"{redirect} in the environment moves what git reads (its common directory, "
                f"objects, grafts or shallow file) away from this script's repository "
                f"{repo_root}; unset it and run again")
    here = [] if from_cwd else ["-C", str(repo_root)]
    own_env = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE")}
    try:
        current = subprocess.check_output(["git", *here, "rev-parse", "--absolute-git-dir"])
        own = subprocess.check_output(["git", "-C", str(repo_root), "rev-parse", "--absolute-git-dir"],
                                      env=own_env)
    except (subprocess.CalledProcessError, OSError) as exc:
        return f"could not confirm that git reads this script's repository {repo_root}: {exc}"
    current, own = current.rstrip(b"\n"), own.rstrip(b"\n")
    if not (os.path.isabs(current) and os.path.isabs(own)):
        return (f"could not confirm that git reads this script's repository {repo_root}: "
                f"git rev-parse --absolute-git-dir printed {os.fsdecode(current)!r} and "
                f"{os.fsdecode(own)!r}, not two absolute paths")
    current = os.path.realpath(current)
    own = os.path.realpath(own)
    if current != own:
        return (f"git reads the git directory {os.fsdecode(current)!r}, not this script's "
                f"repository's own {os.fsdecode(own)!r} (GIT_DIR or GIT_WORK_TREE in the "
                f"environment, or a core.worktree, points git at another repository)")
    root = os.path.realpath(os.fsencode(repo_root))
    dot_git = os.path.join(root, b".git")
    registered = False
    try:
        # git passes GIT_WORK_TREE on to hooks and names a file in the git
        # directory it runs in with GIT_INDEX_FILE, so each refuses only
        # where it points away from repo_root (round 7).
        if "GIT_WORK_TREE" in os.environ:
            top = subprocess.check_output(["git", *here, "rev-parse", "--show-toplevel"]).rstrip(b"\n")
            if not (os.path.isabs(top) and _existing_realpath(top) == root):
                return (f"GIT_WORK_TREE in the environment gives git the work tree "
                        f"{os.fsdecode(top)!r}, not this script's repository {repo_root}")
        if "GIT_INDEX_FILE" in os.environ:
            index = subprocess.check_output(
                ["git", *here, "rev-parse", "--path-format=absolute", "--git-path", "index"]).rstrip(b"\n")
            if not (os.path.isabs(index) and _existing_realpath(os.path.dirname(index)) == current):
                return (f"GIT_INDEX_FILE in the environment gives git the index "
                        f"{os.fsdecode(index)!r}, not one in the git directory "
                        f"{os.fsdecode(current)!r} it reads; unset it and run again")
        common = subprocess.check_output(
            ["git", *here, "rev-parse", "--path-format=absolute", "--git-common-dir"]).rstrip(b"\n")
        if not os.path.isabs(common):
            return (f"could not confirm that git reads this script's repository {repo_root}: "
                    f"git rev-parse --git-common-dir printed {os.fsdecode(common)!r}, not an "
                    f"absolute path")
        common = os.path.realpath(common)
        # git reads objects and refs from the common directory: a commondir
        # file naming another checkout's git directory, or objects or refs
        # there as symbolic links into one, gives git that checkout's while it
        # reports this git directory (r5 review W1). A reftable repository
        # keeps its refs in reftable (r6 review N3).
        if os.path.islink(dot_git) or any(os.path.islink(os.path.join(common, part))
                                           for part in (b"objects", b"refs", b"reftable")):
            pass
        elif os.path.isdir(dot_git):
            registered = _existing_realpath(dot_git) == current and common == current
        elif os.path.isfile(dot_git) and os.path.isfile(os.path.join(current, b"gitdir")):
            with open(os.path.join(current, b"gitdir"), "rb") as fh:
                linked = _existing_realpath(os.path.join(current, fh.read().rstrip(b"\n")))
            # A linked worktree's git directory sits in its common directory's
            # worktrees directory, where git worktree add makes it.
            registered = (linked is not None and linked == _existing_realpath(dot_git)
                          and os.path.dirname(current)
                          == _existing_realpath(os.path.join(common, b"worktrees")))
        elif os.path.isfile(dot_git) and current != os.path.join(os.path.dirname(current), b".git"):
            # Read from the git directory's own config file only, as pre-push
            # reads it, so -c and GIT_CONFIG_* cannot supply one.
            try:
                worktree = subprocess.check_output(
                    ["git", "config", "--file", os.path.join(current, b"config"), "--get", "core.worktree"])
            except subprocess.CalledProcessError:
                worktree = b""
            worktree = worktree.rstrip(b"\n")
            if not worktree:
                return (f"git reads the separate git directory {os.fsdecode(current)!r}, which "
                        f"sets no core.worktree, so this script's repository {repo_root} cannot "
                        f"be confirmed as its work tree; in that checkout run: "
                        f"git config core.worktree \"$PWD\"")
            registered = (_existing_realpath(os.path.join(current, worktree)) == root
                          and common == current)
    except (subprocess.CalledProcessError, OSError) as exc:
        return f"could not confirm that git reads this script's repository {repo_root}: {exc}"
    if not registered:
        return (f"this script's repository {repo_root} is not a work tree registered with the "
                f"git directory {os.fsdecode(current)!r} that git reads (a .git symbolic link, "
                f"a .git file naming another checkout's git directory, a git directory taking "
                f"its common directory from another checkout, or objects, refs or reftable "
                f"that are symbolic links, as in a relocated objects directory or a "
                f"git-new-workdir checkout: keep them as directories in the git directory, "
                f"or make the checkout with git worktree add); tools/git-hooks/pre-push "
                f"refuses the same layout")
    return None


# --- TODO index-format parsing (PR-1 rework, 2026-08) -----------------------
# TODO.md is an INDEX of ``| <id> | <title> | <tags> |`` rows under ``## Priority
# N`` bands; the per-item detail lives in the PRIVATE sibling's TODO-REFERENCE.md
# (relocated there in the 2026-08 migration) as ``### <id>
# <title>`` blocks. The private P-TODO.md keeps the older ``### <id>`` section
# shape until its own consolidation. These helpers parse the index form so every
# backlog reader shares one tested parser rather than re-deriving the grammar.

TODO_ID_RE = re.compile(
    r"^(?:P-\d+(?:\.\d+){1,2}[a-z]?|\d+(?:\.\d+)+(?:\.[a-z]|[a-z])?|TF-\d+)$"
)

# '**Next item number: 3.110.**', optionally a '- **...** (note)' list item.
TODO_COUNTER_RE = re.compile(
    r"^\s*-?\s*\*\*Next item number:\s*((?:\d+\.\d+)|TF-\d+)\.\*\*"
)

_TODO_TAG_RE = re.compile(r"`\[[^\]]*\]`")


def parse_todo_index(text: str) -> list[dict]:
    """Parse a new-format TODO.md index into a list of item dicts, in file order.

    Each open item is a table row ``| <id> | <title> | <tags> |`` under a
    ``## Priority N`` band. Returns ``[{"id", "title", "tags" (list of raw
    ``[..]`` code spans), "line"}]``. Rows whose first cell is not a backlog id
    (the ``| ID | Item | Tags |`` header, the ``|---|`` separator, any non-item
    row) are skipped, so the header row cannot be mistaken for an item.
    """
    items: list[dict] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = split_row(line)
        if len(cells) < 3 or is_separator_row(cells):
            continue
        item_id = cells[0].strip()
        if not TODO_ID_RE.match(item_id):
            continue
        tags = _TODO_TAG_RE.findall(cells[2])
        items.append(
            {"id": item_id, "title": cells[1].strip(), "tags": tags, "line": lineno}
        )
    return items


def todo_index_ids(text: str) -> set[str]:
    """The set of live backlog ids declared as index rows in a new-format TODO.md."""
    return {it["id"] for it in parse_todo_index(text)}


def resolve_todo_reference(repo_root: "Path | None" = None) -> "Path | None":
    """The TODO detail file (``TODO-REFERENCE.md``), private-first, or ``None``.

    Post-2026-08 migration the per-item DETAIL lives in the private sibling
    (``grc_library_private/TODO-REFERENCE.md``); the public ``TODO.md`` is an
    index-only roadmap. Resolution: the private sibling's copy if present, else
    the legacy public ``<repo>/TODO-REFERENCE.md`` (a pre-migration or adopter
    clone), else ``None``. A detail-reading backlog gate routes through this and
    no-ops on the detail when it returns ``None`` (public CI / adopter clone),
    scanning only the public index; the maintainer's run reads the private copy.
    """
    root = (repo_root or REPO_ROOT).resolve()
    # scope the private-sibling lookup to THIS root (not the global sibling), so an
    # explicit adopter/test root resolves correctly.
    private = root.parent / _SIBLING_REPO_DIRS["private"]
    if private.is_dir():
        cand = private / "TODO-REFERENCE.md"
        if cand.is_file():
            return cand
    pub = root / "TODO-REFERENCE.md"
    return pub if pub.is_file() else None


def has_todo_index_header(text: str) -> bool:
    """True iff the text contains an index TABLE HEADER row (``| ID | Item | Tags |``).

    This is the reliable signal that a backlog file is in INDEX form (versus the
    legacy ``### <id>`` block form). It is STRICTER than "contains a parseable
    index row": a legacy item whose BODY happens to hold a markdown table with a
    backlog-id-shaped first cell has no such header, so it is correctly classified
    as legacy rather than a half-converted index. Conversely a genuine index whose
    only rows are the header + separator (or malformed) still classifies as index.
    """
    in_fence = False
    for line in text.splitlines():
        if is_fence_line(line):   # 3b83: the shared predicate, not a private copy of it
            in_fence = not in_fence   # F1793-11: skip fenced example tables
            continue
        if in_fence:
            continue
        s = line.strip()
        # F1793-10: a header row STARTS with a pipe; the TERMINAL pipe is not
        # required (a header missing it is still an index header, and
        # find_malformed_index_rows flags the malformation). Requiring it let a
        # malformed header silently misclassify an index file as legacy, hiding
        # its items with no gate firing (a silent-green escape).
        if not s.startswith("|"):
            continue
        cells = split_row(line)
        if tuple(c.strip() for c in cells[:3]) == ("ID", "Item", "Tags"):
            return True
    return False


class PathContainmentError(ValueError):
    """A supplied path segment cannot be safely joined beneath its base (3b295)."""

    refusal = True


class _JoinSpellingError(ValueError):
    """Keep the offending segment for join_under's existing diagnostic."""

    def __init__(self, reason: str, segment: object):
        super().__init__(reason)
        self.segment = segment


def check_join_spelling(base: Path, *segments: str, check_length: bool = True) -> None:
    """Check raw relative components before a caller can exempt a path.

    The first pass in join_under precedes base resolution; its second pass uses
    the resolved base for PC_NAME_MAX, preserving the original error order.
    """
    if not segments:
        raise _JoinSpellingError("no segments", "<no segments>")
    for segment in segments:
        if not isinstance(segment, str) or not segment or "\0" in segment or "\\" in segment:
            raise _JoinSpellingError(
                "expected a non-empty relative string without NUL or backslash", segment)
        if Path(segment).is_absolute() or PureWindowsPath(segment).drive:
            raise _JoinSpellingError("absolute or drive-qualified segment", segment)
        if ".." in segment.split("/"):
            raise _JoinSpellingError("parent component", segment)
        if any(part in ("", ".") for part in segment.split("/")):
            raise _JoinSpellingError("empty or dot component", segment)
    if not check_length:
        return
    try:
        name_max = os.pathconf(base, "PC_NAME_MAX")
    except (OSError, ValueError):
        name_max = 255
    if name_max <= 0:
        name_max = 255
    for segment in segments:
        try:
            if any(len(os.fsencode(part)) > name_max for part in segment.split("/")):
                raise _JoinSpellingError("name too long", segment)
        except (TypeError, ValueError) as exc:
            if isinstance(exc, _JoinSpellingError):
                raise
            raise _JoinSpellingError(str(exc), segment) from exc


def join_under(base: Path, *segments: str) -> Path:
    """Check containment and return the lexical join, or refuse.

    Segments must be raw relative strings. Empty strings, empty or dot
    components, NUL bytes, backslashes, Windows drives, absolute paths
    and every parent component are refused with PathContainmentError. Existing
    components are resolved strictly, including symlinks; missing suffixes
    with valid component spellings are allowed beneath the last verified
    component. A dangling link targeting outside the base is refused. Only
    ENOENT or ENOTDIR after a verified prefix is a lookup
    failure. Other resolution errors leave containment unverifiable and
    are refusals: symbolic-link loops, unsearchable directories, single names
    too long for the filesystem, and resolved paths too long to resolve.
    A finite internal link chain that resolves successfully stays usable
    through its original lexical spelling, even if native reads reject it.
    A missing base or a base that is a file is refused. A symlinked base
    establishes its resolved target as the base. Refusal messages name the
    resolved base directory when resolution succeeds; otherwise they name
    the supplied base.
    Resolution proves containment only; the returned path preserves the base
    and relative spelling used by native lookups, including internal symlinks.

    This is a point-in-time containment check, not an atomic file operation.
    It does not prevent later symlink replacement, hard-link aliases, mount
    changes, or unsafe interpretation of the returned path by another API.
    It does not check file contents, ownership, permissions or file type.
    """
    segment = "<no segments>"
    message_base = base
    lookup_failure = False
    try:
        check_join_spelling(base, *segments, check_length=False)
        segment = str(base)
        root = Path(base).resolve(strict=True)
        message_base = root
        if not root.is_dir():
            raise ValueError("base is not a directory")
        check_join_spelling(root, *segments)
        joined = root
        for segment in segments:
            for part in Path(segment).parts:
                joined = joined / part
                try:
                    joined.lstat()
                except FileNotFoundError:
                    # The prefix was verified, and nothing can be reached beyond
                    # a missing component. Preserve the caller's native lookup.
                    return Path(base).joinpath(*segments)
                except NotADirectoryError:
                    lookup_failure = True
                    raise
                resolved = joined.resolve(strict=False)
                if not resolved.is_relative_to(root):
                    raise ValueError("resolves outside the base")
                try:
                    joined = joined.resolve(strict=True)
                except (FileNotFoundError, NotADirectoryError):
                    # The non-strict resolution above proved the dangling target
                    # is inside. Retry only the caller's original lexical lookup.
                    lookup_failure = True
                    raise
        return Path(base).joinpath(*segments)
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        if isinstance(exc, _JoinSpellingError):
            segment = exc.segment
        if message_base is base:
            try:
                message_base = Path(base).resolve(strict=True)
            except (OSError, RuntimeError, TypeError, ValueError):
                pass
        if isinstance(exc, (OSError, RuntimeError)):
            reason = (exc.strerror or "operating-system lookup failed"
                      if lookup_failure else "cannot verify containment")
        else:
            reason = str(exc)
        if not isinstance(segment, str):
            segment = f"<non-string entry: {type(segment).__name__}>"
        if isinstance(segment, str):
            if Path(segment).is_absolute() or PureWindowsPath(segment).drive:
                segment = "<absolute or drive-qualified path>"
            elif ".." in segment.split("/"):
                segment = "<path with parent component>"
        error = PathContainmentError(
            f"refused path {segment!r} under {str(message_base)!r}: {reason}"
        )
        error.refusal = not lookup_failure
        raise error from exc


def is_containment_refusal(exc: PathContainmentError) -> bool:
    """Return whether containment failed, rather than a verified lookup.

    By convention, call sites rely on join_under to mark verified lookup
    failures; the attribute is writable. An arbitrary OSError cause is
    never sufficient evidence to retry an unchecked lexical path.
    """
    return exc.refusal
