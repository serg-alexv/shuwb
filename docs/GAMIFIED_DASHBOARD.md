# Gamified Litigation Observatory Dashboard

Status: product and visualization contract for a public, collaboration-friendly legal-intelligence interface.

## Product thesis

The dashboard is a live observatory, not a leaderboard of litigants. Gamification is allowed only when it improves data quality, collaboration, coverage, verification, or reader orientation.

The core game loop:

```text
new record discovered
  -> community/source verification
  -> extraction challenge
  -> reconciliation
  -> canonical promotion
  -> visible map/graph/timeline update
  -> contributor credit and audit trail
```

## Primary analytical jobs

1. monitoring: what changed since the last daily run;
2. coverage: what portion of the litigation universe is discovered/verified/extracted;
3. topology: how cases move through instance levels, appeal, cassation and remand;
4. strategy: which legal/evidence strategies appear, spread and survive appeal;
5. finance: how claimed losses are reduced into court-proven and awarded amounts;
6. transferability: which `SHUS-2024` patterns carry into `JULY-2026` and which do not.

## MVP views

### 1. War-room delta

Daily state changes:

- new cases;
- new acts;
- newly verified official records;
- extraction failures;
- human-review flags;
- cohort coverage change;
- new appeal/cassation/remand events.

No metric may hide its verification state.

### 2. Cohort map

A geographic substrate is useful only for physical incidents and court hubs.

Layers:

- physical incident sites;
- first-instance court hubs;
- appeal/cassation routes;
- record certainty: measured / reported / inferred / unknown.

The map must not imply that court geography equals damage geography.

### 3. Procedural topology

Graph or Sankey-like view:

```text
case -> first instance -> appeal -> cassation -> remand -> second round
```

Useful encodings:

- node shape = proceeding level;
- edge style = procedural transition;
- badge = result type;
- warning mark = unresolved source/provenance issue.

### 4. Financial decomposition

For each claim component:

```text
claimed -> defendant recognized -> court-proven -> awarded -> paid/settled
```

Required ratios:

- `R_claim = awarded / claimed`;
- `R_proved = awarded / court_accepted_loss`;
- `R_economic = (awarded + pretrial_paid) / estimated_economic_loss`;
- `R_quantity = quantity_accepted / quantity_claimed`.

The dashboard must not present `awarded / claimed` as the sole effectiveness score.

### 5. Strategy diffusion

A timeline/network view showing:

- first observed strategy use;
- actor: plaintiff / defendant / court;
- treatment: accepted / rejected / partial / not reached;
- appeal survival;
- strategy + evidence interactions.

Examples:

- `COGS_PURCHASE x SUPPLIER_UPD x WB_REPORT`;
- `RETAIL_PRICE x no supplier documents`;
- `FORCE_MAJEURE x UAV_CLAUSE x contract exposure class`.

### 6. Case dossier

A source-first card for each case:

- normalized case ID;
- incident cohort;
- parties;
- procedural stages;
- claim components;
- evidence/finding matrix;
- cited acts/authorities;
- exact provenance spans;
- extraction status;
- Git commit and source manifest row.

## Gamification mechanics

### Allowed mechanics

| mechanic | purpose |
|---|---|
| verification quests | invite contributors to resolve missing source/provenance records |
| coverage badges | show corpus completeness by cohort/stage/court |
| streaks for verified contributions | reward repeated high-quality verification |
| boss fights | complex cases with remand, contradictory quantities, many acts |
| strategy cards | make legal/evidence strategies memorable and inspectable |
| fog of war | visually separate unknown, discovered, verified and gold records |
| bounty board | list high-value missing records or ambiguous cases |
| audit score | reward corrections, not only additions |

### Forbidden mechanics

- no shaming individual judges, sellers or representatives;
- no speculative claim that a seller will win;
- no public score that ranks legal teams without severity/selection controls;
- no betting-like UX;
- no gamified legal advice;
- no hidden AI confidence as if it were fact.

## Contributor roles

| role | capability |
|---|---|
| scout | proposes new source/case candidate |
| verifier | confirms official record and source locator |
| extractor | annotates facts/relations with spans |
| reconciler | resolves contradictions and amount math |
| reviewer | approves canonical promotion |
| maintainer | merges data PRs and schema changes |

## URL and persistence contract

Public routes should be stable and shareable:

```text
/?cohort=SHUS-2024&status=OFFICIAL_RECORD_VERIFIED
/case/A41-61831-2024
/strategy/VALUATION_COGS
/source/SRC-SUDACT-A41-61831-2024-AP1
/delta/2026-08-17
```

State stored in URL:

- cohort;
- verification status;
- selected case;
- date range;
- court/stage filters;
- strategy/evidence filters;
- metric mode;
- uncertainty visibility.

## Mobile-first contract

Mobile portrait is primary:

- top: daily delta and corpus confidence;
- then: cohort switcher;
- then: case cards;
- then: financial decomposition;
- then: source/provenance drill-down.

Hover-only interactions are prohibited. Every value needed to understand a claim must be visible or reachable by tap/focus.

## Accessibility and trust

- direct labels over detached legends where possible;
- redundant encoding for status, not color alone;
- reduced-motion mode for timeline/graph animations;
- visible source caveats near every public metric;
- stale/offline state with last source commit SHA;
- exportable CSV/JSON with schema version.

## Suggested stack

Recommended MVP stack:

- Next.js / React for public UI;
- TypeScript data contracts generated or aligned from schema;
- static projection JSON produced from canonical Git data;
- D3/SVG for topology and decomposition charts;
- simple map library or static GeoJSON layer for incident/court map;
- no WebGL until scale requires it;
- GitHub Actions to build projection artifacts.

## Quality gates

A dashboard build is acceptable only if it reports:

- source commit SHA;
- schema version;
- generated_at;
- row counts by state;
- unresolved flags;
- excluded/quarantined record counts;
- known coverage caveats.
