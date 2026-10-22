# Changelog

本文件记录面向用户的显著变更。版本号与发布节奏尚未最终确定（见 `docs/decisions/open-questions.md`）。

格式参考 [Keep a Changelog](https://keepachangelog.com/)。正式 `0.1.0` 发布前以 **Unreleased** 汇总；**不要**假装已有正式历史版本。

## [Unreleased]

### Added

- 新 Skill（Draft）：`literature-search` — 文献检索策略规划（Stage 1–7、Strategy Only / Search Assisted、分库检索式参考、10 个合成评测案例）。
- ScholarlyOps 项目初始化：品牌元数据 `project.json`、中英文 README。
- 文档：安装与架构（中/英）、产品规格、路线图、开放问题、贡献与安全说明。
- 第一批 Skills（均为 Draft）：`research-context`、`evidence-writing`、`manuscript-audit`、`review-response`。
- `manuscript-audit` 示范流程、参考规范、程序检查脚本与合成评测案例。
- 标准库验证工具 `tools/validate_skills.py`、单元测试与 GitHub Actions 工作流。
- 安全基线：`.gitignore`、`.env.example`、`SECURITY.md`。
- Phase 2：`tools/run_evals.py` 可重复本地评测；案例扩展至 17 个；数值脚本区分格式/四舍五入/字面冲突。
- Cursor 人工验收指南：`docs/zh-CN/cursor-smoke-test.md`、`docs/en/cursor-smoke-test.md`。
- Agent 语义盲测协议：`docs/zh-CN/agent-evaluation-guide.md`、`docs/en/agent-evaluation-guide.md`；`evals/agent-semantic/`（blind-set、rubric、scorecard）；`tools/prepare_agent_blind_pack.py`（隔离输入、禁止复制 expect）。

### Changed

- 安装体验：README / 安装指南改为 **「让 Agent 帮你安装」优先**，其次原生平台路径，CLI `npx skills` 为备用；新增可复制安装指令；记录 Codex `$skill-installer`、Cursor/Claude 全局目录与 Marketplace 要求；暂缓未验证插件 Manifest（见 `docs/decisions/plugin-distribution.md`）。
- 发布准备：中英文 README / 安装指南统一全局安装示例；核实 CLI 1.7.4。
- `SECURITY.md`：不以编造邮箱为披露渠道；说明 GitHub 私密漏洞报告须维护者在网页端启用；补充发布前安全清单。
- `docs/decisions/open-questions.md`：保留许可证待决及 MIT / Apache-2.0 决策对照；补充维护者发布待办。


- `manuscript-audit` 指令明确证据状态、严重程度与脚本能力边界；语义案例不得被本地运行器标为通过。
- **安装主路径改为 Agent 全局安装**（`npx skills add … -g`）；项目级复制改为可选。README 与中英文安装/验收文档已同步。
- 保留单一权威源 `.agents/skills/`（`npx skills --list` 已验证可发现 4 个 Skill）。
- **数值/单位检测器改为候选异常报告**：保留行号与上下文；不再将字面差异自动标为 Critical/`verified`；跨组/时间点与 μ/µ/u 别名进入 tolerated；评测扩展至 24 案例。

### Notes

- 许可证未选定；无 `LICENSE` 文件。
- 轻量级名称检索结果记入 `project.json` 与开放问题文档（非商标法律意见）。
- Cursor Skill 加载仍待用户在 IDE 中确认。
