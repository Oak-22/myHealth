# ADR 0003: Separate Operational, Workflow, And Analytical Storage By Workload

## Status

Accepted

## Context

The platform has materially different storage needs:

- transactional correctness for canonical health records
- key-addressable workflow coordination and idempotency state
- downstream analytical modeling and trend computation

A single storage system would simplify the topology but would also blur
workload boundaries and make it harder to preserve operational
correctness while supporting analytics and async coordination.

## Decision

Use polyglot persistence with:

- PostgreSQL for canonical operational truth
- DynamoDB for workflow coordination, checkpointing, and idempotency
- BigQuery for downstream analytics

## Consequences

### Positive

- each storage layer is aligned to its workload
- transactional correctness is insulated from analytical processing
- workflow state remains lightweight and operationally separate
- data-engineering concerns are explicit in the architecture

### Negative

- more cross-system lineage and synchronization work is required
- the system becomes operationally more complex
- data contracts between layers must be documented carefully

## Evidence

- [system_architecture.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_architecture.md)
- [system_spec.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_spec.md)
- [data_dictionary.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/data/data_dictionary.md)
