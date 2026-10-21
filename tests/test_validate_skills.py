#!/usr/bin/env python3
"""Tests for tools/validate_skills.py and related fixtures."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools" / "validate_skills.py"


def load_validator():
    """加载 validate_skills 模块。

    Returns:
        模块对象。

    Raises:
        FileNotFoundError: 工具不存在。
    """
    spec = importlib.util.spec_from_file_location("validate_skills", TOOLS)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(TOOLS)
    module = importlib.util.module_from_spec(spec)
    sys.modules["validate_skills"] = module
    spec.loader.exec_module(module)
    return module


class TestFrontmatterParsing(unittest.TestCase):
    """Frontmatter 有限解析测试。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.v = load_validator()

    def test_parse_folded_description(self) -> None:
        text = "---\nname: demo-skill\ndescription: >-\n  line one\n  line two\n---\n\nBody\n"
        fm = self.v.parse_frontmatter(text)
        self.assertIsNotNone(fm)
        assert fm is not None
        self.assertEqual(fm["name"], "demo-skill")
        self.assertIn("line one", fm["description"])
        self.assertIn("line two", fm["description"])


class TestRepoValidation(unittest.TestCase):
    """对当前仓库运行验证。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.v = load_validator()

    def test_current_repo_passes(self) -> None:
        code = self.v.main([])
        self.assertEqual(code, 0, "validate_skills.py should pass on this repo")

    def test_project_json_brand(self) -> None:
        data = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
        self.assertEqual(data["brand_name"], "ScholarlyOps")
        self.assertEqual(data["license_status"], "undetermined")
        self.assertEqual(data["skills_root"], ".agents/skills")
        self.assertEqual(
            data.get("distribution", {}).get("primary_end_user_path"),
            "agent_global_install",
        )

    def test_four_skills_present(self) -> None:
        skills = ROOT / ".agents" / "skills"
        for name in (
            "research-context",
            "evidence-writing",
            "manuscript-audit",
            "review-response",
        ):
            self.assertTrue((skills / name / "SKILL.md").is_file(), name)

    def test_eval_cases_exist(self) -> None:
        cases = ROOT / "evals" / "cases" / "manuscript-audit"
        self.assertTrue(cases.is_dir())
        found = list(cases.glob("*/input.md"))
        self.assertGreaterEqual(len(found), 17)
        for case_dir in cases.iterdir():
            if case_dir.is_dir():
                self.assertTrue(
                    (case_dir / "expect.json").is_file(),
                    f"missing expect.json in {case_dir.name}",
                )


class TestBrokenSkillDetected(unittest.TestCase):
    """临时损坏 Skill 应被检出。"""

    def test_name_mismatch_fails(self) -> None:
        v = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / ".agents" / "skills" / "good-name"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: wrong-name\ndescription: test\n---\n\n# x\n",
                encoding="utf-8",
            )
            # minimal stubs so required doc checks are not the only failures
            for rel in [
                "README.md",
                "README_EN.md",
                "CONTRIBUTING.md",
                "SECURITY.md",
                "CHANGELOG.md",
                "project.json",
                "docs/PRODUCT_SPEC.md",
                "docs/ROADMAP.md",
                "docs/decisions/open-questions.md",
                "docs/zh-CN/installation.md",
                "docs/zh-CN/architecture.md",
                "docs/en/installation.md",
                "docs/en/architecture.md",
                "evals/README.md",
                "docs/zh-CN/cursor-smoke-test.md",
                "docs/en/cursor-smoke-test.md",
                ".gitignore",
                ".editorconfig",
            ]:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                if rel.endswith("installation.md"):
                    path.write_text(".agents/skills\n", encoding="utf-8")
                elif rel == "project.json":
                    path.write_text(
                        json.dumps(
                            {
                                "brand_name": "ScholarlyOps",
                                "repo_name_suggested": "scholarlyops-skills",
                                "skills_root": ".agents/skills",
                                "license_status": "undetermined",
                            }
                        ),
                        encoding="utf-8",
                    )
                elif rel.startswith("README"):
                    path.write_text(
                        "# t\n\n[x](README_EN.md)\n[y](README.md)\n" if "EN" in rel else "# t\n\n[EN](README_EN.md)\n",
                        encoding="utf-8",
                    )
                else:
                    path.write_text("x\n", encoding="utf-8")

            code = v.main(["--root", str(root)])
            self.assertEqual(code, 1)


class TestNumericEvalCase(unittest.TestCase):
    """评测案例与脚本联动。"""

    def test_case_01_triggers_numeric_script(self) -> None:
        script = (
            ROOT
            / ".agents"
            / "skills"
            / "manuscript-audit"
            / "scripts"
            / "check_numeric_consistency.py"
        )
        spec = importlib.util.spec_from_file_location("numcheck", script)
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        text = (
            ROOT
            / "evals"
            / "cases"
            / "manuscript-audit"
            / "01_numeric_unit_mismatch"
            / "input.md"
        ).read_text(encoding="utf-8")
        findings = mod.find_conflicts(text)
        self.assertTrue(any(f["label"] == "enrolled_n" for f in findings))


if __name__ == "__main__":
    unittest.main()
