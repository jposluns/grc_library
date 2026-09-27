#!/usr/bin/env python3
"""Run a shell command string with gh and git replaced by recording stand-ins (P-TODO 3b116).

Hook and guard verification sometimes has to confirm how a real shell treats a command string (does bash
join this continuation, does `sh -c` run this). Doing that with a shell-FUNCTION stub is unsafe: a nested
`sh -c` does not inherit bash functions, and on 2026-09-27 such a check ran the real `gh pr merge 1`
against the live repository (no effect, the PR was long merged). This tool works in layers:

  1. Stand-ins. Executables named gh and git (and any --stub NAME) come first on PATH; each records its
     arguments and exits 0. Nested sh, bash, env and xargs reach them through PATH.
  2. An inert environment for a real binary reached anyway (a path such as /usr/bin/gh, a PATH reset):
     GH_TOKEN is an invalid placeholder and GH_HOST a reserved .invalid host, so a real gh has no working
     credential; git's global and system config are off, and GIT_CONFIG_* rewrite every https, ssh and
     git@ remote URL to a .invalid host, so a real git cannot reach a remote; HOME and the gh and XDG config
     dirs are an empty temp dir. Inherited GH_*, GIT_*, token, askpass, SSH agent, BASH_FUNC_* (exported
     bash functions), BASH_ENV and ENV variables are removed.
  3. Refusal of a command that would undo layer 2: `env -i` / `--ignore-environment` / `env -u`, `unset`,
     `exec -c`, `setsid`, or an assignment to PATH, HOME, GH_*, GIT_* or XDG_* (exit 2).
  4. Containment in time: the command runs in its own process group, and the whole group is killed before
     the temp dir is removed, so a background child cannot outlive the stand-ins.

RESIDUE, stated: this is not a sandbox and there is no network isolation (user namespaces are not permitted
on this host). A real binary reached despite layer 1 still runs, in the inert environment; a command that
builds its environment changes at run time (eval of a variable, a script file it writes) can evade layer
3; another network client (curl) is not stubbed. It is for honest verification of shell semantics on
command strings the caller wrote.

Usage:
    python3 tools/run-shell-stubbed.py [--shell bash|sh|both] [--stub NAME ...] 'COMMAND'
    python3 tools/run-shell-stubbed.py --self-test

Output: per shell, the exit code, stdout, stderr and each stubbed call as `STUB <name> <argv...>`.
Exit codes: 0 ran; 2 refused or usage error.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time

DEFAULT_STUBS = ("gh", "git")
INVALID_HOST = "stubbed-shell.invalid"
_STRIP_PREFIXES = ("GH_", "GIT_", "GITHUB_", "BASH_FUNC_")
_STRIP_NAMES = ("SSH_AUTH_SOCK", "SSH_ASKPASS", "BASH_ENV", "ENV", "CDPATH")
_US, _RS = "\x1f", "\x1e"  # unit and record separators keep argument boundaries in the call log
SHIM = """#!/bin/sh
{{ printf '%s' '{name}'; for a in "$@"; do printf '\\037%s' "$a"; done; printf '\\036'; }} >> "{log}"
exit 0
"""
_UNDO = re.compile(r"(?:^|[\s;&|(`])(?:env\s+(?:-\w*[iu]|--ignore-environment|--unset)|unset\s|exec\s+-\w*c|setsid\b"
                   r"|(?:export\s+|declare\s+-\w*x\s+|readonly\s+)?(?:PATH|HOME|GH_\w*|GIT_\w*|XDG_\w*)\+?=)")


def undoes_environment(command: str) -> str | None:
    """The first construct in command that would strip or override the inert environment, else None."""
    m = _UNDO.search(command)
    return m.group(0).strip(" ;&|(`") if m else None


def _environment(bindir: str, home: str) -> dict:
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(_STRIP_PREFIXES) and k not in _STRIP_NAMES and "TOKEN" not in k}
    rewrites = [f"https://{INVALID_HOST}/", "https://", "ssh://", "git@", "git://", "http://"]
    env.update(PATH=bindir + os.pathsep + os.environ.get("PATH", "/usr/bin:/bin"), HOME=home,
               GH_CONFIG_DIR=os.path.join(home, ".config", "gh"), XDG_CONFIG_HOME=os.path.join(home, ".config"),
               GH_TOKEN="stubbed-shell-invalid", GH_HOST=INVALID_HOST, GH_PROMPT_DISABLED="1",
               GH_NO_UPDATE_NOTIFIER="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
               GIT_TERMINAL_PROMPT="0", GIT_CONFIG_COUNT=str(len(rewrites) - 1))
    for i, prefix in enumerate(rewrites[1:]):
        env[f"GIT_CONFIG_KEY_{i}"] = f"url.{rewrites[0]}.insteadOf"
        env[f"GIT_CONFIG_VALUE_{i}"] = prefix
    return env


def _rmtree(path: str) -> None:
    """Remove the temp dir even after the command made parts of it unreadable."""
    try:
        shutil.rmtree(path)
        return
    except OSError:
        pass
    for root, dirs, _files in os.walk(path, topdown=True, onerror=None):
        for d in dirs:
            os.chmod(os.path.join(root, d), stat.S_IRWXU)
    os.chmod(path, stat.S_IRWXU)
    for root, dirs, _files in os.walk(path):
        for d in dirs:
            os.chmod(os.path.join(root, d), stat.S_IRWXU)
    shutil.rmtree(path)


def run(command: str, shells=("bash", "sh"), stubs=DEFAULT_STUBS, timeout: int = 30) -> list[dict]:
    """Run command under each shell with stand-ins; one result dict per shell. Raises ValueError when the
    command would undo the inert environment (layer 3)."""
    undo = undoes_environment(command)
    if undo:
        raise ValueError(f"the command would strip or override the inert environment: {undo!r}")
    results = []
    for shell in shells:
        tmp = tempfile.mkdtemp(prefix="stubbed-shell-")
        try:
            bindir, home, log = os.path.join(tmp, "bin"), os.path.join(tmp, "home"), os.path.join(tmp, "calls.log")
            os.makedirs(bindir)
            os.makedirs(os.path.join(home, ".config"))
            open(log, "w").close()
            for name in stubs:
                shim = os.path.join(bindir, name)
                with open(shim, "w", encoding="utf-8") as fh:
                    fh.write(SHIM.format(name=name, log=log))
                os.chmod(shim, 0o755)
            exe = shutil.which(shell, path="/usr/bin:/bin") or shell
            # Output goes to files, not pipes: a background child holding a pipe would keep the wait open until
            # it had run, so it could not be stopped (3b116 QA r1).
            out_path, err_path = os.path.join(tmp, "stdout"), os.path.join(tmp, "stderr")
            with open(out_path, "w") as o_fh, open(err_path, "w") as e_fh:
                p = subprocess.Popen([exe, "-c", command], stdout=o_fh, stderr=e_fh, stdin=subprocess.DEVNULL,
                                     env=_environment(bindir, home), cwd=tmp, start_new_session=True)
                try:
                    rc = p.wait(timeout=timeout)
                    timed_out = ""
                except subprocess.TimeoutExpired:
                    rc, timed_out = None, f"timed out after {timeout}s"
                finally:
                    try:
                        os.killpg(p.pid, signal.SIGKILL)  # layer 4: nothing in the group outlives the stand-ins
                    except ProcessLookupError:
                        pass
                    p.wait()
            with open(out_path, encoding="utf-8", errors="replace") as fh:
                out = fh.read()
            with open(err_path, encoding="utf-8", errors="replace") as fh:
                err = fh.read() + timed_out
            with open(log, encoding="utf-8") as fh:
                records = [r for r in fh.read().split(_RS) if r]
            calls = ["STUB " + " ".join(r.split(_US)) for r in records]
            results.append({"shell": shell, "rc": rc, "stdout": out, "stderr": err, "calls": calls,
                            "argv": [r.split(_US) for r in records]})
        finally:
            _rmtree(tmp)
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
    shells = ("bash", "sh") if args.shell == "both" else (args.shell,)
    try:
        results = run(args.command, shells, stubs)
    except ValueError as exc:
        print(f"REFUSE: {exc}", file=sys.stderr)
        return 2
    for r in results:
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
    before = {d for d in os.listdir(tempfile.gettempdir()) if d.startswith("stubbed-shell-")}
    for r in run("gh pr 'merge' 1; sh -c 'gh \"pr\" merge 2'; bash -c \"git push\"; env gh pr create; "
                 "echo x | xargs gh pr merge"):
        checks.append((f"{r['shell']}-nested-shells-hit-stubs",
                       r["calls"] == ["STUB gh pr merge 1", "STUB gh pr merge 2", "STUB git push",
                                      "STUB gh pr create", "STUB gh pr merge x"]))
    r = run("gh pr merge 'a b' ''", shells=("sh",))[0]
    checks.append(("argument-boundaries-kept", r["argv"] == [["gh", "pr", "merge", "a b", ""]]))
    probe = "printf '%s|' \"$GH_TOKEN\" \"$GH_HOST\" \"$HOME\" \"$GH_CONFIG_DIR\" \"${BASH_ENV:-unset}\" \"${GIT_ASKPASS:-unset}\""
    saved = {k: os.environ.get(k) for k in ("BASH_ENV", "GIT_ASKPASS", "BASH_FUNC_gh%%")}
    os.environ.update({"BASH_ENV": "/nonexistent", "GIT_ASKPASS": "/bin/true", "BASH_FUNC_gh%%": "() { echo FUNC; }"})
    try:
        r = run(probe, shells=("sh",))[0]
        tok, host, home, cfg, benv, askpass = (r["stdout"].split("|") + [""] * 6)[:6]
        checks.append(("token-is-placeholder", tok == "stubbed-shell-invalid"))
        checks.append(("host-is-invalid", host == INVALID_HOST))
        checks.append(("home-is-temp", "stubbed-shell-" in home and cfg.startswith(home)))
        checks.append(("inherited-shell-and-git-vars-removed", benv == "unset" and askpass == "unset"))
        r = run("gh pr merge 4", shells=("bash",))[0]
        checks.append(("exported-bash-function-removed", r["calls"] == ["STUB gh pr merge 4"]))
    finally:
        for k, v in saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
    git = shutil.which("git", path="/usr/bin:/bin")
    if git:  # local only: the remote URL a reached real git would use, in a throwaway repository
        r = run(f"'{git}' init -q r && '{git}' -C r remote add o https://github.com/x/y && "
                f"'{git}' -C r remote add s git@github.com:x/y && '{git}' -C r remote get-url o && "
                f"'{git}' -C r remote get-url s", shells=("sh",))[0]
        urls = r["stdout"].split()
        checks.append(("real-git-remote-rewritten", len(urls) == 2 and all(INVALID_HOST in u for u in urls)))
    # A background child must not outlive the run: after the stand-ins are gone it would reach the real gh.
    marker_dir = tempfile.mkdtemp(prefix="stubbed-shell-test-")
    marker = os.path.join(marker_dir, "alive")
    try:
        run(f"(sleep 1; echo alive > '{marker}') & echo started", shells=("bash",), timeout=10)
        time.sleep(2)
        checks.append(("background-child-killed", not os.path.exists(marker)))
    finally:
        shutil.rmtree(marker_dir, ignore_errors=True)
    r = run("mkdir -p d/e && touch d/e/f && chmod 000 d/e d", shells=("sh",))[0]
    checks.append(("read-only-tree-cleaned", r["rc"] == 0))
    for cmd in ("env -i gh pr merge 1", "env --ignore-environment gh", "env -u GH_TOKEN gh", "unset HOME; gh",
                "PATH=/usr/bin gh pr merge", "HOME=/root git push", "export GH_TOKEN=x", "GIT_CONFIG_GLOBAL=~/.g git",
                "exec -c gh", "setsid gh pr merge &", "XDG_CONFIG_HOME=/x gh"):
        checks.append((f"refuse:{cmd}", undoes_environment(cmd) is not None))
    for cmd in ("gh pr view 1", "git clone https://github.com/org/gh", "printf '%s' /usr/bin/gh",
                "git diff -- tools/gh", "echo PATH is set", "grep -n HOME file"):
        checks.append((f"allow:{cmd}", undoes_environment(cmd) is None))
    checks.append(("main-refuses", main(["--shell", "sh", "env -i gh pr merge 1"]) == 2))
    left = [d for d in os.listdir(tempfile.gettempdir()) if d.startswith("stubbed-shell-") and d not in before]
    checks.append(("temp-dirs-removed", not left))
    failed = [n for n, ok in checks if not ok]
    print(f"run-shell-stubbed self-test: {'OK' if not failed else 'FAIL ' + str(failed)} ({len(checks)} checks)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
