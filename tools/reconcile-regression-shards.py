#!/usr/bin/env python3
"""Reconcile the gate-36 CI shards: results plus per-module credited starts.

The quality workflow's summary job (the required check "Lint markdown
corpus") runs this as its one verification step, with ``NEEDS_RESULTS``
holding GitHub Actions' ``toJSON(needs)`` for the lint job and every
regression-shard job. It fails unless:

  1. every needed job's result is ``success`` (the round-1 rule the old
     inline summary command enforced: a failed, cancelled or skipped
     needed job fails the required check rather than going missing);
  2. every ``regression-shard-*`` job published a ``credited`` output
     (the block-style ``module: count`` lines
     tools/run-linter-regression.py appends to ``GITHUB_OUTPUT`` after
     validating the shard sentinel), each naming exactly the on-disk
     top-level ``tests/test_*.py`` modules of this checkout; and
  3. summed across all shards, every module's credited-start total is
     at least one. This restores, before merge, the serial runner's
     refusal of a module with no credited start (its "N loaded, 0
     credited starts" refusal): one shard enforces at least one
     credited start for ITSELF, but only the cross-shard sum can see a
     module whose every test was skipped at class or module level in
     every shard it landed in.

Fail closed: an unset or unparseable ``NEEDS_RESULTS``, an empty needs
context, no regression-shard job among the needs, a shard with a
missing, empty or malformed ``credited`` output, a module set that is
not exactly the on-disk test modules, or an unreadable ``tests/``
directory is a refusal (exit 2). A needed job that did not succeed, or
a module whose cross-shard total is zero, is a failure (exit 1). Only a
fully reconciled green run exits 0.

The on-disk module set is read from ``tests/`` under the CURRENT
WORKING DIRECTORY (the workflow runs this from the checkout root), with
the same top-level ``tests/test_*.py`` enumeration the regression
runner's drivers use.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import json
import os
import sys

SHARD_JOB_PREFIX = "regression-shard-"
CREDITED_OUTPUT_NAME = "credited"


def on_disk_modules() -> list[str]:
    """The top-level tests/test_*.py modules of the current checkout."""
    return sorted(
        "tests." + entry.name[:-3]
        for entry in os.scandir("tests")
        if entry.is_file(follow_symlinks=False)
        and entry.name.startswith("test_") and entry.name.endswith(".py"))


def parse_credited(text: str) -> dict[str, int] | str:
    """The ``module: count`` mapping of one shard's credited output, or a
    string naming what is malformed. Every line must be
    ``<module>: <nonnegative integer>`` with a dotted-identifier module
    name; an empty output and a repeated module are malformed."""
    counts: dict[str, int] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        name, sep, value = line.partition(": ")
        name = name.strip()
        value = value.strip()
        if (not sep or not value.isdigit()
                or not all(part.isidentifier()
                           for part in name.split(".")) or not name):
            return "holds the unreadable line %r" % line
        if name in counts:
            return "names the module %r twice" % name
        counts[name] = int(value)
    if not counts:
        return "is empty"
    return counts


def reconcile(needs: dict, modules: list[str]) -> tuple[int, list[str]]:
    """(exit code, report lines) for the needs context ``needs`` against the
    on-disk ``modules``. Pure, for the regression tests."""
    lines: list[str] = []
    lines.append("needed job results %s"
                 % sorted((name, (job or {}).get("result"))
                          for name, job in needs.items()))
    if not isinstance(needs, dict) or not needs:
        lines.append("REFUSED: the needs context is empty; the summary "
                     "cannot confirm any needed job")
        return 2, lines
    failed = [name for name, job in sorted(needs.items())
              if not isinstance(job, dict) or job.get("result") != "success"]
    code = 0
    if failed:
        lines.append("FAIL: needed job(s) did not succeed: %s"
                     % ", ".join(failed))
        code = 1
    shards = [name for name in sorted(needs)
              if name.startswith(SHARD_JOB_PREFIX)]
    if not shards:
        lines.append("REFUSED: no %s* job is among the needs; the "
                     "per-module credited-start reconciliation has nothing "
                     "to sum" % SHARD_JOB_PREFIX)
        return 2, lines
    if code:
        # A failed needed job already fails the check; its outputs may
        # legitimately be absent, so the reconciliation is not reached.
        return code, lines
    totals: dict[str, int] = dict.fromkeys(modules, 0)
    for name in shards:
        job = needs[name]
        outputs = job.get("outputs")
        text = (outputs or {}).get(CREDITED_OUTPUT_NAME, "")
        if not isinstance(text, str) or not text.strip():
            lines.append("REFUSED: %s published no %r output; every shard "
                         "must publish its per-module credited-start counts"
                         % (name, CREDITED_OUTPUT_NAME))
            return 2, lines
        counts = parse_credited(text)
        if isinstance(counts, str):
            lines.append("REFUSED: the %r output of %s %s"
                         % (CREDITED_OUTPUT_NAME, name, counts))
            return 2, lines
        if sorted(counts) != modules:
            lines.append("REFUSED: the %r output of %s names the modules %s, "
                         "not exactly the on-disk tests/test_*.py modules %s"
                         % (CREDITED_OUTPUT_NAME, name, sorted(counts),
                            modules))
            return 2, lines
        for module, count in counts.items():
            totals[module] += count
    for module in modules:
        lines.append("credited starts %s=%d" % (module, totals[module]))
    zero = [module for module in modules if totals[module] < 1]
    if zero:
        for module in zero:
            lines.append("FAIL: tests/%s.py: 0 credited starts across all "
                         "shards (the serial runner refuses such a module; "
                         "a file on the run list is not a file whose tests "
                         "ran)" % module.partition(".")[2])
        return 1, lines
    lines.append("OK: every needed job succeeded and every module earned a "
                 "credited start across the %d shards" % len(shards))
    return 0, lines


def main() -> int:
    raw = os.environ.get("NEEDS_RESULTS")
    if not raw:
        print("REFUSED: NEEDS_RESULTS is unset or empty; the summary cannot "
              "read the needed jobs", file=sys.stderr)
        return 2
    try:
        needs = json.loads(raw)
    except ValueError as exc:
        print("REFUSED: NEEDS_RESULTS is not valid JSON: %s" % exc,
              file=sys.stderr)
        return 2
    if not isinstance(needs, dict):
        print("REFUSED: NEEDS_RESULTS is not a JSON object", file=sys.stderr)
        return 2
    try:
        modules = on_disk_modules()
    except OSError as exc:
        print("REFUSED: cannot enumerate tests/ under the working "
              "directory: %s" % exc, file=sys.stderr)
        return 2
    if not modules:
        print("REFUSED: no tests/test_*.py module found under the working "
              "directory", file=sys.stderr)
        return 2
    code, lines = reconcile(needs, modules)
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
