---
description: "myHealth project context for agents working in this repository"
---

# myHealth Context

Routing: Read this file fully for architecture, stack, system-design, service-boundary, documentation, or implementation work in `myHealth`.

`myHealth` is a backend-centric, event-driven personal health data and
inference platform with a dual-domain governance model.

The repository is focused on:

- storage-first ingestion of heterogeneous health data
- normalization and validation of clinical, biometric, molecular, and
  genomic records
- retrieval-augmented reasoning over longitudinal health context
- durable backend workflows, service contracts, and storage boundaries
- privacy-preserving inference over pseudonymized health context
- more autonomous preclinical molecular and genomic computation over
  public, synthetic, non-PHI, or pseudonymized payloads

## Architectural Direction

- Backend-managed services are authoritative; the frontend is a thin
  delivery layer.
- FastAPI is the primary Python service framework.
- The active distributed direction is defined by ADR 0006:
  event-driven service isolation for learning architecture.
- The first service boundaries are:
  - Health Gateway Service
  - Clinical Ingestion Worker
  - Genomic Annotation Worker
- Governance is split by domain:
  - Clinical workflows are restrained, privacy-first, and
    patient-context aware.
  - Preclinical molecular/genomic workflows may be more autonomous and
    HPC-oriented when they operate on public, synthetic, non-PHI, or
    pseudonymized data.
- Large payloads use a storage-first path:
  registration -> idempotent transaction ID -> S3 pre-signed upload ->
  S3/Lambda validation -> SQS task event -> private worker.
- The system separates operational truth, workflow state, retrieval
  context, read projections, and analytics across different storage
  layers.
- Multimodal and LLM reasoning are integrated into backend workflows,
  not delegated to the UI.

## Engineering Priorities

- security and privacy of sensitive health data
- durable data models, service contracts, and invariant enforcement
- clear ingestion, parser, and transformation boundaries
- idempotent retry behavior for large asynchronous payloads
- observability, auditability, and operational correctness
- deliberate hands-on exposure to distributed systems patterns
- clear separation between product LLM inference controls and
  development-agent instruction scaffolding

## Stack Direction

- Thin frontend or delivery layer for user interaction
- FastAPI route handlers, Jinja2 templates, HTML forms/links, CSS, and
  optional HTMX for server-rendered partial updates
- No authored custom JavaScript or TypeScript, and no React, Next.js,
  Node.js frontend runtime, or SPA architecture
- Streamlit only for internal experiments, analytical prototypes, and
  research cockpit workflows
- Python-first backend services built around FastAPI and worker modules
- Amazon S3 for raw object vault storage
- AWS Lambda for lightweight edge ingest validation and event
  publication
- Amazon SQS for asynchronous ingestion, parsing, indexing, and
  projection queues
- PostgreSQL as the primary transactional system of record
- pgvector for retrieval metadata and embeddings
- DynamoDB for workflow checkpoints, idempotency records, and ephemeral
  coordination state
- Redis for read-optimized projections and short-lived cache state
- BigQuery and Parquet for analytics
- Bedrock-backed inference routed through backend-managed services

## Source Of Truth

For deeper system details, use:

- [System Architecture](../../../docs/architecture/system_architecture.md)
- [System Spec](../../../docs/architecture/system_spec.md)
- [Technology Stack](../../../docs/architecture/technology_stack.md)
- [ADR 0006](../../../docs/adr/0006_event_driven_service_isolation.md)
- [ADR 0007](../../../docs/adr/0007_dual_domain_governance.md)
- [ADR 0008](../../../docs/adr/0008_server_rendered_python_first_ui.md)
- [Ingestion Phase 1 Contracts](../../../docs/contracts/ingestion_phase_1_contracts.md)
