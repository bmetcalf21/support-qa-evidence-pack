# Bug ID: BUG-001 - Expired Password Redirects to Home

**Severity:** S3 - Major  
**Environment:** Staging - Chrome 122 / Windows 11

## Description
When a user signs in with an expired password, the app redirects to `/home` in an unauthenticated state instead of forcing the password-change flow.

## Steps to Reproduce
1. Open the login page.
2. Enter username `test_user_expired`.
3. Enter valid but expired password.
4. Select **Sign In**.

## Expected Result
User is redirected to `/change-password` with clear instructions to update credentials.

## Actual Result
User is redirected to `/home`, sees no actionable message, and cannot proceed.

## Evidence
- Sanitized auth trace indicates `PASSWORD_EXPIRED` flag is set before redirect handler routes to `/home`.

## Impact
Users with expired credentials are blocked from self-service recovery and generate avoidable support volume.
