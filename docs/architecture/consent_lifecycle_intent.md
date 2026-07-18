# Consent Lifecycle Architectural Intent

## Status And Scope

This document records future product intent. No consent service or
product enforcement code is currently implemented.

Consent is an authorization input, not a substitute for authentication,
legal basis, or clinical safety review. The same rules should apply
regardless of whether a future workload runs in a private cloud, on a
user device, or across federated participants.

## Intent

`myHealth` should make consent explicit, scoped, versioned, revocable,
and enforceable at every sensitive use boundary.

A consent grant should identify:

- the pseudonymous subject and granting principal
- the approved purpose and data categories
- permitted actions and recipients
- effective and optional expiration timestamps
- the policy and disclosure version presented to the user
- provenance for how the decision was captured

Consent should default to denied when a required grant is missing,
expired, ambiguous, or cannot be evaluated.

## Lifecycle

The minimum lifecycle is:

```text
draft -> active -> expired
             \-> revoked
             \-> superseded
```

- Activation requires an authenticated, attributable decision.
- Material scope changes create a new version rather than mutating the
  prior decision.
- Revocation blocks new governed processing immediately at authorization
  boundaries and starts downstream cleanup where policy requires it.
- Historical decisions remain auditable without retaining unnecessary
  sensitive payload content.

## Enforcement Boundaries

Consent should be checked before:

- ingestion from an optional connected source
- retrieval of governed health context
- creation of embeddings or other derived artifacts
- product inference over governed context
- secondary analytics, research, export, or third-party disclosure

Long-running work should carry a consent-decision reference, not raw
consent or PHI in queue messages. Workers must revalidate authorization
before consequential writes or disclosures so revocation can stop stale
work.

## Minimal Persistence Intent

PostgreSQL is the likely system of record for consent decisions,
versions, scopes, and state transitions. Records should use pseudonymous
subject references and append-only decision history. Read models or
caches may accelerate checks but must not become authoritative and must
be invalidated on revocation.

Audit events should record decision identifiers, policy versions,
actors, timestamps, and outcomes without copying clinical content.

## Deferred Decisions

- jurisdiction-specific legal bases and age/delegation rules
- consent vocabulary and data-category taxonomy
- emergency-access and break-glass policy
- UX and identity-proofing mechanisms
- centralized, local-first, or federated enforcement topology
