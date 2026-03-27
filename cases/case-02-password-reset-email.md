# Case 02: Password Reset Email Not Received

## Snapshot
- Queue: access support
- Status: resolved
- Priority: medium
- Requester: single user (sanitized)
- Environment: web login portal in Chrome on macOS
- Outcome: resolved at first line

## Intake
The user completed the password-reset flow successfully on screen, but no reset email arrived after multiple attempts.

## Triage Notes
1. Verified the account was active and not locked.
2. Confirmed the user entered the expected corporate email address.
3. Asked the user to check spam and mailbox rules before changing directory data.
4. Reviewed auth events and found reset notifications routed to an outdated alias.
5. Corrected the primary email attribute and retriggered the reset flow.

## Decision
The issue matched a documented identity-data problem with a low-risk recovery path, so it was handled at first line.

## Resolution
The reset email was delivered to the corrected address, and the user completed password recovery successfully.

## Root Cause
The directory profile still held an outdated email alias after a domain migration.

## Related Artifacts
- `knowledge-base/kb-001-password-reset-email-delivery.md`
- `operations/triage-decision-guide.md`
