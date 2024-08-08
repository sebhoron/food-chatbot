import os
import json
from dotenv import load_dotenv
from haystack.utils import Secret
from haystack.dataclasses import ChatMessage
from haystack.components.generators.chat import AzureOpenAIChatGenerator
from haystack.components.generators.utils import print_streaming_chunk

from tools import get_current_weather, rag_pipeline_func, tools


def main():
    load_dotenv()

    messages = [
        ChatMessage.from_system(
            "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."
        ),
        ChatMessage.from_user("Where does Mark live?"),
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


if __name__ == "__main__":
    main()
