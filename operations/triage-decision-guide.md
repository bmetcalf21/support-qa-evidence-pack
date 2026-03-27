# Triage Decision Guide

## Purpose
Use this guide to decide whether first-line support should answer from known guidance, ask a clarifying question, or escalate for specialist ownership.

## Decision Table

| Situation | Action | Reason |
| --- | --- | --- |
| Known single-user issue with a documented recovery path | Answer | Fastest safe path when the guidance is already established |
| Report is ambiguous or missing key context | Clarify | Avoids misrouting and weak troubleshooting |
| Multi-user impact, security uncertainty, suspected defect, or failed standard path | Escalate | Specialist review is justified |

## Answer at First Line When
- Impact is limited to one user.
- The issue matches a documented KB article or repeatable case pattern.
- The troubleshooting steps are low risk and reversible.
- The agent can verify success before closure.

## Ask for Clarification When
- Error wording, timing, or environment details are missing.
- The user report is too vague to choose a KB path.
- Reproduction is inconsistent or unclear.
- The current evidence is not enough to separate user error, policy issue, and product defect.

## Escalate When
- More than one user or team is affected.
- Identity, permissions, or security behavior is unclear.
- A suspected defect or policy misconfiguration blocks resolution.
- Standard troubleshooting has already failed.
- Ownership needs to move to engineering, identity, network, or incident management.

## Minimum Evidence Before Escalation
- One-sentence issue summary
- User impact statement
- Environment details
- Steps already attempted
- Current status after troubleshooting
- Sanitized logs, screenshots, or command output when available

## Related Examples
- `cases/case-01-mfa-loop.md`
- `cases/case-02-password-reset-email.md`
- `cases/case-03-vpn-dns-resolution.md`
- `operations/escalation-playbook.md`
