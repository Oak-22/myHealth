# Technology Stack

## Purpose

This document lists the major technologies used across `myHealth` so
the implementation surface is easy to scan without overloading the
architecture and specification documents.

## Frontend And Delivery Layer

- HTML/CSS
- minimal JavaScript
- FastAPI templating
- HTMX
- Streamlit for rapid internal experiments and prototype flows

## Backend Application Layer

- Python
- FastAPI

## Ingestion And Workflow Layer

- Cron-based scheduling
- Airflow

## Operational Persistence

- PostgreSQL as the transactional system of record
- pgvector for retrieval metadata and embeddings
- DynamoDB for workflow checkpoints, idempotency records, and ephemeral
  coordination state

## Database Tooling

- pgAdmin for PostgreSQL administration, schema inspection, and query
  workflows
- Oracle SQL Data Modeler for relational schema design and ERD modeling
- `psql` for direct SQL access, validation, and operational inspection

## Analytical Stack

- BigQuery for downstream analytical models
- dbt for transformations and data quality checks
- Parquet for analytics-oriented intermediate datasets

## Document And Object Storage

- Amazon S3 for raw document and object storage

## Inference And Retrieval

- AWS Bedrock for embedding and generation models
- PostgreSQL with pgvector for vector storage and similarity search
- Python retrieval and prompt orchestration inside the FastAPI backend
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

## Modeling And Documentation Artifacts

- product and architecture docs
- system specification
- ADRs
- data model artifacts, including ERDs and companion design notes
- data dictionary docs
