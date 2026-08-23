import pytest
from app.schemas import BookingCreate
from ml.schema import FEATURES
from pydantic import ValidationError


def booking_payload(**overrides):
    payload = {
        "email": "guest@example.com",
        "full_name": "Ada Guest",
        "no_of_adults": 2,
        "no_of_children": 1,
        "no_of_weekend_nights": 1,
        "no_of_week_nights": 3,
        "required_car_parking_space": 1,
        "lead_time": 30,
        "arrival_year": 2025,
        "arrival_month": 8,
        "arrival_date": 15,
        "repeated_guest": 0,
        "no_of_previous_cancellations": 0,
        "no_of_previous_bookings_not_canceled": 2,
        "avg_price_per_room": 125.5,
        "no_of_special_requests": 2,
        "type_of_meal_plan": "Meal Plan 1",
        "room_type_reserved": "Room_Type 1",
        "market_segment_type": "Online",
    }
    payload.update(overrides)
    return payload


def test_booking_create_accepts_complete_feature_contract():
    booking = BookingCreate(**booking_payload())

    assert booking.email == "guest@example.com"
    assert booking.avg_price_per_room == 125.5
    assert booking.room_type_reserved == "Room_Type 1"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("no_of_adults", -1),
        ("no_of_children", 21),
        ("arrival_month", 13),
        ("arrival_year", 1999),
        ("avg_price_per_room", -0.01),
    ],
)
def test_booking_create_rejects_invalid_numeric_boundaries(field, value):
    with pytest.raises(ValidationError):
        BookingCreate(**booking_payload(**{field: value}))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("type_of_meal_plan", "Breakfast only"),
        ("room_type_reserved", "Suite"),
        ("market_segment_type", "Partner"),
    ],
)
def test_booking_create_rejects_unsupported_categories(field, value):
    with pytest.raises(ValidationError):
        BookingCreate(**booking_payload(**{field: value}))


def test_as_form_coerces_string_values():
    form_payload = {
        key: str(value) if isinstance(value, (int, float)) else value
        for key, value in booking_payload().items()
    }

    booking = BookingCreate.as_form(**form_payload)

    assert booking.no_of_adults == 2
    assert booking.avg_price_per_room == 125.5
    assert booking.arrival_year == 2025


def test_model_features_matches_ml_feature_contract():
    features = BookingCreate(**booking_payload()).model_features()

    assert set(features) == set(FEATURES)
    assert len(features) == 17
    assert "email" not in features
    assert "full_name" not in features
