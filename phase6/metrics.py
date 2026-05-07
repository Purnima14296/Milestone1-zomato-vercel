"""
Phase 6 Metrics: Comprehensive metrics collection and analysis system.

This module provides detailed metrics collection for the restaurant recommendation
system, including constraint satisfaction, diversity measurement, latency tracking,
and cost analysis for quality monitoring and improvement.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
from collections import defaultdict, Counter


class MetricType(Enum):
    """Enumeration of metric types."""
    CONSTRAINT_SATISFACTION = "constraint_satisfaction"
    DIVERSITY = "diversity"
    LATENCY = "latency"
    COST = "cost"
    QUALITY = "quality"
    USER_SATISFACTION = "user_satisfaction"


@dataclass
class ConstraintMetrics:
    """Metrics for constraint satisfaction analysis."""
    location_satisfaction: float  # 0-1
    budget_satisfaction: float   # 0-1
    rating_satisfaction: float    # 0-1
    cuisine_satisfaction: float   # 0-1
    overall_satisfaction: float    # 0-1
    violated_constraints: List[str]
    partially_satisfied: List[str]
    fully_satisfied: List[str]


@dataclass
class DiversityMetrics:
    """Metrics for result diversity analysis."""
    cuisine_diversity: float      # 0-1
    price_diversity: float        # 0-1
    rating_diversity: float       # 0-1
    location_diversity: float     # 0-1
    overall_diversity: float      # 0-1
    unique_cuisines: int
    price_range: Tuple[float, float]
    rating_range: Tuple[float, float]
    unique_locations: int


@dataclass
class LatencyMetrics:
    """Metrics for performance and latency analysis."""
    total_latency: float         # seconds
    phase1_latency: float        # seconds
    phase2_latency: float        # seconds
    phase3_latency: float        # seconds
    phase4_latency: float        # seconds
    phase5_latency: float        # seconds
    llm_latency: float           # seconds
    database_latency: float      # seconds
    api_overhead: float         # seconds


@dataclass
class CostMetrics:
    """Metrics for cost analysis."""
    total_cost: float           # currency units
    llm_cost: float             # currency units
    api_calls_cost: float       # currency units
    storage_cost: float         # currency units
    compute_cost: float         # currency units
    tokens_used: int
    cost_per_recommendation: float


@dataclass
class QualityMetrics:
    """Metrics for overall quality assessment."""
    relevance_score: float      # 0-1
    explanation_quality: float  # 0-1
    ranking_consistency: float  # 0-1
    user_intent_match: float    # 0-1
    overall_quality: float      # 0-1


@dataclass
class UserSatisfactionMetrics:
    """Metrics for user satisfaction analysis."""
    click_through_rate: float   # 0-1
    conversion_rate: float      # 0-1
    user_ratings: float         # 1-5
    feedback_sentiment: float   # -1 to 1
    retention_rate: float       # 0-1


@dataclass
class SystemMetrics:
    """Comprehensive system metrics for a single recommendation request."""
    request_id: str
    timestamp: float
    user_preferences: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    constraint_metrics: ConstraintMetrics
    diversity_metrics: DiversityMetrics
    latency_metrics: LatencyMetrics
    cost_metrics: CostMetrics
    quality_metrics: QualityMetrics
    user_satisfaction_metrics: Optional[UserSatisfactionMetrics]


class MetricsCollector:
    """
    Comprehensive metrics collection and analysis system.
    
    Collects, analyzes, and stores metrics for quality monitoring
    and continuous improvement of the recommendation system.
    """
    
    def __init__(self):
        self.metrics_history: List[SystemMetrics] = []
        self.aggregated_metrics: Dict[str, Any] = {}
    
    def collect_constraint_metrics(
        self, 
        preferences: Dict[str, Any], 
        recommendations: List[Dict[str, Any]]
    ) -> ConstraintMetrics:
        """
        Collect constraint satisfaction metrics.
        
        Args:
            preferences: User preferences
            recommendations: Generated recommendations
            
        Returns:
            ConstraintMetrics object
        """
        violated = []
        partial = []
        satisfied = []
        
        # Location constraint
        location_sat = self._check_location_constraint(preferences, recommendations)
        if location_sat >= 0.9:
            satisfied.append("location")
        elif location_sat >= 0.5:
            partial.append("location")
        else:
            violated.append("location")
        
        # Budget constraint
        budget_sat = self._check_budget_constraint(preferences, recommendations)
        if budget_sat >= 0.9:
            satisfied.append("budget")
        elif budget_sat >= 0.5:
            partial.append("budget")
        else:
            violated.append("budget")
        
        # Rating constraint
        rating_sat = self._check_rating_constraint(preferences, recommendations)
        if rating_sat >= 0.9:
            satisfied.append("rating")
        elif rating_sat >= 0.5:
            partial.append("rating")
        else:
            violated.append("rating")
        
        # Cuisine constraint
        cuisine_sat = self._check_cuisine_constraint(preferences, recommendations)
        if cuisine_sat >= 0.9:
            satisfied.append("cuisine")
        elif cuisine_sat >= 0.5:
            partial.append("cuisine")
        else:
            violated.append("cuisine")
        
        overall_sat = (location_sat + budget_sat + rating_sat + cuisine_sat) / 4
        
        return ConstraintMetrics(
            location_satisfaction=location_sat,
            budget_satisfaction=budget_sat,
            rating_satisfaction=rating_sat,
            cuisine_satisfaction=cuisine_sat,
            overall_satisfaction=overall_sat,
            violated_constraints=violated,
            partially_satisfied=partial,
            fully_satisfied=satisfied
        )
    
    def collect_diversity_metrics(
        self, 
        recommendations: List[Dict[str, Any]]
    ) -> DiversityMetrics:
        """
        Collect diversity metrics for recommendations.
        
        Args:
            recommendations: Generated recommendations
            
        Returns:
            DiversityMetrics object
        """
        if not recommendations:
            return DiversityMetrics(0, 0, 0, 0, 0, 0, (0, 0), (0, 0), 0)
        
        # Extract data
        cuisines = []
        prices = []
        ratings = []
        locations = []
        
        for rec in recommendations:
            # Cuisines
            rec_cuisines = rec.get("cuisines", [])
            if isinstance(rec_cuisines, str):
                rec_cuisines = [rec_cuisines]
            cuisines.extend(rec_cuisines)
            
            # Price
            price = rec.get("cost_estimate", 0)
            prices.append(price)
            
            # Rating
            rating = rec.get("rating", 0)
            ratings.append(rating)
            
            # Location
            location = rec.get("city", "")
            locations.append(location)
        
        # Calculate diversity metrics
        cuisine_diversity = self._calculate_cuisine_diversity(cuisines)
        price_diversity = self._calculate_price_diversity(prices)
        rating_diversity = self._calculate_rating_diversity(ratings)
        location_diversity = self._calculate_location_diversity(locations)
        
        overall_diversity = (cuisine_diversity + price_diversity + rating_diversity + location_diversity) / 4
        
        unique_cuisines = len(set(str(c).strip("'\"[]") for c in cuisines))
        price_range = (min(prices), max(prices)) if prices else (0, 0)
        rating_range = (min(ratings), max(ratings)) if ratings else (0, 0)
        unique_locations = len(set(locations))
        
        return DiversityMetrics(
            cuisine_diversity=cuisine_diversity,
            price_diversity=price_diversity,
            rating_diversity=rating_diversity,
            location_diversity=location_diversity,
            overall_diversity=overall_diversity,
            unique_cuisines=unique_cuisines,
            price_range=price_range,
            rating_range=rating_range,
            unique_locations=unique_locations
        )
    
    def collect_latency_metrics(
        self, 
        phase_timings: Dict[str, float]
    ) -> LatencyMetrics:
        """
        Collect latency metrics for system performance.
        
        Args:
            phase_timings: Dictionary of timing data for each phase
            
        Returns:
            LatencyMetrics object
        """
        total = sum(phase_timings.values())
        
        return LatencyMetrics(
            total_latency=total,
            phase1_latency=phase_timings.get("phase1", 0),
            phase2_latency=phase_timings.get("phase2", 0),
            phase3_latency=phase_timings.get("phase3", 0),
            phase4_latency=phase_timings.get("phase4", 0),
            phase5_latency=phase_timings.get("phase5", 0),
            llm_latency=phase_timings.get("llm", 0),
            database_latency=phase_timings.get("database", 0),
            api_overhead=phase_timings.get("api", 0)
        )
    
    def collect_cost_metrics(
        self, 
        cost_data: Dict[str, Any]
    ) -> CostMetrics:
        """
        Collect cost metrics for financial analysis.
        
        Args:
            cost_data: Dictionary containing cost information
            
        Returns:
            CostMetrics object
        """
        total_cost = cost_data.get("total_cost", 0)
        num_recommendations = cost_data.get("num_recommendations", 1)
        
        return CostMetrics(
            total_cost=total_cost,
            llm_cost=cost_data.get("llm_cost", 0),
            api_calls_cost=cost_data.get("api_calls_cost", 0),
            storage_cost=cost_data.get("storage_cost", 0),
            compute_cost=cost_data.get("compute_cost", 0),
            tokens_used=cost_data.get("tokens_used", 0),
            cost_per_recommendation=total_cost / num_recommendations if num_recommendations > 0 else 0
        )
    
    def collect_quality_metrics(
        self, 
        preferences: Dict[str, Any], 
        recommendations: List[Dict[str, Any]]
    ) -> QualityMetrics:
        """
        Collect quality metrics for recommendation assessment.
        
        Args:
            preferences: User preferences
            recommendations: Generated recommendations
            
        Returns:
            QualityMetrics object
        """
        relevance_score = self._calculate_relevance_score(preferences, recommendations)
        explanation_quality = self._calculate_explanation_quality(recommendations)
        ranking_consistency = self._calculate_ranking_consistency(recommendations)
        user_intent_match = self._calculate_user_intent_match(preferences, recommendations)
        
        overall_quality = (relevance_score + explanation_quality + ranking_consistency + user_intent_match) / 4
        
        return QualityMetrics(
            relevance_score=relevance_score,
            explanation_quality=explanation_quality,
            ranking_consistency=ranking_consistency,
            user_intent_match=user_intent_match,
            overall_quality=overall_quality
        )
    
    def collect_system_metrics(
        self, 
        request_id: str,
        preferences: Dict[str, Any],
        recommendations: List[Dict[str, Any]],
        phase_timings: Dict[str, float],
        cost_data: Dict[str, Any]
    ) -> SystemMetrics:
        """
        Collect comprehensive system metrics for a single request.
        
        Args:
            request_id: Unique identifier for the request
            preferences: User preferences
            recommendations: Generated recommendations
            phase_timings: Timing data for each phase
            cost_data: Cost information
            
        Returns:
            SystemMetrics object
        """
        constraint_metrics = self.collect_constraint_metrics(preferences, recommendations)
        diversity_metrics = self.collect_diversity_metrics(recommendations)
        latency_metrics = self.collect_latency_metrics(phase_timings)
        cost_metrics = self.collect_cost_metrics(cost_data)
        quality_metrics = self.collect_quality_metrics(preferences, recommendations)
        
        system_metrics = SystemMetrics(
            request_id=request_id,
            timestamp=time.time(),
            user_preferences=preferences,
            recommendations=recommendations,
            constraint_metrics=constraint_metrics,
            diversity_metrics=diversity_metrics,
            latency_metrics=latency_metrics,
            cost_metrics=cost_metrics,
            quality_metrics=quality_metrics,
            user_satisfaction_metrics=None
        )
        
        self.metrics_history.append(system_metrics)
        return system_metrics
    
    def get_aggregated_metrics(self, num_recent: int = 100) -> Dict[str, Any]:
        """
        Get aggregated metrics from recent history.
        
        Args:
            num_recent: Number of recent metrics to aggregate
            
        Returns:
            Dictionary of aggregated metrics
        """
        recent_metrics = self.metrics_history[-num_recent:] if self.metrics_history else []
        
        if not recent_metrics:
            return {}
        
        # Aggregate constraint metrics
        constraint_sats = [m.constraint_metrics.overall_satisfaction for m in recent_metrics]
        avg_constraint_sat = statistics.mean(constraint_sats) if constraint_sats else 0
        
        # Aggregate diversity metrics
        diversity_scores = [m.diversity_metrics.overall_diversity for m in recent_metrics]
        avg_diversity = statistics.mean(diversity_scores) if diversity_scores else 0
        
        # Aggregate latency metrics
        total_latencies = [m.latency_metrics.total_latency for m in recent_metrics]
        avg_latency = statistics.mean(total_latencies) if total_latencies else 0
        
        # Aggregate cost metrics
        total_costs = [m.cost_metrics.total_cost for m in recent_metrics]
        avg_cost = statistics.mean(total_costs) if total_costs else 0
        
        # Aggregate quality metrics
        quality_scores = [m.quality_metrics.overall_quality for m in recent_metrics]
        avg_quality = statistics.mean(quality_scores) if quality_scores else 0
        
        return {
            "total_requests": len(recent_metrics),
            "avg_constraint_satisfaction": avg_constraint_sat,
            "avg_diversity": avg_diversity,
            "avg_latency": avg_latency,
            "avg_cost": avg_cost,
            "avg_quality": avg_quality,
            "constraint_distribution": self._get_constraint_distribution(recent_metrics),
            "diversity_trends": self._get_diversity_trends(recent_metrics),
            "performance_trends": self._get_performance_trends(recent_metrics)
        }
    
    def save_metrics(self, file_path: str) -> None:
        """Save metrics history to JSON file."""
        metrics_data = []
        for m in self.metrics_history:
            metrics_data.append({
                "request_id": m.request_id,
                "timestamp": m.timestamp,
                "user_preferences": m.user_preferences,
                "recommendations": m.recommendations,
                "constraint_metrics": asdict(m.constraint_metrics),
                "diversity_metrics": asdict(m.diversity_metrics),
                "latency_metrics": asdict(m.latency_metrics),
                "cost_metrics": asdict(m.cost_metrics),
                "quality_metrics": asdict(m.quality_metrics),
                "user_satisfaction_metrics": asdict(m.user_satisfaction_metrics) if m.user_satisfaction_metrics else None
            })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2, ensure_ascii=False)
    
    def load_metrics(self, file_path: str) -> None:
        """Load metrics history from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            metrics_data = json.load(f)
        
        self.metrics_history = []
        for item in metrics_data:
            system_metrics = SystemMetrics(
                request_id=item["request_id"],
                timestamp=item["timestamp"],
                user_preferences=item["user_preferences"],
                recommendations=item["recommendations"],
                constraint_metrics=ConstraintMetrics(**item["constraint_metrics"]),
                diversity_metrics=DiversityMetrics(**item["diversity_metrics"]),
                latency_metrics=LatencyMetrics(**item["latency_metrics"]),
                cost_metrics=CostMetrics(**item["cost_metrics"]),
                quality_metrics=QualityMetrics(**item["quality_metrics"]),
                user_satisfaction_metrics=UserSatisfactionMetrics(**item["user_satisfaction_metrics"]) if item["user_satisfaction_metrics"] else None
            )
            self.metrics_history.append(system_metrics)
    
    # Helper methods for metric calculations
    def _check_location_constraint(self, preferences: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> float:
        """Check location constraint satisfaction."""
        target_location = preferences.get("location", "").lower()
        if not target_location:
            return 1.0
        
        matching = 0
        for rec in recommendations:
            location = rec.get("city", "").lower()
            if target_location in location:
                matching += 1
        
        return matching / len(recommendations) if recommendations else 0
    
    def _check_budget_constraint(self, preferences: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> float:
        """Check budget constraint satisfaction."""
        budget = preferences.get("budget", {})
        if not isinstance(budget, dict):
            return 1.0
        
        max_budget = budget.get("max", float('inf'))
        if max_budget == float('inf'):
            return 1.0
        
        matching = 0
        for rec in recommendations:
            cost = rec.get("cost_estimate", 0)
            if cost <= max_budget:
                matching += 1
        
        return matching / len(recommendations) if recommendations else 0
    
    def _check_rating_constraint(self, preferences: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> float:
        """Check rating constraint satisfaction."""
        min_rating = preferences.get("minimum_rating", 0)
        
        matching = 0
        for rec in recommendations:
            rating = rec.get("rating", 0)
            if rating >= min_rating:
                matching += 1
        
        return matching / len(recommendations) if recommendations else 0
    
    def _check_cuisine_constraint(self, preferences: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> float:
        """Check cuisine constraint satisfaction."""
        target_cuisines = preferences.get("cuisines", [])
        if not target_cuisines:
            return 1.0
        
        matching = 0
        for rec in recommendations:
            rec_cuisines = rec.get("cuisines", [])
            if isinstance(rec_cuisines, str):
                rec_cuisines = [rec_cuisines]
            
            rec_cuisines_clean = [str(c).strip("'\"[]") for c in rec_cuisines]
            
            if any(target.lower() in cuisine.lower() for target in target_cuisines for cuisine in rec_cuisines_clean):
                matching += 1
        
        return matching / len(recommendations) if recommendations else 0
    
    def _calculate_cuisine_diversity(self, cuisines: List[str]) -> float:
        """Calculate cuisine diversity using entropy."""
        if not cuisines:
            return 0
        
        # Clean and normalize cuisines
        clean_cuisines = [str(c).strip("'\"[]") for c in cuisines]
        cuisine_counts = Counter(clean_cuisines)
        total = len(clean_cuisines)
        
        # Calculate entropy
        entropy = 0
        for count in cuisine_counts.values():
            probability = count / total
            entropy -= probability * (probability and statistics.log(probability, 2) or 0)
        
        # Normalize by maximum possible entropy
        max_entropy = statistics.log(len(cuisine_counts), 2) if len(cuisine_counts) > 1 else 0
        return entropy / max_entropy if max_entropy > 0 else 0
    
    def _calculate_price_diversity(self, prices: List[float]) -> float:
        """Calculate price diversity using coefficient of variation."""
        if not prices or len(prices) < 2:
            return 0
        
        mean_price = statistics.mean(prices)
        if mean_price == 0:
            return 0
        
        std_dev = statistics.stdev(prices)
        cv = std_dev / mean_price
        
        # Normalize to 0-1 scale
        return min(cv / 0.5, 1.0)  # Assuming CV of 0.5 is maximum diversity
    
    def _calculate_rating_diversity(self, ratings: List[float]) -> float:
        """Calculate rating diversity using range."""
        if not ratings or len(ratings) < 2:
            return 0
        
        rating_range = max(ratings) - min(ratings)
        # Normalize by maximum possible range (5.0 - 0.0 = 5.0)
        return min(rating_range / 5.0, 1.0)
    
    def _calculate_location_diversity(self, locations: List[str]) -> float:
        """Calculate location diversity using unique locations ratio."""
        if not locations:
            return 0
        
        unique_locations = len(set(locations))
        total_locations = len(locations)
        
        return unique_locations / total_locations
    
    def _calculate_relevance_score(self, preferences: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> float:
        """Calculate relevance score based on preference matching."""
        if not recommendations:
            return 0
        
        scores = []
        for rec in recommendations:
            score = 0
            
            # Location relevance
            target_location = preferences.get("location", "").lower()
            location = rec.get("city", "").lower()
            if target_location and target_location in location:
                score += 0.25
            
            # Budget relevance
            budget = preferences.get("budget", {})
            if isinstance(budget, dict):
                max_budget = budget.get("max", float('inf'))
                cost = rec.get("cost_estimate", 0)
                if cost <= max_budget:
                    score += 0.25
            
            # Rating relevance
            min_rating = preferences.get("minimum_rating", 0)
            rating = rec.get("rating", 0)
            if rating >= min_rating:
                score += 0.25
            
            # Cuisine relevance
            target_cuisines = preferences.get("cuisines", [])
            if target_cuisines:
                rec_cuisines = rec.get("cuisines", [])
                if isinstance(rec_cuisines, str):
                    rec_cuisines = [rec_cuisines]
                
                rec_cuisines_clean = [str(c).strip("'\"[]") for c in rec_cuisines]
                if any(target.lower() in cuisine.lower() for target in target_cuisines for cuisine in rec_cuisines_clean):
                    score += 0.25
            else:
                score += 0.25  # No cuisine constraint
            
            scores.append(score)
        
        return statistics.mean(scores) if scores else 0
    
    def _calculate_explanation_quality(self, recommendations: List[Dict[str, Any]]) -> float:
        """Calculate explanation quality based on length and content."""
        if not recommendations:
            return 0
        
        scores = []
        for rec in recommendations:
            explanation = rec.get("reason", "")
            if not explanation:
                scores.append(0)
                continue
            
            score = 0
            
            # Length check (not too short, not too long)
            if 20 <= len(explanation) <= 200:
                score += 0.3
            
            # Contains relevant keywords
            keywords = ["rating", "cost", "budget", "cuisine", "location", "recommend", "because"]
            keyword_count = sum(1 for keyword in keywords if keyword.lower() in explanation.lower())
            score += min(keyword_count / len(keywords), 0.4)
            
            # Contains specific numbers
            import re
            numbers = re.findall(r'\d+\.?\d*', explanation)
            if numbers:
                score += 0.3
            
            scores.append(score)
        
        return statistics.mean(scores) if scores else 0
    
    def _calculate_ranking_consistency(self, recommendations: List[Dict[str, Any]]) -> float:
        """Calculate ranking consistency based on rating and cost ordering."""
        if len(recommendations) < 2:
            return 1.0
        
        # Check if higher-ranked items have higher ratings
        rating_consistency = 0
        cost_consistency = 0
        
        for i in range(len(recommendations) - 1):
            current = recommendations[i]
            next_rec = recommendations[i + 1]
            
            # Higher rank should have higher or equal rating
            if current.get("rating", 0) >= next_rec.get("rating", 0):
                rating_consistency += 1
            
            # For cost, lower cost should be ranked higher (optional)
            # This is more complex, so we'll focus on rating consistency
        
        rating_score = rating_consistency / (len(recommendations) - 1)
        return rating_score
    
    def _calculate_user_intent_match(self, preferences: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> float:
        """Calculate how well recommendations match user intent."""
        # This is a simplified version - in practice, this could use ML models
        constraint_score = self._check_location_constraint(preferences, recommendations)
        budget_score = self._check_budget_constraint(preferences, recommendations)
        rating_score = self._check_rating_constraint(preferences, recommendations)
        cuisine_score = self._check_cuisine_constraint(preferences, recommendations)
        
        return (constraint_score + budget_score + rating_score + cuisine_score) / 4
    
    def _get_constraint_distribution(self, metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Get distribution of constraint satisfaction scores."""
        constraint_scores = [m.constraint_metrics.overall_satisfaction for m in metrics]
        
        return {
            "mean": statistics.mean(constraint_scores) if constraint_scores else 0,
            "median": statistics.median(constraint_scores) if constraint_scores else 0,
            "min": min(constraint_scores) if constraint_scores else 0,
            "max": max(constraint_scores) if constraint_scores else 0,
            "std_dev": statistics.stdev(constraint_scores) if len(constraint_scores) > 1 else 0
        }
    
    def _get_diversity_trends(self, metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Get diversity trends over time."""
        diversity_scores = [m.diversity_metrics.overall_diversity for m in metrics]
        
        return {
            "mean": statistics.mean(diversity_scores) if diversity_scores else 0,
            "trend": "improving" if len(diversity_scores) > 1 and diversity_scores[-1] > diversity_scores[0] else "stable"
        }
    
    def _get_performance_trends(self, metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Get performance trends over time."""
        latencies = [m.latency_metrics.total_latency for m in metrics]
        
        return {
            "mean_latency": statistics.mean(latencies) if latencies else 0,
            "trend": "improving" if len(latencies) > 1 and latencies[-1] < latencies[0] else "stable"
        }
