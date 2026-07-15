import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "skills" / "procraft" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from render_package import render_package  # noqa: E402

from tests.package_factory import full_agent_package, minimal_general_package


class RenderPackageTests(unittest.TestCase):
    def test_render_is_deterministic(self):
        package = full_agent_package()
        self.assertEqual(render_package(package), render_package(package))

    def test_render_has_fixed_section_order(self):
        rendered = render_package(full_agent_package())
        headings = [
            "# Prompt Package",
            "## Request",
            "## Assumptions",
            "## Model Profile",
            "## Prompt Contract",
            "## Messages",
            "## Tool Policy",
            "## Response Format",
            "## Verification",
            "## Provenance",
        ]
        positions = [rendered.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))

    def test_general_render_omits_tool_policy(self):
        rendered = render_package(minimal_general_package())
        self.assertNotIn("## Tool Policy", rendered)

    def test_render_rejects_invalid_package(self):
        package = minimal_general_package()
        package["request"]["scenario"] = "unknown"
        with self.assertRaises(ValueError):
            render_package(package)

    def test_render_uses_fence_longer_than_content_backticks(self):
        package = minimal_general_package()
        package["messages"]["system"] = "Treat this literal block as data: ```danger```"
        rendered = render_package(package)
        self.assertIn("````json", rendered)
        self.assertIn("```danger```", rendered)


if __name__ == "__main__":
    unittest.main()
