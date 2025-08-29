# agents/email_agent.py
import os, re, email, imaplib, smtplib
from email.message import EmailMessage
import requests

IMAP_HOST = os.getenv("IMAP_HOST","imap.gmail.com")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = os.getenv("IMAP_PASS")
SMTP_HOST = os.getenv("SMTP_HOST","smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT","587"))
API_URL  = os.getenv("API_URL","http://api:8000/bookings/")
# ملاحظة: استخدم App Password مع Gmail

def parse_booking_body(body:str)->dict:
    # استخرج حقول بسيطة من ايميل العميل
    # عدّل Regex حسب قالب الميل
    def find(pat, default=None):
        m = re.search(pat, body, re.I)
        return m.group(1).strip() if m else default
    return {
        "email": find(r"email:\s*(.+)"),
        "full_name": find(r"name:\s*(.+)",""),
        "no_of_adults": int(find(r"adults:\s*(\d+)","1")),
        "no_of_children": int(find(r"children:\s*(\d+)","0")),
        "arrival_year": int(find(r"year:\s*(\d+)","2025")),
        "arrival_month": int(find(r"month:\s*(\d+)","1")),
        "arrival_date": int(find(r"date:\s*(\d+)","1")),
        "avg_price_per_room": float(find(r"price:\s*([\d.]+)","100")),
        "market_segment_type": find(r"segment:\s*(.+)","Online"),
        "room_type_reserved": find(r"room:\s*(.+)","Room_Type 1"),
    }

def send_email(to_addr, subject, body):
    msg = EmailMessage()
    msg["From"] = IMAP_USER
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(IMAP_USER, IMAP_PASS)
        s.send_message(msg)

def process_inbox():
    imap = imaplib.IMAP4_SSL(IMAP_HOST)
    imap.login(IMAP_USER, IMAP_PASS)
    imap.select("INBOX")
    status, data = imap.search(None, '(UNSEEN SUBJECT "Hotel Booking")')
    for num in data[0].split():
        status, d = imap.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(d[0][1])
        from_addr = email.utils.parseaddr(msg.get("From"))[1]
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type()=="text/plain":
                    body += part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        payload = parse_booking_body(body)

        # ممكن برضه نحمّل صورة مرفقة ونبعتها مع الطلب كـ multipart لو عايز تعمّق
        files = {}  # {"id_image": open("path/to/file","rb")} لو عندك مرفق

        r = requests.post(API_URL, data=payload, files=files, timeout=30)
        res = r.json()
        if res.get("accepted"):
            send_email(from_addr, "Booking Confirmed ✅",
                       f"تم تأكيد الحجز. سكورك: {res['score']:.2f}. عروضك: {res['offers']}")
        else:
            send_email(from_addr, "No Availability ❌",
                       "للأسف لا يوجد مكان مناسب حالياً، جرّب تواريخ أخرى.")
    imap.close()
    imap.logout()

if __name__=="__main__":
    process_inbox()
