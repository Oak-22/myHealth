---
description: "Use for myHealth architecture, stack, service-boundary, documentation, harness-evaluation, or future implementation planning work."
applyTo: "docs/**/*.md, .github/**/*.md, scripts/hooks/**/*.sh"
---
# myHealth Context

`myHealth` is a backend-centric, event-driven personal health data and
inference platform concept with a dual-domain governance model.

Current repository mode: harness evaluation target. Product
implementation code is intentionally absent until ADR 0009 and ADR 0010
readiness criteria are satisfied or explicitly amended.

## Architectural Direction

- Backend-managed services remain the intended authoritative boundary;
  the frontend remains a thin delivery layer concept.
- Active implementation language and framework choices are deferred
  while the repository is used as a harness evaluation target.
- The active distributed direction is defined by ADR 0006:
  event-driven service isolation for learning architecture.
- The first service boundaries are the Health Gateway Service, Clinical
  Ingestion Worker, and Genomic Annotation Worker.
- Clinical workflows are restrained, privacy-first, and
  patient-context aware.
- Preclinical molecular and genomic workflows may be more autonomous
  and compute-oriented when operating on public, synthetic, non-PHI, or
  pseudonymized payloads.
- Large payloads use a storage-first path:
  registration -> idempotent transaction ID -> raw object reference ->
  upload validation -> queue task event -> private worker.
- Multimodal and LLM reasoning belong in backend-managed workflows, not
  in UI code.

## Engineering Priorities

- Security and privacy of sensitive health data.
- Durable data models, service contracts, and invariant enforcement.
- Clear ingestion, parser, and transformation boundaries.
- Idempotent retry behavior for large asynchronous payloads.
- Observability, auditability, and operational correctness.
- Clear separation between product LLM inference controls and
  development-agent instruction scaffolding.
- Current sequencing: postpone substantial product implementation until
  the agentic harness/control-plane foundation and AgentOps
  token-economics observability foundation are solid enough to support
  repeatable, observable agent-assisted development. See ADR 0009.

## Stack Direction

- No active product implementation stack is currently present.
- Historical stack ADRs remain useful as product intent, but they are
  deferred by ADR 0010 until product implementation resumes.
- Amazon S3 for raw object vault storage.
- AWS Lambda for lightweight edge ingest validation and event
  publication.
- Amazon SQS for asynchronous ingestion, parsing, indexing, and
  projection queues.
- PostgreSQL as the primary transactional system of record.
- pgvector for retrieval metadata and embeddings.
- DynamoDB for workflow checkpoints, idempotency records, and ephemeral
  coordination state.
- Redis for read-optimized projections and short-lived cache state.
- BigQuery and Parquet for analytics.
- Bedrock-backed inference routed through backend-managed services.

## Source Of Truth

Use these canonical docs for deeper system details:

- [System Architecture](../../docs/architecture/system_architecture.md)
- [System Spec](../../docs/architecture/system_spec.md)
- [Technology Stack](../../docs/architecture/technology_stack.md)
- [ADR 0006](../../docs/adr/0006_event_driven_service_isolation.md)
- [ADR 0007](../../docs/adr/0007_dual_domain_governance.md)
- [ADR 0008](../../docs/adr/0008_server_rendered_python_first_ui.md)
- [ADR 0009](../../docs/adr/0009_sequence_myhealth_after_agentic_foundation.md)
- [ADR 0010](../../docs/adr/0010_convert_myhealth_to_harness_evaluation_target.md)
- [Ingestion Phase 1 Contracts](../../docs/contracts/ingestion_phase_1_contracts.md)
