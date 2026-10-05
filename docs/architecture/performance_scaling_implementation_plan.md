# Backend Performance, Scale-Out, and Caching Implementation Plan

## Status

Projected implementation plan. This is future product work; the current
repository is a harness evaluation target and does not yet contain an active
backend deployment.

## Current Findings

- Loader.io is not currently configured or referenced.
- New Relic is not currently configured or referenced.
- Prometheus and Grafana are the current observability intent.
- Redis is already the intended read-optimized projection and short-lived
  cache layer.
- AWS Fargate, Lambda, SQS, PostgreSQL/pgvector, and DynamoDB are documented
  as the intended runtime and persistence components.

## Goals and Guardrails

Performance work should establish measurable behavior for the Health Gateway,
ingestion APIs, retrieval, dashboard reads, and asynchronous workers without
using real PHI. Loader.io traffic must use synthetic fixtures and a dedicated
non-production environment. New Relic telemetry must apply the same PHI
minimization and retention controls as all other operational telemetry.

Initial targets should be agreed before implementation; proposed starting
targets are:

| Area | Initial target |
|---|---|
| Read/API p95 latency | < 500 ms for non-inference endpoints |
| Write/API p95 latency | < 750 ms, excluding asynchronous work |
| Error rate under target load | < 1% |
| Queue processing | No sustained backlog growth at expected peak |
| Cache behavior | Hit ratio measured per endpoint; no stale canonical writes |
| Scale-out | Add capacity without changing API behavior or data correctness |

Inference latency should be measured separately because model-provider time is
an external dependency.

## Projected Implementation Sequence

### 1. Establish the baseline

- Define representative synthetic workloads for authentication, dashboard
  reads, ingestion initiation, retrieval, and chat/inference orchestration.
- Add request IDs, correlation IDs, endpoint timing, status code, payload-size,
  database-query, cache, and queue metrics.
- Record baseline throughput, p50/p95/p99 latency, error rate, CPU, memory,
  database connections, slow queries, Redis hit/miss rates, and queue age.
- Add a performance test data reset/seed process so runs are repeatable.

### 2. Add New Relic backend observability

- Instrument the Health Gateway and workers with New Relic APM/OpenTelemetry,
  subject to the final vendor/security review.
- Capture service maps, transaction traces, dependency timing, error
  analytics, deployment markers, and infrastructure/container metrics.
- Configure attribute scrubbing and allowlists so PHI, prompts, document text,
  tokens, and raw identifiers never enter traces or logs.
- Keep Prometheus/Grafana for platform metrics and dashboards where useful;
  define ownership to avoid conflicting alerts.
- Create alerts for p95 latency, error rate, saturation, queue age, database
  pool exhaustion, cache failures, and task retry/dead-letter growth.

### 3. Introduce the Nginx edge layer

- Place Nginx (or an AWS-managed equivalent where appropriate) in front of
  the gateway for TLS termination/integration, connection handling, request
  size limits, compression, timeouts, and rate limiting.
- Do not cache authenticated or PHI-bearing responses at the shared edge.
- Route long-running ingestion and inference work asynchronously; enforce
  bounded upstream timeouts and return job/status references.
- Load-test Nginx limits and confirm forwarded headers, request IDs, and audit
  context are preserved.

### 4. Implement scale-out

- Keep the Health Gateway stateless so multiple Fargate tasks can run behind a
  load balancer.
- Store sessions, idempotency, rate-limit counters, and workflow state in the
  documented managed stores rather than local container memory.
- Scale gateway tasks on CPU/memory plus request latency and in-flight work.
- Scale ingestion and analytics workers from SQS depth, oldest-message age,
  task duration, and failure rate.
- Set minimum/maximum capacity, health checks, graceful shutdown, retry
  budgets, and dead-letter handling before enabling autoscaling.
- Validate PostgreSQL connection-pool limits and Redis capacity before raising
  task counts; scale-out must not simply move the bottleneck to the database.

### 5. Implement and validate caching

- Use Redis for dashboard projections, ingestion-status projections, and
  short-lived retrieval/session data as already documented.
- Define an owner, key format, TTL, invalidation event, maximum value size,
  and authorization scope for every cache entry.
- Never treat Redis as canonical clinical truth; writes commit to PostgreSQL
  and invalidate or refresh affected projections.
- Measure hit ratio, stale-read rate, eviction rate, memory use, latency, and
  behavior during Redis failure.
- Add protection against cache stampedes (request coalescing or bounded
  refresh) and verify tenant/patient isolation in keys and authorization.

### 6. Run Loader.io performance testing

- Create a dedicated non-production environment with synthetic accounts,
  documents, telemetry, and embeddings.
- Start with smoke, baseline, load, stress, spike, soak, and recovery tests.
- Exercise the Nginx/load-balancer entry point and test realistic mixes rather
  than a single hot endpoint.
- Ramp traffic gradually, capture Loader.io results alongside New Relic and
  infrastructure metrics, and identify the first saturation point.
- Repeat after each scale-out or caching change and retain results by build,
  configuration, dataset size, and test profile.
- Add a release gate for agreed latency/error thresholds; never point Loader.io
  at production or expose real patient data to the service.

## Acceptance Criteria

The plan is complete when the team can reproduce a seeded test run, correlate
each Loader.io request with backend telemetry, demonstrate gateway and worker
scale-out, verify cache correctness and failure behavior, and document capacity
limits plus rollback procedures. Thresholds should be finalized from baseline
measurements and product SLO decisions before production launch.

## Dependencies and Decisions

- Confirm whether Nginx is required as a self-managed proxy or whether an AWS
  managed edge/load-balancing service satisfies the same controls.
- Approve New Relic data residency, retention, access, and PHI-scrubbing
  configuration.
- Select the Loader.io plan and establish IP allowlisting, test windows, and
  synthetic-data ownership.
- Decide whether Prometheus/Grafana and New Relic are complementary or whether
  one becomes the primary alerting system.
