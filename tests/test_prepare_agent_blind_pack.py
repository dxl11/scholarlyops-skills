"""Tests for answer-free Agent blind-pack preparation."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from prepare_agent_blind_pack_loader import load_prepare_module


class TestPrepareAgentBlindPack(unittest.TestCase):
    """盲测包不得泄漏标准答案。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.mod = load_prepare_module()
        cls.repo = cls.mod.repo_root()

    def test_wave_a_copies_input_only(self) -> None:
        """Wave A 仅含 input.md 与 TASK.md，不含 expect。"""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "blind"
            code = self.mod.main(
                ["--wave", "wave_a_semantic_core", "--out", str(out)]
            )
            self.assertEqual(code, 0)
            manifest = json.loads(
                (out / "pack_manifest.json").read_text(encoding="utf-8")
            )
            self.assertFalse(manifest["contains_expect_or_answers"])
            self.assertEqual(len(manifest["case_ids"]), 7)
            for case_id in manifest["case_ids"]:
                case_dir = out / "CASES" / case_id
                self.assertTrue((case_dir / "input.md").is_file())
                self.assertTrue((case_dir / "TASK.md").is_file())
                self.assertFalse((case_dir / "expect.json").exists())
                self.assertFalse((case_dir / "case.yaml").exists())

    def test_single_case(self) -> None:
        """单案例导出成功。"""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "one"
            code = self.mod.main(
                ["--case", "06_citation_not_supporting", "--out", str(out)]
            )
            self.assertEqual(code, 0)
            self.assertTrue(
                (out / "CASES" / "06_citation_not_supporting" / "input.md").is_file()
            )

    def test_unknown_wave_fails(self) -> None:
        """未知 wave 非零退出。"""
        with tempfile.TemporaryDirectory() as tmp:
            code = self.mod.main(
                ["--wave", "not_a_real_wave", "--out", str(Path(tmp) / "x")]
            )
            self.assertNotEqual(code, 0)

    def test_task_mentions_forbidden_expect(self) -> None:
        """TASK 明确禁止读取 expect。"""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "t"
            self.mod.main(["--case", "02_correlation_to_causation", "--out", str(out)])
            task = (out / "CASES" / "02_correlation_to_causation" / "TASK.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("expect.json", task)
            self.assertIn("Do **not**", task)


if __name__ == "__main__":
    unittest.main()
