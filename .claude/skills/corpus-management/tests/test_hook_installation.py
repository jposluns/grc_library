"""Installer self-tests invoke installed shims without creating commits."""

import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[4]
TOOLS = Path(".claude/skills/corpus-management/tools")
HOOKS = ("pre-commit", "commit-msg")


def old_shim(name):
    title = "commit-on-main pre-commit" if name == "pre-commit" else "version-bump commit-msg"
    local = ('hooks="$(git rev-parse --git-path hooks)"\n'
             'if [ -x "$hooks/commit-msg-local" ]; then "$hooks/commit-msg-local" "$@"; fi\n'
             if name == "commit-msg" else "")
    return (f"#!/bin/sh\n# Managed by {TOOLS}/install-git-hooks.sh: {title} dispatcher v1.\n"
            f'set -eu\n{local}root="$(git rev-parse --show-toplevel)"\n'
            f'[ -f "$root/{TOOLS}/git-hooks/{name}" ] || exit 0\n'
            f'exec sh "$root/{TOOLS}/git-hooks/{name}" "$@"\n')


class HookInstallationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="hook-install-")
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo with spaces"
        self.repo.mkdir()
        self.env = {k: v for k, v in os.environ.items()
                    if not k.startswith(("GIT_", "GRC_"))}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.command("bash", "-c", shlex.join(["git", "-C", str(self.repo), "init", "-q"]))
        self.hooks = self.repo / ".git/hooks"
        (self.repo / TOOLS).mkdir(parents=True)
        shutil.copyfile(ROOT / TOOLS / "install-git-hooks.sh",
                        self.repo / TOOLS / "install-git-hooks.sh")

    def command(self, *args, code=0):
        result = subprocess.run(args, cwd=self.repo, env=self.env,
                                text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result

    def install(self, code=0):
        return self.command("sh", str(self.repo / TOOLS / "install-git-hooks.sh"), code=code)

    def invoke(self, name, code=0):
        return self.command(str(self.hooks / name), "message with spaces", code=code)

    def dispatcher(self, name, code=0):
        target = self.repo / TOOLS / "git-hooks" / name
        target.parent.mkdir(exist_ok=True)
        target.write_text(f'#!/bin/sh\nprintf "%s\\n" "$1"\nexit {code}\n')
        return target

    def assert_missing(self, name):
        result = self.invoke(name, code=1)
        self.assertIn(f"{name}: missing tracked dispatcher:", result.stderr)
        self.assertIn(str(self.repo / TOOLS / "git-hooks" / name), result.stderr)

    def test_fresh_shims_refuse_missing_dispatchers(self):
        self.install()
        for name in HOOKS:
            with self.subTest(hook=name):
                self.assert_missing(name)

    def test_dispatchers_forward_arguments_and_failure(self):
        self.install()
        for name in HOOKS:
            with self.subTest(hook=name):
                self.dispatcher(name)
                self.assertEqual(self.invoke(name).stdout, "message with spaces\n")
                self.dispatcher(name, code=7)
                self.invoke(name, code=7)

    def test_removed_dispatchers_refuse(self):
        self.install()
        for name in HOOKS:
            with self.subTest(hook=name):
                target = self.dispatcher(name)
                self.invoke(name)
                target.unlink()
                self.assert_missing(name)

    def test_exact_old_shims_upgrade_and_are_idempotent(self):
        for name in HOOKS:
            (self.hooks / name).write_text(old_shim(name))
        result = self.install()
        self.assertEqual(result.stdout.count("upgraded:"), 2)
        installed = {name: (self.hooks / name).read_bytes() for name in HOOKS}
        self.install()
        for name in HOOKS:
            with self.subTest(hook=name):
                self.assertEqual((self.hooks / name).read_bytes(), installed[name])
                self.assertTrue(os.access(self.hooks / name, os.X_OK))
                self.assert_missing(name)
                self.dispatcher(name, code=9)
                self.invoke(name, code=9)

    def test_altered_old_shims_are_not_overwritten(self):
        for name in HOOKS:
            (self.hooks / name).write_text(old_shim(name) + "# local change\n")
        before = {name: (self.hooks / name).read_bytes() for name in HOOKS}
        self.install(code=1)
        for name in HOOKS:
            self.assertEqual((self.hooks / name).read_bytes(), before[name])

    def test_old_shim_symlinks_are_not_followed(self):
        for name in HOOKS:
            target = self.repo / (name + "-target")
            target.write_text(old_shim(name))
            (self.hooks / name).symlink_to(target)
        self.install(code=1)
        for name in HOOKS:
            self.assertTrue((self.hooks / name).is_symlink())
            self.assertEqual((self.hooks / name).read_text(), old_shim(name))

    def test_foreign_framework_hook_and_legacy_are_preserved(self):
        hook = self.hooks / "pre-commit"
        legacy = self.hooks / "pre-commit.legacy"
        hook.write_text("#!/bin/sh\nexit 0\n")
        legacy.write_text(old_shim("pre-commit"))
        result = self.install(code=1)
        self.assertIn("pre-commit uninstall", result.stderr)
        self.assertIn("stale (v1) and fails open", result.stderr)
        self.assertIn("NOTE: a managed hook is present", result.stderr)
        self.assertIn("cannot be verified from file contents", result.stderr)
        self.assertEqual(hook.read_text(), "#!/bin/sh\nexit 0\n")
        self.assertEqual(legacy.read_text(), old_shim("pre-commit"))
        # Model the documented framework uninstall restoring the managed shim.
        hook.unlink()
        legacy.rename(hook)
        self.install()
        self.assert_missing("pre-commit")

    def test_current_framework_legacy_keeps_chain_note(self):
        self.install()
        hook = self.hooks / "pre-commit"
        legacy = self.hooks / "pre-commit.legacy"
        hook.rename(legacy)
        managed = legacy.read_bytes()
        hook.write_text("#!/bin/sh\nexit 0\n")
        result = self.install(code=1)
        self.assertIn("NOTE: a managed hook is present", result.stderr)
        self.assertIn("cannot be verified from file contents", result.stderr)
        self.assertNotIn("stale (v1)", result.stderr)
        self.assertEqual(legacy.read_bytes(), managed)
        self.assertEqual(hook.read_text(), "#!/bin/sh\nexit 0\n")

    def test_local_commit_msg_runs_first_and_its_failure_propagates(self):
        local = self.hooks / "commit-msg-local"
        for old in (False, True):
            with self.subTest(upgrade=old):
                if old:
                    (self.hooks / "commit-msg").write_text(old_shim("commit-msg"))
                self.install()
                local.write_text('#!/bin/sh\necho local-first\nexit 0\n')
                local.chmod(0o755)
                result = self.invoke("commit-msg", code=1)
                self.assertEqual(result.stdout, "local-first\n")
                self.assertIn("missing tracked dispatcher", result.stderr)
                local.write_text('#!/bin/sh\nexit 8\n')
                self.invoke("commit-msg", code=8)

    def test_failed_upgrade_preserves_old_shims_and_cleans_temps(self):
        for name in HOOKS:
            (self.hooks / name).write_text(old_shim(name))
        bindir = self.repo / "bin"
        bindir.mkdir()
        mover = bindir / "mv"
        mover.write_text("#!/bin/sh\nexit 1\n")
        mover.chmod(0o755)
        self.env["PATH"] = str(bindir) + os.pathsep + self.env["PATH"]
        result = self.install(code=1)
        self.assertEqual(result.stderr.count("could not upgrade"), 2)
        for name in HOOKS:
            self.assertEqual((self.hooks / name).read_text(), old_shim(name))
            self.assertEqual(list(self.hooks.glob("." + name + ".*")), [])

    def test_directory_and_dangling_symlink_are_refused(self):
        (self.hooks / "pre-commit").mkdir()
        (self.hooks / "commit-msg").symlink_to(self.repo / "absent")
        self.install(code=1)
        self.assertTrue((self.hooks / "pre-commit").is_dir())
        self.assertTrue((self.hooks / "commit-msg").is_symlink())


if __name__ == "__main__":
    unittest.main()
