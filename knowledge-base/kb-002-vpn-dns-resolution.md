# KB Article: VPN Connected but Internal Hostnames Do Not Resolve

**Audience:** Internal helpdesk / support agents  
**Last Updated:** 2026-02-09

## Issue
User appears connected to VPN, but internal sites fail due to DNS resolution errors.

## Quick Checks
- [ ] Confirm VPN client status is connected.
- [ ] Run `ipconfig /all` and verify corporate DNS suffix/search list.
- [ ] Run `nslookup` against an internal hostname.
- [ ] Flush DNS cache and reconnect VPN.

## Resolution Steps for Agents
1. Validate VPN auth success and tunnel status.
2. Compare current DNS settings against the standard client profile.
3. If DNS entries are missing, reinstall or refresh VPN profile package.
4. Reconnect VPN and rerun `nslookup` test.
5. Confirm user access to at least one internal URL before closing ticket.

## Escalation Criteria
- DNS still fails after profile refresh and reconnect.
- Affected user cohort exceeds one person (possible profile rollout issue).
- VPN gateway logs show policy push failures.

## Related Ticket
- `tickets/ticket-03-vpn-dns.md`
