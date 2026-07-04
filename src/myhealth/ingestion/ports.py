"""Abstract ports for the asynchronous ingestion boundary."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Protocol

from myhealth.ingestion.schemas import (
    IdempotencyDecision,
    IngestionManifest,
    IngestionStatus,
    IngestionTaskEvent,
    PreSignedUpload,
    ProcessingResult,
    StorageObjectRef,
)


class StorageKeyFactory(Protocol):
    """Creates raw-vault object keys for registered uploads."""

    def build_key(self, manifest: IngestionManifest) -> str:
        """Return an object key for the registered manifest."""


class ObjectStoragePort(ABC):
    """Storage facade for raw payload upload and retrieval."""

    @abstractmethod
    def allocate_raw_object(self, manifest: IngestionManifest) -> StorageObjectRef:
        """Allocate the final raw object location for a manifest."""

    @abstractmethod
    def create_presigned_upload(
        self,
        storage_ref: StorageObjectRef,
        content_type: str,
        expires_in: timedelta,
    ) -> PreSignedUpload:
        """Create a direct-to-object-store upload capability."""


class IdempotencyStorePort(ABC):
    """DynamoDB-style idempotency boundary for distributed retries."""

    @abstractmethod
    def reserve(self, transaction_id: str, manifest: IngestionManifest) -> IdempotencyDecision:
        """Reserve a transaction before parsing or replay an existing one."""

    @abstractmethod
    def mark_completed(self, transaction_id: str, result: ProcessingResult) -> None:
        """Persist a completed result for future replay decisions."""

    @abstractmethod
    def mark_failed(self, transaction_id: str, result: ProcessingResult) -> None:
        """Persist a failed result for audit and retry policy decisions."""


class ManifestRepositoryPort(ABC):
    """Canonical repository for pre-parse ingestion manifests."""

    @abstractmethod
    def create(self, manifest: IngestionManifest) -> None:
        """Persist the registered manifest."""

    @abstractmethod
    def update_status(
        self,
        manifest_id: str,
        status: IngestionStatus,
        reason: str | None = None,
    ) -> None:
        """Update durable workflow status."""


class EventPublisherPort(ABC):
    """Message broker facade for worker task publication."""

    @abstractmethod
    def publish(self, event: IngestionTaskEvent) -> None:
        """Publish an ingestion task or follow-up event."""
