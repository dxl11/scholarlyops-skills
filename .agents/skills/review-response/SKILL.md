---
name: review-response
description: >-
  Split reviewer comments into discrete issues and link each to manuscript
  loci, proposed or completed edits, supporting evidence, reply drafts, and
  status. Use when preparing a response-to-reviewers letter; never claim
  unfinished experiments or edits are done, and never invent page/line numbers.
---

# review-response · 审稿意见回复

**成熟度**：Draft

## 何时使用

用户提供审稿意见（及可选修订稿/审计报告），需要拆分问题并生成可追踪的回复草稿时。

## 输入

- 审稿意见原文（按审稿人分列更佳）
- 可选：当前稿件、修改说明、`manuscript-audit` 报告、研究上下文
- 作者已决定的处理策略（若有）

## 工作流程

1. **拆分**：每条可独立处理的意见一个 ID（如 R1-Q3）。
2. **分类**：方法 / 结果 / 讨论 / 写作 / 文献 / 其他。
3. **映射**：意见原文 → 拟处理方式 → 稿件位置 → 修改前/后 → 证据 → 回复草稿 → 状态。
4. **状态枚举**（强制诚实）：
   - `not_started` | `in_progress` | `done` | `wont_fix_with_rationale` | `needs_author_decision`
5. **禁止**：伪造实验、页码、行号、文献、已完成修改或作者未做决定。
6. **输出**建议文件：`review_response_tracker.md` + 可选 `response_letter_draft.md`；不覆盖原稿。

## 输出模板

```markdown
# Review Response Tracker

## Meta
- Skill: review-response (Draft)
- Limits: ...

## Items
### R1-Q1
- Reviewer text:
- Category:
- Planned action:
- Manuscript locus:
- Before:
- After:
- Evidence:
- Evidence state:
- Reply draft:
- Status: needs_author_decision
- Author decision needed:
```

## 异常处理

| 情况 | 行为 |
|------|------|
| 意见含糊 | 标 `needs_author_decision` 并列出澄清问题 |
| 要求新实验但未做 | 状态不得为 `done`；回复中如实说明计划或局限 |
| 缺少页码 | 用章节标题定位；不编造行号 |
| 与审计报告冲突 | 并列两边证据，标 `conflicting` 或待确认 |

## 限制

- Draft：无期刊门户自动提交。
- 独立安装仅依赖本目录；见 `references/integrity.md`。

## 参考

- [references/integrity.md](references/integrity.md)
- [examples/tracker_snippet.md](examples/tracker_snippet.md)
