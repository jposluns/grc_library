"""PR1 behavior fixtures: stdlib only; synthetic inputs stay in memory."""
import json
import re
import contextlib
import io
import os
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

if "W" not in globals():
    import importlib.util
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(ROOT / "tools"))
    spec = importlib.util.spec_from_file_location(
        "currency_wrapper", ROOT / "tools/lint-standards-currency.py"
    )
    W = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(W)
    E = W._engine()

H = (
    "| Standard ID | Current version | Publication date | Topic "
    "| Superseded versions |"
)
S = "| --- | --- | --- | --- | --- |"
ROWS = [
    "| ISO/IEC 27001 | 2022 | 2022 | Security | 2013 |",
    "| NIST SP 800-61 | Rev. 3 | 2025 | IR | Rev. 2, Rev. 1 |",
    "| PCI DSS | 4.0.1 | 2024 | Payments | 4.0 |",
    "| SLSA | 1.0 | 2023 | Supply chain | - |",
    "| WCAG | 2.2 | 2023 | Accessibility | 2.1 |",
]
REGISTER = H + "\n" + S + "\n" + "\n".join(ROWS) + "\n"


@contextlib.contextmanager
def memory_tree(root, values):
    root = Path(root).resolve()
    files = {root / name: value for name, value in values.items()}
    dirs = {root}
    for path in files:
        dirs.update(
            p for p in path.parents if p == root or root in p.parents
        )
    original = {
        name: getattr(Path, name)
        for name in ("read_text", "read_bytes", "exists", "is_file", "is_dir")
    }
    old_scandir = os.scandir

    def inside(p):
        return p == root or root in p.parents

    def raw_bytes(p):
        if p not in files:
            raise FileNotFoundError(str(p))
        if isinstance(files[p], Exception):
            raise files[p]
        value = files[p]
        return value if isinstance(value, bytes) else value.encode("utf-8")

    def read(p, *args, **kwargs):
        if not inside(p):
            return original["read_text"](p, *args, **kwargs)
        value = files.get(p)
        if isinstance(value, bytes):
            # A bytes value is the file's raw content, read as Path.read_text reads it: decoded,
            # with universal newlines (a lone CR and a CRLF both become LF).
            return value.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        raw_bytes(p)  # raises for a missing path or an injected error
        return value

    def read_raw(p, *args, **kwargs):
        if not inside(p):
            return original["read_bytes"](p, *args, **kwargs)
        return raw_bytes(p)

    def predicate(name, members):
        return lambda p: (
            p in members if inside(p) else original[name](p)
        )

    @contextlib.contextmanager
    def scan(p):
        p = Path(p)
        if not inside(p):
            with old_scandir(p) as result:
                yield result
            return
        children = sorted(
            c for c in (set(files) | dirs) if c.parent == p
        )
        yield iter(
            SimpleNamespace(
                name=c.name,
                path=str(c),
                is_symlink=lambda: False,
                is_dir=lambda c=c: c in dirs,
            )
            for c in children
        )

    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.object(Path, "read_text", read))
        stack.enter_context(patch.object(Path, "read_bytes", read_raw))
        stack.enter_context(patch.object(
            Path, "exists", predicate("exists", set(files) | dirs)
        ))
        stack.enter_context(patch.object(
            Path, "is_file", predicate("is_file", files)
        ))
        stack.enter_context(patch.object(
            Path, "is_dir", predicate("is_dir", dirs)
        ))
        stack.enter_context(patch("os.scandir", scan))
        yield root


class CitationCoverageTests(unittest.TestCase):
    def occurrences(self, text, suffix=".md"):
        return [
            o for o in E.discover(text, suffix)
            if o["channel"] == "grammar"
        ]

    def kinds(self, text, register=REGISTER):
        entries = W.parse_register_text(register)
        return [
            k for o in self.occurrences(text)
            for k, _ in E.resolve(o, entries)
        ]

    def invoke(
        self, text, *args, suffix=".md", register=REGISTER, exceptions=None, page=None
    ):
        relative = (
            "ai/citation.md" if suffix == ".md"
            else ".web/templates/landing.html"
        )
        values = {
            "governance/register-canonical-citations.md": register,
            relative: text,
        }
        if exceptions is not None:  # 3b75: the historical register data and its generated page
            values[W.HISTORICAL_DATA_REL] = exceptions
            if page is None:
                try:
                    rows = W.HCR.load(exceptions if isinstance(exceptions, str) else exceptions.decode())
                except (W.HCR.RegisterDataError, UnicodeError, AttributeError):
                    rows = []
                page = "# Register\n\n## Exceptions\n\n" + W.HCR.render(rows) + "\n"
        if page is not None and page is not False:  # page=False: the page file is absent
            values[W.HISTORICAL_REGISTER_REL] = page
        with memory_tree("/currency-fixture", values) as root, \
             patch.object(W, "REPO_ROOT", root), \
             patch.object(
                 W, "CANONICAL_REGISTER",
                 root / "governance/register-canonical-citations.md",
             ), \
             contextlib.redirect_stdout(io.StringIO()) as out, \
             contextlib.redirect_stderr(io.StringIO()) as err:
            code = W.main(["--root", str(root), *args])
            return code, out.getvalue(), err.getvalue()

    def test_table_version_column(self):
        # A framework in a table with an explicit Version column carries its
        # edition in that column; it resolves clean, not a false UNPINNED.
        reg = REGISTER + "| COBIT | 2019 | 2018 | Governance | COBIT 5 |\n"
        import json
        versioned = (
            "| Framework | Version | Role |\n"
            "| --- | --- | --- |\n"
            "| COBIT | 2019 | Governance |\n"
        )
        _, out, _ = self.invoke(
            versioned, "--format", "json", register=reg
        )
        cobit = [
            f for f in json.loads(out)["findings"]
            if f["observed"] == "COBIT"
        ]
        self.assertEqual(cobit, [])
        # An ordinary table (no Version/Edition header) must NOT associate a
        # neighbouring cell: the bare framework stays UNPINNED.
        plain = (
            "| Framework | Role |\n"
            "| --- | --- |\n"
            "| COBIT | 2019 governance |\n"
        )
        _, out2, _ = self.invoke(plain, "--format", "json", register=reg)
        cobit2 = [
            f["kind"] for f in json.loads(out2)["findings"]
            if f["observed"] == "COBIT"
        ]
        self.assertEqual(cobit2, ["UNPINNED"])

    def test_missing_row_and_deletion(self):
        self.assertEqual(
            self.kinds("ISO 9001:2015"), ["UNREGISTERED"]
        )
        self.assertEqual(self.kinds("ISO/IEC 27001:2022"), [])
        deleted = REGISTER.replace(ROWS[0] + "\n", "")
        self.assertEqual(
            self.kinds("ISO/IEC 27001:2022", deleted),
            ["UNREGISTERED"],
        )
        self.assertEqual(self.invoke("ISO 9001:2015")[0], 0)
        self.assertEqual(
            self.invoke(
                "ISO 9001:2015", "--coverage-mode", "enforce"
            )[0],
            1,
        )

    def test_normalized_revisions_and_rollout(self):
        for old in ("Rev. 2", "Rev.2", "r2"):
            citation = (
                "NIST SP 800-61"
                + (" " if old != "r2" else "") + old
            )
            self.assertEqual(self.kinds(citation), ["STALE"])
        for new in ("Rev. 3", "Rev.3", "r3"):
            self.assertEqual(
                self.kinds("NIST SP 800-61 " + new), []
            )
        self.assertEqual(
            self.invoke("NIST SP 800-61 Rev. 2")[0], 1
        )
        self.assertEqual(self.invoke("NIST SP 800-61r2")[0], 0)
        self.assertEqual(
            self.invoke(
                "NIST SP 800-61r2", "--coverage-mode", "enforce"
            )[0],
            1,
        )

    def test_identity_and_ambiguity(self):
        self.assertEqual(
            self.kinds("ISO 27001:2022"), ["NONCANONICAL_ID"]
        )
        self.assertEqual(
            self.kinds("ISO/IEC 27001-1:2022"), ["UNREGISTERED"]
        )
        two = (
            REGISTER
            + "| IEC 27001 | 2022 | 2022 | Different issuer | - |\n"
        )
        self.assertEqual(
            self.kinds("ISO 27001:2022", two), ["AMBIGUOUS"]
        )
        for a, b in [
            ("ISO 12345", "IEC 12345"),
            ("ISO TS 12345", "ISO TR 12345"),
            ("NIST SP 1234", "NIST IR 1234"),
            ("ISO 12345", "ISO 12345-1"),
        ]:
            self.assertNotEqual(E.identity_key(a), E.identity_key(b))

    def test_versions_and_pins(self):
        self.assertEqual(
            self.kinds("ISO/IEC 27001 §9.3"), ["UNPINNED"]
        )
        self.assertEqual(self.kinds("SLSA Level 3"), ["UNPINNED"])
        self.assertEqual(self.kinds("WCAG 2.2 AA"), [])
        self.assertEqual(
            self.kinds("WCAG 2.1.1 AA"), ["UNRESOLVED_EDITION"]
        )
        self.assertEqual(self.invoke("PCI DSS v4.0")[0], 1)
        self.assertEqual(self.invoke("PCI DSS v4.0.1")[0], 0)
        final = (
            REGISTER
            + "| NIST SP 800-208 | Final | 2020 | Crypto | - |\n"
        )
        self.assertEqual(
            self.kinds("NIST SP 800-208", final), ["UNPINNED"]
        )
        o = self.occurrences("NIST SP 800-208")[0]
        self.assertEqual(
            E.resolve(
                o, W.parse_register_text(final),
                {o["identity"]: "Synthetic evidence-backed exception"},
            ),
            [],
        )

    def test_parser_integrity(self):
        self.assertEqual(len(W.parse_register_text(REGISTER)), 5)
        seven = REGISTER.replace(
            H, H + " Upstream check location | Last verified (UTC) |"
        )
        seven = seven.replace(S, S + " --- | --- |")
        for row in ROWS:
            seven = seven.replace(
                row, row + " https://iso.org | needs-reconfirm |"
            )
        self.assertEqual(
            W.parse_register_text(seven)[0]["source_line"], 3
        )
        self.assertEqual(
            W.parse_register_text(seven)[0]["superseded_raw"], "2013"
        )
        for malformed in [
            REGISTER.replace("Standard ID", "Standard identifier"),
            REGISTER.replace(S, "| --- | --- |"),
            REGISTER.replace(ROWS[0], ROWS[0][:-1]),
            REGISTER.replace("2022 | 2022", "| 2022", 1),
            REGISTER + ROWS[0] + "\n",
            H + "\n" + S + "\n",
        ]:
            with self.assertRaises(W.RegisterError):
                W.parse_register_text(malformed)

        tooling = (
            "\n## AI security tooling references\n\n| "
            + " | ".join(W.PROJECT_HEADER) + " |\n"
            + "| " + " | ".join(["---"] * 8) + " |\n"
            + "| Demo | 1 | 2026 | Tool | MIT | Active "
            "| https://iso.org | pending |\n"
        )
        self.assertEqual(
            len(W.parse_register_text(REGISTER + tooling)), 5
        )
        empty = (
            REGISTER + "\n## Empty standards section\n\n"
            + H + "\n" + S + "\n"
        )
        self.assertEqual(len(W.parse_register_text(empty)), 5)

    def test_carry_and_boundaries(self):
        found = self.occurrences(
            "ISO/IEC 27001:2022 and 27002:2022. 27003:2022"
        )
        self.assertEqual(
            [o["observed"] for o in found],
            ["ISO/IEC 27001", "ISO/IEC 27002"],
        )
        for text in [
            "ISO/IEC 27001:2022 | 27002:2022",
            "ISO/IEC 27001:2022 and 12 controls",
            "ISO/IEC 27001:2022 and NIST SP 800-61r3 and 27002:2022",
        ]:
            self.assertFalse(any(
                o["observed"].endswith("27002")
                for o in self.occurrences(text)
            ))

    def test_rendering(self):
        html = (
            "<p>ISO/<em>IEC</em>\n27001&#58;2022</p>"
            "<li>ISO/IEC</li><li>27002:2022</li>"
        )
        found = self.occurrences(html, ".html")
        self.assertEqual(
            [(o["observed"], o["version"]) for o in found],
            [("ISO/IEC 27001", "2022")],
        )
        self.assertEqual(found[0]["span"][0], [1, 4])
        for text in [
            "<script>ISO 9001:2015</script>",
            "<!-- ISO 9001:2015 -->",
            '<a href="ISO 9001:2015">link</a>',
            "<style>ISO 9001:2015</style>",
        ]:
            self.assertEqual(self.occurrences(text, ".html"), [])
        self.assertEqual(len(self.occurrences(
            '<img alt="ISO 9001:2015">', ".html"
        )), 1)
        self.assertEqual(len(self.occurrences(
            "[ISO 9001:2015](https://iso.org/ISO-7777)"
        )), 1)
        self.assertEqual(
            self.occurrences("[link](ISO 9001:2015)"), []
        )
        self.assertEqual(
            self.occurrences("~~~\nISO 9001:2015\n~~~"), []
        )
        self.assertEqual(
            self.kinds("Formerly ISO/IEC 27001:2013"), ["STALE"]
        )

    def test_scope_and_errors(self):
        values = {
            "governance/register-canonical-citations.md": REGISTER,
            "ai/citation.md": "ISO 9001:2015",
            ".web/templates/landing.html": "ISO 9001:2015",
            ".web/templates/partials/footer.html": "WCAG 2.1",
            ".web/templates-v2/landing.html": "ISO 9001:2015",
            ".web/templates-v3/landing.html": "ISO 9001:2015",
            ".web/dist/index.html": "ISO 9001:2015",
            "CHANGELOG.md": "ISO/IEC 27001:2013",
        }
        with memory_tree("/currency-scope", values) as root, \
             patch.object(W, "REPO_ROOT", root):
            files = W.iter_files([".", "ai", "ai/citation.md"])
            self.assertEqual(
                [p.relative_to(root).as_posix() for p in files],
                [
                    ".web/templates/landing.html",
                    ".web/templates/partials/footer.html",
                    "ai/citation.md",
                ],
            )
            self.assertEqual(
                W.iter_files(["ai"]), [root / "ai/citation.md"]
            )
            with self.assertRaises(OSError):
                W.iter_files(["../outside"])
            with self.assertRaises(OSError):
                W.iter_files(["missing.md"])

        code, out, err = self.invoke(PermissionError("unreadable"))
        self.assertEqual(code, 2)
        self.assertIn("unreadable", err)
        self.assertEqual(self.invoke("x", register="")[0], 1)
        with memory_tree("/currency-missing", {}), \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(
                W.main(["--root", "/currency-missing"]), 2
            )

    def test_all_families_and_diagnostics(self):
        text = (
            "ISO/IEC/IEEE 42010:2022; ISO/IEC TS 25058:2024; "
            "NIST IR 8286r1; NIST AI 100-2e2025; NIST SP 1270; "
            "FIPS 140-3; NIST AI RMF 1.0; NIST CSF 2.0; IEEE 2883-2022; "
            "ETSI EN 304 223 V2.1.1; CEN TS 12345:2020; EN 301 549; "
            "CIS Controls v8.1; ITIL 4; WCAG 2.2 AA; COBIT 2019; "
            "SLSA Level 3"
        )
        self.assertEqual(len(self.occurrences(text)), 17)
        code, out, err = self.invoke(
            "ISO 9001:2015\n\nISO 9001:2015", "--format", "json"
        )
        import json
        report = json.loads(out)
        self.assertEqual(
            report["inventories"]["UNREGISTERED"]["identities"], 1
        )
        self.assertEqual(
            report["inventories"]["UNREGISTERED"]["occurrences"], 2
        )
        self.assertEqual(
            [f["span"][0] for f in report["findings"]],
            [[1, 1], [3, 1]],
        )
        self.assertEqual(code, 0)

    def test_html_and_review_modes(self):
        self.assertEqual(self.invoke(
            "<p>ISO/IEC 27001:2013</p>", suffix=".html"
        )[0], 0)
        self.assertEqual(self.invoke(
            "<p>ISO/IEC 27001:2013</p>",
            "--coverage-mode", "enforce", suffix=".html"
        )[0], 1)
        code, out, err = self.invoke(
            "ISO/IEC 27001:2099", "--coverage-mode", "enforce"
        )
        self.assertEqual(code, 0)
        self.assertIn("advisory review remains", out)
        self.assertNotIn("OK:", out)
        self.assertTrue(any(
            o["channel"] == "candidate"
            for o in E.discover("NIST future publication", ".md")
        ))


# 3b75: the sanctioned historical-context form (policy register + engine binding).
HREG = (
    REGISTER
    + "| ISO/IEC 27002 | 2022 | 2022 | Controls | 2013 |\n"
    + "| ISO/IEC 27701 | 2025 | 2025 | PIMS | 2019 |\n"
)
# 3b75 redesign: the rows live in a TOML data file; the Markdown page is a generated view.
HXHEAD = "schema_version = 1\n"
HSENT = (
    "The 2019 edition of ISO/IEC 27701 extended ISO/IEC 27001:2013 "
    "with privacy-specific controls."
)
HURL = "https://www.iso.org/standard/71670.html"


def hrow(sentence=HSENT, citation="ISO/IEC 27001:2013", path="ai/citation.md",
         xid="HCE-001", url=HURL, verified="2026-09-01",
         reason="Records the edition lineage accurately."):
    """One [[exception]] table; strings as TOML basic strings (JSON escaping is valid TOML)."""
    import json as _json
    q = _json.dumps
    return ("\n[[exception]]\nid = %s\npath = %s\ncitation = %s\nsentence = %s\n"
            "reason = %s\nupstream = %s\nverified = %s\n") % (
        q(xid), q(path), q(citation), q(sentence), q(reason), q(url), verified)


def hx(*rows):
    return HXHEAD + "".join(rows or (hrow(),))


def assert_refused(tc, doc, sent, citation="ISO/IEC 27001:2013", msg=None):
    """Both layers refuse the declaration (3b75 QA r7): the gate exits 1 with no HISTORICAL finding,
    by the wrapper's register screen or the engine's INVALID_EXCEPTION, AND the engine alone, given
    the declaration directly, sanctions nothing, so its binding rules keep their own coverage now
    that the wrapper screens most malformed sentences first. Returns the engine's error details."""
    msg = msg or repr(doc)
    code, found, err = tc.run_json(doc, hx(hrow(sent, citation=citation)))
    tc.assertEqual(code, 1, msg)
    kinds = [f["kind"] for f in found]
    tc.assertNotIn("HISTORICAL", kinds, msg)
    if "INVALID_EXCEPTION" not in kinds:
        tc.assertIn("ERROR: historical register", err, msg)
    wrapper = CitationCoverageTests.invoke.__globals__["W"]
    eng = wrapper._engine()
    entries = wrapper.parse_register_text(HREG)
    occ = [o for o in eng.discover(citation, ".md") if o["channel"] == "grammar"][0]
    ex = dict(id="HCE-001", path="ai/citation.md", sentence=sent, citation=citation, reason="r",
              identity=occ["identity"], edition=eng.edition_key(occ["version"]))
    raw = doc.decode("utf-8") if isinstance(doc, bytes) else doc
    source = raw.replace("\r\n", "\n").replace("\r", "\n") if isinstance(doc, bytes) else raw
    _, sanctioned, errors = eng.apply_historical_exceptions(
        source, "ai/citation.md", [ex], entries, raw=raw
    )
    tc.assertEqual(sanctioned, [], msg)
    tc.assertTrue(errors, msg)
    return [e["detail"] for e in errors]


class HistoricalContextTests(unittest.TestCase):
    invoke = CitationCoverageTests.invoke

    def run_json(self, text, exceptions, *args, register=HREG, page=None):
        code, out, err = self.invoke(
            text, "--format", "json", *args,
            register=register, exceptions=exceptions, page=page,
        )
        return code, (json.loads(out)["findings"] if out.strip() else []), err

    @staticmethod
    def kinds_of(findings):
        return sorted(
            (f["kind"], f["observed"], f["legacy"]) for f in findings
        )

    def test_sanctioned_historical_citation_passes(self):
        code, found, _ = self.run_json(HSENT + "\n", hx())
        self.assertEqual(code, 0)
        hist = [f for f in found if f["kind"] == "HISTORICAL"]
        self.assertEqual(
            [(f["observed"], f["version"], f["span"]) for f in hist],
            [("ISO/IEC 27001", "2013", [[1, 44], [1, 61]])],
        )
        self.assertTrue(hist[0]["detail"].startswith("HCE-001: "))
        self.assertNotIn("STALE", [f["kind"] for f in found])
        _, out, _ = self.invoke(HSENT + "\n", register=HREG, exceptions=hx())
        self.assertIn(
            "SANCTIONED ISO/IEC 'ISO/IEC 27001' edition='2013': HCE-001: ",
            out,
        )
        self.assertIn("HISTORICAL: 1 identities; 1 occurrences", out)

    def test_unmarked_citation_still_blocks(self):
        for exceptions in (None, HXHEAD):
            code, out, _ = self.invoke(
                HSENT + "\n", register=HREG, exceptions=exceptions
            )
            self.assertEqual(code, 1)
            self.assertIn(
                "BLOCKING ISO/IEC 'ISO/IEC 27001' edition='2013'", out
            )
        # A declaration binds to its path only.
        code, found, _ = self.run_json(
            HSENT + "\n", hx(hrow(path="ai/other.md")),
            "--paths", "ai/citation.md",
        )
        self.assertEqual(code, 1)
        self.assertIn(("STALE", "ISO/IEC 27001", True), self.kinds_of(found))
        # A default run refuses a row naming an unscanned path.
        code, _, err = self.invoke(
            HSENT + "\n", register=HREG, exceptions=hx(hrow(path="ai/other.md"))
        )
        self.assertEqual(code, 1)
        self.assertIn(
            "historical exception(s) outside the scan scope: HCE-001", err
        )

    def test_current_tense_declaration_refused(self):
        for sentence, message in [
            ("ISO/IEC 27001:2013 requires a Statement of Applicability.",
             "present-tense wording 'requires'"),
            ("Until 2025, ISO/IEC 27001:2013 remains the certification "
             "basis.", "present-tense wording 'remains'"),
            ("Auditors certified sites against ISO/IEC 27001:2013 in 2020.",
             "sentence carries no historical-context cue"),
        ]:
            code, _, err = self.invoke(
                sentence + "\n", register=HREG, exceptions=hx(hrow(sentence))
            )
            self.assertEqual(code, 1, sentence)
            self.assertIn("HCE-001: " + message, err)

    def test_fragment_of_longer_sentence_refused(self):
        for doc, sentence in [
            ("The previous edition ISO/IEC 27001:2013 governs "
             "certification here.\n",
             "The previous edition ISO/IEC 27001:2013"),
            ("Our programme relies on\nthe previous edition ISO/IEC "
             "27001:2013 for certification.\n",
             "the previous edition ISO/IEC 27001:2013 for certification."),
            ("Today we rely on the previous edition ISO/IEC 27001:2013 for "
             "certification.\n",
             "the previous edition ISO/IEC 27001:2013 for certification."),
        ]:
            self.assertIn(
                "HCE-001: declared sentence is not a standalone paragraph at its site (the whole line from column 1, blank lines above and below)",
                assert_refused(self, doc, sentence),
            )
            # Where the engine was reached (the wrapper accepted the row), the citation still blocks.
            _, found, err = self.run_json(doc, hx(hrow(sentence)))
            if "ERROR: historical register" not in err:
                self.assertIn(("STALE", "ISO/IEC 27001", True), self.kinds_of(found))

    def test_only_declared_occurrences_are_masked(self):
        both = (
            "The 2019 edition of ISO/IEC 27701 extended "
            "ISO/IEC 27001:2013 and ISO/IEC 27002:2013."
        )
        code, found, _ = self.run_json(both + "\n", hx(hrow(both)))
        self.assertEqual(code, 1)
        kinds = self.kinds_of(found)
        self.assertIn(("HISTORICAL", "ISO/IEC 27001", False), kinds)
        self.assertIn(("STALE", "ISO/IEC 27002", True), kinds)
        # The same citation on the same line, outside the sentence.
        sentence = (
            "The previous edition, ISO/IEC 27001:2013, was withdrawn in 2022."
        )
        line = "ISO/IEC 27001:2013 anchors this control set. " + sentence
        code, found, _ = self.run_json(line + "\n", hx(hrow(sentence)))
        self.assertEqual(code, 1)
        self.assertEqual(
            [f["span"][0] for f in found
             if f["kind"] == "STALE" and f["legacy"]],
            [[1, 1]],
        )
        # Another superseded edition of the same standard is not declared.
        two = HREG.replace(
            "| Security | 2013 |", "| Security | 2013, 2005 |"
        )
        mixed = "ISO/IEC 27001:2005 was replaced by ISO/IEC 27001:2013."
        code, found, _ = self.run_json(
            mixed + "\n", hx(hrow(mixed, citation="ISO/IEC 27001:2005")),
            register=two,
        )
        self.assertEqual(code, 1)
        self.assertEqual(
            sorted((f["kind"], f["version"]) for f in found),
            [("HISTORICAL", "2005"), ("STALE", "2013")],
        )

    def test_edited_or_duplicated_sentence_is_invalid(self):
        edited = HSENT.replace("privacy-specific", "privacy")
        code, found, _ = self.run_json(edited + "\n", hx())
        self.assertEqual(code, 1)
        self.assertIn(
            "HCE-001: declared sentence not found",
            [f["detail"] for f in found],
        )
        code, found, _ = self.run_json(HSENT + "\n\n" + HSENT + "\n", hx())
        self.assertEqual(code, 1)
        self.assertIn(
            "HCE-001: declared sentence occurs 2 times",
            [f["detail"] for f in found],
        )
        # An unused declaration blocks even with no stale citation present.
        code, out, _ = self.invoke(
            "No citations here.\n", register=HREG, exceptions=hx()
        )
        self.assertEqual(code, 1)
        self.assertIn("BLOCKING exception 'HCE-001'", out)

    def test_enforce_mode_honours_only_the_sanction(self):
        s = "The previous edition, ISO/IEC 27001:2013, was withdrawn in 2022."
        mode = ("--coverage-mode", "enforce")
        self.assertEqual(self.invoke(
            s + "\n", *mode, register=HREG, exceptions=hx(hrow(s)))[0], 0)
        self.assertEqual(
            self.invoke(s + "\n", *mode, register=HREG)[0], 1)

    def test_declaration_schema(self):
        current = HSENT.replace("27001:2013", "27001:2022")
        for exceptions, message in [
            (hx(hrow(current, citation="ISO/IEC 27001:2022")),
             "is not exactly one registered superseded edition"),
            (hx(hrow(url="-")), "upstream evidence URL required"),
            (hx(hrow(verified="2999-01-01")), "must be a date on or before today"),
            (hx(hrow(xid="H-1")), "needs a unique HCE-NNN id"),
            (hx(hrow(), hrow()), "needs a unique HCE-NNN id"),
            (hx(hrow(path="../x.md")), "path must be a canonical repo .md path"),
            (hx(hrow(path="ai//x.md")), "path must be a canonical repo .md path"),
            (hx(hrow().replace("reason =", "why =")), "fields must be exactly"),
        ]:
            code, _, err = self.invoke(
                HSENT + "\n", register=HREG, exceptions=exceptions
            )
            self.assertEqual(code, 1, exceptions)
            self.assertIn(message, err)

    def test_engine_refuses_non_stale_declaration(self):
        # Engine contract, independent of the wrapper's parse-time screen.
        text = "The previous edition was replaced by ISO/IEC 27001:2022.\n"
        declared = dict(
            id="HCE-009", path="ai/citation.md", reason="engine contract",
            sentence=text.strip(), identity=E.identity_key("ISO/IEC 27001"),
            edition=E.edition_key("2022"),
        )
        masked, sanctioned, errors = E.apply_historical_exceptions(
            text, "ai/citation.md", [declared], W.parse_register_text(HREG)
        )
        self.assertEqual((masked, sanctioned), (text, []))
        self.assertEqual(
            [f["detail"] for f in errors],
            ["HCE-009: no registered superseded citation of the declared "
             "edition inside the declared sentence"],
        )


class HistoricalContextRoundTwoTests(unittest.TestCase):
    """3b75 QA round 1 (claude, codex): each counterexample is a regression."""
    invoke = CitationCoverageTests.invoke
    run_json = HistoricalContextTests.run_json

    def test_neighbouring_series_member_is_still_found(self):
        sent = "The earlier ISO/IEC 27001:2013 and 27002:2013 editions were withdrawn in 2022."
        base_code, base, _ = self.run_json(sent + "\n", None, "--coverage-mode", "enforce")
        self.assertEqual(base_code, 1)
        self.assertTrue(any(f["kind"] == "STALE" and "27002" in f["observed"] for f in base))
        for mode, want in (("enforce", 1), ("report", 0)):
            code, found, _ = self.run_json(sent + "\n", hx(hrow(sent)), "--coverage-mode", mode)
            self.assertEqual(code, want, mode)
            self.assertEqual([f["observed"] for f in found if f["kind"] == "HISTORICAL"], ["ISO/IEC 27001"])
            self.assertTrue(any(f["kind"] == "STALE" and "27002" in f["observed"] for f in found), mode)

    def test_binding_refuses_fragments_and_runs(self):
        for doc, sent in [
            ("The earlier ISO/IEC 27001:2013 edition\ngoverns our audits today.\n",
             "The earlier ISO/IEC 27001:2013 edition"),
            ("> Our programme was built\n> on the previous edition ISO/IEC 27001:2013 for certification.\n",
             "on the previous edition ISO/IEC 27001:2013 for certification."),
            ("Standards we apply:\n- The earlier ISO/IEC 27001:2013 edition.\n",
             "The earlier ISO/IEC 27001:2013 edition."),
            ("Our programme covers, e.g. The earlier ISO/IEC 27001:2013 edition.\n",
             "The earlier ISO/IEC 27001:2013 edition."),
            ("ISO/IEC 27001:2013 was withdrawn in 2022. The earlier edition followed.\n",
             "ISO/IEC 27001:2013 was withdrawn in 2022. The earlier edition followed."),
        ]:
            assert_refused(self, doc, sent)

    def test_sanction_is_one_occurrence_only(self):
        sent = "The earlier ISO/IEC 27001:2013 edition was withdrawn."
        # Another citation on the SAME line: the sentence is not the whole line, so nothing binds.
        code, found, _ = self.run_json(sent + " ISO/IEC 27001:2013 again.\n", hx(hrow(sent)))
        self.assertEqual(code, 1)
        self.assertIn("INVALID_EXCEPTION", [f["kind"] for f in found])
        self.assertIn("STALE", [f["kind"] for f in found])
        # On ANOTHER line (its own paragraph): the sentence binds; the other stays STALE.
        doc = sent + "\n\n" + "Line two is " + "ISO/IEC 27001:2013 edition.\n"
        code, found, _ = self.run_json(doc, hx(hrow(sent)))
        self.assertEqual(code, 1, doc)
        self.assertEqual(len([f for f in found if f["kind"] == "HISTORICAL"]), 1, doc)
        self.assertIn("STALE", [f["kind"] for f in found], doc)

    def test_register_data_is_strict(self):
        # 3b75 redesign: the rows live in TOML; the structural checks refuse, fail closed.
        row = hrow()
        for data, message in [
            ("schema_version = 1\nschema_version = 1\n", "not valid TOML"),            # duplicate key
            ("schema_version = 2\n" + row, "schema_version must be the integer 1"),
            ("schema_version = true\n" + row, "schema_version must be the integer 1"),
            ("schema_version = 1\nextra = 1\n", "top-level keys must be"),
            ("exception = []\n", "top-level keys must be"),                             # no schema_version
            ("schema_version = 1\nexception = 3\n", "exception must be an array of tables"),
            (HXHEAD + row.replace("reason =", "why ="), "fields must be exactly"),
            (HXHEAD + row + 'extra = "x"\n', "fields must be exactly"),  # every key present, one extra
            (HXHEAD + row.replace('reason = "Records the edition lineage accurately."\n', ""), "fields must be exactly"),
            (HXHEAD + row.replace("path = ", "path = 3 #"), "path must be"),
            (HXHEAD + hrow(verified="2026-09-01T00:00:00"), "verified must be a TOML date"),
            (HXHEAD + hrow(verified='"2026-09-01"'), "verified must be a TOML date"),
            (HXHEAD + hrow(reason="Records the edition lin\u0435age accurately."), "single-line printable ASCII"),
            (HXHEAD + hrow(reason="Records the edition\nlineage accurately."), "single-line printable ASCII"),
            (HXHEAD + hrow(reason=" Records the edition lineage accurately."), "no leading, trailing or doubled space"),
            (HXHEAD + hrow(reason="Records the  edition lineage accurately."), "doubled space"),  # claude r5
            (HXHEAD + hrow(url="https://www.iso.org/standard/71670.html|x"), "upstream evidence URL required"),
            # An https URL that names no host is not evidence (codex r5).
            (HXHEAD + hrow(url="https://#"), "upstream evidence URL required"),
            (HXHEAD + hrow(url="https:///"), "upstream evidence URL required"),
            (HXHEAD + hrow(url="https://?"), "upstream evidence URL required"),
            (HXHEAD + hrow(url="https://localhost/x"), "upstream evidence URL required"),
            (HXHEAD + hrow(url="https://www.iso.org:99999/x"), "upstream evidence URL required"),
        ]:
            code, _, err = self.invoke(HSENT + "\n", register=HREG, exceptions=data)
            self.assertEqual(code, 1, data)
            self.assertIn(message, err, data)
            self.assertNotIn("\u0435", err)  # the error names the field, it does not echo content

    def test_register_page_is_generated_and_in_sync(self):
        import importlib, tempfile
        H = W.HCR
        s = "The earlier ISO/IEC 27001:2013 edition was withdrawn."
        data = hx(hrow(s))
        rows = H.load(data)
        good = "# Register\n\n" + H.render(rows) + "\n"
        # In sync: the sanction binds.
        code, found, _ = self.run_json("\n" + s + "\n\n", data, page=good)
        self.assertEqual((code, [f["kind"] for f in found]), (0, ["HISTORICAL"]))
        # Drift, a missing page, or missing sentinels: refused, and nothing is sanctioned.
        for page, message in [
            ("# Register\n\n" + H.render([]) + "\n", "the generated table differs"),
            (good.replace("HCE\\-001", "HCE\\-002"), "the generated table differs"),
            ("# Register\n\nno table\n", "sentinels are missing"),
            (good.replace(H.END, ""), "sentinels are missing"),
        ]:
            code, found, err = self.run_json("\n" + s + "\n\n", data, page=page)
            self.assertEqual(code, 1, page)
            self.assertIn(message, err, page)
            self.assertNotIn("HISTORICAL", [f["kind"] for f in found])
        # The page must show the generated table as its only table (3b75 redesign QA, codex, claude).
        fake = "| Exception ID | Path |\n| --- | --- |\n| HCE-999 | governance/x.md |\n"
        for page, message in [
            ("<script>\n\n" + good + "\n</script>\n", "raw HTML or a comment outside the generated block"),
            ("<script>\n" + good + "</script>\n", "must stand alone"),
            ("<details>\n\n" + good + "\n</details>\n", "raw HTML or a comment outside the generated block"),
            ("```\n\n" + good + "\n```\n", "a fence marker outside the generated block"),
            ("> ```\n> x\n\n" + good, "a fence marker outside the generated block"),   # a quoted fence (claude r3)
            ("- ~~~\n\n" + good, "a fence marker outside the generated block"),
            ("---\nException ID: HCE-999\nPath: ai/phantom.md\n---\n\n" + good, "front matter at the top of the page"),  # codex r3
            (("---\nException ID: HCE-999\n---\n\n" + good).replace("\n", "\r\n"), "LF line endings only"),  # r4
            (good.replace("# Register\n", "# Register\u2028"), "LF line endings only"),
            (good + "\n$$\n\\begin{array}{ll} HCE-001 & ai/x.md \\end{array}\n$$\n", "math markup"),  # claude r4
            (fake + "\n" + good, "a table (or a pipe) outside the generated block"),
            ("a | b\n:-- | --:\n1 | 2\n\n" + good, "a table (or a pipe) outside the generated block"),  # no outer pipes
            ("# Register\n\n- item\n\n  " + H.render(rows) + "\n", "must stand alone"),  # nested in a list item
            (good.replace(H.END + "\n", H.END + "x\n"), "must stand alone"),
            # An image can show a picture of a table (claude r5).
            ("![Exceptions](https://www.iso.org/t.png)\n\n" + good, "an image outside the generated block"),
            (good + "\n![Exceptions][t]\n\n[t]: https://www.iso.org/t.svg\n", "an image outside the generated block"),
            (" \t" + H.render(rows) + "\n", "must stand alone"),  # an indented block on line 1
        ]:
            code, found, err = self.run_json("\n" + s + "\n\n", data, page=page)
            self.assertEqual(code, 1, page)
            self.assertIn(message, err, page)
            self.assertNotIn("HISTORICAL", [f["kind"] for f in found])
        # Blank lines may hold spaces or tabs (codex r2): accepted.
        code, found, _ = self.run_json("\n" + s + "\n\n", data, page="# Register\n \t\n" + H.render(rows) + "\n  \nEnd.\n")
        self.assertEqual((code, [f["kind"] for f in found]), (0, ["HISTORICAL"]))
        # The start and end of the file are a boundary: one blank line there is enough (codex r5).
        R = H.render(rows)
        for page in ["\n" + R + "\n", " \t\n" + R + "\n", R + "\n \t", R, R + "\n"]:
            code, found, err = self.run_json("\n" + s + "\n\n", data, page=page)
            self.assertEqual((code, [f["kind"] for f in found]), (0, ["HISTORICAL"]), (page, err))
        # A list item that ends before the block leaves the block standing alone: accepted.
        code, found, _ = self.run_json("\n" + s + "\n\n", data, page="- " + good)
        self.assertEqual((code, [f["kind"] for f in found]), (0, ["HISTORICAL"]))
        # No data file: an empty generated table with a populated table beside it is refused.
        code, _, err = self.invoke("The earlier edition was withdrawn.\n", register=HREG,
                                   page=fake + "\n" + H.render([]) + "\n")
        self.assertEqual(code, 1)
        self.assertIn("a table (or a pipe) outside the generated block", err)
        # An unreadable data file is an input error (exit 2), never an absent register.
        code, _, err = self.invoke("\n" + s + "\n", register=HREG, exceptions=PermissionError("denied"),
                                   page=good)
        self.assertEqual(code, 2, err)
        # A data file with no page at all is refused.
        code, found, err = self.run_json("\n" + s + "\n\n", data, page=False)
        self.assertEqual(code, 1)
        self.assertIn("is missing; run python3 tools/build-historical-citation-exceptions.py", err)
        # No data file: a page showing rows is refused; an empty generated table passes.
        code, _, err = self.invoke("\n" + s + "\n", register=HREG, page=good)
        self.assertEqual(code, 1)
        self.assertIn("the generated table differs", err)
        code, _, err = self.invoke("The earlier edition was withdrawn.\n", register=HREG,
                                   page="# Register\n\n" + H.render([]) + "\n")
        self.assertEqual(code, 0, err)
        # Rendering escapes every punctuation character, so a cell cannot introduce markup, and the
        # rendered cells read back as the data (round trip).
        cell = "a|b<c>`d`*e*_f_[g](h)&#105;\\i"
        esc = H.escape(cell)
        self.assertNotRegex(esc, r"(?<!\\)[|<>`*_\[\]()&#]")
        self.assertEqual(re.sub(r"\\(.)", r"\1", esc), cell)
        # The build tool: --check exits 0 in sync, 1 on drift, 2 on malformed data.
        spec = importlib.util.spec_from_file_location(
            "bhce", Path(W.__file__).with_name("build-historical-citation-exceptions.py"))
        B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / ".project-governance").mkdir()
            (root / H.DATA_REL).write_text(data); (root / H.PAGE_REL).write_text(good)
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(B.main(["--check", "--root", d]), 0)
                (root / H.PAGE_REL).write_text("# Register\n\n" + H.render([]) + "\n")
                self.assertEqual(B.main(["--check", "--root", d]), 1)
                (root / H.PAGE_REL).write_text("<details>\n\n" + good.split("\n", 2)[2] + "\n</details>\n")
                self.assertEqual(B.main(["--check", "--root", d]), 1)  # a page gate 6 refuses (r4)
                (root / H.PAGE_REL).write_text("# Register\n\n" + H.render([]) + "\n")
                self.assertEqual(B.main(["--root", d]), 0)
                self.assertEqual((root / H.PAGE_REL).read_text(), good)
                # Write mode still reports a page gate 6 would refuse (claude r5).
                (root / H.PAGE_REL).write_text("a | b\n\n" + good)
                self.assertEqual(B.main(["--root", d]), 1)
                (root / H.PAGE_REL).write_text(good)
                (root / H.DATA_REL).write_text("schema_version = 2\n")
                self.assertEqual(B.main(["--check", "--root", d]), 2)
                # An unreadable data file is an input error, never "no rows" (codex, gemini r2).
                (root / H.DATA_REL).write_text(data)
                os.chmod(root / H.DATA_REL, 0)
                try:
                    if os.access(root / H.DATA_REL, os.R_OK):
                        self.skipTest("running with permission to read a mode-000 file")
                    self.assertEqual(B.main(["--check", "--root", d]), 2)
                finally:
                    os.chmod(root / H.DATA_REL, 0o600)

    def test_round_three_structural_rules(self):
        # 3b75 QA r2 (claude, codex, gemini): the sentence is the WHOLE of its line or cell.
        for doc, sent in [
            ("The earlier ISO/IEC 27001:2013 edition, e.g.\n",
             "The earlier ISO/IEC 27001:2013 edition, e.g."),
            ("See i.e.\nThe earlier ISO/IEC 27001:2013 edition was withdrawn.\n",
             "The earlier ISO/IEC 27001:2013 edition was withdrawn."),
            ("The earlier ISO/IEC 27001:2013 edition was withdrawn. It governs us today.\n",
             "The earlier ISO/IEC 27001:2013 edition was withdrawn."),
            ("Intro text\nThe earlier ISO/IEC 27001:2013 edition was withdrawn.\n",
             "The earlier ISO/IEC 27001:2013 edition was withdrawn."),
        ]:
            code, found, _ = self.run_json(doc, hx(hrow(sent)))
            self.assertEqual(code, 1, doc)
            self.assertIn("INVALID_EXCEPTION", [f["kind"] for f in found], doc)
            self.assertIn("STALE", [f["kind"] for f in found], doc)
        # 3b75 QA r3 (claude, codex): only a STANDALONE PARAGRAPH binds. A table cell (real or a
        # pipe line inside a paragraph), a list item (parent, child or sibling), a heading
        # neighbour and a sentence missing its terminator are all refused.
        s = "The earlier ISO/IEC 27001:2013 edition was withdrawn."
        for doc in [
            "| A | B |\n| --- | --- |\n| Lineage | " + s + " |\n",
            "Organizations certify against\n| " + s + " |\nwhich remains mandatory today.\n",
            "- We currently require:\n  - " + s + "\n",
            "- " + s + "\n- Another item.\n",
            "## Current requirements\n" + s + "\n",
            "> " + s + "\n",
            "    " + s + "\n",
        ]:
            assert_refused(self, doc, s)
        # A declared sentence that itself carries a list, heading or quote marker is refused.
        for marked in ("- " + s, "## " + s, "> " + s, "1. " + s):
            assert_refused(self, "\n" + marked + "\n\n", marked)
        bare = "The earlier ISO/IEC 27001:2013 edition was withdrawn"
        assert_refused(self, "\n" + bare + "\n\n", bare)
        # The accepted shape: its own paragraph, blank lines around.
        code, found, _ = self.run_json("Intro.\n\n" + s + "\n\nMore.\n", hx(hrow(s)))
        self.assertEqual(code, 0)
        self.assertEqual([f["kind"] for f in found if f["kind"] in ("HISTORICAL", "STALE")], ["HISTORICAL"])
        # The wrapper refuses a pipe in the sentence (the plain-text sentence grammar).
        piped = "The earlier ISO/IEC 27001:2013 edition | was withdrawn."
        code, _, err = self.run_json(piped + "\n", hx(hrow(piped)))
        self.assertEqual(code, 1)
        self.assertIn("sentence must be plain text", err)
        # The citation named by the row, written exactly: another written form of the same edition
        # in the sentence is not sanctioned by it.
        sent = "The earlier ISO/IEC 27001 (2013) edition was withdrawn."
        code, found, err = self.run_json(sent + "\n", hx(hrow(sent)))
        self.assertEqual(code, 1)
        self.assertIn("verbatim exactly once", err)
        both = "The earlier ISO/IEC 27001:2013 edition, also cited as ISO/IEC 27001 (2013), was withdrawn."
        code, found, _ = self.run_json(both + "\n", hx(hrow(both)), "--coverage-mode", "enforce")
        self.assertEqual(code, 1)
        self.assertEqual(len([f for f in found if f["kind"] == "HISTORICAL"]), 1)
        self.assertIn("STALE", [f["kind"] for f in found])
        # The next line continues the paragraph: refused.
        sent = "The earlier ISO/IEC 27001:2013 edition was withdrawn."
        code, found, _ = self.run_json(sent + "\nIt governs us today.\n", hx(hrow(sent)))
        self.assertEqual(code, 1)
        self.assertIn("INVALID_EXCEPTION", [f["kind"] for f in found])
        # The wrapper refuses a sentence carrying the citation twice.
        twice = "The earlier ISO/IEC 27001:2013 edition and ISO/IEC 27001:2013 were withdrawn."
        code, _, err = self.run_json(twice + "\n", hx(hrow(twice)))
        self.assertEqual(code, 1)
        self.assertIn("verbatim exactly once", err)
        # The engine alone (a wrapper that names no written citation) refuses two occurrences.
        eng = CitationCoverageTests.invoke.__globals__["W"]._engine()
        entries = CitationCoverageTests.invoke.__globals__["W"].parse_register_text(HREG)
        occ = [o for o in eng.discover("ISO/IEC 27001:2013", ".md") if o["channel"] == "grammar"][0]
        ex = dict(id="HCE-009", path="ai/c.md", sentence=twice, reason="r",
                  identity=occ["identity"], edition=eng.edition_key(occ["version"]))
        _, sanctioned, errors = eng.apply_historical_exceptions(twice + "\n", "ai/c.md", [ex], entries)
        self.assertEqual(sanctioned, [])
        self.assertIn("occurs more than once", errors[0]["detail"])
        # Anything in the data file that is not TOML data (markup, stray text) fails closed.
        for body, message in [
            ("<!-- hidden\n" + hrow(), "not valid TOML"),
            (hrow() + "Some text.\n", "not valid TOML"),
        ]:
            code, _, err = self.invoke(HSENT + "\n", register=HREG, exceptions=HXHEAD + body)
            self.assertEqual(code, 1, body)
            self.assertIn(message, err, body)

    def test_round_five_containers_and_parsing(self):
        s = "The earlier ISO/IEC 27001:2013 edition was withdrawn."
        # 3b75 QA r4 (codex): a code span in the sentence could, once masked, expose a fence that
        # hides a later citation; it is refused, and the later citation still blocks.
        fence = "ISO/IEC 27001:2013 ```was the previous edition```."
        assert_refused(self, "\n" + fence + "\n\nPCI DSS 4.0 governs certification.\n", fence)
        # Legacy-check line eligibility comes from the original text, not the masked one.
        eng = CitationCoverageTests.invoke.__globals__["W"]._engine()
        compiled = [(None, re.compile(r"PCI DSS 4\.0"), "PCI")]
        masked = "            ```was```.\nPCI DSS 4.0 x\n"
        original = "ISO/IEC 27001:2013 ```was```.\nPCI DSS 4.0 x\n"
        self.assertEqual(eng.check_text(masked, compiled, eligible_from=original), [(2, "PCI")])
        # 3b75 QA r4 (codex): a no-break-space line is not a Markdown blank line.
        code, found, _ = self.run_json("Our programme relies on\n\u00a0\n" + s + "\n\u00a0\n", hx(hrow(s)))
        self.assertEqual(code, 1)
        self.assertIn("INVALID_EXCEPTION", [f["kind"] for f in found])
        # 3b75 QA r4 (codex): a raw-HTML quotation around the paragraph.
        code, found, _ = self.run_json("<blockquote>\n\n" + s + "\n\n</blockquote>\n", hx(hrow(s)))
        self.assertEqual(code, 1)
        self.assertIn("INVALID_EXCEPTION", [f["kind"] for f in found])
        # 3b75 QA r4 (claude): a sentence present only inside a fenced block is not found.
        code, found, _ = self.run_json("```\n" + s + "\n```\n", hx(hrow(s)))
        self.assertEqual(code, 1)
        self.assertTrue(any("declared sentence not found" in f["detail"] for f in found))
        # A citation cell carrying more than the one registered edition (codex r4).
        for register, message in [
            (hx(hrow(s, citation="ISO/IEC 27001:2013 extra")), "is not exactly one registered superseded edition"),
        ]:
            code, _, err = self.invoke("\n" + s + "\n", register=HREG, exceptions=register)
            self.assertEqual(code, 1, register)
            self.assertIn(message, err, register)

    def test_round_nine_guards(self):
        s = "The earlier ISO/IEC 27001:2013 edition was withdrawn."
        # 3b75 QA r8 (claude): the absolute-path guard.
        code, _, err = self.run_json("\n" + s + "\n\n", hx(hrow(s, path="/ai/citation.md")))
        self.assertEqual(code, 1)
        self.assertIn("path must be a canonical repo .md path", err)
        # 3b75 QA r8 (claude): a fence line carrying text after its run does not close the block.
        self.assertIn("HCE-001: the document's fenced blocks are not all simple three-character fences",
                      assert_refused(self, "```\nx\n```y\n\n" + s + "\n\n", s))

    def test_round_eight_lookalikes_and_rows(self):
        s = "The earlier ISO/IEC 27001:2013 edition was withdrawn."
        # 3b75 QA r7 (claude): a non-ASCII lookalike letter hides a present-tense verb from the
        # word screen and from the reviewer; the data file refuses non-ASCII text, and the engine
        # alone refuses the sentence too.
        for sent in ("The previously adopted ISO/IEC 27001:2013 r\u0435quires annual audits.",
                     "The earlier ISO/IEC 27001:2013 edition \u0433overns audits."):
            code, _, err = self.run_json("\n" + sent + "\n\n", hx(hrow(sent)))
            self.assertEqual(code, 1, sent)
            self.assertIn("single-line printable ASCII", err, sent)
            assert_refused(self, "\n" + sent + "\n\n", sent)
        # 3b75 QA r7 (claude): further present-tense verbs.
        for sent in ("The control set, previously agreed, conforms to ISO/IEC 27001:2013.",
                     "Our certification continues under ISO/IEC 27001:2013 as previously scoped."):
            code, _, err = self.run_json("\n" + sent + "\n\n", hx(hrow(sent)))
            self.assertEqual(code, 1, sent)
            self.assertIn("present-tense wording", err, sent)
        # 3b75 QA r7 (claude): two rows cannot sanction the one occurrence.
        code, _, err = self.run_json("\n" + s + "\n\n", hx(hrow(s), hrow(s, xid="HCE-002")))
        self.assertEqual(code, 1)
        self.assertIn("repeats another row's path, sentence and citation", err)
        # A valid row binds.
        code, found, _ = self.run_json("\n" + s + "\n\n", hx(hrow(s)))
        self.assertEqual((code, [f["kind"] for f in found]), (0, ["HISTORICAL"]))

    def test_round_seven_markup_and_line_model(self):
        s = "The earlier ISO/IEC 27001:2013 edition was withdrawn."
        tbl = "<table><tr><th>Current baseline</th></tr><tr><td>"
        # 3b75 QA r6 (claude, codex, gemini): comment markers a regex pairs but a renderer does not
        # (in a code span, in a fence, escaped, or the complete `<!-->` comment) hid real HTML.
        for doc in (
            "Write `<!--` to open.\n\n" + tbl + "\n\n" + s + "\n\n</td></tr></table>\n\nWrite `-->` to close.\n",
            "```\n<!--\n```\n\n" + tbl + "\n\n" + s + "\n\n</td></tr></table>\n\n```\n-->\n```\n",
            "<!-->\n" + tbl + "\n-->\n\n" + s + "\n\n<!-- </td></tr></table> -->\n",
            "\\<!--\n\n<blockquote>\n\n" + s + "\n\n</blockquote>\n\n-->\n",
            "<!--\n\n" + s + "\n\n",  # an unclosed comment in the citing document (claude r6)
        ):
            self.assertIn("HCE-001: the document carries raw HTML or an HTML comment",
                          assert_refused(self, doc, s))
        # A lone CR in the file's bytes, which a universal-newline read turns into LF (codex r6).
        self.assertIn("HCE-001: the document uses line separators other than LF or CRLF",
                      assert_refused(self, ("\n" + s + "\r\rIt governs certification today.\n").encode(), s))
        # CRLF is an ordinary line ending, so a CRLF document still binds.
        code, found, _ = self.run_json(("Intro.\r\n\r\n" + s + "\r\n\r\nMore.\r\n").encode(), hx(hrow(s)))
        self.assertEqual((code, [f["kind"] for f in found]), (0, ["HISTORICAL"]))
        # A fence the line model toggles differently from a renderer (claude r6): a 4-backtick
        # fence around a 3-backtick line, an indented fence, mixed fence characters, an open fence.
        for doc in (
            "````\n```\n\n" + s + "\n\n```\n````\n",
            "  ```\ncode\n  ```\n\n" + s + "\n\n",
            "```\n~~~\n\n" + s + "\n\n",  # a tilde line does not close a backtick fence
            "~~~~\n~~~\n\n" + s + "\n\n",  # nor does a shorter run close a longer one
            "    ~~~\n~~~\n\n" + s + "\n\n",  # a 4-space line is indented code, not a fence
            "\n" + s + "\n\n```\nnever closed\n",
            "```a`b\ncode\n```\n\n" + s + "\n\n",
        ):
            fences = doc
            self.assertIn("HCE-001: the document's fenced blocks are not all simple three-character fences",
                          assert_refused(self, doc, s), repr(fences))
        # Plain fences elsewhere in the document do not stop a sanction.
        code, found, _ = self.run_json("```text\ncode\n```\n\n" + s + "\n\n~~~\nmore\n~~~\n", hx(hrow(s)))
        self.assertEqual((code, [f["kind"] for f in found]), (0, ["HISTORICAL"]))
        # The sentence is plain text: a character reference hides a break or a present-tense word, a
        # tilde run or emphasis can change what renders (codex r6, claude r6).
        for sent in (
            "The earlier ISO/IEC 27001:2013 edition was withdrawn.&#32;The replacement followed.",
            "The previous edition ISO/IEC 27001:2013 r&#101;quires certification.",
            "ISO/IEC 27001:2013 ~~~ was the earlier edition.",
            "The earlier ISO/IEC 27001:2013 edition was *withdrawn*.",
            "The earlier ISO/IEC 27001:2013 edition was withdrawn\\.",
        ):
            code, _, err = self.run_json("\n" + sent + "\n\n", hx(hrow(sent)))
            self.assertEqual(code, 1, sent)
            self.assertIn("sentence must be plain text", err, sent)
            assert_refused(self, "\n" + sent + "\n\n", sent)
        # The data file: separators other than LF or CRLF, and Markdown or HTML around the data,
        # are not TOML and fail closed (codex r6, claude r6; the redesign removes the page parser).
        for sep in ("\u2028", "\x0b", "\x85", "\r"):
            body = (HXHEAD + hrow(s)).replace("\n", sep).encode("utf-8")
            code, found, err = self.invoke("\n" + s + "\n", register=HREG, exceptions=body)
            self.assertEqual(code, 1, repr(sep))
            self.assertIn("ERROR: historical register data", err, repr(sep))
        code, _, err = self.invoke("\n" + s + "\n", register=HREG, exceptions=(
            "Write `<!--` to comment a row out.\n<details>\nWrite `-->` to close it.\n" + hx(hrow(s))))
        self.assertEqual(code, 1)
        self.assertIn("not valid TOML", err)

    def test_round_six_line_model_and_html(self):
        s = "The earlier ISO/IEC 27001:2013 edition was withdrawn."
        # 3b75 QA r5 (claude, codex): with NO exceptions, a U+2028 earlier in the file must not
        # shift which line the legacy check reads; the stale citation keeps blocking.
        doc = "Intro\u2028more\n\n```\ncode\n```\nISO/IEC 27001:2013\n"
        code, out, _ = self.invoke(doc, register=HREG)
        self.assertEqual(code, 1)
        self.assertIn("BLOCKING legacy \"stale citation 'ISO/IEC 27001 2013'", out)
        # A non-LF line separator after the sentence (the renderer continues the paragraph).
        for sep in ("\u2028", "\x0c", "\r"):
            assert_refused(self, "Intro.\n\n" + s + sep + "\nIt governs certification today.\n", s, msg=repr(sep))
        # Raw HTML anywhere in the document: deny by default (any container, attribute tricks).
        for wrap in ("<script>\n\n{}\n\n</script>\n", "<article>\n\n{}\n\n</article>\n",
                     '<blockquote title="</blockquote>">\n\n{}\n\n</blockquote>\n', "Text <br> here.\n\n{}\n"):
            code, found, _ = self.run_json(wrap.format(s), hx(hrow(s)))
            self.assertEqual(code, 1, wrap)
            self.assertTrue(any("raw HTML" in f["detail"] for f in found), wrap)
        # Inline HTML in the sentence itself.
        inl = "The earlier ISO/IEC 27001:2013 <em>edition</em> was withdrawn."
        code, found, _ = self.run_json("\n" + inl + "\n\n", hx(hrow(inl)))
        self.assertEqual(code, 1)
        # Curly quotes do not hide a sentence break (codex r5).
        curly = "He wrote \u201cThe earlier ISO/IEC 27001:2013 edition was withdrawn.\u201d The replacement followed."
        assert_refused(self, "\n" + curly + "\n\n", curly)
        # HTML around the data is not TOML and fails closed (codex r5).
        code, _, err = self.invoke("\n" + s + "\n", register=HREG,
                                   exceptions="Policy <script type=\"text/plain\">\n" + hx(hrow(s)) + "End </script>\n")
        self.assertEqual(code, 1)
        self.assertIn("not valid TOML", err)

    def test_wrapper_screens_and_schema(self):
        for sent, cit, reason, verified, message in [
            ("We use the previous edition ISO/IEC 27001:2013 for certification.",
             "ISO/IEC 27001:2013", None, "2026-09-01", "present-tense wording 'use'"),
            (HSENT, "ISO/IEC 27001:2013", "short", "2026-09-01", "reason required"),
            (HSENT, "ISO/IEC 27001:2013", None, '"2026-09-01"', "verified must be a TOML date"),
            (HSENT, "ISO/IEC 27001:2013", None, "2026-09-01T00:00:00", "verified must be a TOML date"),
        ]:
            row = hrow(sent, cit, verified=verified)
            if reason:
                row = row.replace("Records the edition lineage accurately.", reason)
            code, _, err = self.invoke(sent + "\n", register=HREG, exceptions=hx(row))
            self.assertEqual(code, 1, message)
            self.assertIn(message, err, message)


if __name__ == "__main__":
    unittest.main()
