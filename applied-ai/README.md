# Applied AI: Support Triage Assistant

This folder shows one narrow applied-AI use case that fits the rest of the repository: helping first-line support decide whether to answer from existing guidance, ask for more information, or escalate.

## Why This Exists
- It supports the support-operations thesis instead of distracting from it.
- It uses explicit policy and evaluation criteria.
- It avoids stronger claims than the repo can justify.

## Scope
The assistant is designed for three decisions only:
- `answer`: respond from a known KB path
- `clarify`: ask for missing information before proceeding
- `escalate`: hand off because the issue is risky, unclear, or outside first-line ownership

## Files
- `assistant-policy.md`: response contract, guardrails, and escalation rules
- `evaluation-set.json`: small labeled examples tied to the cases, KBs, and QA artifacts in this repo
- `evaluate.py`: standard-library scoring script for candidate predictions

## Quick Check
Run the scorer against a prediction file in this format:

```json
[
  {
    "case_id": "eval-01",
    "decision": "answer",
    "knowledge_refs": ["knowledge-base/kb-003-mfa-loop.md"]
  }
]
```

```bash
python3 applied-ai/evaluate.py predictions.json
```

## What It Demonstrates
- AI workflow design grounded in operational policy
- Guardrails for when not to automate
- A lightweight evaluation approach for answer-versus-escalate accuracy

## Deliberate Limits
- No claim of production deployment
- No fake analytics or dashboarding
- No generic chatbot claims beyond the artifacts in this folder
