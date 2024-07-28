from abc import ABC, abstractmethod
from typing import Any


class LLM(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, prompt: str, **kwargs: Any) -> str:
        pass
