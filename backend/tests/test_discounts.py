import pytest

from app.discounts import compute_discounts


@pytest.mark.parametrize(
    ("score", "expected_offers"),
    [
        (0.49, []),
        (0.5, [{"type": "small_discount", "value": 0.1}]),
        (
            0.7,
            [
                {"type": "free_meal", "value": 1},
                {"type": "extra_night", "value": 1},
            ],
        ),
        (
            0.85,
            [
                {"type": "half_price", "value": 0.5},
                {"type": "extra_week", "value": 7},
                {"type": "free_meal", "value": 1},
            ],
        ),
    ],
)
def test_discount_score_thresholds_return_expected_contract(
    score, expected_offers
):
    result = compute_discounts(score)

    assert result == {"score": score, "offers": expected_offers}


@pytest.mark.parametrize(
    ("loyalty_points", "has_bonus"),
    [(99, False), (100, True), (250, True)],
)
def test_loyalty_bonus_is_applied_at_one_hundred_points(
    loyalty_points, has_bonus
):
    result = compute_discounts(0.49, loyalty_points=loyalty_points)
    bonus = {"type": "loyalty_bonus", "value": 0.15}

    assert result["score"] == 0.49
    assert (bonus in result["offers"]) is has_bonus
    assert all(set(offer) == {"type", "value"} for offer in result["offers"])
