# Code Pattern Scaffolding

## Purpose

This note maps low-level code design patterns to the non-functional
requirements and macro architecture that make them necessary in
`myHealth`.

The goal is not to use patterns for their own sake. A pattern should
appear only where a real constraint creates pressure for it.

## Crosswalk

| NFR pressure | Macro architecture consequence | Code-level pattern | Natural location |
| --- | --- | --- | --- |
| Source-specific parsing must remain isolated | Clinical and genomic ingestion workers process heterogeneous formats | Strategy | `src/myhealth/ingestion/strategies.py` |
| Integration constraints belong at boundaries | Gateway/workers integrate with S3, SQS, DynamoDB, PostgreSQL, Bedrock | Ports and adapters | `src/myhealth/*/ports.py`, future `adapters/` |
| Duplicate inputs must not create duplicate writes | Storage-first async ingestion reserves transactions before parsing | Factory / idempotency factory | `src/myhealth/ingestion/idempotency.py` |
| Workflow state must be durable and auditable | Manifest and status state are stored outside transient workers | Repository | `src/myhealth/*/repositories.py` or `repositories/` |
| Related canonical writes must succeed together | Ingestion persists records, provenance, status, and outbox events | Unit of Work | future Postgres persistence layer |
| Slow workflows must not block user requests | Gateway publishes events; workers react asynchronously | Event publisher / queue consumer | `events.py`, future worker handlers |
| Complex orchestration must not leak into routes | Gateway exposes simple operations over retrieval, inference, storage | Facade | future `services/inference.py`, `services/storage.py` |
| Components must be testable with fakes | FastAPI routes and services receive dependencies explicitly | Dependency Injection | FastAPI dependencies and service constructors |
| Connection lifecycle must be controlled | Engines, pools, clients, settings are process-scoped resources | Lifecycle-managed singleton-like resources | app startup/lifespan, not global mutable classes |

## Current Phase 1 Patterns

Phase 1 ingestion contracts already contain these patterns:

- **Strategy**
  - `IngestionStrategy`
  - `StrategyRegistry`
  - Reason: heterogeneous payload parsing requires swappable parser
    algorithms.

- **Ports and adapters**
  - `ObjectStoragePort`
  - `IdempotencyStorePort`
  - `ManifestRepositoryPort`
  - `EventPublisherPort`
  - Reason: the ingestion core should not depend directly on AWS,
    PostgreSQL, or queue SDKs.

- **Repository port**
  - `ManifestRepositoryPort`
  - Reason: manifest persistence is canonical workflow state and should
    not leak raw SQL into registration logic.

- **Idempotency factory**
  - `IdempotencyKeyFactory`
  - Reason: distributed retries require deterministic transaction IDs
    before parsing starts.

- **Event contract**
  - `IngestionTaskEvent`
  - `build_object_created_event(...)`
  - Reason: storage-first ingestion crosses a queue boundary and needs a
    stable worker-facing payload shape.

## Future Pattern Scaffolding

### Adapter

**NFR pressure**: integration constraints should be handled at adapters,
not in core logic.

**Macro constraint**: the platform talks to S3, SQS, DynamoDB,
PostgreSQL, Bedrock, BigQuery, and external healthcare formats.

**Where it belongs**:

```text
src/myhealth/adapters/storage/s3.py
src/myhealth/adapters/queue/sqs.py
src/myhealth/adapters/idempotency/dynamodb.py
src/myhealth/adapters/inference/bedrock.py
src/myhealth/adapters/parsers/apple_health_xml.py
src/myhealth/adapters/parsers/fhir_json.py
src/myhealth/adapters/parsers/vcf.py
```

**Rule**: adapters translate external APIs or payload formats into
internal contracts. Core services should depend on ports, not SDKs.

### Facade

**NFR pressure**: privacy and audit constraints require complex
orchestration to stay backend-owned and reviewable.

**Macro constraint**: routes should not directly assemble retrieval,
pseudonymization, prompt construction, provider calls, and audit logs.

**Where it belongs**:

```text
src/myhealth/services/inference_facade.py
src/myhealth/services/storage_facade.py
src/myhealth/services/ingestion_facade.py
```

**Candidate methods**:

```text
answer_health_question(...)
register_clinical_upload(...)
request_document_extraction(...)
request_genomic_annotation(...)
```

**Rule**: facades expose one application-level operation while hiding
multi-step orchestration behind it.

### Unit Of Work

**NFR pressure**: canonical records must preserve provenance, duplicate
inputs must not create uncontrolled writes, and workflow transitions
must be auditable.

**Macro constraint**: ingestion writes may involve records, provenance,
status changes, embeddings metadata, and outbox events.

**Where it belongs**:

```text
src/myhealth/persistence/unit_of_work.py
src/myhealth/repositories/
```

**Candidate transaction**:

```text
persist normalized records
  + provenance links
  + manifest status transition
  + audit event
  + outbox event
```

**Rule**: use a unit of work when multiple persistence changes must
succeed or fail together.

### Outbox

**NFR pressure**: partial failures must be recoverable and downstream
systems must not silently miss state changes.

**Macro constraint**: event-driven services need reliable publication
after canonical database writes.

**Where it belongs**:

```text
src/myhealth/persistence/outbox.py
src/myhealth/workers/outbox_publisher.py
```

**Rule**: when a database write should cause a downstream event, write
the outbox record in the same transaction as the state change.

### Dependency Injection

**NFR pressure**: services must be testable, privacy boundaries must be
auditable, and integrations must be replaceable with fakes.

**Macro constraint**: gateway routes, workers, and services depend on
storage, queues, repositories, idempotency stores, and inference
providers.

**Where it belongs**:

```text
src/myhealth/gateway/dependencies.py
src/myhealth/workers/dependencies.py
service constructors
```

**Rule**: pass ports/repositories/services into use cases rather than
creating SDK clients inside business logic.

### Observer

**NFR pressure**: multiple subsystems need to react to workflow state
changes.

**Macro constraint**: the architecture is event-driven, so most
reaction should happen through durable events rather than in-process
observer lists.

**Where it belongs**:

```text
src/myhealth/workers/indexing_worker.py
src/myhealth/workers/analytics_projection_worker.py
src/myhealth/workers/audit_worker.py
```

**Rule**: prefer queue/event consumers over in-process Observer for
cross-service behavior. Use in-process observer hooks only for local
metrics or instrumentation where durability is not required.

### Singleton

**NFR pressure**: resource usage and connection lifecycle must be
controlled.

**Macro constraint**: services need database engines, HTTP clients,
settings, and cloud SDK clients without recreating them per operation.

**Where it belongs**:

```text
FastAPI lifespan setup
worker process startup
settings module
connection pool initialization
```

**Rule**: avoid hand-rolled global mutable singletons. Prefer
framework-managed lifecycle resources and dependency injection.

## Implementation Order

1. Keep Phase 1 ingestion contracts stable.
2. Add concrete adapters for local development first, such as local
   filesystem storage, in-memory idempotency, and fake queue publisher.
3. Add cloud adapters once the local contract behavior is verified.
4. Add repository implementations when PostgreSQL schemas are ready.
5. Add Unit of Work when normalized records, provenance, status, and
   outbox events need transactional persistence.
6. Add facades once routes or workers start coordinating multiple
   services directly.
7. Add durable event consumers for indexing, analytics projection, and
   audit workflows.

## Guardrails

- Do not introduce a pattern without a named NFR pressure.
- Do not duplicate a macro service boundary inside every module.
- Keep clinical privacy and provenance boundaries more important than
  pattern purity.
- Prefer simple functions until orchestration or integration pressure
  makes a pattern useful.
