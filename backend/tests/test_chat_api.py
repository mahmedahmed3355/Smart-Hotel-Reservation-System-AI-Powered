import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from app.chat_api import router


def build_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_chat_endpoint_returns_offer_reply(monkeypatch):
    monkeypatch.setattr(
        "app.chat_api.reply",
        lambda message, last_score, loyalty_points: "mocked offer reply",
    )

    client = build_client()

    response = client.post(
        "/chat/",
        json={
            "message": "show me offers",
            "last_score": 0.9,
            "loyalty_points": 100,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"reply": "mocked offer reply"}


def test_chat_endpoint_uses_default_values(monkeypatch):
    captured = {}

    def fake_reply(message, last_score, loyalty_points):
        captured["message"] = message
        captured["last_score"] = last_score
        captured["loyalty_points"] = loyalty_points
        return "ok"

    monkeypatch.setattr("app.chat_api.reply", fake_reply)

    client = build_client()

    response = client.post(
        "/chat/",
        json={"message": "hello"},
    )

    assert response.status_code == 200
    assert response.json() == {"reply": "ok"}
    assert captured == {
        "message": "hello",
        "last_score": 0.7,
        "loyalty_points": 0,
    }


def test_chat_schema_rejects_invalid_payload():
    client = build_client()

    response = client.post(
        "/chat/",
        json={"last_score": "not-a-number"},
    )

    assert response.status_code == 422
