import logging
import sys

from logs.json_formatter import JSONFormatter


def get_json_logger(level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = JSONFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
