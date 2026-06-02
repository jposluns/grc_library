# Capacitor / Ionic Security Rules

These rules apply to mobile applications built with Capacitor (the modern Cordova successor) and Ionic Framework. They supplement the core rules in `core/`, the TypeScript / JavaScript rules in [`languages/typescript.md`](typescript.md), and the underlying-platform rules in [`languages/swift.md`](swift.md) (iOS) and [`languages/kotlin.md`](kotlin.md) (Android). They implement the controls in [`standard-mobile-application-security.md`](../../../dev-security/standard-mobile-application-security.md), with emphasis on Section 13 (hybrid and cross-platform frameworks). Section numbers below refer to that standard.

Hybrid framework rule: Capacitor wraps a WebView and exposes native APIs through plugins; Ionic adds UI components on top of either Capacitor or Cordova. Web-stack security (CSP, XSS, etc.) and mobile-stack security (Sections 2-10) BOTH apply. The WebView IS the application UI, so any control assumed to be enforced at the network or browser layer must be enforced inside the WebView host.

If the app is on Cordova rather than Capacitor: migrate. Cordova is in maintenance mode (per Apache's published status) and most plugins have lagging security maintenance.

---

## Secure storage delegation (Section 2, Section 13)

```ts
// NEVER: sensitive data in @capacitor/preferences (insecure by default)
import { Preferences } from '@capacitor/preferences';
await Preferences.set({ key: 'auth_token', value: token });  // Plaintext

// NEVER: sensitive data in localStorage / IndexedDB inside the WebView
localStorage.setItem('auth_token', token);  // Plaintext, JS-readable

// CORRECT: a secure-storage plugin that delegates to platform key stores
import { SecureStoragePlugin } from 'capacitor-secure-storage-plugin';
await SecureStoragePlugin.set({ key: 'auth_token', value: token });
// Or @aparajita/capacitor-secure-storage:
import { SecureStorage } from '@aparajita/capacitor-secure-storage';
await SecureStorage.set('auth_token', token, true /* synchronized */, false /* access via biometry */);
```

`@capacitor/preferences`, `localStorage`, `sessionStorage`, IndexedDB, and `WebSQL` are all prohibited for any data covered by Section 2. The same rule applies to Ionic Storage when configured with the default driver.

---

## Content Security Policy in the wrapped WebView (Section 13)

```html
<!-- NEVER: missing CSP -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>

<!-- NEVER: CSP that permits unsafe-inline and unsafe-eval -->
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self' 'unsafe-inline' 'unsafe-eval' data: gap:">

<!-- CORRECT: explicit CSP scoped to the app's origins and capacitor:// -->
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self' capacitor://* ionic://*;
               script-src 'self';
               style-src 'self' 'unsafe-hashes';
               img-src 'self' https: data:;
               connect-src 'self' https://api.example.com">
```

The bundler (Vite, Webpack) is configured to extract inline styles into separate files so `unsafe-inline` is unnecessary. Ionic Angular and Ionic React frameworks both support hashed inline styles via the build pipeline.

---

## JavaScript bridge / plugin trust boundary (Section 13)

```typescript
// NEVER: a custom plugin that runs arbitrary native code from JS
@CapacitorPlugin(name = "ShellPlugin")
class ShellPlugin: Plugin() {
    @PluginMethod
    fun exec(call: PluginCall) {
        val cmd = call.getString("cmd") ?: return
        Runtime.getRuntime().exec(cmd)  // Bridge command injection
    }
}

// CORRECT: plugin exposes a narrow API; all bridge inputs validated
@CapacitorPlugin(name = "PaymentSheet")
class PaymentSheetPlugin: Plugin() {
    @PluginMethod
    fun show(call: PluginCall) {
        val productId = call.getString("productId") ?: run {
            call.reject("productId required")
            return
        }
        if (!isValidProductId(productId)) {
            call.reject("productId invalid")
            return
        }
        // Proceed with validated input
    }
}
```

Treat every plugin call from the WebView as untrusted: the WebView's origin can include user-supplied content (deep links, OAuth flows, embedded content) and a compromised page can call any registered plugin.

Cordova plugins (if migration is incomplete): audit each plugin's permission and capability surface; remove unused plugins.

---

## Network (Section 5)

```ts
// NEVER: bypass CSP's connect-src by setting allowMixedContent on the WebView
// (Capacitor capacitor.config.json):
{
  "android": {
    "allowMixedContent": true   // Allows http:// inside the app
  }
}
```

```ts
// CORRECT: HTTPS-only; certificate pinning via @capacitor-community/http
// or via a custom native HTTP plugin
import { CapacitorHttp } from '@capacitor/core';

const response = await CapacitorHttp.request({
  url: 'https://api.example.com/v1/me',
  method: 'GET',
  // Pinning is configured at the native layer per platform's
  // Network Security Config (Android) and URLSessionDelegate (iOS)
});
```

For Tier 1 / Tier 2 apps (per Section 1), certificate pinning is required. Capacitor delegates HTTP to the native layer when `CapacitorHttp` is enabled; otherwise the WebView's `fetch` / `XMLHttpRequest` uses the WebView's HTTP stack and pinning is harder.

---

## Backend attestation (Section 5)

App Attest (iOS) and Play Integrity (Android) implementations live in native plugin code; the JS layer forwards opaque tokens.

```ts
// CORRECT: plugin wraps native attestation; JS forwards token only
import { Attestation } from './plugins/attestation';

const challenge = await api.getAttestationChallenge();
const token = await Attestation.attest({ challenge });
await api.verifyAttestation(token);  // Backend verifies against Apple / Google
```

Don't trust attestation client-side; don't roll your own. The Capacitor plugin must call the native platform API, not a JS-side mock.

---

## Deep links and App Links / Universal Links (Section 6)

```ts
// NEVER: deep-link handler that triggers a sensitive action without validation
import { App } from '@capacitor/app';

App.addListener('appUrlOpen', (event) => {
  const url = new URL(event.url);
  if (url.pathname === '/transfer') {
    performTransfer(url.searchParams.get('amount'));  // Replayable
  }
});

// CORRECT: validated, replay-protected, requires explicit user confirmation
App.addListener('appUrlOpen', (event) => {
  const action = parseSignedDeepLink(event.url);
  if (!action || !action.isFresh || !action.matchesCurrentSession) return;
  router.push('/confirm', { state: action });
});
```

Use App Links (Android `autoVerify="true"`) and Universal Links (iOS Associated Domains) over custom URL schemes; configure via `capacitor.config.json` and platform-specific files.

---

## Permissions (Section 10)

```ts
// NEVER: request a broad permission for a narrow need
import { Geolocation } from '@capacitor/geolocation';
await Geolocation.requestPermissions({ permissions: ['location', 'coarseLocation'] });
// when only coarseLocation is actually needed

// CORRECT: narrow scope
await Geolocation.requestPermissions({ permissions: ['coarseLocation'] });
```

`Camera`, `Geolocation`, `LocalNotifications`, `PushNotifications` all expose `requestPermissions` with platform-specific options. Honour the rationale strings; do not request permissions just because a plugin happens to support them.

---

## Debug-tooling exclusion in release (Section 13)

```ts
// NEVER: leave the WebView inspector enabled in release
// (capacitor.config.json):
{
  "ios": {
    "webContentsDebuggingEnabled": true  // iOS 16+: web inspector accessible
  },
  "android": {
    "webContentsDebuggingEnabled": true  // chrome://inspect can attach
  }
}

// CORRECT: enable only in debug variants
{
  "ios": {
    "webContentsDebuggingEnabled": false
  },
  "android": {
    "webContentsDebuggingEnabled": false
  }
}
```

For Cordova: same rule via `<preference name="AndroidInsecureFileModeEnabled" value="false">` and similar.

---

## Over-the-air updates (Section 13)

Apple and Google permit OTA of web assets (HTML, CSS, JS) but not native code, subject to the store's review policies. Ionic Appflow Live Updates is one option; Capacitor Live Updates is another. Both must satisfy the Section 13 OTA rule.

```ts
// CORRECT: signed Live Update channels
import { LiveUpdate } from '@capacitor/live-updates';

const sync = await LiveUpdate.sync();
// Update payload signature verification is non-bypassable in the SDK
// when configured with public-key verification
```

Live Updates cannot grant new permissions or modify native code. Plugin updates that change permission scope require a store release.

---

## In-app purchases (Section 14)

```ts
// NEVER: grant entitlement from a Capacitor IAP plugin result alone
import { CdvPurchase } from 'cordova-plugin-purchase';
CdvPurchase.store.when().approved((p) => {
  unlockPremium();  // Client-only validation
  p.finish();
});

// CORRECT: forward platform receipt to backend for verification
CdvPurchase.store.when().approved(async (purchase) => {
  const verified = await backend.verifyPurchase({
    productId: purchase.id,
    receipt: purchase.transaction?.appStoreReceipt,    // iOS
    purchaseToken: purchase.transaction?.purchaseToken, // Android
    platform: Capacitor.getPlatform(),
  });
  if (verified.entitlementGranted) unlockPremium();
  await purchase.finish();
});
```

`cordova-plugin-purchase` (now also Capacitor-compatible) and `@capacitor-community/in-app-purchases` both require backend verification per Section 14.

---

## Cross-site scripting in the WebView (web-stack carryover)

The WebView IS the UI; any standard web XSS / DOM-XSS vulnerability ships as a native-app vulnerability.

```ts
// NEVER: inject untrusted HTML
const div = document.getElementById('feed');
div!.innerHTML = userSuppliedHtml;  // XSS

// CORRECT: rely on the framework's default escaping (Angular interpolation,
// React JSX, Vue mustaches all escape by default); use a sanitiser when
// raw HTML is unavoidable
// Angular: bypassSecurityTrustHtml only with explicit DomSanitizer review
// React: use a vetted library like DOMPurify before dangerouslySetInnerHTML
```

The Ionic framework's components are XSS-safe when used with the framework's idiomatic data binding; raw `[innerHTML]` / `dangerouslySetInnerHTML` patterns require an explicit sanitisation step.

---

## Framework alignment

Implements Section 13 (hybrid and cross-platform frameworks) of [`standard-mobile-application-security.md`](../../../dev-security/standard-mobile-application-security.md) and the relevant native-layer Sections (2, 5, 6, 10, 14) as they apply through Capacitor's WebView + plugin architecture. Web-stack security from [`languages/typescript.md`](typescript.md) and `core/owasp.md` also applies because the WebView IS the application UI.

Supplements: OWASP MASVS v2 (L1, L2, R); MASTG hybrid-framework guidance; Capacitor security documentation; Ionic security best practices.
