---
corpus-id: secrot
origin: pack
family: security
facet: SECC
secondary: [SECI]
slug: rotate-leaked-secret
map-nist-airmf-broad: [MANAGE 2.3, MANAGE 4.3]
map-nist-80053-broad: [IA-5, IR-4]
map-atlas-broad: [AML.T0012, AML.T0091.000, AML.T0091.001]
map-iso-23894-broad: [A.11]
map-owasp-mcp-broad: [MCP01]
map-owasp-cheatsheet-broad: [secrets-management]
map-csa-ccm-broad: [CEK-12, CEK-13, IAM-14, SEF-07]
map-csa-aicm-broad: [CEK-12, CEK-13, IAM-14, SEF-07]
---

# Rotate a leaked secret

A secret that reaches a remote or an external service is treated as compromised and rotated, whatever any
scanner said. Rotation happens regardless of whether the exposure was intentional, brief, or already deleted
from the destination.
