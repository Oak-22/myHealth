# Technology Stack

## Purpose

This document records the current technology posture for `myHealth`.
Under ADR 0010, the repository is a harness evaluation target rather
than an active product implementation. Product language and framework
choices are deferred until the agentic harness/control-plane and
AgentOps token-economics foundations are ready.

## Active Technology Surface

- GitHub repository instructions, agents, prompts, skills, and hook
  configuration
- shell hook scripts under `scripts/hooks/`
- architecture, contract, ADR, product, data, and notes documentation
- Mermaid diagrams embedded in markdown

## Deferred Product Stack

Historical ADRs and architecture docs still describe a backend-centric
health platform using AWS-managed infrastructure, event-driven
ingestion, retrieval, and privacy boundaries. Those remain product
intent, not active implementation commitments.

The following categories are deferred until product development resumes:

- application programming language
- web framework
- UI rendering framework
- test framework
- package manager and runtime
- deployment packaging

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
- retrieval and prompt orchestration inside future backend-managed
  services
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
