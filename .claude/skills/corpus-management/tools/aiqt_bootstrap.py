"""Verify the vendored AIQT corpus core and publish its ``aiqt_corpus`` module
in ``sys.modules`` so a corpus tool can ``from aiqt_corpus import ...`` for the
generic file/text/date/git/metadata helpers. This is the SINGLE shim for the
Corpus-Management re-point: the AIQT copy is vendored and digest-verified
against its release root (see ``.claude/aiqt/PIN.toml`` and
``lint-aiqt-vendor-digest.py``), not pip-installed. The module it publishes is
reached through ``sys.modules`` ONLY: the shim never puts the pack's
``tools/`` directory (or anything else from the pack) on ``sys.path``, and at
the START of bootstrap -- before any discovery or verification -- it takes
OWNERSHIP of the module NAME: a finder installed at the FRONT of
``sys.meta_path`` owns the name ``aiqt_corpus`` and never consults
``sys.path`` for it. Until the verified module is published that guard
refuses every import of the name with ``ModuleNotFoundError``, whatever
``sys.path`` holds (every bootstrap run first RETRACTS any earlier
publication, so each verification window fails closed), and once published
it serves ONLY the published verified module. The guard covers EXACTLY
the bare name ``aiqt_corpus``, from the first time the guard is installed
onward: from then on no ``sys.path`` entry of any shape -- literal,
symlinked, retargeted after the scrub, relative and re-resolved after a
chdir, or a plain directory holding a symlink named ``aiqt_corpus.py`` --
can make the on-disk file importable under that bare name
(RBQ38-c3-scrub-toctou, RBQ38-c3-file-symlink-alias). An import of the
name made BEFORE the guard is first installed resolves through
``sys.path`` like any other import; the module it leaves behind
carries no installation marker -- unless the planted file's own body
SET the marker attribute, a disclosed forgery that survives the
no-bytes failure corner (RBQ57-c3-self-marked-planted, below) -- and
an unmarked one is refused by the marker check when the bootstrap
then runs. EVERY refusal of an ``aiqt_corpus`` found in ``sys.modules``
-- and a bootstrap failure of ANY exception type, not only
``ImportError`` (RBQ53-c3-non-importerror-failure), after an UNMARKED
pre-existing module was seen -- REMOVES that refused or unmarked
module from ``sys.modules`` under the import lock (when
the name still binds that same object), through ONE shared helper,
before the error propagates, so a later import of the name in this
process fails closed through the unpublished guard instead of
returning the unmarked module (RBQ43-c3-prebootstrap-module-stays,
RBQ48-c3-other-refusal-paths); a module that carries the installation
marker for the verified bytes -- published by this run, an earlier
run, or a racing run, even as the SAME pre-existing object -- is
never removed or unpublished by another run's failure, only by a
check that actually refused it
(RBQ51-c3-handler-unpublishes-verified,
RBQ53-c3-left-alone-wording). The SAME pack file imported under a DOTTED or other module name
is NOT covered by the guard (RBQ40-c3-dotted-name-residual): the guard
protects the BARE NAME ``aiqt_corpus`` and nothing else. As a CLASS,
ANY ``sys.path`` entry from which the pack's files can be reached under
a path of Python identifiers can import the same file under another
name, without the installation marker -- a pack root, a pack root's
parent, an identifier-named ancestor of a pack root, an entry holding
a symlink (at any depth) to a pack directory
(RBQ48-c3-symlink-dotted-route), the empty entry or ``.`` while the
working directory is such a place (RBQ48-c3-empty-entry-route), and
any other such route; those are EXAMPLES, and no list of such routes
here is complete. As a SECOND, BEST-EFFORT layer the shim removes the
entry shapes it recognises: every ``sys.path`` entry whose RESOLVED
path (``os.path.realpath``; the empty entry resolves against the
current working directory, exactly like ``.``) is a pack ``tools/``
directory (RBQ34-c3-symlink-alias, RBQ33-c3-stale-path-race,
RBQ28-c3-tools-on-path, RBQ27-c3-concurrent-import), a pack ROOT, or a
pack root's PARENT (RBQ43-c3-repo-root-premise,
RBQ48-c3-empty-entry-route). The repository root carries NO dotted
route of its own to the in-repo pack: ``.claude`` is not a Python
identifier, so no dotted spelling reaches the in-repo pack file
through a repository-root entry (established by execution), and that
entry is kept; routes the scrub does not recognise, loads of the pack
file BY PATH, and removal of the guard itself are disclosed under
REMAINING below.

Only the corpus tools that import the generic ``aiqt_corpus`` helpers import
this module; a tool that needs only grc-local config/store helpers keeps
importing ``lint_common`` and does not touch this shim.

The shim VERIFIES the selected copy before importing any of its code:
``aiqt_rules.verify_vendor_dir()`` checks the pin record's shape and
schema version, the release root (the pin, the root record, and the recomputed
manifest digest must agree), and every vendored file's byte count and SHA-256
against its manifest row, with no missing, extra, symlinked, or special entry
and no unlistable directory. A selected copy that does not verify raises
``ImportError``.

Discovery:

1. ``AIQT_PACK_ROOT`` (the AIQT-standard name) or ``GRC_AIQT_PACK`` env var
   (explicit override for a non-default layout or a test harness). A set,
   non-empty override is STRICT (RBQ33-c3-explicit-root-fallback): the named
   root must carry a regular ``tools/aiqt_corpus.py`` and a regular
   ``PIN.toml`` (checked with a non-following lstat) and must then verify as
   above, or the shim raises ``ImportError``. There is NO fallback: a named
   root that is missing, shapeless, or unverifiable never falls through to
   discovery or to the in-repository copy, so a stale variable fails loud
   instead of silently selecting another pack. An override must additionally
   not be or cross a symlinked path component (checked without following
   links, before any verification, and the path is never resolve()d:
   RBQ11-bootstrap-symlinked-override), and its verified release root must
   equal THIS repository's committed ``.claude/aiqt/PIN.toml`` release root; a
   self-consistent pack pinned to a different root is refused, and a missing
   or unreadable repository pin refuses every override
   (RBQ11-override-not-pinned). The repository pin is read only through
   link-free, expected-type path components, so a symlinked ``.claude/aiqt``
   cannot hand the override its own trust anchor
   (RBQ14-repo-pin-symlinked-vendor), and the release root compared is the
   one verification itself validated, never a re-read of the override's pin
   record (RBQ14-pin-reread-race).
2. With no override set: the in-repo vendored location
   ``<repo>/.claude/aiqt/``, the digest-verified copy CI and dev both use
   (this file lives at ``<repo>/.claude/skills/corpus-management/tools/``, so
   ``parents[4]`` is the repo root). An in-repo copy that is present but does
   not verify fails LOUD rather than falling through.

Discovery STOPS at the repository root: the earlier dev-convenience walk UP
from this file is removed, because it could import an unverified
``aiqt_corpus.py`` from an ancestor outside this checkout.

Importing the vendored corpus writes no bytecode inside the vendor tree:
the module is executed from captured in-memory bytes, never from the file,
and ``ensure_on_path()`` additionally disables bytecode writing for this
process (``sys.dont_write_bytecode = True``), so nothing can create
``tools/__pycache__/`` under the digest-pinned ``.claude/aiqt/`` and then
fail the digest gate.

The consumer's ``import aiqt_corpus`` runs the VERIFIED bytes, not a re-read:
after verification succeeds, the shim reads ``tools/aiqt_corpus.py`` once
more THROUGH THE VERIFIER'S non-following, nonblocking regular-file reader
(so a symlink, FIFO, or other special file swapped into place is refused,
never followed or blocked on: RBQ27-c3-capture-fifo), refuses unless those
bytes still match the file's manifest row (RBQ26-c3-module-swap-race), then
compiles exactly those captured bytes with ``dont_inherit=True`` (so the
verified code runs with default compiler flags, not with this shim's
``from __future__ import annotations``: RBQ28-c3-compile-inherit) and
executes them into a FRESH module object that is NOT yet in ``sys.modules``,
while holding NO import lock (RBQ33-c3-import-lock-deadlock): a concurrent
``import aiqt_corpus`` during execution finds no ``aiqt_corpus`` in
``sys.modules`` and is refused by the name guard on ``sys.meta_path`` BEFORE
``sys.path`` is ever consulted for the name, so it fails closed with
``ModuleNotFoundError``; it can neither wait on a lock the shim holds, nor
see a half-built module, nor import the on-disk file
(RBQ27-c3-concurrent-import, RBQ38-c3-scrub-toctou). Only after execution completes is the module
published in ``sys.modules``, under the interpreter's global import lock
held just for that dictionary check-and-insert (no module code runs under
it). The loader marks the module it built with an installation marker (the
SHA-256 of the captured verified bytes): an ``aiqt_corpus`` already in
``sys.modules`` is accepted ONLY when it carries that marker for the bytes
this bootstrap verified AND its origin resolves to the located copy's
``tools/aiqt_corpus.py`` -- never by origin alone
(RBQ33-c3-stale-path-race) -- and ``ensure_on_path()`` re-checks both the
marker and the origin again AFTER installation
(RBQ33-c3-origin-recheck-comment).

REMAINING, disclosed: the byte pinning covers only ``tools/aiqt_corpus.py``
(today the only vendored code the shim imports, itself stdlib-only); any
other vendored file read after verification is an ordinary disk re-read.
The import-by-NAME surface is held by the ``sys.meta_path`` name guard, not
by ``sys.path`` matching: the guard never consults ``sys.path`` for
``aiqt_corpus``, so no entry of any shape -- a literal pack ``tools/``
entry, a symlinked alias, a symlink retargeted AFTER the scrub, a path
created or renamed into place, a relative entry re-resolved after a chdir
(RBQ38-c3-scrub-toctou), a plain directory holding a symlink named
``aiqt_corpus.py`` (RBQ38-c3-file-symlink-alias), a bind mount, a
hard-linked copy, an entry re-inserted after bootstrap begins, or the ``''``
entry -- can decide what ``import aiqt_corpus`` yields. What the name guard
does NOT cover, disclosed: code that loads the pack file BY PATH
rather than by name (``importlib.util.spec_from_file_location``,
``runpy.run_path``, or an ``exec`` of read bytes) never consults
``sys.meta_path`` and is outside every import-system control here; code
that REMOVES or reorders the guard on ``sys.meta_path`` (an ordinary
writable list), or inserts its own finder in FRONT of it, re-opens the name
-- such code is already running in this process and needs no import tricks;
and the guard owns ONLY the bare name ``aiqt_corpus``: the SAME pack
file can be imported under a DOTTED or other module name through ANY
``sys.path`` entry from which the pack's files can be reached under a
path of Python IDENTIFIERS, and no list of such routes here is
complete. EXAMPLES, each established by execution: a pack-root entry
(``import tools.aiqt_corpus``); a pack-root-parent entry such as
``.claude`` (``import aiqt.tools.aiqt_corpus``); for an OVERRIDE pack,
ANY chain of identifier-named ancestors (``import
pk.tools.aiqt_corpus`` through the pack root's parent,
``import grand.pk.tools.aiqt_corpus`` through its grandparent, and so
on); a plain entry holding a SYMLINK, at any depth, to a pack
directory (``import xtools.aiqt_corpus`` through an entry whose
``xtools`` link targets a pack ``tools/``, or
``import yclaude.aiqt.tools.aiqt_corpus`` through one whose
``yclaude`` link targets a pack root's parent:
RBQ48-c3-symlink-dotted-route, a disclosed residual the scrub does not
recognise); and the empty entry or ``.`` while the working directory
is such a place (RBQ48-c3-empty-entry-route); the REPOSITORY ROOT does
NOT carry a dotted route of its own -- ``.claude`` is not a Python
identifier, so every dotted spelling through a repository-root entry
fails with ``ModuleNotFoundError`` (RBQ43-c3-repo-root-premise; the
earlier claim that the repository root was such a route was false).
The second-layer ``sys.path`` scrub is BEST-EFFORT: it removes the
entry shapes it RECOGNISES -- entries that RESOLVE to a pack
``tools/`` directory, to a pack ROOT, or to a pack root's PARENT, with
the empty entry resolved against the current working directory exactly
like ``.`` (nothing in this tree relies on such an entry; the
repository root, which carries no dotted route of its own, is kept) --
and it decides once, at
scrub time, by resolved path, so an entry it cannot see, or whose target
changes after it ran, keeps a module of ANOTHER name planted in a pack
``tools/`` importable through that entry (for the bare name
``aiqt_corpus`` the guard closes it); every route the scrub does not
recognise REMAINS, among them an identifier-named ancestor entry two
or more levels above an OVERRIDE pack root and a plain entry holding a
symlink to a pack directory at any depth
(RBQ40-c3-dotted-name-residual, RBQ48-c3-symlink-dotted-route). An import of
``aiqt_corpus`` made BEFORE this shim is first loaded -- before the guard
exists -- resolves through ``sys.path`` like any other import; the module
it leaves in ``sys.modules`` carries no installation marker -- unless
the planted file's own body SET the marker attribute
(RBQ57-c3-self-marked-planted) -- and an unmarked one is
refused by the marker check when the bootstrap then runs; EVERY such
refusal -- and a bootstrap failure of ANY exception type
(RBQ53-c3-non-importerror-failure) after an UNMARKED pre-existing
module was seen -- REMOVES the refused or unmarked module from
``sys.modules`` under the
import lock (when the name still binds the same object), through ONE
shared helper, before the error propagates, so a later
``import aiqt_corpus`` in this process fails closed through the
unpublished guard instead of returning the unmarked module
(RBQ43-c3-prebootstrap-module-stays,
RBQ48-c3-other-refusal-paths); a module carrying the installation
marker for the verified bytes is never removed or unpublished by
another run's failure (RBQ51-c3-handler-unpublishes-verified). The
installation marker is an ordinary module attribute: code already
running in this process can forge it -- including the BODY of a
planted on-disk ``aiqt_corpus.py`` run by a pre-guard import --
which is outside this shim's threat model; a module self-marked that
way survives a bootstrap failure that happened BEFORE any bytes were
captured, and a later plain import returns it from ``sys.modules``
with no acceptance check, until a run that captured bytes refuses
and removes it (RBQ57-c3-self-marked-planted, disclosed in
``_marked_for_verified_bytes``). A thread that imports ``aiqt_corpus`` before this shim has published
it fails with ``ModuleNotFoundError`` (fail closed) rather than waiting.

It fails LOUD (``ImportError`` naming the fix) when the vendored copy cannot
be found or does not verify, so a broken setup surfaces here rather than as a
downstream ``No module named aiqt_corpus``. The discovery lives ONLY in this
file: if the upstream discovery convention changes, this shim changes and the
re-pointed tools do not (their ``from aiqt_corpus import ...`` line is stable,
exactly the point of a single shim).
"""

from __future__ import annotations

import _imp  # the interpreter's own global import lock (reentrant per thread)
import collections.abc
import hashlib
import importlib.abc
import importlib.machinery
import importlib.util
import os
import stat
import sys
from pathlib import Path

__all__ = ["ensure_on_path", "find_pack_tools"]

_verified_corpus_source: bytes | None = None

# The attribute the verified-source loader sets on a module it executed from
# the captured verified bytes: the SHA-256 hex digest of exactly those bytes.
# ensure_on_path() accepts an aiqt_corpus already in sys.modules ONLY when
# this marker matches the digest of the bytes the CURRENT verification
# captured (and the origin matches too); a module that reached sys.modules
# any other way -- an import of the on-disk file through a stale sys.path
# entry above all -- carries no marker and is refused, whatever its origin
# claims (RBQ33-c3-stale-path-race).
_INSTALL_MARKER_ATTR = "__aiqt_bootstrap_installed_digest__"


def _module_marker(module):
    """The installation marker of ``module``, or ``None`` when it carries
    none. EVERY site that reads the marker reads it through this helper:
    a ``sys.modules`` entry need not be a real module object, and an
    object with a MISSING or NON-MAPPING ``__dict__`` (an int, a
    ``__slots__`` instance planted in-process) is treated as UNMARKED --
    refused and removed like any other impostor -- never an
    ``AttributeError`` that would replace the original bootstrap error
    inside the failure handler and leave the object importable
    (RBQ57-c3-no-dict-module). Any entry whose NAMESPACE CANNOT BE
    READ, or whose MARKER LOOKUP RAISES an ``Exception`` -- a
    ``__dict__`` descriptor raising any ``Exception``, where plain
    ``getattr`` suppresses only ``AttributeError`` -- is treated as
    UNMARKED the same way, never an exception that would replace the
    original bootstrap error (RBQ58-c3-dict-descriptor-raises). ONLY
    ``Exception`` is caught -- catching ``BaseException`` here would
    swallow a REAL ``KeyboardInterrupt`` landing in this window -- so
    a descriptor raising a ``BaseException`` subclass still CRASHES
    the read and the entry SURVIVES: a DISCLOSED residual of the same
    in-process forgery class as RBQ57/RBQ58
    (RBQ59-c3-baseexception-descriptor-wording)."""
    try:
        namespace = getattr(module, "__dict__", None)
        if not isinstance(namespace, collections.abc.Mapping):
            return None
        return namespace.get(_INSTALL_MARKER_ATTR)
    except Exception:
        return None


class _PublishedVerifiedLoader(importlib.abc.Loader):
    """Serves the ALREADY-EXECUTED published verified module when an import
    resolves through the name guard after publication (the name was popped
    from ``sys.modules``): ``create_module`` returns the published module
    object itself and ``exec_module`` runs nothing, so no disk bytes are
    read or executed on this path (RBQ38-c3-scrub-toctou)."""

    def __init__(self, module) -> None:
        self._module = module

    def create_module(self, spec):
        return self._module

    def exec_module(self, module) -> None:
        if module is not self._module:
            raise ImportError(
                "the aiqt_corpus name guard serves only the published "
                "verified module; refusing to execute into any other module "
                "object (RBQ38-c3-scrub-toctou)."
            )


class _AiqtCorpusNameGuard(importlib.abc.MetaPathFinder):
    """Owns the module NAME ``aiqt_corpus`` from the front of
    ``sys.meta_path`` (RBQ38-c3-scrub-toctou, RBQ38-c3-file-symlink-alias):

    - it never consults ``sys.path`` for the name, so no path entry of any
      shape -- literal, symlinked, retargeted after the scrub, relative and
      re-resolved after a chdir, a plain directory holding a symlink named
      ``aiqt_corpus.py``, a bind mount, or a hard-linked copy -- can decide
      what an ``import aiqt_corpus`` yields;
    - until the verified module is PUBLISHED it refuses every import of the
      name with ``ModuleNotFoundError`` (fail closed, never blocking);
    - once published it serves ONLY the published verified module (already
      executed from the captured verified bytes; nothing re-runs);
    - every bootstrap run RETRACTS any earlier publication when it installs
      the guard, so DURING every verification window -- a first bootstrap
      or a re-bootstrap -- the name always fails closed; the module a
      prior run left in ``sys.modules`` is untouched by the retraction.

    Finders for every other name are untouched (``find_spec`` returns
    ``None`` for them immediately). The guard covers EXACTLY the bare name
    ``aiqt_corpus``: code that loads the pack file by PATH, or under
    ANOTHER module name (a dotted import through any ``sys.path`` entry
    from which the pack's files are reachable under identifier names:
    RBQ40-c3-dotted-name-residual), or that removes
    this finder from ``sys.meta_path``, is outside it and disclosed under
    REMAINING in the module docstring."""

    # The tag by which a newer load of this same shim replaces a stale
    # guard left by an earlier load (tests load the shim repeatedly).
    _aiqt_bootstrap_name_guard = True

    def __init__(self) -> None:
        self._module = None
        self._origin: str | None = None

    def publish(self, module) -> None:
        """Hand the guard the verified module: from now on imports of the
        name are served from it (or from ``sys.modules``), never from
        disk."""
        self._origin = (getattr(getattr(module, "__spec__", None),
                                "origin", None)
                        or getattr(module, "__file__", None))
        self._module = module

    def retract(self) -> None:
        """Take the name back to the fail-closed state (no published
        module): every bootstrap run calls this through
        ``_install_name_guard()`` BEFORE any discovery or verification, so
        an import inside the new run's verification window is refused even
        when an earlier run had published (RBQ38-c3-scrub-toctou)."""
        self._module = None
        self._origin = None

    def find_spec(self, fullname, path=None, target=None):
        if fullname != "aiqt_corpus":
            return None
        module = self._module
        if module is None:
            raise ModuleNotFoundError(
                "import of aiqt_corpus refused by the aiqt_bootstrap name "
                "guard: no verified module has been published (the "
                "bootstrap has not finished, or it failed), and the name "
                "is never resolved through sys.path, so no stale, aliased, "
                "retargeted or relative sys.path entry can make the "
                "on-disk file importable (RBQ38-c3-scrub-toctou, "
                "RBQ38-c3-file-symlink-alias). Run ensure_on_path() to "
                "publish the verified module.",
                name="aiqt_corpus")
        spec = importlib.util.spec_from_loader(
            "aiqt_corpus", _PublishedVerifiedLoader(module),
            origin=self._origin)
        if self._origin is not None:
            spec.has_location = True
        return spec


_NAME_GUARD = _AiqtCorpusNameGuard()


def _install_name_guard() -> None:
    """Put THIS shim instance's name guard at the FRONT of ``sys.meta_path``
    -- before any discovery or verification -- and drop guards left by
    earlier loads of this same shim, under the global import lock, so an
    import that is already waiting resolves against the installed guard.
    The front position means the guard decides the name before any
    path-based finder; a superseded guard behind it could otherwise serve a
    module from an earlier bootstrap. On EVERY run the list is rewritten by
    ONE atomic slice assignment that puts the guard first and drops every
    other copy of it and every stale tagged guard, so a finder that was
    placed in front of it between runs is displaced behind it by the next
    bootstrap (RBQ40-c3-guard-not-refronted) and the guard is never ABSENT
    from ``sys.meta_path`` for even an instant of a re-run: the importer's
    UNLOCKED ``list(sys.meta_path)`` snapshot (taken before any import
    lock) can never land in a guardless gap, as the two-step
    remove-then-insert form allowed (RBQ43-c3-refront-race). Retraction
    opens no window of its own: it only unpublishes while the guard stays
    in place. A finder inserted in front AFTER the last bootstrap run,
    with no further run, stays in front and is disclosed under REMAINING. Any earlier publication is RETRACTED
    here, so the verification window of THIS run fails closed too. The
    guard STAYS installed after bootstrap: an unpublished guard left by a
    FAILED bootstrap keeps the name failing closed rather than reopening
    ``sys.path`` (RBQ38-c3-scrub-toctou, RBQ38-c3-file-symlink-alias)."""
    _imp.acquire_lock()
    try:
        _NAME_GUARD.retract()
        refronted = [_NAME_GUARD]
        refronted.extend(
            finder for finder in sys.meta_path
            if finder is not _NAME_GUARD
            and not getattr(finder, "_aiqt_bootstrap_name_guard", False))
        # ONE list mutation: the new contents are built first, then written
        # with a single slice assignment, so during a re-run sys.meta_path
        # never passes through a state without the guard
        # (RBQ43-c3-refront-race).
        sys.meta_path[:] = refronted
    finally:
        _imp.release_lock()


def _load_verifier():
    """The pin verifier (aiqt_rules), loaded by explicit file path from this
    shim's own directory, so the lookup cannot be redirected through
    ``sys.path`` and never imports from the copy under verification."""
    path = Path(__file__).resolve().parent / "aiqt_rules.py"
    spec = importlib.util.spec_from_file_location("_aiqt_bootstrap_verifier", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _has_module(pack_root: Path) -> bool:
    """The pack shape the IN-REPO location is discovered by; an explicit
    override uses the stricter ``_require_pack_shape`` instead."""
    try:
        return ((pack_root / "tools" / "aiqt_corpus.py").is_file()
                and ((pack_root / ".aiqt").exists() or (pack_root / "PIN.toml").is_file()))
    except OSError:
        return False


def _verified(pack_root: Path, what: str) -> tuple[Path, str, bytes]:
    """Verify the selected copy's release root, manifest inventory, and file
    types BEFORE any of its code is imported; an unverifiable copy raises
    ImportError (fail loud, never fall through). Returns the pack root
    together with the release root the verifier itself validated, so a later
    comparison never has to re-read the pack's pin record
    (RBQ14-pin-reread-race). Also RETURNS the captured bytes of
    ``tools/aiqt_corpus.py``: the file is read once more AFTER verification,
    through the verifier's own non-following, nonblocking regular-file reader
    (so a symlink or FIFO swapped into place is refused, never followed or
    blocked on: RBQ27-c3-capture-fifo), and refused unless those bytes still
    match the file's manifest row; ``ensure_on_path()`` later executes
    exactly the captured bytes, so a rewrite of the module between
    verification and import is refused here or has no effect
    (RBQ26-c3-module-swap-race). This function never assigns
    ``_verified_corpus_source``: the caller assigns it only after the
    copy is ADMITTED (for an override, only after
    ``_pinned_to_repository``), so the bytes of a self-consistent but
    REFUSED pack can never become the reference the failure handler
    validates installation markers against
    (RBQ57-c3-refused-override-bytes)."""
    rules = _load_verifier()
    try:
        pin, inventory = rules.verify_vendor_dir(pack_root)
    except Exception as exc:
        raise ImportError(
            f"the {what} AIQT copy at {pack_root} does not verify against its pin "
            f"record and release manifest ({type(exc).__name__}: {exc}); refusing to "
            "expose or import unverified code. Re-vendor from the pinned release "
            "(see .claude/aiqt/PIN.toml and lint-aiqt-vendor-digest.py), or point "
            "AIQT_PACK_ROOT (or GRC_AIQT_PACK) at a copy that verifies."
        ) from exc
    rel = "tools/aiqt_corpus.py"
    try:
        row = inventory.get(rel)
        if row is None:
            raise ValueError(f"{rel} has no row in the verified manifest inventory")
        data = rules._read_bytes(pack_root / rel, "vendored corpus module")
        nbytes, filedigest = row
        if len(data) != nbytes or rules.sha(data) != filedigest:
            raise ValueError(
                f"{rel} no longer matches its manifest row: the file changed "
                "between verification and the byte capture")
    except (OSError, ValueError) as exc:
        raise ImportError(
            f"the {what} AIQT copy at {pack_root} cannot pin the corpus module's "
            f"verified bytes ({type(exc).__name__}: {exc}); refusing to expose or "
            "import code whose executed bytes could differ from the verified ones "
            "(RBQ26-c3-module-swap-race)."
        ) from exc
    return pack_root, pin["source"]["release-root"], data


class _VerifiedSourceLoader(importlib.abc.Loader):
    """Executes ``aiqt_corpus`` from the exact bytes ``_verified()`` captured
    and digest-checked, never from a re-read of the file, so the code that
    runs is the code that was verified (RBQ26-c3-module-swap-race). The
    compile uses ``dont_inherit=True``: the verified bytes get the default
    compiler flags, not this shim's ``from __future__ import annotations``
    (RBQ28-c3-compile-inherit). After a successful execution the loader sets
    the installation marker (the SHA-256 of the executed bytes) on the
    module, so the bootstrap can later tell a module it built from the
    captured bytes apart from one that reached ``sys.modules`` any other way
    (RBQ33-c3-stale-path-race)."""

    def __init__(self, origin: str, source: bytes) -> None:
        self._origin = origin
        self._source = source

    def create_module(self, spec):
        return None

    def exec_module(self, module) -> None:
        exec(compile(self._source, self._origin, "exec", dont_inherit=True),
             module.__dict__)
        module.__dict__[_INSTALL_MARKER_ATTR] = hashlib.sha256(self._source).hexdigest()

    def get_source(self, fullname: str) -> str:
        return self._source.decode("utf-8")


def _install_verified_corpus(tools: Path) -> None:
    """Install ``aiqt_corpus`` into ``sys.modules`` from the bytes
    ``_verified()`` captured and digest-checked, so the consumer's
    ``import aiqt_corpus`` never re-reads ``tools/aiqt_corpus.py`` from disk
    (RBQ26-c3-module-swap-race). Refuses when no captured bytes exist (fail
    closed). The captured bytes are executed into a fresh module object that
    is NOT yet in ``sys.modules``, while holding NO import lock: a concurrent
    ``import aiqt_corpus`` during execution finds nothing and fails closed
    with ``ModuleNotFoundError`` -- it can neither block on a lock this shim
    holds (the deadlock when another thread is partway through importing a
    dependency such as ``subprocess``: RBQ33-c3-import-lock-deadlock) nor
    see a partially initialized module. Only after execution completes is
    the module published, under the global import lock held just for the
    ``sys.modules`` check-and-insert (no module code runs under it). An
    ``aiqt_corpus`` that appeared in ``sys.modules`` meanwhile is kept only
    when it carries this bootstrap's installation marker for the same
    verified bytes (another ``ensure_on_path()`` won the publish race);
    anything else is refused and REMOVED from ``sys.modules`` through the
    one shared helper (RBQ48-c3-other-refusal-paths).
    ``ensure_on_path()`` re-checks the installed
    module's marker and origin after this returns
    (RBQ33-c3-origin-recheck-comment). A failed execution publishes
    nothing. A successful publication also hands the module to the
    ``sys.meta_path`` name guard, which from then on serves ONLY the
    published verified module (RBQ38-c3-scrub-toctou)."""
    source = _verified_corpus_source
    if source is None:
        raise ImportError(
            "no verified aiqt_corpus bytes were captured for the located copy; "
            "refusing to import the module from an unverified re-read "
            "(RBQ26-c3-module-swap-race)."
        )
    origin = str(tools / "aiqt_corpus.py")
    loader = _VerifiedSourceLoader(origin, source)
    spec = importlib.util.spec_from_loader("aiqt_corpus", loader, origin=origin)
    spec.has_location = True
    module = importlib.util.module_from_spec(spec)
    # Execute the captured verified bytes into the unpublished module,
    # holding no import lock (RBQ33-c3-import-lock-deadlock).
    loader.exec_module(module)
    _imp.acquire_lock()
    try:
        existing = sys.modules.get("aiqt_corpus")
        if existing is None:
            sys.modules["aiqt_corpus"] = module
            published = module
        elif _module_marker(existing) != hashlib.sha256(source).hexdigest():
            # The refused module must not stay importable: the one shared
            # helper removes it before the error propagates (the import
            # lock is reentrant for this thread)
            # (RBQ48-c3-other-refusal-paths).
            _remove_refused_module(existing)
            raise ImportError(
                "an aiqt_corpus appeared in sys.modules while the verified module "
                "was executing, and it does not carry this bootstrap's installation "
                "marker for the verified bytes; refusing to accept a module that was "
                "not installed from the captured verified bytes "
                "(RBQ33-c3-stale-path-race, RBQ48-c3-other-refusal-paths)."
            )
        else:
            # another ensure_on_path() published a module built from the
            # same verified bytes first; keep it.
            published = existing
        # From now on the name guard serves ONLY this published verified
        # module; an import of the name never consults sys.path
        # (RBQ38-c3-scrub-toctou, RBQ38-c3-file-symlink-alias).
        _NAME_GUARD.publish(published)
    finally:
        _imp.release_lock()


def _refuse_symlinked_override(root: Path, what: str) -> None:
    """Refuse an override that is, or crosses, a symlinked path component:
    the named path and every ancestor are checked with a non-following lstat
    BEFORE verification and WITHOUT any resolve(), so the pack the verifier
    reads is exactly the pack the path names and a link cannot redirect it
    (RBQ11-bootstrap-symlinked-override). A component that cannot be checked
    refuses too (fail closed)."""
    for component in (root, *root.parents):
        try:
            symlinked = component.is_symlink()
        except OSError as exc:
            raise ImportError(
                f"the {what} AIQT override {root} cannot be checked for symlinked "
                f"path components at {component} ({type(exc).__name__}: {exc}); "
                "refusing to expose or import code through it."
            ) from exc
        if symlinked:
            raise ImportError(
                f"the {what} AIQT override {root} is or crosses a symlinked path "
                f"component at {component}; refusing to follow links to a pack. "
                "Point the override at the pack's real, link-free path."
            )


def _require_pack_shape(root: Path, what: str) -> None:
    """An explicit override is STRICT (RBQ33-c3-explicit-root-fallback): the
    named root must carry a regular ``tools/aiqt_corpus.py`` and a regular
    ``PIN.toml``, each checked with a non-following lstat on its final
    component. Anything else -- a missing root, a shapeless root, a special
    or symlinked entry -- raises ImportError, and discovery NEVER falls back
    to the in-repo vendored copy, so a stale or mistyped override fails loud
    instead of silently selecting another pack."""
    for rel in ("tools/aiqt_corpus.py", "PIN.toml"):
        target = root / rel
        try:
            mode = os.lstat(target).st_mode
        except OSError as exc:
            raise ImportError(
                f"the {what} AIQT override {root} does not carry a regular {rel} "
                f"({type(exc).__name__}: {exc}). An explicit override is strict: it "
                "must name a verifiable pack root holding a regular "
                "tools/aiqt_corpus.py and a regular PIN.toml, and it never falls "
                "back to discovery or to the in-repo vendored copy "
                "(RBQ33-c3-explicit-root-fallback)."
            ) from exc
        if not stat.S_ISREG(mode):
            raise ImportError(
                f"the {what} AIQT override {root} carries {rel} as a non-regular "
                "file. An explicit override is strict: it must name a verifiable "
                "pack root holding a regular tools/aiqt_corpus.py and a regular "
                "PIN.toml, and it never falls back to discovery or to the in-repo "
                "vendored copy (RBQ33-c3-explicit-root-fallback)."
            )


_REPO_PIN_PATH_REFUSAL = (
    "the repository pin record cannot be trusted: a component of "
    "<repo>/.claude/aiqt/PIN.toml is missing, is a symlink, or is not the "
    "expected type (checked without following links), so no AIQT override "
    "can be admitted against it (RBQ14-repo-pin-symlinked-vendor). Restore "
    ".claude/aiqt as a plain directory carrying a regular PIN.toml."
)


def _repository_pin_path(repo_root: Path) -> Path:
    """The repository's committed pin record path, admitted only through
    expected, link-free components: the repository root, ``.claude`` and
    ``.claude/aiqt`` must be real directories and ``PIN.toml`` a regular
    file, each checked with a non-following lstat BEFORE the record is read
    (RBQ14-repo-pin-symlinked-vendor). Any symlink, wrong type, or
    uncheckable component refuses with the same fixed text (fail closed):
    otherwise a symlinked ``.claude/aiqt`` would let an override supply both
    the candidate pack and the repository trust anchor it is compared
    against."""
    pin_path = repo_root / ".claude" / "aiqt" / "PIN.toml"
    checks = ((repo_root, stat.S_ISDIR),
              (repo_root / ".claude", stat.S_ISDIR),
              (repo_root / ".claude" / "aiqt", stat.S_ISDIR),
              (pin_path, stat.S_ISREG))
    for component, expected_type in checks:
        try:
            mode = os.lstat(component).st_mode
        except OSError as exc:
            raise ImportError(_REPO_PIN_PATH_REFUSAL) from exc
        if stat.S_ISLNK(mode) or not expected_type(mode):
            raise ImportError(_REPO_PIN_PATH_REFUSAL)
    return pin_path


def _pinned_to_repository(pack_root: Path, pack_pin: str, what: str) -> Path:
    """Refuse an override whose VERIFIED release root is not THIS repository's
    committed pin (RBQ11-override-not-pinned): a pack that is merely
    self-consistent carries no authority here. ``pack_pin`` is the release
    root verify_vendor_dir() already validated for ``pack_root``; the
    override's own PIN.toml is deliberately NOT re-read here, so a pin record
    swapped in after verification cannot change the compared value
    (RBQ14-pin-reread-race). The repository pin itself is read only through
    link-free, expected-type path components
    (RBQ14-repo-pin-symlinked-vendor). A missing or unreadable repository pin
    record refuses every override (fail closed)."""
    rules = _load_verifier()
    here = Path(__file__).resolve()
    pin_path = (_repository_pin_path(here.parents[4])
                if len(here.parents) > 4 else None)
    try:
        if pin_path is None:
            raise ValueError("this shim has no repository root above it")
        repository_root = rules._load_pin_file(pin_path)["source"]["release-root"]
    except Exception as exc:
        raise ImportError(
            f"the {what} AIQT copy at {pack_root} is refused: the repository pin record "
            f"({pin_path}) is missing or unreadable ({type(exc).__name__}: {exc}), so no "
            "override can be admitted against it. Restore .claude/aiqt/PIN.toml."
        ) from exc
    if pack_pin != repository_root:
        raise ImportError(
            f"the {what} AIQT copy at {pack_root} verifies against its own pin, but its "
            f"release root {pack_pin} is not the repository's pinned release root "
            f"{repository_root} (.claude/aiqt/PIN.toml); refusing a self-consistent but "
            "unpinned pack."
        )
    return pack_root


def _pack_tools_entry(entry: str) -> bool:
    """SECOND-layer path hygiene; the name guard on ``sys.meta_path`` is
    the guarantee for ``aiqt_corpus`` itself (it never consults
    ``sys.path`` for the name). True when a ``sys.path`` entry REACHES a
    pack ``tools/`` directory by its RESOLVED path:
    ``os.path.realpath(entry)`` is a directory named ``tools`` with an
    ``aiqt_corpus.py`` beside it and a pack marker -- ``PIN.toml`` or
    ``.aiqt`` -- in its parent. Deciding on the RESOLVED path, never on the
    entry's spelling, also matches an entry that reaches the pack through a
    symlink of ANY name -- an aliased directory, a link named ``tools`` in
    a markerless parent, or a chain of links (RBQ34-c3-symlink-alias). The
    match decides ONCE, at scrub time, on the ENTRY alone, so it
    deliberately claims no more than that: it cannot see an entry whose
    target changes afterwards (a symlink retargeted, a path created or
    renamed into place, or a relative entry re-resolved after a chdir:
    RBQ38-c3-scrub-toctou), a plain directory holding a symlink named
    ``aiqt_corpus.py`` to the pack's file (only the entry is resolved,
    never the files under it: RBQ38-c3-file-symlink-alias), a bind mount,
    or a hard-linked copy; for the name ``aiqt_corpus`` every one of those
    is closed by the name guard, not here (see REMAINING in the module
    docstring). An entry that is not a ``str`` -- bytes, an int, or any
    other object put on ``sys.path`` -- is reported unmatched too, never a
    ``TypeError``: the import system's own ``PathFinder`` skips such
    entries, and so do this scrub and the masquerade scan
    (RBQ40-c3-nonstr-path-typeerror). An entry the filesystem refuses to
    inspect -- an ``OSError``, or a ``ValueError`` such as an embedded NUL
    byte (RBQ38-c3-realpath-valueerror) -- is reported unmatched instead
    of raising out of the scrub. The empty entry is resolved against the
    current working directory, exactly like ``.``, and matched by the
    same rule (RBQ48-c3-empty-entry-route)."""
    if not isinstance(entry, str):
        # Skipped exactly as PathFinder skips it; never a TypeError out of
        # the scrub (RBQ40-c3-nonstr-path-typeerror).
        return False
    try:
        base = Path(os.path.realpath(entry))
        return (base.name == "tools"
                and (base / "aiqt_corpus.py").is_file()
                and ((base.parent / "PIN.toml").is_file()
                     or (base.parent / ".aiqt").exists()))
    except (OSError, ValueError):
        return False


def _is_pack_root(base: Path) -> bool:
    """True when ``base`` is laid out as a pack ROOT: a
    ``tools/aiqt_corpus.py`` file below it and a pack marker --
    ``PIN.toml`` or ``.aiqt`` -- beside that ``tools/`` directory. A
    filesystem refusal reports False: the caller treats an uninspectable
    candidate as not a pack root, and for the bare name the
    ``sys.meta_path`` guard holds regardless."""
    try:
        return ((base / "tools" / "aiqt_corpus.py").is_file()
                and ((base / "PIN.toml").is_file()
                     or (base / ".aiqt").exists()))
    except OSError:
        return False


def _pack_dotted_entry(entry) -> bool:
    """SECOND-layer, BEST-EFFORT path hygiene for the DOTTED routes
    (RBQ43-c3-repo-root-premise): True when a ``sys.path`` entry's
    RESOLVED path (``os.path.realpath``) is a pack ROOT, or is the PARENT
    of a pack root (an immediate child directory is a pack root). Those
    are the one- and two-component dotted routes to the pack file
    (``import tools.aiqt_corpus`` through a pack-root entry,
    ``import aiqt.tools.aiqt_corpus`` through a pack-root-parent entry
    such as ``.claude``), the entry shapes RECOGNISED here; they are not
    the whole class of dotted routes, which the module docstring's
    REMAINING section discloses without claiming a complete list. The
    empty entry is resolved against the current working directory,
    exactly like ``.``, and matched by the same rule, so a working
    directory at a pack root or at a pack root's parent does not keep
    the empty entry alive as a dotted route
    (RBQ48-c3-empty-entry-route). Established by execution: the
    repository root is
    NOT such a route for the in-repo pack, because ``.claude`` is not a
    Python identifier, so a repository-root entry is never matched here
    (it is a pack root's GRANDPARENT and carries no dotted route of its
    own) and
    stays on ``sys.path``; nothing in this tree puts a pack root or a
    pack root's parent on ``sys.path`` (searched: the tree's own
    insertions are tool directories and the skill root), so removing the
    matched entries breaks nothing the tree relies on. Like
    ``_pack_tools_entry`` this decides ONCE, at scrub time, on the
    resolved entry and the directories below it at that moment; a
    non-``str`` entry and an entry the filesystem
    refuses to inspect are reported unmatched, never an exception out of
    the scrub. Routes this does not recognise are disclosed under
    REMAINING in the module docstring -- among them an identifier-named
    ancestor entry two or more levels above an OVERRIDE pack root and a
    plain entry holding a symlink to a pack directory at any depth
    (RBQ48-c3-symlink-dotted-route) -- and that disclosure is a class
    with examples, never a complete enumeration."""
    if not isinstance(entry, str):
        return False
    try:
        base = Path(os.path.realpath(entry))
        if _is_pack_root(base):
            return True
        with os.scandir(base) as children:
            for child in children:
                try:
                    if child.is_dir() and _is_pack_root(Path(child.path)):
                        return True
                except OSError:
                    continue
        return False
    except (OSError, ValueError):
        return False


def _scrub_pack_tools_entries() -> None:
    """SECOND, BEST-EFFORT layer: remove every ``sys.path`` entry that
    RESOLVES to a
    pack ``tools/`` directory (``_pack_tools_entry``: a literal entry or a
    symlinked alias of any name, RBQ34-c3-symlink-alias), to a pack ROOT,
    or to a pack root's PARENT (``_pack_dotted_entry``, with the empty
    entry resolved against the current working directory exactly like
    ``.``: RBQ43-c3-repo-root-premise, RBQ48-c3-empty-entry-route) at
    the START
    of bootstrap, BEFORE any discovery or verification
    (RBQ33-c3-stale-path-race). For the bare name ``aiqt_corpus`` the
    guarantee is the ``sys.meta_path`` name guard, which never consults
    ``sys.path``; this scrub removes the entry shapes it RECOGNISES and
    claims NO more (RBQ28-c3-tools-on-path): the repository root carries
    no dotted route of its own to the in-repo pack (``.claude`` is not a
    Python
    identifier) and is kept, and the pack file stays importable under a
    dotted name through any route the scrub does not recognise -- among
    them an identifier-named ancestor entry two or more
    levels above an OVERRIDE pack root and a plain entry holding a
    symlink to a pack directory at any depth
    (RBQ40-c3-dotted-name-residual, RBQ48-c3-symlink-dotted-route); the
    module docstring's REMAINING section discloses the class without
    claiming a complete list. The global import lock is held only
    across
    this list surgery -- no module code runs under it -- so an import that
    is already waiting resolves against the scrubbed path."""
    _imp.acquire_lock()
    try:
        sys.path[:] = [entry for entry in sys.path
                       if not (_pack_tools_entry(entry)
                               or _pack_dotted_entry(entry))]
    finally:
        _imp.release_lock()


def find_pack_tools() -> Path | None:
    """Return the vendored AIQT ``tools/`` directory, or ``None`` if not found.
    Every returned copy has been verified against its own pin record and
    manifest. A set, non-empty override is STRICT: it must carry a regular
    ``tools/aiqt_corpus.py`` and a regular ``PIN.toml``, be link-free,
    verify, and carry the repository's own pinned release root, or this
    raises ImportError with NO fallback to discovery or the in-repo copy
    (RBQ33-c3-explicit-root-fallback). An in-repo copy that carries the pack
    shape but does not verify raises ImportError instead of being skipped.
    The captured verified bytes are assigned to
    ``_verified_corpus_source`` HERE, only after the selected copy is
    ADMITTED -- for an override, only after ``_pinned_to_repository``
    -- never inside ``_verified()``, so a refused pack's bytes never
    become the reference (RBQ57-c3-refused-override-bytes)."""
    global _verified_corpus_source
    # 1. explicit override: AIQT_PACK_ROOT is the AIQT-standard name; GRC_AIQT_PACK
    #    is accepted too. A set, non-empty variable is strict: the named root must
    #    be link-free, carry a regular tools/aiqt_corpus.py and a regular PIN.toml,
    #    verify, and match the repository pin, or ImportError is raised -- never a
    #    fall-through (RBQ33-c3-explicit-root-fallback). The path is normalized
    #    textually (os.path.abspath touches no filesystem link) and never
    #    resolve()d.
    for var in ("AIQT_PACK_ROOT", "GRC_AIQT_PACK"):
        env = os.environ.get(var)
        if env:
            root = Path(os.path.abspath(Path(env).expanduser()))
            _refuse_symlinked_override(root, var)
            _require_pack_shape(root, var)
            verified_root, release_root, data = _verified(
                root, f"{var} override")
            admitted = _pinned_to_repository(verified_root, release_root,
                                             f"{var} override")
            # Only an ADMITTED override's bytes become the reference: a
            # refused self-consistent pack's bytes must never replace
            # the bytes an earlier run verified, or the failure handler
            # would validate that run's marked module against the
            # refused digest, treat it as unmarked and remove it
            # (RBQ57-c3-refused-override-bytes).
            _verified_corpus_source = data
            return admitted / "tools"

    here = Path(__file__).resolve()

    # 2. the in-repo vendored location <repo>/.claude/aiqt/: the digest-verified
    #    copy CI and dev both use. Discovery STOPS at the repository root: there
    #    is deliberately no walk-up above it (an ancestor copy is outside this
    #    checkout and cannot be held to this checkout's pin).
    if len(here.parents) > 4:
        vendored = here.parents[4] / ".claude" / "aiqt"
        if _has_module(vendored):
            pack_root, _release_root, data = _verified(
                vendored, "in-repo vendored")
            _verified_corpus_source = data
            return pack_root / "tools"
    return None


def _accept_installed(module, expected: Path, when: str) -> None:
    """Accept an ``aiqt_corpus`` in ``sys.modules`` only when BOTH hold
    (refuse with ImportError otherwise):

    - it carries the installation marker the verified-source loader set, and
      the marker equals the digest of the bytes the CURRENT verification
      captured -- so it was installed from captured verified bytes, by this
      bootstrap or by another instance of this same shim that verified the
      same bytes; a module that reached ``sys.modules`` any other way is
      refused whatever its origin, because an origin can be worn by a module
      imported from the on-disk file (RBQ33-c3-stale-path-race); and
    - its origin resolves to the located copy's ``tools/aiqt_corpus.py``.
    """
    source = _verified_corpus_source
    marker = _module_marker(module)
    if source is None or marker != hashlib.sha256(source).hexdigest():
        raise ImportError(
            f"the aiqt_corpus in sys.modules {when} does not carry this "
            "bootstrap's installation marker for the verified bytes: it was not "
            "installed from the captured verified bytes, and a module is never "
            "accepted by its origin alone (RBQ33-c3-stale-path-race). Remove it, "
            "or let this shim install the module."
        )
    spec = getattr(module, "__spec__", None)
    origin = getattr(spec, "origin", None) or getattr(module, "__file__", None)
    if origin is None or Path(origin).resolve() != expected:
        raise ImportError(
            f"the aiqt_corpus in sys.modules {when} resolves to {origin!r}, not "
            f"the located copy's {str(expected)!r}: an aiqt_corpus from outside "
            "the located verified pack is never accepted. Remove it, or point "
            "AIQT_PACK_ROOT (or GRC_AIQT_PACK) at the copy that provides it."
        )


def _marked_for_verified_bytes(module) -> bool:
    """True when ``module`` carries the installation marker
    (``_INSTALL_MARKER_ATTR``) for the verified bytes: the marker equals
    the SHA-256 digest of the bytes the current verification captured, so
    the module was installed from captured verified bytes by this shim
    (or by another run of it that verified the same bytes). The FAILURE
    path never removes or unpublishes such a module, whichever run
    published it (RBQ51-c3-handler-unpublishes-verified). When NO
    bytes have been captured (``_verified_corpus_source`` is ``None``, a
    failure before any verification in this shim instance), the marker
    cannot be validated against bytes: a module that carries ANY marker
    is then still treated as marked, because removing it could remove a
    module ANOTHER shim instance verified and published
    (RBQ51-c3-handler-unpublishes-verified). DISCLOSED
    (RBQ57-c3-self-marked-planted): this no-bytes corner keeps MORE
    than verified modules. The marker is an ordinary module attribute,
    so a planted on-disk ``aiqt_corpus.py`` imported through
    ``sys.path`` BEFORE the guard existed can SET the marker in its
    own body; such a SELF-MARKED module survives a failure in this
    corner, and a later plain ``import aiqt_corpus`` is served that
    module straight from ``sys.modules`` with NO acceptance check,
    until a bootstrap run that captured bytes refuses and removes it.
    Forging the marker -- in a planted file's body or by any other
    code in this process -- is disclosed as outside this shim's threat
    model; the failure path still removes every UNMARKED impostor. A
    missing or non-mapping ``__dict__`` is unmarked
    (RBQ57-c3-no-dict-module); an entry whose namespace cannot be read
    or whose marker lookup raises an ``Exception`` is unmarked
    (RBQ58-c3-dict-descriptor-raises); a ``__dict__`` descriptor
    raising a ``BaseException`` subclass still crashes the read and
    the entry survives, a disclosed residual of the same in-process
    forgery class as RBQ57/RBQ58
    (RBQ59-c3-baseexception-descriptor-wording); ``None`` is
    unmarked."""
    if module is None:
        return False
    marker = _module_marker(module)
    if marker is None:
        return False
    source = _verified_corpus_source
    if source is None:
        return True
    return marker == hashlib.sha256(source).hexdigest()


def _remove_refused_module(refused) -> None:
    """Remove a refused ``aiqt_corpus`` from ``sys.modules`` under the
    import lock, only when the name still binds that SAME object, and take
    back a guard publication of that same object, so a later import of the
    name fails closed through the unpublished guard instead of returning
    the refused module. EVERY path that refuses an ``aiqt_corpus`` found
    in ``sys.modules`` -- the pre-bootstrap acceptance check, the
    mid-install marker check, and the after-installation re-check -- and
    a bootstrap failure of ANY exception type, not only ``ImportError``
    (RBQ53-c3-non-importerror-failure), after an UNMARKED pre-existing
    module was seen go through
    this ONE helper before the error propagates
    (RBQ43-c3-prebootstrap-module-stays, RBQ48-c3-other-refusal-paths).
    Both checks are OBJECT IDENTITY (``is``) against the refused object:
    a DIFFERENT module object another thread swapped in or published
    meanwhile is left alone, but identity alone cannot tell a refusal
    from a racing acceptance or publication of the SAME object, so a
    caller must pass only a module it actually refused -- or, on the
    failure path, an UNMARKED pre-existing module -- never a marked,
    verified module (RBQ53-c3-left-alone-wording,
    RBQ51-c3-handler-unpublishes-verified). ``None`` is a no-op."""
    if refused is None:
        return
    _imp.acquire_lock()
    try:
        if sys.modules.get("aiqt_corpus") is refused:
            del sys.modules["aiqt_corpus"]
        if _NAME_GUARD._module is refused:
            _NAME_GUARD.retract()
    finally:
        _imp.release_lock()


def ensure_on_path() -> Path:
    """Verify the vendored AIQT copy, install its ``aiqt_corpus`` module in
    ``sys.modules`` from the captured verified bytes, and return the verified
    ``tools/`` directory. The name is historical: the shim no longer puts
    anything on ``sys.path``.

    At the START -- before any discovery or verification -- a name guard
    is installed at the FRONT of ``sys.meta_path`` that OWNS the name
    ``aiqt_corpus`` and never consults ``sys.path`` for it: until the
    verified module is published, every import of the name fails closed
    with ``ModuleNotFoundError``, whatever ``sys.path`` holds -- a literal
    pack entry, a symlinked alias, a symlink retargeted AFTER the scrub, a
    relative entry re-resolved after a chdir, or a plain directory holding
    a symlink named ``aiqt_corpus.py`` (RBQ38-c3-scrub-toctou,
    RBQ38-c3-file-symlink-alias) -- and once published the guard serves
    ONLY the published verified module. The guard covers the bare name
    ``aiqt_corpus`` only, from the first time it is installed; an import
    made before then resolves through ``sys.path`` and the module it left
    behind is refused by the installation-marker check. EVERY refusal of
    an ``aiqt_corpus`` found in ``sys.modules`` -- before this bootstrap
    ran, during installation, or at the after-installation re-check --
    and a bootstrap failure of ANY exception type, not only
    ``ImportError`` (RBQ53-c3-non-importerror-failure), after an
    UNMARKED pre-existing module was seen REMOVE
    the refused or unmarked module from ``sys.modules`` through ONE
    shared helper,
    under the import lock (when the name still binds the same object),
    before the error propagates, so the name then
    fails closed for the rest of the process
    (RBQ43-c3-prebootstrap-module-stays,
    RBQ48-c3-other-refusal-paths); a module that carries the
    installation marker for the verified bytes is never removed or
    unpublished by another run's failure, whether this run, an earlier
    run, or a racing run published it
    (RBQ51-c3-handler-unpublishes-verified,
    RBQ53-c3-left-alone-wording); the same pack
    file imported under a DOTTED or other name is outside the guard
    (RBQ40-c3-dotted-name-residual). Every bootstrap run re-fronts the
    guard with ONE atomic slice assignment of ``sys.meta_path`` that puts
    the guard first and drops duplicate and stale tagged guards, so a
    finder placed in front of it between runs is displaced on the next
    run (RBQ40-c3-guard-not-refronted) and the guard is never absent from
    ``sys.meta_path`` for any instant of the re-front
    (RBQ43-c3-refront-race). As a SECOND, BEST-EFFORT layer, every
    ``sys.path``
    entry whose RESOLVED path is a pack ``tools/`` directory (spelled
    literally or through a symlink of any name: RBQ34-c3-symlink-alias),
    a pack ROOT, or a pack root's PARENT is removed when the scrub
    recognises that shape (the empty entry resolves against the current
    working directory, exactly like ``.``: RBQ43-c3-repo-root-premise,
    RBQ48-c3-empty-entry-route), and no pack
    directory is ever placed on ``sys.path``
    (RBQ27-c3-concurrent-import, RBQ28-c3-tools-on-path,
    RBQ33-c3-stale-path-race); the repository root carries NO dotted
    route of its own to the in-repo pack (``.claude`` is not a Python
    identifier)
    and is kept; what remains outside the guard -- the CLASS of dotted
    routes the scrub does not recognise (among them a plain entry
    holding a symlink to a pack directory at any depth:
    RBQ48-c3-symlink-dotted-route, RBQ40-c3-dotted-name-residual), a
    load BY PATH, removal of the guard -- is
    disclosed in the module docstring's REMAINING section, as examples
    and never a complete list. A ``sys.path`` entry that is not a
    ``str`` is SKIPPED by the scrub and by the masquerade scan, exactly as
    the import system skips it, and never raises ``TypeError``
    (RBQ40-c3-nonstr-path-typeerror). Bytecode writing is additionally
    disabled for this process, so nothing can write ``__pycache__`` inside
    the digest-pinned vendor tree.

    Raises ``ImportError`` (with the fix) if the vendored copy cannot be
    located or does not verify (an explicit override is strict and never
    falls back); if an ``aiqt_corpus`` already in ``sys.modules`` does not
    carry this bootstrap's installation marker for the verified bytes with
    an origin at the located copy -- presence, origin, or both are never
    enough (RBQ33-c3-stale-path-race); or if an importable ``aiqt_corpus``
    exists anywhere on ``sys.path`` (an installed copy in site-packages or a
    planted file), which could masquerade as the vendored module for tooling
    that inspects the import system -- that scan reads ``sys.path`` directly
    through ``importlib.machinery.PathFinder``, bypassing the name guard,
    and an entry the scan cannot inspect (one with an embedded NUL byte,
    for example) refuses with ``ImportError`` too, never a raw
    ``ValueError`` (RBQ38-c3-realpath-valueerror).

    When ``aiqt_corpus`` is not already installed, the captured verified
    bytes are executed into a fresh unpublished module with NO import lock
    held (a concurrent import fails closed with ``ModuleNotFoundError``
    instead of deadlocking or seeing a partial module:
    RBQ33-c3-import-lock-deadlock), the module is published under the global
    import lock held only for the ``sys.modules`` insert, and the installed
    module's marker and origin are then RE-CHECKED before this returns
    (RBQ33-c3-origin-recheck-comment), so the consumer's
    ``import aiqt_corpus`` never re-reads the module file after verification
    (RBQ26-c3-module-swap-race).
    """
    # FIRST, before any discovery or verification: own the module name.
    # The guard refuses every import of aiqt_corpus until the verified
    # module is published, whatever sys.path holds (RBQ38-c3-scrub-toctou,
    # RBQ38-c3-file-symlink-alias).
    _install_name_guard()
    # The vendor tree must stay byte-identical to its manifest (gate 98):
    # nothing may create tools/__pycache__ inside it.
    sys.dont_write_bytecode = True
    # An UNMARKED pre-existing aiqt_corpus seen now must not stay
    # importable when this bootstrap FAILS for any reason, before (or
    # at) the acceptance check: the failure handler at the bottom
    # removes it through the one shared helper, whatever the exception
    # type (RBQ48-c3-other-refusal-paths,
    # RBQ53-c3-non-importerror-failure).
    preexisting = sys.modules.get("aiqt_corpus")
    try:
        # SECOND layer, before discovery or verification: no sys.path
        # entry the scrub recognises may reach a pack
        # (RBQ33-c3-stale-path-race).
        _scrub_pack_tools_entries()
        tools = find_pack_tools()
        if tools is None:
            raise ImportError(
                "vendored AIQT copy not found: no AIQT_PACK_ROOT or GRC_AIQT_PACK "
                "override is set (a set override is strict and never falls through "
                "to this message) and the in-repo .claude/aiqt/ carries no "
                "tools/aiqt_corpus.py plus `.aiqt` entry or PIN.toml (discovery "
                "stops at the repository root). Set AIQT_PACK_ROOT (or "
                "GRC_AIQT_PACK) to a verifiable copy's root, or restore the "
                "vendored .claude/aiqt/."
            )
        # Belt and braces: the scrub above already removed pack tools/
        # entries, but the located copy's own entry is removed again by
        # exact string too.
        p = str(tools)
        _imp.acquire_lock()
        try:
            while p in sys.path:
                sys.path.remove(p)
        finally:
            _imp.release_lock()
        expected = (tools / "aiqt_corpus.py").resolve()
        existing = sys.modules.get("aiqt_corpus")
        if existing is not None:
            try:
                _accept_installed(existing, expected,
                                  "before this bootstrap ran")
            except ImportError:
                # The refused module must not stay importable: the one
                # shared helper removes it from sys.modules under the
                # import lock, only when the name still binds the SAME
                # object, so a later import of the name in this process
                # fails closed through the unpublished guard instead of
                # returning the unmarked module
                # (RBQ43-c3-prebootstrap-module-stays,
                # RBQ48-c3-other-refusal-paths).
                _remove_refused_module(existing)
                raise
            _NAME_GUARD.publish(existing)
            return tools
        # The masquerade scan reads sys.path DIRECTLY (PathFinder),
        # bypassing the name guard, which would otherwise refuse this very
        # inspection.
        try:
            spec = importlib.machinery.PathFinder.find_spec("aiqt_corpus")
        except (OSError, ValueError) as exc:
            raise ImportError(
                "sys.path cannot be scanned for a masquerading aiqt_corpus "
                f"({type(exc).__name__}: {exc}); refusing to continue with an "
                "uninspectable sys.path entry in place "
                "(RBQ38-c3-realpath-valueerror)."
            ) from exc
        if spec is not None:
            origin = spec.origin
            raise ImportError(
                f"aiqt_corpus resolves to {origin!r}, not the located copy's {str(expected)!r}: "
                "an installed or planted aiqt_corpus on sys.path could masquerade as the "
                "vendored module. Remove it, or point AIQT_PACK_ROOT (or GRC_AIQT_PACK) at "
                "the copy that provides it."
            )
        _install_verified_corpus(tools)
        # Re-check the INSTALLED module's marker and origin after
        # installation (RBQ33-c3-origin-recheck-comment): what sys.modules
        # now holds must be a module built from the captured verified
        # bytes at the located copy's path, not whatever won a publish
        # race.
        installed = sys.modules.get("aiqt_corpus")
        if installed is None:
            raise ImportError(
                "aiqt_corpus is not in sys.modules after installation; refusing to "
                "return a tools/ directory whose module is not installed "
                "(RBQ33-c3-origin-recheck-comment)."
            )
        try:
            _accept_installed(installed, expected, "after installation")
        except ImportError:
            # The after-installation re-check refuses the same way: the
            # refused module must not stay importable or stay published
            # (RBQ48-c3-other-refusal-paths).
            _remove_refused_module(installed)
            raise
        return tools
    except BaseException:
        # A bootstrap failure of ANY kind -- ImportError or any other
        # exception (RBQ53-c3-non-importerror-failure) -- after a
        # pre-existing module was seen: an UNMARKED pre-existing module
        # must not stay importable, so it is removed through the one
        # shared helper (which acts only while the name still binds that
        # same object) before the error propagates unchanged. A module
        # that carries the installation marker for the verified bytes is
        # NEVER removed or unpublished by this failure path, whoever
        # published it -- this run, an earlier successful run, or a
        # racing run that accepted and published the SAME pre-existing
        # object meanwhile: the helper's object-identity check alone
        # cannot protect the same object, so this marker check does
        # (RBQ51-c3-handler-unpublishes-verified,
        # RBQ53-c3-left-alone-wording). A DIFFERENT module object
        # swapped in meanwhile is left alone by the helper's identity
        # check (RBQ48-c3-other-refusal-paths).
        if not _marked_for_verified_bytes(preexisting):
            _remove_refused_module(preexisting)
        raise


# Module-level side effect: discovery runs on import, so a consumer's
# `import aiqt_bootstrap` is enough before `from aiqt_corpus import ...`.
ensure_on_path()
