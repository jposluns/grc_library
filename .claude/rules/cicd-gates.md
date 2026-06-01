---
paths:
  - ".github/workflows/**"
  - ".pre-commit-config.yaml"
  - "tools/**"
---

<!-- Source: dev-security/claude-rules/pipeline/cicd-gates.md (GRC Library, CC BY-SA 4.0). Copied verbatim for this project; security requirements unchanged. Path-scoped to this repo's CI/CD surfaces. -->

# CI/CD Pipeline Security Gates

These rules apply to DevOps engineers configuring CI/CD pipelines for any language, platform, or cloud provider.

---

## Mandatory gate order

Every pipeline deploying to Test or Production must run these gates in this order. A failure at any gate halts the pipeline.

```
1. Secret scanning          → Fail on any detected secret
2. SAST                     → Fail on Critical or High findings
3. SCA (dependency scan)    → Fail on Critical CVE
4. Container image scan     → Fail on Critical CVE in image or base layer (if containers)
5. IaC scan                 → Fail on Critical misconfiguration (if IaC present)
6. Licence compliance       → Fail on unapproved copyleft licence (GPL/AGPL without Legal approval)
7. Runtime EOL check        → Fail on deployment to EOL runtime version
8. SBOM generation          → Generate and archive on every production build
9. Artefact signing         → Sign all production build artefacts
10. Manual approval          → Require human approval before production deployment
```

---

## Secret scanning

- Scan all files in the repository, not just changed files
- Scan git history on first configuration, then new commits incrementally
- Fail the build immediately on any detected secret: do not allow override without CISO approval
- Patterns to detect: API keys, private keys, connection strings, OAuth tokens, cloud credentials, certificate private key material
- Recommended tools: TruffleHog, detect-secrets, GitLeaks, or equivalent

---

## SAST configuration

- Configure SAST to run on the full codebase, not just changed files, on protected branch merges
- Threshold: Critical → fail; High → fail; Medium → warn and track
- Do not use blanket `# nosec` or equivalent suppressions without documented rationale reviewed by the security team
- Retain SAST results as acceptance-into-service gate evidence

---

## SCA (software composition analysis)

- Scan all dependencies including transitive dependencies
- Critical CVE in any dependency: fail immediately
- High CVE: fail unless a tracked issue exists with remediation within 14 days
- Verify dependency names resolve in approved registries (detect typosquatting and dependency confusion)
- Generate and retain SBOM on every production build (CycloneDX or SPDX format)

---

## Container image scanning

- Scan base images before first use and on a scheduled cadence (weekly minimum)
- Scan every image build, not just base image pulls
- Critical CVE in image or any layer: fail
- Enforce: no root user; no privileged mode in production; no `:latest` tag in Test or Production
- Sign all production images using a signing key stored in the secrets management service

---

## IaC scanning

- Scan Terraform, Bicep, CloudFormation, Kubernetes manifests, and Helm charts
- Critical findings (open storage buckets, disabled encryption, open security groups): fail
- High findings: fail unless tracked with remediation timeline
- Verify: encryption explicitly configured; network access explicitly restricted; logging enabled; resource tagging applied

---

## Runtime EOL gate

- Maintain a list of approved runtime versions (node, python, dotnet, java, ruby, go, etc.)
- Fail the pipeline if the configured runtime version has passed its vendor EOL date
- Update the approved version list within 30 days of any new EOL date announcement
- Cloud governance policy enforcement and pipeline gate are both required: one does not substitute for the other

---

## Pipeline identity and authorization

- The pipeline runs as a dedicated service identity, not a human account
- The pipeline identity must not be able to approve its own production deployments
- Use managed identity or a PAM-vaulted service account with minimum permissions
- Service connection credentials are stored in the CI/CD platform's secrets mechanism, not in pipeline YAML
- Audit all pipeline permission changes: changes to pipeline service identity permissions require security team review

---

## Branch protection requirements

Protected branches feeding Test or Production pipelines must enforce:
- Minimum 1 required reviewer before merge (2 for security-sensitive repositories)
- No direct push to protected branches (force push prohibited)
- SAST, SCA, and secret scanning must pass before merge is permitted
- Branch deletion restricted to repository administrators

---

## Production deployment approval

- Production deployments require manual approval from a designated approver who is not the pipeline author
- The approval event is recorded in the CI/CD audit log
- Emergency deployments: approval may be asynchronous but must be obtained within 4 hours and documented
- Artefact signature must be verified before deployment: deploy nothing with an invalid or absent signature

---

## Pipeline as code security

Pipeline definition files (YAML, JSON, HCL) must:
- Be stored in version control: no manual pipeline configuration
- Not contain hard-coded credentials, tokens, or secrets
- Not contain logic that disables or bypasses security gates
- Be subject to code review before changes take effect on protected branches
- Never fetch and execute untrusted scripts from external URLs at runtime

---

## Framework alignment

| Gate | CSA CCM | NIST SSDF | ISO 27001 | SLSA |
| --- | --- | --- | --- | --- |
| Secret scanning | CEK-10 to 21 | PW.8.2 | A.8.10 | Level 2 |
| SAST | AIS-04 | VE.1 | A.8.29 | Level 2 |
| SCA | TVM-06 | PO.5, PW.4 | A.8.8 | Level 2 |
| Container scan | IVS-04 | VE.1 | A.8.8 | Level 2 |
| IaC scan | CCC-06 | PW.9 | A.8.9 | N/A |
| Artefact signing | CCC-04 to 05 | DS.2 | A.8.27 | Level 3 |
| Manual approval | CCC-01 to 03 | N/A | A.8.32 | Level 2 |
| Branch protection | CCC-04 | PO.5 | A.8.32 | Level 2 |
