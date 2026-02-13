"""
Prompt templates for privacy-preserving LLM inference on pseudonymized patient data.

Key patterns:
- Require citations to source passages (not raw PHI, just reference IDs)
- Ask model to list assumptions and flag missing data
- Request confidence scores and recommended next steps
- Enforce structured reasoning to catch hallucinations
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ClinicalPromptRequest:
    """Input to a clinical prompt template."""
    
    pseudonym_id: str
    age_bucket: str
    sex: str
    comorbidities: list[str]
    current_medications: list[str]
    vital_signs_summary: dict
    lab_results: dict
    device_metrics: dict
    last_clinical_visit: Optional[str]
    known_concerns: list[str]
    data_sources: list[str]  # Passage IDs for citation


class ClinicalPromptTemplates:
    """
    Clinical reasoning prompt templates.
    
    Design: Structured prompts that require reasoning, citations, and confidence.
    Output is easily verifiable and auditable.
    """
    
    @staticmethod
    def patient_summary_and_concerns(req: ClinicalPromptRequest) -> str:
        """
        Generate a clinical summary and identify top concerns.
        
        Useful for: initial triage, risk stratification, patient education.
        """
        return f"""You are a clinical decision support assistant. Analyze the following pseudonymized patient profile and provide a structured summary.

**Patient Profile:**
- Pseudonym ID: {req.pseudonym_id}
- Age: {req.age_bucket}
- Sex: {req.sex}
- Comorbidities (ICD codes): {', '.join(req.comorbidities) or 'None'}
- Current medications: {', '.join(req.current_medications) or 'None'}
- Vital signs (recent trends): {req.vital_signs_summary}
- Lab results: {req.lab_results}
- Wearable metrics (7-day avg): {req.device_metrics}
- Last clinical visit: {req.last_clinical_visit or 'Unknown'}
- Known alerts/flags: {', '.join(req.known_concerns) or 'None'}
- Data sources (passage IDs): {', '.join(req.data_sources)}

**Your Task:**
1. **Clinical Summary** (~100 words): Synthesize the patient profile into a narrative summary.
   - Cite which data sources (passage IDs) support each claim.
   - Flag any contradictions or missing data that would improve confidence.

2. **Top 3 Clinical Concerns** (prioritized by urgency):
   - List each concern with:
     - A clinical explanation (1-2 sentences)
     - Which vital signs, labs, or comorbidities support it
     - Confidence (HIGH / MEDIUM / LOW)
     - Data source citations (passage IDs)

3. **Recommended Next Steps** (if appropriate for patient education):
   - Suggested actions (lifestyle, monitoring frequency, when to escalate)
   - Why these are recommended based on the profile
   - Caveats: "This requires clinician review before implementation"

4. **Missing Data / Limitations:**
   - What additional information would improve confidence?
   - Any data points that seem inconsistent?
   - Assumptions you are making about this patient?

**Constraints:**
- Do NOT invent patient names, dates, or specific identifiers.
- Do NOT provide medical advice directly; frame as "consider discussing with provider."
- Cite your sources (passage IDs) for every claim.
- If you are uncertain, say so and explain why.
"""

    @staticmethod
    def medication_review_prompt(req: ClinicalPromptRequest) -> str:
        """
        Review current medications for potential interactions, gaps, or concerns.
        """
        return f"""You are a pharmacist assistant. Review the current medication list for this pseudonymized patient.

**Patient Context:**
- Pseudonym ID: {req.pseudonym_id}
- Age: {req.age_bucket}
- Comorbidities: {', '.join(req.comorbidities) or 'None'}
- Medications: {', '.join(req.current_medications) or 'None'}
- Labs: {req.lab_results}
- Data sources: {', '.join(req.data_sources)}

**Your Task:**
1. **Medication Review:**
   - Are these medications appropriate for the diagnoses listed?
   - Any potential drug-drug interactions?
   - Any concerning lab interactions (e.g., ACE inhibitor with high creatinine)?

2. **Medication Gaps:**
   - Based on comorbidities and recent labs, are any medications missing?
   - Examples: A1c 8.2 + diabetes but no GLP-1 agonist listed — why might that be?

3. **Recommendations:**
   - Suggest medication adjustments (if appropriate for patient education).
   - Frame as "Consider discussing with provider: [recommendation]"
   - Cite supporting data (passage IDs, lab values, guidelines).

4. **Confidence & Caveats:**
   - How confident are you in these recommendations?
   - What additional data would help (drug allergy history, prior trials, insurance restrictions)?

**Constraints:**
- Do NOT prescribe or authorize medication changes.
- Do NOT reference patient names, medical record numbers, or specific dates.
- Cite your reasoning and data sources.
"""

    @staticmethod
    def heart_health_check_prompt(req: ClinicalPromptRequest) -> str:
        """
        Focused check on cardiovascular risk based on vital signs, labs, meds, and comorbidities.
        """
        return f"""You are a cardiovascular risk assessment tool. Evaluate cardiac risk for this pseudonymized patient.

**Patient Profile:**
- Pseudonym ID: {req.pseudonym_id}
- Age: {req.age_bucket}
- Sex: {req.sex}
- Comorbidities: {', '.join(req.comorbidities) or 'None'}
- Vital signs: {req.vital_signs_summary}
- Recent labs: {req.lab_results}
- Medications: {', '.join(req.current_medications) or 'None'}
- Device metrics: {req.device_metrics}
- Data sources: {', '.join(req.data_sources)}

**Your Task:**
1. **Cardiovascular Risk Assessment:**
   - Estimate 10-year ASCVD risk based on age, sex, comorbidities, and labs (if available).
   - Are there signs of heart rate instability or elevated BP trends?
   - Any concerns based on wearable data (e.g., HR variability)?

2. **Actionable Recommendations:**
   - Lifestyle modifications (exercise frequency, diet, stress management).
   - Monitoring recommendations (daily BP checks, ECG, frequency of visits).
   - When to escalate (chest pain, syncope, arrhythmia detection).

3. **Missing Data:**
   - Would lipid panel, ECG, or echocardiogram improve risk stratification?
   - Is medication optimization needed (e.g., statin, aspirin, ACE inhibitor)?

4. **Confidence Level:**
   - Rate confidence in this risk assessment (HIGH / MEDIUM / LOW).
   - Explain limitations based on available data.

**Constraints:**
- Do NOT diagnose acute conditions (e.g., "patient is having an MI").
- Do NOT authorize medication changes without provider review.
- Cite all recommendations with data sources and reasoning.
"""

    @staticmethod
    def system_prompt_for_clinical_assistant() -> str:
        """
        System prompt to be prepended to all clinical LLM calls.
        Enforces safety, auditability, and responsibility disclaimers.
        """
        return """You are a clinical decision support assistant integrated into myHealth, a privacy-preserving healthcare platform.

**Your Role:**
- Synthesize pseudonymized patient data into actionable clinical insights.
- Identify patterns in vital signs, labs, medications, and wearable data.
- Suggest next steps for patient education and provider collaboration.

**Critical Constraints:**
1. **Privacy & Compliance:**
   - All patient data is pseudonymized (patient_XXXX IDs, binned ages, coded diagnoses).
   - Do NOT request, invent, or reference raw PHI (names, dates, SSNs, specific locations).
   - Do NOT embed or reference identifiable information in your response.

2. **Accountability:**
   - Cite your sources: reference passage IDs provided in the patient profile.
   - Explain your reasoning step-by-step.
   - Clearly state confidence levels (HIGH / MEDIUM / LOW).
   - Flag assumptions and missing data that limit your confidence.

3. **Responsibility:**
   - You are a decision SUPPORT tool, not a replacement for clinicians.
   - Frame all recommendations as "Consider discussing with your provider: [recommendation]"
   - Do NOT diagnose, prescribe, or authorize medical actions.
   - If uncertain, err on the side of escalation and human review.

4. **Safety & Hallucination Prevention:**
   - Do NOT invent vital signs, labs, or patient history.
   - Do NOT make recommendations beyond the scope of the provided data.
   - If data is missing or contradictory, acknowledge and ask for clarification.
   - Do NOT extrapolate to conditions not supported by available evidence.

**Output Format:**
- Use clear headings and numbered lists for readability.
- Cite sources (passage IDs) inline with claims.
- Provide a confidence statement for each recommendation.
- End with: "This is clinical decision support. Clinician review is required before patient action."
"""


# Example usage
if __name__ == "__main__":
    from adapters.pseudonymizer import PseudonymizedPatient
    
    # Create a synthetic pseudonymized patient
    synthetic_patient = PseudonymizedPatient(
        pseudonym_id="patient_00042",
        source_mrn="MRN-123456",
        age_bucket="65-74",
        sex="F",
        comorbidities=["E11", "I10"],  # T2DM, HTN
        current_medications=["860975", "197414"],  # Metformin, Lisinopril
        vital_signs_summary={
            "heart_rate_trend": "increased 12% over 7 days (avg 60→67 bpm)",
            "blood_pressure_latest": "135/88 mmHg"
        },
        lab_results={
            "hba1c": "8.2 %",
            "creatinine": "1.1 mg/dL"
        },
        device_metrics={"steps_7d_average": "7,200 steps/day", "sleep_7d_average": "6.5 hours/night"},
        last_clinical_visit="7 days ago",
        known_concerns=["HIGH_A1C", "ELEVATED_BP"],
        data_sources=["patient_00042:passage_42", "patient_00042:passage_91"]
    )
    
    # Convert to prompt request
    prompt_req = ClinicalPromptRequest(
        pseudonym_id=synthetic_patient.pseudonym_id,
        age_bucket=synthetic_patient.age_bucket,
        sex=synthetic_patient.sex,
        comorbidities=synthetic_patient.comorbidities,
        current_medications=synthetic_patient.current_medications,
        vital_signs_summary=synthetic_patient.vital_signs_summary,
        lab_results=synthetic_patient.lab_results,
        device_metrics=synthetic_patient.device_metrics,
        last_clinical_visit=synthetic_patient.last_clinical_visit,
        known_concerns=synthetic_patient.known_concerns,
        data_sources=synthetic_patient.data_sources
    )
    
    # Generate prompts
    print("=== System Prompt ===")
    print(ClinicalPromptTemplates.system_prompt_for_clinical_assistant())
    
    print("\n=== Patient Summary & Concerns Prompt ===")
    print(ClinicalPromptTemplates.patient_summary_and_concerns(prompt_req))
    
    print("\n=== Cardiovascular Risk Assessment Prompt ===")
    print(ClinicalPromptTemplates.heart_health_check_prompt(prompt_req))
