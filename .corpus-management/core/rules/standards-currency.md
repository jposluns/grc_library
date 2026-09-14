# Standards currency

An external-standard citation names the current version, not a superseded one. The
project's canonical register lists, per standard, the current version and the version
strings that are superseded; a line that cites a standard identifier immediately followed
by one of that standard's superseded versions is flagged. The version may follow the
identifier via a colon, an opening parenthesis, or whitespace, and may carry a ``v``
prefix; a version-continuation guard prevents a match inside a longer version string (so a
superseded ``4.0`` is not matched within a current ``4.0.1``). A citation of a
non-superseded version, and any occurrence inside a fenced code block, are not flagged.
The canonical register, and the repository root it is read from, are project configuration
and are not part of this clause.
