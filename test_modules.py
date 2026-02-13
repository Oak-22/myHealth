#!/usr/bin/env python3
"""Quick validation that all modules load and basic functionality works."""

import sys
sys.path.insert(0, '/Users/julianbuccat/Projects/Dev/myHealth')

print("Testing module imports...")

try:
    from adapters.pseudonymizer import Pseudonymizer, PseudonymizedPatient
    print("✓ Pseudonymizer imported")
except Exception as e:
    print(f"✗ Pseudonymizer import failed: {e}")
    sys.exit(1)

try:
    from prompts.clinical_templates import ClinicalPromptTemplates, ClinicalPromptRequest
    print("✓ ClinicalPromptTemplates imported")
except Exception as e:
    print(f"✗ ClinicalPromptTemplates import failed: {e}")
    sys.exit(1)

try:
    from verifier.output_verifier import OutputVerifier, VerificationResult
    print("✓ OutputVerifier imported")
except Exception as e:
    print(f"✗ OutputVerifier import failed: {e}")
    sys.exit(1)

print("\nTesting basic functionality...")

# Test pseudonymizer
pseudo = Pseudonymizer(llm_mode="dev")
test_patient = {
    "mrn": "MRN-TEST123",
    "dob": "1960-01-15",
    "sex": "M",
    "diagnoses": [{"icd_code": "E11"}],
    "medications": [{"rxnorm_code": "860975"}],
    "vital_signs": {"heart_rate": {"current": 72, "baseline": 70}},
    "labs": [],
    "wearable_data": {},
    "alerts": [],
    "_source_passages": ["patient_00001:passage_1"],
}

result = pseudo.pseudonymize_patient(test_patient, strict=False)
print(f"✓ Pseudonymizer: {result.pseudonym_id}, age_bucket={result.age_bucket}")

# Test prompt templates
req = ClinicalPromptRequest(
    pseudonym_id=result.pseudonym_id,
    age_bucket=result.age_bucket,
    sex=result.sex,
    comorbidities=result.comorbidities,
    current_medications=result.current_medications,
    vital_signs_summary=result.vital_signs_summary,
    lab_results=result.lab_results,
    device_metrics=result.device_metrics,
    last_clinical_visit=result.last_clinical_visit,
    known_concerns=result.known_concerns,
    data_sources=result.data_sources,
)

prompt = ClinicalPromptTemplates.patient_summary_and_concerns(req)
print(f"✓ Prompt template generated ({len(prompt)} chars)")

# Test verifier
verifier = OutputVerifier()
test_output = """
## Summary
Patient patient_00001 has elevated heart rate (72 bpm, passage_1).

### Recommendation
Consider discussing with provider: increase exercise frequency.

**Confidence: MEDIUM**
"""

verification = verifier.verify_output(test_output, ["patient_00001:passage_1"])
print(f"✓ Verifier: valid={verification.is_valid}, confidence={verification.confidence_score:.2f}")

print("\n✓✓✓ All modules working correctly! ✓✓✓")
