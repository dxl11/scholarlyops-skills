#!/usr/bin/env python3
"""Run ScholarlyOps local (API-free) manuscript-audit evaluations.

Separates:
  - deterministic script checks (executed and scored here)
  - agent_semantic cases (skipped with explicit reason; never marked pass)

Writes timestamped outputs under evals/runs/ without modifying cases/expected.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class EvalRunnerError(Exception):
    """统一评测运行异常。"""


@dataclass
class CaseResult:
    """单个案例的运行结果。"""

    case_id: str
    mode: str
    status: str  # pass | fail | skip
    reason: str = ""
    details: dict[str, Any] = field(default_factory=dict)


def repo_root() -> Path:
    """返回仓库根目录。

    Returns:
        仓库根 Path。
    """
    return Path(__file__).resolve().parents[1]


def _load_module(name: str, path: Path):
    """动态加载 Python 模块。

    Args:
        name: 模块名。
        path: 文件路径。

    Returns:
        模块对象。

    Raises:
        EvalRunnerError: 加载失败。
    """
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise EvalRunnerError(f"cannot_load:{path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except EvalRunnerError:
        raise
    except Exception as exc:  # noqa: BLE001 — surface as unified error
        raise EvalRunnerError(f"load_failed:{path}:{exc}") from exc


def _read_json(path: Path) -> dict[str, Any]:
    """读取 JSON 文件。

    Args:
        path: JSON 路径。

    Returns:
        解析后的字典。

    Raises:
        EvalRunnerError: 读取或解析失败。
    """
    try:
        # utf-8-sig tolerates PowerShell/Windows BOM-prefixed JSON files
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvalRunnerError(f"json_error:{path}:{exc}") from exc


def _parse_mode_from_yaml(text: str) -> str | None:
    """从简易 case.yaml 提取 mode 字段（非完整 YAML 解析）。

    Args:
        text: YAML 文本。

    Returns:
        mode 字符串或 None。
    """
    match = re.search(r"^mode:\s*(\S+)", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def discover_cases(cases_root: Path) -> list[Path]:
    """发现 manuscript-audit 案例目录。

    Args:
        cases_root: cases/manuscript-audit 路径。

    Returns:
        排序后的案例目录列表。
    """
    if not cases_root.is_dir():
        return []
    return sorted(p for p in cases_root.iterdir() if p.is_dir() and (p / "input.md").is_file())


def evaluate_deterministic(
    case_dir: Path,
    expect: dict[str, Any],
    numeric_mod: Any,
    unit_mod: Any,
) -> CaseResult:
    """对确定性案例运行脚本并与期望比较。

    Args:
        case_dir: 案例目录。
        expect: expect.json 内容。
        numeric_mod: 数值检查模块。
        unit_mod: 单位检查模块。

    Returns:
        CaseResult。
    """
    case_id = case_dir.name
    input_path = case_dir / "input.md"
    try:
        text = input_path.read_text(encoding="utf-8")
    except OSError as exc:
        return CaseResult(case_id, "deterministic", "fail", f"read_input:{exc}")

    analysis = numeric_mod.analyze_all(text)
    numeric_findings = analysis["conflicts"]
    unit_findings = unit_mod.find_unit_conflicts(text)

    scripts = expect.get("scripts", {})
    num_exp = scripts.get("numeric", {})
    unit_exp = scripts.get("units", {})
    failures: list[str] = []

    found_labels = {f["label"] for f in numeric_findings}
    must_find = set(num_exp.get("must_find_labels", []))
    must_not = set(num_exp.get("must_not_find_labels", []))
    missing = sorted(must_find - found_labels)
    if missing:
        failures.append(f"numeric_missed_labels:{missing}")
    unexpected = sorted(found_labels & must_not)
    if unexpected:
        failures.append(f"numeric_forbidden_labels:{unexpected}")

    max_n = num_exp.get("max_findings")
    if max_n is not None and len(numeric_findings) > int(max_n):
        failures.append(
            f"numeric_too_many_findings:{len(numeric_findings)}>{max_n}"
        )
    min_n = num_exp.get("min_findings")
    if min_n is not None and len(numeric_findings) < int(min_n):
        failures.append(
            f"numeric_too_few_findings:{len(numeric_findings)}<{min_n}"
        )

    required_tol = set(num_exp.get("require_tolerated_classification", []))
    if required_tol:
        seen = {t["classification"] for t in analysis.get("tolerated", [])}
        # also accept observed_labels classifications
        seen |= {
            o["classification"]
            for o in analysis.get("observed_labels", [])
            if o.get("classification") in required_tol
        }
        missing_tol = sorted(required_tol - seen)
        if missing_tol:
            failures.append(f"missing_tolerated_classification:{missing_tol}")

    unit_families = {f["quantity_family"] for f in unit_findings}
    must_families = set(unit_exp.get("must_find_quantity_families", []))
    miss_f = sorted(must_families - unit_families)
    if miss_f:
        failures.append(f"units_missed_families:{miss_f}")
    max_u = unit_exp.get("max_findings")
    if max_u is not None and len(unit_findings) > int(max_u):
        failures.append(f"units_too_many:{len(unit_findings)}>{max_u}")
    min_u = unit_exp.get("min_findings")
    if min_u is not None and len(unit_findings) < int(min_u):
        failures.append(f"units_too_few:{len(unit_findings)}<{min_u}")

    details = {
        "numeric_findings": numeric_findings,
        "unit_findings": unit_findings,
        "tolerated": analysis.get("tolerated", []),
        "failures": failures,
    }
    if failures:
        return CaseResult(
            case_id,
            "deterministic",
            "fail",
            "; ".join(failures),
            details,
        )
    return CaseResult(case_id, "deterministic", "pass", "matched_expect_json", details)


def evaluate_case(
    case_dir: Path,
    numeric_mod: Any,
    unit_mod: Any,
) -> CaseResult:
    """评估单个案例。

    Args:
        case_dir: 案例目录。
        numeric_mod: 数值模块。
        unit_mod: 单位模块。

    Returns:
        CaseResult。
    """
    case_id = case_dir.name
    expect_path = case_dir / "expect.json"
    if not expect_path.is_file():
        return CaseResult(
            case_id,
            "unknown",
            "fail",
            "missing_expect_json",
        )

    try:
        expect = _read_json(expect_path)
    except EvalRunnerError as exc:
        return CaseResult(case_id, "unknown", "fail", str(exc))

    mode = expect.get("mode")
    if not mode and (case_dir / "case.yaml").is_file():
        mode = _parse_mode_from_yaml((case_dir / "case.yaml").read_text(encoding="utf-8"))
    mode = mode or "unknown"

    if mode == "agent_semantic" or expect.get("local_runner") == "skip_with_reason":
        return CaseResult(
            case_id,
            "agent_semantic",
            "skip",
            "requires_agent_or_human_judgment_not_executed",
            {
                "agent_expectations": expect.get("agent_expectations", {}),
                "note": "Not marked pass; semantic audit was not run.",
            },
        )

    if mode == "deterministic":
        return evaluate_deterministic(case_dir, expect, numeric_mod, unit_mod)

    return CaseResult(case_id, mode, "fail", f"unsupported_mode:{mode}")


def render_markdown(summary: dict[str, Any]) -> str:
    """生成人工可读 Markdown 汇总。

    Args:
        summary: 汇总字典。

    Returns:
        Markdown 文本。
    """
    lines = [
        "# ScholarlyOps eval run",
        "",
        f"- Generated (UTC): {summary['generated_at_utc']}",
        f"- Cases total: {summary['totals']['total']}",
        f"- Executed (deterministic): {summary['totals']['executed']}",
        f"- Passed: {summary['totals']['passed']}",
        f"- Failed: {summary['totals']['failed']}",
        f"- Skipped: {summary['totals']['skipped']}",
        "",
        "## Known limits",
        "",
    ]
    for item in summary.get("known_limits", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Case results", ""])
    for case in summary["cases"]:
        lines.append(
            f"- `{case['case_id']}` — **{case['status']}** "
            f"(mode={case['mode']}) — {case.get('reason', '')}"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Skipped agent_semantic cases are NOT passes.",
            "- Absence of script findings is not proof of scientific correctness.",
            "",
        ]
    )
    return "\n".join(lines)


def run(root: Path | None = None) -> tuple[int, dict[str, Any]]:
    """执行全部本地评测。

    Args:
        root: 仓库根；默认自动检测。

    Returns:
        (exit_code, summary_dict)。exit_code 在存在 fail 时非 0。

    Raises:
        EvalRunnerError: 关键路径或模块不可用。
    """
    root = root or repo_root()
    skill_scripts = root / ".agents" / "skills" / "manuscript-audit" / "scripts"
    numeric_mod = _load_module(
        "check_numeric_consistency",
        skill_scripts / "check_numeric_consistency.py",
    )
    unit_mod = _load_module(
        "check_unit_tokens",
        skill_scripts / "check_unit_tokens.py",
    )

    cases_root = root / "evals" / "cases" / "manuscript-audit"
    case_dirs = discover_cases(cases_root)
    results: list[CaseResult] = []
    for case_dir in case_dirs:
        results.append(evaluate_case(case_dir, numeric_mod, unit_mod))

    passed = sum(1 for r in results if r.status == "pass")
    failed = sum(1 for r in results if r.status == "fail")
    skipped = sum(1 for r in results if r.status == "skip")
    executed = sum(1 for r in results if r.mode == "deterministic" and r.status != "skip")

    summary: dict[str, Any] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "skill": "manuscript-audit",
        "skill_maturity": "Draft",
        "runner": "tools/run_evals.py",
        "totals": {
            "total": len(results),
            "executed": executed,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
        },
        "critical_miss_proxy": [
            asdict(r)
            for r in results
            if r.status == "fail" and r.mode == "deterministic"
        ],
        "false_positive_proxy": [
            asdict(r)
            for r in results
            if r.status == "fail" and "too_many" in r.reason
        ],
        "known_limits": [
            "Scripts are heuristic; paraphrases and unit conversions are out of scope.",
            "agent_semantic cases require Cursor/human review and are skipped here.",
            "Passing local evals does not prove zero real-world error rate.",
            "No external literature API calls are performed.",
        ],
        "cases": [asdict(r) for r in results],
    }

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = root / "evals" / "runs" / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "summary.md").write_text(render_markdown(summary), encoding="utf-8")
    # stable pointer without overwriting historical runs
    latest = root / "evals" / "runs" / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    (latest / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (latest / "summary.md").write_text(render_markdown(summary), encoding="utf-8")
    (latest / "POINTS_TO.txt").write_text(f"{stamp}\n", encoding="utf-8")

    summary["output_dir"] = str(out_dir.relative_to(root)).replace("\\", "/")
    exit_code = 1 if failed else 0
    return exit_code, summary


def main(argv: list[str] | None = None) -> int:
    """CLI 入口。

    Args:
        argv: 命令行参数。

    Returns:
        进程退出码。
    """
    parser = argparse.ArgumentParser(description="Run ScholarlyOps local evals")
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--json", action="store_true", help="Print summary JSON to stdout")
    args = parser.parse_args(argv)
    try:
        code, summary = run(args.root.resolve() if args.root else None)
    except EvalRunnerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        totals = summary["totals"]
        print(
            "ScholarlyOps run_evals — "
            f"total={totals['total']} executed={totals['executed']} "
            f"passed={totals['passed']} failed={totals['failed']} "
            f"skipped={totals['skipped']}"
        )
        for case in summary["cases"]:
            print(
                f"  [{case['status'].upper()}] {case['case_id']} "
                f"({case['mode']}) {case.get('reason', '')}"
            )
        print(f"Wrote: {summary.get('output_dir')} and evals/runs/latest/")
        print(
            "Note: skipped agent_semantic cases are not passes; "
            "semantic audit was not executed."
        )
    return code


if __name__ == "__main__":
    raise SystemExit(main())
