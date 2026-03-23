"""Async task definitions for background processing."""

from datetime import datetime
from .celery_app import app
from ..database.session import SessionLocal
from ..database.models import Task, TaskStatus, Notification
from ..utils.logger import logger


@app.task(name='tasks.send_notification')
def send_notification(user_id: int, message: str):
    """Send notification to user."""
    db = SessionLocal()
    try:
        notification = Notification(
            user_id=user_id,
            message=message,
            is_sent=True,
            sent_at=datetime.utcnow(),
        )
        db.add(notification)
        db.commit()
        logger.info(f"Notification sent to user {user_id}")
        return {"status": "success", "message": "Notification sent"}
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@app.task(name='tasks.check_overdue_tasks')
def check_overdue_tasks():
    """Check and notify about overdue tasks."""
    db = SessionLocal()
    try:
        overdue_tasks = db.query(Task).filter(
            Task.status != TaskStatus.COMPLETED,
            Task.due_date < datetime.utcnow(),
        ).all()

        for task in overdue_tasks:
            message = f"⚠️ Task '{task.title}' is overdue!"
            send_notification.delay(task.user_id, message)

        logger.info(f"Checked {len(overdue_tasks)} overdue tasks")
        return {"status": "success", "checked": len(overdue_tasks)}
    except Exception as e:
        logger.error(f"Error checking overdue tasks: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@app.task(name='tasks.cleanup_old_data')
def cleanup_old_data():
    """Cleanup old completed tasks and notifications."""
    db = SessionLocal()
    try:
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=30)

        # Delete old completed tasks
        deleted_tasks = db.query(Task).filter(
            Task.status == TaskStatus.COMPLETED,
            Task.completed_at < cutoff_date,
        ).delete()

        # Delete old notifications
        deleted_notifications = db.query(Notification).filter(
            Notification.created_at < cutoff_date,
        ).delete()

        db.commit()
        logger.info(f"Cleanup: deleted {deleted_tasks} tasks and {deleted_notifications} notifications")
        return {
            "status": "success",
            "deleted_tasks": deleted_tasks,
            "deleted_notifications": deleted_notifications,
        }
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
