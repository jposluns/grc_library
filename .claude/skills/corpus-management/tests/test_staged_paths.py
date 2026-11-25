"""Declared staged-path tests use real indexes and invoke hooks without commits."""

import ast
import importlib.util
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[4]
TOOLS = Path(".claude/skills/corpus-management/tools")
CHECK = TOOLS / "check-staged-paths.py"
HOOK = TOOLS / "git-hooks/pre-commit"


class DeclaredStagedPathsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="declared-paths-")
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo with space"
        self.repo.mkdir()
        self.env = {k: v for k, v in os.environ.items()
                    if not k.startswith("GIT_") and not k.startswith("GRC_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_TERMINAL_PROMPT="0")
        self.git("init", "-q", "-b", "feature")
        for rel in (CHECK, HOOK, TOOLS / "check-commit-on-main.py",
                    TOOLS / "install-git-hooks.sh"):
            target = self.repo / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, target)
        for name in ("check-version-date-commit.py", "aiqt_bootstrap.py", "aiqt_rules.py"):
            shutil.copy2(ROOT / TOOLS / name, self.repo / TOOLS / name)
        shutil.copytree(ROOT / ".claude/aiqt", self.repo / ".claude/aiqt")
        spec = importlib.util.spec_from_file_location("staged_paths", self.repo / CHECK)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.declaration = self.repo / ".git/grc-staged-paths.json"

    def run_command(self, args, *, extra=None, cwd=None, data=None):
        return subprocess.run(args, cwd=cwd or self.repo,
                              env={**self.env, **(extra or {})}, input=data,
                              capture_output=True, timeout=30)

    def git(self, *args, extra=None):
        cp = self.run_command(["bash", "-c", shlex.join(
            ["git", "-C", str(self.repo), *map(str, args)])], extra=extra)
        self.assertEqual(cp.returncode, 0, cp.stderr)
        return cp.stdout

    def write(self, name, data="content\n"):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data)

    def declare(self, *paths, extra=None, cwd=None):
        cp = self.run_command([sys.executable, "-I", str(self.repo / CHECK),
                               "--declare", "--", *paths], extra=extra, cwd=cwd)
        self.assertEqual(cp.returncode, 0, cp.stderr)

    def check(self, expected, text=None, extra=None, hook=False):
        args = (["sh", str(self.repo / HOOK)] if hook else
                [sys.executable, "-I", str(self.repo / CHECK), "--pre-commit"])
        cp = self.run_command(args, extra=extra)
        self.assertEqual(cp.returncode, expected, cp.stderr)
        if text:
            self.assertIn(text.encode(), cp.stderr)
        return cp

    def test_missing_empty_and_malformed_declarations_fail_closed(self):
        self.check(1, "--declare --", hook=True)
        for payload in (b"", b"{", b"[]", b'{"paths":[]}',
                        b'{"head":null,"paths":[],"extra":true}',
                        b'{"head":null,"paths":["a","a"]}',
                        b'{"head":null,"paths":["unexpected"],"paths":[]}'):
            with self.subTest(payload=payload):
                self.declaration.write_bytes(payload)
                self.check(1, "REFUSING")
        self.declare()
        self.check(0, hook=True)
        self.declaration.write_bytes(b" " * (self.mod.LIMIT + 1))
        self.check(1, "size limit")

    def test_declaration_read_and_incomplete_git_output_fail_closed(self):
        from contextlib import ExitStack, redirect_stdout, redirect_stderr
        import io
        from unittest.mock import patch

        for failure, message in (("unreadable", "permission denied"),
                                 ("invalid_utf8", "utf-8"),
                                 ("incomplete_paths", "incomplete path list")):
            with self.subTest(failure=failure), ExitStack() as stack:
                self.declare("wanted")
                stack.enter_context(patch.object(
                    self.mod, "context", return_value=(self.repo, self.declaration, None)))
                if failure == "unreadable":
                    opened = stack.enter_context(patch.object(
                        self.mod.os, "open", side_effect=PermissionError("permission denied")))
                elif failure == "invalid_utf8":
                    self.declaration.write_bytes(b'{"head":null,"paths":["\xff"]}')
                else:
                    # Matching names without the final NUL must still refuse.
                    git = stack.enter_context(patch.object(
                        self.mod, "git", side_effect=[b"", b"wanted"]))
                out, err = io.StringIO(), io.StringIO()
                with redirect_stdout(out), redirect_stderr(err):
                    self.assertEqual(self.mod.main(["--pre-commit"]), 1)
                self.assertEqual(out.getvalue(), "")
                self.assertIn("REFUSING", err.getvalue())
                self.assertIn(message, err.getvalue())
                if failure == "unreadable":
                    self.assertEqual(opened.call_args.args[0], self.declaration)
                elif failure == "incomplete_paths":
                    self.assertEqual(git.call_count, 2)
        self.declare()
        self.check(0)

    def test_exact_extra_missing_scope_flips(self):
        self.write("wanted")
        self.write("other")
        self.declare("wanted")
        self.check(1, "declared paths not staged")
        self.git("add", "--", "wanted")
        self.check(0, hook=True)
        self.git("add", "--", "other")
        self.check(1, "undeclared staged paths", hook=True)
        self.declare("wanted", "other")
        self.check(0, hook=True)
        self.git("rm", "--cached", "--", "other")
        self.check(1, "declared paths not staged", hook=True)
        self.declare("wanted")
        self.check(0, hook=True)

    def test_direct_script_heredoc_and_subprocess_routes(self):
        # Ignore the checker files so a real root sweep stages just these two
        # authored files. Keep the scripts outside the swept worktree.
        (self.repo / ".git/info/exclude").write_text(".claude/\n")
        spec = importlib.util.spec_from_file_location(
            "bulk_command_guard", ROOT / ".claude/hooks/block-bulk-git-add.py")
        bulk = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bulk)
        for route in ("direct", "script", "heredoc", "heredoc-script", "subprocess"):
            with self.subTest(route=route):
                self.git("read-tree", "--empty")
                self.write("wanted")
                self.write("other")
                self.declare("wanted")
                command = shlex.join(["git", "-C", str(self.repo), "add", "-A"])
                if route == "direct":
                    args, data = ["bash", "-c", command], None
                elif route == "script":
                    script = Path(self.tmp.name) / "stage.sh"
                    script.write_text(command + "\n")
                    args, data = ["sh", str(script)], None
                elif route in ("heredoc", "heredoc-script"):
                    body = command
                    if route == "heredoc-script":
                        script = Path(self.tmp.name) / "stage.sh"
                        script.write_text(command + "\n")
                        body = shlex.join(["sh", str(script)])
                    args, data = ["bash", "-c", "sh <<'STAGE'\n" + body + "\nSTAGE\n"], None
                else:
                    script = Path(self.tmp.name) / "stage.py"
                    script.write_text("import subprocess\nsubprocess.run(" +
                                      repr(["bash", "-c", command]) + ", check=True)\n")
                    args, data = [sys.executable, "-I", str(script)], None
                command_text = args[2] if route in ("direct", "heredoc", "heredoc-script") else shlex.join(args)
                # The existing parser already recognizes this literal shell heredoc.
                if route in ("direct", "heredoc"):
                    self.assertIsNotNone(bulk.refusal(command_text))
                else:
                    self.assertIsNone(bulk.refusal(command_text))
                cp = self.run_command(args, data=data)
                self.assertEqual(cp.returncode, 0, cp.stderr)
                self.check(1, "undeclared staged paths", hook=True)
                self.declare("wanted", "other")
                self.check(0, hook=True)

    def test_literal_names_and_subdirectory_declaration(self):
        paths = ["space name", "line\nbreak", "tab\tname", 'quote"name',
                 "café", "-dash", ":(glob)*", "dir/child", os.fsdecode(b"byte-\xff"),
                 os.fsdecode(b"byte-\xff.txt"), os.fsdecode(b"byte-\xff.md")]
        for path in paths:
            self.write(path)
        self.git("--literal-pathspecs", "add", "--", *paths)
        self.declare(*paths, cwd=self.repo / "dir")
        self.check(0)
        self.check(0, hook=True)
        self.declare("dir")
        self.check(1, "staged paths differ")
        self.declare("*")
        self.check(1, "staged paths differ")

    def test_invalid_declarations_and_strict_cli(self):
        for paths in (["/absolute"], ["../outside"], ["./name"], ["a//b"],
                      ["a/../b"], ["a/"], [""], ["a", "a"], ["a\0b"], [1], "a"):
            with self.subTest(paths=paths):
                with self.assertRaises((ValueError, TypeError)):
                    self.mod.validate_paths(paths)
        for args in ([], ["--pre-commit", "extra"], ["--declare"], ["--declare", "a"]):
            cp = self.run_command([sys.executable, "-I", str(self.repo / CHECK), *args])
            self.assertEqual(cp.returncode, 2, cp.stderr)

    def test_existing_corrupt_head_is_not_an_unborn_branch(self):
        self.declare()
        before = self.declaration.read_bytes()
        ref = self.repo / ".git/refs/heads/feature"
        ref.write_text("1" * 40 + "\n")
        cp = self.run_command([sys.executable, "-I", str(self.repo / CHECK),
                               "--declare", "--"])
        self.assertEqual(cp.returncode, 1, cp.stderr)
        self.assertIn(b"HEAD could not be read", cp.stderr)
        self.assertEqual(self.declaration.read_bytes(), before)
        self.check(1, "HEAD could not be read")
        ref.unlink()
        self.check(0)

    def test_intent_to_add_is_not_staged_content(self):
        self.write("planned")
        self.git("add", "--intent-to-add", "--", "planned")
        # Some Git versions already hide intent-to-add by default. Supply the
        # opposite default first so the check must explicitly choose invisibility.
        # Both controls still use the real index and real Git diff output.
        self.assertEqual(self.git("diff", "--cached", "--name-only",
                                  "--ita-visible-in-index", "--"), b"planned\n")
        from unittest.mock import patch
        real_git = self.mod.git

        def visible_default(root, *args):
            if args[0] == "diff":
                args = (args[0], "--ita-visible-in-index", *args[1:])
            return real_git(root, *args)

        with patch.object(self.mod, "git", visible_default):
            self.assertEqual(self.mod.staged_paths(self.repo), set())
        self.declare()
        self.check(0, hook=True)
        self.declare("planned")
        self.check(1, "declared paths not staged", hook=True)
        self.git("add", "--", "planned")
        self.check(0, hook=True)

    def test_effective_index_selection(self):
        self.write("ordinary")
        self.write("temporary")
        self.git("add", "--", "ordinary")
        other = {"GIT_INDEX_FILE": str(Path(self.tmp.name) / "temporary-index")}
        self.git("add", "--", "temporary", extra=other)
        self.declare("temporary")
        self.check(0, extra=other, hook=True)
        self.check(1, "ordinary", hook=True)
        self.declare("ordinary")
        self.check(0, hook=True)
        self.check(1, "temporary", extra=other, hook=True)

    def test_unmerged_index_and_git_error_refuse(self):
        self.write("conflict")
        blob = self.git("hash-object", "-w", "--", "conflict").strip().decode()
        cp = self.run_command(["bash", "-c", shlex.join(
            ["git", "-C", str(self.repo), "update-index", "--index-info"])],
            data=(f"100644 {blob} 1\tconflict\n100644 {blob} 2\tconflict\n").encode())
        self.assertEqual(cp.returncode, 0, cp.stderr)
        self.declare("conflict")
        self.check(1, "unresolved merge entries")
        (self.repo / ".git/index").write_bytes(b"corrupt index")
        self.check(1, "REFUSING")

    def test_declaration_link_and_nonregular_refusal(self):
        self.declare()
        data = self.declaration.read_bytes()
        self.declaration.unlink()
        target = Path(self.tmp.name) / "outside"
        target.write_bytes(data)
        self.declaration.symlink_to(target)
        self.check(1)
        self.declaration.unlink()
        os.link(target, self.declaration)
        self.check(1, "one link")
        self.declaration.unlink()
        self.declaration.mkdir()
        self.check(1)
        self.declaration.rmdir()
        os.mkfifo(self.declaration)
        self.check(1, "regular file")

    def test_stale_declaration(self):
        self.declare()
        obj = json.loads(self.declaration.read_text())
        obj["head"] = "0" * 40
        self.declaration.write_text(json.dumps(obj))
        self.check(1, "HEAD changed")
        self.declare()
        self.check(0)

    def test_installed_dispatcher_and_missing_checker(self):
        cp = self.run_command(["sh", str(self.repo / TOOLS / "install-git-hooks.sh")])
        self.assertEqual(cp.returncode, 0, cp.stderr)
        installed = self.repo / ".git/hooks/pre-commit"
        cp = self.run_command(["sh", str(installed)])
        self.assertEqual(cp.returncode, 1, cp.stderr)
        self.assertIn(b"--declare --", cp.stderr)
        self.declare()
        cp = self.run_command(["sh", str(installed)])
        self.assertEqual(cp.returncode, 0, cp.stderr)
        (self.repo / CHECK).unlink()
        cp = self.run_command(["sh", str(installed)])
        self.assertNotEqual(cp.returncode, 0)

    def test_existing_checks_still_precede_staged_paths(self):
        for name in ("check-generated-commit.py", "check-changelog-preflight-commit.py"):
            with self.subTest(name=name):
                path = self.repo / TOOLS / name
                path.write_text("import sys\nprint('existing check refused', file=sys.stderr)\nsys.exit(7)\n")
                self.check(7, "existing check refused", hook=True)
                path.unlink()
        self.git("symbolic-ref", "HEAD", "refs/heads/main")
        self.check(1, "check-commit-on-main", hook=True)

    def test_born_head_rename_deletion_and_linked_worktree(self):
        # Clone existing history, never create commits. Keep the index at HEAD;
        # no checkout is needed to test its staged delta.
        clone = Path(self.tmp.name) / "existing history"
        cp = self.run_command(["bash", "-c", shlex.join([
            "git", "-C", str(ROOT), "clone", "--quiet", "--no-hardlinks",
            "--no-checkout", str(ROOT), str(clone)])])
        self.assertEqual(cp.returncode, 0, cp.stderr)
        self.repo = clone
        (clone / CHECK).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / CHECK, clone / CHECK)
        self.git("read-tree", "HEAD")
        original = self.git("show", "HEAD:README.md")
        (clone / "renamed.md").write_bytes(original)
        self.git("update-index", "--force-remove", "--", "README.md")
        self.git("add", "--", "renamed.md")
        self.declare("renamed.md")
        self.check(1, "README.md")
        self.declare("README.md", "renamed.md")
        self.check(0)
        self.git("update-index", "--force-remove", "--", "renamed.md")
        self.declare("README.md")
        self.check(0)
        self.declare()
        self.check(1, "README.md")
        self.declare("README.md")
        linked = Path(self.tmp.name) / "linked tree"
        self.git("worktree", "add", "--quiet", "--detach", str(linked), "HEAD")
        shutil.copy2(ROOT / CHECK, linked / CHECK)
        self.repo = linked
        self.check(1, "--declare --")
        self.declare()
        self.check(0)
        common_declaration = json.loads((clone / ".git/grc-staged-paths.json").read_text())
        self.assertEqual(common_declaration["paths"], ["README.md"])
        self.repo = clone
        self.check(0)

    def test_legacy_fixture_adaptation_keeps_real_check(self):
        import runpy
        helper = ROOT / TOOLS.parent / "tests/_staged_paths_fixture.py"
        runpy.run_path(str(helper))["install"](ROOT, self.repo)
        self.write("fixture-file")
        self.git("add", "--", "fixture-file")
        self.check(0, hook=True)
        self.assertEqual(json.loads(self.declaration.read_text())["paths"], ["fixture-file"])
        # This fixture-only helper does not alter the production hook.
        self.assertNotIn("_declare_staged_fixture.py", (ROOT / HOOK).read_text())
        (self.repo / CHECK).unlink()
        cp = self.run_command(["sh", str(self.repo / HOOK)])
        self.assertNotEqual(cp.returncode, 0)

    def test_each_command_hook_discloses_residual(self):
        names = ("block-bulk-git-add.py", "block-unbumped-version-commit.py",
                 "block-verification-pipes.py", "block-stdin-interpreter.py",
                 "block-repeated-tool-failure.py")
        reference = (ROOT / TOOLS.parent / "docs/guide-command-text-hooks.md").read_text()
        for name in names:
            with self.subTest(name=name):
                doc = ast.get_docstring(ast.parse((ROOT / ".claude/hooks" / name).read_text()))
                for phrase in ("script file", "heredoc fed to a shell", "subprocess"):
                    self.assertIn(phrase, doc)
                self.assertIn("`" + name + "`", reference)


if __name__ == "__main__":
    unittest.main()
