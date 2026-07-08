---
name: adr-sync-update
description: "Keep architecture docs and ADRs synchronized with harness, contract, sequencing, or future implementation decisions."
argument-hint: "What changed and which ADR/doc is affected?"
---
# ADR Sync Update

## When to use
- Service boundaries changed.
- Runtime or storage decisions changed.
- Governance assumptions changed across clinical versus preclinical paths.
- Harness mode, evaluation posture, or implementation sequencing changed.

## Procedure
1. Confirm architecture impact in docs/architecture and docs/adr.
2. Update impacted ADR files and architecture docs with concise decision rationale.
3. Ensure implementation, harness, and documentation references do not conflict.
4. Flag unresolved tradeoffs and follow-up ADR requirements.

## Output format
- Files updated
- Decision rationale
- Open architecture questions
