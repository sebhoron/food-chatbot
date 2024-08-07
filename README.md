# Haystack Example

This project demonstrates a simple Retrieval-Augmented Generation (RAG) pipeline using the Haystack framework and Azure OpenAI. It showcases how to create a basic question-answering system with a small in-memory document store.

## Features

- In-memory document store
- BM25 retriever
- Custom prompt template
- Integration with Azure OpenAI for text generation
- Visualizes the pipeline structure

## Prerequisites

- Python 3.7+
- An Azure OpenAI account with API access

## Installation

1. Clone this repository:
`git clone https://github.com/yourusername/haystack-rag-example.git
cd haystack-rag-example`
2. Install the required packages:
`pip install -r requirements.txt`
3. Create a `.env` file in the project root and add your Azure OpenAI credentials:
`AZURE_OPENAI_INSTANCE_NAME=your_instance_name
AZURE_OPENAI_KEY=your_api_key
GENERATION_MODEL_NAME=your_model_deployment_name`

## Usage

Run the main script:
`python main.py`

This will:
1. Set up an in-memory document store with sample data
2. Create a RAG pipeline using Haystack components
3. Run a sample question through the pipeline
4. Generate a visualization of the pipeline structure

## Pipeline Components

- `InMemoryDocumentStore`: Stores the document collection
- `InMemoryBM25Retriever`: Retrieves relevant documents based on the query
- `PromptBuilder`: Constructs the prompt for the language model
- `AzureOpenAIGenerator`: Generates answers using Azure OpenAI
- `Pipeline`: Orchestrates the flow of data between components

## Customization

- Modify the `prompt_template` to change how the prompt is constructed
- Add more documents to the `document_store` for a larger knowledge base
- Adjust the pipeline structure or add new components as needed

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

This project uses the [Haystack](https://github.com/deepset-ai/haystack) framework by deepset.