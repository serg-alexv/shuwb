"""
SHUWB ingestion state machine.

State transitions:
    DISCOVERED → KAD_SYNCED → ACT_INGESTED → LLM_EXTRACTED
    → RECONCILED → OFFICIAL_RECORD_VERIFIED

Side-exit states available from any state:
    → QUARANTINED_NON_FIRE
    → FLAGGED_FOR_HUMAN_REVIEW

This module only orchestrates state transitions and validates
transition preconditions. No fake API calls are made.
All I/O is delegated to adapter interfaces.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class State(str, Enum):
    DISCOVERED = "DISCOVERED"
    KAD_SYNCED = "KAD_SYNCED"
    ACT_INGESTED = "ACT_INGESTED"
    LLM_EXTRACTED = "LLM_EXTRACTED"
    RECONCILED = "RECONCILED"
    OFFICIAL_RECORD_VERIFIED = "OFFICIAL_RECORD_VERIFIED"
    GOLD_EXTRACTED = "GOLD_EXTRACTED"
    QUARANTINED_NON_FIRE = "QUARANTINED_NON_FIRE"
    FLAGGED_FOR_HUMAN_REVIEW = "FLAGGED_FOR_HUMAN_REVIEW"


# Allowed forward transitions (exits to quarantine/review from any state
# are handled separately in StateMachine.transition).
_FORWARD: dict[State, list[State]] = {
    State.DISCOVERED: [State.KAD_SYNCED],
    State.KAD_SYNCED: [State.ACT_INGESTED],
    State.ACT_INGESTED: [State.LLM_EXTRACTED],
    State.LLM_EXTRACTED: [State.RECONCILED],
    State.RECONCILED: [State.OFFICIAL_RECORD_VERIFIED],
    State.OFFICIAL_RECORD_VERIFIED: [State.GOLD_EXTRACTED],
    State.QUARANTINED_NON_FIRE: [State.DISCOVERED],
    State.FLAGGED_FOR_HUMAN_REVIEW: [
        State.DISCOVERED,
        State.KAD_SYNCED,
        State.ACT_INGESTED,
        State.RECONCILED,
        State.QUARANTINED_NON_FIRE,
    ],
    State.GOLD_EXTRACTED: [],
}

_SIDE_EXIT = {State.QUARANTINED_NON_FIRE, State.FLAGGED_FOR_HUMAN_REVIEW}

# Forbidden shortcut
_FORBIDDEN: set[tuple[State, State]] = {
    (State.DISCOVERED, State.OFFICIAL_RECORD_VERIFIED),
    (State.LLM_EXTRACTED, State.OFFICIAL_RECORD_VERIFIED),
}


@dataclass
class TransitionEvent:
    from_state: State
    to_state: State
    reason: str
    timestamp: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )


@dataclass
class CaseRecord:
    case_id: str
    incident_id: str
    discovery_source_id: str
    state: State = State.DISCOVERED
    history: list[TransitionEvent] = field(default_factory=list)
    # Populated as the record advances through the pipeline
    kad_metadata: Optional[dict] = None
    act_locator: Optional[str] = None
    extraction_candidate_id: Optional[str] = None
    reconciliation_report_id: Optional[str] = None
    official_record_locator: Optional[str] = None


class TransitionError(ValueError):
    pass


class StateMachine:
    """Orchestrate state transitions for a CaseRecord.

    Usage::

        sm = StateMachine(record)
        sm.transition(State.KAD_SYNCED, reason="docket synced via KAD adapter")
    """

    def __init__(self, record: CaseRecord) -> None:
        self.record = record

    def transition(self, target: State, reason: str) -> None:
        if not reason:
            raise TransitionError("reason is required for every transition")

        current = self.record.state

        if (current, target) in _FORBIDDEN:
            raise TransitionError(
                f"Forbidden transition: {current} → {target}. {reason}"
            )

        allowed = _FORWARD.get(current, []) + list(_SIDE_EXIT)
        if target not in allowed:
            raise TransitionError(
                f"Invalid transition: {current} → {target}. "
                f"Allowed: {[s.value for s in allowed]}"
            )

        event = TransitionEvent(from_state=current, to_state=target, reason=reason)
        self.record.history.append(event)
        self.record.state = target
