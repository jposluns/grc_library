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

    def test_bare_ensure_flagged(self) -> None:
        # The 'ensure' rule requires 'that' after 'ensure'/'ensures'.
        fixture = self.make_fixture(
            "standard-bare-ensure.md",
            VALID_METADATA + "\n\nThe team must ensure compliance.\n",
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
        # should never appear in organisation-neutral library content. The
        # first term in the list is "Traffic Tech" — using it triggers
        # the rule.
        fixture = self.make_fixture(
            "standard-sanitisation.md",
            VALID_METADATA + "\n\nThe vendor Traffic Tech provided the platform.\n",
        )
        result = run_linter("tools/lint-language.py", fixture)
        self.assertLinterFails(result, "sanitisation")

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
            VALID_METADATA + "\n\nThe organisation is aligned with ISO/IEC 27001:2013.\n",
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
            VALID_METADATA + "\n\n[Unverified] The organisation shall implement controls.\n",
        )
        result = run_linter("tools/lint-shall-near-uncertainty.py", fixture)
        self.assertLinterFails(result)

    def test_must_near_tbd_flagged(self) -> None:
        # Different mandatory ('must') and different uncertainty ('TBD')
        # markers exercise a different code path through the rule set.
        fixture = self.make_fixture(
            "standard-must-tbd.md",
            VALID_METADATA + "\n\nTBD: define the threshold; the organisation must enforce it.\n",
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
        # Phase 23.63: template-placeholder organisation domains must
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


class RequiredSectionsTests(LinterTestCase):
    """tools/lint-required-sections.py"""

    def test_missing_orientation_section_flagged(self) -> None:
        bad = VALID_METADATA.replace("## Purpose", "## Background")
        fixture = self.make_fixture("standard-no-orientation.md", bad)
        result = run_linter("tools/lint-required-sections.py", fixture)
        self.assertLinterFails(result)


class SectionPlacementTests(LinterTestCase):
    """tools/lint-section-placement.py"""

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
        # and a SUBSUMED cell as 'subsumption', from field 4.
        mod = self._load_module()
        text = (
            "| Date | PR | Touched | Findings | Hot-fix | Detail | Summary |\n"
            "|---|---|---|---|---|---|---|\n"
            "| 2026-06-25 | 99 | x | **`/validate-pr` SKIPPED (handoff-PR "
            "exception, loop-break)** | none | - | s |\n"
            "| 2026-06-25 | 98 | x | **NOT run; SUBSUMED by Sweep 42** | none | - | s |\n"
            "| 2026-06-25 | 97 | x | **0 findings (clean)** | none | - | s |\n"
        )
        status = mod.parse_validate_pr_status(text)
        self.assertEqual(status.get(99), "handoff")
        self.assertEqual(status.get(98), "subsumption")
        self.assertEqual(status.get(97), "normal")

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
    a minimal Data Retention Schedule register and the three procedures it is
    cross-referenced with, so a deliberate retention drift can be detected
    without depending on the live corpus (which is clean).
    """

    REGISTER_REL = "governance/register-data-retention-schedule.md"
    PROCS = {
        "compliance/procedure-capa.md": "CAPA records",
        "compliance/standard-internal-audit.md": "Internal audit reports",
        "compliance/procedure-control-testing.md": "Control testing evidence",
    }

    def _write_tree(self, d: str, *, capa_proc_years: int = 7, capa_anchor: bool = True) -> None:
        root = Path(d)
        (root / "governance").mkdir(parents=True, exist_ok=True)
        (root / "compliance").mkdir(parents=True, exist_ok=True)
        register = (
            "# Data Retention Schedule\n\n"
            "| Record category | Retention period | Basis |\n"
            "|---|---|---|\n"
            "| CAPA records | 7 years after closure | Quality management |\n"
            "| Internal audit reports | 7 years | ISO 19011 |\n"
            "| Control testing evidence | 7 years | Audit support |\n"
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


class TodoRotationOnPrTests(unittest.TestCase):
    """tools/check-todo-rotation-on-pr.py (delta gate D5)

    Unit-tests the false-positive-critical trigger helper
    ``asserts_todo_closure`` directly (the gate is otherwise a git-diff
    delta check verified behaviourally via run-pr-time-checks.sh). The
    trigger must fire on the canonical "clos(e|es|ed|ing) [the] TODO §"
    closure phrasing and NOT on incidental TODO mentions.
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
        ):
            self.assertIsNotNone(
                m.asserts_todo_closure([line]),
                f"closure phrasing should be flagged: {line!r}",
            )

    def test_incidental_todo_mentions_not_flagged(self) -> None:
        m = self._load()
        for line in (
            "rotated TODO §4.5 S4 into DONE.md, closing the #466 finding.",
            "TODO §4.10 + P3 docs updated; the complementary check remains.",
            "the close-TODO-to-DONE rotation discipline",
            "Resolves the two pending maintainer decisions.",
            "S4 (no-bare-normative-shall) shipped in #466 (gate 56).",
        ):
            self.assertIsNone(
                m.asserts_todo_closure([line]),
                f"incidental mention must not be flagged: {line!r}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
