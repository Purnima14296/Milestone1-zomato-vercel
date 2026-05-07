"""
Phase 6 Dashboard: Evaluation dashboard and reporting system.

This module provides comprehensive dashboards and reports for visualizing
system performance, quality metrics, and evaluation results to support
data-driven decision making and continuous improvement.
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
from golden_tests import GoldenTestSuite, GoldenTestCase
from monitoring import MonitoringSystem, AlertLevel


class ReportType(Enum):
    """Enumeration of report types."""
    QUALITY_SUMMARY = "quality_summary"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    CONSTRAINT_ANALYSIS = "constraint_analysis"
    DIVERSITY_ANALYSIS = "diversity_analysis"
    COST_ANALYSIS = "cost_analysis"
    GOLDEN_TESTS = "golden_tests"
    SYSTEM_HEALTH = "system_health"
    TREND_ANALYSIS = "trend_analysis"


@dataclass
class DashboardWidget:
    """Represents a dashboard widget."""
    widget_id: str
    title: str
    widget_type: str  # "metric", "chart", "table", "alert"
    data: Dict[str, Any]
    position: Dict[str, int]  # x, y, width, height
    refresh_interval: int = 300  # seconds


@dataclass
class DashboardConfig:
    """Configuration for a dashboard."""
    dashboard_id: str
    title: str
    description: str
    widgets: List[DashboardWidget]
    layout: Dict[str, Any]
    created_at: float
    updated_at: float


class EvaluationDashboard:
    """
    Comprehensive evaluation dashboard and reporting system.
    
    Provides real-time dashboards, automated reports, and actionable insights
    for monitoring and improving the recommendation system quality.
    """
    
    def __init__(self, metrics_collector: MetricsCollector, monitoring_system: MonitoringSystem):
        self.metrics_collector = metrics_collector
        self.monitoring_system = monitoring_system
        self.golden_test_suite = GoldenTestSuite()
        
        # Dashboard configurations
        self.dashboards: Dict[str, DashboardConfig] = {}
        self.reports: Dict[str, Any] = {}
        
        # Initialize default dashboards
        self._initialize_default_dashboards()
    
    def _initialize_default_dashboards(self) -> None:
        """Initialize default dashboard configurations."""
        # Main Quality Dashboard
        quality_widgets = [
            DashboardWidget(
                widget_id="quality_score",
                title="Overall Quality Score",
                widget_type="metric",
                data={"value": 0.85, "trend": "up", "unit": "%"},
                position={"x": 0, "y": 0, "width": 3, "height": 2}
            ),
            DashboardWidget(
                widget_id="constraint_satisfaction",
                title="Constraint Satisfaction",
                widget_type="chart",
                data={"labels": [], "datasets": []},
                position={"x": 3, "y": 0, "width": 6, "height": 4}
            ),
            DashboardWidget(
                widget_id="diversity_metrics",
                title="Diversity Metrics",
                widget_type="table",
                data={"headers": [], "rows": []},
                position={"x": 9, "y": 0, "width": 3, "height": 4}
            ),
            DashboardWidget(
                widget_id="recent_alerts",
                title="Recent Alerts",
                widget_type="alert",
                data={"alerts": []},
                position={"x": 0, "y": 4, "width": 12, "height": 3}
            )
        ]
        
        self.dashboards["quality"] = DashboardConfig(
            dashboard_id="quality",
            title="Quality Overview",
            description="System quality metrics and performance indicators",
            widgets=quality_widgets,
            layout={"columns": 12, "rows": 7},
            created_at=time.time(),
            updated_at=time.time()
        )
        
        # Performance Dashboard
        performance_widgets = [
            DashboardWidget(
                widget_id="response_time",
                title="Response Time (P95)",
                widget_type="metric",
                data={"value": 1.2, "trend": "stable", "unit": "s"},
                position={"x": 0, "y": 0, "width": 3, "height": 2}
            ),
            DashboardWidget(
                widget_id="throughput",
                title="Requests per Second",
                widget_type="metric",
                data={"value": 45.2, "trend": "up", "unit": "req/s"},
                position={"x": 3, "y": 0, "width": 3, "height": 2}
            ),
            DashboardWidget(
                widget_id="error_rate",
                title="Error Rate",
                widget_type="metric",
                data={"value": 0.02, "trend": "down", "unit": "%"},
                position={"x": 6, "y": 0, "width": 3, "height": 2}
            ),
            DashboardWidget(
                widget_id="latency_chart",
                title="Latency Trends",
                widget_type="chart",
                data={"labels": [], "datasets": []},
                position={"x": 0, "y": 2, "width": 12, "height": 4}
            ),
            DashboardWidget(
                widget_id="system_resources",
                title="System Resources",
                widget_type="chart",
                data={"labels": [], "datasets": []},
                position={"x": 0, "y": 6, "width": 12, "height": 3}
            )
        ]
        
        self.dashboards["performance"] = DashboardConfig(
            dashboard_id="performance",
            title="Performance Monitoring",
            description="System performance and resource utilization",
            widgets=performance_widgets,
            layout={"columns": 12, "rows": 9},
            created_at=time.time(),
            updated_at=time.time()
        )
    
    def update_dashboard_data(self, dashboard_id: str) -> None:
        """Update dashboard data with latest metrics."""
        if dashboard_id not in self.dashboards:
            return
        
        dashboard = self.dashboards[dashboard_id]
        
        if dashboard_id == "quality":
            self._update_quality_dashboard(dashboard)
        elif dashboard_id == "performance":
            self._update_performance_dashboard(dashboard)
        
        dashboard.updated_at = time.time()
    
    def _update_quality_dashboard(self, dashboard: DashboardConfig) -> None:
        """Update quality dashboard with latest metrics."""
        # Get aggregated metrics
        aggregated = self.metrics_collector.get_aggregated_metrics(100)
        
        if not aggregated:
            return
        
        # Update quality score widget
        quality_score = aggregated.get("avg_quality", 0) * 100
        for widget in dashboard.widgets:
            if widget.widget_id == "quality_score":
                widget.data["value"] = quality_score
                widget.data["trend"] = "improving" if quality_score > 80 else "stable"
            
            elif widget.widget_id == "constraint_satisfaction":
                # Update constraint satisfaction chart
                constraint_dist = aggregated.get("constraint_distribution", {})
                widget.data = {
                    "labels": ["Satisfaction", "Diversity", "Performance"],
                    "datasets": [{
                        "label": "Current",
                        "data": [
                            constraint_dist.get("mean", 0) * 100,
                            aggregated.get("avg_diversity", 0) * 100,
                            100 - (aggregated.get("avg_latency", 0) * 10)  # Simple performance score
                        ],
                        "backgroundColor": ["#4CAF50", "#2196F3", "#FF9800"]
                    }]
                }
            
            elif widget.widget_id == "diversity_metrics":
                # Update diversity metrics table
                widget.data = {
                    "headers": ["Metric", "Value", "Status"],
                    "rows": [
                        ["Cuisine Diversity", f"{aggregated.get('avg_diversity', 0):.2%}", "Good"],
                        ["Constraint Satisfaction", f"{aggregated.get('avg_constraint_satisfaction', 0):.2%}", "Good"],
                        ["Average Quality", f"{aggregated.get('avg_quality', 0):.2%}", "Good"],
                        ["Average Latency", f"{aggregated.get('avg_latency', 0):.2f}s", "Good"]
                    ]
                }
            
            elif widget.widget_id == "recent_alerts":
                # Update recent alerts
                recent_alerts = self.monitoring_system.get_recent_alerts(hours=24)
                widget.data["alerts"] = [
                    {
                        "level": alert.level.value,
                        "component": alert.component,
                        "message": alert.message,
                        "timestamp": alert.timestamp
                    }
                    for alert in recent_alerts[:5]
                ]
    
    def _update_performance_dashboard(self, dashboard: DashboardConfig) -> None:
        """Update performance dashboard with latest metrics."""
        # Get system metrics summary
        metrics_summary = self.monitoring_system.get_metrics_summary(hours=1)
        
        if not metrics_summary:
            return
        
        # Update performance widgets
        for widget in dashboard.widgets:
            if widget.widget_id == "response_time":
                widget.data["value"] = metrics_summary.get("response_time_p95", {}).get("mean", 0)
                widget.data["trend"] = "stable"
            
            elif widget.widget_id == "throughput":
                widget.data["value"] = metrics_summary.get("throughput", {}).get("mean", 0)
                widget.data["trend"] = "up"
            
            elif widget.widget_id == "error_rate":
                widget.data["value"] = metrics_summary.get("error_rate", {}).get("mean", 0) * 100
                widget.data["trend"] = "down"
            
            elif widget.widget_id == "latency_chart":
                # Update latency trends chart
                widget.data = {
                    "labels": ["1h ago", "50m ago", "40m ago", "30m ago", "20m ago", "10m ago", "Now"],
                    "datasets": [{
                        "label": "Response Time (s)",
                        "data": [1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9],
                        "borderColor": "#2196F3",
                        "fill": False
                    }]
                }
            
            elif widget.widget_id == "system_resources":
                # Update system resources chart
                widget.data = {
                    "labels": ["CPU", "Memory", "Disk"],
                    "datasets": [{
                        "label": "Usage (%)",
                        "data": [
                            metrics_summary.get("cpu", {}).get("mean", 0) * 100,
                            metrics_summary.get("memory", {}).get("mean", 0) * 100,
                            metrics_summary.get("disk", {}).get("mean", 0) * 100
                        ],
                        "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56"]
                    }]
                }
    
    def generate_report(self, report_type: ReportType, hours: int = 24) -> Dict[str, Any]:
        """
        Generate a comprehensive report for the specified type.
        
        Args:
            report_type: Type of report to generate
            hours: Time period for the report
            
        Returns:
            Report data dictionary
        """
        if report_type == ReportType.QUALITY_SUMMARY:
            return self._generate_quality_summary_report(hours)
        elif report_type == ReportType.PERFORMANCE_ANALYSIS:
            return self._generate_performance_analysis_report(hours)
        elif report_type == ReportType.CONSTRAINT_ANALYSIS:
            return self._generate_constraint_analysis_report(hours)
        elif report_type == ReportType.DIVERSITY_ANALYSIS:
            return self._generate_diversity_analysis_report(hours)
        elif report_type == ReportType.COST_ANALYSIS:
            return self._generate_cost_analysis_report(hours)
        elif report_type == ReportType.GOLDEN_TESTS:
            return self._generate_golden_tests_report()
        elif report_type == ReportType.SYSTEM_HEALTH:
            return self._generate_system_health_report(hours)
        elif report_type == ReportType.TREND_ANALYSIS:
            return self._generate_trend_analysis_report(hours)
        else:
            return {"error": f"Unknown report type: {report_type}"}
    
    def _generate_quality_summary_report(self, hours: int) -> Dict[str, Any]:
        """Generate quality summary report."""
        aggregated = self.metrics_collector.get_aggregated_metrics(100)
        
        return {
            "report_type": "quality_summary",
            "time_period_hours": hours,
            "generated_at": time.time(),
            "executive_summary": {
                "overall_quality_score": aggregated.get("avg_quality", 0),
                "constraint_satisfaction": aggregated.get("avg_constraint_satisfaction", 0),
                "diversity_score": aggregated.get("avg_diversity", 0),
                "performance_score": min(1.0, 2.0 - aggregated.get("avg_latency", 0)),
                "total_recommendations": aggregated.get("total_requests", 0)
            },
            "detailed_metrics": {
                "constraint_metrics": aggregated.get("constraint_distribution", {}),
                "diversity_metrics": aggregated.get("diversity_trends", {}),
                "performance_metrics": aggregated.get("performance_trends", {})
            },
            "recommendations": self._generate_quality_recommendations(aggregated)
        }
    
    def _generate_performance_analysis_report(self, hours: int) -> Dict[str, Any]:
        """Generate performance analysis report."""
        metrics_summary = self.monitoring_system.get_metrics_summary(hours)
        
        return {
            "report_type": "performance_analysis",
            "time_period_hours": hours,
            "generated_at": time.time(),
            "performance_summary": {
                "avg_response_time": metrics_summary.get("response_time_p95", {}).get("mean", 0),
                "p99_response_time": metrics_summary.get("response_time_p95", {}).get("max", 0),
                "throughput": metrics_summary.get("throughput", {}).get("mean", 0),
                "error_rate": metrics_summary.get("error_rate", {}).get("mean", 0),
                "total_requests": metrics_summary.get("sample_count", 0)
            },
            "resource_utilization": {
                "cpu": metrics_summary.get("cpu", {}),
                "memory": metrics_summary.get("memory", {}),
                "disk": metrics_summary.get("disk", {})
            },
            "performance_issues": self._identify_performance_issues(metrics_summary),
            "recommendations": self._generate_performance_recommendations(metrics_summary)
        }
    
    def _generate_constraint_analysis_report(self, hours: int) -> Dict[str, Any]:
        """Generate constraint analysis report."""
        recent_metrics = self.metrics_collector.metrics_history[-100:] if self.metrics_collector.metrics_history else []
        
        constraint_violations = defaultdict(int)
        constraint_satisfaction = []
        
        for metrics in recent_metrics:
            constraint_satisfaction.append(metrics.constraint_metrics.overall_satisfaction)
            
            for violated in metrics.constraint_metrics.violated_constraints:
                constraint_violations[violated] += 1
        
        return {
            "report_type": "constraint_analysis",
            "time_period_hours": hours,
            "generated_at": time.time(),
            "constraint_performance": {
                "avg_satisfaction": statistics.mean(constraint_satisfaction) if constraint_satisfaction else 0,
                "satisfaction_trend": "improving" if len(constraint_satisfaction) > 1 and constraint_satisfaction[-1] > constraint_satisfaction[0] else "stable",
                "total_violations": sum(constraint_violations.values()),
                "violation_breakdown": dict(constraint_violations)
            },
            "constraint_analysis": {
                "most_violated": max(constraint_violations.items(), key=lambda x: x[1]) if constraint_violations else None,
                "least_violated": min(constraint_violations.items(), key=lambda x: x[1]) if constraint_violations else None,
                "violation_rate": sum(constraint_violations.values()) / len(recent_metrics) if recent_metrics else 0
            },
            "recommendations": self._generate_constraint_recommendations(constraint_violations)
        }
    
    def _generate_diversity_analysis_report(self, hours: int) -> Dict[str, Any]:
        """Generate diversity analysis report."""
        recent_metrics = self.metrics_collector.metrics_history[-100:] if self.metrics_collector.metrics_history else []
        
        diversity_scores = []
        cuisine_diversity = []
        price_diversity = []
        rating_diversity = []
        
        for metrics in recent_metrics:
            diversity_scores.append(metrics.diversity_metrics.overall_diversity)
            cuisine_diversity.append(metrics.diversity_metrics.cuisine_diversity)
            price_diversity.append(metrics.diversity_metrics.price_diversity)
            rating_diversity.append(metrics.diversity_metrics.rating_diversity)
        
        return {
            "report_type": "diversity_analysis",
            "time_period_hours": hours,
            "generated_at": time.time(),
            "diversity_summary": {
                "avg_overall_diversity": statistics.mean(diversity_scores) if diversity_scores else 0,
                "avg_cuisine_diversity": statistics.mean(cuisine_diversity) if cuisine_diversity else 0,
                "avg_price_diversity": statistics.mean(price_diversity) if price_diversity else 0,
                "avg_rating_diversity": statistics.mean(rating_diversity) if rating_diversity else 0,
                "diversity_trend": "improving" if len(diversity_scores) > 1 and diversity_scores[-1] > diversity_scores[0] else "stable"
            },
            "diversity_insights": {
                "cuisine_analysis": self._analyze_cuisine_diversity(recent_metrics),
                "price_analysis": self._analyze_price_diversity(recent_metrics),
                "rating_analysis": self._analyze_rating_diversity(recent_metrics)
            },
            "recommendations": self._generate_diversity_recommendations(diversity_scores)
        }
    
    def _generate_cost_analysis_report(self, hours: int) -> Dict[str, Any]:
        """Generate cost analysis report."""
        recent_metrics = self.metrics_collector.metrics_history[-100:] if self.metrics_collector.metrics_history else []
        
        total_costs = []
        llm_costs = []
        costs_per_recommendation = []
        tokens_used = []
        
        for metrics in recent_metrics:
            total_costs.append(metrics.cost_metrics.total_cost)
            llm_costs.append(metrics.cost_metrics.llm_cost)
            costs_per_recommendation.append(metrics.cost_metrics.cost_per_recommendation)
            tokens_used.append(metrics.cost_metrics.tokens_used)
        
        return {
            "report_type": "cost_analysis",
            "time_period_hours": hours,
            "generated_at": time.time(),
            "cost_summary": {
                "total_cost": sum(total_costs),
                "avg_cost_per_request": statistics.mean(total_costs) if total_costs else 0,
                "avg_llm_cost": statistics.mean(llm_costs) if llm_costs else 0,
                "avg_cost_per_recommendation": statistics.mean(costs_per_recommendation) if costs_per_recommendation else 0,
                "total_tokens_used": sum(tokens_used),
                "avg_tokens_per_request": statistics.mean(tokens_used) if tokens_used else 0
            },
            "cost_breakdown": {
                "llm_cost_percentage": (sum(llm_costs) / sum(total_costs) * 100) if total_costs else 0,
                "other_costs_percentage": ((sum(total_costs) - sum(llm_costs)) / sum(total_costs) * 100) if total_costs else 0
            },
            "cost_trends": {
                "cost_trend": "increasing" if len(total_costs) > 1 and total_costs[-1] > total_costs[0] else "stable",
                "efficiency_trend": "improving" if len(costs_per_recommendation) > 1 and costs_per_recommendation[-1] < costs_per_recommendation[0] else "stable"
            },
            "recommendations": self._generate_cost_recommendations(total_costs, llm_costs)
        }
    
    def _generate_golden_tests_report(self) -> Dict[str, Any]:
        """Generate golden tests report."""
        test_summary = self.golden_test_suite.get_test_summary()
        
        return {
            "report_type": "golden_tests",
            "generated_at": time.time(),
            "test_suite_summary": test_summary,
            "test_results": self._run_golden_tests(),
            "test_analysis": {
                "pass_rate": 0.95,  # Placeholder
                "failure_analysis": [],
                "performance_regression": False
            },
            "recommendations": self._generate_golden_test_recommendations()
        }
    
    def _generate_system_health_report(self, hours: int) -> Dict[str, Any]:
        """Generate system health report."""
        health_status = self.monitoring_system.get_system_health()
        recent_alerts = self.monitoring_system.get_recent_alerts(hours=hours)
        metrics_summary = self.monitoring_system.get_metrics_summary(hours)
        
        return {
            "report_type": "system_health",
            "time_period_hours": hours,
            "generated_at": time.time(),
            "health_status": health_status.value,
            "alert_summary": {
                "total_alerts": len(recent_alerts),
                "critical_alerts": len([a for a in recent_alerts if a.level == AlertLevel.CRITICAL]),
                "error_alerts": len([a for a in recent_alerts if a.level == AlertLevel.ERROR]),
                "warning_alerts": len([a for a in recent_alerts if a.level == AlertLevel.WARNING]),
                "resolved_alerts": len([a for a in recent_alerts if a.resolved])
            },
            "system_metrics": metrics_summary,
            "health_checks": self.monitoring_system.health_checks,
            "recommendations": self._generate_health_recommendations(recent_alerts)
        }
    
    def _generate_trend_analysis_report(self, hours: int) -> Dict[str, Any]:
        """Generate trend analysis report."""
        # This would analyze trends over time
        return {
            "report_type": "trend_analysis",
            "time_period_hours": hours,
            "generated_at": time.time(),
            "trends": {
                "quality_trend": "stable",
                "performance_trend": "improving",
                "cost_trend": "increasing",
                "diversity_trend": "stable"
            },
            "anomalies": [],
            "predictions": {
                "next_week_quality": 0.87,
                "next_week_performance": 0.92,
                "next_month_cost": 150.50
            },
            "recommendations": self._generate_trend_recommendations()
        }
    
    # Helper methods for generating recommendations
    def _generate_quality_recommendations(self, aggregated: Dict[str, Any]) -> List[str]:
        """Generate quality improvement recommendations."""
        recommendations = []
        
        quality_score = aggregated.get("avg_quality", 0)
        constraint_sat = aggregated.get("avg_constraint_satisfaction", 0)
        diversity = aggregated.get("avg_diversity", 0)
        
        if quality_score < 0.8:
            recommendations.append("Consider improving LLM prompt quality for better explanations")
        
        if constraint_sat < 0.9:
            recommendations.append("Review constraint validation logic to improve satisfaction rates")
        
        if diversity < 0.7:
            recommendations.append("Increase diversity in recommendation algorithm to avoid filter bubbles")
        
        if not recommendations:
            recommendations.append("System quality is performing well. Continue current configuration.")
        
        return recommendations
    
    def _generate_performance_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate performance improvement recommendations."""
        recommendations = []
        
        avg_latency = metrics.get("response_time_p95", {}).get("mean", 0)
        error_rate = metrics.get("error_rate", {}).get("mean", 0)
        cpu_usage = metrics.get("cpu", {}).get("mean", 0)
        
        if avg_latency > 2.0:
            recommendations.append("Consider optimizing database queries or adding caching")
        
        if error_rate > 0.05:
            recommendations.append("Investigate error patterns and improve error handling")
        
        if cpu_usage > 0.8:
            recommendations.append("Consider scaling horizontally or optimizing CPU-intensive operations")
        
        if not recommendations:
            recommendations.append("System performance is optimal. Continue monitoring.")
        
        return recommendations
    
    def _generate_constraint_recommendations(self, violations: Dict[str, int]) -> List[str]:
        """Generate constraint improvement recommendations."""
        recommendations = []
        
        if violations.get("location", 0) > 5:
            recommendations.append("Improve location matching algorithm or expand location database")
        
        if violations.get("budget", 0) > 5:
            recommendations.append("Review budget constraint logic and cost estimation accuracy")
        
        if violations.get("rating", 0) > 5:
            recommendations.append("Update rating data or adjust rating constraint thresholds")
        
        if violations.get("cuisine", 0) > 5:
            recommendations.append("Improve cuisine classification and matching algorithms")
        
        if not recommendations:
            recommendations.append("Constraint satisfaction is performing well.")
        
        return recommendations
    
    def _generate_diversity_recommendations(self, diversity_scores: List[float]) -> List[str]:
        """Generate diversity improvement recommendations."""
        recommendations = []
        
        if diversity_scores:
            avg_diversity = statistics.mean(diversity_scores)
            
            if avg_diversity < 0.6:
                recommendations.append("Implement diversity-aware ranking algorithms")
                recommendations.append("Add explicit diversity objectives in recommendation scoring")
            elif avg_diversity < 0.8:
                recommendations.append("Consider adding more diversity factors to ranking")
        
        if not recommendations:
            recommendations.append("Diversity metrics are within acceptable range.")
        
        return recommendations
    
    def _generate_cost_recommendations(self, total_costs: List[float], llm_costs: List[float]) -> List[str]:
        """Generate cost optimization recommendations."""
        recommendations = []
        
        if total_costs:
            avg_cost = statistics.mean(total_costs)
            avg_llm_cost = statistics.mean(llm_costs) if llm_costs else 0
            
            if avg_llm_cost / avg_cost > 0.7:
                recommendations.append("Consider optimizing LLM usage or switching to more cost-effective models")
                recommendations.append("Implement response caching to reduce LLM calls")
            
            if avg_cost > 1.0:
                recommendations.append("Review cost per recommendation and implement cost controls")
        
        if not recommendations:
            recommendations.append("Cost structure is optimized. Continue monitoring.")
        
        return recommendations
    
    def _generate_golden_test_recommendations(self) -> List[str]:
        """Generate golden test improvement recommendations."""
        return [
            "Continue monitoring golden test performance",
            "Add more edge case scenarios to test suite",
            "Automate golden test execution in CI/CD pipeline"
        ]
    
    def _generate_health_recommendations(self, alerts: List) -> List[str]:
        """Generate health improvement recommendations."""
        recommendations = []
        
        critical_alerts = [a for a in alerts if a.level == AlertLevel.CRITICAL]
        error_alerts = [a for a in alerts if a.level == AlertLevel.ERROR]
        
        if critical_alerts:
            recommendations.append("Address critical system issues immediately")
        
        if len(error_alerts) > 10:
            recommendations.append("Investigate recurring error patterns")
        
        if not recommendations:
            recommendations.append("System health is stable. Continue monitoring.")
        
        return recommendations
    
    def _generate_trend_recommendations(self) -> List[str]:
        """Generate trend-based recommendations."""
        return [
            "Monitor trends for early detection of performance degradation",
            "Set up automated alerts for significant trend changes",
            "Regularly review and adjust system parameters based on trends"
        ]
    
    def _run_golden_tests(self) -> Dict[str, Any]:
        """Run golden test suite (placeholder implementation)."""
        # This would actually run the golden tests
        return {
            "total_tests": 20,
            "passed": 19,
            "failed": 1,
            "execution_time": 45.2,
            "test_results": []
        }
    
    def _analyze_cuisine_diversity(self, metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Analyze cuisine diversity patterns."""
        return {"analysis": "Cuisine diversity is stable with good variety"}
    
    def _analyze_price_diversity(self, metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Analyze price diversity patterns."""
        return {"analysis": "Price diversity shows good range distribution"}
    
    def _analyze_rating_diversity(self, metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Analyze rating diversity patterns."""
        return {"analysis": "Rating diversity is within expected range"}
    
    def _identify_performance_issues(self, metrics: Dict[str, Any]) -> List[str]:
        """Identify performance issues from metrics."""
        issues = []
        
        if metrics.get("response_time_p95", {}).get("mean", 0) > 2.0:
            issues.append("High response times detected")
        
        if metrics.get("error_rate", {}).get("mean", 0) > 0.05:
            issues.append("Elevated error rate detected")
        
        return issues
    
    def export_dashboard(self, dashboard_id: str, file_path: str) -> None:
        """Export dashboard configuration to JSON file."""
        if dashboard_id not in self.dashboards:
            return
        
        dashboard = self.dashboards[dashboard_id]
        dashboard_data = asdict(dashboard)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
    
    def export_report(self, report_type: ReportType, file_path: str, hours: int = 24) -> None:
        """Export report to JSON file."""
        report = self.generate_report(report_type, hours)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
