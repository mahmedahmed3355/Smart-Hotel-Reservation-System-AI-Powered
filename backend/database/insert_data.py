from pathlib import Path

import pandas as pd
from config.settings import (
    DATA_CSV,
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
)
from sqlalchemy import create_engine

if not DB_PASSWORD:
    raise RuntimeError(
        "DB_PASSWORD is required. "
        "Set it in the environment before loading data."
    )

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

csv_path = Path(DATA_CSV)

if not csv_path.exists():
    raise FileNotFoundError(
        f"Reservation dataset not found: {csv_path}"
    )

df = pd.read_csv(csv_path)
df = df.where(pd.notnull(df), None)

df.to_sql(
    "hotel_reservations",
    engine,
    if_exists="append",
    index=False,
)

print(f"Inserted {len(df)} rows into hotel_reservations")
