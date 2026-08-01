"""
Abstract provider interface and concrete implementations for vector stores.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .models import VectorRecord, VectorSearchRequest, VectorSearchResponse, SearchMatch
from .config import VectorStoreConfig
from .exceptions import CollectionNotFoundError, CollectionAlreadyExistsError, SearchError

class VectorStoreProvider(ABC):
    @abstractmethod
    def create_collection(self, config: VectorStoreConfig) -> None:
        pass
        
    @abstractmethod
    def collection_exists(self, collection_name: str) -> bool:
        pass
        
    @abstractmethod
    def delete_collection(self, collection_name: str) -> None:
        pass
        
    @abstractmethod
    def upsert(self, collection_name: str, record: VectorRecord) -> None:
        pass
        
    @abstractmethod
    def batch_upsert(self, collection_name: str, records: List[VectorRecord]) -> None:
        pass
        
    @abstractmethod
    def delete(self, collection_name: str, vector_id: str) -> None:
        pass
        
    @abstractmethod
    def search(self, collection_name: str, request: VectorSearchRequest) -> VectorSearchResponse:
        pass
        
    @abstractmethod
    def health_check(self) -> bool:
        pass

class QdrantProvider(VectorStoreProvider):
    """
    Qdrant implementation.
    For this architecture scaffolding, we use an in-memory dictionary.
    In production, this would import qdrant_client and interact with the database.
    """
    def __init__(self, host: str = "localhost", port: int = 6333):
        self.host = host
        self.port = port
        self._collections: Dict[str, Dict[str, VectorRecord]] = {}
        self._is_healthy = True
        
    def create_collection(self, config: VectorStoreConfig) -> None:
        if config.collection_name in self._collections:
            raise CollectionAlreadyExistsError(f"Collection {config.collection_name} already exists.")
        self._collections[config.collection_name] = {}
        
    def collection_exists(self, collection_name: str) -> bool:
        return collection_name in self._collections
        
    def delete_collection(self, collection_name: str) -> None:
        if collection_name not in self._collections:
            raise CollectionNotFoundError(f"Collection {collection_name} not found.")
        del self._collections[collection_name]
        
    def upsert(self, collection_name: str, record: VectorRecord) -> None:
        if collection_name not in self._collections:
            raise CollectionNotFoundError(f"Collection {collection_name} not found.")
        self._collections[collection_name][record.id] = record
        
    def batch_upsert(self, collection_name: str, records: List[VectorRecord]) -> None:
        for r in records:
            self.upsert(collection_name, r)
            
    def delete(self, collection_name: str, vector_id: str) -> None:
        if collection_name not in self._collections:
            raise CollectionNotFoundError(f"Collection {collection_name} not found.")
        self._collections[collection_name].pop(vector_id, None)
        
    def search(self, collection_name: str, request: VectorSearchRequest) -> VectorSearchResponse:
        if collection_name not in self._collections:
            raise CollectionNotFoundError(f"Collection {collection_name} not found.")
            
        matches = []
        collection = self._collections[collection_name]
        
        for vid, record in collection.items():
            # Dummy dot product logic for test (assuming vectors are normalized)
            score = sum(a * b for a, b in zip(request.vector, record.vector))
            
            # Filter logic
            include = True
            if request.filter:
                for k, v in request.filter.items():
                    if getattr(record.metadata, k, None) != v:
                        include = False
                        break
                        
            if include and (request.score_threshold is None or score >= request.score_threshold):
                matches.append(
                    SearchMatch(
                        id=record.id,
                        score=score,
                        metadata=record.metadata,
                        payload=record.payload
                    )
                )
                
        # Sort and take top_k
        matches.sort(key=lambda x: x.score, reverse=True)
        return VectorSearchResponse(matches=matches[:request.top_k])
        
    def health_check(self) -> bool:
        return self._is_healthy
