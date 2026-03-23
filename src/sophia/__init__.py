"""Sophia AI Integration - RESTHeart Cloud's AI Assistant."""

from .sophia_client import SophiaClient
from .knowledge_manager import KnowledgeManager
from .models import SophiaContext, ChatMessage, SearchResult

__all__ = [
    "SophiaClient",
    "KnowledgeManager",
    "SophiaContext",
    "ChatMessage",
    "SearchResult",
]
