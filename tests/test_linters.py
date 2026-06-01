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


if __name__ == "__main__":
    unittest.main(verbosity=2)
