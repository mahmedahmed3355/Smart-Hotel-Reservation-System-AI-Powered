import os


def get_env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


DB_HOST = get_env("DB_HOST", "localhost")
DB_PORT = get_env("DB_PORT", "5432")
DB_NAME = get_env("DB_NAME", "hotel_booking_db")
DB_USER = get_env("DB_USER", "hotel_admin")
DB_PASSWORD = get_env("DB_PASSWORD")

GCS_BUCKET = get_env("GCS_BUCKET")
MODEL_PATH = get_env("MODEL_PATH", "models/smart_hotel_model.pkl")
DATA_CSV = get_env("DATA_CSV", "data/Hotel Reservations.csv")
