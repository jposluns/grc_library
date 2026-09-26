# Standards currency

The project's canonical register supplies citation identities and current and
superseded edition facts. The gate does not query publishers or establish
publisher truth or clause semantics.

The established stale-citation check remains blocking. It matches registered
identifiers followed by registered superseded markers, including v-prefixed
versions, and preserves version-continuation boundaries and fenced-code
exclusion.

P-3.213 PR1 adds register-independent discovery for ISO/IEC-family publications,
NIST publications and frameworks, IEEE, ETSI/CEN, and CIS Controls, ITIL, WCAG,
COBIT and SLSA. Exact normalized identifiers resolve to register rows.
Diagnostic spelling matches suggest corrections but are not accepted aliases.
Parts, publication kinds and issuer identities remain distinct.

Report mode is the default during migration. Newly discovered stale forms,
HTML findings, missing registrations, noncanonical identifiers and missing
edition pins are advisory. Only the established Markdown stale check blocks
in report mode. Explicit enforce mode additionally blocks those recognized
citation findings; PR1 gate invocations do not enable it.

Ambiguous identities, broader discovery candidates and unresolved editions
remain explicit review inventories. An unrecognized edition is not declared
current or superseded. Final and compound register cells do not automatically
authorize bare citations. Exceptions require explicit project policy and
evidence.

A superseded edition cited as history, rather than as a current reference, is
the one sanctioned exception form. The project wrapper reads it from a reviewed
machine-readable data file, parsed strictly (valid structured data, exactly the
declared fields, typed values, every string single-line printable ASCII with
no doubled space or emoji shortcode, rows
unique by identifier and by path, sentence and citation); a human-readable page
shows the rows in a table generated from the data, and the wrapper refuses a page
whose generated table differs, whose table does not stand alone, or that carries
a line ending other than LF, front matter, raw HTML, a comment, a fence marker,
math markup, an image, a table or a pipe character outside it. The page can
never change what is sanctioned, and no table drawn in Markdown, HTML, math or
an image can appear beside the generated one; prose or an indented block that
imitates a row is not detected, so review of the page is the control. Each
declaration names one path, one verbatim sentence, one registered
superseded citation written exactly once in that sentence, a reason and
upstream evidence (an https URL naming a host, with no credentials). The wrapper screens the declared text against a
present-tense vocabulary and requires a historical cue; this is a heuristic on
the declared text only, and review of each row is the control. The engine
binds a declaration only where its sentence occurs exactly once on a non-code
line of that file, ends with a sentence terminator (not an abbreviation's),
contains no other sentence or clause break, and stands as its own paragraph
there: the whole line from column 1, not a list item, heading, quotation, table
row or indented block, and with a blank line (spaces and tabs only, or the
file boundary) above and below. The sentence is plain ASCII text: letters,
digits, spaces and the marks . , ; : ' " ( ) / % - only, so no markup, escape,
character reference or lookalike letter can change what renders or what the
screen reads, and a closing quote or bracket
after a terminator still counts as a break. Nothing binds in a file that
carries raw HTML or any HTML comment, a line the line model reads as a fence
(after any leading whitespace) other than a three-character fence at column 1,
with no backtick in a backtick fence's info string, closed by a bare line of
the same character, or a line
separator other than LF or CRLF in its untranslated bytes; each such
declaration is a blocking finding. It then removes only the finding at the one
occurrence written exactly as the declared citation, reading the original text
for discovery, so every other citation, including another written form of the
same edition, is checked unchanged: the established check still blocks it, and
a discovery-only stale form stays advisory in report mode. Sanctioned
citations are reported as their own inventory. A declaration that does not
bind is a blocking finding in every mode, a default run refuses one that names
a file outside its scan scope, and an absent register sanctions nothing; a
malformed or empty canonical register, or a malformed historical register,
fails.

The project wrapper owns the register schema, publication surfaces, exclusions
and exception reasons. Malformed or empty registers fail; missing or unreadable
intended inputs are environmental errors. Reports include counts and every
finding location, and do not claim cleanliness while review items remain.
