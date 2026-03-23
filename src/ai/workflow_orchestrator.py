"""Autonomous Workflow Orchestrator - Multi-agent task coordination."""

import uuid
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from ..utils.logger import logger


class AgentStatus(str, Enum):
    """Status of autonomous agents."""
    IDLE = "idle"
    WORKING = "working"
    PAUSED = "paused"
    FAILED = "failed"
    COMPLETED = "completed"


class WorkflowStatus(str, Enum):
    """Workflow execution status."""
    QUEUED = "queued"
    EXECUTING = "executing"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class Agent:
    """Autonomous agent for task execution."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    status: AgentStatus = AgentStatus.IDLE
    current_task_id: Optional[str] = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    success_rate: float = 1.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_heartbeat: datetime = field(default_factory=datetime.utcnow)

    def is_alive(self) -> bool:
        """Check if agent is alive based on heartbeat."""
        from datetime import timedelta
        return (datetime.utcnow() - self.last_heartbeat).seconds < 300  # 5 min timeout


@dataclass
class WorkflowNode:
    """Node representing a task in workflow graph."""
    task_id: str
    task_name: str
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"
    retry_count: int = 0
    max_retries: int = 3
    assigned_agent_id: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class WorkflowOrchestrator:
    """Autonomous multi-agent workflow orchestrator."""

    def __init__(self):
        """Initialize orchestrator."""
        self.agents: Dict[str, Agent] = {}
        self.workflows: Dict[str, Dict] = {}
        self.task_graph: Dict[str, WorkflowNode] = {}

    def create_agent(self, name: str, capability: str = "general") -> Agent:
        """Create and register a new autonomous agent."""
        agent = Agent(name=f"{name}-{capability}")
        self.agents[agent.id] = agent
        logger.info(f"Agent created: {agent.name} ({agent.id})")
        return agent

    def orchestrate_workflow(self, task_graph: Dict[str, List[str]]) -> str:
        """Orchestrate workflow execution with dependency resolution."""
        workflow_id = str(uuid.uuid4())

        # Build workflow nodes
        nodes = {}
        for task_id, dependencies in task_graph.items():
            nodes[task_id] = WorkflowNode(
                task_id=task_id,
                task_name=f"Task-{task_id}",
                dependencies=dependencies,
            )

        self.workflows[workflow_id] = {
            "id": workflow_id,
            "status": WorkflowStatus.QUEUED,
            "nodes": nodes,
            "created_at": datetime.utcnow(),
            "started_at": None,
        }

        logger.info(f"Workflow created: {workflow_id} with {len(nodes)} tasks")
        return workflow_id

    def execute_workflow(self, workflow_id: str) -> Dict:
        """Execute workflow with intelligent task dispatch."""
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}

        workflow = self.workflows[workflow_id]
        workflow["status"] = WorkflowStatus.EXECUTING
        workflow["started_at"] = datetime.utcnow()

        # Get available agents
        available_agents = [
            agent for agent in self.agents.values() if agent.is_alive() and agent.status == AgentStatus.IDLE
        ]

        if not available_agents:
            logger.warning(f"No available agents for workflow {workflow_id}")
            return {"error": "No available agents"}

        # Topological sort for task execution
        execution_order = self._topological_sort(workflow["nodes"])

        results = []
        for task_id in execution_order:
            # Select best agent based on success rate
            agent = self._select_best_agent(available_agents)

            # Assign and execute task
            result = self._execute_task(task_id, agent, workflow["nodes"])
            results.append(result)

            if result["status"] == "failed" and workflow["nodes"][task_id].retry_count >= 3:
                workflow["status"] = WorkflowStatus.FAILED
                logger.error(f"Workflow {workflow_id} failed at task {task_id}")
                return {"status": "failed", "failed_task": task_id}

        workflow["status"] = WorkflowStatus.COMPLETED
        logger.info(f"Workflow {workflow_id} completed successfully")
        return {"status": "completed", "workflow_id": workflow_id, "results": results}

    def _topological_sort(self, nodes: Dict[str, WorkflowNode]) -> List[str]:
        """Topologically sort tasks for optimal execution."""
        visited = set()
        order = []

        def visit(node_id: str):
            if node_id in visited:
                return
            visited.add(node_id)
            for dep in nodes[node_id].dependencies:
                visit(dep)
            order.append(node_id)

        for node_id in nodes:
            visit(node_id)

        return order

    def _select_best_agent(self, agents: List[Agent]) -> Agent:
        """Select best agent based on success rate and current load."""
        return max(agents, key=lambda a: a.success_rate)

    def _execute_task(self, task_id: str, agent: Agent, nodes: Dict) -> Dict:
        """Execute task on agent with error handling."""
        node = nodes[task_id]
        node.assigned_agent_id = agent.id
        node.started_at = datetime.utcnow()
        agent.status = AgentStatus.WORKING
        agent.current_task_id = task_id

        try:
            # Simulate task execution
            logger.info(f"Agent {agent.name} executing task {task_id}")
            # In production, this would call actual task execution
            result = {"status": "success", "task_id": task_id, "agent_id": agent.id}

            node.status = "completed"
            node.result = str(result)
            agent.tasks_completed += 1
            agent.status = AgentStatus.IDLE

            return result

        except Exception as e:
            logger.error(f"Task {task_id} failed: {str(e)}")
            node.error = str(e)
            node.retry_count += 1
            agent.tasks_failed += 1
            agent.success_rate = agent.tasks_completed / (
                agent.tasks_completed + agent.tasks_failed
            )

            return {"status": "failed", "task_id": task_id, "error": str(e)}

    def get_workflow_status(self, workflow_id: str) -> Dict:
        """Get current workflow status and progress."""
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}

        workflow = self.workflows[workflow_id]
        nodes = workflow["nodes"]

        completed = sum(1 for node in nodes.values() if node.status == "completed")
        failed = sum(1 for node in nodes.values() if node.status == "failed")
        total = len(nodes)

        return {
            "workflow_id": workflow_id,
            "status": workflow["status"].value,
            "progress": f"{completed}/{total}",
            "completion_rate": (completed / total * 100) if total > 0 else 0,
            "failed_tasks": failed,
            "agents_active": sum(1 for a in self.agents.values() if a.status == AgentStatus.WORKING),
        }
