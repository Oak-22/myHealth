# Agent Instructions

Routing: Read this index fully to understand the instruction layer model and choose relevant global or repo files.

This directory contains instruction assets that support disciplined
AI-human collaboration in this repository.

## Layer Model

- `agent.md`
  General AI agent working principles.
- `global/`
  Ignored local symlink to reusable guidance shared across local
  repositories.
- `repo/`
  Repository-specific context, boundaries, and operating constraints.

`agent.md` defines general collaboration behavior. Global guidance
supplies default decision rules when the local symlink exists. Repo
guidance supplies local facts and constraints that shape or override
those defaults.

## Active Instruction Tree

This is the active instruction tree for `myHealth`.

`.github/agent_instructions/global` should be a local symlink to:

```text
/Users/julianbuccat/.config/agent_instructions/global
```

That symlink is intentionally ignored so the public repository does not
depend on a machine-specific path.

The older `.github/agent-instructions/` path and the
`templates/ai-human-workflow/` scaffold are not active instruction
sources.

## Usage

Start here, then load only the instruction files relevant to the task.
Use each file's `Routing:` sentence as the first-pass trigger for
whether the full file should enter context.

For architecture, ingestion, privacy, data-contract, or worker-boundary
work, load the repo files listed in `.github/agent_instructions/repo/`.
