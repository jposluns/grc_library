#!/usr/bin/env bash
# ci-status.sh (3b167 ORCH-CI-STATUS): the fleet-owned /orch command (step 4) names "the
# repo's ci-status.sh" as the CI reader. The logic lives in tools/ci-status.py, per this
# repository's Python-tool conventions (in-process testable with gh stubbed); this wrapper
# exists so the /orch-documented name works verbatim. Same arguments, same exit codes
# (0 green, 1 not green, 2 usage/gh error, 3 pending): see `python3 tools/ci-status.py --help`.
set -euo pipefail
exec python3 "$(dirname "$0")/ci-status.py" "$@"
