# app/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, Text
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

class Booking(Base):
    __tablename__ = "hotel_reservations"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(String, index=True, nullable=True)
    email = Column(String, index=True)
    full_name = Column(String)
    no_of_adults = Column(Integer)
    no_of_children = Column(Integer)
    arrival_year = Column(Integer)
    arrival_month = Column(Integer)
    arrival_date = Column(Integer)
    avg_price_per_room = Column(Float)
    market_segment_type = Column(String)
    room_type_reserved = Column(String)
    customer_image_path = Column(Text)               # مسار الصورة (GCS/Public URL)
    ocr_raw_text = Column(Text)                      # النص المستخرج
    is_verified = Column(Boolean, default=False)     # نتيجة التحقق
    prediction_score = Column(Float, nullable=True)  # ناتج الموديل
    discounts = Column(JSONB, default={})            # JSONB للخصومات
