---
corpus-id: cnsprd
origin: pack
family: aiqt
tier: 10
facet: INTEG
secondary: [ACCUR, QUALI]
slug: consumer-follows-its-producer
---

# A consumer follows its producer

A call that consumes another operation's output is issued only after the production it needs, including
asynchronous work needed for that output, is observed complete, within one message and across
messages. Calls issued together have no ordering. A delay or a presence test is not the ordering.
Independent calls stay free to run together.

Where the output has a content digest, the consumer binds to it under
explicit-binding-over-ambient-context, with size only supplementary; an unreadable required input fails
under check-fails-closed-on-unreadable. A per-call hook cannot see sibling calls, so this ordering rests
on the caller.
