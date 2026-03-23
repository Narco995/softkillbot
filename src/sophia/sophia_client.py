"""Sophia AI Client - REST API Integration."""

import json
import asyncio
import aiohttp
from typing import Optional, List, AsyncIterator, Dict, Any
from datetime import datetime
from urllib.parse import urlencode

from ..utils.logger import logger
from .models import ChatMessage, ChatStatus, SearchResult, SophiaContext, AgenticThinkingEvent, EventType


class SophiaClient:
    """Client for interacting with RESTHeart Sophia AI API."""

    BASE_URL = "https://sophia-api.restheart.com"
    WS_BASE = "wss://sophia-api.restheart.com"

    def __init__(self, api_token: str, context_id: str):
        """Initialize Sophia client.
        
        Args:
            api_token: Bearer token for authentication
            context_id: Sophia context ID
        """
        self.api_token = api_token
        self.context_id = context_id
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }
        self.chat_sessions: Dict[str, ChatMessage] = {}

    async def send_prompt(
        self,
        chat_id: str,
        user_id: str,
        prompt: str,
    ) -> ChatMessage:
        """Send a prompt to Sophia AI.
        
        Args:
            chat_id: Unique chat session ID
            user_id: User identifier
            prompt: User's question/prompt
            
        Returns:
            ChatMessage with initial status
        """
        try:
            async with aiohttp.ClientSession() as session:
                body = {
                    "chatId": chat_id,
                    "prompt": prompt,
                    "context": self.context_id,
                }

                async with session.post(
                    f"{self.BASE_URL}/chats?wm=upsert",
                    headers=self.headers,
                    json=body,
                ) as resp:
                    if resp.status != 200:
                        raise Exception(f"Sophia API error: {resp.status} {await resp.text()}")

                    data = await resp.json()
                    chat_msg = ChatMessage(
                        chat_id=chat_id,
                        user_id=user_id,
                        prompt=prompt,
                        status=ChatStatus(data.get("status", "waiting")),
                    )
                    self.chat_sessions[chat_id] = chat_msg

                    logger.info(f"Prompt sent to Sophia: {chat_id}")
                    return chat_msg
        except Exception as e:
            logger.error(f"Error sending prompt to Sophia: {str(e)}")
            raise

    async def stream_response(
        self,
        chat_id: str,
    ) -> AsyncIterator[Dict[str, Any]]:
        """Stream response from Sophia AI via WebSocket.
        
        Args:
            chat_id: Chat session ID
            
        Yields:
            Streaming events from Sophia
        """
        try:
            import websockets

            avars = json.dumps({"chatId": chat_id})
            ws_url = f"{self.WS_BASE}/chats/_streams/subscribe?avars={avars}"

            headers = {"Authorization": f"Bearer {self.api_token}"}

            async with websockets.connect(ws_url, extra_headers=headers) as websocket:
                logger.info(f"WebSocket connected for chat {chat_id}")

                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=300)
                        event = json.loads(message)

                        # Extract fields from update
                        if "updateDescription" in event:
                            fields = event["updateDescription"].get("updatedFields", {})

                            # Update chat status and chunks
                            if fields.get("status"):
                                status = fields["status"]
                                if chat_id in self.chat_sessions:
                                    self.chat_sessions[chat_id].status = ChatStatus(status)
                                    logger.debug(f"Chat status: {status}")

                            # Collect text chunks
                            for key, value in fields.items():
                                if key.startswith("chunks."):
                                    if chat_id in self.chat_sessions:
                                        self.chat_sessions[chat_id].chunks.append(value)
                                        self.chat_sessions[chat_id].answer += value

                            # Handle events for agentic mode
                            if "events" in fields:
                                events = fields["events"]
                                if chat_id in self.chat_sessions:
                                    self.chat_sessions[chat_id].events.extend(events)

                            yield {
                                "type": "update",
                                "fields": fields,
                            }

                            # Stop when done
                            if fields.get("status") == "done":
                                logger.info(f"Chat {chat_id} completed")
                                break

                    except asyncio.TimeoutError:
                        logger.warning(f"WebSocket timeout for chat {chat_id}")
                        break
                    except Exception as e:
                        logger.error(f"WebSocket error: {str(e)}")
                        break
        except Exception as e:
            logger.error(f"Error streaming response: {str(e)}")
            raise

    async def semantic_search(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        limit: int = 5,
    ) -> List[SearchResult]:
        """Perform semantic search on knowledge base.
        
        Args:
            query: Search query
            tags: Optional tags to filter by
            limit: Max results to return
            
        Returns:
            List of search results
        """
        try:
            async with aiohttp.ClientSession() as session:
                avars = json.dumps({"tags": tags or [self.context_id]})
                params = {
                    "prompt": query,
                    "avars": avars,
                    "limit": limit,
                }

                url = f"{self.BASE_URL}/textSegments/_aggrs/search?"
                url += "&".join(f"{k}={v}" for k, v in params.items())

                async with session.get(url, headers=self.headers) as resp:
                    if resp.status != 200:
                        raise Exception(f"Search error: {resp.status}")

                    data = await resp.json()
                    results = [
                        SearchResult(
                            text=item.get("text", ""),
                            filename=item.get("metadata", {}).get("filename", ""),
                            relevance_score=item.get("relevance_score", 0),
                            tags=item.get("metadata", {}).get("tags", []),
                            metadata=item.get("metadata", {}),
                        )
                        for item in data[:limit]
                    ]

                    logger.info(f"Semantic search found {len(results)} results")
                    return results
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return []

    async def get_chat_history(self, chat_id: str) -> Optional[ChatMessage]:
        """Get chat history and current state.
        
        Args:
            chat_id: Chat session ID
            
        Returns:
            ChatMessage with full history
        """
        return self.chat_sessions.get(chat_id)

    def get_answer(self, chat_id: str) -> str:
        """Get complete answer from chat.
        
        Args:
            chat_id: Chat session ID
            
        Returns:
            Complete answer text
        """
        if chat_id in self.chat_sessions:
            return self.chat_sessions[chat_id].answer
        return ""

    def get_thinking_process(self, chat_id: str) -> str:
        """Get AI's thinking process (agentic mode).
        
        Args:
            chat_id: Chat session ID
            
        Returns:
            Thinking process description
        """
        if chat_id in self.chat_sessions:
            events = self.chat_sessions[chat_id].events
            thinking = []

            for event in events:
                if event.get("type") == "tool_start":
                    thinking.append(f"🔍 Searching: {event.get('content', '')}")
                elif event.get("type") == "tool_result":
                    thinking.append(f"📄 Found: {event.get('content', '')}")

            return "\n".join(thinking)
        return ""
