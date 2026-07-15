import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "evals" / "fixtures" / "representative-cases.json"


class EvaluationFixtureTests(unittest.TestCase):
    def test_fixture_is_provider_neutral_and_executable(self):
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual("not_run", data["status"])
        self.assertEqual("no-skill", data["baseline_id"])
        self.assertEqual("procraft-v0.2.0", data["candidate_id"])
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


if __name__ == "__main__":
    unittest.main()
