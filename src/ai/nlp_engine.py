"""NLP Engine for intelligent task understanding and processing."""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

from ..utils.logger import logger
from ..utils.config import get_settings


class TaskCategory(str, Enum):
    """Task categories identified by AI."""
    URGENT = "urgent"
    STANDARD = "standard"
    RESEARCH = "research"
    DEVELOPMENT = "development"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"
    MEETING = "meeting"
    REVIEW = "review"


class TaskComplexity(str, Enum):
    """Complexity levels determined by AI analysis."""
    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    CRITICAL = "critical"


@dataclass
class TaskIntelligence:
    """AI-powered task analysis results."""
    original_text: str
    extracted_title: str
    extracted_description: str
    category: TaskCategory
    complexity: TaskComplexity
    estimated_duration_minutes: int
    suggested_priority: int  # 1-5
    dependencies: List[str]
    skills_required: List[str]
    subtasks: List[str]
    suggested_assignee_type: str
    confidence_score: float


class NLPEngine:
    """NLP engine for intelligent task processing."""

    # Knowledge base for pattern matching
    CATEGORY_KEYWORDS = {
        TaskCategory.URGENT: ["asap", "urgent", "immediate", "critical", "now"],
        TaskCategory.DEVELOPMENT: ["code", "build", "implement", "develop", "feature"],
        TaskCategory.TESTING: ["test", "verify", "check", "validate", "qa"],
        TaskCategory.DOCUMENTATION: ["doc", "write", "guide", "readme", "manual"],
        TaskCategory.DEPLOYMENT: ["deploy", "release", "push", "launch", "server"],
        TaskCategory.RESEARCH: ["research", "investigate", "explore", "analyze", "study"],
        TaskCategory.MEETING: ["meeting", "call", "standup", "sync", "discussion"],
        TaskCategory.REVIEW: ["review", "check", "approve", "feedback"],
    }

    COMPLEXITY_INDICATORS = {
        TaskComplexity.TRIVIAL: ["simple", "quick", "minor", "small"],
        TaskComplexity.SIMPLE: ["basic", "straightforward", "easy"],
        TaskComplexity.MODERATE: ["moderate", "medium", "standard"],
        TaskComplexity.COMPLEX: ["complex", "complicated", "advanced"],
        TaskComplexity.CRITICAL: ["critical", "emergency", "blocking", "severe"],
    }

    DURATION_ESTIMATES = {
        TaskComplexity.TRIVIAL: 15,
        TaskComplexity.SIMPLE: 30,
        TaskComplexity.MODERATE: 120,
        TaskComplexity.COMPLEX: 480,
        TaskComplexity.CRITICAL: 60,
    }

    @staticmethod
    def analyze_task(task_text: str) -> TaskIntelligence:
        """Analyze task using NLP and ML techniques."""
        try:
            text_lower = task_text.lower()

            # Extract category
            category = NLPEngine._extract_category(text_lower)

            # Extract complexity
            complexity = NLPEngine._extract_complexity(text_lower)

            # Extract title
            title = NLPEngine._extract_title(task_text)

            # Extract description
            description = NLPEngine._extract_description(task_text)

            # Detect dependencies
            dependencies = NLPEngine._detect_dependencies(text_lower)

            # Extract skills
            skills = NLPEngine._extract_skills(text_lower)

            # Generate subtasks
            subtasks = NLPEngine._generate_subtasks(task_text, complexity)

            # Estimate duration
            duration = NLPEngine.DURATION_ESTIMATES.get(complexity, 60)

            # Determine priority (1-5)
            priority = NLPEngine._calculate_priority(category, complexity, text_lower)

            # Confidence score
            confidence = NLPEngine._calculate_confidence(text_lower)

            logger.info(f"Task analyzed: {title} (Confidence: {confidence:.2%})")

            return TaskIntelligence(
                original_text=task_text,
                extracted_title=title,
                extracted_description=description,
                category=category,
                complexity=complexity,
                estimated_duration_minutes=duration,
                suggested_priority=priority,
                dependencies=dependencies,
                skills_required=skills,
                subtasks=subtasks,
                suggested_assignee_type=category.value,
                confidence_score=confidence,
            )
        except Exception as e:
            logger.error(f"Error analyzing task: {str(e)}")
            raise

    @staticmethod
    def _extract_category(text: str) -> TaskCategory:
        """Extract task category from text."""
        scores = {}
        for category, keywords in NLPEngine.CATEGORY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text)
            scores[category] = score

        best_match = max(scores, key=scores.get)
        return best_match if scores[best_match] > 0 else TaskCategory.STANDARD

    @staticmethod
    def _extract_complexity(text: str) -> TaskComplexity:
        """Extract task complexity from text."""
        for complexity, indicators in NLPEngine.COMPLEXITY_INDICATORS.items():
            if any(indicator in text for indicator in indicators):
                return complexity
        return TaskComplexity.MODERATE

    @staticmethod
    def _extract_title(task_text: str) -> str:
        """Extract title from task text."""
        lines = task_text.split('\n')
        return lines[0][:100] if lines else "Untitled Task"

    @staticmethod
    def _extract_description(task_text: str) -> str:
        """Extract description from task text."""
        lines = task_text.split('\n')
        return '\n'.join(lines[1:]) if len(lines) > 1 else ""

    @staticmethod
    def _detect_dependencies(text: str) -> List[str]:
        """Detect task dependencies from context."""
        dependency_keywords = ["after", "before", "depends on", "requires", "needs"]
        dependencies = []

        for keyword in dependency_keywords:
            if keyword in text:
                # Extract potential dependency descriptions
                idx = text.find(keyword)
                potential = text[idx : idx + 100].split('.')[0]
                if potential:
                    dependencies.append(potential.strip())

        return dependencies[:3]  # Limit to 3 dependencies

    @staticmethod
    def _extract_skills(text: str) -> List[str]:
        """Extract required skills from task description."""
        skill_keywords = {
            "Python": ["python", "py", "django", "flask"],
            "JavaScript": ["javascript", "js", "react", "node", "typescript"],
            "DevOps": ["docker", "kubernetes", "deploy", "infra", "aws"],
            "Data": ["sql", "database", "analytics", "data"],
            "Testing": ["test", "qa", "pytest", "unittest"],
        }

        found_skills = []
        for skill, keywords in skill_keywords.items():
            if any(keyword in text for keyword in keywords):
                found_skills.append(skill)

        return found_skills[:5]

    @staticmethod
    def _generate_subtasks(task_text: str, complexity: TaskComplexity) -> List[str]:
        """Generate subtasks based on complexity and content."""
        subtasks = []

        if complexity == TaskComplexity.TRIVIAL:
            subtasks = ["Complete task"]
        elif complexity == TaskComplexity.SIMPLE:
            subtasks = ["Understand requirements", "Execute", "Verify"]
        elif complexity == TaskComplexity.MODERATE:
            subtasks = [
                "Analyze requirements",
                "Design solution",
                "Implement",
                "Test",
                "Review",
            ]
        elif complexity in [TaskComplexity.COMPLEX, TaskComplexity.CRITICAL]:
            subtasks = [
                "Requirements gathering",
                "Architecture design",
                "Implementation planning",
                "Development",
                "Unit testing",
                "Integration testing",
                "Code review",
                "Deployment preparation",
            ]

        return subtasks

    @staticmethod
    def _calculate_priority(category: TaskCategory, complexity: TaskComplexity, text: str) -> int:
        """Calculate task priority (1-5)."""
        priority = 3  # Default

        # Category influence
        if category == TaskCategory.URGENT:
            priority = 5
        elif category in [TaskCategory.DEPLOYMENT, TaskCategory.TESTING]:
            priority = 4

        # Complexity influence
        if complexity == TaskComplexity.CRITICAL:
            priority = 5
        elif complexity == TaskComplexity.COMPLEX:
            priority = 4

        # Text keywords influence
        if any(word in text for word in ["asap", "urgent", "blocking"]):
            priority = 5
        elif any(word in text for word in ["soon", "important"]):
            priority = min(4, priority + 1)

        return min(5, max(1, priority))

    @staticmethod
    def _calculate_confidence(text: str) -> float:
        """Calculate confidence score of analysis."""
        confidence = 0.7  # Base confidence

        # Increase confidence with clear keywords
        keywords_found = sum(
            1
            for keywords_list in NLPEngine.CATEGORY_KEYWORDS.values()
            for keyword in keywords_list
            if keyword in text
        )
        confidence += (keywords_found * 0.05)

        # Increase with text length
        confidence += min(0.2, len(text.split()) * 0.01)

        return min(0.99, confidence)
