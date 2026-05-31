# Security and content defect reporting

This file describes how to report problems with the contents of this repository.

## Scope

This repository contains documentation, not executable software, so the conventional notion of a "security vulnerability" does not strictly apply. The reporting paths below cover the issues that matter for a CC BY-SA 4.0 governance library:

- **Content accuracy defects.** A document overstates compliance, misattributes a regulatory citation, repeats an incorrect framework identifier, or includes guidance that is materially wrong.
- **Licence concerns.** A document appears to reproduce restrictively-licensed third-party text without permission, or a contribution otherwise raises a licence-compatibility concern with the library's CC BY-SA 4.0 licence.
- **Organisation or personal data leakage.** A document includes a real company name, personal name, email address, phone number, internal system name, incident detail, IP address, or other identifier that should have been substituted per [`specification-ingestion.md`](specification-ingestion.md) Appendix A.
- **Broken or harmful external link.** An external reference in a document points to a defaced, replaced, or malicious resource.
- **Specification or tooling defect.** A scripted audit produces false positives or false negatives that allow conformance violations to land.

## How to report

Open a GitHub issue at https://github.com/jposluns/grc_library/issues. Use the issue title to summarise the concern in one sentence. Use the body to:

1. Identify the file path or repository area concerned.
2. Describe the defect, including the line number, the affected text, and the reason it is problematic.
3. Suggest a remediation if you have one. A pull request is welcome.

For sensitive disclosures (for example a licence concern with potential legal implications), open the issue with the minimum public detail required to identify the artefact and indicate in the body that further detail is available on request.

## What to expect

This repository is maintained on a best-effort basis by volunteers. There is no commercial support, no service-level agreement, and no guaranteed response time. Maintainers triage issues during their regular review cadence, which is monthly at a minimum.

For each accepted issue:

- The maintainer acknowledges receipt in the issue thread.
- A pull request resolves the defect.
- The affected document's version is incremented per the rules in [`specification-ingestion.md`](specification-ingestion.md) Version numbering.

## Out of scope

- Requests for new documents or new domains. Open an issue using the contribution workflow described in [`CONTRIBUTING.md`](CONTRIBUTING.md).
- Generic feature requests that are not defect reports.
- Reports of issues with downstream forks of this repository. Report those to the maintainer of the fork.

## Disclosure

Issues filed in this repository are public by default. Do not include sensitive personal data, organisation-internal data, or third-party confidential material in an issue. If a reporter does so by accident, a maintainer will redact the affected content and request that the reporter re-file with appropriate redaction.
