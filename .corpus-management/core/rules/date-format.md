# Date-format metadata

A document's `**Date:**` metadata field is an ISO 8601 `YYYY-MM-DD` date: a
four-digit year within a plausible range, a real calendar date, and exact
two-digit zero padding on the month and day. A `**Date:**` line inside a fenced
code block is documentation of the metadata-block format, not the file's own
metadata, and is not validated (the shared fence-aware scan skips it). Two
literal placeholder values, `YYYY-MM-DD` and `<YYYY-MM-DD>`, are legitimate only
in a template or worklist file (whose own metadata carries fill-in markers by
design), recognized by a filename prefix; the same placeholder value in any
other file is a finding. A non-ISO format, a two-digit year, an impossible
calendar date, missing zero padding, or a year outside the plausible range is
flagged; inline dates in prose are not checked (only the metadata field). The
plausible year range and the template/worklist filename prefixes are the check's
parameters, project configuration and not part of this clause; a file with no
`**Date:**` field contributes no findings.
