import json
import logging
from typing import Any, Dict, Optional


class JsonLoggingMixin:
    def __get_logger(self) -> logging.Logger:
        if not hasattr(self, "context"):
            raise AttributeError("LoggingMixin requires context attribute")
        if not isinstance(self.context.logger, logging.Logger):
            raise AttributeError("Logger is not a logger")
        return self.context.logger

    def whoami(self) -> str:
        return self.__class__.__name__

    def log(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        error: Optional[Exception] = None,
        level: int = logging.INFO,
    ) -> None:
        logger = self.__get_logger()
        payload: Dict[str, Any] = {"message": message}
        if details is not None:
            payload["details"] = details
        try:
            payload["component"] = self.whoami()
        except Exception:  # pylint: disable=broad-except
            payload["component"] = "unknown"
        logger.log(level, json.dumps(payload), exc_info=error)
