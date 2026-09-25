# Canada Public Sector GRC Requirements Annex

**Document Title:** Canada Public Sector GRC Requirements Annex\
**Document Type:** Annex\
**Version:** 0.0.16\
**Date:** 2026-09-25\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/public-sector/README.md`](README.md), [`compliance/public-sector/annex-public-sector-requirements.md`](annex-public-sector-requirements.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`privacy/jurisdictions/annex-privacy-canada.md`](../../privacy/jurisdictions/annex-privacy-canada.md), [`ai/jurisdictions/annex-ai-canada.md`](../../ai/jurisdictions/annex-ai-canada.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material Canadian public-sector law, policy, directive, or guidance change\
**Repository Path:** [`compliance/public-sector/annex-canada-public-sector-requirements.md`](annex-canada-public-sector-requirements.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex is the Canada-specific public-sector carrier for the GRC library. It supplements the jurisdiction-neutral [`compliance/public-sector/annex-public-sector-requirements.md`](annex-public-sector-requirements.md) by organizing Canadian federal, provincial, territorial, municipal or local, contractor, health-information, financial-sector, and private-sector applicability boundaries.

The annex is scoped to the federal public-sector authority layer and the public-sector access, privacy, and health-information layers of all ten provinces and all three territories. Clause-level content is added cluster by cluster: the federal public-sector privacy and access-to-information baselines in domain cluster 4 carry quoted clause text; the other clusters remain largely foundations, and until the forthcoming Canadian authority coverage register exists, no jurisdiction is recorded as covered. It distinguishes laws from binding policies and directives, regulatory guidance, strategies, voluntary frameworks, consultation drafts, and historical or superseded sources.

This foundation establishes the applicability model and durable section structure. Source-specific duties, dates, thresholds, control mappings, and jurisdictional conclusions are added only from current, held, publisher-canonical sources. Until the forthcoming Canadian authority coverage register (the companion evidence register to this annex) exists, each such source is recorded in the Canonical Citations Register, as the federal privacy baseline's sources are.

---

## Applicability triggers

This annex is relevant where the entity is:

1. A federal government institution.
2. A provincial or territorial ministry, agency, board, commission, Crown entity, or other public body.
3. A municipal or local public body within the scope of a jurisdiction-specific statute.
4. A health-information custodian, trustee, public health body, health authority, or service provider within the scope of an applicable health-information law.
5. A contractor handling government records, personal information, health information, or public-facing service delivery.
6. A federally regulated financial institution subject to an applicable Office of the Superintendent of Financial Institutions guideline.
7. A private-sector organization whose Canadian activities fall under federal or provincial private-sector privacy law.
8. An entity occupying more than one of these roles for different activities, records, systems, or legal relationships.

---

## Applicability decision tree

1. **Is the entity a federal government institution?**
   - If yes, use the federal public-sector lane in this annex.
   - Assess the applicable federal statutes separately from Treasury Board policies, directives, standards, notices, tools, and guidance.
   - Do not substitute PIPEDA for the federal public-sector Privacy Act.

2. **Is the entity a provincial or territorial public body?**
   - If yes, use the row and source set for that province or territory.
   - Do not infer that a federal Treasury Board instrument governs the entity.
   - Confirm the statute's definitions, exclusions, responsible authority, and current consolidation before recording a requirement.

3. **Is the entity a municipality, local authority, school board, police service, library, or other local public body?**
   - If yes, determine whether the jurisdiction uses the general public-sector statute, a separate municipal or local-authority statute, or another statutory arrangement.
   - Do not generalize a provincial-body rule to a municipal or local body without source support.

4. **Is the entity acting as a public-sector contractor or service provider?**
   - If yes, identify the governing contract, data-processing terms, records-control terms, security requirements, and any statute-specific contractor or service-provider provisions.
   - Contractor status does not make every public-sector authority directly applicable to the contractor's entire business.
   - Record each applicable contractual and statutory basis separately.

5. **Is the entity a federally regulated financial institution?**
   - If yes, assess applicable OSFI instruments in the FRFI lane.
   - OSFI guidance is sector-specific and is not a general Canadian public-sector authority.
   - Being federally regulated does not make the institution a federal government institution.

6. **Is the entity a private-sector organization engaged in commercial activities or another private-sector processing context?**
   - If yes, use [`privacy/jurisdictions/annex-privacy-canada.md`](../../privacy/jurisdictions/annex-privacy-canada.md) for the private-sector privacy layer.
   - Do not use PIPEDA or OPC PIPEDA guidance as a substitute for federal, provincial, territorial, municipal, or health-sector public-body law.

7. **Do two or more lanes apply?**
   - If yes, document applicability by entity, activity, record class, system, jurisdiction, sector, and contractual role.
   - Apply the source-specific analysis for every applicable lane; this annex does not resolve conflicts of law.

---

## Authority and force model

| Source status | Treatment in this annex |
| --- | --- |
| Law or regulation | State the statutory or regulatory scope and requirement only from the current official text |
| Binding policy, directive, standard, or notice | State the issuer, covered organizations, application conditions, and force without presenting the instrument as legislation |
| Regulatory or government guidance | Use for interpretation and control design; do not restate it as a statutory duty |
| Strategy, roadmap, plan, or programme | Use as policy direction or context; do not present it as a binding obligation |
| Voluntary framework or standard | Record voluntary status and any actual adoption separately |
| Consultation draft | Label non-final and exclude from active authority treatment unless the corpus intentionally references the draft |
| Historical or superseded source | Preserve for provenance where useful; identify the current successor and do not use the historical source as the active baseline |

A source's presence in the Canadian authority coverage register does not make it applicable, current, binding, or suitable for the Canonical Citations Register. Only current, fit sources receive active citation rows and relationship nodes.

---

## Domain cluster 1: federal AI governance and automated decision-making

This section carries the federal public-sector AI layer. It distinguishes binding directives and mandatory tools from advisory guidance, strategies, roadmaps, registers, learning resources, product-specific notices, and other informational sources.

| Coverage area | Required treatment |
| --- | --- |
| Automated administrative decisions | State the covered federal-institution and decision context from the controlling directive |
| Algorithmic impact assessment | Register the directive, overview page, and questionnaire definition as separate sources |
| Transparency, explanations, oversight, recourse, testing, and monitoring | Attribute each requirement to the exact source and applicable impact level |
| Generative and agentic AI | Separate advisory guides, binding notices, and departmental accountabilities |
| Strategy and transparency registers | Label policy direction, implementation reporting, and public inventories accurately |
| Transition and review status | Use current tense and preserve completed transition dates as historical facts |

The complete Canadian AI regulatory framing remains in [`ai/jurisdictions/annex-ai-canada.md`](../../ai/jurisdictions/annex-ai-canada.md). This annex carries the public-sector applicability and control-mapping layer and does not duplicate that annex's full per-regime treatment.

---

## Domain cluster 2: federally regulated financial institutions

This section carries Canadian financial-sector technology, cyber-risk, and model-risk sources only where the adopter is a federally regulated financial institution or is contractually supporting one.

| Coverage area | Required treatment |
| --- | --- |
| Technology and cyber risk | Attribute applicable expectations to the exact OSFI guideline |
| Model risk, including AI and machine-learning models | Preserve publication and future-effective status |
| Third parties and service providers | Distinguish direct FRFI applicability from contractual flow-down |
| Public-sector boundary | State expressly that OSFI does not govern Canadian public bodies generally |

Sector-specific AI treatment is cross-referenced to [`ai/jurisdictions/annex-ai-canada.md`](../../ai/jurisdictions/annex-ai-canada.md). Broader financial-services treatment remains in the financial-services annex and related operational documents.

---

## Domain cluster 3: security, cloud, identity, records, incidents, and digital service

This section carries federal public-sector security and digital-service sources selected as current and fit.

| Coverage area | Required treatment |
| --- | --- |
| Government security governance | Distinguish policies, directives, standards, plans, playbooks, and guidance |
| Security categorization | Cite only the held source and exact categorization provisions |
| IT security risk management | Limit ITSG-33 claims to the held annexes |
| Network security zones | Use the exact CCCS identifier and current edition |
| Cloud security | Use the current cloud categorization guidance and current control profile |
| Historical cloud controls | Treat the legacy GC cloud profile's Appendix A control list as replaced by the CCCS Medium Cloud Control Profile (ITSP.50.103 Annex B); a cloud service provider holding an authorization under Appendix A (version 1.1, 28 March 2018) contacts CCCS for its compliance transition requirements |
| Identity management | Distinguish binding direction from draft or voluntary trust frameworks |
| Incident and event management | Separate enterprise plans from advisory incident-response guidance |
| Records, open government, and digital service | Attribute obligations and recommendations to their exact federal sources |

A source reference or framework-alignment row does not establish implementation, effectiveness, sufficiency, conformity, or compliance.

---

## Domain cluster 4: federal access to information and privacy

This section carries the federal public-sector access and privacy layer.

| Coverage area | Required treatment |
| --- | --- |
| Access to government records | Use the current federal statute and applicable Treasury Board policy as separate sources |
| Federal public-sector privacy | Use the Privacy Act and applicable Treasury Board policy |
| Private-sector privacy boundary | Use PIPEDA and its regulations only for their applicable private-sector contexts; OPC guidance that also addresses federal institutions (for example, on personal-information retention and disposal) may inform federal practice as guidance, alongside the Privacy Act |
| Breach safeguards and retention | Keep statutory, regulatory, and guidance sources separate |
| Request and response workflows | Record source-specific clocks, extensions, exemptions, and review routes only after claim-level verification |
| Contractor handling | Identify whether duties arise from law, government control of records, contract, or more than one source |

The complete private-sector and provincial-private-sector treatment remains in [`privacy/jurisdictions/annex-privacy-canada.md`](../../privacy/jurisdictions/annex-privacy-canada.md).

### Federal public-sector privacy baseline

This baseline quotes the current official English texts of the **Privacy Act** (R.S.C. 1985, c. P-21), a statute, and the **Treasury Board Policy on Privacy Protection** (in effect since 9 October 2024), a Treasury Board policy issued under paragraph 71(1)(d) of the Act (Policy section 2.1), which is not itself legislation. Each requirement is quoted verbatim, with its punctuation, and its provision number is given in the Provision column rather than inside the quotation, so that no condition, exception or qualifier is lost in paraphrase; the adopter reads each provision in its full context before relying on it.

**Applicability.** The Act's duties rest on a *government institution* or its head, which section 3 of the Act defines as "(a) any department or ministry of state of the Government of Canada, or any body or office, listed in the schedule, and (b) any parent Crown corporation, and any wholly-owned subsidiary of such a corporation, within the meaning of section 83 of the Financial Administration Act". The Policy "and its supporting instruments apply to government institutions as defined in section 3 of the Act" (Policy section 6.1), and "does not apply to the Bank of Canada" (Policy section 6.2). The Act's duties for personal information under an institution's control remain the institution's. Policy 4.2.16 makes the head of the institution, or a delegate, responsible for "Taking steps to ensure, when personal information is involved, that third parties under contract, agreement or arrangement with the government institution provide appropriate privacy protections"; that third party's obligations for the information then arise from the instruments the institution uses (for example, contract terms) and from other applicable law. Part 1 of PIPEDA does not apply to a government institution to which the Privacy Act applies (PIPEDA paragraph 4(2)(a)); where the third party is a private-sector organization, its own handling of personal information in the course of commercial activity falls under PIPEDA or substantially similar provincial private-sector law, treated in the Canadian privacy annex.

| Privacy Act text (quoted) | Provision |
| --- | --- |
| "No personal information shall be collected by a government institution unless it relates directly to an operating program or activity of the institution." | Section 4 |
| "A government institution shall, wherever possible, collect personal information that is intended to be used for an administrative purpose directly from the individual to whom it relates except where the individual authorizes otherwise or where personal information may be disclosed to the institution under subsection 8(2)." | Subsection 5(1) |
| "A government institution shall inform any individual from whom the institution collects personal information about the individual of the purpose for which the information is being collected." | Subsection 5(2) |
| "Subsections (1) and (2) do not apply where compliance therewith might (a) result in the collection of inaccurate information; or (b) defeat the purpose or prejudice the use for which information is collected." | Subsection 5(3) |
| "Personal information that has been used by a government institution for an administrative purpose shall be retained by the institution for such period of time after it is so used as may be prescribed by regulation in order to ensure that the individual to whom it relates has a reasonable opportunity to obtain access to the information." | Subsection 6(1) (the period is set by regulation and is not stated in this annex) |
| "A government institution shall take all reasonable steps to ensure that personal information that is used for an administrative purpose by the institution is as accurate, up-to-date and complete as possible." | Subsection 6(2) |
| "A government institution shall dispose of personal information under the control of the institution in accordance with the regulations and in accordance with any directives or guidelines issued by the designated minister in relation to the disposal of that information." | Subsection 6(3) |
| "Personal information under the control of a government institution shall not, without the consent of the individual to whom it relates, be used by the institution except (a) for the purpose for which the information was obtained or compiled by the institution or for a use consistent with that purpose; or (b) for a purpose for which the information may be disclosed to the institution under subsection 8(2)." | Section 7 |
| "Personal information under the control of a government institution shall not, without the consent of the individual to whom it relates, be disclosed by the institution except in accordance with this section." | Subsection 8(1) |
| "Sections 7 and 8 do not apply to personal information that is publicly available." | Subsection 69(2) |
| "This Act does not apply to (a) library or museum material preserved solely for public reference or exhibition purposes; or (b) material placed in the Library and Archives of Canada, the National Gallery of Canada, the Canadian Museum of History, the Canadian Museum of Nature, the National Museum of Science and Technology, the Canadian Museum for Human Rights or the Canadian Museum of Immigration at Pier 21 by or on behalf of persons or organizations other than government institutions." | Subsection 69(1) (excludes the whole Act) |
| "This Act does not apply to personal information that the Canadian Broadcasting Corporation collects, uses or discloses for journalistic, artistic or literary purposes and does not collect, use or disclose for any other purpose." | Section 69.1 (excludes the whole Act) |
| "This Act does not apply to confidences of the Queen’s Privy Council for Canada, including, without restricting the generality of the foregoing, any information contained in" | Subsection 70(1), opening words; its paragraphs list the kinds of confidence covered (excludes the whole Act, subject to subsection 70(3)) |
| "Subsection (1) does not apply to (a) confidences of the Queen’s Privy Council for Canada that have been in existence for more than twenty years; or (b) discussion papers described in paragraph (1)(b) (i) if the decisions to which the discussion papers relate have been made public, or (ii) where the decisions have not been made public, if four years have passed since the decisions were made." | Subsection 70(3) |
| "The head of a government institution shall cause to be included in personal information banks all personal information under the control of the government institution that (a) has been used, is being used or is available for use for an administrative purpose; or (b) is organized or intended to be retrieved by the name of an individual or by an identifying number, symbol or other particular assigned to an individual." | Subsection 10(1) |
| "Subsection (1) does not apply in respect of personal information under the custody or control of the Library and Archives of Canada that has been transferred there by a government institution for historical or archival purposes." | Subsection 10(2) |
| "Subject to this Act, every individual who is a Canadian citizen or a permanent resident within the meaning of subsection 2(1) of the Immigration and Refugee Protection Act has a right to and shall, on request, be given access to (a) any personal information about the individual contained in a personal information bank; and (b) any other personal information about the individual under the control of a government institution with respect to which the individual is able to provide sufficiently specific information on the location of the information as to render it reasonably retrievable by the government institution." | Subsection 12(1) |
| "The Governor in Council may, by order, extend the right to be given access to personal information under subsection (1) to include individuals not referred to in that subsection and may set such conditions as the Governor in Council deems appropriate." | Subsection 12(3) |
| "Where access to personal information is requested under subsection 12(1), the head of the government institution to which the request is made shall, subject to section 15, within thirty days after the request is received, (a) give written notice to the individual who made the request as to whether or not access to the information or a part thereof will be given; and (b) if access is to be given, give the individual who made the request access to the information or the part thereof." | Section 14 |
| "The head of a government institution may extend the time limit set out in section 14 in respect of a request for (a) a maximum of thirty days if (i) meeting the original time limit would unreasonably interfere with the operations of the government institution, or (ii) consultations are necessary to comply with the request that cannot reasonably be completed within the original time limit, or (b) such period of time as is reasonable, if additional time is necessary for translation purposes or for the purposes of converting the personal information into an alternative format, by giving notice of the extension and the length of the extension to the individual who made the request within thirty days after the request is received, which notice shall contain a statement that the individual has a right to make a complaint to the Privacy Commissioner about the extension." | Section 15 (the closing words from "by giving notice of the extension" apply to both paragraphs (a) and (b)) |

| Policy on Privacy Protection text (quoted; responsibilities of heads of government institutions or their delegates, Policy 4.2) | Provision |
| --- | --- |
| "Ensuring that employees of the government institution are aware of policies, procedures and legal responsibilities under the Act;" | Policy 4.2.1 |
| "Notifying the Treasury Board of Canada Secretariat (TBS) and the Office of the Privacy Commissioner of Canada (OPC) of any planned initiatives (legislation, regulations, policies or programs) that could relate to the Act or to any of its provisions, or that may have an impact on the privacy of individuals. This notification is to take place at a sufficiently early stage to permit TBS and the OPC to review and discuss the issues involved while respecting Cabinet confidences;" | Policy 4.2.2 |
| "Ensuring that personal information banks (PIBs) are prepared and updated, as required by section 10 of the Act;" | Policy 4.2.4 |
| "Obtaining the approval of the President of the Treasury Board to establish, modify or terminate a PIB, unless otherwise specified in the terms and conditions of a delegation under subsection 71(6) of the Act;" | Policy 4.2.5 |
| "Ensuring that, when applicable, privacy impact assessments and multi-institutional privacy impact assessments are developed, maintained and summaries published;" | Policy 4.2.8 |
| "Establishing plans to address privacy breaches that affect personal information under the control of the institution, including those that occur within third-party entities under contract, agreement or arrangement with the institution;" | Policy 4.2.10 |
| "Conducting periodic reviews of established plans that address privacy breaches to ensure that they reflect best practices and guidance;" | Policy 4.2.11 |
| "Reporting material privacy breaches to TBS and the OPC after making efforts to contain, assess and mitigate the breach and no later than seven days after the institution determines that the breach is material;" | Policy 4.2.12 |
| "Taking steps to ensure, when personal information is involved, that third parties under contract, agreement or arrangement with the government institution provide appropriate privacy protections;" | Policy 4.2.16 |

Policy Appendix A defines a *material privacy breach* (the threshold for the Policy 4.2.12 report) as follows:

> A privacy breach that could reasonably be expected to create a real risk of significant harm to an individual. Significant harm includes bodily harm, humiliation, damage to reputation or relationships, loss of employment, business or professional opportunities, financial loss, identity theft, negative effects on the credit record and damage to or loss of property.

### Federal access-to-information baseline

This baseline quotes the current official English texts of the **Access to Information Act** (R.S.C. 1985, c. A-1) and the **Access to Information Regulations** (SOR/83-507), both legislation, and two Treasury Board instruments issued under paragraph 70(1)(c) of the Act, which are not themselves legislation: the **Policy on Access to Information** (in effect since 28 June 2023) and the **Directive on Access to Information Requests** (in effect since 13 July 2022). The quotation convention is the one used in the privacy baseline above: each requirement is quoted verbatim and its provision number is given in the Provision column, and the adopter reads each provision in its full context before relying on it. Where a quotation is only the opening words or an extract of a longer provision, the Provision column says so. This is a baseline of the request workflow and the institution's duties, not a complete transcription of the Act.

**Purpose, scope and right of access.**

| Access to Information Act text (quoted) | Provision |
| --- | --- |
| "The purpose of this Act is to enhance the accountability and transparency of federal institutions in order to promote an open and democratic society and to enable public debate on the conduct of those institutions." | Subsection 2(1) |
| "government institution means (a) any department or ministry of state of the Government of Canada, or any body or office, listed in Schedule I, and (b) any parent Crown corporation, and any wholly-owned subsidiary of such a corporation, within the meaning of section 83 of the Financial Administration Act; (institution fédérale)" | Section 3, definition of *government institution* |
| "Subject to this Part, but notwithstanding any other Act of Parliament, every person who is (a) a Canadian citizen, or (b) a permanent resident within the meaning of subsection 2(1) of the Immigration and Refugee Protection Act, has a right to and shall, on request, be given access to any record under the control of a government institution." | Subsection 4(1) |
| "The Governor in Council may, by order, extend the right to be given access to records under subsection (1) to include persons not referred to in that subsection and may set such conditions as the Governor in Council deems appropriate." | Subsection 4(2) |
| "The head of a government institution shall, without regard to the identity of a person making a request for access to a record under the control of the institution, make every reasonable effort to assist the person in connection with the request, respond to the request accurately and completely and, subject to the regulations, provide timely access to the record in the format requested." | Subsection 4(2.1) |

| Policy on Access to Information text (quoted) | Provision |
| --- | --- |
| "This policy and its supporting instruments apply to government institutions as defined in section 3 of the Access to Information Act, including departments, ministries of state, any parent Crown corporations and any wholly owned subsidiary of these corporations." | Policy 6.1 |
| "This policy does not apply to the Bank of Canada." | Policy 6.2 |

The order made under subsection 4(2) that extends the right of access to further persons is not carried here; an adopter that needs the full eligibility rule reads that order alongside subsection 4(1).

**Requests, fees, response periods and transfers.**

| Access to Information Act text (quoted) | Provision |
| --- | --- |
| "A request for access to a record under this Part shall be made in writing to the government institution that has control of the record and shall provide sufficient detail to enable an experienced employee of the institution to identify the record with a reasonable effort." | Section 6 |
| "Subject to this section, a person who makes a request for access to a record under this Part shall pay, at the time the request is made, any application fee of not more than $25, that may be prescribed by regulation." | Subsection 11(1) |
| "Where access to a record is requested under this Part, the head of the government institution to which the request is made shall, subject to sections 8 and 9, within 30 days after the request is received, (a) give written notice to the person who made the request as to whether or not access to the record or a part thereof will be given; and (b) if access is to be given, give the person who made the request access to the record or part thereof." | Section 7 |
| "Where a government institution receives a request for access to a record under this Part and the head of the institution considers that another government institution has a greater interest in the record, the head of the institution may, subject to such conditions as may be prescribed by regulation, within fifteen days after the request is received, transfer the request and, if necessary, the record to the other government institution, in which case the head of the institution transferring the request shall give written notice of the transfer to the person who made the request." | Subsection 8(1) |
| "The head of a government institution may extend the time limit set out in section 7 or subsection 8(1) in respect of a request under this Part for a reasonable period of time, having regard to the circumstances, if (a) the request is for a large number of records or necessitates a search through a large number of records and meeting the original time limit would unreasonably interfere with the operations of the government institution, (b) consultations are necessary to comply with the request that cannot reasonably be completed within the original time limit, or (c) notice of the request is given pursuant to subsection 27(1) by giving notice of the extension and, in the circumstances set out in paragraph (a) or (b), the length of the extension, to the person who made the request within thirty days after the request is received, which notice shall contain a statement that the person has a right to make a complaint to the Information Commissioner about the extension." | Subsection 9(1), complete |
| "Where the head of a government institution extends a time limit under subsection (1) for more than thirty days, the head of the institution shall give notice of the extension to the Information Commissioner at the same time as notice is given under subsection (1)." | Subsection 9(2) |
| "Where the head of a government institution refuses to give access to a record requested under this Part or a part thereof, the head of the institution shall state in the notice given under paragraph 7(a) (a) that the record does not exist, or (b) the specific provision of this Part on which the refusal was based or, where the head of the institution does not indicate whether a record exists, the provision on which a refusal could reasonably be expected to be based if the record existed, and shall state in the notice that the person who made the request has a right to make a complaint to the Information Commissioner about the refusal." | Subsection 10(1) |
| "Where the head of a government institution fails to give access to a record requested under this Part or a part thereof within the time limits set out in this Part, the head of the institution shall, for the purposes of this Part, be deemed to have refused to give access." | Subsection 10(3) |

| Access to Information Regulations text (quoted) | Provision |
| --- | --- |
| "A request for access to a record under Part 1 of the Act must be made by forwarding to the appropriate officer of the government institution that has control of the record, together with the required application fee, (a) a completed Access to Information Request Form; or (b) a written request that provides sufficient detail to enable the officer to identify the record." | Subsection 4(1) |
| "A person who makes a request for access to a record under Part 1 of the Act must pay an application fee of $5 at the time the request is made." | Section 7 |

**Declining to act on a request.**

| Access to Information Act text (quoted) | Provision |
| --- | --- |
| "With the Information Commissioner’s written approval, the head of a government institution may, before giving a person access to a record or refusing to do so, decline to act on the person’s request if, in the opinion of the head of the institution, the request is vexatious, is made in bad faith or is otherwise an abuse of the right to make a request for access to records." | Subsection 6.1(1) |
| "The head of a government institution is not authorized under subsection (1) to decline to act on a person’s request for a record for the sole reason that the information contained in it has been published under Part 2." | Subsection 6.1(1.1) |
| "The head of the institution shall give written notice to the person who made the request for access to a record under this Part of the suspension of the period, and of the reasons for the suspension, at the same time as they communicate with the Information Commissioner to obtain his or her approval to decline to act." | Subsection 6.1(1.3) |
| "If the head of a government institution declines to act on the person’s request, they shall give the person written notice of their decision to decline to act on the request and their reasons for doing so." | Subsection 6.1(2) |

**Exemptions.** The following navigation descriptions are editorial summaries of the exemption provisions. They identify subject matter only and are not grounds for withholding; the provision's full conditions, exceptions and discretion govern.

| Exemption subject matter (editorial summary) | Provision |
| --- | --- |
| Information obtained in confidence from specified governments and organizations; federal-provincial affairs; international affairs and defence; law enforcement, investigations and security | Sections 13 to 16 |
| Specified investigation, examination and audit records; lobbying and elections investigations; public-sector integrity and disclosure-protection records; the Secretariat of the National Security and Intelligence Committee of Parliamentarians | Sections 16.1 to 16.6 |
| Safety of individuals; Canadian economic interests and economic interests of specified institutions | Sections 17 to 18.1 |
| Personal information; third-party information; specified confidential investment information and National Arts Centre information | Sections 19 to 20.4 |
| Government advice, deliberations and plans; testing and auditing; internal audits; legal and patent/trademark privileges | Sections 21 to 23.1 |
| Schedule II disclosure prohibitions; severability; material intended for publication | Sections 24 to 26 |

| Access to Information Act text (quoted) | Provision |
| --- | --- |
| "Subject to subsection (2), the head of a government institution shall refuse to disclose any record requested under this Part that contains information that was obtained in confidence from (a) the government of a foreign state or an institution thereof; (b) an international organization of states or an institution thereof; (c) the government of a province or an institution thereof; (d) a municipal or regional government established by or pursuant to an Act of the legislature of a province or an institution of such a government; or (e) an aboriginal government." | Subsection 13(1) |
| "Subject to subsection (2), the head of a government institution shall refuse to disclose any record requested under this Part that contains personal information." | Subsection 19(1) |
| "The head of a government institution shall refuse to disclose any record requested under this Part that contains information the disclosure of which is restricted by or pursuant to any provision set out in Schedule II." | Subsection 24(1) |
| "Notwithstanding any other provision of this Part, where a request is made to a government institution for access to a record that the head of the institution is authorized to refuse to disclose under this Part by reason of information or other material contained in the record, the head of the institution shall disclose any part of the record that does not contain, and can reasonably be severed from any part that contains, any such information or material." | Section 25 |

**Exclusions from Part 1.**

| Access to Information Act text (quoted) | Provision |
| --- | --- |
| "This Part does not apply to (a) published material, other than material published under Part 2, or material available for purchase by the public; (b) library or museum material preserved solely for public reference or exhibition purposes; or (c) material placed in the Library and Archives of Canada, the National Gallery of Canada, the Canadian Museum of History, the Canadian Museum of Nature, the National Museum of Science and Technology, the Canadian Museum for Human Rights or the Canadian Museum of Immigration at Pier 21 by or on behalf of persons or organizations other than government institutions." | Section 68 |
| "This Part does not apply to confidences of the Queen’s Privy Council for Canada, including, without restricting the generality of the foregoing," | Subsection 69(1), opening words only |
| "If a certificate under section 38.13 or 38.41 of the Canada Evidence Act prohibiting the disclosure of information contained in a record is issued before a complaint is filed under this Part in respect of a request for access to that information, this Part does not apply to that information." | Subsection 69.1(1) |

**Complaints, orders and Federal Court review.**

| Access to Information Act text (quoted) | Provision |
| --- | --- |
| "Subject to this Part, the Information Commissioner shall receive and investigate complaints (a) from persons who have been refused access to a record requested under this Part or a part thereof; (b) from persons who have been required to pay an amount under section 11 that they consider unreasonable; (c) from persons who have requested access to records in respect of which time limits have been extended pursuant to section 9 where they consider the extension unreasonable; (d) from persons who have not been given access to a record or a part thereof in the official language requested by the person under subsection 12(2), or have not been given access in that language within a period of time that they consider appropriate; (d.1) from persons who have not been given access to a record or a part thereof in an alternative format pursuant to a request made under subsection 12(3), or have not been given such access within a period of time that they consider appropriate; (e) in respect of any publication or bulletin referred to in section 5; or (f) in respect of any other matter relating to requesting or obtaining access to records under this Part." | Subsection 30(1) |
| "A complaint under this Part shall be made to the Information Commissioner in writing unless the Commissioner authorizes otherwise. If the complaint relates to a request by a person for access to a record, it shall be made within sixty days after the day on which the person receives a notice of a refusal under section 7, is given access to all or part of the record or, in any other case, becomes aware that grounds for the complaint exist." | Section 31 |
| "If, after investigating a complaint described in any of paragraphs 30(1)(a) to (e), the Commissioner finds that the complaint is well-founded, he or she may make any order in respect of a record to which this Part applies that he or she considers appropriate, including requiring the head of the government institution that has control of the record in respect of which the complaint is made (a) to disclose the record or a part of the record; and (b) to reconsider their decision to refuse access to the record or a part of the record." | Subsection 36.1(1) |
| "The Information Commissioner shall, after investigating a complaint under this Part, provide a report that sets out the results of the investigation and any order or recommendations that he or she makes to (a) the complainant; (b) the head of the government institution; (c) any third party that was entitled under paragraph 35(2)(c) to make and that made representations to the Commissioner in respect of the complaint; and (d) the Privacy Commissioner, if he or she was entitled under paragraph 35(2)(d) to make representations and he or she made representations to the Commissioner in respect of the complaint. However, no report is to be made under this subsection and no order is to be made until the expiry of the time within which the notice referred to in paragraph (1)(c) is to be given to the Information Commissioner." | Subsection 37(2) |
| "A person who makes a complaint described in any of paragraphs 30(1)(a) to (e) and who receives a report under subsection 37(2) in respect of the complaint may, within 30 business days after the day on which the head of the government institution receives the report, apply to the Court for a review of the matter that is the subject of the complaint." | Subsection 41(1) |
| "The head of a government institution who receives a report under subsection 37(2) may, within 30 business days after the day on which they receive it, apply to the Court for a review of any matter that is the subject of an order set out in the report." | Subsection 41(2) |

This is the principal review route, not the complete procedure: investigations (sections 32 to 36), when an order takes effect (subsections 36.1(4) and (5)), third-party and Privacy Commissioner review (subsections 41(3) and (4)) and stays (section 41.1) are further provisions an adopter reads before relying on this summary.

**Proactive publication under Part 2.** Part 2 has separate branches for parliamentary entities (sections 71.01 to 71.14), ministers (sections 72 to 80), government institutions (sections 81 to 90) and the named judicial administration offices (sections 90.01 to 90.24). This baseline quotes only section 88 (briefing materials, which applies to a government entity as defined in section 81, a narrower group than all government institutions) and the publication limits in section 90. The other publication duties in sections 82 to 87 (travel and hospitality expenses, tabled reports, position reclassifications, contracts, and grants and contributions), with their clocks, and the other branches are read in the Act.

| Access to Information Act text (quoted) | Provision |
| --- | --- |
| "The head of a government entity shall cause to be published in electronic form (a) within 120 days after the appointment of a deputy head or a person to a position of an equivalent rank, the package of briefing materials that is prepared for the deputy head or the person for the purpose of enabling him or her to assume the powers, duties and functions of his or her office; (b) within 30 days after the end of the month in which any memorandum prepared for the deputy head or the person is received by his or her office, the title and reference number of each memorandum that is received; and (c) within 120 days after an appearance before a committee of Parliament, the package of briefing materials that is prepared for the deputy head or the person for the purpose of that appearance." | Section 88 |
| "A head of a government institution is not required to cause to be published any of the information, any part of the information, any of the materials or any part of the materials referred to in any of sections 82 to 88 if that information, that part of the information, those materials or that part of those materials were set out in a record and, in dealing with a request for access to that record, he or she could under Part 1 refuse to disclose that record, in whole or in part, for a reason that is set out in that Part." | Subsection 90(1) |
| "A head of a government institution shall not cause to be published any of the information, any part of the information, any of the materials or any part of the materials referred to in any of sections 82 to 88 if that information, that part of the information, those materials or that part of those materials were set out in a record and, in dealing with a request for access to that record, he or she would be required under Part 1 to refuse to disclose that record, in whole or in part, for a reason that is set out in that Part or because that Part does not apply to the information or materials in question." | Subsection 90(2) |

**Institutional accountability, records and reporting.**

| Access to Information Act text (quoted) | Provision |
| --- | --- |
| "No person shall, with intent to deny a right of access under this Part, (a) destroy, mutilate or alter a record; (b) falsify a record or make a false record; (c) conceal a record; or (d) direct, propose, counsel or cause any person in any manner to do anything mentioned in any of paragraphs (a) to (c)." | Subsection 67.1(1) |
| "Every year the head of every government institution shall prepare a report on the administration of this Act within the institution during the period beginning on April 1 of the preceding year and ending on March 31 of the current year." | Subsection 94(1) |
| "The head of a government institution may, by order, delegate any of their powers, duties or functions under this Act to one or more officers or employees of that institution." | Subsection 95(1) |

| Policy on Access to Information text (quoted) | Provision |
| --- | --- |
| "Determining, in a manner consistent with jurisprudence and considering any TBS guidance, whether records are under the control of the government institution." | Policy 4.3.1 |
| "Deliberations and decisions concerning requests received under the Act are documented;" | Policy 4.3.9, sub-item 3 |
| "The principle of severability is applied;" | Policy 4.3.9, sub-item 5 |

| Directive on Access to Information Requests text (quoted) | Provision |
| --- | --- |
| "Establishing and maintaining an internal management system to track: The processing of access requests; Consultation requests; Complaints; Reports, recommendations, and orders by the Information Commissioner; and Reviews by the courts." | Directive 4.1.18 and its sub-items 1 to 5 |
| "Documenting the processing of requests by placing on file all documents that support decisions under Part 1 of the Act, including communications where factors considered when exercising discretion are discussed, recommendations are given, rationales are provided and decisions are made." | Directive 4.1.19 |
| "Ensuring that any extension taken is as short as possible and can be reasonably justified." | Directive 4.1.28 |
| "Citing exemptions and exclusions invoked on records, provided under Part 1 of the Act, on each page, unless doing so would reveal the exempted information or cause the injury upon which the exemption is based to materialize." | Directive 4.1.34 |
| "Establishing internal procedures to address alleged or suspected obstructions related to the right of access under Part 1 of the Act and the Information Commissioner’s duties and functions, which are outlined in sections 67 (1) and 67.1(1) of the Act. Procedures should outline measures for:" | Directive 4.1.45, opening requirement |
| "Documenting and reporting any suspected falsification, concealment, mutilation or improper destruction of records as described in section 67.1(1) or any obstruction of the Information Commissioner’s duties and functions as defined in 67(1) immediately to the head of the government institution;" | Directive 4.1.45, sub-item 1 |
| "Publishing summaries of completed access to information requests to the Government of Canada Open Government portal within 30 calendar days after the end of each month, in accordance with Appendix D: Mandatory Procedures for Publishing Summaries of Completed Access to Information Requests." | Directive 4.1.46 |
| "Ensuring searches for records are comprehensive and consider both the letter and the spirit of the request." | Directive 4.2.3 |
| "Establishing measures to support the right of public access to information when entering into contracts, arrangements and agreements." | Directive 4.2.8 |

The suspension of the response period while the head of the institution seeks the Information Commissioner's approval to decline (subsection 6.1(1.2)), third-party notification (sections 27 and 28), the Appendix D fields for published request summaries, and records retention and disposal are not carried in this baseline.

---

## Domain cluster 5: provincial and territorial access and privacy

This section is scoped to all ten provinces and all three territories. Each official statute is to be registered individually in the companion coverage register, including separate provincial and municipal or local-authority instruments.

| Delivery group | Jurisdictions | Foundation rule |
| --- | --- | --- |
| Western and Central | British Columbia, Alberta, Saskatchewan, Manitoba | Reflect Alberta's split access and privacy statutes, and Saskatchewan's provincial and local-authority instruments, only from held current sources |
| Ontario and Quebec | Ontario, Quebec | Keep Ontario provincial and municipal instruments separate and Quebec public-body law distinct from private-sector privacy law |
| Atlantic | New Brunswick, Nova Scotia, Prince Edward Island, Newfoundland and Labrador | Use each jurisdiction's current official consolidation |
| Territories | Yukon, Northwest Territories, Nunavut | Include all three; do not infer one territory's scope, definitions, or procedures from another |

No source-specific statutory duty is added while its official consolidation is source-gated, incomplete, stale, or unverified.

---

## Domain cluster 6: health-information privacy

This section is scoped to the health-information privacy layer across all provinces and territories. The inventory is to record the applicable primary in each jurisdiction without assuming that every jurisdiction uses the same statutory model or has a standalone health-information statute.

| Coverage area | Required treatment |
| --- | --- |
| Health-information custodians, trustees, and public health bodies | Resolve the exact statutory terms and scope per jurisdiction |
| Health-information service providers and contractors | Separate direct statutory duties from contractual flow-down |
| Collection, use, disclosure, safeguarding, access, correction, retention, and disposal | Add only source-supported requirements and clocks |
| Health-information systems and repositories | Distinguish generally applicable health-information law from narrower electronic-health legislation |
| Interaction with general public-sector privacy law | State the source-specific precedence, exclusion, or concurrent-application rule |
| Jurisdictions without a verified standalone primary | Record the general-law carrier or remaining source gap explicitly |

Health-information rows remain source-gated until the exact official title, identifier, current consolidation, effective status, and publisher provenance are held and verified.

---

## Relationship to the Canadian AI and privacy annexes

- [`ai/jurisdictions/annex-ai-canada.md`](../../ai/jurisdictions/annex-ai-canada.md) remains the consolidating per-regime view of Canadian AI governance. This annex supplies the federal, provincial, territorial, municipal, contractor, and FRFI public-sector applicability paths.
- [`privacy/jurisdictions/annex-privacy-canada.md`](../../privacy/jurisdictions/annex-privacy-canada.md) remains the consolidating Canadian privacy annex, including the federal private-sector layer. This annex supplies the dedicated federal and sub-national public-sector and health-information carrier.
- Where the same source is relevant to more than one annex, each annex cross-references the same canonical citation and relationship node. It does not create a second source identity.
- Where operational procedures are maintained elsewhere in the library, this annex provides applicability and mapping rather than duplicating the procedure.

---

## Library gaps requiring additional documentation

1. **Provincial, territorial and municipal public-records request workflows** with jurisdiction-specific clocks, extensions, exemptions, review routes, and disclosure logs (the federal access-to-information baseline is carried in domain cluster 4).
2. **Complete municipal and local-authority source inventory** for jurisdictions whose local bodies are governed separately.
3. **National health-information privacy inventory** with an explicit carrier for every province and territory.
4. **Public-sector contractor clause set** covering government records, privacy, security, access support, retention, return, and destruction.
5. **Current-source acquisition and reconfirmation workflow** for publisher sites that block automated retrieval.
6. **Source-specific control mappings** for each fit authority, with no inference of implementation or compliance.
7. **Canadian authority coverage register** retaining no-fit, duplicate, draft, historical, superseded, and source-gated evidence.

---

## Framework alignment

Source-specific framework mappings are populated only after the relevant domain cluster passes reference, claim-fit, and matrix-fit review.

When those mappings are added, each authority cluster follows the mapping discipline set out in its own section above: federal AI-governance sources are mapped to the AI-governance documents without collapsing their force; OSFI sources are mapped only in the federally-regulated-financial-institution context; federal security, cloud, identity, and digital-service sources are mapped with their supersession relationships preserved; federal access and privacy sources keep public-sector and private-sector applicability contexts separate; provincial, territorial, municipal, and health-information law is mapped only from held current official consolidations; and historical, draft, duplicate, and no-fit sources retain disposition evidence without an active compliance mapping.

---

## Limitations

This annex is a CC BY-SA 4.0 navigation and control-mapping aid. It is not legal advice, a legal opinion, compliance certification, or evidence that an adopting entity has implemented, satisfied, or complied with a Canadian authority.

Canadian public-sector applicability depends on the entity, activity, record, system, jurisdiction, sector, statutory definitions, contractual role, and current source text. Contractor status, public funding, or work for a public body does not by itself establish that every public-sector requirement applies directly.

This foundation does not replace a jurisdiction-specific freedom-of-information workflow, privacy request workflow, health-information workflow, records schedule, security authorization, procurement process, or contractual analysis. Adopting entities obtain jurisdiction-specific legal advice and verify current official sources before reliance.

Draft, future-effective, historical, superseded, incomplete, or source-gated materials remain labelled as such. A citation, relationship, or mapping does not establish implementation, effectiveness, sufficiency, conformity, or compliance.

---

**End of Document**
