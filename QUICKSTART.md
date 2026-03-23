# 🚀 QUICKSTART - Get Softkillbot Running in 30 Seconds

## Linux/macOS

```bash
# 1. Clone
git clone https://github.com/Narco995/softkillbot.git
cd softkillbot

# 2. Run (one command!)
bash start.sh
```

**DONE!** Bot is running. Go to t.me/Softkillbot

---

## Windows

```bash
# 1. Clone
git clone https://github.com/Narco995/softkillbot.git
cd softkillbot

# 2. Run
run.bat
```

**DONE!** Bot is running. Go to t.me/Softkillbot

---

## Docker (Any OS)

```bash
# 1. Clone
git clone https://github.com/Narco995/softkillbot.git
cd softkillbot

# 2. Build
docker build -f docker/Dockerfile -t softkillbot .

# 3. Run
docker run -e TELEGRAM_TOKEN=8245547877:AAFq-l4tSh7OL3sNcvPifMDyj_wwPKYMR90 \
           -e RESTHEART_JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmcmVlLnJlc3RoZWFydC5jb20iLCJzdWIiOiJhYmluYXRoYXNob2tAZ21haWwuY29tIiwiZXhwIjoxNzc0MjkxMjUxLCJzcnZOb2RlIjoiZmJhNDZhLnVzLWVhc3QtMS1mcmVlLTEucmVzdGhlYXJ0LmNvbSIsInJvbGVzIjpbInNydi1hZG1pbiJdfQ.d4HCH2o3r0RyqUo26YSSZ2b9ScOJ2Rhude2Uu6k_cuQ \
           softkillbot
```

**DONE!** Bot is running in Docker.

---

## 📄 Commands

Once running, try these in Telegram:

- `/start` - Welcome
- `/help` - All commands
- `/upload` - Upload documents
- `/list` - List documents
- `/search hello` - Search
- `/delete_doc filename` - Delete
- Send any message to chat

---

## 🔧 Troubleshooting

### Bot not responding?
1. Check it's running: `ps aux | grep src.main`
2. Check logs for errors
3. Verify tokens in `.env`

### ModuleNotFoundError?
```bash
pip install -r requirements.txt --force-reinstall
```

### Permission denied on start.sh?
```bash
chmod +x start.sh
bash start.sh
```

---

## 🔗 Links

- Bot: [t.me/Softkillbot](https://t.me/Softkillbot)
- GitHub: [github.com/Narco995/softkillbot](https://github.com/Narco995/softkillbot)
- Docs: [DEPLOY.md](DEPLOY.md)
