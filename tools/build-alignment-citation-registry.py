#!/usr/bin/env python3
"""Generate tools/alignment_citation_ids.json, the committed identifier catalogue that the
fabricated-citation existence gate (gate 96) validates OWASP ASVS and MITRE CWE citations
against (P-TODO P-1.63 part d).

The catalogue is extracted from the held sources in the grc_library_ref sibling:
- OWASP ASVS 5.0.0 requirements CSV (columns chapter_id, section_id, req_id), and the retained
  ASVS 4.0.3 requirements CSV under .superseded/ (same columns), each validated on its own and
  committed as its own family so the gate validates ASVS citations against the union of held
  editions (a legacy 4.0.3 identifier is not a fabrication);
- MITRE CWE 4.20 weaknesses CSV (column cwe_id; every status kept, deprecated included).
CI has no grc_library_ref, so the gate reads only this committed JSON. The JSON carries each
family's identifier counts and a SHA-512 digest over its metadata (name, edition, source) and
sorted identifiers; tools/alignment_citation_reference.py PINS the expected counts and digests
in code and refuses a JSON that differs, so a JSON-only edit (even one that recomputes the
stored digest) fails at load. After a deliberate regeneration for a new held edition, update
those pins from the values this generator prints. The generator refuses a source that breaks
the edition's structure (a requirement outside any section, a section outside any chapter) or
falls below a structural minimum, so a truncated source never yields an empty family.

Usage:
  python3 tools/build-alignment-citation-registry.py            # regenerate
  python3 tools/build-alignment-citation-registry.py --check    # exit 1 on drift, writes nothing
Exit codes: 0 in sync or written; 1 --check drift; 2 grc_library_ref absent or present but
unusable (not a directory, a dangling link, or one that cannot be examined, or a source in it
that cannot be examined, is not a regular file, cannot be read or is not valid UTF-8, 3b677), a
source file genuinely absent from a usable sibling, or a source malformed (missing column,
malformed or duplicate identifier, or CSV the csv module refuses, such as a field over its
limit; the message names the file, 3b677 r7, and the physical line the csv module was parsing
when it refused, 3b677 r8). The probes use os.lstat/os.stat, so the verdict is the same
on Python 3.11 and 3.12+. This is a
maintainer parity aid: --check needs the reference sibling and is not a CI gate.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_common  # noqa: E402

OUT = Path(__file__).resolve().parent / "alignment_citation_ids.json"
ASVS_SRC = "frameworks/OWASP/OWASP-ASVS-5.0.0-requirements.csv"
ASVS4_SRC = ".superseded/frameworks/OWASP/OWASP-ASVS-4.0.3-requirements.csv"
CWE_SRC = "frameworks/MITRE/CWE/CWE-4.20--weaknesses.csv"
_ASVS_REQ = re.compile(r"V\d+\.\d+\.\d+")
_ASVS_SEC = re.compile(r"V\d+\.\d+")
_ASVS_CH = re.compile(r"V\d+")
_CWE = re.compile(r"CWE-\d+")


def _vkey(v: str) -> tuple[int, ...]:
    return tuple(int(p) for p in v[1:].split("."))


def digest(meta: list[str], ids: list[str]) -> str:
    """SHA-512 over the family's metadata (name, edition, source) and its identifiers, each on
    its own line, in the committed (sorted) order."""
    return hashlib.sha512("\n".join(meta + ids).encode("utf-8")).hexdigest()


# Structural minimums: a truncated or header-only source must never yield an empty (and so
# silently disabled) family. The full editions are far above these floors (ASVS 5.0.0 has 345
# requirements, 80 sections, 17 chapters; CWE 4.20 has 969 weaknesses).
MIN_ASVS_REQS, MIN_ASVS_SECTIONS, MIN_ASVS_CHAPTERS, MIN_CWE = 300, 60, 14, 900
# ASVS 4.0.3 has 286 requirements, 69 sections, 14 chapters.
MIN_ASVS4_REQS, MIN_ASVS4_SECTIONS, MIN_ASVS4_CHAPTERS = 250, 55, 14


class _Undecodable(ValueError):
    """A held source in the sibling that is not valid UTF-8 (3b677)."""


class _CountedLines:
    """The file's physical lines, counted as the csv reader takes them (3b677 r8)."""

    def __init__(self, fh) -> None:
        self._fh = fh
        self.count = 0

    def __iter__(self) -> "_CountedLines":
        return self

    def __next__(self) -> str:
        line = next(self._fh)
        self.count += 1
        return line


def _read_csv(path: Path, needed: tuple[str, ...]) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        lines = _CountedLines(fh)
        try:
            reader = csv.DictReader(lines)
            missing = [c for c in needed if c not in (reader.fieldnames or [])]
            if missing:
                raise ValueError(f"{path.name}: missing column(s) {missing}")
            return list(reader)
        except csv.Error as exc:
            # 3b677 r7: csv.Error (a field over the csv module's limit, for example) is not a
            # ValueError, so it escaped main as a traceback naming no file; exit 2 naming it.
            # 3b677 r8: on csv.Error reader.line_num is still the end of the last completed
            # record, one too low for a one-line record and further off when a quoted field spans
            # lines. The reader raises while parsing the last line it took, so name that one.
            raise ValueError(f"{path}: malformed CSV at line {lines.count} ({exc})") from exc
        except UnicodeDecodeError as exc:
            # 3b677: name the source; the bare codec message names no file.
            raise _Undecodable(f"cannot decode {path} as UTF-8 ({exc.reason} at byte "
                               f"{exc.start})") from exc


def _unique(values: list[str], pattern: re.Pattern, label: str) -> None:
    bad = [v for v in values if not pattern.fullmatch(v)]
    if bad:
        raise ValueError(f"{label}: malformed identifier(s) {bad[:5]}")
    if len(set(values)) != len(values):
        raise ValueError(f"{label}: duplicate identifier(s)")


def _asvs(ref: Path, src: str, mins: tuple[int, int, int]) -> tuple[list, list, list]:
    rows = _read_csv(ref / src, ("chapter_id", "section_id", "req_id"))
    reqs = [r["req_id"].strip() for r in rows]
    _unique(reqs, _ASVS_REQ, "ASVS req_id")
    reqs = sorted(reqs, key=_vkey)
    sections = sorted({r["section_id"].strip() for r in rows}, key=_vkey)
    chapters = sorted({r["chapter_id"].strip() for r in rows}, key=_vkey)
    for label, vals, pat in (("ASVS section_id", sections, _ASVS_SEC),
                             ("ASVS chapter_id", chapters, _ASVS_CH)):
        _unique(vals, pat, label)
    for rq in reqs:
        if rq.rsplit(".", 1)[0] not in sections:
            raise ValueError(f"ASVS requirement {rq} has no section {rq.rsplit('.', 1)[0]}")
    for sec in sections:
        if sec.split(".")[0] not in chapters:
            raise ValueError(f"ASVS section {sec} has no chapter")
    if len(reqs) < mins[0] or len(sections) < mins[1] or len(chapters) < mins[2]:
        raise ValueError(f"ASVS source {src} looks truncated ({len(reqs)} requirements, "
                         f"{len(sections)} sections, {len(chapters)} chapters)")
    return reqs, sections, chapters


def _asvs_family(edition: str, src: str, lists: tuple[list, list, list]) -> dict:
    reqs, sections, chapters = lists
    return {
        "name": "OWASP ASVS",
        "edition": edition,
        "source": src,
        "requirements": reqs,
        "sections": sections,
        "chapters": chapters,
        "counts": {"requirements": len(reqs), "sections": len(sections), "chapters": len(chapters)},
        "sha512": digest(["OWASP ASVS", edition, src], reqs + sections + chapters),
    }


def build(ref: Path) -> dict:
    asvs5 = _asvs(ref, ASVS_SRC, (MIN_ASVS_REQS, MIN_ASVS_SECTIONS, MIN_ASVS_CHAPTERS))
    asvs4 = _asvs(ref, ASVS4_SRC, (MIN_ASVS4_REQS, MIN_ASVS4_SECTIONS, MIN_ASVS4_CHAPTERS))
    cwe_rows = _read_csv(ref / CWE_SRC, ("cwe_id",))
    cwes = [r["cwe_id"].strip() for r in cwe_rows]
    _unique(cwes, _CWE, "CWE cwe_id")
    cwes = sorted(cwes, key=lambda c: int(c[4:]))
    if len(cwes) < MIN_CWE:
        raise ValueError(f"CWE source looks truncated ({len(cwes)} weaknesses)")
    return {
        "_note": ("GENERATED by tools/build-alignment-citation-registry.py from grc_library_ref; "
                  "do not hand-edit (gate 96 verifies the counts and digests at load)."),
        "asvs": _asvs_family("5.0.0", ASVS_SRC, asvs5),
        "asvs4": _asvs_family("4.0.3", ASVS4_SRC, asvs4),
        "cwe": {
            "name": "MITRE CWE",
            "edition": "4.20",
            "source": CWE_SRC,
            "scope": "weaknesses (every status, deprecated included); categories and views are not held",
            "ids": cwes,
            "counts": {"ids": len(cwes)},
            "sha512": digest(["MITRE CWE", "4.20", CWE_SRC], cwes),
        },
    }


def render(data: dict) -> str:
    return json.dumps(data, indent=1, ensure_ascii=True) + "\n"


def main(argv: list[str]) -> int:
    check = "--check" in lint_common.strict_flags(argv[1:], ("--check",))
    try:
        # Strict (3b74): a present but unusable sibling is named as such, not reported as absent.
        ref = lint_common.resolve_sibling("ref", strict=True)
    except lint_common.InaccessiblePath as exc:
        print(f"build-alignment-citation-registry: the grc_library_ref sibling is present but "
              f"unusable ({exc}).", file=sys.stderr)
        return 2
    if ref is None:
        print("build-alignment-citation-registry: grc_library_ref is not present; clone it beside "
              "this repository or launch with --add-dir (this parity aid needs the held sources).",
              file=sys.stderr)
        return 2
    # 3b677: probe each source with strict_kind before the read, so one that cannot be examined
    # (an unsearchable sibling, a dangling link) is named as unusable, not reported missing.
    # 3b677 r6: level by level, so a missing source directory is still reported missing.
    for src in (ASVS_SRC, ASVS4_SRC, CWE_SRC):
        try:
            kind = lint_common.strict_kind_under(ref, src)
        except lint_common.InaccessiblePath as exc:
            print(f"build-alignment-citation-registry: the grc_library_ref sibling is present but "
                  f"unusable ({exc}).", file=sys.stderr)
            return 2
        if kind not in (None, "file"):
            print(f"build-alignment-citation-registry: the grc_library_ref sibling is present but "
                  f"unusable ({ref / src} is present but is not a regular file).", file=sys.stderr)
            return 2
    try:
        rendered = render(build(ref))
    except _Undecodable as exc:
        print(f"build-alignment-citation-registry: the grc_library_ref sibling is present but "
              f"unusable ({exc}).", file=sys.stderr)
        return 2
    except (FileNotFoundError, ValueError) as exc:
        print(f"build-alignment-citation-registry: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"build-alignment-citation-registry: the grc_library_ref sibling is present but "
              f"unusable ({exc}).", file=sys.stderr)
        return 2
    if check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != rendered:
            print("build-alignment-citation-registry --check: DRIFT, tools/alignment_citation_ids.json "
                  "is out of date with grc_library_ref. Run the generator and commit.", file=sys.stderr)
            return 1
        print("build-alignment-citation-registry --check: OK (registry in sync with the held sources).")
        return 0
    OUT.write_text(rendered, encoding="utf-8")
    data = json.loads(rendered)
    print(f"build-alignment-citation-registry: wrote {OUT.name}. Pins for "
          f"tools/alignment_citation_reference.py: ASVS {data['asvs']['counts']} "
          f"{data['asvs']['sha512']}; ASVS 4.0.3 {data['asvs4']['counts']} {data['asvs4']['sha512']}; CWE {data['cwe']['counts']} {data['cwe']['sha512']}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
