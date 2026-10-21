# Cursor smoke-test · manuscript-audit

English | [简体中文](../zh-CN/cursor-smoke-test.md)

> **Status**: Must be checked in the Cursor IDE. A successful terminal install ≠ loaded in the IDE.  
> See [Agent Skills](https://cursor.com/docs/skills) · [Installation](installation.md)

**Prefer verifying global install** (primary end-user path). Only install into a test project when you are specifically checking project-level compatibility.

Canonical sources remain `.agents/skills/` in this repo (single source of truth). Global install copies/links via `npx skills` — do not maintain a second SKILL.md tree here.

## 0. Prerequisites (recommended: global)

```bash
npx skills add dxl11/scholarlyops-skills --global --agent cursor --skill manuscript-audit
# optional: -y --copy (non-interactive + copy; used in maintainer verification)
npx skills list --global --agent cursor
```

Note the printed `path` (maintainer env previously used `%USERPROFILE%\.agents\skills\manuscript-audit`).

Optional repo-local evals (independent of IDE load):

```bash
python tools/run_evals.py
```

Agent semantic blind testing (separate from script evals; do not pre-read expect in the same session): see [Agent semantic evaluation guide](agent-evaluation-guide.md).

## 1. Discovery after global install

1. Open **any project that is not this repo** (cross-project reuse).
2. Type `/` in Agent chat; search `manuscript-audit`.
3. Or inspect Skills in Settings.

**Pass**: skill appears and can be selected.

## 2. Manual invoke

```text
Follow the installed manuscript-audit skill. If Python is available, run scripts under the installed skill directory first, then semantic judgment.
Output Summary, Deterministic checks, Issues, Unrun checks, Limits.
Do not overwrite inputs; do not mark guesses as Critical.
```

## 3. Correct SKILL.md

Ask the agent for the full skill path and the Critical / Needs Review rows verbatim.

## 4–8. Cases, evidence, recording

Use synthetic text from cases `01` and `12`. Require loci/evidence. Record Cursor version, install path, discovery in a non-repo project, and pass/fail notes.

## 9. If not discovered

Check `npx skills list -g --json`, Frontmatter, restart, settings. Use project-level install **only** for compatibility tests (omit `-g`).

## 10. Human checklist

- [ ] Discovered in a **non-repo** project after global install
- [ ] Correct SKILL.md path quoted
- [ ] Cases 01 / 12 acceptable
