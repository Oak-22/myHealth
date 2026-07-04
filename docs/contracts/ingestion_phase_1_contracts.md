# Ingestion Phase 1 Contracts

## Purpose

Phase 1 defines the storage-first boundary for extremely large clinical,
pre-clinical molecular, biometric, document, and genomic payloads.

The rule is simple: no parser receives bytes until the input has been
registered, assigned an idempotent transaction ID, and placed in the raw
object vault.

## Core Flow

```
[Client / UI]
      ↓ request upload registration
[Health Gateway Service]
      ↓ create manifest + transaction ID
[DynamoDB Idempotency Store]
      ↓ reserve or replay transaction
[S3 Pre-signed Upload URL]
      ↓ direct client upload
[S3 Raw Vault]
      ↓ object-created event
[Lambda Edge Ingest Validator]
      ↓ publish task event
[SQS Ingestion Queue]
      ↓ consume event
[Private Worker Service]
      ↓ parse only after idempotency and manifest checks
```

## Implemented Contract Modules

- [schemas.py](/Users/julianbuccat/Projects/dev/myHealth/src/myhealth/ingestion/schemas.py): canonical dataclasses and enums for manifests, uploads, storage references, task events, parser context, normalized batches, and processing results.
- [ports.py](/Users/julianbuccat/Projects/dev/myHealth/src/myhealth/ingestion/ports.py): abstract interfaces for object storage, idempotency, manifest persistence, and event publication.
- [registration.py](/Users/julianbuccat/Projects/dev/myHealth/src/myhealth/ingestion/registration.py): gateway-side registration use case that creates the transaction before upload/parsing.
- [strategies.py](/Users/julianbuccat/Projects/dev/myHealth/src/myhealth/ingestion/strategies.py): parser strategy interface and registry for XML, CSV, FHIR JSON, PDF/OCR, VCF, and molecular matrix parsers.
- [events.py](/Users/julianbuccat/Projects/dev/myHealth/src/myhealth/ingestion/events.py): task-event construction helpers for S3/Lambda-to-queue boundaries.

## Main Schemas

### UploadRegistrationRequest

Created by the gateway when a user or upstream system wants to ingest a
large payload.

Required fields include:

- `subject_ref`
- `source_system`
- `data_domain`
- `payload_format`
- `job_type`
- `original_filename`
- `declared_content_type`

Optional fields include declared file size, source timestamp, a
client-supplied idempotency key, and metadata.

### IngestionManifest

The canonical pre-parse intake record. It binds:

- `manifest_id`
- `transaction_id`
- subject reference
- source system
- data domain
- payload format
- job type
- declared file metadata
- storage object reference
- durable workflow status

### IngestionTaskEvent

The queue contract consumed by private workers. It carries the manifest,
transaction, job type, storage reference, domain, format, and trace
metadata needed to process the object without coupling the worker to the
gateway.

## Idempotency Rule

The transaction ID is deterministic and created before parsing. If a
client does not supply a key, the platform hashes stable registration
inputs such as subject, source, domain, format, job type, filename,
content type, declared size, and source timestamp.

Workers should check this transaction before expensive work. Duplicate
events should replay or no-op rather than parse the same massive payload
again.

## Parser Strategy Rule

Workers must resolve parsers through `StrategyRegistry`, not through
large if/else chains.

Examples of intended strategies:

- `AppleHealthXmlStrategy`
- `FhirJsonStrategy`
- `LabCsvStrategy`
- `PdfOcrStrategy`
- `VcfGenomicStrategy`
- `MolecularMatrixStrategy`

## Phase 1 Non-Goals

This phase does not implement AWS clients, real S3 uploads, real SQS
publication, DynamoDB persistence, OCR, VCF parsing, or PostgreSQL
writes. It defines the contracts those implementations must satisfy.

## Verification

Current tests validate that:

- upload registration creates a transaction before parsing
- duplicate registration returns an idempotency replay decision
- object-created events carry the worker contract

Run:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
