# Index-header parity

A corpus's document-index register mirrors, per active document, that document's
own metadata Owner and Review Frequency, which is the go-forward source of truth,
and this check locks that mirror. For every active-index row it resolves the row's
Repository-Path code-span link to the target document, reads that document's
metadata header, and compares two fields, or three when the project enables the
Title comparison. Review Frequency is compared as a BASE
cadence token set: each side is tokenized with a longest-phrase-first, consuming,
word-boundary cadence recognizer, and the base tokens (every recognized cadence
except the event-trigger marker) must be equal, so an added event-trigger clause
("and upon material change") does not by itself create a finding. A per-document
allow-list admits legitimate multi-cadence documents whose index row records a
primary cadence while the header adds another, and each allow-list entry is pinned
to the document path and to the exact expected index and header base sets, so a
later cadence change fails closed rather than inheriting a blanket exemption. A
side with no base cadence at all (purely event-driven) agrees only with another
purely-event-driven side; a base-vs-event-only shape mismatch, and an
unrecognizable cadence on either side, are findings (fail-closed, per the
guard-inputs discipline). Owner is compared by trimming surrounding whitespace and
requiring byte equality (Owner values are canonical titles, so case drift is real
drift); under a strict-owner mode an Owner mismatch is a finding, and otherwise it
is an advisory warning that does not affect the outcome. Title, when enabled, is
compared by trimming surrounding whitespace and requiring byte equality, ratcheted
against a project baseline of known differences, each pinned to the document path
and to the exact index and header titles: an empty title on either side, a
difference with no baseline entry, a pinned difference whose titles changed, and a
baseline entry whose titles now agree are findings, while an unchanged pinned
difference passes and, when its class is a work-list class, is reported as a work
item that does not affect the outcome. With Title enabled, a malformed baseline
entry, a linked header with no title field or with more than one, a baseline entry
that matches no readable row (an advisory warning instead when the project runs on
a partial tree), and a run that compares no title are also findings. Title is not
compared unless the project enables it. A malformed row, a Repository-Path cell
with no parseable code-span link, a link whose display path disagrees with its
target, a linked document that does not exist, cannot be read or is not valid
UTF-8, and a linked header missing the Owner or Review Frequency field are each
findings; a missing or unreadable index register, and an index whose active table
header row is not found, are environmental errors. The index relative path, the
index table's column schema and column indices, the mirrored metadata field names,
the per-document base-cadence allow-list, and the title baseline with its classes
are project configuration and are not part of this clause; the cadence recognizer
vocabulary is a generic default the project may override. A corpus whose index
rows each agree with their linked headers, apart from pinned title differences,
contributes no findings.
