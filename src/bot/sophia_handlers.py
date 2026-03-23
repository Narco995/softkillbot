"""Telegram Bot Handlers for Sophia AI Integration."""

import asyncio
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from ..sophia import SophiaClient, KnowledgeManager
from ..utils.logger import logger


class SophiaHandlers:
    """Handlers for Sophia AI integration with Telegram bot."""

    def __init__(self, sophia_token: str, context_id: str):
        """Initialize Sophia handlers.
        
        Args:
            sophia_token: Sophia API token
            context_id: Sophia context ID
        """
        self.sophia_client = SophiaClient(sophia_token, context_id)
        self.knowledge_manager = KnowledgeManager(sophia_token, context_id)
        self.active_chats = {}  # Track active chat sessions

    async def ask_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /ask command - Ask Sophia AI a question.
        
        Usage: /ask <your question>
        """
        if not update.message or not update.message.text:
            await update.message.reply_text("Please provide a question.")
            return

        # Extract question
        question = update.message.text.replace("/ask ", "").strip()
        if not question:
            await update.message.reply_text("Please provide a question.")
            return

        user_id = update.effective_user.id
        chat_id = f"tg-{user_id}"

        try:
            # Show typing indicator
            await context.bot.send_chat_action(update.effective_chat.id, "typing")

            # Send prompt to Sophia
            chat_msg = await self.sophia_client.send_prompt(
                chat_id=chat_id,
                user_id=str(user_id),
                prompt=question,
            )

            # Show thinking indicator
            thinking_msg = await update.message.reply_text(
                "🔍 Searching knowledge base..."
            )

            # Stream response
            full_answer = ""
            async for event in self.sophia_client.stream_response(chat_id):
                fields = event.get("fields", {})

                # Collect answer
                for key, value in fields.items():
                    if key.startswith("chunks."):
                        full_answer += value

            # Delete thinking message
            await thinking_msg.delete()

            # Send answer
            if full_answer:
                # Split long answers
                max_length = 4096
                for i in range(0, len(full_answer), max_length):
                    chunk = full_answer[i : i + max_length]
                    await update.message.reply_text(
                        chunk,
                        parse_mode="Markdown",
                    )
            else:
                await update.message.reply_text("❌ No answer found.")

            logger.info(f"Sophia answered for user {user_id}")

        except Exception as e:
            logger.error(f"Error in ask handler: {str(e)}")
            await update.message.reply_text(f"⚠️ Error: {str(e)}")

    async def search_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /search command - Semantic search in knowledge base.
        
        Usage: /search <query>
        """
        if not update.message or not update.message.text:
            await update.message.reply_text("Please provide a search query.")
            return

        query = update.message.text.replace("/search ", "").strip()
        if not query:
            await update.message.reply_text("Please provide a search query.")
            return

        try:
            await context.bot.send_chat_action(update.effective_chat.id, "typing")

            # Perform semantic search
            results = await self.sophia_client.semantic_search(
                query=query,
                limit=3,
            )

            if not results:
                await update.message.reply_text(
                    f"🔍 No results found for: *{query}*",
                    parse_mode="Markdown",
                )
                return

            # Format results
            reply = f"🔍 *Search Results for:* _{query}_\n\n"
            for i, result in enumerate(results, 1):
                reply += f"*{i}. {result.filename}*\n"
                reply += f"{result.text[:200]}...\n"
                reply += f"_Relevance: {result.relevance_score:.1%}_\n\n"

            await update.message.reply_text(
                reply,
                parse_mode="Markdown",
            )

            logger.info(f"Search for user {update.effective_user.id}: {query}")

        except Exception as e:
            logger.error(f"Error in search handler: {str(e)}")
            await update.message.reply_text(f"⚠️ Error: {str(e)}")

    async def upload_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle document uploads to knowledge base.
        
        Admins can send files to upload to Sophia knowledge base.
        """
        # Check if user is admin (you should implement proper admin check)
        if not update.message or not update.message.document:
            await update.message.reply_text("Please attach a document.")
            return

        try:
            await context.bot.send_chat_action(update.effective_chat.id, "typing")

            # Download file
            file = await context.bot.get_file(update.message.document.file_id)
            file_bytes = await file.download_as_bytearray()
            filename = update.message.document.file_name

            # Upload to Sophia
            doc = await self.knowledge_manager.upload_from_bytes(
                file_bytes=bytes(file_bytes),
                filename=filename,
                tags=["telegram-bot"],
            )

            await update.message.reply_text(
                f"✅ Document uploaded: *{filename}*\n"
                f"Size: {doc.file_size} bytes\n"
                f"Status: {doc.status}",
                parse_mode="Markdown",
            )

            logger.info(f"Document uploaded: {filename}")

        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            await update.message.reply_text(f"⚠️ Upload failed: {str(e)}")

    async def list_docs_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /docs command - List uploaded documents."""
        try:
            await context.bot.send_chat_action(update.effective_chat.id, "typing")

            # List documents
            docs = await self.knowledge_manager.list_documents()

            if not docs:
                await update.message.reply_text("📚 No documents uploaded yet.")
                return

            reply = "📚 *Uploaded Documents:*\n\n"
            for doc in docs:
                reply += f"📄 *{doc.filename}*\n"
                reply += f"  Size: {doc.file_size} bytes\n"
                reply += f"  Segments: {doc.segments_count}\n"
                reply += f"  Status: {doc.status}\n\n"

            await update.message.reply_text(
                reply,
                parse_mode="Markdown",
            )

            logger.info(f"Listed {len(docs)} documents")

        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            await update.message.reply_text(f"⚠️ Error: {str(e)}")

    def get_handlers(self) -> list:
        """Get command handlers for bot.
        
        Returns:
            List of CommandHandler objects
        """
        return [
            CommandHandler("ask", self.ask_handler),
            CommandHandler("search", self.search_handler),
            CommandHandler("docs", self.list_docs_handler),
        ]
