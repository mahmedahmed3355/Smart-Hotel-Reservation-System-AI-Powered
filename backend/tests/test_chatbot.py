import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from app.chatbot_agent import reply


def test_reply_returns_offer_types(monkeypatch):
    monkeypatch.setattr(
        "app.chatbot_agent.compute_discounts",
        lambda score, points: {
            "offers": [
                {"type": "10% discount"},
                {"type": "free breakfast"},
            ]
        },
    )

    result = reply(
        "What offers do you have?",
        last_score=0.9,
        loyalty_points=50,
    )

    assert result == "عندنا ليك: 10% discount, free breakfast"


def test_reply_returns_fallback_when_no_offers(monkeypatch):
    monkeypatch.setattr(
        "app.chatbot_agent.compute_discounts",
        lambda score, points: {"offers": []},
    )

    result = reply("عروض")

    assert "مفيش عروض كبيرة" in result


def test_reply_handles_price_questions():
    result = reply("What is the price?")

    assert "100$" in result


def test_reply_handles_arabic_price_questions():
    result = reply("عايز أعرف السعر")

    assert "100$" in result


def test_reply_returns_default_help_message():
    result = reply("hello")

    assert "أقدر أساعدك" in result
