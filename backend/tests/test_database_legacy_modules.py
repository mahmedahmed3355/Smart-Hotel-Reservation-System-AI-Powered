import importlib
import sys
from unittest.mock import MagicMock

import pandas as pd
import pytest
import sqlalchemy

import config.settings as settings


def _import_fresh(module_name: str):
    previous_module = sys.modules.pop(module_name, None)

    try:
        module = importlib.import_module(module_name)
    except Exception:
        sys.modules.pop(module_name, None)

        if previous_module is not None:
            sys.modules[module_name] = previous_module

        raise

    sys.modules.pop(module_name, None)

    if previous_module is not None:
        sys.modules[module_name] = previous_module

    return module


def test_insert_data_requires_password(monkeypatch):
    monkeypatch.setattr(settings, "DB_PASSWORD", "")

    with pytest.raises(RuntimeError, match="DB_PASSWORD is required"):
        _import_fresh("database.insert_data")


def test_insert_data_requires_existing_csv(monkeypatch, tmp_path):
    create_engine = MagicMock()

    monkeypatch.setattr(sqlalchemy, "create_engine", create_engine)

    missing_csv = tmp_path / "missing.csv"

    monkeypatch.setattr(settings, "DB_USER", "hotel_user")
    monkeypatch.setattr(settings, "DB_PASSWORD", "secret")
    monkeypatch.setattr(settings, "DB_HOST", "db.example")
    monkeypatch.setattr(settings, "DB_PORT", "5433")
    monkeypatch.setattr(settings, "DB_NAME", "hotel_db")
    monkeypatch.setattr(settings, "DATA_CSV", str(missing_csv))

    with pytest.raises(
        FileNotFoundError,
        match="Reservation dataset not found",
    ):
        _import_fresh("database.insert_data")


def test_insert_data_loads_and_writes_dataframe(monkeypatch, tmp_path):
    csv_path = tmp_path / "reservations.csv"

    source_df = pd.DataFrame(
        {
            "booking_id": [1, 2],
            "guest_name": ["Alice", "Bob"],
            "lead_time": [10, None],
        }
    )
    source_df.to_csv(csv_path, index=False)

    engine = MagicMock()
    create_engine = MagicMock(return_value=engine)
    to_sql = MagicMock()

    monkeypatch.setattr(sqlalchemy, "create_engine", create_engine)
    monkeypatch.setattr(pd.DataFrame, "to_sql", to_sql)

    monkeypatch.setattr(settings, "DB_USER", "hotel_user")
    monkeypatch.setattr(settings, "DB_PASSWORD", "secret")
    monkeypatch.setattr(settings, "DB_HOST", "db.example")
    monkeypatch.setattr(settings, "DB_PORT", "5433")
    monkeypatch.setattr(settings, "DB_NAME", "hotel_db")
    monkeypatch.setattr(settings, "DATA_CSV", str(csv_path))

    module = _import_fresh("database.insert_data")

    expected_url = (
        "postgresql://hotel_user:secret"
        "@db.example:5433/hotel_db"
    )

    assert module.DATABASE_URL == expected_url
    create_engine.assert_called_once_with(expected_url)
    assert module.engine is engine

    assert module.csv_path == csv_path
    assert module.df.loc[0, "booking_id"] == 1
    assert module.df.loc[0, "guest_name"] == "Alice"
    assert pd.isna(module.df.loc[1, "lead_time"])

    to_sql.assert_called_once_with(
        "hotel_reservations",
        engine,
        if_exists="append",
        index=False,
    )
