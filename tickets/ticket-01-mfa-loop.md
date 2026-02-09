# Ticket: TICKET-001 - MFA Login Loop

## Metadata
- Platform: Jira Service Management (simulated)
- Status: Resolved
- Priority: Medium
- Category: Access / MFA
- User: Brandon Metcalf (simulated)
- Environment: Chrome on Windows 10
- Impact: Single user unable to authenticate
- Tags: MFA, Login, SSO, User-Access

## User Report
User states: "I keep getting looped back to the enter code screen." After valid credentials, the MFA prompt reloads repeatedly and no push notification is received.

## Triage and Troubleshooting
1. Verified account in directory; account was active and not locked.
2. Confirmed browser and OS details (Chrome, Windows 10).
3. Asked user to clear cache/cookies and retry in Incognito mode.
4. Issue persisted in Incognito mode.
5. Reset MFA token in backend.

## Resolution
User logged in successfully after MFA token reset. Guided user through new QR code enrollment.

## Root Cause
MFA token desync caused by device time drift.

## Evidence
- `screenshots/jsm-ticket-01-mfa-loop.jpeg`
