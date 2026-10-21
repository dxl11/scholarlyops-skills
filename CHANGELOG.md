# Changelog

本文件记录面向用户的显著变更。版本号与发布节奏尚未最终确定（见 `docs/decisions/open-questions.md`）。

格式参考 [Keep a Changelog](https://keepachangelog.com/)。正式 `0.1.0` 发布前以 **Unreleased** 汇总；**不要**假装已有正式历史版本。

## [Unreleased]

### Added

- ScholarlyOps 项目初始化：品牌元数据 `project.json`、中英文 README。
- 文档：安装与架构（中/英）、产品规格、路线图、开放问题、贡献与安全说明。
- 第一批 Skills（均为 Draft）：`research-context`、`evidence-writing`、`manuscript-audit`、`review-response`。
- `manuscript-audit` 示范流程、参考规范、程序检查脚本与合成评测案例。
- 标准库验证工具 `tools/validate_skills.py`、单元测试与 GitHub Actions 工作流。
- 安全基线：`.gitignore`、`.env.example`、`SECURITY.md`。
- Phase 2：`tools/run_evals.py` 可重复本地评测；案例扩展至 17 个；数值脚本区分格式/四舍五入/字面冲突。
- Cursor 人工验收指南：`docs/zh-CN/cursor-smoke-test.md`、`docs/en/cursor-smoke-test.md`。

### Changed

- `manuscript-audit` 指令明确证据状态、严重程度与脚本能力边界；语义案例不得被本地运行器标为通过。

### Notes

- 许可证未选定；无 `LICENSE` 文件。
- 轻量级名称检索结果记入 `project.json` 与开放问题文档（非商标法律意见）。
- Cursor Skill 加载仍待用户在 IDE 中确认。
