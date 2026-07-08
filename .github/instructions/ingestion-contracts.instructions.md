---
description: "Use for upload registration, S3/object references, queue events, idempotency, parser strategies, ingestion worker concepts, or ingestion docs."
applyTo: "docs/contracts/**/*.md, docs/architecture/**/*.md, docs/adr/**/*.md, .github/**/*.md"
---
# Ingestion Contract Instructions

## Core Boundary

No parser receives bytes until the input has been:

1. registered by the Health Gateway Service
2. assigned a deterministic idempotent transaction ID
3. assigned an ingestion manifest
4. assigned a raw-vault object reference
5. uploaded through the storage-first path
6. represented as a queue task event

## Current Mode

The repository is currently a harness evaluation target. Product source
code and tests are intentionally absent under ADR 0010.

The Phase 1 contract layer lives as documentation under:

- `docs/contracts/ingestion_phase_1_contracts.md`

## Agent Rules

- Treat documented schemas, events, and state transitions as public
  contracts.
- Preserve transaction assignment before parsing.
- Preserve storage-first upload semantics.
- Queue events should carry references and metadata, not raw bytes.
- Idempotency behavior should remain deterministic.
- Parser selection should remain strategy-based in future
  implementation, not broad conditional chains.
- Capture future test expectations in contracts or evaluation specs
  until product implementation resumes.
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

Use [Ingestion Phase 1 Contracts](../../docs/contracts/ingestion_phase_1_contracts.md)
as the human-readable contract overview.
