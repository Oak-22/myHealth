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

if command -v pytest >/dev/null 2>&1; then
  run_check "pytest ingestion contracts" pytest -q tests/test_ingestion_contracts.py
else
  skips+=("pytest")
fi

if command -v bandit >/dev/null 2>&1; then
  run_check "bandit" bandit -q -r src/myhealth
else
  skips+=("bandit")
fi

if [ ${#failures[@]} -eq 0 ] && [ ${#skips[@]} -eq 0 ]; then
  echo '{"continue": true}'
  exit 0
fi

msg="Session-end soft gate summary"
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
