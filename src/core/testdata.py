import json
from pandas import DataFrame


class TestData:
    def __init__(self) -> None:
        self.queries: list[str] = []
        self.query_types: list[str] = []
        self.chunks: list[list[str]] = []
        self.ground_truths: list[str] = []

    def add(
        self, query: str, query_type: str, chunks: list[str], ground_truth: str
    ) -> None:
        self.queries.append(query)
        self.query_types.append(query_type)
        self.chunks.append(chunks)
        self.ground_truths.append(ground_truth)

    def to_dict(self) -> dict[str, list[str] | list[list[str]]]:
        return {
            "queries": self.queries,
            "query_types": self.query_types,
            "chunks": self.chunks,
            "ground_truths": self.ground_truths,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def from_dict(self, data: dict[str, list[str] | list[list[str]]]) -> None:
        self.queries = data["queries"]
        self.query_types = data["query_types"]
        self.chunks = data["chunks"]
        self.ground_truths = data["ground_truths"]

    def load_csv(self, path: str) -> None:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    data = line.split("\t")
                    self.queries.append(data[0])
                    self.query_types.append(data[1])
                    self.chunks.append(data[2].split(" "))
                    self.ground_truths.append(data[3])

    def load_json(self, path: str) -> None:
        with open(path) as f:
            data = json.load(f)
            self.from_dict(data)

    def save_json(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f)

    def to_pandas(self) -> DataFrame:
        df = DataFrame(
            {
                "query": self.queries,
                "query_type": self.query_types,
                "chunks": self.chunks,
                "ground_truth": self.ground_truths,
            }
        )
        return df
