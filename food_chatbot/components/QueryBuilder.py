import os

from dotenv import load_dotenv
from haystack.core import component
from haystack.components.generators import AzureOpenAIGenerator

load_dotenv()

llm = AzureOpenAIGenerator(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)


@component
class QueryBuilder:
    """
    A component generating personal welcome message and making it upper case
    """

    @component.output_types(query=str)
    def run(self, prompt: str):
        return {
            "welcome_text": (
                "Hello {name}, welcome to Haystack!".format(name=prompt)
            ).upper(),
            "note": "welcome message is ready",
        }
