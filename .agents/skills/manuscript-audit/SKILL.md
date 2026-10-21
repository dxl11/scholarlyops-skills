---
name: manuscript-audit
description: >-
  Audit consistency and evidence risks across abstract, body, figure/table
  captions, supplements, and conclusions. Prefer programmatic checks for
  determinate numeric/unit mismatches; for semantic issues provide loci and
  review rationale. Use before submission or after major rewrites; never
  overwrite the original manuscript by default.
---

# manuscript-audit · 论文一致性审计

**成熟度**：Draft（示范实现：流程 + 脚本 + 合成评测；真实稿件验证待完成）  
**输出默认**：新报告文件，例如 `manuscript_audit_report.md`

## 严重程度定义

| 级别 | 含义 |
|------|------|
| Critical | 可能改变科学解读的**已确认**冲突（如关键数值互斥且超出容差、无依据的因果坐实） |
| Major | 重要不一致或证据缺口，影响可信度，需优先修复 |
| Minor | 术语不统一、次要表述问题等，不立即颠覆结论 |
| Needs Review | 语义可疑或证据不足，**不能**当作已确认错误 |

没有来源支持的猜测 → 最多 `Needs Review`，不得写成已确认 Critical/Major。  
**无法核查 ≠ 错误**；**未发现错误 ≠ 证明不存在错误**。

## 证据状态（必须一致使用）

| 状态 | 含义 |
|------|------|
| `verified` | 当前材料足以支持该判断（例如脚本确认的字面数值冲突） |
| `partially_supported` | 仅部分内容有支持 |
| `unverified` | 尚未完成核查 |
| `unsupported` | 现有证据不支持该主张 |
| `conflicting` | 证据互相冲突 |

## 数值差异分层（程序检查）

脚本 `scripts/check_numeric_consistency.py` 区分：

1. **字面冲突**（超出容差）→ 可报 Critical / `verified`
2. **格式差异**（7.1 vs 7.10）→ **不**记为错误
3. **四舍五入容差内**（默认 abs_tol≈0.051）→ **不**记为错误，写入 tolerated
4. **单位问题** → 由 `check_unit_tokens.py` 处理（不做单位换算）
5. **语义不一致**（相关→因果等）→ 仅模型/人工，不得伪称为脚本已验证

每个重要问题尽量包含：问题标识、严重程度、原文位置、证据、判断理由、建议处理、是否需作者确认、证据状态。

## 何时使用

用户需要检查摘要、正文、图注、表格、补充材料与结论之间的一致性与证据风险时。

## 输入

- 稿件文本（全文或相关节选）；**建议使用副本**
- 图注 / 表注
- 可选：参考文献列表、补充材料说明
- 可选：运行程序检查的文本文件路径

## 工作流程

1. **材料清单**：记录收到什么、缺什么；不可读附件标为未执行检查。
2. **程序优先**（可确定差异）：
   - 在本 Skill 目录下运行：
     - `python scripts/check_numeric_consistency.py --input <file>`
     - `python scripts/check_unit_tokens.py --input <file>`
   - 将脚本 JSON/文本输出纳入报告的“Deterministic checks”节。
3. **语义审计**（模型）：相关→因果、摘要 vs 正文、图注 vs 正文、方法 vs 结果、术语漂移、结论过度扩张、引用元数据异常、引文不支持主张。
4. **引用分层**：存在性 / 元数据 / 内容支持 / 论证恰当性分开写；无法访问全文时声明限制。
5. **分级输出**：每条问题含严重程度、原文位置、证据、建议修正、是否需作者确认、证据状态。
6. **未执行检查**：明确列出原因（缺材料、无网络、格式不可解析等）。

## 输出契约

```markdown
# Manuscript Audit Report

## Summary
- Skill: manuscript-audit (Draft)
- Deterministic findings: N
- Semantic findings: N
- Needs author confirmation: N

## Deterministic checks
...

## Issues
### ISSUE-001
- Severity: Critical | Major | Minor | Needs Review
- Location: ...
- Evidence: ...
- Evidence state: ...
- Suggested fix: ...
- Author confirmation: yes/no

## Unrun checks
- ...

## Limits
- ...
```

## 异常处理

| 情况 | 行为 |
|------|------|
| 缺图注 | 跳过图注相关检查并记入 Unrun |
| 脚本失败 | 报告错误类型；不伪造通过 |
| 用户要“直接改对并覆盖原稿” | 可给修订建议文件；默认不覆盖 |
| 要求把猜测标成已确认错误 | 拒绝；改用 Needs Review |

## 与其他 Skill

可选输入来自 `research-context`；审计后可衔接 `review-response`。均可独立运行。

## 参考与示例

- [references/integrity.md](references/integrity.md)
- [references/severity.md](references/severity.md)
- [references/report_template.md](references/report_template.md)
- [examples/tiny_manuscript.md](examples/tiny_manuscript.md)

## 限制

- 程序检查覆盖面有限（启发式数值/单位），不是完整科学证明。
- **不**做单位换算、完整统计复核或自动文献 API 核验。
- 语义审计依赖 Agent/人工；本地 `tools/run_evals.py` 对 `agent_semantic` 案例一律 skip，**不得**记为通过。
- Draft：不得称为 Stable。
- 本地评测：`python tools/run_evals.py`（详见 `evals/README.md`）。
