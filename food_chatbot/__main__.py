"""Module providing a chatbot assistant."""

import json
import os
import gradio as gr

from haystack.dataclasses import ChatMessage
from haystack.components.generators.chat import AzureOpenAIChatGenerator

from .tools import (
    tools,
    get_weather,
    find_recipe_by_ingredients,
    get_recipe_details,
)

def main():
    """_summary_

    Returns:
        _type_: _description_
    """

    messages = [
        ChatMessage.from_system(
            """You are a friendly personal assistant. 
            Don't make assumptions about what values to plug into functions.
            Ask for clarification if a user request is ambiguous."""
        )
    ]

    chat_generator = AzureOpenAIChatGenerator(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    available_functions = {
        "get_weather": get_weather,
        "find_recipe_by_ingredients": find_recipe_by_ingredients,
        "get_recipe_details": get_recipe_details,
    }

    def chatbot_with_fc(message):
        messages.append(ChatMessage.from_user(message))
        response = chat_generator.run(
            messages=messages, generation_kwargs={"tools": tools}
        )

        while True:
            if (
                response
                and response["replies"][0].meta["finish_reason"] == "tool_calls"
            ):
                function_calls = json.loads(response["replies"][0].content)
                print(response["replies"][0])
                for function_call in function_calls:
                    ## Parse function calling information
                    function_name = function_call["function"]["name"]
                    function_args = json.loads(function_call["function"]["arguments"])

                    print("Function Name:", function_name)
                    print("Function Arguments:", function_args)

                    ## Find the correspoding function and call it with the given arguments
                    function_to_call = available_functions[function_name]
                    function_response = function_to_call(**function_args)

                    print("Function Response:", function_response)

                    ## Append function response to the messages list
                    messages.append(
                        ChatMessage.from_function(
                            content=json.dumps(function_response), name=function_name
                        )
                    )
                    response = chat_generator.run(
                        messages=messages, generation_kwargs={"tools": tools}
                    )

                    print(response)

            # Regular Conversation
            else:
                messages.append(response["replies"][0])
                break
        return response["replies"][0].content

    demo = gr.ChatInterface(
        fn=chatbot_with_fc,
        examples=[
            "What can I cook with spinach, halloumi and tomatoes?",
            "What's the weather like in London?",
        ],
        title="Ask me about weather or where people live!",
    )

    demo.launch()


if __name__ == "__main__":
    main()
