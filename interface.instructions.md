---
description: "Interface/boundary rules for integrating modern Python 3.14 with legacy external systems"
applyTo: "**/*.py"
---

## Purpose

This document governs how myHealth's **core Python 3.14 logic** interfaces with external systems that may impose older Python version constraints. Compatibility is necessary at boundaries; **incompatibility in core is not**.

## Principle: Adapter Pattern, Not Degradation

Do not downgrade the entire codebase to accommodate one external system. Instead:

1. **Identify the boundary** (where your code calls/receives from an external system)
2. **Create an adapter module** that handles compatibility concerns
3. **Isolate downgrades** to that adapter; core modules remain 3.14-native
4. **Document the constraint** and the reason (legacy driver, compliance tooling, hospital system, etc.)

### Example Structure
```
myhealth/
├── core/
│   ├── health_analytics.py          # Pure 3.14, no downgrades
│   └── patient_pseudonymizer.py     # Pure 3.14, no downgrades
├── adapters/
│   ├── ehr_integration.py           # ↓ Compatibility adapter for legacy EHR API
│   ├── bedrock_boundary.py          # ↓ Compatibility shim for Bedrock SDK version
│   └── database_driver.py           # ↓ Compatibility layer for old psycopg2 version
└── tests/
    └── test_adapters/               # Test boundaries in isolation
```

## Identifying Boundaries in myHealth

### Known Compatibility Constraints

**AWS Bedrock SDK**
- Constraint: Some Bedrock SDK versions target Python 3.10
- Location: `/adapters/bedrock_boundary.py`
- Pattern: Wrap `boto3` calls; use feature detection for `converse` API vs. older `invoke_model`

**HealthKit Integration** 
- Constraint: iOS/Swift bridge may support only 3.11+
- Location: `/adapters/healthkit_bridge.py`
- Pattern: Version-gate JSON marshalling; document expected iOS SDK versions

**Database Drivers (PostgreSQL/DynamoDB)**
- Constraint: `psycopg3` may target 3.10; DynamoDB SDK version constraints
- Location: `/adapters/database_driver.py`
- Pattern: Feature-detect connection pooling, async patterns

**EHR/HL7 FHIR Client**
- Constraint: Hospital-grade FHIR libraries often target 3.10 or earlier
- Location: `/adapters/ehr_integration.py`
- Pattern: Isolate FHIR data marshalling; pseudonymize before crossing boundary

**Observability/Compliance Tooling**
- Constraint: CloudTrail audit, Lake Formation, HealthOmics may lock Python version
- Location: `/adapters/compliance_logging.py`
- Pattern: Use boto3 compatibility layer; feature-detect audit APIs

## Adapter Module Rules

### 1. Declare the Constraint Explicitly

```python
"""
EHR Integration Adapter

**Python Compatibility Constraint**: This module targets Python 3.10
for compatibility with the hospital's HL7 FHIR client (v1.8).

Core modules (myhealth/core/) remain Python 3.14-native.
Compatibility is isolated to this adapter.

External System: Epic EHR, FHIR API 4.0.1
Reason: Hospital deployment standard; cannot upgrade FHIR client
"""
```

### 2. Use Feature Detection, Not Version Checks

**Bad (version-checks are fragile):**
```python
import sys
if sys.version_info < (3, 12):
    # use old syntax
```

**Good (feature detection):**
```python
try:
    from typing import TypeAlias  # 3.10+
    TypeAlias = TypeAlias
except ImportError:
    TypeAlias = "TypeAlias"  # Fallback for 3.9
```

### 3. Wrap External Calls Tightly

```python
# adapters/bedrock_boundary.py

def call_bedrock_converse(prompt: str, system: str = "") -> str:
    """
    Bedrock inference wrapper.
    
    Handles version differences in boto3 Bedrock SDK.
    Core modules call this; do not call bedrock-runtime directly.
    """
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    
    # Feature-detect converse API (3.11+) vs. invoke_model (older)
    try:
        response = client.converse(
            modelId="arn:aws:bedrock:...",
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            systemPrompt=system if system else None
        )
        return response["output"]["message"]["content"][0]["text"]
    except AttributeError:
        # Fallback for older boto3 versions
        response = client.invoke_model(
            modelId="...",
            body=json.dumps({"prompt": prompt, "max_tokens_to_sample": 512})
        )
        return json.loads(response["body"].read())["completion"]
```

### 4. Test Boundaries in Isolation

Create `/tests/test_adapters/` with tests that:
- Verify the adapter handles version mismatches gracefully
- Mock external systems (HealthKit, EHR, Bedrock) to avoid real network calls
- Document fallback behavior

```python
# tests/test_adapters/test_bedrock_boundary.py

def test_bedrock_converse_fallback():
    """Verify adapter falls back if converse API unavailable."""
    with patch("boto3.client") as mock_client:
        mock_client.return_value.converse.side_effect = AttributeError
        result = call_bedrock_converse("test prompt")
        assert result is not None
        # Verify fallback invoked
```

### 5. Document Cross-Boundary Data Flow

When pseudonymized health data or sensitive information crosses a boundary, **explicitly redact/marshal** it in the adapter:

```python
# adapters/ehr_integration.py

def send_to_ehr(patient_record: PatientRecord) -> dict:
    """
    Send pseudonymized patient data to EHR.
    
    Data flow:
    1. Core module passes patient_record (uses patient_XXXX IDs)
    2. Adapter redacts timestamps, location info per HIPAA
    3. Marshal to HL7/FHIR JSON (requires older SDK)
    4. POST to hospital EHR endpoint
    
    Constraint: HL7 library targets Python 3.10
    """
    hl7_payload = {
        "resourceType": "Patient",
        "id": patient_record.pseudonym_id,  # patient_XXXX
        "name": [{"given": ["Pseudonymized"]}],  # Redacted
        # ...
    }
    return ehr_client.send(hl7_payload)
```

## When to Escalate (Do NOT Use Adapters For)

- **Core business logic** should never have compatibility downgrades
- **Health data processing** (pseudonymization, validation) must stay 3.14-pure
- **Vector DB ingestion** (Qdrant) must use modern Python; constraint is adapter-level
- If an adapter becomes more than ~200 LOC, the external system may be too incompatible; escalate to architecture review

## Agent Behavior at Boundaries

When reviewing boundary code:

1. **Verify isolation**: Does this adapter touch core logic? (Should not.)
2. **Check documentation**: Is the constraint clearly stated? (Constraint + reason required.)
3. **Validate feature detection**: Are version checks replaced by capability detection? (Yes = good.)
4. **Test coverage**: Are fallback paths tested? (Yes = good.)
5. **Ask about sunset**: Is there a plan to upgrade the external system? (Document in ticket.)

Example agent flag:
> "This adapter calls `converse()` without fallback to `invoke_model()`. If the Bedrock SDK version is constrained to pre-3.11, this will fail. Add feature detection or document the minimum SDK version required."

## Common myHealth Boundaries & Patterns

| Boundary | External System | Constraint | Adapter Location | Pattern |
|----------|-----------------|------------|------------------|---------|
| Bedrock | AWS SDK | boto3 version | `adapters/bedrock_boundary.py` | Feature-detect API version |
| HealthKit | iOS Swift | iOS SDK version | `adapters/healthkit_bridge.py` | Version-gate JSON marshalling |
| PostgreSQL | psycopg3 | Driver version | `adapters/database_driver.py` | Fallback to psycopg2 syntax |
| EHR/FHIR | Hospital HL7 | HL7 library targets 3.10 | `adapters/ehr_integration.py` | Redact + marshal pre-crossing |
| CloudTrail | AWS Audit | boto3 audit APIs | `adapters/compliance_logging.py` | Feature-detect audit actions |

---

**Key Takeaway**: Boundaries are where the real world imposes constraints. Core logic is where you own the standards. Keep them separate.
