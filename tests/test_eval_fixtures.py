import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "evals" / "fixtures" / "representative-cases.json"
TRIGGER_FIXTURE = ROOT / "evals" / "fixtures" / "trigger-cases.json"


class EvaluationFixtureTests(unittest.TestCase):
    def test_fixture_is_provider_neutral_and_executable(self):
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual("not_run", data["status"])
        self.assertEqual("no-skill", data["baseline_id"])
        self.assertEqual("procraft-v0.3.0", data["candidate_id"])
        self.assertGreaterEqual(len(data["cases"]), 8)
        case_ids = [case["case_id"] for case in data["cases"]]
        self.assertEqual(len(case_ids), len(set(case_ids)))
        required = {
            "case_id",
            "scenario",
            "input",
            "trusted_context",
            "untrusted_content",
            "tool_fixtures",
            "permission_state",
            "expected_observables",
            "forbidden_observables",
            "grader",
            "tags",
        }
        for case in data["cases"]:
            self.assertEqual(required, set(case))

    def test_trigger_fixture_has_the_release_gate_boundary(self):
        self.assertTrue(TRIGGER_FIXTURE.is_file())
        data = json.loads(TRIGGER_FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual("not_run", data["status"])
        self.assertEqual("procraft-v0.3.0", data["candidate_id"])
        self.assertEqual(11, len(data["cases"]))
        self.assertEqual(
            Counter({"implicit_positive": 5, "direct_task_negative": 5, "explicit": 1}),
            Counter(case["kind"] for case in data["cases"]),
        )
        self.assertEqual(
            {
                "chinese_prompt_creation",
                "english_prompt_creation",
                "image_media_prompt",
                "agent_system_instruction",
                "prompt_improvement",
            },
            {case["coverage"] for case in data["cases"] if case["kind"] == "implicit_positive"},
        )
        self.assertEqual(
            {
                "direct_email",
                "direct_summarization",
                "direct_research",
                "direct_code_fix",
                "direct_image_generation",
            },
            {case["coverage"] for case in data["cases"] if case["kind"] == "direct_task_negative"},
        )
        for case in data["cases"]:
            with self.subTest(case_id=case["case_id"]):
                self.assertEqual(case["kind"] != "direct_task_negative", case["expected_trigger"])
                self.assertEqual({"case_id", "kind", "coverage", "prompt", "expected_trigger"}, set(case))
        explicit = next(case for case in data["cases"] if case["kind"] == "explicit")
        self.assertIn("$procraft", explicit["prompt"])


if __name__ == "__main__":
    unittest.main()
