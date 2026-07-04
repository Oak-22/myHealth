"""Schema contracts for the storage-first ingestion boundary.

These dataclasses are intentionally infrastructure-neutral. Gateway,
Lambda, queue consumers, and parsing workers should agree on these
shapes before any parsing logic is introduced.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4


class DataDomain(StrEnum):
    """High-level privacy and workload domain for an uploaded payload."""

    CLINICAL = "clinical"
    PRECLINICAL_MOLECULAR = "preclinical_molecular"
    GENOMIC = "genomic"
    BIOMETRIC = "biometric"
    DOCUMENT = "document"


class SourceSystem(StrEnum):
    """External source family for a payload."""

    APPLE_HEALTH = "apple_health"
    FHIR_API = "fhir_api"
    LAB_PORTAL = "lab_portal"
    CLINICAL_DOCUMENT = "clinical_document"
    CLINVAR = "clinvar"
    SYNTHETIC_SYNTHEA = "synthetic_synthea"
    UNKNOWN = "unknown"


class PayloadFormat(StrEnum):
    """Wire/storage format of the uploaded object."""

    XML = "xml"
    JSON = "json"
    CSV = "csv"
    TSV = "tsv"
    PDF = "pdf"
    VCF = "vcf"
    PARQUET = "parquet"
    ZIP = "zip"
    UNKNOWN = "unknown"


class JobType(StrEnum):
    """Worker class that should consume the ingestion task."""

    BIOMETRIC_PARSE = "biometric_parse"
    CLINICAL_DOCUMENT_PARSE = "clinical_document_parse"
    OCR_EXTRACT = "ocr_extract"
    GENOMIC_PARSE = "genomic_parse"
    MOLECULAR_MATRIX_PARSE = "molecular_matrix_parse"
    FHIR_NORMALIZE = "fhir_normalize"


class IngestionStatus(StrEnum):
    """Durable workflow states visible before and after parsing."""

    REGISTERED = "registered"
    UPLOAD_URL_ISSUED = "upload_url_issued"
    OBJECT_CREATED = "object_created"
    QUEUED = "queued"
    IDEMPOTENCY_REPLAYED = "idempotency_replayed"
    PARSING = "parsing"
    VALIDATED = "validated"
    FAILED_VALIDATION = "failed_validation"
    PERSISTED = "persisted"
    INDEXED = "indexed"
    AVAILABLE_FOR_INFERENCE = "available_for_inference"
    FAILED = "failed"
    QUARANTINED = "quarantined"


class IdempotencyDecision(StrEnum):
    """Result of attempting to reserve an idempotent transaction."""

    RESERVED = "reserved"
    REPLAY_EXISTING = "replay_existing"
    CONFLICT = "conflict"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class StorageObjectRef:
    """Stable reference to an object in the raw vault layer."""

    bucket: str
    key: str
    version_id: str | None = None
    region: str | None = None
    etag: str | None = None

    @property
    def uri(self) -> str:
        return f"s3://{self.bucket}/{self.key}"


@dataclass(frozen=True, slots=True)
class PreSignedUpload:
    """Upload capability returned by the gateway before file transfer."""

    url: str
    method: str
    expires_at: datetime
    required_headers: dict[str, str] = field(default_factory=dict)
    storage_ref: StorageObjectRef | None = None


@dataclass(frozen=True, slots=True)
class UploadRegistrationRequest:
    """Gateway request to register an object before upload and parsing."""

    subject_ref: str
    source_system: SourceSystem
    data_domain: DataDomain
    payload_format: PayloadFormat
    job_type: JobType
    original_filename: str
    declared_content_type: str
    declared_size_bytes: int | None = None
    source_observed_at: datetime | None = None
    client_supplied_idempotency_key: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class IngestionManifest:
    """Canonical intake record created before any parser sees bytes."""

    manifest_id: UUID
    transaction_id: str
    subject_ref: str
    source_system: SourceSystem
    data_domain: DataDomain
    payload_format: PayloadFormat
    job_type: JobType
    original_filename: str
    declared_content_type: str
    declared_size_bytes: int | None
    status: IngestionStatus
    storage_ref: StorageObjectRef
    created_at: datetime
    source_observed_at: datetime | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class UploadRegistrationResponse:
    """Gateway response for storage-first asynchronous ingestion."""

    manifest: IngestionManifest
    upload: PreSignedUpload
    idempotency_decision: IdempotencyDecision


@dataclass(frozen=True, slots=True)
class IngestionTaskEvent:
    """Queue contract consumed by private ingestion workers."""

    event_id: UUID
    event_type: str
    manifest_id: UUID
    transaction_id: str
    job_type: JobType
    source_system: SourceSystem
    data_domain: DataDomain
    payload_format: PayloadFormat
    storage_ref: StorageObjectRef
    emitted_at: datetime
    trace_id: str | None = None
    attributes: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["event_id"] = str(self.event_id)
        payload["manifest_id"] = str(self.manifest_id)
        payload["emitted_at"] = self.emitted_at.isoformat()
        return payload


@dataclass(frozen=True, slots=True)
class ParseContext:
    """Context available to strategies after idempotency is reserved."""

    manifest_id: UUID
    transaction_id: str
    subject_ref: str
    source_system: SourceSystem
    data_domain: DataDomain
    payload_format: PayloadFormat
    storage_ref: StorageObjectRef
    trace_id: str | None = None


@dataclass(frozen=True, slots=True)
class NormalizedRecordBatch:
    """Parser output before persistence into canonical stores."""

    manifest_id: UUID
    transaction_id: str
    records: tuple[dict[str, Any], ...]
    provenance: dict[str, Any]
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ProcessingResult:
    """Durable result reported after a worker attempts processing."""

    manifest_id: UUID
    transaction_id: str
    status: IngestionStatus
    record_count: int = 0
    error_code: str | None = None
    error_message: str | None = None
    completed_at: datetime = field(default_factory=utc_now)


def new_manifest_id() -> UUID:
    return uuid4()


def new_event_id() -> UUID:
    return uuid4()
