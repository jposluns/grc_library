#!/usr/bin/env python3
"""Reconcile the gate-36 shards: results, unit sets, credited starts.

The quality workflow's summary job (the required check "Lint markdown
corpus") runs this as its one verification step, with ``NEEDS_RESULTS``
holding GitHub Actions' ``toJSON(needs)`` for the lint job and every
regression-shard job. The pre-push guard (tools/pre-push-guard.sh) runs
it in its local mode, ``--shard-outputs`` (below), over the shards it ran
itself. It fails unless:

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
     every shard it landed in; and
  4. every shard published a ``units_sha256`` output (the sha256 of the
     TOTAL unit list its own suite load found) and a ``selected_sha256``
     output (that of its selected units), each 64 lowercase hex
     characters, and every shard's ``units_sha256`` is the same. Each
     shard checks that its selection partitions the units IT discovered;
     only this cross-shard agreement shows the shards discovered the same
     suite, so a discovery difference between runners fails here.

Fail closed: an unset or unparseable ``NEEDS_RESULTS``, an empty needs
context, no regression-shard job among the needs, a shard with a
missing, empty or malformed ``credited``, ``units_sha256`` or
``selected_sha256`` output, a module set that is not exactly the
on-disk test modules, or an unreadable ``tests/`` directory is a
refusal (exit 2). A needed job that did not succeed, a module whose
cross-shard total is zero, or shards whose ``units_sha256`` differ is a
failure (exit 1). Only a fully reconciled green run exits 0.

Local mode: ``--shard-outputs K RC_1 FILE_1 ... RC_K FILE_K`` builds the
needs context from the K shards the pre-push guard ran, shard i being
``regression-shard-i``: RC_i is that shard's exit status as the guard
read it (``success`` only for exactly ``0``) and FILE_i is the
``GITHUB_OUTPUT`` file that shard wrote, parsed with the GitHub Actions
step-output grammar (``name=value`` and ``name<<DELIM`` blocks). A
count that is not K, a missing argument, a status that is not a decimal
integer, or an unreadable or unparseable file is a refusal (exit 2); a
missing shard is therefore never a pass. There is no lint job in this
mode (the guard runs the shards, not the lint job), so the needs
context holds the shards alone.

The on-disk module set is read from ``tests/`` under the CURRENT
WORKING DIRECTORY (the workflow runs this from the checkout root), with
the same top-level ``tests/test_*.py`` enumeration the regression
runner's drivers use.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import json
import os
import re
import sys

SHARD_JOB_PREFIX = "regression-shard-"
CREDITED_OUTPUT_NAME = "credited"
DIGEST_OUTPUT_NAMES = ("units_sha256", "selected_sha256")
DIGEST_RE = re.compile(r"[0-9a-f]{64}")
OUTPUT_NAME_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_-]*")
SHARD_OUTPUTS_FLAG = "--shard-outputs"


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
    unit_sets: dict[str, str] = {}
    for name in shards:
        job = needs[name]
        outputs = job.get("outputs")
        for output in DIGEST_OUTPUT_NAMES:
            digest = (outputs or {}).get(output, "")
            if not isinstance(digest, str) or not DIGEST_RE.fullmatch(digest):
                lines.append("REFUSED: %s published no well-formed %r output "
                             "(64 lowercase hex characters); every shard must "
                             "publish the digests of its total and selected "
                             "unit lists" % (name, output))
                return 2, lines
        unit_sets[name] = outputs[DIGEST_OUTPUT_NAMES[0]]
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
    for name in shards:
        lines.append("unit set %s=%s" % (name, unit_sets[name]))
    if len(set(unit_sets.values())) != 1:
        lines.append("FAIL: the shards discovered different unit sets (their "
                     "%s outputs differ); a discovery difference between "
                     "runners means the shards did not partition one suite"
                     % DIGEST_OUTPUT_NAMES[0])
        return 1, lines
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
    lines.append("OK: every needed job succeeded, the %d shards discovered "
                 "one unit set, and every module earned a credited start "
                 "across them" % len(shards))
    return 0, lines


def parse_step_outputs(text: str) -> dict[str, str] | str:
    """The outputs a GitHub Actions step wrote to its GITHUB_OUTPUT file,
    or a string naming what is malformed. Each entry is ``name=value`` on
    one line or ``name<<DELIM``, value lines, then ``DELIM`` alone; a
    repeated name, an unterminated block or any other line is malformed."""
    outputs: dict[str, str] = {}
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    i = 0
    while i < len(lines):
        line = lines[i]
        name, sep, value = line.partition("<<")
        if sep and OUTPUT_NAME_RE.fullmatch(name) and value:
            end = i + 1
            while end < len(lines) and lines[end] != value:
                end += 1
            if end == len(lines):
                return "has the unterminated block %r" % name
            body = "".join(part + "\n" for part in lines[i + 1:end])
            i = end + 1
        else:
            name, sep, body = line.partition("=")
            if not sep or not OUTPUT_NAME_RE.fullmatch(name):
                return "holds the unreadable line %r" % line
            i += 1
        if name in outputs:
            return "sets the output %r twice" % name
        outputs[name] = body
    return outputs


def local_needs(argv: list[str]) -> dict | str:
    """The needs context of ``--shard-outputs K RC_1 FILE_1 ...``, or a
    refusal message (see the module docstring's local mode)."""
    if not argv or not (argv[0].isascii() and argv[0].isdigit()) \
            or int(argv[0]) < 1:
        return ("%s needs the shard count K (a positive decimal integer) "
                "first" % SHARD_OUTPUTS_FLAG)
    count = int(argv[0])
    pairs = argv[1:]
    if len(pairs) != 2 * count:
        return ("%s %d needs exactly %d status and output-file pairs, one "
                "per shard; %d argument(s) were given, so a shard is missing"
                % (SHARD_OUTPUTS_FLAG, count, count, len(pairs)))
    needs: dict = {}
    for index in range(1, count + 1):
        status, path = pairs[2 * index - 2], pairs[2 * index - 1]
        name = SHARD_JOB_PREFIX + str(index)
        if not (status.isascii() and status.isdigit()):
            return "%s's exit status %r is not a decimal integer" % (name,
                                                                     status)
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except (OSError, UnicodeDecodeError) as exc:
            return "cannot read %s's output file %s: %s" % (name, path, exc)
        outputs = parse_step_outputs(text)
        if isinstance(outputs, str):
            return "%s's output file %s %s" % (name, path, outputs)
        needs[name] = {"result": "success" if status == "0" else "failure",
                       "outputs": outputs}
    return needs


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == SHARD_OUTPUTS_FLAG:
        needs = local_needs(argv[1:])
        if isinstance(needs, str):
            print("REFUSED: " + needs, file=sys.stderr)
            return 2
    elif argv:
        print("REFUSED: usage: reconcile-regression-shards.py [%s K RC_1 "
              "FILE_1 ... RC_K FILE_K] (no argument reads NEEDS_RESULTS)"
              % SHARD_OUTPUTS_FLAG, file=sys.stderr)
        return 2
    else:
        raw = os.environ.get("NEEDS_RESULTS")
        if not raw:
            print("REFUSED: NEEDS_RESULTS is unset or empty; the summary "
                  "cannot read the needed jobs", file=sys.stderr)
            return 2
        try:
            needs = json.loads(raw)
        except ValueError as exc:
            print("REFUSED: NEEDS_RESULTS is not valid JSON: %s" % exc,
                  file=sys.stderr)
            return 2
        if not isinstance(needs, dict):
            print("REFUSED: NEEDS_RESULTS is not a JSON object",
                  file=sys.stderr)
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
