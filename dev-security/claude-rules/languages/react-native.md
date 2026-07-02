# React Native Security Rules

These rules apply to mobile applications built with React Native (with or without Expo). They supplement the core rules in `core/`, the JavaScript / TypeScript rules in [`languages/typescript.md`](typescript.md), and the underlying-platform rules in [`languages/swift.md`](swift.md) (iOS) and [`languages/kotlin.md`](kotlin.md) (Android). They implement the controls in [`standard-mobile-application-security.md`](../../../dev-security/standard-mobile-application-security.md), with particular emphasis on Section 15 (hybrid and cross-platform frameworks). Section numbers below refer to that standard.

Hybrid framework rule: React Native shifts the layer at which a control is implemented; it does not remove the control. If a Section 4 storage requirement exists for native iOS / Android, the equivalent requirement applies to the React Native app, just delegated to the right plugin or native module.

---

## Secure storage delegation (Section 4, Section 15)

```ts
// NEVER: sensitive data in AsyncStorage
import AsyncStorage from '@react-native-async-storage/async-storage';
await AsyncStorage.setItem('auth_token', token);  // Plaintext in app sandbox

// NEVER: sensitive data in MMKV without encryption
import { MMKV } from 'react-native-mmkv';
const storage = new MMKV();  // Default constructor; not encrypted
storage.set('token', token);

// CORRECT: react-native-keychain delegates to iOS Keychain + Android Keystore
import * as Keychain from 'react-native-keychain';
await Keychain.setGenericPassword('username', token, {
  accessControl: Keychain.ACCESS_CONTROL.BIOMETRY_CURRENT_SET_OR_DEVICE_PASSCODE,
  accessible: Keychain.ACCESSIBLE.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
  authenticationType: Keychain.AUTHENTICATION_TYPE.BIOMETRICS,
});

// CORRECT: encrypted MMKV (delegates to platform secure storage for the key)
const storage = new MMKV({
  id: 'secure',
  encryptionKey: secureEncryptionKey,  // Obtained via Keychain / Keystore
});
```

`AsyncStorage` and the unencrypted `MMKV` constructor are prohibited for any data covered by Section 4 of the standard.

---

## JS bridge as a trust boundary (Section 15)

```ts
// NEVER: a native module that accepts and executes arbitrary JS-supplied
// commands without validation
@ReactMethod
fun executeCommand(command: String) {
  Runtime.getRuntime().exec(command)  // Command injection across the bridge
}

// CORRECT: native module exposes a narrow API; all bridge inputs validated
@ReactMethod
fun showPaymentSheet(productId: String, callback: Callback) {
  if (!isValidProductId(productId)) {
    callback.invoke("invalid_product_id")
    return
  }
  // Proceed with the validated input
}
```

Old (legacy) bridge and JSI / TurboModule bridge both apply: every method call from JS that reaches native code is a trust boundary; native code validates inputs as if they came from the network.

Don't use `eval`, `Function(...)`, or dynamic `require()` on JS-bundle-supplied or remote-update-supplied strings.

---

## Network (Section 7)

```ts
// NEVER: bypass certificate validation
import https from 'https';
const agent = new https.Agent({ rejectUnauthorized: false });  // MITM trivially possible

// NEVER: ATS exception or NSC cleartext exception at the native layer
// to allow plain HTTP requests from JS-layer fetch()

// CORRECT: certificate pinning via react-native-ssl-pinning or react-native-cert-pinner
import { fetch as pinnedFetch } from 'react-native-ssl-pinning';
const response = await pinnedFetch('https://api.example.com/v1/me', {
  method: 'GET',
  sslPinning: { certs: ['sha256/PRIMARY_PIN', 'sha256/BACKUP_PIN'] },
});

// Tier 1 / Tier 2 per Section 3 require pinning; backup pins documented
```

For Tier 3 / Tier 4 apps without pinning, the native-layer ATS (iOS) and Network Security Config (Android) protections are non-negotiable: no blanket cleartext exception.

---

## Backend attestation (Section 7)

App Attest (iOS) and Play Integrity (Android) implementations live in native code; React Native consumes them via a native module.

```ts
// CORRECT: a thin RN module wraps the platform attestation calls;
// JS layer only forwards opaque tokens to the backend
import { Attestation } from './native/Attestation';

const challenge = await api.getAttestationChallenge();
const token = await Attestation.attest(challenge);  // Native module
await api.verifyAttestation(token);  // Backend verifies against Apple / Google
```

Don't roll your own attestation. Don't trust client-side verdicts.

---

## Debug-tooling exclusion in release (Section 15)

```ts
// NEVER: leave Flipper / react-native-debugger / Reactotron enabled in release
// builds — they can attach to the running process and expose state
if (__DEV__) {
  require('./ReactotronConfig');
}
// Wrong: still imported in release because the bundler keeps the import
```

```ts
// CORRECT: conditional require by __DEV__ AND the bundler is configured
// to dead-code-eliminate the dev-only branch in release builds
if (__DEV__) {
  // eslint-disable-next-line global-require
  require('./ReactotronConfig');
}
// Metro / EAS production builds strip the __DEV__ === false branch
```

Native-side Flipper integration: remove or guard the Flipper initialization in the iOS `AppDelegate` / Android `MainApplication` for release builds.

---

## Over-the-air updates (Section 15)

```ts
// NEVER: an OTA channel that delivers unsigned payloads or that can
// modify native binary behaviour
codePush.sync({ updateDialog: false, installMode: codePush.InstallMode.IMMEDIATE });
// Wrong if the CodePush keys are publishable / unrotatable

// CORRECT: signed CodePush updates verified by the client SDK
codePush.sync({
  updateDialog: false,
  installMode: codePush.InstallMode.ON_NEXT_RESTART,
  // Public key for verification is bundled with the app at install time
});
```

Same rule for EAS Update (Expo), Shorebird, and other RN OTA mechanisms: the update is signed; the client SDK verifies the signature; the OTA payload cannot grant capabilities the app did not have at install time (no new permissions, no new native code).

Native binary changes always require a store release. OTA is for JS-bundle and asset updates only.

---

## Deep links and Universal Links / App Links (Section 8)

```ts
// NEVER: a deep-link handler that triggers a sensitive action without
// session validation
Linking.addEventListener('url', ({ url }) => {
  const action = parseDeepLink(url);
  if (action.type === 'transfer') {
    performTransfer(action.amount);  // Unauthenticated; replayable
  }
});

// CORRECT: validated, replay-protected, requires explicit user confirmation
Linking.addEventListener('url', ({ url }) => {
  const action = parseSignedDeepLink(url);
  if (!action || !action.isFresh || !action.matchesCurrentSession) return;
  navigateToConfirmation(action);  // User must confirm
});
```

Use Universal Links (iOS Associated Domains) and App Links (Android with `autoVerify="true"` plus Digital Asset Links) over custom URL schemes; they require domain ownership verification at the OS level.

---

## Permissions (Section 12)

```ts
// NEVER: bundle a permission the app does not need just because a popular
// dependency might use it
// (Check the merged Info.plist usage descriptions and AndroidManifest.xml
// permissions every release; remove unused entries.)

// NEVER: a permission rationale string that does not match actual data flow
// In Info.plist: NSCameraUsageDescription = "We need this to function"
// (Apple and Google now reject deceptive descriptions)
```

`react-native-permissions` is the standard cross-platform request flow; honour the OS rationale and "Don't ask again" semantics.

---

## In-app purchases (Section 16)

```ts
// NEVER: grant entitlement from RN's purchase-result callback alone
await RNIap.requestPurchase('com.example.premium');
RNIap.purchaseUpdatedListener(async (purchase) => {
  unlockPremium();  // Client-only validation
  await RNIap.finishTransaction(purchase);
});

// CORRECT: forward the platform receipt (iOS) or purchaseToken (Android)
// to the backend; backend validates via StoreKit Server API or
// Play Developer API; backend returns the entitlement state
RNIap.purchaseUpdatedListener(async (purchase) => {
  const verified = await backend.verifyPurchase({
    productId: purchase.productId,
    receipt: purchase.transactionReceipt,    // iOS
    purchaseToken: purchase.purchaseToken,   // Android
    platform: Platform.OS,
  });
  if (verified.entitlementGranted) unlockPremium();
  await RNIap.finishTransaction(purchase);
});
```

Same rule for `react-native-iap`, `expo-in-app-purchases`, and `react-native-purchases` (RevenueCat). Backend verification is still required even when RevenueCat aggregates the validation.

---

## Logging and crash reporters

```ts
// NEVER: send raw user state to a crash reporter without redaction
Sentry.setExtra('user_data', { token, email, ssn });

// NEVER: log credentials / PII to the JS console (the console output
// can be captured by attached debuggers and by some crash-report SDKs)
console.log('Token:', token);

// CORRECT: redact before sending; use the SDK's `beforeSend` hook
Sentry.init({
  dsn: '...',
  beforeSend(event) {
    return redactPII(event);  // Strip tokens, emails, etc.
  },
});
```

---

## Expo-specific notes

- `expo-secure-store` delegates to Keychain / Keystore; acceptable for Section 4 data.
- `expo-application` and `expo-device` provide platform info; do not use platform info as a primary security signal (it is JS-readable and spoofable).
- EAS Build signing certificates managed in Expo's secrets; never in repo.
- EAS Update channels follow the OTA rule above: signed, no native-binary changes, no new permissions.

---

## Framework alignment

Implements Section 15 (hybrid and cross-platform frameworks) of [`standard-mobile-application-security.md`](../../../dev-security/standard-mobile-application-security.md) and the relevant native-layer Sections (4, 5, 6, 7, 8, 9, 11, 12, 16) as they apply through the React Native bridge.

Supplements: OWASP MASVS v2 (L1, L2, R); MASTG hybrid-framework guidance; React Native Security guide; Expo Security documentation.
