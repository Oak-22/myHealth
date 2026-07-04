# Copilot Instructions

Routing: GitHub Copilot should read this file fully before repo changes to converge on the shared instruction tree and report loaded files.

This is the checked-in discovery adapter for the repository instruction
system. The repo intentionally does not expose a root-level `AGENTS.md`
entrypoint because this project has privacy-sensitive clinical and
preclinical boundaries.

Before making code, documentation, data-layout, architecture, or Git
changes, load the `.github/agent_instructions/` tree and report what was
loaded.

## Discovery Path

```text
.github/copilot-instructions.md
  -> .github/agent_instructions/agent.md
  -> .github/agent_instructions/README.md
  -> .github/agent_instructions/global/README.md
  -> .github/agent_instructions/repo/README.md
  -> task-relevant instruction files
```

## Required Load Sequence

1. Read `.github/agent_instructions/agent.md`.
2. Read `.github/agent_instructions/README.md`.
3. Read `.github/agent_instructions/global/README.md` when the local
   symlink exists.
4. Read `.github/agent_instructions/repo/README.md`.
5. Read task-relevant files referenced by those indexes.

## Routing Sentences

Instruction files may begin with a `Routing:` sentence. Use that
sentence to decide which optional task-relevant files need full loading;
the required load sequence above still applies before repository
changes.

## Required First Response Block

Start change-making turns with an instruction load report:

```md
Instruction Load Report

- [x] `.github/agent_instructions/agent.md`
- [x] `.github/agent_instructions/README.md`
- [x] `.github/agent_instructions/global/README.md` (Local symlink, when present)
- [x] `.github/agent_instructions/repo/README.md`
- [x] `path/to/relevant-instruction.md` (Trigger: brief reason)
- [ ] `path/to/skipped-instruction.md` (Skipped: brief reason)
```

If repo instruction files cannot be read, say which files were
unavailable and continue only when the task can still be handled safely.
If the local global symlink is absent, report it as skipped and continue
with the checked-in repo instructions.

## Audit Boundary

The load report is an operational audit artifact. It should list files
read for the task, not expose hidden chain-of-thought or private
reasoning.
