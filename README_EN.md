<div align="center">

# ScholarlyOps

### More rigorous research writing. Claims grounded in evidence.

Academic Research Workflow Skills — an extensible set of evidence-grounded AI skills for organizing research context, constraining drafting, auditing manuscript consistency, and tracking review responses.

<br/>

[![Website](https://img.shields.io/badge/Website-ailwb.com-1F6FEB?style=for-the-badge&logo=googlechrome&logoColor=white)](https://ailwb.com/)
[![简体中文](https://img.shields.io/badge/README-%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-24292F?style=for-the-badge)](README.md)

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

## Quick start

1. Clone or download this repository (use a local checkout if the remote URL is not set yet).
2. Copy the skill you need into your project:

```text
your-project/
└── .agents/
    └── skills/
        └── manuscript-audit/
```

PowerShell example:

```powershell
New-Item -ItemType Directory -Force -Path ".agents\skills" | Out-Null
Copy-Item -Recurse -Force `
  "D:\path\to\scholarlyops-skills\.agents\skills\manuscript-audit" `
  ".agents\skills\manuscript-audit"
```

3. Invoke the skill explicitly in Cursor Agent (for example, audit a synthetic manuscript copy).
4. Optionally run local checks from the repo root:

```bash
python tools/validate_skills.py
python -m unittest discover -s tests -v
python tools/run_evals.py
```

Full install / uninstall / troubleshooting: [Installation (English)](docs/en/installation.md) · [安装指南（中文）](docs/zh-CN/installation.md)  
Cursor UI checklist: [cursor-smoke-test.md](docs/en/cursor-smoke-test.md)

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
- Whether Cursor has discovered `.agents/skills/` **must be confirmed in the IDE**; this repo does not claim a completed load test in your environment.
- Literature APIs, auto-submission, and cross-agent installers are **not implemented** (see [Roadmap](docs/ROADMAP.md)).

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
