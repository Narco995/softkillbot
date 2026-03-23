"""Task service for managing tasks."""

from datetime import datetime
from sqlalchemy.orm import Session
from ..database.models import Task, TaskStatus, TaskPriority, UserAnalytics
from ..utils.logger import logger


class TaskService:
    """Service for task management operations."""

    @staticmethod
    def create_task(
        db: Session,
        user_id: int,
        title: str,
        description: str = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        due_date: datetime = None,
    ) -> Task:
        """Create a new task."""
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        # Update analytics
        analytics = db.query(UserAnalytics).filter(UserAnalytics.user_id == user_id).first()
        if analytics:
            analytics.total_tasks_created += 1
            db.commit()

        logger.info(f"Task {task.id} created for user {user_id}")
        return task

    @staticmethod
    def get_task(db: Session, task_id: int, user_id: int) -> Task:
        """Get task by ID (with user verification)."""
        return db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()

    @staticmethod
    def list_tasks(db: Session, user_id: int, status: TaskStatus = None) -> list:
        """List tasks for a user."""
        query = db.query(Task).filter(Task.user_id == user_id)
        if status:
            query = query.filter(Task.status == status)
        return query.order_by(Task.created_at.desc()).all()

    @staticmethod
    def update_task(db: Session, task_id: int, user_id: int, **kwargs) -> Task:
        """Update task."""
        task = TaskService.get_task(db, task_id, user_id)
        if not task:
            return None

        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)

        db.commit()
        db.refresh(task)
        logger.info(f"Task {task_id} updated")
        return task

    @staticmethod
    def complete_task(db: Session, task_id: int, user_id: int) -> Task:
        """Mark task as completed."""
        task = TaskService.update_task(
            db,
            task_id,
            user_id,
            status=TaskStatus.COMPLETED,
            completed_at=datetime.utcnow(),
        )

        if task:
            # Update analytics
            analytics = db.query(UserAnalytics).filter(UserAnalytics.user_id == user_id).first()
            if analytics:
                analytics.total_tasks_completed += 1
                db.commit()

        return task

    @staticmethod
    def delete_task(db: Session, task_id: int, user_id: int) -> bool:
        """Delete task."""
        task = TaskService.get_task(db, task_id, user_id)
        if not task:
            return False

        db.delete(task)
        db.commit()
        logger.info(f"Task {task_id} deleted")
        return True
