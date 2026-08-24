import importlib
import sys
from unittest.mock import MagicMock

import pytest
import sqlalchemy

import config.settings as settings

MODULE_NAME = "database.db_config"


def _import_fresh():
    previous_module = sys.modules.pop(MODULE_NAME, None)

    try:
        module = importlib.import_module(MODULE_NAME)
    except Exception:
        sys.modules.pop(MODULE_NAME, None)

        if previous_module is not None:
            sys.modules[MODULE_NAME] = previous_module

        raise

    sys.modules.pop(MODULE_NAME, None)

    if previous_module is not None:
        sys.modules[MODULE_NAME] = previous_module

    return module


def test_db_config_requires_password(monkeypatch):
    monkeypatch.setattr(settings, "DB_PASSWORD", "")

    with pytest.raises(RuntimeError, match="DB_PASSWORD is required"):
        _import_fresh()


def test_db_config_builds_url_and_creates_engine(monkeypatch):
    monkeypatch.setattr(settings, "DB_HOST", "db.example.com")
    monkeypatch.setattr(settings, "DB_PORT", "5433")
    monkeypatch.setattr(settings, "DB_NAME", "hotel")
    monkeypatch.setattr(settings, "DB_USER", "hotel_user")
    monkeypatch.setattr(settings, "DB_PASSWORD", "secret")

    create_engine = MagicMock()

    monkeypatch.setattr(
        sqlalchemy,
        "create_engine",
        create_engine,
    )

    module = _import_fresh()

    expected_url = (
        "postgresql://hotel_user:secret"
        "@db.example.com:5433/hotel"
    )

    assert module.DATABASE_URL == expected_url
    create_engine.assert_called_once_with(expected_url)
    assert module.engine is create_engine.return_value
