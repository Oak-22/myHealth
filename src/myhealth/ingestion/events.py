"""Event construction helpers for ingestion workflow boundaries."""

from __future__ import annotations

from myhealth.ingestion.schemas import (
    IngestionManifest,
    IngestionTaskEvent,
    new_event_id,
    utc_now,
)


def build_object_created_event(
    manifest: IngestionManifest,
    event_type: str,
    trace_id: str | None = None,
    attributes: dict[str, str] | None = None,
) -> IngestionTaskEvent:
    """Create the queue task emitted after raw object creation."""

    return IngestionTaskEvent(
        event_id=new_event_id(),
        event_type=event_type,
        manifest_id=manifest.manifest_id,
        transaction_id=manifest.transaction_id,
        job_type=manifest.job_type,
        source_system=manifest.source_system,
        data_domain=manifest.data_domain,
        payload_format=manifest.payload_format,
        storage_ref=manifest.storage_ref,
        emitted_at=utc_now(),
        trace_id=trace_id,
        attributes=attributes or {},
    )
