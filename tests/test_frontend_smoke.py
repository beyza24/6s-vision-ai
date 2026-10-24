from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "frontend"


def test_panel_has_demo_gates_scores_and_council():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    assert "styles.css" in html and "app.js" in html and "mock.js" in html
    for marker in ("btn-demo", "btn-confirm", "btn-false", "btn-assign", "btn-council", "incident-list", "scores"):
        assert marker in html
    assert "Demo: yeni tespit" in html
    assert "Konseyi çalıştır" in html
    assert 'className = "chip ' in js
    assert "/api/demo/spawn" in js
    assert "/council" in js
    assert "/confirm" in js
    assert "/false-alarm" in js
    assert "/assign" in js


def test_frontend_is_served(client):
    page = client.get("/")
    assert page.status_code == 200
    assert "6S-VISION AI" in page.text
    assert "btn-council" in page.text
