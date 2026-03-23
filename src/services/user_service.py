"""User service for managing user data."""

from sqlalchemy.orm import Session
from ..database.models import User, UserAnalytics
from ..utils.logger import logger


class UserService:
    """Service for user management operations."""

    @staticmethod
    def get_or_create_user(
        db: Session,
        telegram_id: str,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
    ) -> User:
        """Get existing user or create new one."""
        user = db.query(User).filter(User.telegram_id == telegram_id).first()

        if user:
            logger.info(f"User {telegram_id} found")
            return user

        # Create new user
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create analytics record
        analytics = UserAnalytics(user_id=user.id)
        db.add(analytics)
        db.commit()

        logger.info(f"User {telegram_id} created")
        return user

    @staticmethod
    def get_user(db: Session, telegram_id: str) -> User:
        """Get user by telegram ID."""
        return db.query(User).filter(User.telegram_id == telegram_id).first()

    @staticmethod
    def update_user(db: Session, telegram_id: str, **kwargs) -> User:
        """Update user information."""
        user = UserService.get_user(db, telegram_id)
        if not user:
            return None

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        db.commit()
        db.refresh(user)
        logger.info(f"User {telegram_id} updated")
        return user

    @staticmethod
    def get_user_analytics(db: Session, user_id: int) -> UserAnalytics:
        """Get user analytics."""
        return db.query(UserAnalytics).filter(UserAnalytics.user_id == user_id).first()

    @staticmethod
    def increment_command_count(db: Session, user_id: int):
        """Increment user command count."""
        analytics = UserService.get_user_analytics(db, user_id)
        if analytics:
            analytics.total_commands_used += 1
            db.commit()
