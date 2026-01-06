# Bug ID: [BUG-00X] - [Title]

**Severity:** [S3 - Major / S4 - Minor]
**Environment:** [Production / Staging] - [Browser/OS]

## Description
When a user attempts to sign in with an expired password, they are redirected to the homepage instead of the "Change Password" prompt.

## Steps to Reproduce
1. Go to Login Page.
2. Enter username `test_user_expired`.
3. Enter correct (but expired) password.
4. Click "Sign In".

## Expected Result
User should be redirected to `/change-password` screen.

## Actual Result
User is redirected to `/home` (unauthenticated state) with no error message.

## Evidence
[Insert Screenshot or Log Snippet Here]