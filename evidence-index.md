# Evidence Index

This file maps each artifact to the skill signal it demonstrates.

## Current Verified Evidence

| Evidence ID | Skill Signal | Artifact | Status | Notes |
| --- | --- | --- | --- | --- |
| EV-001 | Ticket triage and resolution quality | `tickets/ticket-01-mfa-loop.md` | Complete | Access incident from report through root cause and resolution |
| EV-002 | Jira Service Management platform exposure | `screenshots/jsm-ticket-01-mfa-loop.jpeg` | Complete | Platform screenshot evidence |
| EV-003 | Repeatable ticket documentation standards | `templates/ticket-template.md` | Complete | Standardized metadata and workflow fields |
| EV-004 | Reusable bug reporting format | `templates/bug-template.md` | Complete | Defect report template with repro and expected/actual |
| EV-005 | Reusable KB authoring format | `templates/kb-template.md` | Complete | Internal help article template |
| EV-006 | Authentication QA coverage examples | `templates/test-cases.md` | Complete | Baseline auth test scenarios |
| EV-007 | Password reset triage and identity-attribute troubleshooting | `tickets/ticket-02-password-reset.md` | Complete | Demonstrates email-delivery root cause analysis |
| EV-008 | Network triage for VPN and DNS failures | `tickets/ticket-03-vpn-dns.md` | Complete | Demonstrates connectivity diagnosis and verification loop |
| EV-009 | KB quality for password reset delivery incidents | `knowledge-base/kb-001-password-reset-email-delivery.md` | Complete | Mapped directly to ticket workflow |
| EV-010 | KB quality for VPN DNS-resolution incidents | `knowledge-base/kb-002-vpn-dns-resolution.md` | Complete | Mapped directly to ticket workflow |
| EV-011 | KB quality for MFA login-loop incidents | `knowledge-base/kb-003-mfa-loop.md` | Complete | Mapped directly to ticket workflow |
| EV-012 | Defect documentation quality for auth failure routing | `qa-artifacts/bugs/bug-001-expired-password-redirect.md` | Complete | Reproducible issue with expected vs actual behavior |
| EV-013 | Defect documentation quality for client sync UX | `qa-artifacts/bugs/bug-002-client-sync-conflict-state.md` | Complete | Captures conflict-state timing defect and user impact |
| EV-014 | Structured regression planning across support-critical flows | `qa-artifacts/test-plan.md` | Complete | Entry/exit criteria with linked defects |
| EV-015 | Escalation process rigor and handoff quality | `runbooks/escalation-playbook.md` | Complete | Severity rubric, evidence requirements, and closure checklist |

## Platform Exposure Tracker (Truth-Safe)

| Platform | Current Evidence | Planned Proof Artifact | Status | Target Date |
| --- | --- | --- | --- | --- |
| Jira Service Management | `screenshots/jsm-ticket-01-mfa-loop.jpeg` | Additional ticket artifacts | Verified | Ongoing |
| ServiceNow | None yet in this repo | Badge/cert screenshot in `badges/` and one simulated ticket | In Progress | February 16, 2026 |
| Freshdesk | Simulated workflow artifact only (no platform screenshot yet): `tickets/ticket-03-vpn-dns.md` | Badge/cert screenshot in `badges/` | In Progress | February 16, 2026 |
| Zendesk | Simulated workflow artifact only (no platform screenshot yet): `tickets/ticket-02-password-reset.md` | Optional screenshot and ticket artifact | In Progress | Backlog |

## Near-Term Build Targets

- Tickets: complete (3 total)
- KB articles: complete (3 total)
- Bug reports: complete (2 total)
- Test plan: complete (1)
- Runbook: complete (1)
