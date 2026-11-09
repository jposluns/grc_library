---
corpus-id: secvde
origin: pack
family: security
facet: SECI
secondary: [ACCUR]
slug: verify-dependency-exists
map-cwe-broad: [CWE-1357]
map-nist-airmf-broad: [GOVERN 6.1, MANAGE 3.1]
map-nist-ssdf-broad: [PW.4.1]
map-atlas-broad: [AML.T0011.001]
map-iso-23894-broad: [A.11, B.5]
map-owasp-llm-broad: [LLM04]
map-csa-ccm-broad: [STA-01, UEM-02]
map-csa-aicm-broad: [UEM-02]
---

# Verify a dependency exists before adding it

A dependency the assistant proposes is verified to exist in an approved registry before it is added, so an
invented or typosquatted package name is never introduced. Existence and identity are confirmed against the
registry itself, not assumed from a plausible-looking name in generated text.
