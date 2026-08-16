# Support Operations Workflow Pack

[![CI](https://github.com/bmetcalf21/support-qa-evidence-pack/actions/workflows/ci.yml/badge.svg)](https://github.com/bmetcalf21/support-qa-evidence-pack/actions/workflows/ci.yml)

This repository is a sanitized portfolio artifact showing how I structure support operations work from intake through resolution, escalation, documentation, and QA follow-through.

It is designed for technical operations, workflow automation, and applied AI roles. The goal is not to simulate a company. The goal is to show operating judgment, documentation discipline, and a practical approach to lightweight AI assistance.

## What This Repo Proves
- I can turn messy support issues into repeatable workflows and decision criteria.
- I can connect case handling, KB content, escalation rules, and QA coverage into one system.
- I can design a narrow AI-assistance layer with explicit guardrails and evaluation instead of vague automation claims.

## Start Here
1. `cases/case-01-mfa-loop.md`
2. `operations/triage-decision-guide.md`
3. `operations/escalation-playbook.md`
4. `applied-ai/README.md`
5. `artifact-map.md`

## Repository Structure
- `cases/`: sanitized support cases showing intake, triage, resolution, and related artifacts
- `knowledge-base/`: agent-facing guidance derived from recurring issues
- `operations/`: triage and escalation guidance for consistent handling
- `qa/`: regression coverage and bug reports tied to support-critical workflows
- `applied-ai/`: assistant policy, retrieval/model harness, evaluation set and scorer, example predictions, and a bounded local smoke-run record
- `evidence/`: proof artifacts for tool exposure and earned credentials
- `templates/`: reusable formats behind the published artifacts

## Where Applied AI Fits
The AI layer is intentionally narrow. It covers one support task: deciding when an assistant should answer from known guidance, ask a clarifying question, or escalate to a human. A provider-neutral harness retrieves only approved repository sources, builds an inspectable context packet, can invoke an operator-supplied local model command over stdin, allowlists citations, and requires an `answer` to cite at least one retrieved knowledge-base source. A committed evidence record shows one validated local model smoke run. It does not verify that free-text reasoning is entailed by a citation and is presented as a tested local harness, not a hosted production service.

## Verify the Evaluator

```bash
python3 -m unittest discover -s tests -v
python3 applied-ai/harness.py "One user enters valid credentials but keeps returning to the MFA prompt."
python3 applied-ai/evaluate.py applied-ai/example-predictions.json --require-perfect
```

`example-predictions.json` is a hand-authored, perfect-by-construction fixture for checking the scorer and CI contract. It is not a model benchmark or evidence of model quality.

`applied-ai/model-run-evidence.json` records one local `qwen3.5:4b` retrieve-invoke-validate smoke run. It demonstrates that the transport path produced and validated a structured response; it is not a benchmark, production result, or broad model-quality claim.

## Portfolio Safety
- All cases are sanitized and illustrative.
- No employer, customer, or production claims are implied.
- No metrics or business outcomes are invented.
- Platform exposure is claimed only where a proof artifact exists in `evidence/`.

## License

No license is granted. All rights reserved.
