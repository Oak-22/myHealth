# Agent Instructions

This directory contains agent-facing instruction assets for this
repository.

## Structure

- `global/`
  Reusable agent guidance that is not specific to project `myHealth`
- `repo/`
  `myHealth`-specific instruction models and operating constraints

## How To Use It

- Start here to understand the instruction layout
- Read `global/README.md` for reusable guidance categories
- Read `repo/README.md` for `myHealth`-specific models and boundaries
- Load only the subject files relevant to the current task

## Keep Out Of `.github/instructions/`

- `knowledge_base/`
  Human-facing shared knowledge such as personal learning notes,
  incident reports, and coding drills
- `docs/`
  Repo-owned human documentation such as architecture notes, ADRs, and
  runbooks

That material should stay outside the agent instruction tree.

