# .NET MAUI Security Rules

These rules apply to mobile applications built with .NET MAUI (Multi-platform App UI). They supplement the core rules in `core/`, the server-side C# rules in [`languages/csharp.md`](csharp.md), and the underlying-platform rules in [`languages/swift.md`](swift.md) (iOS) and [`languages/kotlin.md`](kotlin.md) (Android). They implement the controls in [`standard-mobile-application-security.md`](../../../dev-security/standard-mobile-application-security.md), with emphasis on Section 15 (hybrid and cross-platform frameworks). Section numbers below refer to that standard.

Hybrid framework rule: .NET MAUI shifts the layer at which a control is implemented; it does not remove the control. The C# layer runs on top of the native iOS / Android platforms via Mono / .NET runtime; every Section 4-12 requirement that applies to native still applies to a MAUI app, delegated to the appropriate .NET API or native handler.

For Blazor Hybrid apps within MAUI, the additional WebView controls in Section 15 apply on top of the rules below.

---

## Secure storage delegation (Section 4, Section 15)

```csharp
// NEVER: sensitive data in Preferences (the cross-platform .NET preferences API)
Preferences.Set("auth_token", token);  // Plaintext in iOS NSUserDefaults / Android SharedPreferences

// NEVER: sensitive data in a plain file or unencrypted SQLite
File.WriteAllText(Path.Combine(FileSystem.AppDataDirectory, "token.txt"), token);

// CORRECT: SecureStorage delegates to iOS Keychain + Android Keystore
await SecureStorage.Default.SetAsync("auth_token", token);
var retrieved = await SecureStorage.Default.GetAsync("auth_token");

// CORRECT: SQLite with encryption (sqlite-net-base + sqlcipher integration)
// configured at connection open
var options = new SQLiteConnectionString(
    Path.Combine(FileSystem.AppDataDirectory, "app.db"),
    storeDateTimeAsTicks: true,
    key: encryptionKey  // Obtained via SecureStorage
);
var connection = new SQLiteAsyncConnection(options);
```

`Preferences` and unencrypted SQLite are prohibited for any data covered by Section 4.

---

## Cross-platform handlers and dependency-service trust boundary (Section 15)

```csharp
// NEVER: a custom handler that exposes broad native APIs to the
// MAUI / Blazor layer without validation
public interface INativeBridge
{
    string ExecuteCommand(string command);  // Too broad
}

// CORRECT: handlers expose narrow, validated APIs
public interface IPaymentSheet
{
    Task<PaymentResult> ShowAsync(string productId);
}

public class PaymentSheetImplementation : IPaymentSheet
{
    public async Task<PaymentResult> ShowAsync(string productId)
    {
        if (!IsValidProductId(productId))
        {
            return PaymentResult.InvalidArgument;
        }
        // Proceed
    }
}
```

Same rule for Blazor Hybrid's `IJSRuntime` interop: every call from the WebView's JS into native code is a trust boundary; the native code validates inputs as if from the network.

---

## Network (Section 7)

```csharp
// NEVER: globally trust any server certificate
ServicePointManager.ServerCertificateValidationCallback = (s, c, ch, e) => true;

// NEVER: HttpClient configured with a permissive ServerCertificateCustomValidationCallback
var handler = new HttpClientHandler
{
    ServerCertificateCustomValidationCallback = (req, cert, chain, errors) => true,
};

// CORRECT: certificate pinning via a SocketsHttpHandler custom validator
var handler = new SocketsHttpHandler
{
    SslOptions = new SslClientAuthenticationOptions
    {
        RemoteCertificateValidationCallback = (sender, cert, chain, errors) =>
            ValidatePin(cert, expectedPinSet: new[] { "PRIMARY", "BACKUP" }),
    },
};
var client = new HttpClient(handler);
```

For Tier 1 / Tier 2 (per Section 3), pinning is required. Native iOS ATS and Android Network Security Config still apply at the platform layer below MAUI.

---

## Backend attestation (Section 7)

App Attest (iOS) and Play Integrity (Android) live in the native iOS / Android platforms; consume them via a partial-class platform implementation or a NuGet wrapper.

```csharp
// CORRECT: platform-conditional implementation; client sends opaque token
// to backend for verification
public interface IAttestationService
{
    Task<string> AttestAsync(string challenge);
}

#if IOS
public class AttestationService : IAttestationService
{
    public async Task<string> AttestAsync(string challenge)
    {
        // Use DCAppAttestService bindings
    }
}
#elif ANDROID
public class AttestationService : IAttestationService
{
    public async Task<string> AttestAsync(string challenge)
    {
        // Use Play Integrity API bindings
    }
}
#endif

// Then on the call site:
var token = await attestationService.AttestAsync(challenge);
await backend.VerifyAttestation(token);  // Backend verifies
```

Don't trust attestation client-side. Don't roll your own.

---

## Build hardening and release configuration (Section 9, Section 15)

```xml
<!-- NEVER: ship a Debug-mode release; ship release without trimming/AOT review -->
<PropertyGroup Condition="'$(Configuration)|$(TargetFramework)' == 'Release|net8.0-android'">
    <DebugType>none</DebugType>
    <Optimize>true</Optimize>
    <AndroidLinkMode>SdkOnly</AndroidLinkMode>
    <EnableLLVM>true</EnableLLVM>
    <AndroidUseAapt2>true</AndroidUseAapt2>
</PropertyGroup>

<!-- For iOS release: -->
<PropertyGroup Condition="'$(Configuration)|$(TargetFramework)' == 'Release|net8.0-ios'">
    <UseInterpreter>false</UseInterpreter>
    <MtouchLink>SdkOnly</MtouchLink>
    <MtouchUseLlvm>true</MtouchUseLlvm>
    <CodesignKey>iPhone Distribution: ...</CodesignKey>
</PropertyGroup>
```

ProGuard / R8 rules for Android release (via `<AndroidEnableProguard>true</AndroidEnableProguard>` in csproj). Assembly trimming reviewed for false-positive removals.

`DEBUG`-conditional code paths must not leak into release builds:

```csharp
#if DEBUG
    Logger.LogTrace("Verbose state: {state}", state);
#endif
```

Hot reload (`MAUI` hot reload, XAML hot reload) attaches in debug only; verify your CI is not producing hot-reload-instrumented release artefacts.

---

## Deep links (Section 8)

```csharp
// NEVER: a deep-link handler triggering sensitive action without validation
public override bool OpenUrl(UIApplication app, NSUrl url, NSDictionary options)
{
    // url.AbsoluteString = "myapp://transfer?amount=1000"
    PerformTransfer(ParseAmount(url));  // Unauthenticated; replayable
    return true;
}

// CORRECT: validated, replay-protected, requires explicit user confirmation
// Use MAUI's Shell routing or AppLinks / Universal Links
[QueryProperty(nameof(SignedAction), "action")]
public partial class ConfirmPage : ContentPage
{
    public string? SignedAction
    {
        set
        {
            var action = ParseSignedDeepLink(value);
            if (action == null || !action.IsFresh || !action.MatchesCurrentSession) return;
            ShowConfirmation(action);
        }
    }
}
```

Use App Links (Android `autoVerify="true"`) and Universal Links (iOS Associated Domains) configured in the MAUI project's `Platforms/Android/AndroidManifest.xml` and `Platforms/iOS/Entitlements.plist`.

---

## Permissions (Section 12)

```csharp
// NEVER: request a permission the app does not need
var status = await Permissions.RequestAsync<Permissions.LocationAlways>();
// for a feature that only needs LocationWhenInUse

// CORRECT: narrow permission scope
var status = await Permissions.RequestAsync<Permissions.LocationWhenInUse>();
```

`Permissions` cross-platform API maps to platform-native flows. Honour `PermissionStatus.Denied` and "permanently denied" cases; do not retry prompts that the user has dismissed permanently.

---

## In-app purchases (Section 16)

MAUI does not ship a first-party IAP API. Common community options: `Plugin.InAppBilling` (cross-platform), `Xamarin.Essentials.InAppPurchase` (legacy), or platform-specific bindings.

```csharp
// NEVER: grant entitlement from the IAP plugin result alone
var purchase = await CrossInAppBilling.Current.PurchaseAsync(productId, ItemType.InAppPurchase);
if (purchase != null && purchase.State == PurchaseState.Purchased)
{
    GrantEntitlement();  // Client-only validation
}

// CORRECT: forward the receipt (iOS) or purchase token (Android) to the
// backend; backend validates via StoreKit Server API / Play Developer API
if (purchase != null && purchase.State == PurchaseState.Purchased)
{
    var verified = await backend.VerifyPurchaseAsync(new VerifyPurchaseRequest
    {
        ProductId = purchase.ProductId,
        Receipt = purchase.PurchaseToken,  // iOS: ASN.1 receipt or JWS; Android: purchaseToken
        Platform = DeviceInfo.Platform.ToString(),
    });
    if (verified.EntitlementGranted) GrantEntitlement();
    await CrossInAppBilling.Current.FinishPurchaseAsync(purchase);
}
```

Same rule for `Plugin.InAppBilling`, `RevenueCat.Xamarin`, and any platform-specific binding.

---

## Logging and crash reporters

```csharp
// NEVER: log credentials / PII
Logger.LogInformation("Token: {token}, User: {email}", token, email);

// CORRECT: scoped logging that strips sensitive fields
Logger.LogInformation("Auth event for user {userIdHash}", HashUserId(userId));
```

`Microsoft.AppCenter.Crashes` / Sentry / Firebase Crashlytics: use the SDK's `beforeSend` / `SetAttachmentsHandler` to redact PII before transmission.

---

## Blazor Hybrid (MAUI Blazor) WebView (Section 7, Section 15)

```razor
@* NEVER: render unsanitized user-supplied HTML *@
<div>@((MarkupString)userInput)</div>

@* CORRECT: rely on Razor's default HTML-encoding; render plain text *@
<div>@userInput</div>
```

```csharp
// NEVER: blanket allow-all CSP on the BlazorWebView
// CORRECT: CSP delivered via served content; restrict origins; no
// unsafe-inline / unsafe-eval; the BlazorWebView's hostpage HTML
// includes the appropriate <meta http-equiv="Content-Security-Policy">
```

`IJSRuntime.InvokeAsync` calls into JS from C#; if untrusted JS is also loaded into the WebView (it should not be), the IJSRuntime callable surface is a trust boundary.

---

## Framework alignment

Implements Section 15 of [`standard-mobile-application-security.md`](../../../dev-security/standard-mobile-application-security.md) and the relevant native-layer Sections (4, 5, 6, 7, 8, 9, 11, 12, 16) as they apply through .NET MAUI's handler architecture and Mono / .NET runtime on iOS and Android.

Supplements: OWASP MASVS v2 (L1, L2, R); MASTG hybrid-framework guidance; .NET MAUI documentation security topics.
