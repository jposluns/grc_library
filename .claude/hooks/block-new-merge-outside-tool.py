#!/usr/bin/env python3
"""PreToolUse hook: refuse a grc_library_new merge outside the merge tool (3b882 part 4).

The only sanctioned path for a grc_library_new squash merge is
``python3 tools/merge-grc-library-new.py <PR number> [--dry-run]``, which checks the
/validate-pr and /retro rows, the title, the head's CI and the merge commit itself.

Registered in .claude/settings.json twice: matcher Bash, and matcher
mcp__github__merge_pull_request (decision D4).

Rule (plan 3b882m section 4):
  1. Allow when the raw Bash command fully matches the sanctioned pattern, ASCII only.
  2. Otherwise exit 2 when (a) the normalized text, or the payload cwd, names
     grc_library_new and (b) the normalized text matches one of the merge patterns.
  3. Every other input exits 0.

The normalized text is NFKC, percent-decoded, NFKC again and casefolded. For Bash it is
the command; for any other tool it is the tool name with the input's owner and repo,
then owner and repo joined by a slash, so the text also carries owner/repo. A
payload that is not a JSON object is checked on its raw text. The hook reads no store,
no network and no file, and parses no shell syntax: it matches text only, so it accepts
over-refusal (a commit message, grep, echo or heredoc body that names both).
"""
import json
import re
import sys
import unicodedata
from urllib.parse import unquote

NEW = "grc_library_new"
SANCTIONED = re.compile(r"python3 tools/merge-grc-library-new\.py [1-9][0-9]{0,5}( --dry-run)?",
                        re.ASCII)
MERGE_PATTERNS = tuple(re.compile(p, re.DOTALL) for p in (
    r"\bpr\b.*\bmerge\b",
    r"pulls/[^\s]*/merge",
    r"mergepullrequest",
    r"merge_pull_request",
    r"merge-when-green",
    # 3b882 fix round 4: an auto-merge, a branch merge and a REST branch-merge call.
    r"enablepullrequestautomerge",
    r"mergebranch",
    r"repos/[^/\s]+/[^/\s]+/merges\b",
))

REASON = (
    "BLOCKED (new-merge-outside-tool): this call would merge a grc_library_new pull request "
    "outside its merge tool.\n"
    "WHY: a grc_library_new squash merge goes only through "
    "python3 tools/merge-grc-library-new.py, which checks the /validate-pr and /retro rows, "
    "the title, the head's CI and the merge commit. This hook matches text only and accepts "
    "over-refusal: any command that names grc_library_new, or runs from a grc_library_new "
    "clone, and mentions a pull-request merge, an auto-merge (GraphQL "
    "enablePullRequestAutoMerge), a branch merge (GraphQL mergeBranch) or a REST "
    "repos/<owner>/<repo>/merges call is refused, including commit messages, greps, "
    "echo and heredoc bodies. Residual not closed by this hook: commands built at runtime "
    "(command substitution, variables, base64, a script file run later, a Python subprocess "
    "call); shell quoting, backslash escapes or brace expansion that split a word (p and r "
    "split by empty quotes, a backslash inside merge, or a brace list inside the repository "
    "name); gh aliases that hide pr merge; a merge run from a grc_library_new clone when the "
    "payload cwd is elsewhere and the text names neither; "
    "merges whose text never names grc_library_new (a GraphQL "
    "mergePullRequest by node id, an enablePullRequestAutoMerge or mergeBranch mutation by "
    "node id, a REST repositories/<id>/pulls/N/merge or repositories/<id>/merges call, or gh pr "
    "merge N from a grc_library_new clone under another directory name or from a clone "
    "where gh repo set-default points at grc_library_new); a merge queue entry (GraphQL "
    "enqueuePullRequest), even one that names grc_library_new; GitHub completing an "
    "auto-merge enabled earlier (from the web UI or before this hook); "
    "MCP merge tools under other names; "
    "merges from the web UI, from other machines or from other accounts; and "
    "direct pushes to main.\n"
    "CONSIDER INSTEAD: run python3 tools/merge-grc-library-new.py <PR number> (add --dry-run "
    "to check first); if this command only mentions a merge, reword it so it does not name "
    "both grc_library_new and a merge."
)


def normalize(text):
    first = unicodedata.normalize("NFKC", text)
    return unicodedata.normalize("NFKC", unquote(first)).casefold()


def merge_text(text):
    return any(p.search(text) for p in MERGE_PATTERNS)


def decide(raw):
    """Return True when the payload text must be refused."""
    try:
        payload = json.loads(raw)
    except ValueError:
        payload = None
    if not isinstance(payload, dict):
        text = normalize(raw)
        return NEW in text and merge_text(text)
    tool = payload.get("tool_name")
    tool = tool if isinstance(tool, str) else ""
    tool_input = payload.get("tool_input")
    tool_input = tool_input if isinstance(tool_input, dict) else {}
    cwd = payload.get("cwd")
    cwd = normalize(cwd) if isinstance(cwd, str) else ""
    if tool == "Bash":
        command = tool_input.get("command")
        if not isinstance(command, str):
            return False
        if SANCTIONED.fullmatch(command):
            return False
        text = normalize(command)
    else:
        parts = [tool] + [tool_input.get(k) for k in ("owner", "repo")]
        text = normalize(" ".join(p if isinstance(p, str) else "" for p in parts))
        text = text + " " + normalize("/".join(
            tool_input.get(k) if isinstance(tool_input.get(k), str) else ""
            for k in ("owner", "repo")))
    return (NEW in text or NEW in cwd) and merge_text(text)


def main():
    stream = getattr(sys.stdin, "buffer", None)
    data = stream.read() if stream is not None else sys.stdin.read()
    raw = data.decode("utf-8", "replace") if isinstance(data, bytes) else data
    if decide(raw):
        reason = REASON
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
