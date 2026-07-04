# Data Dictionary

## Purpose

This document is a curated dictionary for the most important data
domains in `myHealth`. It is intentionally high signal rather than
exhaustive.

## Conventions

- event timestamps should be stored with clear timezone handling
- numeric health values should preserve units
- identifiers should distinguish source identifiers from internal
  canonical identifiers
- provenance columns should describe where data came from, not just when
  it was written

## Core Domains

### `ingestion_manifests`

- `manifest_id`
  Unique identifier for an ingestion attempt or batch
- `source_type`
  Logical source category such as Apple Health, lab CSV, or PDF upload
- `source_version`
  Known schema or export version when available
- `received_at`
  Timestamp when the platform accepted the source payload
- `processing_status`
  Current workflow state for the manifest
- `idempotency_key`
  Stable key used to prevent duplicate processing

### `source_files`

- `source_file_id`
  Internal identifier for an uploaded or discovered source artifact
- `manifest_id`
  Parent ingestion manifest reference
- `file_format`
  Declared or detected format such as XML, CSV, PDF, or VCF
- `checksum`
  Hash used for deduplication and integrity checks
- `storage_uri`
  Storage location for the raw payload when applicable

### `observations`

- `observation_id`
  Canonical identifier for a normalized measurement
- `subject_id`
  Pseudonymized internal subject reference
- `observation_type`
  Normalized metric type such as heart rate or sleep duration
- `observed_at`
  Event timestamp for the measured value
- `value_numeric`
  Primary numeric value when applicable
- `unit`
  Measurement unit preserved from source or mapped canonically
- `source_record_ref`
  Trace back to the source event or file location

  ## observations

| Column | Type | Description | Notes |
|---|---|---|---|
| observation_id | UUID | Canonical observation identifier | Primary key |
| subject_id | UUID | Pseudonymized subject reference | Foreign key |
| observation_type | TEXT | Normalized metric type | e.g. heart_rate |
| observed_at | TIMESTAMPTZ | Event timestamp | Source event time |
| value_numeric | NUMERIC | Measured numeric value | Unit-dependent |
| unit | TEXT | Measurement unit | bpm, mg/dL, etc. |


### `lab_results`

- `lab_result_id`
  Canonical identifier for a laboratory result
- `subject_id`
  Pseudonymized subject reference
- `analyte_code`
  Normalized test identifier
- `result_value`
  Result value as normalized text or numeric form
- `result_unit`
  Unit associated with the result
- `reference_range`
  Source or normalized reference interval
- `collected_at`
  Sample collection timestamp when available

### `daily_telemetry_entries`

- `telemetry_entry_id`
  Canonical identifier for a daily telemetry record
- `subject_id`
  Pseudonymized subject reference
- `entry_date`
  Local calendar date the entry describes
- `source_type`
  Manual entry, Apple Health import, CPAP export, workout import, or
  other telemetry source
- `recorded_at`
  Timestamp when the platform accepted or recorded the entry
- `source_record_ref`
  Trace back to the source form submission, file, or imported record

### `sleep_recovery_assessments`

- `assessment_id`
  Canonical identifier for a subjective recovery assessment
- `subject_id`
  Pseudonymized subject reference
- `entry_date`
  Date the assessment describes
- `restedness_score`
  User-reported restedness rating
- `mental_clarity_score`
  User-reported mental clarity rating
- `sleep_inertia_score`
  User-reported sleep inertia rating
- `energy_score`
  Midday energy rating when available
- `focus_score`
  Midday focus rating when available
- `productivity_score`
  End-of-day productivity or performance rating when available

### `cpap_sessions`

- `cpap_session_id`
  Canonical identifier for a CPAP therapy session
- `subject_id`
  Pseudonymized subject reference
- `session_started_at`
  Start timestamp for the therapy session
- `usage_minutes`
  Total CPAP usage duration
- `ahi`
  Apnea-hypopnea index reported by the source system
- `leak_95_percentile`
  95th percentile leak value when available
- `pressure_95_percentile`
  95th percentile pressure value when available
- `mask_removed`
  Whether the mask was removed during the session
- `source_record_ref`
  Trace back to OSCAR, device export, or manual source

### `behavioral_factors`

- `behavioral_factor_id`
  Canonical identifier for a daily behavior factor
- `subject_id`
  Pseudonymized subject reference
- `entry_date`
  Date the behavior describes
- `factor_type`
  Workout, caffeine, alcohol, late meal, stressor, congestion, or other
  behavioral category
- `value_numeric`
  Numeric representation where applicable
- `value_text`
  Categorical or free-text representation where applicable
- `unit`
  Unit for numeric values when applicable

### `documents`

- `document_id`
  Canonical identifier for a document artifact
- `subject_id`
  Owning subject or access boundary reference
- `document_type`
  High-level classification such as clinical note or radiology report
- `source_file_id`
  Link to the uploaded or discovered raw artifact
- `ingested_at`
  Timestamp the document entered the platform

### `document_chunks`

- `chunk_id`
  Identifier for retrieval-addressable text chunk
- `document_id`
  Parent document reference
- `chunk_index`
  Stable ordering of chunks within a document
- `page_ref`
  Page or location metadata for provenance
- `chunk_text`
  Extracted text content
- `embedding_status`
  State of downstream embedding/index generation

### `genomic_variants`

- `variant_id`
  Internal identifier for a normalized variant record
- `subject_id`
  Subject reference when variant data is person-linked
- `gene_symbol`
  Associated gene or locus annotation
- `variant_notation`
  Canonical textual representation of the variant
- `clinical_significance`
  Source-derived or normalized significance label
- `annotation_source`
  Provenance for the interpretation or annotation

## Sensitivity Classes

The platform should distinguish at least:

- direct identifiers
- pseudonymized subject references
- clinical content
- derived analytics
- telemetry source facts
- operational metadata

This classification helps determine allowed storage, retrieval, logging,
and inference behavior.
