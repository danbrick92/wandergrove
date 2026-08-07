from abc import ABC, abstractmethod
from utils.context import Context
from logs.json_logger_mixin import JsonLoggingMixin


class BaseHandler(JsonLoggingMixin, ABC):
    def __init__(self, context: Context) -> None:
        self.context = context
        self.config = context.config
        self.logger = context.logger

    @abstractmethod
    def run_handler(self):
        pass
