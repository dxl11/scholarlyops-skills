# 评测说明 · ScholarlyOps

本目录存放**合成**或已确认可公开的评测材料。禁止提交未经授权的完整论文、私有数据或个人信息。

## 布局

```text
evals/
├── README.md
├── cases/manuscript-audit/<case_id>/
├── cases/literature-search/<case_id>/   # 全部 agent_semantic（本地 skip）
├── expected/manuscript-audit/<case_id>.md
├── expected/literature-search/<case_id>.md
├── agent-semantic/    # manuscript-audit Agent 盲测协议
├── results/
└── runs/              # tools/run_evals.py（当前仅 manuscript-audit）
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

## 案例清单（literature-search）

全部为 `agent_semantic`：本地 `run_evals.py` **不**执行这些案例；结构由 `tests/test_validate_skills.py` 检查存在性。人工/Agent 评分前不得记为 pass。

| ID | 场景 |
|----|------|
| 01_fuzzy_topic_needs_structure | 模糊主题需结构化 |
| 02_pico_intervention | 医学干预 / PICO |
| 03_qualitative_not_forced_pico | 定性研究不强制 PICO |
| 04_english_synonym_matrix | 英文同义词矩阵 |
| 05_pubmed_scopus_syntax_not_mixed | PubMed/Scopus 语法不得混用 |
| 06_too_few_results_expand | 结果太少需扩展 |
| 07_too_many_results_precision | 结果太多需提高精度 |
| 08_systematic_review_logging | 系统综述检索记录 |
| 09_no_db_no_fake_hits | 无库连接不得虚构命中 |
| 10_seed_papers_expand | 由种子论文扩展关键词 |

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
| 18_treatment_control_ok | 治疗组 vs 对照组（合法差异） | deterministic |
| 19_baseline_vs_analyzed_n_ok | 入组 vs 分析集 n | deterministic |
| 20_timepoints_ok | 不同时间点 | deterministic |
| 21_condition_units_mixed_candidate_not_error | 不同条件单位混用（候选≠错误） | deterministic |
| 22_micro_symbol_alias_ok | μ/µ/u 别名 | deterministic |
| 23_true_numeric_conflict_candidate | 同口径数值冲突候选 | deterministic |
| 24_ambiguous_context_candidate | 缺上下文候选 | deterministic |

## 脚本输出约定（重要）

数值/单位脚本输出的是 **candidates（Needs Review）**，不是已证实 Critical 错误：

- `max_error_findings`（默认 0）：禁止脚本级 `error_findings`
- `require_loci`：候选必须含行号与上下文
- 容差/跨范围/别名走 `tolerated`，不得计为候选冲突

## 误报 / 漏检判定

- **漏检**：`must_find_labels` / 单位族未出现 → fail  
- **误报**：干净/合法差异案例出现候选超限，或出现 `error_findings` / Critical → fail  
- **语义**：仅人工/Agent；未执行不得写 pass

## Agent 语义盲测（与本地运行器分开）

本地 `run_evals.py` **不会**执行 Agent。语义质量评估见：

- [中文指南](../docs/zh-CN/agent-evaluation-guide.md)
- [English guide](../docs/en/agent-evaluation-guide.md)
- `evals/agent-semantic/rubric.md`、`scorecard-template.json`、`blind-set.json`

准备隔离输入（不含答案）：

```bash
python tools/prepare_agent_blind_pack.py --wave wave_a_semantic_core --out %USERPROFILE%\scholarlyops-blind\run1
```

评分必须以未经改写的 `raw_agent_output.md` 为准；会话中若已打开 expect，则该次不得记为有效盲测。  
**当前仓库未提交任何虚构的 Agent 实测分数**；`agent-semantic/results/` 在真实评分前为空。

在有限测试集上通过 ≠ 现实错误率为零；Agent 有效样本量不足时不得宣称 Stable。
