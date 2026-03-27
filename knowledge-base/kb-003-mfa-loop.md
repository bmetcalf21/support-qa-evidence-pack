# KB Article: Troubleshooting MFA Login Loops

**Audience:** Internal support agents  
**Last Updated:** 2026-03-27

## Use This When
The user enters valid credentials and a valid MFA code, but the sign-in flow returns to the MFA prompt instead of completing.

## Quick Checks
- [ ] Confirm device time is set to automatic.
- [ ] Clear browser cache and cookies.
- [ ] Retry in Incognito/private mode.
- [ ] Retry in an alternate supported browser.

## First-Line Path
1. Verify account state in the identity admin console.
2. Confirm there is no lockout or conditional access denial.
3. Revoke or reset MFA token/session state for the user.
4. Ask user to sign in again and re-enroll MFA if prompted.
5. Confirm successful login completion before closure.

## Escalate When
- MFA loop persists after token reset and browser isolation steps.
- Conditional access logs show policy conflict requiring identity-team review.
- Multiple users report the same behavior in a short window.

## Related Case
- `cases/case-01-mfa-loop.md`
