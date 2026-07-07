---
name: adr-sync-update
description: "Keep architecture docs and ADRs synchronized with implementation. Use after architecture-affecting changes to services, boundaries, or stack choices."
argument-hint: "What changed in implementation and which ADR/doc is affected?"
---
# ADR Sync Update

## When to use
- Service boundaries changed.
- Runtime or storage decisions changed.
- Governance assumptions changed across clinical versus preclinical paths.

## Procedure
1. Confirm architecture impact in docs/architecture and docs/adr.
2. Update impacted ADR files and architecture docs with concise decision rationale.
3. Ensure implementation references and docs do not conflict.
4. Flag unresolved tradeoffs and follow-up ADR requirements.

## Output format
- Files updated
- Decision rationale
- Open architecture questions
