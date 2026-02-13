# myHealth: Architecture

## Overview
The myHealth platform is built on a **secure, cloud-native microservices architecture** designed for healthcare-grade compliance. Core design principles:
- **Zero public internet exposure** (all inference within VPC).
- **PHI/PII segregation** at storage, embedding, and inference stages.
- **Composable services** for scalability (containers, serverless, orchestration).

## Front-End
- **streamlit** with x for chatbot integration

## Back-End
- **FastAPI (Python)** for REST endpoints (e.g., `/api/healthkit/sync`).
- **PostgreSQL / DynamoDB** for structured data storage.
- **DBT + SQL validation** for ensuring relational data quality post-ingestion.

## AI/LLM Layer
- **LLM Proxy inside VPC**: User-facing chatbot for interactive queries on user health data
- **LangGraph** for memory orchestration and runtime guardrails.
- **Vector DB (Qdrant)** for user-specific chatbot memory

## Cloud & Data Flow
**Data from User → Insights**:
```
[User Prompt / HealthKit Data]
      ↓
[Streamlit frontend]
      ↓ fetch()
[AWS API Gateway]
      ↓
[Lambda]
      ↓
[FastAPI service / Vector DB / Bedrock Inference]
      ↓
[Secure Response to Frontend]
```

**Data from Wearables → Database**:
```
[Apple Watch / iPhone]
      ↓ HealthKit
[iOS App Wrapper / React Native Bridge]
      ↓ Secure HTTPS JSON POST
[FastAPI Backend /api/healthkit/sync]
      ↓
[Database (Postgres / DynamoDB)]
      ↓
[Web UI Health Summary + Trends]
```

## Security & Compliance
- **AWS VPC with private subnets** for inference and DBs.
- **Lake Formation + Glue** for data lineage and RBAC.
- **CloudTrail, Config, Audit Manager** for continuous compliance.
- **IAM least privilege** for all resources.
- **Pre-embedding pseudonymization** for health records (names → patient_0001).

## Observability
- **Prometheus + Grafana** dashboards for app + infra metrics.
- **CloudWatch + HealthOmics** for system + data event tracking.

## Deployment & Orchestration
- **Docker** for all microservices.
- **AWS Fargate** for serverless container execution (MVP).
- **Kubernetes (EKS)** for multi-tenant, large-scale deployments (Phase 2).
- **Airflow** for orchestrating ETL and health data workflows.
