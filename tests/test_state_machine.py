"""
State machine tests using fixture data from the repository.
Run: python -m tests.test_state_machine
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from ingestion.state_machine import (  # noqa: E402
    CaseRecord,
    State,
    StateMachine,
    TransitionError,
)


class TestForwardTransitions(unittest.TestCase):
    def _record(self) -> CaseRecord:
        return CaseRecord(
            case_id="А41-21723/2024",
            incident_id="SHUS-2024",
            discovery_source_id="SRC-SUDACT-A41-21723-2024-FI",
        )

    def test_happy_path(self):
        rec = self._record()
        sm = StateMachine(rec)
        steps = [
            (State.KAD_SYNCED, "docket fetched from KAD stub"),
            (State.ACT_INGESTED, "act text retrieved"),
            (State.LLM_EXTRACTED, "extraction candidate produced"),
            (State.RECONCILED, "reconciliation report passed"),
            (State.OFFICIAL_RECORD_VERIFIED, "official record confirmed by human"),
        ]
        for target, reason in steps:
            sm.transition(target, reason=reason)
        self.assertEqual(rec.state, State.OFFICIAL_RECORD_VERIFIED)
        self.assertEqual(len(rec.history), 5)

    def test_reason_required(self):
        rec = self._record()
        sm = StateMachine(rec)
        with self.assertRaises(TransitionError):
            sm.transition(State.KAD_SYNCED, reason="")

    def test_forbidden_shortcut_discovered_to_verified(self):
        rec = self._record()
        sm = StateMachine(rec)
        with self.assertRaises(TransitionError):
            sm.transition(State.OFFICIAL_RECORD_VERIFIED, reason="shortcut")

    def test_forbidden_llm_to_verified(self):
        rec = self._record()
        sm = StateMachine(rec)
        sm.transition(State.KAD_SYNCED, reason="ok")
        sm.transition(State.ACT_INGESTED, reason="ok")
        sm.transition(State.LLM_EXTRACTED, reason="ok")
        with self.assertRaises(TransitionError):
            sm.transition(State.OFFICIAL_RECORD_VERIFIED, reason="model self-verify")

    def test_side_exit_quarantine(self):
        rec = self._record()
        sm = StateMachine(rec)
        sm.transition(State.KAD_SYNCED, reason="ok")
        sm.transition(State.QUARANTINED_NON_FIRE, reason="not a fire case")
        self.assertEqual(rec.state, State.QUARANTINED_NON_FIRE)

    def test_flag_for_review(self):
        rec = self._record()
        sm = StateMachine(rec)
        sm.transition(State.FLAGGED_FOR_HUMAN_REVIEW, reason="source mismatch")
        self.assertEqual(rec.state, State.FLAGGED_FOR_HUMAN_REVIEW)

    def test_invalid_transition(self):
        rec = self._record()
        sm = StateMachine(rec)
        with self.assertRaises(TransitionError):
            sm.transition(State.GOLD_EXTRACTED, reason="bad jump")


if __name__ == "__main__":
    unittest.main()
