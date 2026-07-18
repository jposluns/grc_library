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
reachability per source family, sibling-repo access, and the operator identity
(maintainer vs adopter fork, by the ``origin`` remote, TODO section 1.19.5). This
tool probes what a SCRIPT can observe and prints one profile block the resume step
consumes; the
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
SIBLINGS = ("grc_library_ref", "grc_library_scratch", "grc_library_private")

# The canonical maintainer origin (owner/repo). A clone whose ``origin`` remote
# points here is the maintainer's own repo; any other owner is an adopter fork.
# Used by the origin-identity probe (TODO section 1.19.5).
MAINTAINER_ORIGIN_OWNER_REPO = "jposluns/grc_library"

# The committed adopt-config marker (TODO section 3.92a). The /adopt run-once
# onboarding writes it; the /resume adopter-path reads it to skip re-onboarding.
# Its minimal schema (per the adopt SKILL step 6): mode == "adopter",
# adopted_at (UTC date), sibling_choice in the set below, adopt_config_version.
ADOPT_CONFIG = REPO_ROOT / ".claude" / "adopt-config.json"
VALID_SIBLING_CHOICES = ("own-siblings", "self-contained")

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


def _origin_url() -> str | None:
    rc, out = run(["git", "-C", str(REPO_ROOT), "remote", "get-url", "origin"])
    out = out.strip()
    return out if rc == 0 and out else None


def _origin_is_maintainer(url: str | None) -> bool:
    """True if ``url`` points at the canonical maintainer owner/repo on GitHub.

    Parses the origin to a host plus an exactly-two-segment ``owner/repo`` path
    and requires host ``github.com`` and ``owner/repo`` ==
    ``MAINTAINER_ORIGIN_OWNER_REPO``. Handles HTTPS
    (``https://github.com/owner/repo[.git]``), the scp-like SSH form (the ``git@``
    prefix, host ``github.com``, path ``owner/repo``, optional ``.git``), and
    ``ssh://`` URLs, case-insensitively, tolerating a trailing ``.git`` / slash. A non-GitHub host
    (including an SSH host alias), a fork under a different owner, a different
    repo, or a malformed multi-segment path does NOT match. The host-pin closes
    the theoretical false-maintainer classifications noted in TODO section 1.19.5;
    since section 1.19.6 makes the classification load-bearing (it drives the
    ``/resume`` maintainer-vs-adopter path), a false MAINTAINER is the dangerous
    direction and is foreclosed, while a maintainer using an unusual SSH host
    alias degrades to the recoverable false-ADOPTER (``/resume`` proposes
    ``/adopt``, which they decline).
    """
    if not url:
        return False
    u = url.strip()
    if u.endswith("/"):
        u = u[:-1]
    if u.lower().endswith(".git"):
        u = u[:-4]

    host: str | None = None
    path: str | None = None
    low = u.lower()
    if low.startswith(("https://", "http://", "ssh://")):
        rest = u.split("://", 1)[1]
        if "/" not in rest:
            return False
        hostpart, path = rest.split("/", 1)
        hostpart = hostpart.split("@")[-1]   # strip any user@
        host = hostpart.split(":")[0]        # strip any :port
    elif "@" in u and ":" in u.split("@", 1)[1]:
        # scp-like SSH: [user@]host:owner/repo
        after_at = u.split("@", 1)[1]
        host, path = after_at.split(":", 1)
    else:
        return False

    if not host or path is None or host.lower() != "github.com":
        return False
    segments = [s for s in path.split("/") if s]
    if len(segments) != 2:
        return False
    return "/".join(segments).lower() == MAINTAINER_ORIGIN_OWNER_REPO.lower()


def _adopt_config_status() -> tuple[bool, "bool | None"]:
    """Return (present, valid) for ``.claude/adopt-config.json`` (TODO 3.92a).

    ``valid`` is ``None`` when the file is absent. When present, ``valid`` is
    True only for parseable JSON with ``mode == "adopter"`` AND a recognized
    ``sibling_choice`` (the schema the adopt SKILL step 6 writes); an unparseable
    file, a non-object, a wrong/absent ``mode``, or an out-of-set ``sibling_choice``
    is present-but-invalid. This is the mechanical backstop for the /resume
    adopter-path's malformed-config handling (previously assistant-prose only).
    """
    if not ADOPT_CONFIG.exists():
        return (False, None)
    try:
        data = json.loads(ADOPT_CONFIG.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, ValueError):
        return (True, False)
    if not isinstance(data, dict):
        return (True, False)
    valid = (
        data.get("mode") == "adopter"
        and data.get("sibling_choice") in VALID_SIBLING_CHOICES
    )
    return (True, bool(valid))


def probe_identity(siblings: dict) -> dict:
    """Classify the operator by ORIGIN IDENTITY (TODO section 1.19.5).

    - ``maintainer``: origin is the canonical maintainer repo AND at least one
      private sibling is readable (corroboration).
    - ``maintainer-fresh-machine``: origin is the maintainer repo but NO sibling
      is readable (a fresh maintainer clone; the siblings should be cloned, this
      is NOT an adopter).
    - ``adopter``: origin is a fork (any other owner) or absent.

    Detection only: the ``/resume`` maintainer-vs-adopter path acts on this and,
    on an un-onboarded adopter clone, proposes the ``/adopt`` run-once onboarding
    skill (built in the same section-1.19.6 change as this probe's load-bearing
    use).
    """
    url = _origin_url()
    is_maint_origin = _origin_is_maintainer(url)
    any_sibling = any(bool(e.get("readable")) for e in siblings.values())
    if is_maint_origin:
        classification = "maintainer" if any_sibling else "maintainer-fresh-machine"
    else:
        classification = "adopter"
    adopt_present, adopt_valid = _adopt_config_status()
    return {
        "origin_url": url,
        "origin_is_maintainer_repo": is_maint_origin,
        "any_sibling_readable": any_sibling,
        "classification": classification,
        "adopt_config_present": adopt_present,
        "adopt_config_valid": adopt_valid,
    }


def ref_availability_decision(classification: str, ref_readable: bool) -> str:
    """The _ref-required loud gate (TODO section 1.19.7).

    Reference-checking is critical to the orchestrator's content work, so a
    missing grc_library_ref is a LOUD failure for the maintainer, never a silent
    graceful degradation. Graceful degradation of the sibling-reaching tools
    (lint_common.resolve_sibling) is ADOPTER-ONLY.
    """
    if ref_readable:
        return "ok (grc_library_ref readable)."
    if classification == "maintainer":
        return (
            "HALT (LOUD): identity is maintainer but grc_library_ref is NOT "
            "readable. _ref is a REQUIRED orchestrator dependency (reference-"
            "checking is critical to content work); do NOT proceed on reference-"
            "dependent work. Grant sibling access (the FIX line above), then "
            "re-resume. The sibling-reaching tools' graceful degradation is "
            "ADOPTER-ONLY, never the maintainer.")
    if classification == "maintainer-fresh-machine":
        return (
            "clone _ref FIRST: a fresh maintainer clone has no grc_library_ref; "
            "content work requires it, so clone the private siblings before any "
            "reference-dependent work (tooling-only work may proceed only if the "
            "maintainer directs).")
    if classification == "adopter":
        return (
            "ok (adopter, _ref absent as expected): the sibling-reaching tools "
            "degrade gracefully; the committed reference-acquisition manifest + "
            "/adopt .ref bootstrap cover reference acquisition.")
    # Unknown / undetermined identity: fail SAFE (loud), never silently graceful-
    # degrade (the gate's whole point). Unreachable for the closed probe_identity
    # set today, but keeps the helper correct-by-construction if that set changes.
    return (
        f"HALT (LOUD): undetermined operator identity ({classification!r}) with "
        "grc_library_ref unreadable; treat _ref as REQUIRED and do NOT silently "
        "degrade. Resolve the identity and sibling access, then re-resume.")


def private_availability_decision(classification: str, private_readable: bool) -> str:
    """The _private-required loud gate (TODO section 1.19.8 layered assurance).

    grc_library_private holds the maintainer orchestrator's operational state, so
    for the maintainer a missing _private is a LOUD failure to fix (clone it),
    never a silent skip or a hallucinated-from-memory work-around. The graceful
    path is ADOPTER-ONLY: an adopter legitimately has no _private and is offered a
    choice (redirect to the in-repo .private placeholder, or create their own).
    Mirrors ref_availability_decision; the PreToolUse hook is the mechanical
    enforcement that this decision is not merely advisory.
    """
    if private_readable:
        return "ok (grc_library_private readable)."
    if classification == "maintainer":
        return (
            "HALT (LOUD): identity is maintainer but grc_library_private is NOT "
            "readable. _private is a REQUIRED orchestrator dependency (it holds "
            "the operational state the CLAUDE.md delegation directive points to); "
            "do NOT proceed on operational work and do NOT reconstruct its content "
            "from memory. Grant sibling access (the FIX line above) or clone it "
            "(git clone https://github.com/jposluns/grc_library_private.git "
            "../grc_library_private), then re-resume.")
    if classification == "maintainer-fresh-machine":
        return (
            "clone _private FIRST: a fresh maintainer clone has no "
            "grc_library_private; operational work requires it, so clone the "
            "private siblings (git clone "
            "https://github.com/jposluns/grc_library_private.git "
            "../grc_library_private) before proceeding.")
    if classification == "adopter":
        return (
            "ok (adopter, _private absent as expected): _private is the "
            "maintainer's private operational store; an adopter is offered a "
            "choice (point their own store at ../grc_library_private, use the "
            "in-repo .private placeholder, or create their own). Nothing here is "
            "required to use the corpus or run the public gates.")
    return (
        f"HALT (LOUD): undetermined operator identity ({classification!r}) with "
        "grc_library_private unreadable; treat _private as REQUIRED and do NOT "
        "silently degrade. Resolve the identity and sibling access, then re-resume.")


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


def _self_test() -> int:
    """Unit tests for the sibling-availability decision functions."""
    import unittest

    class T(unittest.TestCase):
        def test_private_readable_ok(self):
            self.assertTrue(private_availability_decision("maintainer", True).startswith("ok"))

        def test_private_maintainer_absent_halts(self):
            self.assertIn("HALT (LOUD)", private_availability_decision("maintainer", False))

        def test_private_fresh_machine_clones(self):
            self.assertIn("clone _private FIRST", private_availability_decision("maintainer-fresh-machine", False))

        def test_private_adopter_graceful(self):
            self.assertTrue(private_availability_decision("adopter", False).startswith("ok (adopter"))

        def test_private_unknown_fails_safe(self):
            self.assertIn("HALT (LOUD)", private_availability_decision("weird", False))

        def test_ref_parity(self):
            self.assertIn("HALT (LOUD)", ref_availability_decision("maintainer", False))
            self.assertTrue(ref_availability_decision("adopter", False).startswith("ok"))

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T)
    )
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-egress", action="store_true")
    ap.add_argument("--json", action="store_true",
                    help="Print the machine-readable profile only.")
    ap.add_argument("--self-test", action="store_true",
                    help="Run the availability-decision unit tests and exit.")
    args = ap.parse_args(argv)

    if args.self_test:
        return _self_test()

    try:
        profile: dict = {
            "repo_root": str(REPO_ROOT),
            "platform": sys.platform,
            "gh": probe_gh(),
            "hooks": probe_hooks(),
            "siblings": probe_siblings(),
        }
        profile["identity"] = probe_identity(profile["siblings"])
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
        idn = profile["identity"]
        decisions["operator_identity"] = (
            f"{idn['classification']} (origin "
            f"{'is' if idn['origin_is_maintainer_repo'] else 'is NOT'} "
            f"{MAINTAINER_ORIGIN_OWNER_REPO}; sibling(s) "
            f"{'present' if idn['any_sibling_readable'] else 'absent'}). "
            + {
                "maintainer": "proceed with the private siblings.",
                "maintainer-fresh-machine": (
                    "a fresh maintainer clone; clone the private siblings, then "
                    "proceed as maintainer (NOT adopter)."),
                "adopter": (
                    "an adopter fork; if no .claude/adopt-config.json exists, /resume "
                    "proposes the /adopt run-once onboarding skill (else proceed in "
                    "adopter-mode per the recorded config)."),
            }[idn["classification"]]
        )
        # _ref-required loud gate (TODO section 1.19.7): a missing grc_library_ref is a LOUD
        # failure for the maintainer, never a silent graceful degradation (that is adopter-only).
        ref_readable = bool(
            profile["siblings"].get("grc_library_ref", {}).get("readable"))
        decisions["ref_availability"] = ref_availability_decision(
            idn["classification"], ref_readable)
        # _private-required loud gate (TODO section 1.19.8 layered assurance): a missing
        # grc_library_private is a LOUD failure for the maintainer, never a silent skip.
        private_readable = bool(
            profile["siblings"].get("grc_library_private", {}).get("readable"))
        decisions["private_availability"] = private_availability_decision(
            idn["classification"], private_readable)
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
    idn = profile["identity"]
    print(f"- Operator identity: {idn['classification']} "
          f"(origin={idn['origin_url']}, maintainer-repo="
          f"{idn['origin_is_maintainer_repo']}, sibling(s) readable="
          f"{idn['any_sibling_readable']})")
    print(f"- Adopt-config: present={idn['adopt_config_present']}, "
          f"valid={idn['adopt_config_valid']} "
          f"(adopter-path: present+valid -> proceed adopter-mode; present+invalid "
          f"-> re-propose /adopt; absent on an adopter -> propose /adopt)")
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
