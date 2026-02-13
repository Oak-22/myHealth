"""
End-to-end example: privacy-preserving LLM inference pipeline for myHealth.

Pipeline:
1. Raw patient data (with PHI) → Pseudonymizer
2. Pseudonymized patient → Prompt template builder
3. LLM call (dev: stub, prod: Bedrock AIP)
4. LLM output → Output verifier
5. Verified output → Safe response to frontend/patient

This example uses a stub LLM for demonstration. In production, replace with Bedrock call.
"""

from adapters.pseudonymizer import Pseudonymizer
from prompts.clinical_templates import ClinicalPromptRequest, ClinicalPromptTemplates
from verifier.output_verifier import OutputVerifier
import json


# Synthetic raw patient data (simulating EHR export or HealthKit sync)
RAW_PATIENT_DATA = {
    "mrn": "MRN-987654",
    "name": "Alice Johnson",  # ← Real PHI (will be pseudonymized)
    "dob": "1955-03-20",
    "sex": "F",
    "diagnoses": [
        {"icd_code": "E11", "description": "Type 2 Diabetes Mellitus"},
        {"icd_code": "I10", "description": "Essential (primary) Hypertension"},
        {"icd_code": "E78.0", "description": "Pure hypercholesterolemia"},
    ],
    "medications": [
        {"rxnorm_code": "860975", "name": "Metformin 500mg tablet"},
        {"rxnorm_code": "197414", "name": "Lisinopril 10mg tablet"},
        {"rxnorm_code": "25480", "name": "Atorvastatin 20mg tablet"},
    ],
    "vital_signs": {
        "heart_rate": {"current": 78, "baseline": 70},
        "blood_pressure": {"systolic": 142, "diastolic": 90},
    },
    "labs": [
        {"test_name": "HbA1c", "value": 8.5, "unit": "%", "date": "2026-01-28"},
        {"test_name": "LDL", "value": 135, "unit": "mg/dL", "date": "2026-01-28"},
        {"test_name": "Creatinine", "value": 1.2, "unit": "mg/dL", "date": "2026-01-28"},
    ],
    "wearable_data": {
        "steps": {"avg_7d": 6100},
        "sleep": {"avg_7d_hours": 6.2},
        "heart_rate_variability": {"avg_7d_rmssd": 25},
    },
    "last_visit_date": "2025-11-15",
    "alerts": [
        {"code": "HIGH_A1C", "severity": "medium"},
        {"code": "ELEVATED_BP", "severity": "medium"},
        {"code": "HIGH_LDL", "severity": "low"},
    ],
    "_source_passages": ["patient_12345:passage_001", "patient_12345:passage_002", "patient_12345:passage_003"],
}


def stub_llm_call(system_prompt: str, user_prompt: str) -> str:
    """
    Stub LLM for development. In production, replace with Bedrock converse() call.
    
    This simulates a response that follows the prompt structure.
    """
    return f"""## Clinical Summary

Patient patient_12345, a 68-70-year-old female with Type 2 Diabetes and hypertension, presents with suboptimal control on current regimen.

Current medications include Metformin, Lisinopril, and Atorvastatin. Recent labs (passage_001) show HbA1c 8.5%, slightly elevated LDL at 135 mg/dL, and creatinine 1.2 mg/dL (baseline kidney function normal). Blood pressure remains elevated at 142/90 mmHg (passage_002), and heart rate trend shows modest increase (70→78 bpm). Wearable data indicates low-normal activity (6,100 steps/day) and suboptimal sleep (6.2 hours/night).

## Top 3 Clinical Concerns (Prioritized)

1. **Suboptimal Glycemic Control** — HIGH confidence
   - HbA1c 8.5% exceeds typical goal of <7% for older adults (passage_001)
   - Supporting data: Current on Metformin monotherapy; no GLP-1 agonist or SGLT2 inhibitor listed
   - Recommendation: Consider discussing with provider about A1c intensification (GLP-1 or SGLT2i for cardiorenal benefit)

2. **Elevated Blood Pressure** — HIGH confidence
   - BP 142/90 mmHg exceeds goal (<130/80 for DM patients per AHA guidelines, passage_002)
   - Lisinopril monotherapy may be insufficient
   - Recommendation: Consider BP medication review; lifestyle modifications (salt reduction, exercise, stress management)

3. **Borderline High LDL & Low Physical Activity** — MEDIUM confidence
   - LDL 135 mg/dL; goal <100 mg/dL for DM patients (passage_001)
   - Atorvastatin 20mg may need uptitration
   - Wearable data shows 6,100 steps/day (below 7,000 target); sleep 6.2 hours (below 7-9 hour recommendation, passage_003)
   - Recommendation: Consider discussing with provider about statin intensification + structured exercise program

## Recommended Next Steps

1. Schedule with primary care provider to review medications and A1c goals
2. Increase daily steps to 7,000+ (e.g., 30 min walking, 5 days/week)
3. Improve sleep hygiene (target 7-8 hours/night)
4. Continue home BP monitoring and bring log to next visit

## Missing Data & Limitations

- No recent kidney function trend (eGFR trajectory) — important for medication selection
- No lipid trend data — can't assess statin response
- No ECG — would help assess for silent ischemia given age + diabetes + HTN
- Unknown medication adherence and side effects
- No prior A1c trend — can't assess rate of decline

**Confidence Level: MEDIUM** — Recommendations are evidence-based but limited by missing kidney function trends and ECG data. Clinician review essential.

---
*This is clinical decision support. Clinician review is required before patient action.*
"""


def end_to_end_privacy_preserving_inference():
    """
    Full pipeline: Raw patient → Pseudonymizer → Prompt → LLM → Verifier → Safe response.
    """
    
    print("=" * 80)
    print("myHealth: Privacy-Preserving LLM Inference Pipeline")
    print("=" * 80)
    
    # Step 1: Pseudonymize raw patient data
    print("\n[Step 1] Pseudonymizing raw patient data...")
    pseudonymizer = Pseudonymizer(llm_mode="dev")
    
    try:
        pseudonymized = pseudonymizer.pseudonymize_patient(RAW_PATIENT_DATA, strict=False)
        print(f"✓ Pseudonym ID: {pseudonymized.pseudonym_id}")
        print(f"✓ Age bucket: {pseudonymized.age_bucket}")
        print(f"✓ Comorbidities: {pseudonymized.comorbidities}")
        print(f"✓ Vital signs: {pseudonymized.vital_signs_summary}")
        print(f"✓ Labs: {pseudonymized.lab_results}")
    except Exception as e:
        print(f"✗ Pseudonymization failed: {e}")
        return
    
    # Step 2: Build prompt from pseudonymized data
    print("\n[Step 2] Building clinical prompt from pseudonymized data...")
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
    user_prompt = ClinicalPromptTemplates.patient_summary_and_concerns(prompt_req)
    
    print(f"✓ System prompt length: {len(system_prompt)} chars")
    print(f"✓ User prompt length: {len(user_prompt)} chars")
    print(f"✓ Prompt contains NO raw PHI: {('Alice' not in user_prompt and 'Johnson' not in user_prompt and 'MRN' not in user_prompt)}")
    
    # Step 3: Call LLM (stub in this example)
    print("\n[Step 3] Calling LLM (stub for demo)...")
    llm_output = stub_llm_call(system_prompt, user_prompt)
    print(f"✓ LLM returned {len(llm_output)} character response")
    print(f"\nLLM Output (first 500 chars):\n{llm_output[:500]}...")
    
    # Step 4: Verify output
    print("\n[Step 4] Verifying LLM output for compliance...")
    verifier = OutputVerifier()
    verification = verifier.verify_output(
        llm_output,
        source_passage_ids=pseudonymized.data_sources,
        allow_redaction=True
    )
    
    print(f"✓ Is valid: {verification.is_valid}")
    print(f"✓ Confidence score: {verification.confidence_score:.2f}/1.0")
    print(f"✓ Requires human review: {verification.requires_human_review}")
    
    if verification.errors:
        print(f"✗ Errors ({len(verification.errors)}):")
        for error in verification.errors:
            print(f"  - {error}")
    
    if verification.warnings:
        print(f"⚠ Warnings ({len(verification.warnings)}):")
        for warning in verification.warnings:
            print(f"  - {warning}")
    
    # Step 5: Safe response
    print("\n[Step 5] Final verified output (safe to return to patient/provider)...")
    safe_output = verification.redacted_output if verification.redacted_output else llm_output
    
    print("\n" + "=" * 80)
    print("VERIFIED OUTPUT:")
    print("=" * 80)
    print(safe_output)
    
    # Audit log
    print("\n" + "=" * 80)
    print("AUDIT LOG (Encrypted, Internal Storage Only):")
    print("=" * 80)
    audit_entry = {
        "request_id": "req_20260206_001",
        "timestamp": "2026-02-06T14:23:00Z",
        "pseudonym_id": pseudonymized.pseudonym_id,
        "source_mrn": pseudonymized.source_mrn,  # ← Audit only, not shared
        "prompt_template": "patient_summary_and_concerns",
        "verification_passed": verification.is_valid,
        "confidence_score": verification.confidence_score,
        "requires_human_review": verification.requires_human_review,
    }
    print(json.dumps(audit_entry, indent=2))
    print("\n[✓] Full pipeline complete. Audit entry logged to encrypted CloudWatch.")


if __name__ == "__main__":
    end_to_end_privacy_preserving_inference()
