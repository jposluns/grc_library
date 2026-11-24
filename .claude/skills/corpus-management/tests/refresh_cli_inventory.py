#!/usr/bin/env python3
"""Refresh existing CLI inventory pins after reviewing the named files.

Usage: python3 -I .claude/skills/corpus-management/tests/refresh_cli_inventory.py
       <repository-relative path> ...

No automatic selection, new rows, policy changes or missing-file acceptance.
Uses the regression inventory's own pin algorithm. Review remains a human task.
"""

import argparse
import hashlib
import importlib.util
import os
import tempfile
from pathlib import Path
import re


def refreshed(source, root, paths, inventory):
    """Return updated text only after all explicit paths and rows validate."""
    tools = '.claude/skills/corpus-management/tools/'
    rows = inventory._rows(inventory.INVENTORY, 4)
    dependencies = inventory._rows(inventory.DEPENDENCIES, 2)
    if not paths or len(paths) != len(set(paths)):
        raise ValueError('name one or more distinct reviewed paths')
    for name in paths:
        if Path(name).as_posix() != name or Path(name).is_absolute() or any(
                part in ('', '.', '..') for part in name.split('/')):
            raise ValueError('expected a canonical repository-relative path: ' + name)
        path = root / name
        if any(parent.is_symlink() for parent in (path, *path.parents)):
            raise ValueError('symlink refused: ' + name)
        data = path.read_bytes()
        if name.startswith(tools) and name[len(tools):] in rows:
            key = name[len(tools):]
            policy, mode, digest = rows[key]
            old = f'{key} {policy} {mode} {digest}'
            new = f'{key} {policy} ' + ' '.join(inventory._pin(key, data))
        elif name in dependencies:
            old = name + ' ' + dependencies[name][0]
            new = name + ' ' + hashlib.sha256(data).hexdigest()
        else:
            raise ValueError('path has no existing inventory row: ' + name)
        pattern = r'(?m)^(        )' + re.escape(old) + r'$'
        source, count = re.subn(pattern, lambda match: match[1] + new, source)
        if count != 1:
            raise ValueError('expected exactly one matching pin row: ' + name)
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+')
    args = parser.parse_args()
    tests = Path(__file__).resolve().parent
    target = tests / 'test_linters.py'
    temporary = None
    try:
        spec = importlib.util.spec_from_file_location('_inventory_source', target)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        original = target.read_bytes()
        # Work on LF text for inventory matching, then restore the original CRs.
        # Pin rows must each have one consistent terminator; other bytes survive.
        source = original.decode('utf-8')
        normalized = source.replace('\r\n', '\n')
        updated = refreshed(normalized, module.REPO_ROOT,
                            args.paths, module.ExplicitPathCliInventoryTests)
        old_lines, new_lines = normalized.splitlines(keepends=True), updated.splitlines(keepends=True)
        raw_lines = source.splitlines(keepends=True)
        assert len(old_lines) == len(new_lines) == len(raw_lines)
        result = ''.join(raw if old == new else new.rstrip('\n') +
                         ('\r\n' if raw.endswith('\r\n') else '\n' if raw.endswith('\n') else '')
                         for old, new, raw in zip(old_lines, new_lines, raw_lines)).encode('utf-8')
        with tempfile.NamedTemporaryFile(dir=tests, prefix='.inventory-', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(result)
            os.fchmod(stream.fileno(), target.stat().st_mode & 0o777)
        os.replace(temporary, target)
        temporary = None
    except (OSError, ValueError, AssertionError) as exc:
        parser.error(str(exc))
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(f'Refreshed {len(args.paths)} reviewed inventory pin(s).')


if __name__ == '__main__':
    main()
