# Database syntax notes · literature-search

**Purpose**: Short, attributable reminders for drafting queries.  
**Not** a full copy of vendor manuals. Always re-check the live official help before a formal review search.  
**Checked for this Draft skill**: 2026-10-22 (URLs may move; treat dates as audit trail).

## Distinctions

| Type | Examples | Notes |
|------|----------|-------|
| Database / content | MEDLINE, Scopus content, WoS Core Collection | What is indexed |
| Platform | PubMed.gov, Ovid, EBSCOhost, Clarivate WoS UI | How you query |
| Search engine | Google Scholar | Different operators, ranking, reproducibility limits |

Never claim one source covers an entire discipline. Never assume the user has institutional access.

---

## PubMed (NLM)

**Primary help**: [PubMed User Guide / Help](https://pubmed.ncbi.nlm.nih.gov/help/)  
**Training index**: [NLM PubMed Online Training](https://www.nlm.nih.gov/bsd/disted/pubmedtutorial/020_770.html)

### Draft-relevant syntax (verify on help page before formal use)

| Feature | Typical pattern | Caution |
|---------|-----------------|---------|
| Boolean | `AND`, `OR`, `NOT` (uppercase customary) | Parentheses for grouping |
| Fields | e.g. `[Title/Abstract]`, `[Title]`, `[MeSH Terms]`, `[All Fields]` | Tags change search translation |
| Phrase | `"exact phrase"` | ATM / phrase index may alter unquoted terms |
| Truncation | `*` after ≥4 leading characters (per PubMed help) | Wildcards interact with ATM |
| Proximity | PubMed proximity search (see current help / NLM tours) | Do not invent operators |
| Mapping | Automatic Term Mapping (ATM) | Quotes / tags can bypass mapping |

**MeSH**: Only mark a MeSH heading as verified if checked in the MeSH Browser or equivalent in-session tool. Otherwise: `unverified_controlled_vocabulary`.

**Grammar status for this Skill**: `syntax_checked_against_official_help` (summary level). Re-verify after NLM UI changes.

---

## Scopus (Elsevier)

**Support**: [Scopus Advanced search help (Support Center)](https://service.elsevier.com/app/answers/detail/a_id/11365/supporthub/scopus/)  
**Developer search tips** (field codes): [Elsevier Scopus search tips](https://dev.elsevier.com/sc_search_tips.html)

### Draft-relevant syntax

| Feature | Typical pattern | Caution |
|---------|-----------------|---------|
| Combined title/abs/key | `TITLE-ABS-KEY(...)` | Prefer Advanced search field codes |
| Boolean | `OR`, `AND`, `AND NOT` | Precedence: OR → proximity → AND → AND NOT |
| Proximity | `W/n` (unordered), `PRE/n` (ordered) | Do not put `AND` inside a proximity expression |
| Phrase | `"loose phrase"` or `{exact}` | Exact braces stricter than quotes |
| Wildcards | `*`, `?` | Confirm current limits in help |

**Do not** paste PubMed `[Title/Abstract]` strings into Scopus.

**Grammar status**: `syntax_checked_against_official_help` (summary). Institutional UI variants may differ.

---

## Web of Science Core Collection (Clarivate)

**Field tags**: [WoS Core Collection Advanced Search Field Tags](https://webofscience.zendesk.com/hc/en-us/articles/26916347018257-Web-of-Science-Core-Collection-Advanced-Search-Field-Tags)  
**Operators**: [Search Operators](https://webofscience.zendesk.com/hc/en-us/articles/20016122409105-Search-Operators)

### Draft-relevant syntax

| Feature | Typical pattern | Caution |
|---------|-----------------|---------|
| Topic | `TS=(...)` | Title, Abstract, Author Keywords, Keywords Plus (per Clarivate docs) |
| Boolean | `AND`, `OR`, `NOT` | Case-insensitive operators per help |
| Proximity | `NEAR/x` (and related operators per current help) | Defaults and limits per Clarivate docs |
| Wildcards | `*`, `$`, `?` (per product help) | Confirm before formal use |

**Grammar status**: `syntax_checked_against_official_help` (summary). Editions (SCI-EXPANDED etc.) affect coverage—state what the user can access.

---

## Google Scholar

**Help**: [Google Scholar search tips](https://scholar.google.com/intl/en/scholar/help.html) (interface-oriented)

| Feature | Typical approach | Caution |
|---------|------------------|---------|
| Boolean | `OR` often required uppercase; `-` for exclude (UI-dependent) | Not a bibliographic database; ranking opaque |
| Phrase | `"..."` | Limited field control vs PubMed/Scopus/WoS |
| Reproducibility | Weaker for systematic reviews | Prefer as exploratory adjunct |

**Grammar status**: `partial`. Prefer professional databases for reproducible review searches.

---

## Other databases (Embase, CINAHL, IEEE Xplore, ACM DL, PsycINFO, ERIC, …)

Provide: concept logic + candidate terms + `needs_syntax_adaptation`.  
Do **not** invent platform-specific field codes as “verified executable” without checking that product’s current help.

---

## License / reuse note

Link to official pages; do not paste entire vendor manuals into ScholarlyOps. Summaries above are short factual notes for Agent drafting under Strategy Only mode.
