# Copilot Instructions

This is the checked-in discovery adapter for repository-aware agents in
`myHealth`.

Before making code, documentation, data-layout, architecture, or Git
changes, load the relevant checked-in instruction files and report what
was loaded. Keep the report to operational file paths and routing
reasons; do not expose private reasoning.

## Active Context Surface

```text
.github/copilot-instructions.md
  -> .github/instructions/*.instructions.md
  -> .github/agents/*.agent.md when a specialist role is relevant
  -> .github/prompts/*.prompt.md when an explicit reusable prompt fits
  -> .github/skills/*/SKILL.md when an explicit skill workflow fits
```

## Required Baseline

For repository work, load only the task-relevant files under
`.github/instructions/`.

Always include `.github/instructions/token-economics.instructions.md`
for repository tasks so agents apply session-efficiency behavior.

Common routing:

- Python, tests, service modules, or ingestion-adjacent implementation:
  `.github/instructions/myhealth-python.instructions.md`
- Architecture, stack, service boundaries, or system docs:
  `.github/instructions/myhealth-context.instructions.md`
- PHI/PII, prompts, logs, audit flows, inference context, queue payloads,
  or persistence surfaces:
  `.github/instructions/privacy-and-compliance.instructions.md`
- Upload registration, object references, queue events, idempotency,
  parser strategies, ingestion workers, or ingestion docs:
  `.github/instructions/ingestion-contracts.instructions.md`
- Token-cost control, context compaction, model-size selection, or
  session-splitting behavior:
  `.github/instructions/token-economics.instructions.md`
- Agent instructions, prompts, skills, templates, workflow scaffolds, or
  public/private context layering:
  `.github/instructions/agent-context-routing.instructions.md`
- Project overlay notes, promotable design framing, or possible future
  ADR/architecture/contract material:
  `docs/notes/README.md` and, when present, relevant local overlays
  under `.github/local/overlays/implementation-overlays/`

## Specialist Agents

Specialist personas live in `.github/agents/*.agent.md`. Use them when
the task naturally calls for a role such as architecture stewardship,
data engineering, testing, compliance, security, documentation curation,
or risk-first code review.

## Local Overlays

Local overlays are optional, ignored, and non-canonical:

```text
.github/local/overlays/*.instructions.md
```

Load local overlays only when present and relevant. They may shape local
workflow behavior, but they must not define product requirements,
architecture decisions, PHI policy, ingestion contracts, or runtime
behavior.

## Source Of Truth

Canonical product truth remains in:

- `docs/architecture/`
- `docs/contracts/`
- `docs/adr/`
- service-level code and tests

Project overlay notes may live as gitignored local overlays. In that
location, they are already promoted local agent-control material. They
remain non-canonical from the repository/product perspective until
promoted into one of the canonical documentation layers, checked-in
agent instructions, or code/tests.
