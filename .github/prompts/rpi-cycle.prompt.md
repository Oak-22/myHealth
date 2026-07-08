---
name: RPI Cycle
description: "Run a lightweight Research-Plan-Implement loop before changing myHealth code, docs, contracts, or agent-control artifacts."
agent: "Architecture Steward"
argument-hint: "Describe the feature, workflow, documentation, or harness change"
---
Use the lightweight RPI loop for the requested scope.

Research:
- Load only the relevant repository instructions and source-of-truth
  files.
- Identify known constraints, unknowns, and any privacy or contract
  boundaries.

Plan:
- Propose the smallest coherent change.
- Name files to edit and validation to run.
- Avoid creating new markdown unless it has a durable owner layer.

Implement:
- Make the scoped change.
- Update source-of-truth docs, tests, prompts, or instructions only when
  behavior changed.
- Report validation evidence, remaining risks, and any artifact that
  should later be promoted or deleted.
