# 安装指南 · ScholarlyOps

[English](../en/installation.md) | 简体中文

品牌与路径约定见仓库根目录 [`project.json`](../../project.json)。标准 Skills 根目录：`.agents/skills/`。

## 前置依赖

| 场景 | 依赖 |
|------|------|
| 仅使用 Skills | 兼容 Agent（优先 Cursor） |
| 开发 / 运行验证 | Python 3.10+（标准库即可） |

本仓库**不要求** Node.js。未经验证的第三方 CLI **不作为**正式安装方式。

---

## 场景 1：克隆整个仓库做本地开发

### 步骤

```bash
git clone <YOUR_REPO_URL> scholarlyops-skills
cd scholarlyops-skills
```

远程地址未定时，也可直接使用本地已有目录。

### 验证

```bash
python tools/validate_skills.py
python -m unittest tests.test_validate_skills -v
```

期望：验证退出码为 0；单元测试全部通过。

### 卸载

删除本地克隆目录即可（勿误删其他项目中的副本）。

---

## 场景 2：在 Cursor 当前项目中使用 Skills

### 放置位置

```text
你的项目/
└── .agents/
    └── skills/
        ├── research-context/
        ├── evidence-writing/
        ├── manuscript-audit/
        └── review-response/
```

Cursor 文档亦提及 `.cursor/skills/`。本项目**标准位置**为 `.agents/skills/`，以利于扩展。若你的环境仅识别其一，可复制到实际被识别的目录，并在团队文档中记录。

### PowerShell（从本仓库复制全部 Skills）

```powershell
$src = "D:\path\to\scholarlyops-skills\.agents\skills"
$dst = ".agents\skills"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Recurse -Force "$src\*" $dst
```

### Bash

```bash
mkdir -p .agents/skills
cp -R /path/to/scholarlyops-skills/.agents/skills/* .agents/skills/
```

### 如何确认已被识别

1. 确认目标项目中存在 `.agents/skills/<name>/SKILL.md`。
2. 在 Cursor Agent 对话中点名该 Skill（例如“按 manuscript-audit 审计以下文稿”）。
3. **注意**：文件存在 ≠ 已加载。请在你的 Cursor 版本中观察 Agent 是否引用该 Skill 的指令；本仓库不声称已在你的环境完成加载实测。

### 运行示例

对 `manuscript-audit`：提供合成案例 `evals/cases/manuscript-audit/01_numeric_unit_mismatch/input.md`（开发仓库内）或你自己的稿件副本，要求输出分级审计报告。

### 更新 / 移除

- 更新：重新复制对应 Skill 目录覆盖（先备份本地改动）。
- 移除：删除 `.agents/skills/<skill-name>/`。

---

## 场景 3：将单个 Skill 安装到其他项目

以 `manuscript-audit` 为例：

```powershell
New-Item -ItemType Directory -Force -Path ".agents\skills" | Out-Null
Copy-Item -Recurse -Force `
  "D:\path\to\scholarlyops-skills\.agents\skills\manuscript-audit" `
  ".agents\skills\manuscript-audit"
```

该 Skill 目录应自包含 `SKILL.md`、`references/`、`scripts/` 等运行所需文件，**不依赖**安装后不存在的仓库其他路径。

验证：打开 `.agents/skills/manuscript-audit/SKILL.md`，确认 Frontmatter 中 `name: manuscript-audit`。

---

## 场景 4：扩展到其他兼容 Agent（待验证）

不同产品可能使用不同目录（例如用户级 `~/.claude/skills/`、`~/.codex/skills/` 等）。**本项目尚未对上述路径做实测。**

建议流程：

1. 查阅目标产品官方 Skills 文档，确认真实目录。
2. 将单个 Skill 目录复制到该路径。
3. 用最小任务验证是否加载。
4. 将结果记入 `docs/decisions/open-questions.md` 或新的兼容性笔记。

在验证前，不得宣传“已支持某 Agent”。

---

## 常见故障排查

| 现象 | 可能原因 | 处理 |
|------|----------|------|
| Agent 未按 Skill 规则输出 | 目录未放对或未被加载 | 检查 `.agents/skills/.../SKILL.md`；在对话中显式引用 |
| `validate_skills.py` 失败 | 路径错误 / Frontmatter 不规范 | 阅读工具输出的具体错误 |
| 复制后脚本找不到文件 | 只拷了 `SKILL.md` | 复制整个 Skill 目录 |
| 中文路径问题 | Shell 编码 | 使用引号包裹路径；优先相对路径 |

## Cursor 加载验收

结构符合官方 `.agents/skills/` 约定，但**加载是否成功须在 IDE 中确认**。步骤见 [cursor-smoke-test.md](cursor-smoke-test.md)。

## 本地评测（与 IDE 无关）

```bash
python tools/run_evals.py
```

仅评分确定性脚本案例；语义案例会 skip，不记为通过。

## 安全提醒

- 不要把私有稿件提交到公共仓库。
- 不要在 Skill 或示例中写入真实 API Key。
