# Independent re-verification record (covering #1153, #1156, #1159 claims)

**Date:** 2026-07-25
**Worker:** `opus-20260725T102556Z-c46a` (file-drop transport)
**Consumed in:** PR #1161

This is the run's independence-gap closer. It was first routed to the `codex` family (the only family
independent of every opus delivery), which registered a heartbeat but never claimed it and went stale
without serving, so it was re-routed to this worker, which started at 10:25Z and authored none of the
#1153 / #1156 / #1159 work whose claims it re-verifies. Its independence of those CLAIMS is therefore
genuine even though it shares a family with the workers that produced them.

Headline: every load-bearing claim CORROBORATED, including H-01, the one change of the run that merged
without human review. One warning (a register omission, fixed in #1161) and one note refuting the
ORDER's restatement of a claim rather than the corpus (codified in #1161).

---

# Result independent-reverify-run-2: independent re-verification of three claim sets

- **Order:** `independent-reverify-run-2` (kind `qa`, command `verify`, priority 0)
- **Worker:** `opus-20260725T102556Z-c46a` (family `opus`, same-VM file-drop, model `claude-opus-5[1m]`,
  session start 10:25:56Z)
- **Read basis, pinned and read-only:** `grc_library` `6b8c1c8d` and `grc_library_ref` `4a0f2978`,
  both reach-checked (`cat-file -t` printed `commit`). Every corpus and held-source read went through
  `git -C ... show <sha>:<path>` or `git -C ... grep <sha>`. No `checkout`, `switch`, `reset`,
  `stash`, `fetch`, or `worktree` against either shared checkout.
- **Scratch work:** a disposable directory under this worker's own scratchpad
  (`.../scratchpad/reverify2`), used only to extract two tool files for the claim-3 gate runs.
  Nothing was written to the corpus, the reference base, or the exchange root beyond this delivery.

## Identity and independence disclosure

**I am `opus-20260725T102556Z-c46a`**, the worker the order's preamble names. Two notes for the
record, because the order asks for honesty about exactly this:

1. **The order body contains a stale sentence.** After the preamble explains the re-route to `opus`,
   the body still reads "You are family `codex`, independent of every opus delivery in this run."
   That is left over from the original codex routing and is superseded by the preamble. I am family
   `opus`, so the blanket "independent of every opus delivery" premise does not hold for me by
   construction and has to be established per claim set instead. It is, below.
2. **My prior involvement in this run, in full.** This session has served two earlier orders, both
   on TODO 3.113 (worker-id collision): `verify-3113-collision-draft` and
   `redraft-3113-collision-fix`. Neither touches #1153, #1156, or #1159, and neither reads the
   documents or held sources examined here. **I authored none of the work whose claims are
   re-verified below**, so my independence of all three claim sets is genuine, exactly as the
   preamble reasons.

**One methodological tension I could not avoid, disclosed.** The order says not to read the opus
deliveries first, and also requires a bare-token grep "across ALL file types including ... `.working/`".
Those conflict: the `.working/` narration of the #1156 fix (`DONE.md`, `CHANGELOG-detailed.md`,
`improvement-log.md`, `validate-pr/`) contains the corrected strings, so the required grep surfaced
that narration in its output. I did not open any opus delivery as a source, and every verdict below
was formed from the held text or the corpus itself and is cited to that source, not to the narration.

## Verdicts at a glance

| # | Claim | Verdict |
| --- | --- | --- |
| 1a | SP 800-208's actual title | CORROBORATED |
| 1b | Neither fabricated title survives | CORROBORATED AS MADE; the ORDER's restatement of it is refuted (note) |
| 1c | ML-DSA-44 condition is a BAND | CORROBORATED |
| 1d | FIPS 203/204 do not prescribe the AES mapping | CORROBORATED |
| 1e | FIPS 205 in both paired surfaces, agreeing | CORROBORATED |
| 1f | MCP Top 10 Beta disclosed at the control anchor | CORROBORATED; adjacent gap found (warning) |
| 2a | Retention stated as a FLOOR | CORROBORATED |
| 2b | Both ten-year clocks reached | CORROBORATED, tested against all five ten-year provisions |
| 2c | Cited Articles prescribe what is attributed | CORROBORATED on every provision checked; NO error-severity finding |
| 3a | Four gate-44 routes remain open | CORROBORATED, independently constructed and run |
| 3b | Any fifth route | **TWO further routes found, neither tracked (warning)** |

**The most valuable things in this delivery** are the two untracked gate-44 routes (claim 3b), one of
which means a fix to a tracked route would leave its twin open, and the finding that the order's own
paraphrase of claim 1b overstates what the corpus claims.

## Claim set 1: the #1156 citation fixes

### 1a. SP 800-208's title: CORROBORATED

Held title page, verbatim, `grc_library_ref` at `4a0f2978`,
`standards/NIST/NIST-SP-800-208--Stateful-Hash-Based-Signature-Schemes--full-text.md:16-19`:

```text
NIST Special Publication 800-208

Recommendation for Stateful
Hash-Based Signature Schemes
```

(The title wraps across two source lines. The trust line records it as an ACCEPTED STANDARD, US
Government work, public domain, October 2020.)

All three corpus carriers now state that title:

- `security/framework-cryptographic-key-lifecycle.md:126`, `| NIST SP 800-208 | Recommendation for Stateful Hash-Based Signature Schemes | Stateful hash-based signature key management (LMS, HSS, XMSS, XMSS^MT) |`
- `security/policy-encryption-and-key-management.md:213`, `| NIST SP 800-208 | Recommendation for Stateful Hash-Based Signature Schemes |`
- `security/roadmap-post-quantum-cryptography.md:161`, `| NIST SP 800-208 | Recommendation for Stateful Hash-Based Signature Schemes | PQC transition planning |`

and `docs/reference-acquisition-manifest.md:253` agrees.

### 1b. No surviving fabrication: CORROBORATED AS THE CORPUS MAKES IT, and the order's restatement is REFUTED (note)

**As the corpus claims it, the claim holds.** In a TITLE SLOT for SP 800-208 there is no surviving
fabrication: the three carriers above are correct, and the only occurrence of the string "PQC
transition planning" outside `.working/` narration is
`security/roadmap-post-quantum-cryptography.md:161`'s RELEVANCE column, lowercase, beside the
correct title. That is the provenance the #1156 work identified (a column copy), and it is a
legitimate description of the standard's relevance, not a title.

**As the ORDER restates it, the claim is refuted.** The order asks me to verify "that neither
fabricated title ('PQC Transition Planning', 'Post-Quantum Cryptography Readiness') survives
anywhere in the corpus, as a bare-token grep across ALL file types". Taken literally that is false:
"Post-Quantum Cryptography Readiness" survives in at least eight places, because it is the leading
substring of the corpus's OWN document title, "Post-Quantum Cryptography Readiness Roadmap":

- `docs/portal.md:165`, `docs/maturity-scorecard.md:143`
- `compliance/matrix-grc-compliance-alignment.md:152`
- `governance/register-document-index-and-classification.md:264`
- `.web/corpus-link-manifest.md:658` and `:659`
- `dev-security/standard-security-baseline-and-standards-reference.md:58` (lowercase)

None is a title of SP 800-208, so none is a residual fabrication. The corpus scopes its own claim
correctly: `.working/validate-pr/2026-07-25-PR-1158.md:108` records the check as "The fabricated SP
800-208 titles **in a title slot** | none outside `.working/` narration of the fix".

**Finding (note, in the ORDER not the corpus):** a bare-token grep for that phrase returns many
legitimate hits, so an unscoped restatement of the claim invites a false refutation from any verifier
who runs the grep and reads the count. The claim is only checkable as "in a title slot for SP
800-208". I record this because the order asked for a refutation, and the honest answer is that the
refutable version of the claim is the paraphrase rather than the corpus's own wording.

### 1c. The ML-DSA-44 condition is a BAND: CORROBORATED

Corpus, `security/roadmap-post-quantum-cryptography.md:56`:

> ML-DSA-44 (category 2; reduced to category 1 when the approved RBG provides at least 128 but less
> than 192 bits of security, which FIPS 204 permits while requiring at least 128 bits, and
> recommending at least 192)

Held FIPS 204 Section 3.6.1 (Randomness Generation),
`standards/NIST/NIST-FIPS-204--Module-Lattice-Based-Digital-Signature-ML-DSA--full-text.md:1190-1193`:

> For ML-DSA-44, the RBG **should** have a security strength of at least 192 bits and **shall** have
> a security strength of at least 128 bits. If an approved RBG with at least 128 bits of security but
> less than 192 bits of security is used, then the claimed security strength of ML-DSA-44 is reduced
> from category 2 to category 1.

Three-way match, and the distinction the order asks about is present: the corpus states a BAND ("at
least 128 but less than 192"), which is the standard's own condition, not a bare upper bound. The
`shall` / `should` split is rendered correctly as "requiring at least 128 bits, and recommending at
least 192". No finding.

### 1d. FIPS 203 and FIPS 204 do not prescribe the AES mapping: CORROBORATED

Corpus, `security/roadmap-post-quantum-cryptography.md:51`:

> The categories are defined in NIST's original PQC Call for Proposals and are stated in FIPS 203 and
> FIPS 204 as a claim that a parameter set is at least as secure as a generic block cipher with a
> prescribed key size or a generic hash function with a prescribed output length; categories 1, 3,
> and 5 are **conventionally read** against AES-128, AES-192, and AES-256 key search respectively.

Two independent checks against the held text, and both hold:

1. **Neither standard prescribes an AES mapping.** In each of FIPS 203 and FIPS 204 the token "AES"
   occurs **exactly once**, and in both cases it is the Acronyms block:
   FIPS 203 line 605 and FIPS 204 line 745, each reading `AES` followed by
   `Advanced Encryption Standard` and then the next acronym (`CBD` and `API` respectively). So the
   AES-equivalence mapping is correctly attributed away from the standards, to convention.
2. **What the corpus DOES attribute to them, they do state.** FIPS 204:1381,
   "each ML-DSA parameter set is claimed to be at least as secure as a generic block cipher with a
   prescribed key size", and FIPS 203:2614, "block cipher with a prescribed key size or a generic
   hash function with a prescribed output". The corpus paraphrase is faithful, including the
   disjunction.

No finding. This is the most precisely-attributed sentence of the set.

### 1e. FIPS 205 in both paired approved-algorithm surfaces: CORROBORATED

- `security/policy-encryption-and-key-management.md:93`, the "Post-quantum cryptography" row of the
  Section 6 approved-algorithms table: "SLH-DSA (NIST FIPS 205, August 2024) **where a conservative
  hash-only signature assumption is required**".
- `security/framework-cryptographic-key-lifecycle.md:50`, the "Approved algorithms" list: "and
  SLH-DSA (FIPS 205) **where a conservative hash-only signature assumption is required**".

Both surfaces name it, and they AGREE: the qualifying condition is word-for-word identical. The
framework's terser list omits the "NIST" prefix and the "August 2024" date that the policy table
carries, which is a formatting difference between a bullet list and a table cell rather than a
disagreement of substance. No finding.

### 1f. MCP Top 10 Beta disclosure: CORROBORATED at the control anchor, with an adjacent gap

**The control-anchor site discloses it fully.**
`ai/standard-ai-and-agentic-development-security.md:350`, the "Framework anchors" sentence for the
ten MCP-SEC controls:

> These controls align with the OWASP MCP Top 10 (2025, **Beta; a living document whose categories
> may change, so it anchors these controls corroboratively rather than normatively**)

That is the claim as scoped, and it holds, with the normative caveat spelled out.
`docs/reference-acquisition-manifest.md:467` also records "(2025, Beta)" plus "Phase-3 Beta living
document ... beta, so re-check before any normative reliance".

**Finding F1 (warning): the canonical citations register does not record the Beta status.**
`governance/register-canonical-citations.md:231`:

```text
| OWASP MCP Top 10 | 2025 | 2025 | Security risks for Model Context Protocol integrations | - | https://owasp.org/www-project-mcp-top-10/ | 2026-06-30 |
```

No Beta or living-document marker anywhere in the row. This matters for three reasons:

1. That register is the corpus's authoritative citation surface, its stated purpose is citation
   precision, and it drives `tools/lint-standards-currency.py` (named in its own Related Documents).
2. **The register's own convention has a place for exactly this.** Other rows carry publication
   status in the version and published columns: `:259` ISO 16484, "Part 3 at draft (DIS)"; `:159`
   Canada OSFI E-23, "Final published 11 September 2025; effective 1 May 2027"; `:117` ETSI EN 304
   223 records a superseded draft. So this is an omission against convention, not an absence of any
   mechanism.
3. Two other surfaces already record the Beta status, so the corpus disagrees with itself about a
   material property of the publication, and the surface that omits it is the one a reader consults
   for citation precision.

Not a refutation of claim 1f, which is scoped to the control anchor. Severity warning, and cheap:
one cell.

**One borderline case I judged NOT a finding**, recorded so the judgement is visible:
`ai/standard-ai-access-and-agent-permissions.md:108` says "See also the OWASP MCP Top 10 risk
categories (tool poisoning, context contamination, permission escalation)" with no Beta marker. I
read a "see also" cross-reference as not a control anchor, so the claim as scoped is unaffected. A
stricter reader could disagree, since the sentence does lean on the categories by name.

## Claim set 2: the #1153 H-01 retention fix (merged without human review)

The two rows are `governance/register-data-retention-schedule.md:103` (model cards and validation
reports) and `:106` (training data provenance records).

### 2a. Stated as a FLOOR, not a ceiling: CORROBORATED

Both rows carry the same construction in the retention-period column: "Model decommission + 5 years,
or 10 years where either EU AI Act keeping period applies ..., **whichever is longer**", and both
justification cells say so explicitly: `:103` "Composed as a floor rather than a replacement so the
period is never shortened for a long-lived model", and `:106` "Composed as a floor rather than a
replacement". A "whichever is longer" disjunction cannot shorten either input, so the original
defect (a carve-out that would have SHORTENED retention) is structurally closed rather than merely
described as closed. No finding.

### 2b. Both ten-year clocks reached: CORROBORATED, and I tested the framing harder than the claim

Both rows reach both: `:103` states the Article 18(1) system clock at length and then "**The Act has
a SECOND 10-year clock and this row reaches it**", identifying Annex XI, the model anchor, and
Article 54(3)(b); `:106` reaches both by reference to the row above, via Annex IV item 2(d) for the
system side and Annex XI Section 1 point 2(c) for the model side.

**I tried to refute the "second clock" framing by enumerating every ten-year keeping provision in
the Act.** There are five, not two:

| Provision | Duty holder | Anchor | Set kept |
| --- | --- | --- | --- |
| Article 18(1) (line 4146) | provider | SYSTEM placed on market or put into service | Art 11 technical documentation, Art 17 QMS documentation, notified-body changes and decisions, Art 47 DoC |
| Article 22(3)(b) (line 4236) | authorised representative of a high-risk-system provider | SYSTEM | provider contact details, DoC copy, the technical documentation, notified-body certificate |
| Article 23(5) (line 4286) | importer | SYSTEM | notified-body certificate, instructions for use, Art 47 DoC |
| Article 47(1) (line 5168) | provider | SYSTEM | the EU declaration of conformity itself |
| Article 54(3)(b) (line 5462) | authorised representative of a GPAI-model provider | **MODEL** placed on market | Annex XI technical documentation |

**The framing survives.** The row's distinguishing axis is the ANCHOR, which it states directly
("the anchor is the MODEL being placed on the market rather than the system"). On that axis there are
exactly two: four provisions run from the SYSTEM and only Article 54(3)(b) runs from the MODEL. The
row also already names Article 22(3)(b) and Article 23(5) explicitly, treating them as extensions of
the provider duty and as a narrower importer duty respectively, so it is not unaware of them.

Article 47(1) is the only ten-year provision the rows do not cite, and that is correct rather than an
omission: it keeps the declaration of conformity itself, which is not model documentation and is
already inside the Article 18(1)(e) set these rows do cite. No finding.

### 2c. Every cited Article prescribes what is attributed to it: CORROBORATED, no error-severity finding

The order makes this the error-severity axis, so I checked each attribution against the held text of
`legislation/EU/EU-AI-Act-Regulation-2024-1689--full-text.md` at `4a0f2978`. Every one holds.

**Article 18(1)** (line 4146), verbatim:

> The provider shall, for a period ending 10 years after the high-risk AI system has been placed on
> the market or put into service, keep at the disposal of the national competent authorities:
> (a) the technical documentation referred to in Article 11; (b) the documentation concerning the
> quality management system referred to in Article 17; (c) the documentation concerning the changes
> approved by notified bodies, where applicable; (d) the decisions and other documents issued by the
> notified bodies, where applicable; (e) the EU declaration of conformity referred to in Article 47.

The row's summary matches item for item, including the 10-year period, the dual anchor ("placed on
the market or put into service"), and "at the disposal of national competent authorities".

**Article 54(3)(b)** (line 5461), verbatim, under the heading "Article 54 / Authorised
representatives of providers of general-purpose AI models":

> (b) keep a copy of the technical documentation specified in Annex XI at the disposal of the AI
> Office and national competent authorities, for a period of 10 years after the general-purpose AI
> model has been placed on the market, and the contact details of the provider that appointed the
> authorised representative;

The row's reading is exact, **including its caveat**, which is the most legally careful sentence in
either row: "Article 54(3)(b) binds the REPRESENTATIVE and speaks of its own copy, so it does not by
itself stop a provider destroying the master." The text says "keep a copy", and the duty is a
mandated task of the representative, so the caveat is right.

**Article 54(2)** (line 5452): "The provider shall enable its authorised representative to perform
the tasks specified in the mandate received from the provider." Matches the row's use of it as
corroboration, and the row correctly flags `shall`.

**Article 54(3)(c)**: "provide the AI Office, upon a reasoned request, with all the information and
documentation, including that referred to in point (b)". Matches.

**Article 53(1)(a)** (line 5397), verbatim: "draw up and keep up-to-date the technical documentation
of the model, including its training and testing process and the results of its evaluation, which
shall contain, at a minimum, the information set out in Annex XI". Two attributions confirmed: the
duty exists, and **no period is stated in it**, exactly as the row says. Annex XI's own heading
("Technical documentation referred to in Article 53(1), point (a)") independently confirms the
pairing. The row writes "KEEP UP TO DATE" where the source hyphenates "keep up-to-date", which is
not a substantive difference.

**Annex IV item 2(g)**: "the validation and testing procedures used, including information about the
validation and testing data used and ... **test logs and all test reports**". The row cites 2(g) for
"test logs and test reports". Correct letter, correct content.

**Annex IV item 2(d)**: "where relevant, the data requirements in terms of datasheets describing the
training methodologies and ... their **provenance**, scope and main characteristics; how the data was
obtained and selected; labelling procedures". The row cites 2(d) for provenance of the data sets.
Correct letter, correct content.

**Annex XI Section 1, point 2(c)**, verbatim: "information on the data used for training, testing and
validation, where applicable, including the type and **provenance** of data and curation
methodologies (e.g. cleaning, filtering, etc.), the number of data points, their scope and main
characteristics". The row's paraphrase is faithful.

**And the row's disambiguation is correct**, which is the single most falsifiable detail in claim set
2. `:106` says "the point number matters: Section 1 contains two items lettered (c), and point 1(c)
is the unrelated date-of-release item". Verified: Annex XI Section 1 point 1(c) reads "the date of
release and methods of distribution", and point 2(c) is the data-provenance item. Two items lettered
(c), exactly as claimed.

**Recital 89**: the row says "the Act's sole use of the term is the non-binding recital 89". The
token "model card" occurs **exactly once** in the entire Act text, inside recital **(89)**, reading
"Developers of free and open-source tools ... should be **encouraged** to implement widely adopted
documentation practices, such as **model cards** and data sheets". Sole use confirmed by count,
recital number confirmed by reading the numbered recital markers around it, and non-binding confirmed
by "should be encouraged". Exact on all three points.

**Article 23(5)**, the narrowness claim: "Importers shall keep, for a period of 10 years ..., a copy
of the certificate issued by the notified body, where applicable, of the instructions for use, and of
the EU declaration of conformity referred to in Article 47." The technical documentation is indeed
absent from that keeping set (Article 23(6) separately requires importers to ensure that the
technical documentation can be made available on request, which is a different duty). The row's
"narrower and excludes the technical documentation" is correct.

**Result: no error-severity finding in claim set 2.** For the run's highest-risk change, merged
without human review, every attributed value is stated by the provision cited for it, and the two
places where the drafting could most easily have gone wrong (the Annex XI double-(c) and the
representative-versus-provider distinction in Article 54(3)(b)) are both handled correctly.

## Claim set 3: the four gate-44 fail-open routes

TODO 3.115 (`TODO.md:249-251`) records the four routes as (a) YAML front matter, (b) a table cell of
pure metadata, (c) a link target containing a literal `)` "which `LINK_TARGET_RE`'s `[^)]*` stops
short of", and (d) an HTML attribute value appearing after a `>`.

### 3a. All four are real: CORROBORATED by construction and by running the gate

I extracted `tools/lint-paired-skill-step-parity.py` and `tools/lint_common.py` at `6b8c1c8d` into
my scratchpad and ran the gate's own `content_tokens` over a case I built for each route, using one
distinctive marker token. A route is OPEN when the marker survives stripping, because a surviving
token can satisfy the subsection check by itself. I ran eight CONTROLS alongside, one per route the
gate already closes, so that a "survives" result cannot be an artefact of my harness.

```text
case                                                     result
----------------------------------------------------------------
(a) YAML front matter                           SURVIVES (open)
(b) table cell of pure metadata                 SURVIVES (open)
(c) link target with a literal )                SURVIVES (open)
(c') same, absolute URL                         SURVIVES (open)
(d) HTML attr value after a >                   SURVIVES (open)
(e5) IMAGE_RE, same [^)]* defect                SURVIVES (open)
(f5) INDENTED code block                        SURVIVES (open)
CONTROL fenced code                                    stripped
CONTROL html comment                                   stripped
CONTROL plain link target                              stripped
CONTROL image, no paren                                stripped
CONTROL ref-link label                                 stripped
CONTROL ref definition                                 stripped
CONTROL url                                            stripped
CONTROL simple html tag attr                           stripped
```

All four claimed routes are real, and all eight controls behave as the closed routes should. The
mechanism in each case:

- **(a)** nothing in `content_tokens` strips YAML front matter; the delimiters are not fences that
  `iter_non_code_lines` toggles on, so `title: <token>` is read as prose.
- **(b)** no table-aware stripping exists, so a metadata-only cell contributes its tokens.
- **(c)** `LINK_TARGET_RE = re.compile(r"\]\([^)]*\)")` (`:233`) stops at the FIRST `)`, so for
  `[the doc](../a(b)/<token>.md)` it consumes `](../a(b)` and leaves `/<token>.md)` behind. I add
  **(c')** as a sub-case worth recording: it also survives with an absolute `https://` target, because
  `LINK_TARGET_RE` runs BEFORE `URL_RE` (`:281` then `:285`) and has already eaten the scheme by the
  time `URL_RE` looks, so the URL strip cannot recover the tail.
- **(d)** `HTML_TAG_RE = re.compile(r"<[^>]+>")` (`:245`) matches up to the first `>`, so for
  `<div title="a>b <token>">` it consumes `<div title="a>` and leaves `b <token>">`.

### 3b. A fifth route: TWO found, and neither is tracked anywhere

**Finding F2 (warning): `IMAGE_RE` carries the identical `[^)]*` truncation defect as
`LINK_TARGET_RE`, and only the latter is tracked.**

`IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")` (`tools/lint-paired-skill-step-parity.py:232`) has
the same `\([^)]*\)` tail as `LINK_TARGET_RE` on the next line. So `![alt](../a(b)/<token>.png)`
leaves `/<token>.png)` behind, exactly as route (c) does, while my control confirms that an ordinary
image IS stripped whole. TODO 3.115 route (c) names only the link-target pattern.

Why this matters more than a count: **a fix to route (c) that patches `LINK_TARGET_RE` alone will
leave its twin open**, and the fix will look complete because the tracked case will pass. This is the
same defect class in a second pattern, which is precisely the sibling-check that the corpus's own
regression discipline exists to catch. It is also cheap to fold in, since both patterns need the same
correction.

**Finding F3 (warning): an INDENTED code block is not stripped, and no backlog item records it.**

`iter_non_code_lines` is fence-only, so a four-space-indented code block is read as prose and its
tokens count as content. The gate's own docstring states the caveat plainly at `:256-258`, "fenced
code (via ``iter_non_code_lines``, whose contract is fence-only: an INDENTED code block is not
stripped, so do not rely on it being)". A known caveat is not a tracker, though, and this is a
genuine fail-open route by the same test as the other six: an identifier inside an indented code
block can satisfy a subsection match on its own.

**Both are untracked.** Verified against `TODO.md` at `6b8c1c8d`, unpiped with the return code
captured (see the process note below):

```text
grep -n -i "indented" TODO.md   ->  rc=1 (absent)
grep -n "IMAGE_RE"    TODO.md   ->  rc=1 (absent)
grep -n -i "fence"    TODO.md   ->  rc=0, two hits, both unrelated (:138 corpus diagram policy,
                                    :305 the gate-mutation "unbalanced-fence" probe class)
```

So the count in TODO 3.115 should be six rather than four. This is not a refutation of the claim as
written (the four it names are all real), but it is a completeness gap of the same kind the item was
created to fix, and TODO 3.115 itself anticipates it: "Do NOT assume the class is exhausted when
these four close ... treat each round as sampling an open class rather than draining a closed one."
The per-round base rate it records (2, then 5, then 1, then 1) now gains a further 2 from this round.

## Process note worth recording

While checking the two absences above I first ran `grep ... | head -5` and read `$?`, which is
`head`'s status rather than `grep`'s. I caught it before relying on the result and redid both checks
unpiped with `rc` captured immediately, which is what the transcript above shows.
`.working/improvement-log.md:61` tracks this exact class at five occurrences with the standing
correction "capture `rc` into a variable immediately after the command and NEVER pipe a verification
into a truncating filter". This would have been a sixth, and in the same shape as the fourth (a
masked absence proving nothing). The standing correction works; it needs applying at the moment of
writing the command, not at review.

## What I did not check

- I did not re-verify the other #1156 items (the OWASP Agentic date, the ETSI superlative, the ASI
  crosswalk name) or the TRAIGA refutation, none of which this order lists.
- For claim 2 I verified the provisions the two rows CITE. I did not audit the Act for a provision
  that ought to be cited and is not, beyond the ten-year enumeration in 2b.
- For claim 3 I exercised `content_tokens`, which is where all seven routes live. I did not run the
  full gate over the real corpus, so I am not asserting that any live document currently exploits a
  route; the claim under test is that the routes exist, and that is what I tested.
- I read no opus delivery as a source. Where the required all-file-types grep surfaced `.working/`
  narration, I treated it as out of scope and cited only held text or corpus documents.

## Token spend

Approximately 640,000 input tokens and approximately 62,000 output tokens for this order (this
session's third). The bulk is the held EU AI Act text (Article 18, Articles 22 to 23, Articles 47 and
53 to 54, Annex IV, Annex XI, recital 89), the held FIPS 203, FIPS 204, and SP 800-208 extracts, the
corpus retention and PQC documents, the gate-44 tool plus `lint_common`, and the constructed gate
runs. Best-effort estimate: the harness does not expose an exact per-order counter to the worker
session. Session usage is now substantial, so I will check my remaining capacity before claiming
another order.
