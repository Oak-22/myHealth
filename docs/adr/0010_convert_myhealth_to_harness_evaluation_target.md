# ADR 0010: Convert myHealth To A Harness Evaluation Target

## Status

Accepted

## Context

ADR 0009 postponed substantial `myHealth` product implementation until
the agentic harness/control-plane and AgentOps token-economics
foundations are solid enough to support repeatable, observable
development.

The repository still contained Python source stubs, ingestion tests, and
active Python-oriented instructions. Those artifacts created misleading
implementation gravity: future agents could treat partial code as the
current product truth and extend it before the underlying harness was
ready.

At the same time, workspace hook scripts are part of the agentic
harness. They sit between natural-language instructions and executable
enforcement, so they should remain even while product implementation
code is removed.

## Decision

Convert `myHealth` into a documentation, architecture, and harness
evaluation target until the enabling layers mature.

Remove active product implementation artifacts, including:

- source stubs under `src/`
- implementation tests under `tests/`
- non-hook utility scripts
- active language-specific implementation instructions

Keep agent-harness artifacts, including:

- `.github/agents/`
- `.github/instructions/`
- `.github/prompts/`
- `.github/skills/`
- `.github/hooks/`
- `scripts/hooks/`
- architecture, contract, ADR, product, and data docs

Hook scripts remain in scope because they provide explicit,
reviewable enforcement for the development harness.

## Evaluation Posture

`myHealth` can now be used as a target repository for harness
evaluation. Future evaluation slices may intentionally introduce small
violation specimens, such as:

- code or docs that violate nuanced instruction-layer rules
- prompts that attempt to bypass privacy or artifact-promotion
  boundaries
- changes that create markdown bloat or duplicate source-of-truth
  material
- implementation sketches that ignore RPI sequencing

Those specimens should be temporary, scoped, and clearly labeled as
evaluation material. Durable findings should be promoted into the
agentic control-plane or AgentOps/token-economics repositories when they
are reusable across projects.

## Consequences

### Positive

- removes false implementation gravity from partial code
- makes the repository a cleaner benchmark for agentic harness behavior
- keeps explicit hook enforcement available for evaluation
- preserves source-of-truth architecture and contract material
- makes future product implementation an intentional restart on top of
  stronger foundations

### Negative

- product code and automated product tests are temporarily absent
- existing implementation-oriented docs must be read as architectural
  intent rather than current runtime behavior
- some skills and hooks now validate harness shape instead of app
  correctness
- product implementation will require a fresh language and stack
  confirmation before code returns

## Guardrails

- Do not reintroduce product source code until ADR 0009 readiness
  criteria are satisfied or explicitly amended.
- Keep `scripts/hooks/` because hook scripts are harness enforcement.
- Treat language and framework choices as deferred product decisions,
  not active implementation commitments.
- Put reusable harness templates in `agent-instruction-control-plane`
  unless the behavior is specific to `myHealth`.
- Put reusable token and workflow observability concepts in
  `agentops-token-economics-observatory` unless the behavior is specific
  to `myHealth`.

## Evidence

- [ADR 0009](0009_sequence_myhealth_after_agentic_foundation.md)
- [Agentic Harnessing Framework](../architecture/agentic_harnessing_framework.md)
- [Spec-Driven RPI instruction](../../.github/instructions/spec-driven-rpi.instructions.md)
- [Token Economics instruction](../../.github/instructions/token-economics.instructions.md)
