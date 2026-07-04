"""Gateway-side upload registration use case."""

from __future__ import annotations

from datetime import timedelta

from myhealth.ingestion.idempotency import IdempotencyKeyFactory
from myhealth.ingestion.ports import (
    IdempotencyStorePort,
    ManifestRepositoryPort,
    ObjectStoragePort,
)
from myhealth.ingestion.schemas import (
    IdempotencyDecision,
    IngestionManifest,
    IngestionStatus,
    StorageObjectRef,
    UploadRegistrationRequest,
    UploadRegistrationResponse,
    new_manifest_id,
    utc_now,
)


class IngestionRegistrationService:
    """Registers data inputs before S3 upload and before parsing.

    This use case is intentionally synchronous and light. It creates a
    manifest, reserves a deterministic transaction ID, and returns a
    direct-to-S3 upload capability. It never reads or parses file bytes.
    """

    def __init__(
        self,
        storage: ObjectStoragePort,
        manifests: ManifestRepositoryPort,
        idempotency: IdempotencyStorePort,
        upload_ttl: timedelta = timedelta(minutes=30),
    ) -> None:
        self._storage = storage
        self._manifests = manifests
        self._idempotency = idempotency
        self._upload_ttl = upload_ttl

    def register_upload(
        self,
        request: UploadRegistrationRequest,
    ) -> UploadRegistrationResponse:
        transaction_id = IdempotencyKeyFactory.build(request)
        placeholder_ref = StorageObjectRef(bucket="", key="")
        manifest = IngestionManifest(
            manifest_id=new_manifest_id(),
            transaction_id=transaction_id,
            subject_ref=request.subject_ref,
            source_system=request.source_system,
            data_domain=request.data_domain,
            payload_format=request.payload_format,
            job_type=request.job_type,
            original_filename=request.original_filename,
            declared_content_type=request.declared_content_type,
            declared_size_bytes=request.declared_size_bytes,
            status=IngestionStatus.REGISTERED,
            storage_ref=placeholder_ref,
            created_at=utc_now(),
            source_observed_at=request.source_observed_at,
            metadata=request.metadata,
        )

        storage_ref = self._storage.allocate_raw_object(manifest)
        manifest = IngestionManifest(
            manifest_id=manifest.manifest_id,
            transaction_id=manifest.transaction_id,
            subject_ref=manifest.subject_ref,
            source_system=manifest.source_system,
            data_domain=manifest.data_domain,
            payload_format=manifest.payload_format,
            job_type=manifest.job_type,
            original_filename=manifest.original_filename,
            declared_content_type=manifest.declared_content_type,
            declared_size_bytes=manifest.declared_size_bytes,
            status=IngestionStatus.UPLOAD_URL_ISSUED,
            storage_ref=storage_ref,
            created_at=manifest.created_at,
            source_observed_at=manifest.source_observed_at,
            metadata=manifest.metadata,
        )

        decision = self._idempotency.reserve(transaction_id, manifest)
        if decision is IdempotencyDecision.RESERVED:
            self._manifests.create(manifest)

        upload = self._storage.create_presigned_upload(
            storage_ref=storage_ref,
            content_type=request.declared_content_type,
            expires_in=self._upload_ttl,
        )
        return UploadRegistrationResponse(
            manifest=manifest,
            upload=upload,
            idempotency_decision=decision,
        )
