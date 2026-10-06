# Hybrid Inference Routing Intent

## Status

Future product intent; no routing implementation currently exists.

## Boundary

Inference should be routed by consequence and answerability, not only by
whether the requester is a patient or clinician.

```text
Could failure plausibly change diagnosis, treatment, urgency,
medication use, or whether the patient seeks care?

No  -> prefer the patient-controlled local lane
Yes -> use the governed clinical lane
```

Outpatient use is the primary local-first case, but custody is the
stronger boundary: patient-controlled processing remains the patient
lane wherever it occurs, and professionally governed decision support
remains the clinical lane even when the patient is remote.

## Patient-Controlled Lane

- local encrypted health-data custody
- deterministic calculations and safety rules
- local retrieval and open-weight inference where device capacity allows
- routine organization, explanation, journaling, and visit preparation
- purpose-specific disclosure only after consent

## Governed Clinical Lane

- minimum-necessary, provenance-linked context
- higher-capability inference through a private clinical boundary
- evidence and uncertainty surfaced to the clinician
- clinician confirmation before consequential action
- no automatic promotion of model output into diagnosis or treatment

## Routing Outcomes

Routing selects permitted compute; it does not guarantee an answer.
Either lane may answer, qualify, request information, abstain, or
escalate. Urgent safety checks should use deterministic policy before
LLM generation where practical.

## Deferred Decisions

- supported patient devices and local model sizes
- exact clinical-risk taxonomy and routing thresholds
- offline behavior and context-package format
- evaluation requirements for each permitted task
