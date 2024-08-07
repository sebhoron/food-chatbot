import os
import json
from dotenv import load_dotenv
from haystack import Pipeline, Document
from haystack.utils import Secret
from haystack.dataclasses import ChatMessage
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators import AzureOpenAIGenerator
from haystack.components.generators.chat import AzureOpenAIChatGenerator
from haystack.components.generators.utils import print_streaming_chunk
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder

load_dotenv()

WEATHER_INFO = {
    "Berlin": {"weather": "mostly sunny", "temperature": 7, "unit": "celsius"},
    "Paris": {"weather": "mostly cloudy", "temperature": 8, "unit": "celsius"},
    "Rome": {"weather": "sunny", "temperature": 14, "unit": "celsius"},
    "Madrid": {"weather": "sunny", "temperature": 10, "unit": "celsius"},
    "London": {"weather": "cloudy", "temperature": 9, "unit": "celsius"},
}

document_store = InMemoryDocumentStore()
document_store.write_documents(
    [
        Document(content="My name is Jean and I live in Paris."),
        Document(content="My name is Mark and I live in Berlin."),
        Document(content="My name is Giorgio and I live in Rome."),
    ]
)

prompt_template = """
Given these documents, answer the question.
Documents:
{% for doc in documents %}
    {{ doc.content }}
{% endfor %}
Question: {{question}}
Answer:
"""

retriever = InMemoryBM25Retriever(document_store=document_store)

prompt_builder = PromptBuilder(template=prompt_template)

llm = AzureOpenAIGenerator(
    azure_endpoint="https://%s.openai.azure.com"
    % os.getenv("AZURE_OPENAI_INSTANCE_NAME"),
    api_key=Secret.from_token(os.getenv("AZURE_OPENAI_KEY")),
    azure_deployment=os.getenv("GENERATION_MODEL_NAME"),
)

rag_pipeline = Pipeline()
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")
rag_pipeline.draw(path="my_pipeline")


def rag_pipeline_func(query):
    result = rag_pipeline.run(
        {
            "retriever": {"query": query},
            "prompt_builder": {"question": query},
        }
    )
    return {"reply": result["llm"]["replies"][0]}


def get_current_weather(location: str):
    if location in WEATHER_INFO:
        return WEATHER_INFO[location]

    else:
        return {"weather": "sunny", "temperature": 21.8, "unit": "fahrenheit"}


tools = [
    {
        "type": "function",
        "function": {
            "name": "rag_pipeline_func",
            "description": "Get information about where people live",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to use in the search. Infer this from the user's message. It should be a question or a statement",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"],
            },
        },
    },
]

messages = [
    ChatMessage.from_system(
        "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."
    ),
    ChatMessage.from_user("What's the weather like in Rome?"),
]

chat_generator = AzureOpenAIChatGenerator(
    azure_endpoint="https://%s.openai.azure.com"
    % os.getenv("AZURE_OPENAI_INSTANCE_NAME"),
    api_key=Secret.from_token(os.getenv("AZURE_OPENAI_KEY")),
    azure_deployment=os.getenv("GENERATION_MODEL_NAME"),
    streaming_callback=print_streaming_chunk,
)
response = chat_generator.run(messages=messages, generation_kwargs={"tools": tools})

function_call = json.loads(response["replies"][0].content)[0]
function_name = function_call["function"]["name"]
function_args = json.loads(function_call["function"]["arguments"])
print("Function Name:", function_name)
print("Function Arguments:", function_args)

## Find the correspoding function and call it with the given arguments
available_functions = {
    "rag_pipeline_func": rag_pipeline_func,
    "get_current_weather": get_current_weather,
}
function_to_call = available_functions[function_name]
function_response = function_to_call(**function_args)
print("Function Response:", function_response)

function_message = ChatMessage.from_function(
    content=json.dumps(function_response), name=function_name
)
messages.append(function_message)

response = chat_generator.run(messages=messages, generation_kwargs={"tools": tools})

print(response)
