# Case 03: VPN Connected but Internal DNS Fails

## Snapshot
- Queue: connectivity support
- Status: resolved
- Priority: high
- Requester: single user (sanitized)
- Environment: Windows 11 laptop with corporate VPN client 5.x
- Outcome: resolved at first line after structured troubleshooting

## Intake
The user reported that the VPN client showed a successful connection, but internal hostnames still failed to resolve.

## Triage Notes
1. Confirmed the VPN tunnel was authenticated and connected.
2. Captured `ipconfig /all` output and found missing corporate DNS suffix entries.
3. Ran `nslookup intranet.corp` and confirmed the request was going to local ISP DNS.
4. Flushed DNS cache and restarted the VPN client with no improvement.
5. Reinstalled the VPN profile package and reconnected.
6. Re-ran `nslookup intranet.corp` and confirmed internal resolution succeeded.

## Decision
The issue stayed at first line because it matched a known VPN profile failure pattern and recovered after the standard path. If the profile refresh had failed or more users were affected, the next step would have been escalation.

## Resolution
Reinstalling the VPN profile restored the expected DNS settings and internal services became reachable again.

## Root Cause
The VPN client profile was outdated or corrupted and no longer applied the required DNS configuration for split-tunnel resolution.

## Related Artifacts
- `knowledge-base/kb-002-vpn-dns-resolution.md`
- `operations/triage-decision-guide.md`
- `operations/escalation-playbook.md`
