# ADR 0004: Enforce Pseudonymization Before Retrieval And Inference

## Status

Accepted

## Context

The platform processes sensitive health data and aims to support
retrieval-assisted and multimodal inference without leaking raw
identifiers through prompts, embeddings, or general application code.

Relying on ad hoc filtering at prompt time is brittle. The more durable
approach is to define a structural privacy boundary before data reaches
core inference pathways.

## Decision

Enforce pseudonymization and structural transformation before health
data reaches core prompts, retrieval artifacts, and inference-facing
logic.

This boundary is represented in the current repo by
[`adapters/pseudonymizer.py`](/Users/julianbuccat/Projects/Dev/myHealth/adapters/pseudonymizer.py)
and reinforced by verifier and instruction-layer guidance.

## Consequences

### Positive

- privacy becomes an architectural property instead of an afterthought
- prompts and retrieval artifacts operate on safer context
- core modules can be reasoned about without raw identifier handling
- the system better reflects healthcare-grade boundary thinking

### Negative

- pseudonymization logic becomes a critical boundary that must be
  correct
- some downstream use cases may require careful handling of source-to-
  pseudonym traceability
- debugging can be harder when raw identifiers are intentionally absent

## Evidence

- [pseudonymizer.py](/Users/julianbuccat/Projects/Dev/myHealth/adapters/pseudonymizer.py)
- [privacy-and-phi-boundary.md](/Users/julianbuccat/Projects/Dev/myHealth/.github/instructions/repo/privacy-and-phi-boundary.md)
- [copilot.md](/Users/julianbuccat/Projects/Dev/myHealth/.github/instructions/global/copilot.md)
