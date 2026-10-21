# 架构说明 · ScholarlyOps

[English](../en/architecture.md) | 简体中文

## 1. 产品目标与非目标

**目标**：以科研证据为核心，提供可扩展、可独立安装、可测试的 Agent Skills，覆盖材料整理、证据写作、全文审计、审稿回复等任务。

**非目标**：替代研究者的科学判断；无人复核的自动发表；虚构实验结果；未授权复制第三方 Skills 仓库。

## 2. 用户与场景

见 [产品规格](../PRODUCT_SPEC.md)。核心场景：投稿前自查、证据约束改写、审稿意见闭环。

## 3. Skill 职责与触发边界

| Skill | 何时触发 | 何时不应触发 |
|-------|----------|--------------|
| `research-context` | 用户要整理杂乱研究材料为结构化记录 | 用户只要润色一段已定稿文字 |
| `evidence-writing` | 基于已有证据起草/改写段落 | 用户要求“编造数据让结果显著” |
| `manuscript-audit` | 检查跨章节一致性与证据风险 | 用户只要生成全新无关章节 |
| `review-response` | 处理审稿意见与回复草稿 | 用户尚未提供任何审稿意见 |

## 4. 共享规范与独立 Skill

- **权威规范**维护在 `docs/PRODUCT_SPEC.md` 与本架构文档。
- **运行时需要的规则**必须随 Skill 打包（例如 `references/integrity.md`），以便单独复制后仍可用。
- 品牌字符串集中在 `project.json`，文档引用该来源，避免名称漂移。

## 5. 输入、输出与错误处理

各 Skill 的 `SKILL.md` 定义契约。共通规则：

- 输出须含限制声明与待作者确认项（如适用）。
- 材料不足 → 降级证据状态，不补造。
- 默认写入新文件或报告，不覆盖原稿。

## 6. 程序检查 vs 语义判断

`manuscript-audit` 将数值/单位等可确定差异优先交给 `scripts/`；因果表述、引文支持性等由模型标注位置与理由，并标为 Needs Review 或相应严重度，禁止无证据的“已确认错误”。

## 7. 文件组织

```text
.agents/skills/<skill-name>/
├── SKILL.md           # 必需
├── references/        # 按需
├── scripts/           # 按需；相对路径调用
├── examples/          # 按需
└── tests/             # 按需（Skill 内单元级）
```

引用检查由 `tools/validate_skills.py` 执行：本地相对路径须存在；禁止依赖其他 Skill 内部文件作为运行时必需；禁止本机绝对路径。

## 8. 添加、测试、更新、发布

1. 按 [CONTRIBUTING.md](../../CONTRIBUTING.md) 新增 Skill。  
2. 运行 `python tools/validate_skills.py` 与单元测试。  
3. 合成评测放入 `evals/`。  
4. 成熟度升级必须有测试/试跑记录。  
5. 正式发布依赖许可证与远程仓库决策（见开放问题）。

## 9. 中英文文档同步

- README、安装、架构成对维护。
- 变更功能列表或限制时同步两边。
- 验证工具检查 README 关键内部链接。

## 10. 安全审核与回归

- 变更后运行验证与相关评测。
- CI：`.github/workflows/validate.yml`（无外部密钥）。
- 秘密扫描：人工检查 + 忽略规则；已跟踪秘密须维护者处置。

## 11. 分发与安装架构

- **权威源码**：仓库内 `.agents/skills/`（单一来源，可被 `npx skills` 发现）。
- **最终用户主路径**：Agent **全局安装**（`npx skills add <owner>/<repo> -g`），跨项目复用。
- **项目级安装**：可选，用于团队锁定版本；非使用前提。
- **开发者**：克隆本仓库跑验证与评测。

详见 [installation.md](installation.md)。

## 12. 当前实现、规划与限制

**已实现**：文档骨架；四 Skill Draft；`manuscript-audit` 示范脚本与合成案例；仓库验证器与 CI；`npx skills` 发现与 Cursor 全局落盘验证记录。

**规划**：Phase 3–6 见 [ROADMAP.md](../ROADMAP.md)。

**限制**：均为 Draft；无完整 YAML 解析；Cursor IDE `/` 加载与 Claude Code 仍待用户侧确认；许可证未定。
