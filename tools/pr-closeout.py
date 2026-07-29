#!/usr/bin/env python3
"""PR close-out scaffolding (TODO 3.133).

Mechanizes the per-PR bookkeeping half of a close-out so the orchestrator stops
hand-editing the same set of surfaces after every merge. It computes the merge
SHA / base SHA / CI state for the just-merged PR, EMITS the newest-first
close-out rows and the forward CHANGELOG/README edits at their correct insert
points, and (only under --apply) performs guarded, idempotent, in-place writes.

Two PR identities, distinct by design (history proves a merged PR's close-out is
NOT written in that PR: the retro / validate rows can only exist after the merge,
and the recursion-avoidance rule holds their commit to the following PR):

  * positional N  = the just-merged PR. Subject of the BACKWARD close-out rows
    (merge-bypass-log, validate-pr history + optional detail file, improvement
    log). Everything about N is auto-derived: merge SHA, base SHA, CI state, N.
  * --this-pr M   = the batch PR being assembled. Subject of the FORWARD release
    surfaces (README Library + README Version + Date, CHANGELOG root + detailed
    mirror). Default M = N + 1 with a loud caveat that it is a GUESS until the PR
    exists (GitHub assigns the number at `gh pr create`).

--closeout-only writes just the backward rows (the biggest lever), leaving the
forward README/CHANGELOG bump to the existing hand edit.

Default mode is PREVIEW (dry-run): it prints, per surface, the rendered row /
entry template, the exact insert anchor, and a unified diff, and writes nothing.
This is the reviewable artefact. Pass --apply to mutate. Every write is guarded
(insert only under a recognized header, never re-matching a data row), idempotent
(a row / entry already present for the PR is a no-op, and the Version bump is
coupled to a successful insert), and fail-loud (an unrecognized surface shape or a
missing judgement arg under --apply stops the run and names the file, rather than
guessing an insert point: silence-reads-as-health is the failure class this repo
most aggressively rejects).

The tool mechanizes PLACEMENT, VERSION BUMPS, and FORMAT only. Every piece of
judgement (the summary prose, the validate-pr verdict + findings, the retro
analysis, the bypass justification) is an orchestrator-supplied arg. In preview
mode a missing judgement field renders a grep-able TODO marker so the orchestrator
can see exactly what is left to fill; under --apply a missing field is refused
unless --allow-placeholders is passed.

Which surfaces carry a Version field is DERIVED from each file, never hardcoded:
the three backward ledgers are append-only and version-exempt (TODO 3.135), so the
tool bumps a ledger's Version + Date only if the file actually carries a Version
head field. Today that means README.md is the only versioned surface it bumps; if
the exemption is ever reverted the tool bumps the ledgers again with no code change.

Stdlib-only, Python 3.11. Advisory exit-0 like tools/collect-deliveries.py: the
git/gh derivation degrades gracefully to placeholders when the tools are absent,
and preview + apply exit 0 on success or a full no-op.

Exit codes:
    0 : previewed, applied, or a fully-idempotent no-op
    1 : --self-test failed (the only path that fails on a pure-logic fault)
    2 : invocation error (argparse)
    3 : under --apply, a surface was in an unexpected shape (header not found), a
        required judgement arg was missing, or a bypass row was requested on a
        non-green PR without --allow-red. Nothing written.
"""
from __future__ import annotations

import argparse
import datetime
import difflib
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Reuse the shared metadata helpers rather than re-deriving the field regex.
from lint_common import REPO_ROOT, parse_metadata_block, resolve_working, resolve_working_for_write  # noqa: F401  (REPO_ROOT rebindable in --self-test)

# --------------------------------------------------------------------------
# Surface locations (relative to REPO_ROOT).
# --------------------------------------------------------------------------
BYPASS_LOG = ".working/merge-bypass-log.md"
VALIDATE_HISTORY = ".working/validate-pr/history.md"
VALIDATE_DETAIL_DIR = ".working/validate-pr"
IMPROVEMENT_LOG = ".working/improvement-log.md"
README = "README.md"
CHANGELOG = "CHANGELOG.md"
CHANGELOG_DETAILED = ".working/changelog-details/CHANGELOG-detailed.md"

# Header signatures. The insert anchors on THESE lines and appends after them
# (skipping a separator row if one follows); it never re-matches a data row's
# leading cells, which is the fused-row mitigation.
BYPASS_HEADER = "| Date (UTC) | PR |"
VALIDATE_HEADER = "| Date | PR | Touched files |"
IMPROVEMENT_HEADER = "| Date | PR | FR closed |"

# A markdown table separator row: | --- | --- | ... (optional colons).
SEPARATOR_RE = re.compile(r"^\s*\|(\s*:?-{3,}:?\s*\|)+\s*$")

# CHANGELOG entry anchors: the first entry line of each file. A new entry is
# placed immediately before it. The two files have DIFFERENT entry shapes, so the
# anchor is passed per surface (the root uses `**date | ver | PR #M**`, the mirror
# uses `## date, Library Version ver, PR #M (...)`).
CHANGELOG_ROOT_ANCHOR = re.compile(r"^\*\*\d{4}-\d{2}-\d{2} \|")
CHANGELOG_DETAILED_ANCHOR = re.compile(r"^## \d{4}-\d{2}-\d{2}, Library Version ")

DEFAULT_MECHANISM = "`gh pr merge --admin --squash --delete-branch`"
DEFAULT_MODE = "offloaded to an exec'd worker, READ-ONLY, refute-briefed"
PLACEHOLDER = "<!-- TODO(orchestrator): fill {field} -->"
UNKNOWN = "UNKNOWN (derive by hand)"


class SurfaceShapeError(Exception):
    """A surface did not carry the expected header / anchor. Fail loud."""


class WorkingStateUnavailable(Exception):
    """A mandatory EXISTING maintainer working-state surface is unavailable
    (neither the private sibling nor an in-repo .working/ holds it). Fail loud
    rather than recreate a public .working/ tree or crash on a missing path."""


def existing_working_path(rel: str) -> Path:
    """Resolve a MANDATORY existing .working/-tree surface for READING, via the
    read resolver (private sibling then in-repo). Raise WorkingStateUnavailable
    when it is absent, so a caller fails cleanly instead of crashing on a missing
    public path or recreating public working state via the write resolver."""
    path = resolve_working(rel[len(".working/"):], repo_root=REPO_ROOT)
    if path is None or not path.is_file():
        raise WorkingStateUnavailable(rel)
    return path


class MissingJudgement(Exception):
    """A required orchestrator-authored field was empty under --apply."""

    def __init__(self, field_name: str) -> None:
        super().__init__(field_name)
        self.field_name = field_name


# --------------------------------------------------------------------------
# Pure version arithmetic.
# --------------------------------------------------------------------------
def bump_semver(current: str) -> str:
    """PURE. Bump the patch of an x.y.z semantic version."""
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", current.strip())
    if not m:
        raise ValueError(f"not a semver: {current!r}")
    return f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"


def bump_calver(current: str, today: datetime.date) -> str:
    """PURE. Month-aware library CalVer bump (spec-master 4.5).

    Same YYYY.MM window -> patch + 1. Month (or year) rollover -> today's YYYY.MM.0.
    The tool bumps from what is WRITTEN, never from a recomputed merge count, so it
    can never go backwards even though the true merge sequence has gaps.
    """
    m = re.fullmatch(r"(\d{4})\.(\d{2})\.(\d+)", current.strip())
    if not m:
        raise ValueError(f"not a CalVer YYYY.MM.patch: {current!r}")
    year, month, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if (today.year, today.month) == (year, month):
        return f"{year:04d}.{month:02d}.{patch + 1}"
    return f"{today.year:04d}.{today.month:02d}.0"


# --------------------------------------------------------------------------
# Pure metadata-field editing (version / date TOKEN, head window only).
# --------------------------------------------------------------------------
def read_head_field(text: str, field_name: str) -> str | None:
    """PURE. The head-window value of **Field:**, or None. The trailing hard-break
    backslash is already stripped by parse_metadata_block; any parenthetical
    annotation stays ON the value and the caller extracts the leading token."""
    return parse_metadata_block(text).fields.get(field_name)


def _version_token(value: str) -> str:
    """PURE. First whitespace-delimited token of a field value.

    '2026.07.704 (CalVer, ...)' -> '2026.07.704'; '1.10.65 (semantic ...)' -> '1.10.65'.
    """
    parts = value.split()
    return parts[0] if parts else ""


def replace_head_token(text: str, field_name: str, old_token: str, new_token: str) -> str:
    """PURE. Replace exactly one version/date TOKEN inside the first head-window
    **Field:** line, preserving the parenthetical suffix and trailing backslash.

    Only the first line whose lstrip starts with the exact `**Field:**` marker (and
    that carries old_token) is touched, so a sibling field (README Version vs
    Library Version) and any body line shaped like a metadata field are left alone.
    """
    lines = text.split("\n")
    marker = f"**{field_name}:**"
    for i, line in enumerate(lines):
        if line.lstrip().startswith(marker) and old_token in line:
            lines[i] = line.replace(old_token, new_token, 1)
            return "\n".join(lines)
    raise SurfaceShapeError(
        f"head-window field {field_name!r} carrying token {old_token!r} not found")


def set_date(text: str, today: datetime.date) -> str:
    """PURE. Set the head-window **Date:** token to today (idempotent, D4 co-bump).

    A file with no Date field is returned unchanged (the append-only ledgers)."""
    old = read_head_field(text, "Date")
    if old is None:
        return text
    old_token = _version_token(old)
    if old_token == today.isoformat():
        return text
    return replace_head_token(text, "Date", old_token, today.isoformat())


# --------------------------------------------------------------------------
# Pure table-cell safety: prose cells must never introduce an unescaped pipe or a
# newline, either of which fuses or splits a ledger column.
# --------------------------------------------------------------------------
def escape_cell(value: str) -> str:
    """PURE. Collapse whitespace (killing embedded newlines) and escape any
    unescaped pipe, so orchestrator prose is safe inside a markdown table cell.
    Idempotent: an already-escaped `\\|` is left as-is."""
    collapsed = re.sub(r"\s+", " ", value).strip()
    return re.sub(r"(?<!\\)\|", lambda _m: "\\|", collapsed)


# --------------------------------------------------------------------------
# Pure newest-first idempotent row insertion.
# --------------------------------------------------------------------------
def _pr_cell(row: str, index: int) -> str:
    """PURE. The stripped Nth interior cell of a pipe row (0-based)."""
    parts = [c.strip() for c in row.strip().strip("|").split("|")]
    return parts[index] if 0 <= index < len(parts) else ""


def insert_row(text: str, header_signature: str, new_row: str, *,
               pr_token: str, pr_col: int) -> tuple[str, bool]:
    """PURE. Insert new_row newest-first under the table whose header line CONTAINS
    header_signature. Skip a separator row if one follows the header. Refuse (no
    change, inserted=False) if a contiguous body row already carries pr_token in
    column pr_col.

    Raises SurfaceShapeError if the header is not found: an unknown surface shape
    fails loud rather than inserting at a guessed offset.
    """
    lines = text.split("\n")
    hi = next((i for i, ln in enumerate(lines) if header_signature in ln), None)
    if hi is None:
        raise SurfaceShapeError(f"table header {header_signature!r} not found")
    at = hi + 1
    if at < len(lines) and SEPARATOR_RE.match(lines[at]):
        at += 1
    j = at
    while j < len(lines) and lines[j].lstrip().startswith("|"):
        if _pr_cell(lines[j], pr_col) == pr_token:
            return text, False
        j += 1
    lines.insert(at, new_row)
    return "\n".join(lines), True


def insert_changelog_entry(text: str, entry_block: str, *,
                           anchor: re.Pattern, batch_pr: int) -> tuple[str, bool]:
    """PURE. Insert entry_block newest-first, immediately before the first line
    matching `anchor` (the current top entry), blank-line separated. Idempotent on
    a word-bounded `PR #<batch_pr>` already present anywhere in the file, so PR #121
    is never mistaken for a match inside PR #1214.

    Raises SurfaceShapeError if no anchor line is found.
    """
    if re.search(rf"PR #{batch_pr}\b", text):
        return text, False
    lines = text.split("\n")
    at = next((i for i, ln in enumerate(lines) if anchor.match(ln)), None)
    if at is None:
        raise SurfaceShapeError(f"no CHANGELOG entry anchor /{anchor.pattern}/ found")
    block = entry_block.rstrip("\n").split("\n") + [""]
    lines[at:at] = block
    return "\n".join(lines), True


# --------------------------------------------------------------------------
# The close-out spec: judgement flows in here; renderers stay pure.
# --------------------------------------------------------------------------
@dataclass
class CloseoutSpec:
    merged_pr: int
    batch_pr: int
    date: datetime.date
    merge_sha: str
    base_sha: str
    ci_state: str
    # judgement (orchestrator-authored)
    summary: str = ""
    verdict: str = ""
    findings: list[str] = field(default_factory=list)
    touched: str = ""
    justification: str = ""
    change: str = ""
    mechanism: str = DEFAULT_MECHANISM
    mode: str = DEFAULT_MODE
    hotfix: str = "none"
    fr_closed: str = "none"
    retro_well: str = ""
    retro_friction: str = ""
    retro_pattern: str = ""
    retro_proposed: str = ""
    title: str = ""
    allow_placeholders: bool = False

    def need(self, value: str, name: str) -> str:
        """A required judgement field: return it, or a loud placeholder / refusal."""
        if value:
            return value
        if self.allow_placeholders:
            return PLACEHOLDER.format(field=name)
        raise MissingJudgement(name)

    @property
    def d(self) -> str:
        return self.date.isoformat()

    @property
    def has_findings(self) -> bool:
        # A "PASS / CLEAN, 0 findings" verdict leaves just the history row.
        return bool(self.findings)


def render_bypass_row(s: CloseoutSpec) -> str:
    return ("| {d} | #{pr} | {ci} | {mech} | {just} | {change} |").format(
        d=s.d, pr=s.merged_pr, ci=escape_cell(s.ci_state), mech=escape_cell(s.mechanism),
        just=escape_cell(s.need(s.justification, "justification")),
        change=escape_cell(s.need(s.change or s.summary, "change")))


def render_validate_row(s: CloseoutSpec) -> str:
    detail = (f"[{s.d}-PR-{s.merged_pr}.md]({s.d}-PR-{s.merged_pr}.md)"
              if s.has_findings else "none")
    findings_cell = escape_cell(s.need(s.verdict, "verdict"))
    if s.findings:
        findings_cell += " " + escape_cell(" ".join(s.findings))
    return ("| {d} | {pr} | {touched} | {findings} | {hotfix} | {detail} | {summary} |").format(
        d=s.d, pr=s.merged_pr, touched=escape_cell(s.need(s.touched, "touched")),
        findings=findings_cell, hotfix=escape_cell(s.hotfix), detail=detail,
        summary=escape_cell(s.need(s.summary, "summary")))


def render_retro_row(s: CloseoutSpec) -> str:
    # Pattern and Proposed cells are legitimately empty on most PRs.
    return ("| {d} | #{pr} | {fr} | {well} | {fric} | {pat} | {prop} |").format(
        d=s.d, pr=s.merged_pr, fr=escape_cell(s.fr_closed),
        well=escape_cell(s.need(s.retro_well, "retro-well")),
        fric=escape_cell(s.need(s.retro_friction, "retro-friction")),
        pat=escape_cell(s.retro_pattern), prop=escape_cell(s.retro_proposed))


def render_detail_file(s: CloseoutSpec) -> str:
    """SCAFFOLD ONLY. Live detail files are free-form worker deliverables (they open
    `# Result: validate-pr-<N>`), so this is a best-effort skeleton the orchestrator
    replaces, not a confirmed schema. It exists so a findings sweep is never left
    with a dangling Detail link and no file."""
    bullets = "\n".join(f"- {escape_pipes_only(f)}" for f in s.findings) or "- (none recorded)"
    return (f"# validate-pr: PR #{s.merged_pr}\n\n"
            f"**Date:** {s.d} (UTC)\\\n"
            f"**PR:** #{s.merged_pr} (squash `{s.merge_sha}`, base `{s.base_sha}`)\\\n"
            f"**Mode:** {s.mode}\\\n"
            f"**Verdict:** {s.need(s.verdict, 'verdict')}\n\n"
            f"## Scope\n\n{s.need(s.touched, 'touched')}\n\n"
            f"## Findings\n\n{bullets}\n\n"
            f"## Proof of run\n\n- {PLACEHOLDER.format(field='proof-of-run')}\n")


def escape_pipes_only(value: str) -> str:
    """PURE. Escape unescaped pipes without collapsing newlines (for prose bodies,
    not table cells)."""
    return re.sub(r"(?<!\\)\|", lambda _m: "\\|", value)


def render_changelog_root(s: CloseoutSpec, calver: str) -> str:
    return f"**{s.d} | {calver} | PR #{s.batch_pr}** - {s.need(s.summary, 'summary')}"


def render_changelog_detailed(s: CloseoutSpec, calver: str) -> str:
    title = s.title or PLACEHOLDER.format(field="title")
    batch = (f"- Batches PR #{s.merged_pr}'s `/validate-pr` + `/retro` rows "
             f"(recursion-avoidance)")
    if s.has_findings:
        batch += (f", plus the [{s.d}-PR-{s.merged_pr}.md]"
                  f"(../validate-pr/{s.d}-PR-{s.merged_pr}.md) detail file")
    batch += "."
    return (f"## {s.d}, Library Version {calver}, PR #{s.batch_pr} ({title})\n\n"
            f"{PLACEHOLDER.format(field='one-paragraph plain-language lead')}\n\n"
            f"### Changed\n\n- {PLACEHOLDER.format(field='detailed change bullets')}\n\n"
            f"### Verification\n\n"
            f"- {PLACEHOLDER.format(field='audit-suite + gates-run bullets')}\n"
            f"- Library and README Version + Date bumps recorded in README.md.\n"
            f"{batch}\n")


# --------------------------------------------------------------------------
# D7 length pre-check (warn before the CI gate does).
# --------------------------------------------------------------------------
def changelog_length_warnings(summary: str, word_max: int = 100,
                              sentence_max: int = 45) -> list[str]:
    """PURE. Mirror check-changelog-length-on-pr.py so a D7 problem shows at
    close-out time, not at push time."""
    warns: list[str] = []
    words = len(summary.split())
    if words > word_max:
        warns.append(f"summary is {words} words (> {word_max})")
    for sentence in re.split(r"(?<=[.!?])\s+", summary.strip()):
        n = len(sentence.split())
        if n > sentence_max:
            warns.append(f"a sentence runs {n} words (> {sentence_max}): {sentence[:50]!r}...")
    return warns


# --------------------------------------------------------------------------
# Auto-derivation (git / gh). Isolated so the pure core stays testable; degrades
# gracefully to placeholders when git/gh are absent (advisory, never fatal).
# --------------------------------------------------------------------------
def _run(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True, check=True,
                          cwd=REPO_ROOT).stdout.strip()


def derive_merge_and_base(pr: int) -> tuple[str, str, str | None]:
    """Return (merge_sha, base_sha, warning_or_None). Tries gh, then a git-log grep,
    then degrades to UNKNOWN placeholders with a warning."""
    try:
        oid = _run(["gh", "pr", "view", str(pr), "--json", "mergeCommit",
                    "--jq", ".mergeCommit.oid"])
        if oid:
            try:
                base = _run(["git", "rev-parse", "--short", f"{oid}~1"])
            except (subprocess.CalledProcessError, FileNotFoundError):
                base = UNKNOWN
            return oid[:8], base or UNKNOWN, None
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    try:
        oid = _run(["git", "log", "--grep", f"(#{pr})", "-1", "--format=%H"])
        if oid:
            try:
                base = _run(["git", "rev-parse", "--short", f"{oid}~1"])
            except (subprocess.CalledProcessError, FileNotFoundError):
                base = UNKNOWN
            return oid[:8], base, None
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return (UNKNOWN, UNKNOWN,
            f"could not derive merge/base SHA for #{pr} (gh/git unavailable); "
            f"templates carry {UNKNOWN} placeholders")


def derive_ci_state(pr: int) -> tuple[str, bool | None, str | None]:
    """Return (ci_cell, all_green_or_None, warning_or_None). all_green is None when
    the state could not be read (degraded)."""
    try:
        raw = _run(["gh", "pr", "checks", str(pr)])
    except (subprocess.CalledProcessError, FileNotFoundError):
        return (UNKNOWN, None,
                f"could not read CI checks for #{pr}; CI cell carries a placeholder")
    rows = [ln.split("\t") for ln in raw.splitlines() if ln.strip()]
    if not rows:
        return (UNKNOWN, None, f"`gh pr checks {pr}` returned no rows; CI cell placeholder")
    names: list[str] = []
    all_green = True
    for cells in rows:
        name = cells[0] if cells else ""
        state = cells[1].lower() if len(cells) > 1 else ""
        elapsed = cells[2] if len(cells) > 2 else ""
        if state not in ("pass", "success", "neutral", "skipping"):
            all_green = False
        names.append(f"{name} {elapsed}".strip())
    tone = "all checks green" if all_green else "checks NOT all green"
    return (f"{tone} ({', '.join(names)}), via `gh pr checks {pr}`", all_green, None)


# --------------------------------------------------------------------------
# The plan: one edit per surface, previewed or applied uniformly.
# --------------------------------------------------------------------------
@dataclass
class Edit:
    path: Path
    before: str
    after: str
    note: str
    template: str = ""
    insert_desc: str = ""

    @property
    def changed(self) -> bool:
        return self.before != self.after


def build_plan(s: CloseoutSpec, *, closeout_only: bool,
               today: datetime.date) -> list[Edit]:
    edits: list[Edit] = []

    def bump_and_insert(rel: str, header_sig: str, row: str, pr_token: str) -> None:
        path = (existing_working_path(rel)
                if rel.startswith(".working/") else REPO_ROOT / rel)
        text = path.read_text(encoding="utf-8")
        new, inserted = insert_row(text, header_sig, row, pr_token=pr_token, pr_col=1)
        if inserted:
            ver = read_head_field(text, "Version")
            if ver:  # a versioned surface: bump Version + Date, coupled to the insert
                vtok = _version_token(ver)
                new = replace_head_token(new, "Version", vtok, bump_semver(vtok))
                new = set_date(new, today)
                note = f"row inserted; Version {vtok}->{bump_semver(vtok)} + Date bumped"
            else:  # append-only ledger (TODO 3.135): no Version/Date to bump
                note = "row inserted (append-only ledger: no Version/Date field to bump)"
        else:
            note = f"row already present for {pr_token} (idempotent no-op)"
        edits.append(Edit(path, text, new, note, template=row,
                          insert_desc=f"newest-first, after header {header_sig!r}"))

    # ---- Backward close-out rows (subject: merged PR N) ----
    bump_and_insert(BYPASS_LOG, BYPASS_HEADER, render_bypass_row(s), f"#{s.merged_pr}")
    bump_and_insert(VALIDATE_HISTORY, VALIDATE_HEADER, render_validate_row(s), str(s.merged_pr))
    bump_and_insert(IMPROVEMENT_LOG, IMPROVEMENT_HEADER, render_retro_row(s), f"#{s.merged_pr}")

    if s.has_findings:
        detail_rel = f"{VALIDATE_DETAIL_DIR[len('.working/'):]}/{s.d}-PR-{s.merged_pr}.md"
        detail_path = resolve_working(detail_rel, repo_root=REPO_ROOT)
        if detail_path is None:
            detail_path = resolve_working_for_write(detail_rel, repo_root=REPO_ROOT)
        before = detail_path.read_text(encoding="utf-8") if detail_path.exists() else ""
        after = before if before else render_detail_file(s)
        note = ("detail file already present (no-op)" if before
                else "detail file created (SCAFFOLD: confirm against a recent worker file)")
        try:
            _desc = str(detail_path.relative_to(REPO_ROOT))
        except ValueError:
            _desc = str(detail_path)  # resolved into the private sibling (post-migration)
        edits.append(Edit(detail_path, before, after, note,
                          template=("" if before else after),
                          insert_desc=_desc))

    if closeout_only:
        return edits

    # ---- Forward release surfaces (subject: batch PR M) ----
    readme_path = REPO_ROOT / README
    rtext = readme_path.read_text(encoding="utf-8")
    lib = _version_token(read_head_field(rtext, "Library Version") or "")
    rdme = _version_token(read_head_field(rtext, "README Version") or "")
    calver = bump_calver(lib, today) if lib else UNKNOWN
    changelog_text = (REPO_ROOT / CHANGELOG).read_text(encoding="utf-8")
    already = bool(re.search(rf"PR #{s.batch_pr}\b", changelog_text))
    if already:
        edits.append(Edit(readme_path, rtext, rtext,
                          f"README not bumped (PR #{s.batch_pr} already in CHANGELOG)"))
    else:
        new = rtext
        if lib:
            new = replace_head_token(new, "Library Version", lib, calver)
        if rdme:
            new = replace_head_token(new, "README Version", rdme, bump_semver(rdme))
        new = set_date(new, today)
        note = (f"Library {lib}->{calver}, "
                f"README {rdme}->{bump_semver(rdme) if rdme else '(none)'}, "
                f"Date->{today.isoformat()}")
        edits.append(Edit(readme_path, rtext, new, note))

    for rel, renderer, anchor in (
            (CHANGELOG, render_changelog_root, CHANGELOG_ROOT_ANCHOR),
            (CHANGELOG_DETAILED, render_changelog_detailed, CHANGELOG_DETAILED_ANCHOR)):
        path = (existing_working_path(rel)
                if rel.startswith(".working/") else REPO_ROOT / rel)
        text = path.read_text(encoding="utf-8")
        block = renderer(s, calver)
        new, inserted = insert_changelog_entry(text, block, anchor=anchor, batch_pr=s.batch_pr)
        edits.append(Edit(path, text, new,
                          "entry inserted" if inserted else "entry already present (no-op)",
                          template=block, insert_desc="newest-first, before the top entry"))
    return edits


def apply_edits(plan: list[Edit]) -> None:
    for e in plan:
        if e.changed:
            e.path.parent.mkdir(parents=True, exist_ok=True)
            e.path.write_text(e.after, encoding="utf-8")


def render_preview(plan: list[Edit]) -> None:
    print("PREVIEW (dry-run): nothing written. Re-run with --apply to write.\n")
    for e in plan:
        try:
            rel = e.path.relative_to(REPO_ROOT)
        except ValueError:
            rel = e.path  # resolved into the private sibling (post-migration)
        print(f"=== {rel}: {e.note} ===")
        if e.insert_desc:
            print(f"    insert point: {e.insert_desc}")
        if e.template.strip():
            print("    template:")
            for ln in e.template.split("\n"):
                print(f"      {ln}")
        if e.changed:
            diff = difflib.unified_diff(
                e.before.splitlines(), e.after.splitlines(),
                fromfile=str(rel), tofile=str(rel), lineterm="")
            print("\n".join(diff))
        print()


# --------------------------------------------------------------------------
# CLI.
# --------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("merged_pr", type=int, nargs="?",
                    help="the just-merged PR N (subject of the close-out rows)")
    ap.add_argument("--this-pr", type=int,
                    help="the batch PR M being assembled (default N+1, a guess)")
    ap.add_argument("--summary", default="", help="CHANGELOG summary for M (judgement)")
    ap.add_argument("--verdict", default="", help="validate-pr verdict (judgement)")
    ap.add_argument("--findings", action="append", default=[],
                    help="a validate-pr finding (repeatable); presence creates a detail file")
    ap.add_argument("--touched", default="", help="validate-pr touched-files cell (judgement)")
    ap.add_argument("--justification", default="", help="bypass justification (judgement)")
    ap.add_argument("--change", default="", help="bypass Change cell (default: --summary)")
    ap.add_argument("--mechanism", default=DEFAULT_MECHANISM)
    ap.add_argument("--mode", default=DEFAULT_MODE)
    ap.add_argument("--hotfix", default="none")
    ap.add_argument("--fr-closed", default="none")
    ap.add_argument("--retro-well", default="")
    ap.add_argument("--retro-friction", default="")
    ap.add_argument("--retro-pattern", default="")
    ap.add_argument("--retro-proposed", default="")
    ap.add_argument("--title", default="", help="detailed-CHANGELOG header parenthetical")
    ap.add_argument("--date", help="close-out date YYYY-MM-DD (default today UTC)")
    ap.add_argument("--closeout-only", action="store_true",
                    help="write only the backward rows; leave README/CHANGELOG manual")
    ap.add_argument("--apply", action="store_true",
                    help="mutate files in place (guarded, idempotent). Default is preview.")
    ap.add_argument("--dry-run", action="store_true",
                    help="force preview even if --apply is given (the default already)")
    ap.add_argument("--allow-red", action="store_true",
                    help="permit a bypass row on a non-green PR (maintainer reason required)")
    ap.add_argument("--allow-placeholders", action="store_true",
                    help="under --apply, write grep-able TODO markers for missing judgement")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)

    if a.self_test:
        return self_test()
    if a.merged_pr is None:
        ap.error("merged_pr is required unless --self-test")

    applying = a.apply and not a.dry_run
    today = (datetime.date.fromisoformat(a.date) if a.date
             else datetime.datetime.now(datetime.timezone.utc).date())
    batch_pr = a.this_pr if a.this_pr is not None else a.merged_pr + 1
    if a.this_pr is None and not a.closeout_only:
        print(f"note: --this-pr not given; ASSUMING batch PR #{batch_pr} (merged + 1). "
              f"This is a GUESS until the PR exists; pass --this-pr or correct the "
              f"CHANGELOG/README number after `gh pr create`.")

    merge_sha, base_sha, sha_warn = derive_merge_and_base(a.merged_pr)
    ci_state, ci_green, ci_warn = derive_ci_state(a.merged_pr)
    for w in (sha_warn, ci_warn):
        if w:
            print(f"warning: {w}")
    if ci_green is False:
        print(f"warning: #{a.merged_pr} is NOT all-green on CI. A bypass row on a red PR "
              f"skips the mechanical gates, which nothing in this project authorizes.")
        # A bypass row is written in every apply mode (both full and --closeout-only).
        if applying and not a.allow_red:
            print("error: refusing to APPLY a bypass row on a non-green PR without "
                  "--allow-red.", file=sys.stderr)
            return 3

    spec = CloseoutSpec(
        merged_pr=a.merged_pr, batch_pr=batch_pr, date=today,
        merge_sha=merge_sha, base_sha=base_sha, ci_state=ci_state,
        summary=a.summary, verdict=a.verdict, findings=a.findings, touched=a.touched,
        justification=a.justification, change=a.change, mechanism=a.mechanism, mode=a.mode,
        hotfix=a.hotfix, fr_closed=a.fr_closed, retro_well=a.retro_well,
        retro_friction=a.retro_friction, retro_pattern=a.retro_pattern,
        retro_proposed=a.retro_proposed, title=a.title,
        allow_placeholders=(not applying) or a.allow_placeholders)

    for w in changelog_length_warnings(a.summary):
        print(f"warning (D7): {w}")

    try:
        plan = build_plan(spec, closeout_only=a.closeout_only, today=today)
    except MissingJudgement as exc:
        print(f"error: missing judgement arg '{exc.field_name}'. Supply it, or re-run with "
              f"--allow-placeholders to scaffold a grep-able TODO marker.", file=sys.stderr)
        return 3
    except SurfaceShapeError as exc:
        print(f"error: a surface is in an unexpected shape: {exc}. Nothing written.",
              file=sys.stderr)
        return 3
    except WorkingStateUnavailable as exc:
        print(f"error: maintainer working state unavailable ({exc}); the private-sibling "
              f"working-state store is not accessible. Nothing written.", file=sys.stderr)
        return 3
    except OSError as exc:
        print(f"error: could not read a required close-out surface: {exc}. Nothing written.",
              file=sys.stderr)
        return 3

    if applying:
        apply_edits(plan)
        for e in plan:
            try:
                rel = e.path.relative_to(REPO_ROOT)
            except ValueError:
                rel = e.path  # resolved into the private sibling (post-migration)
            print(f"{'WROTE' if e.changed else 'SKIP '} {rel}: {e.note}")
    else:
        render_preview(plan)
    return 0


# --------------------------------------------------------------------------
# Self-test: pure functions, constructed fixtures, plus one tempfile end-to-end
# that pins the version-vs-unversioned branch. Each check pins WHICH position and
# WHAT value, never a bare boolean a sibling branch also produces. The count is
# len(checks), never a literal (the hardcoded-count class this repo has fixed).
# --------------------------------------------------------------------------
def self_test() -> int:
    from datetime import date
    import tempfile

    failures: list[str] = []
    total = [0]

    def check(name, got, want) -> None:
        total[0] += 1
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}: {name}"
              + ("" if ok else f" -> {got!r}, expected {want!r}"))
        if not ok:
            failures.append(name)

    # ---- version arithmetic ----
    check("semver bumps the patch", bump_semver("1.2.940"), "1.2.941")
    check("calver +1 within the same month", bump_calver("2026.07.704", date(2026, 7, 27)),
          "2026.07.705")
    check("calver resets to .0 on month rollover", bump_calver("2026.07.704", date(2026, 8, 1)),
          "2026.08.0")
    check("calver resets on year rollover too", bump_calver("2026.12.5", date(2027, 1, 3)),
          "2027.01.0")

    # ---- README token replacement: parenthetical + backslash preserved, sibling
    #      field untouched, date co-bump replaces only the date token ----
    readme = ("# R\n\n**Date:** 2026-07-20\\\n"
              "**Library Version:** 2026.07.704 (CalVer, library-wide; see x)\\\n"
              "**README Version:** 1.10.65 (semantic per-document version for this file)\n")
    out = replace_head_token(readme, "Library Version", "2026.07.704", "2026.07.705")
    check("library token replaced, parenthetical + backslash kept",
          "**Library Version:** 2026.07.705 (CalVer, library-wide; see x)\\" in out, True)
    check("README Version is NOT touched by the Library edit",
          "**README Version:** 1.10.65 (semantic" in out, True)
    dated = set_date(out, date(2026, 7, 27))
    check("date co-bump replaces only the date token", "**Date:** 2026-07-27\\" in dated, True)
    check("date co-bump left the library line intact",
          "**Library Version:** 2026.07.705 (CalVer, library-wide; see x)\\" in dated, True)
    check("date co-bump is idempotent when already today",
          set_date(dated, date(2026, 7, 27)), dated)

    # ---- table-cell safety: unescaped pipe escaped, newline collapsed, idempotent ----
    check("escape_cell leaves plain text alone", escape_cell("plain text"), "plain text")
    check("escape_cell escapes an unescaped pipe", escape_cell("a | b"), "a \\| b")
    check("escape_cell collapses an embedded newline", escape_cell("multi\nline"), "multi line")
    check("escape_cell does not double-escape", escape_cell("a \\| b"), "a \\| b")

    # ---- bypass log: HAS a separator; PR cell carries a hash ----
    bypass = ("## Rows\n\n"
              "| Date (UTC) | PR | CI state at merge | Mechanism | Justification | Change |\n"
              "| --- | --- | --- | --- | --- | --- |\n"
              "| 2026-07-26 | #1187 | green | m | j | c |\n")
    new, ins = insert_row(bypass, BYPASS_HEADER, "| 2026-07-26 | #1188 | g | m | j | c |",
                          pr_token="#1188", pr_col=1)
    lines = new.split("\n")
    sep = next(i for i, ln in enumerate(lines) if SEPARATOR_RE.match(ln))
    check("bypass insert reports a real insert", ins, True)
    check("bypass row lands directly BELOW the separator (newest-first)",
          lines[sep + 1], "| 2026-07-26 | #1188 | g | m | j | c |")
    check("bypass separator is not duplicated",
          sum(1 for ln in lines if SEPARATOR_RE.match(ln)), 1)
    _, again = insert_row(new, BYPASS_HEADER, "| x |", pr_token="#1188", pr_col=1)
    check("bypass idempotency refuses a second #1188 row", again, False)

    # ---- validate-pr history: NO separator; PR cell has no hash ----
    hist = ("## Sweep entries\n\n"
            "| Date | PR | Touched files | Findings | Hot-fix PR | Detail | Summary |\n"
            "| 2026-07-26 | 1187 | t | f | none | none | s |\n")
    new, ins = insert_row(hist, VALIDATE_HEADER,
                          "| 2026-07-26 | 1188 | t | f | none | none | s |",
                          pr_token="1188", pr_col=1)
    lines = new.split("\n")
    hi = next(i for i, ln in enumerate(lines) if ln.startswith("| Date | PR | Touched"))
    check("validate row lands directly BELOW the header (no separator invented)",
          lines[hi + 1], "| 2026-07-26 | 1188 | t | f | none | none | s |")
    check("no separator row was added to a separatorless table",
          any(SEPARATOR_RE.match(ln) for ln in lines), False)
    _, again = insert_row(new, VALIDATE_HEADER, "| x |", pr_token="1188", pr_col=1)
    check("validate idempotency refuses a duplicate 1188", again, False)

    # ---- improvement log: PR col=1 and FR-closed col=2 are isolated ----
    imp = ("## Entries\n\n"
           "| Date | PR | FR closed | What went well | Friction | Pattern (if any) | Proposed improvement |\n"
           "| 2026-07-26 | #1187 | #1186 | w | f | p | q |\n")
    new, ins = insert_row(imp, IMPROVEMENT_HEADER,
                          "| 2026-07-26 | #1188 | #1187 | w | f |  |  |",
                          pr_token="#1188", pr_col=1)
    lines = new.split("\n")
    hi = next(i for i, ln in enumerate(lines) if ln.startswith("| Date | PR | FR closed"))
    check("retro row lands newest-first below the header", _pr_cell(lines[hi + 1], 1), "#1188")
    check("retro FR-closed cell survives (different column)", _pr_cell(lines[hi + 1], 2), "#1187")

    # ---- unknown surface fails loud, never a guessed insert ----
    try:
        insert_row("no table here\n", BYPASS_HEADER, "| r |", pr_token="1", pr_col=1)
        check("missing header raises", False, True)
    except SurfaceShapeError:
        check("missing header raises rather than guessing an offset", True, True)

    # ---- CHANGELOG root: newest-first, word-bounded idempotency ----
    ch = ("# Changelog\n\nintro prose line\n\n"
          "**2026-07-26 | 2026.07.678 | PR #1188** - prior entry.\n\n"
          "**2026-07-26 | 2026.07.677 | PR #1187** - older entry.\n")
    new, ins = insert_changelog_entry(
        ch, "**2026-07-27 | 2026.07.679 | PR #1189** - new entry.",
        anchor=CHANGELOG_ROOT_ANCHOR, batch_pr=1189)
    lines = new.split("\n")
    first_entry = next(ln for ln in lines if ln.startswith("**2026"))
    check("new root entry is the topmost entry", "PR #1189" in first_entry, True)
    _, again = insert_changelog_entry(new, "dup", anchor=CHANGELOG_ROOT_ANCHOR, batch_pr=1189)
    check("root idempotency refuses a second PR #1189 entry", again, False)
    _, three = insert_changelog_entry(
        ch, "**2026-07-27 | 2026.07.679 | PR #121** - short-number entry.",
        anchor=CHANGELOG_ROOT_ANCHOR, batch_pr=121)
    check("PR #121 is not mistaken for a match inside PR #1188/#1187", three, True)

    # ---- CHANGELOG detailed: DIFFERENT anchor shape must still match ----
    chd = ("# Detailed\n\nintro\n\n"
           "## 2026-07-26, Library Version 2026.07.678, PR #1188 (prior)\n\n"
           "### Changed\n- x\n")
    new, ins = insert_changelog_entry(
        chd, "## 2026-07-27, Library Version 2026.07.679, PR #1189 (new)\n\n### Changed\n- y",
        anchor=CHANGELOG_DETAILED_ANCHOR, batch_pr=1189)
    check("detailed entry anchor matches the `## date, Library Version` shape", ins, True)
    check("detailed new entry is placed above the prior one",
          new.index("PR #1189") < new.index("PR #1188"), True)

    # ---- renderers: shape, hash conventions, findings->detail link, pipe safety ----
    base = dict(merged_pr=1187, batch_pr=1188, date=date(2026, 7, 26),
                merge_sha="1ac623a9", base_sha="dea21c95", ci_state="all checks green (x)")
    s_clean = CloseoutSpec(**base, verdict="PASS, 0 findings", touched="t",
                           justification="j", summary="did a thing", retro_well="w",
                           retro_friction="f", change="c")
    check("bypass PR cell carries the hash",
          render_bypass_row(s_clean).split("|")[2].strip(), "#1187")
    check("clean verdict emits NO detail-file link",
          "-PR-1187.md" in render_validate_row(s_clean), False)
    s_find = CloseoutSpec(**base, verdict="FAIL, 1 error", findings=["E1: reachable false-submit"],
                          touched="t", justification="j", summary="x",
                          retro_well="w", retro_friction="f")
    check("findings verdict emits a detail-file link",
          "2026-07-26-PR-1187.md" in render_validate_row(s_find), True)
    check("detailed CHANGELOG names the close-out batch",
          "Batches PR #1187's" in render_changelog_detailed(s_find, "2026.07.679"), True)

    # pipe safety: a pipe in judgement prose is escaped, so the 7 column delimiters
    # of a 6-column bypass row are preserved (unescaped pipes == 7).
    s_pipe = CloseoutSpec(**base, verdict="v", touched="t",
                          justification="plain merge failed | admin used", summary="s", change="c")
    row = render_bypass_row(s_pipe)
    check("a pipe in a cell is escaped", "admin used" in row and "failed \\| admin" in row, True)
    check("column count is preserved despite the prose pipe",
          row.count("|") - row.count("\\|"), 7)

    # ---- missing judgement: refuse by default, marker under allow_placeholders ----
    try:
        render_bypass_row(CloseoutSpec(**base))  # no justification
        check("missing justification refuses", False, True)
    except MissingJudgement as exc:
        check("missing justification names the field", exc.field_name, "justification")
    s_ph = CloseoutSpec(**base, allow_placeholders=True)
    check("placeholder mode emits a grep-able TODO marker",
          "TODO(orchestrator): fill justification" in render_bypass_row(s_ph), True)

    # ---- D7 length pre-check discriminates sentence vs total ----
    check("D7 flags an over-long single sentence",
          any("sentence" in w for w in changelog_length_warnings("word " * 50)), True)
    check("D7 passes a normal 40-word entry", changelog_length_warnings("word " * 40), [])

    # ---- end-to-end on constructed surfaces: the KEY correction, that an
    #      append-only ledger is NOT version-bumped while README IS ----
    global REPO_ROOT
    saved_root = REPO_ROOT
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            REPO_ROOT = root
            (root / ".working" / "validate-pr").mkdir(parents=True)
            (root / ".working" / "changelog-details").mkdir(parents=True)
            (root / BYPASS_LOG).write_text(
                "# Merge-bypass log\n\n**License:** CC BY-SA 4.0\n\n"
                "## Rows\n\n"
                "| Date (UTC) | PR | CI state at merge | Mechanism | Justification | Change |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                "| 2026-07-26 | #1186 | green | m | j | c |\n", encoding="utf-8")
            (root / VALIDATE_HISTORY).write_text(
                "# History\n\n**License:** CC BY-SA 4.0\n\n"
                "| Date | PR | Touched files | Findings | Hot-fix PR | Detail | Summary |\n"
                "| 2026-07-26 | 1186 | t | f | none | none | s |\n", encoding="utf-8")
            (root / IMPROVEMENT_LOG).write_text(
                "# Improvement\n\n**License:** CC BY-SA 4.0\n\n"
                "| Date | PR | FR closed | What went well | Friction | Pattern (if any) | Proposed improvement |\n"
                "| 2026-07-26 | 1186 | none | w | f |  |  |\n", encoding="utf-8")
            (root / README).write_text(
                "# R\n\n**Date:** 2026-07-26\\\n"
                "**Library Version:** 2026.07.704 (CalVer, x)\\\n"
                "**README Version:** 1.10.65 (semantic per-document version for this file)\n",
                encoding="utf-8")
            (root / CHANGELOG).write_text(
                "# Changelog\n\nintro\n\n"
                "**2026-07-26 | 2026.07.704 | PR #1187** - prior.\n", encoding="utf-8")
            (root / CHANGELOG_DETAILED).write_text(
                "# Detailed\n\nintro\n\n"
                "## 2026-07-26, Library Version 2026.07.704, PR #1187 (prior)\n\n"
                "### Changed\n- x\n", encoding="utf-8")

            spec = CloseoutSpec(
                merged_pr=1187, batch_pr=1188, date=date(2026, 7, 27),
                merge_sha="1ac623a9", base_sha="dea21c95", ci_state="all checks green",
                summary="did a thing", verdict="PASS, 0 findings", touched="t",
                justification="j", retro_well="w", retro_friction="f", change="c")
            plan = build_plan(spec, closeout_only=False, today=date(2026, 7, 27))
            by_name = {e.path.name: e for e in plan}

            check("bypass ledger row inserted",
                  by_name["merge-bypass-log.md"].changed, True)
            check("bypass ledger is NOT version-bumped (append-only)",
                  "no Version/Date field" in by_name["merge-bypass-log.md"].note, True)
            check("bypass after-text still has no **Version:** field",
                  "**Version:**" in by_name["merge-bypass-log.md"].after, False)
            check("README IS bumped (the one versioned surface)",
                  "2026.07.705" in by_name["README.md"].after
                  and "1.10.66" in by_name["README.md"].after, True)
            check("README Date co-bumped to today",
                  "**Date:** 2026-07-27\\" in by_name["README.md"].after, True)
            check("CHANGELOG root gains the PR #1188 entry",
                  "PR #1188" in by_name["CHANGELOG.md"].after, True)
            check("CHANGELOG detailed gains the PR #1188 entry",
                  "PR #1188" in by_name["CHANGELOG-detailed.md"].after, True)

            # idempotency: apply, then re-plan; every surface is a no-op
            apply_edits(plan)
            plan2 = build_plan(spec, closeout_only=False, today=date(2026, 7, 27))
            check("a second run changes nothing (fully idempotent)",
                  any(e.changed for e in plan2), False)
            check("the bypass row was not duplicated on re-run",
                  (root / BYPASS_LOG).read_text().count("| #1187 |"), 1)
    finally:
        REPO_ROOT = saved_root

    if failures:
        print(f"\nself-test: FAILED ({len(failures)} of {total[0]})")
        return 1
    print(f"\nself-test: {total[0]}/{total[0]} passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
