#!/usr/bin/env python3
"""Score triage decisions against the local evaluation set."""

from __future__ import annotations

import json
import sys
from pathlib import Path


EVAL_PATH = Path(__file__).with_name("evaluation-set.json")
ALLOWED_DECISIONS = {"answer", "clarify", "escalate"}


def load_json(path: Path, label: str) -> list[dict]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid {label} JSON") from exc
    except OSError as exc:
        raise ValueError(f"{label} input is unavailable") from exc
    if not isinstance(value, list):
        raise ValueError(f"{label} input must be a JSON list")
    return value


def index_by_unique_case_id(items: list[dict], label: str) -> dict[str, dict]:
    """Index records by case ID and reject ambiguous duplicate inputs."""
    indexed = {}
    for item in items:
        if not isinstance(item, dict):
            raise ValueError(f"{label} records must be objects")
        case_id = item.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"{label} case_id is required and must be non-empty text")
        if case_id in indexed:
            raise ValueError(f"Duplicate {label} case_id: {case_id}")
        indexed[case_id] = item
    return indexed


def reference_set(item: dict, field: str, case_id: str) -> set[str]:
    if field not in item:
        raise ValueError(f"{field} is required for {case_id}")
    values = item[field]
    if not isinstance(values, list):
        raise ValueError(f"{field} must be a list for {case_id}")
    if any(not isinstance(value, str) or not value for value in values):
        raise ValueError(f"{field} must contain non-empty strings for {case_id}")
    if len(values) != len(set(values)):
        raise ValueError(f"{field} must contain unique values for {case_id}")
    return set(values)


def score_predictions(eval_cases: list[dict], predictions: list[dict]) -> dict:
    """Score decisions and supporting references against evaluation cases."""
    expected_by_id = index_by_unique_case_id(eval_cases, "evaluation")
    prediction_by_id = index_by_unique_case_id(predictions, "prediction")

    for case_id, predicted in prediction_by_id.items():
        decision = predicted.get("decision")
        if decision not in ALLOWED_DECISIONS:
            allowed = ", ".join(sorted(ALLOWED_DECISIONS))
            raise ValueError(f"decision must be one of {allowed} for {case_id}")
        reference_set(predicted, "knowledge_refs", case_id)

    decision_total = len(expected_by_id)
    decision_correct = 0
    citation_total = 0
    citation_correct = 0
    missing = []
    unexpected = sorted(case_id for case_id in prediction_by_id if case_id not in expected_by_id)

    for case_id, expected in expected_by_id.items():
        expected_decision = expected.get("expected_decision")
        if not isinstance(expected_decision, str) or not expected_decision:
            raise ValueError(
                f"expected_decision is required and must be non-empty text for {case_id}"
            )
        if expected_decision not in ALLOWED_DECISIONS:
            allowed = ", ".join(sorted(ALLOWED_DECISIONS))
            raise ValueError(f"expected_decision must be one of {allowed} for {case_id}")
        expected_refs = reference_set(expected, "expected_refs", case_id)
        citation_total += 1

        predicted = prediction_by_id.get(case_id)
        if predicted is None:
            missing.append(case_id)
            continue

        if predicted.get("decision") == expected_decision:
            decision_correct += 1

        predicted_refs = reference_set(predicted, "knowledge_refs", case_id)
        if expected_refs == predicted_refs:
            citation_correct += 1

    decision_accuracy = decision_correct / decision_total if decision_total else 0.0
    citation_accuracy = citation_correct / citation_total if citation_total else 0.0

    return {
        "decision_accuracy": round(decision_accuracy, 3),
        "decision_correct": decision_correct,
        "decision_total": decision_total,
        "citation_accuracy": round(citation_accuracy, 3),
        "citation_correct": citation_correct,
        "citation_total": citation_total,
        "missing_predictions": missing,
        "unexpected_case_ids": unexpected,
    }


def main() -> int:
    if len(sys.argv) not in {2, 3} or (len(sys.argv) == 3 and sys.argv[2] != "--require-perfect"):
        print("Usage: python3 applied-ai/evaluate.py <predictions.json> [--require-perfect]")
        print("Prediction format: [{\"case_id\": \"eval-01\", \"decision\": \"answer\", \"knowledge_refs\": [\"...\"]}]")
        return 1
    require_perfect = len(sys.argv) == 3

    predictions_path = Path(sys.argv[1])
    eval_cases = load_json(EVAL_PATH, "evaluation-set")
    predictions = load_json(predictions_path, "predictions")
    summary = score_predictions(eval_cases, predictions)

    print(json.dumps(summary, indent=2))
    if require_perfect and (
        summary["decision_correct"] != summary["decision_total"]
        or summary["citation_correct"] != summary["citation_total"]
        or summary["missing_predictions"]
        or summary["unexpected_case_ids"]
    ):
        return 2
    return 0


def cli() -> int:
    try:
        return main()
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except (OSError, KeyError, TypeError):
        print("error: predictions input is unavailable or invalid", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
