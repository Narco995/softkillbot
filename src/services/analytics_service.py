"""Analytics service for tracking user behavior."""

from datetime import datetime
from sqlalchemy.orm import Session
from ..database.models import UserAnalytics, Task, TaskStatus
from ..utils.logger import logger


class AnalyticsService:
    """Service for analytics and metrics."""

    @staticmethod
    def get_user_stats(db: Session, user_id: int) -> dict:
        """Get user statistics."""
        analytics = db.query(UserAnalytics).filter(UserAnalytics.user_id == user_id).first()
        if not analytics:
            return None

        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        completion_rate = (
            (analytics.total_tasks_completed / analytics.total_tasks_created * 100)
            if analytics.total_tasks_created > 0
            else 0
        )

        return {
            "total_tasks_created": analytics.total_tasks_created,
            "total_tasks_completed": analytics.total_tasks_completed,
            "completion_rate": round(completion_rate, 2),
            "total_commands_used": analytics.total_commands_used,
            "last_activity": analytics.last_activity.isoformat(),
            "active_tasks": len([t for t in tasks if t.status != TaskStatus.COMPLETED]),
        }

    @staticmethod
    def get_system_stats(db: Session) -> dict:
        """Get system-wide statistics."""
        try:
            total_users = db.query(UserAnalytics).count()
            total_tasks = db.query(Task).count()
            completed_tasks = db.query(Task).filter(Task.status == TaskStatus.COMPLETED).count()

            return {
                "total_users": total_users,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_rate": (
                    (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                ),
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error getting system stats: {str(e)}")
            return {}
