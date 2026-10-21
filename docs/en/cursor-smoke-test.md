# Cursor smoke-test guide · manuscript-audit

English | [简体中文](../zh-CN/cursor-smoke-test.md)

> **Status**: This checklist must be executed **in the Cursor IDE UI**.  
> Do **not** claim the skill is loaded until you record a real verification.  
> Official reference: [Cursor Agent Skills](https://cursor.com/docs/skills) (project dirs include `.agents/skills/` and `.cursor/skills/`).

This repo’s **canonical source** is `.agents/skills/` (single source of truth). Do not permanently maintain a second full copy just for loading experiments; use a temporary alternate path only while debugging.

## 0. Prerequisites

- Open this repository (or a project that contains a copy of `manuscript-audit`) as the Cursor workspace root.
- Confirm `.agents/skills/manuscript-audit/SKILL.md` exists.
- Optional local script evals (independent of IDE discovery):

```bash
python tools/run_evals.py
```

## 1. Confirm Cursor discovers `manuscript-audit`

In Agent chat:

1. Type `/` and search for `manuscript-audit`.
2. Or inspect Cursor Settings panels related to Skills / Rules.

**Pass**: the skill appears in `/` or the Skills list.  
**Fail**: see section 9. Record discovered / not discovered below.

> Community reports: some builds index `.agents/skills` but fail slash invocation, while `.cursor/skills` works more reliably. If only `/` fails, record version + symptom, then optionally **temporarily** copy one skill to `.cursor/skills/` for a controlled experiment (do not commit dual sources).

## 2. Manual invocation

```text
Follow the manuscript-audit skill strictly (read .agents/skills/manuscript-audit/SKILL.md).
Audit the synthetic manuscript below. Run scripts under that skill directory when possible, then do semantic judgment.
Output must use the report template: Summary, Deterministic checks, Issues (Severity / Location / Evidence / Evidence state / Suggested fix / Author confirmation), Unrun checks, Limits.
Do not overwrite my input file. Do not mark guesses as Critical.
```

You may also try `/manuscript-audit` if your Cursor build supports slash skills.

## 3. Verify the correct SKILL.md was read

Ask:

```text
Quote the skill file path you are following and paste the Critical and Needs Review rows from its severity table verbatim.
```

**Pass**: path points at this repo’s (or your copy’s) `manuscript-audit/SKILL.md`, and the excerpt matches the file.

## 4. Synthetic input: numeric mismatch

Use `evals/cases/manuscript-audit/01_numeric_unit_mismatch/input.md`.

**Expect**:

- Enrollment 120 vs 100 as Critical with locus (`verified` if based on text/script).
- uM vs mg/mL mentioned (Major / Needs Review).
- No extra Critical findings without evidence.

Optional terminal check:

```bash
python .agents/skills/manuscript-audit/scripts/check_numeric_consistency.py --input evals/cases/manuscript-audit/01_numeric_unit_mismatch/input.md --json
```

## 5. Synthetic input: benign rounding

Use `evals/cases/manuscript-audit/12_rounding_tolerance/input.md`.

**Expect**: 7.14 vs 7.1 must **not** be scored as a Critical literal error. Treating rounding as Critical is a **false positive**.

## 6. Every issue needs evidence

| Field | Requirement |
|------|-------------|
| Location | Concrete section locus |
| Evidence | Quote or script output |
| Evidence state | Shared vocabulary |
| Author confirmation | Usually yes for Critical/Major |

Critical/Major without location/evidence → fail.

## 7. Separate scripts vs semantic judgment

Require the agent to split **Deterministic checks** (scripts) from **Semantic findings**. Local `tools/run_evals.py` only covers scripts. **Do not** claim semantic audit passed because local evals passed.

## 8. Record the run

Copy to private notes or gitignored `outputs/`:

```text
Date:
Cursor version:
Workspace root:
Skill discovered (Y/N):
Slash /manuscript-audit works (Y/N):
SKILL.md path quoted by agent:
Case IDs tested:
Output saved as:
Pass/Fail notes:
```

## 9. If the skill is not discovered

1. Workspace root must contain `.agents/skills/`.
2. Path must be `.agents/skills/manuscript-audit/SKILL.md`.
3. Frontmatter: `name: manuscript-audit` matches folder; non-empty `description`.
4. Skill not disabled in settings.
5. Restart Cursor / reload window.
6. Controlled experiment: copy **one** skill to `.cursor/skills/manuscript-audit/` and retest (record only; don’t dual-track sources in git).
7. Log Cursor version + OS in `docs/decisions/open-questions.md`.

## 10. Must be done in the IDE (terminal cannot replace)

- [ ] Discovery via `/` or Settings
- [ ] Correct SKILL.md quoted
- [ ] Cases 01 and 12 report quality
- [ ] Semantic items not falsely marked script-`verified`

Until checked, docs must keep stating: **Cursor load verification pending user confirmation**.
