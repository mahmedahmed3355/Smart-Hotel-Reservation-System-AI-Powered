# discounts.py
import json

def calculate_discounts(user_info: dict):
    """
    حسب قواعد العمل نحدد الخصومات
    """
    discounts = {
        "extra_meal": 1 if user_info.get("vip", False) else 0,
        "extra_week": 0,
        "discount_percent": 50 if user_info.get("loyal_customer", False) else 0
    }
    return json.dumps(discounts)
