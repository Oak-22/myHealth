---
name: ingestion-contract-evolution
description: "Evolve ingestion contracts safely. Use when changing schemas, events, idempotency behavior, parser strategy routing, or ingestion tests."
argument-hint: "Describe the contract change and affected payload types"
---
# Ingestion Contract Evolution

## When to use
- You are adding or modifying ingestion schema fields.
- You are changing registration, event emission, idempotency keys, or strategy routing.
- You need compatibility checks and focused tests before merge.

## Procedure
1. Identify affected contracts under src/myhealth/ingestion.
2. Implement additive and explicit contract updates.
3. Update tests under tests/test_ingestion_contracts.py.
4. Update docs/contracts/ingestion_phase_1_contracts.md if behavior changed.
5. Run focused checks:
   - pytest -q tests/test_ingestion_contracts.py
   - ruff check src tests
   - mypy src

## Output format
- Contract delta summary
- Compatibility risk
- Validation evidence
