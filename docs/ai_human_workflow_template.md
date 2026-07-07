# AI-Human Workflow Template (Deprecated In myHealth)

This note remains as historical context.

## Deprecation Summary

`myHealth` no longer uses the legacy `.github/agent_instructions/`
compatibility tree or the local `templates/ai-human-workflow/` scaffold.

The active control-plane surface is artifact-typed:

1. `.github/copilot-instructions.md`
2. `.github/instructions/*.instructions.md`
3. `.github/agents/*.agent.md`
4. `.github/prompts/*.prompt.md`
5. `.github/skills/*/SKILL.md`
6. `.github/hooks/*.json`

## Template Ownership

Reusable control-plane template evolution is now tracked in the
dedicated repository:

- `ai_agent_instruction_control_plane`

Applied collaboration lessons and case studies are tracked in:

- `ai_human_engineering_collaboration_case_studies_and_best_practices`
