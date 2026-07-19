#!/usr/bin/env python3
"""PreToolUse AskUserQuestion hook: block re-asking an already-decided question.

Shipped 2026-07-19 (TODO section 1.22.6) after the assistant re-asked the maintainer
four content forks (section 3.68 vuln-SLA, section 3.69 MFA scope, section 3.70
asymmetric-key minimums, the standards-rendering item) whose decisions were already
recorded in ``.working/pending-decisions.md``. The failure was skipping the compute-first
/ check-before-asking gate (clarify-before-acting): the answer was a findable fact in the
decision stores, and the assistant asked instead of reading. This hook is the mechanical
backstop for that discipline, the AskUserQuestion analogue of the pipe-guard and the
unattended-question guard.

What it does: reads the PreToolUse JSON payload on stdin (the ``AskUserQuestion`` tool
input carries a ``questions`` array), extracts the DISTINCTIVE decision keys from each
question's text (backlog section tokens like ``section 3.69`` / a bare ``3.69`` written
as ``§3.69``, and coded backlog ids like ``FR-205`` / ``GR-13`` / ``SR-3``), and greps
the decision stores for each key. If a key already appears in a store, the hook BLOCKS
(exit 2) and prints the matching store lines, so the assistant reads the recorded decision
instead of re-asking. A question that carries no decision key (a genuinely novel decision)
or whose keys are absent from the stores is ALLOWED.

Decision stores searched (whichever exist; adopter-safe):
  - ``.working/pending-decisions.md`` (the live + resolved decision queue)
  - ``../grc_library_private/design-decisions.md`` (the durable design-decision record)
  - ``.working/DONE.md`` (closed-item ledger, records the disposition)

Over-matching is deliberately toward BLOCKING (a false block costs one re-check and a
clarifying note; a false allow re-asks the maintainer, the failure this prevents). The
companion forcing-function tool ``tools/decisions-search.py`` runs the same search on
demand, and the CLAUDE.md "search decisions before asking" discipline is the primary
control; this hook is defence-in-depth.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds
stderr back to the model as the reason. Fail-OPEN on any parse/read failure or when no
store is readable: this is a guardrail against one mistake shape, not a security boundary,
and a hook that blocked on a malformed payload or an absent store (an adopter clone) would
be worse than the mistake it prevents. NOTE: like the sibling guards, this hook does not
fire in a child session whose ``CLAUDE_PROJECT_DIR`` is unset (documented harness
limitation); the discipline is the primary control either way. SECOND LIMITATION (the
#1041 verifier's residual): the hook reads the question from ``tool_input.questions`` (with
a ``toolInput`` fallback); if the live Claude Code ``AskUserQuestion`` PreToolUse payload
nests the questions differently, ``extract_keys`` returns empty and the hook silently
no-ops (fail-open, never a false block). That is fail-safe, but it means the hook can be
decorative if the schema differs, so the CLAUDE.md "search decisions before asking"
discipline and the ``tools/decisions-search.py`` on-demand search are the LOAD-BEARING
control; this hook is defence-in-depth on top of them, not a substitute.

Self-test: ``python3 .claude/hooks/block-answered-question.py --self-test``.
"""

import json
import os
import re
import sys
from pathlib import Path

# Distinctive decision keys the hook extracts from a question's text.
# 1) A section token written with the section glyph or the word "section":
#    "§3.69", "§ 1.22.5", "section 3.68". Captured as the numeric part ("3.69").
SECTION_RE = re.compile(r"(?:§|\bsection\b)\s*(\d+(?:\.\d+)+)", re.IGNORECASE)
# 2) A coded BACKLOG id: FR-205, GR-13, SR-3, DD-12, RB-6, FIT-8, FQ-1, GAP-1, P-3.
#    Restricted to the KNOWN backlog-id prefixes, NOT any `[A-Z]{1,4}-\d+`: the corpus is
#    full of control codes (`SEF-07`, `IAM-09`) and hyphen-numeric statute codes (`A-2.1`)
#    that share the generic shape and would over-block a genuinely novel security/privacy
#    question that merely mentions one (the #1041 verifier's finding). A new backlog-id
#    prefix is added here; section-number detection covers the rest.
CODED_ID_RE = re.compile(r"\b((?:FR|SR|GR|DD|RB|FIT|FQ|GAP|P)-\d+)\b")

STORE_RELPATHS = [
    (".working/pending-decisions.md", False),
    ("../grc_library_private/design-decisions.md", True),  # sibling; may be absent
    (".working/DONE.md", False),
]


def extract_keys(text: str) -> list[str]:
    """Return the distinctive decision keys found in the question text, deduped,
    order-preserving. A key is a section number ("3.69") or a coded id ("FR-205")."""
    keys: list[str] = []
    seen: set[str] = set()
    for m in SECTION_RE.finditer(text):
        k = m.group(1)
        if k not in seen:
            seen.add(k)
            keys.append(k)
    for m in CODED_ID_RE.finditer(text):
        k = m.group(1)
        if k not in seen:
            seen.add(k)
            keys.append(k)
    return keys


def _questions_text(payload: dict) -> str:
    """Concatenate every question + option label/description from the tool input."""
    tool_input = payload.get("tool_input") or payload.get("toolInput") or {}
    parts: list[str] = []
    for q in tool_input.get("questions", []) or []:
        if not isinstance(q, dict):
            continue
        parts.append(str(q.get("question", "")))
        parts.append(str(q.get("header", "")))
        for opt in q.get("options", []) or []:
            if isinstance(opt, dict):
                parts.append(str(opt.get("label", "")))
                parts.append(str(opt.get("description", "")))
    return "\n".join(parts)


def _read_stores(project_dir: str) -> list[tuple[str, str]]:
    """Return [(store_label, text), ...] for each readable store."""
    base = Path(project_dir)
    out: list[tuple[str, str]] = []
    for rel, _sibling in STORE_RELPATHS:
        p = (base / rel).resolve()
        try:
            out.append((rel, p.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            continue
    return out


def find_matches(keys: list[str], stores: list[tuple[str, str]]) -> list[str]:
    """Return human-readable 'store:line' hits for keys that appear in any store.
    A section key '3.69' matches a store token '3.69' or '3.69a' (word-ish boundary
    that tolerates a trailing letter but not a longer number, so '3.6' does not match
    '3.69')."""
    hits: list[str] = []
    for key in keys:
        if re.fullmatch(r"\d+(?:\.\d+)+", key):
            # section number: allow an optional trailing lowercase letter, forbid a
            # trailing digit or dot (so 3.6 != 3.69 and 3.69 != 3.691)
            pat = re.compile(r"(?<![\d.])" + re.escape(key) + r"[a-z]?(?![\d.])")
        else:
            pat = re.compile(r"\b" + re.escape(key) + r"\b")
        for label, text in stores:
            for ln in text.splitlines():
                if pat.search(ln):
                    snippet = ln.strip()
                    if len(snippet) > 240:
                        snippet = snippet[:240] + " ..."
                    hits.append(f"[{label}] key `{key}`: {snippet}")
                    break  # one representative line per (key, store) is enough
    return hits


def decide(payload: dict, project_dir: str) -> tuple[bool, str]:
    text = _questions_text(payload)
    keys = extract_keys(text)
    if not keys:
        return False, ""  # no decision key -> genuinely novel question, allow
    stores = _read_stores(project_dir)
    if not stores:
        return False, ""  # adopter / no stores -> fail-open
    hits = find_matches(keys, stores)
    if not hits:
        return False, ""
    body = "\n".join(f"  - {h}" for h in hits)
    reason = (
        "AskUserQuestion BLOCKED (answered-question guardrail): this question references "
        "a backlog key that ALREADY appears in the decision stores, so the answer may be "
        "recorded. READ the matched lines below (and run `python3 tools/decisions-search.py "
        "<key>` for full context) BEFORE asking the maintainer; re-asking a decided question "
        "wastes their time (the failure this guard prevents).\n"
        f"{body}\n"
        "If, after reading, the decision is genuinely NOT recorded (the match is a "
        "different, still-open aspect), re-issue the question with the distinctive key "
        "removed or reworded so it does not collide, or note in the question that you "
        "checked the store and the specific sub-decision is unrecorded."
    )
    return True, reason


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # fail-open
    workspace = payload.get("workspace") or {}
    project_dir = (
        workspace.get("project_dir")
        or os.environ.get("CLAUDE_PROJECT_DIR")
        or "/home/jposluns/grc_library"
    )
    try:
        block, reason = decide(payload, project_dir)
    except Exception:
        return 0  # fail-open on any unexpected error
    if block:
        try:
            from _hook_state import record_block, subject_from_payload
            record_block(subject_from_payload(payload), "answered-question")
        except Exception:
            pass
        print(reason, file=sys.stderr)
        return 2
    return 0


def _self_test() -> int:
    import tempfile
    import unittest

    STORE = (
        "- **3.69 MFA (SUPERSEDES the 2026-07-14 block):** apply type-anchored wording "
        "across the three docs; service accounts exempt where documented.\n"
        "- **3.70** = TIGHTEN the two dev-security crypto tables to P-384 / RSA-4096.\n"
        "- **FR-205 MFA scope = OPTION A**: harmonize to all user/interactive + remote.\n"
        "Some unrelated line about section 3.101 tooling.\n"
    )

    def payload_for(qtext, opts=None):
        return {
            "tool_input": {
                "questions": [
                    {"question": qtext, "header": "h", "options": opts or []}
                ]
            }
        }

    class T(unittest.TestCase):
        def setUp(self):
            self.d = tempfile.mkdtemp()
            wk = Path(self.d) / ".working"
            wk.mkdir()
            (wk / "pending-decisions.md").write_text(STORE, encoding="utf-8")
            (wk / "DONE.md").write_text("", encoding="utf-8")

        def test_extract_section_glyph(self):
            self.assertIn("3.69", extract_keys("what about §3.69 MFA?"))

        def test_extract_section_word(self):
            self.assertIn("3.68", extract_keys("section 3.68 vuln-SLA"))

        def test_extract_coded_id(self):
            self.assertIn("FR-205", extract_keys("the FR-205 fork"))

        def test_control_codes_not_extracted(self):
            # corpus control codes / statute codes must NOT become keys (the #1041
            # verifier's over-block finding): SEF-07, IAM-09, A-2.1 are not backlog ids
            for token in ("SEF-07", "IAM-09", "A-2.1", "ISO-27001"):
                self.assertEqual(
                    [k for k in extract_keys(f"question about {token}?")
                     if k.upper() == token.split(".")[0].upper()],
                    [],
                    f"{token} should not be extracted as a backlog id",
                )

        def test_novel_control_code_question_allowed(self):
            # a novel question mentioning a control code that IS in the store must still
            # be ALLOWED, because the control code is not a backlog-id key
            block, _ = decide(payload_for("Map control SEF-07 to which doc?"), self.d)
            self.assertFalse(block)

        def test_block_on_recorded_section(self):
            block, reason = decide(payload_for("Decide §3.69 MFA scope"), self.d)
            self.assertTrue(block)
            self.assertIn("3.69", reason)

        def test_block_on_recorded_coded_id(self):
            block, _ = decide(payload_for("FR-205 MFA scope fork?"), self.d)
            self.assertTrue(block)

        def test_allow_novel_section(self):
            # 3.999 is not in the store
            block, _ = decide(payload_for("new item §3.999 design?"), self.d)
            self.assertFalse(block)

        def test_allow_no_key(self):
            block, _ = decide(payload_for("Should I use blue or green?"), self.d)
            self.assertFalse(block)

        def test_section_boundary_no_false_prefix(self):
            # asking about 3.6 must not match the store's 3.69 / 3.70
            block, _ = decide(payload_for("what about §3.6 today?"), self.d)
            self.assertFalse(block)

        def test_option_text_scanned(self):
            block, _ = decide(
                payload_for("Pick one", [{"label": "x", "description": "per §3.70"}]),
                self.d,
            )
            self.assertTrue(block)

        def test_fail_open_no_stores(self):
            block, _ = decide(payload_for("§3.69?"), tempfile.mkdtemp())
            self.assertFalse(block)

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
