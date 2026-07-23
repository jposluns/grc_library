#!/usr/bin/env python3
"""Gate-name parity audit across the four audit-programme surfaces.

The audit programme defines a single set of audit gates whose names must
match exactly across four surfaces:

  1. governance/specification-audit-programme.md, section 6 "Gate inventory"
     - the canonical numbered table of gates.
  2. .github/workflows/quality.yml
     - the `- name: ...` field of each lint-job step.
  3. tools/run_all_audits.sh
     - the first argument to each `run_gate "..."` call.
  4. .pre-commit-config.yaml
     - the `name: ...` field of each local hook.

When the four surfaces drift (a label is abbreviated in one but not the
others, or a gate is added to one surface but not the others), the audit
programme's CI-parity guarantee in specification-audit-programme.md
section 3 principle 5 is broken. This linter detects that drift
deterministically.

In addition to the four-surface row parity, this gate ADDITIVELY guards the
three exclusion allow-lists and the PR-only D1-D8 delta gates (TODO 3.99): each
exclusion member is cross-checked against a positive signal that it is genuinely
not a corpus gate (a setup step invokes no gate script; a delta-gate step's
script is not a §6-inventory script; a non-gate pre-commit hook carries no
`--check`), so a real gate mistakenly added to an exclusion set fails rather than
being masked; and each D-numbered delta gate in the PR-time runner is confirmed
to map to a workflow delta-gate step of the same script, with the D-numbers
contiguous D1..D8. See ``verify_exclusion_and_delta_guards``.

Comparison: the spec inventory table is the canonical source of truth.
The other three surfaces are validated against it. For each row of the
inventory, this linter confirms that:

  - The gate name appears, verbatim, in the workflow, runner, and
    pre-commit hook at the same ordered position.
  - The gate's script path (e.g., tools/lint-metadata.py) matches the
    command in each of the three runtime surfaces.

Exit codes:

  0   parity clean.
  1   one or more drift findings present.
  2   internal error parsing one of the four surfaces.

The linter is itself part of the audit programme and is added to
.github/workflows/quality.yml, tools/run_all_audits.sh, and
.pre-commit-config.yaml under the conventional name "Gate-name parity
audit" so it self-checks on every run.

Stdlib-only Python 3.11.

The ``--root`` argument overrides the repository root the linter
reads its four surface files from. Used by the gate-36 regression
test suite to point at a synthetic source-set with engineered drift
so the linter's detection logic can be exercised. Default: the
repository root derived from this file's location.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SPEC_PATH = "governance/specification-audit-programme.md"
WORKFLOW_PATH = ".github/workflows/quality.yml"
RUNNER_PATH = "tools/run_all_audits.sh"
PRECOMMIT_PATH = ".pre-commit-config.yaml"
# The PR-time runner where the D1-D8 delta gates are actually invoked (the
# positive-signal surface for the delta-gate parity guard, TODO 3.99).
PRTIME_PATH = "tools/run-pr-time-checks.sh"

# Workflow steps that are setup, not audit gates. These names are
# excluded from the workflow's audit-gate list before comparison.
WORKFLOW_SETUP_STEPS = {"Checkout", "Set up Python"}

# Workflow steps that are PR-only delta gates documented in
# governance/specification-audit-programme.md §6.1. These are not part
# of the corpus inventory in §6 and therefore are excluded from
# the parity audit. Delta gates run only on pull_request events and
# inspect the PR's change set rather than the repository state at HEAD.
WORKFLOW_DELTA_GATE_STEPS = {
    "CHANGELOG-on-PR check",
    "Per-PR version-bump check",
    "CHANGELOG dash-on-PR check",
    "Per-PR Version-Date co-bump check",
    "Backlog-rotation-on-PR check",
    "Pack-README version-history co-bump check",
    "Handoff-snapshot freshness check",
    "CHANGELOG length-on-PR check",
    "Detect collection candidates on pack PRs (informational)",
}

# Pre-commit hooks that are setup or regeneration steps, not audit
# gates. These are excluded from the pre-commit-to-spec parity check.
# The regenerate-derived-artefacts hook runs the build scripts in
# write mode so taxonomy.yml / docs/portal.md / docs/maturity-scorecard.md
# are refreshed after the corresponding --check gates have verified the committed state (the L-k ordering: checks fail loud on drift first, then the regen auto-fixes the local tree); it is not
# itself a verification gate.
PRECOMMIT_NON_GATE_HOOKS = {"Regenerate taxonomy, portal, and maturity scorecard"}

# Regex to extract the tools/X.py portion of a `python3 tools/X.py ...`
# style command. Captures the script's repository-relative path only,
# discarding the `python3` prefix and any trailing arguments.
SCRIPT_RE = re.compile(r"python3\s+(tools/[A-Za-z0-9_.\-]+\.py)")

# Regex to extract the tools/X.py portion from a markdown link in the
# inventory table's Script column.
SPEC_SCRIPT_RE = re.compile(r"`(tools/[A-Za-z0-9_.\-]+\.py)`")

# Inventory-table row pattern. Captures the gate number, the gate name,
# and the rest of the row (which contains the script link).
SPEC_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")


class ParseError(Exception):
    """Raised when one of the four surfaces cannot be parsed."""


def parse_spec_inventory(path: Path) -> list[tuple[int, int, str, str]]:
    """Return [(line_number, gate_index, name, script_path), ...] from spec section 6.

    Reads the spec markdown, locates the "## 6." heading, walks forward
    until the next "## " heading, and extracts every table row that
    matches SPEC_ROW_RE. Skips the table header divider row.
    """
    rows: list[tuple[int, int, str, str]] = []
    in_section_6 = False
    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            if line.startswith("## 6."):
                in_section_6 = True
                continue
            if in_section_6 and line.startswith("## ") and not line.startswith("## 6."):
                break
            if not in_section_6:
                continue
            m = SPEC_ROW_RE.match(line)
            if not m:
                continue
            gate_num_str, gate_name, rest = m.group(1), m.group(2), m.group(3)
            # Skip header divider rows ("---" content).
            if gate_name.strip("- ") == "":
                continue
            try:
                gate_num = int(gate_num_str)
            except ValueError:
                continue
            script_match = SPEC_SCRIPT_RE.search(rest)
            if not script_match:
                raise ParseError(
                    f"{path.relative_to(REPO_ROOT)}:{lineno}: "
                    f"inventory row for gate {gate_num} has no recognizable "
                    f"`tools/X.py` script link"
                )
            rows.append((lineno, gate_num, gate_name, script_match.group(1)))
    if not rows:
        raise ParseError(
            f"{path.relative_to(REPO_ROOT)}: no §6 gate-inventory rows found"
        )
    return rows


def parse_workflow(path: Path) -> list[tuple[int, str, str]]:
    """Return [(line_number, step_name, script_path), ...] from quality.yml.

    Skips the setup steps named in WORKFLOW_SETUP_STEPS. Looks for
    consecutive `- name: X` / `run: python3 tools/Y.py ...` pairs.
    Indentation-tolerant: matches on the keyword content, not on column.
    """
    name_re = re.compile(r"^\s*-\s*name:\s*(.+?)\s*$")
    run_re = re.compile(r"^\s*run:\s*(.+?)\s*$")
    entries: list[tuple[int, str, str]] = []
    pending: tuple[int, str] | None = None
    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            m_name = name_re.match(line)
            if m_name:
                pending = (lineno, m_name.group(1))
                continue
            m_run = run_re.match(line)
            if m_run and pending is not None:
                step_lineno, step_name = pending
                if step_name in WORKFLOW_SETUP_STEPS:
                    pending = None
                    continue
                if step_name in WORKFLOW_DELTA_GATE_STEPS:
                    pending = None
                    continue
                script_match = SCRIPT_RE.search(m_run.group(1))
                if not script_match:
                    raise ParseError(
                        f"{path.relative_to(REPO_ROOT)}:{lineno}: "
                        f"step '{step_name}' has run command "
                        f"{m_run.group(1)!r} that does not match the "
                        f"`python3 tools/X.py ...` pattern"
                    )
                entries.append((step_lineno, step_name, script_match.group(1)))
                pending = None
    if not entries:
        raise ParseError(
            f"{path.relative_to(REPO_ROOT)}: no audit-step entries found"
        )
    return entries


def parse_runner(path: Path) -> list[tuple[int, str, str]]:
    """Return [(line_number, gate_name, script_path), ...] from run_all_audits.sh.

    Matches lines of the form:
        run_gate "<gate name>" python3 tools/<script>.py [...]
    Ignores the function-definition line (`run_gate() {`).
    """
    line_re = re.compile(r"^run_gate\s+\"([^\"]+)\"\s+(.+?)\s*$")
    entries: list[tuple[int, str, str]] = []
    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            m = line_re.match(line)
            if not m:
                continue
            gate_name, command = m.group(1), m.group(2)
            script_match = SCRIPT_RE.search(command)
            if not script_match:
                raise ParseError(
                    f"{path.relative_to(REPO_ROOT)}:{lineno}: "
                    f"run_gate '{gate_name}' command {command!r} does not "
                    f"match the `python3 tools/X.py ...` pattern"
                )
            entries.append((lineno, gate_name, script_match.group(1)))
    if not entries:
        raise ParseError(
            f"{path.relative_to(REPO_ROOT)}: no run_gate entries found"
        )
    return entries


def parse_precommit(path: Path) -> list[tuple[int, str, str]]:
    """Return [(line_number, hook_name, script_path), ...] from .pre-commit-config.yaml.

    Looks for blocks of `- id: ... / name: ... / entry: ...`. Captures
    the (name, entry) pair, recording the line number of the name field.
    """
    id_re = re.compile(r"^\s*-\s*id:\s*(.+?)\s*$")
    name_re = re.compile(r"^\s*name:\s*(.+?)\s*$")
    entry_re = re.compile(r"^\s*entry:\s*(.+?)\s*$")
    entries: list[tuple[int, str, str]] = []
    pending_name: tuple[int, str] | None = None
    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            if id_re.match(line):
                pending_name = None
                continue
            m_name = name_re.match(line)
            if m_name:
                pending_name = (lineno, m_name.group(1))
                continue
            m_entry = entry_re.match(line)
            if m_entry and pending_name is not None:
                hook_lineno, hook_name = pending_name
                if hook_name in PRECOMMIT_NON_GATE_HOOKS:
                    pending_name = None
                    continue
                script_match = SCRIPT_RE.search(m_entry.group(1))
                if not script_match:
                    raise ParseError(
                        f"{path.relative_to(REPO_ROOT)}:{lineno}: "
                        f"hook '{hook_name}' entry {m_entry.group(1)!r} "
                        f"does not match the `python3 tools/X.py ...` "
                        f"pattern"
                    )
                entries.append((hook_lineno, hook_name, script_match.group(1)))
                pending_name = None
    if not entries:
        raise ParseError(
            f"{path.relative_to(REPO_ROOT)}: no local hook entries found"
        )
    return entries


# --- Additive hardening of the exclusion allow-lists + the D1-D8 delta gates
# (TODO 3.99). These guards ADD to the parity audit; they do not weaken the
# name/script row-parity above. Gap (i): the three exclusion allow-lists are
# themselves unguarded, so a real §6 gate mistakenly added to an exclusion set
# would be silently masked from parity. Each guard cross-checks every exclusion
# member against a POSITIVE signal that it is genuinely NOT a corpus gate:
#   - WORKFLOW_SETUP_STEPS: the named step exists in the workflow and invokes no
#     `python3 tools/X.py` gate script (it is a `uses:` action step).
#   - WORKFLOW_DELTA_GATE_STEPS: the named step exists and its script is NOT one
#     of the §6-inventory gate scripts (it is a delta / informational script).
#   - PRECOMMIT_NON_GATE_HOOKS: the named hook exists and its entry is a write /
#     regeneration invocation (no `--check`), not a verification gate. (The regen
#     hook runs `build-taxonomy.py`/`build-portal.py` in write mode; the §6 gates
#     run the SAME scripts WITH `--check`, so the `--check` flag is the
#     discriminator, not the script name.)
# Gap (ii): the 8 PR-only delta gates (D1-D8) live only in the workflow with no
# cross-surface parity. The delta-gate guard confirms each D-numbered gate in the
# PR-time runner (PRTIME_PATH) maps to a WORKFLOW_DELTA_GATE_STEPS step of the
# same script, and that the D-numbers are contiguous D1..D8.
WF_NAME_RE = re.compile(r"^\s*-\s*name:\s*(.+?)\s*$")
PC_NAME_RE = re.compile(r"^\s*name:\s*(.+?)\s*$")
PC_ENTRY_RE = re.compile(r"^\s*entry:\s*(.+?)\s*$")
RUN_CHECK_DN_RE = re.compile(r'^\s*run_check\s+"D(\d+)\s+(.+?)"')


def _wf_step_script(wf_lines: list[str], name: str) -> str | None:
    """The first `python3 tools/X.py` script under the workflow step ``name``
    (None if the step invokes no such script, i.e. a setup/uses step)."""
    for i, line in enumerate(wf_lines):
        m = WF_NAME_RE.match(line)
        if m and m.group(1) == name:
            for j in range(i + 1, min(i + 14, len(wf_lines))):
                if WF_NAME_RE.match(wf_lines[j]):
                    break
                sm = SCRIPT_RE.search(wf_lines[j])
                if sm:
                    return sm.group(1)
            return None
    return None


def verify_exclusion_and_delta_guards(
    root: Path, spec_scripts: set[str]
) -> list[str]:
    """Additive TODO-3.99 guards over the exclusion allow-lists and the D1-D8
    delta gates. Returns a (possibly empty) list of findings. Never mutates the
    row-parity result; the caller appends these to its findings."""
    findings: list[str] = []
    wf_lines = (root / WORKFLOW_PATH).read_text(encoding="utf-8").splitlines()
    wf_names = {m.group(1) for m in (WF_NAME_RE.match(l) for l in wf_lines) if m}
    pc_lines = (root / PRECOMMIT_PATH).read_text(encoding="utf-8").splitlines()
    prtime = (root / PRTIME_PATH)
    prtime_lines = (
        prtime.read_text(encoding="utf-8").splitlines() if prtime.is_file() else []
    )

    # (i) WORKFLOW_SETUP_STEPS: must exist and invoke no gate script.
    for name in sorted(WORKFLOW_SETUP_STEPS):
        if name not in wf_names:
            findings.append(
                f"exclusion guard: WORKFLOW_SETUP_STEPS member {name!r} is not a "
                f"step in {WORKFLOW_PATH} (stale exclusion?)"
            )
            continue
        scr = _wf_step_script(wf_lines, name)
        if scr is not None:
            findings.append(
                f"exclusion guard: WORKFLOW_SETUP_STEPS member {name!r} invokes "
                f"gate script {scr!r}; a setup step must not run a gate. If this "
                f"is a real gate, remove it from the exclusion set."
            )

    # (i) WORKFLOW_DELTA_GATE_STEPS: must exist and NOT be a §6-inventory gate.
    for name in sorted(WORKFLOW_DELTA_GATE_STEPS):
        if name not in wf_names:
            findings.append(
                f"exclusion guard: WORKFLOW_DELTA_GATE_STEPS member {name!r} is "
                f"not a step in {WORKFLOW_PATH} (stale exclusion?)"
            )
            continue
        scr = _wf_step_script(wf_lines, name)
        if scr is not None and scr in spec_scripts:
            findings.append(
                f"exclusion guard: WORKFLOW_DELTA_GATE_STEPS member {name!r} runs "
                f"{scr!r}, which IS a §6-inventory gate script; a real gate is "
                f"masked from parity by this exclusion."
            )

    # (i) PRECOMMIT_NON_GATE_HOOKS: must exist and be a non-gate (no --check).
    pc_entries: dict[str, str] = {}
    pending: str | None = None
    for line in pc_lines:
        mn = PC_NAME_RE.match(line)
        if mn:
            pending = mn.group(1)
            continue
        me = PC_ENTRY_RE.match(line)
        if me and pending is not None:
            pc_entries[pending] = me.group(1)
            pending = None
    for name in sorted(PRECOMMIT_NON_GATE_HOOKS):
        if name not in pc_entries:
            findings.append(
                f"exclusion guard: PRECOMMIT_NON_GATE_HOOKS member {name!r} is not "
                f"a hook in {PRECOMMIT_PATH} (stale exclusion?)"
            )
            continue
        if "--check" in pc_entries[name]:
            findings.append(
                f"exclusion guard: PRECOMMIT_NON_GATE_HOOKS member {name!r} entry "
                f"carries --check ({pc_entries[name]!r}); a --check invocation is a "
                f"verification gate, not a regeneration hook."
            )

    # (ii) D1-D8 delta-gate parity across the workflow and the PR-time runner.
    dmap: dict[int, tuple[str, str | None]] = {}
    for i, line in enumerate(prtime_lines):
        m = RUN_CHECK_DN_RE.match(line)
        if not m:
            continue
        num, nm = int(m.group(1)), m.group(2)
        scr = None
        for j in range(i, min(i + 3, len(prtime_lines))):
            sm = SCRIPT_RE.search(prtime_lines[j])
            if sm:
                scr = sm.group(1)
                break
        dmap[num] = (nm, scr)
    if prtime_lines:  # only if the runner is present (portable-clone tolerant)
        nums = sorted(dmap)
        if nums != list(range(1, 9)):
            findings.append(
                f"delta-gate guard: D-numbers in {PRTIME_PATH} are {nums}, not the "
                f"contiguous D1..D8 set (a delta gate was added, removed, or "
                f"misnumbered without updating the parity surfaces)."
            )
        for num, (nm, scr) in sorted(dmap.items()):
            if nm not in WORKFLOW_DELTA_GATE_STEPS:
                findings.append(
                    f"delta-gate guard: D{num} {nm!r} in {PRTIME_PATH} has no "
                    f"matching WORKFLOW_DELTA_GATE_STEPS entry in {WORKFLOW_PATH}."
                )
                continue
            wf_scr = _wf_step_script(wf_lines, nm)
            if wf_scr != scr:
                findings.append(
                    f"delta-gate guard: D{num} {nm!r} script drift: "
                    f"{PRTIME_PATH} = {scr!r}; {WORKFLOW_PATH} = {wf_scr!r}."
                )
    return findings


def main(argv: list[str]) -> int:
    global REPO_ROOT
    parser = argparse.ArgumentParser(
        description="Gate-name parity audit across the four audit-programme surfaces."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Override repository root the four source files are read from "
             "(used by the gate-36 regression test suite for synthetic-drift "
             "isolation).",
    )
    args = parser.parse_args(argv)
    if args.root is not None:
        REPO_ROOT = args.root.resolve()

    spec_path = REPO_ROOT / SPEC_PATH
    workflow_path = REPO_ROOT / WORKFLOW_PATH
    runner_path = REPO_ROOT / RUNNER_PATH
    precommit_path = REPO_ROOT / PRECOMMIT_PATH

    for p in (spec_path, workflow_path, runner_path, precommit_path):
        if not p.is_file():
            print(f"ERROR: required file not found: {p.relative_to(REPO_ROOT)}",
                  file=sys.stderr)
            return 2

    try:
        spec = parse_spec_inventory(spec_path)
        workflow = parse_workflow(workflow_path)
        runner = parse_runner(runner_path)
        precommit = parse_precommit(precommit_path)
    except ParseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    findings: list[str] = []

    # Count parity. If any surface has a different number of gates, the
    # comparison cannot proceed row-by-row; report the count drift and
    # stop here. The maintainer fixes the missing entries and re-runs.
    counts = {
        SPEC_PATH: len(spec),
        WORKFLOW_PATH: len(workflow),
        RUNNER_PATH: len(runner),
        PRECOMMIT_PATH: len(precommit),
    }
    if len(set(counts.values())) != 1:
        findings.append("Gate counts differ across surfaces:")
        for label, count in counts.items():
            findings.append(f"  {label}: {count}")
        findings.append(
            "Each surface must declare the same number of audit gates. "
            "Add the missing entries to the surface(s) with the lower "
            "count, or remove the extra entries from the surface(s) "
            "with the higher count."
        )
        print("\n".join(findings))
        print(f"\nFAIL: {len(findings)} parity finding(s).")
        return 1

    # Row-by-row parity. Spec inventory is canonical.
    for idx, (spec_line, gate_num, spec_name, spec_script) in enumerate(spec):
        wf_line, wf_name, wf_script = workflow[idx]
        ru_line, ru_name, ru_script = runner[idx]
        pc_line, pc_name, pc_script = precommit[idx]

        if wf_name != spec_name:
            findings.append(
                f"Gate {gate_num} name drift: "
                f"spec({SPEC_PATH}:{spec_line}) = {spec_name!r}; "
                f"workflow({WORKFLOW_PATH}:{wf_line}) = {wf_name!r}"
            )
        if ru_name != spec_name:
            findings.append(
                f"Gate {gate_num} name drift: "
                f"spec({SPEC_PATH}:{spec_line}) = {spec_name!r}; "
                f"runner({RUNNER_PATH}:{ru_line}) = {ru_name!r}"
            )
        if pc_name != spec_name:
            findings.append(
                f"Gate {gate_num} name drift: "
                f"spec({SPEC_PATH}:{spec_line}) = {spec_name!r}; "
                f"pre-commit({PRECOMMIT_PATH}:{pc_line}) = {pc_name!r}"
            )

        if wf_script != spec_script:
            findings.append(
                f"Gate {gate_num} script drift: "
                f"spec({SPEC_PATH}:{spec_line}) = {spec_script!r}; "
                f"workflow({WORKFLOW_PATH}:{wf_line}) = {wf_script!r}"
            )
        if ru_script != spec_script:
            findings.append(
                f"Gate {gate_num} script drift: "
                f"spec({SPEC_PATH}:{spec_line}) = {spec_script!r}; "
                f"runner({RUNNER_PATH}:{ru_line}) = {ru_script!r}"
            )
        if pc_script != spec_script:
            findings.append(
                f"Gate {gate_num} script drift: "
                f"spec({SPEC_PATH}:{spec_line}) = {spec_script!r}; "
                f"pre-commit({PRECOMMIT_PATH}:{pc_line}) = {pc_script!r}"
            )

    # Additive TODO-3.99 guards: cross-check the exclusion allow-lists against a
    # positive signal, and check the D1-D8 delta gates' cross-surface parity.
    spec_scripts = {script for (_, _, _, script) in spec}
    findings.extend(verify_exclusion_and_delta_guards(REPO_ROOT, spec_scripts))

    if findings:
        for finding in findings:
            print(finding)
        print(
            f"\nFAIL: {len(findings)} parity finding(s) across the audit "
            f"programme's four surfaces."
        )
        print(
            "The Audit Programme Specification section 3 principle 5 "
            "requires that the spec, workflow, runner, and pre-commit "
            "hook all declare the same gates with the same names and "
            "scripts in the same order. The spec is canonical."
        )
        return 1

    print(
        f"OK: gate-name parity confirmed for {len(spec)} gates across "
        f"all four audit-programme surfaces."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
