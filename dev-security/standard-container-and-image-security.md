# Container and Image Security Standard

**Document Title:** Container and Image Security Standard\
**Document Type:** Standard\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md), [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`dev-security/standard-devops-security-requirements.md`](standard-devops-security-requirements.md), [`dev-security/standard-software-composition-analysis.md`](standard-software-composition-analysis.md), [`operations/standard-production-security-requirements.md`](../operations/standard-production-security-requirements.md), [`operations/standard-cloud-security-configuration-baseline.md`](../operations/standard-cloud-security-configuration-baseline.md), [`operations/procedure-patch-management.md`](../operations/procedure-patch-management.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md), [`supply-chain/register-sbom.md`](../supply-chain/register-sbom.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** Annual and upon material change to container platforms, runtime, or supply-chain practice\
**Repository Path:** [`dev-security/standard-container-and-image-security.md`](standard-container-and-image-security.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This standard defines the security controls applied to container images, container runtimes, image registries, and the supply chain that produces and distributes images. It covers Linux containers (Docker, OCI), Windows containers, Kubernetes and equivalent orchestrators, serverless container platforms, and the secure-build pipelines that produce images.

---

## Scope

This standard applies to every container image built, stored, distributed, or executed by the organisation, in any environment from developer workstations through production. It applies regardless of whether the orchestrator is self-managed, managed by a cloud provider, or operated by a third party.

---

## Section 1: image build

| Control area | Requirement |
| --- | --- |
| Base images | Sourced from approved registries; minimal images (distroless, Alpine, Wolfi, or vendor minimal) preferred; vendor-supported base only |
| Reproducibility | Build pipelines produce reproducible images where the language and toolchain allow; build-time inputs version-pinned |
| Multi-stage builds | Multi-stage builds used to exclude build tools from final images |
| Image identity | Each image has a unique digest; tags are mutable references, digests are immutable; production deployments pin by digest |
| User identity | Containers run as a non-root user; explicit `USER` directive in the image |
| File-system permissions | Read-only root filesystem where the application allows |
| Secrets | No secrets in image layers, environment variables baked into images, or build arguments persisted in metadata |
| Vendor scanning | Build pipelines fail on Critical vulnerabilities per the SCA standard |
| Signing | Images signed before push using Sigstore Cosign, Notation, or equivalent; signatures verified at pull and at admission |
| SBOM | Per the SBOM register; SBOM generated for every image and attached as an attestation |
| Provenance | Build provenance attestation produced per SLSA Build Level 3 target |
| Image hardening | Unnecessary packages removed; setuid binaries removed; init system minimized |

---

## Section 2: image registry

| Control area | Requirement |
| --- | --- |
| Authoritative registry | Production images are pulled only from approved registries; no `:latest` or public-registry pulls in production |
| Authentication | Registry access authenticated with short-lived credentials; long-lived registry credentials prohibited |
| Authorisation | Per-repository RBAC; least-privilege push and pull |
| Image scanning at rest | Registry continuously scans stored images against new vulnerability data; scan output integrated with the vulnerability programme |
| Image immutability | Tags immutable where the registry supports it; mutable tags retire after a defined window |
| Retention | Defined retention; superseded images garbage-collected; provenance attestations retained alongside images |
| Geo-redundancy | Production registry has documented replication and recovery objectives |
| Air-gap and offline support | Where the deployment requires air-gapped operation, image distribution to the air-gapped registry follows a documented secure-transfer procedure |

---

## Section 3: runtime

| Control area | Requirement |
| --- | --- |
| Admission control | Cluster admission control verifies image signature, SBOM presence, base image, registry origin, and policy compliance before workload acceptance |
| Pod security | Pod security standards baseline at minimum; restricted level preferred for application workloads |
| Privilege restriction | Privileged containers prohibited in application workloads; `hostNetwork`, `hostPID`, `hostIPC` prohibited |
| Capability dropping | Linux capabilities dropped to minimum required; ambient capabilities not granted |
| Seccomp and AppArmor | Default seccomp profiles applied; targeted profiles for high-sensitivity workloads |
| Read-only file system | Applied at the workload level where the application supports it |
| Resource limits | CPU, memory, ephemeral storage limits set; exceeded limits trigger eviction |
| Network policy | Default-deny network policy; explicit allow rules for required traffic |
| Service mesh | Optional but recommended; provides mTLS, identity, and policy enforcement |
| Workload identity | Federated workload identity preferred over static credentials |
| Secrets injection | Secrets injected at runtime from the secrets management service; not from environment variables baked into images |
| Logging | Container stdout and stderr forwarded to the centralized log platform; sensitive content masked |

---

## Section 4: orchestrator security

| Control area | Requirement |
| --- | --- |
| Control plane | Encrypted at rest (etcd); access via authenticated and audited paths only |
| API server | Audit logging enabled with the most-verbose level appropriate to the workload sensitivity |
| RBAC | Least-privilege RBAC; impersonation and `*` verbs restricted |
| Cluster authentication | Federated identity for human operators; service accounts scoped per workload |
| Cluster upgrades | Within the vendor-supported version; controlled upgrades following the change management procedure |
| Add-on hygiene | Cluster add-ons (DNS, ingress, monitoring) treated as production software with their own SBOM, scanning, and signing |
| Multi-tenancy | Where the cluster is multi-tenant, namespace isolation plus network policy plus resource quota enforce tenancy |
| Disaster recovery | Per the resilience programme |

---

## Section 5: developer workflow

| Control area | Requirement |
| --- | --- |
| Local development | Developers can run containers locally; local images do not need to meet the production signing requirements |
| Production-image awareness | Developers building images for production are aware of the production requirements; image-build templates encode them by default |
| Pre-commit scanning | IDE plugins or pre-commit hooks scan Dockerfiles for known anti-patterns |
| Build pipeline | Per the DevOps security standard; produces signed images with attestations |
| Local-to-production gap | Local images and production images use the same base; local cannot bypass production gates |

---

## Section 6: serverless container platforms

| Control area | Requirement |
| --- | --- |
| Provider configuration | Provider-native security configuration applied (IAM, network, logging, identity) |
| Image source | Pulled from the approved registry; not from public registries in production |
| Cold-start considerations | Secret retrieval at cold start uses workload identity; not embedded |
| Concurrency and timeout | Configured per the application and per cost-governance constraints |
| Observability | Function-level logs and metrics integrated with the SIEM |

---

## Section 7: supply-chain integrity

| Control area | Requirement |
| --- | --- |
| Build-pipeline security | Build pipelines run on hardened agents; pipeline definitions in code with peer review |
| Attestation | Build provenance, vulnerability scan, SBOM, and signature attestations produced per build; verifiable end to end |
| Dependency pinning | Base images, language dependencies, OS packages pinned to digests or specific versions |
| Source-of-truth registry | Each artefact's provenance traceable to the source repository and commit |
| Sigstore or equivalent | Transparency log used where the platform supports it |
| Tool-chain integrity | Compiler, build tools, and CI runner integrity verified |
| Insider-risk safeguards | Build secrets accessible only to the build identity; tampering with build artefacts logged and alerted |

---

## Section 8: vulnerability management

| Control area | Requirement |
| --- | --- |
| Build-time scanning | Per the SCA standard |
| Registry rescanning | Continuous as new vulnerability data appears |
| Runtime scanning | Optional but recommended for high-sensitivity workloads |
| Patching SLAs | Per the patch management procedure; container images rebuilt and redeployed per the SLA |
| Base-image refresh | Base images rebuilt on a defined cadence regardless of CVE pressure |
| EOL handling | EOL base images and runtimes treated per the runtime EOL classification in the security baseline standard |

---

## Section 9: data handling in containers

| Control area | Requirement |
| --- | --- |
| Persistent storage | External to the container; volumes encrypted at rest |
| Personal data handling | Containers processing personal data follow the data classification standard; ROPA updated |
| Cross-container data flows | Service mesh or network policy enforces flows; sensitive flows audit-logged |
| Backup | Per the resilience programme; container-resident data backed up via the underlying storage class |

---

## Section 10: incident response readiness

| Control area | Requirement |
| --- | --- |
| Forensic readiness | Persistent storage and logs retained long enough to support investigation per the IR procedure |
| Runtime snapshot capability | Capability to snapshot a running container for forensic analysis is documented |
| Image quarantine | Compromised images are quarantined; admission control prevents redeployment until cleared |
| Kill switch | Workload-level disable mechanism documented per service |
| Recovery | Per the recovery runbook template |

---

## Operating expectations

1. New container workloads accept this standard as a gating criterion before production deployment.
2. The container platform is treated as production infrastructure; cluster upgrades, add-on changes, and policy changes follow the change management procedure.
3. Quarterly review of orchestrator and registry configuration against current CIS Benchmarks.
4. Annual tabletop exercise covering a container-supply-chain incident scenario.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| NIST SP 800-190 | Application Container Security Guide | US federal baseline |
| NIST SP 800-204 series | Microservices security, service mesh, DevSecOps | Cross-walk |
| CIS Benchmarks | Docker, Kubernetes, vendor-specific | Configuration baselines |
| CNCF Cloud Native Security Whitepaper v2 | CNCF | Cloud-native foundations |
| SLSA | Supply-chain Levels for Software Artifacts | Build provenance |
| Sigstore | Open source signing and transparency | Signing and attestation |
| CycloneDX, SPDX | SBOM formats | Cross-walk |
| OWASP Container Security Verification Standard | OWASP | Practical requirements |
| Kubernetes Pod Security Standards | Kubernetes | Pod security baseline |
| MITRE ATT&CK (Containers) | MITRE | Threat coverage |
| ISO/IEC 27001:2022 | A.8.7, A.8.8, A.8.25 to A.8.34 | Vulnerability and secure development |

---

## Limitations

This standard is a public-domain baseline. Specific orchestrator and platform configurations evolve rapidly; the standard expresses requirements rather than vendor-specific settings. Adopting organisations select the appropriate CIS Benchmark profile (Level 1 typical, Level 2 high-security) and tune to their workload.

---

**End of Document**
