# 开放问题 · ScholarlyOps

**不要把下列选项写成既定事实。**

## 1. 正式 GitHub 仓库地址

- 当前本机 `git remote` 与 `npx skills add … --list` 已指向：`dxl11/scholarlyops-skills`（`https://github.com/dxl11/scholarlyops-skills`）
- 是否为最终对外品牌账号 / 是否迁移组织：仍可由维护者确认
- 文档安装命令已使用上述标识；若迁移仓库须同步替换

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

- 推荐安装器：`npx skills`（已验证可发现本仓库 4 个 Skills；支持 `-g`）。
- Cursor 全局安装落盘：本环境实测为 `~/.agents/skills/`（以 CLI `list -g` 的 `path` 为准）。
- Claude Code：命令已写，**加载未实测**。
- 其他 Agent：仅计划支持。

## 7. Cursor IDE 加载实测

- 终端：`npx skills` 发现 + Cursor 全局安装落盘 → **已验证**（见安装文档验证表）。
- IDE：`/` 菜单发现、跨项目调用、语义执行 → **待**按 `docs/zh-CN/cursor-smoke-test.md` 勾选。
- 仓库权威源码仍为 `.agents/skills/`（单一来源）；最终用户主路径为 Agent **全局安装**，项目级安装为可选。

## 8. Agent 语义盲测实测

- 协议与工具已就绪：`docs/*/agent-evaluation-guide.md`、`evals/agent-semantic/`、`tools/prepare_agent_blind_pack.py`。
- Wave A（7 个 `agent_semantic` 案例）的**有效盲测分数：尚未执行**；不得虚构结果。
- 在有效样本量不足前，`manuscript-audit` 保持 Draft，不得据此升 Stable/Beta。
