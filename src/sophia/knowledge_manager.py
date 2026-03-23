"""Knowledge Base Manager - Document Upload & Management."""

import aiohttp
import io
from typing import Optional, List, BinaryIO
from pathlib import Path

from ..utils.logger import logger
from .models import UploadedDocument


class KnowledgeManager:
    """Manage documents in Sophia knowledge base."""

    BASE_URL = "https://sophia-api.restheart.com"

    def __init__(self, api_token: str, context_id: str):
        """Initialize knowledge manager.
        
        Args:
            api_token: Bearer token
            context_id: Sophia context ID
        """
        self.api_token = api_token
        self.context_id = context_id
        self.headers = {"Authorization": f"Bearer {api_token}"}

    async def upload_document(
        self,
        file_path: str,
        tags: Optional[List[str]] = None,
        filename: Optional[str] = None,
    ) -> UploadedDocument:
        """Upload document to knowledge base.
        
        Args:
            file_path: Path to file (PDF, Markdown, TXT, HTML)
            tags: Tags for document
            filename: Custom filename
            
        Returns:
            UploadedDocument metadata
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            filename = filename or file_path.name
            file_size = file_path.stat().st_size
            file_type = file_path.suffix.lower()
            tags = tags or [self.context_id]

            # Create form data
            data = aiohttp.FormData()
            with open(file_path, "rb") as f:
                data.add_field("file", f, filename=filename)

            # Add metadata
            import json
            metadata = {
                "filename": filename,
                "tags": tags,
                "context": self.context_id,
            }
            data.add_field("metadata", json.dumps(metadata))

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.BASE_URL}/docs.files?wm=upsert",
                    headers=self.headers,
                    data=data,
                ) as resp:
                    if resp.status not in [200, 201]:
                        raise Exception(f"Upload failed: {resp.status} {await resp.text()}")

                    result = await resp.json()
                    doc = UploadedDocument(
                        doc_id=result.get("_id", ""),
                        filename=filename,
                        file_size=file_size,
                        file_type=file_type,
                        tags=tags,
                        status="processing",
                    )

                    logger.info(f"Document uploaded: {filename} ({file_size} bytes)")
                    return doc
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            raise

    async def upload_from_bytes(
        self,
        file_bytes: bytes,
        filename: str,
        tags: Optional[List[str]] = None,
    ) -> UploadedDocument:
        """Upload document from bytes.
        
        Args:
            file_bytes: File content as bytes
            filename: Filename
            tags: Tags for document
            
        Returns:
            UploadedDocument metadata
        """
        try:
            tags = tags or [self.context_id]
            file_type = Path(filename).suffix.lower()

            data = aiohttp.FormData()
            data.add_field(
                "file",
                io.BytesIO(file_bytes),
                filename=filename,
            )

            import json
            metadata = {
                "filename": filename,
                "tags": tags,
                "context": self.context_id,
            }
            data.add_field("metadata", json.dumps(metadata))

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.BASE_URL}/docs.files?wm=upsert",
                    headers=self.headers,
                    data=data,
                ) as resp:
                    if resp.status not in [200, 201]:
                        raise Exception(f"Upload failed: {resp.status}")

                    result = await resp.json()
                    doc = UploadedDocument(
                        doc_id=result.get("_id", ""),
                        filename=filename,
                        file_size=len(file_bytes),
                        file_type=file_type,
                        tags=tags,
                        status="processing",
                    )

                    logger.info(f"Document uploaded: {filename}")
                    return doc
        except Exception as e:
            logger.error(f"Error uploading from bytes: {str(e)}")
            raise

    async def list_documents(self, tags: Optional[List[str]] = None) -> List[UploadedDocument]:
        """List uploaded documents.
        
        Args:
            tags: Filter by tags
            
        Returns:
            List of documents
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Query documents
                query = {"metadata.tags": {"$in": tags or [self.context_id]}}
                params = {"filter": query}

                async with session.get(
                    f"{self.BASE_URL}/docs.files",
                    headers=self.headers,
                    params=params,
                ) as resp:
                    if resp.status != 200:
                        return []

                    data = await resp.json()
                    docs = [
                        UploadedDocument(
                            doc_id=doc.get("_id", ""),
                            filename=doc.get("filename", ""),
                            file_size=doc.get("length", 0),
                            file_type=Path(doc.get("filename", "")).suffix,
                            tags=doc.get("metadata", {}).get("tags", []),
                            status="ready",
                            segments_count=doc.get("segments_count", 0),
                        )
                        for doc in data.get("_embedded", [])
                    ]

                    logger.info(f"Found {len(docs)} documents")
                    return docs
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            return []

    async def delete_document(self, doc_id: str) -> bool:
        """Delete a document from knowledge base.
        
        Args:
            doc_id: Document ID
            
        Returns:
            True if deleted successfully
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    f"{self.BASE_URL}/docs.files/{doc_id}",
                    headers=self.headers,
                ) as resp:
                    if resp.status in [200, 204]:
                        logger.info(f"Document deleted: {doc_id}")
                        return True
                    else:
                        logger.error(f"Delete failed: {resp.status}")
                        return False
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False
