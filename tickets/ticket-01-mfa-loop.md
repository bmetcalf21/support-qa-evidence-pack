# Ticket ID: [BLP-1] - [MFA Login Loop - User stuck at authentication prompt]

**Status:** Resolved
**Priority:** [Medium]
**Tags:** [MFA, Login, SSO, User-Access]

## User Report
**User:** [Brandon Metcalf]
**Issue:** User reports they cannot log in. States "I keep getting looped back to the enter code screen." After entering valid credentials, the browser refreshes the MFA prompt indefinitely without sending a push notification.

## Triage & Troubleshooting
1. **Verified User:** Checked Active Directory; account is not locked.
2. **Environment:** User is on Chrome / Windows 10.
3. **Action:** Asked user to clear cache/cookies and attempt Incognito mode.
4. **Result:** Issue persisted in Incognito.
5. **Action:** Reset MFA token on backend.

## Resolution
User successfully logged in after MFA token reset. Guided user through new QR code setup.

## Root Cause
MFA token desync due to time drift on user device.