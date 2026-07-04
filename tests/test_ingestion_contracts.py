from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

from myhealth.ingestion.events import build_object_created_event
from myhealth.ingestion.ports import (
    IdempotencyStorePort,
    ManifestRepositoryPort,
    ObjectStoragePort,
)
from myhealth.ingestion.registration import IngestionRegistrationService
from myhealth.ingestion.schemas import (
    DataDomain,
    IdempotencyDecision,
    IngestionManifest,
    IngestionStatus,
    JobType,
    PayloadFormat,
    PreSignedUpload,
    ProcessingResult,
    SourceSystem,
    StorageObjectRef,
    UploadRegistrationRequest,
)


class FakeStorage(ObjectStoragePort):
    def allocate_raw_object(self, manifest: IngestionManifest) -> StorageObjectRef:
        return StorageObjectRef(
            bucket="myhealth-raw-vault",
            key=f"raw/{manifest.subject_ref}/{manifest.manifest_id}/{manifest.original_filename}",
            region="us-west-2",
        )

    def create_presigned_upload(
        self,
        storage_ref: StorageObjectRef,
        content_type: str,
        expires_in: timedelta,
    ) -> PreSignedUpload:
        return PreSignedUpload(
            url=f"https://upload.example.test/{storage_ref.key}",
            method="PUT",
            expires_at=datetime.now(timezone.utc) + expires_in,
            required_headers={"content-type": content_type},
            storage_ref=storage_ref,
        )


class FakeManifests(ManifestRepositoryPort):
    def __init__(self) -> None:
        self.created: list[IngestionManifest] = []
        self.statuses: list[tuple[str, IngestionStatus, str | None]] = []

    def create(self, manifest: IngestionManifest) -> None:
        self.created.append(manifest)

    def update_status(
        self,
        manifest_id: str,
        status: IngestionStatus,
        reason: str | None = None,
    ) -> None:
        self.statuses.append((manifest_id, status, reason))


class FakeIdempotency(IdempotencyStorePort):
    def __init__(self) -> None:
        self.keys: set[str] = set()

    def reserve(self, transaction_id: str, manifest: IngestionManifest) -> IdempotencyDecision:
        if transaction_id in self.keys:
            return IdempotencyDecision.REPLAY_EXISTING
        self.keys.add(transaction_id)
        return IdempotencyDecision.RESERVED

    def mark_completed(self, transaction_id: str, result: ProcessingResult) -> None:
        pass

    def mark_failed(self, transaction_id: str, result: ProcessingResult) -> None:
        pass


class IngestionContractTests(unittest.TestCase):
    def test_register_upload_assigns_transaction_before_parsing(self) -> None:
        manifests = FakeManifests()
        service = IngestionRegistrationService(
            storage=FakeStorage(),
            manifests=manifests,
            idempotency=FakeIdempotency(),
        )
        request = UploadRegistrationRequest(
            subject_ref="subject-123",
            source_system=SourceSystem.CLINVAR,
            data_domain=DataDomain.GENOMIC,
            payload_format=PayloadFormat.VCF,
            job_type=JobType.GENOMIC_PARSE,
            original_filename="variants.vcf",
            declared_content_type="text/vcf",
            declared_size_bytes=10_000_000,
            source_observed_at=datetime(2026, 7, 4, tzinfo=timezone.utc),
        )

        response = service.register_upload(request)

        self.assertEqual(response.idempotency_decision, IdempotencyDecision.RESERVED)
        self.assertEqual(response.manifest.status, IngestionStatus.UPLOAD_URL_ISSUED)
        self.assertEqual(response.manifest.storage_ref.bucket, "myhealth-raw-vault")
        self.assertTrue(response.manifest.transaction_id)
        self.assertEqual(len(manifests.created), 1)

    def test_duplicate_registration_replays_existing_transaction(self) -> None:
        idempotency = FakeIdempotency()
        manifests = FakeManifests()
        service = IngestionRegistrationService(
            storage=FakeStorage(),
            manifests=manifests,
            idempotency=idempotency,
        )
        request = UploadRegistrationRequest(
            subject_ref="subject-123",
            source_system=SourceSystem.APPLE_HEALTH,
            data_domain=DataDomain.BIOMETRIC,
            payload_format=PayloadFormat.ZIP,
            job_type=JobType.BIOMETRIC_PARSE,
            original_filename="apple-health.zip",
            declared_content_type="application/zip",
            declared_size_bytes=500_000_000,
        )

        first = service.register_upload(request)
        second = service.register_upload(request)

        self.assertEqual(first.manifest.transaction_id, second.manifest.transaction_id)
        self.assertEqual(second.idempotency_decision, IdempotencyDecision.REPLAY_EXISTING)
        self.assertEqual(len(manifests.created), 1)

    def test_object_created_event_carries_worker_contract(self) -> None:
        service = IngestionRegistrationService(
            storage=FakeStorage(),
            manifests=FakeManifests(),
            idempotency=FakeIdempotency(),
        )
        response = service.register_upload(
            UploadRegistrationRequest(
                subject_ref="subject-abc",
                source_system=SourceSystem.LAB_PORTAL,
                data_domain=DataDomain.CLINICAL,
                payload_format=PayloadFormat.PDF,
                job_type=JobType.OCR_EXTRACT,
                original_filename="lab.pdf",
                declared_content_type="application/pdf",
            )
        )

        event = build_object_created_event(
            response.manifest,
            event_type="LabReportReceived",
            trace_id="trace-1",
        )

        self.assertEqual(event.manifest_id, response.manifest.manifest_id)
        self.assertEqual(event.transaction_id, response.manifest.transaction_id)
        self.assertEqual(event.job_type, JobType.OCR_EXTRACT)
        self.assertEqual(event.storage_ref.uri, response.manifest.storage_ref.uri)
        self.assertEqual(event.trace_id, "trace-1")


if __name__ == "__main__":
    unittest.main()
