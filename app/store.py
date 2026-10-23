"""In-memory store — k1 only."""
from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from typing import Optional
from uuid import uuid4

from app.schemas import (
    AssignBody,
    Incident,
    IncidentCreate,
    IncidentStatus,
    RuleDraft,
)


class Store:
    def __init__(self) -> None:
        self._lock = Lock()
        self.incidents: dict[str, Incident] = {}
        self.rules: dict[str, RuleDraft] = {}

    def list_incidents(self) -> list[Incident]:
        with self._lock:
            return sorted(self.incidents.values(), key=lambda i: i.timestamp, reverse=True)

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        with self._lock:
            return self.incidents.get(incident_id)

    def create_incident(self, body: IncidentCreate) -> Incident:
        incident = Incident(
            id=str(uuid4()),
            timestamp=datetime.now(timezone.utc),
            **body.model_dump(),
        )
        with self._lock:
            self.incidents[incident.id] = incident
        return incident

    def set_status(self, incident_id: str, status: IncidentStatus) -> Optional[Incident]:
        with self._lock:
            item = self.incidents.get(incident_id)
            if not item:
                return None
            updated = item.model_copy(update={"status": status})
            self.incidents[incident_id] = updated
            return updated

    def assign(self, incident_id: str, body: AssignBody) -> Optional[Incident]:
        with self._lock:
            item = self.incidents.get(incident_id)
            if not item:
                return None
            updated = item.model_copy(update={"assignee": body.assignee})
            self.incidents[incident_id] = updated
            return updated

    def set_council(self, incident_id: str, council) -> Optional[Incident]:
        with self._lock:
            item = self.incidents.get(incident_id)
            if not item:
                return None
            updates: dict = {"council": council}
            # Konsey önerisi alanları günceller; insan hâlâ onaylar
            if council is not None:
                updates.update(
                    {
                        "principle_6s": council.principle_6s,
                        "priority": council.priority,
                        "confidence": council.confidence,
                        "ai_explanation": council.synthesis or item.ai_explanation,
                    }
                )
                if not council.is_violation:
                    updates["status"] = IncidentStatus.review
            updated = item.model_copy(update=updates)
            self.incidents[incident_id] = updated
            return updated

    def add_rule(self, rule: RuleDraft) -> RuleDraft:
        with self._lock:
            self.rules[rule.id] = rule
        return rule

    def get_rule(self, rule_id: str) -> Optional[RuleDraft]:
        with self._lock:
            return self.rules.get(rule_id)

    def approve_rule(self, rule_id: str) -> Optional[RuleDraft]:
        with self._lock:
            rule = self.rules.get(rule_id)
            if not rule:
                return None
            updated = rule.model_copy(update={"status": "active"})
            self.rules[rule_id] = updated
            return updated


store = Store()
