# Agent Instructions

This directory contains IDE-facing instruction assets used to support
human plus AI collaboration in this repository.

## Layer Model

- `global/`
  Reusable guidance intended to apply across repositories
- `repo/`
  Repository-specific context, boundaries, and operating constraints

## Navigation

Use this README to understand the directory layout, then move to the
layer that matches the task:

- read `global/README.md` for reusable cross-project guidance
- read `repo/README.md` for repository-specific guidance
- load only the subject files needed for the current task

## Placement Rules

Put content in `global/` when it is reusable outside this repository,
such as general coding guidance, formatting rules, or interface design
principles.

Put content in `repo/` when it depends on the local codebase, domain,
architecture, privacy model, or repository-specific workflows.

## Notes

The `global/` directory may be locally symlinked to a canonical
cross-repository configuration path. That implementation detail should
not change how this tree is read: start at this overview, then follow
the layer-specific READMEs.
