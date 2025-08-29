# app/discounts.py
def compute_discounts(score: float, loyalty_points: int = 0) -> dict:
    offers = []
    if score >= 0.85:
        offers.append({"type":"half_price", "value":0.5})
        offers.append({"type":"extra_week", "value":7})
        offers.append({"type":"free_meal", "value":1})
    elif score >= 0.7:
        offers.append({"type":"free_meal", "value":1})
        offers.append({"type":"extra_night", "value":1})
    elif score >= 0.5:
        offers.append({"type":"small_discount", "value":0.1})
    # مكافأة ولاء
    if loyalty_points >= 100:
        offers.append({"type":"loyalty_bonus", "value":0.15})
    return {"score": score, "offers": offers}
