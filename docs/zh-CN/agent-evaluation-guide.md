# Agent 语义评测指南 · manuscript-audit

[English](../en/agent-evaluation-guide.md) | 简体中文

> **目的**：验证 Skill 在真实 Agent 工作流中的语义审计质量。  
> **原则**：不虚构实测结果；未执行 = skip（不得记 pass）；保持 **Draft**，有效测试不足时不得宣称 Stable。  
> **配套**：`evals/agent-semantic/`（盲测集、rubric、scorecard）

本指南与英文版内容一致。

---

## 1. 两类评测必须分开报告

| 类型 | 如何运行 | 当前状态（以本机最近执行为准） |
|------|----------|--------------------------------|
| 程序确定性 | `python tools/run_evals.py` | 本地脚本自动评分；语义案例自动 skip |
| Agent 语义 | 本指南的盲测流程 + 人工 scorecard | **仅在实际执行并评分后**计入 |

`tools/run_evals.py` 对 `agent_semantic` 一律 skip，这是设计。skip ≠ pass。

数值/单位检测器默认不在本阶段修改；仅当发现可复现缺陷时才改，并补回归测试。

---

## 2. 盲测集合（复用现有 24 案）

覆盖要求与案例映射见 `evals/agent-semantic/blind-set.json`。

**Wave A（语义核心，优先）**

| 案例 | 考察点 |
|------|--------|
| `02_correlation_to_causation` | 相关 → 因果 |
| `05_citation_metadata_error` | DOI/元数据未核实 |
| `06_citation_not_supporting` | 引文存在但不支持主张 |
| `07_missing_evidence` | 证据不足 / 缺方法 |
| `09_terminology_inconsistency` | 术语漂移 |
| `10_methods_results_contradiction` | 方法 vs 结果矛盾 |
| `17_insufficient_evidence_not_auto_error` | 缺证据 ≠ 自动 Critical |

**Wave B（可选双轨）**：干净对照、四舍五入/格式、合法组别/时间点/样本量、真实数值冲突候选等（见 `blind-set.json`）。用于检查 Agent 是否过度升级脚本候选。

不要为“凑数量”再复制相似合成稿。

---

## 3. 防答案泄漏

Agent 执行时**只能**获得：

1. 盲测包中的 `input.md`
2. 同目录 `TASK.md`（任务说明）
3. 已安装的 `manuscript-audit` Skill 指令（全局或项目技能目录）

**不得**预先读取：

- 该案例的 `expect.json`
- `evals/expected/manuscript-audit/<id>.md`
- `evals/agent-semantic/rubric.md` 中针对答案的核对段落（评分阶段再读）
- 已填写的 scorecard

若同一会话已打开过标准答案 → 该次结果**无效盲测**。

---

## 4. 准备隔离工作区

在**仓库外**（或明确隔离目录）生成盲测包：

```bash
# 推荐：输出到仓库外，避免 Agent 索引到 expect
python tools/prepare_agent_blind_pack.py --wave wave_a_semantic_core --out %USERPROFILE%\scholarlyops-blind\run1

# 或指定单个案例
python tools/prepare_agent_blind_pack.py --case 02_correlation_to_causation --out %USERPROFILE%\scholarlyops-blind\run1
```

脚本行为：

- 仅复制 `input.md`，并写入中立 `TASK.md`
- **拒绝**复制 `expect.json` / `expected/` / rubric
- 写出 `pack_manifest.json`（案例 ID 列表，不含期望答案）
- 默认在目标目录创建 `CASES/<case_id>/`

验证：每个案例目录下不得出现 `expect.json`。

---

## 5. 在 Cursor 中逐案例执行

对 **每一个** 案例重复：

### 5.1 打开隔离工作区

用 Cursor 打开盲测包根目录（或该案例子目录），**不要**同时打开含 `evals/expected` 的 ScholarlyOps 仓库窗口作为同一 Agent 上下文。

### 5.2 新开 Agent 会话

每个案例使用**全新** Agent 聊天。不要在同一会话串联多个案例并回看上一条的评分讨论。

### 5.3 调用 Skill

确认已安装 Skill（参见 [安装指南](installation.md) / [Cursor 验收](cursor-smoke-test.md)），然后发送例如：

```text
请严格按已安装的 manuscript-audit Skill 审计本目录中的 input.md。
若环境有 Python，先运行该 Skill 安装目录下 scripts/ 中的检查脚本，再做语义判断。
按 Skill 输出契约写出完整报告（Summary、Deterministic checks、Issues、Unrun checks、Limits）。
不要覆盖 input.md。不要把猜测标为已确认 Critical。不要读取仓库中的 expect 或标准答案。
```

也可使用 `/manuscript-audit`（若 IDE 支持）。

### 5.4 保存原始输出

将 Agent **未改写**的完整回复保存为：

`CASES/<case_id>/raw_agent_output.md`

可选：再存 `human_edited_report.md`，但评分以 `raw_agent_output.md` 为准。

### 5.5 记录版本元数据

在同目录填写 `run_meta.json`（可手写）：

```json
{
  "case_id": "02_correlation_to_causation",
  "date": "YYYY-MM-DD",
  "agent_name": "Cursor Agent",
  "agent_version": "",
  "model_name": "",
  "model_version": "",
  "skill_git_commit_or_path": "",
  "blind_workspace": ""
}
```

---

## 6. 独立评分步骤（可稍后、可换人）

1. 打开仓库中的 `expect.json` 与 `evals/expected/...md`（此时才允许看答案）。
2. 对照 `evals/agent-semantic/rubric.md`。
3. 复制 `evals/agent-semantic/scorecard-template.json` →  
   `evals/agent-semantic/results/<date>_<case_id>.json`（或仓库外评分目录）。
4. 填写检出/漏检/误报/严重程度/loci/`verified` 滥用等字段。
5. `status` 只能是 `pass` | `fail` | `partial` | `skip`。  
   会话污染或未跑 → `skip`。

**禁止**为了让汇总好看而改写原始 Agent 输出后再评分。

---

## 7. 评分维度（摘要）

对每条预期发现评价：

- 是否发现关键问题 / 是否漏检  
- 是否误报无问题内容  
- 严重程度是否在允许 band 内  
- 结论是否有证据；位置是否可在原文找到  
- 是否将未核实事项标为 `verified`  
- 是否将候选异常过度升级为 Critical  
- 建议是否符合研究材料  

详见 `evals/agent-semantic/rubric.md`。

---

## 8. 结果报告模板（汇总时使用）

```text
## 程序确定性测试
- 命令：python tools/run_evals.py
- 结果：…（executed / passed / failed / skipped）

## Agent 语义测试（盲测）
- 已准备案例：…
- 已实际执行：…
- 已人工评分：…
- 尚未执行：…
- 无效/无法判断：…

## 质量摘要（仅有效已评分案例）
- 关键问题召回：…
- 误报：…
- 严重程度合理性：…
- 证据定位质量：…

## 成熟度
- 仍为 Draft。有效样本量不足时不得宣称 Stable。
```

若无法从终端自动调用付费 Agent API：采用本指南的**人工驱动**流程即可，**不要伪造** Agent 输出。

---

## 9. 已知限制

- 合成案例 ≠ 真实投稿稿件。  
- 语义判断依赖模型与操作者；同一案例可复测但结果可能波动。  
- 本地程序通过不代表 Agent 语义可靠。  
- 本仓库不强制引入付费 API 自动化。
