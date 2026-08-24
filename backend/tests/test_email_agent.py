import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from agents.email_agent import (
    parse_booking_body,
    validate_booking_payload,
)

VALID_BODY = """
Email: guest@example.com
Name: Mohamed Ahmed
Adults: 2
Children: 1
Weekend_Nights: 2
Week_Nights: 3
Parking: 1
Lead_Time: 10
Year: 2026
Month: 8
Date: 24
Repeated_Guest: 0
Previous_Cancellations: 1
Previous_Bookings_Not_Canceled: 2
Price: 150.5
Special_Requests: 2
Meal_Plan: Meal Plan 1
Segment: Online
Room: Room_Type 1
"""


def test_parse_booking_body_extracts_configured_values():
    payload = parse_booking_body(VALID_BODY)

    assert payload["email"] == "guest@example.com"
    assert payload["full_name"] == "Mohamed Ahmed"
    assert payload["no_of_adults"] == 2
    assert payload["no_of_children"] == 1
    assert payload["arrival_year"] == 2026
    assert payload["arrival_month"] == 8
    assert payload["arrival_date"] == 24
    assert payload["avg_price_per_room"] == 150.5
    assert payload["type_of_meal_plan"] == "Meal Plan 1"
    assert payload["room_type_reserved"] == "Room_Type 1"
    assert payload["market_segment_type"] == "Online"


def test_parse_booking_body_uses_defaults_for_optional_fields():
    payload = parse_booking_body(
        """
        Email: guest@example.com
        Adults: 2
        Year: 2026
        Month: 8
        Date: 24
        Price: 100
        """
    )

    assert payload["no_of_children"] == 0
    assert payload["no_of_weekend_nights"] == 0
    assert payload["lead_time"] == 0
    assert payload["type_of_meal_plan"] == "Meal Plan 1"
    assert payload["room_type_reserved"] == "Room_Type 1"
    assert payload["market_segment_type"] == "Online"


def test_validate_booking_payload_returns_validated_data():
    payload = parse_booking_body(VALID_BODY)

    validated = validate_booking_payload(payload)

    assert validated["email"] == "guest@example.com"
    assert validated["no_of_adults"] == 2
    assert validated["arrival_year"] == 2026


def test_malformed_booking_body_raises_validation_error():
    payload = parse_booking_body(
        """
        Adults: 2
        Year: 2026
        Month: 8
        Date: 24
        Price: 100
        """
    )

    with pytest.raises(ValidationError):
        validate_booking_payload(payload)


def test_invalid_booking_value_raises_validation_error():
    payload = parse_booking_body(VALID_BODY)
    payload["arrival_month"] = 13

    with pytest.raises(ValidationError):
        validate_booking_payload(payload)
