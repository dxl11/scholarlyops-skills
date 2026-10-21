# Cursor 人工验收指南 · manuscript-audit

[English](../en/cursor-smoke-test.md) | 简体中文

> **状态**：本文件是**需你在 Cursor IDE 界面中执行**的验收清单。  
> 仓库维护者**尚未**在本机完成加载实测前，不得宣称 Skill 已成功加载。  
> 参考官方文档：[Cursor Agent Skills](https://cursor.com/docs/skills)（项目级目录含 `.agents/skills/` 与 `.cursor/skills/`）。

本仓库**标准源码目录**为 `.agents/skills/`（单一事实来源）。不要为了试加载而长期维护第二份完整副本；仅在排查时临时验证备用路径。

## 0. 前置

- 已用本仓库作为 Cursor 工作区根目录打开，或已将 `manuscript-audit` 目录复制到目标项目的 `.agents/skills/manuscript-audit/`。
- 确认存在：`.agents/skills/manuscript-audit/SKILL.md`。
- 可选：先跑本地脚本评测（与 IDE 加载无关）：

```bash
python tools/run_evals.py
```

## 1. 确认 Cursor 是否发现 `manuscript-audit`

在 Cursor Agent 聊天输入框：

1. 输入 `/`，搜索 `manuscript-audit`。
2. 或打开 Cursor Settings 中与 Skills / Rules 相关的面板，查看是否列出该 Skill。

**通过标准**：能在 `/` 菜单或 Skills 列表中看到 `manuscript-audit`。  
**失败**：见第 9 节排查。将结果记入下方记录表（发现 / 未发现）。

> 社区曾有反馈：部分版本中 `.agents/skills` 可被索引但 `/` 调用异常，而 `.cursor/skills` 更稳定。若仅 `/` 失败，先记录版本与现象，再考虑**临时**复制单 Skill 到 `.cursor/skills/` 做对照实验（不要提交双份源码到仓库）。

## 2. 如何手动调用

推荐明确指令（复制使用）：

```text
请严格按 manuscript-audit Skill（读取 .agents/skills/manuscript-audit/SKILL.md）审计以下合成稿件。
先运行该 Skill 目录下的 scripts（若环境允许），再做语义判断。
输出必须使用报告模板：含 Summary、Deterministic checks、Issues（含 Severity / Location / Evidence / Evidence state / Suggested fix / Author confirmation）、Unrun checks、Limits。
不得覆盖我的输入文件；不得把猜测标为 Critical。
```

也可尝试：`/manuscript-audit`（若当前 Cursor 版本支持 slash 调用）。

## 3. 验证 Agent 是否读取了正确的 SKILL.md

在同一会话中要求：

```text
请引用你正在遵循的 Skill 文件路径，并摘录其中「严重程度定义」表格的 Critical 与 Needs Review 两行原文。
```

**通过标准**：路径指向本仓库（或你复制到的项目内）`.../manuscript-audit/SKILL.md`，且摘录与文件一致（含 Needs Review 不得当作已确认错误）。

## 4. 合成输入：数值差异

打开并粘贴：`evals/cases/manuscript-audit/01_numeric_unit_mismatch/input.md`  
或让 Agent 读取该文件。

**期望（人工核对）**：

- 报告 enrolled 120 vs 100（Critical，证据状态宜为 `verified` 若基于原文）。
- 单位 uM vs mg/mL 应被提及（脚本 Major 或 Needs Review）。
- 每个问题有原文位置；无依据的额外 Critical → 记为失败。

可选对照脚本（终端）：

```bash
python .agents/skills/manuscript-audit/scripts/check_numeric_consistency.py --input evals/cases/manuscript-audit/01_numeric_unit_mismatch/input.md --json
```

## 5. 合成输入：合理四舍五入（不应直接判错）

使用：`evals/cases/manuscript-audit/12_rounding_tolerance/input.md`

**期望**：

- 7.14 vs 7.1 **不应**被标为 Critical 字面错误。
- 可说明“在容差内 / 可能为四舍五入”，或列入 tolerated / Needs Review（若模型不确定）。
- 将“把四舍五入当成 Critical”记为**误报**。

## 6. 确认每个问题都有依据

对报告中每条 ISSUE 检查：

| 字段 | 要求 |
|------|------|
| Location | 指向摘要/结果等具体位置 |
| Evidence | 引用原文片段或脚本输出 |
| Evidence state | 使用统一词表 |
| Author confirmation | Critical/Major 通常为 yes |

无 Location/Evidence 的 Critical/Major → 不合格。

## 7. 区分脚本检查与模型语义判断

在报告中要求 Agent 分节：

- **Deterministic checks**：粘贴或概述脚本 JSON（数值/单位）。
- **Semantic findings**：因果表述、引文支持性等；证据不足时用 Needs Review / `unverified`。

本地已自动跑通的仅是脚本层（`tools/run_evals.py`）。**语义节不得仅因本地评测通过而宣称已验证。**

## 8. 如何记录本次验收

请复制下表到你的私人笔记或 `outputs/`（已 gitignore），**不要**把真实私有稿件提交进仓库：

```text
Date:
Cursor version:
Workspace root:
Skill discovered (Y/N):
Slash /manuscript-audit works (Y/N):
SKILL.md path quoted by agent:
Case IDs tested:
Output saved as:
Pass/Fail notes:
```

建议同时保存 Agent 完整回复到本地文件，文件名含日期与 case id。

## 9. 若 Skill 未被发现 — 检查清单

1. 工作区根目录是否为包含 `.agents/skills/` 的仓库根（而非子文件夹）。
2. 路径是否为 `.agents/skills/manuscript-audit/SKILL.md`（Windows 下目录分隔在磁盘上为 `\`，但文档描述用 `/`）。
3. Frontmatter 是否含 `name: manuscript-audit` 与非空 `description`，且 `name` 与文件夹名一致。
4. Cursor Settings 中 Skill 是否被禁用。
5. 重启 Cursor / 重开窗口后再试 `/`。
6. 对照实验：临时仅复制**一个** Skill 到 `.cursor/skills/manuscript-audit/`，观察是否可发现（记录结果；不要把双份源码定为仓库长期结构）。
7. 记录 Cursor 版本号与操作系统，写入 `docs/decisions/open-questions.md` 的兼容性笔记。

## 10. 本清单中必须由你完成的项（终端无法代替）

- [ ] `/` 菜单或 Settings 中是否出现 `manuscript-audit`
- [ ] Agent 是否引用正确 `SKILL.md` 原文
- [ ] 案例 01 与 12 的 Agent 报告质量（依据、误报）
- [ ] 语义问题是否错误标成“脚本已 verified”

完成以上勾选前，项目文档应继续写：**Cursor 加载验证待用户确认**。
