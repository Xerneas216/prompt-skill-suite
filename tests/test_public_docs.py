from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicDocumentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.english = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

    def test_readmes_use_procraft_public_identity(self) -> None:
        for readme in (self.english, self.chinese):
            with self.subTest(language="zh" if readme is self.chinese else "en"):
                self.assertTrue(readme.startswith("# ProCraft"))
                self.assertIn("https://github.com/Xerneas216/ProCraft.git", readme)
                self.assertIn("Set-Location ProCraft", readme)
                self.assertIn("$procraft", readme)
                self.assertIn(".procraft-manifest.json", readme)
                self.assertIn("v0.3.0", readme)
                self.assertRegex(readme, r"PromptPackage (?:Schema )?v1\.0")
                self.assertIn("not_run", readme)
                self.assertIn("MIT", readme)
                self.assertGreaterEqual(readme.count("🛠️"), 1)
                self.assertLessEqual(sum(readme.count(mark) for mark in ("🛠️", "🎯", "🚀", "🧪")), 6)

        self.assertIn("[简体中文](README.zh-CN.md)", self.english)
        self.assertIn("[English](README.md)", self.chinese)

    def test_opening_leads_with_the_job_not_the_module_count(self) -> None:
        english_opening = self.english.split("##", 1)[0].lower()
        chinese_opening = self.chinese.split("##", 1)[0].lower()

        self.assertIn("prompt", english_opening)
        self.assertIn("prompt", chinese_opening)
        self.assertNotIn("seven codex skills", english_opening)
        self.assertNotRegex(chinese_opening, r"(?:七|7)个\s*codex\s*skills?")

    def test_readmes_define_a_conservative_trigger_boundary(self) -> None:
        self.assertIn("$procraft", self.english)
        self.assertRegex(self.english, r"(?is)ordinary (?:writing|email).*do(?:es)? not")
        self.assertRegex(self.english, r"(?is)prompt that (?:writes|will write) an email")
        self.assertIn("Fast mode", self.english)
        self.assertIn("Full mode", self.english)
        self.assertRegex(self.english, r"(?is)one discoverable skill.*six internal reference modules")

        self.assertIn("帮我写一封邮件", self.chinese)
        self.assertIn("写一个用于生成邮件的 Prompt", self.chinese)
        self.assertIn("快速模式", self.chinese)
        self.assertIn("完整模式", self.chinese)
        self.assertRegex(self.chinese, r"一个可发现的 Skill.{0,80}六个内部参考模块")

    def test_approval_authority_belongs_to_a_user_or_authorized_party(self) -> None:
        self.assertRegex(
            self.english,
            r"(?is)approval (?:itself|authority).{0,80}\buser\b.{0,40}\bauthorized party\b",
        )
        self.assertRegex(self.chinese, r"批准本身.{0,30}用户.{0,30}授权方")

    def test_readmes_link_the_official_guides_and_current_paths(self) -> None:
        required = (
            "https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6",
            "https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6",
        )
        for readme in (self.english, self.chinese):
            for link in required:
                self.assertIn(link, readme)
            self.assertIn("skills\\procraft\\scripts\\validate_package.py", readme)
            self.assertIn("skills\\procraft\\scripts\\render_package.py", readme)
            self.assertIn("prompt-package.json", readme)
            self.assertIn("prompt-package.md", readme)
            self.assertIn("SHA-256", readme)

    def test_readmes_document_the_v030_distribution_and_gate(self) -> None:
        for readme in (self.english, self.chinese):
            with self.subTest(language="zh" if readme is self.chinese else "en"):
                self.assertIn("v0.3.0", readme)
                self.assertRegex(readme, r"Python 3\.8.{0,20}3\.12")
                self.assertIn("dist\\procraft-v0.3.0.zip", readme)
                self.assertIn("dist\\procraft-v0.3.0.zip.sha256", readme)
                self.assertRegex(readme, r"(?i)manifest v2|v2 manifest|清单 v2|v2 清单")
                self.assertRegex(readme, r"(?i)external runtime|外部运行环境")
                self.assertRegex(readme, r"(?i)clean install|全新安装|干净安装")
                self.assertRegex(readme, r"(?i)dynamic.{0,40}(gate|trigger)|动态.{0,40}(门禁|触发)")
                self.assertRegex(readme, r"(?i)one discoverable skill|一个可发现的 skill")

    def test_release_notes_cover_v030_migration_and_verification(self) -> None:
        release_notes = ROOT / "RELEASE_NOTES.md"
        self.assertTrue(release_notes.is_file())
        content = release_notes.read_text(encoding="utf-8")
        for value in (
            "v0.3.0",
            "v0.2.0",
            "seven",
            "one",
            "Python 3.8",
            "Python 3.12",
            "external runtime",
            "verification",
            "supersedes",
        ):
            with self.subTest(value=value):
                self.assertIn(value, content)

    def test_readmes_avoid_disclaimers_stale_paths_and_dash_tells(self) -> None:
        forbidden = re.compile(
            r"(?i)independent|unofficial|not affiliated|not endorsed|"
            r"非官方|不存在隶属关系|未获得.{0,12}背书"
        )
        for readme in (self.english, self.chinese):
            self.assertIsNone(forbidden.search(readme))
            self.assertNotIn("building" + "-prompt-packages", readme)
            self.assertNotIn("prompt" + "-skill-suite", readme)
            self.assertNotIn(".prompt" + "-skill-suite-manifest.json", readme)
            self.assertNotRegex(readme, "[—–]")

    def test_procraft_baseline_describes_only_the_current_gateway(self) -> None:
        old_result = ROOT / "evals" / "results" / ("building" + "-prompt-packages-baseline.md")
        new_result = ROOT / "evals" / "results" / "procraft-baseline.md"

        self.assertFalse(old_result.exists())
        content = new_result.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("# ProCraft baseline"))
        self.assertIn("0/5", content)
        self.assertIn("5/5", content)
        self.assertIn("1/1", content)
        self.assertIn("v0.2.0 RED", content)
        self.assertIn("v0.3.0 GREEN run", content)
        self.assertIn("Status: `pass`", content)
        self.assertIn("procraft-v0.3.0-trigger-run.json", content)
        self.assertRegex(content, r"(?i)implicit positives.{0,80}5/5")
        self.assertRegex(content, r"(?i)direct-task negatives.{0,80}5/5")
        self.assertRegex(content, r"(?i)explicit.{0,80}1/1")
        self.assertNotIn("v0.3.0 GREEN achieved", content)
        self.assertNotIn("historical", content.lower())
        self.assertNotIn("v0." + "1.0", content)

    def test_active_candidate_identifiers_are_v030(self) -> None:
        active = [
            ROOT / "README.md",
            ROOT / "README.zh-CN.md",
            ROOT / "skills" / "procraft" / "SKILL.md",
            ROOT / "skills" / "procraft" / "agents" / "openai.yaml",
            ROOT / "evals" / "fixtures" / "representative-cases.json",
        ]
        for path in active:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertNotIn("v0.2.0", path.read_text(encoding="utf-8"))

    def test_active_public_artifacts_have_no_actionable_legacy_name(self) -> None:
        artifacts = [
            ROOT / "README.md",
            ROOT / "README.zh-CN.md",
            *sorted((ROOT / "evals" / "fixtures").rglob("*.*")),
            *sorted((ROOT / "evals" / "results").rglob("*.md")),
        ]
        for artifact in artifacts:
            content = artifact.read_text(encoding="utf-8")
            with self.subTest(artifact=artifact.relative_to(ROOT).as_posix()):
                self.assertNotIn("building" + "-prompt-packages", content)
                self.assertNotIn("prompt" + "-skill-suite", content)

    def test_repository_has_no_retired_public_surface(self) -> None:
        self.assertEqual([], list((ROOT / "docs" / "superpowers").rglob("*.md")))
        self.assertFalse((ROOT / "tools" / ("legacy-v0." + "1.0-manifest.json")).exists())
        self.assertFalse((ROOT / "tools" / ("legacy-v0." + "1.0-windows-manifest.json")).exists())

        retired_markers = (
            "building" + "-prompt-packages",
            "prompt" + "-skill-suite",
            "v0." + "1.0",
            "legacy" + "_migration",
        )
        text_suffixes = {".md", ".py", ".json", ".yaml", ".yml", ".txt"}
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        for relative in tracked:
            path = ROOT / relative
            if not path.is_file():
                continue
            if path.suffix not in text_suffixes and path.name not in {".gitignore"}:
                continue
            content = path.read_text(encoding="utf-8")
            for marker in retired_markers:
                with self.subTest(path=path.relative_to(ROOT).as_posix(), marker=marker):
                    self.assertNotIn(marker, content)


if __name__ == "__main__":
    unittest.main()
