import aiohttp
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class RESTHeartClient:
    """RESTHeart Cloud API Client"""
    
    def __init__(self, base_url: str, jwt_token: str):
        self.base_url = base_url.rstrip('/')
        self.jwt_token = jwt_token
        self.headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
    
    async def upload_document(
        self, 
        file_path: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Upload a document to knowledge base"""
        try:
            async with aiohttp.ClientSession() as session:
                with open(file_path, 'rb') as f:
                    form = aiohttp.FormData()
                    form.add_field('file', f, filename=file_path.split('/')[-1])
                    
                    if metadata:
                        form.add_field('properties', str(metadata))
                    
                    url = f"{self.base_url}/docs.files"
                    async with session.post(url, data=form, headers={
                        "Authorization": f"Bearer {self.jwt_token}"
                    }) as resp:
                        if resp.status in [200, 201]:
                            return await resp.json()
                        else:
                            error = await resp.text()
                            logger.error(f"Upload failed: {error}")
                            raise Exception(f"Upload failed: {resp.status}")
        except Exception as e:
            logger.error(f"Document upload error: {e}")
            raise
    
    async def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/docs.files"
                async with session.get(url, headers=self.headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get('_embedded', {}).get('rh:doc', [])
                    else:
                        logger.error(f"List failed: {resp.status}")
                        return []
        except Exception as e:
            logger.error(f"List documents error: {e}")
            return []
    
    async def delete_document(self, filename: str) -> bool:
        """Delete a document"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/docs.files/{filename}"
                async with session.delete(url, headers=self.headers) as resp:
                    return resp.status in [200, 204]
        except Exception as e:
            logger.error(f"Delete document error: {e}")
            return False
    
    async def get_text_segments(self, filename: str) -> List[Dict[str, Any]]:
        """Get text segments for a document"""
        try:
            async with aiohttp.ClientSession() as session:
                filter_query = f'{{"metadata.filename":"{filename}"}}'
                url = f"{self.base_url}/textSegments?filter={filter_query}"
                async with session.get(url, headers=self.headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get('_embedded', {}).get('rh:textSegment', [])
                    return []
        except Exception as e:
            logger.error(f"Get segments error: {e}")
            return []
    
    async def create_context(
        self, 
        context_id: str,
        template: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create or update a context"""
        try:
            default_options = {
                "max_tokens_to_sample": 4000,
                "temperature": 0.3,
                "agenticMode": True,
                "maxAgentIterations": 6
            }
            
            if options:
                default_options.update(options)
            
            payload = {
                "template": template,
                "options": default_options,
                "tags": ["telegram-bot"]
            }
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/contexts/{context_id}?wm=upsert"
                async with session.put(
                    url, 
                    json=payload, 
                    headers=self.headers
                ) as resp:
                    if resp.status in [200, 201]:
                        return await resp.json()
                    else:
                        error = await resp.text()
                        logger.error(f"Context creation failed: {error}")
                        raise Exception(f"Context creation failed: {resp.status}")
        except Exception as e:
            logger.error(f"Create context error: {e}")
            raise
    
    async def delete_context(self, context_id: str) -> bool:
        """Delete a context"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/contexts/{context_id}"
                async with session.delete(url, headers=self.headers) as resp:
                    return resp.status in [200, 204]
        except Exception as e:
            logger.error(f"Delete context error: {e}")
            return False