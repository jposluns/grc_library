#!/usr/bin/env python3
"""Stop hook: when the assistant's last message discusses 'session' and 'depth' in
proximity, surface the FACTUAL session length and compaction count, not inference.

Maintainer-directed 2026-08-15: "add a hook when you use the term 'session' and 'depth'
within a few words or in the same sentence to include the session length and number of
compactions, so i can see facts, not inference." The orchestrator had repeatedly asserted
"session depth"/"deep session" as an un-instrumented inference (the evidence-grounded-
completion un-observable-state failure); this replaces the felt inference with the two
externally-observable numbers the maintainer actually tracks.

NON-BLOCKING: emits the facts via the hook `systemMessage` field (shown to the maintainer),
never blocks turn-end. FAIL OPEN on any error, a personal instrument must never trap the run.
MAINTAINER-ORCHESTRATOR-ONLY: reads degradation-watch-log.md from the operational store (via lint_common.resolve_working); if that is
absent (adopter, or the operational store not present) it is a silent no-op.

Fact sources (the maintainer's own metric log):
  * session length  = now minus the newest `session-start` ISO timestamp.
  * compaction count = canonical `| <iso> | compaction |` rows with ts >= session-start.
"""
import sys, os, re, json
from pathlib import Path
from datetime import datetime, timezone

# The settings.json launcher runs `python3 -I` (SECI-config-is-executable-trust-gate):
# the helpers (_hookutil, lint_common) are loaded at their call sites via _load_sibling,
# ONLY from reviewed source bytes; no directory ever enters sys.path and no import
# statement names them. MISSING-HELPER BEHAVIOUR: worker detection falls back to False
# and the facts surface exits silently (rc 0).
def _load_sibling(name, _cache={}):
    """Execute a reviewed repository helper's .py SOURCE BYTES and return the module.

    SECI-config-is-executable-trust-gate: the settings.json launcher runs `python3 -I`,
    this function never touches sys.path and never uses import machinery for the
    helper, so nothing planted beside a hook (a stdlib-named decoy module, a
    __pycache__/*.pyc) can execute, and no bytecode cache is ever read or written.
    Containment is decided on the path AS LAUNCHED, before any symlink resolution:
    os.path.abspath(__file__) (unresolved) must sit at <root>/.claude/hooks/<hook>.py,
    and every component from that root down to the hook and down to the helper (the
    root itself, .claude, .claude/hooks, tools, the hook file and the helper file)
    must not be a symlink; only then are real paths compared, requiring the hook's and
    the helper's real locations to sit at exactly their expected places under the real
    repository root (ancestors ABOVE the root may be symlinks: both sides of each
    comparison resolve them identically). Any violation is REFUSED fail-closed: exit 2
    with a clear message, raised as SystemExit so the hooks' fail-open
    `except Exception` guards cannot swallow it. A MISSING helper is different: the
    plain OSError propagates to the caller, which takes this hook's documented
    missing-helper behaviour, never a sys.modules fallback.

    TEST-ONLY SEAM: when this hook is loaded AS A MODULE by the in-repo test harness
    (__name__ != "__main__"), a helper already present in sys.modules is reused, which
    preserves the patch-the-helper-then-load-the-hook test contract. A production launch
    is always a direct execution (__name__ == "__main__"), and neither the environment
    nor any file in the tree can change that, so a production load NEVER consults a
    pre-existing sys.modules entry: it always re-executes the reviewed source and
    overwrites the entry (dependencies included: todo_index_rows reads lint_common from
    the entry this loader has just written).
    """
    import os.path
    import sys
    if name in _cache:
        return _cache[name]
    if __name__ != "__main__" and name in sys.modules:
        _cache[name] = sys.modules[name]
        return _cache[name]

    def _refuse(why):
        print("BLOCKED (hook-helper-isolation): " + why + "; refusing to execute "
              "anything but the reviewed helper sources.", file=sys.stderr)
        sys.exit(2)

    hook_path = os.path.abspath(__file__)  # the path AS LAUNCHED, symlinks unresolved
    hooks_dir = os.path.dirname(hook_path)
    claude_dir = os.path.dirname(hooks_dir)
    root = os.path.dirname(claude_dir)
    if os.path.basename(hooks_dir) != "hooks" or os.path.basename(claude_dir) != ".claude":
        _refuse("this hook's launch path " + hook_path + " is not under "
                "<repo-root>/.claude/hooks, so no repository root can anchor helper "
                "containment")
    parts = (".claude", "hooks") if name.startswith("_") else ("tools",)
    helper_dir = os.path.join(root, *parts)
    helper_path = os.path.join(helper_dir, name + ".py")
    for p in (root, claude_dir, hooks_dir, hook_path, helper_dir, helper_path):
        if os.path.islink(p):
            _refuse(p + " is a symlink on the path as launched (containment is "
                    "decided before any symlink resolution)")
    real_root = os.path.realpath(root)
    if os.path.realpath(hook_path) != os.path.join(real_root, ".claude", "hooks",
                                                   os.path.basename(hook_path)):
        _refuse("this hook's real location " + os.path.realpath(hook_path)
                + " does not sit at its launch-path place under the real repository "
                "root " + real_root)
    if os.path.realpath(helper_path) != os.path.join(real_root, *parts, name + ".py"):
        _refuse("helper " + helper_path + " does not resolve to its expected place "
                "under the real repository root " + real_root)
    for dep in {"todo_index_rows": ("lint_common",)}.get(name, ()):
        _load_sibling(dep)
    with open(helper_path, "rb") as fh:
        source = fh.read()
    module = type(sys)(name)
    module.__file__ = helper_path
    exec(compile(source, helper_path, "exec", dont_inherit=True), module.__dict__)
    sys.modules[name] = module
    _cache[name] = module
    return module


ISO = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z)"  # seconds OPTIONAL: the degradation log's dominant form is minute-only (handoff-snapshot.py:211)

# --- session-start matcher (KEEP IN LOCKSTEP with tools/handoff-snapshot.py) ---
# A row is a session-start entry when the TYPE TOKEN `session-start` heads the row (after
# optional bullet/heading/table markers and an optional leading ISO), NOT when the substring
# appears inside another row's prose note (a compaction/considered DECOY). Two cases:
# ISO-before-token (table iso-first, bullet iso-first, bold-iso) and token-first (bare, bullet,
# ###, table token-first, reversed inline). `(?![\w-])` rejects `session-start-<suffix>`.
# Reality-validated against the live degradation log: 87/87 real rows, 0 decoys.
_SS_RE_B = re.compile(r"^[\s\-#>|]*(?:\*\*)?" + ISO + r"(?:\*\*)?\s*\|?\s*session-start(?![\w-])")
_SS_RE_A = re.compile(r"^[\s\-#>|]*session-start(?![\w-])[:\s|]")
# NOTE: this matcher is deliberately LINE-ANCHORED (session-start must HEAD its row after optional
# markers). That anchoring IS the decoy-exclusion mechanism: a session-start mentioned inside another
# row's note (a compaction/considered decoy, INCLUDING a quoted `| session-start <iso>`) sits on a line
# that starts with the OTHER row's structure, so it never matches. ASSUMPTION: one record per physical
# line. A record concatenated onto another row's line (a write that dropped the trailing newline) is a
# DATA defect to correct in the log, NOT to parse here: matching it mid-line reintroduces the
# prose-decoy ambiguity (codex #1759 iter-2 proved a mid-line Case-C leaks quoted-pipe decoys).


def _session_start_stamps(text):
    """Every session-start row's ISO stamp, TYPE-token-keyed (excludes prose/decoy mentions)."""
    out = []
    for ln in text.splitlines():
        m = _SS_RE_B.match(ln)
        if m:
            out.append(m.group(1))
            continue
        if _SS_RE_A.match(ln):
            m2 = re.search(ISO, ln)
            if m2:
                out.append(m2.group(1))
    return out



def _fail_open():
    sys.exit(0)


def _parse(ts):
    # Accept BOTH minute-only (the log's dominant form) and full-seconds ISO stamps.
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ"):
        try:
            return datetime.strptime(ts, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"unparseable timestamp: {ts!r}")


def _last_assistant_text(transcript_path):
    try:
        with open(transcript_path, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return ""
    for ln in reversed(lines):
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        if obj.get("type") == "assistant":
            parts = obj.get("message", {}).get("content", [])
            return " ".join(
                p.get("text", "")
                for p in parts
                if isinstance(p, dict) and p.get("type") == "text"
            )
    return ""


def _has_pair(text):
    # primary: any sentence containing both 'session' and 'depth' (word-boundary, ci)
    for sent in re.split(r"[.!?\n]+", text):
        low = sent.lower()
        if re.search(r"\bsession", low) and re.search(r"\bdepth", low):
            return True
    # fallback: the two tokens within ~45 chars ("within a few words")
    low = text.lower()
    for m in re.finditer(r"\bsession", low):
        if "depth" in low[m.start(): m.start() + 45]:
            return True
    for m in re.finditer(r"\bdepth", low):
        if "session" in low[max(0, m.start() - 45): m.start()]:
            return True
    return False


def _is_worker() -> bool:
    """Dispatched orch-verify worker? Session-discipline hooks are orchestrator-scoped and no-op in a
    worker (WK-HOOK1: the stamp hook made every claude worker re-send its whole deliverable). Fail-safe:
    any detection error -> False (keep orchestrator behaviour, the status quo)."""
    try:
        return _load_sibling("_hookutil").is_verify_worker()
    except Exception:
        return False


def main():
    if "--self-test" not in sys.argv and _is_worker():
        return
    try:
        payload = json.load(sys.stdin)
    except Exception:
        _fail_open()
    tp = payload.get("transcript_path")
    if not tp or not os.path.exists(tp):
        _fail_open()
    text = _last_assistant_text(tp)
    if not text or not _has_pair(text):
        _fail_open()
    repo = Path(os.environ.get("CLAUDE_PROJECT_DIR") or str(Path(__file__).resolve().parents[2])).resolve()
    try:
        resolve_working = _load_sibling("lint_common").resolve_working
        log_path = resolve_working("degradation-watch-log.md", repo_root=repo)
    except Exception:
        _fail_open()
    if log_path is None or not log_path.exists():
        _fail_open()
    try:
        content = log_path.read_text(encoding="utf-8")
    except Exception:
        _fail_open()
    # TYPE-token-keyed session-start detection (see _session_start_stamps): recalls all
    # live layout variants (table both directions, bullet both directions, bold-iso, colon,
    # ### heading, bare) and excludes decoy prose (a compaction/considered row's note).
    starts = _session_start_stamps(content)
    if not starts:
        _fail_open()
    start_ts = max(starts, key=_parse)
    start_dt = _parse(start_ts)
    now = datetime.now(timezone.utc)
    secs = (now - start_dt).total_seconds()
    h, mm = int(secs // 3600), int((secs % 3600) // 60)
    comp = 0
    for ln in content.splitlines():
        m = re.match(r"\|\s*" + ISO + r"\s*\|\s*compaction\s*\|", ln)
        if m and _parse(m.group(1)) >= start_dt:
            comp += 1
    facts = (
        f"SESSION FACTS (not inference): length {h}h{mm:02d}m "
        f"(session-start {start_ts} UTC); compactions this session: {comp}. "
        f"Hold any session-depth / length / degradation claim against these numbers."
    )
    print(json.dumps({"systemMessage": facts}))
    sys.exit(0)


def _self_test():
    # Reality fixture (guard-input discipline): the degradation log's dominant form is
    # MINUTE-ONLY; the pre-fix regex/_parse silently missed it. Assert both forms parse and
    # that the minute-only start is selected as newest, mirroring handoff-snapshot.py's fixture.
    assert _parse("2026-08-27T15:30Z").minute == 30          # minute-only parses
    assert _parse("2026-07-29T12:00:00Z").second == 0        # full-seconds still parses
    # Multi-shape reality fixture: every session-start LAYOUT the live log carries, plus a
    # DECOY compaction row whose note mentions session-start with a NEWER iso (must be excluded
    # so it cannot wrongly win max()) and a session-start-<suffix> row (must not match).
    fixture = (
        "| 2026-07-29T10:00:00Z | session-start | table iso-first, full-seconds |\n"
        "| session-start | 2026-07-29T11:00Z | table token-first |\n"
        "session-start | 2026-07-29T12:00:00Z | reversed inline |\n"
        "- session-start 2026-07-29T13:00Z (bullet token-first)\n"
        "- 2026-07-29T14:00:00Z  session-start: bullet iso-first\n"
        "- **2026-07-29T15:00Z** session-start: bold-iso\n"
        "session-start 2026-07-29T16:00:00Z | bare token-first\n"
        "### session-start 2026-07-29T17:00Z\n"
        "- session-start: 2026-07-29T18:30:45Z (bullet colon, the TRUE newest)\n"
        "| 2026-07-29T09:30:00Z | considered | quote: | session-start 2026-12-31T23:59:59Z | end (pipe-prose decoy, codex #1759 iter-2) |\n"
        "| 2026-07-29T23:59:59Z | compaction | DECOY note mentions session-start 2026-07-29T23:59:59Z |\n"
        "elapsed = now minus the session-start row (prose decoy)\n"
        "session-start-continuation 2026-07-29T22:00Z (suffix decoy)\n"
        "| 2026-07-29T13:00Z | compaction | C1 |\n"
    )
    starts = _session_start_stamps(fixture)
    reals = {"2026-07-29T10:00:00Z", "2026-07-29T11:00Z", "2026-07-29T12:00:00Z",
             "2026-07-29T13:00Z", "2026-07-29T14:00:00Z", "2026-07-29T15:00Z",
             "2026-07-29T16:00:00Z", "2026-07-29T17:00Z", "2026-07-29T18:30:45Z"}
    assert reals <= set(starts), ("recall gap", reals - set(starts))          # all 9 shapes recalled
    assert "2026-07-29T23:59:59Z" not in starts, "DECOY compaction iso leaked"  # decoy excluded
    assert "2026-07-29T22:00Z" not in starts, "session-start-<suffix> leaked"    # suffix excluded
    assert "2026-12-31T23:59:59Z" not in starts, "pipe-prose decoy iso leaked (would wrongly win newest)"
    assert "2026-07-29T09:30:00Z" not in starts, "decoy host considered-row iso leaked"
    assert max(starts, key=_parse) == "2026-07-29T18:30:45Z", max(starts, key=_parse)  # not the newer decoy
    comp = sum(1 for ln in fixture.splitlines()
               if re.match(r"\|\s*" + ISO + r"\s*\|\s*compaction\s*\|", ln))
    assert comp == 2, comp                                    # two compaction rows counted
    print("surface-session-facts self-test: shape-recall + decoy-exclusion + minute-only PASS")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        _self_test()
        sys.exit(0)
    try:
        main()
    except Exception:
        _fail_open()
