"""
ReviewGuard AI — Document Upload Service
Orchestrates the secure ingestion, validation, and storage of documents.
"""
import os
import uuid
import hashlib
import aiofiles
import structlog
from datetime import datetime
from fastapi import UploadFile
from sqlalchemy.orm import Session

from config import settings
from dependencies import CurrentUser
from app.storage.service import StorageService
from app.storage.validators import validate_path_safety, validate_mime_type, validate_magic_bytes
from app.storage.exceptions import FileTooLargeError, StorageError
from models.db.document import Document
from models.enums import DocumentStatus

logger = structlog.get_logger(__name__)

class DocumentUploadService:
    def __init__(self, db: Session, storage_service: StorageService):
        self.db = db
        self.storage = storage_service

    def _generate_storage_key(self, ext: str) -> str:
        """Generates a sharded UUID key: YYYY/MM/DD/uuid.ext"""
        now = datetime.utcnow()
        shard = now.strftime("%Y/%m/%d")
        file_uuid = str(uuid.uuid4())
        return f"{shard}/{file_uuid}{ext}"

    async def upload_document(self, file: UploadFile, current_user: CurrentUser, organization_id: uuid.UUID = None) -> Document:
        """
        One-pass upload pipeline:
        1. Validate headers/safety.
        2. Stream to a temp file, simultaneously hashing and checking magic-bytes on first chunk.
        3. Enforce max size limit during stream.
        4. Move to permanent storage via StorageService.
        5. Persist DB record.
        """
        upload_id = uuid.uuid4()
        log = logger.bind(upload_id=str(upload_id), user_id=str(current_user.id), filename=file.filename)
        
        # 1. Header Validation
        validate_path_safety(file.filename)
        mime_type = validate_mime_type(file.content_type, file.filename)
        
        _, ext = os.path.splitext(file.filename)
        if not ext:
            ext = ".txt" if mime_type == "text/plain" else ""
            
        storage_key = self._generate_storage_key(ext)
        temp_path = os.path.join(settings.temp_directory, f"temp_{upload_id}{ext}")
        os.makedirs(settings.temp_directory, exist_ok=True)
        
        checksum_hash = hashlib.new(settings.checksum_algorithm)
        bytes_read = 0
        max_bytes = settings.upload_max_size_mb * 1024 * 1024
        
        log.info("upload_started", mime_type=mime_type)
        start_time = datetime.utcnow()
        
        try:
            # 2 & 3. One-Pass Stream, Hash, Validate, and Size Check
            async with aiofiles.open(temp_path, 'wb') as temp_file:
                is_first_chunk = True
                
                while True:
                    chunk = await file.read(8192)
                    if not chunk:
                        break
                        
                    if is_first_chunk:
                        validate_magic_bytes(chunk, mime_type)
                        is_first_chunk = False
                        
                    bytes_read += len(chunk)
                    if bytes_read > max_bytes:
                        raise FileTooLargeError(f"File exceeds maximum allowed size of {settings.upload_max_size_mb} MB.")
                        
                    checksum_hash.update(chunk)
                    await temp_file.write(chunk)
                    
            if bytes_read == 0:
                raise StorageError("Uploaded file is empty.", "EMPTY_FILE", 400)
                
            checksum_hex = checksum_hash.hexdigest()
            log.info("upload_streamed", size_bytes=bytes_read, checksum=checksum_hex)
            
            # 4. Move to Permanent Storage
            # Read from temp and save to actual storage provider
            with open(temp_path, "rb") as temp_reader:
                await self.storage.save(temp_reader, storage_key)
                
            # 5. Persist DB Record
            doc = Document(
                original_filename=file.filename,
                mime_type=mime_type,
                extension=ext,
                file_size_bytes=bytes_read,
                storage_provider=self.storage.provider_name,
                storage_key=storage_key,
                checksum=checksum_hex,
                owner_id=current_user.id,
                organization_id=organization_id,
                uploaded_by=current_user.id,
                status=DocumentStatus.STORED
            )
            self.db.add(doc)
            self.db.commit()
            self.db.refresh(doc)
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            log.info("upload_completed", document_id=str(doc.id), duration_sec=duration)
            
            return doc
            
        except Exception as e:
            log.error("upload_failed", error=str(e))
            self.db.rollback()
            raise e
            
        finally:
            # Always clean up the temp file
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception as e:
                    log.warning("temp_cleanup_failed", temp_path=temp_path, error=str(e))

