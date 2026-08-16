import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "applied-ai" / "evaluate.py"
SPEC = importlib.util.spec_from_file_location("support_evaluate", MODULE_PATH)
assert SPEC is not None
evaluate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(evaluate)


class ScorePredictionsTests(unittest.TestCase):
    def test_json_loader_attributes_malformed_evaluation_set(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            malformed = Path(temp_dir) / "evaluation-set.json"
            malformed.write_text("{", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "invalid evaluation-set JSON"):
                evaluate.load_json(malformed, "evaluation-set")

    def test_missing_evaluation_case_id_is_descriptive(self) -> None:
        with self.assertRaisesRegex(ValueError, "evaluation case_id is required"):
            evaluate.score_predictions(
                [{"expected_decision": "answer", "expected_refs": []}],
                [],
            )

    def test_missing_expected_decision_is_descriptive(self) -> None:
        with self.assertRaisesRegex(ValueError, "expected_decision is required"):
            evaluate.score_predictions(
                [{"case_id": "eval-01", "expected_refs": []}],
                [{"case_id": "eval-01", "decision": "answer", "knowledge_refs": []}],
            )

    def test_requires_knowledge_refs_even_for_abstention(self) -> None:
        evaluation_cases = [
            {
                "case_id": "eval-01",
                "expected_decision": "clarify",
                "expected_refs": [],
            }
        ]
        predictions = [{"case_id": "eval-01", "decision": "clarify"}]

        with self.assertRaisesRegex(ValueError, "knowledge_refs is required"):
            evaluate.score_predictions(evaluation_cases, predictions)

    def test_rejects_non_list_knowledge_refs(self) -> None:
        evaluation_cases = [
            {
                "case_id": "eval-01",
                "expected_decision": "answer",
                "expected_refs": ["kb.md"],
            }
        ]
        predictions = [
            {
                "case_id": "eval-01",
                "decision": "answer",
                "knowledge_refs": {"kb.md": False},
            }
        ]

        with self.assertRaisesRegex(ValueError, "knowledge_refs must be a list"):
            evaluate.score_predictions(evaluation_cases, predictions)

    def test_scores_complete_correct_predictions(self):
        cases = [
            {
                "case_id": "eval-01",
                "expected_decision": "answer",
                "expected_refs": ["knowledge-base/article.md"],
            }
        ]
        predictions = [
            {
                "case_id": "eval-01",
                "decision": "answer",
                "knowledge_refs": ["knowledge-base/article.md"],
            }
        ]

        summary = evaluate.score_predictions(cases, predictions)

        self.assertEqual(1.0, summary["decision_accuracy"])
        self.assertEqual(1.0, summary["citation_accuracy"])
        self.assertEqual([], summary["missing_predictions"])
        self.assertEqual([], summary["unexpected_case_ids"])

    def test_reports_missing_unexpected_and_incorrect_predictions(self):
        cases = [
            {
                "case_id": "eval-01",
                "expected_decision": "answer",
                "expected_refs": ["knowledge-base/article.md"],
            },
            {
                "case_id": "eval-02",
                "expected_decision": "escalate",
                "expected_refs": ["knowledge-base/escalation.md"],
            },
        ]
        predictions = [
            {
                "case_id": "eval-01",
                "decision": "answer",
                "knowledge_refs": ["knowledge-base/article.md"],
            },
            {
                "case_id": "eval-extra",
                "decision": "answer",
                "knowledge_refs": [],
            },
        ]

        summary = evaluate.score_predictions(cases, predictions)

        self.assertEqual(0.5, summary["decision_accuracy"])
        self.assertEqual(0.5, summary["citation_accuracy"])
        self.assertEqual(2, summary["citation_total"])
        self.assertEqual(["eval-02"], summary["missing_predictions"])
        self.assertEqual(["eval-extra"], summary["unexpected_case_ids"])

    def test_scores_present_but_incorrect_decision_and_citation(self):
        cases = [
            {
                "case_id": "eval-01",
                "expected_decision": "answer",
                "expected_refs": ["knowledge-base/article.md"],
            }
        ]
        predictions = [
            {
                "case_id": "eval-01",
                "decision": "escalate",
                "knowledge_refs": ["knowledge-base/wrong.md"],
            }
        ]

        summary = evaluate.score_predictions(cases, predictions)

        self.assertEqual(0.0, summary["decision_accuracy"])
        self.assertEqual(0.0, summary["citation_accuracy"])

    def test_extra_or_unnecessary_citations_fail_exact_reference_scoring(self):
        evaluation = [
            {
                "case_id": "eval-01",
                "expected_decision": "answer",
                "expected_refs": ["KB-1"],
            },
            {
                "case_id": "eval-02",
                "expected_decision": "escalate",
                "expected_refs": [],
            },
        ]
        predictions = [
            {
                "case_id": "eval-01",
                "decision": "answer",
                "knowledge_refs": ["KB-1", "KB-HALLUCINATED"],
            },
            {
                "case_id": "eval-02",
                "decision": "escalate",
                "knowledge_refs": ["KB-UNNECESSARY"],
            },
        ]

        summary = evaluate.score_predictions(evaluation, predictions)

        self.assertEqual(2, summary["citation_total"])
        self.assertEqual(0, summary["citation_correct"])
        self.assertEqual(0.0, summary["citation_accuracy"])
        self.assertEqual([], summary["missing_predictions"])

    def test_rejects_duplicate_evaluation_case_ids(self):
        cases = [
            {"case_id": "eval-01", "expected_decision": "answer", "expected_refs": []},
            {"case_id": "eval-01", "expected_decision": "escalate", "expected_refs": []},
        ]

        with self.assertRaisesRegex(ValueError, "Duplicate evaluation case_id: eval-01"):
            evaluate.score_predictions(cases, [])

    def test_rejects_duplicate_prediction_case_ids(self):
        predictions = [
            {"case_id": "eval-01", "decision": "answer", "knowledge_refs": []},
            {"case_id": "eval-01", "decision": "escalate", "knowledge_refs": []},
        ]

        with self.assertRaisesRegex(ValueError, "Duplicate prediction case_id: eval-01"):
            evaluate.score_predictions([], predictions)

    def test_rejects_unknown_prediction_decision(self):
        predictions = [
            {"case_id": "eval-01", "decision": "invented", "knowledge_refs": []}
        ]

        with self.assertRaisesRegex(ValueError, "decision must be one of"):
            evaluate.score_predictions([], predictions)

    def test_validates_refs_on_unexpected_prediction(self):
        predictions = [
            {"case_id": "eval-extra", "decision": "answer", "knowledge_refs": "kb.md"}
        ]

        with self.assertRaisesRegex(ValueError, "knowledge_refs must be a list"):
            evaluate.score_predictions([], predictions)


class EvaluatorCliTests(unittest.TestCase):
    def test_invalid_prediction_json_reports_clean_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            predictions = Path(temp_dir) / "predictions.json"
            predictions.write_text("{", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(predictions)],
                cwd=MODULE_PATH.parents[1],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(2, result.returncode)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn(str(predictions), result.stderr)
        self.assertIn("invalid predictions JSON", result.stderr)

    def test_require_perfect_accepts_complete_example_fixture(self) -> None:
        fixture = MODULE_PATH.with_name("example-predictions.json")

        result = subprocess.run(
            [sys.executable, str(MODULE_PATH), str(fixture), "--require-perfect"],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_require_perfect_rejects_invalid_decision_as_schema_error(self):
        fixture = MODULE_PATH.with_name("example-predictions.json")
        predictions = json.loads(fixture.read_text(encoding="utf-8"))
        predictions[0]["decision"] = "not-a-valid-decision"
        predictions[0]["knowledge_refs"] = []

        with tempfile.TemporaryDirectory() as temporary:
            drifted = Path(temporary) / "drifted.json"
            drifted.write_text(json.dumps(predictions), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(drifted), "--require-perfect"],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertEqual("", result.stdout)
        self.assertIn("decision must be one of", result.stderr)


if __name__ == "__main__":
    unittest.main()
