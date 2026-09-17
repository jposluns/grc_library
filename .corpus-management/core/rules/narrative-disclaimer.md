# Executive-narrative authority-disclaimer presence

Every executive-narrative page carries the required verbatim authority disclaimer as
the first body content after its metadata block. The check locates the leading
metadata block (the contiguous leading run of metadata-field lines, blank lines within
the run tolerated, optionally preceded by leading blank or #-prefixed lines, ending at
the first following separator) and requires
the first non-blank line after that separator to be the disclaimer text, matched
verbatim at column zero (compared with trailing-whitespace stripped only, so an
indented code block or a rewrapped, mistyped, or altered clause does not satisfy it).
Fences are not skipped, so a fenced example of the disclaimer, or any body content
before it, is a finding; a section heading appearing first, a page whose content is not valid UTF-8, and a
page with no body after the metadata block are each flagged. Body text cannot forge
the metadata-close anchor, because the anchor requires a real leading metadata-field
run. The required disclaimer text, the narrative page scope, and the single
entry-point exemption are supplied by the adopter and are not part of this clause; the
metadata-block location and disclaimer-position logic are fixed by the check. A page whose
content is valid UTF-8 and which carries the verbatim disclaimer in the required
position contributes no findings.
