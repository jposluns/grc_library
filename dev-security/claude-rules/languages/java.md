# Java / Spring Security Rules

These rules apply to all Java and Kotlin code including Spring Boot, Jakarta EE, plain Java services, and serverless functions. They supplement the core rules in `core/`.

---

## Secrets: Java Specific

```java
// NEVER — hardcoded in source
private static final String API_KEY = "sk-...";
String connString = "jdbc:postgresql://host/db?user=admin&password=secret";

// NEVER — in application.properties / application.yml committed to source control
// spring.datasource.password=mysecret   ← WRONG if committed

// CORRECT — from environment variables
String apiKey = System.getenv("API_KEY");
if (apiKey == null || apiKey.isBlank()) {
    throw new IllegalStateException("API_KEY environment variable is not configured");
}

// CORRECT — Spring Boot externalized configuration with env override
// application.properties: spring.datasource.password=${DB_PASSWORD}
// Set DB_PASSWORD in the deployment environment or secrets manager

// CORRECT — AWS Secrets Manager / Azure Key Vault / GCP Secret Manager via SDK
// Use the platform SDK with managed identity — never pass credentials to the SDK call
```

---

## SQL Injection: Java Specific

```java
// NEVER — string concatenation in queries
String query = "SELECT * FROM users WHERE username = '" + username + "'";
stmt.executeQuery(query);  // SQL injection risk

// NEVER — JPQL/HQL string concatenation
String jpql = "FROM User WHERE username = '" + username + "'";  // injection risk

// CORRECT — JDBC PreparedStatement
String sql = "SELECT * FROM users WHERE username = ?";
PreparedStatement stmt = conn.prepareStatement(sql);
stmt.setString(1, username);
ResultSet rs = stmt.executeQuery();

// CORRECT — Spring JdbcTemplate named parameters
String sql = "SELECT * FROM users WHERE username = :username";
MapSqlParameterSource params = new MapSqlParameterSource("username", username);
jdbcTemplate.query(sql, params, rowMapper);

// CORRECT — Spring Data JPA repository
Optional<User> findByUsername(String username);  // automatically parameterized

// CORRECT — JPA Criteria API
CriteriaBuilder cb = em.getCriteriaBuilder();
CriteriaQuery<User> query = cb.createQuery(User.class);
Root<User> root = query.from(User.class);
query.where(cb.equal(root.get("username"), username));  // safe
```

---

## XML / XXE Prevention

```java
// NEVER — default DocumentBuilderFactory (vulnerable to XXE)
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(inputStream);  // XXE risk

// CORRECT — disable DTD and external entities
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
factory.setXIncludeAware(false);
factory.setExpandEntityReferences(false);
DocumentBuilder builder = factory.newDocumentBuilder();

// CORRECT — use a vetted XML processing library configured for safety
// Consider Jackson XML or JAXB with schema validation as an alternative
```

---

## Deserialization

```java
// NEVER — deserialize untrusted data with Java's native ObjectInputStream
ObjectInputStream ois = new ObjectInputStream(inputStream);
Object obj = ois.readObject();  // deserialization gadget risk — RCE possible

// NEVER — use XStream with untrusted input without strict class allowlist
// NEVER — use SnakeYAML with Yaml.load() on untrusted input

// CORRECT — use JSON (Jackson) for external data exchange
ObjectMapper mapper = new ObjectMapper();
mapper.activateDefaultTyping(
    mapper.getPolymorphicTypeValidator(),
    ObjectMapper.DefaultTyping.NONE  // disable polymorphic typing for untrusted input
);
MyClass obj = mapper.readValue(jsonString, MyClass.class);

// CORRECT — if Java serialization is required, use a deserialization filter
ObjectInputStream ois = new ObjectInputStream(inputStream);
ois.setObjectInputFilter(filterInfo -> {
    Class<?> clazz = filterInfo.serialClass();
    if (clazz != null && !ALLOWLIST.contains(clazz.getName())) {
        return ObjectInputFilter.Status.REJECTED;
    }
    return ObjectInputFilter.Status.ALLOWED;
});
```

---

## Command Injection

```java
// NEVER — Runtime.exec() or ProcessBuilder with shell
Runtime.getRuntime().exec("ls " + userInput);  // command injection risk
new ProcessBuilder("sh", "-c", "ls " + userInput).start();  // injection risk

// CORRECT — argument array, never shell=true
ProcessBuilder pb = new ProcessBuilder("ls", "-la", sanitizedDirectory);
pb.redirectErrorStream(true);
Process process = pb.start();

// CORRECT — prefer Java APIs over shell commands (Files, Paths, etc.)
// Use java.nio.file.Files.list() instead of shelling out to ls
```

---

## Path Traversal

```java
// NEVER — concatenate user input into file paths
File file = new File("/uploads/" + userInput);  // path traversal risk
Path path = Paths.get("/uploads/" + filename);   // path traversal risk

// CORRECT — resolve and validate against base directory
Path baseDir = Paths.get("/uploads").toRealPath();
Path target = baseDir.resolve(filename).normalize();
if (!target.startsWith(baseDir)) {
    throw new SecurityException("Path traversal attempt detected");
}
// Now safe to use target
```

---

## Cryptography: Java Specific

```java
// NEVER — MD5 or SHA-1 for integrity or password hashing
MessageDigest.getInstance("MD5")   // broken
MessageDigest.getInstance("SHA-1") // broken for security use

// NEVER — ECB mode
Cipher.getInstance("AES/ECB/PKCS5Padding")  // no IV, reveals patterns

// CORRECT — AES-GCM
KeyGenerator keyGen = KeyGenerator.getInstance("AES");
keyGen.init(256, new SecureRandom());
SecretKey key = keyGen.generateKey();
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
byte[] iv = new byte[12];
new SecureRandom().nextBytes(iv);
cipher.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(128, iv));

// CORRECT — password hashing with Spring Security BCrypt
PasswordEncoder encoder = new BCryptPasswordEncoder(12);
String hash = encoder.encode(rawPassword);
boolean matches = encoder.matches(rawPassword, hash);

// CORRECT — secure random token generation
byte[] token = new byte[32];
new SecureRandom().nextBytes(token);
String tokenHex = HexFormat.of().formatHex(token);
```

---

## Spring Boot Security Configuration

```java
// CORRECT — Spring Security baseline configuration
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2Login(Customizer.withDefaults())  // use enterprise IdP, never custom auth
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
                .maximumSessions(1)
            )
            .headers(headers -> headers
                .frameOptions(HeadersConfigurer.FrameOptionsConfig::deny)
                .contentTypeOptions(Customizer.withDefaults())
                .httpStrictTransportSecurity(hsts -> hsts.includeSubDomains(true).maxAgeInSeconds(31536000))
            )
            .csrf(Customizer.withDefaults())  // never disable CSRF for stateful apps
            .cors(cors -> cors.configurationSource(corsConfigurationSource()));
        return http.build();
    }

    // NEVER — disabling security for convenience
    // http.csrf().disable()   ← prohibited
    // http.authorizeRequests().anyRequest().permitAll()  ← prohibited
}
```

---

## Logging: Java Specific

```java
// NEVER — log sensitive data
logger.info("User {} logged in with password {}", username, password);  // prohibited
logger.debug("Auth token: {}", token);  // prohibited

// NEVER — log exceptions with full stack trace containing system details to external callers
// Return generic error + correlation ID to caller; full stack trace to server logs only

// CORRECT — structured logging with SLF4J / Logback
private static final Logger logger = LoggerFactory.getLogger(MyService.class);

logger.info("Authentication successful for user={} correlationId={}", username, correlationId);
logger.warn("Authorization failure resource={} user={} correlationId={}", resourceId, username, correlationId);
logger.error("Unexpected error correlationId={}", correlationId, exception);  // exception as last arg = stack trace to log, not caller

// CORRECT — MDC for request correlation
MDC.put("correlationId", UUID.randomUUID().toString());
MDC.put("userId", authenticatedUserId);
try {
    // ... handle request
} finally {
    MDC.clear();
}
```

---

## Dependency Management

```xml
<!-- CORRECT — Maven: pin exact versions, no ranges -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
    <version>3.2.5</version>  <!-- pin exact version, not [3.0,) -->
</dependency>
```

```gradle
// CORRECT — Gradle: exact version pinning
implementation 'org.springframework.boot:spring-boot-starter-security:3.2.5'
// Run: gradle dependencyCheckAnalyze (OWASP Dependency Check plugin)
```

- Run OWASP Dependency Check or Snyk on every build
- Fail the build on Critical CVEs
- Never use `-SNAPSHOT` versions in production builds

---

## SAST Tools for Java

- **SpotBugs + Find Security Bugs plugin**: static analysis for security bugs
- **Semgrep** with Java ruleset: pattern-based security scanning
- **SonarQube**: code quality and security hotspot detection
- **OWASP Dependency Check**: SCA for known CVEs in dependencies

---

## Framework Alignment

| Control Area | OWASP ASVS | NIST SSDF | ISO 27001 |
| --- | --- | --- | --- |
| Secrets management | V2.10 | PW.8.2 | A.8.24 |
| SQL injection prevention | V5.3 | PW.6 | A.8.28 |
| XML/XXE prevention | V5.3 | PW.6 | A.8.28 |
| Deserialization | V1.5, V5.5 | PW.6 | A.8.28 |
| Cryptography | V6 | PW.7 | A.8.24 to 8.25 |
| Authentication (Spring Security) | V2, V3 | N/A | A.5.17 |
| Logging | V7 | RV.1 | A.8.15 to 8.16 |
| Dependency management | V1.14 | PO.5, PW.4 | A.8.8 |
