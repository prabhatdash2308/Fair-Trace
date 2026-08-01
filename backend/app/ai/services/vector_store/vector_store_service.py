"""
The orchestrator of the Enterprise Vector Store Service.
"""
import time
from typing import List, Dict, Any
from .config import VectorStoreConfig
from .models import VectorRecord, VectorSearchRequest, VectorSearchResponse
from .providers import VectorStoreProvider
from .telemetry import Telemetry
from .exceptions import VectorStoreError

class VectorStoreService:
    """
    Enterprise Vector Store Gateway.
    No agent should bypass this service to access Qdrant/Pinecone.
    """
    def __init__(
        self,
        provider: VectorStoreProvider,
        config: VectorStoreConfig,
        telemetry: Telemetry
    ):
        self.provider = provider
        self.config = config
        self.telemetry = telemetry
        
    def _get_coll(self) -> str:
        return self.config.collection_name
        
    def create_collection(self) -> None:
        self.provider.create_collection(self.config)
        
    def collection_exists(self) -> bool:
        return self.provider.collection_exists(self._get_coll())
        
    def delete_collection(self) -> None:
        self.provider.delete_collection(self._get_coll())
        
    def upsert(self, record: VectorRecord, correlation_id: str) -> None:
        start = time.perf_counter()
        try:
            self.provider.upsert(self._get_coll(), record)
        finally:
            ms = int((time.perf_counter() - start) * 1000)
            self.telemetry.record_upsert(correlation_id, ms, 1)
            
    def batch_upsert(self, records: List[VectorRecord], correlation_id: str) -> None:
        start = time.perf_counter()
        try:
            self.provider.batch_upsert(self._get_coll(), records)
        finally:
            ms = int((time.perf_counter() - start) * 1000)
            self.telemetry.record_upsert(correlation_id, ms, len(records))
            
    def delete(self, vector_id: str, correlation_id: str) -> None:
        start = time.perf_counter()
        try:
            self.provider.delete(self._get_coll(), vector_id)
        finally:
            ms = int((time.perf_counter() - start) * 1000)
            self.telemetry.record_delete(correlation_id, ms, 1)
            
    def search(self, request: VectorSearchRequest, correlation_id: str) -> VectorSearchResponse:
        start = time.perf_counter()
        try:
            res = self.provider.search(self._get_coll(), request)
            return res
        finally:
            ms = int((time.perf_counter() - start) * 1000)
            count = len(res.matches) if 'res' in locals() else 0
            self.telemetry.record_search(correlation_id, ms, count)
            
    def health_check(self) -> bool:
        start = time.perf_counter()
        try:
            is_healthy = self.provider.health_check()
            return is_healthy
        except Exception:
            is_healthy = False
            return False
        finally:
            ms = int((time.perf_counter() - start) * 1000)
            self.telemetry.record_health_check(ms, is_healthy)
