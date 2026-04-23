from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any
from utils.context import Context
from logs.json_logger_mixin import JsonLoggingMixin


T_in = TypeVar("T_in")
T_out = TypeVar("T_out")


class BasePipelineHandler(JsonLoggingMixin, ABC, Generic[T_in, T_out]):
    def __init__(self, context: Any):
        self.context = context

    @abstractmethod
    async def run_pipeline(self, data: T_in) -> T_out:
        raise NotImplementedError("subclasses must implement this method")
