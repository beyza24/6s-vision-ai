import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import store


@pytest.fixture()
def client():
    store.incidents.clear()
    store.rules.clear()
    with TestClient(app) as c:
        yield c
