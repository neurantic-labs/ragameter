from ragameter.base.llm import LLM
from ragameter.base.metric import Metric
from ragameter.base.ranker import Ranker
from ragameter.base.retriever import Retriever
from ragameter.core.testdata import TestData


class TestDataEvaluator:
    def __init__(
        self,
        llm: LLM,
        retriever: Retriever,
        rankers: list[Ranker],
        testdata: TestData,
    ) -> None:
        self.testdata = testdata
        self.llm = llm
        self.retriever = retriever
        self.rankers = rankers

    def _init_keys(self, testdata: TestData, metrics: list[Metric]) -> dict[str, list[str] | list[float] | list[list[str]]]:
        data : dict[str , list[str] | list[float] | list[list[str]]] = {}
        #add all columns of test data
        for key in testdata.to_dict().keys():
            data[key] = []
        #add column for retriever results
        if self.retriever.name in data.keys():
            raise KeyError("Retriever name must be unique from other retrievers")
        data[self.retriever.name] = []
        #add columns for retrieval metric results
        for metric in metrics:
            metricname = f"{metric.name}-{self.retriever.name}"
            if metricname in data.keys():
                raise KeyError("Retriever Metric name must be unique from other metrics")
            data[metricname] = []
            
        #add columns for ranker results
        for ranker in self.rankers:
            if not ranker.name in data.keys():
                data[ranker.name] = []
                #add columns for ranker metric results
                for metric in metrics:
                    metricname = f"{metric.name}-{ranker.name}"
                    if metricname in data.keys():
                        raise KeyError("Metric name must be unique from other metrics")
                    data[metricname] = []
            else:
                raise KeyError("Ranker name must be unique from other rankers")
        return data

    def evaluate(self, testdata: TestData, metrics: list[Metric]) -> None:

        data = self._init_keys(testdata, metrics)

        for idx, query in enumerate(self.testdata.queries):
            query_type = self.testdata.query_types[idx]
            ground_truth = self.testdata.ground_truths[idx]
            ref_chunks = self.testdata.chunks[idx]
            
            retrieved_chunks = self.retriever.retrieve(query=query)
            
            #append retriever chunks
            data[self.retriever.name].append(retrieved_chunks)
            #append retriever metrics
            for metric in metrics:
                metricname = f"{metric.name}-{self.retriever.name}"
                result = metric.measure(
                    query=query,
                    query_type=query_type,
                    ground_truth=ground_truth,
                    chunks=ref_chunks,
                )
                data[metricname].append(result)
                
            #need to work on
            #append ranker chunks
            for ranker in self.rankers:
                if ranker.name in data.keys():
                    result = ranker.rank(query=query, retrieved_chunks=retrieved_chunks)
                    data[ranker.name].append(result)
                    #append ranker metrics
                    for metric in metrics:
                        metricname = f"{metric.name}-{ranker.name}"
                        result = metric.measure(
                            query=query,
                            query_type=query_type,
                            ground_truth=ground_truth,
                            chunks=ref_chunks,
                        )
                        data[metricname].append(result)
