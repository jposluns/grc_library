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
edition pins are advisory. In report mode exactly two kinds of finding block:
those of the established Markdown stale check and a historical exception
declaration that does not bind (below); every other finding is advisory. A run
also fails on errors that are not findings: a failure of the unpinned ratchet
below where a project holds one, a malformed input or a failed base read
(below), and the register and input errors in the last paragraph. Explicit
enforce mode additionally blocks those recognized citation findings; PR1 gate
invocations do not enable it.

A project may hold a per-standard ratchet on missing edition pins: a
checked-in baseline of each standard's unpinned count, which may only fall.
A default-scope run fails when a standard's count is above its baseline,
naming the standard and both counts, and when a baseline is above the count,
so the baseline is lowered in the change that pins the citations. The same
run compares the baseline with its copy at a base revision and fails when an
entry is above its base value, or is new while the base register already lists
that standard; a new entry comes only with that standard's new register row,
and no higher than that standard's unpinned count at the base, and a row with
a base entry is not removed in the same change. One function selects the base
from authoritative inputs, resolving each ref by its exact full name and
passing only the resolved object onward: for a pull request, the first parent
of the checked-out merge commit, of which the event's stated base must be an
ancestor or the commit itself; for a push, the event's previous tip, which
must be a proper ancestor of the pushed commit; for a scheduled or manual run,
and for every local run, the merge base with the fully qualified main-branch
remote-tracking ref. A run is a CI run only when the CI flag
(`GITHUB_ACTIONS`) is exactly the string `true` and the event file
(`GITHUB_EVENT_PATH`) names a readable file holding an object; when the flag
is exactly `true` and the event file is unset, missing, unreadable or not an
object, the run fails closed, and a run with any other flag value, or none, is
local. A missing, unreadable or malformed baseline fails. The base read fails
closed on a project root that is not the top of a work tree, a shallow
repository, a CI run whose event file is unset, missing, unreadable or not an
object, a CI event with no base rule, an event that names no valid commit, a
pull request base that is neither the first parent of the checked-out merge
commit nor an ancestor of it, a checked-out commit that does not have exactly
two parents in a pull request run, a push's previous tip that is not a proper ancestor of
the pushed commit, a missing ref, zero or several merge bases, a failing git
call, a base whose register or baseline cannot be read, and a base whose
default-scope files cannot be read where its counts are needed; a base with no
baseline fails too, except the one bootstrap: a base that predates the ratchet,
that is, one with no baseline whose copy of the gate exists and does not yet
hold the ratchet. A base with no baseline and no copy of the gate fails
closed, and so does a base with no baseline whose copy of the gate holds the
ratchet. That bootstrap holds the seeded baseline to the live
counts and to each standard's unpinned count at the base, read from the base
revision's tree through version control with the same predicate, so seeding
cannot raise a count. Every git call the ratchet makes (the work-tree and
shallow checks, the refs, the base and the parent, the commit and ancestry
checks, and the tree and blob reads) goes through one helper, so git cannot substitute an
object or a parent for the ones the object ids name. Its environment is an
allowlist built from nothing: of the inherited variables only `HOME`, which
git needs to find its global configuration, is passed on, and every other one
is absent, so no `GIT_` variable can point git at another repository or
substitute an object (`GIT_DIR`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`,
`GIT_REPLACE_REF_BASE` and `GIT_GRAFT_FILE` among them) and no `LD_PRELOAD`
or `LD_LIBRARY_PATH` reaches git. To that it adds only
`GIT_NO_REPLACE_OBJECTS=1` (no replace ref substitutes an object),
`GIT_GRAFT_FILE=/dev/null` (the repository's `info/grafts`, which git still
honours, is not read), `GIT_CONFIG_NOSYSTEM=1` (the system configuration is
not read), `LC_ALL=C` and the fixed search path below as `PATH`. Every
call also passes `-c core.commitGraph=false`, so the commit-graph file cannot
substitute a commit's parents. The helper runs git by absolute path: git is
resolved once on the fixed search path `/usr/local/bin:/usr/bin:/bin`, never
the inherited `PATH`, and the child's `PATH` is set to that same value, so a
substitute git earlier on the caller's `PATH` is not run; no git there fails,
naming the searched path. A shallow file is not harmless: it can hide a
commit's parents and so move the merge base to an older commit. Before any
base is computed the ratchet asks git, through the helper
(`rev-parse --is-shallow-repository`), and a shallow repository fails with a
message that the base cannot be computed in a shallow clone and that full
history must be fetched. A failing call's message shows git's error output
without its advisory hint lines (`hint: ...` and a bare `hint:`, with or
without a trailing space), so a deprecation hint cannot hide the real error.
Disclosed residuals, in this order: a local process that controls the
environment (the CI flag, `HOME` and the global configuration it locates,
the variables the interpreter reads, or any other), the git executable on the
fixed search path, or the event file is not defended against, because with
`HEAD` these choose the base and what git reports of it; CI is the defended
path. A local caller can move or recreate the main-branch remote-tracking ref; edits
to the gate, the CI workflows, the audit runner or the pre-commit invocation
can change or remove the ratchet, and review of such an edit is the control;
and the base count uses the head register, so a register edit in the same
change can change which citations count. Each text run states its totals of
unpinned and unregistered citations; a machine-readable run carries them in
its report.

Ambiguous identities, broader discovery candidates and unresolved editions
remain explicit review inventories. An unrecognized edition is not declared
current or superseded. Final and compound register cells do not automatically
authorize bare citations. Exceptions require explicit project policy and
evidence.

A superseded edition cited as history, rather than as a current reference, is
the one sanctioned exception form. The project wrapper reads it from a reviewed
machine-readable data file, parsed strictly (valid structured data, exactly the
declared fields, typed values, every string single-line printable ASCII with
no doubled space, rows
unique by identifier and by path, sentence and citation); a human-readable page
shows the rows in a table generated from the data, and the wrapper refuses a page
whose generated table differs, whose table does not stand alone, or that carries
a line ending other than LF, front matter, raw HTML, a comment, a fence marker,
math markup, an image, a table or a pipe character outside it. The page can
never change what is sanctioned, and no table drawn in Markdown, HTML, math or
an image can appear beside the generated one; prose or an indented block that
imitates a row, or an emoji shortcode that renders as a glyph, is not
detected, so review of the page is the control. Each
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
