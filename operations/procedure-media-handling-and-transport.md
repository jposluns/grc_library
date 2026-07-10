# Media Handling and Transport Procedure

**Document Title:** Media Handling and Transport Procedure\
**Document Type:** Procedure\
**Version:** 1.3.7\
**Date:** 2026-07-10\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md), [`operations/standard-physical-security-of-it-infrastructure.md`](standard-physical-security-of-it-infrastructure.md)\
**Classification:** Public\
**Category:** Operations\
**Review Frequency:** Annual and upon material platform or regulatory change\
**Repository Path:** [`operations/procedure-media-handling-and-transport.md`](procedure-media-handling-and-transport.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

This procedure defines the minimum requirements for classifying, storing, transporting, transferring, sanitizing, and disposing of physical and digital media throughout its lifecycle.

---

## 1. Purpose and scope

### 1.1 Purpose

To protect information held on physical and digital media from unauthorized disclosure, loss, or tampering during storage, internal movement, external transfer, and disposal. This procedure implements the media controls required by the Data Classification and Handling Standard and the Records Retention and Destruction Standard, ensuring that the method of media protection is always proportionate to the sensitivity classification of the information it contains.

### 1.2 Scope

1. Applies to all physical media including removable storage (USB drives, portable hard drives, optical media, magnetic tapes), printed documents, and decommissioned hardware containing storage.
2. Applies to all digital media transfers including file transfer, email attachment, cloud sharing, and direct network transfer.
3. Applies to organization-issued and personally-owned devices (BYOD) where they are used to handle organizational data.
4. Covers all employees, contractors, and third parties who handle organizational media in any classification.
5. Applies globally across all office locations, data centre sites, field operations, and logistics environments including BASC-certified trade and customs operations.

---

## 2. Governance

| Role | Responsibility |
| --- | --- |
| **CISO** | Owns this procedure; approves use of non-standard transfer mechanisms for Confidential or Restricted data; reviews annual metrics. |
| **IT Operations** | Manages approved media inventory and physical storage; performs and documents sanitization and disposal; maintains the asset register; procures and manages approved secure disposal vendors. |
| **Data Owners** | Classify data held on media under their domain; authorize transfers of Confidential or Restricted data; confirm retention holds before disposal is initiated. |
| **All Employees and Contractors** | Handle media in accordance with the classification of the information it contains; report loss or suspected compromise of media immediately to IT Operations and the CISO. |

Sector-conditional roles (for example, a BASC Regional Compliance Officer who confirms destruction of trade and customs data per BASC and applicable national customs authority obligations) apply where the organization participates in a covered sector programme; see [`compliance/`](../compliance/).

---

## 3. Media classification

The required level of protection for any piece of media is determined by the highest classification of information it contains, as defined in the Data Classification and Handling Standard.

| Data Classification | Physical Media Requirement | Digital Media Requirement |
| --- | --- | --- |
| **Public** | No restrictions. Normal disposal. | No restrictions on transfer channel. |
| **Controlled** | Standard storage; no special transport requirements. | Standard approved channels. |
| **Internal** | Locked storage when unattended. | Approved internal channels only; external transfer requires management approval. |
| **Confidential** | Locked container for storage and transport; encryption required if electronic. | Encrypted transfer channel (TLS 1.3); no personal cloud storage. |
| **Restricted** | Double-locked storage; signed chain-of-custody log for transport; encryption mandatory. | Encrypted transfer channel (TLS 1.3); approved system only; PAM-controlled access. |

Where a single piece of media contains data of multiple classifications, the controls applicable to the highest classification apply to the entire piece of media.

---

## 4. Secure transport of physical media

### 4.1 Approved transport methods

Physical media containing Confidential or Restricted information must only be transported using approved methods:

- Sealed, tamper-evident packaging for inter-office courier or postal services.
- Locked transport containers for hand-carry movement between sites.
- Accredited and contracted secure courier services where third-party transport is required.

Personal or untracked postal services are prohibited for Confidential and Restricted media. Consumer parcel carriers without tracked, signed-delivery services are prohibited.

### 4.2 Chain of custody

A chain-of-custody log must be maintained for every physical transport event involving Confidential or Restricted media. Each log entry must record:

| Field | Requirement |
| --- | --- |
| Media identifier | Asset tag, serial number, or unique label |
| Data classification | Highest classification of contents |
| Sender (name and role) | Individual releasing the media |
| Recipient (name and role) | Individual accepting the media |
| Handoff timestamp | Date and time at each transfer point |
| Transport method | Courier, hand-carry, or postal with reference/tracking number |
| Seal or container reference | Tamper-evident seal number or container ID |
| Signature | Both sender and recipient |

Chain-of-custody logs are retained for a minimum of 3 years or for the duration of the associated data's retention period, whichever is longer.

### 4.3 Encryption requirement for transport

All electronic media transported physically and containing Confidential or Restricted data must be encrypted before transport. Encryption must meet the requirements of the Encryption and Key Management Policy. Unencrypted removable media containing Confidential or Restricted data must not leave an IT-controlled area.

### 4.4 Loss or suspected compromise during transport

Loss or suspected compromise of physical media in transit must be reported immediately to the CISO and treated as a security incident under the Incident Response Procedure. If the media contained personal data, the DPO is notified concurrently to assess breach notification obligations.

---

## 5. Transfer of digital data

### 5.1 Approved transfer mechanisms

Digital transfer of organizational data must use approved channels. The approved mechanism depends on the classification of the data being transferred:

| Data Classification | Approved Transfer Mechanisms |
| --- | --- |
| Public / Controlled | Approved collaboration platform, email, or file-sharing service. |
| Internal | Approved internal systems; external transfer requires management approval and must use an encrypted channel. |
| Confidential | Approved encrypted file transfer service or encrypted email; TLS 1.3 minimum for all channels. |
| Restricted | Approved secure file transfer service with end-to-end encryption; access logged; transfer pre-authorized by CISO or Data Owner. |

### 5.2 Prohibition on personal cloud storage

The use of personal cloud storage services (including consumer file-sharing services) to store, transfer, or stage Confidential or Restricted data is strictly prohibited. This prohibition applies to all employees, contractors, and third parties. Violations are investigated under the Acceptable Use Policy and Incident Response Procedure.

### 5.3 Encrypted channels

All digital transfers of Confidential or Restricted data over any network, including the internal corporate network, must use an encrypted channel with TLS 1.3 or a higher-equivalent standard. TLS 1.2 may be used only where a documented technical constraint prevents TLS 1.3, with the constraint recorded in the exception register and reviewed quarterly.

### 5.4 Transfer to third parties

External transfer of Confidential or Restricted data to third parties requires:

1. Written authorization from the Data Owner.
2. A current and valid data sharing or processing agreement.
3. Confirmation that the receiving party's controls meet or exceed the requirements of this procedure.
4. Use of an approved encrypted transfer mechanism.

Ad-hoc external transfers using unapproved channels are prohibited. Requests for external transfers that cannot be accommodated by an approved channel are escalated to the CISO for resolution.

---

## 6. Media storage

### 6.1 Physical media storage

Physical media containing Confidential or Restricted data must be stored in locked, access-controlled cabinets within IT-managed infrastructure areas, as defined in the Physical Security of IT Infrastructure Standard. Storage requirements by classification:

| Classification | Storage Requirement |
| --- | --- |
| Internal | Locked cabinet in an access-controlled area; key or combination held by IT Operations. |
| Confidential | Locked cabinet in a restricted IT infrastructure area; access limited to authorized personnel; access log maintained. |
| Restricted | Double-locked storage (locked cabinet within a locked room); access list reviewed quarterly by the CISO; access events logged. |

Media containing Confidential or Restricted data must not be stored in general office areas, reception areas, or any area accessible without IT Operations authorization.

### 6.2 Portable digital media encryption

All portable digital media (USB drives, external hard drives, portable SSDs) used for organizational data must be encrypted. Unencrypted portable media is prohibited for Confidential or Restricted data. IT Operations maintains an inventory of organization-issued portable media and the data classification they are approved to carry. Personal USB drives and portable storage devices are not permitted to connect to organization-managed endpoints unless explicitly approved by the CISO for a documented purpose.

### 6.3 Backup media

Backup media (tapes or portable drives used for off-site backup) must be encrypted, stored in immutable repositories where technically feasible, and transported using chain-of-custody procedures consistent with §4. Backup media management is governed jointly by this procedure and the Backup and Recovery Procedure.

---

## 7. Media sanitization and destruction

### 7.1 Sanitization before reuse

Before any storage media is reissued for a different user or purpose, it must be sanitized to remove all previous data. The sanitization method must be appropriate to the classification of the data previously held and consistent with the organization's media-sanitization programme (NIST SP 800-88 Rev. 2) and the sanitization-technique categories of IEEE 2883 (NIST SP 800-88 Rev. 2 reframes around an enterprise sanitization programme and defers the technique detail to IEEE 2883, NSA specifications, or an organizationally-approved standard):

| Media Type | Required Sanitization Method |
| --- | --- |
| Hard disk drives (HDD) | IEEE 2883 Clear (overwrite) for Internal and below; Purge (verified overwrite or degauss) for Confidential and above. |
| Solid-state drives (SSD) and flash media | Cryptographic erasure using ATA Secure Erase, Sanitize (Block Erase), or equivalent. |
| Magnetic tapes | Degaussing followed by label removal and overwrite verification. |
| Mobile device storage | Factory reset with cryptographic erasure where supported by the device OS. |
| Optical media (CD, DVD, Blu-ray) | Physical destruction (shredding); optical media cannot be reliably overwritten and must not be reused for Confidential or above. |

### 7.2 Destruction of electronic media

Electronic media that cannot be sanitized, including media that has failed, damaged media, or media for which cryptographic erasure keys are unavailable, must be physically destroyed:

- Shredding, crushing, or disintegration in a manner that renders data recovery infeasible.
- Destruction must be performed or witnessed by an IT Operations staff member, or by a contracted accredited disposal vendor with Certificates of Destruction issued.

### 7.3 Destruction of paper and physical records

Paper and physical records containing Confidential or Restricted data must be destroyed by cross-cut shredding at DIN 66399 Level P-4 or higher, or by contracted secure document destruction services that meet equivalent standards. Strip-cut shredding is not acceptable for Confidential or Restricted records. Shredding bins in general office areas are subject to locked-bin requirements for any area where Confidential or Restricted documents are handled.

### 7.4 Destruction at end of retention period

Media disposal initiated by expiry of the Records Retention Schedule is coordinated between IT Operations and the relevant Data Owner. Prior to disposal, the Data Owner confirms that:

1. No active retention hold (litigation freeze or regulatory hold) is in effect.
2. The retention period for all data on the media has expired.

Media subject to an active retention hold must not be destroyed until Legal Counsel formally lifts the hold, per the Records Retention and Destruction Standard §3.

---

## 8. Certificate of destruction

### 8.1 Requirement

A Certificate of Destruction is mandatory for the disposal of all media that has held Confidential or Restricted data. This includes:

- All decommissioned servers and workstations.
- All portable media (USB drives, external drives, tapes) removed from service.
- All organization-issued mobile devices.
- Paper records of Confidential or Restricted classification destroyed by a contracted service.

A Certificate of Destruction is not required for internal-only paper records shredded on-site, provided the shredding is recorded in the Destruction Register.

### 8.2 Certificate contents

Each Certificate of Destruction must include:

| Field | Requirement |
| --- | --- |
| Asset or media identifier | Asset tag, serial number, or batch reference |
| Data classification | Highest classification of information held |
| Destruction method | Method applied (e.g., cryptographic erasure, physical shredding) |
| Date of destruction | Date destruction was completed |
| Location | Site or facility where destruction occurred |
| Performed by | Individual or vendor name |
| Witness (for on-site physical destruction) | Name and role of witness |
| Vendor certificate reference | Certificate number from the destruction vendor (if applicable) |

### 8.3 Retention

Certificates of Destruction are retained for a minimum of 7 years, consistent with the Records Retention and Destruction Standard. Certificates are stored in the IT Operations records system with access restricted to IT Operations and the CISO.

---

## 9. Surplus and disposal

### 9.1 Surplus hardware

Surplus hardware declared for disposal by IT Operations must be processed through the following workflow before leaving IT custody:

1. The asset is flagged for disposal in the asset register by the IT Operations lead.
2. The Data Owner for any data stored on the device confirms retention obligations are met and no hold is in effect.
3. Media sanitization or destruction is performed per §7 and recorded.
4. A Certificate of Destruction is obtained per §8.
5. The asset register is updated to "disposed" with the disposal date, method, and Certificate of Destruction reference.

No hardware may be donated, sold, transferred to a third party, or placed for general waste disposal without completing the above workflow.

### 9.2 Secure disposal vendor requirements

Where external vendors are used for media sanitization or physical destruction, vendors must:

- Hold documented and current accreditation such as R2, e-Stewards, ADISA, or equivalent national standard.
- Provide a Certificate of Destruction for each disposal event, itemized to the asset or batch level.
- Sign a data processing or confidentiality agreement prior to receiving any media.
- Be reviewed annually by IT Operations and the CISO for continued compliance with accreditation requirements.

### 9.3 Sector-programme data disposal

Where media holds data governed by a sector programme (for example, BASC-governed trade and customs data where the organization participates in BASC), destruction must be confirmed by the sector-conditional role defined by the relevant sector annex (for example, a BASC Regional Compliance Officer) before the Certificate of Destruction is filed. The sector-conditional role verifies that:

- The sector-programme minimum retention period has expired or the records have been migrated to an approved successor system.
- No sector authority hold or audit request (for example, no outstanding customs authority hold or audit request under BASC) is outstanding.
- The destruction method satisfies the relevant sector annex's data-security requirements.

See [`compliance/`](../compliance/) for the sector annex applicable to the organization's covered programmes.

---

## 10. Metrics

The following metrics are reported to the CISO quarterly and reviewed annually at the information security management review:

| Metric | Target |
| --- | --- |
| Disposal events with Certificate of Destruction (where required) | 100% |
| Media inventory accuracy (registered portable media vs. actual) | 100% quarterly reconciliation |
| Unauthorized media removal incidents (count) | Zero target; each incident investigated |
| Transfers of Confidential/Restricted data via unapproved channels (count) | Zero target; each incident investigated |
| Chain-of-custody log completion rate for qualifying physical transports | 100% |
| BASC trade data destruction confirmations completed on schedule | 100% |

---

## 11. Framework alignment

| Control Area | ISO/IEC 27001:2022 | NIST SP 800-88 Rev. 2 / IEEE 2883 | CSA CCM v4.1 | COBIT 2019 |
| --- | --- | --- | --- | --- |
| Media handling and classification | A.8.10 | 800-88 Rev. 2: programme scope | DSP-04 | DSS05.06 |
| Physical transport and chain of custody | A.8.10, A.7.10 | IEEE 2883: Clear | DCS-05 | DSS05.06 |
| Digital transfer controls | A.8.24, A.5.14 | N/A | DSP-10, CEK-03 | DSS05.02 |
| Media storage | A.8.10, A.7.9 | 800-88 Rev. 2: programme | DCS-04 | DSS05.01 |
| Sanitization and destruction | A.8.10 | IEEE 2883: Purge / Destruct | DSP-02 | DSS05.06 |
| Certificate of Destruction and records | A.5.33 | 800-88 Rev. 2: documentation | DSP-02 | DSS05.06 |

This procedure also aligns with ISO/IEC 27040:2024 (Storage security) for the secure handling, storage, and sanitization of storage media.

---

*This document is released under CC BY-SA 4.0. No rights reserved.*



**End of Document**
