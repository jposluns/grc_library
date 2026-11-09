---
corpus-id: secmin
origin: pack
family: security
facet: SECP
secondary: [SECC]
slug: data-minimization
map-cwe-tight: [CWE-201]
map-cwe-broad: [CWE-359]
map-nist-airmf-broad: [MAP 4.2]
map-nist-80053-tight: [SI-12(1)]
map-nist-80053-broad: [SI-19]
map-atlas-broad: [AML.T0057]
map-iso-23894-broad: [A.8]
map-owasp-llm-broad: [LLM02]
map-owasp-asvs-broad: [V14]
map-csa-ccm-broad: [DSP-08, DSP-12, DSP-17]
map-csa-aicm-broad: [DSP-08, DSP-12, DSP-17, DSP-22]
---

# Minimize personal data sent to AI services

Only the personal and sensitive data a task genuinely needs is sent to or retained by an AI service, and
minimizing what is exposed is preferred to controlling exposure after the fact. What is sent is redacted or
pseudonymized before it leaves the trust boundary wherever practical.
