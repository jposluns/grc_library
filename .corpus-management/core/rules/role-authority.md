# Role authority

A document's Owner and Approving Authority metadata values each resolve to a known
role: a role defined in the project's role-authority register, or an entry on the
project's allow-list of cross-functional bodies, named forums, or external authorities
that are not formal organizational roles. A value matching neither is an undefined-role
finding, since an unresolved Owner or Approving Authority creates governance ambiguity.
An obvious template placeholder is deliberately not flagged: a value containing an angle
bracket, a wholly bracketed value, or a literal ``Role Name`` / ``Role Title``. The
values are read from the metadata lines ``**Owner:**`` and ``**Approving Authority:**``,
and a trailing CommonMark hard-line-break backslash is stripped before the value is
compared. The role-authority register (its path and table format), the allow-list, and
the scan scope are project configuration, not part of this clause; a document with no
Owner or Approving Authority line contributes no findings.
