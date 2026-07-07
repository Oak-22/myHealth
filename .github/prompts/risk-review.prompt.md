---
name: Risk Review
description: "Run a severity-first review using the Code Reviewer agent with emphasis on bugs, regressions, and privacy boundaries."
agent: "Code Reviewer"
argument-hint: "Optional scope: files, module, or recent diff"
---
Perform a risk-first review of the requested scope.

Requirements:
- Prioritize findings by severity.
- Include contract drift and missing-test risks.
- Include privacy/PHI boundary risks when relevant.
- Keep summary short and findings actionable.
