import pytest
from sqlalchemy.dialects.postgresql import JSONB

from app import database
from app.models import Booking


def test_build_database_url_uses_configured_values(monkeypatch):
    monkeypatch.setattr(database, "DB_USER", "hotel_user")
    monkeypatch.setattr(database, "DB_PASSWORD", "secret")
    monkeypatch.setattr(database, "DB_HOST", "db.example")
    monkeypatch.setattr(database, "DB_PORT", "5433")
    monkeypatch.setattr(database, "DB_NAME", "hotel")

    assert database.build_database_url() == (
        "postgresql+psycopg2://hotel_user:secret@db.example:5433/hotel"
    )


def test_database_functions_reject_missing_password_before_session(monkeypatch):
    monkeypatch.setattr(database, "DB_PASSWORD", None)
    session_local = pytest.fail
    monkeypatch.setattr(database, "SessionLocal", session_local)

    with pytest.raises(RuntimeError, match="DB_PASSWORD is required"):
        database.build_database_url(require_password=True)

    with pytest.raises(RuntimeError, match="DB_PASSWORD is required"):
        next(database.get_db())


def test_booking_metadata_matches_persistence_contract():
    table = Booking.__table__

    assert table.name == "hotel_reservations"
    for name in [
        "booking_id",
        "email",
        "full_name",
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
        "type_of_meal_plan",
        "room_type_reserved",
        "market_segment_type",
    ]:
        assert table.c[name].nullable is False

    assert table.c.booking_id.unique is True
    assert table.c.is_verified.nullable is False
    assert table.c.is_verified.server_default is not None
    assert isinstance(table.c.discounts.type, JSONB)
