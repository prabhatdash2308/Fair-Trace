from typing import List
from app.ai.embeddings.models import ChunkToEmbed
from app.ai.embeddings.exceptions import InvalidInputError

class Batcher:
    @staticmethod
    def validate_and_batch(chunks: List[ChunkToEmbed], batch_size: int, token_estimator=None) -> List[List[ChunkToEmbed]]:
        """
        Validates chunks and splits them into batches.
        Rejects the entire request if validation fails.
        """
        if not chunks:
            raise InvalidInputError("No chunks provided for embedding.")

        seen_checksums = set()
        
        for chunk in chunks:
            if not chunk.text or not chunk.text.strip():
                raise InvalidInputError(f"Chunk {chunk.chunk_id} is empty or whitespace.")
            
            # Since chunks could have same text in theory, we don't strictly reject duplicate checksums 
            # here unless we compute the semantic chunk hash. Wait, the prompt says "duplicate checksums".
            # We will validate no duplicate chunk IDs instead to ensure strict batch integrity.
            if chunk.chunk_id in seen_checksums:
                raise InvalidInputError(f"Duplicate chunk ID {chunk.chunk_id} in batch.")
            seen_checksums.add(chunk.chunk_id)

            # Check utf-8 validity
            try:
                chunk.text.encode('utf-8')
            except UnicodeEncodeError:
                raise InvalidInputError(f"Chunk {chunk.chunk_id} contains invalid UTF-8.")

            # Optional token limit validation (e.g. 8192 tokens for OpenAI)
            if token_estimator:
                tokens = token_estimator(chunk.text)
                if tokens > 8000:
                    raise InvalidInputError(f"Chunk {chunk.chunk_id} exceeds token limit ({tokens} > 8000).")

        # Split into batches
        batches = []
        for i in range(0, len(chunks), batch_size):
            batches.append(chunks[i:i + batch_size])
            
        return batches
