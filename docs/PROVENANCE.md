# Provenance and verification contract

## Principle

An LLM extraction is never a canonical fact by itself. It is a candidate assertion linked to source evidence.

## Required provenance fields

Every sourced observation should be able to resolve to:

- `source_id`
- `source_url`
- `source_type`
- `retrieved_at`
- `document_date`
- `document_hash` when bytes are archived lawfully
- `page_or_section`
- `paragraph_or_locator`
- `source_span`
- `extractor_type` (`human`, `llm`, `parser`, `import`)
- `extractor_name_version`
- `extracted_at`
- `confidence`
- `verification_status`
- `verified_by`
- `verification_note`

## Verification states

- `UNVERIFIED` — extraction has not been checked against source.
- `SOURCE_VERIFIED` — value and context checked against the cited source.
- `CROSS_VERIFIED` — corroborated by at least one independent source or authoritative record.
- `CONFLICTED` — credible sources disagree; no silent resolution.
- `RETRACTED` — previously accepted observation invalidated.

## Epistemic states

Keep these distinct from verification:

- `CONFIRMED` — directly supported by source evidence.
- `INFERRED` — reasoned from confirmed observations; inference rule must be recorded.
- `UNKNOWN` — insufficient evidence.
- `NOT_APPLICABLE` — field is semantically inapplicable.
- `NOT_REACHED` — court did not decide the issue.

## Source hierarchy

Prefer authoritative primary sources for canonical litigation facts: judicial acts/card data and official documents. Secondary reporting can discover cases, incidents or disputed facts but should not overwrite a conflicting primary source without explicit conflict handling.

## Raw documents

Do not assume the repository has redistribution rights to every source document. When redistribution status is unclear, store metadata, hash and stable source locator rather than copying third-party content wholesale.

## Reproducibility

Any derived dataset or visualization build must record:

- source commit SHA;
- schema version;
- transformation version;
- build timestamp;
- rows rejected/quarantined and reasons.
