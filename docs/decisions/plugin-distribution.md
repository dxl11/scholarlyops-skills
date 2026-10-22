# 决策记录 · 原生插件 / Marketplace 分发

**状态**：评估完成，**暂缓提交**未验证的插件 Manifest  
**日期**：2026-10-22  
**权威 Skill 源**：始终为仓库 `.agents/skills/`（禁止长期人工双份 `SKILL.md`）

## 背景

用户期望 Cursor / Claude Code 具备「官方插件市场」式安装。官方文档要求：

| 平台 | 从 GitHub 以插件方式分发时通常需要 | 资料 |
|------|-------------------------------------|------|
| Cursor | 插件 Manifest（Agent Plugin 根级 `plugin.json` 或 Cursor Plugin `.cursor-plugin/plugin.json`）；经 Marketplace / From GitHub 导入时常需 `.cursor-plugin/marketplace.json` | [Cursor Skills](https://cursor.com/docs/skills)、[Cursor Plugins](https://cursor.com/docs/plugins) |
| Claude Code | Marketplace 仓含 `.claude-plugin/marketplace.json`；插件内再挂 `skills/` | [Claude Code Skills](https://code.claude.com/docs/en/skills)、[Plugins](https://code.claude.com/docs/en/plugins/overview) |
| Codex | 当前可用 `$skill-installer` 按 GitHub **Skill 目录 URL** 装入 `~/.codex/skills/`；另有 Plugins 方向（`openai/skills` 已标 deprecated） | [skill-installer](https://github.com/openai/skills/blob/main/skills/.system/skill-installer/SKILL.md) |

## 决策

1. **现在不**向仓库添加未在本机/官方流程实测通过的 `.cursor-plugin/*`、`.claude-plugin/*` 或根级 `plugin.json`。  
2. 最终用户首选：**让 Agent 安装**到用户级全局目录，或 **CLI** `npx skills add … --global`。  
3. 若日后要做 Marketplace：编写**自动打包脚本**，从 `.agents/skills/` 生成插件布局（复制或链接），在 CI 中校验 Manifest，并在真实 Cursor/Claude 中完成一次安装实测后再宣称「支持插件安装」。  
4. Codex 继续文档化 `$skill-installer` +  
   `https://github.com/dxl11/scholarlyops-skills/tree/main/.agents/skills/<skill-name>`  
   （需用户在 Codex 内实测）。

## 非目标（当前）

- 声称已在 Cursor Marketplace / Claude Marketplace 上架  
- 把「复制文件到全局目录」说成「原生插件市场安装」  
- 默认项目级安装  

## 后续触发条件

当维护者完成：自动打包 + 至少一次 Cursor「From GitHub」或 Claude `/plugin` 实测通过 → 再提交 Manifest，并更新安装文档验证表。
