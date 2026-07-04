---
description: "Privacy and PHI boundary rules specific to myHealth"
---

# Privacy And PHI Boundary

Routing: Read this file fully for work involving PHI/PII, clinical data, prompts, inference, logging, audit trails, tests, or persistence boundaries.

`myHealth` is designed so that raw PHI/PII should not propagate through
general application code.

## Core Rule

Privacy should be enforced structurally through system boundaries, not
treated as an afterthought at prompt time.

## Working Assumptions

- Raw PHI/PII should not appear in normal repository workflows.
- Pseudonymization and structural transformation should happen before
  data reaches core inference logic.
- The Health Gateway Service controls user-facing intake and identity
  context.
- Private ingestion and annotation workers should operate on scoped
  manifests, storage references, pseudonymous subject references, and
  explicit workflow state.
- Clinical workflows are restrained by default. Preclinical molecular
  and genomic workflows may be more autonomous only when they operate on
  public, synthetic, non-PHI, or pseudonymized payloads.
- Backend-managed boundaries are responsible for controlling exposure,
  auditability, and allowed data flow.

## Agent Guidance

- Do not introduce logging that exposes names, identifiers, raw file
  contents, or raw patient details.
- Prefer pseudonymized or structurally reduced clinical context in code,
  prompts, docs, and tests.
- Preserve explicit privacy boundaries when refactoring adapters,
  prompts, validation, and inference orchestration.
- Treat a weakened privacy boundary as an architectural issue rather
  than a small implementation detail.
- Do not put PHI into queue payloads. Queue events should carry manifest
  IDs, transaction IDs, storage references, source type, job type, and
  trace metadata.
- Do not put direct raw payload bytes in tests unless the data is
  synthetic and clearly non-identifying.
- Do not promote preclinical molecular analysis into patient-facing
  clinical guidance without an explicit review, provenance, and
  pseudonymized linkage boundary.

## LLM Boundary

Development agents and product LLMs are different systems.

- Development agents edit code and docs. They must not receive PHI.
- Product LLMs may later reason over health context only through
  backend-managed, pseudonymized, audited inference workflows.

Checked-in agent instructions do not themselves create product inference
behavior. Keep them lightweight and subordinate to the architecture
docs.

## Boundary Orientation

When working in this repo, pay special attention to:

- upload registration
- raw object vault references
- ingestion manifests
- idempotency records
- queue event schemas
- parser strategies
- pseudonymization boundaries
- prompt construction
- verifier / output checking
- audit-sensitive persistence and observability paths
