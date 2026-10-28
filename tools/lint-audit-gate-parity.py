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
three exclusion allow-lists and the per-PR D-numbered delta gates (3.99 (closing PR #1087), extended by #1250): each
exclusion member is cross-checked against a positive signal that it is genuinely
not a corpus gate (a setup step invokes no gate script; a delta-gate step's
script is not a §6-inventory script; a non-gate pre-commit hook carries no
`--check`), so a real gate mistakenly added to an exclusion set fails rather than
being masked; and each D-numbered delta gate in the PR-time runner is confirmed
to map to a workflow delta-gate step of the same script, with the D-numbers
contiguous D1..HIGHEST_DELTA_GATE apart from retired numbers (D6, retired 2026-08-03). See ``verify_exclusion_and_delta_guards``.

It also checks the spec's section 5 "Gate categories" grouped list against
the section-6 inventory (backlog 3b158): every inventory gate number appears
exactly once across the section-5 category lists, and those lists name no
number the inventory lacks. Only the parenthesized list that opens a
top-level numbered category item counts, ``N. **Category** (gates 12, 21):``
at column 0; numbers later on that line (a ``(gate 40)`` gloss) or in other
section-5 paragraphs are prose and are not read. HTML comments and fenced
blocks in section 5 are ignored. One pass over the whole spec pairs them in
context, close to CommonMark: a fence opens on up to three spaces then three
or more backticks or tildes (a backtick opener's info string holds no
backtick) and closes only on a line of the same character, at least as long,
with nothing else on it, so a fence line with an info string inside a fence
is fence text; outside fences and comments, inline code spans (a run of N
backticks to the next run of exactly N on the line) are blanked before
``<!--`` is looked for, so a ``<!--`` quoted in a code span or shown in a
fenced block opens nothing; an open comment ends at the first ``-->`` in
the raw text, backticks included; and a fence line inside a comment is
comment text. A fence or comment that never closes before the end of the
file is a finding at its opening line, and the lists are then not compared,
since what the block hides is unknown. A forgotten opener that pairs with a
later block's closer is not itself a finding: placed before section 5 it
hides the heading (a missing section 5), and placed among the category
lines it hides the lists after it (missing numbers), but placed after the
lists or in section 6, for example a stray backtick fence before the real
section 6 fenced block, it hides only prose and inventory text that this
check does not read (``parse_spec_inventory`` reads the rows without the
markup pass), so it is not reported. A section-5 line that starts like a list
item with ``*`` or ``_`` emphasis (``N. *``, ``N) *``, ``N. _`` or ``- *``,
indented or not) without that exact one-line list shape is a finding, and so
is a missing section 5, so a reformatted or wrapped list fails loud instead
of being skipped; the lists are then not compared either, which would only
repeat the line's numbers as missing. Which category a gate belongs in stays
a review judgment. See ``verify_category_coverage``.

Comparison: the spec inventory table is the canonical source of truth.
The other three surfaces are validated against it. For each row of the
inventory, this linter confirms that:

  - The gate name appears, verbatim, in the workflow, runner, and
    pre-commit hook at the same ordered position.
  - The gate's script path (e.g., tools/lint-metadata.py) matches the
    command in each of the three runtime surfaces.
  - The invocation arguments (flags after the script path) are identical
    across the execution surfaces that run the gate. The workflow, runner,
    and pre-commit hook all invoke each gate with the same flags (a
    --strict / --enforce / --check present on one surface but not another
    is a finding); the spec §6 row carries no argv, so it is not compared.

Each gate line is matched against a closed allowlist, not read as shell (3b646,
maintainer option A): the command must be exactly ``python3 [-I] tools/X.py``
followed by plain arguments (GATE_COMMAND), a runner line must be
``run_gate "LABEL" <command>`` at column 0 or the ``run_gate() {`` definition, a
gate workflow step has only the keys name and run, and a gate pre-commit hook has
language system, pass_filenames false and no args; no gate value may continue on a
deeper-indented line. The two YAML surfaces are accepted only in the structure the
current files use (3b646 round 6, the maintainer's 23:20Z rule carried from line shapes
to structure). Every line is blank, a comment, an unquoted ``key:`` or ``key: value``
line or a plain ``- word`` list item, apart from the text lines of an excluded step's
``run: |`` block scalar; no value begins with a quote or another YAML indicator, apart
from the exact pre-commit ``types:`` and ``types_or:`` lists the hooks use and the one
pinned quoted value, the workflow's ``python-version: "3.11"`` (exactly that text, quote
opened and closed on the line with nothing after it, kept quoted because YAML reads an
unquoted ``3.10`` as the number 3.1; WORKFLOW_PINNED_QUOTED_VALUES), so no quote or flow
collection stays open across lines and a comment line is never inside a value;
a nested value sits exactly two columns deeper than its key; no mapping repeats a key;
and each level holds only the keys of the file's fixed skeleton (WORKFLOW_SKELETON,
PRECOMMIT_SKELETON), the levels above the steps and hooks every one of them, so a step
is read only as an item of jobs.lint.steps and a hook only as an item of repos[].hooks,
and the workflow keeps its push and pull_request triggers. A step's first key is
``- name:`` and a hook's
``- id:``. A gate hook decides when it runs with exactly one of always_run, files,
types and types_or, pinned to the values the gate hooks use (PRECOMMIT_GATE_SELECTORS),
and the workflow's push branches, runner and permissions are pinned too. Any other
shape is a parse error (exit 2). The allowlist does NOT cover: the values of the
excluded setup, delta-gate and regeneration steps and hooks (their uses, with, env, if,
run and entry values, the text of the ``run: |`` block included), which the exclusion
guards check only by script; runner shell code outside run_gate lines (the function
body, a redefinition of python3 or run_gate, PATH or BASH_ENV, and whether bash
reaches a run_gate line inside a conditional, heredoc, loop or backslash
continuation); the values the skeletons leave free (the workflow and job names, and
the names and ids of steps and hooks, which the parity comparison reads but does not
pin); YAML a real reader takes differently in ways these rules do not exclude (the
check reads the structure, it does not validate YAML, so a value a real reader rejects,
such as one holding ``: ``, fails there and not here); whether GitHub Actions or
pre-commit runs at all (a workflow disabled in the repository settings, pre-commit not
installed, ``SKIP=`` or ``--no-verify``); which python3 is found on PATH; and what the
gate script does once started.

Exit codes:

  0   parity clean.
  1   one or more drift findings present.
  2   internal error parsing one of the files the gate reads: the four surfaces
      (the specification, quality.yml, run_all_audits.sh and .pre-commit-config.yaml)
      and tools/run-pr-time-checks.sh. A file that is not valid UTF-8 (an invalid
      byte, or UTF-16) is one of these errors, whichever of the five it is.

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
import shlex
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SPEC_PATH = "governance/specification-audit-programme.md"
WORKFLOW_PATH = ".github/workflows/quality.yml"
RUNNER_PATH = "tools/run_all_audits.sh"
PRECOMMIT_PATH = ".pre-commit-config.yaml"
# The PR-time runner where the D-numbered delta gates are actually invoked (the
# positive-signal surface for the delta-gate parity guard, 3.99 (closing PR #1087)).
PRTIME_PATH = "tools/run-pr-time-checks.sh"

# Workflow steps that are setup, not audit gates. These names are
# excluded from the workflow's audit-gate list before comparison.
WORKFLOW_SETUP_STEPS = {"Checkout", "Set up Python", "Install pinned dependencies"}

# Workflow steps that are per-PR delta gates documented in
# governance/specification-audit-programme.md §6.1. These are not part
# of the corpus inventory in §6 and therefore are excluded from
# the parity audit. Delta gates run in quality.yml on pull_request events
# and locally via the pre-push guard (run-pr-time-checks.sh); they inspect
# the PR's change set rather than the repository state at HEAD.
WORKFLOW_DELTA_GATE_STEPS = {
    "CHANGELOG-on-PR check",
    "Per-PR version-bump check",
    "CHANGELOG dash-on-PR check",
    "Per-PR Version-Date co-bump check",
    "Backlog-rotation-on-PR check",
    "CHANGELOG length-on-PR check",
    "Detect collection candidates on pack PRs (informational)",
    "Daily-changelog-rollup reminder",
    "Retired-section-orphan check",
    "CLAUDE.md-size ratchet",
    "Narrative-corpus mixed-diff check",
    "Number-floor monotonicity check",
    "Stranded-control-code check",
    "Class-completeness attestation check",
    "Alignment-citation register check",
}

# Delta-gate numbers are PERMANENT and never reused (the same rule as backlog
# item numbers): a retired delta gate leaves a GAP in the D1..N sequence rather
# than being renumbered, because the number leaks into CHANGELOG entries and
# prose where a recycled number would silently mis-resolve. D6 (pack-README
# version-history co-bump) was retired 2026-08-03 when the pack README's
# ``## Version history`` section was removed; the contiguity guard below
# tolerates this gap.
RETIRED_DELTA_GATES = {6}
HIGHEST_DELTA_GATE = 15

# Pre-commit hooks that are setup or regeneration steps, not audit
# gates. These are excluded from the pre-commit-to-spec parity check.
# The regenerate-derived-artefacts hook runs the build scripts in
# write mode so taxonomy.yml / narrative.yml / docs/portal.md / docs/maturity-scorecard.md / governance/relationship-model.generated.json / the TODO.md number-allocation block
# are refreshed. The ordering differs by artefact: for taxonomy.yml / docs/portal.md /
# docs/maturity-scorecard.md the --check gates run BEFORE this regen hook (check-then-regen:
# the gates fail loud on drift first, then the regen auto-fixes the local tree), while the
# narrative.yml --check, the relationship-model-in-sync --check, and the number-allocation --check (gate 91, always_run) run AFTER this hook, so those artefacts are instead protected by
# pre-commit's modification detection plus the later check; this hook is not
# itself a verification gate.
PRECOMMIT_NON_GATE_HOOKS = {"Regenerate taxonomy, narrative registry, portal, maturity scorecard, relationship model, and number-allocation block"}

# Regex to extract the tools/X.py portion of a `python3 tools/X.py ...` or
# `python3 -I tools/X.py ...` style command. Captures the script's
# repository-relative path only, discarding the `python3` prefix, the optional
# isolated-mode flag and any trailing arguments. It is used to find the script of
# the excluded and delta-gate steps; a gate line itself must match GATE_COMMAND below.
# Whether a gate runs with `-I` is not compared across surfaces; only its script and
# flags are.
SCRIPT_RE = re.compile(r"python3\s+(?:-I\s+)?(tools/[A-Za-z0-9_.\-]+\.py)")

# Gate lines are matched against a closed allowlist (3b646 round 4, maintainer option A).
# Rounds 1 to 3 read the shell grammar and refused the shapes known to hide an
# interpreter; each round found a new one (a second call, a quoted option, a glob-expanded
# interpreter). Now a gate command must be exactly GATE_COMMAND, from its first character
# to its last after trailing spaces and tabs are dropped:
#
#   python3 [-I] tools/NAME.py [ARG ...]
#
# with one space between words, NAME made of lower-case letters, digits, '-' and '_'
# (starting with a letter or digit), and each ARG a plain word of letters, digits and
# _ . / = , + - only. Those characters have no meaning to the shell or to a YAML plain
# scalar, so the shell's words, pre-commit's shlex split and a split on spaces agree, and
# no quoting, variable, glob, brace, redirection, operator, comment or second command can
# appear. Anything else is a ParseError. The same patterns guard
# tools/audit-gate-blindspots.py's runner reading (a test keeps the strings equal).
#
# Per surface:
#   - runner: every line that is not a comment and holds the word run_gate is either a
#     line in RUNNER_NON_GATE_LINES (the function definition) or matches RUNNER_LINE_RE
#     from column 0: run_gate "LABEL" GATE_COMMAND, LABEL in RUNNER_LABEL's characters.
#   - both YAML surfaces (3b646 round 6): the file is read into a tree and must match its
#     fixed skeleton, WORKFLOW_SKELETON or PRECOMMIT_SKELETON, the structure the current
#     files use. Round 5 allowlisted line shapes but not structure, so a `- name:` or
#     `- id:` line was read as a step or hook at any column under any key, and a comment
#     line was skipped while a quoted value was still open. Now:
#       * _yaml_lines: every line is blank, a comment, an unquoted `key:` or `key: value`
#         line (after an optional `- `) or a plain `- word` item; no value begins with a
#         quote or another YAML indicator (YAML_VALUE_INDICATORS), apart from the exact
#         PRECOMMIT_FLOW_LISTS values, the one WORKFLOW_PINNED_QUOTED_VALUES value and the
#         `|` of a block scalar, whose text lines are consumed as text; no line holds a tab.
#       * _yaml_tree: a nested mapping or list is exactly two columns deeper than its key
#         (so a list at its key's column, `x:` then `- name:`, is refused), a line deeper
#         than a mapping's keys that no key above it opens is refused (a plain value never
#         continues), and a mapping never repeats a key, at any level.
#       * _check_skeleton: each mapping holds only its skeleton's keys, and the mappings
#         above the steps and hooks (_Exact) hold every one of them, each list item
#         matches the skeleton's item, and pinned scalars hold their pinned values. A
#         step is therefore only an item of jobs.lint.steps, with its dash at column 6
#         and its keys at column 8, and a hook only an item of repos[].hooks, likewise.
#     A comment line is skipped only where no value is open: a value never opens a quote
#     or a flow collection (both refused at their first character, except the one-line
#     PRECOMMIT_FLOW_LISTS values and the one-line WORKFLOW_PINNED_QUOTED_VALUES value,
#     each of which closes on its own line), a plain value never continues on a later
#     line, and
#     the only multi-line value, a `run: |` block scalar, consumes its lines as text
#     before comments are looked for (so a `#` line inside it is text, as YAML reads it).
#   - workflow: a step whose first key is not `- name:` is a finding. A step whose name is
#     not excluded is a gate step: it has exactly the keys name and run, and its run
#     value matches GATE_COMMAND.
#   - pre-commit: a hook whose first key is not `- id:`, or that lacks a name or an entry,
#     is a finding. Unless excluded, a hook is a gate hook: its language is system, its
#     pass_filenames is false (pre-commit appends the file names otherwise), it has no
#     args (no key outside PRECOMMIT_GATE_HOOK_KEYS), it decides when it runs with exactly
#     one entry of PRECOMMIT_GATE_SELECTORS, verbose is true if present, and its entry
#     matches GATE_COMMAND.
# Every surface is split into lines at LF only, as bash splits it; a CR stays in its line
# (and fails the pattern), and a YAML surface holding CR, NEL, LS or PS, which YAML reads
# as a line break, is a finding.
#
# NOT COVERED by the allowlist (each runs what it runs; this check does not pin it):
#   - the values of the excluded steps and hooks (WORKFLOW_SETUP_STEPS,
#     WORKFLOW_DELTA_GATE_STEPS, PRECOMMIT_NON_GATE_HOOKS): their uses, with, env, if, run
#     and entry values and the text of a `run: |` block, which the exclusion guards check
#     only by script. Their keys are in the skeleton, so no gate step or hook can sit
#     inside them;
#   - runner shell code outside run_gate lines: the run_gate function body, the preamble,
#     a function, alias or PATH/BASH_ENV change that redefines python3 or run_gate, and
#     whether bash runs a run_gate line at all (a conditional, a heredoc, a loop or a
#     backslash continuation from the line before);
#   - the values the skeletons leave free: the workflow and job names, and step and hook
#     names and ids, which the parity comparison reads but does not pin;
#   - YAML a real reader takes differently in ways these rules do not exclude: the check
#     reads structure and does not validate YAML, so a value a real reader rejects (one
#     holding ': ', say) fails in that reader, not here;
#   - whether GitHub Actions or pre-commit runs at all (a workflow disabled in the
#     repository settings, pre-commit not installed, SKIP= or --no-verify);
#   - which python3 is found on PATH, and what the gate script itself does.
GATE_COMMAND = (r"python3(?: -I)? (?P<script>tools/[a-z0-9][a-z0-9_-]*\.py)"
                r"(?P<args>(?: [A-Za-z0-9_./=,+-]+)*)")
GATE_COMMAND_RE = re.compile(GATE_COMMAND)
RUNNER_LABEL = r"[A-Za-z0-9][A-Za-z0-9 ./-]*"
RUNNER_LINE_RE = re.compile(rf'run_gate "(?P<name>{RUNNER_LABEL})" +{GATE_COMMAND}')
RUN_GATE_WORD_RE = re.compile(r"\brun_gate\b")
# The fixed list of non-interpreter lines that hold the word run_gate.
RUNNER_NON_GATE_LINES = frozenset({"run_gate() {"})
WORKFLOW_GATE_STEP_KEYS = ("name", "run")
PRECOMMIT_GATE_HOOK_KEYS = frozenset({"id", "name", "entry", "language", "pass_filenames",
                                      "always_run", "types", "types_or", "files", "verbose"})
# The keys of PRECOMMIT_GATE_HOOK_KEYS that decide whether pre-commit runs a hook. The
# others that do (exclude, exclude_types, stages, ...) are outside it, as are the top-level
# settings (fail_fast, files, exclude, ...), so a gate hook cannot have them. A gate hook
# has exactly one of these keys, with one of the exact values the current gate hooks use,
# so every gate hook runs on every commit or whenever a markdown file is staged.
PRECOMMIT_RUN_KEYS = ("always_run", "files", "types", "types_or")
PRECOMMIT_GATE_SELECTORS = frozenset({
    ("always_run", "true"),
    ("types", "[markdown]"),
    ("types_or", "[markdown, python, shell]"),
    ("files", r"(\.md$|^tools/build-(narrative-registry|portal|taxonomy)\.py$"
              r"|^tools/lint-language\.py$|^\.corpus-management/tools/gate_lint_language\.py$)"),
    ("files", r"\.(md|py|yaml|yml|json|toml|txt)$"),
    ("files", r"\.(md|py|yaml|yml|json|toml|txt|cff)$"),
})
GATE_SHAPE = ("a gate line is exactly `python3 [-I] tools/X.py ...`: one space between "
              "words, X in lower-case letters, digits, '-' and '_', and plain arguments of "
              "letters, digits and _ . / = , + - only; no other interpreter or option, "
              "quoting, variable, glob, redirection, wrapper, second command, comment or "
              "continuation line (see GATE_COMMAND in tools/lint-audit-gate-parity.py)")


def _gate_command(command: str) -> re.Match[str] | None:
    """The GATE_COMMAND match of ``command`` (trailing spaces and tabs dropped), or None."""
    return GATE_COMMAND_RE.fullmatch(command.rstrip(" \t"))


def _gate_argv(match: re.Match[str]) -> tuple[str, ...]:
    """The arguments after the script of a GATE_COMMAND match."""
    return tuple(match.group("args").split())

# Regex to extract the tools/X.py portion from a markdown link in the
# inventory table's Script column.
SPEC_SCRIPT_RE = re.compile(r"`(tools/[A-Za-z0-9_.\-]+\.py)`")

# Characters allowed in a plain gate invocation argv (flags, paths, values, matched
# quotes, and backslash for shlex escaping). This is an ALLOWLIST: if every character of
# the argv tail is in this set, shlex word-splitting models the shell faithfully (quote-
# aware, whitespace-normalizing between tokens). If ANY other character appears -- shell
# expansion, substitution, globbing, or control such as $ ` & | ; < > ( ) * ? [ ] { } ~
# -- shlex cannot be trusted (it strips quotes but ignores expansion/globbing), so the
# raw remainder is compared instead. Allowlisting rather than blocklisting the special
# characters is complete by construction: an unanticipated metacharacter routes to the
# safe raw comparand rather than being silently mis-parsed.
_SAFE_ARGV_CHARS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    " \t_=./:@,+-'\"\\"
)


def _extract_argv(command: str, script_path: str) -> tuple[str, ...]:
    """Return a comparable representation of the argv a run command passes to
    ``script_path``. For a plain flag list (every real gate) this is the shlex
    word-split token tuple, quote-aware so ``--sep 'a b'`` is ONE token and repeated
    whitespace between tokens is irrelevant. If the remainder contains ANY character
    outside the ``_SAFE_ARGV_CHARS`` allowlist (shell expansion, substitution, globbing,
    or control -- ``$`` ``&`` ``|`` ``;`` ``<`` ``>`` ``(`` ``)`` ``*`` ``?`` and the
    like), or is malformed (unbalanced quotes), it is returned as a single raw-sentinel
    token holding the stripped remainder verbatim: shlex strips quotes but does not model
    expansion/globbing and cannot tell an unquoted ``&&`` operator from a quoted ``'&&'``
    literal, so for those cases the raw text is compared, which preserves EVERY textual
    difference and so fails toward flagging rather than masking a divergence (or crashing).
    No real gate invocation contains such a character (each is a plain
    ``python3 tools/x.py --flags`` call), so the shlex path handles every live line.
    The value is only ever compared with this function's output on another execution
    surface; the spec §6 row carries no argv, so it is not argv-compared.

    CONTRACT + residue: the guard compares the flags of a SIMPLE gate invocation.
    A metacharacter-bearing invocation is out of that contract, and the raw comparand
    is a documented best-effort, NOT a model of shell execution semantics: it may flag
    an equivalent quote-spelling difference (e.g. ``--x 'a&b'`` vs ``--x "a&b"`` -- the
    SAFE fail-toward-flagging direction), and it does not distinguish how the shell-run
    surfaces (workflow, runner) versus the direct-exec pre-commit hooks would interpret
    an operator in identical text (such text would break the gate loudly under argparse
    anyway). No live gate invocation contains a metacharacter, so this residue is inert;
    modelling per-surface shell semantics is deliberately out of scope for this guard.
    """
    idx = command.find(script_path)
    if idx < 0:
        return ()
    tail = command[idx + len(script_path):]
    if all(ch in _SAFE_ARGV_CHARS for ch in tail):
        try:
            return tuple(shlex.split(tail))
        except ValueError:
            pass
    return ("\x00raw:" + tail.strip(),)


# Inventory-table row pattern. Captures the gate number, the gate name,
# and the rest of the row (which contains the script link).
SPEC_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")


class ParseError(Exception):
    """Raised when one of the four surfaces or tools/run-pr-time-checks.sh cannot be
    parsed."""


def parse_spec_inventory(path: Path) -> list[tuple[int, int, str, str]]:
    """Return [(line_number, gate_index, name, script_path), ...] from spec section 6.

    Reads the spec markdown, locates the "## 6." heading, walks forward
    until the next "## " heading, and extracts every table row that
    matches SPEC_ROW_RE. Skips the table header divider row.
    """
    rows: list[tuple[int, int, str, str]] = []
    in_section_6 = False
    for lineno, line in enumerate(_universal_newlines(_read_utf8(path)).split("\n"), 1):
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


# Section-5 grouped list (3b158). A line opening with CATEGORY_ITEM_RE is a
# category item and must match CATEGORY_LIST_RE; only group 1, the leading
# "(gates ...)" list, is read, so later "(gate N)" glosses stay prose. The item
# shape is wide (any numbered or bulleted line opening with "*" or "_"
# emphasis), so a near-miss such as "8) **...**", "- **...**" or "8. __...__"
# is malformed, not unread.
CATEGORY_ITEM_RE = re.compile(r"^\s*(?:\d+[.)]|[-*+])\s+[*_]")
CATEGORY_LIST_RE = re.compile(r"^\d+\. \*\*[^*]+\*\* \(gates? (\d+(?:, \d+)*)\):")
# CommonMark fence lines: up to three spaces, then a run of three or more
# backticks or tildes. FENCE_LINE_RE's group 2 is the info string (a backtick
# opener's may not hold a backtick); a closer has nothing but spaces or tabs
# after its run.
FENCE_LINE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")
BACKTICK_RUN_RE = re.compile(r"`+")


def _fence_opener(line: str) -> tuple[str, int, str] | None:
    """(character, run length, info string) if ``line`` opens a fence."""
    m = FENCE_LINE_RE.match(line)
    if not m or (m.group(1)[0] == "`" and "`" in m.group(2)):
        return None
    return m.group(1)[0], len(m.group(1)), m.group(2)


def _mask_code_spans(line: str) -> str:
    """``line`` with each inline code span (a run of N backticks to the next
    run of exactly N backticks on the line) blanked to spaces, offsets kept.
    A run with no such closer is literal text and stays."""
    pos = 0
    while m := BACKTICK_RUN_RE.search(line, pos):
        closer = re.compile(rf"(?<!`){m.group(0)}(?!`)").search(line, m.end())
        if closer is None:
            pos = m.end()
            continue
        line = line[:m.start()] + " " * (closer.end() - m.start()) + line[closer.end():]
        pos = closer.end()
    return line


def _scan_markup(lines: list[str]) -> tuple[list[str | None], list[str]]:
    """One pass over ``lines`` pairing fences and HTML comments in context.

    Returns the text of each line outside comments (None for a fence line or
    a line inside a fence) and the markup findings, each at the line where the
    block opens. Fences pair as CommonMark pairs them: a closer is the
    opener's character, at least the opener's run, and nothing else, so a
    fence line with an info string inside a fence is fence text. Outside
    fences and comments, code spans are blanked before "<!--" is looked for,
    so a "<!--" quoted in a code span opens nothing; an open comment ends at
    the first "-->" in the raw text, backticks included, as CommonMark ends
    it. A fence line inside a comment is comment text. A block is a finding
    only when it never closes before the end of the file. A forgotten opener
    that pairs with a later block's closer is not reported as such: it hides
    the text up to that closer, which fails the check only if that text held
    category lines whose numbers are not listed elsewhere, or the section 5
    heading."""
    not_checked = "the category lists are not checked until it is closed"
    visible: list[str | None] = []
    findings: list[str] = []
    fence: tuple[str, int, int] | None = None  # character, run, opening line
    comment = 0  # opening line of the open comment
    for lineno, line in enumerate(lines, start=1):
        if fence is not None:
            char, run, _ = fence
            closer = FENCE_CLOSE_RE.match(line)
            if closer and closer.group(1)[0] == char and len(closer.group(1)) >= run:
                fence = None
            visible.append(None)
            continue
        if not comment:
            opener = _fence_opener(line)
            if opener:
                fence = (opener[0], opener[1], lineno)
                visible.append(None)
                continue
        kept: list[str] = []
        pos = 0
        while True:
            if not comment:
                start = _mask_code_spans(line[pos:]).find("<!--")
                if start == -1:
                    kept.append(line[pos:])
                    break
                kept.append(line[pos:pos + start])
                comment, pos = lineno, pos + start + 4
                continue
            end = line.find("-->", pos)
            if end == -1:
                break
            comment, pos = 0, end + 3
        visible.append("".join(kept))
    if fence is not None:
        findings.append(
            f"{SPEC_PATH}:{fence[2]}: section-5 categories: unclosed code fence "
            f"(no later closing fence of its character and at least its "
            f"length); {not_checked}"
        )
    elif comment:
        findings.append(
            f"{SPEC_PATH}:{comment}: section-5 categories: unclosed HTML comment "
            f"('<!--' with no later '-->'); {not_checked}"
        )
    return visible, findings


def verify_category_coverage(path: Path, expected: set[int]) -> list[str]:
    """Return findings for the section-5 grouped list against ``expected``,
    the section-6 inventory numbers: each must be listed exactly once, and no
    other number may be listed. ``_scan_markup`` reads the whole file first;
    a comment or fence that never closes is reported at its opening line and
    the comparison is skipped, because the block hides an unknown part of the
    file. The comparison then reads the lines the markup pass left
    outside fences and comments (not the
    shared ``lint_common.iter_non_code_lines``, whose fence toggle pairs
    fences differently from the CommonMark pairing checked here). A malformed
    category line or a missing section 5 is reported without the comparison,
    which would only repeat its numbers as missing."""
    lines = _universal_newlines(_read_utf8(path)).split("\n")
    visible, findings = _scan_markup(lines)
    if findings:
        return findings
    listed: dict[int, list[int]] = {}
    seen_section_5 = False
    in_section_5 = False
    for lineno, line in enumerate(visible, start=1):
        if line is None:
            continue
        if line.startswith("## "):
            in_section_5 = line.startswith("## 5.")
            seen_section_5 = seen_section_5 or in_section_5
            continue
        if not in_section_5 or not CATEGORY_ITEM_RE.match(line):
            continue
        m = CATEGORY_LIST_RE.match(line)
        if not m:
            findings.append(
                f"{SPEC_PATH}:{lineno}: section-5 categories: malformed category "
                f"line (expected 'N. **Category** (gates 1, 2, 3):' at its start, "
                f"at column 0, with the whole list on one line); the lists are "
                f"not compared until it is fixed"
            )
            continue
        for token in m.group(1).split(", "):
            listed.setdefault(int(token), []).append(lineno)
    if not seen_section_5:
        findings.append(
            f"{SPEC_PATH}: section-5 categories: no '## 5.' section found"
        )
    if findings:
        return findings
    for number in sorted(expected | set(listed)):
        lines = listed.get(number, [])
        if number not in expected:
            findings.append(
                f"{SPEC_PATH}:{lines[0]}: section-5 categories: gate {number} "
                f"not in the section-6 inventory (listed at lines {lines})"
            )
        elif not lines:
            findings.append(
                f"{SPEC_PATH}: section-5 categories: gate {number} missing; "
                f"add it to exactly one category list"
            )
        elif len(lines) > 1:
            findings.append(
                f"{SPEC_PATH}:{lines[0]}: section-5 categories: gate {number} "
                f"listed {len(lines)} times (lines {lines}); list it exactly once"
            )
    return findings


YAML_KEY_RE = re.compile(r"( *)(- )?([A-Za-z_][A-Za-z0-9_-]*):(?: +(.*))?")
# A block-sequence item that is a plain word, not a mapping (`- main` under `branches:`).
YAML_PLAIN_ITEM_RE = re.compile(r"( *)- ([A-Za-z0-9_./-]+)")
# A value may not begin with a quote, so no quote is ever open across lines, nor with any
# other YAML indicator: a flow collection, an anchor, alias or tag, a folded or chomped
# block scalar, a comment, a directive or reserved character, or a dash.
YAML_VALUE_INDICATORS = ("'", '"', "[", "]", "{", "}", "&", "*", "!", "|", ">", "%", "@",
                         "`", "#", "?", ":", ",", "-")
# The only flow sequences: the exact pre-commit types: and types_or: lists the hooks use.
# YAML reads each word as a string; yes, null and the other YAML specials are not in them.
PRECOMMIT_FLOW_LISTS = {"types": frozenset({"[markdown]"}),
                        "types_or": frozenset({"[markdown, python, shell]"})}
# The only quoted value, keyed by key name: the workflow's `python-version: "3.11"`. It stays
# quoted because YAML reads an unquoted version as a number (`3.10` loads as the float 3.1),
# a trap for any later version ending in zero. The value must be exactly this text after
# trailing spaces and tabs are dropped: a double quote opened and closed on the same line,
# with no quote, `#` or anything else after it. So the comment-line guarantee holds: the
# quote never stays open past its own line, and a later comment line is never inside it.
# `"3.12"`, `'3.11'`, `"3.11" # x`, an open `"3.11` and a quoted value of any other key stay
# refused.
WORKFLOW_PINNED_QUOTED_VALUES = {"python-version": '"3.11"'}
# The value that opens a literal block scalar (an excluded step's `run: |`).
YAML_BLOCK_SCALAR = "|"
YAML_STRUCTURE = ("a gate YAML surface is accepted only in the fixed structure of the current "
                  "file: blank and comment lines, unquoted `key:` or `key: value` lines and "
                  "plain `- word` items, each nested value exactly two columns deeper than its "
                  "key, no key repeated in a mapping, no value beginning with a quote or other "
                  "YAML indicator (apart from the exact pre-commit types: and types_or: lists, "
                  "the workflow's one pinned quoted value `python-version: \"3.11\"` and an "
                  "excluded step's `run: |`), and at each level only the keys of "
                  "WORKFLOW_SKELETON or PRECOMMIT_SKELETON in tools/lint-audit-gate-parity.py")
# Characters YAML (1.1, as PyYAML reads it) takes as a line break besides LF.
YAML_OTHER_BREAKS = ("\r", "\x85", "\u2028", "\u2029")

# The fixed skeletons (3b646 round 6). A dict is a mapping that may hold only its keys, and
# an _Exact one must hold every one of them; a one-item list is a list whose items match
# that item; a frozenset is a plain value pinned to its members; and a tuple names the node
# kinds allowed: a plain "scalar", "empty" (a key with no value) or a `|` "block" scalar.
class _Exact(dict):
    """A skeleton mapping that must hold every one of its keys."""


_SCALAR, _EMPTY, _BLOCK = ("scalar",), ("empty",), ("block",)
WORKFLOW_STEP_SKELETON = {
    "name": _SCALAR, "uses": _SCALAR, "if": _SCALAR, "run": _SCALAR + _BLOCK,
    "with": {"fetch-depth": _SCALAR, "python-version": _SCALAR},
    "env": {"BASE_SHA": _SCALAR, "HEAD_SHA": _SCALAR},
}
WORKFLOW_SKELETON = _Exact({
    "name": _SCALAR,
    "on": _Exact({"push": _Exact({"branches": [frozenset({"main"})]}), "pull_request": _EMPTY}),
    "permissions": _Exact({"contents": frozenset({"read"})}),
    "jobs": _Exact({"lint": _Exact({"name": _SCALAR, "runs-on": frozenset({"ubuntu-latest"}),
                                    "steps": [WORKFLOW_STEP_SKELETON]})}),
})
PRECOMMIT_SKELETON = _Exact({
    "repos": [_Exact({"repo": frozenset({"local"}),
                      "hooks": [dict.fromkeys(sorted(PRECOMMIT_GATE_HOOK_KEYS), _SCALAR)]})],
})
_KIND_NAMES = {"mapping": "a mapping", "sequence": "a list", "scalar": "a plain value",
               "block": "a `|` block scalar", "empty": "empty"}


def _yaml_value_problem(key: str, value: str, flow_lists: dict[str, frozenset[str]],
                        pinned_quoted: dict[str, str]) -> str | None:
    """Why the ``value`` of ``key`` is refused, or None."""
    if value.startswith(("'", '"')):
        if key in pinned_quoted and value == pinned_quoted[key]:
            return None
        return (f"has a {key} value that begins with a quote; no value is quoted apart from "
                f"the workflow's python-version: \"3.11\" exactly, so a quote never stays open "
                f"across lines")
    if key in flow_lists and value.startswith("["):
        if value in flow_lists[key]:
            return None
        return f"has a {key} list other than {' or '.join(sorted(flow_lists[key]))}"
    if value == YAML_BLOCK_SCALAR:
        return None
    if value.startswith(YAML_VALUE_INDICATORS):
        return (f"has a {key} value that begins with {value[0]!r}, a YAML indicator (a flow "
                f"collection, anchor, alias, tag, block scalar, comment or reserved character)")
    return None


def _read_utf8(path: Path) -> str:
    """The text of ``path``, decoded as UTF-8 with no newline translation. Every file the
    gate reads goes through here (3b675 round 2), so a file that is not valid UTF-8 (an
    invalid byte, or UTF-16) is a ParseError (exit 2), never a decode traceback."""
    try:
        return path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ParseError(f"{path.relative_to(REPO_ROOT)}: is not valid UTF-8 (byte "
                         f"{exc.object[exc.start]:#04x} at offset {exc.start}); only UTF-8 "
                         f"is accepted") from None


def _universal_newlines(text: str) -> str:
    """``text`` with CRLF and lone CR made LF, as a text-mode open() read gives it."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _lf_lines(path: Path) -> list[str]:
    """The lines of ``path`` split at LF only. A universal-newline read would also split
    at CR, which bash does not: `x.py\\r&& python3 -B ...` is one line to bash. A file
    that is not valid UTF-8 (an invalid byte, or UTF-16) is a ParseError (exit 2)."""
    return _read_utf8(path).split("\n")


class _YamlLine:
    """A key line (``key`` set) or a plain list item (``key`` None, its word in ``value``)
    of a YAML surface: its line number, its indent, whether it opens a list item, and the
    column of its key or word."""

    def __init__(self, lineno: int, indent: int, dash: bool, key: str | None, value: str,
                 column: int) -> None:
        self.lineno, self.indent, self.dash = lineno, indent, dash
        self.key, self.value, self.column = key, value, column


def _yaml_lines(path: Path, flow_lists: dict[str, frozenset[str]],
                pinned_quoted: dict[str, str]) -> list[_YamlLine]:
    """The key lines and plain list items of ``path``, split at LF only, trailing spaces
    and tabs dropped. Blank lines and comment lines are skipped, and so are the text lines
    of a ``key: |`` block scalar: the lines after it that are blank or indented deeper
    than its key, the first exactly two columns deeper and none less deep than the first.
    Those text lines are consumed before comments are looked for, so a ``#`` line inside
    the block is text, as YAML reads it, and every other comment line falls where no value
    is open (see GATE_COMMAND's comment). Any other line is a ParseError."""
    rel = path.relative_to(REPO_ROOT)
    lines: list[_YamlLine] = []
    block: tuple[int, int] | None = None  # the open block scalar's line and key column
    text_column = 0  # the column of the open block scalar's first text line, once read
    for lineno, raw in enumerate(_lf_lines(path), 1):
        if any(c in raw for c in YAML_OTHER_BREAKS):
            raise ParseError(f"{rel}:{lineno}: holds a line break other than LF, which YAML "
                             f"reads as a new line that this check would not; only LF line "
                             f"endings are accepted")
        line = raw.rstrip(" \t")
        indent = len(line) - len(line.lstrip(" "))
        if block is not None:
            if not line:
                continue
            if indent > block[1]:
                if not text_column and indent != block[1] + 2:
                    raise ParseError(f"{rel}:{lineno}: the first text line of the block "
                                     f"scalar at line {block[0]} is at column {indent}, not "
                                     f"{block[1] + 2}; {YAML_STRUCTURE}")
                if text_column and indent < text_column:
                    raise ParseError(f"{rel}:{lineno}: a text line of the block scalar at "
                                     f"line {block[0]} is less indented than its first text "
                                     f"line; {YAML_STRUCTURE}")
                text_column = text_column or indent
                continue
            if not text_column:
                raise ParseError(f"{rel}:{block[0]}: the block scalar has no text line; "
                                 f"{YAML_STRUCTURE}")
            block, text_column = None, 0
        if not line or line.lstrip(" ").startswith("#"):
            continue
        if "\t" in line:
            raise ParseError(f"{rel}:{lineno}: line {line.strip()!r} holds a tab; "
                             f"{YAML_STRUCTURE}")
        k = YAML_KEY_RE.fullmatch(line)
        if k is None:
            item = YAML_PLAIN_ITEM_RE.fullmatch(line)
            if item is None:
                raise ParseError(f"{rel}:{lineno}: line {line.strip()!r} is not an unquoted "
                                 f"key directly followed by a colon, nor a plain list item; "
                                 f"{YAML_STRUCTURE}")
            lines.append(_YamlLine(lineno, indent, True, None, item.group(2), item.start(2)))
            continue
        value = k.group(4) or ""
        problem = _yaml_value_problem(k.group(3), value, flow_lists, pinned_quoted)
        if problem:
            raise ParseError(f"{rel}:{lineno}: line {line.strip()!r} {problem}; "
                             f"{YAML_STRUCTURE}")
        lines.append(_YamlLine(lineno, indent, bool(k.group(2)), k.group(3), value,
                               k.start(3)))
        if value == YAML_BLOCK_SCALAR:
            block = (lineno, k.start(3))
    if block is not None and not text_column:
        raise ParseError(f"{rel}:{block[0]}: the block scalar has no text line; "
                         f"{YAML_STRUCTURE}")
    return lines


class _YamlNode:
    """A node of a YAML surface's tree: a "mapping" (``entries`` as (line, key, node), in
    order), a "sequence" (``items``), a plain "scalar" or a "block" scalar (``value``), or
    "empty" (a key with no value)."""

    def __init__(self, kind: str, lineno: int, value: str = "") -> None:
        self.kind, self.lineno, self.value = kind, lineno, value
        self.entries: list[tuple[int, str, _YamlNode]] = []
        self.items: list[_YamlNode] = []

    def keys(self) -> list[str]:
        return [key for _, key, _ in self.entries]

    def get(self, key: str) -> _YamlNode | None:
        return next((node for _, k, node in self.entries if k == key), None)


def _yaml_tree(path: Path, lines: list[_YamlLine]) -> _YamlNode:
    """The mapping ``lines`` make, read as YAML reads block collections, with every layout
    that could be read another way refused. A key with no value takes the mapping or list
    on the lines after it only when they are exactly two columns deeper than the key; at
    the key's column (a list) or any other deeper column they are a ParseError. A
    mapping's keys share one column and are unique; a list's items share one column; a
    line deeper than a mapping's keys or a list's items that no key above it opens is a
    ParseError, so a plain value never continues on a later line."""
    rel = path.relative_to(REPO_ROOT)
    pos = 0

    def refuse(line: _YamlLine, problem: str) -> ParseError:
        return ParseError(f"{rel}:{line.lineno}: {problem}; {YAML_STRUCTURE}")

    def value(line: _YamlLine) -> _YamlNode:
        if line.value == YAML_BLOCK_SCALAR:
            return _YamlNode("block", line.lineno, line.value)
        if line.value:
            return _YamlNode("scalar", line.lineno, line.value)
        if pos == len(lines) or lines[pos].indent < line.column or (
                lines[pos].indent == line.column and not lines[pos].dash):
            return _YamlNode("empty", line.lineno)
        nested = lines[pos]
        if nested.indent != line.column + 2:
            raise refuse(nested, f"is at column {nested.indent} below the key {line.key!r} at "
                                 f"column {line.column}; a nested mapping or list is exactly "
                                 f"two columns deeper than its key")
        return sequence(nested.indent) if nested.dash else mapping(nested.indent)

    def mapping(column: int, first: _YamlLine | None = None) -> _YamlNode:
        nonlocal pos
        node = _YamlNode("mapping", (first or lines[pos]).lineno)
        line = first
        while True:
            if line is None:
                if pos == len(lines) or lines[pos].indent < column:
                    return node
                line = lines[pos]
                if line.indent > column:
                    raise refuse(line, f"is indented deeper than the keys at column {column}, "
                                       f"but no key above it opens a nested value (a plain "
                                       f"value never continues on another line)")
                if line.dash:
                    raise refuse(line, f"is a list item at column {column}, where the mapping "
                                       f"above it has its keys")
                pos += 1
            if line.key in node.keys():
                raise refuse(line, f"repeats the key {line.key!r} of the mapping that starts "
                                   f"at line {node.lineno}; a key appears at most once in a "
                                   f"mapping")
            node.entries.append((line.lineno, line.key, value(line)))
            line = None

    def sequence(column: int) -> _YamlNode:
        nonlocal pos
        node = _YamlNode("sequence", lines[pos].lineno)
        while pos < len(lines) and lines[pos].indent == column and lines[pos].dash:
            line = lines[pos]
            pos += 1
            node.items.append(_YamlNode("scalar", line.lineno, line.value) if line.key is None
                              else mapping(line.column, line))
        if pos < len(lines) and lines[pos].indent >= column:
            raise refuse(lines[pos], f"is at column {lines[pos].indent}, inside the list whose "
                                     f"items are at column {column}, but is not one of its "
                                     f"items")
        return node

    if not lines:
        raise ParseError(f"{rel}: holds no YAML key; {YAML_STRUCTURE}")
    return mapping(0)


def _check_skeleton(path: Path, node: _YamlNode, skeleton, where: str) -> None:
    """Raise a ParseError unless ``node``, at the dotted key path ``where``, matches
    ``skeleton`` (see WORKFLOW_SKELETON's comment)."""
    rel = path.relative_to(REPO_ROOT)

    def refuse(lineno: int, problem: str) -> ParseError:
        return ParseError(f"{rel}:{lineno}: {where or 'the top level'} {problem}; "
                          f"{YAML_STRUCTURE}")

    if isinstance(skeleton, frozenset):
        if node.kind != "scalar" or node.value not in skeleton:
            found = repr(node.value) if node.kind == "scalar" else _KIND_NAMES[node.kind]
            raise refuse(node.lineno, f"is {found}, not {' or '.join(sorted(skeleton))}")
        return
    if isinstance(skeleton, tuple):
        if node.kind not in skeleton:
            raise refuse(node.lineno, f"is {_KIND_NAMES[node.kind]}, not "
                                      f"{' or '.join(_KIND_NAMES[k] for k in skeleton)}")
        return
    kind = "sequence" if isinstance(skeleton, list) else "mapping"
    if node.kind != kind:
        raise refuse(node.lineno, f"is {_KIND_NAMES[node.kind]}, not {_KIND_NAMES[kind]}")
    if kind == "sequence":
        for index, item in enumerate(node.items, 1):
            _check_skeleton(path, item, skeleton[0], f"{where}[{index}]")
        return
    for lineno, key, child in node.entries:
        if key not in skeleton:
            raise refuse(lineno, f"has the key {key!r}, which is not one of its keys "
                                 f"{sorted(skeleton)}")
        _check_skeleton(path, child, skeleton[key], f"{where}.{key}" if where else key)
    missing = [key for key in skeleton if key not in node.keys()] if isinstance(
        skeleton, _Exact) else []
    if missing:
        raise refuse(node.lineno, f"lacks the key(s) {missing}; it holds every one of "
                                  f"{list(skeleton)}")


def _yaml_surface(path: Path, skeleton, flow_lists: dict[str, frozenset[str]],
                  pinned_quoted: dict[str, str]) -> _YamlNode:
    """The tree of the YAML surface ``path``, checked against ``skeleton``."""
    root = _yaml_tree(path, _yaml_lines(path, flow_lists, pinned_quoted))
    _check_skeleton(path, root, skeleton, "")
    return root


def _yaml_list(path: Path, node: _YamlNode, *keys: str) -> _YamlNode:
    """The list under ``keys`` from ``node``, which the skeleton check has already typed;
    a missing key is a ParseError."""
    for key in keys:
        child = node.get(key)
        if child is None:
            raise ParseError(f"{path.relative_to(REPO_ROOT)}:{node.lineno}: has no {key} "
                             f"list; {YAML_STRUCTURE}")
        node = child
    return node


def _not_a_gate_line(path: Path, lineno: int, what: str, problem: str) -> ParseError:
    return ParseError(f"{path.relative_to(REPO_ROOT)}:{lineno}: {what} {problem}; {GATE_SHAPE}")


def parse_workflow(path: Path) -> list[tuple[int, str, str, tuple[str, ...]]]:
    """Return [(line_number, step_name, script_path, argv), ...] from quality.yml.

    Reads the file against WORKFLOW_SKELETON, then each item of jobs.lint.steps, whose
    first key must be ``name``. Skips the setup steps named in WORKFLOW_SETUP_STEPS and
    the delta-gate steps in WORKFLOW_DELTA_GATE_STEPS. Every other step is a gate step:
    its keys must be exactly ``name`` and ``run``, and its ``run`` value must match
    GATE_COMMAND. Anything outside the skeleton is a ParseError. See GATE_COMMAND's
    comment for what this does not cover.
    """
    steps = _yaml_list(path, _yaml_surface(path, WORKFLOW_SKELETON, {},
                                           WORKFLOW_PINNED_QUOTED_VALUES), "jobs", "lint", "steps")
    entries: list[tuple[int, str, str, tuple[str, ...]]] = []
    for step in steps.items:
        first = step.keys()[0]
        if first != "name":
            raise _not_a_gate_line(path, step.lineno, f"step whose first key is {first!r}",
                                   "is not read as a step (a step's first key is `- name:`)")
        step_name = step.get("name").value
        if step_name in WORKFLOW_SETUP_STEPS or step_name in WORKFLOW_DELTA_GATE_STEPS:
            continue
        what = f"step '{step_name}'"
        keys = tuple(step.keys())
        if keys != WORKFLOW_GATE_STEP_KEYS:
            raise _not_a_gate_line(path, step.lineno, what, f"has keys {list(keys)}, not "
                                   f"exactly {list(WORKFLOW_GATE_STEP_KEYS)}")
        run = step.get("run")
        m = _gate_command(run.value) if run.kind == "scalar" else None
        if not m:
            raise _not_a_gate_line(path, run.lineno, what, f"run command {run.value!r} is not "
                                   f"an accepted gate line")
        entries.append((step.lineno, step_name, m.group("script"), _gate_argv(m)))
    if not entries:
        raise ParseError(
            f"{path.relative_to(REPO_ROOT)}: no audit-step entries found"
        )
    return entries


def parse_runner(path: Path) -> list[tuple[int, str, str, tuple[str, ...]]]:
    """Return [(line_number, gate_name, script_path, argv), ...] from run_all_audits.sh.

    Every line that is not a comment and holds the word ``run_gate`` must be a line in
    RUNNER_NON_GATE_LINES (the function definition ``run_gate() {``) or match, from
    column 0, RUNNER_LINE_RE:
        run_gate "<gate name>" python3 [-I] tools/<script>.py [plain arguments]
    Anything else is a ParseError. See GATE_COMMAND's comment for what this does not
    cover.
    """
    entries: list[tuple[int, str, str, tuple[str, ...]]] = []
    for lineno, raw in enumerate(_lf_lines(path), 1):
        line = raw.rstrip(" \t")
        if (line.lstrip().startswith("#") or not RUN_GATE_WORD_RE.search(line)
                or line in RUNNER_NON_GATE_LINES):
            continue
        m = RUNNER_LINE_RE.fullmatch(line)
        if not m:
            raise _not_a_gate_line(path, lineno, "run_gate line", f"{line!r} is not an "
                                   f"accepted gate line (run_gate \"LABEL\" at column 0, "
                                   f"LABEL in letters, digits, space, '.', '/' and '-')")
        entries.append((lineno, m.group("name"), m.group("script"), _gate_argv(m)))
    if not entries:
        raise ParseError(
            f"{path.relative_to(REPO_ROOT)}: no run_gate entries found"
        )
    return entries


def parse_precommit(path: Path) -> list[tuple[int, str, str, tuple[str, ...]]]:
    """Return [(line_number, hook_name, script_path, argv), ...] from .pre-commit-config.yaml.

    Reads the file against PRECOMMIT_SKELETON, then each item of each repos[].hooks list,
    whose first key must be ``id``; it must have a ``name`` and an ``entry``, and the line
    number of the name is recorded. Skips the hooks in PRECOMMIT_NON_GATE_HOOKS. Every
    other hook is a gate hook: its ``language`` must be ``system``, its
    ``pass_filenames`` must be ``false``, it must decide when it runs with exactly one of
    PRECOMMIT_RUN_KEYS, with a (key, value) in PRECOMMIT_GATE_SELECTORS, its ``verbose``
    (if any) must be ``true``, and its ``entry`` must match GATE_COMMAND. The skeleton
    holds no ``args`` (which pre-commit appends to the command) and no other key. Anything
    outside the skeleton is a ParseError. See GATE_COMMAND's comment for what this does
    not cover.
    """
    root = _yaml_surface(path, PRECOMMIT_SKELETON, PRECOMMIT_FLOW_LISTS, {})
    entries: list[tuple[int, str, str, tuple[str, ...]]] = []
    for repo in _yaml_list(path, root, "repos").items:
        for hook in _yaml_list(path, repo, "hooks").items:
            first = hook.keys()[0]
            if first != "id":
                raise _not_a_gate_line(path, hook.lineno, f"hook whose first key is {first!r}",
                                       "is not read as a hook (a hook's first key is `- id:`)")
            name, command = hook.get("name"), hook.get("entry")
            if name is None or command is None:
                raise _not_a_gate_line(path, hook.lineno, f"hook '{hook.get('id').value}'",
                                       "does not have exactly one name and one entry")
            if name.value in PRECOMMIT_NON_GATE_HOOKS:
                continue
            what = f"hook '{name.value}'"
            values = {key: node.value for _, key, node in hook.entries}
            if values.get("language") != "system":
                raise _not_a_gate_line(path, hook.lineno, what, "does not have language: system")
            if values.get("pass_filenames") != "false":
                raise _not_a_gate_line(path, hook.lineno, what, "does not have pass_filenames: "
                                       "false, so pre-commit would append file names to the "
                                       "command")
            run_keys = [(key, values[key]) for key in PRECOMMIT_RUN_KEYS if key in values]
            if len(run_keys) != 1 or run_keys[0] not in PRECOMMIT_GATE_SELECTORS:
                raise _not_a_gate_line(path, hook.lineno, what, f"decides when it runs with "
                                       f"{run_keys}, not exactly one entry of "
                                       f"PRECOMMIT_GATE_SELECTORS (one of "
                                       f"{', '.join(PRECOMMIT_RUN_KEYS)}, with a value a gate "
                                       f"hook uses), so an edit could stop it from running")
            if values.get("verbose", "true") != "true":
                raise _not_a_gate_line(path, hook.lineno, what, "has a verbose value other "
                                       "than true")
            m = _gate_command(command.value)
            if not m:
                raise _not_a_gate_line(path, command.lineno, what, f"entry {command.value!r} "
                                       f"is not an accepted gate line")
            entries.append((name.lineno, name.value, m.group("script"), _gate_argv(m)))
    if not entries:
        raise ParseError(
            f"{path.relative_to(REPO_ROOT)}: no local hook entries found"
        )
    return entries


# --- Additive hardening of the exclusion allow-lists + the D-numbered delta gates
# (3.99 (closing PR #1087)). These guards ADD to the parity audit; they do not weaken the
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
#     hook runs `build-taxonomy.py`/`build-narrative-registry.py`/`build-portal.py`/`build-relationship-model.py`/`build-todo-number-allocation.py` in write mode; the §6 gates
#     run the SAME scripts WITH `--check`, so the `--check` flag is the
#     discriminator, not the script name.)
# Gap (ii): the live PR-time delta gates (D1..HIGHEST_DELTA_GATE, retired numbers excepted) run in the workflow (authoritative) and the local pre-push runner, with no
# cross-surface parity. The delta-gate guard confirms each D-numbered gate in the
# PR-time runner (PRTIME_PATH) maps to a WORKFLOW_DELTA_GATE_STEPS step of the
# same script, and that the D-numbers are contiguous D1..HIGHEST_DELTA_GATE apart from retired numbers (D6).
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
    """Additive 3.99 (closing PR #1087) guards over the exclusion allow-lists and the D-numbered
    delta gates. Returns a (possibly empty) list of findings. Never mutates the
    row-parity result; the caller appends these to its findings."""
    findings: list[str] = []
    wf_lines = _read_utf8(root / WORKFLOW_PATH).splitlines()
    wf_names = {m.group(1) for m in (WF_NAME_RE.match(l) for l in wf_lines) if m}
    pc_lines = _read_utf8(root / PRECOMMIT_PATH).splitlines()
    prtime = (root / PRTIME_PATH)
    prtime_lines = (
        _read_utf8(prtime).splitlines() if prtime.is_file() else []
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

    # (ii) D-numbered delta-gate parity across the workflow and the PR-time runner.
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
        expected = sorted(set(range(1, HIGHEST_DELTA_GATE + 1)) - RETIRED_DELTA_GATES)
        if nums != expected:
            findings.append(
                f"delta-gate guard: D-numbers in {PRTIME_PATH} are {nums}, not the "
                f"expected D1..D{HIGHEST_DELTA_GATE} set minus retired "
                f"{sorted(RETIRED_DELTA_GATES)} (= {expected}); a delta gate was "
                f"added, removed, or misnumbered without updating the parity surfaces."
            )
        retired_wired = sorted(RETIRED_DELTA_GATES & set(dmap))
        if retired_wired:
            findings.append(
                f"delta-gate guard: retired D-number(s) {retired_wired} are still "
                f"wired as live delta gates in {PRTIME_PATH}; a retired delta gate "
                f"must not be invoked, only its retired-marker row may remain."
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
        type=str,
        default=None,
        help="Override repository root the four source files are read from "
             "(used by the gate-36 regression test suite for synthetic-drift "
             "isolation).",
    )
    args = parser.parse_args(argv)
    if args.root is not None:  # 3b50b2d1: a missing, empty or non-directory --root is refused
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from lint_common import require_dir
        args.root = require_dir(args.root, "--root")
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

    # Section-5 grouped-list coverage (3b158), against the section-6 numbers.
    try:
        findings.extend(verify_category_coverage(
            spec_path, {gate_num for (_, gate_num, _, _) in spec}
        ))
    except ParseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: section-5 categories: {exc}", file=sys.stderr)
        return 2

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
        wf_line, wf_name, wf_script, wf_argv = workflow[idx]
        ru_line, ru_name, ru_script, ru_argv = runner[idx]
        pc_line, pc_name, pc_script, pc_argv = precommit[idx]

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

        # Invocation (argv) parity across the THREE execution surfaces
        # (workflow, runner, pre-commit). The spec §6 row carries no argv, so
        # it is not argv-compared. Every gate hook must be pass_filenames: false
        # (parse_precommit), so its authored entry flags are directly comparable. Surfaces are
        # grouped by the script they run; within each group of two or more
        # surfaces that agree on the script, the flags must be identical, so a
        # --strict / --enforce / --check that lands on one surface but not the
        # others is caught rather than silently diverging. Comparing flags of
        # two DIFFERENT scripts is meaningless (a script drift is already
        # reported by the script-drift checks above), so the grouping is by
        # script rather than a blanket three-way equality.
        exec_surfaces = (
            (WORKFLOW_PATH, wf_line, wf_script, wf_argv),
            (RUNNER_PATH, ru_line, ru_script, ru_argv),
            (PRECOMMIT_PATH, pc_line, pc_script, pc_argv),
        )
        by_script: dict[str, list[tuple[str, int, tuple[str, ...]]]] = {}
        for surf_path, surf_line, surf_script, surf_argv in exec_surfaces:
            by_script.setdefault(surf_script, []).append(
                (surf_path, surf_line, surf_argv)
            )
        for surf_script, members in by_script.items():
            if len(members) < 2:
                continue
            if len({argv for (_, _, argv) in members}) == 1:
                continue
            detail = "; ".join(
                f"{mp}:{ml} = {(' '.join(margv) or '<no args>')!r}"
                for (mp, ml, margv) in members
            )
            findings.append(
                f"Gate {gate_num} invocation (argv) drift: execution surfaces "
                f"running {surf_script!r} disagree on flags: {detail}. Every "
                f"execution surface that runs a gate must invoke it with "
                f"identical flags."
            )

    # Additive 3.99 (closing PR #1087) guards: cross-check the exclusion allow-lists against a
    # positive signal, and check the D-numbered delta gates' cross-surface parity.
    spec_scripts = {script for (_, _, _, script) in spec}
    try:
        findings.extend(verify_exclusion_and_delta_guards(REPO_ROOT, spec_scripts))
    except ParseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

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
        f"all four audit-programme surfaces, each listed once in section 5."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
