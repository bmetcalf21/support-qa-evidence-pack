# KB Article: Troubleshooting MFA Loops

**Audience:** Internal Helpdesk / End Users
**Last Updated:** [Date]

## Issue
Users are stuck in a loop where they enter the MFA code, the page reloads, and asks for the code again.

## Quick Fix Checklist
- [ ] Ensure PC/Phone time is set to "Automatic".
- [ ] Clear Browser Cache & Cookies.
- [ ] Try a different browser (Edge/Chrome).

## Resolution Steps for Agents
1. Verify user status in Admin Console.
2. If status is "Active," select **"Revoke MFA Tokens"**.
3. Ask user to log in again; they will be prompted to re-scan the QR code.
4. If issue persists, check Azure AD logs for "Conditional Access" failures.