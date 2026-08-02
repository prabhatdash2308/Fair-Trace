import time
import math
from typing import List, Dict, Any
import structlog
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models as qmodels

from app.vectorstore.base import BaseVectorStore
from app.vectorstore.models import VectorPoint
from app.vectorstore.exceptions import VectorCollectionError, VectorUpsertError, VectorValidationError
from config import Settings

logger = structlog.get_logger(__name__)

class QdrantService(BaseVectorStore):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = AsyncQdrantClient(url=settings.qdrant_url)
        self.collection_name = settings.QDRANT_COLLECTION
        self.dimension = settings.embedding_dimension
        self.distance_mapping = {
            "Cosine": qmodels.Distance.COSINE,
            "Euclid": qmodels.Distance.EUCLID,
            "Dot": qmodels.Distance.DOT,
        }
        self.distance = self.distance_mapping.get(settings.vector_distance, qmodels.Distance.COSINE)

    async def initialize_collection(self) -> None:
        """Idempotent initialization: check existence and validate schema."""
        try:
            collections_response = await self.client.get_collections()
            exists = any(c.name == self.collection_name for c in collections_response.collections)
            
            if exists:
                collection_info = await self.client.get_collection(self.collection_name)
                # Validate schema
                if collection_info.config.params.vectors.size != self.dimension:
                    raise VectorCollectionError(
                        f"Collection {self.collection_name} dimension mismatch. "
                        f"Expected {self.dimension}, got {collection_info.config.params.vectors.size}"
                    )
                if collection_info.config.params.vectors.distance != self.distance:
                    raise VectorCollectionError(
                        f"Collection {self.collection_name} distance mismatch. "
                        f"Expected {self.distance}, got {collection_info.config.params.vectors.distance}"
                    )
                logger.info("qdrant_collection_validated", collection=self.collection_name)
            else:
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qmodels.VectorParams(
                        size=self.dimension,
                        distance=self.distance
                    )
                )
                logger.info("qdrant_collection_created", collection=self.collection_name)
                
                # Create standard indexes (payload fields)
                await self._create_indexes()

        except Exception as e:
            if isinstance(e, VectorCollectionError):
                raise e
            logger.error("qdrant_initialization_error", error=str(e))
            raise VectorCollectionError(f"Failed to initialize Qdrant collection: {str(e)}")

    async def _create_indexes(self):
        """Create indexes on frequently filtered payload fields."""
        index_fields = ["document_id", "user_id", "organization_id", "chunk_id"]
        for field in index_fields:
            await self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name=field,
                field_schema=qmodels.PayloadSchemaType.KEYWORD
            )

    def _validate_vector(self, vector: List[float]):
        if not vector:
            raise VectorValidationError("Vector is empty.")
        if len(vector) != self.dimension:
            raise VectorValidationError(f"Vector dimension is {len(vector)}, expected {self.dimension}.")
        for v in vector:
            if math.isnan(v) or math.isinf(v):
                raise VectorValidationError("Vector contains NaN or Infinity.")

    async def upsert_batch(self, points: List[VectorPoint]) -> None:
        if not points:
            return

        # Vector validation
        for p in points:
            self._validate_vector(p.vector)

        qdrant_points = [
            qmodels.PointStruct(
                id=p.id,
                vector=p.vector,
                payload=p.payload
            ) for p in points
        ]

        try:
            await self.client.upsert(
                collection_name=self.collection_name,
                points=qdrant_points,
                wait=True
            )
        except Exception as e:
            logger.error("qdrant_upsert_error", error=str(e))
            raise VectorUpsertError(f"Failed to upsert to Qdrant: {str(e)}")

    async def health(self) -> Dict[str, Any]:
        start_time = time.time()
        try:
            # 1. Reachable ping
            await self.client.get_collections()
            
            # 2. Collection specific checks
            info = await self.client.get_collection(self.collection_name)
            
            duration_ms = int((time.time() - start_time) * 1000)
            return {
                "status": "healthy",
                "collection": self.collection_name,
                "dimension": info.config.params.vectors.size,
                "distance": info.config.params.vectors.distance.name,
                "vector_count": info.points_count,
                "duration_ms": duration_ms
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
