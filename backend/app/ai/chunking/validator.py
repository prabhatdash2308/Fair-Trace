from typing import List
from app.ai.chunking.chunk_models import ChunkModel
from app.ai.chunking.exceptions import ValidationFailedError, OversizedChunkError
from config import settings

class ChunkValidator:
    """Validates chunks against enterprise constraints before saving."""
    
    @staticmethod
    def validate(chunks: List[ChunkModel]) -> None:
        """
        Validates a list of chunks. Raises exceptions if invalid.
        """
        if not chunks:
            raise ValidationFailedError("No chunks were generated.")
            
        previous_end = 0
        for i, chunk in enumerate(chunks):
            # 1. Empty Check
            if not chunk.text or not chunk.text.strip():
                raise ValidationFailedError(f"Chunk {i} is empty or whitespace only.")
                
            # 2. Size Limits
            if chunk.token_estimate > settings.max_chunk_size:
                raise OversizedChunkError(f"Chunk {i} exceeds max token limit ({chunk.token_estimate} > {settings.max_chunk_size}).")
            
            # 3. UTF-8 Validity
            try:
                chunk.text.encode('utf-8').decode('utf-8')
            except UnicodeDecodeError:
                raise ValidationFailedError(f"Chunk {i} contains invalid UTF-8 characters.")
                
            # 4. Excessive punctuation heuristic (e.g. broken OCR or bad formatting)
            # If > 50% of the text is punctuation, it's likely garbage
            punct_count = sum(1 for char in chunk.text if not char.isalnum() and not char.isspace())
            if len(chunk.text) > 0 and (punct_count / len(chunk.text)) > 0.5:
                # We won't strictly reject, but we could. For now, we allow it but it might be flagged.
                pass
                
            # 5. Overlap sequence validation
            # Current chunk's start offset should be <= previous chunk's end offset
            if i > 0:
                if chunk.start_offset > previous_end:
                    raise ValidationFailedError(f"Gap detected between chunk {i-1} and {i} ({previous_end} -> {chunk.start_offset}).")
            previous_end = chunk.end_offset
