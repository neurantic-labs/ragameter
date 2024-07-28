from abc import ABC, abstractmethod
from typing import Any


class Retriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, **kwargs: Any) -> list[str]:
        pass
