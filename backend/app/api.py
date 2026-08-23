# app/api.py
import os
import shutil
import tempfile
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from services.gcs import upload_to_gcs
from services.ocr import extract_from_id
from sqlalchemy.orm import Session

from app.database import get_db
from app.discounts import compute_discounts
from app.inference import predict_score
from app.models import Booking
from app.schemas import BookingCreate

router = APIRouter(prefix="/bookings", tags=["bookings"])

GCS_BUCKET = os.getenv("GCS_BUCKET", "your-bucket")

@router.post("/")
def create_booking(
    booking_request: Annotated[BookingCreate, Depends(BookingCreate.as_form)],
    id_image: Annotated[UploadFile, File(...)],
    db: Annotated[Session, Depends(get_db)],
):
    # 1) خزّن الصورة مؤقتاً ثم ارفعها GCS
    tmpdir = tempfile.mkdtemp()
    local_path = os.path.join(tmpdir, id_image.filename)
    with open(local_path, "wb") as f:
        shutil.copyfileobj(id_image.file, f)

    # 2) OCR
    ocr = extract_from_id(local_path)
    # لو الـ OCR رجّع ايميل مختلف نقدر نعمل تحقق بسيط
    verified = (
        ocr.get("email") or booking_request.email
    ).lower() == booking_request.email.lower()

    # 3) رفع الصورة GCS
    gcs_key = f"ids/{uuid.uuid4()}_{id_image.filename}"
    public_url = upload_to_gcs(local_path, GCS_BUCKET, gcs_key)

    # 4) تنبؤ
    model_features = booking_request.model_features()
    score = predict_score(model_features)
    offers = compute_discounts(score)

    # 5) قبول/رفض بسيط
    accept = verified and (score >= 0.5)

    # 6) حفظ بالـ DB
    booking_data = booking_request.model_dump()
    booking_data["full_name"] = (
        booking_request.full_name or ocr.get("full_name") or ""
    )
    booking = Booking(
        booking_id=f"BKG-{uuid.uuid4().hex}",
        **booking_data,
        customer_image_path=public_url,
        ocr_raw_text=ocr.get("raw_text", ""),
        is_verified=verified,
        prediction_score=score,
        discounts=offers,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    shutil.rmtree(tmpdir, ignore_errors=True)

    return {
        "accepted": accept,
        "score": score,
        "offers": offers,
        "database_id": booking.id,
        "booking_id": booking.booking_id,
        "image_url": public_url,
    }
