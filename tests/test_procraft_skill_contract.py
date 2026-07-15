import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

INTERNAL_SKILLS = {
    "defining-prompt-contracts": ("ProCraft · Contract", ("contract",)),
    "prompting-general-tasks": ("ProCraft · General", ("ready contract", "general")),
    "prompting-tool-agents": ("ProCraft · Agent", ("ready contract", "tool")),
    "prompting-software-engineering": (
        "ProCraft · Software",
        ("ready contract", "software"),
    ),
    "reviewing-prompt-packages": ("ProCraft · Review", ("candidate", "review")),
    "evaluating-prompt-packages": (
        "ProCraft · Evaluate",
        ("passing static review", "evaluation"),
    ),
}


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
    return match.group(1).rstrip('"\'')


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

    def test_procraft_frontmatter_covers_positive_and_negative_trigger_boundaries(self):
        path = SKILLS / "procraft" / "SKILL.md"
        if not path.is_file():
            self.fail("skills/procraft/SKILL.md must exist as the canonical entry")
        metadata = _frontmatter(path)
        self.assertEqual("procraft", metadata.get("name"))
        description = metadata.get("description", "").casefold()
        for phrase in (
            "prompt",
            "提示词",
            "系统指令",
            "system",
            "developer",
            "user",
            "agent",
            "tool",
            "structured output",
            "reusable",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, description)
        for ordinary_task in ("writing", "research", "programming"):
            with self.subTest(ordinary_task=ordinary_task):
                self.assertIn(ordinary_task, description)
        self.assertRegex(description, r"(?:do not use|only (?:use|when))")

    def test_procraft_ui_uses_the_canonical_name_and_explicit_invocation(self):
        path = SKILLS / "procraft" / "agents" / "openai.yaml"
        if not path.is_file():
            self.fail("skills/procraft/agents/openai.yaml must exist")
        self.assertEqual("ProCraft", _yaml_value(path, "display_name"))
        default_prompt = _yaml_value(path, "default_prompt")
        self.assertIn("$procraft", default_prompt)

    def test_internal_skills_are_stage_gated_inside_the_procraft_workflow(self):
        for skill_name, (display_name, stage_terms) in INTERNAL_SKILLS.items():
            with self.subTest(skill=skill_name):
                skill_file = SKILLS / skill_name / "SKILL.md"
                metadata = _frontmatter(skill_file)
                description = metadata.get("description", "").casefold()
                self.assertIn("procraft workflow", description)
                self.assertIn("only", description)
                for term in stage_terms:
                    self.assertIn(term, description)

                yaml_file = SKILLS / skill_name / "agents" / "openai.yaml"
                self.assertEqual(display_name, _yaml_value(yaml_file, "display_name"))
                default_prompt = _yaml_value(yaml_file, "default_prompt").casefold()
                self.assertIn("procraft workflow", default_prompt)
                self.assertIn(f"${skill_name}", default_prompt)

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
