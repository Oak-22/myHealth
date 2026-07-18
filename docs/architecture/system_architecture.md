# myHealth: Architecture

## Overview
The myHealth platform is a **personal health data and inference system** designed to ingest heterogeneous health data sources and enable retrieval‑augmented reasoning over longitudinal health records. The system unifies wearable data, laboratory exports, clinical documents, genomic datasets, and external health APIs into a normalized backend platform capable of analytics, semantic retrieval, and LLM‑assisted interpretation.

Current repository mode: under ADR 0010, this repository is a harness
evaluation target. The architecture below records product intent and
future implementation direction; it is not evidence that product source
code is currently present.

Rather than functioning as a traditional application where most logic lives in the UI, myHealth is architected as a **backend‑centric, event-driven health data platform**. The frontend acts primarily as a thin delivery layer while backend services handle ingestion pipelines, data normalization, inference orchestration, and analytical processing.

Key architectural priorities include:
- **Secure handling of sensitive health data**, including PHI/PII segregation across storage, retrieval, and inference workflows.
- **Composable services** enabling independent scaling of ingestion, inference, and analytics.
- **Service isolation by workload**, especially between user-facing gateway behavior and heavy biometric/document parsing.
- **Dual-domain governance**, separating restrained clinical workflows from more autonomous preclinical molecular and genomic workflows.
- **Telemetry analytics as a first-class workload**, preserving
  longitudinal behavioral, sleep, recovery, CPAP, and performance
  signals as canonical source facts before deriving trends or
  predictions.
- **Cloud‑native infrastructure** designed to support heterogeneous healthcare data pipelines and ML‑enabled insights.

## Engineering Principles

- **Data modeling and invariants** — schemas, normalization, constraint enforcement, and long‑lived correctness of stored data across ingestion, operational storage, and analytical models.
- **Data engineering pipelines** — reliable ingestion, schema evolution handling, parsing of heterogeneous formats (JSON/XML/CSV/PDF), and transformation workflows that move raw data → validated → analytics-ready datasets.
- **Databases and storage systems** — deliberate use of relational databases, operational key‑value stores, object storage, and analytical data warehouses, each chosen based on workload and access patterns.
- **In‑application inference orchestration** — integration of LLM and multimodal inference within backend workflows, enabling retrieval‑augmented reasoning over user health data without custom model training.
- **Security and data governance** — authentication, prevention of data leakage, injection protection, trust‑zone boundaries, and careful handling of sensitive health data.
- **Operational thinking** — structured logs, metrics, traces, lineage awareness, and post‑mortem analysis as first‑class parts of system design.
- **API robustness** — cross‑system, backward‑compatible service contracts, versioning strategies, and predictable integration boundaries.
- **State management over time and failure modes** — systems designed to survive restarts, partial failures, retries, race conditions, concurrency, and complex request dynamics.
- **Performance at scale (simulated)** — attention to algorithmic complexity, I/O bottlenecks, batching, caching layers, back‑pressure, and workload isolation across operational and analytical systems.

## Data Sources

The application is designed to ingest and reason over heterogeneous healthcare-related data originating from several realistic consumer and clinical data sources.

Core ingestion formats include XML, JSON, CSV, and PDF, with Parquet used downstream for analytics-oriented storage and transformation efficiency.

### Wearable and Personal Health Applications

These systems generate local device exports containing longitudinal biometric measurements collected directly from wearables and sensors.

**Source examples**
- Apple Health export (primary example for this project)

**Data formats demonstrated**
- XML (Apple Health "Export All Health Data" archive)

### Personal Telemetry And Recovery Tracking

These inputs capture longitudinal behavioral and subjective signals that
explain why health and cognitive-performance outcomes vary over time.

Unlike dashboard-only analytics, telemetry contributes new source facts
to the platform. Raw telemetry entries are operational records with
provenance, timestamps, and sensitivity classification. Recovery scores,
correlations, predictions, and trend summaries are downstream analytical
derivatives.

**Source examples**
- daily behavior logs
- sleep and recovery questionnaires
- CPAP / OSCAR exports
- workout summaries
- subjective cognitive-performance ratings

**Data formats demonstrated**
- server-rendered HTML forms
- CSV exports
- manual entries
- future API or file imports

**Metric examples**
- workout type, duration, and intensity
- late meal, alcohol, caffeine, stressor, and congestion indicators
- CPAP usage, AHI, leak, pressure, and mask-removal events
- sleep duration, deep sleep, REM, resting heart rate, HRV, respiratory
  rate, and wrist temperature
- restedness, mental clarity, energy, focus, productivity, and
  motivation ratings

### EHR APIs and Connected Services

These services expose network APIs that allow backend systems to programmatically retrieve historical health or lifestyle data without relying on manual file exports.

**Source examples**
- Electronic Health Record APIs (FHIR‑compatible REST APIs exposed by hospital systems)
- Pharmacy or medication management APIs
- Insurance or claims data APIs
- Nutrition or lifestyle tracking APIs

**Data formats demonstrated**
- JSON (API responses retrieved via backend ingestion services)

### Laboratory Data Exports

Laboratory portals frequently export structured tabular datasets containing diagnostic measurements and longitudinal biomarker values.

**Source examples**
- Laboratory portals exporting test results
- Synthetic clinical datasets generated by Synthea

**Data formats demonstrated**
- CSV (tabular lab values and longitudinal clinical metrics)

### Genomic Variant Datasets

Genomic variant datasets are used to demonstrate ingestion and annotation of bioinformatics-style data commonly used in precision medicine workflows.

**Source examples**
- ClinVar public variant archive
- Synthetic genomic datasets generated by Synthea

**Data formats demonstrated**
- CSV (ClinVar tabular exports)
- VCF (Variant Call Format)

These datasets allow the platform to demonstrate variant annotation workflows, conflicting clinical interpretations, and confidence scoring associated with genetic variants.

### Clinical Documents and Reports

Clinical encounters and diagnostic reports are frequently delivered as document artifacts that may contain either machine-readable text or scanned images.

**Source examples**
- Clinical visit summaries
- Radiology reports

**Processing characteristics**
- PDF documents containing selectable text
- Scanned documents or image-based PDFs requiring **OCR extraction**

These documents are ingested and parsed so that textual content can be indexed and reasoned over by the inference layer.

### Imaging Metadata and Interpretations

Medical imaging workflows often include **structured metadata and clinician-written interpretations** associated with imaging studies rather than the raw image files themselves.

**Source examples**
- Radiology interpretation summaries
- Imaging study metadata accompanying diagnostic reports

**Processing characteristics**
- Semi-structured textual interpretations
- Document-embedded metadata fields (study type, modality, timestamps)

In this case the system primarily reasons over **textual interpretations and metadata**, while multimodal models may optionally analyze embedded images when present.

These heterogeneous sources intentionally expose the system to multiple data formats (XML, JSON, CSV, PDF, Parquet, etc.) to demonstrate ingestion, normalization, and reasoning across structured and unstructured healthcare data.

Multimodal reasoning over these documents (text and images) is handled using off‑the‑shelf vision-capable LLMs rather than custom model training, reducing system complexity, regulatory exposure, and long-term maintenance.

## Domain Governance Model

`myHealth` is intentionally split into two governance domains.

### Clinical Domain

The clinical domain includes patient-facing and PHI-adjacent workflows:
wearable health records, lab reports, EHR-style data, clinical
documents, imaging interpretations, chat, retrieval, and health insight
surfaces.

This domain is restrained by default:

- strict PHI/PII minimization
- pseudonymization before inference
- provenance-aware retrieval
- bounded product LLM behavior
- audit-friendly workflow state
- conservative patient-facing outputs

### Preclinical Molecular Domain

The preclinical molecular domain includes non-PHI, synthetic, public, or
pseudonymized genomic and molecular workloads: VCF parsing,
ClinVar-style annotation, coordinate mappings, molecular matrices, and
research-style analytical pipelines.

This domain may be more autonomous:

- heavier worker dependencies and memory profiles
- high-throughput batch processing
- exploratory annotation and scoring workflows
- analytical/HPC-style output generation
- less coupling to patient-facing clinical UI behavior

The molecular domain must not silently cross into patient-facing
clinical guidance. Any derived molecular result that becomes clinical
context needs an explicit review, provenance, and pseudonymized linkage
boundary.

## Front-End

The frontend acts strictly as a **delivery layer**, not a system-of-record or application logic tier.

- **FastAPI route handlers + Jinja2** render the durable core application UI.
- **HTML forms and links** are the default interaction model for filters, drill-downs, ingestion status, and LLM query forms.
- **CSS** is the primary presentation technology.
- **HTMX** is allowed only as declarative progressive enhancement for server-rendered partial page updates.
- **No authored custom JavaScript or TypeScript** unless a future ADR documents a specific need.
- **No React / Next.js / Node.js frontend runtime / SPA architecture** — the frontend remains intentionally thin and backend-owned.
- **Streamlit (Python)** is reserved for internal experiments, research cockpit workflows, and analytical prototypes; it is not the durable patient/provider product shell.
- **All authoritative logic remains in backend services and databases.**

## Back-End And Service Boundaries

The backend is the **core application layer** of myHealth and contains the majority of system logic. It is responsible for enforcing application invariants, orchestrating data ingestion, coordinating inference workflows, and serving as the system-of-record boundary for all application state.

The system is intentionally split around workload boundaries rather than around frontend pages. The first service boundaries are:

- **Health Gateway Service**: user-facing FastAPI service responsible for authentication, server-rendered Jinja2 views, optional HTMX fragments, upload initiation, chat loops, retrieval requests, and ingestion status views.
- **Clinical Ingestion Worker**: private containerized worker responsible for Apple Health XML parsing, clinical document parsing, PDF/OCR extraction, source validation, and normalized ingestion output. It has no public endpoints and does not serve user web requests.
- **Telemetry Analytics Worker**: private or backend-managed worker responsible for normalizing daily telemetry entries, CPAP/sleep/recovery metrics, longitudinal feature generation, and dashboard/read-model refreshes.
- **Genomic Annotation Worker**: private containerized worker responsible for VCF parsing, ClinVar-style datasets, molecular matrix parsing, coordinate mappings, and variant annotation. It has no public endpoints and can carry heavier bioinformatics dependencies than the gateway.

The gateway should return fast responses and delegate long-running work through durable events. Parsing, OCR, telemetry feature generation, genomic annotation, indexing, analytics projection, and audit workflows run asynchronously.

### Application Services

- **FastAPI (Python)** provides REST endpoints, gateway behavior, and service APIs where synchronous service interfaces are required.
- **SQS or equivalent message broker** decouples user-facing requests from ingestion, parsing, indexing, and analytical projection workflows.
- **AWS Lambda** handles serverless edge ingest tasks such as S3 upload triggers, lightweight object validation, and event publication.
- **Authorization and access control** are enforced within backend services rather than delegated to the frontend.
- **Input validation and invariant enforcement** occur at API, service, and database boundaries.
- **Backend-controlled state transitions** ensure ingestion events, user actions, and inference workflows remain durable and auditable.

### Ingestion and Processing Responsibilities

Backend services convert heterogeneous healthcare data into validated, queryable, and analytics-ready representations.

- **Wearable ingestion pipeline** parses exported Apple Health XML in the Clinical Ingestion Worker and normalizes it into relational schemas.
- **Telemetry pipeline** stores user-entered behavior, CPAP, sleep,
  recovery, and cognitive-performance signals as canonical operational
  facts before deriving analytical features or dashboard projections.
- **Document ingestion pipeline** registers uploaded PDFs and clinical documents, tracks provenance, and coordinates parsing / extraction workflows through asynchronous events.
- **Genomic variant ingestion pipeline** parses ClinVar or synthetic genomic datasets (CSV/VCF) and stores variant annotations and provenance metadata for downstream interpretation.
- **Background processing** manages queued ingestion, retries, dead-letter handling, partial failures, and asynchronous workflow coordination.
- **Transformation boundaries** separate raw intake data from validated operational data and downstream analytical models.

### Inference and Retrieval Responsibilities

- **Inference orchestration** routes application requests through retrieval, prompt construction, Bedrock API calls, and response shaping.
- **Retrieval integration** combines structured health data, document-derived context, and analytical outputs to support context-aware responses.
- **Multimodal processing support** allows backend workflows to reason over both textual and document-derived image content.
- **Model access control and auditability** are maintained by routing all inference calls through backend-managed services.
- **Clinical inference restraint** ensures product LLMs only receive approved, pseudonymized, provenance-aware clinical context.
- **Preclinical analytical autonomy** allows molecular and genomic workers to perform richer autonomous computation over public, synthetic, or pseudonymized datasets without becoming patient-facing medical guidance by default.

### Polyglot Persistence Strategy

Different classes of data require different storage models. myHealth intentionally separates **transactional truth, operational workflow state, semantic retrieval context, and analytical workloads** across specialized systems.

- **PostgreSQL (Transactional System of Record)**  
  Primary relational database responsible for transactional correctness and long‑lived application state. It serves as the authoritative source of truth for operational data while also storing relational metadata used by downstream processing and retrieval layers.
  - user accounts
  - health record metadata
  - telemetry source facts and daily recovery entries
  - permissions and authorization mappings
  - ingestion manifests
  - document metadata and provenance tracking
  - audit‑sensitive application data

  PostgreSQL enforces strong invariants through schema constraints, normalization, indexes, and ACID transactions, ensuring durable and auditable system state.

- **PostgreSQL + pgvector (Semantic Retrieval Layer)**  
  Implemented as a PostgreSQL extension that enables vector similarity search for document-derived chunks and embeddings while remaining co-located with relational metadata.
  - extracted text chunks from PDFs and clinical documents
  - embeddings used for semantic retrieval
  - metadata filters combined with vector search (e.g., user, document type, time range)

  This supports retrieval-augmented inference while keeping semantic context tightly integrated with application-level access controls and relational provenance.

- **DynamoDB (Operational Key–Value Store)**  
  Used for high-throughput, key-addressable operational state such as:
  - ingestion job checkpoints
  - idempotency keys for ingestion APIs
  - cached idempotent responses where appropriate
  - async task and workflow state
  - chatbot session references
  - rate limiting counters

  This isolates ephemeral workflow coordination from relational application data.

- **Redis (Read-Optimized Cache / Projection Store)**  
  Used for fast query paths where the frontend needs low-latency,
  repeatedly accessed state that does not need to hit canonical
  PostgreSQL tables directly.
  - dashboard-ready trend snapshots
  - ingestion status projections
  - live UI refresh state
  - short-lived retrieval/session cache

  Redis supports CQRS-style separation between command writes and read
  models while PostgreSQL remains the source of truth.

- **Google BigQuery (Analytical Warehouse)**  
  A downstream analytical layer used for:
  - long‑term health trends
  - derived health metrics
  - dashboard-ready models
  - cohort and population analysis

  Analytical workloads are isolated from the operational application database.

- **dbt + SQL validation** ensures transformation correctness, data quality enforcement, and analytical model generation.

## AI / LLM Layer

- **AWS Bedrock inference APIs** provide access to multimodal foundation models used for in-application reasoning over health data and documents.
- **Retrieval layer** combines structured health data, document embeddings, and analytical outputs to support context-aware responses.
- Future: Agent orchestration (LangGraph or equivalent)

## Cloud & Data Flow


### Wearable Data → Health Platform

```
[Apple Health App]
      ↓ Export All Health Data (.zip)
[Health Gateway Service]
      ↓ Create Manifest + Pre-signed Upload URL
[S3 Raw Object Storage]
      ↓ S3 Event
[Lambda Edge Ingest Validator]
      ↓ Publish BiometricFileUploaded
[SQS Ingestion Queue]
      ↓ Consume Task
[Clinical Ingestion Worker]
      ↓ Parse XML + Normalize + Validate
[PostgreSQL (System of Record)]
      ↓
[DynamoDB (Idempotency + Workflow State)]
      ↓
[Redis Read Projection]
      ↓
[dbt Transformations → BigQuery (Analytical Data Warehouse)]
      ↓
[Health Insights + Dashboards]
```

### Personal Telemetry → Recovery Analytics

```
[Daily Behavior / CPAP / Recovery / Cognitive Inputs]
      ↓ Server-rendered Forms or File/API Imports
[Health Gateway Service]
      ↓ Validate + Persist Source Facts
[PostgreSQL Telemetry Records]
      ↓ Publish TelemetryUpdated
[Telemetry Analytics Worker]
      ↓ Feature Generation + Trend Models
[Redis Read Projection / BigQuery Analytical Models]
      ↓
[Recovery Dashboard + Correlation / Prediction Views]
```

### External Documents / Laboratory Data → Multimodal AI Pipeline

```
[PDFs / Lab Reports / External Clinical Documents]
      ↓ Pre-signed Upload
[S3 Raw Document Storage]
      ↓ S3 Event + Lambda Validation
[SQS Document Ingestion Queue]
      ↓
[Clinical Ingestion Worker]
      ↓ Parsing / OCR / Table Extraction
[PostgreSQL Document Index + Provenance]
      ↓
[Structured Lab Data → PostgreSQL]
      ↓
[Embeddings / Retrieval Index]
      ↓
[LLM / Multimodal Inference]
      ↓
[Summaries / Extracted Insights Returned to App]
```

Genomic variant datasets (e.g., ClinVar) follow a similar ingestion path but are processed through a specialized genomic ingestion service that parses variant files, stores variant annotations in PostgreSQL, and enables downstream interpretation or explanation through the inference layer.

### Genomic / Molecular Payload → Annotation Pipeline

```
[VCF / ClinVar CSV / Molecular Matrix]
      ↓ Pre-signed Upload
[S3 Raw Vault]
      ↓ S3 Event + Lambda Validation
[SQS Genomic Ingestion Queue]
      ↓
[Genomic Annotation Worker]
      ↓ Parse + Annotate + Normalize
[PostgreSQL Variant / Molecular Records]
      ↓
[BigQuery / Parquet Analytical Models]
      ↓
[Retrieval + Inference Context]
```

### User Query → Insight

```
[User Prompt]
      ↓
[Server-rendered HTML UI]
      ↓
[Health Gateway Service]
      ↓
[Vector Retrieval / ML Inference]
      ↓
[Response Returned to UI]
```

## Security & Compliance

- **Private networking and restricted service boundaries** for sensitive workloads.
- **Strict authentication and authorization layers**.
- **Data minimization and pseudonymization** prior to embedding or ML usage.
- **Audit-friendly storage models** enabling traceability of sensitive operations.

Future privacy-control intent is defined separately so it is not
mistaken for current implementation:

- [Consent lifecycle](consent_lifecycle_intent.md)
- [Retention and deletion](retention_deletion_intent.md)
- [NLP de-identification](nlp_deidentification_intent.md)
- [Hybrid inference routing](hybrid_inference_routing_intent.md)
- [Abstention and answerability](abstention_answerability_intent.md)
- [Patient edge privacy](patient_edge_privacy_intent.md)
- [Confidential clinical inference](confidential_clinical_inference_intent.md)
- [Research alignment and operator responsibility](../research/README.md)

## Observability and Governance

Operational maturity is treated as a core engineering requirement.

- **Structured logging** across services
- **Metrics collection** for service health and workload performance
- **Tracing** for request lifecycle debugging
- **Post‑mortem driven improvements** for reliability

## Deployment & Orchestration

- **Docker** for service containerization
- **Cloud container runtime (e.g., Fargate)** for MVP deployments
- **Kubernetes (future phase)** for larger-scale orchestration
