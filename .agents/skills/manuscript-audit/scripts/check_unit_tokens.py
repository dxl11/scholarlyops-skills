#!/usr/bin/env python3
"""Heuristic unit-token scanner for manuscript-audit.

Collects numeric+unit occurrences with line/context, normalizes obvious aliases
(μ / µ / u), and reports *candidate* mixed-unit situations for review.

Never certifies a scientific unit error as Critical/verified.
Does not perform unit conversion without required context (MW, density, etc.).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

MAX_BYTES = 2_000_000

# Longer tokens first where needed for matching.
UNIT_SPECS: list[dict[str, Any]] = [
    {
        "family": "concentration",
        "token": "µg/mL",
        "canonical": "ug/ml",
        "class": "mass_per_volume",
    },
    {
        "family": "concentration",
        "token": "ug/mL",
        "canonical": "ug/ml",
        "class": "mass_per_volume",
    },
    {
        "family": "concentration",
        "token": "mg/mL",
        "canonical": "mg/ml",
        "class": "mass_per_volume",
    },
    {
        "family": "concentration",
        "token": "μM",
        "canonical": "um",
        "class": "molar",
    },
    {
        "family": "concentration",
        "token": "µM",  # micro sign U+00B5
        "canonical": "um",
        "class": "molar",
    },
    {
        "family": "concentration",
        "token": "uM",
        "canonical": "um",
        "class": "molar",
    },
    {
        "family": "concentration",
        "token": "nM",
        "canonical": "nm",
        "class": "molar",
    },
    {
        "family": "concentration",
        "token": "mM",
        "canonical": "mm",
        "class": "molar",
    },
    {"family": "time", "token": "hours", "canonical": "h", "class": "duration"},
    {"family": "time", "token": "hour", "canonical": "h", "class": "duration"},
    {"family": "time", "token": "hr", "canonical": "h", "class": "duration"},
    {"family": "time", "token": "minutes", "canonical": "min", "class": "duration"},
    {"family": "time", "token": "min", "canonical": "min", "class": "duration"},
    {"family": "time", "token": "sec", "canonical": "s", "class": "duration"},
    {"family": "time", "token": "s", "canonical": "s", "class": "duration"},
    {"family": "time", "token": "h", "canonical": "h", "class": "duration"},
    {
        "family": "temperature",
        "token": "°C",
        "canonical": "celsius",
        "class": "temp_c",
    },
    {"family": "temperature", "token": "C", "canonical": "celsius", "class": "temp_c"},
    {"family": "temperature", "token": "K", "canonical": "kelvin", "class": "temp_k"},
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


def _line_map(text: str) -> list[tuple[int, int, str]]:
    """构建行映射。

    Args:
        text: 全文。

    Returns:
        (start, end, line_text) 列表。
    """
    lines: list[tuple[int, int, str]] = []
    offset = 0
    for line in text.splitlines(keepends=True):
        lines.append((offset, offset + len(line), line.rstrip("\r\n")))
        offset += len(line)
    return lines


def _offset_to_line(lines: list[tuple[int, int, str]], offset: int) -> tuple[int, str]:
    """偏移转行号。

    Args:
        lines: 行映射。
        offset: 字符偏移。

    Returns:
        (line_no, line_text)。
    """
    for idx, (start, end, content) in enumerate(lines):
        if start <= offset < end or (offset == end and idx == len(lines) - 1):
            return idx + 1, content
    if lines:
        return len(lines), lines[-1][2]
    return 1, ""


def normalize_unit_token(token: str) -> str:
    """规范化单位书写别名（不做量纲换算）。

    Args:
        token: 原始单位字符串。

    Returns:
        规范化键。
    """
    t = token.strip()
    t = t.replace("μ", "u").replace("µ", "u").replace("Μ", "u")
    t = t.replace("µg", "ug").replace("μg", "ug")
    return t


def collect_unit_occurrences(text: str) -> list[dict[str, Any]]:
    """收集数值+单位出现及其位点。

    Args:
        text: 稿件文本。

    Returns:
        出现列表。
    """
    lines = _line_map(text)
    # Sort tokens by length descending to prefer µg/mL over g etc.
    specs = sorted(UNIT_SPECS, key=lambda s: len(s["token"]), reverse=True)
    occurrences: list[dict[str, Any]] = []
    occupied: set[tuple[int, int]] = set()

    for spec in specs:
        token = spec["token"]
        # Word-ish boundary: avoid matching bare "C" inside words via lookaround.
        if token == "C":
            pattern = re.compile(
                rf"(\d+(?:\.\d+)?)\s*(°?C)\b",
                re.IGNORECASE,
            )
        elif token == "s":
            pattern = re.compile(rf"(\d+(?:\.\d+)?)\s*(s)\b(?![a-z])", re.IGNORECASE)
        else:
            pattern = re.compile(
                rf"(\d+(?:\.\d+)?)\s*({re.escape(token)})\b",
                re.IGNORECASE if token.isascii() else 0,
            )
        for match in pattern.finditer(text):
            span = (match.start(), match.end())
            if any(not (span[1] <= a or span[0] >= b) for a, b in occupied):
                continue
            occupied.add(span)
            line_no, line_text = _offset_to_line(lines, match.start())
            raw_unit = match.group(2)
            occurrences.append(
                {
                    "family": spec["family"],
                    "unit_raw": raw_unit,
                    "unit_normalized": spec["canonical"],
                    "unit_class": spec["class"],
                    "value": match.group(1),
                    "line": line_no,
                    "context": line_text.strip(),
                    "match_text": match.group(0),
                    "span": [match.start(), match.end()],
                }
            )
    return occurrences


def analyze_units(text: str) -> dict[str, Any]:
    """分析单位出现并生成候选/容差结果。

    Args:
        text: 稿件文本。

    Returns:
        occurrences、tolerated、candidates、conflicts、error_findings。
    """
    occurrences = collect_unit_occurrences(text)
    by_family: dict[str, list[dict[str, Any]]] = {}
    for occ in occurrences:
        by_family.setdefault(occ["family"], []).append(occ)

    tolerated: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []

    for family, group in sorted(by_family.items()):
        classes = {o["unit_class"] for o in group}
        canonicals = {o["unit_normalized"] for o in group}
        raw_units = sorted({o["unit_raw"] for o in group})
        loci = [
            {
                "line": o["line"],
                "value": o["value"],
                "unit_raw": o["unit_raw"],
                "unit_normalized": o["unit_normalized"],
                "unit_class": o["unit_class"],
                "context": o["context"],
                "match_text": o["match_text"],
            }
            for o in group
        ]

        if len(canonicals) <= 1:
            if len(raw_units) > 1:
                tolerated.append(
                    {
                        "check": "unit_tokens",
                        "quantity_family": family,
                        "classification": "unit_alias_only",
                        "units_seen": raw_units,
                        "canonicals": sorted(canonicals),
                        "loci": loci,
                        "severity": None,
                        "evidence_state": "verified",
                        "scored_as_error": False,
                        "note": "Multiple spellings normalize to the same unit alias (e.g. μM/µM/uM).",
                    }
                )
            continue

        # Same class, different canonical (e.g. h vs min): convertible in principle
        # but may be intentional different durations — candidate, not certified error.
        if len(classes) == 1:
            candidates.append(
                {
                    "check": "unit_tokens",
                    "quantity_family": family,
                    "classification": "same_class_different_scale",
                    "units_seen": raw_units,
                    "unit_classes": sorted(classes),
                    "canonicals": sorted(canonicals),
                    "severity": "Needs Review",
                    "evidence_state": "unverified",
                    "scored_as_error": False,
                    "loci": loci,
                    "note": (
                        "Same unit class with different scales/symbols. "
                        "May be intentional (different timepoints/conditions). "
                        "No conversion performed."
                    ),
                }
            )
            continue

        # Distinct classes in one family (e.g. molar vs mass/volume)
        candidates.append(
            {
                "check": "unit_tokens",
                "quantity_family": family,
                "classification": "possibly_incompatible_unit_classes",
                "units_seen": raw_units,
                "unit_classes": sorted(classes),
                "canonicals": sorted(canonicals),
                "severity": "Needs Review",
                "evidence_state": "partially_supported",
                "scored_as_error": False,
                "loci": loci,
                "note": (
                    "Mixed unit classes under the same quantity family were detected. "
                    "Conversion would require additional information (e.g. molecular weight); "
                    "not certified as a confirmed error. Different substances/conditions may "
                    "legitimately use different units."
                ),
                "limits": [
                    "Does not prove the tokens refer to the same quantity or substance.",
                    "No unit conversion is attempted.",
                ],
            }
        )

    return {
        "occurrences": occurrences,
        "tolerated": tolerated,
        "candidates": candidates,
        "conflicts": candidates,
        "error_findings": [],
        "limits": [
            "Alias normalization covers μ/µ/u style micro signs; incomplete for all notations.",
            "Cannot reliably separate different experimental conditions without NLP.",
            "Never emits Critical/verified scientific unit errors.",
        ],
    }


def find_unit_conflicts(text: str) -> list[dict[str, Any]]:
    """返回单位相关候选列表（兼容旧测试名）。

    Args:
        text: 稿件文本。

    Returns:
        candidates。
    """
    return analyze_units(text)["candidates"]


def main(argv: list[str] | None = None) -> int:
    """命令行入口。

    Args:
        argv: CLI 参数。

    Returns:
        退出码。
    """
    parser = argparse.ArgumentParser(description="Unit token heuristic (candidate reporter)")
    parser.add_argument("--input", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        text = _read_text(Path(args.input))
        analysis = analyze_units(text)
        payload = {
            "tool": "check_unit_tokens.py",
            "candidate_count": len(analysis["candidates"]),
            "error_finding_count": 0,
            "findings": analysis["candidates"],
            "candidates": analysis["candidates"],
            "error_findings": [],
            "tolerated_differences": analysis["tolerated"],
            "occurrences": analysis["occurrences"],
            "limits": analysis["limits"],
        }
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"candidates={len(analysis['candidates'])} errors=0")
            for item in analysis["candidates"]:
                print(
                    f"- [{item['severity']}] {item['quantity_family']}: "
                    f"{item['units_seen']} ({item['classification']})"
                )
            for item in analysis["tolerated"]:
                print(
                    f"- [tolerated/{item['classification']}] "
                    f"{item['quantity_family']}: {item['units_seen']}"
                )
            if not analysis["candidates"] and not analysis["tolerated"]:
                print("No unit candidates or alias-only diffs detected.")
        return 0
    except SkillScriptError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
