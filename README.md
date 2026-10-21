<div align="center">

<img src="assets/scholarlyops-logo.jpg" alt="ScholarlyOps" width="280" />

# ScholarlyOps

### 让科研写作更严谨，让关键结论有据可查。

学术研究工作流 Skills —— 一套以科研证据为核心的可扩展 AI Skills，帮助研究者整理材料、约束写作、审计一致性，并追踪审稿回复。

<br/>

<p style="font-size: 1.35em; line-height: 1.8;">
  <a href="https://ailwb.com/"><b><u>网站</u></b></a>
  &nbsp;·&nbsp;
  <a href="README.md"><b><u>中文</u></b></a>
  &nbsp;·&nbsp;
  <a href="README_EN.md"><b><u>English</u></b></a>
</p>

<br/>

`事实保真` · `证据可追溯` · `修改可审计` · `工作流可测试`

</div>

---

## 这是什么

ScholarlyOps 不是零散提示词合集，而是面向科研生命周期的 **Agent Skills** 工具包。它把“写得像论文”收束为可执行的证据约束：重要主张尽量连回材料，改写可追溯，一致性问题可分级报告，审稿意见可逐条映射。

它当前覆盖四条核心工作流：

| 场景 | Skill | 作用 |
|------|-------|------|
| 材料散乱、事实与解释混在一起 | [`research-context`](.agents/skills/research-context/) | 整理为结构化研究记录，区分事实、解释、待核实与缺失项 |
| 段落流畅但证据稀薄 | [`evidence-writing`](.agents/skills/evidence-writing/) | 在证据约束下起草或改写，避免无据拔高结论 |
| 摘要、正文、图注、结论对不上 | [`manuscript-audit`](.agents/skills/manuscript-audit/) | 做一致性与证据风险审计（含可运行的启发式脚本检查） |
| 审稿意见多、修改难追踪 | [`review-response`](.agents/skills/review-response/) | 拆分意见并关联修改、证据与回复状态 |

四个 Skill 目前均为 **Draft**：流程与边界已写清，并配有本地结构验证与合成评测；**尚未**达到 Beta/Stable，也**未**完成大规模真实稿件验证。

## 它解决什么问题

科研场景里，通用写作助手常优化“读起来更顺”，却可能：

- 悄悄改掉样本量、数值或单位；
- 把相关说成因果，把趋势说成已证实；
- 让引文看起来很支撑，实际上并未核验；
- 直接覆盖原稿，事后难以交代改了什么。

ScholarlyOps 针对这些问题给出可检查的工作方式：

- **事实保真**：不为文采改动数据、设计、统计推断与结论强度。
- **证据可追溯**：重要主张尽量关联原文、图表、数据或文献位置；无法核查则明确标记。
- **修改可审计**：保留原文、修订、理由、证据与待确认项；默认生成新输出，不覆盖原稿。
- **工作流可测试**：Skill 结构可验证，确定性检查可回归；语义判断与脚本能力分开声明。

## 核心 Skills

| Skill | 中文名 | 职责摘要 | 成熟度 |
|-------|--------|----------|--------|
| [`research-context`](.agents/skills/research-context/) | 研究上下文整理 | 目标、设计、变量、结果、限制与待核实清单 | Draft |
| [`evidence-writing`](.agents/skills/evidence-writing/) | 证据约束写作 | 主张—证据映射下的起草与改写 | Draft |
| [`manuscript-audit`](.agents/skills/manuscript-audit/) | 论文一致性审计 | 跨章节一致性；数值/单位等启发式程序检查 + 语义复核指引 | Draft |
| [`review-response`](.agents/skills/review-response/) | 审稿意见回复 | 意见拆分、修改映射、状态与待作者决定项 | Draft |

成熟度定义见 [产品规格](docs/PRODUCT_SPEC.md)：`Draft` / `Beta` / `Stable`。当前无一 Skill 超过 Draft。

`manuscript-audit` 的本地脚本可检出部分**字面数值冲突**与**单位 token 冲突**，并区分格式差与四舍五入容差；这不等于完整的科研语义审计，也不能替代作者与领域专家判断。

## 快速开始（推荐：Agent 全局安装）

面向最终用户的主要方式：用官方 [`npx skills`](https://github.com/vercel-labs/skills) 把 Skills 装进 Cursor / Claude Code 的**个人全局**技能目录，跨项目复用。  
**不必**克隆本仓库，也**不必**把 Skill 复制进每个业务项目。

前置：Node.js 18+。需要跑 `manuscript-audit` 脚本时另需 Python 3.10+。

```bash
# 查看可安装的 Skills（本环境对 GitHub 源 --list：已发现 4 个）
npx skills add dxl11/scholarlyops-skills --list

# 全局安装单个 Skill（Cursor + Claude Code）
npx skills add dxl11/scholarlyops-skills --global --agent cursor claude-code --skill manuscript-audit

# 全局安装全部 Skills
npx skills add dxl11/scholarlyops-skills --global --agent cursor claude-code --skill '*'

# 查看 / 更新 / 卸载（示例）
npx skills list --global
npx skills update --global -y
npx skills remove manuscript-audit --global --agent cursor -y
```

仅 Cursor 或仅 Claude Code 时，把 `--agent` 改成单一目标即可。

然后打开**任意**工作项目：在 Cursor Agent 用 `/` 搜索或点名 Skill。  
**文件已安装 ≠ IDE 已加载**；Cursor 界面验收见 [cursor-smoke-test.md](docs/zh-CN/cursor-smoke-test.md)。Claude Code 加载仍**待你本机验证**。

- 完整说明（平台命令、项目级安装、排障）：[安装指南（中文）](docs/zh-CN/installation.md) · [Installation (English)](docs/en/installation.md)
- 维护者本地开发（非最终用户默认路径）：

```bash
git clone https://github.com/dxl11/scholarlyops-skills.git
cd scholarlyops-skills
python tools/validate_skills.py
```

### 使用示例（manuscript-audit）

1. 使用稿件副本，勿默认覆盖原稿。
2. 启用 `manuscript-audit`，提供摘要、相关正文、图注/表注与可选参考文献。
3. 阅读分级报告：Critical / Major / Minor / Needs Review，核对位置、证据与待确认项。

合成案例：[`evals/cases/manuscript-audit/`](evals/cases/manuscript-audit/)

## 项目状态与已知限制

> 本项目处于**开发中**。请勿将下列信息理解为已正式发布或已获认证。

- 全部 Skills 为 **Draft**；未做大规模真实论文验证。
- **许可证尚未确定**；在添加 `LICENSE` 之前，不得宣称 MIT、Apache-2.0 或其他许可证。见 [open-questions.md](docs/decisions/open-questions.md)。
- 正式 GitHub 远程地址、商标与品牌法律清核仍待确认；元数据见 [`project.json`](project.json)。
- `run_evals.py` 仅自动评分**确定性脚本**案例；需 Agent/人工的语义案例会 skip，**不**记为通过。
- `npx skills`（1.7.4）对本仓库的 **Skill 发现**（`--list` → 4 个）已验证；Cursor **全局安装落盘**曾在维护环境验证；**IDE `/` 菜单发现与调用**仍待按 smoke-test 确认。
- Claude Code：安装命令已按 CLI 给出，**安装与加载均待本机实测**；未宣称已支持其他网页/云端 Agent。
- 程序测试通过 ≠ 论文审计能力已充分验证；Agent 语义有效盲测不足时保持 Draft。见 [评测说明](evals/README.md)。
- 文献 API、自动投稿等**未实现**，仅列于 [路线图](docs/ROADMAP.md)。
- 安全披露途径见 [SECURITY.md](SECURITY.md)（GitHub 私密漏洞报告需维护者在网页端确认启用；**无**单独编造的安全邮箱）。

## 目录结构

```text
scholarlyops-skills/
├── README.md / README_EN.md
├── project.json                 # 品牌与元数据集中管理
├── .agents/skills/              # 标准 Skills 根目录
├── docs/                        # 产品、架构、安装、决策
├── evals/                       # 合成评测案例
├── tools/                       # validate_skills.py / run_evals.py
├── tests/
└── .github/workflows/
```

## 依赖与环境

- 使用 Skills：兼容 Agent（优先 Cursor）；无强制业务运行时。
- 运行仓库验证与本地评测：Python **3.10+**，仅标准库。

```bash
python tools/validate_skills.py
python -m unittest discover -s tests -v
python -m unittest discover -s .agents/skills/manuscript-audit/tests -v
python tools/run_evals.py
```

## 学术诚信与数据安全

- 不得伪造实验、数值、引文支持或“已完成修改”。
- 证据状态：`verified` / `partially_supported` / `unverified` / `unsupported` / `conflicting`。
- 引用分层核验：存在性 → 元数据 → 内容支持 → 论证恰当性。
- 私有稿件与输出目录由 `.gitignore` 保护；安全问题见 [SECURITY.md](SECURITY.md)。

## 贡献

欢迎改进文档、评测案例、验证工具与 Skill 指令。请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 相关文档

- [产品规格](docs/PRODUCT_SPEC.md) · [路线图](docs/ROADMAP.md)
- [架构（中文）](docs/zh-CN/architecture.md) · [Architecture (EN)](docs/en/architecture.md)
- [评测说明](evals/README.md) · [Cursor 验收](docs/zh-CN/cursor-smoke-test.md) · [更新日志](CHANGELOG.md)
- [English README](README_EN.md)
