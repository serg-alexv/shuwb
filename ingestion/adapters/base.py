"""
Adapter interfaces for ingestion pipeline.

Concrete implementations are provided externally (not committed here)
because they require credentials and network access to real systems.
Adapters are injected at runtime.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class KADAdapter(ABC):
    """Abstract adapter for official court docket sources (e.g. kad.arbitr.ru).

    Implementations must never invent data. If the remote source is
    unavailable the method must raise ``SourceUnavailable``.
    """

    @abstractmethod
    def fetch_docket(self, case_id: str) -> dict:
        """Return docket metadata for *case_id* as a plain dict.

        Required keys: case_id, court_name, filing_date, parties (list).
        Optional keys: acts (list of act locators), status.
        """

    @abstractmethod
    def fetch_act_text(self, act_locator: str) -> str:
        """Return the full text of a judicial act by its locator."""


class DiscoveryAdapter(ABC):
    """Abstract adapter for discovery-stage source indexers (e.g. sudact.ru)."""

    @abstractmethod
    def search(self, query: str, cohort_tag: str) -> list[dict]:
        """Return a list of discovery candidate records matching *query*.

        Each record must include: case_id, source_url, act_date, act_stage_hint.
        Records are DISCOVERED-stage only; no canonical facts are asserted.
        """


class SourceUnavailable(RuntimeError):
    """Raised when a remote source cannot be reached or returns an error."""


class StubKADAdapter(KADAdapter):
    """In-memory stub for tests. Returns data supplied at construction."""

    def __init__(self, dockets: Optional[dict] = None, acts: Optional[dict] = None):
        self._dockets: dict = dockets or {}
        self._acts: dict = acts or {}

    def fetch_docket(self, case_id: str) -> dict:
        if case_id not in self._dockets:
            raise SourceUnavailable(f"No stub docket for '{case_id}'")
        return dict(self._dockets[case_id])

    def fetch_act_text(self, act_locator: str) -> str:
        if act_locator not in self._acts:
            raise SourceUnavailable(f"No stub act for '{act_locator}'")
        return self._acts[act_locator]
