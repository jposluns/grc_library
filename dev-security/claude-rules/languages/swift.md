# Swift / iOS (and Objective-C) Security Rules

These rules apply to iOS applications written in Swift or Objective-C. They supplement the core rules in `core/` and implement the controls in [`standard-mobile-application-security.md`](../../../dev-security/standard-mobile-application-security.md). Section numbers below refer to that standard.

Objective-C-specific patterns are noted inline where they differ from Swift; the underlying iOS platform APIs are the same.

---

## Secure storage (Section 4)

```swift
// NEVER: sensitive data in UserDefaults / NSUserDefaults
UserDefaults.standard.set(apiToken, forKey: "auth_token")  // Plaintext in plist
NSUserDefaults.standardUserDefaults().setObject(token, forKey: "auth") // Obj-C equivalent

// NEVER: sensitive data in a file without protection class
try data.write(to: docsURL.appendingPathComponent("token.dat"))

// CORRECT: Keychain with appropriate accessibility class
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "auth_token",
    kSecValueData as String: tokenData,
    kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
]
SecItemAdd(query as CFDictionary, nil)

// CORRECT: file with explicit Data Protection class
try data.write(
    to: url,
    options: [.atomic, .completeFileProtectionUntilFirstUserAuthentication]
)
```

`kSecAttrAccessibleAlways` is prohibited. `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` is the default for credentials.

Backup exclusion: set the `isExcludedFromBackup` resource value on URLs that hold sensitive content.

```swift
var url = sensitiveFileURL
var values = URLResourceValues()
values.isExcludedFromBackup = true
try url.setResourceValues(values)
```

---

## Cryptography (Section 5)

```swift
// NEVER: custom crypto, ECB mode, hardcoded keys, CommonCrypto with insecure params
let cipher = MyCustomAESImplementation(key: hardcodedKey)  // Custom crypto prohibited

// CORRECT: CryptoKit with platform-managed key material
import CryptoKit
let key = SymmetricKey(size: .bits256)
let sealed = try AES.GCM.seal(plaintext, using: key)

// CORRECT: Secure Enclave for asymmetric keys where the hardware supports it
let access = SecAccessControlCreateWithFlags(
    nil,
    kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
    [.privateKeyUsage, .biometryCurrentSet],
    nil
)!
let attributes: [String: Any] = [
    kSecAttrKeyType as String: kSecAttrKeyTypeECSECPrimeRandom,
    kSecAttrKeySizeInBits as String: 256,
    kSecAttrTokenID as String: kSecAttrTokenIDSecureEnclave,
    kSecPrivateKeyAttrs as String: [
        kSecAttrIsPermanent as String: true,
        kSecAttrApplicationTag as String: tag,
        kSecAttrAccessControl as String: access,
    ],
]
```

Use `SecRandomCopyBytes` for security-sensitive randomness. `arc4random` is acceptable for non-security uses; `Int.random(in:)` (Swift) uses a CSPRNG.

---

## Authentication and local biometrics (Section 6)

```swift
// NEVER: biometric used as the sole authentication factor
LAContext().evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, ...) { ok, _ in
    if ok { grantFullAccess() }  // Wrong: biometric alone is not authentication
}

// CORRECT: biometric is a step-up signal; the credential is the
// Keychain-stored token (or an attested federated session)
let context = LAContext()
context.localizedReason = "Confirm payment"
context.evaluatePolicy(.deviceOwnerAuthentication, localizedReason: "...") { ok, error in
    guard ok else { return }
    // Retrieve the Keychain-protected credential and proceed
}
```

Bind sensitive Keychain items to biometry-current-set via `SecAccessControlCreateWithFlags(.biometryCurrentSet, ...)` so a new fingerprint enrolment invalidates the binding.

Use ASWebAuthenticationSession for OAuth / OIDC flows: it presents the system browser and isolates cookies from the app.

---

## Network and App Transport Security (Section 7)

```xml
<!-- NEVER: blanket ATS bypass in Info.plist -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key><true/>
</dict>
```

Domain-scoped exceptions are documented per Section 7; blanket exceptions are prohibited.

```swift
// Certificate pinning via URLSessionDelegate (Tier 1, Tier 2 per Section 3)
func urlSession(_ session: URLSession,
                didReceive challenge: URLAuthenticationChallenge,
                completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
    guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
          let serverTrust = challenge.protectionSpace.serverTrust else {
        completionHandler(.cancelAuthenticationChallenge, nil)
        return
    }
    // Compare serverTrust's leaf or intermediate against pinned SPKI hashes;
    // backup pins documented for rotation per Section 5.
    if matchesPin(serverTrust) {
        completionHandler(.useCredential, URLCredential(trust: serverTrust))
    } else {
        completionHandler(.cancelAuthenticationChallenge, nil)
    }
}
```

---

## Backend attestation: App Attest and DeviceCheck (Section 7)

Tier 1 and Tier 2 application backends require App Attest. The client generates an attestation key, attests on first use, and signs subsequent assertions; the backend verifies tokens against Apple's attestation service.

```swift
import DeviceCheck

guard DCAppAttestService.shared.isSupported else {
    // Fall back per the backend's documented degraded-trust path
    return
}

DCAppAttestService.shared.generateKey { keyId, error in
    guard let keyId = keyId else { return }
    // Send keyId to backend; backend issues a nonce/challenge.
    DCAppAttestService.shared.attestKey(keyId, clientDataHash: challengeHash) { attestation, error in
        // Send attestation blob to backend for Apple verification.
    }
}
```

Never trust App Attest assertions purely client-side. The backend is the verifier.

---

## Platform interaction (Section 8)

```swift
// NEVER: open a custom URL scheme that triggers a sensitive action without authentication
func application(_ app: UIApplication, open url: URL, options: ...) -> Bool {
    if url.host == "transfer" {
        let amount = url.queryItem("amount")
        performTransfer(amount: amount)  // Unauthenticated; deep-link replay
        return true
    }
    return false
}

// CORRECT: deep links validated, authenticated, and replay-protected
func application(_ app: UIApplication, open url: URL, options: ...) -> Bool {
    guard let action = parseSignedDeepLink(url),
          action.isFresh, action.matchesCurrentSession else {
        return false
    }
    showConfirmation(for: action)  // Require explicit user confirmation
    return true
}
```

Universal Links (Associated Domains) are preferred over custom URL schemes because they require domain ownership verification at OS level.

Privacy and pasteboard:

```swift
// NEVER: log credentials / PII to the console (visible in Console.app and crash reports)
NSLog("Auth token: %@", token)
print("User \(email) logged in")

// CORRECT: redact in logging; use OSLog with appropriate privacy markers
import OSLog
let logger = Logger(subsystem: "com.example.app", category: "auth")
logger.info("Auth event for user \(userID, privacy: .private)")
```

For sensitive text fields:
```swift
// Mark TextField as not shareable to pasteboard / not screenshotted where possible
secureTextField.textContentType = .password
// In iOS 18+ for sensitive views: ContentView().sensoryFeedback / privacySensitive()
```

---

## WebView (WKWebView; Section 7 and Section 8)

```swift
// NEVER: load arbitrary user-supplied URL into a webview without scheme validation
webView.load(URLRequest(url: URL(string: userInput)!))

// NEVER: JavaScript bridge that exposes native APIs to arbitrary JS
webView.configuration.userContentController.add(self, name: "executeNativeCommand")
// where executeNativeCommand interprets a JSON message and calls into native code

// CORRECT: explicit allow-list of origins; bridge restricted to a small, validated API
let config = WKWebViewConfiguration()
config.preferences.javaScriptCanOpenWindowsAutomatically = false
config.defaultWebpagePreferences.allowsContentJavaScript = true
// Inject only specifically-validated message handlers
config.userContentController.add(SafeBridge(allowedCommands: ["showPaymentSheet"]), name: "bridge")
```

Universal Links inside WKWebView: handle via `navigationAction.navigationType == .linkActivated` to differentiate user taps from programmatic navigations.

---

## App Tracking Transparency and privacy permissions (Section 12)

```swift
// NEVER: deceptive ATT prompt copy ("Allow tracking to unlock this feature")
let dialog = ATTrackingManager.requestTrackingAuthorization { ... }

// CORRECT: prompt copy describes the actual data use; permission is optional
// to the core experience; the feature must function without tracking authorization
```

`NSUserTrackingUsageDescription` text is reviewed and matches actual data flow. Do not request tracking from a deceptive context (e.g. immediately after a different security prompt).

---

## Code signing and distribution (Section 11)

- Code-signing identities held in Apple Developer team accounts; team membership reviewed.
- Distribution profiles do not bundle development entitlements.
- TestFlight builds excluded from production telemetry / data per Section 11.
- App Store privacy labels accurately reflect SDK behaviour (per Section 12).

---

## In-app purchases (Section 16)

```swift
// NEVER: grant entitlement from client-side StoreKit result alone
let result = try await product.purchase()
if case .success(let verification) = result {
    grantEntitlement()  // Client-only validation
}

// CORRECT: send the JWS-signed transaction representation to the backend
// for validation against the StoreKit Server API; backend grants entitlement
if case .success(.verified(let transaction)) = result {
    let jwsRepresentation = transaction.jwsRepresentation
    await backend.validateAndGrant(jws: jwsRepresentation)
    await transaction.finish()
}
```

`transaction.jwsRepresentation` is what the backend verifies against Apple. Subscription state is polled or webhooked via App Store Server Notifications per Section 16.

---

## Reverse-engineering resistance (Section 9, Tier 1 and Tier 2)

- Jailbreak detection used as a signal, not as the sole defence. Detection signals reported to backend; user experience degraded gracefully (not abrupt crash).
- String obfuscation for embedded secrets (with the caveat that no embedded secret is truly secret on a jailbroken device).
- Anti-debug checks (`ptrace(PT_DENY_ATTACH, 0, 0, 0)` and similar) for Tier 1 only; do not rely on these as the security model.
- Compiler hardening (PIE, stack canaries, ARC) enabled in release builds. The Xcode defaults are correct; verify they remain enabled in release configurations.

---

## Framework alignment

Implements these sections of [`standard-mobile-application-security.md`](../../../dev-security/standard-mobile-application-security.md):

- Section 4 (storage): Keychain accessibility classes; data protection classes; backup exclusion.
- Section 5 (cryptography): CryptoKit; Secure Enclave; `SecRandomCopyBytes`.
- Section 6 (authentication and authorization): biometry as step-up; ASWebAuthenticationSession; biometry-current-set binding.
- Section 7 (network): ATS scoped exceptions; certificate pinning; App Attest server verification.
- Section 8 (platform interaction): Universal Links over custom schemes; deep-link validation; OSLog privacy markers.
- Section 9 (MASVS-R): Tier 1 / Tier 2 hardening defaults.
- Section 11 (distribution): code-signing posture.
- Section 12 (privacy): ATT prompt honesty.
- Section 16 (IAP): server-side `jwsRepresentation` verification.

Supplements: OWASP MASVS v2 (L1, L2, R); MASTG iOS test cases; Apple Platform Security guide.
