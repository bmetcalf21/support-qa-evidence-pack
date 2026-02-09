# Ticket: TICKET-003 - VPN Connected but Internal DNS Fails

## Metadata
- Platform: Freshdesk-style workflow (simulated)
- Status: Resolved
- Priority: High
- Category: VPN-DNS
- User: Finance analyst (simulated)
- Environment: Windows 11 laptop, corporate VPN client 5.x
- Impact: Single user blocked from internal web tools
- Tags: VPN, DNS, Connectivity, Remote-Access

## User Report
User confirms VPN status shows "Connected" but internal hostnames do not resolve, causing access failures to internal dashboards.

## Triage and Troubleshooting
1. Confirmed VPN tunnel state was up and authentication completed.
2. Collected `ipconfig /all` output and found missing corporate DNS suffix entries.
3. Ran `nslookup intranet.corp` and observed timeout using local ISP DNS.
4. Flushed DNS cache and restarted VPN client; issue persisted.
5. Reinstalled VPN profile package and reconnected.
6. Re-ran `nslookup intranet.corp`; internal hostname resolved successfully.

## Resolution
After VPN profile reinstall, corporate DNS settings and suffix search list were restored. Internal services became reachable.

## Root Cause
Corrupted or outdated VPN client profile omitted required DNS configuration for split-tunnel name resolution.

## Evidence
- Sanitized command result: `nslookup intranet.corp` failed before profile reinstall and succeeded after reconnect.

## Related Knowledge Base
- `knowledge-base/kb-002-vpn-dns-resolution.md`
