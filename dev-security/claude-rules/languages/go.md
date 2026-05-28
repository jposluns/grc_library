# Go Security Rules

These rules apply to all Go code including HTTP services, CLI tools, gRPC services, and serverless functions. They supplement the core rules in `core/`.

---

## Secrets — Go Specific

```go
// NEVER — hardcoded in source
const apiKey = "sk-..."
dbURL := "postgres://user:password@host/db"

// NEVER — in config structs initialized with literals containing secrets
config := Config{APIKey: "sk-..."}  // prohibited

// CORRECT — from environment variables
apiKey := os.Getenv("API_KEY")
if apiKey == "" {
    log.Fatal("API_KEY environment variable is not set")
}

// CORRECT — use a secrets manager SDK with workload identity
// AWS SDK, GCP SDK, or Azure SDK — authenticate via IAM role/managed identity
// Never pass credentials to the SDK directly
```

---

## SQL Injection — Go Specific

```go
// NEVER — string concatenation in queries
query := "SELECT * FROM users WHERE username = '" + username + "'"
rows, err := db.Query(query)  // SQL injection risk

// CORRECT — database/sql with positional parameters
rows, err := db.QueryContext(ctx,
    "SELECT id, email FROM users WHERE username = $1",
    username,
)

// CORRECT — named parameters with sqlx
rows, err := db.NamedQueryContext(ctx,
    "SELECT id, email FROM users WHERE username = :username",
    map[string]interface{}{"username": username},
)

// CORRECT — GORM ORM (parameterized by default)
var user User
result := db.Where("username = ?", username).First(&user)
// NEVER use db.Where("username = " + username)  ← injection risk
```

---

## Template Injection

```go
// NEVER — use text/template for HTML output (no auto-escaping)
import "text/template"
tmpl := template.Must(template.New("page").Parse("<h1>{{.Title}}</h1>"))
tmpl.Execute(w, userInput)  // XSS if userInput contains HTML

// CORRECT — use html/template for all HTML output (auto-escapes)
import "html/template"
tmpl := template.Must(template.New("page").Parse("<h1>{{.Title}}</h1>"))
tmpl.Execute(w, userInput)  // Title is automatically HTML-escaped

// NEVER — use template.HTML(), template.JS(), template.URL() with untrusted data
// These bypass escaping — only use with values you fully control
```

---

## Command Injection

```go
// NEVER — exec.Command with shell
cmd := exec.Command("sh", "-c", "ls "+userInput)  // command injection risk

// CORRECT — explicit argument list, no shell
cmd := exec.CommandContext(ctx, "ls", "-la", sanitizedPath)
output, err := cmd.Output()

// CORRECT — use Go standard library instead of shell commands
// Use os.ReadDir() instead of running ls
// Use filepath.Walk() instead of find
// Use os.Remove() instead of rm
```

---

## Path Traversal

```go
// NEVER — join user input with a base path without validation
path := filepath.Join("/uploads", userFilename)  // traversal possible with "../.."
os.Open(path)  // risk

// CORRECT — clean and validate against base directory
baseDir, _ := filepath.Abs("/uploads")
requestedPath := filepath.Join(baseDir, filepath.Clean("/"+userFilename))
if !strings.HasPrefix(requestedPath, baseDir+string(os.PathSeparator)) &&
    requestedPath != baseDir {
    http.Error(w, "Forbidden", http.StatusForbidden)
    return
}
// Now safe to use requestedPath
```

---

## Cryptography — Go Specific

```go
// NEVER — MD5 or SHA-1 for security purposes
import "crypto/md5"
import "crypto/sha1"
hash := md5.Sum(data)   // broken — do not use for security
hash := sha1.Sum(data)  // broken — do not use for security

// CORRECT — SHA-256 for integrity
import "crypto/sha256"
hash := sha256.Sum256(data)

// CORRECT — AES-GCM encryption
import (
    "crypto/aes"
    "crypto/cipher"
    "crypto/rand"
    "io"
)

func encrypt(key, plaintext []byte) ([]byte, error) {
    block, err := aes.NewCipher(key)  // key must be 32 bytes for AES-256
    if err != nil {
        return nil, err
    }
    gcm, err := cipher.NewGCM(block)
    if err != nil {
        return nil, err
    }
    nonce := make([]byte, gcm.NonceSize())
    if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
        return nil, err
    }
    return gcm.Seal(nonce, nonce, plaintext, nil), nil
}

// CORRECT — secure random token
import "crypto/rand"
import "encoding/hex"

func generateToken(n int) (string, error) {
    b := make([]byte, n)
    _, err := rand.Read(b)
    if err != nil {
        return "", err
    }
    return hex.EncodeToString(b), nil
}

// NEVER — math/rand for security tokens
import "math/rand"
token := rand.Int()  // predictable — prohibited for security use
```

---

## HTTP Security Headers

```go
// CORRECT — security middleware for HTTP handlers
func securityHeaders(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("X-Content-Type-Options", "nosniff")
        w.Header().Set("X-Frame-Options", "DENY")
        w.Header().Set("X-XSS-Protection", "0")  // use CSP instead
        w.Header().Set("Content-Security-Policy", "default-src 'self'")
        w.Header().Set("Referrer-Policy", "strict-origin-when-cross-origin")
        w.Header().Set("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        next.ServeHTTP(w, r)
    })
}

// NEVER — remove or omit security headers in production handlers
```

---

## TLS Configuration

```go
// CORRECT — TLS 1.2 minimum, secure cipher suites
tlsConfig := &tls.Config{
    MinVersion: tls.VersionTLS12,
    CipherSuites: []uint16{
        tls.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
        tls.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
        tls.TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,
        tls.TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,
    },
    PreferServerCipherSuites: true,
}
server := &http.Server{
    TLSConfig: tlsConfig,
}

// NEVER — skip TLS certificate verification
tr := &http.Transport{
    TLSClientConfig: &tls.Config{InsecureSkipVerify: true},  // prohibited in production
}
```

---

## Context and Timeout Propagation

```go
// CORRECT — always use context.Context for propagating cancellation and deadlines
func processRequest(ctx context.Context, userID string) (*Result, error) {
    // Context carries deadline from the HTTP request
    row := db.QueryRowContext(ctx, "SELECT * FROM users WHERE id = $1", userID)
    // ...
}

// NEVER — call blocking operations without a timeout
resp, err := http.Get(url)  // no timeout — risk of goroutine leak

// CORRECT — HTTP client with timeout
client := &http.Client{Timeout: 10 * time.Second}
resp, err := client.Get(url)
```

---

## Error Handling

```go
// NEVER — expose internal error details to HTTP callers
if err != nil {
    http.Error(w, err.Error(), http.StatusInternalServerError)  // leaks internals
    return
}

// CORRECT — generic error to caller, full detail to server log
if err != nil {
    correlationID := r.Header.Get("X-Correlation-ID")
    log.Printf("internal error correlationID=%s: %v", correlationID, err)
    http.Error(w, fmt.Sprintf("internal error — reference %s", correlationID), http.StatusInternalServerError)
    return
}

// NEVER — ignore errors
result, _ := doSomethingImportant()  // silent failure risk
```

---

## Dependency Management

```go
// CORRECT — use Go modules with a committed go.sum
// go.mod pins exact versions; go.sum provides checksums
// Never commit vendor/ with modified files

// Run govulncheck on every build
// go install golang.org/x/vuln/cmd/govulncheck@latest
// govulncheck ./...

// Keep dependencies minimal — each dependency increases attack surface
```

---

## SAST Tools for Go

- **govulncheck** — official Go vulnerability scanner: `golang.org/x/vuln/cmd/govulncheck`
- **gosec** — Go security checker: `github.com/securego/gosec`
- **Semgrep** with Go ruleset — pattern-based security scanning
- **staticcheck** — comprehensive Go static analysis (includes security checks)

---

## Framework Alignment

| Control Area | OWASP ASVS | NIST SSDF | ISO 27001 |
| --- | --- | --- | --- |
| Secrets management | V2.10 | PW.8.2 | A.8.24 |
| SQL injection prevention | V5.3 | PW.6 | A.8.28 |
| Template injection / XSS | V5.3 | PW.6 | A.8.28 |
| Command injection | V5.3 | PW.6 | A.8.28 |
| Path traversal | V5.3 | PW.6 | A.8.28 |
| Cryptography | V6 | PW.7 | A.8.24–8.25 |
| TLS configuration | V9 | — | A.8.24 |
| Error handling | V7 | RV.1 | A.8.15 |
| Dependency management | V1.14 | PO.5, PW.4 | A.8.8 |
