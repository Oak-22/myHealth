# Legacy Agent Instruction Control Plan

Routing: Read this file only when maintaining compatibility with the
legacy `.github/agent_instructions/` path.

## Status

This file has been superseded by:

```text
.github/instructions/agent-context-routing.instructions.md
```

The active checked-in context surface is:

```text
.github/copilot-instructions.md
  -> .github/instructions/*.instructions.md
  -> .github/agents/*.agent.md
```

## Compatibility Rule

Keep `.github/agent_instructions/` available for older local workflows,
but do not add new canonical instructions here. When a rule needs to be
active for current agents, migrate it into `.github/instructions/`.

## Local Overlay Rule

Private or machine-specific guidance belongs in ignored local overlays,
for example:

```text
.github/local/overlays/*.instructions.md
.github/agent_instructions/repo/local.md
.github/agent_instructions/global
```

Local overlays may shape workflow behavior when relevant, but they must
not define product requirements, architecture decisions, privacy policy,
ingestion contracts, or runtime behavior.
