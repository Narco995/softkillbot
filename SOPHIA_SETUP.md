# 🚀 Sophia AI - Complete Setup Instructions

## Quick Start

### 1. Request Sophia API Access

Email: **support@restheart.com**

Request:
```
Subject: Enable Sophia AI for Softkillbot

Hi,

I'd like to enable Sophia AI for my Softkillbot project.
Please provide a Dedicated tier RESTHeart Cloud account with Sophia plugin.

Thank you!
```

### 2. Get Your API Token

Once access is granted:

```bash
# Create API token
curl -X POST https://sophia-api.restheart.com/tokens \
  -H "Content-Type: application/json" \
  -d '{
    "username": "telegram-bot",
    "context": "telegram-bot",
    "tags": ["telegram-bot"]
  }'

# Response:
# {
#   "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
# }

# ⚠️ SAVE THIS TOKEN IMMEDIATELY!
```

### 3. Set Environment Variables

```bash
# .env
SOPHIA_API_TOKEN=your_token_from_step_2
SOPHIA_CONTEXT_ID=telegram-bot
SOPHIA_ENABLED=True
```

### 4. Add Dependencies

```bash
pip install websockets aiohttp
```

### 5. Initialize Sophia in Bot

```python
# src/bot/main.py

from src.sophia.sophia_handlers import SophiaHandlers
from telegram.ext import Application
import os

# Create Sophia handlers
sophia_handlers = SophiaHandlers(
    sophia_token=os.getenv('SOPHIA_API_TOKEN'),
    context_id=os.getenv('SOPHIA_CONTEXT_ID')
)

# Add to bot
app = Application.builder().token(TELEGRAM_TOKEN).build()

# Register Sophia handlers
for handler in sophia_handlers.get_handlers():
    app.add_handler(handler)

app.run_polling()
```

### 6. Upload Knowledge Documents

```python
import asyncio
from src.sophia import KnowledgeManager

async def upload_docs():
    km = KnowledgeManager(
        api_token=os.getenv('SOPHIA_API_TOKEN'),
        context_id=os.getenv('SOPHIA_CONTEXT_ID')
    )
    
    # Upload FAQ
    await km.upload_document(
        './docs/faq.pdf',
        tags=['faq', 'telegram-bot']
    )
    
    # Upload API docs
    await km.upload_document(
        './docs/api.md',
        tags=['api', 'documentation']
    )
    
    # Upload product catalog
    await km.upload_document(
        './docs/products.html',
        tags=['products', 'catalog']
    )

# Run once to upload
asyncio.run(upload_docs())
```

### 7. Test Commands

```
# In Telegram

/ask What are your business hours?
/ask How do I reset my password?
/search API authentication
/search pricing
/docs
```

---

## File Structure

New files added:

```
src/sophia/
├── __init__.py              # Package exports
├── models.py               # Data models
├── sophia_client.py        # REST API client
├── knowledge_manager.py    # Document management

src/bot/
├── sophia_handlers.py      # Telegram bot handlers

Documentation:
├── SOPHIA_INTEGRATION.md   # Full integration guide
├─┐ SOPHIA_SETUP.md         # This file
```

---

## Commands Reference

### /ask

Ask Sophia AI using RAG + Claude:

```
/ask <your question>

Example:
/ask What is your return policy?
```

### /search

Semantic search in knowledge base:

```
/search <query>

Example:
/search customer support
```

### /docs

List uploaded documents:

```
/docs
```

### Upload Documents

Send any file (PDF, Markdown, HTML, TXT):

```
[Send file in Telegram]

Bot responds:
✅ Document uploaded: filename.pdf
Size: 125000 bytes
Status: processing
```

---

## Features

✅ **Claude-Powered AI** - Advanced LLM reasoning  
✅ **RAG** - Answers grounded in YOUR documents  
✅ **Semantic Search** - Vector-based similarity  
✅ **Agentic Mode** - AI reasons autonomously  
✅ **Real-time Streaming** - WebSocket updates  
✅ **Document Upload** - PDF, MD, HTML, TXT support  
✅ **Multi-format** - Support for various document types  
✅ **Async/Await** - Non-blocking operations  

---

## Configuration

### Agentic Mode

Enable advanced reasoning:

```python
# In SophiaClient
agentic_mode: bool = True  # Enabled by default
max_agent_iterations: int = 5  # Search depth
stream_thinking_events: bool = True  # Show reasoning
```

### Temperature

Control creativity (0.0 = deterministic, 1.0 = creative):

```python
temperature: float = 0.3  # More factual
```

### Max Tokens

Limit response length:

```python
max_tokens: int = 4000  # Max response length
```

---

## Error Handling

### Token Expired

```
401 Unauthorized

Solution: Re-issue token from Sophia API
```

### Rate Limited

```
429 Too Many Requests

Solution: Add retry with exponential backoff
```

### No Results

```
No answer found

Solution: Upload more documents or refine query
```

---

## Troubleshooting

### Documents not searchable

```python
# Check documents are uploaded
docs = await km.list_documents()
print(f"Found {len(docs)} documents")

# Check status is "ready"
for doc in docs:
    print(f"{doc.filename}: {doc.status}")
```

### WebSocket connection fails

```python
# Check token is valid
# Check network connectivity
# Implement retry logic
```

### Slow responses

```python
# Reduce max_agent_iterations
# Reduce document count
# Optimize queries
```

---

## Performance Tips

1. **Use semantic search** instead of full prompts for simple lookups
2. **Tag documents** properly for better filtering
3. **Keep documents focused** on specific topics
4. **Use agentic mode** for complex questions
5. **Cache frequently asked questions** locally

---

## Next Steps

1. ✅ Request access from RESTHeart
2. ✅ Get API token
3. ✅ Set environment variables
4. ✅ Upload documents
5. ✅ Test commands
6. ✅ Deploy bot
7. ✅ Monitor usage

---

## Support

- **RESTHeart**: https://restheart.org
- **Sophia Docs**: https://restheart.org/docs/sophia
- **Email**: support@restheart.com
- **GitHub**: https://github.com/Narco995/softkillbot

---

**Your bot is now powered by Claude AI with RAG!** 🤖🚀
