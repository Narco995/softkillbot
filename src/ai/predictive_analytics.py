"""Predictive Analytics & Forecasting Engine."""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from statistics import mean, stdev

from ..utils.logger import logger


@dataclass
class Prediction:
    """Prediction result with confidence interval."""
    metric: str
    predicted_value: float
    confidence: float
    lower_bound: float
    upper_bound: float
    timestamp: datetime


class PredictiveAnalytics:
    """Predictive analytics engine for task and resource forecasting."""

    def __init__(self):
        """Initialize analytics engine."""
        self.historical_data: Dict[str, List[float]] = {}
        self.trends: Dict[str, float] = {}

    def predict_task_completion_time(self, task_data: Dict) -> Prediction:
        """Predict task completion time using historical data."""
        try:
            # Extract historical task times
            similar_tasks = self._find_similar_tasks(task_data)
            historical_times = [t["duration"] for t in similar_tasks]

            if not historical_times:
                # Use default if no history
                return Prediction(
                    metric="task_completion_time",
                    predicted_value=task_data.get("estimated_duration", 120),
                    confidence=0.5,
                    lower_bound=task_data.get("estimated_duration", 120) * 0.7,
                    upper_bound=task_data.get("estimated_duration", 120) * 1.3,
                    timestamp=datetime.utcnow(),
                )

            # Calculate statistics
            mean_time = mean(historical_times)
            std_dev = stdev(historical_times) if len(historical_times) > 1 else 0
            confidence = min(0.95, 0.5 + (len(similar_tasks) * 0.05))

            return Prediction(
                metric="task_completion_time",
                predicted_value=mean_time,
                confidence=confidence,
                lower_bound=max(0, mean_time - (2 * std_dev)),
                upper_bound=mean_time + (2 * std_dev),
                timestamp=datetime.utcnow(),
            )
        except Exception as e:
            logger.error(f"Error predicting task time: {str(e)}")
            raise

    def predict_resource_utilization(self, current_load: float, history: List[float]) -> Prediction:
        """Predict future resource utilization."""
        try:
            # Simple linear regression based on history
            if len(history) < 2:
                return Prediction(
                    metric="resource_utilization",
                    predicted_value=current_load,
                    confidence=0.5,
                    lower_bound=current_load * 0.8,
                    upper_bound=min(100, current_load * 1.2),
                    timestamp=datetime.utcnow(),
                )

            # Calculate trend
            trend = (history[-1] - history[0]) / len(history)
            predicted_value = current_load + (trend * 1)
            predicted_value = max(0, min(100, predicted_value))

            # Calculate confidence based on variance
            variance = self._calculate_variance(history)
            confidence = max(0.4, 1.0 - (variance / 100))

            return Prediction(
                metric="resource_utilization",
                predicted_value=predicted_value,
                confidence=confidence,
                lower_bound=max(0, predicted_value - 10),
                upper_bound=min(100, predicted_value + 10),
                timestamp=datetime.utcnow(),
            )
        except Exception as e:
            logger.error(f"Error predicting resource utilization: {str(e)}")
            raise

    def identify_bottlenecks(self, workflow_data: Dict) -> List[Dict]:
        """Identify workflow bottlenecks using analysis."""
        bottlenecks = []

        try:
            tasks = workflow_data.get("tasks", [])

            for task in tasks:
                # Calculate task criticality
                duration = task.get("duration", 0)
                dependents = len(task.get("dependents", []))
                variance = task.get("variance", 0)

                criticality_score = (duration * 0.5) + (dependents * 0.3) + (variance * 0.2)

                if criticality_score > 50:
                    bottlenecks.append(
                        {
                            "task_id": task.get("id"),
                            "criticality_score": criticality_score,
                            "reason": self._determine_bottleneck_reason(task),
                            "recommendation": self._suggest_optimization(task),
                        }
                    )

            logger.info(f"Identified {len(bottlenecks)} bottlenecks")
            return sorted(bottlenecks, key=lambda x: x["criticality_score"], reverse=True)[:5]
        except Exception as e:
            logger.error(f"Error identifying bottlenecks: {str(e)}")
            return []

    def detect_anomalies(self, metrics: List[float], threshold: float = 2.0) -> List[Dict]:
        """Detect anomalies in workflow metrics using statistical analysis."""
        anomalies = []

        try:
            if len(metrics) < 3:
                return anomalies

            mean_val = mean(metrics)
            std_val = stdev(metrics)

            for i, metric in enumerate(metrics):
                # Z-score based anomaly detection
                z_score = abs((metric - mean_val) / std_val) if std_val > 0 else 0

                if z_score > threshold:
                    anomalies.append(
                        {
                            "index": i,
                            "value": metric,
                            "z_score": z_score,
                            "severity": "high" if z_score > 3 else "medium",
                        }
                    )

            if anomalies:
                logger.warning(f"Detected {len(anomalies)} anomalies in metrics")

            return anomalies
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return []

    def forecast_team_productivity(self, team_history: List[Dict]) -> Dict:
        """Forecast team productivity trends."""
        try:
            if not team_history:
                return {"forecast": "insufficient_data"}

            # Extract productivity metrics
            productivity_scores = [h.get("productivity", 0.5) for h in team_history]
            timestamps = [h.get("timestamp", datetime.utcnow()) for h in team_history]

            # Calculate trend
            if len(productivity_scores) >= 2:
                trend = (
                    (productivity_scores[-1] - productivity_scores[0]) / len(productivity_scores)
                )
            else:
                trend = 0

            avg_productivity = mean(productivity_scores)

            return {
                "current_productivity": productivity_scores[-1] if productivity_scores else 0,
                "average_productivity": avg_productivity,
                "trend": "improving" if trend > 0 else "declining" if trend < 0 else "stable",
                "trend_strength": abs(trend),
                "forecast_next_week": (
                    avg_productivity + (trend * 7) if productivity_scores else avg_productivity
                ),
            }
        except Exception as e:
            logger.error(f"Error forecasting productivity: {str(e)}")
            return {"error": str(e)}

    def _find_similar_tasks(self, task_data: Dict) -> List[Dict]:
        """Find similar historical tasks."""
        # In production, this would query a database
        return [
            {"duration": 120},
            {"duration": 135},
            {"duration": 128},
        ]

    def _calculate_variance(self, data: List[float]) -> float:
        """Calculate variance of data."""
        if len(data) < 2:
            return 0
        mean_val = mean(data)
        return mean((x - mean_val) ** 2 for x in data) ** 0.5

    def _determine_bottleneck_reason(self, task: Dict) -> str:
        """Determine reason for bottleneck."""
        duration = task.get("duration", 0)
        dependents = len(task.get("dependents", []))

        if duration > 300 and dependents > 3:
            return "Long-running task with many dependents"
        elif dependents > 5:
            return "High critical path node"
        elif duration > 400:
            return "Excessive task duration"
        return "Complex task dependencies"

    def _suggest_optimization(self, task: Dict) -> str:
        """Suggest optimization for bottleneck."""
        reason = self._determine_bottleneck_reason(task)

        if "duration" in reason:
            return "Consider parallelizing subtasks or optimizing implementation"
        elif "dependents" in reason:
            return "Refactor task dependencies or implement early execution"
        else:
            return "Review task structure and dependencies"
