"""
ReviewGuard AI — Uploads Router
Secure API for document ingestion, retrieval, and deletion.
"""
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Query, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from core.exceptions import ForbiddenError
from dependencies import get_db, get_current_user, CurrentUser
from config import Settings, get_settings
from app.storage.service import StorageService
from services.document_upload_service import DocumentUploadService
from models.db.document import Document
from schemas.upload import DocumentResponse, BaseAPIResponse
from app.storage.exceptions import StorageError

router = APIRouter()

def get_document_upload_service(db: Session = Depends(get_db)) -> DocumentUploadService:
    # Inject dependencies
    storage_service = StorageService()
    return DocumentUploadService(db, storage_service)

def get_document_parser_service(db: Session = Depends(get_db)):
    from app.ai.parsers.parser_service import DocumentParserService
    return DocumentParserService(db, StorageService())

@router.post("/{document_id}/parse", response_model=BaseAPIResponse)
async def parse_document(
    document_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service = Depends(get_document_parser_service)
):
    """
    Triggers parsing for an uploaded document.
    """
    from app.ai.parsers.exceptions import ParserError
    try:
        result = await service.parse_document(str(document_id), str(current_user.id))
        return BaseAPIResponse(success=True, data=result, message="Document parsed successfully.")
    except ParserError as e:
        raise HTTPException(status_code=e.http_status, detail=e.message)


@router.post("", response_model=BaseAPIResponse[DocumentResponse])
async def upload_document(
    file: UploadFile = File(...),
    organization_id: Optional[uuid.UUID] = None,
    current_user: CurrentUser = Depends(get_current_user),
    service: DocumentUploadService = Depends(get_document_upload_service)
):
    """
    Securely uploads a document.
    Validates magic bytes, MIME types, and size.
    """
    try:
        doc = await service.upload_document(file, current_user, organization_id)
        # Convert to Pydantic explicitly to avoid missing lazy-loaded fields or alias issues
        doc_resp = DocumentResponse.model_validate(doc)
        return BaseAPIResponse(success=True, data=doc_resp, message="Upload completed successfully.")
    except StorageError as e:
        # Re-raise as HTTPException so our global handlers can format it
        raise HTTPException(status_code=e.http_status, detail=e.message)


@router.get("", response_model=BaseAPIResponse[List[DocumentResponse]])
def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lists documents owned by the current user."""
    # In enterprise setups, Admins/Managers might see more, but for now we scope to owner
    docs = db.query(Document).filter(Document.owner_id == current_user.id).offset(skip).limit(limit).all()
    resp_data = [DocumentResponse.model_validate(d) for d in docs]
    return BaseAPIResponse(success=True, data=resp_data)


@router.get("/{document_id}", response_model=BaseAPIResponse[DocumentResponse])
def get_document(
    document_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves metadata for a specific document."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
        
    if doc.owner_id != current_user.id and current_user.role.value != "ADMIN":
        raise ForbiddenError("You do not have permission to access this document.")
        
    return BaseAPIResponse(success=True, data=DocumentResponse.model_validate(doc))


@router.delete("/{document_id}", response_model=BaseAPIResponse[None])
async def delete_document(
    document_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletes a document and its underlying storage file."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
        
    if doc.owner_id != current_user.id and current_user.role.value != "ADMIN":
        raise ForbiddenError("You do not have permission to delete this document.")
        
    storage = StorageService()
    try:
        await storage.delete(doc.storage_key)
    except StorageError:
        # If it's already missing from disk, we still want to clean up the DB record
        pass
        
    db.delete(doc)
    db.commit()
    
    return BaseAPIResponse(success=True, message="Document deleted successfully.")

@router.post("/{document_id}/chunk")
async def chunk_document(
    document_id: uuid.UUID,
    strategy: str = Query("SEMANTIC", description="Chunking strategy (SEMANTIC, RECURSIVE, SENTENCE)"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chunks a parsed document using the specified strategy.
    """
    from app.ai.chunking.chunk_service import ChunkService
    from models.enums import ChunkStrategy
    
    try:
        strat_enum = ChunkStrategy[strategy.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid chunking strategy.")
        
    chunk_service = ChunkService(db)
    
    try:
        import asyncio
        stats = await asyncio.to_thread(chunk_service.chunk_document, document_id, current_user.id, strat_enum)
        return stats.model_dump()
    except Exception as e:
        # We catch everything else inside the service, but if it throws ChunkingError:
        raise HTTPException(status_code=422, detail=str(e))

@router.post("/{document_id}/embed")
async def embed_document(
    document_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings)
):
    """
    Generates embeddings for document chunks and upserts them to Qdrant.
    Idempotent operation (skips already embedded chunks).
    """
    from app.ai.embeddings.service import EmbeddingService
    from app.vectorstore.qdrant_service import QdrantService
    
    vector_store = QdrantService(settings=settings)
    embedding_service = EmbeddingService(db=db, settings=settings, vector_store=vector_store)
    
    try:
        stats = await embedding_service.embed_document(
            document_id=str(document_id),
            user_id=current_user.id,
            organization_id=getattr(current_user, "organization_id", None)
        )
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
