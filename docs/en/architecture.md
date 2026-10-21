# Architecture · ScholarlyOps

English | [简体中文](../zh-CN/architecture.md)

## 1. Goals and non-goals

**Goals**: Evidence-grounded, installable, testable agent skills for research material structuring, evidence-constrained writing, manuscript audit, and review response.

**Non-goals**: Replacing scientific judgment; unsupervised auto-publication; fabricating results; republishing third-party skill repos as original work.

## 2. Users and scenarios

See [Product Spec](../PRODUCT_SPEC.md). Core scenarios: pre-submission self-check, evidence-constrained rewrite, review-response loop.

## 3. Skill responsibilities and triggers

| Skill | Trigger when | Do not trigger when |
|-------|--------------|---------------------|
| `research-context` | User needs a structured research record | User only wants polish of fixed prose |
| `evidence-writing` | Draft/rewrite under known evidence | User asks to invent data for significance |
| `manuscript-audit` | Cross-section consistency / evidence risks | User wants unrelated new sections only |
| `review-response` | Handling reviewer comments | No reviewer comments provided |

## 4. Shared norms vs standalone skills

- Authoritative norms live in `docs/PRODUCT_SPEC.md` and this doc.
- Runtime-required rules ship inside each skill (e.g. `references/integrity.md`) so a copied skill still works alone.
- Branding is centralized in `project.json`.

## 5. I/O and errors

Contracts are defined in each `SKILL.md`. Shared rules: declare limits; degrade evidence states instead of fabricating; prefer new outputs over overwriting originals.

## 6. Programmatic vs semantic checks

`manuscript-audit` routes determinate numeric/unit mismatches to `scripts/` when possible. Causality shifts and citation support need model judgment with loci and rationale—never mark unsupported guesses as confirmed errors.

## 7. Layout

```text
.agents/skills/<skill-name>/
├── SKILL.md           # required
├── references/        # optional
├── scripts/           # optional; relative paths
├── examples/          # optional
└── tests/             # optional
```

`tools/validate_skills.py` checks local relative paths, forbids cross-skill runtime deps and absolute machine paths.

## 8. Add, test, update, release

Follow [CONTRIBUTING.md](../../CONTRIBUTING.md); run the validator and unit tests; place synthetic evals in `evals/`; upgrade maturity only with evidence; public release waits on license and remote decisions.

## 9. EN/ZH sync

Keep README, installation, and architecture pairs aligned; validator checks critical README links.

## 10. Security and regression

Re-run validation after changes; CI via `.github/workflows/validate.yml` (no personal secrets); tracked secrets require maintainer remediation—do not rewrite history in this init task.

## 11. Distribution

- **Canonical source**: `.agents/skills/` in this repo (single source; discoverable by `npx skills`).
- **Primary end-user path**: Agent **global** install (`npx skills add <owner>/<repo> -g`).
- **Project install**: optional team pin; not required.
- **Maintainers**: clone this repo for validation/evals.

See [installation.md](installation.md).

## 12. Status

**Done**: docs skeleton; four Draft skills; manuscript-audit demos; validator/CI; verified `npx skills` discovery and Cursor global on-disk install.

**Planned**: Phases 3–6 in [ROADMAP.md](../ROADMAP.md).

**Limits**: all Draft; limited frontmatter parsing; Cursor IDE `/` load and Claude Code still pending user confirmation; license undetermined.
