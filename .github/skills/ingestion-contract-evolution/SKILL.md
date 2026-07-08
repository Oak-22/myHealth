---
name: ingestion-contract-evolution
description: "Evolve ingestion contracts safely. Use when changing documented schemas, events, idempotency behavior, parser strategy routing, or future test expectations."
argument-hint: "Describe the contract change and affected payload types"
---
# Ingestion Contract Evolution

## When to use
- You are adding or modifying ingestion schema fields.
- You are changing registration, event emission, idempotency keys, or strategy routing.
- You need compatibility checks or future test expectations before merge.

## Procedure
1. Identify affected documented contracts under docs/contracts.
2. Make additive and explicit contract updates.
3. Capture future implementation and test expectations in the contract doc.
4. Update related ADRs or architecture docs if behavior changed.
5. Run focused checks:
   - git diff --check
   - bash -n scripts/hooks/*.sh

## Output format
- Contract delta summary
- Compatibility risk
- Validation evidence
