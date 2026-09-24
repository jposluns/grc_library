#!/usr/bin/env python3
"""Generate the section 7.1 publisher table from its machine-readable source of record (gate 102).

The citation-verification specification's section 7.1 carries one fenced ``json citation-publishers``
block (the source of record, parsed strictly by ``tools/citation_publishers.py``). This tool renders
the human-readable GFM table from it and writes it between the ``BEGIN-GENERATED
citation-publishers`` / ``END-GENERATED citation-publishers`` sentinels in the same section. The
table is generated, never hand-edited; ``--check`` (gate 102) fails on any drift, so the table a
reader sees and the data the gates read cannot diverge.

Usage:
    python3 tools/build-citation-publishers.py            # regenerate the table in place
    python3 tools/build-citation-publishers.py --check    # exit 1 on drift, 2 on malformed input
    python3 tools/build-citation-publishers.py --self-test

Exit codes: 0 in sync (or regenerated); 1 drift under --check; 2 malformed or missing source of
record, sentinels, or specification.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
from citation_publishers import BEGIN, END, InputError, _fence_scan, parse_block, render, section_bounds, source_span  # noqa: E402
from lint_common import strict_flags  # noqa: E402

SPEC = REPO_ROOT / "governance" / "specification-citation-verification.md"


def regenerate(text: str) -> str:
    """The specification text with the generated region replaced by the rendered table."""
    start, end = section_bounds(text)
    nb, ne = text.count(BEGIN), text.count(END)
    if nb != 1 or ne != 1:
        raise InputError(f"expected exactly one sentinel pair, found {nb} BEGIN and {ne} END")
    lines = text.split("\n")
    fenced, _ = _fence_scan(lines)
    for marker in (BEGIN, END):
        at = [k for k, line in enumerate(lines) if line == marker and k not in fenced]
        if len(at) != 1:
            raise InputError(f"the sentinel {marker} must be a whole line of its own, outside code blocks")
    b, e = text.index(BEGIN), text.index(END)
    if not (start <= b < e < end):
        raise InputError("the sentinel pair must be in order and inside section 7.1")
    # The generated region must not overlap ANY part of the source block, or regenerating would
    # erase some or all of it.
    src_start, src_end = source_span(text)
    if b < src_end and src_start < e + len(END):
        raise InputError("the json citation-publishers block must not overlap the generated region")
    table = render(parse_block(text))
    return text[: b + len(BEGIN)] + "\n\n" + table + "\n" + text[e:]


def main(argv: list[str]) -> int:
    # 3b50b2a: parse strictly before anything else. A membership test used to let a mistyped
    # --check fall through to the in-place WRITE below (exit 0, spec regenerated, no check run).
    flags = strict_flags(argv, ("--check", "--self-test"))
    if flags == {"--check", "--self-test"}:
        print("ERROR: --check and --self-test are separate runs; give one.", file=sys.stderr)
        return 2
    if "--self-test" in flags:
        return self_test()
    try:
        text = SPEC.read_bytes().decode("utf-8")
        if "\r" in text or text.startswith("\ufeff"):
            raise InputError("the specification must use LF line endings without a BOM")
        new = regenerate(text)
    except (InputError, OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if "--check" in flags:
        if new != text:
            print(
                "FAIL: the section 7.1 publisher table is out of sync with its json citation-publishers "
                "block. Edit the block, then run `python3 tools/build-citation-publishers.py`; never "
                "hand-edit the generated table.",
                file=sys.stderr,
            )
            return 1
        print("OK: section 7.1 publisher table is in sync with its source of record.")
        return 0
    if new != text:
        SPEC.write_bytes(new.encode("utf-8"))
        print("Regenerated the section 7.1 publisher table.")
    else:
        print("OK: section 7.1 publisher table already in sync.")
    return 0


def self_test() -> int:
    fence = "```"
    block = (
        fence + "json citation-publishers\n"
        '[{"publisher": "ISO", "domains": ["iso.org"], "covers": "ISO standards."},\n'
        ' {"publisher": "NIST", "domains": ["nist.gov", "csrc.nist.gov"], "covers": "NIST SP."}]\n'
        + fence + "\n"
    )
    table = (
        "| Publisher | Canonical domain | Standards covered |\n| --- | --- | --- |\n"
        "| ISO | `iso.org` | ISO standards. |\n| NIST | `nist.gov`, `csrc.nist.gov` | NIST SP. |\n"
    )
    doc = "# T\n\n### 7.1 Initial allow-list\n\nIntro.\n\n" + BEGIN + "\n\nstale\n\n" + END + "\n\n" + block + "\n### 7.2 Next\n"
    cases = []

    def case(name, fn):
        try:
            cases.append((name, fn()))
        except Exception as exc:  # a crash is a failure, reported by name
            cases.append((name, f"raised {type(exc).__name__}: {exc}"))

    case("renders the table between the sentinels", lambda: table in regenerate(doc))
    case("regeneration is idempotent", lambda: regenerate(regenerate(doc)) == regenerate(doc))
    case("only the region changes", lambda: "stale" not in regenerate(doc)
         and regenerate(doc).startswith("# T\n\n### 7.1 Initial allow-list\n\nIntro.\n\n" + BEGIN)
         and regenerate(doc).endswith(END + "\n\n" + block + "\n### 7.2 Next\n"))

    def refuses(mutated, fragment):
        def run():
            try:
                regenerate(mutated)
            except InputError as exc:
                return fragment in str(exc)
            return False
        return run

    case("missing sentinels refused", refuses(doc.replace(BEGIN, ""), "sentinel pair"))
    case("duplicated sentinel pair refused", refuses(doc + BEGIN + END, "sentinel pair"))
    case("reversed sentinels refused", refuses(
        doc.replace(BEGIN, "@@B@@").replace(END, BEGIN).replace("@@B@@", END), "in order"))
    case("sentinels outside 7.1 refused", refuses(
        doc.replace("### 7.1 Initial allow-list\n\nIntro.\n\n" + BEGIN, BEGIN + "\n### 7.1 Initial allow-list\n\nIntro.\n\n"),
        "inside section 7.1"))
    case("missing block refused", refuses(doc.replace(fence + "json citation-publishers", fence + "json"), "exactly one"))
    case("two blocks refused", refuses(doc.replace("### 7.2", block + "### 7.2"), "exactly one"))
    case("malformed JSON refused", refuses(doc.replace('"covers": "NIST SP."}]', '"covers": "NIST SP."},]'), "malformed JSON"))
    case("duplicate key refused", refuses(doc.replace('"covers": "ISO standards."', '"covers": "a", "covers": "b"'), "duplicate key"))
    case("unknown key refused", refuses(doc.replace('"covers": "ISO standards."', '"covers": "x", "note": "y"'), "exactly the keys"))
    case("duplicate domain refused", refuses(doc.replace('["nist.gov", "csrc.nist.gov"]', '["nist.gov", "iso.org"]'), "duplicate domain"))
    case("duplicate publisher refused", refuses(doc.replace('"publisher": "NIST"', '"publisher": "ISO"'), "duplicate publisher"))
    case("non-canonical domain refused", refuses(doc.replace('"iso.org"', '"ISO.org"'), "canonical lowercase host"))
    case("scheme in domain refused", refuses(doc.replace('"iso.org"', '"https://iso.org"'), "canonical lowercase host"))
    case("pipe in covers refused", refuses(doc.replace("ISO standards.", "ISO | IEC"), "pipe"))
    case("NaN refused", refuses(doc.replace('["iso.org"]', '["iso.org", NaN]'), "non-finite"))
    case("empty domains refused", refuses(doc.replace('["iso.org"]', "[]"), "non-empty array"))
    case("block inside the generated region refused (regeneration would erase it)",
         refuses(doc.replace(block, "").replace(END, block + END), "overlap"))
    case("sentinel inside a JSON string refused (partial overlap would erase the source)",
         refuses(doc.replace(BEGIN + "\n", "").replace('"ISO standards."', '"' + BEGIN + '"')
                 .replace(block, block + "\n"), "whole line"))
    case("sentinel line inside the source block refused",
         refuses(doc.replace(BEGIN + "\n\nstale\n\n", "")
                 .replace(' {"publisher": "NIST"', BEGIN + '\n {"publisher": "NIST"'), "whole line"))
    case("indented closing fence accepted", lambda: table in regenerate(doc.replace("}]\n" + fence + "\n", "}]\n  " + fence + "\n")))
    case("block outside 7.1 refused",
         refuses(doc.replace(block, "").replace("### 7.2 Next\n", "### 7.2 Next\n\n" + block), "not inside section 7.1"))
    bad = [name for name, ok in cases if ok is not True]
    for name, ok in cases:
        print(("PASS" if ok is True else "FAIL") + ": " + name + ("" if ok is True else f" ({ok})"))
    print(f"self-test: {len(cases) - len(bad)}/{len(cases)} passed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
