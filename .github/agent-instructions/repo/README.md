# Repo Instruction Models

This folder contains **project-specific agent instructions** for
`myHealth`.

Think of these files as focused conceptual models inside the project,
not as generic global instructions.

## Current Models

- `myhealth-context.md`
  Broad product and system context for `myHealth`
- `privacy-and-phi-boundary.md`
  Privacy, pseudonymization, and PHI-boundary expectations

## Scope

This folder is for `myHealth`-specific agent guidance only.

Keep here:

- project architecture and system context
- domain-specific constraints
- privacy and security boundaries specific to `myHealth`
- repo-local workflows and conventions

Do not keep here:

- reusable cross-repo writing rules
- generic Python or interface guidance
- human-facing notes, incident reports, or coding drills

## Boundary

If an instruction is reusable across unrelated repositories, it should
not live here. It belongs in `../global/` instead.
