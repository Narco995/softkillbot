# Softkillbot 🤖

**Autonomous Task & Workflow Automation Telegram Bot**

A production-grade Telegram bot for intelligent task management, user analytics, background job processing, and real-time notifications.

## Features ✨

- **Task Management**: Create, update, list, and track tasks with priorities
- **Smart Notifications**: Intelligent notification scheduling and delivery
- **User Analytics**: Track engagement metrics and user behavior
- **Background Processing**: Async job execution with Celery + Redis
- **Admin Dashboard**: Real-time bot health monitoring and statistics
- **Database Persistence**: PostgreSQL for reliable data storage
- **CI/CD Pipeline**: Automated testing and deployment via GitHub Actions
- **Monitoring**: Prometheus metrics and comprehensive logging

## Commands

- `/start` - Onboarding & user registration
- `/help` - Command documentation
- `/create_task` - Create a new task
- `/list_tasks` - View all tasks with filtering
- `/update_task` - Modify task details
- `/status` - Bot health & statistics
- `/notify` - Manage notifications
- `/analytics` - View engagement metrics
- `/admin` - Admin dashboard

## Tech Stack

- **Language**: Python 3.11+
- **Bot Framework**: python-telegram-bot (async)
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
- **Testing**: pytest + coverage
- **Deployment**: Docker + GitHub Actions
- **Monitoring**: Prometheus + Structured Logging

## Project Structure

```
softkillbot/
├── src/
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── main.py              # Bot entry point
│   │   ├── handlers/            # Command & message handlers
│   │   ├── commands/            # Command implementations
│   │   ├── callbacks/           # Callback query handlers
│   │   └── middleware/          # Custom middleware
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── session.py           # DB session management
│   │   └── migrations/          # Alembic migrations
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py      # Task business logic
│   │   ├── user_service.py      # User management
│   │   ├── analytics_service.py # Analytics processing
│   │   └── notification_service.py # Notification handling
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── celery_app.py        # Celery configuration
│   │   ├── tasks.py             # Async task definitions
│   │   └── schedulers.py        # Scheduled job handlers
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration management
│   │   ├── logger.py            # Logging setup
│   │   ├── decorators.py        # Custom decorators
│   │   └── validators.py        # Input validation
│   └── api/
│       ├── __init__.py
│       └── webhooks.py          # External API webhooks
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # pytest configuration
│   ├── test_handlers.py         # Handler tests
│   ├── test_services.py         # Service layer tests
│   ├── test_workers.py          # Worker tests
│   └── fixtures/                # Test fixtures
├── docker/
│   ├── Dockerfile               # Bot container
│   ├── Dockerfile.worker        # Worker container
│   └── docker-compose.yml       # Multi-container setup
├── .github/
│   └── workflows/
│       ├── ci.yml               # CI pipeline
│       └── deploy.yml           # CD pipeline
├── config/
│   ├── settings.py              # Environment settings
│   ├── logging.yaml             # Logging configuration
│   └── prometheus.yml           # Prometheus config
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── Makefile                     # Development commands
└── docker-compose.yml           # Local development setup
```

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 7+

### Setup

```bash
# Clone repository
git clone https://github.com/Narco995/softkillbot.git
cd softkillbot

# Create environment file
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Start services (Docker Compose)
docker-compose up -d

# Run migrations
alembic upgrade head

# Start bot
python -m src.bot.main
```

## Development

```bash
# Run tests
make test

# Run tests with coverage
make test-coverage

# Format code
make format

# Lint code
make lint

# Type check
make type-check
```

## Deployment

The bot is production-ready with automated CI/CD:

1. **GitHub Actions** runs tests on every push
2. **Docker** containers ensure consistency
3. **Kubernetes** ready for scaling (optional)
4. **Monitoring** via Prometheus & structured logging

## Configuration

Set environment variables in `.env`:

```
TELEGRAM_TOKEN=your_bot_token
DATABASE_URL=postgresql://user:pass@localhost/softkillbot
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
DEBUG=False
```

## License

MIT License - See LICENSE file

## Support

For issues and feature requests, please open a GitHub issue.
