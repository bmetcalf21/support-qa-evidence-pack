# KB Article: Password Reset Email Not Received

**Audience:** Internal support agents  
**Last Updated:** 2026-03-27

## Use This When
The user completes the password-reset form successfully, but the reset email never arrives.

## Quick Checks
- [ ] Confirm the account is active and not locked.
- [ ] Confirm the exact email address entered in the reset form.
- [ ] Ask user to check spam/junk and mailbox rules.
- [ ] Verify whether reset events exist in auth logs.

## First-Line Path
1. Verify destination email in identity directory profile.
2. If alias/domain is outdated, update profile to current primary address.
3. Trigger a new password reset email.
4. Keep user on the call and confirm message delivery.
5. Confirm successful password reset and login.

## Escalate When
- No reset event appears in logs after trigger.
- Multiple users report reset-email non-delivery.
- SMTP provider or notification service errors are present.

## Related Case
- `cases/case-02-password-reset-email.md`
