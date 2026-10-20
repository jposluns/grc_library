#!/usr/bin/env python3
"""D15: alignment-citation register check (PR-time, diff-scoped, ADVISORY).

THE CLASS. The canonical-citations register
(``governance/register-canonical-citations.md``) is the positive list of the
standards and regulations whose currency the library tracks; its Maintenance
section asks that a standard is added "before the citing PR merges". Nothing
enforced that: a PR could add a framework-alignment row, or name an EU
instrument in prose, for an instrument with no register row, and the register
(and so the standards-currency gate that reads it) would never learn of it.
The 2026-10-04 PR #2697 is the observed case: it added Directive (EU)
2022/2557 and Recommendation 2003/361/EC in prose, neither of which has a row.

WHAT IT CHECKS. Only lines the PR adds or changes (``git diff`` of the PR head
against its merge base), in Markdown files under the audited domain
directories (``lint_common.AUDITED_DOMAIN_DIRS``; gate 52 forbids a hardcoded
list), minus gate 6's exempt files:

1. **List-form alignment tables**: a table whose first header cell means "each
   row names one framework or standard" (``Framework``, ``Framework /
   Standard``, ``Regulation`` and the other headers in ``LIST_HEADERS``). The
   first cell of each added row is a citation.
2. **Matrix-header alignment tables**: a table under a framework-alignment or
   crosswalk heading whose header row names one framework per column. When the
   PR adds the header row, each header cell after the first is a citation.
3. **Free-text citation-list columns** (``Regulatory``, ``Legal / Regulatory``,
   ``Other`` and the rest of ``FREE_TEXT_HEADERS``) of either table form: each
   ``;`` or ``,`` separated segment of an added cell is a citation once its
   provision suffix (``Art. 32``, ``§3.1``) is removed.
4. **EU/EC instrument numbers** anywhere on an added non-code line
   (``Directive (EU) 2022/2557``, ``Recommendation 2003/361/EC``,
   ``Regulation (EU) No 910/2014``), compared by number against the numbers in
   the register's Standard ID, Current version and Superseded versions cells.

PROVISION TAILS (3b378). A provision tail (``PROVISION_TAIL``: ``Art. 32``, ``Annex I``,
``: High Risk``, ``Ch 1``, ``Chapter IX``) is removed only from its first match outside
parentheses (``strip_provision``), so ``EU AI Act Chapter IX`` is the EU AI Act and
``California CCPA ADMT and risk-assessment regulations (11 CCR Div 6 Ch 1 Arts 10-11)`` keeps
its parenthetical instead of ending at ``(11 CCR Div 6``. ``Ch`` and ``Chapter`` count only
before a whole numeral token, a capital Roman numeral of I, V, X, L and C or a number, so
``Chapter IX`` and ``Chapter L`` are tails and ``Chapter Implementation Guide``, ``Widget Act
Chapter Values`` and ``Chapter XYZ Rules`` keep their words. The text after a parenthetical
(``Resolver.paren_tail_ok``) is cut the same way. A segment that begins with a jurisdiction
and a colon (``JURISDICTION_LABEL``: the jurisdictions that begin a register Standard ID, as
the register writes them) names the instrument after the colon: ``Canada: TBS Directive on
Automated Decision-Making`` is the citation ``TBS Directive on Automated Decision-Making`` with
the full form ``Canada TBS Directive on Automated Decision-Making``, where before the colon was
read as a provision tail and left the not-citable ``Canada``. Any other label before a colon
is still read as a provision tail (``NIST AI RMF 1.0: Govern function`` is the NIST AI RMF).
When that label is not registered itself and is either an agency label (``agency_labels`` in
the alias file: ``CBP``, ``FINTRAC``, ``FMCSA``) or not a citation on its own
(``not_citable``: a publisher name such as ``NIST``, a placeholder, or descriptive text), the
text after the colon is resolved instead (``Resolver.after_label``), and when it is
unregistered the finding is the full form, the label and the text after the colon (``FMCSA:
Electronic Logging Devices (ELD)``), not the label alone. The two kinds differ when nothing
after the colon is a citation: an agency label is still reported by its full form (``CBP:
Unknown Programme``), and so is a bare agency label in any case or shape (``CBP``, ``cbp``),
while a not-citable label gives no finding (``NIST: Govern function``, ``Other: N/A``,
``Security management process: risk analysis``). A label may not be both an agency label and a
``not_citable.exact`` entry; ``load_aliases`` refuses the overlap. A registered label
(``Switzerland nFADP: Federal Act on Data Protection``, ``Cloud Controls Matrix: CCM v4
Implementation Guidelines``) never goes through ``after_label``, whatever its shape. A label
registered only as a series stem (the series rule below) counts too: with today's register
``ISO``, ``IEC``, ``IEEE`` and ``ISO/IEC`` are series stems (of ``ISO 31000``, ``IEC
62443-1-1``, ``IEEE 2883`` and ``ISO/IEC 27001``), so ``ISO: Unknown Act 2020`` keeps its tail
and gives no finding, while ``NIST``, ``CSA`` and ``OWASP`` are the series stem of no Standard
ID and ``NIST: Unknown Act 2020`` is reported as the full form. This asymmetry is a known
residual, kept as it is. A generic prose label in a free-text cell is not a
citation on its own, so ``Note: Unknown Act 2020`` is reported with its prefix, as the full
form.

HOW A CITATION RESOLVES. Gate 6 (``tools/lint-standards-currency.py`` and its
pack engine) owns the register parser and the identity normalization; this
check imports both rather than re-implementing them, so the two tools read the
same rows and the same identities. A citation inside gate 6's grammar (ISO/IEC,
NIST, IEEE, ETSI/CEN and the named frameworks) is reported only when gate 6's
own ``resolve`` returns ``UNREGISTERED``; a NONCANONICAL or AMBIGUOUS spelling
has a nearby row and is gate 6's to report, not this check's. Any other
citation is registered when its normalized identity, after a trailing edition
or version is removed, matches a register Standard ID exactly, through a curated
alias or umbrella pattern (``tools/alignment-register-aliases.json``), as a
whole-word suffix of a Standard ID (``GDPR`` for ``EU GDPR``, ``Law 25`` for
``Quebec Law 25``), through an acronym the citation carries in parentheses when
the text after the parenthetical is acceptable and either nothing precedes it or
the name before it names the acronym's own row by that row's words (the row-word
rule below, so ``Medical Device Regulation (MDR) 2017/745`` is registered through
the EU MDR row and ``Unknown Widget Standard (GDPR)`` and ``Medical Device
Regulation (MDR) Unregistered Act`` are not), or as a series prefix of a Standard
ID (``IEC 62443`` for the ``IEC 62443-*`` part rows). The series and suffix
acceptance is this check's addition to gate 6: it can only make D15 report less
than gate 6 would for the same text, never more.

THE ROW-WORD RULE (3b374). A parenthetical's text names register rows through the
same lookups (exact, curated alias or umbrella, whole-word suffix, series stem,
edition: ``(GDPR)`` names the EU GDPR and UK GDPR rows). It stands for the
citation only for a row after which the TEXT AFTER IT is acceptable. That text is
read from the citation before its provision tail was removed, so the whole tail
is judged: once that row's own instrument numbers are removed (those in its
Standard ID, its Current version cell, the title part of its Topic cell, or a
curated alias key targeting it; not a Superseded versions number, which names an
earlier instrument), with any designation of one and an optional ``EU`` before
it (``TAIL_DESIGNATION``: ``Regulation (EU) 2016/679``, ``EU Regulation
2017/745``), it is only provision references (``PROVISION_REF``: a provision
word such as ``Art.``, ``Annex`` or ``Recital`` with its numbers, a Roman
numeral in capitals only, and after a connector a bare sub-point such as
``(b)``; a sub-point (``SUBPOINT``) is a lowercase letter or two, one uppercase
letter, a Roman numeral of up to six letters all lowercase or all capitals, or
one to three digits with an optional letter of either case, and only sub-points
chain, as in ``10(1)(a)``, ``(b)(ii)``, ``164.308(a)(1)(ii)(A)``,
``59.1-577(B)(1)``, ``7(IV)`` and ``10(2A)``), dates, editions, punctuation,
``&`` and ``and`` or ``or``
(``(CCM) v4.1``, ``(MDR) 2017/745``, ``(MDR) Annex I``, ``(MDR) Art. 10
and Annex I``, ``(MDR) Article 10 & Annex I``, ``(MDR) Art. 10(1)(a) and
(b)``, ``EU General Data Protection Regulation (GDPR): Regulation (EU)
2016/679``, ``Medical Device Regulation (MDR): EU Regulation 2017/745``); or its
text up to any provision tail follows the parenthetical to make a name of the
same row, the rest being such a tail (``(HIPAA) Security Rule`` through the
``HIPAA Security Rule`` umbrella; ``(CCPA) Regulations`` names the CCPA
Regulations row, not the CCPA row ``(CCPA)`` names). ``(MDR) Unregistered
Act``, ``(MDR) 2017/999``, ``(MDR) Annex I 2017/999``, ``(MDR) Annex civic``,
``(MDR): Unregistered Act``, ``(MDR): Regulation (EU) 2017/999``, ``(MDR): EU
Regulation 2017/999``, ``(MDR) Art. 10(1)(a) and (Fake)``, ``(MDR) Art.
10(1)(a) and (b)(Fake)``, ``(MDR) Art. 10(1)(a) and (b)(Act)``, ``(MDR) Art.
10(Fake)`` and ``(HIPAA) Security Rule: Unregistered Act`` are not acceptable.
The designation's kind word is not compared with the row's, so ``(GDPR):
Decision 2016/679`` is acceptable. When a name precedes it, that name, with or
without a trailing edition, must also name the row by the ROW'S WORDS. The
name's words are case-folded with accents removed, a possessive ``'s`` is
removed (``EU's``), a plural is read as its singular
(``Devices`` as ``device``, on both sides), ``European`` is read as ``EU`` for a
row whose Standard ID carries ``EU`` (that ``EU`` marks the instrument as the
European Union's), the row's own instrument numbers are dropped, another
instrument number is kept as one word no row carries (``2019/1937`` is not read
as two years), four-digit years from 1900 to 2099 outside instrument numbers are
dropped, and the function words of ``NAME_FUNCTION_WORDS`` (``of``, ``and``,
``the`` ...) need not be row words and give no initials. Then (a) every other
word is a word of the row's Standard ID, at least one is not a family token, and
they include every Standard ID word the parenthetical does not carry (function
words, instrument numbers and years aside: ``UK (UK GDPR)``; ``NIST (CSF)`` is
not, since ``nist`` names a family; ``Working Party Guidelines (WP248 rev.01)``
and ``Anonymisation Techniques (WP216)`` are not, since the long Article 29
Working Party Standard IDs carry more words); or (b) the name carries one of the
row's own instrument numbers and every other word is a row word (of the Standard
ID, of the title part of the Topic cell, or of a curated alias key targeting the
row: ``Regulation (EU) 2016/679 (GDPR)``, ``EU Regulation 2016/679 (GDPR)``); or
(c) every other word is a row word or belongs to a run of consecutive other
words with no function word between them (a function word breaks a run and
gives it no letter) whose initials spell an acronym word of the Standard ID
other than one the parenthetical carries (``Cloud Security Alliance`` for the
``CSA`` of ``CSA CCM`` before ``(CCM)``; ``Consumer Safety and`` spells no
``CSA``, so ``Consumer Safety and Cloud Matrix (CCM)`` is reported like
``Consumer Safety Cloud Matrix (CCM)``, and neither do ``Cloud Security and
Alliance`` and ``Cloud Security for Alliance``, so ``Cloud Security and Alliance
Cloud Controls Matrix (CCM)`` is reported too; ``Global Data Protection
Rules (GDPR)`` is not spelled out from the ``GDPR`` it carries), at least one row
word stands outside such runs (``Cloud Security Alliance (STAR)`` is only the
run), and the initials of the other words, in order and a repeated word counted
once, give all but at most one letter, and at least two, of an acronym word of
the parenthetical (``Data Protection Regulation`` gives ``DPR`` of ``GDPR``;
``Regulation`` gives only ``R``; ``Medical Device Regulation`` gives only ``DR``
of ``IVDR``; ``Trust and Risk`` gives only ``TR`` of ``STAR``, since ``and``
gives no letter; ``Cloud Cloud (CCM)`` gives only ``C``). The title part of a
Topic cell is its text before a parenthetical, a ``;``, a sentence end, or a
``,`` or ``:`` followed by a lowercase word (``topic_title``), so UK GDPR's
words are those of ``UK General Data Protection Regulation``, not of the
description of the retained law after it. So ``EU General Data Protection
Regulation (GDPR)``, ``EU Medical Devices Regulation (MDR)``, ``Health
Insurance Portability and Accountability Act of 1996 (HIPAA)``, ``European
Medical Device Regulation (MDR)``, ``CSA Security Trust Assurance and Risk
(STAR)`` and ``Cloud Security Alliance Cloud Controls Matrix (CCM)`` register,
and ``EU In Vitro Diagnostic Medical Devices Regulation (IVDR)`` does through
the curated alias ``In Vitro Diagnostic Medical Devices Regulation`` (the
instrument's own title), while ``Unregistered Framework (HIPAA)``,
``Regulation (GDPR)``, ``Medical Device Regulation (IVDR)``, ``Retained (GDPR)``
and ``Consumer Safety Act (STAR)`` do not. A name that is itself a Standard ID,
alias or umbrella match registers the citation without the parenthetical, so the
rule decides only names that are not; an umbrella match is not taken as the
row's own name (``HIPAA Privacy Rule`` is not made of HIPAA row words), which
changes nothing since such a name registers on its own. What it still lets
through: a name of row words that leaves out one letter of the acronym
(``Medical Regulation (MDR)``, ``Controls Matrix (CCM)``, ``Regulation of
Medical Devices (MDR)``, and so ``Cloud and Matrix (CCM)`` and ``Medical and
Regulation (MDR)``, whose ``and`` gives no letter); a name of non-family Standard
ID words that covers the Standard ID beside the parenthetical (``EU (GDPR)``); a
name of row words with one of the row's instrument numbers, whatever its
initials (``Regulation 2017/745 (MDR)``); words whose initials spell another
acronym of the Standard ID beside row words (``Cyber Security Agency Cloud
Controls Matrix (CCM)``, ``Consumer Safety Act Trust Assurance Risk (STAR)``,
through the ``CSA`` of the Standard ID); and a parenthesised word of up to six
Roman numeral letters all lowercase or all capitals after a provision number,
read as a sub-point (``(MDR) Art. 10(civic)``, ``(MDR) Art. 10(MIX)``). A
name of an Article 29 Working Party row's descriptive Topic words
(``Determining Whether Processing (WP248 rev.01)``) or of a few words of its
long Standard ID (``Party (WP248 rev.01)``) is reported; ``Article (WP248
rev.01)`` is not checked at all, since its leading ``Article`` is read as a
provision tail and the segment is stripped to nothing.
What it still reports although the instrument is the row's: a name with a word
its row lacks (``European Union Medical Device Regulation (MDR)``: ``union``;
``European Health Insurance Portability and Accountability Act (HIPAA)``, since
``European`` is read as ``EU`` only for an EU row), a name whose initials miss
two or more letters of the acronym (``Protection Regulation (GDPR)``), a name
whose words spell an acronym of the Standard ID only across function words
(``National Institute of Standards and Technology Cybersecurity Framework
(CSF)``: ``of`` and ``and`` break the run, so ``National Institute of Standards
and Technology`` spells no ``NIST``), a short title that leaves out words of a
long Article 29 Working Party Standard ID (``Guidelines on Data Protection
Officers (WP243)``, ``Working Party Guidelines on Data Protection Impact
Assessment (WP248 rev.01)``, ``Working Party Opinion on Anonymisation Techniques
(WP216)``), a name carrying an instrument number the register does not record
for the row (``Regulation 2016/679 (UK GDPR)``: the UK GDPR row records no
number), and a parenthetical followed by other text, including a title after a
provision and a provision this grammar does not read (``Medical Device
Regulation (MDR) as amended``, ``Medical Device Regulation (MDR) Art. 10:
General obligations``, ``CSA Security Trust Assurance and Risk (STAR) Level
2``, ``(MDR) Annex XIV Part A``, ``(MDR) Annex I GSPR 17``; an edition number
with no ``v``, ``Version`` or ``Rev`` before it: ``(CSF) 2.0``, while ``(CSF)
v2.0`` is acceptable; a parenthesised word of three or more lowercase letters
that are not all Roman numeral letters: ``(MDR) Art. 10(1)(aaa)``; a Code of
Federal Regulations reference is not read, since its title number could not be
checked against the row: ``Health Insurance Portability and Accountability Act
(HIPAA): 45 CFR 164.312``, ``(HIPAA) 45 CFR Part 164``; nor is the row's own
instrument number after a bare ``EU`` with no designation kind word: ``(MDR):
EU 2017/745``).

A citation whose provision suffix was removed keeps its full form for the exact
lookups (a Standard ID or curated alias, with or without a trailing edition or a
terminal parenthetical, or an umbrella pattern): ``UK ICO, Employment practices
and data protection: Monitoring workers (June 2024)`` is registered by an alias
or row keyed on that full title, so an alias need not be keyed on the series
name before the colon (which would cover every title in the series). A
trailing edition or year is removed from the full form first, never a
parenthetical (``T (DRAFT) v2`` becomes ``T (DRAFT)``). A parenthetical that
is then terminal (nothing but whitespace or punctuation after it) is dropped
only on an allowlist: every item in it is a date, an edition or version
(``(June 2024)``, ``(2019, updated 2024)``, ``(v2.0)``; a month is a full or
standard abbreviated month name, so ``(Decision 2024)`` is not a date), a WP
number or EDPB-style designator that the name's own register row carries
(``(WP 248)`` after a name of the WP248 row, not after any other name), or an
acronym word of three or more capitals registered as the acronym of the name
before it: it names that name's register row itself as a Standard ID or curated
alias key (not through an umbrella pattern, which may match a whole family), or
it is an acronym word of that row's Standard ID (``CSA AI Controls Matrix
(AICM)``, through the ``CSA AICM`` row). So ``... Monitoring workers (June 2024)
Unknown Act``, ``(Unknown Act)``, ``(UK)``, ``(USA)``, ``(RETIRED)``, ``(DRAFT)
v2``, ``(DRAFT), 2024``, ``(N/A)``, ``(RFC 9457)``, ``(WP 999)``, ``(HIPAA)``
after a name that is not HIPAA's and ``(Novel 2024)`` are not registered by a
full-title alias. Otherwise the stripped form resolves as
before, and a warning names the stripped form. A segment that begins with the
exact words ``Article 29 Working Party`` (that spelling and case, after leading
whitespace, optionally followed by a colon) keeps them: they name the issuing
body, not a provision, so the provision rule applies only to the text after
them, and the citation is registered when a row carries its WP number or
Opinion designator. The full form is matched on its WP numbers only when it
carries at least one, every one is registered, and nothing but WP numbers,
dates and editions follows the last one (``(WP 248) Decision 2017`` is text
after it), so ``Article 29 Working Party
Guidelines on DPIA under Article 35 (WP 248)`` matches the WP248 row although
its stripped form ends at ``under``, while ``... (WP 248, WP 999)``, ``... (WP
248) and Article 36`` and ``... (replaced by EDPB Guidelines 07/2020)`` do not.
The same WP-number rule decides a citation with no provision tail (3b374), so
``Article 29 Working Party Guidelines on DPIA (WP 248, WP 999)`` and ``... (WP
248) Decision 2017`` are not registered either; such a citation that carries no
WP number is still matched on its other designators (``Opinion 05/2014``).
Designators are matched within their issuing body: each register row's
designators are recorded with the body its Standard ID names (``EDPB ...``
rows; ``Article 29 Working Party``, ``WP29`` and ``WPnnn`` rows), a citation's
body is ``Article 29 Working Party`` at its start, or an EDPB name (``EDPB``,
``EU EDPB``, ``European Data Protection Board`` at its start, or an ``(EDPB)``
suffix), and a WP number is an Article 29 Working Party designator only. So an
EDPB ``Guidelines 07/2020`` row does not register ``Article 29 Working Party
Guidelines 07/2020``, ``EU Unknown Act (WP 248)`` and ``EDPB Guidelines on DPIA
(WP 248)`` are not registered by the WP248 row, and a name with no issuer is not
matched on its designators (none of these rules changed a whole-corpus finding
on 2026-10-17). The
exception is anchored to the segment start because both corpus uses
(2026-10-17) begin a cell (``security/policy-byod.md:168``,
``privacy/standard-pseudonymization-and-anonymization.md:150``), while after
another citation (``GDPR Article 29 Working Party guidance``) the words follow
the instrument actually cited, which then resolves alone as it did before
3b367. The bare body name is not a citation (``not_citable``).

WHAT IS NOT A FINDING. The exclusion policy
(``tools/alignment-register-exclusions.json``) encodes the maintainer decision
of 2026-10-16 ("Tracked only"): the register covers standards and regulations
whose currency is tracked, so RFCs, vendor guidance and books are not expected
in it. Each policy pattern or entry carries its class and its reason, and the
policy file is validated on load. Generic placeholders (``N/A``, ``Internal``,
``sectoral laws``), bare publisher names (``NIST``, ``OWASP``) and segments
with no citation shape (no acronym or digit, and no instrument word in a
multiword name) are not citations (the ``not_citable`` block of the alias file).

POSTURE. ADVISORY, the D8 precedent: it prints a ``D15 WARN`` line per
unregistered citation and, once its modules load, ALWAYS exits 0. It is wired into the PR-time runner
and the ``pull_request`` job of ``quality.yml`` only, never into
``tools/run_all_audits.sh``: the corpus-gate bar requires near-zero false
positives, and that runner hides a passing gate's warnings. An absent register
where D15 reads it (an adopter may drop it) is a NOTE and a no-op, and so is a
missing merge base or a failed ``git diff`` (fail-open, the guard-malfunction
stance). An unreadable policy file is a NOTE and a no-op for the main check; the
sibling probe can still run then (see SIBLING PROBE below).

RESIDUE (what D15 does NOT establish). It is delta-only, so a citation that is
already on main is out of scope (gate 6's report mode inventories those for its
grammar families). It cannot see a citation outside the four surfaces above (an
instrument named in prose without a number, a citation in a table it does not
recognize), a citation the alias or suffix rules accept loosely (``AI Act``
resolves to any registered AI Act), or an EU number that appears only in
another row's Current version cell (the EN 54 row's Construction Products
Regulation (EU) 305/2011 counts as registered). Only the spelled-out,
segment-initial ``Article 29 Working Party`` (the one form the corpus used on
2026-10-17) is exempt from provision stripping: ``Art. 29 Working Party``,
``Art 29 Working Party``, ``Articles 29 Working Party``, ``Article 29 WP``,
``Article 29 Data Protection Working Party`` and ``Article 29`` before a
differently cased body name (``Article 29 working party Opinion 2/2017``;
neither rule uses ``re.I``) at the start of a segment are still stripped to
nothing and not checked. The full form gets only the exact lookups and the
Article 29 Working Party WP-number match, not the suffix, series or comma-list
rules, nor the stripped form's parenthesised-acronym rule. The stripped form's
parenthesised acronym registers only by the row-word rule, so a name using a
word its row does not carry warns although it names the same instrument
(``European Union Medical Device Regulation (MDR)``), and so do a name whose
initials miss two letters of the acronym and a parenthetical followed by text
that is not only provision references, dates, editions and the row's own
numbers and designations, nor a name of the row with the parenthetical; on 2026-10-17 the rule
changed no whole-corpus D15 status from main (9e0554e8). Outside D15's surfaces
it no longer registers prose fragments that main's any-parenthetical rule did
(``Higher tier (GDPR)``, ``Managed Detection and Response (MDR)``). An Article 29 Working Party citation with a WP number and title text
after it (``Article 29 Working Party WP248 Guidelines on DPIA``) is no longer
registered by that number (none in the corpus on 2026-10-17). A free-text cell is
split on ``,`` before the full-form lookup, so a full-title alias or row whose
name contains a comma (``UK ICO, Employment practices ...``) matches only in a
list-form row or a matrix header; in a free-text cell its pieces resolve
separately. The stripped form's own lookup still drops everything from its
first ``(``, so with an alias ``FOO Guidance`` the name ``FOO Guidance (June
2024) Unknown Act`` counts as registered (this predates 3b367). The full form
still drops any four-digit year, date, version or edition parenthetical,
whether or not it is the named document's own, and an acronym item followed by
``s`` drops when its singular is the row's acronym (``(CCMs)`` after a CCM
name). The date and edition items are matched as written and are case-sensitive
(the WP-number match of an Article 29 Working Party citation reads its WP numbers
and the dates and editions after them case-insensitively, so ``(WP 248 rev.01)``
registers and ``(wp 248, wp 999)`` takes the same rule as ``(WP 248, WP 999)``;
the terminal-parenthetical allowlist's WP-number item is case-sensitive, so a
lowercase ``(wp 248)`` there is kept): ``(Mar 3, 2024)`` is
split at its comma into ``Mar 3`` and ``2024``, and ``(rev 2)``, ``(rev.01)``,
``(version 2)``, ``(V2)`` and ``(2024 Edition)`` match no item (``Rev`` and
``Version`` must be capitalized, ``v`` and ``edition`` lowercase), so each is
kept, and the citation warns only if neither the full form nor the stripped
form resolves and the stripped form is not excluded and is a citation (false
positives). A row's designators are read from its whole Standard ID, so a
designator named inside a row's ID (a replaced document) counts for that row
only within the row's issuing body: an EDPB row ``EDPB Guidelines 9/2022
(replacing Guidelines 01/2021)`` counts ``Guidelines 1/2021``, but the WP250 in
``EDPB Guidelines 9/2022 (replacing WP250)`` does not count for that row, since
a WP number counts only for an Article 29 Working Party row. An acronym the
glossary register expands is not used: the glossary is not tied to register
rows, and a PR can add a row to it. The EDPB's endorsement of WP29 documents is
not modelled: ``EDPB Opinion 05/2014`` and ``EDPB WP248`` are not registered by
the Article 29 Working Party rows.

SIBLING PROBE (report only). When the PR changes ``tools/alignment-register-aliases.json``
or the register, D15 also scans the WHOLE corpus at the PR head (every in-scope document,
every line, the three table surfaces above but not EU/EC numbers in prose) and lists each
citation that is still unregistered and shares a distinctive token with a changed alias key
(added, removed or retargeted between the merge base and the head) or a changed register
Standard ID (in one version's set of Standard IDs and not the other's: a row added or
removed, and a row whose Standard ID is edited counts as the old ID removed and the new one
added; an edit to a row's other cells, such as a date or a version, changes no Standard ID,
so on 2026-10-17 a synthetic edit that moved every date in the Last verified (UTC) cells of
all 23 register tables one day later, 217 dates in 216 of their 219 rows (189 of the 192
Standard ID rows and the 27 rows of the AI security tooling references table, which is keyed
by Project and which gate 6 does not parse; the other 3 rows read ``needs-reconfirm``), listed
nothing, where taking each of those 189 Standard IDs as changed lists 86 citations). It exists because in PR #2833 (3b364) round 1
aliased only the cited ``US TSA Pipeline Security Directives`` while the sibling row ``US TSA
Rail Cybersecurity Directives`` kept warning until a later round. The probe resolves
citations with the head's alias file (an absent one is an empty map), so a replay against
another head, or a PR that deletes the file, classifies with that head's aliases; the main
D15 check above, and both parts' exclusion policy, read the files in the checkout
(``ALIASES_PATH``, ``EXCLUSIONS_PATH``), which in CI is the commit checked out as the head (the
PR merge ref). D15 reads the register at ``--register-ref`` when it is given and at the head
otherwise, and only an absent register there ends the run: it, a missing merge base and a
failed ``git diff`` of the changed file names each end the run before the probe, with only
its own NOTE and no probe-skipped NOTE. A head without the register does not end a run with
a ``--register-ref`` that has one: the main check reads that ref's register, and the probe
compares the head's absent register as one with no rows, so when the PR deletes the register
every Standard ID of the merge base's register counts as removed. When
the main check cannot load the register or its policy files (an unreadable
or absent file in the checkout) it is skipped with a NOTE. The probe still lists siblings then
only when the file that failed is the checkout's alias file (absent, unreadable or malformed),
which the probe does not read: it also needs the exclusion policy in the checkout, a register
that parses and a head alias file that is absent or loads, and prints a NOTE that it was
skipped when one of them fails. With ``--register-ref``
the family tokens and the judgement of which citations are unregistered use that ref's
register, while the changed Standard IDs are still those between the merge base and the
head. A DISTINCTIVE TOKEN is a
case-folded run of ASCII letters and digits, after accents are removed (NFKD, combining
marks dropped, so ``Qu\u00e9bec`` and ``Quebec`` match), that is either a designator (letters and digits
together: ``C5``, ``WP248``, ``02G``), a number of three or more digits that is not a year
from 1900 to 2099 (``2557``, ``62443``), or a word of three or more letters not in
``SIBLING_STOP_WORDS``; and in every case one that appears in fewer than ``FAMILY_ROWS``
(ten) of the head register's Standard IDs: ``ISO``, ``IEC``, ``NIST``, ``800`` and
``Canada`` each name a family of rows (on 2026-10-17 every NIST alias key matched about 100
corpus rows through ``NIST`` alone), so the probe does not match on them. The stop list holds function words and words that name a kind of
instrument (``Act``, ``Directive``, ``Framework``), a topic (``Security``, ``Privacy``,
``Risk``) or a jurisdiction or kind of body (``European``, ``National``, ``Authority``):
each describes many unrelated instruments, so a shared stop word is no evidence that two
names denote one instrument (in the tests, ``ACME Security Directives`` is not listed beside a
``TSA Pipeline Security Directives`` fixture alias). Publisher acronyms stay distinctive, because the
3b364 sibling shared only ``TSA`` with the aliased row; a year is not distinctive because
unrelated editions share it; a two-letter word (``EU``, ``AI``, ``UK``) is too short. The
probe lists in two tiers, so that a citation sharing only a distinctive word is still listed
and the noise stays visibly weak. A
citation that shares a strong token of a changed entry, an acronym (a word with a capital
after its first letter as written: ``TSA``, ``CSA``, ``MiCA``, ``GenAI``), a designator or a
number, is a ``D15 SIBLING`` line. A citation that shares no acronym, designator or number
with any changed entry and a distinctive word with at least one is a ``D15 SIBLING (word
match)`` line after the strong ones, naming the shared
words (``pipeline`` of ``Transportation Security Administration Pipeline Security Directives
(SD Pipeline-2021-02G)`` beside the former alias key ``US TSA Pipeline Security Directives``
(removed in PR #2839; a test adds it back as a fixture), which
the 3b370 round 2 review found lost while the probe matched an entry with an acronym on its
acronym alone; ``quebec`` beside ``Quebec Law 25``). A word match is weak evidence: on
2026-10-17 words such as ``party``, ``assessment``, ``access``, ``design``, ``provisions`` and
``certification`` paired unrelated instruments of different publishers, and those words are
in the stop list, but other words still pair unrelated instruments. A changed entry with no
distinctive token is named in a NOTE line, and so is a change to the alias file's
``umbrella``, ``not_citable`` or ``agency_labels`` entries, which the probe does not compare. The probe never
changes the exit status and does not run when neither file changes. Residual (printed
beside the result): not listed are a form that shares no distinctive token with the changed
entry (``Law 25`` beside ``Quebec Law 25``, or a spelled-out name beside its acronym that
shares no distinctive word with it, such as one sharing only stop words or family tokens:
``Cloud Security Alliance Cloud Controls Matrix v4.1`` beside ``CSA Cloud Controls Matrix``), every
form of a changed entry with no distinctive token, a form sharing only a family token
(``NIST SP 800-57`` beside ``NIST SP 800-218``; the family tokens of the register in use are
printed), a sibling outside the three table surfaces (prose, an EU/EC number, or another
table: the ``Regulation / Programme`` table of Canadian programmes in the logistics annex is
not one), and the siblings of an ``umbrella``, ``not_citable`` or ``agency_labels`` change;
and a listed citation
can be a different instrument from the same publisher, as a word match often is.

Usage:
    python3 tools/check-alignment-register-on-pr.py                 # CI (GITHUB_BASE_REF)
    python3 tools/check-alignment-register-on-pr.py origin/main      # locally
    python3 tools/check-alignment-register-on-pr.py BASE HEAD --register-ref REF

Exit code once modules load: always 0 (advisory), including malformed arguments and internal errors.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from aiqt_corpus import iter_non_code_lines  # noqa: E402  # the line model gate 6 reads
from lint_common import AUDITED_DOMAIN_DIRS, PrRangeError, git, git_show, resolve_pr_range  # noqa: E402

TOOLS = Path(__file__).resolve().parent
REGISTER_REL = "governance/register-canonical-citations.md"
ALIASES_REL = "tools/alignment-register-aliases.json"
ALIASES_PATH = TOOLS / "alignment-register-aliases.json"
EXCLUSIONS_PATH = TOOLS / "alignment-register-exclusions.json"
# The three classes the 2026-10-16 decision names; a policy row of any other class is refused.
EXCLUSION_CLASSES = frozenset({"RFC", "vendor guidance", "book"})

# First header cells meaning "each row names one framework or standard". A header cell is
# compared by identity key, which drops the spaces around "/" ("Framework / Standard" is
# "framework/standard"), so both header sets are compared through ``header_keys``.
LIST_HEADERS = frozenset({
    "framework", "frameworks", "framework / standard", "framework or standard",
    "framework / regulation", "standard", "standards", "standard / framework",
    "regulation", "regulations", "regulation / guidance", "regulation / standard",
    "law / regulation", "regulation / guideline", "regulation / framework",
    "regulation / directive", "standard / regulation",
})
# Column headers whose cells are a free-text list of citations.
FREE_TEXT_HEADERS = frozenset({
    "regulatory", "regulatory references", "regulatory reference", "legal",
    "legal / regulatory", "other", "other references", "trade compliance",
    "framework reference", "framework references", "trade and supply chain programs",
})
# A matrix-header table is recognized only under one of these headings.
ALIGNMENT_HEADING = re.compile(r"framework alignment|crosswalk|standards alignment", re.I)

SEPARATOR = re.compile(r"\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?\s*")
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")

# EU/EC instrument numbers. A number counts when the instrument carries an EU/EC marker or
# suffix, or when one side of the number is a four-digit year (the register's own bare
# "Regulation 2016/679" form); ``num`` is compared verbatim with leading zeros dropped.
EU_NUMBER = re.compile(
    r"\b(?P<kind>(?:(?:Commission|Council)\s+)?(?:(?:Implementing|Delegated)\s+)?"
    r"(?:Regulation|Directive|Decision|Recommendation))"
    r"\s+(?:\((?P<marker>EU|EC|EEC|EU,\s*Euratom)\)\s+)?(?:No\.?\s+)?"
    r"(?P<num>\d{1,4}/\d{1,4})(?:/(?P<suffix>EC|EEC|EU))?(?![\w/])"
    r"|\((?P<marker2>EU|EC|EEC)\)\s+(?:No\.?\s+)?(?P<num2>\d{1,4}/\d{1,4})(?![\w/])"
)
# A designation in the text after a parenthetical acronym (``Resolver.paren_tail_ok``): an
# ``EU_NUMBER`` with an optional "EU " before it ("EU Regulation 2017/745").
TAIL_DESIGNATION = re.compile(rf"(?:\bEU\s+)?(?:{EU_NUMBER.pattern})")

# A trailing edition or version written after a framework name.
VERSION_TAIL = re.compile(
    r"(?:[\s:,(]+(?:v(?:ersion)?\s*)?\d+(?:\.\d+)*(?:\s*\(?(?:beta|draft|final)\)?)?\)?"
    r"|[\s:,(]+(?:Rev(?:ision)?\.?\s*\d+(?:\.\d+)*|\d{4}\s+edition|edition\s+\d+|beta|draft)\)?"
    r"|:\d{4})\s*$",
    re.I,
)
# A provision reference written after a citation ("GDPR Art. 32", "EU AI Act: High Risk",
# "EU AI Act Chapter IX"). ``strip_provision`` finds the first one outside parentheses.
# "Ch" and "Chapter" count only before a whole numeral token ("Chapter L", not "Chapter
# Implementation Guide").
PROVISION_TAIL = re.compile(
    r"\s*(?::\s|\bArt(?:icle)?s?\b\.?|§|\bSch(?:edule)?\b\.?"
    r"|\bAnnex\b|\bClauses?\b|\bSections?\b"
    r"|\bCh(?:apters?)?\b\.?\s+(?:[IVXLC]+|\d+)\b|\bRecital\b|\bpara(?:graph)?\b\.?|\bs\.\s*\d).*$"
)
# A jurisdiction label before a colon at the start of a segment ("Canada: TBS Directive on
# Automated Decision-Making"): the colon introduces the instrument, so it is not read as a
# provision tail. The names are the jurisdictions that begin a register Standard ID
# (2026-10-19), written as the register writes them (case-sensitive).
JURISDICTION_LABEL = re.compile(
    r"\s*(Australia|Brazil|British Columbia|Canada|China|Colorado|EU|Illinois|India|Malaysia|NYC"
    r"|Ontario|Quebec|Saudi Arabia|Singapore|South Korea|Switzerland|Texas|UK|US):\s+(?=\S)"
)
# "Article 29 Working Party" at the start of a segment names the issuing body, not a provision,
# so PROVISION_TAIL is applied only after it (exact spelling and case; not "Art 29", "Articles
# 29" or a mention after another citation, which is that citation's provision). A colon right
# after the body name introduces the document ("Article 29 Working Party: Opinion 2/2017"), so
# it is kept with the name rather than read as a provision tail.
ISSUING_BODY = re.compile(r"\s*Article\s+29\s+Working\s+Party\b(?::(?=\s+\S))?")
# An EDPB name: an optional "EU " and the board's acronym or full name at the start, or an
# "(EDPB)" issuer suffix at the end ("Guidelines 07/2020 on the concepts of controller and
# processor (EDPB)").
EDPB_NAME = re.compile(r"\s*(?:EU\s+)?(?:EDPB|European\s+Data\s+Protection\s+Board)\b")
EDPB_SUFFIX = re.compile(r"\(EDPB\)[\s.,;:]*$")
# The items of a terminal parenthetical the full form may drop without a register lookup: a date
# ("June 2024", "2025-05", "adopted 7 July 2021", "Sept. 2017") or an edition or version ("v2.0",
# "Version 1.1", "2025 edition"). A month is a full or standard abbreviated name ending at a word
# boundary, so "Decision 2024", "Marketing 2024" and "Novel 2024" are not dates.
MONTH = (
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?"
    r"|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b\.?"
)
DATE_ITEM = (
    r"(?:(?:adopted|updated|effective|published|revised)\s+)?(?:\d{1,2}\s+)?"
    rf"(?:{MONTH}\s+)?(?:\d{{1,2}},?\s+)?"
    r"\d{4}(?:[-.]\d{2}){0,2}"
)
EDITION_ITEM = r"(?:v|Version\s*|Rev(?:ision)?\.?\s*)\d+(?:\.\d+)*|\d{4}\s+edition|edition\s+\d+"
FIXED_ITEM = re.compile(rf"{DATE_ITEM}|{EDITION_ITEM}")
# A WP number ("WP 249") or EDPB-style designator ("Opinion 2/2017") is dropped only when the
# register row of the name it follows carries that designator (``Resolver.designator_source``).
DESIGNATOR_ITEM = re.compile(
    r"WP\s?\d{2,3}|(?:Guidelines|Opinion|Recommendations?|Statement)\s+\d{1,2}/\d{4}"
)
# The one other droppable item: an acronym word in capitals of three or more characters
# ("AICM", "KSIs", "O-AA"), and only when it is registered as the acronym of the name it follows
# (``Resolver.acronym_source``). Any other capitals word ("RETIRED", "DRAFTS", "USA", "HIPAA"
# after a name that is not HIPAA's) is substantive and stays part of the name.
ACRONYM_ITEM = re.compile(r"(?=[A-Z0-9&./:-]{3})[A-Z][A-Z0-9&./:-]*[A-Z0-9]s?")
# A parenthetical that ends the text, with nothing but whitespace or punctuation after its
# closing parenthesis; ``Resolver.paren_items`` judges its items.
TERMINAL_PAREN = re.compile(r"\s*\(([^()]*)\)[\s.,;:]*$")
# What may follow the last WP number of an Article 29 Working Party full form for the WP-number
# match: further WP numbers, dates, editions and punctuation only ("(WP 248 rev.01)"). Both read
# case-insensitively, as ``DESIGNATOR`` does, so "(wp 248, wp 999)" takes the same rule.
WP_NUMBER = re.compile(r"\bWP\s?(\d{2,3})\b", re.I)
WP_TAIL = re.compile(rf"(?:[\s.,;:()]|WP\s?\d{{2,3}}|{DATE_ITEM}|{EDITION_ITEM})*", re.I)
# A provision reference after a parenthetical acronym ("Annex I", "Art. 10(2)", "Arts. 5 to 7",
# "\u00a7164.312(a)", "Recital 26"): a provision word and one or more provision numbers, each a
# Roman numeral in capitals or digits with dotted parts, either with parenthesised sub-points,
# joined by "-", "\u2013", ",", "&", "and", "or" or "to". After such a connector a bare
# parenthesised sub-point may stand for a number ("Art. 10(1)(a) and (b)"). A sub-point
# (``SUBPOINT``) is a lowercase letter or two, one uppercase letter, a Roman numeral of up to
# six letters all lowercase or all capitals ("(cii)", "(IV)"), or one to three digits with an
# optional letter of either case ("(2A)"), and only sub-points chain after a number or a bare
# sub-point ("Art. 10(1)(a)", "(b)(ii)", "164.308(a)(1)(ii)(A)", "Art. 7(IV)"), so
# "(Fake)" and "(Act)" are not sub-points, alone or chained ("Art. 10(Fake)", "(b)(Fake)").
SUBPOINT = r"\((?-i:[a-z]{1,2}|[A-Z]|[ivxlcdm]{1,6}|[IVXLCDM]{1,6}|\d{1,3}[A-Za-z]?)\)"
PROVISION_NUMBER = rf"(?-i:[IVXLC]+|\d+[a-z]?(?:\.\d+)*)(?:{SUBPOINT})*"
PROVISION_SUBPOINT = rf"(?:{SUBPOINT})+"
PROVISION_REF = (
    r"(?:Art(?:icle)?s?\.?|\u00a7\u00a7?|Sch(?:edule)?s?\.?|Annex(?:es)?|Clauses?|Sections?"
    r"|Ch(?:apter)?s?\.?|Recitals?|para(?:graph)?s?\.?|s\.)"
    rf"\s*{PROVISION_NUMBER}"
    rf"(?:\s*(?:[-\u2013,&]|\band\b|\bor\b|\bto\b)\s*(?:{PROVISION_NUMBER}|{PROVISION_SUBPOINT}))*"
)
# What may follow a parenthetical acronym for it to stand for the citation (the row-word rule),
# once the row's own instrument numbers and designations are removed: only provision
# references, dates, editions, punctuation, "&" and "and" or "or" ("(CCM) v4.1", "(MDR) Annex
# I", "(MDR) Art. 10", "(MDR) Article 10 & Annex I", "(MDR) Art. 10(1)(a) and (b)"); so no
# other instrument number and no title ("(MDR) Annex I 2017/999", "(MDR): Unregistered Act").
# ``Resolver.paren_tail_ok`` also accepts a tail that the parenthetical names the row with.
PAREN_TAIL = re.compile(
    rf"(?:[\s.,;:()&]|\band\b|\bor\b|{PROVISION_REF}|{DATE_ITEM}|{EDITION_ITEM})*", re.I
)
# A possessive "'s" ("EU's"), removed from a name before its words are read.
POSSESSIVE = re.compile(r"(?<=[A-Za-z])['\u2019]s\b")
# An instrument number ("2017/745", "No 910/2014", "93/42/EEC"), compared as int/int.
INSTRUMENT_NUMBER = re.compile(r"\b(?:No\.?\s*)?(\d{1,4})/(\d{1,4})(?:/(?:EU|EC|EEC))?(?![\w/])")
# Words a spelled-out name may carry that its row need not, and that give no initials (the
# row-word rule).
NAME_FUNCTION_WORDS = frozenset({"a", "an", "and", "for", "in", "of", "on", "the", "to"})
# The title part of a register Topic cell: the text before a parenthetical, a ";", a sentence
# end, or a "," or ":" followed by a lowercase word ("UK General Data Protection Regulation
# (retained EU GDPR ...)" reads as "UK General Data Protection Regulation"; "Security, Trust,
# Assurance and Risk programme" is kept whole).
TOPIC_TITLE_END = re.compile(r"\s*(?:[(;]|\.\s|[,:]\s+(?=[a-z]))")
# A control code or code fragment standing alone ("A.3.4", "DE.CM-09", "SEF-07").
FRAGMENT = re.compile(
    r"(?:[A-Z]{1,4}\.)+[A-Z0-9]{1,4}(?:[.-][A-Z0-9]{1,3})*|[A-Z&]{2,5}-\d{1,3}(?:\.\d+)?"
)
# Trailing control codes in a free-text cell ("CSA CCM LOG-05", "NIST SP 800-53 CA-2"); a
# segment that is nothing but a code becomes empty and is not a citation.
CODE_TAIL = re.compile(r"(?:^|\s+)(?:[A-Z&]{2,5}-\d{1,2}(?:\.\d{1,2})?(?:\(\d+\))?\s*)+$")
ACRONYM = re.compile(r"\b[A-Z][A-Z0-9&]*[A-Z0-9](?:-[A-Z0-9]+)*\b")
INSTRUMENT_WORD = re.compile(
    r"\b(?:Act|Regulations?|Directive|Law|Code|Standard|Framework|Guidelines?|Rules?)\b"
)
# The sibling probe's stop list (see the module docstring): function words, and words naming a
# kind of instrument, a topic, or a jurisdiction or kind of body, none of which identifies one
# instrument. Case-folded; words shorter than three letters are never distinctive anyway.
SIBLING_STOP_WORDS = frozenset({
    # function words
    "and", "for", "from", "into", "its", "not", "per", "the", "under", "via", "with",
    # kinds of instrument
    "act", "acts", "amendment", "annex", "article", "baseline", "benchmark", "chapter",
    "code", "codes", "control", "controls", "criteria", "decision", "directive",
    "directives", "edition", "framework", "frameworks", "guidance", "guide", "guideline",
    "guidelines", "handbook", "law", "laws", "matrix", "model", "notice", "opinion", "order",
    "part", "policy", "principles", "program", "programme", "publication", "recommendation",
    "regulation", "regulations", "regulatory", "report", "requirement", "requirements",
    "rev", "revision", "rule", "rules", "section", "series", "special", "specification",
    "standard", "standards", "statement", "version",
    # topics
    "assurance", "cloud", "compliance", "critical", "cyber", "cybersecurity", "data",
    "digital", "governance", "incident", "information", "infrastructure", "management",
    "operational", "personal", "privacy", "protection", "quality", "reporting",
    "resilience", "risk", "safety", "security", "service", "services", "system", "systems",
    "technology",
    # generic words that named unrelated instruments of different publishers on 2026-10-17
    # (3b370 round 1 review: "Third-Party Risk Toolkit" beside an Article 29 Working Party
    # row, "Age Appropriate Design Code" beside EDPB Guidelines 4/2019)
    "access", "agentic", "application", "applications", "artificial", "assessment",
    "certification", "conduct", "design", "intelligence", "maturity", "party", "provision",
    "provisions", "right", "rights", "testing", "top", "verification", "working",
    # jurisdictions and kinds of body
    "agency", "association", "authority", "board", "commission", "council", "department",
    "european", "federal", "general", "government", "institute", "international",
    "kingdom", "ministry", "national", "office", "organisation", "organization", "states",
    "union", "united", "usa",
})
TOKEN = re.compile(r"[a-z0-9]+")
# A token in this many register Standard IDs names a family, not an instrument (2026-10-17:
# iso 31, iec 30, nist 19, 800 13, canada 12 of 192 rows; the next, edpb, 9; tsa 1).
FAMILY_ROWS = 10


def _load_gate6():
    """Gate 6's wrapper (register parser) and its pack engine (identity, discovery, resolve)."""
    spec = importlib.util.spec_from_file_location(
        "lint_standards_currency_for_d15", TOOLS / "lint-standards-currency.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module._engine()


GATE6 = ENGINE = None


def ensure_gate6():
    """Load gate 6 on demand so CLI failures can be reported as advisory notes."""
    global GATE6, ENGINE
    if ENGINE is None:
        GATE6, ENGINE = _load_gate6()


def identity_key(name: str) -> str:
    ensure_gate6()
    return ENGINE.identity_key(name)


def header_keys(headers: frozenset) -> frozenset:
    """The identity keys of a header set, normalized as a header cell is."""
    return frozenset(identity_key(h) for h in headers)


class PolicyError(ValueError):
    pass


def load_exclusions(text: str) -> list[dict]:
    """Validate and compile the exclusion policy. Every row names its class (one of the three
    the decision covers) and a reason; a pattern row must compile, an entry row names an exact
    citation. Raises PolicyError on any malformed row."""
    data = json.loads(text)
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise PolicyError("exclusion policy: schema_version 1 required")
    rows = []
    for kind in ("patterns", "entries"):
        items = data.get(kind)
        if not isinstance(items, list):
            raise PolicyError(f"exclusion policy: {kind!r} must be a list")
        for n, item in enumerate(items, 1):
            where = f"exclusion policy {kind}[{n}]"
            if not isinstance(item, dict):
                raise PolicyError(f"{where}: must be an object")
            if item.get("class") not in EXCLUSION_CLASSES:
                raise PolicyError(f"{where}: class must be one of {sorted(EXCLUSION_CLASSES)}")
            reason = item.get("reason")
            if not isinstance(reason, str) or len(reason.strip()) < 10:
                raise PolicyError(f"{where}: a reason of at least ten characters is required")
            key = "pattern" if kind == "patterns" else "name"
            value = item.get(key)
            if not isinstance(value, str) or not value.strip():
                raise PolicyError(f"{where}: {key!r} required")
            if kind == "patterns":
                try:
                    matcher = re.compile(value, re.I)
                except re.error as exc:
                    raise PolicyError(f"{where}: pattern does not compile ({exc})") from None
            else:
                matcher = re.compile(r"(?<!\w)" + re.escape(value) + r"(?!\w)", re.I)
            rows.append(dict(cls=item["class"], reason=reason, label=value, matcher=matcher))
    return rows


def load_aliases(text: str) -> dict:
    """Aliases (corpus name to register Standard ID), umbrella patterns (a family citation to
    the row that covers it, with any further rows it needs under ``also``), the
    not-citable vocabulary and the agency labels. A label may not be both an agency label and a
    ``not_citable.exact`` entry (compared by identity key)."""
    data = json.loads(text)
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise PolicyError("alias file: schema_version 1 required")
    aliases = data.get("aliases", {})
    umbrella = data.get("umbrella", [])
    not_citable = data.get("not_citable", {})
    agency_labels = data.get("agency_labels", [])
    if not isinstance(aliases, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in aliases.items()
    ):
        raise PolicyError("alias file: 'aliases' must map names to register Standard IDs")
    if not isinstance(umbrella, list):
        raise PolicyError("alias file: 'umbrella' must be a list")
    if not isinstance(not_citable, dict):
        raise PolicyError("alias file: 'not_citable' must be an object")
    for key in ("exact", "patterns"):
        values = not_citable.get(key, [])
        if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
            raise PolicyError(f"alias file: 'not_citable.{key}' must be a list of strings")
    if not isinstance(agency_labels, list) or not all(isinstance(v, str) for v in agency_labels):
        raise PolicyError("alias file: 'agency_labels' must be a list of strings")
    compiled = []
    for n, item in enumerate(umbrella, 1):
        try:
            also = item.get("also", [])
            if not isinstance(also, list) or not all(isinstance(r, str) for r in also):
                raise TypeError("'also' must be a list of register Standard IDs")
            compiled.append((re.compile(item["pattern"], re.I), item["row"], tuple(also)))
        except (AttributeError, KeyError, TypeError, re.error) as exc:
            raise PolicyError(f"alias file: umbrella[{n}] malformed ({exc})") from None
    exact = {identity_key(v) for v in not_citable.get("exact", [])}
    agencies = {identity_key(v) for v in agency_labels}
    # A label in both lists would be declared reportable and not citable at once: after_label
    # treats the two alike, and agency_label wins in _unregistered (read before not_citable)
    # and in resolve (its colon fallback reports an agency label's full form as unregistered).
    # The overlap is refused to keep the file unambiguous. The error names each entry as
    # agency_labels spells it.
    shared = list(dict.fromkeys(v for v in agency_labels if identity_key(v) in exact))
    if shared:
        raise PolicyError(
            f"alias file: 'agency_labels' and 'not_citable.exact' share {', '.join(shared)}"
        )
    try:
        patterns = [re.compile(p, re.I) for p in not_citable.get("patterns", [])]
    except re.error as exc:
        raise PolicyError(f"alias file: not_citable pattern does not compile ({exc})") from None
    return dict(
        aliases={identity_key(k): v for k, v in aliases.items()},
        umbrella=compiled,
        not_citable_exact=exact,
        not_citable_patterns=patterns,
        agency_labels=agencies,
    )


def eu_numbers(text: str) -> list[tuple[str, str]]:
    """(observed, number) for each EU/EC instrument number in ``text``."""
    out = []
    for m in EU_NUMBER.finditer(text):
        num = m["num"] or m["num2"]
        marked = bool(m["marker"] or m["suffix"] or m["marker2"])
        left, right = num.split("/")
        if not marked and not any(len(p) == 4 and 1950 <= int(p) <= 2099 for p in (left, right)):
            continue
        out.append((m[0], f"{int(left)}/{int(right)}"))
    return out


class Register:
    """The register rows as gate 6 parses them, plus the lookups this check adds."""

    def __init__(self, text: str):
        ensure_gate6()
        self.entries = GATE6.parse_register_text(text)
        self.ids = {e["identity_key"]: e["id"] for e in self.entries}
        self.numbers = set()
        # (issuing body, designator) per row: the body is derived from the Standard ID, so an
        # EDPB "Guidelines 07/2020" row does not register an Article 29 Working Party one.
        self.designators = set()
        # The same pairs per row, and the acronym words of each row's Standard ID ("CCM" of "CSA
        # CCM"), by identity key.
        self.row_designators = {}
        self.acronyms = {}
        for e in self.entries:
            cells = e["cells"]
            for cell in (cells[0], cells[1], cells[4]):
                self.numbers.update(num for _, num in eu_numbers(cell))
            body = row_body(e["id"])
            pairs = {(body, d) for d in designators(e["id"])} if body else set()
            self.designators |= pairs
            self.row_designators.setdefault(e["identity_key"], set()).update(pairs)
            self.acronyms[e["identity_key"]] = {
                w for w in re.findall(r"[^\s(),;]+", e["id"]) if ACRONYM_ITEM.fullmatch(w)
            }

    def has_id(self, std_id: str) -> bool:
        return identity_key(std_id) in self.ids

    def suffix_rows(self, name: str) -> list[str]:
        """The identity keys of the Standard IDs ``name`` is the whole-word tail of (``GDPR`` of
        ``EU GDPR`` and ``UK GDPR``). A one-word name qualifies only when it is an acronym or
        carries a digit."""
        key = identity_key(name)
        if len(key.split()) < 2 and not (ACRONYM.fullmatch(name) or re.search(r"\d", name)):
            return []
        return [k for k in self.ids if k.endswith(" " + key)]

    def by_suffix(self, name: str) -> bool:
        """``name`` is the whole-word tail of a Standard ID (``suffix_rows``)."""
        return bool(self.suffix_rows(name))

    def series_rows(self, key: str) -> list[str]:
        """The identity keys of the Standard IDs ``key`` is a series stem of: the ID continues
        with a part number (``IEC 62443`` of ``IEC 62443-3-3``) or with an edition or qualifier
        (``BASC International Security Standard`` of ``... 6.0.2 (2022, ...)``)."""
        out = []
        for k in self.ids:
            tail = k[len(key):] if k.startswith(key) and len(k) > len(key) else ""
            if (key[-1:].isdigit() and tail[:1] == "-") or re.match(r" (?:\d|series\b|\()", tail):
                out.append(k)
        return out

    def by_series(self, key: str) -> bool:
        """``key`` is a series stem of a Standard ID (``series_rows``)."""
        return bool(self.series_rows(key))

    def edition_rows(self, key: str) -> list[str]:
        """The identity keys of the Standard IDs ``key`` is followed by an edition and a
        qualifier (``CSA CCM v4.1 DSP domain``): the edition token marks where the registered
        name ends."""
        return [k for k in self.ids if re.match(re.escape(k) + r" v?\d", key)]

    def by_edition(self, key: str) -> bool:
        """``key`` is a Standard ID followed by an edition and a qualifier (``edition_rows``)."""
        return bool(self.edition_rows(key))


# EDPB and Article 29 Working Party designators ("Guidelines 07/2020", "Opinion 05/2014",
# "WP248"), compared with the leading zero dropped, so a long-form citation of a registered
# soft-law document matches its row whatever title wording follows the designator.
DESIGNATOR = re.compile(
    r"\b(?:(Guidelines|Opinion|Recommendations?|Statement)\s+0*(\d{1,2})/(\d{4})|WP\s?(\d{2,3}))\b",
    re.I,
)


def designators(text: str, issuer_known: bool = False) -> set[str]:
    if not issuer_known and not re.search(r"\b(?:EDPB|Article 29|WP\s?\d)", text, re.I):
        return set()
    out = set()
    for m in DESIGNATOR.finditer(text):
        out.add(f"wp{m[4]}" if m[4] else f"{m[1].lower().rstrip('s')} {int(m[2])}/{m[3]}")
    return out


def row_body(std_id: str) -> str:
    """The issuing body of a register row, from its Standard ID: ``edpb`` for an EDPB row,
    ``a29`` for an Article 29 Working Party, WP29 or WPnnn row, else empty."""
    if re.match(r"\s*EDPB\b", std_id):
        return "edpb"
    if re.search(r"Article\s+29\s+Working\s+Party|\bWP29\b", std_id) or re.match(r"\s*WP\s?\d", std_id):
        return "a29"
    return ""


def citation_issuer(name: str) -> str:
    """The issuing body a citation names: ``a29`` when it begins with ``Article 29 Working
    Party``, ``edpb`` when it begins with an EDPB name or ends with ``(EDPB)``, else empty."""
    if ISSUING_BODY.match(name):
        return "a29"
    if EDPB_NAME.match(name) or EDPB_SUFFIX.search(name):
        return "edpb"
    return ""


def citation_designators(name: str) -> set[tuple[str, str]]:
    """(issuing body, designator) per designator of a citation that names its issuer. A WP
    number is an Article 29 Working Party designator, so only such a citation carries one."""
    body = citation_issuer(name)
    if not body:
        return set()
    return {(body, d) for d in designators(name, True) if body == "a29" or not d.startswith("wp")}


def strip_markdown(cell: str) -> str:
    cell = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", cell)
    cell = re.sub(r"<br\s*/?>", "; ", cell, flags=re.I)
    cell = re.sub(r"<[^>]+>", "", cell)
    cell = cell.replace("\\|", "|")
    cell = re.sub(r"[*_`]", "", cell)
    return re.sub(r"\s+", " ", cell).strip()


def strip_version(name: str) -> str:
    """Remove trailing editions and versions; a parenthetical is never removed ("T (DRAFT) v2"
    becomes "T (DRAFT)"), so a terminal parenthetical is judged by the caller."""
    while True:
        m = VERSION_TAIL.search(name)
        if not m or m.start() == 0 or re.search(r"[()]", m[0]):
            return name
        name = name[:m.start()].strip()


class Resolver:
    def __init__(self, register: Register, aliases: dict, exclusions: list[dict]):
        self.register, self.aliases, self.exclusions = register, aliases, exclusions
        self._row_words: dict[str, set[str]] | None = None
        self._row_numbers: dict[str, set[str]] = {}
        self._family: frozenset | None = None

    def excluded(self, text: str):
        for row in self.exclusions:
            if row["matcher"].search(text):
                return row
        return None

    def not_citable(self, name: str) -> bool:
        key = identity_key(name)
        if not key or key in self.aliases["not_citable_exact"]:
            return True
        if any(p.fullmatch(name) for p in self.aliases["not_citable_patterns"]):
            return True
        # A leading digit or lowercase letter alone does not make an instrument prose:
        # "21 CFR Part 11", "15 U.S.C"/"15 USC 45", and "ePrivacy Directive"
        # still need register lookup; "2 CFRs apply" and "10 USCIS forms" do not.
        instrument = bool(INSTRUMENT_WORD.search(name) or re.search(r"\b(?:CFR\b|U\.?S\.?C\b)", name))
        if FRAGMENT.fullmatch(name):
            return True
        if name[0].isdigit() and not instrument:
            return True
        if name[0].islower() and not (instrument or re.search(r"\d", name)):
            return True
        # A citation has a shape: an acronym, a digit, or an instrument word with a name.
        return not (
            ACRONYM.search(name) or re.search(r"\d", name)
            or (INSTRUMENT_WORD.search(name) and len(name.split()) > 1)
        )

    def agency_label(self, name: str) -> bool:
        """``name`` is an agency label (``agency_labels`` in the alias file: ``CBP``,
        ``FINTRAC``, ``FMCSA``). Unlike a ``not_citable`` publisher name, an agency label is
        reported: bare as itself, in any case or shape, unless it is registered or excluded
        (``cbp``; ``_unregistered`` reads it after the exclusion policy and before
        ``not_citable``: the exact list, the patterns and the shape heuristic), and before a
        colon by its full form unless the text after the colon is registered or excluded
        (``after_label``)."""
        return identity_key(name) in self.aliases["agency_labels"]

    def named_row(self, cand: str) -> str | None:
        """The identity key of the register row ``cand`` names as a Standard ID or a curated
        alias key; None when it names none."""
        reg, key = self.register, identity_key(cand)
        if key in reg.ids:
            return key
        target = self.aliases["aliases"].get(key)
        if target and reg.has_id(target):
            return identity_key(target)
        return None

    def exact_row(self, cand: str) -> str | None:
        """The identity key of the register row ``cand`` names exactly: a Standard ID, a curated
        alias of one, or an umbrella pattern; None when it names none. An umbrella that also
        lists further rows (``also``: ``BASC Security Standard 6.0.2/6.0.3`` cites both the
        6.0.2 and the 6.0.3 row) applies only when every one of them is in the register."""
        row = self.named_row(cand)
        if row:
            return row
        for p, row, also in self.aliases["umbrella"]:
            if p.fullmatch(cand) and all(self.register.has_id(r) for r in (row, *also)):
                return identity_key(row)
        return None

    def exact_registered(self, cand: str) -> bool:
        """``cand`` is a register Standard ID, a curated alias of one, or matches an umbrella."""
        return self.exact_row(cand) is not None

    def acronym_source(self, word: str, row: str) -> str:
        """Why ``word`` is registered as the acronym of a name of the register row ``row``: it
        names that row itself as a Standard ID or curated alias key (an umbrella pattern does
        not count, since it can match a whole family), or it is an acronym word of the row's
        Standard ID. Empty when neither holds."""
        forms = {word, word[:-1]} if word.endswith("s") else {word}
        if any(self.named_row(f) == row for f in forms):
            return "registered"
        if forms & self.register.acronyms.get(row, set()):
            return "row acronym"
        return ""

    def designator_source(self, item: str, row: str) -> str:
        """``row designator`` when the register row ``row`` carries the designator ``item`` (a
        WP number or an EDPB-style designator) within the row's issuing body; else empty. A WP
        number is an Article 29 Working Party designator only."""
        body = row_body(self.register.ids.get(row, ""))
        pairs = {(body, d) for d in designators(item, True) if body == "a29" or not d.startswith("wp")}
        if body and pairs and pairs <= self.register.row_designators.get(row, set()):
            return "row designator"
        return ""

    def paren_items(self, inner: str, row: str) -> list[tuple[str, str]]:
        """(item, rule) per item of the parenthetical ``inner`` after a name of the register
        row ``row``; the rule is empty for a substantive item, which keeps the parenthetical
        part of the name."""
        out = []
        for item in (i.strip() for i in re.split(r"[,;]", inner)):
            if FIXED_ITEM.fullmatch(item):
                out.append((item, "date or edition"))
            elif DESIGNATOR_ITEM.fullmatch(item):
                out.append((item, self.designator_source(item, row)))
            elif ACRONYM_ITEM.fullmatch(item):
                out.append((item, self.acronym_source(item, row)))
            else:
                out.append((item, ""))
        return out

    def wp_registered(self, full: str) -> bool:
        """An Article 29 Working Party full form ("... under Article 35 (WP 248)") whose WP
        numbers are all registered, with nothing but WP numbers, dates and editions after the
        last one."""
        nums = list(WP_NUMBER.finditer(full))
        if citation_issuer(full) != "a29" or not nums or not WP_TAIL.fullmatch(full[nums[-1].end():]):
            return False
        return {("a29", f"wp{m[1]}") for m in nums} <= self.register.designators

    def full_registered(self, full: str) -> bool:
        """The full form of a citation, before ``split_parts`` removed its provision or title
        tail ("UK ICO, Employment practices and data protection: Monitoring workers"), matches
        exactly. A trailing edition or year is removed first; then a terminal parenthetical is
        dropped only when every item in it is a date, an edition, or a designator or acronym
        registered for the row the name before it names (``paren_items``); a substantive
        parenthetical, or one with text after it, is kept. An Article 29 Working Party full
        form is also registered by its WP numbers (``wp_registered``). Only these lookups
        apply: the suffix, series and comma-list rules stay with the stripped form."""
        if self.wp_registered(full):
            return True
        core = strip_version(full)
        if any(self.exact_registered(c) for c in {full, core}):
            return True
        m = TERMINAL_PAREN.search(core)
        if not m:
            return False
        bare = core[:m.start()].strip()
        for name in filter(None, {bare, strip_version(bare)}):
            row = self.exact_row(name)
            if row and all(rule for _, rule in self.paren_items(m[1], row)):
                return True
        return False

    def paren_rows(self, inner: str) -> set[str]:
        """The identity keys of the register rows a parenthetical's text names through the
        stripped form's lookups: exactly (``exact_row``), or as a whole-word suffix, series stem
        or edition-qualified name of a Standard ID (``(GDPR)`` names the EU GDPR and UK GDPR
        rows)."""
        reg, rows = self.register, set()
        for cand in filter(None, {inner, strip_version(inner)}):
            key = identity_key(cand)
            rows.update(filter(None, [self.exact_row(cand)]))
            rows.update(reg.suffix_rows(cand) + reg.series_rows(key) + reg.edition_rows(key))
        return rows

    def _row_entry(self, row: str) -> dict | None:
        return next((e for e in self.register.entries if e["identity_key"] == row), None)

    def row_words(self, row: str) -> set[str]:
        """The words of the register row ``row``, judged from the row itself: the tokens
        (case-folded, accents removed, a plural read as its singular by ``singular``) of its
        Standard ID, of the title part of its Topic cell (``topic_title``: ``Medical Device
        Regulation`` for ``EU MDR``; ``UK General Data Protection Regulation`` for ``UK GDPR``,
        whose cell goes on to describe the retained law) and of each curated alias key that
        targets it."""
        if self._row_words is None:
            words: dict[str, set[str]] = {}
            for e in self.register.entries:
                topic = topic_title(e["cells"][3] if len(e["cells"]) > 3 else "")
                text = fold_accents(f"{e['id']} {topic}").casefold()
                words.setdefault(e["identity_key"], set()).update(map(singular, TOKEN.findall(text)))
            for key, target in self.aliases["aliases"].items():
                if self.register.has_id(target):
                    words.setdefault(identity_key(target), set()).update(
                        map(singular, TOKEN.findall(fold_accents(key).casefold()))
                    )
            self._row_words = words
        return self._row_words.get(row, set())

    def row_numbers(self, row: str) -> set[str]:
        """The instrument numbers (``int/int``) of the register row ``row``: those in its
        Standard ID, its Current version cell (where the register records an instrument's
        number: ``Regulation 2017/745`` for ``EU MDR``), the title part of its Topic cell and
        each curated alias key that targets it. A Superseded versions number names an earlier
        instrument, so it is not one of the row's."""
        if row not in self._row_numbers:
            e = self._row_entry(row)
            texts = [e["id"], e["cells"][1], topic_title(e["cells"][3] if len(e["cells"]) > 3 else "")] if e else []
            texts += [k for k, t in self.aliases["aliases"].items() if self.register.has_id(t) and identity_key(t) == row]
            self._row_numbers[row] = {
                f"{int(m[1])}/{int(m[2])}" for text in texts for m in INSTRUMENT_NUMBER.finditer(text)
            }
        return self._row_numbers[row]

    def paren_tail_ok(self, after: str, row: str, inner: str = "") -> bool:
        """The whole text ``after`` the parenthetical ``inner`` naming the register row ``row``
        lets it stand for the citation: once the row's own instrument designations
        (``TAIL_DESIGNATION`` with a number of ``row_numbers``: ``(GDPR): Regulation (EU)
        2016/679``, ``(MDR): EU Regulation 2017/745``) and then its own instrument numbers are
        removed, it is only provision references (``PROVISION_REF``), dates, editions,
        punctuation and ``&``, ``and`` or ``or`` (``PAREN_TAIL``: ``(CCM) v4.1``, ``(MDR)
        2017/745``, ``(MDR) Annex I``, ``(MDR) Art. 10 and Annex I``, ``(MDR) Art. 10(1)(a) and
        (b)``); or its text up to its first provision tail outside parentheses
        (``strip_provision``) follows ``inner`` to
        make a name of the same row (``exact_row``: ``(HIPAA) Security Rule`` as ``HIPAA
        Security Rule``; not ``(CCPA) Regulations``, a name of another row) and the rest is
        such a tail. So ``(MDR) Unregistered Act``, ``(MDR) 2017/999``, ``(MDR) Annex I
        2017/999``, ``(MDR): Unregistered Act``, ``(MDR): Regulation (EU) 2017/999``, ``(MDR):
        EU Regulation 2017/999``, ``(MDR) Art. 10(1)(a) and (Fake)``, ``(MDR) Art. 10(1)(a)
        and (b)(Fake)``, ``(MDR) Art. 10(Fake)`` and ``(HIPAA) Security Rule: Unregistered
        Act`` do not."""
        numbers = self.row_numbers(row)

        def own_designation(m: re.Match) -> str:
            left, right = (m["num"] or m["num2"]).split("/")
            return " " if f"{int(left)}/{int(right)}" in numbers else m[0]

        rest = INSTRUMENT_NUMBER.sub(
            lambda m: " " if f"{int(m[1])}/{int(m[2])}" in numbers else m[0],
            TAIL_DESIGNATION.sub(own_designation, after),
        )
        if PAREN_TAIL.fullmatch(rest):
            return True
        head = strip_provision(rest)
        tail = rest[len(head):]
        title = f"{inner} {head.strip()}"
        return bool(
            inner and head.strip() and PAREN_TAIL.fullmatch(tail)
            and row in {self.exact_row(title), self.exact_row(strip_version(title))}
        )

    def words_name_row(self, name: str, row: str, inner: str = "") -> bool:
        """``name`` names the register row ``row`` by its words, for the parenthetical ``inner``.
        The name's words are case-folded with accents removed, a possessive ``'s`` is removed
        (``EU's`` as ``eu``), a plural is read as its singular (``singular``: ``Devices`` as
        ``device``), ``European`` is read as ``eu`` when the row's Standard ID carries ``EU``,
        an instrument number of the row (``row_numbers``) is dropped, another instrument number
        stays one word that no row carries (so ``2019/1937`` is not read as two years), and a
        four-digit year from 1900 to 2099 outside an instrument number is dropped; function
        words (``NAME_FUNCTION_WORDS``) need not be row words and give no initials. It names the
        row when any of these holds:

        - every other word is a word of the row's Standard ID, at least one of them is not a
          family token, and they include every word of the Standard ID that ``inner`` does not
          carry, leaving out its function words, instrument numbers and years (``UK`` before
          ``(UK GDPR)``; ``NIST`` before ``(CSF)`` is not, since ``nist`` names a family;
          ``Working Party Guidelines`` before ``(WP248 rev.01)`` is not, since the Standard ID
          also carries ``Article 29 ... Data Protection Impact Assessment``);
        - the name carries an instrument number of the row and every other word is a word of
          the row (``row_words``): ``Regulation (EU) 2016/679`` before ``(GDPR)``; or
        - every other word is a word of the row or one of a run of consecutive other words
          with no function word between them (a function word breaks a run and gives it no
          letter) whose initials spell an acronym word of the Standard ID other than one
          ``inner`` carries (``Cloud Security Alliance`` for the ``CSA`` of ``CSA CCM`` before
          ``(CCM)``; ``Consumer Safety and`` and ``Cloud Security and Alliance`` spell no
          ``CSA``; ``Global Data Protection Rules`` does not spell out the ``GDPR`` of
          ``(GDPR)``); at least one row word stands outside such runs (``Cloud Security Alliance
          Consumer Safety Act (CCM)`` is only runs); and the initials of the name's other
          words, in order and a repeated word counted once, give all but at most one letter,
          and at least two, of an acronym word of ``inner`` (``Data Protection Regulation``
          gives ``DPR`` of ``GDPR``; ``Regulation`` gives only ``R``; ``Medical Device
          Regulation`` gives only ``DR`` of ``IVDR``; the ``and`` of ``Trust and Risk`` gives
          no ``A`` of ``STAR``; ``Cloud Cloud`` gives only ``C`` of ``CCM``).

        So ``Unknown Widget Standard`` names no row, ``Regulation`` does not name the GDPR rows
        and ``Retained`` does not name UK GDPR."""
        if self._family is None:
            self._family = family_tokens(self.register)
        std_id = self.register.ids.get(row, "")
        id_words = {singular(w) for w in TOKEN.findall(fold_accents(std_id).casefold())}
        numbers, own = self.row_numbers(row), []

        def number(m: re.Match) -> str:
            num = f"{int(m[1])}/{int(m[2])}"
            if num in numbers:
                own.append(num)
                return " "
            return f" n{int(m[1])}x{int(m[2])} "  # one word, not two years, that no row carries

        text = INSTRUMENT_NUMBER.sub(number, POSSESSIVE.sub("", fold_accents(name)))
        words = [
            "eu" if w == "european" and "eu" in id_words else singular(w)
            for w in TOKEN.findall(text.casefold())
            if not is_year(w)
        ]
        content = [i for i, w in enumerate(words) if w not in NAME_FUNCTION_WORDS]
        if not content:
            return False
        inner_words = {singular(w) for w in TOKEN.findall(fold_accents(inner).casefold())}
        required = {
            singular(w)
            for w in TOKEN.findall(INSTRUMENT_NUMBER.sub(" ", fold_accents(std_id)).casefold())
            if w not in NAME_FUNCTION_WORDS and not is_year(w)
        } - inner_words
        if (
            all(words[i] in id_words for i in content)
            and any(words[i] not in self._family for i in content)
            and required <= {words[i] for i in content}
        ):
            return True
        vocab = self.row_words(row)
        if own and all(words[i] in vocab for i in content):
            return True
        acronyms = {a.casefold() for a in self.register.acronyms.get(row, set())}
        acronyms -= set(TOKEN.findall(fold_accents(inner).casefold()))
        # A run is consecutive words with no function word between them, so a function word
        # gives no letter of a run and breaks one ("Consumer Safety and" and "Cloud Security
        # and Alliance" do not spell CSA).
        in_run = [False] * len(words)
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                if words[j - 1] in NAME_FUNCTION_WORDS:
                    break
                if j - i >= 2 and "".join(w[0] for w in words[i:j]) in acronyms:
                    in_run[i:j] = [True] * (j - i)
        if not all(words[k] in vocab or in_run[k] for k in content):
            return False
        if not any(words[k] in vocab and not in_run[k] for k in content):
            return False
        # A repeated word gives its initial once ("Cloud Cloud" gives only C).
        initials = "".join(w[0] for w in dict.fromkeys(words[i] for i in content))
        # The acronym words of ``inner``, a lowercase plural "s" dropped ("CCMs" spells "ccm").
        spelled = [
            re.sub(r"[^a-z0-9]", "", (w[:-1] if w.endswith("s") else w).casefold())
            for w in inner.split() if ACRONYM_ITEM.fullmatch(w)
        ]
        return any(
            common_subsequence(initials, a) >= max(2, len(a) - 1) for a in spelled if len(a) >= 3
        )

    def paren_names_row(self, before: str, inner: str, after: str = "") -> bool:
        """The parenthetical ``inner`` may stand for the citation in the stripped form's lookups:
        it names a register row (``paren_rows``) for which the text ``after`` it is acceptable
        (``paren_tail_ok``) and either nothing precedes it or the name ``before`` it, with or
        without a trailing edition, names that row by its words (``words_name_row``). So
        ``Medical Device Regulation (MDR)`` registers through the EU MDR row and ``Unknown
        Widget Standard (GDPR)`` does not register through the GDPR rows. A name that is itself
        registered (a Standard ID, alias or umbrella match) registers the citation on its own,
        so this rule decides only names that are not."""
        names = list(filter(None, {before, strip_version(before)}))
        return any(
            self.paren_tail_ok(after, row, inner)
            and (not before or any(self.words_name_row(n, row, inner) for n in names))
            for row in self.paren_rows(inner)
        )

    def name_registered(self, name: str, full: str = "") -> bool:
        """``name`` is registered by the stripped form's lookups. ``full`` is the citation before
        its provision tail was removed: the text after a parenthetical is read from it when it
        begins with ``name`` up to that parenthetical, so the whole tail is judged
        (``paren_tail_ok``: ``(MDR) Annex I 2017/999`` does not count although the stripped
        form ends at ``(MDR)``)."""
        reg = self.register
        bare = name.split("(", 1)[0].strip()
        candidates = {name, strip_version(name), bare, strip_version(bare)}
        for m in re.finditer(r"\(([^()]*)\)", name):  # an acronym or alias in parentheses
            after = full[m.end():] if full.startswith(name[:m.end()]) else name[m.end():]
            if self.paren_names_row(name[:m.start()].strip(), m[1].strip(), after):
                candidates |= {m[1].strip(), strip_version(m[1].strip())}
        for cand in filter(None, candidates):
            key = identity_key(cand)
            if self.exact_registered(cand):
                return True
            if reg.by_suffix(cand) or reg.by_series(key) or reg.by_edition(key):
                return True
        # An Article 29 Working Party citation that carries a WP number is matched by the
        # full-form WP-number rule (``wp_registered``) whether or not it had a provision tail.
        if citation_issuer(name) == "a29" and WP_NUMBER.search(name):
            if self.wp_registered(name):
                return True
        elif citation_designators(name) & reg.designators:
            return True
        # A comma list in a name cell ("EU AI Act, GDPR") is registered when every member is.
        parts = [p.strip() for p in bare.split(",")]
        return len(parts) > 1 and all(p and self.name_registered(p) for p in parts)

    def resolve(self, text: str, full: str = "") -> list[tuple[str, str]]:
        """(status, detail) per citation in one cell or segment: status is ``registered``,
        ``excluded``, ``not-citable`` or ``unregistered``. A registered citation is registered
        even when it also matches the exclusion policy (a registered vendor framework stays
        tracked); the policy decides only what an unregistered citation means. ``full`` is the
        segment before its provision or title tail was removed: an exact match on it registers
        the citation, and otherwise ``text`` resolves as before. A label cut at a colon that is
        not a citation on its own or is an agency label (``after_label``) is resolved by the
        text after the colon, and an unregistered one is reported as ``full`` ("FINTRAC:
        Proceeds of Crime (Money Laundering) and Terrorist Financing Act", not "FINTRAC"). When
        nothing after the colon is unregistered or excluded and not all of it is registered
        (none of it, or only part of it), an agency label is still reported as ``full`` ("CBP:
        Unknown Programme") and any other label is not a citation ("NIST: Govern function",
        "Security management process: risk analysis")."""
        text, full = strip_markdown(text), strip_markdown(full)
        if not text:
            return [("not-citable", "")]
        if full and full != text and self.full_registered(full):
            return [("registered", full)]
        after = self.after_label(text, full)
        if after is not None:
            inner = self.resolve(strip_provision(after).strip(" ."), after)
            if any(status == "unregistered" for status, _ in inner):
                return [("unregistered", full)]
            if all(status == "registered" for status, _ in inner):
                return [("registered", full)]
            excluded = [o for o in inner if o[0] == "excluded"]
            if excluded:
                return excluded
            return [("unregistered", full)] if self.agency_label(text) else [("not-citable", text)]
        grammar = [o for o in ENGINE.discover(text, ".md") if o["channel"] == "grammar"]
        if grammar:
            out = []
            for occ in grammar:
                kinds = [k for k, _ in ENGINE.resolve(occ, self.register.entries, GATE6.BARE_EXCEPTIONS)]
                observed = occ["observed"]
                if "UNREGISTERED" in kinds and not (
                    self.register.by_series(occ["identity"]) or self.name_registered(observed)
                ):
                    out.append(self._unregistered(observed))
                else:
                    out.append(("registered", observed))
            return out
        if self.name_registered(text, full):
            return [("registered", text)]
        return [self._unregistered(text)]

    def after_label(self, text: str, full: str) -> str | None:
        """The text after the colon when the citation ``text`` is a label cut at a colon and its
        full form ``full`` continues it ("FMCSA: Electronic Logging Devices (ELD)"), and the
        label is not excluded, is not registered (``name_registered``: a registered name before
        a colon, such as ``Switzerland nFADP`` or the alias key ``Cloud Controls Matrix``, keeps
        its tail and resolves as before; so does a publisher name that is only a series stem of
        a Standard ID, such as ``ISO``, ``IEC``, ``IEEE`` or ``ISO/IEC`` with today's register,
        so ``ISO: Unknown Act 2020`` gives no finding while ``NIST: Unknown Act 2020`` is
        reported) and is an agency label (``agency_label``: ``FINTRAC``,
        ``FMCSA``) or not a citation on its own (``not_citable``). None otherwise, so ``ACME:
        Unknown Act`` still reports ``ACME``. A generic prose label is not a citation on its
        own either, so ``Note: Unknown Act 2020`` in a free-text cell is reported with its
        prefix, as the full form, like an agency label."""
        if not full.startswith(text):
            return None
        m = re.match(r"\s*:\s+(?=\S)", full[len(text):])
        if not m or self.excluded(text) or self.name_registered(text):
            return None
        if not (self.agency_label(text) or self.not_citable(text)):
            return None
        return full[len(text) + m.end():]

    def _unregistered(self, text: str) -> tuple[str, str]:
        row = self.excluded(text)
        if row:
            return ("excluded", f"{row['cls']}: {row['reason']}")
        # An agency label is reported whatever its case or shape ("cbp", a configured
        # "Customs Bureau"), so not_citable below (the exact list, the patterns and the shape
        # heuristic) never silences it.
        if self.agency_label(text):
            return ("unregistered", text)
        if self.not_citable(text):
            return ("not-citable", text)
        return ("unregistered", text)


def strip_provision(text: str) -> str:
    """``text`` without its provision tail: from the first ``PROVISION_TAIL`` match outside
    parentheses, so a provision inside a parenthetical stays part of the name ("California
    CCPA ADMT and risk-assessment regulations (11 CCR Div 6 Ch 1 Arts 10-11)" is kept whole,
    not cut at "(11 CCR Div 6")."""
    pos = 0
    while m := PROVISION_TAIL.search(text, pos):
        depth = 0
        for ch in text[:m.start()]:
            depth += ch == "("
            depth -= ch == ")" and depth > 0
        if depth == 0:
            return text[:m.start()]
        pos = m.start() + 1
    return text


def split_parts(cell: str, free_text: bool) -> list[tuple[str, str]]:
    """Split a cell into (citation, full form) pairs. Both kinds split on ";" outside
    parentheses and on " / " and " + "; a free-text cell also splits on ",". Each citation
    loses its provision suffix outside parentheses ("Art. 32", ": High Risk", "Chapter IX";
    ``strip_provision``), and a free-text segment its trailing control codes ("CSA CCM
    LOG-05"); the full form keeps the provision suffix, so a title after a colon still reaches
    the exact lookups. A segment that begins with a jurisdiction label (``JURISDICTION_LABEL``)
    is the instrument after the colon, and its full form is the jurisdiction and the instrument
    without the colon ("Canada TBS Directive on Automated Decision-Making"). A segment whose
    citation is empty is dropped. A link to a corpus document is an internal reference, not a
    citation."""
    cell = re.sub(r"\[[^\]]*\]\((?!https?:)[^)]*\.md(?:#[^)]*)?\)", "", cell)
    cell = strip_markdown(cell)
    stops = ";," if free_text else ";"
    depth, buf, parts = 0, [], []
    for ch in cell:
        depth += ch == "("
        depth -= ch == ")" and depth > 0
        if ch in stops and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    out = []
    for part in parts:
        for full in re.split(r"\s+/\s+|\s+\+\s+", part):
            body = ISSUING_BODY.match(full)
            label = None if body else JURISDICTION_LABEL.match(full)
            if label:
                rest = full[label.end():]
                seg, full = strip_provision(rest), f"{label[1]} {rest}"
            else:
                head = body[0] if body else ""
                seg = head + strip_provision(full[len(head):])
            if free_text:
                seg, full = CODE_TAIL.sub("", seg), CODE_TAIL.sub("", full)
            seg, full = seg.strip(" ."), full.strip(" .")
            if seg:
                out.append((seg, full))
    return out


def cells_of(line: str) -> list[str]:
    raw = line.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|") and not raw.endswith("\\|"):
        raw = raw[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", raw)]


def iter_tables(lines: list[str], eligible: set[int]):
    """Yield (header_line_no, header_cells, row_line_nos, heading) for each pipe table."""
    heading, i = "", 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in eligible and re.match(r"#{1,6}\s", line):
            heading = line
        if (
            i + 1 in eligible and line.lstrip().startswith("|")
            and i + 1 < len(lines) and SEPARATOR.fullmatch(lines[i + 1])
        ):
            header = cells_of(line)
            j = i + 2
            rows = []
            while j < len(lines) and lines[j].lstrip().startswith("|") and j + 1 in eligible:
                rows.append(j + 1)
                j += 1
            yield i + 1, header, rows, heading
            i = j
            continue
        i += 1


def scan_text(text: str, added: set[int], resolver: Resolver) -> list[tuple[int, str, str]]:
    """(line_no, surface, citation) for each unregistered citation on an added line of one
    Markdown document. PURE over its inputs, so the unit tests drive it without git."""
    lines = text.splitlines()
    eligible = {ln for ln, _ in iter_non_code_lines(text)}
    found: list[tuple[int, str, str]] = []
    list_headers, free_text_headers = header_keys(LIST_HEADERS), header_keys(FREE_TEXT_HEADERS)

    def record(ln, surface, cell, free_text):
        for part, full in split_parts(cell, free_text):
            for status, detail in resolver.resolve(part, full):
                if status == "unregistered":
                    found.append((ln, surface, detail))

    for header_ln, header, rows, heading in iter_tables(lines, eligible):
        norm = [identity_key(strip_markdown(h)) for h in header]
        list_form = bool(norm) and norm[0] in list_headers
        matrix_form = not list_form and bool(ALIGNMENT_HEADING.search(heading))
        if not (list_form or matrix_form):
            continue
        free_cols = {i for i, h in enumerate(norm) if h in free_text_headers}
        if matrix_form and header_ln in added:
            for i, cell in enumerate(header[1:], 1):
                if i not in free_cols:
                    record(header_ln, "alignment-table header", cell, False)
        for ln in rows:
            if ln not in added:
                continue
            row = cells_of(lines[ln - 1])
            if list_form and row:
                record(ln, "alignment-table row", row[0], False)
            for i in sorted(free_cols):
                if i < len(row):
                    record(ln, "citation-list cell", row[i], True)

    for ln in sorted(added & eligible):
        if ln - 1 >= len(lines):
            continue
        for observed, num in eu_numbers(lines[ln - 1]):
            # A table cell already reported as this instrument is not reported twice.
            if num not in resolver.register.numbers and not any(
                f[0] == ln and observed in f[2] for f in found
            ):
                found.append((ln, "EU/EC instrument number", observed))

    seen, out = set(), []
    for item in sorted(found):
        key = (item[0], identity_key(item[2]))
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def added_lines(diff: str) -> set[int]:
    """Head-side line numbers a unified ``-U0`` diff adds or changes."""
    out: set[int] = set()
    for line in diff.splitlines():
        m = HUNK.match(line)
        if m:
            start, count = int(m[1]), int(m[2] if m[2] is not None else 1)
            out.update(range(start, start + count))
    return out


def in_scope(rel: str) -> bool:
    ensure_gate6()
    if not rel.endswith(".md") or rel in GATE6.EXEMPT_FILES:
        return False
    return rel.split("/", 1)[0] in AUDITED_DOMAIN_DIRS and "/" in rel


def build_resolver(register_text: str, aliases_text: str | None = None) -> Resolver:
    """The resolver over ``register_text``. The main check reads the alias file from the
    checkout (``ALIASES_PATH``); the sibling probe passes the head's alias file as
    ``aliases_text``. The exclusion policy is always read from the checkout."""
    if aliases_text is None:
        aliases_text = ALIASES_PATH.read_text(encoding="utf-8")
    return Resolver(
        Register(register_text),
        load_aliases(aliases_text),
        load_exclusions(EXCLUSIONS_PATH.read_text(encoding="utf-8")),
    )


def fold_accents(text: str) -> str:
    """``text`` with accents removed (NFKD, combining marks dropped): ``Qu\u00e9bec`` becomes
    ``Quebec``."""
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def singular(word: str) -> str:
    """A case-folded word with a plural ``s`` removed (``devices`` to ``device``; not ``access``
    or a word of three letters or fewer), so the row-word rule compares singular and plural
    forms as one word. Applied to both sides, so an odd stem (``analysi``) still matches."""
    return word[:-1] if len(word) > 3 and word.endswith("s") and not word.endswith("ss") else word


def is_year(word: str) -> bool:
    """``word`` is a four-digit year from 1900 to 2099."""
    return len(word) == 4 and word.isdigit() and 1900 <= int(word) <= 2099


def topic_title(topic: str) -> str:
    """The title part of a register Topic cell (``TOPIC_TITLE_END``)."""
    return TOPIC_TITLE_END.split(topic, 1)[0].strip()


def common_subsequence(a: str, b: str) -> int:
    """The length of the longest common subsequence of ``a`` and ``b``."""
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0]
        for j, other in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if ch == other else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]


def distinctive_tokens(text: str, family: frozenset = frozenset()) -> set[str]:
    """The distinctive tokens of a name (module docstring, SIBLING PROBE): designators mixing
    letters and digits, numbers of three or more digits that are not a 1900-2099 year, and
    words of three or more letters outside ``SIBLING_STOP_WORDS``; none in ``family``. Accents
    are removed first."""
    out = set()
    for tok in TOKEN.findall(fold_accents(text).casefold()):
        digits = sum(c.isdigit() for c in tok)
        if digits and digits < len(tok):
            out.add(tok)
        elif digits:
            if len(tok) >= 3 and not (len(tok) == 4 and 1900 <= int(tok) <= 2099):
                out.add(tok)
        elif len(tok) >= 3 and tok not in SIBLING_STOP_WORDS:
            out.add(tok)
    return out - family


def family_tokens(register: Register) -> frozenset:
    """Tokens in ``FAMILY_ROWS`` or more register Standard IDs: they name a family of
    instruments (``iso``, ``nist``, ``800``), not one, so the sibling probe does not match on
    them."""
    counts: dict[str, int] = {}
    for e in register.entries:
        for tok in distinctive_tokens(e["id"]):
            counts[tok] = counts.get(tok, 0) + 1
    return frozenset(t for t, n in counts.items() if n >= FAMILY_ROWS)


def entry_tokens(entry: str, family: frozenset = frozenset()) -> tuple[set[str], set[str]]:
    """(strong, words): the distinctive tokens of a changed entry, none in ``family``, split
    into its acronyms (a word with a capital after its first letter as written: ``TSA``,
    ``MiCA``, ``GenAI``), designators and numbers, and its other distinctive words
    (``Pipeline``, ``Quebec``). A citation sharing a strong token is a ``D15 SIBLING`` line;
    one sharing only words is a weak ``D15 SIBLING (word match)`` line, since a word such as
    ``Pipeline`` names many publishers' instruments."""
    tokens = distinctive_tokens(entry, family)
    caps = {
        t.casefold() for t in re.findall(r"[A-Za-z0-9]+", fold_accents(entry))
        if t.isalpha() and any(c.isupper() for c in t[1:])
    }
    strong = {t for t in tokens if t in caps or any(c.isdigit() for c in t)}
    return strong, tokens - strong


def alias_sections(text: str | None) -> dict:
    """The top-level object of one version of the alias file; an absent file is an empty map.
    Raises PolicyError when the file is not a JSON object (and ValueError on invalid JSON)."""
    if text is None:
        return {}
    data = json.loads(text)
    if not isinstance(data, dict):
        raise PolicyError("alias file: the top level must be a JSON object")
    return data


def changed_alias_keys(base_text: str | None, head_text: str | None) -> list[str]:
    """Alias keys added, removed or retargeted between two versions of the alias file (an
    absent file has no aliases). Raises ValueError on a malformed file."""
    maps = []
    for text in (base_text, head_text):
        aliases = alias_sections(text).get("aliases", {})
        if not isinstance(aliases, dict):
            raise PolicyError("alias file: 'aliases' must map names to register Standard IDs")
        maps.append(aliases)
    base, head = maps
    return sorted(k for k in set(base) | set(head) if base.get(k) != head.get(k))


def changed_uncovered_sections(base_text: str | None, head_text: str | None) -> list[str]:
    """The alias-file sections the sibling probe does not compare (``umbrella``,
    ``not_citable``, ``agency_labels``) that differ between two versions of the file."""
    base, head = alias_sections(base_text), alias_sections(head_text)
    return [s for s in ("umbrella", "not_citable", "agency_labels") if base.get(s) != head.get(s)]


def changed_standard_ids(base_text: str | None, head_text: str | None) -> list[str]:
    """Standard IDs in one version of the register and not the other (an absent register has
    no rows): a row added or removed, and a row whose Standard ID is edited counts as its old
    ID removed and its new ID added. Only the set of Standard IDs is compared, so an edit to a
    row's other cells (a date, a version) changes nothing here."""
    ensure_gate6()
    base, head = (
        {e["id"] for e in GATE6.parse_register_text(text)} if text is not None else set()
        for text in (base_text, head_text)
    )
    return sorted(base ^ head)


def probe_siblings(changed: list[tuple[str, str]], docs, resolver: Resolver) -> tuple[list[tuple], list[tuple]]:
    """(strong, weak): lists of (rel, line_no, surface, citation, shared tokens, kind, entry)
    for the unregistered alignment-table citations in ``docs`` (pairs of path and text, every
    line scanned). A citation sharing a strong token (``entry_tokens``) with a changed ``(kind,
    entry)`` is strong and names the first such entry; any other citation sharing a word of a
    changed entry is weak and names the first entry it shares a word with. Each citation is
    listed once. PURE over its inputs."""
    family = family_tokens(resolver.register)
    probes = [(kind, entry, *entry_tokens(entry, family)) for kind, entry in changed]
    strong, weak = [], []
    for rel, text in docs:
        every_line = set(range(1, len(text.splitlines()) + 1))
        for ln, surface, citation in scan_text(text, every_line, resolver):
            if surface == "EU/EC instrument number":
                continue
            tokens = distinctive_tokens(citation)
            hit = next(
                ((kind, entry, tokens & probe) for kind, entry, probe, _ in probes if tokens & probe), None
            )
            out = strong
            if hit is None:
                out = weak
                hit = next(
                    ((kind, entry, tokens & words) for kind, entry, _, words in probes if tokens & words), None
                )
            if hit is not None:
                kind, entry, shared = hit
                out.append((rel, ln, surface, citation, sorted(shared), kind, entry))
    return strong, weak


def sibling_report(texts: dict, register_text: str, docs) -> list[str]:
    """The sibling probe's output lines. ``texts`` holds the base and head versions of the
    alias file and the register (``base_aliases``, ``head_aliases``, ``base_register``,
    ``head_register``; None when absent); ``register_text`` is the register the citations
    resolve against (the head's, or the ``--register-ref`` one); ``docs`` are (path, text)
    pairs. The resolver reads the head's alias file, an absent one as an empty map. Raises
    OSError or ValueError (PolicyError, RegisterError, JSON) when an input cannot be read."""
    head_aliases = texts["head_aliases"]
    resolver = build_resolver(
        register_text, head_aliases if head_aliases is not None else '{"schema_version": 1}'
    )
    changed = [("alias key", k) for k in changed_alias_keys(texts["base_aliases"], head_aliases)] + [
        ("register Standard ID", s)
        for s in changed_standard_ids(texts["base_register"], texts["head_register"])
    ]
    family = family_tokens(resolver.register)
    lines = []
    for section in changed_uncovered_sections(texts["base_aliases"], head_aliases):
        lines.append(
            f"D15 NOTE: this PR changes the {section!r} entries of {ALIASES_REL}; the sibling probe "
            f"compares alias keys and register Standard IDs only and does not cover them."
        )
    if not changed:
        lines.append(
            "D15 NOTE: no alias key or register Standard ID is added, removed or retargeted (an "
            "edit to other register cells, such as a date or a version, is not compared); the "
            "sibling probe has nothing to match."
        )
    for kind, entry in changed:
        if not any(entry_tokens(entry, family)):
            lines.append(f"D15 NOTE: changed {kind} {entry!r} has no distinctive token; the sibling probe cannot list its siblings.")
    strong, weak = probe_siblings(changed, docs, resolver)
    for rel, ln, surface, citation, shared, kind, entry in strong:
        lines.append(
            f"D15 SIBLING {rel}:{ln}: {surface} {citation!r} shares "
            f"{', '.join(repr(t) for t in shared)} with changed {kind} {entry!r} and has no row in {REGISTER_REL}"
        )
    for rel, ln, surface, citation, shared, kind, entry in weak:
        lines.append(
            f"D15 SIBLING (word match) {rel}:{ln}: {surface} {citation!r} shares only the word(s) "
            f"{', '.join(repr(t) for t in shared)} with changed {kind} {entry!r} and has no row in "
            f"{REGISTER_REL}; weak evidence"
        )
    lines.append(
        f"D15 SIBLING-PROBE: {len(strong) + len(weak)} unregistered alignment-table citation(s) in "
        f"the corpus share a distinctive token with the {len(changed)} alias key(s) or register "
        f"Standard ID(s) this PR changes: {len(strong)} share an acronym, designator or number "
        f"(D15 SIBLING) and {len(weak)} share only a distinctive word (D15 SIBLING (word match), "
        f"weak evidence: a word such as \"pipeline\" names many instruments); check each for another "
        f"form of the same instrument. Residual, not listed: a form sharing no distinctive token "
        f"with a changed entry (\"Law 25\" beside \"Quebec Law 25\", or a spelled-out name beside "
        f"its acronym that shares no distinctive word with it, such as one sharing only stop words "
        f"or family tokens: \"Cloud Security Alliance Cloud Controls Matrix v4.1\" beside \"CSA "
        f"Cloud Controls Matrix\"); every form of a changed entry with no distinctive token (NOTE lines "
        f"above); a form sharing only a family token (in {FAMILY_ROWS} or more Standard IDs of "
        f"this register: {', '.join(sorted(family)) or 'none'}), such as \"NIST SP 800-57\" beside "
        f"\"NIST SP 800-218\"; a sibling outside the three alignment-table surfaces (prose, an "
        f"EU/EC number, another table); and siblings of umbrella, not_citable or agency_labels changes. A listed "
        f"citation can be another instrument from the same publisher, and a word match often is. "
        f"Report only; exit 0."
    )
    return lines


def run_sibling_probe(merge_base: str, head: str, register_text: str) -> None:
    """The report-only whole-corpus sibling probe; prints only, never affects the exit."""
    try:
        texts = dict(
            base_aliases=git_show(merge_base, ALIASES_REL), head_aliases=git_show(head, ALIASES_REL),
            base_register=git_show(merge_base, REGISTER_REL), head_register=git_show(head, REGISTER_REL),
        )
        names = git("ls-tree", "-r", "--name-only", "-z", head).split("\0")
        docs = ((rel, git_show(head, rel)) for rel in sorted(n for n in names if n and in_scope(n)))
        lines = sibling_report(texts, register_text, ((rel, text) for rel, text in docs if text is not None))
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:  # PolicyError, RegisterError, JSON
        print(f"D15 NOTE: sibling probe cannot read the alias file, the register or the corpus ({exc}); skipped.")
        return
    for line in lines:
        print(line)


def run(base: str | None, head: str, register_ref: str | None) -> int:
    try:
        merge_base, head = resolve_pr_range(base, head)
    except PrRangeError as exc:
        print(f"D15 NOTE: {exc} Advisory check skipped (fail-open).")
        return 0
    try:
        register_text = subprocess.check_output(
            ["git", "show", f"{register_ref or head}:{REGISTER_REL}"],
            text=True, stderr=subprocess.DEVNULL,
        ).rstrip("\n")
    except subprocess.CalledProcessError:
        print(f"D15 NOTE: {REGISTER_REL} is absent at {register_ref or head}; nothing to check against.")
        return 0
    try:
        names = git("diff", "--name-only", "--no-renames", "-z", merge_base, head).split("\0")
    except subprocess.CalledProcessError as exc:
        print(f"D15 NOTE: git diff failed ({exc}); advisory check skipped (fail-open).")
        return 0
    probe = bool({ALIASES_REL, REGISTER_REL} & set(names))
    try:
        resolver = build_resolver(register_text)
    except (OSError, ValueError) as exc:  # PolicyError, RegisterError and JSON errors
        print(f"D15 NOTE: cannot load the register or the D15 policy files ({exc}); advisory check skipped (fail-open).")
        # The probe reads the head's alias file, so a checkout without one (a PR that deletes
        # it) still reaches the probe.
        if probe:
            run_sibling_probe(merge_base, head, register_text)
        return 0
    files = sorted(n for n in names if n and in_scope(n))
    hits = []
    for rel in files:
        try:
            diff = git("diff", "-U0", "--no-renames", merge_base, head, "--", rel)
            text = git("show", f"{head}:{rel}")
        except subprocess.CalledProcessError:
            continue  # deleted in the PR: nothing added
        for ln, surface, citation in scan_text(text, added_lines(diff), resolver):
            hits.append((rel, ln, surface, citation))
    if not hits:
        print(f"D15 OK: {len(files)} corpus document(s) changed; no added citation lacks a register row.")
    for rel, ln, surface, citation in hits:
        print(f"D15 WARN {rel}:{ln}: {surface} {citation!r} has no row in {REGISTER_REL}")
    if hits:
        print(
            f"D15 ADVISORY: {len(hits)} added citation(s) with no register row. Add a row (see the "
            f"register's Maintenance section), curate an alias in "
            f"tools/{ALIASES_PATH.name}, or, for an RFC, vendor guidance or a book, an entry in "
            f"tools/{EXCLUSIONS_PATH.name}. Warning only; exit 0."
        )
    if probe:
        run_sibling_probe(merge_base, head, register_text)
    return 0


def main(argv: list[str] | None = None) -> int:
    class AdvisoryParser(argparse.ArgumentParser):
        def error(self, message):
            raise PolicyError(f"argument error: {message}")

    try:
        ap = AdvisoryParser(description="D15: advisory alignment-citation register check.")
        ap.add_argument("base", nargs="?", default=None, help="base ref (default: origin/$GITHUB_BASE_REF)")
        ap.add_argument("head", nargs="?", default="HEAD", help="head ref (default: HEAD)")
        ap.add_argument(
            "--register-ref", default=None,
            help="read the register at this ref instead of the head (replays an old PR against today's register)",
        )
        args = ap.parse_args(argv)
        ensure_gate6()
        return run(args.base, args.head, args.register_ref)
    except Exception as exc:
        print(f"D15 NOTE: {exc}; advisory check skipped (fail-open).")
        return 0


if __name__ == "__main__":
    sys.exit(main())
