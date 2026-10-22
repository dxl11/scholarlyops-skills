# Cursor 人工验收指南 · manuscript-audit

[English](../en/cursor-smoke-test.md) | 简体中文

> **状态**：须在 Cursor IDE 中勾选。终端安装成功 ≠ IDE 已加载。  
> 参考：[Cursor Agent Skills](https://cursor.com/docs/skills) · [安装指南](installation.md)

**优先验证全局安装**（最终用户主路径）。仅在专门测试项目级兼容时，才把 Skill 装进某个测试项目。

本仓库权威源码仍在 `.agents/skills/`（单一来源）。全局安装由 `npx skills` 复制/链接到用户技能目录，不要在仓库里维护第二套 SKILL.md。

## 0. 前置（推荐：全局安装）

首选：在 Cursor Agent 粘贴 [安装指南](installation.md) 第 1 节的「让 Agent 帮你安装」指令。

备用 CLI：

```bash
npx skills add dxl11/scholarlyops-skills --global --agent cursor --skill manuscript-audit
# 可选：-y --copy（非交互 + 复制落盘；维护环境曾用此组合验证）
npx skills list --global --agent cursor
```

确认 `list` 输出中的 `path`（本维护环境曾落到 `%USERPROFILE%\.agents\skills\manuscript-audit`）。

可选仓库内脚本评测（与全局加载无关）：

```bash
python tools/run_evals.py
```

Agent 语义盲测（与程序评测分开；勿在同会话预读 expect）：见 [Agent 语义评测指南](agent-evaluation-guide.md)。

## 1. 确认 Cursor 是否发现全局 Skill

1. 打开**任意非本仓库**的工作项目（验证跨项目复用）。
2. Agent 输入 `/`，搜索 `manuscript-audit`。
3. 或查看 Settings 中 Skills 相关列表。

**通过**：能看到并选用 `manuscript-audit`。  
**失败**：见第 9 节。

## 2. 手动调用

```text
请严格按已安装的 manuscript-audit Skill 审计以下合成稿件。
若环境有 Python，先运行该 Skill 安装目录下 scripts/ 中的检查脚本，再做语义判断。
输出须含 Summary、Deterministic checks、Issues、Unrun checks、Limits。
不得覆盖输入文件；不得把猜测标为 Critical。
```

也可尝试 `/manuscript-audit`。

## 3. 验证读取了正确的 SKILL.md

```text
请给出你遵循的 Skill 文件的完整路径，并摘录严重程度表中 Critical 与 Needs Review 两行原文。
```

**通过**：路径落在用户全局技能目录（或你选择的项目级目录），内容与官方 `SKILL.md` 一致。

## 4–5. 合成案例

- 数值冲突：可粘贴仓库 `evals/cases/manuscript-audit/01_numeric_unit_mismatch/input.md` 内容（不必克隆仓库到业务项目）。
- 四舍五入：`12_rounding_tolerance` 内容；7.14 vs 7.1 不应直接 Critical。

## 6–7. 证据与脚本/语义分界

每条 ISSUE 须有 Location / Evidence / Evidence state。  
Deterministic checks 与 Semantic findings 分节；未跑脚本须写入 Unrun。

## 8. 记录

```text
Date / Cursor version / Install path from skills list:
Discovered in non-repo project (Y/N):
Slash works (Y/N):
Cases 01 & 12 notes:
```

## 9. 未发现时排查

1. `npx skills list -g --json` 是否还有该 Skill。
2. `path` 下是否有 `SKILL.md`，`name` 是否匹配。
3. 重启 Cursor；检查是否禁用 Skills。
4. 对照：仅当验证项目级安装时，才对测试项目执行不带 `-g` 的 `npx skills add ...`。
5. 记录 Cursor 版本到 `docs/decisions/open-questions.md`。

## 10. 须人工完成

- [ ] 全局安装后，在**非本仓库**项目中被发现
- [ ] 引用路径正确
- [ ] 案例 01 / 12 报告质量合格
