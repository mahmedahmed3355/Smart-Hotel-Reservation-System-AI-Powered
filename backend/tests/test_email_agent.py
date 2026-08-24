import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

import agents.email_agent as email_agent_module

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

def test_send_email_uses_configured_smtp(monkeypatch):
    smtp = MagicMock()
    smtp.__enter__.return_value = smtp

    monkeypatch.setattr(
        email_agent_module.smtplib,
        "SMTP",
        MagicMock(return_value=smtp),
    )

    monkeypatch.setattr(
        email_agent_module,
        "IMAP_USER",
        "hotel@example.com",
    )
    monkeypatch.setattr(
        email_agent_module,
        "IMAP_PASS",
        "secret",
    )
    monkeypatch.setattr(
        email_agent_module,
        "SMTP_HOST",
        "smtp.example.com",
    )
    monkeypatch.setattr(
        email_agent_module,
        "SMTP_PORT",
        2525,
    )

    email_agent_module.send_email(
        "guest@example.com",
        "Booking Confirmed",
        "Your booking is confirmed.",
    )

    email_agent_module.smtplib.SMTP.assert_called_once_with(
        "smtp.example.com",
        2525,
    )
    smtp.starttls.assert_called_once()
    smtp.login.assert_called_once_with(
        "hotel@example.com",
        "secret",
    )
    smtp.send_message.assert_called_once()

    message = smtp.send_message.call_args.args[0]

    assert message["From"] == "hotel@example.com"
    assert message["To"] == "guest@example.com"
    assert message["Subject"] == "Booking Confirmed"
    assert message.get_content().strip() == "Your booking is confirmed."


def _build_email_message(
    from_addr: str,
    body: str,
    multipart: bool = False,
):
    from email.message import EmailMessage

    message = EmailMessage()
    message["From"] = from_addr

    if multipart:
        message.set_content("ignored alternative")
        message.add_alternative(body, subtype="plain")
    else:
        message.set_content(body)

    return message.as_bytes()


def _configure_imap(monkeypatch, message_bytes):
    imap = MagicMock()

    imap.search.return_value = (
        "OK",
        [b"1"],
    )
    imap.fetch.return_value = (
        "OK",
        [(b"1", message_bytes)],
    )

    monkeypatch.setattr(
        email_agent_module.imaplib,
        "IMAP4_SSL",
        MagicMock(return_value=imap),
    )

    return imap


def test_process_inbox_confirms_accepted_booking(monkeypatch):
    message_bytes = _build_email_message(
        "Guest <guest@example.com>",
        VALID_BODY,
    )

    imap = _configure_imap(
        monkeypatch,
        message_bytes,
    )

    response = MagicMock()
    response.json.return_value = {
        "accepted": True,
        "score": 0.95,
        "offers": ["Late checkout"],
    }

    post = MagicMock(return_value=response)

    monkeypatch.setattr(
        email_agent_module.requests,
        "post",
        post,
    )

    send_email = MagicMock()

    monkeypatch.setattr(
        email_agent_module,
        "send_email",
        send_email,
    )

    email_agent_module.process_inbox()

    imap.login.assert_called_once_with(
        email_agent_module.IMAP_USER,
        email_agent_module.IMAP_PASS,
    )
    imap.select.assert_called_once_with("INBOX")

    post.assert_called_once()

    call_kwargs = post.call_args.kwargs

    assert call_kwargs["data"]["email"] == "guest@example.com"
    assert call_kwargs["timeout"] == 30

    response.raise_for_status.assert_called_once()

    send_email.assert_called_once_with(
        "guest@example.com",
        "Booking Confirmed",
        "تم تأكيد الحجز. "
        "سكورك: 0.95. "
        "عروضك: ['Late checkout']",
    )

    imap.close.assert_called_once()
    imap.logout.assert_called_once()


def test_process_inbox_sends_no_availability_email(monkeypatch):
    message_bytes = _build_email_message(
        "Guest <guest@example.com>",
        VALID_BODY,
    )

    imap = _configure_imap(
        monkeypatch,
        message_bytes,
    )

    response = MagicMock()
    response.json.return_value = {
        "accepted": False,
    }

    monkeypatch.setattr(
        email_agent_module.requests,
        "post",
        MagicMock(return_value=response),
    )

    send_email = MagicMock()

    monkeypatch.setattr(
        email_agent_module,
        "send_email",
        send_email,
    )

    email_agent_module.process_inbox()

    send_email.assert_called_once_with(
        "guest@example.com",
        "No Availability",
        "للأسف لا يوجد مكان مناسب حالياً، "
        "جرّب تواريخ أخرى.",
    )

    imap.close.assert_called_once()
    imap.logout.assert_called_once()


def test_process_inbox_skips_invalid_booking(monkeypatch):
    invalid_body = """
    Adults: 2
    Year: 2026
    Month: 8
    Date: 24
    Price: 100
    """

    message_bytes = _build_email_message(
        "Guest <guest@example.com>",
        invalid_body,
    )

    imap = _configure_imap(
        monkeypatch,
        message_bytes,
    )

    post = MagicMock()
    send_email = MagicMock()

    monkeypatch.setattr(
        email_agent_module.requests,
        "post",
        post,
    )
    monkeypatch.setattr(
        email_agent_module,
        "send_email",
        send_email,
    )

    email_agent_module.process_inbox()

    post.assert_not_called()
    send_email.assert_not_called()

    imap.close.assert_called_once()
    imap.logout.assert_called_once()


def test_process_inbox_skips_failed_api_request(monkeypatch):
    message_bytes = _build_email_message(
        "Guest <guest@example.com>",
        VALID_BODY,
    )

    imap = _configure_imap(
        monkeypatch,
        message_bytes,
    )

    monkeypatch.setattr(
        email_agent_module.requests,
        "post",
        MagicMock(
            side_effect=email_agent_module.requests.RequestException(
                "API unavailable"
            )
        ),
    )

    send_email = MagicMock()

    monkeypatch.setattr(
        email_agent_module,
        "send_email",
        send_email,
    )

    email_agent_module.process_inbox()

    send_email.assert_not_called()

    imap.close.assert_called_once()
    imap.logout.assert_called_once()


def test_process_inbox_handles_multipart_message(monkeypatch):
    message_bytes = _build_email_message(
        "Guest <guest@example.com>",
        VALID_BODY,
        multipart=True,
    )

    imap = _configure_imap(
        monkeypatch,
        message_bytes,
    )

    response = MagicMock()
    response.json.return_value = {
        "accepted": False,
    }

    monkeypatch.setattr(
        email_agent_module.requests,
        "post",
        MagicMock(return_value=response),
    )

    send_email = MagicMock()

    monkeypatch.setattr(
        email_agent_module,
        "send_email",
        send_email,
    )

    email_agent_module.process_inbox()

    send_email.assert_called_once()

    imap.close.assert_called_once()
    imap.logout.assert_called_once()
