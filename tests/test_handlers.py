import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update, Message, Chat, User
from telegram.ext import ContextTypes
from src.handlers.documents import DocumentHandler
from src.handlers.chat import ChatHandler


@pytest.fixture
def mock_update():
    """Create mock Telegram update"""
    update = MagicMock(spec=Update)
    update.effective_user = MagicMock(spec=User)
    update.effective_user.id = "12345"
    update.effective_user.first_name = "Test"
    update.message = MagicMock(spec=Message)
    update.message.text = "test message"
    update.message.message_id = 1
    update.message.reply_text = AsyncMock()
    return update


@pytest.fixture
def mock_context():
    """Create mock context"""
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.user_data = {}
    context.bot = MagicMock()
    context.bot.get_file = AsyncMock()
    return context


@pytest.mark.asyncio
async def test_document_handler_init(mock_restheart_client):
    """Test document handler initialization"""
    handler = DocumentHandler()
    assert handler.restheart is not None


@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context):
    """Test /start command"""
    handler = DocumentHandler()
    result = await handler.upload_start(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_called_once()
    assert result == 0  # UPLOAD_DOCUMENT state


@pytest.mark.asyncio
async def test_chat_handler_init(mock_restheart_client):
    """Test chat handler initialization"""
    handler = ChatHandler()
    assert handler.restheart is not None


@pytest.mark.asyncio
async def test_list_documents_empty(mock_update, mock_context, mock_restheart_client):
    """Test listing empty documents"""
    mock_restheart_client.list_documents = AsyncMock(return_value=[])
    
    handler = DocumentHandler()
    handler.restheart = mock_restheart_client
    
    await handler.list_documents(mock_update, mock_context)
    mock_update.message.reply_text.assert_called()
