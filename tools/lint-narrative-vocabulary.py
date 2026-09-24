#!/usr/bin/env python3
"""Executive-narrative vocabulary audit - grc wrapper over the pack engine.

Flag narrative-vocabulary defects on executive pages: absolutes ("guarantee",
"eliminates", "makes impossible", "removes all risk" and inflections), an unqualified
"shall", and em/en dashes.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan (the
shall/dash/quote/link regexes + matching logic + the scan functions) is the source of
record in the pack engine (.corpus-management/tools/gate_lint_narrative_vocabulary.py);
it is vocabulary-free and takes the absolutes denylist + external-standard vocabulary via
configure(ref). This wrapper supplies the grc vocabulary, configures the engine, and keeps
the narrative scan scope (discover), the self-test, main, module-global shims
(scan_page_text / check_file), and the exit codes.
"""

from __future__ import annotations

import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path (engine imports aiqt_corpus)
from lint_common import CROSS_EXTERNAL_CONTEXT_RE, REPO_ROOT, guard_explicit_paths_cwd, positional_args, self_test_requested  # noqa: E402  # grc-config/store, stays local

import re  # noqa: E402  # for the grc absolutes denylist patterns below

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

# The absolutes denylist (spec, "Causal vocabulary"): the listed words plus
# their inflections. Lookbehind blocks hyphenated-identifier matches.
# Single-word absolutes: one token, cannot span a soft line break (checked per line).
ABSOLUTES_SINGLE: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("guarantee", re.compile(r"(?<![\w-])guarantee\w*", re.IGNORECASE)),
    ("eliminates", re.compile(r"(?<![\w-])eliminat\w*", re.IGNORECASE)),
)
# Multi-word absolutes: the phrase can wrap across a soft line break, so these are
# checked against the per-PARAGRAPH joined non-code text, not a single line.
ABSOLUTES_MULTI: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("makes impossible", re.compile(r"(?<![\w-])makes?\s+(?:\w+\s+){0,2}impossible", re.IGNORECASE)),
    ("removes all risk", re.compile(r"(?<![\w-])remov\w*\s+all\s+risk", re.IGNORECASE)),
)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_narrative_vocabulary  # the pack-owned engine (source of record)
    return gate_lint_narrative_vocabulary


# Configure the engine ONCE with the grc narrative vocabulary.
import types  # noqa: E402
_engine().configure(types.SimpleNamespace(
    absolutes_single=ABSOLUTES_SINGLE, absolutes_multi=ABSOLUTES_MULTI,
    cross_external_context_re=CROSS_EXTERNAL_CONTEXT_RE))


def scan_page_text(text: str) -> list:
    """Shim -> engine (engine already configured); kept module-global for the self-test."""
    return _engine().scan_page_text(text)


def check_file(path: Path, rel: str) -> list[str]:
    """Shim -> engine (engine already configured); kept module-global for the self-test + main."""
    return _engine().check_file(path, rel)


def discover(root: Path = REPO_ROOT) -> list[Path]:
    exec_root = root / "executive"
    if not exec_root.is_dir():
        return []
    return sorted(p for p in exec_root.rglob("*.md") if p.is_file())


def _self_test() -> int:
    failures: list[str] = []

    def classes(text: str) -> list[str]:
        return [cls for _, cls, _ in scan_page_text(text)]

    def expect(name: str, text: str, want: list[str]) -> None:
        got = classes(text)
        if got != want:
            failures.append(f"{name}: expected classes {want}, got {got}")

    # Absolutes: base words, inflections, phrase variants.
    expect("absolute-guarantee", "The control guarantees the outcome.\n", ["absolute"])
    expect("absolute-guaranteed", "Delivery is guaranteed by the gate.\n", ["absolute"])
    expect("absolute-eliminates", "This eliminates the risk.\n", ["absolute"])
    expect("absolute-eliminating", "Eliminating the class of failure entirely.\n", ["absolute"])
    expect("absolute-makes-impossible", "The gate makes a leak impossible.\n", ["absolute"])
    expect("absolute-make-it-impossible", "Controls make it impossible to bypass review.\n", ["absolute"])
    expect("absolute-removes-all-risk", "Adoption removes all risk of drift.\n", ["absolute"])
    # No quotation exemption for absolutes: a blockquote hit still fails.
    expect("absolute-blockquote-still-flagged", "> ISO 31000: adoption guarantees outcomes.\n", ["absolute"])
    # Word-reference and fenced forms are exempt; approved causal words pass.
    expect("absolute-backtick-pass", "The word `guarantee` is banned.\n", [])
    expect("absolute-fenced-pass", "```\nguarantees\n```\n", [])
    expect("causal-vocab-pass", "The register is a contribution to, and evidence for, assurance.\n", [])

    # Qualified-shall rule.
    expect("shall-bare", "The organization shall maintain a register.\n", ["shall"])
    expect("shall-sentence-initial", "Shall we proceed with the review?\n", ["shall"])
    expect("shall-quoted-source-before", 'ISO 27001 states: "The organization shall determine the scope."\n', [])
    expect("shall-quoted-source-after", '"The organization shall determine the scope." (ISO 27001, clause 4.3)\n', [])
    expect("shall-quoted-link-adjacent", '"Access shall be revoked." per [the standard](../standards/example-standard.md).\n', [])
    expect("shall-quoted-no-source", '"The organization shall determine the scope."\n', ["shall"])
    expect("shall-curly-quoted-source", "NIST SP 800-53 requires: \u201cAccess shall be reviewed.\u201d\n", [])
    expect("shall-blockquote-attributed-same-line", "> GDPR Article 32: processing shall be secured.\n", [])
    expect("shall-blockquote-attribution-adjacent", "From ISO 22301:\n\n> The organization shall establish a BCMS.\n", [])
    expect("shall-blockquote-unattributed", "> The organization shall establish a BCMS.\n\nPlain prose follows.\n", ["shall"])
    expect("shall-hyphenated-identifier-pass", "See lint-shall-near-uncertainty.py for gate 9.\n", [])
    expect("shall-substring-pass", "Marshall reviewed the plan.\n", [])
    expect("shall-backtick-pass", "The word `shall` is harmonized to `must`.\n", [])

    # Dash ban.
    expect("dash-em-flagged", "Risk\u2014the board's concern\u2014is framed here.\n", ["dash"])
    expect("dash-en-flagged", "See items 1\u20133 above.\n", ["dash"])
    expect("dash-backtick-pass", "The glyphs `\u2014` and `\u2013` are banned.\n", [])
    expect("dash-fenced-pass", "```\na \u2014 b\n```\n", [])

    # Multi-class line ordering (dash, then absolute, then shall).
    expect("multi-class", "It guarantees success \u2014 and shall be adopted.\n",
           ["dash", "absolute", "shall"])

    # F1: a multi-word absolute wrapped across a soft line break must not escape.
    expect("absolute-makes-impossible-softbreak", "The control makes\nit impossible to bypass review.\n", ["absolute"])
    # F3: a mismatched fence marker inside a fenced block must not toggle out, so
    # prose after the block is still scanned.
    expect("absolute-mixed-fence-noescape", "~~~\n```\nexample\n~~~\nThe control guarantees success.\n", ["absolute"])

    # F2: a fenced block physically BETWEEN a blockquoted 'shall' and a later
    # citation must NOT collapse into false adjacency, so the shall is UNqualified.
    expect("shall-fence-separated-unqualified",
           "> The org shall comply.\n```text\nexample fenced line\n```\n[ISO 27001](https://iso.org/iso)\n",
           ["shall"])
    # F3: an absolute inside a link DESTINATION (not visible prose) must PASS;
    # the same absolute in visible link TEXT (or plain prose) still FAILS.
    expect("absolute-in-link-url-pass", "See the [source](https://iso.org/guarantee) page.\n", [])
    expect("absolute-in-link-text-flagged", "See the [guarantee](https://iso.org/x) page.\n", ["absolute"])
    expect("absolute-in-refdef-url-pass", "[n]: https://iso.org/guarantee\n", [])
    # F3 negative-of-negative: a line that LOOKS like a ref-def but renders as
    # visible prose keeps its absolute scanned (only the dest token is blanked).
    expect("fake-refdef-prose-absolute-flagged", "[note]: The guarantee applies.\n", ["absolute"])
    # A real ref-def whose TITLE or LABEL contains an absolute is link metadata, not
    # visible prose -> must PASS (no false positive).
    expect("refdef-title-absolute-pass", '[n]: https://iso.org/x "guarantee"\n', [])
    expect("refdef-label-absolute-pass", "[guarantee]: https://iso.org/x\n", [])

    # File-level fail-loud: an unreadable / non-UTF-8 page is flagged, not skipped.
    import tempfile
    with tempfile.TemporaryDirectory() as _td:
        _bin = Path(_td) / "brief-binary.md"
        _bin.write_bytes(b"\xff\xfe not utf-8 \x00")
        if not any("not readable" in f for f in check_file(_bin, "executive/brief-binary.md")):
            failures.append("unreadable-failloud: expected a 'not readable' finding, got none")

    if failures:
        for fl in failures:
            print(f"  SELF-TEST FAIL: {fl}")
        print(f"self-test: {len(failures)} case(s) failed.")
        return 1
    print("self-test: all vocabulary cases passed (absolutes denylist incl. inflections and "
          "no-quotation-exemption; qualified-shall inline/blockquote adjacency forms; dash ban "
          "with code-span/fence exemptions).")
    return 0


def main(argv: list[str]) -> int:
    args = positional_args(argv[1:])
    if self_test_requested(argv[1:], args):
        return _self_test()
    # 3b50: a missing path used to raise a FileNotFoundError traceback (rc 1, the findings code);
    # refuse it with exit 2. Content-only: the vocabulary check is sound on any narrative file.
    files = ([Path(a) for a in guard_explicit_paths_cwd(args, allow_outside=True)]
             if args else discover())
    all_findings: list[str] = []
    for f in files:
        try:
            rel = f.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            rel = f.as_posix()
        all_findings.extend(check_file(f, rel))
    if all_findings:
        for finding in all_findings:
            print(f"  {finding}")
        print(f"FAIL: {len(all_findings)} narrative-vocabulary finding(s) across "
              f"{len(files)} file(s).")
        return 1
    print(f"OK: {len(files)} narrative file(s) checked; no absolutes, no unqualified "
          f"'shall', no em/en dashes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
