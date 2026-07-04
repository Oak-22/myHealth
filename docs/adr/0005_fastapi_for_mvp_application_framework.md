# ADR 0005: Use FastAPI As The Primary Python Service Framework

## Status

Accepted, amended by ADR 0006

## Context

`myHealth` is optimized around backend services, ingestion pipelines,
validation boundaries, retrieval, and inference orchestration. The
project also aims to signal strong Python backend and data-engineering
capability while giving the developer direct exposure to production
software engineering patterns.

Two broad application approaches were considered:

- a FastAPI-first backend
- a split architecture with FastAPI for ingestion and ML services plus
  Django or Django REST Framework for application and portal surfaces

While Django would provide strong batteries-included support for admin
workflows, relational CRUD, and portal development, adopting both
frameworks at MVP stage would increase:

- implementation complexity
- deployment and environment complexity
- auth and boundary complexity
- cognitive load for a solo developer
- failure surface for agent-assisted implementation

## Decision

Use FastAPI as the primary Python framework for user-facing and
service-facing application surfaces.

ADR 0008 defines the user-facing UI stack as FastAPI route handlers,
Jinja2 templates, HTML forms/links, CSS, and optional HTMX progressive
enhancement. Custom JavaScript/TypeScript and SPA frameworks are out of
scope unless a future ADR changes that decision.

The system should use clear boundaries for:

- API routes
- ingestion workflows
- domain services
- repositories and persistence logic
- retrieval and inference orchestration

ADR 0006 changes the deployment target from a single FastAPI-centered
application to an event-driven, service-isolated architecture. FastAPI
remains the primary framework for service APIs and gateway behavior.

Django is deferred unless a concrete product need emerges for:

- a richer admin surface
- complex internal portal workflows
- server-rendered back office functionality that materially exceeds what
  a thin FastAPI-based surface can support

## Consequences

### Positive

- keeps the Python application model coherent across services
- aligns with the backend/service orientation already expressed in the
  repo
- supports async-friendly APIs and typed request/response contracts
- reduces framework sprawl while still allowing service isolation
- improves the chance of successful agent-assisted implementation

### Negative

- Django admin and batteries-included portal ergonomics are deferred
- some internal dashboard or CRUD workflows may require more custom work
- distributed deployment still introduces operational complexity through
  queues, workers, contracts, and observability

## Follow-Up Guidance

FastAPI services should be structured with consistent internal layering.
Internal modules should be separated by responsibility so each service
can evolve without becoming tangled.

Suggested internal boundaries:

- `api/`
- `services/`
- `adapters/`
- `repositories/`
- `workflows/`
- `models/`

ADR 0006 defines the first concrete split: a Health Gateway Service,
private Clinical Ingestion Worker, and private Genomic Annotation Worker
connected through object storage and an asynchronous message broker.

## Evidence

- [system_architecture.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_architecture.md)
- [system_spec.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_spec.md)
- [0001_backend_centric_platform.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/adr/0001_backend_centric_platform.md)
- [0008_server_rendered_python_first_ui.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/adr/0008_server_rendered_python_first_ui.md)
