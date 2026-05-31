# Citation Verification Worklist - Batch Q3: AI Security Tooling Landscape Provenance

**Document Title:** Citation Verification Worklist: Batch Q3 (AI Security Tooling Landscape Provenance)\
**Document Type:** Worklist\
**Version:** 1.0.0\
**Date:** 2026-05-30\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/specification-citation-verification.md`](specification-citation-verification.md), [`governance/template-citation-verification-worklist.md`](template-citation-verification-worklist.md), [`governance/register-citation-verifications.md`](register-citation-verifications.md), [`governance/register-ai-security-tooling-landscape.md`](register-ai-security-tooling-landscape.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** This worklist is a per-batch working artefact; it does not have a recurring review cadence. The authoritative record is the Citation Verifications Register; the integrity anchors live in the AI Security Tooling Landscape Register's per-entry Provenance blocks.\
**Repository Path:** [`governance/worklist-citation-verification-batch-q3-ai-tooling.md`](worklist-citation-verification-batch-q3-ai-tooling.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This is the worklist for batch Q3 of citation verification under the Citation Verification Specification ([`specification-citation-verification.md`](specification-citation-verification.md)). The batch scope is the 55 Provenance blocks added to the AI Security Tooling Landscape Register ([`register-ai-security-tooling-landscape.md`](register-ai-security-tooling-landscape.md)) in Phase 23.10.

At register creation (Phase 23.7), the entries documented project scope, license, capabilities, and GRC concerns surfaced. At Phase 23.10, a Provenance block was added to each entry with AI-captured fields (Source URL, Version at assessment, Date assessed) and human-pending fields (Integrity anchor, Wayback snapshot URL). This worklist enumerates the entries whose Provenance blocks still need human verification.

The AI verifier cannot complete provenance verification because:

- `web.archive.org` is blocked at the harness level (per Citation Verification Specification §3.5).
- Commit SHA capture against a live source requires authoritative-source access the AI verifier does not have.
- Per the methodology, primary capture is the human verifier's responsibility.

---

## 2. How to use this worklist

For each row in §4:

1. Open the **Source URL** in a browser. Confirm it resolves and serves the expected project content.
2. For GitHub-hosted entries: capture the commit SHA of the default branch (or the assessed branch where specified) at the time of verification. The SHA is the **Integrity anchor**.
3. For non-GitHub web sources (commercial vendor pages): capture the SHA-256 of the page content. The SHA-256 is the **Integrity anchor**.
4. Submit the Source URL to `https://web.archive.org/save/` and record the resulting snapshot URL. Where a snapshot already exists for the verification date, the existing snapshot URL is acceptable.
5. Confirm the entry's recorded capabilities still match the current project documentation. Note any divergence in the **Divergence detail** column.
6. Assign the **Verification status** (`human-verified` if everything matches; `re-verification-due` if material divergence; `pending-resolution` if the project no longer exists or has been renamed).
7. Sign the **Captured by** column.

At batch close: notify the AI verifier with the completed worklist. The AI verifier then:

- Updates the AI Security Tooling Landscape Register's per-entry Provenance block: populates `Integrity anchor` and `Wayback snapshot URL` from the worklist; updates `Verification status` to `human-verified` (or other terminal state).
- Appends a row to the Citation Verifications Register per Specification §9 with `Standard ID` set to the tooling-register section identifier (e.g., `5.1.1` for PROMPTPurify) and `Verified Field` set to "provenance (Phase 23.10)".
- Proposes corrective edits to the tooling register's content where divergence was found.

---

## 3. Publisher URL patterns and source-capture notes

### 3.1 GitHub-hosted projects

Most entries are GitHub-hosted. For each:

- **Source URL**: `https://github.com/<owner>/<repo>` (the repository root).
- **Default branch**: typically `main`, but some projects use `master`, `develop`, or a custom name. Confirm via the repository page.
- **Commit SHA capture**: use `https://github.com/<owner>/<repo>/commits/<branch>` to view the latest commit; copy the 40-character SHA. Alternatively, use the GitHub API: `https://api.github.com/repos/<owner>/<repo>/branches/<branch>` returns the latest commit SHA.
- **Wayback submission**: `https://web.archive.org/save/https://github.com/<owner>/<repo>`. Wait for the snapshot to complete; record the resulting URL.

### 3.2 Commercial vendor pages

For entries in §5.8 of the tooling register:

- **Source URL**: the vendor product page captured at assessment time.
- **Integrity anchor (SHA-256)**: download the page HTML and compute SHA-256 of the file. The hash captures the page state at verification time.
- **Wayback submission**: same pattern as GitHub. Vendor pages change frequently; the Wayback snapshot is critical evidence.

### 3.3 Archived or unmaintained projects

For entries explicitly marked archived (rebuff, CodeGate, Vigil-LLM) or unmaintained (LLMFuzzer):

- The Source URL should still resolve; the project page should still be visible (archive flag preserves the repository).
- Commit SHA capture is still meaningful (it pins the last state before archival).
- Wayback snapshot is critical for archived projects: it preserves the page state at verification time even if the GitHub repository is later deleted by the owner.

---

## 4. Worklist

Pre-filled by the AI verifier from the AI Security Tooling Landscape Register's Provenance blocks. Captured columns are filled by the human verifier during the batch.

| Section ID | Project | Source URL | Hosting kind | Expected default branch | Captured commit SHA / page SHA-256 | Wayback snapshot URL | Capabilities still match? | Divergence detail | Captured by | Verification status | Date checked |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5.1.1 | PROMPTPurify | https://github.com/securelayer7/PROMPTPurify | github | main |  |  |  |  |  |  |  |
| 5.1.2 | Protect AI llm-guard | https://github.com/protectai/llm-guard | github | main |  |  |  |  |  |  |  |
| 5.1.3 | Protect AI rebuff (archived) | https://github.com/protectai/rebuff | github | main |  |  |  |  |  |  |  |
| 5.1.4 | ClawGuard | https://github.com/Claw-Guard/ClawGuard | github | main |  |  |  |  |  |  |  |
| 5.1.5 | CourtGuard | https://github.com/isaacwu2000/CourtGuard | github | main |  |  |  |  |  |  |  |
| 5.1.6 | NVIDIA NeMo Guardrails | https://github.com/NVIDIA/NeMo-Guardrails | github | develop |  |  |  |  |  |  |  |
| 5.1.7 | Guardrails AI | https://github.com/guardrails-ai/guardrails | github | main |  |  |  |  |  |  |  |
| 5.1.8 | Vigil-LLM (archived) | https://github.com/deadbits/vigil-llm | github | main |  |  |  |  |  |  |  |
| 5.1.9 | Stacklok CodeGate (archived) | https://github.com/stacklok/codegate | github | main |  |  |  |  |  |  |  |
| 5.1.10 | LLM Warden (jackhhao) | https://github.com/jackhhao/llm-warden | github | main |  |  |  |  |  |  |  |
| 5.1.11 | KOKOSde LocalMod | https://github.com/KOKOSde/localmod | github | main |  |  |  |  |  |  |  |
| 5.1.12 | Meta PurpleLlama bundle | https://github.com/meta-llama/PurpleLlama | github | main |  |  |  |  |  |  |  |
| 5.2.1 | promptfoo | https://github.com/promptfoo/promptfoo | github | main |  |  |  |  |  |  |  |
| 5.2.2 | NVIDIA garak | https://github.com/NVIDIA/garak | github | main |  |  |  |  |  |  |  |
| 5.2.3 | Microsoft PyRIT | https://github.com/microsoft/pyrit | github | main |  |  |  |  |  |  |  |
| 5.2.4 | Confident AI deepteam | https://github.com/confident-ai/deepteam | github | main |  |  |  |  |  |  |  |
| 5.2.5 | PISmith | https://github.com/albert-y1n/PISmith | github | main |  |  |  |  |  |  |  |
| 5.2.6 | Promptmap | https://github.com/utkusen/promptmap | github | main |  |  |  |  |  |  |  |
| 5.2.7 | ETH Zurich AgentDojo | https://github.com/ethz-spylab/agentdojo | github | main |  |  |  |  |  |  |  |
| 5.2.8 | HarmBench | https://github.com/centerforaisafety/HarmBench | github | main |  |  |  |  |  |  |  |
| 5.2.9 | Trusted-AI ART | https://github.com/Trusted-AI/adversarial-robustness-toolbox | github | main |  |  |  |  |  |  |  |
| 5.2.10 | IBM HEART | https://github.com/IBM/heart-library | github | main |  |  |  |  |  |  |  |
| 5.2.11 | Open-Prompt-Injection | https://github.com/liu00222/Open-Prompt-Injection | github | main |  |  |  |  |  |  |  |
| 5.2.12 | BCG-X ARTKIT | https://github.com/BCG-X-Official/artkit | github | main |  |  |  |  |  |  |  |
| 5.2.13 | Giskard | https://github.com/Giskard-AI/giskard | github | main |  |  |  |  |  |  |  |
| 5.2.14 | CyberArk FuzzyAI | https://github.com/cyberark/FuzzyAI | github | main |  |  |  |  |  |  |  |
| 5.2.15 | LLMFuzzer (unmaintained) | https://github.com/mnns/LLMFuzzer | github | main |  |  |  |  |  |  |  |
| 5.2.16 | AIJack | https://github.com/Koukyosyumei/AIJack | github | main |  |  |  |  |  |  |  |
| 5.2.17 | AIAPwn | https://github.com/karimhabush/aiapwn | github | main |  |  |  |  |  |  |  |
| 5.2.18 | UK AISI inspect_evals | https://github.com/UKGovernmentBEIS/inspect_evals | github | main |  |  |  |  |  |  |  |
| 5.3.1 | Protect AI modelscan | https://github.com/protectai/modelscan | github | main |  |  |  |  |  |  |  |
| 5.3.2 | Picklescan | https://github.com/mmaitre314/picklescan | github | main |  |  |  |  |  |  |  |
| 5.3.3 | Trail of Bits fickling | https://github.com/trailofbits/fickling | github | master |  |  |  |  |  |  |  |
| 5.4.1 | LangSmith SDK | https://github.com/langchain-ai/langsmith-sdk | github | main |  |  |  |  |  |  |  |
| 5.4.2 | Langfuse | https://github.com/langfuse/langfuse | github | main |  |  |  |  |  |  |  |
| 5.4.3 | Arize Phoenix | https://github.com/Arize-ai/phoenix | github | main |  |  |  |  |  |  |  |
| 5.4.4 | Helicone | https://github.com/Helicone/helicone | github | main |  |  |  |  |  |  |  |
| 5.5.1 | Lasso MCP Gateway | https://github.com/lasso-security/mcp-gateway | github | main |  |  |  |  |  |  |  |
| 5.6.1 | TikiTribe claude-secure-coding-rules | https://github.com/TikiTribe/claude-secure-coding-rules | github | main |  |  |  |  |  |  |  |
| 5.6.2 | Wiz secure-rules-files | https://github.com/wiz-sec-public/secure-rules-files | github | main |  |  |  |  |  |  |  |
| 5.6.3 | Kariedo claude-code-security-rules | https://github.com/kariedo/claude-code-security-rules | github | main |  |  |  |  |  |  |  |
| 5.7.1 | PentestGPT | https://github.com/GreyDGL/PentestGPT | github | main |  |  |  |  |  |  |  |
| 5.7.2 | PentAGI | https://github.com/vxcontrol/pentagi | github | main |  |  |  |  |  |  |  |
| 5.7.3 | AI-OPS | https://github.com/antoninoLorenzo/AI-OPS | github | main |  |  |  |  |  |  |  |
| 5.7.4 | HackSynth | https://github.com/aielte-research/HackSynth | github | main |  |  |  |  |  |  |  |
| 5.7.5 | HexStrike AI | https://github.com/0x4m4/hexstrike-ai | github | main |  |  |  |  |  |  |  |
| 5.7.6 | BurpGPT | https://github.com/aress31/burpgpt | github | main |  |  |  |  |  |  |  |
| 5.7.7 | Strix | https://github.com/usestrix/strix | github | main |  |  |  |  |  |  |  |
| 5.8.1 | Lakera Guard | https://www.lakera.ai/lakera-guard | web | n/a |  |  |  |  |  |  |  |
| 5.8.2 | PromptArmor | https://www.promptarmor.com/ | web | n/a |  |  |  |  |  |  |  |
| 5.8.3 | HiddenLayer AIM | https://www.hiddenlayer.com/platform/ai-runtime-security | web | n/a |  |  |  |  |  |  |  |
| 5.8.4 | CalypsoAI Moderator | https://moderator.calypsoai.com/solutions | web | n/a |  |  |  |  |  |  |  |
| 5.8.5 | Mindgard | https://mindgard.ai/ai-security-platform | web | n/a |  |  |  |  |  |  |  |
| 5.8.6 | SplxAI / SPLX | https://splx.ai/ | web | n/a |  |  |  |  |  |  |  |
| 5.9.1 | Awesome AI Security (brinhosa) | https://github.com/brinhosa/awesome-ai-security | github | main |  |  |  |  |  |  |  |

**Total entries in batch: 55.**

The Expected default branch column is a best-effort hint. Where the project uses a different branch name, the human verifier records the actual default branch name encountered. For Trail of Bits fickling specifically, the default branch is `master` rather than `main` (Trail of Bits convention).

---

## 5. Closing notes

| Field | Value |
| --- | --- |
| Batch identifier | Q3 - AI Security Tooling Landscape Provenance |
| Standards in batch | n/a (this is tooling registration provenance, not standards citation) |
| Tooling-register entries in batch | 55 |
| Batch opened | 2026-05-30 |
| Batch closed |  |
| Spot-check entries (per Citation Verification Specification §8.6) |  |
| Spot-check verifier |  |
| Recorded register rows |  |
| Tooling-register entries updated |  |

---

## 6. After batch close

When the batch is complete:

1. The human verifier notifies the AI verifier with the completed worklist.
2. The AI verifier updates each tooling-register entry's Provenance block: populates `Integrity anchor` and `Wayback snapshot URL`; sets `Verification status` to `human-verified` (or other terminal state per the divergence detail).
3. The AI verifier appends 55 rows to the Citation Verifications Register, one per worklist row, with `Standard ID` set to the tooling-register section identifier (e.g., `5.1.1`).
4. The AI verifier proposes corrective edits to the tooling-register content where divergence was found; the human verifier approves before commit.
5. The worklist file is archived or deleted at maintainer preference; the authoritative records are the updated Provenance blocks in the tooling register and the rows in the Citation Verifications Register.

---

**End of Document**
