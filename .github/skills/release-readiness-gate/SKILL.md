---
name: release-readiness-gate
description: "Run a harness-readiness gate across docs, ADRs, instructions, prompts, skills, hook JSON, and hook scripts."
argument-hint: "Optional scope (full repo, harness only, docs only)"
---
# Release Readiness Gate

## When to use
- Before release branch cut, tag, or harness evaluation milestone.
- After significant ADR, instruction, prompt, skill, hook, or contract changes.

## Procedure
1. Run validation commands:
   - git diff --check
   - bash -n scripts/hooks/*.sh
   - python3 -m json.tool .github/hooks/pretool-guardrails.json
   - python3 -m json.tool .github/hooks/posttool-validation.json
   - python3 -m json.tool .github/hooks/stop-session-gate.json
2. Capture failing checks and likely root causes.
3. Categorize blockers versus warnings.
4. Produce a concise go/no-go recommendation.

## Output format
- Validation matrix
- Blockers
- Recommendation (go, conditional go, no-go)
