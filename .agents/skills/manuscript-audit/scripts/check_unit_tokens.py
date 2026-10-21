#!/usr/bin/env python3
"""Heuristic unit-token conflict scanner for manuscript-audit.

Flags the same quantity word appearing with differing unit tokens nearby.
Limited heuristic — not full unit conversion or dimensional analysis.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

MAX_BYTES = 2_000_000

QUANTITY_UNITS: list[tuple[str, list[str]]] = [
    ("concentration", [r"μM", r"uM", r"nM", r"mM", r"mg/mL", r"µg/mL", r"ug/mL"]),
    ("time", [r"h", r"hr", r"hours", r"min", r"minutes", r"s", r"sec"]),
    ("temperature", [r"°C", r"C", r"K"]),
]


class SkillScriptError(Exception):
    """统一脚本异常包装。"""


def _read_text(path: Path, max_bytes: int = MAX_BYTES) -> str:
    """读取文本文件。

    Args:
        path: 输入路径。
        max_bytes: 最大字节数。

    Returns:
        文本内容。

    Raises:
        SkillScriptError: 读取失败或文件过大。
    """
    try:
        if not path.is_file():
            raise SkillScriptError(f"input_not_found:{path}")
        if path.stat().st_size > max_bytes:
            raise SkillScriptError("input_too_large")
        return path.read_text(encoding="utf-8", errors="replace")
    except SkillScriptError:
        raise
    except OSError as exc:
        raise SkillScriptError(f"read_failed:{exc}") from exc


def find_unit_conflicts(text: str) -> list[dict[str, Any]]:
    """查找数量词附近出现的多种单位 token。

    Args:
        text: 稿件文本。

    Returns:
        发现列表。
    """
    findings: list[dict[str, Any]] = []
    for quantity, units in QUANTITY_UNITS:
        hit_units: set[str] = set()
        for unit in units:
            pattern = re.compile(
                rf"(\d+(?:\.\d+)?)\s*({re.escape(unit)})\b",
                re.IGNORECASE,
            )
            for match in pattern.finditer(text):
                hit_units.add(match.group(2))
        # Normalize trivial aliases
        normalized = set()
        for u in hit_units:
            key = u.lower().replace("μ", "u").replace("µg", "ug")
            if key in {"hr", "hours"}:
                key = "h"
            if key in {"minutes"}:
                key = "min"
            if key in {"sec"}:
                key = "s"
            normalized.add(key)
        if len(normalized) >= 2:
            findings.append(
                {
                    "check": "unit_tokens",
                    "quantity_family": quantity,
                    "units_seen": sorted(hit_units),
                    "severity": "Major",
                    "evidence_state": "partially_supported",
                    "note": "Multiple unit tokens for related numeric measures; confirm intentional vs error.",
                }
            )
    return findings


def main(argv: list[str] | None = None) -> int:
    """命令行入口。

    Args:
        argv: CLI 参数。

    Returns:
        退出码。
    """
    parser = argparse.ArgumentParser(description="Unit token heuristic")
    parser.add_argument("--input", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        text = _read_text(Path(args.input))
        findings = find_unit_conflicts(text)
        payload = {
            "tool": "check_unit_tokens.py",
            "finding_count": len(findings),
            "findings": findings,
            "limits": [
                "Does not convert units; alias collapsing is incomplete.",
                "False positives possible when mixed units are intentional.",
            ],
        }
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"findings={len(findings)}")
            for item in findings:
                print(
                    f"- [{item['severity']}] {item['quantity_family']}: "
                    f"{item['units_seen']}"
                )
            if not findings:
                print("No multi-unit conflicts flagged by heuristics.")
        return 0
    except SkillScriptError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
