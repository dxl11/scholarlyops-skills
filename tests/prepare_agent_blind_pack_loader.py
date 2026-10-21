"""Helper to load tools/prepare_agent_blind_pack.py in unit tests."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def load_prepare_module() -> ModuleType:
    """动态加载盲测包准备模块。

    Returns:
        已加载的模块对象。

    Raises:
        RuntimeError: 加载失败。
    """
    path = Path(__file__).resolve().parents[1] / "tools" / "prepare_agent_blind_pack.py"
    spec = importlib.util.spec_from_file_location("prepare_agent_blind_pack", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot_load:{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
