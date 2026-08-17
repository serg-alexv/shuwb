# Extraction pipeline

## Goal

Convert judicial acts and related public-source documents into source-grounded candidate observations without allowing model output to become canonical data automatically.

## Pipeline

```text
source discovery
  → source manifest
  → fetch/normalize document
  → deterministic document segmentation
  → LLM/parser extraction candidates
  → schema validation
  → entity/relation reconciliation
  → verification queue
  → canonical normalized tables
  → derived analytics/web build
```

## Model boundary

The extractor may propose:

- case/party/court/judge entities;
- procedural events;
- claim components and amounts;
- strategy use;
- evidence use;
- issue-level findings;
- citations;
- source spans and confidence.

The extractor must not:

- invent a value required by the schema;
- resolve a source conflict silently;
- infer a court finding solely from the final award;
- convert an attorney assertion into a judicial finding;
- mark its own output as `SOURCE_VERIFIED`;
- write directly to canonical datasets.

## OpenAI adapter

Use the Responses API as the default direct extraction interface. Request strict Structured Outputs against a purpose-built JSON schema where supported. Keep the API adapter replaceable: the canonical contract is `schema/extraction_candidate.schema.json`, not a model-specific payload.

For bulk historical ingestion, the Batch API is appropriate for asynchronous corpus processing; every batch request should carry a deterministic `custom_id` derived from source id + segment id so outputs can be reconciled reproducibly.

The runtime reads `OPENAI_API_KEY` from the environment/secret store. Never commit keys or copied secret values.

## Prompt contract

The extraction prompt should require:

1. no completion of missing facts;
2. exact source span for each candidate;
3. explicit distinction between plaintiff, defendant and court statements;
4. one candidate per atomic fact/relation where practical;
5. `UNKNOWN`/`NOT_REACHED` rather than speculative completion;
6. confidence as extraction certainty, not probability that a party wins;
7. warnings for ambiguous units, dates, actors or conflicting amounts.

## Segmentation

Preserve document structure. Segment boundaries should include enough overlap to avoid separating a finding from its reasoning, but deduplicate repeated candidates by source locator and semantic key during reconciliation.

Recommended structural sections where detectable:

- header/case metadata;
- procedural history;
- plaintiff position;
- defendant position;
- evidence discussion;
- legal reasoning;
- operative part;
- appellate/cassation history.

## Reconciliation

Candidate reconciliation is deterministic where possible:

- normalize Russian case-number typography;
- normalize currency and numeric separators without changing value;
- preserve both raw and normalized party names;
- treat remand rounds as separate proceedings;
- do not merge similar strategies unless ontology code matches;
- retain competing quantities/valuations with actor provenance.

## Validation gates

A candidate can advance to canonical data only when:

- JSON/schema validation passes;
- referenced source exists in the manifest;
- source locator/span is non-empty for sourced facts;
- controlled vocabulary values are valid;
- required foreign keys resolve or enter an explicit reconciliation queue;
- verification status is set by the verifier, not the extractor.

## Evaluation set

Before bulk ingestion, manually annotate a gold set spanning:

- at least several first-instance decisions;
- at least several appellate/cassation acts;
- partial grants and total denials;
- conflicting quantity calculations;
- cost/retail/lost-profit valuation arguments;
- evidence admitted, rejected and merely requested;
- remand/repeated-round cases.

Measure entity accuracy, amount/date exact match, relation accuracy, issue-treatment classification, source-span validity and false-positive rate. The most important failure class is a plausible but unsupported canonical fact.

## Audit artifacts

Each extraction run should preserve:

- source commit SHA;
- extractor model/version;
- prompt version/hash;
- schema version;
- request custom id;
- response/request id where available;
- usage/cost metadata where available;
- validation errors;
- reconciliation result;
- verifier action.
