def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_demo_spawn_and_false_alarm(client):
    r = client.post("/api/demo/spawn")
    assert r.status_code == 200
    incident = r.json()
    assert incident["title"]
    assert incident["confidence"] >= 0.9

    rid = incident["id"]
    listed = client.get("/api/incidents").json()
    assert any(i["id"] == rid for i in listed)

    fa = client.post(f"/api/incidents/{rid}/false-alarm")
    assert fa.status_code == 200
    assert fa.json()["status"] == "false_alarm"
