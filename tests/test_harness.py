import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).parents[1]
MODULE_PATH = REPO_ROOT / "applied-ai" / "harness.py"


def load_harness():
    if not MODULE_PATH.is_file():
        raise AssertionError("applied-ai/harness.py does not exist")
    spec = importlib.util.spec_from_file_location("support_harness", MODULE_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ContextPacketTests(unittest.TestCase):
    def test_default_limit_retrieves_each_evaluation_cases_expected_refs(self):
        harness = load_harness()
        cases = json.loads(
            (REPO_ROOT / "applied-ai/evaluation-set.json").read_text(encoding="utf-8")
        )

        for case in cases:
            with self.subTest(case_id=case["case_id"]):
                packet = harness.build_context_packet(REPO_ROOT, case["summary"])
                retrieved = {source["ref"] for source in packet["sources"]}
                self.assertTrue(set(case["expected_refs"]) <= retrieved)

    def test_approved_documents_match_policy_scope(self):
        harness = load_harness()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            files = {
                "knowledge-base/kb.md": "kb",
                "operations/triage-decision-guide.md": "triage",
                "operations/escalation-playbook.md": "escalate",
                "operations/not-policy-approved.md": "exclude",
                "cases/case.md": "case",
                "qa/bugs/bug.md": "bug",
            }
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            refs = {item["ref"] for item in harness.approved_documents(root)}

        self.assertEqual(
            set(files) - {"operations/not-policy-approved.md"},
            refs,
        )

    def test_retrieval_normalizes_for_document_length(self):
        harness = load_harness()
        documents = [
            {
                "ref": "knowledge-base/a-long.md",
                "text": "mfa loop " + " ".join(f"noise{index}" for index in range(20)),
            },
            {"ref": "knowledge-base/z-concise.md", "text": "mfa loop"},
        ]

        ranked = harness.retrieve_sources("mfa loop", documents, limit=2)

        self.assertEqual("knowledge-base/z-concise.md", ranked[0]["ref"])

    def test_invokes_local_model_command_and_validates_response(self):
        harness = load_harness()
        packet = harness.build_context_packet(
            REPO_ROOT,
            "One user enters valid credentials but keeps returning to the MFA prompt.",
        )
        cited_ref = packet["sources"][0]["ref"]
        response = {
            "decision": "answer",
            "reason": "The retrieved runbook covers the reported symptom.",
            "next_step": "Follow the documented reset sequence.",
            "knowledge_refs": [cited_ref],
        }
        command = [
            sys.executable,
            "-c",
            "import json,sys; sys.stdin.read(); print(json.dumps(json.loads(sys.argv[1])))",
            json.dumps(response),
        ]

        validated = harness.invoke_model(command, packet, timeout_seconds=5)

        self.assertEqual(response, validated)

    def test_missing_policy_fails_closed_without_private_path(self):
        harness = load_harness()

        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(RuntimeError, "assistant policy is missing") as ctx:
                harness.build_context_packet(Path(temp_dir), "MFA loop")

        self.assertNotIn(temp_dir, str(ctx.exception))

    def test_builds_grounded_packet_from_approved_repository_sources(self):
        harness = load_harness()

        packet = harness.build_context_packet(
            REPO_ROOT,
            "One user enters valid credentials but keeps returning to the MFA prompt.",
            limit=2,
        )

        refs = [source["ref"] for source in packet["sources"]]
        self.assertEqual("knowledge-base/kb-003-mfa-loop.md", refs[0])
        self.assertTrue(
            all(
                ref.startswith(("knowledge-base/", "operations/", "cases/", "qa/bugs/"))
                for ref in refs
            )
        )
        self.assertIn("knowledge-base/kb-003-mfa-loop.md", packet["prompt"])
        self.assertIn(packet["request"], packet["prompt"])
        self.assertNotIn(str(REPO_ROOT), packet["prompt"])

    def test_rejects_response_citation_outside_retrieved_context(self):
        harness = load_harness()
        packet = harness.build_context_packet(
            REPO_ROOT,
            "One user enters valid credentials but keeps returning to the MFA prompt.",
            limit=1,
        )
        response = {
            "decision": "answer",
            "reason": "Use the documented first-line path.",
            "next_step": "Reset the session and verify recovery.",
            "knowledge_refs": ["knowledge-base/not-retrieved.md"],
        }

        self.assertTrue(hasattr(harness, "validate_response"))
        with self.assertRaisesRegex(ValueError, "outside retrieved context"):
            harness.validate_response(response, packet)

    def test_rejects_answer_without_grounding_reference(self):
        harness = load_harness()
        packet = harness.build_context_packet(
            REPO_ROOT,
            "zzzxqv no matching repository language",
            limit=1,
        )
        response = {
            "decision": "answer",
            "reason": "A confident but unsupported answer.",
            "next_step": "Tell the user to proceed.",
            "knowledge_refs": [],
        }

        with self.assertRaisesRegex(ValueError, "answer requires"):
            harness.validate_response(response, packet)

    def test_rejects_answer_without_retrieved_knowledge_base_reference(self):
        harness = load_harness()
        packet = {
            "sources": [
                {
                    "ref": "operations/triage-decision-guide.md",
                    "text": "Operational routing only",
                }
            ]
        }
        response = {
            "decision": "answer",
            "reason": "The operational guide appears relevant.",
            "next_step": "Proceed from the guide.",
            "knowledge_refs": ["operations/triage-decision-guide.md"],
        }

        with self.assertRaisesRegex(ValueError, "knowledge-base reference"):
            harness.validate_response(response, packet)

    def test_model_nonzero_exit_fails_closed(self):
        harness = load_harness()
        packet = {"prompt": "bounded prompt", "sources": []}
        completed = subprocess.CompletedProcess(["model"], 3, "", "failure")

        with mock.patch.object(harness.subprocess, "run", return_value=completed):
            with self.assertRaisesRegex(RuntimeError, "failed with exit code 3"):
                harness.invoke_model(["model"], packet)

    def test_model_timeout_fails_closed(self):
        harness = load_harness()
        packet = {"prompt": "bounded prompt", "sources": []}

        with mock.patch.object(
            harness.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired(["model"], 1),
        ):
            with self.assertRaisesRegex(RuntimeError, "could not complete"):
                harness.invoke_model(["model"], packet, timeout_seconds=1)

    def test_recorded_local_model_run_validates_against_retrieved_context(self):
        harness = load_harness()
        evidence_path = REPO_ROOT / "applied-ai" / "model-run-evidence.json"
        self.assertTrue(evidence_path.is_file())
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        packet = harness.build_context_packet(
            REPO_ROOT,
            evidence["request"],
            limit=evidence["retrieval_limit"],
        )

        self.assertEqual(
            evidence["response"],
            harness.validate_response(evidence["response"], packet),
        )
        self.assertEqual("passed", evidence["validation"])

    def test_rejects_non_text_decision_without_type_error(self):
        harness = load_harness()
        packet = {"sources": []}
        response = {
            "decision": [],
            "reason": "Malformed schema",
            "next_step": "Reject it",
            "knowledge_refs": [],
        }

        with self.assertRaisesRegex(ValueError, "decision must be allowed text"):
            harness.validate_response(response, packet)

    def test_accepts_answer_citing_retrieved_source(self):
        harness = load_harness()
        packet = harness.build_context_packet(
            REPO_ROOT,
            "One user enters valid credentials but keeps returning to the MFA prompt.",
            limit=1,
        )
        response = {
            "decision": "answer",
            "reason": "The request matches the documented MFA loop path.",
            "next_step": "Follow the first-line checks and verify recovery.",
            "knowledge_refs": [packet["sources"][0]["ref"]],
        }

        self.assertEqual(response, harness.validate_response(response, packet))


class HarnessCliTests(unittest.TestCase):
    def test_cli_reports_invalid_model_output_without_traceback_or_private_path(self):
        result = subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                "MFA loop",
                "--model-command",
                sys.executable,
                "-c",
                "print('not-json')",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(2, result.returncode)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn(str(MODULE_PATH), result.stderr)
        self.assertIn("Model command returned invalid JSON", result.stderr)

    def test_cli_invokes_and_validates_model_command(self):
        response = {
            "decision": "answer",
            "reason": "The retrieved MFA runbook covers this symptom.",
            "next_step": "Follow the documented reset sequence.",
            "knowledge_refs": ["knowledge-base/kb-003-mfa-loop.md"],
        }
        result = subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                "One user enters valid credentials but keeps returning to the MFA prompt.",
                "--model-command",
                sys.executable,
                "-c",
                "import json,sys; sys.stdin.read(); print(json.dumps(json.loads(sys.argv[1])))",
                json.dumps(response),
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(response, json.loads(result.stdout)["response"])

    def test_cli_emits_inspectable_context_packet(self):
        result = subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                "One user enters valid credentials but keeps returning to the MFA prompt.",
                "--limit",
                "2",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertTrue(result.stdout.strip(), "CLI emitted no context packet")
        packet = json.loads(result.stdout)
        self.assertEqual(
            "knowledge-base/kb-003-mfa-loop.md",
            packet["sources"][0]["ref"],
        )
        self.assertNotIn(str(REPO_ROOT), result.stdout)


if __name__ == "__main__":
    unittest.main()
