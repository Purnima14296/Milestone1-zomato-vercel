# Phase 6: Evaluation, Monitoring & Iteration (Quality Loop)

This folder contains the implementation of Phase 6 - the comprehensive evaluation, monitoring, and quality improvement system for the restaurant recommendation system. Phase 6 provides tools for measuring system performance, tracking metrics, and generating actionable insights for continuous improvement.

## Features

### Core Components

#### 1. Golden Tests (`golden_tests.py`)
- **Comprehensive test suite** with repeatable test cases
- **Multiple scenarios**: Budget-focused, rating-focused, cuisine-specific, location edge cases, complex preferences
- **Test categorization**: Budget, Rating, Cuisine, Location, Complex, Constraint-heavy, Minimal, Extreme values
- **Test management**: Save/load test cases, generate summaries, filter by scenarios and tags

#### 2. Metrics Collection (`metrics.py`)
- **Constraint satisfaction metrics**: Location, budget, rating, cuisine compliance
- **Diversity metrics**: Cuisine, price, rating, location diversity analysis
- **Latency metrics**: Phase-by-phase timing, LLM latency, database performance
- **Cost metrics**: Total cost, LLM cost, API costs, cost per recommendation
- **Quality metrics**: Relevance, explanation quality, ranking consistency
- **Aggregated analytics**: Trends, distributions, performance insights

#### 3. Monitoring System (`monitoring.py`)
- **Real-time monitoring**: CPU, memory, disk usage, active requests
- **Health checks**: Component health monitoring with custom check functions
- **Alert system**: Multi-level alerts (INFO, WARNING, ERROR, CRITICAL) with callbacks
- **Performance tracking**: Request latency, throughput, error rates
- **System metrics**: Resource utilization, queue sizes, response times

#### 4. Evaluation Dashboard (`dashboard.py`)
- **Interactive dashboards**: Quality overview, performance monitoring
- **Real-time widgets**: Metrics, charts, tables, alerts
- **Comprehensive reports**: Quality summary, performance analysis, constraint analysis, diversity analysis, cost analysis
- **Export capabilities**: Dashboard configurations, report generation
- **Trend analysis**: Performance trends, anomaly detection

#### 5. Quality Improvement (`quality_improvement.py`)
- **Intelligent analysis**: Automated quality assessment and insight generation
- **Actionable recommendations**: Prioritized improvement suggestions with impact/effort estimates
- **Trend detection**: Quality trend analysis and anomaly detection
- **Implementation tracking**: Monitor improvement effectiveness
- **Continuous improvement**: Data-driven optimization recommendations

## Usage

### Command Line Interface

The main entry point is `main.py` which provides comprehensive CLI access to all Phase 6 functionality.

#### Basic Commands

```bash
# Run golden test suite
python phase6/main.py golden-tests

# Analyze metrics
python phase6/main.py metrics --metrics-input storage/metrics.json

# Run monitoring system
python phase6/main.py monitoring --monitoring-hours 24

# Generate dashboard
python phase6/main.py dashboard --dashboard-id quality

# Generate reports
python phase6/main.py reports --report-type quality_summary --report-hours 24

# Run quality improvement analysis
python phase6/main.py quality --quality-hours 24

# Run all components
python phase6/main.py all
```

#### Advanced Options

```bash
# Run specific test scenario
python phase6/main.py golden-tests --test-scenario budget_focused

# Save/load golden test cases
python phase6/main.py golden-tests --save-tests tests.json
python phase6/main.py golden-tests --load-tests tests.json

# Export monitoring data
python phase6/main.py monitoring --export-monitoring monitoring_data.json

# Generate specific report type
python phase6/main.py reports --report-type performance_analysis --export-report perf_report.json

# Export improvement recommendations
python phase6/main.py quality --export-improvements improvements.json
```

### Programmatic Usage

```python
from phase6.golden_tests import GoldenTestSuite
from phase6.metrics import MetricsCollector
from phase6.monitoring import MonitoringSystem
from phase6.dashboard import EvaluationDashboard
from phase6.quality_improvement import QualityImprovementEngine

# Initialize components
test_suite = GoldenTestSuite()
metrics_collector = MetricsCollector()
monitoring_system = MonitoringSystem()
dashboard = EvaluationDashboard(metrics_collector, monitoring_system)
quality_engine = QualityImprovementEngine(metrics_collector, monitoring_system)

# Run golden tests
test_cases = test_suite.get_all_test_cases()

# Collect metrics
system_metrics = metrics_collector.collect_system_metrics(
    request_id="req_123",
    preferences={"location": "Bellandur", "budget": {"max": 2000}},
    recommendations=[...],
    phase_timings={"phase1": 0.1, "phase2": 0.05, "phase3": 0.2, "phase4": 1.5, "phase5": 0.1},
    cost_data={"total_cost": 0.05, "llm_cost": 0.04, "tokens_used": 150}
)

# Generate quality improvement recommendations
recommendations = quality_engine.generate_improvement_recommendations()
```

## Architecture

### Component Integration

```
Phase 6 Architecture:
├── Golden Tests → Test Cases → Validation Results
├── Metrics Collection → System Metrics → Aggregated Analytics
├── Monitoring System → Real-time Alerts → Health Status
├── Dashboard → Visual Reports → Executive Insights
└── Quality Improvement → Analysis → Recommendations → Implementation Tracking
```

### Data Flow

1. **Data Collection**: Metrics, monitoring data, test results
2. **Analysis**: Statistical analysis, trend detection, anomaly identification
3. **Insight Generation**: Quality insights, performance patterns
4. **Recommendations**: Actionable improvement suggestions
5. **Visualization**: Dashboards, reports, alerts
6. **Feedback Loop**: Implementation tracking, impact measurement

## Report Types

### Available Reports

1. **Quality Summary**: Overall system quality assessment
2. **Performance Analysis**: System performance and resource utilization
3. **Constraint Analysis**: Constraint satisfaction and violation analysis
4. **Diversity Analysis**: Recommendation diversity metrics and trends
5. **Cost Analysis**: Cost efficiency and optimization opportunities
6. **Golden Tests**: Test suite execution results and analysis
7. **System Health**: Comprehensive health status and alert summary
8. **Trend Analysis**: Long-term trends and predictions

### Report Structure

Each report includes:
- Executive summary with key metrics
- Detailed analysis with visualizations
- Trend analysis and anomaly detection
- Actionable recommendations
- Success metrics and KPIs

## Quality Improvement Process

### 1. Analysis Phase
- Collect metrics from all system components
- Analyze quality dimensions (constraints, diversity, performance, cost)
- Detect anomalies and trends
- Generate quality insights

### 2. Recommendation Phase
- Prioritize improvements by impact and effort
- Generate actionable recommendations
- Define success metrics and timelines
- Identify dependencies and risks

### 3. Implementation Phase
- Track improvement implementation
- Monitor impact on quality metrics
- Adjust recommendations based on results
- Update quality thresholds and baselines

### 4. Continuous Improvement
- Regular quality assessments
- Automated recommendation generation
- Long-term trend monitoring
- Adaptive threshold adjustment

## Configuration

### Quality Thresholds

```python
quality_thresholds = {
    "min_quality_score": 0.8,           # Minimum acceptable quality
    "min_constraint_satisfaction": 0.9, # Minimum constraint satisfaction
    "min_diversity_score": 0.7,         # Minimum diversity
    "max_response_time_p95": 2.0,       # Maximum P95 response time (seconds)
    "max_error_rate": 0.05,             # Maximum error rate (5%)
    "max_cost_per_recommendation": 0.5   # Maximum cost per recommendation ($)
}
```

### Monitoring Thresholds

```python
thresholds = {
    "error_rate": 0.05,      # 5%
    "response_time_p95": 2.0, # 2 seconds
    "cpu_usage": 0.8,        # 80%
    "memory_usage": 0.85,     # 85%
    "disk_usage": 0.9,       # 90%
    "queue_size": 100
}
```

## Integration with Other Phases

### Phase 1-5 Integration
- **Phase 1**: Data quality metrics and validation
- **Phase 2**: Preference validation and normalization metrics
- **Phase 3**: Retrieval performance and candidate quality
- **Phase 4**: LLM performance and explanation quality
- **Phase 5**: User experience and presentation metrics

### Data Sources
- **System Metrics**: Performance, resource utilization
- **User Metrics**: Satisfaction, engagement, feedback
- **Business Metrics**: Cost, efficiency, ROI
- **Quality Metrics**: Constraint satisfaction, diversity, relevance

## Best Practices

### 1. Regular Monitoring
- Set up automated monitoring for all critical metrics
- Configure appropriate alert thresholds
- Monitor trends and anomalies
- Regular health checks

### 2. Quality Assurance
- Run golden tests regularly
- Track quality metrics over time
- Implement quality gates
- Continuous improvement process

### 3. Performance Optimization
- Monitor latency and throughput
- Identify bottlenecks early
- Optimize resource utilization
- Scale proactively

### 4. Cost Management
- Track costs per recommendation
- Monitor LLM usage and costs
- Implement cost controls
- Optimize for cost efficiency

## Troubleshooting

### Common Issues

1. **Missing Metrics Data**
   - Ensure metrics collection is properly configured
   - Check data pipeline integrity
   - Verify storage accessibility

2. **High Alert Volume**
   - Review alert thresholds
   - Implement alert suppression rules
   - Add alert correlation

3. **Quality Score Degradation**
   - Check constraint satisfaction rates
   - Review diversity metrics
   - Analyze performance impact

4. **Performance Issues**
   - Monitor resource utilization
   - Check for bottlenecks
   - Review system capacity

## Future Enhancements

### Planned Features
- **Machine Learning**: Predictive quality models
- **Advanced Analytics**: Root cause analysis, correlation analysis
- **Automated Optimization**: Self-tuning system parameters
- **Integration**: CI/CD pipeline integration, A/B testing
- **Visualization**: Advanced dashboards, real-time streaming

### Scalability
- Distributed monitoring
- Cloud-native deployment
- Microservices architecture
- Event-driven processing

---

Phase 6 provides the foundation for continuous quality improvement and operational excellence in the restaurant recommendation system. By implementing comprehensive monitoring, analysis, and improvement capabilities, it ensures the system maintains high quality standards and continues to evolve based on data-driven insights.
