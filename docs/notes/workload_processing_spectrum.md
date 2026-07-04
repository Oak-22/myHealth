# Workload Processing Spectrum

## Purpose

This note captures the mental model for deciding whether a `myHealth`
workflow should run synchronously in the user-facing request path,
asynchronously in clinical ingestion workers, in telemetry analytics
workers, or in heavier genomic/molecular processing workers.

The boundary is not traffic volume alone. Distributed processing is
justified when a class of work has different resource, privacy, latency,
or failure characteristics from the user-facing application.

## Spectrum

### 1. Patient / User Request-Response

- small payloads
- low latency
- synchronous
- auth/session aware
- direct user feedback
- simple reads/writes
- stable DB transactions
- examples: dashboard page, lab trend filter, ingestion status, LLM
  question submission

Use this path when the user expects an immediate response and the work
can complete safely within a normal web request.

### 2. Clinical Asset Ingestion And Analysis

- medium to large payloads
- privacy-sensitive
- async preferred
- OCR/parsing/normalization may be slow
- provenance and audit required
- failure should not block the UI
- examples: Apple Health export, lab PDF, clinical document, EHR bundle

Use this path when the work touches PHI-adjacent clinical assets,
requires provenance, or may fail/retry independently of the user's
browser session.

### 3. Telemetry And Recovery Analytics

- small to medium individual payloads
- high longitudinal volume over time
- mixed manual, wearable, CPAP, and behavioral sources
- source facts should become canonical operational records
- derived trends, correlations, features, and predictions are analytics
- privacy-sensitive but usually less compute-heavy than genomic work
- examples: daily recovery entries, CPAP sessions, Apple Health sleep
  metrics, exercise/caffeine/alcohol/stressor logs, cognitive
  performance ratings

Use this path when the platform is collecting longitudinal behavioral or
physiological source facts that explain health and performance outcomes.
Do not treat these records as dashboard-only artifacts; raw telemetry is
part of the source-of-truth layer, while recovery scores and predictive
features are derived.

### 4. Genomic / Molecular Workloads

- large to huge payloads
- latency tolerant
- CPU/memory-heavy
- batch-oriented
- retry/idempotency required
- specialized dependencies
- isolated worker runtime
- examples: VCF parsing, ClinVar annotation, molecular matrices,
  coordinate mappings

Use this path when the workload has a scientific-computing or
data-engineering profile and should not compete with clinical UI
requests or gateway resources.

## Interview Framing

The architectural boundary is workload asymmetry, not company scale.
User-facing clinical requests are low-latency, small-payload,
synchronous workflows with stable transactional reads and writes.
Clinical asset ingestion is more privacy-sensitive and failure-prone, so
it moves into asynchronous storage-first processing.
Telemetry/recovery analytics occupies a middle lane: individual inputs
may be lightweight, but the value comes from preserving them as
longitudinal source facts and deriving trends, correlations, and
features over time. Genomic and molecular workloads are the far end:
large payloads, specialized dependencies, high CPU/memory requirements,
and latency tolerance. That justifies isolated workers, queues,
idempotency, and separate compute profiles.

## Rule Of Thumb

- Keep it synchronous when it is small, fast, user-facing, and
  transactionally simple.
- Queue it when it is slow, retry-prone, privacy-sensitive, or can fail
  independently.
- Isolate it when it needs a different compute profile, dependency set,
  network boundary, or privacy posture.
