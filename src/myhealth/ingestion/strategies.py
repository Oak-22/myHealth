"""Parser strategy contracts for private ingestion workers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from myhealth.ingestion.schemas import (
    JobType,
    NormalizedRecordBatch,
    ParseContext,
    PayloadFormat,
    SourceSystem,
)


class IngestionStrategy(ABC):
    """Parses one source/format family after idempotency is reserved."""

    source_system: SourceSystem
    payload_format: PayloadFormat
    job_type: JobType

    @abstractmethod
    def parse(self, payload: bytes, context: ParseContext) -> NormalizedRecordBatch:
        """Parse payload bytes into normalized records and provenance."""


class StrategyRegistry:
    """Runtime lookup for parser strategies without if/else chains."""

    def __init__(self, strategies: Iterable[IngestionStrategy] = ()) -> None:
        self._strategies: dict[tuple[SourceSystem, PayloadFormat, JobType], IngestionStrategy] = {}
        for strategy in strategies:
            self.register(strategy)

    def register(self, strategy: IngestionStrategy) -> None:
        key = (strategy.source_system, strategy.payload_format, strategy.job_type)
        self._strategies[key] = strategy

    def resolve(
        self,
        source_system: SourceSystem,
        payload_format: PayloadFormat,
        job_type: JobType,
    ) -> IngestionStrategy:
        key = (source_system, payload_format, job_type)
        try:
            return self._strategies[key]
        except KeyError as exc:
            raise LookupError(f"No ingestion strategy registered for {key}") from exc
