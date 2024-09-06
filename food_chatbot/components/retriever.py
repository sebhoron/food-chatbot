"""Module configuring retriever component"""

from haystack_integrations.document_stores.mongodb_atlas import (
    MongoDBAtlasDocumentStore,
)
from haystack_integrations.components.retrievers.mongodb_atlas.embedding_retriever import (
    MongoDBAtlasEmbeddingRetriever,
)

document_store = MongoDBAtlasDocumentStore(
    database_name="recipe_details",
    collection_name="food_chatbot",
    vector_search_index="embedding_index",
)

retriever = MongoDBAtlasEmbeddingRetriever(document_store=document_store)
