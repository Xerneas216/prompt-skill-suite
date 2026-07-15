from __future__ import annotations

import re
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
                self.assertIn("v0.2.0", readme)
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
        self.assertRegex(self.english, r"(?is)one public gateway.*six internal specialists")

        self.assertIn("帮我写一封邮件", self.chinese)
        self.assertIn("写一个用于生成邮件的 Prompt", self.chinese)
        self.assertIn("快速模式", self.chinese)
        self.assertIn("完整模式", self.chinese)
        self.assertRegex(self.chinese, r"一个公开入口.{0,80}六个内部模块")

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
            self.assertIn("v0.1.0", readme)
            self.assertIn("SHA-256", readme)
            self.assertIn("legacy_migration", readme)

    def test_readmes_avoid_disclaimers_stale_paths_and_dash_tells(self) -> None:
        forbidden = re.compile(
            r"(?i)independent|unofficial|not affiliated|not endorsed|"
            r"非官方|不存在隶属关系|未获得.{0,12}背书"
        )
        for readme in (self.english, self.chinese):
            self.assertIsNone(forbidden.search(readme))
            self.assertNotIn("building-prompt-packages", readme)
            self.assertNotIn("prompt-skill-suite", readme)
            self.assertNotIn(".prompt-skill-suite-manifest.json", readme)
            self.assertNotRegex(readme, "[—–]")

    def test_procraft_baseline_replaces_the_old_result_name(self) -> None:
        old_result = ROOT / "evals" / "results" / "building-prompt-packages-baseline.md"
        new_result = ROOT / "evals" / "results" / "procraft-baseline.md"

        self.assertFalse(old_result.exists())
        content = new_result.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("# ProCraft baseline"))
        self.assertIn("historical", content.lower())
        self.assertIn("not_run", content)
        self.assertNotIn("building-prompt-packages", content)

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
                self.assertNotIn("building-prompt-packages", content)
                self.assertNotIn("prompt-skill-suite", content)

    def test_stale_design_records_open_with_a_do_not_execute_notice(self) -> None:
        records = sorted((ROOT / "docs" / "superpowers").rglob("*.md"))
        self.assertTrue(records)
        for record in records:
            content = record.read_text(encoding="utf-8")
            if "prompt-skill-suite" not in content and "building-prompt-packages" not in content:
                continue
            notice = content[:600].lower()
            with self.subTest(record=record.name):
                self.assertIn("historical record", notice)
                self.assertIn("do not execute", notice)
                self.assertIn("readme", notice)


if __name__ == "__main__":
    unittest.main()
