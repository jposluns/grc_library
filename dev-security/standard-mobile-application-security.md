# Mobile Application Security Standard

**Document Title:** Mobile Application Security Standard 
**Document Type:** Standard 
**Version:** 0.0.1 
**Date:** 2026-05-28 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md), [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`dev-security/standard-software-composition-analysis.md`](standard-software-composition-analysis.md), [`dev-security/standard-api-security.md`](standard-api-security.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`security/standard-endpoint-hardening.md`](../security/standard-endpoint-hardening.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`privacy/framework-childrens-data.md`](../privacy/framework-childrens-data.md) 
**Classification:** Public 
**Category:** Developer Security 
**Review Frequency:** Annual and upon material change to mobile platforms, threat-pattern, or store-policy expectations 
**Repository Path:** [`dev-security/standard-mobile-application-security.md`](standard-mobile-application-security.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines the security controls applied to mobile applications the organisation develops, publishes, or significantly customises. It covers iOS and Android applications; mobile-web is governed by the API security standard plus the web-application standards in the dev-security domain.

---

## Scope

This standard applies to:

1. Native and cross-platform mobile applications published by the organisation to public application stores.
2. Enterprise (in-house distributed) mobile applications.
3. Embedded SDKs distributed to other organisations for inclusion in their applications.
4. Mobile clients of internally-built backend services.

It does not cover the device-management posture for organisationally-issued devices (governed by the endpoint hardening standard) or BYOD posture (governed by the BYOD policy).

---

## Section 1: platform alignment

The standard aligns to the OWASP Mobile Application Security Verification Standard (MASVS) v2 conceptual verification levels.

| MASVS-L1 | Standard mobile application security |
| --- | --- |
| MASVS-L2 | Defence-in-depth |
| MASVS-R | Resilience against reverse engineering |

Note on MASVS v2 structure: MASVS v2 reorganised the operational test groupings into MAS Testing Profiles in the Mobile Application Security Testing Guide (MASTG). The L1, L2, and R concepts remain as verification-level shorthand; this standard uses them as such while pointing implementers to MASTG for the concrete test catalogue.

Applications classified by sensitivity tier determine the verification level applied.

| Sensitivity tier | Verification level |
| --- | --- |
| Tier 1: Critical (handles payment, regulated data, authentication, safety-critical functions) | MASVS-L2 plus MASVS-R |
| Tier 2: High (handles personal data; significant business function) | MASVS-L2 |
| Tier 3: Standard (general consumer app) | MASVS-L1 |
| Tier 4: Low (information-only, no sensitive data) | MASVS-L1 |

---

## Section 2: storage

| Control area | Requirement |
| --- | --- |
| Sensitive data at rest | Encrypted using platform key stores (iOS Keychain, Android Keystore); never in plain shared preferences, files, or databases |
| Class-conformant storage | iOS data protection classes selected appropriately (e.g. Complete Until First User Authentication); Android equivalent with EncryptedSharedPreferences / EncryptedFile |
| Caches and temporary files | No sensitive data in temporary or unencrypted caches; cache cleared on logout |
| Backup exclusion | Sensitive data excluded from cloud backup where the platform supports it; allow-list approach |
| Logs and crash reports | No sensitive data in logs; crash reporters configured to redact PII and credentials |
| Pasteboard and screenshots | Sensitive fields excluded from screenshots and pasteboard where the platform supports it |
| External storage | Personal data not written to shared or external storage |

---

## Section 3: cryptography

| Control area | Requirement |
| --- | --- |
| Algorithm selection | Per the encryption policy; deprecated algorithms prohibited |
| Key generation | Hardware-backed where available (Secure Enclave, StrongBox) |
| Key storage | Platform key store only; no keys in code, resources, or shared storage |
| Random number generation | Platform-provided cryptographically secure RNG |
| Network cryptography | TLS 1.2 minimum; TLS 1.3 preferred; ATS / Network Security Config enforce HTTPS |
| Certificate pinning | Implemented for Tier 1 and Tier 2 applications; backup pins and rotation plan documented |
| Custom cryptography | Prohibited; rely on platform and audited libraries |

---

## Section 4: authentication and authorisation

| Control area | Requirement |
| --- | --- |
| Authentication strength | Per the authentication standard; mobile clients support phishing-resistant authentication where the backend supports it |
| Local authentication | Biometric authentication (Face ID, Touch ID, Android BiometricPrompt) used for re-authentication, not as the sole credential |
| Session management | Tokens stored in the platform key store; refresh on use; revocation honoured |
| Step-up | Sensitive operations re-authenticate the user; biometric step-up acceptable for low-value steps, full authentication for high-value |
| Logout | Logout clears all session material; remote logout supported via push or platform-native mechanism |
| Multi-tenant separation | Where the application supports multiple accounts, accounts are isolated in storage and session |
| Out-of-band push for authentication | Push challenges include enough context to prevent push-fatigue confusion |

---

## Section 5: network communication

| Control area | Requirement |
| --- | --- |
| HTTPS-only | iOS App Transport Security (ATS) and Android Network Security Configuration enforce HTTPS; exceptions documented |
| Backend API security | Per the API security standard |
| Domain restriction | Network requests restricted to declared backend domains |
| WebView hardening | If WebView is used, JavaScript bridge restricted; URL allow-list applied; mixed content disabled |
| Third-party SDK network access | SDKs are inventoried and reviewed for their network behaviour |
| Offline operation | Sensitive operations require connectivity unless explicitly designed for offline; offline data follows the storage controls |

---

## Section 6: platform interaction

| Control area | Requirement |
| --- | --- |
| Inter-application communication | Deep links validated; URL schemes authenticated; data shared via intents and extensions sanitised |
| Custom URL schemes and universal links | Authenticated where they trigger sensitive actions; replay-protected |
| App permissions | Minimum required; rationale shown to the user; never-asks-twice respected |
| Background execution | Sensitive operations not performed in the background without justification |
| Notifications | Sensitive content not visible on lock screen; rich notification content classification-aware |
| Clipboard | Sensitive data not auto-copied; pasteboard usage clearly indicated |
| Accessibility services | If used, scope minimized; rationale documented |
| Drag-and-drop | Sensitive content not draggable to other applications by default |

---

## Section 7: code quality and reverse-engineering resistance (MASVS-R)

Required for Tier 1 applications; recommended for Tier 2.

| Control area | Requirement |
| --- | --- |
| Anti-tampering | Integrity checks on critical code paths; runtime detection of modification |
| Anti-debugging | Detection of attached debugger in production; behaviour-modification under detection |
| Root and jailbreak detection | Detection with graceful degradation; legitimate developer modes accommodated |
| Obfuscation | Class, method, and string obfuscation in release builds; not as the sole defence |
| Hooking and frame-injection detection | Detection of common dynamic analysis tools |
| Emulator detection | Detection of common emulators; behaviour adjustment under detection |
| Anti-reversing native code | Symbol stripping; native-code anti-tamper for critical components |

Resilience controls reduce ease of attack; they do not replace fundamental security. Defence in depth applies.

---

## Section 8: third-party SDKs

| Control area | Requirement |
| --- | --- |
| Inventory | All bundled SDKs inventoried with version, vendor, purpose, data accessed |
| Supplier assessment | Per the supplier security and privacy assurance standard |
| Permission scope | SDK requests only the permissions necessary; broader permissions removed or replaced |
| Network behaviour | SDK network destinations monitored; unexpected destinations investigated |
| Update cadence | SDKs updated per the patch management procedure |
| Removal path | Each bundled SDK has a documented removal path if the supplier or its behaviour becomes unacceptable |
| Privacy disclosure | Per the privacy notice; app-store privacy labels accurately reflect SDK behaviour |

---

## Section 9: store and distribution

| Control area | Requirement |
| --- | --- |
| App-store-specific posture | iOS App Store and Google Play policy compliance; per-store privacy labels accurate |
| Build signing | Production signing keys held in the secrets management service or platform key vault; release signing privileged action |
| Enterprise distribution | Enterprise certificates managed with the same rigour as code-signing root keys |
| Update mechanism | Updates delivered via the store; no side-channel updates that bypass store review |
| Forced upgrade | Tier 1 apps support forced upgrade for security-critical releases |
| Beta and TestFlight | Beta builds excluded from production data; testers are organisation-managed |

---

## Section 10: privacy

| Control area | Requirement |
| --- | --- |
| Privacy notice | Per the privacy notice template |
| Just-in-time consent | Per the consent management framework; permission prompts include rationale |
| Children's data | Per the children's data framework; age gating and parental-consent flows where applicable |
| App-tracking-transparency / privacy permissions | iOS ATT and Android privacy controls respected; deceptive prompts prohibited |
| Identifiers | Advertising identifier use minimized; first-party identifiers used only with consent |
| ROPA | Mobile-app processing recorded |
| Cross-border transfer | Per the cross-border data flow register where backend or third-party SDKs transfer data internationally |

---

## Section 11: testing

| Control area | Requirement |
| --- | --- |
| SAST | Static analysis with mobile-specific rules in CI |
| DAST and MAST | Mobile Application Security Testing on pre-release builds; per OWASP MASTG |
| Penetration testing | Annual for Tier 1; per the penetration testing standard |
| Pre-release scanning | Store-pre-flight scanning; reproducible build verification where applicable |
| Adversarial evaluation | For applications consuming AI features, AI-specific tests per the AI red team report template |

---

## Section 12: incident readiness

| Control area | Requirement |
| --- | --- |
| Telemetry | Crash and behaviour telemetry forwarded per the logging standard |
| Vulnerability disclosure | Per the security defect reporting path in SECURITY.md |
| Rapid response | Critical patches can be released through the standard store path within the regulatory window |
| Backend kill switch | Sensitive backend features can be remotely disabled where the mobile client supports it |
| Customer communication | Per the resilience programme communications |

---

## Operating expectations

1. New mobile applications target MASVS-L1 at minimum; tier classification determines whether L2 and R apply.
2. Annual review against the current MASVS and platform-store policy.
3. Third-party SDK inventory refreshed at every release.
4. Code-signing material treated as high-sensitivity per the cryptographic key lifecycle.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| OWASP MASVS v2 | L1, L2, R | Mobile verification standard |
| OWASP MASTG | Mobile testing guide | Test methodology |
| OWASP Mobile Top 10 | Threat taxonomy | Threat coverage |
| Apple Platform Security and App Store Review Guidelines | Apple | iOS platform |
| Android Enterprise security model and Play Console policy | Android | Android platform |
| NIST SP 800-163 Rev 1 | Vetting the Security of Mobile Applications | US baseline |
| NIST SP 800-124 Rev 2 | Managing the Security of Mobile Devices | Endpoint cross-walk |
| ISO/IEC 27001:2022 | A.5.10, A.8.21, A.8.25 to A.8.34 | Information transfer; secure development |
| GDPR / UK GDPR / equivalents | Privacy framework | Privacy compliance |
| ATT&CK (Mobile) | MITRE | Threat coverage |

---

## Limitations

This standard is a public-domain baseline. Mobile platforms and store policies change frequently; the standard expresses requirements rather than vendor-specific implementations. Adopting organisations select the appropriate MASVS verification level per application tier and confirm current platform-store policy at each release.

---

**End of Document**
