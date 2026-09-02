#!/usr/bin/env python3
"""Gate 97: verdict-recording carrier-completeness for verdict-bearing skills.

A skill that adjudicates a per-item verdict (matrix-fit, claim-fit) restates its
verdict-recording CONTRACT in many carriers: the judge-output step, the record and
report steps, the Verification completion bullets, the Red Flags and Common
Rationalizations, and the paired command's reject rule and report-back. When a change
adds a REQUIRED field to that contract (PR #1926 added a held-source ``path:line``
citation), every carrier must carry it, and any per-verdict-type EXCEPTION (a
``source-not-held`` verdict legitimately has no held-source ``path:line``, citing the
failed index lookup instead) must be expressed wherever the requirement is stated, or
the carrier is internally contradictory. #1926 cost four adversarial-QA rounds because
that completeness was applied carrier-by-carrier and verified by expensive workers; this
gate mechanizes it.

Two checks, driven by ``tools/skill-verdict-fields.json`` (which declares, per enrolled
skill, the required field token set, its exception, and a carrier-signal regex):

  Check 1 (MISSING-FIELD): a unit matching the skill's ``carrier_signal`` must carry the
      required PRIMARY field (its ``requires_all`` substrings and ``requires_regex``
      patterns all satisfied), unless the unit carries a reasoned exempt marker. The
      exception excuses NOTHING here: the primary is the baseline every carrier states.
  Check 2 (EXCEPTION-CONTRADICTION): a CARRIER unit whose primary field is fully present,
      where the field's exception is ``mandatory_with_primary``, must ALSO carry the
      exception (or the exempt marker). A carrier asserting the requirement without its
      exception alternative is the contradiction #1926's rounds 2 to 4 kept surfacing.
      Restricted to carrier units, so mechanics prose that merely mentions the field
      tokens is not a false positive.

The exempt marker (``verdict-fields: exempt: <reason>``) suppresses both checks for a
unit that mentions the tokens in mechanics prose rather than a requirement statement; a
reasonless marker is itself a finding (mirrors gate 44's reasoned-opt-out).

This is a PROJECT-side gate keyed by a PROJECT-side manifest; adopters of the bare
guardrails pack do not inherit it (they inherit no gate), so the pack prose stays
canonical and unannotated. Complementary to gate 44 (paired-skill STEP parity): gate 44
proves the command represents the skill's step STRUCTURE; this gate proves specific
verdict-field CONTENT is present in every requirement-stating unit of BOTH files. Use a
distinct exempt-marker namespace (``verdict-fields: exempt:``) so the two escapes never
blur.

COVERAGE AND RESIDUES (stated plainly, per the project's anti-false-completeness stance).
The carrier signal matches the OPERATIVE recording carriers (the judge-output step, the
record/surface step, the Verification completion bullets, and the paired command's reject
rule and report-back) plus the stale-note Red Flag. It deliberately does NOT match a
pedagogical restatement that carries no signal phrase (a Common Rationalization table row),
so a required field dropped from such a row is not caught; those rows are pedagogy, not the
operative contract. Granularity is the UNIT (a list item, a table row, or a paragraph):
within one multi-requirement paragraph, an exception dropped from a single sentence is
masked if the exception phrase recurs elsewhere in that paragraph. The project's
one-requirement-per-unit editorial discipline mitigates this, and the #1926 failures were
ACROSS separate carriers, which the per-unit check DOES catch. The field is matched by a
DISCRIMINATING regex (the held-source ``path:line`` phrase), not the bare tokens ``held``
and ``path:line`` which also occur inside ``source-not-held`` and the claim ``path:line``.
A carrier_signal that matches ZERO carriers for an enrolled skill is caught FAIL-CLOSED by the tool itself (exit 2, per-skill), with the standing regression assertion on the live census a defence-in-depth second layer. The remaining residues are covered by the same-PR grep-every-carrier discipline.

Exit 0 clean, 1 on any finding, 2 on an environmental error: a missing or unparseable
manifest, a manifest-named file that does not exist, or a FAIL-CLOSED schema violation (no
skills; a skill missing files/carrier_signal/fields; an invalid carrier_signal or requires_regex
pattern; a field or declared exception with no valid predicate, where a predicate is a non-empty
LIST of non-empty strings; or an enrolled skill whose signal matches zero carriers). A vacuous
manifest or a vacuous signal must refuse, not pass silently.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "tools" / "skill-verdict-fields.json"

_FENCE = re.compile(r"^\s*(```|~~~)")
_HEADING = re.compile(r"^\s{0,3}#")
_UNIT_MARKER = re.compile(r"^\s*(?:[-*+]\s|\d+\.\s|\|)")


def segment_units(text):
    """Segment markdown into (start_line, unit_text) requirement-carrying units.

    A unit is a list item (with wrapped continuations), a table row, a heading line,
    or a paragraph (a run of lines between blanks). Fenced code and YAML frontmatter
    are excluded. The unit text joins its lines with single spaces so a multi-line
    carrier sentence is matched as one string.
    """
    lines = text.splitlines()
    # strip a leading YAML frontmatter block
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                lines = lines[j + 1:]
                offset = j + 1
                break
        else:
            offset = 0
    else:
        offset = 0

    units = []
    cur_start = None
    cur_lines = []
    in_fence = False

    def flush():
        nonlocal cur_start, cur_lines
        if cur_lines:
            units.append((cur_start, " ".join(s.strip() for s in cur_lines)))
        cur_start, cur_lines = None, []

    for idx, line in enumerate(lines):
        lineno = idx + 1 + offset
        if _FENCE.match(line):
            in_fence = not in_fence
            flush()
            continue
        if in_fence:
            continue
        if not line.strip():
            flush()
            continue
        if _HEADING.match(line):
            flush()
            units.append((lineno, line.strip()))
            continue
        if _UNIT_MARKER.match(line):
            flush()
            cur_start, cur_lines = lineno, [line]
        else:
            if cur_start is None:
                cur_start, cur_lines = lineno, [line]
            else:
                cur_lines.append(line)
    flush()
    return units


def _exempt_state(unit_text, marker):
    """Return 'none', 'valid' (reasoned), or 'reasonless'."""
    if marker not in unit_text:
        return "none"
    m = re.search(re.escape(marker) + r"\s*:\s*(.*?)\s*(?:-->|$)", unit_text)
    if m and m.group(1).strip():
        return "valid"
    return "reasonless"


def _tokens_present(unit_text, tokens):
    low = unit_text.lower()
    return all(tok.lower() in low for tok in tokens)


def _field_satisfied(unit_text, spec):
    """Satisfied when ALL ``requires_all`` substrings are present AND ALL ``requires_regex``
    patterns match. A regex pins a DISCRIMINATING phrase (the held-source ``path:line``
    citation, distinct from the claim ``path:line`` and from the substring ``held`` inside
    ``source-not-held``); a bare substring set cannot tell those apart."""
    if spec.get("requires_all") and not _tokens_present(unit_text, spec["requires_all"]):
        return False
    for rx in spec.get("requires_regex", []):
        if not re.search(rx, unit_text):
            return False
    return True


def _field_label(spec):
    return " + ".join(list(spec.get("requires_all", [])) + list(spec.get("requires_regex", [])))


def _valid_predicates(spec):
    """A field/exception spec is a VALID predicate only if it declares at least one
    predicate entry and EVERY entry is a non-empty string. An empty list, an empty
    string, or a non-string entry is a vacuous predicate (matches everything) and is
    rejected fail-closed."""
    preds = []
    for key in ("requires_all", "requires_regex"):
        val = spec.get(key)
        if val is None:
            continue
        if not isinstance(val, list):
            return False  # a scalar string is not a predicate LIST (list("held") -> chars)
        preds.extend(val)
    return bool(preds) and all(isinstance(p, str) and p.strip() for p in preds)


def _regex_ok(spec):
    """Every ``requires_regex`` pattern must compile; an invalid pattern is a schema
    error (exit 2), not an uncaught traceback at match time."""
    import re as _re
    for rx in spec.get("requires_regex", []) or []:
        try:
            _re.compile(rx)
        except _re.error:
            return False
    return True


def check_skill(skill, marker, root):
    """Return a list of finding dicts for one enrolled skill (both its files)."""
    findings = []
    signal_re = re.compile(skill["carrier_signal"])
    for rel in skill["files"]:
        path = root / rel
        if not path.exists():
            findings.append({"file": rel, "line": 0, "cls": "env",
                             "msg": "manifest-named file does not exist"})
            continue
        text = path.read_text(encoding="utf-8")
        for start_line, unit in segment_units(text):
            state = _exempt_state(unit, marker)
            if state == "reasonless":
                findings.append({"file": rel, "line": start_line, "cls": "exempt-marker",
                                 "msg": "reasonless `%s` marker (needs `: <reason>`)" % marker})
                continue
            exempt = state == "valid"
            if exempt:
                continue
            is_carrier = bool(signal_re.search(unit))
            for field in skill["fields"]:
                primary_ok = _field_satisfied(unit, field)
                exc = field.get("exception")
                exc_ok = bool(exc) and _field_satisfied(unit, exc)
                if is_carrier and not primary_ok:
                    findings.append({
                        "file": rel, "line": start_line, "cls": "missing-field",
                        "msg": "[%s/%s] carrier unit lacks the required field (%s)"
                               % (skill["name"], field["name"], _field_label(field))})
                if (is_carrier and exc and exc.get("mandatory_with_primary")
                        and primary_ok and not exc_ok):
                    findings.append({
                        "file": rel, "line": start_line, "cls": "exception-contradiction",
                        "msg": "[%s/%s] unit states the requirement (%s) without its `%s` "
                               "exception (%s)"
                               % (skill["name"], field["name"], _field_label(field),
                                  exc["verdict"], _field_label(exc))})
    return findings


def run(manifest_path, root):
    """Return (exit_code, findings, n_skills, n_units_checked)."""
    try:
        manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("ENV ERROR: cannot load manifest %s: %s" % (manifest_path, exc),
              file=sys.stderr)
        return 2, [], 0, (0, 0)
    marker = manifest.get("exempt_marker", "verdict-fields: exempt")
    # Fail-closed schema validation: a vacuous manifest (no skills, a skill missing its
    # files/signal/fields, or a field with no predicate) would pass every carrier silently,
    # defeating the gate. Refuse it (the guard-input discipline: ignorance must REFUSE).
    skills = manifest.get("skills")
    if not skills:
        print("ENV ERROR: manifest declares no skills (would pass vacuously)", file=sys.stderr)
        return 2, [], 0, (0, 0)
    for _sk in skills:
        if not (_sk.get("files") and _sk.get("carrier_signal") and _sk.get("fields")):
            print("ENV ERROR: skill %r missing files/carrier_signal/fields" % _sk.get("name"),
                  file=sys.stderr)
            return 2, [], 0, (0, 0)
        try:
            re.compile(_sk["carrier_signal"])
        except re.error as _e:
            print("ENV ERROR: skill %r carrier_signal is an invalid regex: %s"
                  % (_sk.get("name"), _e), file=sys.stderr)
            return 2, [], 0, (0, 0)
        for _fl in _sk["fields"]:
            if not _valid_predicates(_fl):
                print("ENV ERROR: field %r has no valid predicate (a non-empty list of "
                      "requires_all/requires_regex strings)" % _fl.get("name"), file=sys.stderr)
                return 2, [], 0, (0, 0)
            if not _regex_ok(_fl):
                print("ENV ERROR: field %r has an invalid requires_regex pattern"
                      % _fl.get("name"), file=sys.stderr)
                return 2, [], 0, (0, 0)
            _ex = _fl.get("exception")
            if _ex is not None and (not _valid_predicates(_ex) or not _regex_ok(_ex)):
                print("ENV ERROR: exception on field %r has no valid predicate / an invalid "
                      "regex" % _fl.get("name"), file=sys.stderr)
                return 2, [], 0, (0, 0)
    all_findings = []
    n_scanned = 0
    n_carriers = 0
    for skill in manifest.get("skills", []):
        signal_re = re.compile(skill["carrier_signal"])
        skill_carriers = 0
        skill_has_file = False
        for rel in skill["files"]:
            p = root / rel
            if not p.exists():
                continue
            skill_has_file = True
            for _ln, unit in segment_units(p.read_text(encoding="utf-8")):
                n_scanned += 1
                if signal_re.search(unit):
                    n_carriers += 1
                    skill_carriers += 1
        if skill_has_file and skill_carriers == 0:
            print("ENV ERROR: skill %r matched ZERO carrier units across its files; its "
                  "carrier_signal is vacuous (would pass silently)" % skill.get("name"),
                  file=sys.stderr)
            return 2, [], 0, (n_scanned, n_carriers)
        all_findings.extend(check_skill(skill, marker, root))
    if any(f["cls"] == "env" for f in all_findings):
        for f in all_findings:
            if f["cls"] == "env":
                print("ENV ERROR: %s: %s" % (f["file"], f["msg"]), file=sys.stderr)
        return 2, all_findings, len(manifest.get("skills", [])), (n_scanned, n_carriers)
    return (1 if all_findings else 0), all_findings, len(manifest.get("skills", [])), (n_scanned, n_carriers)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    ap.add_argument("--root", default=str(REPO_ROOT))
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return _self_test()
    code, findings, n_skills, counts = run(args.manifest, Path(args.root))
    n_scanned, n_carriers = counts
    print("=== skill verdict-recording carrier-completeness audit ===")
    for f in findings:
        if f["cls"] != "env":
            print("  %s:%d %s: %s" % (f["file"], f["line"], f["cls"], f["msg"]),
                  file=sys.stderr)
    if code == 0:
        print("OK: %d skill(s), %d unit(s) scanned, %d carrier unit(s) checked; every "
              "required verdict field is present in every matched carrier." % (n_skills, n_scanned, n_carriers))
    elif code == 1:
        print("\nFAIL: %d verdict-carrier finding(s). A carrier that states a verdict "
              "requirement must carry the required field token(s) and any "
              "mandatory-with-primary exception, or a reasoned `verdict-fields: exempt: "
              "<reason>` marker. Fix the carrier; do not weaken the manifest."
              % len([x for x in findings if x["cls"] != "env"]), file=sys.stderr)
    return code


def _self_test():
    import tempfile
    cases = 0
    fails = 0

    def check(desc, files, manifest, expect_code):
        nonlocal cases, fails
        cases += 1
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for rel, body in files.items():
                p = root / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(body, encoding="utf-8")
            mpath = root / "manifest.json"
            mpath.write_text(json.dumps(manifest), encoding="utf-8")
            code, _f, _s, _u = run(str(mpath), root)
            ok = code == expect_code
            print(("PASS" if ok else "FAIL") + ": " + desc
                  + (" (got %d want %d)" % (code, expect_code) if not ok else ""))
            if not ok:
                fails += 1

    HELD_RX = r"(?i)(?:held[- ]source|reference-base)[^\n]{0,60}path:line"
    FIELD_WITH_EXC = {
        "name": "held-src", "requires_regex": [HELD_RX],
        "exception": {"verdict": "source-not-held", "requires_all": ["index lookup"],
                      "mandatory_with_primary": True}}
    SIGNAL = "(?i)(every verdict|verdicts? without|reject any|report back:)"

    def man(fields):
        return {"version": 1, "exempt_marker": "verdict-fields: exempt",
                "skills": [{"name": "t", "files": ["s.md"], "carrier_signal": SIGNAL,
                            "fields": fields}]}

    # 1. missing-field: a carrier unit lacking the field
    check("missing-field carrier fails",
          {"s.md": "## H\n\n- Every verdict cites the quoted passage.\n"},
          man([FIELD_WITH_EXC]), 1)
    # 2. exception-contradiction: primary present, mandatory exception absent
    check("exception-contradiction fails",
          {"s.md": "## H\n\n- Every verdict cites the held source `path:line`; a verdict "
                   "without it is rejected.\n"},
          man([FIELD_WITH_EXC]), 1)
    # 3. legitimate carrier stating the primary AND its exception passes
    check("carrier with primary and exception passes",
          {"s.md": "## H\n\n- Every verdict cites the held source `path:line` (or, for "
                   "source-not-held, the executed index lookup that returned nothing).\n"},
          man([FIELD_WITH_EXC]), 0)
    # 3b. a carrier with ONLY the exception (no primary held-source path:line) FAILS:
    #     the primary is the baseline, the exception excuses nothing (check-1-requires-primary).
    check("carrier with only the exception (no primary) fails",
          {"s.md": "## H\n\n- Every verdict cites, for source-not-held, the executed index "
                   "lookup that returned nothing.\n"},
          man([FIELD_WITH_EXC]), 1)
    # 3c. an empty-reason exempt marker (`: -->`) is reasonless and FAILS (parser bug guard)
    check("empty-reason exempt marker (: -->) fails",
          {"s.md": "## H\n\n- Every verdict cites the held source `path:line` (or, for `source-not-held`, the executed index lookup that returned nothing).\n- The held source `path:line`. <!-- verdict-fields: exempt: -->\n"},
          man([FIELD_WITH_EXC]), 1)
    # 4a. reasoned exempt marker passes
    check("reasoned exempt marker passes",
          {"s.md": "## H\n\n- Every verdict cites the held source `path:line` (or, for `source-not-held`, the executed index lookup that returned nothing).\n- The `path:line` comes from opening the held file. "
                   "<!-- verdict-fields: exempt: mechanics prose, not a requirement -->\n"},
          man([FIELD_WITH_EXC]), 0)
    # 4b. reasonless exempt marker fails
    check("reasonless exempt marker fails",
          {"s.md": "## H\n\n- Every verdict cites the held source `path:line` (or, for `source-not-held`, the executed index lookup that returned nothing).\n- The held source `path:line`. <!-- verdict-fields: exempt -->\n"},
          man([FIELD_WITH_EXC]), 1)
    # 5. environmental: missing manifest file
    with tempfile.TemporaryDirectory() as td:
        cases += 1
        code, _f, _s, _u = run(str(Path(td) / "nope.json"), Path(td))
        ok = code == 2
        print(("PASS" if ok else "FAIL") + ": missing manifest -> exit 2"
              + (" (got %d)" % code if not ok else ""))
        if not ok:
            fails += 1
    # 6. non-carrier unit lacking the field passes (not a requirement statement)
    check("non-carrier unit without field passes",
          {"s.md": "## H\n\n- Every verdict cites the held source `path:line` (or, for `source-not-held`, the executed index lookup that returned nothing).\n- The judge reads the source title from the catalogue.\n"},
          man([{"name": "hp", "requires_regex": [HELD_RX]}]), 0)
    # 7. field with no exception: carrier with primary passes
    check("no-exception field, carrier with primary passes",
          {"s.md": "## H\n\n- Every verdict cites the held source `path:line`.\n"},
          man([{"name": "hp", "requires_regex": [HELD_RX]}]), 0)
    # 8. manifest-named file missing -> env exit 2
    with tempfile.TemporaryDirectory() as td:
        cases += 1
        mpath = Path(td) / "m.json"
        mpath.write_text(json.dumps(man([FIELD_WITH_EXC])), encoding="utf-8")
        code, _f, _s, _u = run(str(mpath), Path(td))
        ok = code == 2
        print(("PASS" if ok else "FAIL") + ": manifest-named file missing -> exit 2"
              + (" (got %d)" % code if not ok else ""))
        if not ok:
            fails += 1

    # 9. fail-closed: empty manifest (no skills) -> exit 2
    with tempfile.TemporaryDirectory() as td:
        cases += 1
        mp = Path(td) / "m.json"; mp.write_text(json.dumps({"version": 1, "skills": []}))
        code, _f, _s, _u = run(str(mp), Path(td))
        ok = code == 2
        print(("PASS" if ok else "FAIL") + ": empty manifest (no skills) -> exit 2"
              + (" (got %d)" % code if not ok else ""))
        if not ok:
            fails += 1
    # 10. fail-closed: a field with no predicate -> exit 2
    with tempfile.TemporaryDirectory() as td:
        cases += 1
        (Path(td) / "s.md").write_text("## H\n\n- Every verdict cites something.\n")
        mp = Path(td) / "m.json"
        mp.write_text(json.dumps({"version": 1, "exempt_marker": "verdict-fields: exempt",
                                  "skills": [{"name": "t", "files": ["s.md"],
                                              "carrier_signal": SIGNAL,
                                              "fields": [{"name": "empty"}]}]}))
        code, _f, _s, _u = run(str(mp), Path(td))
        ok = code == 2
        print(("PASS" if ok else "FAIL") + ": field with no predicate -> exit 2"
              + (" (got %d)" % code if not ok else ""))
        if not ok:
            fails += 1

    # 11. fail-closed: an explicitly-empty exception object {} -> exit 2
    with tempfile.TemporaryDirectory() as td:
        cases += 1
        (Path(td) / "s.md").write_text("## H\n\n- Every verdict cites something.\n")
        mp = Path(td) / "m.json"
        mp.write_text(json.dumps({"version": 1, "exempt_marker": "verdict-fields: exempt",
                                  "skills": [{"name": "t", "files": ["s.md"],
                                              "carrier_signal": SIGNAL,
                                              "fields": [{"name": "f", "requires_regex": [HELD_RX],
                                                          "exception": {}}]}]}))
        code, _f, _s, _u = run(str(mp), Path(td))
        ok = code == 2
        print(("PASS" if ok else "FAIL") + ": empty exception {} -> exit 2"
              + (" (got %d)" % code if not ok else ""))
        if not ok:
            fails += 1
    # 12. fail-closed: an empty-STRING predicate (matches everything) -> exit 2
    with tempfile.TemporaryDirectory() as td:
        cases += 1
        (Path(td) / "s.md").write_text("## H\n\n- Every verdict cites something.\n")
        mp = Path(td) / "m.json"
        mp.write_text(json.dumps({"version": 1, "exempt_marker": "verdict-fields: exempt",
                                  "skills": [{"name": "t", "files": ["s.md"],
                                              "carrier_signal": SIGNAL,
                                              "fields": [{"name": "f", "requires_all": [""]}]}]}))
        code, _f, _s, _u = run(str(mp), Path(td))
        ok = code == 2
        print(("PASS" if ok else "FAIL") + ": empty-string predicate -> exit 2"
              + (" (got %d)" % code if not ok else ""))
        if not ok:
            fails += 1

    # 13. fail-closed: a SCALAR-STRING predicate (list("held") -> chars) -> exit 2
    check("scalar-string predicate -> exit 2",
          {"s.md": "## H\n\n- Every verdict cites the held source `path:line`.\n"},
          man([{"name": "f", "requires_all": "held"}]), 2)
    # 14. fail-closed: an INVALID requires_regex pattern -> exit 2 (not a traceback)
    check("invalid requires_regex -> exit 2",
          {"s.md": "## H\n\n- Every verdict cites the held source `path:line`.\n"},
          man([{"name": "f", "requires_regex": ["("]}]), 2)
    # 15. fail-closed: one enrolled skill with a NEVER-MATCH signal (0 carriers) -> exit 2,
    #     even though the other skill supplies carriers (per-skill, not aggregate).
    with tempfile.TemporaryDirectory() as td:
        cases += 1
        (Path(td) / "a.md").write_text("## H\n\n- Every verdict cites the held source "
                                       "`path:line` (or, for source-not-held, the index lookup).\n")
        (Path(td) / "b.md").write_text("## H\n\n- Nothing here.\n")
        mp = Path(td) / "m.json"
        mp.write_text(json.dumps({"version": 1, "exempt_marker": "verdict-fields: exempt",
                                  "skills": [
                                      {"name": "ok", "files": ["a.md"], "carrier_signal": SIGNAL,
                                       "fields": [{"name": "f", "requires_regex": [HELD_RX]}]},
                                      {"name": "vac", "files": ["b.md"], "carrier_signal": "(?!)",
                                       "fields": [{"name": "f", "requires_regex": [HELD_RX]}]}]}))
        code, _f, _s, _u = run(str(mp), Path(td))
        ok = code == 2
        print(("PASS" if ok else "FAIL") + ": per-skill never-match signal -> exit 2"
              + (" (got %d)" % code if not ok else ""))
        if not ok:
            fails += 1

    print("\n%d/%d self-test case(s) passed." % (cases - fails, cases))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
