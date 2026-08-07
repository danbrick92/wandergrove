from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from utils.base_handler import BaseHandler


T_in = TypeVar("T_in")
T_out = TypeVar("T_out")


class BasePipelineHandler(ABC, BaseHandler, Generic[T_in, T_out]):
    @abstractmethod
    async def run_pipeline(self, data: T_in) -> T_out:
        raise NotImplementedError("subclasses must implement this method")
