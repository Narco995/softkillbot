"""Configuration management for Softkillbot."""

import os
from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Telegram
    telegram_token: str = Field(..., alias="TELEGRAM_TOKEN")
    bot_username: str = Field("Softkillbot", alias="BOT_USERNAME")

    # Database
    database_url: str = Field(..., alias="DATABASE_URL")
    database_echo: bool = Field(False, alias="DATABASE_ECHO")

    # Redis
    redis_url: str = Field("redis://localhost:6379/0", alias="REDIS_URL")
    redis_pool_size: int = Field(10, alias="REDIS_POOL_SIZE")

    # Celery
    celery_broker_url: str = Field("redis://localhost:6379/1", alias="CELERY_BROKER_URL")
    celery_result_backend: str = Field("redis://localhost:6379/2", alias="CELERY_RESULT_BACKEND")
    celery_worker_concurrency: int = Field(4, alias="CELERY_WORKER_CONCURRENCY")

    # Application
    debug: bool = Field(False, alias="DEBUG")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    environment: str = Field("development", alias="ENVIRONMENT")

    # API
    api_host: str = Field("0.0.0.0", alias="API_HOST")
    api_port: int = Field(8000, alias="API_PORT")
    api_workers: int = Field(4, alias="API_WORKERS")

    # Monitoring
    prometheus_port: int = Field(9090, alias="PROMETHEUS_PORT")
    enable_metrics: bool = Field(True, alias="ENABLE_METRICS")

    # Features
    enable_analytics: bool = Field(True, alias="ENABLE_ANALYTICS")
    enable_notifications: bool = Field(True, alias="ENABLE_NOTIFICATIONS")
    max_tasks_per_user: int = Field(100, alias="MAX_TASKS_PER_USER")
    task_timeout_seconds: int = Field(3600, alias="TASK_TIMEOUT_SECONDS")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
