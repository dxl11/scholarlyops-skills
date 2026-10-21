# Agent 语义评测（盲测）

本目录定义 **manuscript-audit** 的 Agent/人工语义评测协议。  
**不含**任何虚构的实测分数。`results/` 仅在真实盲测评分后写入。

| 文件 | 用途 |
|------|------|
| `blind-set.json` | 覆盖映射与推荐 Wave A/B 案例列表 |
| `rubric.md` | 评分细则 |
| `scorecard-template.json` | 单案例评分卡模板 |
| `results/` | 已评分 scorecard（gitignore 实际运行目录可选） |

## 快速流程

1. 准备盲测包（**不含** expect）：  
   `python tools/prepare_agent_blind_pack.py --wave wave_a_semantic_core --out <仓库外目录>`
2. 在 Cursor 中对新工作区**每个案例开新会话**，只给 `input.md` + `TASK.md`。
3. 保存原始输出到该案例目录的 `raw_agent_output.md`。
4. **另开**评分步骤：对照仓库 `expect.json` / `evals/expected/`，填写 scorecard。
5. 汇总时分开报告：程序测试 vs Agent 语义测试。

详见：

- [中文指南](../../docs/zh-CN/agent-evaluation-guide.md)
- [English guide](../../docs/en/agent-evaluation-guide.md)
