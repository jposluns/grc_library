#!/usr/bin/env python3
"""Per-PR handoff-snapshot freshness delta gate (D7).

When a pull request touches the session handoff
(``.working/session-handoff.md``), the close-out checklist's
reconcile-not-append discipline requires the refreshed Current-truth
snapshot line to describe the state the PR itself produces. This delta
gate mechanizes the version-token half of that discipline (the
maintainer-accepted graduation of the append-not-reconcile class, which
reached SEVEN logged occurrences, #619 / #622 / #628 / #629 a1 / #630 F1
/ #632 a2 / #633 round-1 F3, without the prose checklist line
extinguishing it): every backtick-quoted version token the snapshot line
carries for a known, labelled surface must equal that surface's live
header value in the SAME tree (the PR head), and no labelled surface may
carry more than one token (the duplicate-token shape of the seventh
occurrence fails here too).

Why delta-scoped, not a standing gate: the snapshot legitimately drifts
forward between refreshes (its own preamble says "verify against live
files at /resume"), and the close-out refresh batches into the NEXT PR
by recursion-avoidance, so merged ``main`` lags by one PR by design. The
invariant is snapshot-fresh-AT-REFRESH-TIME, never snapshot-fresh-always,
and refresh time is exactly "a PR whose diff touches the handoff".

Scope is deliberately version-tokens-only (mechanical, false-positive
free): prose claims on the same line (merged-through numbers, green-at
SHAs, "in flight" branch names, rides-the-next-PR annotations) stay
convention-guarded. To keep the parse unambiguous, a labelled token is
the FIRST backtick span immediately following a known label; a second
labelled occurrence of the same surface anywhere in the line is a
duplicate-token failure. Labels whose token is absent from the line are
skipped (the line is prose, not a form); a label present with its named
live file missing fails loud; a touched handoff with no Current-truth
line fails loud (malformed working state).

The snapshot line is located as the FIRST line containing the marker
``Version snapshot (D7 validates these tokens)`` (a dedicated, token-bearing
marker the handoff author sets for D7). An earlier "Current truth" header
marker located a token-less header line, so the check passed vacuously and
validated nothing (TODO 3.89 / 3.101, fixed 2026-07-23); the non-vacuity guard
in ``validate_snapshot_tokens`` now FAILS a located line that carries no
recognized token, so a future layout drift fails loud instead of passing
silently. One remaining parse note: the ``README`` label matches any
"README" immediately followed by a backtick token, so a snapshot
phrasing like ``pack README `x.y.z``` would compare the pack version
against the root README's header and false-fail. Keep the marker text
unique to the snapshot line and quote the pack version as ``pack
`x.y.z``` (the standing form).

Checked labels (label pattern -> live file and header field):

  - ``library `YYYY.MM.NNN```        -> README.md            **Library Version:**
  - ``README `X.Y.Z```               -> README.md            **README Version:**
  - ``pack `X.Y.Z```                 -> dev-security/claude-rules/README.md **Version:**
  - ``audit-spec `X.Y.Z```           -> governance/specification-audit-programme.md **Version:**
  - ``guardrail-history `X.Y.Z```    -> .working/guardrail-reviews/history.md **Version:**
  - ``validate-pr history `X.Y.Z```  -> .working/validate-pr/history.md **Version:**
  - ``improvement-log `X.Y.Z```      -> .working/improvement-log.md **Version:**
  - ``claim-fit history `X.Y.Z```    -> .working/claim-fit/history.md **Version:**

This is a CI-only delta gate (D7), not part of the corpus audit
programme inventory in governance/specification-audit-programme.md
section 6; it is documented in section 6.1 (PR-only delta gates)
alongside D1 through D6 and is exempt from gate 35's parity audit (its
inputs, a git history range and the PR base ref, are not available to
tools/run_all_audits.sh or .pre-commit-config.yaml).

Usage:
  python3 tools/check-handoff-snapshot-on-pr.py [BASE_REF] [HEAD_REF]

BASE_REF defaults to the GitHub Actions PR base (GITHUB_BASE_REF as
``origin/<branch>``) or ``origin/main``; HEAD_REF defaults to ``HEAD``.
Exit 0 on pass or not-triggered; exit 1 on a stale, duplicated, or
unresolvable token; exit 2 on environment errors (git failures).
"""

import os
import re
import subprocess
import sys

HANDOFF = ".working/session-handoff.md"

# Label pattern -> (live file, header regex). Order matters only for
# report readability. Each label regex is anchored on a word boundary and
# expects the token as the first backtick span after the label; the
# labels cannot collide because the label texts are disjoint.
SURFACES = [
    (
        "library",
        re.compile(r"\blibrary `([0-9]{4}\.[0-9]{2}\.[0-9]+)`"),
        "README.md",
        re.compile(r"^\*\*Library Version:\*\*\s+([0-9]{4}\.[0-9]{2}\.[0-9]+)", re.M),
    ),
    (
        "README",
        re.compile(r"\bREADME `([0-9]+\.[0-9]+\.[0-9]+)`"),
        "README.md",
        re.compile(r"^\*\*README Version:\*\*\s+([0-9]+\.[0-9]+\.[0-9]+)", re.M),
    ),
    (
        "pack",
        re.compile(r"\bpack `([0-9]+\.[0-9]+\.[0-9]+)`"),
        "dev-security/claude-rules/README.md",
        re.compile(r"^\*\*Version:\*\*\s+([0-9]+\.[0-9]+\.[0-9]+)", re.M),
    ),
    (
        "audit-spec",
        re.compile(r"\baudit-spec `([0-9]+\.[0-9]+\.[0-9]+)`"),
        "governance/specification-audit-programme.md",
        re.compile(r"^\*\*Version:\*\*\s+([0-9]+\.[0-9]+\.[0-9]+)", re.M),
    ),
    (
        "guardrail-history",
        re.compile(r"\bguardrail-history `([0-9]+\.[0-9]+\.[0-9]+)`"),
        ".working/guardrail-reviews/history.md",
        re.compile(r"^\*\*Version:\*\*\s+([0-9]+\.[0-9]+\.[0-9]+)", re.M),
    ),
    (
        "validate-pr history",
        re.compile(r"\bvalidate-pr history `([0-9]+\.[0-9]+\.[0-9]+)`"),
        ".working/validate-pr/history.md",
        re.compile(r"^\*\*Version:\*\*\s+([0-9]+\.[0-9]+\.[0-9]+)", re.M),
    ),
    (
        "improvement-log",
        re.compile(r"\bimprovement-log `([0-9]+\.[0-9]+\.[0-9]+)`"),
        ".working/improvement-log.md",
        re.compile(r"^\*\*Version:\*\*\s+([0-9]+\.[0-9]+\.[0-9]+)", re.M),
    ),
    (
        "claim-fit history",
        re.compile(r"\bclaim-fit history `([0-9]+\.[0-9]+\.[0-9]+)`"),
        ".working/claim-fit/history.md",
        re.compile(r"^\*\*Version:\*\*\s+([0-9]+\.[0-9]+\.[0-9]+)", re.M),
    ),
]

# The snapshot line is the one the handoff author dedicates to D7 by an explicit
# marker. It changed once (a "Current truth" header bullet, which carries NO
# version tokens, used to be matched; the tokens moved to a dedicated
# "Version snapshot (D7 validates these tokens)" sub-line, so the old marker
# located a token-less line and the check passed vacuously, TODO 3.89 / 3.101).
# The marker below matches the token-bearing line; the non-vacuity guard in
# validate_snapshot_tokens fails loudly if a future layout drift ever again
# locates a line with no recognized token, so this class cannot silently recur.
SNAPSHOT_MARKER = "Version snapshot (D7 validates these tokens)"


def run_git(args):
    try:
        out = subprocess.run(
            ["git"] + args, capture_output=True, text=True, check=False
        )
    except OSError as exc:
        print(f"D7: git invocation failed: {exc}", file=sys.stderr)
        sys.exit(2)
    return out


def blob(ref, path):
    """Return the file's content at ref, or None if absent there."""
    out = run_git(["show", f"{ref}:{path}"])
    if out.returncode != 0:
        return None
    return out.stdout


def snapshot_line(handoff_text):
    """Return the version-snapshot line (the first line carrying the marker),
    or None."""
    for line in handoff_text.splitlines():
        if SNAPSHOT_MARKER in line:
            return line
    return None


def validate_snapshot_tokens(line, live_texts):
    """Pure core: validate every labelled version token on the snapshot ``line``
    against the corresponding live header in ``live_texts`` (a dict mapping each
    SURFACES live_path to its text, or None if absent at the PR head).

    Returns ``(checked, failures)``. ``checked`` is the number of tokens actually
    compared against a live header; ``failures`` is the human-readable list. A
    snapshot line that carries NO recognized token yields ``checked == 0`` and a
    non-vacuity failure (the guard against the TODO 3.89 / 3.101 vacuous-pass
    class), so the caller never reports OK on a line the check did not truly
    validate. Kept git-free so it is unit-testable via --self-test.
    """
    failures = []
    checked = 0
    for label, token_re, live_path, header_re in SURFACES:
        tokens = token_re.findall(line)
        if not tokens:
            continue
        if len(tokens) > 1:
            failures.append(
                f"duplicate token: label '{label}' appears {len(tokens)} "
                f"times on the snapshot line ({', '.join(tokens)}); a "
                "reconciled line carries each surface once"
            )
            continue
        token = tokens[0]
        live = live_texts.get(live_path)
        if live is None:
            failures.append(
                f"unresolvable label: '{label}' quotes `{token}` but "
                f"{live_path} is absent at the PR head"
            )
            continue
        m = header_re.search(live)
        if m is None:
            failures.append(
                f"unresolvable label: '{label}' quotes `{token}` but "
                f"{live_path} carries no parsable header version field"
            )
            continue
        live_value = m.group(1)
        checked += 1
        if token != live_value:
            failures.append(
                f"stale token: '{label}' quotes `{token}` but {live_path} "
                f"at the PR head carries `{live_value}`"
            )
    if checked == 0 and not failures:
        failures.append(
            "non-vacuity: the located snapshot line carries no recognized "
            "version token, so D7 would validate nothing (the snapshot layout "
            "or the marker drifted). Quote at least one labelled token "
            "(library / README / pack / ...) on the snapshot line."
        )
    return checked, failures


def main():
    if os.environ.get("GITHUB_BASE_REF"):
        default_base = f"origin/{os.environ['GITHUB_BASE_REF']}"
    else:
        default_base = "origin/main"
    base_ref = sys.argv[1] if len(sys.argv) > 1 else default_base
    head_ref = sys.argv[2] if len(sys.argv) > 2 else "HEAD"

    mb = run_git(["merge-base", base_ref, head_ref])
    if mb.returncode != 0:
        print(
            f"D7: cannot resolve merge-base of {base_ref} and {head_ref}: "
            f"{mb.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(2)
    base_sha = mb.stdout.strip()

    changed = run_git(["diff", "--name-only", f"{base_sha}..{head_ref}"])
    if changed.returncode != 0:
        print(f"D7: git diff failed: {changed.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    if HANDOFF not in changed.stdout.splitlines():
        print("D7 OK: session handoff untouched by this PR; not triggered.")
        return 0

    handoff = blob(head_ref, HANDOFF)
    if handoff is None:
        # Handoff deleted by the PR (e.g. an adopter fork stripping
        # .working/): nothing to validate.
        print("D7 OK: session handoff absent at head; not triggered.")
        return 0

    line = snapshot_line(handoff)
    if line is None:
        print(
            f"D7 FAIL: {HANDOFF} is in this PR's diff but carries no "
            f"'{SNAPSHOT_MARKER}' snapshot line (malformed working "
            "state).",
            file=sys.stderr,
        )
        return 1

    # Resolve each distinct live file once, then validate via the pure core.
    live_texts = {}
    for _label, _token_re, live_path, _header_re in SURFACES:
        if live_path not in live_texts:
            live_texts[live_path] = blob(head_ref, live_path)
    checked, failures = validate_snapshot_tokens(line, live_texts)

    if failures:
        print(
            f"D7 FAIL: the {HANDOFF} Current-truth snapshot line was "
            "refreshed in this PR but does not match the state the PR "
            "itself produces:",
            file=sys.stderr,
        )
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        print(
            "Reconcile every quoted version token to the PR-head value "
            "(the close-out checklist's reconcile-not-append line), or "
            "remove the stale token.",
            file=sys.stderr,
        )
        return 1

    print(
        f"D7 OK: handoff snapshot line reconciled; {checked} labelled "
        "version token(s) match the PR head's live headers."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
