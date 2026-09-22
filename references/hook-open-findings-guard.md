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
eligible operational store (`$GRC_STORE`, or `<repo-parent>/private` by default, which is `/opt/grc/private`
for this checkout; used only when it is a directory resolving OUTSIDE the repo), then `<repo-parent>/grc_library_private/.working/open-findings.md`, then the in-repo
`.working/open-findings.md`. If the helper cannot be imported it checks only the in-repo path; a missing
or unreadable selected ledger fails open. Its `## Open` table carries one row per
confirmed defect with a severity and a disposition. A row with an EMPTY disposition is undispositioned.
A row leaves the ledger only via `FIXED`, `ROUTED`, `REFUTED`, or `ACCEPTED`.

## What it blocks (two conditions)

1. **Undispositioned `error` row (primary).** An `error`-severity row with no disposition blocks
   a Bash command whose whitespace-collapsed text contains the case-sensitive substring `gh pr create`
   or `gh pr merge` (it misses `gh pr 'merge'` and gates `echo "gh pr merge"`; it does not parse shell
   syntax), because shipping past a known wrong behaviour is the thing worth
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
