# KB Article: Password Reset Email Not Received

**Audience:** Internal helpdesk / support agents  
**Last Updated:** 2026-02-09

## Issue
User submits "Forgot Password" but never receives a reset email.

## Quick Checks
- [ ] Confirm the account is active and not locked.
- [ ] Confirm the exact email address entered in the reset form.
- [ ] Ask user to check spam/junk and mailbox rules.
- [ ] Verify whether reset events exist in auth logs.

## Resolution Steps for Agents
1. Verify destination email in identity directory profile.
2. If alias/domain is outdated, update profile to current primary address.
3. Trigger a new password reset email.
4. Keep user on the call and confirm message delivery.
5. Confirm successful password reset and login.

## Escalation Criteria
- No reset event appears in logs after trigger.
- Multiple users report reset-email non-delivery.
- SMTP provider or notification service errors are present.

## Related Ticket
- `tickets/ticket-02-password-reset.md`
