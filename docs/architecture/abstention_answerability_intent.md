# Abstention And Answerability Intent

## Status

Future product intent; no calibrated abstention layer currently exists.

## Principle

`I do not know` is a valid product outcome in both patient and clinical
lanes. Escalation changes the available evidence, capability, and human
oversight; it must not convert uncertainty into false certainty.

Risk routing and answerability are independent decisions:

| Consequence | Answerability | Intended action |
| --- | --- | --- |
| low | sufficient | local answer |
| low | insufficient | clarify or abstain |
| high | sufficient | governed clinical synthesis |
| high | insufficient | defer with uncertainty preserved |

## Answerability Signals

The system should not trust model-reported confidence alone. A separate
decision layer should consider:

- retrieval relevance, completeness, and provenance
- missing required fields, dates, or units
- contradictions between sources
- agreement with deterministic validators and tools
- instability across independent reasoning attempts
- task distribution, consent, and safety-policy boundaries
- calibrated performance on representative evaluation data

## Response Contract

Each substantive result should resolve to one disposition:

- `answer`
- `answer_with_limits`
- `ask_for_information`
- `abstain`
- `escalate`

An abstention should state what is supported, what is uncertain, why it
is uncertain, what information could resolve it, and the safest next
action. Reason codes and evidence references should be machine-readable
without copying PHI into general logs.

## Evaluation

Track error among answered queries, correct and unnecessary abstention,
harm-weighted false answers, escalation quality, and calibration under
data or model drift. Coverage alone is not a success metric.
