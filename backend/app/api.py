# app/api.py
import os, uuid, tempfile, shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Booking
from services.ocr import extract_from_id
from services.gcs import upload_to_gcs
from app.inference import predict_score
from app.discounts import compute_discounts

router = APIRouter(prefix="/bookings", tags=["bookings"])

GCS_BUCKET = os.getenv("GCS_BUCKET", "your-bucket")

@router.post("/")
async def create_booking(
    email: str = Form(...),
    full_name: str = Form(""),
    no_of_adults: int = Form(...),
    no_of_children: int = Form(0),
    arrival_year: int = Form(...),
    arrival_month: int = Form(...),
    arrival_date: int = Form(...),
    avg_price_per_room: float = Form(...),
    market_segment_type: str = Form("Online"),
    room_type_reserved: str = Form("Room_Type 1"),
    id_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1) خزّن الصورة مؤقتاً ثم ارفعها GCS
    tmpdir = tempfile.mkdtemp()
    local_path = os.path.join(tmpdir, id_image.filename)
    with open(local_path, "wb") as f:
        shutil.copyfileobj(id_image.file, f)

    # 2) OCR
    ocr = extract_from_id(local_path)
    # لو الـ OCR رجّع ايميل مختلف نقدر نعمل تحقق بسيط
    verified = (ocr.get("email") or email).lower() == email.lower()

    # 3) رفع الصورة GCS
    gcs_key = f"ids/{uuid.uuid4()}_{id_image.filename}"
    public_url = upload_to_gcs(local_path, GCS_BUCKET, gcs_key)

    # 4) تنبؤ
    payload = {
        "email": email, "full_name": full_name or ocr.get("full_name") or "",
        "no_of_adults": no_of_adults, "no_of_children": no_of_children,
        "arrival_year": arrival_year, "arrival_month": arrival_month, "arrival_date": arrival_date,
        "avg_price_per_room": avg_price_per_room,
        "market_segment_type": market_segment_type,
        "room_type_reserved": room_type_reserved
    }
    score = predict_score(payload)
    offers = compute_discounts(score)

    # 5) قبول/رفض بسيط
    accept = verified and (score >= 0.5)

    # 6) حفظ بالـ DB
    booking = Booking(
        email=email,
        full_name=payload["full_name"],
        no_of_adults=no_of_adults,
        no_of_children=no_of_children,
        arrival_year=arrival_year,
        arrival_month=arrival_month,
        arrival_date=arrival_date,
        avg_price_per_room=avg_price_per_room,
        market_segment_type=market_segment_type,
        room_type_reserved=room_type_reserved,
        customer_image_path=public_url,
        ocr_raw_text=ocr.get("raw_text",""),
        is_verified=verified,
        prediction_score=score,
        discounts=offers
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    shutil.rmtree(tmpdir, ignore_errors=True)

    return {"accepted": accept, "score": score, "offers": offers, "booking_id": booking.id, "image_url": public_url}
