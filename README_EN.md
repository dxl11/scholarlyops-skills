# ScholarlyOps

**Academic Research Workflow Skills**

Evidence-grounded AI skills for the research lifecycle.

English | [简体中文](README.md)

> **Status**: Initialization / under development. All skills are **Draft**. License not selected. Name/trademark not legally cleared. Do not invent stars, downloads, user counts, or third-party certifications.

Central metadata: [`project.json`](project.json). Suggested repository name: `scholarlyops-skills`.

## Why ScholarlyOps

AI writing help often optimizes for fluency and can silently change numbers, inflate causality, invent citation support, or overwrite originals. ScholarlyOps encodes mitigations into executable skills: factual fidelity, evidence traceability, auditable edits, modularity, testability, and security-first defaults.

## Problems addressed

| Problem | Capability |
|---------|------------|
| Scattered notes; facts mixed with interpretation | `research-context` structured research records |
| Fluent prose with thin evidence | `evidence-writing` evidence-constrained drafting |
| Abstract / body / captions / conclusions disagree | `manuscript-audit` consistency audit |
| Review replies hard to track | `review-response` comment–edit mapping |

## Design principles

1. **Factual fidelity** — do not alter data, design, statistics, or claim strength for style.
2. **Evidence traceability** — link claims to text, figures, data, or literature loci when possible.
3. **Auditable edits** — keep original, revision, rationale, evidence, and author decisions; do not overwrite by default.
4. **Modularity** — clear skill boundaries; independently installable; no implicit absolute paths.
5. **Testability** — runnable structural checks and synthetic evals; maturity requires evidence.
6. **Security first** — no hardcoded secrets; no silent upload of private materials; external APIs must declare boundaries.

## Current skills and maturity

| Skill | Role | Maturity |
|-------|------|----------|
| [`research-context`](.agents/skills/research-context/) | Structure goals, design, data, results, limits, and open questions | Draft |
| [`evidence-writing`](.agents/skills/evidence-writing/) | Draft/rewrite under evidence constraints | Draft |
| [`manuscript-audit`](.agents/skills/manuscript-audit/) | Cross-section consistency and evidence-risk audit (reference implementation) | Draft |
| [`review-response`](.agents/skills/review-response/) | Split reviewer comments and link edits, evidence, and status | Draft |

Maturity levels: `Draft` / `Beta` / `Stable` (see [Product Spec](docs/PRODUCT_SPEC.md)). **No skill is Beta or Stable yet.**

## Layout

```text
scholarlyops-skills/
├── README.md / README_EN.md
├── project.json                 # centralized branding/metadata
├── .agents/skills/              # canonical skills root
├── docs/
├── evals/
├── tools/validate_skills.py     # stdlib validator
├── tests/
└── .github/workflows/
```

## Install and use

- [Installation (English)](docs/en/installation.md)
- [安装指南（中文）](docs/zh-CN/installation.md)

Canonical project-level path: `.agents/skills/` (Cursor docs also mention `.cursor/skills/`; this repo standardizes on `.agents/skills/`).

**Copy one skill (PowerShell):**

```powershell
New-Item -ItemType Directory -Force -Path ".agents\skills" | Out-Null
Copy-Item -Recurse -Force `
  "D:\path\to\scholarlyops-skills\.agents\skills\manuscript-audit" `
  ".agents\skills\manuscript-audit"
```

## Example (`manuscript-audit`)

1. Work on a copy; do not overwrite originals by default.
2. Enable `manuscript-audit` in your agent.
3. Provide abstract, relevant body sections, captions, optional references.
4. Receive a graded report: Critical / Major / Minor / Needs Review with loci, evidence, and author confirmations.

Synthetic cases: [`evals/cases/manuscript-audit/`](evals/cases/manuscript-audit/)

## Dependencies

- Using skills: a compatible agent (Cursor preferred); no mandatory runtime.
- Validating this repo: Python **3.10+**, standard library only.

```bash
python tools/validate_skills.py
python -m unittest discover -s tests -v
python -m unittest discover -s .agents/skills/manuscript-audit/tests -v
python tools/run_evals.py
```

`run_evals.py` scores **deterministic** cases only; `agent_semantic` cases are skipped (not passes). Cursor load: [smoke-test guide](docs/en/cursor-smoke-test.md).

## Integrity and security

- Do not fabricate experiments, numbers, citation support, or completed edits.
- Evidence states: `verified` / `partially_supported` / `unverified` / `unsupported` / `conflicting`.
- Layered citation checks: existence → metadata → content support → argumentative fitness.
- Private manuscripts and outputs are gitignored; see [SECURITY.md](SECURITY.md).

## Current limitations

- All skills are Draft; no large-scale real-manuscript validation yet.
- License and official GitHub remote are undecided.
- Literature APIs, auto-submission, cross-agent installers are **not implemented** (roadmap only).
- Frontmatter checks are limited string parsing, not full YAML validation.
- Whether Cursor auto-loads `.agents/skills/` in *your* session must be confirmed in the IDE; this repo does not claim a completed load test in your environment.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License status

**Undetermined.** Do not claim MIT, Apache-2.0, or any other license until a `LICENSE` file is added. See [open-questions.md](docs/decisions/open-questions.md).

## Related docs

- [Product Spec](docs/PRODUCT_SPEC.md) · [Roadmap](docs/ROADMAP.md)
- [Architecture (EN)](docs/en/architecture.md) · [架构（中文）](docs/zh-CN/architecture.md)
- [Evals](evals/README.md) · [Cursor smoke-test](docs/en/cursor-smoke-test.md) · [Changelog](CHANGELOG.md)
