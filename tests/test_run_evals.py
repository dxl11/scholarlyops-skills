#!/usr/bin/env python3
"""Tests for tools/run_evals.py."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "run_evals.py"


def load_runner():
    """加载 run_evals 模块。

    Returns:
        模块对象。
    """
    spec = importlib.util.spec_from_file_location("run_evals", RUNNER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["run_evals"] = module
    spec.loader.exec_module(module)
    return module


class TestRunEvals(unittest.TestCase):
    """评测运行器集成测试。"""

    def test_local_evals_pass_or_skip_only(self) -> None:
        mod = load_runner()
        code, summary = mod.run(ROOT)
        self.assertEqual(code, 0, msg=summary)
        self.assertGreaterEqual(summary["totals"]["total"], 17)
        self.assertGreater(summary["totals"]["passed"], 0)
        self.assertGreater(summary["totals"]["skipped"], 0)
        self.assertEqual(summary["totals"]["failed"], 0)
        # ensure semantic cases are skips, not passes
        semantic = [
            c for c in summary["cases"] if c["mode"] == "agent_semantic"
        ]
        self.assertTrue(semantic)
        self.assertTrue(all(c["status"] == "skip" for c in semantic))


if __name__ == "__main__":
    unittest.main()
