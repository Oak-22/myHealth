# myHealth Agent Pack

This directory owns the runtime-neutral source manifests for myHealth agents.
The manifests are product assets; rendering and validation are supplied by the
Agentic Engineering Platform's agent control plane.

The Architecture Steward is the first portability pilot. Generate or verify
its GitHub custom-agent installation from a sibling platform checkout:

```sh
python3 ../agentic-engineering-platform/platform/agent-control-plane/scripts/render_portable_agent.py \
  --manifest agent-pack/agents/architecture-steward/agent.toml \
  --runtime github \
  --output .github/agents/architecture-steward.agent.md
```

Append `--check` to validate the installed file without changing it.
