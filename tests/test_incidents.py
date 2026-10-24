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


def test_rule_routes_fake_then_approve(client):
    parsed = client.post("/api/rules/parse", json={"text": "Hat 2'de baret zorunlu"})
    assert parsed.status_code == 200
    draft = parsed.json()
    assert draft["status"] == "pending_approval"
    assert "baret" in draft["raw_text"]
    assert draft["id"]

    approved = client.post(f"/api/rules/{draft['id']}/approve")
    assert approved.status_code == 200
    assert approved.json()["status"] == "active"


def test_openapi_lists_incident_routes(client):
    spec = client.get("/openapi.json")
    assert spec.status_code == 200
    paths = spec.json()["paths"]
    for path in (
        "/health",
        "/api/incidents",
        "/api/incidents/{incident_id}",
        "/api/incidents/{incident_id}/confirm",
        "/api/incidents/{incident_id}/false-alarm",
        "/api/incidents/{incident_id}/assign",
        "/api/scores/6s",
        "/api/rules/parse",
        "/api/rules/{rule_id}/approve",
        "/api/demo/spawn",
        "/api/incidents/{incident_id}/council",
    ):
        assert path in paths
