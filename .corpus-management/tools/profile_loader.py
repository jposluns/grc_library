#!/usr/bin/env python3
"""Reference-vocabulary profile loader (Corpus-Management pack, Phase-4 PR-A).

Loads one CONCERN's reference-vocabulary profile from the pack's defaults tree
(``defaults/grc/<concern>.toml``), optionally overlaid by an adopter's own
``<adopter_dir>/<concern>.toml``. Profiles are versioned TOML: each file
carries ``schema_version = 1`` plus exactly one concern-namespaced table
(``[<concern>]``), and nothing else. The pack register ``core/profiles.toml``
lists the shipped profiles; the compiler validates both at gate-99 config time.

Overlay semantics (KEY-LEVEL REPLACE): for each top-level key of the concern
table, an adopter value replaces the default value WHOLE (no deep merge); a
key absent from the adopter file falls back to the default; an explicit empty
value (``[]``, ``""``, ``{}``) is a deliberate CLEAR, not a fallback. An
adopter key with no counterpart in the default profile is an error (a typo'd
override must never silently do nothing).

This loader is deliberately CONCERN-AGNOSTIC: it validates the profile
ENVELOPE (schema_version, exactly one concern table, no stray top-level keys)
and the overlay mechanics, and it compiles any regex table it finds, but it
does NOT know the inner schema of any one concern. Per-concern deep validation
belongs to the engine that consumes the profile (it validates the shape it
needs, when it needs it); that keeps a new concern from requiring a loader edit.

Regex values are stored as strings with an EXPLICIT case flag, as an inline
table of exactly ``{ regex = "<pattern>", ignorecase = <bool> }``; the loader
compiles each into a ``re.Pattern`` in the returned structure. Both fields are
required: an implicit case default is the kind of silent policy this loader
refuses to carry.

FAIL-CLOSED: a missing default profile, an unparseable file, a wrong
``schema_version``, an unknown top-level key, a non-table concern value, an
unknown adopter override key, a malformed regex table, or an uncompilable
regex all raise ``ProfileError`` with the offending file and location. A
broken profile is a broken setup to fix, never a state to degrade around.

No filesystem discovery is performed by gate engines: project wrappers call
``load()`` and pass the resolved values into the engine, exactly as they pass
hand-maintained config today.

Usage:
    from profile_loader import load, ProfileError
    profile = load("citations")                          # pack defaults
    profile = load("citations", adopter_dir=my_dir)      # with adopter overlay

Stdlib-only (Python 3.11 tomllib, re, pathlib).
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

# A concern name is a pack id (the compiler's RULE_ID_RE shape); anything else
# is refused before it can reach a filesystem path.
CONCERN_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

# A regex value is an inline table with EXACTLY these keys.
REGEX_TABLE_KEYS = {"regex", "ignorecase"}


class ProfileError(ValueError):
    """A profile failed validation. Callers fail loud; never fall back silently."""


def _default_defaults_dir() -> Path:
    # <pack>/tools/profile_loader.py -> parents[1] is the pack root.
    return Path(__file__).resolve().parents[1] / "defaults" / "grc"


def _read_profile(path: Path, concern: str) -> dict:
    """Parse one profile file; validate its envelope; return its concern table."""
    try:
        with open(path, "rb") as fh:
            data = tomllib.load(fh)
    except (tomllib.TOMLDecodeError, UnicodeDecodeError, OSError) as exc:
        raise ProfileError(f"{path}: cannot parse: {exc}") from exc
    sv = data.get("schema_version")
    if not isinstance(sv, int) or isinstance(sv, bool) or sv != 1:
        raise ProfileError(f"{path}: schema_version must be the integer 1")
    unknown = set(data) - {"schema_version", concern}
    if unknown:
        raise ProfileError(
            f"{path}: unknown top-level key(s): {', '.join(sorted(unknown))} "
            f"(a profile carries schema_version plus exactly one [{concern}] table)"
        )
    table = data.get(concern)
    if not isinstance(table, dict):
        raise ProfileError(
            f"{path}: missing or non-table [{concern}] table (the concern-namespaced "
            f"table is required)"
        )
    return table


def _compile_regexes(value: object, path: Path, where: str) -> object:
    """Recursively rebuild ``value``, compiling every regex table found.

    A dict carrying a ``regex`` key must be exactly ``{regex, ignorecase}``
    with the declared types; it is replaced by the compiled ``re.Pattern``.
    Every other dict/list is rebuilt (so callers own the returned structure);
    scalars pass through unchanged.
    """
    if isinstance(value, dict):
        if "regex" in value:
            if set(value) != REGEX_TABLE_KEYS:
                raise ProfileError(
                    f"{path}: {where}: a regex table must carry exactly the keys "
                    f"'regex' (string) and 'ignorecase' (bool); found: "
                    f"{', '.join(sorted(value))}"
                )
            pattern = value["regex"]
            ignorecase = value["ignorecase"]
            if not isinstance(pattern, str):
                raise ProfileError(f"{path}: {where}: 'regex' must be a string")
            if not isinstance(ignorecase, bool):
                raise ProfileError(f"{path}: {where}: 'ignorecase' must be a boolean")
            try:
                return re.compile(pattern, re.IGNORECASE if ignorecase else 0)
            except (re.error, RecursionError, OverflowError) as exc:
                raise ProfileError(
                    f"{path}: {where}: uncompilable regex {pattern!r}: "
                    f"{type(exc).__name__}: {exc}"
                ) from exc
        return {
            k: _compile_regexes(v, path, f"{where}.{k}") for k, v in value.items()
        }
    if isinstance(value, list):
        return [
            _compile_regexes(v, path, f"{where}[{i}]") for i, v in enumerate(value)
        ]
    return value


def _compile_table(table: dict, path: Path, concern: str) -> dict:
    """Compile the regex tables among a concern table's VALUES.

    The concern table itself is never passed to ``_compile_regexes``: a
    concern table whose keys happened to be exactly ``regex`` and
    ``ignorecase`` would otherwise be misread as a regex table (and crash on
    the subsequent ``dict()``). A regex table is only ever recognized as a
    VALUE, never as the concern table.
    """
    return {
        k: _compile_regexes(v, path, f"[{concern}].{k}") for k, v in table.items()
    }


def load(
    concern: str,
    *,
    adopter_dir: str | Path | None = None,
    defaults_dir: str | Path | None = None,
) -> dict:
    """Load the ``concern`` profile: pack default, key-level adopter overlay.

    ``defaults_dir`` overrides the pack defaults tree (the compiler's
    validation pass and the regression fixtures use it; project wrappers do
    not pass it). Returns the concern table as a plain dict, with every
    declared regex compiled to an ``re.Pattern``.
    """
    if not isinstance(concern, str) or not CONCERN_RE.match(concern):
        raise ProfileError(
            f"concern name {concern!r} must match ^[a-z0-9][a-z0-9-]*$"
        )
    droot = Path(defaults_dir) if defaults_dir is not None else _default_defaults_dir()
    dpath = droot / f"{concern}.toml"
    if not dpath.is_file():
        raise ProfileError(
            f"{dpath}: no default profile for concern {concern!r} (a missing "
            f"default profile is a broken setup to fix, never to silently "
            f"work around)"
        )
    default_table = _compile_table(
        _read_profile(dpath, concern), dpath, concern
    )

    if adopter_dir is None:
        return dict(default_table)
    apath = Path(adopter_dir) / f"{concern}.toml"
    try:
        apath.lstat()  # does NOT follow symlinks: sees a broken symlink as present
    except FileNotFoundError:
        return dict(default_table)  # genuinely absent: fall back to the default
    if not apath.is_file():
        raise ProfileError(
            f"{apath}: adopter override exists but is not a regular file (a "
            f"directory or broken symlink is a misconfiguration to fix, never a "
            f"silent fallback to defaults)"
        )
    adopter_table = _compile_table(
        _read_profile(apath, concern), apath, concern
    )
    unknown = set(adopter_table) - set(default_table)
    if unknown:
        raise ProfileError(
            f"{apath}: unknown override key(s) with no counterpart in the "
            f"default profile: {', '.join(sorted(unknown))} (a typo'd override "
            f"must never silently do nothing)"
        )
    merged = dict(default_table)
    merged.update(adopter_table)  # key-level replace: adopter value wins whole
    return merged
