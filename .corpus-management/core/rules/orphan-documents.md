# Orphan documents

Every artefact document is reachable from the corpus reference graph: it
carries at least one inbound markdown link from another document. An
orphan artefact, one with zero inbound references, is unreachable and is
flagged, so it is either linked from a relevant register, README, or
related document, or removed if no longer needed. The reverse-reference
graph is built from markdown links outside fenced code blocks (a link
inside a fence is documentation, not a live reference). Entry-point
documents reached by filename convention rather than by inbound link,
and files outside the artefact set, are exempt. The artefact set, the
convention-reached exempt names, and the scan scope are project
configuration and are not part of this clause.
