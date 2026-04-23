import json
import logging
import traceback
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    def __format_error(self, record: logging.LogRecord, log_record: Dict[str, Any]) -> Dict[str, Any]:
        if record.exc_info:
            etype, evalue, etb = record.exc_info
            log_record["exception_type"] = etype.__name__ if etype else None
            log_record["exception_message"] = str(evalue)
            log_record["traceback"] = "".join(traceback.format_exception(etype, evalue, etb))

        if record.stack_info:
            log_record["stack"] = record.stack_info
        return log_record

    def format(self, record: logging.LogRecord) -> str:
        try:
            update_dict = json.loads(record.getMessage())
        except json.JSONDecodeError:
            update_dict = {"message": record.getMessage()}

        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
        }
        log_record.update(update_dict)

        if record.levelname in ["WARNING", "ERROR", "CRITICAL", "FATAL"]:
            log_record = self.__format_error(record, log_record)

        return json.dumps(log_record)
