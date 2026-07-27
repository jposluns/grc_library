#!/usr/bin/env python3
"""Paired-skill step-parity audit.

For each known paired surface (a SKILL.md + slash-command .md
describing the same workflow), run two checks:

1. Step-identifier parity: the set of step identifiers in the two
   files must match by symmetric difference.
2. Subsection representation: every UNNUMBERED ``###`` subsection of
   the skill's step section must leave a mechanical trace in the
   paired command, or carry an explicit reasoned opt-out marker.

Check 2 closes a blind spot check 1 has by construction. Check 1
compares numbered identifiers, so an unnumbered subsection is
invisible to it: on 2026-07-25 a false-negative audit found that
``.claude/commands/deep-assessment.md`` omitted the whole of
``deep-assessment/SKILL.md``'s ninth Process subsection, "Parallel
execution (worker fan-out)" (including its phase-2 barrier rule), and
this gate passed the pair because the command has eight numbered steps
and the skill has eight numbered phases. Eight equals eight is
consistent with both a complete command and a command missing an
entire unnumbered subsection.

The motivating finding is Sweep 3 in the validation-sweep history
register: PR #78 introduced the deterministic pre-flight scanner
as ``### 3.5.`` in the SKILL.md heading and as ``3a.`` in the
slash-command numbered list. The two surfaces named the same
logical step with two different identifiers; the drift was caught
by subagent A's semantic triage in Sweep 3 and fixed in PR #80.
This gate catches the same shape mechanically on future drift.

Scope: only paired surfaces in the PAIRS registry are checked. Skills
that ship both a SKILL.md and a slash-command counterpart must be
registered in PAIRS to inherit the parity check; missing the
registration is a discipline gap the orchestrator must close at
ship time (per `ai-assistant-workflow-disciplines.md` §3 Apply-time
worker correction).

Step-identifier extraction (check 1):
- SKILL.md headings: ``### N. Title`` or ``### N<suffix>. Title``
  (where suffix is a lowercase letter or `.N`, e.g. ``3a``, ``3.5``).
- Slash-command numbered items: ``N. **Title**:`` at line start.
- Slash-command prose mentions: ``Step N`` (case-sensitive S),
  to catch the ``Step 8 (only when...)`` form the validation-sweep
  command file uses for the final step.

Subsection representation (check 2). A command is deliberately a
CONCISE entry point, so it never reproduces a skill's full prose. This
check therefore detects an ENTIRELY UNREPRESENTED subsection, not a
compressed one, by requiring a heading-vocabulary anchor:

- Candidate subsections are the ``###`` headings that carry no step
  identifier and sit in the same ``##`` section as the skill's numbered
  step headings. Lines inside fenced code blocks are skipped, so an
  illustrative heading inside a fence (the validation-sweep skill's
  ``### Finding: <one-line title>`` SARIF-lite template) is not a
  subsection.
- A candidate is REPRESENTED when every core token of its heading
  (lowercased alphanumeric runs, minus a short stop-word list and
  tokens under three characters) appears in the command body. The match
  is EXACT. An earlier version also accepted a shared five-character
  prefix; it was removed because it accepted unrelated words, and
  ``token_present`` records the measurement that justified the removal.
- A subsection that legitimately has no command counterpart carries
  ``<!-- parity: command-exempt: <reason> -->`` on its heading line or
  within the two lines below it. The reason is required: an unexplained
  exemption is itself a finding, so the opt-out cannot rot into a
  silent suppression.

Why a conjunction over the core tokens rather than "no heading token
appears anywhere". The weaker disjunctive rule does not detect the
motivating case: the command reuses "worker" (a worker's read surface)
and "fan-out" (wide fan-out readers on a cheaper tier) for unrelated
purposes, so the omitted subsection's heading tokens DO appear, and a
disjunctive rule passes it. A majority-of-tokens rule passes it too
(three of five). Only the conjunction fails it.

Scope: only paired surfaces in the PAIRS registry are checked.

Exit codes:
    0 - All paired surfaces have matching step-identifier sets and no
        unrepresented subsection.
    1 - At least one pair has a symmetric-difference mismatch or an
        unrepresented skill subsection.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT, iter_non_code_lines, read_text_safe


# Each entry: (skill_path, command_path). Add a pair when a new
# skill ships a slash-command counterpart.
PAIRS: list[tuple[str, str]] = [
    (
        "dev-security/claude-rules/skills/validation-sweep/SKILL.md",
        ".claude/commands/validate.md",
    ),
    (
        "dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md",
        ".claude/commands/validate-pr.md",
    ),
    (
        "dev-security/claude-rules/skills/library-fitness-review/SKILL.md",
        ".claude/commands/fitness.md",
    ),
    (
        "dev-security/claude-rules/skills/pr-retrospective/SKILL.md",
        ".claude/commands/retro.md",
    ),
    (
        "dev-security/claude-rules/skills/deep-qa-review/SKILL.md",
        ".claude/commands/full-qa.md",
    ),
    (
        "dev-security/claude-rules/skills/guardrail-review/SKILL.md",
        ".claude/commands/guardrails.md",
    ),
    (
        "dev-security/claude-rules/skills/matrix-fit/SKILL.md",
        ".claude/commands/matrix-fit.md",
    ),
    (
        "dev-security/claude-rules/skills/claim-fit/SKILL.md",
        ".claude/commands/claim-fit.md",
    ),
    (
        "dev-security/claude-rules/skills/high-assurance-verification/SKILL.md",
        ".claude/commands/high-assurance.md",
    ),
    (
        "dev-security/claude-rules/skills/deep-assessment/SKILL.md",
        ".claude/commands/deep-assessment.md",
    ),
    (
        "dev-security/claude-rules/skills/reference-audit/SKILL.md",
        ".claude/commands/reference-audit.md",
    ),
    (
        "dev-security/claude-rules/skills/publication-screening/SKILL.md",
        ".claude/commands/screen-publications.md",
    ),
    (
        "dev-security/claude-rules/skills/adopt/SKILL.md",
        ".claude/commands/adopt.md",
    ),
]

# SKILL.md step heading: `### N. ` or `### N<suffix>. ` where
# suffix is a lowercase letter or `.N` continuation (e.g. `3a`,
# `3.5`). Captures the identifier portion (digits + optional
# alphanumeric/dot suffix).
SKILL_STEP_RE = re.compile(
    r"^###\s+(\d+(?:[a-z]|\.\d+)?)\.\s",
    re.MULTILINE,
)

# Slash-command numbered list item: `N. **Title**:` at line start.
# Captures the identifier the same way as SKILL_STEP_RE.
COMMAND_NUMBERED_RE = re.compile(
    r"^(\d+(?:[a-z]|\.\d+)?)\.\s+\*\*",
    re.MULTILINE,
)

# Slash-command prose mention: `Step N` (case-sensitive S).
# Used for steps mentioned in narrative rather than as numbered
# items (e.g. the validation-sweep command file's
# "Step 8 (only when the sweep produced findings)" form).
COMMAND_PROSE_RE = re.compile(r"\bStep\s+(\d+(?:[a-z]|\.\d+)?)\b")

# --- check 2: subsection representation ---------------------------------

# Any `## ` heading (a section boundary). `### ` does not match: the
# fourth character must be whitespace.
SECTION_H2_RE = re.compile(r"^##\s")

# Any `### ` heading; captures the heading text with a trailing closing
# `#` run (an ATX variant no corpus file uses) stripped.
SUBSECTION_H3_RE = re.compile(r"^###\s+(.*?)\s*#*\s*$")

# A `### ` heading that DOES carry a step identifier, i.e. the shape
# SKILL_STEP_RE matches. Such a heading is check 1's business, not
# check 2's.
NUMBERED_H3_RE = re.compile(r"^###\s+\d+(?:[a-z]|\.\d+)?\.\s")

# Author opt-out for a subsection with no legitimate command
# counterpart. The reason group is optional in the pattern so a
# reasonless marker can be detected and reported rather than silently
# honoured.
SUBSECTION_EXEMPT_RE = re.compile(
    r"<!--\s*parity:\s*command-exempt(?::(?P<reason>[^>]*?))?\s*-->",
    re.IGNORECASE,
)

TOKEN_RE = re.compile(r"[a-z0-9]+")

# Deliberately short and closed: function words that carry no
# distinguishing content in a heading. Anything domain-bearing stays in
# the required set.
SUBSECTION_STOP_WORDS = frozenset(
    {
        "the", "a", "an", "and", "or", "of", "to", "in", "for", "on",
        "with", "its", "it", "is", "are", "be", "by", "at", "as", "any",
        "all", "then", "into", "from", "per", "not", "no", "if", "when",
        "only", "every", "this", "that",
    }
)

# How many lines below a heading an opt-out marker may sit.
EXEMPT_WINDOW = 2


HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
# A scheme is not required: slash-command files link to corpus documents by
# RELATIVE path, so a scheme-only pattern left the very class it was written
# to close open for most links in this repo (2026-07-25, the #1154 post-merge
# sweep's V1, which demonstrated five further routes).
URL_RE = re.compile(r"(?:\bhttps?://|\bwww\.)\S+", re.IGNORECASE)
# An IMAGE is stripped whole, target AND alt text, because alt text is not prose
# a reader reads as content. An inline LINK keeps its text, which is prose, and
# loses only its target. That asymmetry is deliberate; stripping link text too
# would discard genuine representation.
#
# BOTH image forms are matched, the inline `![alt](target)` and the REFERENCE
# `![alt][label]`. Matching only the inline form was the thirteenth fail-open route
# (found by the #1159 sweep): a reference-form image fell through to
# REF_LINK_LABEL_RE below, which strips the label and KEEPS the bracketed text as
# though it were link text, so `![alt caption][label]` leaked `alt` and `caption`
# as prose while `![alt caption](img.png)` correctly leaked nothing. The `!` is what
# distinguishes the two cases, and it must be consumed here rather than left to the
# link-shaped strips, which cannot see it.
IMAGE_RE = re.compile(
    r"!\[[^\]]*\]"
    r"(?:\((?:\\.|\([^()\n]*\)|[^()\\\n])*\)|\([^)]*\)|\[[^\]]*\])"
)
LINK_TARGET_RE = re.compile(r"\]\((?:\\.|\([^()\n]*\)|[^()\\\n])*\)|\]\([^)]*\)")
# The inline reference-link LABEL form `[visible text][label]`. The label is a
# reference key, not prose, but it survived every strip added in #1154 and #1155
# and could satisfy a subsection token match on its own: a command reading
# `See [the notes][parallel-execution-worker-fan-out]` counted `parallel`,
# `execution`, `worker`, `fan` and `out` while omitting the subsection entirely.
# Handled exactly as LINK_TARGET_RE handles an inline target: the label is
# replaced and the closing bracket kept, so the VISIBLE TEXT survives as prose.
# A shortcut reference (`[label]` alone, no second bracket pair) is deliberately
# NOT matched, because there the label IS the visible text.
REF_LINK_LABEL_RE = re.compile(r"\]\[[^\]]*\]")
REF_DEFINITION_RE = re.compile(r"^\s*\[[^\]]+\]:.*$", re.MULTILINE)
HTML_TAG_RE = re.compile(
    r"</?[A-Za-z][^\s>/]*(?:\s+[^\s=>\"']+(?:\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>\"']+))?)*\s*/?>"
    r"|<[^>]+>"
)
# --- fourteenth route (a): YAML front matter -----------------------------
# Front matter is a metadata header, not prose: a `description:` value can
# carry every core token of a subsection heading while the command body omits
# the subsection entirely. Only a block at the VERY START of the document
# counts, and only when every non-blank line inside it is YAML-shaped. The
# second condition is what separates front matter from a `---` THEMATIC BREAK
# opening a document, which the naive `\A---.*?---` form strips through,
# swallowing the prose between two breaks (measured, this delivery).
FRONT_MATTER_DELIM_RE = re.compile(r"^(?:---|\.\.\.)[ \t]*$")
YAML_LINE_RE = re.compile(r"^(?:[ \t]+\S|-[ \t]|[A-Za-z_][\w.\-]*[ \t]*:)")


def strip_front_matter(text: str) -> str:
    """Drop a leading YAML front-matter block, delimiters included."""
    lines = text.split("\n")
    if not lines or lines[0].rstrip() != "---":
        return text
    for index in range(1, len(lines)):
        line = lines[index]
        if FRONT_MATTER_DELIM_RE.match(line):
            return "\n".join(lines[index + 1:])
        if line.strip() and not YAML_LINE_RE.match(line):
            return text
    return text


# --- fifteenth route (b): a machine-identifier-only table cell -----------
# No table-aware stripping existed, so a metadata cell contributed its tokens.
# Only a LEADING-PIPE table row is treated as a table, because this repo writes
# inline pipe-separated lists in ordinary prose (`.claude/commands/validate.md`
# line 8's `error|warning|note` and line 15's column-name list), and a looser
# "two or more pipes" rule strips those (measured, this delivery).
#
# Within such a row, only a cell whose WHOLE content is one machine-identifier
# atom is dropped: a path, or a slug of three-plus segments. A cell of ordinary
# words is visible reading text, so it stays prose, and so does a one-hyphen
# English compound such as `fan-out`. The residual is stated in the docstring.
TABLE_ROW_RE = re.compile(r"^[ \t]*\|")
# A machine-identifier atom is a PATH or a three-plus-segment slug. The path branch
# requires a path INDICATOR (a leading `/`, `./`, or `../`; a second `/`; or a `.` on
# either side of the slash) rather than accepting any single-slash expression, because
# an ordinary English slash-compound in a cell (`read/write`, `input/output`,
# `true/false`) is reading prose, not a path, and a bare `\S*/\S*` blanked it, an
# over-strip (a gate-44 false positive) the codex adversarial verifier caught on the
# first cut of this route (verify-3115, 2026-07-27).
_PATH_ATOM_RE = r"\.{0,2}/\S+|\S*/\S*/\S+|\S*/\S*\.\S+|\S*\.\S*/\S+"
SLUG_ONLY_CELL_RE = re.compile(
    r"\A(?:" + _PATH_ATOM_RE + r"|[A-Za-z0-9]+(?:[-_.][A-Za-z0-9]+){2,})\Z"
)


def strip_metadata_table_cells(text: str) -> str:
    """Blank every machine-identifier-only cell of a leading-pipe table row."""
    out: list[str] = []
    for line in text.split("\n"):
        if not TABLE_ROW_RE.match(line) or line.count("|") < 2:
            out.append(line)
            continue
        out.append("|".join(
            " " if SLUG_ONLY_CELL_RE.match(cell.strip()) else cell
            for cell in line.split("|")
        ))
    return "\n".join(out)


def content_tokens(text: str) -> set[str]:
    """Tokens of the command's PROSE, symmetric with the skill side.

    The skill side reads through ``iter_non_code_lines``, so the command
    side must too, or the two halves of the comparison disagree about what
    counts as content. The sources below are stripped first because a token
    appearing in any of them is not a representation of anything:

    - a leading YAML FRONT-MATTER block, delimiters included, which is a
      metadata header rather than prose (see ``strip_front_matter``),
    - fenced code (via ``iter_non_code_lines``, whose contract is fence-only:
      an INDENTED code block is not stripped, so do not rely on it being),
    - a table cell whose WHOLE content is one machine-identifier atom, a path
      or a three-plus-segment slug (see ``strip_metadata_table_cells``),
    - HTML comments, which are invisible to a reader,
    - reference-link definitions, whose whole line is a key and a target,
    - images WHOLE, alt text included, since alt text is not command prose,
    - inline-link TARGETS and inline reference-link LABELS, keeping the visible
      link text in both cases, since the text is prose and the target and the
      label are keys,
    - HTML tags, INCLUDING a quoted attribute value that itself contains a
      ``>``, and
    - URLs, whose path slugs routinely contain topic words.

    Route history, as ORDINALS only. No completeness claim attaches to this
    class: three successive ones have been falsified (#1158 "the last route",
    #1159 "the last reference-form route", and #1160's own round then found a
    thirteenth), so each round samples an open class rather than draining a
    closed one. The reference-LABEL strip closed the twelfth route (2026-07-25)
    and the image-REFERENCE-form strip closed the thirteenth (see IMAGE_RE).
    This change closes four more:

    - FOURTEENTH, a YAML front-matter block, whose values are metadata;
    - FIFTEENTH, a machine-identifier-only table cell (a PARTIAL close, see
      ``strip_metadata_table_cells`` for the residual this deliberately leaves);
    - SIXTEENTH, a target truncated at its first ``)``, which was one defect
      sitting in TWO patterns, ``LINK_TARGET_RE`` and ``IMAGE_RE``, both
      corrected together because fixing either alone leaves the other open
      while looking complete;
    - SEVENTEENTH, an HTML attribute value appearing after a ``>``.

    Two routes of this class are KNOWN AND STILL OPEN, tracked rather than
    silently carried: an INDENTED code block (the fence-only caveat above), and
    a table cell of ordinary words that is semantically metadata, which no
    syntactic rule separates from prose.

    Every widening above was gated on a false-positive census over all
    registered pairs: the census removes ZERO tokens from all 13 command files
    and changes no pair's verdict.

    Without this, ONE incidental token anywhere in the file satisfied the
    subsection check. A single line of the form
    an HTML comment whose only occurrence of the word was a link-path slug
    was demonstrated (2026-07-25, the #1154 verifier's F-2) to make the
    gate pass a command that omitted the whole subsection, because the
    detection rested on the one token ``parallel``.
    """
    visible = "\n".join(
        line for _n, line in iter_non_code_lines(strip_front_matter(text))
    )
    visible = strip_metadata_table_cells(visible)
    visible = HTML_COMMENT_RE.sub(" ", visible)
    visible = REF_DEFINITION_RE.sub(" ", visible)
    visible = IMAGE_RE.sub(" ", visible)
    visible = LINK_TARGET_RE.sub("] ", visible)
    visible = REF_LINK_LABEL_RE.sub("] ", visible)
    visible = HTML_TAG_RE.sub(" ", visible)
    visible = URL_RE.sub(" ", visible)
    return set(TOKEN_RE.findall(visible.lower()))


def token_present(token: str, corpus: set[str]) -> bool:
    """Whole-token match, EXACT.

    An earlier version accepted a shared five-character prefix, intended to
    absorb inflection (a heading's ``execution`` against a command's
    ``Execute``). It also accepted UNRELATED words, and this corpus's own
    vocabulary supplies the collisions: ``integration`` was satisfied by
    ``integrity``, ``reference`` by ``referendum``, ``compliance`` by
    ``complicated``. That made it the dominant fail-open route, and the only
    one reachable through ORDINARY PROSE rather than unusual markup, so no
    amount of narrowing WHERE tokens may appear could close it (2026-07-25,
    the #1155 verifier's W1).

    Removing it is false-positive-free by MEASUREMENT, not by argument: across
    all registered pairs the check examines 5 subsection tokens and all 5 match
    exactly, so nothing relied on the prefix rule. A future genuine inflection
    case has two honest answers, either wording the command to use the
    heading's own term, or an explicit ``command-exempt`` marker stating why;
    both are visible, unlike a silent prefix collision. Whether to add a
    principled inflection rule instead is a design question left open rather
    than guessed at.
    """
    return token in corpus


def heading_core_tokens(heading: str) -> list[str]:
    """Content tokens of a subsection heading, order-preserved and deduped."""
    core: list[str] = []
    for token in TOKEN_RE.findall(heading.lower()):
        if len(token) < 3 or token in SUBSECTION_STOP_WORDS:
            continue
        if token not in core:
            core.append(token)
    return core


def extract_skill_subsections(text: str) -> list[tuple[int, str, str | None]]:
    """Unnumbered ``###`` subsections of the skill's step section.

    Returns ``(line_number, heading_text, exemption_reason)`` triples.
    ``exemption_reason`` is ``None`` when no opt-out marker is present
    and the empty string when a marker carries no reason.

    The step section is the ``##`` section enclosing the skill's
    numbered step headings, which is ``## Process`` in most pack skills
    and the unwrapped top level in ``adopt``. A skill with no numbered
    step headings yields no candidates.
    """
    visible = list(iter_non_code_lines(text))
    numbered = [n for n, line in visible if NUMBERED_H3_RE.match(line)]
    if not numbered:
        return []
    first_step, last_step = numbered[0], numbered[-1]
    start = 0
    end = visible[-1][0] + 1
    for n, line in visible:
        if not SECTION_H2_RE.match(line):
            continue
        if n < first_step:
            start = n
        elif n > last_step:
            end = n
            break
    by_line = dict(visible)
    found: list[tuple[int, str, str | None]] = []
    for n, line in visible:
        if not start < n < end:
            continue
        match = SUBSECTION_H3_RE.match(line)
        if match is None or NUMBERED_H3_RE.match(line):
            continue
        # The window is bounded by the NEXT heading as well as by
        # EXEMPT_WINDOW. Without the heading bound, a marker sitting after
        # the second of two adjacent headings falls inside the first
        # heading's window and silently exempts it too (2026-07-25, the
        # #1154 verifier's F-1, demonstrated on tightly-stacked headings).
        window_lines = []
        for k in range(n, n + EXEMPT_WINDOW + 1):
            candidate = by_line.get(k, "")
            if k > n and (SUBSECTION_H3_RE.match(candidate) or SECTION_H2_RE.match(candidate)):
                break
            window_lines.append(candidate)
        window = "\n".join(window_lines)
        exempt = SUBSECTION_EXEMPT_RE.search(window)
        reason: str | None = None
        if exempt is not None:
            reason = (exempt.group("reason") or "").strip()
        found.append((n, match.group(1).strip(), reason))
    return found


def unrepresented_subsections(
    skill_text: str, command_text: str
) -> list[tuple[int, str, list[str]]]:
    """Skill subsections with no representation in the paired command.

    Returns ``(line_number, heading_text, missing_core_tokens)`` triples.
    """
    command = content_tokens(command_text)
    out: list[tuple[int, str, list[str]]] = []
    for line_no, heading, reason in extract_skill_subsections(skill_text):
        if reason:
            continue
        if reason == "":
            out.append(
                (line_no, heading, ["<opt-out marker carries no reason>"])
            )
            continue
        core = heading_core_tokens(heading)
        if not core:
            continue
        missing = [t for t in core if not token_present(t, command)]
        if missing:
            out.append((line_no, heading, missing))
    return out


def extract_skill_steps(text: str) -> set[str]:
    return set(SKILL_STEP_RE.findall(text))


def extract_command_steps(text: str) -> set[str]:
    return (
        set(COMMAND_NUMBERED_RE.findall(text))
        | set(COMMAND_PROSE_RE.findall(text))
    )


def main() -> int:
    findings: list[str] = []
    pairs_checked = 0
    for skill_rel, command_rel in PAIRS:
        skill_path = REPO_ROOT / skill_rel
        command_path = REPO_ROOT / command_rel
        if not skill_path.is_file():
            findings.append(
                f"missing SKILL file: {skill_rel} (configured in PAIRS)"
            )
            continue
        if not command_path.is_file():
            findings.append(
                f"missing slash-command file: {command_rel} "
                f"(configured in PAIRS)"
            )
            continue
        skill_text = read_text_safe(skill_path)
        command_text = read_text_safe(command_path)
        if skill_text is None or command_text is None:
            findings.append(
                f"unreadable file in pair: {skill_rel} / {command_rel}"
            )
            continue
        skill_steps = extract_skill_steps(skill_text)
        command_steps = extract_command_steps(command_text)
        only_in_skill = skill_steps - command_steps
        only_in_command = command_steps - skill_steps
        if only_in_skill or only_in_command:
            findings.append(
                f"pair drift: {skill_rel} (steps {sorted(skill_steps)}) "
                f"vs {command_rel} (steps {sorted(command_steps)}). "
                f"Only in SKILL: {sorted(only_in_skill)}; "
                f"only in command: {sorted(only_in_command)}. "
                "Same logical step in both files must use the same "
                "identifier; rename one to match the other."
            )
        for line_no, heading, missing in unrepresented_subsections(
            skill_text, command_text
        ):
            findings.append(
                f"unrepresented subsection: {skill_rel}:{line_no} "
                f"'### {heading}' has no representation in {command_rel} "
                f"(core heading token(s) absent: {sorted(missing)}). "
                "A command is a concise entry point, not a copy, but an "
                "entirely unrepresented subsection is lockstep drift: "
                "carry the subsection's substance into the command, or "
                "mark the subsection "
                "'<!-- parity: command-exempt: <reason> -->'."
            )
        pairs_checked += 1

    if findings:
        for f in findings:
            print(f"FAIL: {f}", file=sys.stderr)
        return 1
    print(
        f"OK: {pairs_checked} paired skill+slash-command surface(s) "
        "have matching step-identifier sets and no unrepresented "
        "skill subsection."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
