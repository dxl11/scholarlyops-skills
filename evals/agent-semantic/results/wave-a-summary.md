# Wave A 汇总 · manuscript-audit Agent 语义评分

**评分日期**：2026-10-21  
**原始报告根目录**（证据未改写）：`[blind-pack]/CASES/`（本机 Temp `scholarlyops-blind-smoke`）  
**评分卡目录**：`evals/agent-semantic/results/2026-10-21_*.json`  
**成熟度结论**：仍为 **Draft**。n=7 且正式有效盲测 = 0，**不得**据此宣称 Stable 或普遍可靠性。

---

## 1. 执行与评分状态（必须区分）

| 类别 | 数量 | 说明 |
|------|------|------|
| 测试已执行（有 `raw_agent_output.md` + `run_meta.json`） | **7 / 7** | 02, 05, 06, 07, 09, 10, 17 |
| 已完成人工内容评分 | **7 / 7** | 本文件对应的 scorecard |
| 按 rubric §1 的**有效盲测** | **0 / 7** | 同一多轮会话先前编写过各案 `expect.json`；审计轮未重开答案，但会话污染 → `blind_valid=false` |
| 评分有争议（内容） | **0 硬争议**；**1 轻量备注** | 案例 09 严重程度 Minor vs 可能 Major（均在 band 内） |
| 仍未评分 | **0** | — |
| 计入 Stable 主张 | **0** | 全部 `counts_toward_stable_claim=false` |

程序确定性测试（`tools/run_evals.py`）与本 Wave **分开**，不在此混算 pass 率。

---

## 2. 内容质量指标（练习分；非有效盲测分）

对 `agent_expectations.must_find` 共 **9** 条预期发现：

| 指标 | 结果 |
|------|------|
| 有效内容评分案例数 | 7（全部完成） |
| 关键问题检出 | **9 / 9** 检出 |
| 关键问题漏检 | **0** |
| 不合理误报（must_not 严重违规 / 无依据 Critical） | **0** |
| 严重程度落在 expect band 或合理保守 | **9 / 9** |
| 证据位置可核验 | **7 / 7** 案例 |
| 不当使用 `verified`（未核实却标 verified） | **0** |
| 不当把缺证据当成已证实错误 | **0**（07、17 明确区分） |
| 内容 `status=pass` | **7 / 7** |

粗召回（内容）：9/9。样本量过小，不报过多小数，不作外推。

---

## 3. 分案例一览

| case_id | 内容 status | blind_valid | 漏检 | 误报 | 严重程度 | 证据状态要点 |
|---------|-------------|-------------|------|------|----------|--------------|
| 02 | pass | false | 0 | 0 | Critical/Major 均在 band | 因果 `verified`（允许）；疗效 `unsupported` |
| 05 | pass | false | 0 | 0 | Needs Review 在 band | `unverified`；未声称在线已核验；未把 DOI 当已证伪 |
| 06 | pass | false | 0 | 0 | Critical 在 band | `unsupported`/`conflicting`；未标治愈为真 |
| 07 | pass | false | 0 | 0 | Major + Needs Review | 缺口≠试验必不存在；有 Unrun |
| 09 | pass | false | 0 | 0 | Minor 在 band（可接受 Major） | 区分 response/objective/remission；未造数值冲突 |
| 10 | pass | false | 0 | 0 | Critical 在 band | Methods 排除 KO vs Results 报告 KO：`conflicting` |
| 17 | pass | false | 0 | 0 | Needs Review | 缺表/计数 → unverified；未虚构 Critical |

---

## 4. 独立核查要点（对照评分指令）

### 02
原始 ISSUE-001/002 覆盖相关→因果与临床疗效过度主张；保留 r=0.42；有 Results/Discussion 位点。内容通过。

### 05
明确「未做 registry/online lookup」→ `unverified` / Needs Review；**未**把 DOI 直接判为无效造假。符合「未核验 ≠ 已证伪」。

### 06
指出人类转移瘤治愈主张超出细胞实验摘录；有双边引文；**未**进一步声称该主张在现实中已被证明为假。

### 07
识别 RCT 声称与 Methods 缺失；写明 Missing Methods ≠ proof design never occurred；列出 Unrun。

### 09
准确列出 overall response / objective response / overall remission；数值同为 50%。Minor 落在 band；评分人未自动背书——认为 remission 可能抬到 Major，但无终点定义时 Minor/Major 均可接受。**轻量备注，非 fail。**

### 10
Methods「knockout excluded」与 Results「Knockout mice showed…」确为研究对象/范围冲突；Critical + conflicting 恰当。

### 17
报告缺主终点表与原始计数及因此无法核验；拒绝把缺失解释为结果虚假。

---

## 5. 模板兼容说明

`scorecard-template.json` 保留全部原字段。本轮以兼容方式**追加**评分指令要求的字段：`run_meta`、`expected_findings`、`observed_findings`、`missed_findings`、`false_positive_findings`、`severity_assessment`、`evidence_traceability`、`evidence_state_calibration`、`instruction_adherence`、`reviewer_notes`、`overall_status`。  
**建议**（见下节）：下一轮将上述字段升为模板正式字段，并增加 `blind_valid` 与 `counts_toward_stable_claim` 的文档化说明。

原始 `raw_agent_output.md` / `run_meta.json` **未修改**。

---

## 6. 建议修复项（本阶段只记录，不改被测对象）

1. **盲测执行流程**：强制「新 Cursor 窗口 / 新 Agent 会话 / 仓库外工作区」，且评分会话与审计会话分离；在 `run_meta` 增加 `blind_session_id` 与「本会话是否曾打开 expect」自检项，避免再次出现会话污染导致 0 有效盲测。  
2. **案例 09 预期微调（可选）**：在 `scoring_notes` 中写明——出现 *remission* 且无终点定义时，优先接受 `Needs Review` 或 `Major`，`Minor` 仅在 Agent 明确论证「可能仅为用词滑移」时可用（仍保留 band，避免唯一标签）。  
3. **Skill / 文档（非本轮修改）**：在 Agent 评测指南中强调 Methods–Results **逻辑矛盾**（如案例 10）不依赖数值脚本；可考虑在未来增加「语义逻辑检查清单」示例，仍保持脚本不输出 Critical。

其他观察（非立即修复）：单位脚本在 Windows 默认 GBK 控制台下 `--json` 曾需 `PYTHONIOENCODING=utf-8`（运行元数据已反映）；属工具链体验，非本轮 Wave A 语义失败。

---

## 7. 生成的评分文件清单

- `evals/agent-semantic/results/2026-10-21_02_correlation_to_causation.json`
- `evals/agent-semantic/results/2026-10-21_05_citation_metadata_error.json`
- `evals/agent-semantic/results/2026-10-21_06_citation_not_supporting.json`
- `evals/agent-semantic/results/2026-10-21_07_missing_evidence.json`
- `evals/agent-semantic/results/2026-10-21_09_terminology_inconsistency.json`
- `evals/agent-semantic/results/2026-10-21_10_methods_results_contradiction.json`
- `evals/agent-semantic/results/2026-10-21_17_insufficient_evidence_not_auto_error.json`
- `evals/agent-semantic/results/wave-a-summary.md`（本文件）

---

## 8. 一句话结论

Wave A **7 案均已执行并完成内容评分**，内容侧关键问题 **0 漏检 / 0 严重误报**，但因 **会话污染，有效盲测为 0**，**不能**支持升成熟度；优先按第 6 节做下一轮真盲测。
