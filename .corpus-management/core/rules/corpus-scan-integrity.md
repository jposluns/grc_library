# Corpus scan integrity

Every fenced code block in a corpus document is balanced, and no file ends
inside an open fence. The shared fence-aware iterator treats each line whose
stripped form opens with three backticks or three tildes as a state toggle, so
an unbalanced (odd) fence count leaves the iterator inside a code block for the
rest of the file, silently suppressing every fence-aware check's scan of the
remainder. A balanced fence count is therefore the precondition for any
fence-aware gate's result to mean what it says: the integrity guard runs before
the checks whose soundness depends on it.
