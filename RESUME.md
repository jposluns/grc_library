# Resuming a session (manual entry point)

This is the manual entry point for resuming a Claude Code session in an environment
where the `/resume` slash command is not available (for example, a machine whose Claude
Code does not discover this project's [`.claude/commands/`](.claude/commands/)). It
carries no protocol and no per-session state of its own by design, so it cannot drift
from the real resume behaviour.

To resume, execute the resume protocol in
[`.claude/commands/resume.md`](.claude/commands/resume.md) verbatim, exactly as if
`/resume` had been invoked. That protocol reads
[`.working/session-handoff.md`](.working/session-handoff.md) for the live per-session
state and the next-actions queue, and its first step points at that handoff's "Known
environment behaviours" section for machine-specific notes (for example a `gh`-CLI PR
mechanism, or a machine that requires a manual commit and push).

Do not copy the protocol or the queue into this file. The single sources of truth are
[`.claude/commands/resume.md`](.claude/commands/resume.md) (the protocol) and
[`.working/session-handoff.md`](.working/session-handoff.md) (the state). Keeping this
file a pointer is what ensures that a resume started here runs the same current protocol
as `/resume`, and reads the same live queue.
