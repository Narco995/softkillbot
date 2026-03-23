# Softkillbot Deployment Guide

## Local Development Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Git

### Quick Start

```bash
# Clone repository
git clone https://github.com/Narco995/softkillbot.git
cd softkillbot

# Copy environment file
cp .env.example .env

# Start services
docker-compose up -d

# Install dependencies (for local development)
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start bot
python -m src.bot.main
```

## Production Deployment

### Using Docker Compose

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f bot
```

### Using Kubernetes (Optional)

1. Build and push Docker images to registry
2. Create Kubernetes manifests
3. Deploy using kubectl

### Environment Variables

Set in `.env` file:

```
TELEGRAM_TOKEN=your_bot_token
DATABASE_URL=postgresql://user:pass@postgres:5432/softkillbot
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
DEBUG=False
LOG_LEVEL=INFO
ENVIRONMENT=production
```

## Monitoring

### Logs

```bash
# View bot logs
docker-compose logs -f bot

# View worker logs
docker-compose logs -f celery_worker
```

### Database

```bash
# Connect to PostgreSQL
psql postgresql://softkill_user:softkill_pass@localhost:5432/softkillbot

# Check Redis
redis-cli -h localhost ping
```

## Maintenance

### Database Backup

```bash
# Backup database
docker-compose exec postgres pg_dump -U softkill_user softkillbot > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T postgres psql -U softkill_user softkillbot
```

### Updates

```bash
# Pull latest code
git pull origin main

# Rebuild images
docker-compose build

# Restart services
docker-compose up -d
```

## Troubleshooting

### Bot not responding

1. Check logs: `docker-compose logs bot`
2. Verify token is correct in `.env`
3. Check database connection
4. Restart bot: `docker-compose restart bot`

### Database connection errors

1. Check PostgreSQL is running: `docker-compose ps postgres`
2. Verify credentials in `.env`
3. Check database exists: `docker-compose exec postgres psql -U softkill_user -l`

### Worker not processing tasks

1. Check worker logs: `docker-compose logs celery_worker`
2. Verify Redis is running: `docker-compose ps redis`
3. Check Celery broker URL in `.env`
4. Restart worker: `docker-compose restart celery_worker`
