# myHealth Agent Customizations

This repository now includes VS Code agent customizations under .github and workspace MCP settings under .vscode.

## What was scaffolded

- Custom agents: .github/agents
- File instructions: .github/instructions
- Workflow skills: .github/skills
- Reusable prompts: .github/prompts
- Workspace hooks: .github/hooks
- Hook scripts: scripts/hooks
- MCP server config: .vscode/mcp.json

## Your selected setup

- Agents: Tester, Security Expert, Compliance, Code Reviewer, Architecture Steward, Data Engineer, Documentation Curator
- Skills strategy: workflow-based
- Hook strictness: soft fail
- Hook events: PreToolUse, PostToolUse, Stop
- Validation stack in hooks: pytest, ruff, mypy, bandit, pip-audit (skips if tool missing)
- MCP targets: PostgreSQL and OpenAPI

## Skills vs prompts

- Skills are reusable multi-step workflows and can load scripts/resources.
- Prompts are single reusable task templates.
- Use skills for recurring procedures and prompts for quick repeat asks.

## Next actions in VS Code

1. Run MCP: Open Workspace Folder MCP Configuration and confirm .vscode/mcp.json is loaded.
2. Start and trust myhealthPostgres and myhealthOpenApi servers from MCP: List Servers.
3. Open Chat: Open Customizations to verify agents, skills, prompts, and hooks are discovered.
4. In Chat, select Code Reviewer as your active agent for day-to-day default behavior.

## Notes

- There is no documented setting that reliably pins a custom agent as default in all chat entry points; selecting Code Reviewer in chat keeps your workflow aligned with your chosen default role.
- Hook scripts are workspace-editable. Keep approvals enabled for edits to scripts/hooks if you want stricter governance.
