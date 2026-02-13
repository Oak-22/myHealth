# myHealth AI Agent Instructions

## Project Overview
**myHealth** is a secure, HIPAA-compliant healthcare platform that integrates wearable data (Apple HealthKit) with AI-powered insights. The system prioritizes **PHI/PII privacy** and operates within an AWS VPC with zero public internet exposure.

### Key Architectural Principles
- **Privacy-by-design**: PHI is never stored unencrypted; pseudonymization and redaction happen pre-embedding and pre-inference
- **Multi-agent memory segregation**: Separate vector DB namespaces for dev-agent, chatbot-agent, and shared knowledge
- **VPC-constrained inference**: All Bedrock calls happen inside private subnets; proxy filters sensitive data before reaching LLM
- **Layered security**: AWS Lake Formation, CloudTrail auditing, IAM least-privilege, and continuous compliance scanning

## Critical: Privacy-by-Structure (Not Filtering)

**This repository is architecturally designed to prevent PHI/PII exposure, not dependent on runtime filtering.**

Raw PHI/PII **never enters the codebase**. All pseudonymization and structural transformation happens **upstream in `adapters/pseudonymizer.py`** before data reaches core logic, prompts, or inference pipelines. This means:

- ✅ **Agents can freely explore, modify, and refactor all code** without exposure risk
- ✅ **Raw PHI never appears in the repository** — only pseudonymized clinical features
- ✅ **Security is architectural (by design), not operational (by filtering)**
- ✅ **Compliant with HIPAA's "minimize PHI exposure" principle** at the systems level

**For agents working on this codebase:**
- You can safely reason about, test, and improve all modules
- The boundary is explicit: `adapters/pseudonymizer.py` is where raw data transforms to safe context
- Core modules (`prompts/`, `verifier/`, backend services) work only with pseudonymized data
- No need for external filtering or proxy logic — the design itself prevents leakage

## Architecture at a Glance

### Data Flows
1. **Wearables → DB**: Apple Watch/iPhone → iOS app → FastAPI `/api/healthkit/sync` → PostgreSQL/DynamoDB
2. **User Query → AI**: User prompt → Vercel frontend → API Gateway/Lambda → FastAPI service → Bedrock (via VPC proxy) → Response
3. **Vector DB Memory**: Ingested health records are pseudonymized (e.g., "Jane Doe" → "patient_0001") before insertion into Qdrant

### Core Services
- **Frontend**: React.js + TailwindCSS PWA (optional Next.js for SEO/SSR)
- **Backend**: FastAPI (Python) with Rust optional for CV inference
- **AI Layer**: AWS Bedrock with Application Inference Profiles (Claude Sonnet 4/Opus 4), LangGraph for orchestration
- **Database**: PostgreSQL (primary) / DynamoDB, with DBT for validation
- **Observability**: Prometheus + Grafana dashboards, CloudWatch + HealthOmics

## Developer Workflows

### Local Development
- **Python dependencies**: FastAPI, boto3 (Bedrock client), LangGraph, Qdrant client
- **AWS credentials**: Requires `AWS_PROFILE` or env vars pointing to development account with Bedrock access
- **Bedrock model ID**: Use Application Inference Profile ARN (e.g., `arn:aws:bedrock:us-east-1:ACCOUNT:application-inference-profile/ID`)

### Testing AI Interactions
```python
# Example from invoke_bedrock.py (reference for agent interactions)
import boto3
client = boto3.client("bedrock-runtime", region_name="us-east-1")
response = client.converse(
    modelId="arn:aws:bedrock:...",  # AIP ARN
    messages=[{"role": "user", "content": [{"text": "..."}]}],
    inferenceConfig={"maxTokens": 512, "temperature": 0.7}
)
```

### Deployment
- **Containerization**: All services packaged as Docker images
- **MVP**: AWS Fargate (serverless containers)
- **Scale**: AWS EKS (Kubernetes) for multi-tenant Phase 2
- **Orchestration**: Airflow/Kestra for ETL and health data workflows

## Project-Specific Conventions

### PHI/PII Handling
- **NEVER** log raw patient names, SSNs, or health conditions in error messages
- **ALWAYS** pseudonymize health records before vector DB ingestion (use pattern: `patient_XXXX`)
- **LLM proxy must filter** prompts for PII; reject or redact before Bedrock calls
- Reference: [secure-claude-proxy-llm-copilot-ext.md](../secure-claude-proxy-llm-copilot-ext.md)

### Vector DB Organization
- **dev-agent namespace**: System docs, architecture, code references
- **chatbot-agent namespace**: Pseudonymized patient health records, anonymized trends
- **shared-knowledge namespace**: HIPAA guidelines, clinical decision trees, nutrition data

### API Design
- Use `/api/healthkit/sync` pattern for data ingestion endpoints
- All responses must omit raw PII even in error responses
- Implement request signing with AWS IAM for service-to-service calls

### Naming Conventions
- Health metrics: snake_case (e.g., `heart_rate_avg`, `sleep_duration_minutes`)
- Pseudonymized IDs: `patient_XXXX`, `provider_XXXX`
- Bedrock resources: Use ARN format for Application Inference Profiles, not model IDs

## Integration Points

### AWS Bedrock (Claude Models)
- **Model Access**: Application Inference Profiles (AIP) provide cost-optimized access to Claude Sonnet 4 (default) and Opus 4 (higher reasoning)
- **Request Format**: Use `converse` API (supports multi-turn conversations with system prompts)
- **Guardrails**: LLM proxy inside VPC filters requests; never send raw health data

### Apple HealthKit
- Requires iOS app wrapper or React Native bridge
- Health data ingested via secure HTTPS POST to FastAPI backend
- Supported metrics: heart rate, sleep, steps, exercise, ECG, blood pressure

### Data Quality & Validation
- Use **DBT + SQL validation** post-ingestion to ensure relational integrity
- Check for missing timestamps, out-of-range values (e.g., HR > 300)
- Log validation errors with patient_ID (not name) for audit trail

## Common Patterns

### Error Handling
- Catch AWS service errors (e.g., Bedrock throttling, API Gateway timeouts)
- Return HTTP 422 with redacted error messages (e.g., "health data validation failed" not "John's HR invalid")
- Log full error with request ID to CloudWatch for debugging

### Scalability Considerations
- Fargate is suitable for MVP; plan EKS migration when multi-tenancy required
- Vector DB may need sharding by patient cohort at scale; Qdrant supports namespaces
- DynamoDB for high-throughput wearable sync; PostgreSQL for relational queries

## LLM Inference Pipeline (Privacy-Preserving)

The core feature: translating raw patient data into AI-driven insights while maintaining strict PHI/PII privacy.

**Architecture** (four-stage pipeline):
1. **Pseudonymizer** (`adapters/pseudonymizer.py`): MRN → patient_XXXXX, age bucketing, ICD codes only, structural aggregation
2. **Prompt Builder** (`prompts/clinical_templates.py`): System + user prompts with citation requirements and safety guardrails
3. **LLM Inference**: Bedrock AIP inside VPC (no public internet exposure)
4. **Output Verifier** (`verifier/output_verifier.py`): Scan for PHI leakage, validate citations, check plausible ranges, flag hallucinations

**Key insight**: Model receives *rich, meaningful clinical features* (trends, labs, codes) not redacted text. Deterministic pseudonymization enables patient tracking without leaking identifiers.

**Usage** (three-line minimal):
```python
pseudonymized = Pseudonymizer().pseudonymize_patient(raw_data, strict=True)
prompt = ClinicalPromptTemplates.patient_summary_and_concerns(pseudonymized)
verification = OutputVerifier().verify_output(llm_output, pseudonymized.data_sources)
```

See [LLM_INFERENCE_PIPELINE.md](../LLM_INFERENCE_PIPELINE.md) for full documentation, examples, and FastAPI integration patterns.

## Key Files & Reference
- Architecture overview: [myHealth_Architecture.md](../myHealth_Architecture.md)
- Executive summary: [myHealth_Executive_Summary.md](../myHealth_Executive_Summary.md)
- Bedrock integration reference: [invoke_bedrock.py](../invoke_bedrock.py)
- VS Code extension setup: [secure-claude-proxy-llm-copilot-ext.md](../secure-claude-proxy-llm-copilot-ext.md)
- **LLM Inference Pipeline**: [LLM_INFERENCE_PIPELINE.md](../LLM_INFERENCE_PIPELINE.md) ← Start here for privacy-preserving inference
- Python version contract: [python.instructions.md](../python.instructions.md)
- Interface/boundary patterns: [interface.instructions.md](../interface.instructions.md)

---

**When in doubt**: Prioritize **privacy**, **auditability**, and **data integrity** over feature velocity. HIPAA compliance is non-negotiable.
