# Jakarta EE Application Security Standard

**Document Title:** Jakarta EE Application Security Standard\
**Document Type:** Standard\
**Version:** 0.0.4\
**Date:** 2026-09-25\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md), [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`dev-security/standard-api-security.md`](standard-api-security.md), [`dev-security/standard-software-composition-analysis.md`](standard-software-composition-analysis.md), [`dev-security/standard-container-and-image-security.md`](standard-container-and-image-security.md), [`dev-security/procedure-secure-code-review.md`](procedure-secure-code-review.md), [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md), [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md), [`operations/procedure-patch-management.md`](../operations/procedure-patch-management.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** Annual and upon a new Jakarta EE platform release or material change to the application-server estate\
**Repository Path:** [`dev-security/standard-jakarta-ee-application-security.md`](standard-jakarta-ee-application-security.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the security controls for server-side Java applications that the organization builds on the Jakarta EE platform, or on its predecessor Java EE where still in service. It covers the platform's own security features (authentication mechanisms, identity stores, declarative and programmatic authorization, the authentication and authorization service-provider interfaces) and the servlet-layer concerns that sit around them: sessions, cookies, transport, container configuration, injection, error handling, logging, and patching.

---

## 2. Scope

This standard applies to:

1. Web applications and services deployed to a Jakarta EE application server or servlet container, whether full platform, Web Profile, or Core Profile.
2. Applications still on the Java EE `javax.*` namespace, until they are migrated.
3. Custom authentication mechanisms, identity stores, authentication modules, and authorization policy providers that the organization writes or configures for those applications.
4. The application-server and servlet-container configuration those applications run on.

It does not duplicate the general developer security baseline or the API security standard; it adds platform-specific requirements to them. Container-image hardening is covered by the container and image security standard.

---

## 3. Platform alignment

The standard aligns to the Jakarta EE 11 component specifications listed below. An application on an earlier platform release meets the equivalent control through that release's mechanism, or through a documented compensating control.

| Specification | Version | Security relevance |
| --- | --- | --- |
| Jakarta EE Platform | 11 | Login mechanisms, TLS support, unauthenticated callers, removal of the Java Security Manager requirement |
| Jakarta Security | 4.0 | HTTP authentication mechanisms, identity stores, security context, OpenID Connect client |
| Jakarta Servlet | 6.1 | Security constraints, roles, sessions, cookies, error pages, URI canonicalization |
| Jakarta Authentication | 3.1 | Server authentication module service-provider interface and Servlet Container Profile |
| Jakarta Authorization | 3.0 | Policy provider and role-mapping service-provider interface |

A Jakarta EE 11 runtime requires Java SE 17 or later. Applications run on a Java SE release that the runtime vendor supports.

---

## 4. Authentication mechanisms

| Control area | Requirement |
| --- | --- |
| Explicit mechanism | Every application that authenticates callers declares its authentication mechanism explicitly: a built-in Jakarta Security mechanism selected by annotation, or a reviewed custom `HttpAuthenticationMechanism`. It does not rely on the container to choose one. |
| Single configuration path | An application that provides an `HttpAuthenticationMechanism` does not also declare a `login-config` element in `web.xml`. |
| Multiple mechanisms | Where more than one mechanism is defined, the application supplies a custom `HttpAuthenticationMechanismHandler`, and its selection logic is security-reviewed. |
| HTTP Basic | Permitted only over a protected transport, and only for non-interactive or legacy clients that cannot use a stronger mechanism. Not used for interactive browser login. |
| HTTP Digest | Not used. It requires clear-text password equivalents to be available to the container. |
| Form-based login | The login page, and every security constraint that requires authentication, carry a `CONFIDENTIAL` transport guarantee. Form login is used only with cookie-based sessions. Password fields do not block browser password managers, following OWASP ASVS 5.0.0 V6.2.7 rather than the Servlet specification's recommendation to set `autocomplete="off"` on the password field. |
| Custom mechanisms | A custom `HttpAuthenticationMechanism` treats every request as potentially hostile, including requests to unconstrained resources. It establishes a caller identity only from a credential validated through an identity store, and fails closed on any validation error. |
| Programmatic login | Application-initiated login through `SecurityContext.authenticate()` sets `newAuthentication` to true for a fresh login, so that stale authentication state is discarded. |
| Remember-me | Used only where a documented business need exists. The remember-me cookie keeps the `Secure` and `HttpOnly` attributes, its lifetime is set to the shortest period the use case allows, the backing token store supports server-side revocation, and the token is removed on logout. |
| Authentication strength | Password, multi-factor, and re-authentication requirements per the authentication standard. Phishing-resistant methods are delegated to the enterprise identity provider through OpenID Connect where the provider supports them. |

---

## 5. Identity stores

| Control area | Requirement |
| --- | --- |
| Production identity stores | Production applications use an LDAP, database, OpenID Connect, or reviewed custom identity store. The in-memory identity store is prohibited outside test and demonstration environments, and the container option that blocks its use in production is enabled where the server provides one. |
| Password storage | A database identity store verifies passwords with the built-in `Pbkdf2PasswordHash`, or a stronger approved password-hashing function, with parameters set to current guidance per the authentication standard. Plaintext and reversible storage are prohibited. |
| Store credentials | Directory bind passwords, database credentials, and client secrets are never literal values in annotations, deployment descriptors, or source. They are supplied through expressions or server configuration that resolve from the secrets management service. |
| Directory transport | LDAP identity stores connect over LDAPS or StartTLS, with server certificate validation. |
| Query construction | Caller and group queries use parameter placeholders. Custom identity stores never concatenate caller-supplied values into SQL, JPQL, or LDAP filters. |
| Least-privilege store accounts | The account an identity store uses to reach its directory or database has read-only access, limited to the caller and group data it needs. |
| Multiple stores | Where several identity stores are configured, their priority order is documented and deliberate, and a store that only supplies groups is declared for group provision only. |
| Stateless stores | Custom identity stores do not track whether a caller is authenticated or how far an authentication dialog has progressed. |

---

## 6. OpenID Connect client

Applies where the application uses the Jakarta Security OpenID Connect mechanism, or an equivalent server-provided mechanism.

| Control area | Requirement |
| --- | --- |
| Flow | Authorization Code flow only (the mechanism's default response type). Implicit and hybrid response types are not configured. |
| State and nonce | The nonce stays enabled (the default). State and nonce are stored in the HTTP session (the default). Where cookie storage is chosen instead, the cookie carries the `HttpOnly` and `Secure` attributes. |
| Redirect URI | The redirect URI is an HTTPS URI that exactly matches a value pre-registered at the provider. No wildcard or open-redirect patterns are used. |
| Client secret | The client secret is resolved from the secrets management service through an expression, never hardcoded. Private-key client authentication is preferred where the provider and the runtime support it. |
| Token validation | The runtime's issuer, subject, audience, authorized-party, expiry, issued-at, not-before, and nonce checks are not disabled or bypassed. Clock-skew allowance is bounded and documented. |
| Token expiry | Expired access or identity tokens trigger either a refresh or a logout. The specification ignores an expired token unless `tokenAutoRefresh` (default false) is enabled, or the logout-on-expiry setting for that specific token (access or identity) is enabled. The application therefore enables automatic refresh, or both token-specific logout-on-expiry settings, so that neither token's expiry is ignored. Leaving either token's expiry ignored is prohibited. |
| Logout | Logout invalidates the local session. Provider notification of logout is enabled where the provider offers an end-session endpoint. |
| Group and role claims | Caller name and group claims are read only from validated tokens issued by the organization's identity provider. The mapping from provider groups to application roles is documented. |

---

## 7. Authorization and role mapping

| Control area | Requirement |
| --- | --- |
| Default deny | Every application resource is covered by a security constraint. Resources intended for anonymous access are listed explicitly; everything else requires authentication and a named role. |
| HTTP method coverage | Security constraints either name no HTTP methods, or the application sets `deny-uncovered-http-methods`. Container warnings about uncovered methods at deployment are treated as defects. Where the server offers a default of denying uncovered methods, that default is enabled. |
| Explicit denial | Resources that must never be reachable directly are protected by an authorization constraint that names no roles. |
| Special role names | The any-authenticated-user role name (`**`) is used only where every authenticated caller is genuinely entitled. The all-roles name (`*`) is never passed to `isUserInRole`. |
| Role references | Every role name used in programmatic checks is declared, and mapped to an application security role. |
| Group-to-role mapping | The mapping from identity-provider groups to application roles is explicit and documented. The container's default mapping of a group to a role of the same name, and any mapping of principal names to roles, is reviewed so that a directory group cannot grant an application role unintentionally. |
| Forwarded and included resources | Resources reached only through a `RequestDispatcher` forward or include enforce their own authorization in code, because declarative constraints do not apply to them. |
| Object-level authorization | Declarative constraints provide function-level control only. Every operation on a specific record checks, in code, that the caller is entitled to that record (for example with `SecurityContext` plus ownership or tenancy checks). |
| Business-tier enforcement | Sensitive operations are authorized in the business tier as well as the web tier. Enterprise bean methods carry method permissions (`@RolesAllowed`, `@DenyAll`), which the enterprise bean container enforces. Other CDI beans and service classes do not rely on those annotations unless the runtime's enforcement of them is verified by test; otherwise they check authorization in code through `SecurityContext`. |
| Run-as identities | Run-as identities are documented, least-privileged, and used only where a component must call a protected component on behalf of an unauthenticated or system caller. |
| Authorization policy providers | Replacement Jakarta Authorization `Policy`, `PolicyFactory`, and `PolicyConfigurationFactory` implementations are installed through reviewed server configuration. An application does not replace them itself, whether by setting the `jakarta.security.jacc.PolicyFactory.provider` or `jakarta.security.jacc.PolicyConfigurationFactory.provider` context parameter or by calling `setPolicyFactory`, `setPolicy`, or `setPolicyConfigurationFactory`, unless the security architecture forum approves a documented need. |
| Effective configuration | Where `metadata-complete` is true, or constraints are merged from annotations, fragments, and descriptors, the effective security configuration is verified in the deployed application, not assumed from source annotations. |

---

## 8. Jakarta Authentication modules

| Control area | Requirement |
| --- | --- |
| Mechanism preference | New work uses a Jakarta Security `HttpAuthenticationMechanism` rather than a raw `ServerAuthModule`, unless the security architecture forum approves a documented need. |
| Controlled registration | A `ServerAuthModule` or `AuthConfigProvider` is registered through exactly one controlled path (server configuration, or a single startup registration in the application). No other code registers or removes providers. Rights to modify the authentication configuration factory are limited to that path. |
| Success semantics | For protected resources, a module returns success only when it has fully satisfied the authentication policy and established the caller principal. |
| Failure semantics | A failed validation returns a failure status with an appropriate HTTP status and a generic response body. It never proceeds to the resource. |
| Unprotected resources | When a module is called for an unprotected resource under an optional request policy, it does not start an authentication dialog. It either establishes an identity from a complete, valid credential, or leaves the caller unauthenticated. An authentication the application requests explicitly (for example `HttpServletRequest.authenticate()` from an unconstrained login endpoint) arrives with a mandatory policy and may start the dialog. |
| Session registration | Container authentication-session registration is requested deliberately. Modules do not relay the authentication-type or session-registration properties they receive as input. |
| Clean-up | The module's clean-up on logout removes any authentication state it holds, including cookies it set. |

---

## 9. Transport security

| Control area | Requirement |
| --- | --- |
| Protocol and cipher suites | Server listeners are configured per the encryption policy. The legacy protocols and cipher suites that the platform requires products to support for interoperability are disabled unless an approved exception applies. |
| Confidential transport | Every application URL carries a `CONFIDENTIAL` transport guarantee, so the container rejects or redirects non-TLS requests. Browser-facing applications send HTTP Strict Transport Security. |
| TLS offload | Where TLS terminates at a load balancer or proxy, the container trusts forwarded protocol and client-address headers only from known proxies. This keeps the request's secure flag, redirects, and cookie `Secure` attributes correct. |
| Outbound connections | Connections to directories, databases, identity providers, and downstream services use TLS with certificate validation. Trust-all trust managers and hostname-verification bypasses are prohibited. |
| Mutual TLS | Where client-certificate authentication is used, the certificate chain and revocation status are validated before the certificate identity is used for authentication or authorization. |

---

## 10. Sessions and cookies

| Control area | Requirement |
| --- | --- |
| Tracking mode | Sessions are tracked by cookie only. URL rewriting (`jsessionid` path parameters) is disabled. |
| Session cookie attributes | The session cookie is `HttpOnly` and `Secure`, carries an explicit `SameSite` value suited to the application (`Strict` or `Lax`), and uses the `__Host-` name prefix where the deployment allows. Cookie attributes are set through the container's session cookie configuration. |
| Session identifier renewal | A new session identifier is issued immediately after successful authentication, re-authentication, or privilege change, using `changeSessionId()` or equivalent container behaviour. The container's behaviour is verified by test, because the platform preserves the pre-login session object across login. |
| Timeouts | Idle timeout and absolute session lifetime follow the authentication standard. A session timeout of zero or less, which disables expiry, is prohibited. |
| Logout | Logout calls `HttpServletRequest.logout()`, invalidates the session, clears remember-me and mechanism cookies, and makes the terminated session unusable server-side. |
| Application cookies | Cookies the application sets carry `Secure`, carry `HttpOnly` unless client script has a documented need, and carry an explicit `SameSite` value. |
| Cross-site request forgery | State-changing operations use non-safe HTTP methods and are protected by a synchronizer or framework anti-forgery token. `SameSite` counts as defence in depth, not as the sole control. |
| Session contents | Sessions do not hold credentials or other secrets beyond what the application needs. Sensitive data is removed from the session once used. |

---

## 11. Container defaults to harden

| Control area | Requirement |
| --- | --- |
| Management interfaces | Administration consoles and management endpoints are not reachable from untrusted networks, require strong authentication, and have default or sample accounts removed. |
| Sample and default content | Sample applications, default welcome applications, and example resources are removed from production servers. |
| Directory listings | Directory listing is disabled on the container's default servlet. |
| Server identification | Server banners, `X-Powered-By`, and version-bearing headers are suppressed. |
| HTTP TRACE | TRACE is disabled at the container, or denied by a security constraint on every application. |
| URI canonicalization | The container's rejection of suspicious URI sequences (encoded `/`, dot-segments carrying path parameters or encoded characters) stays at the specification default. Container options that relax canonicalization need a documented security review. |
| Protected directories | Configuration resources that must not be served are kept under `WEB-INF`, and never under `META-INF/resources` inside a JAR in `WEB-INF/lib`, which the container serves directly. Secrets are never packaged in the application archive (see section 5). Application code never passes caller-controlled paths to `getResource`, `getResourceAsStream`, or `RequestDispatcher`, which can reach `WEB-INF` content. |
| Upload limits | Every servlet that accepts multipart content sets explicit maximum file and request sizes, suited to its use case. |
| Process isolation | Applications do not rely on the Java Security Manager or `permissions.xml` for isolation, because Jakarta EE 11 removed that requirement. Isolation comes from the operating system, container, and network controls in the container and image security standard. |
| Development modes | Framework development and debug modes (for example a Faces project stage of `Development`) and hot-deploy features are disabled in production. |

---

## 12. Injection in persistence, expression language, and dependency-injection contexts

| Control area | Requirement |
| --- | --- |
| Persistence queries | JPQL, Criteria, and native queries bind caller-influenced values as parameters. Caller input is never concatenated into query strings. |
| Dynamic query structure | Caller-selected sort columns, filter fields, and entity names are mapped through an allow-list to fixed identifiers, never inserted directly into a query. |
| Expression language | Caller-supplied input is never evaluated as an expression-language expression, whether through `ELProcessor`, `ExpressionFactory`, or dynamically built Faces or Pages expressions. Expressions in security annotations resolve only from trusted configuration. |
| Dependency injection and reflection | Caller input never selects a CDI bean, class, or method by name (for example through `Instance.select` with caller-derived qualifiers, `Class.forName`, or reflective invocation) except through a fixed allow-list. |
| Deserialization | Java native deserialization of untrusted data is prohibited. Where legacy code cannot be removed, a deserialization filter restricts accepted classes. JSON and XML binding does not enable polymorphic type resolution from caller data. |
| XML processing | XML parsers and binding contexts disable external entity and DTD resolution. |
| Directory queries | Custom LDAP queries escape caller input for the filter context, or use parameterized filter construction. |
| Input validation | Bean Validation constraints are enforced at the service boundary. Client-side validation is not relied on. |
| Mass assignment | Request payloads bind to dedicated transfer objects with explicitly allowed fields, never directly to persistence entities. |
| Output encoding | Framework auto-escaping in Faces, Pages, and template output is not disabled for caller-influenced content. Any exception is reviewed. |

---

## 13. Error handling and information disclosure

| Control area | Requirement |
| --- | --- |
| Error pages | Each application declares error pages for 4xx and 5xx status codes and a default error page for unhandled exceptions, so no container default error output reaches clients. |
| Error content | Error responses carry a generic message and a correlation identifier. Stack traces, exception messages, exception class names, request URIs, and query strings from the container's error attributes are not rendered to clients. |
| Authentication failures | Authentication failures return uniform responses that do not reveal whether the caller name exists. |
| Asynchronous processing | Code running in application-created threads or asynchronous contexts catches and handles its own errors, and fails closed. |
| Fail closed | Exceptions in authentication, authorization, or validation paths deny the operation. They never continue with partial state. |

---

## 14. Logging

| Control area | Requirement |
| --- | --- |
| Security events | Authentication success and failure, logout, session creation and invalidation, authorization denials, and changes to roles or identity-store configuration are logged, with caller, time, source address, and outcome. |
| Deployment warnings | Container deployment warnings about uncovered HTTP methods, insecure defaults, or in-memory identity stores are captured and raised as findings. |
| Sensitive data | Passwords, session identifiers, tokens, remember-me values, and client secrets are never written to application, access, or error logs. Other personal data in logs is limited to the caller and source identifiers the security events above need, and is protected per the logging standard. Access logs exclude query strings that may carry sensitive values. |
| Log injection | Caller-supplied values are encoded before being written to logs. |
| Forwarding | Logs are forwarded per the logging standard. |

---

## 15. Dependency and container patching

| Control area | Requirement |
| --- | --- |
| Supported runtime | Application servers and servlet containers are on a release the vendor currently supports, certified for the Jakarta EE profile the application targets. Security patches are applied per the patch management procedure. |
| Java SE currency | The Java SE runtime is a vendor-supported release at or above the platform minimum, and is patched per the patch management procedure. |
| Component inventory | A software bill of materials is maintained for each application, covering bundled libraries and the server-provided Jakarta EE implementation versions. |
| Composition analysis | Dependencies are scanned per the software composition analysis standard. Findings are remediated within the vulnerability management procedure's time frames. |
| Provided APIs | Jakarta EE API artefacts supplied by the server are declared as provided, not bundled. The application does not ship duplicate or conflicting security implementations. |
| Namespace migration | Applications on the Java EE `javax.*` namespace have a dated migration plan. Namespace-transformation tooling used during migration is inventoried and patched like any other dependency. |
| Container images | Server and container images follow the container and image security standard. |

---

## 16. Verification

| Control area | Requirement |
| --- | --- |
| Configuration review | The effective deployed security configuration (constraints, role mapping, authentication mechanism, cookie and session settings, TLS listeners) is reviewed before first production release, and after any change to it. |
| Static analysis | Static analysis in CI includes rules for injection into persistence queries and expression language, unsafe deserialization, and insecure cookie and session configuration. |
| Dynamic testing | Pre-release testing covers authentication bypass through uncovered HTTP methods, session fixation, forced browsing to forwarded-only resources, and error-page information disclosure. |
| Code review | Custom authentication mechanisms, identity stores, authentication modules, and policy providers are reviewed per the secure code review procedure before first use and on every change. |
| Penetration testing | Per the penetration testing and red team standard. |

---

## 17. Operating expectations

1. Each Jakarta EE application has an owning role accountable for its posture against this standard.
2. The effective security configuration of each production application is re-verified annually, and after any application-server upgrade.
3. Application-server and Java SE versions are checked against vendor support windows at each release.
4. Container deployment logs are reviewed for uncovered-method and insecure-default warnings at each deployment.
5. This standard is reviewed when a new Jakarta EE platform release is published.

---

## 18. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| Jakarta EE Platform 11 | Login mechanisms; TLS and cipher-suite support; unauthenticated users; removal of Security Manager requirements | Platform baseline |
| Jakarta Security 4.0 | Authentication mechanisms; identity stores; OpenID Connect mechanism; remember-me; security context | Application authentication |
| Jakarta Servlet 6.1 | Security constraints and uncovered methods; roles; sessions and cookies; error pages; URI canonicalization | Web-tier security |
| Jakarta Authentication 3.1 | Servlet Container Profile | Authentication module contract |
| Jakarta Authorization 3.0 | Policy provider configuration; principal-to-role mapping | Authorization provider contract |
| OWASP ASVS 5.0.0 | V1 (encoding and sanitization), V2 (validation), V3 (web frontend: cookies, headers, origin separation), V4 (API and web service), V5 (file handling), V6 (authentication), V7 (session management), V8 (authorization), V10 (OAuth and OIDC), V11 (cryptography), V12 (secure communication), V13 (configuration), V14 (data protection), V15 (secure coding and architecture), V16 (logging and error handling) | Application security verification baseline |
| OWASP Top 10:2025 | A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions | Web risk taxonomy |
| MITRE CWE 4.20 | CWE-89, CWE-90, CWE-117, CWE-209, CWE-306, CWE-319, CWE-352, CWE-384, CWE-470, CWE-502, CWE-532, CWE-564, CWE-611, CWE-613, CWE-614, CWE-650, CWE-798, CWE-862, CWE-863, CWE-915, CWE-916, CWE-917, CWE-1004, CWE-1104, CWE-1188, CWE-1275, CWE-1392, CWE-1395 | Weakness coverage |
| NIST SP 800-218 (SSDF 1.1) | PO.1, PW.4, PW.5, PW.7, PW.8, PW.9, RV.1, RV.2 | Secure development practices |

---

## 19. Limitations

This standard is a CC BY-SA 4.0 baseline. Application servers differ in how they expose platform features (cookie attributes, uncovered-method defaults, canonicalization options, identity-store blocking), so the standard states requirements rather than vendor-specific settings. Adopting organizations map each requirement to their server's configuration, and confirm the current platform and vendor guidance at each release. The injection, output-encoding, and anti-forgery requirements rest on OWASP ASVS 5.0.0 and CWE rather than on the Jakarta Persistence, Expression Language, Faces, and CDI specifications, which the reference base does not hold; javadoc-level details (password-hash parameters, cookie-attribute APIs, multipart limits) are likewise stated as outcomes rather than API settings.

---

**End of Document**
