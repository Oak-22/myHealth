"""
Pseudonymizer: Convert raw PHI to deterministic, pseudonymized clinical context.

This adapter ensures:
- Patient IDs map to consistent pseudonyms (patient_XXXX)
- Sensitive fields are transformed to structured clinical features
- No raw PHI is passed to LLM proxies or external systems
- All transformations are auditable and deterministic

Key principle: Pseudonymization happens upstream, before any LLM call.
The model receives rich clinical features (age_bucket, labs, trends) not raw data.
"""

import hashlib
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta


@dataclass
class PseudonymizedPatient:
    """Output of pseudonymization: structured clinical context (no PHI)."""
    
    pseudonym_id: str  # patient_XXXX
    source_mrn: str  # Audit trail: which MRN was mapped
    age_bucket: str  # "65-74" (binned to prevent re-identification)
    sex: str  # "M" or "F" (clinically needed; limited re-id risk)
    comorbidities: list[str]  # ICD-10 codes (no descriptions to avoid PII)
    current_medications: list[str]  # Drug codes (not brand names with PHI)
    vital_signs_summary: dict  # Trends only, not raw timestamps
    lab_results: dict  # Recent values, binned/rounded
    device_metrics: dict  # Heart rate trend, steps, etc. (aggregated)
    last_clinical_visit: Optional[str]  # "7 days ago", "3 months ago" (relative, not dates)
    known_concerns: list[str]  # Risk flags, symptoms (codified)
    data_sources: list[str]  # Audit trail: which passage IDs support this


class Pseudonymizer:
    """
    Deterministic pseudonymization of patient records.
    
    Design:
    - MRN → pseudonym_id mapping is cryptographic but deterministic
    - All raw PHI (names, dates, IDs) are stripped
    - Sensitive values (age, location) are binned/aggregated
    - Output is structured, LLM-friendly, audit-ready
    """
    
    SALT = "myhealth-pseudonym-v1"  # Change only if re-pseudonymization required
    
    def __init__(self, llm_mode: str = "dev"):
        """
        Args:
            llm_mode: "dev" or "prod". In dev, pseudonymization is lenient for testing.
        """
        self.llm_mode = llm_mode
    
    def pseudonymize_patient(
        self,
        raw_patient: dict,
        strict: bool = True
    ) -> PseudonymizedPatient:
        """
        Convert raw patient record to pseudonymized clinical context.
        
        Args:
            raw_patient: Dict with keys like {mrn, name, dob, sex, labs, meds, vitals, ...}
            strict: If True, fail fast if critical fields are missing or contain PHI.
        
        Returns:
            PseudonymizedPatient with no raw PHI, only clinical features.
        
        Raises:
            ValueError: If strict=True and validation fails.
        """
        # 1. Validate input
        self._validate_input(raw_patient, strict)
        
        # 2. Generate consistent pseudonym from MRN
        mrn = raw_patient.get("mrn", "unknown")
        pseudonym_id = self._hash_to_pseudonym(mrn)
        
        # 3. Extract and transform clinical features
        age_bucket = self._bucket_age(raw_patient.get("dob"))
        sex = self._validate_sex(raw_patient.get("sex"))
        comorbidities = self._extract_icd_codes(raw_patient.get("diagnoses", []))
        medications = self._extract_medication_codes(raw_patient.get("medications", []))
        vital_signs = self._aggregate_vitals(raw_patient.get("vital_signs", {}))
        labs = self._summarize_labs(raw_patient.get("labs", []))
        device_data = self._summarize_device_metrics(raw_patient.get("wearable_data", {}))
        last_visit = self._relative_date(raw_patient.get("last_visit_date"))
        concerns = self._extract_risk_flags(raw_patient.get("alerts", []))
        
        # 4. Audit trail: where did this data come from?
        data_sources = raw_patient.get("_source_passages", [])
        
        return PseudonymizedPatient(
            pseudonym_id=pseudonym_id,
            source_mrn=mrn,  # Audit only; not sent to model
            age_bucket=age_bucket,
            sex=sex,
            comorbidities=comorbidities,
            current_medications=medications,
            vital_signs_summary=vital_signs,
            lab_results=labs,
            device_metrics=device_data,
            last_clinical_visit=last_visit,
            known_concerns=concerns,
            data_sources=data_sources,
        )
    
    def to_llm_context(self, pseudonymized: PseudonymizedPatient) -> dict:
        """
        Convert PseudonymizedPatient to LLM-safe context dict (no source_mrn audit field).
        Safe to send to model.
        """
        return {
            "pseudonym_id": pseudonymized.pseudonym_id,
            "age_bucket": pseudonymized.age_bucket,
            "sex": pseudonymized.sex,
            "comorbidities": pseudonymized.comorbidities,
            "current_medications": pseudonymized.current_medications,
            "vital_signs_summary": pseudonymized.vital_signs_summary,
            "lab_results": pseudonymized.lab_results,
            "device_metrics": pseudonymized.device_metrics,
            "last_clinical_visit": pseudonymized.last_clinical_visit,
            "known_concerns": pseudonymized.known_concerns,
            "data_sources": pseudonymized.data_sources,
        }
    
    # ===== Private Methods =====
    
    def _validate_input(self, raw_patient: dict, strict: bool):
        """Fail fast if raw input contains obvious PHI or is malformed."""
        if strict:
            # Check for unencrypted PHI in keys
            dangerous_fields = ["name", "ssn", "email", "phone", "address"]
            for field in dangerous_fields:
                if field in raw_patient and raw_patient[field]:
                    raise ValueError(
                        f"Raw PHI field '{field}' detected. "
                        f"Pseudonymize upstream before calling adapter. "
                        f"In dev mode, set strict=False to override."
                    )
    
    def _hash_to_pseudonym(self, mrn: str) -> str:
        """
        Deterministically hash MRN to pseudonym_id (patient_XXXX).
        Same MRN always produces same pseudonym (good for patient tracking).
        """
        hash_obj = hashlib.sha256(f"{mrn}{self.SALT}".encode())
        hash_hex = hash_obj.hexdigest()[:8]  # First 8 chars of hash
        numeric = int(hash_hex, 16) % 100000  # Map to 5-digit number
        return f"patient_{numeric:05d}"
    
    def _bucket_age(self, dob: Optional[str]) -> str:
        """
        Convert birthdate to age bucket (avoids exact age, limits re-id risk).
        Assumes dob format: "YYYY-MM-DD"
        """
        if not dob:
            return "unknown"
        try:
            birth = datetime.strptime(dob, "%Y-%m-%d")
            today = datetime.now()
            age = (today - birth).days // 365
            # Bucket into 10-year ranges
            lower = (age // 10) * 10
            upper = lower + 9
            return f"{lower}-{upper}"
        except (ValueError, TypeError):
            return "unknown"
    
    def _validate_sex(self, sex: Optional[str]) -> str:
        """Normalize sex field (clinically needed, low re-id risk)."""
        if not sex:
            return "unknown"
        s = str(sex).upper().strip()
        return "M" if s.startswith("M") else "F" if s.startswith("F") else "unknown"
    
    def _extract_icd_codes(self, diagnoses: list) -> list[str]:
        """Extract ICD-10 codes from diagnoses (drop descriptions to avoid PII)."""
        codes = []
        for dx in diagnoses:
            if isinstance(dx, dict):
                code = dx.get("icd_code") or dx.get("code")
                if code:
                    codes.append(code)
            elif isinstance(dx, str) and dx.startswith("E"):  # Likely ICD code
                codes.append(dx)
        return codes
    
    def _extract_medication_codes(self, medications: list) -> list[str]:
        """Extract medication codes (RxNorm, not brand names which may contain PHI)."""
        codes = []
        for med in medications:
            if isinstance(med, dict):
                code = med.get("rxnorm_code") or med.get("code") or med.get("name")
                if code and not any(c.isdigit() for c in code[:2]):  # Skip raw names
                    codes.append(code)
            elif isinstance(med, str) and len(med) < 20:  # Likely a code, not description
                codes.append(med)
        return codes
    
    def _aggregate_vitals(self, vital_signs: dict) -> dict:
        """
        Summarize vital signs as trends, not raw values with timestamps.
        Example: "heart_rate_trend": "increased +12% over 7 days (avg 60→67 bpm)"
        """
        summary = {}
        
        if "heart_rate" in vital_signs:
            hr_data = vital_signs["heart_rate"]
            if isinstance(hr_data, dict):
                current = hr_data.get("current")
                baseline = hr_data.get("baseline", current)
                if current and baseline:
                    pct_change = ((current - baseline) / baseline * 100) if baseline else 0
                    direction = "increased" if pct_change > 0 else "decreased" if pct_change < 0 else "stable"
                    summary["heart_rate_trend"] = f"{direction} {abs(pct_change):.1f}% (avg {baseline:.0f}→{current:.0f} bpm)"
        
        if "blood_pressure" in vital_signs:
            bp_data = vital_signs["blood_pressure"]
            if isinstance(bp_data, dict):
                systolic = bp_data.get("systolic")
                if systolic:
                    summary["blood_pressure_latest"] = f"{systolic}/{bp_data.get('diastolic', '?')} mmHg"
        
        return summary
    
    def _summarize_labs(self, labs: list) -> dict:
        """
        Summarize recent lab results (values rounded to limit precision re-id).
        """
        summary = {}
        for lab in labs:
            if isinstance(lab, dict):
                test_name = lab.get("test_name")
                value = lab.get("value")
                unit = lab.get("unit")
                if test_name and value is not None:
                    # Round to 1-2 decimals to avoid false precision
                    rounded = round(float(value), 1) if isinstance(value, (int, float)) else value
                    summary[test_name.lower().replace(" ", "_")] = f"{rounded} {unit or ''}"
        return summary
    
    def _summarize_device_metrics(self, wearable_data: dict) -> dict:
        """
        Summarize wearable data as trends and aggregates, not timestamps.
        Example: "steps_7d": "avg 7,200 steps/day"
        """
        summary = {}
        if "steps" in wearable_data:
            steps_data = wearable_data["steps"]
            if isinstance(steps_data, dict):
                avg_7d = steps_data.get("avg_7d")
                if avg_7d:
                    summary["steps_7d_average"] = f"{avg_7d:,.0f} steps/day"
        
        if "sleep" in wearable_data:
            sleep_data = wearable_data["sleep"]
            if isinstance(sleep_data, dict):
                avg_7d = sleep_data.get("avg_7d_hours")
                if avg_7d:
                    summary["sleep_7d_average"] = f"{avg_7d:.1f} hours/night"
        
        return summary
    
    def _relative_date(self, date_str: Optional[str]) -> Optional[str]:
        """Convert absolute date to relative descriptor (e.g., '7 days ago')."""
        if not date_str:
            return None
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            delta = (datetime.now() - date).days
            if delta < 1:
                return "today"
            elif delta < 7:
                return f"{delta} days ago"
            elif delta < 30:
                weeks = delta // 7
                return f"{weeks} week{'s' if weeks > 1 else ''} ago"
            else:
                months = delta // 30
                return f"{months} month{'s' if months > 1 else ''} ago"
        except (ValueError, TypeError):
            return "unknown"
    
    def _extract_risk_flags(self, alerts: list) -> list[str]:
        """Extract risk flags and alerts (codified, no details that leak PHI)."""
        flags = []
        for alert in alerts:
            if isinstance(alert, dict):
                flag = alert.get("code") or alert.get("type")
                if flag:
                    flags.append(flag)
            elif isinstance(alert, str):
                flags.append(alert)
        return flags


# Example usage & testing
if __name__ == "__main__":
    # Synthetic test data (no real PHI)
    raw_patient = {
        "mrn": "MRN-123456",  # Will be hashed to patient_XXXXX
        "name": "John Doe",  # This should trigger validation error
        "dob": "1958-05-15",
        "sex": "M",
        "diagnoses": [
            {"icd_code": "E11", "description": "Type 2 Diabetes"},
            {"icd_code": "I10", "description": "Hypertension"},
        ],
        "medications": [
            {"rxnorm_code": "860975", "name": "Metformin 500mg"},
            {"rxnorm_code": "197414", "name": "Lisinopril 10mg"},
        ],
        "vital_signs": {
            "heart_rate": {"current": 72, "baseline": 65},
            "blood_pressure": {"systolic": 135, "diastolic": 88},
        },
        "labs": [
            {"test_name": "HbA1c", "value": 8.2, "unit": "%"},
            {"test_name": "Creatinine", "value": 1.1, "unit": "mg/dL"},
        ],
        "wearable_data": {
            "steps": {"avg_7d": 7200},
            "sleep": {"avg_7d_hours": 6.5},
        },
        "last_visit_date": "2026-01-30",
        "alerts": [{"code": "HIGH_A1C"}, {"code": "ELEVATED_BP"}],
        "_source_passages": ["patient_00001:passage_42", "patient_00001:passage_91"],
    }
    
    # Test strict mode (should fail due to "name" field)
    pseudonymizer = Pseudonymizer(llm_mode="prod")
    try:
        result = pseudonymizer.pseudonymize_patient(raw_patient, strict=True)
        print("ERROR: Should have failed on 'name' field")
    except ValueError as e:
        print(f"✓ Validation caught PHI: {e}")
    
    # Test lenient mode (dev)
    pseudonymizer_dev = Pseudonymizer(llm_mode="dev")
    result = pseudonymizer_dev.pseudonymize_patient(raw_patient, strict=False)
    print(f"\n✓ Pseudonymized patient:")
    print(f"  Pseudonym ID: {result.pseudonym_id}")
    print(f"  Age bucket: {result.age_bucket}")
    print(f"  Sex: {result.sex}")
    print(f"  Comorbidities: {result.comorbidities}")
    print(f"  Vital signs: {result.vital_signs_summary}")
    print(f"  Labs: {result.lab_results}")
    print(f"  Device metrics: {result.device_metrics}")
    print(f"  Last visit: {result.last_clinical_visit}")
    print(f"  Concerns: {result.known_concerns}")
    
    # Safe to send to LLM
    llm_context = pseudonymizer_dev.to_llm_context(result)
    print(f"\n✓ LLM-safe context (no source_mrn):")
    print(llm_context)
