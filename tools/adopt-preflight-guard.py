#!/usr/bin/env python3
"""Pre-flight adopter-clone guard for /adopt (TODO section 3.92b).

`/adopt` is the RUN-ONCE fork-onboarding that RESETS the machinery-core `.working/`
working-state to clean adopter baselines. That reset is destructive on the WRONG
clone: run on the maintainer's own repo (or a maintainer's fresh-machine clone) it
would wipe live operational state. The dangerous direction is already defended by
the host-pinned origin match, the step-1 operator confirmation, the adopt-config
short-circuit, and git-revertability; this helper moves the guard from convention
to a MECHANICAL pre-flight: /adopt step 1 invokes it, and it refuses (non-zero,
so the destructive reset does NOT proceed) unless the operator identity classifies
as `adopter`.

It is a thin wrapper over the single source of truth for operator identity,
`tools/detect-env.py`: it runs the probe, reads `identity.classification`, and
gates on it, so the classification logic lives in exactly one place. It makes NO
independent classification decision.

FAIL-SAFE: any outcome other than a confirmed `adopter` classification REFUSES
(a `maintainer` / `maintainer-fresh-machine` clone, an undetermined identity, a
probe error, or malformed probe output). The safe default for a destructive reset
is to NOT run.

Exit codes (binary by design: proceed only on a confirmed adopter, else refuse):
  0   classification is `adopter`: /adopt may proceed.
  3   REFUSED: any other outcome. This deliberately collapses every non-adopter
      case into one refuse code: a `maintainer` / `maintainer-fresh-machine`
      classification, an undetermined identity, OR a probe that could not be
      located, failed / timed out, or returned unparseable output. /adopt must
      NOT run its working-state reset in any of these. The printed message
      distinguishes "not adopter" from "could not determine"; the exit code does
      not, because both block /adopt equally.

It is a utility helper invoked by /adopt, NOT an audit gate: it is not wired into
run_all_audits.sh and never runs in CI.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DETECT_ENV = REPO_ROOT / "tools" / "detect-env.py"


def classify() -> "str | None":
    """Return the operator classification from detect-env, or None on any failure.

    None (not a string) means the probe could not be run or did not yield a
    classification: the caller treats that as a REFUSE (fail-safe).
    """
    if not DETECT_ENV.exists():
        return None
    try:
        proc = subprocess.run(
            [sys.executable, str(DETECT_ENV), "--json"],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    try:
        data = json.loads(proc.stdout)
    except (json.JSONDecodeError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    identity = data.get("identity")
    if not isinstance(identity, dict):
        return None
    cls = identity.get("classification")
    return cls if isinstance(cls, str) else None


def main(argv: "list[str] | None" = None) -> int:
    cls = classify()
    if cls == "adopter":
        print("adopt-preflight-guard: OK -- operator identity is 'adopter'; "
              "/adopt may proceed.")
        return 0
    if cls is None:
        print(
            "adopt-preflight-guard: REFUSED -- could not determine the operator "
            "identity (detect-env probe missing, failed, or returned no "
            "classification). /adopt's working-state reset must NOT run on an "
            "undetermined identity; resolve the environment and re-run.",
            file=sys.stderr,
        )
        return 3
    print(
        f"adopt-preflight-guard: REFUSED -- operator identity is '{cls}', not "
        "'adopter'. /adopt resets working-state to adopter baselines and must run "
        "ONLY on a confirmed adopter (fork) clone, never on the maintainer's own "
        "repo or a maintainer fresh-machine clone. The reset was NOT run.",
        file=sys.stderr,
    )
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
