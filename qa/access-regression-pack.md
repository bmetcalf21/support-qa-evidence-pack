# Access and Support Regression Pack

**Owner:** Support QA portfolio example  
**Last Updated:** 2026-03-27  
**Purpose:** Preserve coverage for support-critical flows after identity, client, or policy changes

This is a candidate regression pack derived from the support cases and bug reports in this repository. It is a planning artifact, not a claim of completed test execution.

## Coverage Areas
- Login and MFA success and failure paths
- Password reset delivery and recovery
- VPN connection with internal DNS resolution
- Client sync conflict messaging

## Coverage Matrix

| ID | Scenario | Why It Matters | Expected Result |
| --- | --- | --- | --- |
| RG-01 | Valid login with valid MFA | Confirms the critical access happy path still works | Session is created and the dashboard loads |
| RG-02 | Invalid password handling | Verifies safe error handling for common auth failures | User receives a generic credential error with no sensitive detail |
| RG-03 | MFA loop recovery | Covers a known support case and KB path | User can complete token reset, re-enroll MFA, and sign in |
| RG-04 | Password reset email delivery | Protects a support-critical self-service recovery path | Reset email is sent to the current primary address and the flow completes |
| RG-05 | Expired password routing | Guards against a defect that increases support volume | User is sent to the password-change flow instead of an unusable landing page |
| RG-06 | VPN connected, DNS validation | Confirms remote-access connectivity after client or policy changes | Internal hostname resolution succeeds after VPN connection |
| RG-07 | VPN profile recovery | Covers the standard path for a known DNS-profile issue | Profile refresh restores the correct DNS settings |
| RG-08 | Client sync conflict messaging | Verifies the client does not overstate success during a conflict | Conflict warning appears before or instead of any success state |

## Defect References
- `qa/bugs/bug-001-expired-password-redirect.md`
- `qa/bugs/bug-002-client-sync-conflict-state.md`
