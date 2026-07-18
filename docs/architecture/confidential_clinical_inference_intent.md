# Confidential Clinical Inference Intent

## Status

Future hardening intent; the repository contains no deployed inference
service or confidential-computing implementation.

## Existing Baseline

The existing [AWS private inference diagram](diagrams/aws_private_inference_architecture.png)
defines the intended network boundary:

- Fargate workload in a private subnet
- IAM task role and security group controls
- private Bedrock access through a VPC interface endpoint
- private S3 access through an S3 gateway endpoint

This remains the baseline. Confidential computing extends it by
protecting selected data while in use; it does not replace VPC, IAM,
encryption, minimization, or application authorization.

## Intended Clinical Boundary

High-consequence inference should use:

- consent-authorized, minimum-necessary context packages
- pseudonymization or de-identification where clinically safe
- encryption in transit and at rest with narrowly scoped keys
- isolated execution and workload attestation where the serving path
  supports it
- key release conditioned on approved workload identity or measurement
- no provider training on submitted clinical context
- explicit retention and deletion behavior
- provenance, model/version identity, and content-minimized audit events
- clinician review with uncertainty and abstention preserved

Attested CPU enclaves may protect preprocessing, context assembly, key
use, or policy enforcement. Confidential GPU execution is relevant when
`myHealth` controls a compatible model-serving environment. An external
frontier API can only provide guarantees exposed and contractually
supported by that provider; the application cannot independently attest
opaque provider internals.

## Homomorphic Computation

Fully homomorphic LLM inference is not part of the intended interactive
clinical path. Its complexity and compute cost are disproportionate to
the current product need.

Homomorphic encryption or secure multiparty computation may be
reconsidered later for narrow aggregate statistics or bounded
cross-institution calculations. Such use would require a separate ADR
and measured benefit over confidential computing and data minimization.

## Deferred Decisions

- managed Bedrock versus self-hosted confidential model serving
- enclave and confidential-GPU technologies
- attestation verifier, trust policy, and key hierarchy
- clinical context retention and inference service-level objectives
