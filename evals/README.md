# 评测说明 · ScholarlyOps

本目录存放**合成**或已确认可公开的评测材料。禁止提交未经授权的完整论文、私有数据或个人信息。

## 布局

```text
evals/
├── README.md
├── cases/manuscript-audit/<case_id>/
│   ├── input.md       # 合成输入
│   ├── case.yaml      # 元数据（含 mode）
│   └── expect.json    # 机器可读期望（本地运行器用）
├── expected/manuscript-audit/<case_id>.md  # 人工可读期望
├── results/           # 可选：抽查脚本输出样例（勿放私有全文）
└── runs/              # 运行器输出（默认 gitignore；含 latest/）
```

## 案例 mode

| mode | 含义 | 本地运行器行为 |
|------|------|----------------|
| `deterministic` | 可用脚本判定 | 执行并与 `expect.json` 比较；失败 → 非零退出码 |
| `agent_semantic` | 需 Agent/人工 | **skip**，写明原因；**绝不**记为 pass |

## 本地运行（可重复）

```bash
python tools/run_evals.py
python tools/run_evals.py --json
```

输出写入 `evals/runs/<UTC时间戳>/summary.{json,md}`，并更新 `evals/runs/latest/`（不修改 cases/expected）。

汇总字段：案例总数、已执行、通过、失败、跳过及原因、失败明细、已知限制。

## 案例清单（manuscript-audit）

| ID | 场景 | mode |
|----|------|------|
| 01_numeric_unit_mismatch | 数值 + 单位冲突 | deterministic |
| 02_correlation_to_causation | 相关→因果 | agent_semantic |
| 03_abstract_body_mismatch | 摘要 vs 正文 ORR | deterministic |
| 04_caption_body_conflict | 图注 vs 正文 | deterministic |
| 05_citation_metadata_error | DOI/元数据异常 | agent_semantic |
| 06_citation_not_supporting | 引文不支持主张 | agent_semantic |
| 07_missing_evidence | 缺少必要方法证据 | agent_semantic |
| 08_unsupported_issue_in_report | 不得无依据乱报 Critical | deterministic |
| 09_terminology_inconsistency | 术语不一致 | agent_semantic |
| 10_methods_results_contradiction | 方法 vs 结果 | agent_semantic |
| 11_clean_control | 无实质问题对照 | deterministic |
| 12_rounding_tolerance | 四舍五入不应判错 | deterministic |
| 13_same_value_incompatible_units | 同值不兼容单位 | deterministic |
| 14_table_figure_body_conflict | 表/图/正文冲突 | deterministic |
| 15_abstract_results_conclusion_conflict | 摘要/结果/结论冲突 | deterministic |
| 16_format_only_not_error | 格式差异非错误 | deterministic |
| 17_insufficient_evidence_not_auto_error | 证据不足≠自动错误 | agent_semantic |

## 误报 / 漏检判定

- **漏检**：`expect.json` 要求的 `must_find_labels` / 单位族未出现 → fail  
- **误报**：`max_findings` 超限，或对照/容差案例出现错误级 finding → fail  
- **语义**：仅人工/Agent；未执行不得写 pass

在有限测试集上通过 ≠ 现实错误率为零。
