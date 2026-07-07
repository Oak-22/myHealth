---
description: "Use for myHealth architecture, stack, service-boundary, documentation, or implementation work."
applyTo: "src/**/*.py, docs/**/*.md, tests/**/*.py, .github/**/*.md"
---
# myHealth Context

`myHealth` is a backend-centric, event-driven personal health data and
inference platform with a dual-domain governance model.

## Architectural Direction

- Backend-managed services are authoritative; the frontend is a thin
  delivery layer.
- FastAPI is the primary Python service framework.
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

## Stack Direction

- FastAPI, Jinja2, HTML forms/links, CSS, and optional HTMX for
  server-rendered partial updates.
- No authored custom JavaScript or TypeScript, React, Next.js, Node.js
  frontend runtime, or SPA architecture.
- Streamlit only for internal experiments, analytical prototypes, and
  research cockpit workflows.
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
- [Ingestion Phase 1 Contracts](../../docs/contracts/ingestion_phase_1_contracts.md)
