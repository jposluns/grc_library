#!/usr/bin/env python3
"""Generate the public reference-acquisition manifest (1.19.7 (closing PR #1007)).

The manifest [`docs/reference-acquisition-manifest.md`] is a PUBLIC BIBLIOGRAPHY of the
corpus's citation-source reference base: for each trusted-bucket entry in
`grc_library_ref/catalogue.yml` (standards / frameworks / legislation / programs) it lists
the title, version/edition, bucket, upstream URL, and acquisition class (free|licensed),
with the held source TEXT stripped. An adopter's `/adopt` uses it to bootstrap a `.ref`:
FREE sources are web-fetched, LICENSED sources are listed for manual acquisition.

**Copyright guardrail:** this reads ONLY catalogue bibliographic metadata (`title`,
`origin`/`body`/`jurisdiction`, `checked_edition`, `upstream_url`, `bucket`, `acquisition`);
it NEVER reads the held `--full-text` files nor the catalogue `notes`/`extract` fields, and
never reproduces source prose. The manifest is a bibliography, never the texts.

**Sibling-independence:** this is an ORCHESTRATOR/maintainer tool. It locates the real
`grc_library_ref` sibling via `lint_common.resolve_sibling("ref")` and NO-OPS (exit 0) when
that sibling is absent (an adopter's portable clone), so it is NEVER a CI gate and
`check-portability.sh` stays green. The maintainer-side `_ref`-required loud gate lives at
`/orch` (detect-env `ref_availability`), not here. The committed manifest ships statically,
so an adopter gets it without any sibling.

Usage:
  python3 tools/build-reference-manifest.py            # regenerate the committed manifest
  python3 tools/build-reference-manifest.py --check    # drift check (exit 1 if out of date)

`--check` is an orchestrator/maintainer drift check (it reads `_ref`), NOT a CI gate; run it
at `_ref`-update / resume, folded into the resync-`_ref` discipline.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_common  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "docs" / "reference-acquisition-manifest.md"
TRUSTED = ("standards", "frameworks", "legislation", "programs")
# Generator schema version: bump on a change to the manifest's SHAPE (columns,
# header), recorded in CHANGELOG.md. Not the library CalVer, and not the row
# contents (which advance with the reference base). The manifest is exempt from
# the date/version-staleness gates (like docs/portal.md), so this stays stable
# across content regens; the Date below is the reference base's own max currency.
SCHEMA_VERSION = "1.0.0"
FALLBACK_DATE = "2026-07-17"
BUCKET_LABEL = {
    "standards": "Standards",
    "frameworks": "Frameworks",
    "legislation": "Legislation",
    "programs": "Programs",
}


# The YAML 1.1 double-quoted escape set (the one yaml.safe_load implements), plus the three
# hex forms; \x, \u and \U carry 2, 4 and 8 hex digits (P-TODO 3b63).
_DQ_ESCAPES = {"0": "\0", "a": "\a", "b": "\b", "t": "\t", "\t": "\t", "n": "\n",
               "v": "\v", "f": "\f", "r": "\r", "e": "\x1b", " ": " ", '"': '"',
               "/": "/", "\\": "\\", "N": "\x85", "_": "\xa0", "L": "\u2028",
               "P": "\u2029"}
_DQ_HEX = {"x": 2, "u": 4, "U": 8}


def _unescape_double(s: str) -> str:
    """Unescape a YAML double-quoted scalar's backslash escapes: the named escapes and the
    \\x, \\u and \\U hex forms, matching yaml.safe_load for every escape YAML defines.
    An escape YAML does not define keeps its character (yaml.safe_load would raise instead);
    the catalogue is machine-generated and carries none."""
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            c = s[i + 1]
            width = _DQ_HEX.get(c)
            digits = s[i + 2:i + 2 + width] if width else ""
            if width and len(digits) == width and all(ch in "0123456789abcdefABCDEF"
                                                      for ch in digits):
                out.append(chr(int(digits, 16)))
                i += 2 + width
                continue
            out.append(_DQ_ESCAPES.get(c, c))
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def _scalar(v: str):
    """Parse a catalogue scalar value: strip a matched surrounding quote pair
    (unescaping YAML escapes per quote style), map bare booleans, else return the
    raw string; a bare null/~ is None and a bare decimal integer an int, as yaml.safe_load gives.
    (The audit toolchain is stdlib-only, so this hand-parses the catalogue rather than importing
    PyYAML.)"""
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] == '"':
        return _unescape_double(v[1:-1])
    if len(v) >= 2 and v[0] == v[-1] == "'":
        return v[1:-1].replace("''", "'")  # YAML single-quote escape
    if v == "true":
        return True
    if v == "false":
        return False
    # A bare null or ~ is YAML's null (yaml.safe_load gives None); a bare decimal integer is an
    # int. Without this, an unquoted null reached render() as the literal text "null" (3b63).
    if v in ("null", "~", "Null", "NULL", ""):
        return None
    if re.fullmatch(r"[-+]?(0|[1-9][0-9]*)", v):
        return int(v)
    return v


def _parse_catalogue(text: str) -> dict:
    """Minimal stdlib parser for grc_library_ref/catalogue.yml.

    The catalogue is machine-generated with a fixed, regular shape: top-level
    bucket keys at column 0 (`standards:`), list entries beneath them
    (`  - key: value`), and entry fields (`    key: value`). Values are quoted
    strings, bare scalars, or booleans; the one list field (`topics`) is stored
    verbatim and never read. Returns `{bucket: [entry_dict, ...]}`, matching the
    dict shape `render()`/`_max_date()` consume. This avoids a non-stdlib PyYAML
    dependency in the stdlib-only audit toolchain (no tool imports `yaml`)."""
    catalogue: dict = {}
    bucket = None
    entry = None
    # Split on the three ASCII line-break forms only. str.splitlines also splits on U+2028,
    # U+2029, U+0085 and other separators, which would truncate a value that carries one
    # (P-TODO 3b63). A raw one inside a quoted value is kept verbatim here, where
    # yaml.safe_load would fold it into a space; the catalogue carries none.
    for raw in re.split(r"\r\n|\r|\n", text):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*$", raw)  # top-level bucket opener
        if m:
            bucket = m.group(1)
            catalogue.setdefault(bucket, [])
            entry = None
            continue
        if bucket is None:  # pre-bucket top-level metadata scalars: skip
            continue
        m = re.match(r"^  - ([A-Za-z_][\w-]*):\s?(.*)$", raw)  # entry start
        if m:
            entry = {m.group(1): _scalar(m.group(2))}
            catalogue[bucket].append(entry)
            continue
        m = re.match(r"^    ([A-Za-z_][\w-]*):\s?(.*)$", raw)  # entry field
        if m and entry is not None:
            entry[m.group(1)] = _scalar(m.group(2))
    return catalogue


def _cell(v: str) -> str:
    """Escape a value for a markdown table cell (pipes; collapse line breaks, including a bare
    carriage return, which would otherwise split the row for any reader)."""
    return str(v).replace("|", "\\|").replace("\r\n", " ").replace("\r", " ").replace("\n", " ").strip()


def _issuer(bucket: str, e: dict) -> str:
    if bucket == "programs":
        return _cell(e.get("body", ""))
    if bucket == "legislation":
        return _cell(e.get("jurisdiction", ""))
    return _cell(e.get("origin", ""))


def _max_date(catalogue: dict) -> str:
    """Deterministic manifest Date: the max last_updated across trusted entries
    (the reference base's own currency), else FALLBACK_DATE. Not today() (which
    would break --check)."""
    dates = []
    for bucket in TRUSTED:
        for e in catalogue.get(bucket, []):
            for key in ("last_updated", "last_checked"):
                v = str(e.get(key, "") or "")
                if len(v) == 10 and v[4] == "-" and v[7] == "-":
                    dates.append(v)
    return max(dates) if dates else FALLBACK_DATE


def render(catalogue: dict) -> str:
    fields = [
        ("Document Title", "Reference-Acquisition Manifest"),
        ("Document Type", "Guide"),
        ("Version", SCHEMA_VERSION),
        ("Date", _max_date(catalogue)),
        ("Owner", "Governance Library Maintainer"),
        ("Approving Authority", "Governance Library Maintainer"),
        ("Related Documents", "[`README.md`](../README.md), "
         "[`docs/portal.md`](portal.md)"),
        ("Classification", "Public"),
        ("Category", "Documentation"),
        ("Review Frequency", "Regenerated from grc_library_ref/catalogue.yml on any "
         "reference-base change; maintainer-side, not a CI gate"),
        ("Repository Path", "[`docs/reference-acquisition-manifest.md`]"
         "(reference-acquisition-manifest.md)"),
        ("Confidentiality", "Public"),
        ("License", "CC BY-SA 4.0"),
    ]
    lines = [
        "<!--",
        "Auto-generated by tools/build-reference-manifest.py from "
        "grc_library_ref/catalogue.yml.",
        "Do not edit by hand. Regenerate with "
        "`python3 tools/build-reference-manifest.py`.",
        "-->",
        "",
        "# Reference-acquisition manifest",
        "",
    ]
    for i, (name, value) in enumerate(fields):
        suffix = "\\" if i < len(fields) - 1 else ""
        lines.append(f"**{name}:** {value}{suffix}")
    lines += [
        "",
        "---",
        "",
        "## Overview",
        "",
        "**Purpose.** A public bibliography of the citation-source reference base the GRC",
        "Library corpus draws on: the trusted, citation-grade sources (standards, frameworks,",
        "legislation, programs) the corpus cites as ground truth. It lists bibliographic",
        "metadata only, title, version, issuer, upstream URL, and acquisition class, so a fork",
        "adopting the library can acquire the sources it needs. It carries NO source text.",
        "",
        "**How `/adopt` uses it.** When a fork runs `/adopt`, the FREE-class sources are",
        "web-fetched into the adopter's reference sibling; the LICENSED-class sources are listed",
        "for manual acquisition (the adopter obtains them under their own licence). `/adopt`",
        "never redistributes licensed content.",
        "",
        "**Trust and scope.** Only the four citation-grade trusted buckets are listed; untrusted",
        "publications, recommendation-tier books, and scaffolding templates are excluded. The",
        "acquisition class is the source of truth held in `grc_library_ref`'s catalogue: FREE =",
        "freely and legally downloadable from the issuer; LICENSED = purchase, membership, or",
        "paywall required. A blank upstream URL means the catalogue does not yet record one.",
        "",
        "**Generated file, do not hand-edit.** Produced by `tools/build-reference-manifest.py`",
        "from `grc_library_ref/catalogue.yml`; regenerate on any reference-base change (the",
        "generator is maintainer-side, never a CI gate, so the public repo stays clonable",
        "without the private reference sibling).",
        "",
    ]
    total = 0
    free_total = 0
    for bucket in TRUSTED:
        entries = sorted(catalogue.get(bucket, []), key=lambda e: e["title"].lower())
        if not entries:
            continue
        free = sum(1 for e in entries if e.get("acquisition") == "free")
        lines += [
            f"## {BUCKET_LABEL[bucket]} ({len(entries)}: {free} free, {len(entries) - free} licensed)",
            "",
            "| Title | Version / edition | Issuer | Upstream URL | Acquisition |",
            "| --- | --- | --- | --- | --- |",
        ]
        for e in entries:
            title = _cell(e["title"])
            version = _cell(e.get("checked_edition", "") or "")
            issuer = _issuer(bucket, e)
            url = _cell(e.get("upstream_url", "") or "")
            acq = _cell(e.get("acquisition", "")).upper()
            lines.append(f"| {title} | {version} | {issuer} | {url} | {acq} |")
            total += 1
            if e.get("acquisition") == "free":
                free_total += 1
        lines.append("")
    lines += [
        f"**Total: {total} sources ({free_total} free, {total - free_total} licensed).**",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    # 3b50b2a: parse strictly first, so a mistyped --check can never fall through to the WRITE
    # below (and is refused even in an adopter clone, before the no-op branch).
    check = "--check" in lint_common.strict_flags(sys.argv[1:], ("--check",))
    ref = lint_common.resolve_sibling("ref")
    if ref is None:
        # Adopter / portable clone: no reference sibling. No-op (exit 0); the committed
        # manifest is used as-is. (Maintainer-side absence is caught loud at /orch.)
        note = ("build-reference-manifest: grc_library_ref not present; "
                "no-op (the committed manifest ships statically for adopters).")
        print(note)
        return 0
    catalogue_path = ref / "catalogue.yml"
    if not catalogue_path.is_file():
        print(f"build-reference-manifest: {catalogue_path} not found", file=sys.stderr)
        return 2
    catalogue = _parse_catalogue(catalogue_path.read_text(encoding="utf-8"))
    rendered = render(catalogue)
    if check:
        current = MANIFEST.read_text(encoding="utf-8") if MANIFEST.exists() else ""
        if current != rendered:
            print("build-reference-manifest --check: DRIFT, the committed manifest is out of "
                  "date with grc_library_ref's catalogue. Run "
                  "`python3 tools/build-reference-manifest.py` and commit.", file=sys.stderr)
            return 1
        print("build-reference-manifest --check: OK (manifest in sync with the reference base).")
        return 0
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(rendered, encoding="utf-8")
    print(f"build-reference-manifest: wrote {MANIFEST} ({rendered.count(chr(10))} lines).")
    return 0


if __name__ == "__main__":
    # Exit codes: 0 in sync, written, or no sibling; 1 --check DRIFT only; 2 catalogue missing or a
    # bad flag; 3 an unexpected internal error. Python's own uncaught-exception exit is 1, the same
    # as DRIFT, so an unexpected error is mapped to 3 to keep 1 meaning drift (P-TODO 3b62: the
    # pre-push guard reports drift from this code and must not misreport a crash as drift).
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 (deliberate: any unexpected failure becomes exit 3)
        import traceback
        traceback.print_exc()
        print(f"build-reference-manifest: internal error ({type(exc).__name__}); exit 3",
              file=sys.stderr)
        sys.exit(3)
