"""Tests for tools/merge-grc-library-new.py, part P2a of the 3b882 merge-tool plan: the merge
argv (T3), the read-back of the merged commit (T4), the admin-merge log row printed to standard
output (T5), the title suffix (T6, decision D3) and the CI check on the pinned head (decision D5);
part P2b: both required workflows (D5), the log-row cell escaping (T5) and the open-findings check
reused from merge-when-green.py (plan section 3); part P2c: the admin-merge log pre-flight before any
gh call, the row appended to the log and read back, and the open-findings check failing closed;
part P2d: the pre-flight reads the log's real shape (text before the header, the header as the
first table line, a table line last) and refuses a log it could not append to.

Every gh call is stubbed through the tool's gh() seam, so nothing contacts a network, and every
test points GRC_STORE at a temporary directory, so none reads the operational store.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import re
import shlex
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "tools" / "merge-grc-library-new.py"
REPO = "jposluns/grc_library_new"
HEAD = "af9f9882" + "0123456789abcdef0123456789abcdef"
OID = "cef8d20e" + "c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6"
TITLE = "content: a grc_library_new change (CalVer 2026.11.69, README 1.11.919)"
SUBJECT = TITLE + " (#31)"
BODY = f"Squash merge of #31 at {HEAD[:12]}."
VALIDATE_ROW = "| 2026-11-14 | #31 [repo: grc_library_new] | train 1 | claude | IDS | done |"
RETRO_ROW = "| 2026-11-14 | #31 (/retro) [NEW31-RETRO] [repo: grc_library_new] | t | a | b | c |"
HEADER = "| Date (UTC) | PR | CI state at merge | Mechanism | Justification | Change |"
NOW = datetime(2026, 11, 15, 14, 0, tzinfo=timezone.utc)
MERGE_ARGV = ["pr", "merge", "31", "--repo", REPO, "--squash", "--subject", SUBJECT,
              "--body", BODY, "--match-head-commit", HEAD, "--admin"]
QUALITY = "Repository quality checks"
ATTRIBUTION = "Pull request attribution"
LEDGER_HEAD = ("## Open\n| Date | Severity | Finding | Source | Disposition |\n"
               "| --- | --- | --- | --- | --- |\n")
OPEN_ERROR = "| 2026-11-15 | error | a live defect | probe |  |\n"
FIXED_ERROR = "| 2026-11-15 | error | a fixed defect | probe | FIXED #1 |\n"
LOG_REL = "merge-bypass-log.md"
HOOK_NAME = "block-on-open-findings.py"
OLD_LOG_ROW = "| 2026-09-20 | #2408 | green | admin squash | review | content |"
# Part 2d: the true shape of the admin-merge log (texts/log-shape.md): a title, a licence line,
# prose and a list before the table, the header with no separator row, then data rows, ending
# with a data row and a newline.
LOG_SHAPE = (
    "# Merge-bypass log\n"
    "\n"
    "**License:** CC BY-SA 4.0\n"
    "\n"
    "Every merge since this log was created that used the admin merge path on a protected "
    "branch, one row each. (A synthetic stand-in for the real preamble, which runs about 30 "
    "lines of prose, lists and blank lines before the table.)\n"
    "\n"
    "- a list item in the preamble\n"
    "\n"
    + HEADER + "\n"
    "| 2026-09-20 | #2408 | Repository quality checks completed/success | admin squash "
    "(merge-when-green.py --admin) | branch protection | example change |\n"
    "| 2026-11-14 | #3132 | Repository quality checks completed/success | admin squash "
    "(merge-when-green.py --admin) | branch protection | example change |\n"
)


def gfm_cells(row):
    """The cells of a table row split close to GFM: only an unescaped pipe separates cells (a
    backslash-backslash pair escapes itself).

    This over-approximates GFM: GFM's backslash escape applies only before ASCII punctuation,
    while this helper treats a backslash as escaping any character after it. The two differ
    only when that character is not ASCII punctuation, so it is never a pipe or a backslash,
    and the split is the same (3b882 fix round 9)."""
    cells, cur, i = [], "", 0
    while i < len(row):
        if row[i] == "\\" and i + 1 < len(row):
            cur += row[i:i + 2]
            i += 2
            continue
        if row[i] == "|":
            cells.append(cur)
            cur = ""
        else:
            cur += row[i]
        i += 1
    cells.append(cur)
    return cells[1:-1]


def load_tool():
    spec = importlib.util.spec_from_file_location("_merge_grc_library_new_p2a", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Decision D5: each required workflow is bound to its own file, as gh api lists them for
# grc_library_new, and counts only from a pull_request run.
WORKFLOW_PATHS = {"Repository quality checks": ".github/workflows/quality.yml",
                  "Pull request attribution": ".github/workflows/pr-attribution.yml"}


def run(name, conclusion="success", status="completed", sha=HEAD, run_id=43583397326,
        created="2026-11-14T10:30:00Z", path=None, event="pull_request"):
    if path is None:
        path = WORKFLOW_PATHS.get(name, ".github/workflows/other.yml")
    return {"id": run_id, "name": name, "head_sha": sha, "status": status,
            "conclusion": conclusion, "created_at": created, "path": path, "event": event}


class FakeGh:
    """A stand-in for the tool's gh(): answers by call shape and records every call."""

    def __init__(self, **over):
        self.calls = []
        self.view = {"number": 31, "title": TITLE, "state": "OPEN", "headRefOid": HEAD,
                     "baseRefName": "main", "url": f"https://github.com/{REPO}/pull/31"}
        self.view.update(over.pop("view", {}))
        runs = over.pop("runs", [run(QUALITY), run(ATTRIBUTION, run_id=43583397345)])
        self.runs = over.pop("runs_text", json.dumps({"total_count": len(runs), "workflow_runs": runs}))
        self.runs_error = over.pop("runs_error", None)
        self.pages = over.pop("pages", None)
        self.merged = over.pop("merged", [{"state": "MERGED", "mergeCommit": {"oid": OID}}])
        self.message = over.pop("message", SUBJECT + "\n\n" + BODY)
        self.parents = over.pop("parents", [{"sha": "d" * 40}])
        self.merge_error = over.pop("merge_error", None)
        assert not over, over

    def __call__(self, *args):
        args = list(args)
        self.calls.append(args)
        if args[:2] == ["pr", "view"] and "headRefOid" in args[-1]:
            return json.dumps(self.view)
        if args[:2] == ["pr", "view"]:
            index = min(sum(1 for c in self.calls if c[:2] == ["pr", "view"]
                            and "mergeCommit" in c[-1]) - 1, len(self.merged) - 1)
            return json.dumps(self.merged[index])
        if args[:2] == ["pr", "merge"]:
            if self.merge_error:
                raise self.merge_error
            return ""
        if args[0] == "api" and "/actions/runs" in args[1]:
            if self.runs_error:
                raise self.runs_error
            if self.pages is not None:
                found = re.search(r"[?&]page=([0-9]+)(?:&|$)", args[1])
                index = int(found.group(1)) - 1 if found else 0
                if not 0 <= index < len(self.pages):
                    raise AssertionError(f"unexpected runs page {args[1]}")
                return self.pages[index]
            return self.runs
        if args[0] == "api" and "/commits/" in args[1]:
            return json.dumps({"sha": OID, "commit": {"message": self.message},
                               "parents": self.parents})
        raise AssertionError(f"unexpected gh call {args}")

    def merge_calls(self):
        return [c for c in self.calls if c[:2] == ["pr", "merge"]]


class MergeGrcLibraryNewMergeTests(unittest.TestCase):

    def setUp(self):
        self.mod = load_tool()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        parent = Path(self.tmp.name)
        self.root = parent / "repo"
        self.root.mkdir()
        self.store = parent / "store"
        (self.store / "validate-pr").mkdir(parents=True)
        self.write_rows(VALIDATE_ROW, RETRO_ROW)
        self.install_hook()
        (self.store / "open-findings.md").write_text(LEDGER_HEAD, encoding="utf-8")
        self.log = self.store / LOG_REL
        self.log.write_text(LOG_SHAPE, encoding="utf-8")
        patcher = mock.patch.dict(os.environ, {"GRC_STORE": str(self.store)})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.sleeps = []

    def write_rows(self, validate, retro):
        (self.store / "validate-pr" / "history-grc_library_new.md").write_text(
            validate + "\n", encoding="utf-8")
        (self.store / "improvement-log-grc_library_new.md").write_text(retro + "\n", encoding="utf-8")

    def merge(self, fake, dry_run=False):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = self.mod.run_merge(31, root=self.root, gh=fake, dry_run=dry_run,
                                      sleep=self.sleeps.append, now=NOW)
        return code, out.getvalue(), err.getvalue()

    # T3: the merge argv, and no merge call on any refusal or a dry run.

    def test_T3_merge_argv_is_exact(self):
        fake = FakeGh()
        code, out, err = self.merge(fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(fake.merge_calls(), [MERGE_ARGV])

    def test_T3_view_is_pinned_to_the_new_repository(self):
        fake = FakeGh()
        self.merge(fake)
        self.assertEqual(fake.calls[0], ["pr", "view", "31", "--repo", REPO, "--json",
                                         "number,title,state,headRefOid,baseRefName,url"])

    def test_T3_rows_refused_makes_no_gh_call(self):
        self.write_rows(VALIDATE_ROW, "")
        fake = FakeGh()
        code, out, err = self.merge(fake)
        self.assertEqual(code, 1, err)
        self.assertEqual(fake.calls, [])
        self.assertEqual(out, "")

    def test_T3_bad_pr_state_head_base_url_or_number_makes_no_merge_call(self):
        cases = {
            "closed": {"state": "CLOSED"},
            "merged": {"state": "MERGED"},
            "short head": {"headRefOid": HEAD[:12]},
            "upper-case head": {"headRefOid": HEAD.upper()},
            "no head": {"headRefOid": None},
            "base not main": {"baseRefName": "develop"},
            "other repository": {"url": "https://github.com/jposluns/grc_library/pull/31"},
            "other PR url": {"url": f"https://github.com/{REPO}/pull/310"},
            "other number": {"number": 3},
        }
        for name, view in cases.items():
            with self.subTest(case=name):
                fake = FakeGh(view=view)
                code, out, err = self.merge(fake)
                self.assertEqual(code, 1, err)
                self.assertEqual(fake.merge_calls(), [])
                self.assertEqual(out, "")

    def test_T3_unreadable_view_makes_no_merge_call(self):
        def broken(*args):
            raise subprocess.CalledProcessError(1, ["gh", *args], "", "HTTP 401")
        code, out, err = self.merge(broken)
        self.assertEqual(code, 2, err)
        self.assertIn("HTTP 401", err)
        self.assertEqual(out, "")

    def test_T3_dry_run_makes_no_merge_call(self):
        fake = FakeGh()
        code, out, err = self.merge(fake, dry_run=True)
        self.assertEqual(code, 0, err)
        self.assertEqual(fake.merge_calls(), [])
        self.assertIn("DRY RUN", err)
        self.assertEqual(out, "")

    def test_T3_merge_call_error_exits_2_loudly(self):
        fake = FakeGh(merge_error=subprocess.CalledProcessError(1, ["gh"], "", "merge refused"))
        code, out, err = self.merge(fake)
        self.assertEqual(code, 2, err)
        self.assertIn("merge refused", err)
        self.assertEqual(len(fake.merge_calls()), 1)

    # T4: the read-back of the merged commit.

    def test_T4_clean_message_exits_0(self):
        code, out, err = self.merge(FakeGh())
        self.assertEqual(code, 0, err)
        self.assertNotIn("MERGED BUT", err)

    def test_T4_trailers_fail_loud_and_the_row_records_them(self):
        for trailer in ("Co-authored-by: a <b@example.com>", "co-authored-by: a <b@example.com>",
                        "Signed-off-by: a <b@example.com>"):
            with self.subTest(trailer=trailer):
                fake = FakeGh(message=SUBJECT + "\n\n" + BODY + "\n\n" + trailer + "\n")
                code, out, err = self.merge(fake)
                self.assertEqual(code, 3, err)
                self.assertIn("MERGED BUT", err)
                self.assertIn(trailer.split(":")[0], err)
                self.assertEqual(len(out.splitlines()), 1)
                self.assertIn("trailer", out.splitlines()[0])
                self.assertIn(trailer.split(":")[0], out.splitlines()[0])

    def test_T4_message_differs_fails_loud(self):
        for message in ("other subject\n\n" + BODY, SUBJECT + "\n\nother body", SUBJECT):
            with self.subTest(message=message):
                code, out, err = self.merge(FakeGh(message=message))
                self.assertEqual(code, 3, err)
                self.assertIn("MERGED BUT", err)
                self.assertIn("differs", err)
                self.assertEqual(len(out.splitlines()), 1)

    def test_T4_merge_commit_stays_null_after_retries(self):
        fake = FakeGh(merged=[{"state": "OPEN", "mergeCommit": None}])
        code, out, err = self.merge(fake)
        self.assertEqual(code, 3, err)
        self.assertIn("MERGED BUT", err)
        polls = [c for c in fake.calls if c[:2] == ["pr", "view"] and "mergeCommit" in c[-1]]
        self.assertEqual(len(polls), 5)
        self.assertEqual(self.sleeps, [2, 2, 2, 2])
        self.assertEqual(len(out.splitlines()), 1)

    def test_T4_merge_commit_appears_on_a_later_poll(self):
        fake = FakeGh(merged=[{"state": "OPEN", "mergeCommit": None},
                              {"state": "MERGED", "mergeCommit": {"oid": OID}}])
        code, out, err = self.merge(fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(self.sleeps, [2])

    def test_T4_two_parents_fail_loud(self):
        code, out, err = self.merge(FakeGh(parents=[{"sha": "d" * 40}, {"sha": "e" * 40}]))
        self.assertEqual(code, 3, err)
        self.assertIn("parent", err)

    def test_T4_unreadable_commit_fails_loud(self):
        fake = FakeGh()
        real = fake.__call__

        def flaky(*args):
            if args[0] == "api" and "/commits/" in args[1]:
                fake.calls.append(list(args))
                raise subprocess.CalledProcessError(1, ["gh"], "", "HTTP 502")
            return real(*args)
        code, out, err = self.merge(flaky)
        self.assertEqual(code, 3, err)
        self.assertIn("MERGED BUT", err)
        self.assertIn("HTTP 502", err)

    # T5: the admin-merge log row, printed to standard output only.

    def test_T5_header_matches_the_admin_merge_log(self):
        self.assertEqual(self.mod.LOG_HEADER, HEADER)

    def test_T5_one_tagged_row_on_stdout(self):
        code, out, err = self.merge(FakeGh())
        self.assertEqual(code, 0, err)
        lines = out.splitlines()
        self.assertEqual(len(lines), 1, out)
        row = lines[0]
        self.assertTrue(row.startswith("| 2026-11-15 | #31 [repo: grc_library_new] | "), row)
        self.assertTrue(row.endswith(" |"), row)
        cells = re.split(r"(?<!\\)\|", row)[1:-1]
        self.assertEqual(len(cells), len(HEADER.split("|")[1:-1]), row)
        self.assertIn(HEAD, row)
        self.assertIn(OID, row)
        self.assertIn(shlex.join(["gh", *MERGE_ARGV]).replace("|", "\\|"), row)
        self.assertNotIn(row, err)

    def test_T5_row_is_not_a_bare_pr_cell(self):
        # Decision D2: the tagged form, never a bare '#N' that gate 50 Check 6 would read as a
        # grc_library PR.
        code, out, err = self.merge(FakeGh())
        self.assertIsNone(re.match(r"^\|[^|]*\|\s*#(\d+)\s*\|", out.splitlines()[0]))

    def test_T5_pipes_in_the_title_are_escaped(self):
        title = "content: a | b (CalVer 2026.11.69, README 1.11.919)"
        subject = title + " (#31)"
        fake = FakeGh(view={"title": title}, message=subject + "\n\n" + BODY)
        code, out, err = self.merge(fake)
        self.assertEqual(code, 0, err)
        row = out.splitlines()[0]
        self.assertEqual(len(re.split(r"(?<!\\)\|", row)[1:-1]), 6, row)
        self.assertIn("a \\| b", row)
        self.assertEqual(len(gfm_cells(row)), 6, row)

    def test_T5_backslash_before_a_pipe_does_not_split_a_cell(self):
        # A title holding "\|" must not become "\\|" (an escaped backslash, then a bare pipe
        # that GFM reads as a cell boundary); every backslash is escaped as well.
        for title in ("content: a \\| b (CalVer 2026.11.69, README 1.11.919)",
                      "content: a \\\\| b (CalVer 2026.11.69, README 1.11.919)",
                      "content: a \\ b | c \\ (CalVer 2026.11.69, README 1.11.919)"):
            with self.subTest(title=title):
                fake = FakeGh(view={"title": title}, message=title + " (#31)\n\n" + BODY)
                code, out, err = self.merge(fake)
                self.assertEqual(code, 0, err)
                lines = out.splitlines()
                self.assertEqual(len(lines), 1, out)
                cells = gfm_cells(lines[0])
                self.assertEqual(len(cells), 6, lines[0])
                self.assertEqual(cells[1].strip(), "#31 [repo: grc_library_new]")
        fake = FakeGh(view={"title": "content: a \\| b (CalVer 2026.11.69, README 1.11.919)"},
                      message="content: a \\| b (CalVer 2026.11.69, README 1.11.919) (#31)\n\n" + BODY)
        code, out, err = self.merge(fake)
        self.assertIn("a \\\\\\| b", out)

    def test_T5_title_suffix_refuses_line_breaking_characters(self):
        # 3b882 fix round 8 (round 7 agy-B F2): this checks the D3 title suffix refusal of every
        # character str.splitlines() treats as a line boundary, and of other control characters
        # (3b882 fix round 7): such a title is refused before any merge call, so no row is
        # printed. It also checks that _cell turns the same character into a space.
        for char in ("\n", "\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029",
                     "\r", "\x00", "\x1b"):
            with self.subTest(char=repr(char)):
                self.assertEqual(self.mod._cell(f"a{char}b"), "a b")
                title = f"content: a{char}b (CalVer 2026.11.69, README 1.11.919)"
                fake = FakeGh(view={"title": title}, message=title + " (#31)\n\n" + BODY)
                code, out, err = self.merge(fake)
                self.assertEqual(code, 1, err)
                self.assertEqual((out, fake.merge_calls()), ("", []))

    def test_row_present_digit_check_follows_the_whole_lead(self):
        # agy LOW: the digit check sits after the whole lead, #N, or #N (/retro) in the retro
        # register, as row_present's docstring says; this keeps the current refusals.
        v_row, r_row = VALIDATE_ROW, RETRO_ROW
        self.assertTrue(self.mod.row_present(v_row, 31, retro=False))
        self.assertFalse(self.mod.row_present(v_row.replace("#31", "#310"), 31, retro=False))
        self.assertFalse(self.mod.row_present(v_row.replace("#31", "#31\uff13"), 31, retro=False))
        self.assertTrue(self.mod.row_present(r_row, 31, retro=True))
        self.assertFalse(self.mod.row_present(r_row.replace("#31", "#310"), 31, retro=True))
        self.assertFalse(self.mod.row_present(r_row.replace("(/retro)", "(/retro)2026"), 31,
                                              retro=True))

    def snapshot(self):
        # Every entry under the temporary root: a file by its bytes, a symlink by its target, a
        # directory and anything else by its kind, so a created directory shows as a change
        # (3b882 fix round 7); each with its st_mode (lstat, so a symlink's own), so a mode
        # change to any entry shows as a change too (3b882 fix round 9).
        def entry(p):
            mode = p.lstat().st_mode
            if p.is_symlink():
                return ("symlink", str(p.readlink()), mode)
            if p.is_file():
                return ("file", p.read_bytes(), mode)
            return ("dir", mode) if p.is_dir() else ("other", mode)
        return {p: entry(p)
                for p in sorted(Path(self.tmp.name).rglob("*")) if "__pycache__" not in p.parts}

    @staticmethod
    def changed_paths(before, after):
        return sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))

    def test_T5_snapshot_sees_a_created_directory(self):
        # 3b882 fix round 7 (round 6 agy-B F2): a created directory, empty or not, is a change.
        before = self.snapshot()
        created = Path(self.tmp.name) / "created-by-the-tool"
        created.mkdir()
        self.assertEqual(self.changed_paths(before, self.snapshot()), [created])

    def test_T5_snapshot_sees_a_mode_change(self):
        # 3b882 fix round 9 (round 8 agy-B F2): a mode change to an existing file, with its bytes
        # unchanged, is a change.
        before = self.snapshot()
        self.log.chmod(self.log.stat().st_mode ^ 0o100)
        self.assertEqual(self.changed_paths(before, self.snapshot()), [self.log])

    def test_T5_dry_run_writes_no_file_and_the_merge_changes_only_the_log(self):
        before = self.snapshot()
        code, out, err = self.merge(FakeGh(), dry_run=True)
        self.assertEqual(code, 0, err)
        self.assertEqual(self.snapshot(), before)
        code, out, err = self.merge(FakeGh())
        self.assertEqual(code, 0, err)
        self.assertEqual(self.changed_paths(before, self.snapshot()), [self.log])

    def test_T5_no_row_without_a_merge(self):
        for fake in (FakeGh(view={"title": "no suffix"}),
                     FakeGh(runs=[run("Repository quality checks", conclusion="failure")])):
            code, out, err = self.merge(fake)
            self.assertEqual(code, 1, err)
            self.assertEqual(out, "")

    # T6: decision D3, the (CalVer ..., README ...) title suffix.

    def test_T6_title_without_suffix_refused_before_merge(self):
        for title in ("content: no suffix",
                      "content: x (CalVer 2026.11.69)",
                      "content: x (CalVer 2026.11.69, README 1.11.919) trailing",
                      "content: x (CalVer 2026.11.69,README 1.11.919)",
                      "content: x (CalVer ２０２６.11.69, README 1.11.919)",
                      "content: x (calver 2026.11.69, readme 1.11.919)"):
            with self.subTest(title=title):
                fake = FakeGh(view={"title": title})
                code, out, err = self.merge(fake)
                self.assertEqual(code, 1, err)
                self.assertIn("CalVer", err)
                self.assertEqual(fake.merge_calls(), [])

    def test_T6_title_with_a_control_or_line_breaking_character_refused_before_merge(self):
        # 3b882 fix round 7 (round 6 agy-B F1): the suffix check refused a newline only; a
        # carriage return, vertical tab or any other control or line-breaking character is
        # refused too, anywhere in the title.
        for char in ("\r", "\r\n", "\v", "\f", "\t", "\x00", "\x1b", "\x1c", "\x1d", "\x1e",
                     "\x7f", "\x85", "\x9b", "\u2028", "\u2029"):
            for title in (f"content: a{char}b (CalVer 2026.11.69, README 1.11.919)",
                          f"content: ab (CalVer 2026.11.69, README 1.11.919){char}"):
                with self.subTest(title=repr(title)):
                    self.assertFalse(self.mod.title_has_suffix(title))
                    fake = FakeGh(view={"title": title})
                    code, out, err = self.merge(fake)
                    self.assertEqual(code, 1, err)
                    self.assertIn("CalVer", err)
                    self.assertEqual((out, fake.merge_calls()), ("", []))

    # 3b882 fix round 8 (round 7 claude F1): format characters (Unicode category Cf).
    FORMAT_CHARACTERS = ("\u202e", "\u200b", "\u2066", "\ufeff", "\u00ad", "\u200e", "\u200f",
                         "\u2067", "\u2068", "\u2069", "\u202a", "\u202d", "\u061c", "\u200d")

    def test_T6_title_with_a_format_character_refused_before_merge(self):
        # A bidi override or isolate, a zero-width space or joiner, a byte order mark or a soft
        # hyphen would reach the squash subject and the admin-merge log row unchanged, where it
        # can make them display other than what they hold; the D3 check refuses each one,
        # anywhere in the title.
        import unicodedata
        for char in self.FORMAT_CHARACTERS:
            self.assertEqual(unicodedata.category(char), "Cf", repr(char))
            for title in (f"content: a{char}b (CalVer 2026.11.69, README 1.11.919)",
                          f"{char}content: ab (CalVer 2026.11.69, README 1.11.919)",
                          f"content: ab (CalVer 2026.11.69, README 1.11.919){char}"):
                with self.subTest(char=repr(char), title=repr(title)):
                    self.assertFalse(self.mod.title_has_suffix(title))
                    fake = FakeGh(view={"title": title})
                    code, out, err = self.merge(fake)
                    self.assertEqual(code, 1, err)
                    self.assertIn("format character", err)
                    self.assertEqual((out, fake.merge_calls()), ("", []))

    def test_T5_format_characters_become_spaces_in_a_cell(self):
        # The same characters in any other cell text become a space, so the log row shows what
        # it holds.
        for char in self.FORMAT_CHARACTERS:
            with self.subTest(char=repr(char)):
                self.assertEqual(self.mod._cell(f"a{char}b"), "a b")

    def test_title_has_suffix_docstring_names_format_characters(self):
        doc = " ".join(self.mod.title_has_suffix.__doc__.split())
        self.assertIn("Cc, Zl, Zp or Cf", doc)
        cell = " ".join(self.mod._cell.__doc__.split())
        self.assertIn("format character", cell)

    def test_T6_title_with_suffix_allowed(self):
        for title in (TITLE, "tools: y (CalVer 2026.9.3, README 1.10.4)"):
            with self.subTest(title=title):
                self.assertTrue(self.mod.title_has_suffix(title))

    # D5: every required workflow concluded success on the pinned head.

    def test_D5_required_workflows_from_the_new_repository(self):
        # Both workflow names in texts/required-workflows.txt (3b882 P2b item 1).
        self.assertEqual(self.mod.REQUIRED_WORKFLOWS, (QUALITY, ATTRIBUTION))

    def test_D5_only_one_required_workflow_green_refused_before_merge(self):
        cases = {
            "quality only": ([run(QUALITY)], ATTRIBUTION),
            "attribution only": ([run(ATTRIBUTION, run_id=2)], QUALITY),
            "attribution failed": ([run(QUALITY), run(ATTRIBUTION, conclusion="failure", run_id=2)],
                                   ATTRIBUTION),
            "attribution pending": ([run(QUALITY), run(ATTRIBUTION, status="in_progress",
                                                       conclusion=None, run_id=2)], ATTRIBUTION),
            "quality failed": ([run(QUALITY, conclusion="failure"), run(ATTRIBUTION, run_id=2)],
                               QUALITY),
            "attribution on another head": ([run(QUALITY), run(ATTRIBUTION, sha="b" * 40, run_id=2)],
                                            ATTRIBUTION),
        }
        for name, (runs, culprit) in cases.items():
            with self.subTest(case=name):
                fake = FakeGh(runs=runs)
                code, out, err = self.merge(fake)
                self.assertEqual(code, 1, err)
                self.assertIn(culprit, err)
                self.assertEqual(fake.merge_calls(), [])
                self.assertEqual(out, "")

    def test_D5_row_names_both_green_runs(self):
        code, out, err = self.merge(FakeGh())
        self.assertEqual(code, 0, err)
        self.assertIn(f"{QUALITY} completed/success on {HEAD} (run 43583397326)", out)
        self.assertIn(f"{ATTRIBUTION} completed/success on {HEAD} (run 43583397345)", out)

    def test_D5_runs_read_by_pinned_head(self):
        fake = FakeGh()
        self.merge(fake)
        api = [c for c in fake.calls if c[0] == "api" and "/actions/runs" in c[1]]
        self.assertEqual(api, [["api", f"repos/{REPO}/actions/runs?head_sha={HEAD}&per_page=100&page=1"]])

    def test_D5_two_page_head_read_in_full(self):
        # 3b882 fix round 5 (round 4 agy-A finding 1): a head with more runs than one page holds
        # is read page by page until every run is read, then judged as one list.
        first = [run("Other workflow", run_id=1000 + i) for i in range(99)] + [run(QUALITY, run_id=2000)]
        second = [run(ATTRIBUTION, run_id=2001)]
        fake = FakeGh(pages=[json.dumps({"total_count": 101, "workflow_runs": first}),
                             json.dumps({"total_count": 101, "workflow_runs": second})])
        code, out, err = self.merge(fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(fake.merge_calls(), [MERGE_ARGV])
        api = [c for c in fake.calls if c[0] == "api" and "/actions/runs" in c[1]]
        self.assertEqual(api, [["api", f"repos/{REPO}/actions/runs?head_sha={HEAD}&per_page=100&page={n}"]
                               for n in (1, 2)])
        self.assertIn(f"{QUALITY} completed/success on {HEAD} (run 2000)", out)
        self.assertIn(f"{ATTRIBUTION} completed/success on {HEAD} (run 2001)", out)

    def test_D5_page_ending_early_or_inconsistent_refused_before_merge(self):
        # 3b882 fix round 5 (round 4 agy-A finding 1): a page that ends before total_count is
        # reached, or a malformed, over-full or inconsistent page, refuses with exit 2; part of
        # the list is never judged, even when the runs read so far are green.
        full = [run("Other workflow", run_id=1000 + i) for i in range(100)]
        both = [run(QUALITY, run_id=1), run(ATTRIBUTION, run_id=2)]

        def page(total, runs):
            return json.dumps({"total_count": total, "workflow_runs": runs})
        cases = {
            "second page ends early": [page(201, full), page(201, both)],
            "second page empty": [page(101, full), page(101, [])],
            "first page ends early": [page(3, both)],
            "total_count changes": [page(101, full), page(102, [run(QUALITY, run_id=1)])],
            "more runs than total_count": [page(101, full), page(101, both)],
            "run id repeated": [page(101, full), page(101, [run(QUALITY, run_id=1000)])],
            "second page not JSON": [page(101, full), "<html>"],
            "second page without a run list": [page(101, full), json.dumps({"total_count": 101})],
            "second page total_count not an integer": [page(101, full), page("101", both[:1])],
            "page holds more than per_page": [page(102, full + both)],
        }
        for name, pages in cases.items():
            with self.subTest(case=name):
                fake = FakeGh(pages=pages)
                code, out, err = self.merge(fake)
                self.assertEqual(code, 2, err)
                self.assertEqual(fake.merge_calls(), [])
                self.assertEqual(out, "")

    def test_D5_not_green_refused_before_merge(self):
        q = "Repository quality checks"
        cases = {
            "failure": [run(q, conclusion="failure")],
            "pending": [run(q, status="in_progress", conclusion=None)],
            "queued": [run(q, status="queued", conclusion=None)],
            "cancelled": [run(q, conclusion="cancelled")],
            "skipped": [run(q, conclusion="skipped")],
            "missing": [run("Pull request attribution")],
            "no runs": [],
            "other head only": [run(q, sha="b" * 40)],
            "latest failed after an older success": [
                run(q, run_id=1, created="2026-11-14T10:00:00Z"),
                run(q, conclusion="failure", run_id=2, created="2026-11-14T11:00:00Z")],
            "latest pending after an older success": [
                run(q, run_id=1, created="2026-11-14T10:00:00Z"),
                run(q, status="in_progress", conclusion=None, run_id=2,
                    created="2026-11-14T11:00:00Z")],
        }
        for name, runs in cases.items():
            with self.subTest(case=name):
                fake = FakeGh(runs=runs)
                code, out, err = self.merge(fake)
                self.assertEqual(code, 1, err)
                self.assertIn(q, err)
                self.assertEqual(fake.merge_calls(), [])

    def test_D5_unreadable_runs_refused_before_merge(self):
        cases = {
            "gh error": {"runs_error": subprocess.CalledProcessError(1, ["gh"], "", "HTTP 403")},
            "not JSON": {"runs_text": "<html>"},
            "not an object": {"runs_text": "[]"},
            "no run list": {"runs_text": json.dumps({"total_count": 0})},
            "truncated list": {"runs_text": json.dumps(
                {"total_count": 101, "workflow_runs": [run("Repository quality checks")]})},
            "run not an object": {"runs_text": json.dumps({"total_count": 1, "workflow_runs": ["x"]})},
        }
        for name, over in cases.items():
            with self.subTest(case=name):
                fake = FakeGh(**over)
                code, out, err = self.merge(fake)
                self.assertEqual(code, 2, err)
                self.assertEqual(fake.merge_calls(), [])

    def test_D5_latest_success_after_an_older_failure_allowed(self):
        q = "Repository quality checks"
        fake = FakeGh(runs=[run(q, conclusion="failure", run_id=1, created="2026-11-14T10:00:00Z"),
                            run(q, run_id=2, created="2026-11-14T11:00:00Z"),
                            run(ATTRIBUTION, run_id=3)])
        code, out, err = self.merge(fake)
        self.assertEqual(code, 0, err)

    def test_D5_malformed_run_record_refused_before_merge(self):
        # 3b882 fix round 6 (round 5 codex F1): a required workflow's pull_request runs are
        # ordered by created_at, then id, so each must carry a positive integer id and a
        # parseable created_at. A failed run with no created_at used to sort below a dated
        # success, and a green run with a missing or string id was accepted; each now refuses
        # with exit 2 before any merge call.
        dated = run(QUALITY, run_id=2, created="2026-11-14T11:00:00Z")
        failed = run(QUALITY, conclusion="failure", run_id=5)
        del failed["created_at"]
        no_id = run(QUALITY)
        del no_id["id"]
        cases = {
            "missing created_at": [dated, failed, run(ATTRIBUTION, run_id=3)],
            "missing id": [no_id, run(ATTRIBUTION, run_id=3)],
            "string id": [run(QUALITY, run_id="43583397326"), run(ATTRIBUTION, run_id=3)],
            "zero id": [run(QUALITY, run_id=0), run(ATTRIBUTION, run_id=3)],
            "boolean id": [run(QUALITY, run_id=True), run(ATTRIBUTION, run_id=3)],
            "unparseable created_at": [dated, run(QUALITY, conclusion="failure", run_id=5,
                                                  created="yesterday"), run(ATTRIBUTION, run_id=3)],
            "created_at without a zone": [run(QUALITY, created="2026-11-14T11:00:00"),
                                          run(ATTRIBUTION, run_id=3)],
            "malformed attribution run": [run(QUALITY), run(ATTRIBUTION, run_id=None)],
        }
        for name, runs in cases.items():
            for dry_run in (False, True):
                with self.subTest(case=name, dry_run=dry_run):
                    fake = FakeGh(runs=runs)
                    code, out, err = self.merge(fake, dry_run=dry_run)
                    self.assertEqual(code, 2, err)
                    self.assertIn("malformed", err)
                    self.assertEqual(fake.merge_calls(), [])
                    self.assertEqual(out, "")

    def test_D5_runs_ordered_by_parsed_created_at(self):
        # 3b882 fix round 6: created_at is compared as a time, not as text, so a later failed
        # run written with an offset still outranks an earlier success.
        fake = FakeGh(runs=[run(QUALITY, run_id=1, created="2026-11-14T11:00:00Z"),
                            run(QUALITY, conclusion="failure", run_id=2,
                                created="2026-11-14T12:30:00+01:00"),
                            run(QUALITY, conclusion="failure", run_id=4,
                                created="2026-11-14T11:30:00.250+00:00"),
                            run(ATTRIBUTION, run_id=3)])
        code, out, err = self.merge(fake)
        self.assertEqual(code, 1, err)
        self.assertIn("latest run 4", err)
        self.assertEqual(fake.merge_calls(), [])

    def assert_ci_refused(self, cases):
        for name, (runs, culprit) in cases.items():
            with self.subTest(case=name):
                fake = FakeGh(runs=runs)
                code, out, err = self.merge(fake)
                self.assertEqual(code, 1, err)
                self.assertIn(culprit, err)
                self.assertEqual(fake.merge_calls(), [])
                self.assertEqual(out, "")

    def test_D5_required_workflows_bound_to_their_files(self):
        self.assertEqual(self.mod.WORKFLOW_PATHS, WORKFLOW_PATHS)
        self.assertEqual(set(self.mod.WORKFLOW_PATHS), set(self.mod.REQUIRED_WORKFLOWS))
        self.assertEqual(self.mod.CI_EVENT, "pull_request")

    def test_D5_same_named_run_from_another_file_refused_before_merge(self):
        # claude F1: a PR could add a workflow file that reuses a required name. Only the bound
        # file may satisfy it, and a same-named run from any other path refuses, even beside a
        # green run from the bound file (as evaluate_runs in merge-when-green.py does).
        decoy = ".github/workflows/decoy.yml"
        self.assert_ci_refused({
            "decoy only": ([run(QUALITY, path=decoy), run(ATTRIBUTION, run_id=2)], QUALITY),
            "decoy green after the real run failed": ([
                run(QUALITY, conclusion="failure", run_id=1, created="2026-11-14T10:00:00Z"),
                run(QUALITY, path=decoy, run_id=3, created="2026-11-14T11:00:00Z"),
                run(ATTRIBUTION, run_id=2)], QUALITY),
            "decoy beside a green real run": ([
                run(QUALITY), run(QUALITY, path=decoy, run_id=3), run(ATTRIBUTION, run_id=2)],
                QUALITY),
            "attribution decoy": ([
                run(QUALITY), run(ATTRIBUTION, run_id=2), run(ATTRIBUTION, path=decoy, run_id=3)],
                ATTRIBUTION),
            "no path reported": ([run(QUALITY, path=""), run(ATTRIBUTION, run_id=2)], QUALITY),
        })

    def test_D5_only_a_pull_request_run_counts(self):
        # claude F1: a later workflow_dispatch or push run on the head never stands in for the
        # pull_request run of a required workflow.
        def later(event):
            return [run(QUALITY, conclusion="failure", run_id=1, created="2026-11-14T10:00:00Z"),
                    run(QUALITY, event=event, run_id=3, created="2026-11-14T11:00:00Z"),
                    run(ATTRIBUTION, run_id=2)]
        self.assert_ci_refused({
            "workflow_dispatch success after a failed pull_request run": (
                later("workflow_dispatch"), QUALITY),
            "push success after a failed pull_request run": (later("push"), QUALITY),
            "workflow_dispatch only": ([run(QUALITY, event="workflow_dispatch"),
                                        run(ATTRIBUTION, run_id=2)], QUALITY),
            "no event reported": ([run(QUALITY, event=None), run(ATTRIBUTION, run_id=2)],
                                  QUALITY),
        })

    def test_D5_later_failed_non_pull_request_run_does_not_refuse(self):
        # 3b882 fix round 4 (round 3 agy M1): the latest pull_request run is judged, so a later
        # failed workflow_dispatch (or push) run on the head never refuses a green pull_request run.
        for event in ("workflow_dispatch", "push"):
            with self.subTest(event=event):
                fake = FakeGh(runs=[
                    run(QUALITY, run_id=1, created="2026-11-14T10:00:00Z"),
                    run(QUALITY, conclusion="failure", event=event, run_id=3,
                        created="2026-11-14T11:00:00Z"),
                    run(ATTRIBUTION, run_id=2)])
                code, out, err = self.merge(fake)
                self.assertEqual(code, 0, err)
                self.assertEqual(len(fake.merge_calls()), 1)

    # Plan section 3: the open-findings check, reused from merge-when-green.py.

    def install_open_findings(self, rows):
        """A copy of the open-findings hook in the fixture repository (so merge-when-green's
        open_findings_block finds it) and a ledger in the fixture store."""
        self.install_hook()
        (self.store / "open-findings.md").write_text(LEDGER_HEAD + rows, encoding="utf-8")

    def install_hook(self):
        hooks = self.root / ".claude" / "hooks"
        hooks.mkdir(parents=True, exist_ok=True)
        (hooks / HOOK_NAME).write_bytes((REPO_ROOT / ".claude" / "hooks" / HOOK_NAME).read_bytes())

    def test_open_findings_undispositioned_error_refuses_before_any_gh_call(self):
        self.install_open_findings(OPEN_ERROR)
        for dry_run in (False, True):
            with self.subTest(dry_run=dry_run):
                fake = FakeGh()
                code, out, err = self.merge(fake, dry_run=dry_run)
                self.assertEqual(code, 1, err)
                self.assertEqual(fake.calls, [])
                self.assertIn("a live defect", err)
                self.assertIn("REFUSED", err)
                self.assertEqual(out, "")

    def test_open_findings_dispositioned_error_allows_the_merge(self):
        self.install_open_findings(FIXED_ERROR)
        fake = FakeGh()
        code, out, err = self.merge(fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(fake.merge_calls(), [MERGE_ARGV])

    def test_open_findings_reads_a_clean_ledger_once_and_the_merge_goes_ahead(self):
        # 3b882 fix round 6 (round 5 claude F2, codex F2): renamed from
        # test_open_findings_second_ledger_read_never_allows_a_merge, which no longer fit: the
        # test asserts one ledger read and, on that clean ledger, a merge that goes ahead.
        # codex MED 1: the ledger is read once and that text is judged. A second read that
        # raises PermissionError (merge-when-green's open_findings_block allows on any read
        # error) must never decide a merge. 3b882 fix round 5 (round 4 agy-B): the ledger is
        # clean, so the first read alone allows and only a second read could take part; the
        # tool must read it exactly once (an open ledger refused on the first read, so the old
        # case passed whether or not a second read happened).
        self.install_open_findings(FIXED_ERROR)
        real = Path.read_text
        reads = []

        def read_text(path, *args, **kwargs):
            if Path(path).name == "open-findings.md":
                reads.append(str(path))
                if len(reads) > 1:
                    raise PermissionError(13, "Permission denied", str(path))
            return real(path, *args, **kwargs)
        for dry_run in (False, True):
            with self.subTest(dry_run=dry_run):
                reads.clear()
                fake = FakeGh()
                with mock.patch.object(Path, "read_text", autospec=True, side_effect=read_text):
                    code, out, err = self.merge(fake, dry_run=dry_run)
                self.assertEqual(len(reads), 1, reads)
                self.assertEqual(code, 0, err)
                self.assertNotIn("Permission denied", err)
                self.assertEqual(fake.merge_calls(), [] if dry_run else [MERGE_ARGV])

    def test_open_findings_parse_failure_refuses_before_any_gh_call(self):
        # codex MED 1: a ledger the hook cannot parse refuses (merge-when-green allows it).
        hook = self.root / ".claude" / "hooks" / HOOK_NAME
        hook.write_text(hook.read_text(encoding="utf-8") + "\n\ndef parse_open_rows(text):\n"
                        "    raise ValueError('unparseable ledger')\n", encoding="utf-8")
        self.assert_refused_before_gh("open-findings")

    def test_open_findings_agrees_with_merge_when_green_on_a_readable_ledger(self):
        # The tool judges the text it read with the hook's own parse and decision, the two
        # calls merge-when-green.py's open_findings_block() makes, so on a readable, parseable
        # ledger the two tools agree. On a readable ledger the hook cannot parse they differ:
        # merge-when-green.py allows it, and this tool refuses it.
        spec = importlib.util.spec_from_file_location(
            "_mgln_test_merge_when_green", REPO_ROOT / "tools" / "merge-when-green.py")
        mwg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mwg)
        ledger = Path(self.tmp.name) / "ledger.md"
        for rows in ("", OPEN_ERROR, FIXED_ERROR, FIXED_ERROR + OPEN_ERROR):
            with self.subTest(rows=rows):
                ledger.write_text(LEDGER_HEAD + rows, encoding="utf-8")
                self.assertEqual(self.mod.open_findings(REPO_ROOT, ledger),
                                 mwg.open_findings_block(REPO_ROOT, ledger))

    def test_open_findings_is_merge_when_green_decision_on_the_real_hook(self):
        ledger = Path(self.tmp.name) / "ledger.md"
        ledger.write_text(LEDGER_HEAD + OPEN_ERROR, encoding="utf-8")
        code, message = self.mod.open_findings(REPO_ROOT, ledger)
        self.assertEqual(code, 1)
        self.assertIn("a live defect", message)
        ledger.write_text(LEDGER_HEAD + FIXED_ERROR, encoding="utf-8")
        self.assertEqual(self.mod.open_findings(REPO_ROOT, ledger), (0, ""))

    # Part 2c: a refusal before any gh call, dry run or not.

    def assert_refused_before_gh(self, needle):
        for dry_run in (False, True):
            with self.subTest(dry_run=dry_run):
                fake = FakeGh()
                code, out, err = self.merge(fake, dry_run=dry_run)
                self.assertEqual(code, 2, err)
                self.assertEqual(fake.calls, [])
                self.assertEqual(out, "")
                self.assertIn("REFUSED", err)
                self.assertIn(needle, err)

    # Part 2c item 1: the admin-merge log pre-flight.

    def test_log_preflight_missing_log_refuses_before_any_gh_call(self):
        os.replace(self.log, Path(self.tmp.name) / "moved-log.md")
        self.assert_refused_before_gh(LOG_REL)

    def test_log_preflight_header_mismatch_refuses_before_any_gh_call(self):
        for text in ("", "# Merge-bypass log\n\nprose only, no table\n",
                     HEADER.replace("Change", "Changes") + "\n",
                     HEADER + " \n", HEADER.replace("| ", "|", 1) + "\n",
                     "# t\n\n| a | b | c |\n\n" + HEADER + "\n" + OLD_LOG_ROW + "\n",
                     LOG_SHAPE.replace(HEADER, HEADER.replace("PR", "Pull request"))):
            with self.subTest(text=text):
                self.log.write_text(text, encoding="utf-8")
                self.assert_refused_before_gh("header")

    def test_log_preflight_unreadable_log_refuses_before_any_gh_call(self):
        self.log.write_bytes(b"\xff" + HEADER.encode() + b"\n")
        self.assert_refused_before_gh(LOG_REL)
        if hasattr(os, "geteuid") and os.geteuid() != 0:
            self.log.write_text(HEADER + "\n", encoding="utf-8")
            self.log.chmod(0)
            self.addCleanup(self.log.chmod, 0o644)
            self.assert_refused_before_gh(LOG_REL)
            self.log.chmod(0o644)
        os.replace(self.log, Path(self.tmp.name) / "moved-log.md")
        self.log.mkdir()
        self.assert_refused_before_gh(LOG_REL)

    def test_log_preflight_outside_the_store_refuses_before_any_gh_call(self):
        # Decision D1: the private sibling and in-repo .working/ fallbacks never stand in, and a
        # store entry that resolves outside the store is refused.
        moved = Path(self.tmp.name) / "moved-log.md"
        os.replace(self.log, moved)
        sibling = Path(self.tmp.name) / "grc_library_private" / ".working"
        sibling.mkdir(parents=True)
        (sibling / LOG_REL).write_text(HEADER + "\n", encoding="utf-8")
        (self.root / ".working").mkdir()
        (self.root / ".working" / LOG_REL).write_text(HEADER + "\n", encoding="utf-8")
        self.assert_refused_before_gh(LOG_REL)
        self.assertEqual((sibling / LOG_REL).read_text(encoding="utf-8"), HEADER + "\n")
        self.assertEqual((self.root / ".working" / LOG_REL).read_text(encoding="utf-8"),
                         HEADER + "\n")
        self.log.symlink_to(moved)
        self.assert_refused_before_gh(LOG_REL)
        self.assertEqual(moved.read_text(encoding="utf-8"), LOG_SHAPE)

    def test_log_preflight_in_store_symlink_refuses_before_any_gh_call(self):
        # codex MED 2: the append opens the log with O_NOFOLLOW, so a final-component symlink,
        # even to a writable file inside the store, would refuse the row after the merge. The
        # pre-flight refuses it before any gh call.
        target = self.store / "real-merge-bypass-log.md"
        os.replace(self.log, target)
        self.log.symlink_to(target.name)
        self.assertTrue(self.log.resolve().is_relative_to(self.store.resolve()))
        self.assert_refused_before_gh("symlink")
        self.assertEqual(target.read_text(encoding="utf-8"), LOG_SHAPE)

    # Part 2d item 1: the header is the first table line; text before it is allowed.

    def test_log_preflight_accepts_the_real_log_shape(self):
        self.assertEqual(self.log.read_text(encoding="utf-8"), LOG_SHAPE)
        code, out, err = self.merge(FakeGh(), dry_run=True)
        self.assertEqual(code, 0, err)
        self.assertEqual(self.log.read_text(encoding="utf-8"), LOG_SHAPE)
        code, out, err = self.merge(FakeGh())
        self.assertEqual(code, 0, err)
        self.assertEqual(len(out.splitlines()), 1, out)
        self.assertEqual(self.log.read_text(encoding="utf-8"), LOG_SHAPE + out)

    def test_log_preflight_text_before_the_header_is_allowed(self):
        for text in ("\n" + HEADER + "\n", "# Merge bypass log\n\n" + HEADER + "\n",
                     "# t\n\n- a | b list item\n  | indented, not a table line\n\n" + HEADER
                     + "\n" + OLD_LOG_ROW + "\n"):
            with self.subTest(text=text):
                self.log.write_text(text, encoding="utf-8")
                fake = FakeGh()
                code, out, err = self.merge(fake, dry_run=True)
                self.assertEqual(code, 0, err)
                self.assertEqual(len(fake.merge_calls()), 0)
                self.assertIn("DRY RUN", err)

    # Part 2d item 2: the last line itself must be a table line, with no blank or
    # whitespace-only line after it, so the row lands in the table.

    def test_log_preflight_last_line_not_a_table_line_refuses_before_any_gh_call(self):
        for text in (HEADER + "\n" + OLD_LOG_ROW + "\nprose after the table\n",
                     HEADER + "\n" + OLD_LOG_ROW + "\nprose after the table",
                     HEADER + "\n\n- a list after the table\n\n",
                     HEADER + "\n" + OLD_LOG_ROW + "\n\n",
                     HEADER + "\n" + OLD_LOG_ROW + "\n \t\n",
                     LOG_SHAPE + "\nA closing paragraph.\n"):
            with self.subTest(text=text):
                self.log.write_text(text, encoding="utf-8")
                self.assert_refused_before_gh("outside the table")
                self.assertEqual(self.log.read_text(encoding="utf-8"), text)

    # Part 2d item 3: a log that cannot be opened for append refuses before the merge.

    @unittest.skipIf(hasattr(os, "geteuid") and os.geteuid() == 0,
                     "root may write a file whatever its mode")
    def test_log_preflight_unwritable_log_refuses_before_any_gh_call(self):
        self.log.chmod(0o444)
        self.addCleanup(self.log.chmod, 0o644)
        self.assert_refused_before_gh("not writable")
        self.assertEqual(self.log.read_text(encoding="utf-8"), LOG_SHAPE)

    def test_log_preflight_checks_writability_without_writing(self):
        # The check is os.access for reading and writing (what the append's O_RDWR needs) on
        # the log path itself, a final symlink being refused first, after the D1 store check;
        # it opens nothing for writing, so the log's bytes and modification time stay as they
        # were.
        before = (self.log.read_bytes(), self.log.stat().st_mtime_ns)
        seen = []
        real = os.access

        def access(path, mode, *args, **kwargs):
            seen.append((Path(path), mode))
            return real(path, mode, *args, **kwargs)
        with mock.patch.object(self.mod.os, "access", side_effect=access):
            code, out, err = self.merge(FakeGh(), dry_run=True)
        self.assertEqual(code, 0, err)
        self.assertIn((self.log.resolve(), os.R_OK | os.W_OK),
                      [(path.resolve(), mode) for path, mode in seen])
        self.assertEqual((self.log.read_bytes(), self.log.stat().st_mtime_ns), before)

    # Part 2c item 2: the printed row is appended to the log and read back.

    def test_log_row_appended_exactly_once(self):
        code, out, err = self.merge(FakeGh())
        self.assertEqual(code, 0, err)
        lines = out.splitlines()
        self.assertEqual(len(lines), 1, out)
        self.assertEqual(self.log.read_text(encoding="utf-8"), LOG_SHAPE + lines[0] + "\n")

    def test_log_row_appended_after_a_failed_commit_readback(self):
        fake = FakeGh(message=SUBJECT + "\n\n" + BODY + "\n\nCo-authored-by: a <b@example.com>\n")
        code, out, err = self.merge(fake)
        self.assertEqual(code, 3, err)
        # The row was printed, naming the tagged PR cell, and appended: a tool that appends
        # and prints nothing leaves out empty and the log unchanged, and fails here.
        self.assertTrue(out.startswith("| 2026-11-15 | #31 [repo: grc_library_new] | "), out)
        self.assertTrue(out.endswith(" |\n"), out)
        self.assertEqual(self.log.read_text(encoding="utf-8"), LOG_SHAPE + out)

    def test_log_without_a_final_newline_gets_the_row_on_its_own_line(self):
        self.log.write_text(HEADER + "\n" + OLD_LOG_ROW, encoding="utf-8")
        code, out, err = self.merge(FakeGh())
        self.assertEqual(code, 0, err)
        self.assertEqual(self.log.read_text(encoding="utf-8"),
                         HEADER + "\n" + OLD_LOG_ROW + "\n" + out)

    def test_log_append_failure_exits_3_and_prints_the_row_to_stderr(self):
        fake = FakeGh()

        def swap(*args):
            if list(args[:2]) == ["pr", "merge"]:
                os.replace(self.log, Path(self.tmp.name) / "moved-log.md")
                self.log.mkdir()
            return fake(*args)
        code, out, err = self.merge(swap)
        self.assertEqual(code, 3, err)
        self.assertEqual(len(fake.merge_calls()), 1)
        row = out.splitlines()[0]
        self.assertIn(row, err.splitlines())
        self.assertIn("by hand", err)

    def test_log_readback_mismatch_or_error_exits_3_and_prints_the_row_to_stderr(self):
        for patch in ({"return_value": "| other |"}, {"side_effect": OSError("read failed")}):
            with self.subTest(patch=patch):
                self.log.write_text(HEADER + "\n", encoding="utf-8")
                with mock.patch.object(self.mod, "_log_last_line", **patch):
                    code, out, err = self.merge(FakeGh())
                self.assertEqual(code, 3, err)
                self.assertIn(out.splitlines()[0], err.splitlines())
                self.assertIn("by hand", err)

    # Part 2c item 3: the open-findings check fails closed.

    def test_open_findings_hook_absent_refuses_before_any_gh_call(self):
        os.replace(self.root / ".claude" / "hooks" / HOOK_NAME, Path(self.tmp.name) / "moved-hook.py")
        self.assert_refused_before_gh("open-findings")

    def test_open_findings_hook_unloadable_refuses_before_any_gh_call(self):
        (self.root / ".claude" / "hooks" / HOOK_NAME).write_text(
            "raise RuntimeError('broken')\n", encoding="utf-8")
        self.assert_refused_before_gh("open-findings")

    def test_open_findings_no_ledger_in_the_store_refuses_before_any_gh_call(self):
        moved = Path(self.tmp.name) / "moved-ledger.md"
        os.replace(self.store / "open-findings.md", moved)
        self.assert_refused_before_gh("open-findings")
        # Decision D1: a ledger in the private sibling or the in-repo .working/ never stands in.
        sibling = Path(self.tmp.name) / "grc_library_private" / ".working"
        sibling.mkdir(parents=True)
        (sibling / "open-findings.md").write_text(LEDGER_HEAD, encoding="utf-8")
        (self.root / ".working").mkdir()
        (self.root / ".working" / "open-findings.md").write_text(LEDGER_HEAD, encoding="utf-8")
        self.assert_refused_before_gh("open-findings")
        (self.store / "open-findings.md").symlink_to(moved)
        self.assert_refused_before_gh("open-findings")

    def test_open_findings_unreadable_ledger_refuses_before_any_gh_call(self):
        (self.store / "open-findings.md").write_bytes(b"\xff" + LEDGER_HEAD.encode())
        self.assert_refused_before_gh("open-findings")

    # The command line, and --check-rows staying read-only.

    def test_cli_check_rows_makes_no_gh_call(self):
        def no_gh(*args):
            raise AssertionError("gh called")
        with mock.patch.object(self.mod, "gh", no_gh), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.mod.main(["--check-rows", "31"]), 0)

    def test_cli_merge_mode_uses_the_gh_helper(self):
        fake = FakeGh()
        with mock.patch.object(self.mod, "gh", fake), mock.patch.object(self.mod, "REPO_ROOT", self.root), \
                mock.patch.object(self.mod.time, "sleep", self.sleeps.append), \
                contextlib.redirect_stdout(io.StringIO()) as out, \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.mod.main(["31", "--dry-run"]), 0)
        # 3b882 fix round 6 (round 5 agy-B F2): main() must have called the patched gh helper
        # (the PR view and the Actions runs read), not merely returned 0.
        self.assertTrue(fake.calls, "main() made no gh call")
        self.assertIn(["pr", "view", "31", "--repo", REPO, "--json",
                       "number,title,state,headRefOid,baseRefName,url"], fake.calls)
        self.assertTrue(any(c[0] == "api" and "/actions/runs?head_sha=" + HEAD in c[1]
                            for c in fake.calls), fake.calls)
        self.assertEqual(fake.merge_calls(), [])
        self.assertEqual(out.getvalue(), "")

    def test_cli_bad_usage_exits_2_without_gh(self):
        def no_gh(*args):
            raise AssertionError("gh called")
        for argv in (["031"], ["0"], ["3x"], ["３１"], ["31", "--check-rows", "31"],
                     ["--check-rows", "31", "--dry-run"], ["--self-test", "31"], []):
            with self.subTest(argv=argv), mock.patch.object(self.mod, "gh", no_gh), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                try:
                    code = self.mod.main(argv)
                except SystemExit as exc:
                    code = exc.code
                self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
