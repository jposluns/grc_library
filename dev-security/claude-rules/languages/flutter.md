# Flutter / Dart Security Rules

These rules apply to mobile applications built with Flutter and written in Dart. They supplement the core rules in `core/` and the underlying-platform rules in [`languages/swift.md`](swift.md) (iOS) and [`languages/kotlin.md`](kotlin.md) (Android). They implement the controls in [`standard-mobile-application-security.md`](../../../dev-security/standard-mobile-application-security.md), with emphasis on Section 15 (hybrid and cross-platform frameworks). Section numbers below refer to that standard.

Hybrid framework rule: Flutter shifts the layer at which a control is implemented; it does not remove the control. Every Section 4-12 requirement that applies to native iOS / Android applies to Flutter apps, delegated to the appropriate package or platform-channel method.

---

## Secure storage delegation (Section 4, Section 15)

```dart
// NEVER: sensitive data in shared_preferences
import 'package:shared_preferences/shared_preferences.dart';
final prefs = await SharedPreferences.getInstance();
await prefs.setString('auth_token', token);  // Plaintext in app sandbox

// NEVER: sensitive data in a plain file under the app directory
final file = File('${appDir.path}/token.txt');
await file.writeAsString(token);

// NEVER: SQLite database without encryption for sensitive data
final db = await openDatabase('app.db');  // sqflite default; plaintext

// CORRECT: flutter_secure_storage delegates to iOS Keychain + Android Keystore
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
const storage = FlutterSecureStorage(
  iOptions: IOSOptions(
    accessibility: KeychainAccessibility.first_unlock_this_device,
  ),
  aOptions: AndroidOptions(
    encryptedSharedPreferences: true,
    keyCipherAlgorithm: KeyCipherAlgorithm.RSA_ECB_OAEPwithSHA_256andMGF1Padding,
    storageCipherAlgorithm: StorageCipherAlgorithm.AES_GCM_NoPadding,
  ),
);
await storage.write(key: 'auth_token', value: token);

// CORRECT: SQLCipher-backed sqlite_storage for sensitive databases
import 'package:sqflite_sqlcipher/sqflite.dart';
final db = await openDatabase('app.db', password: passphraseFromSecureStorage);
```

`shared_preferences` and unencrypted sqflite are prohibited for any data covered by Section 4.

---

## Platform channels as a trust boundary (Section 15)

```dart
// NEVER: a platform channel that executes arbitrary commands from Dart
const platform = MethodChannel('app.example/native');
await platform.invokeMethod('executeShell', userSuppliedCommand);
```

```kotlin
// And on the native side:
methodChannel.setMethodCallHandler { call, result ->
    when (call.method) {
        "executeShell" -> {
            // NEVER: pass call.arguments straight to Runtime.exec
            val cmd = call.arguments as String
            Runtime.getRuntime().exec(cmd)
        }
    }
}
```

```dart
// CORRECT: platform channels expose a narrow validated API
await platform.invokeMethod('showPaymentSheet', {
  'productId': validatedProductId,
});
```

```kotlin
// On the native side: validate inputs as if from the network
"showPaymentSheet" -> {
    val productId = call.argument<String>("productId")
    if (!isValidProductId(productId)) {
        result.error("INVALID_ARG", "productId invalid", null)
        return@setMethodCallHandler
    }
    // proceed
}
```

Same rule for `PigeonInterface` (codegen) and FFI: every cross-boundary call is a trust boundary; native code validates inputs as if from the network.

---

## Network (Section 7)

```dart
// NEVER: blanket bypass certificate validation
HttpOverrides.global = MyHttpOverrides();
class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback = (X509Certificate cert, String host, int port) => true;
  }
}
```

```dart
// CORRECT: certificate pinning via http_certificate_pinning or
// the platform's pin support via Network Security Config / ATS
import 'package:http_certificate_pinning/http_certificate_pinning.dart';

final secureResponse = await HttpCertificatePinning.check(
  serverURL: 'https://api.example.com',
  headerHttp: {},
  sha: SHA.SHA256,
  allowedSHAFingerprints: ['PRIMARY_PIN', 'BACKUP_PIN'],
  timeout: 30,
);
```

For Tier 1 / Tier 2 apps (per Section 3), pinning is required. The native-layer ATS (iOS) and Network Security Config (Android) constraints from Sections 4-5 still apply to Flutter HTTP traffic.

---

## Backend attestation (Section 7)

App Attest (iOS) and Play Integrity (Android) live in native code; consume them via a Flutter package or a platform channel.

```dart
// CORRECT: a thin Flutter package wraps the platform attestation calls;
// Dart layer only forwards opaque tokens to the backend
import 'package:flutter_app_attest/flutter_app_attest.dart';

final challenge = await api.getAttestationChallenge();
final token = await FlutterAppAttest.attest(challenge);
await api.verifyAttestation(token);  // Backend verifies against Apple / Google
```

Don't trust attestation verdicts client-side. The backend is the verifier.

---

## Debug-tooling exclusion in release (Section 15)

```dart
// NEVER: leave debug-only code paths enabled in release
if (kDebugMode) {
  // verbose logging, debug UI, mock data sources
} else {
  // production path
}
// Wrong if the debug branch leaks state into release telemetry
// (e.g. crash reports include debug-only labels)

// CORRECT: kReleaseMode-gated production builds; assertions and debug
// branches dead-code-eliminated by the Dart compiler
assert(() {
  debugPrint('Sensitive state: $state');  // Stripped in release
  return true;
}());
```

Build production binaries with `flutter build apk --release --obfuscate --split-debug-info=symbols/` and equivalent for `--target-platform`. Obfuscation by itself is not a security boundary, but the standard's Section 9 requires it for release builds in Tier 1 / Tier 2.

Dart DevTools attaches only in debug / profile builds; verify your CI does not ship profile builds to production.

---

## Over-the-air updates (Section 15)

Flutter does not ship an Apple- or Google-blessed OTA mechanism analogous to React Native CodePush, because Apple and Google prohibit code OTA in their stores' default terms. Third-party solutions exist:

```dart
// CORRECT: Shorebird delivers signed Dart code updates;
// signature verification is non-bypassable in the Shorebird client
// (see https://shorebird.dev/ for the signing model)
// Updates cannot grant new permissions or modify native code.

// NEVER: a "code push" that loads untrusted Dart code from a
// network source and executes it via dart:mirrors or equivalent
```

If OTA is used, the same Section 15 rules apply: signed payloads, no native-binary changes, no new permissions, signature verification cannot be bypassed.

---

## Deep links and App Links / Universal Links (Section 8)

```dart
// NEVER: deep-link handler that triggers a sensitive action without
// session validation
final initialLink = await getInitialLink();
if (initialLink?.path == '/transfer') {
  performTransfer(initialLink!.queryParameters['amount']);  // Replayable
}

// CORRECT: validated, replay-protected, requires explicit user confirmation
linkStream.listen((Uri? uri) {
  if (uri == null) return;
  final action = parseSignedDeepLink(uri);
  if (action == null || !action.isFresh || !action.matchesCurrentSession) {
    return;
  }
  navigatorKey.currentState?.pushNamed('/confirm', arguments: action);
});
```

Use `App Links` (Android `autoVerify="true"` + Digital Asset Links) and `Universal Links` (iOS Associated Domains) over custom URL schemes.

---

## Permissions (Section 12)

```dart
// NEVER: request a broad permission for a narrow need
await Permission.locationAlways.request();  // For a feature that needs only "while in use"

// CORRECT: narrow scope; rationale shown
final status = await Permission.locationWhenInUse.request();
```

`permission_handler` is the standard cross-platform request flow; respect the OS rationale and "permanently denied" semantics. Photo Picker (`image_picker` with the system picker on iOS 14+ and Android 13+) does not require storage permissions and is preferred where the use case fits.

---

## In-app purchases (Section 16)

```dart
// NEVER: grant entitlement from the in_app_purchase plugin's purchase
// stream alone
import 'package:in_app_purchase/in_app_purchase.dart';

InAppPurchase.instance.purchaseStream.listen((purchases) {
  for (final purchase in purchases) {
    if (purchase.status == PurchaseStatus.purchased) {
      unlockPremium();  // Client-only validation
      InAppPurchase.instance.completePurchase(purchase);
    }
  }
});

// CORRECT: forward platform receipt (iOS) or purchaseToken (Android)
// to the backend; backend validates against StoreKit Server API or
// Play Developer API; backend returns the entitlement state
InAppPurchase.instance.purchaseStream.listen((purchases) async {
  for (final purchase in purchases) {
    if (purchase.status != PurchaseStatus.purchased) continue;
    final verified = await backend.verifyPurchase(
      productId: purchase.productID,
      verificationData: purchase.verificationData.serverVerificationData,
      platform: Platform.isIOS ? 'ios' : 'android',
    );
    if (verified.entitlementGranted) unlockPremium();
    await InAppPurchase.instance.completePurchase(purchase);
  }
});
```

`verificationData.serverVerificationData` carries the StoreKit JWS (iOS) or `purchaseToken` (Android) for backend verification per Section 16.

---

## Logging and crash reporters

```dart
// NEVER: log credentials / PII
debugPrint('Token: $token');
log('User $email logged in');

// CORRECT: redact; SDK-specific hooks
import 'package:sentry_flutter/sentry_flutter.dart';
await SentryFlutter.init((options) {
  options.beforeSend = (event, hint) {
    return redactPII(event);
  };
});
```

`Crashlytics.instance.setCustomKey('user_id_hash', userIdHash)` not the raw email or token.

---

## Framework alignment

Implements Section 15 (hybrid and cross-platform frameworks) of [`standard-mobile-application-security.md`](../../../dev-security/standard-mobile-application-security.md) and the relevant native-layer Sections (4, 5, 6, 7, 8, 9, 11, 12, 16) as they apply through Flutter's platform-channel bridge and Dart runtime.

Supplements: OWASP MASVS v2 (L1, L2, R); MASTG hybrid-framework guidance; Flutter Security best practices documentation.
