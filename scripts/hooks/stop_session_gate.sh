#!/usr/bin/env bash
set -euo pipefail

failures=()
skips=()

run_check() {
  local label="$1"
  shift
  if "$@"; then
    return 0
  fi
  failures+=("$label")
}

for hook in scripts/hooks/*.sh; do
  run_check "bash syntax $hook" bash -n "$hook"
done

for hook_config in .github/hooks/*.json; do
  run_check "hook json $hook_config" python3 -m json.tool "$hook_config" >/dev/null
done

if [ ${#failures[@]} -eq 0 ] && [ ${#skips[@]} -eq 0 ]; then
  echo '{"continue": true}'
  exit 0
fi

msg="Session-end harness soft gate summary"
if [ ${#failures[@]} -gt 0 ]; then
  msg+="; failed: ${failures[*]}"
fi
if [ ${#skips[@]} -gt 0 ]; then
  msg+="; skipped (not installed): ${skips[*]}"
fi

python3 - <<'PY' "$msg"
import json
import sys

print(json.dumps({"continue": True, "systemMessage": sys.argv[1]}))
PY
