"""Tests for AI and advanced features."""

import pytest
from src.ai.nlp_engine import NLPEngine, TaskComplexity, TaskCategory
from src.ai.workflow_orchestrator import WorkflowOrchestrator
from src.ai.code_generator import CodeGenerator, CodeLanguage, CodeTemplateType
from src.ai.predictive_analytics import PredictiveAnalytics
from src.ai.knowledge_base import KnowledgeBase
from src.ai.self_healing import SelfHealingSystem
from src.ai.collaboration_hub import CollaborationHub


class TestNLPEngine:
    """Tests for NLP Engine."""

    def test_task_analysis(self):
        """Test task analysis."""
        task_text = "Build a Python REST API with database integration"
        result = NLPEngine.analyze_task(task_text)

        assert result.extracted_title
        assert result.category == TaskCategory.DEVELOPMENT
        assert result.complexity == TaskComplexity.MODERATE
        assert result.estimated_duration_minutes > 0
        assert result.confidence_score > 0

    def test_category_detection(self):
        """Test category detection."""
        urgent_task = "ASAP: Fix critical bug in production"
        result = NLPEngine.analyze_task(urgent_task)
        assert result.category == TaskCategory.URGENT
        assert result.suggested_priority == 5


class TestWorkflowOrchestrator:
    """Tests for Workflow Orchestrator."""

    def test_agent_creation(self):
        """Test agent creation."""
        orchestrator = WorkflowOrchestrator()
        agent = orchestrator.create_agent("worker", "python")

        assert agent.name == "worker-python"
        assert agent.id in orchestrator.agents

    def test_workflow_orchestration(self):
        """Test workflow orchestration."""
        orchestrator = WorkflowOrchestrator()
        task_graph = {
            "task1": [],
            "task2": ["task1"],
            "task3": ["task1", "task2"],
        }

        workflow_id = orchestrator.orchestrate_workflow(task_graph)
        assert workflow_id
        assert workflow_id in orchestrator.workflows


class TestCodeGenerator:
    """Tests for Code Generator."""

    def test_code_generation(self):
        """Test code generation."""
        task = "Create a function to validate email addresses"
        code = CodeGenerator.generate_code(
            task,
            CodeLanguage.PYTHON,
            CodeTemplateType.FUNCTION,
        )

        assert code.code
        assert code.language == CodeLanguage.PYTHON
        assert code.quality_score > 0
        assert len(code.test_cases) > 0


class TestPredictiveAnalytics:
    """Tests for Predictive Analytics."""

    def test_task_time_prediction(self):
        """Test task completion time prediction."""
        analytics = PredictiveAnalytics()
        task_data = {"complexity": "moderate", "estimated_duration": 120}

        prediction = analytics.predict_task_completion_time(task_data)
        assert prediction.predicted_value > 0
        assert prediction.confidence > 0
        assert prediction.lower_bound <= prediction.predicted_value
        assert prediction.upper_bound >= prediction.predicted_value

    def test_anomaly_detection(self):
        """Test anomaly detection."""
        analytics = PredictiveAnalytics()
        metrics = [100, 105, 102, 500, 103, 101]  # 500 is anomaly

        anomalies = analytics.detect_anomalies(metrics)
        assert len(anomalies) > 0
        assert any(a["value"] == 500 for a in anomalies)


class TestKnowledgeBase:
    """Tests for Knowledge Base."""

    def test_add_knowledge(self):
        """Test adding knowledge."""
        kb = KnowledgeBase()
        item_id = kb.add_knowledge(
            "Python Best Practices",
            "Always use type hints and docstrings",
            "python",
            ["best-practices", "python"],
        )

        assert item_id
        assert item_id in kb.items

    def test_semantic_search(self):
        """Test semantic search."""
        kb = KnowledgeBase()
        kb.add_knowledge(
            "API Design",
            "REST API best practices",
            "api",
            ["api", "rest"],
        )

        results = kb.semantic_search("REST API")
        assert len(results) > 0


class TestSelfHealingSystem:
    """Tests for Self-Healing System."""

    def test_system_diagnosis(self):
        """Test system diagnosis."""
        healer = SelfHealingSystem()
        diagnostics = healer.diagnose_system()

        assert "overall_health" in diagnostics
        assert "component_health" in diagnostics
        assert "recommendations" in diagnostics

    def test_auto_recovery(self):
        """Test auto-recovery."""
        healer = SelfHealingSystem()
        error = {"type": "timeout", "severity": "medium"}

        result = healer.auto_recover(error)
        assert result["status"] in ["recovered", "failed"]


class TestCollaborationHub:
    """Tests for Collaboration Hub."""

    def test_session_creation(self):
        """Test collaboration session creation."""
        hub = CollaborationHub()
        session_id = hub.create_session("task1", "user1")

        assert session_id
        assert session_id in hub.sessions

    def test_multi_user_collaboration(self):
        """Test multi-user collaboration."""
        hub = CollaborationHub()
        session_id = hub.create_session("task1", "user1")

        # User 2 joins
        assert hub.join_session(session_id, "user2")

        # Apply changes
        change = {"field": "title", "value": "Updated Title"}
        result = hub.apply_change(session_id, "user1", change)
        assert result["status"] in ["applied", "merged"]
