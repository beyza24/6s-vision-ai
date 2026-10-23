from app.council.deliberate import run_council
from app.schemas import Category, Incident, IncidentStatus, Principle6S, Priority
from datetime import datetime, timezone


def _incident() -> Incident:
    return Incident(
        id="t1",
        camera_id="cam-1",
        timestamp=datetime.now(timezone.utc),
        category=Category.kke,
        principle_6s=Principle6S.safety,
        title="Baretsiz çalışan",
        description="Hat 2",
        priority=Priority.high,
        confidence=0.94,
        status=IncidentStatus.open,
    )


def test_fake_council_returns_votes_and_synthesis():
    verdict = run_council(_incident(), prefer_live=False)
    assert verdict.mode == "fake"
    assert len(verdict.votes) == 3
    assert verdict.human_final is True
    assert verdict.synthesis
    assert verdict.is_violation is True


def test_council_endpoint(client):
    spawned = client.post("/api/demo/spawn").json()
    rid = spawned["id"]
    r = client.post(f"/api/incidents/{rid}/council")
    assert r.status_code == 200
    body = r.json()
    assert body["council"] is not None
    assert len(body["council"]["votes"]) >= 2
    assert "synthesis" in body["council"]
