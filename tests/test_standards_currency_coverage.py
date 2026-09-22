"""PR1 behavior fixtures: stdlib only; synthetic inputs stay in memory."""
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
        for name in ("read_text", "exists", "is_file", "is_dir")
    }
    old_scandir = os.scandir

    def inside(p):
        return p == root or root in p.parents

    def read(p, *args, **kwargs):
        if not inside(p):
            return original["read_text"](p, *args, **kwargs)
        if p not in files:
            raise FileNotFoundError(str(p))
        if isinstance(files[p], Exception):
            raise files[p]
        return files[p]

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
        self, text, *args, suffix=".md", register=REGISTER
    ):
        relative = (
            "ai/citation.md" if suffix == ".md"
            else ".web/templates/landing.html"
        )
        values = {
            "governance/register-canonical-citations.md": register,
            relative: text,
        }
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


if __name__ == "__main__":
    unittest.main()
