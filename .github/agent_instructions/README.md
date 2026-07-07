# Legacy Agent Instructions

Routing: Read this index only for compatibility with older local
workflows that still reference `.github/agent_instructions/`.

This directory is retained as a legacy compatibility path. The active
checked-in instruction namespace is now:

```text
.github/copilot-instructions.md
  -> .github/instructions/*.instructions.md
  -> .github/agents/*.agent.md
```

Do not add new canonical instructions here. Migrate durable repository
rules into `.github/instructions/*.instructions.md` and specialist
personas into `.github/agents/*.agent.md`.

Optional local overlays may still exist here during transition:

```text
.github/agent_instructions/global
.github/agent_instructions/repo/local.md
```

These paths are ignored and non-canonical. Repository work must remain
safe when they are absent.
