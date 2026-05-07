"""
Phase 6 Monitoring: Comprehensive logging and monitoring system.

This module provides real-time monitoring, alerting, and health checks
for the restaurant recommendation system to ensure reliable operation
and early detection of issues.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import statistics
from collections import defaultdict, deque


class AlertLevel(Enum):
    """Enumeration of alert levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class HealthStatus(Enum):
    """Enumeration of system health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"


@dataclass
class Alert:
    """Represents a system alert."""
    timestamp: float
    level: AlertLevel
    component: str
    message: str
    details: Dict[str, Any]
    resolved: bool = False
    resolved_timestamp: Optional[float] = None


@dataclass
class HealthCheck:
    """Represents a health check result."""
    component: str
    status: HealthStatus
    timestamp: float
    response_time: float
    details: Dict[str, Any]
    error_message: Optional[str] = None


@dataclass
class SystemMetrics:
    """Real-time system metrics."""
    timestamp: float
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_requests: int
    queue_size: int
    error_rate: float
    response_time_p95: float
    throughput: float


class MonitoringSystem:
    """
    Comprehensive monitoring and alerting system.
    
    Provides real-time monitoring, health checks, alerting, and
    performance tracking for the recommendation system.
    """
    
    def __init__(self, max_alerts: int = 1000, max_metrics: int = 10000):
        self.max_alerts = max_alerts
        self.max_metrics = max_metrics
        
        # Storage
        self.alerts: deque[Alert] = deque(maxlen=max_alerts)
        self.health_checks: Dict[str, HealthCheck] = {}
        self.system_metrics: deque[SystemMetrics] = deque(maxlen=max_metrics)
        
        # Alert callbacks
        self.alert_callbacks: List[Callable[[Alert], None]] = []
        
        # Health check functions
        self.health_check_functions: Dict[str, Callable[[], HealthCheck]] = {}
        
        # Thresholds
        self.thresholds = {
            "error_rate": 0.05,  # 5%
            "response_time_p95": 2.0,  # 2 seconds
            "cpu_usage": 0.8,  # 80%
            "memory_usage": 0.85,  # 85%
            "disk_usage": 0.9,  # 90%
            "queue_size": 100
        }
        
        # Setup logging
        self.setup_logging()
    
    def setup_logging(self) -> None:
        """Setup structured logging for monitoring."""
        self.logger = logging.getLogger("zomato_rec.monitoring")
        self.logger.setLevel(logging.INFO)
        
        # Create handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def add_alert_callback(self, callback: Callable[[Alert], None]) -> None:
        """Add a callback function for alert notifications."""
        self.alert_callbacks.append(callback)
    
    def register_health_check(self, component: str, check_function: Callable[[], HealthCheck]) -> None:
        """Register a health check function for a component."""
        self.health_check_functions[component] = check_function
    
    def create_alert(
        self, 
        level: AlertLevel, 
        component: str, 
        message: str, 
        details: Optional[Dict[str, Any]] = None
    ) -> Alert:
        """
        Create and store a new alert.
        
        Args:
            level: Alert severity level
            component: System component generating the alert
            message: Alert message
            details: Additional alert details
            
        Returns:
            Alert object
        """
        alert = Alert(
            timestamp=time.time(),
            level=level,
            component=component,
            message=message,
            details=details or {}
        )
        
        self.alerts.append(alert)
        
        # Log the alert
        log_level = {
            AlertLevel.INFO: logging.INFO,
            AlertLevel.WARNING: logging.WARNING,
            AlertLevel.ERROR: logging.ERROR,
            AlertLevel.CRITICAL: logging.CRITICAL
        }.get(level, logging.INFO)
        
        self.logger.log(log_level, f"[{component.upper()}] {message} - {details}")
        
        # Trigger callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Error in alert callback: {e}")
        
        return alert
    
    def resolve_alert(self, alert: Alert) -> None:
        """Mark an alert as resolved."""
        alert.resolved = True
        alert.resolved_timestamp = time.time()
        self.logger.info(f"Alert resolved: [{alert.component.upper()}] {alert.message}")
    
    def run_health_checks(self) -> Dict[str, HealthCheck]:
        """Run all registered health checks."""
        results = {}
        
        for component, check_function in self.health_check_functions.items():
            try:
                start_time = time.time()
                health_check = check_function()
                end_time = time.time()
                
                health_check.response_time = end_time - start_time
                health_check.timestamp = end_time
                
                results[component] = health_check
                self.health_checks[component] = health_check
                
                # Create alert if unhealthy
                if health_check.status in [HealthStatus.UNHEALTHY, HealthStatus.CRITICAL]:
                    self.create_alert(
                        AlertLevel.ERROR if health_check.status == HealthStatus.UNHEALTHY else AlertLevel.CRITICAL,
                        component,
                        f"Health check failed: {health_check.status.value}",
                        health_check.details
                    )
                
            except Exception as e:
                # Create error alert for failed health check
                self.create_alert(
                    AlertLevel.ERROR,
                    component,
                    f"Health check execution failed",
                    {"error": str(e)}
                )
        
        return results
    
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics."""
        try:
            import psutil
            
            # Get system metrics
            cpu_usage = psutil.cpu_percent(interval=1) / 100
            memory = psutil.virtual_memory()
            memory_usage = memory.percent / 100
            disk = psutil.disk_usage('/')
            disk_usage = disk.used / disk.total
            
            # Get application-specific metrics (simplified)
            active_requests = self._get_active_requests()
            queue_size = self._get_queue_size()
            error_rate = self._get_error_rate()
            response_time_p95 = self._get_response_time_p95()
            throughput = self._get_throughput()
            
            metrics = SystemMetrics(
                timestamp=time.time(),
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                active_requests=active_requests,
                queue_size=queue_size,
                error_rate=error_rate,
                response_time_p95=response_time_p95,
                throughput=throughput
            )
            
            self.system_metrics.append(metrics)
            
            # Check thresholds and create alerts
            self._check_metric_thresholds(metrics)
            
            return metrics
            
        except ImportError:
            # psutil not available, return dummy metrics
            return SystemMetrics(
                timestamp=time.time(),
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                active_requests=0,
                queue_size=0,
                error_rate=0.0,
                response_time_p95=0.0,
                throughput=0.0
            )
    
    def _check_metric_thresholds(self, metrics: SystemMetrics) -> None:
        """Check metrics against thresholds and create alerts."""
        if metrics.error_rate > self.thresholds["error_rate"]:
            self.create_alert(
                AlertLevel.WARNING,
                "system",
                f"High error rate: {metrics.error_rate:.2%}",
                {"error_rate": metrics.error_rate, "threshold": self.thresholds["error_rate"]}
            )
        
        if metrics.response_time_p95 > self.thresholds["response_time_p95"]:
            self.create_alert(
                AlertLevel.WARNING,
                "system",
                f"High response time: {metrics.response_time_p95:.2f}s",
                {"response_time_p95": metrics.response_time_p95, "threshold": self.thresholds["response_time_p95"]}
            )
        
        if metrics.cpu_usage > self.thresholds["cpu_usage"]:
            self.create_alert(
                AlertLevel.WARNING,
                "system",
                f"High CPU usage: {metrics.cpu_usage:.1%}",
                {"cpu_usage": metrics.cpu_usage, "threshold": self.thresholds["cpu_usage"]}
            )
        
        if metrics.memory_usage > self.thresholds["memory_usage"]:
            self.create_alert(
                AlertLevel.WARNING,
                "system",
                f"High memory usage: {metrics.memory_usage:.1%}",
                {"memory_usage": metrics.memory_usage, "threshold": self.thresholds["memory_usage"]}
            )
        
        if metrics.disk_usage > self.thresholds["disk_usage"]:
            self.create_alert(
                AlertLevel.ERROR,
                "system",
                f"High disk usage: {metrics.disk_usage:.1%}",
                {"disk_usage": metrics.disk_usage, "threshold": self.thresholds["disk_usage"]}
            )
        
        if metrics.queue_size > self.thresholds["queue_size"]:
            self.create_alert(
                AlertLevel.WARNING,
                "system",
                f"High queue size: {metrics.queue_size}",
                {"queue_size": metrics.queue_size, "threshold": self.thresholds["queue_size"]}
            )
    
    def get_system_health(self) -> HealthStatus:
        """Get overall system health status."""
        if not self.health_checks:
            return HealthStatus.HEALTHY
        
        statuses = [check.status for check in self.health_checks.values()]
        
        if HealthStatus.CRITICAL in statuses:
            return HealthStatus.CRITICAL
        elif HealthStatus.UNHEALTHY in statuses:
            return HealthStatus.UNHEALTHY
        elif HealthStatus.DEGRADED in statuses:
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.HEALTHY
    
    def get_recent_alerts(
        self, 
        level: Optional[AlertLevel] = None, 
        component: Optional[str] = None,
        resolved: Optional[bool] = None,
        hours: int = 24
    ) -> List[Alert]:
        """Get recent alerts with filtering options."""
        cutoff_time = time.time() - (hours * 3600)
        
        filtered_alerts = []
        for alert in self.alerts:
            if alert.timestamp < cutoff_time:
                continue
            
            if level and alert.level != level:
                continue
            
            if component and alert.component != component:
                continue
            
            if resolved is not None and alert.resolved != resolved:
                continue
            
            filtered_alerts.append(alert)
        
        return sorted(filtered_alerts, key=lambda a: a.timestamp, reverse=True)
    
    def get_metrics_summary(self, hours: int = 1) -> Dict[str, Any]:
        """Get summary of system metrics for the specified time period."""
        cutoff_time = time.time() - (hours * 3600)
        recent_metrics = [m for m in self.system_metrics if m.timestamp >= cutoff_time]
        
        if not recent_metrics:
            return {}
        
        # Calculate statistics
        cpu_values = [m.cpu_usage for m in recent_metrics]
        memory_values = [m.memory_usage for m in recent_metrics]
        error_rates = [m.error_rate for m in recent_metrics]
        response_times = [m.response_time_p95 for m in recent_metrics]
        throughputs = [m.throughput for m in recent_metrics]
        
        return {
            "time_period_hours": hours,
            "sample_count": len(recent_metrics),
            "cpu": {
                "mean": statistics.mean(cpu_values),
                "max": max(cpu_values),
                "min": min(cpu_values)
            },
            "memory": {
                "mean": statistics.mean(memory_values),
                "max": max(memory_values),
                "min": min(memory_values)
            },
            "error_rate": {
                "mean": statistics.mean(error_rates),
                "max": max(error_rates),
                "min": min(error_rates)
            },
            "response_time_p95": {
                "mean": statistics.mean(response_times),
                "max": max(response_times),
                "min": min(response_times)
            },
            "throughput": {
                "mean": statistics.mean(throughputs),
                "max": max(throughputs),
                "min": min(throughputs)
            },
            "alerts_count": len(self.get_recent_alerts(hours=hours))
        }
    
    def export_monitoring_data(self, file_path: str) -> None:
        """Export monitoring data to JSON file."""
        data = {
            "alerts": [asdict(alert) for alert in self.alerts],
            "health_checks": {k: asdict(v) for k, v in self.health_checks.items()},
            "system_metrics": [asdict(m) for m in self.system_metrics],
            "export_timestamp": time.time()
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _get_active_requests(self) -> int:
        """Get number of active requests (placeholder)."""
        # In a real implementation, this would track actual requests
        return 0
    
    def _get_queue_size(self) -> int:
        """Get current queue size (placeholder)."""
        # In a real implementation, this would check actual queues
        return 0
    
    def _get_error_rate(self) -> float:
        """Get current error rate (placeholder)."""
        # In a real implementation, this would calculate from recent requests
        return 0.0
    
    def _get_response_time_p95(self) -> float:
        """Get 95th percentile response time (placeholder)."""
        # In a real implementation, this would calculate from recent requests
        return 0.0
    
    def _get_throughput(self) -> float:
        """Get current throughput (placeholder)."""
        # In a real implementation, this would calculate from recent requests
        return 0.0


class PerformanceTracker:
    """
    Performance tracking and analysis system.
    
    Tracks performance metrics over time and provides insights
    for optimization and capacity planning.
    """
    
    def __init__(self, max_history: int = 10000):
        self.max_history = max_history
        self.request_history: deque[Dict[str, Any]] = deque(maxlen=max_history)
        self.performance_summary = {}
    
    def track_request(
        self, 
        request_id: str,
        endpoint: str,
        start_time: float,
        end_time: float,
        status_code: int,
        response_size: int = 0
    ) -> None:
        """Track a single request for performance analysis."""
        request_data = {
            "request_id": request_id,
            "endpoint": endpoint,
            "start_time": start_time,
            "end_time": end_time,
            "duration": end_time - start_time,
            "status_code": status_code,
            "response_size": response_size,
            "timestamp": end_time
        }
        
        self.request_history.append(request_data)
        self._update_performance_summary()
    
    def _update_performance_summary(self) -> None:
        """Update performance summary statistics."""
        if not self.request_history:
            return
        
        recent_requests = list(self.request_history)[-1000:]  # Last 1000 requests
        
        # Calculate statistics
        durations = [r["duration"] for r in recent_requests]
        status_codes = [r["status_code"] for r in recent_requests]
        response_sizes = [r["response_size"] for r in recent_requests]
        
        # Error rate
        error_count = sum(1 for code in status_codes if code >= 400)
        error_rate = error_count / len(status_codes)
        
        # Response time percentiles
        sorted_durations = sorted(durations)
        p50 = sorted_durations[int(len(sorted_durations) * 0.5)]
        p95 = sorted_durations[int(len(sorted_durations) * 0.95)]
        p99 = sorted_durations[int(len(sorted_durations) * 0.99)]
        
        self.performance_summary = {
            "total_requests": len(recent_requests),
            "error_rate": error_rate,
            "avg_response_time": statistics.mean(durations),
            "p50_response_time": p50,
            "p95_response_time": p95,
            "p99_response_time": p99,
            "avg_response_size": statistics.mean(response_sizes) if response_sizes else 0,
            "requests_per_second": self._calculate_rps(recent_requests)
        }
    
    def _calculate_rps(self, requests: List[Dict[str, Any]]) -> float:
        """Calculate requests per second."""
        if len(requests) < 2:
            return 0.0
        
        timestamps = [r["timestamp"] for r in requests]
        time_span = max(timestamps) - min(timestamps)
        
        return len(requests) / time_span if time_span > 0 else 0.0
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get current performance summary."""
        return self.performance_summary.copy()
    
    def get_endpoint_performance(self, endpoint: str) -> Dict[str, Any]:
        """Get performance statistics for a specific endpoint."""
        endpoint_requests = [r for r in self.request_history if r["endpoint"] == endpoint]
        
        if not endpoint_requests:
            return {}
        
        durations = [r["duration"] for r in endpoint_requests]
        status_codes = [r["status_code"] for r in endpoint_requests]
        
        error_count = sum(1 for code in status_codes if code >= 400)
        error_rate = error_count / len(status_codes)
        
        return {
            "endpoint": endpoint,
            "total_requests": len(endpoint_requests),
            "error_rate": error_rate,
            "avg_response_time": statistics.mean(durations),
            "min_response_time": min(durations),
            "max_response_time": max(durations)
        }
