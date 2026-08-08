#!/usr/bin/env python3
"""validate-review-artifacts.py - structural validator for AIQT review artefacts.

Validates a SARIF-lite finding record or a verdict envelope (the two machine
forms of the AIQT cross-family review contract, guardrails/aiqt/review-contract.md
sections 4 and 5) without third-party dependencies. The JSON Schema files under
guardrails/aiqt/schemas/ (finding.schema.json, verdict.schema.json) remain the
NORMATIVE interchange form for every consumer, Python or not; this tool is a
hand-rolled structural check implementing exactly their required fields, types,
enums, and regex patterns, kept in parity with them by hand.

STATED RESIDUE (per validate-inference-before-action, "Guard inputs"): this is
not a JSON Schema implementation, so a schema edit does not propagate here
automatically; the parity is maintained by hand and the .json files win on any
divergence. Two deliberate strictness choices, both in the refusal-loud
direction: draft 2020-12 "integer" admits any number with a zero fractional
part (1.0 validates upstream), while this checker accepts only JSON integers
and rejects booleans; and the anchored patterns are applied with fullmatch,
matching the ECMA-262 end-of-string semantics the schemas mean, where Python's
own `$` would tolerate a trailing newline.

Pure validation core (each returns a list of error strings; empty = valid):
  validate_finding(obj) -> list[str]
  validate_verdict(obj) -> list[str]
  check_counts_match(verdict, findings) -> list[str]
      the counts-must-match-finding-set cross-check (contract section 5); it
      runs only over a well-formed counts object (validate_verdict reports a
      malformed one, double-reporting would be noise) and tallies only levels
      that are valid enum values (an invalid level is reported by the
      per-finding validation)

Modes:
  --kind finding <file>                 validate one finding object
  --kind verdict <file>                 validate one verdict envelope
  --kind verdict <file> --findings <f>  also validate every finding in the
                                        attached set (a JSON array of finding
                                        objects) and cross-check the envelope's
                                        counts against the set's per-level tally
  --self-test                           run the synthetic-fixture unit tests

Refusals are loud: every validation error prints on its own line and the tool
exits 1; unreadable or unparseable input exits 2; a valid artefact prints OK
and exits 0.

Stdlib-only (project convention). Portable pack companion to
guardrails/aiqt/review-contract.md; consumed by the AIQT CI kit and L1 CLI.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# --- schema constants (hand-kept in parity with guardrails/aiqt/schemas/) ----------
FINDING_REQUIRED = (
    "tool", "ruleId", "level", "location", "fingerprint",
    "evidence", "impact", "recommendation",
)
LEVEL_ENUM = ("error", "warning", "note")
VERDICT_ENUM = ("SHIP", "HOLD")
VERDICT_REQUIRED = ("verdict", "counts", "proof_of_run", "head", "base", "model")
COUNTS_REQUIRED = ("error", "warning", "note")
PROOF_REQUIRED = ("files_read", "commands_run", "checks_passed")

# Pattern strings byte-identical to the schema files; applied via fullmatch so
# the end anchor carries ECMA-262 semantics (no trailing-newline tolerance).
RULE_ID_PATTERN = "^[a-z0-9]+(-[a-z0-9]+)*$"
LOCATION_PATTERN = "^[^:]+:[0-9]+$"
FINGERPRINT_PATTERN = "^[a-z0-9-]+:[^:]+:[0-9]+$"
_RULE_ID_RE = re.compile(RULE_ID_PATTERN)
_LOCATION_RE = re.compile(LOCATION_PATTERN)
_FINGERPRINT_RE = re.compile(FINGERPRINT_PATTERN)

# minLength floors from the schemas.
_FINDING_MIN1_STRINGS = ("tool", "evidence", "impact", "recommendation")
_VERDICT_STRING_MINLEN = (("head", 7), ("base", 7), ("model", 1))


def _is_int(value: object) -> bool:
    """JSON integer: a Python int that is not a bool (bool subclasses int)."""
    return isinstance(value, int) and not isinstance(value, bool)


def _check_min_string(obj: dict, field: str, min_length: int,
                      errors: list[str], prefix: str = "") -> None:
    value = obj[field]
    if not isinstance(value, str):
        errors.append(f"{prefix}{field}: expected a string, got {type(value).__name__}")
    elif len(value) < min_length:
        errors.append(f"{prefix}{field}: shorter than minLength {min_length}")


def _check_pattern(obj: dict, field: str, rx: re.Pattern, pattern: str,
                   errors: list[str]) -> None:
    value = obj[field]
    if not isinstance(value, str):
        errors.append(f"{field}: expected a string, got {type(value).__name__}")
    elif not rx.fullmatch(value):
        errors.append(f"{field}: {value!r} does not match pattern {pattern}")


# --- pure validators -----------------------------------------------------------------
def validate_finding(obj) -> list[str]:
    """PURE. Error list for one SARIF-lite finding object; empty = valid."""
    if not isinstance(obj, dict):
        return ["top-level value is not a JSON object"]
    errors: list[str] = []
    for field in FINDING_REQUIRED:
        if field not in obj:
            errors.append(f"missing required field: {field}")
    for field in sorted(set(obj) - set(FINDING_REQUIRED)):
        errors.append(f"unexpected field (additionalProperties: false): {field}")
    for field in _FINDING_MIN1_STRINGS:
        if field in obj:
            _check_min_string(obj, field, 1, errors)
    if "level" in obj and obj["level"] not in LEVEL_ENUM:
        errors.append(f"level: {obj['level']!r} is not one of {list(LEVEL_ENUM)}")
    if "ruleId" in obj:
        _check_pattern(obj, "ruleId", _RULE_ID_RE, RULE_ID_PATTERN, errors)
    if "location" in obj:
        _check_pattern(obj, "location", _LOCATION_RE, LOCATION_PATTERN, errors)
    if "fingerprint" in obj:
        _check_pattern(obj, "fingerprint", _FINGERPRINT_RE, FINGERPRINT_PATTERN, errors)
    return errors


def _validate_counts(counts, errors: list[str]) -> None:
    if not isinstance(counts, dict):
        errors.append(f"counts: expected an object, got {type(counts).__name__}")
        return
    for key in COUNTS_REQUIRED:
        if key not in counts:
            errors.append(f"counts.{key}: missing required field")
        elif not _is_int(counts[key]):
            errors.append(f"counts.{key}: expected an integer, "
                          f"got {type(counts[key]).__name__}")
        elif counts[key] < 0:
            errors.append(f"counts.{key}: {counts[key]} is below minimum 0")
    for key in sorted(set(counts) - set(COUNTS_REQUIRED)):
        errors.append(f"counts.{key}: unexpected field (additionalProperties: false)")


def _validate_proof_of_run(proof, errors: list[str]) -> None:
    if not isinstance(proof, dict):
        errors.append(f"proof_of_run: expected an object, got {type(proof).__name__}")
        return
    for key in PROOF_REQUIRED:
        if key not in proof:
            errors.append(f"proof_of_run.{key}: missing required field")
    for key in sorted(set(proof) - set(PROOF_REQUIRED)):
        errors.append(f"proof_of_run.{key}: unexpected field "
                      "(additionalProperties: false)")
    if "files_read" in proof:
        value = proof["files_read"]
        if not _is_int(value):
            errors.append(f"proof_of_run.files_read: expected an integer, "
                          f"got {type(value).__name__}")
        elif value < 0:
            errors.append(f"proof_of_run.files_read: {value} is below minimum 0")
    for key in ("commands_run", "checks_passed"):
        if key not in proof:
            continue
        value = proof[key]
        if not isinstance(value, list):
            errors.append(f"proof_of_run.{key}: expected an array, "
                          f"got {type(value).__name__}")
            continue
        for i, item in enumerate(value):
            if not isinstance(item, str):
                errors.append(f"proof_of_run.{key}[{i}]: expected a string, "
                              f"got {type(item).__name__}")


def validate_verdict(obj) -> list[str]:
    """PURE. Error list for one verdict envelope; empty = valid."""
    if not isinstance(obj, dict):
        return ["top-level value is not a JSON object"]
    errors: list[str] = []
    for field in VERDICT_REQUIRED:
        if field not in obj:
            errors.append(f"missing required field: {field}")
    for field in sorted(set(obj) - set(VERDICT_REQUIRED)):
        errors.append(f"unexpected field (additionalProperties: false): {field}")
    if "verdict" in obj and obj["verdict"] not in VERDICT_ENUM:
        errors.append(f"verdict: {obj['verdict']!r} is not one of {list(VERDICT_ENUM)}")
    if "counts" in obj:
        _validate_counts(obj["counts"], errors)
    if "proof_of_run" in obj:
        _validate_proof_of_run(obj["proof_of_run"], errors)
    for field, min_length in _VERDICT_STRING_MINLEN:
        if field in obj:
            _check_min_string(obj, field, min_length, errors)
    return errors


def check_counts_match(verdict, findings) -> list[str]:
    """PURE. Contract section 5: counts must equal the attached finding set.

    Returns an empty list when the envelope's counts agree with the set's
    per-level tally, or when the counts object is malformed (validate_verdict
    already reports that defect; double-reporting is noise). Findings whose
    level is not a valid enum value do not enter the tally; the per-finding
    validation reports them.
    """
    if not isinstance(verdict, dict) or not isinstance(verdict.get("counts"), dict):
        return []
    counts = verdict["counts"]
    if any(key not in counts or not _is_int(counts[key]) for key in COUNTS_REQUIRED):
        return []
    tally = {key: 0 for key in COUNTS_REQUIRED}
    for finding in findings:
        if isinstance(finding, dict) and finding.get("level") in tally:
            tally[finding["level"]] += 1
    errors: list[str] = []
    for key in COUNTS_REQUIRED:
        if counts[key] != tally[key]:
            errors.append(f"counts.{key}: verdict says {counts[key]}, "
                          f"the attached finding set has {tally[key]}")
    return errors


# --- self-test ------------------------------------------------------------------------
def _valid_finding() -> dict:
    return {
        "tool": "codex-change-0001",
        "ruleId": "missed-parallel-fix",
        "level": "warning",
        "location": "tools/example.py:42",
        "fingerprint": "missed-parallel-fix:tools/example.py:42",
        "evidence": "synthetic evidence quote (SYNTHETIC FIXTURE)",
        "impact": "synthetic one-line impact",
        "recommendation": "synthetic one-line fix",
    }


def _valid_verdict() -> dict:
    return {
        "verdict": "SHIP",
        "counts": {"error": 0, "warning": 1, "note": 0},
        "proof_of_run": {
            "files_read": 3,
            "commands_run": ["python3 -m pytest -q"],
            "checks_passed": ["self-test"],
        },
        "head": "abcdef0123456",
        "base": "0123456abcdef",
        "model": "synthetic-model-id",
    }


def self_test() -> int:
    failures, total = [], [0]

    def check(name, got, want):
        total[0] += 1
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}: {name}"
              + ("" if ok else f" -> {got!r}, expected {want!r}"))
        if not ok:
            failures.append(name)

    # Fully-valid pair.
    check("valid finding passes", validate_finding(_valid_finding()), [])
    check("valid verdict passes", validate_verdict(_valid_verdict()), [])
    check("valid pair counts match",
          check_counts_match(_valid_verdict(), [_valid_finding()]), [])

    # Every required field absent, one at a time.
    for field in FINDING_REQUIRED:
        broken = _valid_finding()
        del broken[field]
        check(f"finding missing {field} refused",
              validate_finding(broken), [f"missing required field: {field}"])
    for field in VERDICT_REQUIRED:
        broken = _valid_verdict()
        del broken[field]
        check(f"verdict missing {field} refused",
              validate_verdict(broken), [f"missing required field: {field}"])
    for key in COUNTS_REQUIRED:
        broken = _valid_verdict()
        del broken["counts"][key]
        check(f"counts missing {key} refused",
              validate_verdict(broken), [f"counts.{key}: missing required field"])
    for key in PROOF_REQUIRED:
        broken = _valid_verdict()
        del broken["proof_of_run"][key]
        check(f"proof_of_run missing {key} refused",
              validate_verdict(broken),
              [f"proof_of_run.{key}: missing required field"])

    # Every enum violated.
    broken = _valid_finding()
    broken["level"] = "critical"
    check("level enum violated refused", validate_finding(broken),
          ["level: 'critical' is not one of ['error', 'warning', 'note']"])
    broken = _valid_verdict()
    broken["verdict"] = "ship"
    check("verdict enum violated refused", validate_verdict(broken),
          ["verdict: 'ship' is not one of ['SHIP', 'HOLD']"])

    # Every pattern violated.
    broken = _valid_finding()
    broken["ruleId"] = "Missed_Parallel"
    got = validate_finding(broken)
    check("ruleId pattern violated refused",
          (len(got), got and got[0].startswith("ruleId:")), (1, True))
    broken = _valid_finding()
    broken["location"] = "tools/example.py"
    got = validate_finding(broken)
    check("location pattern violated refused",
          (len(got), got and got[0].startswith("location:")), (1, True))
    broken = _valid_finding()
    broken["fingerprint"] = "MISSED:tools/example.py:42"
    got = validate_finding(broken)
    check("fingerprint pattern violated refused",
          (len(got), got and got[0].startswith("fingerprint:")), (1, True))
    # ECMA end-anchor semantics: a trailing newline refuses (fullmatch).
    broken = _valid_finding()
    broken["location"] = "tools/example.py:42\n"
    check("location with trailing newline refused (ECMA anchor semantics)",
          len(validate_finding(broken)), 1)

    # additionalProperties: false, all four object surfaces.
    broken = _valid_finding()
    broken["severity"] = "high"
    check("finding extra field refused", validate_finding(broken),
          ["unexpected field (additionalProperties: false): severity"])
    broken = _valid_verdict()
    broken["comment"] = "x"
    check("verdict extra field refused", validate_verdict(broken),
          ["unexpected field (additionalProperties: false): comment"])
    broken = _valid_verdict()
    broken["counts"]["info"] = 0
    check("counts extra field refused", validate_verdict(broken),
          ["counts.info: unexpected field (additionalProperties: false)"])
    broken = _valid_verdict()
    broken["proof_of_run"]["duration"] = 1
    check("proof_of_run extra field refused", validate_verdict(broken),
          ["proof_of_run.duration: unexpected field (additionalProperties: false)"])

    # Type, minimum, and minLength refusals.
    broken = _valid_finding()
    broken["evidence"] = ""
    check("empty evidence refused", validate_finding(broken),
          ["evidence: shorter than minLength 1"])
    broken = _valid_finding()
    broken["tool"] = 7
    check("non-string tool refused", validate_finding(broken),
          ["tool: expected a string, got int"])
    broken = _valid_verdict()
    broken["counts"]["error"] = True
    check("boolean count refused (bool is not a JSON integer)",
          validate_verdict(broken),
          ["counts.error: expected an integer, got bool"])
    broken = _valid_verdict()
    broken["counts"]["note"] = -1
    check("negative count refused", validate_verdict(broken),
          ["counts.note: -1 is below minimum 0"])
    broken = _valid_verdict()
    broken["proof_of_run"]["files_read"] = -2
    check("negative files_read refused", validate_verdict(broken),
          ["proof_of_run.files_read: -2 is below minimum 0"])
    broken = _valid_verdict()
    broken["proof_of_run"]["commands_run"] = "ls"
    check("non-array commands_run refused", validate_verdict(broken),
          ["proof_of_run.commands_run: expected an array, got str"])
    broken = _valid_verdict()
    broken["proof_of_run"]["checks_passed"] = ["ok", 3]
    check("non-string checks_passed item refused", validate_verdict(broken),
          ["proof_of_run.checks_passed[1]: expected a string, got int"])
    broken = _valid_verdict()
    broken["head"] = "abc123"
    check("short head refused", validate_verdict(broken),
          ["head: shorter than minLength 7"])
    broken = _valid_verdict()
    broken["model"] = ""
    check("empty model refused", validate_verdict(broken),
          ["model: shorter than minLength 1"])
    broken = _valid_verdict()
    broken["counts"] = [0, 1, 0]
    check("non-object counts refused", validate_verdict(broken),
          ["counts: expected an object, got list"])
    broken = _valid_verdict()
    broken["proof_of_run"] = None
    check("non-object proof_of_run refused", validate_verdict(broken),
          ["proof_of_run: expected an object, got NoneType"])

    # Non-object top level.
    check("non-object finding refused", validate_finding(["x"]),
          ["top-level value is not a JSON object"])
    check("non-object verdict refused", validate_verdict("x"),
          ["top-level value is not a JSON object"])

    # Counts-mismatch cross-check.
    mismatch = _valid_verdict()
    mismatch["counts"] = {"error": 2, "warning": 0, "note": 0}
    check("counts mismatch refused",
          check_counts_match(mismatch, [_valid_finding()]),
          ["counts.error: verdict says 2, the attached finding set has 0",
           "counts.warning: verdict says 0, the attached finding set has 1"])
    check("counts mismatch against empty set refused",
          check_counts_match(mismatch, []) != [], True)
    malformed = _valid_verdict()
    malformed["counts"] = {"error": "2", "warning": 0, "note": 0}
    check("malformed counts skips cross-check (validate_verdict owns it)",
          check_counts_match(malformed, []), [])
    invalid_level = _valid_finding()
    invalid_level["level"] = "critical"
    check("invalid-level finding excluded from tally",
          check_counts_match(_valid_verdict(), [_valid_finding(), invalid_level]),
          [])

    print(f"self-test: {total[0] - len(failures)}/{total[0]} passed")
    return 1 if failures else 0


# --- CLI ------------------------------------------------------------------------------
def _read_json(path: str):
    """(value, None) on success; (None, message) on unreadable/unparseable."""
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh), None
    except OSError as exc:
        return None, f"cannot read {path}: {exc}"
    except json.JSONDecodeError as exc:
        return None, f"cannot parse {path} as JSON: {exc}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json_file", nargs="?",
                    help="the finding or verdict JSON file to validate")
    ap.add_argument("--kind", choices=("finding", "verdict"),
                    help="which artefact class the JSON file holds")
    ap.add_argument("--findings", metavar="FILE",
                    help="beside --kind verdict only: a JSON array of finding "
                         "objects; each is validated and the envelope's counts "
                         "are cross-checked against the set")
    ap.add_argument("--self-test", action="store_true",
                    help="run the synthetic-fixture unit tests")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.json_file or not args.kind:
        ap.error("--kind finding|verdict and a JSON file are required "
                 "unless --self-test is given")
    if args.findings and args.kind != "verdict":
        ap.error("--findings only applies beside --kind verdict")

    obj, err = _read_json(args.json_file)
    if err:
        print(f"ERROR: {err}")
        return 2

    errors: list[str] = []
    if args.kind == "finding":
        errors.extend(validate_finding(obj))
    else:
        errors.extend(validate_verdict(obj))
        if args.findings:
            findings, err = _read_json(args.findings)
            if err:
                print(f"ERROR: {err}")
                return 2
            if not isinstance(findings, list):
                errors.append("findings file: top-level value is not a JSON array")
            else:
                for i, finding in enumerate(findings):
                    for msg in validate_finding(finding):
                        errors.append(f"findings[{i}]: {msg}")
                errors.extend(check_counts_match(obj, findings))

    if errors:
        for msg in errors:
            print(msg)
        return 1
    print(f"OK: {args.json_file} is a valid {args.kind}"
          + (f" (finding set cross-checked: {args.findings})" if args.findings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
