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

## Differentiation
- **Privacy by design**: PHI never embedded directly; redaction and pseudonymization before storage.
- **Hybrid data flows**: Wearables → Cloud Storage → Cloud DWH → Secure LLM inference.
- **Scalability path**: MVP runs on Fargate + FastAPI; roadmap includes Kubernetes for multi-tenant deployments.

## Target Users
- **Patients**: Daily health insights, triage support,
- **Clinics & providers**: Secure health data integration, risk scoring (cardiometabolic index), multimodal analysis.

## Documentation Layout

Repo-specific documentation lives directly in [docs](docs):

- [architecture](docs/architecture)
- [product](docs/product)
- [data](docs/data)
- [adr](docs/adr)
- [runbooks](docs/runbooks)

Recommended starting points:

- [PRD](docs/product/prd.md)
- [System Architecture](docs/architecture/system_architecture.md)
- [System Spec](docs/architecture/system_spec.md)
- [Technology Stack](docs/architecture/technology_stack.md)
- [Non-Functional Requirements](docs/architecture/non_functional_requirements.md)
- [Data Model](docs/data/data_model.md)
- [Data Dictionary](docs/data/data_dictionary.md)
- [ADRs](docs/adr)


