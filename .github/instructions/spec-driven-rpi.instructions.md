---
description: "Use when turning ideas into research, plans, implementation tasks, specs, harness templates, or durable agent-control artifacts."
applyTo: "docs/**/*.md, .github/**/*.md, scripts/hooks/**/*.sh"
---
# Spec-Driven RPI

## Purpose

myHealth uses a lightweight Research-Plan-Implement loop to keep
agent-assisted work intentional, traceable, and small enough to review.

This adapts the useful parts of spec-driven development to the existing
repository shape: product truth stays in `docs/architecture/`,
`docs/contracts/`, `docs/adr/`, and checked-in harness artifacts;
agent-control behavior stays in `.github/`.

## Scope Mapping

- Ask scope maps to Research.
- Plan scope maps to Plan.
- Agent scope maps to Implement.

Do not skip directly to implementation when the request changes product
behavior, service boundaries, privacy posture, ingestion contracts, or
agent-control behavior.

## RPI Loop

Research:

- Identify the source-of-truth files that already govern the task.
- Capture unknowns as explicit questions or assumptions.
- Prefer evidence from current code, tests, ADRs, contracts, and
  architecture docs over speculative notes.

Plan:

- State the smallest coherent change.
- Name affected artifacts and validation commands.
- Keep temporary reasoning out of checked-in docs unless it defines a
  reusable rule, source-of-truth decision, or reviewable contract.

Implement:

- Make scoped changes that trace back to the plan.
- Update contracts, ADRs, architecture docs, instructions, prompts,
  skills, hooks, or future tests only when behavior or durable workflow
  changed.
- Summarize validation evidence and remaining risks.

## Spec Artifacts

Use a feature or workflow spec only when the change is large enough to
benefit from durable traceability. A useful spec names:

- user or operator outcome
- non-goals
- acceptance criteria
- source-of-truth references
- architecture, privacy, and contract constraints
- validation evidence expected before merge

Specs should be promoted into the existing documentation layers instead
of creating parallel truth. If a spec becomes canonical architecture,
contract, or agent behavior, move the durable content into the relevant
checked-in home and delete or archive the transient working version.

## Markdown Bloat Controls

- Do not commit raw chat transcripts, scratch reasoning, or duplicate
  summaries of existing docs.
- Prefer updating the nearest source-of-truth artifact over adding a new
  markdown file.
- Keep generated plans and research notes local unless they define a
  reusable workflow, a canonical decision, or validation evidence that a
  reviewer needs.
- When adding a new markdown file, state its owner layer in the file:
  architecture, contract, ADR, instruction, prompt, local overlay, or
  historical note.
- Delete or consolidate stale working artifacts when their durable
  content has been promoted.

## Harness Template Posture

Reusable LLM harness templates belong in the dedicated
`agent-instruction-control-plane` repository first. Promote only the
myHealth-specific behavior into this repository, and keep it aligned
with:

- `.github/copilot-instructions.md`
- `.github/instructions/agent-context-routing.instructions.md`
- `.github/instructions/token-economics.instructions.md`
- `docs/architecture/agentic_harnessing_framework.md`
