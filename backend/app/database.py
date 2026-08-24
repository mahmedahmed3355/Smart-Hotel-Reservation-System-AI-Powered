from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.settings import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
)


def build_database_url(require_password: bool = True) -> str:
    if require_password and not DB_PASSWORD:
        raise RuntimeError(
            'DB_PASSWORD is required to initialize the database.'
        )

    password = DB_PASSWORD or ''

    return (
        f'postgresql+psycopg2://{quote_plus(DB_USER or "")}:{quote_plus(password)}'
        f'@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )


DB_URL = build_database_url(require_password=False)

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


def get_db():
    if not DB_PASSWORD:
        raise RuntimeError(
            'DB_PASSWORD is required to access the database.'
        )

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
