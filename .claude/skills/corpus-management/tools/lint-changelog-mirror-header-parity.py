#!/usr/bin/env python3
"""CHANGELOG detailed-mirror per-PR header-parity audit (gate 59).

The change-tracking discipline keeps two CHANGELOG surfaces in lock-step:
the adopter-facing root ``.working/CHANGELOG.md`` (compact one-line ``date | version | PR`` entries) and
the maintainer-grade detailed mirror (full structured entries,
resolved from the operational store). Delta check D1
enforces, per commit, that a PR touches the root ``.working/CHANGELOG.md`` (the
detailed mirror lives in the operational store, cross-repo and outside the
public diff, so D1 does not require it); it does NOT check that the two carry
the SAME set of per-PR
entry headers (matched in BOTH the compact ``**date | version | PR #N**``
form and the legacy ``## YYYY-MM-DD, Library Version X, PR #N`` form). That cross-commit
integrity is gate-blind: a later PR's commit can overwrite an earlier
PR's detailed-mirror header in place, orphaning the earlier bodies under
the wrong header.

This gate closes that gap: it parses the per-PR header set from each
file and requires them to match, so a lost or duplicated detailed-mirror
header fails the build instead of surfacing only at a later manual sweep.

It also asserts CROSS-FILE VERSION AGREEMENT: a PR present in
BOTH files must carry the SAME ``Library Version`` in each. Set parity plus
per-file monotonicity left this gate-blind, because two files can each be
independently monotonic while disagreeing on one shared PR's version: the
root ``.working/CHANGELOG.md`` can carry one version for a PR while the detailed
mirror carries another, and set parity and monotonicity both still pass. Every compared header carries a parseable
``X.Y.Z`` version (entry classification, below, fails any other), and a PR
duplicated within one file is already caught by the duplicate check rather
than by this join. The 2 version texts must also be identical, so
``2026.06.9`` in one file against ``2026.6.9`` in the other disagrees.

It also asserts Library-Version ORDERING: entries
are newest-first, so within each file the cutoff-scoped headers'
``Library Version`` values must be STRICTLY DECREASING top-down (the
change-tracking rule's "version numbers across CHANGELOG entries
strictly increase in the order the entries appear" stated for a
reverse-chronological file). Versions compare as integer tuples, never
strings (``2026.06.9`` above ``2026.06.10`` is a violation a string
compare would miss). This is the CHANGELOG version-monotonicity control
the change-tracking rule describes; gate 13 deliberately skips
.working/CHANGELOG.md (no ``Version`` metadata field), so without this check
the described control would exist nowhere.

Repository epoch (the rename to the new repository, ``EPOCH_START`` =
2026-11-09). Pull-request numbers restarted at #1 on that date, while the old
repository's records carry numbers up to #3127, so a PR number alone no longer
names one pull request. The gate therefore reads dates as well as numbers:

- ``CUTOFF_PR`` is 1 and no dynamic floor applies: a line is compared in both
  files when it fully matches a comparison shape at column 0, is dated on or after
  ``EPOCH_START``, carries a version at or above ``VERSION_FLOOR`` and passes the
  rest of entry classification (below); a compared mirror header leaves the
  comparison only through the deferral exception, with a printed note. The old
  repository's cutoff, its dynamic floor and its historical exemptions belong to
  that repository's archived history and do not apply here.
- Root grammar. The root ``.working/CHANGELOG.md`` is read by a grammar of
  line shapes, not by pattern detection alone; ``main`` removes at most 1 leading byte order
  mark (U+FEFF), once, before the root is read (``root_findings`` removes none, so a
  second one stays in line 1, where the strict character rule refuses it), and the root is
  split into lines on LF only (``lf_lines``): a CR before an LF
  is part of the line ending, and a vertical tab, a form feed, U+001C to U+001E, U+0085,
  U+2028 and U+2029 stay in their line, so the strict character rule refuses each and line
  numbers count as an editor counts them; ``pr_headers`` reads the root over the same LF-only
  split, so its line numbers match the rule's. Strict character rule (an allowlist rather than
  a list of refused forms, because Markdown forms keep appearing that can hide a CalVer version
  in the root, such as GitHub inline math in ``$2026$.11.67``): every root line that is not blank (the title, the
  intro, the weekly bullets and headings, and the canonical lines with their summary tails)
  may hold only these characters of printable ASCII (U+0020 to U+007E): ASCII letters, digits,
  the space and ``.``, ``,``, ``:``, ``;``, ``-``, ``'``, ``"``, ``(``, ``)``, ``/``, ``#``,
  ``|``, ``&``, ``%``, ``+``, ``?``, ``!``, ``=`` and ``@`` (``ROOT_ALLOWED_CHARS``), and
  ``*`` only as the 2 bold delimiters of a canonical header (its leading ``**`` and the ``**``
  that closes its date, version and PR header). Every other character is refused, among them
  ``$``, ``{``, ``}``, ``^``, ``[``, ``]``, ``<``, ``>``, ``\\``, ``~``, ``_``, the backtick,
  a tab and every character outside printable ASCII, so a renderer syntax this docstring does not
  name is refused unless the allowlist names its characters. No HTML character reference is
  allowed either (an ``&`` followed by a name, by ``#`` and decimal digits or by ``#x`` and
  hexadecimal digits, and then ``;``, such as ``&#46;``, ``&#x200B;`` or ``&amp;``); a plain
  ``&`` is allowed. Each refused character or reference fails the line
  (``root_character_findings``), and the message names its line number, its column (counted
  in characters from 1) and the character, by its code point, or the reference. So no link,
  image, autolink, HTML tag or comment, backslash escape, code span, emphasis,
  strikethrough, inline math, brace group, invisible or control character, look-alike
  character or character reference can split a version in the root, and no backtick or ``*``
  can join a digit to one (``3*2026.06.9``). The intro, weekly-bullet and summary-tail rules
  read each line as
  written: nothing is removed first (removing every backtick and every emphasis marker
  before the read would join ``3*2026.06.9`` into ``32026.06.9``).
  Above its first ``## Week of`` heading (the whole
  file when it has none) it must hold only these lines: the ``# Changelog`` title, which must be
  its first non-blank line (a root without it fails, and so does a canonical
  per-PR line placed before it); the intro paragraph
  directly after the title (blank lines may come between), each of whose lines starts with a
  letter and holds no date-like token, no ``X.Y.Z`` version, no CalVer library version
  (``CALVER_RE``, below) and no numbered PR identity: a labelled PR identity (``PR`` or ``PRs``
  with a number, after an optional ``-``, ``:``, ``.``, ``no.``, ``number`` or ``#``, so
  ``PR #N``, ``PR N``, ``PRN``, ``PR-N``, ``PR: N`` and ``PR no. N`` among them; ``GH-N``;
  ``owner/repo#N``; ``grc_library#N``, where the bare form names only the repository's own
  name, so ``issue#42`` is not a PR identity; ``pull N``, ``pull request N``,
  ``pull-request N`` or a ``pull/N`` URL) or a bare ``#N``; blank lines
  (empty, or holding only
  spaces and tabs); and canonical per-PR lines, ``**YYYY-MM-DD | X.Y.Z | PR #N**`` at column 0,
  optionally followed by ``" - <summary>"``, with a valid ASCII ISO date, a parseable ``X.Y.Z``
  version and exactly 1 PR number of ``CUTOFF_PR`` (1) or more. A canonical line in the root
  whose summary tail holds a CalVer library version fails too (every per-PR record
  carries one, so the tail would carry a record unread); a non-CalVer ``X.Y.Z`` such as
  ``1.0.2`` is allowed there. In the mirror a canonical line whose summary tail holds an
  ``X.Y.Z`` version and a labelled PR identity naming a number other than the header's PR
  fails. Header parity compares only the PR number and the version of a
  canonical line, not the whole line, so every mirror canonical line (a mirror line that
  fully matches the compact comparison shape) meets the same strict character rule as a root
  line, must end at an LF (a line that ``splitlines`` ends at another line boundary fails at
  that character's column), and has its summary tail read as written, as the root reads its
  lines. The tail gets no second read: no link scan and no normalization (no
  character-reference decoding, no removal of format, control or default-ignorable
  characters and no NFKC). Any other line in that region
  fails: with the specific failure of the mirror rules below when they also fail it, otherwise
  as an old-repository record when its first date is before ``EPOCH_START``, and otherwise as
  outside the root grammar, with a message naming the canonical shape (a legacy ``##`` header,
  a milestone, a weekly roll-up bold line, a table row, a second prose paragraph and an intro
  line holding a version or a PR identity all fail there). A canonical per-PR line is compared
  only when it is dated on or after ``EPOCH_START`` and carries a version at or above
  ``VERSION_FLOOR``; otherwise it fails as below. At and below the first ``## Week of`` heading
  the root must hold only ``## Week of YYYY-MM-DD`` headings with a valid date, blank lines and
  ``- `` bullets that hold no CalVer library version (whether or not a date or a
  labelled PR goes with it): no ``CALVER_RE`` token, an optional
  ``v`` or ``V``, then ``20`` and 2 digits, a dot, 1 or 2 digits, a dot and digits, read after
  the root read. Every per-PR record carries one. A non-CalVer ``X.Y.Z`` such as ``1.0.2``
  or ``4.0.3`` is allowed, so ``- OWASP ASVS references moved from 4.0.3 to 5.0.0 after the
  review in PR #1.`` passes. A line that fully matches a comparison shape fails as
  a per-PR line below the weekly summaries
  (per-PR lines belong only to the current week), a weekly heading with an invalid date fails
  as unparseable, and every other line fails with a message naming the allowed lines.
- Mirror classification reads every
  line of the detailed mirror raw and fails closed for each line it detects; it detects entries
  by content, so, unlike the root grammar, it is open-ended. A table row (a line whose first
  character other than a space or a tab is ``|``) is skipped. Before detection inline code spans
  are removed and Markdown link syntax is flattened, so ``[text](url)`` reads as its link text
  and its URL. For the opening rules a date-like token is 3 runs of digits joined by ``-`` or
  ``/``, such as ``2026-11-9``, ``2026/11/10`` or ``2026-06-21``, read Unicode-wide; an ``X.Y.Z``
  token joined by dots is not date-like there. A line is an entry candidate in any of 3 ways:

  - by content, in any order: the line holds 3 separate tokens, in
    any order and with any separators (spaces, colons, slashes, commas, ``|`` and others): a
    date-like token (3 runs of digits joined by ``-``, ``/`` or a Unicode dash from U+2010 to
    U+2015, a ``T`` time suffix allowed; a year-first date joined by dots with a month of 1 to
    12 and a day of 1 to 31, such as ``2026.11.10``; a day-first date joined by dots with a day
    of 1 to 31, a month of 1 to 12 and a 4-digit year, such as ``10.11.2026``, which a
    ``YYYY.MM.patch`` version cannot match; a day and a month name with a year, joined by
    spaces, such as ``10 November 2026``, ``21 Jun 2026`` or ``November 10, 2026``, or by
    those dashes, such as ``10-Nov-2026`` or ``2026-Nov-10``; or the 8-digit form
    ``20261110``), an ``X.Y.Z`` version (with or without a
    ``Version`` or ``Library Version`` label, a leading ``v`` or a suffix such as ``-rc1``) and a
    numbered PR identity (a labelled PR identity as in the root grammar above, such as ``PR #N``,
    ``PR: N``, ``PR no. N``, ``PR number N``, ``PRN``, ``GH-N``, ``owner/repo#N``,
    ``pull-request N`` or a ``pull/N`` URL, or a bare ``#N``). Emphasis markers are
    removed first, so ``__2026.11.67__`` reads as a version. A dot-joined token read as both the
    date and the version counts once, so
    ``Version 2026.11.10, PR #2`` alone is not a candidate;
  - by a leading triple (``TRIPLE_RE``): after an opening of markup only, the line starts
    with a date-like token, an ``X.Y.Z`` version and a PR cell that may be a bare number closing
    its cell (``- 2026-11-10, Version 2026.12.2, 2``);
  - by its canonical opening: it starts at
    column 0 with ``## ``, ``**`` or ``- **``, and its heading text (after ``## ``) or its first
    bold span (after ``**`` or ``- **``) starts, after optional spaces, with ``Week of`` or with
    a date-like token that ends that text or is followed, after optional spaces, by ``,`` and
    then a ``Version`` or ``Library Version`` label, an ``X.Y.Z`` version or a numbered PR
    identity (``PR #N``, ``PR N``, ``PRs #N``, ``pull N`` or ``#N``) that ends that text (an
    optional ``:`` or ``.`` aside) or is followed by ``,`` or ``|``, or by
    ``|`` and then an
    ``X.Y.Z`` version or ``MILESTONE:``, the cell joints of the 2 comparison
    shapes and the milestone form (``## 2026-11-10, Library Version ...``,
    ``**2026-11-10 | 2026.11.67 | ...**`` and ``**2026-11-10 | MILESTONE:**``), or that text
    holds a ``|`` cell
    separator together with an ``X.Y.Z`` version or a numbered PR identity (``PR #N``,
    ``PR N``, ``PRs #N``, ``pull N`` or ``#N``) that ends its cell (an optional ``:`` or
    ``.`` aside), the cell form of the compact shape
    (``**PR #5 | 2026.12.5**``).

  Every other line is not a candidate: a line without the full date, version and PR triple
  and without a canonical opening is a body line, so
  ``**Supersedes PR #1:** reverted on 2026-11-10.``, ``**Follow-up to PR #1:** none.``,
  ``**Ruling 2026-11-09:** applied.``, ``**Before | after:**``,
  ``- **2026-11-10:** the maintainer ruled.``, ``**2026-11-10 follow-up:** none.``,
  ``- **2026-11-10, 17:07Z:** the maintainer ruled option B.``,
  ``**2026-11-10 | review:** done.``, ``**2026-11-10, PR #1 follow-up:** none.``,
  ``**2026-11-10 | PR #1 review:** done.``,
  ``## Ruling of 2026-11-10``, ``## Follow-up for PR #1`` and
  ``**Gate 59 | 2026-11-10 review:** done.`` pass. The bold milestone form behind a markup-only opening
  (``* **2026-07-29 | MILESTONE:** split landed in PR #3127.``) is a candidate too, and the
  milestone exemption never excuses it. A body line that holds all 3 tokens, such as
  ``- Corrects the 2026-11-09, Library Version 2026.11.66, PR #1 header.``, is a candidate by
  content and fails; a record quoted in an inline code span or a table row is not read.
- A candidate by content, by a leading triple or as a milestone behind an opening that is not
  a column-0 full match of a
  comparison shape always fails, and the exempt shapes never excuse it: as an old-repository
  record when its first date is before ``EPOCH_START``; otherwise, when it is not a candidate by
  its opening, with the message naming the expected shapes, and when it is, by the rules below
  (each of which fails it).
- An entry candidate must fully match one of the 2 comparison shapes,
  ``**YYYY-MM-DD | X.Y.Z | PR #N**`` (optionally followed by ``" - <summary>"``)
  or ``## YYYY-MM-DD, Library Version X.Y.Z, PR #N`` (the bare ``Version``
  label of the mirror's older entries reads as the same shape), with a valid
  ASCII ISO date (read with ``datetime.date.fromisoformat``), a parseable
  ``X.Y.Z`` version and exactly 1 PR number of ``CUTOFF_PR`` (1) or more, with no leading zero in
  the PR number or in a version part apart from a 2-digit month (``2027.01.5``, the CalVer
  ``YYYY.MM.patch`` form), so ``PR #02`` and ``2026.11.067`` fail; or it
  must fully match one of the named exempt shapes: a ``## Week of YYYY-MM-DD``
  heading, an old weekly roll-up bold line ``**Week of YYYY-MM-DD (PRs #A-#B)**``,
  or the bold milestone form ``**YYYY-MM-DD | MILESTONE:**``, whether or not its
  text names a PR. Every other entry candidate fails with a message naming the
  expected shapes; no candidate passes unread.
- A candidate is an old-repository record, and fails with a message naming it as a record to
  archive, only when its first date is a calendar date before ``EPOCH_START``. The first date is
  the first year-first date joined by ``-`` or ``/`` (in any cell, with 1-digit or 2-digit months
  and days); when the line has none, the first date in any other form the content rule reads
  apart from a dot-joined year-first date (a date joined by a Unicode dash, a day-first date
  with a 4-digit year joined by ``-``, ``/`` or dots, a day and a month name with a year joined
  by spaces or dashes, or the 8-digit form), so
  ``### 21-Jun-2026 | 2026.06.9 | PR: 3127`` names ``21-Jun-2026``; and when it has none of
  those, the first dot-joined year-first date. A later date on the line (``reverts the 2026-11-02
  change``) does not make it one. A milestone dated before ``EPOCH_START`` is one too. The 2
  weekly shapes are exempt whatever their date when they match in full with a valid date; a
  ``## Week of`` heading or a bold ``Week of`` line with a date that is not a valid calendar date
  fails as unparseable, and a bold ``Week of`` line that does not match the roll-up shape fails
  as an old-repository record when its first date is before ``EPOCH_START`` and otherwise as
  unreadable. A date that is not a valid ASCII ``YYYY-MM-DD`` calendar date fails as
  unparseable only in a line that matches a comparison shape, a weekly shape or the milestone
  form in full, or as the date-like token right after a candidate's marker; anywhere else, as in
  ``- 2026/11/09 | 2026.11.66 | PR #1``, the line fails with the message naming the expected
  shapes. A legacy line that names more than 1 PR (``PR #1 and PR #2``) fails
  with the message that one header per PR is required. Every comparison shape needs a PR number
  of 1 or more with no leading zero, so a line naming ``PR #0`` (below ``CUTOFF_PR``) matches no
  comparison shape and fails with the message naming the expected shapes.
- ``VERSION_FLOOR`` is ``2026.11.66``, the first version shipped by a new-repository PR (main
  starts at 2026.11.65). A line that fully matches a comparison shape with a valid date on or
  after ``EPOCH_START`` but carries a version below ``VERSION_FLOOR`` is an old-repository
  record and fails, whatever its date (an old record dated on the epoch day itself cannot be
  told from a new one by its date).
- Residuals. The root grammar closes its line shapes: every root line is the title, an intro
  line, a blank line, a canonical per-PR line, a ``## Week of`` heading or a ``- `` bullet, or it
  fails. 3 of its rules depend on token detection, so they are only as complete as their
  detectors: an intro line passes when the date-like, ``X.Y.Z`` version, CalVer version and PR
  identity detectors find nothing in it, and a ``- `` bullet below the first ``## Week of``
  heading or a canonical line's summary tail in the root passes when ``CALVER_RE`` finds nothing
  in it, each read as written. Every per-PR record carries a CalVer library
  version, and the strict character rule allows only the characters it names, so it leaves no
  character or reference that renders invisibly or as another character and no link, tag,
  escape, code span, emphasis, inline math or brace group that could split one or join a digit
  to one; a record in an intro line, a weekly bullet or a root summary tail passes unread only
  when its version is written in allowlisted characters that ``CALVER_RE`` misses as written,
  such as a version split by a space, which does not render whole, or a renderer syntax made
  only of allowlisted characters, such as a GitHub emoji shortcode (``:one:``), which the rule
  does not model. The rule also restricts what an author may write in the root: every
  character outside the allowlist (a link's brackets, an underscore, ``grc_library`` among
  them, an angle bracket, a backslash, a tilde, a backtick, a dollar sign, a brace, a caret, a
  tab and every character outside printable ASCII), a ``*`` other than a canonical header's
  bold delimiters and a character reference all fail there, so such text must be written
  another way (a bare URL, plain words) or kept out of the root; a file reference there is
  written as plain text,
  without backticks, so gate 11, which requires a backticked file reference in the root to be
  a Markdown link, finds none there. The same restriction holds every mirror canonical line,
  whose summary is written in the same plain form; a mirror canonical line that does not meet
  it fails and is left out of the comparison. The mirror rules are open-ended: a mirror entry that has no canonical opening and lacks one of the 3 tokens (a date written without a
  year or only in words, a version that is not ``X.Y.Z``, or a PR named only in words or as a
  bare number away from the start of the line), that sits in a table row or an inline code span,
  or that is in any other shape none of the 3 candidate rules reads, is not detected. A
  mirror-only entry in such a shape passes unread; a root entry whose mirror counterpart is
  written in such a shape fails as missing from the mirror. The content rule can also fail a
  body line that holds a date, a version and a PR identity for another reason (a section number
  such as ``6.1.2`` reads as a version, and a version such as ``2026.12.5`` also reads as a
  dot-joined date).
- Classification runs on both raw surfaces before store-scope deferral, so an
  old or unreadable record (by date or by ``VERSION_FLOOR``) can never be
  deferred into a silent pass, and failing
  lines are left out of the comparison. The deferral exception for open PRs
  applies only after it: store scope may defer a mirror header that fully
  matches a comparison shape and names another open PR, each with a printed
  note; it never exempts a line from classification. Old records must be
  archived out of both surfaces (the mirror's go to the private
  ``changelog-archive/``).
- A root or mirror file that cannot be read or is not valid UTF-8 fails the
  gate, naming the file, rather than reading as empty text.

PR numbers cited below without further qualification are old-repository PRs;
they record why each rule exists.

No floor in the new repository. The old repository scoped the comparison
to ``max(CUTOFF_PR, oldest PR still in the mirror)``, because its root kept
every per-PR line while its mirror kept only the current week. That floor let a
root header with no mirror entry pass whenever the mirror held only a higher or
open PR, and let a dropped oldest mirror entry pass with no notice. In the new
repository the root keeps per-PR lines only for the current week, as the mirror
does: one coupled close-out rolls a completed week up into a summary line in the
root and sweeps the same week from the mirror to the pushed
``grc_library_private/changelog-archive/``. Every compared header (see entry
classification above) is therefore compared in both files, and a root header
with no mirror counterpart fails whatever the mirror's oldest entry is. (Doing
only the root roll-up, leaving the mirror full, fails whenever the mirror's
swept entries stay evaluated: when origin/main's commit subjects carry merge
evidence for a swept PR (a squash ``(#N)`` or a ``Merge pull request #N``
subject), when origin/main's root headers name it, or when the git evidence
(the merge-base changelog, origin/main's changelog or origin/main's log) cannot
be read, or no declaration or clean-base scope is established, so no entry
defers. Only when scope is established and none of that evidence protects a
swept PR does store scope defer its mirror entry as an open PR, with a printed
note. The coupled tool prevents a root-only roll-up.) Historical parity for
swept weeks moves to git history and to the private-sibling archive.

The ordering assertion reuses the same scope. The old repository's only
non-decreasing pairs (its 2026-06-21 window) are dated before ``EPOCH_START``,
so they fail as old-repository records rather than as ordering violations, and
no second baseline constant is needed.

Store scope (maintainer ruling 2026-09-30 17:07Z, option B, simplified 21:03Z;
clean-base allowed 2026-10-22 01:29Z; shared with gate 50 through
``lint_common.store_scope``). The detailed mirror lives
in the operational store every open branch shares, so another open PR's in-flight
mirror entry would otherwise read as MISSING from this branch's root. A mirror
record defers only when all of these hold: this branch has a clean-base scope (see
below) or declares its own PR (the
single new singular root header naming a PR absent from the merge-base root
headers, from origin/main's root headers and from origin/main's ``(#N)`` and
``Merge pull request #N`` commit subjects; no other ref is consulted, and
historical edits, roll-ups, a merged PR's header, a second new identity, a
combined identity, an unparseable or unrecognized new header, and a fence or
comment delimiter at or above the candidate declare nothing); the record's key
belongs to its complete, unambiguous raw header identity; and the shared flags
permit deferral, because every named PR exceeds ``max(declared own PR, highest
root header PR)`` or every named PR is another open PR absent from this branch's
root headers and from all of that origin/main evidence. A mirror header naming
the branch's declared own PR is never deferred. One shared,
case-insensitive grammar reads every PR identity and range, and header ranges
protect their interiors. The declared own PR and every PR covered by that evidence remain
evaluated, so a merged PR's mirror entry missing its branch root line still fails.
D1 can accept a ``Changelog: <one-line-reason>`` trailer instead of a root entry,
so it does not guarantee a declaration before merge. A clean-base scope declares
no own PR: the root has a parseable PR ceiling, no new header-like line against the
merge-base, and no delimiters. Store scope reads historical milestone lines
already in the merge-base as no new header-like line, but the root grammar fails any milestone
line in the root, so such a root still fails the gate. Its ceiling is the root maximum. It uses the same
readable origin/main evidence and protects every merged PR. Because the own PR
is unknown under clean-base, a trailer-only PR's own mirror entry defers like
another open PR's until it merges; once origin/main carries its merge subject or
root header it is evaluated again. A branch that adds its own root header
declares instead, and its own entry is evaluated. Neither basis, or an
unreadable merge-base changelog, origin/main changelog or origin/main log,
disables all deferral and prints a note. origin/main is read offline from the
local remote-tracking ref, so a PR merged after the last fetch reads as open; its
deferral is printed like every other. Every deferred header prints its location,
named PRs and reason.

Both surfaces are read raw, without fence or comment masking, and no comparison
floor is computed: a post-epoch header leaves the comparison only when store
scope defers it, and each deferral is printed. An unknown or
ambiguous boundary, a header-shaped line the boundary grammar cannot read, or a
fence or comment delimiter disables further mirror deferral, so example records
and later entries stay evaluated and an unrecognized header is never swallowed
into the deferred entry above it. Open-PR deferral also reaches entries below the
own entry. A plain, unmarked header lookalike is indistinguishable from a real
entry, including inside the own entry, and so is an open PR's header carried onto
a stacked branch that has not yet written its own entry, which declares; both
residues are loud, because every deferral note names the entry and the declared
own PR.

Empty comparison. When the gate compares no PR while a mirror is present (for
example a weekly-only root with no per-PR header, or a mirror holding only
deferred entries), it still exits 0 but also prints the shared ``DEGRADED:``
line through ``lint_common.print_degraded``. The line says that no PR was
compared and gives the number of deferred mirror headers, so an empty
comparison is never read as an attestation of parity. When no store supplies
the mirror, every root check that needs no mirror still runs (the root must be
readable UTF-8, entry classification, and the root's duplicate and
ordering checks), so a bad root fails in public CI too; only the checks that need
the mirror (header parity, version agreement and the mirror's own duplicate and
ordering checks) are skipped, with the same kind of line.

Exit codes:
    0   the per-PR header multisets of the post-epoch headers match, each
        file's Library Versions strictly decrease, and every entry candidate
        fully matches a comparison shape or a named exempt shape and is not
        an old-repository record (with a DEGRADED line when no PR was
        compared or no mirror is present)
    1   one or more headers are missing, extra or duplicated, an entry
        candidate is dated before EPOCH_START, carries a version below
        VERSION_FLOOR, carries an unparseable date, matches no comparison or
        exempt shape at column 0 or names more than 1 PR,
        a Library Version is out of order (equal or increasing top-down), a
        root line above the first ## Week of heading is outside the root
        grammar, a root line at or below that heading is not a ## Week of
        heading with a valid date, a blank line or a "- " bullet that holds
        no CalVer library version, the root does not start with the
        # Changelog title, a root line or a mirror canonical line holds a
        character or an HTML character reference the strict character rule
        refuses, a mirror canonical line ends at a line boundary other than LF,
        a canonical line's summary
        tail holds a CalVer
        library version (root) or names another PR's record (mirror), or
        the root or mirror file cannot be
        read as UTF-8 text
    2   an explicit --root is not a directory holding both inputs
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from collections import Counter
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack .claude/skills/corpus-management/tools/ on sys.path
from aiqt_corpus import read_text_safe  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import REPO_ROOT, changelog_entry_boundary, changelog_header_prs, print_degraded, require_dir, resolve_working, store_deferral_note, store_deferral_flags, store_scope  # noqa: E402  # grc-config/store, stays local

# Paths of the two surfaces, relative to the repository root.
ROOT_CHANGELOG_REL = ".working/CHANGELOG.md"
DETAILED_MIRROR_REL = ".working/changelog-details/CHANGELOG-detailed.md"

# Compare PRs at or above this number. Numbering restarted at #1 on
# EPOCH_START, so every new-repository PR is in scope, and no dynamic floor
# raises it; see the module docstring.
CUTOFF_PR = 1

# The new repository's first day. A dated header-like line dated before it is an
# old-repository record that must be archived; the gate fails on it before any
# deferral is considered.
EPOCH_START = "2026-11-09"
EPOCH_START_DATE = datetime.date.fromisoformat(EPOCH_START)

# The first Library Version shipped by a new-repository PR (main starts at 2026.11.65). A
# line that fully matches a comparison shape with a version below it is an old-repository
# record, whatever its date, and fails before any deferral: a date alone cannot tell an old
# record dated on EPOCH_START from a new one.
VERSION_FLOOR = "2026.11.66"
VERSION_FLOOR_TUPLE = tuple(int(part) for part in VERSION_FLOOR.split("."))

# The shape patterns below (HEADER_RE, COMPACT_HEADER_RE, LEGACY_LEAD_RE, WEEK_HEADING_RE,
# WEEK_ROLLUP_RE, MILESTONE_RE, LOOSE_DATE_RE and PR_TOKEN_RE) are ASCII-only, so a digit
# outside 0-9 (a full-width digit, for example) never reads as part of a date, a version or a PR
# number. The candidate detectors (DATE_LIKE_RE, DATE_ANY_RE, CANONICAL_OPENING_RE and
# LEAD_TOKEN_RE) are Unicode-wide on purpose, so such a line is still a candidate and then
# fails.

# The legacy comparison shape, matched in full:
# "## 2026-11-10, Library Version 2026.11.2, PR #2". The bare "Version" label of the mirror's
# older entries is read as the same shape. Groups: (1) the date, (2,3,4) the version, (5) the PR.
# No leading zero in the PR number or in a version part, apart from the 2-digit
# month of the CalVer YYYY.MM.patch form (01 to 09), so "PR #02" and "2026.11.067" are not
# comparison shapes and fail as candidates.
_SHAPE_VERSION = r"([1-9][0-9]*)\.(0|[1-9][0-9]*|0[1-9])\.(0|[1-9][0-9]*)"
HEADER_RE = re.compile(
    r"^## (\d{4}-\d{2}-\d{2}), (?:Library )?Version " + _SHAPE_VERSION + r", PR #([1-9][0-9]*)$",
    re.ASCII)

# The compact comparison shape (from the root reformat), matched in full, with or
# without the ``- summary`` tail:
# ``**2026-11-10 | 2026.11.67 | PR #1**`` or the same followed by
# `` - <summary>``. Groups: (1) the date, (2,3,4) the version triple, (5) the PR.
COMPACT_HEADER_RE = re.compile(
    r"^\*\*(\d{4}-\d{2}-\d{2}) \| " + _SHAPE_VERSION + r" \| PR #([1-9][0-9]*)\*\*(?: - .*)?$",
    re.ASCII)

# The named exempt shapes, each matched in full with a valid date: a weekly heading, an old
# weekly roll-up bold line with a PRs range, and the bold milestone form (its text may name a
# PR). A weekly shape is exempt whatever its date; a milestone dated before EPOCH_START fails
# as an old-repository record.
WEEK_HEADING_RE = re.compile(r"^## Week of (\d{4}-\d{2}-\d{2})$", re.ASCII)
WEEK_ROLLUP_RE = re.compile(
    r"^\*\*Week of (\d{4}-\d{2}-\d{2}) \(PRs #\d+-#?\d+\)\*\*(?: .*)?$", re.ASCII)
MILESTONE_RE = re.compile(r"^\*\*(\d{4}-\d{2}-\d{2}) \| MILESTONE:\*\*(?: .*)?$", re.ASCII)

# The opening of a legacy-shaped line, used only to report a legacy line that names more than
# 1 PR (``PR #1 and PR #2``) with the one-header-per-PR message.
LEGACY_LEAD_RE = re.compile(r"^## \d{4}-\d{2}-\d{2}, ", re.ASCII)

# The entry-candidate markers of the opening rule: a line that starts at column 0 with "## " (a
# level-2 heading, so "###" and deeper qualify only through TRIPLE_RE), "- **" (a list-item bold
# line) or "**".
CANDIDATE_MARKERS = ("## ", "- **", "**")

# A date-like token: 3 runs of digits joined by "-" or "/", such as 2026-11-9, 2026/11/10 or
# 2026-06-21. Unicode-wide, so a date in full-width digits is a candidate and then fails. An X.Y.Z
# token joined by dots (a version such as 2026.11.66 or a section number such as 6.1.2) is not
# date-like.
DATE_LIKE_RE = re.compile(r"\d+[-/]\d+[-/]\d+")

# A canonical opening: the heading text of a "## " line, or the first bold span of a "**" or
# "- **" line, starts (after optional spaces) with "Week of" or with a date-like token that
# ends the text or is followed, after optional spaces, by "," and a "Version" or "Library
# Version" label, an X.Y.Z version or a numbered PR identity that ends the text (an optional
# ":" or "." aside) or is followed by "," or "|", so "**2026-11-10, PR #1 follow-up:** none."
# is a body line, or by "|" and an X.Y.Z version or "MILESTONE:", the cell joints of the 2
# comparison shapes and the milestone form. A dated note such as "**2026-11-10:** the
# maintainer ruled.", "- **2026-11-10, 17:07Z:** the maintainer ruled option B." or
# "**2026-11-10 | review:** done." or a heading such as "## Ruling of 2026-11-10" or
# "## Follow-up for PR #1" has none, so it is a body line unless it holds a date, a version
# and a PR identity (the content rule) or starts with a comparison-like triple (TRIPLE_RE).
CANONICAL_OPENING_RE = re.compile(
    r"\s*(?:Week of|\d+[-/]\d+[-/]\d+\s*(?:$"
    r"|,\s*(?i:(?:Library\s+)?Version\b|v?\d+\.\d+\.\d+"
    r"|(?:(?:PRs?|pull)\s*#?\s*|#)\d+(?=\s*(?:[,|]|[:.]?\s*$)))"
    r"|\|\s*(?:[vV]?\d+\.\d+\.\d+|(?i:MILESTONE):)))")

# The cell form of a canonical opening: heading text or a first bold span that holds a "|"
# cell separator together with an X.Y.Z version token (VERSION_TOKEN_RE) or a numbered PR
# identity (PR_IDENTITY_RE: a PR or PRs label or the word pull followed by a number, with or
# without "#", or a #N token, case-insensitive, that ends its cell: only spaces and an
# optional ":" or "." come before the next "|" or the end of the text), so
# "**PR #5 | 2026.12.5**" and "**2026-11-10 | PR #2**" are candidates while
# "**Gate 59 | 2026-11-10 review:**" and "**2026-11-10 | PR #1 review:** done." are not. A
# heading such as "## Pull-request checklist" names no number.
VERSION_TOKEN_RE = re.compile(r"\d+\.\d+\.\d+")
PR_IDENTITY_RE = re.compile(r"(?:\b(?:PRs?|pull)\s*#?\s*|#)\d+(?=\s*[:.]?\s*(?:\||$))",
                            re.IGNORECASE)

# An inline code span; removed (replaced by a space) before any detection, so an archive note
# that quotes a record in backticks is body text.
CODE_SPAN_RE = re.compile(r"(`+).*?\1")

# Markdown link syntax; flatten() reads it as its link text and URL before mirror content
# detection, so a linked date or PR cell is still read. No summary tail is read through it:
# the strict character rule refuses square brackets in every root line and in every mirror
# canonical line, so neither holds a link.
LINK_RE = re.compile(r"!?\[([^\]]*)\]\(\s*<?([^)\s>]*)>?(?:\s+[^)]*)?\)")

# The date-like forms of the content rule: 3 runs of digits joined by "-", "/" or a Unicode
# dash from U+2010 to U+2015 (a "T" time suffix may follow); a dot-joined year-first date
# with a month of 1 to 12 and a day of 1 to 31 (2026.11.10); a dot-joined day-first date with
# a day of 1 to 31, a month of 1 to 12 and a 4-digit year (10.11.2026), whose first part is
# at most 31 and whose last part has 4 digits, so a YYYY.MM.patch version such as 2026.11.67
# never matches it; a day and a month name with a year, joined by spaces (10 November 2026,
# November 10, 2026) or by those dashes (10-Nov-2026, 2026-Nov-10); and the 8-digit form
# YYYYMMDD with a year from 2000 to 2099 (20261110).
_DATE_SEP = r"[-/\u2010-\u2015]"
_MONTH = (r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?"
          r"|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)")
_DAY = r"\d{1,2}(?:st|nd|rd|th)?"
_DOT_DATE = r"(?<![\w.])\d{4}\.(?:0?[1-9]|1[0-2])\.(?:0?[1-9]|[12]\d|3[01])(?!\w|\.\d)"
_DAY_MONTH = r"\b" + _DAY + r"\s+" + _MONTH + r"\.?,?\s+\d{4}\b"
_MONTH_DAY = r"\b" + _MONTH + r"\.?\s+" + _DAY + r",?\s+\d{4}\b"
_DMY_DOT_DATE = r"(?<![\w.])(?:0?[1-9]|[12]\d|3[01])\.(?:0?[1-9]|1[0-2])\.\d{4}(?!\w|\.\d)"
_DASH_MONTH = (r"\b\d{1,2}" + _DATE_SEP + _MONTH + _DATE_SEP + r"\d{4}\b"
               r"|\b\d{4}" + _DATE_SEP + _MONTH + _DATE_SEP + r"\d{1,2}\b")
_BASIC_DATE = r"(?<![\w.])20\d\d(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])(?!\w|\.\d)"
_DATE_ANY = (r"\d+" + _DATE_SEP + r"\d+" + _DATE_SEP + r"\d+|" + _DOT_DATE + "|" + _DMY_DOT_DATE
             + "|" + _DAY_MONTH + "|" + _MONTH_DAY + "|" + _DASH_MONTH + "|" + _BASIC_DATE)
DATE_ANY_RE = re.compile(_DATE_ANY, re.IGNORECASE)

# An X.Y.Z version token for the content rule and the root grammar: a leading "v" and a
# suffix such as "-rc1" may come with it; a 4-part dotted number is not one.
VERSION_ANY_RE = re.compile(r"(?<![\w.])v?\d+\.\d+\.\d+(?!\.\d)", re.IGNORECASE)

# A CalVer library version token: an optional "v" or "V", then "20" and 2 digits, a dot, 1 or 2
# digits, a dot and digits, not preceded by a digit. Every per-PR record carries one, so the
# root's intro, its bullets below the first "## Week of" heading and a canonical root line's
# summary tail hold none, read as written (the root read removes nothing); a non-CalVer X.Y.Z
# such as 1.0.2 or 4.0.3 is allowed there.
CALVER_RE = re.compile(r"(?<![0-9])[vV]?20[0-9]{2}\.[0-9]{1,2}\.[0-9]+")

# The strict character rule (an allowlist, because new Markdown forms, GitHub inline math such
# as $2026$.11.67 among them, were found in the earlier repository to hide a CalVer version): a
# root line that is not blank, and a mirror line that fully matches the canonical compact shape
# (COMPACT_HEADER_RE), holds only the characters below (ASCII letters, digits, the space and
# . , : ; - ' " ( ) / # | & % + ? ! = @), "*" only as the 2 bold delimiters of a canonical
# header (its leading "**" and the "**" that closes its date | version | PR header), and no HTML
# character reference (an "&" followed by a name, by "#" and decimal digits or by "#x" and
# hexadecimal digits, and then ";"). A plain "&" is allowed. Every other character is refused,
# so each new renderer syntax is refused unless this set names its characters. With links,
# tags, escapes, code spans, emphasis, inline math, brace groups and every character outside
# printable ASCII refused, those lines are read as written: no link scanner, second read,
# character-reference decoding, invisible-character removal, NFKC, backtick removal or
# emphasis removal applies to them.
ROOT_ALLOWED_CHARS = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
                               " .,:;-'\"()/#|&%+?!=@")
ROOT_CHAR_REFERENCE_RE = re.compile(r"&(?:[A-Za-z][A-Za-z0-9]*|#[0-9]+|#[xX][0-9A-Fa-f]+);")

# A labelled PR identity, case-insensitive, with the number as the only group that
# matched: PR or PRs followed by an optional "-", ":", "." or "#", an optional "no." or
# "number" and an optional "#" (PR #N, PR N, PRN, PR-N, PR: N, PR. N, PR no. N,
# PR number N); GH-N; owner/repo#N (an owner that starts with a letter or "_" and is not
# part of a URL path or a longer word) or the bare grc_library#N, the repository's own
# name only, so a word such as issue#42 written with no space is not read as a PR; and
# pull N, pull request N, pull-request N or a pull/N URL.
_PR_LABELLED = (
    r"\bPRs?\s*(?:[-:.#]\s*)?(?:(?:no\.?|number)\s*)?#?\s*(\d+)"
    r"|\bGH-(\d+)"
    r"|(?<![\w./#&-])(?:[A-Za-z_][\w.-]*/[\w.-]+|grc_library)#(\d+)"
    r"|\bpull(?:[\s-]+request)?\s*[-#/]?\s*(\d+)")
LABELLED_PR_RE = re.compile(_PR_LABELLED, re.IGNORECASE)

# A numbered PR identity for the content rule and the intro: a labelled PR
# identity or a bare #N token.
PR_ANY_RE = re.compile(_PR_LABELLED + r"|(?<![\w&])#(\d+)", re.IGNORECASE)

# Markdown emphasis markers, removed before any version, date or PR detection: a
# run of "*" that touches a character other than a space on either side, and a run of "_" that
# opens emphasis (no letter or digit before it, a character other than a space after it) or
# closes it (a character other than a space before it, no letter or digit after it). A "* " list
# marker, a "*" between spaces and an underscore inside a word (grc_library) stay.
EMPHASIS_RE = re.compile(
    r"\*+(?=\S)|(?<=\S)\*+|(?<![^\W_])_+(?=[^\s_])|(?<=[^\s_])_+(?![^\W_])")

# A markup-only opening (spaces, tabs, a no-break space, a byte order mark, quote markers, then
# list markers, "1." numbers or "#" heading markers, each followed by a space or a tab), and
# the bold milestone form behind one: "* **2026-07-29 | MILESTONE:** ..." is a milestone moved
# off column 0, so it is a candidate that the milestone exemption never excuses.
OPENING_RE = re.compile(r"[ \t\u00a0\ufeff>]*(?:(?:[-*+]|\d+[.)]|#{1,6})[ \t\u00a0]+)*")
LOOSE_MILESTONE_RE = re.compile(r"\*\*\s*[^\s|*]+\s*\|\s*MILESTONE:", re.IGNORECASE)

# A joint between 2 cells of a triple: a comma, a semicolon, a "|" cell separator, or a hyphen,
# en dash or em dash followed by a space, with bold or underscore markers allowed around it.
_JOINT = r"[\s*_]*(?:[,|;]|[-\u2013\u2014](?=\s))[\s*_]*"

# A comparison-like triple at the start of a line's content: an opening of markup only
# (non-word characters, underscores and ordered-list numbers such as "1."), then a date-like
# token, an X.Y.Z version (optionally labelled or prefixed "v") and a PR cell (PR #N, PR N,
# PRN, pull N, pull request N, #N, or a bare number that closes its cell, optionally after "("
# or "["), joined by _JOINT (the version and the PR cell may also be joined by an opening "("
# or "["). Unicode-wide (digits and spaces), so a no-break space or full-width digits do not
# hide a line. Used with match(), so a triple that follows words on its line is body text. A
# line holding one must be a column-0 full match of a comparison shape or fail. An underscore
# may touch the date (``__2026-11-10 | ...__``); a dot cannot directly precede it.
TRIPLE_RE = re.compile(
    r"(?:[\W_]|\d+[.)](?=\s))*?"
    r"(?<!\.)\d+[-/]\d+[-/]\d+(?![^\W_])"
    + _JOINT
    + r"(?:(?:Library\s+)?Version:?\s*)?v?\d+\.\d+\.\d+(?![\w.])"
    r"[\s*_]*(?:[,|;]|[-\u2013\u2014](?=\s)|(?=[(\[]))[\s*_]*[(\[]?\s*"
    r"(?:(?:PRs?|pull(?:\s+request)?)\s*#?\s*\d+|#\s*\d+|\d+(?=\s*(?:\*\*|__|\||,|;|\)|\]|$)))",
    re.IGNORECASE)

# The token right after a candidate's marker; when it is date-like but not a valid ASCII
# YYYY-MM-DD calendar date, the line fails as carrying an unparseable date.
LEAD_TOKEN_RE = re.compile(r"\w+(?:[-/.]\w+)*")

# A year-first date with "-" or "/" separators and 1 or 2 digit months and days. The first one on
# a line (its first date cell) decides whether the line is an old-repository record.
LOOSE_DATE_RE = re.compile(r"(?<![0-9])([0-9]{4})([-/])([0-9]{1,2})\2([0-9]{1,2})(?![0-9])",
                           re.ASCII)

# The other date forms that decide an old-repository record when a line has no year-first date
# joined by "-" or "/": a day and a month name with a year, then a dot-joined date.
MONTHS = {name: number for number, name in enumerate(
    ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"), start=1)}
NAMED_DATE_RE = re.compile(
    r"\b(?P<d1>[0-9]{1,2})(?:st|nd|rd|th)?\s+(?P<m1>" + _MONTH + r")\.?,?\s+(?P<y1>[0-9]{4})\b"
    r"|\b(?P<m2>" + _MONTH + r")\.?\s+(?P<d2>[0-9]{1,2})(?:st|nd|rd|th)?,?\s+(?P<y2>[0-9]{4})\b",
    re.IGNORECASE | re.ASCII)
DOT_DATE_RE = re.compile(r"(?<![\w.])([0-9]{4})\.([0-9]{1,2})\.([0-9]{1,2})(?![\w]|\.[0-9])",
                         re.ASCII)

# The parts of the other DATE_ANY_RE tokens that decide an old-repository record when a line
# has no year-first date joined by ASCII "-" or "/": 3 runs of digits joined by "-", "/" or a
# Unicode dash (year-first when the first run has 4 digits, day-first when the last has), a
# day-first dot-joined date, a day and a month name joined by dashes in either order, and the
# 8-digit form. These parts patterns are ASCII-only, like the other shape patterns, so a date
# in full-width digits yields no date parts here (_date_parts returns None) and never decides
# an old-repository record. DATE_ANY_RE itself stays Unicode-wide on purpose, like the other
# candidate detectors: the mirror's content rule reads it without NFKC, so a mirror line whose
# only date is in full-width digits is still a candidate and then fails.
_SEP_PARTS_RE = re.compile(r"([0-9]+)" + _DATE_SEP + r"([0-9]+)" + _DATE_SEP + r"([0-9]+)",
                           re.ASCII)
_DMY_DOT_PARTS_RE = re.compile(r"([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})", re.ASCII)
_DASH_MONTH_PARTS_RE = re.compile(
    r"(?P<d1>[0-9]{1,2})" + _DATE_SEP + r"(?P<m1>" + _MONTH + r")" + _DATE_SEP
    + r"(?P<y1>[0-9]{4})|(?P<y2>[0-9]{4})" + _DATE_SEP + r"(?P<m2>" + _MONTH + r")" + _DATE_SEP
    + r"(?P<d2>[0-9]{1,2})", re.IGNORECASE | re.ASCII)
_BASIC_PARTS_RE = re.compile(r"([0-9]{4})([0-9]{2})([0-9]{2})", re.ASCII)

# The 2 comparison shapes and the named exempt shapes, named in the failure message for any
# other mirror entry candidate.
EXPECTED_SHAPES = ("**YYYY-MM-DD | X.Y.Z | PR #N** (optionally followed by \" - <summary>\") "
                   "or ## YYYY-MM-DD, Library Version X.Y.Z, PR #N; the only exempt shapes "
                   "are ## Week of YYYY-MM-DD, **Week of YYYY-MM-DD (PRs #A-#B)** and "
                   "**YYYY-MM-DD | MILESTONE:**")

# The root grammar: the title line, the opening of an intro line, the heading that ends the
# per-PR region, and the canonical per-PR shape named in every root failure message.
ROOT_TITLE = "# Changelog"
INTRO_START_RE = re.compile(r"[^\W\d_]")
WEEK_PREFIX = "## Week of"
ROOT_EXPECTED_SHAPE = ("**YYYY-MM-DD | X.Y.Z | PR #N** at column 0 (optionally followed by "
                       "\" - <summary>\"), with a valid ISO date, a parseable X.Y.Z version and "
                       "1 PR number of 1 or more; the root accepts no other per-PR shape")
ROOT_GRAMMAR = ("the # Changelog title as the first non-blank line, the intro paragraph directly "
                "after it (lines that start "
                "with a letter and hold no date-like token, no X.Y.Z version, no CalVer library "
                "version and no numbered PR identity), blank lines and per-PR lines in the canonical shape "
                + ROOT_EXPECTED_SHAPE)
ROOT_WEEKLY_LINES = ("## Week of YYYY-MM-DD headings with a valid date, blank lines and \"- \" "
                     "bullets that hold no CalVer library version (such as 2026.11.67 or "
                     "v2026.11.67; a version such as 1.0.2 is allowed)")

# A PR number token, used to name the PRs of a failing candidate in its message.
PR_TOKEN_RE = re.compile(r"#(\d+)", re.ASCII)


def pr_headers(
    text: str,
    cutoff: int = CUTOFF_PR,
    root: bool = False,
) -> list[tuple[int, int, tuple[int, int, int] | None, str]]:
    """Return ordered ``(lineno, pr, version, version_text)`` per comparison-shape line.

    Only lines that fully match one of the 2 comparison shapes (``HEADER_RE`` or
    ``COMPACT_HEADER_RE``) with ``PR #N`` where ``N >= cutoff`` are returned; ``cutoff``
    defaults to ``CUTOFF_PR``, which ``main`` uses; ``cutoff=0`` reads every such line. Both
    shapes require an ``X.Y.Z`` version, so ``version`` is always an int 3-tuple (for numeric
    comparison). ``version_text`` is the version EXACTLY as it appears in the header (leading
    zeros preserved), for failure messages. Dates are checked by ``entry_findings``, not here.
    With ``root=True`` (the root ``.working/CHANGELOG.md``) the text is split on LF only
    (``lf_lines``), as ``root_findings`` splits it, so the line numbers match the strict
    character rule's; otherwise (the mirror) it is split with ``str.splitlines``, as
    ``entry_findings`` and the store-scope deferral flags split it.
    """
    records: list[tuple[int, int, tuple[int, int, int] | None, str]] = []
    lines = lf_lines(text) if root else text.splitlines()
    for lineno, line in enumerate(lines, start=1):
        m = HEADER_RE.match(line) or COMPACT_HEADER_RE.match(line)
        if not m:
            continue
        n = int(m.group(5))
        if n < cutoff:
            continue
        version = tuple(int(m.group(i)) for i in (2, 3, 4))
        records.append((lineno, n, version, f"{m.group(2)}.{m.group(3)}.{m.group(4)}"))
    return records


def _named_prs(line: str) -> list[int]:
    """The PR numbers a failing candidate names, for its failure message only."""
    m = HEADER_RE.match(line) or COMPACT_HEADER_RE.match(line)
    if m:
        return [int(m.group(5))]
    prs = changelog_header_prs(line) if changelog_entry_boundary(line) else []
    return list(prs) or sorted({int(n) for n in PR_TOKEN_RE.findall(line)}
                               | _pr_numbers(flatten(line)))


def _valid_date(text: str) -> datetime.date | None:
    """``text`` as an ASCII ``YYYY-MM-DD`` calendar date, or ``None`` when it is not one."""
    try:
        return datetime.date.fromisoformat(text)
    except ValueError:
        return None


def flatten(line: str) -> str:
    """``line`` with inline code spans removed, Markdown links read as their text and URL, and
    Markdown emphasis markers removed."""
    return EMPHASIS_RE.sub("", LINK_RE.sub(r"\1 \2", CODE_SPAN_RE.sub(" ", line)))


def _pr_numbers(text: str, pattern: re.Pattern = PR_ANY_RE) -> set[int]:
    """The PR numbers that ``pattern`` (a PR identity detector) names in ``text``."""
    return {int(next(group for group in m.groups() if group is not None))
            for m in pattern.finditer(text)}


def version_and_date(text: str) -> bool:
    """``True`` when ``text`` holds an ``X.Y.Z`` version and a separate date token of any form
    ``DATE_ANY_RE`` reads (a dot-joined token read as both counts once)."""
    versions = [m.span() for m in VERSION_ANY_RE.finditer(text)]
    if not versions:
        return False
    return any(d.end() <= start or end <= d.start()
               for d in DATE_ANY_RE.finditer(text) for start, end in versions)


def content_triple(text: str) -> bool:
    """``True`` when ``text`` holds a date-like token, an ``X.Y.Z`` version and a numbered PR
    identity, in any order; the date and the version must be separate tokens."""
    return PR_ANY_RE.search(text) is not None and version_and_date(text)


def root_character_findings(line: str) -> list[tuple[int, str]]:
    """``(column, what)`` for each character and each HTML character reference in ``line`` (a root
    line, or a mirror line that fully matches ``COMPACT_HEADER_RE``) that the strict character rule
    refuses (an allowlist), in column order. ``column`` counts characters
    from 1; ``what`` names a refused character by its code point (every character that is not in
    ``ROOT_ALLOWED_CHARS`` and is not a ``*`` that is one of the 2 bold delimiters of a canonical
    header: the leading ``**`` and the ``**`` that closes the ``date | version | PR`` header) or
    quotes the reference."""
    canonical = COMPACT_HEADER_RE.match(line)
    delimiters = ({0, 1, canonical.end(5), canonical.end(5) + 1} if canonical is not None
                  else set())
    hits = []
    for index, char in enumerate(line):
        if char in ROOT_ALLOWED_CHARS or (char == "*" and index in delimiters):
            continue
        if not " " <= char <= "~":
            hits.append((index + 1, f"character U+{ord(char):04X} outside printable ASCII"))
        else:
            hits.append((index + 1, f"refused character {char!r} (U+{ord(char):04X})"))
    hits.extend((m.start() + 1, f"HTML character reference {m.group(0)!r}")
                for m in ROOT_CHAR_REFERENCE_RE.finditer(line))
    return sorted(hits)


def calver_versions(line: str) -> list[str]:
    """The CalVer library version tokens (``CALVER_RE``) in the root line ``line``, read as
    written (the strict character rule refuses every backtick and every
    ``*`` but a canonical header's bold delimiters, so the root read removes nothing). A root
    bullet below the first ``## Week of`` heading or a canonical root line's summary tail fails
    when this is not empty; it replaces the earlier version-with-date and version-with-labelled-PR
    rules there. Each version is listed once, in the order read."""
    return list(dict.fromkeys(CALVER_RE.findall(line)))


def root_tail_versions(line: str, match: re.Match) -> list[str]:
    """The CalVer library versions a canonical root line's summary tail holds; ``match`` is
    the ``COMPACT_HEADER_RE`` match of ``line``."""
    return calver_versions(line[match.end(5) + 2:])


def tail_prs(line: str, match: re.Match) -> list[int]:
    """The other PRs a canonical compact mirror line's summary tail names as a record; the root
    reads its tails with ``root_tail_versions`` instead.

    The tail is read as written, as the root reads its lines: the
    strict character rule holds every mirror canonical line, so the tail holds no link, code
    span, emphasis, escape, character reference or character outside printable ASCII to read
    around (``entry_findings``).

    ``match`` is the ``COMPACT_HEADER_RE`` match of ``line``. When the tail after the closing
    ``**`` holds an ``X.Y.Z`` version, every labelled PR identity in it naming a number other
    than the header's PR is returned; otherwise the list is empty.
    """
    tail = line[match.end(5) + 2:]
    if not VERSION_ANY_RE.search(tail):
        return []
    own = int(match.group(5))
    return sorted(n for n in _pr_numbers(tail, LABELLED_PR_RE) if n != own)


def misplaced_milestone(text: str) -> bool:
    """``True`` when ``text`` holds the bold milestone form behind a non-empty markup-only
    opening, such as ``* **2026-07-29 | MILESTONE:** split landed.``."""
    opening = OPENING_RE.match(text)
    return opening.end() > 0 and LOOSE_MILESTONE_RE.match(text, opening.end()) is not None


def candidate_text(line: str) -> tuple[str, str] | None:
    """``(rest, span)`` when ``line`` is an entry candidate by its canonical opening, else
    ``None``.

    The opening rule: a line that starts at column 0 with ``## ``, ``**`` or
    ``- **`` (a list-item bold line) is a candidate when its heading text (after ``## ``) or its
    first bold span (after ``**`` or ``- **``) matches ``CANONICAL_OPENING_RE`` (it starts with
    ``Week of`` or with a date-like token that ends that text or is followed by ``,`` and a
    ``Version`` label, a version or a numbered PR identity that ends that text or is followed
    by ``,`` or ``|``, or by ``|`` and an ``X.Y.Z`` version or ``MILESTONE:``)
    or is in the cell form (it holds a ``|`` cell separator together with an
    ``X.Y.Z`` version or a numbered PR identity that ends its cell).
    ``rest`` is the line after its marker and ``span`` is the heading text or the first bold
    span (the rest of the line when the bold span is not closed). The caller passes the line with
    its inline code spans removed. A line that starts with a comparison-like triple
    (``TRIPLE_RE``) or holds a date, a version and a PR identity in any order (``content_triple``)
    is a candidate whatever its opening; ``_classify_line`` reads those rules.
    """
    for marker in CANDIDATE_MARKERS:
        if line.startswith(marker):
            rest = line[len(marker):]
            span = rest if marker == "## " else rest.partition("**")[0]
            hit = (CANONICAL_OPENING_RE.match(span)
                   or ("|" in span and (VERSION_TOKEN_RE.search(span)
                                       or PR_IDENTITY_RE.search(span))))
            return (rest, span) if hit else None
    return None


def _first_date(text: str) -> tuple[str, datetime.date | None] | None:
    """``(token, date)`` for the first date in ``text``, or ``None`` when it holds none.

    The first year-first date joined by ASCII ``-`` or ``/`` decides; when there is none, the
    first ``DATE_ANY_RE`` token in any other form apart from a dot-joined year-first date
    (``_date_parts``: a date joined by a Unicode dash, a day-first date with a 4-digit year, a day
    and a month name with a year, or the 8-digit form, so
    ``21-Jun-2026`` decides before the version ``2026.06.9``); when there is neither,
    the first dot-joined year-first date. ``date`` is ``None`` when the token is not a
    calendar date.
    """
    m = LOOSE_DATE_RE.search(text)
    if m is not None:
        token, parts = m.group(0), (m.group(1), m.group(3), m.group(4))
    else:
        token = parts = None
        for any_date in DATE_ANY_RE.finditer(text):
            parts = _date_parts(any_date.group(0))
            if parts is not None:
                token = any_date.group(0)
                break
        if token is None:
            m = DOT_DATE_RE.search(text)
            if m is None:
                return None
            token, parts = m.group(0), (m.group(1), m.group(2), m.group(3))
    try:
        return token, datetime.date(*(int(part) for part in parts))
    except ValueError:
        return token, None


def _date_parts(token: str) -> tuple[str, str, str] | None:
    """``(year, month, day)`` of a ``DATE_ANY_RE`` token, or ``None`` for a dot-joined year-first
    date (read last, by ``DOT_DATE_RE``) and for 3 runs of digits with no 4-digit year at either
    end."""
    m = _SEP_PARTS_RE.fullmatch(token)
    if m is not None:
        first, middle, last = m.groups()
        if len(first) == 4:
            return first, middle, last
        return (last, middle, first) if len(last) == 4 else None
    m = _DMY_DOT_PARTS_RE.fullmatch(token)
    if m is not None:
        return m.group(3), m.group(2), m.group(1)
    m = NAMED_DATE_RE.fullmatch(token) or _DASH_MONTH_PARTS_RE.fullmatch(token)
    if m is not None:
        month = MONTHS[(m.group("m1") or m.group("m2"))[:3].lower()]
        return m.group("y1") or m.group("y2"), str(month), m.group("d1") or m.group("d2")
    m = _BASIC_PARTS_RE.fullmatch(token)
    return m.groups() if m is not None else None


def _old_date(text: str) -> str | None:
    """The first date in ``text`` (``_first_date``) when it is a calendar date before
    ``EPOCH_START``.

    Only the first date cell decides: a new entry that cites an older date later
    on its line is not an old-repository record.
    """
    first = _first_date(text)
    if first is None or first[1] is None:
        return None
    return first[0] if first[1] < EPOCH_START_DATE else None


class EntryFindings:
    """The failing lines of one surface, by kind; each kind fails the gate.

    ``old`` holds ``(lineno, prs, date)``, ``unparseable`` holds ``(lineno, token)``,
    ``unreadable`` holds ``(lineno, line)``, ``multi`` holds ``(lineno, prs)`` and ``floor``
    holds ``(lineno, pr, version_text)``. ``below`` stays empty: every
    comparison shape needs a PR number of 1 or more, so ``PR #0`` fails as ``unreadable``; it is
    kept so that ``shape_findings`` keeps its return shape. The root alone
    fills ``grammar`` (``(lineno, line)``, a line above its first ``## Week of`` heading outside
    the root grammar), ``late`` (``(lineno, line)``, a comparison-shape line at or below that
    heading) and ``weekly`` (``(lineno, line)``, any other line at or below that heading that is
    not a valid ``## Week of`` heading, a blank line or an allowed ``- `` bullet) and
    ``calver_tail`` (``(lineno, pr, versions)``, a canonical line whose summary tail holds a
    CalVer library version) and ``chars`` (``(lineno, column, what)``, a character or an
    HTML character reference the strict character rule refuses), which every mirror
    canonical line fills too. ``tail`` holds ``(lineno, pr, other_prs)`` for a canonical
    compact mirror line whose summary tail names another PR's record.
    """

    def __init__(self) -> None:
        self.floor: list[tuple[int, int, str]] = []
        self.old: list[tuple[int, list[int], str]] = []
        self.unparseable: list[tuple[int, str]] = []
        self.unreadable: list[tuple[int, str]] = []
        self.below: list[tuple[int, int]] = []
        self.multi: list[tuple[int, list[int]]] = []
        self.grammar: list[tuple[int, str]] = []
        self.late: list[tuple[int, str]] = []
        self.weekly: list[tuple[int, str]] = []
        self.tail: list[tuple[int, int, list[int]]] = []
        self.calver_tail: list[tuple[int, int, list[str]]] = []
        self.chars: list[tuple[int, int, str]] = []

    def lines(self) -> set[int]:
        """Every failing line number, left out of the comparison."""
        return ({hit[0] for hit in self.old} | {hit[0] for hit in self.unparseable}
                | {hit[0] for hit in self.unreadable} | {hit[0] for hit in self.below}
                | {hit[0] for hit in self.multi} | {hit[0] for hit in self.floor}
                | {hit[0] for hit in self.grammar} | {hit[0] for hit in self.late}
                | {hit[0] for hit in self.weekly} | {hit[0] for hit in self.tail}
                | {hit[0] for hit in self.calver_tail} | {hit[0] for hit in self.chars})

    def __bool__(self) -> bool:
        return bool(self.lines())


def _classify_line(found: EntryFindings, lineno: int, line: str, root: bool = False) -> bool:
    """Classify one line by the mirror rules; ``True`` when it recorded a failure in ``found``.

    ``root`` is true for a root line, whose summary tail ``root_findings`` reads by the CalVer
    rule instead of the mirror's tail rule.

    A table row is skipped, inline code spans are removed and Markdown links are flattened before
    detection, and Markdown emphasis markers are removed before the content rule and the date
    reading (``flatten``). A line that starts with a comparison-like triple (``TRIPLE_RE``),
    holds a date, a version and a PR identity in any order (``content_triple``) or holds the
    milestone form behind an opening (``misplaced_milestone``) and is not a column-0 full
    match of a comparison shape fails first: as ``old`` when its first date (``_first_date``: the
    first year-first date joined by ``-`` or ``/``, else the first date in another form the
    content rule reads apart from a dot-joined year-first date, else the first dot-joined
    year-first date) is before ``EPOCH_START``, otherwise as ``unreadable``
    when it is not a candidate by its opening, and
    otherwise through rules 5 to 7 below (the exempt shapes of rules 1 and 3 never excuse it).
    Each candidate by its opening (``candidate_text``) is classified in this order, fail closed:

    1. a ``## Week of <date>`` heading or an old weekly roll-up bold line
       ``**Week of <date> (PRs #A-#B)**``, matched in full, is exempt whatever its date when the
       date is valid, and fails as ``unparseable`` when it is not;
    2. a candidate whose first date (``_first_date``) is a calendar date before
       ``EPOCH_START`` is an old-repository record (``old``);
    3. the bold milestone form ``**<date> | MILESTONE:**`` is exempt, whether or not its text
       names a PR;
    4. a line that fully matches one of the 2 comparison shapes is compared; a version below
       ``VERSION_FLOOR`` makes it an old-repository record (``floor``) whatever its date, and a
       compact mirror line whose summary tail holds an ``X.Y.Z`` version and a labelled PR
       identity naming another number fails as ``tail``. The shapes read only
       a PR number of 1 or more, so ``PR #0`` (below ``CUTOFF_PR``) matches no shape and fails
       as ``unreadable`` under rule 7;
    5. a date that is not a valid ASCII ``YYYY-MM-DD`` calendar date in a matched shape, or a
       date-like token right after the marker, fails as ``unparseable``; a date elsewhere on a
       line that matches no shape (``- 2026/11/09 | 2026.11.66 | PR #1``) is not read here, and
       the line fails as ``unreadable``;
    6. a legacy-shaped line naming more than 1 PR fails as ``multi`` (one header per PR);
    7. every other candidate fails as ``unreadable``, with a message naming the expected shapes
       (a malformed bold ``Week of`` line among them).
    """
    if line.lstrip(" \t").startswith("|"):
        return False  # a table row
    scan = CODE_SPAN_RE.sub(" ", line)
    plain = flatten(line)
    full = HEADER_RE.match(line) or COMPACT_HEADER_RE.match(line)
    loose = full is None and (TRIPLE_RE.match(scan) is not None or content_triple(plain)
                              or misplaced_milestone(scan))
    candidate = candidate_text(scan)
    if candidate is None:
        if not loose:
            return False
        # A triple behind any other opening: never compared, always a failure.
        old = _old_date(plain)
        if old is not None:
            found.old.append((lineno, _named_prs(line), old))
        else:
            found.unreadable.append((lineno, line))
        return True
    rest, _span = candidate
    week = None if loose else (WEEK_HEADING_RE.match(line) or WEEK_ROLLUP_RE.match(line))
    if week:
        if _valid_date(week.group(1)) is None:
            found.unparseable.append((lineno, week.group(1)))
            return True
        return False
    old = _old_date(plain)
    if old is not None:
        found.old.append((lineno, _named_prs(line), old))
        return True
    shaped = full or (None if loose else MILESTONE_RE.match(line))
    if shaped:
        if _valid_date(shaped.group(1)) is None:
            found.unparseable.append((lineno, shaped.group(1)))
        elif shaped.re is MILESTONE_RE:
            return False
        elif tuple(int(shaped.group(i)) for i in (2, 3, 4)) < VERSION_FLOOR_TUPLE:
            found.floor.append((lineno, int(shaped.group(5)),
                                f"{shaped.group(2)}.{shaped.group(3)}.{shaped.group(4)}"))
        elif shaped.re is COMPACT_HEADER_RE and not root and tail_prs(line, shaped):
            found.tail.append((lineno, int(shaped.group(5)), tail_prs(line, shaped)))
        else:
            return False
        return True
    lead = LEAD_TOKEN_RE.match(rest)
    if lead and DATE_LIKE_RE.fullmatch(lead.group(0)) and _valid_date(lead.group(0)) is None:
        found.unparseable.append((lineno, lead.group(0)))
        return True
    tokens = sorted({int(n) for n in PR_TOKEN_RE.findall(line)})
    if LEGACY_LEAD_RE.match(line) and len(tokens) > 1:
        found.multi.append((lineno, tokens))
        return True
    found.unreadable.append((lineno, line))
    return True


def entry_findings(text: str) -> EntryFindings:
    """Classify every line of the detailed mirror ``text`` by the mirror rules.

    Lines are read raw, with no cutoff and no deferral, over the same ``splitlines()`` view as
    ``pr_headers``, so the line numbers agree. See ``_classify_line`` for the rules. Every line
    that fully matches ``COMPACT_HEADER_RE`` also meets the strict character rule
    (``root_character_findings``), and its line ending must be LF, CR LF or the
    end of the file: a line that ``splitlines()`` ends at another line boundary (a vertical tab,
    a form feed, U+001C to U+001E, U+0085, U+2028 or U+2029, none of which ends a line in
    Markdown) fails as ``chars`` at the column of that character.
    """
    found = EntryFindings()
    for lineno, raw in enumerate(text.splitlines(keepends=True), start=1):
        line = raw.splitlines()[0] if raw.splitlines() else ""
        if COMPACT_HEADER_RE.match(line):
            found.chars.extend((lineno, column, what)
                               for column, what in root_character_findings(line))
            ending = raw[len(line):]
            if ending not in ("", "\n", "\r\n"):
                found.chars.append((lineno, len(line) + 1,
                                    f"character U+{ord(ending[0]):04X} outside printable ASCII"))
        _classify_line(found, lineno, line)
    return found


def root_findings(text: str) -> EntryFindings:
    """Check the root ``text`` against the root grammar; fail every other line.

    ``main`` removes at most 1 leading byte order mark, once, before it calls this:
    this function removes none, so a byte order mark left in ``text`` fails line 1 by the
    strict character rule. The text is split on LF only (``lf_lines``). Every line that is
    not blank then meets the strict character rule (an allowlist): each
    character outside ``ROOT_ALLOWED_CHARS``, each ``*`` other than a canonical header's 2 bold
    delimiters and each HTML character reference fails as ``chars``, with its column
    (``root_character_findings``). The intro,
    weekly-bullet and summary-tail rules read each line as written, and every other line
    through the mirror rules. Above the first ``## Week of``
    heading (the whole file when it has none) only these lines pass: the ``# Changelog`` title as
    the first non-blank line (when the first non-blank line of the file is anything
    else, that line fails as ``grammar``, and an empty root fails at line 1), the intro paragraph directly after it (blank lines may come
    between; each line starts with a letter and holds no date-like token, no ``X.Y.Z`` version,
    no CalVer library version and no numbered PR identity (``PR_ANY_RE``: a labelled PR identity
    or a bare ``#N``)), blank lines (empty or only spaces and tabs) and canonical per-PR lines
    (``COMPACT_HEADER_RE`` in full, then the mirror rules' date and ``VERSION_FLOOR`` checks, and
    a summary tail that holds no CalVer library version, else ``calver_tail``). Every
    other line there fails: with its mirror-rule failure when the
    mirror rules fail it, otherwise as ``old`` when its first date is before ``EPOCH_START``, and
    otherwise as ``grammar``. At and below that heading only ``## Week of`` headings with a
    valid date, blank lines and ``- `` bullets for which ``calver_versions`` is empty (no
    CalVer library version, which replaces the earlier version-with-date and
    version-with-labelled-PR rules) pass: a comparison-shape line fails as ``late``, a weekly heading with an invalid date as
    ``unparseable`` and every other line as ``weekly``.
    """
    found = EntryFindings()
    lines = lf_lines(text)
    for lineno, line in enumerate(lines, start=1):
        if line.strip(" \t"):
            found.chars.extend((lineno, column, what)
                               for column, what in root_character_findings(line))
    week = next((i for i, line in enumerate(lines) if line.startswith(WEEK_PREFIX)), len(lines))
    state = "start"  # start, then title, then intro, then body
    untitled = None  # the first non-blank line when it is not the title
    for index, line in enumerate(lines[:week]):
        lineno = index + 1
        if line.strip(" \t") == "":
            if state == "intro":
                state = "body"
            continue
        plain = flatten(line)
        if state == "start":
            state = "body"
            if line == ROOT_TITLE:
                state = "title"
                continue
            untitled = (lineno, line)
        elif state in ("title", "intro"):
            # The strict character rule above leaves no link, escape, code span,
            # emphasis or hidden character to read around, so the line is read as written.
            if INTRO_START_RE.match(line) and not (
                    DATE_LIKE_RE.search(line) or VERSION_ANY_RE.search(line)
                    or CALVER_RE.search(line) or PR_ANY_RE.search(line)):
                state = "intro"
                continue
            state = "body"
        if _classify_line(found, lineno, line, root=True):
            continue
        canonical = COMPACT_HEADER_RE.match(line)
        if canonical:
            versions = root_tail_versions(line, canonical)
            if versions:
                found.calver_tail.append((lineno, int(canonical.group(5)), versions))
            continue
        old = _old_date(plain)
        if old is not None:
            found.old.append((lineno, _named_prs(line), old))
        else:
            found.grammar.append((lineno, line))
    if state == "start":
        # No non-blank line above the first ## Week of heading: the title is missing.
        untitled = (week + 1, lines[week]) if week < len(lines) else (1, "")
    if untitled is not None and untitled[0] not in found.lines():
        found.grammar.append(untitled)
    for index in range(week, len(lines)):
        lineno, line = index + 1, lines[index]
        if HEADER_RE.match(line) or COMPACT_HEADER_RE.match(line):
            found.late.append((lineno, line))
            continue
        if line.strip(" \t") == "":
            continue
        heading = WEEK_HEADING_RE.match(line)
        if heading:
            if _valid_date(heading.group(1)) is None:
                found.unparseable.append((lineno, heading.group(1)))
            continue
        if line.startswith("- ") and not calver_versions(line):
            continue
        found.weekly.append((lineno, line))
    return found


def strip_bom(text: str) -> str:
    """``text`` without 1 leading U+FEFF byte order mark. ``main`` calls it once per
    surface; a second leading mark stays and fails line 1 by the strict character rule."""
    return text[1:] if text.startswith("\ufeff") else text


def lf_lines(text: str) -> list[str]:
    """The root ``text`` split into lines on LF only. A CR
    directly before an LF is part of that line ending and removed; every other character (a lone
    CR, a vertical tab, a form feed, U+001C to U+001E, U+0085, U+2028 and U+2029 among them)
    stays in its line, where the strict character rule refuses it, so line numbers count LF line
    endings as an editor does. A final LF ends the last line and adds no empty line.
    ``read_surface`` reads the file with universal newlines, so a CR LF or a lone CR in the file
    reaches this function from ``main`` as an LF, as CommonMark also ends a line there."""
    parts = text.split("\n")
    lines = [part[:-1] if part.endswith("\r") else part for part in parts[:-1]]
    if parts[-1]:
        lines.append(parts[-1])
    return lines


def epoch_findings(text: str) -> tuple[list[tuple[int, list[int], str]], list[tuple[int, str]]]:
    """``(old, unparseable)`` from ``entry_findings``: the epoch rule's 2 kinds of failure.

    ``old`` holds ``(lineno, prs, date)`` for each old-repository record (an entry candidate
    carrying a date before ``EPOCH_START``) and ``unparseable`` holds ``(lineno, token)`` for
    each candidate whose date is not a valid ASCII ``YYYY-MM-DD`` calendar date. PR numbers
    restarted at #1 on ``EPOCH_START``, so an old record's number may name a different pull
    request than a new one.
    """
    found = entry_findings(text)
    return found.old, found.unparseable


def shape_findings(text: str) -> tuple[list[tuple[int, str]], list[tuple[int, int]]]:
    """``(unreadable, below)`` from ``entry_findings``.

    ``unreadable`` holds ``(lineno, line)`` for each entry candidate that matches no
    comparison shape and no named exempt shape. ``below`` is always empty:
    every comparison shape needs a PR number of 1 or more, so a line naming
    ``PR #0`` (below ``CUTOFF_PR``) is in ``unreadable``; it is kept for the return shape.
    """
    found = entry_findings(text)
    return found.unreadable, found.below


def _describe_old(lineno: int, prs: list[int], date: str) -> str:
    if len(prs) == 1:
        return f"line {lineno} PR #{prs[0]} ({date})"
    if prs:
        return f"line {lineno} PRs " + ", ".join(f"#{pr}" for pr in prs) + f" ({date})"
    return f"line {lineno} with no PR number read ({date})"


def print_epoch_failures(where: str, old: list[tuple[int, list[int], str]],
                         unparseable: list[tuple[int, str]]) -> None:
    """Print the epoch rule's FAIL lines for one surface."""
    if old:
        print(
            f"FAIL: per-PR header(s) in {where} dated before EPOCH_START {EPOCH_START} "
            "are old-repository records to archive (PR numbers restarted at #1 on that "
            "date): " + ", ".join(_describe_old(*hit) for hit in old)
        )
    if unparseable:
        print(
            f"FAIL: entry line(s) in {where} carry a date gate 59 cannot parse "
            "(each must be a valid ASCII YYYY-MM-DD calendar date): "
            + ", ".join(f"line {lineno} ({token!r})" for lineno, token in unparseable)
        )


def print_entry_failures(where: str, found: EntryFindings,
                         expected: str = EXPECTED_SHAPES) -> None:
    """Print every FAIL line of ``entry_findings`` or ``root_findings`` for one surface."""
    print_epoch_failures(where, found.old, found.unparseable)
    if found.floor:
        print(
            f"FAIL: per-PR header(s) in {where} carry a Library Version below VERSION_FLOOR "
            f"{VERSION_FLOOR} (the first version shipped by a new-repository PR; main starts at "
            "2026.11.65), so they are old-repository records to archive, whatever their date: "
            + ", ".join(f"line {lineno} PR #{pr} ({version})" for lineno, pr, version in found.floor)
        )
    print_shape_failures(where, found.unreadable, found.multi, expected)
    if found.tail:
        print(
            f"FAIL: per-PR line(s) in {where} carry another PR's record in their summary tail "
            "(an X.Y.Z version and a labelled PR identity naming a number other than the "
            "header's PR); "
            "each PR needs its own header: "
            + ", ".join(f"line {lineno} PR #{pr} (names " + ", ".join(f"#{n}" for n in others)
                        + ")" for lineno, pr, others in found.tail)
        )
    if found.calver_tail:
        print(
            f"FAIL: per-PR line(s) in {where} hold a CalVer library version in their summary "
            "tail (every per-PR record carries one, so the tail would carry a record unread); "
            "each PR needs its own header: "
            + ", ".join(f"line {lineno} PR #{pr} (" + ", ".join(versions) + ")"
                        for lineno, pr, versions in found.calver_tail)
        )
    if found.chars:
        print(
            f"FAIL: line(s) in {where} hold a character or an HTML character reference that the "
            "strict character rule refuses (a root line that is not blank and a canonical per-PR "
            "line in the mirror may hold only ASCII letters, digits, the space and "
            ". , : ; - ' \" ( ) / # | & % + ? ! = @, with * only as the 2 bold delimiters of a "
            "canonical header, and no HTML character reference such as &#46; or &amp;; a plain & "
            "is allowed, and every other character is refused): "
            + ", ".join(f"line {lineno} column {column}: {what}"
                        for lineno, column, what in found.chars)
        )
    if found.grammar:
        print(
            f"FAIL: line(s) in {where} above its first {WEEK_PREFIX} heading are outside the "
            f"root grammar (that region must hold only {ROOT_GRAMMAR}): "
            + ", ".join(f"line {lineno} ({line!r})" for lineno, line in found.grammar)
        )
    if found.late:
        print(
            f"FAIL: per-PR line(s) in {where} sit at or below its first {WEEK_PREFIX} heading; "
            "per-PR lines belong only to the current week, above the weekly summaries, in the "
            f"canonical shape {ROOT_EXPECTED_SHAPE}: "
            + ", ".join(f"line {lineno} ({line!r})" for lineno, line in found.late)
        )
    if found.weekly:
        print(
            f"FAIL: line(s) in {where} at or below its first {WEEK_PREFIX} heading are outside "
            f"the root grammar (that region must hold only {ROOT_WEEKLY_LINES}): "
            + ", ".join(f"line {lineno} ({line!r})" for lineno, line in found.weekly)
        )


def print_shape_failures(where: str, unreadable: list[tuple[int, str]],
                         multi: list[tuple[int, list[int]]] = (),
                         expected: str = EXPECTED_SHAPES) -> None:
    """Print the FAIL lines for entry candidates the comparison cannot fully read.

    No below-``CUTOFF_PR`` line is printed: a ``PR #0`` line matches no
    comparison shape, so it is printed with the unreadable lines.
    """
    if unreadable:
        print(
            f"FAIL: entry line(s) in {where} are in "
            f"a shape gate 59 cannot compare (each must be {expected}): "
            + ", ".join(f"line {lineno} ({line!r})" for lineno, line in unreadable)
        )
    if multi:
        print(
            f"FAIL: per-PR header(s) in {where} name more than 1 PR; "
            "one header per PR is required: "
            + ", ".join(f"line {lineno} (" + ", ".join(f"#{pr}" for pr in prs) + ")"
                        for lineno, prs in multi)
        )


def read_surface(path: Path) -> tuple[str | None, str]:
    """Read ``path`` as UTF-8 text: ``(text, "")``, or ``(None, reason)`` when it cannot.

    ``read_text_safe`` returns ``None`` for a file that is not valid UTF-8; gate 59 must not
    read that as empty text, so the caller fails and names the file.
    """
    try:
        text = read_text_safe(path)
    except OSError as exc:
        return None, f"cannot be read ({exc.strerror or type(exc).__name__})"
    if text is None:
        return None, "not valid UTF-8"
    return text, ""


def print_unreadable_files(failures: list[tuple[str, str]]) -> None:
    """Print one FAIL line per root or mirror file that could not be read as UTF-8 text."""
    for where, reason in failures:
        print(f"FAIL: {where} is {reason}; gate 59 cannot check its headers, so it fails "
              "rather than reading the file as empty.")


def pr_header_counts(text: str, cutoff: int = CUTOFF_PR) -> Counter:
    """Return a Counter of PR numbers (>= cutoff) appearing in per-PR headers."""
    return Counter(pr for _, pr, _, _ in pr_headers(text, cutoff=cutoff))


def ordering_violations(
    records: list[tuple[int, int, tuple[int, int, int] | None, str]],
) -> list[str]:
    """Return human-readable strictly-decreasing violations in file order.

    Entries are newest-first, so each versioned header's Library Version
    must be strictly GREATER than the next versioned header's below it.
    Equal and increasing pairs are reported with distinct wording so
    triage is immediate.
    """
    versioned = [r for r in records if r[2] is not None]
    violations: list[str] = []
    for (a_line, a_pr, a_v, a_s), (b_line, b_pr, b_v, b_s) in zip(
        versioned, versioned[1:]
    ):
        if a_v > b_v:
            continue
        if a_v == b_v:
            violations.append(
                f"line {a_line} (PR #{a_pr}) and line {b_line} (PR #{b_pr}) "
                f"share Library Version {a_s}; each entry must carry its own"
            )
        else:
            violations.append(
                f"line {a_line} (PR #{a_pr}, {a_s}) sits above line {b_line} "
                f"(PR #{b_pr}, {b_s}) but carries the SMALLER version; entries "
                f"are newest-first, so versions must strictly decrease top-down"
            )
    return violations


def version_mismatches(
    root_records: list[tuple[int, int, tuple[int, int, int] | None, str]],
    mirror_records: list[tuple[int, int, tuple[int, int, int] | None, str]],
) -> list[tuple[int, str, str]]:
    """PRs present in BOTH files whose Library Versions DIFFER.

    Returns ``(pr, root_version_text, mirror_version_text)`` triples, ordered by
    PR. In the earlier repository the gate checked set parity of PR numbers and
    strict monotonicity WITHIN each file, but never that a PR present in both
    carried the SAME version in each, so a mirror could record a version that
    was never shipped while both files stayed independently monotonic and their
    PR sets matched (there, one PR's root and README entries both said
    2026.07.642 while the mirror said 2026.07.641).

    Two deliberate exclusions, and 1 tightening:

    - A record whose version did not parse carries ``None``, which the caller
      already tolerates for the ordering assertion; such a pair is SKIPPED here
      too rather than reported, so this check cannot start failing on a shape the
      rest of the gate accepts.
    - The version texts must also be identical, so a zero-padded part on one
      side only (``2026.06.9`` against ``2026.6.9``) is a disagreement.
    - A PR appearing MORE THAN ONCE in either file is already a failure via the
      existing duplicate checks, so this join assumes at most one record per PR
      per file and reads the FIRST if that assumption is ever violated. It
      therefore adds no new policy for duplicates and cannot mask them: the
      duplicate check fires independently in the same run.
    """
    root_by_pr: dict[int, tuple[tuple[int, int, int] | None, str]] = {}
    for _lineno, pr, version, version_text in root_records:
        root_by_pr.setdefault(pr, (version, version_text))
    mismatches: list[tuple[int, str, str]] = []
    seen: set[int] = set()
    for _lineno, pr, version, version_text in mirror_records:
        if pr in seen or pr not in root_by_pr:
            continue
        seen.add(pr)
        root_version, root_text = root_by_pr[pr]
        if root_version is None or version is None:
            continue
        if root_version != version or root_text != version_text:
            mismatches.append((pr, root_text, version_text))
    return sorted(mismatches)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=str,  # a str, so an empty --root= reaches require_dir as "" (Path("") is ".")
        default=None,
        help="repository root to scan (default: the audited repository, whose "
             "detailed mirror resolves via lint_common.resolve_working)",
    )
    args = parser.parse_args(argv)

    if args.root is not None:
        # EXPLICIT --root stays verbatim: the regression fixtures build a synthetic tree
        # with its own .working/changelog-details/, read as given. An explicit --root
        # must be a directory holding both inputs; in the earlier repository a missing
        # input raised a traceback (rc 1, the findings code).
        root = require_dir(args.root, "--root")
        root_changelog = root / ROOT_CHANGELOG_REL
        detailed_mirror = root / DETAILED_MIRROR_REL
        missing = [str(p) for p in (root_changelog, detailed_mirror) if not p.is_file()]
        if missing:
            print(f"ERROR: --root {args.root}: required input(s) missing: {', '.join(missing)}",
                  file=sys.stderr)
            return 2
        scope_root = root
    else:
        root_changelog = REPO_ROOT / ROOT_CHANGELOG_REL
        # The store holds the .working/ tree's files at its root, so the lookup takes the
        # mirror's path below .working/ from the one constant --root also reads.
        resolved = resolve_working(DETAILED_MIRROR_REL[len(".working/"):])
        if resolved is None:
            # The detailed mirror is maintainer-only working state. Once `.working/` moves
            # to the operational store it is absent in public CI and adopter clones; on the
            # maintainer's machine the operational store (or the private-sibling fallback)
            # supplies it and per-PR header parity, version agreement, and ordering are all
            # enforced. Every root check that needs no mirror runs here too (a readable
            # UTF-8 root, entry classification, and the root's duplicate and ordering
            # checks), so a bad root fails in CI.
            root_text, root_err = read_surface(root_changelog)
            if root_text is None:
                print_unreadable_files([(f"root {ROOT_CHANGELOG_REL}", root_err)])
                return 1
            root_text = strip_bom(root_text)  # at most 1 byte order mark, once
            root_found = root_findings(root_text)
            root_skip = root_found.lines()
            root_records = [r for r in pr_headers(root_text, cutoff=CUTOFF_PR, root=True)
                            if r[0] not in root_skip]
            root_counts = Counter(pr for _, pr, _, _ in root_records)
            dup_root = sorted(n for n, c in root_counts.items() if c > 1)
            order_root = ordering_violations(root_records)
            if root_found or dup_root or order_root:
                print_entry_failures(f"root {ROOT_CHANGELOG_REL}", root_found, ROOT_EXPECTED_SHAPE)
                if dup_root:
                    print(
                        "FAIL: PR header(s) appearing more than once in root "
                        f".working/CHANGELOG.md (>= #{CUTOFF_PR}): "
                        + ", ".join(f"#{n}" for n in dup_root)
                    )
                if order_root:
                    print(
                        f"FAIL: root .working/CHANGELOG.md Library Version ordering violated "
                        f"(>= #{CUTOFF_PR}):"
                    )
                    for v in order_root:
                        print(f"  {v}")
                print(
                    "\nOld-repository records dated before EPOCH_START "
                    f"{EPOCH_START} must be archived out of the root .working/CHANGELOG.md, "
                    "every dated header must carry a valid YYYY-MM-DD date in a shape gate 59 "
                    "can compare, with one header per PR, and the root's Library Versions must "
                    "strictly decrease top-down. Above its first ## Week of heading the root "
                    "must hold only the lines of the root grammar, and at or below it only "
                    f"{ROOT_WEEKLY_LINES}."
                )
                return 1
            print(
                "OK: the detailed CHANGELOG mirror is not present "
                "(maintainer-only working state; skipping the header-parity "
                "audit in public CI / adopter clone). The root CHANGELOG passed the "
                "epoch, header-shape, duplicate and ordering checks."
            )
            print_degraded(
                "gate 59",
                "gate 59 skipped the root/detailed-mirror CHANGELOG header-parity and "
                "version-agreement checks and the mirror's own checks (no private store "
                "supplies the detailed mirror); only the root's own checks ran, so this "
                "pass attests nothing about header parity."
            )
            return 0
        detailed_mirror = resolved
        scope_root = REPO_ROOT

    # Both surfaces are read RAW (no example masking anywhere in the store scope), exactly as
    # the pre-store-scope gate read them, so no record can be removed from evaluation by a
    # mask. No floor is computed: every post-epoch header is compared in both files, and only
    # store-scope deferral below removes a mirror header, with a note.
    root_text, root_err = read_surface(root_changelog)
    mirror_text, mirror_err = read_surface(detailed_mirror)
    unreadable_files = [(where, err) for where, err in (
        (f"root {ROOT_CHANGELOG_REL}", root_err),
        (f"the detailed mirror ({detailed_mirror})", mirror_err)) if err]
    if unreadable_files:
        print_unreadable_files(unreadable_files)
        return 1
    root_text = strip_bom(root_text)  # at most 1 byte order mark, once
    mirror_text = strip_bom(mirror_text)  # as for the root
    cutoff = CUTOFF_PR
    # Entry classification, on the raw surfaces and BEFORE any deferral: the root must follow
    # its grammar (root_findings) and every mirror entry candidate must fully match a
    # comparison shape or a named exempt shape; an old-repository record
    # (dated before EPOCH_START), an unparseable date, a PR below CUTOFF_PR, a legacy line
    # naming more than 1 PR and every other shape fail here, so none can be deferred into a
    # silent pass. Failing lines are left out of the comparison so they cannot mask a new PR.
    root_found = root_findings(root_text)
    mirror_found = entry_findings(mirror_text)
    root_skip = root_found.lines()
    mirror_skip = mirror_found.lines()
    root_records = [r for r in pr_headers(root_text, cutoff=cutoff, root=True)
                    if r[0] not in root_skip]
    scope = store_scope(root_text, repo_root=scope_root)
    if scope.note:
        print(f"note: {scope.note}")
    mirror_lines = mirror_text.splitlines()
    flags = store_deferral_flags(mirror_lines, scope)
    mirror_records: list[tuple[int, int, tuple[int, int, int] | None, str]] = []
    deferred = 0
    for record in pr_headers(mirror_text, cutoff=cutoff):
        if record[0] in mirror_skip:
            continue  # already a failure (entry classification); never offered to deferral
        # Deferral is decided from EVERY PR the header line names (the shared parser), never from
        # this gate's single-PR record, and only when that record's own key is AMONG them (one
        # PR-key rule for the record and the deferral decision; a greedy-parsed key outside the
        # PR cell, or a line the shared parser cannot read, is ambiguous and kept, fail closed).
        # record[0] is the 1-based line number pr_headers assigned over the same splitlines()
        # view; a deferred header defers every PR it names, and the note reports them all.
        # The branch's declared own PR is never deferred, whatever the shared flags say.
        line_deferred, line_prs = flags[record[0] - 1]
        own = scope.own_pr is not None and scope.own_pr in line_prs
        if line_deferred and record[1] in line_prs and not own:
            print(store_deferral_note(line_prs, scope, str(detailed_mirror), record[0]))
            deferred += 1
        else:
            mirror_records.append(record)
    root_counts = Counter(pr for _, pr, _, _ in root_records)
    mirror_counts = Counter(pr for _, pr, _, _ in mirror_records)

    missing = sorted(set(root_counts) - set(mirror_counts))
    extra = sorted(set(mirror_counts) - set(root_counts))
    dup_root = sorted(n for n, c in root_counts.items() if c > 1)
    dup_mirror = sorted(n for n, c in mirror_counts.items() if c > 1)
    order_root = ordering_violations(root_records)
    order_mirror = ordering_violations(mirror_records)
    version_diff = version_mismatches(root_records, mirror_records)

    problems = (root_found or mirror_found or missing or extra or dup_root or dup_mirror
                or order_root or order_mirror or version_diff)
    if not problems:
        shared = len(set(root_counts))
        print(
            f"OK: root and detailed-mirror CHANGELOG per-PR headers match "
            f"for all {shared} PR(s) at or above #{cutoff}, each "
            f"file's Library Versions strictly decrease top-down, and every "
            f"shared PR carries the SAME Library Version in both files."
        )
        if shared == 0:
            print_degraded(
                "gate 59",
                "gate 59 compared no PR: no per-PR header dated on or after "
                f"{EPOCH_START} was left to compare in either file after store-scope "
                f"deferral ({deferred} detailed-mirror header(s) deferred); this pass "
                "attests nothing about header parity."
            )
        return 0

    print_entry_failures(f"root {ROOT_CHANGELOG_REL}", root_found, ROOT_EXPECTED_SHAPE)
    print_entry_failures(f"the detailed mirror ({detailed_mirror})", mirror_found)
    if version_diff:
        print(
            "FAIL: PR(s) present in BOTH files with DIFFERENT Library Versions "
            "(the mirror and the root must agree; the shipped version is the one "
            "in README.md at that PR's merge commit): "
            + ", ".join(
                f"#{pr} root={root_text} mirror={mirror_text}"
                for pr, root_text, mirror_text in version_diff
            )
        )
    if missing:
        print(
            "FAIL: PR header(s) present in root .working/CHANGELOG.md but MISSING from the "
            f"detailed mirror (>= #{cutoff}): "
            + ", ".join(f"#{n}" for n in missing)
        )
    if extra:
        print(
            "FAIL: PR header(s) present in the detailed mirror but MISSING from root "
            f".working/CHANGELOG.md (>= #{cutoff}): "
            + ", ".join(f"#{n}" for n in extra)
        )
    if dup_root:
        print(
            "FAIL: PR header(s) appearing more than once in root .working/CHANGELOG.md "
            f"(>= #{cutoff}): " + ", ".join(f"#{n}" for n in dup_root)
        )
    if dup_mirror:
        print(
            "FAIL: PR header(s) appearing more than once in the detailed mirror "
            f"(>= #{cutoff}): " + ", ".join(f"#{n}" for n in dup_mirror)
        )
    if order_root:
        print(
            f"FAIL: root .working/CHANGELOG.md Library Version ordering violated "
            f"(>= #{cutoff}):"
        )
        for v in order_root:
            print(f"  {v}")
    if order_mirror:
        print(
            f"FAIL: detailed-mirror Library Version ordering violated "
            f"(>= #{cutoff}):"
        )
        for v in order_mirror:
            print(f"  {v}")
    print(
        "\nThe root .working/CHANGELOG.md and its maintainer-grade detailed mirror "
        "must carry the same "
        "per-PR header set, with each file's Library Versions strictly "
        "decreasing top-down. Add the missing entry, reconcile the duplicated / "
        "orphaned header, or re-version the out-of-order entry so the two "
        "surfaces stay in lock-step. Old-repository records dated before "
        f"EPOCH_START {EPOCH_START} must be archived out of both surfaces, and every "
        "dated header must carry a valid YYYY-MM-DD date in a shape gate 59 can compare, "
        "with one header per PR. Above its first ## Week of heading the root must hold only "
        f"the lines of the root grammar, and at or below it only {ROOT_WEEKLY_LINES}."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
