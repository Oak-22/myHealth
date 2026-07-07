#!/usr/bin/env bash
set -euo pipefail

payload="$(cat)"

python3 - <<'PY' <<<"$payload"
import json
import re
import sys

raw = sys.stdin.read().strip()
if not raw:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}))
    raise SystemExit(0)

try:
    event = json.loads(raw)
except json.JSONDecodeError:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": "Hook could not parse tool payload; require manual approval."
        },
        "systemMessage": "Guardrail hook could not parse JSON input."
    }))
    raise SystemExit(0)

tool_name = event.get("tool_name", "")
tool_input = event.get("tool_input", {}) or {}
command = ""
if isinstance(tool_input, dict):
    command = str(tool_input.get("command", ""))

risky_patterns = [
    r"\brm\s+-rf\s+/",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\s+-fd\b",
    r"\bDROP\s+TABLE\b",
    r"\bTRUNCATE\s+TABLE\b",
    r"\bcurl\b[^\n|]*\|\s*(bash|sh)\b",
]

if tool_name in {"run_in_terminal", "send_to_terminal"} and command:
    for pattern in risky_patterns:
        if re.search(pattern, command, flags=re.IGNORECASE):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": "Potentially destructive command detected by workspace guardrails."
                },
                "systemMessage": f"Guardrail flagged command for manual approval: {command}"
            }))
            raise SystemExit(0)

print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}))
PY
