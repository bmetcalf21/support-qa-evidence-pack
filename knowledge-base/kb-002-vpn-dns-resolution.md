# KB Article: VPN Connected but Internal Hostnames Do Not Resolve

**Audience:** Internal support agents  
**Last Updated:** 2026-03-27

## Use This When
The VPN client shows a successful connection, but internal hostnames or URLs still fail due to DNS resolution errors.

## Quick Checks
- [ ] Confirm VPN client status is connected.
- [ ] Run `ipconfig /all` and verify corporate DNS suffix/search list.
- [ ] Run `nslookup` against an internal hostname.
- [ ] Flush DNS cache and reconnect VPN.

## First-Line Path
1. Validate VPN auth success and tunnel status.
2. Compare current DNS settings against the standard client profile.
3. If DNS entries are missing, reinstall or refresh VPN profile package.
4. Reconnect VPN and rerun `nslookup` test.
5. Confirm user access to at least one internal URL before closing ticket.

## Escalate When
- DNS still fails after profile refresh and reconnect.
- Affected user cohort exceeds one person (possible profile rollout issue).
- VPN gateway logs show policy push failures.

## Related Case
- `cases/case-03-vpn-dns-resolution.md`
