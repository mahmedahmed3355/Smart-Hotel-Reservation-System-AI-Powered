from sqlalchemy import create_engine

from config.settings import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
)

if not DB_PASSWORD:
    raise RuntimeError(
        "DB_PASSWORD is required. "
        "Set it in the environment before starting the application."
    )

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)
