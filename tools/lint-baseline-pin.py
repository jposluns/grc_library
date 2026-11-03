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
copied-file path (always under ``.web/baseline/``) to its lowercase
hexadecimal SHA-256.

This gate recomputes the SHA-256 of every file under ``.web/baseline/`` and
compares the tree with the pin. It fails on:

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
- a pin key outside ``.web/baseline/`` (the pin governs only the vendored
  tree; a key elsewhere would silently extend its authority);
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
        tree, or a refused tree shape: a symlinked or non-directory
        ``.web`` or ``.web/baseline``).
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
    print(f"OK: {len(pinned)} file(s) under {TREE_REL}/ verified against "
          f"{PIN_REL} (baseline {version}).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
