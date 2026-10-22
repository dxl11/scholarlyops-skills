# Installation · ScholarlyOps

English | [简体中文](../zh-CN/installation.md)

> **Principle**: Prefer asking your current Agent to install into a **user-global** skills directory; `npx skills` is the fallback.  
> **Files on disk ≠ loaded**: Confirm discovery/invocation in the Agent UI after install.  
> **One natural-language prompt is not guaranteed to work on every Agent**—use the verified paths below.

Repo: [`https://github.com/dxl11/scholarlyops-skills`](https://github.com/dxl11/scholarlyops-skills)  
Canonical source (single tree): `.agents/skills/<skill-name>/` (`SKILL.md`, `references/`, `scripts/`, `examples/`, …)

Five skills: `research-context` · `literature-search` · `evidence-writing` · `manuscript-audit` · `review-response` (all **Draft**)

---

## 1. Install with your Agent (preferred)

Paste the block below into your **Cursor / Claude Code / Codex** session. The Agent should detect its own product and OS, then use that platform’s supported official path for a **global** install.

### Copy-paste install prompt

```text
Please install ScholarlyOps skills for me.

Repository: https://github.com/dxl11/scholarlyops-skills
Canonical path: .agents/skills/

Five skills (list them first; let me choose all or a subset):
1. research-context
2. literature-search
3. evidence-writing
4. manuscript-audit
5. review-response

Requirements:
1. Identify the current Agent name and OS (Windows / macOS / Linux).
2. Prefer this Agent’s official/built-in install path; if unavailable, use a verified global-directory copy or the CLI fallback.
3. Install into the user-global skills directory for reuse across projects; do not default to the current business project folder.
4. Before writing, check the destination; if a same-named skill exists, explain the conflict and ask before overwriting.
5. Keep the full required contents for each chosen skill: SKILL.md, references/, scripts/, examples/, etc. (not an empty stub).
6. After install, report the actual file paths and how to verify loading in this Agent (e.g. / search for the skill name).
7. If install cannot complete, explain why and point to native-plugin / CLI alternatives in the repo docs.
8. Do not run unreviewed remote scripts; do not write real API keys; do not rewrite git history.
```

### Expected Agent behavior (not a universal guarantee)

| Step | Behavior |
|------|----------|
| Inventory | Show the five skills; confirm all vs subset |
| Path | Follow “Verified paths per Agent” below |
| No silent overwrite | Ask before replace/backup/skip |
| Verify | Report paths; remind to restart / new turn before testing load |

---

## 2. Native / platform install paths (verified summary)

Based on public official docs (reviewed ~**2026-10-22**). **This repo does not yet ship a verified Cursor/Claude marketplace plugin package**, so we do **not** claim one-click marketplace listing works today.

### 2.1 Codex (OpenAI)

| Item | Detail |
|------|--------|
| Built-in installer | `$skill-installer` ([skill-installer SKILL.md](https://github.com/openai/skills/blob/main/skills/.system/skill-installer/SKILL.md)) |
| Global dir | `$CODEX_HOME/skills/` (default `~/.codex/skills/`) |
| GitHub directory URL | Supported for third-party skill folders; **aborts** if destination already exists |
| Example (one skill) | Ask `$skill-installer` to install e.g. `https://github.com/dxl11/scholarlyops-skills/tree/main/.agents/skills/manuscript-audit` |
| Multiple skills | Repeat per `.agents/skills/<name>`, or pass multiple `--path` values if the installer scripts allow |
| After install | Restart / new turn per Codex guidance |
| Note | The `openai/skills` repo itself is deprecated toward Plugins; **GitHub-path install via `$skill-installer` is still documented**. Not end-to-end tested in this maintainer environment—verify inside Codex. |

### 2.2 Cursor

| Item | Detail |
|------|--------|
| Docs | [cursor.com/docs/skills](https://cursor.com/docs/skills) |
| User-global dirs | `~/.agents/skills/`, `~/.cursor/skills/` (Windows: `%USERPROFILE%\.agents\skills\`, etc.) |
| Project-level | `.agents/skills/`, `.cursor/skills/` (**not** the default end-user path) |
| Compatibility | Also discovers `~/.claude/skills/`, `~/.codex/skills/`, … |
| Native import from GitHub | Docs: skills are **not** imported alone; package as a **Plugin**, then Marketplace / “From GitHub Repository” (repo needs `.cursor-plugin/marketplace.json`, etc.) |
| This repo | **No** verified Cursor marketplace plugin config yet—use Agent install into global dirs, or CLI |
| Cloud Agents | Only `~/.cursor/skills/` syncs when enabled; `~/.agents/skills/` stays local by default (per Cursor docs) |
| UI checklist | [cursor-smoke-test.md](cursor-smoke-test.md) (**pending your machine**) |

### 2.3 Claude Code

| Item | Detail |
|------|--------|
| Docs | [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) |
| Personal global | `~/.claude/skills/<name>/SKILL.md` (all local projects; not the same as cloud/Cowork sync) |
| Project-level | `.claude/skills/` (optional) |
| Plugin marketplace | Needs a marketplace repo with `.claude-plugin/marketplace.json`, then `/plugin marketplace add …` and `/plugin install …` ([Plugins](https://code.claude.com/docs/en/plugins/overview)) |
| This repo | **No** verified Claude marketplace plugin package yet—use Agent copy to `~/.claude/skills/`, or CLI |
| This environment | Claude Code install/load **pending** |

### 2.4 Native plugin distribution (decision)

Keeping `.agents/skills/` as the **only** canonical source:

- Official Cursor/Claude “marketplace” UX needs **extra** plugin/marketplace layout (skills usually under the plugin’s `skills/`).  
- Future packaging should be **automated** from `.agents/skills/`—no hand-synced duplicate `SKILL.md` trees.  
- **We do not commit unverified** `.cursor-plugin/*` / `.claude-plugin/*` configs. See [plugin-distribution.md](../decisions/plugin-distribution.md).

---

## 3. CLI installation (fallback)

Needs **Node.js 18+**. CLI: [`npx skills`](https://github.com/vercel-labs/skills) (checked **1.7.4**; trust `npx skills --help`).

### 3.1 List skills

```bash
npx skills add dxl11/scholarlyops-skills --list
```

### 3.2 Global install — all skills

```bash
npx skills add dxl11/scholarlyops-skills --global --agent cursor claude-code --skill '*'
```

### 3.3 Global install — one skill

```bash
npx skills add dxl11/scholarlyops-skills --global --agent cursor --skill manuscript-audit
npx skills add dxl11/scholarlyops-skills --global --agent claude-code --skill literature-search
```

### 3.4 Target one Agent only

Set `--agent` to `cursor`, `claude-code`, or another ID from `--help`.

### 3.5 Project-level (optional, not default)

```bash
# from the business project root (no --global)
npx skills add dxl11/scholarlyops-skills --agent cursor --skill manuscript-audit
```

### 3.6 List / update / remove

```bash
npx skills list --global
npx skills update --global -y
npx skills update manuscript-audit --global -y
npx skills remove manuscript-audit --global --agent cursor -y
```

Short flags: `-g`, `-a`, `-s`. Optional `--copy` (copy instead of symlink; used in prior Windows Cursor landing checks).

### 3.7 Platform tips

Same `npx` commands on Windows PowerShell, macOS, and Linux. Inspect common landing dirs with the PowerShell/`ls` snippets in the Chinese guide (or trust `skills list --global` `path` fields).

---

## 4. Troubleshooting

| Issue | What to try |
|-------|-------------|
| Installed but `/` finds nothing | Restart Agent/IDE; confirm global path; Cursor Customize → Skills; smoke-test |
| Landed in project, not global | Reinstall with `--global` or copy to user-level dirs |
| Name conflict | Backup first; Codex installer aborts if destination exists |
| Permission errors | Don’t blindly elevate; use a writable user home path |
| CLI shows fewer than 5 skills | Ensure GitHub has the latest commit; or `npx skills add . --list` on a local clone |
| Update | `npx skills update --global` or Agent re-sync with overwrite confirmation |
| Uninstall | `npx skills remove …` or delete the user-level skill folder after confirming the path |
| manuscript-audit scripts | Python 3.10+; run from the **installed** skill `scripts/` |
| Safety | No secrets in skill files; no untrusted install scripts; only trusted repo sources |

---

## 5. Source development (maintainers)

```bash
git clone https://github.com/dxl11/scholarlyops-skills.git
cd scholarlyops-skills
python tools/validate_skills.py
```

Edit only `.agents/skills/`.

---

## 6. Verification log (factual)

| Check | Status |
|-------|--------|
| Local tree has 5 skills; `npx skills add . --list` | Verified in maintainer env |
| Cursor global landing via CLI `--copy` | Previously verified for `manuscript-audit`; not re-run this phase |
| Cursor IDE `/` load | **Pending** user smoke-test |
| Codex `$skill-installer` + this repo URL | **Docs checked**; **not end-to-end tested here** |
| Claude Code global dir / marketplace | **Docs checked**; **install/load not tested** |
| Cursor/Claude marketplace packages | **Not provided** |

License may still be undetermined: [open-questions.md](../decisions/open-questions.md).
