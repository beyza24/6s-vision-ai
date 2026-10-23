"""K1 API / store acceptance tests."""

from app.schemas import Category, IncidentCreate, IncidentStatus, Principle6S, Priority
from app.store import Store


def test_store_crud():
    s = Store()
    created = s.create_incident(
        IncidentCreate(
            category=Category.kke,
            principle_6s=Principle6S.safety,
            title="Test",
            priority=Priority.high,
            confidence=0.91,
        )
    )
    assert created.id
    assert s.get_incident(created.id).title == "Test"
    assert len(s.list_incidents()) == 1
    updated = s.set_status(created.id, IncidentStatus.false_alarm)
    assert updated.status == IncidentStatus.false_alarm


def test_incident_api_flow(client):
    spawned = client.post("/api/demo/spawn").json()
    rid = spawned["id"]

    detail = client.get(f"/api/incidents/{rid}")
    assert detail.status_code == 200

    conf = client.post(f"/api/incidents/{rid}/confirm")
    assert conf.status_code == 200

    assigned = client.post(
        f"/api/incidents/{rid}/assign",
        json={"assignee": "ISG", "note": "baret"},
    )
    assert assigned.status_code == 200
    assert assigned.json()["status"] == "resolved"
    assert assigned.json()["assignee"] == "ISG"

    scores = client.get("/api/scores/6s")
    assert scores.status_code == 200
    body = scores.json()
    assert "overall" in body
    assert "safety" in body
