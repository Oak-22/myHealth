---
description: "Use when touching PHI/PII boundaries, prompts, logs, audit flows, inference context, queue payloads, or persistence surfaces."
applyTo: "docs/**/*.md, .github/**/*.md, scripts/hooks/**/*.sh"
---
# Privacy and Compliance Guardrails

Privacy should be enforced structurally through system boundaries, not
treated as an afterthought at prompt time.

- Do not add logging that includes names, direct identifiers, raw payload bytes, or sensitive source content.
- Queue payloads should carry references and metadata, not raw clinical payload data.
- Use pseudonymous subject references in docs, evaluation specimens, and
  future code comments.
- Treat privacy boundary changes as architectural changes and align docs when behavior changes.
- Preserve the distinction between development-agent customization and product inference controls.
- Pseudonymization and structural transformation should happen before
  data reaches core inference logic.
- Clinical workflows are restrained by default. Preclinical molecular
  and genomic workflows may be more autonomous only when operating on
  public, synthetic, non-PHI, or pseudonymized payloads.
- Do not promote preclinical molecular analysis into patient-facing
  clinical guidance without explicit review, provenance, and
  pseudonymized linkage boundaries.

Development agents and product LLMs are different systems. Development
agents edit code and docs and must not receive PHI. Product LLMs may
later reason over health context only through backend-managed,
pseudonymized, audited inference workflows.
