#!/usr/bin/env bash
# run_all_checks.sh: the name the lab_infra-standard /orch step 4 looks for ("run the repo's
# tools/run_all_checks.sh unpiped to confirm the gates are green"). This project's mechanical
# gate runner is run_all_audits.sh; this is a thin pass-through wrapper so the standard /orch
# runs our full audit suite. Keep in lock-step: any flags/env the runner accepts pass through.
exec "$(dirname "$0")/run_all_audits.sh" "$@"
