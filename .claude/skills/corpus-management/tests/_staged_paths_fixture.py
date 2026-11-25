"""Scope setup for older, synthetic tests of OTHER native commit checks.

Only install() injects this helper into an isolated fixture. Those tests vary the
index to exercise their own gate; automatically declaring that fixture index
keeps the real staged-path check in the chain without changing their predicate.
Production hooks never call this helper. DeclaredStagedPathsTests tests explicit
scope declarations, missing declarations and mismatches without this setup.
"""

import importlib.util
from pathlib import Path
import shutil

TOOLS = Path(".claude/skills/corpus-management/tools")


def install(src, repo):
    target = repo / TOOLS
    shutil.copy2(src / TOOLS / "check-staged-paths.py", target / "check-staged-paths.py")
    shutil.copy2(Path(__file__), target / "_declare_staged_fixture.py")
    hook = target / "git-hooks/pre-commit"
    text = hook.read_text()
    # These fixtures test older policies, including metadata edits that the
    # pairing policy now rejects independently. Keep their original assertions
    # and chain intact; test_commit_metadata.py exercises the added dispatcher
    # step separately, including failure and missing-checker propagation.
    pairing = ('python3 -I "$root/.claude/skills/corpus-management/tools/'
               'check-version-date-commit.py" --pre-commit || exit $?\n')
    if text.count(pairing) != 1:
        raise AssertionError("Version-Date fixture hook anchor changed")
    text = text.replace(pairing, "")
    anchor = "# Mandatory: a missing checker or declaration refuses, including an empty index."
    if text.count(anchor) != 1:
        raise AssertionError("staged-path fixture hook anchor changed")
    text = text.replace(anchor, '# Synthetic fixture scope for a different check.\n'
                        'python3 -I "$root/.claude/skills/corpus-management/tools/'
                        '_declare_staged_fixture.py" || exit $?\n' + anchor)
    hook.write_text(text)


def declare_fixture():
    spec = importlib.util.spec_from_file_location(
        "fixture_staged_paths", Path(__file__).with_name("check-staged-paths.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    root, path, head = module.context()
    module.declare(path, head, sorted(module.staged_paths(root)))


if __name__ == "__main__":
    declare_fixture()
