from qdrant_client.http import models as qmodels
from typing import Any, Optional
from app.ai.retrieval.models import RetrievalQuery

class QdrantFilterBuilder:
    """Builds nested Qdrant must filters dynamically based on user context."""
    
    @staticmethod
    def build(query: RetrievalQuery) -> Optional[qmodels.Filter]:
        must_conditions = []
        
        # Security Isolations
        if query.user_id:
            must_conditions.append(
                qmodels.FieldCondition(
                    key="user_id",
                    match=qmodels.MatchValue(value=query.user_id)
                )
            )
            
        if query.organization_id:
            must_conditions.append(
                qmodels.FieldCondition(
                    key="organization_id",
                    match=qmodels.MatchValue(value=query.organization_id)
                )
            )
            
        # Target Isolations
        if query.document_id:
            must_conditions.append(
                qmodels.FieldCondition(
                    key="document_id",
                    match=qmodels.MatchValue(value=query.document_id)
                )
            )
            
        if query.document_type:
            must_conditions.append(
                qmodels.FieldCondition(
                    key="document_type",
                    match=qmodels.MatchValue(value=query.document_type)
                )
            )
            
        if query.section:
            must_conditions.append(
                qmodels.FieldCondition(
                    key="section",
                    match=qmodels.MatchValue(value=query.section)
                )
            )
            
        if query.heading:
            must_conditions.append(
                qmodels.FieldCondition(
                    key="heading",
                    match=qmodels.MatchValue(value=query.heading)
                )
            )
            
        if not must_conditions:
            return None
            
        return qmodels.Filter(must=must_conditions)
