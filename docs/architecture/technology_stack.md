# Technology Stack

## Purpose

This document lists the major technologies used across `myHealth` so
the implementation surface is easy to scan without overloading the
architecture and specification documents.

## Frontend And Delivery Layer

- FastAPI route handlers for core application views
- Jinja2 server-side templates
- HTML forms and links as the default interaction model
- CSS for presentation
- HTMX only as declarative progressive enhancement for server-rendered
  partial page updates
- no authored custom JavaScript or TypeScript
- no React, Next.js, Node.js frontend runtime, or SPA architecture
- Streamlit for internal experiments, research cockpit workflows, and
  analytical prototypes only

## Backend Application Layer

- Python
- FastAPI for the Health Gateway Service and service-facing APIs

## Service Boundaries

- Health Gateway Service for authentication, server-rendered
  FastAPI/Jinja2 views, optional HTMX fragments, upload initiation, chat
  loops, retrieval requests, and ingestion status views
- Clinical Ingestion Worker as a private containerized worker for Apple
  Health XML parsing, PDF/OCR extraction, source validation, and
  normalized clinical ingestion output
- Telemetry Analytics Worker for sleep, recovery, CPAP, behavior, and
  cognitive-performance feature generation and read-model refreshes
- Genomic Annotation Worker as a private containerized worker for VCF,
  ClinVar-style datasets, molecular matrices, coordinate mappings, and
  variant annotation workflows

## Governance Domains

- Clinical domain for PHI-adjacent, patient-facing, restrained
  workflows over wearable, lab, document, EHR-style, retrieval, and chat
  contexts
- Preclinical molecular domain for more autonomous, high-compute
  workflows over public, synthetic, non-PHI, or pseudonymized genomic
  and molecular payloads

## Ingestion And Workflow Layer

- Cron-based scheduling
- Airflow
- Amazon S3 event notifications for object-upload triggers
- AWS Lambda for serverless edge ingest validation and event publishing
- Amazon SQS for asynchronous ingestion, parsing, indexing, and
  projection queues
- SQS dead-letter queues for failed workflow tasks

## Operational Persistence

- PostgreSQL as the transactional system of record
- pgvector for retrieval metadata and embeddings
- DynamoDB for workflow checkpoints, idempotency records, and ephemeral
  coordination state
- Redis for read-optimized dashboard projections, ingestion status
  projections, and short-lived cache state

## Database Tooling

- pgAdmin for PostgreSQL administration, schema inspection, and query
  workflows
- Oracle SQL Data Modeler for relational schema design and ERD modeling
- `psql` for direct SQL access, validation, and operational inspection

## Analytical Stack

- BigQuery for downstream analytical models
- dbt for transformations and data quality checks
- Parquet for analytics-oriented intermediate datasets
- telemetry feature models for recovery, sleep, CPAP, behavior, and
  cognitive-performance analysis

## Document And Object Storage

- Amazon S3 for raw document and object storage
- S3 pre-signed URLs for direct client uploads that bypass gateway
  server file handling

## Inference And Retrieval

- AWS Bedrock for embedding and generation models
- PostgreSQL with pgvector for vector storage and similarity search
- Python retrieval and prompt orchestration inside the Health Gateway
  Service and supporting backend services
- document chunking and provenance-aware context assembly in
  application-managed ingestion and retrieval workflows

## Security, Privacy, And Cloud Boundary

- AWS VPC
- IAM 
- interface endpoints for private Bedrock access
- gateway endpoints for private S3 access

## Observability And Governance

- Prometheus
- Grafana
- CloudTrail
- Audit Manager


## Compute And Deployment

- AWS Fargate for serverless container compute
- private worker containers for parsing, OCR, molecular, and genomic
  workloads
- AWS Lambda for lightweight event-triggered compute

## Modeling And Documentation Artifacts

- product and architecture docs
- system specification
- ADRs
- data model artifacts, including ERDs and companion design notes
- data dictionary docs
