# Installation · ScholarlyOps

English | [简体中文](../zh-CN/installation.md)

> **CLI version**: Commands below were checked against `npx skills` (`skills` **1.7.4**) `--help`. If your CLI is newer, trust `npx skills --help`.  
> **Files on disk ≠ skill loaded**: After install, confirm discovery/invocation inside Cursor / Claude Code.

## Three usage scenarios

| Scenario | Who | Default? |
|----------|-----|----------|
| **Agent global install** | End users: personal agent skill dirs; reuse across projects | **Yes (primary)** |
| Project-level install | Teams pinning skills inside one business repo | **Optional** |
| Source development | Maintainers cloning this repo to edit skills and run tests | Maintainers only |

**End users do not need to clone this repository** or copy skills into every business project.

## Prerequisites

| Purpose | Requirement |
|---------|-------------|
| Recommended installer (`npx skills`) | Node.js 18+ (`npx` fetches the CLI; no global `skills` install required) |
| Using installed skills | Compatible agent (Cursor and/or Claude Code) |
| `manuscript-audit` deterministic scripts | Python 3.10+ (stdlib). Without Python, follow `SKILL.md` for semantic audit; scripts will not run |
| Repo development / local evals | Python 3.10+ |

Security:

- Do not put API keys in install commands.
- Do not install as root/Administrator by default.
- `npx skills` fetches from GitHub; use `dxl11/scholarlyops-skills` (or a fork you trust).

## Repository layout and discovery (checked)

- **Single source of truth**: `.agents/skills/<skill-name>/SKILL.md` (no second manually synced tree).
- This layout is discoverable by `npx skills` (after adding `literature-search`, expect **5** skills; confirm with `npx skills add dxl11/scholarlyops-skills --list` on the version you pull).

```bash
npx skills add dxl11/scholarlyops-skills --list
# or from this repo root:
npx skills add . --list
```

Expected: `research-context`, `literature-search`, `evidence-writing`, `manuscript-audit`, `review-response`.  
(If the remote has not received the latest commit yet, `--list` may still show the older set.)

References:

- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [Cursor Skills docs](https://cursor.com/docs/skills)
- [Claude Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

---

## 1. Primary path: Agent global install (recommended)

### 1.1 Install one skill (example: literature-search or manuscript-audit)

**Cursor and Claude Code together** (when both are detected by the CLI):

```bash
npx skills add dxl11/scholarlyops-skills --global --agent cursor claude-code --skill literature-search
# or:
npx skills add dxl11/scholarlyops-skills --global --agent cursor claude-code --skill manuscript-audit
```

**Cursor only:**

```bash
npx skills add dxl11/scholarlyops-skills --global --agent cursor --skill literature-search
```

**Claude Code only:**

```bash
npx skills add dxl11/scholarlyops-skills --global --agent claude-code --skill literature-search
```

Short-flag equivalent (same meaning; maintainer Windows env previously verified Cursor landing for `manuscript-audit` with `--copy -y`):

```bash
npx skills add dxl11/scholarlyops-skills -g -a cursor -s literature-search -y --copy
```

| Flag | Meaning |
|------|---------|
| `--global` / `-g` | User-level install (cross-project) |
| `--agent` / `-a` | Target agent(s), e.g. `cursor claude-code` |
| `--skill` / `-s` | Skill name |
| `-y` | Skip prompts (omit the first time to review the summary) |
| `--copy` | Copy files instead of symlinking |

### 1.2 Install all skills

```bash
npx skills add dxl11/scholarlyops-skills --global --agent cursor claude-code --skill '*'
```

Use a single `--agent` value to target only Cursor or only Claude Code.

Short-flag example:

```bash
npx skills add dxl11/scholarlyops-skills -g -a cursor --skill '*' -y --copy
```

CLI also offers `--all` (`--skill '*' --agent '*' -y`), which targets **every** agent the CLI detects. Prefer an explicit `--agent` list when you only want Cursor and/or Claude Code.

### 1.3 List installed skills

```bash
npx skills list --global
npx skills list --global --agent cursor
npx skills list --global --agent claude-code
npx skills list --global --json
```

Aliases: `npx skills ls -g`, `npx skills ls -g -a cursor`.

### 1.4 Update

```bash
npx skills update --global -y
npx skills update manuscript-audit --global -y
```

Alias: `npx skills update -g -y`.

### 1.5 Uninstall

```bash
npx skills remove manuscript-audit --global --agent cursor -y
npx skills remove --global --agent cursor --skill '*' -y
```

Interactive: `npx skills remove`.

Clearing everything managed by the CLI is destructive — prefer named removes or agent-scoped `--skill '*'`. Only use `npx skills remove --global --all` if you intentionally want to remove every installed skill.

### 1.6 Platform notes

The same `npx …` commands work on **Windows PowerShell, macOS, and Linux** (Node.js 18+).

Inspect landing dirs (always prefer the `path` from `skills list --global`):

**PowerShell:**

```powershell
Get-ChildItem "$env:USERPROFILE\.agents\skills" -ErrorAction SilentlyContinue
Get-ChildItem "$env:USERPROFILE\.cursor\skills" -ErrorAction SilentlyContinue
Get-ChildItem "$env:USERPROFILE\.claude\skills" -ErrorAction SilentlyContinue
```

**macOS / Linux:**

```bash
ls -la ~/.agents/skills 2>/dev/null
ls -la ~/.cursor/skills 2>/dev/null
ls -la ~/.claude/skills 2>/dev/null
```

### 1.7 Cursor vs Claude Code: paths and limits

| Agent | Paths often cited in docs | Maintainer-env note | Limit |
|-------|---------------------------|---------------------|-------|
| Cursor | Often `~/.cursor/skills/` | Global install previously landed under `%USERPROFILE%\.agents\skills\<skill>\` with Agent=Cursor in `list -g` | **IDE `/` discovery and semantic run still pending your checklist** ([cursor-smoke-test.md](cursor-smoke-test.md)) |
| Claude Code | Often `~/.claude/skills/` | **Not installed/verified here** | Commands follow CLI docs; trust your CLI/product output |

### 1.8 Start using a skill

1. After global install, open **any** working project (ScholarlyOps clone not required).
2. **Cursor**: type `/` and search the skill name, or ask to follow `manuscript-audit`.
3. **Claude Code**: follow that product’s Agent Skills UX (**not verified in this repo**).
4. Prefer manuscript **copies**; do not overwrite originals by default.
5. For deterministic scripts, run `scripts/` from the **installed skill directory** (Python 3.10+).

### 1.9 Troubleshooting

1. Check `npx skills list --global --json` for name + `path`.
2. Ensure `SKILL.md` exists; Frontmatter `name` matches the folder.
3. Restart the agent app; retry discovery.
4. Ensure skills are not disabled in settings.
5. For scripts: Python 3.10+; paths relative to the installed skill’s `scripts/`.

---

## 2. Optional: project-level install

```bash
# from the business project root (no --global)
npx skills add dxl11/scholarlyops-skills --agent cursor --skill manuscript-audit
```

Typical landing path (confirm via CLI): `.agents/skills/<skill>/` inside that project only.

---

## 3. Source development (maintainers)

```bash
git clone https://github.com/dxl11/scholarlyops-skills.git
cd scholarlyops-skills
python tools/validate_skills.py
python -m unittest discover -s tests -v
python tools/run_evals.py
```

Edit only `.agents/skills/` in this repo.

---

## 4. Standalone install boundaries

Each skill ships its own `SKILL.md` plus needed `references/` / `scripts/` / `examples/`. After a single-skill global install, do not depend on other repo paths.

```bash
python scripts/check_numeric_consistency.py --input /path/to/copy.md --json
```

---

## 5. Verification log (factual; no reinstall this phase)

| Check | Status |
|-------|--------|
| `skills` 1.7.4 `--help` flag check | Checked (this phase) |
| `npx skills add … --list` skill discovery | **Local tree has 5 skills**; remote `--list` depends on pushed revision (push not required in this phase) |
| Cursor global install landing (`-g -a cursor --copy`) | **Verified earlier** in maintainer env; **not re-run** this phase |
| Cursor IDE `/` discovery + invoke | **Pending user IDE check** |
| Claude Code global install + load | **Pending** |
| Other agents | **Planned only** |

## 6. Security and scope

| Mode | Scope |
|------|-------|
| Global `--global` | Current user’s agent skill dirs; cross-project |
| Project (no `-g`) | Current repository only |
| Source clone | Local development copy |

License may still be undetermined; see [open-questions.md](../decisions/open-questions.md) and [SECURITY.md](../../SECURITY.md).
