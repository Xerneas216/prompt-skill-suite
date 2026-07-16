import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

INTERNAL_MODULES = (
    "defining-prompt-contracts",
    "prompting-general-tasks",
    "prompting-tool-agents",
    "prompting-software-engineering",
    "reviewing-prompt-packages",
    "evaluating-prompt-packages",
)


def _frontmatter(skill_file: Path) -> dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", text, re.DOTALL)
    if not match:
        raise AssertionError(f"Missing YAML frontmatter: {skill_file}")
    fields = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip().strip('"')
    return fields


def _yaml_value(path: Path, key: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"^\s*{re.escape(key)}:\s*[\"']?(.*?)[\"']?\s*$", text, re.MULTILINE)
    if not match:
        raise AssertionError(f"Missing {key} in {path}")
    return match.group(1).rstrip("\"'")


def _section(text: str, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        text,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise AssertionError(f"Missing section: {heading}")
    return match.group(1).casefold()


class ProCraftSkillContractTests(unittest.TestCase):
    def _procraft_text(self) -> str:
        path = SKILLS / "procraft" / "SKILL.md"
        if not path.is_file():
            self.fail("skills/procraft/SKILL.md must exist as the canonical entry")
        return path.read_text(encoding="utf-8")

    def test_procraft_is_the_public_entry_directory(self):
        self.assertTrue((SKILLS / "procraft" / "SKILL.md").is_file())

    def test_distribution_exposes_exactly_one_skill_directory(self):
        skill_files = sorted(path.relative_to(SKILLS).as_posix() for path in SKILLS.glob("*/SKILL.md"))
        self.assertEqual(["procraft/SKILL.md"], skill_files)
        for module in INTERNAL_MODULES:
            with self.subTest(module=module):
                self.assertFalse((SKILLS / module).exists())

    def test_internal_stage_instructions_and_references_are_merged(self):
        for module in INTERNAL_MODULES:
            with self.subTest(module=module):
                merged = SKILLS / "procraft" / "references" / f"{module}.md"
                self.assertTrue(merged.is_file(), merged)
                content = merged.read_text(encoding="utf-8")
                self.assertIn("## Stage instructions", content)
                self.assertIn("## Detailed reference", content)

    def test_procraft_frontmatter_covers_positive_and_negative_trigger_boundaries(self):
        metadata = _frontmatter(SKILLS / "procraft" / "SKILL.md")
        self.assertEqual("procraft", metadata.get("name"))
        description = metadata.get("description", "").casefold()
        for phrase in ("prompt", "提示词", "llm", "agent", "image", "video", "audio"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, description)
        for ordinary_task in (
            "writing",
            "research",
            "coding",
            "summarization",
            "email",
            "image generation",
        ):
            with self.subTest(ordinary_task=ordinary_task):
                self.assertIn(ordinary_task, description)
        self.assertRegex(description, r"(?:do not use|only (?:use|when))")

    def test_procraft_ui_uses_the_canonical_name_and_explicit_invocation(self):
        path = SKILLS / "procraft" / "agents" / "openai.yaml"
        if not path.is_file():
            self.fail("skills/procraft/agents/openai.yaml must exist")
        self.assertEqual("ProCraft", _yaml_value(path, "display_name"))
        self.assertIn("$procraft", _yaml_value(path, "default_prompt"))

    def test_full_mode_reads_merged_references_directly(self):
        full = _section(self._procraft_text(), "Full mode")
        for module in INTERNAL_MODULES:
            with self.subTest(module=module):
                self.assertIn(f"](references/{module}.md)", full)

    def test_promptpackage_v1_keeps_logical_participating_module_names(self):
        schema_path = SKILLS / "procraft" / "references" / "prompt-package.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        modules = schema["$defs"]["provenance"]["properties"]["participating_modules"]["items"][
            "enum"
        ]
        self.assertEqual(["procraft", *INTERNAL_MODULES], modules)

    def test_mode_priority_is_explicit_then_full_then_fast(self):
        selection = _section(self._procraft_text(), "Mode selection")
        positions = [selection.find(token) for token in ("explicit", "full mode", "fast mode")]
        self.assertTrue(all(position >= 0 for position in positions), positions)
        self.assertEqual(positions, sorted(positions))

    def test_fast_mode_has_a_minimal_output_contract_and_is_the_ambiguous_default(self):
        text = self._procraft_text()
        fast = _section(text, "Fast mode")
        for term in ("directly usable prompt", "variables", "assumptions"):
            self.assertIn(term, fast)
        selection = _section(text, "Mode selection")
        self.assertRegex(selection, r"(?:ambiguous|unclear).{0,120}fast mode")
        self.assertRegex(selection, r"(?:offer|suggest).{0,120}(?:upgrade|full mode)")

    def test_full_mode_lists_every_escalation_condition(self):
        full = _section(self._procraft_text(), "Full mode")
        for term in (
            "promptpackage",
            "production",
            "system",
            "developer",
            "user",
            "structured outputs",
            "tool",
            "approval",
            "long-running",
            "repository",
            "review",
            "evaluation",
            "migration",
        ):
            with self.subTest(term=term):
                self.assertIn(term, full)

    def test_full_mode_defines_the_canonical_package_pipeline_and_dual_delivery(self):
        full = _section(self._procraft_text(), "Full mode")
        for term in (
            "canonical promptpackage",
            "contract",
            "specialist",
            "routing",
            "static review",
            "validate",
            "render",
            "evaluation",
            "not_run",
            "json",
            "markdown",
        ):
            with self.subTest(term=term):
                self.assertIn(term, full)


if __name__ == "__main__":
    unittest.main()
