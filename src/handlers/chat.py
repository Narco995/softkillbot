import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.restheart.client import RESTHeartClient
from src.config import settings

logger = logging.getLogger(__name__)

class ChatHandler:
    """Handle chat and context operations"""
    
    def __init__(self):
        self.restheart = RESTHeartClient(
            settings.RESTHEART_BASE_URL,
            settings.RESTHEART_JWT_TOKEN
        )
    
    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Chat with knowledge base"""
        if not update.message.text:
            return
        
        user_message = update.message.text
        user_id = str(update.effective_user.id)
        
        try:
            await update.message.reply_text("⏳ Thinking...")
            
            # Build template with user message
            template = f"""Based on the provided documents, answer this question:
            
{user_message}

<documents-placeholder>"""
            
            # Create context for this conversation
            context_id = f"chat_{user_id}_{update.message.message_id}"
            
            result = await self.restheart.create_context(
                context_id=context_id,
                template=template,
                options={
                    "max_tokens_to_sample": 2000,
                    "temperature": 0.5,
                    "agenticMode": True
                }
            )
            
            # Extract response (simplified - actual response handling depends on API)
            response = result.get('response', 'No response generated.')
            
            await update.message.reply_text(f"🤖 {response}")
        
        except Exception as e:
            logger.error(f"Chat error: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Search knowledge base"""
        if not context.args:
            await update.message.reply_text("Usage: `/search <query>`")
            return
        
        query = ' '.join(context.args)
        
        try:
            await update.message.reply_text(f"🔍 Searching for: `{query}`...")
            
            # Get all documents and search their segments
            docs = await self.restheart.list_documents()
            
            results = []
            for doc in docs:
                segments = await self.restheart.get_text_segments(doc.get('_id'))
                for segment in segments:
                    text = segment.get('text', '')
                    if query.lower() in text.lower():
                        results.append({
                            'doc': doc.get('_id'),
                            'text': text[:200] + '...' if len(text) > 200 else text
                        })
            
            if not results:
                await update.message.reply_text("❌ No results found.")
                return
            
            message = f"🔍 Found {len(results)} results:\n\n"
            for i, result in enumerate(results[:5], 1):
                message += f"{i}. **{result['doc']}**\n_{result['text']}_\n\n"
            
            await update.message.reply_text(message)
        
        except Exception as e:
            logger.error(f"Search error: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")