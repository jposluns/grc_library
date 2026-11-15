"""Tests for tools/merge-grc-library-new.py, part P2a of the 3b882 merge-tool plan: the merge
argv (T3), the read-back of the merged commit (T4), the admin-merge log row printed to standard
output (T5), the title suffix (T6, decision D3) and the CI check on the pinned head (decision D5).

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


def load_tool():
    spec = importlib.util.spec_from_file_location("_merge_grc_library_new_p2a", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(name, conclusion="success", status="completed", sha=HEAD, run_id=43583397326,
        created="2026-11-14T10:30:00Z"):
    return {"id": run_id, "name": name, "head_sha": sha, "status": status,
            "conclusion": conclusion, "created_at": created}


class FakeGh:
    """A stand-in for the tool's gh(): answers by call shape and records every call."""

    def __init__(self, **over):
        self.calls = []
        self.view = {"number": 31, "title": TITLE, "state": "OPEN", "headRefOid": HEAD,
                     "baseRefName": "main", "url": f"https://github.com/{REPO}/pull/31"}
        self.view.update(over.pop("view", {}))
        runs = over.pop("runs", [run("Repository quality checks")])
        self.runs = over.pop("runs_text", json.dumps({"total_count": len(runs), "workflow_runs": runs}))
        self.runs_error = over.pop("runs_error", None)
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

    def test_T5_writes_no_file(self):
        before = sorted(p for p in Path(self.tmp.name).rglob("*"))
        code, out, err = self.merge(FakeGh())
        self.assertEqual(code, 0, err)
        self.assertEqual(sorted(p for p in Path(self.tmp.name).rglob("*")), before)

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

    def test_T6_title_with_suffix_allowed(self):
        for title in (TITLE, "tools: y (CalVer 2026.9.3, README 1.10.4)"):
            with self.subTest(title=title):
                self.assertTrue(self.mod.title_has_suffix(title))

    # D5: every required workflow concluded success on the pinned head.

    def test_D5_required_workflows_from_the_new_repository(self):
        self.assertEqual(self.mod.REQUIRED_WORKFLOWS, ("Repository quality checks",))

    def test_D5_runs_read_by_pinned_head(self):
        fake = FakeGh()
        self.merge(fake)
        api = [c for c in fake.calls if c[0] == "api" and "/actions/runs" in c[1]]
        self.assertEqual(api, [["api", f"repos/{REPO}/actions/runs?head_sha={HEAD}&per_page=100"]])

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
                            run(q, run_id=2, created="2026-11-14T11:00:00Z")])
        code, out, err = self.merge(fake)
        self.assertEqual(code, 0, err)

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
