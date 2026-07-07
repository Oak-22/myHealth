# Legacy Repository Instructions

Routing: Read this file only when a workflow still references the legacy
`.github/agent_instructions/repo/` path.

Repository-specific instruction content has moved to:

- `.github/instructions/myhealth-context.instructions.md`
- `.github/instructions/privacy-and-compliance.instructions.md`
- `.github/instructions/ingestion-contracts.instructions.md`
- `.github/instructions/agent-context-routing.instructions.md`

Keep this directory as a compatibility shim while older tooling catches
up. Do not add new canonical repository rules here.

Optional ignored local overlay:

- `.github/agent_instructions/repo/local.md`
