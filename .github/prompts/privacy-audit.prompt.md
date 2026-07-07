---
name: Privacy Audit
description: "Run a privacy/compliance audit using the Compliance agent for PHI boundaries, logs, prompts, and queue payloads."
agent: "Compliance"
argument-hint: "Describe changed area or provide target files"
---
Audit the requested scope for privacy and compliance boundary adherence.

Checklist:
- No direct identifiers or raw sensitive data in logs/events/tests.
- Queue payloads carry references and metadata only.
- Pseudonymization boundary remains explicit.
- Architecture and policy docs stay aligned.
