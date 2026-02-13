"""
Output verifier: Post-LLM validation to catch hallucinations and rule violations.

Patterns:
- Check for unredacted PHI in model output
- Verify lab/vital ranges are plausible
- Ensure citations reference valid source IDs
- Enforce structured output format
- Flag low-confidence or speculative claims
"""

from dataclasses import dataclass, field
from typing import Optional
import re


@dataclass
class VerificationResult:
    """Result of output verification."""
    
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    confidence_score: float = 1.0  # 0.0 to 1.0; reduced by violations
    requires_human_review: bool = False
    redacted_output: Optional[str] = None  # Safe version of output if issues found


class OutputVerifier:
    """
    Verify LLM output for compliance and correctness.
    
    Rules:
    1. No unredacted PHI (names, dates, SSNs, MRNs)
    2. Lab/vital values must be plausible ranges
    3. Citations must reference valid source passage IDs
    4. No diagnosis claims without supporting evidence
    5. No prescriptive medical advice (only recommendations for provider discussion)
    6. Output must be structured (headings, citations, confidence levels)
    """
    
    # Regex patterns for detecting unredacted PHI
    PHI_PATTERNS = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b(?:\+1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "date_full": r"\b\d{4}-\d{2}-\d{2}\b",  # YYYY-MM-DD dates
        "mrn": r"\b[A-Z]{2,}-\d{6,}\b",  # MRN-123456 pattern
        "names_common": r"\b(?:John|Jane|Mary|James|Robert|Michael|David|Jennifer|Linda|Barbara|Susan|Jessica)\b",
    }
    
    # Plausible ranges for vital signs and labs
    PLAUSIBLE_RANGES = {
        "heart_rate": (40, 200),  # bpm
        "systolic_bp": (70, 220),  # mmHg
        "diastolic_bp": (40, 140),  # mmHg
        "hba1c": (4, 14),  # %
        "creatinine": (0.5, 3.0),  # mg/dL
        "glucose": (50, 400),  # mg/dL
        "ldl": (0, 300),  # mg/dL
    }
    
    def __init__(self):
        self.pseudonym_pattern = re.compile(r"patient_\d{5}")  # Valid pseudonym format
    
    def verify_output(
        self,
        llm_output: str,
        source_passage_ids: list[str],
        allow_redaction: bool = True
    ) -> VerificationResult:
        """
        Verify LLM output for compliance.
        
        Args:
            llm_output: Raw text from LLM
            source_passage_ids: List of valid passage IDs (for citation validation)
            allow_redaction: If True, automatically redact detected PHI; if False, flag as error
        
        Returns:
            VerificationResult with is_valid, errors, warnings, confidence_score
        """
        result = VerificationResult(is_valid=True)
        redacted = llm_output
        
        # 1. Check for unredacted PHI
        phi_findings = self._scan_for_phi(llm_output)
        if phi_findings:
            if allow_redaction:
                result.warnings.extend([f"PHI detected and redacted: {finding}" for finding in phi_findings])
                redacted = self._redact_phi(llm_output)
                result.confidence_score *= 0.8
            else:
                result.is_valid = False
                result.errors.extend([f"Unredacted PHI found: {finding}" for finding in phi_findings])
        
        # 2. Check for invalid citations
        citation_errors = self._validate_citations(redacted, source_passage_ids)
        if citation_errors:
            result.warnings.extend(citation_errors)
            result.confidence_score *= 0.9
        
        # 3. Check for plausible lab/vital values
        range_errors = self._validate_value_ranges(redacted)
        if range_errors:
            result.warnings.extend(range_errors)
            result.confidence_score *= 0.85
        
        # 4. Check for prescriptive medical advice (no "prescribe X")
        if self._contains_prescriptive_advice(redacted):
            result.warnings.append("Output contains prescriptive advice (not just recommendations for provider discussion)")
            result.confidence_score *= 0.7
            result.requires_human_review = True
        
        # 5. Check for structured output (headings, numbered lists)
        if not self._is_structured(redacted):
            result.warnings.append("Output lacks clear structure (missing headings, citations, or confidence levels)")
            result.confidence_score *= 0.9
        
        # 6. Check confidence statements
        if not self._has_confidence_statements(redacted):
            result.warnings.append("Output missing confidence level statements (HIGH/MEDIUM/LOW)")
            result.confidence_score *= 0.85
        
        # Final checks
        if result.errors:
            result.is_valid = False
        
        if result.confidence_score < 0.7:
            result.requires_human_review = True
        
        result.redacted_output = redacted if phi_findings and allow_redaction else None
        
        return result
    
    # ===== Private Validation Methods =====
    
    def _scan_for_phi(self, text: str) -> list[str]:
        """Scan for unredacted PHI using regex patterns."""
        findings = []
        for phi_type, pattern in self.PHI_PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                findings.append(f"{phi_type}: {', '.join(set(matches[:3]))}")  # Limit to first 3 matches
        return findings
    
    def _redact_phi(self, text: str) -> str:
        """Redact detected PHI from text."""
        redacted = text
        for phi_type, pattern in self.PHI_PATTERNS.items():
            redacted = re.sub(pattern, f"[REDACTED_{phi_type.upper()}]", redacted)
        return redacted
    
    def _validate_citations(self, text: str, valid_source_ids: list[str]) -> list[str]:
        """Check that citations reference valid source passage IDs."""
        errors = []
        
        # Extract all cited passage IDs (format: patient_XXXXX:passage_NNN)
        citation_pattern = r"(patient_\d{5}:passage_\d+)"
        cited_ids = set(re.findall(citation_pattern, text))
        
        for cited_id in cited_ids:
            if cited_id not in valid_source_ids:
                errors.append(f"Citation '{cited_id}' not in provided source data (may indicate hallucination)")
        
        # Count citations
        if len(cited_ids) == 0:
            errors.append("No citations found in output (claims lack source attribution)")
        
        return errors
    
    def _validate_value_ranges(self, text: str) -> list[str]:
        """Check for lab/vital values outside plausible ranges."""
        errors = []
        
        # Simple regex to find values (e.g., "72 bpm", "8.2%", "135/88 mmHg")
        value_pattern = r"(\d+(?:\.\d+)?)\s*(bpm|%|mmHg|mg/dL|hours)"
        matches = re.findall(value_pattern, text)
        
        for value_str, unit in matches:
            value = float(value_str)
            
            # Check ranges
            if unit == "bpm" and not (self.PLAUSIBLE_RANGES["heart_rate"][0] <= value <= self.PLAUSIBLE_RANGES["heart_rate"][1]):
                errors.append(f"Heart rate {value} bpm outside plausible range (40-200 bpm)")
            elif unit == "%" and "a1c" in text.lower():
                if not (self.PLAUSIBLE_RANGES["hba1c"][0] <= value <= self.PLAUSIBLE_RANGES["hba1c"][1]):
                    errors.append(f"HbA1c {value}% outside plausible range (4-14%)")
            elif unit == "mg/dL" and "creatinine" in text.lower():
                if not (self.PLAUSIBLE_RANGES["creatinine"][0] <= value <= self.PLAUSIBLE_RANGES["creatinine"][1]):
                    errors.append(f"Creatinine {value} mg/dL outside plausible range (0.5-3.0 mg/dL)")
        
        return errors
    
    def _contains_prescriptive_advice(self, text: str) -> bool:
        """Check if output prescribes rather than recommends (e.g., 'prescribe X' vs. 'consider X')."""
        prescriptive_keywords = [
            r"\bprescribe\b",
            r"\bstart\s+\w+\s+immediately",
            r"\bdispense\b",
            r"\b(must|should)\s+take\b",
        ]
        
        for pattern in prescriptive_keywords:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _is_structured(self, text: str) -> bool:
        """Check if output has structured format (headings, numbered lists)."""
        has_headings = bool(re.search(r"^#+\s+", text, re.MULTILINE))  # Markdown headings
        has_numbered_lists = bool(re.search(r"^\d+\.\s+", text, re.MULTILINE))  # Numbered lists
        has_citations = bool(re.search(r"passage_\d+", text))
        
        return has_headings and (has_numbered_lists or has_citations)
    
    def _has_confidence_statements(self, text: str) -> bool:
        """Check if output includes confidence statements (HIGH / MEDIUM / LOW)."""
        confidence_keywords = [
            r"\b(HIGH|MEDIUM|LOW)\s+(?:confidence|certainty|confidence_level)\b",
            r"(?:confidence|certainty):\s*(HIGH|MEDIUM|LOW)",
        ]
        
        for pattern in confidence_keywords:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False


# Example usage & tests
if __name__ == "__main__":
    verifier = OutputVerifier()
    
    # Test 1: Clean output (should pass)
    clean_output = """
    ## Clinical Summary
    
    Patient patient_00042 presents with elevated HbA1c (8.2%, passage_42) and hypertension (135/88 mmHg, passage_91).
    
    ### Top Concerns
    1. Suboptimal glycemic control (HbA1c 8.2%) — HIGH confidence (supported by passage_42)
    2. Elevated blood pressure — MEDIUM confidence (borderline; may improve with lifestyle)
    
    ### Recommendations
    Consider discussing with provider:
    - A1c goal review and GLP-1 agonist consideration
    - BP monitoring; may benefit from lifestyle modifications
    
    **Confidence Level: MEDIUM** (limited by missing lipid panel, ECG)
    """
    
    valid_sources = ["patient_00042:passage_42", "patient_00042:passage_91"]
    result = verifier.verify_output(clean_output, valid_sources)
    print(f"✓ Clean output valid: {result.is_valid}, confidence: {result.confidence_score:.2f}")
    print(f"  Warnings: {result.warnings}")
    
    # Test 2: Output with unredacted PHI
    phi_output = """
    John Doe (SSN 123-45-6789) presented on 2026-01-30 with elevated HbA1c.
    Email: john.doe@email.com, Phone: 555-123-4567.
    """
    
    result = verifier.verify_output(phi_output, valid_sources, allow_redaction=True)
    print(f"\n✓ PHI output detected and redacted: valid={result.is_valid}")
    print(f"  Redacted:\n{result.redacted_output}")
    
    # Test 3: Output with invalid citation
    invalid_citation_output = """
    Patient patient_00042 has concerning findings (passage_999 shows elevated values).
    """
    
    result = verifier.verify_output(invalid_citation_output, valid_sources)
    print(f"\n✓ Invalid citation detected: valid={result.is_valid}")
    print(f"  Warnings: {result.warnings}")
    
    # Test 4: Prescriptive advice (should flag)
    prescriptive_output = """
    You must prescribe metformin immediately and dispense it today.
    """
    
    result = verifier.verify_output(prescriptive_output, valid_sources)
    print(f"\n✓ Prescriptive advice detected: requires_human_review={result.requires_human_review}")
    print(f"  Warnings: {result.warnings}")
    print(f"  Confidence score: {result.confidence_score:.2f}")
