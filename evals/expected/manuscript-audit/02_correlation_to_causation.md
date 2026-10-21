# Expected (02) — agent / human scoring

**Mode**: `agent_semantic` (local runner always SKIP)

## Must find

1. Causal language from correlation only (`r=0.42` in Results → “caused” in Discussion). Severity band: Major–Critical.
2. “Proves clinical efficacy” unsupported by excerpt. Severity band: Major–Critical–Needs Review.

## Must not

- Alter or invent a different `r` value.
- Mark Critical without citing Discussion/Results loci.

## Notes

Severity need not be unique within the allowed band. Score after a blind run using `evals/agent-semantic/rubric.md`.
