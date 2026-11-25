"""Staged metadata pairing and full-runner freshness ordering regressions."""

import contextlib
import importlib.util
import io
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

TOOLS = Path(__file__).resolve().parents[1] / "tools"
ROOT = TOOLS.parents[3]
SPEC = importlib.util.spec_from_file_location("commit_metadata", TOOLS / "check-version-date-commit.py")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)
OLD = "1" * 40
NEW = "2" * 40
ZERO = "0" * 40
BEFORE = b"# Document\n\n**Version:** 1.0\\\n**Date:** 2026-11-23\\\n\nBody.\n"


class CommitMetadataTests(unittest.TestCase):
    def setUp(self):
        patch = mock.patch.object(CHECK, "utc_today", return_value="2026-11-24")
        patch.start()
        self.addCleanup(patch.stop)

    def check(self, after, before=BEFORE, status="M", name="document.md", failure=None):
        old_mode = "000000" if before is None else "100644"
        new_mode = "000000" if after is None else "100644"
        old_oid = ZERO if before is None else OLD
        new_oid = ZERO if after is None else NEW
        raw = os.fsencode(f":{old_mode} {new_mode} {old_oid} {new_oid} {status}\0{name}\0")
        if status.startswith("R"):
            raw += b"renamed.md\0"
        reads = []

        def git(*args):
            if args[0] == "ls-files":
                return b""
            if args[0] == "diff":
                self.assertIn("--cached", args)
                self.assertIn("-z", args)
                return raw
            self.assertEqual(args[:2], ("cat-file", "blob"))
            reads.append(args[2])
            if args[2] == failure:
                raise CHECK.InspectionError("blob unreadable")
            return {OLD: before, NEW: after}[args[2]]

        output = io.StringIO()
        with mock.patch.object(CHECK, "git", side_effect=git), contextlib.redirect_stdout(output), \
                contextlib.redirect_stderr(output):
            rc = CHECK.main(["--pre-commit"])
        return rc, output.getvalue(), reads

    def test_version_without_date_refused(self):
        rc, out, reads = self.check(BEFORE.replace(b"1.0", b"1.1"))
        self.assertEqual(rc, 1, out)
        self.assertIn("document.md", out)
        self.assertEqual(reads, [OLD, NEW])

    def test_date_without_version_refused(self):
        self.assertEqual(self.check(BEFORE.replace(b"2026-11-23", b"2026-11-24"))[0], 1)

    def test_neither_changed_passes(self):
        self.assertEqual(self.check(BEFORE.replace(b"Body.", b"Revised body."))[0], 0)

    def test_both_changed_passes(self):
        after = BEFORE.replace(b"1.0", b"1.1").replace(b"2026-11-23", b"2026-11-24")
        self.assertEqual(self.check(after)[0], 0)

    def test_date_only_unversioned_document_passes(self):
        before = b"**Date:** 2026-11-23\n"
        self.assertEqual(self.check(before.replace(b"23", b"24"), before=before)[0], 0)

    def test_unreadable_either_document_fails_closed(self):
        for oid in (OLD, NEW):
            with self.subTest(oid=oid):
                rc, out, _ = self.check(BEFORE, failure=oid)
                self.assertEqual(rc, 2, out)
                self.assertIn("blob unreadable", out)

    def test_invalid_utf8_fails_closed(self):
        self.assertEqual(self.check(BEFORE + b"\xff")[0], 2)
        self.assertEqual(self.check(BEFORE, before=BEFORE + b"\xff")[0], 2)

    def test_new_and_deleted_documents(self):
        self.assertEqual(self.check(BEFORE, before=None, status="A")[0], 0)
        self.assertEqual(self.check(None, status="D")[0], 0)
        self.assertEqual(self.check(b"**Version:** 1.0\n", before=None, status="A")[0], 0)
        self.assertEqual(self.check(b"\xff", before=None, status="A")[0], 0)
        self.assertEqual(self.check(None, before=b"\xff", status="D")[0], 0)

    def test_removed_version_still_requires_date_change(self):
        self.assertEqual(self.check(BEFORE.replace(b"**Version:** 1.0\\\n", b""))[0], 1)

    def test_rename_and_unusual_filename(self):
        rc, out, _ = self.check(BEFORE.replace(b"1.0", b"1.1"), status="R090",
                                name="old\nname\t.md")
        self.assertEqual(rc, 1, out)
        self.assertIn("renamed.md", out)

    def test_index_enumeration_failure_is_not_a_pass(self):
        with mock.patch.object(CHECK, "git", side_effect=CHECK.InspectionError("index unreadable")), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(CHECK.main([]), 2)

    def test_unmerged_and_nonregular_entries_refuse(self):
        self.assertEqual(self.check(BEFORE, status="U")[0], 2)
        for mode in ("120000", "160000"):
            with self.subTest(mode=mode), self.assertRaises(CHECK.InspectionError):
                CHECK.read_document((mode, NEW))

    def test_same_day_second_bump_needs_no_cosmetic_date_edit(self):
        before = BEFORE.replace(b"2026-11-23", b"2026-11-24")
        self.assertEqual(self.check(before.replace(b"1.0", b"1.1"), before=before)[0], 0)
        self.assertEqual(self.check(before.replace(b"Date:** ", b"Date:**  "), before=before)[0], 1)

    def test_both_changed_requires_today_not_cosmetic_or_other_date(self):
        for date in (b"2026-11-22", b"2026-11-25", b"2026-11-23  ", b"bad-date"):
            after = BEFORE.replace(b"1.0", b"1.1").replace(b"2026-11-23", date)
            self.assertEqual(self.check(after)[0], 1, date)

    def test_generated_outputs_are_out_of_scope(self):
        for path in CHECK.GENERATED_FILES:
            with self.subTest(path=path):
                self.assertEqual(self.check(BEFORE.replace(b"23", b"24"), name=path)[0], 0)
        self.assertEqual(self.check(BEFORE.replace(b"23", b"24"), name="other/portal.md")[0], 1)

    def test_byte_filenames_preserve_document_checks(self):
        for name in ("space name.md", "line\nbreak.md", "tab\tname.md", "-dash.md", "wild[?]*.md",
                     os.fsdecode(b"byte-\xff.md")):
            with self.subTest(name=name):
                self.assertEqual(self.check(BEFORE, name=name)[0], 0)
                self.assertEqual(self.check(BEFORE.replace(b"1.0", b"1.1"), name=name)[0], 1)
        rc, _, reads = self.check(b"\xff", name=os.fsdecode(b"byte-\xff.txt"))
        self.assertEqual((rc, reads), (0, []))

    def test_listing_error_after_document_names_staged_index(self):
        def entries(*args):
            yield "previous.md", ("100644", OLD), ("100644", NEW)
            raise CHECK.InspectionError("unmerged index entry: conflicted.md")
        output = io.StringIO()
        with mock.patch.object(CHECK, "staged_documents", side_effect=entries), \
                contextlib.redirect_stderr(output):
            self.assertEqual(CHECK.main([]), 2)
        self.assertIn("cannot inspect staged index: unmerged index entry: conflicted.md", output.getvalue())
        self.assertNotIn("previous.md", output.getvalue())

    def test_blob_error_names_actual_document(self):
        rc, out, _ = self.check(BEFORE, name="actual.md", failure=NEW)
        self.assertEqual(rc, 2)
        self.assertIn("cannot inspect 'actual.md':", out)

    def test_hook_checks_documents_without_process_inspection(self):
        with mock.patch.object(CHECK.os, "getppid", side_effect=AssertionError("process access")), \
                mock.patch.object(Path, "read_bytes", side_effect=OSError("no process filesystem")):
            self.assertEqual(self.check(BEFORE)[0], 0)
            self.assertEqual(self.check(BEFORE.replace(b"1.0", b"1.1"))[0], 1)

    def test_empty_index_needs_no_process_inspection(self):
        with mock.patch.object(CHECK, "git", return_value=b"") as git, \
                mock.patch.object(CHECK.os, "getppid", side_effect=AssertionError("process access")), \
                mock.patch.object(Path, "read_bytes", side_effect=OSError("no process filesystem")), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(CHECK.main(["--pre-commit"]), 0)
        git.assert_called_once_with("diff", "--cached", "--raw", "--no-abbrev", "-z",
                                    "--find-renames", "--no-ext-diff", "--no-textconv",
                                    "--no-relative", "--ita-invisible-in-index", "--")

    def test_amend_can_leave_date_only_change_relative_to_parent(self):
        parent = BEFORE
        head = parent.replace(b"1.0", b"1.1").replace(b"2026-11-23", b"2026-11-24")
        amended = head.replace(b"1.1", b"1.0")
        # HEAD is the commit being amended; restoring its parent's Version passes.
        rc, out, reads = self.check(amended, before=head)
        self.assertEqual(rc, 0, out)
        self.assertEqual(reads, [OLD, NEW])
        # The resulting snapshot changes only Date against the parent.
        self.assertEqual(amended, parent.replace(b"2026-11-23", b"2026-11-24"))
        self.assertTrue(CHECK.unpaired(parent.decode(), amended.decode(), "2026-11-24"))

    def test_specification_date_has_no_cosmetic_space(self):
        spec = (TOOLS.parent / "specs/specification-audit-programme.md").read_text()
        self.assertEqual(CHECK.parse_metadata_block(spec).raw_lines["Date"][1],
                         "**Date:** 2026-11-25" + chr(92))

    def test_staged_ownership_excludes_whole_outputs_only(self):
        register = b'[[owned_targets]]\nkind="file"\ntarget="generated.md"\n'
        register += b'[[owned_targets]]\nkind="tree"\ntarget="generated"\n'
        register += b'[[owned_targets]]\nkind="block"\ntarget="authored.md"\n'
        def git(*args):
            if args[0] == "ls-files":
                return f"100644 {OLD} 0\t{CHECK.OWNERSHIP}\0".encode()
            return register
        with mock.patch.object(CHECK, "git", side_effect=git):
            files, trees = CHECK.generated_targets()
        self.assertIn("generated.md", files)
        self.assertNotIn("authored.md", files)
        self.assertEqual(trees, ["generated/"])

    def test_real_head_and_index_pairing_in_both_directions(self):
        # Copy existing history; no fixture creates a commit.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repository"
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
            result = subprocess.run(["bash", "-c", shlex.join([
                "git", "-C", str(ROOT), "clone", "--quiet", "--no-hardlinks",
                "--no-checkout", str(ROOT), str(root)])],
                env=env, capture_output=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)

            def git(*args):
                return subprocess.run(["bash", "-c", shlex.join(["git", "-C", str(root), *args])],
                                      env=env, capture_output=True, check=True, timeout=30).stdout

            git("read-tree", "HEAD")
            name = ".claude/skills/corpus-management/specs/specification-audit-programme.md"
            before = git("show", "HEAD:" + name)
            version_only = re.sub(rb"(?m)^(\*\*Version:\*\* )[^\n]+", rb"\g<1>999.0.0", before, count=1)
            date_only = re.sub(rb"(?m)^(\*\*Date:\*\* )[^\n]+", rb"\g<1>2099-01-01", before, count=1)
            both = re.sub(rb"(?m)^(\*\*Date:\*\* )[^\n]+", rb"\g<1>2099-01-01", version_only, count=1)
            doc = root / name
            doc.parent.mkdir(parents=True)
            with mock.patch.object(CHECK, "ROOT", root), mock.patch.dict(os.environ, env, clear=True), \
                    mock.patch.object(CHECK, "utc_today", return_value="2099-01-01"), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                for content, expected in ((version_only, 1), (date_only, 1), (both, 0),
                                          (before + b"\nBody edit.\n", 0), (before + b"\xff", 2)):
                    doc.write_bytes(content)
                    git("add", "--", name)
                    doc.write_bytes(both)  # A working-tree repair cannot change the outcome.
                    self.assertEqual(CHECK.main([]), expected)
                # Date-only relative to HEAD, but paired with Version relative to its parent.
                doc.write_bytes(date_only)
                git("add", "--", name)
                self.assertEqual(CHECK.main([]), 1)
                self.assertEqual(CHECK.main(["--pre-commit"]), 1)
                for filename in ("space name.md", "tab\tname.md", "line\nname.md",
                                 "-dash.md", "wild[?]*.md", os.fsdecode(b"byte-\xff.md")):
                    git("read-tree", "HEAD")
                    git("update-index", "--force-remove", "--", name)
                    renamed = root / filename
                    renamed.write_bytes(version_only)
                    git("add", "--", ":(literal)" + filename)
                    self.assertEqual(CHECK.main(["--pre-commit"]), 1, filename)
                    renamed.write_bytes(both)
                    git("add", "--", ":(literal)" + filename)
                    self.assertEqual(CHECK.main(["--pre-commit"]), 0, filename)
                    renamed.unlink()
                git("read-tree", "HEAD")
                extra = root / os.fsdecode(b"byte-\xff.txt")
                extra.write_bytes(b"\xff")
                git("add", "--", extra.name)
                self.assertEqual(CHECK.main(["--pre-commit"]), 0)

    def test_real_regeneration_with_staged_bump(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repository"
            shutil.copytree(ROOT, root, symlinks=True)
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
            def git(*args):
                return subprocess.run(["bash", "-c", shlex.join(["git", "-C", str(root), *args])],
                                      env=env, capture_output=True, check=True, timeout=30).stdout
            # Raise the maximum source Date so both generated Dates really change.
            name = "governance/specification-master-project.md"
            doc = root / name
            before = doc.read_bytes()
            doc.write_bytes(re.sub(rb"(?m)^(\*\*Date:\*\* )[^\n]+", rb"\g<1>2099-01-01",
                            re.sub(rb"(?m)^(\*\*Version:\*\* )[^\n]+", rb"\g<1>999.0.0", before)))
            generated_before = {p: git("show", "HEAD:" + p) for p in CHECK.GENERATED_FILES
                                if p.startswith("governance/")}
            for script in ("build-taxonomy.py", "build-portal.py"):
                result = subprocess.run([sys.executable, "-I", str(root / TOOLS.relative_to(ROOT) / script)],
                                        env=env, cwd=root, capture_output=True, timeout=120)
                self.assertEqual(result.returncode, 0, result.stderr)
            for path, old in generated_before.items():
                new = (root / path).read_bytes()
                old_fields = CHECK.parse_metadata_block(old.decode()).fields
                new_fields = CHECK.parse_metadata_block(new.decode()).fields
                self.assertEqual(old_fields["Version"], new_fields["Version"])
                self.assertNotEqual(old_fields["Date"], new_fields["Date"])
            git("add", "--", name, *generated_before, ".claude/skills/corpus-management/data/taxonomy.yml")
            with mock.patch.object(CHECK, "ROOT", root), mock.patch.dict(os.environ, env, clear=True), \
                    mock.patch.object(CHECK, "utc_today", return_value="2099-01-01"), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(CHECK.main([]), 0)

    def test_dispatcher_stops_on_pairing_failure_and_missing_checker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tools = root / TOOLS.relative_to(ROOT)
            tools.mkdir(parents=True)
            (tools / "check-commit-on-main.py").write_text("raise SystemExit(0)\n")
            check = tools / "check-version-date-commit.py"
            check.write_text("raise SystemExit(7)\n")
            (tools / "check-generated-commit.py").write_text("print('UNEXPECTED LATER CHECK')\n")
            bindir = root / "bin"
            bindir.mkdir()
            git = bindir / "git"
            git.write_text("#!/bin/sh\nprintf '%s\\n' " + shlex.quote(str(root)) + "\n")
            git.chmod(0o755)
            env = {**os.environ, "PATH": str(bindir) + os.pathsep + os.environ["PATH"]}
            for expected in (7, 2):
                result = subprocess.run(["sh", str(TOOLS / "git-hooks/pre-commit")], env=env,
                                        capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                self.assertNotIn("UNEXPECTED", result.stdout)
                if check.exists():
                    check.unlink()


class FullRunnerFreshnessTests(unittest.TestCase):
    FIRST = ["lint-document-date-staleness.py", "lint-version-bump-recency.py"]

    def run_runner(self, failure="", fast="0"):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tools = root / TOOLS.relative_to(ROOT)
            tools.mkdir(parents=True)
            shutil.copyfile(TOOLS / "run_all_audits.sh", tools / "run_all_audits.sh")
            bindir = root / "bin"
            bindir.mkdir()
            stub = bindir / "python3"
            stub.write_text("#!" + sys.executable + "\n" +
                            "import os, pathlib, sys\n"
                            "scripts = [a for a in sys.argv[1:] if a.endswith('.py')]\n"
                            "if '-c' in sys.argv:\n"
                            "    print('0' * 32)\n"
                            "    raise SystemExit(0)\n"
                            "name = pathlib.Path(scripts[0]).name\n"
                            "with open(os.environ['GATE_LOG'], 'a') as log: log.write(name + '\\n')\n"
                            "raise SystemExit(7 if name == os.environ['FAILED_GATE'] else 0)\n")
            stub.chmod(0o755)
            log = root / "gates.log"
            env = {**os.environ, "PATH": str(bindir) + os.pathsep + os.environ["PATH"],
                   "GATE_LOG": str(log), "FAILED_GATE": failure, "FAIL_FAST": fast}
            result = subprocess.run(["bash", str(tools / "run_all_audits.sh")], env=env,
                                    capture_output=True, text=True, timeout=60)
            return result, log.read_text().splitlines()

    def test_first_gate_failure_stops_immediately(self):
        result, ran = self.run_runner(self.FIRST[0])
        self.assertEqual(result.returncode, 7, result.stdout + result.stderr)
        self.assertEqual(ran, self.FIRST[:1])

    def test_second_gate_failure_stops_immediately(self):
        result, ran = self.run_runner(self.FIRST[1])
        self.assertEqual(result.returncode, 7, result.stdout + result.stderr)
        self.assertEqual(ran, self.FIRST)

    def test_success_runs_inventory_once_in_order(self):
        result, ran = self.run_runner()
        spec = (TOOLS.parent / "specs/specification-audit-programme.md").read_text()
        inventory = re.findall(r"^\| \d+ \| [^\n]+?\]\(\.\./tools/([^/)]+\.py)\) \|$", spec, re.M)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(ran[:2], self.FIRST)
        self.assertEqual(ran, inventory)
        self.assertEqual(len(ran), len(set(ran)))

    def test_later_failure_still_aggregates_by_default(self):
        result, ran = self.run_runner("lint-metadata.py")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertGreater(len(ran), 3)
        self.assertEqual(ran[:3], self.FIRST + ["lint-metadata.py"])

    def test_later_failure_still_honors_fail_fast(self):
        result, ran = self.run_runner("lint-metadata.py", fast="1")
        self.assertEqual(result.returncode, 7, result.stdout + result.stderr)
        self.assertEqual(ran, self.FIRST + ["lint-metadata.py"])


if __name__ == "__main__":
    unittest.main()
