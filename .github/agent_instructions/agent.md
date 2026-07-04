# General AI Agent Instructions

Routing: Read this file fully for repository work where general AI-agent collaboration, safety, code, documentation, architecture, or review behavior matters.

## Purpose

Use this instruction file as portable guidance for AI-assisted work
across repositories.

The goal is to help agents behave like careful engineering
collaborators: read context first, preserve user intent, make focused
changes, and leave the workspace easier to understand than it was found.

## Working Principles

- Inspect the relevant files before proposing or making changes.
- Prefer the repository's existing patterns over new abstractions unless
  an ADR or task request explicitly changes the architecture.
- Keep edits scoped to the requested behavior or artifact.
- Preserve user-authored work and avoid reverting unrelated changes.
- Explain meaningful tradeoffs when a choice affects maintainability,
  public API, data shape, privacy boundary, or workflow semantics.
- Verify changes with the smallest useful command set.
- When architecture docs and implementation diverge, surface the
  mismatch and update both when the task calls for it.

## Safety And Privacy

Treat every repository as if it may contain sensitive context.

- Do not expose secrets, credentials, tokens, private paths, or personal
  data in generated artifacts.
- Avoid copying private local configuration into public-facing files.
- Keep reusable global guidance separate from repo-specific rules.
- Put project-specific architecture, deployment, domain, and privacy
  constraints in the repository-local instruction layer.

## Code Changes

When editing code:

- Prefer local helper functions and existing module structure.
- Add comments only where they clarify non-obvious intent.
- Avoid unrelated refactors while fixing a narrow issue.
- Preserve semantic field order in human-reviewed outputs when order
  helps readers understand the workflow.
- Use structured parsers or APIs instead of ad hoc text manipulation
  when the file format supports it.
- Add focused tests when adding contracts, state transitions, parsing
  boundaries, idempotency behavior, or queue/event shapes.

## Documentation Changes

When editing documentation:

- Keep the document's existing voice and section rhythm.
- Preserve meaning while improving clarity, ordering, and scanability.
- Use examples that match the repository's own domain.
- Avoid turning temporary observations into durable documentation unless
  the user explicitly wants them curated.
- Distinguish source artifacts, derived artifacts, validation outputs,
  manifests, events, and read projections clearly.

## Review Stance

When asked for a review, prioritize:

- bugs or behavior regressions
- data-shape or schema mismatches
- missing validation or tests
- confusing artifact boundaries
- stale documentation that teaches the wrong workflow
- privacy, PHI, or pseudonymization boundary regressions

Lead with findings. Keep summaries secondary.

## Local Vs Public Instructions

Global instructions should be portable and non-personal.

Repository-specific private overlays belong in a local ignored layer,
such as `.github/agent_instructions/repo/local.md`.

Reusable private/global instructions may be loaded through the ignored
`.github/agent_instructions/global` symlink. Checked-in repo-specific
files must remain useful when that symlink is absent.
