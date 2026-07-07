#!/usr/bin/env bash
set -euo pipefail

payload="$(cat)"

tool_name="$(python3 - <<'PY' <<<"$payload"
import json
import sys

raw = sys.stdin.read().strip()
if not raw:
    print("")
    raise SystemExit(0)
try:
    event = json.loads(raw)
except json.JSONDecodeError:
    print("")
    raise SystemExit(0)
print(event.get("tool_name", ""))
PY
)"

case "$tool_name" in
  apply_patch|create_file|edit_notebook_file|vscode_renameSymbol|mcp_provides_tool_pylanceInvokeRefactoring)
    ;;
  *)
    echo '{"continue": true}'
    exit 0
    ;;
esac

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

if command -v ruff >/dev/null 2>&1; then
  run_check "ruff check" ruff check src tests
else
  skips+=("ruff")
fi

if command -v mypy >/dev/null 2>&1; then
  run_check "mypy" mypy src
else
  skips+=("mypy")
fi

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

if command -v pip-audit >/dev/null 2>&1; then
  run_check "pip-audit" pip-audit
else
  skips+=("pip-audit")
fi

if [ ${#failures[@]} -eq 0 ] && [ ${#skips[@]} -eq 0 ]; then
  echo '{"continue": true}'
  exit 0
fi

msg="Soft-fail validation summary"
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
