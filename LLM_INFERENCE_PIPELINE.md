# Privacy-Preserving LLM Inference Pipeline for myHealth

This scaffold implements a **deterministic, auditable, and compliant** pipeline for using Claude/Bedrock to provide health insights while maintaining strict PHI/PII privacy.

## Architecture Overview

```
Raw Patient Data (with PHI)
    ↓
[1. PSEUDONYMIZER]  adapters/pseudonymizer.py
    - Hash MRN → patient_XXXXX
    - Age bucketing (65-74, not 68)
    - Extract ICD codes, RxNorm codes (no descriptions)
    - Aggregate vital signs as trends, not timestamps
    ↓
Pseudonymized Patient Context (no PHI)
    ↓
[2. PROMPT BUILDER]  prompts/clinical_templates.py
    - System prompt (enforces safety & citations)
    - User prompt (fills clinical context)
    - Structured request for citations, confidence, assumptions
    ↓
LLM-Safe Prompt (ready for Bedrock)
    ↓
[3. LLM INFERENCE]  (Bedrock AIP in VPC, or stub for dev)
    - Bedrock converse() API
    - All comms inside private subnets
    - No raw PHI sent
    ↓
LLM Output (potentially with hallucinations, PHI leakage)
    ↓
[4. OUTPUT VERIFIER]  verifier/output_verifier.py
    - Scan for unredacted PHI (emails, SSNs, dates, names)
    - Validate citations reference actual source IDs
    - Check lab/vital values are plausible ranges
    - Flag prescriptive advice (prescribe vs. recommend)
    - Verify structured format (headings, confidence, citations)
    ↓
Verified & Redacted Output
    ↓
[5. AUDIT LOG]  (Encrypted CloudWatch, IAM-protected)
    - Request ID, pseudonym_id, source_mrn (audit trail)
    - Template used, verification passed/failed
    - Confidence score, human review required flag
    ↓
Safe Response to Frontend/Patient
```

## Key Design Decisions

### 1. Deterministic Pseudonymization
- MRN → `patient_XXXXX` via SHA256 hash (same MRN always produces same ID)
- Enables patient tracking across requests without leaking identifiers
- Age binned to 10-year ranges (avoids re-identification via age+sex+diagnosis)
- Medication codes (RxNorm) instead of brand names

### 2. Structured Clinical Context
- Model receives **rich, meaningful features**, not redacted text
- Example: "HbA1c 8.2%, passage_42" (structured) vs. "[REDACTED] glucose value" (useless)
- Trends instead of raw timestamps (e.g., "HR increased 12% over 7d")
- Provenance attached (passage IDs link back to source data)

### 3. Citations & Auditability
- Every claim must cite a source passage ID (e.g., `patient_00001:passage_42`)
- Invalid citations are flagged as hallucinations
- Full audit trail (request ID, source MRN, template, confidence) in encrypted logs

### 4. Post-LLM Validation (Rule Layer)
- No PHI leakage: regex scan for emails, SSNs, full dates, patient names
- Factual checks: heart rate 72 bpm ✓, HbA1c 8.2% ✓, but 350 bpm ✗
- Safety checks: forbid "prescribe X immediately" (must say "discuss with provider")
- Structure checks: require headings, numbered lists, confidence statements

## Modules

### `adapters/pseudonymizer.py`
Converts raw EHR/HealthKit data to pseudonymized clinical context.

**Key classes:**
- `Pseudonymizer`: Main transformation engine
  - `pseudonymize_patient(raw_patient, strict=True)` → `PseudonymizedPatient`
  - `to_llm_context()` → dict safe for LLM

**Example usage:**
```python
from adapters.pseudonymizer import Pseudonymizer

pseudo = Pseudonymizer(llm_mode="prod")
pseudonymized = pseudo.pseudonymize_patient(raw_patient_data, strict=True)
llm_context = pseudo.to_llm_context(pseudonymized)
# llm_context has NO source_mrn (audit field stripped)
```

### `prompts/clinical_templates.py`
Prompt templates that enforce safe, structured clinical reasoning.

**Key templates:**
- `patient_summary_and_concerns()` → clinicalreasoning + top 3 concerns
- `medication_review_prompt()` → drug interaction check
- `heart_health_check_prompt()` → cardiovascular risk assessment
- `system_prompt_for_clinical_assistant()` → prepended to all calls (privacy guardrails)

**Pattern:**
```python
from prompts.clinical_templates import ClinicalPromptRequest, ClinicalPromptTemplates

req = ClinicalPromptRequest(...)
system = ClinicalPromptTemplates.system_prompt_for_clinical_assistant()
user = ClinicalPromptTemplates.patient_summary_and_concerns(req)

# Send to Bedrock or LLM stub
response = bedrock_client.converse(
    modelId=AIP_ARN,
    messages=[
        {"role": "user", "content": [{"text": system + "\n\n" + user}]}
    ]
)
```

### `verifier/output_verifier.py`
Validates LLM output for compliance, factual correctness, and safety.

**Key methods:**
- `verify_output(llm_output, source_passage_ids, allow_redaction=True)` → `VerificationResult`

**Checks:**
- PHI leakage (email, phone, SSN, full dates, names)
- Citation validity (referenced passage IDs exist)
- Plausible ranges (HR 40-200 bpm, HbA1c 4-14%, etc.)
- Prescriptive advice (forbid "prescribe X"; require "discuss with provider")
- Structured format (headings, citations, confidence)

**Example:**
```python
from verifier.output_verifier import OutputVerifier

verifier = OutputVerifier()
result = verifier.verify_output(llm_output, source_passage_ids)

if result.is_valid:
    print(f"✓ Output approved, confidence {result.confidence_score:.2f}")
else:
    print(f"✗ Errors: {result.errors}")

if result.requires_human_review:
    # Escalate to clinician
    pass
```

## Running the Example

### Quick Test (Validates all modules load)
```bash
cd /Users/julianbuccat/Projects/Dev/myHealth
python3 test_modules.py
```

**Expected output:**
```
✓ Pseudonymizer imported
✓ ClinicalPromptTemplates imported
✓ OutputVerifier imported
✓ Pseudonymizer: patient_12345, age_bucket=60-69
✓ Prompt template generated (2850 chars)
✓ Verifier: valid=True, confidence=0.95
✓✓✓ All modules working correctly! ✓✓✓
```

### Full End-to-End Pipeline
```bash
python3 example_e2e_pipeline.py
```

**What it does:**
1. Takes synthetic raw patient data (with PHI: name, SSN simulation)
2. Pseudonymizes it (removes all PHI)
3. Builds a clinical prompt (structured context only)
4. Calls stub LLM (simulates Bedrock response)
5. Verifies output (checks for PHI leakage, plausible values, citations)
6. Logs audit entry (encrypted, internal only)

## Integration with FastAPI Backend

### Pattern: Chat/Query Endpoint
```python
from fastapi import FastAPI, HTTPException
from adapters.pseudonymizer import Pseudonymizer
from prompts.clinical_templates import ClinicalPromptRequest, ClinicalPromptTemplates
from verifier.output_verifier import OutputVerifier
import boto3

app = FastAPI()
pseudonymizer = Pseudonymizer(llm_mode=os.getenv("LLM_MODE", "dev"))
verifier = OutputVerifier()
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

@app.post("/api/chat/health-insights")
async def get_health_insights(patient_id: str, query_type: str = "summary"):
    """
    Get AI-powered health insights for a patient.
    
    Privacy flow:
    1. Fetch raw patient record (internal, encrypted)
    2. Pseudonymize (strip all PHI)
    3. Build prompt from pseudonymized data
    4. Call Bedrock (inside VPC, no raw PHI)
    5. Verify output (catch hallucinations, PHI leakage)
    6. Return safe response to frontend
    7. Log audit trail (encrypted, immutable)
    """
    
    # 1. Fetch raw record (internal only)
    raw_patient = get_patient_record_internal(patient_id)
    
    # 2. Pseudonymize
    try:
        pseudonymized = pseudonymizer.pseudonymize_patient(raw_patient, strict=True)
    except ValueError as e:
        # PHI detection failed; log and escalate
        log_security_event("PHI_DETECTION_FAILED", patient_id=None)
        raise HTTPException(status_code=422, detail="Data validation failed")
    
    # 3. Build prompt
    prompt_req = ClinicalPromptRequest(
        pseudonym_id=pseudonymized.pseudonym_id,
        age_bucket=pseudonymized.age_bucket,
        sex=pseudonymized.sex,
        comorbidities=pseudonymized.comorbidities,
        current_medications=pseudonymized.current_medications,
        vital_signs_summary=pseudonymized.vital_signs_summary,
        lab_results=pseudonymized.lab_results,
        device_metrics=pseudonymized.device_metrics,
        last_clinical_visit=pseudonymized.last_clinical_visit,
        known_concerns=pseudonymized.known_concerns,
        data_sources=pseudonymized.data_sources
    )
    
    system_prompt = ClinicalPromptTemplates.system_prompt_for_clinical_assistant()
    if query_type == "summary":
        user_prompt = ClinicalPromptTemplates.patient_summary_and_concerns(prompt_req)
    elif query_type == "medications":
        user_prompt = ClinicalPromptTemplates.medication_review_prompt(prompt_req)
    else:
        raise HTTPException(status_code=400, detail="Unknown query type")
    
    # 4. Call Bedrock (inside VPC, no public internet)
    try:
        response = bedrock.converse(
            modelId=os.getenv("BEDROCK_AIP_ARN"),
            messages=[{"role": "user", "content": [{"text": system_prompt + "\n\n" + user_prompt}]}],
            inferenceConfig={"maxTokens": 1024, "temperature": 0.7}
        )
        llm_output = response["output"]["message"]["content"][0]["text"]
    except Exception as e:
        log_error("BEDROCK_CALL_FAILED", request_id=request.headers.get("X-Request-ID"), error=str(e))
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable")
    
    # 5. Verify output
    verification = verifier.verify_output(llm_output, pseudonymized.data_sources, allow_redaction=True)
    
    if not verification.is_valid:
        log_security_event("LLM_OUTPUT_VALIDATION_FAILED", request_id=..., errors=verification.errors)
        raise HTTPException(status_code=500, detail="Output validation failed")
    
    safe_output = verification.redacted_output if verification.redacted_output else llm_output
    
    # 6. Return to frontend (frontend must NOT log raw response)
    return {
        "status": "success",
        "response": safe_output,
        "confidence": verification.confidence_score,
        "requires_human_review": verification.requires_human_review,
        "request_id": request.headers.get("X-Request-ID"),
    }
```

## Deployment

### Development (Lenient Mode)
```bash
export LLM_MODE=dev
export AWS_PROFILE=myhealth-dev
python3 test_modules.py  # Validate modules
```

### Production (Strict Mode)
```bash
export LLM_MODE=prod
export BEDROCK_AIP_ARN=arn:aws:bedrock:us-east-1:ACCOUNT:application-inference-profile/PROFILE_ID
export AWS_ROLE_ARN=arn:aws:iam::ACCOUNT:role/lambda-bedrock-invoke
# Deploy FastAPI in Fargate with private VPC networking
# All inference happens inside VPC; no public internet exposure
```

## Key Files

- **`adapters/pseudonymizer.py`** — Deterministic PHI → context transformation
- **`prompts/clinical_templates.py`** — Safe, structured prompt engineering
- **`verifier/output_verifier.py`** — Post-LLM validation & hallucination detection
- **`example_e2e_pipeline.py`** — Full pipeline demonstration
- **`test_modules.py`** — Quick validation all modules work

## Testing & Validation

### Unit Tests
```python
# test_pseudonymizer.py
def test_deterministic_hashing():
    """Same MRN always produces same pseudonym."""
    pseudo = Pseudonymizer()
    p1 = pseudo.pseudonymize_patient({"mrn": "MRN-123"}, strict=False)
    p2 = pseudo.pseudonymize_patient({"mrn": "MRN-123"}, strict=False)
    assert p1.pseudonym_id == p2.pseudonym_id

def test_phi_detection():
    """Strict mode rejects raw PHI."""
    pseudo = Pseudonymizer()
    with pytest.raises(ValueError):
        pseudo.pseudonymize_patient({"name": "John Doe"}, strict=True)

def test_output_verifier_catches_hallucinations():
    """Invalid citations are flagged."""
    verifier = OutputVerifier()
    output = "Patient has high HR (passage_999 shows elevated rate)"
    result = verifier.verify_output(output, source_passage_ids=["patient_001:passage_1"])
    assert not result.is_valid
    assert any("passage_999" in w for w in result.warnings)
```

### Privacy Tests (HIPAA Compliance)
```python
# Automated check: no raw PHI leaves the boundary
def test_no_phi_in_llm_prompt():
    """Verify prompt to Bedrock contains no identifiable information."""
    pseudo = Pseudonymizer()
    pseudonymized = pseudo.pseudonymize_patient(raw_patient, strict=False)
    llm_context = pseudo.to_llm_context(pseudonymized)
    
    # Assert no raw data
    assert llm_context["source_mrn"] is None  # Should be stripped
    assert "John" not in str(llm_context)
    assert "1958-05-15" not in str(llm_context)  # Full DOB
```

## Security Considerations

1. **Key Rotation**: Change `Pseudonymizer.SALT` only if re-pseudonymization required (re-hashes all patients).
2. **Audit Log Encryption**: CloudWatch logs must be KMS-encrypted; access controlled via IAM.
3. **VPC Isolation**: All Bedrock calls from private subnets only; no NAT/IGW to public internet.
4. **Request Signing**: Use AWS Signature Version 4 for service-to-service calls.
5. **Prompt Injection**: System prompts are hardcoded (not user-supplied); user queries must be sanitized.

## Future Enhancements

- [ ] Multi-turn conversations (store pseudonym mapping + conversation state in Qdrant)
- [ ] Feedback loop (clinician validates output → improve prompts)
- [ ] A/B testing (test multiple prompt templates on same patient)
- [ ] Cost optimization (cache embeddings for common patient profiles)
- [ ] Batch processing (async job queue for bulk health reports)

---

**When in doubt**: Prioritize **privacy**, **auditability**, and **data integrity** over feature velocity. HIPAA compliance is non-negotiable.
