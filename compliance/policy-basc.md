# BASC Information Security Policy

**Document Title:** BASC Information Security Policy  
**Document Type:** Policy  
**Version:** 1.0.0  
**Date:** 2026-05-27  
**Owner:** Chief Information Security Officer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`security/policy-information-security.md`](../security/policy-information-security.md), [`compliance/register-basc-it-responsibilities.md`](register-basc-it-responsibilities.md), [`compliance/register-basc-it-compliance-kpis.md`](register-basc-it-compliance-kpis.md), [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md)  
**Classification:** Public  
**Category:** Compliance Management  
**Review Frequency:** Annual and upon material BASC framework or infrastructure change  
**Repository Path:** [`compliance/policy-basc.md`](policy-basc.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

---

## Purpose

This policy establishes the framework for managing and protecting the organisation's information assets and supporting infrastructure in alignment with the Business Alliance for Secure Commerce (BASC) International Security Standards. It ensures the confidentiality, integrity, and availability of data across all BASC-certified operations.

---

## Scope

Applies to all employees, contractors, and third parties accessing the organisation's information systems, data, and technology resources.

---

## Definitions

| Term | Definition |
| --- | --- |
| CIO | Chief Information Officer, responsible for IT strategy and its alignment with business goals |
| CISO | Chief Information Security Officer, responsible for information security and privacy strategy |
| Policy | High-level guidelines directing decisions and actions |
| Standard | Mandatory controls that enforce policies |
| Procedure | Step-by-step instructions for carrying out tasks |
| Exception | An approved deviation from a policy or standard |

---

## Roles and Responsibilities

| Role | Responsibility |
| --- | --- |
| **Chief Information Officer (CIO)** | Approves this policy jointly with the CISO; oversees implementation and improvement. |
| **Chief Information Security Officer (CISO)** | Co-approves the policy; leads enhancement of IT, security, and privacy policies and standards. |
| **IT Operations Manager** | Manages technical configuration and change management requests; monitors compliance; declares incidents when necessary. |
| **Service Desk Manager** | Handles user and change management requests via the ITSM portal; monitors compliance; declares incidents when necessary. |
| **Department Heads** | Ensures departmental compliance with security practices; declares incidents when necessary. |
| **All Users** | Adhere to this policy and report any concerns or policy violations. |

---

## BASC Information Security Requirements

All requirements identified in Chapter 6 of the BASC International Security Standard are mapped below to the organisation's control areas.

| ID | Description | Control Area |
| --- | --- | --- |
| 6.1.a | Manage and protect information and IT resources, including response measures for non-compliance. | Asset Management; Threat Response |
| 6.1.b | Safeguard confidentiality, integrity, and availability of information in all forms. | Governance; Access Management; Asset Management; System Integrity; Threat Response |
| 6.1.c | Protect IT infrastructure. | Access Management; Asset Management; System Integrity; Threat Response |
| 6.2.a | Establish security criteria for IT systems and ensure recovery capabilities. | Threat Response |
| 6.2.b | Communicate cybersecurity threats to relevant parties. | Threat Response |
| 6.2.c | Identify critical stakeholders in IT infrastructure. | Access Management |
| 6.2.d | Classify information, systems, and access levels based on criticality. | Governance |
| 6.2.e | Use unique user credentials with periodic updates. | Access Management |
| 6.2.f | Limit and review user permissions based on assigned roles. | Access Management |
| 6.2.g | Revoke system access upon contract termination. | Access Management |
| 6.2.h | Prevent unauthorised software installation. | System Integrity |
| 6.2.i | Use licensed, updated hardware/software to protect against malware. | System Integrity |
| 6.2.j | Maintain secure backup copies of sensitive data offsite. | Asset Management |
| 6.2.k | Keep an updated user access record with criticality level. | Access Management |
| 6.2.l | Lock unattended computers. | Asset Management |
| 6.2.m | Evaluate IT infrastructure annually and address vulnerabilities. | Threat Response |
| 6.2.n | Identify unauthorised access or policy breaches. | Threat Response |
| 6.2.o | Review and update cybersecurity policies annually or as needed. | Governance |
| 6.2.p | Use VPN or MFA for remote access. | Access Management |
| 6.2.q | Prevent unauthorised remote access from personal or other devices. | System Integrity |
| 6.2.r | Inventory IT infrastructure media and equipment; ensure legal disposal. | Asset Management |
| 6.2.s | Restrict unauthorised devices from connecting to IT infrastructure. | System Integrity; Access Management |
| 6.2.t | Monitor cybersecurity policy compliance in digital content and tools. | System Integrity; Threat Response |
| 6.2.u | Conduct cybersecurity drills to test response effectiveness. | Threat Response |
| 6.2.v | Implement controls for admin and superuser account traceability. | Access Management |

---

## Information Security Controls

### Governance

An Information Security Manager is formally appointed and assigned responsibility for information security.

This policy is reviewed at least annually, or following any significant changes to the organisation's environment, with all revisions documented and approved by the CIO.

Information assets are classified by sensitivity: Confidential, Internal, Public.

Mandatory annual security awareness training is required for all personnel, covering the BASC Control and Security Management System (CSMS) and cybercrime prevention.

*Requirement IDs: 6.1.b, 6.2.d, 6.2.o*

### Access Management

Access rights are granted based on the principle of least privilege.

Access rights are reviewed at least annually to ensure they remain aligned with assigned functions and tasks.

User accounts are individually assigned and protected by passwords and MFA.

Privileged access, including superuser and administrator accounts, is managed through Privileged Identity Management (PIM).

Access for all third parties requires a supplier evaluation approved by the CISO.

Access is revoked immediately upon termination or contract conclusion.

*Requirement IDs: 6.1.b, 6.1.c, 6.2.c, 6.2.e, 6.2.f, 6.2.g, 6.2.k, 6.2.p, 6.2.s, 6.2.v*

### Asset and Media Management

All IT equipment and storage media are inventoried and tracked.

Disposal of media and assets is performed securely.

Unattended computers must be locked.

Antivirus and firewall protection are active and monitored.

Physical and virtual backups are maintained securely offsite and tested regularly.

*Requirement IDs: 6.1.a, 6.1.b, 6.1.c, 6.2.j, 6.2.l, 6.2.r*

### System Integrity

Only licensed and updated software is permitted.

The installation of unauthorised software on corporate devices is strictly prohibited.

Compliance with this policy for all sanctioned applications and platforms is actively monitored through the change management process.

Personal device connections to internal systems are restricted unless explicitly authorised through the endpoint management platform.

*Requirement IDs: 6.1.b, 6.1.c, 6.2.h, 6.2.i, 6.2.q, 6.2.s, 6.2.t*

### Threat Response

Cybersecurity incidents are documented, analysed, and communicated according to the established incident response process.

Unauthorised data manipulation or policy violations are monitored and investigated.

Regular information security incident process reviews are conducted.

Where required, post-incident evaluations are conducted to identify root causes and implement corrective actions.

Compliance is monitored through logs, reports, and audits.

*Requirement IDs: 6.1.a, 6.1.b, 6.1.c, 6.2.a, 6.2.b, 6.2.m, 6.2.n, 6.2.t, 6.2.u*

---

## Exception Process

### Submission

Any employee may submit an exception request via the ITSM portal or designated collaboration platform channel. The request must include: justification; duration; mitigation measures; impact assessment.

### Evaluation

- The CISO assesses information security and privacy impact.
- The CIO evaluates business implications.
- Legal is consulted when the deviation involves contractual or regulatory risk.

### Approval

- Temporary exceptions (less than 90 days): approved by CISO and CIO.
- Long-term exceptions: reviewed by the Change Control Board and require a risk acceptance memo signed by executive leadership.

### Documentation and Monitoring

All exceptions are logged and assigned an expiry or review date. Owners are responsible for implementing compensating controls and tracking progress.

---

## Information Security Audit Checklist

| Area | Evidence Required |
| --- | --- |
| Governance | IT Security Manager appointed; policy reviewed annually; information assets classified (Confidential, Internal, Public); security awareness training completed with attendance records. |
| Access Management | Access rights based on roles in the enterprise identity provider; MFA enforced; administrator access traceability controls enforced; third-party access authorised through supplier evaluation; access revocation within 2 hours of termination. |
| Asset Management | Managed computer inventory maintained; unattended computers locked via policy; offsite backups implemented and tested; secure media and hardware disposal procedures followed. |
| System Integrity | Personal device access managed through endpoint management platform; only authorised devices on the network; only licensed and supported systems and software in use; controls prevent unauthorised software installation. |
| Threat Response | Cybersecurity incidents tracked and reported; security incident response process documented and followed; logs and audit trails reviewed regularly; annual IT infrastructure evaluation conducted. |

---

## Framework Alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| BASC International Standard v6 (2023) | Chapter 6 — IT and Information Security | Primary source of control requirements |
| ISO/IEC 27001:2022 | A.5–A.8 — Security controls | Information security management alignment |
| NIST SP 800-53 r5 | AC, IA, SI, IR — Access, identity, integrity, incident | Control family mapping |
| CSA CCM v5 | IAM, HRS, TVM, LOG | Cloud control alignment |
| WCO SAFE Framework (2021) | AEO Security | Trade and customs information security |

---

**End of Document**
