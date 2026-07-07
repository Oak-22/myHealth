---
name: release-readiness-gate
description: "Run a release-readiness gate across tests, lint, typing, and security checks. Use before release tagging or deployment decisions."
argument-hint: "Optional scope (full repo, ingestion only, docs only)"
---
# Release Readiness Gate

## When to use
- Before release branch cut, tag, or deployment approval.
- After significant backend or ingestion contract changes.

## Procedure
1. Run validation commands:
   - ruff check src tests
   - mypy src
   - pytest -q
   - bandit -q -r src/myhealth
   - pip-audit
2. Capture failing checks and likely root causes.
3. Categorize blockers versus warnings.
4. Produce a concise go/no-go recommendation.

## Output format
- Validation matrix
- Blockers
- Recommendation (go, conditional go, no-go)
