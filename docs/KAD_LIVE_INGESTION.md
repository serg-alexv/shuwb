# KAD Live Ingestion Pipeline

Status: design contract for the daily monitoring layer. Canonical data remains Git-first; any database, queue, dashboard or game surface is a reproducible projection from validated repository records.

## Purpose

The ingestion pipeline monitors Russian arbitration records for WB/RWB warehouse-loss litigation and converts public case/activity signals into auditable discovery records, extraction candidates, and later canonical observations.

It must preserve cohort separation:

- `SHUS-2024` is the Shushary 13 Jan 2024 precedent cohort.
- `JULY-2026-*` cohorts are live crisis cohorts and must not inherit 2024 facts.
- cross-cohort analytics happen only in the statistical layer with explicit cohort effects and transferability checks.

## Daily loop

```text
KAD / public court index discovery
  -> raw case metadata snapshot
  -> heuristic prefilter
  -> candidate queue
  -> act ingestion
  -> text extraction
  -> structured extraction candidate
  -> reconciliation and provenance validation
  -> canonical Git data PR
  -> dashboard projection build
```

## Target parties

Primary defendant identifiers:

| party | identifier | notes |
|---|---|---|
| ООО «Вайлдберриз» | INN `7721546864` | historical WB defendant naming |
| ООО «РВБ» | INN `9714053621` | later marketplace operator naming |

The pipeline must treat party names as non-stable aliases. INN/OGRN-derived matching has higher priority than name-string matching when available.

## Primary court routing hints

| court layer | likely code / court | role |
|---|---|---|
| first instance | `А41`, Arbitration Court of Moscow Region | expected primary hub |
| appeal | 10th Arbitration Appeal Court | appellate hub for `А41` cases |
| cassation | Arbitration Court of Moscow District / `Ф05` | cassation hub |
| alternative first instance | `А56`, St Petersburg and Leningrad Region | possible incident-location route, not assumed |

These are routing hints only. The discovery process must not discard out-of-hub records without recording the exclusion reason.

## Search matrix

### Positive cohort markers

| cohort | match-any tokens |
|---|---|
| `SHUS-2024` | `Шушары`, `13.01.2024`, `13 января 2024`, `пожар на складе Шушары`, `складской комплекс в Шушарах` |
| `JULY-2026-ELEK` | `Электросталь`, `18.07.2026`, `БПЛА`, `новая редакция оферты`, `07.07.2026` |
| `JULY-2026-KOT` | `Котовск`, `18.07.2026`, `БПЛА`, `новая редакция оферты`, `07.07.2026` |
| `JULY-2026-OTHER` | `Невинномысск`, `Краснодар`, `склад`, `БПЛА`, `атака`, `пожар`, `оферта` |

### Negative / quarantine markers

Records matching these markers should not be silently deleted. They go to `QUARANTINED_NON_FIRE` unless another signal is strong enough.

- `возврат комиссии`
- `КВВ`
- `габариты товара`
- `ПВЗ`
- `нарушение правил маркировки`
- `штраф за самовыкуп`
- ordinary logistics penalty disputes without fire/incident markers

## State machine

```text
DISCOVERED
  -> KAD_SYNCED
  -> ACT_INGESTED
  -> LLM_EXTRACTED
  -> RECONCILED
  -> OFFICIAL_RECORD_VERIFIED
  -> GOLD_EXTRACTED optional
```

### State definitions

| state | meaning | allowed dashboard exposure |
|---|---|---|
| `DISCOVERED` | case or act found by search/indexing | visible as unverified signal |
| `KAD_SYNCED` | docket chronology and metadata captured | visible with metadata caveat |
| `ACT_INGESTED` | act text/PDF captured or linked | visible with source locator |
| `LLM_EXTRACTED` | structured candidate produced | hidden from public default unless flagged as candidate |
| `RECONCILED` | spans, amounts, dates and controlled vocabularies pass validation | visible as reconciled but not final |
| `OFFICIAL_RECORD_VERIFIED` | official/court/KAD record verified | canonical public default |
| `GOLD_EXTRACTED` | human-verified gold annotation | benchmark and model-eval layer |
| `QUARANTINED_NON_FIRE` | likely irrelevant dispute | only visible in audit/debug views |
| `FLAGGED_FOR_HUMAN_REVIEW` | contradiction, low confidence or failed reconciliation | visible as unresolved signal |

## Reconciliation checks

Minimum deterministic checks:

- case ID format and normalized Cyrillic/Latin variants;
- cohort marker span present unless manually overridden;
- source locator exists for every extracted field;
- date parse and proceeding order sanity;
- amount parse with currency normalization;
- `awarded_total <= claim_total` warning, not hard failure;
- recovery ratios guarded against zero/unknown denominators;
- evidence quote actually appears in source text;
- no canonical row from LLM candidate without verification state;
- no 2026 row inserted into `SHUS-2024` cohort.

## Daily outputs

The daily job produces:

1. raw discovery snapshot;
2. candidate case delta;
3. quarantined/non-fire delta;
4. act ingestion delta;
5. extraction candidate JSONL;
6. reconciliation report;
7. data PR or issue if canonical write is blocked;
8. dashboard projection manifest including source commit SHA.

## Non-goals

- no bypassing KAD/court terms or access controls;
- no CAPTCHA evasion contract;
- no hidden private database as source of truth;
- no dashboard-only edits to canonical facts;
- no automated legal advice to sellers.
