#!/usr/bin/env python3
"""PreToolUse hook (Edit AND Write): check submitted decisions-log text.


Shipped 2026-07-19 after a recurring failure the maintainer named directly: the assistant
DEFERS a queued/authorized item (or winds down, re-sequences, skips) on an un-instrumented
internal-state justification ("heavy context", "long turn", "too risky to do now / do it
fresh later") INSTEAD of either doing the work or asking a specific question. Deferral-with-no-
question is strictly worse than both valid moves: it stalls progress AND hands the maintainer
nothing to act on, while dressing avoidance up as prudence.

The durable control (maintainer-designed 2026-07-19) is a WRITE-BEFORE-ENACT decisions log:
the assistant writes a classified entry to ``grc_library_private/autonomous-decisions-log.md``
BEFORE enacting any SIGNIFICANT autonomous decision (one that DISPOSES of a queued/authorized
item or CHANGES the plan: defer, re-sequence, wind-down, skip, or an authorial choice made
without asking), never a routine execution step. These are rubric requirements; this hook
checks textual proxies and does not establish that a decision complies with the rubric.

The rubric requires every logged entry to carry a ``**Classification:**`` line naming one of:

  - ``ACT``   : there is no real blocker, so do it (the default).
  - ``ASK``   : a specific decision that is the maintainer's; the entry states the question,
                and while the maintainer is reachable the assistant ASKS it (never records a
                defer instead).
  - ``BLOCKED: <blocker-type>`` : a NAMED, externally-observable blocker from the closed set
                ``maintainer-decision-unreachable`` / ``irreversible-needs-confirmation`` /
                ``failing-check`` / ``source-unavailable`` / ``maintainer-directed-hold``.

Target selection compares the last slash-separated path component, after removing trailing
slashes, with ``autonomous-decisions-log.md``. It does not require the private directory,
resolve the target path, or check existence. Nonmatching targets are allowed.

The submitted text is the whole string-valued ``content`` field when present, including an
empty string; otherwise it is a string-valued ``new_string``, or an empty string. Selection
uses field type and precedence, not the tool name. Write content is not reduced to a diff,
and Edit validation does not reconstruct the resulting file. Non-string, empty, and
whitespace-only inputs to ``decide`` are allowed.

For other inputs, the hook requires at least one case-insensitive ``_CLASSIFICATION_RE``
match anywhere in the submission. The pattern is not anchored to a Markdown line, and its
whitespace match can extend across a newline. This is not a per-entry presence check.
For every captured value, the first whitespace-delimited token, uppercased and stripped
of trailing colons, must be ACT, ASK, or BLOCKED. A BLOCKED head must also yield a blocker
token in ``VALID_BLOCKERS``. Further text is permitted; blocker reality is not verified.

The forbidden-phrase check rejects a submission containing both a ``DEFERRAL_MARKERS``
substring and a ``FORBIDDEN`` substring anywhere in its lowercased text. They need not
occur in the same entry or describe an actual deferral or justification.

The audit-token check applies when any stripped classification capture, uppercased, starts
with BLOCKED, including invalid values such as BLOCKEDNESS, and ``SET_COMPLETENESS_RE``
matches anywhere in the submission. It requires an ``AUDIT_TOKEN_RE`` match anywhere and
uses only the first match. Its integer must equal ``todo_count`` when that count is not
None. These checks do not prove that an audit occurred or was fresh or complete.

The count sums all ``TODO_ROW_RE`` matches in public ``root/TODO.md`` and all
``ITEM_HEADING_RE`` matches in sibling ``root.parent/grc_library_private/P-TODO.md``,
plus private ``TODO_ROW_RE`` matches when ``_has_todo_index_header`` is true. A missing
private file contributes zero. A public path that is not a file, or any Exception caught
during counting, yields None and skips only audit-count equality. These are syntax counts,
not independent verification of open-item status.

During normal hook execution, return 0 allows the tool call; return 2 blocks it after
printing the reason to stderr. ``main`` returns 0 on Exceptions caught while loading JSON
or handling and validating the payload. Module initialization, self-test execution, and
printing the refusal are outside those handlers. This is a discipline guardrail, not a
security boundary. The configured shell command uses ``CLAUDE_PROJECT_DIR`` to locate this
script; once invoked, the script does not require that variable. Counting uses a truthy
workspace ``project_dir``, then that environment variable, then this script's repository root.

Self-test: ``python3 .claude/hooks/block-unjustified-decision.py --self-test``.
"""
import json
import os
import re
import sys
from pathlib import Path

# F1793-12: gate private P-TODO index-row counting on has_todo_index_header,
# as tools/audit-backlog-actionability.py parse_items gates its index parser.
# Without a recognized header, private body-table rows are not counted.
# If importing the canonical classifier raises Exception, use the inline replica
# and continue validation. Other module-initialization operations are not protected.
_TOOLS_DIR = str(Path(__file__).resolve().parents[2] / "tools")
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
try:
    from lint_common import has_todo_index_header as _has_todo_index_header
except Exception:  # pragma: no cover - use inline classifier on import trouble
    def _has_todo_index_header(text: str) -> bool:  # noqa: D103
        in_fence = False
        for line in text.splitlines():
            st = line.lstrip()
            if st.startswith("```") or st.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence or not st.startswith("|"):
                continue
            # Replicate lint_common.split_row EXACTLY (codex #1811): drop exactly ONE
            # bounding pipe each side, not every leading pipe. A `.strip("|")` would
            # misclassify `|| ID | Item | Tags |` as an index header (canonical: not one).
            parts = line.split("|")
            if parts and parts[0].strip() == "":
                parts = parts[1:]
            if parts and parts[-1].strip() == "":
                parts = parts[:-1]
            cells = [c.strip() for c in parts]
            if tuple(cells[:3]) == ("ID", "Item", "Tags"):
                return True
        return False

LOG_BASENAME = "autonomous-decisions-log.md"

# Phrases associated with un-instrumented justifications for inaction.
# Any listed substring plus any DEFERRAL_MARKERS substring anywhere in the
# lowercased submission causes refusal, regardless of entry boundaries or intent.
FORBIDDEN = (
    "heavy context",
    "context weight",
    "context is heavy",
    "this deep in",
    "deep into the turn",
    "long turn",
    "enormous turn",
    "fresh context",
    "do it fresh",
    "do it later",
    "risky to do now",
    "risky to do unattended",
    "felt sensitive",
    "too sensitive to do now",
    "best fresh",
    "given my context",
)

# The closed set of permitted blocker-type tokens for a BLOCKED head.
# Membership does not establish that an externally observable blocker exists.
VALID_BLOCKERS = (
    "maintainer-decision-unreachable",
    "irreversible-needs-confirmation",
    "failing-check",
    "source-unavailable",
    "maintainer-directed-hold",
)

_CLASSIFICATION_RE = re.compile(r"\*\*Classification:\*\*\s*(.+)", re.IGNORECASE)

# Substring markers used by the forbidden-phrase check over the whole submission.
# The audit-token guard instead tests classification captures for a BLOCKED prefix;
# it does not use this set.
DEFERRAL_MARKERS = (
    "blocked", "defer", "wind down", "wind-down", "skip",
    "hold off", "postpone", "punt", "back-burner", "sit on",
    "leave for later", "do it later", "push to", "park it",
)

# Case-insensitive textual proxy for set-completeness / backlog-exhaustion language.
# A match does not establish a false claim, an actual hold, or a justification for one.
SET_COMPLETENESS_RE = re.compile(
    r"all .{0,30}(blocked|actionable|items)"
    r"|every .{0,20}(item|remaining)"
    r"|no .{0,25}(remaining|actionable|clean).{0,15}(item|work|task)"
    r"|queue .{0,15}(exhausted|drained|empty)"
    r"|everything .{0,15}(blocked|held)"
    r"|nothing .{0,15}(actionable|left|to do)"
    r"|clean .{0,15}quick.?clears? .{0,15}(exhausted|drained|done)",
    re.IGNORECASE,
)

# Audit-token pattern: `backlog-audit: <N> items enumerated` (also singular `item`),
# case-insensitive. When the guard applies, search the whole submission and use
# only the first match; token presence and count equality do not prove an audit.
AUDIT_TOKEN_RE = re.compile(r"backlog-audit:\s*(\d+)\s+items?\s+enumerated", re.IGNORECASE)

# Heading-prefix regex used by _todo_item_count only for private P-TODO.md.
# Matches include numeric prefixes such as 1.19.10a and coded prefixes such as
# SR-1, RB-R6, and GR-GAP-1; P-1.15 matches through its P-1 prefix.
# This does not validate the complete item ID or establish open-item status.
# `## Priority N` headers and table rows do not match this heading regex;
# rows are counted separately with TODO_ROW_RE under the rules below.
# The companion audit tool has its own heading and row parsers.
# tests/test_linters.py compares the combined hook and tool counts on the live
# public and private files; that check does not prove parity for every input.
ITEM_HEADING_RE = re.compile(
    r"^### (?:\d+(?:\.\d+){1,2}[a-z]?|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\b", re.MULTILINE
)
# _todo_item_count counts every match of this row regex in public TODO.md.
# In private P-TODO.md it counts these matches only if _has_todo_index_header
# is true, and adds heading matches independently. Counting does not deduplicate
# IDs or filter matching rows by status, section, or Markdown fence.
TODO_ROW_RE = re.compile(
    r"^\|\s*(?:P-\d+(?:\.\d+){1,2}[a-z]?|\d+(?:\.\d+)+(?:\.[a-z]|[a-z])?|TF-\d+)\s*\|",
    re.MULTILINE,
)


def _todo_item_count(project_dir: str | None) -> int | None:
    """Return a syntax-based count from the public and private backlog files.

    Resolve a truthy ``project_dir`` as root; otherwise use this script's repository
    root. Count all ``TODO_ROW_RE`` matches in ``root/TODO.md``. In sibling
    ``root.parent/grc_library_private/P-TODO.md``, count all ``ITEM_HEADING_RE``
    matches and add ``TODO_ROW_RE`` matches if ``_has_todo_index_header`` is true.
    The sum does not deduplicate IDs or independently verify open-item status.

    Return None if public TODO.md is not a file or any operation in the try block
    raises Exception, including private-file reading or header classification.
    A private path that is not a file contributes zero unless checking it raises.
    In ``decide``, None skips audit-count equality, not token presence when the
    audit-token guard applies.
    """
    try:
        root = Path(project_dir).resolve() if project_dir else Path(__file__).resolve().parents[2]
        todo = root / "TODO.md"
        if not todo.is_file():
            return None
        count = len(TODO_ROW_RE.findall(todo.read_text(encoding="utf-8")))
        ptodo = root.parent / "grc_library_private" / "P-TODO.md"
        if ptodo.is_file():
            ptodo_text = ptodo.read_text(encoding="utf-8")
            # F1793-12: gate private row counting on the header classifier,
            # as the audit tool gates its index parser. Once a header is found,
            # count row-regex matches throughout ptodo_text, including body tables
            # or fenced text that matches. Add heading matches independently;
            # do not deduplicate matches between the two counts.
            if _has_todo_index_header(ptodo_text):
                count += len(TODO_ROW_RE.findall(ptodo_text))
            count += len(ITEM_HEADING_RE.findall(ptodo_text))
        return count
    except Exception:
        return None


def _added_text(payload: dict) -> str:
    """Return submitted text by field type and precedence, without checking tool name.

    Select truthy ``tool_input``, then truthy ``toolInput``, then an empty mapping.
    Return the whole string-valued ``content`` field, even when empty; otherwise
    return string-valued ``new_string``. Return '' if neither is a string or an
    Exception is caught. No diff or resulting-file reconstruction is performed.
    """
    try:
        ti = payload.get("tool_input") or payload.get("toolInput") or {}
        if isinstance(ti.get("content"), str):
            return ti["content"]
        if isinstance(ti.get("new_string"), str):
            return ti["new_string"]
        return ""
    except Exception:
        return ""


def _targets_log(payload: dict) -> bool:
    try:
        ti = payload.get("tool_input") or payload.get("toolInput") or {}
        fp = ti.get("file_path") or ti.get("filePath") or ""
        return isinstance(fp, str) and fp.rstrip("/").split("/")[-1] == LOG_BASENAME
    except Exception:
        return False


def decide(added: str, todo_count: "int | None" = None):
    """Return (block, reason) from textual checks over the whole submitted string.

    Pure: this function does not read files, check a target path, or verify an audit.
    ``todo_count`` is a caller-supplied expected count, normally from
    ``_todo_item_count``. None skips count equality but not token presence when
    the audit-token guard applies. Checks do not enforce per-entry classification.
    """
    if not isinstance(added, str) or not added.strip():
        return False, ""  # allow non-string, empty, or whitespace-only input
    classifications = _CLASSIFICATION_RE.findall(added)
    if not classifications:
        return True, (
            "BLOCKED (unjustified-decision): DECISION-GUARD: the decisions-log submission has no "
            "`**Classification:**` marker with text matched by the classification pattern.\n"
            "WHY: the write-before-enact rubric requires every decision classified at decision "
            "time so avoidance cannot be dressed as prudence.\n"
            "CONSIDER INSTEAD: add a `**Classification:**` line naming exactly one of "
            "ACT / ASK / BLOCKED: <blocker-type> (default ACT; ASK a specific question if it is "
            "the maintainer's; BLOCKED only for a named observable blocker), then re-write."
        )
    problems = []
    for c in classifications:
        c_stripped = c.strip()
        head = c_stripped.split()[0].upper().rstrip(":") if c_stripped.split() else ""
        if head == "BLOCKED":
            # For a normalized BLOCKED head, extract the following sequence matched
            # by [A-Za-z0-9-]+ under re.IGNORECASE after colon/whitespace separators
            # (so the letter ranges also match a few non-ASCII letters via Unicode
            # case-folding, e.g. the Kelvin sign, which lower()s to an ASCII letter).
            m = re.match(r"BLOCKED[:\s]+([A-Za-z0-9-]+)", c_stripped, re.IGNORECASE)
            btype = (m.group(1).lower() if m else "")
            if btype not in VALID_BLOCKERS:
                problems.append(
                    f"BLOCKED names '{btype or '(none)'}', not in the closed valid set "
                    f"{VALID_BLOCKERS}."
                )
        elif head not in ("ACT", "ASK"):
            problems.append(
                f"Classification '{c_stripped[:40]}' is not ACT / ASK / BLOCKED."
            )
    # Reject co-occurring deferral-marker and forbidden-phrase substrings anywhere
    # in the lowercased submission, regardless of classification or entry boundaries.
    low = added.lower()
    has_deferral_marker = any(k in low for k in DEFERRAL_MARKERS)
    if has_deferral_marker:
        hits = [p for p in FORBIDDEN if p in low]
        if hits:
            problems.append(
                f"the submission contains forbidden phrase(s) {hits} and a deferral-marker "
                f"substring; this co-occurrence does not establish an actual deferral or justification."
            )
    # Audit-token guard (TODO gr-actionability, layer 2): require a token when any
    # stripped, uppercased classification capture starts with BLOCKED and
    # SET_COMPLETENESS_RE matches anywhere in the submission. This includes invalid
    # classifications such as BLOCKEDNESS; the two matches may be in different entries.
    # Use only the first AUDIT_TOKEN_RE match anywhere in the submission and compare
    # its integer with todo_count when supplied. These are textual proxies, not proof
    # of a real, fresh, or complete audit or of an actual hold.
    # If no classification capture starts with BLOCKED, or no set-pattern match
    # exists, this guard adds no problem. Other validation checks still apply.
    blocked_classification = any(
        c.strip().upper().startswith("BLOCKED") for c in classifications
    )
    if blocked_classification and SET_COMPLETENESS_RE.search(added):
        m = AUDIT_TOKEN_RE.search(added)
        if not m:
            problems.append(
                "the submission contains a classification value starting with BLOCKED and "
                "text matching the set-completeness pattern, but no matching fresh-audit token. "
                "A `backlog-audit: <N> items enumerated` token "
                "is required by this text check; "
                "its presence does not prove a fresh or complete audit."
            )
        elif todo_count is not None and int(m.group(1)) != todo_count:
            problems.append(
                f"the first audit token reports {m.group(1)} items "
                f"enumerated, but the supplied TODO.md + P-TODO.md count is "
                f"{todo_count}; this mismatch alone does not establish whether the "
                f"audit is stale or incomplete."
            )
    if problems:
        return True, (
            "BLOCKED (unjustified-decision): DECISION-GUARD: the decisions-log submission failed textual checks.\nWHY: "
            + " ".join(problems)
            + "\nThe rubric requires a real observable blocker for a hold; these textual "
            "checks do not verify blocker reality, decision intent, or "
            "audit freshness or completeness.\n"
            "CONSIDER INSTEAD: default to ACT; if the decision is the maintainer's and they are "
            "reachable, ASK the specific question (do not defer); record BLOCKED only with a "
            "named observable blocker from the closed set. For an un-instrumented deferral, "
            "name a real observable blocker or ACT/ASK. For a backlog-exhaustion hold, run "
            "`tools/audit-backlog-actionability.py`, enumerate every open item, and "
            "embed `backlog-audit: <N> items enumerated` where <N> matches the "
            "combined TODO.md + P-TODO.md count computed by this hook when available. "
            "Verify the enumeration itself before holding; token and count checks do not verify the audit."
        )
    return False, ""


def main(argv: list) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # fail-open
    try:
        if not _targets_log(payload):
            return 0  # no matching basename, or target extraction failed
        workspace = payload.get("workspace") or {}
        project_dir = (
            workspace.get("project_dir")
            or os.environ.get("CLAUDE_PROJECT_DIR")
            or None  # _todo_item_count falls back to this file's repo root
        )
        block, reason = decide(_added_text(payload), _todo_item_count(project_dir))
    except Exception:
        return 0  # fail-open on Exception during payload handling or validation
    if block:
        print(reason, file=sys.stderr)
        return 2
    return 0


def _self_test() -> int:
    import unittest

    class T(unittest.TestCase):
        def test_nonmatching_basename_not_targeted(self):
            p = {"tool_input": {"file_path": "/x/CHANGELOG.md",
                                "content": "no classification here"}}
            self.assertFalse(_targets_log(p))

        def test_act_entry_allowed(self):
            self.assertFalse(decide(
                "### ts | ACT | do the thing\n- **Classification:** ACT\n- reason")[0])

        def test_ask_entry_allowed(self):
            self.assertFalse(decide(
                "- **Classification:** ASK: which target branch?\n- reason")[0])

        def test_valid_blocked_allowed(self):
            self.assertFalse(decide(
                "- **Classification:** BLOCKED: source-unavailable - the RTS is paywalled")[0])

        def test_missing_classification_blocked(self):
            b, r = decide("### ts | just deferring this one\n- I'll defer this for now")
            self.assertTrue(b)
            self.assertIn("Classification", r)

        def test_invalid_blocker_type_blocked(self):
            b, r = decide("- **Classification:** BLOCKED: too-hard - it is a lot")
            self.assertTrue(b)
            self.assertIn("closed valid set", r)

        def test_forbidden_justification_in_defer_blocked(self):
            b, r = decide(
                "- **Classification:** BLOCKED: irreversible-needs-confirmation\n"
                "- deferring because the context is heavy and it is risky to do now")
            self.assertTrue(b)
            self.assertIn("un-instrumented", r)

        def test_postpone_and_blocked_markers_with_forbidden_phrase_blocked(self):
            # 3.103 (closing PR #1081): this fixture contains "postpone" and a
            # forbidden phrase, but its BLOCKED classification already supplies a
            # deferral marker. It does not isolate recognition of "postpone".
            b, r = decide(
                "- **Classification:** BLOCKED: irreversible-needs-confirmation\n"
                "- postpone this one because the context is heavy right now")
            self.assertTrue(b)
            self.assertIn("un-instrumented", r)

        def test_empty_add_allowed(self):
            self.assertFalse(decide("")[0])

        def test_exhaustion_claim_without_audit_token_blocked(self):
            # A BLOCKED capture plus "every remaining item is blocked" matches
            # the audit-token guard; no AUDIT_TOKEN_RE match is present.
            b, r = decide(
                "- **Classification:** BLOCKED: maintainer-directed-hold\n"
                "- winding down: every remaining item is blocked, so hold here")
            self.assertTrue(b)
            self.assertIn("fresh-audit", r)

        def test_exhaustion_claim_with_matching_audit_token_allowed(self):
            # The audit token's integer matches the supplied todo_count=5.
            # This fixture neither reads the live backlog nor establishes an audit.
            self.assertFalse(decide(
                "- **Classification:** BLOCKED: maintainer-directed-hold\n"
                "- winding down: every remaining item is blocked\n"
                "- backlog-audit: 5 items enumerated",
                todo_count=5)[0])

        def test_exhaustion_claim_with_wrong_count_blocked(self):
            b, r = decide(
                "- **Classification:** BLOCKED: maintainer-directed-hold\n"
                "- winding down: nothing left to do\n"
                "- backlog-audit: 3 items enumerated",
                todo_count=5)
            self.assertTrue(b)
            self.assertIn("stale or incomplete", r)

        def test_specific_blocker_defer_without_set_claim_allowed(self):
            # This fixture has a permitted BLOCKED token and no
            # SET_COMPLETENESS_RE match, so the audit-token guard adds no problem.
            self.assertFalse(decide(
                "- **Classification:** BLOCKED: maintainer-directed-hold\n"
                "- deferring this one item pending the maintainer's call on the scope",
                todo_count=5)[0])

        def test_act_entry_with_set_language_not_blocked(self):
            # Regression (pre-push verifier finding, gr-actionability L2):
            # these fixtures match the set-completeness pattern, but their only
            # classification captures start with ACT, so the audit-token guard
            # does not apply. Deferral-marker substrings are present, but no
            # forbidden phrase matches; both submissions therefore pass.
            self.assertFalse(decide(
                "- **Classification:** ACT\n"
                "- reviewed all 92 open items; none is blocked; proceeding with P1",
                todo_count=92)[0])
            self.assertFalse(decide(
                "- **Classification:** ACT\n"
                "- not deferring anything: every remaining item is actionable, doing them now",
                todo_count=92)[0])

        def test_ask_entry_with_set_language_not_blocked(self):
            # This fixture matches the set-completeness pattern, but its only
            # classification capture starts with ASK, so the audit-token guard
            # does not apply. "blocked" is a deferral marker, but no forbidden
            # phrase matches; the submission therefore passes.
            self.assertFalse(decide(
                "- **Classification:** ASK: which blocked item to escalate first?\n"
                "- every remaining item needs a maintainer call",
                todo_count=92)[0])

        def test_added_text_reads_new_string(self):
            p = {"tool_input": {"file_path": "/x/autonomous-decisions-log.md",
                                "new_string": "- **Classification:** ACT"}}
            self.assertEqual(_added_text(p), "- **Classification:** ACT")
            self.assertTrue(_targets_log(p))

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
