"""6S skor motoru. Sahip: k3. Saf fonksiyon; store'a yazmaz."""
from __future__ import annotations

from app.schemas import Incident, IncidentStatus, Priority, Principle6S, Scores6S

_OPEN_PENALTY = {Priority.high: 12.0, Priority.medium: 8.0, Priority.low: 4.0}
_REVIEW_PENALTY = 6.0
_RESOLVED_PENALTY = 2.0
_REPEAT_PENALTY = 10.0


def compute_scores(incidents: list[Incident]) -> Scores6S:
    scores = {principle: 100.0 for principle in Principle6S}
    groups: dict[tuple[Principle6S, str], list[Incident]] = {}
    for incident in incidents:
        if incident.status == IncidentStatus.false_alarm:
            continue
        key = (incident.principle_6s, incident.title.strip().lower())
        groups.setdefault(key, []).append(incident)

    for (principle, _title), group in groups.items():
        open_count = sum(1 for item in group if item.status != IncidentStatus.resolved)
        for item in group:
            if item.status == IncidentStatus.resolved:
                scores[principle] -= _RESOLVED_PENALTY
            elif item.status == IncidentStatus.review:
                scores[principle] -= _REVIEW_PENALTY
            else:
                scores[principle] -= _OPEN_PENALTY[item.priority]
        if open_count >= 2:
            scores[principle] -= _REPEAT_PENALTY

    bounded = {principle: round(min(100.0, max(0.0, value)), 1) for principle, value in scores.items()}
    overall = round(sum(bounded.values()) / len(bounded), 1)
    return Scores6S(
        seiri=bounded[Principle6S.seiri],
        seiton=bounded[Principle6S.seiton],
        seiso=bounded[Principle6S.seiso],
        seiketsu=bounded[Principle6S.seiketsu],
        shitsuke=bounded[Principle6S.shitsuke],
        safety=bounded[Principle6S.safety],
        overall=overall,
    )
