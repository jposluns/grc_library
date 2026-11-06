#!/usr/bin/env python3
"""Baseline-pin integrity audit (grc gate 110).

The website baseline template package (the shared site template; the
adopted version is the one ``.baseline/pin.toml`` records) is vendored
byte-for-byte under ``.web/baseline/``. Those copies are
verbatim third-party material: no copied file is ever edited, and an update
arrives only as a new package version that bumps the pin and the copied
files together. The pin file ``.baseline/pin.toml`` records the adopted
baseline version and the SHA-256 of every copied file, in the format the
package README's "Adoption in a repository" section defines: a top-level
``version`` string and a ``[files]`` table mapping each repository-relative
copied-file path (under ``.web/baseline/``, or one of the pinned tools
below) to its lowercase hexadecimal SHA-256.

The pin also records the package's build tools that the repository copies
outside the served tree, never served: exactly the paths in
``PINNED_TOOLS`` (the palette gate ``.baseline/check_palette.py``, which the
package's adoption step 3 pins in the same ``[files]`` table and the site
build runs; the overflow check ``.baseline/check_overflow.js``, which the
package's specification pins like the palette gate and which no gate runs;
and the package's link-preview card builder
``.baseline/build_card.js`` with its 3 Inter fonts and their licence under
``.baseline/card-fonts/``, which no build or gate runs).
Each is verified like a copied file: a regular file, not a symbolic link,
reached through real directories from ``.baseline`` down (``.baseline`` and,
for the fonts, ``.baseline/card-fonts``), whose SHA-256 matches its pin entry; a
pinned tool that is missing, a tool present with no pin entry, and a pin with
no entry for a ``PINNED_TOOLS`` path (the pin must include every one, file or
no file) are findings.

This gate recomputes the SHA-256 of every file under ``.web/baseline/`` and
of every pinned tool, and compares them with the pin. It fails on:

- a hash mismatch (a copied file whose bytes drifted from the pin);
- a pin entry without a file (a pinned path missing from the tree, or
  present but refused as a non-regular file, below);
- a file without a pin entry (an unlisted file inside the tree, a symbolic
  link included);
- a non-regular file inside the tree (a FIFO, a socket, a device, anything
  that is not a regular file and not a directory), named by path and
  decided by ``lstat`` before any open or read, so the gate never opens a
  non-regular file: an opened FIFO with no writer would block the gate,
  and one with a writer could feed it substitute bytes;
- a pin key outside ``.web/baseline/`` other than a ``PINNED_TOOLS`` path
  (the pin governs only the vendored tree and those tools; a key elsewhere
  would silently extend its authority);
- a pinned tool whose bytes drift from the pin, that is missing, that is a
  symbolic link or not a regular file, or whose ``.baseline`` directory (or
  ``.baseline/card-fonts`` directory) is a symbolic link or not a real
  directory; a tool present with no pin entry;
  and a ``PINNED_TOOLS`` path with no pin entry and no file;
- a refused tree shape, found before traversal starts and named by path:
  a ``.web`` or ``.web/baseline`` entry that is a symbolic link or not a
  real directory (a link could alias the pinned bytes from elsewhere);
- a missing or malformed pin (no ``.baseline/pin.toml``, TOML that
  ``tomllib`` refuses, a missing or non-string ``version``, a missing or
  non-table ``[files]``, or a value that is not a 64-character lowercase
  hexadecimal digest), reported as a prerequisite failure.

The gate is offline and deterministic: it reads only the repository's own
files, makes no network request, and runs on stdlib Python 3.11 alone
(``tomllib``, ``hashlib``). The ``--root`` argument overrides the
repository root the gate reads the pin and the tree from; it exists for the
gate-36 regression tests, which point it at a synthetic tree with an
engineered regression. The default is the repository root derived from this
file's location.

Exit codes:

    0   the tree and the pin agree.
    1   one or more findings (mismatch, unpinned file, missing file, a
        non-regular file inside the tree, a key outside the vendored
        tree, a pinned-tool fault, or a refused tree shape: a symlinked or
        non-directory ``.web`` or ``.web/baseline``).
    2   prerequisite failure: the pin is missing or malformed, the named
        root is not a directory, or a listed file cannot be read.
"""

from __future__ import annotations

import argparse
import hashlib
import stat
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PIN_REL = ".baseline/pin.toml"
TREE_REL = ".web/baseline"
TREE_PREFIX = TREE_REL + "/"
HEX_DIGITS = frozenset("0123456789abcdef")
# The package's build tools pinned outside the served tree (the palette gate,
# copied from the package's tools/check_palette.py, and the overflow check,
# copied from its tools/check_overflow.js). Fixed paths: a new tool is a
# reviewed edit here, never a pin key alone.
PINNED_TOOLS = frozenset({".baseline/check_palette.py",
                          ".baseline/check_overflow.js",
                          # Baseline 1.10.0 (SPECIFICATION.md section 7.35):
                          # the link-preview card builder, copied from the
                          # package's tools/build_card.js, and its 3 Inter
                          # fonts with their SIL OFL licence, copied from
                          # tools/card-fonts/. Never served: the builder runs
                          # only on a review machine, never in the build.
                          ".baseline/build_card.js",
                          ".baseline/card-fonts/Inter-Bold.otf",
                          ".baseline/card-fonts/Inter-ExtraBold.otf",
                          ".baseline/card-fonts/Inter-Regular.otf",
                          ".baseline/card-fonts/inter-LICENSE.txt"})


class PinError(Exception):
    """A missing or malformed pin, or an unusable root: a prerequisite
    failure (exit 2), never a finding (exit 1)."""


def load_pin(root: Path) -> tuple[str, dict[str, str]]:
    """Return ``(version, files)`` from ``<root>/.baseline/pin.toml``.

    Raises :class:`PinError` for a missing pin, TOML that ``tomllib``
    refuses, a missing or non-string ``version``, a missing or non-table
    ``[files]``, or a digest value that is not 64 lowercase hexadecimal
    characters. Key placement (inside ``.web/baseline/``) is a finding,
    not a parse error, and is checked by the caller.
    """
    pin_path = root / PIN_REL
    try:
        raw = pin_path.read_bytes()
    except FileNotFoundError:
        raise PinError(f"{PIN_REL}: missing; the vendored baseline tree must "
                       f"carry its pin") from None
    except OSError as exc:
        raise PinError(f"{PIN_REL}: cannot be read ({exc})") from None
    try:
        data = tomllib.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise PinError(f"{PIN_REL}: malformed ({exc})") from None
    version = data.get("version")
    if not isinstance(version, str) or not version:
        raise PinError(f"{PIN_REL}: malformed (top-level 'version' must be a "
                       f"nonempty string)")
    files = data.get("files")
    if not isinstance(files, dict) or not files:
        raise PinError(f"{PIN_REL}: malformed ('[files]' must be a nonempty "
                       f"table of path to SHA-256)")
    pinned: dict[str, str] = {}
    for key, value in files.items():
        if (not isinstance(value, str) or len(value) != 64
                or not set(value) <= HEX_DIGITS):
            raise PinError(f"{PIN_REL}: malformed (the value of {key!r} must "
                           f"be a 64-character lowercase hexadecimal SHA-256)")
        pinned[key] = value
    return version, pinned


def tree_shape_findings(root: Path) -> list[str]:
    """Pre-traversal shape findings for the vendored tree (exit 1).

    The vendored tree must be reached through real directories: a symbolic
    link at ``.web`` or ``.web/baseline`` (or a non-directory entry there)
    could alias the pinned bytes from elsewhere, so traversal is refused
    before it starts, naming the path. An absent entry is not a shape
    finding; the pin comparison then reports every validly keyed pin
    entry as a missing file.
    """
    for rel in (".web", TREE_REL):
        path = root / rel
        if path.is_symlink():
            return [f"{rel}: symbolic link in place of a real directory; "
                    f"the vendored tree must be reached through real "
                    f"directories inside the repository"]
        if not path.exists():
            return []
        if not path.is_dir():
            return [f"{rel}: present but not a real directory"]
    # The round-5 "resolves outside the repository root" refusal was removed
    # as unreachable (round 2 NOTE 3): the tree path is the fixed relative
    # ".web/baseline" with no ".." component, and the loop above has just
    # established that both components are real directories and not symbolic
    # links, so resolving the tree appends those two components to the
    # resolved root and can never land outside it.
    return []


def discover_tree(root: Path) -> tuple[dict[str, Path], list[str]]:
    """Return ``(files, findings)`` for the tree under ``<root>/.web/baseline``.

    ``files`` maps each regular file's repository-relative POSIX path to its
    on-disk path. Every entry is classified by ``lstat`` before anything is
    opened. A symbolic link inside the tree is a finding (the vendored
    copies are plain files; a link could point outside the pinned bytes),
    and so is any other non-regular entry (a FIFO, a socket, a device): the
    gate must never open one, because an opened FIFO with no writer would
    block the hash read forever and one with a writer could feed it
    substitute bytes (round 2 finding 1).
    An absent tree returns an empty map, so every validly keyed pin entry
    then reports as a missing file (a key outside ``.web/baseline/`` is
    reported as a key problem instead). The caller refuses a symlinked or
    non-directory ``.web`` or ``.web/baseline`` through
    :func:`tree_shape_findings` before calling this, so the tree here is
    absent or a real directory.
    """
    tree = root / TREE_REL
    if not tree.is_dir():
        return {}, []
    files: dict[str, Path] = {}
    findings: list[str] = []
    for path in sorted(tree.rglob("*")):
        rel = TREE_PREFIX + path.relative_to(tree).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            findings.append(f"{rel}: symbolic link inside the vendored tree; "
                            f"only pinned regular files belong here")
            continue
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            findings.append(f"{rel}: not a regular file (refused by lstat, "
                            f"never opened); only pinned regular files "
                            f"belong under {TREE_REL}/")
            continue
        files[rel] = path
    return files, findings


def tool_findings(root: Path, pinned: dict[str, str]) -> list[str]:
    """Findings for the pinned build tools (``PINNED_TOOLS``).

    Each tool is classified by ``lstat`` before anything is opened, as in
    the vendored tree: a pinned tool must be a regular file reached through
    real directories from ``.baseline`` down (a symbolic link could alias
    other bytes) whose
    SHA-256 matches its pin entry. A tool present with no pin entry is a
    finding too, so the build never runs an unpinned copy, and so is a pin
    with no entry for a tool even when the file is absent too: the pin must
    include every ``PINNED_TOOLS`` path, so the gate never skips one
    silently.
    """
    findings: list[str] = []
    for rel in sorted(PINNED_TOOLS):
        path = root / rel
        if rel not in pinned:
            if path.is_symlink() or path.exists():
                findings.append(f"{rel}: present with no entry in {PIN_REL} "
                                f"(file without a pin entry)")
            else:
                findings.append(f"{rel}: no entry in {PIN_REL} and no file; "
                                f"the pin must include every pinned tool "
                                f"(pinned tool without a pin entry)")
            continue
        # Every directory from .baseline down to the tool must be real: the
        # card fonts sit one level deeper, in .baseline/card-fonts/, and a
        # symbolic link there could alias other bytes as one at .baseline
        # could. The first faulty directory is named, so each tool yields one
        # finding.
        bad_dir = None
        for depth in range(1, len(Path(rel).parts)):
            dir_rel = "/".join(Path(rel).parts[:depth])
            dir_path = root / dir_rel
            if dir_path.is_symlink() or not dir_path.is_dir():
                bad_dir = dir_rel
                break
        if bad_dir is not None:
            findings.append(f"{bad_dir}: symbolic link or not a real "
                            f"directory; a pinned tool must be reached "
                            f"through a real directory")
            continue
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError:
            findings.append(f"{rel}: pinned in {PIN_REL} but missing (pin "
                            f"entry without a file)")
            continue
        if stat.S_ISLNK(mode):
            findings.append(f"{rel}: symbolic link in place of a pinned tool; "
                            f"only a pinned regular file belongs here")
            continue
        if not stat.S_ISREG(mode):
            findings.append(f"{rel}: not a regular file (refused by lstat, "
                            f"never opened)")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != pinned[rel]:
            findings.append(f"{rel}: SHA-256 {digest} does not match the "
                            f"pinned {pinned[rel]}; a copied tool is never "
                            f"edited: restore the pinned bytes or adopt a "
                            f"new baseline version by bumping the pin and "
                            f"the copies together")
    return findings


def key_problem(key: str) -> str | None:
    """Why ``key`` is not a clean path inside ``.web/baseline/``, or None."""
    if not key.startswith(TREE_PREFIX):
        return "outside .web/baseline/"
    tail = key[len(TREE_PREFIX):]
    if not tail:
        return "names the tree itself, not a file in it"
    parts = tail.split("/")
    if "\\" in key or any(part in ("", ".", "..") for part in parts):
        return "not a clean relative path"
    return None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Baseline-pin integrity audit (gate 110)."
    )
    parser.add_argument(
        "--root",
        default=str(REPO_ROOT),
        help="repository root holding .baseline/pin.toml and .web/baseline/ "
             "(default: this repository; used by the regression tests)",
    )
    args = parser.parse_args(argv[1:])
    root = Path(args.root)
    findings: list[str] = []
    try:
        if not root.is_dir():
            raise PinError(f"--root {args.root!r} is not a directory")
        version, pinned = load_pin(root)
        findings = tree_shape_findings(root)
        if not findings:
            files, findings = discover_tree(root)
            for key in sorted(pinned):
                if key in PINNED_TOOLS:
                    continue
                problem = key_problem(key)
                if problem:
                    findings.append(f"{PIN_REL}: pin key {key!r} is "
                                    f"{problem}; the pin covers only the "
                                    f"vendored tree")
                    continue
                path = files.pop(key, None)
                if path is None:
                    findings.append(f"{key}: pinned in {PIN_REL} but missing "
                                    f"from the tree (pin entry without a "
                                    f"file)")
                    continue
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if digest != pinned[key]:
                    findings.append(f"{key}: SHA-256 {digest} does not match "
                                    f"the pinned {pinned[key]} (baseline "
                                    f"{version}); a copied file is never "
                                    f"edited: restore the pinned bytes or "
                                    f"adopt a new baseline version by bumping "
                                    f"the pin and the copies together")
            for rel in sorted(files):
                findings.append(f"{rel}: present under {TREE_REL}/ with no "
                                f"pin entry (file without a pin entry)")
            findings.extend(tool_findings(root, pinned))
    except PinError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: {TREE_REL}: cannot be read ({exc})", file=sys.stderr)
        return 2
    if findings:
        for finding in findings:
            print(f"ERROR: {finding}")
        print(f"{len(findings)} baseline-pin finding(s).")
        return 1
    tools = len(PINNED_TOOLS & set(pinned))
    print(f"OK: {len(pinned) - tools} file(s) under {TREE_REL}/ and {tools} "
          f"pinned tool(s) verified against {PIN_REL} (baseline {version}).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
