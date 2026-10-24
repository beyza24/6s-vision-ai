from datetime import datetime, timezone

from app.schemas import Category, Incident, IncidentStatus, Priority, Principle6S
from app.scoring.engine import compute_scores
from app.scoring.explain import build_explanation
from app.scoring.mapping import map_priority


def _incident(**kwargs) -> Incident:
    base = dict(
        id="i1",
        timestamp=datetime.now(timezone.utc),
        category=Category.kke,
        principle_6s=Principle6S.safety,
        title="Baretsiz çalışan",
        priority=Priority.high,
        confidence=0.9,
        status=IncidentStatus.open,
    )
    base.update(kwargs)
    return Incident(**base)


def test_priority_table():
    cases = [
        (Category.kke, Principle6S.safety, Priority.high),
        (Category.trafik, Principle6S.seiton, Priority.high),
        (Category.temizlik, Principle6S.seiso, Priority.low),
        (Category.temizlik, Principle6S.safety, Priority.high),
        (Category.diger, Principle6S.shitsuke, Priority.low),
        (Category.ekipman, Principle6S.seiketsu, Priority.medium),
    ]
    for category, principle, expected in cases:
        assert map_priority(category, principle) == expected


def test_scores_empty_are_full():
    scores = compute_scores([])
    assert scores.safety == 100
    assert scores.overall == 100


def test_open_high_safety_drops_only_that_dimension():
    scores = compute_scores([_incident()])
    assert scores.safety == 88
    assert scores.seiri == 100
    assert scores.overall == 98


def test_repeat_open_incidents_cost_extra():
    one = compute_scores([_incident()])
    two = compute_scores([_incident(id="a"), _incident(id="b")])
    assert two.safety < one.safety


def test_resolved_costs_less_than_open():
    open_scores = compute_scores([_incident()])
    resolved = compute_scores([_incident(status=IncidentStatus.resolved)])
    assert resolved.safety > open_scores.safety


def test_false_alarm_does_not_change_score():
    scores = compute_scores([_incident(status=IncidentStatus.false_alarm)])
    assert scores.safety == 100
    assert scores.overall == 100


def test_explanation_has_text_and_three_actions():
    text, plan = build_explanation(
        title="Baretsiz çalışan",
        category=Category.kke,
        principle=Principle6S.safety,
    )
    assert "Baretsiz çalışan" in text
    assert "Güvenlik" in text
    assert len(plan) == 3
    assert all(plan)
