---
description: "myHealth project context for agents working in this repository"
---

# myHealth Context

`myHealth` is a backend-centric personal health data and inference
platform.

The repository is focused on:

- ingestion of heterogeneous health data
- normalization and validation of records
- retrieval-augmented reasoning over longitudinal health context
- durable backend workflows and storage boundaries

## Architectural Direction

- Backend logic is authoritative; the frontend is a thin delivery layer
- FastAPI is the primary application/service boundary
- The system separates operational truth, workflow state, retrieval
  context, and analytics across different storage layers
- Multimodal and LLM reasoning are integrated into backend workflows,
  not delegated to the UI

## Engineering Priorities

- security and privacy of sensitive health data
- durable data models, service contracts and invariant enforcement
- clear ingestion and transformation boundaries
- observability, auditability, and operational correctness

## Stack Direction

- Thin frontend or delivery layer for user interaction
- FastAPI templating, HTMX, HTML/CSS, and minimal JavaScript for
  delivery-layer experiences
- Python-first backend built around FastAPI services
- PostgreSQL as the primary transactional system of record
- DynamoDB for key-addressable workflow state
- BigQuery for analytics
- Bedrock-backed inference routed through backend-managed services

## Source Of Truth

For deeper system details, use
[system_architecture.md](docs/architecture/system_architecture.md).
