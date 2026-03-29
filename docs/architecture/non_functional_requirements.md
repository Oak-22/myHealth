# Non-Functional Requirements

## Purpose

This document captures the production-oriented qualities the platform
is designed to preserve independent of any single feature.

## Security And Privacy

- sensitive health data must remain inside approved trust boundaries
- prompts and logs must avoid raw identifier leakage
- access control must be enforced by backend services
- data movement between storage systems must preserve sensitivity
  classification and provenance
- inference inputs must be bounded to approved context only

## Reliability

- ingestion operations must be retry-safe
- partial failures must be visible and recoverable
- long-running tasks must checkpoint progress
- duplicate inputs must not create uncontrolled duplicate writes
- downstream analytics must tolerate late-arriving data

## Data Integrity

- canonical health records must preserve source provenance
- units, timestamps, and source identifiers must be normalized
  deterministically
- validation failures must be surfaced without silently dropping data
- operational truth and derived analytics must remain distinct

## Auditability

- workflow state transitions must be traceable
- outputs should be explainable back to source records or documents
- schema and boundary decisions should be documented
- inference behavior should be reviewable through bounded inputs and
  observable execution paths

## Performance

- ingestion should support batching where safe
- large document processing should be asynchronous
- analytical queries must not compete with operational writes on the
  same path
- retrieval operations should support metadata filtering in addition to
  vector similarity

## Maintainability

- source-specific parsing logic should remain isolated by boundary
- canonical schemas should not encode one-off source quirks directly
- integration constraints should be handled at adapters, not in core
  logic
- important architectural decisions should be documented with ADRs

## Operability

- failure states must be observable without code inspection
- operators should be able to determine what source failed, where it
  failed, and whether retry is safe
- runbooks should exist for common ingestion and data quality incidents

## Compliance Posture

This project models a production-oriented healthcare platform and is
therefore designed around:

- least-privilege access assumptions
- PHI minimization
- provenance preservation
- audit-oriented system boundaries

It is not a claim of certified regulatory compliance, but it should
look and behave like a system designed with those constraints in mind.
