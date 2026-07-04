# Agent Instruction Control Plan

Routing: Read this file fully for work involving agent instructions, templates, control-plane docs, workflow scaffolds, or public/private instruction layering.

## Purpose

This plan keeps the AI-agent instruction system coherent without making
agent scaffolding the center of the repository.

The product architecture is the source of truth. Agent instructions are
a lightweight control surface that helps development agents respect that
architecture, especially privacy and domain-boundary rules.

## Canonical Active Path

The active checked-in instruction path is:

```text
.github/copilot-instructions.md
  -> .github/agent_instructions/
```

`.github/copilot-instructions.md` is the checked-in adapter for agents
that understand GitHub/Copilot-style repository instructions.

The repository intentionally does not expose a root-level `AGENTS.md`.
For this privacy-sensitive project, agent controls should remain inside
`.github/` rather than presenting a broad public root entrypoint.

## Local Global Symlink

Reusable cross-repository instructions are loaded through an ignored
local symlink:

```text
.github/agent_instructions/global
  -> /Users/julianbuccat/.config/agent_instructions/global
```

This symlink is intentionally not a checked-in dependency. If it is
absent, agents should report it as skipped and continue with the
checked-in repo instruction layer.

## Deprecated / Inactive Paths

- `.github/agent-instructions/`
  Older hyphenated instruction path from the first adoption pass.
- `templates/ai-human-workflow/.github/agent-instructions/`
  Copyable public-template scaffold, not an active instruction source.

Do not add new active instructions to the deprecated path. If useful
content exists there, migrate it into `.github/agent_instructions/`.

## Public Vs Local Guidance

Checked-in files must be portable and safe for the public repository.
They may describe optional local overlays, but they must not require
machine-specific paths.

Allowed optional local overlays:

```text
.github/agent_instructions/repo/local.md
```

These are ignored and optional. Agents may load them when present and
relevant, but repository work must remain safe when they are absent.

## Template Policy

The `templates/ai-human-workflow/` directory is retained as a reusable
scaffold. It should not be treated as a live instruction path for this
repo.

When template guidance improves, either:

- update the template scaffold for future reuse, or
- migrate the relevant rule into `.github/agent_instructions/`

Do not leave two active versions of the same instruction.

## MyHealth-Specific Implementation Expectations

Instruction files should reflect the current system:

- dual-domain governance
- restrained clinical workflows
- more autonomous preclinical molecular/genomic workflows over public,
  synthetic, non-PHI, or pseudonymized payloads
- event-driven service isolation
- Health Gateway Service
- Clinical Ingestion Worker
- Genomic Annotation Worker
- storage-first ingestion
- idempotent transaction assignment before parsing
- S3 raw vault references
- SQS task events
- DynamoDB workflow/idempotency state
- Redis read projections
- PostgreSQL canonical truth
- strict privacy and PHI boundaries
- Python-first server-rendered UI
- no authored custom JavaScript or TypeScript
- HTMX only as optional progressive enhancement

## Minimalism Rule

Do not add agent scaffolding merely because a template supports it.
Prefer the smallest checked-in instruction set that:

- gives supported IDE agents a clear `.github/` entrypoint
- protects privacy and PHI boundaries
- points to current architecture docs
- prevents duplicate active instruction paths

If an instruction would duplicate an ADR or architecture document,
prefer linking to the source document instead of restating it in full.

## Maintenance Checklist

When changing architecture or implementation:

1. Update docs and ADRs when decisions change.
2. Update `.github/agent_instructions/repo/myhealth-context.md` when the
   system shape changes.
3. Update `.github/agent_instructions/repo/ingestion-contracts.md` when
   ingestion contracts or worker boundaries change.
4. Update `.github/agent_instructions/repo/privacy-and-phi-boundary.md`
   when privacy, logging, prompt, or data-flow boundaries change.
5. Update `.github/agent_instructions/repo/myhealth-context.md` when the
   locked frontend stack changes.
6. Keep `.github/copilot-instructions.md` aligned with
   `.github/agent_instructions/`.
7. Keep templates marked as scaffolds, not active instructions.
