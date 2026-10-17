#!/usr/bin/env python3
"""Answer "is X held in grc_library_ref?" from the AUTHORITATIVE index, not a partial grep.

Forcing-function orchestrator aid (advisory, NOT an audit gate). A held / not-held claim
about the reference base MUST quote this tool's output, never a bare filename grep. The
2026-07-17 lesson that motivated it: a partial ``grep -rlE '27002' ... | head -1`` grabbed
a vendor publication and wrongly concluded "ISO/IEC 27002:2022 is not held", when the ref
index lists the standard plainly. This is the `evidence-grounded-completion`
"inventory/absence claims require the index, not a partial look" corollary, mechanized the
same executed-not-narrated way: run it, quote it, never narrate from memory.

WHAT IT DOES. It searches the reference base's OWN index files (``INDEX.md`` and
``catalogue.yml``; ``SECTION-INDEX.md`` / ``COVERAGE-MAP.md`` if present) for the query as a
case-insensitive substring over titles, ids, and paths, and reports every match (with the
held path and, where the catalogue records it, the version / checked-edition) as HELD, or
reports NOT-FOUND-IN-INDEX. A not-found result means "absent from the index", and the index
is the authority for what is held; it does not license a from-memory assertion, and if the
index itself may be stale that is a separate check (the reference-version-currency SOP).

EXTRACT COMPLETENESS (3b365). An index match proves only that an extract is listed, not that its
text is quotable: on 2026-10-17 a bare HELD for Ecuador's data protection law was read as quotable
although its extract's header says the body is image scans. So the tool opens every extract a
match names and reads its header. A match names an extract when its line holds a root-relative
``...--full-text.md`` path in backticks or double quotes (closed as opened), or when it is a line
of a catalogue.yml record whose one ``path:`` or ``extract:`` field holds one (so a match on a
record's title, notes or checked_edition line checks that record's extract). A record runs from
its ``  - `` line through its indented ``    key:`` field lines; blank and comment lines inside
it are skipped, and any other line ends it. A record with no such field, or with more than one
(even if one of them is an extract path), names no extract through the record; but a matched
line that itself holds an extract path in backticks or double quotes (such as that record's own
quoted ``path:`` line) names that path directly. The header is the title and metadata at the top
of the extract (every leading byte-order mark is ignored). The title is the first non-blank
line when, after leading whitespace, it starts ``# ``; a later heading starting with one or
more ``#`` and a space is body, except a ``## Screening note`` section before a ``---``. A
metadata bullet starts ``- `` at column 0; an indented ``- `` line is body. A ``---`` line within
the first 40 lines ends the header at the first one, but only while every line before it is
header material: the title, blank lines, metadata bullets, and a screening section (a line
starting ``## Screening note`` and every line after it up to the ``---``), so a publication's
Screening note is header. The first line before the ``---`` of any other kind (body prose, a
heading other than the title, an indented bullet, a ``----- PAGE`` line) ends the header instead:
the header stops before that line and any blank lines just above it, and the ``---`` is then a
horizontal rule in the body. With no ``---`` in the first 40 lines, the header ends at the first
of these lines: a ``----- PAGE`` line, a blank line after a metadata bullet, a non-title line that
starts with one or more ``#`` and a space after leading whitespace, or an indented ``- `` line
(before or after the first metadata bullet). Other non-blank prose also ends the header,
before or after the first metadata bullet,
as it does with ``---``. At most the first 40 lines, within the first 256 KiB, are header. A
header line carrying "INCOMPLETE BODY", "NO BODY TEXT", "PARTIAL:" or "Not recovered" (the marker
forms the reference base's extracts use) marks the body incomplete, and so does a body with no
non-blank line after the header (``---`` and ``----- PAGE`` lines are not body text). Incomplete
means the part the note describes is not quotable from the extract; the rest may be. When every
named extract is incomplete the result is HELD-INCOMPLETE, naming each extract and quoting its
note; when some are complete, the result stays HELD and the incomplete ones follow as a WARNING.
A named extract that is missing, unreadable (a permission error), not a regular file, a symlink
loop, or resolves (following symlinks) outside the reference base gives CANNOT-EVALUATE (exit 2,
fail closed, never HELD). So does an extract larger than 256 KiB whose first 256 KiB hold no
header end, or no body text after the header: the rest of the file was not read. An extract of
at most 256 KiB whose header runs to its end, or whose body has no text, is read in full and is
incomplete (its body has no text), not CANNOT-EVALUATE. A match that names no extract (for
example a catalogue line in a record without an extract path, or a line outside any well-formed
record) is reported as before and does not change the result.

Residuals (not detected): the markers are exact and case-sensitive substrings, so a gap described
in other words (or in another case) is not detected; text before the first ``---`` is header only
under the rule above, so a note after a line of another kind (other than in a screening section)
is body and not read; in an extract with no ``---`` in its first 40 lines, a second bullet block
after a blank line is not header; a wrapped bullet's continuation line ends the header, with or
without a ``---``, so a marker on it or after it is missed (none occur in the reference base);
an indented metadata sub-bullet is read as body (none occur in the reference base), so its marker
is missed; a catalogue record whose single ``path:`` or ``extract:`` field does not hold a quoted
``--full-text.md`` path (a ``.json`` path, ``null``, or an unquoted path) names no extract; record
field lines that follow a line of another shape (a continuation line or an unindented key) are not
attributed to the record; a screened publication extract may omit material by design, which its
Screening note describes in words the markers need not match.

Usage:
  python3 tools/ref-holds.py "27002"
  python3 tools/ref-holds.py "ISO/IEC 27002:2022"
  python3 tools/ref-holds.py "MITRE ATT&CK"
  python3 tools/ref-holds.py --ref-root /path/to/grc_library_ref "CSF 2.0"
  python3 tools/ref-holds.py --self-test

Exit codes:
  0  at least one index match (HELD), with at least one named extract complete or no extract
     named; OR, on an adopter clone with the reference sibling absent, a clean advisory no-op
     (nothing to report), per the #1792 degrade
  1  no index match (NOT-FOUND-IN-INDEX)
  2  the ref index could not be read (locate grc_library_ref, or pass --ref-root); OR a matched
     extract could not be read (CANNOT-EVALUATE)
  3  index matches, but every named extract marks its body incomplete (HELD-INCOMPLETE)
Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import os
import re
import stat
import sys
from pathlib import Path

from lint_common import REPO_ROOT, InaccessiblePath, require_dir, resolve_sibling, strict_kind

# Default: grc_library_ref is a sibling of the repo containing this tool.
DEFAULT_REF_ROOT = REPO_ROOT.parent / "grc_library_ref"

INDEX_FILES = ("INDEX.md", "catalogue.yml", "SECTION-INDEX.md", "COVERAGE-MAP.md")

# 3b365: an extract path as the index files write it, root-relative in backticks or double quotes
# (r6: closed by the same delimiter that opens it).
EXTRACT_PATH = re.compile(r'([`"])([^`"\s]+--full-text\.md)\1')
# catalogue.yml's record shape: "  - title: ..." opens a record and each "    key: value" line is one
# of its fields; a record's extract is its path field or, in publication records, its extract field.
CATALOGUE_RECORD = re.compile(r"  - \w+: ")
CATALOGUE_FIELD = re.compile(r"    \w+: ")
CATALOGUE_PATH_FIELD = re.compile(r"(?:  - |    )(?:path|extract):")
CATALOGUE_PATH = re.compile(r'(?:  - |    )(?:path|extract): "([^"\s]+--full-text\.md)"\s*$')
# The header markers the reference base's extracts use for a body the extraction did not capture.
INCOMPLETE_MARKERS = ("INCOMPLETE BODY", "NO BODY TEXT", "PARTIAL:", "Not recovered")
HEADER_LINES = 40
READ_BYTES = 256 * 1024
PAGE_MARK = "----- PAGE"
# A publication extract's screening section: this heading, then its paragraphs, then the "---".
SCREENING_NOTE = "## Screening note"


def find_ref_root(explicit: str | None) -> Path | None:
    if explicit:
        # require_dir checks the path as given before resolving it (3b74: "missing/../ref" used to
        # normalize into a real root) and refuses, exit 2, a missing, non-directory or unresolvable one.
        p = require_dir(Path(explicit).expanduser(), "--ref-root")
        try:
            present = any(strict_kind(p / n) is not None for n in ("INDEX.md", "catalogue.yml"))
        except OSError:
            # An index that cannot even be examined is present-but-unreadable: let the read refuse it.
            return p
        return p if present else None
    # Default: the real grc_library_ref sibling, located via the shared resolver
    # (1.19.2 (closing PR #996)). None on a portable clone that has no sibling. The lookup is strict
    # (3b74): an ABSENT sibling or index still gives None, but one that cannot be examined raises
    # InaccessiblePath for main() to refuse, where pathlib raised on Python 3.11 and read it as
    # absent on 3.12+.
    sibling = resolve_sibling("ref", strict=True)
    if sibling is not None and any(strict_kind(sibling / n) is not None
                                   for n in ("INDEX.md", "catalogue.yml")):
        return sibling
    return None


class IndexUnreadable(RuntimeError):
    """A grc_library_ref index file exists but cannot be read."""


def catalogue_record_extracts(lines: list[str]) -> dict[int, str]:
    """Map the line number of each line of a catalogue.yml record to the record's extract path.

    Only a record with exactly one path or extract field, holding an extract path, is mapped. A
    blank or comment line inside a record is skipped (it is not mapped and does not close the
    record); a line of any other shape (a section key, a continuation line) closes the current
    record, so a line is never attributed to a record it may not belong to."""
    owner: dict[int, str] = {}
    record: list[int] = []
    paths: list[str | None] = []

    def close() -> None:
        if len(paths) == 1 and paths[0] is not None:
            owner.update(dict.fromkeys(record, paths[0]))

    for i, line in enumerate(lines, 1):
        if CATALOGUE_RECORD.match(line):
            close()
            record, paths = [i], []
        elif record and CATALOGUE_FIELD.match(line):
            record.append(i)
        elif record and (not line.strip() or line.lstrip().startswith("#")):
            continue
        else:
            close()
            record, paths = [], []
            continue
        if CATALOGUE_PATH_FIELD.match(line):
            m = CATALOGUE_PATH.match(line)
            paths.append(m.group(1) if m else None)
    close()
    return owner


def search_index(ref_root: Path, query: str) -> list[tuple[str, int, str, tuple[str, ...]]]:
    """Return (index_file, line_no, line, extracts) for every line matching the query
    (case-insensitive), where extracts are the extract paths the line itself names plus, on a
    catalogue.yml record's line, the record's extract path. A record's field line holding a quoted
    extract path therefore names it even when the record as a whole names none."""
    q = query.lower()
    hits: list[tuple[str, int, str, tuple[str, ...]]] = []
    for name in INDEX_FILES:
        f = ref_root / name
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            if os.path.lexists(f):
                # 3b74: a dangling link is a present index that cannot be read, not an absent one;
                # skipping it let a verdict rest on fewer index files than exist.
                raise IndexUnreadable(f"{name}: a dangling link") from None
            continue  # an absent index file is simply not consulted
        except OSError as exc:
            # A present but unreadable index is not evidence of absence (3b50b2e1).
            raise IndexUnreadable(f"{name}: {exc.strerror}") from exc
        lines = text.splitlines()
        owner = catalogue_record_extracts(lines) if name == "catalogue.yml" else {}
        for i, line in enumerate(lines, 1):
            if q in line.lower():
                named = [m[1] for m in EXTRACT_PATH.findall(line)] + ([owner[i]] if i in owner else [])
                hits.append((name, i, line.strip(), tuple(dict.fromkeys(named))))
    return hits


class ExtractUnreadable(RuntimeError):
    """An extract named by an index match cannot be located inside the reference base or read."""


def read_extract(ref_root: Path, rel: str) -> tuple[bytes, bool]:
    """Return the first READ_BYTES bytes of the extract and whether the file holds more.

    The path is resolved strictly (every symlink followed) and must lie inside the resolved
    reference base and be a regular file, so a symlink that leaves the base, a FIFO or a device is
    refused rather than opened."""
    try:
        base = ref_root.resolve(strict=True)
        target = (ref_root / rel).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        # Python 3.11's resolve() raises RuntimeError on a symlink loop.
        raise ExtractUnreadable(getattr(exc, "strerror", None) or str(exc) or type(exc).__name__) from exc
    if not target.is_relative_to(base):
        raise ExtractUnreadable("the path resolves outside the reference base")
    try:
        if not stat.S_ISREG(target.stat().st_mode):
            raise ExtractUnreadable("not a regular file")
        # O_NONBLOCK and O_NOFOLLOW keep a swap to a FIFO or symlink after the checks from hanging the
        # open or leaving the base; fstat then confirms the opened file is the regular file checked.
        fd = os.open(target, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0))
        with open(fd, "rb") as fh:
            if not stat.S_ISREG(os.fstat(fh.fileno()).st_mode):
                raise ExtractUnreadable("not a regular file")
            data = fh.read(READ_BYTES + 1)
    except OSError as exc:
        raise ExtractUnreadable(exc.strerror or type(exc).__name__) from exc
    return data[:READ_BYTES], len(data) > READ_BYTES


def split_header(lines: list[str]) -> tuple[list[str], list[str]]:
    """Split an extract's lines into its header and the rest (see the module docstring)."""
    # A heading is header only as the title, except a ## Screening note section before a ---;
    # metadata bullets start at column 0.
    title = next((n for n, line in enumerate(lines[:HEADER_LINES]) if line.strip()), None)
    sep = next((n for n, line in enumerate(lines[:HEADER_LINES]) if line.strip() == "---"), None)
    if sep is not None:
        screening = False
        for n, line in enumerate(lines[:sep]):
            s = line.strip()
            if screening or not s or line.startswith("- ") or (n == title and s.startswith("# ")):
                continue
            if s.startswith(SCREENING_NOTE):
                screening = True
                continue
            # 3b365 r4: other prose before the separator is body (SAMM's line 7), so the header ends
            # at the blank before it and the "---" is only a horizontal rule.
            while n and not lines[n - 1].strip():
                n -= 1
            return lines[:n], lines[n:]
        # The separator ends the header, so notes between the bullets and it (a Screening note) stay in.
        return lines[:sep], lines[sep:]
    bullets = False
    for n, line in enumerate(lines):
        s = line.strip()
        if n >= HEADER_LINES or s.startswith(PAGE_MARK):
            return lines[:n], lines[n:]
        if not s:
            if bullets:
                return lines[:n], lines[n:]
        elif line.startswith("- "):
            bullets = True
        elif n == title and s.startswith("# "):
            continue
        else:
            # Body prose, a later heading of any depth, and indented bullets end the header
            # before or after metadata bullets, just as they do with a separator.
            return lines[:n], lines[n:]
    return lines, []


def incomplete_body_notes(ref_root: Path, rel: str) -> list[str]:
    """Return the extract's header lines that carry an incomplete-body marker, or a note that its
    body is empty (an empty list when the extract is complete).

    Only the header is searched, so a marker quoted in the body is not read as a note about the
    extraction."""
    data, more = read_extract(ref_root, rel)
    # Every leading U+FEFF is encoding residue, not part of the title line.
    lines = data.decode("utf-8", errors="replace").lstrip("\ufeff").splitlines()
    if more and lines:
        lines.pop()  # the last line may be cut at the read bound
    header, rest = split_header(lines)
    if more and not rest:
        raise ExtractUnreadable(f"no header end within its first {READ_BYTES} bytes")
    notes = [s for s in (line.strip() for line in header) if any(m in s for m in INCOMPLETE_MARKERS)]
    body = any(s and s != "---" and not s.startswith(PAGE_MARK) for s in (line.strip() for line in rest))
    if not body and more:
        raise ExtractUnreadable(f"no body text within its first {READ_BYTES} bytes")
    if not body:
        notes.append("(the body after the header has no text)")
    return notes


def run(ref_root: Path, query: str, stream=sys.stdout) -> int:
    try:
        hits = search_index(ref_root, query)
    except IndexUnreadable as exc:
        print(f"ERROR: grc_library_ref index unreadable ({exc}); refusing a verdict.",
              file=sys.stderr)
        return 2
    if not hits:
        print(
            f"NOT-FOUND-IN-INDEX: no entry matching {query!r} in the grc_library_ref index "
            f"({', '.join(n for n in INDEX_FILES if (ref_root / n).exists())}). "
            f"The index is the authority for what is held: 'not found' means not-in-the-index, "
            f"NOT a from-memory not-held claim. If the standard/framework is load-bearing, follow "
            f"the missing-reference SOP (attempt acquire / pause), and confirm the index itself is "
            f"current before relying on the negative.",
            file=stream,
        )
        return 1
    # 3b365: open every extract the matches name and read its header notes, so a listed extract whose
    # body is incomplete is not reported as quotable. An extract that cannot be read refuses a verdict.
    incomplete: dict[str, list[str]] = {}
    complete = 0
    for rel in dict.fromkeys(p for *_, named in hits for p in named):
        try:
            notes = incomplete_body_notes(ref_root, rel)
        except ExtractUnreadable as exc:
            print(f"CANNOT-EVALUATE: matched extract {rel} could not be read ({exc}); refusing a "
                  f"verdict (an unreadable extract is not evidence that its text is held).",
                  file=sys.stderr)
            return 2
        if notes:
            incomplete[rel] = notes
        else:
            complete += 1
    if incomplete and not complete:
        print(f"HELD-INCOMPLETE: {len(hits)} index match(es) for {query!r} in grc_library_ref, but "
              f"every matched extract's header marks its body incomplete; the part each note "
              f"describes is not quotable from the extract (read the original for it):", file=stream)
    else:
        print(f"HELD: {len(hits)} index match(es) for {query!r} in grc_library_ref:", file=stream)
    # De-dupe identical lines across index files while preserving provenance of the first hit.
    seen: set[str] = set()
    for name, lineno, line, _ in hits:
        key = line
        if key in seen:
            continue
        seen.add(key)
        print(f"  [{name}:{lineno}] {line[:240]}", file=stream)
    if incomplete and complete:
        print("WARNING: these matched extracts mark their body incomplete; the part each note describes "
              "is not quotable from the extract:", file=stream)
    for rel, notes in incomplete.items():
        print(f"  incomplete extract: {rel}", file=stream)
        for note in notes:
            print(f"    note: {note}", file=stream)
    return 3 if incomplete and not complete else 0


def _self_test() -> int:
    # Every scratch path the self-test makes (including a child git's) lands under one root that is
    # removed on exit, so a run leaves nothing behind in the temp directory (3b103).
    import atexit as _atx, os as _os, shutil as _shu, tempfile as _tpf
    _tpf.tempdir = _tpf.mkdtemp(prefix="grc-selftest-"); _os.environ["TMPDIR"] = _tpf.tempdir
    _atx.register(_shu.rmtree, _tpf.tempdir, True)
    import io
    import tempfile
    import unittest

    class T(unittest.TestCase):
        def _tmp(self) -> Path:
            # Under the self-test root (removed on exit), and each one also removed after its test.
            d = Path(tempfile.mkdtemp())
            self.addCleanup(_shu.rmtree, d, True)
            return d

        def _mk(self, index_body: str) -> Path:
            d = self._tmp()
            (d / "INDEX.md").write_text(index_body, encoding="utf-8")
            return d

        def test_held_match(self):
            d = self._mk(
                "- _[standards]_ ISO/IEC 27002:2022, Information security controls "
                "(`standards/ISO/ISO-IEC-27002-2022--full-text.md`)\n"
            )
            # 3b365: a named extract is now opened, so the fixture holds it (a missing one fails closed).
            self._extract(d, "standards/ISO/ISO-IEC-27002-2022--full-text.md", self.COMPLETE)
            buf = io.StringIO()
            rc = run(d, "27002", stream=buf)
            self.assertEqual(rc, 0)
            self.assertIn("HELD", buf.getvalue())
            self.assertIn("27002", buf.getvalue())

        def test_not_found(self):
            d = self._mk("- _[standards]_ ISO/IEC 27001:2022 (`standards/ISO/x.md`)\n")
            buf = io.StringIO()
            rc = run(d, "NONESUCH-99999", stream=buf)
            self.assertEqual(rc, 1)
            self.assertIn("NOT-FOUND-IN-INDEX", buf.getvalue())

        def test_case_insensitive(self):
            d = self._mk("- MITRE ATT&CK Enterprise (`frameworks/MITRE/x.md`)\n")
            self.assertEqual(run(d, "mitre att&ck", stream=io.StringIO()), 0)

        # 3b365: an index match proves only that an extract is listed, not that its body is quotable.
        COMPLETE = "- Extraction note: text auto-extracted on 2026-09-27 from the source (PyMuPDF).\n"
        INCOMPLETE = ("- Extraction note: text auto-extracted. INCOMPLETE BODY: pages 2 to 69 are image "
                      "scans. Not recovered: OCR failed the quality check.\n")
        # One fixture per marker, each carrying only that marker, so dropping any one is detected.
        MARKER_NOTES = {
            "INCOMPLETE BODY": "- Extraction note: INCOMPLETE BODY: pages 2 to 69 are image scans.\n",
            "NO BODY TEXT": "- Extraction: 11 pages. NO BODY TEXT: every page is an image scan.\n",
            "PARTIAL:": "- Extraction: 18 pages. PARTIAL: text inside images is not captured.\n",
            "Not recovered": "- Extraction: 9 pages. Not recovered: OCR failed the quality check.\n",
        }

        def _extract(self, d: Path, rel: str, header: str, body: str = "Body text.\n") -> None:
            self._write(d, rel, f"# Title (full-text extract)\n\n- Source file: `originals/x.pdf`\n"
                                f"{header}\n---\n\n{body}")

        def _write(self, d: Path, rel: str, text: str) -> None:
            p = d / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")

        def _link(self, target: Path, link: Path, is_dir: bool = False) -> None:
            if not hasattr(os, "symlink"):
                self.skipTest("os.symlink is unavailable")
            link.parent.mkdir(parents=True, exist_ok=True)
            try:
                os.symlink(target, link, target_is_directory=is_dir)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"cannot create a symlink here ({exc})")

        def _outside(self, rel: str) -> Path:
            """A readable, complete extract outside the reference base, so only containment refuses it."""
            o = self._tmp()
            self._extract(o, rel, self.COMPLETE)
            self.assertEqual(incomplete_body_notes(o, rel), [])  # readable and complete as such
            return o

        def _run(self, d: Path, query: str) -> tuple[int, str, str]:
            import contextlib
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stderr(err):
                rc = run(d, query, stream=out)
            return rc, out.getvalue(), err.getvalue()

        def test_complete_extract_held(self):
            d = self._mk("- _[legislation]_ Law A (`legislation/A/A--full-text.md`)\n")
            self._extract(d, "legislation/A/A--full-text.md", self.COMPLETE)
            rc, out, err = self._run(d, "Law A")
            self.assertEqual(rc, 0, out + err)
            self.assertTrue(out.startswith("HELD: "), out)
            self.assertNotIn("INCOMPLETE", out)
            self.assertNotIn("WARNING", out)

        def test_marker_in_body_not_header_held(self):
            d = self._mk("- _[legislation]_ Law A (`legislation/A/A--full-text.md`)\n")
            self._extract(d, "legislation/A/A--full-text.md", self.COMPLETE,
                          body="The archive says INCOMPLETE BODY and Not recovered in its text.\n")
            rc, out, err = self._run(d, "Law A")
            self.assertEqual(rc, 0, out + err)
            self.assertNotIn("WARNING", out)

        def test_incomplete_body_extract_held_incomplete(self):
            d = self._mk("- _[legislation]_ Law E (`legislation/E/E--full-text.md`)\n")
            self._extract(d, "legislation/E/E--full-text.md", self.INCOMPLETE)
            rc, out, err = self._run(d, "Law E")
            self.assertEqual(rc, 3, out + err)
            self.assertTrue(out.startswith("HELD-INCOMPLETE: "), out)
            # 3b365 r3: only the part the note describes is not quotable, not the whole text.
            self.assertIn("the part each note describes is not quotable from the extract", out)
            self.assertNotIn("its text is not quotable", out)
            self.assertIn("legislation/E/E--full-text.md", out)
            self.assertIn(self.INCOMPLETE.strip(), out)

        def _assert_marker_alone_held_incomplete(self, marker: str) -> None:
            note = self.MARKER_NOTES[marker]
            self.assertEqual([m for m in self.MARKER_NOTES if m in note], [marker])
            d = self._mk("- _[publications]_ Deck P (`publications/P--full-text.md`)\n")
            self._extract(d, "publications/P--full-text.md", note)
            rc, out, err = self._run(d, "Deck P")
            self.assertEqual(rc, 3, out + err)
            self.assertIn(note.strip(), out)

        def test_incomplete_body_marker_alone_held_incomplete(self):
            self._assert_marker_alone_held_incomplete("INCOMPLETE BODY")

        def test_no_body_text_marker_alone_held_incomplete(self):
            self._assert_marker_alone_held_incomplete("NO BODY TEXT")

        def test_partial_marker_alone_held_incomplete(self):
            self._assert_marker_alone_held_incomplete("PARTIAL:")

        def test_not_recovered_marker_alone_held_incomplete(self):
            self._assert_marker_alone_held_incomplete("Not recovered")

        def test_empty_body_held_incomplete(self):
            d = self._mk("- Law Z one (`legislation/Z/Z1--full-text.md`)\n"
                         "- Law Z two (`legislation/Z/Z2--full-text.md`)\n")
            self._extract(d, "legislation/Z/Z1--full-text.md", self.COMPLETE, body="\n\n")
            # Page markers are not body text either.
            self._write(d, "legislation/Z/Z2--full-text.md", f"# Title\n\n{self.COMPLETE}\n\n"
                                                             "----- PAGE 1 -----\n\n----- PAGE 2 -----\n")
            rc, out, err = self._run(d, "Law Z")
            self.assertEqual(rc, 3, out + err)
            self.assertIn("legislation/Z/Z1--full-text.md", out)
            self.assertIn("legislation/Z/Z2--full-text.md", out)
            self.assertIn("has no text", out)

        # 3b365 r2: 19 real extracts have no "---"; their header ends at a blank line or "----- PAGE".
        def test_no_separator_marker_in_body_held(self):
            d = self._mk("- Standard N (`standards/N/N--full-text.md`)\n")
            self._write(d, "standards/N/N--full-text.md",
                        f"# Title\n\n- Source file: `originals/n.pdf`\n{self.COMPLETE}\n\n"
                        "----- PAGE 1 -----\n\nThe archive copy: Not recovered, INCOMPLETE BODY.\n")
            rc, out, err = self._run(d, "Standard N")
            self.assertEqual(rc, 0, out + err)
            self.assertNotIn("incomplete", out.lower())

        def test_no_separator_page_mark_ends_header(self):
            d = self._mk("- Standard Q (`standards/Q/Q--full-text.md`)\n")
            self._write(d, "standards/Q/Q--full-text.md",
                        f"# Title\n\n{self.COMPLETE}----- PAGE 1 -----\nPage text. Not recovered here.\n")
            rc, out, err = self._run(d, "Standard Q")
            self.assertEqual(rc, 0, out + err)

        def test_no_separator_header_marker_held_incomplete(self):
            d = self._mk("- Standard I (`standards/I/I--full-text.md`)\n")
            note = self.MARKER_NOTES["Not recovered"]
            self._write(d, "standards/I/I--full-text.md",
                        f"# Title\n\n- Source file: `originals/i.pdf`\n{note}\n----- PAGE 1 -----\n\nCover.\n")
            rc, out, err = self._run(d, "Standard I")
            self.assertEqual(rc, 3, out + err)
            self.assertIn(note.strip(), out)

        def test_header_line_cap_applies(self):
            # Lines 1 and 2 are the title and a blank, so the marker lands on line 40 or line 41.
            d = self._mk("- Cap in (`standards/C/in--full-text.md`)\n"
                         "- Cap out (`standards/C/out--full-text.md`)\n")
            note = self.MARKER_NOTES["Not recovered"]
            for rel, filler in (("standards/C/in--full-text.md", 37), ("standards/C/out--full-text.md", 38)):
                bullets = "".join(f"- Metadata {k}.\n" for k in range(filler))
                self._write(d, rel, f"# Title\n\n{bullets}{note}\n---\n\nBody text.\n")
            rc, out, err = self._run(d, "Cap in")
            self.assertEqual(rc, 3, out + err)
            rc, out, err = self._run(d, "Cap out")
            self.assertEqual(rc, 0, out + err)
            self.assertNotIn("incomplete", out.lower())

        def test_screening_note_late_in_header_bound_held_incomplete(self):
            # 3b365 r4: the note and "---" sit at lines 38 and 39, after a blank that the no-separator
            # rule would end the header at, so only the "---" rule over all 40 lines keeps the note.
            d = self._mk("- Late note (`publications/L--full-text.md`)\n")
            bullets = "".join(f"- Metadata {k}.\n" for k in range(32))
            text = (f"# Title\n\n{bullets}\n## Screening note\n\n"
                    "KEPT (partial). PARTIAL: the appendix tables are not captured.\n---\n\nBody text.\n")
            lines = text.splitlines()
            self.assertEqual((lines[37][:16], lines[38]), ("KEPT (partial). ", "---"))
            self._write(d, "publications/L--full-text.md", text)
            rc, out, err = self._run(d, "Late note")
            self.assertEqual(rc, 3, out + err)
            self.assertIn("PARTIAL: the appendix tables are not captured.", out)

        def test_body_prose_before_horizontal_rule_held(self):
            # 3b365 r4: SAMM has body prose at line 7 and its first "---" at line 9; the prose ends the
            # header, so a marker in it (or after it) is body, not a note about the extraction.
            d = self._mk("- Model S (`frameworks/S/S--full-text.md`)\n")
            self._write(d, "frameworks/S/S--full-text.md",
                        f"# Title\n\n- Source file: `originals/s.pdf`\n{self.COMPLETE}\n"
                        "The model's archive was Not recovered in 2019; it is organized as five functions.\n\n"
                        f"{self.MARKER_NOTES['PARTIAL:']}\n---\n\n## Levels\n\nBody text.\n")
            rc, out, err = self._run(d, "Model S")
            self.assertEqual(rc, 0, out + err)
            self.assertNotIn("incomplete", out.lower())
            # The header still ends at the blank before the prose, so a bullet note above it counts.
            self._write(d, "frameworks/S/S--full-text.md",
                        f"# Title\n\n{self.MARKER_NOTES['Not recovered']}\nThe model is organized as five "
                        "functions.\n\n---\n\nBody text.\n")
            rc, out, err = self._run(d, "Model S")
            self.assertEqual(rc, 3, out + err)
            self.assertIn(self.MARKER_NOTES["Not recovered"].strip(), out)

        def test_later_title_line_ends_header_held(self):
            # 3b365 r5: only the first non-blank line is the "# " title; a later "# " line is a body
            # heading, so a marker bullet after it is body, with or without a "---".
            d = self._mk("- Code H (`legislation/H/H--full-text.md`)\n")
            for text in ("# T\n- Source file\n# Part One\n- Not recovered: annex B\n---\n\nBody text.\n",
                         "# T\n# Part One\n- Not recovered: annex B\n\n----- PAGE 1 -----\n\nBody text.\n"):
                self._write(d, "legislation/H/H--full-text.md", text)
                rc, out, err = self._run(d, "Code H")
                self.assertEqual(rc, 0, text + out + err)
                self.assertNotIn("incomplete", out.lower())
            # The title itself is still header, so a marker bullet under it counts.
            self._write(d, "legislation/H/H--full-text.md",
                        "\n# T\n- Source file\n- Not recovered: annex B\n---\n\n# Part One\n\nBody text.\n")
            rc, out, err = self._run(d, "Code H")
            self.assertEqual(rc, 3, out + err)
            self.assertIn("- Not recovered: annex B", out)

        def test_indented_bullet_not_header_held(self):
            # 3b365 r5: metadata bullets start at column 0 (as in every real extract); an indented
            # "- " line is a body list item, so a marker in it is body.
            d = self._mk("- Code J (`legislation/J/J--full-text.md`)\n")
            for text in ("# T\n- Source file\n  - Not recovered: annex B\n---\n\nBody text.\n",
                         "# T\n\n  - Not recovered: annex B\n\n----- PAGE 1 -----\n\nBody text.\n"):
                self._write(d, "legislation/J/J--full-text.md", text)
                rc, out, err = self._run(d, "Code J")
                self.assertEqual(rc, 0, text + out + err)
                self.assertNotIn("incomplete", out.lower())

        def test_no_separator_heading_or_indented_bullet_after_bullets_held(self):
            # Without "---", any later heading, body prose, or indented "- " line ends the
            # header even after a column-0 bullet, so a marker bullet after it is body.
            d = self._mk("- Code N (`legislation/N/N--full-text.md`)\n")
            for text in ("# T\n- Source file\n# Part One\n- Not recovered: annex B\n\nBody text.\n",
                         "# T\n- Source file\n## Part One\n- Not recovered: annex B\n\nBody text.\n",
                         "# T\n- Source file\n  ### Part One\n- Not recovered: annex B\n\nBody text.\n",
                         "# T\n- Source file\nPart One is here.\n- Not recovered: annex B\n\nBody text.\n",
                         "# T\n- Source file\n  - Not recovered: annex B\n\nBody text.\n",
                         "# T\n- Source file\n# Part One\n- Not recovered: annex B\n\n----- PAGE 1 -----\n\n"
                         "Body text.\n",
                         "# T\n- Source file\n  - Not recovered: annex B\n\n----- PAGE 1 -----\n\nBody text.\n"):
                self._write(d, "legislation/N/N--full-text.md", text)
                rc, out, err = self._run(d, "Code N")
                self.assertEqual(rc, 0, text + out + err)
                self.assertNotIn("incomplete", out.lower())

        def test_wrapped_bullet_continuation_ends_header_held(self):
            # A continuation line ends the header even when it or a later bullet has a marker.
            d = self._mk("- Code W (`legislation/W/W--full-text.md`)\n")
            for continuation in ("  INCOMPLETE BODY: OCR failed.\n", "INCOMPLETE BODY: OCR failed.\n",
                                 "  pages 2 to 9 are scans.\n- Not recovered: OCR failed.\n"):
                for separator in ("", "---\n"):
                    content = ("# T\n- Extraction note: pages 2 to 9 are scans.\n"
                               f"{continuation}{separator}Body text.\n")
                    self._write(d, "legislation/W/W--full-text.md", content)
                    rc, out, err = self._run(d, "Code W")
                    self.assertEqual(rc, 0, content + out + err)
                    self.assertNotIn("incomplete", out.lower())

        def test_byte_order_mark_before_title_held_incomplete(self):
            # Every leading U+FEFF is stripped, so the title and the bullet under it are header.
            d = self._mk("- Code B (`legislation/B/B--full-text.md`)\n")
            for prefix in ("\ufeff", "\ufeff\ufeff"):
                self._write(d, "legislation/B/B--full-text.md",
                            prefix + "# T\n- Not recovered: x\n---\n\nBody text.\n")
                rc, out, err = self._run(d, "Code B")
                self.assertEqual(rc, 3, out + err)
                self.assertIn("note: - Not recovered: x", out)

        def test_indented_title_held_incomplete(self):
            d = self._mk("- Code I (`legislation/I/I--full-text.md`)\n")
            for separator in ("---\n\n", "\n"):
                self._write(d, "legislation/I/I--full-text.md",
                            f"  # T\n- Not recovered: x\n{separator}Body text.\n")
                rc, out, err = self._run(d, "Code I")
                self.assertEqual(rc, 3, out + err)
                self.assertIn("note: - Not recovered: x", out)

        def test_mixed_path_delimiters_name_no_extract(self):
            # 3b365 r6: a path opened by a backtick and closed by a double quote (or the reverse) is
            # not an extract path, so the match names no extract (here a missing one) and stays HELD.
            for line in ('- Law P (`legislation/P/P--full-text.md")\n',
                         '- Law P ("legislation/P/P--full-text.md`)\n'):
                d = self._mk(line)
                rc, out, err = self._run(d, "Law P")
                self.assertEqual(rc, 0, line + out + err)
                self.assertNotIn("CANNOT-EVALUATE", err)
            # Matching delimiters still name it.
            d = self._mk('- Law P ("legislation/P/P--full-text.md")\n')
            self._extract(d, "legislation/P/P--full-text.md", self.MARKER_NOTES["PARTIAL:"])
            rc, out, err = self._run(d, "Law P")
            self.assertEqual(rc, 3, out + err)

        def test_header_beyond_read_bound_cannot_evaluate(self):
            d = self._mk("- Law B (`legislation/B/B--full-text.md`)\n")
            self._write(d, "legislation/B/B--full-text.md",
                        f"# Title\n\n- Extraction note: {'x' * READ_BYTES}\n\n---\n\nBody text.\n")
            rc, out, err = self._run(d, "Law B")
            self.assertEqual(rc, 2, out + err)
            self.assertIn("CANNOT-EVALUATE", err)

        def test_no_body_text_within_read_bound_cannot_evaluate(self):
            # 3b365 r4: an empty body is HELD-INCOMPLETE only when the whole file was read; here text
            # follows past the read bound, so the extract cannot be evaluated.
            d = self._mk("- Law T (`legislation/T/T--full-text.md`)\n")
            self._extract(d, "legislation/T/T--full-text.md", self.COMPLETE,
                          body="\n" * (READ_BYTES + 16) + "Body text.\n")
            rc, out, err = self._run(d, "Law T")
            self.assertEqual(rc, 2, out + err)
            self.assertIn("no body text within its first", err)
            self._extract(d, "legislation/T/T--full-text.md", self.COMPLETE, body="\n" * 16)
            rc, out, err = self._run(d, "Law T")
            self.assertEqual(rc, 3, out + err)
            self.assertIn("has no text", out)

        # 3b365 r2: a catalogue line is checked against its record's extract.
        CATALOGUE = ("standards:\n"
                     '  - title: "Law K, Spanish original"\n'
                     '    path: "legislation/K/K--full-text.md"\n'
                     '    checked_edition: "No. 459, 26 May 2021 (as published)"\n'
                     '  - title: "Law J, OSCAL catalogue"\n'
                     '    path: "legislation/J/J.json"\n'
                     '    checked_edition: "Release J 2024"\n')

        def _catalogue(self, text: str) -> Path:
            d = self._tmp()
            (d / "catalogue.yml").write_text(text, encoding="utf-8")
            self._extract(d, "legislation/K/K--full-text.md", self.MARKER_NOTES["INCOMPLETE BODY"])
            return d

        def test_catalogue_field_match_checks_record_extract(self):
            d = self._catalogue(self.CATALOGUE)
            rc, out, err = self._run(d, "No. 459, 26 May 2021")
            self.assertEqual(rc, 3, out + err)
            self.assertIn("incomplete extract: legislation/K/K--full-text.md", out)

        def test_catalogue_record_without_extract_not_attributed(self):
            d = self._catalogue(self.CATALOGUE)
            rc, out, err = self._run(d, "Release J 2024")
            self.assertEqual(rc, 0, out + err)
            self.assertNotIn("incomplete", out.lower())

        # 3b365 r3: publication records name their extract in an "extract:" field.
        def test_catalogue_extract_field_checks_record_extract(self):
            d = self._catalogue("publications:\n"
                                '  - title: "Deck K overview"\n'
                                '    extract: "legislation/K/K--full-text.md"\n'
                                '    notes: "Slides 16 to 18 are photos."\n')
            rc, out, err = self._run(d, "Slides 16 to 18")
            self.assertEqual(rc, 3, out + err)
            self.assertIn("incomplete extract: legislation/K/K--full-text.md", out)

        def test_catalogue_blank_and_comment_lines_keep_record_open(self):
            d = self._catalogue("standards:\n"
                                '  - title: "Law K"\n'
                                '    path: "legislation/K/K--full-text.md"\n'
                                "\n"
                                "    # edition re-checked 2026-10\n"
                                '    checked_edition: "Edition K 2026"\n')
            rc, out, err = self._run(d, "Edition K 2026")
            self.assertEqual(rc, 3, out + err)
            self.assertIn("incomplete extract: legislation/K/K--full-text.md", out)

        def test_catalogue_new_record_or_section_closes_record(self):
            d = self._catalogue("standards:\n"
                                '  - title: "Law K"\n'
                                '    path: "legislation/K/K--full-text.md"\n'
                                '  - title: "Law W, no extract"\n'
                                '    checked_edition: "Edition W 2026"\n'
                                "frameworks:\n"
                                '    checked_edition: "Edition Y 2026"\n')
            for query in ("Edition W 2026", "Edition Y 2026"):
                rc, out, err = self._run(d, query)
                self.assertEqual(rc, 0, query + out + err)
                self.assertNotIn("incomplete", out.lower())

        def test_catalogue_record_with_two_path_fields_not_attributed(self):
            for second in ('    path: "legislation/K/K.json"\n', '    extract: null\n',
                           '    extract: "legislation/K/K--full-text.md"\n'):
                d = self._catalogue("standards:\n"
                                    '  - title: "Law K"\n'
                                    '    path: "legislation/K/K--full-text.md"\n'
                                    f"{second}"
                                    '    checked_edition: "Edition K 2026"\n')
                rc, out, err = self._run(d, "Edition K 2026")
                self.assertEqual(rc, 0, second + out + err)
                self.assertNotIn("incomplete", out.lower())

        def test_catalogue_two_field_record_own_path_line_names_its_path(self):
            # 3b365 r4: a match on the field line itself names the path it holds (the line names the
            # extract directly), though the record's other lines name none.
            d = self._catalogue("standards:\n"
                                '  - title: "Law K"\n'
                                '    path: "legislation/K/K--full-text.md"\n'
                                '    path: "legislation/K/K.json"\n'
                                '    checked_edition: "Edition K 2026"\n')
            rc, out, err = self._run(d, "K--full-text")
            self.assertEqual(rc, 3, out + err)
            self.assertIn("incomplete extract: legislation/K/K--full-text.md", out)
            rc, out, err = self._run(d, "Law K")
            self.assertEqual(rc, 0, out + err)
            self.assertNotIn("incomplete", out.lower())

        def test_catalogue_record_with_non_extract_path_not_attributed(self):
            d = self._catalogue("publications:\n"
                                '  - title: "Book K"\n'
                                "    extract: null\n"
                                '    notes: "Book K is held as an epub."\n')
            rc, out, err = self._run(d, "Book K is held")
            self.assertEqual(rc, 0, out + err)
            self.assertNotIn("incomplete", out.lower())

        # 3b365 r3: with a "---" in the first 40 lines, a note between the bullets and it is header.
        def test_screening_note_before_separator_is_header(self):
            d = self._mk("- Deck G (`publications/G--full-text.md`)\n")
            self._write(d, "publications/G--full-text.md",
                        f"# Title\n\n{self.COMPLETE}\n## Screening note\n\n"
                        "KEPT (partial). PARTIAL: the appendix tables are not captured.\n\n---\n\nBody text.\n")
            rc, out, err = self._run(d, "Deck G")
            self.assertEqual(rc, 3, out + err)
            self.assertIn("PARTIAL: the appendix tables are not captured.", out)

        def test_separator_rule_body_marker_after_separator_held(self):
            d = self._mk("- Deck H (`publications/H--full-text.md`)\n")
            self._write(d, "publications/H--full-text.md",
                        f"# Title\n\n{self.COMPLETE}\n## Screening note\n\nKEPT (full text).\n\n---\n\n"
                        "The archive says Not recovered in its text.\n")
            rc, out, err = self._run(d, "Deck H")
            self.assertEqual(rc, 0, out + err)
            self.assertNotIn("incomplete", out.lower())

        def test_no_separator_second_bullet_block_not_header(self):
            # Residual, documented: without a "---" the header ends at the first blank after a bullet.
            d = self._mk("- Standard R (`standards/R/R--full-text.md`)\n")
            self._write(d, "standards/R/R--full-text.md",
                        f"# Title\n\n{self.COMPLETE}\n{self.MARKER_NOTES['PARTIAL:']}\nBody text.\n")
            rc, out, err = self._run(d, "Standard R")
            self.assertEqual(rc, 0, out + err)

        def test_self_test_temp_directories_are_removed_after_each_test(self):
            made: list[Path] = []

            class Probe(unittest.TestCase):
                def runTest(probe):
                    made.append(T._tmp(probe))
                    made.append(T._outside(probe, "O--full-text.md"))
                    made.append(T._catalogue(probe, T.CATALOGUE))
                    probe.assertTrue(all(p.is_dir() for p in made))

            Probe._extract, Probe._write = T._extract, T._write
            Probe._tmp, Probe.COMPLETE = T._tmp, T.COMPLETE
            Probe.MARKER_NOTES = T.MARKER_NOTES
            result = unittest.TestResult()
            Probe().run(result)
            self.assertTrue(result.wasSuccessful(), result.errors + result.failures)
            self.assertEqual(len(made), 3)
            self.assertEqual([p for p in made if os.path.lexists(p)], [])

        def test_mixed_complete_and_incomplete_held_with_warning(self):
            d = self._mk("- Law M edition 1 (`legislation/M/M1--full-text.md`)\n"
                         "- Law M edition 2 (`legislation/M/M2--full-text.md`)\n")
            self._extract(d, "legislation/M/M1--full-text.md", self.COMPLETE)
            self._extract(d, "legislation/M/M2--full-text.md", self.INCOMPLETE)
            rc, out, err = self._run(d, "Law M")
            self.assertEqual(rc, 0, out + err)
            self.assertTrue(out.startswith("HELD: "), out)
            self.assertNotIn("HELD-INCOMPLETE", out)
            self.assertIn("WARNING", out)
            warning = out[out.index("WARNING"):]
            self.assertIn("the part each note describes is not quotable from the extract", warning)
            self.assertNotIn("their text is not quotable", warning)
            self.assertIn("legislation/M/M2--full-text.md", warning)
            self.assertNotIn("legislation/M/M1--full-text.md", warning)
            self.assertIn(self.INCOMPLETE.strip(), warning)

        def test_unreadable_extract_cannot_evaluate(self):
            d = self._mk("- Law U (`legislation/U/U--full-text.md`)\n")
            (d / "legislation/U/U--full-text.md").mkdir(parents=True)  # present, but not a readable file
            rc, out, err = self._run(d, "Law U")
            self.assertEqual(rc, 2, out + err)
            self.assertNotIn("HELD", out)
            self.assertIn("CANNOT-EVALUATE", err)
            self.assertIn("legislation/U/U--full-text.md", err)

        def test_missing_extract_cannot_evaluate(self):
            d = self._mk("- Law X (`legislation/X/X--full-text.md`)\n")
            rc, out, err = self._run(d, "Law X")
            self.assertEqual(rc, 2, out + err)
            self.assertNotIn("HELD", out)
            self.assertIn("CANNOT-EVALUATE", err)

        def test_unreadable_extract_beside_complete_cannot_evaluate(self):
            d = self._mk("- Law V one (`legislation/V/V1--full-text.md`)\n"
                         "- Law V two (`legislation/V/V2--full-text.md`)\n")
            self._extract(d, "legislation/V/V1--full-text.md", self.COMPLETE)
            (d / "legislation/V/V2--full-text.md").mkdir(parents=True)
            rc, out, err = self._run(d, "Law V")
            self.assertEqual(rc, 2, out + err)
            self.assertIn("CANNOT-EVALUATE", err)

        def _assert_outside(self, d: Path, query: str) -> None:
            rc, out, err = self._run(d, query)
            self.assertEqual(rc, 2, out + err)
            self.assertNotIn("HELD", out)
            self.assertIn("outside the reference base", err)

        def test_extract_path_outside_reference_base_cannot_evaluate(self):
            o = self._outside("O--full-text.md")
            d = self._mk(f"- Law O (`../{o.name}/O--full-text.md`)\n")
            self.assertTrue((d / ".." / o.name / "O--full-text.md").is_file())
            self._assert_outside(d, "Law O")

        def test_absolute_extract_path_cannot_evaluate(self):
            o = self._outside("O--full-text.md")
            d = self._mk(f"- Law O (`{o / 'O--full-text.md'}`)\n")
            self.assertTrue(Path(o / "O--full-text.md").is_absolute())
            self._assert_outside(d, "Law O")

        def test_file_symlink_escape_cannot_evaluate(self):
            o = self._outside("O--full-text.md")
            d = self._mk("- Law S (`legislation/S/S--full-text.md`)\n")
            self._link(o / "O--full-text.md", d / "legislation/S/S--full-text.md")
            self._assert_outside(d, "Law S")

        def test_directory_symlink_escape_cannot_evaluate(self):
            o = self._outside("D/D--full-text.md")
            d = self._mk("- Law D (`legislation/D/D--full-text.md`)\n")
            self._link(o / "D", d / "legislation/D", is_dir=True)
            self._assert_outside(d, "Law D")

        def test_symlink_inside_reference_base_followed(self):
            d = self._mk("- Law L (`legislation/L/L--full-text.md`)\n")
            self._extract(d, "legislation/real/L--full-text.md", self.MARKER_NOTES["Not recovered"])
            self._link(d / "legislation/real/L--full-text.md", d / "legislation/L/L--full-text.md")
            rc, out, err = self._run(d, "Law L")
            self.assertEqual(rc, 3, out + err)

        def test_fifo_extract_cannot_evaluate(self):
            import threading
            if not hasattr(os, "mkfifo"):
                self.skipTest("os.mkfifo is unavailable")
            d = self._mk("- Law F (`legislation/F/F--full-text.md`)\n")
            fifo = d / "legislation/F/F--full-text.md"
            fifo.parent.mkdir(parents=True)
            try:
                os.mkfifo(fifo)
            except OSError as exc:
                self.skipTest(f"cannot create a FIFO here ({exc})")
            result: list = []
            worker = threading.Thread(target=lambda: result.append(self._run(d, "Law F")), daemon=True)
            worker.start()
            worker.join(10)
            if worker.is_alive():
                # Release a reader blocked opening the FIFO, so the failure is reported, not a hang.
                os.close(os.open(fifo, os.O_WRONLY))
                worker.join(10)
                self.fail("reading a FIFO extract blocked")
            rc, out, err = result[0]
            self.assertEqual(rc, 2, out + err)
            self.assertIn("not a regular file", err)

    suite = unittest.TestLoader().loadTestsFromTestCase(T)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def _identity_is_adopter(identity: dict) -> bool:
    """PURE decision over a detect-env ``probe_identity`` result: an operator is an
    adopter ONLY on a SUCCESSFULLY-READ, non-maintainer origin. A None/absent
    ``origin_url`` is NOT treated as adopter -- detect-env swallows a git-origin
    probe FAILURE (e.g. a subprocess timeout, rc 124) into a None origin, which
    ``probe_identity`` then classifies as ``adopter``; keying on that classification
    alone would let a MAINTAINER's transient git timeout silently no-op the
    missing-grc_library_ref HALT. Fail SAFE: only a positively-read fork/private
    origin degrades; a None origin, a maintainer origin, or any missing field ->
    False (loud). Pure + injectable so the fail-safe is regression-locked (the
    guard-input pure-decision-behind-a-thin-observer discipline)."""
    origin_url = identity.get("origin_url")
    # Degrade ONLY on a fully-formed non-maintainer identity: a non-empty STRING
    # origin_url AND the maintainer flag EXACTLY False. isinstance-guarding the url
    # (probe_identity yields str|None) and requiring `is False` make the decision
    # monotonically fail-safe: any None/empty/non-str origin, or any non-exactly-
    # False flag, -> False (loud). This TRUSTS probe_identity to produce a (url,
    # flag) pair consistent with each other (the flag is derived from the url); a
    # dict whose flag CONTRADICTS its url is non-producible by that observer, and
    # re-deriving maintainer-ness from the url here would duplicate detect-env's
    # canonical origin check (forbidden by the guard-input single-source rule).
    return isinstance(origin_url, str) and bool(origin_url) and identity.get("origin_is_maintainer_repo") is False


def _operator_is_adopter() -> bool:
    """True ONLY if the operator has a positively-read, non-maintainer origin (see
    _identity_is_adopter). Maintainer / maintainer-fresh-machine / undetermined /
    absent-or-unreadable origin / any error -> False, so a maintainer's
    genuinely-missing grc_library_ref stays a LOUD exit-2 failure (the 1.19.7
    (closing PR #1007) loud gate that /orch relies on). Reuses the SINGLE canonical
    identity source (detect-env.py) via importlib (the file is hyphenated, so not
    import-able by name) rather than duplicating the origin check here (the
    guard-input single-source discipline). Only reached on the rare absent-ref
    branch, so the probe cost is not on any hot path."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "detect_env", str(Path(__file__).resolve().parent / "detect-env.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return _identity_is_adopter(mod.probe_identity(mod.probe_siblings()))
    except Exception:
        return False


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description="Answer held/not-held for grc_library_ref from its index (forcing-function; quote the output).",
    )
    p.add_argument("query", nargs="?", help="Substring to search (title, id, or path).")
    p.add_argument("--ref-root", default=None, help="Path to grc_library_ref (default: sibling of this repo).")
    p.add_argument("--self-test", action="store_true", help="Run inline unit tests and exit.")
    a = p.parse_args(argv[1:])

    if a.self_test:
        return _self_test()
    if a.ref_root is not None and not a.ref_root.strip():
        # 3b50b2e1: an empty --ref-root silently fell back to the default sibling.
        print("ERROR: --ref-root needs a directory argument (an empty value is refused).",
              file=sys.stderr)
        return 2
    if not a.query:
        print("ERROR: provide a query (or --self-test). Example: ref-holds.py \"27002\"", file=sys.stderr)
        return 2

    try:
        ref_root = find_ref_root(a.ref_root)
    except InaccessiblePath as exc:
        # Only the default lookup raises this; an explicit root's index errors reach search_index.
        print(f"ERROR: the grc_library_ref sibling is present but cannot be examined ({exc}); "
              f"refusing a verdict (an unreadable reference base is not an absent one).",
              file=sys.stderr)
        return 2
    except (OSError, RuntimeError) as exc:
        # expanduser() raises RuntimeError for an unknown user, and Python 3.11's resolve() raises
        # it on a symlink loop; an explicit root that cannot be resolved is refused (3b50b2e1 r5).
        print(f"ERROR: --ref-root {a.ref_root}: unresolvable ({exc}).", file=sys.stderr)
        return 2
    if ref_root is None:
        # A GENUINELY ABSENT default sibling on an ADOPTER clone degrades to an
        # advisory no-op (exit 0), per 1.19.2 (closing PR #996): ref-holds is a
        # maintainer-only forcing-function tool, and an adopter clone that never
        # fetched grc_library_ref has nothing to answer against. The branch is
        # gated on the detect-env OPERATOR IDENTITY (adopter -> graceful; a
        # maintainer / undetermined identity stays a LOUD exit 2, the 1.19.7 loud
        # gate /orch relies on), NOT on the committed .ref placeholder, which is
        # NOT shipped by default (a fresh adopter clone has no .ref, so the old
        # placeholder gate errored spuriously -- deep-assessment 3.183(3)). It is
        # further gated on resolve_sibling("ref") is None (the real sibling dir
        # truly absent), NOT merely on find_ref_root being None: a real
        # grc_library_ref dir that EXISTS but lacks its index (a corrupt/partial
        # checkout) still errors (exit 2), so a broken ref is surfaced, not masked.
        # An EXPLICIT --ref-root that did not resolve likewise stays the operator's
        # mistake to surface (exit 2).
        if (
            a.ref_root is None
            and resolve_sibling("ref") is None
            and _operator_is_adopter()
        ):
            print(
                "advisory: grc_library_ref sibling absent (adopter clone); "
                "ref-holds is a maintainer-only advisory, nothing to report."
            )
            return 0
        looked = a.ref_root if a.ref_root is not None else DEFAULT_REF_ROOT
        print(
            "ERROR: could not locate a readable grc_library_ref index (INDEX.md or catalogue.yml). "
            f"Pass --ref-root /path/to/grc_library_ref (looked in {looked}).",
            file=sys.stderr,
        )
        return 2
    return run(ref_root, a.query)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
