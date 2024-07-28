from src.base.model import QueryType
from src.core.testdata_generator import TestDataConfigs, TestDataGenerator
from src.llms.groq import GroqLLM, GroqLLMConfig


if __name__ == "__main__":
    # r1 = Retriever1()
    # r2 = Ranker1()
    # r3 = Ranker2()

    # testset = Testset()
    # testset.load_json("./test.json")
    # testset.load_csv("./test.csv")
    # testset.load_excel"./test.xlsx")

    # evaluator = Evaluator(
    #     retrievers = [r1],
    #     rankers = [r2, r3],
    #     metrics = [Metric1, Metric2],
    #     testset = testset
    # )
    # evaluator.evaluate()

    llm = GroqLLM(
        config=GroqLLMConfig(
            name="llama3-8b-8192",
            url="https://api.groq.com/openai/v1/chat/completions",
            apikey="",
        )
    )

    generator = TestDataGenerator(
        llm=llm,
        configs=TestDataConfigs(
            num_queries=5,
            query_types=[QueryType.SIMPLE, QueryType.SUMMARIZATION]
        ),
    )
    testdata = generator.generate(
        chunks=[
            """
                               Telemetry is the automatic recording and transmission of data from remote or inaccessible sources to an IT system in a different location for monitoring and analysis. Telemetry data may be relayed using radio, infrared, ultrasonic, GSM, satellite or cable, depending on the application (telemetry is not only used in software development, but also in meteorology, intelligence, medicine, and other fields).
                               In the software development world, telemetry can offer insights on which features end users use most, detection of bugs and issues, and offering better visibility into performance without the need to solicit feedback directly from users.
                               """,
            """In a general sense, telemetry works through sensors at the remote source which measures physical (such as precipitation, pressure or temperature) or electrical (such as current or voltage) data. This is converted to electrical voltages that are combined with timing data. They form a data stream that is transmitted over a wireless medium, wired or a combination of both.
                               At the remote receiver, the stream is disaggregated and the original data displayed or processed based on the user’s specifications.
                               """,
            """In the context of software development, the concept of telemetry is often confused with logging.
                               But logging is a tool used in the development process to diagnose errors and code flows, and it’s focused on the internal structure of a website, app, or another development project. Once a project is released, however, telemetry is what you’re looking for to enable automatic collection of data from real-world use. Telemetry is what makes it possible to collect all that raw data that becomes valuable, actionable analytics.
                               """,
        ]
    )
    with open("./output.json", "w") as fp:
        fp.write(testdata.to_json())
        fp.close()
