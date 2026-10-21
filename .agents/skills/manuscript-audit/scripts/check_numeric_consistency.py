#!/usr/bin/env python3
"""Heuristic numeric consistency scanner for manuscript-audit.

Detects repeated measure-like phrases with conflicting numeric literals
in the same document. Distinguishes:
  - format-only differences (7.1 vs 7.10)
  - differences within rounding tolerance
  - true literal conflicts

This is NOT a full scientific validator and does NOT perform unit conversion
or semantic claim checking.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_TIMEOUT_NOTE = "local_file_read"
MAX_BYTES = 2_000_000
DEFAULT_ABS_TOL = 0.051  # tolerate one-decimal rounding noise (e.g. 7.14 -> 7.1)
DEFAULT_REL_TOL = 0.0

# Pairs of (label_pattern, number capture). Intentionally simple.
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "enrolled_n",
        re.compile(
            r"(?:enrolled|recruited|included)\s+(\d+(?:\.\d+)?)\s+"
            r"(?:patients|participants|subjects)",
            re.IGNORECASE,
        ),
    ),
    (
        "sample_n",
        re.compile(r"\bn\s*=\s*(\d+(?:\.\d+)?)\b", re.IGNORECASE),
    ),
    (
        "mean_response_pct",
        re.compile(
            r"(?:mean\s+response(?:\s+rate)?|平均(?:响应|应答)(?:率)?)\s*"
            r"(?:was|of|为|:)?\s*(\d+(?:\.\d+)?)\s*%",
            re.IGNORECASE,
        ),
    ),
    (
        "orr_pct",
        re.compile(
            r"(?:ORR|overall response rate)\s*(?:was|of|=|:)?\s*(\d+(?:\.\d+)?)\s*%",
            re.IGNORECASE,
        ),
    ),
    (
        "mean_tumor_reduction_pct",
        re.compile(
            r"mean tumor size reduction of\s*(\d+(?:\.\d+)?)\s*%",
            re.IGNORECASE,
        ),
    ),
    (
        "mean_score",
        re.compile(
            r"mean score(?:\s+was|\s+of|:)?\s*(\d+(?:\.\d+)?)\b",
            re.IGNORECASE,
        ),
    ),
]


class SkillScriptError(Exception):
    """统一脚本异常包装。"""


def _read_text(path: Path, max_bytes: int = MAX_BYTES) -> str:
    """读取文本文件，限制最大字节数。

    Args:
        path: 输入文件路径。
        max_bytes: 允许读取的最大字节数。

    Returns:
        文件文本内容。

    Raises:
        SkillScriptError: 文件不存在、过大或读取失败。
    """
    try:
        if not path.is_file():
            raise SkillScriptError(f"input_not_found:{path}")
        size = path.stat().st_size
        if size > max_bytes:
            raise SkillScriptError(f"input_too_large:{size}>{max_bytes}")
        return path.read_text(encoding="utf-8", errors="replace")
    except SkillScriptError:
        raise
    except OSError as exc:
        raise SkillScriptError(f"read_failed:{exc}") from exc


def _to_float(value: str) -> float:
    """将捕获的数字字符串转为 float。

    Args:
        value: 数字字符串。

    Returns:
        浮点值。
    """
    return float(value)


def classify_value_set(
    raw_values: list[str],
    abs_tol: float = DEFAULT_ABS_TOL,
    rel_tol: float = DEFAULT_REL_TOL,
) -> dict[str, Any]:
    """对同一标签下的数值集合做冲突分类。

    Args:
        raw_values: 原始字符串数值列表。
        abs_tol: 绝对容差（四舍五入容忍）。
        rel_tol: 相对容差。

    Returns:
        含 classification、unique_raw、unique_floats 等字段的字典。
        classification 为 format_only | within_rounding_tolerance | literal_conflict | single。
    """
    unique_raw = sorted(set(raw_values), key=lambda x: (_to_float(x), x))
    floats = [_to_float(v) for v in unique_raw]
    unique_floats = sorted(set(floats))

    if len(unique_floats) <= 1:
        if len(unique_raw) <= 1:
            return {
                "classification": "single",
                "unique_raw": unique_raw,
                "unique_floats": unique_floats,
            }
        return {
            "classification": "format_only",
            "unique_raw": unique_raw,
            "unique_floats": unique_floats,
            "note": "String forms differ but numeric values are equal.",
        }

    # Check pairwise tolerance against min/max span
    lo, hi = unique_floats[0], unique_floats[-1]
    tol = abs_tol
    if rel_tol > 0:
        tol = max(abs_tol, abs(lo) * rel_tol, abs(hi) * rel_tol)
    if (hi - lo) <= tol + 1e-12:
        return {
            "classification": "within_rounding_tolerance",
            "unique_raw": unique_raw,
            "unique_floats": unique_floats,
            "abs_tol": abs_tol,
            "rel_tol": rel_tol,
            "note": "Differences fall within configured rounding tolerance; not scored as an error.",
        }

    return {
        "classification": "literal_conflict",
        "unique_raw": unique_raw,
        "unique_floats": unique_floats,
        "note": "Same measure label matched with differing numeric literals beyond tolerance.",
    }


def find_conflicts(
    text: str,
    abs_tol: float = DEFAULT_ABS_TOL,
    rel_tol: float = DEFAULT_REL_TOL,
) -> list[dict[str, Any]]:
    """查找同标签下的数值冲突（仅 literal_conflict 记为错误级发现）。

    Args:
        text: 稿件文本。
        abs_tol: 绝对容差。
        rel_tol: 相对容差。

    Returns:
        冲突列表（仅含应报告为问题的项）。
    """
    findings: list[dict[str, Any]] = []
    for label, pattern in PATTERNS:
        values = pattern.findall(text)
        if not values:
            continue
        classified = classify_value_set(values, abs_tol=abs_tol, rel_tol=rel_tol)
        if classified["classification"] != "literal_conflict":
            continue
        findings.append(
            {
                "check": "numeric_consistency",
                "label": label,
                "values": classified["unique_raw"],
                "unique_floats": classified["unique_floats"],
                "classification": "literal_conflict",
                "severity": "Critical",
                "evidence_state": "verified",
                "note": classified["note"],
            }
        )
    return findings


def analyze_all(
    text: str,
    abs_tol: float = DEFAULT_ABS_TOL,
    rel_tol: float = DEFAULT_REL_TOL,
) -> dict[str, Any]:
    """分析全部标签，包含容差内与格式差异（供评测与调试）。

    Args:
        text: 稿件文本。
        abs_tol: 绝对容差。
        rel_tol: 相对容差。

    Returns:
        含 conflicts、tolerated、observed_labels 的分析结果。
    """
    conflicts: list[dict[str, Any]] = []
    tolerated: list[dict[str, Any]] = []
    observed: list[dict[str, Any]] = []

    for label, pattern in PATTERNS:
        values = pattern.findall(text)
        if not values:
            continue
        classified = classify_value_set(values, abs_tol=abs_tol, rel_tol=rel_tol)
        entry = {"label": label, **classified}
        observed.append(entry)
        if classified["classification"] == "literal_conflict":
            conflicts.append(
                {
                    "check": "numeric_consistency",
                    "label": label,
                    "values": classified["unique_raw"],
                    "unique_floats": classified["unique_floats"],
                    "classification": "literal_conflict",
                    "severity": "Critical",
                    "evidence_state": "verified",
                    "note": classified["note"],
                }
            )
        elif classified["classification"] in {
            "format_only",
            "within_rounding_tolerance",
        }:
            tolerated.append(
                {
                    "check": "numeric_consistency",
                    "label": label,
                    "classification": classified["classification"],
                    "values": classified["unique_raw"],
                    "severity": None,
                    "evidence_state": "verified",
                    "note": classified.get("note", ""),
                    "scored_as_error": False,
                }
            )

    return {
        "conflicts": conflicts,
        "tolerated": tolerated,
        "observed_labels": observed,
    }


def main(argv: list[str] | None = None) -> int:
    """命令行入口。

    Args:
        argv: 参数列表；默认使用 sys.argv[1:]。

    Returns:
        进程退出码；0 表示执行成功（即使发现冲突）。
    """
    parser = argparse.ArgumentParser(description="Numeric consistency heuristic")
    parser.add_argument("--input", required=True, help="Path to manuscript text")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument(
        "--abs-tol",
        type=float,
        default=DEFAULT_ABS_TOL,
        help="Absolute tolerance for rounding (default 0.051)",
    )
    parser.add_argument(
        "--rel-tol",
        type=float,
        default=DEFAULT_REL_TOL,
        help="Relative tolerance (default 0.0)",
    )
    args = parser.parse_args(argv)

    try:
        text = _read_text(Path(args.input))
        analysis = analyze_all(text, abs_tol=args.abs_tol, rel_tol=args.rel_tol)
        findings = analysis["conflicts"]
        payload = {
            "tool": "check_numeric_consistency.py",
            "timeout_model": DEFAULT_TIMEOUT_NOTE,
            "abs_tol": args.abs_tol,
            "rel_tol": args.rel_tol,
            "finding_count": len(findings),
            "findings": findings,
            "tolerated_differences": analysis["tolerated"],
            "limits": [
                "Heuristic regex only; may miss paraphrases.",
                "Does not convert units or judge causality.",
                "Rounding tolerance avoids scoring tiny format/rounding diffs as Critical.",
                "Not a substitute for author review.",
            ],
        }
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"findings={len(findings)}")
            for item in findings:
                print(
                    f"- [{item['severity']}] {item['label']}: "
                    f"values={item['values']} ({item['note']})"
                )
            for item in analysis["tolerated"]:
                print(
                    f"- [tolerated/{item['classification']}] {item['label']}: "
                    f"values={item['values']}"
                )
            if not findings and not analysis["tolerated"]:
                print("No conflicting labeled numerics detected by heuristics.")
        return 0
    except SkillScriptError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
