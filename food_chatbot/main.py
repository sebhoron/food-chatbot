import json
import os
import gradio as gr

from dotenv import load_dotenv
from haystack.dataclasses import ChatMessage
from haystack.components.generators.chat import AzureOpenAIChatGenerator

from tools import get_weather, rag_pipeline_func, tools

def main():
    load_dotenv()

    messages = [
        ChatMessage.from_system(
            "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."
        ),
        ChatMessage.from_user("What's the weather in Berlin?"),
    ]

    chat_generator = AzureOpenAIChatGenerator(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
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
        "get_weather": get_weather,
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

    def chatbot_with_fc(message, history):
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

                    ## Find the correspoding function and call it with the given arguments
                    function_to_call = available_functions[function_name]
                    function_response = function_to_call(**function_args)

                    ## Append function response to the messages list using `ChatMessage.from_function`
                    messages.append(
                        ChatMessage.from_function(
                            content=json.dumps(function_response), name=function_name
                        )
                    )
                    response = chat_generator.run(
                        messages=messages, generation_kwargs={"tools": tools}
                    )

            # Regular Conversation
            else:
                messages.append(response["replies"][0])
                break
        return response["replies"][0].content

    demo = gr.ChatInterface(
        fn=chatbot_with_fc,
        examples=[
            "Can you tell me where Giorgio lives?",
            "What's the weather like in Madrid?",
            "Who lives in London?",
            "What's the weather like where Mark lives?",
        ],
        title="Ask me about weather or where people live!",
    )

    demo.launch()


if __name__ == "__main__":
    main()
