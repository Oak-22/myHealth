# ADR 0009: Sequence myHealth Development After Agentic Foundation Work

## Status

Accepted

## Context

`myHealth` is intended to become the applied product layer for a
privacy-sensitive, backend-centric health data and inference platform.
The repository already contains meaningful architecture, contract, ADR,
and agent-control scaffolding, but the next risk is not simply writing
more product code.

The higher-leverage dependency is the development harness itself:

- the agentic control-plane and instruction-template work
- the AgentOps and token-economics observability work
- the RPI workflow that keeps research, planning, and implementation
  separate enough to review
- the feedforward and feedback mechanisms that constrain agent-assisted
  development before and after code changes

If `myHealth` product development proceeds before those foundation
projects are stable enough, the repository is likely to accumulate
duplicated markdown, weak review loops, inconsistent agent behavior, and
implementation churn.

## Decision

Postpone substantial `myHealth` product implementation until two
foundation tracks are solid enough to support repeatable development:

1. Agentic harness/control-plane foundation
2. AgentOps and token-economics observability foundation

During this pause, `myHealth` work should focus on:

- clarifying architecture, contracts, ADRs, and agent-control behavior
- preserving existing source-of-truth documentation
- defining readiness criteria for the foundation tracks
- applying small, low-risk documentation or harness updates
- avoiding new product feature implementation unless it is needed to
  validate the harness itself

## Foundation Readiness Criteria

The agentic harness/control-plane track is ready when:

- the checked-in instruction, prompt, hook, and template patterns have a
  stable promotion path
- RPI behavior is documented and discoverable by repository-aware agents
- generated markdown has clear ownership rules and bloat controls
- feedforward and feedback mechanisms are explicit enough to reuse
  across project work

The AgentOps and token-economics track is ready when:

- the event and telemetry concepts needed by development agents are
  defined
- token-cost, latency, model-routing, and review-loop signals have an
  inspectable schema or working prototype
- the observability model can explain which agent workflows are costly,
  noisy, high-risk, or valuable
- myHealth can consume the observability discipline without becoming
  the place where the generic platform is designed

`myHealth` product development can resume when both tracks have enough
working shape to support a small end-to-end implementation slice with:

- a clear spec or plan
- constrained agent context
- visible token and workflow economics
- validation feedback
- a promotion path for durable lessons

## Consequences

### Positive

- reduces implementation churn in `myHealth`
- gives the product repository stronger development guardrails before
  sensitive health workflows expand
- keeps reusable harness and observability templates in their own
  foundation projects
- makes agent-assisted development itself observable and reviewable
- aligns implementation velocity with architecture and governance
  maturity

### Negative

- delays visible product features in `myHealth`
- requires discipline to avoid turning the pause into unbounded
  meta-work
- creates cross-repository dependency management overhead
- may require revisiting existing implementation assumptions once the
  foundation tracks mature

## Guardrails During The Pause

- Do not add new `myHealth` product features unless they validate a
  foundation mechanism or unblock source-of-truth alignment.
- Prefer work in the agentic control-plane and AgentOps/token-economics
  repositories when the artifact is reusable across projects.
- Promote only myHealth-specific decisions back into this repository.
- Keep privacy, ingestion, and architecture source-of-truth files
  current, but avoid speculative implementation detail.
- Treat substantial implementation requests as RPI planning candidates
  before writing code.

## Evidence

- [Agentic Harnessing Framework](../architecture/agentic_harnessing_framework.md)
- [Spec-Driven RPI instruction](../../.github/instructions/spec-driven-rpi.instructions.md)
- [Token Economics instruction](../../.github/instructions/token-economics.instructions.md)
- [Agent Context Routing instruction](../../.github/instructions/agent-context-routing.instructions.md)
