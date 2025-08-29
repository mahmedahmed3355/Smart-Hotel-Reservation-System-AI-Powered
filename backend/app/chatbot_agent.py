# app/chatbot.py
from app.discounts import compute_discounts

def reply(message: str, last_score: float = 0.7, loyalty_points: int = 0) -> str:
    m = message.lower()
    if "offer" in m or "عروض" in m:
        offers = compute_discounts(last_score, loyalty_points)["offers"]
        if not offers: return "حالياً مفيش عروض كبيرة، نقدر نوفر خصم بسيط 5-10% حسب الإتاحة."
        text = "عندنا ليك: " + ", ".join([o["type"] for o in offers])
        return text
    if "price" in m or "السعر" in m:
        return "الأسعار بتبدأ من 100$ لليلة وبتقل مع العروض ونقاط الولاء."
    return "أقدر أساعدك بعروض، الأسعار، أو توفر الغرف. إسألني 🙂"
