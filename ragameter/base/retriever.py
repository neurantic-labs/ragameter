from abc import ABC, abstractmethod
from typing import Any


class Retriever(ABC):
    def __init__(self, name: str, **kwargs: Any) -> None:
        self.name = name

    @abstractmethod
    def retrieve(self, query: str, **kwargs: Any) -> list[str]:
        pass
