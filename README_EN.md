<div align="center">

<img src="assets/scholarlyops-logo.jpg" alt="ScholarlyOps" width="280" />

# ScholarlyOps

### More rigorous research writing. Claims grounded in evidence.

Academic Research Workflow Skills — an extensible set of evidence-grounded AI skills for organizing research context, constraining drafting, auditing manuscript consistency, and tracking review responses.

<br/>

<p style="font-size: 1.35em; line-height: 1.8;">
  <a href="https://ailwb.com/"><b><u>Website</u></b></a>
  &nbsp;·&nbsp;
  <a href="README.md"><b><u>中文</u></b></a>
  &nbsp;·&nbsp;
  <a href="README_EN.md"><b><u>English</u></b></a>
</p>

<br/>

`Factual fidelity` · `Evidence traceability` · `Auditable edits` · `Testable workflows`

</div>

---

## What it is

ScholarlyOps is not a loose pile of prompts. It is an **Agent Skills** kit for the research lifecycle. It turns “make it sound more academic” into executable evidence constraints: link claims to materials when possible, keep edits traceable, report consistency issues with severity, and map reviewer comments to concrete actions.

Five core workflows are available today:

| Need | Skill | What it does |
|------|-------|--------------|
| Scattered notes; facts mixed with interpretation | [`research-context`](.agents/skills/research-context/) | Builds a structured research record; separates facts, interpretation, open questions, and gaps |
| Fuzzy topic; unclear keywords or databases | [`literature-search`](.agents/skills/literature-search/) | Plans literature search strategies: frameworks, synonym matrices, database-specific queries, iteration logs |
| Fluent prose with thin evidence | [`evidence-writing`](.agents/skills/evidence-writing/) | Drafts or rewrites under evidence constraints; avoids unsupported claim inflation |
| Abstract, body, captions, and conclusions disagree | [`manuscript-audit`](.agents/skills/manuscript-audit/) | Consistency and evidence-risk audit (including runnable heuristic script checks) |
| Review comments hard to track | [`review-response`](.agents/skills/review-response/) | Splits comments and links edits, evidence, and status |

All five skills are currently **Draft**: workflows and boundaries are defined, with structural validation and synthetic evals. None are Beta/Stable, and **large-scale real-manuscript / live-database validation has not been completed**.

## Problems it addresses

General writing assistants often optimize for fluency and can:

- silently change sample sizes, values, or units;
- turn correlation into causation, or trends into proven effects;
- imply citation support that was never checked;
- overwrite originals so later audit trails are weak.

ScholarlyOps responds with checkable practice:

- **Factual fidelity** — do not alter data, design, statistical inference, or claim strength for style.
- **Evidence traceability** — connect important claims to text, figures, data, or literature loci; mark what cannot be verified.
- **Auditable edits** — retain original, revision, rationale, evidence, and author decisions; prefer new outputs over overwriting originals.
- **Testable workflows** — skill structure is validatable; deterministic checks are regressable; script capability is declared separately from semantic judgment.

## Core skills

| Skill | Role | Maturity |
|-------|------|----------|
| [`research-context`](.agents/skills/research-context/) | Structure goals, design, variables, results, limits, and open items | Draft |
| [`literature-search`](.agents/skills/literature-search/) | Search strategy planner: frameworks, keyword matrices, per-database strings, iteration (Strategy Only by default) | Draft |
| [`evidence-writing`](.agents/skills/evidence-writing/) | Draft/rewrite with claim–evidence mapping | Draft |
| [`manuscript-audit`](.agents/skills/manuscript-audit/) | Cross-section consistency; heuristic numeric/unit checks plus semantic review guidance | Draft |
| [`review-response`](.agents/skills/review-response/) | Split comments; map edits, evidence, status, and author decisions | Draft |

Maturity levels are defined in the [Product Spec](docs/PRODUCT_SPEC.md): `Draft` / `Beta` / `Stable`. No skill is beyond Draft today.

`literature-search` defaults to **strategy and query drafts** without inventing hit counts; Search Assisted only when real tools and access exist. PubMed / Scopus / WoS / Google Scholar notes are summary-level checks against official help—re-verify before formal review searches.

`manuscript-audit` local scripts can detect some **literal numeric conflicts** and **unit-token conflicts**, and can tolerate format/rounding differences within configured bounds. That is **not** a full scientific semantic auditor and does not replace author or expert judgment.

## Quick start (preferred: ask your Agent to install)

**Preferred**: paste the prompt below into Cursor / Claude Code / Codex and install into a **user-global** skills directory (reuse across projects).  
You do **not** need to clone this repo first, and you should **not** default to installing into a business project.  
One natural-language prompt is **not guaranteed** on every Agent—see the [installation guide](docs/en/installation.md) for verified paths and limits.

```text
Please install ScholarlyOps skills.
Repository: https://github.com/dxl11/scholarlyops-skills
Canonical path: .agents/skills/
Five skills: research-context, literature-search, evidence-writing, manuscript-audit, review-response.
List them first and let me choose all or a subset; prefer this Agent’s official install path; install user-global; ask before overwriting; report paths and how to verify loading; if blocked, explain and point to CLI/docs alternatives.
```

**Next**: platform-native options (Codex `$skill-installer` GitHub directory URLs; Cursor/Claude global skill dirs; Marketplace plugins need extra manifests—**this repo does not yet ship a verified plugin package**). See installation guide §2.

**CLI fallback** (Node.js 18+; [`npx skills`](https://github.com/vercel-labs/skills) 1.7.4):

```bash
npx skills add dxl11/scholarlyops-skills --list
npx skills add dxl11/scholarlyops-skills --global --agent cursor claude-code --skill '*'
npx skills add dxl11/scholarlyops-skills --global --agent cursor --skill manuscript-audit
npx skills list --global
```

Then open any project and invoke via `/` or by name. **On-disk ≠ loaded.** [Cursor smoke test](docs/en/cursor-smoke-test.md) · [Installation guide](docs/en/installation.md) · [中文安装](docs/zh-CN/installation.md)

Maintainer development:

```bash
git clone https://github.com/dxl11/scholarlyops-skills.git
cd scholarlyops-skills
python tools/validate_skills.py
```

### Example (`manuscript-audit`)

1. Work on a copy; do not overwrite originals by default.
2. Enable `manuscript-audit`; provide abstract, relevant body sections, captions, and optional references.
3. Review the graded report: Critical / Major / Minor / Needs Review, with loci, evidence, and author confirmations.

Synthetic cases: [`evals/cases/manuscript-audit/`](evals/cases/manuscript-audit/)

## Project status and known limits

> This project is **under development**. The notes below are not a formal release or certification claim.

- All skills are **Draft**; no large-scale real-paper / live-database validation yet.
- `literature-search` synthetic cases: [`evals/cases/literature-search/`](evals/cases/literature-search/) (local runner skips semantic cases; not counted as pass).
- **License is undetermined**; do not claim MIT, Apache-2.0, or any other license until a `LICENSE` file is added. See [open-questions.md](docs/decisions/open-questions.md).
- Official GitHub remote, trademark, and brand legal clearance are still open; metadata lives in [`project.json`](project.json).
- `run_evals.py` scores **deterministic script** cases only; agent/human semantic cases are skipped and **not** counted as passes.
- Preferred install entry is **ask your Agent**; CLI `npx skills` is the fallback. Cursor/Claude **official Marketplace plugin packages are not shipped yet** (see [plugin-distribution.md](docs/decisions/plugin-distribution.md)).
- `npx skills` (1.7.4) local discovery and prior Cursor global landing were verified in the maintainer environment; **IDE `/` load** and **Codex / Claude Code end-to-end install** still need confirmation on your machine.
- Passing programmatic tests ≠ fully validated manuscript auditing; keep Draft while valid Agent semantic blinds remain insufficient. See [evals/README.md](evals/README.md).
- Literature APIs and auto-submission are **not implemented** (see [Roadmap](docs/ROADMAP.md)).
- Security reporting: [SECURITY.md](SECURITY.md) (GitHub private vulnerability reporting must be confirmed/enabled by maintainers in the web UI; **no** invented security email).

## Layout

```text
scholarlyops-skills/
├── README.md / README_EN.md
├── project.json                 # centralized branding/metadata
├── .agents/skills/              # canonical skills root
├── docs/
├── evals/
├── tools/                       # validate_skills.py / run_evals.py
├── tests/
└── .github/workflows/
```

## Dependencies

- Using skills: a compatible agent (Cursor preferred); no mandatory app runtime.
- Validating this repo: Python **3.10+**, standard library only.

```bash
python tools/validate_skills.py
python -m unittest discover -s tests -v
python -m unittest discover -s .agents/skills/manuscript-audit/tests -v
python tools/run_evals.py
```

## Integrity and security

- Do not fabricate experiments, numbers, citation support, or completed edits.
- Evidence states: `verified` / `partially_supported` / `unverified` / `unsupported` / `conflicting`.
- Layered citation checks: existence → metadata → content support → argumentative fitness.
- Private manuscripts and outputs are gitignored; see [SECURITY.md](SECURITY.md).

## Contributing

Documentation fixes, evaluation cases, validator improvements, and skill-instruction updates are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Related docs

- [Product Spec](docs/PRODUCT_SPEC.md) · [Roadmap](docs/ROADMAP.md)
- [Architecture (EN)](docs/en/architecture.md) · [架构（中文）](docs/zh-CN/architecture.md)
- [Evals](evals/README.md) · [Cursor smoke-test](docs/en/cursor-smoke-test.md) · [Changelog](CHANGELOG.md)
- [简体中文 README](README.md)
