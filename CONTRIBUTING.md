# 贡献指南 · ScholarlyOps

感谢关注 **ScholarlyOps**（学术研究工作流 Skills）。贡献须可审查、可复现，并遵守学术完整性。

## 行为准则（简版）

- 不以夸大结果、伪造数据或误导性引文为目标。
- PR 说明动机、范围与验证方式。
- 不提交密钥、未脱敏私有数据或未经授权的论文全文。

## 开始之前

1. 阅读 [README.md](README.md)、[docs/PRODUCT_SPEC.md](docs/PRODUCT_SPEC.md)、[docs/zh-CN/architecture.md](docs/zh-CN/architecture.md)。
2. 品牌与元数据以 [`project.json`](project.json) 为准；避免散落硬编码不一致名称。
3. 查看 [docs/decisions/open-questions.md](docs/decisions/open-questions.md)（许可证、仓库地址等）。
4. 第三方材料必须先确认许可证并注明来源。

## 开发环境

- Python 3.10+（验证与测试仅标准库）
- Node.js 18+（可选；用于 `npx skills` 验证发现/安装）
- Cursor 或其他兼容 Agent（可选）

```bash
python tools/validate_skills.py
python -m unittest discover -s tests -v
python -m unittest discover -s .agents/skills/manuscript-audit/tests -v
python tools/run_evals.py
npx skills add . --list
```

说明：

- 最终用户主路径是 **Agent 全局安装**，见 [docs/zh-CN/installation.md](docs/zh-CN/installation.md)。
- 权威 Skill 源只在 `.agents/skills/`；不要另维护一套需手工同步的副本。
- `run_evals.py` 对 `agent_semantic` 案例会 skip，不得把 skip 写成 pass。

## 创建新 Skill

1. 在 `.agents/skills/<skill-name>/` 新建目录（功能导向命名；**不要**强制加 `scholarlyops-` 前缀）。
2. 编写 `SKILL.md`：Frontmatter 含 `name`、`description`；`name` 与目录名一致；仅小写字母、数字、连字符。
3. 写清：输入、步骤、输出、异常、限制、成熟度（默认 Draft）。
4. 长规范放入 `references/`；脚本相对 Skill 根目录引用，禁止本机绝对路径。
5. 独立安装后必须可运行：不得依赖安装后不存在的仓库其他文件。
6. 更新 README（中英文）技能表、架构文档；如适用补充 `evals/`。
7. 运行验证工具；不要无证据将成熟度标为 Beta/Stable。

## 修改现有 Skill

- 保持职责边界；冲突指令需先讨论。
- 变更输出契约时同步更新示例与评测期望。
- 重要规则变更后运行相关检查，防止回归。

## 编写测试用例

- 优先合成案例或已确认可公开的材料。
- 每个案例说明：输入、预期发现、可接受输出、不可接受错误。
- 包含无问题对照样例，避免“凡文必报错”。
- 评测说明写入 `evals/README.md` 与案例旁的 `expected` 说明。

## 更新中英文文档

- 中英文 README / 安装 / 架构须保持核心内容同步。
- 品牌名、副标题与 `project.json` 一致。
- 不虚构已完成功能、测试成绩或许可证。

## 第三方知识、脚本、数据与模板

- 记录来源、许可证、署名要求。
- 不得整仓复制其他公开 Skills 仓库后当作原创发布。
- 许可证未定时，贡献物最终授权条款仍待维护者确认。

## 问题报告与功能建议

- Bug：复现步骤、期望/实际、相关 Skill 与验证命令输出摘要。
- 功能：场景、非目标、是否可用合成评测验收。
- 安全问题优先按 [SECURITY.md](SECURITY.md) 私下报告。

## Pull Request 建议

- 单一主题；附验证命令结果摘要。
- 不跳过失败测试、不伪造通过。

## 许可证

项目许可证尚未确定。详见开放问题文档。
