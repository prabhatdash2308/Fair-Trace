import uuid
from typing import List, Dict, Any

class MockQdrantClient:
    def __init__(self, host=None, port=None, url=None, api_key=None, path=None):
        self.collections = {}
        
    def collection_exists(self, collection_name: str) -> bool:
        return collection_name in self.collections
        
    def create_collection(self, collection_name: str, vectors_config: Any):
        self.collections[collection_name] = []
        
    def upsert(self, collection_name: str, points: List[Any]):
        if collection_name not in self.collections:
            self.collections[collection_name] = []
        self.collections[collection_name].extend(points)
        
    def search(self, collection_name: str, query_vector: List[float], limit: int = 5, query_filter: Any = None):
        # Return dummy search results
        class MockScoredPoint:
            def __init__(self, id, payload, score):
                self.id = id
                self.payload = payload
                self.score = score
        
        return [
            MockScoredPoint(
                id=str(uuid.uuid4()),
                payload={
                    "text": "Jane met most of her goals but missed one deadline.",
                    "document_id": query_filter.must[0].match.value if query_filter else "doc-1",
                    "chunk_index": 0
                },
                score=0.95
            ),
            MockScoredPoint(
                id=str(uuid.uuid4()),
                payload={
                    "text": "Sam is a dinosaur and too old for this team.",
                    "document_id": query_filter.must[0].match.value if query_filter else "doc-1",
                    "chunk_index": 1
                },
                score=0.88
            )
        ]

    def delete(self, collection_name: str, points_selector: Any):
        pass
        
    def count(self, collection_name: str, count_filter: Any = None):
        class MockCountResult:
            def __init__(self, count):
                self.count = count
        return MockCountResult(count=len(self.collections.get(collection_name, [])))
