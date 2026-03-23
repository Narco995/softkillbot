"""Tests for service layer."""

import pytest
from datetime import datetime
from src.database.models import TaskStatus, TaskPriority
from src.services.user_service import UserService
from src.services.task_service import TaskService


class TestUserService:
    """Tests for UserService."""

    def test_get_or_create_user_new(self, db_session):
        """Test creating a new user."""
        user = UserService.get_or_create_user(
            db_session,
            telegram_id="123456",
            username="testuser",
            first_name="Test",
            last_name="User",
        )

        assert user.telegram_id == "123456"
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.is_active is True
        assert user.is_admin is False

    def test_get_or_create_user_existing(self, db_session):
        """Test getting existing user."""
        # Create user
        user1 = UserService.get_or_create_user(
            db_session,
            telegram_id="123456",
            username="testuser",
        )

        # Get same user
        user2 = UserService.get_or_create_user(
            db_session,
            telegram_id="123456",
            username="testuser",
        )

        assert user1.id == user2.id

    def test_update_user(self, db_session):
        """Test updating user."""
        user = UserService.get_or_create_user(
            db_session,
            telegram_id="123456",
            username="testuser",
        )

        updated = UserService.update_user(
            db_session,
            telegram_id="123456",
            username="newusername",
        )

        assert updated.username == "newusername"


class TestTaskService:
    """Tests for TaskService."""

    @pytest.fixture
    def user(self, db_session):
        """Create test user."""
        return UserService.get_or_create_user(
            db_session,
            telegram_id="123456",
            username="testuser",
        )

    def test_create_task(self, db_session, user):
        """Test creating a task."""
        task = TaskService.create_task(
            db_session,
            user_id=user.id,
            title="Test Task",
            description="Test Description",
            priority=TaskPriority.HIGH,
        )

        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == TaskPriority.HIGH
        assert task.status == TaskStatus.PENDING

    def test_list_tasks(self, db_session, user):
        """Test listing tasks."""
        # Create multiple tasks
        for i in range(3):
            TaskService.create_task(
                db_session,
                user_id=user.id,
                title=f"Task {i}",
            )

        tasks = TaskService.list_tasks(db_session, user.id)
        assert len(tasks) == 3

    def test_complete_task(self, db_session, user):
        """Test completing a task."""
        task = TaskService.create_task(
            db_session,
            user_id=user.id,
            title="Test Task",
        )

        completed = TaskService.complete_task(
            db_session,
            task_id=task.id,
            user_id=user.id,
        )

        assert completed.status == TaskStatus.COMPLETED
        assert completed.completed_at is not None
