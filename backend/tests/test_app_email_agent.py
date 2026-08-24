import json
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from app.email_agent import calculate_discounts


def test_calculate_discounts_for_regular_customer():
    result = json.loads(calculate_discounts({}))

    assert result == {
        "extra_meal": 0,
        "extra_week": 0,
        "discount_percent": 0,
    }


def test_calculate_discounts_for_vip_customer():
    result = json.loads(
        calculate_discounts(
            {
                "vip": True,
                "loyal_customer": True,
            }
        )
    )

    assert result == {
        "extra_meal": 1,
        "extra_week": 0,
        "discount_percent": 50,
    }
