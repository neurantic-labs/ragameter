import re
import json

from pandas import DataFrame
from pydantic import BaseModel

from ragameter.base.llm import LLM
from ragameter.base.model import QueryType
from ragameter.core.prompts import generate_n_reference_qns
from ragameter.core.testdata import TestData


class TestDataConfigs(BaseModel):
    chunk_window: int = 1
    query_types: list[QueryType] = [QueryType.SIMPLE]
    max_retries: int = 3
    num_queries: int = 2
    limit_per_minute: int = 60


class TestDataGenerator:
    def __init__(self, llm: LLM, configs: TestDataConfigs):
        self.llm = llm
        self.config: TestDataConfigs = configs
        self._data: TestData = TestData()

    def _add_data(
        self, query: str, query_type: str, chunks: list[str], ground_truth: str
    ) -> None:
        self._data.queries.append(query)
        self._data.ground_truths.append(ground_truth)
        self._data.chunks.append(chunks)
        self._data.query_types.append(query_type)

    def generate(self, chunks: list[str]) -> TestData:
        """Generates Testdatas

        Args:
            chunks (list[str]): list of chunks for generating queries
        Returns:
            TestData: data containing queries , ground_truths , chunks and query_types
        """

        # group the chunks based on the group size
        for i in range(0, len(chunks), self.config.chunk_window):
            selected_chunks = chunks[i : i + self.config.chunk_window]
            prompt = generate_n_reference_qns(
                num_queries=self.config.num_queries,
                selected_chunks=selected_chunks,
                query_types=self.config.query_types,
            )

            k = 0
            while k <= self.config.max_retries:
                print(k)
                if k >= self.config.max_retries:
                    print(f"Max retry exceeded chunk at index {i}")
                    self._add_data(
                        query="", query_type="", chunks=selected_chunks, ground_truth=""
                    )
                    break

                try:
                    llm_output = self.llm.generate(system_prompt="", prompt=prompt)
                    data = self.__extract_json(llm_output)
                    for query, type, gt in zip(
                        data["queries"], data["query_types"], data["ground_truths"]
                    ):
                        self._add_data(
                            query=query,
                            query_type=type,
                            chunks=selected_chunks,
                            ground_truth=gt,
                        )
                    break
                except Exception as e:
                    print(f"CHUNK {i} : ", e)
                    k += 1
                    print("retrying...")
                    continue
        return self._data

    def __extract_json(self, llm_output: str) -> dict[str, list[str]]:
        """regex pattern to parse json
        ```
          {
            "queries" : [],
            "query_types" : [],
            "ground_truths" : [],
          }
        ```
        """
        pattern = r"\{[^{}]*\}"

        match = re.search(pattern, llm_output, re.DOTALL)

        if match:
            json_string = json.loads(match.group())

            queries = json_string["queries"]
            ground_truths = json_string["ground_truths"]
            query_types = json_string["query_types"]

            minimum = min(len(queries), len(ground_truths), len(query_types))

            return {
                "queries": queries[:minimum],
                "ground_truths": ground_truths[:minimum],
                "query_types": query_types[:minimum],
            }
        else:
            raise ValueError("JSON structure not found in the provided string.")

    def to_pandas(self) -> DataFrame:
        data = {
            "queries": self._data.queries,
            "query_types": self._data.query_types,
            "ground_truths": self._data.ground_truths,
            "chunks": self._data.chunks,
        }
        df = DataFrame(data=data)
        return df

    def to_json(self) -> str:
        data = {
            "queries": self._data.queries,
            "query_types": self._data.query_types,
            "ground_truths": self._data.ground_truths,
            "chunks": self._data.chunks,
        }
        return json.dumps(data)
