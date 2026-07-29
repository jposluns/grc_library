#!/usr/bin/env python3
"""PreToolUse hook: block a WRITE to the maintainer's frozen public ``.working/`` tree.

Shipped 2026-07-29 (maintainer-directed, the ``.working`` -> ``_private`` migration writer
contract). After PR2b-2b copied ``.working/`` into ``grc_library_private/.working/``, the private
copy is the CANONICAL working-state store (``lint_common.resolve_working*`` resolves there) and
the public ``grc_library/.working/`` tree was DELETED in PR #1235 (PR2b-3). This hook now guards
against its RE-CREATION: any WRITE that would re-materialize a path under the public tree is the
public tree is the codex-I-4/I-5 wrong-tree/recreate bug: a tool or a bookkeeping step that writes
public ``.working`` diverges it from the private canonical copy, and a divergence is lost or split
at the delete. This hook is the mechanical enforcement of the writer contract: for the MAINTAINER
(with ``_private`` present) a write to public ``.working`` is refused; the write belongs in
``_private``.

Fires on Edit, Write, and Bash. BLOCKS (exit 2) only when ALL hold:
  (a) operator is the MAINTAINER (origin remote is ``jposluns/grc_library``), AND
  (b) ``grc_library_private/.working/`` EXISTS (the private canonical store is in place), AND
  (c) the operation WRITES/CREATES a path under ``<repo>/.working/`` (an Edit/Write ``file_path``,
      or a Bash write-shape, found by shlex-tokenizing the command (so quoted MULTI-token text is not
      mis-scanned) and resolving each write TARGET: a ``>``/``>>``/``>|``/fd redirect, a
      ``cp``/``mv``/``rsync``/``install`` DESTINATION (honouring ``-t``/``--target-directory``),
      ``tee``, ``touch``, ``mkdir``, ``sed -i``, ``dd of=``, or a ``git checkout``/``restore``/``stash``
      of a ``.working`` path, with ``$PWD``/``$(pwd)``/``$HOME``/``~`` expanded).
Removals (``rm``, ``git rm``, ``git clean``) are ALLOWED (the PR2b-3 delete is a removal). Reads are
ALLOWED.

Adopter (no ``_private``): ``.working/`` is the adopter's OWN live tree -> ALLOW (never block).
Fail-open on any uncertainty: a false block bricks the session, a false allow only misses the guard
(the delete-time freeze+compare still covers it). A hook bug must never be worse than the bug it
prevents. Genuinely-dynamic write forms (a shell variable, ``xargs``, a subshell ``cd``) are not
statically resolvable and are accepted fail-open by design.

Escape: a Bash command carrying ``WorkingWrite: intentional`` proceeds (the narrow authorized case).

Exit protocol (Claude Code hooks): exit 0 allows; exit 2 blocks and feeds stderr to the model.
Self-test: ``python3 .claude/hooks/block-public-working-write.py --self-test``.
"""

import json
import os
import re
import shlex
import sys
from pathlib import Path

MAINTAINER_ORIGIN = "jposluns/grc_library"
ORIGIN_BLOCK_RE = re.compile(r'\[remote "origin"\][^\[]*', re.DOTALL)
URL_RE = re.compile(r"url\s*=\s*(\S+)")
ESCAPE = "WorkingWrite: intentional"

# Bash WRITE-shape detection. A lexical scan cannot resolve full shell semantics, so this is a
# BEST-EFFORT, FAIL-OPEN, FALSE-POSITIVE-AVERSE detector (a false BLOCK bricks the session and
# drives escape-hatch overuse, worse than a missed write the delete-time freeze+compare and the
# tools' own require-private resolvers still catch). We TOKENIZE with shlex so quotes are respected
# (a `.working` path inside a commit message or a grep pattern is an ARGUMENT, never a write
# target), then read write TARGETS from redirects and a small write-verb set and resolve each
# against the repo. Statically-resolvable expansions ($PWD, $(pwd), $HOME, leading ~) are expanded;
# genuinely-dynamic forms (a shell variable, xargs, a subshell cd) are accepted fail-open.
# RESIDUE (documented per the state-the-proxy discipline; maintainer-directed 2026-07-29 after a
# dual-family re-verify): shlex drops quote-provenance and command-position, so a QUOTED
# single-character operator (a bare `>` argument) and a bare write-verb WORD in argument position
# can over-block, and unspaced/dynamic/exotic-verb forms under-block. Both classes are bounded
# (they act on the now-DELETED public tree and are escape-covered) and are the accepted
# best-effort/fail-open cost of a stdlib-only static scan; the decision was to keep the detector
# and document the residue rather than emulate a full shell parser.
_HOME = os.path.expanduser("~")
_WRITE_VERBS = {"cp", "mv", "rsync", "install"}          # DEST = -t/--target-directory or last non-option arg
_CREATE_VERBS = {"tee", "touch", "mkdir"}                # every non-option arg is a target
_GIT_RESTORE_SUBCMDS = {"checkout", "restore", "stash"}  # git subcommands that WRITE files from history
_SHELL_SEP = {";", "|", "||", "&&", "&", "|&"}
_REDIR_TOK_RE = re.compile(r"^(?:\d*>{1,2}|&>>?)\|?(.*)$")


def _expand(tok, project_dir):
    """Best-effort expansion of the statically-resolvable shell forms."""
    for pwd_form in ("$(pwd)", "${PWD}", "$PWD"):
        tok = tok.replace(pwd_form, project_dir)
    tok = tok.replace("${HOME}", _HOME).replace("$HOME", _HOME)
    if tok == "~":
        tok = _HOME
    elif tok.startswith("~/"):
        tok = _HOME + tok[1:]
    return tok


def _origin_is_maintainer(project_dir: str) -> bool:
    cfg = Path(project_dir) / ".git" / "config"
    try:
        text = cfg.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    block = ORIGIN_BLOCK_RE.search(text)
    if not block:
        return False
    m = URL_RE.search(block.group(0))
    if not m:
        return False
    url = m.group(1)
    norm = url[:-4] if url.endswith(".git") else url
    return norm == MAINTAINER_ORIGIN or norm.endswith("/" + MAINTAINER_ORIGIN) or norm.endswith(":" + MAINTAINER_ORIGIN)


def _private_working_present(project_dir: str) -> bool:
    return (Path(project_dir).resolve().parent / "grc_library_private" / ".working").is_dir()


def _path_under_public_working(project_dir: str, file_path: str) -> bool:
    """True if file_path resolves under <repo>/.working/ (public), not the private sibling."""
    try:
        repo = Path(project_dir).resolve()
        p = Path(file_path)
        p = p if p.is_absolute() else (repo / p)
        p = p.resolve()
    except (OSError, ValueError):
        return False
    pub = (repo / ".working").resolve()
    try:
        p.relative_to(pub)
        return True
    except ValueError:
        return False


def _bash_write_targets(command, project_dir):
    """Candidate WRITE-target paths, from redirects and a small write-verb set, via shlex so
    quoted text (a commit message, a grep pattern) is never mis-scanned. A `.working/` SOURCE of
    a copy-out is not a target; a `sed` without -i is a read; git checkout/restore/stash of a
    `.working` path is a recreate; $PWD/$(pwd)/$HOME/~ are expanded."""
    try:
        toks = shlex.split(command, comments=False, posix=True)
    except ValueError:
        return []  # unbalanced quotes etc.: unparseable -> fail-open (do not block)
    targets = []
    i, n = 0, len(toks)
    while i < n:
        t = toks[i]
        if t and (t.lstrip("0123456789").startswith(">") or t.startswith("&>")):  # redirect: >f >>f >|f 2>f &> &>>, or standalone
            mm = _REDIR_TOK_RE.match(t)
            attached = mm.group(1) if mm else ""
            if attached:
                targets.append(attached)
            elif i + 1 < n:
                targets.append(toks[i + 1]); i += 1
            i += 1; continue
        if t == "dd":
            for a in toks[i + 1:]:
                if a in _SHELL_SEP:
                    break
                if a.startswith("of="):
                    targets.append(a[3:])
            i += 1; continue
        if t == "git":
            sub = toks[i + 1] if i + 1 < n else ""
            if sub in _GIT_RESTORE_SUBCMDS:
                for a in toks[i + 2:]:
                    if a in _SHELL_SEP:
                        break
                    if not a.startswith("-"):
                        targets.append(a)  # a restored pathspec under .working is a recreate
            i += 1; continue
        if t in _WRITE_VERBS:
            args, tdir, want_dir = [], None, False
            j = i + 1
            while j < n and toks[j] not in _SHELL_SEP:
                a = toks[j]
                if want_dir:
                    tdir = a; want_dir = False
                elif a in ("-t", "--target-directory"):
                    want_dir = True
                elif a.startswith("--target-directory="):
                    tdir = a.split("=", 1)[1]
                elif not a.startswith("-"):
                    args.append(a)
                j += 1
            if tdir is not None:
                targets.append(tdir)      # explicit DEST dir; SOURCES not flagged
            elif args:
                targets.append(args[-1])  # last non-option arg is the DEST
            i = j; continue
        if t in _CREATE_VERBS:
            j = i + 1
            while j < n and toks[j] not in _SHELL_SEP:
                if not toks[j].startswith("-"):
                    targets.append(toks[j])
                j += 1
            i = j; continue
        if t == "sed":
            seg, has_i = [], False
            for a in toks[i + 1:]:
                if a in _SHELL_SEP:
                    break
                seg.append(a)
                if a.startswith("-i") or a.startswith("--in-place"):
                    has_i = True
            if has_i:  # only -i writes; a read sed (no -i) has no write target
                targets += [a for a in seg if not a.startswith("-")]
            i += 1; continue
        i += 1
    return [_expand(t, project_dir) for t in targets]


def _bash_writes_public_working(command, project_dir):
    """Does the Bash command WRITE/CREATE a path under public .working/? Fail-open (False) on the
    escape or on any candidate that does not resolve under the repo's public .working/."""
    if ESCAPE in command:
        return False
    for target in _bash_write_targets(command, project_dir):
        if _path_under_public_working(project_dir, target):
            return True
    return False


def decide(tool_name: str, tool_input: dict, project_dir: str) -> str | None:
    """Return a block reason string, or None to allow. Pure; fail-open (None) on uncertainty."""
    if not project_dir:
        return None
    if not _origin_is_maintainer(project_dir):
        return None
    if not _private_working_present(project_dir):
        return None
    if tool_name in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        fp = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        if fp and _path_under_public_working(project_dir, fp):
            return (
                f"BLOCKED (public-.working writer-contract guard): {fp} would RE-CREATE a path under "
                f"the public grc_library/.working/ tree, which was DELETED in PR #1235 (PR2b-3). The "
                f"canonical working-state store is the private-sibling working-state tree "
                f"(resolve_working* resolves there); the public tree must not be re-created. Write to "
                f"the private location instead, or use resolve_working_for_write."
            )
        return None
    if tool_name == "Bash":
        cmd = tool_input.get("command", "") or ""
        if _bash_writes_public_working(cmd, project_dir):
            return (
                "BLOCKED (public-.working writer-contract guard): this command writes/creates under "
                "the public grc_library/.working/ tree, which was DELETED in PR #1235 (PR2b-3); this "
                "guard now prevents its RE-CREATION. The canonical store is the private-sibling "
                "working-state tree; target that instead. (Removals such as `rm`/`git rm` are "
                "allowed; add `WorkingWrite: intentional` to the command only for a genuinely "
                "authorized public-.working write.)"
            )
        return None
    return None


def _self_test() -> int:
    import tempfile, textwrap
    failures = []
    def mk_repo(origin_url, with_private):
        parent = tempfile.mkdtemp()
        d = Path(parent) / "grc_library"; d.mkdir()
        g = d / ".git"; g.mkdir()
        (g / "config").write_text(f'[remote "origin"]\n\turl = {origin_url}\n')
        (d / ".working").mkdir()
        if with_private:
            (Path(parent) / "grc_library_private" / ".working").mkdir(parents=True, exist_ok=True)
        return str(d)
    # maintainer + private present
    m = mk_repo("https://github.com/jposluns/grc_library.git", True)
    cases = [
        ("Write", {"file_path": ".working/DONE.md"}, m, True, "Write to public .working blocked"),
        ("Edit", {"file_path": f"{m}/.working/session-handoff.md"}, m, True, "Edit abs public .working blocked"),
        ("Write", {"file_path": "security/policy.md"}, m, False, "Write to corpus allowed"),
        ("Write", {"file_path": "../grc_library_private/.working/DONE.md"}, m, False, "Write to private .working allowed"),
        ("Bash", {"command": "echo x > .working/next-prs.txt"}, m, True, "redirect to public .working blocked"),
        ("Bash", {"command": "cp a.md .working/b.md"}, m, True, "cp into public .working blocked"),
        ("Bash", {"command": "mkdir -p .working/newdir"}, m, True, "mkdir public .working blocked"),
        ("Bash", {"command": "sed -i 's/a/b/' .working/DONE.md"}, m, True, "sed -i public .working blocked"),
        ("Bash", {"command": "cat .working/DONE.md"}, m, False, "read public .working allowed"),
        ("Bash", {"command": "grep -n x .working/DONE.md"}, m, False, "grep public .working allowed"),
        ("Bash", {"command": "git rm -r .working"}, m, False, "git rm public .working allowed"),
        ("Bash", {"command": "rm -rf .working"}, m, False, "rm public .working allowed"),
        ("Bash", {"command": "echo x > grc_library_private/.working/DONE.md"}, m, False, "redirect to private allowed"),
        ("Bash", {"command": "echo x > .working/DONE.md  # WorkingWrite: intentional"}, m, False, "escape allowed"),
        ("Bash", {"command": "git commit -m 'a .working->.working link and .working->_private move'"}, m, False, "arrow in prose not a redirect"),
        ("Bash", {"command": f"echo x > {m}/.working/recreated.txt"}, m, True, "abs-path redirect recreating public working blocked"),
        ("Bash", {"command": "cp .working/DONE.md /tmp/DONE.md"}, m, False, "cp working SOURCE (copy-out) allowed"),
        ("Bash", {"command": "mv .working/DONE.md /tmp/DONE.md"}, m, False, "mv working SOURCE allowed"),
        ("Bash", {"command": "cp a.md /tmp/b.md"}, m, False, "cp no-working not blocked"),
        ("Bash", {"command": "rsync .working/DONE.md /tmp/DONE.md"}, m, False, "rsync working SOURCE allowed"),
        ("Bash", {"command": f"echo x 2> {m}/.working/err.log"}, m, True, "fd-redirect (2>) recreating public working blocked"),
        ("Bash", {"command": "sed -n '1,20p' .working/README.md"}, m, False, "sed READ (no -i) allowed"),
        ("Bash", {"command": "sed 's/a/b/' .working/file"}, m, False, "sed no -i (read) allowed"),
        ("Bash", {"command": "cp --target-directory=/tmp .working/source"}, m, False, "cp copy-out via --target-directory allowed"),
        ("Bash", {"command": "mv -t /tmp .working/source"}, m, False, "mv copy-out via -t allowed"),
        ("Bash", {"command": "install .working/source /tmp/out"}, m, False, "install SOURCE .working allowed"),
        ("Bash", {"command": "printf '%s' 'echo x > .working/example'"}, m, False, "quoted redirect text not a write"),
        ("Bash", {"command": "git commit -m 'touch .working records now live in _private'"}, m, False, "verb+.working in commit message not a write"),
        ("Bash", {"command": "grep -n 'touch .working/x' README.md"}, m, False, "verb+.working in grep pattern not a write"),
        ("Bash", {"command": "printf x >| .working/force.txt"}, m, True, "clobber redirect >| to public working blocked"),
        ("Bash", {"command": "dd if=/dev/null of=.working/dd.bin"}, m, True, "dd of= into public working blocked"),
        ("Bash", {"command": "cp source --target-directory=.working"}, m, True, "cp DEST via --target-directory=.working blocked"),
        ("Bash", {"command": "mv -t .working source"}, m, True, "mv DEST via -t .working blocked"),
        ("Bash", {"command": "touch $PWD/.working/x"}, m, True, "$PWD-expanded public working write blocked"),
        ("Bash", {"command": "touch $(pwd)/.working/x"}, m, True, "$(pwd)-expanded public working write blocked"),
        ("Bash", {"command": "git checkout HEAD~1 -- .working/README.md"}, m, True, "git checkout restore of public working blocked"),
        ("Bash", {"command": "git restore --source=HEAD~1 .working/DONE.md"}, m, True, "git restore of public working blocked"),
        ("Bash", {"command": "git checkout other-branch"}, m, False, "git checkout branch (no .working path) allowed"),
        ("Bash", {"command": "printf .working/x | xargs touch"}, m, False, "xargs indirection accepted fail-open"),
        ("Bash", {"command": "echo x &> .working/log.txt"}, m, True, "bash &> both-streams redirect to public working blocked"),
        ("Bash", {"command": "echo x &>> .working/log.txt"}, m, True, "bash &>> both-streams append to public working blocked"),
        ("Bash", {"command": "echo x > /tmp/out 2>&1"}, m, False, "2>&1 fd-dup not a public-working target"),
    ]
    for tn, ti, pd, want_block, label in cases:
        got = decide(tn, ti, pd)
        if bool(got) != want_block:
            failures.append(f"  {label}: want_block={want_block} got_block={bool(got)}  ({got or 'allowed'})")
    # adopter (no private) -> never block
    a = mk_repo("https://github.com/someuser/grc_library.git", False)
    for tn, ti, label in [("Write", {"file_path": ".working/DONE.md"}, "adopter Write"), ("Bash", {"command": "echo x > .working/x"}, "adopter Bash")]:
        if decide(tn, ti, a):
            failures.append(f"  adopter must not be blocked: {label}")
    # maintainer but NO private working (pre-copy) -> allow (nothing canonical yet)
    mnp = mk_repo("https://github.com/jposluns/grc_library.git", False)
    if decide("Write", {"file_path": ".working/DONE.md"}, mnp):
        failures.append("  maintainer without _private/.working must allow (pre-copy)")
    if failures:
        print("SELF-TEST FAILED:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"OK: block-public-working-write self-test passed ({len(cases)+3} cases).")
    return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # fail-open
    if not isinstance(payload, dict):
        return 0  # fail-open: a non-object top-level JSON has no tool fields
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    try:
        reason = decide(tool_name, tool_input, project_dir)
    except Exception:
        return 0  # fail-open on any bug
    if reason:
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
