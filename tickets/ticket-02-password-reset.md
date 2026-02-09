# Ticket: TICKET-002 - Password Reset Email Not Received

## Metadata
- Platform: Zendesk-style workflow (simulated)
- Status: Resolved
- Priority: Medium
- Category: Access / Password
- User: Sales manager (simulated)
- Environment: Web app login portal, Chrome on macOS
- Impact: Single user unable to reset password
- Tags: Password-Reset, Email-Delivery, Access

## User Report
User reports that "Forgot Password" completes successfully on screen, but no reset email arrives after multiple attempts.

## Triage and Troubleshooting
1. Verified account status in identity directory; account was active and not locked.
2. Confirmed the user entered the expected corporate email address.
3. Asked user to check spam/junk and mailbox filtering rules.
4. Reviewed auth logs and found reset emails sent to an outdated alias.
5. Updated primary email attribute in directory profile and retriggered password reset flow.

## Resolution
Password reset email delivered to the corrected address. User completed reset and signed in successfully.

## Root Cause
Directory profile retained an outdated email alias after domain migration, so reset notifications were routed incorrectly.

## Evidence
- Sanitized log note: Reset email events present, routed to stale alias prior to profile correction.

## Related Knowledge Base
- `knowledge-base/kb-001-password-reset-email-delivery.md`
