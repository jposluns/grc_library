#!/usr/bin/env python3
"""Pre-flight adopter-clone guard for /adopt (§3.92.b, tool-side shipped in PR #1017).

`/adopt` is the RUN-ONCE fork-onboarding that RESETS the machinery-core `.working/`
working-state to clean adopter baselines. That reset is destructive on the WRONG
clone: run on a clone whose origin is the maintainer repository, it
would wipe live operational state. The dangerous direction is already defended by
the host-pinned origin match, the step-1 operator confirmation, the adopt-config
short-circuit, and git-revertability; this helper moves the guard from convention
to a MECHANICAL pre-flight: /adopt step 1 invokes it, and it refuses (non-zero,
so the destructive reset does NOT proceed) unless the clone classifies as
`adopter`.

Classification (decision D4) uses repository-local evidence only, through the one
origin classifier the shipped tools share: `_operator_context` in
`build-reference-manifest.py`, beside this file. It reads git's `origin` twice (the
second time with no `GIT_` variable in its environment), requires both reads to
give the same single line, and places that origin against the maintainer repository
the classifier declares (`MAINTAINER_ORIGIN_OWNER_REPO`). An https, http or ssh URL
or a `user@host:owner/repo` form naming another owner/repo is `adopter`; the
maintainer repository on github.com is `maintainer`; anything else (no readable
origin, a redirected repository, a local-path or other unplaced origin, the
maintainer repository on another host, two reads that disagree) is undetermined.
This guard makes NO independent classification decision.

FAIL-SAFE: any outcome other than a confirmed `adopter` classification REFUSES
(a `maintainer` clone, an undetermined identity, or a classifier that could not be
loaded or raised). The safe default for a destructive reset is to NOT run.

Exit codes (binary by design: proceed only on a confirmed adopter, else refuse):
  0   classification is `adopter`: /adopt may proceed.
  3   REFUSED: any other outcome. This deliberately collapses every non-adopter
      case into one refuse code: a `maintainer` classification, an undetermined
      identity, OR a classifier that could not be loaded or failed. /adopt must
      NOT run its working-state reset in any of these. The printed message
      distinguishes "not adopter" from "could not determine"; the exit code does
      not, because both block /adopt equally.

It is a utility helper invoked by /adopt, NOT an audit gate: it is not wired into
run_all_audits.sh and never runs in CI.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

CLASSIFIER = Path(__file__).resolve().parent / "build-reference-manifest.py"


def _load_classifier():
    """Load the shared origin classifier module by path (its file name is hyphenated)."""
    spec = importlib.util.spec_from_file_location("_adopt_guard_origin_classifier", CLASSIFIER)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def classify() -> "str | None":
    """Return "adopter" or "maintainer" from the shared origin classifier, or None.

    None (not a string) means the identity could not be determined, or the
    classifier could not be loaded or raised: the caller treats that as a REFUSE
    (fail-safe).
    """
    try:
        mod = _load_classifier()
        if mod is None:
            return None
        context, _reason = mod._operator_context()
    except KeyboardInterrupt:
        raise
    except BaseException:  # noqa: BLE001 (deliberate: any failure is undetermined, never adopter)
        return None
    return context if context in ("adopter", "maintainer") else None


def main(argv: "list[str] | None" = None) -> int:
    cls = classify()
    if cls == "adopter":
        print("adopt-preflight-guard: OK -- operator identity is 'adopter'; "
              "/adopt may proceed.")
        return 0
    if cls is None:
        print(
            "adopt-preflight-guard: REFUSED -- could not determine the operator "
            "identity (the origin classifier could not be loaded, failed, or could "
            "not place this clone's origin). /adopt's working-state reset must NOT "
            "run on an undetermined identity; resolve the environment and re-run.",
            file=sys.stderr,
        )
        return 3
    print(
        f"adopt-preflight-guard: REFUSED -- operator identity is '{cls}', not "
        "'adopter'. /adopt resets working-state to adopter baselines and must run "
        "ONLY on a confirmed adopter (fork) clone, never on a clone whose origin "
        "is the maintainer repository. The reset was NOT run.",
        file=sys.stderr,
    )
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
