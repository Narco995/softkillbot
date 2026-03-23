"""Celery application and task queue configuration."""

from celery import Celery
from ..utils.config import get_settings

settings = get_settings()

# Create Celery app
app = Celery(
    'softkillbot',
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# Configure Celery
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    worker_concurrency=settings.celery_worker_concurrency,
)


@app.task(bind=True)
def debug_task(self):
    """Debug task for testing."""
    print(f'Request: {self.request!r}')
