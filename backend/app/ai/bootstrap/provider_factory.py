"""
Bootstrap factory for AI providers.
"""
import os
from app.ai.services.llm.providers import OpenAIProvider
from app.ai.services.embeddings.providers import OpenAIEmbeddingProvider
from app.ai.services.vector_store.providers import QdrantProvider

api_key = os.getenv("OPENAI_API_KEY", "dummy-key")

llm_provider = OpenAIProvider(api_key=api_key)
embedding_provider = OpenAIEmbeddingProvider(api_key=api_key)
vector_store_provider = QdrantProvider(host="localhost", port=6333)
