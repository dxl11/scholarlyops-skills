#!/usr/bin/env python3
"""Skill-local tests for manuscript-audit scripts."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def _load(name: str, filename: str):
    """动态加载脚本模块。

    Args:
        name: 模块名。
        filename: 脚本文件名。

    Returns:
        加载后的模块对象。

    Raises:
        FileNotFoundError: 脚本不存在。
    """
    path = SCRIPTS / filename
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestNumericScript(unittest.TestCase):
    """数值一致性脚本测试。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.mod = _load("check_numeric_consistency", "check_numeric_consistency.py")

    def test_detects_enrollment_conflict(self) -> None:
        text = "We enrolled 120 patients.\nWe enrolled 100 patients."
        findings = self.mod.find_conflicts(text)
        self.assertTrue(any(f["label"] == "enrolled_n" for f in findings))

    def test_clean_text_no_conflict(self) -> None:
        text = "We enrolled 100 patients. Mean response was 48%."
        findings = self.mod.find_conflicts(text)
        self.assertEqual(findings, [])

    def test_rounding_not_error(self) -> None:
        text = "Mean score was 7.14.\nMean score was 7.1."
        analysis = self.mod.analyze_all(text)
        self.assertEqual(analysis["conflicts"], [])
        self.assertTrue(
            any(
                t["classification"] == "within_rounding_tolerance"
                for t in analysis["tolerated"]
            )
        )

    def test_format_only_not_error(self) -> None:
        text = "Mean score was 7.10.\nMean score was 7.1."
        analysis = self.mod.analyze_all(text)
        self.assertEqual(analysis["conflicts"], [])
        self.assertTrue(
            any(t["classification"] == "format_only" for t in analysis["tolerated"])
        )

    def test_orr_conflict(self) -> None:
        text = "ORR was 62%.\nORR was 41%."
        findings = self.mod.find_conflicts(text)
        self.assertTrue(any(f["label"] == "orr_pct" for f in findings))


class TestUnitScript(unittest.TestCase):
    """单位 token 脚本测试。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.mod = _load("check_unit_tokens", "check_unit_tokens.py")

    def test_mixed_concentration_units(self) -> None:
        text = "Treated at 10 uM and later 10 mg/mL."
        findings = self.mod.find_unit_conflicts(text)
        self.assertTrue(any(f["quantity_family"] == "concentration" for f in findings))


if __name__ == "__main__":
    unittest.main()
