import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    CallbackQueryHandler
)
from src.config import settings
from src.handlers.documents import DocumentHandler, UPLOAD_DOCUMENT, CONFIRM_UPLOAD
from src.handlers.chat import ChatHandler

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=settings.LOG_LEVEL
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot"""
    
    # Create application
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()
    
    # Initialize handlers
    doc_handler = DocumentHandler()
    chat_handler = ChatHandler()
    
    # Upload conversation
    upload_conv = ConversationHandler(
        entry_points=[CommandHandler("upload", doc_handler.upload_start)],
        states={
            UPLOAD_DOCUMENT: [
                MessageHandler(filters.Document.ALL, doc_handler.handle_document)
            ],
            CONFIRM_UPLOAD: [
                CallbackQueryHandler(doc_handler.confirm_upload, pattern="confirm_upload"),
                CallbackQueryHandler(doc_handler.cancel_upload, pattern="cancel_upload")
            ]
        },
        fallbacks=[CommandHandler("cancel", doc_handler.cancel_upload)]
    )
    
    # Add handlers
    application.add_handler(upload_conv)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("list", doc_handler.list_documents))
    application.add_handler(CommandHandler("search", chat_handler.search))
    application.add_handler(CommandHandler("delete_doc", doc_handler.delete_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler.chat))
    
    # Start bot
    logger.info("Starting Softkillbot...")
    application.run_polling(allowed_updates=['message', 'callback_query'])

async def start(update, context):
    """Start command"""
    await update.message.reply_text(
        "🤖 **Welcome to Softkillbot!**\n\n"
        "I can help you manage your knowledge base and chat with documents.\n\n"
        "Use /help for available commands."
    )

async def help_command(update, context):
    """Help command"""
    help_text = """
📚 **Available Commands:**

*Document Management:*
/upload - Upload a document
/list - List all documents
/delete_doc <filename> - Delete a document

*Knowledge Base:*
/search <query> - Search documents

*Bot:*
/help - Show this message
/start - Start the bot
"""
    await update.message.reply_text(help_text)

if __name__ == '__main__':
    main()