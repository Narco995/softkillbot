"""Sophia AI Data Models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class ChatStatus(str, Enum):
    """Chat status enumeration."""
    WAITING = "waiting"
    STREAMING = "streaming"
    DONE = "done"
    ERROR = "error"


class EventType(str, Enum):
    """Event type enumeration."""
    TOOL_START = "tool_start"
    TOOL_RESULT = "tool_result"
    TEXT_START = "text_start"
    TEXT_CHUNK = "text_chunk"
    TEXT_DONE = "text_done"


@dataclass
class SophiaContext:
    """Sophia AI Context configuration."""
    context_id: str
    template: str
    tags: List[str] = field(default_factory=list)
    welcome: str = "Hello! How can I help you today?"
    temperature: float = 0.3
    max_tokens: int = 4000
    relevants_limit: int = 5
    history_limit: int = 3
    agentic_mode: bool = True
    max_agent_iterations: int = 5
    stream_thinking_events: bool = True


@dataclass
class ChatMessage:
    """Chat message."""
    chat_id: str
    user_id: str
    prompt: str
    status: ChatStatus = ChatStatus.WAITING
    answer: str = ""
    chunks: List[str] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    thinking_process: str = ""
    used_documents: List[str] = field(default_factory=list)


@dataclass
class SearchResult:
    """Semantic search result."""
    text: str
    filename: str
    relevance_score: float
    tags: List[str]
    metadata: Dict[str, Any]
    source_url: Optional[str] = None
    page_number: Optional[int] = None


@dataclass
class UploadedDocument:
    """Uploaded document metadata."""
    doc_id: str
    filename: str
    file_size: int
    file_type: str
    tags: List[str]
    status: str  # "processing", "ready", "error"
    segments_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None


@dataclass
class AgenticThinkingEvent:
    """Agentic mode thinking event."""
    event_type: EventType
    content: str
    iteration: int
    documents_searched: List[str] = field(default_factory=list)
    confidence: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)
