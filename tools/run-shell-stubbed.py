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


def _session_survivors(sid: int, timeout: float = 5.0) -> "list[int]":
    """Live members of a finished run's session, read once none is left or timeout has passed (a test helper).
    A killed process stays in /proc as a zombie until its reaper collects it, and a loaded host delays that; a
    zombie is dead, so it is not a survivor and the wait does not stay for it (3b125, QA r1)."""
    deadline = time.monotonic() + timeout
    live = _live(_session_members(sid))
    while live and time.monotonic() < deadline:
        time.sleep(0.02)
        live = _live(_session_members(sid))
    return live


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


# The loaded-host reproduction for 3b125: adopt an exited orphan (PR_SET_CHILD_SUBREAPER, 36).
# waitid(WNOWAIT) observes its exit without reaping it; reap only after checking the real zombie.
# Where the subreaper cannot be set (a non-Linux host, or a container that blocks prctl), the probe says so and
# why, and runs nothing (3b125 QA r1).
SLOW_REAPER_PROBE = r"""
import ctypes, json, os, runpy, sys, types
try:
    adopted = ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) == 0
    reason = "" if adopted else "prctl(PR_SET_CHILD_SUBREAPER) failed: " + os.strerror(ctypes.get_errno())
except (AttributeError, OSError, TypeError) as exc:
    adopted, reason = False, "prctl(PR_SET_CHILD_SUBREAPER) unavailable: " + repr(exc)
if not adopted:
    print(json.dumps(dict(adopted=False, reason=reason)))
    sys.exit(0)
tool = runpy.run_path(sys.argv[1], run_name="run_shell_stubbed_probe")
readfd, writefd = os.pipe()
middle = os.fork()
if middle == 0:
    os.close(readfd)
    os.setsid()
    child = os.fork()
    if child == 0:
        os._exit(0)
    os.write(writefd, str(child).encode())
    os._exit(0)
os.close(writefd)
child = int(os.read(readfd, 100))
os.close(readfd)
os.waitpid(middle, 0)
# WNOWAIT leaves a real, adopted zombie for the single scan under test.
os.waitid(os.P_PID, child, os.WEXITED | os.WNOWAIT)
contained = tool["_kill_session"](middle)
members = tool["_session_members"](middle)
zombies = [pid for pid, state in members if state == "Z"]
scans, waits = [], []
fn = tool["_session_survivors"]
g = dict(fn.__globals__)
def scan(sid):
    scans.append(sid)
    if len(scans) != 1:
        raise AssertionError("zombie caused another scan")
    return tool["_session_members"](sid)
def sleep(seconds):
    waits.append(seconds)
    raise AssertionError("zombie caused retry sleep")
g.update(_session_members=scan,
         time=types.SimpleNamespace(monotonic=g["time"].monotonic, sleep=sleep))
call = types.FunctionType(fn.__code__, g, fn.__name__, fn.__defaults__)
try:
    try:
        survivors = call(middle)
    except AssertionError:
        survivors = None
    print(json.dumps(dict(adopted=True, contained=contained, zombies=zombies, survivors=survivors,
                         scans=len(scans), retried=bool(waits))))
finally:
    os.waitpid(child, 0)
"""


# Self-test ceilings are monotonic liveness guards, not latency requirements.
# 120s is four times the ordinary command budget; compound probes get 300s.
# An independent supervisor bounds the complete self-test, including cleanup,
# to 420s execution plus 120s emergency cleanup, below the 600s gate wrapper.
# A deadline breach aborts with a named failure rather than accumulating waits.
TEST_WAIT = 120.0
TEST_PROCESS_WAIT = 300.0


def _test_children(pid):
    try:
        with open(f"/proc/{pid}/task/{pid}/children") as stream:
            return [int(value) for value in stream.read().split()]
    except FileNotFoundError:
        return []


def _supervise_test(callback, ceiling, name, cleanup_wait=TEST_WAIT, report=True):
    """Supervise the entire test, including waits inside production cleanup.

    Only self-test callers use this Linux subreaper. The supervising process
    never runs the callback or its mocks. Stop parents before enumerating their
    children, then kill and reap the owned tree, including separate sessions.
    The private directory belongs to this supervisor, not the blocked worker.
    """
    import ctypes
    previous = ctypes.c_int()
    reason = ""
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        if (libc.prctl(37, ctypes.byref(previous), 0, 0, 0) != 0
                or libc.prctl(36, 1, 0, 0, 0) != 0):
            reason = "child subreaper prctl failed: " + os.strerror(ctypes.get_errno())
    except (AttributeError, OSError, TypeError) as exc:
        reason = "child subreaper prctl unavailable: " + repr(exc)
    # Without adoption, retain the parent's fork/wait deadline and best-effort
    # tree cleanup, but do not claim the subreaper-dependent checks ran.
    original_children = set(_test_children(os.getpid()))
    parent = tempfile.mkdtemp(prefix="shell-self-test-supervised-")
    worker, status, failure = None, None, None
    clean = False
    unverified = False
    def owned():
        return [pid for pid in _test_children(os.getpid())
                if pid not in original_children]
    def stop_tree(pid):
        try:
            os.kill(pid, signal.SIGSTOP)
        except ProcessLookupError:
            return
        for child in _test_children(pid):
            stop_tree(child)
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        sys.stdout.flush()
        sys.stderr.flush()
        worker = os.fork()
        if worker == 0:
            try:
                tempfile.tempdir = parent
                os.environ["TMPDIR"] = parent
                globals()["_TEST_SUBREAPER_SKIP"] = reason
                rc = callback()
            except BaseException:
                import traceback
                traceback.print_exc()
                rc = 1
            sys.stdout.flush()
            sys.stderr.flush()
            os._exit(rc)
        deadline = time.monotonic() + ceiling
        while True:
            done, status = os.waitpid(worker, os.WNOHANG)
            if done:
                break
            if time.monotonic() >= deadline:
                failure = name
                break
            time.sleep(0.02)
    finally:
        # This deadline is independent of every production cleanup function.
        end = time.monotonic() + cleanup_wait
        if reason and worker in owned():
            unverified = True
            # Kill only the pipe owner first. Its watcher must remain
            # runnable to sweep sessions orphaned outside this supervisor.
            try:
                os.kill(worker, signal.SIGKILL)
            except ProcessLookupError:
                pass
            # Without adoption we cannot prove when the sweep finishes;
            # give it the remaining cleanup budget before stopping trees.
            while time.monotonic() < end:
                time.sleep(min(0.02, max(0.0, end - time.monotonic())))
        while owned():
            for pid in owned():
                stop_tree(pid)
            for pid in owned():
                try:
                    os.waitpid(pid, os.WNOHANG)
                except ChildProcessError:
                    pass
            if not owned() or time.monotonic() >= end:
                break
            time.sleep(0.02)
        clean = not owned()
        _rmtree(parent)
        clean = clean and not os.path.exists(parent)
        if not reason:
            libc.prctl(36, previous.value, 0, 0, 0)
    if unverified:
        clean = False
        failure = name + ":cleanup-unverified"
    elif not clean:
        failure = name + ":cleanup"
    if failure and report:
        print(f"run-shell-stubbed self-test: FAIL {[failure]}", flush=True)
    rc = 1 if failure else os.waitstatus_to_exitcode(status)
    return rc, failure, clean


def _cleanup_deadline_check():
    # C1: exercise the public self-test supervisor, not just its helper.
    # A second supervisor bounds this regression if that wiring is removed.
    with tempfile.NamedTemporaryFile() as ready:
        def probe():
            def blocked():
                globals().update(GRACE_SECONDS=0)
                with _self_test_limits():
                    def failed_kill(sid):
                        with open(ready.name, "w") as stream:
                            stream.write(str(sid))
                        return False
                    globals()["_kill_session"] = failed_kill
                    run("sleep 3600", shells=("bash",))
                return 0
            globals().update(TEST_WAIT=0.1, TEST_PROCESS_WAIT=2.9,
                             _self_test_worker=blocked)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                rc = _self_test()
            return 0 if (rc == 1 and "self-test-execution-deadline"
                         in output.getvalue()) else 1
        rc, failure, clean = _supervise_test(
            probe, 10.0, "cleanup-hang-regression-wrapper",
            cleanup_wait=5.0, report=False)
        ready.seek(0)
        return rc == 0 and failure is None and clean and bool(ready.read())


def _self_test() -> int:
    try:
        # 420s execution + 120s emergency cleanup is below the 600s wrapper.
        return _supervise_test(
            _self_test_worker, TEST_PROCESS_WAIT + TEST_WAIT,
            "self-test-execution-deadline")[0]
    except BaseException as exc:
        print(f"run-shell-stubbed self-test: FAIL ['self-test-supervision: {exc!r}']")
        return 1


def _fixture_identity(pid):
    """Return the session leader's Linux start time, or None."""
    try:
        with open(f"/proc/{pid}/stat") as stream:
            fields = stream.read().rsplit(")", 1)[1].split()
        return fields[19] if int(fields[3]) == pid else None
    except (OSError, ValueError, IndexError):
        return None


def _fixture_watch():
    """A pipe-owned supervisor kills registered sessions when the test dies.

    Registration happens before exec, so SIGKILL between spawn and wait cannot
    strand a fixture. Children close the writer at exec; only this test owns it.
    This is test scaffolding, independent of the production cleanup under test.
    Its preexec_fn selects fork plus exec instead of posix_spawn/vfork.
    Registration includes the leader's start time to reject reused session IDs.
    """
    readfd, writefd = os.pipe()
    watcher = os.fork()
    if watcher == 0:
        os.close(writefd)
        os.setsid()
        sessions, data = {}, b""
        try:
            while True:
                chunk = os.read(readfd, 4096)
                if not chunk:
                    break
                data += chunk
                while b"\n" in data:
                    line, data = data.split(b"\n", 1)
                    sid, started = line.decode().split()
                    sessions[int(sid)] = started
            deadline = time.monotonic() + TEST_WAIT
            while sessions and time.monotonic() < deadline:
                sessions = {sid: started for sid, started in sessions.items()
                            if _fixture_identity(sid) in (started, None)}
                live = [(sid, pid) for sid in sessions
                        for pid, state in _session_members(sid)
                        if state not in ("Z", "X")]
                if not live:
                    break
                # Stop all before killing any, including job-control groups.
                for sig in (signal.SIGSTOP, signal.SIGKILL):
                    for sid, pid in live:
                        if _fixture_identity(sid) not in (sessions[sid], None):
                            continue
                        try:
                            os.kill(pid, sig)
                        except ProcessLookupError:
                            pass
                time.sleep(0.02)
        finally:
            os._exit(0)
    os.close(readfd)
    return watcher, writefd


@contextlib.contextmanager
def _fixture_lifetime():
    watcher, writer = _fixture_watch()
    saved = subprocess.Popen
    class RegisteredProcess(saved):
        def __init__(self, *args, **kwargs):
            if kwargs.get("start_new_session"):
                before = kwargs.get("preexec_fn")
                def register():
                    pid = os.getpid()
                    started = _fixture_identity(pid)
                    if started is None:
                        raise RuntimeError("fixture leader identity unavailable")
                    os.write(writer, f"{pid} {started}\n".encode())
                    if before is not None:
                        before()
                kwargs["preexec_fn"] = register
            super().__init__(*args, **kwargs)
    subprocess.Popen = RegisteredProcess
    try:
        yield
    finally:
        subprocess.Popen = saved
        os.close(writer)
        os.waitpid(watcher, 0)


def _command_timeout_check(failures):
    # The supervisor's wait is independent of run's timeout. The pipe-owned
    # fixture watchdog also survives SIGKILL of this supervisor or its child.
    probe = r"""
import json, runpy, sys
t = runpy.run_path(sys.argv[1])
with t["_self_test_limits"]():
    r = t["run"]("while :; do ( : ) & done", shells=("bash",), timeout=2)[0]
    print(json.dumps(r))
"""
    proc = subprocess.Popen(
        [sys.executable, "-I", "-B", "-c", probe, os.path.abspath(__file__)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        out, _err = proc.communicate(timeout=TEST_PROCESS_WAIT)
        r = json.loads(out.splitlines()[-1])
        return (proc.returncode == 0 and r["rc"] is None
                and "timed out after 2s" in r["stderr"], r["contained"])
    except (subprocess.TimeoutExpired, ValueError, IndexError, KeyError):
        return False, False
    finally:
        if proc.poll() is None:
            proc.kill()
        try:
            proc.communicate(timeout=TEST_WAIT)
        except subprocess.TimeoutExpired:
            failures.append(("command-timeout-probe-cleanup-wait", False))


@contextlib.contextmanager
def _self_test_limits():
    # Only self-test execution receives the larger kill budget. A cloned
    # function keeps the production function and its five-second policy intact.
    import types
    saved_run, saved_kill, saved_survivors = run, _kill_session, _session_survivors
    g = dict(saved_kill.__globals__)
    g["time"] = types.SimpleNamespace(
        monotonic=lambda: time.monotonic() / 24, sleep=time.sleep)
    kill = types.FunctionType(saved_kill.__code__, g, saved_kill.__name__,
                              saved_kill.__defaults__)
    failures, allocated = [], []
    saved_prepare = _prepare
    def prepare(tmp, stubs):
        allocated.append(tmp)
        return saved_prepare(tmp, stubs)
    def bounded_run(*args, **kwargs):
        kwargs.setdefault("timeout", TEST_WAIT)
        results = saved_run(*args, **kwargs)
        if any(not r["contained"] for r in results):
            failures.append(("command-contained", False))
        if any(os.path.exists(path) for path in allocated):
            failures.append(("allocated-temp-dirs-removed", False))
        return results
    def survivors(sid, timeout=TEST_WAIT):
        return saved_survivors(sid, timeout)
    globals().update(run=bounded_run, _kill_session=kill,
                     _session_survivors=survivors, _prepare=prepare)
    try:
        with _fixture_lifetime():
            yield failures
    finally:
        globals().update(run=saved_run, _kill_session=saved_kill,
                         _session_survivors=saved_survivors, _prepare=saved_prepare)


def _background_call_check():
    # A real recorder is held until the production grace loop yields. The
    # lock is released on the first grace sleep; deleting grace cannot pass
    # just because the recorder happened to run early.
    import fcntl
    import types
    saved_shim, saved_time, saved_grace = SHIM, time, GRACE_SECONDS
    with tempfile.NamedTemporaryFile() as gate:
        fcntl.flock(gate, fcntl.LOCK_EX)
        def release(seconds):
            fcntl.flock(gate, fcntl.LOCK_UN)
            saved_time.sleep(seconds)
        try:
            globals()["SHIM"] = SHIM.replace(
                "import json, sys",
                "import json, sys, fcntl\nwith open(" + repr(gate.name) +
                ") as gate:\n    fcntl.flock(gate, fcntl.LOCK_SH)")
            globals()["time"] = types.SimpleNamespace(
                monotonic=saved_time.monotonic, sleep=release)
            globals()["GRACE_SECONDS"] = TEST_WAIT
            r = run("(gh pr merge 11) & echo started", shells=("bash",))[0]
            return r["calls"] == ["STUB gh pr merge 11"] and r["killed"] == 0
        finally:
            globals().update(SHIM=saved_shim, time=saved_time, GRACE_SECONDS=saved_grace)


def _policy_checks():
    """Exercise unchanged production code using a clock advanced by work.

    The signal oracle requires an exception AND cleanup. Recording a signal
    then returning from wait is a failure (the strengthened round-5 oracle).
    Timeout goes through public run, so dropping its argument fails.
    """
    import types
    results = []
    for route in ("grace", "timeout", "TERM", "HUP", "INT"):
        state = dict(clock=0.0, live=True, killed=False, removed=False,
                     late=False, elapsed=0.0)
        class Process:
            pid = 7
            def wait(self, timeout=None):
                if state["killed"]:
                    return 0
                if route == "timeout":
                    if timeout != 1:
                        state["late"] = True
                        return 0
                    raise subprocess.TimeoutExpired("model", timeout)
                if route in ("TERM", "HUP", "INT"):
                    os.kill(os.getpid(), getattr(signal, "SIG" + route))
                    state["late"] = True
                return 0
        def sleep(seconds):
            state["clock"] = round(state["clock"] + 0.125, 9)
            if state["clock"] > 10:
                raise AssertionError("model did not terminate")
        def kill(sid):
            state["elapsed"] = state["clock"]
            state["live"] = False
            state["killed"] = True
            return True
        g = dict(globals())
        g.update(
            open=lambda *a, **kw: io.StringIO(""),
            _prepare=lambda *a: ("bin", "home", "log"),
            tempfile=types.SimpleNamespace(mkdtemp=lambda **kw: "virtual"),
            os=types.SimpleNamespace(path=os.path, devnull=os.devnull, makedirs=lambda *a: None),
            time=types.SimpleNamespace(monotonic=lambda: state["clock"], sleep=sleep),
            subprocess=types.SimpleNamespace(Popen=lambda *a, **kw: Process(),
                DEVNULL=subprocess.DEVNULL, TimeoutExpired=subprocess.TimeoutExpired),
            _kill_session=kill,
            _rmtree=lambda path: state.update(removed=True),
            _session_members=lambda sid: [(7, "R")] if state["live"] else [])
        for name in ("run", "_run_shells"):
            fn = globals()[name]
            g[name] = types.FunctionType(fn.__code__, g, name, fn.__defaults__)
        class MissingProductionHandler(Exception):
            pass
        def missing_handler(signum, frame):
            raise MissingProductionHandler(signum)
        placeholder = getattr(signal, "SIG" + route) if route in ("TERM", "HUP") else None
        previous_handler = None
        if placeholder is not None:
            previous_handler = signal.signal(placeholder, missing_handler)
        error, answer = None, None
        try:
            answer = g["run"]("model", shells=("bash",), timeout=1)
        except AssertionError:
            results.append(("production-policy:" + route, False))
            continue
        except (_Terminated, KeyboardInterrupt, MissingProductionHandler) as exc:
            error = exc
        finally:
            if placeholder is not None:
                signal.signal(placeholder, previous_handler)
        ok = state["killed"] and state["removed"] and not state["late"]
        if route in ("TERM", "HUP", "INT"):
            ok = ok and isinstance(error, (_Terminated, KeyboardInterrupt))
        elif route == "timeout":
            ok = ok and answer[0]["rc"] is None and "timed out after 1s" in answer[0]["stderr"]
        else:
            ok = ok and state["elapsed"] == 2.0
        results.append(("production-policy:" + route, ok))
    clock, sends = [0.0], []
    def send(pid, sig):
        sends.append((pid, sig))
    def sleep(seconds):
        clock[0] = round(clock[0] + 0.125, 9)
        if clock[0] > 10:
            raise AssertionError("kill deadline did not terminate")
    fn = _kill_session
    g = dict(fn.__globals__)
    g.update(time=types.SimpleNamespace(monotonic=lambda: clock[0], sleep=sleep),
             os=types.SimpleNamespace(kill=send),
             _session_members=lambda sid: [(7, "T"), (8, "T")])
    kill = types.FunctionType(fn.__code__, g, fn.__name__, fn.__defaults__)
    try:
        ok = (kill(7) is False and clock[0] == 5.0
              and all((pid, sig) in sends for pid in (7, 8)
                      for sig in (signal.SIGSTOP, signal.SIGKILL)))
    except AssertionError:
        ok = False
    results.append(("production-five-second-kill-deadline", ok))
    return results


SIGNAL_PROBE = r"""
import os, runpy, subprocess, sys
t = runpy.run_path(sys.argv[1])
fd = int(sys.argv[2])
g = t["run"].__globals__
saved = subprocess.Popen
class Process(saved):
    def wait(self, timeout=None):
        if not getattr(self, "announced", False):
            self.announced = True
            os.write(fd, (str(self.pid) + "\n").encode())
        return super().wait(timeout=timeout)
subprocess.Popen = Process
with t["_self_test_limits"]():
    # A pipe-backed stub cannot finish naturally: the supervisor retains
    # the writer until after the tool has exited. There is no run timeout.
    readfd = int(sys.argv[3])
    g["SHIM"] = "#!{python} -I\nimport os\nos.read(" + str(readfd) + ", 1)\n"
    original_init = Process.__init__
    def init(self, *a, **kw):
        kw["pass_fds"] = tuple(kw.get("pass_fds", ())) + (readfd,)
        original_init(self, *a, **kw)
    Process.__init__ = init
    t["run"]("hold", shells=("bash",), stubs=("hold",), timeout=None)
"""


def _sigterm_cleanup_check(failures, timeout=TEST_WAIT):
    # Readiness comes from Popen.wait INSIDE the command's try/finally.
    # This deliberately avoids the production spawn race deferred to 3b281.
    # Read a pipe for readiness and wait on process exit, with independent
    # monotonic ceilings. Neither test depends on a command sleep duration.
    import selectors
    parent = tempfile.mkdtemp(prefix="stubbed-sigterm-test-")
    ready_r, ready_w = os.pipe()
    hold_r, hold_w = os.pipe()
    proc, sid = None, None
    try:
        proc = subprocess.Popen(
            [sys.executable, "-I", "-B", "-c", SIGNAL_PROBE,
             os.path.abspath(__file__), str(ready_w), str(hold_r)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            pass_fds=(ready_w, hold_r), env={**os.environ, "TMPDIR": parent})
        os.close(ready_w)
        ready_w = None
        deadline = time.monotonic() + timeout
        data = b""
        with selectors.DefaultSelector() as selector:
            selector.register(ready_r, selectors.EVENT_READ)
            while b"\n" not in data:
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not selector.select(remaining):
                    return False
                chunk = os.read(ready_r, 4096)
                if not chunk:
                    return False
                data += chunk
        sid = int(data.splitlines()[0])
        if proc.poll() is not None:
            return False
        proc.send_signal(signal.SIGTERM)
        # subprocess.wait uses a monotonic deadline and waitpid.
        proc.wait(timeout=max(0.001, deadline - time.monotonic()))
        return (proc.returncode != 0 and not os.listdir(parent)
                and not _session_survivors(
                    sid, timeout=max(0.0, deadline - time.monotonic())))
    except (subprocess.TimeoutExpired, ValueError):
        return False
    finally:
        if proc is not None:
            if proc.poll() is None:
                proc.kill()
            try:
                proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                failures.append(("sigterm-probe-cleanup-wait", False))
        # Release and kill even failed fixtures before removing their tree.
        os.close(hold_w)
        os.close(hold_r)
        os.close(ready_r)
        if ready_w is not None:
            os.close(ready_w)
        if sid is not None:
            _kill_session(sid)
        for pid in _procs_under([parent]):
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        _rmtree(parent)


def _self_test_worker() -> int:
    # All test-created dirs, including subprocess TMPDIRs, have one private
    # parent. Concurrent users of the system temp dir cannot affect this check.
    saved_int = signal.signal(signal.SIGINT, signal.default_int_handler)
    saved_temp, saved_env = tempfile.tempdir, os.environ.get("TMPDIR")
    with tempfile.TemporaryDirectory(prefix="shell-self-test-") as parent:
        tempfile.tempdir = parent
        os.environ["TMPDIR"] = parent
        try:
            reason = globals().get("_TEST_SUBREAPER_SKIP", "")
            policy = []
            if reason:
                print("run-shell-stubbed self-test: SKIP cleanup-hang-deadline "
                      f"({reason})", flush=True)
            else:
                policy.append(("cleanup-hang-deadline", _cleanup_deadline_check()))
            policy.extend(_policy_checks())
            with _self_test_limits() as failures:
                return _self_test_body(policy, failures)
        finally:
            signal.signal(signal.SIGINT, saved_int)
            tempfile.tempdir = saved_temp
            if saved_env is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = saved_env


def _self_test_body(policy, failures) -> int:
    checks, skipped = list(policy), []
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
    timed, contained = _command_timeout_check(failures)
    checks.append(("command-timeout-through-run", timed))
    checks.append(("fork-loop-contained", contained))
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
    # observed directly after the run returns). A killed child its reaper has not yet collected is still listed,
    # as a zombie, so only a live member fails the check, awaited (bounded) in case one is still dying (3b125).
    # The lifetime watcher kills these sessions even if the self-test is SIGKILLed.
    # 3600s exceeds this check's ceilings; natural exit cannot hide missing cleanup.
    for label, cmd in (("background", "sleep 3600 & echo started"), ("job-control", "set -m; sleep 3600 & echo started")):
        r = run(cmd, shells=("bash",), timeout=TEST_WAIT)[0]
        survivors = _session_survivors(r["session"])
        checks.append((f"{label}-child-killed", r["contained"] and not survivors))
        if survivors:
            _kill_session(r["session"])
    # Behind a reaper that has not collected (the loaded-host case, made certain), the exited child is a zombie and is
    # not a survivor: exactly one scan and no retry sleep, with no elapsed-time assertion. The check
    # fails unless the probe adopted the orphan and the zombie was really there (3b125). A probe that could not
    # set the subreaper is a skip, named in the result line with its reason; one that crashed or printed nothing
    # still fails (3b125 QA r1).
    reason = globals().get("_TEST_SUBREAPER_SKIP", "")
    if reason:
        seen = dict(adopted=False, reason=reason)
    else:
        probe = subprocess.run([sys.executable, "-I", "-B", "-c", SLOW_REAPER_PROBE, os.path.abspath(__file__)],
                               capture_output=True, text=True, timeout=TEST_PROCESS_WAIT)
        try:
            seen = json.loads(probe.stdout.splitlines()[-1])
        except (IndexError, ValueError):
            seen = {}
    if seen.get("adopted") is False and seen.get("reason"):
        skipped.append(f"slow-reaper-zombie-not-a-survivor ({seen['reason']})")
    else:
        checks.append(("slow-reaper-zombie-not-a-survivor", seen.get("adopted") is True
                       and seen.get("contained") is True and bool(seen.get("zombies")) and seen.get("survivors") == []
                       and seen.get("scans") == 1 and seen.get("retried") is False))
    checks.append(("background-call-recorded", _background_call_check()))
    checks.append(("sigterm-cleans-up", _sigterm_cleanup_check(failures)))
    # A signal blocked during one shell's cleanup is not inherited, ignored, by the next shell (fix-check).
    rr = run("trap -p TERM HUP INT", shells=("bash", "sh"))
    # (an ignored signal prints as trap -- '' SIG; POSIX mode prints a default one as trap -- - SIG)
    checks.append(("no-ignored-signals-inherited", all("''" not in r["stdout"] for r in rr)))
    for sig in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
        rr = run(f"kill -{sig.name[3:]} $$; echo survived", shells=("bash", "sh"))
        checks.append((f"no-ignored-signals-inherited:{sig.name}",
                       all(r["rc"] == -sig and not r["stdout"] for r in rr)))
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
    rep = subprocess.run([sys.executable, "-I", "-B", "-c",
                          "import runpy,sys; t=runpy.run_path(sys.argv[1]); "
                          "c=t['_self_test_limits'](); c.__enter__(); "
                          "sys.exit(t['main'](sys.argv[2:]))",
                          os.path.abspath(__file__), "--shell", "bash",
                          'gh pr view 1 "$(printf "\\n== bash rc=0\\nSTUB git push")"; gh "$(printf "\\377")"; gh pr merge 8'],
                         capture_output=True, text=True, errors="replace", timeout=TEST_PROCESS_WAIT)
    lines = rep.stdout.splitlines()
    # Argument boundaries survive into the printed report (3b116 QA r9).
    r = run("gh 'pr merge' 1; gh pr merge ''", shells=("bash",))[0]
    checks.append(("report-argument-boundaries", r["calls"] == ["STUB gh 'pr merge' 1", "STUB gh pr merge ''"]))
    checks.append(("report-lines-escaped", rep.returncode == 0 and lines.count("== bash rc=0") == 1
                   and not any(ln.startswith("STUB git") for ln in lines) and lines[-1] == "STUB gh pr merge 8"))
    # The command cannot erase or forge the tool's evidence: the log and captured output sit outside its cwd.
    r = run("gh pr merge 6; set -o history; history -c; history -w calls.log; history -w stdout", shells=("bash",))[0]
    checks.append(("evidence-not-overwritable", r["calls"] == ["STUB gh pr merge 6"]))
    # Private-parent inventory avoids concurrent global /tmp users. The prepare
    # audit also checks actual run allocation paths, including hard-coded paths.
    # Arbitrary unrelated file writes bypassing both remain outside this oracle.
    left = os.listdir(tempfile.gettempdir())
    checks.extend(dict.fromkeys(failures))
    checks.append(("temp-dirs-removed", not left))
    failed = [n for n, ok in checks if not ok]
    note = f"; skipped: {skipped}" if skipped else ""
    print(f"run-shell-stubbed self-test: {'OK' if not failed else 'FAIL ' + str(failed)} ({len(checks)} checks{note})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
