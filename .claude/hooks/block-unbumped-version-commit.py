#!/usr/bin/env python3
"""PreToolUse: auto-bump (or, failing that, refuse) a `git commit` that changes a versioned document's body without bumping it.

WHY THIS IS A HOOK AND NOT A CONVENTION, STATED WITH THE COUNT. The convention existed, is written
down in two places, and the orchestrator broke it FIVE times in a single session on 2026-07-26, plus
a sixth downstream miss (the derived artefacts left unregenerated after a bump). Between the third
and the fifth it wrote a close-out checklist bullet describing the failure precisely, and then
committed the same defect twice more. That is the signature of a control at the wrong layer: the
knowledge was present and the timing was not.

THE ACTUAL CAUSE, because it decides the design. Gates 40 and D2 already catch this, but they speak
at PRE-PUSH time, roughly six minutes into a guard run and several commits after the edit. By then
the repair is itself a new commit touching the same file, which is how one miss becomes a chain: a
D4 repair that moved a `Date` became a gate-40 failure, whose repair became a gate-33 failure. The
fix has to fire at the moment of the commit, where the correction is free.

WHAT IT READS. The STAGED diff (`git diff --cached`), targeting `project_root()` via `git -C`.
That root is derived from the hook's own location (NOT the command's `-C` target or the runtime cwd).
The Git subprocesses inherit ambient Git environment variables, so `GIT_DIR` / `GIT_WORK_TREE`
pointing at a scratch repository can redirect Git despite `-C`; working-file reads still use
`project_root()`. It does not
simulate preceding commands, a `commit -a`, or a path-selected commit, so any of those can make the
inspected index differ from what the eventual commit contains. Eligibility comes from WORKING-TREE
contents: a staged `.md` file outside `.corpus-management/` whose working file carries any column-zero
`**Version:**` line. For each, it asks whether a changed line is non-metadata (a column-zero `**Key:** value`
line, matched anywhere, is treated as metadata; a blank changed line is ignored) while no changed line is a
`**Version:**` line. This is a lighter, commit-time cousin of gate 40's committed-history check (gate 40
remains the authority and compares differently); it checks only that a `**Version:**` line was added or
removed, not that the value increments. Eligible paths come from `git diff --cached --name-only` filtered to
staged `.md` files (outside `.corpus-management/`) whose working file carries a `**Version:**` line (a
per-file read error skips only that file). Git-quoted (including octal-escaped) `--name-only` paths are
not decoded before suffix checks and working-file reads, so a file can fail eligibility and never enter
`versioned`. The diff-header parser associates hunks by splitting each header at its first ` b/` and
requiring the resulting path to be in `versioned`; a ` b/`-containing or Git-quoted header path can also
break that association. Quoting can therefore defeat eligibility as well as hunk association.

WHAT IT DOES, AND WHAT IT DELIBERATELY DOES NOT.
  - AUTO-FIXES FIRST, THEN BLOCKS (auto-fix added #1237): on a staged body change to a versioned
    file with no staged `Version` change, it attempts a PATCH increment of the FIRST numeric `**Version:**` match before the metadata-region
    boundary (skipping an earlier bracketed-template Version),
    updates the first matching `**Date:**` in the leading metadata region IF one is present (otherwise the
    Date is left unchanged), writes the file, then re-stages it. The write-then-stage is not transactional,
    so a later failure can leave the working file modified. It reports the file(s) it could NOT auto-bump
    (other unstaged changes present, no `SEMVER_VERSION` match before the metadata-region end, or an
    Exception during the attempt) and BLOCKS THE WHOLE tool call if any remain; auto-bumps done earlier in
    the same run are kept.
  - ALSO WARNS (never blocks), only when the offender list is empty, over the eligible
    working-tree-VERSIONED staged paths (not every staged `.md`), for those in a subdirectory outside
    `.working/` and `.claude/` when none of the derived artefacts is staged alongside them
    (a corpus path checks `taxonomy.yml` / `docs/portal.md` / `docs/maturity-scorecard.md`; an executive
    path checks `narrative.yml`). It does NOT verify that a `**Version:**` value actually moved, so a
    Date-only staged change can trigger it; it warns rather than blocks because the regeneration order
    matters and the generated artefacts can be staged alongside the document without unstaging it.
  - DOES NOT block a `Version` bump whose `Date` is stale: delta gate D4 owns that comparison, it
    needs the commit's own date which does not exist yet at PreToolUse time, and duplicating it here
    from a guessed date would be a check whose input cannot answer it.
  - DOES NOT touch files with no `**Version:**` line at all.
  - DOES NOT act on a `git commit --amend`: an amend reuses an existing commit and its diff is not
    the staged set alone, so the hook leaves it (the refuse-what-you-cannot-answer discipline); a
    staged body change amended in is NOT version-checked here (gate 40 / D2 remain the authority).

FAIL-OPEN, BUT NOT UNIVERSALLY. A failure during the INITIAL JSON parse, repository location, or
staged-diff inspection ALLOWS the commit; an error reading one candidate working file skips only that
file, so other offenders can still block. A failure DURING an offender's auto-bump (a `git diff`/`git add`
error, or any exception in `try_auto_bump`) is caught as an unsuccessful attempt, which keeps that file a
blocking offender rather than allowing. A guard that blocks all work when it breaks gets removed within a
day (the same trade `block-on-open-findings.py` records), which is why the read path fails open; the
auto-bump path fails toward the block it was already going to issue. Defence in depth under gates 40 and
D2, which remain the authority.

THE ESCAPE HATCH IS DELIBERATE AND NARROW. A command whose text contains the bare token
`VersionBump: none` proceeds (matched anywhere in the command string; the `<reason>` is a CONVENTION
for the reviewer, NOT mechanically required or checked by this hook). Some body edits genuinely do
not warrant a bump, and without a sanctioned opt-out an author whose edit genuinely does not warrant one
has no clean path, so the guard becomes friction that invites disabling it wholesale, which is worse than a
hatch that, by convention, leaves a reason in the commit message where a reviewer can see it.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION_LINE = re.compile(r"^\*\*Version:\*\*", re.M)
# METADATA_PREFIX matches a column-zero `**Key:** value` line ANYWHERE (classify_hunk applies it
# per changed line, with no leading-block tracking). Changing only such lines is a metadata edit,
# not a body change, so it must not by itself demand a bump.
METADATA_PREFIX = re.compile(r"^\*\*[A-Za-z][A-Za-z ()/-]*:\*\*")
OPT_OUT = re.compile(r"VersionBump:\s*none\b", re.I)
# Generated artefacts, split by SOURCE: corpus documents feed the taxonomy chain;
# executive/ pages feed narrative.yml. Split sets so staging one family cannot
# suppress the warn for the other (the #1454 codex E1 routing catch).
TAXONOMY_GENERATED = ("taxonomy.yml", "docs/portal.md", "docs/maturity-scorecard.md")
NARRATIVE_GENERATED = ("narrative.yml",)
GENERATED = TAXONOMY_GENERATED + NARRATIVE_GENERATED
# A `**Version:**` line beginning with three dot-separated digit groups (auto-bumpable); the trailing
# `(.*)` preserves any remainder, so this does NOT distinguish semver from a numerically similar CalVer
# and increments a `**Version:** 2026.07.725` just as it would a semver value. README's `**Library
# Version:**` field is a DIFFERENT key and is not matched by VERSION_LINE at all; a bracketed template
# `**Version:** <x.y.z ...>` has no leading digit group and does not match SEMVER_VERSION. When no numeric
# match exists before the metadata-region end bump_semver returns None and the offender blocks; a numeric
# match can still block if the file has other unstaged changes or the auto-bump raises.
SEMVER_VERSION = re.compile(r"^(\*\*Version:\*\*[ \t]*)(\d+)\.(\d+)\.(\d+)(.*)$", re.M)
DATE_META = re.compile(r"^(\*\*Date:\*\*[ \t]*)(\d{4}-\d{2}-\d{2})(.*)$", re.M)
# README carries its version under a DIFFERENT key (``**README Version:**``), which VERSION_LINE does
# not match, so README is outside the body-without-bump check above. The date-lag NOTE below covers
# both keys: a staged Version (or README Version) change whose staged ``**Date:**`` is not today UTC
# is the UTC-rollover co-bump miss D4 otherwise catches only at the pre-push guard (2026-09-24, #2492).
ANY_VERSION_LINE = re.compile(r"^\*\*(?:README )?Version:\*\*")
HUNK_NEW = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def _lf_lines(s: str, keepends: bool = False) -> list[str]:
    """PURE. Split on LF only. git diff output and hunk positions are LF-delimited, whereas
    str.splitlines() also splits on U+2028, U+0085 and similar, which can fabricate a diff line
    (a fake 'diff --git' or '+++') from content inside one real line (#2496 r4, codex)."""
    parts = s.split("\n")
    if keepends:
        out = [x + "\n" for x in parts[:-1]]
        if parts[-1]:
            out.append(parts[-1])
        return out
    return parts[:-1] if parts and parts[-1] == "" else parts


def version_line_changed(lines: list[str]) -> bool:
    """PURE. True when a +/- changed line (not a diff header) is a Version or README Version line."""
    for ln in lines:
        if ln.startswith(("+++", "---", "@@", "diff ", "index ", "new file", "deleted file")):
            continue
        if ln and ln[0] in "+-" and ANY_VERSION_LINE.match(ln[1:]):
            return True
    return False


def stale_date_after_bump(diff: str, staged_text: dict, today: str) -> list[str]:
    """PURE. Paths whose staged diff changes a Version/README Version line while the staged file's
    first ``**Date:**`` value is not ``today``. A file with no Date line is not reported."""
    out, cur, buf = [], None, []

    def flush():
        if not cur:
            return
        text = staged_text.get(cur, "")
        head = text[:_metadata_region_end(text)]
        # Only a Version line that sits in the METADATA header counts (a body/fenced example
        # changing is not a bump), and only the header Date is compared.
        # Position-based (not text-membership): track new-file line numbers from the hunk headers
        # and count an added Version line only when it LIES within the header, so a body/fenced
        # example whose new value equals the unchanged header Version is not mistaken for a bump.
        # Count LF-delimited lines only (git hunk positions do; str.splitlines() also splits on
        # U+2028 and similar). Inside a hunk every '+' line is an added line, including one whose
        # content begins '++' (rendered '+++'); the '+++ b/...' file header precedes the first '@@'.
        header_lines = head.count("\n") + (1 if head and not head.endswith("\n") else 0)
        n, hit, in_hunk = 0, False, False
        for ln in buf:
            h = HUNK_NEW.match(ln)
            if h:
                n, in_hunk = int(h.group(1)), True
            elif not in_hunk:
                continue
            elif ln.startswith("+"):
                if ANY_VERSION_LINE.match(ln[1:]) and 1 <= n <= header_lines:
                    hit = True
                n += 1
            elif ln.startswith(" "):
                n += 1
        if not hit:
            return
        m = DATE_META.search(head)
        if m and m.group(2) != today:
            out.append(cur)

    for ln in _lf_lines(diff):
        if ln.startswith("diff --git "):
            flush()
            parts = ln.split(" b/", 1)
            cur, buf = (parts[1] if len(parts) == 2 else None), []
        else:
            buf.append(ln)
    flush()
    return out


def project_root() -> Path:
    # Derived from this file's location, never hardcoded, so the guard follows a repo relocation
    # (the row-E lesson from the /home/grc move, where five hooks kept a stale absolute root).
    return Path(__file__).resolve().parents[2]


# `git commit` is almost never adjacent in this project: the wrong-repo guard requires `git -C
# <root> commit`, so a substring test for "git commit" matches nothing that actually gets run. The
# self-test caught exactly that, which is the case for writing the fixture from real command shapes.
COMMIT_RE = re.compile(r"\bgit\b(?:\s+-C\s+\S+)*\s+commit\b")


def is_commit(cmd: str) -> bool:
    """PURE. Does the flattened command text contain `git`, optional whitespace-delimited `-C`
    operands, and `commit` (a textual match, not a guarantee a commit will be created: `git commit
    --dry-run` and `echo 'git commit'` both match)? Any `--amend` substring anywhere exempts it."""
    flat = " ".join(cmd.split())
    if not COMMIT_RE.search(flat):
        return False
    # `--amend` reuses an existing commit and its diff is not the staged set alone; leave it alone
    # rather than guess, which is the refuse-to-answer-what-you-cannot discipline.
    return "--amend" not in flat


def classify_hunk(lines: list[str]) -> tuple[bool, bool]:
    """PURE. (body_changed, version_changed) for one file's unified-diff lines.

    A changed line counts as BODY unless it is blank/whitespace-only or a column-zero `**Key:**
    value` metadata line (matched by position anywhere, not only in a leading block). Header lines
    beginning `+++`/`---`/`@@`/`diff `/`index `/`new file`/`deleted file` are skipped by a prefix check
    on the RAW diff line (before the +/- change marker is stripped), so a `+`/`-`-marked content line
    starting `diff `/`index `/`@@`/etc. does NOT match and is kept as body, though content rendered
    `+++`/`---` does match and is skipped. Returns two independent
    booleans because the interesting state is
    body-without-version, and collapsing them early would hide it.
    """
    body = version = False
    for ln in lines:
        if ln.startswith(("+++", "---", "@@", "diff ", "index ", "new file", "deleted file")):
            continue
        if not ln or ln[0] not in "+-":
            continue
        text = ln[1:]
        if VERSION_LINE.match(text):
            version = True
        elif METADATA_PREFIX.match(text):
            continue
        elif text.strip():
            body = True
    return body, version


def offenders(diff: str, versioned: set[str]) -> list[str]:
    """PURE. Staged versioned files whose body changed with no Version change. Each diff header is
    split at its FIRST literal ` b/`, so a path CONTAINING ` b/` (or a Git-quoted path) can be
    misidentified or missed; such a file is then not seen as an offender."""
    out, cur, buf = [], None, []

    def flush():
        if cur in versioned:
            body, ver = classify_hunk(buf)
            if body and not ver:
                out.append(cur)

    for ln in _lf_lines(diff):
        if ln.startswith("diff --git "):
            flush()
            parts = ln.split(" b/", 1)
            cur, buf = (parts[1] if len(parts) == 2 else None), []
        else:
            buf.append(ln)
    flush()
    return out


def git(root: Path, *args: str) -> str:
    # Raw bytes, decoded WITHOUT newline translation: text=True would apply universal newlines and
    # turn a lone CR inside a tracked line into a line break before any parser sees it (#2496 r5).
    out = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=True).stdout
    return out.decode("utf-8", "surrogateescape")


def _metadata_region_end(text: str) -> int:
    """PURE. Char offset where the leading run of blank, `#`-prefixed, and `**Key:**`-metadata-shaped
    lines ends (a heuristic boundary, not a parse of document structure; each line is stripped first, so an
    INDENTED metadata-shaped line also extends the region and a Markdown `#` heading is treated as a comment).
    The auto-bump searches only
    before this offset, so a `**Version:**`/`**Date:**` at or after it (a fenced example or a template)
    is left untouched."""
    off = 0
    for line in _lf_lines(text, keepends=True):
        st = line.strip()
        if st == "" or st.startswith("#") or METADATA_PREFIX.match(st):
            off += len(line)
            continue
        break
    return off


def bump_semver(text: str) -> str | None:
    """PURE. `text` with the FIRST `SEMVER_VERSION` match BEFORE `_metadata_region_end(text)`
    patch-bumped, or None if there is no such match. The regex matches any three dot-separated digit
    groups, so a CalVer-shaped `**Version:** 2026.07.725` in the metadata region also matches and is
    bumped. A bracketed-template `**Version:** <x.y.z>` line does not itself match and is skipped, so a
    later numeric Version line before the region end is still found and bumped; None is returned only when
    NO numeric match exists before the region end -> caller blocks."""
    m = SEMVER_VERSION.search(text[:_metadata_region_end(text)])
    if not m:
        return None
    maj, mnr, pat = int(m.group(2)), int(m.group(3)), int(m.group(4))
    repl = f"{m.group(1)}{maj}.{mnr}.{pat + 1}{m.group(5)}"
    return text[:m.start()] + repl + text[m.end():]


def set_date(text: str, today: str) -> str:
    """PURE. Set the FIRST `**Date:** YYYY-MM-DD` in the metadata block to `today`; unchanged if none."""
    m = DATE_META.search(text[:_metadata_region_end(text)])
    if not m:
        return text
    return text[:m.start()] + f"{m.group(1)}{today}{m.group(3)}" + text[m.end():]


def try_auto_bump(root: Path, path: str, today: str) -> bool:
    """Attempt a patch Version bump + Date update on an offender and re-stage it. Return True on
    success, False (caller blocks) when the file has OTHER unstaged changes (auto-staging would grab
    them), cannot be read, has no `SEMVER_VERSION` match before the metadata-region end, or any
    Exception occurs during the attempt. The write-then-stage is not transactional, so a failure after
    the write can leave the working file modified."""
    try:
        if git(root, "diff", "--name-only", "--", path).strip():
            return False
        f = root / path
        # newline="" on both sides: a CRLF file keeps its line endings when auto-bumped.
        text = f.read_text(newline="")
        bumped = bump_semver(text)
        if bumped is None:
            return False
        f.write_text(set_date(bumped, today), newline="")
        git(root, "add", "--", path)
        return True
    except Exception:
        return False


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get("tool_name") != "Bash":
        return 0
    cmd = (payload.get("tool_input") or {}).get("command", "") or ""
    if not is_commit(cmd) or OPT_OUT.search(cmd):
        return 0

    try:
        root = project_root()
        staged = [p for p in git(root, "diff", "--cached", "--name-only").splitlines() if p]
        if not staged:
            return 0
        versioned = set()
        for p in staged:
            if p.startswith(".corpus-management/"):
                continue
            # Generated artefacts carry their own Version lines but are REGENERATED, never hand-bumped
            # (gates 33/34/85 check them); a regenerated scorecard row is not a body edit to bump.
            if p in GENERATED:
                continue
            f = root / p
            try:
                if f.suffix == ".md" and VERSION_LINE.search(f.read_text(errors="replace")):
                    versioned.add(p)
            except OSError:
                continue
        # UTC-rollover co-bump NOTE (non-blocking): covers README's different Version key too.
        try:
            md = sorted(p for p in staged if p.endswith(".md") and p not in GENERATED
                        and not p.startswith(".corpus-management/"))
            if md:
                today_note = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                vdiff = git(root, "diff", "--cached", "--unified=0", "--", *md)
                texts = {p: git(root, "show", f":{p}") for p in md}
                lag = stale_date_after_bump(vdiff, texts, today_note)
                if lag:
                    print("NOTE (version-bump guard): a staged Version/README Version change carries a "
                          f"**Date:** that is not today UTC ({today_note}): {', '.join(lag)}. Co-bump the "
                          "Date in THIS commit (a later Date-only commit fails gate 40); D4 blocks at push.",
                          file=sys.stderr)
        except Exception:
            pass
        if not versioned:
            return 0
        diff = git(root, "diff", "--cached", "--unified=0", "--", *sorted(versioned))
        bad = offenders(diff, versioned)
    except Exception:
        return 0  # fail OPEN, deliberately: see the module docstring

    if not bad:
        # The sixth-instance shape: a versioned corpus document staged without its derived
        # artefacts. This does NOT verify a Version actually moved (a Date-only staged change can
        # trigger it). A WARNING, not a block: regeneration order matters, and the generated artefacts
        # can be staged alongside the document without unstaging it.
        moved = [p for p in versioned if "/" in p and not p.startswith((".working/", ".claude/"))]
        exec_pages = [p for p in moved if p.startswith("executive/")]
        corpus_pages = [p for p in moved if not p.startswith("executive/")]
        if corpus_pages and not any(g in staged for g in TAXONOMY_GENERATED):
            print("NOTE (version-bump guard): a versioned corpus document is staged and none of "
                  f"{', '.join(TAXONOMY_GENERATED)} is staged. If this document feeds the taxonomy, "
                  "run `python3 tools/build-taxonomy.py` FIRST, then build-portal.py, and stage both. "
                  "Gate 33 catches it otherwise, six minutes from now.", file=sys.stderr)
        if exec_pages and not any(g in staged for g in NARRATIVE_GENERATED):
            print("NOTE (version-bump guard): a versioned executive/ page is staged and narrative.yml "
                  "is not staged. Run `python3 tools/build-narrative-registry.py` and stage it. "
                  "Gate 85 catches it otherwise, six minutes from now.", file=sys.stderr)
        return 0

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    fixed, remaining = [], []
    for p in bad:
        (fixed if try_auto_bump(root, p, today) else remaining).append(p)
    if fixed:
        print("NOTE (version-bump guard): auto-bumped **Version:** (patch), set the first date-shaped "
              f"**Date:** before the metadata-region end to {today} if one exists, and re-staged: "
              f"{', '.join(fixed)}. A PATCH "
              "bump is assumed; if a minor/major is intended, edit **Version:** yourself and re-commit.",
              file=sys.stderr)
    if not remaining:
        return 0

    lines = [
        "BLOCKED (unbumped-version-commit): a commit containing staged file(s) with a changed BODY, no "
        "staged `**Version:**` line addition/removal, and an unsuccessful auto-bump (other unstaged changes "
        "present, no numeric Version match before the metadata-region end such as a bracketed template, or an exception during the attempt):",
        "",
    ]
    lines += [f"  - {p}" for p in remaining]
    lines += [
        "",
        "WHY: a body change without a Version+Date bump trips the delta gates (D2 on a body change "
        "without a Version, D4 on a Version without a matching Date) and gate 40 (a later Date-only "
        "commit is itself a body change post-dating the bump); this fires at commit time rather than "
        "at the pre-push guard six minutes later.",
        "",
        "CONSIDER INSTEAD: bump `**Version:**` AND `**Date:**` in the SAME edit, then re-stage. If "
        "this body edit genuinely does not warrant a bump, include `VersionBump: none <reason>` in the "
        "commit COMMAND text (e.g. an inline `-m` message; a `-F` message file is not inspected) and it "
        "will proceed.",
    ]
    print("\n".join(lines), file=sys.stderr)
    return 2


def self_test() -> int:
    cases, fails = 0, []

    def ck(name, got, want):
        nonlocal cases
        cases += 1
        if got != want:
            fails.append(f"{name}: {got!r} != {want!r}")
        print(f"  {'PASS' if got == want else 'FAIL'}: {name}")

    # --- command recognition ---
    ck("a plain git commit is in scope", is_commit("git -C /r commit -q -m x"), True)
    ck("a heredoc commit is in scope", is_commit("git -C /r commit -q -F -"), True)
    ck("--amend is deliberately out of scope", is_commit("git commit --amend --no-edit"), False)
    ck("git status is not a commit", is_commit("git -C /r status --short"), False)
    ck("a commit inside a chain is still a commit",
       is_commit("python3 tools/preflight-changelog.py && git -C /r commit -q -m x"), True)

    # --- the opt-out ---
    ck("the opt-out phrase is recognized", bool(OPT_OUT.search("m 'x\n\nVersionBump: none typo only'")), True)
    ck("a mention of versions is not an opt-out", bool(OPT_OUT.search("bump the version")), False)

    # --- THE REALITY FIXTURE: the actual 2026-07-26 miss, the spec body edited with no bump ---
    real = (
        "diff --git a/governance/specification-audit-programme.md b/governance/specification-audit-programme.md\n"
        "--- a/governance/specification-audit-programme.md\n"
        "+++ b/governance/specification-audit-programme.md\n"
        "@@ -197,1 +197,1 @@\n"
        "-the sibling-free portability check (section 1.19.1) leaves\n"
        "+the sibling-free portability check (PR #993) leaves\n")
    ck("the real 2026-07-26 miss is caught",
       offenders(real, {"governance/specification-audit-programme.md"}),
       ["governance/specification-audit-programme.md"])

    # --- the same edit WITH the bump staged: must not fire ---
    fixed = real + (
        "@@ -5,2 +5,2 @@\n"
        "-**Version:** 1.17.29\\\n"
        "+**Version:** 1.17.30\\\n"
        "-**Date:** 2026-07-25\\\n"
        "+**Date:** 2026-07-26\\\n")
    ck("the same edit with the bump staged does NOT fire",
       offenders(fixed, {"governance/specification-audit-programme.md"}), [])

    # --- a metadata-only change must not demand a bump (false-positive guard) ---
    meta_only = (
        "diff --git a/x.md b/x.md\n@@ -3,1 +3,1 @@\n"
        "-**Date:** 2026-07-25\\\n+**Date:** 2026-07-26\\\n")
    ck("a Date-only edit does not demand a bump", offenders(meta_only, {"x.md"}), [])

    # --- an unversioned file is out of scope even with a big body change ---
    unver = "diff --git a/notes.txt b/notes.txt\n@@ -1,1 +1,1 @@\n-old body\n+new body\n"
    ck("an unversioned file is out of scope", offenders(unver, set()), [])

    # --- multi-file: only the offending one is named ---
    multi = real + (
        "diff --git a/ok.md b/ok.md\n@@ -1,2 +1,2 @@\n"
        "-**Version:** 1.0.0\\\n+**Version:** 1.0.1\\\n-body\n+body two\n")
    ck("only the offending file of two is named",
       offenders(multi, {"governance/specification-audit-programme.md", "ok.md"}),
       ["governance/specification-audit-programme.md"])

    # --- classify_hunk directly, both halves independently ---
    ck("classify: body only", classify_hunk(["-a", "+b"]), (True, False))
    ck("classify: version only", classify_hunk(["-**Version:** 1\\", "+**Version:** 2\\"]), (False, True))
    ck("classify: both", classify_hunk(["-a", "+b", "+**Version:** 2\\"]), (True, True))
    ck("classify: blank added line is not a body change", classify_hunk(["+   "]), (False, False))
    ck("classify: diff headers are ignored",
       classify_hunk(["diff --git a/x b/x", "--- a/x", "+++ b/x", "@@ -1 +1 @@"]), (False, False))

    # --- 3.134 auto-bump: pure helpers ---
    ck("bump_semver patches Z", bump_semver("**Version:** 1.2.3\\\nbody"), "**Version:** 1.2.4\\\nbody")
    ck("bump_semver keeps trailing text", bump_semver("**Version:** 1.10.87 (per-doc)\\"), "**Version:** 1.10.88 (per-doc)\\")
    ck("bump_semver returns None on a bracketed-template Version", bump_semver("**Version:** <x.y.z: new docs start at 0.0.1>\\"), None)
    ck("bump_semver returns None with no Version line", bump_semver("just body text"), None)
    ck("bump_semver ignores a fenced/body Version example (F1 hardening)",
       bump_semver("**README Version:** 9.9.9\\\n\nbody\n\n```\n**Version:** 1.0.0\n```\n"), None)
    ck("bump_semver still bumps a real metadata Version above a body example",
       bump_semver("**Version:** 2.3.4\\\n\nbody\n\n```\n**Version:** 1.0.0\n```\n"),
       "**Version:** 2.3.5\\\n\nbody\n\n```\n**Version:** 1.0.0\n```\n")
    ck("set_date rewrites the Date", set_date("**Date:** 2026-07-01\\", "2026-07-29"), "**Date:** 2026-07-29\\")
    ck("set_date is a no-op with no Date line", set_date("**Version:** 1.0.0\\", "2026-07-29"), "**Version:** 1.0.0\\")

    # --- 3.134 auto-bump: git-fixture behaviour ---
    import tempfile
    def mkrepo():
        d = Path(tempfile.mkdtemp())
        git(d, "init", "-q")
        git(d, "config", "user.email", "t@t")
        git(d, "config", "user.name", "t")
        return d
    # clear offender -> auto-bumped + re-staged
    d = mkrepo()
    (d / "x.md").write_text("**Version:** 1.0.0\\\n**Date:** 2026-07-01\\\n\nold body\n")
    git(d, "add", "x.md"); git(d, "commit", "-q", "-m", "init")
    (d / "x.md").write_text("**Version:** 1.0.0\\\n**Date:** 2026-07-01\\\n\nnew body\n")
    git(d, "add", "x.md")  # stage the body change with NO version bump
    ck("clear offender auto-bumps", try_auto_bump(d, "x.md", "2026-07-29"), True)
    ck("auto-bumped Version is staged", "**Version:** 1.0.1" in git(d, "show", ":x.md"), True)
    ck("auto-bumped Date is staged", "**Date:** 2026-07-29" in git(d, "show", ":x.md"), True)
    # --- 3b24 (#2496 r5 residue): no newline translation anywhere on the auto-bump path ---
    dc = mkrepo()
    (dc / "c.md").write_bytes(b"**Version:** 1.0.0\\\r\n**Date:** 2026-07-01\\\r\n\r\nold body\r\n")
    git(dc, "add", "c.md"); git(dc, "commit", "-q", "-m", "init")
    (dc / "c.md").write_bytes(b"**Version:** 1.0.0\\\r\n**Date:** 2026-07-01\\\r\n\r\nnew body\r\n")
    git(dc, "add", "c.md")
    ck("a CRLF offender auto-bumps", try_auto_bump(dc, "c.md", "2026-07-29"), True)
    ck("the auto-bump keeps CRLF line endings",
       (dc / "c.md").read_bytes(), b"**Version:** 1.0.1\\\r\n**Date:** 2026-07-29\\\r\n\r\nnew body\r\n")
    dr = mkrepo()
    (dr / "r.md").write_bytes(b"line one\rstill line one\n")
    git(dr, "add", "r.md"); git(dr, "commit", "-q", "-m", "init")
    ck("git() returns a lone CR untranslated", "one\rstill" in git(dr, "show", "HEAD:r.md"), True)
    # unstaged changes present -> ambiguous -> not auto-bumped
    d2 = mkrepo()
    (d2 / "y.md").write_text("**Version:** 2.0.0\\\n\nbody\n")
    git(d2, "add", "y.md"); git(d2, "commit", "-q", "-m", "init")
    (d2 / "y.md").write_text("**Version:** 2.0.0\\\n\nstaged body\n"); git(d2, "add", "y.md")
    (d2 / "y.md").write_text("**Version:** 2.0.0\\\n\nUNSTAGED further edit\n")  # extra unstaged change
    ck("offender with other unstaged changes is NOT auto-bumped (block fallback)", try_auto_bump(d2, "y.md", "2026-07-29"), False)
    # a different key (**Library Version:**) -> no SEMVER_VERSION match -> try_auto_bump returns False;
    # main also excludes it from versioned eligibility
    d3 = mkrepo()
    (d3 / "z.md").write_text("**Library Version:** 2026.07.725\\\n\nbody\n")
    git(d3, "add", "z.md"); git(d3, "commit", "-q", "-m", "init")
    (d3 / "z.md").write_text("**Library Version:** 2026.07.725\\\n\nnew body\n"); git(d3, "add", "z.md")
    ck("direct try_auto_bump returns False for a Library-Version-only file (no SEMVER_VERSION match)", try_auto_bump(d3, "z.md", "2026-07-29"), False)

    # --- 2026-09-24: UTC-rollover co-bump NOTE (pure helper) ---
    rd = ("diff --git a/README.md b/README.md\n@@ -2,1 +2,1 @@\n"
          "-**README Version:** 1.11.282 (x)\n+**README Version:** 1.11.283 (x)\n")
    ck("README Version bump with a stale Date is reported",
       stale_date_after_bump(rd, {"README.md": "**Date:** 2026-09-23\\\n**README Version:** 1.11.283 (x)\\\n"}, "2026-09-24"), ["README.md"])
    ck("README Version bump with today's Date is not reported",
       stale_date_after_bump(rd, {"README.md": "**Date:** 2026-09-24\\\n**README Version:** 1.11.283 (x)\\\n"}, "2026-09-24"), [])
    ck("a body-only change is not reported",
       stale_date_after_bump("diff --git a/x.md b/x.md\n@@ -1 +1 @@\n-a\n+b\n", {"x.md": "**Date:** 2026-01-01\\\n"}, "2026-09-24"), [])
    ck("a Version bump on a file with no Date line is not reported",
       stale_date_after_bump("diff --git a/y.md b/y.md\n@@ -1 +1 @@\n-**Version:** 1.0.0\n+**Version:** 1.0.1\n", {"y.md": "no date"}, "2026-09-24"), [])
    # --- 2026-09-24 r1: a body/fenced Version example change is not a header bump ---
    ex = ("diff --git a/e.md b/e.md\n@@ -30,1 +30,1 @@\n-**Version:** 1.0.0\n+**Version:** 1.0.1\n")
    ex_text = "**Version:** 3.0.0\\\n**Date:** 2026-01-01\\\n\n---\n\nbody\n\n```\n**Version:** 1.0.1\n```\n"
    ck("a body Version example change is not reported", stale_date_after_bump(ex, {"e.md": ex_text}, "2026-09-24"), [])
    # --- 2026-09-24 r2 (codex): a fenced example whose NEW value equals the unchanged header Version ---
    col = ("diff --git a/c.md b/c.md\n@@ -9,1 +9,1 @@\n-**Version:** 2.9.9\n+**Version:** 3.0.0\n")
    col_text = "**Version:** 3.0.0\\\n**Date:** 2026-01-01\\\n\n---\n\nbody\n\n```\n**Version:** 3.0.0\n```\n"
    ck("a fenced example colliding with the header Version text is not reported", stale_date_after_bump(col, {"c.md": col_text}, "2026-09-24"), [])
    hdr = ("diff --git a/h.md b/h.md\n@@ -1,1 +1,1 @@\n-**Version:** 2.9.9\n+**Version:** 3.0.0\n")
    ck("a header-position Version bump with a stale Date is reported", stale_date_after_bump(hdr, {"h.md": col_text}, "2026-09-24"), ["h.md"])
    # --- 2026-09-24 r3 (codex, gemini): U+2028 in the header must not shift the LF line count; an
    # added body line beginning '++' (rendered '+++') must still advance the new-file position ---
    u_text = "**Date:** 2026-01-01\n# t\u2028# c\u2028# c\n---\n**Version:** 1.0.1\n"
    u = ("diff --git a/u.md b/u.md\n@@ -4,1 +4,1 @@\n-**Version:** 1.0.0\n+**Version:** 1.0.1\n")
    ck("a U+2028 in the header does not pull a body Version line into it", stale_date_after_bump(u, {"u.md": u_text}, "2026-09-24"), [])
    pp_text = "**Date:** 2026-01-01\\\n**Version:** 3.0.0\\\n\n---\n\n++ note\n**Version:** 1.0.1\n"
    pp = ("diff --git a/p.md b/p.md\n--- a/p.md\n+++ b/p.md\n@@ -2,1 +2,2 @@\n-**Version:** 2.0.0\n+**Version:** 3.0.0\n+++ note\n")
    ck("a '+++' added body line in the hunk does not disturb a header bump", stale_date_after_bump(pp, {"p.md": pp_text}, "2026-09-24"), ["p.md"])
    # --- 2026-09-24 r4 (codex): the diff itself is split on LF only; a U+2028 inside a deleted line
    # must not fabricate a '+++' line that shifts a real header Version bump out of the header ---
    cx = ("diff --git a/x.md b/x.md\n--- a/x.md\n+++ b/x.md\n@@ -2,2 +2 @@\n"
          "-# title\u2028+++ note\n-**Version:** 1.0.0\n+**Version:** 1.0.1\n")
    ck("a U+2028 in a deleted line does not fabricate a '+++' line (header bump still reported)",
       stale_date_after_bump(cx, {"x.md": "**Date:** 2026-01-01\n**Version:** 1.0.1\n"}, "2026-09-24"), ["x.md"])
    ob = "diff --git a/a.md b/a.md\n@@ -1 +1 @@\n-old\u2028diff --git a/x b/zz.md\n+new\n"
    ck("a U+2028 in a changed line does not fabricate a file header in the BLOCKING offender scan",
       offenders(ob, {"zz.md"}), [])
    mr = "**Date:** 2026-01-01\u2028note\n**Version:** 1.0.1\n\nbody\n"
    ck("the metadata region counts a U+2028-bearing line as ONE LF line", _metadata_region_end(mr), len("**Date:** 2026-01-01\u2028note\n**Version:** 1.0.1\n\n"))
    # --- 2026-09-24: generated-artefact exemption, end to end through main() in a scratch repo ---
    import shutil, subprocess, json as _json
    d5 = mkrepo()
    (d5 / ".claude" / "hooks").mkdir(parents=True)
    shutil.copy(__file__, d5 / ".claude" / "hooks" / "hook.py")
    (d5 / "docs").mkdir()
    (d5 / "docs" / "maturity-scorecard.md").write_text("**Version:** 1.0.0\\\n\n| row | old |\n")
    (d5 / "x.md").write_text("**Version:** 1.0.0\\\n\nold body\n")
    git(d5, "add", "-A"); git(d5, "commit", "-q", "-m", "init")
    (d5 / "docs" / "maturity-scorecard.md").write_text("**Version:** 1.0.0\\\n\n| row | new |\n")
    git(d5, "add", "docs/maturity-scorecard.md")
    # an extra UNSTAGED scorecard change makes auto-bump decline, so without the exemption this would BLOCK
    (d5 / "docs" / "maturity-scorecard.md").write_text("**Version:** 1.0.0\\\n\n| row | newer |\n")
    payload = _json.dumps({"tool_name": "Bash", "tool_input": {"command": f"git -C {d5} commit -q -m x"}})
    r = subprocess.run([sys.executable, "-B", str(d5 / ".claude" / "hooks" / "hook.py")], input=payload,
                       capture_output=True, text=True)
    ck("a regenerated scorecard body edit is NOT blocked", r.returncode, 0)
    # control: an ordinary versioned doc with an extra unstaged change still blocks
    (d5 / "x.md").write_text("**Version:** 1.0.0\\\n\nnew body\n"); git(d5, "add", "x.md")
    (d5 / "x.md").write_text("**Version:** 1.0.0\\\n\nnewer unstaged\n")
    r2 = subprocess.run([sys.executable, "-B", str(d5 / ".claude" / "hooks" / "hook.py")], input=payload,
                        capture_output=True, text=True)
    ck("control: an ordinary versioned doc still blocks", r2.returncode, 2)

    if fails:
        print(f"\nself-test: FAILED ({len(fails)} of {cases})")
        for f in fails:
            print(f"  {f}")
        return 1
    print(f"\nself-test: {cases}/{cases} passed")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if "--self-test" in sys.argv else main())
