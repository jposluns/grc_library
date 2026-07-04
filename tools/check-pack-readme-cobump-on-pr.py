#!/usr/bin/env python3
"""Per-PR pack-README version-history co-bump delta gate (D6).

When a pull request changes the ``**Version:**`` value of the pack README
(``dev-security/claude-rules/README.md``), the project's paired-surface
discipline requires the same diff to add the matching row to that README's
``## Version history`` table (a table line whose first cell is the new
version). This delta gate mechanizes instance (a) of the close-out
checklist's paired-surface-completeness guard, which until now was
convention-only and recurrently missable (the pack README carries BOTH the
metadata Version line and its own history table, so bumping one without
the other leaves the pack's shipping history silently incomplete).

Why the existing gates leave the gap: gate 13 (version monotonicity)
confirms the metadata Version only increases; delta gate D2 confirms a
body change carries a Version bump; neither reads the ``## Version
history`` table at all. The pack README's own Date line is D4's to
cover (the #352 case in D4's docstring); this check owes nothing to
the Date discipline. Before this check, no gate paired the Version
VALUE with its history ROW.

Trigger and check, both delta-scoped:

  - TRIGGER: the pack README's ``**Version:**`` value differs between the
    PR merge-base and the PR head.
  - CHECK: the PR's added lines for that file include a version-history
    table row whose first cell is exactly the new version (``| <new> |``).
  - A missing or unparsable Version line at head fails loud (malformed
    metadata is a defect, not an exemption).

There is deliberately NO opt-out trailer: the paired-surface rule is
unconditional (a pack Version bump with no history row has no legitimate
case), and the gate stays silent whenever the Version value did not
change, so bookkeeping-only PRs never see it.

This is a CI-only delta gate (D6), not part of the corpus audit programme
inventory in governance/specification-audit-programme.md section 6; it is
documented in section 6.1 (PR-only delta gates) alongside D1 through D5
and is exempt from gate 35's parity audit (its inputs, a git history
range and the PR base ref, are not available to tools/run_all_audits.sh
or .pre-commit-config.yaml).

Usage:
  python3 tools/check-pack-readme-cobump-on-pr.py [BASE_REF] [HEAD_REF]

BASE_REF defaults to the GitHub Actions PR base (GITHUB_BASE_REF as
``origin/<branch>``) or ``origin/main``; HEAD_REF defaults to ``HEAD``.
Exit 0 on pass or not-triggered; exit 1 on a triggered-and-missing row;
exit 2 on environment errors (git failures).
"""

import os
import re
import subprocess
import sys

PACK_README = "dev-security/claude-rules/README.md"
VERSION_RE = re.compile(r"^\*\*Version:\*\*\s+([0-9]+\.[0-9]+\.[0-9]+)", re.MULTILINE)


def run_git(args):
    try:
        out = subprocess.run(
            ["git"] + args, capture_output=True, text=True, check=False
        )
    except OSError as exc:
        print(f"D6: git invocation failed: {exc}", file=sys.stderr)
        sys.exit(2)
    return out


def blob_version(ref):
    """Return the pack README's Version value at ref, or None if the file
    or the field is absent there."""
    out = run_git(["show", f"{ref}:{PACK_README}"])
    if out.returncode != 0:
        return None
    m = VERSION_RE.search(out.stdout)
    return m.group(1) if m else None


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
            f"D6: cannot resolve merge-base of {base_ref} and {head_ref}: "
            f"{mb.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(2)
    base_sha = mb.stdout.strip()

    base_version = blob_version(base_sha)
    head_version = blob_version(head_ref)

    if head_version is None:
        head_exists = run_git(["cat-file", "-e", f"{head_ref}:{PACK_README}"])
        if head_exists.returncode != 0:
            # Pack README absent at head (e.g. a fork that removed the
            # pack): nothing to pair, not this gate's business.
            print("D6 OK: pack README absent at head; not triggered.")
            return 0
        print(
            f"D6 FAIL: {PACK_README} at head carries no parsable "
            "'**Version:** X.Y.Z' line (malformed metadata).",
            file=sys.stderr,
        )
        return 1

    if base_version == head_version:
        print(
            f"D6 OK: pack README Version unchanged ({head_version}); "
            "not triggered."
        )
        return 0

    diff = run_git(
        ["diff", f"{base_sha}..{head_ref}", "--", PACK_README]
    )
    if diff.returncode != 0:
        print(f"D6: git diff failed: {diff.stderr.strip()}", file=sys.stderr)
        sys.exit(2)

    row_re = re.compile(
        r"^\+\|\s*" + re.escape(head_version) + r"\s*\|"
    )
    for line in diff.stdout.splitlines():
        if row_re.match(line):
            print(
                f"D6 OK: pack README Version {base_version} -> "
                f"{head_version} with a matching version-history row "
                "added in the same diff."
            )
            return 0

    print(
        f"D6 FAIL: the PR changes the pack README Version "
        f"({base_version} -> {head_version}) but adds no "
        f"'| {head_version} | ...' row to its '## Version history' "
        "table in the same diff. Add the paired history row (the "
        "close-out checklist's paired-surface instance (a)).",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
