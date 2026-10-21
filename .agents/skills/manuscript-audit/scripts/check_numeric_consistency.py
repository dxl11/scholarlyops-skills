#!/usr/bin/env python3
"""Heuristic numeric consistency scanner for manuscript-audit.

Reports *candidate* inconsistencies with loci for agent/human review.
Does NOT certify scientific errors: regex alone never yields evidence_state
`verified` or severity `Critical`.

Classifies:
  - format_only (7.1 vs 7.10)
  - within_rounding_tolerance
  - cross_scope_difference (e.g. treatment vs control; week 4 vs week 12)
  - candidate_inconsistency (same label, values differ, scope not clearly distinct)

This is NOT a full scientific validator.
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
DEFAULT_ABS_TOL = 0.051
DEFAULT_REL_TOL = 0.0

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

# Context cues that suggest different experimental scopes (heuristic, incomplete).
SCOPE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("arm_treatment", re.compile(r"\b(?:treatment|treated|intervention)\s+(?:arm|group)?\b|\btreatment\b", re.I)),
    ("arm_control", re.compile(r"\b(?:control|placebo|vehicle)\s+(?:arm|group)?\b|\bcontrols?\b", re.I)),
    ("time_baseline", re.compile(r"\bbaseline\b|\bday\s*0\b|\bpre[- ]?dose\b", re.I)),
    ("time_week", re.compile(r"\bweek\s*(\d+)\b", re.I)),
    ("time_month", re.compile(r"\bmonth\s*(\d+)\b", re.I)),
    ("time_day", re.compile(r"\bday\s*(\d+)\b", re.I)),
    ("pop_enrolled", re.compile(r"\benrolled\b|\brecruited\b|\bincluded\b", re.I)),
    ("pop_analyzed", re.compile(r"\banalyze[sd]\b|\banalysis\s+set\b|\bITT\b|\bPP\b|\bFAS\b|\bsafety\s+population\b", re.I)),
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


def _line_map(text: str) -> list[tuple[int, int, str]]:
    """构建字符偏移到行的映射。

    Args:
        text: 全文。

    Returns:
        列表项为 (start_offset, end_offset, line_text)，行号从 1 起对应下标+1。
    """
    lines: list[tuple[int, int, str]] = []
    offset = 0
    for line in text.splitlines(keepends=True):
        start = offset
        end = offset + len(line)
        lines.append((start, end, line.rstrip("\r\n")))
        offset = end
    return lines


def _offset_to_line(lines: list[tuple[int, int, str]], offset: int) -> tuple[int, str]:
    """字符偏移转行号与行文本。

    Args:
        lines: _line_map 结果。
        offset: 字符偏移。

    Returns:
        (line_number_1based, line_text)。
    """
    for idx, (start, end, content) in enumerate(lines):
        if start <= offset < end or (offset == end and idx == len(lines) - 1):
            return idx + 1, content
    if lines:
        return len(lines), lines[-1][2]
    return 1, ""


def extract_scope_hints(context: str) -> set[str]:
    """从上下文提取粗粒度实验范围提示。

    Args:
        context: 行文本或局部窗口。

    Returns:
        范围提示集合（可能为空）。正则无法可靠时返回空，由上层降级为候选复核。
    """
    hints: set[str] = set()
    for name, pattern in SCOPE_PATTERNS:
        match = pattern.search(context)
        if not match:
            continue
        if name in {"time_week", "time_month", "time_day"} and match.lastindex:
            hints.add(f"{name}:{match.group(1)}")
        else:
            hints.add(name)
    return hints


def collect_occurrences(text: str) -> list[dict[str, Any]]:
    """收集所有模式匹配及其位点。

    Args:
        text: 稿件文本。

    Returns:
        出现列表，每项含 label、value、line、context、span。
    """
    lines = _line_map(text)
    occurrences: list[dict[str, Any]] = []
    for label, pattern in PATTERNS:
        for match in pattern.finditer(text):
            raw = match.group(1)
            line_no, line_text = _offset_to_line(lines, match.start())
            window_start = max(0, match.start() - 60)
            window_end = min(len(text), match.end() + 60)
            window = text[window_start:window_end].replace("\n", " ")
            context = line_text if line_text.strip() else window
            occurrences.append(
                {
                    "label": label,
                    "value": raw,
                    "value_float": _to_float(raw),
                    "line": line_no,
                    "context": context.strip(),
                    "match_text": match.group(0),
                    "span": [match.start(), match.end()],
                    "scope_hints": sorted(extract_scope_hints(context)),
                }
            )
    return occurrences


def classify_value_set(
    raw_values: list[str],
    abs_tol: float = DEFAULT_ABS_TOL,
    rel_tol: float = DEFAULT_REL_TOL,
) -> dict[str, Any]:
    """对同一标签下的数值集合做数值层分类（不含范围语义）。

    Args:
        raw_values: 原始字符串数值列表。
        abs_tol: 绝对容差。
        rel_tol: 相对容差。

    Returns:
        classification 为 single | format_only | within_rounding_tolerance |
        beyond_tolerance。
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
            "note": "Differences fall within configured rounding tolerance.",
        }

    return {
        "classification": "beyond_tolerance",
        "unique_raw": unique_raw,
        "unique_floats": unique_floats,
        "note": "Numeric literals differ beyond tolerance for this label.",
    }


def _scopes_clearly_disjoint(occ_group: list[dict[str, Any]]) -> bool:
    """判断各组出现是否带有互斥的非空范围提示。

    Args:
        occ_group: 同一 label 的出现列表。

    Returns:
        True 表示存在至少两套互斥提示，宜视为跨范围差异而非自动错误。
    """
    hint_sets = [set(o.get("scope_hints") or []) for o in occ_group]
    nonempty = [h for h in hint_sets if h]
    if len(nonempty) < 2:
        return False
    # If every pair of nonempty sets is disjoint, treat as cross-scope.
    for i, a in enumerate(nonempty):
        for b in nonempty[i + 1 :]:
            if a & b:
                return False
    return True


def analyze_all(
    text: str,
    abs_tol: float = DEFAULT_ABS_TOL,
    rel_tol: float = DEFAULT_REL_TOL,
) -> dict[str, Any]:
    """分析全文数值一致性，输出候选异常与容差项。

    Args:
        text: 稿件文本。
        abs_tol: 绝对容差。
        rel_tol: 相对容差。

    Returns:
        含 occurrences、tolerated、candidates、conflicts、error_findings 的结果。
        conflicts 与 candidates 对齐，供旧评测兼容；error_findings 恒为空列表
        （启发式不得输出 Critical/verified）。
    """
    occurrences = collect_occurrences(text)
    by_label: dict[str, list[dict[str, Any]]] = {}
    for occ in occurrences:
        by_label.setdefault(occ["label"], []).append(occ)

    tolerated: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    observed: list[dict[str, Any]] = []

    for label, group in sorted(by_label.items()):
        raw_values = [o["value"] for o in group]
        classified = classify_value_set(raw_values, abs_tol=abs_tol, rel_tol=rel_tol)
        observed.append({"label": label, **classified, "occurrence_count": len(group)})

        if classified["classification"] in {"single"}:
            continue

        loci = [
            {
                "line": o["line"],
                "value": o["value"],
                "context": o["context"],
                "match_text": o["match_text"],
                "scope_hints": o["scope_hints"],
            }
            for o in group
        ]

        if classified["classification"] in {"format_only", "within_rounding_tolerance"}:
            tolerated.append(
                {
                    "check": "numeric_consistency",
                    "label": label,
                    "classification": classified["classification"],
                    "values": classified["unique_raw"],
                    "loci": loci,
                    "severity": None,
                    "evidence_state": "verified",
                    "note": classified.get("note", ""),
                    "scored_as_error": False,
                }
            )
            continue

        # beyond_tolerance
        if _scopes_clearly_disjoint(group):
            tolerated.append(
                {
                    "check": "numeric_consistency",
                    "label": label,
                    "classification": "cross_scope_difference",
                    "values": classified["unique_raw"],
                    "loci": loci,
                    "severity": None,
                    "evidence_state": "unverified",
                    "note": (
                        "Values differ but scope hints look disjoint "
                        "(e.g. arms/timepoints/populations). Not scored as an error; "
                        "agent should confirm they are not the same estimand."
                    ),
                    "scored_as_error": False,
                }
            )
            continue

        # Insufficient regex evidence to certify a scientific error.
        candidates.append(
            {
                "check": "numeric_consistency",
                "label": label,
                "values": classified["unique_raw"],
                "unique_floats": classified["unique_floats"],
                "classification": "candidate_inconsistency",
                "severity": "Needs Review",
                "evidence_state": "partially_supported",
                "scored_as_error": False,
                "loci": loci,
                "note": (
                    "Same detection label matched differing literals beyond tolerance, "
                    "without clearly disjoint scope hints. Candidate for agent/human review; "
                    "not certified Critical/verified by this heuristic."
                ),
                "limits": [
                    "Cannot reliably prove same estimand (arm/timepoint/population) via regex alone.",
                ],
            }
        )

    return {
        "occurrences": occurrences,
        "tolerated": tolerated,
        "candidates": candidates,
        # Backward-compatible alias used by evals/tests expecting "conflicts"
        "conflicts": candidates,
        "error_findings": [],
        "observed_labels": observed,
        "limits": [
            "Heuristic regex only; paraphrases and implicit estimands may be missed.",
            "Never emits Critical or verified for scientific error certification.",
            "Cross-scope cues are incomplete; empty hints force candidate review.",
        ],
    }


def find_conflicts(
    text: str,
    abs_tol: float = DEFAULT_ABS_TOL,
    rel_tol: float = DEFAULT_REL_TOL,
) -> list[dict[str, Any]]:
    """返回候选不一致列表（兼容旧测试名）。

    Args:
        text: 稿件文本。
        abs_tol: 绝对容差。
        rel_tol: 相对容差。

    Returns:
        candidates 列表（非已确认 Critical 错误）。
    """
    return analyze_all(text, abs_tol=abs_tol, rel_tol=rel_tol)["candidates"]


def main(argv: list[str] | None = None) -> int:
    """命令行入口。

    Args:
        argv: 参数列表；默认使用 sys.argv[1:]。

    Returns:
        进程退出码；0 表示执行成功。
    """
    parser = argparse.ArgumentParser(
        description="Numeric consistency heuristic (candidate reporter)"
    )
    parser.add_argument("--input", required=True, help="Path to manuscript text")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--abs-tol", type=float, default=DEFAULT_ABS_TOL)
    parser.add_argument("--rel-tol", type=float, default=DEFAULT_REL_TOL)
    args = parser.parse_args(argv)

    try:
        text = _read_text(Path(args.input))
        analysis = analyze_all(text, abs_tol=args.abs_tol, rel_tol=args.rel_tol)
        payload = {
            "tool": "check_numeric_consistency.py",
            "timeout_model": DEFAULT_TIMEOUT_NOTE,
            "abs_tol": args.abs_tol,
            "rel_tol": args.rel_tol,
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
                lines = ",".join(str(x["line"]) for x in item["loci"])
                print(
                    f"- [{item['severity']}/{item['evidence_state']}] "
                    f"{item['label']}: values={item['values']} lines={lines}"
                )
            for item in analysis["tolerated"]:
                print(
                    f"- [tolerated/{item['classification']}] {item['label']}: "
                    f"values={item['values']}"
                )
            if not analysis["candidates"] and not analysis["tolerated"]:
                print("No numeric candidates or tolerated diffs detected.")
        return 0
    except SkillScriptError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
