# Patient Edge Privacy Intent

## Status

Future product intent; no patient-device runtime currently exists.

## Principle

Routine patient understanding should remain close to patient-controlled
data. Raw longitudinal records should not require centralized transfer
for bounded, low-consequence tasks.

## Intended Boundary

- encrypted local vault with device-bound key protection
- explicit authentication for application access
- local retrieval, deterministic analytics, and supported open-weight
  inference
- local de-identification before an optional disclosure package
- consent-scoped export with clear destination and purpose
- safe offline behavior and secure model/update provenance
- deletion that covers local sources, caches, and derived artifacts

Local execution is not secure merely because it is local. Shared or
compromised devices, backups, notification surfaces, crash reports, and
model supply-chain integrity remain part of the threat model.

## Federated Learning

Federated learning is not required for local inference. It is a separate,
optional population-learning plane and should not be an MVP dependency.

If later adopted, participation should be explicit opt-in and separable
from product use. Secure aggregation, update clipping, differential
privacy, minimum cohort sizes, poisoning defenses, and auditable model
release criteria would be required. Model updates must not be assumed
non-identifying merely because raw records remain on-device.

## Non-Goals

- autonomous diagnosis or treatment recommendations
- mandatory cloud synchronization of the local vault
- mandatory participation in shared-model improvement
- treating a patient device as a clinically managed endpoint
