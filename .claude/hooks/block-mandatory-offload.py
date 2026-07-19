#!/usr/bin/env python3
"""PreToolUse hook (Task / Agent): block the orchestrator from self-running an offloadable
pass while live workers are available.

Shipped 2026-07-19 after the orchestrator repeatedly self-ran offloadable QA passes (the
`/validate-pr` Subagent A) while live credit-offload workers sat idle, spending scarce
orchestrator credits that do not renew for days. The maintainer directed a HARD guardrail: "If
a worker CAN do something and workers are available, USE THEM. If no workers are available and
on a VM, ALERT the maintainer that the workers are stalled, or obtain explicit authorization to
proceed without workers." This hook is the mechanical backstop for that rule; the CLAUDE.md
`## Mandatory worker offload` discipline is the primary control, and this is defence-in-depth.

What it does: on a Task / Agent subagent dispatch, it reads the dispatched prompt, classifies
whether the subagent would run an OFFLOADABLE pass, and if so consults the scratch worker
registry:

  - offloadable AND >= 1 live worker  -> BLOCK (exit 2): enqueue a credit-offload order instead
    of self-running (or record explicit maintainer authorization to self-run anyway).
  - offloadable AND 0 live workers    -> ALLOW (exit 0) with a stderr WARNING: per the rule the
    orchestrator must alert the maintainer that the workers are stalled, or confirm authorization
    to self-run. A hook cannot force the alert; it warns.
  - not offloadable, or not a Task / Agent call -> ALLOW silently.

Detection heuristic (the hard part): a genuinely-offloadable `/validate-pr` Subagent A and a
legitimate ORCHESTRATOR-SIDE pre-push skeptical verifier are both "refute-briefed subagents on a
diff". This hook checks an ALLOW-OVERRIDE marker set FIRST (the critical-path verifiers that must
never be blocked), and only then a BLOCK-TRIGGER marker set (the offloadable QA-pass skills). The
override-first order means a prompt that names both (for example "pre-push validate-pr-style
review") is ALLOWED, biasing the residual error toward a false ALLOW (a missed offload, which the
CLAUDE.md rule and the maintainer still catch) rather than a false BLOCK (stopping a legitimate
critical-path verifier, which would be worse). Research / draft seeds, AND a bare `verify` pass,
are deliberately NOT mechanically detected here (too generic / fuzzy to separate from legitimate
orchestrator-side analysis without a high false-block rate; `verify` in particular is both the
offloaded verify pass AND the always-allowed pre-push verifier, so a bare-word marker cannot tell
them apart); the CLAUDE.md rule covers them, this hook targets the mechanically-detectable QA
passes that drove the failure.

Severity: BLOCK (exit 2) by default, because the maintainer directed a HARD guardrail and a WARN
is exactly the "auto-pilot ignores it" failure mode that let the orchestrator self-run
repeatedly; the override allowlist is the safety valve for legitimate verifiers. Flip the module
constant `BLOCK_SEVERITY = False` to downgrade to WARN-only (exit 0 + stderr) if the maintainer
prefers to preserve flow over enforcement. See the delivery MANIFEST for the full tradeoff.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds
stderr back to the model as the reason. Fail-OPEN on any parse/registry error (never break the
session; a guardrail, not a security boundary). Like the sibling guards, it does not fire in a
child session whose `CLAUDE_PROJECT_DIR` is unset (documented harness limitation); the CLAUDE.md
rule is the primary control either way. This hook lives in `grc_library/.claude/` and so fires in
the ORCHESTRATOR's session; a worker session (cwd in `grc_library_scratch`) does not load it, so
a worker legitimately dispatching subagents to run ITS claimed pass is unaffected.

Self-test: `python3 .claude/hooks/block-mandatory-offload.py --self-test`.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# BLOCK (exit 2) when offloadable and workers are live; set False for WARN-only (exit 0).
BLOCK_SEVERITY = True

# The subagent-dispatch tool names this hook targets (Claude Code exposes it as "Task"; some
# surfaces name it "Agent"). A matcher of "Task|Agent" scopes the hook, and this set is the
# belt-and-suspenders re-check inside the hook.
DISPATCH_TOOLS = {"Task", "Agent"}

# Live-worker freshness window: a worker whose last_seen is older than this is not counted live
# (mirrors the ~20-minute stale-scan window used by the credit-offload queue).
LIVE_WINDOW_SEC = 20 * 60

# ALLOW-OVERRIDE markers, checked FIRST: the critical-path, orchestrator-side verifiers that must
# never be blocked even though they resemble an offloadable diff review.
OVERRIDE_MARKERS = (
    "pre-push",
    "before push",
    "before pushing",
    "skeptical verifier",
    "skeptical review",
    "high-assurance",
    "high assurance",
    "adversarial verifier",
    "adversarial verification",
    "critical-path verifier",
)

# BLOCK-TRIGGER markers: the offloadable QA-pass skills (the mechanically-detectable set from the
# `## Mandatory worker offload` offloadable inventory). Kept specific (slash forms and hyphenated skill
# names) to minimize false positives on ordinary prose.
BLOCK_MARKERS = (
    "validate-pr",
    "/validate",            # also covers a corpus-wide /validate sweep
    "validation-sweep",
    "matrix-fit",
    "claim-fit",
    "reference-audit",
    "screen-publications",
    "screen publications",
    "full-qa",
    "/fitness",
    "library-fitness",
    "deep-assessment",      # the read-only probe phases are offloadable
)


def _dispatch_text(payload: dict) -> str:
    """The prompt / description text of a Task / Agent dispatch, joined. '' on any error."""
    try:
        ti = payload.get("tool_input") or payload.get("toolInput") or {}
        parts = [
            str(ti.get("prompt", "")),
            str(ti.get("description", "")),
            str(ti.get("subagent_type", "")),
        ]
        return "\n".join(p for p in parts if p)
    except Exception:
        return ""


def _is_dispatch(payload: dict) -> bool:
    name = payload.get("tool_name") or payload.get("toolName") or ""
    return name in DISPATCH_TOOLS


def classify(text: str) -> str:
    """Return 'override' (never block), 'offloadable' (block-trigger present and no override), or
    'other' (allow). Override is checked first, so a mixed prompt biases toward allow."""
    if not isinstance(text, str) or not text.strip():
        return "other"
    low = text.lower()
    if any(m in low for m in OVERRIDE_MARKERS):
        return "override"
    if any(m in low for m in BLOCK_MARKERS):
        return "offloadable"
    return "other"


def _scratch_dir(project_dir: str) -> Path:
    return Path(project_dir).resolve().parent / "grc_library_scratch"


def _parse_last_seen(text: str):
    """Best-effort: return a timezone-aware datetime from a `last_seen:` ISO-Z line, else None."""
    import re
    m = re.search(r"last_seen[:\*\s]+([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)", text)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def count_live_workers(project_dir: str):
    """Return (count, source) of live workers, or (None, reason) if the registry is unreadable
    (fail-open signal). Primary: shell out to the queue helper's list-workers and count [LIVE];
    fallback: read workers/*.md and count status active within the freshness window."""
    scratch = _scratch_dir(project_dir)
    # Primary: the helper computes [LIVE] authoritatively.
    try:
        helper = scratch / "tools" / "credit-offload-queue.py"
        if helper.is_file():
            r = subprocess.run(
                [sys.executable, str(helper), "list-workers"],
                capture_output=True, text=True, cwd=str(scratch), timeout=20,
            )
            if r.returncode == 0 and r.stdout:
                return sum(1 for ln in r.stdout.splitlines() if "[LIVE]" in ln), "list-workers"
    except Exception:
        pass
    # Fallback: read the registry files directly.
    try:
        wdir = scratch / "workers"
        if not wdir.is_dir():
            return None, "no-registry"
        now = datetime.now(timezone.utc)
        count = 0
        found_any = False
        for f in sorted(wdir.glob("*.md")):
            if f.name == "README.md":
                continue
            found_any = True
            txt = f.read_text(encoding="utf-8", errors="replace")
            if "status:" in txt.lower() and "active" not in txt.lower():
                continue
            ls = _parse_last_seen(txt)
            if ls is not None and (now - ls).total_seconds() <= LIVE_WINDOW_SEC:
                count += 1
        if not found_any:
            return None, "no-registry"
        return count, "workers-dir"
    except Exception:
        return None, "unreadable"


def decide(payload: dict, project_dir: str):
    """Return (block, reason). block True -> exit 2; block False with a reason -> exit 0 + WARN;
    block False with '' -> silent allow."""
    if not _is_dispatch(payload):
        return False, ""
    kind = classify(_dispatch_text(payload))
    if kind != "offloadable":
        return False, ""  # override or other -> allow silently
    live, source = count_live_workers(project_dir)
    if live is None:
        return False, ""  # registry unreadable -> fail-open (allow silently)
    if live <= 0:
        return False, (
            "MANDATORY-OFFLOAD (warning, 0 live workers): this looks like an OFFLOADABLE pass "
            "and NO credit-offload worker is currently live. Per the maintainer's hard rule, do "
            "NOT silently self-run: ALERT the maintainer that the workers are stalled (on a VM), "
            "or record explicit authorization to proceed without workers, before running this "
            "inline. (Registry source: " + source + ".)"
        )
    reason = (
        "BLOCKED (mandatory-offload guardrail): this dispatch looks like an OFFLOADABLE pass and "
        f"{live} credit-offload worker(s) are LIVE. Do not self-run it and spend scarce "
        "orchestrator credits: ENQUEUE a credit-offload order (`python3 "
        "../grc_library_scratch/tools/credit-offload-queue.py` per the `## Mandatory worker offload` "
        "discipline) and consume the delivered result. To self-run anyway, first record explicit "
        "maintainer authorization. If this is actually a critical-path verifier (pre-push / "
        "skeptical / high-assurance / adversarial), name that in the prompt so the override "
        "allows it. (Registry source: " + source + ".)"
    )
    return True, reason


def main(argv: list) -> int:
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
        # Last-resort fallback: resolve the project root from this hook's own location
        # (<project>/.claude/hooks/this.py -> parents[2]). No hardcoded path, so it stays
        # correct across a repo move (for example /home/jposluns -> /home/grc).
        or str(Path(__file__).resolve().parents[2])
    )
    try:
        block, reason = decide(payload, project_dir)
    except Exception:
        return 0  # fail-open on any unexpected error
    if block and BLOCK_SEVERITY:
        print(reason, file=sys.stderr)
        return 2
    if reason:  # WARN path (0 workers, or block downgraded to WARN)
        print(reason, file=sys.stderr)
    return 0


def _self_test() -> int:
    import tempfile
    import unittest

    def payload(tool="Task", prompt="", desc="", project=None):
        p = {"tool_name": tool, "tool_input": {"prompt": prompt, "description": desc}}
        if project is not None:
            p["workspace"] = {"project_dir": project}
        return p

    class T(unittest.TestCase):
        def setUp(self):
            # Build a fake colocation <parent>/{grc_library, grc_library_scratch/workers}
            self.parent = tempfile.mkdtemp()
            self.proj = Path(self.parent) / "grc_library"
            (self.proj).mkdir(parents=True)
            self.wdir = Path(self.parent) / "grc_library_scratch" / "workers"
            self.wdir.mkdir(parents=True)

        def _write_worker(self, name, age_sec, status="active"):
            ts = datetime.now(timezone.utc)
            ts = ts.replace(microsecond=0)
            from datetime import timedelta
            stamp = (ts - timedelta(seconds=age_sec)).strftime("%Y-%m-%dT%H:%M:%SZ")
            (self.wdir / f"{name}.md").write_text(
                f"# Worker {name}\n- **status:** {status}\n- **last_seen:** {stamp}\n",
                encoding="utf-8",
            )

        def test_non_dispatch_tool_allowed(self):
            b, r = decide(payload(tool="Bash", prompt="validate-pr", project=str(self.proj)),
                          str(self.proj))
            self.assertFalse(b)
            self.assertEqual(r, "")

        def test_offloadable_with_live_worker_blocks(self):
            self._write_worker("w-a", 60)  # fresh
            b, r = decide(payload(prompt="run the /validate-pr Subagent A on this diff",
                                  project=str(self.proj)), str(self.proj))
            self.assertTrue(b)
            self.assertIn("BLOCKED (mandatory-offload", r)

        def test_offloadable_with_zero_workers_warns_allows(self):
            self._write_worker("w-a", 999999)  # stale -> not live
            b, r = decide(payload(prompt="run a /matrix-fit sweep", project=str(self.proj)),
                          str(self.proj))
            self.assertFalse(b)          # allow
            self.assertIn("0 live workers", r)  # but warn

        def test_pre_push_verifier_allowed_even_with_workers(self):
            self._write_worker("w-a", 60)
            b, r = decide(payload(prompt="pre-push skeptical verifier: refute this diff before "
                                         "push", project=str(self.proj)), str(self.proj))
            self.assertFalse(b)
            self.assertEqual(r, "")

        def test_override_wins_over_block_marker(self):
            self._write_worker("w-a", 60)
            # names both a block trigger and an override marker -> override wins -> allow
            b, r = decide(payload(prompt="high-assurance adversarial verifier, validate-pr style",
                                  project=str(self.proj)), str(self.proj))
            self.assertFalse(b)

        def test_non_offloadable_prompt_allowed(self):
            self._write_worker("w-a", 60)
            b, r = decide(payload(prompt="author the CHANGELOG entry for this PR",
                                  project=str(self.proj)), str(self.proj))
            self.assertFalse(b)
            self.assertEqual(r, "")

        def test_registry_unreadable_fails_open(self):
            # point project_dir where no sibling scratch/workers exists
            lonely = tempfile.mkdtemp()
            proj = Path(lonely) / "grc_library"
            proj.mkdir()
            b, r = decide(payload(prompt="/validate-pr", project=str(proj)), str(proj))
            self.assertFalse(b)          # fail-open allow
            self.assertEqual(r, "")

        def test_malformed_payload_fails_open(self):
            b, r = decide({"tool_name": "Task"}, str(self.proj))  # no tool_input
            self.assertFalse(b)

        def test_classify_helper(self):
            self.assertEqual(classify("run /validate-pr"), "offloadable")
            self.assertEqual(classify("pre-push verifier"), "override")
            self.assertEqual(classify("write the docs"), "other")
            self.assertEqual(classify(""), "other")

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
