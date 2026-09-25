# Canada Public Sector GRC Requirements Annex

**Document Title:** Canada Public Sector GRC Requirements Annex\
**Document Type:** Annex\
**Version:** 0.0.11\
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

The annex is scoped to the federal public-sector authority layer and the public-sector access, privacy, and health-information layers of all ten provinces and all three territories. Clause-level content is added cluster by cluster: the federal public-sector privacy baseline in domain cluster 4 is the first; the other clusters remain foundations, and until the forthcoming Canadian authority coverage register exists, no jurisdiction is recorded as covered. It distinguishes laws from binding policies and directives, regulatory guidance, strategies, voluntary frameworks, consultation drafts, and historical or superseded sources.

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

**Applicability.** The Act's duties rest on a *government institution*, which section 3 of the Act defines as "(a) any department or ministry of state of the Government of Canada, or any body or office, listed in the schedule, and (b) any parent Crown corporation, and any wholly-owned subsidiary of such a corporation, within the meaning of section 83 of the Financial Administration Act". The Policy "and its supporting instruments apply to government institutions as defined in section 3 of the Act" (Policy section 6.1), and "does not apply to the Bank of Canada" (Policy section 6.2). The Act's duties for personal information under an institution's control remain the institution's. Policy 4.2.16 requires the head of the institution, or a delegate, to take steps to ensure that an organization serving it under contract, agreement or arrangement provides appropriate privacy protections; that organization's obligations for the information then arise from the instruments the institution uses (for example, contract terms) and from other applicable law. Where that organization is itself a government institution, the Act applies to it directly (and Part 1 of PIPEDA does not: PIPEDA paragraph 4(2)(a)); where it is a private-sector organization, its own handling of personal information in the course of commercial activity falls under PIPEDA or substantially similar provincial private-sector law, treated in the Canadian privacy annex.

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
| "This Act does not apply to confidences of the Queen’s Privy Council for Canada, including, without restricting the generality of the foregoing, any information contained in" | Subsection 70(1), opening words; its paragraphs list the kinds of confidence covered (excludes the whole Act) |
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

The federal *Access to Information Act* request workflow (clocks, extensions, exemptions and review routes) is not yet carried here; it remains a library gap below.

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

1. **Canadian public-records request workflow** with jurisdiction-specific clocks, extensions, exemptions, review routes, and disclosure logs.
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
