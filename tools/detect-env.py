#!/usr/bin/env python3
"""Execution-environment detection for session start (/resume step aid).

WHAT THIS IS (and is NOT). An advisory orchestrator dev-AID (#724), not a
gate. It always exits 0 after printing its report (2 only on internal error). The
project runs across materially-different execution environments (a managed cloud
sandbox; the maintainer's local NUC) whose transport and tooling assumptions
diverge in ways a session hits live: the PR mechanism (GitHub MCP vs the `gh`
CLI), the CI-poll and merge transport (GraphQL vs the REST fallback when the
shared 5,000/hr GraphQL pool is exhausted, observed in #687), the stop-hook
auto-commit-push (present in cloud, absent on the NUC), the pipe-guard PreToolUse
hook (fires on the NUC; silent in cloud resumed sessions because
``CLAUDE_PROJECT_DIR`` is unset there, the #677 root cause), egress
reachability per source family, and sibling-repo access. This tool probes what a
SCRIPT can observe and prints one profile block the resume step consumes; the
items only the assistant can observe from its own side (which MCP tools are in
its tool list) are printed as ASSISTANT-PROBE lines for the assistant to fill,
never guessed.

HARD CONSTRAINT (design, not a bug): ``permissions`` and ``additionalDirectories``
bind at session launch; a hook cannot grant them at runtime. Where access is
missing this tool prints the one-line fix for the maintainer (``--add-dir`` or a
machine-local ``.claude/settings.local.json`` entry); it never attempts a
self-grant.

Usage:
    python3 tools/detect-env.py                 # full probe (network included)
    python3 tools/detect-env.py --no-egress     # skip network probes
    python3 tools/detect-env.py --json          # machine-readable profile only

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SIBLINGS = ("grc_library_ref", "grc_library_scratch")

# Representative egress probes, one per source family the project's work waits
# on. Reachability of the FAMILY is what the profile reports; a probe is a HEAD
# request with a short timeout, and a 403 is reported as reachable-but-blocked
# (the iso.org shape), distinct from unreachable.
EGRESS_PROBES = (
    ("github-api", "https://api.github.com/zen"),
    ("eur-lex", "https://eur-lex.europa.eu/homepage.html"),
    ("nist-csrc", "https://csrc.nist.gov/"),
    ("iso-org", "https://www.iso.org/home.html"),
    ("planalto-br", "https://www.planalto.gov.br/"),
)


def run(cmd: list[str], timeout: int = 10) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except FileNotFoundError:
        return 127, "not found"
    except subprocess.TimeoutExpired:
        return 124, "timeout"


def probe_gh() -> dict:
    out: dict = {"present": shutil.which("gh") is not None}
    if not out["present"]:
        return out
    rc, _ = run(["gh", "auth", "status"], timeout=15)
    out["authenticated"] = rc == 0
    rc, body = run(["gh", "api", "rate_limit", "--jq",
                    "{graphql: .resources.graphql.remaining, core: .resources.core.remaining}"],
                   timeout=15)
    if rc == 0:
        try:
            out["rate_remaining"] = json.loads(body)
        except json.JSONDecodeError:
            out["rate_remaining"] = "unparsed"
    return out


def probe_hooks() -> dict:
    settings = REPO_ROOT / ".claude" / "settings.json"
    hook_script = REPO_ROOT / ".claude" / "hooks" / "block-verification-pipes.py"
    project_dir_set = bool(os.environ.get("CLAUDE_PROJECT_DIR"))
    configured = False
    if settings.is_file():
        configured = "block-verification-pipes" in settings.read_text(
            encoding="utf-8", errors="replace")
    return {
        "pipe_guard_configured": configured,
        "hook_script_present": hook_script.is_file(),
        "CLAUDE_PROJECT_DIR_set": project_dir_set,
        # The hook command resolves the guard script through $CLAUDE_PROJECT_DIR.
        # When that var is unset IN THIS PROCESS the cloud harness fails to resolve
        # it and the hook silently does not fire (the #677 root cause); but the
        # NUC harness has been OBSERVED to fire the hook anyway (it resolves the path
        # for hook execution even when the var is absent from the Bash-tool env). So
        # actual firing is NOT reliably script-predictable across environments; it is
        # an ASSISTANT-PROBE (observe whether a piped verification command is
        # blocked), and the unpiped-verification habit (RM-10) is the control either
        # way. This field reports only the observable in-process input, not a firing
        # prediction.
        "child_session": bool(os.environ.get("CLAUDE_CODE_CHILD_SESSION")),
    }


def probe_siblings() -> dict:
    out = {}
    for name in SIBLINGS:
        path = REPO_ROOT.parent / name
        entry: dict = {"readable": path.is_dir()}
        if entry["readable"]:
            rc, _ = run(["git", "-C", str(path), "rev-parse", "HEAD"])
            entry["git_ok"] = rc == 0
        else:
            entry["fix"] = (f"launch with --add-dir {path} or add it to "
                            f"additionalDirectories in .claude/settings.local.json "
                            f"(machine-local, git-ignored); binds at launch, "
                            f"cannot be granted mid-session")
        out[name] = entry
    return out


def probe_one(url: str, method: str) -> dict:
    req = urllib.request.Request(url, method=method,
                                 headers={"User-Agent": "grc-detect-env/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            resp.read(64)
            return {"status": resp.status, "class": "reachable"}
    except urllib.error.HTTPError as exc:
        return {"status": exc.code,
                "class": "reachable-but-blocked" if exc.code in (403, 405, 429)
                else "reachable-error"}
    except Exception as exc:  # URLError, timeout, TLS: unreachable classes
        return {"status": None, "class": f"unreachable ({type(exc).__name__})"}


def probe_egress() -> dict:
    out = {}
    for name, url in EGRESS_PROBES:
        result = probe_one(url, "HEAD")
        # Some hosts drop or reject HEAD; a GET retry distinguishes
        # "HEAD-intolerant but reachable" from genuinely unreachable.
        if result["class"].startswith("unreachable") or result["status"] in (400, 405):
            result = probe_one(url, "GET")
        out[name] = result
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-egress", action="store_true")
    ap.add_argument("--json", action="store_true",
                    help="Print the machine-readable profile only.")
    args = ap.parse_args(argv)

    try:
        profile: dict = {
            "repo_root": str(REPO_ROOT),
            "platform": sys.platform,
            "gh": probe_gh(),
            "hooks": probe_hooks(),
            "siblings": probe_siblings(),
        }
        if not args.no_egress:
            profile["egress"] = probe_egress()

        gh = profile["gh"]
        graphql_left = (gh.get("rate_remaining") or {}).get("graphql") \
            if isinstance(gh.get("rate_remaining"), dict) else None
        decisions = {
            "pr_mechanism": ("ASSISTANT-PROBE: use GitHub MCP if mcp__github__* "
                             "tools are in your tool list; else gh CLI"
                             if gh.get("authenticated")
                             else "ASSISTANT-PROBE: GitHub MCP if present; gh CLI "
                                  "is NOT authenticated here"),
            "ci_merge_transport": ("gh GraphQL ok" if isinstance(graphql_left, int)
                                   and graphql_left > 100 else
                                   ("REST fallback advised: GraphQL remaining "
                                    f"{graphql_left}" if isinstance(graphql_left, int)
                                    else "unknown (no gh rate data); prefer MCP or "
                                         "REST endpoints")),
            "commit_push_mode": ("ASSISTANT-PROBE: cloud stop-hook auto-commit-push "
                                 "cannot be script-detected; if this is a managed "
                                 "cloud session assume present, on a local machine "
                                 "commit and push manually"),
            "pipe_guard": ("ASSISTANT-PROBE: whether the pipe-guard hook fires is not "
                           "reliably script-detectable (an unset CLAUDE_PROJECT_DIR "
                           "blocks it on the cloud harness but NOT the NUC harness, "
                           "which resolves the hook path anyway); observe whether a "
                           "piped verification command is actually blocked. Rely on "
                           "the unpiped-verification habit (RM-10) either way"),
        }
        profile["decisions"] = decisions
    except Exception as exc:  # never crash the resume step
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(profile, indent=2))
        return 0

    print("# Environment profile (detect-env)\n")
    print(f"- Repo root: {profile['repo_root']} ({profile['platform']})")
    g = profile["gh"]
    print(f"- gh CLI: present={g.get('present')} authenticated="
          f"{g.get('authenticated', 'n/a')} rate={g.get('rate_remaining', 'n/a')}")
    h = profile["hooks"]
    print(f"- Hooks: pipe-guard configured={h['pipe_guard_configured']}, "
          f"CLAUDE_PROJECT_DIR set={h['CLAUDE_PROJECT_DIR_set']}, child session="
          f"{h['child_session']} (actual firing is an ASSISTANT-PROBE; unset "
          f"CLAUDE_PROJECT_DIR blocks the hook on the cloud harness but not the NUC "
          f"harness, so observe a piped verification, RM-10 unpiped habit is the "
          f"control either way)")
    for name, entry in profile["siblings"].items():
        line = f"- Sibling {name}: readable={entry['readable']}"
        if entry.get("git_ok") is not None:
            line += f", git={entry['git_ok']}"
        print(line)
        if "fix" in entry:
            print(f"  FIX: {entry['fix']}")
    for name, e in (profile.get("egress") or {}).items():
        print(f"- Egress {name}: {e['class']} (HTTP {e['status']})")
    print("\n## Decisions for the resume step\n")
    for key, val in profile["decisions"].items():
        print(f"- {key}: {val}")
    print("\nASSISTANT-PROBE lines are the assistant's to fill from its own tool "
          "list and session type; this script reports only what it can observe.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
