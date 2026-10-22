# Search strategy methods · literature-search

Short method reminders for ScholarlyOps Agents. Not a substitute for full handbooks.

## Question frameworks (choose; do not force PICO)

| Framework | Elements (typical) | Prefer when |
|-----------|--------------------|-------------|
| PICO / PICOS | Population, Intervention, Comparator, Outcome (+ Study design) | Intervention / comparative clinical questions |
| PEO | Population, Exposure, Outcome/Experience | Exposure or experiential questions |
| SPIDER | Sample, Phenomenon of Interest, Design, Evaluation, Research type | Some qualitative / mixed-method questions |
| Concept map only | 2–4 core concepts | Early exploratory topics |

Always state why the framework fits and which slots are still `MISSING` / assumed.

## Building sensitivity vs precision

- **OR within a concept** expands synonyms and spelling variants that are truly interchangeable for the question.  
- **AND across concepts** increases precision but risks missing papers that omit a concept from title/abstract.  
- Outcomes and study-design filters are often applied **later** (screening or database limits), not always in the core string.  
- Related-but-not-synonymous terms: keep in a “related” column; do not auto-OR them into the main concept block without rationale.

## Controlled vocabulary

- MeSH, Emtree, CINAHL Headings, thesaurus terms: mark **verified** only after checking an official browser/tool in-session.  
- Otherwise: `unverified_controlled_vocabulary` and still provide free-text candidates.

## Iteration heuristics

**Too few hits**: drop non-essential AND concepts; add verified synonyms/variants; check spelling; use seed-paper author keywords; broaden fields.  
**Too many hits**: tighten fields (title/abstract); remove overly broad terms; use proximity; add a justified concept; apply limits only with documented rationale.

## Reporting & reproducibility

For systematic / scoping reviews, remind users to keep a search log (database, platform, date, full string, limits, hits, revisions).  
Point to **PRISMA-S** (PRISMA extension for searching) as a reporting framework to consult—**do not** claim that producing one string equals PRISMA-S compliance.

Cochrane and other handbook chapters on searching are external references; link rather than copy.

## Modes

- **Strategy Only**: plan + strings; `NOT_EXECUTED` for hits.  
- **Search Assisted**: only with real tools/access; never invent counts or citations.
