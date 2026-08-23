from __future__ import annotations

from typing import Annotated, Literal

from fastapi import Form
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, ValidationError

MealPlan = Literal[
    "Meal Plan 1",
    "Meal Plan 2",
    "Meal Plan 3",
    "Not Selected",
]

RoomType = Literal[
    "Room_Type 1",
    "Room_Type 2",
    "Room_Type 3",
    "Room_Type 4",
    "Room_Type 5",
    "Room_Type 6",
    "Room_Type 7",
]

MarketSegment = Literal[
    "Aviation",
    "Complementary",
    "Corporate",
    "Offline",
    "Online",
]


class BookingCreate(BaseModel):
    email: str
    full_name: str = ""

    no_of_adults: Annotated[int, Field(ge=0, le=20)]
    no_of_children: Annotated[int, Field(ge=0, le=20)]
    no_of_weekend_nights: Annotated[int, Field(ge=0, le=30)]
    no_of_week_nights: Annotated[int, Field(ge=0, le=60)]
    required_car_parking_space: Annotated[int, Field(ge=0, le=1)]
    lead_time: Annotated[int, Field(ge=0, le=1000)]
    arrival_year: Annotated[int, Field(ge=2000, le=2100)]
    arrival_month: Annotated[int, Field(ge=1, le=12)]
    arrival_date: Annotated[int, Field(ge=1, le=31)]
    repeated_guest: Annotated[int, Field(ge=0, le=1)]
    no_of_previous_cancellations: Annotated[int, Field(ge=0, le=1000)]
    no_of_previous_bookings_not_canceled: Annotated[int, Field(ge=0, le=1000)]
    avg_price_per_room: Annotated[float, Field(ge=0)]
    no_of_special_requests: Annotated[int, Field(ge=0, le=20)]

    type_of_meal_plan: MealPlan
    room_type_reserved: RoomType
    market_segment_type: MarketSegment

    @classmethod
    def as_form(
        cls,
        email: Annotated[str, Form(...)],
        no_of_adults: Annotated[int, Form(...)],
        lead_time: Annotated[int, Form(...)],
        arrival_year: Annotated[int, Form(...)],
        arrival_month: Annotated[int, Form(...)],
        arrival_date: Annotated[int, Form(...)],
        avg_price_per_room: Annotated[float, Form(...)],
        full_name: Annotated[str, Form()] = "",
        no_of_children: Annotated[int, Form()] = 0,
        no_of_weekend_nights: Annotated[int, Form()] = 0,
        no_of_week_nights: Annotated[int, Form()] = 0,
        required_car_parking_space: Annotated[int, Form()] = 0,
        repeated_guest: Annotated[int, Form()] = 0,
        no_of_previous_cancellations: Annotated[int, Form()] = 0,
        no_of_previous_bookings_not_canceled: Annotated[int, Form()] = 0,
        no_of_special_requests: Annotated[int, Form()] = 0,
        type_of_meal_plan: Annotated[MealPlan, Form()] = "Meal Plan 1",
        room_type_reserved: Annotated[RoomType, Form()] = "Room_Type 1",
        market_segment_type: Annotated[MarketSegment, Form()] = "Online",
    ) -> BookingCreate:
        try:
            return cls(
                email=email,
                full_name=full_name,
                no_of_adults=no_of_adults,
                no_of_children=no_of_children,
                no_of_weekend_nights=no_of_weekend_nights,
                no_of_week_nights=no_of_week_nights,
                required_car_parking_space=required_car_parking_space,
                lead_time=lead_time,
                arrival_year=arrival_year,
                arrival_month=arrival_month,
                arrival_date=arrival_date,
                repeated_guest=repeated_guest,
                no_of_previous_cancellations=no_of_previous_cancellations,
                no_of_previous_bookings_not_canceled=no_of_previous_bookings_not_canceled,
                avg_price_per_room=avg_price_per_room,
                no_of_special_requests=no_of_special_requests,
                type_of_meal_plan=type_of_meal_plan,
                room_type_reserved=room_type_reserved,
                market_segment_type=market_segment_type,
            )
        except ValidationError as exc:
            raise RequestValidationError(exc.errors()) from exc

    def model_features(self) -> dict:
        return self.model_dump(
            include={
                "no_of_adults",
                "no_of_children",
                "no_of_weekend_nights",
                "no_of_week_nights",
                "required_car_parking_space",
                "lead_time",
                "arrival_year",
                "arrival_month",
                "arrival_date",
                "repeated_guest",
                "no_of_previous_cancellations",
                "no_of_previous_bookings_not_canceled",
                "avg_price_per_room",
                "no_of_special_requests",
                "type_of_meal_plan",
                "room_type_reserved",
                "market_segment_type",
            }
        )
