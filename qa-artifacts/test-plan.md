# Test Plan: Access and Connectivity Regression Pack

**Owner:** Support QA (simulated)  
**Last Updated:** 2026-02-09  
**Scope:** Login, MFA, password reset, VPN-DNS, and client sync reliability

## Objective
Validate that core access and connectivity workflows behave correctly after identity, client, or policy updates.

## In Scope
- Username/password authentication outcomes
- MFA challenge and recovery behavior
- Password reset delivery and completion flow
- VPN connection and internal DNS resolution
- Client sync conflict-state messaging

## Out of Scope
- Load/performance testing
- Multi-region disaster recovery
- Production data validation

## Test Environment
- Staging identity provider and web application
- Corporate VPN test profile
- Simulated user accounts and sanitized logs

## Entry Criteria
- Staging environment available
- Test accounts provisioned
- Latest build deployed

## Exit Criteria
- All critical-path tests executed
- No open Sev-3+ defects blocking release
- Test report and defect links published

## Test Matrix

| ID | Scenario | Steps (Summary) | Expected Result | Result |
| --- | --- | --- | --- | --- |
| TP-01 | Valid login + valid MFA | Sign in with active user and valid MFA code | Dashboard loads and session is established | Pending |
| TP-02 | Invalid password | Sign in with valid username and wrong password | User sees generic credential error | Pending |
| TP-03 | MFA loop recovery | Trigger MFA loop and perform token reset workflow | User can re-enroll MFA and sign in | Pending |
| TP-04 | Password reset email delivery | Submit reset and validate delivery to current primary email | Reset email arrives and flow completes | Pending |
| TP-05 | Expired password routing | Sign in with expired password test user | User is sent to change-password flow | Pending |
| TP-06 | VPN connected, DNS validation | Connect VPN and query internal hostname | Internal hostname resolves and internal URL opens | Pending |
| TP-07 | VPN profile corruption recovery | Use corrupted profile then reinstall profile package | DNS settings restored and resolution succeeds | Pending |
| TP-08 | Client sync conflict messaging | Create two offline edits and reconnect | Conflict warning is shown without false success state | Pending |

## Defect References
- `qa-artifacts/bugs/bug-001-expired-password-redirect.md`
- `qa-artifacts/bugs/bug-002-client-sync-conflict-state.md`
