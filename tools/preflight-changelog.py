#!/usr/bin/env python3
"""CHANGELOG-hygiene first-commit pre-flight aid (TODO P4.14).

A gating helper run BEFORE the first commit of any PR that edits the
CHANGELOG, as:

    python3 tools/preflight-changelog.py && git commit ...

It exits non-zero (so the ``&&`` chain will not fire) when the working-tree
additions to the root [`CHANGELOG.md`] or the maintainer-grade detailed
mirror contain any of:

  - a gate-2 spelling finding (ise, isation, or yse), found by gate 2's own
    matcher (the engine's ``spelling_matches``: the same language profile and
    official-quote masks), or
  - an em-dash or en-dash in prose (the no-dash convention: delta gate D3
    enforces this PR-time on the root file, and gate 51 enforces it on the
    ``.working/`` mirror, but NEITHER fires on the first local commit), or
  - a path-shaped backtick code span that is not wrapped in a markdown link
    (the link-coverage convention that ``lint-changelog-link-coverage.py``
    enforces post-commit on the root file), or
  - a relative markdown-link whose in-repo target does not resolve to an
    existing file (3.34 (closing PR #1084)): unlike the two checks above, this one has NO
    authoritative gate behind it, because the detailed mirror lives under
    ``.working/`` (gate-exempt) so the corpus broken-link gate never scans it,
    a dangling link there is otherwise ungated. Cross-repo / out-of-repo
    targets (a sibling repo, an ``inbox/`` worker-provenance path), external
    ``http(s)``/``mailto:``/anchor targets, and code-span-illustrative links
    are excluded; resolution is relative to the source file's own directory.

  - a root ``CHANGELOG.md`` compact entry whose summary exceeds the D7 length
    ceiling (100 words total, or a single sentence over 45 words); this reuses
    ``check-changelog-length-on-pr.py`` (the D7 delta-gate authority) so the two
    never drift, catching an over-long entry at authoring rather than at the guard.

In addition to the added-line checks above, a FULL-MIRROR link-resolution pass
(3.34 (closing PR #1084) remaining half) scans EVERY in-repo relative markdown link in the
whole detailed mirror (not only added lines), reusing the identical resolution
and exclusion rules, and fails on any dangling target with its line number. This
catches a link that went dangling by a later move of its TARGET, which the
added-line pass (source line unchanged) cannot see. It runs unconditionally.

This is a developer AID, not a new audit gate. The authoritative gates
(D3, gate 51, the link-coverage gate) remain and run in CI and
``run_all_audits.sh`` / ``run-pr-time-checks.sh``; this aid only moves their
diagnosis earlier, to before the first commit, closing the recurring
commit-then-amend loop (improvement-log #341/#347/#349/#355). Run it in an
``&&`` chain: a ``;`` join commits whatever its exit status. Where
``tools/install-git-hooks.sh`` has installed the git-native pre-commit
hook, ``check-changelog-preflight-commit.py`` also runs it (``--staged``)
inside every commit that stages ``CHANGELOG.md`` and refuses on failure.

The check is scoped to the lines a PR ADDS (``git diff`` against HEAD), so
historical entries that predate the conventions never false-alarm. Dash
detection strips inline code spans first (a regex character class or a
quoted format literal may legitimately contain a dash), matching gate 51.

Known limitation: because the aid scans the added diff-lines in isolation,
it does NOT track fenced (```` ``` ````) code-block state the way the
authoritative link-coverage gate does (that gate skips path-shaped spans
inside fenced blocks). A path-shaped span added inside a fenced block in a
CHANGELOG entry would therefore make this aid exit 1 (over-block) where the
gate exits 0. The divergence fails safe (it over-blocks the author's own
commit; it never lets a defect through) and is latent (CHANGELOG entries do
not currently use fenced blocks), so full fenced-block tracking is left
unimplemented; if a CHANGELOG entry ever needs a fenced path-span, run the
commit without the aid and rely on the authoritative gate.

Usage:
    python3 tools/preflight-changelog.py            # working tree vs HEAD
    python3 tools/preflight-changelog.py --staged   # staged diff only

Exit codes:
    0   no spelling, dash, unlinked-reference, dangling-link, or D7-over-length issue in the added CHANGELOG lines
    1   one or more issues (do not commit until fixed)
    2   git invocation error: a ``git diff`` that fails (an unborn HEAD, or a directory that is not
        a repository, an operational store or private sibling holding the mirror included) exits 2
        instead of reporting 0 added lines and passing (fail closed, 3b141 QA r1); or the gate-2
        language engine cannot be loaded (a missing or unimportable tools/lint-language.py, pack
        engine or profile loader, or a malformed language profile), reported as one named ERROR
        line rather than a traceback, whether or not any line was added (3b201)
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from aiqt_corpus import CODE_SPAN_RE  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import REPO_ROOT, resolve_working  # noqa: E402  # grc-config/store, stays local

# D7 length check reuse (P-1.4): import the authoritative per-PR length checker so the
# 100-word / 45-word-sentence ceiling on a root-CHANGELOG compact entry is caught at
# authoring (this aid) rather than only at the pre-push guard. The module name is
# hyphenated, so load it via importlib; reusing its ENTRY_RE + evaluate keeps the two in
# lock-step (no duplicated length logic to drift).
import importlib.util as _ilu  # noqa: E402
_d7_spec = _ilu.spec_from_file_location(
    '_changelog_len_d7', Path(__file__).resolve().parent / 'check-changelog-length-on-pr.py')
_d7 = _ilu.module_from_spec(_d7_spec)
_d7_spec.loader.exec_module(_d7)


# Gate 2's project entry point. load_language() loads it, and through it the pack
# engine and the language profile, exactly as the gate does.
_LANGUAGE_GATE = Path(_TOOLS_DIR) / "lint-language.py"


class LanguageEngineUnavailable(RuntimeError):
    """Gate 2's wrapper, engine or language profile could not be loaded (main() exits 2)."""


def load_language():
    """``(engine, checks)``: gate 2's engine module and its compiled language checks.

    Any failure to load (a missing or unimportable wrapper, engine or profile
    loader, or a malformed profile) raises LanguageEngineUnavailable naming the
    cause, so the aid fails closed with exit 2 and a named message rather than a
    traceback, and never skips the spelling check (3b201).
    """
    try:
        spec = _ilu.spec_from_file_location("_changelog_language", _LANGUAGE_GATE)
        mod = _ilu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        engine = mod._engine()
        for name in ("spelling_matches", "compile_language", "language_vocabulary"):
            if not callable(getattr(engine, name, None)):
                raise TypeError(f"language engine {name} must be callable")
        return engine, engine.compile_language(mod._language_config())
    except KeyboardInterrupt:
        raise
    except BaseException as exc:
        detail = " ".join(str(exc).splitlines())
        raise LanguageEngineUnavailable(
            f"the gate-2 language engine could not be loaded through {_LANGUAGE_GATE.name} "
            f"(its pack engine, profile loader and language profile included): "
            f"{type(exc).__name__}: {detail}") from exc


def spelling_findings(lines, language=None):
    """Check added lines with gate 2's own spelling matcher.

    ``language`` is a load_language() result (None loads it). The engine's
    ``spelling_matches`` applies gate 2's vocabulary, patterns and quote masks.
    Additions are checked in isolation, including inline code as in gate 2.
    Fenced additions may over-report, like the existing preflight link check.
    """
    engine, checks = language or load_language()
    return [(path, f"gate 2 spelling [{kind}]: {word}", text.strip())
            for path, text in lines
            for kind, word in engine.spelling_matches(text, checks)]


def d7_length_findings(lines):
    """The D7 length-ceiling findings for the ROOT ``CHANGELOG.md`` compact entries in
    ``lines`` (a list of ``(path, added_text)``), reusing ``check-changelog-length-on-pr``'s
    ENTRY_RE + evaluate so this aid and the D7 delta gate never drift (P-1.4). Only the root
    file is length-gated; the detailed mirror is out of the D7 gate's scope."""
    entries = []
    for path, text in lines:
        if path == "CHANGELOG.md":
            m = _d7.ENTRY_RE.match(text)
            if m:
                entries.append((m.group(1), m.group(2)))
    return [
        ("CHANGELOG.md", f"D7 length ceiling exceeded ({offence})", "")
        for offence in _d7.evaluate(entries, _d7.DEFAULT_WORD_MAX, _d7.DEFAULT_SENTENCE_MAX)
    ]


CHANGELOG_FILES = (
    "CHANGELOG.md",
    ".working/changelog-details/CHANGELOG-detailed.md",
)

EM_DASH = "\u2014"
EN_DASH = "\u2013"

# Inline code-span stripper: a run of N backticks, the shortest content, then
# a closing run of N backticks (the standard CommonMark code-span shape). Same
# approach as gate 51 (lint-working-prose-hygiene.py), so a dash that is
# legitimately inside a code span (a regex character class, a quoted format
# literal) is treated as content, not prose.
#
# DELIBERATE two-parser seam (GR-11): this file carries TWO code-span parsers
# because each mirrors a DIFFERENT authoritative gate. This regex mirrors gate
# 51's any-length span stripper (the dash check); the manual single-backtick
# walk in unlinked_refs_in_line() mirrors lint-changelog-link-coverage.py's
# per-line walk byte-for-byte (the link check). Unifying them would break
# parity with one gate or the other; keep each in step with ITS gate.

# --- File-reference recognition, mirrored from lint-changelog-link-coverage.py ---
# Kept in step with that gate (the authoritative post-commit check); this aid
# only surfaces the same class earlier. If the gate's logic changes, update
# this block to match.
FILE_EXTENSIONS = (
    ".md",
    ".py",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".cff",
    ".toml",
    ".html",
    ".css",
    ".js",
)
TOP_LEVEL_FILES = {
    "README.md",
    "CHANGELOG.md",
    "NOTICE.md",
    "LICENSE",
    "CITATION.cff",
    "AUTHORS.md",
    "TODO.md",
    "TODO-REFERENCE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "taxonomy.yml",
    ".pre-commit-config.yaml",
    "specification-ingestion.md",
    "specification-master-project.md",
}


def looks_like_file_reference(text: str) -> bool:
    if "/" in text and text.endswith(FILE_EXTENSIONS):
        return True
    if text in TOP_LEVEL_FILES:
        return True
    if "/" not in text and text.endswith(FILE_EXTENSIONS):
        base = text[: text.rindex(".")]
        if base and re.match(r"^\.?[A-Za-z0-9][A-Za-z0-9_\-.]*$", base):
            return True
    return False


def unlinked_refs_in_line(line: str) -> list[str]:
    """Return path-shaped backtick spans on a line that are NOT wrapped in a
    markdown link. Mirrors the per-line walk in lint-changelog-link-coverage.py."""
    findings: list[str] = []
    i = 0
    while i < len(line):
        # Skip an already-linked reference: [`...`](...)
        if line[i] == "[" and i + 1 < len(line) and line[i + 1] == "`":
            close = line.find("](", i + 2)
            if close != -1:
                paren_close = line.find(")", close + 2)
                if paren_close != -1:
                    i = paren_close + 1
                    continue
        if line[i] != "`":
            i += 1
            continue
        end = line.find("`", i + 1)
        if end == -1:
            break
        inner = line[i + 1 : end]
        if looks_like_file_reference(inner):
            findings.append(inner)
        i = end + 1
    return findings


# --- Markdown-link target resolution (3.34 (closing PR #1084)) ---
# The detailed mirror lives under `.working/` (gate-exempt), so the corpus
# broken-link gate does not scan it; a dangling relative link there is otherwise
# ungated. This check verifies that each IN-REPO relative markdown-link target
# an added line introduces resolves to an existing file. Excluded (by
# construction, consistent with the worker-provenance plain-text convention):
# external `http(s)`/`mailto:`/anchor targets;
# cross-repo / out-of-repo targets (a sibling repo such as `grc_library_ref` /
# `grc_library_scratch`, or an `inbox/` worker-provenance path, or any target
# that resolves outside this repo); and links inside a code span (an
# illustrative ``[text](url)``). Resolution is relative to the SOURCE file's
# own directory, so the same check serves both CHANGELOG files.
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CROSS_REPO_MARKERS = ("grc_library_ref", "grc_library_scratch", "/inbox/")


def unresolved_link_targets(
    source_rel_path: str,
    line: str,
    root: Path = REPO_ROOT,
    *,
    source_path: Path | None = None,
) -> list[str]:
    """Return in-repo relative markdown-link targets on ``line`` that do NOT
    resolve to an existing file (see the block comment above for exclusions).
    ``root`` is the repository root (default ``REPO_ROOT``); it is a parameter so
    the full-mirror scan (3.34 (closing PR #1084)) can reuse this identical resolution against
    a test root without a divergent reimplementation. ``source_path`` is the
    PHYSICAL on-disk location of the source file when it differs from its logical
    ``root``/``source_rel_path`` location (the post-.working-move case: the mirror
    is read from the private sibling). Link CLASSIFICATION stays logical against
    the public ``root``; link EXISTENCE follows the physical working tree for a
    target that stays inside logical ``.working/``, and the public ``root`` for a
    target that leaves ``.working/`` into the public corpus."""
    findings: list[str] = []
    stripped = CODE_SPAN_RE.sub("", line)  # drop code-span-illustrative links
    public_root = root.resolve()
    logical_source = public_root / source_rel_path
    physical_source = source_path or logical_source
    logical_working = public_root / ".working"
    for match in MD_LINK_RE.finditer(stripped):
        base = match.group(1).split("#", 1)[0].strip()
        if not base or base.startswith(("http://", "https://", "mailto:")):
            continue
        if any(marker in base for marker in CROSS_REPO_MARKERS):
            continue
        logical_target = (logical_source.parent / base).resolve()
        try:
            logical_target.relative_to(public_root)
        except ValueError:
            continue  # resolves outside this repo: treated as cross-repo
        try:
            logical_target.relative_to(logical_working)
        except ValueError:
            # The link left logical .working but stayed in the public repo:
            # resolve existence against the public corpus.
            resolved = logical_target
        else:
            # The link stayed inside logical .working: follow the selected
            # physical working tree (a private-only mirror included).
            resolved = (physical_source.parent / base).resolve()
        if not resolved.exists():
            findings.append(base)
    return findings


# --- Full-mirror link-resolution scan (3.34 (closing PR #1084) remaining half) ---
# The added-line check above catches a NEW dangling link before commit, but a
# link that went dangling by a later move of its TARGET (the source line
# unchanged) is invisible to it. This full-mirror pass scans EVERY in-repo
# relative markdown link in the whole detailed mirror, reusing the identical
# resolution + exclusion rules of unresolved_link_targets line-by-line. It runs
# unconditionally (the mirror is currently clean at 0 dangling of 142 links, so
# default-on adds no noise; the tradeoff is that it re-reads the whole mirror
# each run, negligible for a single file). Known limitation inherited from the
# per-line resolver: a link inside a FENCED code block is not skipped (the
# resolver only strips single-backtick code spans); there are 0 fenced-block
# links in the mirror today, so no false positive arises. If a future
# fenced-block illustrative link appears, add ```-fence tracking here.
DETAILED_MIRROR_REL = ".working/changelog-details/CHANGELOG-detailed.md"


def unresolved_links_in_mirror(root: Path | None = None) -> list[tuple[int, str, str]]:
    """Every in-repo relative markdown-link target in the WHOLE detailed mirror
    that does NOT resolve. Returns ``(line_no, target, line_text)`` per dangling
    link. Reuses ``unresolved_link_targets`` (same rules). ``root=None`` (the
    default) resolves the mirror via ``resolve_working`` (private sibling then
    in-repo); an explicit ``root`` preserves the temp-fixture behaviour. Link
    targets resolve against ``REPO_ROOT`` in the default case, since the mirror's
    references are authored relative to the public corpus. Returns [] if absent."""
    if root is None:
        mirror = resolve_working(
            DETAILED_MIRROR_REL[len(".working/"):], repo_root=REPO_ROOT)
        if mirror is None or not mirror.is_file():
            return []
        resolution_root = REPO_ROOT
    else:
        mirror = root / DETAILED_MIRROR_REL
        if not mirror.is_file():
            return []
        resolution_root = root
    findings: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(
        mirror.read_text(encoding="utf-8").splitlines(), start=1
    ):
        for target in unresolved_link_targets(
                DETAILED_MIRROR_REL, line, root=resolution_root,
                source_path=mirror):
            findings.append((lineno, target, line.strip()))
    return findings


def _foreign_repo_env() -> dict[str, str]:
    """This process's environment for a ``git diff`` in ANOTHER repository (the operational store or
    the private sibling holding the mirror): every variable that ``git rev-parse --local-env-vars``
    names as local to one repository is dropped (GIT_INDEX_FILE, GIT_DIR, GIT_WORK_TREE,
    GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_DIRECTORIES, GIT_COMMON_DIR, GIT_CONFIG_PARAMETERS
    and the rest; git drops the same list before it enters a submodule), and every other variable
    is kept. A pre-commit hook inherits them for the PUBLIC repository (``git commit -a`` names its
    temporary index in GIT_INDEX_FILE), and the mirror's ``git diff --cached`` read that index
    through them: it found no staged mirror addition, so a commit the standalone aid refuses passed
    (3b141 QA r2). A failure to list them raises ``CalledProcessError``, and ``main()`` exits 2."""
    local = set(subprocess.run(["git", "rev-parse", "--local-env-vars"], capture_output=True,
                               text=True, check=True).stdout.split())
    return {k: v for k, v in os.environ.items() if k not in local}


def _added_lines_from_repo(
    repo: Path, paths: tuple[str, ...], staged: bool, env: dict[str, str] | None = None
) -> list[tuple[str, str]]:
    """(file, added-line-text) for every added CHANGELOG line in ONE repo's diff, run with ``env``:
    None inherits this process's environment, right for the public repository, where a pre-commit
    hook's GIT_INDEX_FILE names the index being committed; a mirror in another repository passes
    :func:`_foreign_repo_env`.

    The flags override every setting that would reshape what the parser below reads (3b141 QA
    r1): an external diff driver (``diff.external``, ``GIT_EXTERNAL_DIFF``, the ``command`` of a
    ``diff=<driver>`` attribute), a ``textconv`` filter, a ``-diff`` or ``binary`` attribute (it
    prints "Binary files ... differ"), colour (``color.diff``, ``color.ui``), and the ``+++ b/``
    prefix (``diff.noprefix``, ``diff.mnemonicPrefix``, ``diff.dstPrefix``). Each leaves no
    ``+++ b/`` header or ``+`` line, so the aid reported 0 added lines and passed. Not pinned: the
    source prefix (only the ``---`` line carries it, and the parser skips that line), and
    ``diff.relative`` (it changes a path, never whether a ``+`` line is read).

    A git failure raises ``CalledProcessError`` carrying git's ``stderr``, and ``main()`` exits 2:
    an unread diff is not zero added lines. This replaces the 3.190 fail-open, which returned []
    for any git failure (a sibling that is not a git repository included), so a failed diff
    printed "OK: 0 added CHANGELOG line(s)" and exited 0."""
    cmd = ["git", "diff", "--no-ext-diff", "--no-textconv", "--text", "--no-color",
           "--dst-prefix=b/", "--unified=0"]
    if staged:
        cmd.append("--cached")
    cmd += ["HEAD", "--", *paths]
    out = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True,
                         check=True, env=env).stdout
    results: list[tuple[str, str]] = []
    current: str | None = None
    for line in out.splitlines():
        if line.startswith("+++ b/"):
            current = line[len("+++ b/") :]
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+") and current is not None:
            results.append((current, line[1:]))
    return results


def added_lines(staged: bool, root: Path = REPO_ROOT) -> list[tuple[str, str]]:
    """Added CHANGELOG lines across the public repo AND the (post-move) private
    detailed mirror. The public root CHANGELOG.md (and, pre-move, the in-repo
    mirror) come from this repo's diff; a private-sibling mirror gets its OWN
    repository-local ``git diff`` so private additions still receive the dash and
    unlinked-path checks. That diff runs without this repository's local git
    variables (:func:`_foreign_repo_env`), so ``--staged`` reads THAT repository's
    index. The ``staged`` choice is applied separately in each repository,
    preserving staged-only versus full-working-tree semantics."""
    public_paths = ["CHANGELOG.md"]
    if (root / DETAILED_MIRROR_REL).is_file():
        public_paths.append(DETAILED_MIRROR_REL)
    results = _added_lines_from_repo(root, tuple(public_paths), staged)
    mirror = resolve_working(
        DETAILED_MIRROR_REL[len(".working/"):], repo_root=root
    )
    if mirror is None or not mirror.is_file():
        return results
    try:
        mirror.relative_to(root.resolve())
    except ValueError:
        # The mirror lives outside this repo (the operational store, Option C, or a
        # private sibling). resolve_working already located it; derive its OWN repo
        # root from the stripped mirror-relative path's depth (store layout is
        # changelog-details/<file> -> root is parents[1]) and diff it there with the
        # stripped rel path, so the store (no .working/ prefix) and any sibling layout
        # both resolve correctly. Fixes the prior parents[2]+".working/"-rel mismatch
        # that silently no-op'd the store mirror's added-line checks.
        stripped_rel = DETAILED_MIRROR_REL[len(".working/"):]
        private_root = mirror.parents[stripped_rel.count("/")]
        results.extend(
            _added_lines_from_repo(private_root, (stripped_rel,), staged,
                                   env=_foreign_repo_env())
        )
    return results


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Pre-commit aid: fail when added CHANGELOG lines carry an em/en "
            "dash in prose, a gate-2 spelling, an unlinked path-shaped reference, a dangling "
            "in-repo markdown-link target, or a root entry over the D7 length ceiling."
        )
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help=("Check only the staged diff's added lines (default: full working tree vs HEAD); "
              "link targets and the full-mirror scan still read the working tree."),
    )
    args = parser.parse_args(argv[1:])

    try:
        lines = added_lines(args.staged)
    except subprocess.CalledProcessError as exc:
        # Fail closed (3b141 QA r1): a failed diff is not zero added lines.
        detail = (exc.stderr or "").strip()
        print(f"ERROR: git diff failed: {exc}" + (f"\n{detail}" if detail else ""), file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: the CHANGELOG diff could not be read: {exc}", file=sys.stderr)
        return 2
    try:
        language = load_language()
    except LanguageEngineUnavailable as exc:
        # Fail closed (3b201): an unloadable engine is not a clean spelling check.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    findings: list[tuple[str, str, str]] = []
    for path, text in lines:
        stripped = CODE_SPAN_RE.sub("", text)
        if EM_DASH in stripped or EN_DASH in stripped:
            findings.append((path, "em/en dash in prose", text.strip()))
        for ref in unlinked_refs_in_line(text):
            findings.append((path, f"unlinked file reference `{ref}`", text.strip()))
        # Resolution on the ROOT changelog only: the detailed mirror is covered
        # in full by the full-mirror pass below (which also catches a link that
        # went dangling by a later move of its target), so resolving the mirror
        # here too would double-report a newly-added mirror dangling link.
        if path != DETAILED_MIRROR_REL:
            for tgt in unresolved_link_targets(path, text):
                findings.append(
                    (path, f"dangling markdown-link target `{tgt}`", text.strip())
                )

    # Full-mirror scan (3.34 (closing PR #1084) remaining half): catch a link that went
    # dangling by a later move of its target, which the added-line pass misses.
    for lineno, tgt, evidence in unresolved_links_in_mirror():
        findings.append(
            (
                DETAILED_MIRROR_REL[len(".working/"):],
                f"dangling markdown-link target `{tgt}` (full-mirror scan, line {lineno})",
                evidence,
            )
        )

    findings.extend(spelling_findings(lines, language))
    findings.extend(d7_length_findings(lines))

    if not findings:
        scope = "staged" if args.staged else "working-tree"
        print(
            f"OK: {len(lines)} added CHANGELOG line(s) ({scope}) are spelling-clean and dash-free, "
            f"every path-shaped reference is a markdown link, every in-repo link "
            f"target resolves, and no root entry exceeds the D7 length ceiling."
        )
        return 0

    for path, issue, evidence in findings:
        # Only append the evidence line when there is evidence: the D7 length findings
        # carry no line-evidence (the offence string already names the PR and the count),
        # so a blank indented line would otherwise print (claude vpr1325 cosmetic note).
        msg = f"FAIL {path}: {issue}" + (f"\n    {evidence}" if evidence else "")
        print(msg, file=sys.stderr)
    print(
        f"\n{len(findings)} CHANGELOG-hygiene issue(s) in the added lines. Fix "
        f"before committing: fix gate-2 spellings, remove em/en dashes from prose (use commas, "
        f"colons, or parentheses), wrap path-shaped references as "
        f"[`path`](path), fix any dangling in-repo link target (or exclude "
        f"a cross-repo / illustrative link), and shorten any root entry over the "
        f"D7 length ceiling (100 words total, or a single sentence over 45 words). "
        f"This aid mirrors gate 2 spelling, delta gate D3, the D7 length check, gate 51, the "
        f"link-coverage gate, and the detailed-mirror link-resolution check "
        f"(3.34 (closing PR #1084)), surfaced before the first commit.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
