from abc import ABC, abstractmethod
from typing import Any


class ADataPipeline(ABC):
    
    def extract(self, **kwargs) -> Any:
        return {}
    
    def transform(self, **kwargs) -> Any:
        return {}
    
    def load(self, **kwargs) -> Any:
        return {}
