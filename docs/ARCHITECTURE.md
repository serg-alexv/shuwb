# Litigation Observatory architecture v1.1

## Invariants

1. Git is canonical; databases and dashboards are projections.
2. Incident cohorts remain distinct and are joined only through explicit analytical models.
3. `case_id` is not the atomic observation. The minimum analytical grain may be `judicial_act × claim_component × issue × strategy/evidence`.
4. Assertions, evidence, findings and awards are separate entities.
5. Every canonical value has provenance and a verification state.
6. Missing, unknown, not reached and not applicable are different states.

## Entity backbone

```text
DIM_INCIDENT ──< FACT_INCIDENT_FACILITY >── DIM_FACILITY
      │
      └──< FACT_CONTRACT_EXPOSURE >── DIM_SELLER
                                      │
                                      └──< DIM_CASE
                                             │
                                             ├──< CASE_PARTY >── DIM_PARTY
                                             ├──< FACT_PROCEEDING
                                             │      └──< DIM_JUDICIAL_ACT
                                             │             ├──< FACT_JUDICIAL_FINDING
                                             │             ├──< FACT_STRATEGY_USE
                                             │             ├──< FACT_EVIDENCE_USE
                                             │             └──< FACT_CITATION
                                             └──< FACT_CLAIM_COMPONENT
                                                    ├──< FACT_VALUATION
                                                    └──< FACT_AWARD
```

## Why strategy/evidence are event tables

Boolean flags such as `strat_val_cogs=true` destroy process information. The same strategy can be asserted by different actors, first appear on appeal, be accepted in part, be rejected, or never be reached. The canonical representation therefore records actor, stage, treatment, materiality and source span.

## Why contract exposure is not an incident field

Offer applicability may differ by seller, shipment/batch and time. Contract exposure therefore records goods transfer, offer publication/effective/acceptance times and a normalized exposure class. This is essential for 2026 cohort analysis.

## Proceeding identity

`case_id + instance_level` is not unique because remand can produce repeated rounds. Use a distinct `proceeding_id` plus `instance_level`, `round_no`, `act_id` and court metadata.

## Outcome decomposition

Do not use `seller_win` as the principal target. Model the judicial path:

```text
liability finding
  → claim component accepted?
  → quantity accepted
  → valuation basis accepted
  → amount awarded
  → survival on appeal/cassation
```

Recommended descriptive ratios:

- `recovery_claim = awarded / claimed`
- `recovery_proved = awarded / court_accepted_loss`
- `recovery_economic = (awarded + pretrial_paid) / estimated_economic_loss`
- `quantity_acceptance = quantity_accepted / quantity_claimed`

Ratios must carry denominator provenance and should be null when the denominator is not reliably known.

## Statistical architecture

Start with descriptive and partial-pooling models. Avoid encoding substantive conclusions as strong priors before corpus calibration.

For cross-cohort strategy effects, prefer partial pooling:

`beta[strategy, cohort] = mu[strategy] + delta[strategy, cohort]`

with `delta ~ Normal(0, tau_strategy)`.

For recovery ratios, account explicitly for structural mass at 0 and 1 (e.g. zero/one-inflated beta or a staged model), rather than applying a plain logit-normal model to all outcomes.

## Visualization contract

The web observatory is a derived analytical surface, not a second database. Primary views:

1. incident/cohort explorer;
2. procedural timeline and appeal/remand topology;
3. issue/strategy/evidence matrix;
4. claim-to-award financial decomposition;
5. strategy diffusion/citation graph;
6. uncertainty and data-quality overlays.

All views must expose source links, confidence/verification state and last-derived commit SHA. Essential values must remain visible without hover; mobile interaction must use tap/focus and URL-backed state.
