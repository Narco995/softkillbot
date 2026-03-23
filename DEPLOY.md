# 🚀 Deployment Guide - Softkillbot

## Quick Start

### Linux/macOS
```bash
bash start.sh
```

### Windows
```bash
run.bat
```

### Or use Make
```bash
make install
make run
```

---

## Manual Setup

### 1. Clone Repository
```bash
git clone https://github.com/Narco995/softkillbot.git
cd softkillbot
```

### 2. Create Virtual Environment
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment
```bash
cp .env.example .env
# Edit .env with your tokens
```

### 5. Run Bot
```bash
python -m src.main
```

---

## Docker Deployment

### Build Image
```bash
make docker-build
# or
docker build -f docker/Dockerfile -t softkillbot .
```

### Run Container
```bash
make docker-run
# or
docker run -e TELEGRAM_TOKEN=your_token \
           -e RESTHEART_JWT_TOKEN=your_jwt \
           softkillbot
```

### Docker Compose
```bash
docker-compose -f docker/docker-compose.yml up -d
```

---

## Environment Variables

```env
TELEGRAM_TOKEN=your_bot_token_here
RESTHEART_JWT_TOKEN=your_jwt_token_here
DATABASE_URL=sqlite:///./softkillbot.db
LOG_LEVEL=INFO
```

---

## Testing

```bash
# Run all tests
make test
# or
pytest tests/ -v

# With coverage
pytest tests/ --cov=src
```

---

## Production Deployment

### Option 1: Systemd Service (Linux)

Create `/etc/systemd/system/softkillbot.service`:
```ini
[Unit]
Description=Softkillbot Telegram Bot
After=network.target

[Service]
Type=simple
User=bot
WorkingDirectory=/home/bot/softkillbot
Environment="PATH=/home/bot/softkillbot/venv/bin"
ExecStart=/home/bot/softkillbot/venv/bin/python -m src.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable softkillbot
sudo systemctl start softkillbot
sudo systemctl status softkillbot
```

### Option 2: PM2 (Node.js Runtime)

```bash
npm install -g pm2
pm2 start "python -m src.main" --name softkillbot
pm2 save
pm2 startup
```

### Option 3: Cloud Deployment

**Heroku:**
```bash
heroku login
heroku create softkillbot
git push heroku main
```

**AWS Lambda + Telegram Webhook:**
- Use API Gateway with Lambda
- Configure Telegram webhook
- Deploy with AWS SAM

**DigitalOcean:**
```bash
doctl apps create --spec app.yaml
```

---

## Troubleshooting

### Bot not responding
- Check TELEGRAM_TOKEN is valid
- Ensure bot is running: `ps aux | grep src.main`
- Check logs for errors

### RESTHeart connection failed
- Verify RESTHEART_JWT_TOKEN is valid
- Check JWT token expiration
- Verify internet connection

### Import errors
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Ensure Python 3.11+: `python --version`

---

## Monitoring

```bash
# View logs
tail -f logs/*.log

# Monitor process
top

# With docker
docker logs -f softkillbot
```

---

## Support

- 📖 [Telegram Bot API](https://core.telegram.org/bots/api)
- 🌐 [RESTHeart Docs](https://restheart.org/docs/)
- 💬 [@Softkillbot](https://t.me/Softkillbot)
