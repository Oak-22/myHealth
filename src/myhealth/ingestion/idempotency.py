"""Idempotent transaction ID generation for ingestion registration."""

from __future__ import annotations

from hashlib import sha256

from myhealth.ingestion.schemas import UploadRegistrationRequest


class IdempotencyKeyFactory:
    """Builds deterministic transaction IDs before parsing occurs."""

    @staticmethod
    def build(request: UploadRegistrationRequest) -> str:
        if request.client_supplied_idempotency_key:
            return request.client_supplied_idempotency_key

        observed_at = (
            request.source_observed_at.isoformat()
            if request.source_observed_at is not None
            else ""
        )
        size = "" if request.declared_size_bytes is None else str(request.declared_size_bytes)
        material = "|".join(
            [
                request.subject_ref,
                request.source_system,
                request.data_domain,
                request.payload_format,
                request.job_type,
                request.original_filename,
                request.declared_content_type,
                size,
                observed_at,
            ]
        )
        return sha256(material.encode("utf-8")).hexdigest()
