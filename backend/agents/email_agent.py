import email
import imaplib
import logging
import os
import re
import smtplib
from email.message import EmailMessage
from typing import Any, cast, overload

import requests
from pydantic import ValidationError

from app.schemas import BookingCreate

logger = logging.getLogger(__name__)

IMAP_HOST = os.getenv("IMAP_HOST", "imap.gmail.com")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = os.getenv("IMAP_PASS")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
API_URL = os.getenv("API_URL", "http://api:8000/bookings/")


def parse_booking_body(body: str) -> dict[str, Any]:
    @overload
    def find(pattern: str) -> str | None: ...

    @overload
    def find(pattern: str, default: str) -> str: ...

    def find(
        pattern: str,
        default: str | None = None,
    ) -> str | None:
        match = re.search(pattern, body, re.IGNORECASE)
        return match.group(1).strip() if match else default

    return {
        "email": find(r"email:\s*(.+)"),
        "full_name": find(r"name:\s*(.+)", ""),
        "no_of_adults": int(find(r"adults:\s*(\d+)", "1")),
        "no_of_children": int(find(r"children:\s*(\d+)", "0")),
        "no_of_weekend_nights": int(find(r"weekend_nights:\s*(\d+)", "0")),
        "no_of_week_nights": int(find(r"week_nights:\s*(\d+)", "0")),
        "required_car_parking_space": int(find(r"parking:\s*(\d+)", "0")),
        "lead_time": int(find(r"lead_time:\s*(\d+)", "0")),
        "arrival_year": int(find(r"year:\s*(\d+)", "2025")),
        "arrival_month": int(find(r"month:\s*(\d+)", "1")),
        "arrival_date": int(find(r"date:\s*(\d+)", "1")),
        "repeated_guest": int(find(r"repeated_guest:\s*(\d+)", "0")),
        "no_of_previous_cancellations": int(find(r"previous_cancellations:\s*(\d+)", "0")),
        "no_of_previous_bookings_not_canceled": int(find(r"previous_bookings_not_canceled:\s*(\d+)", "0")),
        "avg_price_per_room": float(find(r"price:\s*([\d.]+)", "100")),
        "no_of_special_requests": int(find(r"special_requests:\s*(\d+)", "0")),
        "type_of_meal_plan": find(
            r"meal_plan:\s*(.+)",
            "Meal Plan 1",
        ),
        "market_segment_type": find(
            r"segment:\s*(.+)",
            "Online",
        ),
        "room_type_reserved": find(
            r"room:\s*(.+)",
            "Room_Type 1",
        ),
    }


def validate_booking_payload(
    payload: dict[str, Any],
) -> dict[str, Any]:
    booking = BookingCreate.model_validate(payload)
    return booking.model_dump()


def send_email(
    to_addr: str,
    subject: str,
    body: str,
) -> None:
    if IMAP_USER is None or IMAP_PASS is None:
        raise RuntimeError("IMAP_USER and IMAP_PASS must be configured")

    msg = EmailMessage()
    msg["From"] = IMAP_USER
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(IMAP_USER, IMAP_PASS)
        smtp.send_message(msg)


def process_inbox() -> None:
    imap = imaplib.IMAP4_SSL(IMAP_HOST)
    imap.login(
        cast(str, IMAP_USER),
        cast(str, IMAP_PASS),
    )
    imap.select("INBOX")

    _status, data = imap.search(
        None,
        '(UNSEEN SUBJECT "Hotel Booking")',
    )

    for num in data[0].split():
        _status, message_data = imap.fetch(num, "(RFC822)")

        if not message_data:
            logger.warning("Skipping email with no message data")
            continue

        raw_message = message_data[0]

        if not isinstance(raw_message, tuple) or len(raw_message) < 2 or not isinstance(raw_message[1], bytes):
            logger.warning("Skipping email with invalid message data")
            continue

        msg = email.message_from_bytes(raw_message[1])
        from_addr = email.utils.parseaddr(msg.get("From"))[1]

        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload_bytes = part.get_payload(decode=True)

                    if isinstance(
                        payload_bytes,
                        bytes,
                    ):
                        body += payload_bytes.decode(errors="ignore")
        else:
            payload_bytes = msg.get_payload(decode=True)

            if isinstance(payload_bytes, bytes):
                body = payload_bytes.decode(errors="ignore")

        try:
            payload = validate_booking_payload(parse_booking_body(body))
        except ValidationError:
            logger.warning(
                "Skipping invalid booking email from %s",
                from_addr,
                exc_info=True,
            )
            continue

        files: dict[str, Any] = {}

        try:
            response = requests.post(
                API_URL,
                data=payload,
                files=files,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()
        except requests.RequestException:
            logger.exception(
                "Booking API request failed for %s",
                from_addr,
            )
            continue

        if result.get("accepted"):
            send_email(
                from_addr,
                "Booking Confirmed",
                (f"تم تأكيد الحجز. سكورك: {result['score']:.2f}. عروضك: {result['offers']}"),
            )
        else:
            send_email(
                from_addr,
                "No Availability",
                "للأسف لا يوجد مكان مناسب حالياً، جرّب تواريخ أخرى.",
            )

    imap.close()
    imap.logout()


if __name__ == "__main__":
    process_inbox()
