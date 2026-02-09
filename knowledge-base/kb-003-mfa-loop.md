# KB Article: Troubleshooting MFA Login Loops

**Audience:** Internal helpdesk / support agents  
**Last Updated:** 2026-02-09

## Issue
User enters a valid MFA code, but the prompt reloads repeatedly and authentication does not complete.

## Quick Checks
- [ ] Confirm device time is set to automatic.
- [ ] Clear browser cache and cookies.
- [ ] Retry in Incognito/private mode.
- [ ] Retry in an alternate supported browser.

## Resolution Steps for Agents
1. Verify account state in the identity admin console.
2. Confirm there is no lockout or conditional access denial.
3. Revoke or reset MFA token/session state for the user.
4. Ask user to sign in again and re-enroll MFA if prompted.
5. Confirm successful login completion before closure.

## Escalation Criteria
- MFA loop persists after token reset and browser isolation steps.
- Conditional access logs show policy conflict requiring identity-team review.
- Multiple users report the same behavior in a short window.

## Related Ticket
- `tickets/ticket-01-mfa-loop.md`
