#!/usr/bin/env python3
"""Score triage decisions against the local evaluation set."""

from __future__ import annotations

import json
import sys
from pathlib import Path


EVAL_PATH = Path(__file__).with_name("evaluation-set.json")


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 applied-ai/evaluate.py <predictions.json>")
        print("Prediction format: [{\"case_id\": \"eval-01\", \"decision\": \"answer\", \"knowledge_refs\": [\"...\"]}]")
        return 1

    predictions_path = Path(sys.argv[1])
    eval_cases = load_json(EVAL_PATH)
    predictions = load_json(predictions_path)

    expected_by_id = {case["case_id"]: case for case in eval_cases}
    prediction_by_id = {item["case_id"]: item for item in predictions}

    decision_total = len(expected_by_id)
    decision_correct = 0
    citation_total = 0
    citation_correct = 0
    missing = []
    unexpected = sorted(case_id for case_id in prediction_by_id if case_id not in expected_by_id)

    for case_id, expected in expected_by_id.items():
        predicted = prediction_by_id.get(case_id)
        if predicted is None:
            missing.append(case_id)
            continue

        if predicted.get("decision") == expected["expected_decision"]:
            decision_correct += 1

        expected_refs = set(expected.get("expected_refs", []))
        if expected_refs:
            citation_total += 1
            predicted_refs = set(predicted.get("knowledge_refs", []))
            if expected_refs.issubset(predicted_refs):
                citation_correct += 1

    decision_accuracy = decision_correct / decision_total if decision_total else 0.0
    citation_accuracy = citation_correct / citation_total if citation_total else 0.0

    summary = {
        "decision_accuracy": round(decision_accuracy, 3),
        "decision_correct": decision_correct,
        "decision_total": decision_total,
        "citation_accuracy": round(citation_accuracy, 3),
        "citation_correct": citation_correct,
        "citation_total": citation_total,
        "missing_predictions": missing,
        "unexpected_case_ids": unexpected,
    }

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
