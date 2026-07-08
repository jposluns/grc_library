# Reference-audit per-document state

Maps each corpus document to the grc_library_ref commit at its last
per-document reference audit (the /reference-audit --docs mode's delta
anchor). Live surface: non-dated, stays in-repo under the current-week
sweep model. Rewritten by tools/audit-reference-breadth.py --update-state;
commit the refresh with the touching PR's QA batch.

| Document | Ref SHA at last audit | Updated (UTC) |
| --- | --- | --- |
