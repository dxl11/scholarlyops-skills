# Installation · ScholarlyOps

English | [简体中文](../zh-CN/installation.md)

## Three usage scenarios

| Scenario | Who | Default? |
|----------|-----|----------|
| **Agent global install** | End users: install into Cursor / Claude Code personal skill dirs; reuse across projects | **Yes (primary)** |
| Source development | Maintainers developing/testing in this repo | Maintainers only |
| Project-level install | Teams that must pin the same skill set inside one repo | **Optional**, not required |

Project-level install is **not** a prerequisite for using ScholarlyOps.

## Prerequisites

| Purpose | Requirement |
|---------|-------------|
| Recommended installer (`npx skills`) | Node.js 18+ (`npx` fetches the CLI; no need to install `skills` globally) |
| Using installed skills | A compatible agent (Cursor or Claude Code) |
| `manuscript-audit` deterministic scripts | Python 3.10+ (stdlib). Without Python, semantic audit can still follow `SKILL.md`, but scripts will not run |
| Repo development / local evals | Python 3.10+ |

Security:

- Do not put API keys in install commands.
- Do not install as root/Administrator by default.
- `npx skills` fetches from GitHub; only use trusted sources.
- These skills do not require running custom remote scripts at install time; if the CLI behavior changes, follow its prompts.

## Repository layout and discovery (verified)

- Canonical skill source (single source of truth): `.agents/skills/<skill-name>/SKILL.md`
- This layout **is discoverable** by `npx skills`; a second parallel `skills/` tree is **not** required.
- Verified CLI: `skills` **1.7.4** via `npx skills`
- Verified discovery (local and GitHub both listed 4 skills):

```bash
npx skills add dxl11/scholarlyops-skills --list
# or from this repo root:
npx skills add . --list
```

Discovered: `research-context`, `evidence-writing`, `manuscript-audit`, `review-response`.

GitHub id (from local `git remote`, and `--list` succeeded): `dxl11/scholarlyops-skills`  
If you fork/move the repo, replace `dxl11/scholarlyops-skills` with your `<owner>/<repo>`.

---

## 1. Primary path: Agent global install (recommended)

After a global install, skills can be reused across **many** working projects without copying them into each repo.

### 1.1 Install one skill (example: manuscript-audit)

**Cursor:**

```bash
npx skills add dxl11/scholarlyops-skills -g -a cursor -s manuscript-audit -y --copy
```

**Claude Code:**

```bash
npx skills add dxl11/scholarlyops-skills -g -a claude-code -s manuscript-audit -y --copy
```

Notes:

- `-g` / `--global`: user-level install (cross-project).
- `-a`: target agent.
- `-s`: skill name.
- `-y`: skip prompts (omit the first time if you want to review the summary).
- `--copy`: copy files (used in our Windows verification; the CLI may also offer symlinks).

### 1.2 Install all four skills

```bash
# Cursor
npx skills add dxl11/scholarlyops-skills -g -a cursor --skill '*' -y --copy

# Claude Code
npx skills add dxl11/scholarlyops-skills -g -a claude-code --skill '*' -y --copy
```

Or target multiple agents when both are present:

```bash
npx skills add dxl11/scholarlyops-skills -g -a cursor -a claude-code --skill '*' -y --copy
```

### 1.3 Verify installation

```bash
npx skills list -g -a cursor
npx skills list -g -a claude-code
npx skills list -g --json
```

**Paths — document vs this machine:**

| Agent | Common path in CLI docs | Verified here (2026-10-21) |
|-------|-------------------------|----------------------------|
| Cursor | `~/.cursor/skills/` | Install landed at `%USERPROFILE%\.agents\skills\<skill>\`, listed under Agent=`Cursor` |
| Claude Code | `~/.claude/skills/` | **Not installed/verified in this environment** (commands follow CLI docs; trust the CLI’s printed path) |

Always trust the `path` field from `npx skills list -g`.

### 1.4 Invoke an installed skill

1. Open **any** working project (ScholarlyOps repo not required).
2. In Cursor Agent, type `/` and search the skill name, or ask explicitly to follow `manuscript-audit`.
3. For Claude Code, enable/use skills per that product’s UX.

Presence on disk ≠ loaded. Confirm in the IDE. See [cursor-smoke-test.md](cursor-smoke-test.md).

### 1.5 Update

```bash
npx skills update -g -a cursor -y
npx skills update manuscript-audit -g -a cursor -y
```

### 1.6 Uninstall

```bash
npx skills remove manuscript-audit -g -a cursor -y
npx skills remove -g -a cursor -s '*' -y
```

Confirm with `npx skills list -g`.

### 1.7 Troubleshooting load failures

1. Check `npx skills list -g --json` for name + `path`.
2. Ensure `SKILL.md` exists; Frontmatter has `name` / `description`; `name` matches folder.
3. Restart the agent IDE; retry `/` search.
4. Ensure skills are not disabled in settings.
5. For `manuscript-audit` scripts: need Python 3.10+; run scripts relative to the **installed skill directory**.

---

## 2. Optional: project-level install

Use only when a team must pin skills inside a business repository. Scope is that repo only.

```bash
# from the business project root (no -g)
npx skills add dxl11/scholarlyops-skills -a cursor -s manuscript-audit -y --copy
```

Typical landing path (confirm via CLI): `.agents/skills/<skill>/` inside the project.

Manual copy remains a fallback, not the default end-user path.

---

## 3. Source development (maintainers)

```bash
git clone https://github.com/dxl11/scholarlyops-skills.git
cd scholarlyops-skills
python tools/validate_skills.py
python -m unittest discover -s tests -v
python tools/run_evals.py
```

Edit only `.agents/skills/` in this repo — do not maintain a second divergent `SKILL.md` tree.

---

## 4. Standalone install boundaries

Each skill ships its own `SKILL.md` plus needed `references/` / `scripts/` / `examples/`. After a single-skill global install:

- Do **not** depend on other repo paths or absolute machine paths.
- Example for `manuscript-audit` (cwd = installed skill dir):

```bash
python scripts/check_numeric_consistency.py --input /path/to/copy.md --json
```

- Without Python: install can still succeed; declare script checks as unrun in the audit report.

## 5. Verification log (factual)

| Check | Status |
|-------|--------|
| Discover 4 skills from local `.` | Passed |
| Discover 4 skills from `dxl11/scholarlyops-skills` | Passed |
| Global install `manuscript-audit` to Cursor (`-g -a cursor --copy`) | Passed: files under `~/.agents/skills/manuscript-audit` |
| Cursor IDE `/` discovery + semantic run | **Pending IDE checklist** |
| Claude Code global install + load | **Pending** |
| Other agents | **Planned only** |

## 6. Security and scope

| Mode | Scope |
|------|-------|
| Global `-g` | Current user’s agent skill dirs; visible across projects |
| Project install | Current repository only |
| Source clone | Local development copy |

License may still be undetermined; see [open-questions.md](../decisions/open-questions.md).
