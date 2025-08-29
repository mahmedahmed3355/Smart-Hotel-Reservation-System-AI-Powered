DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "hotel_admin",
    "password": "P@$$w0rd",
    "dbname": "hotel_booking_db"
}

from sqlalchemy import create_engine

# إعدادات قاعدة البيانات (غير القيم دي حسب بيئتك)
DB_USER = "hotel_admin"
DB_PASSWORD = "P@$$w0rd"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "hotel_db"

# PostgreSQL connection URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy Engine
engine = create_engine(DATABASE_URL)
