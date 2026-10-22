#!/usr/bin/env python3
"""Validate native push records and run the full guard without cached passes."""
import os
from pathlib import Path
import posixpath
import pwd
import re
import subprocess
import sys
import tempfile
import time
from urllib.parse import unquote, urlsplit


def guarded_destination(url):
    # Match the owner/repository on any host, including local test remotes.
    url = unquote(url).casefold().rstrip("/")
    path = urlsplit(url).path if "://" in url else url.split(":", 1)[-1]
    path = posixpath.normpath(path).rstrip("/")
    if path.endswith(".git"):
        path = path[:-4].rstrip("/")
    return path == "jposluns/grc_library" or path.endswith("/jposluns/grc_library")


def clean_environment():
    env = {k: v for k, v in os.environ.items()
           if k in ("LANG", "TMPDIR", "TERM", "GRC_STORE", "SSH_AUTH_SOCK",
                    "http_proxy", "https_proxy", "ftp_proxy", "all_proxy", "no_proxy",
                    "HTTP_PROXY", "HTTPS_PROXY", "FTP_PROXY", "ALL_PROXY", "NO_PROXY")
           or k.startswith("LC_")}
    env["PATH"] = "/usr/bin:/bin"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["HOME"] = pwd.getpwuid(os.getuid()).pw_dir
    env["PYTHONNOUSERSITE"] = "1"
    return env


def main():
    if len(sys.argv) != 3:
        raise ValueError("expected remote name and destination URL")
    if not guarded_destination(sys.argv[2]):
        return 0
    env = clean_environment()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], env=env,
                                   text=True).strip()
    guarded = False
    for line in sys.stdin:
        fields = line.removesuffix("\n").split(" ")
        if len(fields) != 4:
            raise ValueError("malformed pre-push ref record")
        local_ref, sha, remote_ref, remote_sha = fields
        if re.fullmatch(r"0{40}|0{64}", sha):
            continue
        # Tags and other namespaces retain the dirty-tree backstop's policy.
        if not remote_ref.startswith("refs/heads/"):
            continue
        kind = subprocess.check_output(["git", "cat-file", "-t", sha],
                                       env=env, text=True).strip()
        if kind != "commit" or sha != head:
            raise ValueError("push from a checkout whose HEAD is the commit being "
                             "pushed; every branch update must equal HEAD")
        guarded = True
    if not guarded:
        return 0
    rc = subprocess.call(["sh", "tools/install-git-hooks.sh", "--check"], env=env)
    if rc:
        return rc
    # Separate file descriptions avoid racing the child's write offset. The
    # guard sees a regular file (RM-10); Git receives output during the run.
    git_dir = subprocess.check_output(["git", "rev-parse", "--git-dir"],
                                      env=env, text=True).strip()
    with tempfile.TemporaryDirectory(prefix="pre-push-log-", dir=git_dir) as tmp:
        path = Path(tmp) / "output"
        with path.open("wb") as out, path.open("rb") as incoming:
            with subprocess.Popen(["bash", "tools/pre-push-guard.sh"], env=env,
                                  stdout=out, stderr=subprocess.STDOUT) as child:
                while True:
                    chunk = incoming.read(65536)
                    if chunk:
                        sys.stdout.buffer.write(chunk)
                        sys.stdout.buffer.flush()
                    elif child.poll() is not None:
                        # A final read after observing exit catches the last write.
                        sys.stdout.buffer.write(incoming.read())
                        sys.stdout.buffer.flush()
                        if child.returncode:
                            return child.returncode if child.returncode >= 0 else 1
                        current = subprocess.check_output(
                            ["git", "rev-parse", "HEAD"], env=env, text=True).strip()
                        dirty = subprocess.check_output(
                            ["git", "status", "--porcelain", "--untracked-files=no"],
                            env=env, text=True)
                        # Every branch SHA was bound to head before the guard.
                        if current != head or dirty:
                            raise ValueError("HEAD or tracked tree changed during the guard")
                        return 0
                    else:
                        time.sleep(0.05)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"pre-push guard: refusing on error: {exc}", file=sys.stderr)
        sys.exit(1)
