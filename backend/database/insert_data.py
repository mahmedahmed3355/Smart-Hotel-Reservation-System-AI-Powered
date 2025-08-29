import pandas as pd
from sqlalchemy import create_engine

# 1. إعداد الاتصال بقاعدة البيانات
# عدّل القيم حسب إعداداتك (user, password, host, dbname)
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "hotel_booking_db"
DB_USER = "hotel_admin"
DB_PASSWORD = "P@$$w0rd"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 2. إنشاء engine
engine = create_engine(DATABASE_URL)

# 3. قراءة CSV باستخدام pandas
csv_file = "/home/mohamed/Desktop/Smart Hotl reservation System/hotel_booking_pipeline/data/Hotel Reservations.csv"  # غيّر المسار حسب مكان الملف
df = pd.read_csv(csv_file)

# ✅ معالجة بسيطة لو في NaN
df = df.where(pd.notnull(df), None)

# 4. إدخال البيانات في جدول hotel_bookings
df.to_sql(
    "Hotel Reservations", 
    engine, 
    if_exists="append",   # append علشان نضيف من غير ما نمسح الجدول
    index=False
)

print("✅ Data inserted successfully into hotel_bookings table!")
