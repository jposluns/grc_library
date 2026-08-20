# Worker dispatch mechanics (reference)

**Read this at the worker-dispatch boundary, like a skill: when constructing or pinning a worker
order, or dispatching one and reading its result back.** [`.claude/CLAUDE.md`](../.claude/CLAUDE.md)
carries the lean always-on core (the two clauses whose blast radius reaches beyond this activity);
this file carries the full mechanics. The companion playbook
[`worker-offload.md`](worker-offload.md) covers WHETHER to offload and to which family; this one
covers HOW to construct the order and get the result back.

This is project-only operational machinery, not pack material.

## The transport

Dispatch is the shared `orch` harness. `orch-verify <family> <prompt-file> [workdir] [options]` runs
ONE read-only worker to completion and returns its stdout plus a `WORKER_STATUS` line reporting the
account, model, effort, and return code. `orch --help` and `orch-verify --help` are the authority on
options and defaults; treat anything written here about specific flags as secondary to them.

Consequences of the transport that shape every order:

- **Workers are READ-ONLY.** A worker cannot commit, push, or edit. It inspects and reports. Any
  change it proposes is a CANDIDATE the orchestrator applies and verifies (the research-assistant
  discipline in the `ai-assistant-workflow-disciplines` pack rule).
- **Results arrive on stdout and are not persisted for you.** Redirect at dispatch. An uncaptured
  result is a lost result.
- **Every worker is SINGLE-SHOT.** There is no resumable worker session, so scope each order to one
  self-contained pass. Work that needs a second round is a second order carrying forward whatever
  context the first produced.
- **A worker sees the working tree it is pointed at.** Where the orchestrator may edit that tree
  concurrently, the worker can observe half-applied state; pin the order to a commit and say so.

## Pinning an order

**Pin an order to a commit that CONTAINS what it references.** For a backlog item N, that is the commit
that CREATED item N, not a later one; for a diff review, the commit under review; for a corpus sweep,
the merge commit the sweep is meant to cover. A branch head is never a pin: a squash-merge deletes it,
and the order then references a commit that no longer exists.

**Commit the artefact BEFORE dispatching QA on it.** An uncommitted artefact does not exist at the
pinned revision, so the worker either reports it missing, or reads the working tree and reviews a
moving target while the orchestrator keeps editing. A worker that REFUSES an uncommitted basis is
correct, and its refusal is a finding about the DISPATCH, not an unhelpful worker: fix the dispatch,
do not re-brief the worker to be more accommodating.

**Pin the reference base too.** An order that reads `grc_library_ref` names the `_ref` commit it may
read at. Without that pin a worker operating under a provenance rule cannot quote held source and will
correctly return a hold.

## Constructing the brief

- **State the procedure, do not assume it.** Point the worker at the skill or rule that defines the
  formal shape of the pass, and tell it to execute that as written.
- **Give it the asserted-clean set.** Say which surfaces a prior session asserted clean, so a
  contradiction can be flagged as a MISS-SIGNAL rather than triaged as an ordinary finding.
- **Demand grounded findings.** Every positive finding carries a path, a line, the quoted offending
  text, the ground-truth quote that contradicts it, and a severity. A finding that cannot be grounded
  in a quote is not a finding, and the brief should say so, so the worker reports nothing rather than
  padding.
- **Require an honest mechanical section.** Ask for the command's own output, and require an
  UNRUNNABLE check to be reported as unrunnable. Never let a brief's own asserted values be restatable
  as if measured; that is precisely how a fabricated proof-of-run gets produced.
- **Name the read-only constraint explicitly**, including inspecting version-control history read-only
  (`git show <ref>:<path>`, `git diff`, `git log`) and never moving the working tree's HEAD.
- **Give parallel same-brief dispatches distinct output paths.** Two families running one brief will
  otherwise collide on a content-derived name and one will overwrite the other.

## Reading the result back

- **Read the FULL substantive output, never a truncated tail.** Map its structure first (verdict,
  findings, proof-of-run), then read each section. A tail-and-conclude read once landed mid-file and
  nearly produced a false reading of a verifier's verdict.
- **Every POSITIVE finding is re-verified at source before it is routed.** A worker finding is a
  hypothesis. A clean zero-finding result is trusted on its proof-of-run.
- **Check the proof-of-run against what the worker could actually do.** A mechanical result a
  read-only or plan-mode worker could not have produced is fabricated, however plausible its numbers.
- **Reconcile the panel, do not average it.** A finding raised by one family only is triaged on its
  own merits; agreement between families is corroboration worth recording; a disagreement is itself a
  signal about which family was right, and belongs in the QA record.

## Re-issuing

A worker silent past 20 minutes gets the SAME order issued to a distinct account, and whichever
returns FIRST is authoritative. The late delivery is then read as a CROSS-REFERENCE only, to confirm
the accepted result missed nothing; it is never re-adjudicated as a competing verdict. Duplicating a
read-only order costs a worker cycle and nothing else, which is what makes this safe: it converts a
stalled order from an indefinite block into a bounded one.
