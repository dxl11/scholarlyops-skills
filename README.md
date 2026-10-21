# ScholarlyOps

**学术研究工作流 Skills**

基于科研证据的可扩展 AI 工作流技能集。

[English](README_EN.md) | 简体中文

> **状态**：初始化 / 开发中。当前 Skills 成熟度均为 **Draft**。许可证尚未选定。名称与商标未做法律清核。请勿虚构 Star、下载量、用户规模或第三方认证。

项目元数据集中见 [`project.json`](project.json)。建议仓库名：`scholarlyops-skills`。

## 为什么需要 ScholarlyOps

科研写作中，AI 常被用来“把文字写得更像论文”，却容易在无意中改变数值、夸大因果、虚构引文支持或覆盖原稿。ScholarlyOps 把这些风险变成可执行的 Skill 约束：事实保真、证据可追溯、修改可审计、模块可测试、安全优先。

## 解决哪些问题

| 问题 | 对应能力 |
|------|----------|
| 材料散乱、事实与解释混杂 | `research-context` 结构化研究记录 |
| 段落漂亮但证据稀薄 | `evidence-writing` 证据约束写作 |
| 摘要/正文/图注/结论不一致 | `manuscript-audit` 一致性审计 |
| 审稿回复难以追踪修改 | `review-response` 意见—修改映射 |

## 设计理念

1. **事实保真**：不为文采改动数据、设计、统计与结论强度。
2. **证据可追溯**：重要主张尽量关联原文、图表、数据或文献位置。
3. **修改可审计**：保留原文、修订、理由、证据与待确认项；默认不覆盖原稿。
4. **模块化**：每 Skill 边界清晰，可独立安装，无隐式绝对路径依赖。
5. **可测试**：结构验证与合成评测可运行；成熟度必须有证据。
6. **安全优先**：不硬编码凭据；不默认上传私有材料；外部 API 须明示边界。

## 当前 Skills 与成熟度

| Skill | 中文名 | 职责 | 成熟度 |
|-------|--------|------|--------|
| [`research-context`](.agents/skills/research-context/) | 研究上下文整理 | 整理目标、设计、数据、结果、限制与待核实项 | Draft |
| [`evidence-writing`](.agents/skills/evidence-writing/) | 证据约束写作 | 在证据约束下起草/改写段落 | Draft |
| [`manuscript-audit`](.agents/skills/manuscript-audit/) | 论文一致性审计 | 跨章节一致性与证据风险审计（示范实现） | Draft |
| [`review-response`](.agents/skills/review-response/) | 审稿意见回复 | 拆分意见并关联修改、证据与状态 | Draft |

成熟度定义：`Draft` / `Beta` / `Stable`（见 [产品规格](docs/PRODUCT_SPEC.md)）。**尚未有任何 Skill 达到 Beta 或 Stable。**

## 目录结构

```text
scholarlyops-skills/
├── README.md / README_EN.md
├── project.json                 # 品牌与元数据集中管理
├── .agents/skills/              # 标准 Skills 根目录
├── docs/                        # 产品、架构、安装、决策
├── evals/                       # 合成评测案例
├── tools/validate_skills.py     # 结构与链接验证（标准库）
├── tests/                       # 单元测试
└── .github/workflows/           # CI（无外部密钥）
```

## 安装与使用

完整说明：

- [安装指南（中文）](docs/zh-CN/installation.md)
- [Installation (English)](docs/en/installation.md)

Cursor 项目级 Skills 标准路径：`.agents/skills/`（亦兼容文档中提及的 `.cursor/skills/`；本仓库以 `.agents/skills/` 为准）。

**快速复制单个 Skill（PowerShell）：**

```powershell
New-Item -ItemType Directory -Force -Path ".agents\skills" | Out-Null
Copy-Item -Recurse -Force `
  "D:\path\to\scholarlyops-skills\.agents\skills\manuscript-audit" `
  ".agents\skills\manuscript-audit"
```

## 使用示例（manuscript-audit）

1. 使用稿件副本，勿默认覆盖原稿。
2. 在 Agent 中启用 `manuscript-audit`。
3. 提供摘要、正文相关节、图注/表注、可选参考文献。
4. 获得分级报告：Critical / Major / Minor / Needs Review，含位置、证据与待确认项。

合成案例：[`evals/cases/manuscript-audit/`](evals/cases/manuscript-audit/)

## 依赖与环境

- 阅读与使用 Skills：兼容 Agent（优先 Cursor）；无强制运行时。
- 运行仓库验证与测试：Python **3.10+**，仅标准库。

```bash
python tools/validate_skills.py
python -m unittest discover -s tests -v
python -m unittest discover -s .agents/skills/manuscript-audit/tests -v
python tools/run_evals.py
```

`run_evals.py` 只自动评分**确定性脚本**案例；`agent_semantic` 会被 skip，不记为通过。Cursor 加载见 [人工验收指南](docs/zh-CN/cursor-smoke-test.md)。

## 学术诚信与数据安全

- 不得伪造实验、数值、引文支持或“已完成修改”。
- 证据状态：`verified` / `partially_supported` / `unverified` / `unsupported` / `conflicting`。
- 引用分层核验：存在性 → 元数据 → 内容支持 → 论证恰当性。
- 私有稿件与输出目录由 `.gitignore` 保护；报告安全问题见 [SECURITY.md](SECURITY.md)。

## 当前限制

- 全部 Skills 为 Draft；未做大规模真实稿件验证。
- 未选定许可证；未配置正式 GitHub 远程地址。
- 文献 API、自动投稿、跨 Agent 安装器等**未实现**，仅列于路线图。
- Frontmatter 验证为有限字符串检查，非完整 YAML 解析。
- Cursor 是否在当前会话中自动加载 `.agents/skills/` **需用户在 IDE 中确认**；本仓库提供结构与文档，不声称已在你的环境完成加载实测。

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证状态

**尚未确定。** 在维护者添加 `LICENSE` 之前，不得宣称已采用 MIT、Apache-2.0 或其他许可证。讨论见 [open-questions.md](docs/decisions/open-questions.md)。

## 相关文档

- [产品规格](docs/PRODUCT_SPEC.md) · [路线图](docs/ROADMAP.md)
- [架构（中文）](docs/zh-CN/architecture.md) · [Architecture (EN)](docs/en/architecture.md)
- [评测说明](evals/README.md) · [Cursor 验收（中文）](docs/zh-CN/cursor-smoke-test.md) · [更新日志](CHANGELOG.md)
