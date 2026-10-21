#!/usr/bin/env python3
"""Prepare an isolated blind-test pack for manuscript-audit Agent evaluation.

Copies only case inputs and a neutral TASK.md. Never copies expect.json,
expected answers, or rubric files into the Agent workspace.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class BlindPackError(Exception):
    """统一盲测包准备异常。"""


FORBIDDEN_NAMES = frozenset(
    {
        "expect.json",
        "case.yaml",
        "rubric.md",
        "scorecard-template.json",
    }
)

TASK_TEMPLATE = """# Blind audit task (no gold answers in this folder)

You are evaluating a **synthetic** manuscript excerpt for consistency and evidence risk.

## Allowed materials

- `input.md` in this folder
- The installed `manuscript-audit` Skill instructions (global or project Skill path)
- Optional: run Skill `scripts/check_numeric_consistency.py` and `scripts/check_unit_tokens.py` if Python is available

## Forbidden

- Do **not** open or search for `expect.json`, `evals/expected/`, scorecards, or answer keys
- Do **not** overwrite `input.md`
- Do **not** invent experiments, numbers, or citations that are not in the input
- Do **not** mark guesses as confirmed Critical / verified scientific errors

## Required output

Follow the `manuscript-audit` output contract:

1. Summary
2. Deterministic checks
3. Issues (severity, location, evidence, evidence state, suggested fix, author confirmation)
4. Unrun checks
5. Limits

Save your **unedited** report so a separate human scorer can compare it to held-out expectations later.
"""


def repo_root() -> Path:
    """返回仓库根目录。

    Returns:
        仓库根 Path。
    """
    return Path(__file__).resolve().parents[1]


def load_blind_set(path: Path) -> dict[str, Any]:
    """加载盲测集定义。

    Args:
        path: blind-set.json 路径。

    Returns:
        解析后的字典。

    Raises:
        BlindPackError: 读取或解析失败。
    """
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BlindPackError(f"blind_set_error:{path}:{exc}") from exc


def resolve_case_ids(
    blind_set: dict[str, Any],
    wave: str | None,
    case: str | None,
    all_cases: bool,
) -> list[str]:
    """解析待导出的案例 ID 列表。

    Args:
        blind_set: 盲测集定义。
        wave: wave 名称（如 wave_a_semantic_core）。
        case: 单个案例 ID。
        all_cases: 是否导出清单中全部 wave 案例（去重）。

    Returns:
        案例 ID 列表。

    Raises:
        BlindPackError: 参数无效。
    """
    if sum(bool(x) for x in (wave, case, all_cases)) != 1:
        raise BlindPackError("specify_exactly_one_of:--wave|--case|--all-waves")

    waves = blind_set.get("waves") or {}
    if case:
        return [case]
    if wave:
        if wave not in waves:
            raise BlindPackError(f"unknown_wave:{wave}:known={sorted(waves)}")
        ids = list(waves[wave].get("case_ids") or [])
        if not ids:
            raise BlindPackError(f"empty_wave:{wave}")
        return ids
    # all waves
    seen: list[str] = []
    for spec in waves.values():
        for cid in spec.get("case_ids") or []:
            if cid not in seen:
                seen.append(cid)
    if not seen:
        raise BlindPackError("no_cases_in_waves")
    return seen


def assert_safe_output_tree(out_root: Path) -> None:
    """确保输出目录不混入答案文件名约定。

    Args:
        out_root: 输出根目录。

    Raises:
        BlindPackError: 发现禁止文件。
    """
    if not out_root.exists():
        return
    for path in out_root.rglob("*"):
        if path.is_file() and path.name in FORBIDDEN_NAMES:
            raise BlindPackError(f"forbidden_file_already_present:{path}")


def prepare_case(case_id: str, cases_root: Path, dest_root: Path) -> Path:
    """将单个案例的 input 复制到盲测目录。

    Args:
        case_id: 案例 ID。
        cases_root: evals/cases/manuscript-audit。
        dest_root: 盲测包 CASES 根。

    Returns:
        案例目标目录。

    Raises:
        BlindPackError: 输入缺失或复制失败。
    """
    src = cases_root / case_id
    input_path = src / "input.md"
    if not input_path.is_file():
        raise BlindPackError(f"missing_input:{case_id}")

    dest = dest_root / case_id
    try:
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(input_path, dest / "input.md")
        (dest / "TASK.md").write_text(TASK_TEMPLATE, encoding="utf-8")
        # Guard: never copy expect even if present nearby
        for name in FORBIDDEN_NAMES:
            leaked = dest / name
            if leaked.exists():
                leaked.unlink()
                raise BlindPackError(f"refused_leak:{leaked}")
    except BlindPackError:
        raise
    except OSError as exc:
        raise BlindPackError(f"copy_failed:{case_id}:{exc}") from exc
    return dest


def build_pack(
    *,
    out: Path,
    case_ids: list[str],
    wave: str | None,
    repo: Path,
) -> dict[str, Any]:
    """构建完整盲测包。

    Args:
        out: 输出根目录。
        case_ids: 案例列表。
        wave: 选用的 wave 名（可空）。
        repo: 仓库根。

    Returns:
        manifest 字典。

    Raises:
        BlindPackError: 准备失败。
    """
    cases_root = repo / "evals" / "cases" / "manuscript-audit"
    if not cases_root.is_dir():
        raise BlindPackError(f"missing_cases_root:{cases_root}")

    out = out.resolve()
    try:
        out.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise BlindPackError(f"mkdir_failed:{out}:{exc}") from exc

    assert_safe_output_tree(out)
    cases_dest = out / "CASES"
    prepared: list[str] = []
    for case_id in case_ids:
        prepare_case(case_id, cases_root, cases_dest)
        prepared.append(case_id)

    # Final leak scan
    for path in out.rglob("*"):
        if path.is_file() and path.name in FORBIDDEN_NAMES:
            raise BlindPackError(f"leak_detected:{path}")
        if path.is_file() and path.name.endswith(".md"):
            # expected answer files must not appear
            if "expected" in path.parts:
                raise BlindPackError(f"expected_tree_leak:{path}")

    manifest: dict[str, Any] = {
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "skill": "manuscript-audit",
        "wave": wave,
        "case_ids": prepared,
        "contains_expect_or_answers": False,
        "instructions": (
            "Open each CASES/<id> in a fresh Agent session. "
            "Score later against the repo expect files—not inside this pack."
        ),
        "scoring_docs_in_repo": [
            "evals/agent-semantic/rubric.md",
            "evals/agent-semantic/scorecard-template.json",
            "docs/zh-CN/agent-evaluation-guide.md",
            "docs/en/agent-evaluation-guide.md",
        ],
    }
    try:
        (out / "pack_manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (out / "README_BLIND.md").write_text(
            "# Blind pack\n\n"
            "This directory is intentionally free of gold answers.\n"
            "Run one fresh Agent session per `CASES/<case_id>`.\n"
            "Score afterward using the ScholarlyOps repo scorecard—not here.\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise BlindPackError(f"manifest_write_failed:{exc}") from exc
    return manifest


def main(argv: list[str] | None = None) -> int:
    """CLI 入口。

    Args:
        argv: 可选参数列表。

    Returns:
        进程退出码；失败非零。
    """
    parser = argparse.ArgumentParser(
        description="Prepare answer-free blind packs for Agent semantic evals."
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output directory (prefer a path outside this git repo).",
    )
    parser.add_argument(
        "--wave",
        default=None,
        help="Wave name from evals/agent-semantic/blind-set.json",
    )
    parser.add_argument("--case", default=None, help="Single case id")
    parser.add_argument(
        "--all-waves",
        action="store_true",
        help="Union of all waves in blind-set.json",
    )
    parser.add_argument(
        "--blind-set",
        default=None,
        help="Optional path to blind-set.json",
    )
    args = parser.parse_args(argv)

    repo = repo_root()
    blind_path = (
        Path(args.blind_set)
        if args.blind_set
        else repo / "evals" / "agent-semantic" / "blind-set.json"
    )

    try:
        blind_set = load_blind_set(blind_path)
        case_ids = resolve_case_ids(
            blind_set, args.wave, args.case, args.all_waves
        )
        out = Path(args.out)
        # Soft warning if writing inside the repo (still allowed for CI tests)
        try:
            out.resolve().relative_to(repo.resolve())
            print(
                "WARNING: output is inside the git repo; "
                "prefer an external directory for real blind runs.",
                file=sys.stderr,
            )
        except ValueError:
            pass

        manifest = build_pack(
            out=out, case_ids=case_ids, wave=args.wave, repo=repo
        )
    except BlindPackError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        f"Blind pack ready: cases={len(manifest['case_ids'])} "
        f"out={Path(args.out).resolve()}"
    )
    for cid in manifest["case_ids"]:
        print(f"  - {cid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
