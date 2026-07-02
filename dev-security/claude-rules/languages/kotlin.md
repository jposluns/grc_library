# Kotlin / Android (and Java for Android) Security Rules

These rules apply to Android applications written in Kotlin or Java. They supplement the core rules in `core/` and implement the controls in [`standard-mobile-application-security.md`](../../../dev-security/standard-mobile-application-security.md). Section numbers below refer to that standard.

Java-Android idioms are noted inline where they differ from Kotlin; the underlying Android platform APIs are the same. For server-side Java (Spring Boot, Jakarta EE), see [`languages/java.md`](java.md) instead.

---

## Secure storage (Section 4)

```kotlin
// NEVER: sensitive data in plain SharedPreferences
val prefs = context.getSharedPreferences("auth", Context.MODE_PRIVATE)
prefs.edit().putString("token", apiToken).apply()  // Plaintext in /data/data/<pkg>/shared_prefs/

// NEVER: sensitive data in MODE_WORLD_READABLE / MODE_WORLD_WRITEABLE
context.openFileOutput("token.dat", Context.MODE_WORLD_READABLE)  // Deprecated and dangerous

// NEVER: sensitive data on external storage
context.getExternalFilesDir(null)  // Acceptable for non-sensitive only

// CORRECT: EncryptedSharedPreferences backed by the Android Keystore
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .setUserAuthenticationRequired(true, 300)  // Require recent auth for high-sensitivity
    .build()

val securePrefs = EncryptedSharedPreferences.create(
    context,
    "auth_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
securePrefs.edit().putString("token", apiToken).apply()

// CORRECT: EncryptedFile for larger payloads
val encryptedFile = EncryptedFile.Builder(
    context,
    File(context.filesDir, "sensitive.dat"),
    masterKey,
    EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB
).build()
```

`android:allowBackup="false"` in the manifest, OR explicit backup rules excluding sensitive files via `android:fullBackupContent` / `android:dataExtractionRules` (the latter on Android 12+).

Same rules in Java: `getSharedPreferences()` and `openFileOutput()` are the same APIs; `EncryptedSharedPreferences.create(...)` and `EncryptedFile.Builder(...)` work identically.

---

## Cryptography (Section 5)

```kotlin
// NEVER: hardcoded keys, ECB mode, custom crypto
val key = "MyHardcodedKey16".toByteArray()  // Hardcoded
val cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")  // ECB leaks structure

// CORRECT: Android Keystore for hardware-backed key generation
val keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
val spec = KeyGenParameterSpec.Builder(
    "auth_key",
    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
)
    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
    .setKeySize(256)
    .setIsStrongBoxBacked(true)  // Tier 1: require StrongBox where available
    .setUserAuthenticationRequired(true)
    .build()
keyGenerator.init(spec)
val key = keyGenerator.generateKey()

// CORRECT: AES-GCM with a fresh IV per encryption
val cipher = Cipher.getInstance("AES/GCM/NoPadding")
cipher.init(Cipher.ENCRYPT_MODE, key)
val iv = cipher.iv
val ciphertext = cipher.doFinal(plaintext)
```

Use `SecureRandom` for security-sensitive randomness. `java.util.Random` and `kotlin.random.Random.Default` are not cryptographically secure.

```kotlin
// NEVER
val token = (1..32).map { ('a'..'z').random() }.joinToString("")

// CORRECT
val bytes = ByteArray(32)
SecureRandom().nextBytes(bytes)
```

`Tink` (Google's high-level crypto library) is acceptable as an alternative to raw `javax.crypto`.

---

## Authentication and local biometrics (Section 6)

```kotlin
// NEVER: biometric used as the sole credential
BiometricPrompt(activity, executor, object : BiometricPrompt.AuthenticationCallback() {
    override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
        grantFullAccess()  // Wrong: biometric is not authentication
    }
}).authenticate(promptInfo)

// CORRECT: biometric is step-up to unlock a credential held in the Keystore
val biometricPrompt = BiometricPrompt(activity, executor, object : BiometricPrompt.AuthenticationCallback() {
    override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
        // The Cipher inside result.cryptoObject is now usable to decrypt the
        // Keystore-protected credential; the OS gated access to it on biometric success.
        val cipher = result.cryptoObject?.cipher
        cipher?.let { decryptCredentialAndProceed(it) }
    }
})
biometricPrompt.authenticate(
    promptInfo,
    BiometricPrompt.CryptoObject(cipher)  // Binds the unlock to a specific Keystore key
)
```

Set `setInvalidatedByBiometricEnrollment(true)` on key specs so that a new fingerprint enrolment invalidates the binding.

OAuth / OIDC: use `Custom Tabs` (`androidx.browser`) for the auth flow; never embed the IdP login page in a `WebView`.

---

## Network and Network Security Configuration (Section 7)

```xml
<!-- NEVER: cleartext traffic globally enabled -->
<application android:usesCleartextTraffic="true" ...>

<!-- NEVER: Network Security Config that trusts user-installed CAs -->
<network-security-config>
    <base-config>
        <trust-anchors>
            <certificates src="user"/>
        </trust-anchors>
    </base-config>
</network-security-config>

<!-- CORRECT: cleartext denied; user CAs not trusted in production -->
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system"/>
        </trust-anchors>
    </base-config>
    <!-- Domain-scoped exceptions documented per Section 7 -->
</network-security-config>
```

Certificate pinning (Tier 1, Tier 2 per Section 3) via Network Security Config (`<pin-set>`) or OkHttp `CertificatePinner`:

```kotlin
val pinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/PRIMARY_PIN", "sha256/BACKUP_PIN")
    .build()
val client = OkHttpClient.Builder().certificatePinner(pinner).build()
```

Backup pins documented; pin-rotation plan exists.

---

## Backend attestation: Play Integrity (Section 7)

Tier 1 and Tier 2 application backends require Play Integrity. The client requests a token, sends to the backend, the backend verifies against Google's attestation service.

```kotlin
import com.google.android.play.core.integrity.IntegrityManagerFactory
import com.google.android.play.core.integrity.IntegrityTokenRequest

val integrityManager = IntegrityManagerFactory.create(context)
val request = IntegrityTokenRequest.builder()
    .setNonce(backendIssuedNonce)  // Backend-issued, per-request
    .build()

integrityManager.requestIntegrityToken(request)
    .addOnSuccessListener { response ->
        // Send response.token() to backend; backend calls
        // Google's Play Integrity verifier for server-side verification.
        backend.verifyIntegrityToken(response.token())
    }
    .addOnFailureListener { /* report degraded-trust state */ }
```

Never trust Play Integrity verdicts purely client-side. The backend is the verifier. Use Standard requests (cached) for low-frequency checks; Classic / Recurring requests for high-frequency operations.

---

## Platform interaction (Section 8)

```xml
<!-- NEVER: exported component without permission protection or signature check -->
<activity android:name=".TransferActivity" android:exported="true"/>

<!-- NEVER: implicit intent with sensitive data -->
<!-- An app holding android.intent.action.SEND can intercept this -->
```

```kotlin
// NEVER: send sensitive data via implicit intent
val intent = Intent(Intent.ACTION_SEND).apply {
    type = "text/plain"
    putExtra(Intent.EXTRA_TEXT, "Auth token: $token")
}
startActivity(Intent.createChooser(intent, "Share"))

// CORRECT: explicit intent (component name) for inter-app data; receiver
// has matching signature-level permission for cross-app integration
val intent = Intent().apply {
    component = ComponentName("com.example.trusted", "com.example.trusted.Receiver")
    putExtra("payload", payload)
}
startActivity(intent)
```

Deep links: prefer App Links (`android:autoVerify="true"` + Digital Asset Links) over custom URL schemes; they require domain ownership verification at OS level. Validate intent-filter inputs.

Logging:

```kotlin
// NEVER: log credentials / PII
Log.d("Auth", "Token: $token")
Log.i("User", "Logged in: $email")

// CORRECT: redact; use a logging facade that strips sensitive fields
private val logger = AppLogger.forCategory("auth")
logger.info("Auth event for user", userIdHash)  // hash, not raw id
```

`Log.isLoggable(...)` plus build-type gating keeps debug logging out of release.

---

## WebView (Section 7, 8)

```kotlin
// NEVER: enable JavaScript with a JS interface that exposes broad native APIs
webView.settings.javaScriptEnabled = true
webView.addJavascriptInterface(NativeBridge(), "Native")
// where NativeBridge accepts arbitrary commands

// NEVER: load arbitrary URLs without scheme / domain validation
webView.loadUrl(userSuppliedUrl)

// CORRECT: WebView restricted to known origins; JS bridge accepts a narrow API
webView.settings.apply {
    javaScriptEnabled = true
    allowFileAccess = false
    allowContentAccess = false
    allowFileAccessFromFileURLs = false
    allowUniversalAccessFromFileURLs = false
}
webView.webViewClient = object : WebViewClient() {
    override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean {
        return !isAllowedHost(request.url.host)  // true cancels navigation
    }
}
webView.addJavascriptInterface(NarrowBridge(allowed = setOf("showSheet")), "Native")
```

`WebView.setSafeBrowsingEnabled(true)` (default on modern Android) and CSP delivered by the served content. WebView from untrusted origins is a sandbox boundary; treat traversals across it as untrusted.

---

## App permissions and privacy (Section 12)

```kotlin
// NEVER: request a broad permission for a narrow need
// Wrong: ACCESS_FINE_LOCATION when you only need approximate location
ActivityCompat.requestPermissions(activity, arrayOf(ACCESS_FINE_LOCATION), REQ)

// CORRECT: request the narrowest permission; ACCESS_COARSE_LOCATION suffices
ActivityCompat.requestPermissions(activity, arrayOf(ACCESS_COARSE_LOCATION), REQ)

// CORRECT: foreground-service location vs background-location requested
// only where the feature genuinely requires it; rationale shown to the user
shouldShowRequestPermissionRationale(activity, ACCESS_BACKGROUND_LOCATION)
```

Honour the "Don't ask again" / `shouldShowRequestPermissionRationale` flow. Photo Picker (`ActivityResultContracts.PickVisualMedia`) does not require storage permissions and is preferred over `READ_MEDIA_IMAGES` where the use case fits.

---

## Distribution and signing (Section 11)

- App signing keys held in a CI/CD secrets manager or Google Play App Signing; never committed to source control.
- Release builds use `minifyEnabled true` and ProGuard / R8 with appropriate keep rules. The resulting `mapping.txt` is preserved per release for crash de-symbolication.
- Debug builds excluded from production data: signing variant, `applicationIdSuffix`, BuildConfig flags.
- Side-loaded distribution (APK / AAB outside store) prohibited for production.

---

## In-app billing / receipt validation (Section 16)

```kotlin
// NEVER: grant entitlement from BillingClient result alone
billingClient.queryPurchasesAsync(...) { result, purchases ->
    purchases.forEach {
        if (it.purchaseState == Purchase.PurchaseState.PURCHASED) {
            grantEntitlement()  // Client-only validation
        }
    }
}

// CORRECT: send purchaseToken to backend for verification against
// Google Play Developer API; backend grants entitlement after successful verify
purchases.forEach { purchase ->
    if (purchase.purchaseState == Purchase.PurchaseState.PURCHASED) {
        backend.verifyAndGrant(
            productId = purchase.products.first(),
            purchaseToken = purchase.purchaseToken
        )
    }
}
```

Acknowledge purchases only after backend verification. Real-time Developer Notifications (RTDN) feed the backend for subscription state changes per Section 16.

---

## Reverse-engineering resistance (Section 9, Tier 1 and Tier 2)

- Root detection used as a signal, not as the sole defence. RootBeer / SafetyNet-Attest-style checks reported to backend; user experience degrades gracefully.
- String obfuscation for embedded secrets (with the caveat that no embedded secret is truly secret on a rooted device).
- ProGuard / R8 obfuscation enabled in release builds; not the sole defence.
- Frida and Xposed hook detection for Tier 1; native code anti-tamper where the threat model warrants it.

---

## Framework alignment

Implements these sections of [`standard-mobile-application-security.md`](../../../dev-security/standard-mobile-application-security.md):

- Section 4 (storage): EncryptedSharedPreferences, EncryptedFile, manifest backup posture.
- Section 5 (cryptography): Android Keystore (StrongBox-backed for Tier 1), AES-GCM, SecureRandom.
- Section 6 (authentication and authorisation): BiometricPrompt with CryptoObject; setInvalidatedByBiometricEnrollment; Custom Tabs for OAuth.
- Section 7 (network): Network Security Config; OkHttp CertificatePinner; Play Integrity server verification.
- Section 8 (platform interaction): App Links over custom schemes; explicit intents for cross-app data; logging redaction.
- Section 9 (MASVS-R): root detection as signal; R8; native anti-tamper for Tier 1.
- Section 11 (distribution): App Signing; ProGuard / R8 in release; mapping.txt preservation.
- Section 12 (privacy): narrow permission scopes; Photo Picker preference.
- Section 16 (IAP): server-side `purchaseToken` verification via Play Developer API; acknowledgement gating.

Supplements: OWASP MASVS v2 (L1, L2, R); MASTG Android test cases; Android Developers Security guide.
