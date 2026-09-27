#!/usr/bin/env python3
"""Run a shell command string with gh and git replaced by recording stand-ins (P-TODO 3b116).

Hook and guard verification sometimes has to confirm how a real shell treats a command string (does bash
join this continuation, does `sh -c` run this). Doing that with a shell-FUNCTION stub is unsafe: a nested
`sh -c` does not inherit bash functions, and on 2026-09-27 such a check ran the real `gh pr merge 1`
against the live repository (no effect, the PR was long merged). A first design here layered environment
tricks and name-matching refusals; review showed ordinary shell forms defeat each of those, so this version
leans on an enforcement mechanism bash itself provides:

  1. Restricted bash (`bash --norc --noprofile -r`) runs the command, with PATH set to a read-only directory
     holding only: gh and git stand-ins (isolated Python recorders, not shells, so no function the command
     defines can reach them), wrappers named bash and sh that start restricted bash again without startup
     files, and an audited whitelist of utilities none of which can run another program or write file
     content. Restricted mode forbids changing PATH, SHELL, ENV or BASH_ENV, command names containing a
     slash, `command -p`, `hash -p`, `exec`, `enable -f`, turning restriction off, and output redirection;
     on this host it also passes no exported function to a child. Bash builtins such as `history -w`
     and `fc` can still write into the working directory (its own subdirectory of the temp dir), but
     restricted mode refuses a slash in their file names, so they cannot reach the call log or captured
     output one level up; the PATH directory is read-only; a file written there cannot be run by name or
     sourced out of restriction; and the nested shells skip startup files, so a written .bashrc is inert. A real gh or git is therefore unreachable, including from a nested
     shell or a background child.
  2. The environment is built from scratch, not inherited: PATH, a temporary HOME and gh/XDG config dirs,
     and, as a second layer, an invalid GH_TOKEN, a reserved .invalid GH_HOST and git config off.
  3. Every process in the run's session is killed, and the temp dir removed, when the command ends; a child
     that survived would find PATH naming a removed directory and could run nothing.

LIMITS, stated: output redirection (`>`) is refused, as restricted mode requires, so a command string that
redirects cannot be verified here; the whitelisted utilities refuse any argument containing a slash, so a
command that names a path elsewhere cannot be verified (a utility can still read a file whose name arrives on
stdin, such as wc --files0-from=-, which is reading like `<` below); TMPDIR is not read-only, so bash can put
a large here-doc's short-lived temp file, with content the command chose, in any writable directory; loader
variables (LD_*, GCONV_PATH) are dropped before each wrapper execs the real program, but the wrappers' own
Python starts with them, which matters only if the command can create a shared object, and none of the
whitelisted utilities can; the fc builtin likewise writes a temp file of history lines the command chose to
TMPDIR (or /tmp), which stays if the shell is killed while the editor runs; resource limits (ulimit) are allowed,
so a command can stop a stand-in from recording a call (it exits 1, the call is missing from the report, and no
warning is printed); and a SIGKILL to this tool itself skips cleanup, leaving the session running;
input redirection (`<`, `$(< file)`) is allowed by restricted mode, so a command can read any file the user
can read and print it into the report (reading, not writing: nothing runs or changes); `sh` is emulated by `bash --posix` (dash has no restricted mode), so a
dash-only difference is not observed. This relies on bash's restricted mode and on the whitelist audit; it is not a
kernel sandbox.

Usage:
    python3 tools/run-shell-stubbed.py [--shell bash|sh|both] [--stub NAME ...] 'COMMAND'
    python3 tools/run-shell-stubbed.py --self-test

Output: per shell, the exit code, stdout, stderr and each stubbed call as `STUB <name> <argv...>`.
Exit codes: 0 ran (or self-test passed); 1 self-test failed; 2 usage error; 3 processes of the run were
still alive at the kill deadline.
"""
from __future__ import annotations

import argparse
import shlex
import threading
import contextlib
import io
import json
import re
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
# Audited (3b116 QA r3): none has an option that runs another program or writes file content. sort (its
# --compress-program runs a program; -o writes a file), touch and chmod (which let the command plant or
# enable a script) are deliberately absent.
WHITELIST = ("cat", "sleep", "true", "false", "head", "tail", "tr", "wc", "grep", "mkdir", "ls", "basename",
             "dirname", "seq")
INVALID_HOST = "stubbed-shell.invalid"
# The stand-in is an isolated Python recorder, not a shell: a bash stand-in runs unrestricted and imports
# SHELLOPTS and PS4 from the environment, so a command could make it run a program through PS4 (3b116 QA r3,
# r5; restricted bash passes no exported function to a child here, so functions were not the route).
# One JSON line per call, so no argument (a separator byte, a newline) can split or forge a record (QA r7).
SHIM = """#!{python} -I
import json, sys
with open({log!r}, "a", encoding="utf-8") as fh:
    fh.write(json.dumps([{name!r}] + sys.argv[1:]) + "\\n")
"""
UTIL_WRAPPER = """#!{python} -I
import os, sys
args = sys.argv[1:]
if any("/" in a or a == ".." for a in args):
    sys.stderr.write("{name}: refused: a path argument (only names in the working directory)\\n")
    sys.exit(126)
env = {{k: v for k, v in os.environ.items() if not (k.startswith("LD_") or k == "GCONV_PATH")}}
os.execve({real!r}, [{name!r}] + args, env)
"""
# Nested shells start restricted bash again with no startup files. The wrapper admits only short options that
# neither load a file nor make the shell interactive or a login shell: an interactive shell reads HOME's
# history file and a startup file runs before restriction applies (3b116 QA r3, r8). Long options are refused.
SHELL_WRAPPER = """#!{python} -I
import os, sys
args = sys.argv[1:]
i = 0
while i < len(args):
    a = args[i]
    if a == "--" or a[:1] not in "-+" or a in ("-", "+"):
        break
    if a in ("-o", "+o"):
        i += 2
        continue
    if a.startswith("--") or set(a[1:]) - set("abcefhkmnptuvxBCEHPT"):
        sys.stderr.write("{name}: refused: option " + a + " (interactive, login and long options can load files)\\n")
        sys.exit(126)
    i += 1
env = {{k: v for k, v in os.environ.items() if not (k.startswith("LD_") or k == "GCONV_PATH")}}
os.execve({bash!r}, [{bash!r}, "--norc", "--noprofile"] + {posix!r} + ["-r"] + args, env)
"""


def _rmtree(path: str) -> None:
    """Remove the temp dir even after the command made parts of it unreadable."""
    try:
        shutil.rmtree(path)
        return
    except OSError:
        pass
    os.chmod(path, stat.S_IRWXU)
    for root, dirs, _files in os.walk(path, topdown=True):
        os.chmod(root, stat.S_IRWXU)
        for d in dirs:
            os.chmod(os.path.join(root, d), stat.S_IRWXU)
    shutil.rmtree(path)


def _procs_under(paths) -> "list[int]":
    """PIDs owned by this user whose working directory is inside one of paths (a test helper)."""
    roots = [os.path.realpath(x) + os.sep for x in paths]
    out = []
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            if os.stat(f"/proc/{entry}").st_uid != os.getuid():
                continue
            cwd = os.readlink(f"/proc/{entry}/cwd") + os.sep
        except OSError:
            continue
        if any(cwd.startswith(r) for r in roots):
            out.append(int(entry))
    return out


def _all_procs_named(cmdline: str) -> "list[tuple[int, str]]":
    """(pid, cmdline) of processes owned by this user whose command line is exactly cmdline (a test helper)."""
    out = []
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            with open(f"/proc/{entry}/cmdline", "rb") as fh:
                cmd = fh.read().replace(b"\0", b" ").decode("utf-8", "replace").strip()
            if cmd == cmdline and os.stat(f"/proc/{entry}").st_uid == os.getuid():
                out.append((int(entry), cmd))
        except OSError:
            continue
    return out


def _session_members(sid: int) -> "list[tuple[int, str]]":
    """(pid, state) of every process whose session id is sid."""
    out = []
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            with open(f"/proc/{entry}/stat", encoding="utf-8") as fh:
                fields = fh.read().rsplit(")", 1)[1].split()
        except OSError:
            continue
        if int(fields[3]) == sid:  # after the command name: state, ppid, pgrp, session
            out.append((int(entry), fields[0]))
    return out


GRACE_SECONDS = 2.0
_CLEANUP_SIGNALS = {signal.SIGTERM, signal.SIGHUP, signal.SIGINT}


def _live(members) -> "list[int]":
    return [pid for pid, state in members if state not in ("Z", "X")]


def _kill_session(sid: int) -> bool:
    """Kill every process in the run's session. start_new_session makes the shell a session leader; `set -m`
    moves a child into a new process group but not out of the session, and setsid is not reachable (3b116
    QA r3). A fork loop can outpace killing, so members are first STOPPED until a pass finds none still
    running (a stopped process cannot fork), then killed until the session is empty (3b116 QA r6). True when
    the session is empty; False if members remained at the deadline."""
    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline:
        running = [pid for pid, state in _session_members(sid) if state not in ("T", "t", "Z", "X")]
        if not running:
            break
        for pid in running:
            try:
                os.kill(pid, signal.SIGSTOP)
            except ProcessLookupError:
                pass
    while time.monotonic() < deadline:
        members = [pid for pid, state in _session_members(sid) if state not in ("Z", "X")]
        if not members:
            return True
        # Stop every member again before killing any: a job-control group orphaned by a kill is sent SIGCONT
        # by the kernel and could resume forking (3b116 QA r9).
        for pid in members:
            try:
                os.kill(pid, signal.SIGSTOP)
            except ProcessLookupError:
                pass
        for pid in members:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        time.sleep(0.02)
    return not [pid for pid, state in _session_members(sid) if state not in ("Z", "X")]


def _prepare(tmp: str, stubs) -> tuple[str, str, str]:
    bindir, home, log = os.path.join(tmp, "bin"), os.path.join(tmp, "home"), os.path.join(tmp, "calls.log")
    os.makedirs(bindir)
    os.makedirs(os.path.join(home, ".config"))
    open(log, "w").close()
    for name in stubs:
        with open(os.path.join(bindir, name), "w", encoding="utf-8") as fh:
            fh.write(SHIM.format(python=sys.executable, name=name, log=log))
    for name, posix in (("bash", []), ("sh", ["--posix"])):
        with open(os.path.join(bindir, name), "w", encoding="utf-8") as fh:
            fh.write(SHELL_WRAPPER.format(python=sys.executable, bash=BASH, posix=posix, name=name))
    for name in list(stubs) + ["bash", "sh"]:
        os.chmod(os.path.join(bindir, name), 0o755)
    for util in WHITELIST:
        real = shutil.which(util, path="/usr/bin:/bin")
        if real and not os.path.exists(os.path.join(bindir, util)):
            # A wrapper, not a symlink: restricted mode limits command names, not arguments, so the utility
            # itself refuses a path argument; it cannot read or create anything outside the work dir
            # (3b116 QA r6).
            with open(os.path.join(bindir, util), "w", encoding="utf-8") as fh:
                fh.write(UTIL_WRAPPER.format(python=sys.executable, name=util, real=real))
            os.chmod(os.path.join(bindir, util), 0o755)
    os.chmod(bindir, 0o555)  # nothing can be planted on PATH (3b116 QA r3)
    return bindir, home, log


class _Terminated(Exception):
    pass


def _on_signal(signum, _frame):
    raise _Terminated(signum)


def run(command: str, shells=("bash", "sh"), stubs=DEFAULT_STUBS, timeout: int = 30) -> list[dict]:
    """Run command under each shell (restricted bash; sh as restricted bash --posix); one result dict each."""
    results = []
    # SIGTERM and SIGHUP are turned into an exception so the finally blocks kill the session and remove the temp
    # dir (only SIGINT did before; QA r8). Handlers are installed only from the main thread.
    saved_handlers = {}
    if threading.current_thread() is threading.main_thread():
        saved_handlers[signal.SIGINT] = signal.getsignal(signal.SIGINT)
        for sig in (signal.SIGTERM, signal.SIGHUP):
            saved_handlers[sig] = signal.signal(sig, _on_signal)
    try:
        return _run_shells(command, shells, stubs, timeout, results)
    finally:
        for sig, handler in saved_handlers.items():
            signal.signal(sig, handler)


def _run_shells(command, shells, stubs, timeout, results) -> list[dict]:
    for shell in shells:
        tmp = tempfile.mkdtemp(prefix="stubbed-shell-")
        cleanup_mask = None
        try:
            bindir, home, log = _prepare(tmp, stubs)
            env = {"PATH": bindir, "HOME": home, "LANG": "C.UTF-8", "GH_CONFIG_DIR": os.path.join(home, ".config", "gh"),
                   "XDG_CONFIG_HOME": os.path.join(home, ".config"), "GH_TOKEN": "stubbed-shell-invalid",
                   "GH_HOST": INVALID_HOST, "GH_PROMPT_DISABLED": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                   "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0"}
            argv = [BASH, "--norc", "--noprofile"] + (["--posix"] if shell == "sh" else []) + ["-r", "-c", command]
            # The command runs in its own subdirectory: restricted mode refuses a slash in a builtin's file
            # name, so it cannot overwrite the call log or captured output one level up (3b116 QA r5).
            work = os.path.join(tmp, "work")
            os.makedirs(work)
            out_path, err_path = os.path.join(tmp, "stdout"), os.path.join(tmp, "stderr")
            with open(out_path, "w") as o_fh, open(err_path, "w") as e_fh:
                p = subprocess.Popen(argv, stdout=o_fh, stderr=e_fh, stdin=subprocess.DEVNULL, env=env, cwd=work,
                                     start_new_session=True)
                timed_out = ""
                try:
                    rc = p.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    rc, timed_out = None, f"timed out after {timeout}s"
                finally:
                    # A second signal must not cut cleanup short (3b116 QA r9), so the three are BLOCKED, not
                    # ignored, until this shell's temp dir is removed: a signal that arrives meanwhile is
                    # delivered afterwards (the run still stops), and nothing ignored is inherited by the next
                    # shell (fix-check after QA r9). Main thread only.
                    if threading.current_thread() is threading.main_thread():
                        cleanup_mask = signal.pthread_sigmask(signal.SIG_BLOCK, _CLEANUP_SIGNALS)
                    grace_end = time.monotonic() + GRACE_SECONDS
                    while time.monotonic() < grace_end and _live(_session_members(p.pid)):
                        time.sleep(0.02)  # let a backgrounded call finish recording (QA r8)
                    killed = len(_live(_session_members(p.pid)))
                    contained = _kill_session(p.pid)
                    p.wait()
            with open(out_path, encoding="utf-8", errors="replace") as fh:
                out = fh.read()
            with open(err_path, encoding="utf-8", errors="replace") as fh:
                err = fh.read() + timed_out
            with open(log, encoding="utf-8") as fh:
                records = [json.loads(line) for line in fh if line.strip()]
            results.append({"shell": shell, "rc": rc, "stdout": out, "stderr": err, "contained": contained,
                            "killed": killed,
                            "session": p.pid, "calls": ["STUB " + shlex.join(r) for r in records], "argv": records})
        finally:
            _rmtree(tmp)
            if cleanup_mask is not None:
                signal.pthread_sigmask(signal.SIG_SETMASK, cleanup_mask)
    return results


def _printable(line: str) -> str:
    """Control characters escaped, so the command's output cannot rewrite the report on a terminal (QA r7)."""
    return "".join(c if c.isprintable() or c == "\t" else repr(c)[1:-1] for c in line)


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
    for name in args.stub:  # a plain name only: it becomes a file in the PATH dir (QA r7)
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name) or name in ("bash", "sh") + WHITELIST:
            print(f"ERROR: --stub {name!r}: not a plain executable name, or a name the tool reserves.", file=sys.stderr)
            return 2
    stubs = tuple(dict.fromkeys(DEFAULT_STUBS + tuple(args.stub)))
    shells = ("bash", "sh") if args.shell == "both" else (args.shell,)
    uncontained = False
    for r in run(args.command, shells, stubs):
        print(f"== {r['shell']} rc={r['rc']}")
        uncontained = uncontained or not r["contained"]
        if r["killed"]:
            print(f"WARNING: {r['killed']} process(es) were still running {GRACE_SECONDS:.0f}s after the command "
                  f"ended and were killed; a call they would have made is missing")
        if not r["contained"]:
            print("WARNING: processes of this run were still alive at the kill deadline")
        for c in r["calls"]:
            print("STUB " + _printable(c[5:]))  # a call argument cannot forge a report line (QA r8)
        # The command's own output is prefixed, so it cannot pass for a report line (3b116 QA r6).
        for label in ("stdout", "stderr"):
            if r[label]:
                print(f"-- {label}\n" + "\n".join("| " + _printable(line)
                                                       for line in r[label].rstrip("\n").split("\n")))
    return 3 if uncontained else 0  # an uncontained run is not a normal result (QA r7)


def _self_test() -> int:
    checks = []
    before = {d for d in os.listdir(tempfile.gettempdir()) if d.startswith("stubbed-shell-")}
    for r in run("gh pr 'merge' 1; sh -c 'gh \"pr\" merge 2'; bash -c \"git push\"; bash -e -c 'gh pr create'"):
        checks.append((f"{r['shell']}-nested-shells-hit-stubs", r["calls"] ==
                       ["STUB gh pr merge 1", "STUB gh pr merge 2", "STUB git push", "STUB gh pr create"]))
    r = run("gh pr merge 'a b' ''", shells=("sh",))[0]
    checks.append(("argument-boundaries-kept", r["argv"] == [["gh", "pr", "merge", "a b", ""]]))
    # Every route to a real program that ordinary shell syntax offers is refused. The target is the harmless
    # /usr/bin/id, so a regression can only ever run id; each case names the refusal it expects and the
    # stand-in calls it expects, and no case may show id's output (3b116 QA r6).
    slash = "restricted: cannot specify `/' in command names"
    for label, cmd, expect, calls in (
            ("slash-path", "/usr/bin/id", slash, []), ("path-change", "PATH=/usr/bin; id", "PATH: readonly variable", []),
            ("path-prefix", "PATH=/usr/bin id", "PATH: readonly variable", []),
            ("command-p", "command -p id", "command: -p: restricted", []), ("exec", "exec /usr/bin/id", "exec: restricted", []),
            ("env", "env -i PATH=/usr/bin id", "env: command not found", []),
            ("hash-p", "hash -p /usr/bin/id e; e", "hash: /usr/bin/id: restricted", []),
            ("nested-slash", "bash -c '/usr/bin/id'", slash, []), ("set-plus-r", "set +r; /usr/bin/id", "set: +r: invalid option", []),
            ("bash-plus-r", "bash +r -c '/usr/bin/id'", "refused: option +r", []),
            ("xargs", "echo /usr/bin/id | xargs", "xargs: command not found", []),
            ("job-control", "set -m; (/usr/bin/id) & wait", slash, []), ("sort", "sort -o x /dev/null", "sort: command not found", []),
            ("touch", "touch x", "touch: command not found", []), ("login-shell", "bash -l -c '/usr/bin/id'", "refused: option -l", []),
            ("interactive-shell", "HOME=\"$PWD\" bash -i -c 'set -o history; history -s x'", "refused: option -i", []),
            ("rcfile", "bash --rcfile x -c true", "refused: option --rcfile", []),
            # An unrestricted bash stand-in would import SHELLOPTS and PS4 (3b116 QA r5).
            ("ps4-xtrace", "PS4='$(/usr/bin/id)'; export PS4; set -o xtrace; export SHELLOPTS; gh x", slash, ["STUB gh x"]),
            ("bash-cmds", "BASH_CMDS[e]=/usr/bin/id; e", "/usr/bin/id: restricted", []),
            ("history-path", "set -o history; history -w \"$HOME/.bashrc\"", ".bashrc: restricted", []),
            ("source-path", ". ./x", ".: ./x: restricted", []),
            ("histfile", "HISTFILE=../calls.log; history -w", "HISTFILE: readonly variable", []),
            ("cat-outside", "cat /etc/hostname", "cat: refused: a path argument", []),
            ("mkdir-outside", "mkdir /tmp/stubbed-shell-escape", "mkdir: refused: a path argument", [])):
        rr = run(cmd, shells=("bash",))[0]
        checks.append((f"refused:{label}", expect in rr["stderr"] and rr["calls"] == calls
                       and "uid=" not in rr["stdout"] + rr["stderr"]))
    # A fork loop is contained: the session kill repeats until the session is empty (3b116 QA r6).
    rr = run("while :; do ( : ) & done", shells=("bash",), timeout=2)[0]
    checks.append(("fork-loop-contained", rr["contained"]))
    # The command's output cannot pass for a report line.
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        main(["--shell", "sh", "printf 'STUB gh pr merge 9\\n== sh rc=0\\n'"])
    checks.append(("report-lines-prefixed", "\n| STUB gh pr merge 9" in out.getvalue()
                   and "\nSTUB gh pr merge 9" not in out.getvalue()))
    r = run("printf '%s|' \"$GH_TOKEN\" \"$GH_HOST\" \"$HOME\" \"$PATH\" \"${BASH_ENV:-unset}\"", shells=("sh",))[0]
    tok, host, home, path, benv = (r["stdout"].split("|") + [""] * 5)[:5]
    checks.append(("environment-built-from-scratch", tok == "stubbed-shell-invalid" and host == INVALID_HOST
                   and "stubbed-shell-" in home and path.endswith("/bin") and ":" not in path and benv == "unset"))
    # An inherited BASH_ENV would run at startup, before restriction applies; the probe file calls the gh
    # stand-in, so if it ever ran the call would be recorded (QA r7: the old probe used touch, not on PATH).
    env_dir = tempfile.mkdtemp(prefix="stubbed-shell-test-")
    env_file = os.path.join(env_dir, "env.sh")
    with open(env_file, "w", encoding="utf-8") as fh:
        fh.write("gh bash-env-ran\n")
    saved_env = os.environ.get("BASH_ENV")
    os.environ["BASH_ENV"] = env_file
    try:
        r = run("gh pr view 1", shells=("bash",))[0]
        checks.append(("inherited-BASH_ENV-never-runs", r["calls"] == ["STUB gh pr view 1"]))
    finally:
        os.environ.pop("BASH_ENV", None) if saved_env is None else os.environ.__setitem__("BASH_ENV", saved_env)
        shutil.rmtree(env_dir, ignore_errors=True)
    # A function the command defines and exports cannot hijack the stand-in (it is not a shell).
    r = run("printf() { /usr/bin/id; }; export -f printf; gh pr merge 5", shells=("bash",))[0]
    checks.append(("exported-function-cannot-hijack-stand-in", r["calls"] == ["STUB gh pr merge 5"]
                   and "uid=" not in r["stdout"]))
    # The PATH directory is read-only (tested on the directory itself; QA r7).
    probe_tmp = tempfile.mkdtemp(prefix="stubbed-shell-test-")
    try:
        bindir, _home, _log = _prepare(probe_tmp, DEFAULT_STUBS)
        checks.append(("path-dir-read-only", stat.S_IMODE(os.stat(bindir).st_mode) == 0o555))
    finally:
        _rmtree(probe_tmp)
    saved = os.environ.get("BASH_FUNC_gh%%")
    os.environ["BASH_FUNC_gh%%"] = "() { echo FUNC; }"
    try:
        r = run("gh pr merge 4", shells=("bash",))[0]
        checks.append(("inherited-function-ignored", r["calls"] == ["STUB gh pr merge 4"]))
    finally:
        os.environ.pop("BASH_FUNC_gh%%", None) if saved is None else os.environ.__setitem__("BASH_FUNC_gh%%", saved)
    # Nothing in the run's session survives it, in the background or under job control (QA r7: the session is
    # observed directly after the run returns).
    for label, cmd in (("background", "sleep 30 & echo started"), ("job-control", "set -m; sleep 30 & echo started")):
        r = run(cmd, shells=("bash",), timeout=10)[0]
        alive = _session_members(r["session"])
        checks.append((f"{label}-child-killed", r["contained"] and not alive))
        if alive:
            _kill_session(r["session"])
    # A backgrounded call is recorded, not killed before it runs (QA r8).
    r = run("(sleep 0.3; gh pr merge 11) & echo started", shells=("bash",))[0]
    checks.append(("background-call-recorded", r["calls"] == ["STUB gh pr merge 11"] and r["killed"] == 0))
    # A SIGTERM to the tool still kills the command and removes the temp dir (QA r8). The sleep length is a
    # token unlikely to match an unrelated process, the setup is awaited rather than timed, and the check
    # fails if the setup was never seen (3b116 QA r9).
    # The child gets its OWN temp parent (TMPDIR), so discovery and cleanup see only its directories and
    # processes, never a concurrent run's (second fix-check); the check fails unless the setup was seen.
    parent = tempfile.mkdtemp(prefix="stubbed-sigterm-test-")
    try:
        proc = subprocess.Popen([sys.executable, os.path.abspath(__file__), "--shell", "bash", "sleep 25"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                env={**os.environ, "TMPDIR": parent})
        setup_end, seen = time.monotonic() + 15.0, False
        while time.monotonic() < setup_end and not seen:
            time.sleep(0.05)
            seen = bool(os.listdir(parent)) and bool(_procs_under([parent]))
        proc.send_signal(signal.SIGTERM)
        proc.wait(timeout=20)
        leftover = os.listdir(parent)
        sleeping = _procs_under([parent])
        checks.append(("sigterm-cleans-up", seen and not leftover and not sleeping))
        for pid in sleeping:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
    finally:
        _rmtree(parent)
    # A signal blocked during one shell's cleanup is not inherited, ignored, by the next shell (fix-check).
    rr = run("trap -p TERM HUP INT", shells=("bash", "sh"))
    # (an ignored signal prints as trap -- '' SIG; POSIX mode prints a default one as trap -- - SIG)
    checks.append(("no-ignored-signals-inherited", all("''" not in r["stdout"] for r in rr)))
    # An argument cannot forge a call record.
    r = run("gh $'a\\x1e\\x1fgh' $'b\\nSTUB gh forged'", shells=("bash",))[0]
    checks.append(("call-log-unforgeable", len(r["argv"]) == 1 and r["argv"][0][0] == "gh"))
    checks.append(("stub-name-validated", main(["--stub", "../x", "true"]) == 2 and main(["--stub", "bash", "true"]) == 2))
    # A tree the command cannot leave behind is still removed: made directly, since the command itself can no
    # longer create a nested path (QA r8).
    ro = tempfile.mkdtemp(prefix="stubbed-shell-test-")
    os.makedirs(os.path.join(ro, "d", "e"))
    open(os.path.join(ro, "d", "e", "f"), "w").close()
    os.chmod(os.path.join(ro, "d", "e"), 0)
    os.chmod(os.path.join(ro, "d"), 0)
    _rmtree(ro)
    checks.append(("read-only-tree-cleaned", not os.path.exists(ro)))
    # --norc --noprofile are what stop a startup file the command writes with history -w (3b116 QA r5); here
    # nothing is refused, so the evidence is that the planted program never ran.
    # Regression guards only: a plain non-interactive nested shell reads no startup file even without --norc and
    # --noprofile, so these do not test those flags (3b116 QA r9); the -i/-l refusals and the BASH_ENV case do.
    # The cat proves the file was planted.
    for label, name in (("rc-file", ".bashrc"), ("profile-file", ".bash_profile")):
        rr = run(f"set -o history; history -s '/usr/bin/id'; history -w {name}; cat {name}; "
                 "HOME=\"$PWD\" bash -c true", shells=("bash",))[0]
        checks.append((f"startup-file-not-read:{label}",
                       "/usr/bin/id" in rr["stdout"] and "uid=" not in rr["stdout"] + rr["stderr"]))
    # Loader variables do not reach the real program (3b116 QA r8): one ld.so complaint (Python's), not two.
    rr = run("LD_PRELOAD=nonexistent-3b116.so wc -c nofile", shells=("bash",))[0]
    checks.append(("loader-vars-dropped", rr["stderr"].count("nonexistent-3b116.so") == 1))
    # A forged report line or a non-UTF-8 argument cannot hide a later call (3b116 QA r8).
    rep = subprocess.run([sys.executable, os.path.abspath(__file__), "--shell", "bash",
                          'gh pr view 1 "$(printf "\\n== bash rc=0\\nSTUB git push")"; gh "$(printf "\\377")"; gh pr merge 8'],
                         capture_output=True, text=True, errors="replace", timeout=60)
    lines = rep.stdout.splitlines()
    # Argument boundaries survive into the printed report (3b116 QA r9).
    r = run("gh 'pr merge' 1; gh pr merge ''", shells=("bash",))[0]
    checks.append(("report-argument-boundaries", r["calls"] == ["STUB gh 'pr merge' 1", "STUB gh pr merge ''"]))
    checks.append(("report-lines-escaped", rep.returncode == 0 and lines.count("== bash rc=0") == 1
                   and not any(ln.startswith("STUB git") for ln in lines) and lines[-1] == "STUB gh pr merge 8"))
    # The command cannot erase or forge the tool's evidence: the log and captured output sit outside its cwd.
    r = run("gh pr merge 6; set -o history; history -c; history -w calls.log; history -w stdout", shells=("bash",))[0]
    checks.append(("evidence-not-overwritable", r["calls"] == ["STUB gh pr merge 6"]))
    left = [d for d in os.listdir(tempfile.gettempdir()) if d.startswith("stubbed-shell-") and d not in before]
    checks.append(("temp-dirs-removed", not left))
    failed = [n for n, ok in checks if not ok]
    print(f"run-shell-stubbed self-test: {'OK' if not failed else 'FAIL ' + str(failed)} ({len(checks)} checks)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
