#!/usr/bin/env python3
"""Read-only held-branch expiry report for manual use at session start.

WHY THIS EXISTS. A lapsed hold or a name that matches no local branch protects
nothing. This report makes those entries visible before the turn-end guard.
Nothing runs the report automatically; the test suite runs --self-test. It
uses the standard library and the
repository's lint_common helper.

The copied predicate is parity-tested against the unchanged held_branches().
Only the first token after '#' is considered. A non-comment line whose token
is not a date is MALFORMED because the hook does not treat it as a hold; a file
with such lines never exits 0 until they are removed, commented out or corrected.
The hook accepts date-shaped impossible dates lexically; this report flags
those too.

Expiry uses UTC dates: LAPSED (<0 days), DUE (0 through --days inclusive), OK,
or MALFORMED. A valid date beyond the configured due window reports OK.
The header also gives the hook's local date: the hook lapses a hold by that
date. --today overrides both clocks. Entries are reported per line, including
duplicates: entry-live copies the hook's per-line predicate; branch-held is
yes if ANY line holds that name. These fields describe the held-name record;
presence distinguishes whole short names from split fragments and names
belonging to a different branch.
A byte-order mark stays part of the name, just as it does in the hook.

Presence uses one git enumeration pairing full names with short names using NUL.
Git forbids NUL and LF in ref names; LF separates listing records. The hook's
view is the short-name output split on any whitespace. The report refuses to
judge presence if any non-empty stdout line is not exactly a full branch ref,
NUL and one of its short-name forms: the branch name, heads/<name>, or the full
ref name. This includes trace output from git configuration.
LOCAL means the entry is a whole short name in a clean listing and, if a
branch literally named by the entry exists, the entry's name matches it. The
hook applies the hold only while the entry is live (entry-live) and when its
own listing shows the same name (see the limits below).
GONE means no whole short name applies this hold to the named branch; the
branch may be deleted, may be a ref git cannot list, or may have a name the
hook's whitespace split breaks apart.
SHADOWED means git lists the entry's exact refs/heads/<name> paired with a
different short name, even if the entry matches another branch or a fragment.
Such rows name, as hook-exempts, any different branch whose whole short name
matches the entry. The hook exempts that branch only while an entry of this
name is live (this entry or a duplicate), and never when the name contains
whitespace that the hook's split breaks. A GONE row can carry hook-exempts too.
Fragment matches identify the split short names they came from. The report prints
required-name only if that paired name is exactly one token after the hook's
whitespace split; otherwise it explains that no hold name can match this branch
because the hook splits its name, and prints the tokens the hook sees.
UNKNOWN means presence cannot be judged.
A nonzero git exit, timeout, missing git, or a fatal: or error: diagnostic makes
all entries UNKNOWN, and exits 2 even for an existing empty held-branches file.
Only these C-locale warning shapes mark the named entry UNKNOWN:
warning: ignoring broken ref refs/heads/<name>
warning: ignoring ref with broken name refs/heads/<name>
The ref must match through the end of the diagnostic line. Other warnings do
not change presence. Successfully decoded git diagnostics, including captured timeout stderr,
are retained on stderr; when subprocess decoding fails, only the decoding error
is available. A decoding failure or unclean listing also makes all presence UNKNOWN and
exits 2, including for an existing empty held-branches file.
Entry names are compared as strings and never used as paths. For branch enumeration, the tool opens,
stats and lists nothing under the git directory; it asks git only.
Ref listing does not prove object integrity.

Exit 0: no reported entry needs expiry or presence attention (including a
missing file); LOCAL describes the clean listing, subject to the limits below.
Exit 0 says nothing about branches that no entry names.
Exit 1: an entry is lapsed, due, malformed, GONE or SHADOWED.
Exit 2: the file, the store or git could not be read, presence is UNKNOWN,
report output could not be encoded, or an argument is invalid.
Expiry and presence are independent labelled fields. --quiet keeps entries
with expiry other than OK or presence other than LOCAL. Its header prints only
with rows or differing dates. The final summary counts all entries, including
duplicates and rows suppressed by --quiet, for each state that occurred.

Store resolution is strict: this tool refuses where the hook's resolver falls
through to another location. Git has one five-second timeout on enumeration.
The report removes inherited GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE and GIT_TRACE*
and LANGUAGE, sets LC_ALL=C, and explicitly decodes git output as UTF-8. The hook does not scrub its
environment, so an inherited GIT_DIR can make them read different repositories.
The hook also locates the held-branches file from its own environment: started
with a different GRC_STORE (observed), it read no file where the report read one.
Inherited GIT_TRACE output to stdout can add tokens to the hook's view, so
the report can say GONE for a token that appears there.
Trace output can also interrupt a listing record: the hook then loses the
branch's token while the report can say LOCAL and exit 0 for that entry.
The hook decodes git output using the interpreter's locale encoding; the
report uses UTF-8, so their decoding can differ: one can fail where the other
succeeds (observed, next sentence), and under a non-UTF-8 locale other than C
the hook may read a non-ASCII name as different text (not observed: the test
host has no such locale).
With LC_ALL=C, PYTHONUTF8=0 and PYTHONCOERCECLOCALE=0, and the hook started
without -I, a UTF-8 branch name with a non-ASCII letter raised
UnicodeDecodeError in the hook's listing and its main() returned 0; the
report decoded the listing successfully (with an ASCII stdout it then exits 2
when it prints the row). The configured launcher starts the
hook with python3 -I, which ignores those two PYTHON variables: started that
way under LC_ALL=C (observed on Python 3.14), the hook decoded the listing as
UTF-8.
These are listing and environment limits, not a prediction of whether the
hook will block a turn.
--self-test writes temporary fixtures; the report path never writes.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path

from lint_common import resolve_working, resolve_working_for_write

REPO = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[1])
EXPIRY = re.compile(r"\d{4}-\d{2}-\d{2}")
GIT_TIMEOUT = 5
Entry = tuple[str, str | None, str]


def parse_line(line: str) -> Entry | None:
    """Return branch, first date-shaped token, reason; skip comments and blanks."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    name, _, rest = line.partition("#")
    parts = rest.strip().split(None, 1)
    expiry = parts[0] if parts and EXPIRY.fullmatch(parts[0]) else None
    return name.strip(), expiry, parts[1] if len(parts) > 1 else "no reason recorded"


def hook_held(entry: Entry, today: dt.date) -> bool:
    """Copied lexical predicate, including the hook's acceptance of invalid dates."""
    return entry[1] is not None and entry[1] >= today.isoformat()


def classify(expiry: str | None, today: dt.date, days: int) -> tuple[str, int | None]:
    if expiry is None:
        return "MALFORMED", None
    try:
        remaining = (dt.date.fromisoformat(expiry) - today).days
    except ValueError:
        return "MALFORMED", None
    if remaining < 0:
        return "LAPSED", remaining
    if remaining <= days:
        return "DUE", remaining
    return "OK", remaining


class BranchStatuses(dict[str, tuple[str, str | None]]):
    def __init__(self) -> None:
        super().__init__()
        self.exempted: dict[str, list[str]] = {}
        self.fragments: dict[str, list[str]] = {}


def branch_statuses(repo: Path, branches: set[str]) -> BranchStatuses | None:
    """Return paired-listing presence, or None if git cannot judge the whole run."""
    environment = {key: value for key, value in os.environ.items()
                   if key not in {"GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "LANGUAGE"}
                   and not key.startswith("GIT_TRACE")}
    environment["LC_ALL"] = "C"
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "for-each-ref",
             "--format=%(refname)%00%(refname:short)", "refs/heads"],
            capture_output=True, encoding="utf-8", env=environment,
            timeout=GIT_TIMEOUT, check=False,
        )
    except (OSError, subprocess.TimeoutExpired, UnicodeError) as exc:
        if isinstance(exc, subprocess.TimeoutExpired) and exc.stderr:
            diagnostic = exc.stderr
            if isinstance(diagnostic, bytes):
                diagnostic = diagnostic.decode("utf-8", errors="replace")
            print(diagnostic, end="" if diagnostic.endswith("\n") else "\n", file=sys.stderr)
        print(f"audit-held-branch-expiry: git enumeration failed: {exc}", file=sys.stderr)
        return None
    if result.stderr:
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n", file=sys.stderr)
    diagnostics = result.stderr.split("\n")
    if result.returncode != 0 or any(line.startswith(("fatal:", "error:"))
                                     for line in diagnostics):
        if not result.stderr:
            print(f"audit-held-branch-expiry: git exited {result.returncode}", file=sys.stderr)
        return None
    uncertain = {match.group(1) for line in diagnostics
                 if (match := re.fullmatch(
                     r"warning: ignoring (?:broken ref|ref with broken name) refs/heads/(.*)",
                     line)) is not None}
    # NUL separates each full/short pair; only LF separates records.
    # Ref names cannot contain either byte; Unicode separators remain names.
    full_names = {}
    short_names = []
    for line in result.stdout.split("\n"):
        if not line:
            continue
        full, _, short = line.partition("\x00")
        name = full.removeprefix("refs/heads/")
        if (not full.startswith("refs/heads/") or not name
                or short not in {name, "heads/" + name, full}):
            print("audit-held-branch-expiry: git wrote something other than the branch "
                  "listing to stdout (for example trace output); presence was not judged.",
                  file=sys.stderr)
            return None
        full_names[full] = short
        short_names.append(short)
    # The hook uses str.split(), including Unicode whitespace within names.
    names = set("\n".join(short_names).split())
    statuses = BranchStatuses()
    whole_names = set(short_names)
    for branch in branches:
        needed = full_names.get("refs/heads/" + branch)
        if branch in uncertain:
            statuses[branch] = ("UNKNOWN", None)
        elif needed is not None and needed != branch:
            statuses[branch] = ("SHADOWED", needed)
        elif branch in names and branch in whole_names:
            statuses[branch] = ("LOCAL", None)
        else:
            statuses[branch] = ("GONE", None)
        if statuses[branch][0] in {"GONE", "SHADOWED"}:
            statuses.exempted[branch] = [full.removeprefix("refs/heads/")
                                        for full, short in full_names.items()
                                        if short == branch and full != "refs/heads/" + branch]
            statuses.fragments[branch] = [short for short in short_names
                                          if short != branch and branch in short.split()]
    return statuses


def report(path: Path, repo: Path, today: dt.date, local_today: dt.date,
           days: int = 5, quiet: bool = False) -> int:
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"audit-held-branch-expiry: no held-branches file was found at {path}")
        return 0
    except (OSError, UnicodeError) as exc:
        print(f"audit-held-branch-expiry: cannot read {path}: {exc}", file=sys.stderr)
        return 2
    entries = [entry for line in content.splitlines()
               if (entry := parse_line(line)) is not None]
    held_branches = {entry[0] for entry in entries if hook_held(entry, local_today)}
    presences = branch_statuses(repo, {entry[0] for entry in entries})
    status = 2 if presences is None else 0
    if presences is None:
        presences = BranchStatuses()
        presences.update({entry[0]: ("UNKNOWN", None) for entry in entries})
    rows = []
    expiry_counts: dict[str, int] = {}
    presence_counts: dict[str, int] = {}
    for entry in entries:
        branch, expiry, _ = entry
        state, remaining = classify(expiry, today, days)
        presence, needed = presences[branch]
        expiry_counts[state] = expiry_counts.get(state, 0) + 1
        presence_counts[presence] = presence_counts.get(presence, 0) + 1
        if state != "OK" or presence in {"GONE", "SHADOWED"}:
            status = max(status, 1)
        if presence == "UNKNOWN":
            status = 2
        if not quiet or state != "OK" or presence != "LOCAL":
            held = "yes" if hook_held(entry, local_today) else "no"
            rows.append(f"{branch!r} expiry={expiry or '-'} "
                        f"days={remaining if remaining is not None else '-'} "
                        f"expiry-state={state} branch-presence={presence} entry-live={held} "
                        f"branch-held={'yes' if branch in held_branches else 'no'}"
                        + (f" required-name={needed!r}" if needed is not None
                           and needed.split() == [needed] else
                           " no hold name can match this branch because the hook splits its name;"
                           f" hook-tokens={needed.split()!r}" if needed is not None else "")
                        + (f" hook-exempts={presences.exempted[branch]!r}"
                           if presences.exempted.get(branch) else "")
                        + (f" hook-token-fragment-of={presences.fragments[branch]!r}"
                           if presences.fragments.get(branch) else ""))
    if not quiet or rows or today != local_today:
        print(f"report-date-utc={today.isoformat()} hook-date-local={local_today.isoformat()}")
        if today != local_today:
            print("The hook lapses a hold by the local date.")
    for row in rows:
        print(row)
    counts = [f"expiry-state:{state}={expiry_counts[state]}"
              for state in ("LAPSED", "DUE", "OK", "MALFORMED") if state in expiry_counts]
    counts += [f"branch-presence:{presence}={presence_counts[presence]}"
               for presence in ("LOCAL", "GONE", "SHADOWED", "UNKNOWN")
               if presence in presence_counts]
    print("summary" + (" " + " ".join(counts) if counts else " entries=0"))
    return status


def iso_date(value: str) -> dt.date:
    try:
        if not EXPIRY.fullmatch(value):
            raise ValueError
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a calendar date YYYY-MM-DD") from exc


def nonnegative(value: str) -> int:
    try:
        days = int(value)
        if days < 0:
            raise ValueError
        return days
    except ValueError as exc:
        raise argparse.ArgumentTypeError("--days must be a nonnegative integer") from exc


def self_test() -> int:
    import contextlib
    import io
    import tempfile
    from unittest import mock

    checks = []
    today = dt.date(2026, 10, 12)

    def check(name: str, got: object, want: object) -> None:
        ok = got == want
        checks.append(ok)
        print(f"  {'PASS' if ok else 'FAIL'}: {name}" +
              ("" if ok else f" -> {got!r}, expected {want!r}"))

    for token, want in [
        ("2026-10-11", ("LAPSED", -1)), ("2026-10-12", ("DUE", 0)),
        ("2026-10-16", ("DUE", 4)), ("2026-10-17", ("DUE", 5)),
        ("2026-10-18", ("OK", 6)), (None, ("MALFORMED", None)),
        ("2026-99-99", ("MALFORMED", None)),
    ]:
        check(str(token), classify(token, today, 5), want)
    check("comment", parse_line(" # comment"), None)
    check("blank", parse_line(" \t"), None)
    check("expiry before event", parse_line(
        "tooling/example-one  # 2026-10-22 (re-triaged 2026-09-22: decision pending) HELD pending design decision"
    )[1], "2026-10-22")
    check("event is not expiry", parse_line(
        "claude/example-two  # ROUTED-to-guardrails 2026-09-04 (seed 20260904T212707Z); not merging"
    )[1], None)
    check("lexical hook residue", hook_held(parse_line("b # 2026-99-99"), today), True)
    def _self_test_statuses(names: set[str]) -> BranchStatuses:
        statuses = BranchStatuses()
        statuses.update({name: ("GONE", None) for name in names})
        return statuses

    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "held-branches.txt"
        with contextlib.redirect_stdout(io.StringIO()):
            missing = report(path, Path(td), today, today)
        check("missing", missing, 0)
        path.mkdir()
        with contextlib.redirect_stderr(io.StringIO()):
            unreadable = report(path, Path(td), today, today)
        check("unreadable existing input", unreadable, 2)
        path.rmdir()
        path.write_text("b # 2026-10-11 reason\n", encoding="utf-8")
        original = path.read_bytes()
        with mock.patch.object(sys.modules[__name__], "branch_statuses",
                               side_effect=lambda repo, names: _self_test_statuses(names)):
            with contextlib.redirect_stdout(io.StringIO()) as out:
                rc = report(path, Path(td), today, today)
        check("report alerts", rc, 1)
        check("report fields", "days=-1 expiry-state=LAPSED branch-presence=GONE entry-live=no branch-held=no" in out.getvalue(), True)
        check("read-only", path.read_bytes(), original)
    print(f"self-test: {sum(checks)}/{len(checks)} passed")
    return 0 if all(checks) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=nonnegative, default=5, help="due window, inclusive (default 5)")
    ap.add_argument("--today", type=iso_date, help="override both dates with YYYY-MM-DD")
    ap.add_argument("--quiet", action="store_true", help="print entries needing expiry or branch attention")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    today = args.today or dt.datetime.now(dt.timezone.utc).date()
    local_today = args.today or dt.date.today()
    try:
        # Same resolver and precedence as the hook; strict mode fails closed on
        # inaccessible candidates instead of falling through to an older store.
        path = resolve_working("held-branches.txt", repo_root=REPO, strict=True)
        missing = path is None
        if missing:
            # This helper only computes a path. It creates no file or directory.
            path = resolve_working_for_write("held-branches.txt", repo_root=REPO)
    except (OSError, UnicodeError) as exc:
        print(f"audit-held-branch-expiry: cannot resolve held-branches.txt: {exc}",
              file=sys.stderr)
        return 2
    try:
        if missing:
            print(f"audit-held-branch-expiry: no held-branches file was found at {path}")
            return 0
        return report(path, REPO, today, local_today, args.days, args.quiet)
    except UnicodeError as exc:
        print(f"audit-held-branch-expiry: cannot encode report output: {exc}",
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
