"""
Quick Reference: Privacy-Preserving LLM Inference for myHealth

Three modules, four steps, zero raw PHI sent to external systems.
"""

# Step 1: PSEUDONYMIZE raw patient data
# ────────────────────────────────────────────────────────────────
from adapters.pseudonymizer import Pseudonymizer

raw_patient = {
    "mrn": "MRN-123456",
    "name": "John Doe",  # ← Raw PHI
    "dob": "1958-05-15",
    "diagnoses": [{"icd_code": "E11"}],
    "medications": [{"rxnorm_code": "860975"}],
    "labs": [{"test_name": "HbA1c", "value": 8.2}],
    # ... more fields
}

pseudonymizer = Pseudonymizer(llm_mode="prod")
pseudonymized = pseudonymizer.pseudonymize_patient(raw_patient, strict=True)

# Output: PseudonymizedPatient object
# ├── pseudonym_id: "patient_00042"        ← Deterministic hash of MRN
# ├── age_bucket: "65-74"                 ← Binned (not exact age)
# ├── sex: "M"
# ├── comorbidities: ["E11", "I10"]       ← ICD codes (not descriptions)
# ├── vital_signs_summary: {              ← Trends, not timestamps
# │   "heart_rate_trend": "increased 12% (60→67 bpm)",
# │   "blood_pressure_latest": "135/88 mmHg"
# │ }
# ├── data_sources: ["patient_00042:passage_42", ...]  ← Audit trail
# └── source_mrn: "MRN-123456"            ← Audit only (not sent to LLM)


# Step 2: BUILD PROMPT from pseudonymized context
# ────────────────────────────────────────────────────────────────
from prompts.clinical_templates import ClinicalPromptRequest, ClinicalPromptTemplates

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
    data_sources=pseudonymized.data_sources,
)

system = ClinicalPromptTemplates.system_prompt_for_clinical_assistant()
user = ClinicalPromptTemplates.patient_summary_and_concerns(prompt_req)

# Output: Two strings (system + user prompts)
# ✓ Contains: patient_00042, age_bucket, ICD codes, trends, passage IDs
# ✓ NO raw PHI: no name, no full DOB, no exact age, no SSN, no email, no phone
# ✓ Rich context: clinical features the model needs to reason


# Step 3: CALL LLM (Bedrock AIP inside VPC)
# ────────────────────────────────────────────────────────────────
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

response = bedrock.converse(
    modelId="arn:aws:bedrock:us-east-1:ACCOUNT:application-inference-profile/...",
    messages=[{"role": "user", "content": [{"text": system + "\n\n" + user}]}],
    inferenceConfig={"maxTokens": 1024, "temperature": 0.7}
)

llm_output = response["output"]["message"]["content"][0]["text"]

# Output: LLM-generated clinical summary
# Potentially contains:
# ✓ Valid citations (e.g., "passage_42")
# ✓ Confidence statements (e.g., "HIGH confidence")
# ✓ Recommendations ("Consider discussing with provider...")
# ✗ Possible PHI leakage (hallucination)
# ✗ Possible invalid citations (if model invents passage IDs)
# ✗ Implausible values (e.g., "HR 500 bpm")


# Step 4: VERIFY output for compliance
# ────────────────────────────────────────────────────────────────
from verifier.output_verifier import OutputVerifier

verifier = OutputVerifier()
verification = verifier.verify_output(
    llm_output,
    source_passage_ids=pseudonymized.data_sources,
    allow_redaction=True
)

# Output: VerificationResult object
# ├── is_valid: True/False
# ├── errors: ["Unredacted PHI found: email john@example.com", ...]
# ├── warnings: ["Citation 'passage_999' not in provided data", ...]
# ├── confidence_score: 0.85 (0.0-1.0)
# ├── requires_human_review: True/False
# └── redacted_output: Safe version if PHI detected


# FINAL STEP: Return safe output to frontend
# ────────────────────────────────────────────────────────────────
if verification.is_valid:
    # ✓ No errors, confidence OK
    response = {
        "status": "success",
        "insights": verification.redacted_output or llm_output,
        "confidence": verification.confidence_score,
        "requires_human_review": verification.requires_human_review,
    }
else:
    # ✗ Validation failed, escalate
    response = {
        "status": "error",
        "message": "Output validation failed. Please contact support.",
        "request_id": "req_20260206_001",  # For debugging
    }


# WHAT GETS LOGGED (Encrypted, Internal Only)
# ────────────────────────────────────────────────────────────────
audit_entry = {
    "request_id": "req_20260206_001",
    "timestamp": "2026-02-06T14:23:00Z",
    "pseudonym_id": pseudonymized.pseudonym_id,
    "source_mrn": pseudonymized.source_mrn,  # ← Audit trail (encrypted log only)
    "template": "patient_summary_and_concerns",
    "verification_passed": verification.is_valid,
    "confidence_score": verification.confidence_score,
}
# Logged to: CloudWatch (KMS-encrypted) + S3 (server-side encryption)
# Access: IAM role-based only; immutable; audit trail for compliance


# SECURITY CHECKLIST
# ────────────────────────────────────────────────────────────────
"""
✓ Raw PHI (name, DOB, SSN): Stripped by Pseudonymizer
✓ Clinical context: Preserved (age_bucket, ICD codes, trends)
✓ Patient tracking: Works (deterministic pseudonym_id)
✓ Citations: Required + validated (passage_42 must exist)
✓ Confidence: Scored + flagged for human review if low
✓ Hallucinations: Caught (invalid citations, implausible values)
✓ Prescriptive advice: Forbidden ("discuss with provider" only)
✓ VPC isolation: All Bedrock calls from private subnets
✓ Audit trail: Encrypted logs (request_id, pseudonym_id, source_mrn)
✓ Compliance: HIPAA-ready (PHI segregation, auditability, integrity)
"""


# THREE MODULES SUMMARY
# ────────────────────────────────────────────────────────────────

print("""
┌─────────────────────────────────────────────────────────────────┐
│ adapters/pseudonymizer.py (450 lines)                           │
├─────────────────────────────────────────────────────────────────┤
│ Raw PHI → Pseudonymized Clinical Context                        │
│ - MRN → patient_XXXXX (deterministic hash)                      │
│ - DOB → age_bucket (privacy + utility)                          │
│ - Medications → RxNorm codes only                               │
│ - Vitals → Trends (not raw timestamps)                          │
│ - Labs → Rounded values (re-id defense)                         │
│ - Validation: Strict mode rejects raw PHI                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ prompts/clinical_templates.py (350 lines)                       │
├─────────────────────────────────────────────────────────────────┤
│ Pseudonymized Context → LLM-Safe Prompt                         │
│ - System prompt: Safety guardrails                              │
│ - User prompts: 4 templates (summary, meds, cardio, etc.)       │
│ - Citations required: Every claim must cite passage_ID          │
│ - Confidence enforced: HIGH / MEDIUM / LOW                      │
│ - Responsibility: "Discuss with provider" (not "prescribe")     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ verifier/output_verifier.py (400 lines)                         │
├─────────────────────────────────────────────────────────────────┤
│ LLM Output → Verified & Redacted Response                       │
│ - PHI detection: emails, SSNs, dates, names, MRNs              │
│ - Citation validation: All passage_IDs must exist               │
│ - Value ranges: HR 40-200, HbA1c 4-14%, etc.                   │
│ - Safety: Forbid prescriptive advice                            │
│ - Structure: Require headings, citations, confidence            │
│ - Scoring: Confidence reduced by violations                     │
│ - Human review: Flag if confidence < 0.7                        │
└─────────────────────────────────────────────────────────────────┘

FULL PIPELINE:
Raw Patient → [1. Pseudonymize] → [2. Build Prompt] → [3. Call LLM]
                    ↓                      ↓                  ↓
            Pseudonymized         Prompt (no PHI)      LLM Output
                                                             ↓
                                                  [4. Verify Output]
                                                             ↓
                                              Safe Response + Audit Log
""")


if __name__ == "__main__":
    # Run this module to see the architecture
    pass
