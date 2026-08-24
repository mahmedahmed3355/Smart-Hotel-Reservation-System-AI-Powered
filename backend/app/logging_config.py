import logging

from pythonjsonlogger.json import JsonFormatter


def configure_logging(
    *,
    logger: logging.Logger | None = None,
) -> logging.Logger:
    target_logger = logger or logging.getLogger()

    if target_logger.handlers:
        return target_logger

    handler = logging.StreamHandler()
    handler.setFormatter(
        JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )
    )

    target_logger.addHandler(handler)
    target_logger.setLevel(logging.INFO)

    return target_logger
