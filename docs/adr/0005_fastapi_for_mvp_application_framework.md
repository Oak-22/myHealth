# ADR 0005: Use FastAPI As The Primary Application Framework For MVP

## Status

Accepted

## Context

`myHealth` is currently optimized around backend services, ingestion
pipelines, validation boundaries, retrieval, and inference
orchestration. The project also aims to signal strong Python backend
and data-engineering capability without introducing unnecessary
framework complexity for a solo developer workflow.

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

Use FastAPI as the primary application framework for the MVP.

The initial system should remain a single FastAPI-centered backend with
clear internal boundaries for:

- API routes
- ingestion workflows
- domain services
- repositories and persistence logic
- retrieval and inference orchestration

Django is deferred unless a concrete product need emerges for:

- a richer admin surface
- complex internal portal workflows
- server-rendered back office functionality that materially exceeds what
  a thin FastAPI-based surface can support

## Consequences

### Positive

- keeps the MVP architecture simpler and more coherent
- aligns with the backend/service orientation already expressed in the
  repo
- supports async-friendly APIs and typed request/response contracts
- reduces framework sprawl for a solo developer
- improves the chance of successful agent-assisted implementation

### Negative

- Django admin and batteries-included portal ergonomics are deferred
- some internal dashboard or CRUD workflows may require more custom work
- a future second framework may still be introduced if the product
  surface expands

## Follow-Up Guidance

The FastAPI codebase should still be structured to allow future
extraction or layering. Internal modules should be separated by
responsibility so the system can evolve without a monolithic tangle.

Suggested internal boundaries:

- `api/`
- `services/`
- `adapters/`
- `repositories/`
- `workflows/`
- `models/`

## Evidence

- [system_architecture.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_architecture.md)
- [system_spec.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_spec.md)
- [0001_backend_centric_platform.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/adr/0001_backend_centric_platform.md)
