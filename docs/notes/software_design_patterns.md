# Software Design Patterns Reference

## Purpose

This document is a learning and design reference for `myHealth`. It
captures major software engineering patterns at both the system level
and code level, then explains how each pattern does or does not apply to
this project.

The goal is not to claim that every advanced pattern should be used.
Good architecture is selective. For `myHealth`, the strongest signal is
showing that we understand the tradeoffs, choose patterns deliberately,
and can explain why those choices fit a privacy-sensitive health data
platform.

## Pattern Decision Legend

- **Adopted**: part of the intended architecture.
- **Used locally**: useful within a specific component, but not the
  overall system shape.
- **Deferred**: plausible later, but premature for the MVP.
- **Comparison pattern**: useful to understand, but not the current
  design.

## High-Level Architectural Patterns

These patterns define the macro shape of the application: how services
are organized, how data flows, where state lives, and how components
communicate.

### Backend-Centric Modular Monolith

**Definition**: A single deployable application whose internal code is
organized into clear modules, such as API, ingestion, normalization,
retrieval, inference orchestration, and persistence.

**MyHealth status**: Comparison pattern and internal discipline.

**MyHealth example**: Even with service isolation, each service should
be internally modular. The Health Gateway Service, Clinical Ingestion
Worker, Genomic Annotation Worker, and future retrieval or analytics
services should each keep clear boundaries between API/event handlers,
workflows, domain services, adapters, repositories, and models.

**Why it still matters**: A modular monolith remains the baseline
architecture to understand. `myHealth` deliberately moves beyond it
earlier for learning value, but the same modular discipline prevents the
distributed version from becoming a set of tangled services.

**Tradeoffs**:

- Easier to develop, test, and deploy initially.
- Strong local transactions and simpler debugging.
- Can become tangled if module boundaries are not protected.
- Scaling is mostly by scaling the whole backend until specific
  workloads are separated.

### Microservices And Service Isolation

**Definition**: The application is split into independently deployable
services. Each service owns a focused business capability and often owns
its own persistence layer.

**MyHealth status**: Adopted as a learning architecture.

**MyHealth example**: The first split is not many tiny services. It is a
small number of isolated services around sharply different workloads:

- **Health Gateway Service**: handles authentication, serves
  server-rendered Jinja2 views and optional HTMX fragments, manages
  user-facing API routes, and coordinates chat loops.
- **Clinical Ingestion Worker**: runs as an isolated containerized
  worker for heavy Apple Health XML parsing, PDF/OCR extraction, and
  other CPU- or memory-intensive clinical ingestion work.
- **Genomic Annotation Worker**: runs as an isolated containerized
  worker for VCF parsing, ClinVar-style datasets, molecular matrices,
  coordinate mappings, and variant annotation.

Later service candidates might include a retrieval service, inference
gateway, audit/log service, or analytics export service, but those
should follow real pressure from scale, ownership, or security
boundaries.

**Why adopt earlier**: `myHealth` is intentionally a hands-on SWE
learning project. The service split creates practice with distributed
contracts, queues, idempotency, retries, dead-letter handling,
observability, and workload isolation.

**Boundary rule**: Split by workload and trust boundary, not by every
class or feature. The gateway owns user-facing coordination. The parser
owns heavy private ingestion work.

**Tradeoffs**:

- Supports independent scaling and fault isolation.
- Allows different technologies per service when justified.
- Requires strong CI/CD, observability, service contracts, and
  deployment automation.
- Makes cross-service data consistency and local development harder.

### Event-Driven Architecture

**Definition**: Components communicate by publishing and consuming
events that represent state changes, such as `DocumentUploaded`,
`IngestionValidated`, or `EmbeddingsGenerated`.

**MyHealth status**: Adopted.

**MyHealth example**: The gateway publishes or initiates events such as
`BiometricFileUploaded` and `LabReportReceived`. The parsing worker
consumes queued tasks and emits follow-up events such as
`IngestionValidated`, `HealthRecordsPersisted`,
`EmbeddingsRequested`, and `AnalyticsProjectionRequested`.

**Why it fits**: Health data ingestion, document extraction, embedding
generation, and analytical exports are naturally asynchronous. They also
need retry handling, progress visibility, and failure isolation.

**Tradeoffs**:

- Decouples slow processing from user-facing requests.
- Handles long-running ingestion and indexing workflows well.
- Introduces eventual consistency.
- Requires careful observability because failures are less linear than
  request/response flows.

### Serverless Architecture

**Definition**: Code runs as cloud-managed functions or jobs that are
triggered on demand. The cloud provider manages scaling and much of the
runtime infrastructure.

**MyHealth status**: Adopted selectively.

**MyHealth example**: The gateway generates S3 pre-signed upload URLs.
An S3-triggered Lambda validates object metadata and publishes an
ingestion event to SQS, bypassing gateway server file handling for large
biometric exports and documents.

**Why selective**: Serverless is excellent for edge ingest and small
event-triggered tasks. Long-running XML parsing, OCR, and normalization
belong in private worker containers with explicit workflow state.

**Tradeoffs**:

- Reduces infrastructure management.
- Scales automatically for bursty workloads.
- Can introduce cold starts, vendor lock-in, and scattered state
  management.
- Works best when function boundaries are very clear.

### Layered Architecture

**Definition**: The system is organized into layers such as presentation,
API, service, domain, persistence, and external integrations.

**MyHealth status**: Adopted.

**MyHealth example**: FastAPI route handlers render Jinja2 templates
using HTML/CSS, with optional HTMX fragments for server-owned partial
updates. Streamlit is reserved for internal experiments and analytical
prototypes. Service modules enforce workflow rules, repositories or
database modules manage persistence, and provider clients call AWS
Bedrock or storage systems.

**Why it fits**: Sensitive data systems need clear trust boundaries.
Layering prevents UI code from becoming the source of truth and makes it
easier to test business rules away from delivery details.

### Ports And Adapters

**Definition**: Also known as hexagonal architecture. Core application
logic depends on abstract interfaces, while adapters handle concrete
systems such as databases, cloud APIs, file formats, or model providers.

**MyHealth status**: Adopted as a guiding code pattern.

**MyHealth example**: Inference orchestration should not be tightly
coupled to one provider SDK. The application can define an inference
port, with adapters for AWS Bedrock now and another provider later if
needed.

**Why it fits**: Health data systems benefit from replaceable
integrations. File formats, model providers, storage systems, and API
clients will evolve.

## Data And State Design Patterns

These patterns focus on how the platform stores truth, coordinates
workflow state, and handles change over time.

### Polyglot Persistence

**Definition**: Different storage systems are used for different
workloads instead of forcing all data into one database model.

**MyHealth status**: Adopted.

**MyHealth example**:

- PostgreSQL stores canonical operational truth.
- pgvector stores retrieval embeddings and metadata near relational
  access controls.
- DynamoDB stores workflow checkpoints and idempotency records.
- Redis stores read-optimized projections and short-lived dashboard
  state.
- BigQuery stores analytical models and trends.

**Why it fits**: Transactional records, workflow coordination, vector
search, and analytics have different access patterns and scaling needs.

### CQRS

**Definition**: Command Query Responsibility Segregation separates write
operations from read operations. Commands mutate state; queries read
optimized projections.

**MyHealth status**: Adopted for read/write path separation.

**MyHealth example**: Ingestion commands write validated records into
PostgreSQL. Dashboard queries can read Redis projections or BigQuery
models optimized for trend analysis. Retrieval queries can read pgvector
indexes optimized for semantic search.

**Why it fits**: The platform has very different write and read paths.
Ingestion requires correctness and provenance; dashboards need fast
analytical reads; inference needs bounded context retrieval.

**Tradeoffs**:

- Enables workload-specific optimization.
- Makes read models faster and simpler.
- Requires synchronization and freshness tracking between write models
  and read models.

### Idempotent Design

**Definition**: An operation can be safely repeated without producing a
different result after the first successful application.

**MyHealth status**: Adopted.

**MyHealth example**: Re-uploading the same Apple Health export or
retrying a failed document ingestion job should not create duplicate
canonical records. Idempotency keys and source fingerprints can prevent
uncontrolled record multiplication.

**Why it fits**: Healthcare ingestion is retry-heavy. Files can be
duplicated, network calls can fail after partial success, and background
jobs can restart.

### Event Sourcing

**Definition**: The system stores a sequence of immutable events as the
primary source of truth, then derives current state from those events.

**MyHealth status**: Comparison pattern; not adopted as the primary data
model.

**MyHealth example**: A full event-sourced ingestion ledger could store
every workflow transition as an immutable event. Current document status
would be rebuilt from that event stream.

**Why not now**: The project already needs clear relational models for
health records, provenance, authorization, and retrieval metadata. Full
event sourcing would add complexity before it pays off.

**Useful lesson**: Even without full event sourcing, `myHealth` should
record important workflow transitions and audit-relevant events.

### Outbox Pattern

**Definition**: When a service changes database state and needs to emit
an event, it writes the event to an outbox table in the same transaction.
A separate worker publishes the event later.

**MyHealth status**: Deferred but highly relevant.

**MyHealth example**: When a document record is persisted, the same
transaction could write an outbox event requesting text extraction or
embedding generation.

**Why it fits later**: It prevents the classic failure where the
database write succeeds but the event publish fails, leaving downstream
systems unaware of the change.

### Saga Pattern

**Definition**: A long-running workflow is split into a sequence of
steps, each with compensating actions when later steps fail.

**MyHealth status**: Deferred.

**MyHealth example**: A document ingestion saga might upload the raw
file to S3, persist metadata in PostgreSQL, extract text, generate
chunks, create embeddings, and mark the document available for
inference. If embedding generation fails, the saga records failure and
leaves the document in a retryable state.

**Why it fits later**: Ingestion and inference preparation are
multi-step workflows with partial failure modes.

## Low-Level Code Design Patterns

These patterns shape implementation inside modules and services.

### Factory

**Definition**: A factory centralizes object creation so callers do not
need to know the concrete class or setup details.

**MyHealth status**: Used locally.

**MyHealth example**: A parser factory can choose an Apple Health XML
parser, CSV lab parser, PDF text extractor, or VCF parser based on the
source manifest.

**Why it fits**: Ingestion supports heterogeneous formats. Factory
selection keeps branching logic out of every workflow step.

### Strategy

**Definition**: A family of algorithms is encapsulated behind a shared
interface so the application can choose among them at runtime.

**MyHealth status**: Used locally.

**MyHealth example**: Different chunking strategies can be used for
clinical notes, lab reports, wearable summaries, and genomic annotations.
Different retrieval strategies can combine structured filters, vector
similarity, and recency weighting.

**Why it fits**: Health data sources vary. The system should swap
algorithms without rewriting orchestration code.

### Adapter

**Definition**: An adapter translates one interface or data shape into
another expected by the application.

**MyHealth status**: Adopted as a routine integration pattern.

**MyHealth example**: Apple Health XML records, FHIR JSON resources,
ClinVar CSV rows, and Bedrock SDK responses can each be adapted into
internal canonical models.

**Why it fits**: Most value in `myHealth` comes from integrating systems
that were not designed to look alike.

### Facade

**Definition**: A facade exposes a simple interface over a complex
subsystem.

**MyHealth status**: Used locally.

**MyHealth example**: An inference facade can expose one method such as
`answer_health_question(...)` while hiding retrieval, prompt assembly,
privacy checks, Bedrock calls, and response shaping.

**Why it fits**: Complex orchestration should not leak into API route
handlers or UI code.

### Repository

**Definition**: A repository encapsulates data access for a specific
aggregate or model so application services do not contain raw SQL or
database-specific details everywhere.

**MyHealth status**: Used locally where it improves clarity.

**MyHealth example**: Ingestion services can call repositories for
manifests, documents, health measurements, embeddings, or audit records.

**Tradeoff**: Repositories should clarify persistence boundaries, not
become thin wrappers around every SQL statement with no added meaning.

### Unit Of Work

**Definition**: A unit of work groups related persistence changes into
one transaction boundary.

**MyHealth status**: Used locally for transactional workflows.

**MyHealth example**: Persisting an ingestion manifest, normalized
records, provenance links, and status transitions should succeed or fail
as a coherent transaction where possible.

**Why it fits**: Health records require durable correctness and
auditable state changes.

### Observer

**Definition**: Observers subscribe to changes in another object or
stream of events.

**MyHealth status**: Used conceptually in event-driven workflow
processing.

**MyHealth example**: An indexing worker can observe `validated`
ingestion items and generate retrieval artifacts. A metrics component
can observe workflow completions and emit counters.

**Why it fits**: Background processing benefits from decoupled reaction
to state changes.

### Singleton

**Definition**: A singleton ensures only one instance of a class exists
and provides global access to it.

**MyHealth status**: Use cautiously.

**MyHealth example**: Database engines, connection pools, or settings
objects may behave like process-level singletons.

**Caution**: Global mutable state makes tests and concurrency harder.
Dependency injection or explicit application lifecycle management is
usually cleaner in FastAPI.

### Dependency Injection

**Definition**: Dependencies are provided to a component rather than
constructed inside it.

**MyHealth status**: Adopted.

**MyHealth example**: FastAPI dependencies can provide database sessions,
authenticated users, settings, repositories, and service objects.

**Why it fits**: Dependency injection improves testability and makes it
easier to swap real provider clients for fakes in tests.

## Cross-Cutting Engineering Patterns

These patterns are not tied to one module. They make the system safer,
more observable, and easier to operate.

### Validation At Boundaries

**Definition**: Validate data at every external or trust boundary:
request input, file metadata, parser output, database constraints, and
provider responses.

**MyHealth status**: Adopted.

**MyHealth example**: A biomarker value should preserve unit metadata,
timestamps should be normalized deterministically, and source lineage
should be required before records become available for inference.

### Privacy By Design

**Definition**: Privacy constraints are built into the architecture
instead of added as a UI feature or afterthought.

**MyHealth status**: Adopted.

**MyHealth example**: PHI/PII should be segregated where appropriate,
pseudonymization should happen before inference, and model calls should
flow through backend-managed services with auditability.

### Retrieval-Augmented Generation

**Definition**: The system retrieves bounded, relevant context from
trusted stores and passes that context to an LLM instead of relying only
on model memory.

**MyHealth status**: Adopted.

**MyHealth example**: A health question can retrieve structured lab
values, document chunks, provenance metadata, and recent wearable trends
before constructing a prompt.

**Why it fits**: Personal health reasoning must be grounded in the
user's actual records and should preserve provenance.

### Circuit Breaker

**Definition**: When a downstream dependency repeatedly fails, the
application temporarily stops calling it and returns a controlled error
or fallback.

**MyHealth status**: Deferred.

**MyHealth example**: If the inference provider is throttling or timing
out, the application can fail gracefully rather than piling up requests.

### Backpressure

**Definition**: The system slows intake or processing when downstream
components cannot keep up.

**MyHealth status**: Deferred but relevant.

**MyHealth example**: Large document batches or embedding jobs should be
queued and rate-limited so they do not overwhelm the database, model
provider, or worker pool.

### Structured Observability

**Definition**: Logs, metrics, and traces include stable identifiers and
domain context, making workflows debuggable across components.

**MyHealth status**: Adopted.

**MyHealth example**: Ingestion logs should include a workflow ID,
source type, manifest ID, processing stage, counts, retry attempts, and
latency.

## Pattern Fit Summary

| Pattern | Status | MyHealth use |
| --- | --- | --- |
| Backend-centric modular monolith | Comparison | Internal service discipline and baseline pattern |
| Microservices / service isolation | Adopted | Gateway plus private clinical and genomic workers |
| Event-driven architecture | Adopted | Upload, ingestion, indexing, and projection workflows |
| Serverless | Adopted selectively | S3-triggered edge ingest validation and event publishing |
| Layered architecture | Adopted | UI, API, service, persistence boundaries |
| Ports and adapters | Adopted | Provider and data-source integrations |
| Polyglot persistence | Adopted | PostgreSQL, pgvector, DynamoDB, BigQuery |
| CQRS | Adopted | PostgreSQL command path plus Redis/BigQuery/read projections |
| Idempotent design | Adopted | Retry-safe ingestion |
| Event sourcing | Comparison | Useful audit lesson, not primary state model |
| Outbox | Deferred | Reliable event publishing |
| Saga | Deferred | Long-running ingestion workflows |
| Factory | Used locally | Parser and provider selection |
| Strategy | Used locally | Chunking, retrieval, and processing algorithms |
| Adapter | Adopted | External formats to canonical models |
| Facade | Used locally | Inference and retrieval orchestration |
| Repository | Used locally | Persistence boundary clarity |
| Unit of work | Used locally | Transactional state changes |
| Observer | Used conceptually | Worker reactions to workflow state |
| Singleton | Use cautiously | Settings and connection pools only |
| Dependency injection | Adopted | FastAPI services and tests |

## How To Use This Reference While Building

When adding a new feature, ask:

1. What is the source of truth for this state?
2. Is this synchronous user-facing work or asynchronous workflow work?
3. Does the operation need idempotency?
4. Which layer should own the invariant?
5. Is this a one-off integration or should it be hidden behind an
   adapter?
6. Is the read path different enough from the write path to justify a
   projection or analytical model?
7. What identifiers, logs, metrics, and provenance are needed to debug
   it later?

These questions keep advanced concepts connected to actual engineering
decisions rather than becoming vocabulary pasted onto the project.
