# Directional dependency

A deliverable-corpus document does not link into the project-internal governance
directory. Any link in a deliverable document, whether an inline link (bare,
titled, or angle-bracketed) or a reference-style ``[label]:`` definition, whose
target resolves into the project-governance subtree is flagged, enforcing the one-way
dependency rule that published content must not depend on project-internal governance.
An external target (an ``http:``, ``https:``, ``mailto:``, ``tel:``, ``ftp:``, or pure
``#`` link) is not checked and a fragment is stripped before resolution. A link inside a
fenced code block is counted too (fail closed: no block structure can hide a dependency),
so an example link is written in an inline code span or prose instead. The
project-governance directory name and the deliverable-corpus scan scope are project
configuration and are not part of this clause.
