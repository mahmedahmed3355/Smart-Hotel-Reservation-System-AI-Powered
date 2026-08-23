from __future__ import annotations

from dataclasses import dataclass

NUMERIC_FEATURES = (
    "no_of_adults",
    "no_of_children",
    "no_of_weekend_nights",
    "no_of_week_nights",
    "required_car_parking_space",
    "lead_time",
    "arrival_year",
    "arrival_month",
    "arrival_date",
    "repeated_guest",
    "no_of_previous_cancellations",
    "no_of_previous_bookings_not_canceled",
    "avg_price_per_room",
    "no_of_special_requests",
)

CATEGORICAL_FEATURES = (
    "type_of_meal_plan",
    "room_type_reserved",
    "market_segment_type",
)

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

TARGET_COLUMN = "booking_status"

CATEGORICAL_VALUES = {
    "type_of_meal_plan": (
        "Meal Plan 1",
        "Meal Plan 2",
        "Meal Plan 3",
        "Not Selected",
    ),
    "room_type_reserved": (
        "Room_Type 1",
        "Room_Type 2",
        "Room_Type 3",
        "Room_Type 4",
        "Room_Type 5",
        "Room_Type 6",
        "Room_Type 7",
    ),
    "market_segment_type": (
        "Aviation",
        "Complementary",
        "Corporate",
        "Offline",
        "Online",
    ),
}


@dataclass(frozen=True)
class FeatureSchema:
    features: tuple[str, ...] = FEATURES
    numeric_features: tuple[str, ...] = NUMERIC_FEATURES
    categorical_features: tuple[str, ...] = CATEGORICAL_FEATURES


SCHEMA = FeatureSchema()
