# 开放问题 · ScholarlyOps

**不要把下列选项写成既定事实。**

## 1. 正式 GitHub 仓库地址

- 建议仓库名：`scholarlyops-skills`（见 `project.json`）
- 组织/个人账号归属：未定
- 远程 URL：未定

文档中的 `<YOUR_REPO_URL>` 为占位。

## 2. 许可证

当前**没有** `LICENSE` 文件。

| 选项 | 主要差别（讨论用） |
|------|-------------------|
| MIT | 宽松、简短；专利条款弱；需贡献者同意 |
| Apache-2.0 | 含专利授权与终止条款；NOTICE/归属要求更明确 |
| 其他 | 需单独评估 |

发布前还须核查：原创文本与脚本、合成案例、第三方引用材料的许可证与署名。

**在添加 `LICENSE` 前，不得对外声称已采用任一许可证。**

## 3. 商标与品牌核查

- 开发阶段统一品牌名：ScholarlyOps
- 轻量级检索（2026-10-21，搜索引擎/GitHub 公开结果）：
  - 未发现名为 `scholarlyops-skills` 的精确仓库命中
  - 未发现同名 ScholarlyOps Skills 产品；存在近音/近义项目（如 OpenScholarOPS、scholarly 包、其他 academic skills 仓库），**不构成清核结论**
- **待办**：正式发布前完成商标与域名可用性法律核查（本检索不能替代）

## 4. 发布方式

- 首个 tag 版本号
- 是否上架第三方技能目录（均未验证）
- 安全披露联系邮箱

## 5. 第三方 API 集成

文献 DOI/全文 API、模型云服务等：是否引入、费用、密钥与数据出境边界均未定。当前验证**不依赖**外网 API。

## 6. 其他 Agent 专用安装插件

Cursor 以 `.agents/skills/` 为仓库标准。其他 Agent 的真实路径与加载方式**未经本项目实测**；安装文档中仅可作为“待验证扩展”，不得写“已支持”。

## 7. Cursor 加载实测

是否在维护者本机 Cursor 中确认 Skills 被识别：待用户/维护者在 IDE 内验证。仓库结构符合公开文档所述路径约定，但**不等于**已完成加载实测。

验收步骤见：

- `docs/zh-CN/cursor-smoke-test.md`
- `docs/en/cursor-smoke-test.md`

官方文档同时列出 `.agents/skills/` 与 `.cursor/skills/`。本仓库以 `.agents/skills/` 为唯一源码树。社区曾报告部分版本 `/` 调用对 `.agents/skills` 不稳定——若复现，记录 Cursor 版本后再决定是否增加临时对照路径（仍避免双份源码长期并存）。
