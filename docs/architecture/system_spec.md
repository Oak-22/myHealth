# System Specification

## Purpose

This document translates the high-level architecture into concrete
backend and data-platform behavior.

## System Boundaries

`myHealth` is composed of five major technical layers:

- API and intake boundary
- ingestion and normalization
- operational storage and workflow state
- retrieval and analytical context generation
- inference orchestration and response shaping

The backend is the system-of-record boundary for application state.

## Service Responsibilities

### API And Intake Boundary

The API layer is responsible for:

- authenticated request intake
- validation of request shape and file metadata
- creation of ingestion manifests and workflow records
- controlled access to retrieval and inference workflows

### Ingestion And Normalization Layer

The ingestion layer is responsible for:

- parsing source-specific formats
- mapping raw source data into canonical models
- recording provenance and source metadata
- rejecting or quarantining invalid data
- supporting retry-safe processing

### Operational Storage And Workflow Layer

The operational workflow layer is responsible for:

- persistence of workflow state and ingestion manifests
- background execution of asynchronous ingestion tasks
- checkpointing long-running jobs
- idempotent retry handling
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

## Canonical Data Flow

The canonical processing flow is:

1. source intake is registered
2. raw payload metadata is captured
3. parsing and validation are performed
4. canonical operational records are written
5. downstream analytical and retrieval artifacts are generated
6. inference requests retrieve bounded context from approved stores

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

## Persistence Responsibilities

### PostgreSQL

PostgreSQL owns:

- users and access mappings
- source manifests
- normalized health records
- document metadata
- provenance and audit-sensitive relational state
- semantic retrieval metadata colocated with relational controls

### DynamoDB

DynamoDB owns:

- workflow checkpoints
- idempotency records
- async task state
- short-lived operational coordination data

### BigQuery

BigQuery owns:

- derived analytical models
- trend and cohort style datasets
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
