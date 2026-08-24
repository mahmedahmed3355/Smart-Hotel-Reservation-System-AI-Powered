import json
import logging

from app.logging_config import configure_logging


def test_configure_logging_emits_parseable_json():
    logger = logging.getLogger("smart_hotel.test")
    logger.handlers.clear()
    logger.propagate = False

    configure_logging(logger=logger)

    handler = logger.handlers[0]
    record = logger.makeRecord(
        logger.name,
        logging.INFO,
        __file__,
        1,
        "booking processed",
        (),
        None,
    )

    rendered = handler.format(record)
    payload = json.loads(rendered)

    assert payload["message"] == "booking processed"
    assert payload["levelname"] == "INFO"
    assert payload["name"] == "smart_hotel.test"


def test_configure_logging_is_idempotent():
    logger = logging.getLogger("smart_hotel.idempotent")
    logger.handlers.clear()
    logger.propagate = False

    configure_logging(logger=logger)
    configure_logging(logger=logger)

    assert len(logger.handlers) == 1
