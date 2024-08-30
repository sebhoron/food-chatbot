# Food Chatbot


## Description

This project demonstrates a tooling capabilities for LLMs using the Haystack framework and Azure OpenAI. It showcases how to create a basic question-answering system.

## Features

- Weather checker and recipe finder
- Custom prompt template
- Integration with Azure OpenAI for text generation
- Visualizes the pipeline structure

## Prerequisites

- [Git](https://git-scm.com/downloads)
- [Python 3.10+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/)
- An Azure OpenAI account with API access
- A Spoonacular API key
- Visual Crossing Weather API key

## Installation

1. Clone this repository:
* `git clone https://github.com/sebhoron/food-chatbot.git`
* `cd food-chatbot`
2. Install the required packages:
`poetry shell`
`poetry install`
3. Create a `.env` file in the project root and add your Azure OpenAI credentials:
* `AZURE_OPENAI_KEY=your_api_key`
* `AZURE_OPENAI_INSTANCE_NAME=your_instance_name`
* `AZURE_OPENAI_ENDPOINT0=your_instance_endpoint`
* `AZURE_OPENAI_DEPLOYMENT_NAME=your_model_deployment_name`
* `VISUAL_CROSSING_WEATHER_API_KEY=your_weather_api_key`
* `SPOONACULAR_API_KEY=your_food_api_key`

## Usage

Run the main script:
`poetry run python -m food-chatbot`

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

This project uses the [Haystack](https://github.com/deepset-ai/haystack) framework by deepset.
