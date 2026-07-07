# Project Overlay Notes

This directory documents the promotion model for project overlay notes
in `myHealth`.

The active note bodies currently live as promoted local overlays under:

```text
.github/local/overlays/implementation-overlays/
```

Those files are the final local promoted state for agent-control
overlays. They may later be promoted again into repo-canonical ADRs,
architecture docs, contract docs, checked-in agent instructions, or
implementation plans.

They sit between private learning material and canonical project truth:

```text
engineering_knowledge_base/
  private learning capture, development reflections, and habit formation

.github/local/overlays/implementation-overlays/
  promoted local project overlays and agent-control posture

docs/notes/
  checked-in index for the overlay model

docs/architecture/
docs/contracts/
docs/adr/
  canonical system truth, integration contracts, and decisions
```

## How To Use These Notes

Agents may load local project-note overlays when the task touches the
overlay subject area. Use them as project-relevant design overlays: they
can shape questions, implementation posture, review criteria, and
promotion proposals.

Do not treat a local overlay as canonical product behavior until the
relevant idea is promoted into `docs/architecture/`, `docs/contracts/`,
`docs/adr/`, checked-in `.github/instructions/`, or code/tests.

## Promotion Targets

- Promote to `docs/adr/` when the note implies a durable architecture
  decision or tradeoff.
- Promote to `docs/architecture/` when the note describes system shape,
  service boundaries, data flow, or operational topology.
- Promote to `docs/contracts/` when the note defines integration
  behavior, payload shape, state transition rules, or compatibility
  expectations.
- Promote to `.github/instructions/` when the note defines repeatable
  agent behavior or review posture.
- Promote to code/tests only when the architecture or contract impact is
  clear enough to implement.

## Current Local Overlay Themes

- `agent-control-plane-convergence` was promoted out of local overlays
  as a dedicated external case study:
  `ai_human_engineering_collaboration_case_studies_and_best_practices/case_study_03_agent_control_plane_convergence.md`
- `clever-hans.instructions.md`
  Mechanistic-interpretability-inspired guidance for avoiding
  shortcut-learning failures in BioML-style agent systems. In this
  project, it frames generated ML or molecular hypotheses as untrusted
  until constrained by deterministic validation and contextual review.
- `code-pattern-scaffolding.instructions.md`
  Maps non-functional requirements to code-level design patterns and
  likely module locations.
- `data-structures-algorithms-reference.instructions.md`
  Connects data structure and algorithm choices to workload shape,
  privacy boundaries, and service contracts.
- `implementation-maturity.instructions.md`
  Defines project-facing implementation posture for CI/CD discipline,
  PR quality, git hygiene, DSA evidence, and promotion behavior.
- `implementation-overlays-index.instructions.md`
  Indexes local implementation overlays at the same level and clarifies their
  role as implementation-informing local agent-control material.
- `software-design-patterns.instructions.md`
  Captures system and code pattern tradeoffs for a privacy-sensitive
  health platform.
- `workload-processing-spectrum.instructions.md`
  Defines when work belongs in request-response paths, clinical
  ingestion workers, telemetry analytics, or genomic/molecular workers.

## Relationship To Personal Learning Notes

Use `engineering_knowledge_base/personal_learning_notes/foundations/`
for private learning notes: what was learned, why it mattered, and which
habits or mental models should be reinforced during development.

Use `.github/local/overlays/implementation-overlays/` for project-facing local
overlays: ideas that have already been promoted out of scratch notes
into durable local agent posture and may later be promoted into
canonical repository guidance.
