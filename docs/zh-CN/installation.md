# 安装指南 · ScholarlyOps

[English](../en/installation.md) | 简体中文

> **原则**：优先让当前 Agent 帮你装到**用户级全局**技能目录；`npx skills` 为备用。  
> **文件落盘 ≠ 已加载**：安装后仍须在 Agent UI 中确认发现/调用。  
> **一句自然语言不能保证对所有 Agent 都生效**——请按下方「已核实路径」选择。

仓库：[`https://github.com/dxl11/scholarlyops-skills`](https://github.com/dxl11/scholarlyops-skills)  
权威源码（单一来源）：`.agents/skills/<skill-name>/`（含 `SKILL.md`、`references/`、`scripts/`、`examples/` 等）

五个 Skills：`research-context` · `literature-search` · `evidence-writing` · `manuscript-audit` · `review-response`（均为 **Draft**）

---

## 1. 让 Agent 帮你安装（首选）

把下面整段复制到 **Cursor / Claude Code / Codex** 等当前会话中。Agent 应识别自身环境与操作系统，再选用该平台支持的官方方式安装到**全局**目录。

### 可复制安装指令

```text
请帮我安装 ScholarlyOps Skills。

仓库：https://github.com/dxl11/scholarlyops-skills
权威路径：.agents/skills/

五个 Skills（请先列出并让我选择全部或指定若干）：
1. research-context
2. literature-search
3. evidence-writing
4. manuscript-audit
5. review-response

要求：
1. 识别当前 Agent 名称与操作系统（Windows / macOS / Linux）。
2. 优先使用本 Agent 的官方/内置安装方式；若不可用，再使用经核实的全局目录复制或 CLI 备用方案。
3. 安装到用户级全局技能目录，供多个项目复用；不要默认装进当前业务项目目录。
4. 安装前检查目标目录；若同名 Skill 已存在，先说明冲突并征求确认，未经确认不得覆盖。
5. 保留所选 Skill 的完整必要内容：SKILL.md、references/、scripts/、examples/ 等（不要只拷一个空壳）。
6. 安装后报告实际文件路径，并说明如何在本 Agent 中验证是否已加载（例如 / 菜单搜索 Skill 名）。
7. 若无法完成安装，清楚说明原因，并给出本仓库文档中的替代方式（原生插件路径 / CLI）。
8. 不要执行未经审查的远程脚本；不要写入真实 API Key 或凭据；不要改写 Git 历史。
```

### 预期行为（由 Agent 执行，非保证自动成功）

| 步骤 | 说明 |
|------|------|
| 列清单 | 展示 5 个 Skill，确认「全部」或子集 |
| 选路径 | 按下方「各 Agent 已核实路径」选择 |
| 防覆盖 | 目标已存在 → 询问后再决定跳过/备份/覆盖 |
| 核实 | 报告落盘路径；提醒用户重启或重新打开会话后再测加载 |

---

## 2. 原生 / 平台安装路径（已核实摘要）

下列内容依据公开官方文档核对（查阅日约 **2026-10-22**）。**本仓库尚未提交已验证的 Cursor/Claude 插件 Marketplace 包**；因此不宣称「一键插件市场上架已可用」。

### 2.1 Codex（OpenAI）

| 项 | 内容 |
|----|------|
| 内置安装器 | `$skill-installer`（见 [openai/skills skill-installer](https://github.com/openai/skills/blob/main/skills/.system/skill-installer/SKILL.md)） |
| 全局目录 | `$CODEX_HOME/skills/`（默认 `~/.codex/skills/`） |
| GitHub 目录 URL | 支持按路径安装第三方仓库中的 Skill 文件夹；目标已存在时**中止**（不静默覆盖） |
| 示例（单个 Skill） | 在 Codex 中让 `$skill-installer` 安装类似：`https://github.com/dxl11/scholarlyops-skills/tree/main/.agents/skills/manuscript-audit` |
| 多个 Skill | 对每个 `.agents/skills/<name>` 重复安装，或一次传入多个 `--path`（以安装器脚本能力为准） |
| 安装后 | 按 Codex 提示重启/新回合后再发现 Skill |
| 注意 | `openai/skills` 仓库本身已标记 deprecated、导向 Plugins；**`$skill-installer` 对 GitHub 路径安装的能力仍以该 SKILL 文档为准**。本环境未替你实际跑通 Codex 安装，请在 Codex 内验证。 |

### 2.2 Cursor

| 项 | 内容 |
|----|------|
| 官方 Skills 文档 | [cursor.com/docs/skills](https://cursor.com/docs/skills) |
| 用户级全局目录 | `~/.agents/skills/`、`~/.cursor/skills/`（Windows：`%USERPROFILE%\.agents\skills\` 等） |
| 项目级 | `.agents/skills/`、`.cursor/skills/`（**非**默认推荐给最终用户） |
| 兼容加载 | 也可发现 `~/.claude/skills/`、`~/.codex/skills/` 等 |
| 从 GitHub「原生导入 Skills」 | 文档写明：Skills **不会**单独从裸仓库导入；需打成 **Plugin**，经 Marketplace /「From GitHub Repository」导入，且仓库需含 `.cursor-plugin/marketplace.json` 等（见同站 Plugins 文档） |
| 本仓库现状 | **未提供**已验证的 Cursor 插件 Marketplace 配置；请用「让 Agent 安装」复制到全局目录，或用下方 CLI |
| Cloud Agents | 仅 `~/.cursor/skills/` 可按设置同步；`~/.agents/skills/` 默认不进 Cloud（以官方文档为准） |
| UI 验收 | [cursor-smoke-test.md](cursor-smoke-test.md)（**待你本机勾选**） |

### 2.3 Claude Code

| 项 | 内容 |
|----|------|
| 官方 Skills 文档 | [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) |
| 个人全局目录 | `~/.claude/skills/<name>/SKILL.md`（本机各项目可用；不等于云端/Cowork 全自动同步） |
| 项目级 | `.claude/skills/`（可选，非最终用户默认） |
| 插件 Marketplace | 需带 `.claude-plugin/marketplace.json` 的 marketplace 仓库；再 `/plugin marketplace add …` 与 `/plugin install …`（见 [Plugins](https://code.claude.com/docs/en/plugins/overview)） |
| 本仓库现状 | **未提供**已验证的 Claude Code marketplace 插件包；请用 Agent 复制到 `~/.claude/skills/`，或 CLI |
| 本环境 | Claude Code 安装与加载 **待实测** |

### 2.4 原生插件分发评估（结论）

在保持 `.agents/skills/` 为**唯一权威源**的前提下：

- Cursor / Claude Code 的「官方插件市场体验」需要**额外**的 marketplace/plugin 清单与目录布局（技能常位于插件内的 `skills/`）。  
- 若未来提供插件包，应使用**自动打包**（从 `.agents/skills/` 生成），避免人工维护两份 `SKILL.md`。  
- **当前不提交未经验证的** `.cursor-plugin/*` / `.claude-plugin/*`，以免「有 JSON 却装不上」的误导。详见 [plugin-distribution.md](../decisions/plugin-distribution.md)。

---

## 3. 命令行安装（备用）

适用：Agent 无法写用户目录、或你更习惯终端。需要 **Node.js 18+**。CLI：[`npx skills`](https://github.com/vercel-labs/skills)（核对版本：**1.7.4**；以 `npx skills --help` 为准）。

### 3.1 列出仓库中的 Skills

```bash
npx skills add dxl11/scholarlyops-skills --list
```

### 3.2 全局安装全部 Skills

```bash
npx skills add dxl11/scholarlyops-skills --global --agent cursor claude-code --skill '*'
```

### 3.3 全局安装指定 Skill

```bash
npx skills add dxl11/scholarlyops-skills --global --agent cursor --skill manuscript-audit
npx skills add dxl11/scholarlyops-skills --global --agent claude-code --skill literature-search
```

### 3.4 只安装到某一个 Agent

把 `--agent` 设为 `cursor`、`claude-code`，或 CLI 支持的其他标识（见 `--help`）。

### 3.5 项目级安装（可选，非默认）

在业务项目根目录执行（**不加** `--global`）：

```bash
npx skills add dxl11/scholarlyops-skills --agent cursor --skill manuscript-audit
```

仅影响该仓库；不会自动作用于你的其他项目。

### 3.6 查看 / 更新 / 卸载

```bash
npx skills list --global
npx skills update --global -y
npx skills update manuscript-audit --global -y
npx skills remove manuscript-audit --global --agent cursor -y
```

短参数等价：`-g`、`-a`、`-s`。可选 `--copy`（复制而非符号链接；Windows 维护环境曾用于 Cursor 落盘验证）。

### 3.7 各平台提示

`npx …` 在 Windows PowerShell、macOS、Linux 上写法相同。

```powershell
# Windows：查看常见落盘位置
Get-ChildItem "$env:USERPROFILE\.agents\skills" -ErrorAction SilentlyContinue
Get-ChildItem "$env:USERPROFILE\.cursor\skills" -ErrorAction SilentlyContinue
Get-ChildItem "$env:USERPROFILE\.claude\skills" -ErrorAction SilentlyContinue
Get-ChildItem "$env:USERPROFILE\.codex\skills" -ErrorAction SilentlyContinue
```

```bash
# macOS / Linux
ls -la ~/.agents/skills ~/.cursor/skills ~/.claude/skills ~/.codex/skills 2>/dev/null
```

---

## 4. 常见问题（Troubleshooting）

| 问题 | 建议 |
|------|------|
| 装了但 `/` 搜不到 | 重启 Agent/IDE；确认落在全局目录；Cursor 打开 Customize → Skills；见 smoke-test |
| 装进了当前项目而不是全局 | 重新用 `--global` 或复制到用户级目录；项目级仅可选 |
| 同名 Skill 已存在 | 先备份再覆盖；Codex `$skill-installer` 默认遇已存在会中止 |
| 权限不足 | 勿用管理员盲目提权；检查主目录写权限；改用用户可写路径 |
| CLI 拉取不到 5 个 Skill | 确认 GitHub 已包含最新提交；或 `npx skills add . --list` 在本地克隆上验证 |
| 更新 | `npx skills update --global`；或让 Agent 按防覆盖规则重新同步 |
| 卸载 | `npx skills remove …`；或手动删除对应用户级 Skill 文件夹（先确认路径） |
| manuscript-audit 脚本 | 需 Python 3.10+；在**安装目录**下运行 `scripts/` |
| 安全 | 不把密钥写入 Skill 文件；不运行来路不明的安装脚本；`npx`/`git` 仅指向你信任的仓库 |

---

## 5. 源码开发（维护者）

```bash
git clone https://github.com/dxl11/scholarlyops-skills.git
cd scholarlyops-skills
python tools/validate_skills.py
```

只编辑 `.agents/skills/`。不要另建需手工同步的第二套 Skill 树。

---

## 6. 验证状态（如实）

| 项目 | 状态 |
|------|------|
| 本地 `.agents/skills/` 含 5 个 Skill；`npx skills add . --list` | 维护环境曾验证 |
| Cursor 全局落盘（CLI `--copy`） | 此前对 `manuscript-audit` 验证过；非本阶段重测 |
| Cursor IDE `/` 加载 | **待用户** smoke-test |
| Codex `$skill-installer` + 本仓库 URL | **文档已核对**；**本环境未实测** |
| Claude Code 全局目录 / 插件市场 | **文档已核对**；**安装与加载未实测** |
| Cursor/Claude 官方 Marketplace 上架包 | **未提供**（见插件分发决策） |

许可证仍可能未定：见 [open-questions.md](../decisions/open-questions.md)。
