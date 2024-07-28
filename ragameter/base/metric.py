from abc import ABC, abstractmethod
from typing import Any


class Metric(ABC):
    
    def __init__(self, name: str, **kwargs: Any) -> None:
        self.name = name
        
    @abstractmethod
    def measure(self, **kwargs: Any) -> float:
        pass
