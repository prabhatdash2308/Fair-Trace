from typing import List, Optional
from app.ai.retrieval.models import RetrievedChunk

class DeterministicRanker:
    """Ranks chunks deterministically, prioritizing exact score, then structural positions."""
    
    @staticmethod
    def rank(chunks: List[RetrievedChunk], query_heading: Optional[str] = None, query_section: Optional[str] = None) -> List[RetrievedChunk]:
        """
        Sort order (highest priority first):
        1. similarity_score (Descending)
        2. heading match (Boolean flag, Descending) - True if matched
        3. section match (Boolean flag, Descending) - True if matched
        4. chunk_index (Ascending) - Maintains document reading flow for ties
        """
        def sort_key(chunk: RetrievedChunk):
            heading_match = 1 if query_heading and chunk.heading and query_heading.lower() in chunk.heading.lower() else 0
            section_match = 1 if query_section and chunk.section and query_section.lower() in chunk.section.lower() else 0
            
            # Since Python sorts tuples sequentially, we invert ascending logic for descending properties
            # chunk_index might not be in RetrievedChunk yet (wait, I need to add it to models.py!)
            # I will use vector_id as a fallback if chunk_index is missing since it is a stable string.
            
            # Let's add chunk_index explicitly to models.py!
            return (
                -chunk.similarity_score,
                -heading_match,
                -section_match,
                getattr(chunk, 'chunk_index', 999999), 
                chunk.vector_id
            )
            
        return sorted(chunks, key=sort_key)
