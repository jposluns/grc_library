"""Tests for tools/merge-grc-library-new.py, part P2a of the 3b882 merge-tool plan: the merge
argv (T3), the read-back of the merged commit (T4), the admin-merge log row printed to standard
output (T5), the title suffix (T6, decision D3) and the CI check on the pinned head (decision D5);
part P2b: both required workflows (D5), the log-row cell escaping (T5) and the open-findings check
reused from merge-when-green.py (plan section 3); part P2c: the admin-merge log pre-flight before any
gh call, the row appended to the log and read back, and the open-findings check failing closed.

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


def gfm_cells(row):
    """The cells of a table row split as GFM does: a backslash escapes the character after it,
    so only an unescaped pipe separates cells (a backslash-backslash pair escapes itself)."""
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
        runs = over.pop("runs", [run(QUALITY), run(ATTRIBUTION, run_id=43583397345)])
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
        self.install_hook()
        (self.store / "open-findings.md").write_text(LEDGER_HEAD, encoding="utf-8")
        self.log = self.store / LOG_REL
        self.log.write_text(HEADER + "\n", encoding="utf-8")
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

    def test_T5_line_breaking_title_characters_keep_one_row(self):
        # Every character str.splitlines() treats as a line boundary, and any other control
        # character, becomes a space, so the row stays one line of six cells.
        for char in ("\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029", "\r",
                     "\x00", "\x1b"):
            with self.subTest(char=repr(char)):
                title = f"content: a{char}b (CalVer 2026.11.69, README 1.11.919)"
                fake = FakeGh(view={"title": title}, message=title + " (#31)\n\n" + BODY)
                code, out, err = self.merge(fake)
                self.assertEqual(code, 0, err)
                lines = out.splitlines()
                self.assertEqual(len(lines), 1, repr(out))
                self.assertEqual(len(gfm_cells(lines[0])), 6, repr(lines[0]))
                self.assertNotIn(char, lines[0])

    def snapshot(self):
        return {p: (p.read_bytes() if p.is_file() else None)
                for p in sorted(Path(self.tmp.name).rglob("*")) if "__pycache__" not in p.parts}

    def test_T5_dry_run_writes_no_file_and_the_merge_changes_only_the_log(self):
        before = self.snapshot()
        code, out, err = self.merge(FakeGh(), dry_run=True)
        self.assertEqual(code, 0, err)
        self.assertEqual(self.snapshot(), before)
        code, out, err = self.merge(FakeGh())
        self.assertEqual(code, 0, err)
        after = self.snapshot()
        changed = sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))
        self.assertEqual(changed, [self.log])

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
                            run(q, run_id=2, created="2026-11-14T11:00:00Z"),
                            run(ATTRIBUTION, run_id=3)])
        code, out, err = self.merge(fake)
        self.assertEqual(code, 0, err)

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

    def test_open_findings_unloadable_merge_when_green_refuses(self):
        fake = FakeGh()
        with mock.patch.object(self.mod, "MERGE_WHEN_GREEN", self.root / "absent.py"):
            code, out, err = self.merge(fake)
        self.assertEqual(code, 2, err)
        self.assertEqual(fake.calls, [])
        self.assertIn("merge-when-green", err)

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
        for text in ("", "\n" + HEADER + "\n", HEADER.replace("Change", "Changes") + "\n",
                     HEADER + " \n", "# Merge bypass log\n\n" + HEADER + "\n",
                     HEADER.replace("| ", "|", 1) + "\n"):
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
        self.assertEqual(moved.read_text(encoding="utf-8"), HEADER + "\n")

    # Part 2c item 2: the printed row is appended to the log and read back.

    def test_log_row_appended_exactly_once(self):
        code, out, err = self.merge(FakeGh())
        self.assertEqual(code, 0, err)
        lines = out.splitlines()
        self.assertEqual(len(lines), 1, out)
        self.assertEqual(self.log.read_text(encoding="utf-8"), HEADER + "\n" + lines[0] + "\n")

    def test_log_row_appended_after_a_failed_readback(self):
        fake = FakeGh(message=SUBJECT + "\n\n" + BODY + "\n\nCo-authored-by: a <b@example.com>\n")
        code, out, err = self.merge(fake)
        self.assertEqual(code, 3, err)
        self.assertEqual(self.log.read_text(encoding="utf-8"), HEADER + "\n" + out)

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
