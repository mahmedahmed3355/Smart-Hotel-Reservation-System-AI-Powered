from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

pytest.importorskip("multipart")

import app.api as booking_api
from app.main import app


class FakeSession:
    def __init__(self):
        self.added = []
        self.commit_calls = 0
        self.refresh_calls = 0

    def add(self, instance):
        self.added.append(instance)

    def commit(self):
        self.commit_calls += 1

    def refresh(self, instance):
        self.refresh_calls += 1
        instance.id = 321

    def rollback(self):
        pass


def multipart_data(**overrides):
    data = {
        "email": "guest@example.com",
        "full_name": "Submitted Name",
        "no_of_adults": "2",
        "no_of_children": "1",
        "no_of_weekend_nights": "1",
        "no_of_week_nights": "3",
        "required_car_parking_space": "0",
        "lead_time": "30",
        "arrival_year": "2025",
        "arrival_month": "8",
        "arrival_date": "15",
        "repeated_guest": "0",
        "no_of_previous_cancellations": "0",
        "no_of_previous_bookings_not_canceled": "1",
        "avg_price_per_room": "125.5",
        "no_of_special_requests": "2",
        "type_of_meal_plan": "Meal Plan 1",
        "room_type_reserved": "Room_Type 1",
        "market_segment_type": "Online",
    }
    data.update(overrides)
    return data


@pytest.fixture
def api_client(monkeypatch):
    session = FakeSession()
    extract_from_id = Mock(
        return_value={
            "email": "GUEST@EXAMPLE.COM",
            "full_name": "OCR Name",
            "raw_text": "ID document text",
        }
    )
    upload_to_gcs = Mock(return_value="https://storage.example/id.png")
    predict_score = Mock(return_value=0.85)

    monkeypatch.setattr(booking_api, "extract_from_id", extract_from_id)
    monkeypatch.setattr(booking_api, "upload_to_gcs", upload_to_gcs)
    monkeypatch.setattr(booking_api, "predict_score", predict_score)
    app.dependency_overrides[booking_api.get_db] = lambda: session

    with TestClient(app) as client:
        yield client, session, extract_from_id, upload_to_gcs, predict_score

    app.dependency_overrides.clear()


def post_booking(client, data):
    return client.post(
        "/bookings/",
        data=data,
        files={"id_image": ("id.png", b"fake image", "image/png")},
    )


def test_create_booking_runs_successful_multipart_flow(api_client):
    client, session, ocr, upload, predict = api_client

    response = post_booking(client, multipart_data())

    assert response.status_code == 200
    body = response.json()
    assert body == {
        "accepted": True,
        "score": 0.85,
        "offers": {
            "score": 0.85,
            "offers": [
                {"type": "half_price", "value": 0.5},
                {"type": "extra_week", "value": 7},
                {"type": "free_meal", "value": 1},
            ],
        },
        "database_id": 321,
        "booking_id": body["booking_id"],
        "image_url": "https://storage.example/id.png",
    }
    assert body["booking_id"].startswith("BKG-")
    assert len(session.added) == 1
    assert session.commit_calls == 1
    assert session.refresh_calls == 1
    ocr.assert_called_once()
    upload.assert_called_once()
    predict.assert_called_once_with(
        {
            "no_of_adults": 2,
            "no_of_children": 1,
            "no_of_weekend_nights": 1,
            "no_of_week_nights": 3,
            "required_car_parking_space": 0,
            "lead_time": 30,
            "arrival_year": 2025,
            "arrival_month": 8,
            "arrival_date": 15,
            "repeated_guest": 0,
            "no_of_previous_cancellations": 0,
            "no_of_previous_bookings_not_canceled": 1,
            "avg_price_per_room": 125.5,
            "no_of_special_requests": 2,
            "type_of_meal_plan": "Meal Plan 1",
            "room_type_reserved": "Room_Type 1",
            "market_segment_type": "Online",
        }
    )

    persisted = session.added[0]
    assert persisted.full_name == "Submitted Name"
    assert persisted.customer_image_path == "https://storage.example/id.png"
    assert persisted.ocr_raw_text == "ID document text"
    assert persisted.is_verified is True
    assert persisted.prediction_score == 0.85
    assert persisted.discounts == body["offers"]
    assert persisted.booking_id == body["booking_id"]


def test_create_booking_uses_ocr_name_and_rejects_mismatched_email(api_client):
    client, session, ocr, upload, predict = api_client
    ocr.return_value = {
        "email": "other@example.com",
        "full_name": "OCR Fallback Name",
        "raw_text": "other document",
    }
    predict.return_value = 0.7

    response = post_booking(client, multipart_data(full_name=""))

    assert response.status_code == 200
    assert response.json()["accepted"] is False
    persisted = session.added[0]
    assert persisted.full_name == "OCR Fallback Name"
    assert persisted.is_verified is False
    assert persisted.prediction_score == 0.7
    assert upload.called


def test_create_booking_rejects_score_below_threshold(api_client):
    client, session, _ocr, upload, predict = api_client
    predict.return_value = 0.49

    response = post_booking(client, multipart_data())

    assert response.status_code == 200
    assert response.json()["accepted"] is False
    persisted = session.added[0]
    assert persisted.is_verified is True
    assert persisted.prediction_score == 0.49
    assert upload.called


def test_invalid_booking_does_not_call_external_dependencies(api_client):
    client, session, ocr, upload, predict = api_client

    response = post_booking(client, multipart_data(no_of_adults="-1"))

    assert response.status_code == 422
    ocr.assert_not_called()
    upload.assert_not_called()
    predict.assert_not_called()
    assert session.added == []
    assert session.commit_calls == 0
    assert session.refresh_calls == 0

def test_create_booking_returns_502_when_ocr_fails(api_client):
    client, session, ocr, upload, predict = api_client
    ocr.side_effect = RuntimeError("ocr unavailable")

    response = post_booking(client, multipart_data())

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Unable to process identification image."
    )
    upload.assert_not_called()
    predict.assert_not_called()
    assert session.added == []
    assert session.commit_calls == 0


def test_create_booking_returns_502_when_upload_fails(api_client):
    client, session, _ocr, upload, predict = api_client
    upload.side_effect = RuntimeError("storage unavailable")

    response = post_booking(client, multipart_data())

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Unable to store identification image."
    )
    predict.assert_not_called()
    assert session.added == []
    assert session.commit_calls == 0


def test_create_booking_rolls_back_when_database_commit_fails(
    api_client,
):
    client, session, _ocr, _upload, _predict = api_client
    rollback = Mock()
    session.rollback = rollback

    def fail_commit():
        session.commit_calls += 1
        raise RuntimeError("database unavailable")

    session.commit = fail_commit

    response = post_booking(client, multipart_data())

    assert response.status_code == 500
    assert response.json()["detail"] == "Unable to save booking."
    rollback.assert_called_once()
    assert len(session.added) == 1
