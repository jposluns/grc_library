# Evidence-Grounded Completion Claims

Never declare a piece of work "done", "complete", "fixed", "shipped", "ready", "resolved", "merged-and-clean", or any synonym without evidence that supports the claim. The cost of an unsupported completion claim compounds: a downstream reader, reviewer, or operator trusts the claim and skips their own verification, and a defect that the claim missed proceeds further into the system.

This rule applies to human developers and to AI coding assistants equally; in practice it is binding more often on AI assistants, because the failure mode (declaring victory based on inference rather than observation) is the dominant pattern when an assistant feels pressure to summarise progress.

The rule is a discipline, not a vocabulary ban. The words above are fine when an evidence-grounded verification supports them. The words are forbidden when they are decorative narration.

---

## What counts as a completion claim

Any statement that asserts a state about the work, rather than describing an action you just performed. Both of these are completion claims:

- "The bug is fixed."
- "All tests pass."

Neither of these is:

- "I just ran the test suite."
- "I edited `foo.py` to change the comparison from `==` to `is`."

The first pair makes assertions a reader will rely on. The second pair reports actions; the reader still has to do their own verification.

Synonyms that count as completion claims include: done, complete, completed, finished, fixed, shipped, ready, resolved, addressed, handled, sorted, taken care of, all set, good to go, merged-and-clean, green, passing, working, validated, verified (in the conclusory sense), confirmed, looks good, LGTM. "Good catch" is also a completion claim when used to acknowledge a user-reported issue: it implies the issue is now understood and being acted on, which is a state assertion the user will rely on.

---

## The verification protocol

Before stating a completion claim, perform every step:

### 1. Enumerate every file in scope

List, by path, every file you touched or made claims about in this round of work. Files you read but did not touch count if your claim references them; files unrelated to the claim do not.

If the round of work was large, "this round of work" is the set of files relevant to *the claim you are about to make*, not every file the agent has ever touched in the session.

### 2. Re-read each file in full

Not just the section you edited. Not just the lines around the diff. The full file, or, for very long files where re-reading is impractical, the sections that are relevant to the claim plus an explicit statement of which sections were read and which were not.

The re-read is the step that catches stale claims: a preamble that contradicts a body change, a downstream reference that the edit broke, a CHANGELOG entry that lists files the actual diff did not touch.

### 3. Quote specific lines that support each claim

Paraphrases do not count. For each completion claim, identify the lines in the re-read files that ground the claim, and quote them (with file path and line number) in the message that carries the claim.

If a claim depends on a passing audit, gate, lint, or test suite, the supporting evidence is the gate's output and exit code, not "I ran it and it looked fine". Quote the relevant lines from the output.

### 4. Proactively search for contradictions

For each completion claim, run a search across the affected files for phrases that would *falsify* the claim if present. Report the search command and its result.

Examples of contradiction searches:

- For "the README is updated to v1.8.0": grep the README for `1.7` and any earlier version string. If a stale reference appears, the claim is not yet supported.
- For "the new rule is wired into all four surfaces": grep the four surface files for the rule's name. If any one is missing, the claim is not yet supported.
- For "the version-monotonicity audit passes": run the audit standalone (not piped through `tail` or `head` or `grep`, where a non-zero exit code can be masked) and report the actual exit code.

A contradiction search that returns nothing is evidence. A contradiction search that was not performed is not.

### 5. Distinguish mechanical from semantic verification

A passing gate, lint, or test suite proves only what that gate covers. The audit programme verifies the things the audit programme was built to verify; it does not verify everything.

"All 32 gates pass" is evidence for the claims those 32 gates check. It is not evidence for claims those gates do not check, such as "the rule is internally consistent with the project's existing discipline", "the prose is accurate", or "the references are not stale". Those claims require a separate verification protocol (re-read, quote, contradiction-search) of their own.

State the boundary explicitly: "All 32 gates pass; the gate-coverage limits mean this does not by itself prove [list of unchecked claims]; I have also verified [list of separately-verified claims] by re-reading and quoting from [files]".

### 6. State unverified items explicitly

If part of the claim is unverified, name the unverified part. Do not imply verification you did not perform.

"The CHANGELOG entry is added and links resolve; I have not separately checked that every downstream document that cites the bumped version has been updated, because that audit is not part of the 32-gate programme and I did not run it manually" is honest. "Done" with no scope is not.

---

## Prohibited anti-patterns

- **Declaring victory in the response that carries the failing evidence**. If the same message contains "all gates pass" and a tool result showing a non-zero exit code, the claim is incoherent. Read the tool result before composing the summary.
- **Treating "the user did not push back" as confirmation**. Silence from the operator is not a verification step. The user may not have noticed.
- **Relying on prior runs**. "It passed last time, and the only change is small" does not substitute for running the gates on the current state. The whole point of the audit programme is that "small" changes break things.
- **Saying "good catch" to a user-reported issue without first verifying that the issue is real and bounded**. "Good catch" implies "you caught what I should have caught, and I now understand the scope". If you have not yet enumerated the scope, you do not yet know whether the catch is one stale claim or ten.
- **Stating a claim and immediately performing the search that would have falsified it**. The search is part of the claim, not a coda. Run it first.
- **Hedging with "should" or "appears to" while still making a state assertion**. "The fix should work" or "the entry appears to be present" are still claims a reader will rely on. Either you ran the verification (state the result) or you did not (state the gap).
- **Conflating "I edited the file" with "the file is correct"**. The edit happened; the file's correctness is a separate proposition that needs its own verification.
- **Bypassing the verification protocol to make progress faster**. The protocol exists precisely because skipping it is the failure mode. The minute saved by skipping is paid back many times when the unsupported claim turns out to be wrong.

---

## Tool-specific guidance for AI coding assistants

### Reading tool results

A tool result (subagent return, bash output, file read) is the source of truth. Read it before composing the summary. If it contains an error, a failure indicator, or unexpected content, address that before proceeding.

A common failure mode is composing the next message in parallel with the tool call and committing to a summary before reading the result. Resist this; the summary is downstream of the result, not upstream of it.

### Async work

When a background task is in flight, do not begin work that depends on its output. Wait for the completion notification, read the full result, and then act. Forecasting the result and proceeding optimistically is the failure mode this rule is designed to prevent.

### Pipe-masked exit codes

When verifying via a command pipeline, the pipe can mask the verification command's exit code. Use one of:

- Run the verification standalone first, observe its result, then act in a separate step.
- Use `set -o pipefail` so the pipeline's exit code reflects the first failure.
- Inspect `${PIPESTATUS[@]}` after the pipeline.
- Run with no pipe and accept the full output.

Never chain a verification step with a dependent action step using `&&` when the verification's exit code may be masked. Concretely: `audit-script | tail && commit` is forbidden when `audit-script` can fail in a way the pipe hides.

### Stop hooks and pre-commit failures

A failing pre-commit hook, a stop-hook warning, or a "this branch has uncommitted changes" notice is signal, not noise. Address the underlying state. Do not bypass with `--no-verify` (see the gate-discipline rule) and do not treat it as a UI annoyance.

### Self-honesty in summaries

When narrating what you did, describe what actually happened, not what you intended. If you committed before noticing a failure, say so plainly. If you needed to amend, the amendment is part of the story. If you took a shortcut, name it.

The cost of plain narration is small (one extra clause); the cost of softened narration is large (a misled reader who relies on the softer claim).

---

## Exception-handling protocol

For genuinely impractical re-reads (a generated file that is millions of lines long, a binary artefact, a third-party dependency that you cannot read in full), state the scope of what you read and what you did not. The exception is not "I skipped the re-read"; the exception is "I read sections A, B, and C; I did not read sections D and E because [reason]; here are the claims my re-read supports and the claims that remain unverified".

---

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | OWASP ASVS |
| --- | --- | --- | --- | --- |
| Evidence-grounded assertions | RV.1, RV.2 | GRC-05, LOG-02 | A.5.36, A.8.15 | V1.1, V14.1 |
| Distinguishing mechanical from semantic verification | RV.1 | GRC-05 | A.5.36 | V14.1 |
| Documented exception handling | PO.5 | GRC-04 | A.5.4 | V1.1 |
| Audit trail of verifications performed | PS.1, RV.2 | LOG-02, LOG-08 | A.8.15, A.5.36 | V14.1 |

---

## Why this rule exists

The classic failure mode this rule addresses: an AI coding assistant runs a passing audit, infers that the work is done, writes "all gates pass; ready to ship", and is wrong because the audit covered some claims and not others. A reviewer reads the summary, trusts the assistant, and the unsupported claim lands.

The discipline reverses the flow. The summary is composed *after* the verification, *from* the evidence, not from inference. The vocabulary of completion ("done", "fixed", "ready") becomes a flag that the assistant must satisfy the protocol before emitting; the protocol is mechanical (enumerate, re-read, quote, contradiction-search) so it can be checked without subjective judgement.

The cost of the protocol (a few extra tool calls and a more careful summary) is small. The cost of an unsupported completion claim that lands and gets relied on (a defect that ships, a reviewer's trust eroded, a user who later has to catch what the assistant should have caught) is much larger. The asymmetry justifies the discipline.

For AI coding assistants specifically: if a user catches an inconsistency that this rule's protocol would have caught, the right response is not "good catch" (which implies you understood and have it under control). The right response is "you caught what I should have caught; rerunning the verification protocol now", followed by actually rerunning the protocol.
