# 🧠 Sophia AI Integration - Complete Guide

## Overview

Softkillbot now integrates **Sophia AI** from RESTHeart Cloud, providing:

✅ **Claude-Powered AI** - Advanced LLM via AWS Bedrock  
✅ **RAG (Retrieval-Augmented Generation)** - Answers grounded in YOUR documents  
✅ **Vector Search** - Semantic search across knowledge base  
✅ **Agentic Mode** - AI reasons autonomously before answering  
✅ **Real-time Streaming** - WebSocket-based response streaming  
✅ **Document Management** - Upload PDFs, Markdown, HTML, TXT  

---

## Architecture

```
Telegram User
     ↓ sends /ask "question"
Telegram Bot (Softkillbot)
     ↓ POST /chats
Sophia AI API (RESTHeart Cloud)
     ↓ RAG + Claude reasoning
     ↓ searches knowledge base
     ↓ streams answer via WebSocket
Telegram Bot
     ↓ sends answer
Telegram User ✅
```

---

## Setup

### 1. Get Sophia API Token

```bash
# Contact support@restheart.com
# Request: Dedicated RESTHeart Cloud tier with Sophia AI plugin

# Once enabled, create a token:
POST https://sophia-api.restheart.com/tokens
Body: {
  "username": "telegram-bot",
  "context": "telegram-bot",
  "tags": ["telegram-bot"]
}

# ⚠️ Save token immediately - shown only once!
```

### 2. Set Environment Variables

```bash
# .env file
SOPHIA_API_TOKEN=your_token_here
SOPHIA_CONTEXT_ID=telegram-bot
```

### 3. Create Sophia Context

```python
from src.sophia import SophiaClient

client = SophiaClient(
    api_token="your_token",
    context_id="telegram-bot"
)

# Context is auto-created on first use
```

### 4. Upload Knowledge Documents

```python
from src.sophia import KnowledgeManager

km = KnowledgeManager(
    api_token="your_token",
    context_id="telegram-bot"
)

# Upload PDF
await km.upload_document(
    file_path="./faq.pdf",
    tags=["faq", "telegram-bot"]
)

# Upload Markdown
await km.upload_document(
    file_path="./docs.md",
    tags=["documentation", "telegram-bot"]
)
```

---

## Usage

### Command: /ask

Ask Sophia AI a question using RAG + Claude:

```
User: /ask What are the system requirements?

Bot: 🔍 Searching knowledge base...

Sophia AI:
- Searches uploaded documents
- Retrieves relevant information
- Uses Claude to compose answer
- Streams response in real-time

User receives: Detailed answer grounded in your documents
```

### Command: /search

Perform semantic search in knowledge base:

```
User: /search "API authentication"

Bot:
🔍 Search Results for: "API authentication"

1. docs.md
To authenticate, send a Bearer token in the Authorization header...
Relevance: 95%

2. faq.pdf
How do I get an API token?
Relevance: 87%
```

### Command: /docs

List uploaded documents:

```
User: /docs

Bot:
📚 Uploaded Documents:

📄 faq.pdf
  Size: 125000 bytes
  Segments: 234
  Status: ready

📄 docs.md
  Size: 45000 bytes
  Segments: 89
  Status: ready
```

### Upload Documents

Admins can send files to upload:

```
User: [sends file: product-catalog.pdf]

Bot: ✅ Document uploaded: product-catalog.pdf
Size: 250000 bytes
Status: processing
```

---

## Implementation

### Initialize in Bot

```python
from src.sophia import SophiaClient, KnowledgeManager
from src.bot.sophia_handlers import SophiaHandlers
from telegram.ext import Application

# Create handlers
sophia_handlers = SophiaHandlers(
    sophia_token="your_token",
    context_id="telegram-bot"
)

# Add to bot
app = Application.builder().token(TELEGRAM_TOKEN).build()

# Add Sophia handlers
for handler in sophia_handlers.get_handlers():
    app.add_handler(handler)

app.run_polling()
```

### Example: Full Integration

```python
import asyncio
from src.sophia import SophiaClient, KnowledgeManager

async def main():
    # Initialize
    sophia = SophiaClient(
        api_token="your_token",
        context_id="telegram-bot"
    )
    km = KnowledgeManager(
        api_token="your_token",
        context_id="telegram-bot"
    )
    
    # Upload knowledge
    await km.upload_document("./faq.pdf", tags=["faq"])
    
    # Ask question
    chat_msg = await sophia.send_prompt(
        chat_id="tg-12345",
        user_id="12345",
        prompt="What is the API rate limit?"
    )
    
    # Stream response
    async for event in sophia.stream_response("tg-12345"):
        print(event)
    
    # Get answer
    answer = sophia.get_answer("tg-12345")
    print(f"Answer: {answer}")
    
    # Semantic search
    results = await sophia.semantic_search("authentication")
    for result in results:
        print(f"{result.filename}: {result.relevance_score:.1%}")

asyncio.run(main())
```

---

## Agentic Mode

When enabled, Sophia AI autonomously:

1. **Searches** knowledge base (iteration 1)
2. **Reads** relevant documents
3. **Searches again** if needed (iteration 2+)
4. **Reasons** to compose comprehensive answer
5. **Streams** thinking events to client

### Enable Agentic Mode

```python
from src.sophia import SophiaClient

client = SophiaClient(api_token, context_id)

# Agentic mode enabled by default
# AI will automatically search multiple times
# and reason before answering complex questions
```

### Get Thinking Process

```python
# After response completes
thinking = client.get_thinking_process("tg-12345")
print(thinking)

# Output:
# 🔍 Searching: API authentication
# 📄 Found: 5 relevant documents
# 🔍 Searching: rate limiting
# 📄 Found: 3 relevant documents
```

---

## Supported Document Formats

✅ **PDF** - PDF documents  
✅ **Markdown** - .md files  
✅ **HTML** - Web pages  
✅ **Plain Text** - .txt files  

Documents are auto-processed into vector embeddings for semantic search.

---

## API Reference

### SophiaClient

```python
class SophiaClient:
    async def send_prompt(chat_id, user_id, prompt) -> ChatMessage
    async def stream_response(chat_id) -> AsyncIterator[Dict]
    async def semantic_search(query, tags=None, limit=5) -> List[SearchResult]
    async def get_chat_history(chat_id) -> Optional[ChatMessage]
    def get_answer(chat_id) -> str
    def get_thinking_process(chat_id) -> str
```

### KnowledgeManager

```python
class KnowledgeManager:
    async def upload_document(file_path, tags=None) -> UploadedDocument
    async def upload_from_bytes(file_bytes, filename, tags=None) -> UploadedDocument
    async def list_documents(tags=None) -> List[UploadedDocument]
    async def delete_document(doc_id) -> bool
```

---

## Error Handling

```python
try:
    chat_msg = await sophia.send_prompt(chat_id, user_id, prompt)
    async for event in sophia.stream_response(chat_id):
        pass
except Exception as e:
    print(f"Error: {e}")
    # Handle error gracefully
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid token | Re-issue token |
| 429 Too Many Requests | Rate limit | Add retry with backoff |
| 500 Server Error | Service issue | Fallback message |
| Connection timeout | Network issue | Retry with exponential backoff |

---

## Performance

- **Search latency**: <100ms
- **Answer streaming**: Real-time (first token in <2s)
- **Concurrent chats**: 1000+
- **Max document size**: 50MB
- **Max documents**: Unlimited

---

## Security

✅ **JWT Authentication** - Scoped API tokens  
✅ **HTTPS/WSS** - Encrypted communication  
✅ **Rate Limiting** - Protection against abuse  
✅ **Document Isolation** - Per-context data separation  

---

## Troubleshooting

### Documents not found in search

```python
# Check if documents are uploaded
docs = await km.list_documents()
print(f"Found {len(docs)} documents")

# Check document status
for doc in docs:
    print(f"{doc.filename}: {doc.status}")
    # Status should be "ready"
```

### No answer from Sophia

```python
# Check knowledge base has documents
if not docs:
    print("Upload documents first!")

# Check if prompt is clear
if len(prompt) < 5:
    print("Prompt too short")

# Check API token validity
try:
    await sophia.send_prompt(chat_id, user_id, "test")
except Exception as e:
    print(f"Token error: {e}")
```

### WebSocket connection fails

```python
# Check token is valid
# Check network connectivity
# Implement retry logic

for attempt in range(3):
    try:
        async for event in sophia.stream_response(chat_id):
            pass
        break
    except Exception as e:
        if attempt < 2:
            await asyncio.sleep(2 ** attempt)  # exponential backoff
        else:
            raise
```

---

## Next Steps

1. **Request Dedicated Tier**: Contact support@restheart.com
2. **Get API Token**: Create token via Sophia API
3. **Upload Documents**: Feed your knowledge base
4. **Test Commands**: Try /ask and /search
5. **Deploy Bot**: Run with Docker Compose
6. **Monitor Usage**: Track API calls and performance

---

## Support

- **RESTHeart Docs**: https://restheart.org
- **Sophia AI Docs**: https://restheart.org/docs/sophia
- **Support Email**: support@restheart.com
- **GitHub Issues**: https://github.com/Narco995/softkillbot/issues

---

**Your bot now has Claude-powered AI with RAG!** 🚀
