# NLP De-Identification Architectural Intent

## Status And Scope

This document records future product intent. No production NLP
de-identification pipeline is currently implemented.

The boundary applies to unstructured clinical text before it reaches
retrieval artifacts, embeddings, prompts, analytics, or general-purpose
logs. It complements structured pseudonymization; it does not replace
access control or source-data protection.

## Intent

`myHealth` should remove or consistently transform identifying text
while preserving clinically meaningful context needed for approved
uses. The pipeline should favor privacy when confidence is insufficient.

The minimal flow is:

```text
restricted source text
  -> deterministic normalization
  -> identifier candidate detection
  -> contextual classification
  -> redact or pseudonymize
  -> privacy validation
  -> approved de-identified artifact
```

Direct identifiers, dates, locations, contact details, record numbers,
provider/facility references, and identifying free-text spans should be
considered according to the governing policy. Transformations must avoid
changing clinically material facts such as measurements, medication
doses, negation, temporal order, and relationships between events.

## Minimal Technical Boundary

- Use Python for normalization, NLP inference, policy application, and
  validation. Initial implementation should remain a small isolated
  adapter/worker rather than a new distributed platform.
- Prefer deterministic rules for well-structured identifiers and a
  locally controlled clinical NER component only where context is
  required.
- Do not send raw clinical text to an external model or API merely to
  de-identify it.
- Use stable, scoped replacement tokens only when approved workflows
  need entity continuity; otherwise redact.
- Keep re-identification mappings, if any, in a separately authorized
  boundary and never in embeddings, prompts, logs, or queue payloads.

SQL is relevant only for metadata and control state: artifact IDs,
pseudonymous subject references, source lineage, policy/model versions,
review status, and validation outcomes. Raw text and reversible mapping
values should not be duplicated into general relational audit tables.

## Safety And Quality Gates

An artifact should remain quarantined when validation fails or residual
identifier risk exceeds policy. Evaluation should include:

- recall by identifier category, with emphasis on false negatives
- preservation of clinically material meaning
- deterministic regression fixtures using synthetic data
- adversarial formats, OCR noise, misspellings, and multilingual text
- policy and model-version traceability
- sampled human review for high-risk document classes

Logs and metrics should describe counts, categories, versions, latency,
and outcomes without reproducing source spans.

## Deferred Decisions

- identifier taxonomy and jurisdiction-specific safe-harbor rules
- Python NLP library and clinical NER model
- confidence thresholds and human-review sampling rates
- reversible pseudonymization versus irreversible redaction by use case
- execution topology; local and centralized options will be evaluated
  separately
