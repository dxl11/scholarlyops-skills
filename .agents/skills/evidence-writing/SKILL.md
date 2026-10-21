---
name: evidence-writing
description: >-
  Draft or rewrite manuscript paragraphs under evidence constraints from the
  user-provided research context, data, and verifiable citations. Use when the
  user needs claim-linked academic prose; refuse to invent data, citations, or
  stronger conclusions than the evidence allows.
---

# evidence-writing · 证据约束写作

**成熟度**：Draft  
**原则**：事实保真 > 文采

## 何时使用

用户已有（或刚整理的）研究上下文、数据要点或可核验文献，需要起草/改写摘要、引言、结果或讨论段落时。

## 输入

- 研究上下文（推荐先由 `research-context` 产出）
- 目标章节与篇幅
- 可用证据：数值、图表说明、文献条目（用户提供）
- 可选：领域惯例或期刊语气要求（不得压过事实保真）

## 工作流程

1. **核对可用证据清单**；列出缺口。
2. **起草时绑定主张**：每条重要主张标注证据来源位置或 `unverified`。
3. **区分**：事实 / 推论 / 假设 / 未核实；禁止把假设写成已证实。
4. **禁止夸大**：相关≠因果；趋势≠显著；“提示”≠“证明”。
5. **改写模式**：给出原文、修订文、修改理由、是否可能改变原意、待确认项。
6. **输出**到新文件建议名：`evidence_draft.md` 或差异报告；默认不覆盖原稿。

## 输出契约

```markdown
# Evidence-Constrained Draft

## Claims map
| Claim | Evidence locus | Evidence state |
|-------|----------------|----------------|

## Draft text
...

## Author confirmations required
- ...

## Limits
- Sources not accessed: ...
```

## 异常处理

| 情况 | 行为 |
|------|------|
| 证据不足仍要求强硬结论 | 弱化措辞或拒绝该句；列出所需证据 |
| 用户要求虚构文献 | 拒绝 |
| 改写可能改变科学含义 | 保留原意选项 + 风险说明 |

## 限制

- Draft：无自动文献 API；无法访问全文时内容支持层保持 `unverified`。
- 不保证符合特定期刊排版细则。

## 参考

- [references/integrity.md](references/integrity.md)
- [examples/claim_map_snippet.md](examples/claim_map_snippet.md)
