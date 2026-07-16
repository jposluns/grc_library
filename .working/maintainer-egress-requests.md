# Maintainer egress requests

**Version:** 1.0.0\
**Date:** 2026-07-16\
**License:** CC BY-SA 4.0

Standing queue of reference documents the assistant needs but **cannot fetch from this
environment** (egress-blocked: canada.ca / many gc.ca hosts return a WAF access-rejection to
datacenter IPs, the DD-10 known issue; also paywalled or licensed sources). The maintainer,
who has ordinary browser access, downloads the listed items and drops them at the stated
**destination**, after which the assistant (or a worker) ingests / re-verifies them.

Maintainer-directed 2026-07-16: "Create a file with all the links you want me to download and
drop somewhere ... Use that file in future for anything you can't get that you want me to
download for you."

## How this file is used

1. The assistant adds a dated request block under **Pending** with, per item: the exact
   instrument **title** (searchable), the issuing **body**, the **held edition** the ref base
   currently records (so the maintainer can tell whether a fresh copy is even newer), the ref
   **path** of the held copy (if any), the **reason** it is needed, and a **URL** only where a
   verified one is available (the assistant does not fabricate URLs; where the ref base records
   none and no reliable one is embedded, the item is listed by title for the maintainer to
   locate).
2. The maintainer downloads each item and drops it at the **destination** below.
3. The assistant / a worker ingests or re-verifies, then moves the block to **Fulfilled** with
   the ingest/verify outcome.

## Destination (confirmed 2026-07-16)

**`grc_library_ref/ingest/`** (the reference-base ingest directory). These are reference
sources that belong in `grc_library_ref`; the ingest workflow (dedupe, identify, bucket,
extract to `--full-text.md`, catalogue, regenerate indexes, run the ref gate; see the
`grc_library_ref` `CONTRIBUTING.md` and the `multi-session-orchestration` runbook §6) processes
whatever is dropped there. Drop the original (PDF/HTML) named clearly; the assistant handles
extraction and cataloguing. (If a future request is corpus-only or scratch-only, the assistant
will name a different destination in that block.)

---

## Pending

### 2026-07-16 - Canada.ca sources for TODO §2.22 (reference-utilization apply; Canada expert review)

**Context.** The credit-offload worker delivery `canada-ca-reference-breadth` proposes citation-grade
pairings of ~16 Canada.ca instruments to corpus documents (TODO §2.22). All are held in
`grc_library_ref` with editions confirmed at ingest on 2026-07-15, but canada.ca blocks automated
re-fetch from this environment (confirmed 2026-07-16: `tbs-sct.canada.ca` returns a WAF rejection),
so the assistant cannot re-verify currency at apply. For an expert-review-bound change the maintainer
elected to download fresh copies personally. **What is needed:** the current canonical version of each
instrument below, so currency is confirmed (and any newer edition is captured) before the §2.22
citations are applied. Drop each into `grc_library_ref/ingest/`.

The ref base records **no `upstream_url`** for these and embedded URLs in the extracted text are
truncated/OCR-artifacted, so items are listed by exact title + held edition for the maintainer to
locate on canada.ca; two reliable URL leads are given where extraction produced a usable one (verify
before trusting).

**Treasury Board of Canada Secretariat (TBS) / GC:**

1. **Guide on the Use of Agentic Artificial Intelligence** - held edition "modified 2026-05-22"; ref `frameworks/Canada-TBS/Canada-TBS-Guide-on-the-use-of-agentic-AI--full-text.md`. URL lead (verify, possibly truncated in extraction): `https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/guide-use-agentic-artificial-intelligence.html`. Needed for §2.22 A1/A2 (agentic-AI standards).
2. **Guide on the Use of Generative AI ("Generative AI in Your Daily Work")** - held edition "guide"; ref `frameworks/Canada-TBS/Canada-TBS-Generative-AI-in-Your-Daily-Work--full-text.md`. Needed for §2.22 A11 (ethical AI guideline; the FASTER principles).
3. **Event Logging Guidance** - held edition "2025-12-08"; ref `frameworks/Canada-TBS/Canada-TBS-Event-Logging-Guidance--full-text.md`. Needed for §2.22 A4 (logging retention numbers - value-specific, so currency matters).
4. **Patch Management Guidance** - held edition "2025-12-08"; ref `frameworks/Canada-TBS/Canada-TBS-Patch-Management-Guidance--full-text.md`. Needed for §2.22 A5 (patch-window numbers - value-specific).
5. **GC Cyber Security Event Management Plan (GC CSEMP)** - held edition "modified 2026-05-20"; ref `frameworks/Canada-TBS/Canada-TBS-GC-Cyber-Security-Event-Management-Plan-CSEMP--full-text.md`. Needed for §2.22 A6 (IR timeframes - value-specific).
6. **Policy on Privacy Protection** - held edition "2024-10-09"; ref `frameworks/Canada-TBS/Canada-TBS-Policy-on-Privacy-Protection--full-text.md`. Needed for §2.22 A9 (federal Privacy Act limb; public-sector annex).
7. **Policy on Access to Information** - held edition "2023"; ref `frameworks/Canada-TBS/Canada-TBS-Policy-on-Access-to-Information--full-text.md`. Needed for §2.22 A10 (public-sector FOI).
8. **Policy on Service and Digital** - held edition "amended 2025-08-29"; ref `frameworks/Canada-TBS/Canada-TBS-Policy-on-Service-and-Digital--full-text.md`. Needed for §2.22 B4 (AI-annex provenance anchor).

**Canadian Centre for Cyber Security (CCCS):**

9. **Baseline Security Requirements for Network Security Zones (ITSP.80.022)** - held edition "version 2.0, effective 2021-01-12 (confirmed current upstream 2026-07-15)"; ref `frameworks/Canada-CCCS/Canada-CCCS-ITSP-80-022-Baseline-Security-Requirements-Network-Security-Zones--full-text.md`. Needed for §2.22 A3 (network-zone control).
10. **Medium Cloud Control Profile (ITSP.50.103, Annex B)** - **NOT currently held**. The delivery flags that the held "GC Security Control Profile for Cloud-based GC Services" (2016; ref `frameworks/Canada-CCCS/...Cloud-based-GC-Services--full-text.md`) has its Appendix A control list SUPERSEDED by ITSP.50.103 Annex B. If cloud-control material is to be cited, ITSP.50.103 is the current instrument and should be ingested. Please download ITSP.50.103 (the current Cloud Medium profile) if available.

**Office of the Privacy Commissioner (OPC):**

11. **PIPEDA Fair Information Principles** - held edition "2025-05-29"; ref `frameworks/Canada-OPC/Canada-OPC-PIPEDA-Fair-Information-Principles--full-text.md`. URL lead (verify): `https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/`. Needed for §2.22 A8 (the 10 fair-information principles behind the Canada privacy annex's Schedule-1 statement).
12. **Personal Information Retention and Disposal: Principles and Best Practices** - held edition "2025-08-11"; ref `frameworks/Canada-OPC/Canada-OPC-Personal-Information-Retention-and-Disposal--full-text.md`. Needed for §2.22 A12 (secure-disposal methods).

**GC AI programs (provenance anchors for the Canada AI annex, §2.22 B1-B3):**

13. **AI Strategy for the Federal Public Service 2025-2027** - held edition "published 2025-03-04; ISBN 978-0-660-76811-3"; ref `programs/Canada-AI-Strategy-FPS/Canada-AI-Strategy-Federal-Public-Service-2025-2027--full-text.md`.
14. **Government of Canada AI Register (MVP)** - held edition "MVP; published 2025-11-28; modified 2026-04-28"; ref `programs/Canada-AI-Register/Canada-GC-AI-Register-MVP--full-text.md`.
15. **Progress on AI in Government** - held edition "modified 2025-11-28"; ref `programs/Canada-AI-Strategy-FPS/Canada-Progress-on-AI-in-Government--full-text.md`.

**Australia ASD/ACSC (co-sealed by CCCS; not canada.ca, may already be fetchable, listed for completeness):**

16. **Choosing Secure and Verifiable Technologies (2024)** - held edition "December 2024"; ref `frameworks/Australia-ASD/Australia-ASD-Choosing-Secure-and-Verifiable-Technologies--full-text.md`. Needed for §2.22 A7 (supplier onboarding/assurance).

**Priority for the expert review:** items 1-2 and 13-15 (the AI-cluster: agentic + generative guides and
the three GC AI-program provenance sources) are the highest-value, since the AI annex is the expert-review
focus. Items 3-5 are value-specific (numbers), so their currency matters most for accuracy. The rest are
name-level citations where the held 2026-07-15 editions are already recent.

## Fulfilled

(none yet)
