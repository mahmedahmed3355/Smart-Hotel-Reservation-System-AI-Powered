# ocr.py
import re
from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    
    # استخراج عدد البالغين
    adults_match = re.search(r'Adults:\s*(\d+)', text)
    no_of_adults = int(adults_match.group(1)) if adults_match else 0
    
    # ممكن تضيف باقي البيانات بنفس الطريقة
    ocr_data = {"no_of_adults": no_of_adults}
    return ocr_data
