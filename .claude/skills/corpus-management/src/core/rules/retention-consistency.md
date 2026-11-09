# Cross-document retention consistency

A procedure document's evidence-retention period matches the canonical period for
the same category in the central retention-schedule register. Each configured check
names a register row (matched on its first table cell, case-insensitively and exact
after trimming) and the procedure document that must cite the same period. The
register period is the first number-and-unit value in the matched row; the procedure
period is the number-and-unit value stated after a configured anchor phrase, so that
an unrelated period elsewhere in the procedure (a recurrence window, a remediation
target) is not mistaken for the retention figure. Periods are normalized to days for
comparison (years, months, and days). A register row that cannot be found or parsed,
a procedure that cannot be read, a procedure with no anchored retention statement,
and a period that does not match the register are each flagged; a missing register is
a single terminal finding. The register path, the register-category-to-procedure
check list, and the anchor phrase are project configuration and are not part of this
clause; a corpus whose procedures each match their canonical register row contributes
no findings.
