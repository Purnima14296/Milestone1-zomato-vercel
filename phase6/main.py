"""
Phase 6 Main Entry Point: Comprehensive evaluation, monitoring, and quality improvement.

This module provides the main entry point for Phase 6, integrating all components
for system evaluation, monitoring, and continuous quality improvement.
"""

import sys
from pathlib import Path

# Add the phase6 directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from golden_tests import GoldenTestSuite, TestScenario
from metrics import MetricsCollector, SystemMetrics
from monitoring import MonitoringSystem, AlertLevel, HealthStatus
from dashboard import EvaluationDashboard, ReportType
from quality_improvement import QualityImprovementEngine
import argparse
import json
import time


def build_parser() -> argparse.ArgumentParser:
    """Build the comprehensive command-line argument parser."""
    p = argparse.ArgumentParser(
        description="Phase 6: Evaluation, Monitoring & Quality Improvement System"
    )
    
    # Main actions
    p.add_argument(
        "action",
        choices=["golden-tests", "metrics", "monitoring", "dashboard", "reports", "quality", "all"],
        help="Main action to perform"
    )
    
    # Golden tests options
    p.add_argument(
        "--test-scenario",
        choices=[s.value for s in TestScenario],
        help="Run specific test scenario"
    )
    p.add_argument(
        "--save-tests",
        help="Save golden test cases to file"
    )
    p.add_argument(
        "--load-tests",
        help="Load golden test cases from file"
    )
    
    # Metrics options
    p.add_argument(
        "--metrics-input",
        help="Input file for metrics analysis"
    )
    p.add_argument(
        "--metrics-output",
        help="Output file for metrics results"
    )
    p.add_argument(
        "--aggregate",
        type=int,
        default=100,
        help="Number of recent metrics to aggregate"
    )
    
    # Monitoring options
    p.add_argument(
        "--monitoring-hours",
        type=int,
        default=1,
        help="Hours of monitoring data to analyze"
    )
    p.add_argument(
        "--alert-level",
        choices=[level.value for level in AlertLevel],
        help="Filter alerts by level"
    )
    p.add_argument(
        "--export-monitoring",
        help="Export monitoring data to file"
    )
    
    # Dashboard options
    p.add_argument(
        "--dashboard-id",
        choices=["quality", "performance"],
        default="quality",
        help="Dashboard to generate"
    )
    p.add_argument(
        "--export-dashboard",
        help="Export dashboard configuration to file"
    )
    
    # Reports options
    p.add_argument(
        "--report-type",
        choices=[rt.value for rt in ReportType],
        help="Type of report to generate"
    )
    p.add_argument(
        "--report-hours",
        type=int,
        default=24,
        help="Hours of data for report generation"
    )
    p.add_argument(
        "--export-report",
        help="Export report to file"
    )
    
    # Quality improvement options
    p.add_argument(
        "--quality-hours",
        type=int,
        default=24,
        help="Hours of data for quality analysis"
    )
    p.add_argument(
        "--export-improvements",
        help="Export improvement recommendations to file"
    )
    
    return p


def run_golden_tests(args: argparse.Namespace) -> int:
    """Run golden test suite."""
    print("=== Golden Test Suite ===")
    
    # Initialize test suite
    test_suite = GoldenTestSuite()
    
    # Load test cases if specified
    if args.load_tests:
        try:
            test_suite.load_test_cases(args.load_tests)
            print(f"Loaded test cases from: {args.load_tests}")
        except Exception as e:
            print(f"Error loading test cases: {e}")
            return 1
    
    # Run specific scenario or all tests
    if args.test_scenario:
        scenario = TestScenario(args.test_scenario)
        test_cases = test_suite.get_test_cases_by_scenario(scenario)
        print(f"Running {len(test_cases)} test cases for scenario: {scenario.value}")
    else:
        test_cases = test_suite.get_all_test_cases()
        print(f"Running all {len(test_cases)} test cases")
    
    # Display test summary
    summary = test_suite.get_test_summary()
    print(f"\nTest Suite Summary:")
    print(f"  Total test cases: {summary['total_test_cases']}")
    print(f"  Scenarios: {len(summary['scenarios'])}")
    print(f"  Tags: {len(summary['tags'])}")
    
    # Display test cases by scenario
    print(f"\nTest Cases by Scenario:")
    for scenario_type in TestScenario:
        cases = test_suite.get_test_cases_by_scenario(scenario_type)
        print(f"  {scenario_type.value}: {len(cases)} cases")
    
    # Save test cases if specified
    if args.save_tests:
        try:
            test_suite.save_test_cases(args.save_tests)
            print(f"Saved test cases to: {args.save_tests}")
        except Exception as e:
            print(f"Error saving test cases: {e}")
            return 1
    
    print("\nGolden tests completed successfully!")
    return 0


def run_metrics_analysis(args: argparse.Namespace) -> int:
    """Run metrics collection and analysis."""
    print("=== Metrics Analysis ===")
    
    # Initialize metrics collector
    metrics_collector = MetricsCollector()
    
    # Load metrics if input file specified
    if args.metrics_input:
        try:
            metrics_collector.load_metrics(args.metrics_input)
            print(f"Loaded metrics from: {args.metrics_input}")
        except Exception as e:
            print(f"Error loading metrics: {e}")
            return 1
    
    # Generate sample metrics if none loaded
    if not metrics_collector.metrics_history:
        print("No metrics found. Generating sample metrics...")
        # This would normally collect real metrics
        print("Sample metrics generation not implemented in demo mode")
        return 1
    
    # Get aggregated metrics
    aggregated = metrics_collector.get_aggregated_metrics(args.aggregate)
    
    print(f"\nAggregated Metrics (last {args.aggregate} requests):")
    if aggregated:
        print(f"  Total requests: {aggregated.get('total_requests', 0)}")
        print(f"  Avg constraint satisfaction: {aggregated.get('avg_constraint_satisfaction', 0):.2%}")
        print(f"  Avg diversity: {aggregated.get('avg_diversity', 0):.2%}")
        print(f"  Avg latency: {aggregated.get('avg_latency', 0):.2f}s")
        print(f"  Avg cost: ${aggregated.get('avg_cost', 0):.3f}")
        print(f"  Avg quality: {aggregated.get('avg_quality', 0):.2%}")
    else:
        print("  No aggregated metrics available")
    
    # Save metrics if output specified
    if args.metrics_output:
        try:
            metrics_collector.save_metrics(args.metrics_output)
            print(f"Saved metrics to: {args.metrics_output}")
        except Exception as e:
            print(f"Error saving metrics: {e}")
            return 1
    
    print("\nMetrics analysis completed!")
    return 0


def run_monitoring(args: argparse.Namespace) -> int:
    """Run monitoring system."""
    print("=== Monitoring System ===")
    
    # Initialize monitoring system
    monitoring_system = MonitoringSystem()
    
    # Collect system metrics
    print("Collecting system metrics...")
    system_metrics = monitoring_system.collect_system_metrics()
    
    print(f"\nCurrent System Metrics:")
    print(f"  CPU usage: {system_metrics.cpu_usage:.1%}")
    print(f"  Memory usage: {system_metrics.memory_usage:.1%}")
    print(f"  Disk usage: {system_metrics.disk_usage:.1%}")
    print(f"  Active requests: {system_metrics.active_requests}")
    print(f"  Queue size: {system_metrics.queue_size}")
    print(f"  Error rate: {system_metrics.error_rate:.2%}")
    print(f"  Response time P95: {system_metrics.response_time_p95:.2f}s")
    print(f"  Throughput: {system_metrics.throughput:.2f} req/s")
    
    # Run health checks
    print("\nRunning health checks...")
    health_results = monitoring_system.run_health_checks()
    
    print(f"\nHealth Check Results:")
    for component, health_check in health_results.items():
        print(f"  {component}: {health_check.status.value} ({health_check.response_time:.3f}s)")
    
    # Get system health
    overall_health = monitoring_system.get_system_health()
    print(f"\nOverall System Health: {overall_health.value}")
    
    # Get recent alerts
    recent_alerts = monitoring_system.get_recent_alerts(hours=args.monitoring_hours)
    
    print(f"\nRecent Alerts (last {args.monitoring_hours} hours):")
    if recent_alerts:
        for alert in recent_alerts[:5]:  # Show first 5
            print(f"  [{alert.level.value.upper()}] {alert.component}: {alert.message}")
        if len(recent_alerts) > 5:
            print(f"  ... and {len(recent_alerts) - 5} more")
    else:
        print("  No recent alerts")
    
    # Get metrics summary
    metrics_summary = monitoring_system.get_metrics_summary(args.monitoring_hours)
    
    if metrics_summary:
        print(f"\nMetrics Summary (last {args.monitoring_hours} hours):")
        print(f"  Sample count: {metrics_summary.get('sample_count', 0)}")
        if 'cpu' in metrics_summary:
            print(f"  CPU: {metrics_summary['cpu']['mean']:.1%} avg, {metrics_summary['cpu']['max']:.1%} max")
        if 'memory' in metrics_summary:
            print(f"  Memory: {metrics_summary['memory']['mean']:.1%} avg, {metrics_summary['memory']['max']:.1%} max")
        if 'error_rate' in metrics_summary:
            print(f"  Error rate: {metrics_summary['error_rate']['mean']:.2%} avg")
    
    # Export monitoring data if specified
    if args.export_monitoring:
        try:
            monitoring_system.export_monitoring_data(args.export_monitoring)
            print(f"Exported monitoring data to: {args.export_monitoring}")
        except Exception as e:
            print(f"Error exporting monitoring data: {e}")
            return 1
    
    print("\nMonitoring completed!")
    return 0


def run_dashboard(args: argparse.Namespace) -> int:
    """Run dashboard generation."""
    print("=== Dashboard Generation ===")
    
    # Initialize components
    metrics_collector = MetricsCollector()
    monitoring_system = MonitoringSystem()
    dashboard = EvaluationDashboard(metrics_collector, monitoring_system)
    
    # Update dashboard data
    print(f"Updating {args.dashboard_id} dashboard...")
    dashboard.update_dashboard_data(args.dashboard_id)
    
    print(f"\nDashboard '{args.dashboard_id}' updated successfully!")
    
    # Export dashboard if specified
    if args.export_dashboard:
        try:
            dashboard.export_dashboard(args.dashboard_id, args.export_dashboard)
            print(f"Exported dashboard to: {args.export_dashboard}")
        except Exception as e:
            print(f"Error exporting dashboard: {e}")
            return 1
    
    print("\nDashboard generation completed!")
    return 0


def run_reports(args: argparse.Namespace) -> int:
    """Run report generation."""
    print("=== Report Generation ===")
    
    # Initialize components
    metrics_collector = MetricsCollector()
    monitoring_system = MonitoringSystem()
    dashboard = EvaluationDashboard(metrics_collector, monitoring_system)
    
    # Generate report
    report_type = ReportType(args.report_type) if args.report_type else ReportType.QUALITY_SUMMARY
    print(f"Generating {report_type.value} report...")
    
    report = dashboard.generate_report(report_type, args.report_hours)
    
    print(f"\nReport Summary:")
    print(f"  Type: {report.get('report_type', 'unknown')}")
    print(f"  Generated at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(report.get('generated_at', time.time())))}")
    print(f"  Time period: {report.get('time_period_hours', 'unknown')} hours")
    
    # Display key metrics based on report type
    if report_type == ReportType.QUALITY_SUMMARY:
        exec_summary = report.get('executive_summary', {})
        print(f"  Overall quality: {exec_summary.get('overall_quality_score', 0):.2%}")
        print(f"  Constraint satisfaction: {exec_summary.get('constraint_satisfaction', 0):.2%}")
        print(f"  Diversity: {exec_summary.get('diversity_score', 0):.2%}")
    
    elif report_type == ReportType.PERFORMANCE_ANALYSIS:
        perf_summary = report.get('performance_summary', {})
        print(f"  Avg response time: {perf_summary.get('avg_response_time', 0):.2f}s")
        print(f"  Throughput: {perf_summary.get('throughput', 0):.2f} req/s")
        print(f"  Error rate: {perf_summary.get('error_rate', 0):.2%}")
    
    # Export report if specified
    if args.export_report:
        try:
            dashboard.export_report(report_type, args.export_report, args.report_hours)
            print(f"Exported report to: {args.export_report}")
        except Exception as e:
            print(f"Error exporting report: {e}")
            return 1
    
    print("\nReport generation completed!")
    return 0


def run_quality_improvement(args: argparse.Namespace) -> int:
    """Run quality improvement analysis."""
    print("=== Quality Improvement Analysis ===")
    
    # Initialize components
    metrics_collector = MetricsCollector()
    monitoring_system = MonitoringSystem()
    quality_engine = QualityImprovementEngine(metrics_collector, monitoring_system)
    
    # Analyze system quality
    print(f"Analyzing system quality (last {args.quality_hours} hours)...")
    quality_analysis = quality_engine.analyze_system_quality(args.quality_hours)
    
    print(f"\nQuality Analysis Results:")
    print(f"  Overall quality score: {quality_analysis.get('overall_quality_score', 0):.2%}")
    
    # Display dimension analysis
    dimensions = quality_analysis.get('dimension_analysis', {})
    for dim_name, dim_data in dimensions.items():
        if isinstance(dim_data, dict) and 'avg' in str(dim_data):
            print(f"  {dim_name}: {dim_data}")
    
    # Generate improvement recommendations
    print("\nGenerating improvement recommendations...")
    recommendations = quality_engine.generate_improvement_recommendations(args.quality_hours)
    
    print(f"\nImprovement Recommendations ({len(recommendations)} found):")
    for i, rec in enumerate(recommendations[:5]):  # Show first 5
        print(f"  {i+1}. [{rec.priority.value.upper()}] {rec.title}")
        print(f"     Impact: {rec.estimated_impact:.1%}, Effort: {rec.estimated_effort:.1%}")
        print(f"     {rec.description}")
    
    if len(recommendations) > 5:
        print(f"  ... and {len(recommendations) - 5} more recommendations")
    
    # Export recommendations if specified
    if args.export_improvements:
        try:
            quality_engine.export_improvement_plan(args.export_improvements)
            print(f"Exported improvement plan to: {args.export_improvements}")
        except Exception as e:
            print(f"Error exporting improvement plan: {e}")
            return 1
    
    print("\nQuality improvement analysis completed!")
    return 0


def run_all(args: argparse.Namespace) -> int:
    """Run all Phase 6 components."""
    print("=== Complete Phase 6 Evaluation ===")
    
    results = {}
    
    # Run golden tests
    print("\n1. Running Golden Tests...")
    try:
        results['golden_tests'] = run_golden_tests(args)
    except Exception as e:
        print(f"Error in golden tests: {e}")
        results['golden_tests'] = 1
    
    # Run metrics analysis
    print("\n2. Running Metrics Analysis...")
    try:
        results['metrics'] = run_metrics_analysis(args)
    except Exception as e:
        print(f"Error in metrics analysis: {e}")
        results['metrics'] = 1
    
    # Run monitoring
    print("\n3. Running Monitoring...")
    try:
        results['monitoring'] = run_monitoring(args)
    except Exception as e:
        print(f"Error in monitoring: {e}")
        results['monitoring'] = 1
    
    # Run dashboard generation
    print("\n4. Running Dashboard Generation...")
    try:
        results['dashboard'] = run_dashboard(args)
    except Exception as e:
        print(f"Error in dashboard generation: {e}")
        results['dashboard'] = 1
    
    # Run reports
    print("\n5. Running Report Generation...")
    try:
        results['reports'] = run_reports(args)
    except Exception as e:
        print(f"Error in report generation: {e}")
        results['reports'] = 1
    
    # Run quality improvement
    print("\n6. Running Quality Improvement Analysis...")
    try:
        results['quality'] = run_quality_improvement(args)
    except Exception as e:
        print(f"Error in quality improvement: {e}")
        results['quality'] = 1
    
    # Summary
    print("\n=== Phase 6 Complete Summary ===")
    for component, result in results.items():
        status = "SUCCESS" if result == 0 else "FAILED"
        print(f"  {component}: {status}")
    
    overall_success = all(result == 0 for result in results.values())
    print(f"\nOverall: {'SUCCESS' if overall_success else 'FAILED'}")
    
    return 0 if overall_success else 1


def main(argv: list[str] | None = None) -> int:
    """Main entry point for Phase 6."""
    args = build_parser().parse_args(argv)
    
    try:
        if args.action == "golden-tests":
            return run_golden_tests(args)
        elif args.action == "metrics":
            return run_metrics_analysis(args)
        elif args.action == "monitoring":
            return run_monitoring(args)
        elif args.action == "dashboard":
            return run_dashboard(args)
        elif args.action == "reports":
            return run_reports(args)
        elif args.action == "quality":
            return run_quality_improvement(args)
        elif args.action == "all":
            return run_all(args)
        else:
            print(f"Unknown action: {args.action}")
            return 1
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
