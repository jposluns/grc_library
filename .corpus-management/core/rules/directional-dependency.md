# Directional dependency

A deliverable-corpus document does not link into the project-internal governance
directory. Any link in a deliverable document, whether an inline link (bare,
titled, or angle-bracketed) or a reference-style ``[label]:`` definition, whose
target resolves into the project-governance subtree is flagged, enforcing the one-way
dependency rule that published content must not depend on project-internal governance.
An external target (an ``http:``, ``https:``, ``mailto:``, ``tel:``, ``ftp:``, or pure
``#`` link) is not checked, a fragment is stripped before resolution, and a link inside a
fenced code block is not counted (a marker-aware fence scan tracks the opening fence's
character and run length, so a ``` inside a ~~~ block is content, not a fence toggle). The
project-governance directory name and the deliverable-corpus scan scope are project
configuration and are not part of this clause.
