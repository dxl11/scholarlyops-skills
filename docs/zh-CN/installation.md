# 安装指南 · ScholarlyOps

[English](../en/installation.md) | 简体中文

## 三种使用场景

| 场景 | 对象 | 是否默认推荐 |
|------|------|--------------|
| **Agent 全局安装** | 最终用户：装到 Cursor / Claude Code 等个人技能目录，跨项目复用 | **是（主要路径）** |
| 源码开发 | 维护者：在本仓库开发、测试、改 Skill | 维护者专用 |
| 项目级安装 | 团队需要锁定同一套 Skill 版本时 | **可选**，非必要条件 |

项目级安装**不是**使用 ScholarlyOps 的前提。

## 前置依赖

| 用途 | 依赖 |
|------|------|
| 推荐安装方式（`npx skills`） | Node.js 18+（通过 `npx` 临时拉取 CLI，无需全局安装 `skills`） |
| 调用已安装 Skill | Cursor 或 Claude Code 等兼容 Agent |
| `manuscript-audit` 确定性脚本 | Python 3.10+（标准库）；未安装 Python 时仍可做语义审计，但脚本检查不可用 |
| 本仓库开发与本地评测 | Python 3.10+ |

安全说明：

- 不要把 API Key 写进安装命令。
- 不要默认用管理员 / root 安装。
- `npx skills` 会从 GitHub 拉取仓库内容；请确认来源为可信仓库后再执行。
- 本项目的 Skill **不会**在安装时隐式要求你执行自定义远程脚本；若未来安装器行为变化，以 CLI 提示为准。

## 仓库与 Skill 发现（已验证）

- 权威源码目录（单一来源）：`.agents/skills/<skill-name>/SKILL.md`
- 当前仓库布局**可被** `npx skills` 发现，**无需**再建第二套 `skills/` 副本。
- 实测 CLI：`skills` **1.7.4**（`npx skills`）
- 实测发现命令（本地与 GitHub 均成功列出 4 个 Skill）：

```bash
npx skills add dxl11/scholarlyops-skills --list
# 或在本仓库根目录：
npx skills add . --list
```

已发现：`research-context`、`evidence-writing`、`manuscript-audit`、`review-response`。

GitHub 仓库标识（来自本机 `git remote`，且 `--list` 已成功）：`dxl11/scholarlyops-skills`  
若你 fork 或迁移仓库，请把下文中的 `dxl11/scholarlyops-skills` 换成你的 `<owner>/<repo>`。

---

## 一、主要路径：Agent 全局安装（推荐）

全局安装后，Skill 可在**多个工作项目**中复用，无需每个业务仓库复制一遍。

### 1.1 安装某一个 Skill（示例：manuscript-audit）

**Cursor：**

```bash
npx skills add dxl11/scholarlyops-skills -g -a cursor -s manuscript-audit -y --copy
```

**Claude Code：**

```bash
npx skills add dxl11/scholarlyops-skills -g -a claude-code -s manuscript-audit -y --copy
```

说明：

- `-g` / `--global`：安装到用户级目录（跨项目）。
- `-a`：目标 Agent。
- `-s`：Skill 名称。
- `-y`：跳过交互确认（适合脚本化；首次建议先去掉 `-y` 看摘要）。
- `--copy`：复制文件（本机 Windows 实测采用此方式更直观；默认也可能创建链接，以 CLI 输出为准）。

### 1.2 安装整套四个 Skills

```bash
# Cursor
npx skills add dxl11/scholarlyops-skills -g -a cursor --skill '*' -y --copy

# Claude Code
npx skills add dxl11/scholarlyops-skills -g -a claude-code --skill '*' -y --copy
```

也可一次指定多个 Agent（若本机都已安装）：

```bash
npx skills add dxl11/scholarlyops-skills -g -a cursor -a claude-code --skill '*' -y --copy
```

### 1.3 检查安装结果

```bash
npx skills list -g -a cursor
npx skills list -g -a claude-code
# 机器可读：
npx skills list -g --json
```

**路径说明（务必区分“文档表”与“本机实测”）：**

| Agent | CLI 文档常见全局路径 | 本仓库维护环境实测（2026-10-21） |
|-------|----------------------|----------------------------------|
| Cursor | `~/.cursor/skills/` | 安装落到 `%USERPROFILE%\.agents\skills\<skill>\`，且 `skills list -g` 显示绑定 Agent=`Cursor` |
| Claude Code | `~/.claude/skills/` | **本环境未实测安装到 Claude Code**（命令已按 CLI 文档给出，路径以你机器上 CLI 输出为准） |

Cursor / Claude 也可能同时从项目级 `.agents/skills/`、`.cursor/skills/`、`.claude/skills/` 等位置发现技能。**以 `npx skills list -g` 打印的实际 `path` 为准。**

手工抽查（Windows PowerShell 示例）：

```powershell
Get-ChildItem "$env:USERPROFILE\.agents\skills" -ErrorAction SilentlyContinue
Get-ChildItem "$env:USERPROFILE\.cursor\skills" -ErrorAction SilentlyContinue
Get-ChildItem "$env:USERPROFILE\.claude\skills" -ErrorAction SilentlyContinue
```

### 1.4 如何调用已安装的 Skill

1. 打开**任意**工作项目（不必是 ScholarlyOps 仓库）。
2. 在 Cursor Agent 输入 `/`，搜索 Skill 名（如 `manuscript-audit`），或直接点名：“按 manuscript-audit 审计以下文稿”。
3. Claude Code：按该产品对 Skills 的调用方式启用（通常为相关任务自动选用或显式提及 Skill 名）。

文件存在 ≠ 已加载。请在 IDE 中确认 Agent 是否遵循该 `SKILL.md`。验收清单见 [cursor-smoke-test.md](cursor-smoke-test.md)。

### 1.5 更新

```bash
npx skills update -g -a cursor -y
# 或按 Skill：
npx skills update manuscript-audit -g -a cursor -y
```

### 1.6 卸载

```bash
npx skills remove manuscript-audit -g -a cursor -y
# 移除该来源下已装技能时，按 CLI 提示操作；可用：
npx skills remove -g -a cursor -s '*' -y
```

卸载后可用 `npx skills list -g` 确认列表为空（或不再包含目标 Skill）。

### 1.7 加载失败时排查

1. `npx skills list -g --json` 是否仍列出该 Skill 及正确 `path`。
2. 该路径下是否存在 `SKILL.md`，Frontmatter 是否含 `name` / `description`，且 `name` 与目录名一致。
3. 重启 Cursor / Claude Code 后再试 `/` 搜索。
4. 确认未在 Settings 中禁用 Skills。
5. `manuscript-audit` 脚本失败时：检查是否已安装 Python 3.10+；脚本路径相对于 **Skill 安装目录** 下的 `scripts/`。

---

## 二、可选：项目级安装

仅当团队需要把同一套 Skill **锁进某个业务仓库**时使用。影响范围限于该项目目录，不会自动作用于你的其他项目。

```bash
# 在业务项目根目录执行（不要加 -g）
npx skills add dxl11/scholarlyops-skills -a cursor -s manuscript-audit -y --copy
```

典型落点（以 CLI 输出为准）：项目内 `.agents/skills/<skill>/` 等。

也可用手工复制（等价备选，非推荐默认）：

```powershell
New-Item -ItemType Directory -Force -Path ".agents\skills" | Out-Null
Copy-Item -Recurse -Force `
  "D:\path\to\scholarlyops-skills\.agents\skills\manuscript-audit" `
  ".agents\skills\manuscript-audit"
```

---

## 三、源码开发（维护者）

```bash
git clone https://github.com/dxl11/scholarlyops-skills.git
cd scholarlyops-skills
python tools/validate_skills.py
python -m unittest discover -s tests -v
python tools/run_evals.py
```

开发时编辑的权威文件始终在仓库 `.agents/skills/`。不要维护第二套互不同步的 `SKILL.md`。

---

## 四、独立安装边界

每个 Skill 自带 `SKILL.md` 与所需 `references/` / `scripts/` / `examples/`。单独全局安装后：

- **不得**依赖未安装的仓库其他路径或本机绝对路径。
- `manuscript-audit` 脚本示例：

```bash
# 在 Skill 安装目录内执行（路径以 skills list 为准）
python scripts/check_numeric_consistency.py --input /path/to/copy.md --json
```

- 未安装 Python 时：安装仍成功，但确定性脚本不可用；语义流程仍可按 `SKILL.md` 进行，并应在报告中写明未运行脚本。

## 五、验证状态记录（如实）

| 项目 | 状态 |
|------|------|
| `npx skills` 发现本仓库 4 个 Skill（本地 `.`） | 已验证通过 |
| `npx skills` 发现 `dxl11/scholarlyops-skills`（GitHub） | 已验证通过 |
| Cursor 全局安装 `manuscript-audit`（`-g -a cursor --copy`） | 已验证：文件落到 `~/.agents/skills/manuscript-audit`，`list -g` 可见 |
| Cursor IDE 内 `/` 菜单发现与语义执行 | **待你在 IDE 勾选**（见 smoke-test） |
| Claude Code 全局安装与加载 | **待验证**（命令已按 CLI 文档提供） |
| 其他 Agent | **仅计划支持**，未宣称已支持 |

## 六、安全与范围

| 方式 | 影响范围 |
|------|----------|
| 全局安装 `-g` | 当前用户下的 Agent 技能目录；跨项目可见 |
| 项目级安装 | 仅当前仓库；可随仓库共享给团队 |
| 源码克隆 | 仅本地开发副本 |

许可证仍可能未最终确定；安装与使用前请阅读仓库根目录说明与 [open-questions.md](../decisions/open-questions.md)。
