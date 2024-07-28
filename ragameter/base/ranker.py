from abc import ABC, abstractmethod
from typing import Any


class Ranker(ABC):
    def __init__(self, name: str, **kwargs: Any) -> None:
        self.name = name

    @abstractmethod
    def rank(self, chunks: list[str], **kwargs: Any) -> list[str]:
        pass
