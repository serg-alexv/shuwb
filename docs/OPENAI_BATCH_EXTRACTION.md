# OpenAI Batch Extraction Adapter

Status: implementation contract for asynchronous extraction jobs. This document describes the adapter boundary; credentials, keys and private artifacts must never be committed.

## Current API assumptions

The Batch API accepts JSONL input files uploaded with purpose `batch` and supports `/v1/responses` as a batch endpoint with a `24h` completion window. The public OpenAI quickstart uses the Responses API as the current default text-generation interface.

Implementation must keep the model name configurable and must not hard-code a historical model as the product contract.

## Boundary

```text
act text + metadata
  -> request JSONL row with custom_id
  -> /v1/responses batch
  -> extraction candidate JSON
  -> local schema validation
  -> reconciliation
  -> data PR / review queue
```

The model produces `candidate` data only. It cannot promote canonical facts.

## JSONL row shape

```json
{
  "custom_id": "SHUS-2024_A41-61831-2024_APPEAL_001",
  "method": "POST",
  "url": "/v1/responses",
  "body": {
    "model": "${OPENAI_EXTRACTION_MODEL}",
    "input": [
      {
        "role": "system",
        "content": "Extract structured litigation data. Return only JSON matching the provided schema. Every non-null factual field must have an evidence span. Do not infer missing facts."
      },
      {
        "role": "user",
        "content": "<ACT_TEXT_AND_METADATA>"
      }
    ],
    "text": {
      "format": {
        "type": "json_schema",
        "name": "litigation_case_extraction",
        "strict": true,
        "schema": "<schema/extraction_candidate.schema.json>"
      }
    }
  }
}
```

## `custom_id` convention

```text
<cohort>_<normalized_case_id>_<instance_or_stage>_<act_sequence>
```

Examples:

```text
SHUS-2024_A41-61831-2024_APPEAL_001
JULY-2026-ELEK_A41-UNKNOWN-FIRST_001
```

## Prompt rules

The extraction prompt must instruct the model to:

- preserve exact case IDs and dates;
- output `null` instead of guessing;
- attach evidence spans to every factual field;
- separate claims, evidence, judicial findings and awards;
- distinguish asserted strategy from court-accepted finding;
- avoid legal advice;
- avoid cross-cohort assumptions;
- return controlled vocabularies only.

## Reconciliation task

After batch output:

1. validate JSON syntax;
2. validate JSON Schema;
3. verify every quote occurs in the source text;
4. normalize amounts and dates;
5. compute derived metrics only in projection code;
6. compare component totals against claim/award totals where available;
7. flag contradictions, missing spans, unsupported fields and impossible state transitions;
8. emit `FLAGGED_FOR_HUMAN_REVIEW` instead of silently correcting.

## Candidate status

Allowed extraction statuses:

- `PARSED_SCHEMA_VALID`
- `PARSED_SCHEMA_INVALID`
- `SPAN_VERIFIED`
- `SPAN_MISSING`
- `AMOUNT_CONFLICT`
- `DATE_CONFLICT`
- `VOCAB_CONFLICT`
- `FLAGGED_FOR_HUMAN_REVIEW`

## Secrets

Use environment variables or CI secrets:

```text
OPENAI_API_KEY
OPENAI_EXTRACTION_MODEL
```

Never commit API keys, raw credentials, cookies or private access tokens.

## Data retention

Public repository records should store source URLs, manifests, extracted facts and provenance. Raw documents may be link-only when redistribution status is uncertain.
