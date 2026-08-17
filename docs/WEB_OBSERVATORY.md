# Web observatory brief

## Analytical job

The web layer is an exploratory legal-intelligence workspace for comparing incident cohorts, following procedural trajectories, inspecting strategy/evidence effectiveness and tracing the financial decomposition of claims. It is a reproducible projection of Git data, not an editable second source of truth.

## Primary views

### 1. Cohort explorer

Purpose: orient the user to incidents without implying that geography equals jurisdiction.

- incident cards and optional quiet map;
- physical facility locations;
- incident date/status;
- case counts by verification state;
- separate court-jurisdiction view.

Fallback: cohort table if geospatial coverage is sparse.

### 2. Litigation topology

Purpose: show `case → proceeding round → act → appeal/cassation/remand`.

Preferred renderer: SVG/D3 or a declarative graph for small/medium networks; switch to Canvas/Sigma only if scale requires it.

Essential values remain directly labeled; hover is supplementary.

### 3. Strategy × evidence matrix

Purpose: compare strategy use, court treatment and evidence bundles.

- rows: strategy/issue families;
- columns: cohort, stage, or time window;
- cells: count, acceptance proportion, uncertainty;
- drill-down: source-supported cases and exact findings.

Avoid interpreting low-N cells as stable effects.

### 4. Financial decomposition

Purpose: show where claims are reduced.

For a claim component:

`claimed → defendant-recognized → court-proven → awarded → paid`

Show quantity and unit-value decomposition separately when available. Never rely on a single `awarded/claimed` ratio.

### 5. Diffusion/citation graph

Purpose: distinguish court citation diffusion from plaintiff strategy adoption.

- judicial citations are explicit edges;
- strategy similarity without citation is a separate inferred relation;
- inferred edges must be visually and semantically marked as inferred.

### 6. Data quality/uncertainty

Every aggregate exposes:

- verified / unverified / conflicted counts;
- missingness;
- current source commit SHA;
- build time;
- cohort and filter state.

## Reading path

1. Immediate evidence: current cohort/case counts and data-quality state.
2. Compare: time/cohort/strategy/evidence distributions.
3. Inspect: case/act/finding details with provenance.
4. Reproduce: copy a URL-backed view and commit SHA.

## State contract

Important interaction state is encoded in URL search params:

- cohort(s);
- date range;
- court/instance;
- strategy/evidence/issue filters;
- verification threshold;
- selected case/act;
- metric definition.

Back/forward navigation must restore analytical state. Saved views may later add immutable IDs mapped to filter JSON.

## Mobile contract

Mobile portrait is a first-class sibling layout:

- cards and stacked small multiples instead of wide dashboards;
- tap/focus instead of hover;
- persistent filter summary with a sheet/drawer for editing;
- graph view switches to focused ego-network or ordered procedural timeline;
- source/provenance remains reachable within one tap from a finding.

## Accessibility

- redundant encodings beyond color;
- keyboard/focus path on desktop;
- text alternative for graphs and maps;
- reduced-motion mode;
- direct labels for essential values;
- sufficient hit targets on touch devices.

## Suggested implementation stack

Initial route: Next.js/React + TypeScript, server-built static/JSON projections from repository data, declarative charts for standard views, D3/SVG for bespoke litigation topology. Use a geospatial library only once facility/court geography carries analytical value.

The data build should produce a versioned artifact such as `web/public/data/observatory.json` containing `source_commit_sha`, `schema_version`, `built_at` and validation summary.

## QA gates

- schema validation before build;
- no aggregate from `CONFLICTED` or `UNVERIFIED` rows unless explicitly selected;
- visual regression for core views;
- URL-state round-trip tests;
- mobile portrait tests;
- accessible names for interactive marks;
- stale/partial data state displayed explicitly;
- source links checked for every drill-down record.
