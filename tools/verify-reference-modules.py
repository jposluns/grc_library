#!/usr/bin/env python3
"""Reference-module vs scratch-source parity aid (standards-validation discipline).

A maintainer dev-aid that confirms the in-repo control-reference modules
([`tools/ccm_aicm_reference.py`], [`tools/nist_csf_reference.py`], and
[`tools/cobit_iso31000_reference.py`]) still match the authoritative source
extracts in the multi-session scratch repo's ``ref/`` reference base: the CSA
CCM v4.1.0 / AICM v1.1.0 catalogue CSVs under ``ref/frameworks/CSA/``, the
NIST CSWP-29 CSF 2.0 full text under ``ref/standards/NIST/``, the COBIT 2019
Governance and Management Objectives extract under ``ref/frameworks/COBIT/``,
and the ISO 31000:2018 full text under ``ref/standards/ISO/``. The in-repo
modules are a *derived encoding* of codes and titles; the scratch extracts are
the *source text*. Gates 48/49/54/58/61 enforce code validity against the
modules, so a silent drift between the modules and the source would let the
gates pass codes the source does not actually contain (or reject codes it
does). This aid is the parity check that catches such drift; it is the
mechanical half of the standards-validation discipline documented in the
multi-session-orchestration runbook section 6.

It is a developer AID, not an audit gate: it is named ``verify-*`` (not
``lint-*``) so the gate machinery (the four-surface parity gate 35, the
regression suite gate 36) does not auto-discover it, and it is NOT wired into
``run_all_audits.sh`` / CI. The reason it cannot be a CI gate: the scratch
``ref/`` source lives in the separate ``grc_library_scratch`` repo, which is
not present in this repo's CI environment. Run it manually when doing
standards / control-code work, or when the scratch reference base is refreshed.

What it checks, per catalogue:

  * **CSA CCM v4.1.0** (both directions): the ``CCM_V41`` keyset against the
    Control IDs in ``frameworks/CSA/CCM/CSA-CCM-v4.1.0-catalogue__CCM.csv``
    (the ``Control ID`` column).
  * **CSA AICM v1.1.0** (both directions): the ``AICM_V11`` keyset against
    the Control IDs in
    ``frameworks/CSA/AICM/CSA-AICM-v1.1.0-catalogue__AICM.csv``.
  * **NIST CSF 2.0** (both directions): the ``CSF_CATEGORIES`` keyset against
    the ``FUNCTION.CATEGORY`` tokens in
    ``standards/NIST/NIST-CSF-2.0--CSWP-29--full-text.md``.
  * **COBIT 2019** (both directions, plus range closure): the
    ``COBIT_OBJECTIVES`` keyset against the objective-code tokens of the
    Governance and Management Objectives extract, and the
    ``COBIT_PRACTICE_COUNTS`` ranges against the extract's practice tokens
    (every extract token must fall inside the recorded per-objective range,
    and every recorded range maximum must appear in the extract).
  * **ISO 31000:2018** (module-to-source direction ONLY): every
    ``ISO31000_CLAUSES`` key appears in the extract as a standalone clause
    token, so a fabricated MULTI-PART clause number (a ``4.5`` or ``5.8``)
    cannot sit in the module. Single-digit clause tokens are weaker evidence
    (any digit-and-dot-isolated occurrence of the digit anywhere in the text
    matches, so a fabricated ``7`` or ``8`` could pass); that residual is
    covered by the module's deterministic-parse provenance, not by this
    check. The reverse direction is not checked: the extract's layout does not support a
    reliable line-scan enumeration of its clause tree, and the module's
    provenance is already a deterministic parse cross-checked at ingestion.

Note the scope boundary: this aid validates *code existence* parity (does the
module's code set match the source's). It does NOT validate semantic mapping
fit (whether a given document belongs under a given control), which is the
apply-time author-every-cell responsibility, nor control *titles* (a possible
future extension). The discipline's prose half (verify a mapping's semantic
fit against the source control *title*, not the code number) is the worker /
orchestrator obligation the runbook records; this aid is the code-set parity
backstop under it.

Locating the scratch source (first match wins). The resolved directory is the
scratch ``ref/`` ROOT (the buckets sit under it); a CLI path ending in
``ref/standards`` is accepted for back-compat and resolved to its parent:

  1. a path given as the first CLI argument (an explicit path that does not
     resolve is an ERROR, exit 2, never a fallthrough to the defaults),
  2. the ``GRC_SCRATCH_REF`` environment variable (same error contract as
     the CLI path: a set-but-nonexistent value exits 2),
  3. ``../grc_library_scratch/ref`` relative to this repo,
  4. ``/home/user/grc_library_scratch/ref``.

If none resolve, the aid SKIPS (prints a notice and exits 0): the scratch base
is legitimately absent in many environments, and a dev-aid must not fail a
workflow for an environment it cannot see.

Exit codes: 0 = parity (or skipped, source absent), 1 = drift detected,
2 = an explicitly-given source path does not resolve, or the source is
present but a required file is missing or unreadable.

Usage:
    python3 tools/verify-reference-modules.py
    python3 tools/verify-reference-modules.py /path/to/scratch/ref
    GRC_SCRATCH_REF=/path/to/ref python3 tools/verify-reference-modules.py
"""

from __future__ import annotations

import csv
import os
import re
import sys
from pathlib import Path

from ccm_aicm_reference import AICM_V11, CCM_V41
from cobit_iso31000_reference import (
    COBIT_OBJECTIVES,
    COBIT_PRACTICE_COUNTS,
    ISO31000_CLAUSES,
)
from nist_csf_reference import CSF_CATEGORIES

# Source-extract paths, relative to the scratch ref/ root.
CCM_CSV = "frameworks/CSA/CCM/CSA-CCM-v4.1.0-catalogue__CCM.csv"
AICM_CSV = "frameworks/CSA/AICM/CSA-AICM-v1.1.0-catalogue__AICM.csv"
CSF_MD = "standards/NIST/NIST-CSF-2.0--CSWP-29--full-text.md"
COBIT_MD = (
    "frameworks/COBIT/"
    "COBIT-2019-Framework-Governance-and-Management-Objectives--full-text.md"
)
ISO31000_MD = "standards/ISO/ISO-31000-2018--Risk-management-guidelines--full-text.md"

CONTROL_ID_RE = re.compile(r"^[A-Z&]{2,4}-[0-9]{2}$")
CSF_CATEGORY_RE = re.compile(r"\b(?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2}\b")
COBIT_OBJECTIVE_RE = re.compile(r"\b(?:EDM|APO|BAI|DSS|MEA)\d{2}\b")
COBIT_PRACTICE_RE = re.compile(r"\b((?:EDM|APO|BAI|DSS|MEA)\d{2})\.(\d{2})\b")

REPO_ROOT = Path(__file__).resolve().parent.parent


def locate_source(argv: list[str]) -> Path | None:
    """Return the scratch ``ref/`` root directory, or ``None`` if not found.

    An EXPLICIT CLI path that does not resolve raises ``SystemExit(2)``
    rather than silently falling through to the default locations (a typo'd
    path must not produce a green result computed against a different tree).
    """
    candidates: list[Path] = []
    if len(argv) > 1:
        given = Path(argv[1])
        # Back-compat: an old-style ref/standards path resolves to its parent.
        if given.name == "standards" and (given.parent / "frameworks").is_dir():
            given = given.parent
        if not given.is_dir():
            print(
                f"ERROR: the given source path is not a directory: {given}",
                file=sys.stderr,
            )
            raise SystemExit(2)
        candidates.append(given)
    env = os.environ.get("GRC_SCRATCH_REF")
    if env:
        env_path = Path(env)
        if not env_path.is_dir():
            print(
                f"ERROR: GRC_SCRATCH_REF is set but is not a directory: {env_path}",
                file=sys.stderr,
            )
            raise SystemExit(2)
        candidates.append(env_path)
    candidates.append(REPO_ROOT.parent / "grc_library_scratch" / "ref")
    candidates.append(Path("/home/user/grc_library_scratch/ref"))
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


def cobit_drift(path: Path) -> list[str]:
    """Objective-code parity (both directions) plus practice-range closure."""
    text = path.read_text(encoding="utf-8")
    msgs = compare(
        "COBIT 2019 objectives",
        set(COBIT_OBJECTIVES),
        set(COBIT_OBJECTIVE_RE.findall(text)),
    )
    seen_max: dict[str, int] = {}
    for obj, prac in COBIT_PRACTICE_RE.findall(text):
        num = int(prac)
        if obj not in COBIT_PRACTICE_COUNTS:
            msgs.append(
                f"COBIT 2019 practices: extract token {obj}.{prac} names an "
                f"objective the module does not record"
            )
            continue
        if num > COBIT_PRACTICE_COUNTS[obj]:
            msgs.append(
                f"COBIT 2019 practices: extract token {obj}.{prac} exceeds the "
                f"module's recorded range ({obj} ends at "
                f".{COBIT_PRACTICE_COUNTS[obj]:02d})"
            )
        seen_max[obj] = max(seen_max.get(obj, 0), num)
    for obj, count in sorted(COBIT_PRACTICE_COUNTS.items()):
        if seen_max.get(obj, 0) < count:
            msgs.append(
                f"COBIT 2019 practices: the module records {obj} ending at "
                f".{count:02d}, but the extract's highest seen token is "
                f".{seen_max.get(obj, 0):02d}"
            )
    return msgs


def iso31000_drift(path: Path) -> list[str]:
    """Module-to-source: every recorded clause number appears in the extract."""
    text = path.read_text(encoding="utf-8")
    missing = [
        clause
        for clause in sorted(ISO31000_CLAUSES)
        if re.search(rf"(?<![\d.]){re.escape(clause)}(?![\d.])", text) is None
    ]
    if not missing:
        return []
    return [
        f"ISO 31000:2018 clauses: {len(missing)} clause number(s) in the "
        f"in-repo module but NOT found in the source extract: "
        f"{', '.join(missing)}"
    ]


def main(argv: list[str]) -> int:
    source = locate_source(argv)
    if source is None:
        print(
            "SKIP: scratch ref/ base not found (looked at CLI arg, "
            "GRC_SCRATCH_REF, ../grc_library_scratch/ref, "
            "/home/user/grc_library_scratch/ref). This is a dev-aid, "
            "not a gate; absence of the scratch base is not an error."
        )
        return 0

    set_checks = [
        ("CSA CCM v4.1.0", set(CCM_V41), CCM_CSV, "csv"),
        ("CSA AICM v1.1.0", set(AICM_V11), AICM_CSV, "csv"),
        ("NIST CSF 2.0", set(CSF_CATEGORIES), CSF_MD, "csf"),
    ]
    drift: list[str] = []
    for label, module_set, filename, kind in set_checks:
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

    for filename, checker, ok_line in [
        (
            COBIT_MD,
            cobit_drift,
            (
                f"OK: COBIT 2019 module ({len(COBIT_OBJECTIVES)} objectives, "
                f"{sum(COBIT_PRACTICE_COUNTS.values())} practices by range) "
                f"matches the source extract."
            ),
        ),
        (
            ISO31000_MD,
            iso31000_drift,
            (
                f"OK: ISO 31000:2018 module ({len(ISO31000_CLAUSES)} clause "
                f"numbers) all present in the source extract "
                f"(module-to-source direction; see docstring)."
            ),
        ),
    ]:
        path = source / filename
        if not path.is_file():
            print(f"ERROR: source file not found: {path}", file=sys.stderr)
            return 2
        try:
            msgs = checker(path)
        except OSError as exc:
            print(f"ERROR: cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if msgs:
            drift.extend(msgs)
        else:
            print(ok_line)

    if drift:
        print(f"\n=== reference-module drift vs {source} ===", file=sys.stderr)
        for m in drift:
            print(f"  {m}", file=sys.stderr)
        print(
            f"\nFAIL: {len(drift)} reference-module/source drift issue(s). The "
            f"in-repo modules (which gates 48/49/54/58/61 enforce against) have "
            f"diverged from the authoritative scratch ref/ source extracts. "
            f"Reconcile the module to the source before relying on the gates.",
            file=sys.stderr,
        )
        return 1

    print(
        f"\nOK: all reference modules match the scratch ref/ source "
        f"extracts at {source} (CCM v4.1.0, AICM v1.1.0, NIST CSF 2.0, "
        f"COBIT 2019, ISO 31000:2018)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
