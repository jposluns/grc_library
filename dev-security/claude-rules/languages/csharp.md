# C# / .NET Security Rules

These rules apply to all C# and .NET code including ASP.NET Core, Azure Functions, .NET Worker Services, and console applications. They supplement the core rules in `core/`.

---

## Secrets: c# / .NET specific

```csharp
// NEVER: hardcoded in source
private const string ApiKey = "sk-...";
var connString = "Server=myserver;Password=mypassword;";

// NEVER: in appsettings.json committed to source control
// { "ConnectionStrings": { "Default": "Server=...;Password=..." } }  // WRONG

// CORRECT: from environment variables
var apiKey = Environment.GetEnvironmentVariable("API_KEY")
    ?? throw new InvalidOperationException("API_KEY is not configured");

// CORRECT: User Secrets for local development (dev only, not production)
// dotnet user-secrets set "ApiKey" "value"
// Reads from: %APPDATA%\Microsoft\UserSecrets\<user_secrets_id>\secrets.json
// NEVER in production

// CORRECT: from secrets management service via managed identity
// No credential required in code when using managed identity
var client = new SecretClient(
    new Uri(vaultUri),
    new DefaultAzureCredential());
var secret = await client.GetSecretAsync("api-key");
```

Configuration injection via `IConfiguration` / `IOptions<T>`: secret values should be populated from environment variables or secrets management service at runtime, not from `appsettings.json` in version control.

---

## SQL injection: c# / .NET specific

```csharp
// NEVER: string concatenation
var query = "SELECT * FROM Users WHERE Id = " + userId;
cmd.CommandText = query;

// NEVER: string interpolation
cmd.CommandText = $"SELECT * FROM Users WHERE Id = {userId}";

// CORRECT: parameterized (System.Data.SqlClient / Microsoft.Data.SqlClient)
cmd.CommandText = "SELECT * FROM Users WHERE Id = @UserId";
cmd.Parameters.AddWithValue("@UserId", userId);

// CORRECT: Entity Framework (parameterizes automatically)
var user = await context.Users.FindAsync(userId);

// NEVER: EF raw SQL with interpolation
var users = context.Users.FromSqlRaw($"SELECT * FROM Users WHERE Id = {userId}");  // UNSAFE

// CORRECT: EF raw SQL parameterized
var users = context.Users.FromSqlInterpolated($"SELECT * FROM Users WHERE Id = {userId}");
// or
var users = context.Users.FromSqlRaw("SELECT * FROM Users WHERE Id = {0}", userId);
```

---

## Command injection: c# / .NET specific

```csharp
// NEVER: Process.Start with shell and user input
Process.Start("cmd.exe", $"/c process {userInput}");

// CORRECT: Process with argument array, no shell
var process = new Process
{
    StartInfo = new ProcessStartInfo
    {
        FileName = "process",
        ArgumentList = { userInput },  // Separate arguments
        UseShellExecute = false,
        RedirectStandardOutput = true
    }
};
process.Start();

// NEVER: eval-equivalent in Roslyn (dynamic compilation of user input)
var compilation = CSharpCompilation.Create(...)...;  // Never with user-supplied code
```

---

## Cryptography: c# / .NET specific

```csharp
// CORRECT: AES-256-GCM
using var aesGcm = new AesGcm(key);
byte[] nonce = new byte[AesGcm.NonceByteSizes.MaxSize];
RandomNumberGenerator.Fill(nonce);
aesGcm.Encrypt(nonce, plaintext, ciphertext, tag);

// CORRECT: Password hashing (use BCrypt.Net-Next or ASP.NET Core Identity)
// ASP.NET Core Identity PasswordHasher uses PBKDF2 with HMAC-SHA512
var hasher = new PasswordHasher<object>();
string hash = hasher.HashPassword(null, password);

// PROHIBITED: MD5, SHA1 for security purposes
using var md5 = MD5.Create();
var hash = md5.ComputeHash(data);  // Broken for security

// CORRECT: SHA-256 for integrity hashing
using var sha256 = SHA256.Create();
var hash = sha256.ComputeHash(data);

// CORRECT: cryptographically secure random
byte[] token = RandomNumberGenerator.GetBytes(32);
string tokenHex = Convert.ToHexString(token);

// PROHIBITED
var rng = new Random();  // Not cryptographically secure
var token = rng.Next().ToString();
```

---

## XSS prevention: asp.net core specific

Razor pages and Blazor HTML-encode output by default. Dangerous patterns:

```csharp
// NEVER: @Html.Raw with user input
@Html.Raw(userInput)  // XSS risk

// CORRECT: default Razor encoding
@userInput // Auto-encoded: safe

// NEVER: HtmlString with unvalidated user input
new HtmlString(userInput)  // XSS risk

// CORRECT: only with sanitized content
using Ganss.Xss;
var sanitizer = new HtmlSanitizer();
var sanitized = sanitizer.Sanitize(userInput);
new HtmlString(sanitized)
```

---

## Deserialization

```csharp
// NEVER: BinaryFormatter (removed in .NET 8, but legacy code may use it)
// BinaryFormatter is prohibited: remote code execution risk

// NEVER: JSON.NET TypeNameHandling.All with untrusted data
var settings = new JsonSerializerSettings
{
    TypeNameHandling = TypeNameHandling.All  // Remote code execution with untrusted JSON
};

// CORRECT: System.Text.Json (safe by default, no polymorphic deserialization)
var obj = JsonSerializer.Deserialize<MyType>(json);

// CORRECT: JSON.NET with TypeNameHandling.None
var settings = new JsonSerializerSettings
{
    TypeNameHandling = TypeNameHandling.None
};
```

---

## SSRF: c# / .NET specific

```csharp
// NEVER: HttpClient with user-supplied URL without validation
var response = await httpClient.GetAsync(userSuppliedUrl);

// CORRECT: validate against allowlist
private static readonly HashSet<string> AllowedHosts = new() { "api.example.com" };

var uri = new Uri(userSuppliedUrl);
if (!AllowedHosts.Contains(uri.Host))
    throw new ArgumentException("URL not in allowlist");
var response = await httpClient.GetAsync(uri);
```

---

## ASP.NET core security configuration

```csharp
// Startup / Program.cs

// HTTPS redirection
app.UseHttpsRedirection();

// HSTS
app.UseHsts();

// Security headers (use NWebsec or custom middleware)
app.Use(async (context, next) =>
{
    context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Add("X-Frame-Options", "DENY");
    context.Response.Headers.Add("Referrer-Policy", "no-referrer");
    await next();
});

// CORS: explicit allowlist, never wildcard in production
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowedOrigins", policy =>
    {
        policy.WithOrigins("https://app.example.com")  // Explicit, not AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

// NEVER in production
// .AllowAnyOrigin() // Wildcard: prohibited
```

---

## SAST tools for c# / .NET

Recommended: Security Code Scan, Semgrep with C# rules, Roslyn Analyzers with security rulesets. Run in CI/CD.

---

## Framework alignment

Supplements `core/` rules. C# / .NET controls implement:
- OWASP ASVS V5 (Input), V6 (Crypto), V3 (Session), V14 (Config)
- OWASP Top 10 A03 (Injection), A02 (Crypto), A07 (Auth)
- NIST SSDF PW.6, PW.8