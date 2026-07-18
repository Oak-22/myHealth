# myHealth: A Secure, Cloud-Enabled AI Healthcare Application

## Description 
myHealth is a personal health data and inference platform that ingests heterogeneous health-related data sources and enables retrieval-augmented multimodal reasoning through a thin application interface

## Problem
Healthcare platforms struggle to balance **real-time intelligence** with **privacy and compliance**. Data often remains siloed, insecure, or difficult to integrate across devices and providers. Patients want actionable insights, while organizations need strict HIPAA/GDPR compliance and auditability.

## Solution
myHealth delivers:
- **Seamless multi-source data ingestion** 
- **Secure cloud architecture** (AWS VPC-constrained, zero public internet, HIPAA-eligible services).
- **AI reasoning chatbot** with pseudonymized health records, providing Q&A, triage, and lifestyle recommendations.
- **Observability & governance** through auditable system telemetry, operational visibility, and compliance-oriented controls.
- **Dual-domain architecture** that keeps clinical workflows restrained
  and privacy-first while allowing more autonomous preclinical molecular
  and genomic computation in isolated worker boundaries.
- **Harness evaluation target mode** while the agentic control-plane and
  AgentOps token-economics foundations mature.

## Differentiation
- **Privacy by design**: PHI never embedded directly; redaction and pseudonymization before storage.
- **Hybrid data flows**: Wearables → Cloud Storage → Cloud DWH → Secure LLM inference.
- **Scalability path**: product implementation is deferred until the
  enabling harness and observability layers are ready.

## Target Users
- **Patients**: Daily health insights, triage support,
- **Clinics & providers**: Secure health data integration, risk scoring (cardiometabolic index), multimodal analysis.

## Documentation Layout

Repo-specific documentation lives directly in [docs](docs):

- [architecture](docs/architecture)
- [research alignment](docs/research/README.md)
- [product](docs/product)
- [data](docs/data)
- [adr](docs/adr)
- [notes](docs/notes)
- [runbooks](docs/runbooks)

Recommended starting points:

- [PRD](docs/product/prd.md)
- [System Architecture](docs/architecture/system_architecture.md)
- [System Spec](docs/architecture/system_spec.md)
- [Agentic Harnessing Framework](docs/architecture/agentic_harnessing_framework.md)
- [Technology Stack](docs/architecture/technology_stack.md)
- [Software Design Patterns Reference](docs/notes/software_design_patterns.md)
- [Non-Functional Requirements](docs/architecture/non_functional_requirements.md)
- [Data Model](docs/data/data_model.md)
- [Data Dictionary](docs/data/data_dictionary.md)
- [Ingestion Phase 1 Contracts](docs/contracts/ingestion_phase_1_contracts.md)
- [Workload Processing Spectrum](docs/notes/workload_processing_spectrum.md)
- [Code Pattern Scaffolding](docs/notes/code_pattern_scaffolding.md)
- [ADRs](docs/adr)
  - [ADR 0006: Event-Driven Service Isolation](docs/adr/0006_event_driven_service_isolation.md)
  - [ADR 0007: Dual-Domain Governance](docs/adr/0007_dual_domain_governance.md)
  - [ADR 0008: Python-First Server-Rendered UI](docs/adr/0008_server_rendered_python_first_ui.md)
  - [ADR 0009: Sequence myHealth Development After Agentic Foundation Work](docs/adr/0009_sequence_myhealth_after_agentic_foundation.md)
  - [ADR 0010: Convert myHealth To A Harness Evaluation Target](docs/adr/0010_convert_myhealth_to_harness_evaluation_target.md)
