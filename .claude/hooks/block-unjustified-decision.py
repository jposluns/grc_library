#!/usr/bin/env python3
"""PreToolUse hook (Edit AND Write): guard the autonomous-decisions log write process.

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
without asking), never a routine execution step. This hook guards the FORM of that write so a
non-conforming (self-justifying) decision cannot be logged, and so is defence-in-depth for the
CLAUDE.md decision-rubric discipline, not a substitute for it.

Every logged entry must carry a ``**Classification:**`` line naming exactly one of:

  - ``ACT``   : there is no real blocker, so do it (the default).
  - ``ASK``   : a specific decision that is the maintainer's; the entry states the question,
                and while the maintainer is reachable the assistant ASKS it (never records a
                defer instead).
  - ``BLOCKED: <blocker-type>`` : a NAMED, externally-observable blocker from the closed set
                ``maintainer-decision-unreachable`` / ``irreversible-needs-confirmation`` /
                ``failing-check`` / ``source-unavailable`` / ``maintainer-directed-hold``.

The hook BLOCKS a write to the log when: an added entry has no ``**Classification:**`` line;
a ``BLOCKED`` entry names a blocker-type OUTSIDE the closed set; a ``BLOCKED`` entry cites a
FORBIDDEN un-instrumented justification phrase (the self-justifying language the failure uses);
or a hold/defer entry justified by a backlog SET-COMPLETENESS / exhaustion claim ("everything is
blocked", "queue drained") carries no fresh full-audit proof (a ``backlog-audit: <N> items
enumerated`` token whose ``<N>`` matches the live ``TODO.md`` open-item count). Everything else
is allowed. A write to any OTHER file is out of scope (allowed).

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds
stderr back to the model. Fail-OPEN on any parse/state error: this is a discipline guardrail,
not a security boundary, and a hook that blocked on a malformed payload would be worse than the
lapse it prevents. Does not fire in a child session whose ``CLAUDE_PROJECT_DIR`` is unset
(documented harness limitation); the discipline is the primary control either way.

Self-test: ``python3 .claude/hooks/block-unjustified-decision.py --self-test``.
"""

import json
import os
import re
import sys
from pathlib import Path

LOG_BASENAME = "autonomous-decisions-log.md"

# Un-instrumented self-justifications for INACTION (the language the failure uses). A BLOCKED
# entry citing any of these is refused: an internal-state claim is never a valid blocker.
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

# The CLOSED set of valid, externally-observable blocker types for a BLOCKED classification.
VALID_BLOCKERS = (
    "maintainer-decision-unreachable",
    "irreversible-needs-confirmation",
    "failing-check",
    "source-unavailable",
    "maintainer-directed-hold",
)

_CLASSIFICATION_RE = re.compile(r"\*\*Classification:\*\*\s*(.+)", re.IGNORECASE)

# Deferral / hold / wind-down markers (hoisted from decide() so both the existing
# forbidden-justification check and the new backlog-exhaustion check reference the
# SAME set rather than duplicating it, per TODO gr-actionability).
DEFERRAL_MARKERS = (
    "blocked", "defer", "wind down", "wind-down", "skip",
    "hold off", "postpone", "punt", "back-burner", "sit on",
    "leave for later", "do it later", "push to", "park it",
)

# A set-completeness / backlog-exhaustion claim (the false "everything is blocked,
# so hold" language used to justify STOPPING unattended). Case-insensitive.
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

# The fresh-audit proof token the entry must carry: `backlog-audit: <N> items enumerated`.
AUDIT_TOKEN_RE = re.compile(r"backlog-audit:\s*(\d+)\s+items?\s+enumerated", re.IGNORECASE)

# Item-heading regex for counting live TODO.md OPEN backlog items. PARITY POINT:
# this is ALIGNED to (byte-identical id alternation of) the companion audit tool
# `tools/audit-backlog-actionability.py` ITEM_HEADING_RE, so the two count the same
# set: an id is `N.M` / `N.M.K` / an alphanumeric sub-id (`1.19.10a`) or a coded id
# (`SR-1` / `RB-R6` / `GR-GAP-1`). `## Priority N` section headers and the
# Maintainer-or-Egress-Gated index table rows are NOT items. A test in
# tests/test_linters.py asserts this count equals the tool's on the live TODO, so
# the pair cannot silently drift.
ITEM_HEADING_RE = re.compile(
    r"^### (?:\d+(?:\.\d+){1,2}[a-z]?|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\b", re.MULTILINE
)


def _todo_item_count(project_dir: str | None) -> int | None:
    """Count open backlog items (ITEM_HEADING_RE) in the live TODO.md under
    ``project_dir``. Returns None if the root or file cannot be resolved (the new
    count-equality check then fails open; presence of the audit token is still
    required). Never raises."""
    try:
        root = Path(project_dir) if project_dir else Path(__file__).resolve().parents[2]
        todo = root / "TODO.md"
        if not todo.is_file():
            return None
        return len(ITEM_HEADING_RE.findall(todo.read_text(encoding="utf-8")))
    except Exception:
        return None


def _added_text(payload: dict) -> str:
    """The text this Edit/Write ADDS: Write -> content; Edit -> new_string. '' on any error."""
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
    """Return (block, reason) for the text added to the decisions log. Pure
    (``todo_count`` is the live TODO.md open-item count, or None if unresolved).
    """
    if not isinstance(added, str) or not added.strip():
        return False, ""  # empty add: nothing to validate
    classifications = _CLASSIFICATION_RE.findall(added)
    if not classifications:
        return True, (
            "DECISION-GUARD: a write to the autonomous-decisions log must carry a "
            "`**Classification:**` line naming exactly one of ACT / ASK / BLOCKED: "
            "<blocker-type>. No classification found in the added entry. Classify the "
            "decision (default ACT; ASK a specific question if it is the maintainer's; "
            "BLOCKED only for a named observable blocker), then re-write."
        )
    problems = []
    for c in classifications:
        c_stripped = c.strip()
        head = c_stripped.split()[0].upper().rstrip(":") if c_stripped.split() else ""
        if head == "BLOCKED":
            # blocker-type is the token after "BLOCKED:"
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
    # A BLOCKED / defer / wind-down entry must not cite an un-instrumented justification.
    low = added.lower()
    has_deferral_marker = any(k in low for k in DEFERRAL_MARKERS)
    if has_deferral_marker:
        hits = [p for p in FORBIDDEN if p in low]
        if hits:
            problems.append(
                f"the entry cites un-instrumented justification(s) {hits}, which are never a "
                f"valid basis for deferring/holding. Name a real observable blocker or ACT/ASK."
            )
    # Backlog-exhaustion guard (TODO gr-actionability, layer 2): a hold/wind-down entry
    # justified by a SET-COMPLETENESS / exhaustion claim ("everything is blocked",
    # "queue drained") must carry proof of a FRESH FULL backlog audit whose item count
    # matches the live TODO.md. FP-safe: it gates on the entry being a DECLARED HOLD, i.e.
    # a `Classification: BLOCKED` (per the write-before-enact rubric a hold/defer/wind-down
    # is classified BLOCKED with a named blocker), NOT on the loose deferral-marker
    # substring, so a legitimate ACT/ASK entry, even one reviewing "all 92 items" or noting
    # "none is blocked", is NOT blocked (that positive backlog review is exactly what this
    # control exists to encourage); and a BLOCKED entry for a SPECIFIC named blocker with no
    # set-completeness claim is unaffected (SET_COMPLETENESS_RE does not match).
    blocked_classification = any(
        c.strip().upper().startswith("BLOCKED") for c in classifications
    )
    if blocked_classification and SET_COMPLETENESS_RE.search(added):
        m = AUDIT_TOKEN_RE.search(added)
        if not m:
            problems.append(
                "the entry claims the backlog is exhausted / everything is blocked to "
                "justify a hold, but carries no fresh-audit proof. Run "
                "`tools/audit-backlog-actionability.py`, enumerate every open item, and "
                "embed `backlog-audit: <N> items enumerated` where <N> is the live "
                "TODO.md open-item count. A set-completeness claim without a complete "
                "fresh enumeration is the failure this guard prevents."
            )
        elif todo_count is not None and int(m.group(1)) != todo_count:
            problems.append(
                f"the backlog-exhaustion claim cites `backlog-audit: {m.group(1)} items "
                f"enumerated`, but the live TODO.md has {todo_count} open item(s); the "
                f"audit is stale or incomplete. Re-run the full enumeration and match the "
                f"live count before holding."
            )
    if problems:
        return True, (
            "DECISION-GUARD (write-before-enact log): this decision entry is not well-formed. "
            + " ".join(problems)
            + " Fix: default to ACT; if the decision is the maintainer's and they are reachable "
            "ASK the specific question (do not defer); record BLOCKED only with a named "
            "observable blocker from the closed set. Deferral-with-no-question and "
            "internal-state justifications are the failure this guard prevents."
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
            return 0  # a write to any other file is out of scope
        workspace = payload.get("workspace") or {}
        project_dir = (
            workspace.get("project_dir")
            or os.environ.get("CLAUDE_PROJECT_DIR")
            or None  # _todo_item_count falls back to this file's repo root
        )
        block, reason = decide(_added_text(payload), _todo_item_count(project_dir))
    except Exception:
        return 0  # fail-open on any unexpected error
    if block:
        print(reason, file=sys.stderr)
        return 2
    return 0


def _self_test() -> int:
    import unittest

    class T(unittest.TestCase):
        def test_non_log_file_allowed(self):
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

        def test_synonym_deferral_with_forbidden_blocked(self):
            # TODO 3.103: a deferral phrased with a SYNONYM outside the original
            # five keywords (here "postpone") that carries a forbidden
            # internal-state justification must still be caught by the widened set.
            b, r = decide(
                "- **Classification:** BLOCKED: irreversible-needs-confirmation\n"
                "- postpone this one because the context is heavy right now")
            self.assertTrue(b)
            self.assertIn("un-instrumented", r)

        def test_empty_add_allowed(self):
            self.assertFalse(decide("")[0])

        def test_exhaustion_claim_without_audit_blocked(self):
            # A hold justified by "everything is blocked" with no fresh-audit token.
            b, r = decide(
                "- **Classification:** BLOCKED: maintainer-directed-hold\n"
                "- winding down: every remaining item is blocked, so hold here")
            self.assertTrue(b)
            self.assertIn("fresh-audit", r)

        def test_exhaustion_claim_with_matching_audit_allowed(self):
            # Same claim, but with a fresh-audit token matching the live count.
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
            # FP-safety: a defer entry citing a SPECIFIC named blocker, with no
            # set-completeness claim, is NOT blocked by the exhaustion guard.
            self.assertFalse(decide(
                "- **Classification:** BLOCKED: maintainer-directed-hold\n"
                "- deferring this one item pending the maintainer's call on the scope",
                todo_count=5)[0])

        def test_act_entry_with_set_language_not_blocked(self):
            # FP-guard (pre-push verifier finding, gr-actionability L2): a legitimate
            # ACT entry that reviews the whole backlog ("all N items", "none is
            # blocked") must NOT be blocked. The exhaustion guard gates on a BLOCKED
            # classification, not on the loose "blocked" substring, so this positive
            # review (exactly what the control exists to encourage) passes.
            self.assertFalse(decide(
                "- **Classification:** ACT\n"
                "- reviewed all 92 open items; none is blocked; proceeding with P1",
                todo_count=92)[0])
            self.assertFalse(decide(
                "- **Classification:** ACT\n"
                "- not deferring anything: every remaining item is actionable, doing them now",
                todo_count=92)[0])

        def test_ask_entry_with_set_language_not_blocked(self):
            # FP-guard: an ASK entry with set-completeness language and the word
            # "blocked" in the question is not a hold, so it is not blocked.
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
