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

    def test_detects_enrollment_candidate_with_loci(self) -> None:
        text = "We enrolled 120 patients.\nWe enrolled 100 patients."
        findings = self.mod.find_conflicts(text)
        self.assertEqual(len(findings), 1)
        item = findings[0]
        self.assertEqual(item["label"], "enrolled_n")
        self.assertEqual(item["severity"], "Needs Review")
        self.assertNotEqual(item["evidence_state"], "verified")
        self.assertFalse(item.get("scored_as_error"))
        self.assertGreaterEqual(len(item["loci"]), 2)
        self.assertTrue(all("line" in x and "context" in x for x in item["loci"]))

    def test_never_emits_critical_or_error_findings(self) -> None:
        text = "ORR was 62%.\nORR was 41%."
        analysis = self.mod.analyze_all(text)
        self.assertEqual(analysis["error_findings"], [])
        for item in analysis["candidates"]:
            self.assertNotEqual(item["severity"], "Critical")

    def test_clean_text_no_candidate(self) -> None:
        text = "We enrolled 100 patients. Mean response was 48%."
        self.assertEqual(self.mod.find_conflicts(text), [])

    def test_rounding_not_candidate(self) -> None:
        text = "Mean score was 7.14.\nMean score was 7.1."
        analysis = self.mod.analyze_all(text)
        self.assertEqual(analysis["candidates"], [])
        self.assertTrue(
            any(
                t["classification"] == "within_rounding_tolerance"
                for t in analysis["tolerated"]
            )
        )

    def test_format_only_not_candidate(self) -> None:
        text = "Mean score was 7.10.\nMean score was 7.1."
        analysis = self.mod.analyze_all(text)
        self.assertEqual(analysis["candidates"], [])
        self.assertTrue(
            any(t["classification"] == "format_only" for t in analysis["tolerated"])
        )

    def test_treatment_vs_control_not_candidate(self) -> None:
        text = (
            "Mean score was 8.2 in the treatment group.\n"
            "Mean score was 3.1 in the control group."
        )
        analysis = self.mod.analyze_all(text)
        self.assertEqual(analysis["candidates"], [])
        self.assertTrue(
            any(
                t["classification"] == "cross_scope_difference"
                for t in analysis["tolerated"]
            )
        )

    def test_timepoints_not_candidate(self) -> None:
        text = "Mean score was 7.0 at week 4.\nMean score was 5.2 at week 12."
        analysis = self.mod.analyze_all(text)
        self.assertEqual(analysis["candidates"], [])
        self.assertTrue(
            any(
                t["classification"] == "cross_scope_difference"
                for t in analysis["tolerated"]
            )
        )

    def test_enrolled_vs_analyzed_separate_labels(self) -> None:
        text = (
            "We enrolled 120 patients at baseline.\n"
            "In the analyzed ITT set, n=100."
        )
        analysis = self.mod.analyze_all(text)
        # Different labels; no within-label conflict required
        self.assertEqual(analysis["candidates"], [])

    def test_orr_candidate(self) -> None:
        text = "ORR was 62%.\nORR was 41%."
        findings = self.mod.find_conflicts(text)
        self.assertTrue(any(f["label"] == "orr_pct" for f in findings))


class TestUnitScript(unittest.TestCase):
    """单位 token 脚本测试。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.mod = _load("check_unit_tokens", "check_unit_tokens.py")

    def test_mixed_concentration_is_candidate_not_critical(self) -> None:
        text = "Treated at 10 uM and later 10 mg/mL."
        findings = self.mod.find_unit_conflicts(text)
        self.assertTrue(any(f["quantity_family"] == "concentration" for f in findings))
        for item in findings:
            self.assertEqual(item["severity"], "Needs Review")
            self.assertFalse(item.get("scored_as_error"))
            self.assertTrue(item.get("loci"))

    def test_micro_symbol_aliases_tolerated(self) -> None:
        text = "Dose was 10 μM in batch A and 10 µM in batch B and 10 uM in batch C."
        analysis = self.mod.analyze_units(text)
        self.assertEqual(analysis["candidates"], [])
        self.assertEqual(analysis["error_findings"], [])
        self.assertTrue(
            any(t["classification"] == "unit_alias_only" for t in analysis["tolerated"])
        )

    def test_clean_single_unit_no_candidate(self) -> None:
        text = "Cells were treated at 10 uM for 24 h."
        self.assertEqual(self.mod.find_unit_conflicts(text), [])

    def test_never_critical(self) -> None:
        text = "Used 5 mM and 2 mg/mL stocks."
        for item in self.mod.find_unit_conflicts(text):
            self.assertNotEqual(item["severity"], "Critical")


if __name__ == "__main__":
    unittest.main()
