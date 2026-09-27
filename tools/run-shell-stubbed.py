#!/usr/bin/env python3
"""Run a shell command string with gh and git replaced by recording stand-ins (P-TODO 3b116).

Hook and guard verification sometimes has to confirm how a real shell treats a command string (does bash
join this continuation, does `sh -c` run this). Doing that with a shell-FUNCTION stub is unsafe: a nested
`sh -c` does not inherit bash functions, and on 2026-09-27 such a check ran the real `gh pr merge 1`
against the live repository (no effect, the PR was long merged). A first design here layered environment
tricks and name-matching refusals; review showed ordinary shell forms defeat each of those, so this version
leans on an enforcement mechanism bash itself provides:

  1. Restricted bash (`bash -r`) runs the command, with PATH set to a directory holding only the gh and git
     stand-ins (each records its arguments and exits 0), wrappers named bash and sh that start restricted
     bash again, and a whitelist of harmless utilities. Restricted mode forbids changing PATH, SHELL, ENV or
     BASH_ENV, command names containing a slash, `command -p`, `hash -p`, `exec`, `enable -f`, importing
     functions from the environment, turning restriction off, and output redirection. No env, xargs,
     find, interpreter or network client is on PATH, so nothing on PATH can run a program by path. A real
     gh or git is therefore unreachable, including from a nested shell or a background child.
  2. The environment is built from scratch, not inherited: PATH, a temporary HOME and gh/XDG config dirs,
     and, as a second layer, an invalid GH_TOKEN, a reserved .invalid GH_HOST and git config off.
  3. The command's process group is killed, and the temp dir removed, when the command ends.

LIMITS, stated: output redirection (`>`) is refused, as restricted mode requires, so a command string that
redirects cannot be verified here; `sh` is emulated by `bash --posix` (dash has no restricted mode), so a
dash-only difference is not observed; an argument containing the log's separator bytes (0x1e, 0x1f) is
ambiguous in the call log. This relies on bash's restricted mode being intact; it is not a kernel sandbox.

Usage:
    python3 tools/run-shell-stubbed.py [--shell bash|sh|both] [--stub NAME ...] 'COMMAND'
    python3 tools/run-shell-stubbed.py --self-test

Output: per shell, the exit code, stdout, stderr and each stubbed call as `STUB <name> <argv...>`.
Exit codes: 0 ran; 2 usage error.
"""
from __future__ import annotations

import argparse
import os
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time

DEFAULT_STUBS = ("gh", "git")
BASH = "/bin/bash"
# Harmless utilities: none can run another program, open a network connection, or change PATH.
WHITELIST = ("cat", "sleep", "true", "false", "head", "tail", "tr", "wc", "sort", "grep", "mkdir", "touch",
             "chmod", "ls", "basename", "dirname", "seq")
INVALID_HOST = "stubbed-shell.invalid"
_US, _RS = "\x1f", "\x1e"  # unit and record separators keep argument boundaries in the call log
SHIM = """#!{bash} -r
{{ printf '%s' '{name}'; for a in "$@"; do printf '\\037%s' "$a"; done; printf '\\036'; }} >> "{log}"
exit 0
"""
SHELL_WRAPPER = """#!/bin/sh
exec {bash} {posix}-r "$@"
"""


def _rmtree(path: str) -> None:
    """Remove the temp dir even after the command made parts of it unreadable."""
    try:
        shutil.rmtree(path)
        return
    except OSError:
        pass
    os.chmod(path, stat.S_IRWXU)
    for root, dirs, _files in os.walk(path):
        for d in dirs:
            os.chmod(os.path.join(root, d), stat.S_IRWXU)
    shutil.rmtree(path)


def _prepare(tmp: str, stubs) -> tuple[str, str, str]:
    bindir, home, log = os.path.join(tmp, "bin"), os.path.join(tmp, "home"), os.path.join(tmp, "calls.log")
    os.makedirs(bindir)
    os.makedirs(os.path.join(home, ".config"))
    open(log, "w").close()
    # The shim is run by an unrestricted bash (it is a script run via PATH); its only action is the append.
    for name in stubs:
        with open(os.path.join(bindir, name), "w", encoding="utf-8") as fh:
            fh.write(SHIM.format(bash=BASH, name=name, log=log).replace(" -r\n", "\n", 1))
    for name, posix in (("bash", ""), ("sh", "--posix ")):
        with open(os.path.join(bindir, name), "w", encoding="utf-8") as fh:
            fh.write(SHELL_WRAPPER.format(bash=BASH, posix=posix))
    for name in list(stubs) + ["bash", "sh"]:
        os.chmod(os.path.join(bindir, name), 0o755)
    for util in WHITELIST:
        real = shutil.which(util, path="/usr/bin:/bin")
        if real and not os.path.exists(os.path.join(bindir, util)):
            os.symlink(real, os.path.join(bindir, util))
    return bindir, home, log


def run(command: str, shells=("bash", "sh"), stubs=DEFAULT_STUBS, timeout: int = 30) -> list[dict]:
    """Run command under each shell (restricted bash; sh as restricted bash --posix); one result dict each."""
    results = []
    for shell in shells:
        tmp = tempfile.mkdtemp(prefix="stubbed-shell-")
        try:
            bindir, home, log = _prepare(tmp, stubs)
            env = {"PATH": bindir, "HOME": home, "LANG": "C.UTF-8", "GH_CONFIG_DIR": os.path.join(home, ".config", "gh"),
                   "XDG_CONFIG_HOME": os.path.join(home, ".config"), "GH_TOKEN": "stubbed-shell-invalid",
                   "GH_HOST": INVALID_HOST, "GH_PROMPT_DISABLED": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                   "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0"}
            argv = [BASH] + (["--posix"] if shell == "sh" else []) + ["-r", "-c", command]  # long options first
            out_path, err_path = os.path.join(tmp, "stdout"), os.path.join(tmp, "stderr")
            with open(out_path, "w") as o_fh, open(err_path, "w") as e_fh:
                p = subprocess.Popen(argv, stdout=o_fh, stderr=e_fh, stdin=subprocess.DEVNULL, env=env, cwd=tmp,
                                     start_new_session=True)
                timed_out = ""
                try:
                    rc = p.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    rc, timed_out = None, f"timed out after {timeout}s"
                finally:
                    try:
                        os.killpg(p.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    p.wait()
            with open(out_path, encoding="utf-8", errors="replace") as fh:
                out = fh.read()
            with open(err_path, encoding="utf-8", errors="replace") as fh:
                err = fh.read() + timed_out
            with open(log, encoding="utf-8") as fh:
                records = [r for r in fh.read().split(_RS) if r]
            results.append({"shell": shell, "rc": rc, "stdout": out, "stderr": err,
                            "calls": ["STUB " + " ".join(r.split(_US)) for r in records],
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
    before = {d for d in os.listdir(tempfile.gettempdir()) if d.startswith("stubbed-shell-")}
    for r in run("gh pr 'merge' 1; sh -c 'gh \"pr\" merge 2'; bash -c \"git push\"; bash -e -c 'gh pr create'"):
        checks.append((f"{r['shell']}-nested-shells-hit-stubs", r["calls"] ==
                       ["STUB gh pr merge 1", "STUB gh pr merge 2", "STUB git push", "STUB gh pr create"]))
    r = run("gh pr merge 'a b' ''", shells=("sh",))[0]
    checks.append(("argument-boundaries-kept", r["argv"] == [["gh", "pr", "merge", "a b", ""]]))
    # Every route to a real binary that ordinary shell syntax offers is refused by restricted bash.
    for label, cmd in (("slash-path", "/usr/bin/gh pr merge 1"), ("path-change", "PATH=/usr/bin; gh pr merge 1"),
                       ("path-prefix", "PATH=/usr/bin gh pr merge 1"), ("command-p", "command -p gh pr merge 1"),
                       ("exec", "exec /usr/bin/gh pr merge 1"), ("env", "env -i PATH=/usr/bin gh pr merge 1"),
                       ("hash-p", "hash -p /usr/bin/gh gh; gh pr merge 1"), ("nested-slash", "bash -c '/usr/bin/gh x'"),
                       ("set-plus-r", "set +r; /usr/bin/gh x"), ("bash-plus-r", "bash +r -c '/usr/bin/gh x'"),
                       ("xargs", "echo /usr/bin/gh | xargs"), ("job-control", "set -m; (/usr/bin/gh x) & wait")):
        rr = run(cmd, shells=("bash",))[0]
        # The evidence must be bash's own refusal, not merely the absence of a visible real run.
        refused = any(s in rr["stderr"] for s in ("restricted", "readonly variable", "command not found",
                                                   "invalid option"))
        checks.append((f"refused:{label}", refused and all(c.startswith("STUB ") for c in rr["calls"])))
    r = run("printf '%s|' \"$GH_TOKEN\" \"$GH_HOST\" \"$HOME\" \"$PATH\" \"${BASH_ENV:-unset}\"", shells=("sh",))[0]
    tok, host, home, path, benv = (r["stdout"].split("|") + [""] * 5)[:5]
    checks.append(("environment-built-from-scratch", tok == "stubbed-shell-invalid" and host == INVALID_HOST
                   and "stubbed-shell-" in home and path.endswith("/bin") and ":" not in path and benv == "unset"))
    # An inherited BASH_ENV would run before restriction applies; the environment is built from scratch.
    env_dir = tempfile.mkdtemp(prefix="stubbed-shell-test-")
    env_marker, env_file = os.path.join(env_dir, "ran"), os.path.join(env_dir, "env.sh")
    with open(env_file, "w", encoding="utf-8") as fh:
        fh.write(f"touch '{env_marker}'\n")
    saved_env = os.environ.get("BASH_ENV")
    os.environ["BASH_ENV"] = env_file
    try:
        run("true", shells=("bash",))
        checks.append(("inherited-BASH_ENV-never-runs", not os.path.exists(env_marker)))
    finally:
        os.environ.pop("BASH_ENV", None) if saved_env is None else os.environ.__setitem__("BASH_ENV", saved_env)
        shutil.rmtree(env_dir, ignore_errors=True)
    saved = os.environ.get("BASH_FUNC_gh%%")
    os.environ["BASH_FUNC_gh%%"] = "() { echo FUNC; }"
    try:
        r = run("gh pr merge 4", shells=("bash",))[0]
        checks.append(("inherited-function-ignored", r["calls"] == ["STUB gh pr merge 4"]))
    finally:
        os.environ.pop("BASH_FUNC_gh%%", None) if saved is None else os.environ.__setitem__("BASH_FUNC_gh%%", saved)
    marker_dir = tempfile.mkdtemp(prefix="stubbed-shell-test-")
    marker = os.path.join(marker_dir, "alive")
    try:
        run(f"(sleep 1; touch '{marker}') & echo started", shells=("bash",), timeout=10)
        time.sleep(2)
        checks.append(("background-child-killed", not os.path.exists(marker)))
    finally:
        shutil.rmtree(marker_dir, ignore_errors=True)
    r = run("mkdir -p d/e && touch d/e/f && chmod 000 d/e d", shells=("sh",))[0]
    checks.append(("read-only-tree-cleaned", r["rc"] == 0))
    left = [d for d in os.listdir(tempfile.gettempdir()) if d.startswith("stubbed-shell-") and d not in before]
    checks.append(("temp-dirs-removed", not left))
    failed = [n for n, ok in checks if not ok]
    print(f"run-shell-stubbed self-test: {'OK' if not failed else 'FAIL ' + str(failed)} ({len(checks)} checks)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
