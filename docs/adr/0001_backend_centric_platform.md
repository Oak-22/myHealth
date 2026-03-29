# ADR 0001: Adopt A Backend-Centric Platform Architecture

## Status

Accepted

## Context

`myHealth` integrates heterogeneous health data sources, ingestion
workflows, privacy boundaries, retrieval, analytics, and inference.
These concerns require durable state transitions, invariant
enforcement, provenance tracking, and controlled access to sensitive
data.

A frontend-centric architecture would push too much operational
responsibility into the UI layer and make privacy, validation, and
workflow control harder to reason about.

## Decision

Adopt a backend-centric architecture in which:

- FastAPI and backend services own system behavior
- the frontend acts as a thin delivery layer
- ingestion, validation, retrieval, and inference orchestration are
  backend responsibilities
- authoritative application state lives in backend-managed storage

## Consequences

### Positive

- privacy and access control remain centralized
- ingestion and workflow behavior can be made durable and auditable
- analytical and inference features can evolve without pushing business
  logic into the UI
- system boundaries read clearly as production-oriented backend design

### Negative

- backend complexity increases earlier
- more service and storage design work is required up front
- frontend iteration is constrained by backend contract design

## Evidence

- [system_architecture.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_architecture.md)
- [system_spec.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_spec.md)
- [myhealth-context.md](/Users/julianbuccat/Projects/Dev/myHealth/.github/instructions/repo/myhealth-context.md)
