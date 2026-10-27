#!/usr/bin/env python3
"""Tooling backlog-reference audit (grc gate 107): the provenance-sweep recurrence backstop.

WHAT IT CATCHES. The 2026-08 provenance sweep (PRs #1764, #1767, #1768, #1770,
#1786, #1788, #1789; the item-15 / P-1.51 lane) re-pointed retired positional
backlog pointers in tool and hook provenance prose (``TODO N.M``,
``TODO section N.M``, ``section N.M``, ``section-N.M``) to the durable
``N.M (closing PR #X)`` form. Nothing mechanical stopped the class from
recurring: gate 69 (lint-positional-backlog-tokens) scans corpus MARKDOWN only,
and ``tools/`` / ``.claude/hooks/`` are outside its scope. This gate is the
backstop (backlog item 3b151): it scans ``.py``, ``.sh``, ``.md``, ``.json``,
``.yml`` and ``.yaml`` files, plus suffix-less scripts whose shebang names a
Python or Bourne-family shell interpreter (note 10; the ``tools/git-hooks/``
trio, the nmw-actionable hook) and the registered rule-overlay
``PROVENANCE.txt`` records, under ``tools/``, ``.claude/`` and
``.github/`` (note 11; backlog item 3b636 widened the roots from
``.claude/hooks/`` after a live pointer survived in a playbook), for a
qualified positional backlog pointer and fails when the pointer names an item
that is no longer live, because a positional number is only a sound citation
while its item is open; a closed item's number must be anchored to its
closing PR.

DETECTION, stated because each choice has a false-positive or false-negative
cost (all measured against the repo at adoption; the raw census had ~95 hits
and three survivors: two enumerated in ``EXEMPT``, the third reworded at
source):

  1. LINE-WRAP TOLERANCE. Each file is read as ONE wrap-joined text: comment
     leaders (leading ``#`` runs) are blanked length-preservingly and newlines
     are read as spaces, so a pointer split across comment lines is still one
     token. Findings are reported at the physical line where the pointer
     starts, and the inline marker (rule 6) binds to that line or the line
     above it.

  2. ILLUSTRATIVE LITERALS DO NOT REGISTER. Backtick code spans and, in
     ``.py`` / ``.sh`` files and the suffix-less scripts, SAME-LINE
     double-quoted spans are blanked (length-preservingly) BEFORE matching,
     in ONE pass, so every boundary guard below reads the ORIGINAL source
     context and a span blanked earlier can never manufacture an opener or
     closer for a later one (3b151 QA r3: the previous second pass did
     exactly that). A backtick span pairs sequentially across line wraps
     (300-character cap) but NEVER across a blank line (3b151 QA r2:
     unbounded pairing let one stray backtick blank prose paragraphs away),
     so a stray unpaired backtick can blank at most the rest of its own
     paragraph. A double-quoted span is blanked when it opens and closes on
     one physical line, its opening quote carries at most two attached
     string-prefix letters (``r``, ``b``, ``u``, ``f`` in either case, so a
     prefixed ``r``- or ``f``-string literal still blanks), and no word
     character, apostrophe or double quote abuts the OUTSIDE of either end,
     so a digit-adjacent inch mark cannot OPEN a span, but it can close a
     stray earlier opener; a quote hugging another quote cannot pair. A
     SINGLE quote is interpreted NOWHERE: apostrophes are prose
     characters (3b151 QA r3: two rounds of single-quote span heuristics
     each left a shape in which an apostrophe hid a genuine pointer; the
     claim is now exact by construction), so a single-quoted example is
     simply flagged and is cleared with backticks or the rule-6 marker. A
     double-quote triple delimiter (a run of three double quotes, with an
     optional string prefix so a raw docstring cannot mispair) is consumed
     as a bare token, so a docstring's PROSE IS SCANNED like comment prose
     (3b151 QA r1: the previous cross-line double-quote pairing read a
     docstring's first two quotes as an empty span and blanked most
     docstrings whole) and the delimiter can never mispair with a later
     double quote. The raw census is dominated by self-test probes and
     docstring examples (the rotation-gate form examples, the hook
     disposition-grammar probes), and every one of them is double-quoted or
     backticked. In ``.md`` files and the registered ``PROVENANCE.txt``
     records (Markdown content, note 11), fence state is computed FIRST on RAW
     lines through the shared ``aiqt_corpus.is_fence_line`` predicate, then
     fenced lines are blanked. This is the same toggle model corpus gates
     use (a toggle is a toggle: fences
     are paired by neither delimiter character nor width), so a fence
     delimiter's backtick run can never pair into the prose around the
     block (3b151 QA r2); a file whose fence-shaped lines toggle an ODD
     number of times leaves the model inside a fence at end of file, where
     an unterminated fence and a miscounted fence-shaped prose line are
     indistinguishable, so the file is REFUSED (note 9, exit 2), never
     silently blanked to its end (3b151 QA r3: a line-leading inline
     triple-backtick span, and a three-backtick line inside a four-backtick
     fence, both miscounted the toggle and hid following prose); then ONLY
     the inline backtick spans are blanked: a double-quoted span in
     Markdown prose is quotation, not an illustrative literal, so a pointer
     inside it is still checked. ``.json`` files are read raw, because
     their content is entirely quoted (the publication-manifest rationale
     strings are genuine prose); JSON escapes are not decoded, so an
     escaped pointer can evade detection. ``.yml`` / ``.yaml`` files (the
     workflows, the playbook manifest) are read raw the same way, only their
     leading ``#`` comment leaders blanked: a quoted YAML scalar is prose
     (a step name, a description), not an illustrative literal. RESIDUE: a genuine pointer inside a
     SAME-LINE double-quoted provenance string is stripped (a quoted
     pointer is read as a mention; silently missed); a pair of stray double
     quotes on one physical line, each end clear of word characters,
     apostrophes and double quotes on the outside, is read as a literal and
     hides what sits between them (including an inch-mark closer); a stray
     backtick, including one in a single-quoted literal, can blank
     prose up to the end of its own paragraph; and in ``.md`` files and the
     registered ``PROVENANCE.txt`` records an EVEN number of miscounted
     fence-shaped prose lines hides the prose between them, while an odd
     number is refused loudly. All remain accepted
     FN-safety costs, each bounded as stated. On the false-positive side, a
     quoted example that wraps across lines, ANY single-quoted example, a
     double-quoted example abutting a word character or another quote, and
     prose inside a triple-quoted string are all still checked and so can
     be flagged: ambiguity keeps real pointers flagged, and such an example
     is cleared with backticks or the rule-6 marker.

  3. QUALIFIED FORMS ONLY. A match requires the ``TODO`` qualifier (optionally
     carrying the private list's ``P-`` prefix, and optionally followed by
     ``section`` / ``Section``) or the lowercase ``section`` / ``section-``
     qualifier, followed by a dotted number whose FIRST component is a single
     digit (the live backlog series) and whose tail may carry the child-item
     letter of the shared id grammar (``3.92a`` / ``3.92.a``, matching
     ``lint_common.TODO_ID_RE``), so a statute token never matches and a
     child-item pointer is checked against its own id rather than its
     parent's. A bare unqualified dotted number, a capitalized ``Section N.M``
     without the qualifier (measured: always a document section here), a
     lowercase or mixed-case spelling of the qualifier, a hyphenated
     qualifier-to-number join, an intervening word between the qualifier and
     the number (``item``), and the ``§``- or ``P-``-prefixed id
     shapes are OUT of scope (gate 69's class in markdown; stated residue
     here).

  4. PR-ANCHORED POINTERS PASS. A pointer immediately followed by
     ``(closing PR #X)`` or ``(introducing PR #X)`` is the durable re-pointed
     form and passes without a liveness check. The complete anchor is
     required: X is ASCII digits, with optional whitespace before the
     closing parenthesis; matching uses text before literal blanking.

  5. DOCUMENT-SECTION AND EXTERNAL-STANDARD EXCLUSION. A ``section``-form
     match (not ``TODO``-qualified) is excluded when a census-derived cue
     (for example a ``.md`` filename, ``spec``, ``specification``, ``heading``,
     ``table``, ``row``, ``block``, ``publisher``, ``ISO``, ``NIST``,
     ``Article``, ``RFC``) appears within a short window around the match. The
     cue scan runs on the UNSTRIPPED reading (same coordinates: the blanking
     is length-preserving), so a cue inside backticks still counts. This keeps
     the frequent spec-section citations out of the net. RESIDUE: a genuine
     backlog ``section``-form pointer next to a cue word is suppressed; the
     ``TODO``-qualified form is never cue-suppressed.

  6. MARKER. ``todo-ref-ok: <reason>`` on the pointer's first line or the line
     above clears a deliberate mention. A marker with an EMPTY reason clears
     nothing (fail closed) and the finding says so. Complete HTML comments
     bound their own reasons: closing delimiters and outside text never
     contribute. Bodies containing a double hyphen, starting with > or ->,
     or ending with a hyphen are malformed. Segments with incomplete or
     malformed comment delimiters grant no clearance. Each reason ends at
     its physical newline or comment terminator. Comments are never removed
     from pointer detection.

  7. EXEMPT. A small dict keyed by (repo-relative file, id, distinctive
     substring of the pointer's source line), gate-78 style, so an exemption
     cannot silently widen to a different line. Seeded with the two exempted
     census survivors (the third was reworded at source); both exempted ids
     also collide with a backlog number live at adoption (one private, one
     public), so the rows keep those document references green after the
     unrelated backlog items close; see the rationales on the rows.

  8. OPEN-VERSUS-DELETED, WITH GATE-78 GRACEFUL DEGRADATION. The live set is
     read from ``TODO.md`` plus, when the private sibling is reachable,
     ``TODO-REFERENCE.md``, ``P-TODO.md`` and ``P-TODO-REFERENCE.md``, all
     through the shared ``tools/todo_index_rows.py`` grammar (index rows and
     item headings), the same reader gates 78 and 90 use, so redirect stubs
     held as headings in the reference file stay live. A pointer at a live
     item passes (the sweep deliberately left then-live refs in place). When
     the private sibling is unreachable (public CI, adopter clones), an id
     absent from ``TODO.md`` cannot be proven deleted, so the pointer is
     reported as a SKIPPED unresolved reference and the gate exits 0 for that
     class, exactly as gate 78 downgrades its recycled-number check when the
     DONE ledger is absent.

  9. FAIL-CLOSED INPUTS. Errors name the path and exit 2, even under
     --report. Every enumerated entry is classified with os.lstat and, for
     symlinks, os.stat before suffix or fixture-name filtering. Any failure,
     including disappearance after enumeration, is refused on every Python
     version. Confirmed directories named tests, fixtures or __pycache__ are
     pruned, including accessible directory symlinks; unclassifiable entries
     with those names are refused. Other directory symlinks, special entries,
     unreadable directories or regular files, undecodable selected files or
     backlogs, odd Markdown fence counts, an unusable present private sibling
     and an empty selection are refused. Every regular file is read in binary
     before selection, regardless of suffix; selected files must also decode
     as UTF-8. An absent scan root is allowed if another supplies a selected
     file. Only an absent private sibling selects note 8's degraded path;
     an absent backlog list inside a present sibling contributes no ids.

  10. INTERPRETER SELECTION. Every regular file is probed regardless of
      suffix. An executable mode bit or a shebang requires a resolvable
      interpreter. INTERPRETER_EXEMPT may explicitly waive resolution for a
      repo-relative file with a reviewed nonempty rationale; it is empty at
      adoption. Exempt files still undergo classification/read checks and
      suffix-based scanning. Missing, invalid UTF-8, NUL-containing,
      over-256-byte or unresolved shebangs are refused with the diagnostic
      "cannot determine interpreter; add a supported shebang or exempt it
      explicitly". Direct interpreters resolve by basename. For env, the
      whitespace-word grammar supports -S, attached -S and --split-string=
      payloads; -u/--unset, -C/--chdir and -a/--argv0 consume one operand;
      -i, --ignore-environment, -v and --debug are flags; -- ends options;
      NAME=value assignments precede the command; NAME uses ASCII letters,
      digits and underscores and cannot start with a digit. Quotes, dollar
      signs, backslashes, unknown options/bundles/abbreviations, comment
      words and missing operands/commands refuse resolution. Quoting/escaping is checked through the command
      word, not its arguments. Known whitespace-word forms are conservatively
      read even without -S, ignoring kernel tail packing; this can over-select
      a non-executing form, never silently omit one. A resolved basename
      matching python with a word-character/dot suffix, or sh/ash/dash/bash/
      ksh/mksh/zsh, selects a suffix-less script. The .py/.sh/.md/.json/.yml/
      .yaml suffixes are always selected. Other resolved interpreters and
      other suffixes remain outside prose scope. At adoption the suffix-less
      selection is the tools/git-hooks trio and .claude/hooks/nmw-actionable.

  11. ROOTS AND WHAT THEY LEAVE OUT (3b636). The roots are ``tools/``, the
      whole of ``.claude/`` (hooks, playbooks, commands, references, rules,
      skills, ``CLAUDE.md``, ``settings.json``) and ``.github/``. Two
      ``.gitignore``-listed, machine-local paths are pruned after
      classification, because they are runtime state, not reviewed prose:
      ``.claude/hooks/.state/`` (self-guard block history) and
      ``.claude/settings.local.json``. Third-party content refreshed from
      upstream and never hand-edited is not selected: ``.claude/rules/
      external/``, the five registered addyosmani skill directories
      (``external_overlay.ADDYOSMANI_SKILLS``) and the vendored
      ``.claude/skills/clean-language/``, whose ``FILES`` are pinned
      byte-identical to upstream by its drift check. A dotted number there is
      upstream's, and rewriting it would defeat the drift check. Files
      there are still classified and read (note 9); only each directory's
      own first-party ``PROVENANCE.md`` record, at the directory's root, is
      selected (a nested file sharing that basename is vendored content and
      is not), plus the rule
      overlays' first-party records registered in
      ``external_overlay.RULE_PROVENANCE_PATHS``: those keep a ``.txt``
      suffix to leave Claude rule discovery but hold project-authored
      Markdown, so exactly those paths are selected and read as Markdown;
      no other ``.txt`` file is. RESIDUE: a backlog pointer pasted into
      vendored content is not seen.

Usage:
    python3 tools/lint-tooling-backlog-refs.py
    python3 tools/lint-tooling-backlog-refs.py --report
    python3 tools/lint-tooling-backlog-refs.py --root <dir>

``--report`` prints findings but always exits 0 (the plan's report-first mode;
the wired surfaces run the gate enforcing); a note-9 input error still exits 2.
``--root`` rebases the scan for the regression fixtures; under it the private
sibling is resolved as the given root's ``../grc_library_private``, mirroring
``lint_common.resolve_sibling``.

Exit codes:
    0   no findings (including degraded-skip runs and --report runs).
    1   one or more findings.
    2   TODO.md is missing, an explicit --root is refused, or a note-9
        fail-closed input error (an unreadable or undecodable file, an
        inaccessible subtree, symlink or sibling, an odd fence-toggle count
        in a scanned Markdown file, an empty scan set).

Stdlib-only Python 3.11+ (local helpers and the vendored AIQT core).
"""

from __future__ import annotations

import argparse
import bisect
import os
import re
import stat
import sys
from pathlib import Path
from typing import NamedTuple

from lint_common import (
    REPO_ROOT,
    InaccessiblePath,
    print_degraded,
    require_dir,
    resolve_sibling,
    strict_kind,
)
import aiqt_bootstrap  # noqa: F401  # shared vendored core on sys.path
from aiqt_corpus import is_fence_line
# The registered third-party skill directories (the lint-ungated-dashes registry).
from external_overlay import ADDYOSMANI_SKILLS
# The registered rule-overlay records: Markdown under a .txt suffix (note 11).
from external_overlay import RULE_PROVENANCE_PATHS

# The one index-row and item-heading grammar the backlog readers share (P-TODO 3b121).
from todo_index_rows import index_rows, item_headings

TODO_REL = "TODO.md"
PRIVATE_SIBLING_DIR = "grc_library_private"
# Backlog files held only by the private sibling; absent for public CI / adopter clones.
PRIVATE_BACKLOG_FILES = ("TODO-REFERENCE.md", "P-TODO.md", "P-TODO-REFERENCE.md")

SCAN_ROOTS = ("tools", ".claude", ".github")
SCAN_SUFFIXES = frozenset({".py", ".sh", ".md", ".json", ".yml", ".yaml"})
# Machine-local, never-committed paths (.gitignore) pruned after classification
# (design note 11): they are runtime state, not reviewed provenance prose.
SKIP_REL_PATHS = frozenset({".claude/hooks/.state", ".claude/settings.local.json"})
# Third-party content refreshed FROM UPSTREAM, never hand-edited (design note
# 11; the lint-ungated-dashes exemption plus the vendored clean-language
# skill): its numbering is upstream's, not this backlog's, and a rewrite
# would break the upstream drift checks. Files under these directories are
# still classified and read, but only each directory's OWN first-party record
# (THIRD_PARTY_RECORD_PATHS, at the directory's root) is selected: a nested
# file that merely shares the basename is vendored content (3b636 r3).
THIRD_PARTY_DIRS = (
    (".claude/rules/external",)
    + tuple(f".claude/skills/{name}" for name in ADDYOSMANI_SKILLS)
    + (".claude/skills/clean-language",)
)
THIRD_PARTY_RECORD_PATHS = frozenset(f"{d}/PROVENANCE.md" for d in THIRD_PARTY_DIRS)
# Exactly the registered rule-overlay PROVENANCE.txt records are selected and
# read as Markdown, whatever their suffix (note 11); no other .txt file is.
MARKDOWN_RECORD_PATHS = frozenset(RULE_PROVENANCE_PATHS)
# A suffix-less file is scanned too when its shebang names an interpreter whose
# comment and quote shapes the literal strip already handles (the git hooks and
# nmw-actionable carried provenance prose no suffix rule reached, 3b151 QA r1).
# The probe matches the interpreter's BASENAME, resolved through the exact
# ``env`` grammar of design note 10 (3b151 QA r3): python under any version
# suffix, and the Bourne-family shells (3b151 QA r2: the old pattern missed
# ``ash`` and read only 120 bytes).
SHEBANG_PY_NAME = re.compile(r"python[\w.]*")
SHEBANG_SH_NAME = re.compile(r"sh|ash|dash|bash|ksh|mksh|zsh")
# Bound supported shebangs explicitly; an incomplete probe is never a verdict.
SHEBANG_READ_BYTES = 256
ENV_OPERAND_FLAGS = frozenset({"-u", "--unset", "-C", "--chdir", "-a", "--argv0"})
ENV_FLAGS = frozenset({"-i", "--ignore-environment", "-v", "--debug"})
ENV_SPLIT_LONG = "--split-string="
ENV_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z_0-9]*=.*", re.ASCII)
INTERPRETER_ERROR = (
    "cannot determine interpreter; add a supported shebang or exempt it explicitly"
)
# Repo-relative file -> reviewed nonempty rationale; resolution only (note 10).
INTERPRETER_EXEMPT: dict[str, str] = {}
# Suffixes whose double-quoted spans are illustrative literals (design note
# 2); a suffix-less shebang script is stripped the same way (Python and shell
# share the comment and double-quote shapes at the fidelity this strip needs).
LITERAL_STRIP_SUFFIXES = frozenset({".py", ".sh"})
# Suffixes whose backtick code spans are blanked but whose double-quoted spans
# are Markdown prose quotation and stay checked (design note 2).
BACKTICK_ONLY_SUFFIXES = frozenset({".md"})
# Directory components excluded from the scan (test fixtures embed deliberate tokens).
SKIP_DIR_PARTS = frozenset({"__pycache__", "tests", "fixtures"})

# A qualified positional backlog pointer (design note 3). Case-sensitive
# qualifier (optionally P- prefixed, the private list's stem) and lowercase
# bare section; Section is accepted only after the qualifier, where no
# document-section ambiguity exists. The id's first component is a single
# digit, its tail may carry the TODO_ID_RE child-item letter, and the token
# ends cleanly (a trailing sentence period still matches, a longer dotted tail
# or a word character does not).
BACKLOG_REF = re.compile(
    r"(?<![\w-])(?:(?:P-)?TODO\s+(?:[Ss]ection[-\s]+)?|section[-\s]+)"
    r"(?P<id>[1-9]\.\d+(?:\.\d+)*(?:\.?[a-z])?)(?!\w)(?!\.\d)"
)
TODO_QUALIFIED = re.compile(r"^(?:P-)?TODO\b")
# The durable re-pointed form, immediately after the id (design note 4).
PR_ANCHOR_AFTER = re.compile(r"^\s*\((?:closing|introducing)\s+PR\s+#[0-9]+\s*\)")
# Census-derived document-section / external-standard cues (design note 5).
# RFC through SOC were added post-census (3b151 QA r1: external standards the
# census never saw still cite sections and clauses).
DOC_SECTION_CUE = re.compile(
    r"(?i)\.md\b|\bspecs?\b|\bspecification|§|\bheading|\btable\b|\brows?\b"
    r"|\binventory\b|\bclause|\bchapter|\bblock\b|\bpublisher|\bsource of record\b"
    r"|\bannex\b|\bdelta|\bverification\b|\bISO\b|\bIEC\b|\bNIST\b|\bSP ?800"
    r"|\bCOBIT\b|\bCWE\b|\bASVS\b|\bCSF\b|\bSSDF\b|\bMiCA\b|\bArticle\b|\bTSC\b"
    r"|\bCCM\b|\bAICM\b|\bGDPR\b|\bCPPA\b"
    r"|\bRFC\b|\bPCI\b|\bDSS\b|\bFIPS\b|\bOWASP\b|\bHIPAA\b|\bSOC\b"
)
CUE_WINDOW_BEFORE = 110
CUE_WINDOW_AFTER = 80

# The inline clearing marker (design note 6). The reason must be non-empty.
MARKER_RE = re.compile(r"todo-ref-ok:(?P<reason>[^\n]*)")

# Comment leaders, blanked length-preservingly so wrapped comments join (note 1).
COMMENT_LEAD = re.compile(r"(?m)^[ \t]*#+ ?")

# Backtick code spans and double-quoted literal spans (design note 2). The
# quote characters are assembled via chr() so this pattern's own source line
# stays quote-balanced under the gate's self-scan (the gate-103 precedent:
# identifiers are assembled so a tool cannot leak, or here mispair, on
# itself). Alternatives bind in order: backtick spans (these may wrap lines
# under the 300-character cap but never cross a BLANK line, so a stray
# backtick blanks at most the rest of its own paragraph, 3b151 QA r2); a
# double-quote triple delimiter with an optional string prefix, consumed as a
# bare token, so a docstring's prose stays scanned and a raw docstring's
# prefix cannot peel an empty span off the delimiter; and a SAME-LINE
# double-quoted span, its opening quote carrying at most two attached
# string-prefix letters and NEITHER end abutting a word character, apostrophe
# or double quote on the outside. A digit-adjacent inch mark cannot open a
# span, but can close a stray opener (design note 2). Single quotes appear
# only inside the outside-abutment guards: the pattern never pairs them, so
# no apostrophe shape can open or close a span. Applied in ONE pass, so every
# guard reads the original source context (3b151 QA r3).
_DQ = chr(34)
_SQ = chr(39)
# A backtick span's interior: anything but a backtick, with a newline allowed
# only when the next line is non-blank (a blank line is a paragraph break; a
# CommonMark code span cannot cross one either).
_BT_BODY = "(?:[^`\\n]|\\n(?![ \\t]*\\n))"
# Up to two attached Python string-prefix letters before a double quote
# (r/b/u/f, either case; an over-wide pair like ``bu`` only widens blanking
# by two characters on a shape Python would reject anyway).
_STR_PREFIX = "[rbufRBUF]{0,2}"
CODE_OR_STRING_SPAN = re.compile(
    "(`+)" + _BT_BODY + "{0,300}?\\1"
    + "|" + _STR_PREFIX + _DQ * 3
    + "|(?<![\\w" + _SQ + _DQ + "])" + _STR_PREFIX + _DQ
    + "[^" + _DQ + "\\n]{0,300}?" + _DQ
    + "(?![\\w" + _SQ + _DQ + "])"
)
BACKTICK_SPAN = re.compile("(`+)" + _BT_BODY + "{0,300}?\\1")

# (repo-relative file, id, distinctive substring of the pointer's source line)
# -> rationale. Substring-keyed, not line-keyed, for the gate-78 reason: a line
# key lapses on any unrelated edit that shifts the file. The two rows are the
# legitimate survivors of the census at adoption (grc_library bd04eaf3); the third
# survivor, a stale `formerly TODO 3.148` pointer in lint-paired-skill-step-parity.py,
# was reworded at source instead of exempted.
EXEMPT: dict[tuple[str, str, str], str] = {
    ("tools/lint-allowlist-spec-parity.py", "7.1",
     "section 7.1 domain is admitted"): (
        "Document-section reference (citation-verification specification section "
        "7.1) whose sentence carries none of the census cue words; not a backlog "
        "pointer. The number also collides with a backlog id live in the private "
        "lists at adoption, so this row keeps the doc ref green after that "
        "unrelated item closes."
    ),
    ("tools/lint-scan-scope-parity.py", "6.3",
     "section-6.3 / full-corpus-audit-sweep"): (
        "Document-section reference (the project-governance separation "
        "specification's 'Audited, not exempt' section) with no cue word in "
        "window; it also collides with a live backlog number at adoption, so this "
        "row keeps the doc ref green after that unrelated item closes."
    ),
}


class GateInputError(Exception):
    """A note-9 fail-closed input problem; ``main`` prints it and exits 2."""


class Candidate(NamedTuple):
    """One surviving pointer. ``line`` is 1-based over newline-split lines;
    ``token`` is whitespace-normalized; ``source_line`` is the original line the
    pointer starts on (the EXEMPT binding surface); ``reasonless_marker`` records
    a marker that was present but empty, for the fail-closed finding text."""

    line: int
    token: str
    item_id: str
    source_line: str
    reasonless_marker: bool


def _blank(m: re.Match) -> str:
    """Length-preserving replacement: spaces, with newlines kept in place."""
    return "".join(ch if ch == "\n" else " " for ch in m.group(0))


def _blank_md_fences(text: str) -> tuple[str, bool]:
    """Markdown fenced code blocks blanked length-preservingly, fence lines
    included, on RAW lines through ``aiqt_corpus.is_fence_line``: the same
    toggle model every corpus gate uses, pairing fences by neither delimiter
    character nor width. Runs BEFORE the inline backtick pass, so a fence
    delimiter's backtick run can never pair into the prose around the block
    (design note 2; 3b151 QA r2). Returns the blanked text and whether the
    toggling is BALANCED; an unbalanced file is undecidable under the toggle
    model and must be refused by the caller (note 9; 3b151 QA r3), never
    silently blanked to its end."""
    out: list[str] = []
    in_code = False
    for line in text.split("\n"):
        if is_fence_line(line):
            in_code = not in_code
            out.append(" " * len(line))
        else:
            out.append(" " * len(line) if in_code else line)
    return "\n".join(out), not in_code


def _marker_reasons(text: str) -> dict[int, list[str]]:
    """Read reasons in complete comments or delimiter-free text, by line.

    This partitions only the marker reading. Pointer text is never removed.
    Malformed or incomplete segments grant no clearance.
    """
    reasons: dict[int, list[str]] = {}
    lineno = 1
    for segment in re.split(r"(<!--[\s\S]*?-->)", text):
        body = segment
        valid = True
        if segment.startswith("<!--") and segment.endswith("-->"):
            body = segment[4:-3]
            valid = not ("--" in body or body.startswith((">", "->"))
                         or body.endswith("-"))
        elif "<!--" in segment or "-->" in segment:
            valid = False
        if valid:
            for offset, line in enumerate(body.split("\n")):
                match = MARKER_RE.search(line)
                if match is not None:
                    reasons.setdefault(lineno + offset, []).append(match.group("reason"))
        lineno += segment.count("\n")
    return reasons


def candidate_refs(path: Path, text: str, markdown: bool = False) -> list[Candidate]:
    """All positional backlog pointers in one file, after the literal strip, the
    PR-anchor pass, the cue pass and the marker pass. PURE detection over one
    file's text (the EXEMPT rows and the open-versus-deleted check are
    ``run_scan``'s concern); raises :class:`GateInputError` for a Markdown
    file whose fence toggling is unbalanced (note 9). ``markdown`` reads a
    registered non-``.md`` record as Markdown (note 11)."""
    lines = text.split("\n")
    markers = _marker_reasons(text)
    markdown = markdown or path.suffix in BACKTICK_ONLY_SUFFIXES
    if markdown:
        fenceless, balanced = _blank_md_fences(text)
        if not balanced:
            raise GateInputError(
                "fence-shaped lines toggle an odd number of times, leaving "
                "the shared fence model inside a fence at end of file; an "
                "unterminated fence and a miscounted fence-shaped prose line "
                "are indistinguishable there, so the file is refused rather "
                "than silently blanked to its end (close the fence, or "
                "reword the fence-shaped line)")
    cueview = COMMENT_LEAD.sub(_blank, text)
    # A suffix-less path reaches this gate only through the shebang probe, so
    # it takes the .py/.sh literal strip.
    if path.suffix in LITERAL_STRIP_SUFFIXES or not path.suffix:
        # ONE pass (3b151 QA r3): every boundary guard reads the original
        # source context, so a span blanked earlier can never manufacture an
        # opener or closer for a later one.
        stripped = CODE_OR_STRING_SPAN.sub(_blank, cueview)
    elif markdown:
        stripped = BACKTICK_SPAN.sub(_blank, COMMENT_LEAD.sub(_blank, fenceless))
    else:
        stripped = cueview
    joined = stripped.replace("\n", " ")
    cue_joined = cueview.replace("\n", " ")
    offsets = [0]
    for ln in lines:
        offsets.append(offsets[-1] + len(ln) + 1)

    out: list[Candidate] = []
    for m in BACKLOG_REF.finditer(joined):
        lineno = bisect.bisect_right(offsets, m.start())
        if PR_ANCHOR_AFTER.match(cue_joined[m.end():]):
            continue
        if not TODO_QUALIFIED.match(m.group(0)):
            lo = max(0, m.start() - CUE_WINDOW_BEFORE)
            if DOC_SECTION_CUE.search(cue_joined[lo:m.end() + CUE_WINDOW_AFTER]):
                continue
        cleared = reasonless = False
        for marker_line in (lineno, lineno - 1):
            if 1 <= marker_line <= len(lines):
                for reason in markers.get(marker_line, ()):
                    if reason.strip():
                        cleared = True
                    else:
                        reasonless = True
        if cleared:
            continue
        out.append(Candidate(
            line=lineno,
            token=" ".join(m.group(0).split()),
            item_id=m.group("id"),
            source_line=lines[lineno - 1] if lineno <= len(lines) else "",
            reasonless_marker=reasonless,
        ))
    return out


def load_live_ids(todo_path: Path, private_dir: Path | None) -> set[str]:
    """The live backlog ids (design note 8): index rows and item headings of
    TODO.md plus every reachable private backlog file, through the shared
    todo_index_rows grammar. An ABSENT list contributes no ids: only an
    absent SIBLING selects the note-8 degraded path (``main``'s concern), so
    a list missing inside a present sibling keeps the run enforcing, the safe
    direction; a backlog list that is PRESENT but cannot be examined, read or
    decoded raises GateInputError (note 9), because every id it might hold
    would otherwise silently read as deleted."""
    sources = [todo_path]
    if private_dir is not None:
        sources.extend(private_dir / name for name in PRIVATE_BACKLOG_FILES)
    ids: set[str] = set()
    for p in sources:
        try:
            kind = strict_kind(p)
        except InaccessiblePath as exc:
            raise GateInputError(f"backlog list {p}: inaccessible ({exc})") from exc
        if kind is None:
            continue
        if kind != "file":
            raise GateInputError(f"backlog list {p}: present but not a regular file")
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise GateInputError(
                f"backlog list {p}: not valid UTF-8 ({exc}); the live-id set "
                f"cannot be proven complete over an undecodable list") from exc
        except OSError as exc:
            raise GateInputError(f"backlog list {p}: unreadable ({exc})") from exc
        ids.update(row.item_id for row in index_rows(text))
        ids.update(heading.item_id for heading in item_headings(text))
    return ids


def _env_interpreter(words: list[str]) -> str | None:
    """Resolve only note 10's explicit word grammar; ambiguity returns None."""
    pending = list(words)
    options = True
    while pending:
        word = pending.pop(0)
        if any(ch in word for ch in (chr(34), chr(39), "\\", "$")):
            return None
        if options and word == "--":
            options = False
        elif options and word == "-S":
            continue
        elif options and word.startswith("-S") and len(word) > 2:
            pending.insert(0, word[2:])
        elif options and word.startswith(ENV_SPLIT_LONG):
            payload = word[len(ENV_SPLIT_LONG):]
            if not payload:
                return None
            pending.insert(0, payload)
        elif options and word in ENV_OPERAND_FLAGS:
            if not pending:
                return None
            operand = pending.pop(0)
            if any(ch in operand for ch in (chr(34), chr(39), "\\", "$")):
                return None
        elif options and word in ENV_FLAGS:
            continue
        elif options and word.startswith("-"):
            return None
        elif ENV_ASSIGNMENT.fullmatch(word):
            options = False
        elif "=" in word or word.startswith("#"):
            return None
        else:
            return word if word and not word.startswith("-") else None
    return None


def _shebang_scan_ok(path: Path, executable: bool = False,
                     exempt: bool = False) -> bool:
    """Read every regular file; resolve executable inputs before selection."""
    with path.open("rb") as fh:
        first = fh.readline(SHEBANG_READ_BYTES + 1)
        while fh.read(65536):
            pass
    has_shebang = first.startswith(b"#!")
    if exempt:
        return False
    if not has_shebang:
        if executable:
            raise GateInputError(INTERPRETER_ERROR)
        return False
    if len(first) > SHEBANG_READ_BYTES or b"\x00" in first:
        raise GateInputError(INTERPRETER_ERROR)
    try:
        words = first[2:].decode("utf-8").split()
    except UnicodeDecodeError as exc:
        raise GateInputError(INTERPRETER_ERROR) from exc
    if not words:
        raise GateInputError(INTERPRETER_ERROR)
    interpreter = words.pop(0)
    if any(ch in interpreter for ch in (chr(34), chr(39), "\\", "$")):
        raise GateInputError(INTERPRETER_ERROR)
    name = interpreter.rsplit("/", 1)[-1]
    if name == "env":
        interpreter = _env_interpreter(words)
        if interpreter is None:
            raise GateInputError(INTERPRETER_ERROR)
        name = interpreter.rsplit("/", 1)[-1]
    if not name:
        raise GateInputError(INTERPRETER_ERROR)
    return bool(SHEBANG_PY_NAME.fullmatch(name) or SHEBANG_SH_NAME.fullmatch(name))


def iter_scan_files(root: Path) -> tuple[list[Path], list[str]]:
    """Strictly classify every entry and read every regular file (notes 9/10).

    Explicit scandir traversal avoids version-dependent pathlib predicates
    and os.walk classification. Only confirmed fixture directories are
    pruned; symlink targets must first be examinable. Other directory
    symlinks and special entries refuse.
    """
    files: list[Path] = []
    errors: list[str] = []
    pending: list[Path] = []
    for sub in SCAN_ROOTS:
        base = root / sub
        try:
            kind = strict_kind(base)
        except InaccessiblePath as exc:
            errors.append(f"{base}: scan root inaccessible ({exc})")
            continue
        if kind is None:
            continue
        if kind != "dir":
            errors.append(f"{base}: scan root is present but not a directory")
            continue
        pending.append(base)
    while pending:
        directory = pending.pop()
        try:
            with os.scandir(directory) as entries:
                names = sorted(entry.name for entry in entries)
        except OSError as exc:
            errors.append(f"{directory}: scan subtree unreadable ({exc})")
            continue
        for name in names:
            path = directory / name
            try:
                entry_stat = os.lstat(path)
                is_link = stat.S_ISLNK(entry_stat.st_mode)
                mode = os.stat(path).st_mode if is_link else entry_stat.st_mode
                rel = path.relative_to(root).as_posix()
                if rel in SKIP_REL_PATHS:
                    continue
                if stat.S_ISDIR(mode):
                    if name in SKIP_DIR_PARTS:
                        continue
                    if is_link:
                        raise GateInputError("directory symlink inside a scan root")
                    pending.append(path)
                    continue
                if not stat.S_ISREG(mode):
                    raise GateInputError("entry is not a regular file or directory")
                script = _shebang_scan_ok(
                    path, bool(mode & 0o111),
                    bool(INTERPRETER_EXEMPT.get(rel, "").strip()))
                if rel in MARKDOWN_RECORD_PATHS or rel in THIRD_PARTY_RECORD_PATHS:
                    files.append(path)
                    continue
                if any(rel.startswith(d + "/") for d in THIRD_PARTY_DIRS):
                    continue
                if path.suffix in SCAN_SUFFIXES or (not path.suffix and script):
                    files.append(path)
            except (OSError, GateInputError) as exc:
                errors.append(f"{path}: cannot classify or read scan entry ({exc})")
    return sorted(files), errors


def _is_exempt(rel: str, cand: Candidate) -> bool:
    return any(
        path == rel and item_id == cand.item_id and substring in cand.source_line
        for (path, item_id, substring) in EXEMPT
    )


def run_scan(root: Path, files: list[Path], live: set[str], degraded: bool
             ) -> tuple[list[tuple[str, Candidate]], list[tuple[str, Candidate]], list[str]]:
    """(findings, degraded_skips, read_errors) over the selected ``files``."""
    findings: list[tuple[str, Candidate]] = []
    skipped: list[tuple[str, Candidate]] = []
    errors: list[str] = []
    for path in files:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{rel}: not valid UTF-8; an undecodable selected "
                          f"file cannot be proven clean")
            continue
        except OSError as exc:
            errors.append(f"{rel}: unreadable ({exc})")
            continue
        try:
            cands = candidate_refs(path, text, rel in MARKDOWN_RECORD_PATHS)
        except GateInputError as exc:
            errors.append(f"{rel}: {exc}")
            continue
        for cand in cands:
            if _is_exempt(rel, cand):
                continue
            if cand.item_id in live:
                continue
            (skipped if degraded else findings).append((rel, cand))
    return findings, skipped, errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Flag stale positional backlog references in tooling prose."
    )
    parser.add_argument("--report", action="store_true",
                        help="print findings but always exit 0 (report-only mode)")
    parser.add_argument("--root", default=None,
                        help="scan-root override for the regression fixtures")
    args = parser.parse_args(argv[1:])

    # Compared against None, not truthiness: an explicit empty --root must
    # reach require_dir and be refused, never silently select the live repo.
    root = require_dir(args.root, "--root") if args.root is not None else REPO_ROOT
    todo_path = root / TODO_REL
    try:
        todo_kind = strict_kind(todo_path)
    except InaccessiblePath as exc:
        print(f"ERROR: required file inaccessible: {todo_path} ({exc})", file=sys.stderr)
        return 2
    if todo_kind != "file":
        print(f"ERROR: required file missing: {todo_path}", file=sys.stderr)
        return 2

    # The private sibling: ABSENT selects the note-8 degraded path; an entry
    # that exists but is not an examinable directory refuses instead (note 9;
    # strict resolution, 3b74), so a broken sibling can never silently read as
    # the sibling-less adopter state.
    try:
        if args.root is not None:
            sibling = root.parent / PRIVATE_SIBLING_DIR
            sibling_kind = strict_kind(sibling)
            if sibling_kind not in (None, "dir"):
                print(f"ERROR: private sibling {sibling} is present but not a "
                      f"directory; refusing the degraded path it would silently "
                      f"select.", file=sys.stderr)
                return 2
            private_dir = sibling if sibling_kind == "dir" else None
        else:
            private_dir = resolve_sibling("private", strict=True)
    except InaccessiblePath as exc:
        print(f"ERROR: the private sibling cannot be examined ({exc}); refusing "
              f"the degraded path it would silently select.", file=sys.stderr)
        return 2

    files, scan_errors = iter_scan_files(root)
    if scan_errors:
        for msg in scan_errors:
            print(f"ERROR: {msg}", file=sys.stderr)
        print("ERROR: the scan could not traverse everything in its scope; a "
              "clean verdict over a partial read would be vacuous (fail closed).",
              file=sys.stderr)
        return 2
    if not files:
        roots = " or ".join(str(root / sub) for sub in SCAN_ROOTS)
        print(f"ERROR: no scannable file under {roots}; refusing to report "
              f"success over an empty scan set.", file=sys.stderr)
        return 2

    try:
        live = load_live_ids(todo_path, private_dir)
    except GateInputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    findings, skipped, read_errors = run_scan(root, files, live, private_dir is None)
    if read_errors:
        for msg in read_errors:
            print(f"ERROR: {msg}", file=sys.stderr)
        return 2

    if skipped:
        # 3b635: the degraded skip exits 0, so a green CI run must not read as a pass for
        # the references it could not check (a reference live in TODO.md was checked).
        print_degraded("gate 107",
                       f"gate 107 skipped the open-versus-deleted check of "
                       f"{len(skipped)} positional reference(s) (no {PRIVATE_SIBLING_DIR} sibling "
                       f"supplies the private backlog lists); this pass attests nothing about them.")
        print(f"NOTE: the private backlog lists are unreachable (no "
              f"{PRIVATE_SIBLING_DIR} sibling), so {len(skipped)} positional "
              f"reference(s) could not be checked open-versus-deleted and are "
              f"SKIPPED (gate-78-style graceful degradation):")
        for rel, cand in skipped:
            print(f"  {rel}:{cand.line}: {cand.token!r}")

    if not findings:
        print("OK: no stale positional backlog references in tools/, "
              ".claude/ and .github/ provenance prose.")
        return 0

    by_file: dict[str, list[Candidate]] = {}
    for rel, cand in findings:
        by_file.setdefault(rel, []).append(cand)
    for rel in sorted(by_file):
        print(f"=== {rel} ===")
        for cand in sorted(by_file[rel]):
            extra = (" (a todo-ref-ok marker without a reason does not clear it)"
                     if cand.reasonless_marker else "")
            print(f"  line {cand.line}: {cand.token!r} points at {cand.item_id}, "
                  f"which is not a live backlog item in TODO.md or the reachable "
                  f"private lists; re-point it to the durable "
                  f"'{cand.item_id} (closing PR #N)' form, or clear a deliberate "
                  f"mention with 'todo-ref-ok: <reason>'{extra}")
    verdict = "REPORT-ONLY" if args.report else "FAIL"
    print(f"\n{verdict}: {len(findings)} stale tooling backlog reference(s).")
    return 0 if args.report else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
