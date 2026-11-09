#!/usr/bin/env python3
"""Claude-rules local-copy sync audit (pinned AIQT bytes, exact equality).

The files under ``.claude/rules/`` are what a Claude Code session actually
loads at startup, so every one of them must have a verified owner:

1. The pinned AIQT rule set. The vendored copy under ``.claude/aiqt/`` is the
   source of truth; ``aiqt_rules.validate()`` (imported below) verifies the
   pin identity (the upstream release root digest), every vendored file's
   manifest digest, the rendered copies under ``.claude/rules/aiqt/`` and
   ``.claude/rules/security/`` (byte-identical except for the declared
   paths-scope insertion), and the generated AIQT index block in
   ``.claude/CLAUDE.md``. Any drift is a finding here.

2. The Corpus-Management compiler. The pack's compiler
   (``.claude/skills/corpus-management/tools/build-corpus-management.py``;
   gate 99) may generate rule files under ``.claude/rules/corpus-management/``.
   The completeness check recognizes those files through the pack's validated
   ownership register, never through a directory skip: a local rule file
   covered by a valid register entry (an exact file target, or inside a tree
   target) is accepted as compiler-owned, because its byte-integrity is gate
   99's stricter job. A hand-dropped stray under the reserved subdirectory
   still fails loud. Four ownership defects are findings here (defence in
   depth with the compiler's own validation): an entry that contests the
   AIQT-rendered rule tree (the pin and the compiler can never contest a
   path), an entry under ``.claude/rules/`` outside the reserved
   ``corpus-management/`` subdirectory, a block-kind entry targeting anything
   under ``.claude/rules/`` (a compiler-owned block inside a rendered rule
   body would put two owners on one file), and an index-kind entry targeting
   anything under ``.claude/rules/`` (the rule index is read when the
   corpus-management skill loads, never at session start). An absent register
   yields an empty owned set (fail-closed); an unparseable register is an
   internal error (exit 2).

3. The local-only ``external/`` overlay (third-party rule sets with no
   upstream source), excluded from the completeness check.

Any other markdown file under ``.claude/rules/`` fails the audit as unowned,
rather than going silently unchecked: forgetting to declare a new rule file is
loud, not silent.

The ``--root`` argument overrides the repository root used to resolve every
path. Used by the regression test suite to point at a synthetic minimal
source set with engineered drift.

Stdlib-only.

Exit codes:

    0   the pinned AIQT snapshot validates and every local rule file is
        covered by a verified owner.
    1   one or more findings (AIQT drift, an ownership defect, or an
        unowned local file).
    2   internal error (the Corpus-Management ownership register is
        unparseable, or an unexpected crash).
"""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path, PurePosixPath

sys.path.append(str(Path(__file__).resolve().parent))
from aiqt_rules import validate as validate_snapshot  # noqa: E402  the pinned-AIQT validation
from lint_common import require_dir  # noqa: E402  grc-config helpers, stays local

# The repository root: this file lives at
# .claude/skills/corpus-management/tools/, four levels down.
REPO_ROOT = Path(__file__).resolve().parents[4]

# Directory holding the session-start rule copies.
LOCAL_RULES_DIR_REL = ".claude/rules"

# Local-only overlay: third-party rule sets with no upstream source. These
# are excluded from the completeness check.
LOCAL_ONLY_SUBDIR = "external"

# The AIQT-rendered rule tree: owned by the pin (aiqt_rules.validate()).
# No ownership-register entry may contest it.
AIQT_RENDERED_SUBDIRS = (".claude/rules/aiqt", ".claude/rules/security")

# Compiler-owned recognition (Corpus-Management pack): the ownership register
# the pack's compiler validates (gate 99), read here schema-light so this gate
# stays import-decoupled from the compiler. The reserved subdirectory is the
# ONLY place a compiler-owned rule file may live; recognition is keyed to the
# register, never to a directory skip.
OWNERSHIP_REGISTER_REL = ".claude/skills/corpus-management/src/core/ownership.toml"
CM_RULES_SUBDIR = ".claude/rules/corpus-management"


class OwnershipRegisterError(Exception):
    """The Corpus-Management ownership register exists but cannot be read."""


def load_compiler_owned(root: Path) -> tuple[list[str], set[str], set[str]]:
    """Return ``(findings, owned_files, owned_trees)`` from the
    Corpus-Management pack's ownership register, scoped to targets under
    ``.claude/rules/``.

    An absent register yields an empty owned set (fail-closed: every file
    under the reserved subdirectory then fails as unowned). An unparseable
    or malformed register raises ``OwnershipRegisterError`` (exit 2). An
    entry that contests the AIQT-rendered rule tree, sits under
    ``.claude/rules/`` outside the reserved ``corpus-management/``
    subdirectory, or claims a block or an index inside ``.claude/rules/``
    yields a finding and contributes no coverage.
    """
    reg_path = root / OWNERSHIP_REGISTER_REL
    if not reg_path.is_file():
        return [], set(), set()
    try:
        with open(reg_path, "rb") as fh:
            register = tomllib.load(fh)
    except (tomllib.TOMLDecodeError, UnicodeDecodeError, OSError) as exc:
        raise OwnershipRegisterError(
            f"cannot read the Corpus-Management ownership register "
            f"{OWNERSHIP_REGISTER_REL}: {exc}"
        )
    _sv = register.get("schema_version")
    if not isinstance(_sv, int) or isinstance(_sv, bool) or _sv != 1:
        raise OwnershipRegisterError(
            f"{OWNERSHIP_REGISTER_REL}: 'schema_version' must be the integer 1"
        )
    if "owned_targets" not in register:
        raise OwnershipRegisterError(
            f"{OWNERSHIP_REGISTER_REL}: missing required 'owned_targets' collection"
        )
    entries = register["owned_targets"]
    if not isinstance(entries, list):
        raise OwnershipRegisterError(
            f"{OWNERSHIP_REGISTER_REL}: 'owned_targets' must be a list"
        )
    findings: list[str] = []
    owned_files: set[str] = set()
    owned_trees: set[str] = set()
    claude_rules = PurePosixPath(LOCAL_RULES_DIR_REL)
    cm_rules = PurePosixPath(CM_RULES_SUBDIR)
    aiqt_trees = tuple(PurePosixPath(sub) for sub in AIQT_RENDERED_SUBDIRS)
    for i, entry in enumerate(entries):
        if (
            not isinstance(entry, dict)
            or not isinstance(entry.get("rule"), str)
            or not isinstance(entry.get("kind"), str)
            or not isinstance(entry.get("target"), str)
        ):
            raise OwnershipRegisterError(
                f"{OWNERSHIP_REGISTER_REL}: owned_targets[{i}] must be a "
                f"table with string 'rule', 'kind', and 'target' fields"
            )
        kind = entry["kind"]
        target = entry["target"]
        if kind not in ("block", "file", "tree", "index"):
            raise OwnershipRegisterError(
                f"{OWNERSHIP_REGISTER_REL}: owned_targets[{i}] has unknown kind "
                f"{kind!r} (must be block, file, tree, or index)"
            )
        if "\x00" in target or PurePosixPath(target).is_absolute() or ".." in PurePosixPath(target).parts:
            raise OwnershipRegisterError(
                f"{OWNERSHIP_REGISTER_REL}: owned_targets[{i}] target must be a "
                f"relative, '..'-free, NUL-free path: {target!r}"
            )
        tposix = PurePosixPath(target)
        in_rules = tposix == claude_rules or claude_rules in tposix.parents
        contains_rules = kind == "tree" and (
            tposix == claude_rules or tposix in claude_rules.parents
        )
        contests_aiqt = any(
            tposix == tree or tree in tposix.parents
            or (kind == "tree" and tposix in tree.parents)
            for tree in aiqt_trees
        )
        if contests_aiqt or contains_rules:
            findings.append(
                f"ownership overlap: register entry {entry['rule']!r} "
                f"({kind} {target}) contests the AIQT-rendered rule tree, "
                f"which the pin owns; the pin and compiler outputs can "
                f"never contest a path."
            )
            continue
        if not in_rules:
            continue  # a target outside .claude/rules/ is not this gate's concern
        if kind == "block":
            findings.append(
                f"block-kind ownership entry {entry['rule']!r} targets "
                f"{target} under {LOCAL_RULES_DIR_REL}/: a compiler-owned "
                f"block inside a rendered rule body would put two owners "
                f"on one file; only file or tree kinds may own rule files."
            )
            continue
        if not (tposix == cm_rules or cm_rules in tposix.parents):
            findings.append(
                f"ownership entry {entry['rule']!r} ({kind} {target}) sits "
                f"under {LOCAL_RULES_DIR_REL}/ outside the reserved "
                f"{CM_RULES_SUBDIR}/ subdirectory."
            )
            continue
        if kind == "index":
            findings.append(
                f"index-kind ownership entry {entry['rule']!r} targets "
                f"{target} under {LOCAL_RULES_DIR_REL}/: the rule index ships "
                f"in the corpus-management skill and never loads at session start."
            )
            continue
        if kind == "tree":
            owned_trees.add(target)
        else:
            owned_files.add(target)
    return findings, owned_files, owned_trees


def find_local_rule_files(root: Path) -> list[Path]:
    """Return all markdown files under ``.claude/rules/`` except the
    local-only ``external/`` overlay."""
    local_dir = root / LOCAL_RULES_DIR_REL
    if not local_dir.is_dir():
        return []
    out: list[Path] = []
    for f in sorted(local_dir.rglob("*.md")):
        rel_parts = f.relative_to(local_dir).parts
        if rel_parts and rel_parts[0] == LOCAL_ONLY_SUBDIR:
            continue
        out.append(f)
    return out


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit that the pinned AIQT rule set validates against its "
            "release root and that every local .claude/rules file is "
            "covered by a verified owner."
        )
    )
    parser.add_argument(
        "--root",
        type=str,
        default=REPO_ROOT,
        help=(
            "Override the repository root used to resolve every path. "
            "Defaults to the repository root derived from this file's "
            "location."
        ),
    )
    args = parser.parse_args(argv)
    if args.root is not None:  # a missing, empty or non-directory --root is refused
        args.root = require_dir(args.root, "--root")
    root: Path = args.root.resolve()

    findings: list[str] = []
    try:
        aiqt_owned = validate_snapshot(root)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f"FAIL: AIQT snapshot: {exc}")
        return 1

    # --- Compiler-owned recognition (Corpus-Management pack, gate 99). ---
    try:
        ownership_findings, owned_files, owned_trees = load_compiler_owned(root)
    except OwnershipRegisterError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    findings.extend(ownership_findings)

    # --- Completeness check: every local rule file must be AIQT-owned, or
    # --- compiler-owned (recognized through the validated ownership
    # --- register above, never through a directory skip). ---
    for local_path in find_local_rule_files(root):
        rel = local_path.relative_to(root).as_posix()
        if rel in aiqt_owned:
            continue
        rel_posix = PurePosixPath(rel)
        if rel in owned_files or any(
            PurePosixPath(tree) in rel_posix.parents for tree in owned_trees
        ):
            # Compiler-owned: byte-integrity is gate 99's stricter job
            # (.claude/skills/corpus-management/tools/build-corpus-management.py --check).
            continue
        findings.append(
            f"unmapped local rule file: {rel}. Declare it in the "
            f"Corpus-Management ownership register "
            f"({OWNERSHIP_REGISTER_REL}) if it is compiler-generated "
            f"(gate 99 then owns its bytes), re-render it from the pinned "
            f"AIQT copy if it belongs to the AIQT rule set, or move it "
            f"under .claude/rules/{LOCAL_ONLY_SUBDIR}/ if it is a "
            f"local-only overlay with no upstream source."
        )

    if not findings:
        print(
            f"OK: {len(aiqt_owned)} pinned AIQT rule copies validate against "
            f"the release root; every local rule file is covered."
        )
        return 0

    print("FAIL: claude-rules sync findings:")
    for f in findings:
        print(f"  [claude-rules-sync] {f}")
    print(
        f"\n{len(findings)} finding(s). The .claude/rules/ copies are "
        f"loaded as session context and must track the pinned AIQT copy "
        f"or the compiler's ownership register."
    )
    return 1


def main(argv: list[str] | None = None) -> int:
    """Categorical crash-safety wrapper: any uncaught exception becomes a
    clean exit 2, never a traceback (the gate never crashes)."""
    try:
        return _main(argv)
    except Exception as exc:
        print("FAIL: claude-rules-sync internal error: "
              f"{type(exc).__name__}: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
