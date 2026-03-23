import pytest
from unittest.mock import AsyncMock, patch
from src.restheart.client import RESTHeartClient

@pytest.mark.asyncio
async def test_restheart_client_init():
    client = RESTHeartClient("https://example.com", "test-token")
    assert client.base_url == "https://example.com"
    assert client.jwt_token == "test-token"
    assert "Bearer test-token" in client.headers.get("Authorization", "")

@pytest.mark.asyncio
async def test_list_documents_empty():
    client = RESTHeartClient("https://example.com", "test-token")
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value={'_embedded': {'rh:doc': []}})
        mock_get.return_value.__aenter__.return_value = mock_resp
        
        result = await client.list_documents()
        assert result == []

@pytest.mark.asyncio
async def test_delete_document():
    client = RESTHeartClient("https://example.com", "test-token")
    with patch('aiohttp.ClientSession.delete') as mock_delete:
        mock_resp = AsyncMock()
        mock_resp.status = 204
        mock_delete.return_value.__aenter__.return_value = mock_resp
        
        result = await client.delete_document("test.pdf")
        assert result is True