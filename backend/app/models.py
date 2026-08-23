from sqlalchemy import Boolean, Column, Float, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base


class Booking(Base):
    __tablename__ = "hotel_reservations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(String, unique=True, index=True, nullable=False)

    email = Column(String, index=True, nullable=False)
    full_name = Column(String, nullable=False)

    no_of_adults = Column(Integer, nullable=False)
    no_of_children = Column(Integer, nullable=False)
    no_of_weekend_nights = Column(Integer, nullable=False)
    no_of_week_nights = Column(Integer, nullable=False)
    required_car_parking_space = Column(Integer, nullable=False)
    lead_time = Column(Integer, nullable=False)

    arrival_year = Column(Integer, nullable=False)
    arrival_month = Column(Integer, nullable=False)
    arrival_date = Column(Integer, nullable=False)

    repeated_guest = Column(Integer, nullable=False)
    no_of_previous_cancellations = Column(Integer, nullable=False)
    no_of_previous_bookings_not_canceled = Column(Integer, nullable=False)

    avg_price_per_room = Column(Float, nullable=False)
    no_of_special_requests = Column(Integer, nullable=False)

    type_of_meal_plan = Column(String, nullable=False)
    room_type_reserved = Column(String, nullable=False)
    market_segment_type = Column(String, nullable=False)

    customer_image_path = Column(Text)
    ocr_raw_text = Column(Text)

    is_verified = Column(
        Boolean,
        default=False,
        server_default=text('false'),
        nullable=False,
    )
    prediction_score = Column(Float)
    discounts = Column(
        JSONB,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )
