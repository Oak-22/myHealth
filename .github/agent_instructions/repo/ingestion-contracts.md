# Ingestion Contract Instructions

Routing: Read this file fully for work involving upload registration, S3, queue events, idempotency, parser strategies, clinical ingestion workers, genomic annotation workers, tests, or ingestion docs.

## Core Boundary

No parser receives bytes until the input has been:

1. registered by the Health Gateway Service
2. assigned a deterministic idempotent transaction ID
3. assigned an ingestion manifest
4. assigned an S3 raw-vault object reference
5. uploaded through the storage-first path
6. represented as a queue task event

## Active Implementation

The Phase 1 contract layer lives under:

- `src/myhealth/ingestion/schemas.py`
- `src/myhealth/ingestion/ports.py`
- `src/myhealth/ingestion/idempotency.py`
- `src/myhealth/ingestion/registration.py`
- `src/myhealth/ingestion/events.py`
- `src/myhealth/ingestion/strategies.py`
- `tests/test_ingestion_contracts.py`
- `docs/contracts/ingestion_phase_1_contracts.md`

## Agent Rules

- Treat schema dataclasses and enums as public contracts.
- Preserve transaction assignment before parsing.
- Preserve storage-first upload semantics; do not add raw file upload
  handling to the gateway path unless explicitly requested.
- Queue events should carry references and metadata, not raw bytes.
- Idempotency behavior should be deterministic and covered by tests.
- Parser selection should go through `StrategyRegistry`, not broad
  if/else chains.
- Add focused tests for new event fields, status transitions,
  idempotency behavior, or parser registry behavior.
- Keep worker-specific dependencies out of the gateway layer.

## Worker Boundaries

- Clinical Ingestion Worker:
  Apple Health XML, clinical documents, PDF/OCR extraction, lab CSV, and
  normalized clinical ingestion. Treat this path as restrained,
  PHI-adjacent, pseudonymized before inference, and audit-sensitive.
- Genomic Annotation Worker:
  VCF parsing, ClinVar-style datasets, molecular matrices, coordinate
  mappings, and variant annotation. This path may be more autonomous and
  compute-heavy when operating on public, synthetic, non-PHI, or
  pseudonymized payloads.

## Domain Routing

- Clinical, biometric, and document payloads default to the restrained
  clinical path.
- Preclinical molecular and genomic payloads may route to the
  autonomous molecular path when they are public, synthetic, non-PHI, or
  pseudonymized.
- Cross-domain promotion into patient-facing clinical context requires
  explicit provenance and review boundaries.

## Source Of Truth

Use [Ingestion Phase 1 Contracts](../../../docs/contracts/ingestion_phase_1_contracts.md)
as the human-readable contract overview.
