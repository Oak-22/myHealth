---
description: "Always load for repository tasks so agents apply token-cost control, context compaction, model-size choice, and session-splitting behavior before planning or implementation."
---
# Token Economics

## Purpose

Define durable agent behavior for controlling token cost and reducing
throwaway work during repository tasks.

This instruction is intentionally always-on for repository work. Do not
scope it to specific file globs; session efficiency and context hygiene
apply before deciding which files are relevant.

## Always-On Cost Levers

- Prefer the smallest capable model for the task.
- Keep context lean and task-relevant.
- Reduce throwaway work by planning before implementing non-trivial
  changes.

## Pre-Plan Session Check

Before planning or implementing, check whether the new request is
unrelated to the active thread.

If unrelated, ask a short explicit question first:

`This looks unrelated to the current thread. Do you want to start a new chat for better token efficiency?`

Behavior:

- If user says yes, stop and ask them to continue in a fresh session.
- If user says no, proceed in current session with scoped context.

## Session Boundaries

Start fresh sessions when switching between unrelated workstreams, such
as:

- implementation vs architecture strategy
- feature work vs review-only work
- docs curation vs debugging
- release readiness vs new feature development

## Context Hygiene

- Load only instructions and files relevant to the current request.
- Compact long conversations when the topic remains the same.
- Prefer a fresh session over compaction when topic shifts.

## Guardrails

- Do not drop privacy, contract, or architecture constraints solely to
  reduce tokens.
- Keep required ADR and boundary constraints in scope for decisions.
