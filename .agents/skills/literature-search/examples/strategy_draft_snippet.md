# Example · Strategy Only snippet (synthetic)

**Mode**: Strategy Only · **Execution**: `strategy_draft` (no database run)

## Research question understanding

User idea: “AI for detecting diabetic retinopathy in eye photos.”  
Assumed focus: diagnostic performance of AI/ML on retinal images for diabetic retinopathy (DR).

## Framework

**PICO (assumed)**: adults/patients with diabetes or screening populations (P); AI/ML image models (I); human grading or standard screening (C, optional in string); detection/diagnosis of DR (O).  
Uncertain: exact care setting; whether to force Comparator into the string (often omit early for sensitivity).

## Keyword matrix (excerpt)

| Concept | Core | Synonyms / variants | Related (not auto-synonym) |
|---------|------|---------------------|----------------------------|
| Condition | diabetic retinopathy | DR; diabetic retinal disease | macular edema (related complication) |
| Modality | retinal image | fundus photograph*; retinal photograph* | OCT (different modality—keep separate) |
| Approach | artificial intelligence | machine learning; deep learning; CNN | “computer-aided diagnosis” (broader) |

MeSH candidates: `unverified_controlled_vocabulary` until MeSH Browser check.

## PubMed draft (illustrative)

```text
("diabetic retinopathy"[Title/Abstract] OR "diabetic retinopathy"[MeSH Terms] OR DR[Title/Abstract])
AND
(retin* OR fundus)[Title/Abstract]
AND
("artificial intelligence"[Title/Abstract] OR "machine learning"[Title/Abstract] OR "deep learning"[Title/Abstract])
```

Note: `[MeSH Terms]` line is illustrative only if MeSH verified; otherwise remove or mark pending.

## Scopus draft (separate syntax)

```text
TITLE-ABS-KEY(
  ("diabetic retinopathy" OR "diabetic retinal disease")
  AND (fundus OR retinal OR retin*)
  AND ("artificial intelligence" OR "machine learning" OR "deep learning")
)
```

## Limits

Hit counts: `NOT_EXECUTED`. Do not treat this snippet as a completed systematic search.
