---
name: privacy-boundary-check
description: "Audit PHI/PII and pseudonymization boundaries. Use before merge when prompts, logs, queue payloads, workers, or tests touch sensitive data paths."
argument-hint: "List changed files or describe the workflow being audited"
---
# Privacy Boundary Check

## When to use
- Logging, prompts, persistence, queue payloads, or worker adapters changed.
- Clinical ingestion or cross-domain data flows are modified.

## Procedure
1. Inspect changed files for direct identifier leakage risk.
2. Verify queue payloads carry references and metadata, not raw sensitive content.
3. Confirm pseudonymized references in tests and docs.
4. Validate alignment with repo privacy instructions.
5. Summarize violations by severity and propose precise remediations.

## Output format
- Severity-ranked findings
- Violated boundary
- Exact remediation actions
