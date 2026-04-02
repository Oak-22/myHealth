---
description: "Privacy and PHI boundary rules specific to myHealth"
---

# Privacy And PHI Boundary

`myHealth` is designed so that raw PHI/PII should not propagate through
general application code.

## Core Rule

Privacy should be enforced structurally through system boundaries, not
treated as an afterthought at prompt time.

## Working Assumptions

- raw PHI/PII should not appear in normal repository workflows
- pseudonymization and structural transformation should happen before
  data reaches core inference logic
- backend-managed boundaries are responsible for controlling exposure,
  auditability, and allowed data flow

## Agent Guidance

- do not introduce logging that exposes names, identifiers, or raw
  patient details
- prefer pseudonymized or structurally reduced clinical context in code,
  prompts, and tests
- preserve explicit privacy boundaries when refactoring adapters,
  prompts, validation, and inference orchestration
- when a change weakens the privacy boundary, treat it as an
  architectural issue rather than a small implementation detail

## Boundary Orientation

When working in this repo, pay special attention to:

- ingestion adapters
- pseudonymization boundaries
- prompt construction
- verifier / output checking
- audit-sensitive persistence and observability paths
