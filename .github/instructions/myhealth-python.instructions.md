---
description: "Use when editing Python code, tests, ingestion contracts, or service modules in myHealth."
applyTo: "src/**/*.py, tests/**/*.py, scripts/**/*.py"
---
# myHealth Python Working Rules

- Keep backend services authoritative for state transitions.
- Preserve storage-first ingestion and idempotency-first registration semantics.
- Prefer extending existing modules under src/myhealth before adding new service layers.
- Add focused tests when changing contracts, schemas, parser strategies, or idempotency behavior.
- Keep examples and fixtures pseudonymized; do not introduce PHI-like identifiers.
- Avoid introducing custom JavaScript or TypeScript into this repository.
