# Contributing to shuwb

`shuwb` treats data changes as reviewable research changes.

## Ground rules

1. Do not add an unsourced canonical fact.
2. Do not collapse separate incident cohorts.
3. Do not overwrite conflicts; record them.
4. Distinguish party assertions from court findings.
5. Preserve procedural rounds and claim components.
6. Prefer primary authoritative sources for litigation facts.
7. Do not commit secrets, access tokens, personal contact data not necessary to the public record, or source documents whose redistribution status is unclear.

## Data contribution workflow

A data PR should contain, as applicable:

- source manifest entry;
- normalized observations;
- provenance row(s) pointing to the exact source location/span;
- verification status;
- schema-valid identifiers;
- a short note for conflicts or judgment calls.

### Suggested PR title prefixes

- `source:` source discovery/manifest updates
- `data:` normalized observations
- `schema:` schema or ontology changes
- `verify:` source verification/correction
- `analysis:` reproducible analytical work
- `web:` derived observatory UI
- `docs:` protocol/documentation

## Corrections

Never silently rewrite a disputed or previously published value. Use a normal Git change with a reason and source. If a canonical observation is invalidated, set its verification state to `RETRACTED` or replace it through a reviewed migration preserving history.

## LLM-assisted extraction

LLMs may propose entities, relations, amounts, strategies and findings. Their output must preserve source locators and confidence and remains `UNVERIFIED` until checked. A model must not infer missing legal facts merely to satisfy the schema.

## Analysis contributions

All reported metrics must identify:

- source commit SHA;
- cohort inclusion/exclusion criteria;
- unit of observation;
- treatment of remands/duplicate acts;
- treatment of missing and conflicted data;
- uncertainty where applicable.

Do not describe an association as causal without a defensible identification strategy.
