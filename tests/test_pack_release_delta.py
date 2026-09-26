"""Release-delta fixtures use temporary git repositories and no third-party code."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / ".corpus-management" / "tools"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DELTA = _load("pack_release_delta")
COMPILER = _load("corpus_mgmt_compiler")
MANIFEST = """schema_version = 1
[pack]
version = "1.2.3"
state = "active"
[registers]
clauses = "core/clauses.toml"
id_history = "core/id-history.toml"
ownership = "core/ownership.toml"
gates = "core/gates.toml"
profiles = "core/profiles.toml"
hooks = "core/hooks.toml"
[generation]
ruleset = "gensrc.toml"
[reference_registers]
defaults_root = "defaults"
[release]
waivers = "core/release-waivers.toml"
"""
ENGINE = """KNOWN_KEYS = {"first", "second"}

class Widget:
    def __init__(self, left, right):
        self.left = left

def public(left, right, *, enabled=True):
    gate_keys = {"id", "title"}
    return left

def configure(ref, *, debug=False):
    value = ref.first
    other = getattr(ref, "second", None)
    return value

def _private():
    return 1
"""
REGISTERS = {
    "clauses": ('clauses', 'id', 'alpha',
                'title = "Alpha"\nsource = "core/policies/note.md"\n'),
    "id-history": ('events', 'id', 'alpha', 'event = "created"\n'),
    "ownership": ('owned_targets', 'rule', 'alpha', 'target = "out.md"\nkind = "file"\n'),
    "gates": ('gates', 'id', 'lint-alpha', 'title = "Alpha"\nsource = "tools/engine.py"\n'),
    "profiles": ('profiles', 'id', 'words', 'target = "defaults/words.toml"\ntitle = "Words"\n'),
    "hooks": ('hooks', 'id', 'check-alpha', 'title = "Alpha"\n'),
}


class _Repo:
    def __init__(self, root, version="1.2.3"):
        self.root = root
        self.pack = root / ".corpus-management"
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Release Test")
        self.git("config", "user.email", "release@example.invalid")
        self.write("core/manifest.toml", MANIFEST.replace("1.2.3", version))
        for name, (collection, field, identity, extra) in REGISTERS.items():
            self.write(f"core/{name}.toml",
                       f'schema_version = 1\n[[{collection}]]\n'
                       f'{field} = "{identity}"\n{extra}')
        self.write("defaults/words.toml", 'schema_version = 1\n[words]\nterms = ["alpha"]\n')
        self.write("gensrc.toml", 'schema_version = 1\nsources = ["core/policies/note.md"]\n')
        self.write("core/policies/note.md", "Pack policy.\n")
        self.write("core/rules/alpha.md", "A clause.\n")
        self.write("tools/engine.py", ENGINE)
        self.write("README.md", "Pack readme.\n")
        self.checkpoint()

    def git(self, *args):
        result = subprocess.run(
            ["git", "-C", str(self.root), *args],
            env=self.env, text=True, capture_output=True, check=True,
        )
        return result.stdout.strip()

    def checkpoint(self):
        self.git("add", ".")
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        self.base = self.git("rev-parse", "HEAD")
        self.git("update-ref", "refs/remotes/origin/main", self.base)

    def write(self, rel, text):
        path = self.pack / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def read(self, rel):
        return (self.pack / rel).read_text(encoding="utf-8")

    def replace(self, rel, old, new):
        text = self.read(rel)
        if old not in text:
            raise AssertionError(f"{rel}: missing replacement {old!r}")
        self.write(rel, text.replace(old, new))

    def remove(self, rel):
        (self.pack / rel).unlink()

    def version(self, value):
        data = DELTA.tomllib.loads(self.read("core/manifest.toml"))
        self.replace("core/manifest.toml", f'version = "{data["pack"]["version"]}"',
                     f'version = "{value}"')

    def waiver(self, required="MINOR", before="1.2.3", after="1.2.4"):
        self.write("core/release-waivers.toml", f"""schema_version = 1
[[waiver]]
from = "{before}"
to = "{after}"
required = "{required}"
reason = "Approved fixture re-baseline."
approved_by = "maintainer"
approved = 2026-09-26
decision_ref = "fixture decision"
""")


class ReleaseDeltaTests(unittest.TestCase):
    @contextlib.contextmanager
    def repo(self, version="1.2.3"):
        with tempfile.TemporaryDirectory(prefix="release-delta-") as directory:
            yield _Repo(Path(directory), version)

    def result(self, repo, base=None):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = DELTA.check(repo.root, repo.pack, base)
        return code, output.getvalue()

    def expect(self, repo, floor, code=1, claimed="NONE", base=None):
        actual, output = self.result(repo, base)
        self.assertEqual(actual, code, output)
        self.assertIn(f"FLOOR: {floor}", output)
        self.assertIn(f"CLAIMED: {claimed}", output)
        return output

    def test_no_change_and_explicit_base(self):
        with self.repo() as repo:
            self.expect(repo, "NONE", 0)
            self.expect(repo, "NONE", 0, base=repo.base)

    def test_readme_and_pycache_are_the_only_exclusions(self):
        # 3b81 QA r3: the scope is every pack file except README.md files and __pycache__, so a
        # file reached only through a pack-root or noncanonical reference cannot escape it.
        with self.repo() as repo:
            repo.write("README.md", "Changed.\n")
            repo.write("notes/README.md", "Changed.\n")
            repo.write("tools/__pycache__/engine.cpython-314.pyc", "bytes")
            self.expect(repo, "NONE", 0)
            repo.write("notes/unreferenced.toml", "not even valid TOML")
            self.assertIn("notes/unreferenced.toml", self.expect(repo, "PATCH"))
            repo.write("notes/helper.py", "def run():\n    return 1\n")
            self.assertIn("notes/helper.py", self.expect(repo, "MINOR"))

    def test_patch_surfaces_need_a_bump(self):
        cases = [
            ("core/manifest.toml", 'state = "active"', 'state = "ready"'),
            ("core/policies/note.md", "Pack policy.", "Corrected policy."),
            ("gensrc.toml", "schema_version = 1", "# comment\nschema_version = 1"),
            ("core/clauses.toml", 'title = "Alpha"', 'title = "Corrected"'),
            ("core/gates.toml", 'title = "Alpha"', 'title = "Corrected"'),
            ("core/id-history.toml", 'event = "created"', 'event = "retired"'),
            ("core/ownership.toml", 'target = "out.md"', 'target = "other.md"'),
            ("core/hooks.toml", 'title = "Alpha"', 'title = "Corrected"'),
            ("tools/engine.py", "return 1", "return 2"),
        ]
        for path, old, new in cases:
            with self.subTest(path=path), self.repo() as repo:
                repo.replace(path, old, new)
                output = self.expect(repo, "PATCH")
                if path in ("core/clauses.toml", "core/gates.toml", "core/hooks.toml"):
                    self.assertIn("register value changed", output)
                repo.version("1.2.4")
                self.expect(repo, "PATCH", 0, "PATCH")

    def test_all_register_ids_added_removed_and_renamed(self):
        for name, (collection, field, identity, extra) in REGISTERS.items():
            for action, floor in (("add", "MINOR"), ("remove", "MAJOR"), ("rename", "MAJOR")):
                with self.subTest(register=name, action=action), self.repo() as repo:
                    path = f"core/{name}.toml"
                    if action == "add":
                        repo.write(path, repo.read(path) +
                                   f'\n[[{collection}]]\n{field} = "another"\n{extra}')
                    elif action == "remove":
                        repo.write(path, f"schema_version = 1\n{collection} = []\n")
                    else:
                        repo.replace(path, f'{field} = "{identity}"', f'{field} = "renamed"')
                    self.expect(repo, floor)

    def test_history_multiple_events_keep_one_identity(self):
        with self.repo() as repo:
            path = "core/id-history.toml"
            repo.write(path, repo.read(path) + '\n[[events]]\nid = "alpha"\nevent = "retired"\n')
            self.expect(repo, "PATCH")

    def test_table_keyed_register_and_manifest_union(self):
        with self.repo() as repo:
            repo.replace("core/manifest.toml", "[generation]",
                         'custom = "core/custom.toml"\n[generation]')
            repo.write("core/custom.toml", 'schema_version = 1\n[items.alpha]\nvalue = 1\n')
            repo.checkpoint()
            repo.replace("core/custom.toml", "[items.alpha]", "[items.beta]")
            self.expect(repo, "MAJOR")
        with self.repo() as repo:
            repo.replace("core/manifest.toml", 'hooks = "core/hooks.toml"\n', "")
            self.expect(repo, "MAJOR")
        with self.repo() as repo:
            repo.replace("core/manifest.toml", "[generation]",
                         'custom = "core/custom.toml"\n[generation]')
            repo.write("core/custom.toml", 'schema_version = 1\n[items.alpha]\nvalue = 1\n')
            self.expect(repo, "MINOR")

    def test_register_ambiguity_duplicate_and_missing_file(self):
        cases = [
            ("core/gates.toml", 'schema_version = 1\n[[gates]]\nname = "unknown"\n'),
            ("core/gates.toml", 'schema_version = 1\n[gates.alpha]\nid = "different"\n'),
            ("core/gates.toml", 'schema_version = 1\n[unexpected]\nvalue = 1\n'),
            ("core/gates.toml", 'schema_version = 1\n[[gates]]\nid = "x"\n[[gates]]\nid = "x"\n'),
        ]
        for path, content in cases:
            with self.subTest(content=content), self.repo() as repo:
                repo.write(path, content)
                self.assertEqual(self.result(repo)[0], 2)
        with self.repo() as repo:
            repo.remove("core/gates.toml")
            self.assertEqual(self.result(repo)[0], 2)

    def test_schema_versions(self):
        paths = ["core/manifest.toml", "defaults/words.toml"]
        paths += [f"core/{name}.toml" for name in REGISTERS]
        for path in paths:
            with self.subTest(path=path), self.repo() as repo:
                repo.replace(path, "schema_version = 1", "schema_version = 2")
                self.expect(repo, "MAJOR")

    def test_clause_add_remove_change(self):
        for action, floor in (("add", "MINOR"), ("remove", "MAJOR"), ("edit", "PATCH")):
            with self.subTest(action=action), self.repo() as repo:
                if action == "add":
                    repo.write("core/rules/new.md", "New clause.\n")
                elif action == "remove":
                    repo.remove("core/rules/alpha.md")
                else:
                    repo.write("core/rules/alpha.md", "Changed clause.\n")
                output = self.expect(repo, floor)
                if action == "edit":
                    self.assertIn("strengthening vs clarifying is not machine-decidable", output)

    def test_round_one_refactors_and_scope(self):
        # 3b81 QA r1: renaming a key-set variable or adding a private helper that assigns `keys`
        # is not a configuration change; an engine outside tools/ is classified; the manifest's
        # declared waiver path must be the supported one.
        with self.repo() as repo:
            repo.replace("tools/engine.py", "    gate_keys = ", "    allowed_gate_keys = ")
            repo.replace("tools/engine.py", "def _private():", "def _helper(d):\n    keys = sorted(d)\n    return keys\n\ndef _private():")
            self.expect(repo, "PATCH")
        with self.repo() as repo:
            repo.write("engines/language.py", "def run():\n    return 1\n")
            repo.checkpoint()
            repo.replace("engines/language.py", "def run():", "def _run():")
            self.assertIn("removed run", self.expect(repo, "MAJOR"))
        with self.repo() as repo:
            repo.replace("tools/engine.py", "KNOWN_KEYS = {\"first\", \"second\"}", "KNOWN_KEYS = {\"first\"}")
            self.assertIn("removed second", self.expect(repo, "MAJOR"))
        with self.repo() as repo:
            repo.replace("core/manifest.toml", 'waivers = "core/release-waivers.toml"', 'waivers = "core/other.toml"')
            code, output = self.result(repo)
            self.assertEqual(code, 2, output)
            self.assertIn("[release].waivers must be", output)

    def test_dot_slash_reference_stays_in_scope(self):
        # 3b81 QA r2 (codex): a reference written ./path is the same file to the compiler.
        with self.repo() as repo:
            repo.replace("core/clauses.toml", 'source = "core/policies/note.md"', 'source = "./core/policies/note.md"')
            repo.replace("gensrc.toml", '["core/policies/note.md"]', '["./core/policies/note.md"]')
            repo.checkpoint()
            repo.replace("core/policies/note.md", "Pack policy.", "Changed policy.")
            self.assertIn("core/policies/note.md", self.expect(repo, "PATCH"))

    def test_engine_public_api_and_configuration(self):
        cases = [
            ("def public(", "def _public(", "MAJOR"),
            ("def _private(", "def added(", "MINOR"),
            ("public(left, right,", "public(left,", "MAJOR"),
            ("public(left, right,", "public(left, right, third,", "MINOR"),
            ("class Widget:", "class _Widget:", "MAJOR"),
            ("class Widget:", "class Extra:\n    pass\n\nclass Widget:", "MINOR"),
            ("__init__(self, left, right)", "__init__(self, left)", "MAJOR"),
            ("__init__(self, left, right)", "__init__(self, left, right, extra)", "MINOR"),
            ('{"first", "second"}', '{"first"}', "MAJOR"),
            ('{"first", "second"}', '{"first", "second", "third"}', "MINOR"),
            ('{"id", "title"}', '{"id"}', "MAJOR"),
            ('{"id", "title"}', '{"id", "title", "source"}', "MINOR"),
            ("configure(ref, *, debug=False)", "configure(ref)", "MAJOR"),
            ("configure(ref, *, debug=False)", "configure(ref, *, debug=False, flag=False)", "MINOR"),
            ("value = ref.first", "value = None", "MAJOR"),
            ("value = ref.first", "value = ref.first\n    extra = ref.third", "MINOR"),
            ('getattr(ref, "second", None)', "None", "MAJOR"),
        ]
        for old, new, floor in cases:
            with self.subTest(change=new), self.repo() as repo:
                repo.replace("tools/engine.py", old, new)
                self.expect(repo, floor)
        for old, new, floor in (
            ('ref["first"]', "None", "MAJOR"),
            ('ref["first"]', 'ref["first"] + ref.get("second", "")', "MINOR"),
        ):
            with self.subTest(change=new), self.repo() as repo:
                repo.write("tools/engine.py", 'def configure(ref):\n    return ref["first"]\n')
                repo.checkpoint()
                repo.replace("tools/engine.py", old, new)
                self.expect(repo, floor)

    def test_new_and_removed_engine_files(self):
        with self.repo() as repo:
            repo.write("tools/new.py", "def new():\n    return None\n")
            self.expect(repo, "MINOR")
        with self.repo() as repo:
            repo.remove("tools/engine.py")
            self.expect(repo, "MAJOR")
        with self.repo() as repo:
            repo.write("tools/private.py", "def _helper():\n    pass\n")
            self.expect(repo, "PATCH")

    def test_engine_input_errors(self):
        for content in ("def broken(", 'ACCEPTED_KEYS = compute_keys()\n'):
            with self.subTest(content=content), self.repo() as repo:
                repo.write("tools/engine.py", content)
                self.assertEqual(self.result(repo)[0], 2)

    def test_profile_values_and_keys(self):
        cases = [
            ("defaults/words.toml", 'terms = ["alpha"]', 'terms = ["beta"]', "MINOR"),
            ("defaults/words.toml", 'terms = ["alpha"]', "", "MAJOR"),
            ("defaults/words.toml", 'terms = ["alpha"]', 'terms = ["alpha"]\nextra = []', "MINOR"),
            ("core/profiles.toml", 'title = "Words"', 'title = "Corrected"', "MINOR"),
            ("core/profiles.toml", 'title = "Words"', "", "MAJOR"),
            ("core/profiles.toml", 'title = "Words"', 'title = "Words"\nnote = "Extra"', "MINOR"),
        ]
        for path, old, new, floor in cases:
            with self.subTest(change=new), self.repo() as repo:
                repo.replace(path, old, new)
                self.expect(repo, floor)

    def test_zero_major_breaking_and_stable_major(self):
        for version, code, claimed in (
            ("0.6.1", 1, "PATCH"), ("0.7.0", 0, "MINOR"), ("1.0.0", 0, "MAJOR"),
        ):
            with self.subTest(version=version), self.repo("0.6.0") as repo:
                repo.replace("tools/engine.py", "def public(", "def _public(")
                repo.version(version)
                output = self.expect(repo, "MAJOR", code, claimed)
                self.assertIn("BREAKING", output)
        with self.repo() as repo:
            repo.replace("tools/engine.py", "def public(", "def _public(")
            repo.version("1.3.0")
            self.expect(repo, "MAJOR", 1, "MINOR")
            repo.version("2.0.0")
            self.expect(repo, "MAJOR", 0, "MAJOR")

    def test_version_decrease_and_strict_versions(self):
        with self.repo() as repo:
            repo.version("1.2.2")
            output = self.expect(repo, "PATCH", 1, "DECREASE")
            self.assertIn("version decreased", output)
        # A waiver row that does not move the version up is refused outright: an equal or
        # backward row would waive every later unbumped change (3b81 QA r1).
        for after in ("1.2.3", "1.2.2"):
            with self.subTest(after=after), self.repo() as repo:
                repo.replace("tools/engine.py", "return 1", "return 2")
                repo.waiver("PATCH", after=after)
                code, output = self.result(repo)
                self.assertEqual(code, 2, output)
                self.assertIn("to must be greater than from", output)
        for value in ("1.2", "01.2.3", "1.2.3-rc1", "1.2.3+build"):
            with self.subTest(value=value), self.repo() as repo:
                repo.version(value)
                self.assertEqual(self.result(repo)[0], 2)

    def test_matching_waiver_and_rebaseline(self):
        for before, after in (("1.2.3", "1.2.4"), ("0.6.0", "0.6.80")):
            with self.subTest(before=before), self.repo(before) as repo:
                repo.write("tools/new.py", "def check():\n    pass\n")
                repo.version(after)
                repo.waiver(before=before, after=after)
                self.assertIn("WAIVED", self.expect(repo, "MINOR", 0, "PATCH"))

    def test_mismatching_waivers(self):
        for options in (
            {"before": "1.2.2"}, {"after": "1.2.5"}, {"required": "PATCH"},
        ):
            with self.subTest(options=options), self.repo() as repo:
                repo.write("core/rules/new.md", "New.\n")
                repo.version("1.2.4")
                repo.waiver(**options)
                self.assertNotIn("WAIVED", self.expect(repo, "MINOR", 1, "PATCH"))

    def test_malformed_waivers_fail_closed(self):
        cases = [
            ("schema_version = 1", "schema_version = true"),
            ("schema_version = 1", "schema_version = 2"),
            ('from = "1.2.3"', 'from = "1.2"'),
            ('to = "1.2.4"', "to = 12"),
            ('required = "MINOR"', 'required = "NONE"'),
            ('reason = "Approved fixture re-baseline."', 'reason = ""'),
            ('approved_by = "maintainer"', 'approved_by = "reviewer"'),
            ("approved = 2026-09-26", 'approved = "2026-09-26"'),
            ("approved = 2026-09-26", "approved = 2026-09-26T00:00:00Z"),
            ('decision_ref = "fixture decision"', 'decision_ref = " "'),
            ('decision_ref = "fixture decision"', ""),
            ('decision_ref = "fixture decision"', 'decision_ref = "fixture decision"\nextra = 1'),
            ("schema_version = 1", "schema_version = 1\nextra = 1"),
            ("[[waiver]]", "[waiver]"),
        ]
        for old, new in cases:
            with self.subTest(change=new), self.repo() as repo:
                repo.waiver()
                repo.replace("core/release-waivers.toml", old, new)
                self.assertEqual(self.result(repo)[0], 2)

    def test_unresolvable_base(self):
        with self.repo() as repo:
            code, output = self.result(repo, "no-such-ref")
            self.assertEqual(code, 2)
            self.assertIn("cannot resolve release base", output)
            repo.git("update-ref", "-d", "refs/remotes/origin/main")
            code, output = self.result(repo)
            self.assertEqual(code, 2)
            self.assertIn("origin/main", output)
            self.expect(repo, "NONE", 0, base=repo.base)

    def test_head_is_disk_not_index_or_commit(self):
        with self.repo() as repo:
            repo.replace("core/rules/alpha.md", "A clause.", "Staged clause.")
            repo.git("add", ".")
            repo.write("core/rules/alpha.md", "A clause.\n")
            self.expect(repo, "NONE", 0)
            repo.write("core/rules/alpha.md", "Unstaged clause.\n")
            self.expect(repo, "PATCH")
        with self.repo() as repo:
            repo.write("core/rules/new.md", "Committed on branch.\n")
            repo.git("add", ".")
            repo.git("-c", "commit.gpgsign=false", "commit", "-qm", "branch")
            self.expect(repo, "MINOR")

    def test_mode_only_change(self):
        with self.repo() as repo:
            path = repo.pack / "tools/engine.py"
            path.chmod(path.stat().st_mode | 0o100)
            self.expect(repo, "PATCH")

    def test_compiler_modes_are_read_only_and_combine_failures(self):
        with self.repo() as repo:
            args = ["--root", str(repo.root), "--release-delta", "--base", repo.base]
            with patch.dict(sys.modules, {"pack_release_delta": DELTA}), \
                    patch.object(COMPILER, "_ensure_aiqt", return_value=None) as aiqt, \
                    patch.object(COMPILER, "load_and_validate", return_value=([], [])), \
                    patch.object(COMPILER, "run_check", return_value=[]) as drift, \
                    patch.object(COMPILER, "plan_generate", side_effect=AssertionError("write")), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(COMPILER.main(args), 0)
                aiqt.assert_not_called()
                self.assertEqual(COMPILER.main(args + ["--check"]), 0)
                repo.write("core/rules/new.md", "New.\n")
                self.assertEqual(COMPILER.main(args + ["--check"]), 1)
                drift.return_value = ["fixture drift"]
                repo.version("1.3.0")
                self.assertEqual(COMPILER.main(args + ["--check"]), 1)
                drift.return_value = []
                self.assertEqual(COMPILER.main(args + ["--check"]), 0)
                repo.write("core/release-waivers.toml", "invalid TOML")
                self.assertEqual(COMPILER.main(args + ["--check"]), 2)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            COMPILER.main(["--base", "HEAD", "--check"])
        self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
