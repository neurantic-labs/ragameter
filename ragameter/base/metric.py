from abc import ABC, abstractmethod
from typing import Any


class Metric(ABC):
    @abstractmethod
    def measure(self, **kwargs: Any) -> int:
        pass
