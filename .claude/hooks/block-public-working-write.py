#!/usr/bin/env python3
"""PreToolUse hook: guard selected paths and Bash write-target candidates at public ``.working``.

This guard supports the working-state migration away from the public checkout (``.working`` was copied
to ``grc_library_private/.working`` and the public tree was deleted in PR #1235). It checks origin text,
store-directory presence, and resolved paths; these are PROXIES, not proof of operator identity, a
canonical or writable store, an actual write, or re-creation of a deleted tree.

Registered in settings.json for Bash and Edit/Write. ``decide`` also recognizes MultiEdit and
NotebookEdit, but those tools are NOT registered for this hook.

A normal invocation blocks with exit 2 only when all of the following succeed:
  (a) In ``<project_dir>/.git/config``, a loose ``url =`` match (the ``URL_RE`` regex has no key
      boundary) within the first
      regex-matched ``[remote "origin"]`` block supplies a captured value which, after stripping a
      terminal ``.git``, equals ``jposluns/grc_library`` or ends with ``/`` or ``:`` plus it. Comments
      and key boundaries are NOT checked: a preceding ``pushurl`` can supply the match. No host,
      ownership, or operator identity is verified.
  (b) The primary candidate is a directory resolving OUTSIDE the resolved repository, OR
      ``<repo-parent>/grc_library_private/.working`` is a directory. A nonempty ``GRC_STORE`` selects the
      primary candidate; otherwise it is ``<repo-parent>/private``. Relative overrides resolve against the
      repository root. An unusable override does not fall back to the default primary candidate, but the
      legacy sibling is still checked (unless a resolution error propagates first). The legacy check does
      not verify resolved containment. Neither check verifies contents or writability.
  (c) For Edit/Write (or a direct MultiEdit/NotebookEdit call to ``decide``), the first truthy
      ``file_path``/``notebook_path`` resolves to the resolved ``<repo>/.working`` root or a descendant.
      For Bash, the command lacks the escape substring below and at least one scanner candidate resolves
      there. A candidate match does NOT prove a write.

The Bash scanner shlex-splits the command and reads candidate targets from redirect tokens and the words
``cp``/``mv``/``rsync``/``install``/``tee``/``touch``/``mkdir``/``dd``/``sed`` and ``git`` immediately
followed by ``checkout``/``restore``/``stash``. It groups quoted tokens but does NOT establish command
position, so quoted data, comments, heredoc bodies, scripts, and option values can produce candidates and
cause blocking; real writes can also be missed. ``rm``/``git rm``/``git clean`` and ordinary reads have no
write-verb branch, but their arguments or other tokens can still yield candidates. ``$PWD``/``$(pwd)``/
``$HOME``/``~`` are substituted textually; shell variables, ``xargs``, and a subshell ``cd`` are not
modeled. Both a candidate and the ``.working`` root follow symlinks, so a symlinked public/private tree can
make the spellings resolve to the same data; existing paths and the root itself can match.

A nonmatching origin proxy or a false store predicate allows. Invalid JSON handled by main, a non-object
payload, and exceptions from ``decide`` caught by main also allow; unparseable Bash quoting yields no
candidates. A primary-store check error can still fall through to a legacy-directory match and block.
Helpers are not uniformly exception-safe, and failures outside main's guarded operations are not
universally converted to exit 0.

Escape: the exact, case-sensitive substring ``WorkingWrite: intentional`` anywhere in a Bash command
bypasses this hook's Bash scan; authorization and placement are NOT verified, and the escape does not apply
to Edit/Write.

Exit protocol (Claude Code hooks): exit 0 allows; a block reason is printed to stderr and returns exit 2.
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

# Bash WRITE-shape detection: a best-effort candidate scan, NOT proof of a write. shlex groups
# quoted tokens but removes quote-provenance and does NOT establish command position, so a
# `.working` path inside a commit message, a grep pattern, or any argument can still match. We read
# candidate targets from redirect-like tokens and a small write-verb set (including verbs appearing
# as ordinary arguments); comments and heredoc bodies are NOT removed. Statically-resolvable
# expansions ($PWD, $(pwd), $HOME, leading ~) are substituted textually; shell variables, xargs,
# and a subshell cd are not modeled, so those writes can be MISSED. RESIDUE (state-the-proxy
# discipline; maintainer-directed 2026-07-29 after a dual-family re-verify): both false BLOCKS (a
# quoted operator or a write-verb word in argument position yielding an under-`.working` candidate)
# and missed writes are possible; downstream tools are not guaranteed to catch the misses. This is
# the accepted stdlib-only-static-scan cost; the decision was to keep the detector and document the
# residue rather than emulate a full shell parser.
_HOME = os.path.expanduser("~")
_WRITE_VERBS = {"cp", "mv", "rsync", "install"}          # candidate = recognized -t/--target-directory value, else last non-option token
_CREATE_VERBS = {"tee", "touch", "mkdir"}                # every non-option arg is a target
_GIT_RESTORE_SUBCMDS = {"checkout", "restore", "stash"}  # git subcommand words whose following non-option tokens are treated as candidates
_SHELL_SEP = {";", "|", "||", "&&", "&", "|&"}
_REDIR_TOK_RE = re.compile(r"^(?:\d*>{1,2}|&>>?)\|?(.*)$")


def _expand(tok, project_dir):
    """Textually substitute PWD/HOME forms and a whole ~ or leading ~/.

    PWD forms use project_dir; HOME forms use _HOME. This does not model shell quoting,
    variable-name boundaries, directory changes, or other expansions."""
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
    """Return the store-directory presence proxy that ACTIVATES this guard (not writability or
    canonical contents).

    A nonempty ``GRC_STORE`` selects the primary candidate (relative overrides resolve against the
    resolved repo root); otherwise the candidate is ``<repo-parent>/private``. The primary candidate
    qualifies only if it is a directory whose resolved path is OUTSIDE the resolved repo. An
    unusable ``GRC_STORE`` is NOT backfilled with the default primary candidate. A false primary check,
    or an OSError/ValueError caught inside its try block (e.g. from ``store.resolve()``), falls through to
    the legacy sibling ``grc_library_private/.working``, checked by ``is_dir()`` alone (it does NOT reject
    an inward-resolving symlink), so a caught primary-store resolution error can still yield True. Errors
    resolving the repository root or a relative override BEFORE that try block propagate instead. These checks parallel ``lint_common``'s store
    checks; they are not a full ``resolve_working`` call, and there is no ``deprecated`` lookup."""
    repo = Path(project_dir).resolve()
    env = os.environ.get("GRC_STORE")
    if env:
        # Nonempty GRC_STORE overrides only the primary candidate; resolve a relative value
        # against the REPO ROOT, as lint_common._store_root does. The legacy fallback remains.
        pe = Path(env)
        store = pe if pe.is_absolute() else (repo / pe).resolve()
    else:
        store = repo.parent / "private"
    try:
        if store.is_dir() and not store.resolve().is_relative_to(repo):
            return True  # the primary candidate is a directory resolving outside the repo
    except (OSError, ValueError):
        pass  # try the legacy sibling; a directory there can still activate blocking
    try:
        return (repo.parent / "grc_library_private" / ".working").is_dir()
    except OSError:
        return False


def _path_under_public_working(project_dir: str, file_path: str) -> bool:
    """True if file_path resolves to the resolved <repo>/.working root or a descendant.

    Relative paths use the resolved repository root. Both paths follow symlinks, so this is not a
    lexical public/private distinction; existing and absent paths can match. OSError/ValueError while
    resolving the repository or candidate returns False; resolving the .working root is outside that
    handler and can raise."""
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
    """Return expanded CANDIDATE strings from a shlex token scan, not proven write targets.

    Redirect-like tokens supply an attached suffix or the next token; dd supplies of= suffixes; git
    immediately followed by checkout/restore/stash supplies every following non-option token in its
    segment; cp/mv/rsync/install supply a recognized -t/--target-directory value else the last
    non-option token; tee/touch/mkdir supply every non-option token; sed supplies every non-option
    token (including scripts/option values) when any token in its segment starts with -i/--in-place.
    Argument scans stop at exact _SHELL_SEP tokens; copy/create branches advance past the segment.
    It handles -t/--target-directory specially but does not generally model option arity, shell control
    flow, or actual mutation; quoted
    arguments, comments, and heredoc data can be scanned; dynamic commands can match or be missed;
    _expand performs textual substitutions; unparseable quoting returns an empty list."""
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
                        targets.append(a)  # candidate only: may be a revision, option value, subcommand, or pathspec
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
                targets.append(tdir)      # recognized target-directory value; other operands omitted here
            elif args:
                targets.append(args[-1])  # approximate destination: last non-option token
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
            if has_i:  # a -i/--in-place prefix enables all non-option tokens as candidates
                targets += [a for a in seg if not a.startswith("-")]
            i += 1; continue
        i += 1
    return [_expand(t, project_dir) for t in targets]


def _bash_writes_public_working(command, project_dir):
    """True when any scanned CANDIDATE matches the resolved public .working root or a descendant.

    The exact ESCAPE substring anywhere in the command returns False before scanning. Otherwise return
    False only when NO candidate matches; a nonmatching candidate does not cancel a match. This is a
    lexical proxy for a write; exceptions not handled by the called helpers propagate to main."""
    if ESCAPE in command:
        return False
    for target in _bash_write_targets(command, project_dir):
        if _path_under_public_working(project_dir, target):
            return True
    return False


def decide(tool_name: str, tool_input: dict, project_dir: str) -> str | None:
    """Return a block reason for matching origin/store/path proxies, or None to allow.

    Reads filesystem and environment state through helpers (NOT pure). Edit/Write/MultiEdit/NotebookEdit
    use the first truthy file_path or notebook_path; Bash uses the candidate scanner and its substring
    escape. Unsupported tools allow. Exceptions can propagate; main, not this function, catches them."""
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
                f"BLOCKED (public-working-write): a write to {fp} resolving to the repository's resolved "
                f".working root or a descendant.\n"
                f"WHY: this hook's origin-URL and store-directory checks matched. It guards against "
                f"writes into the retired public working-state tree, but does not establish re-creation, "
                f"canonical contents, or store writability.\n"
                f"CONSIDER INSTEAD: choose the intended operational-store or legacy-sibling destination "
                f"and verify the resolved path (resolve_working_for_write can return an existing public file)."
            )
        return None
    if tool_name == "Bash":
        cmd = tool_input.get("command", "") or ""
        if _bash_writes_public_working(cmd, project_dir):
            return (
                "BLOCKED (public-working-write): a Bash call with a scanned candidate resolving "
                "to the repository's resolved .working root or a descendant.\n"
                "WHY: this hook's origin-URL and store-directory checks matched. The scanner does not "
                "prove the command writes; quoted data, comments, or other arguments can also match.\n"
                "CONSIDER INSTEAD: check the command and its intended destination (verify any path "
                "resolve_working_for_write returns; it can return an existing public file). `rm`, "
                "`git rm`, and `git clean` have no dedicated write-verb branch; reads and removals can "
                "still yield scanner candidates and be blocked. For an intentional bypass of this "
                "Bash scan, include `WorkingWrite: intentional` anywhere in the command; authorization is not verified."
            )
        return None
    return None


def _self_test() -> int:
    import tempfile
    failures = []
    # Remove ambient GRC_STORE so it cannot affect the fixtures. An existing external
    # override would otherwise make their store-presence checks succeed.
    _prev_store = os.environ.pop("GRC_STORE", None)
    def mk_repo(origin_url, with_private, with_store=False):
        parent = tempfile.mkdtemp()
        d = Path(parent) / "grc_library"; d.mkdir()
        g = d / ".git"; g.mkdir()
        (g / "config").write_text(f'[remote "origin"]\n\turl = {origin_url}\n')
        (d / ".working").mkdir()
        if with_private:
            (Path(parent) / "grc_library_private" / ".working").mkdir(parents=True, exist_ok=True)
        if with_store:
            (Path(parent) / "private").mkdir(parents=True, exist_ok=True)
        return str(d)
    # matching origin URL + legacy sibling .working directory present
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
        ("Bash", {"command": "echo x > grc_library_private/.working/DONE.md"}, m, False, "redirect to in-repo grc_library_private/.working outside public .working allowed"),
        ("Bash", {"command": "echo x > .working/DONE.md  # WorkingWrite: intentional"}, m, False, "escape allowed"),
        ("Bash", {"command": "git commit -m 'a .working->.working link and .working->_private move'"}, m, False, "arrow in prose not a redirect"),
        ("Bash", {"command": f"echo x > {m}/.working/recreated.txt"}, m, True, "abs-path redirect candidate under public working blocked"),
        ("Bash", {"command": "cp .working/DONE.md /tmp/DONE.md"}, m, False, "cp working SOURCE (copy-out) allowed"),
        ("Bash", {"command": "mv .working/DONE.md /tmp/DONE.md"}, m, False, "mv working SOURCE allowed"),
        ("Bash", {"command": "cp a.md /tmp/b.md"}, m, False, "cp no-working not blocked"),
        ("Bash", {"command": "rsync .working/DONE.md /tmp/DONE.md"}, m, False, "rsync working SOURCE allowed"),
        ("Bash", {"command": f"echo x 2> {m}/.working/err.log"}, m, True, "fd-redirect (2>) candidate under public working blocked"),
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
    # nonmatching origin URL, with neither store directory present -> allow
    a = mk_repo("https://github.com/someuser/grc_library.git", False)
    for tn, ti, label in [("Write", {"file_path": ".working/DONE.md"}, "adopter Write"), ("Bash", {"command": "echo x > .working/x"}, "adopter Bash")]:
        if decide(tn, ti, a):
            failures.append(f"  adopter must not be blocked: {label}")
    # matching origin URL, but no primary store or legacy sibling .working -> allow
    mnp = mk_repo("https://github.com/jposluns/grc_library.git", False)
    if decide("Write", {"file_path": ".working/DONE.md"}, mnp):
        failures.append("  matching origin without a primary store or grc_library_private/.working must allow")
    # matching origin + default primary store, without legacy sibling .working -> block
    mstore = mk_repo("https://github.com/jposluns/grc_library.git", False, with_store=True)
    if not decide("Write", {"file_path": ".working/DONE.md"}, mstore):
        failures.append("  matching origin with primary store but no legacy sibling .working must block the public .working path")
    # GRC_STORE EXTERNAL (outside the repo) -> usable -> block
    mext = mk_repo("https://github.com/jposluns/grc_library.git", False)
    ext_store = tempfile.mkdtemp()  # a real dir OUTSIDE the temp repo
    os.environ["GRC_STORE"] = ext_store
    if not decide("Write", {"file_path": ".working/DONE.md"}, mext):
        failures.append("  external GRC_STORE (outside repo) must block public .working write")
    # GRC_STORE IN-REPO -> rejected (matches _store_dir) -> inactive (allow, no other store/.working)
    minr = mk_repo("https://github.com/jposluns/grc_library.git", False)
    (Path(minr) / "private").mkdir(parents=True, exist_ok=True)
    os.environ["GRC_STORE"] = str(Path(minr) / "private")
    if decide("Write", {"file_path": ".working/DONE.md"}, minr):
        failures.append("  in-repo GRC_STORE must be REJECTED (guard inactive, mirrors _store_dir outside-repo rule)")
    # RELATIVE GRC_STORE resolves against the REPO ROOT, not the process CWD. DISCRIMINATING reality
    # fixture (a hostile <cwd>/private would make a CWD-relative impl falsely usable): with GRC_STORE=private,
    # an EXTERNAL <cwd>/private present AND an in-repo <repo>/private present, the guard must REJECT
    # (repo-root resolution -> <repo>/private is in-repo). A CWD-relative regression would BLOCK and fail here.
    mrel = mk_repo("https://github.com/jposluns/grc_library.git", False)
    (Path(mrel) / "private").mkdir(parents=True, exist_ok=True)          # <repo>/private (in-repo)
    hostile = tempfile.mkdtemp(); (Path(hostile) / "private").mkdir()    # <cwd>/private (external)
    _cwd = os.getcwd()
    try:
        os.chdir(hostile)
        os.environ["GRC_STORE"] = "private"  # relative; CWD-relative would resolve to the external hostile/private
        if decide("Write", {"file_path": ".working/DONE.md"}, mrel):
            failures.append("  relative GRC_STORE with a HOSTILE <cwd>/private must still be REJECTED (repo-root resolution, not CWD)")
    finally:
        os.chdir(_cwd)
        os.environ.pop("GRC_STORE", None)
    if _prev_store is not None:
        os.environ["GRC_STORE"] = _prev_store
    if failures:
        print("SELF-TEST FAILED:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"OK: block-public-working-write self-test passed ({len(cases)+7} cases).")
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
