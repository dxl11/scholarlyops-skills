# 安装指南 · ScholarlyOps

[English](../en/installation.md) | 简体中文

> **CLI 版本**：下文命令按 `npx skills`（`skills` **1.7.4**）的 `--help` 核对。若你本机 CLI 升级后参数变化，以 `npx skills --help` 为准。  
> **文件安装 ≠ Agent 已加载**：磁盘上有 `SKILL.md` 后，仍须在 Cursor / Claude Code 中确认能否发现并调用。

## 三种使用场景

| 场景 | 对象 | 是否默认推荐 |
|------|------|--------------|
| **Agent 全局安装** | 最终用户：装到个人 Agent 技能目录，跨项目复用 | **是（主要路径）** |
| 项目级安装 | 团队希望在某一业务仓库内共享同一套 Skill | **可选** |
| 源码开发 | 维护者克隆本仓库以修改 Skills、跑测试 | 维护者专用 |

**普通用户不必克隆整个仓库**，也不必把 Skills 复制进每个业务项目。

## 前置依赖

| 用途 | 依赖 |
|------|------|
| 推荐安装（`npx skills`） | Node.js 18+（通过 `npx` 拉取 CLI，无需全局安装 `skills`） |
| 调用已安装 Skill | Cursor 和/或 Claude Code 等兼容 Agent |
| `manuscript-audit` 确定性脚本 | Python 3.10+（标准库）；无 Python 时仍可按 `SKILL.md` 做语义审计，但脚本不可用 |
| 本仓库开发与本地评测 | Python 3.10+ |

安全：

- 不要把 API Key 写进安装命令。
- 不要默认用管理员 / root 安装。
- `npx skills` 会从 GitHub 拉取仓库；请确认来源为 `dxl11/scholarlyops-skills`（或你信任的 fork）。

## 仓库布局与发现（已核对）

- **唯一权威源码**：`.agents/skills/<skill-name>/SKILL.md`（不维护第二套需人工同步的副本）。
- 当前布局可被 `npx skills` 发现（本环境对 GitHub 源执行 `--list`：**已发现 4 个 Skill**）。

```bash
npx skills add dxl11/scholarlyops-skills --list
# 或在本仓库根目录：
npx skills add . --list
```

已发现：`research-context`、`evidence-writing`、`manuscript-audit`、`review-response`。

官方参考（安装器 / Agent Skills 概念）：

- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [Cursor Skills 文档](https://cursor.com/docs/skills)
- [Claude Agent Skills 概览](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

---

## 一、主要路径：Agent 全局安装（推荐）

### 1.1 安装单个 Skill（示例：manuscript-audit）

**同时装到 Cursor 与 Claude Code（若本机两者均由 CLI 识别）：**

```bash
npx skills add dxl11/scholarlyops-skills --global --agent cursor claude-code --skill manuscript-audit
```

**仅 Cursor：**

```bash
npx skills add dxl11/scholarlyops-skills --global --agent cursor --skill manuscript-audit
```

**仅 Claude Code：**

```bash
npx skills add dxl11/scholarlyops-skills --global --agent claude-code --skill manuscript-audit
```

等价短参数（与上相同语义；本仓库维护环境曾用 `--copy -y` 做过 Cursor 落盘验证）：

```bash
npx skills add dxl11/scholarlyops-skills -g -a cursor -s manuscript-audit -y --copy
```

说明：

| 参数 | 含义 |
|------|------|
| `--global` / `-g` | 安装到用户级目录（跨项目） |
| `--agent` / `-a` | 目标 Agent；可写多个，如 `cursor claude-code` |
| `--skill` / `-s` | Skill 名称 |
| `-y` | 跳过确认（首次可去掉以便审阅摘要） |
| `--copy` | 复制文件（相对符号链接更直观；Windows 维护环境曾用此方式） |

### 1.2 安装全部 Skills

```bash
npx skills add dxl11/scholarlyops-skills --global --agent cursor claude-code --skill '*'
```

仅 Cursor 或仅 Claude Code 时，把 `--agent` 改成单一目标即可。

短参数示例：

```bash
npx skills add dxl11/scholarlyops-skills -g -a cursor --skill '*' -y --copy
```

CLI 另提供 `--all`（等价于 `--skill '*' --agent '*' -y`）：会尝试安装到 CLI 检测到的**全部** Agent。若你只想装 Cursor/Claude Code，请显式写 `--agent`，不要误用过宽的 `--all`。

### 1.3 查看已安装 Skills

```bash
npx skills list --global
npx skills list --global --agent cursor
npx skills list --global --agent claude-code
npx skills list --global --json
```

短参数：`npx skills ls -g`、`npx skills ls -g -a cursor`。

### 1.4 更新

```bash
# 更新全部全局 Skills
npx skills update --global -y

# 更新单个 Skill（名称以 list 为准）
npx skills update manuscript-audit --global -y
```

短参数：`npx skills update -g -y`。

### 1.5 卸载

```bash
# 卸载单个 Skill（全局）
npx skills remove manuscript-audit --global --agent cursor -y

# 卸载某 Agent 下本套全部 Skill 名（按 CLI 支持的 '*'）
npx skills remove --global --agent cursor --skill '*' -y
```

也可用交互式：`npx skills remove`（按提示选择）。

卸载整套（危险：会移除该范围内已装技能；执行前先 `list` 确认）：

```bash
# 仅当确认要清空 CLI 管理的已装技能时使用；--all 会移除每一个已安装 Skill
# npx skills remove --global --all
```

更稳妥的做法：按名称逐个 `remove`，或对 `--skill '*'` 限定 `--agent cursor` / `claude-code`。

### 1.6 各平台命令提示

上述 `npx …` 在 **Windows PowerShell、macOS、Linux** 上写法相同（需已安装 Node.js 18+）。

手工查看落盘目录（路径以 `skills list --global` 打印的 `path` 为准）：

**PowerShell：**

```powershell
Get-ChildItem "$env:USERPROFILE\.agents\skills" -ErrorAction SilentlyContinue
Get-ChildItem "$env:USERPROFILE\.cursor\skills" -ErrorAction SilentlyContinue
Get-ChildItem "$env:USERPROFILE\.claude\skills" -ErrorAction SilentlyContinue
```

**macOS / Linux（bash/zsh）：**

```bash
ls -la ~/.agents/skills 2>/dev/null
ls -la ~/.cursor/skills 2>/dev/null
ls -la ~/.claude/skills 2>/dev/null
```

### 1.7 Cursor 与 Claude Code：加载位置与限制

| Agent | CLI 文档中常见路径 | 本仓库维护环境记录 | 限制 |
|-------|-------------------|-------------------|------|
| Cursor | 常提及 `~/.cursor/skills/` | 全局安装曾落到 `%USERPROFILE%\.agents\skills\<skill>\`，且 `list -g` 显示绑定 Cursor | **IDE `/` 菜单发现与语义执行仍待你本机勾选**（见 [cursor-smoke-test.md](cursor-smoke-test.md)） |
| Claude Code | 常提及 `~/.claude/skills/` | **本环境未实测** Claude Code 安装与加载 | 命令已按 CLI 给出；路径与加载以你机器上 CLI/产品行为为准 |

务必以 `npx skills list --global` 的 `path` 为准，不要假设固定目录。

### 1.8 如何开始使用

1. 完成全局安装后，打开**任意**工作项目（不必是 ScholarlyOps 仓库）。
2. **Cursor**：Agent 输入 `/`，搜索 `manuscript-audit`（或其他 Skill 名），或直接说明“按 manuscript-audit Skill 审计以下文稿”。
3. **Claude Code**：按该产品对 Agent Skills 的启用/调用方式操作（**本仓库未实测**）。
4. 使用稿件**副本**；默认不要覆盖原稿。
5. 需要跑确定性脚本时，在 **Skill 安装目录**下执行 `scripts/`（需 Python 3.10+）。

### 1.9 加载失败排查

1. `npx skills list --global --json` 是否仍列出该 Skill 及 `path`。
2. 该路径下是否有 `SKILL.md`，且 Frontmatter `name` 与目录名一致。
3. 重启 Cursor / Claude Code 后再试。
4. 确认未在设置中禁用 Skills。
5. 脚本失败：检查 Python；脚本相对安装目录下的 `scripts/`。

---

## 二、可选：项目级安装

团队需要把 Skill **锁进某个业务仓库**时使用（不加 `--global`）：

```bash
# 在业务项目根目录执行
npx skills add dxl11/scholarlyops-skills --agent cursor --skill manuscript-audit
```

典型落点（以 CLI 输出为准）：项目内 `.agents/skills/<skill>/` 等。  
项目级安装**不会**自动作用于你的其他本地项目。

---

## 三、源码开发（维护者）

```bash
git clone https://github.com/dxl11/scholarlyops-skills.git
cd scholarlyops-skills
python tools/validate_skills.py
python -m unittest discover -s tests -v
python tools/run_evals.py
```

只编辑仓库内 `.agents/skills/`。不要另建需手工同步的第二套 `SKILL.md` 树。

---

## 四、独立安装边界

每个 Skill 自带 `SKILL.md` 与所需 `references/` / `scripts/` / `examples/`。单独全局安装后：

- **不得**依赖未安装的其他仓库路径或本机绝对路径。
- 示例（cwd = Skill 安装目录）：

```bash
python scripts/check_numeric_consistency.py --input /path/to/copy.md --json
```

---

## 五、验证状态（如实；本阶段未重装）

| 项目 | 状态 |
|------|------|
| `npx skills` 1.7.4 `--help` 参数核对 | 已核对（本阶段） |
| `npx skills add dxl11/scholarlyops-skills --list` 发现 4 个 Skill | **已验证**（本阶段） |
| Cursor 全局安装落盘（`-g -a cursor --copy`） | **此前维护环境已验证**；本阶段未重新执行安装 |
| Cursor IDE `/` 发现与调用 | **待用户在 IDE 验证** |
| Claude Code 全局安装与加载 | **待验证** |
| 其他 Agent | **仅计划**，未宣称已支持 |

## 六、安全与范围

| 方式 | 影响范围 |
|------|----------|
| 全局 `--global` | 当前用户 Agent 技能目录；跨项目可见 |
| 项目级（无 `-g`） | 仅当前仓库 |
| 源码克隆 | 仅本地开发副本 |

许可证仍可能未最终确定；见 [open-questions.md](../decisions/open-questions.md) 与 [SECURITY.md](../../SECURITY.md)。
