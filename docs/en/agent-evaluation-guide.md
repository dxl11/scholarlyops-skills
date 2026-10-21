# Agent Semantic Evaluation Guide · manuscript-audit

English | [简体中文](../zh-CN/agent-evaluation-guide.md)

> **Purpose**: Validate how reliably `manuscript-audit` performs semantic audit in a real Agent workflow.  
> **Rules**: Do not invent measured results; unrun cases are **skip** (never pass); keep maturity **Draft** until enough valid tests support a higher claim.  
> **Companion files**: `evals/agent-semantic/` (blind set, rubric, scorecard)

This guide matches the Chinese version in substance.

---

## 1. Report the two evaluation tracks separately

| Track | How to run | Status rule |
|------|------------|-------------|
| Deterministic scripts | `python tools/run_evals.py` | Auto-scored locally; semantic cases are skipped |
| Agent semantic | This blind protocol + human scorecards | Counts **only** after a real blind run is scored |

`tools/run_evals.py` always skips `agent_semantic` cases by design. Skip ≠ pass.

Do not modify the numeric/unit detectors in this phase unless you find a concrete, reproducible defect—and then add a regression test.

---

## 2. Blind set (reuse the existing 24 cases)

Coverage mapping lives in `evals/agent-semantic/blind-set.json`.

**Wave A (semantic core, run first)**

| Case | Focus |
|------|--------|
| `02_correlation_to_causation` | Correlation written as causation |
| `05_citation_metadata_error` | Unverified DOI / metadata |
| `06_citation_not_supporting` | Citation present but does not support the claim |
| `07_missing_evidence` | Insufficient evidence / missing methods |
| `09_terminology_inconsistency` | Terminology drift |
| `10_methods_results_contradiction` | Methods vs results contradiction |
| `17_insufficient_evidence_not_auto_error` | Missing evidence ≠ automatic Critical |

**Wave B (optional dual-track)**: clean control, rounding/format, legitimate group/time/n differences, true numeric conflict candidates (see `blind-set.json`). Use these to check whether the Agent over-upgrades script candidates.

Do not duplicate similar synthetic manuscripts just to inflate case counts.

---

## 3. Prevent answer leakage

During Agent execution, provide **only**:

1. `input.md` from the blind pack  
2. Sibling `TASK.md`  
3. The installed `manuscript-audit` Skill instructions  

**Must not** pre-read:

- That case’s `expect.json`  
- `evals/expected/manuscript-audit/<id>.md`  
- Answer-bearing parts of the rubric before scoring  
- A filled scorecard  

If the same session already opened the gold answers → the run is **invalid as a blind test**.

---

## 4. Prepare an isolated workspace

Generate a pack **outside** the repo (recommended):

```bash
python tools/prepare_agent_blind_pack.py --wave wave_a_semantic_core --out %USERPROFILE%\scholarlyops-blind\run1

python tools/prepare_agent_blind_pack.py --case 02_correlation_to_causation --out %USERPROFILE%\scholarlyops-blind\run1
```

The script:

- Copies only `input.md` and writes a neutral `TASK.md`  
- **Refuses** to copy `expect.json` / `expected/` / rubric  
- Writes `pack_manifest.json` (case IDs only; no expected answers)  
- Creates `CASES/<case_id>/` under the output root  

Check: no `expect.json` under any case folder.

---

## 5. Run case-by-case in Cursor

For **each** case:

### 5.1 Open the isolated workspace

Open the blind-pack root (or the case folder) in Cursor. Do **not** also open the ScholarlyOps repo (with `evals/expected`) in the same Agent context.

### 5.2 Start a fresh Agent session

One new chat per case. Do not chain cases in one session after reviewing scoring notes.

### 5.3 Invoke the Skill

Confirm install ([installation](installation.md) / [Cursor smoke test](cursor-smoke-test.md)), then prompt, for example:

```text
Audit input.md in this folder strictly using the installed manuscript-audit Skill.
If Python is available, run the scripts under the Skill install directory first, then perform semantic judgment.
Follow the Skill output contract (Summary, Deterministic checks, Issues, Unrun checks, Limits).
Do not overwrite input.md. Do not mark guesses as confirmed Critical. Do not read expect files or gold answers from any repo.
```

`/manuscript-audit` may be used if the IDE supports it.

### 5.4 Save raw output

Save the **unedited** Agent reply as:

`CASES/<case_id>/raw_agent_output.md`

Optional human edits go elsewhere; scoring uses the raw file.

### 5.5 Record version metadata

Write `run_meta.json` beside the output (fields: case id, date, agent/model names and versions, Skill commit or install path, workspace path).

---

## 6. Independent scoring step

1. Only now open repo `expect.json` and `evals/expected/...`.  
2. Apply `evals/agent-semantic/rubric.md`.  
3. Copy `scorecard-template.json` to a results path and fill it.  
4. Allowed `status`: `pass` | `fail` | `partial` | `skip`.  
5. Contaminated or unrun sessions → `skip`.

Never rewrite raw Agent output to make the scorecard look better.

---

## 7. Scoring dimensions (summary)

For each expected finding, judge: detection vs miss; false positives; severity band; evidence support; locus findability; misuse of `verified`; over-upgrade of candidates to Critical; fitness of suggestions.

Full detail: `evals/agent-semantic/rubric.md`.

---

## 8. Reporting template

```text
## Deterministic local tests
- Command: python tools/run_evals.py
- Result: … (executed / passed / failed / skipped)

## Agent semantic blind tests
- Prepared: …
- Actually executed: …
- Human-scored: …
- Not yet run: …
- Invalid / inconclusive: …

## Quality summary (valid scored cases only)
- Critical-issue recall: …
- False positives: …
- Severity reasonableness: …
- Evidence locus quality: …

## Maturity
- Remains Draft. Do not claim Stable with too few valid tests.
```

If the terminal cannot call a live Agent without a paid API, use this **human-driven** Cursor workflow. **Do not fabricate** Agent outputs.

---

## 9. Limits

- Synthetic cases ≠ real submissions.  
- Semantic judgment varies by model and operator.  
- Local script pass ≠ Agent reliability.  
- This repo does not require paid API automation.
