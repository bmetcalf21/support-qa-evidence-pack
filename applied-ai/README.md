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
- `harness.py`: provider-neutral retrieval, context-packet assembly, optional local model-command invocation, and structured-response validation
- `evaluation-set.json`: small labeled examples tied to the cases, KBs, and QA artifacts in this repo
- `example-predictions.json`: hand-authored, perfect-by-construction input for checking the scorer contract; not a model benchmark
- `model-run-evidence.json`: one validated local `qwen3.5:4b` retrieve-invoke-validate smoke run; not a benchmark or production claim
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
python3 applied-ai/harness.py "One user enters valid credentials but keeps returning to the MFA prompt."
python3 applied-ai/evaluate.py applied-ai/example-predictions.json --require-perfect
python3 -m unittest discover -s tests -v
```

An operator with a local Ollama model can exercise the complete invocation path without an API key:

```bash
python3 applied-ai/harness.py \
  "One user enters valid credentials but keeps returning to the MFA prompt." \
  --limit 20 \
  --model-command ollama run --format json --hidethinking --think=false --nowordwrap qwen3.5:4b
```

`--model-command` is an argv list, not a shell string. The prompt is sent on stdin; nonzero exit, timeout, invalid JSON, invalid schema, unsupported citation, or an `answer` without a retrieved knowledge-base reference fails closed.

Without `--model-command`, the CLI emits the context packet. With it, the CLI emits `{"packet": ..., "response": ...}` after response validation. Citation accuracy uses exact-set agreement across every evaluation case, including an empty expected set for a correct abstention.

## What It Demonstrates
- AI workflow design grounded in operational policy
- Deterministic retrieval from approved repository sources
- Inspectable prompt/context assembly with repository-relative citations
- Structured-response validation that rejects references outside the retrieved set and answers without a retrieved knowledge-base reference
- Guardrails for when not to automate
- A lightweight evaluation approach for answer-versus-escalate accuracy

## Deliberate Limits
- No claim of production deployment
- No bundled model, provider SDK, API key, or model-quality claim
- The committed model-run evidence is one local smoke test, not an evaluation benchmark
- No claim that citation membership proves the response text is semantically entailed by the cited source
- No fake analytics or dashboarding
- No generic chatbot claims beyond the artifacts in this folder
