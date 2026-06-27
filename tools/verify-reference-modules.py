#!/usr/bin/env python3
"""Reference-module vs scratch-source parity aid (standards-validation discipline).

A maintainer dev-aid that confirms the in-repo control-reference modules
([`tools/ccm_aicm_reference.py`] and [`tools/nist_csf_reference.py`]) still
match the authoritative source extracts in the multi-session scratch repo's
``ref/standards/`` bucket (the CSA CCM v4.1.0 / AICM v1.1.0 catalogue CSVs and
the NIST CSWP-29 CSF 2.0 full text). The in-repo modules are a *derived
encoding* of codes and titles; the scratch ``ref/standards/`` extracts are the
*source text*. Gates 48, 49, and 54 enforce code validity against the modules,
so a silent drift between the modules and the source would let the gates pass
codes the source does not actually contain (or reject codes it does). This aid
is the parity check that catches such drift; it is the mechanical half of the
standards-validation discipline documented in the multi-session-orchestration
runbook section 6.

It is a developer AID, not an audit gate: it is named ``verify-*`` (not
``lint-*``) so the gate machinery (the four-surface parity gate 35, the
regression suite gate 36) does not auto-discover it, and it is NOT wired into
``run_all_audits.sh`` / CI. The reason it cannot be a CI gate: the scratch
``ref/standards/`` source lives in the separate ``grc_library_scratch`` repo,
which is not present in this repo's CI environment. Run it manually when doing
standards / control-code work, or when the scratch reference base is refreshed.

What it checks, per catalogue, in both directions (module set == source set):

  * **CSA CCM v4.1.0**: the ``CCM_V41`` keyset against the Control IDs in
    ``CSA-CCM-v4.1.0-catalogue__CCM.csv`` (the ``Control ID`` column).
  * **CSA AICM v1.1.0**: the ``AICM_V11`` keyset against the Control IDs in
    ``CSA-AICM-v1.1.0-catalogue__AICM.csv``.
  * **NIST CSF 2.0**: the ``CSF_CATEGORIES`` keyset against the
    ``FUNCTION.CATEGORY`` tokens in ``NIST-CSF-2.0--CSWP-29--full-text.md``.

Note the scope boundary: this aid validates *code existence* parity (does the
module's code set match the source's). It does NOT validate semantic mapping
fit (whether a given document belongs under a given control), which is the
apply-time author-every-cell responsibility, nor control *titles* (a possible
future extension). The discipline's prose half (verify a mapping's semantic
fit against the source control *title*, not the code number) is the worker /
orchestrator obligation the runbook records; this aid is the code-set parity
backstop under it.

Locating the scratch source (first match wins):
  1. a path given as the first CLI argument,
  2. the ``GRC_SCRATCH_REF_STANDARDS`` environment variable,
  3. ``../grc_library_scratch/ref/standards`` relative to this repo,
  4. ``/home/user/grc_library_scratch/ref/standards``.

If none resolve, the aid SKIPS (prints a notice and exits 0): the scratch base
is legitimately absent in many environments, and a dev-aid must not fail a
workflow for an environment it cannot see.

Exit codes: 0 = parity (or skipped, source absent), 1 = drift detected,
2 = source present but a required file is missing or unreadable.

Usage:
    python3 tools/verify-reference-modules.py
    python3 tools/verify-reference-modules.py /path/to/scratch/ref/standards
    GRC_SCRATCH_REF_STANDARDS=/path/to/ref/standards python3 tools/verify-reference-modules.py
"""

from __future__ import annotations

import csv
import os
import re
import sys
from pathlib import Path

from ccm_aicm_reference import AICM_V11, CCM_V41
from nist_csf_reference import CSF_CATEGORIES

CCM_CSV = "CSA-CCM-v4.1.0-catalogue__CCM.csv"
AICM_CSV = "CSA-AICM-v1.1.0-catalogue__AICM.csv"
CSF_MD = "NIST-CSF-2.0--CSWP-29--full-text.md"

CONTROL_ID_RE = re.compile(r"^[A-Z&]{2,4}-[0-9]{2}$")
CSF_CATEGORY_RE = re.compile(r"\b(?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2}\b")

REPO_ROOT = Path(__file__).resolve().parent.parent


def locate_source(argv: list[str]) -> Path | None:
    """Return the scratch ref/standards directory, or None if not found."""
    candidates: list[Path] = []
    if len(argv) > 1:
        candidates.append(Path(argv[1]))
    env = os.environ.get("GRC_SCRATCH_REF_STANDARDS")
    if env:
        candidates.append(Path(env))
    candidates.append(REPO_ROOT.parent / "grc_library_scratch" / "ref" / "standards")
    candidates.append(Path("/home/user/grc_library_scratch/ref/standards"))
    for c in candidates:
        if c.is_dir():
            return c
    return None


def csv_control_ids(path: Path) -> set[str]:
    """Extract the Control IDs from a CSA catalogue CSV's ``Control ID`` column."""
    ids: set[str] = set()
    id_col: int | None = None
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if id_col is None:
                if "Control ID" in row:
                    id_col = row.index("Control ID")
                continue
            if len(row) > id_col:
                tok = row[id_col].strip()
                if CONTROL_ID_RE.match(tok):
                    ids.add(tok)
    return ids


def csf_categories(path: Path) -> set[str]:
    """Extract the FUNCTION.CATEGORY tokens from the CSF 2.0 full-text extract."""
    text = path.read_text(encoding="utf-8")
    return set(CSF_CATEGORY_RE.findall(text))


def compare(label: str, module_set: set[str], source_set: set[str]) -> list[str]:
    """Return a list of drift messages for one catalogue (empty if in parity)."""
    msgs: list[str] = []
    only_module = sorted(module_set - source_set)
    only_source = sorted(source_set - module_set)
    if only_module:
        msgs.append(
            f"{label}: {len(only_module)} code(s) in the in-repo module but NOT "
            f"in the source extract: {', '.join(only_module)}"
        )
    if only_source:
        msgs.append(
            f"{label}: {len(only_source)} code(s) in the source extract but NOT "
            f"in the in-repo module: {', '.join(only_source)}"
        )
    return msgs


def main(argv: list[str]) -> int:
    source = locate_source(argv)
    if source is None:
        print(
            "SKIP: scratch ref/standards not found (looked at CLI arg, "
            "GRC_SCRATCH_REF_STANDARDS, ../grc_library_scratch/ref/standards, "
            "/home/user/grc_library_scratch/ref/standards). This is a dev-aid, "
            "not a gate; absence of the scratch base is not an error."
        )
        return 0

    checks = [
        ("CSA CCM v4.1.0", set(CCM_V41), CCM_CSV, "csv"),
        ("CSA AICM v1.1.0", set(AICM_V11), AICM_CSV, "csv"),
        ("NIST CSF 2.0", set(CSF_CATEGORIES), CSF_MD, "csf"),
    ]
    drift: list[str] = []
    for label, module_set, filename, kind in checks:
        path = source / filename
        if not path.is_file():
            print(f"ERROR: source file not found: {path}", file=sys.stderr)
            return 2
        try:
            source_set = csv_control_ids(path) if kind == "csv" else csf_categories(path)
        except OSError as exc:
            print(f"ERROR: cannot read {path}: {exc}", file=sys.stderr)
            return 2
        msgs = compare(label, module_set, source_set)
        if msgs:
            drift.extend(msgs)
        else:
            print(f"OK: {label} module ({len(module_set)} codes) matches the source extract.")

    if drift:
        print(f"\n=== reference-module drift vs {source} ===", file=sys.stderr)
        for m in drift:
            print(f"  {m}", file=sys.stderr)
        print(
            f"\nFAIL: {len(drift)} reference-module/source drift issue(s). The "
            f"in-repo modules (which gates 48/49/54 enforce against) have "
            f"diverged from the authoritative scratch ref/standards extracts. "
            f"Reconcile the module to the source before relying on the gates.",
            file=sys.stderr,
        )
        return 1

    print(
        f"\nOK: all reference modules match the scratch ref/standards source "
        f"extracts at {source} (CCM v4.1.0, AICM v1.1.0, NIST CSF 2.0)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
