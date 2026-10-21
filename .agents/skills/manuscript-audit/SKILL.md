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

## 数值 / 单位脚本（启发式候选检测）

脚本是**候选异常检测器**，不是完整科研事实验证系统。

`scripts/check_numeric_consistency.py`：

1. 保留每次命中的原始数值、行号、上下文片段与标签。
2. **格式差异**（7.1 vs 7.10）与**容差内差异** → tolerated，不报候选错误。
3. 明显跨范围（如 treatment vs control、week 4 vs week 12）→ `cross_scope_difference`（tolerated），不自动当冲突。
4. 同标签、超容差且范围提示不足 → `candidate_inconsistency`，默认 **Needs Review** + `partially_supported`，带 loci；**不得**由脚本标为 Critical / `verified`。
5. 脚本的 `error_findings` 恒为空；是否升级为 Critical 只能由 Agent/作者在充分证据后决定。

`scripts/check_unit_tokens.py`：

1. 保留数值、单位、行号、上下文；规范化 μ / µ / u 等微符号别名。
2. 别名-only → tolerated；不同量纲类别混用 → Needs Review 候选（不做缺信息换算）。
3. 不同实验/物质合法使用不同单位时，脚本无法可靠区分，只能给候选并声明限制。

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
   - 在**本 Skill 安装目录**下运行（全局安装或项目级安装后的目录，不要依赖 ScholarlyOps 开发仓库路径）：
     - `python scripts/check_numeric_consistency.py --input <file>`
     - `python scripts/check_unit_tokens.py --input <file>`
   - 需要 Python 3.10+；若不可用，将脚本检查记入 Unrun，仍可继续语义审计。
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

- 程序检查仅为启发式**候选**检测：不能证明同一估计量/同一物质，也不能替代作者判断。
- **不**做缺信息的单位换算、完整统计复核或自动文献 API 核验；脚本不输出 Critical/`verified` 科学错误结论。
- 语义审计依赖 Agent/人工；本地 `tools/run_evals.py` 对 `agent_semantic` 案例一律 skip，**不得**记为通过。
- Draft：不得称为 Stable。
- 本地评测：`python tools/run_evals.py`（详见 `evals/README.md`）。
