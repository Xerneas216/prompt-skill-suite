import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "skills" / "procraft" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from validate_package import validate_package  # noqa: E402

from tests.package_factory import full_agent_package, minimal_general_package


class ValidatePackageTests(unittest.TestCase):
    def assert_invalid(self, package, fragment):
        errors = validate_package(package)
        self.assertTrue(errors)
        self.assertIn(fragment, "\n".join(errors))

    def test_valid_minimal_general_package(self):
        self.assertEqual([], validate_package(minimal_general_package()))

    def test_valid_full_agent_package(self):
        self.assertEqual([], validate_package(full_agent_package()))

    def test_canonical_procraft_provenance_does_not_require_the_legacy_alias(self):
        package = minimal_general_package()
        modules = package["provenance"]["participating_modules"]
        self.assertIn("procraft", modules)
        self.assertNotIn("building-prompt-packages", modules)
        self.assertEqual([], validate_package(package))

    def test_legacy_entry_provenance_remains_compatible_without_procraft(self):
        package = minimal_general_package()
        modules = package["provenance"]["participating_modules"]
        modules[modules.index("procraft")] = "building-prompt-packages"
        self.assertIn("building-prompt-packages", modules)
        self.assertNotIn("procraft", modules)
        self.assertEqual([], validate_package(package))

    def test_tool_contract_requires_executable_schema(self):
        package = full_agent_package()
        del package["tool_policy"]["tools"][0]["input_schema"]
        self.assert_invalid(package, "input_schema")

    def test_tool_contract_rejects_invalid_json_schema(self):
        package = full_agent_package()
        package["tool_policy"]["tools"][0]["input_schema"] = {"type": "not-a-json-type"}
        self.assert_invalid(package, "input_schema")

    def test_write_tool_requires_recovery_capabilities(self):
        package = full_agent_package()
        del package["tool_policy"]["tools"][2]["status_recovery"]
        self.assert_invalid(package, "status_recovery")

    def test_missing_required_field(self):
        package = minimal_general_package()
        del package["messages"]
        self.assert_invalid(package, "messages")

    def test_illegal_enum(self):
        package = minimal_general_package()
        package["model_profile"]["reasoning_effort"] = "turbo"
        self.assert_invalid(package, "reasoning_effort")

    def test_tools_require_tool_policy(self):
        package = full_agent_package()
        del package["tool_policy"]
        self.assert_invalid(package, "tool_policy")

    def test_non_tool_package_rejects_tool_policy(self):
        package = minimal_general_package()
        package["tool_policy"] = full_agent_package()["tool_policy"]
        self.assert_invalid(package, "tool_policy")

    def test_dangling_tool_reference(self):
        package = full_agent_package()
        package["tool_policy"]["routing"][0]["tool"] = "crm_lookup"
        self.assert_invalid(package, "crm_lookup")

    def test_dangling_dependency_reference(self):
        package = full_agent_package()
        package["tool_policy"]["routing"][1]["depends_on"] = ["missing_step"]
        self.assert_invalid(package, "missing_step")

    def test_two_step_dependency_cycle(self):
        package = full_agent_package()
        package["tool_policy"]["routing"][0]["depends_on"] = ["sanctions"]
        self.assert_invalid(package, "dependency cycle")

    def test_multi_step_dependency_cycle(self):
        package = full_agent_package()
        package["tool_policy"]["routing"][0]["depends_on"] = ["email"]
        self.assert_invalid(package, "dependency cycle")

    def test_dangling_ptc_tool_reference(self):
        package = full_agent_package()
        package["tool_policy"]["ptc"]["eligible_tools"] = ["missing_tool"]
        self.assert_invalid(package, "missing_tool")

    def test_empty_optional_configuration_is_rejected(self):
        package = full_agent_package()
        package["tool_policy"]["long_task"] = {}
        self.assert_invalid(package, "long_task")

    def test_normalized_duplicate_string_in_rule_list(self):
        package = minimal_general_package()
        package["prompt_contract"]["constraints"] = ["Do not add facts", "  do not add facts  "]
        self.assert_invalid(package, "duplicate")

    def test_message_layers_must_not_be_identical(self):
        package = minimal_general_package()
        package["messages"]["developer"] = package["messages"]["system"]
        self.assert_invalid(package, "messages.system")

    def test_single_turn_rejects_all_turns_reasoning(self):
        package = minimal_general_package()
        package["model_profile"]["reasoning_context"] = "all_turns"
        self.assert_invalid(package, "reasoning_context")

    def test_request_may_have_no_explicit_values(self):
        package = minimal_general_package()
        package["request"]["explicit_values"] = {}
        self.assertEqual([], validate_package(package))

    def test_explicit_language_cannot_be_overridden(self):
        package = minimal_general_package()
        package["request"]["language"] = "en"
        self.assert_invalid(package, "/request/language")

    def test_explicit_length_cannot_be_overridden(self):
        package = minimal_general_package()
        package["prompt_contract"]["output"]["length_limit"] = "500 characters"
        self.assert_invalid(package, "/prompt_contract/output/length_limit")

    def test_explicit_delivery_cannot_be_overridden(self):
        package = minimal_general_package()
        package["request"]["delivery"] = "files"
        self.assert_invalid(package, "/request/delivery")

    def test_explicit_value_pointer_must_resolve(self):
        package = minimal_general_package()
        package["request"]["explicit_values"]["/prompt_contract/output/missing"] = "value"
        self.assert_invalid(package, "/prompt_contract/output/missing")

    def test_multi_turn_accepts_all_turns_reasoning(self):
        package = full_agent_package()
        package["model_profile"]["reasoning_context"] = "all_turns"
        self.assertEqual([], validate_package(package))

    def test_dynamic_pass_requires_evidence(self):
        package = minimal_general_package()
        package["verification"]["dynamic_evaluation"]["status"] = "pass"
        self.assert_invalid(package, "dynamic_evaluation")

    def test_static_pass_rejects_findings(self):
        package = minimal_general_package()
        package["verification"]["static_review"]["findings"] = ["Known defect"]
        self.assert_invalid(package, "static_review")

    def test_structured_response_rejects_invalid_json_schema(self):
        package = minimal_general_package()
        package["response_format"] = {
            "type": "json_schema",
            "name": "summary",
            "schema": {"type": "not-a-json-type"},
            "strict": True,
        }
        self.assert_invalid(package, "response_format.schema")

    def test_json_fixture_round_trip(self):
        package = json.loads(json.dumps(full_agent_package()))
        self.assertEqual([], validate_package(package))


if __name__ == "__main__":
    unittest.main()
