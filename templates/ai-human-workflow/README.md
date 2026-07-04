# AI-Human Workflow Template

This directory is a reusable template for workflow artifacts that sit
next to product code in AI-assisted repositories.

## Purpose

The template formalizes three ideas:

- AI agents need explicit operating context
- teams need durable places to capture learning from real work
- workflow artifacts should be portable across repositories

## Template Contents

- `.github/agent-instructions/`
  Reusable and repository-specific agent guidance
- `engineering_knowledge_base/`
  Learning and incident capture derived from real engineering work

## Adoption Guidance

Use this template as checked-in repository structure.

If a team also maintains centralized canonical assets, those may be
linked into a live repository through symlinks, but the portable
template should remain copyable without machine-specific dependencies.

## myHealth Usage Note

In this repository, this directory is a reusable scaffold only. The
active instruction system is rooted under `.github/`:

- `.github/copilot-instructions.md`
- `.github/agent_instructions/`

Do not treat `templates/ai-human-workflow/.github/agent-instructions/`
as an active instruction source for `myHealth`.
