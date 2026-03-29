# ADR 0002: Use PostgreSQL With pgvector For Retrieval Metadata And Embeddings

## Status

Accepted

## Context

The platform needs semantic retrieval over document-derived chunks while
also preserving strong linkage to relational metadata, provenance, user
boundaries, and access controls.

A separate vector database could work, but it would introduce more
infrastructure, more synchronization burden, and more opportunities for
retrieval state to drift from the operational source of truth.

## Decision

Use PostgreSQL as the primary transactional system of record and extend
it with `pgvector` for embeddings and similarity search.

This allows semantic retrieval to remain colocated with:

- document metadata
- provenance
- access-control filters
- time and document-type constraints

## Consequences

### Positive

- retrieval remains tightly coupled to relational provenance
- access filtering can be applied in the same storage boundary
- operational complexity is lower than introducing a dedicated vector
  store
- the architecture signals deliberate backend and data modeling choices

### Negative

- vector workloads still share a platform with transactional storage
- specialized vector-database features may be less mature or less broad
- future scale characteristics may require revisiting the choice

## Evidence

- [system_architecture.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_architecture.md)
- [non_functional_requirements.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/non_functional_requirements.md)
- [data_model.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/data/data_model.md)
