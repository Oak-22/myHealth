# Data Model

## Purpose

This document describes the intended relational and analytical data
model at a systems level. It complements formal modeling artifacts such
as Oracle SQL Data Modeler diagrams.

## Modeling Principles

- PostgreSQL is the canonical operational system of record
- source-specific payloads are normalized into durable domain entities
- provenance is first-class, not optional metadata
- analytical outputs are downstream derivatives, not transactional truth
- schema design should favor explicit invariants over convenience

## Core Entity Groups

### Identity And Access

Representative entities:

- `users`
- `accounts`
- `authorization_bindings`

These entities define who owns data and what backend-controlled access
rules apply to it.

### Ingestion Control Plane

Representative entities:

- `ingestion_manifests`
- `source_files`
- `source_systems`
- `workflow_events`

These entities capture intake state, source lineage, and processing
history.

### Clinical And Health Facts

Representative entities:

- `patients` or pseudonymized subject records
- `observations`
- `lab_results`
- `medications`
- `conditions`
- `encounters`

These entities capture normalized health facts derived from source
systems.

### Documents And Provenance

Representative entities:

- `documents`
- `document_pages`
- `document_chunks`
- `document_extractions`
- `document_embeddings`

These entities preserve the relationship between uploaded artifacts,
extracted text, chunking boundaries, and retrieval artifacts.

### Genomics

Representative entities:

- `genomic_variants`
- `variant_annotations`
- `interpretation_sources`

These entities support ingesting and reasoning over variant-level
information with explicit provenance.

### Analytics

Representative entities or downstream models:

- trend aggregates
- derived health metrics
- dashboard-serving summary tables
- cohort-ready analytical views

These live downstream from operational truth.

## Storage Layer Mapping

- PostgreSQL stores normalized operational entities and retrieval
  metadata
- DynamoDB stores ephemeral workflow coordination state
- BigQuery stores analytical derivatives

## Required Cross-Cutting Attributes

Across core entities, the model should preserve:

- ownership or access boundary
- source system identifier
- source event or document provenance
- ingestion manifest lineage
- timestamps for event time and ingestion time
- sensitivity classification where relevant

## Modeling Deliverables

The data model surface should eventually include:

- narrative model overview in this document
- formal ERD or SQL Data Modeler artifact
- data dictionary for important entities and columns
- ADRs for major modeling decisions
