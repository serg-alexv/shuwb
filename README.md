# shuwb

Open litigation observatory for marketplace warehouse-loss disputes.

## Mission

`shuwb` is a collaboration-friendly, auditable legal-intelligence dataset and analysis stack for disputes between marketplace sellers and Wildberries/RVB arising from warehouse fires and related loss events.

GitHub is the canonical source of truth. Dashboards, notebooks, databases and model outputs are derived views and must be reproducible from versioned repository data.

## Research design

Incident cohorts are kept separate. In particular, `SHUS-2024` and 2026 incidents are **not** pooled as interchangeable observations. Cross-incident analysis uses explicit hierarchical/longitudinal models and tests transferability rather than assuming it.

Canonical observation path:

`Incident → Seller/Contract Exposure → Case → Proceeding → Judicial Act → Claim Component → Strategy/Evidence → Judicial Finding → Award`

The project distinguishes:

- raw sourced facts from derived variables;
- plaintiff/WB assertions from judicial findings;
- case-level outcomes from claim-component outcomes;
- first instance from appeal/cassation/remand rounds;
- descriptive association from causal or predictive claims;
- confirmed, inferred and unknown values.

## Repository layout

```text
schema/                 machine-readable data contracts
data/
  incidents/            incident cohort records
  cases/                normalized case records
  sources/              source manifests, not unsourced claims
docs/                   architecture, provenance, research protocol
analysis/               reproducible notebooks/scripts (derived)
web/                    interactive observatory (derived)
```

## Core analytical questions

1. Which plaintiff strategies and evidence bundles are associated with stronger component-level recovery?
2. Which findings survive appeal and cassation?
3. Which effects transfer across incident cohorts, and which are cohort-specific?
4. How do strategies diffuse after published decisions?
5. How much of observed heterogeneity is attributable to incident, court, judge, claim type, evidence quality or representation?

## Data integrity rule

No canonical fact enters the dataset without provenance. Every extracted fact must be traceable to a source document and location/span, with extraction method, confidence and verification status. LLM output is a proposal until validated against source evidence.

## Status

Bootstrap phase. Schema v1.1 and provenance contracts are being established before bulk ingestion.
