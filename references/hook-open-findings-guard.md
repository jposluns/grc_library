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
python3 -I tools/open-findings-row.py --id ID (--after ANCHOR_ID | --append) [--ledger PATH] [--dry-run] [--open] < row
```

- **Input and output.** One table line on stdin, never in argv. The output carries line numbers,
  verdict codes and counts, never row text or ids.
- **Finding id.** The leading bracketed token of the Finding cell (`[VPR3B330-PR8-R1]`). `--id` is that
  token without brackets and must be unique across `## Open`, `## Closed today`, and unfenced
  archive or mis-filed rows that the hook's `MISFILED_ROW_RE` matches. This hook reads the same token as a class token, so a `FIXED` row needs a
  `[class: ...]` or `[class-exempt: ...]` clause.
- **Placement.** `--after ANCHOR_ID` inserts after the one `## Open` or `## Closed today` row led by that
  id. `--append` inserts after the newest dated `## Open` row (a tie goes to the last in file order),
  not blindly at end of file; an Open table with no dated row is refused.
- **Refusals (exit 1).** A row this hook would parse as malformed; a severity outside `error`,
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
  surfaced without blocking. Either row may not land in `## Closed today`, which this hook does not scan.
- **Class count (report only).** For a `FIXED` row with a `[class: "<token>" @ <count>]` clause, the tool
  re-runs the `check-class-completeness.py` probe on the current checkout and warns when the count
  differs. It does not refuse, because an in-flight branch can differ from this tree; D14 remains the
  pre-push check.
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
  when the temp-file cleanup also failed.
  `--ledger` values ending in `/` or `/.` are usage errors. Relative paths become `Path.cwd() / path`
  without additional normalization or symlink resolution, preserving kernel `link/..` semantics.
  Writes open the parent once with `O_DIRECTORY|O_NOFOLLOW`; temp creation, identity re-check,
  replacement, cleanup and read-back use that directory fd, which is also fsynced. An immediate
  symlink parent refuses with `ledger-parent-symlink` (decided by `lstat` when the parent open
  fails). Missing directory-fd support refuses with `ledger-dir-fd-unavailable`;
  there is no pathname-based fallback. `--dry-run` runs the same pre-flight (the directory-fd
  capability check and the `O_DIRECTORY|O_NOFOLLOW` parent open), so it refuses whatever that
  pre-flight refuses; later write stages can still refuse a real write.
- **Stated residue.** The letter-series ref shape (`3b108`, `3b50b2e1`) overlaps hexadecimal, so a short
  SHA such as `1b2e3a4` passes as a ref in the tool and in this hook. Closing it needs a hook grammar
  change. There is no shared lock: a write between the re-check and the rename, or by a writer
  holding the old inode open, is lost. Extended attributes other than the access ACL are not carried
  over; access ACL handling uses Linux xattrs.

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
