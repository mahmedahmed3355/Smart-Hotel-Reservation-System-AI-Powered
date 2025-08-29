# services/ocr.py
import re
import pytesseract
from PIL import Image

def extract_from_id(image_path: str) -> dict:
    text = pytesseract.image_to_string(Image.open(image_path), lang="eng")
    # أمثلة Regex بسيطة (عدلها حسب شكل الهوية)
    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    adults = re.search(r"Adults:\s*(\d+)", text)
    name   = re.search(r"Name:\s*([A-Za-z ]+)", text)
    return {
        "email": email.group(0) if email else None,
        "no_of_adults": int(adults.group(1)) if adults else None,
        "full_name": name.group(1).strip() if name else None,
        "raw_text": text
    }
