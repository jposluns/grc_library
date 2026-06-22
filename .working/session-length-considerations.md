# Session Length Considerations

**Purpose.** This file is a generic, informative lesson on a recurring phenomenon:
an AI coding assistant's reliability tends to degrade as a single working session
grows long. It explains *why* the degradation happens and *what a maintainer (or the
assistant itself) can do* to mitigate it. It is written for any reader, not as a
reply to any one question, and it is maintainer working state, exempt from corpus
audit gates per the `.working/` exemption.

The short version: a long session is not a more-informed version of a short one. It
is a session carrying more accumulated state, more diluted attention, and more
opportunities for a small early error to compound. Treat session length as a risk
factor, and manage it the way other risk factors are managed: with durable state,
mechanical gates, frequent checkpoints, and fresh starts at natural boundaries.

---

## Why longer sessions become less accurate

The mechanisms below are largely independent; a long session usually suffers several
at once, which is why the degradation can feel sudden rather than gradual.

1. **Context dilution and the "lost in the middle" effect.** An assistant attends to
   a finite context window. As the window fills with conversation history, tool
   output, and file contents, the *relative* salience of any one instruction drops.
   Information in the middle of a long context is recalled less reliably than
   information at the beginning or end, so a discipline stated early and not restated
   can quietly stop being applied. More context is not more understanding; past a
   point it is more noise competing for the same attention budget.

2. **Lossy compaction.** When a session exceeds the context window, the older portion
   is summarized and the summary replaces the raw history. Summarization is lossy by
   construction: nuance, exact quotes, the precise wording of a constraint, and the
   reasons behind a decision can be compressed away or subtly rephrased. After one or
   more compaction cycles, the assistant is reasoning from a paraphrase of a
   paraphrase, and details that were load-bearing may no longer be present in the
   form that made them correct.

3. **State drift and stale cache.** Early in a session the assistant reads a file, a
   version number, or a count, and forms a belief about it. The world then changes
   (commits land, versions bump, files move), but the belief persists unless it is
   re-validated. The longer the session, the more such beliefs accumulate and the
   greater the chance one is acted on after it has gone stale. This is the failure
   mode that "validate the premise before acting on it" exists to prevent, and it
   gets harder to honour as the count of in-flight premises grows.

4. **Error compounding without fresh eyes.** A small early mistake (a wrong
   assumption, a misremembered convention) becomes a premise for later work. Each
   subsequent step that builds on it inherits the error and adds confidence to it. By
   the time the error surfaces, several layers of work may rest on it, and the
   assistant that made the original mistake is the same one reviewing the later work,
   so it is unlikely to catch what it already believes is settled.

5. **Throughput pressure late in a session.** As a session accumulates completed work
   and a visible queue of remaining work, there is implicit pressure to keep the pace
   up. That pressure is exactly when verification steps get abbreviated, a check gets
   skipped "just this once", or a summary substitutes for a re-read. The pressure is
   strongest precisely when the other degradation mechanisms have already made
   shortcuts most dangerous.

6. **No reliable internal gauge of degradation.** The most important point, and the
   most uncomfortable one: the assistant has no dependable way to sense its own
   decline in real time. It does not feel tired or notice its context thinning. It
   will report confidence in a stale fact in the same tone it uses for a freshly
   verified one. Any mitigation that depends on the assistant *noticing* it has
   degraded is unreliable by design. The robust mitigations are the ones that do not
   require self-awareness of the failure.

---

## What helps

The mitigations fall into two groups: things that reduce reliance on the assistant's
accumulated in-session memory, and things that catch errors regardless of whether the
assistant noticed them.

### Reduce reliance on in-session memory

- **Start fresh sessions at natural boundaries.** At the end of a phase, a batch of
  changes, or a major task, prefer a new session over continuing a long one. A fresh
  session that rebuilds its state from durable artefacts is more reliable than a long
  one running on accumulated memory. This is the single highest-leverage habit.

- **Keep state in committed files, not in the conversation.** Anything that must
  survive into later work (decisions made, the queue of remaining work, version
  snapshots, open questions) belongs in a file in the repository, not solely in chat.
  A durable file is immune to compaction and can be re-read fresh; a fact that lives
  only in conversation history is exactly what compaction discards. A single,
  routinely-refreshed handoff file that a fresh session reads first turns "resume a
  long session" into "rebuild state from disk".

- **Prefer small, frequently-merged units of work.** Each merged change is a clean
  reset point: the durable state is consistent, the gates have passed, and a fresh
  session can pick up from there with minimal in-memory context. Large, long-running
  changes keep more unverified state live for longer.

- **Re-point the assistant at key files after a compaction.** If a session must
  continue past a compaction, explicitly re-reading the governing files (the project
  conventions, the current state snapshot) restores the load-bearing details that the
  summary may have flattened. Do not assume the post-compaction summary preserved
  them.

### Catch errors regardless of self-awareness

- **Lean on mechanical gates and fresh-context reviewers.** Deterministic checks
  (linters, audits, tests) and reviews performed in fresh context do not degrade as
  the originating session lengthens. They are the degradation-proof layer: they catch
  what a tiring session would miss precisely because they do not share its
  accumulated state or its blind spots. Routing important verification through this
  layer, rather than through the assistant's own end-of-session judgement, is what
  makes long work safe.

- **Watch for the tells, and nudge verification when they appear.** A maintainer
  observing the work can often see degradation before any single error lands. Typical
  tells: asserting a version number or a count without running a tool to confirm it;
  summarizing what a file says instead of quoting it; skipping a verification step
  that was honoured earlier in the session; growing confidence paired with shrinking
  evidence. The right response to a tell is a small, specific nudge ("re-read that
  file before you rely on it", "run the audit and quote the result"), which costs one
  round-trip and resets the assistant onto evidence.

- **Make the disciplines mechanical, not memory-dependent.** A discipline that
  requires the assistant to *remember* to apply it will eventually lapse in a long
  session. A discipline encoded as a checklist item tied to a concrete trigger (an
  audit that runs before every push, a close-out checklist enumerated in a file) is
  far more robust, because honouring it does not depend on the assistant's degrading
  recall.

---

## The deepest point

Do not rely on the assistant to notice its own degradation; it cannot do so reliably.
Build the workflow so that correctness does not depend on that noticing. Durable state
in committed files, mechanical gates and fresh-context reviewers, small and frequent
merges, and deliberate fresh sessions at boundaries together form a system whose
reliability is largely independent of how long any single session has run. The
assistant's accumulated in-session memory is the part that degrades; the less the
final correctness of the work depends on that memory, the less session length
matters.
