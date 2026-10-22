---
name: literature-search
description: >-
  Plan structured literature search strategies from fuzzy research ideas:
  clarify questions, build synonym matrices (without inventing verified MeSH/Emtree),
  recommend databases, and draft database-specific queries (PubMed, Scopus,
  Web of Science, Google Scholar basics). Use when the user lacks keywords,
  needs English synonyms, does not know which databases to use, needs PubMed/Scopus
  query strings, must refine too-few/too-many results, prepare a reproducible
  review search plan, or expand terms from known seed papers. Default is Strategy
  Only (no fabricated hit counts); Search Assisted only when real search tools
  and access are available.
---

# literature-search · 文献检索策略规划

**成熟度**：Draft（流程 + 参考规范 + 合成案例；真实库执行与大规模用户验证待完成）  
**品牌**：ScholarlyOps（本 Skill 可独立安装；不依赖仓库其他文件）  
**输出默认**：新文件，例如 `literature_search_strategy.md`（不覆盖用户原稿）

## 何时使用

在用户需要以下帮助时启用本 Skill（勿仅凭名称触发）：

- 不知道如何为研究主题选择检索关键词  
- 只有初步想法，需转化为结构化研究问题  
- 需要构建英文同义词与相关术语，且区分同义 vs 相邻概念  
- 不知道应使用哪些学术数据库 / 平台 / 搜索引擎  
- 需要 **PubMed、Scopus、Web of Science、Google Scholar** 等对应语法的检索式  
- 结果太少、太多或相关性差，需要迭代优化策略  
- 为叙述性综述、范围综述或系统综述建立**可追溯**检索方案  
- 已有种子论文，希望从中扩展关键词与检索路径  

## 不负责

- 虚构命中数、题名、DOI、筛选结果或“已在某库执行”的状态  
- 编造已核实的 MeSH / Emtree / CINAHL Headings 等受控词（无法核验则标 `待核实`）  
- 声称单一数据库覆盖整个学科，或假定用户拥有全部数据库权限  
- 仅生成一条检索式即宣称符合完整系统综述检索要求  

## 执行模式

### Mode A — Strategy Only（默认）

生成结构化检索策略与**可粘贴的查询草案**。  
不访问数据库；不得填写真实命中数或执行状态为“已完成检索”。  
记录状态写：`strategy_draft` / `pending_execution`。

### Mode B — Search Assisted（仅当工具真实可用）

仅当当前 Agent **确实**具备浏览器、官方 API 或其他适用检索工具，**且**用户可访问目标库时使用。  
必须分项标明：已生成检索式 / 已提交查询 / 已读取部分结果 / 已筛选 / 未执行。  
无权限或无工具 → **退回 Mode A** 并说明原因。  
**禁止**虚构任何执行结果。

## 工作流程（必须按阶段）

### Stage 1 — 理解研究问题

提取：主题、对象、核心问题、变量/干预/现象、场景、设计或证据类型、用途（探索 / 综述 / 系统综述等）、时间/语言/地域限制。

信息不完整时：**先**用合理假设给出初步方案，并标注假设与待确认项。  
仅当缺失会**显著改变**策略时，提出最少澄清问题（勿连环追问）。

### Stage 2 — 选择问题框架

按问题类型选择，**禁止**一律套 PICO：

| 框架 | 适用提示 |
|------|----------|
| PICO / PICOS | 干预、比较、结局较清晰的定量问题 |
| PEO | 人群—暴露—结局/经验类问题 |
| SPIDER | 部分定性或混合方法问题 |
| 学科特定框架 | 说明来源与适用边界 |
| 非结构化概念抽取 | 探索性研究可不强制框架 |

说明：为何选该框架、哪些槽位仍不确定。

### Stage 3 — 关键词矩阵

对每个核心概念分别整理：主术语、同义词、缩写/全称、英美拼写、单复数与词形、上/下位与相关词、学科词、**已核实**的受控词。

必须区分：

- 真正同义 / 近义可 OR  
- 较宽泛概念  
- 相邻但**不等价**的术语（勿自动并入同义 OR）

受控词无法当场核验 → `unverified_controlled_vocabulary`，不得标为已验证 MeSH 等。

### Stage 4 — 推荐数据库

按学科、问题类型、用途、文献类型与**用户可能权限**推荐。区分：

- **数据库**（如 MEDLINE via PubMed、Scopus 内容集合）  
- **检索平台**（如 Ovid、EBSCOhost、出版社平台）  
- **搜索引擎**（如 Google Scholar）  

示例候选（非强制清单）：医学生命科学 → PubMed / Embase / CINAHL；工程计算机 → IEEE / ACM；心理教育社科 → PsycINFO / ERIC；跨学科 → Scopus / Web of Science；初步探索 → Google Scholar。  
说明推荐理由与访问不确定性；不声称学科穷尽覆盖。

### Stage 5 — 生成分库检索式

- 概念内相关词 **OR**，概念间按问题用 **AND**（或库支持的邻近算子）。  
- **勿**机械把所有结局、设计标签都强制 AND 进式子；题名/摘要常缺失的概念可降低强制程度以保持敏感性。  
- **每个目标库单独一条式子**，禁止把 PubMed 语法原样贴到 Scopus。  

**初始优先并标注语法状态的目标：**

| 目标 | 初始支持 | 语法验证状态 |
|------|----------|--------------|
| PubMed | 完整草案（字段、布尔、短语、截词、邻近要点） | `syntax_checked_against_official_help`（见 references；界面变更时需复核） |
| Scopus Advanced | `TITLE-ABS-KEY` 等字段码草案 | 同上 |
| Web of Science | `TS=` 等字段标签草案 | 同上 |
| Google Scholar | 基础布尔/短语策略（功能有限） | `partial` — 界面与运算符行为与专业库不同 |
| 其他库（Embase、CINAHL、IEEE…） | 术语与逻辑骨架 | `needs_syntax_adaptation` — 未核实前不得伪装为可直接执行 |

核对要点：字段标签、布尔与括号、短语、截词/通配、邻近、自动词映射、特殊字符、长度/复杂度限制。详见 [references/database-guides.md](references/database-guides.md)。

### Stage 6 — 迭代策略

**太少**：是否 AND 过多；扩展真同义/拼写；查受控词；采用种子文献实际用语；放宽字段。  
**太多**：宽泛词噪声；收紧至题名/摘要/关键词；调整概念组合；用邻近算子；仅在有充分理由时加排除。  
不得仅凭主观感觉随意删词。

### Stage 7 — 检索记录

正式检索记录字段：数据库名、平台、日期、完整检索式、过滤器、结果数量、修改史、备注/未决问题。  

- 未实际执行 → 明确 `strategy_draft`；结果数量留空或 `NOT_EXECUTED`。  
- 仅 Mode B 且真实执行后才填命中数与执行状态。  
- 系统综述场景：提醒保存完整记录并参考 **PRISMA-S** 等报告原则；**生成策略 ≠ 已满足完整系统综述检索**。

## 输出契约

完整输出（系统综述或用户要求完整方案时）：

```markdown
# Literature Search Strategy

## Meta
- Skill: literature-search (Draft)
- Mode: Strategy Only | Search Assisted
- Execution status: strategy_draft | queries_submitted | …

## 1. Research question understanding
## 2. Assumptions and items to confirm
## 3. Question framework and rationale
## 4. Concept & keyword matrix
## 5. Term relationship notes (synonym vs related vs broader)
## 6. Recommended databases / platforms / engines
## 7. Database-specific search strings
## 8. Syntax validation status and unverified items
## 9. Iteration advice (too few / too many)
## 10. Search log template
## 11. Next steps
## Limits
```

简单探索：可输出简化版（问题理解、关键词、1–2 个库的草案、下一步），仍须标明 Mode 与未执行状态。

## 与其他 Skill

- 可接收 `research-context` 的结构化主题作为输入。  
- 检索方案确定后，可用 `evidence-writing` / `manuscript-audit` 处理写作与一致性；本 Skill **不**替代引文内容核验。  
- 均可独立安装运行。

## 异常处理

| 情况 | 行为 |
|------|------|
| 主题极度模糊 | 假设 + 待确认；给探索性宽检索与收窄路径 |
| 用户要求编造命中数 | 拒绝；保持 Mode A |
| 用户坚持混用库语法 | 拒绝混用；分库重写并说明差异 |
| 无库权限却要求 Mode B | 退回 Mode A |
| 要求“保证系统综述合规” | 提供可复现模板与提醒；不保证合规认证 |

## 限制

- Draft：语法摘要可能落后于数据库界面更新；执行前请对照官方帮助复核。  
- 不替代图书馆员正式系统综述检索咨询。  
- 独立安装时仅依赖本目录文件。  
- 本地合成案例为 `agent_semantic` / 人工核对；**不得**把未执行检索标为 pass。  

## 参考与示例

- [references/database-guides.md](references/database-guides.md)  
- [references/search-strategy-methods.md](references/search-strategy-methods.md)  
- [examples/strategy_draft_snippet.md](examples/strategy_draft_snippet.md)  
