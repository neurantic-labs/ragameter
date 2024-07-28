from abc import ABC, abstractmethod
from typing import Any


class Ranker(ABC):
    @abstractmethod
    def rank(self, chunks: list[str], **kwargs: Any) -> list[str]:
        pass
