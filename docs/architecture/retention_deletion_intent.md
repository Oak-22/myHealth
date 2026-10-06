# Retention And Deletion Architectural Intent

## Status And Scope

This document records future product intent. No end-to-end retention or
verified deletion workflow is currently implemented.

## Intent

Every persisted data class should have an owner, purpose, retention
rule, deletion trigger, and verifiable disposition. Indefinite retention
must be an explicit exception rather than a default.

Retention policy should cover both source data and derivatives:

- raw uploads and normalized records
- extracted text, chunks, embeddings, and model inputs
- analytical features, projections, and caches
- workflow state, logs, exports, and backups

Derived artifacts must not silently outlive the source or authorization
that permits their use.

## Required Metadata

Canonical records and artifact manifests should carry or resolve to:

- sensitivity and data-class classification
- source and pseudonymous subject references
- governing retention-policy version
- creation, expiration, and legal-hold timestamps where applicable
- lineage to downstream artifacts
- deletion state and last disposition result

PostgreSQL is the likely source of truth for policy assignments,
lineage, holds, and deletion workflow state. Object and analytical
stores may enforce expiry natively, but their results must reconcile to
the authoritative workflow.

## Deletion Workflow

Deletion should be an idempotent, restart-safe workflow:

```text
requested -> authorized -> deleting -> verifying -> completed
                    \-> blocked_by_hold
                    \-> failed
```

The workflow should:

1. authenticate and authorize the request or policy trigger
2. freeze creation of new derivatives for the affected scope
3. resolve source records and lineage-linked artifacts
4. delete or irreversibly render them inaccessible in each store
5. invalidate caches, retrieval indexes, and pending work
6. verify disposition and record content-free evidence

Revoked access and completed deletion are distinct states. The system
must not claim deletion merely because an item is hidden from a user.

## Guarantees And Limits

- New interactive access should cease once an authorized deletion
  enters execution.
- Active stores and derived indexes should have explicit completion
  objectives defined per data class.
- Backup expiry should follow a documented schedule; restoration
  procedures must not silently resurrect deleted data.
- Legal or safety holds should block only the governed scope and expose
  a reason without leaking sensitive content.
- Audit evidence should retain identifiers and outcomes needed to prove
  disposition, not deleted clinical content.

Cryptographic erasure may support stores encrypted with appropriately
scoped keys, but it is not a universal substitute for deletion and
requires a separate key-management design.

## Deferred Decisions

- retention periods and deletion service-level objectives by data class
- backup, disaster-recovery, and legal-hold schedules
- key hierarchy and cryptographic-erasure applicability
- jurisdiction-specific exceptions
- centralized, local-first, or federated deletion coordination
