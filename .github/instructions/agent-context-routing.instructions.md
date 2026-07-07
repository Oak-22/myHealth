---
description: "Use when changing agent instructions, prompts, skills, templates, workflow scaffolds, project overlays, or public/private instruction layering."
applyTo: ".github/**/*.md, .github/**/*.json, docs/notes/**/*.md, engineering_knowledge_base/**/*.md"
---
# Agent Context Routing

## Purpose

This repository uses a small checked-in agent context surface plus
optional local overlays.

Product architecture remains the source of truth. Agent instructions are
a lightweight development control surface that helps agents respect the
architecture, especially privacy and domain-boundary rules.

## Active Checked-In Paths

- `.github/copilot-instructions.md`
  Repository entrypoint and routing adapter.
- `.github/agents/*.agent.md`
  Specialist agent personas.
- `.github/instructions/*.instructions.md`
  Durable repository operating rules.
- `.github/prompts/*.prompt.md`
  Reusable task prompts.
- `.github/skills/*/SKILL.md`
  Task-specific workflows.

## Token-Efficiency Baseline

The checked-in token-economics instruction is part of the durable agent
behavior surface:

- `.github/instructions/token-economics.instructions.md`

This baseline supports lean-context operation and requires a pre-plan
split-chat check when the next request appears unrelated to the active
thread.

## Legacy Compatibility Path

`.github/agent_instructions/` is retained as a compatibility shim for
older local workflows. Do not add new canonical instructions there.
When content needs to become active, migrate it into
`.github/instructions/*.instructions.md`.

## Public Vs Local Guidance

Checked-in files must be portable and safe for the public repository.
They may describe optional local overlays, but they must not require
machine-specific paths.

Allowed optional local overlays:

- `.github/local/overlays/*.instructions.md`
- `.github/agent_instructions/repo/local.md` during legacy transition
- `.github/agent_instructions/global` as an ignored local symlink during
  legacy transition

Agents may load local overlays when present and relevant. Repository
work must remain safe when they are absent. Local overlays may be
gitignored while still being promoted local agent-control state.

## Private Maturity Overlay

The private development maturity model belongs in the ignored
`engineering_knowledge_base/` tree. It may influence PR hygiene,
CI/CD discipline, git hygiene, learning loops, DSA evidence, and
promotion criteria.

It must not define product requirements, architecture decisions, PHI
policy, ingestion contracts, or runtime behavior. Promote stable,
collaborator-useful ideas through:

```text
engineering_knowledge_base/
  -> .github/local/overlays/ or docs/notes/
  -> docs/architecture/, docs/contracts/, or docs/adr/
```

## Project Overlay Notes

`docs/notes/README.md` documents the project overlay model. In this
checkout, the active project-note bodies may live as promoted local
overlays under:

```text
.github/local/overlays/implementation-overlays/
```

Treat local project overlays as promoted local agent-control material,
not as random scratchpad content.

Agents may load `.github/local/overlays/implementation-overlays/*.instructions.md`
when present and when a task touches the overlay subject area. Use them
to shape design questions, implementation posture, review criteria, and
promotion proposals.

They remain non-canonical from the repository/product perspective until
promoted into one of the durable checked-in layers:

- `docs/adr/` for architecture decisions
- `docs/architecture/` for system shape and service boundaries
- `docs/contracts/` for integration behavior and data/state contracts
- `.github/instructions/` for repeatable agent behavior
- code/tests for implemented behavior

## Maintenance Rules

- Keep `.github/copilot-instructions.md` aligned with the active
  checked-in paths.
- Prefer linking to canonical architecture, contract, and ADR docs over
  restating them in full.
- Do not leave two active versions of the same instruction.
- Keep templates marked as scaffolds, not active instruction sources.
