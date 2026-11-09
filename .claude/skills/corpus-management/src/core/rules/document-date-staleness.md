# Document Date staleness

A document's metadata `Date` field reflects when the document was last updated: it
lags the file's most-recent commit date by no more than a tolerated number of
whole days, and it is not dated after the current date (a "last updated" Date
cannot be in the future). A present-but-malformed `Date` value (not exactly
`YYYY-MM-DD`, optional trailing hard-break backslash) is a finding, never a silent
skip; a file with no `Date` field is legitimately date-free and is skipped. The
future-date comparison is applied to every dated file before the commit-date
lookup, so a future-dated file is flagged even when it has no commit history; the
lag comparison applies only once the commit date is known, and a file whose
most-recent commit predates the audit's baseline date is grandfathered. The
commit-date lookup, the concurrency it runs under, the "today" clock, the scan
scope, the exempt-file set (generated outputs whose Date the generator sets), and
the lag / future / baseline thresholds are project configuration and environment
observation, not part of this clause; the clause is the parse-and-compare check
(is the Date well-formed, how far does it lag the commit date, how far does it
lead today). A well-formed Date within tolerance contributes no finding.
