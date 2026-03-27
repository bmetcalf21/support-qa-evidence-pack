# Regression Matrix Template: Access and Recovery

| ID | Scenario | Why It Matters | Expected Result | Status |
| --- | --- | --- | --- | --- |
| RG-01 | Valid login with valid MFA | Protects the primary access path | Session is created successfully | [Planned / Pass / Fail] |
| RG-02 | Invalid password handling | Verifies safe error behavior | Generic credential error is shown | [Planned / Pass / Fail] |
| RG-03 | MFA recovery path | Covers a known support workflow | User can re-enroll MFA and sign in | [Planned / Pass / Fail] |
| RG-04 | Password reset delivery | Protects self-service recovery | Reset email reaches the current primary address | [Planned / Pass / Fail] |
| RG-05 | VPN DNS resolution | Protects remote access to internal services | Internal hostname resolution succeeds | [Planned / Pass / Fail] |
