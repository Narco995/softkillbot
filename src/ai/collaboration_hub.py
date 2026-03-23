"""Real-Time Collaboration Hub for Multi-User Task Management."""

from typing import Dict, List, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

from ..utils.logger import logger


class CollaborationEventType(str, Enum):
    """Types of collaboration events."""
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    COMMENT_ADDED = "comment_added"
    USER_JOINED = "user_joined"
    CONFLICT_DETECTED = "conflict_detected"
    CHANGE_MERGED = "change_merged"


@dataclass
class CollaborationEvent:
    """Collaboration event."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: CollaborationEventType = CollaborationEventType.TASK_UPDATED
    user_id: str = ""
    task_id: str = ""
    data: Dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: int = 1


@dataclass
class CollaborativeSession:
    """Active collaboration session."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    active_users: Set[str] = field(default_factory=set)
    changes: List[Dict] = field(default_factory=list)
    conflicts: List[Dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)


class CollaborationHub:
    """Real-time collaboration hub for multi-user workflows."""

    def __init__(self):
        """Initialize collaboration hub."""
        self.sessions: Dict[str, CollaborativeSession] = {}
        self.event_log: List[CollaborationEvent] = []
        self.user_subscriptions: Dict[str, Set[str]] = {}  # user_id -> task_ids
        self.conflict_resolver = ConflictResolver()

    def create_session(self, task_id: str, user_id: str) -> str:
        """Create new collaboration session."""
        session = CollaborativeSession(task_id=task_id)
        session.active_users.add(user_id)
        self.sessions[session.session_id] = session

        logger.info(f"Collaboration session created: {session.session_id}")
        return session.session_id

    def join_session(self, session_id: str, user_id: str) -> bool:
        """User joins collaboration session."""
        if session_id not in self.sessions:
            return False

        session = self.sessions[session_id]
        session.active_users.add(user_id)
        session.last_activity = datetime.utcnow()

        # Log event
        self._log_event(
            CollaborationEventType.USER_JOINED,
            user_id,
            session.task_id,
            {"session_id": session_id},
        )

        logger.info(f"User {user_id} joined session {session_id}")
        return True

    def apply_change(self, session_id: str, user_id: str, change: Dict) -> Dict:
        """Apply change to collaborative task."""
        if session_id not in self.sessions:
            return {"status": "error", "message": "Session not found"}

        session = self.sessions[session_id]
        change["user_id"] = user_id
        change["timestamp"] = datetime.utcnow().isoformat()
        change["version"] = len(session.changes) + 1

        # Check for conflicts
        conflicts = self._detect_conflicts(session, change)

        if conflicts:
            # Attempt to resolve conflicts
            resolved = self.conflict_resolver.resolve(session.changes, change)
            if resolved:
                session.changes.append(resolved)
                self._log_event(
                    CollaborationEventType.CHANGE_MERGED,
                    user_id,
                    session.task_id,
                    {"change": resolved},
                )
                return {"status": "merged", "change": resolved}
            else:
                session.conflicts.append({"change": change, "conflicts": conflicts})
                self._log_event(
                    CollaborationEventType.CONFLICT_DETECTED,
                    user_id,
                    session.task_id,
                    {"conflicts": conflicts},
                )
                return {"status": "conflict", "conflicts": conflicts}
        else:
            session.changes.append(change)
            session.last_activity = datetime.utcnow()
            self._log_event(
                CollaborationEventType.TASK_UPDATED,
                user_id,
                session.task_id,
                {"change": change},
            )
            return {"status": "applied", "change": change}

    def get_session_state(self, session_id: str) -> Dict:
        """Get current state of collaboration session."""
        if session_id not in self.sessions:
            return {"error": "Session not found"}

        session = self.sessions[session_id]
        return {
            "session_id": session_id,
            "task_id": session.task_id,
            "active_users": list(session.active_users),
            "num_changes": len(session.changes),
            "num_conflicts": len(session.conflicts),
            "last_activity": session.last_activity.isoformat(),
        }

    def get_activity_stream(self, task_id: str, limit: int = 50) -> List[Dict]:
        """Get activity stream for task."""
        events = [
            {
                "event_type": e.event_type.value,
                "user_id": e.user_id,
                "timestamp": e.timestamp.isoformat(),
                "data": e.data,
            }
            for e in self.event_log
            if e.task_id == task_id
        ]
        return events[-limit:]

    def resolve_conflicts_manually(self, session_id: str, resolution: Dict) -> bool:
        """Manually resolve conflicts."""
        if session_id not in self.sessions:
            return False

        session = self.sessions[session_id]
        session.conflicts = [c for c in session.conflicts if c != resolution["conflict"]]
        session.changes.append(resolution["resolved_change"])

        logger.info(f"Conflict resolved manually in session {session_id}")
        return True

    def _detect_conflicts(self, session: CollaborativeSession, change: Dict) -> List[Dict]:
        """Detect conflicts with existing changes."""
        conflicts = []
        change_field = change.get("field")

        for existing_change in session.changes:
            if existing_change.get("field") == change_field:
                # Same field modified - potential conflict
                if existing_change.get("value") != change.get("value"):
                    conflicts.append({
                        "field": change_field,
                        "existing_value": existing_change.get("value"),
                        "new_value": change.get("value"),
                    })

        return conflicts

    def _log_event(self, event_type: CollaborationEventType, user_id: str, task_id: str, data: Dict):
        """Log collaboration event."""
        event = CollaborationEvent(
            event_type=event_type,
            user_id=user_id,
            task_id=task_id,
            data=data,
        )
        self.event_log.append(event)


class ConflictResolver:
    """Resolves conflicts in collaborative editing."""

    def resolve(self, existing_changes: List[Dict], new_change: Dict) -> Dict:
        """Attempt to resolve conflict automatically."""
        # Simple merge strategy: prefer newer changes
        resolved = new_change.copy()
        resolved["merge_strategy"] = "last_write_wins"
        return resolved
