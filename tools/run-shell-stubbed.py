#!/usr/bin/env python3
"""Run a shell command string with gh and git replaced by recording stand-ins (P-TODO 3b116).

Hook and guard verification sometimes has to confirm how a real shell treats a command string (does bash
join this continuation, does `sh -c` run this). Doing that with a shell-FUNCTION stub is unsafe: a nested
`sh -c` does not inherit bash functions, and on 2026-09-27 such a check ran the real `gh pr merge 1`
against the live repository (no effect, the PR was long merged). This tool stubs at the EXECUTABLE level
and removes the credentials a real client would need, in layers:

  1. Stand-in executables for gh and git (and any --stub NAME) come first on PATH; each records its
     argv to a log and exits 0. A nested sh, bash, env or xargs resolves them through PATH.
  2. Credentials are out of reach: HOME, GH_CONFIG_DIR and XDG_CONFIG_HOME point into an empty temp dir;
     GH_TOKEN, GITHUB_TOKEN, GH_ENTERPRISE_TOKEN, GITHUB_ENTERPRISE_TOKEN and SSH_AUTH_SOCK are removed;
     git's global and system config are /dev/null and it never prompts.
  3. A command naming a stubbed tool by path (/usr/bin/gh, ./git) is REFUSED (exit 2), since a path
     skips PATH lookup.

RESIDUE, stated: this is not a sandbox. A command that deliberately re-points HOME or GH_CONFIG_DIR at the
real config, builds a tool's path at run time, or uses another network client is not contained; there is
no network isolation (user namespaces are not permitted on this host). It is for honest verification of
shell semantics, run on command strings the caller wrote.

Usage:
    python3 tools/run-shell-stubbed.py [--shell bash|sh|both] [--stub NAME ...] -- 'COMMAND'
    python3 tools/run-shell-stubbed.py --self-test

Output: per shell, the exit code, stdout, stderr and each stubbed call as `STUB <name> <argv...>`.
Exit codes: 0 ran; 2 refused or usage error.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

DEFAULT_STUBS = ("gh", "git")
TOKEN_VARS = ("GH_TOKEN", "GITHUB_TOKEN", "GH_ENTERPRISE_TOKEN", "GITHUB_ENTERPRISE_TOKEN", "SSH_AUTH_SOCK",
              "GIT_ASKPASS", "SSH_ASKPASS", "GH_HOST")
SHIM = """#!/bin/sh
printf 'STUB %s' '{name}' >> "{log}"
for a in "$@"; do printf ' %s' "$a" >> "{log}"; done
printf '\\n' >> "{log}"
exit 0
"""


def path_invocation(command: str, stubs) -> str | None:
    """The first stubbed name the command reaches by a path (which skips PATH), else None."""
    for name in stubs:
        if re.search(r"(?:^|[\s;&|()`'\"=])[^\s;&|()`'\"=]*/" + re.escape(name) + r"(?=$|[\s;&|()`'\"])", command):
            return name
    return None


def run(command: str, shells=("bash", "sh"), stubs=DEFAULT_STUBS, timeout: int = 30) -> list[dict]:
    """Run command under each shell with stand-ins; returns one result dict per shell."""
    results = []
    for shell in shells:
        with tempfile.TemporaryDirectory(prefix="stubbed-shell-") as tmp:
            bindir, home, log = os.path.join(tmp, "bin"), os.path.join(tmp, "home"), os.path.join(tmp, "calls.log")
            os.makedirs(bindir)
            os.makedirs(os.path.join(home, ".config"))
            open(log, "w").close()
            for name in stubs:
                shim = os.path.join(bindir, name)
                with open(shim, "w", encoding="utf-8") as fh:
                    fh.write(SHIM.format(name=name, log=log))
                os.chmod(shim, 0o755)
            env = {k: v for k, v in os.environ.items() if k not in TOKEN_VARS}
            env.update(PATH=bindir + os.pathsep + os.environ.get("PATH", "/usr/bin:/bin"), HOME=home,
                       GH_CONFIG_DIR=os.path.join(home, ".config", "gh"), XDG_CONFIG_HOME=os.path.join(home, ".config"),
                       GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0",
                       GH_PROMPT_DISABLED="1", GH_NO_UPDATE_NOTIFIER="1")
            exe = shutil.which(shell, path="/usr/bin:/bin") or shell
            try:
                p = subprocess.run([exe, "-c", command], capture_output=True, text=True, env=env, cwd=tmp,
                                   timeout=timeout)
                rc, out, err = p.returncode, p.stdout, p.stderr
            except subprocess.TimeoutExpired:
                rc, out, err = None, "", f"timed out after {timeout}s"
            with open(log, encoding="utf-8") as fh:
                calls = [line.rstrip("\n") for line in fh if line.strip()]
            results.append({"shell": shell, "rc": rc, "stdout": out, "stderr": err, "calls": calls})
    return results


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    ap.add_argument("--shell", choices=("bash", "sh", "both"), default="both")
    ap.add_argument("--stub", action="append", default=[], help="an extra executable name to stub")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("command", nargs="?")
    args = ap.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.command:
        ap.error("a command string is required")
    stubs = tuple(dict.fromkeys(DEFAULT_STUBS + tuple(args.stub)))
    hit = path_invocation(args.command, stubs)
    if hit:
        print(f"REFUSE: the command reaches {hit} by a path, which skips the stand-in on PATH.", file=sys.stderr)
        return 2
    shells = ("bash", "sh") if args.shell == "both" else (args.shell,)
    for r in run(args.command, shells, stubs):
        print(f"== {r['shell']} rc={r['rc']}")
        for c in r["calls"]:
            print(c)
        if r["stdout"]:
            print("-- stdout\n" + r["stdout"].rstrip("\n"))
        if r["stderr"]:
            print("-- stderr\n" + r["stderr"].rstrip("\n"))
    return 0


def _self_test() -> int:
    checks = []
    both = run("gh pr 'merge' 1; sh -c 'gh \"pr\" merge 2'; bash -c \"git push\"")
    for r in both:
        checks.append((f"{r['shell']}-nested-shells-hit-stubs",
                       r["calls"] == ["STUB gh pr merge 1", "STUB gh pr merge 2", "STUB git push"]))
    r = run("printf '%s|%s|%s' \"${GH_TOKEN:-none}\" \"$HOME\" \"$GH_CONFIG_DIR\"", shells=("sh",))[0]
    tok, home, cfg = (r["stdout"].split("|") + ["", "", ""])[:3]
    checks.append(("token-removed", tok == "none"))
    checks.append(("home-is-temp", "stubbed-shell-" in home and cfg.startswith(home)))
    r = run("env gh pr merge 3; command gh pr create", shells=("bash",))[0]
    checks.append(("env-and-command-hit-stubs", r["calls"] == ["STUB gh pr merge 3", "STUB gh pr create"]))
    r = run("x\\\\\ngh pr 'me'\\\nrge 1", shells=("bash",))[0]
    checks.append(("bash-continuation-semantics", r["calls"] == ["STUB gh pr merge 1"]))
    for cmd in ("/usr/bin/gh pr merge 1", "./gh pr merge", "sh -c '/usr/bin/git push'", "x=1 /bin/git push"):
        checks.append((f"refuse-path:{cmd}", path_invocation(cmd, DEFAULT_STUBS) is not None))
    for cmd in ("gh pr view 1", "echo github/ghost", "git -C /opt/x status", "python3 tools/gh-thing.py"):
        checks.append((f"allow:{cmd}", path_invocation(cmd, DEFAULT_STUBS) is None))
    checks.append(("main-refuses-path", main(["--shell", "sh", "/usr/bin/gh pr merge 1"]) == 2))
    failed = [n for n, ok in checks if not ok]
    print(f"run-shell-stubbed self-test: {'OK' if not failed else 'FAIL ' + str(failed)} ({len(checks)} checks)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
