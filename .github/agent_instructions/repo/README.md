# Repository Instructions

Routing: Read this file fully for work inside `myHealth` where local architecture, privacy boundaries, ingestion contracts, or agent-control workflow matter.

This directory holds repository-specific guidance for AI-human
collaboration in `myHealth`.

## Current Focus

`myHealth` is evolving into a backend-centric, event-driven health data
platform with storage-first ingestion and private worker isolation for
clinical, pre-clinical molecular, and genomic payloads.

## Current Files

- `myhealth-context.md`
  Project context, architecture direction, stack, and source-of-truth
  links.
- `privacy-and-phi-boundary.md`
  Privacy, PHI/PII, pseudonymization, and inference boundary rules.
- `ingestion-contracts.md`
  Agent rules for storage-first ingestion, idempotency, event schemas,
  parser strategies, and worker boundaries.
- `control-plan.md`
  Instruction-control plan for canonical paths, template redundancy,
  public/private instruction layering, and implementation expectations.

## Task Routing

- Architecture, stack, ADR, or service-boundary changes:
  load `myhealth-context.md` and `control-plan.md`.
- Ingestion, S3, queue, idempotency, parser, worker, contract, or test
  changes: load `ingestion-contracts.md`.
- PHI, prompts, inference, logging, audit, observability, or test-data
  changes: load `privacy-and-phi-boundary.md`.

## Repo-Specific Guidance

- Keep frontend behavior thin; backend services own state transitions.
- Use the locked UI stack: FastAPI + Jinja2 + HTML/CSS, with HTMX only
  as optional progressive enhancement and no custom JS/TS.
- Treat ingestion manifests, event schemas, idempotency keys, and parser
  strategies as first-class contracts.
- Prefer pseudonymous subject references in examples and tests.
- Avoid logging raw clinical identifiers, file contents, or source PHI.
- Keep public docs and checked-in instructions independent of private
  local config paths.
- Prefer relative links for repo-internal references.
