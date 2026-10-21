---
name: research-context
description: >-
  Organize research goals, hypotheses, design, variables, data, results, author
  interpretations, limits, and references into a structured research record.
  Use when the user needs to consolidate messy notes into auditable context;
  do not invent missing experiments or mark guesses as verified facts.
---

# research-context · 研究上下文整理

**成熟度**：Draft（流程已定义；合成评测尚未充分）  
**品牌**：ScholarlyOps（元数据见安装本 Skill 的仓库 `project.json`，若仅复制本目录则以本文件为准）

## 何时使用

用户提供杂乱的研究目标、实验设计、变量、数据摘要、结果、限制或文献列表，需要结构化研究记录时。

## 输入

- 研究笔记、实验日志摘要、已有段落、表格数值、文献条目（用户粘贴或附件说明）
- 可选：目标章节或下游用途（写作 / 审计 / 审稿）

## 工作流程

1. **清点材料**：列出已收到的文件/段落与明显缺失项。
2. **分层标注**（强制）：
   - 已知事实（用户明确给出的数据/设计）
   - 作者解释
   - 合理推论（须标明推论）
   - 缺失信息
   - 待核实内容
3. **填充结构**（见下方输出模板）；空字段写 `MISSING`，不得臆造。
4. **证据状态**：对每条关键主张标注 `verified` / `partially_supported` / `unverified` / `unsupported` / `conflicting`（含义见 `references/integrity.md`）。
5. **输出新文件建议名**：`research_context_record.md`（默认不覆盖用户原稿）。

## 输出模板

```markdown
# Research Context Record

## Meta
- Generated_for: ScholarlyOps / research-context
- Maturity: Draft
- Limits: ...

## 1. Research goal
## 2. Hypotheses
## 3. Subjects / samples
## 4. Design
## 5. Variables & glossary
## 6. Conditions
## 7. Data & results (facts only)
## 8. Author interpretation
## 9. Limitations
## 10. Related literature (as provided)
## 11. Open questions / unverified
## 12. Missing information checklist
```

## 异常处理

| 情况 | 行为 |
|------|------|
| 结果数字未提供 | 字段 `MISSING`；禁止补全 |
| 事实与解释混写 | 拆分并标注 |
| 相互矛盾 | `conflicting` + 双方原文位置 |
| 用户要求编造数据 | 拒绝该部分并说明完整性约束 |

## 限制

- Draft：未保证覆盖所有学科模板。
- 不访问未提供的数据库或文献全文时，相关项保持 `unverified`。
- 独立安装时仅依赖本目录内文件。

## 参考

- [references/integrity.md](references/integrity.md)
- [examples/minimal_record.md](examples/minimal_record.md)
