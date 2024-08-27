import os
from dotenv import load_dotenv
from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators import AzureOpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder

load_dotenv()

prompt_template = """
Given these documents, answer the question.
Documents:
{% for doc in documents %}
    {{ doc.content }}
{% endfor %}
Question: {{question}}
Answer:
"""


weather_pipeline = Pipeline()
weather_pipeline.add_component("query_builder", )


def get_weather(location: str):
    result = weather_pipeline.run(
        {
            "retriever": {"query": query},
            "prompt_builder": {"question": query},
        }
    )
    return {"reply": result["llm"]["replies"][0]}
