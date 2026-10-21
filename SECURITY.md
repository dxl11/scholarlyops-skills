# 安全政策 · ScholarlyOps

## 支持范围

本项目处于早期开发阶段，当前**无**托管后端服务。主要风险包括：

- 仓库中意外提交的凭据、令牌或私钥
- 指引导致用户泄露敏感研究数据或可识别个人信息
- 不受信任的外部脚本、安装源或依赖
- 本地验证/评测工具中的路径或输入处理风险（如有）

四个 Skills 均为 **Draft**：程序检查与合成评测通过，**不等于**科研审计能力已充分验证。

## 如何报告安全问题

**请勿**在公开 Issue / PR / 讨论中粘贴真实密钥、令牌、Cookie、私有稿件或未脱敏数据。

### 推荐途径（GitHub）

1. 优先使用 GitHub **私密漏洞报告**（Private vulnerability reporting / Security advisories），以便维护者私下协调修复。
2. 该功能必须在仓库的 **Settings → Security → Code security → Private vulnerability reporting**（界面名称可能随 GitHub 更新变化）中由维护者**确认或启用**。
3. **本仓库无法从源码文件判断该开关当前是否已开启。** 若你无法看到 “Report a vulnerability” 入口，请：
   - 暂时用最少非敏感信息开 Issue，标题标明 `[SECURITY]`，**不要**附密钥原文；或
   - 等待维护者在网页端启用私密报告后再提交详情。

官方说明见 GitHub 文档：[Privately reporting a security vulnerability](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-security-advisories/privately-reporting-a-security-vulnerability)。

### 报告内容建议

仅包含：

- 受影响文件**路径类型**（勿贴秘密原文）
- 风险类型（如“疑似密钥被跟踪”“路径穿越”）
- 最少非敏感复现步骤
- 影响范围估计（本地 / 贡献者 / 最终用户）

**本文件不提供单独编造的安全联系邮箱。** 若维护者日后公布专用邮箱，将在此更新；在未公布前，以 GitHub 私密漏洞报告或上述降级流程为准。

## 敏感信息与操作

| 类别 | 要求 |
|------|------|
| API Key / Token | 仅放本地 `.env`；示例只用占位值（见 `.env.example`） |
| 私有稿件 / 原始数据 | 放入 `.gitignore` 保护的目录；公共评测只用合成或已确认可公开材料 |
| 外部 API | Skills **不得**默认上传用户稿件；若未来接入，须事先说明费用、数据出境与用户确认 |
| 外部脚本 / `npx skills` | 审查安装源（推荐 `dxl11/scholarlyops-skills`）；本仓库脚本应可静态阅读 |

## 为何仅改 `.gitignore` 不够

若秘密已被 Git **跟踪**或进入历史，忽略规则不会删除历史对象。需要：

1. 立即轮换已泄露凭据；
2. 从索引移除并提交清理（由维护者执行）；
3. 必要时历史清理（**高风险**，须维护者明确授权；贡献者不得擅自重写历史）。

## 私人研究数据与用户稿件

- Skills 默认生成新输出或差异报告，不覆盖原稿。
- 不鼓励将可识别个人信息写入公共评测集。
- Agent 会话可能把上下文发给模型提供商：用户须自行评估合规与同意。

## 依赖与 CI

- 当前验证与评测工具以 Python **标准库**为主，降低供应链风险。
- GitHub Actions 工作流（`.github/workflows/validate.yml`）使用 `permissions: contents: read`，仅运行校验与测试，不发布密钥。
- 若未来引入第三方包：锁定版本、说明用途、评估许可证与网络行为。

## 维护者发布前安全检查清单（网页端 / 本地）

下列项**无法**仅靠本仓库文件自动完成：

- [ ] 在 GitHub 仓库设置中确认或启用 **Private vulnerability reporting**
- [ ] 确认 Issues / Security 面板对报告者可见入口
- [ ] 扫描是否误提交 `.env`、密钥文件或私有稿件（勿在公开渠道粘贴发现的秘密原文）
- [ ] 确认 `.gitignore` 仍覆盖密钥、`private` 数据目录与本地输出
- [ ] 决定并添加 `LICENSE`（当前未选定；见 `docs/decisions/open-questions.md`）

## 处理原则

- 确认收到目标：≤ 7 天（当前无正式 SLA，尽力而为）。
- 公开披露前与报告者协调。
