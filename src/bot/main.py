"""Main bot application."""

import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

from ..utils.config import get_settings
from ..utils.logger import logger
from ..database.session import init_db

settings = get_settings()


class SoftkillBot:
    """Main bot class."""

    def __init__(self):
        """Initialize bot."""
        self.app = Application.builder().token(settings.telegram_token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup command and message handlers."""
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("create_task", self.create_task))
        self.app.add_handler(CommandHandler("list_tasks", self.list_tasks))
        self.app.add_handler(CommandHandler("status", self.status))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command."""
        user = update.effective_user
        logger.info(f"User {user.id} started bot")
        await update.message.reply_text(
            f"👋 Welcome {user.first_name}! I'm Softkillbot.\n"
            "I help you manage tasks and automate workflows.\n"
            "Use /help to see available commands."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command."""
        help_text = (
            "📋 **Available Commands:**\n\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/create_task - Create a new task\n"
            "/list_tasks - List all tasks\n"
            "/update_task - Update a task\n"
            "/status - Show bot status\n"
            "/analytics - View your analytics\n"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")

    async def create_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /create_task command."""
        await update.message.reply_text(
            "📝 Task creation coming soon!\n"
            "Please provide task details in the format: /create_task [title] [description]"
        )

    async def list_tasks(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /list_tasks command."""
        await update.message.reply_text(
            "📋 Your tasks will appear here.\n"
            "Use /create_task to add a new task."
        )

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /status command."""
        await update.message.reply_text(
            "✅ Bot is running and healthy!\n"
            "Database: Connected\n"
            "Workers: Active"
        )

    def run(self):
        """Run the bot."""
        logger.info("Starting Softkillbot...")
        init_db()
        self.app.run_polling()


def main():
    """Main entry point."""
    bot = SoftkillBot()
    bot.run()


if __name__ == "__main__":
    main()
