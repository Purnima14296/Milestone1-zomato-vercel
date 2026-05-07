"""
Phase 7 Metadata API: System metadata and statistics endpoints.

This module implements endpoints for accessing system metadata, statistics,
and configuration information about the restaurant recommendation system.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
from fastapi import APIRouter, HTTPException, status

from models import (
    MetadataResponse,
    SystemMetadata,
    MetricsResponse,
    SystemMetrics,
    QualityMetrics,
    ErrorResponse
)


class MetadataAPI:
    """System metadata and statistics API endpoints."""
    
    def __init__(self):
        self.router = APIRouter(prefix="/api", tags=["metadata", "metrics"])
        self._setup_routes()
        
        # Load system configuration
        self.system_config = self._load_system_config()
    
    def _setup_routes(self) -> None:
        """Setup metadata and metrics routes."""
        # Metadata endpoints
        self.router.add_api_route(
            "/metadata", 
            self.get_system_metadata, 
            methods=["GET"],
            response_model=MetadataResponse,
            summary="Get system metadata",
            description="Get system information, capabilities, and configuration"
        )
        
        # Metrics endpoints
        self.router.add_api_route(
            "/metrics", 
            self.get_system_metrics, 
            methods=["GET"],
            response_model=MetricsResponse,
            summary="Get system metrics",
            description="Get system performance and quality metrics"
        )
        
        self.router.add_api_route(
            "/stats", 
            self.get_statistics, 
            methods=["GET"],
            summary="Get system statistics",
            description="Get detailed system statistics and usage information"
        )
        
        self.router.add_api_route(
            "/config", 
            self.get_configuration, 
            methods=["GET"],
            summary="Get system configuration",
            description="Get system configuration and feature flags"
        )
    
    async def get_system_metadata(self) -> MetadataResponse:
        """
        Get system metadata and capabilities.
        
        Returns:
            MetadataResponse with system information
        """
        try:
            # Get system statistics
            stats = self._get_system_statistics()
            
            # Create system metadata
            system_metadata = SystemMetadata(
                version="1.0.0",
                description="AI-Powered Restaurant Recommendation System",
                total_restaurants=stats["total_restaurants"],
                total_recommendations=stats["total_recommendations"],
                supported_cuisines=stats["supported_cuisines"],
                supported_locations=stats["supported_locations"],
                features=[
                    "AI-powered recommendations",
                    "Multi-cuisine support",
                    "Budget-based filtering",
                    "Rating-based sorting",
                    "Location-specific results",
                    "Real-time processing",
                    "Quality metrics",
                    "Performance monitoring"
                ]
            )
            
            return MetadataResponse(
                system=system_metadata,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get system metadata: {str(e)}"
            )
    
    async def get_system_metrics(self, hours: int = 24) -> MetricsResponse:
        """
        Get system performance and quality metrics.
        
        Args:
            hours: Number of hours of metrics to return
            
        Returns:
            MetricsResponse with system and quality metrics
        """
        try:
            # Get system metrics
            system_metrics = await self._collect_system_metrics()
            
            # Get quality metrics
            quality_metrics = await self._collect_quality_metrics(hours)
            
            return MetricsResponse(
                timestamp=datetime.utcnow(),
                system=system_metrics,
                quality=quality_metrics,
                period_hours=hours
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get system metrics: {str(e)}"
            )
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get detailed system statistics.
        
        Returns:
            Dictionary with detailed statistics
        """
        try:
            stats = self._get_system_statistics()
            
            # Add additional statistics
            stats.update({
                "api_endpoints": self._get_api_statistics(),
                "performance": self._get_performance_statistics(),
                "usage": self._get_usage_statistics(),
                "quality": self._get_quality_statistics()
            })
            
            return stats
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get system statistics: {str(e)}"
            )
    
    async def get_configuration(self) -> Dict[str, Any]:
        """
        Get system configuration and feature flags.
        
        Returns:
            Dictionary with system configuration
        """
        try:
            return {
                "api": {
                    "version": "1.0.0",
                    "base_url": "/api",
                    "max_top_k": 20,
                    "default_top_k": 5,
                    "rate_limit": {
                        "requests_per_minute": 100,
                        "requests_per_hour": 1000
                    }
                },
                "features": {
                    "recommendations": True,
                    "restaurant_search": True,
                    "preference_validation": True,
                    "health_checks": True,
                    "metrics_collection": True,
                    "caching": True,
                    "authentication": False  # Disabled for demo
                },
                "models": {
                    "llm_model": "llama-3.3-70b-versatile",
                    "embedding_model": None,
                    "recommendation_algorithm": "hybrid_llm_rule_based"
                },
                "data": {
                    "total_restaurants": 5000,
                    "supported_cities": 50,
                    "supported_cuisines": 25,
                    "data_update_frequency": "daily",
                    "cache_ttl": 3600
                },
                "performance": {
                    "max_response_time": 5.0,
                    "target_response_time": 2.0,
                    "max_concurrent_requests": 100,
                    "timeout": 30
                }
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get system configuration: {str(e)}"
            )
    
    def _load_system_config(self) -> Dict[str, Any]:
        """Load system configuration from file or use defaults."""
        config_path = Path(__file__).parent.parent / "config" / "system_config.json"
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default configuration
        return {
            "system": {
                "name": "Zomato Restaurant Recommendation System",
                "version": "1.0.0",
                "description": "AI-powered restaurant recommendation system"
            },
            "data": {
                "restaurants_file": "storage/restaurants.json",
                "recommendations_file": "storage/recommendations.json"
            }
        }
    
    def _get_system_statistics(self) -> Dict[str, Any]:
        """Get basic system statistics."""
        # In production, this would query the database
        return {
            "total_restaurants": 5000,
            "total_recommendations": 12500,
            "supported_cuisines": [
                "North Indian", "South Indian", "Chinese", "Italian", 
                "Continental", "Mexican", "Thai", "Japanese", "BBQ",
                "Mediterranean", "European", "Asian", "Goan", "Fusion",
                "Cafe", "Fast Food", "Healthy Food", "Seafood"
            ],
            "supported_locations": [
                "Bellandur", "Indiranagar", "Koramangala", "HSR Layout",
                "Jayanagar", "Marathahalli", "Whitefield", "MG Road",
                "Electronic City", "BTM Layout", "Basavanagudi"
            ],
            "average_rating": 4.2,
            "average_cost": 1200,
            "total_users": 2500
        }
    
    def _get_api_statistics(self) -> Dict[str, Any]:
        """Get API endpoint statistics."""
        return {
            "total_endpoints": 8,
            "endpoints": {
                "health": {
                    "path": "/api/health",
                    "methods": ["GET"],
                    "calls": 1500,
                    "avg_response_time": 0.05
                },
                "recommendations": {
                    "path": "/api/recommendations",
                    "methods": ["POST", "GET"],
                    "calls": 8500,
                    "avg_response_time": 1.2
                },
                "restaurants": {
                    "path": "/api/restaurants/search",
                    "methods": ["GET"],
                    "calls": 3200,
                    "avg_response_time": 0.3
                },
                "preferences": {
                    "path": "/api/preferences/validate",
                    "methods": ["POST"],
                    "calls": 1800,
                    "avg_response_time": 0.1
                },
                "metadata": {
                    "path": "/api/metadata",
                    "methods": ["GET"],
                    "calls": 500,
                    "avg_response_time": 0.08
                },
                "metrics": {
                    "path": "/api/metrics",
                    "methods": ["GET"],
                    "calls": 300,
                    "avg_response_time": 0.15
                }
            }
        }
    
    def _get_performance_statistics(self) -> Dict[str, Any]:
        """Get performance statistics."""
        return {
            "response_times": {
                "p50": 0.8,
                "p95": 2.1,
                "p99": 4.5,
                "average": 1.1
            },
            "throughput": {
                "requests_per_second": 15.5,
                "requests_per_minute": 930,
                "peak_rps": 45.2
            },
            "error_rates": {
                "overall": 0.02,
                "timeout_errors": 0.005,
                "validation_errors": 0.015
            },
            "availability": {
                "uptime_percentage": 99.8,
                "downtime_minutes": 12
            }
        }
    
    def _get_usage_statistics(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return {
            "daily_requests": 2200,
            "weekly_requests": 15400,
            "monthly_requests": 66000,
            "popular_locations": [
                {"location": "Bellandur", "requests": 850},
                {"location": "Indiranagar", "requests": 720},
                {"location": "Koramangala", "requests": 680}
            ],
            "popular_cuisines": [
                {"cuisine": "North Indian", "requests": 1200},
                {"cuisine": "Chinese", "requests": 980},
                {"cuisine": "Italian", "requests": 750}
            ],
            "user_demographics": {
                "new_users_today": 45,
                "active_users_today": 180,
                "returning_users": 0.72
            }
        }
    
    def _get_quality_statistics(self) -> Dict[str, Any]:
        """Get quality statistics."""
        return {
            "constraint_satisfaction": {
                "location": 0.95,
                "budget": 0.88,
                "rating": 0.92,
                "cuisine": 0.85,
                "overall": 0.90
            },
            "diversity_metrics": {
                "cuisine_diversity": 0.78,
                "price_diversity": 0.82,
                "rating_diversity": 0.65,
                "overall_diversity": 0.75
            },
            "user_satisfaction": {
                "average_rating": 4.3,
                "click_through_rate": 0.68,
                "conversion_rate": 0.24,
                "feedback_sentiment": 0.71
            }
        }
    
    async def _collect_system_metrics(self) -> SystemMetrics:
        """Collect system performance metrics."""
        # In production, this would collect real system metrics
        import psutil
        
        return SystemMetrics(
            cpu_usage=psutil.cpu_percent(),
            memory_usage=psutil.virtual_memory().percent,
            disk_usage=psutil.disk_usage('/').percent,
            active_requests=12,
            total_requests=15420,
            avg_response_time=1.1,
            error_rate=0.02
        )
    
    async def _collect_quality_metrics(self, hours: int) -> QualityMetrics:
        """Collect quality metrics."""
        # In production, this would collect real quality metrics
        return QualityMetrics(
            constraint_satisfaction=0.90,
            diversity_score=0.75,
            avg_quality_score=0.85,
            total_recommendations=12500
        )
