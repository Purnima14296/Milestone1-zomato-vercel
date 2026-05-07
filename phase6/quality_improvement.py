"""
Phase 6 Quality Improvement: Automated quality analysis and improvement recommendations.

This module provides intelligent analysis of system performance metrics and
generates actionable recommendations for continuous improvement of the
restaurant recommendation system.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import statistics
from collections import defaultdict

from metrics import MetricsCollector, SystemMetrics
from golden_tests import GoldenTestSuite
from monitoring import MonitoringSystem


class ImprovementPriority(Enum):
    """Enumeration of improvement priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ImprovementCategory(Enum):
    """Enumeration of improvement categories."""
    PERFORMANCE = "performance"
    QUALITY = "quality"
    COST = "cost"
    DIVERSITY = "diversity"
    CONSTRAINTS = "constraints"
    MONITORING = "monitoring"
    USER_EXPERIENCE = "user_experience"


@dataclass
class ImprovementRecommendation:
    """Represents a single improvement recommendation."""
    id: str
    title: str
    description: str
    category: ImprovementCategory
    priority: ImprovementPriority
    estimated_impact: float  # 0-1
    estimated_effort: float   # 0-1
    action_items: List[str]
    success_metrics: List[str]
    dependencies: List[str]
    timeline: str


@dataclass
class QualityInsight:
    """Represents a quality insight from data analysis."""
    insight_type: str
    description: str
    evidence: Dict[str, Any]
    confidence: float  # 0-1
    actionable: bool


class QualityImprovementEngine:
    """
    Intelligent quality improvement analysis and recommendation engine.
    
    Analyzes system metrics, identifies improvement opportunities, and
    generates actionable recommendations for continuous system enhancement.
    """
    
    def __init__(self, metrics_collector: MetricsCollector, monitoring_system: MonitoringSystem):
        self.metrics_collector = metrics_collector
        self.monitoring_system = monitoring_system
        self.golden_test_suite = GoldenTestSuite()
        
        # Improvement history
        self.recommendations_history: List[ImprovementRecommendation] = []
        self.implemented_changes: List[Dict[str, Any]] = []
        
        # Thresholds and baselines
        self.quality_thresholds = {
            "min_quality_score": 0.8,
            "min_constraint_satisfaction": 0.9,
            "min_diversity_score": 0.7,
            "max_response_time_p95": 2.0,
            "max_error_rate": 0.05,
            "max_cost_per_recommendation": 0.5
        }
    
    def analyze_system_quality(self, hours: int = 24) -> Dict[str, Any]:
        """
        Perform comprehensive system quality analysis.
        
        Args:
            hours: Time period for analysis
            
        Returns:
            Quality analysis results
        """
        # Get recent metrics
        recent_metrics = self.metrics_collector.metrics_history[-100:] if self.metrics_collector.metrics_history else []
        aggregated_metrics = self.metrics_collector.get_aggregated_metrics(100)
        monitoring_summary = self.monitoring_system.get_metrics_summary(hours)
        
        # Analyze different quality dimensions
        quality_analysis = {
            "timestamp": time.time(),
            "analysis_period_hours": hours,
            "overall_quality_score": self._calculate_overall_quality_score(recent_metrics),
            "dimension_analysis": {
                "constraint_satisfaction": self._analyze_constraint_satisfaction(recent_metrics),
                "diversity": self._analyze_diversity(recent_metrics),
                "performance": self._analyze_performance(monitoring_summary),
                "cost_efficiency": self._analyze_cost_efficiency(recent_metrics),
                "user_satisfaction": self._analyze_user_satisfaction(recent_metrics)
            },
            "trend_analysis": self._analyze_quality_trends(recent_metrics),
            "anomaly_detection": self._detect_quality_anomalies(recent_metrics),
            "insights": self._generate_quality_insights(recent_metrics, aggregated_metrics)
        }
        
        return quality_analysis
    
    def generate_improvement_recommendations(self, hours: int = 24) -> List[ImprovementRecommendation]:
        """
        Generate comprehensive improvement recommendations.
        
        Args:
            hours: Time period for analysis
            
        Returns:
            List of improvement recommendations
        """
        quality_analysis = self.analyze_system_quality(hours)
        recommendations = []
        
        # Generate recommendations based on different quality dimensions
        recommendations.extend(self._generate_constraint_recommendations(quality_analysis))
        recommendations.extend(self._generate_diversity_recommendations(quality_analysis))
        recommendations.extend(self._generate_performance_recommendations(quality_analysis))
        recommendations.extend(self._generate_cost_recommendations(quality_analysis))
        recommendations.extend(self._generate_quality_recommendations(quality_analysis))
        recommendations.extend(self._generate_monitoring_recommendations(quality_analysis))
        
        # Sort by priority and impact
        recommendations.sort(key=lambda x: (x.priority.value, -x.estimated_impact))
        
        # Store recommendations history
        self.recommendations_history.extend(recommendations)
        
        return recommendations
    
    def _calculate_overall_quality_score(self, metrics: List[SystemMetrics]) -> float:
        """Calculate overall quality score from metrics."""
        if not metrics:
            return 0.0
        
        quality_scores = []
        for metric in metrics:
            # Weight different quality dimensions
            constraint_weight = 0.3
            diversity_weight = 0.2
            performance_weight = 0.3
            cost_weight = 0.2
            
            # Normalize scores (0-1)
            constraint_score = metric.constraint_metrics.overall_satisfaction
            diversity_score = metric.diversity_metrics.overall_diversity
            performance_score = max(0, 1 - (metric.latency_metrics.total_latency / 5.0))  # 5s max
            cost_score = max(0, 1 - (metric.cost_metrics.cost_per_recommendation / 1.0))  # $1 max
            
            overall_score = (
                constraint_score * constraint_weight +
                diversity_score * diversity_weight +
                performance_score * performance_weight +
                cost_score * cost_weight
            )
            
            quality_scores.append(overall_score)
        
        return statistics.mean(quality_scores) if quality_scores else 0.0
    
    def _analyze_constraint_satisfaction(self, metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Analyze constraint satisfaction patterns."""
        if not metrics:
            return {"status": "no_data"}
        
        satisfaction_scores = [m.constraint_metrics.overall_satisfaction for m in metrics]
        violated_constraints = defaultdict(int)
        
        for metric in metrics:
            for violated in metric.constraint_metrics.violated_constraints:
                violated_constraints[violated] += 1
        
        return {
            "avg_satisfaction": statistics.mean(satisfaction_scores),
            "satisfaction_trend": "improving" if len(satisfaction_scores) > 1 and satisfaction_scores[-1] > satisfaction_scores[0] else "stable",
            "most_violated_constraint": max(violated_constraints.items(), key=lambda x: x[1])[0] if violated_constraints else None,
            "total_violations": sum(violated_constraints.values()),
            "violation_rate": sum(violated_constraints.values()) / len(metrics)
        }
    
    def _analyze_diversity(self, metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Analyze diversity metrics."""
        if not metrics:
            return {"status": "no_data"}
        
        diversity_scores = [m.diversity_metrics.overall_diversity for m in metrics]
        cuisine_diversity = [m.diversity_metrics.cuisine_diversity for m in metrics]
        price_diversity = [m.diversity_metrics.price_diversity for m in metrics]
        
        return {
            "avg_diversity": statistics.mean(diversity_scores),
            "diversity_trend": "improving" if len(diversity_scores) > 1 and diversity_scores[-1] > diversity_scores[0] else "stable",
            "cuisine_diversity": statistics.mean(cuisine_diversity),
            "price_diversity": statistics.mean(price_diversity),
            "diversity_consistency": 1 - (statistics.stdev(diversity_scores) if len(diversity_scores) > 1 else 0)
        }
    
    def _analyze_performance(self, monitoring_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance metrics."""
        if not monitoring_summary:
            return {"status": "no_data"}
        
        response_time = monitoring_summary.get("response_time_p95", {})
        error_rate = monitoring_summary.get("error_rate", {})
        throughput = monitoring_summary.get("throughput", {})
        
        return {
            "avg_response_time": response_time.get("mean", 0),
            "response_time_trend": "stable",
            "avg_error_rate": error_rate.get("mean", 0),
            "error_rate_trend": "stable",
            "avg_throughput": throughput.get("mean", 0),
            "performance_score": self._calculate_performance_score(monitoring_summary)
        }
    
    def _analyze_cost_efficiency(self, metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Analyze cost efficiency."""
        if not metrics:
            return {"status": "no_data"}
        
        costs = [m.cost_metrics.total_cost for m in metrics]
        costs_per_rec = [m.cost_metrics.cost_per_recommendation for m in metrics]
        llm_costs = [m.cost_metrics.llm_cost for m in metrics]
        
        return {
            "avg_total_cost": statistics.mean(costs),
            "avg_cost_per_recommendation": statistics.mean(costs_per_rec),
            "avg_llm_cost": statistics.mean(llm_costs),
            "cost_trend": "stable",
            "cost_efficiency_score": self._calculate_cost_efficiency_score(metrics)
        }
    
    def _analyze_user_satisfaction(self, metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Analyze user satisfaction metrics."""
        # This would include user feedback, click-through rates, etc.
        # For now, return placeholder data
        return {
            "avg_user_rating": 4.2,
            "click_through_rate": 0.15,
            "user_retention": 0.78,
            "feedback_sentiment": 0.65
        }
    
    def _analyze_quality_trends(self, metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Analyze quality trends over time."""
        if len(metrics) < 10:
            return {"status": "insufficient_data"}
        
        # Calculate trends for different metrics
        quality_scores = [self._calculate_overall_quality_score([m]) for m in metrics]
        
        # Simple trend analysis
        recent_scores = quality_scores[-5:]
        earlier_scores = quality_scores[-10:-5]
        
        recent_avg = statistics.mean(recent_scores)
        earlier_avg = statistics.mean(earlier_scores)
        
        trend = "improving" if recent_avg > earlier_avg else "declining" if recent_avg < earlier_avg else "stable"
        
        return {
            "overall_trend": trend,
            "trend_magnitude": abs(recent_avg - earlier_avg),
            "trend_confidence": 0.8 if abs(recent_avg - earlier_avg) > 0.05 else 0.5
        }
    
    def _detect_quality_anomalies(self, metrics: List[SystemMetrics]) -> List[Dict[str, Any]]:
        """Detect quality anomalies in metrics."""
        anomalies = []
        
        if len(metrics) < 20:
            return anomalies
        
        # Check for anomalies in different dimensions
        quality_scores = [self._calculate_overall_quality_score([m]) for m in metrics]
        
        # Simple statistical anomaly detection
        mean_score = statistics.mean(quality_scores)
        std_score = statistics.stdev(quality_scores)
        
        for i, score in enumerate(quality_scores):
            if abs(score - mean_score) > 2 * std_score:  # 2 sigma threshold
                anomalies.append({
                    "timestamp": metrics[i].timestamp,
                    "type": "quality_score_anomaly",
                    "value": score,
                    "expected_range": [mean_score - 2*std_score, mean_score + 2*std_score],
                    "severity": "high" if abs(score - mean_score) > 3 * std_score else "medium"
                })
        
        return anomalies
    
    def _generate_quality_insights(self, metrics: List[SystemMetrics], aggregated: Dict[str, Any]) -> List[QualityInsight]:
        """Generate actionable quality insights."""
        insights = []
        
        if not metrics:
            return insights
        
        # Constraint satisfaction insight
        constraint_sat = aggregated.get("avg_constraint_satisfaction", 0)
        if constraint_sat < 0.85:
            insights.append(QualityInsight(
                insight_type="constraint_satisfaction",
                description=f"Constraint satisfaction is below optimal at {constraint_sat:.2%}",
                evidence={"avg_satisfaction": constraint_sat, "threshold": 0.85},
                confidence=0.9,
                actionable=True
            ))
        
        # Diversity insight
        diversity_score = aggregated.get("avg_diversity", 0)
        if diversity_score < 0.7:
            insights.append(QualityInsight(
                insight_type="diversity_deficit",
                description=f"Recommendation diversity is low at {diversity:.2%}",
                evidence={"avg_diversity": diversity_score, "threshold": 0.7},
                confidence=0.8,
                actionable=True
            ))
        
        # Performance insight
        avg_latency = aggregated.get("avg_latency", 0)
        if avg_latency > 1.5:
            insights.append(QualityInsight(
                insight_type="performance_degradation",
                description=f"Average latency is high at {avg_latency:.2f}s",
                evidence={"avg_latency": avg_latency, "threshold": 1.5},
                confidence=0.85,
                actionable=True
            ))
        
        return insights
    
    def _generate_constraint_recommendations(self, analysis: Dict[str, Any]) -> List[ImprovementRecommendation]:
        """Generate constraint-related improvement recommendations."""
        recommendations = []
        constraint_analysis = analysis["dimension_analysis"]["constraint_satisfaction"]
        
        if constraint_analysis.get("avg_satisfaction", 1.0) < 0.9:
            most_violated = constraint_analysis.get("most_violated_constraint")
            
            recommendations.append(ImprovementRecommendation(
                id="constraint_improvement_1",
                title=f"Improve {most_violated} constraint satisfaction",
                description=f"Constraint satisfaction for {most_violated} is below optimal. Review and improve constraint validation logic.",
                category=ImprovementCategory.CONSTRAINTS,
                priority=ImprovementPriority.HIGH,
                estimated_impact=0.8,
                estimated_effort=0.6,
                action_items=[
                    f"Analyze {most_violated} constraint violation patterns",
                    "Improve constraint matching algorithms",
                    "Update constraint validation logic",
                    "Add better error handling for constraint violations"
                ],
                success_metrics=[
                    "Increase constraint satisfaction rate to >95%",
                    "Reduce constraint violations by >50%",
                    "Improve user feedback on constraint handling"
                ],
                dependencies=["constraint_validation_team", "data_quality_team"],
                timeline="2-4 weeks"
            ))
        
        return recommendations
    
    def _generate_diversity_recommendations(self, analysis: Dict[str, Any]) -> List[ImprovementRecommendation]:
        """Generate diversity-related improvement recommendations."""
        recommendations = []
        diversity_analysis = analysis["dimension_analysis"]["diversity"]
        
        if diversity_analysis.get("avg_diversity", 1.0) < 0.7:
            recommendations.append(ImprovementRecommendation(
                id="diversity_improvement_1",
                title="Enhance recommendation diversity",
                description="Recommendation diversity is below optimal. Implement diversity-aware ranking algorithms.",
                category=ImprovementCategory.DIVERSITY,
                priority=ImprovementPriority.MEDIUM,
                estimated_impact=0.6,
                estimated_effort=0.7,
                action_items=[
                    "Implement diversity-aware ranking algorithms",
                    "Add explicit diversity objectives in scoring",
                    "Introduce serendipity factors in recommendations",
                    "Monitor diversity metrics continuously"
                ],
                success_metrics=[
                    "Increase overall diversity score to >80%",
                    "Improve cuisine diversity by >30%",
                    "Maintain quality while increasing diversity"
                ],
                dependencies=["ranking_algorithm_team", "ml_team"],
                timeline="3-6 weeks"
            ))
        
        return recommendations
    
    def _generate_performance_recommendations(self, analysis: Dict[str, Any]) -> List[ImprovementRecommendation]:
        """Generate performance-related improvement recommendations."""
        recommendations = []
        performance_analysis = analysis["dimension_analysis"]["performance"]
        
        if performance_analysis.get("avg_response_time", 0) > 2.0:
            recommendations.append(ImprovementRecommendation(
                id="performance_improvement_1",
                title="Optimize system response time",
                description=f"Average response time of {performance_analysis.get('avg_response_time', 0):.2f}s is above optimal.",
                category=ImprovementCategory.PERFORMANCE,
                priority=ImprovementPriority.HIGH,
                estimated_impact=0.9,
                estimated_effort=0.8,
                action_items=[
                    "Profile system bottlenecks",
                    "Optimize database queries",
                    "Implement response caching",
                    "Add connection pooling",
                    "Optimize LLM API calls"
                ],
                success_metrics=[
                    "Reduce P95 response time to <2s",
                    "Improve throughput by >20%",
                    "Maintain error rate <1%"
                ],
                dependencies=["performance_team", "backend_team"],
                timeline="4-6 weeks"
            ))
        
        return recommendations
    
    def _generate_cost_recommendations(self, analysis: Dict[str, Any]) -> List[ImprovementRecommendation]:
        """Generate cost-related improvement recommendations."""
        recommendations = []
        cost_analysis = analysis["dimension_analysis"]["cost_efficiency"]
        
        if cost_analysis.get("avg_cost_per_recommendation", 0) > 0.5:
            recommendations.append(ImprovementRecommendation(
                id="cost_optimization_1",
                title="Optimize recommendation costs",
                description=f"Average cost per recommendation of ${cost_analysis.get('avg_cost_per_recommendation', 0):.3f} is above optimal.",
                category=ImprovementCategory.COST,
                priority=ImprovementPriority.MEDIUM,
                estimated_impact=0.7,
                estimated_effort=0.5,
                action_items=[
                    "Optimize LLM prompt length",
                    "Implement response caching",
                    "Review LLM model selection",
                    "Add cost monitoring and alerts",
                    "Implement cost controls"
                ],
                success_metrics=[
                    "Reduce cost per recommendation by >30%",
                    "Maintain quality while reducing costs",
                    "Implement real-time cost monitoring"
                ],
                dependencies=["ml_team", "finance_team"],
                timeline="2-3 weeks"
            ))
        
        return recommendations
    
    def _generate_quality_recommendations(self, analysis: Dict[str, Any]) -> List[ImprovementRecommendation]:
        """Generate general quality improvement recommendations."""
        recommendations = []
        
        overall_score = analysis.get("overall_quality_score", 0)
        if overall_score < 0.8:
            recommendations.append(ImprovementRecommendation(
                id="quality_improvement_1",
                title="Improve overall recommendation quality",
                description=f"Overall quality score of {overall_score:.2%} is below optimal.",
                category=ImprovementCategory.QUALITY,
                priority=ImprovementPriority.HIGH,
                estimated_impact=0.9,
                estimated_effort=0.8,
                action_items=[
                    "Review and improve LLM prompts",
                    "Enhance explanation quality",
                    "Improve ranking algorithms",
                    "Add quality validation checks",
                    "Implement A/B testing for quality improvements"
                ],
                success_metrics=[
                    "Increase overall quality score to >85%",
                    "Improve user satisfaction scores",
                    "Reduce quality-related complaints"
                ],
                dependencies=["ml_team", "product_team"],
                timeline="4-8 weeks"
            ))
        
        return recommendations
    
    def _generate_monitoring_recommendations(self, analysis: Dict[str, Any]) -> List[ImprovementRecommendation]:
        """Generate monitoring-related improvement recommendations."""
        recommendations = []
        
        # Check for anomalies
        anomalies = analysis.get("anomaly_detection", [])
        if len(anomalies) > 5:
            recommendations.append(ImprovementRecommendation(
                id="monitoring_improvement_1",
                title="Enhance monitoring and alerting",
                description=f"Detected {len(anomalies)} quality anomalies. Improve monitoring coverage.",
                category=ImprovementCategory.MONITORING,
                priority=ImprovementPriority.MEDIUM,
                estimated_impact=0.6,
                estimated_effort=0.4,
                action_items=[
                    "Add more comprehensive monitoring",
                    "Implement predictive alerting",
                    "Enhance anomaly detection algorithms",
                    "Add automated root cause analysis",
                    "Improve alert triage processes"
                ],
                success_metrics=[
                    "Reduce false positive alerts by >50%",
                    "Improve anomaly detection accuracy",
                    "Reduce mean time to detection (MTTD)"
                ],
                dependencies=["monitoring_team", "ops_team"],
                timeline="2-4 weeks"
            ))
        
        return recommendations
    
    def _calculate_performance_score(self, monitoring_summary: Dict[str, Any]) -> float:
        """Calculate performance score from monitoring metrics."""
        response_time = monitoring_summary.get("response_time_p95", {}).get("mean", 0)
        error_rate = monitoring_summary.get("error_rate", {}).get("mean", 0)
        throughput = monitoring_summary.get("throughput", {}).get("mean", 0)
        
        # Normalize metrics (0-1)
        response_score = max(0, 1 - (response_time / 5.0))  # 5s max
        error_score = max(0, 1 - (error_rate * 20))  # 5% max
        throughput_score = min(1, throughput / 100)  # 100 req/s max
        
        return (response_score * 0.4 + error_score * 0.4 + throughput_score * 0.2)
    
    def _calculate_cost_efficiency_score(self, metrics: List[SystemMetrics]) -> float:
        """Calculate cost efficiency score."""
        if not metrics:
            return 0.0
        
        costs_per_rec = [m.cost_metrics.cost_per_recommendation for m in metrics]
        avg_cost = statistics.mean(costs_per_rec)
        
        # Normalize (0-1) - lower cost is better
        return max(0, 1 - (avg_cost / 1.0))  # $1 max per recommendation
    
    def track_improvement_implementation(self, recommendation_id: str, implementation_data: Dict[str, Any]) -> None:
        """Track the implementation of an improvement recommendation."""
        implementation_record = {
            "recommendation_id": recommendation_id,
            "implementation_date": time.time(),
            "implementation_data": implementation_data,
            "status": "implemented"
        }
        
        self.implemented_changes.append(implementation_record)
    
    def evaluate_improvement_impact(self, recommendation_id: str, hours_before: int = 24, hours_after: int = 24) -> Dict[str, Any]:
        """Evaluate the impact of an implemented improvement."""
        # This would compare metrics before and after implementation
        # For now, return placeholder data
        return {
            "recommendation_id": recommendation_id,
            "impact_analysis": {
                "quality_improvement": 0.15,
                "performance_improvement": 0.10,
                "cost_reduction": 0.20
            },
            "success_metrics_met": True,
            "recommendation": "Continue with similar improvements"
        }
    
    def export_improvement_plan(self, file_path: str) -> None:
        """Export improvement plan to JSON file."""
        current_recommendations = self.generate_improvement_recommendations()
        
        plan_data = {
            "generated_at": time.time(),
            "recommendations": [asdict(rec) for rec in current_recommendations],
            "quality_analysis": self.analyze_system_quality(),
            "implementation_history": self.implemented_changes
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(plan_data, f, indent=2, ensure_ascii=False)
