<div align="center">

<img src="assets/scholarlyops-logo.jpg" alt="ScholarlyOps" width="280" />

# ScholarlyOps

### More rigorous research writing. Claims grounded in evidence.

Academic Research Workflow Skills — an extensible set of evidence-grounded AI skills for organizing research context, constraining drafting, auditing manuscript consistency, and tracking review responses.

<br/>

<p>
  <a href="https://ailwb.com/">
    <img src="https://img.shields.io/badge/My%20Website-1B2A4A?style=for-the-badge&logo=googlechrome&logoColor=white" alt="My Website" />
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="README.md">
    <img src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-1F4D3A?style=for-the-badge&logoColor=white" alt="中文" />
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="README_EN.md">
    <img src="https://img.shields.io/badge/English-EAECEF?style=for-the-badge&labelColor=EAECEF&color=8B949E" alt="English" />
  </a>
</p>

<br/>

`Factual fidelity` · `Evidence traceability` · `Auditable edits` · `Testable workflows`

</div>

---

## What it is

ScholarlyOps is not a loose pile of prompts. It is an **Agent Skills** kit for the research lifecycle. It turns “make it sound more academic” into executable evidence constraints: link claims to materials when possible, keep edits traceable, report consistency issues with severity, and map reviewer comments to concrete actions.

Four core workflows are available today:

| Need | Skill | What it does |
|------|-------|--------------|
| Scattered notes; facts mixed with interpretation | [`research-context`](.agents/skills/research-context/) | Builds a structured research record; separates facts, interpretation, open questions, and gaps |
| Fluent prose with thin evidence | [`evidence-writing`](.agents/skills/evidence-writing/) | Drafts or rewrites under evidence constraints; avoids unsupported claim inflation |
| Abstract, body, captions, and conclusions disagree | [`manuscript-audit`](.agents/skills/manuscript-audit/) | Consistency and evidence-risk audit (including runnable heuristic script checks) |
| Review comments hard to track | [`review-response`](.agents/skills/review-response/) | Splits comments and links edits, evidence, and status |

All four skills are currently **Draft**: workflows and boundaries are defined, with structural validation and synthetic evals. None are Beta/Stable, and **large-scale real-manuscript validation has not been completed**.

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
| [`evidence-writing`](.agents/skills/evidence-writing/) | Draft/rewrite with claim–evidence mapping | Draft |
| [`manuscript-audit`](.agents/skills/manuscript-audit/) | Cross-section consistency; heuristic numeric/unit checks plus semantic review guidance | Draft |
| [`review-response`](.agents/skills/review-response/) | Split comments; map edits, evidence, status, and author decisions | Draft |

Maturity levels are defined in the [Product Spec](docs/PRODUCT_SPEC.md): `Draft` / `Beta` / `Stable`. No skill is beyond Draft today.

`manuscript-audit` local scripts can detect some **literal numeric conflicts** and **unit-token conflicts**, and can tolerate format/rounding differences within configured bounds. That is **not** a full scientific semantic auditor and does not replace author or expert judgment.

## Quick start (recommended: Agent global install)

Primary path for end users: install skills into Cursor / Claude Code **user-global** skill directories and reuse them across projects.  
You do **not** need to copy skills into every business repo.

Requires Node.js 18+ (`npx`). Python 3.10+ is only needed to run `manuscript-audit` scripts.

```bash
# List skills in this repo (verified: 4 skills discovered)
npx skills add dxl11/scholarlyops-skills --list

# Global install one skill into Cursor (recommended)
npx skills add dxl11/scholarlyops-skills -g -a cursor -s manuscript-audit -y --copy

# Or install all four
npx skills add dxl11/scholarlyops-skills -g -a cursor --skill '*' -y --copy

# Verify
npx skills list -g -a cursor
```

Then open any working project and invoke via `/` search or by naming `manuscript-audit`.

For Claude Code, use `-a claude-code` (Claude Code load verification is still pending on your machine).

- Full guide (update / uninstall / troubleshooting / optional project install): [Installation (English)](docs/en/installation.md) · [安装指南（中文）](docs/zh-CN/installation.md)
- Cursor UI checklist: [cursor-smoke-test.md](docs/en/cursor-smoke-test.md)
- Maintainer local development (not the default end-user path):

```bash
git clone https://github.com/dxl11/scholarlyops-skills.git
cd scholarlyops-skills
python tools/validate_skills.py
python -m unittest discover -s tests -v
python tools/run_evals.py
```

### Example (`manuscript-audit`)

1. Work on a copy; do not overwrite originals by default.
2. Enable `manuscript-audit`; provide abstract, relevant body sections, captions, and optional references.
3. Review the graded report: Critical / Major / Minor / Needs Review, with loci, evidence, and author confirmations.

Synthetic cases: [`evals/cases/manuscript-audit/`](evals/cases/manuscript-audit/)

## Project status and known limits

> This project is **under development**. The notes below are not a formal release or certification claim.

- All skills are **Draft**; no large-scale real-paper validation yet.
- **License is undetermined**; do not claim MIT, Apache-2.0, or any other license until a `LICENSE` file is added. See [open-questions.md](docs/decisions/open-questions.md).
- Official GitHub remote, trademark, and brand legal clearance are still open; metadata lives in [`project.json`](project.json).
- `run_evals.py` scores **deterministic script** cases only; agent/human semantic cases are skipped and **not** counted as passes.
- `npx skills` **discovery** of this repo and Cursor **global install on disk** were verified in the maintainer environment; **IDE `/` menu discovery and correct execution** still need the smoke-test checklist.
- Claude Code and other agents: commands follow the CLI docs; **load verification is pending**. No claim of support for web/cloud agents.
- Literature APIs and auto-submission are **not implemented** (see [Roadmap](docs/ROADMAP.md)).

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
