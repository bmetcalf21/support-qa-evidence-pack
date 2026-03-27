# Case 01: MFA Login Loop

## Snapshot
- Queue: access support
- Status: resolved
- Priority: medium
- Requester: single user (sanitized)
- Environment: Chrome on Windows 10
- Outcome: resolved at first line

## Intake
The user could enter valid credentials but kept getting sent back to the MFA prompt and did not receive a push notification.

## Triage Notes
1. Verified the account was active and not locked.
2. Captured browser and OS details to rule out unsupported-client issues.
3. Tested browser isolation through cache clearing and Incognito mode.
4. Reset MFA token state after the issue persisted across browser isolation.
5. Guided re-enrollment after successful sign-in.

## Decision
The issue matched a known single-user access pattern, so it stayed at first line instead of being escalated.

## Resolution
The user signed in successfully after MFA token reset and new QR enrollment.

## Root Cause
MFA token state had drifted out of sync with the device.

## Related Artifacts
- `knowledge-base/kb-003-mfa-loop.md`
- `operations/triage-decision-guide.md`
- `evidence/screenshots/jsm-ticket-01-mfa-loop.jpeg`
