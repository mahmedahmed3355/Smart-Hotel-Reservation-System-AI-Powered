import pandas as pd
import pytest

from ml.preprocessing import prepare_features
from ml.schema import (
    CATEGORICAL_FEATURES,
    FEATURES,
    NUMERIC_FEATURES,
)


def test_feature_schema_has_17_features():
    assert len(FEATURES) == 17
    assert len(NUMERIC_FEATURES) == 14
    assert len(CATEGORICAL_FEATURES) == 3
    assert len(set(FEATURES)) == 17


def test_prepare_features_preserves_contract():
    frame = pd.DataFrame(
        [{
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
        }]
    )

    prepared = prepare_features(frame)

    assert list(prepared.columns) == list(FEATURES)
    assert prepared.shape == (1, 17)


def test_prepare_features_rejects_missing_columns():
    frame = pd.DataFrame([{"no_of_adults": 2}])

    with pytest.raises(ValueError, match="Missing required features"):
        prepare_features(frame)
