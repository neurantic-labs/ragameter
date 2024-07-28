from pydantic import BaseModel
import requests

from src.base.llm import LLM


class GroqLLMConfig(BaseModel):
    name: str
    url: str
    apikey: str


class GroqLLM(LLM):
    def __init__(self, config: GroqLLMConfig) -> None:
        self.config = config

    def generate(self, system_prompt: str = "", prompt: str = "", **kwargs) -> str:
        messages = []

        if system_prompt and system_prompt.strip() != "":
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})
        response = requests.post(
            self.config.url,
            headers={"Authorization": f"Bearer {self.config.apikey}"},
            json={
                "model": self.config.name,
                "temperature": 0.4,
                "stream": False,
                "messages": messages,
            },
        )
        return response.json()["choices"][0]["message"]["content"]
