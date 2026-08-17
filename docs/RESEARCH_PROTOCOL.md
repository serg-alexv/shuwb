# Research protocol

## Scope

The observatory studies litigation arising from Wildberries/RVB warehouse-loss incidents over time. Incident cohorts are analyzed jointly only through explicit hierarchical models; they are never treated as identical events.

## Primary research objects

- incident cohorts;
- seller/contract exposure;
- case and procedural trajectory;
- claim components and valuation methods;
- plaintiff and defendant strategies;
- evidence types and judicial treatment;
- issue-level judicial findings;
- awards and post-judgment survival;
- citation and strategy diffusion.

## Initial hypotheses to test, not assume

1. Marketplace-generated inventory records may improve proof of custody/quantity.
2. Cost-based valuation may perform differently from retail-price valuation.
3. Strategy effectiveness may depend more on evidence bundles than on strategy labels alone.
4. Appeal/cassation can materially change observed first-instance effectiveness.
5. Some evidentiary effects may transfer across incident cohorts while contract/liability effects may be cohort-specific.
6. Published decisions may change the strategy mix of later plaintiffs.

## Unit-of-analysis ladder

Analyses must state the unit used:

- incident;
- case;
- proceeding round;
- judicial act;
- claim component;
- issue/finding;
- strategy-use event;
- evidence-use event.

Avoid pseudo-replication: multiple acts from one case are correlated observations.

## Core outcomes

### Procedural

- claim accepted/returned/terminated;
- first-instance disposition;
- appeal survival/reversal;
- cassation survival/remand;
- time to decision.

### Financial

- amount claimed;
- amount recognized by defendant;
- amount court accepted as proven;
- amount awarded;
- pretrial compensation;
- claim recovery ratio;
- proved-loss recovery ratio;
- quantity acceptance ratio.

### Issue-level

For each issue: `ACCEPTED`, `REJECTED`, `PARTIAL`, `NOT_REACHED`, `PROCEDURALLY_BARRED`, `UNKNOWN`, plus materiality.

## Statistical sequence

### Phase 0 — census and data quality

Count unique cases, acts, courts, judges, claim components, missingness and conflicts. Establish case-census coverage before inferential analysis.

### Phase 1 — descriptive

Distributions and small multiples by cohort, time, strategy, evidence, court and procedural stage. Report denominators and uncertainty.

### Phase 2 — conditional association

Hierarchical models with incident/court/judge/case effects where identifiable. Interactions of strategy × evidence are first-class terms.

### Phase 3 — longitudinal diffusion

Measure strategy adoption over time, first appearance, persistence/extinction, citation links and post-decision adoption shifts.

### Phase 4 — prediction

Only after leakage checks and sufficient sample size. Use temporal validation where possible. Prediction must not be presented as legal advice or deterministic case outcome.

## Cross-cohort transferability

Do not set 2024 posteriors as fixed priors for 2026. Use partial pooling and estimate heterogeneity. A candidate transferability statistic for strategy `s` is:

`P(|beta[s,2026] - beta[s,2024]| < epsilon | data)`

The value of `epsilon` must be declared and sensitivity-tested.

## Recovery distribution

Because recovery can be exactly 0 or 1, avoid a plain logit-normal likelihood over all cases. Consider a zero/one-inflated beta or staged model:

1. liability/component accepted?;
2. if accepted, quantity/value accepted?;
3. conditional award amount.

## Bias register

Track at minimum:

- publication/indexing bias;
- settlement censoring;
- plaintiff self-selection;
- lawyer/case-complexity confounding;
- repeated observations within case;
- changing offer terms and law;
- missing evidence in published acts;
- post-treatment variables;
- survivorship through appellate stages;
- LLM extraction error.

## Reporting rule

Any public claim must be reproducible from a commit SHA and specify cohort, unit of analysis, denominator, missing-data treatment and verification threshold.
