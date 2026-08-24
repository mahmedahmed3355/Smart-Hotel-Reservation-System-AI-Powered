import pandas as pd

from ml.preprocessing import build_preprocessor, prepare_features


def make_frame():
    return pd.DataFrame(
        [
            {
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
            },
            {
                "no_of_adults": 1,
                "no_of_children": 1,
                "no_of_weekend_nights": 0,
                "no_of_week_nights": 3,
                "required_car_parking_space": 1,
                "lead_time": 60,
                "arrival_year": 2018,
                "arrival_month": 9,
                "arrival_date": 20,
                "repeated_guest": 1,
                "no_of_previous_cancellations": 0,
                "no_of_previous_bookings_not_canceled": 1,
                "avg_price_per_room": 140.0,
                "no_of_special_requests": 2,
                "type_of_meal_plan": "Meal Plan 2",
                "room_type_reserved": "Room_Type 2",
                "market_segment_type": "Corporate",
            },
        ]
    )


def test_preprocessor_is_deterministic():
    frame = make_frame()
    prepared = prepare_features(frame)

    first = build_preprocessor()
    second = build_preprocessor()

    first_output = first.fit_transform(prepared)
    second_output = second.fit_transform(prepared)

    assert first_output.shape == (2, 17)
    assert second_output.shape == (2, 17)
    assert (first_output == second_output).all()


def test_unknown_category_is_supported():
    frame = make_frame()
    prepared = prepare_features(frame)

    preprocessor = build_preprocessor()
    preprocessor.fit(prepared)

    unknown = frame.iloc[[0]].copy()
    unknown["market_segment_type"] = "Unknown-Segment"

    output = preprocessor.transform(
        prepare_features(unknown)
    )

    assert output.shape == (1, 17)
