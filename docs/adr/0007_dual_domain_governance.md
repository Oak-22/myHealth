# ADR 0007: Separate Clinical Safety From Preclinical Molecular Autonomy

## Status

Accepted

## Context

`myHealth` is expanding beyond a personal clinical health application
into a platform that can also handle pre-clinical molecular and genomic
payloads. These domains should not be governed identically.

Clinical workflows may involve PHI/PII, patient-facing explanations,
medical documents, wearable health records, lab reports, and inference
over personal longitudinal health context. This side of the system must
be restrained: privacy-first, auditable, pseudonymized before inference,
and conservative about autonomous behavior.

Pre-clinical molecular and genomic workflows may involve large VCF
files, ClinVar-style datasets, molecular matrices, coordinate mappings,
variant annotations, and research-style computation. This side of the
system has more room for autonomous processing, high-performance
computation, experimental analysis, and exploratory pipeline behavior,
provided it remains separated from clinical identity and PHI-bearing
contexts.

Without an explicit split, the repository can feel muddied: agent
instructions, clinical privacy rules, HPC-style molecular workflows, and
LLM inference controls appear to compete for the same architectural
center.

## Decision

Adopt a dual-domain governance model:

- **Clinical Domain**: restrained, privacy-first, patient-context
  workflows.
- **Preclinical Molecular Domain**: more autonomous, high-compute,
  research-style workflows over non-PHI or pseudonymized molecular and
  genomic payloads.

Both domains share the storage-first ingestion backbone:

```text
register input
  -> assign idempotent transaction ID
  -> issue S3 pre-signed upload
  -> validate object event
  -> publish queue task
  -> private worker processing
```

The domains diverge after routing:

- Clinical tasks route to the Clinical Ingestion Worker and restrained
  inference pathways.
- Molecular/genomic tasks route to the Genomic Annotation Worker and
  analytical/HPC-style pipelines.

## Clinical Domain Rules

- Treat clinical payloads as sensitive by default.
- Do not put PHI/PII in queue events, logs, prompts, tests, or general
  application traces.
- Pseudonymize or structurally reduce clinical context before inference.
- Keep patient-facing LLM behavior bounded by retrieved, approved,
  provenance-aware context.
- Prefer human-reviewable outputs and conservative explanation over
  autonomous decision-making.
- Treat weakened privacy, provenance, or audit boundaries as
  architectural regressions.

## Preclinical Molecular Domain Rules

- Permit more autonomous pipeline behavior for non-PHI, synthetic,
  public, or pseudonymized molecular/genomic payloads.
- Allow heavier compute profiles, specialized dependencies, batch
  processing, and exploratory annotation workflows inside private worker
  boundaries.
- Keep molecular/genomic computation isolated from clinical identity
  systems unless an explicit pseudonymized linkage contract exists.
- Record provenance, source version, reference build, annotation source,
  and confidence metadata for derived results.
- Do not promote research-style output into patient-facing clinical
  guidance without a clinical review boundary.

## Agent And LLM Boundary

Agent scaffolding in this repository is an engineering control surface,
not part of the product inference layer.

There are two different LLM contexts:

- **Development agents** help edit code and docs. They must respect repo
  privacy rules and should not receive PHI.
- **Product LLMs** may later reason over health context only through
  backend-managed, pseudonymized, audited inference workflows.

The repository has not contaminated the product LLM boundary merely by
including agent instructions. The product LLM boundary has not been
built yet. However, instruction scaffolding should stay lightweight and
must not obscure the domain architecture.

## Consequences

### Positive

- clarifies why clinical and preclinical workflows need different
  autonomy levels
- preserves strong privacy and restraint for patient-facing clinical
  workflows
- keeps molecular/genomic experimentation viable without overburdening
  it with clinical UI constraints
- reduces confusion between development-agent controls and product LLM
  inference controls
- creates a clear explanation for why the repo contains both health-app
  and HPC-style platform elements

### Negative

- introduces an additional governance distinction to maintain in docs,
  tests, and instructions
- requires careful routing so clinical and molecular payloads do not
  silently cross trust boundaries
- requires future product decisions before research-style results can be
  surfaced as patient-facing insights

## Implementation Guidance

- Keep `DataDomain.CLINICAL`, `DataDomain.BIOMETRIC`, and
  `DataDomain.DOCUMENT` on the restrained clinical path unless explicitly
  pseudonymized.
- Keep `DataDomain.PRECLINICAL_MOLECULAR` and `DataDomain.GENOMIC` on
  the autonomous molecular path when payloads are public, synthetic, or
  pseudonymized.
- Add explicit routing tests when domain routing is implemented.
- Keep agent instructions minimal and focused on repo safety, not as a
  replacement for product architecture docs.

## Evidence

- [system_architecture.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_architecture.md)
- [system_spec.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_spec.md)
- [ingestion_phase_1_contracts.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/contracts/ingestion_phase_1_contracts.md)
