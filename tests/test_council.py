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


def test_chairman_synthesis_and_dissent_are_turkish():
    incident = _incident().model_copy(update={"confidence": 0.55})
    verdict = run_council(incident, prefer_live=False)
    assert verdict.is_violation is True
    assert "Öneri:" in verdict.synthesis
    assert "Son karar İSG uzmanındadır." in verdict.synthesis
    assert verdict.dissent.startswith("Muhalif görüş")


def test_missing_keys_stay_on_fake(monkeypatch):
    for name in (
        "OPENAI_API_KEY",
        "COUNCIL_API_KEY",
        "OPENROUTER_API_KEY",
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
        "COUNCIL_MEMBERS",
    ):
        monkeypatch.delenv(name, raising=False)
    verdict = run_council(_incident(), prefer_live=True)
    assert verdict.mode == "fake"
    assert len(verdict.votes) == 3


def test_two_live_members_vote(monkeypatch):
    monkeypatch.setenv(
        "COUNCIL_MEMBERS",
        "openai:gpt-4o-mini,openrouter:anthropic/claude-3.5-sonnet",
    )
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-router")

    class _Response:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {
                "choices": [
                    {
                        "message": {
                            "content": (
                                '{"is_violation":true,"principle_6s":"safety",'
                                '"priority":"high","confidence":0.91,"rationale":"baret yok"}'
                            )
                        }
                    }
                ]
            }

    class _Client:
        def __init__(self, *args, **kwargs) -> None:
            return None

        def __enter__(self):
            return self

        def __exit__(self, *args) -> bool:
            return False

        def post(self, url, headers, json):
            assert headers["Authorization"].startswith("Bearer ")
            assert url.endswith("/chat/completions")
            return _Response()

    monkeypatch.setattr("app.council.live.httpx.Client", _Client)
    verdict = run_council(_incident(), prefer_live=True)
    assert verdict.mode == "live"
    assert len(verdict.votes) >= 2
    assert "Son karar İSG uzmanındadır." in verdict.synthesis


def test_council_endpoint(client):
    spawned = client.post("/api/demo/spawn").json()
    rid = spawned["id"]
    r = client.post(f"/api/incidents/{rid}/council")
    assert r.status_code == 200
    body = r.json()
    assert body["council"] is not None
    assert len(body["council"]["votes"]) >= 2
    assert "synthesis" in body["council"]
