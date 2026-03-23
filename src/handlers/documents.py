import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from src.restheart.client import RESTHeartClient
from src.config import settings
import os
import tempfile

logger = logging.getLogger(__name__)

UPLOAD_DOCUMENT, CONFIRM_UPLOAD = range(2)

class DocumentHandler:
    """Handle document operations"""
    
    def __init__(self):
        self.restheart = RESTHeartClient(
            settings.RESTHEART_BASE_URL,
            settings.RESTHEART_JWT_TOKEN
        )
    
    async def upload_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start document upload"""
        await update.message.reply_text(
            "📄 Send me a document to upload to the knowledge base.\n"
            "Supported formats: PDF, TXT, DOCX\n"
            "Max size: 50MB"
        )
        return UPLOAD_DOCUMENT
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document file"""
        document = update.message.document
        
        # Validate file size
        if document.file_size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            await update.message.reply_text(
                f"❌ File too large! Max: {settings.MAX_FILE_SIZE_MB}MB"
            )
            return UPLOAD_DOCUMENT
        
        # Download file
        file = await context.bot.get_file(document.file_id)
        with tempfile.NamedTemporaryFile(delete=False, suffix=document.file_name) as tmp:
            file_bytes = await file.download_as_bytearray()
            tmp.write(file_bytes)
            tmp_path = tmp.name
        
        # Ask for confirmation
        keyboard = [
            [
                InlineKeyboardButton("✅ Upload", callback_data="confirm_upload"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel_upload")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.user_data['temp_file'] = tmp_path
        context.user_data['filename'] = document.file_name
        
        await update.message.reply_text(
            f"📋 Confirm upload of: `{document.file_name}`?",
            reply_markup=reply_markup
        )
        return CONFIRM_UPLOAD
    
    async def confirm_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Confirm and upload document"""
        query = update.callback_query
        await query.answer()
        
        tmp_path = context.user_data.get('temp_file')
        filename = context.user_data.get('filename')
        
        try:
            await query.edit_message_text("⏳ Uploading...")
            
            result = await self.restheart.upload_document(
                tmp_path,
                metadata={"tags": ["telegram"], "uploaded_by": str(update.effective_user.id)}
            )
            
            await query.edit_message_text(
                f"✅ Document uploaded successfully!\n"
                f"📄 Filename: `{filename}`"
            )
        except Exception as e:
            logger.error(f"Upload error: {e}")
            await query.edit_message_text(f"❌ Upload failed: {str(e)}")
        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        
        return ConversationHandler.END
    
    async def cancel_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel upload"""
        query = update.callback_query
        await query.answer()
        
        tmp_path = context.user_data.get('temp_file')
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        
        await query.edit_message_text("❌ Upload cancelled.")
        return ConversationHandler.END
    
    async def list_documents(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List all documents"""
        try:
            await update.message.reply_text("⏳ Fetching documents...")
            
            docs = await self.restheart.list_documents()
            
            if not docs:
                await update.message.reply_text("📭 No documents found.")
                return
            
            message = "📚 **Knowledge Base Documents:**\n\n"
            for i, doc in enumerate(docs, 1):
                filename = doc.get('_id', 'Unknown')
                message += f"{i}. `{filename}`\n"
            
            await update.message.reply_text(message)
        except Exception as e:
            logger.error(f"List error: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def delete_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Delete a document"""
        if not context.args:
            await update.message.reply_text(
                "Usage: `/delete_doc <filename>`"
            )
            return
        
        filename = ' '.join(context.args)
        
        try:
            success = await self.restheart.delete_document(filename)
            
            if success:
                await update.message.reply_text(f"✅ Document `{filename}` deleted.")
            else:
                await update.message.reply_text(f"❌ Could not delete document.")
        except Exception as e:
            logger.error(f"Delete error: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")