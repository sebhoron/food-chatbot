"""Module configuring llm component"""

import os

from dotenv import load_dotenv
from haystack.components.generators import AzureOpenAIGenerator

load_dotenv()

llm = AzureOpenAIGenerator(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)
