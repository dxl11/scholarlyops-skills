# 开放问题 · ScholarlyOps

**不要把下列选项写成既定事实。**

## 1. 正式 GitHub 仓库地址

- 当前本机 `git remote` 与 `npx skills add … --list` 已指向：`dxl11/scholarlyops-skills`（`https://github.com/dxl11/scholarlyops-skills`）
- 是否为最终对外品牌账号 / 是否迁移组织：仍可由维护者确认
- 文档安装命令已使用上述标识；若迁移仓库须同步替换

## 2. 许可证（须由项目所有者决定）

当前**没有** `LICENSE` 文件。自动化助手**不得**擅自创建 `LICENSE`，也**不得**宣称已采用任一许可证。

| 选项 | 主要差别（仅供决策讨论，非法律意见） |
|------|--------------------------------------|
| MIT | 宽松、文本短；几乎无专利授权条款；再分发保留版权与许可声明即可；适合希望被广泛复用的库 |
| Apache-2.0 | 含**专利授权**与侵权诉讼时的专利许可终止条款；要求保留 NOTICE/归属；对贡献与再分发记录要求更明确 |
| 其他 | 需单独评估（含与依赖、合成案例、第三方引用材料的兼容性） |

正式公开发布 / 打 tag 前必须：

1. 所有者选定许可证并添加根目录 `LICENSE`（及如需的 NOTICE）；
2. 确认贡献者理解贡献将按该许可证授权；
3. 核查原创文本与脚本、合成案例、第三方材料的许可证与署名。

**在添加 `LICENSE` 前，不得对外声称已采用 MIT、Apache-2.0 或其他许可证。**

## 3. 商标与品牌核查

- 开发阶段统一品牌名：ScholarlyOps
- 轻量级检索（2026-10-21，搜索引擎/GitHub 公开结果）：
  - 未发现名为 `scholarlyops-skills` 的精确仓库命中
  - 未发现同名 ScholarlyOps Skills 产品；存在近音/近义项目（如 OpenScholarOPS、scholarly 包、其他 academic skills 仓库），**不构成清核结论**
- **待办**：正式发布前完成商标与域名可用性法律核查（本检索不能替代）

## 4. 发布方式与安全入口

- 首个 tag 版本号
- 是否上架第三方技能目录（均未验证）
- **不要编造安全联系邮箱**；优先启用 GitHub 私密漏洞报告（见 `SECURITY.md`）
- 维护者须在 GitHub **网页端**确认/启用 Private vulnerability reporting（无法从本仓库文件判定是否已开）

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
- Wave A：7 案有原始报告与**内容**评分卡，但因会话污染，按 rubric 的**有效盲测 = 0**（见 `evals/agent-semantic/results/wave-a-summary.md`）。
- 不得把内容练习分当作有效盲测通过；在有效样本量不足前，`manuscript-audit` 保持 Draft，不得升 Stable/Beta。

## 9. 正式发布前维护者待办（摘要）

- [ ] 选定并添加 `LICENSE`
- [ ] GitHub：启用/确认私密漏洞报告
- [ ] Cursor IDE smoke-test 勾选（`docs/zh-CN/cursor-smoke-test.md`）
- [ ] Claude Code 安装与加载实测并回写安装文档验证表
- [ ] Codex `$skill-installer` + 本仓库 Skill 目录 URL 实测
- [ ] （可选）按 [plugin-distribution.md](plugin-distribution.md) 自动打包并实测后再提交插件 Manifest
- [ ] 商标/品牌法律清核（如需对外运营品牌）
- [ ] 有效 Agent 语义盲测达到可辩护样本量后再考虑升成熟度
