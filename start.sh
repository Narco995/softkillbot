#!/bin/bash
set -e

echo "🚀 Starting Softkillbot..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null || true

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔐 Creating .env file..."
    cp .env.example .env
fi

# Start the bot
echo ""
echo "================================"
echo "🤖 SOFTKILLBOT IS STARTING"
echo "================================"
echo ""
echo "Bot: @Softkillbot"
echo "Telegram: t.me/Softkillbot"
echo ""
echo "Commands:"
echo "  /start - Start the bot"
echo "  /help - Show commands"
echo "  /upload - Upload documents"
echo "  /list - List documents"
echo "  /search <query> - Search"
echo "  /delete_doc <file> - Delete"
echo ""
echo "Ctrl+C to stop"
echo ""

python -m src.main