import pandas as pd
import pytest

from app.inference import predict_score
from ml.schema import FEATURES


def make_payload():
    return {
        "no_of_adults": 2,
        "no_of_children": 0,
        "no_of_weekend_nights": 1,
        "no_of_week_nights": 2,
        "required_car_parking_space": 0,
        "lead_time": 30,
        "arrival_year": 2018,
        "arrival_month": 8,
        "arrival_date": 15,
        "repeated_guest": 0,
        "no_of_previous_cancellations": 0,
        "no_of_previous_bookings_not_canceled": 0,
        "avg_price_per_room": 100.0,
        "no_of_special_requests": 1,
        "type_of_meal_plan": "Meal Plan 1",
        "room_type_reserved": "Room_Type 1",
        "market_segment_type": "Online",
    }


def test_predict_score_returns_probability():
    score = predict_score(make_payload())

    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0


def test_predict_score_rejects_missing_features():
    with pytest.raises(ValueError, match="Missing required features"):
        predict_score({"no_of_adults": 2})


def test_real_dataset_row_matches_feature_contract():
    frame = pd.read_csv("data/Hotel Reservations.csv")
    row = frame.iloc[0].drop(
        labels=["Booking_ID", "booking_status"]
    ).to_dict()

    assert set(row.keys()) == set(FEATURES)

    score = predict_score(row)

    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0
