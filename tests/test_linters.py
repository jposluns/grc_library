#!/usr/bin/env python3
"""Linter regression tests.

For each in-scope linter, this module constructs a minimal synthetic
markdown fixture that should trigger exactly one rule, invokes the
linter against the fixture, and asserts the linter exits non-zero.

The tests catch a class of defect that no other gate in the audit
programme catches: a regression in the linter's own detection logic.
If a refactor weakens a regex or breaks an exemption list, the corpus
may still happen to be clean (no false positives), but the linter no
longer detects the violation class it exists to detect. A failing
positive test produces an unambiguous signal that the linter itself
is broken.

Scope is now complete: every linter in the audit programme has at
least one positive test in this module. Several linters additionally
have negative tests (fixture that should NOT be flagged) and
environmental tests (exit code 2 when a required register is
absent); see ``tests/README.md`` for the full coverage policy.
Infrastructure-coupled linters that earlier docstrings listed as out
of scope (orphan, citation-verification freshness, tooling-provenance
freshness, library-version monotonicity, gate-name parity,
structural-index, CHANGELOG link-coverage, review-cadence) all have
dedicated test classes; see the class enumeration at the bottom of
this file.

Stdlib-only Python 3.11 (unittest, tempfile, subprocess).
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = REPO_ROOT / "tests" / "tmp"


# Minimal metadata block that satisfies lint-metadata.py's required-fields
# check. Fixtures that need to pass metadata while triggering some other
# linter's rule can prepend this block.
VALID_METADATA = """# Test Document

**Document Title:** Test Document\\
**Document Type:** Standard\\
**Version:** 1.0.0\\
**Date:** 2026-05-31\\
**Owner:** Governance Library Maintainer\\
**Approving Authority:** Governance Library Maintainer\\
**Related Documents:** [`README.md`](../README.md)\\
**Classification:** Public\\
**Category:** Test\\
**Review Frequency:** Annual\\
**Repository Path:** [`tests/tmp/standard-test.md`](standard-test.md)\\
**Confidentiality:** Public\\
**License:** CC BY-SA 4.0

---

## Purpose

Test fixture content for the linter regression suite.

---

**End of Document**
"""


def setUpModule() -> None:
    """Ensure the per-test fixture directory exists and is empty.

    Run once before any test in this module. Removes any leftover
    fixtures from a previously-crashed run so they cannot contaminate
    the current test pass.
    """
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    for f in FIXTURE_DIR.glob("*.md"):
        try:
            f.unlink()
        except OSError:
            pass


def tearDownModule() -> None:
    """Belt-and-suspenders: remove any remaining fixtures after the run.

    Individual tearDown methods already remove their fixtures; this
    catches anything left behind by a crashed assertion.
    """
    for f in FIXTURE_DIR.glob("*.md"):
        try:
            f.unlink()
        except OSError:
            pass


def run_linter(script: str, *paths: str | Path) -> subprocess.CompletedProcess:
    """Invoke a linter as a subprocess and return the completed-process record.

    ``script`` is the linter script's repo-relative path (e.g.
    ``tools/lint-metadata.py``). ``paths`` are arguments passed
    positionally to the linter (typically a fixture path).

    Uses Python 3 from the current interpreter so the test inherits the
    same Python environment.
    """
    cmd = [sys.executable, str(REPO_ROOT / script), *map(str, paths)]
    return subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )


class LinterTestCase(unittest.TestCase):
    """Base class providing fixture-file helpers."""

    fixture_paths: list[Path] = []

    def make_fixture(self, name: str, content: str) -> Path:
        """Write ``content`` to ``tests/tmp/<name>`` and remember to clean up."""
        path = FIXTURE_DIR / name
        path.write_text(content, encoding="utf-8")
        self.fixture_paths.append(path)
        return path

    def tearDown(self) -> None:
        for p in list(self.fixture_paths):
            try:
                p.unlink()
            except OSError:
                pass
            self.fixture_paths.remove(p)

    def assertLinterFails(
        self,
        result: subprocess.CompletedProcess,
        expected_in_output: str | None = None,
    ) -> None:
        """Assert the linter exited non-zero. Optionally match an output substring."""
        if result.returncode == 0:
            self.fail(
                f"linter exited 0 but should have failed.\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        if expected_in_output is not None:
            combined = result.stdout + "\n" + result.stderr
            if expected_in_output not in combined:
                self.fail(
                    f"expected {expected_in_output!r} in linter output but did not find it.\n"
                    f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
                )


class MetadataLinterTests(LinterTestCase):
    """tools/lint-metadata.py"""

    def test_missing_metadata_block_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-no-metadata.md",
            "# A Document\n\nNo metadata at all.\n",
        )
        result = run_linter("tools/lint-metadata.py", fixture)
        self.assertLinterFails(result)

    def test_filename_doctype_prefix_mismatch_flagged(self) -> None:
        bad = VALID_METADATA.replace(
            "tests/tmp/standard-test.md", "tests/tmp/policy-mismatch.md"
        )
        fixture = self.make_fixture("policy-mismatch.md", bad)
        result = run_linter("tools/lint-metadata.py", fixture)
        self.assertLinterFails(result, "filename prefix does not match")

    def test_invalid_version_format_flagged(self) -> None:
        bad = VALID_METADATA.replace("**Version:** 1.0.0", "**Version:** 1.0")
        fixture = self.make_fixture("standard-bad-version.md", bad)
        result = run_linter("tools/lint-metadata.py", fixture)
        self.assertLinterFails(result, "Version")

    def test_invalid_doctype_flagged(self) -> None:
        bad = VALID_METADATA.replace(
            "**Document Type:** Standard",
            "**Document Type:** Fictional",
        )
        fixture = self.make_fixture("standard-bad-doctype.md", bad)
        result = run_linter("tools/lint-metadata.py", fixture)
        self.assertLinterFails(result)


class LanguageLinterTests(LinterTestCase):
    """tools/lint-language.py"""

    def test_em_dash_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-em-dash.md",
            VALID_METADATA + "\n\nThe quick brown fox — jumped over the lazy dog.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertLinterFails(result, "dash")

    def test_ise_americanism_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-ise.md",
            VALID_METADATA + "\n\nThis text was finalised by the team.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertLinterFails(result, "ise")

    def test_ise_third_person_inflection_flagged(self) -> None:
        # Regression for the #480 /validate-pr finding: the third-person
        # singular `-ises` inflection (e.g. "recognises") must be flagged.
        # Before the ISE_PATTERN widening it listed only -ise / -ised / -ising
        # and let the -ises form through.
        fixture = self.make_fixture(
            "standard-ises.md",
            VALID_METADATA + "\n\nThe procedure recognises three modes.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertLinterFails(result, "ise")

    def test_isation_noun_flagged(self) -> None:
        # The 2026-07-02 spelling-coverage extension: Commonwealth -isation
        # noun and adjective forms are flagged (the harmonization sweep
        # flipped the corpus to -ization in the same PR).
        fixture = self.make_fixture(
            "standard-isation.md",
            VALID_METADATA + "\n\nThe organization reviews authorisation and organizational controls.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertLinterFails(result, "isation")

    def test_isation_allowed_word_passes(self) -> None:
        # Words that are -isation in every dialect (ISATION_ALLOWED_WORDS)
        # are not flagged.
        fixture = self.make_fixture(
            "standard-improvisation.md",
            VALID_METADATA + "\n\nThe exercise rewards improvisation under pressure.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertEqual(result.returncode, 0, f"linter should pass.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")

    def test_yse_verb_flagged_analyses_passes(self) -> None:
        # The -yse family: 'analysed' is flagged; the noun plural 'analyses'
        # (correct in every dialect) is deliberately not matched.
        flagged = self.make_fixture(
            "standard-yse.md",
            VALID_METADATA + "\n\nThe team analysed the results.\n",
        )
        result = run_linter("tools/lint-language.py", flagged)
        self.assertLinterFails(result, "yse")
        passing = self.make_fixture(
            "standard-analyses.md",
            VALID_METADATA + "\n\nThe risk analyses are reviewed annually.\n",
        )
        result = run_linter("tools/lint-language.py", passing)
        self.assertEqual(result.returncode, 0, f"linter should pass.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")

    def test_derivational_ise_forms_flagged(self) -> None:
        # The -isable adjective and -iser agent-noun derivations of covered
        # stems are flagged (the FN-verifier catch on the harmonization
        # sweep: localisable, customisable, sanitiser, analyser escaped the
        # inflection-only pattern).
        fixture = self.make_fixture(
            "standard-isable.md",
            VALID_METADATA + "\n\nStrings are localisable; run the sanitiser and the analyser.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertLinterFails(result, "ise")

    def test_prefixed_ise_derivative_flagged(self) -> None:
        # Prefixed derivatives are enumerated as their own stems; the bare
        # \b(...)  construction does not match a stem inside a prefixed word.
        fixture = self.make_fixture(
            "standard-unauthorised.md",
            VALID_METADATA + "\n\nBlock unauthorised access attempts.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertLinterFails(result, "ise")

    def test_allowed_commonwealth_span_masked(self) -> None:
        # A verbatim external-instrument quote in ALLOWED_COMMONWEALTH_SPANS
        # is masked out of the spelling checks (the GDPR Article 25(1)
        # official English text spells 'organisational').
        fixture = self.make_fixture(
            "standard-verbatim-quote.md",
            VALID_METADATA + "\n\nThe controller must \"implement appropriate technical and "
            "organisational measures, such as pseudonymisation, which are designed to "
            "implement data-protection principles, such as data minimisation, in an "
            "effective manner\" per Article 25(1).\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertEqual(result.returncode, 0, f"linter should pass.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")

    def test_bare_ensure_flagged(self) -> None:
        # The 'ensure' rule requires 'that' after 'ensure'/'ensures'.
        fixture = self.make_fixture(
            "standard-bare-ensure.md",
            VALID_METADATA + "\n\nThe team must ensure compliance.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertLinterFails(result, "ensure")

    def test_verbatim_ensure_title_exempt(self) -> None:
        # The 2026-07-02 verbatim-external-title exemption: the canonical
        # COBIT 2019 MEA01.05 practice title carries a bare imperative
        # "Ensure" and is masked (VERBATIM_ENSURE_TITLES), while a bare
        # "ensure" elsewhere on the same line still fails.
        fixture = self.make_fixture(
            "standard-verbatim-ensure.md",
            VALID_METADATA + "\n\nThe row cites MEA01.05 Ensure the "
            "implementation of corrective actions as its COBIT practice.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertEqual(result.returncode, 0, f"linter should pass.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")

    def test_verbatim_ensure_title_does_not_shadow_bare_ensure(self) -> None:
        # A line carrying BOTH the masked verbatim title and a separate bare
        # "ensure" must still fail: the mask is span-scoped, not line-scoped.
        fixture = self.make_fixture(
            "standard-verbatim-ensure-plus-bare.md",
            VALID_METADATA + "\n\nTeams ensure alignment with MEA01.05 Ensure "
            "the implementation of corrective actions across audits.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertLinterFails(result, "ensure")

    def test_en_dash_flagged(self) -> None:
        # En dash is also disallowed by the same rule as em dash.
        fixture = self.make_fixture(
            "standard-en-dash.md",
            VALID_METADATA + "\n\nThe range 2024–2026 has en-dash punctuation.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertLinterFails(result, "dash")

    def test_sanitisation_term_flagged(self) -> None:
        # SANITISATION_TERMS catches specific company/product names that
        # should never appear in organization-neutral library content. The
        # first term in the list is "Traffic Tech" — using it triggers
        # the rule.
        fixture = self.make_fixture(
            "standard-sanitisation.md",
            VALID_METADATA + "\n\nThe vendor Traffic Tech provided the platform.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertLinterFails(result, "sanitisation")

    def test_generator_emitted_prose_ise_flagged(self) -> None:
        # Gate 2 also scans the build-*.py generators' emitted-prose string
        # literals (Sweep 78 B-1, the low-severity cleanup batch): the generated docs/ output is
        # excluded from the .md scan and the .py source is never scanned as
        # markdown, so a Commonwealth -ise spelling in a generator's emitted
        # prose (not a docstring) was doubly blind. It must now be flagged.
        fixture = self.make_fixture(
            "build-gen-ise.py",
            '"""Module docstring: finalised (docstring, must be ignored)."""\n'
            "out = []\n"
            'out.append("This audience blurb was finalised by the team.")\n',
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertLinterFails(result, "ise")

    def test_generator_docstring_prose_not_flagged(self) -> None:
        # Docstrings in a generator are developer documentation, not prose
        # emitted into the corpus, so a Commonwealth -ise spelling inside a
        # module or function docstring must NOT be flagged; only non-docstring
        # string literals are scanned. The one emitted string reads cleanly,
        # so the file must scan clean.
        fixture = self.make_fixture(
            "build-gen-docstring-ok.py",
            '"""Generator docstring describing how output is finalised."""\n'
            "def build():\n"
            '    """Build docstring: recognised behaviour."""\n'
            "    out = []\n"
            '    out.append("This audience blurb reads cleanly.")\n'
            "    return out\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        if result.returncode != 0:
            self.fail(
                "generator docstring -ise should be exempt (docstrings are not "
                "emitted prose) but lint-language failed.\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )

    def test_worked_example_meta_tutorial_exempt(self) -> None:
        # docs/worked-example.md is the meta-tutorial that demonstrates the
        # document-creation process, so it deliberately contains lowercase
        # tutorial step headings, vendor names it shows being sanitised, and
        # the word "ensure" while teaching the ensure-that rule. The
        # is_worked_example carve-out exempts it from the heading-case,
        # sanitisation, and ensure checks; it must scan clean.
        result = run_linter("tools/lint-language.py", "docs/worked-example.md")
        if result.returncode != 0:
            self.fail(
                "docs/worked-example.md should be exempt (heading-case / "
                "sanitisation / ensure) and scan clean, but lint-language "
                f"failed.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )

    def test_generated_docs_excluded_from_scan(self) -> None:
        # The two generated artefacts under docs/ (portal.md,
        # maturity-scorecard.md) are build output and must not be scanned as
        # authored prose; iter_markdown_files filters them via GENERATED_DOCS.
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "lint_language_mod", REPO_ROOT / "tools" / "lint-language.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        scanned = {
            p.relative_to(REPO_ROOT).as_posix()
            for p in mod.iter_markdown_files(["docs"])
        }
        self.assertNotIn("docs/portal.md", scanned)
        self.assertNotIn("docs/maturity-scorecard.md", scanned)
        # Sanity: an authored docs file IS in scope.
        self.assertIn("docs/worked-example.md", scanned)


class LinksLinterTests(LinterTestCase):
    """tools/lint-links.py"""

    def test_broken_relative_link_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-broken-link.md",
            VALID_METADATA + "\n\nSee [broken](this-file-does-not-exist.md) for details.\n",
        )
        result = run_linter("tools/lint-links.py", fixture)
        self.assertLinterFails(result, "target does not exist")


class CitationsLinterTests(LinterTestCase):
    """tools/lint-citations.py"""

    def test_cobit_2025_hallucination_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-cobit-2025.md",
            VALID_METADATA + "\n\nThis standard aligns with COBIT 2025.\n",
        )
        result = run_linter("tools/lint-citations.py", "--paths", str(fixture))
        self.assertLinterFails(result, "COBIT 2025")

    def test_csa_ccm_v5_hallucination_flagged(self) -> None:
        # CSA CCM v5 is in the denylist; the current version is v4.1.
        fixture = self.make_fixture(
            "standard-ccm-v5.md",
            VALID_METADATA + "\n\nMaps to CSA CCM v5 controls.\n",
        )
        result = run_linter("tools/lint-citations.py", "--paths", str(fixture))
        self.assertLinterFails(result, "CCM v5")

    def test_spelled_out_cloud_controls_matrix_v5_flagged(self) -> None:
        # The spelled-out "Cloud Controls Matrix v5" form evades the
        # abbreviated "CCM v5" entry (no "CCM" substring); it needs its
        # own denylist entry. Sweep 30 surfaced five corpus instances of
        # this form that the abbreviated entry had never caught.
        fixture = self.make_fixture(
            "standard-cloud-controls-matrix-v5.md",
            VALID_METADATA + "\n\nAligned with the CSA Cloud Controls Matrix v5 baseline.\n",
        )
        result = run_linter("tools/lint-citations.py", "--paths", str(fixture))
        self.assertLinterFails(result, "Cloud Controls Matrix v5")

    def test_nist_ai_rmf_11_hallucination_flagged(self) -> None:
        # NIST AI RMF 1.1 is a hallucinated version; AI RMF was
        # published as 1.0 with AI 600-1 as the GenAI profile.
        fixture = self.make_fixture(
            "standard-ai-rmf-11.md",
            VALID_METADATA + "\n\nAligned with NIST AI RMF 1.1 guidance.\n",
        )
        result = run_linter("tools/lint-citations.py", "--paths", str(fixture))
        self.assertLinterFails(result, "AI RMF 1.1")

    def test_draft_iso_37301_hallucination_flagged(self) -> None:
        # "Draft 2026 ISO 37301" is a speculative reference; no such
        # revision is published.
        fixture = self.make_fixture(
            "standard-iso-37301-draft.md",
            VALID_METADATA + "\n\nAligns with Draft 2026 ISO 37301 expected updates.\n",
        )
        result = run_linter("tools/lint-citations.py", "--paths", str(fixture))
        self.assertLinterFails(result, "Draft 2026 ISO 37301")


class StandardsCurrencyTests(LinterTestCase):
    """tools/lint-standards-currency.py

    Uses ISO/IEC 27001:2013 as the trigger: the canonical-citations
    register records 2013 as superseded by 2022.
    """

    def test_superseded_iso_27001_2013_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-iso-superseded.md",
            VALID_METADATA + "\n\nThe organization is aligned with ISO/IEC 27001:2013.\n",
        )
        result = run_linter("tools/lint-standards-currency.py", "--paths", str(fixture))
        self.assertLinterFails(result, "2013")

    def test_root_override_with_missing_register_exits_2(self) -> None:
        # Phase 23.64: --root override + missing canonical-citations register → exit 2.
        synthetic_root = FIXTURE_DIR / "synthetic-root-no-register-citations"
        synthetic_root.mkdir(parents=True, exist_ok=True)
        try:
            result = run_linter(
                "tools/lint-standards-currency.py",
                "--root",
                str(synthetic_root),
            )
            self.assertEqual(
                result.returncode,
                2,
                f"linter should exit 2 when --root names a directory "
                f"without governance/register-canonical-citations.md.\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            import shutil
            shutil.rmtree(synthetic_root, ignore_errors=True)


class FilenameTitleTests(LinterTestCase):
    """tools/lint-filename-title-alignment.py"""

    def test_zero_overlap_flagged(self) -> None:
        bad = VALID_METADATA.replace(
            "Test Document",
            "Banana Pineapple Avocado",
        )
        fixture = self.make_fixture("standard-zucchini-celery-rhubarb.md", bad)
        result = run_linter("tools/lint-filename-title-alignment.py", "--paths", str(fixture))
        self.assertLinterFails(result)


class RolesLinterTests(LinterTestCase):
    """tools/lint-roles.py"""

    def test_undefined_role_flagged(self) -> None:
        bad = VALID_METADATA.replace(
            "**Owner:** Governance Library Maintainer",
            "**Owner:** Imaginary Synthetic Role That Does Not Exist",
        )
        fixture = self.make_fixture("standard-bad-role.md", bad)
        result = run_linter("tools/lint-roles.py", fixture)
        self.assertLinterFails(result)

    def test_root_override_with_missing_register_exits_2(self) -> None:
        # Phase 23.64: --root override lets the linter be pointed at a
        # synthetic minimal repository. If --root names a directory
        # that has no role-authority register at the expected
        # governance/ path, the file-missing path must exit 2.
        # Verifies the --root flag is parsed AND used to reconstruct
        # the register path (a regression where --root is silently
        # ignored would let the linter find the real register and
        # exit 0, failing this test).
        synthetic_root = FIXTURE_DIR / "synthetic-root-no-register-roles"
        synthetic_root.mkdir(parents=True, exist_ok=True)
        try:
            result = run_linter(
                "tools/lint-roles.py",
                "--root",
                str(synthetic_root),
            )
            self.assertEqual(
                result.returncode,
                2,
                f"linter should exit 2 when --root points at a directory "
                f"without governance/register-role-authority.md.\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            import shutil
            shutil.rmtree(synthetic_root, ignore_errors=True)


class ShallNearUncertaintyTests(LinterTestCase):
    """tools/lint-shall-near-uncertainty.py"""

    def test_shall_near_unverified_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-shall-unverified.md",
            VALID_METADATA + "\n\n[Unverified] The organization shall implement controls.\n",
        )
        result = run_linter("tools/lint-shall-near-uncertainty.py", fixture)
        self.assertLinterFails(result)

    def test_must_near_tbd_flagged(self) -> None:
        # Different mandatory ('must') and different uncertainty ('TBD')
        # markers exercise a different code path through the rule set.
        fixture = self.make_fixture(
            "standard-must-tbd.md",
            VALID_METADATA + "\n\nTBD: define the threshold; the organization must enforce it.\n",
        )
        result = run_linter("tools/lint-shall-near-uncertainty.py", fixture)
        self.assertLinterFails(result)

    def test_is_required_near_fixme_flagged(self) -> None:
        # 'is required' is one of the multi-word mandatory phrases the
        # linter detects (alongside shall, must, will be required, are
        # required). Pair with FIXME uncertainty for a third combo.
        fixture = self.make_fixture(
            "standard-is-required-fixme.md",
            VALID_METADATA + "\n\nFIXME: align with NIST guidance; encryption is required for all data at rest.\n",
        )
        result = run_linter("tools/lint-shall-near-uncertainty.py", fixture)
        self.assertLinterFails(result)


class PlaceholderLeakageTests(LinterTestCase):
    """tools/lint-placeholder-leakage.py"""

    def test_todo_marker_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-todo.md",
            VALID_METADATA + "\n\nTODO: complete this section.\n",
        )
        result = run_linter("tools/lint-placeholder-leakage.py", fixture)
        self.assertLinterFails(result, "TODO")

    def test_fixme_marker_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-fixme.md",
            VALID_METADATA + "\n\nFIXME: this needs a real value.\n",
        )
        result = run_linter("tools/lint-placeholder-leakage.py", fixture)
        self.assertLinterFails(result, "FIXME")

    def test_angle_bracket_placeholder_flagged(self) -> None:
        # Angle-bracket-syntax placeholder distinct from word-marker
        # placeholders. Exercises a different regex branch.
        fixture = self.make_fixture(
            "standard-angle-placeholder.md",
            VALID_METADATA + "\n\nDate of effect: <YYYY-MM-DD>.\n",
        )
        result = run_linter("tools/lint-placeholder-leakage.py", fixture)
        self.assertLinterFails(result, "<YYYY-MM-DD>")

    def test_yourcompany_dot_com_placeholder_flagged_in_non_template(self) -> None:
        # Phase 23.63: template-placeholder organization domains must
        # be flagged when they appear in a non-template file. The PII
        # linter intentionally exempts them as EXAMPLE_DOMAINS (they
        # are not real PII) but the placeholder linter catches them as
        # leaked template content.
        fixture = self.make_fixture(
            "standard-leaked-yourcompany.md",
            VALID_METADATA + "\n\nContact: admin@yourcompany.com for support.\n",
        )
        result = run_linter("tools/lint-placeholder-leakage.py", fixture)
        self.assertLinterFails(result, "yourcompany.com")

    def test_your_org_dot_com_placeholder_flagged_in_non_template(self) -> None:
        fixture = self.make_fixture(
            "standard-leaked-your-org.md",
            VALID_METADATA + "\n\nReplace https://your-org.com with your real domain.\n",
        )
        result = run_linter("tools/lint-placeholder-leakage.py", fixture)
        self.assertLinterFails(result, "your-org.com")

    def test_template_placeholder_domain_allowed_in_template_file(self) -> None:
        # Defence in depth: a template- prefixed file may use the
        # placeholder domain as legitimate fill-in content. Confirms
        # the filename-prefix carve-out works for this rule too.
        body = VALID_METADATA.replace(
            "tests/tmp/standard-test.md",
            "tests/tmp/template-customer-contact.md",
        ).replace(
            "**Document Type:** Standard",
            "**Document Type:** Template",
        ) + "\n\nContact: ${OWNER_NAME}@yourcompany.com.\n"
        fixture = self.make_fixture("template-customer-contact.md", body)
        result = run_linter("tools/lint-placeholder-leakage.py", fixture)
        self.assertEqual(
            result.returncode,
            0,
            f"template- prefixed file should be allowed to carry "
            f"placeholder domains as content.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


class DateFormatTests(LinterTestCase):
    """tools/lint-date-format.py"""

    def test_non_iso_date_flagged(self) -> None:
        bad = VALID_METADATA.replace(
            "**Date:** 2026-05-31",
            "**Date:** May 31, 2026",
        )
        fixture = self.make_fixture("standard-bad-date.md", bad)
        result = run_linter("tools/lint-date-format.py", fixture)
        self.assertLinterFails(result)

    def test_impossible_calendar_date_flagged(self) -> None:
        bad = VALID_METADATA.replace(
            "**Date:** 2026-05-31",
            "**Date:** 2026-13-45",
        )
        fixture = self.make_fixture("standard-impossible-date.md", bad)
        result = run_linter("tools/lint-date-format.py", fixture)
        self.assertLinterFails(result)

    def test_placeholder_in_code_block_ignored(self) -> None:
        # Regression for Phase 23.57: a `**Date:** YYYY-MM-DD`
        # placeholder inside a fenced code block (documentation
        # showing the metadata-block format) must not be flagged in a
        # non-template file. The structurally-correct rule uses
        # iter_non_code_lines instead of a file-identity allowlist.
        body = VALID_METADATA + (
            "\n\nHere is an example of the canonical metadata block "
            "that adopters should fill in:\n\n"
            "```\n"
            "**Document Title:** ...\\\n"
            "**Date:** YYYY-MM-DD\\\n"
            "**Owner:** ...\n"
            "```\n"
        )
        fixture = self.make_fixture("standard-doc-example.md", body)
        result = run_linter("tools/lint-date-format.py", fixture)
        # The file's REAL Date is 2026-05-31 (from VALID_METADATA);
        # the code-block placeholder is ignored. Should exit 0.
        self.assertEqual(
            result.returncode,
            0,
            f"placeholder Date inside a code block must not be flagged "
            f"in a non-template file (the linter should consult only "
            f"non-code lines).\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_placeholder_in_real_metadata_flagged_in_non_template(self) -> None:
        # Negative test: a placeholder appearing as the file's real
        # Date (outside any code block) in a non-template file
        # remains a finding. Confirms the structural rule still
        # enforces the production-artefact requirement.
        bad = VALID_METADATA.replace(
            "**Date:** 2026-05-31", "**Date:** YYYY-MM-DD"
        )
        fixture = self.make_fixture("standard-bare-placeholder.md", bad)
        result = run_linter("tools/lint-date-format.py", fixture)
        self.assertLinterFails(result, "placeholder Date")

    def test_placeholder_in_real_metadata_allowed_in_template(self) -> None:
        # Defence in depth: a template-prefixed file may use the
        # placeholder as its own Date. Confirms the
        # filename-prefix carve-out is intact.
        body = VALID_METADATA.replace(
            "**Date:** 2026-05-31", "**Date:** YYYY-MM-DD"
        ).replace(
            "tests/tmp/standard-test.md",
            "tests/tmp/template-empty-record.md",
        ).replace(
            "**Document Type:** Standard",
            "**Document Type:** Template",
        )
        fixture = self.make_fixture("template-empty-record.md", body)
        result = run_linter("tools/lint-date-format.py", fixture)
        self.assertEqual(
            result.returncode,
            0,
            f"template- prefixed file should be allowed to carry "
            f"YYYY-MM-DD placeholder as real metadata.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


class LicenseConsistencyTests(LinterTestCase):
    """tools/lint-license-consistency.py"""

    def test_wrong_license_flagged(self) -> None:
        bad = VALID_METADATA.replace(
            "**License:** CC BY-SA 4.0",
            "**License:** MIT",
        )
        fixture = self.make_fixture("standard-bad-license.md", bad)
        result = run_linter("tools/lint-license-consistency.py", fixture)
        self.assertLinterFails(result)


class StubDocumentTests(LinterTestCase):
    """tools/lint-stub-documents.py"""

    # A short redirect-notice body (well under the 100-word stub threshold),
    # used by the lifecycle-marker exemption tests below.
    REDIRECT_BODY = (
        "# Superseded Test Annex\n\n"
        "**Document Title:** Superseded Test Annex\\\n"
        "**Document Type:** Annex\\\n"
        "{status_line}"
        "**Version:** 2.0.0\\\n"
        "**Date:** 2026-07-02\\\n"
        "**Owner:** Governance Library Maintainer\\\n"
        "**Approving Authority:** Governance Library Maintainer\\\n"
        "**Related Documents:** [`README.md`](../README.md)\\\n"
        "**Classification:** {classification}\\\n"
        "**Category:** Test\\\n"
        "**Review Frequency:** Not applicable: superseded document\\\n"
        "**Repository Path:** [`tests/tmp/annex-superseded.md`](annex-superseded.md)\\\n"
        "**Confidentiality:** Public\\\n"
        "**License:** CC BY-SA 4.0\n\n"
        "---\n\n"
        "## Notice\n\n"
        "Superseded; see the per-jurisdiction annexes.\n"
    )

    def test_superseded_status_redirect_not_flagged(self) -> None:
        # The lifecycle marker Status: Superseded exempts a short redirect
        # notice from the stub word-count rule (the L-j re-key; the
        # Classification field stays Public, un-overloaded).
        fixture = self.make_fixture(
            "annex-superseded.md",
            self.REDIRECT_BODY.format(
                status_line="**Status:** Superseded\\\n", classification="Public"
            ),
        )
        result = run_linter("tools/lint-stub-documents.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a Status: Superseded redirect notice must be exempt.\nstdout:\n{result.stdout}",
        )

    def test_deprecated_classification_no_longer_exempts(self) -> None:
        # The former Classification: Deprecated overload no longer carries the
        # exemption: a short document marked only that way is flagged as a
        # stub (the re-key is a migration, not an alias).
        fixture = self.make_fixture(
            "annex-deprecated-only.md",
            self.REDIRECT_BODY.format(status_line="", classification="Deprecated"),
        )
        result = run_linter("tools/lint-stub-documents.py", fixture)
        self.assertLinterFails(result, "stub")

    def test_stub_phrase_flagged(self) -> None:
        bad = (
            "# Standard Test Stub\n\n"
            "**Document Title:** Standard Test Stub\\\n"
            "**Document Type:** Standard\\\n"
            "**Version:** 0.0.1\\\n"
            "**Date:** 2026-05-31\\\n"
            "**Owner:** Governance Library Maintainer\\\n"
            "**Approving Authority:** Governance Library Maintainer\\\n"
            "**Related Documents:** [`README.md`](../README.md)\\\n"
            "**Classification:** Public\\\n"
            "**Category:** Test\\\n"
            "**Review Frequency:** Annual\\\n"
            "**Repository Path:** [`tests/tmp/standard-stub.md`](standard-stub.md)\\\n"
            "**Confidentiality:** Public\\\n"
            "**License:** CC BY-SA 4.0\n\n"
            "---\n\n"
            "## Purpose\n\n"
            "[content to be added]\n\n"
            "---\n"
        )
        fixture = self.make_fixture("standard-stub.md", bad)
        result = run_linter("tools/lint-stub-documents.py", fixture)
        self.assertLinterFails(result, "stub")


class SectionAnchorTests(LinterTestCase):
    """tools/lint-section-anchors.py"""

    def test_invalid_same_doc_anchor_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-bad-anchor.md",
            VALID_METADATA + "\n\nSee [missing](#nonexistent-section-name) for details.\n",
        )
        result = run_linter("tools/lint-section-anchors.py", fixture)
        self.assertLinterFails(result)


class IntraDocRefTests(LinterTestCase):
    """tools/lint-intra-doc-refs.py"""

    def test_nonexistent_intra_section_ref_flagged(self) -> None:
        # The linter only checks documents that contain numbered headings;
        # the fixture must have at least one `## N.` heading for the
        # reference-resolution pass to run.
        body = (
            VALID_METADATA.replace("## Purpose", "## 1. Purpose")
            + "\n\nSee section §99.99 for the missing detail.\n"
        )
        fixture = self.make_fixture("standard-bad-section-ref.md", body)
        result = run_linter("tools/lint-intra-doc-refs.py", fixture)
        self.assertLinterFails(result)

    def test_trailing_link_cross_doc_ref_not_flagged(self) -> None:
        # The r3 O-F1 seam: a section reference whose markdown link
        # follows it ("see section 9.9 in [foo](foo.md)") is a CROSS-doc
        # reference (gate 62's territory), so the intra-doc gate must not
        # resolve it against this document's own headings. Before the
        # trailing-window extension, only a PRECEDING link suppressed the
        # intra-doc check.
        body = (
            VALID_METADATA.replace("## Purpose", "## 1. Purpose")
            + "\n\nSee §9.9 in [the target](xref-target.md) for detail.\n"
        )
        fixture = self.make_fixture("standard-trailing-link-ref.md", body)
        result = run_linter("tools/lint-intra-doc-refs.py", fixture)
        self.assertEqual(
            result.returncode,
            0,
            f"trailing-link cross-doc ref should not be flagged by the "
            f"intra-doc gate.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


class CrossFileSectionRefTests(LinterTestCase):
    """tools/lint-cross-file-section-refs.py (gate 62)

    The adjacent-link class: a §N reference with a markdown link to the
    target in the same clause must name a real numbered heading OR a
    line-initial inline clause (the canonical section model's citable
    non-heading identifiers) in the resolved target.
    """

    TARGET_BODY = (
        VALID_METADATA.replace("## Purpose", "## 1. Purpose")
        + "\n\n## 2. Scope\n\n2.1 The requirement statement this fixture makes citable.\n"
    )

    def test_stale_cross_file_ref_flagged(self) -> None:
        self.make_fixture("standard-xref-target.md", self.TARGET_BODY)
        citer = (
            VALID_METADATA
            + "\n\nSee [the target](standard-xref-target.md) §9.9 for the missing detail.\n"
        )
        fixture = self.make_fixture("standard-xref-citer.md", citer)
        result = run_linter("tools/lint-cross-file-section-refs.py", fixture)
        self.assertLinterFails(result, "9.9")

    def test_resolving_heading_and_inline_clause_refs_pass(self) -> None:
        self.make_fixture("standard-xref-target.md", self.TARGET_BODY)
        citer = (
            VALID_METADATA
            + "\n\nSee [the target](standard-xref-target.md) §2 for scope and"
            + " [the target](standard-xref-target.md) §2.1 for the clause.\n"
        )
        fixture = self.make_fixture("standard-xref-citer.md", citer)
        result = run_linter("tools/lint-cross-file-section-refs.py", fixture)
        self.assertEqual(
            result.returncode,
            0,
            f"resolving refs should pass.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


class RequiredSectionsTests(LinterTestCase):
    """tools/lint-required-sections.py"""

    def test_missing_orientation_section_flagged(self) -> None:
        bad = VALID_METADATA.replace("## Purpose", "## Background")
        fixture = self.make_fixture("standard-no-orientation.md", bad)
        result = run_linter("tools/lint-required-sections.py", fixture)
        self.assertLinterFails(result)

    def test_superseded_status_skipped(self) -> None:
        # A Status: Superseded document (the lifecycle marker, the L-j
        # re-key) is a short redirect notice and exempt from the per-doctype
        # required-section model.
        body = VALID_METADATA.replace(
            "**Document Type:** Standard\\\n",
            "**Document Type:** Standard\\\n**Status:** Superseded\\\n",
        ).replace("## Purpose", "## Notice")
        fixture = self.make_fixture("standard-superseded-skip.md", body)
        result = run_linter("tools/lint-required-sections.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a Status: Superseded document must be skipped.\nstdout:\n{result.stdout}",
        )


class SectionPlacementTests(LinterTestCase):
    """tools/lint-section-placement.py"""

    def test_superseded_status_skipped(self) -> None:
        # A Status: Superseded document (the lifecycle marker, the L-j
        # re-key) is exempt from the placement conventions.
        body = VALID_METADATA.replace(
            "**Document Type:** Standard\\\n",
            "**Document Type:** Standard\\\n**Status:** Superseded\\\n",
        ).replace(
            "## Purpose\n\nTest fixture content for the linter regression suite.\n",
            (
                "## Body section one\n\nText.\n\n"
                "## Body section two\n\nText.\n\n"
                "## Body section three\n\nText.\n\n"
                "## Body section four\n\nText.\n\n"
                "## Purpose\n\nText.\n"
            ),
        )
        fixture = self.make_fixture("standard-superseded-placement.md", body)
        result = run_linter("tools/lint-section-placement.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a Status: Superseded document must be skipped.\nstdout:\n{result.stdout}",
        )

    def test_orientation_section_outside_top_three_flagged(self) -> None:
        # Build a fixture where Purpose is the 5th of 5 ``##`` sections,
        # which violates SP-01 (orientation must be in the top 3).
        bad = VALID_METADATA.replace(
            "## Purpose\n\nTest fixture content for the linter regression suite.\n",
            (
                "## Body section one\n\nText.\n\n"
                "## Body section two\n\nText.\n\n"
                "## Body section three\n\nText.\n\n"
                "## Body section four\n\nText.\n\n"
                "## Purpose\n\nText.\n"
            ),
        )
        fixture = self.make_fixture("standard-orientation-late.md", bad)
        result = run_linter("tools/lint-section-placement.py", fixture)
        self.assertLinterFails(result)


class VersionBumpRecencyTests(LinterTestCase):
    """tools/lint-version-bump-recency.py"""

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: the linter is a git-history-aware corpus check;
        # the first regression-level assertion is that it runs clean on
        # the current HEAD.
        result = run_linter("tools/lint-version-bump-recency.py")
        self.assertEqual(
            result.returncode,
            0,
            f"linter exited {result.returncode} on the corpus HEAD; "
            f"all versioned documents should pass.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_stale_version_after_body_change_flagged(self) -> None:
        # Real failure-detection test (closing the gate-36 discipline
        # gap for this git-history-aware gate). Build a synthetic git
        # repo with two commits: first creates a versioned doc at
        # Version 1.0.0; second modifies the body without bumping
        # Version. Assert the linter fires.
        import shutil
        import subprocess as sp
        import tempfile

        tmp = Path(tempfile.mkdtemp(prefix="lint-recency-test-"))
        try:
            sp.run(["git", "init", "-q", "-b", "main", str(tmp)], check=True)
            sp.run(["git", "-C", str(tmp), "config", "user.email", "test@test"], check=True)
            sp.run(["git", "-C", str(tmp), "config", "user.name", "Test"], check=True)

            # The linter requires a §6 inventory in
            # governance/specification-audit-programme.md to derive the
            # canonical gate count. Provide a minimal stub.
            spec_dir = tmp / "governance"
            spec_dir.mkdir()
            (spec_dir / "specification-audit-programme.md").write_text(
                "# Stub\n\n## 6. Gate inventory (current)\n\n| # | Gate | Script |\n| - | - | - |\n| 1 | Stub | `tools/stub.py` |\n",
                encoding="utf-8",
            )

            target = tmp / "doc.md"
            target.write_text(
                "# Test Doc\n\n**Version:** 1.0.0\\\n**Date:** 2026-06-20\\\n\n## Body\n\nOriginal body content.\n",
                encoding="utf-8",
            )
            sp.run(["git", "-C", str(tmp), "add", "-A"], check=True)
            sp.run(["git", "-C", str(tmp), "commit", "-q", "-m", "Initial"], check=True)

            target.write_text(
                "# Test Doc\n\n**Version:** 1.0.0\\\n**Date:** 2026-06-20\\\n\n## Body\n\nModified body content.\n",
                encoding="utf-8",
            )
            sp.run(["git", "-C", str(tmp), "add", "-A"], check=True)
            sp.run(["git", "-C", str(tmp), "commit", "-q", "-m", "Modify body without Version bump"], check=True)

            result = sp.run(
                [sys.executable, str(REPO_ROOT / "tools/lint-version-bump-recency.py"), "--root", str(tmp)],
                capture_output=True, text=True, cwd=str(tmp),
            )
            self.assertEqual(
                result.returncode,
                1,
                f"linter should have FAILED on synthetic body-without-Version-bump fixture; got exit {result.returncode}.\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn(
                "doc.md",
                result.stdout,
                f"expected doc.md in failure output but did not find it.\nstdout:\n{result.stdout}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class DateCobumpOnPrTests(LinterTestCase):
    """tools/check-date-cobump-on-pr.py (delta gate D4).

    A PR-only delta gate, so the fixtures build a synthetic two-commit
    git repo (base then head) and run the gate over the range, the same
    shape VersionBumpRecencyTests uses. Committer dates are pinned via
    GIT_*_DATE so the bump-commit-date comparison is deterministic.
    """

    HEAD_DATE = "2026-06-26T12:00:00+00:00"

    def _build_repo(self, base_doc: str, head_doc: str):
        import shutil
        import subprocess as sp
        import tempfile

        tmp = Path(tempfile.mkdtemp(prefix="lint-cobump-test-"))
        env = dict(os.environ)
        # Pin both commit dates to 2026-06-26 UTC so the gate's
        # bump-commit-date (committer date) is deterministic.
        env["GIT_AUTHOR_DATE"] = self.HEAD_DATE
        env["GIT_COMMITTER_DATE"] = self.HEAD_DATE
        sp.run(["git", "init", "-q", "-b", "main", str(tmp)], check=True)
        sp.run(["git", "-C", str(tmp), "config", "user.email", "test@test"], check=True)
        sp.run(["git", "-C", str(tmp), "config", "user.name", "Test"], check=True)
        target = tmp / "doc.md"
        target.write_text(base_doc, encoding="utf-8")
        sp.run(["git", "-C", str(tmp), "add", "-A"], check=True, env=env)
        sp.run(["git", "-C", str(tmp), "commit", "-q", "-m", "Initial"], check=True, env=env)
        base_sha = sp.run(
            ["git", "-C", str(tmp), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        target.write_text(head_doc, encoding="utf-8")
        sp.run(["git", "-C", str(tmp), "add", "-A"], check=True, env=env)
        sp.run(["git", "-C", str(tmp), "commit", "-q", "-m", "Second"], check=True, env=env)
        return tmp, base_sha, shutil

    def _run(self, tmp: Path, base_sha: str):
        import subprocess as sp

        return sp.run(
            [
                sys.executable,
                str(REPO_ROOT / "tools/check-date-cobump-on-pr.py"),
                base_sha,
                "HEAD",
            ],
            capture_output=True, text=True, cwd=str(tmp),
        )

    def test_version_bump_without_date_cobump_flagged(self) -> None:
        # Version bumps 1.0.0 -> 1.0.1 but Date stays 2026-06-25 while the
        # bump commit is dated 2026-06-26: the gate must fire.
        base = "# Doc\n\n**Version:** 1.0.0\\\n**Date:** 2026-06-25\\\n\n## Body\n\nA.\n"
        head = "# Doc\n\n**Version:** 1.0.1\\\n**Date:** 2026-06-25\\\n\n## Body\n\nB.\n"
        tmp, base_sha, shutil = self._build_repo(base, head)
        try:
            result = self._run(tmp, base_sha)
            self.assertEqual(
                result.returncode, 1,
                f"gate should FAIL on Version-bump-without-Date-cobump; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("doc.md", result.stdout + result.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_version_and_date_cobumped_not_flagged(self) -> None:
        # Version bumps and Date co-bumps to the 2026-06-26 commit date:
        # the gate must pass.
        base = "# Doc\n\n**Version:** 1.0.0\\\n**Date:** 2026-06-25\\\n\n## Body\n\nA.\n"
        head = "# Doc\n\n**Version:** 1.0.1\\\n**Date:** 2026-06-26\\\n\n## Body\n\nB.\n"
        tmp, base_sha, shutil = self._build_repo(base, head)
        try:
            result = self._run(tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"gate should PASS when Version and Date co-bump; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_body_change_without_version_bump_out_of_scope(self) -> None:
        # Version unchanged (body edited, stale Date): D4 has nothing to
        # assert (D2 governs the missing-bump case), so it must pass.
        base = "# Doc\n\n**Version:** 1.0.0\\\n**Date:** 2026-06-20\\\n\n## Body\n\nA.\n"
        head = "# Doc\n\n**Version:** 1.0.0\\\n**Date:** 2026-06-20\\\n\n## Body\n\nB.\n"
        tmp, base_sha, shutil = self._build_repo(base, head)
        try:
            result = self._run(tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"gate should PASS when Version did not bump; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class DeltaGateRepoTestCase(unittest.TestCase):
    """Shared two-commit temp-repo harness for the PR-time delta gates.

    Generalizes the DateCobumpOnPrTests fixture shape to multi-file
    commits: each commit is a dict of relative path to content, and the
    gate under test runs with POSITIONAL base/head refs (the D4 `_run`
    pattern), so the fixture never consults GITHUB_BASE_REF or an
    `origin/main` remote. Dates are left unpinned because D1/D2/D3/D5
    are date-independent (only D4 compares commit dates).
    """

    def _build_repo(self, base_files, head_files, head_message="Second"):
        import shutil
        import subprocess as sp
        import tempfile

        tmp = Path(tempfile.mkdtemp(prefix="lint-delta-test-"))
        sp.run(["git", "init", "-q", "-b", "main", str(tmp)], check=True)
        sp.run(["git", "-C", str(tmp), "config", "user.email", "test@test"], check=True)
        sp.run(["git", "-C", str(tmp), "config", "user.name", "Test"], check=True)
        for rel, content in base_files.items():
            path = tmp / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        sp.run(["git", "-C", str(tmp), "add", "-A"], check=True)
        sp.run(["git", "-C", str(tmp), "commit", "-q", "-m", "Initial"], check=True)
        base_sha = sp.run(
            ["git", "-C", str(tmp), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        for rel, content in head_files.items():
            path = tmp / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        sp.run(["git", "-C", str(tmp), "add", "-A"], check=True)
        sp.run(["git", "-C", str(tmp), "commit", "-q", "-m", head_message], check=True)
        return tmp, base_sha, shutil

    def _run_gate(self, script_name, tmp, base_sha):
        import subprocess as sp

        return sp.run(
            [sys.executable, str(REPO_ROOT / "tools" / script_name), base_sha, "HEAD"],
            capture_output=True, text=True, cwd=str(tmp),
        )


class ChangelogOnPrTests(DeltaGateRepoTestCase):
    """tools/check-changelog-on-pr.py (delta gate D1)."""

    SCRIPT = "check-changelog-on-pr.py"
    BASE = {
        "foo.md": "# Foo\n\nA.\n",
        "CHANGELOG.md": "# Changelog\n\nOld entry.\n",
        ".working/changelog-details/CHANGELOG-detailed.md": "# Detailed\n\nOld entry.\n",
    }

    def test_content_change_without_changelog_flagged(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            self.BASE, {"foo.md": "# Foo\n\nB.\n"}
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 1,
                f"D1 should FAIL when neither CHANGELOG surface is in the diff; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("neither", result.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_both_changelog_surfaces_changed_passes(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            self.BASE,
            {
                "foo.md": "# Foo\n\nB.\n",
                "CHANGELOG.md": "# Changelog\n\nNew entry.\n\nOld entry.\n",
                ".working/changelog-details/CHANGELOG-detailed.md": (
                    "# Detailed\n\nNew entry.\n\nOld entry.\n"
                ),
            },
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D1 should PASS when both CHANGELOG surfaces move; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_root_without_mirror_flagged(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            self.BASE,
            {"CHANGELOG.md": "# Changelog\n\nNew entry.\n\nOld entry.\n"},
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 1,
                f"D1 should FAIL when the root moves without the mirror; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("detailed mirror", result.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_mirror_without_root_flagged(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            self.BASE,
            {
                ".working/changelog-details/CHANGELOG-detailed.md": (
                    "# Detailed\n\nNew entry.\n\nOld entry.\n"
                )
            },
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 1,
                f"D1 should FAIL when the mirror moves without the root; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("root", result.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_opt_out_trailer_accepted(self) -> None:
        # Back-compat: a `Changelog:` commit trailer opts the PR out.
        tmp, base_sha, shutil = self._build_repo(
            self.BASE,
            {"foo.md": "# Foo\n\nB.\n"},
            head_message="Tweak foo\n\nChangelog: skip (reason: fixture)",
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D1 should PASS on an opt-out trailer; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class VersionBumpOnPrTests(DeltaGateRepoTestCase):
    """tools/check-version-bump-on-pr.py (delta gate D2)."""

    SCRIPT = "check-version-bump-on-pr.py"
    VERSIONED_A = "# Doc\n\n**Version:** 1.0.0\\\n**Date:** 2026-06-25\\\n\n## Body\n\nA.\n"
    VERSIONED_B_SAME = "# Doc\n\n**Version:** 1.0.0\\\n**Date:** 2026-06-25\\\n\n## Body\n\nB.\n"
    VERSIONED_B_BUMPED = "# Doc\n\n**Version:** 1.0.1\\\n**Date:** 2026-06-25\\\n\n## Body\n\nB.\n"

    def test_body_change_without_version_bump_flagged(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            {"doc.md": self.VERSIONED_A}, {"doc.md": self.VERSIONED_B_SAME}
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 1,
                f"D2 should FAIL on a body change without a Version bump; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("doc.md", result.stdout + result.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_version_bumped_passes(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            {"doc.md": self.VERSIONED_A}, {"doc.md": self.VERSIONED_B_BUMPED}
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D2 should PASS when the Version bumped; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_unversioned_file_skipped(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            {"notes.md": "# Notes\n\nA.\n"}, {"notes.md": "# Notes\n\nB.\n"}
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D2 should PASS for a file with no Version field; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_added_file_skipped(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            {"doc.md": self.VERSIONED_A},
            {"doc.md": self.VERSIONED_A, "new.md": self.VERSIONED_A},
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D2 should PASS for a newly-added file; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class ChangelogDashOnPrTests(DeltaGateRepoTestCase):
    """tools/check-changelog-dash-on-pr.py (delta gate D3)."""

    SCRIPT = "check-changelog-dash-on-pr.py"

    def test_added_em_dash_line_flagged(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            {"CHANGELOG.md": "# Changelog\n\nClean line.\n"},
            {"CHANGELOG.md": "# Changelog\n\nNew entry — with an em-dash.\n\nClean line.\n"},
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 1,
                f"D3 should FAIL on an added em-dash CHANGELOG line; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_dash_free_addition_passes(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            {"CHANGELOG.md": "# Changelog\n\nClean line.\n"},
            {"CHANGELOG.md": "# Changelog\n\nNew entry, dash-free.\n\nClean line.\n"},
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D3 should PASS on a dash-free addition; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_preexisting_dash_untouched_passes(self) -> None:
        # unified=0 sees only ADDED lines, so a historical em-dash in
        # context must not fire when a clean line is appended.
        tmp, base_sha, shutil = self._build_repo(
            {"CHANGELOG.md": "# Changelog\n\nOld — historical dash line.\n"},
            {"CHANGELOG.md": "# Changelog\n\nNew clean entry.\n\nOld — historical dash line.\n"},
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D3 should PASS when the only dashes are pre-existing; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_changelog_not_modified_passes(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            {"CHANGELOG.md": "# Changelog\n\nClean line.\n", "foo.md": "# Foo\n\nA.\n"},
            {"foo.md": "# Foo\n\nB.\n"},
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D3 should PASS when CHANGELOG.md is not in the diff; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TodoRotationOnPrDeltaTests(DeltaGateRepoTestCase):
    """tools/check-todo-rotation-on-pr.py (delta gate D5), subprocess tier.

    Complements TodoRotationOnPrTests (the closure-pattern unit tests)
    with behavioural fixtures over a real two-commit range.
    """

    SCRIPT = "check-todo-rotation-on-pr.py"
    BASE = {
        "CHANGELOG.md": "# Changelog\n\nOld entry.\n",
        ".working/changelog-details/CHANGELOG-detailed.md": "# Detailed\n\nOld entry.\n",
        "TODO.md": "# TODO\n\n- item one\n- item two\n",
        ".working/DONE.md": "# DONE\n\nOld row.\n",
    }
    CLOSURE_LINE = "Closes the TODO §4.9 cleanup item.\n"

    def test_closure_claim_without_rotation_flagged(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            self.BASE,
            {"CHANGELOG.md": "# Changelog\n\n" + self.CLOSURE_LINE + "\nOld entry.\n"},
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 1,
                f"D5 should FAIL on a closure claim without the TODO/DONE rotation; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_closure_with_rotation_passes(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            self.BASE,
            {
                "CHANGELOG.md": "# Changelog\n\n" + self.CLOSURE_LINE + "\nOld entry.\n",
                "TODO.md": "# TODO\n\n- item two\n",
                ".working/DONE.md": "# DONE\n\nNew row.\n\nOld row.\n",
            },
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D5 should PASS when TODO and DONE both rotate; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_trailer_opt_out_passes(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            self.BASE,
            {"CHANGELOG.md": "# Changelog\n\n" + self.CLOSURE_LINE + "\nOld entry.\n"},
            head_message="Narrate closure\n\nTodoRotation: narration only (fixture)",
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D5 should PASS on a TodoRotation opt-out trailer; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class PackReadmeCobumpOnPrTests(DeltaGateRepoTestCase):
    """tools/check-pack-readme-cobump-on-pr.py (delta gate D6).

    A PR that changes the pack README's **Version:** value must add the
    matching ``| <new-version> |`` row to its ``## Version history``
    table in the same diff (the paired-surface checklist instance (a),
    mechanized). Uses the shared two-commit temp-repo harness.
    """

    SCRIPT = "check-pack-readme-cobump-on-pr.py"
    PACK = "dev-security/claude-rules/README.md"

    @staticmethod
    def _readme(version, rows):
        table = "\n".join(f"| {v} | 2026.07.1 | 2026-07-04 | note |" for v in rows)
        return (
            "# Pack README\n\n"
            f"**Version:** {version}\\\n"
            "**Date:** 2026-07-04\n\n"
            "Body.\n\n"
            "## Version history\n\n"
            "| Pack | Library | Date | Notable change |\n"
            "| --- | --- | --- | --- |\n"
            f"{table}\n"
        )

    def test_version_bump_with_history_row_passes(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            {self.PACK: self._readme("1.0.0", ["1.0.0"])},
            {self.PACK: self._readme("1.0.1", ["1.0.1", "1.0.0"])},
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D6 should PASS on bump-with-row.\nstdout:\n{result.stdout}"
                f"\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_version_bump_without_history_row_fails(self) -> None:
        # Version bumps but the history table gains no 1.0.1 row.
        tmp, base_sha, shutil = self._build_repo(
            {self.PACK: self._readme("1.0.0", ["1.0.0"])},
            {self.PACK: self._readme("1.0.1", ["1.0.0"])},
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 1,
                f"D6 should FAIL on bump-without-row.\nstdout:\n{result.stdout}"
                f"\nstderr:\n{result.stderr}",
            )
            self.assertIn("1.0.1", result.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_version_unchanged_not_triggered(self) -> None:
        # Body-only edit; Version value identical: the gate stays silent.
        base = self._readme("1.0.0", ["1.0.0"])
        tmp, base_sha, shutil = self._build_repo(
            {self.PACK: base},
            {self.PACK: base.replace("Body.", "Body changed.")},
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D6 should not trigger on an unchanged Version.\nstdout:\n"
                f"{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("not triggered", result.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_pack_readme_untouched_not_triggered(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            {self.PACK: self._readme("1.0.0", ["1.0.0"]), "other.md": "A.\n"},
            {"other.md": "B.\n"},
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D6 should not trigger when the pack README is untouched."
                f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)



class HandoffSnapshotOnPrTests(DeltaGateRepoTestCase):
    """tools/check-handoff-snapshot-on-pr.py (delta gate D7).

    A PR that touches the session handoff must carry a Current-truth
    snapshot line whose labelled version tokens match the live headers
    at the PR head; duplicate labelled tokens fail. Uses the shared
    two-commit temp-repo harness.
    """

    SCRIPT = "check-handoff-snapshot-on-pr.py"
    HANDOFF = ".working/session-handoff.md"
    README = "README.md"

    @staticmethod
    def _readme(calver, version):
        return (
            "# Library\n\n"
            f"**Library Version:** {calver} (CalVer)\\\n"
            f"**README Version:** {version} (semantic)\n\n"
            "Body.\n"
        )

    @staticmethod
    def _handoff(line):
        return (
            "# Session handoff\n\n"
            "## State snapshot\n\n"
            f"- **Current truth (verify against live files at /resume)**: {line}\n"
        )

    def test_matching_tokens_pass(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            {
                self.README: self._readme("2026.07.1", "1.0.0"),
                self.HANDOFF: self._handoff("library `2026.07.1`, README `1.0.0`."),
            },
            {
                self.README: self._readme("2026.07.2", "1.0.1"),
                self.HANDOFF: self._handoff("library `2026.07.2`, README `1.0.1`."),
            },
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D7 should PASS on reconciled tokens.\nstdout:\n{result.stdout}"
                f"\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_stale_token_fails(self) -> None:
        # README advances but the refreshed handoff still quotes the old
        # CalVer: the append-not-reconcile shape.
        tmp, base_sha, shutil = self._build_repo(
            {
                self.README: self._readme("2026.07.1", "1.0.0"),
                self.HANDOFF: self._handoff("library `2026.07.1`, README `1.0.0`."),
            },
            {
                self.README: self._readme("2026.07.2", "1.0.1"),
                self.HANDOFF: self._handoff("library `2026.07.1`, README `1.0.1`."),
            },
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 1,
                f"D7 should FAIL on a stale token.\nstdout:\n{result.stdout}"
                f"\nstderr:\n{result.stderr}",
            )
            self.assertIn("stale token", result.stderr)
            self.assertIn("2026.07.1", result.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_duplicate_token_fails(self) -> None:
        # The seventh-occurrence shape: the same labelled surface quoted
        # twice on the snapshot line.
        tmp, base_sha, shutil = self._build_repo(
            {
                self.README: self._readme("2026.07.1", "1.0.0"),
                self.HANDOFF: self._handoff("library `2026.07.1`, README `1.0.0`."),
            },
            {
                self.README: self._readme("2026.07.1", "1.0.1"),
                self.HANDOFF: self._handoff(
                    "library `2026.07.1`, README `1.0.1`, README `1.0.0`."
                ),
            },
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 1,
                f"D7 should FAIL on a duplicate token.\nstdout:\n{result.stdout}"
                f"\nstderr:\n{result.stderr}",
            )
            self.assertIn("duplicate token", result.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_handoff_untouched_not_triggered(self) -> None:
        # The PR changes only the README; the (now-stale) handoff is not
        # in the diff, so the delta gate stays silent by design.
        handoff = self._handoff("library `2026.07.1`, README `1.0.0`.")
        tmp, base_sha, shutil = self._build_repo(
            {
                self.README: self._readme("2026.07.1", "1.0.0"),
                self.HANDOFF: handoff,
            },
            {self.README: self._readme("2026.07.2", "1.0.1")},
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 0,
                f"D7 should not trigger when the handoff is untouched.\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("not triggered", result.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_missing_snapshot_line_fails(self) -> None:
        tmp, base_sha, shutil = self._build_repo(
            {
                self.README: self._readme("2026.07.1", "1.0.0"),
                self.HANDOFF: self._handoff("library `2026.07.1`."),
            },
            {
                self.README: self._readme("2026.07.1", "1.0.0"),
                self.HANDOFF: "# Session handoff\n\nNo snapshot here.\n",
            },
        )
        try:
            result = self._run_gate(self.SCRIPT, tmp, base_sha)
            self.assertEqual(
                result.returncode, 1,
                f"D7 should FAIL on a missing Current-truth line.\nstdout:\n"
                f"{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("no 'Current truth'", result.stderr.replace('"', "'"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_surfaces_table_paths_resolve_in_real_repo(self) -> None:
        # Pins the confabulated-live-path class caught in the #634 build
        # (the guardrail-history row named .working/guardrail-review/,
        # singular, and the gate failed its own PR): every SURFACES row's
        # live_path must exist in the real repo and its header_re must
        # match that file's content, so a renamed or misspelled surface
        # fails here instead of in CI on the next handoff-touching PR.
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "check_handoff_snapshot_mod",
            REPO_ROOT / "tools" / self.SCRIPT,
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for label, _token_re, live_path, header_re in mod.SURFACES:
            target = REPO_ROOT / live_path
            self.assertTrue(
                target.is_file(),
                f"SURFACES label '{label}' names {live_path}, which does "
                "not exist in the repo",
            )
            self.assertIsNotNone(
                header_re.search(target.read_text(encoding="utf-8")),
                f"SURFACES label '{label}': no parsable header version "
                f"field in {live_path}",
            )


class PrePushGuardTests(unittest.TestCase):
    """tools/pre-push-guard.sh exit-code chain.

    Pins the improvement-log #438/#439 regression class: the guard must
    propagate a failing runner's exit code (captured from the BARE
    command, not an `if ! cmd` test) and must not run the second runner
    after the first fails. The fixture copies the real guard into a temp
    tree beside stub runners.
    """

    def _build_guard_dir(self, first_rc: int, second_rc: int):
        import shutil
        import stat
        import tempfile

        tmp = Path(tempfile.mkdtemp(prefix="lint-guard-test-"))
        tools = tmp / "tools"
        tools.mkdir()
        shutil.copy(REPO_ROOT / "tools" / "pre-push-guard.sh", tools / "pre-push-guard.sh")
        (tools / "run_all_audits.sh").write_text(
            f"#!/bin/bash\nexit {first_rc}\n", encoding="utf-8"
        )
        (tools / "run-pr-time-checks.sh").write_text(
            "#!/bin/bash\ntouch \"$(dirname \"$0\")/../second-ran.marker\"\n"
            f"exit {second_rc}\n",
            encoding="utf-8",
        )
        for name in ("pre-push-guard.sh", "run_all_audits.sh", "run-pr-time-checks.sh"):
            path = tools / name
            path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return tmp, shutil

    def _run_guard(self, tmp: Path, allow_pipe: bool = True):
        import os
        import subprocess as sp

        # capture_output wires the guard's stdout to a PIPE, which the
        # RM-10 self-defence (TODO 1.9(b), PR #620) refuses by design; the
        # documented override is the sanctioned way to run a deliberate,
        # judged pipe, which is exactly what this harness capture is. The
        # refusal path itself is pinned by test_piped_stdout_refused.
        env = dict(os.environ)
        if allow_pipe:
            env["PRE_PUSH_GUARD_ALLOW_PIPE"] = "1"
        else:
            env.pop("PRE_PUSH_GUARD_ALLOW_PIPE", None)
        return sp.run(
            ["bash", str(tmp / "tools" / "pre-push-guard.sh")],
            capture_output=True, text=True, cwd=str(tmp), env=env,
        )

    def test_first_runner_failure_blocks_and_skips_second(self) -> None:
        tmp, shutil = self._build_guard_dir(first_rc=7, second_rc=0)
        try:
            result = self._run_guard(tmp)
            self.assertEqual(
                result.returncode, 7,
                f"guard should exit with the first runner's code; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("FAILED at run_all_audits.sh", result.stdout)
            self.assertFalse(
                (tmp / "second-ran.marker").exists(),
                "second runner must not run after the first fails",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_second_runner_failure_blocks(self) -> None:
        tmp, shutil = self._build_guard_dir(first_rc=0, second_rc=5)
        try:
            result = self._run_guard(tmp)
            self.assertEqual(
                result.returncode, 5,
                f"guard should exit with the second runner's code; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("FAILED at run-pr-time-checks.sh", result.stdout)
            self.assertTrue((tmp / "second-ran.marker").exists())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_both_runners_green_passes(self) -> None:
        tmp, shutil = self._build_guard_dir(first_rc=0, second_rc=0)
        try:
            result = self._run_guard(tmp)
            self.assertEqual(
                result.returncode, 0,
                f"guard should exit 0 when both runners pass; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("Safe to push", result.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_piped_stdout_refused(self) -> None:
        """RM-10 self-defence (TODO 1.9(b)): piped stdout without the
        override refuses with exit 3 before any runner runs."""
        tmp, shutil = self._build_guard_dir(first_rc=0, second_rc=0)
        try:
            result = self._run_guard(tmp, allow_pipe=False)
            self.assertEqual(
                result.returncode, 3,
                f"guard should refuse piped stdout with exit 3; got "
                f"{result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("REFUSING", result.stderr)
            self.assertFalse(
                (tmp / "second-ran.marker").exists(),
                "no runner may run on the refusal path",
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class ExternalOverlayLicenseTests(LinterTestCase):
    """tools/lint-external-overlay-license.py"""

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: external overlay licence consistency holds at HEAD.
        result = run_linter("tools/lint-external-overlay-license.py")
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on HEAD; "
            f"external overlay licence consistency should hold.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


class FollowupAgeingTests(LinterTestCase):
    """tools/lint-followup-ageing.py"""

    def tearDown(self) -> None:
        # The fixtures use subdirectories under FIXTURE_DIR; the module-
        # level tearDown only removes top-level *.md files. Clean
        # subdirectories explicitly so the corpus audits (which scan
        # the entire repo for markdown) do not pick them up.
        import shutil
        for sub in (
            "followup-ageing-expired",
            "followup-ageing-retriaged",
            "followup-ageing-invalid",
        ):
            path = FIXTURE_DIR / sub
            if path.exists():
                shutil.rmtree(path)
        super().tearDown()

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: the register has no expired follow-ups at HEAD.
        result = run_linter("tools/lint-followup-ageing.py")
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on HEAD; "
            f"the sweep-history register should have no expired follow-ups.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_expired_followup_flagged(self) -> None:
        # Positive test: build a fixture with a surfaced/re-triage-by
        # pair whose deadline has passed and no re-triaged trailer.
        # Use --today to make the test independent of the wall clock.
        fixture_dir = FIXTURE_DIR / "followup-ageing-expired"
        fixture_dir.mkdir(parents=True, exist_ok=True)
        fixture_path = fixture_dir / "register.md"
        fixture_path.write_text(
            "# Test register\n\n"
            "### 2026-01-01, Test deferred entry\n\n"
            "- **Finding**: A deferred test finding\n"
            "  - surfaced: 2026-01-01\n"
            "  - re-triage-by: 2026-02-01\n"
            "- **Status**: pending\n\n",
            encoding="utf-8",
        )
        result = run_linter(
            "tools/lint-followup-ageing.py",
            "--target", "register.md",
            "--root", str(fixture_dir),
            "--today", "2026-06-20",
        )
        self.assertEqual(
            result.returncode, 1,
            f"linter should have exited 1 on expired follow-up.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "past its re-triage-by deadline",
            result.stderr,
            f"expected FAIL message about expired deadline; got:\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_fresh_retriaged_trailer_dismisses(self) -> None:
        # Negative test: same expired fixture, but with a re-triaged
        # trailer dated after the deadline. Should pass.
        fixture_dir = FIXTURE_DIR / "followup-ageing-retriaged"
        fixture_dir.mkdir(parents=True, exist_ok=True)
        fixture_path = fixture_dir / "register.md"
        fixture_path.write_text(
            "# Test register\n\n"
            "### 2026-01-01, Test deferred entry\n\n"
            "- **Finding**: A deferred test finding\n"
            "  - surfaced: 2026-01-01\n"
            "  - re-triage-by: 2026-02-01\n"
            "  - re-triaged: 2026-06-15\n"
            "- **Status**: under review\n\n",
            encoding="utf-8",
        )
        result = run_linter(
            "tools/lint-followup-ageing.py",
            "--target", "register.md",
            "--root", str(fixture_dir),
            "--today", "2026-06-20",
        )
        self.assertEqual(
            result.returncode, 0,
            f"linter should have exited 0 with a fresh re-triaged trailer.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_invalid_date_value_exits_two(self) -> None:
        # Environmental test: syntactically YYYY-MM-DD but invalid date
        # value (Feb 30 doesn't exist) triggers exit 2. Note: slash-
        # separated dates would not match the regex at all and would be
        # silently ignored; only well-formed-shape-but-invalid-value
        # dates reach the parser.
        fixture_dir = FIXTURE_DIR / "followup-ageing-invalid"
        fixture_dir.mkdir(parents=True, exist_ok=True)
        fixture_path = fixture_dir / "register.md"
        fixture_path.write_text(
            "# Test register\n\n"
            "### Test entry\n\n"
            "- **Finding**: invalid value\n"
            "  - surfaced: 2026-02-30\n"
            "- **Status**: pending\n\n",
            encoding="utf-8",
        )
        result = run_linter(
            "tools/lint-followup-ageing.py",
            "--target", "register.md",
            "--root", str(fixture_dir),
            "--today", "2026-06-20",
        )
        self.assertEqual(
            result.returncode, 2,
            f"linter should have exited 2 on invalid date value.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


class PairedSkillStepParityTests(LinterTestCase):
    """tools/lint-paired-skill-step-parity.py"""

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: the validation-sweep pair's step identifiers
        # match at HEAD.
        result = run_linter("tools/lint-paired-skill-step-parity.py")
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on HEAD; "
            f"the validation-sweep SKILL+command pair should match.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def _load_module(self):
        # The linter's PAIRS list is hard-coded at module-import time;
        # for unit tests on the regex extractors we import the module
        # directly via spec loading (the filename has hyphens so a
        # bare `import` won't work). The linter imports `lint_common`,
        # so we add tools/ to sys.path before exec.
        import importlib.util
        tools_dir = str(REPO_ROOT / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        spec = importlib.util.spec_from_file_location(
            "_paired_skill_step_parity",
            REPO_ROOT / "tools/lint-paired-skill-step-parity.py",
        )
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_drift_detection(self) -> None:
        # Positive test: SKILL.md heading uses "3.5", command uses
        # "3a". The extractors produce non-equal sets so the
        # symmetric-difference check would fire.
        mod = self._load_module()
        skill_with_3_5 = (
            "# Skill\n"
            "### 1. First step\n"
            "### 2. Second step\n"
            "### 3.5. Half step\n"
            "### 4. Fourth step\n"
        )
        command_with_3a = (
            "1. **First step**: content.\n"
            "2. **Second step**: content.\n"
            "3a. **Half step**: content.\n"
            "4. **Fourth step**: content.\n"
        )
        skill_steps = mod.extract_skill_steps(skill_with_3_5)
        command_steps = mod.extract_command_steps(command_with_3a)
        self.assertIn("3.5", skill_steps)
        self.assertIn("3a", command_steps)
        self.assertNotEqual(
            skill_steps, command_steps,
            "drifted step identifiers should produce non-equal sets",
        )

    def test_matching_pair_passes(self) -> None:
        # Negative test: when both files use the same identifier,
        # the sets match.
        mod = self._load_module()
        skill_with_3a = (
            "### 1. First\n"
            "### 2. Second\n"
            "### 3a. Half\n"
            "### 4. Fourth\n"
        )
        command_with_3a = (
            "1. **First**: x.\n"
            "2. **Second**: x.\n"
            "3a. **Half**: x.\n"
            "4. **Fourth**: x.\n"
        )
        self.assertEqual(
            mod.extract_skill_steps(skill_with_3a),
            mod.extract_command_steps(command_with_3a),
        )


class CollectionEnumerationConsistencyTests(LinterTestCase):
    """tools/lint-collection-enumeration-consistency.py"""

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test against the current corpus: the linter should
        # report consistent enumerations across all declared collections.
        result = run_linter("tools/lint-collection-enumeration-consistency.py")
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on HEAD; "
            f"all declared collections should be consistent.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


class GateCountConsistencyTests(LinterTestCase):
    """tools/lint-gate-count-consistency.py"""

    def test_stale_gate_count_reference_flagged(self) -> None:
        # Build a fixture containing a stale "N-gate" reference where N
        # does not match the canonical count in the live §6 inventory.
        # The canonical count is whatever the spec currently declares;
        # the fixture uses "0-gate" which will never match (the spec
        # cannot have zero gates).
        fixture = self.make_fixture(
            "standard-bad-gate-count.md",
            VALID_METADATA + "\n\nThis stub mentions the 0-gate audit programme.\n",
        )
        result = run_linter("tools/lint-gate-count-consistency.py", fixture)
        self.assertLinterFails(result)

    def test_vanished_file_skipped(self) -> None:
        # A file can vanish between rglob discovery and read when the
        # regression suite runs concurrently in the same tree (the routed
        # #577 sweep I2); scan_file must skip it, not crash. Exercised at
        # the unit level: scan_file on a nonexistent path returns no
        # findings instead of raising FileNotFoundError.
        import importlib.util
        # The linter imports lint_common; add tools/ to sys.path first (the
        # sibling importlib-loading tests' convention) so this test passes
        # in isolation, not only after an earlier class inserted the path.
        tools_dir = str(REPO_ROOT / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        lpath = REPO_ROOT / "tools" / "lint-gate-count-consistency.py"
        spec = importlib.util.spec_from_file_location("lint_gate_count_consistency", lpath)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ghost = REPO_ROOT / "tests" / "no-such-transient-fixture.md"
        self.assertFalse(ghost.exists())
        counts = {"gate": 1, "rule": 1, "skill": 1}
        self.assertEqual(mod.scan_file(ghost, counts), [])

    def test_stale_automated_audits_count_flagged(self) -> None:
        # P8: the "N automated audits" idiom (the audit programme
        # referred to by its audits rather than its gates). "0 automated
        # audits" can never match the canonical count, so the linter
        # must flag it. Added after PR #272 found this idiom escaping
        # patterns P1-P7.
        fixture = self.make_fixture(
            "standard-bad-automated-audits-count.md",
            VALID_METADATA
            + "\n\nThis stub mentions the 0 automated audits in the suite.\n",
        )
        result = run_linter("tools/lint-gate-count-consistency.py", fixture)
        self.assertLinterFails(result)

    def test_stale_wordform_audit_gates_flagged(self) -> None:
        # P9 (word-form): "ninety-nine audit gates" can never match the
        # canonical gate count (58), so the word-form gate-count check must
        # flag it. (The gate-39-blind word-form class; the backlog item that queued it has rotated out.)
        fixture = self.make_fixture(
            "standard-bad-wordform-gates.md",
            "# X\n\nThis stub mentions the ninety-nine audit gates in the suite.\n",
        )
        result = run_linter("tools/lint-gate-count-consistency.py", fixture)
        self.assertLinterFails(result)

    def test_stale_wordform_growth_narrative_flagged(self) -> None:
        # P12 (growth-narrative): "gates to ninety-nine" resolves the
        # collection keyword (gates) and the TO-target word-number; 99 never
        # matches the canonical 58, so it is flagged. The rounded FROM value
        # ("a dozen gates") is deliberately NOT matched.
        fixture = self.make_fixture(
            "standard-bad-wordform-growth.md",
            "# X\n\nThe machinery grew from a dozen gates to ninety-nine over time.\n",
        )
        result = run_linter("tools/lint-gate-count-consistency.py", fixture)
        self.assertLinterFails(result)

    def test_stale_wordform_governance_rules_flagged(self) -> None:
        # P11 (word-form): the qualified "ninety-nine governance rules" can
        # never match the canonical rule count (12), so it is flagged.
        fixture = self.make_fixture(
            "standard-bad-wordform-rules.md",
            "# X\n\nThe pack ships ninety-nine governance rules today.\n",
        )
        result = run_linter("tools/lint-gate-count-consistency.py", fixture)
        self.assertLinterFails(result)

    def test_wordform_pervasive_small_numbers_not_flagged(self) -> None:
        # False-positive guard: the bare small-word-number prose that recurs
        # throughout the corpus must NEVER be flagged (the precision-first
        # constraint the narrow anchoring exists to honour).
        fixture = self.make_fixture(
            "standard-wordform-bare-ok.md",
            "# X\n\nOne gate, one concern. Two rules overlap; do two rules, "
            "two skills, or two gates cover the same ground? Six rules, no "
            "ceremony. The two skills run as a suite. Five gate violations.\n",
        )
        result = run_linter("tools/lint-gate-count-consistency.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"bare small-word-number prose must not be flagged.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_version_history_section_not_scanned(self) -> None:
        # A "## Version history" section is a frozen change log: a stale
        # word-form count quoted in a historical row must NOT be flagged
        # (the in-document analogue of the CHANGELOG.md file exemption).
        fixture = self.make_fixture(
            "standard-wordform-history-ok.md",
            "# X\n\n## Version history\n\n| 1.0.0 | the prior ninety-nine "
            "audit gates were corrected | 2026-06-30 |\n",
        )
        result = run_linter("tools/lint-gate-count-consistency.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a stale count inside a Version history section must not be flagged.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


class ListingSurfaceCompletenessTests(LinterTestCase):
    """tools/lint-listing-surface-completeness.py"""

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: the register index and every domain README are
        # complete against the taxonomy active-document set at HEAD.
        result = run_linter("tools/lint-listing-surface-completeness.py")
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on HEAD; the register and "
            f"domain READMEs should enumerate every active document.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def _load_module(self):
        # The linter reads fixed repository paths; for unit tests on its
        # detection logic we import the module directly (hyphenated
        # filename) and call its check_* functions with a crafted active
        # set. The linter imports lint_common, so tools/ must be on the
        # path before exec.
        import importlib.util
        tools_dir = str(REPO_ROOT / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        spec = importlib.util.spec_from_file_location(
            "_listing_surface_completeness",
            REPO_ROOT / "tools/lint-listing-surface-completeness.py",
        )
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        # Register before exec so the @dataclass decorator can resolve
        # the module via sys.modules during class processing.
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        return mod

    def test_detects_missing_register_doc(self) -> None:
        # A domain-prefixed active document absent from the register
        # index must be flagged as missing.
        mod = self._load_module()
        fake = "governance/standard-fake-missing-from-register.md"
        active = mod.active_documents() | {fake}
        finding = mod.check_register(active)
        self.assertIsNotNone(
            finding, "a domain-prefixed doc absent from the register should flag"
        )
        self.assertIn(fake, finding.missing)

    def test_detects_missing_readme_doc(self) -> None:
        # An active document absent from its domain README must be flagged.
        mod = self._load_module()
        fake = "ai/standard-fake-missing-from-readme.md"
        active = mod.active_documents() | {fake}
        findings = mod.check_domain_readmes(active)
        ai_findings = [f for f in findings if f.surface == "ai/README.md"]
        self.assertTrue(
            ai_findings, "a doc absent from its domain README should flag"
        )
        self.assertIn(fake, ai_findings[0].missing)

    def test_root_level_meta_spec_exempt_from_register(self) -> None:
        # A root-level meta-specification (no domain prefix) is exempt
        # from the register-completeness rule: adding one to the active
        # set must NOT produce a register finding.
        mod = self._load_module()
        active = mod.active_documents() | {"specification-fake-root-meta.md"}
        finding = mod.check_register(active)
        self.assertIsNone(
            finding,
            "root-level meta-specs are exempt; adding one should not flag",
        )


class ChangelogMirrorHeaderParityTests(LinterTestCase):
    """tools/lint-changelog-mirror-header-parity.py"""

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: the root CHANGELOG and its detailed mirror carry the
        # same per-PR header set (at or above the cutoff) at HEAD.
        result = run_linter("tools/lint-changelog-mirror-header-parity.py")
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on HEAD; the root CHANGELOG "
            f"and its detailed mirror should carry the same per-PR headers.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def _write_pair(self, root: Path, root_headers: str, mirror_headers: str) -> None:
        (root / "CHANGELOG.md").write_text(root_headers, encoding="utf-8")
        mirror_dir = root / ".working" / "changelog-details"
        mirror_dir.mkdir(parents=True, exist_ok=True)
        (mirror_dir / "CHANGELOG-detailed.md").write_text(mirror_headers, encoding="utf-8")

    def test_header_missing_from_mirror_flagged(self) -> None:
        # A post-cutoff PR header present in root but absent from the mirror
        # (the #388 orphaned-header defect class) must be flagged.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_pair(
                root,
                "## 2026-07-01, Library Version 2026.07.9, PR #521\n\nlead.\n"
                "## 2026-06-30, Library Version 2026.06.8, PR #520\n\nlead.\n",
                "## 2026-06-30, Library Version 2026.06.8, PR #520\n\nfull.\n",
            )
            result = run_linter(
                "tools/lint-changelog-mirror-header-parity.py", "--root", str(root)
            )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("#521", result.stdout)

    def test_matching_pair_passes(self) -> None:
        # When both surfaces carry the same post-cutoff header set the gate
        # passes.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            same = (
                "## 2026-07-01, Library Version 2026.07.9, PR #521\n\ntext.\n"
                "## 2026-06-30, Library Version 2026.06.8, PR #520\n\ntext.\n"
            )
            self._write_pair(root, same, same)
            result = run_linter(
                "tools/lint-changelog-mirror-header-parity.py", "--root", str(root)
            )
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_pre_cutoff_mismatch_not_flagged(self) -> None:
        # A header below the cutoff present on only one side is an accepted
        # historical exemption, not a violation.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_pair(
                root,
                "## 2026-05-01, Library Version 2026.05.1, PR #462\n\nlead.\n"
                "## 2026-07-01, Library Version 2026.07.9, PR #521\n\nlead.\n",
                "## 2026-07-01, Library Version 2026.07.9, PR #521\n\nfull.\n",
            )
            result = run_linter(
                "tools/lint-changelog-mirror-header-parity.py", "--root", str(root)
            )
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_out_of_order_version_flagged(self) -> None:
        # GR-1: a smaller Library Version ABOVE a larger one (entries are
        # newest-first) must fail the ordering assertion.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            same = (
                "## 2026-07-01, Library Version 2026.07.8, PR #521\n\ntext.\n"
                "## 2026-06-30, Library Version 2026.07.9, PR #520\n\ntext.\n"
            )
            self._write_pair(root, same, same)
            result = run_linter(
                "tools/lint-changelog-mirror-header-parity.py", "--root", str(root)
            )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("SMALLER version", result.stdout)

    def test_equal_versions_flagged(self) -> None:
        # GR-1: two post-cutoff entries sharing one Library Version (the
        # historical #174/#175 shape) must fail with the equal-version wording.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            same = (
                "## 2026-07-01, Library Version 2026.07.9, PR #521\n\ntext.\n"
                "## 2026-06-30, Library Version 2026.07.9, PR #520\n\ntext.\n"
            )
            self._write_pair(root, same, same)
            result = run_linter(
                "tools/lint-changelog-mirror-header-parity.py", "--root", str(root)
            )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("share Library Version", result.stdout)

    def test_single_digit_patch_compares_numerically(self) -> None:
        # GR-1: 2026.06.9 above 2026.06.10 must FAIL (9 < 10 numerically); a
        # string compare would wrongly pass it ("9" > "1"). Guards against a
        # lexicographic-compare regression.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            same = (
                "## 2026-06-10, Library Version 2026.06.9, PR #521\n\ntext.\n"
                "## 2026-06-09, Library Version 2026.06.10, PR #520\n\ntext.\n"
            )
            self._write_pair(root, same, same)
            result = run_linter(
                "tools/lint-changelog-mirror-header-parity.py", "--root", str(root)
            )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("SMALLER version", result.stdout)

    def test_pre_cutoff_out_of_order_exempt(self) -> None:
        # GR-1: the historical PR #170-#175 non-monotonic window sits below
        # the cutoff; a replica must NOT flag.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            same = (
                "## 2026-06-21, Library Version 2026.06.152, PR #170\n\ntext.\n"
                "## 2026-06-21, Library Version 2026.06.153, PR #172\n\ntext.\n"
                "## 2026-06-20, Library Version 2026.06.150, PR #463\n\ntext.\n"
            )
            self._write_pair(root, same, same)
            result = run_linter(
                "tools/lint-changelog-mirror-header-parity.py", "--root", str(root)
            )
        self.assertEqual(result.returncode, 0, result.stdout)


class AcronymConsistencyTests(LinterTestCase):
    """tools/lint-acronym-consistency.py"""

    def test_inconsistent_acronym_expansion_flagged(self) -> None:
        # CISO is in the glossary as "Chief Information Security Officer";
        # use a deliberately-wrong expansion with zero overlapping significant
        # words. The inline-definition regex requires "Words (ACR)" form.
        fixture = self.make_fixture(
            "standard-bad-acronym.md",
            VALID_METADATA + "\n\nThe Cute Internet Snack Object (CISO) is fictional.\n",
        )
        result = run_linter("tools/lint-acronym-consistency.py", fixture)
        self.assertLinterFails(result)

    def test_root_override_with_missing_register_exits_2(self) -> None:
        # Phase 23.64: --root override + missing-glossary → exit 2.
        synthetic_root = FIXTURE_DIR / "synthetic-root-no-register-glossary"
        synthetic_root.mkdir(parents=True, exist_ok=True)
        try:
            result = run_linter(
                "tools/lint-acronym-consistency.py",
                "--root",
                str(synthetic_root),
            )
            self.assertEqual(
                result.returncode,
                2,
                f"linter should exit 2 when --root names a directory "
                f"without governance/register-glossary.md.\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            import shutil
            shutil.rmtree(synthetic_root, ignore_errors=True)


class SecretsLinterTests(LinterTestCase):
    """tools/lint-secrets-in-content.py"""

    def test_aws_key_pattern_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-aws-key.md",
            VALID_METADATA + "\n\nExample key: AKIAIOSFODNN7EXAMPLE.\n",
        )
        result = run_linter("tools/lint-secrets-in-content.py", fixture)
        self.assertLinterFails(result)

    def test_github_pat_pattern_flagged(self) -> None:
        # GitHub classic personal access tokens start with ghp_ and are
        # 40 chars total (4 prefix + 36 hash). Use a synthetic but
        # pattern-matching example.
        fake_token = "ghp_" + "A" * 36
        fixture = self.make_fixture(
            "standard-github-token.md",
            VALID_METADATA + f"\n\nExample token: {fake_token}.\n",
        )
        result = run_linter("tools/lint-secrets-in-content.py", fixture)
        self.assertLinterFails(result)

    def test_slack_token_pattern_flagged(self) -> None:
        # Slack bot tokens are xoxb-<digits>-<digits>-<token>; require
        # enough length to bypass the false-positive filters.
        fake_token = "xoxb-" + "1" * 12 + "-" + "2" * 12 + "-" + "A" * 24
        fixture = self.make_fixture(
            "standard-slack-token.md",
            VALID_METADATA + f"\n\nExample: {fake_token}.\n",
        )
        result = run_linter("tools/lint-secrets-in-content.py", fixture)
        self.assertLinterFails(result)

    def test_pem_private_key_pattern_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-pem-key.md",
            VALID_METADATA + "\n\nExample block:\n\n-----BEGIN RSA PRIVATE KEY-----\nMIIBOgIBAAJB\n-----END RSA PRIVATE KEY-----\n",
        )
        result = run_linter("tools/lint-secrets-in-content.py", fixture)
        self.assertLinterFails(result)

    def test_pem_pkcs8_private_key_flagged(self) -> None:
        # PKCS#8 unencrypted: "-----BEGIN PRIVATE KEY-----" carries NO
        # algorithm token. This is the most common modern serialization
        # (OpenSSL default) and was MISSED by the prior algorithm-token
        # regex; the anchored pattern catches it.
        fixture = self.make_fixture(
            "standard-pem-pkcs8.md",
            VALID_METADATA
            + "\n\nExample block:\n\n-----BEGIN PRIVATE KEY-----\nMIIBOgIBAAJB\n-----END PRIVATE KEY-----\n",
        )
        result = run_linter("tools/lint-secrets-in-content.py", fixture)
        self.assertLinterFails(result, "Private key block")

    def test_pem_encrypted_private_key_flagged(self) -> None:
        # PKCS#8 encrypted: "-----BEGIN ENCRYPTED PRIVATE KEY-----".
        # "ENCRYPTED" is not an algorithm token; the prior regex missed
        # it. The anchored pattern's open-ended uppercase prefix matches.
        fixture = self.make_fixture(
            "standard-pem-encrypted.md",
            VALID_METADATA
            + "\n\nExample block:\n\n-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIBOgIBAAJB\n-----END ENCRYPTED PRIVATE KEY-----\n",
        )
        result = run_linter("tools/lint-secrets-in-content.py", fixture)
        self.assertLinterFails(result, "Private key block")

    def test_pem_pgp_private_key_block_flagged(self) -> None:
        # The REAL PGP private-key header is "PGP PRIVATE KEY BLOCK"
        # (note the " BLOCK" suffix). The prior regex's PGP branch
        # matched a non-existent "PGP PRIVATE KEY" form and missed the
        # real one. The anchored pattern's optional " BLOCK" matches.
        fixture = self.make_fixture(
            "standard-pem-pgp.md",
            VALID_METADATA
            + "\n\nExample block:\n\n-----BEGIN PGP PRIVATE KEY BLOCK-----\nlQOYBF\n-----END PGP PRIVATE KEY BLOCK-----\n",
        )
        result = run_linter("tools/lint-secrets-in-content.py", fixture)
        self.assertLinterFails(result, "Private key block")

    def test_pem_certificate_not_flagged_as_private_key(self) -> None:
        # Negative test: a CERTIFICATE block shares the PEM envelope but
        # is NOT a secret. The anchored pattern must not flag it (the
        # broad "any label" alternative would have). No other secret
        # pattern matches a bare certificate block, so the linter exits 0.
        fixture = self.make_fixture(
            "standard-pem-cert.md",
            VALID_METADATA
            + "\n\nExample block:\n\n-----BEGIN CERTIFICATE-----\nMIIDXTCCA\n-----END CERTIFICATE-----\n",
        )
        result = run_linter("tools/lint-secrets-in-content.py", fixture)
        self.assertEqual(
            result.returncode,
            0,
            f"a CERTIFICATE block must not be flagged as a private key.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_pem_public_key_not_flagged_as_private_key(self) -> None:
        # Negative test: a PUBLIC KEY block is not a secret and must not
        # be flagged. Locks in the precision of the anchored pattern.
        fixture = self.make_fixture(
            "standard-pem-public.md",
            VALID_METADATA
            + "\n\nExample block:\n\n-----BEGIN PUBLIC KEY-----\nMFkwEwYH\n-----END PUBLIC KEY-----\n",
        )
        result = run_linter("tools/lint-secrets-in-content.py", fixture)
        self.assertEqual(
            result.returncode,
            0,
            f"a PUBLIC KEY block must not be flagged as a private key.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_google_api_key_pattern_flagged(self) -> None:
        # Google API keys are AIza<35 chars>.
        fake_key = "AIza" + "A" * 35
        fixture = self.make_fixture(
            "standard-google-key.md",
            VALID_METADATA + f"\n\nExample: {fake_key}.\n",
        )
        result = run_linter("tools/lint-secrets-in-content.py", fixture)
        self.assertLinterFails(result)

    def test_stripe_live_key_pattern_flagged(self) -> None:
        # Stripe live secret keys start with sk_live_ and continue with
        # 24+ chars. Use a synthetic but pattern-matching value.
        fake_key = "sk_live_" + "A" * 28
        fixture = self.make_fixture(
            "standard-stripe-key.md",
            VALID_METADATA + f"\n\nExample: {fake_key}.\n",
        )
        result = run_linter("tools/lint-secrets-in-content.py", fixture)
        self.assertLinterFails(result)

    def test_gitlab_pat_pattern_flagged(self) -> None:
        # GitLab personal access tokens start with glpat- and are
        # 20+ alphanumeric/hyphen/underscore chars after.
        fake_token = "glpat-" + "A" * 22
        fixture = self.make_fixture(
            "standard-gitlab-token.md",
            VALID_METADATA + f"\n\nExample: {fake_token}.\n",
        )
        result = run_linter("tools/lint-secrets-in-content.py", fixture)
        self.assertLinterFails(result)


class PIIContentTests(LinterTestCase):
    """tools/lint-pii-in-content.py"""

    def test_ssn_pattern_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-ssn.md",
            VALID_METADATA + "\n\nContact ID example: 123-45-6789.\n",
        )
        result = run_linter("tools/lint-pii-in-content.py", fixture)
        self.assertLinterFails(result)

    def test_non_allowlisted_email_flagged(self) -> None:
        # Emails on example.com and the posluns.ca domain are
        # allowlisted; a plausible personal email on a non-allowlisted
        # domain should be caught.
        fixture = self.make_fixture(
            "standard-email.md",
            VALID_METADATA + "\n\nContact: jdoe@personal-domain-xyz.invalid.\n",
        )
        result = run_linter("tools/lint-pii-in-content.py", fixture)
        self.assertLinterFails(result)

    def test_public_ipv4_flagged(self) -> None:
        # Use a public IP outside RFC 1918, RFC 5737, and loopback ranges.
        # The IPv4 regex has a negative lookahead for trailing dots (to
        # avoid version-number false positives like "4.0.1.2"), so the
        # IP must not be immediately followed by a period.
        fixture = self.make_fixture(
            "standard-public-ip.md",
            VALID_METADATA + "\n\nForward DNS queries to the IP 8.8.8.8 server\n",
        )
        result = run_linter("tools/lint-pii-in-content.py", fixture)
        self.assertLinterFails(result, "IPv4")

    def test_us_phone_number_flagged(self) -> None:
        # 10-digit phone number with separators.
        fixture = self.make_fixture(
            "standard-phone.md",
            VALID_METADATA + "\n\nContact emergency line: 415-555-0123 ASAP.\n",
        )
        result = run_linter("tools/lint-pii-in-content.py", fixture)
        self.assertLinterFails(result, "phone")


class InternalReferencesTests(LinterTestCase):
    """tools/lint-internal-references.py"""

    def test_internal_tld_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-internal-host.md",
            VALID_METADATA + "\n\nDeploy to `db-primary.corp` and `api.internal`.\n",
        )
        result = run_linter("tools/lint-internal-references.py", fixture)
        self.assertLinterFails(result)

    def test_aws_region_identifier_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-aws-region.md",
            VALID_METADATA + "\n\nDeployed to us-east-1 with failover to eu-west-2.\n",
        )
        result = run_linter("tools/lint-internal-references.py", fixture)
        self.assertLinterFails(result, "AWS region")

    def test_non_documentation_cidr_flagged(self) -> None:
        # CIDR outside RFC 1918, RFC 5737, loopback, link-local. Use
        # 8.8.0.0/16 (Google DNS range; clearly public).
        fixture = self.make_fixture(
            "standard-bad-cidr.md",
            VALID_METADATA + "\n\nFirewall rules allow 8.8.0.0/16 inbound.\n",
        )
        result = run_linter("tools/lint-internal-references.py", fixture)
        self.assertLinterFails(result, "CIDR")

    def test_azure_region_identifier_flagged(self) -> None:
        # Azure regions use names like `eastus2`, `northeurope`, etc.
        fixture = self.make_fixture(
            "standard-azure-region.md",
            VALID_METADATA + "\n\nDeployed to eastus2 for low latency.\n",
        )
        result = run_linter("tools/lint-internal-references.py", fixture)
        self.assertLinterFails(result, "Azure region")

    def test_gcp_region_identifier_flagged(self) -> None:
        # GCP regions use names like `us-central1`, `europe-west2`, etc.
        # Different shape from AWS regions.
        fixture = self.make_fixture(
            "standard-gcp-region.md",
            VALID_METADATA + "\n\nDeployed to us-central1 in Iowa.\n",
        )
        result = run_linter("tools/lint-internal-references.py", fixture)
        self.assertLinterFails(result, "GCP region")


class ExternalLinkDomainsTests(LinterTestCase):
    """tools/lint-external-link-domains.py"""

    def test_non_allowlisted_external_domain_flagged(self) -> None:
        fixture = self.make_fixture(
            "standard-bad-external.md",
            VALID_METADATA + "\n\nSee [link](https://example-not-on-allowlist-xyz.invalid/page) for details.\n",
        )
        result = run_linter("tools/lint-external-link-domains.py", fixture)
        self.assertLinterFails(result)


class CrossDocNumbersTests(LinterTestCase):
    """tools/lint-cross-doc-numbers.py"""

    def test_gdpr_breach_notification_divergence_flagged(self) -> None:
        fixture_a = self.make_fixture(
            "standard-gdpr-72.md",
            VALID_METADATA + "\n\nUnder GDPR, breach notification is required within 72 hours.\n",
        )
        fixture_b = self.make_fixture(
            "standard-gdpr-48.md",
            VALID_METADATA.replace(
                "tests/tmp/standard-test.md", "tests/tmp/standard-gdpr-48.md"
            ) + "\n\nUnder GDPR, breach notification is required within 48 hours.\n",
        )
        result = run_linter("tools/lint-cross-doc-numbers.py", fixture_a, fixture_b)
        self.assertLinterFails(result, "GDPR-breach-notification-hours")


class AuditGateParityTests(LinterTestCase):
    """tools/lint-audit-gate-parity.py

    Tests both directions:

    1. The current real repository state passes (positive baseline).
    2. A synthetic source-set with engineered name drift is correctly
       flagged (negative test). The negative test uses ``--root`` to
       point the linter at a temp directory whose four surface files
       declare matching gate counts but a single mismatched gate name.
    """

    def test_current_surfaces_pass_parity(self) -> None:
        result = run_linter("tools/lint-audit-gate-parity.py")
        self.assertEqual(
            result.returncode,
            0,
            f"audit-gate-parity should pass on the current state.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_synthetic_name_drift_flagged(self) -> None:
        # Build a tiny four-surface fixture where everything aligns
        # except one gate name in the pre-commit hook (mismatch vs spec).
        synthetic_root = FIXTURE_DIR / "synthetic-parity-drift"
        import shutil
        if synthetic_root.exists():
            shutil.rmtree(synthetic_root)
        (synthetic_root / "governance").mkdir(parents=True)
        (synthetic_root / ".github" / "workflows").mkdir(parents=True)
        (synthetic_root / "tools").mkdir(parents=True)
        try:
            # Spec inventory (canonical): one row.
            (synthetic_root / "governance" / "specification-audit-programme.md").write_text(
                "# Audit Programme\n\n"
                "## 6. Gate inventory\n\n"
                "| # | Gate | Script |\n"
                "| --- | --- | --- |\n"
                "| 1 | Metadata audit | [`tools/lint-metadata.py`](../tools/lint-metadata.py) |\n\n"
                "## 7. Next section\n",
                encoding="utf-8",
            )
            # Workflow: matches spec.
            (synthetic_root / ".github" / "workflows" / "quality.yml").write_text(
                "name: Quality\n\n"
                "on: [push]\n\n"
                "jobs:\n"
                "  lint:\n"
                "    runs-on: ubuntu-latest\n"
                "    steps:\n"
                "      - name: Metadata audit\n"
                "        run: python3 tools/lint-metadata.py\n",
                encoding="utf-8",
            )
            # Runner: matches spec.
            (synthetic_root / "tools" / "run_all_audits.sh").write_text(
                '#!/usr/bin/env bash\n'
                'run_gate "Metadata audit" python3 tools/lint-metadata.py\n',
                encoding="utf-8",
            )
            # Pre-commit: WRONG NAME (introduces drift).
            (synthetic_root / ".pre-commit-config.yaml").write_text(
                "repos:\n"
                "  - repo: local\n"
                "    hooks:\n"
                "      - id: lint-metadata\n"
                "        name: Wrong Name For Metadata Audit\n"
                "        entry: python3 tools/lint-metadata.py\n",
                encoding="utf-8",
            )
            result = run_linter(
                "tools/lint-audit-gate-parity.py",
                "--root",
                str(synthetic_root),
            )
            self.assertLinterFails(result, "name drift")
        finally:
            shutil.rmtree(synthetic_root, ignore_errors=True)


class ChangelogLinkCoverageTests(LinterTestCase):
    """tools/lint-changelog-link-coverage.py"""

    def test_unlinked_file_reference_flagged(self) -> None:
        # Synthetic CHANGELOG-shape file with a backtick-wrapped file path
        # that is NOT wrapped in a markdown link.
        fixture = self.make_fixture(
            "fake-changelog.md",
            (
                "# Changelog\n\n"
                "## Phase test\n\n"
                "Refers to `tools/lint-metadata.py` without a link.\n"
            ),
        )
        result = run_linter("tools/lint-changelog-link-coverage.py", fixture)
        self.assertLinterFails(result, "unlinked-file-ref")


class ReviewCadenceTests(LinterTestCase):
    """tools/check-review-cadence.py

    Tests the date-driven cadence enforcement by overriding --as-of to a
    date far past today. The corpus contains many documents with annual
    or quarterly review cadences and Dates in 2026; an as-of in 2030
    should put many of them past the action threshold.
    """

    def test_far_future_as_of_flags_documents(self) -> None:
        result = run_linter(
            "tools/check-review-cadence.py",
            "--as-of",
            "2030-12-31",
        )
        self.assertLinterFails(result)

    def test_biannual_is_six_months_not_two_years(self) -> None:
        # Regression for Phase 23.48: 'biannual' means twice a year
        # (6 months), not every two years. Confused-with-biennial bug
        # would put document review schedules 18 months late.
        #
        # Test the FREQUENCY_MAP entry directly: the check-review-
        # cadence linter walks fixed domain directories and does not
        # accept a fixture-path argument, so we import the module and
        # assert the constant. The hyphenated filename requires
        # importlib.util.spec_from_file_location.
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "check_review_cadence",
            REPO_ROOT / "tools" / "check-review-cadence.py",
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        # FREQUENCY_MAP is a list of (phrase, months) tuples. Find
        # the biannual entry.
        biannual_months = None
        for phrase, months in mod.FREQUENCY_MAP:
            if phrase == "biannual":
                biannual_months = months
                break
        self.assertEqual(
            biannual_months,
            6,
            "biannual should map to 6 months (twice a year), not 24 "
            "(biennial). Otherwise next-review-due dates for biannual "
            "documents are 18 months too late.",
        )
        # Defence in depth: also confirm biennial is still 24.
        biennial_months = None
        for phrase, months in mod.FREQUENCY_MAP:
            if phrase == "biennial":
                biennial_months = months
                break
        self.assertEqual(biennial_months, 24, "biennial should map to 24 months")

    def test_project_governance_in_domains(self) -> None:
        # Regression for Sweep 45: per the maintainer decision to read
        # specification-project-governance-separation.md section 6.3's "full
        # corpus audit sweep" to include review-cadence, the .project-governance/
        # directory must be in this gate's DOMAINS so its non-README cadence-
        # bearing artefacts (the citation-verification registers and worklists,
        # e.g. the verifications register's 12-month re-verification) are
        # scheduled rather than unenforced. Gate 10 skips every README by design
        # (see iter_active_docs), so the directory's README is not cadence-
        # scheduled here; its date currency is covered by gate 31. The #336
        # migration originally omitted the directory (it walks a fixed domain
        # list); asserting the constant directly because the walk takes no
        # fixture path.
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "check_review_cadence",
            REPO_ROOT / "tools" / "check-review-cadence.py",
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertIn(
            ".project-governance",
            mod.DOMAINS,
            "gate 10 must scan .project-governance so the register's 12-month "
            "re-verification cadence is scheduled (gate 10 skips all READMEs "
            "by design, so the directory's README cadence is not scheduled here).",
        )


class CitationVerificationFreshnessTests(LinterTestCase):
    """tools/lint-citation-verification-freshness.py

    The Citation Verifications Register is currently empty (Q-batch
    verifications pending). The linter passes vacuously in that state.
    This test confirms the vacuous-pass behaviour. When the register
    starts carrying entries, a stronger positive test (using --today
    far in the future) can be added.
    """

    def test_empty_register_passes(self) -> None:
        result = run_linter("tools/lint-citation-verification-freshness.py")
        self.assertEqual(
            result.returncode,
            0,
            f"freshness linter should pass while the register is empty.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_root_override_with_missing_register_exits_2(self) -> None:
        # Phase 23.64: --root override + missing register → exit 2.
        synthetic_root = FIXTURE_DIR / "synthetic-root-no-verifications-register"
        synthetic_root.mkdir(parents=True, exist_ok=True)
        try:
            result = run_linter(
                "tools/lint-citation-verification-freshness.py",
                "--root",
                str(synthetic_root),
            )
            self.assertEqual(
                result.returncode,
                2,
                f"linter should exit 2 when --root names a directory "
                f"without governance/register-citation-verifications.md.\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            import shutil
            shutil.rmtree(synthetic_root, ignore_errors=True)


class ToolingProvenanceFreshnessTests(LinterTestCase):
    """tools/lint-tooling-provenance-freshness.py

    The AI Security Tooling Landscape Register has 55 entries dated
    2026-05-30. Overriding --today to a date far in the future puts
    every entry past the 6-month / 12-month cadence; the linter must
    fail.
    """

    def test_far_future_today_flags_entries(self) -> None:
        result = run_linter(
            "tools/lint-tooling-provenance-freshness.py",
            "--today",
            "2030-12-31",
        )
        self.assertLinterFails(result)

    def test_root_override_with_missing_register_exits_2(self) -> None:
        # Phase 23.64: --root override + missing register → exit 2.
        synthetic_root = FIXTURE_DIR / "synthetic-root-no-tooling-register"
        synthetic_root.mkdir(parents=True, exist_ok=True)
        try:
            result = run_linter(
                "tools/lint-tooling-provenance-freshness.py",
                "--root",
                str(synthetic_root),
            )
            self.assertEqual(
                result.returncode,
                2,
                f"linter should exit 2 when --root names a directory "
                f"without governance/register-ai-security-tooling-landscape.md.\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            import shutil
            shutil.rmtree(synthetic_root, ignore_errors=True)


class LibraryVersionMonotonicityTests(LinterTestCase):
    """tools/lint-library-version-monotonicity.py

    The linter normally compares the working-tree README.md against the
    prior committed state (via git). The ``--prior-readme`` flag lets
    the test pass a synthetic prior README so the version-comparison
    logic can be exercised without a git fixture.

    The document-versions check is git-coupled and remains untested by
    this regression suite.
    """

    def test_decreased_library_version_flagged(self) -> None:
        # Synthetic "prior" README claims a Library Version far higher
        # than the current working tree, so the linter must fail.
        prior_fixture = self.make_fixture(
            "fake-prior-readme.md",
            "# Fake README\n\n**Library Version:** 9999.12.99\n",
        )
        result = run_linter(
            "tools/lint-library-version-monotonicity.py",
            "--prior-readme",
            prior_fixture,
        )
        self.assertLinterFails(result, "decreased")

    def test_library_version_in_code_block_ignored(self) -> None:
        # Prior fixture has a high version inside a fenced code block
        # (which is a template / example, not the file's metadata) and
        # the real version outside the fence. The parser must skip the
        # in-fence value and use the real one. Without this skip,
        # template metadata blocks in CONTRIBUTING.md or worked-example.md
        # could be misread as the file's actual version (the failure
        # mode that bit Phase 0 on 2026-06-02).
        prior_fixture = self.make_fixture(
            "fake-prior-readme-fenced.md",
            (
                "# Fake README\n\n"
                "Example template (do not parse):\n\n"
                "```\n"
                "**Library Version:** 9999.99.99\n"
                "```\n\n"
                "**Library Version:** 2026.01.0\n"
            ),
        )
        result = run_linter(
            "tools/lint-library-version-monotonicity.py",
            "--prior-readme",
            prior_fixture,
        )
        # The current working tree is well above 2026.01.0, so if the
        # parser correctly skips the fenced 9999.99.99 the audit passes.
        self.assertEqual(
            result.returncode,
            0,
            msg=(
                f"linter should have passed (current >> 2026.01.0) but "
                f"appears to have read the fenced 9999.99.99 as the "
                f"prior version.\nstdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            ),
        )


class VersionDateConsistencyTests(LinterTestCase):
    """tools/lint-version-date-consistency.py

    The linter enforces two invariants between CHANGELOG.md and
    README.md. We exercise both with synthetic fixtures pointed at via
    the ``--changelog`` and ``--readme`` flags so the test is isolated
    from real repo state.
    """

    def test_date_version_month_mismatch_flagged(self) -> None:
        # CHANGELOG entry dated 2026-06-01 but version says 2026.05.144.
        # This is the exact failure mode the gate exists to catch.
        changelog_fixture = self.make_fixture(
            "fake-changelog-date-mismatch.md",
            (
                "# Changelog\n\n"
                "## 2026-06-01, Library Version 2026.05.144\n\n"
                "Stale month in the version.\n"
            ),
        )
        readme_fixture = self.make_fixture(
            "fake-readme-matching-stale.md",
            "# Fake README\n\n**Library Version:** 2026.05.144\n",
        )
        result = run_linter(
            "tools/lint-version-date-consistency.py",
            "--changelog",
            changelog_fixture,
            "--readme",
            readme_fixture,
        )
        self.assertLinterFails(result, "must match")

    def test_readme_changelog_version_drift_flagged(self) -> None:
        # CHANGELOG and date both say 2026.06.0 but README still records
        # 2026.05.144. This is the README-CHANGELOG drift case.
        changelog_fixture = self.make_fixture(
            "fake-changelog-drift.md",
            (
                "# Changelog\n\n"
                "## 2026-06-01, Library Version 2026.06.0\n\n"
                "Correct month-version pair.\n"
            ),
        )
        readme_fixture = self.make_fixture(
            "fake-readme-stale.md",
            "# Fake README\n\n**Library Version:** 2026.05.144\n",
        )
        result = run_linter(
            "tools/lint-version-date-consistency.py",
            "--changelog",
            changelog_fixture,
            "--readme",
            readme_fixture,
        )
        self.assertLinterFails(result, "must agree")

    def test_heading_with_pr_clause_accepted(self) -> None:
        # Heading shape from PR #38 forward: ", PR #N" suffix on the
        # heading. The gate must still parse the date and version.
        # Positive: heading with PR clause + matching README => pass.
        changelog_fixture = self.make_fixture(
            "fake-changelog-with-pr.md",
            (
                "# Changelog\n\n"
                "## 2026-06-19, Library Version 2026.06.25, PR #38\n\n"
                "Post-PR-clause heading.\n"
            ),
        )
        readme_fixture = self.make_fixture(
            "fake-readme-matching-with-pr.md",
            "# Fake README\n\n**Library Version:** 2026.06.25\n",
        )
        result = run_linter(
            "tools/lint-version-date-consistency.py",
            "--changelog",
            changelog_fixture,
            "--readme",
            readme_fixture,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"heading with PR clause should parse and pass.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_heading_without_pr_clause_still_accepted(self) -> None:
        # Historical headings predate the PR-clause convention; the
        # regex must still parse them.
        changelog_fixture = self.make_fixture(
            "fake-changelog-no-pr.md",
            (
                "# Changelog\n\n"
                "## 2026-06-01, Library Version 2026.06.0\n\n"
                "Pre-convention heading.\n"
            ),
        )
        readme_fixture = self.make_fixture(
            "fake-readme-matching-no-pr.md",
            "# Fake README\n\n**Library Version:** 2026.06.0\n",
        )
        result = run_linter(
            "tools/lint-version-date-consistency.py",
            "--changelog",
            changelog_fixture,
            "--readme",
            readme_fixture,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"heading without PR clause should still parse and pass.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_heading_with_pr_clause_date_mismatch_still_flagged(self) -> None:
        # Defence-in-depth: the PR clause must not paper over a real
        # date/version mismatch. Heading carries PR clause AND the
        # date YYYY-MM does not match the version YYYY.MM => fail.
        changelog_fixture = self.make_fixture(
            "fake-changelog-pr-mismatch.md",
            (
                "# Changelog\n\n"
                "## 2026-06-01, Library Version 2026.05.144, PR #99\n\n"
                "Stale month in the version with PR clause.\n"
            ),
        )
        readme_fixture = self.make_fixture(
            "fake-readme-stale-pr.md",
            "# Fake README\n\n**Library Version:** 2026.05.144\n",
        )
        result = run_linter(
            "tools/lint-version-date-consistency.py",
            "--changelog",
            changelog_fixture,
            "--readme",
            readme_fixture,
        )
        self.assertLinterFails(result, "must match")


class MetadataLineBreaksTests(LinterTestCase):
    """tools/lint-metadata-line-breaks.py

    The linter detects metadata blocks (consecutive ``**Field:**`` lines)
    whose non-last lines lack a Markdown hard-break marker, which causes
    GitHub to soft-wrap the block into a single paragraph. Both ``\\`` and
    two-trailing-spaces are accepted as valid markers. Fenced code blocks
    are skipped so templates that demonstrate metadata format are not
    false-positives.
    """

    def test_missing_hard_break_flagged(self) -> None:
        # Three metadata lines, none with a hard-break marker: 2 non-last
        # lines should be flagged. The block is OUTSIDE any code fence.
        fixture = self.make_fixture(
            "fake-missing-breaks.md",
            (
                "# Fake Document\n\n"
                "**Document Title:** Test\n"
                "**Document Type:** Standard\n"
                "**Version:** 1.0.0\n\n"
                "Body content here.\n"
            ),
        )
        result = run_linter("tools/lint-metadata-line-breaks.py", fixture)
        self.assertLinterFails(result, "missing-hard-break")

    def test_code_fence_metadata_not_flagged(self) -> None:
        # Same metadata block, but inside a fenced code region: must NOT
        # be flagged (templates demonstrating proper format do not need
        # hard-break markers because code-fence preserves line breaks).
        fixture = self.make_fixture(
            "fake-fenced-metadata.md",
            (
                "# Fake Document\n\n"
                "Template:\n\n"
                "```\n"
                "**Document Title:** Test\n"
                "**Document Type:** Standard\n"
                "**Version:** 1.0.0\n"
                "```\n\n"
                "Body content here.\n"
            ),
        )
        result = run_linter("tools/lint-metadata-line-breaks.py", fixture)
        self.assertEqual(
            result.returncode,
            0,
            msg=(
                "fenced template metadata should not be flagged; "
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            ),
        )


class StructureLinterTests(LinterTestCase):
    """tools/lint-structure.py

    The linter walks hardcoded domain directories and reads the
    canonical document-index register. To test in isolation, this
    class builds a tiny synthetic repository structure under a
    per-test temp directory and points the linter at it via ``--root``.

    The synthetic repo has just enough shape to exercise the linter:
    one ``governance/`` domain containing a register that references a
    non-existent file. The linter must flag the broken reference.
    """

    def _build_synthetic_repo(self, root: Path, broken_target: str) -> None:
        gov = root / "governance"
        gov.mkdir(parents=True, exist_ok=True)
        # Master index register links to a path that does not exist.
        (gov / "register-document-index-and-classification.md").write_text(
            "# Index\n\n"
            "| Domain | Type | Title | Path |\n"
            "| --- | --- | --- | --- |\n"
            f"| Governance | Register | Fake | [`{broken_target}`]({broken_target}) |\n",
            encoding="utf-8",
        )
        # Minimal governance README so the linter does not flag missing-README.
        (gov / "README.md").write_text(
            "# Governance README\n\n"
            f"| Type | Title | Path |\n"
            f"| --- | --- | --- |\n"
            f"| Register | Fake | [`{broken_target}`]({broken_target}) |\n",
            encoding="utf-8",
        )

    def test_broken_index_reference_flagged(self) -> None:
        # Build the synthetic repo inside the per-test fixture dir.
        synthetic_root = FIXTURE_DIR / "synthetic-repo"
        if synthetic_root.exists():
            import shutil
            shutil.rmtree(synthetic_root)
        synthetic_root.mkdir(parents=True)
        self._build_synthetic_repo(synthetic_root, "governance/does-not-exist.md")
        try:
            result = run_linter(
                "tools/lint-structure.py",
                "--root",
                str(synthetic_root),
            )
            self.assertLinterFails(result, "non-existent")
        finally:
            import shutil
            shutil.rmtree(synthetic_root, ignore_errors=True)


class OrphanDocumentsTests(LinterTestCase):
    """tools/lint-orphan-documents.py

    The linter walks the entire repository to build the inbound-reference
    graph and flags artefacts with zero inbound references. To trigger a
    finding, we place a fixture with a canonical metadata block in
    ``tests/tmp/`` (where no other document references it). The linter
    scans this directory by default (not on the exemption list) so the
    fixture appears in its artefact set and is flagged as orphan.

    The fixture's metadata gives it a Document Type and filename
    consistent with library conventions; that satisfies the artefact-
    detection criteria the linter uses.
    """

    def test_unreferenced_artefact_flagged(self) -> None:
        # The orphan-documents linter requires a canonical metadata
        # block for artefact detection. The fixture's Repository Path
        # points inside tests/tmp/ where no other document references
        # it.
        body = VALID_METADATA.replace(
            "tests/tmp/standard-test.md",
            "tests/tmp/standard-unreferenced-orphan.md",
        )
        self.make_fixture("standard-unreferenced-orphan.md", body)
        result = run_linter("tools/lint-orphan-documents.py")
        self.assertLinterFails(result, "standard-unreferenced-orphan.md")


class SkillDerivesFromTests(LinterTestCase):
    """tools/lint-skill-derives-from.py

    The audit verifies that every ``SKILL.md`` under
    ``dev-security/claude-rules/skills/`` declares a ``derives_from:``
    YAML frontmatter field whose value resolves to an existing file.
    Tests use ``--root`` to point the linter at a synthetic minimal
    source set with engineered errors so the detection logic can be
    exercised without touching the real corpus.
    """

    def _build_synthetic_root(self, skill_frontmatter: str, target_exists: bool) -> Path:
        import shutil

        synthetic_root = FIXTURE_DIR / "synthetic-skill-derives"
        if synthetic_root.exists():
            shutil.rmtree(synthetic_root)
        skill_dir = synthetic_root / "dev-security" / "claude-rules" / "skills" / "test-skill"
        skill_dir.mkdir(parents=True)
        rules_dir = synthetic_root / "dev-security" / "claude-rules" / "governance"
        rules_dir.mkdir(parents=True)
        if target_exists:
            (rules_dir / "test-rule.md").write_text(
                "# Test Rule\n\nSynthetic canonical rule.\n",
                encoding="utf-8",
            )
        (skill_dir / "SKILL.md").write_text(
            skill_frontmatter,
            encoding="utf-8",
        )
        return synthetic_root

    def test_missing_derives_from_flagged(self) -> None:
        import shutil

        synthetic_root = self._build_synthetic_root(
            skill_frontmatter=(
                "---\n"
                "name: test-skill\n"
                "description: A test skill with no derives_from field.\n"
                "---\n\n"
                "# Test Skill\n"
            ),
            target_exists=True,
        )
        try:
            result = run_linter(
                "tools/lint-skill-derives-from.py",
                "--root",
                str(synthetic_root),
            )
            self.assertLinterFails(result, "missing `derives_from:`")
        finally:
            shutil.rmtree(synthetic_root, ignore_errors=True)

    def test_broken_derives_from_target_flagged(self) -> None:
        import shutil

        synthetic_root = self._build_synthetic_root(
            skill_frontmatter=(
                "---\n"
                "name: test-skill\n"
                "description: A test skill pointing at a non-existent rule.\n"
                "derives_from: ../../governance/does-not-exist.md\n"
                "---\n\n"
                "# Test Skill\n"
            ),
            target_exists=False,
        )
        try:
            result = run_linter(
                "tools/lint-skill-derives-from.py",
                "--root",
                str(synthetic_root),
            )
            self.assertLinterFails(result, "does not exist")
        finally:
            shutil.rmtree(synthetic_root, ignore_errors=True)


class LintCommonHelperTests(unittest.TestCase):
    """lint_common.py shared helpers: parse_metadata_block, parse_iso_date,
    and the iter_non_code_lines fence semantics (GR-3 / GR-4)."""

    def _lint_common(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "lint_common_under_test", REPO_ROOT / "tools" / "lint_common.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_parse_metadata_block_fields_and_backslash(self) -> None:
        lc = self._lint_common()
        block = lc.parse_metadata_block(
            "# T\n\n**Version:** 1.0.0\\\n**Date:** 2026-07-01\\\n**Owner:** X\n"
        )
        self.assertEqual(block.fields["Version"], "1.0.0")
        self.assertEqual(block.fields["Date"], "2026-07-01")
        self.assertEqual(block.fields["Owner"], "X")
        self.assertEqual(block.raw_lines["Date"][0], 4)

    def test_parse_metadata_block_head_window(self) -> None:
        # A **Field:**-shaped line beyond the head window is body
        # prose (e.g. a documented placeholder), not metadata.
        lc = self._lint_common()
        text = "# T\n" + "filler\n" * 35 + "**Version:** 9.9.9\n"
        block = lc.parse_metadata_block(text)
        self.assertNotIn("Version", block.fields)

    def test_parse_metadata_block_first_occurrence_wins(self) -> None:
        lc = self._lint_common()
        block = lc.parse_metadata_block("**Date:** 2026-07-01\n**Date:** 2026-07-02\n")
        self.assertEqual(block.fields["Date"], "2026-07-01")

    def test_parse_iso_date_strict(self) -> None:
        lc = self._lint_common()
        self.assertIsNotNone(lc.parse_iso_date("2026-07-01"))
        self.assertIsNone(lc.parse_iso_date("2026-07-01 (draft)"))
        self.assertIsNone(lc.parse_iso_date("2026-13-01"))
        self.assertIsNone(lc.parse_iso_date("not-a-date"))

    def test_head_version_field_precedence(self) -> None:
        # GR-3 wave 2: `Version` wins, `Library Version` matches, and
        # `README Version` is a distinct field that never matches (the
        # retired trio regex's behaviour, centralized).
        lc = self._lint_common()
        self.assertEqual(lc.head_version("**Version:** 1.2.3\\\n"), "1.2.3")
        self.assertEqual(
            lc.head_version(
                "**Library Version:** 2026.07.100 (CalVer)\\\n"
                "**README Version:** 1.9.461\n"
            ),
            "2026.07.100 (CalVer)",
        )
        self.assertIsNone(lc.head_version("**README Version:** 1.9.461\n"))
        # The precedence proper: with BOTH fields present (Library Version
        # listed first), `Version` still wins, pinning name-precedence
        # over positional order.
        self.assertEqual(
            lc.head_version(
                "**Library Version:** 2026.07.100\\\n"
                "**Version:** 1.2.3\n"
            ),
            "1.2.3",
        )

    def test_head_version_empty_and_absent_out_of_scope(self) -> None:
        # An empty value and an absent field both return None (the trio's
        # in-scope rule: only a non-empty version brings a file in).
        lc = self._lint_common()
        self.assertIsNone(lc.head_version("**Version:**\n"))
        self.assertIsNone(lc.head_version("# Title\n\nNo metadata here.\n"))
        self.assertIsNone(lc.head_version(None))

    def test_head_version_head_window_only(self) -> None:
        # A Version-shaped line past the head window is body prose (a
        # documented placeholder), not metadata.
        lc = self._lint_common()
        text = "\n" * 35 + "**Version:** 9.9.9\n"
        self.assertIsNone(lc.head_version(text))

    def test_tilde_fence_toggles(self) -> None:
        # GR-4: a ~~~ fence must exclude its contents exactly as a
        # backtick fence does (previously it silently suppressed
        # nothing and a stray tilde fence was scanned as prose).
        lc = self._lint_common()
        lines = [l for _, l in lc.iter_non_code_lines("a\n~~~\nhidden\n~~~\nb\n")]
        self.assertEqual(lines, ["a", "b"])

    def test_backtick_fence_still_toggles(self) -> None:
        lc = self._lint_common()
        lines = [l for _, l in lc.iter_non_code_lines("a\n```\nhidden\n```\nb\n")]
        self.assertEqual(lines, ["a", "b"])


class DocumentDateStalenessTests(LinterTestCase):
    """tools/lint-document-date-staleness.py

    The audit verifies that every corpus markdown file with a Date
    metadata field has a Date no more than ``--max-lag-days`` behind
    the file's most-recent git commit date, with files committed
    before ``--baseline-date`` grandfathered. Tests build a synthetic
    minimal git repo under ``--root`` so the linter's detection logic
    can be exercised with engineered commit dates and metadata Dates,
    without touching the real corpus or its git history.
    """

    @staticmethod
    def _git(args: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
        # Always pass git config inline so the test does not depend on
        # the developer's global git identity.
        config = ["-c", "user.email=t@test", "-c", "user.name=Test"]
        subprocess.run(
            ["git", *config, *args],
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )

    def _build_synthetic_repo(
        self,
        *,
        metadata_date: str,
        commit_date: str,
        document_type: str = "Standard",
        document_basename: str = "standard-test.md",
        scan_subdir: str = "ai",
    ) -> Path:
        import shutil

        synthetic_root = FIXTURE_DIR / "synthetic-date-staleness"
        if synthetic_root.exists():
            shutil.rmtree(synthetic_root)
        scan_dir = synthetic_root / scan_subdir
        scan_dir.mkdir(parents=True)
        # Minimal metadata block: only the Date field needs to be
        # detectable by the linter; we still build a syntactically
        # plausible 13-field block so the file isn't malformed.
        body = (
            f"# Test Document\n\n"
            f"**Document Title:** Test Document\\\n"
            f"**Document Type:** {document_type}\\\n"
            f"**Version:** 1.0.0\\\n"
            f"**Date:** {metadata_date}\\\n"
            f"**Owner:** Test Owner\\\n"
            f"**Approving Authority:** Test Owner\\\n"
            f"**Related Documents:** None\\\n"
            f"**Classification:** Public\\\n"
            f"**Category:** Test\\\n"
            f"**Review Frequency:** Annual\\\n"
            f"**Repository Path:** "
            f"[`{scan_subdir}/{document_basename}`]({document_basename})\\\n"
            f"**Confidentiality:** Public\\\n"
            f"**License:** CC BY-SA 4.0\n\n"
            f"---\n\n## Purpose\n\nTest body.\n"
        )
        (scan_dir / document_basename).write_text(body, encoding="utf-8")
        self._git(["init", "-q", "-b", "main"], cwd=synthetic_root)
        self._git(["add", "."], cwd=synthetic_root)
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = commit_date
        env["GIT_COMMITTER_DATE"] = commit_date
        self._git(
            ["commit", "-q", "-m", "test commit"],
            cwd=synthetic_root,
            env=env,
        )
        return synthetic_root

    def test_stale_date_flagged(self) -> None:
        # Metadata Date 22 days behind the commit date and the commit
        # is at or after the baseline: must fail.
        import shutil

        synthetic_root = self._build_synthetic_repo(
            metadata_date="2026-05-28",
            commit_date="2026-06-19T12:00:00Z",
        )
        try:
            result = run_linter(
                "tools/lint-document-date-staleness.py",
                "--root",
                str(synthetic_root),
                "--baseline-date",
                "2026-06-19",
            )
            self.assertLinterFails(result, "lags the file's most-recent commit date")
        finally:
            shutil.rmtree(synthetic_root, ignore_errors=True)

    def test_fresh_date_passes(self) -> None:
        # Metadata Date matches commit date exactly: must pass (exit 0).
        import shutil

        synthetic_root = self._build_synthetic_repo(
            metadata_date="2026-06-19",
            commit_date="2026-06-19T12:00:00Z",
        )
        try:
            result = run_linter(
                "tools/lint-document-date-staleness.py",
                "--root",
                str(synthetic_root),
                "--baseline-date",
                "2026-06-19",
            )
            self.assertEqual(
                result.returncode,
                0,
                f"linter should pass on a fresh Date.\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(synthetic_root, ignore_errors=True)

    def test_malformed_date_is_finding_not_skip(self) -> None:
        # A PRESENT but malformed Date (trailing annotation) must be a
        # FINDING, not a silent skipped_no_date (the GR-3 fail-loud
        # migration; previously the strict line-end-anchored regex
        # silently exempted such a file from the staleness check).
        import shutil

        synthetic_root = self._build_synthetic_repo(
            metadata_date="2026-06-19 (draft)",
            commit_date="2026-06-19T12:00:00Z",
        )
        try:
            result = run_linter(
                "tools/lint-document-date-staleness.py",
                "--root",
                str(synthetic_root),
                "--baseline-date",
                "2026-06-19",
            )
            self.assertLinterFails(result, "malformed metadata Date")
        finally:
            shutil.rmtree(synthetic_root, ignore_errors=True)

    def test_pre_baseline_commit_grandfathered(self) -> None:
        # Commit predates the baseline date: file is grandfathered
        # even though its metadata Date is stale. Must pass.
        import shutil

        synthetic_root = self._build_synthetic_repo(
            metadata_date="2026-01-01",
            commit_date="2026-05-01T12:00:00Z",
        )
        try:
            result = run_linter(
                "tools/lint-document-date-staleness.py",
                "--root",
                str(synthetic_root),
                "--baseline-date",
                "2026-06-19",
            )
            self.assertEqual(
                result.returncode,
                0,
                f"linter should grandfather a pre-baseline commit.\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        finally:
            shutil.rmtree(synthetic_root, ignore_errors=True)

    def test_project_governance_in_default_scan_paths(self) -> None:
        # Regression for Sweep 45: the .project-governance/ directory is
        # audited-not-exempt per specification-project-governance-separation.md
        # section 6.3, which explicitly names "per-document version and date
        # currency". This gate is the date-currency check, so .project-governance
        # must be in its default scan set; the #336 migration originally missed
        # it (it walks an explicit allow-list, not exempt-minus-walk), so the
        # 7 moved files were silently skipped until this was fixed. Asserting
        # the constant directly, in the ReviewCadenceTests.FREQUENCY_MAP style,
        # because the default scan set is a fixed allow-list a fixture cannot
        # exercise.
        import importlib.util
        import sys

        tools_dir = str(REPO_ROOT / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        spec = importlib.util.spec_from_file_location(
            "lint_document_date_staleness",
            REPO_ROOT / "tools" / "lint-document-date-staleness.py",
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertIn(
            ".project-governance",
            mod.DEFAULT_SCAN_PATHS,
            "gate 31 must scan .project-governance (section 6.3 names "
            "date currency); dropping it silently skips the campaign artefacts.",
        )


class ClaudeRulesSyncTests(LinterTestCase):
    """tools/lint-claude-rules-sync.py

    The audit verifies that each project-local .claude/rules copy's body
    matches its dev-security/claude-rules pack source (after stripping
    the local copy's frontmatter and provenance comment), and that every
    local rule file is covered by the sync mapping. The live in-sync
    state must pass (subprocess test); drift detection and the
    completeness check are exercised in-process with a patched MIRROR_MAP
    against a synthetic root so the detection logic is verified without
    perturbing the real tree.
    """

    @staticmethod
    def _load_module():
        import importlib.util
        import sys

        tools_dir = str(REPO_ROOT / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        spec = importlib.util.spec_from_file_location(
            "lint_claude_rules_sync",
            str(REPO_ROOT / "tools" / "lint-claude-rules-sync.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    @staticmethod
    def _make_synthetic(local_body: str, source_body: str, extra_local: str | None = None):
        """Create a synthetic root with one mapped pair; return (root, map).

        The pair is keyed on the same relative paths the real MIRROR_MAP
        uses for secrets.md, so the synthetic local copy may carry a
        provenance comment while the source does not.
        """
        import shutil

        root = FIXTURE_DIR / "synthetic-claude-rules-sync"
        if root.exists():
            shutil.rmtree(root)
        local_rel = ".claude/rules/secrets.md"
        source_rel = "dev-security/claude-rules/core/secrets.md"
        (root / ".claude" / "rules").mkdir(parents=True)
        (root / "dev-security" / "claude-rules" / "core").mkdir(parents=True)
        (root / local_rel).write_text(local_body, encoding="utf-8")
        (root / source_rel).write_text(source_body, encoding="utf-8")
        if extra_local is not None:
            (root / ".claude" / "rules" / extra_local).write_text(
                "# Extra\n\nUnmapped local rule.\n", encoding="utf-8"
            )
        return root, {local_rel: source_rel}

    def test_current_state_passes(self) -> None:
        # The live repository state must be in sync (this is what every
        # other gate run assumes).
        result = run_linter("tools/lint-claude-rules-sync.py")
        self.assertEqual(
            result.returncode,
            0,
            f"claude-rules sync should pass on the current state.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_in_sync_pair_with_local_preamble_passes(self) -> None:
        # A local copy carrying a provenance comment whose body matches
        # the bare source must pass (exit 0).
        import shutil

        mod = self._load_module()
        root, fake_map = self._make_synthetic(
            local_body="<!-- Source: x -->\n\n# Title\n\nIdentical body.\n",
            source_body="# Title\n\nIdentical body.\n",
        )
        saved = mod.MIRROR_MAP
        try:
            mod.MIRROR_MAP = fake_map
            rc = mod.main(["--root", str(root)])
            self.assertEqual(rc, 0, "in-sync pair (modulo provenance) should pass")
        finally:
            mod.MIRROR_MAP = saved
            shutil.rmtree(root, ignore_errors=True)

    def test_body_drift_flagged(self) -> None:
        # Same preamble handling, but the bodies genuinely differ: fail.
        import shutil

        mod = self._load_module()
        root, fake_map = self._make_synthetic(
            local_body="<!-- Source: x -->\n\n# Title\n\nDRIFTED body.\n",
            source_body="# Title\n\nOriginal body.\n",
        )
        saved = mod.MIRROR_MAP
        try:
            mod.MIRROR_MAP = fake_map
            rc = mod.main(["--root", str(root)])
            self.assertEqual(rc, 1, "body drift between copy and source must fail")
        finally:
            mod.MIRROR_MAP = saved
            shutil.rmtree(root, ignore_errors=True)

    def test_unmapped_local_file_flagged(self) -> None:
        # An in-sync mapped pair, plus an extra local rule file that is
        # NOT in the map: the completeness check must fail (this is the
        # property that prevents the drift class recurring one level up).
        import shutil

        mod = self._load_module()
        root, fake_map = self._make_synthetic(
            local_body="# Title\n\nIdentical body.\n",
            source_body="# Title\n\nIdentical body.\n",
            extra_local="unmapped-rule.md",
        )
        saved = mod.MIRROR_MAP
        try:
            mod.MIRROR_MAP = fake_map
            rc = mod.main(["--root", str(root)])
            self.assertEqual(
                rc, 1, "an unmapped local rule file must fail the completeness check"
            )
        finally:
            mod.MIRROR_MAP = saved
            shutil.rmtree(root, ignore_errors=True)


class TodoStalenessTests(LinterTestCase):
    """tools/lint-todo-staleness.py"""

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: TODO.md at HEAD has no stale patterns.
        result = run_linter("tools/lint-todo-staleness.py")
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on HEAD; "
            f"TODO.md should have no stale patterns.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def _load_module(self):
        # Hyphenated filename; load via importlib.
        import importlib.util
        tools_dir = str(REPO_ROOT / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        spec = importlib.util.spec_from_file_location(
            "_lint_todo_staleness",
            REPO_ROOT / "tools/lint-todo-staleness.py",
        )
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_queued_pr_already_merged_detected(self) -> None:
        # Positive test: a TODO line marks PR #999 as "Next" while PR
        # #999 has merged. Use the module's check_file via tempfile.
        mod = self._load_module()
        fixture_dir = FIXTURE_DIR / "todo-staleness-merged"
        fixture_dir.mkdir(parents=True, exist_ok=True)
        try:
            path = fixture_dir / "TODO.md"
            path.write_text(
                "# TODO\n\n"
                "**Next, PR #999: do something important.**\n",
                encoding="utf-8",
            )
            # Pretend PR #999 has merged.
            findings = mod.check_file(path, merged={999}, latest=None)
            self.assertTrue(
                findings,
                f"linter should flag queued PR #999 as already-merged; "
                f"got findings={findings}",
            )
            self.assertIn("queued-PR-merged", findings[0])
        finally:
            import shutil
            shutil.rmtree(fixture_dir, ignore_errors=True)

    def test_queued_pr_not_yet_merged_passes(self) -> None:
        # Negative test: same line, but PR #999 has NOT merged. No finding.
        mod = self._load_module()
        fixture_dir = FIXTURE_DIR / "todo-staleness-not-merged"
        fixture_dir.mkdir(parents=True, exist_ok=True)
        try:
            path = fixture_dir / "TODO.md"
            path.write_text(
                "# TODO\n\n"
                "**Next, PR #999: do something important.**\n",
                encoding="utf-8",
            )
            findings = mod.check_file(path, merged=set(), latest=None)
            self.assertEqual(
                findings, [],
                f"linter should not flag a queued PR that has not "
                f"merged; got findings={findings}",
            )
        finally:
            import shutil
            shutil.rmtree(fixture_dir, ignore_errors=True)

    def test_sweep_cursor_behind_history_detected(self) -> None:
        # Positive test: TODO claims Sweep 5 iter 2 but history has Sweep
        # 11 iter 1. Should flag.
        mod = self._load_module()
        fixture_dir = FIXTURE_DIR / "todo-staleness-cursor"
        fixture_dir.mkdir(parents=True, exist_ok=True)
        try:
            path = fixture_dir / "TODO.md"
            path.write_text(
                "# TODO\n\n"
                "- **Last validation sweep**: Sweep 5 iteration 2.\n",
                encoding="utf-8",
            )
            findings = mod.check_file(
                path, merged=set(), latest=(11, 1)
            )
            self.assertTrue(
                findings,
                f"linter should flag cursor (5, 2) when history is "
                f"at (11, 1); got findings={findings}",
            )
            self.assertIn("sweep-cursor-stale", findings[0])
        finally:
            import shutil
            shutil.rmtree(fixture_dir, ignore_errors=True)

    def test_sweep_cursor_current_passes(self) -> None:
        # Negative test: cursor matches latest history row. No finding.
        mod = self._load_module()
        fixture_dir = FIXTURE_DIR / "todo-staleness-cursor-current"
        fixture_dir.mkdir(parents=True, exist_ok=True)
        try:
            path = fixture_dir / "TODO.md"
            path.write_text(
                "# TODO\n\n"
                "- **Last validation sweep**: Sweep 11 iteration 1.\n",
                encoding="utf-8",
            )
            findings = mod.check_file(
                path, merged=set(), latest=(11, 1)
            )
            self.assertEqual(
                findings, [],
                f"linter should not flag a current cursor; "
                f"got findings={findings}",
            )
        finally:
            import shutil
            shutil.rmtree(fixture_dir, ignore_errors=True)


class OvernightFileTests(LinterTestCase):
    """tools/lint-overnight-file.py"""

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: the overnight-pr.md file at HEAD is in stub form.
        result = run_linter("tools/lint-overnight-file.py")
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on HEAD; "
            f"the overnight-pr.md file should be in stub form.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def _load_module(self):
        import importlib.util
        tools_dir = str(REPO_ROOT / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        spec = importlib.util.spec_from_file_location(
            "_lint_overnight_file",
            REPO_ROOT / "tools/lint-overnight-file.py",
        )
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_status_regex_matches_stub(self) -> None:
        mod = self._load_module()
        text = "**Status:** stub\n"
        m = mod.STATUS_PATTERN.search(text)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "stub")

    def test_status_regex_matches_in_flight(self) -> None:
        mod = self._load_module()
        text = "**Status:** in-flight\n"
        m = mod.STATUS_PATTERN.search(text)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "in-flight")

    def test_status_regex_matches_done(self) -> None:
        mod = self._load_module()
        text = "**Status:** done\n"
        m = mod.STATUS_PATTERN.search(text)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "done")

    def test_valid_pass_statuses_includes_stub_and_in_flight(self) -> None:
        mod = self._load_module()
        self.assertIn("stub", mod.VALID_PASS_STATUSES)
        self.assertIn("in-flight", mod.VALID_PASS_STATUSES)

    def test_valid_fail_statuses_includes_done(self) -> None:
        mod = self._load_module()
        self.assertIn("done", mod.VALID_FAIL_STATUSES)


class SessionStateTests(LinterTestCase):
    """tools/lint-session-state.py (gate 63)

    Well-formedness of the session-concurrency lease: five required
    field lines, a valid Status value, a parseable UTC heartbeat, and
    status/branch coherence. All three status values pass when
    coherent (the interlock decision lives in the /resume step-0
    procedure, not in CI).
    """

    VALID_LEASE = (
        "# Session State (concurrency lease)\n\n"
        "**Active-session:** claude/example-branch\n\n"
        "**Status:** active\n\n"
        "**Last-heartbeat-UTC:** 2026-07-03T12:00:00Z\n\n"
        "**Current-task:** example task\n\n"
        "**Worker-dispatches:** none\n"
    )

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: the session-state.md lease at HEAD is well-formed.
        result = run_linter("tools/lint-session-state.py")
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on HEAD; "
            f"the session-state.md lease should be well-formed.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def _load_module(self):
        import importlib.util
        tools_dir = str(REPO_ROOT / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        spec = importlib.util.spec_from_file_location(
            "_lint_session_state",
            REPO_ROOT / "tools/lint-session-state.py",
        )
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_valid_lease_passes(self) -> None:
        mod = self._load_module()
        missing, invalid = mod.check_text(self.VALID_LEASE)
        self.assertEqual(missing, [])
        self.assertEqual(invalid, [])

    def test_released_lease_with_none_session_passes(self) -> None:
        mod = self._load_module()
        text = self.VALID_LEASE.replace(
            "**Active-session:** claude/example-branch",
            "**Active-session:** none",
        ).replace("**Status:** active", "**Status:** released")
        missing, invalid = mod.check_text(text)
        self.assertEqual(missing, [])
        self.assertEqual(invalid, [])

    def test_missing_field_line_reported(self) -> None:
        mod = self._load_module()
        text = self.VALID_LEASE.replace(
            "**Worker-dispatches:** none\n", ""
        )
        missing, invalid = mod.check_text(text)
        self.assertEqual(len(missing), 1)
        self.assertIn("Worker-dispatches", missing[0])

    def test_invalid_status_value_flagged(self) -> None:
        mod = self._load_module()
        text = self.VALID_LEASE.replace(
            "**Status:** active", "**Status:** paused"
        )
        missing, invalid = mod.check_text(text)
        self.assertEqual(missing, [])
        self.assertTrue(any("paused" in message for message in invalid))

    def test_malformed_heartbeat_flagged(self) -> None:
        mod = self._load_module()
        text = self.VALID_LEASE.replace(
            "**Last-heartbeat-UTC:** 2026-07-03T12:00:00Z",
            "**Last-heartbeat-UTC:** yesterday",
        )
        missing, invalid = mod.check_text(text)
        self.assertEqual(missing, [])
        self.assertTrue(any("yesterday" in message for message in invalid))

    def test_released_with_branch_incoherence_flagged(self) -> None:
        mod = self._load_module()
        text = self.VALID_LEASE.replace(
            "**Status:** active", "**Status:** released"
        )
        missing, invalid = mod.check_text(text)
        self.assertEqual(missing, [])
        self.assertTrue(
            any("released" in message for message in invalid)
        )

    def test_active_with_none_session_incoherence_flagged(self) -> None:
        mod = self._load_module()
        text = self.VALID_LEASE.replace(
            "**Active-session:** claude/example-branch",
            "**Active-session:** none",
        )
        missing, invalid = mod.check_text(text)
        self.assertEqual(missing, [])
        self.assertTrue(any("none" in message for message in invalid))

    def test_duplicate_field_line_flagged(self) -> None:
        mod = self._load_module()
        text = self.VALID_LEASE + "\n**Status:** released\n"
        missing, invalid = mod.check_text(text)
        self.assertEqual(missing, [])
        self.assertTrue(
            any("appears 2 times" in message for message in invalid)
        )

    def test_missing_field_and_value_error_both_reported(self) -> None:
        # A missing field must not suppress a coexisting value error
        # (the #611 sweep's I-1: both classes report in one run).
        mod = self._load_module()
        text = self.VALID_LEASE.replace(
            "**Worker-dispatches:** none\n", ""
        ).replace("**Status:** active", "**Status:** paused")
        missing, invalid = mod.check_text(text)
        self.assertEqual(len(missing), 1)
        self.assertTrue(any("paused" in message for message in invalid))


class CcmAicmCitationTests(LinterTestCase):
    """tools/lint-ccm-aicm-citations.py"""

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: every CCM/AICM citation in the corpus names a valid
        # domain and in-range control, and control-listing titles match the
        # authoritative catalogue.
        result = run_linter("tools/lint-ccm-aicm-citations.py")
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on HEAD; CCM/AICM citations "
            f"should all be valid.\nstdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}",
        )

    def test_invalid_domain_flagged(self) -> None:
        # 'GOV' is not a CCM v4.1 / AICM v1.1 domain (governance is GRC).
        fixture = self.make_fixture(
            "fake-ccm-gov.md",
            "# X\n\nMaps to CSA CCM v4.1 GOV-01 for governance.\n",
        )
        result = run_linter("tools/lint-ccm-aicm-citations.py", fixture)
        self.assertLinterFails(result, "invalid-ccm-domain")

    def test_out_of_range_control_flagged(self) -> None:
        # The IPY domain has only four controls (IPY-01..04).
        fixture = self.make_fixture(
            "fake-ccm-ipy.md",
            "# X\n\nMaps to IPY-05 for interoperability.\n",
        )
        result = run_linter("tools/lint-ccm-aicm-citations.py", fixture)
        self.assertLinterFails(result, "ccm-control-out-of-range")

    def test_title_mismatch_flagged(self) -> None:
        # A control-listing row titling MDS-01 with an unrelated title (the
        # catalogue MDS-01 is "Training Pipeline Security").
        fixture = self.make_fixture(
            "fake-ccm-title.md",
            "# X\n\n| Control ID | Control Title |\n| --- | --- |\n"
            "| MDS-01 | Quantum Teapot Calibration |\n",
        )
        result = run_linter("tools/lint-ccm-aicm-citations.py", fixture)
        self.assertLinterFails(result, "ccm-title-mismatch")

    def test_internal_model_gov_not_flagged(self) -> None:
        # Corpus-internal MODEL-GOV-NN / AI-GOV-NN identifiers are not CCM
        # citations and must not be policed.
        fixture = self.make_fixture(
            "fake-internal.md",
            "# X\n\n**MODEL-GOV-01:** internal control. AI-GOV-03 too.\n",
        )
        result = run_linter("tools/lint-ccm-aicm-citations.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"corpus-internal MODEL-GOV/AI-GOV IDs should not be flagged.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_cross_catalogue_title_flagged(self) -> None:
        # Section-aware check: I&S-07 under a CSA CCM section titled with the
        # AICM variant ("Migration to Hosted Environments") cites the wrong
        # catalogue's title (CCM v4.1.0 I&S-07 is "Migration to Cloud
        # Environments"). The two titles share content words, so the
        # conservative content-word check cannot catch it; the divergent-title
        # check must.
        fixture = self.make_fixture(
            "fake-ccm-cross-catalogue.md",
            "# X\n\n## CSA CCM v4.1 control mapping\n\n"
            "| Control ID | Control Title |\n| --- | --- |\n"
            "| I&S-07 | Migration to Hosted Environments |\n",
        )
        result = run_linter("tools/lint-ccm-aicm-citations.py", fixture)
        self.assertLinterFails(result, "ccm-title-cross-catalogue")

    def test_correct_catalogue_title_not_flagged(self) -> None:
        # False-positive guard for the divergent-title check: I&S-07 under a
        # CSA CCM section titled with the CORRECT CCM variant must pass.
        fixture = self.make_fixture(
            "fake-ccm-correct-catalogue.md",
            "# X\n\n## CSA CCM v4.1 control mapping\n\n"
            "| Control ID | Control Title |\n| --- | --- |\n"
            "| I&S-07 | Migration to Cloud Environments |\n",
        )
        result = run_linter("tools/lint-ccm-aicm-citations.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"the correct CCM-section title for I&S-07 must not be flagged.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_bare_domain_code_in_ccm_context_flagged(self) -> None:
        # Check 4: a bare superseded/fabricated domain code (no -NN suffix) on a
        # line that names the matrices is flagged (the family-list residual
        # shape Sweep 36 found).
        fixture = self.make_fixture(
            "fake-ccm-bare-family.md",
            "# X\n\nMaps to the CSA CCM v4.1 IVS and NET families.\n",
        )
        result = run_linter("tools/lint-ccm-aicm-citations.py", fixture)
        self.assertLinterFails(result, "ccm-bare-domain-code")

    def test_bare_domain_code_under_ccm_section_flagged(self) -> None:
        # Check 4: a bare bad code in a domain-keyed crosswalk row under a CSA
        # CCM section is flagged even though the row line itself does not name
        # the matrix (the reverse-crosswalk residual shape).
        fixture = self.make_fixture(
            "fake-ccm-bare-section.md",
            "# X\n\n## CSA CCM v4.1 (selected domains)\n\n"
            "| GOV Governance, Risk Management, Compliance | docs | note |\n",
        )
        result = run_linter("tools/lint-ccm-aicm-citations.py", fixture)
        self.assertLinterFails(result, "ccm-bare-domain-code")

    def test_bare_code_rename_note_not_flagged(self) -> None:
        # False-positive guard: a historical rename-note legitimately names the
        # old code while describing its replacement (the glossary I&S entry).
        fixture = self.make_fixture(
            "fake-ccm-rename-note.md",
            "# X\n\n| **I&S** | (CSA CCM domain) Infrastructure Security. "
            "Renamed from the v4.0 IVS domain in CCM v4.1.0. |\n",
        )
        result = run_linter("tools/lint-ccm-aicm-citations.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a CCM rename-note naming the old code must not be flagged.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_dotnet_and_currency_not_flagged(self) -> None:
        # False-positive guards: '.NET' on a CCM-context line (leading dot) and
        # currency 'AUD' outside any CCM context must both pass.
        fixture = self.make_fixture(
            "fake-ccm-dotnet-aud.md",
            "# X\n\nThe CSA CCM guidance applies to .NET and ASP.NET services.\n\n"
            "## Penalties\n\nFines up to AUD 50 million apply.\n",
        )
        result = run_linter("tools/lint-ccm-aicm-citations.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"'.NET' in CCM context and currency 'AUD' must not be flagged.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


class MatrixControlCodeTests(LinterTestCase):
    """tools/lint-matrix-control-codes.py"""

    HEADER = (
        "| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 "
        "| NIST CSF 2.0 | CTPAT |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
    )

    def _matrix(self, ccm: str, iso: str, nist: str) -> str:
        return (
            "# X\n\n## Section\n\n"
            + self.HEADER
            + f"| Gov | Doc | path | {ccm} | {iso} | {nist} | N/A |\n"
        )

    def test_runs_clean_on_matrix_at_head(self) -> None:
        # Smoke test: the live matrix's ISO and NIST framework columns are
        # all well-formed at HEAD.
        result = run_linter("tools/lint-matrix-control-codes.py")
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on the live matrix; ISO/NIST "
            f"codes should be valid.\nstdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}",
        )

    def test_iso_annex_out_of_range_flagged(self) -> None:
        # ISO 27001:2022 Annex A theme A.5 has 37 controls; A.5.99 is out of range.
        fixture = self.make_fixture(
            "fake-matrix-iso-range.md",
            self._matrix("GRC-01", "A.5.99", "GV.OC"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertLinterFails(result, "iso-annex-range")

    def test_iso_invalid_theme_flagged(self) -> None:
        # Annex A has only themes A.5-A.8; A.9 does not exist.
        fixture = self.make_fixture(
            "fake-matrix-iso-theme.md",
            self._matrix("GRC-01", "A.9.1", "GV.OC"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertLinterFails(result, "iso-annex-theme")

    def test_iso_clause_out_of_range_flagged(self) -> None:
        # Management-system clauses run §4-§10; §11 does not exist.
        fixture = self.make_fixture(
            "fake-matrix-iso-clause.md",
            self._matrix("GRC-01", "§11.2", "GV.OC"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertLinterFails(result, "iso-clause-range")

    def test_nist_invalid_function_flagged(self) -> None:
        # 'XX' is not one of the six CSF 2.0 Core Function prefixes.
        fixture = self.make_fixture(
            "fake-matrix-nist-func.md",
            self._matrix("GRC-01", "A.5.1", "XX.YY"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertLinterFails(result, "nist-function")

    def test_nist_malformed_flagged(self) -> None:
        # A token that is not FUNCTION.CATEGORY shape.
        fixture = self.make_fixture(
            "fake-matrix-nist-malformed.md",
            self._matrix("GRC-01", "A.5.1", "notacode"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertLinterFails(result, "nist-malformed")

    def test_valid_codes_not_flagged(self) -> None:
        # False-positive guard: a valid Annex A code, a valid clause, and two
        # real CSF 2.0 Categories must all pass. (PR.PS and GV.OC are members
        # of the authoritative 22-Category set.)
        fixture = self.make_fixture(
            "fake-matrix-valid.md",
            self._matrix("GRC-01", "A.5.1, A.8.34, §6.1", "GV.OC, PR.PS"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"valid ISO/NIST tokens must not be flagged.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_nist_csf11_category_flagged(self) -> None:
        # PR.IP is a CSF 1.1 category redistributed in 2.0; it is well-formed
        # (PR is a valid Function prefix) but is not a CSF 2.0 Category, so the
        # membership check must flag it with a relocation note.
        fixture = self.make_fixture(
            "fake-matrix-nist-csf11.md",
            self._matrix("GRC-01", "A.5.1", "PR.IP"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertLinterFails(result, "nist-category")

    def test_nist_relocated_supply_chain_category_flagged(self) -> None:
        # ID.SC (CSF 1.1 Supply Chain Risk Management) became GV.SC in 2.0;
        # well-formed but not a 2.0 Category.
        fixture = self.make_fixture(
            "fake-matrix-nist-idsc.md",
            self._matrix("GRC-01", "A.5.19", "ID.SC"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertLinterFails(result, "nist-category")

    def test_nist_unknown_category_flagged(self) -> None:
        # A well-formed token with a valid Function prefix but a category that
        # exists in no CSF edition (GV.ZZ) is flagged by the membership check.
        fixture = self.make_fixture(
            "fake-matrix-nist-unknown-cat.md",
            self._matrix("GRC-01", "A.5.1", "GV.ZZ"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertLinterFails(result, "nist-category")

    def test_ccm_aicm_only_code_flagged(self) -> None:
        # CCM/AICM catalogue confusion: MDS-01 is a real AICM v1.1.0 code (the
        # AI-only Model Security domain) but NOT a CCM v4.1.0 code, so it must
        # be flagged in the "CSA CCM v4.1" column. This is the matrix-scoped
        # catalogue-discipline check the corpus-wide CSA citation gate (which
        # validates against the AICM-wins union) does not enforce. (Added when
        # gate 49 was tightened to police the CCM column; supersedes the prior
        # "CCM not policed here" test, which encoded the pre-tightening scope.)
        fixture = self.make_fixture(
            "fake-matrix-ccm-aicm.md",
            self._matrix("MDS-01", "A.5.1", "GV.OC"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertLinterFails(result, "ccm-aicm-confusion")

    def test_ccm_invalid_code_flagged(self) -> None:
        # A code-shaped token that is neither a CCM v4.1 nor an AICM code
        # (GOV-99: GOV is a non-existent domain) is flagged as an unknown CCM
        # code.
        fixture = self.make_fixture(
            "fake-matrix-ccm-unknown.md",
            self._matrix("GOV-99", "A.5.1", "GV.OC"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertLinterFails(result, "ccm-unknown")

    def test_ccm_valid_code_and_na_not_flagged(self) -> None:
        # False-positive guard: a valid CCM v4.1 code and an N/A cell both pass.
        fixture = self.make_fixture(
            "fake-matrix-ccm-valid.md",
            self._matrix("GRC-01, AIS-04", "A.5.1", "GV.OC"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"valid CCM v4.1 codes must not be flagged.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    AICM_HEADER = (
        "| Domain | Document Title | Path | CSA CCM v4.1 | CSA AICM v1.1 "
        "| ISO 27001:2022 | NIST CSF 2.0 | CTPAT |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
    )

    def _matrix_with_aicm(self, ccm: str, aicm: str, iso: str, nist: str) -> str:
        return (
            "# X\n\n## Section\n\n"
            + self.AICM_HEADER
            + f"| Gov | Doc | path | {ccm} | {aicm} | {iso} | {nist} | N/A |\n"
        )

    def test_aicm_only_code_and_na_not_flagged(self) -> None:
        # False-positive guard for the CSA AICM v1.1 column: AICM-only
        # (AI-specific) codes pass. MDS-06 (Adversarial Attack Analysis) and
        # GRC-10 (AI Impact Assessment) are is_aicm_only; the CCM column carries
        # the CCM base code, the AICM column the AI-specific delta.
        fixture = self.make_fixture(
            "fake-matrix-aicm-valid.md",
            self._matrix_with_aicm("GRC-01", "MDS-06, GRC-10", "A.5.1", "GV.OC"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"valid AICM-only codes must not be flagged.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_aicm_na_not_flagged(self) -> None:
        # The common case: a non-AI row's AICM cell is N/A and must pass.
        fixture = self.make_fixture(
            "fake-matrix-aicm-na.md",
            self._matrix_with_aicm("GRC-01", "N/A", "A.5.1", "GV.OC"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"an N/A AICM cell must pass.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_aicm_ccm_base_code_flagged(self) -> None:
        # Catalogue discipline, symmetric to ccm-aicm-confusion: IAM-01 is a
        # CCM v4.1 base control (also restated in AICM v1.1, which extends CCM),
        # so it belongs in the "CSA CCM v4.1" column, NOT the AICM column, which
        # carries only the AI-specific delta.
        fixture = self.make_fixture(
            "fake-matrix-aicm-ccmbase.md",
            self._matrix_with_aicm("GRC-01", "IAM-01", "A.5.1", "GV.OC"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertLinterFails(result, "aicm-is-ccm-base")

    def test_aicm_unknown_code_flagged(self) -> None:
        # A code-shaped token that is no real CSA control (ZZ-99) in the AICM
        # column is flagged as an unknown AICM code.
        fixture = self.make_fixture(
            "fake-matrix-aicm-unknown.md",
            self._matrix_with_aicm("GRC-01", "ZZ-99", "A.5.1", "GV.OC"),
        )
        result = run_linter("tools/lint-matrix-control-codes.py", fixture)
        self.assertLinterFails(result, "aicm-unknown")


class DocumentControlCodeTests(LinterTestCase):
    """tools/lint-document-control-codes.py (per-document NIST CSF 2.0 codes)"""

    SCRIPT = "tools/lint-document-control-codes.py"

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: the live corpus carries no CSF-1.1-era NIST codes in
        # per-document framework tables (the DD-12 carriers were migrated in
        # PR #371). Added when the scanner was wired as gate 54.
        result = run_linter(self.SCRIPT)
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on the live corpus; "
            f"per-document NIST CSF codes should all be valid CSF 2.0.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def _row_doc(self, label: str, code_cell: str, notes_cell: str | None = None) -> str:
        # A framework-as-row table: the framework name is the first cell of a
        # body row; codes live in the code cell (cell 1); notes (if any) in cell 2.
        if notes_cell is None:
            return (
                "# X\n\n## Framework alignment\n\n"
                "| Framework | Reference |\n| --- | --- |\n"
                f"| {label} | {code_cell} |\n"
            )
        return (
            "# X\n\n## Framework alignment\n\n"
            "| Framework | Code | Notes |\n| --- | --- | --- |\n"
            f"| {label} | {code_cell} | {notes_cell} |\n"
        )

    def _col_doc(self, nist_body_cell: str) -> str:
        # A framework-as-column table: a NIST CSF column header, then a body
        # row whose NIST column holds the code.
        return (
            "# X\n\n## Control mapping\n\n"
            "| Control Area | NIST CSF | CSA CCM v4.1 |\n| --- | --- | --- |\n"
            f"| Some control | {nist_body_cell} | LOG-01 |\n"
        )

    def test_framework_row_carrier_flagged(self) -> None:
        # ID.SC (CSF 1.1 Supply Chain Risk Management; became GV.SC) in the
        # code cell of a NIST CSF framework row must be flagged.
        fixture = self.make_fixture(
            "fake-doc-row-carrier.md",
            self._row_doc("NIST CSF 2.0", "GV.SC Supply Chain; ID.SC Supply Chain Cybersecurity"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertLinterFails(result, "nist-csf1-carrier")

    def test_framework_column_carrier_flagged(self) -> None:
        # RS.RP-1 in a NIST CSF column cell: the -1 subcategory suffix is
        # stripped and RS.RP (CSF 1.1 Response Planning) is flagged.
        fixture = self.make_fixture(
            "fake-doc-col-carrier.md",
            self._col_doc("Respond: RS.RP-1"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertLinterFails(result, "nist-csf1-carrier")

    def test_notes_cell_carrier_not_flagged(self) -> None:
        # Precision guard: a CSF 1.1 code that appears only in a *notes* cell
        # as part of a rename note must NOT be flagged (the operative code in
        # the code cell, PR.AA, is valid).
        fixture = self.make_fixture(
            "fake-doc-notes-note.md",
            self._row_doc(
                "NIST Cybersecurity Framework 2.0",
                "PR.AA (Identity Management, Authentication, and Access Control)",
                "Note: PR.AC was the CSF 1.1 subcategory; CSF 2.0 renamed it to PR.AA.",
            ),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a CSF 1.1 code in a notes cell must not be flagged.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_valid_codes_not_flagged(self) -> None:
        # False-positive guard: valid CSF 2.0 Categories, including a
        # subcategory-suffixed one (DE.CM-7 -> DE.CM), must all pass.
        fixture = self.make_fixture(
            "fake-doc-valid.md",
            self._col_doc("Detect: DE.CM-7"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertEqual(
            result.returncode, 0,
            f"valid CSF 2.0 codes must not be flagged.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_nist_sp_row_not_scanned(self) -> None:
        # A "NIST SP 800-53" framework row is not a CSF row; its control
        # families (SR, SA-9) must not be scanned as CSF codes.
        fixture = self.make_fixture(
            "fake-doc-nist-sp.md",
            self._row_doc("NIST SP 800-53 Rev. 5", "SA-9 External System Services; SR Supply Chain"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a NIST SP 800-53 row must not be scanned as a CSF table.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_unknown_category_flagged(self) -> None:
        # A well-formed FUNCTION.CATEGORY with a valid Function prefix but a
        # category in no CSF edition (GV.ZZ) is flagged as unknown.
        fixture = self.make_fixture(
            "fake-doc-unknown-cat.md",
            self._row_doc("NIST CSF 2.0", "GV.ZZ"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertLinterFails(result, "nist-unknown-category")


class BookkeepingParityTests(LinterTestCase):
    """tools/lint-bookkeeping-parity.py (gate 50)"""

    def _load_module(self):
        # The linter imports `lint_common`, so tools/ must be on sys.path
        # before exec (the filename has hyphens, so a bare import won't work).
        import importlib.util
        tools_dir = str(REPO_ROOT / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        spec = importlib.util.spec_from_file_location(
            "_lint_bookkeeping_parity",
            REPO_ROOT / "tools/lint-bookkeeping-parity.py",
        )
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: the live bookkeeping records satisfy parity at HEAD.
        result = run_linter("tools/lint-bookkeeping-parity.py")
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on HEAD; the live "
            f"validate-pr / improvement-log / TODO records should be in "
            f"parity.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_missing_validate_pr_row_flagged(self) -> None:
        # PR #11 is in-window (inception 10, max 12) but has no validate-pr
        # row and is not a known handoff: must flag.
        mod = self._load_module()
        findings = mod.qa_cadence_findings(
            {10, 11, 12}, {10: "normal"}, {10, 11},
            inception=10, known_handoff=frozenset(),
        )
        self.assertTrue(findings, "missing validate-pr row should flag")
        self.assertIn("no row", findings[0])
        self.assertIn("#11", findings[0])

    def test_missing_retro_row_flagged(self) -> None:
        # PR #11 has a normal validate-pr row but no retro row: must flag.
        mod = self._load_module()
        findings = mod.qa_cadence_findings(
            {10, 11, 12}, {10: "normal", 11: "normal"}, {10},
            inception=10, known_handoff=frozenset(),
        )
        self.assertTrue(findings, "missing retro row should flag")
        self.assertIn("/retro", findings[0])
        self.assertIn("#11", findings[0])

    def test_handoff_row_exempt_from_both(self) -> None:
        # PR #11 is a handoff PR (validate-pr + retro both legitimately
        # absent): must NOT flag despite no retro row.
        mod = self._load_module()
        findings = mod.qa_cadence_findings(
            {10, 11, 12}, {10: "normal", 11: "handoff"}, {10},
            inception=10, known_handoff=frozenset(),
        )
        self.assertEqual(findings, [], f"handoff PR must be exempt; got {findings}")

    def test_subsumption_row_satisfies_no_retro_required(self) -> None:
        # PR #11's QA was subsumed by a later sweep: validate-pr satisfied,
        # no retro required: must NOT flag.
        mod = self._load_module()
        findings = mod.qa_cadence_findings(
            {10, 11, 12}, {10: "normal", 11: "subsumption"}, {10},
            inception=10, known_handoff=frozenset(),
        )
        self.assertEqual(findings, [], f"subsumption PR must pass; got {findings}")

    def test_highest_pr_batch_lag_exempt(self) -> None:
        # The single highest-numbered PR (#12) is exempt even with no rows:
        # its rows batch into the next, not-yet-existent PR.
        mod = self._load_module()
        findings = mod.qa_cadence_findings(
            {10, 11, 12}, {10: "normal", 11: "normal"}, {10, 11},
            inception=10, known_handoff=frozenset(),
        )
        self.assertEqual(findings, [], f"highest PR must be exempt; got {findings}")

    def test_known_handoff_no_row_allowlist_exempt(self) -> None:
        # A pre-convention handoff PR with no row at all is exempt via the
        # allowlist.
        mod = self._load_module()
        findings = mod.qa_cadence_findings(
            {10, 11, 12}, {10: "normal"}, {10},
            inception=10, known_handoff=frozenset({11}),
        )
        self.assertEqual(findings, [], f"allowlisted handoff must pass; got {findings}")

    def test_findings_cell_handoff_classification(self) -> None:
        # The parser classifies a SKIPPED-handoff Findings cell as 'handoff'
        # and a SUBSUMED cell as 'subsumption', from field 4. The
        # maintainer-exception marker is recognized in BOTH spellings (the
        # -ised rows predate the Canadian-spelling harmonization; new rows
        # follow the house -ized convention; regex widened 2026-07-02).
        mod = self._load_module()
        text = (
            "| Date | PR | Touched | Findings | Hot-fix | Detail | Summary |\n"
            "|---|---|---|---|---|---|---|\n"
            "| 2026-06-25 | 99 | x | **`/validate-pr` SKIPPED (handoff-PR "
            "exception, loop-break)** | none | - | s |\n"
            "| 2026-06-25 | 98 | x | **NOT run; SUBSUMED by Sweep 42** | none | - | s |\n"
            "| 2026-06-25 | 97 | x | **0 findings (clean)** | none | - | s |\n"
            "| 2026-06-25 | 96 | x | **maintainer-authorised exception: "
            "carved out with rationale** | none | - | s |\n"
            "| 2026-06-25 | 95 | x | **maintainer-authorized exception: "
            "carved out with rationale** | none | - | s |\n"
        )
        status = mod.parse_validate_pr_status(text)
        self.assertEqual(status.get(99), "handoff")
        self.assertEqual(status.get(98), "subsumption")
        self.assertEqual(status.get(97), "normal")
        self.assertEqual(status.get(96), "subsumption")
        self.assertEqual(status.get(95), "subsumption")

    def test_todo_strikethrough_bullet_flagged(self) -> None:
        # A whole backlog bullet struck through is a rotation failure.
        mod = self._load_module()
        findings = mod.todo_rotation_findings(
            "# TODO\n\n- ~~FR-99: do the thing (shipped)~~\n"
        )
        self.assertTrue(findings, "struck-through bullet should flag")
        self.assertIn("strikethrough-on-bullet", findings[0])

    def test_todo_status_done_flagged(self) -> None:
        mod = self._load_module()
        findings = mod.todo_rotation_findings(
            "# TODO\n\n- **FR-99**: do the thing. Status: completed\n"
        )
        self.assertTrue(findings, "Status: completed should flag")
        self.assertIn("status-completed", findings[0])

    def test_todo_inline_strikethrough_in_open_item_not_flagged(self) -> None:
        # Inline strikethrough marking completed sub-steps within a still-open
        # item (the FR-167 batch sequence) must NOT flag: the bullet content
        # does not BEGIN with the strikethrough.
        mod = self._load_module()
        findings = mod.todo_rotation_findings(
            "# TODO\n\n- **FR-167 (H, L)**: smallest-first: ~~risk 15~~ -> "
            "~~dev-security 17~~ -> resilience 22.\n"
        )
        self.assertEqual(
            findings, [],
            f"inline progress strikethrough in an open item must not flag; "
            f"got {findings}",
        )

    def test_todo_backticked_convention_reference_not_flagged(self) -> None:
        # The maintenance note describing the convention ("no `[done]`
        # suffixes") references the marker inside a code span: must NOT flag.
        mod = self._load_module()
        findings = mod.todo_rotation_findings(
            "# TODO\n\n- When an item is completed, delete it (no "
            "strikethroughs, no `[done]` suffixes) and add to DONE.\n"
        )
        self.assertEqual(
            findings, [],
            f"backticked convention reference must not flag; got {findings}",
        )

    def test_todo_lowercase_shipped_in_open_item_not_flagged(self) -> None:
        # Descriptive lowercase "shipped in #275" inside an open item is not a
        # self-completion marker (uppercase SHIPPED is the precision lever).
        mod = self._load_module()
        findings = mod.todo_rotation_findings(
            "# TODO\n\n- **FR-167**: batch 1 shipped in #275; batch 2 in flight.\n"
        )
        self.assertEqual(
            findings, [],
            f"descriptive lowercase 'shipped in #N' must not flag; got {findings}",
        )

    def test_version_history_parity_matching_row_not_flagged(self) -> None:
        # Check 4: metadata Version present as a history row: must NOT flag.
        mod = self._load_module()
        files = [(
            "x.md",
            "**Version:** 1.2.3\\\n\n## Version history\n\n"
            "| V | Date |\n|---|---|\n| 1.2.3 | 2026-01-01 |\n",
        )]
        self.assertEqual(
            mod.version_history_parity_findings(files), [],
            "a metadata Version with a matching history row must not flag",
        )

    def test_version_history_parity_missing_row_flagged(self) -> None:
        # Check 4: metadata Version absent from the history table: must flag.
        mod = self._load_module()
        files = [(
            "y.md",
            "**Version:** 1.2.4\\\n\n## Version history\n\n"
            "| V | Date |\n|---|---|\n| 1.2.3 | 2026-01-01 |\n",
        )]
        findings = mod.version_history_parity_findings(files)
        self.assertTrue(findings, "missing paired history row should flag")
        self.assertIn("version-history-parity", findings[0])
        self.assertIn("1.2.4", findings[0])

    def test_version_history_parity_no_table_ignored(self) -> None:
        # Check 4: a versioned file with NO `## Version history` table is out
        # of scope: must NOT flag (the check is scoped to files with both).
        mod = self._load_module()
        files = [("z.md", "**Version:** 9.9.9\\\n\nNo history table here.\n")]
        self.assertEqual(
            mod.version_history_parity_findings(files), [],
            "a file without a Version history table is out of scope",
        )

    def test_version_history_parity_tolerates_extra_historical_rows(self) -> None:
        # Check 4: history rows with no current metadata match (the normal
        # historical rows) are tolerated; only the metadata Version must match.
        mod = self._load_module()
        files = [(
            "x.md",
            "**Version:** 1.3.0\\\n\n## Version history\n\n| V | Date |\n|---|---|\n"
            "| 1.3.0 | 2026-02-01 |\n| 1.2.0 | 2026-01-01 |\n| 1.1.0 | 2025-12-01 |\n",
        )]
        self.assertEqual(
            mod.version_history_parity_findings(files), [],
            "extra historical rows must be tolerated",
        )

    def test_worker_provenance_wellformed_marker_not_flagged(self) -> None:
        # Check 3: a marker naming an inbox/<worker-id>/ delivery path is
        # well-formed: must NOT flag.
        mod = self._load_module()
        text = (
            "## 2026-07-03, Library Version 2026.07.100, PR #612\n\n"
            "Lead paragraph.\n\n"
            "**Worker provenance:** inbox/w-2026-07-03-a/MANIFEST.md, "
            "validated at apply-time per the research-assistant discipline.\n"
        )
        self.assertEqual(
            mod.worker_provenance_findings(text), [],
            "a marker naming an inbox delivery path must not flag",
        )

    def test_worker_provenance_pathless_marker_flagged(self) -> None:
        # Check 3: a marker with no inbox/<worker-id>/ path is malformed.
        mod = self._load_module()
        text = (
            "## 2026-07-03, Library Version 2026.07.100, PR #612\n\n"
            "**Worker provenance:** worker research applied, trust me.\n"
        )
        findings = mod.worker_provenance_findings(text)
        self.assertTrue(findings, "a pathless marker should flag")
        self.assertIn("inbox/<worker-id>/", findings[0])

    def test_worker_provenance_no_markers_no_findings(self) -> None:
        # Check 3: entries with no markers produce no findings (prose
        # mentioning workers without the marker line is out of scope).
        mod = self._load_module()
        text = (
            "## 2026-07-03, Library Version 2026.07.100, PR #612\n\n"
            "A worker delivered research to the inbox and it was applied.\n"
        )
        self.assertEqual(mod.worker_provenance_findings(text), [])

    def test_worker_provenance_bullet_form_marker_validated(self) -> None:
        # Check 3: the mirror's natural list-bullet authoring form is
        # validated too (the #612 verifier's F2): well-formed passes,
        # pathless flags.
        mod = self._load_module()
        good = "- **Worker provenance:** inbox/w-2026-07-03-a/MANIFEST.md\n"
        self.assertEqual(mod.worker_provenance_findings(good), [])
        bad = "- **Worker provenance:** applied from a delivery, path lost.\n"
        findings = mod.worker_provenance_findings(bad)
        self.assertTrue(findings, "a pathless bullet marker should flag")

    def test_worker_provenance_value_on_next_line_flagged(self) -> None:
        # Check 3: the value must be on the SAME line as the marker (the
        # #612 verifier's F4); a bare marker line flags rather than
        # capturing the following line.
        mod = self._load_module()
        text = (
            "**Worker provenance:**\n"
            "inbox/w-2026-07-03-a/MANIFEST.md\n"
        )
        findings = mod.worker_provenance_findings(text)
        self.assertTrue(findings, "a value-less marker line should flag")


class WorkingProseHygieneTests(LinterTestCase):
    """tools/lint-working-prose-hygiene.py (gate 51)"""

    def test_prose_em_dash_flagged(self) -> None:
        fixture = self.make_fixture(
            "working-prose-em-dash.md",
            "# Working note\n\nThe quick brown fox — jumped over the lazy dog.\n",
        )
        result = run_linter("tools/lint-working-prose-hygiene.py", fixture)
        self.assertLinterFails(result, "prose-dash")

    def test_prose_en_dash_flagged(self) -> None:
        fixture = self.make_fixture(
            "working-prose-en-dash.md",
            "# Working note\n\nThe range 2024–2026 carries an en-dash in prose.\n",
        )
        result = run_linter("tools/lint-working-prose-hygiene.py", fixture)
        self.assertLinterFails(result, "prose-dash")

    def test_code_span_dash_not_flagged(self) -> None:
        # A dash inside an inline code span is content, not prose; allowed.
        fixture = self.make_fixture(
            "working-codespan-dash.md",
            "# Working note\n\nThe regex `[–—]` matches an en or em dash.\n",
        )
        result = run_linter("tools/lint-working-prose-hygiene.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"code-span dash must not flag.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_fenced_block_dash_not_flagged(self) -> None:
        # A dash inside a fenced code block is skipped (iter_non_code_lines).
        fixture = self.make_fixture(
            "working-fenced-dash.md",
            "# Working note\n\n```\nsed -e 's/—/-/'  # em dash in a code fence\n```\n",
        )
        result = run_linter("tools/lint-working-prose-hygiene.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"fenced-block dash must not flag.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


class ScanScopeParityTests(LinterTestCase):
    """tools/lint-scan-scope-parity.py (gate 52)

    The gate scans a tools-style directory for ``*.py`` files that
    enumerate the audited-domain run as standalone string literals. It is
    pointed at an isolated temporary directory (not the shared fixture
    dir) so a stray ``.py`` fixture from another test cannot contaminate
    the glob. The gate imports ``AUDITED_DOMAIN_DIRS`` from the real
    ``tools/lint_common.py`` (its own directory is on ``sys.path``), so
    the temp directory needs only the file under test.
    """

    _HARDCODED_RUN = (
        "PATHS = [\n"
        '    "ai",\n'
        '    "architecture",\n'
        '    "compliance",\n'
        '    "dev-security",\n'
        '    "governance",\n'
        '    "operations",\n'
        '    "privacy",\n'
        '    "resilience",\n'
        '    "risk",\n'
        '    "security",\n'
        '    "supply-chain",\n'
        "]\n"
    )

    _DERIVED_RUN = (
        "from lint_common import AUDITED_DOMAIN_DIRS\n"
        'PATHS = ["README.md", *AUDITED_DOMAIN_DIRS]\n'
    )

    def test_hardcoded_domain_run_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "lint-hardcoded.py").write_text(
                self._HARDCODED_RUN, encoding="utf-8"
            )
            result = run_linter("tools/lint-scan-scope-parity.py", d)
            self.assertLinterFails(result, "enumerates the domain run")

    def test_derived_run_not_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "lint-derived.py").write_text(
                self._DERIVED_RUN, encoding="utf-8"
            )
            result = run_linter("tools/lint-scan-scope-parity.py", d)
            self.assertEqual(
                result.returncode, 0,
                f"a deriving linter must not flag.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )


class DirectionalDependencyTests(LinterTestCase):
    """tools/lint-directional-dependency.py (gate 53)

    The gate is pointed at an isolated temporary directory so a corpus
    document carrying a markdown link into ``.project-governance/`` can be
    detected without depending on the live corpus (which is clean). The
    ``.project-governance`` path-component test fires on the resolved
    target regardless of where the scan root lives.
    """

    def test_corpus_to_project_link_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "note.md").write_text(
                "# Note\n\nSee [the register](.project-governance/register.md).\n",
                encoding="utf-8",
            )
            result = run_linter("tools/lint-directional-dependency.py", d)
            self.assertLinterFails(result, "corpus-to-project link")

    def test_relative_parent_link_flagged(self) -> None:
        # A ``../.project-governance/`` shape resolves into the directory too.
        with tempfile.TemporaryDirectory() as d:
            sub = Path(d) / "sub"
            sub.mkdir()
            (sub / "deep.md").write_text(
                "# Sub\n\nSee [reg](../.project-governance/x.md).\n",
                encoding="utf-8",
            )
            result = run_linter("tools/lint-directional-dependency.py", str(sub))
            self.assertLinterFails(result, "corpus-to-project link")

    def test_ordinary_link_not_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "clean.md").write_text(
                "# Clean\n\nSee [the index](register-document-index.md) and "
                "[the spec](../governance/specification-master-project.md).\n",
                encoding="utf-8",
            )
            result = run_linter("tools/lint-directional-dependency.py", d)
            self.assertEqual(
                result.returncode, 0,
                f"an ordinary corpus link must not flag.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )

    def test_fenced_block_link_not_flagged(self) -> None:
        # A link-like token inside a fenced code block is documentation, skipped.
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "fenced.md").write_text(
                "# Fenced\n\n```\n[reg](.project-governance/register.md)\n```\n",
                encoding="utf-8",
            )
            result = run_linter("tools/lint-directional-dependency.py", d)
            self.assertEqual(
                result.returncode, 0,
                f"a fenced-block link must not flag.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )


class RetentionConsistencyTests(LinterTestCase):
    """tools/lint-retention-consistency.py (gate 55)

    The gate is pointed at an isolated temporary repo root (``--root``) holding
    a minimal Data Retention Schedule register and the eight procedures it is
    cross-referenced with (seven distinct files: the privacy-impact procedure
    serves both the PIA and AI-IA pairs), so a deliberate retention drift can
    be detected without depending on the live corpus (which is clean). The
    fixture tree mirrors the LIVE ``RETENTION_CHECKS`` set, including the
    composed register values (7 years, or 5 years post-decommission, whichever
    is longer) that compare on their leading floor figure.
    """

    REGISTER_REL = "governance/register-data-retention-schedule.md"
    PROCS = {
        "compliance/procedure-capa.md": "CAPA records",
        "compliance/standard-internal-audit.md": "Internal audit reports",
        "compliance/procedure-control-testing.md": "Control testing evidence",
        "privacy/procedure-privacy-impact-and-cross-border-transfer.md": (
            "Privacy impact assessments / AI Impact Assessments"
        ),
        "privacy/procedure-data-protection-and-privacy-breach-response.md": (
            "Privacy breach notifications"
        ),
        "ai/procedure-ai-audit.md": "AI audit reports",
        "supply-chain/procedure-supplier-audit.md": "Supplier audit reports",
    }

    def _write_tree(
        self,
        d: str,
        *,
        capa_proc_years: int = 7,
        capa_anchor: bool = True,
        pia_proc_years: int = 7,
    ) -> None:
        root = Path(d)
        for sub in ("governance", "compliance", "privacy", "ai", "supply-chain"):
            (root / sub).mkdir(parents=True, exist_ok=True)
        register = (
            "# Data Retention Schedule\n\n"
            "| Record category | Retention period | Basis |\n"
            "|---|---|---|\n"
            "| CAPA records | 7 years after closure | Quality management |\n"
            "| Internal audit reports | 7 years | ISO 19011 |\n"
            "| Control testing evidence | 7 years | Audit support |\n"
            "| Privacy impact assessments | 7 years, or 5 years after associated "
            "system decommission, whichever is longer | GDPR; PIPEDA |\n"
            "| Privacy breach notifications | 7 years | GDPR; PIPEDA |\n"
            "| AI Impact Assessments | 7 years, or 5 years after associated "
            "system decommission, whichever is longer | EU AI Act |\n"
            "| AI audit reports | 7 years, or 5 years after the associated "
            "system's decommission, whichever is longer | ISO 42001 |\n"
            "| Supplier audit reports | 7 years | Compliance support |\n"
        )
        (root / self.REGISTER_REL).write_text(register, encoding="utf-8")
        bodies = {
            "compliance/procedure-capa.md": (
                "# CAPA\n\nAll CAPA records must be "
                + (f"retained for a minimum of **{capa_proc_years} years**" if capa_anchor else "kept for **7 years**")
                + " from the CAPA closure date.\n"
            ),
            "compliance/standard-internal-audit.md": (
                "# Internal Audit\n\nAll audit working papers must be retained for "
                "a minimum of **7 years** from the date of the final report.\n"
            ),
            "compliance/procedure-control-testing.md": (
                "# Control Testing\n\nEvidence is retained for a minimum of 7 years "
                "per the records-retention standard.\n"
            ),
            # One procedure serves both the PIA and AI-IA pairs (the live
            # corpus shape); its composed statement compares on the leading
            # floor figure.
            "privacy/procedure-privacy-impact-and-cross-border-transfer.md": (
                "# Privacy Impact\n\nAll records retained for a minimum of "
                f"**{pia_proc_years} years, or 5 years after the associated "
                "system's decommission, whichever is longer** (matching the "
                "retention schedule register).\n"
            ),
            "privacy/procedure-data-protection-and-privacy-breach-response.md": (
                "# Breach Response\n\nAll breach evidence must be retained for a "
                "minimum of 7 years, consistent with the retention schedule.\n"
            ),
            "ai/procedure-ai-audit.md": (
                "# AI Audit\n\n5.4 Reports are retained for a minimum of 7 years "
                "in the compliance document repository, per the audit-records "
                "floor.\n"
            ),
            "supply-chain/procedure-supplier-audit.md": (
                "# Supplier Audit\n\nSupplier Audit Reports and their supporting "
                "evidence are retained for a minimum of 7 years, per the "
                "audit-records floor.\n"
            ),
        }
        for rel, body in bodies.items():
            (root / rel).write_text(body, encoding="utf-8")

    def test_consistent_tree_passes(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            self._write_tree(d)
            result = run_linter("tools/lint-retention-consistency.py", "--root", d)
            self.assertEqual(
                result.returncode, 0,
                f"a consistent register/procedure tree must pass.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )

    def test_retention_mismatch_flagged(self) -> None:
        # The CAPA procedure drifts to 5 years while the register row stays 7.
        with tempfile.TemporaryDirectory() as d:
            self._write_tree(d, capa_proc_years=5)
            result = run_linter("tools/lint-retention-consistency.py", "--root", d)
            self.assertLinterFails(result, "MISMATCH")

    def test_missing_citation_flagged(self) -> None:
        # The CAPA procedure no longer carries the retained-for-a-minimum-of anchor.
        with tempfile.TemporaryDirectory() as d:
            self._write_tree(d, capa_anchor=False)
            result = run_linter("tools/lint-retention-consistency.py", "--root", d)
            self.assertLinterFails(result, "retained for a minimum of")

    def test_composed_row_mismatch_on_leading_floor_flagged(self) -> None:
        # The privacy-impact procedure's leading floor drifts to 5 years while
        # the composed register rows (PIA and AI-IA) still lead with 7: the
        # comparison is on the FIRST period figure on each side, so both
        # composed pairs must flag.
        with tempfile.TemporaryDirectory() as d:
            self._write_tree(d, pia_proc_years=5)
            result = run_linter("tools/lint-retention-consistency.py", "--root", d)
            self.assertLinterFails(result, "MISMATCH")
            self.assertIn("2 retention-consistency issue(s)", result.stdout)

    def test_missing_procedure_file_flagged_gracefully(self) -> None:
        # A renamed / moved procedure must yield the graceful "cannot read" finding,
        # not an uncaught FileNotFoundError traceback (read_text_safe catches only
        # UnicodeDecodeError, so the linter guards the missing-file case explicitly).
        with tempfile.TemporaryDirectory() as d:
            self._write_tree(d)
            (Path(d) / "compliance/procedure-capa.md").unlink()
            result = run_linter("tools/lint-retention-consistency.py", "--root", d)
            self.assertLinterFails(result, "cannot read procedure")
            self.assertNotIn(
                "Traceback", result.stderr,
                f"missing procedure must be a graceful finding, not a crash.\nstderr:\n{result.stderr}",
            )


class BareNormativeShallTests(LinterTestCase):
    """tools/lint-bare-normative-shall.py (gate 56)

    Flags a bare normative ``shall`` in authored prose (the FR-44
    ``shall``->``must`` convention) while preserving three classes: a
    backticked ``shall`` word-reference, a hyphenated identifier embedding
    ``shall`` (the gate-9 filename), and a verbatim quote (fenced code or
    Markdown blockquote).
    """

    def test_bare_normative_shall_flagged(self) -> None:
        fixture = self.make_fixture(
            "bare-shall.md",
            "# Doc\n\nThe organization shall implement the controls.\n",
        )
        result = run_linter("tools/lint-bare-normative-shall.py", fixture)
        self.assertLinterFails(result, "shall")

    def test_backticked_shall_word_reference_not_flagged(self) -> None:
        fixture = self.make_fixture(
            "backtick-shall.md",
            "# Doc\n\nNo library `shall` operates without an accountable role.\n",
        )
        result = run_linter("tools/lint-bare-normative-shall.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a backticked `shall` word-reference must not be flagged.\nstdout:\n{result.stdout}",
        )

    def test_hyphenated_filename_token_not_flagged(self) -> None:
        fixture = self.make_fixture(
            "filename-shall.md",
            "# Doc\n\nSee [`lint-shall-near-uncertainty.py`](../tools/lint-shall-near-uncertainty.py).\n",
        )
        result = run_linter("tools/lint-bare-normative-shall.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a hyphenated identifier embedding 'shall' must not be flagged.\nstdout:\n{result.stdout}",
        )

    def test_blockquote_verbatim_shall_not_flagged(self) -> None:
        fixture = self.make_fixture(
            "blockquote-shall.md",
            "# Doc\n\n> Verbatim source extract: the supplier shall comply with the standard.\n",
        )
        result = run_linter("tools/lint-bare-normative-shall.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a bare 'shall' in a verbatim blockquote must not be flagged.\nstdout:\n{result.stdout}",
        )

    def test_must_not_flagged(self) -> None:
        fixture = self.make_fixture(
            "must-only.md",
            "# Doc\n\nThe organization must implement the controls.\n",
        )
        result = run_linter("tools/lint-bare-normative-shall.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"the harmonized 'must' form must not be flagged.\nstdout:\n{result.stdout}",
        )


class TodoMarkedDoneTests(LinterTestCase):
    """tools/lint-todo-marked-done.py (gate 57)

    Flags a TODO backlog item that marks ITSELF done in place (a Markdown
    strikethrough span, a ``[done]`` / ``[completed]`` tag, or a
    ``Status: completed`` / ``Status: done`` field) instead of being
    deleted and rotated to ``.working/DONE.md``. A bare ``SHIPPED`` word is
    deliberately NOT flagged (it appears in legitimate open-item prose); a
    backticked mention of any marker is not flagged (inline code stripped).
    """

    def test_strikethrough_item_flagged(self) -> None:
        fixture = self.make_fixture(
            "todo-strike.md",
            "# TODO\n\n- ~~**FR-9**: write the thing~~ done in #500\n",
        )
        result = run_linter("tools/lint-todo-marked-done.py", fixture)
        self.assertLinterFails(result, "strikethrough")

    def test_done_tag_flagged(self) -> None:
        fixture = self.make_fixture(
            "todo-donetag.md",
            "# TODO\n\n- **P-1.2**: refactor the helper [done]\n",
        )
        result = run_linter("tools/lint-todo-marked-done.py", fixture)
        self.assertLinterFails(result, "done")

    def test_status_completed_flagged(self) -> None:
        fixture = self.make_fixture(
            "todo-status.md",
            "# TODO\n\n- **FR-4**: build the gate (Status: completed)\n",
        )
        result = run_linter("tools/lint-todo-marked-done.py", fixture)
        self.assertLinterFails(result, "Status")

    def test_shipped_in_open_multipart_prose_not_flagged(self) -> None:
        fixture = self.make_fixture(
            "todo-shipped-prose.md",
            "# TODO\n\n- **FR-167**: the AICM column SHIPPED in PR-B; the "
            "extension **SHIPPED** (PR-C). Remaining: gap-fill keeps this open.\n",
        )
        result = run_linter("tools/lint-todo-marked-done.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a bare 'SHIPPED' in open multi-part item prose must not be flagged.\nstdout:\n{result.stdout}",
        )

    def test_backticked_marker_mention_not_flagged(self) -> None:
        fixture = self.make_fixture(
            "todo-backtick-marker.md",
            "# TODO\n\n- Design note: a self-marked item uses strikethrough "
            "`~~`, a `[done]` suffix, or a `Status: completed` field.\n",
        )
        result = run_linter("tools/lint-todo-marked-done.py", fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a backticked mention of a marker must not be flagged.\nstdout:\n{result.stdout}",
        )


class DocumentIsoAnnexATests(LinterTestCase):
    """tools/lint-document-iso-annex-a.py (gate 58)

    Per-document ISO/IEC 27001:2022 Annex A validity: flags a non-existent
    Annex A control, a non-2022 theme, an out-of-range or inverted range, or
    an out-of-range clause, but only inside an ISO 27001:2022-labelled table
    cell. Theme-only refs and valid ranges pass; a bare section number in
    prose (the document's own section) is never read as an ISO clause.
    """

    SCRIPT = "tools/lint-document-iso-annex-a.py"

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: the live corpus carries no invalid ISO 27001:2022 Annex
        # A codes in per-document framework tables. Added when the scanner was
        # wired as gate 58.
        result = run_linter(self.SCRIPT)
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on the live corpus; "
            f"per-document ISO Annex A codes should all be valid 2022 codes.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def _row_doc(self, label: str, code_cell: str, notes_cell: str | None = None) -> str:
        # Framework-as-row: the framework name is the first cell; codes live in
        # the code cell (cell 1); notes (if any) in cell 2.
        if notes_cell is None:
            return (
                "# X\n\n## Framework alignment\n\n"
                "| Framework | Reference |\n| --- | --- |\n"
                f"| {label} | {code_cell} |\n"
            )
        return (
            "# X\n\n## Framework alignment\n\n"
            "| Framework | Code | Notes |\n| --- | --- | --- |\n"
            f"| {label} | {code_cell} | {notes_cell} |\n"
        )

    def _col_doc(self, iso_body_cell: str) -> str:
        # Framework-as-column: an ISO 27001:2022 column header, then a body row
        # whose ISO column holds the code.
        return (
            "# X\n\n## Control mapping\n\n"
            "| Control Area | ISO/IEC 27001:2022 | NIST CSF |\n| --- | --- | --- |\n"
            f"| Some control | {iso_body_cell} | GV.OC |\n"
        )

    def test_nonexistent_control_flagged(self) -> None:
        # A.8.99 is past A.8's 34 controls: out of range.
        fixture = self.make_fixture(
            "iso-doc-oor.md", self._row_doc("ISO/IEC 27001:2022", "A.8.99"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertLinterFails(result, "iso-annex-range")

    def test_non_2022_theme_flagged(self) -> None:
        # A.9 is a 2013-edition theme; the 2022 themes are A.5-A.8.
        fixture = self.make_fixture(
            "iso-doc-2013.md", self._row_doc("ISO/IEC 27001:2022", "A.9.2"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertLinterFails(result, "iso-annex-theme")

    def test_clause_out_of_range_flagged(self) -> None:
        # Management-system clauses run §4-§10; §12 is out of range.
        fixture = self.make_fixture(
            "iso-doc-clause.md", self._col_doc("§12"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertLinterFails(result, "iso-clause-range")

    def test_inverted_range_flagged(self) -> None:
        # A same-theme range whose endpoints are inverted (high to low).
        fixture = self.make_fixture(
            "iso-doc-badrange.md", self._row_doc("ISO/IEC 27001:2022", "A.8.21 to A.8.20"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertLinterFails(result, "iso-annex-range")

    def test_valid_range_not_flagged(self) -> None:
        # False-positive guard: a valid same-theme range, including the
        # "drop the A. and theme" short form on the second endpoint.
        fixture = self.make_fixture(
            "iso-doc-validrange.md",
            self._row_doc("ISO/IEC 27001:2022", "A.8.20 to 21: Network controls"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a valid Annex A range must not be flagged.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_theme_only_and_valid_codes_not_flagged(self) -> None:
        # False-positive guard: a whole-theme reference (A.5), a valid control
        # (A.8.1), and a valid clause (§6) all pass.
        fixture = self.make_fixture(
            "iso-doc-valid.md",
            self._row_doc("ISO/IEC 27001:2022", "A.5; A.8.1; §6"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertEqual(
            result.returncode, 0,
            f"theme-only refs, valid codes, and valid clauses must not be flagged.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_prose_section_number_not_scanned(self) -> None:
        # The critical precision rule: a bare section number in document prose
        # (the document's OWN section, not an ISO clause) is never scanned.
        fixture = self.make_fixture(
            "iso-doc-prose.md",
            "# X\n\n## Scope\n\nThe controls in §12 of this policy apply org-wide.\n",
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a bare section number in prose must not be read as an ISO clause.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_non_iso_row_not_scanned(self) -> None:
        # A non-ISO framework row carrying out-of-range-looking tokens must not
        # be scanned as ISO (the row is not ISO 27001:2022-labelled).
        fixture = self.make_fixture(
            "iso-doc-nonrow.md",
            self._row_doc("NIST SP 800-53 Rev. 5", "AC-99; §12"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a non-ISO framework row must not be scanned as an ISO table.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


class GuardrailCadenceTests(LinterTestCase):
    """tools/lint-guardrail-cadence.py (gate 60)

    The gate compares the live machinery inventory (spec section-6 gate rows,
    pack governance rules, pack SKILLs, commands) against the as-of inventory
    token in the newest guardrail-review history row, warning below the drift
    threshold and failing at/above it; a missing or token-less record fails
    closed (the un-honoured record convention is the defect class).
    """

    HISTORY_REL = ".working/guardrail-reviews/history.md"

    def _write_tree(
        self,
        d: str,
        *,
        gates: int = 3,
        recorded: str = "inventory 3 gates / 2 rules / 2 skills / 1 command",
        with_row: bool = True,
    ) -> None:
        root = Path(d)
        (root / ".working/guardrail-reviews").mkdir(parents=True, exist_ok=True)
        (root / "governance").mkdir(parents=True, exist_ok=True)
        (root / "dev-security/claude-rules/governance").mkdir(parents=True, exist_ok=True)
        (root / ".claude/commands").mkdir(parents=True, exist_ok=True)
        for name in ("alpha", "beta"):
            (root / f"dev-security/claude-rules/skills/{name}").mkdir(parents=True, exist_ok=True)
            (root / f"dev-security/claude-rules/skills/{name}/SKILL.md").write_text("# s\n", encoding="utf-8")
            (root / f"dev-security/claude-rules/governance/{name}.md").write_text("# r\n", encoding="utf-8")
        (root / ".claude/commands/one.md").write_text("# c\n", encoding="utf-8")
        spec_rows = "".join(f"| {n} | Gate {n} | x |\n" for n in range(1, gates + 1))
        # The gate count is parsed from the section-6 region only (mirroring
        # gates 35 and 39); the trailing decoy table pins the scoping: its
        # numeric-first-cell rows sit outside section 6 and must not count.
        (root / "governance/specification-audit-programme.md").write_text(
            "# Spec\n\n## 6. Gate inventory (current)\n\n"
            "| # | Gate | Script |\n|---|---|---|\n" + spec_rows
            + "\n## 7. Notes\n\n| # | Thing |\n|---|---|\n| 99 | decoy |\n| 98 | decoy |\n",
            encoding="utf-8",
        )
        row = f"| 2026-07-02 | r1 | lenses | f | pr | d | Baseline; {recorded}. |\n" if with_row else ""
        (root / self.HISTORY_REL).write_text(
            "# History\n\n| Date | Run | Lenses | Findings | Resulting PR | Detail | Summary |\n"
            "|---|---|---|---|---|---|---|\n" + row,
            encoding="utf-8",
        )

    def test_zero_drift_passes(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            self._write_tree(d)
            result = run_linter("tools/lint-guardrail-cadence.py", "--root", d)
            self.assertEqual(
                result.returncode, 0,
                f"zero drift must pass.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertNotIn("warning", result.stdout)

    def test_small_drift_warns_but_passes(self) -> None:
        # One gate added since the recorded row: below the threshold, warn only.
        with tempfile.TemporaryDirectory() as d:
            self._write_tree(d, gates=4)
            result = run_linter("tools/lint-guardrail-cadence.py", "--root", d)
            self.assertEqual(
                result.returncode, 0,
                f"sub-threshold drift must pass with a warning.\nstdout:\n{result.stdout}",
            )
            self.assertIn("warning", result.stdout)
            self.assertIn("drifted 1", result.stdout)

    def test_just_below_threshold_warns(self) -> None:
        # Two gates added since the recorded row: one below the fail bar,
        # warn only (pins the boundary's underside at the maintainer-set 3).
        with tempfile.TemporaryDirectory() as d:
            self._write_tree(d, gates=5)
            result = run_linter("tools/lint-guardrail-cadence.py", "--root", d)
            self.assertEqual(
                result.returncode, 0,
                f"drift 2 must pass with a warning at threshold 3.\nstdout:\n{result.stdout}",
            )
            self.assertIn("warning", result.stdout)
            self.assertIn("drifted 2", result.stdout)

    def test_threshold_drift_fails(self) -> None:
        # Three gates added since the recorded row: at the maintainer-set
        # threshold (3, the 2026-07-02 return-round redirect), fail.
        with tempfile.TemporaryDirectory() as d:
            self._write_tree(d, gates=6)
            result = run_linter("tools/lint-guardrail-cadence.py", "--root", d)
            self.assertLinterFails(result, "drifted 3")

    def test_missing_inventory_token_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            self._write_tree(d, recorded="no counts recorded here")
            result = run_linter("tools/lint-guardrail-cadence.py", "--root", d)
            self.assertLinterFails(result, "inventory")

    def test_missing_history_row_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            self._write_tree(d, with_row=False)
            result = run_linter("tools/lint-guardrail-cadence.py", "--root", d)
            self.assertLinterFails(result, "inventory")

    def test_commands_axis_optional_for_old_rows(self) -> None:
        # The r1-era row records no commands axis: the comparison runs on the
        # three recorded axes only and passes at zero drift.
        with tempfile.TemporaryDirectory() as d:
            self._write_tree(d, recorded="inventory 3 gates / 2 rules / 2 skills")
            result = run_linter("tools/lint-guardrail-cadence.py", "--root", d)
            self.assertEqual(
                result.returncode, 0,
                f"a three-axis row must compare on its recorded axes.\nstdout:\n{result.stdout}",
            )


class CobitIso31000CitationsTests(LinterTestCase):
    """tools/lint-cobit-iso31000-citations.py (gate 61)

    COBIT 2019 / ISO 31000:2018 citation existence: flags an unknown COBIT
    objective, a practice code past its objective's contiguous range, an
    ISO 31000 clause outside the standard's 1-6 tree (only where the token's
    attribution to ISO 31000 is unambiguous), and the wrong ISO/IEC 31000
    designation. Valid codes and clauses pass; a clause token adjacent to a
    DIFFERENT standard on a multi-standard line is never mis-attributed.
    """

    SCRIPT = "tools/lint-cobit-iso31000-citations.py"

    def test_runs_clean_on_corpus_at_head(self) -> None:
        # Smoke test: the live corpus carries no fabricated COBIT codes or
        # invalid ISO 31000 clause citations. The two live fabrications found
        # while building the gate (MEA01.06, DSS01.06) were fixed in the same
        # PR that wired it as gate 61.
        result = run_linter(self.SCRIPT)
        self.assertEqual(
            result.returncode, 0,
            f"linter exited {result.returncode} on the live corpus; "
            f"COBIT/ISO 31000 citations should all be valid.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def _doc(self, body_line: str) -> str:
        return (
            "# X\n\n## Framework alignment\n\n"
            f"{body_line}\n"
        )

    def test_fabricated_practice_flagged(self) -> None:
        # APO12 has practices .01-.06 only; .07 is the motivating fabrication.
        fixture = self.make_fixture(
            "cobit-fab.md", self._doc("Risk acceptance follows APO12.07."),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertLinterFails(result, "cobit-practice-out-of-range")

    def test_unknown_objective_flagged(self) -> None:
        # There is no APO15; the APO objectives run APO01-APO14.
        fixture = self.make_fixture(
            "cobit-obj.md", self._doc("Aligned to COBIT 2019 APO15."),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertLinterFails(result, "cobit-objective-unknown")

    def test_valid_codes_pass(self) -> None:
        fixture = self.make_fixture(
            "cobit-ok.md",
            self._doc("| COBIT 2019 | APO12.06; DSS05.07; EDM03 | risk |"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertEqual(
            result.returncode, 0,
            f"valid COBIT codes should pass.\nstdout:\n{result.stdout}",
        )

    def test_iso31000_unknown_clause_flagged(self) -> None:
        # ISO 31000:2018 has clauses 1-6 only; a clause 7 citation is invalid.
        fixture = self.make_fixture(
            "iso31000-bad.md", self._doc("Per ISO 31000:2018 §7.1, review."),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertLinterFails(result, "iso31000-clause-unknown")

    def test_iso31000_valid_clause_passes(self) -> None:
        fixture = self.make_fixture(
            "iso31000-ok.md",
            self._doc("| ISO 31000:2018 | §6.4.2 Risk identification |"),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertEqual(
            result.returncode, 0,
            f"a valid ISO 31000 clause should pass.\nstdout:\n{result.stdout}",
        )

    def test_wrong_designation_flagged(self) -> None:
        # ISO 31000 is an ISO (TC 262) standard, never ISO/IEC.
        fixture = self.make_fixture(
            "iso31000-desig.md", self._doc("Assess using ISO/IEC 31000 criteria."),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertLinterFails(result, "iso31000-wrong-designation")

    def test_other_standard_clause_not_misattributed(self) -> None:
        # A multi-standard line: the §9/§9.3 tokens belong to ISO 37301 and
        # ISO 27001, not to ISO 31000, and must not be flagged.
        fixture = self.make_fixture(
            "iso31000-multi.md",
            self._doc(
                "Aligns to ISO 37301:2021 §9 (Performance evaluation), "
                "ISO/IEC 27001:2022 §9.3 (Management review), and "
                "ISO 31000:2018 §6.7 (Monitoring and review)."),
        )
        result = run_linter(self.SCRIPT, fixture)
        self.assertEqual(
            result.returncode, 0,
            f"other standards' clauses must not be mis-attributed.\n"
            f"stdout:\n{result.stdout}",
        )


class AuditSpecDetailedProseTests(LinterTestCase):
    """tools/lint-audit-spec-detailed-prose.py (gate 64)

    Presence check for the audit spec's per-gate detailed prose: every
    inventory gate at or above DESCRIPTION_FLOOR (35) needs a
    "Gate N is ..." description sentence and every gate at or above
    APPENDED_FLOOR (47) also a "Gate N is appended ..." sentence.
    """

    SCRIPT = "tools/lint-audit-spec-detailed-prose.py"

    @staticmethod
    def _spec(rows: list[int], prose: str) -> str:
        table = "\n".join(f"| {n} | Gate {n} name | `tools/g{n}.py` |" for n in rows)
        return (
            "# Spec fixture\n\n## 6. Inventory\n\n"
            "| # | Gate | Script |\n|---|---|---|\n" + table + "\n\n" + prose + "\n"
        )

    def test_complete_prose_passes(self) -> None:
        spec = self.make_fixture(
            "spec-prose-ok.md",
            self._spec(
                [34, 35, 47],
                "Gate 35 is a parity audit for the fixture. "
                "Gate 47 is a listing audit for the fixture. "
                "Gate 47 is appended at the tail.",
            ),
        )
        result = run_linter(self.SCRIPT, "--spec", spec)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_description_fails(self) -> None:
        spec = self.make_fixture(
            "spec-prose-nodesc.md",
            self._spec(
                [35, 47],
                "Gate 47 is a listing audit for the fixture. "
                "Gate 47 is appended at the tail.",
            ),
        )
        result = run_linter(self.SCRIPT, "--spec", spec)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("gate 35", result.stdout)

    def test_missing_appended_sentence_fails(self) -> None:
        spec = self.make_fixture(
            "spec-prose-noapp.md",
            self._spec(
                [47],
                "Gate 47 is a listing audit for the fixture.",
            ),
        )
        result = run_linter(self.SCRIPT, "--spec", spec)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("appended", result.stdout)

    def test_below_floor_gates_exempt_and_no_rows_error(self) -> None:
        spec = self.make_fixture("spec-prose-floor.md", self._spec([12, 34], ""))
        result = run_linter(self.SCRIPT, "--spec", spec)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        empty = self.make_fixture("spec-prose-empty.md", "# No table here\n")
        result = run_linter(self.SCRIPT, "--spec", empty)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)


class CrossFileSectionNamesTests(LinterTestCase):
    """tools/lint-cross-file-section-names.py (gate 65, the names phase)

    The title-anchoring rule: a parenthetical/quoted candidate after a
    cross-file reference is a title claim only when it equals SOME
    numbered-heading title in the target; it must then belong to the
    cited number (renumber drift fails), while paraphrases, shorthands,
    and explanatory parentheticals anchor to nothing and are skipped.
    """

    SCRIPT = "tools/lint-cross-file-section-names.py"

    TARGET_BODY = (
        "## 1. Introduction\n\n## 4. Encryption standards\n\n"
        "### 5.4 Key rotation\n\nBody.\n\n4.7.1 An inline clause line.\n"
    )

    def _target(self, name: str = "names-target.md") -> None:
        self.make_fixture(name, self.TARGET_BODY)

    def test_matching_title_passes(self) -> None:
        self._target()
        citer = self.make_fixture(
            "names-ok.md",
            "See [the target](names-target.md) §4 (Encryption standards) now.\n",
        )
        result = run_linter(self.SCRIPT, citer)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_renumber_drift_fails(self) -> None:
        self._target()
        citer = self.make_fixture(
            "names-drift.md",
            "See [the target](names-target.md) §1 (Encryption standards) now.\n",
        )
        result = run_linter(self.SCRIPT, citer)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("heading §4, not §1", result.stdout)

    def test_paraphrase_and_explanatory_skipped(self) -> None:
        self._target()
        citer = self.make_fixture(
            "names-paraphrase.md",
            "See [the target](names-target.md) §4 (crypto rules) and\n"
            "[the target](names-target.md) §1 (CISO approval, compensating control).\n",
        )
        result = run_linter(self.SCRIPT, citer)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_table_row_checked(self) -> None:
        # Deliberate divergence from gate 62: table rows are scanned.
        self._target()
        citer = self.make_fixture(
            "names-table.md",
            "| Ref | Note |\n|---|---|\n"
            "| [the target](names-target.md) §1 (Encryption standards) | x |\n",
        )
        result = run_linter(self.SCRIPT, citer)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_external_context_skipped(self) -> None:
        self._target()
        citer = self.make_fixture(
            "names-external.md",
            "Aligns to ISO 27001 §1 (Encryption standards); see "
            "[the target](names-target.md) too.\n",
        )
        result = run_linter(self.SCRIPT, citer)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_binding_declaration_pass_and_fail(self) -> None:
        self._target()
        self.make_fixture("names-sibling.md", "## 9. Unrelated\n")
        pass_citer = self.make_fixture(
            "names-bound-ok.md",
            "See [sibling](names-sibling.md) and [the standard](names-target.md). "
            "Section numbers below refer to that standard.\n\n"
            "Apply Section 4 (Encryption standards) throughout.\n",
        )
        result = run_linter(self.SCRIPT, pass_citer)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        fail_citer = self.make_fixture(
            "names-bound-bad.md",
            "See [sibling](names-sibling.md) and [the standard](names-target.md). "
            "Section numbers below refer to that standard.\n\n"
            "Apply Section 1 (Encryption standards) throughout.\n",
        )
        result = run_linter(self.SCRIPT, fail_citer)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_case_insensitive_quoted_title(self) -> None:
        self._target()
        citer = self.make_fixture(
            "names-quoted.md",
            'Per [the target](names-target.md) Section 5.4, "Key Rotation", act.\n',
        )
        result = run_linter(self.SCRIPT, citer)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_table_row_absent_number_fails(self) -> None:
        # The r4 O-1 seam: on a table row (which gate 62 excludes), an
        # anchored title claim whose cited number is absent fails HERE.
        self._target()
        citer = self.make_fixture(
            "names-table-absent.md",
            "| Ref | Note |\n|---|---|\n"
            "| [the target](names-target.md) §9 (Encryption standards) | x |\n",
        )
        result = run_linter(self.SCRIPT, citer)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("not a numbered heading", result.stdout)

    def test_inline_clause_cited_number_skipped(self) -> None:
        # The cited number has no heading title (an inline clause), so
        # even an anchoring parenthetical is not checked against it.
        self._target()
        citer = self.make_fixture(
            "names-clause.md",
            "See [the target](names-target.md) §4.7.1 (Encryption standards).\n",
        )
        result = run_linter(self.SCRIPT, citer)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class TodoRotationOnPrTests(unittest.TestCase):
    """tools/check-todo-rotation-on-pr.py (delta gate D5)

    Unit-tests the false-positive-critical trigger helper
    ``asserts_todo_closure`` directly (the gate is otherwise a git-diff
    delta check verified behaviourally via run-pr-time-checks.sh). The
    trigger (broadened 2026-06-30 by the since-closed rotation-prevention
    backlog item, again 2026-07-02 after the #563 verifier's tooling
    note, and again 2026-07-03 after the #607 miss) must fire on seven
    closure forms, the canonical
    "clos(e|es|ed|ing) [the] TODO §", the coded-id CLOSED major-closure
    marker (FR/GR/SR-style uppercase ids; widened by GR-13), the prose-named
    "clos... the ... (backlog item | TODO item | directive)" form, the
    section-name "section-N.M ... clos(ed|ure)" form, the item-number
    "item(s) N ... closed" form, the rotation-assertion "rotated to the
    DONE ledger" form, and the space-separated "TODO section N.M ...
    clos(ed|ure)" form, and NOT on incidental TODO/FR mentions or
    past-closure narration.
    """

    @staticmethod
    def _load():
        import importlib.util
        path = REPO_ROOT / "tools" / "check-todo-rotation-on-pr.py"
        spec = importlib.util.spec_from_file_location("check_todo_rotation_on_pr", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_closure_phrasings_flagged(self) -> None:
        m = self._load()
        for line in (
            "Adds gate 56, closing TODO §4.5 S4. The gate flags ...",
            "closes TODO §4.14 (the matrix gap-fill).",
            "Completes the family, closing TODO §4.10.",
            "closing the TODO §4.13 item",
            # Coded-id CLOSED major-closure marker (uppercase CLOSED; widened
            # from FR-only to any 2-4-letter uppercase id family per GR-13).
            "FR-58 CLOSED: applied the 3-label inheritance vocabulary.",
            "FR-167 CLOSED: matrix gap-fill for the 6 OT documents.",
            "GR-13 CLOSED: the D5 coded-id widening this very fixture pins.",
            "SR-5 CLOSED: ETSI designation corrected across scratch surfaces.",
            # Prose-named / explicit backlog-item form (the #495 miss shape).
            "closes the maintainer-directed OT post-ingestion audit/validation directive; no FR row.",
            "Closes the P3 docs/ house-style enforcement-gap backlog item.",
            "Closes the deferred backlog item R2 by principle.",
            # Section-name closure form (added 2026-07-02; the #567 vacuous
            # pass used exactly these phrasings).
            "Corpus fix (privacy): **section-1.8 closed**, the DSAR conflicts.",
            "the section-3.14 remainder closed with the batch-B merge.",
            "section-2.13 closure: the DSR clock item resolved at source.",
            # Item-number closure form (the #567 multi-item shape).
            "Corpus fix: **section-2.13 items 12-14 and 16-19 closed**.",
            "items 11 and 12 closed at source with the register bump.",
            "item 5 closed (the AI-audit anchor reword).",
            # Rotation-assertion form: a line CLAIMING the rotation happened
            # must be accompanied by the rotation surfaces in the diff (a
            # true claim passes trivially; past-rotation narration uses the
            # TodoRotation: trailer). This line lived in the negative fixture
            # before the 2026-07-02 widening; the widening deliberately
            # re-classifies it.
            "GR-2 closed (rotated to the DONE ledger), the first machinery item.",
            "the two flat-valued AI rows rotated to the DONE ledger.",
            # Widened form 3 (2026-07-03): the "bullet(s)" noun plus the
            # decimal-dot-tolerant clause run (the #592 mirror evasion, where
            # "section-3.14"'s dots blocked the old [^.\n] run outright).
            "Closes the section-3.14 fit-pass and retirement-recording bullets.",
            "Closes the \u00a75.3 deferred-classifications backlog item.",
            # Widened form 6 (2026-07-03): the short rotation assertion.
            "the third-batch bullet rotated to DONE with the intro re-counted.",
            # Form 7 (2026-07-03): the space-separated TODO-section closure,
            # the #607 lead shape that evaded forms 1 (no §), 4 (no hyphen),
            # and 6 (the rotation target was a markdown link, not the literal
            # DONE token). Case-insensitive on the closure word.
            "With all 38 worklist documents done, TODO section 1.1 is CLOSED and rotated to [`DONE.md`](x).",
            "The low-severity cleanup batch, TODO section 3.14, is fully closed.",
            "todo section 2.13 closure recorded with the register bump.",
        ):
            self.assertIsNotNone(
                m.asserts_todo_closure([line]),
                f"closure phrasing should be flagged: {line!r}",
            )

    def test_incidental_todo_mentions_not_flagged(self) -> None:
        m = self._load()
        for line in (
            "rotated TODO §4.5 S4 into DONE.md, closing the #466 finding.",
            # The form-6 not-negation guard (2026-07-03): negated narration is
            # not a rotation assertion (the two census hits).
            "TODO §1.5 is NOT rotated to DONE (the ATLAS residual holds it open).",
            "Recorded in TODO; not rotated to DONE.",
            "TODO §4.10 + P3 docs updated; the complementary check remains.",
            "the close-TODO-to-DONE rotation discipline",
            "Resolves the two pending maintainer decisions.",
            "S4 (no-bare-normative-shall) shipped in #466 (gate 56).",
            # Past-closure narration of OTHER PRs (the FP class that kept the
            # bare lowercase "Closes FR-N" form deliberately out of the trigger).
            "review (PR #143 closed FR-9 + FR-10, CRO ownership).",
            "(PRs #221-#228 closing FR-33/82/49/37/38/39/40/42) surfaced.",
            "FR-37/38/39/40/42 closed in #224-#228.",
            "FR-70 confirmed a significant gap, not expansion.",
            "per the FR-154 deepen-to-operational-depth decision.",
            # Lowercase coded-id narration stays excluded after the GR-13
            # widening (case-sensitivity is the deliberate FP guard); the
            # former "GR-2 closed (rotated to the DONE ledger)" line moved to
            # the positive fixture with the 2026-07-02 rotation-assertion form.
            "SR-5 upstream-CONFIRMED at #551, so not upstream-gated.",
            # "directive" inside a prepositional phrase, not the closure object
            # (the second-"the" guard excludes these).
            "closing the gap per the maintainer directive about scope.",
            "closes the loop for the maintainer directive on timing.",
            # The generalized "clos... the section" form was census-tested for
            # the 2026-07-02 widening and REJECTED (two historical FPs); the
            # shipped form requires the hyphenated section-N.M token, so bare
            # "section" narration stays excluded.
            "closing the section on retention with a pointer to the register.",
            "the items in section-3.13 remain open for the next batch.",
            # The item-number form's character class admits only digits and
            # punctuation between the numbers and "closed", so deferral
            # narration cannot match.
            "items 4-7 remain deferred, not closed, pending the source.",
            # Form 7's forward-only window: past-closure narration where the
            # closure word PRECEDES the "TODO section N.M" token stays
            # excluded (the #594 lead's shape).
            "the audit spec's last live pointer to the closed TODO section 3.14 reworded.",
            "TODO section 1.5 stays deferred pending the egress instance.",
        ):
            self.assertIsNone(
                m.asserts_todo_closure([line]),
                f"incidental mention must not be flagged: {line!r}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
