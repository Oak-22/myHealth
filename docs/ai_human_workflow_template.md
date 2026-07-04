# AI-Human Workflow Template

This repository contains workflow artifacts that are useful beyond a
single codebase and can be treated as reusable infrastructure for
AI-assisted development.

## Why These Artifacts Exist

AI-assisted development can improve short-term delivery speed, but it
can also reduce how much implementation reasoning remains in the
developer's head after the task is done.

That creates a real risk of knowledge atrophy:

- weaker retention of system behavior
- repeated rediscovery of past fixes
- slower onboarding for new contributors
- over-reliance on externalized reasoning

## Template Pattern

The reusable pattern in this repository separates workflow artifacts
into two categories:

- `.github/agent-instructions/`
  Operating guidance for human plus AI development
- `engineering_knowledge_base/`
  Learning artifacts derived from real engineering work

For portability, this repository also includes a copyable scaffold in
`templates/ai-human-workflow/`.

## myHealth Active Instruction Path

The active instruction path for this repository is not the template
scaffold. Agents should load:

1. `.github/copilot-instructions.md`
2. `.github/agent_instructions/agent.md`
3. `.github/agent_instructions/README.md`
4. `.github/agent_instructions/global/README.md` when the local symlink
   exists
5. `.github/agent_instructions/repo/README.md`
6. Task-relevant repo instruction files

`templates/ai-human-workflow/` remains a copyable scaffold for future
repositories or public template work.

In this local checkout, `.github/agent_instructions/global` is intended
to be an ignored symlink to
`/Users/julianbuccat/.config/agent_instructions/global`.
