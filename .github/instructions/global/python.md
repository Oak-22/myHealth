---
description: "Python production-grade code standards for myHealth"
applyTo: "**/*.py"
---

## Python Version Contract

- **Primary target: Python 3.14.x** (latest stable)
- Use modern language features and stdlib APIs freely—they represent production-grade clarity and stability
- Modern typing, pattern matching, and structural improvements are *not* luxuries; they are maintainability best practices

## Design Philosophy

This is **forward-aligned production code**. Python 3.14 is chosen because:
- **Modern typing** (PEP 696, protocol improvements) promotes correctness in healthcare logic
- **Cleaner syntax** reduces cognitive overhead in sensitive data handling
- **Better error messages** aid debugging in HIPAA-compliance contexts
- **Performance/security improvements** align with production expectations

## Compatibility: The Exception, Not the Rule

- Backward compatibility is *only* required when a constraint is **known and documented**
- If code must support an older Python version, that requirement must be:
  - **Explicit** (noted in comments, docstrings, or config)
  - **Localized** (isolated to that specific module/function)
  - **Justified** (healthcare deployment context, legacy EHR API, compliance tooling, etc.)
- Do not preemptively degrade code to support hypothetical older environments

## Agent Behavior: Intelligent Domain-Aware Flagging

Agents should flag Python 3.14 syntax **only when domain knowledge indicates a real constraint**:

- **Healthcare infrastructure context**: Is this code touching a legacy EHR system, HL7/FHIR API, or hospital-grade database that constrains Python version?
- **Regulatory/compliance tooling**: Does HIPAA audit logging, data warehouse tooling, or compliance scanning impose version limits?
- **Deployment reality**: Will this run in a VPC environment where Python version is locked by security policy or infrastructure-as-code?

**Example flagging (good):**
> "This uses PEP 696 type parameters. If this module interfaces with the HL7 FHIR client (which targets Python 3.10), compatibility shims may be needed in the interface layer. Document the constraint."

**Example NOT flagging (avoid):**
> "You're using `dict | None` syntax. Python 3.9 doesn't support this."
> (Reason: myHealth targets 3.14; no known 3.9 requirement exists.)

**When in doubt**: Ask the user about deployment constraints rather than assuming backward compatibility is needed.