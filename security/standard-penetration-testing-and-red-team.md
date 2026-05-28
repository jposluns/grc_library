# Penetration Testing and Red Team Standard

**Document Title:** Penetration Testing and Red Team Standard 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/procedure-vulnerability-management.md`](procedure-vulnerability-management.md), [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md), [`operations/standard-production-security-requirements.md`](../operations/standard-production-security-requirements.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual and upon material threat, framework, or regulatory change 
**Repository Path:** [`security/standard-penetration-testing-and-red-team.md`](standard-penetration-testing-and-red-team.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines the requirements for the organisation's penetration testing and red team programme. It establishes the minimum scope, frequency, methodology, and reporting requirements for both internal vulnerability assessment and externally conducted penetration testing.

The programme complements the Vulnerability Management Procedure and the Logging and Monitoring Standard by validating that controls are effective in practice, not merely in configuration. Vulnerability scanning identifies what is present; penetration testing determines what is exploitable. Together they provide assurance that the organisation's defensive posture reflects its intended security architecture.

This standard supports the Information Security Policy and addresses NIST SP 800-53 SA-11.

---

## Scope

1. Applies to all in-scope production systems, internet-facing services, internal network infrastructure, cloud environments (cloud platform, AWS, GCP), and enterprise identity provider configurations.
2. Covers external penetration testing (from an unauthenticated attacker perspective), internal network testing (lateral movement and privilege escalation), web and API application testing, and social engineering testing.
3. Applies to the infrastructure programme once systems are live in production.

---

## Governance and accountability

| Role | Responsibility |
| --- | --- |
| **Chief Information Security Officer (CISO)** | Owns this standard; approves scope and Rules of Engagement for each engagement; reviews all findings. |
| **IT Operations** | Coordinates access and deconfliction; ensures that findings are remediated within required timelines. |
| **Testing Vendor / Red Team** | Conducts testing per agreed scope and Rules of Engagement; delivers findings report within agreed timelines. |
| **Internal Audit** | Reviews programme compliance and remediation tracking annually. |

---

## Testing programme requirements

| Test Type | Minimum Frequency | Scope |
| --- | --- | --- |
| **External penetration test** | Annual | All internet-facing services, perimeter, and cloud management interfaces |
| **Internal network penetration test** | Annual (may be combined with external engagement) | Internal network lateral movement, directory services and enterprise identity provider attack paths, segmentation validation |
| **Web and API application test** | Annual per material application; before major release for new applications | OWASP Top 10, authentication, authorization, injection, API security |
| **Social engineering test** | Annual (may be integrated with the security awareness programme) | Phishing, vishing, collaboration platform impersonation simulation |
| **Cloud configuration review** | Annual | Cloud platform and cloud productivity platform configuration assessed against CIS Benchmarks |

---

## Rules of engagement

Every engagement requires a signed Rules of Engagement (RoE) document before testing begins. The RoE must specify:

1. In-scope systems and services.
2. Explicitly out-of-scope systems (including any systems where testing would cause operational disruption).
3. Authorized testing techniques and any prohibited techniques.
4. Notification contacts to be reached immediately if a critical finding requiring immediate action is discovered during testing.
5. Test window: authorized dates, times, and any change freeze periods to avoid.

Testing against production systems without a signed RoE is prohibited. Discovery of a critical finding during testing, including but not limited to active compromise indicators, credentials exposed in cleartext, or a viable data exfiltration path to sensitive data, must be communicated to the CISO immediately, regardless of whether the agreed test window is ongoing.

---

## Reporting

All penetration test results must be reported in writing. Each report must include:

1. Executive summary suitable for presentation to the CIO and senior leadership.
2. Methodology: testing approach, tools used, and phases conducted.
3. Findings with CVSS severity scores assigned to each finding.
4. Evidence: screenshots, proof-of-concept steps, and reproduction instructions.
5. Recommended remediation for each finding, including any quick-win mitigations for Critical and High findings.

Reports are classified Confidential and distributed only to the CIO, CISO, and relevant System Owners. Reports must not be forwarded or shared without CISO approval. Testing vendors must destroy all locally retained copies of findings evidence within 30 days of report delivery unless a longer retention period is agreed in writing.

---

## Remediation timelines

Remediation timelines for penetration test findings align with those established in the Vulnerability Management Procedure.

| Finding Severity | Required Remediation Timeline |
| --- | --- |
| **Critical** | Within 7 days |
| **High** | Within 30 days |
| **Medium** | Within 60 days or next maintenance window |
| **Low / Informational** | Risk acceptance or next scheduled release cycle |

Unresolved Critical and High findings beyond their required timelines are escalated to the CIO and logged in the Risk Register with a documented remediation plan.

---

## Vendor selection and qualification

External penetration testing must be conducted by a qualified third-party vendor. Vendors must:

1. Hold recognized industry certifications: OSCP, CREST, or equivalent.
2. Sign a non-disclosure agreement (NDA) before engagement commencement. The NDA must cover all findings, evidence, and system information obtained during testing.
3. Be selected through the Supplier Due Diligence Procedure.

The CISO retains final approval authority over vendor selection for all penetration testing engagements.

---

## Programme tracking and continuous improvement

1. Findings from all engagements are tracked in the organisation's vulnerability and risk management tooling.
2. Year-over-year trend analysis (finding counts by severity, repeat findings, time-to-remediation) is presented to the CISO and CIO annually.
3. Repeat findings, vulnerabilities identified in a prior engagement that remain unremediated or have recurred, are escalated to the CIO and treated as High-priority regardless of their CVSS score.
4. The CISO reviews the programme scope annually to ensure that emerging attack surfaces (new services, acquired systems, cloud workload growth) are incorporated.

---

## Framework alignment

| Control Area | ISO/IEC 27001:2022 | NIST SP 800-53 | CSA CCM v4.1 | Other |
| --- | --- | --- | --- | --- |
| Penetration testing programme | A.8.8 | SA-11 | TVM-07 | PTES |
| Web application security testing | A.8.8 | SA-11(1) | TVM-07 | OWASP Testing Guide v4.2 |
| Rules of engagement and authorization | A.5.36 | CA-8 | TVM-07 | N/A |
| Remediation tracking | A.8.8 | SI-2 | TVM-06 | N/A |
| Vendor qualification | A.5.19 | SA-12 | STA-05 | N/A |

---

**End of Document**
