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
a ``BLOCKED`` entry names a blocker-type OUTSIDE the closed set; or a ``BLOCKED`` entry cites a
FORBIDDEN un-instrumented justification phrase (the self-justifying language the failure uses).
Everything else is allowed. A write to any OTHER file is out of scope (allowed).

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds
stderr back to the model. Fail-OPEN on any parse/state error: this is a discipline guardrail,
not a security boundary, and a hook that blocked on a malformed payload would be worse than the
lapse it prevents. Does not fire in a child session whose ``CLAUDE_PROJECT_DIR`` is unset
(documented harness limitation); the discipline is the primary control either way.

Self-test: ``python3 .claude/hooks/block-unjustified-decision.py --self-test``.
"""

import json
import re
import sys

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


def decide(added: str):
    """Return (block, reason) for the text added to the decisions log. Pure."""
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
    if any(k in low for k in (
        "blocked", "defer", "wind down", "wind-down", "skip",
        "hold off", "postpone", "punt", "back-burner", "sit on",
        "leave for later", "do it later", "push to", "park it",
    )):
        hits = [p for p in FORBIDDEN if p in low]
        if hits:
            problems.append(
                f"the entry cites un-instrumented justification(s) {hits}, which are never a "
                f"valid basis for deferring/holding. Name a real observable blocker or ACT/ASK."
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
        block, reason = decide(_added_text(payload))
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
