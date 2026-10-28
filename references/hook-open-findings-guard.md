# `block-on-open-findings.py`: full mechanics

Reference detail for the `block-on-open-findings.py` PreToolUse hook. CLAUDE.md carries the
one-paragraph summary and points here for the complete behaviour. The authoritative source is the
hook's own docstring; this file mirrors it for readers who should not have to open the code.

## Why it is a hook and not a convention

The convention ("a delivered QA result blocks progress until read and dispositioned") existed and
failed twice in one day on the same axis. Its scope hole: it covered findings arriving FROM WORKERS
and said nothing about findings the orchestrator generates ITSELF. On 2026-07-25 two live defects in a
file-moving tool, produced by the orchestrator's own probe minutes earlier, were rendered as a table
row and walked past in favour of writing a summary statistic about them. Reading a finding is not
acting on one, and the gap between those two is where the cost lives, so the block is mechanical.

## What it reads

The hook reads `open-findings.md` via `lint_common.resolve_working`, taking the first existing of: an
eligible operational store (`$GRC_STORE`, or `<repo-parent>/private` by default
for this checkout; used only when it is a directory resolving OUTSIDE the repo), then `<repo-parent>/grc_library_private/.working/open-findings.md`, then the in-repo
`.working/open-findings.md`. If the helper cannot be imported it checks only the in-repo path; a missing
or unreadable selected ledger fails open. Its `## Open` table carries one row per
confirmed defect with a severity and a disposition. A row with an EMPTY disposition is undispositioned.
A row leaves the ledger only via `FIXED`, `ROUTED`, `REFUTED`, or `ACCEPTED`.

`FIXED` and `ROUTED` require an adjacent reference: a PR (`#1178`), a backlog item
(`3.73`, `3.56a`, `3.139.1`, `P-1.71`, `3b108`, `3b50c`), a TODO-qualified dotted item
(`TODO 3.73`, `TODO P-1.60`), a private operational-store commit
(`store:abcdef0`, 7 to 40 lowercase hex characters), or a maintainer egress-list entry
(`egress:request-1`, ASCII letters, digits, dots or hyphens, starting and ending with
a letter or digit, naming an entry in `maintainer-egress-requests.md`). Both new forms work after either disposition.
A simple letter-suffixed backlog id is digits + `b` + digits + one lowercase letter
(`3b50c`). Any following character other than a letter, digit or hyphen
(including a full stop) is allowed; parentheses and trailing prose are allowed.
`3b50cc`, `3b50c-`, `3b50c1x` and `3b50cX` are not. Existing letter-digit series
such as `3b5c0` and `3b50b2e1` remain valid.
Whitespace and inline markup may separate the word and reference, as in
`` **FIXED** `store:abcdef0` `` and `ROUTED **egress:request-1**`.
The letter-suffixed id is a legacy-shaped reference: colon separators and inner
markup behave as for legacy references (`FIXED: #1178`, `FIXED: 3b50c`).
The `store:` and `egress:` forms reject colon separators (`FIXED: store:abcdef0`)
and inner markup. Prose may follow a reference; a full stop immediately after a
store SHA is allowed and is not part
of the reference (`FIXED store:abcdef0. Then prose`). These checks validate syntax
only, not the existence of the commit or entry. `REFUTED` and `ACCEPTED` require only
the terminal word; evidence and rationale remain author judgement.

## What it blocks (two conditions)

1. **Undispositioned `error` row (primary).** An `error`-severity row with no disposition blocks
   a Bash command whose whitespace-collapsed text contains the case-sensitive substring `gh pr create`
   or `gh pr merge`, or whose shell tokens have `gh`, then `pr`, then `create` or `merge`, with no fresh
   `gh` between (so a quoted `gh pr 'merge'` is caught, and `echo "gh pr merge"` and
   `gh pr view 1 && git merge x` are gated; this is text matching, not a shell model, so a command run
   through another shell or `eval`, fed on stdin or through a heredoc, built from a variable or an alias,
   quoted in a way shlex reads differently from bash, or split by a mix of continuations bash joins and
   does not, can evade when the hook does not see `gh`, `pr` and the verb as one command's words; 3b112), or a command that mentions `tools/merge-when-green.py` other than as a single simple
   `--dry-run` or `--self-test` command (over-gated by intent, since shell parsing cannot find every
   way to run it; `merge-when-green.py` also applies this guard's decision itself; the text match is a speed bump for an
   honest actor's slip, not an adversarial control, so a deliberately obfuscated command can still evade it; 3b108), because shipping past a known wrong behaviour is the thing worth
   preventing. A `warning` does NOT block a PR (an in-flight change should finish rather than be
   abandoned half-landed) and is surfaced instead. Notes never block.
2. **Mis-filed finding-row (second condition, P-1.70, 2026-09-10).** A row carrying the finding-row
   shape but sitting BEFORE the scanned sections open (in the preamble above `## Open`, or stranded by
   a phantom heading between `## Open` and `## Closed today`), so it escapes the disposition scan and also
   blocks (any severity/disposition). The legitimate post-`## Closed today` archive is
   location-EXEMPT (a row there is indistinguishable from an archived one). This covers the
   push→merge edit window that the pre-push D14 check cannot see.

## Fail-open by design

If the ledger is missing or unreadable this hook ALLOWS the action, because a guard that blocks all
work on its own malfunction would be removed within a day, and a removed guard protects nothing. A
single MALFORMED row (wrong column count, e.g. a stray unescaped pipe) UNDER `## Open` is the
exception: the parser forces it toward BLOCK (not open), so it cannot silently disable the guard. (A
malformed row under `## Closed today` or the dated archive is out of the Open-scoped scan, so it
neither blocks nor fails open.) The fail-open trade is deliberate: the ledger plus the convention are the primary control and this hook is defence
in depth. Conventions alone failed repeatedly on this axis in quick succession, which is why there is
a hook at all.

## Class-completeness attestation (P-1.67, advisory here)

A `Finding` cell that LEADS with a bracketed class token names a CLASS of defect, so its `FIXED`
disposition must attest the fix was checked at the width of the class: a `[class: "<token>" @ <count>]`
clause (emitted by `tools/check-class-completeness.py --attest`) or a `[class-exempt: <reason>]` from a
closed set. A `FIXED` class row under `## Open` missing the attestation is SURFACED AS A WARNING here, never a block
(preserving the fail-open posture); the fail-closed half is the pre-push D14 check
(`tools/check-class-attestation-on-pr.py`), which also reproduces the probe.


## Writing rows (`tools/open-findings-row.py`, 3b334)

Write a ledger row with `tools/open-findings-row.py` rather than by hand. The tool checks one row with
this hook's own functions, loaded from the same checkout as `merge-when-green.py` loads them, and then
inserts the row in place atomically. It defines no grammar of its own, so it cannot accept a row that
this hook reads differently.

```text
python3 -I tools/open-findings-row.py --id ID (--after ANCHOR_ID | --append) [--ledger PATH] [--dry-run] [--open] [--delivery PATH [--source-key KEY]] < row
python3 -I tools/open-findings-row.py --set-disposition --id ID [--ledger PATH] [--dry-run] < cell
```

- **Input and output.** One table line on stdin (for `--set-disposition`, the new Disposition cell instead; see below), never in argv. The output carries line numbers,
  verdict codes and counts, never row text or ids.
- **Finding id.** The leading bracketed token of the Finding cell (`[VPR3B330-PR8-R1]`). `--id` is that
  token without brackets; for the row-adding modes it must be unique across `## Open`, `## Closed today`, and unfenced
  archive or mis-filed rows that the hook's `MISFILED_ROW_RE` matches. This hook reads the same token as a class token, so a `FIXED` row needs a
  `[class: ...]` or `[class-exempt: ...]` clause.
- **Placement.** `--after ANCHOR_ID` inserts after the one `## Open` or `## Closed today` row led by that
  id. `--append` inserts after the newest dated `## Open` row (a tie goes to the last in file order),
  not blindly at end of file; an Open table with no dated row is refused.
- **Refusals (exit 1), row-adding modes** (`--set-disposition` has its own, below). A row this hook would parse as malformed; a severity outside `error`,
  `warning` and `note`; an `error` or `warning` disposition that fails the grammar (for example
  `FIXED (d44d9b2b)`, `ROUTED pending-decisions` or `FIXED d44d9b2b`); a `FIXED` class row without a
  valid clause; more than one clause on any row; a duplicate or mismatched id; a missing or ambiguous
  anchor; and any splice this hook would read as anything other than the earlier rows plus the new one.
  The new row must have a valid ISO Found date (`YYYY-MM-DD`), or `found-not-iso` refuses it.
  Note dispositions are not grammar-checked, as here, but their columns and clause count are.
  Refusing an unattested `FIXED` class row is deliberately stricter than the merge guard warning,
  matching the D14 pre-push check.
- **`--open`.** Records an `error` or `warning` row with an empty disposition. Without the flag such a
  row is refused. With it, an empty error row makes the merge guard block the merge while an empty warning row is
  surfaced without blocking. Either row must not land in `## Closed today`, which this hook does not scan.
- **Class count (report only).** For a `FIXED` row with a `[class: "<token>" @ <count>]` clause, the tool
  re-runs the `check-class-completeness.py` probe on the current checkout and warns when the count
  differs. It does not refuse, because an in-flight branch can differ from this tree; D14 remains the
  pre-push check.
- **Delivery findings (report only, 3b544).** `--delivery PATH` names the review delivery the row
  records (mistakes register 312). The tool prints one `delivery-findings:` line beside the class
  count: the totals of the delivery's last `FINDINGS:` line and the number of ledger rows whose Source
  cell starts with the delivery's own review key, `<family> <item> /validate-pr round <n> @ <sha>`,
  with a warning when there are fewer rows than findings. A row counts only when the key in its Source
  cell is not followed by an ASCII letter or digit, `_` or `-`. The family comes from the delivery's
  `WORKER_STATUS` first line, and the item and sha from its `VPR-COMPLETE` line. The round is often
  absent: it comes only from a `# /validate-pr round <n> (REFUTE...): <item>, ...` heading whose item
  field is the item and that is the delivery's first heading, and neither sample delivery staged for
  3b544 carries one, so such a delivery prints `UNVERIFIABLE (no-round-heading)`. The round number
  `<n>` is a positive integer in ASCII digits with no leading zero, so a heading with `round 0` or
  `round 03` is not a round heading. A heading's item field is read exactly so (3b578): after the
  round number, one or more spaces or tabs, then `(REFUTE` in uppercase, closed by its first `)`,
  which a `:` must follow; then the text up to the first comma or the line end, spaces and tabs
  stripped, which must be one item token (ASCII letters, digits, `.`, `_` or `-`, starting and ending
  with a letter or digit, as in `VPR-COMPLETE`). A heading whose item field is another item names no
  item, even when it mentions the item later. A heading with no item
  field (for example `(refute)`, text before `(REFUTE`, a `)` inside its parentheses, no colon after
  them, or a field that is empty, backticked, or holds a space or a no-break space) gives no round,
  but it names the item when it holds it as a whole token (not next to an ASCII letter or digit, `_` or `-`),
  so it still counts toward `round-heading-ambiguous` below (3b578 r2). The orchestrator should pass
  `--source-key` when it knows the round. `--source-key` gives the whole key; a part the delivery
  carries must agree with it. Without that, a missing, unreadable or conflicting part prints
  `UNVERIFIABLE` with a code instead of a count, never a broader count or a zero. Rows of another
  family, round or sha are not counted, with one stated residue: a round heading after another heading
  is a quote and gives no round, but a delivery whose first heading quotes another round's heading for
  the same item at column 0 still takes that round's key, even when its own headings follow the quote
  (only an unfenced ATX heading before the quote stops it; a setext, HTML, block-quoted or list-item
  heading does not). With `--source-key` that case prints `UNVERIFIABLE (source-key-disagrees)`
  instead. The item field narrows two checks (3b578): a heading whose item field is another item never
  counts toward `round-heading-ambiguous`, even when it mentions the item later, and a heading with no
  item field gives no round, so with `--source-key` it cannot disagree with the key's round and only
  counts toward `round-heading-ambiguous`.
  A delivery that cannot be read (missing, unreadable, not a regular file or not UTF-8), that has no
  column-0 `FINDINGS:` line outside fences, or whose last such line does not parse prints
  `delivery-findings: UNVERIFIABLE (<code>)` and compares nothing, whatever its other parts and
  `--source-key`; the codes below apply only beside parsed totals.
  Outside fences, two column-0 `# /validate-pr round <n>` headings naming the item (the key's, with
  `--source-key`) with different rounds, own or quoted, wherever they stand, make the count
  `UNVERIFIABLE (round-heading-ambiguous)`, even with a correct `--source-key`. Three cases print
  another code instead, the first that applies in this order: a part the delivery carries that does
  not parse prints its code (for example `worker-status-family-unparseable` for an empty `family=`),
  with or without `--source-key`; a `--source-key` not in the key's form prints `source-key-invalid`;
  and without `--source-key`, a delivery with no `VPR-COMPLETE` line prints `no-vpr-complete-line`,
  since no item is known. A delivery with no `WORKER_STATUS` first line, so no family, or with no
  own round heading does not; a `WORKER_STATUS` first line without exactly one valid `family=` value
  (none, two, or an empty one) is a part that does not parse, and so is one whose envelope,
  `WORKER_STATUS: <STATUS> (...)`, does not parse, even with one valid `family=` value: for example
  one with no parentheses, or one whose status is not one or more ASCII uppercase letters (A to Z),
  such as an empty status or one holding a digit, `_`, or a letter outside A to Z (lowercase,
  accented or full-width). A `WORKER_STATUS` first line is a first line that starts with
  `WORKER_STATUS:` at column 0, case and colon exact: an indented first line, a lowercase one
  (`worker_status:`), and one with no colon or a space before the colon (`WORKER_STATUS PASS`,
  `WORKER_STATUS : PASS`) are not `WORKER_STATUS` first lines, whatever follows, so such a delivery
  has no family. A byte-order mark before `WORKER_STATUS` makes the first line not a
  `WORKER_STATUS` first line, so such a delivery has no family. A Source cell that states
  the review in another form than the key (other case or spacing, prose before it, or a shorter sha)
  is not counted, so the count errs low, toward the warning. A combined row counts once, and two
  deliveries with one key share their rows. The line carries counts and codes only, never refuses,
  never blocks the write and never changes the exit code.
- **Environment (exit 2).** This hook cannot load; the ledger is missing, unreadable, a symlink,
  hard-linked or owned by another user; its line ends disagree with this hook's line model; or the file
  changed between read and write (including ctime, mode, uid, gid or access ACL). The write keeps
  the file's uid, gid, mode and POSIX access ACL; a group that cannot be preserved refuses with
  `ledger-group-unpreservable`. `write-failed` reports an opening, write or rename failure before
  the rename succeeds. `written-dir-fsync-failed` means the rename happened but directory durability
  could not be confirmed. `post-write-readback-failed` means the rename happened but the read-back
  itself failed; `post-write-mismatch` means the read-back succeeded and the file does not read back
  as written. A failed temp-file close or unlink during cleanup never replaces the error already in
  flight: the tool prints the original error line, then a second line, `error: temp-cleanup-failed`,
  still exit 2. Unexpected exceptions report `error: internal`, followed by that same second line
  when the temp-file cleanup also failed. A failed close of the parent directory fd never replaces
  the error in flight either and adds no line, since it leaves nothing on disk to clean up. With no
  error in flight, that close runs only after the rename and a verified read-back, so its failure
  prints `error: internal`, still exit 2, while the ledger already holds the new row.
  `--ledger` values ending in `/` or `/.` are usage errors. Relative paths become `Path.cwd() / path`
  without additional normalization or symlink resolution, preserving kernel `link/..` semantics.
  Writes open the parent once with `O_DIRECTORY|O_NOFOLLOW`; temp creation, identity re-check,
  replacement, cleanup and read-back use that directory fd, which is also fsynced. An immediate
  symlink parent refuses with `ledger-parent-symlink` (decided by `lstat` when the parent open
  fails). Missing directory-fd support refuses with `ledger-dir-fd-unavailable`;
  there is no pathname-based fallback. `--dry-run` runs the same pre-flight (the directory-fd
  capability check and the `O_DIRECTORY|O_NOFOLLOW` parent open), so it refuses whatever that
  pre-flight refuses; later write stages can still refuse a real write.
- **Stated residue.** The letter-series and letter-suffixed ref shapes (`3b108`, `3b50b2e1`,
  `12b345a`) overlap hexadecimal, so a short SHA such as `1b2e3a4` or `12b345a` passes as a ref
  in the tool and in this hook. Closing it needs a hook grammar change. There is no shared lock: a write between the re-check and the rename, or by a writer
  holding the old inode open, is lost. Extended attributes other than the access ACL are not carried
  over; access ACL handling uses Linux xattrs.
- **Setting a disposition (`--set-disposition`, 3b678).** Changes the Disposition cell of one
  existing row in place, for example `ROUTED <id>` to `FIXED #N (sha) [class: ...]` once the fix merges,
  which was done by hand. stdin carries the new cell text, never a row. The target is the one row in
  `## Open` or `## Closed today` whose Finding cell leads with `[ID]`; fenced lines, the dated archive
  and mis-filed rows are never targets. Only that row's last cell is replaced, written as one space,
  the cell, one space before a trailing border pipe, and as one space and the cell with no space after
  it on a row with no trailing border pipe (the hook strips the line, so it reads both the same); every
  other byte is kept. The changed row is held to the same checks as a new row, plus a re-parse that the
  hook reads the same rows with only that disposition changed and the merge guard's verdict before and
  after. It refuses an empty cell (it never writes an undispositioned row), no matching row, more than
  one, an unescaped pipe in the cell (`malformed-columns`, on every row shape, checked before the row
  is looked at), and anything the row checks refuse; `--after`, `--append`, `--open`, `--delivery` and
  `--source-key` are usage errors with it. The write and `--dry-run` use the same transaction and
  pre-flight as the other modes. The tool's docstring (`SET DISPOSITION.`) states its residues.

## Why a hard block: the motivating incidents

Relocated from `.claude/CLAUDE.md` `## A delivered QA result BLOCKS progress until it is read and its findings are fixed` (3b177-e); the always-on core stays inline.

**Maintainer-directed 2026-07-25, in capitals, after a large batch of QA deliveries sat unread in worker outboxes
while the orchestrator started new work.** This is the strongest form of the QA priority and it
overrides the queue: a QA result is not a document to get to, it is a STOP until actioned.

**SOURCE-INDEPENDENT (widened 2026-07-25, after the narrow version failed).** The QA-blocking rule in `.claude/CLAUDE.md` was
first written for QA arriving FROM WORKERS, and that scope had a hole almost immediately: live defects in
a file-moving tool, produced by the orchestrator's OWN instrument moments earlier, were rendered as a
table row and walked past in favour of writing a summary statistic about them. The severity of a defect
does not depend on who noticed it, so this covers ANY confirmed finding from ANY source: a worker
delivery, a gate run, an instrument the orchestrator just wrote, a maintainer observation, a self-caught
slip mid-edit.

**Why it is a hard block rather than a priority.** A finding nobody has read is strictly worse than
no QA at all, because the record shows the pass ran and so the surface reads as covered. On
one observed day that cost was concrete: an ERROR-severity finding on `manage-workers.py` and an
error-severity HOLD on an EU AI Act retention change that had already MERGED without human review
both sat unread while further PRs were built on top of them, and the retention finding
described a fact pattern in which records could be destroyed before a statutory keeping period
expires. The QA had already found it. Nobody had looked.
