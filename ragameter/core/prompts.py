from ragameter.base.model import QueryType


def generate_n_reference_qns(
    num_queries: int, selected_chunks: list[str], query_types: list[QueryType]
) -> str:
    prompt = f"""
            You are a query generator.
            Your task is to generate {num_queries} number of queries of types [{[q_type.value for q_type in query_types]} that can be answered using the given context chunks.
            
            # INPUT:
            1. number of queries
            2. context chunks
            3. supported query types
            
            # Context:
            =====
            {selected_chunks}
            =====
            
            # No. of Queries: {num_queries}
            # Supported Query Types : {query_types}
            
            * Only generate queries that belongs to types {query_types}
            * THE OUTPUT SHOULD BE SAME AS IN THE SPECIFIED JSON OUTPUT FORMAT.
            * OUTPUT MUST NOT CONTAIN ANY OTHER INFORMATION OTHER THAN WHATS SPECIFIED IN THE OUTPUT FORMAT.
            
            Output format : JSON
            ```
            {r'''
            {
                "queries" : [list of queries],
                "query_types" : [type of the generated query] ,
                "ground_truths" : [ground truths for each query],
              }
              '''
            }
            ```
            """
    return prompt
