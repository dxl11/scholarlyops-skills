# Installation · ScholarlyOps

English | [简体中文](../zh-CN/installation.md)

Branding and path conventions: [`project.json`](../../project.json). Canonical skills root: `.agents/skills/`.

## Prerequisites

| Scenario | Requirement |
|----------|-------------|
| Use skills only | Compatible agent (Cursor preferred) |
| Develop / validate | Python 3.10+ (stdlib only) |

Node.js is not required. Unverified third-party CLIs are **not** official install methods.

---

## Scenario 1: Clone the whole repo for local development

```bash
git clone <YOUR_REPO_URL> scholarlyops-skills
cd scholarlyops-skills
```

If the remote is unset, use your local checkout.

### Verify

```bash
python tools/validate_skills.py
python -m unittest tests.test_validate_skills -v
```

Expect exit code 0 and all unit tests passing.

### Uninstall

Delete the local clone (do not delete copies inside other projects by accident).

---

## Scenario 2: Use skills in a Cursor project

### Location

```text
your-project/
└── .agents/
    └── skills/
        ├── research-context/
        ├── evidence-writing/
        ├── manuscript-audit/
        └── review-response/
```

Cursor docs also mention `.cursor/skills/`. This project standardizes on `.agents/skills/`. If your environment only recognizes one of them, copy to the path that is actually loaded and document it for your team.

### PowerShell (copy all skills)

```powershell
$src = "D:\path\to\scholarlyops-skills\.agents\skills"
$dst = ".agents\skills"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Recurse -Force "$src\*" $dst
```

### Bash

```bash
mkdir -p .agents/skills
cp -R /path/to/scholarlyops-skills/.agents/skills/* .agents/skills/
```

### Confirm recognition

1. Ensure `.agents/skills/<name>/SKILL.md` exists in the target project.
2. Explicitly invoke the skill in Cursor Agent chat.
3. **File presence ≠ loaded.** Confirm in your Cursor build whether the agent follows the skill instructions. This repository does not claim a completed load test in your environment.

### Example run

For `manuscript-audit`, provide a synthetic case under `evals/cases/manuscript-audit/` (in this repo) or a manuscript **copy**, and request a graded audit report.

### Update / remove

- Update: re-copy the skill directory (back up local edits first).
- Remove: delete `.agents/skills/<skill-name>/`.

---

## Scenario 3: Install a single skill into another project

Example: `manuscript-audit`

```powershell
New-Item -ItemType Directory -Force -Path ".agents\skills" | Out-Null
Copy-Item -Recurse -Force `
  "D:\path\to\scholarlyops-skills\.agents\skills\manuscript-audit" `
  ".agents\skills\manuscript-audit"
```

The skill folder must be self-contained (`SKILL.md`, `references/`, `scripts/`, …) and must **not** depend on other repo paths after install.

Verify: open `SKILL.md` and confirm `name: manuscript-audit`.

---

## Scenario 4: Other compatible agents (unverified)

Other products may use different directories (e.g. user-level `~/.claude/skills/`, `~/.codex/skills/`). **This project has not empirically validated those paths.**

Suggested process: read the vendor docs → copy one skill → run a minimal task → record results in open questions or a compatibility note. Do not advertise “supported” before verification.

---

## Troubleshooting

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Agent ignores skill rules | Wrong path / not loaded | Check `SKILL.md`; invoke by name |
| Validator fails | Bad paths / frontmatter | Read tool error lines |
| Scripts missing after copy | Only copied `SKILL.md` | Copy the whole skill directory |
| Path encoding issues | Shell locale | Quote paths; prefer relative paths |

## Cursor load verification

Layout matches official `.agents/skills/` guidance, but **discovery must be confirmed in the IDE**. See [cursor-smoke-test.md](cursor-smoke-test.md).

## Local evals (IDE-independent)

```bash
python tools/run_evals.py
```

Only deterministic script cases are scored; semantic cases are skipped (not passes).

## Security

- Do not commit private manuscripts to public repos.
- Do not put real API keys in skills or examples.
