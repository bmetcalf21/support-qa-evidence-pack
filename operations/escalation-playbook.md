# Runbook: Support Escalation Playbook

**Owner:** Support operations portfolio example  
**Last Updated:** 2026-03-27

## Purpose
Provide a repeatable escalation workflow when first-line troubleshooting does not restore service or risk increases.

## Escalation Triggers
- Incident impact extends beyond one user.
- Suspected defect or policy misconfiguration blocks resolution.
- Security or access-control behavior is unclear.
- User-impacting issue persists after standard troubleshooting checklist.

## Do Not Escalate Yet When
- The issue matches a documented KB path and the first-line recovery steps have not been tried.
- The report is still missing basic environment details or exact symptoms.
- The user has not yet confirmed whether the issue is resolved after a low-risk corrective step.

## Severity Guide

| Severity | Typical Impact | Escalation Target | SLA for Handoff |
| --- | --- | --- | --- |
| High | Multiple users or business-critical workflow blocked | Engineering + Incident Manager | 15 minutes |
| Medium | Single team blocked or repeated user impact | Engineering queue owner | 1 hour |
| Low | Workaround available, non-blocking behavior issue | Product/engineering backlog | Same business day |

## Required Evidence Before Escalation
- Incident summary in one sentence.
- User impact statement (who is blocked and how).
- Environment details (app/client version, OS/browser, network context).
- Exact steps attempted and outcomes.
- Sanitized logs, screenshot references, or command output.
- Clear reproduction status (`always`, `intermittent`, `unable to reproduce`).

## Handoff Format
1. **What happened:** concise issue statement.
2. **Who is impacted:** user/team count and urgency.
3. **What was tested:** ordered troubleshooting actions.
4. **What failed/succeeded:** decision points and current state.
5. **What is needed:** specific request (fix, policy review, bug triage).

## Communication Rules
- Keep external updates factual; avoid root-cause speculation.
- Log timestamps for all status updates and ownership changes.
- Confirm receiving team acknowledges ownership before closing first-line ticket.

## Related Files
- `operations/triage-decision-guide.md`
- `qa/bugs/bug-001-expired-password-redirect.md`
- `cases/case-03-vpn-dns-resolution.md`

## Closure Checklist
- [ ] Escalated team accepted handoff.
- [ ] User/team notified of status and next update time.
- [ ] Ticket linked to bug/work item if defect confirmed.
- [ ] Final resolution and root cause documented.
