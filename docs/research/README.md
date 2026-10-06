# Research Alignment

## Purpose

This index records research that materially informs `myHealth`
architecture. A citation belongs here only when it maps to a concrete
system boundary, requirement, or evaluation method. Research alignment
is not evidence of implementation, clinical validation, or regulatory
approval.

## Operator Responsibility

Human operators remain responsible for decisions and outcomes produced
through their use of AI. Increasing model capability does not transfer
professional authority, accountability, or duty of care to the model.

`myHealth` should therefore preserve:

- a named human decision owner for consequential workflows
- an explicit boundary between model output and authorized action
- evidence, provenance, limitations, and uncertainty at review time
- abstention and escalation without pressure to produce an answer
- an auditable record of the model contribution and human disposition
- workflow design that supports meaningful review rather than automatic
  or ceremonial approval

Responsibility is shared by system designers, deployers, and operators
according to their control over the workflow. A user-facing disclaimer
does not compensate for unsafe routing, poor evidence, or automation
beyond an operator's ability to supervise.

## Current Research Basis

### Healthcare LLM Abstention

Presacan, O., Nik, A., Ojha, J. et al. “When silence is safer: a review
and decision-theoretic framework for LLM abstention in healthcare.”
*npj Digital Medicine* (2026).
[DOI: 10.1038/s41746-026-02882-1](https://doi.org/10.1038/s41746-026-02882-1)

The paper distinguishes uncertainty-driven abstention from safety-driven
abstention and frames answering versus withholding as a decision under
uncertainty and potential harm.

| Research concept | `myHealth` architectural translation |
| --- | --- |
| Uncertainty-driven abstention | independent answerability evaluation |
| Safety-driven abstention | consequence-based inference routing |
| Potential harm | lane-specific thresholds and human deferral |
| Refusal limitations | extrinsic evidence, policy, and validation checks |
| Clinical-dialog evaluation | harm-weighted error and abstention metrics |

## Architecture Links

- [Abstention and answerability](../architecture/abstention_answerability_intent.md)
- [Hybrid inference routing](../architecture/hybrid_inference_routing_intent.md)
- [Confidential clinical inference](../architecture/confidential_clinical_inference_intent.md)
- [Consent lifecycle](../architecture/consent_lifecycle_intent.md)

## Citation Standard

Future entries should include the primary source, the specific finding
used, its architectural translation, and any important limitation. Do
not use journal reputation as a substitute for evaluating applicability.
