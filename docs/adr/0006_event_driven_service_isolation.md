# ADR 0006: Adopt Event-Driven Service Isolation For Learning Architecture

## Status

Accepted

## Context

`myHealth` is both a personal health data platform and a deliberate
software engineering learning environment. A minimal MVP could remain a
single modular backend for longer, but that would reduce hands-on
exposure to distributed systems, asynchronous processing, service
contracts, idempotency, queueing, and operational observability.

The project already contains workload boundaries that naturally justify
service isolation:

- user-facing authentication, views, chat, and retrieval requests
- heavy Apple Health XML parsing
- PDF parsing and OCR extraction
- audit logging and workflow state transitions
- analytical read-model generation

These workloads have different latency, scaling, reliability, and
security characteristics.

## Decision

Adopt an event-driven, service-isolated architecture earlier than a
minimal MVP would require.

The first service split is:

- **Health Gateway Service**: FastAPI service responsible for
  authentication, server-rendered Jinja2 views, optional HTMX
  fragments, upload initiation, user-facing API routes, chat loops,
  retrieval requests, and response shaping.
- **Clinical Ingestion Worker**: private containerized worker
  responsible for Apple Health XML parsing, clinical document parsing,
  PDF/OCR extraction, source validation, and normalized ingestion output.
  It has no public endpoints and should not serve user web requests.
- **Genomic Annotation Worker**: private containerized worker
  responsible for VCF parsing, ClinVar-style tabular datasets,
  coordinate mappings, molecular matrix parsing, and variant annotation
  workflows. It has an intentionally heavier memory and dependency
  profile than the gateway.

The upload and ingestion flow should use asynchronous event decoupling:

1. The gateway creates an ingestion manifest and returns an S3
   pre-signed upload URL.
2. The client uploads the raw file directly to S3.
3. An S3-triggered Lambda validates basic object metadata and publishes
   a task event to SQS.
4. The appropriate private worker consumes the event, checks idempotency
   state, parses the payload, writes canonical records to PostgreSQL,
   updates workflow state in DynamoDB, and emits follow-up events for
   indexing, audit, analytics, or dashboard refresh.
5. The gateway returns ingestion status using workflow state instead of
   blocking on parsing.

## Consequences

### Positive

- exposes the project to real distributed systems concerns early
- prevents heavy parsing and OCR work from competing with user-facing
  web requests
- creates natural practice with S3 events, Lambda, SQS, background
  workers, retries, dead-letter queues, and idempotency
- makes service contracts, event schemas, and observability first-class
  design artifacts
- better reflects production health-data ingestion patterns

### Negative

- increases local development and deployment complexity
- requires queue and event-schema discipline earlier
- introduces eventual consistency between upload, parsing, indexing, and
  dashboard state
- increases the number of failure modes that must be tested
- can slow feature delivery if service boundaries are over-designed

## Implementation Guidance

Use service isolation where it creates learning value and matches a real
workload boundary. Avoid splitting every module into a separate service.

Initial service boundaries:

- `health-gateway-service`
- `clinical-ingestion-worker`
- `genomic-annotation-worker`
- shared schema/contracts package or documented event schemas

Initial event types:

- `BiometricFileUploaded`
- `LabReportReceived`
- `GenomicPayloadUploaded`
- `MolecularMatrixUploaded`
- `IngestionParsingStarted`
- `IngestionParsingFailed`
- `IngestionValidated`
- `HealthRecordsPersisted`
- `EmbeddingsRequested`
- `AnalyticsProjectionRequested`

Required operational patterns:

- idempotency keys stored in DynamoDB
- SQS dead-letter queues for failed tasks
- structured logs with manifest ID, user ID or pseudonymous subject ID,
  source type, event type, and workflow stage
- explicit workflow states visible to the gateway
- parser strategies for XML, CSV, FHIR JSON, PDF, OCR, and VCF
- storage and LLM facades so cloud SDK logic does not leak into domain
  services

## Relationship To Prior ADRs

This ADR amends ADR 0005. FastAPI remains the primary Python service
framework, but the architecture is no longer described as a single
FastAPI-centered backend.

This ADR preserves ADR 0001. The platform remains backend-centric: the
frontend is still a thin delivery layer, and authoritative state remains
inside backend-managed services and databases.

## Evidence

- [system_architecture.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_architecture.md)
- [system_spec.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_spec.md)
- [software_design_patterns.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/notes/software_design_patterns.md)
- [0008_server_rendered_python_first_ui.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/adr/0008_server_rendered_python_first_ui.md)
