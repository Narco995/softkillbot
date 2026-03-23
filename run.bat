@echo off
echo 🚀 Starting Softkillbot...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo 🔐 Creating .env file...
    copy .env.example .env
)

echo.
echo ================================
echo 🤖 SOFTKILLBOT IS STARTING
echo ================================
echo.
echo Bot: @Softkillbot
echo Telegram: t.me/Softkillbot
echo.
echo Commands:
echo   /start - Start the bot
echo   /help - Show commands
echo   /upload - Upload documents
echo   /list - List documents
echo   /search 'query' - Search
echo   /delete_doc 'file' - Delete
echo.
echo Press Ctrl+C to stop
echo.

python -m src.main
pause