# Email Security Standard

**Document Title:** Email Security Standard\
**Document Type:** Standard\
**Version:** 1.0.1\
**Date:** 2026-06-02\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/policy-acceptable-use.md`](policy-acceptable-use.md), [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md), [`security/standard-data-loss-prevention.md`](standard-data-loss-prevention.md), [`security/standard-security-awareness-and-training.md`](standard-security-awareness-and-training.md), [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md), [`privacy/template-privacy-notice.md`](../privacy/template-privacy-notice.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material change to email infrastructure, threat-pattern, or regulator-expected posture\
**Repository Path:** [`security/standard-email-security.md`](standard-email-security.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This standard defines the minimum email security controls operated by the organisation. It covers email authentication (SPF, DKIM, DMARC, BIMI), inbound anti-phishing and anti-malware controls, outbound controls, business email compromise (BEC) mitigations, user reporting, secure email gateway requirements, and the supplementary controls applicable to high-risk roles.

---

## Scope

This standard applies to every email domain operated by the organisation, every mailbox provisioned to a human or non-human identity, and every email path that originates from or terminates at the organisation. It applies regardless of whether email is hosted on an internal platform or a cloud email service.

It does not cover messaging platforms other than email (chat, SMS, in-product messaging); those are governed by the network communications security policy.

---

## Section 1: outbound authentication

| Control area | Requirement |
| --- | --- |
| SPF | A SPF record published for every domain capable of sending email; the record enumerates authorised senders and ends with `-all` (or `~all` only during a documented transition window) |
| DKIM | DKIM signing enabled on every sending domain; key length at minimum 2048 bits; keys rotated at minimum annually |
| DMARC | DMARC record published for every domain with policy at minimum `p=quarantine` for primary domains and `p=reject` as the target state; aggregate and forensic reports collected and reviewed |
| BIMI | BIMI deployed where DMARC `p=reject` is in force and brand-protection benefits the deployment |
| Subdomain policy | Every sending subdomain has its own SPF and DKIM; DMARC inherits or specifies per subdomain |
| Parked domains | Domains not used for email publish a hardened SPF, an empty DKIM, and DMARC `p=reject` |
| TLS reporting (TLS-RPT) and MTA-STS | Published for every domain that operates a mail server; MTA-STS enforces TLS for inbound delivery |
| DNS hardening | DNSSEC enabled for email domains where the registrar and DNS operator support it |

---

## Section 2: inbound controls

| Control area | Requirement |
| --- | --- |
| Sender authentication enforcement | Inbound mail failing SPF, DKIM, or DMARC handled per the sender's published policy; spoofing patterns blocked |
| Look-alike domain detection | Inbound from look-alike domains (homograph, cousin-domain) flagged or blocked |
| Reputation filtering | Inbound mail evaluated against IP and domain reputation; high-risk traffic quarantined |
| URL rewriting and time-of-click protection | All URLs in inbound mail rewritten through a click-time inspection service |
| Attachment sandboxing | Executable attachments and high-risk file types detonated in a sandbox before delivery |
| Macro and active content blocking | Office and PDF active content blocked or stripped by default |
| Threat intelligence integration | Inbound filtering enriched with threat intelligence feeds |
| Encrypted attachment handling | Password-protected archives are decrypted where the password is provided in-mail and re-scanned; otherwise quarantined for user attestation |
| Inbound encryption | Inbound mail accepts STARTTLS by default; TLS reporting collected |

---

## Section 3: anti-phishing and BEC controls

| Control area | Requirement |
| --- | --- |
| Impersonation protection | Internal-user-impersonation detection covers all executive and finance-role mailboxes by default |
| External-sender markers | External senders identified with a visible banner or marker in the recipient's client |
| New-domain warnings | First-contact-from-domain warnings inserted into the recipient's view |
| Reply-to mismatch detection | Reply-to addresses that differ materially from From addresses flagged |
| Forwarding rule monitoring | Auto-forwarding rules to external addresses detected and reviewed; restricted by policy for high-risk roles |
| Out-of-band verification for sensitive actions | Payments, vendor-detail changes, payroll changes, gift-card requests, and credential-resets require out-of-band verification regardless of the email's apparent authenticity |
| Executive and high-risk role policy | Stricter anti-impersonation and forwarding controls applied to executive, finance, HR, IT administration, and legal mailboxes |

---

## Section 4: outbound controls

| Control area | Requirement |
| --- | --- |
| Data loss prevention | Outbound DLP per the DLP standard; sensitive content blocked or warned per data classification |
| Encryption | Encryption available to senders for messages containing Confidential or Restricted content; identity-based encryption preferred over manual passwords |
| Recipient confirmation | High-sensitivity outbound paths confirm recipient before send |
| Auto-reply restrictions | Auto-reply content does not disclose absence detail to external senders by default |
| Distribution-list controls | External distribution lists protected from accidental large-scale leakage |
| Mass-mail policy | Bulk and marketing outbound segregated from corporate sending; uses a dedicated domain to protect the primary domain's reputation |
| Outbound TLS | Outbound mail enforces TLS to known partner domains where TLS-RPT or known capability supports it |

---

## Section 5: user-facing controls

| Control area | Requirement |
| --- | --- |
| Reporting mechanism | One-click report-phishing control in the recipient's mail client; SOC triages reported items within the SLA |
| Awareness training | Email-specific modules in the awareness programme including phishing, BEC, and attachment hygiene |
| Phishing simulation | Regular simulations covering current threat patterns; results inform targeted training |
| Reporter feedback | Confirmation to the reporter of triage outcome where the reporter contributed material signal |
| Mailbox hygiene | Inbox-rule review encouraged; rules forwarding externally restricted |

---

## Section 6: secure-email-gateway and platform controls

| Control area | Requirement |
| --- | --- |
| Gateway tenancy | Dedicated secure-email-gateway functionality applies to all inbound and outbound mail; cloud-platform-native controls used where they meet or exceed the gateway baseline |
| Sandboxing tenancy | Attachment sandboxing isolated per tenant or per organisation; cross-tenant detonation results not used |
| Log integration | Secure-email-gateway and platform mail logs centralized in the SIEM; retention per the logging standard |
| Mailbox audit logging | Mailbox-level auditing (sign-in, rule changes, mailbox permission changes) enabled |
| Access to mailbox content | Privileged access to user mailbox content restricted, logged, and subject to approval per the privileged access standard |
| Backup and recovery | Mailbox backup and restoration meets the resilience programme expectations |
| Forensic readiness | Message-level evidence preservation supports the security incident response procedure |

---

## Section 7: AI-generated and AI-processed email considerations

| Control area | Requirement |
| --- | --- |
| AI-generated phishing | Detection content tuned to AI-generated phishing patterns (sophisticated grammar, brand mimicry, lack of typographic tells) |
| AI assistants drafting outbound mail | Drafts containing organisation-confidential material processed only by AI systems compliant with the AI access and agent permissions standard |
| Indirect prompt injection via email | Where email content is consumed by an AI assistant, embedded prompt-injection patterns are mitigated per the AI security technical implementation guide |
| Mailbox automation | AI agents acting on a mailbox use the agent-permissions framework; no shared mailbox impersonation |

---

## Section 8: incident response

| Trigger | Response |
| --- | --- |
| Confirmed phishing successful (credential theft) | Per the security incident response procedure; credential reset; session revocation; investigation of downstream access |
| Confirmed BEC successful (payment fraud) | Per the security incident response procedure with finance and legal engagement; banking partner notification; law enforcement notification per local statute |
| Mass-phishing campaign targeting the organisation | Inbound filters tuned; user communication; reporting threshold lowered; coordination with peer organisations where appropriate |
| Outbound mail abuse (compromised account sending mass mail) | Affected account isolated; rate limits engaged; reputation remediation; cause analysis |

---

## Operating expectations

1. SPF, DKIM, DMARC posture audited at least quarterly; movement towards `p=reject` tracked as a security metric.
2. Phishing-simulation programme runs continuously with quarterly review of click and report rates.
3. Email security configuration documented in the configuration baseline and reviewed at every material platform change.
4. The standard is reviewed annually against current threat-actor tactics including emerging AI-enabled phishing patterns.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| RFC 7208 | SPF | Sender authentication |
| RFC 6376 | DKIM | Message authentication |
| RFC 7489 | DMARC | Authentication policy |
| BIMI | AuthIndicators Working Group | Brand indication |
| RFC 8460 | TLS-RPT | TLS reporting |
| RFC 8461 | MTA-STS | TLS enforcement |
| NIST SP 800-177 Rev 1 | Trustworthy Email | US federal baseline |
| ISO/IEC 27001:2022 | A.5.14, A.8.21, A.8.23 | Information transfer; network security; web filtering |
| NIST CSF 2.0 | PROTECT, DETECT | Defensive coverage |
| OWASP Mail Header Injection prevention | OWASP | Application-layer email security |

---

## Limitations

This standard is a CC BY-SA 4.0 baseline. Specific platform configuration (cloud email service, secure-email-gateway, sandboxing provider) varies by deployment; the standard expresses the control requirements rather than product-specific settings. AI-enabled threats evolve rapidly; the standard expects an annual refresh against current threat-actor tactics.

---

**End of Document**
