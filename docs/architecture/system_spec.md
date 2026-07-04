# System Specification

## Purpose

This document translates the high-level architecture into concrete
backend and data-platform behavior.

## System Boundaries

`myHealth` is composed of service boundaries and technical layers:

- Health Gateway Service
- serverless edge ingest boundary
- message broker and workflow queues
- Clinical Ingestion Worker
- Telemetry Analytics Worker
- Genomic Annotation Worker
- ingestion and normalization workers
- operational storage and workflow state
- retrieval and analytical context generation
- inference orchestration and response shaping

Backend-managed services are the system-of-record boundary for
application state.

## Domain Governance

The system separates two governance domains:

- **Clinical domain**: patient-facing or PHI-adjacent workflows,
  including wearables, lab reports, EHR-style records, clinical
  documents, retrieval, chat, and health insights. This domain is
  restrained, pseudonymized before inference, provenance-aware, and
  audit-friendly.
- **Preclinical molecular domain**: non-PHI, synthetic, public, or
  pseudonymized molecular/genomic workflows, including VCF parsing,
  ClinVar-style annotations, molecular matrices, coordinate mappings,
  and analytical/HPC-style processing. This domain may use more
  autonomous worker behavior and heavier compute profiles.

Cross-domain movement from preclinical output into patient-facing
clinical context requires explicit provenance, review, and
pseudonymized linkage rules.

- **Telemetry analytics lane**: longitudinal user-entered,
  device-derived, CPAP, sleep, recovery, and cognitive-performance
  signals. Raw telemetry entries are source facts; trends,
  correlations, feature vectors, and predictions are derived analytics.

## Service Responsibilities

### API And Intake Boundary

The Health Gateway Service is responsible for:

- authenticated request intake
- validation of request shape and file metadata
- creation of ingestion manifests and workflow records
- controlled access to retrieval and inference workflows
- creation of S3 pre-signed upload URLs
- returning fast acknowledgement responses for long-running ingestion
  work

### Serverless Edge Ingest Boundary

The serverless edge ingest boundary is responsible for:

- reacting to S3 object-created events
- validating basic object metadata and expected upload shape
- publishing ingestion task events to the message broker
- avoiding direct large-file uploads through the gateway service

### Ingestion And Normalization Layer

Private ingestion and annotation workers are responsible for:

- parsing source-specific formats
- mapping raw source data into canonical models
- recording provenance and source metadata
- rejecting or quarantining invalid data
- supporting retry-safe processing
- consuming queued ingestion tasks
- emitting downstream events for indexing, audit, analytics, and
  projection refreshes

### Telemetry Analytics Layer

The telemetry analytics layer is responsible for:

- validating daily behavior, CPAP, sleep, recovery, and subjective
  performance inputs
- preserving raw telemetry source facts with timestamps and provenance
- generating longitudinal features for recovery and performance
  analysis
- refreshing dashboard/read-model projections
- keeping derived correlations and predictions distinct from canonical
  telemetry records

### Operational Storage And Workflow Layer

The operational workflow layer is responsible for:

- persistence of workflow state and ingestion manifests
- background execution of asynchronous ingestion tasks
- checkpointing long-running jobs
- idempotent retry handling
- dead-letter handling for failed queue tasks
- surfacing workflow status to operators and dependent services

### Retrieval And Analytical Context Layer

The retrieval and analytical context layer is responsible for:

- selecting relevant structured and document-derived context
- generating retrieval-ready chunks, metadata, and embeddings
- producing downstream analytical context where needed
- preserving provenance between source records and retrieved context

### Inference Orchestration Layer

The inference orchestration layer is responsible for:

- constructing bounded prompts
- enforcing privacy and audit constraints
- shaping outputs for application consumption
- keeping clinical inference restrained to approved, pseudonymized,
  provenance-aware context
- preventing autonomous molecular analysis from becoming patient-facing
  clinical guidance without an explicit review boundary

## Canonical Data Flow

The canonical processing flow is:

1. source intake is registered
2. an S3 pre-signed upload URL is issued
3. raw payload metadata is captured after object upload
4. a serverless edge ingest event publishes a queued task
5. parsing and validation are performed asynchronously
6. canonical operational records are written
7. telemetry source facts are preserved when the payload represents
   daily recovery, behavior, CPAP, sleep, or performance inputs
8. workflow state and read projections are refreshed
9. downstream analytical and retrieval artifacts are generated
10. inference requests retrieve bounded context from approved stores

## Operational Data States

All intake should move through explicit state transitions:

- `registered`
- `received`
- `parsing`
- `validated`
- `failed_validation`
- `persisted`
- `indexed`
- `available_for_inference`

These states allow restart-safe processing and operator visibility.

## Ingestion Contracts

Each ingestion path should define:

- source type
- expected format and encoding
- schema/version assumptions
- required identifiers and timestamps
- validation rules
- idempotency key strategy
- event type and queue contract
- dead-letter behavior
- failure and quarantine behavior

## Data Quality Rules

Examples of platform-level data quality rules:

- timestamps must be timezone-aware or normalized deterministically
- biomarker values must preserve units and reference range metadata
- source lineage must be attached to normalized records
- duplicate source ingestion must not create uncontrolled record
  multiplication
- document parsing output must retain page-level provenance where
  feasible
- telemetry-derived features must remain traceable to raw daily inputs
  and source observations

## Persistence Responsibilities

### PostgreSQL

PostgreSQL owns:

- users and access mappings
- source manifests
- normalized health records
- raw telemetry source facts
- document metadata
- provenance and audit-sensitive relational state
- semantic retrieval metadata colocated with relational controls

### DynamoDB

DynamoDB owns:

- workflow checkpoints
- idempotency records
- async task state
- short-lived operational coordination data

### Redis

Redis owns:

- read-optimized dashboard projections
- ingestion status projections
- telemetry and recovery dashboard projections
- short-lived cache state
- live UI refresh state where eventual consistency is acceptable

### BigQuery

BigQuery owns:

- derived analytical models
- trend and cohort style datasets
- recovery, sleep, CPAP, behavior, and cognitive-performance feature
  models
- reporting-friendly tables separated from operational write paths

## Failure modes

The system must explicitly handle:

- malformed source files
- partial document extraction
- late-arriving or duplicated source payloads
- downstream warehouse lag
- retrieval/indexing drift from source-of-truth records
- inference-provider latency or throttling

## Observability Requirements

Each major workflow should emit:

- structured logs
- request or workflow identifiers
- ingestion manifest references
- source type and processing stage
- success/failure counts
- latency and retry metrics

## Change Management

Changes that affect canonical schemas, ingestion contracts, privacy
boundaries, or persistence responsibilities should be captured with an
ADR and reflected in the data docs.
