"""
Data validation tests for SHUWB Litigation Observatory.
Run: python -m tests.validate_data
Requires: Python ≥ 3.8, stdlib only.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
CASES_CSV = ROOT / "data" / "cases" / "discovery_shus_2024.csv"
SOURCES_CSV = ROOT / "data" / "sources" / "source_manifest.csv"

ALLOWED_CENSUS_STATUSES = {"DISCOVERED", "KAD_SYNCED", "ACT_INGESTED",
                            "LLM_EXTRACTED", "RECONCILED",
                            "OFFICIAL_RECORD_VERIFIED", "QUARANTINED_NON_FIRE",
                            "FLAGGED_FOR_HUMAN_REVIEW"}
ALLOWED_STAGE_HINTS = {"FIRST", "APPEAL", "CASSATION", "SUPREME_COURT", "OTHER"}
BOOLEAN_VALUES = {"true", "false"}

# Fields required when official_record_verified=true
OFFICIAL_PROVENANCE_FIELDS = ["official_record_locator", "verified_by", "verified_at"]

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)
    print(f"ERROR: {msg}", file=sys.stderr)


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def validate_sources(rows: list[dict]) -> set[str]:
    source_ids: set[str] = set()
    for i, row in enumerate(rows, start=2):
        sid = row.get("source_id", "").strip()
        if not sid:
            err(f"source_manifest row {i}: missing source_id")
            continue
        if sid in source_ids:
            err(f"source_manifest row {i}: duplicate source_id '{sid}'")
        source_ids.add(sid)
    return source_ids


def validate_cases(rows: list[dict], source_ids: set[str]) -> None:
    seen_case_ids: set[str] = set()
    for i, row in enumerate(rows, start=2):
        case_id = row.get("case_id", "").strip()
        incident_id = row.get("incident_id", "").strip()
        discovery_source_id = row.get("discovery_source_id", "").strip()
        census_status = row.get("census_status", "").strip()
        act_stage_hint = row.get("act_stage_hint", "").strip()
        official_record_verified = row.get("official_record_verified", "").strip().lower()

        if not case_id:
            err(f"cases row {i}: missing case_id")
            continue

        # Unique case_id
        if case_id in seen_case_ids:
            err(f"cases row {i}: duplicate case_id '{case_id}'")
        seen_case_ids.add(case_id)

        # discovery_source_id resolves to source manifest
        if discovery_source_id not in source_ids:
            err(
                f"cases row {i} (case_id={case_id}): "
                f"discovery_source_id '{discovery_source_id}' not found in source_manifest"
            )

        # Allowed census_status
        if census_status and census_status not in ALLOWED_CENSUS_STATUSES:
            err(
                f"cases row {i} (case_id={case_id}): "
                f"invalid census_status '{census_status}'"
            )

        # Allowed act_stage_hint
        if act_stage_hint and act_stage_hint not in ALLOWED_STAGE_HINTS:
            err(
                f"cases row {i} (case_id={case_id}): "
                f"invalid act_stage_hint '{act_stage_hint}'"
            )

        # Boolean values
        if official_record_verified not in BOOLEAN_VALUES:
            err(
                f"cases row {i} (case_id={case_id}): "
                f"official_record_verified must be 'true' or 'false', got '{official_record_verified}'"
            )

        # If official_record_verified=true, provenance fields must be present
        if official_record_verified == "true":
            for field in OFFICIAL_PROVENANCE_FIELDS:
                if not row.get(field, "").strip():
                    err(
                        f"cases row {i} (case_id={case_id}): "
                        f"official_record_verified=true but required field '{field}' is empty"
                    )


def main() -> int:
    print(f"Validating {CASES_CSV} …")
    print(f"Validating {SOURCES_CSV} …")

    if not CASES_CSV.exists():
        err(f"Missing file: {CASES_CSV}")
    if not SOURCES_CSV.exists():
        err(f"Missing file: {SOURCES_CSV}")

    if errors:
        print(f"\n{len(errors)} error(s) found.", file=sys.stderr)
        return 1

    source_rows = load_csv(SOURCES_CSV)
    source_ids = validate_sources(source_rows)

    case_rows = load_csv(CASES_CSV)
    validate_cases(case_rows, source_ids)

    if errors:
        print(f"\n{len(errors)} validation error(s).", file=sys.stderr)
        return 1

    print(
        f"OK — {len(case_rows)} cases, {len(source_rows)} sources validated with no errors."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
